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


def test_top_option_lists_the_largest_expenses_after_the_report(tmp_path: Path) -> None:
    csv_file = tmp_path / "expenses.csv"
    csv_file.write_text(CSV_TEXT)

    result = runner.invoke(app, ["report", str(csv_file), "--top", "2"])

    assert result.exit_code == 0
    top_section = result.stdout.split("Largest 2 expenses:")[1]
    assert top_section.index("Zara") < top_section.index("Cabify")
    assert "Bar Ramon" not in top_section


def test_negative_top_is_a_usage_error() -> None:
    result = runner.invoke(app, ["report", "expenses.csv", "--top", "-1"])

    assert result.exit_code == 2
