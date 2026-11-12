# expense-tracker

A terminal expense tracker: it reads a CSV of expenses and reports what you spent, by
category. It is the demo project for **Software Development for Business** (ESADE), built
commit by commit across the course — so its history matters as much as its code.

## Install

Needs [uv](https://docs.astral.sh/uv/) and Python 3.13.

```bash
git clone git@github.com:esade-swdev-2026/expense-tracker.git
cd expense-tracker
uv sync
```

## Use

Add an expense, then report on what you have added:

```bash
uv run expenses add "Bar Nuria" dining 12.40
uv run expenses add Renfe transport 21.00 --date 2026-03-01
uv run expenses report
```

Or report on the sample data, everything or one category:

```bash
uv run expenses report expenses.csv
uv run expenses report expenses.csv --category dining --min 20
uv run expenses report expenses.csv --month 2025-09
uv run expenses report expenses.csv --top 5
uv run expenses report expenses.csv --format csv
```

`expenses --help` lists the commands; `expenses report --help` its options.

## The two CSV files

- `data/expenses.csv` is **your data**: `add` writes to it and `report` reads it by default.
  It is not in version control.
- `expenses.csv` at the root is **sample data and is never modified**. It is what the
  terminal sessions of the course work on. Report on it by passing the path:
  `uv run expenses report expenses.csv`.

## Before you push

Run the same checks CI runs, in the same order:

```bash
scripts/check.sh
```

It runs ruff, the formatting check, mypy and pytest, and stops at the first one that fails.
A push should never be the first time your code meets these checks.

## Licence

MIT. See [LICENSE](LICENSE).
