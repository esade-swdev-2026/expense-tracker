import pytest

from expense_tracker.report import Expense, filter_by_date_range

JULY_FIRST = Expense("2025-07-01", "Bar Ramon", "dining", 10.0)
JULY_LAST = Expense("2025-07-31", "Zara", "clothing", 40.0)
AUGUST_FIRST = Expense("2025-08-01", "Cabify", "transport", 15.0)
EXPENSES = [JULY_FIRST, JULY_LAST, AUGUST_FIRST]


@pytest.mark.parametrize(
    ("date_from", "date_to", "expected"),
    [
        ("2025-07-01", "2025-07-31", [JULY_FIRST, JULY_LAST]),
        ("2025-07-02", "2025-08-01", [JULY_LAST, AUGUST_FIRST]),
        ("2025-07-31", "", [JULY_LAST, AUGUST_FIRST]),
        ("", "2025-07-01", [JULY_FIRST]),
        ("", "", EXPENSES),
        ("2025-09-01", "2025-09-30", []),
        ("2025-07-31", "2025-07-31", [JULY_LAST]),
    ],
)
def test_range_bounds_are_inclusive_and_optional(
    date_from: str, date_to: str, expected: list[Expense]
) -> None:
    assert filter_by_date_range(EXPENSES, date_from, date_to) == expected
