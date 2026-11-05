# Database backup cron script

`bin/crons/db_backup.bash` creates a native SQL dump of the MariaDB/MySQL
database identified by the portal's `DATABASE_URL`. It uses `mariadb-dump`
when available and falls back to `mysqldump`.

## Requirements

- Bash
- `mariadb-dump` or `mysqldump`
- `gzip` when compression is requested
- A `DATABASE_URL` using the `mysql` or `mariadb` scheme, with a host,
  username, and database name. It can be exported in the environment or set
  in the project-root `.flaskenv` or `.env` file.

For example:

```sh
export DATABASE_URL='mysql+pymysql://portal_user:password@db.example.org:3306/portal'
```

An environment-provided `DATABASE_URL` takes precedence. If it is unset, the
script sources `.flaskenv` from the project root (two directories above the
script), falling back to `.env` if `.flaskenv` is absent. The selected file is
executed as trusted Bash code with automatic exporting enabled, so use valid
shell assignments and quote values containing spaces or shell metacharacters.
Keep the file private and do not source an untrusted file. The backup script
and URL parsing use Bash; Python is not required. URL-encoded credentials and
database names are supported. The script writes the connection credentials to
a temporary option file with restricted permissions; the password is not
passed on the dump command line. The file is removed on exit.

## Usage

```sh
bin/crons/db_backup.bash [--prefix PREFIX] [--gzip] [--output-dir DIRECTORY]
```

Backups are written to the current directory by default. Set `DB_BACKUP_DIR`
to choose another default destination, or use `--output-dir` to override it.
The directory is created if it does not exist.

Examples:

```sh
# Plain SQL dump in the current directory
bin/crons/db_backup.bash

# Prefix the timestamp and compress the dump
bin/crons/db_backup.bash --prefix nightly --gzip --output-dir /var/backups/conp
```

The resulting filename is
`[PREFIX_]YYYYmmddTHHMMSSZ_HOST_DATABASE.sql[.gz]`. The timestamp is UTC;
characters in the prefix, host, or database name that are unsafe in a filename
are replaced with underscores. A same-name backup is not overwritten.

The dump includes the selected database's schema and data, routines, triggers,
and events. `--single-transaction` provides a consistent snapshot for
transactional tables; tables using non-transactional storage engines may not
be consistent while writes are occurring.

## Testing

From the repository root, run:

```sh
ADMIN_EMAIL=backup-tests@example.org uv run pytest tests/unit_tests/test_db_backup_script.py
```

Tests use a mocked `mariadb-dump` executable and do not require a running
database or MariaDB client installation.
