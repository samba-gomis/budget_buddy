# Database schema definitions

#  Table users 
# Stores information about each registered user
CREATE_TABLE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name   TEXT    NOT NULL,
    first_name  TEXT    NOT NULL,
    email       TEXT    NOT NULL UNIQUE,
    password    TEXT    NOT NULL,       -- bcrypt hashed password
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);
"""

#  Table accounts 
# A user can have one or more accounts
CREATE_TABLE_ACCOUNTS = """
CREATE TABLE IF NOT EXISTS accounts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    balance     REAL    NOT NULL DEFAULT 0.0,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

#  Table categories 
# Possible categories for a transaction (leisure, food, etc.)
CREATE_TABLE_CATEGORIES = """
CREATE TABLE IF NOT EXISTS categories (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT    NOT NULL UNIQUE
);
"""

#  Table transactions 
# Records every financial operation (deposit, withdrawal, transfer)
CREATE_TABLE_TRANSACTIONS = """
CREATE TABLE IF NOT EXISTS transactions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id  INTEGER NOT NULL,
    reference   TEXT    NOT NULL UNIQUE,
    description TEXT,
    amount      REAL    NOT NULL,
    date        TEXT    NOT NULL,          -- ISO format: YYYY-MM-DD HH:MM:SS
    type        TEXT    NOT NULL CHECK(type IN ('deposit', 'withdrawal', 'transfer')),
    category_id INTEGER,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (account_id)  REFERENCES accounts(id)   ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);
"""

# Default categories inserted on first launch
DEFAULT_CATEGORIES = [
    "leisure",
    "food",
    "transport",
    "health",
    "housing",
    "salary",
    "savings",
    "other",
]