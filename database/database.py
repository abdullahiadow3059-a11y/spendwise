"""
Smart Student Expense Tracker - Professional Database Module
Group 9 | Optimized Version
"""

import sqlite3
import hashlib
from datetime import datetime
from contextlib import contextmanager

DB_NAME = "expense_tracker.db"

# ──────────────────────────────────────────────
# UTILITIES & CONNECTION
# ──────────────────────────────────────────────

@contextmanager
def get_db():
    """
    Safe connection manager. 
    Ensures the database closes even if the code crashes.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()

def hash_password(password):
    """Securely hashes passwords so they aren't stored in plain text."""
    return hashlib.sha256(password.encode()).hexdigest()

# ──────────────────────────────────────────────
# SCHEMA CREATION (OPTIMIZED)
# ──────────────────────────────────────────────

def create_tables():
    """Creates tables with performance indexes and strict constraints."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # We use executescript for the initial build for speed
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT
            );

            CREATE TABLE IF NOT EXISTS expenses (
                expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                description TEXT,
                date TEXT DEFAULT (date('now')),
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT
            );

            -- INDEXES: This makes the app stay fast as data grows
            CREATE INDEX IF NOT EXISTS idx_expenses_user ON expenses(user_id);
            CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date);

            CREATE TABLE IF NOT EXISTS budgets (
                budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                monthly_limit REAL NOT NULL CHECK(monthly_limit > 0),
                month TEXT NOT NULL,
                UNIQUE(user_id, category_id, month),
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS savings_goals (
                goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                goal_name TEXT NOT NULL,
                target_amount REAL NOT NULL CHECK(target_amount > 0),
                saved_amount REAL DEFAULT 0.0,
                deadline TEXT,
                status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'cancelled')),
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
        """)
        conn.commit()
    print("[DB] Tables and Indexes initialized.")

# ──────────────────────────────────────────────
# CORE OPERATIONS (SAMPLES)
# ──────────────────────────────────────────────

def register_user(full_name, username, password, email=None):
    """Registers a user with a hashed password."""
    hashed = hash_password(password)
    with get_db() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (full_name, username, password, email) VALUES (?, ?, ?, ?)",
                (full_name, username, hashed, email)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

def login_user(username, password):
    """Validates login against hashed passwords."""
    hashed = hash_password(password)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed))
        user = cursor.fetchone()
        return dict(user) if user else None

def add_expense(user_id, category_id, amount, description="", date=None):
    """Records an expense with automatic date handling."""
    date = date or datetime.today().strftime("%Y-%m-%d")
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (user_id, category_id, amount, description, date) VALUES (?, ?, ?, ?, ?)",
            (user_id, category_id, amount, description, date)
        )
        conn.commit()
        return cursor.lastrowid

# ──────────────────────────────────────────────
# INITIALIZATION
# ──────────────────────────────────────────────

def init_db():
    create_tables()
    # Note: seed_default_categories remains the same as your original
    print("[DB] Database Ready.")

if __name__ == "__main__":
    init_db()
