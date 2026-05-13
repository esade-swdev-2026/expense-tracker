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


def test_csv_format_prints_a_header_and_one_row_per_category(tmp_path: Path) -> None:
    csv_file = tmp_path / "expenses.csv"
    csv_file.write_text(CSV_TEXT)

    result = runner.invoke(app, ["report", str(csv_file), "--format", "csv"])

    assert result.exit_code == 0
    assert result.stdout.splitlines() == [
        "category,total",
        "clothing,40.00",
        "transport,15.00",
        "dining,10.00",
    ]


def test_unknown_format_exits_with_two_and_explains_on_stderr() -> None:
    result = runner.invoke(app, ["report", "expenses.csv", "--format", "json"])

    assert result.exit_code == 2
    assert "format must be table or csv" in result.stderr
