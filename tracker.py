import sqlite3

DB_NAME = "expenses.db"

def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_table():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL
            )
        """)

def add_expense(date, category, amount):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)",
            (date, category, amount),
        )

def get_all_expenses():
    
    with get_conn() as conn:
        return conn.execute(
            "SELECT id, date, category, amount FROM expenses ORDER BY date DESC, id DESC"
        ).fetchall()

def update_expense(expense_id, new_date, new_category, new_amount):

    with get_conn() as conn:
        conn.execute(
            """
            UPDATE expenses
            SET date = ?, category = ?, amount = ?
            WHERE id = ?
            """,
            (new_date, new_category, new_amount, expense_id),
        )

def delete_expense(expense_id):

    with get_conn() as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

def get_monthly_summary(month):
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT category, SUM(amount)
            FROM expenses
            WHERE substr(date, 1, 7) = ?
            GROUP BY category
            """,
            (month,),
        ).fetchall()
    total = sum(r[1] for r in rows)
    return total, rows


def get_daily_totals(month):

    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT date, SUM(amount) as total
            FROM expenses
            WHERE substr(date, 1, 7) = ?
            GROUP BY date
            ORDER BY date ASC
            """,
            (month,),
        ).fetchall()
    return rows

