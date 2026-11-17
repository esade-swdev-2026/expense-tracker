CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    merchant TEXT NOT NULL,
    category TEXT NOT NULL,
    amount NUMERIC(10, 2) NOT NULL
);

COPY expenses (date, merchant, category, amount)
FROM '/seed/expenses.csv' WITH (FORMAT csv, HEADER true);
