import gzip
import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BACKUP_SCRIPT = REPOSITORY_ROOT / "bin" / "crons" / "db_backup.bash"


def _mock_dump_command(tmp_path):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    command = bin_dir / "mariadb-dump"
    command.write_text(
        """#!/usr/bin/env bash
set -eu
printf '%s\\n' "$@" > "$DUMP_ARGS_FILE"
config=${1#--defaults-extra-file=}
test -r "$config"
cp "$config" "$DUMP_CONFIG_FILE"
printf '%s\\n' '-- MariaDB dump' 'CREATE DATABASE portal;' 'USE portal;' > /dev/stdout
""",
        encoding="utf-8",
    )
    command.chmod(0o755)
    return bin_dir


def _run_backup(
    tmp_path,
    *arguments,
    database_url="mysql+pymysql://backup:p%40ss@db.example.org:3307/portal",
    script=BACKUP_SCRIPT,
    block_python=False,
):
    bin_dir = _mock_dump_command(tmp_path)
    output_dir = tmp_path / "backups"
    temp_dir = tmp_path / "temp"
    temp_dir.mkdir()
    args_file = tmp_path / "dump-args.txt"
    config_file = tmp_path / "dump-config.cnf"
    environment = os.environ.copy()
    environment.update(
        {
            "PATH": f"{bin_dir}{os.pathsep}{environment['PATH']}",
            "TMPDIR": str(temp_dir),
            "DUMP_ARGS_FILE": str(args_file),
            "DUMP_CONFIG_FILE": str(config_file),
        }
    )
    if block_python:
        python = bin_dir / "python3"
        python.write_text("#!/usr/bin/env bash\nexit 99\n", encoding="utf-8")
        python.chmod(0o755)
    if database_url is not None:
        environment["DATABASE_URL"] = database_url
    else:
        environment.pop("DATABASE_URL", None)
    result = subprocess.run(
        [str(script), *arguments, "--output-dir", str(output_dir)],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )
    return result, output_dir, args_file, config_file, temp_dir


@pytest.mark.parametrize("env_filename", [".flaskenv", ".env"])
def test_reads_database_url_from_project_env_file_when_not_in_environment(tmp_path, env_filename):
    project_root = tmp_path / "project"
    script = project_root / "bin" / "crons" / "db_backup.bash"
    script.parent.mkdir(parents=True)
    shutil.copy2(BACKUP_SCRIPT, script)
    (project_root / env_filename).write_text(
        "DATABASE_URL='mysql://backup:secret@flaskenv-db.example.org/portal_from_envfile'\n",
        encoding="utf-8",
    )

    result, output_dir, _, _, _ = _run_backup(
        tmp_path, database_url=None, script=script
    )

    assert result.returncode == 0, result.stderr
    backups = list(output_dir.glob("*_flaskenv-db.example.org_portal_from_envfile.sql"))
    assert len(backups) == 1


def test_environment_database_url_takes_precedence_over_project_env_file(tmp_path):
    project_root = tmp_path / "project"
    script = project_root / "bin" / "crons" / "db_backup.bash"
    script.parent.mkdir(parents=True)
    shutil.copy2(BACKUP_SCRIPT, script)
    (project_root / ".flaskenv").write_text(
        "DATABASE_URL='mysql://backup:secret@file-db.example.org/file_database'\n",
        encoding="utf-8",
    )

    result, output_dir, _, _, _ = _run_backup(
        tmp_path,
        database_url="mysql://backup:secret@environment-db.example.org/environment_database",
        script=script,
    )

    assert result.returncode == 0, result.stderr
    backups = list(output_dir.glob("*_environment-db.example.org_environment_database.sql"))
    assert len(backups) == 1


def test_creates_timestamped_native_sql_dump(tmp_path):
    result, output_dir, args_file, config_file, temp_dir = _run_backup(
        tmp_path, block_python=True
    )

    assert result.returncode == 0, result.stderr
    backups = list(output_dir.glob("*_db.example.org_portal.sql"))
    assert len(backups) == 1
    assert backups[0].name[:16].endswith("Z")
    assert backups[0].read_text(encoding="utf-8").startswith("-- MariaDB dump")
    arguments = args_file.read_text(encoding="utf-8").splitlines()
    assert arguments[1:] == [
        "--single-transaction",
        "--routines",
        "--triggers",
        "--events",
        "--databases",
        "portal",
    ]
    client_options = config_file.read_text(encoding="utf-8")
    assert 'password="p@ss"' in client_options
    assert 'user="backup"' in client_options
    assert "port=3307" in config_file.read_text(encoding="utf-8")
    assert not list(temp_dir.iterdir())


def test_decodes_url_escaped_credentials_once(tmp_path):
    result, _, _, config_file, _ = _run_backup(
        tmp_path,
        database_url="mysql://backup:p%252F%40ss@db.example.org/portal",
    )

    assert result.returncode == 0, result.stderr
    assert 'password="p%2F@ss"' in config_file.read_text(encoding="utf-8")


def test_prefix_and_gzip_create_prefixed_compressed_dump(tmp_path):
    result, output_dir, _, _, _ = _run_backup(tmp_path, "--prefix", "nightly run", "--gzip")

    assert result.returncode == 0, result.stderr
    backups = list(output_dir.glob("nightly_run_*_db.example.org_portal.sql.gz"))
    assert len(backups) == 1
    assert gzip.decompress(backups[0].read_bytes()).startswith(b"-- MariaDB dump")


@pytest.mark.parametrize(
    "database_url",
    [
        "sqlite:///portal.db",
        "mysql://backup@db.example.org/",
        "mysql://backup@/portal",
        "mysql://backup:p%ZZ@db.example.org/portal",
    ],
)
def test_rejects_invalid_or_incomplete_database_url(tmp_path, database_url):
    result, output_dir, _, _, _ = _run_backup(tmp_path, database_url=database_url)

    assert result.returncode != 0
    assert "DATABASE_URL" in result.stderr
    assert not list(output_dir.glob("*"))


def test_dump_failure_does_not_leave_partial_backup(tmp_path):
    bin_dir = _mock_dump_command(tmp_path)
    command = bin_dir / "mariadb-dump"
    command.write_text("#!/usr/bin/env bash\nprintf partial\nexit 7\n", encoding="utf-8")
    command.chmod(0o755)
    output_dir = tmp_path / "backups"
    environment = os.environ.copy()
    environment.update(
        {
            "DATABASE_URL": "mysql://backup:secret@db.example.org/portal",
            "PATH": f"{bin_dir}{os.pathsep}{environment['PATH']}",
        }
    )

    result = subprocess.run(
        [str(BACKUP_SCRIPT), "--output-dir", str(output_dir)],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )

    assert result.returncode != 0
    assert not list(output_dir.glob("*"))
