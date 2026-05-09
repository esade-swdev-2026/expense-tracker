import csv
import re
from dataclasses import dataclass

DATE = 0
MERCHANT = 1
CATEGORY = 2
AMOUNT = 3
FIELDS_PER_ROW = 4

NAME_WIDTH = 20
AMOUNT_WIDTH = 10
RULE_WIDTH = 40

MONTH_PATTERN = re.compile(r"\d{4}-(0[1-9]|1[0-2])")


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
                        amount=round(float(row[AMOUNT])),
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
    month: str = "",
) -> list[str]:
    lines = [f"Expense report for {path}"]
    if category != "":
        lines.append(f"category: {category}")
    if month != "":
        lines.append(f"month: {month}")
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


def format_csv(totals: list[tuple[str, float]]) -> list[str]:
    lines = ["category,total"]
    for name, amount in totals:
        lines.append(f"{name},{amount:.2f}")
    return lines


def remove_duplicates(expenses: list[Expense]) -> list[Expense]:
    return list(dict.fromkeys(expenses))


def is_valid_month(month: str) -> bool:
    return MONTH_PATTERN.fullmatch(month) is not None


def filter_by_month(expenses: list[Expense], month: str) -> list[Expense]:
    return [expense for expense in expenses if expense.date.startswith(month + "-")]
