import datetime
from decimal import Decimal

from expense_tracker.database import expense_from_row, row_from_expense
from expense_tracker.report import Expense


def test_a_row_becomes_an_expense_with_a_text_date_and_a_float_amount() -> None:
    row = (datetime.date(2026, 11, 17), "Bar Nuria", "dining", Decimal("12.40"))

    assert expense_from_row(row) == Expense("2026-11-17", "Bar Nuria", "dining", 12.40)


def test_an_expense_becomes_a_row_with_the_amount_in_cents() -> None:
    expense = Expense("2026-11-17", "Renfe", "transport", 21.0)

    assert row_from_expense(expense) == (
        datetime.date(2026, 11, 17),
        "Renfe",
        "transport",
        Decimal("21.00"),
    )


def test_a_float_amount_is_stored_as_exact_cents() -> None:
    expense = Expense("2026-11-17", "Mercadona", "groceries", 0.1 + 0.2)

    assert row_from_expense(expense)[3] == Decimal("0.30")


def test_an_expense_survives_the_round_trip() -> None:
    expense = Expense("2026-02-28", "Cinesa", "leisure", 9.9)

    assert expense_from_row(row_from_expense(expense)) == expense
