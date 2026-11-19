from pathlib import Path

import pytest
from typer.testing import CliRunner

from expense_tracker.cli import app

runner = CliRunner()

BAD_DATE = "17/11/2026"
UNREACHABLE_DATABASE = "postgresql://nobody@localhost:1/nothing"


def test_bad_date_with_database_exits_with_two_and_explains_on_stderr(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATABASE_URL", UNREACHABLE_DATABASE)

    result = runner.invoke(app, ["add", "Bar Nuria", "dining", "12.40", "--date", BAD_DATE])

    assert result.exit_code == 2
    assert f"date must look like 2026-11-17, not {BAD_DATE}" in result.stderr


def test_bad_date_without_database_writes_nothing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["add", "Bar Nuria", "dining", "12.40", "--date", BAD_DATE])

    assert result.exit_code == 2
    assert not (tmp_path / "data" / "expenses.csv").exists()
