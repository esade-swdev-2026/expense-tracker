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


def calculate_totals(x, y, z):
    d = {}
    for e in x:
        if y != "" and e[CATEGORY] != y:
            continue
        if e[AMOUNT] < z:
            continue
        if e[CATEGORY] not in d:
            d[e[CATEGORY]] = 0
        d[e[CATEGORY]] = d[e[CATEGORY]] + e[AMOUNT]
    r = []
    for k in d:
        r.append((k, d[k]))
    r.sort(key=lambda t: -t[1])
    return r


def run(path, cat, minimum):
    rows = []
    try:
        f = open(path)
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) == FIELDS_PER_ROW:
                rows.append((row[DATE], row[MERCHANT], row[CATEGORY], float(row[AMOUNT])))
        f.close()
    except:
        print("could not read " + path)
        sys.exit(1)

    print("Expense report for " + path)
    if cat != "":
        print("category: " + cat)
    if minimum > 0.0:
        print("only amounts of " + ("%.2f" % minimum) + " or more")
    print("-" * RULE_WIDTH)

    totals = calculate_totals(rows, cat, minimum)
    grand = 0
    for t in totals:
        print(t[0].ljust(NAME_WIDTH) + ("%.2f" % t[1]).rjust(AMOUNT_WIDTH))
        grand = grand + t[1]
    print("-" * RULE_WIDTH)
    print("TOTAL".ljust(NAME_WIDTH) + ("%.2f" % grand).rjust(AMOUNT_WIDTH))

    m = 0.0
    mr = None
    for e in rows:
        if e[AMOUNT] > m:
            m = e[AMOUNT]
            mr = e
    if mr is not None:
        print("")
        print("Largest single expense:")
        print(mr[MERCHANT] + " (" + mr[CATEGORY] + ") on " + mr[DATE] + " for " + ("%.2f" % mr[AMOUNT]))
