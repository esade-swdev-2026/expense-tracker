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

Report on the sample data, everything or one category:

```bash
uv run expenses report
uv run expenses report --category dining --min 20
```

Add an expense:

```bash
uv run expenses add "Bar Nuria" dining 12.40
uv run expenses add Renfe transport 21.00 --date 2026-03-01
```

`expenses --help` lists the commands; `expenses report --help` its options.

## The two CSV files

- `expenses.csv` at the root is **sample data and is never modified**. It is what `report`
  reads by default, and what the terminal sessions of the course work on.
- `add` writes to `data/expenses.csv`, which is not in version control. Report on it by
  passing the path: `uv run expenses report data/expenses.csv`.

## Licence

MIT. See [LICENSE](LICENSE).
