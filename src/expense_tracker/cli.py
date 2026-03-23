import csv
import datetime
from pathlib import Path

import typer

from expense_tracker.report import run

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
    DATA_FILE.parent.mkdir(exist_ok=True)
    is_new = not DATA_FILE.exists()
    with DATA_FILE.open("a", newline="") as handle:
        writer = csv.writer(handle)
        if is_new:
            writer.writerow(["date", "merchant", "category", "amount"])
        writer.writerow([date, merchant, category, f"{amount:.2f}"])
    print(f"added {merchant} ({category}) {amount:.2f} to {DATA_FILE}")
