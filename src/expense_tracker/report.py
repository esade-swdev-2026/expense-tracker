import sys
import csv
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


def read_expenses(path):
    expenses = []
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


def total_by_category(expenses, category, minimum):
    totals = {}
    for expense in expenses:
        if category != "" and expense.category != category:
            continue
        if expense.amount < minimum:
            continue
        if expense.category not in totals:
            totals[expense.category] = 0
        totals[expense.category] = totals[expense.category] + expense.amount
    ordered = []
    for name in totals:
        ordered.append((name, totals[name]))
    ordered.sort(key=lambda pair: -pair[1])
    return ordered


def largest_expense(expenses):
    largest = None
    for expense in expenses:
        if largest is None or expense.amount > largest.amount:
            largest = expense
    return largest


def format_report(path, category, minimum, totals, largest):
    lines = ["Expense report for " + path]
    if category != "":
        lines.append("category: " + category)
    if minimum > 0.0:
        lines.append("only amounts of " + ("%.2f" % minimum) + " or more")
    lines.append("-" * RULE_WIDTH)

    grand_total = 0
    for name, amount in totals:
        lines.append(name.ljust(NAME_WIDTH) + ("%.2f" % amount).rjust(AMOUNT_WIDTH))
        grand_total = grand_total + amount
    lines.append("-" * RULE_WIDTH)
    lines.append("TOTAL".ljust(NAME_WIDTH) + ("%.2f" % grand_total).rjust(AMOUNT_WIDTH))

    if largest is not None:
        lines.append("")
        lines.append("Largest single expense:")
        lines.append(
            largest.merchant
            + " ("
            + largest.category
            + ") on "
            + largest.date
            + " for "
            + ("%.2f" % largest.amount)
        )
    return lines


def run(path, category, minimum):
    try:
        expenses = read_expenses(path)
    except:
        print("could not read " + path)
        sys.exit(1)

    totals = total_by_category(expenses, category, minimum)
    largest = largest_expense(expenses)
    for line in format_report(path, category, minimum, totals, largest):
        print(line)
