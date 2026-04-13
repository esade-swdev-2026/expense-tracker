from expense_tracker.report import Expense, remove_duplicates

BAR = Expense("2025-07-01", "Bar Ramon", "dining", 10.0)
ZARA = Expense("2025-07-02", "Zara", "clothing", 40.0)


def test_no_expenses_means_no_duplicates() -> None:
    assert remove_duplicates([]) == []


def test_expenses_without_duplicates_are_unchanged() -> None:
    assert remove_duplicates([BAR, ZARA]) == [BAR, ZARA]


def test_an_exact_duplicate_is_removed_and_the_first_one_kept() -> None:
    assert remove_duplicates([BAR, ZARA, BAR]) == [BAR, ZARA]


def test_same_merchant_on_another_day_is_not_a_duplicate() -> None:
    next_day = Expense("2025-07-02", "Bar Ramon", "dining", 10.0)

    assert remove_duplicates([BAR, next_day]) == [BAR, next_day]


def test_many_copies_of_one_expense_collapse_to_one() -> None:
    assert remove_duplicates([BAR, BAR, BAR]) == [BAR]
