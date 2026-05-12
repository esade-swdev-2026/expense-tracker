import csv
import datetime
from pathlib import Path

import typer

from expense_tracker.report import (
    filter_by_month,
    format_report,
    format_top,
    is_valid_month,
    largest_expense,
    largest_expenses,
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
    month: str = typer.Option("", help="Only this month, as YYYY-MM."),
    top: int = typer.Option(0, min=0, help="Also list the N largest expenses."),
) -> None:
    if month != "" and not is_valid_month(month):
        typer.echo(f"month must look like 2025-07, not {month}", err=True)
        raise typer.Exit(2)
    try:
        expenses = read_expenses(path)
    except (OSError, ValueError):
        typer.echo(f"could not read {path}", err=True)
        raise typer.Exit(1) from None

    if month != "":
        expenses = filter_by_month(expenses, month)
    totals = total_by_category(expenses, category, minimum)
    largest = largest_expense(expenses)
    lines = format_report(path, category, minimum, totals, largest, month)
    if top > 0:
        lines = lines + [""] + format_top(largest_expenses(expenses, top))
    for line in lines:
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
