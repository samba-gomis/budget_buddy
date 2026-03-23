# Database connection and initialization
import sqlite3
import os
from .models import (
    CREATE_TABLE_USERS,
    CREATE_TABLE_ACCOUNTS,
    CREATE_TABLE_CATEGORIES,
    CREATE_TABLE_TRANSACTIONS,
    DEFAULT_CATEGORIES,
)

# Path to the SQLite file (created automatically if it does not exist)
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "finance.db")


def get_connection() -> sqlite3.Connection:
    """
    Opens and returns a connection to the database
    Enables foreign keys (disabled by default in SQLite)
    Uses Row as factory to access columns by name
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """
    Creates all tables if they do not exist yet, then inserts the default categories
    Called once at application startup
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Create tables in the correct order (foreign key compliance)
    cursor.executescript(
        CREATE_TABLE_USERS +
        CREATE_TABLE_ACCOUNTS +
        CREATE_TABLE_CATEGORIES +
        CREATE_TABLE_TRANSACTIONS
    )

    # Insert default categories (ignored if already present)
    for category in DEFAULT_CATEGORIES:
        cursor.execute(
            "INSERT OR IGNORE INTO categories (name) VALUES (?)",
            (category,)
        )

    conn.commit()
    conn.close()
    print("[DB] Database initialized successfully.")


def close_connection(conn: sqlite3.Connection) -> None:
    """
    Cleanly closes an open connection
    Should be called after each operation in the repositories
    """
    if conn:
        conn.close()