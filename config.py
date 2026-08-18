"""Application configuration.

Values can be overridden with environment variables so the same code runs
locally and on PythonAnywhere without edits.
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Change SECRET_KEY in production (set the SILEX_SECRET_KEY env var on PythonAnywhere).
    SECRET_KEY = os.environ.get("SILEX_SECRET_KEY", "dev-secret-change-me")

    # SQLite database lives in the Flask instance folder (auto-created, git-ignored).
    DATABASE = os.environ.get(
        "SILEX_DATABASE",
        os.path.join(BASE_DIR, "instance", "silex.sqlite3"),
    )

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

    # Admin dashboard credentials (override in production!).
    ADMIN_USER = os.environ.get("SILEX_ADMIN_USER", "admin")
    ADMIN_PASSWORD = os.environ.get("SILEX_ADMIN_PASSWORD", "silex-admin")

    # Google Analytics 4 measurement ID, e.g. "G-XXXXXXXXXX" (optional).
    GA_MEASUREMENT_ID = os.environ.get("SILEX_GA_ID", "")

    # Google Maps embed query (the office location).
    MAPS_QUERY = os.environ.get(
        "SILEX_MAPS_QUERY",
        "Elifenta Business Hub, Katargam, Surat, Gujarat 395004",
    )
