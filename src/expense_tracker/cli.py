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
