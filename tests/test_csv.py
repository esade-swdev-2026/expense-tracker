from expense_tracker.report import format_csv


def test_format_csv_has_a_header_and_one_row_per_category() -> None:
    lines = format_csv([("dining", 50.0), ("transport", 15.5)])

    assert lines == ["category,total", "dining,50.00", "transport,15.50"]


def test_format_csv_with_no_totals_is_just_the_header() -> None:
    assert format_csv([]) == ["category,total"]
