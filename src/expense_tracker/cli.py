import csv
import datetime
import os

import typer

from expense_tracker.report import run

app = typer.Typer(help="A terminal expense tracker.")


@app.callback()
def main() -> None:
    pass


@app.command()
def report(
    path: str = typer.Argument("expenses.csv", help="CSV file to read."),
    category: str = typer.Option("", help="Only this category."),
    minimum: float = typer.Option(0.0, "--minimum", "--min", help="Ignore amounts below this."),
) -> None:
    run(path, category, minimum)


@app.command()
def add(
    merchant: str,
    category: str,
    amount: float,
    date: str = typer.Option("", help="YYYY-MM-DD, defaults to today."),
) -> None:
    if date == "":
        date = datetime.date.today().isoformat()
    if not os.path.exists("data"):
        os.makedirs("data")
    exists = os.path.exists("data/expenses.csv")
    f = open("data/expenses.csv", "a", newline="")
    writer = csv.writer(f)
    if not exists:
        writer.writerow(["date", "merchant", "category", "amount"])
    writer.writerow([date, merchant, category, "%.2f" % amount])
    f.close()
    print("added " + merchant + " (" + category + ") " + ("%.2f" % amount) + " to data/expenses.csv")
