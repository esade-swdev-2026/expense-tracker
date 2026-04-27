import pytest

from expense_tracker.report import Expense, filter_by_month, is_valid_month

JULY_FIRST = Expense("2025-07-01", "Bar Ramon", "dining", 10.0)
JULY_LAST = Expense("2025-07-31", "Zara", "clothing", 40.0)
AUGUST_FIRST = Expense("2025-08-01", "Cabify", "transport", 15.0)
OTHER_JULY = Expense("2024-07-15", "Lidl", "groceries", 20.0)


@pytest.mark.parametrize(
    ("month", "expected"),
    [
        ("2025-07", [JULY_FIRST, JULY_LAST]),
        ("2025-08", [AUGUST_FIRST]),
        ("2025-09", []),
        ("2024-07", [OTHER_JULY]),
    ],
)
def test_filter_keeps_only_that_month_of_that_year(month: str, expected: list[Expense]) -> None:
    expenses = [JULY_FIRST, JULY_LAST, AUGUST_FIRST, OTHER_JULY]

    assert filter_by_month(expenses, month) == expected


def test_filter_on_no_expenses_returns_no_expenses() -> None:
    assert filter_by_month([], "2025-07") == []


@pytest.mark.parametrize("month", ["2025-01", "2025-09", "2025-12", "1999-10"])
def test_valid_months(month: str) -> None:
    assert is_valid_month(month)


@pytest.mark.parametrize(
    "month",
    ["", "2025", "2025-7", "2025-13", "2025-00", "25-07", "2025/07", "2025-07-01", "july"],
)
def test_invalid_months(month: str) -> None:
    assert not is_valid_month(month)
