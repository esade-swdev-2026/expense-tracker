import datetime
from decimal import Decimal

import psycopg

from expense_tracker.report import Expense

DatabaseRow = tuple[datetime.date, str, str, Decimal]

SELECT_EXPENSES = "SELECT date, merchant, category, amount FROM expenses ORDER BY date, id"
INSERT_EXPENSE = "INSERT INTO expenses (date, merchant, category, amount) VALUES (%s, %s, %s, %s)"


def expense_from_row(row: DatabaseRow) -> Expense:
    date, merchant, category, amount = row
    return Expense(
        date=date.isoformat(),
        merchant=merchant,
        category=category,
        amount=float(amount),
    )


def row_from_expense(expense: Expense) -> DatabaseRow:
    return (
        datetime.date.fromisoformat(expense.date),
        expense.merchant,
        expense.category,
        Decimal(f"{expense.amount:.2f}"),
    )


def read_expenses_from_database(url: str) -> list[Expense]:
    with psycopg.connect(url) as connection:
        rows = connection.execute(SELECT_EXPENSES).fetchall()
    return [expense_from_row(row) for row in rows]


def add_expense_to_database(url: str, expense: Expense) -> None:
    with psycopg.connect(url) as connection:
        connection.execute(INSERT_EXPENSE, row_from_expense(expense))
