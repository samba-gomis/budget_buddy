# databases/__init__.py
# Exposes the main database functions as a package
from databases.database import get_connection, init_db, close_connection