"""Lightweight SQLite helpers for storing contact / quote enquiries.

Uses the stdlib ``sqlite3`` module so there are no extra dependencies to
install on PythonAnywhere.
"""
import os
import sqlite3
from datetime import datetime

from flask import current_app, g


def get_db():
    """Return a request-scoped SQLite connection."""
    if "db" not in g:
        db_path = current_app.config["DATABASE"]
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        g.db = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """Create tables if they don't exist yet."""
    with app.app_context():
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS enquiries (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                name         TEXT    NOT NULL,
                email        TEXT,
                phone        TEXT    NOT NULL,
                city         TEXT,
                elevator_type TEXT,
                message      TEXT,
                created_at   TEXT    NOT NULL
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                name         TEXT    NOT NULL,
                email        TEXT,
                phone        TEXT    NOT NULL,
                position     TEXT,
                experience   TEXT,
                message      TEXT,
                created_at   TEXT    NOT NULL
            )
            """
        )
        db.commit()


def save_enquiry(name, email, phone, city, elevator_type, message):
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO enquiries (name, email, phone, city, elevator_type, message, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (name, email, phone, city, elevator_type, message,
         datetime.utcnow().isoformat(timespec="seconds")),
    )
    db.commit()
    return cur.lastrowid


def get_enquiries(limit=None):
    """Return all enquiries, newest first."""
    db = get_db()
    sql = "SELECT * FROM enquiries ORDER BY id DESC"
    if limit:
        sql += " LIMIT {:d}".format(int(limit))
    return db.execute(sql).fetchall()


def get_enquiry(enquiry_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM enquiries WHERE id = ?", (enquiry_id,)
    ).fetchone()


def count_enquiries():
    db = get_db()
    row = db.execute("SELECT COUNT(*) AS n FROM enquiries").fetchone()
    return row["n"] if row else 0


def save_application(name, email, phone, position, experience, message):
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO applications (name, email, phone, position, experience, message, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (name, email, phone, position, experience, message,
         datetime.utcnow().isoformat(timespec="seconds")),
    )
    db.commit()
    return cur.lastrowid


def get_applications(limit=None):
    """Return all job applications, newest first."""
    db = get_db()
    sql = "SELECT * FROM applications ORDER BY id DESC"
    if limit:
        sql += " LIMIT {:d}".format(int(limit))
    return db.execute(sql).fetchall()



def init_app(app):
    """Register db lifecycle hooks with the Flask app."""
    app.teardown_appcontext(close_db)
    init_db(app)
