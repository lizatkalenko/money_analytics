# def load(filename):
#     records = []
#     try:  
#         f = open(filename, "r", encoding="utf-8")
#     except FileNotFoundError:
#         return records 
#     with f:
#         for line in f:
#             line = line.strip()
#             if line == "":
#                 continue
#             parts = line.split(";")
#             try:
#                 record = {
#                     "name": parts[0],
#                     "category": parts[1],
#                     "amount": float(parts[2]),
#                     "due_date": parts[3],
#                     "status": parts[4],
#                 }
#             except (IndexError, ValueError):
#                 print("пропущено пошкоджений рядок:", line)
#                 continue
#             records.append(record)
#     return records

# def save(filename, records):
#     with open(filename, "w", encoding="utf-8") as f:
#         for r in records:
#             f.write(f"{r['name']};{r['category']};{r['amount']};{r['due_date']};{r['status']}\n")

import sqlite3

DB = "data.db"

def connect():
    """Підключається до бази даних."""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init():
    """Створює таблицю платежів, якщо її ще немає."""
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL CHECK (amount >= 0),
                due_date TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)

def load(category=None):
    """Повертає список словників, за бажанням лише однієї категорії."""
    with connect() as conn:
        if category is None:
            rows = conn.execute(
                "SELECT * FROM payments ORDER BY due_date"
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM payments WHERE category = ? ORDER BY due_date",
                (category,)
            ).fetchall()

    return [dict(row) for row in rows]

def add(payment):
    """Додає платіж і повертає його внутрішній ID."""
    with connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO payments (name, category, amount, due_date, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                payment["name"],
                payment["category"],
                payment["amount"],
                payment["due_date"],
                payment["status"],
            )
        )
        return cursor.lastrowid

def update_payment(payment_id, field, value):
    queries = {
        "name": "UPDATE payments SET name = ? WHERE id = ?",
        "category": "UPDATE payments SET category = ? WHERE id = ?",
        "amount": "UPDATE payments SET amount = ? WHERE id = ?",
        "due_date": "UPDATE payments SET due_date = ? WHERE id = ?",
        "status": "UPDATE payments SET status = ? WHERE id = ?"
    }

    if field not in queries:
        return False

    with connect() as conn:
        cursor = conn.execute(
            queries[field],
            (value, payment_id)
        )
        return cursor.rowcount > 0


def delete_payment(payment_id):
    """Видаляє платіж за ID. Повертає True, якщо платіж існував."""
    with connect() as conn:
        cursor = conn.execute(
            "DELETE FROM payments WHERE id = ?",
            (payment_id,)
        )
        return cursor.rowcount > 0

if __name__ == "__main__":
    init()