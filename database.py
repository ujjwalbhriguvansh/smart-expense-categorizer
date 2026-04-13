"""
database.py — SQLite setup, table creation, seeding, and CRUD helpers.
3 tables: categories, uploads, transactions
"""

import sqlite3
from datetime import datetime

DB_NAME = "finance.db"

DEFAULT_CATEGORIES = [
    "Salary / Income",
    "Food",
    "Travel",
    "Shopping",
    "Bills & Utilities",
    "Entertainment",
    "Healthcare",
    "Insurance",
    "Savings / Transfers",
    "Education",
    "Rent",
    "Other",
]


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def create_tables(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT    NOT NULL UNIQUE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS uploads (
            id          INTEGER   PRIMARY KEY AUTOINCREMENT,
            filename    TEXT      NOT NULL,
            uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            date        TEXT    NOT NULL,
            description TEXT    NOT NULL,
            amount      REAL    NOT NULL,
            type        TEXT    NOT NULL CHECK(type IN ('debit','credit')),
            category    TEXT    NOT NULL REFERENCES categories(name)
                        ON UPDATE CASCADE ON DELETE SET DEFAULT,
            upload_id   INTEGER NOT NULL REFERENCES uploads(id)
                        ON DELETE CASCADE
        )
    """)

    conn.commit()


def seed_categories(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.executemany(
        "INSERT OR IGNORE INTO categories (name) VALUES (?)",
        [(c,) for c in DEFAULT_CATEGORIES],
    )
    conn.commit()


def insert_upload(conn: sqlite3.Connection, filename: str) -> int:
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO uploads (filename, uploaded_at) VALUES (?, ?)",
        (filename, datetime.utcnow()),
    )
    conn.commit()
    return cur.lastrowid


def insert_transactions(conn, rows: list[dict], upload_id: int) -> int:
    cur = conn.cursor()
    cur.executemany(
        """INSERT INTO transactions (date, description, amount, type, category, upload_id)
           VALUES (:date, :description, :amount, :type, :category, :upload_id)""",
        [{**r, "upload_id": upload_id} for r in rows],
    )
    conn.commit()
    return cur.rowcount


def get_all_transactions(conn, category: str | None = None):
    cur = conn.cursor()
    if category:
        cur.execute(
            "SELECT * FROM transactions WHERE category=? ORDER BY date DESC", (category,)
        )
    else:
        cur.execute("SELECT * FROM transactions ORDER BY date DESC")
    return cur.fetchall()


def get_summary(conn) -> dict:
    cur = conn.cursor()
    cur.execute("SELECT COALESCE(SUM(amount),0) FROM transactions WHERE type='credit'")
    income = cur.fetchone()[0]
    cur.execute("SELECT COALESCE(SUM(ABS(amount)),0) FROM transactions WHERE type='debit'")
    expense = cur.fetchone()[0]
    cur.execute(
        """SELECT category, SUM(ABS(amount)) AS total FROM transactions
           WHERE type='debit' GROUP BY category ORDER BY total DESC"""
    )
    by_cat = {r["category"]: round(r["total"], 2) for r in cur.fetchall()}
    top = max(by_cat, key=by_cat.get) if by_cat else None
    return {
        "income": round(income, 2),
        "expense": round(expense, 2),
        "by_category": by_cat,
        "top_category": top,
    }


def get_all_categories(conn) -> list[str]:
    cur = conn.cursor()
    cur.execute("SELECT name FROM categories ORDER BY name")
    return [r["name"] for r in cur.fetchall()]


def get_transactions_for_download(conn):
    cur = conn.cursor()
    cur.execute(
        "SELECT date, description, amount, type, category FROM transactions ORDER BY date ASC"
    )
    return cur.fetchall()


if __name__ == "__main__":
    conn = get_connection()
    create_tables(conn)
    seed_categories(conn)
    conn.close()
    print("Database initialised ✅")
