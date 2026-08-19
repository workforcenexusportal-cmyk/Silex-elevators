"""Security hardening for the Silex Elevator site.

Provides defence-in-depth on top of the app's existing CSRF, honeypot and
parameterised-SQL protections:

* Strict security response headers (nonce-based Content-Security-Policy,
  clickjacking, MIME-sniffing, referrer, permissions, HSTS).
* A lightweight in-memory rate limiter (brute-force / spam / DoS protection)
  with no external dependencies.

All of this runs with the Python standard library only, so it deploys cleanly
on PythonAnywhere with nothing extra to install.
"""
import secrets
import threading
import time
from collections import defaultdict, deque
from functools import wraps

from flask import g, request, jsonify, render_template, abort


# ---------------------------------------------------------------------------
# Rate limiting (sliding-window, per client IP + endpoint)
# ---------------------------------------------------------------------------
_LOCK = threading.Lock()
_HITS = defaultdict(deque)          # key -> deque[timestamps]
_LAST_SWEEP = [0.0]


def _client_ip():
    """Best-effort client IP, honouring a single trusted proxy hop."""
    fwd = request.headers.get("X-Forwarded-For", "")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.remote_addr or "unknown"


def _sweep(now):
    """Occasionally drop empty buckets so memory can't grow unbounded."""
    if now - _LAST_SWEEP[0] < 300:
        return
    _LAST_SWEEP[0] = now
    for key in list(_HITS.keys()):
        if not _HITS[key]:
            del _HITS[key]


def _allow(key, limit, window):
    """Return True if this hit is within ``limit`` requests per ``window`` s."""
    now = time.time()
    with _LOCK:
        bucket = _HITS[key]
        cutoff = now - window
        while bucket and bucket[0] < cutoff:
            bucket.popleft()
        if len(bucket) >= limit:
            return False
        bucket.append(now)
        _sweep(now)
        return True


def rate_limit(limit, window, methods=("POST",), scope=None):
    """Decorator: cap requests to a view by client IP.

    ``limit`` requests are allowed per ``window`` seconds. Only the given HTTP
    ``methods`` are counted (so a form page's GET is never throttled). When the
    limit is exceeded the client gets a 429 (JSON for API routes, else a page).
    """
    def decorator(view):
        bucket_name = scope or view.__name__

        @wraps(view)
        def wrapped(*args, **kwargs):
            if request.method in methods:
                key = "{}:{}".format(bucket_name, _client_ip())
                if not _allow(key, limit, window):
                    wants_json = (
                        request.path.startswith("/api/")
                        or request.accept_mimetypes.best == "application/json"
                    )
                    if wants_json:
                        resp = jsonify({
                            "reply": "You're sending messages too quickly. "
                                     "Please wait a moment and try again.",
                            "links": [], "chips": [],
                        })
                        resp.status_code = 429
                        resp.headers["Retry-After"] = str(window)
                        return resp
                    try:
                        body = render_template("429.html"), 429
                    except Exception:
                        body = ("Too many requests. Please slow down and "
                                "try again shortly.", 429)
                    resp = body
                    return resp
            return view(*args, **kwargs)
        return wrapped
    return decorator


# ---------------------------------------------------------------------------
# Security headers + per-request CSP nonce
# ---------------------------------------------------------------------------
def _build_csp(nonce):
    """A strict Content-Security-Policy allowing only what the site uses.

    Inline <script> blocks are permitted only when they carry this request's
    nonce, which neutralises reflected/stored XSS. Inline style attributes are
    used widely across the templates, so 'unsafe-inline' is kept for styles
    only (style injection is far lower risk than script execution).
    """
    return "; ".join([
        "default-src 'self'",
        # Scripts: same-origin + nonce'd inline + Google Analytics loader.
        "script-src 'self' 'nonce-{}' https://www.googletagmanager.com "
        "https://www.google-analytics.com".format(nonce),
        # Styles: same-origin + Google Fonts + inline style attributes.
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
        "font-src 'self' https://fonts.gstatic.com data:",
        # Images: same-origin, data URIs, Unsplash gallery, GA pixel.
        "img-src 'self' data: https://images.unsplash.com "
        "https://www.google-analytics.com https://*.googleusercontent.com",
        # Only the Google Maps embed is framed.
        "frame-src https://www.google.com https://maps.google.com",
        "connect-src 'self' https://www.google-analytics.com "
        "https://www.googletagmanager.com",
        "form-action 'self'",
        "base-uri 'self'",
        "object-src 'none'",
        "frame-ancestors 'none'",
        "upgrade-insecure-requests",
    ])


def init_security(app):
    """Attach the CSP nonce and security headers to every response."""

    @app.before_request
    def _assign_nonce():
        g.csp_nonce = secrets.token_urlsafe(16)

    @app.context_processor
    def _inject_nonce():
        return {"csp_nonce": getattr(g, "csp_nonce", "")}

    enable_hsts = bool(app.config.get("ENABLE_HSTS"))

    @app.after_request
    def _set_headers(resp):
        nonce = getattr(g, "csp_nonce", "")
        resp.headers.setdefault("Content-Security-Policy", _build_csp(nonce))
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["X-Frame-Options"] = "DENY"
        resp.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        resp.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=(), payment=(), "
            "usb=(), interest-cohort=()"
        )
        resp.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        resp.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        resp.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        # Don't leak the server/framework fingerprint.
        resp.headers["Server"] = "Silex"
        if enable_hsts:
            resp.headers["Strict-Transport-Security"] = (
                "max-age=63072000; includeSubDomains; preload"
            )
        return resp

    return app
