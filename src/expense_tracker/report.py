import csv
import sys
from dataclasses import dataclass

DATE = 0
MERCHANT = 1
CATEGORY = 2
AMOUNT = 3
FIELDS_PER_ROW = 4

NAME_WIDTH = 20
AMOUNT_WIDTH = 10
RULE_WIDTH = 40


@dataclass(frozen=True)
class Expense:
    date: str
    merchant: str
    category: str
    amount: float


def read_expenses(path: str) -> list[Expense]:
    expenses: list[Expense] = []
    with open(path) as handle:
        reader = csv.reader(handle)
        next(reader)
        for row in reader:
            if len(row) == FIELDS_PER_ROW:
                expenses.append(
                    Expense(
                        date=row[DATE],
                        merchant=row[MERCHANT],
                        category=row[CATEGORY],
                        amount=float(row[AMOUNT]),
                    )
                )
    return expenses


def total_by_category(
    expenses: list[Expense], category: str, minimum: float
) -> list[tuple[str, float]]:
    totals: dict[str, float] = {}
    for expense in expenses:
        if category != "" and expense.category != category:
            continue
        if expense.amount < minimum:
            continue
        totals[expense.category] = totals.get(expense.category, 0.0) + expense.amount
    ordered = list(totals.items())
    ordered.sort(key=lambda pair: -pair[1])
    return ordered


def largest_expense(expenses: list[Expense]) -> Expense | None:
    largest = None
    for expense in expenses:
        if largest is None or expense.amount > largest.amount:
            largest = expense
    return largest


def format_report(
    path: str,
    category: str,
    minimum: float,
    totals: list[tuple[str, float]],
    largest: Expense | None,
) -> list[str]:
    lines = [f"Expense report for {path}"]
    if category != "":
        lines.append(f"category: {category}")
    if minimum > 0.0:
        lines.append(f"only amounts of {minimum:.2f} or more")
    lines.append("-" * RULE_WIDTH)

    grand_total = 0.0
    for name, amount in totals:
        lines.append(name.ljust(NAME_WIDTH) + f"{amount:.2f}".rjust(AMOUNT_WIDTH))
        grand_total = grand_total + amount
    lines.append("-" * RULE_WIDTH)
    lines.append("TOTAL".ljust(NAME_WIDTH) + f"{grand_total:.2f}".rjust(AMOUNT_WIDTH))

    if largest is not None:
        lines.append("")
        lines.append("Largest single expense:")
        lines.append(
            f"{largest.merchant} ({largest.category}) on {largest.date} for {largest.amount:.2f}"
        )
    return lines


def run(path: str, category: str, minimum: float) -> None:
    try:
        expenses = read_expenses(path)
    except (OSError, ValueError):
        print(f"could not read {path}")
        sys.exit(1)

    totals = total_by_category(expenses, category, minimum)
    largest = largest_expense(expenses)
    for line in format_report(path, category, minimum, totals, largest):
        print(line)
