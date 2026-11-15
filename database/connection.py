
import sqlite3
from pathlib import Path

# ==========================================
# ATMOSYNC DATABASE CONNECTION
# ==========================================

# Get project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database file location
DATABASE_PATH = BASE_DIR / "database" / "atmosync.db"

# SQL schema file
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"


def get_connection():
    """
    Establish connection with SQLite database.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    # Enable foreign key constraints
    connection.execute("PRAGMA foreign_keys = ON")

    # Return rows as dictionary-like objects
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """
    Create database tables using schema.sql.
    """

    try:
        connection = get_connection()

        with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
            schema = file.read()

        connection.executescript(schema)

        connection.commit()
        connection.close()

        print("AtmoSync database initialized successfully!")

    except sqlite3.Error as error:
        print("Database Error:", error)

    except FileNotFoundError as error:
        print("Schema file not found:", error)


def test_connection():
    """
    Test database connectivity.
    """

    try:
        connection = get_connection()

        connection.execute("SELECT 1")

        print("Database connection successful!")

        connection.close()

    except sqlite3.Error as error:
        print("Connection failed:", error)


if __name__ == "__main__":
    initialize_database()
    test_connection()
