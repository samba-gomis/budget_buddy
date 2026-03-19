# repositories/transaction_repo.py
# All database operations related to transactions (CRUD + filters)

from databases.database import get_connection, close_connection


def add(account_id: int, reference: str, description: str,
        amount: float, date: str, type_: str, category_id: int | None = None) -> int:
    """
    Inserts a new transaction into the database
    Returns the ID of the newly created transaction
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO transactions
                (account_id, reference, description, amount, date, type, category_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (account_id, reference, description, amount, date, type_, category_id)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        close_connection(conn)


def get_all(account_id: int) -> list[dict]:
    """
    Returns all transactions for a given account, ordered by date descending
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT t.*, c.name AS category_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.account_id = ?
            ORDER BY t.date DESC
            """,
            (account_id,)
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        close_connection(conn)


def filter_by_date(account_id: int, date: str) -> list[dict]:
    """
    Returns all transactions on a specific date (YYYY-MM-DD)
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT t.*, c.name AS category_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.account_id = ? AND DATE(t.date) = ?
            ORDER BY t.date DESC
            """,
            (account_id, date)
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        close_connection(conn)


def filter_by_range(account_id: int, start_date: str, end_date: str) -> list[dict]:
    """
    Returns all transactions between two dates (inclusive).
    Dates must be in YYYY-MM-DD format.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT t.*, c.name AS category_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.account_id = ? AND DATE(t.date) BETWEEN ? AND ?
            ORDER BY t.date DESC
            """,
            (account_id, start_date, end_date)
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        close_connection(conn)


def filter_by_type(account_id: int, type_: str) -> list[dict]:
    """
    Returns all transactions of a given type: 'deposit', 'withdrawal', or 'transfer'.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT t.*, c.name AS category_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.account_id = ? AND t.type = ?
            ORDER BY t.date DESC
            """,
            (account_id, type_)
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        close_connection(conn)


def filter_by_category(account_id: int, category_name: str) -> list[dict]:
    """
    Returns all transactions matching a given category name (e.g. 'food', 'leisure').
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT t.*, c.name AS category_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.account_id = ? AND c.name = ?
            ORDER BY t.date DESC
            """,
            (account_id, category_name)
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        close_connection(conn)


def sort_by_amount(account_id: int, order: str = "asc") -> list[dict]:
    """
    Returns all transactions sorted by amount.
    order: 'asc' for ascending, 'desc' for descending.
    """
    direction = "ASC" if order.lower() == "asc" else "DESC"
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT t.*, c.name AS category_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.account_id = ?
            ORDER BY t.amount {direction}
            """,
            (account_id,)
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        close_connection(conn)


def get_by_month(account_id: int, year: int, month: int) -> list[dict]:
    """
    Returns all transactions for a specific month and year.
    Used by the dashboard to compute the monthly summary.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT t.*, c.name AS category_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.account_id = ?
              AND strftime('%Y', t.date) = ?
              AND strftime('%m', t.date) = ?
            ORDER BY t.date DESC
            """,
            (account_id, str(year), str(month).zfill(2))
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        close_connection(conn)