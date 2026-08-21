"""Lightweight SQLite helpers for storing contact / quote enquiries.

Uses the stdlib ``sqlite3`` module so there are no extra dependencies to
install on PythonAnywhere.
"""
import os
import sqlite3
from datetime import datetime, timedelta

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
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS visits (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                day          TEXT    NOT NULL,
                path         TEXT,
                visitor      TEXT,
                created_at   TEXT    NOT NULL
            )
            """
        )
        db.execute(
            "CREATE INDEX IF NOT EXISTS idx_visits_day ON visits(day)"
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


# -- Visitor analytics ------------------------------------------------------
def record_visit(path, visitor):
    """Log a single page view. ``visitor`` is a salted hash, never a raw IP."""
    db = get_db()
    now = datetime.utcnow()
    db.execute(
        "INSERT INTO visits (day, path, visitor, created_at) VALUES (?, ?, ?, ?)",
        (now.strftime("%Y-%m-%d"), path, visitor,
         now.isoformat(timespec="seconds")),
    )
    db.commit()


def get_visits_daily(days=30):
    """Return ``{day: {'views': n, 'uniques': n}}`` for the last ``days`` days."""
    db = get_db()
    since = (datetime.utcnow().date() - timedelta(days=days - 1)).isoformat()
    rows = db.execute(
        """
        SELECT day,
               COUNT(*)               AS views,
               COUNT(DISTINCT visitor) AS uniques
        FROM visits
        WHERE day >= ?
        GROUP BY day
        """,
        (since,),
    ).fetchall()
    return {r["day"]: {"views": r["views"], "uniques": r["uniques"]}
            for r in rows}


def visit_totals():
    """Return all-time totals plus today's count for the dashboard cards."""
    db = get_db()
    total = db.execute("SELECT COUNT(*) AS n FROM visits").fetchone()["n"]
    uniques = db.execute(
        "SELECT COUNT(DISTINCT visitor) AS n FROM visits"
    ).fetchone()["n"]
    today = datetime.utcnow().strftime("%Y-%m-%d")
    today_n = db.execute(
        "SELECT COUNT(*) AS n FROM visits WHERE day = ?", (today,)
    ).fetchone()["n"]
    return {"total": total, "uniques": uniques, "today": today_n}


def init_app(app):
    """Register db lifecycle hooks with the Flask app."""
    app.teardown_appcontext(close_db)
    init_db(app)
