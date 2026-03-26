import csv
import datetime
from pathlib import Path

import typer

from expense_tracker.report import (
    format_report,
    largest_expense,
    read_expenses,
    total_by_category,
)

DATA_FILE = Path("data") / "expenses.csv"

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
    try:
        expenses = read_expenses(path)
    except (OSError, ValueError):
        typer.echo(f"could not read {path}", err=True)
        raise typer.Exit(1) from None

    totals = total_by_category(expenses, category, minimum)
    largest = largest_expense(expenses)
    for line in format_report(path, category, minimum, totals, largest):
        typer.echo(line)


@app.command()
def add(
    merchant: str,
    category: str,
    amount: float,
    date: str = typer.Option("", help="YYYY-MM-DD, defaults to today."),
) -> None:
    if date == "":
        date = datetime.date.today().isoformat()
    DATA_FILE.parent.mkdir(exist_ok=True)
    is_new = not DATA_FILE.exists()
    with DATA_FILE.open("a", newline="") as handle:
        writer = csv.writer(handle)
        if is_new:
            writer.writerow(["date", "merchant", "category", "amount"])
        writer.writerow([date, merchant, category, f"{amount:.2f}"])
    print(f"added {merchant} ({category}) {amount:.2f} to {DATA_FILE}")
