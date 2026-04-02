import pytest

from expense_tracker.report import (
    Expense,
    format_report,
    largest_expense,
    total_by_category,
)


@pytest.fixture
def expenses() -> list[Expense]:
    return [
        Expense("2025-07-01", "Bar Ramon", "dining", 10.0),
        Expense("2025-07-02", "Zara", "clothing", 40.0),
        Expense("2025-07-03", "Bar Ramon", "dining", 5.0),
        Expense("2025-07-04", "Cabify", "transport", 15.0),
    ]


def test_totals_are_grouped_by_category_and_largest_first(expenses: list[Expense]) -> None:
    result = total_by_category(expenses, category="", minimum=0.0)

    assert result == [("clothing", 40.0), ("dining", 15.0), ("transport", 15.0)]


def test_equal_totals_keep_the_order_they_first_appeared_in(expenses: list[Expense]) -> None:
    result = total_by_category(expenses, category="", minimum=0.0)

    assert [name for name, _ in result][1:] == ["dining", "transport"]


@pytest.mark.parametrize(
    ("category", "expected"),
    [
        ("dining", [("dining", 15.0)]),
        ("transport", [("transport", 15.0)]),
        ("nobody-used-this", []),
    ],
)
def test_category_filter(
    expenses: list[Expense], category: str, expected: list[tuple[str, float]]
) -> None:
    assert total_by_category(expenses, category=category, minimum=0.0) == expected


@pytest.mark.parametrize(
    ("minimum", "expected"),
    [
        (0.0, [("dining", 15.0)]),
        (5.0, [("dining", 15.0)]),
        (10.0, [("dining", 10.0)]),
        (10.01, []),
    ],
)
def test_minimum_keeps_amounts_equal_to_it(
    minimum: float, expected: list[tuple[str, float]]
) -> None:
    dining = [
        Expense("2025-07-01", "Bar Ramon", "dining", 10.0),
        Expense("2025-07-03", "Bar Ramon", "dining", 5.0),
    ]

    assert total_by_category(dining, category="", minimum=minimum) == expected


def test_no_expenses_means_no_totals() -> None:
    assert total_by_category([], category="", minimum=0.0) == []


def test_a_refund_reduces_its_category_total() -> None:
    expenses = [
        Expense("2025-07-01", "Zara", "clothing", 40.0),
        Expense("2025-07-09", "Zara", "clothing", -15.0),
    ]

    assert total_by_category(expenses, category="", minimum=-100.0) == [("clothing", 25.0)]


def test_largest_expense_of_nothing_is_none() -> None:
    assert largest_expense([]) is None


def test_largest_expense_is_the_biggest_amount(expenses: list[Expense]) -> None:
    assert largest_expense(expenses) == Expense("2025-07-02", "Zara", "clothing", 40.0)


def test_largest_expense_tie_goes_to_the_first(expenses: list[Expense]) -> None:
    tied = [*expenses, Expense("2025-07-05", "Mango", "clothing", 40.0)]

    assert largest_expense(tied) == Expense("2025-07-02", "Zara", "clothing", 40.0)


def test_report_of_nothing_still_has_a_zero_total() -> None:
    lines = format_report("empty.csv", "", 0.0, [], None)

    assert lines[-1].split() == ["TOTAL", "0.00"]
    assert "Largest single expense:" not in lines


def test_report_header_mentions_the_filters_in_use() -> None:
    lines = format_report("expenses.csv", "dining", 20.0, [], None)

    assert "category: dining" in lines
    assert "only amounts of 20.00 or more" in lines


def test_report_total_is_the_sum_of_the_categories(expenses: list[Expense]) -> None:
    totals = total_by_category(expenses, category="", minimum=0.0)

    lines = format_report("expenses.csv", "", 0.0, totals, largest_expense(expenses))

    assert [line for line in lines if line.startswith("TOTAL")][0].split()[-1] == "70.00"
