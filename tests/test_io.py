from pathlib import Path

from typer.testing import CliRunner

from expense_tracker.cli import app
from expense_tracker.report import read_expenses

runner = CliRunner()


def test_rows_that_are_not_four_fields_are_skipped(tmp_path: Path) -> None:
    csv_file = tmp_path / "expenses.csv"
    csv_file.write_text(
        "date,merchant,category,amount\n"
        "2025-07-01,Bar Ramon,dining,10.00\n"
        "broken\n"
        "2025-07-02,Zara,clothing,40.00\n"
    )

    merchants = [expense.merchant for expense in read_expenses(str(csv_file))]

    assert merchants == ["Bar Ramon", "Zara"]


def test_report_on_a_missing_file_exits_with_one_and_explains_on_stderr() -> None:
    result = runner.invoke(app, ["report", "nosuch.csv"])

    assert result.exit_code == 1
    assert "could not read nosuch.csv" in result.stderr
