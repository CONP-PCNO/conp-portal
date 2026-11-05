#!/usr/bin/env bash

set -Eeuo pipefail

usage() {
    cat <<'USAGE'
Usage: db_backup.bash [--prefix PREFIX] [--gzip] [--output-dir DIRECTORY]

Dump the database configured by DATABASE_URL to a timestamped SQL file.

Options:
  -p, --prefix PREFIX   Add PREFIX_ before the timestamp in the filename
  -g, --gzip            Compress the SQL dump with gzip
  -o, --output-dir DIR  Write backups to DIR (default: DB_BACKUP_DIR or .)
  -h, --help            Show this help
USAGE
}

fail() {
    printf 'db_backup.bash: %s\n' "$*" >&2
    exit 1
}

prefix=
compress=false
output_dir=${DB_BACKUP_DIR:-.}
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
app_root=$(cd -- "$script_dir/../.." &>/dev/null && pwd)
env_file=
if [[ -f $app_root/.flaskenv ]]; then
    env_file=$app_root/.flaskenv
elif [[ -f $app_root/.env ]]; then
    env_file=$app_root/.env
fi

while (($#)); do
    case "$1" in
        -p|--prefix)
            (($# >= 2)) || fail "missing value for $1"
            prefix=$2
            shift 2
            ;;
        -g|--gzip)
            compress=true
            shift
            ;;
        -o|--output-dir)
            (($# >= 2)) || fail "missing value for $1"
            output_dir=$2
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            fail "unknown argument: $1 (use --help for usage)"
            ;;
    esac
done

if [[ -z ${DATABASE_URL:-} && -n $env_file ]]; then
    set -a
    source "$env_file"
    set +a
fi
[[ -n ${DATABASE_URL:-} ]] || fail "DATABASE_URL is not set in the environment, .flaskenv, or .env"

decode_url_component() {
    local value=$1 decoded= hex byte index

    for ((index = 0; index < ${#value}; index++)); do
        byte=${value:index:1}
        if [[ $byte == % ]]; then
            hex=${value:index+1:2}
            [[ $hex =~ ^[[:xdigit:]]{2}$ ]] || fail "DATABASE_URL contains an invalid percent escape"
            [[ $hex != 00 ]] || fail "DATABASE_URL contains a null byte escape"
            printf -v byte '%b' "\\x$hex"
            decoded+=$byte
            index=$((index + 2))
        else
            decoded+=$byte
        fi
    done
    decoded_component=$decoded
}

if [[ ! $DATABASE_URL =~ ^([A-Za-z][A-Za-z0-9+.-]*)://([^/]*)(/[^?#]*)?([?#].*)?$ ]]; then
    fail "invalid DATABASE_URL format"
fi

database_scheme=${BASH_REMATCH[1],,}
database_authority=${BASH_REMATCH[2]}
database_path=${BASH_REMATCH[3]#/}
database_scheme=${database_scheme%%+*}
[[ $database_scheme == mysql || $database_scheme == mariadb ]] || fail "DATABASE_URL must use the mysql or mariadb scheme"
[[ $database_authority == *@* ]] || fail "DATABASE_URL must include a username and host"

database_userinfo=${database_authority%@*}
database_hostport=${database_authority##*@}
if [[ $database_userinfo == *:* ]]; then
    database_username=${database_userinfo%%:*}
    database_password=${database_userinfo#*:}
else
    database_username=$database_userinfo
    database_password=
fi

database_port=
if [[ $database_hostport =~ ^\[([^]]+)\](:([0-9]+))?$ ]]; then
    database_host=${BASH_REMATCH[1]}
    database_port=${BASH_REMATCH[3]}
elif [[ $database_hostport == *:* ]]; then
    [[ $database_hostport != *:*:* ]] || fail "IPv6 hosts in DATABASE_URL must be enclosed in brackets"
    database_host=${database_hostport%:*}
    database_port=${database_hostport##*:}
    [[ $database_port =~ ^[0-9]+$ ]] || fail "DATABASE_URL port must be numeric"
else
    database_host=$database_hostport
fi

[[ -n $database_host && -n $database_username && -n $database_path ]] || fail "DATABASE_URL must include a host, username, and database name"
if [[ -n $database_port ]]; then
    ((10#$database_port > 0 && 10#$database_port <= 65535)) || fail "DATABASE_URL port must be between 1 and 65535"
fi

decode_url_component "$database_username"
database_username=$decoded_component
decode_url_component "$database_password"
database_password=$decoded_component
decode_url_component "$database_path"
database_name=$decoded_component

if command -v mariadb-dump >/dev/null 2>&1; then
    dump_command=$(command -v mariadb-dump)
elif command -v mysqldump >/dev/null 2>&1; then
    dump_command=$(command -v mysqldump)
else
    fail "neither mariadb-dump nor mysqldump is installed"
fi

mkdir -p -- "$output_dir" || fail "cannot create output directory: $output_dir"
[[ -d $output_dir && -w $output_dir ]] || fail "output directory is not writable: $output_dir"
if [[ $output_dir != / ]]; then
    output_dir=${output_dir%/}
fi

work_dir=$(mktemp -d "${TMPDIR:-/tmp}/conp-db-backup.XXXXXX") || fail "cannot create temporary directory"
temporary_output=
cleanup() {
    if [[ -n $temporary_output ]]; then
        rm -f -- "$temporary_output"
    fi
    rm -rf -- "$work_dir"
}
trap cleanup EXIT

escape_option_value() {
    local escaped=$1
    escaped=${escaped//\\/\\\\}
    escaped=${escaped//\"/\\\"}
    escaped=${escaped//$'\n'/\\n}
    escaped=${escaped//$'\r'/\\r}
    escaped=${escaped//$'\t'/\\t}
    printf '"%s"' "$escaped"
}

{
    printf '[client]\n'
    printf 'host=%s\n' "$(escape_option_value "$database_host")"
    if [[ -n $database_port ]]; then
        printf 'port=%s\n' "$database_port"
    fi
    printf 'user=%s\n' "$(escape_option_value "$database_username")"
    printf 'password=%s\n' "$(escape_option_value "$database_password")"
} > "$work_dir/client.cnf"
chmod 600 "$work_dir/client.cnf"

safe_component() {
    printf '%s' "$1" | LC_ALL=C sed 's/[^A-Za-z0-9._-]/_/g; s/^[._-]*//; s/[._-]*$//'
}

timestamp=$(date -u '+%Y%m%dT%H%M%SZ')
safe_prefix=$(safe_component "$prefix")
safe_host=$(safe_component "$database_host")
safe_database=$(safe_component "$database_name")
[[ -n $safe_host && -n $safe_database ]] || fail "database host and name must contain filename-safe characters"

filename_prefix=
if [[ -n $prefix ]]; then
    [[ -n $safe_prefix ]] || fail "prefix must contain a filename-safe character"
    filename_prefix="${safe_prefix}_"
fi

extension=.sql
if [[ $compress == true ]]; then
    extension=.sql.gz
fi
filename="${filename_prefix}${timestamp}_${safe_host}_${safe_database}${extension}"
output_path="${output_dir%/}/$filename"
[[ $output_dir != / ]] || output_path="/$filename"
[[ ! -e $output_path ]] || fail "backup already exists: $output_path"

if [[ $output_dir == / ]]; then
    temporary_output=$(mktemp "/.${filename}.XXXXXX") || fail "cannot create output file in $output_dir"
else
    temporary_output=$(mktemp "${output_dir}/.${filename}.XXXXXX") || fail "cannot create output file in $output_dir"
fi

dump_arguments=(
    "--defaults-extra-file=$work_dir/client.cnf"
    --single-transaction
    --routines
    --triggers
    --events
    --databases
    "$database_name"
)

if [[ $compress == true ]]; then
    "$dump_command" "${dump_arguments[@]}" | gzip -c > "$temporary_output"
else
    "$dump_command" "${dump_arguments[@]}" > "$temporary_output"
fi

if ! ln "$temporary_output" "$output_path"; then
    fail "could not create backup file (it may already exist): $output_path"
fi
rm -- "$temporary_output"
printf 'Database backup created: %s\n' "$output_path"