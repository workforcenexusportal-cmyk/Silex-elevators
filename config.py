"""Application configuration.

Values can be overridden with environment variables so the same code runs
locally and on PythonAnywhere without edits.
"""
import os
import secrets
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # SECRET_KEY signs the session cookie. In production set SILEX_SECRET_KEY
    # to a long random value. If it isn't set we generate a strong random key
    # per process (sessions won't survive a restart, but the key is never a
    # publicly known default that an attacker could use to forge cookies).
    SECRET_KEY = os.environ.get("SILEX_SECRET_KEY") or secrets.token_hex(32)

    # SQLite database lives in the Flask instance folder (auto-created, git-ignored).
    DATABASE = os.environ.get(
        "SILEX_DATABASE",
        os.path.join(BASE_DIR, "instance", "silex.sqlite3"),
    )

    # -- Session / cookie hardening ------------------------------------------
    SESSION_COOKIE_HTTPONLY = True          # JS can't read the session cookie
    SESSION_COOKIE_SAMESITE = "Lax"         # blocks cross-site cookie sending
    # Send cookies only over HTTPS in production. Set SILEX_HTTPS=1 there.
    SESSION_COOKIE_SECURE = os.environ.get("SILEX_HTTPS", "").lower() in (
        "1", "true", "yes", "on",
    )
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    # Reject oversized request bodies (basic DoS protection). 8 MB comfortably
    # covers gallery photo uploads while still blocking abusive payloads.
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    # Emit HSTS only when actually served over HTTPS.
    ENABLE_HSTS = SESSION_COOKIE_SECURE


    # Business contact details (from the official Silex brochure).
    COMPANY_NAME = "Silex Elevator PVT. LTD"
    COMPANY_TAGLINE = "Elevating spaces with precision and trust"
    PHONE = "+91 85110 33826"
    PHONE_ALT = "+91 93166 64670"
    CONTACT_PERSON = "Yash Vasani"
    CONTACT_PERSON_ALT = "Raj Vasani"
    WHATSAPP = "918511033826"
    EMAIL = "elevatorsilex@gmail.com"
    ADDRESS = "4th Floor, Elifenta Business Hub, Signapor, Katargam, Surat 395004, Gujarat, India"
    CERTIFICATION = "ISO 9001:2008 Certified"
    # 24x7 emergency / breakdown helpline (defaults to the main line).
    EMERGENCY_PHONE = os.environ.get("SILEX_EMERGENCY_PHONE", "+91 85110 33826")

    # Public site URL (used for canonical links, sitemap and Open Graph tags).
    SITE_URL = os.environ.get("SILEX_SITE_URL", "http://127.0.0.1:5000")

    # Downloadable brochure (served from /static).
    BROCHURE_FILE = os.environ.get("SILEX_BROCHURE", "Silex-Elevator-Brochure.pdf")

    # Admin dashboard credentials. Override with env vars in production.
    ADMIN_USER = os.environ.get("SILEX_ADMIN_USER", "rajvasani")
    ADMIN_PASSWORD = os.environ.get("SILEX_ADMIN_PASSWORD", "Sx#9vK2r$Lm7!qZt")

    # Google Analytics 4 measurement ID, e.g. "G-XXXXXXXXXX" (optional).
    GA_MEASUREMENT_ID = os.environ.get("SILEX_GA_ID", "")

    # Google Maps embed query (the office location).
    MAPS_QUERY = os.environ.get(
        "SILEX_MAPS_QUERY",
        "Elifenta Business Hub, Katargam, Surat, Gujarat 395004",
    )
