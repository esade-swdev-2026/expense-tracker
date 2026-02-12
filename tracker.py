import sys
import csv


def calculate_totals(x, y, z):
    d = {}
    for e in x:
        if y != "" and e[2] != y:
            continue
        if e[3] < z:
            continue
        if e[2] not in d:
            d[e[2]] = 0
        d[e[2]] = d[e[2]] + e[3]
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
            # skip rows that do not have all four fields
            if len(row) == 4:
                rows.append((row[0], row[1], row[2], float(row[3])))
        f.close()
    except:
        print("could not read " + path)
        sys.exit(1)

    print("Expense report for " + path)
    if cat != "":
        print("category: " + cat)
    if minimum > 0.0:
        print("only amounts of " + ("%.2f" % minimum) + " or more")
    print("-" * 40)

    totals = calculate_totals(rows, cat, minimum)
    grand = 0
    for t in totals:
        print(t[0].ljust(20) + ("%.2f" % t[1]).rjust(10))
        grand = grand + t[1]
    print("-" * 40)
    print("TOTAL".ljust(20) + ("%.2f" % grand).rjust(10))


if __name__ == "__main__":
    path = "expenses.csv"
    if len(sys.argv) > 1:
        path = sys.argv[1]
    cat = ""
    if len(sys.argv) > 2:
        cat = sys.argv[2]
    minimum = 0.0
    if len(sys.argv) > 3:
        minimum = float(sys.argv[3])
    run(path, cat, minimum)
