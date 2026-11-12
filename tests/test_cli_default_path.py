from pathlib import Path

import pytest
from typer.testing import CliRunner

from expense_tracker.cli import app

runner = CliRunner()


def test_report_reads_what_add_wrote(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)

    runner.invoke(app, ["add", "Bar Nuria", "dining", "12.40", "--date", "2026-11-13"])
    result = runner.invoke(app, ["report"])

    assert result.exit_code == 0
    assert "dining" in result.stdout
    assert "12.40" in result.stdout


def test_report_with_no_data_yet_explains_which_file_it_tried(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["report"])

    assert result.exit_code == 1
    assert "could not read data/expenses.csv" in result.stderr
