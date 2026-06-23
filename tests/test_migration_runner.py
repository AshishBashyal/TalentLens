from pathlib import Path

from database.migration_runner import migration_files


def test_migration_files_are_sorted(tmp_path: Path) -> None:
    (tmp_path / "002_second.sql").write_text("SELECT 2;", encoding="utf-8")
    (tmp_path / "001_first.sql").write_text("SELECT 1;", encoding="utf-8")

    files = migration_files(tmp_path)

    assert [file.name for file in files] == ["001_first.sql", "002_second.sql"]

