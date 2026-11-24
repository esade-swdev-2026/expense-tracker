import csv
import datetime
import os
import re
from pathlib import Path

import psycopg
import typer

from expense_tracker.database import add_expense_to_database, read_expenses_from_database
from expense_tracker.report import (
    Expense,
    filter_by_date_range,
    filter_by_month,
    format_csv,
    format_report,
    format_top,
    is_valid_month,
    largest_expense,
    largest_expenses,
    read_expenses,
    total_by_category,
)

DATA_FILE = Path("data") / "expenses.csv"
DATABASE_URL = "DATABASE_URL"
DATABASE_LABEL = "the database"
OUTPUT_FORMATS = ("table", "csv")
DASHED_DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")

app = typer.Typer(help="A terminal expense tracker.")


@app.callback()
def main() -> None:
    pass


@app.command()
def report(
    path: str = typer.Argument(str(DATA_FILE), help="CSV file to read."),
    category: str = typer.Option("", help="Only this category."),
    minimum: float = typer.Option(0.0, "--minimum", "--min", help="Ignore amounts below this."),
    month: str = typer.Option("", help="Only this month, as YYYY-MM."),
    top: int = typer.Option(0, min=0, help="Also list the N largest expenses."),
    output_format: str = typer.Option("table", "--format", help="table or csv."),
    date_from: str = typer.Option("", "--from", help="Only on or after this date, YYYY-MM-DD."),
    date_to: str = typer.Option("", "--to", help="Only on or before this date, YYYY-MM-DD."),
) -> None:
    if month != "" and not is_valid_month(month):
        typer.echo(f"month must look like 2025-07, not {month}", err=True)
        raise typer.Exit(2)
    for name, bound in (("from", date_from), ("to", date_to)):
        if bound != "" and not is_strict_date(bound):
            typer.echo(f"{name} must look like 2026-11-17, not {bound}", err=True)
            raise typer.Exit(2)
    if date_from != "" and date_to != "" and date_from > date_to:
        typer.echo("from must not be after to", err=True)
        raise typer.Exit(2)
    if output_format not in OUTPUT_FORMATS:
        typer.echo(f"format must be table or csv, not {output_format}", err=True)
        raise typer.Exit(2)
    url = os.environ.get(DATABASE_URL, "")
    source = DATABASE_LABEL if url else path
    try:
        expenses = read_expenses_from_database(url) if url else read_expenses(path)
    except (OSError, ValueError, psycopg.Error):
        typer.echo(f"could not read {source}", err=True)
        raise typer.Exit(1) from None

    if month != "":
        expenses = filter_by_month(expenses, month)
    expenses = filter_by_date_range(expenses, date_from, date_to)
    totals = total_by_category(expenses, category, minimum)
    if output_format == "csv":
        lines = format_csv(totals)
    else:
        lines = format_report(
            source, category, minimum, totals, largest_expense(expenses), month, date_from, date_to
        )
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
    if not is_valid_date(date):
        typer.echo(f"date must look like 2026-11-17, not {date}", err=True)
        raise typer.Exit(2)
    expense = Expense(date=date, merchant=merchant, category=category, amount=amount)
    url = os.environ.get(DATABASE_URL, "")
    if url:
        try:
            add_expense_to_database(url, expense)
        except psycopg.Error:
            typer.echo(f"could not write to {DATABASE_LABEL}", err=True)
            raise typer.Exit(1) from None
        destination = DATABASE_LABEL
    else:
        append_expense_to_file(expense)
        destination = str(DATA_FILE)
    print(f"added {merchant} ({category}) {amount:.2f} to {destination}")


def is_strict_date(text: str) -> bool:
    return DASHED_DATE_PATTERN.fullmatch(text) is not None and is_valid_date(text)


def is_valid_date(text: str) -> bool:
    try:
        datetime.date.fromisoformat(text)
    except ValueError:
        return False
    return True


def append_expense_to_file(expense: Expense) -> None:
    DATA_FILE.parent.mkdir(exist_ok=True)
    is_new = not DATA_FILE.exists()
    with DATA_FILE.open("a", newline="") as handle:
        writer = csv.writer(handle)
        if is_new:
            writer.writerow(["date", "merchant", "category", "amount"])
        writer.writerow([expense.date, expense.merchant, expense.category, f"{expense.amount:.2f}"])
