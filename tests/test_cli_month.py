from pathlib import Path

from typer.testing import CliRunner

from expense_tracker.cli import app

runner = CliRunner()

CSV_TEXT = (
    "date,merchant,category,amount\n"
    "2025-07-01,Bar Ramon,dining,10.00\n"
    "2025-07-02,Zara,clothing,40.00\n"
    "2025-08-01,Cabify,transport,15.00\n"
)


def test_month_option_reports_only_that_month(tmp_path: Path) -> None:
    csv_file = tmp_path / "expenses.csv"
    csv_file.write_text(CSV_TEXT)

    result = runner.invoke(app, ["report", str(csv_file), "--month", "2025-07"])

    assert result.exit_code == 0
    assert "month: 2025-07" in result.stdout
    assert "50.00" in result.stdout
    assert "transport" not in result.stdout


def test_invalid_month_exits_with_two_and_explains_on_stderr() -> None:
    result = runner.invoke(app, ["report", "expenses.csv", "--month", "2025-13"])

    assert result.exit_code == 2
    assert "month must look like 2025-07" in result.stderr
