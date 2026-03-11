import sys
import csv

DATE = 0
MERCHANT = 1
CATEGORY = 2
AMOUNT = 3
FIELDS_PER_ROW = 4

NAME_WIDTH = 20
AMOUNT_WIDTH = 10
RULE_WIDTH = 40


def total_by_category(expenses, category, minimum):
    totals = {}
    for expense in expenses:
        if category != "" and expense[CATEGORY] != category:
            continue
        if expense[AMOUNT] < minimum:
            continue
        if expense[CATEGORY] not in totals:
            totals[expense[CATEGORY]] = 0
        totals[expense[CATEGORY]] = totals[expense[CATEGORY]] + expense[AMOUNT]
    ordered = []
    for name in totals:
        ordered.append((name, totals[name]))
    ordered.sort(key=lambda pair: -pair[1])
    return ordered


def run(path, category, minimum):
    expenses = []
    try:
        f = open(path)
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) == FIELDS_PER_ROW:
                expenses.append((row[DATE], row[MERCHANT], row[CATEGORY], float(row[AMOUNT])))
        f.close()
    except:
        print("could not read " + path)
        sys.exit(1)

    print("Expense report for " + path)
    if category != "":
        print("category: " + category)
    if minimum > 0.0:
        print("only amounts of " + ("%.2f" % minimum) + " or more")
    print("-" * RULE_WIDTH)

    totals = total_by_category(expenses, category, minimum)
    grand_total = 0
    for name, amount in totals:
        print(name.ljust(NAME_WIDTH) + ("%.2f" % amount).rjust(AMOUNT_WIDTH))
        grand_total = grand_total + amount
    print("-" * RULE_WIDTH)
    print("TOTAL".ljust(NAME_WIDTH) + ("%.2f" % grand_total).rjust(AMOUNT_WIDTH))

    largest_amount = 0.0
    largest = None
    for expense in expenses:
        if expense[AMOUNT] > largest_amount:
            largest_amount = expense[AMOUNT]
            largest = expense
    if largest is not None:
        print("")
        print("Largest single expense:")
        print(
            largest[MERCHANT]
            + " ("
            + largest[CATEGORY]
            + ") on "
            + largest[DATE]
            + " for "
            + ("%.2f" % largest[AMOUNT])
        )
