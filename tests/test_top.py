from expense_tracker.report import Expense, format_top, largest_expenses

SMALL = Expense("2025-07-01", "Bar Ramon", "dining", 10.0)
MEDIUM = Expense("2025-07-02", "Cabify", "transport", 15.0)
LARGE = Expense("2025-07-03", "Zara", "clothing", 40.0)


def test_largest_expenses_come_biggest_first() -> None:
    assert largest_expenses([SMALL, LARGE, MEDIUM], 2) == [LARGE, MEDIUM]


def test_asking_for_more_than_there_are_returns_them_all() -> None:
    assert largest_expenses([SMALL, LARGE], 5) == [LARGE, SMALL]


def test_asking_for_none_returns_none() -> None:
    assert largest_expenses([SMALL, LARGE], 0) == []


def test_format_top_puts_one_expense_per_line_under_a_heading() -> None:
    lines = format_top([LARGE, MEDIUM])

    assert lines[0] == "Largest 2 expenses:"
    assert lines[1].startswith("2025-07-03  Zara")
    assert lines[1].endswith("40.00")
    assert len(lines) == 3
