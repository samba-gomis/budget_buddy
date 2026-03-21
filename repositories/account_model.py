# repositories/account_model.py
# All database operations related to accounts and balances

from databases.database import get_connection, close_connection


def create_account(user_id: int, balance: float = 0.0) -> int:
    """
    Creates a new account for a user.
    Returns the ID of the newly created account.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO accounts (user_id, balance) VALUES (?, ?)",
            (user_id, balance)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        close_connection(conn)


def get_accounts_by_user(user_id: int) -> list[dict]:
    """
    Returns all accounts belonging to a user.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE user_id = ?", (user_id,))
        return [dict(row) for row in cursor.fetchall()]
    finally:
        close_connection(conn)


def get_account_by_id(account_id: int) -> dict | None:
    """
    Returns a single account by its ID.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        close_connection(conn)


def get_balance(account_id: int) -> float:
    """
    Returns the current balance of an account.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
        row = cursor.fetchone()
        return row["balance"] if row else 0.0
    finally:
        close_connection(conn)


def update_balance(account_id: int, new_balance: float) -> None:
    """
    Updates the balance of an account.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE accounts SET balance = ? WHERE id = ?",
            (new_balance, account_id)
        )
        conn.commit()
    finally:
        close_connection(conn)