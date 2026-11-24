from pathlib import Path

import pytest
from typer.testing import CliRunner

from expense_tracker.cli import app

runner = CliRunner()

CSV_TEXT = (
    "date,merchant,category,amount\n"
    "2025-07-01,Bar Ramon,dining,10.00\n"
    "2025-07-15,Zara,clothing,40.00\n"
    "2025-07-31,Lidl,groceries,25.00\n"
    "2025-08-01,Cabify,transport,15.00\n"
)


@pytest.fixture
def csv_file(tmp_path: Path) -> Path:
    path = tmp_path / "expenses.csv"
    path.write_text(CSV_TEXT)
    return path


def test_both_bounds_are_inclusive(csv_file: Path) -> None:
    result = runner.invoke(
        app, ["report", str(csv_file), "--from", "2025-07-15", "--to", "2025-07-31"]
    )

    assert result.exit_code == 0
    assert "from: 2025-07-15" in result.stdout
    assert "to: 2025-07-31" in result.stdout
    assert "65.00" in result.stdout
    assert "dining" not in result.stdout
    assert "transport" not in result.stdout


def test_from_alone_has_no_upper_bound(csv_file: Path) -> None:
    result = runner.invoke(app, ["report", str(csv_file), "--from", "2025-07-31"])

    assert result.exit_code == 0
    assert "from: 2025-07-31" in result.stdout
    assert "to:" not in result.stdout
    assert "40.00" in result.stdout
    assert "groceries" in result.stdout
    assert "transport" in result.stdout


def test_to_alone_has_no_lower_bound(csv_file: Path) -> None:
    result = runner.invoke(app, ["report", str(csv_file), "--to", "2025-07-01"])

    assert result.exit_code == 0
    assert "to: 2025-07-01" in result.stdout
    assert "from:" not in result.stdout
    assert "10.00" in result.stdout
    assert "clothing" not in result.stdout


def test_no_date_options_print_no_date_headers(csv_file: Path) -> None:
    result = runner.invoke(app, ["report", str(csv_file)])

    assert "from:" not in result.stdout
    assert "to:" not in result.stdout


def test_range_intersects_with_month(csv_file: Path) -> None:
    result = runner.invoke(
        app,
        [
            "report",
            str(csv_file),
            "--month",
            "2025-07",
            "--from",
            "2025-07-15",
            "--to",
            "2025-08-01",
        ],
    )

    assert result.exit_code == 0
    assert "65.00" in result.stdout
    assert "transport" not in result.stdout


def test_range_intersects_with_category_and_minimum(csv_file: Path) -> None:
    result = runner.invoke(
        app,
        ["report", str(csv_file), "--from", "2025-07-01", "--category", "clothing", "--min", "30"],
    )

    assert result.exit_code == 0
    assert "40.00" in result.stdout
    assert "dining" not in result.stdout


def test_empty_range_is_not_an_error(csv_file: Path) -> None:
    result = runner.invoke(app, ["report", str(csv_file), "--from", "2030-01-01"])

    assert result.exit_code == 0
    assert "0.00" in result.stdout
    assert "Largest single expense" not in result.stdout


def test_range_applies_to_largest_expense_and_top(csv_file: Path) -> None:
    result = runner.invoke(app, ["report", str(csv_file), "--from", "2025-07-31", "--top", "1"])

    assert "Lidl (groceries) on 2025-07-31 for 25.00" in result.stdout
    assert "Zara" not in result.stdout


def test_csv_output_is_filtered_and_has_no_headers(csv_file: Path) -> None:
    result = runner.invoke(
        app, ["report", str(csv_file), "--from", "2025-08-01", "--format", "csv"]
    )

    assert result.stdout.splitlines() == ["category,total", "transport,15.00"]


@pytest.mark.parametrize("option", ["--from", "--to"])
@pytest.mark.parametrize("bad_date", ["20261117", "07/01/2025", "2025-02-30", "2025-7-1", "x"])
def test_invalid_date_exits_with_two_and_explains_on_stderr(option: str, bad_date: str) -> None:
    result = runner.invoke(app, ["report", "expenses.csv", option, bad_date])

    assert result.exit_code == 2
    assert f"{option[2:]} must look like 2026-11-17, not {bad_date}" in result.stderr


def test_inverted_range_exits_with_two_and_explains_on_stderr() -> None:
    result = runner.invoke(
        app, ["report", "expenses.csv", "--from", "2025-08-01", "--to", "2025-07-01"]
    )

    assert result.exit_code == 2
    assert "from must not be after to" in result.stderr
