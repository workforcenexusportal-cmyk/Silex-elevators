"""Silex Elevator — Flask application.

A lightweight company website with a working enquiry form backed by SQLite,
an admin dashboard, email notifications, SEO endpoints and a brochure
download. Designed to deploy cleanly on PythonAnywhere.
"""
import csv
import io
import os
import re
import secrets
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for, flash, abort,
    session, send_from_directory, Response, make_response,
)
from werkzeug.utils import secure_filename

import content
import chatbot
import db
import security
from config import Config


# Image types accepted by the gallery manager, with magic-byte verification so
# a renamed non-image file can't be uploaded.
GALLERY_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}

# Gallery categories — each maps to a sub-folder under static/img/gallery.
GALLERY_CATEGORIES = [
    ("cabin", "Cabin"),
    ("control-operating-panel", "Control Operating Panel"),
    ("landing-operating-panel", "Landing Operating Panel"),
]
GALLERY_CAT_SLUGS = {slug for slug, _ in GALLERY_CATEGORIES}
GALLERY_CAT_LABELS = dict(GALLERY_CATEGORIES)


def _is_allowed_image(filename, head):
    """Return True only if the extension is allowed AND the file's magic bytes
    match that image type (defends against disguised/malicious uploads)."""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in GALLERY_EXTS:
        return False
    if head[:3] == b"\xff\xd8\xff":                       # JPEG
        return ext in {".jpg", ".jpeg"}
    if head[:8] == b"\x89PNG\r\n\x1a\n":                  # PNG
        return ext == ".png"
    if head[:6] in (b"GIF87a", b"GIF89a"):                # GIF
        return ext == ".gif"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":     # WEBP
        return ext == ".webp"
    if head[4:8] == b"ftyp":                              # AVIF/HEIF container
        return ext == ".avif"
    return False



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    security.init_security(app)

    # -- CSRF (lightweight, session based) -----------------------------------
    def get_csrf_token():
        token = session.get("_csrf")
        if not token:
            token = secrets.token_urlsafe(32)
            session["_csrf"] = token
        return token

    def csrf_ok():
        sent = request.form.get("_csrf", "")
        return bool(sent) and secrets.compare_digest(sent, session.get("_csrf", ""))

    # Make common values available to every template.
    @app.context_processor
    def inject_globals():
        return {
            "cfg": app.config,
            "nav_products": content.PRODUCTS,
            "current_year": datetime.now().year,
            "csrf_token": get_csrf_token,
            "canonical_url": request.base_url,
            "social_links": content.SOCIAL_LINKS,
            "media": content.MEDIA,
            "gallery_bg": content.GALLERY_BG,
            "scenes": content.SHOWROOM_SCENES,
        }

    # -- Pages ---------------------------------------------------------------
    @app.route("/")
    def home():
        return render_template(
            "index.html",
            stats=content.STATS,
            products=content.PRODUCTS,
            services=content.SERVICES[:3],
            why_us=content.WHY_US,
            projects=content.PROJECTS[:6],
            testimonials=content.TESTIMONIALS,
            partners=content.PARTNERS,
            posts=content.BLOG_POSTS[:3],
            showroom=content.SHOWROOM,
        )

    @app.route("/about")
    def about():
        return render_template(
            "about.html",
            stats=content.STATS,
            why_us=content.WHY_US,
            india_branches=content.INDIA_BRANCHES,
            global_network=content.GLOBAL_NETWORK,
            partners=content.PARTNERS,
        )

    @app.route("/products")
    def products():
        return render_template("products.html", products=content.PRODUCTS)

    @app.route("/machines")
    def machines():
        return render_template("machines.html")

    @app.route("/products/<slug>")
    def product_detail(slug):
        product = next((p for p in content.PRODUCTS if p["slug"] == slug), None)
        if product is None:
            abort(404)
        related = [p for p in content.PRODUCTS if p["slug"] != slug][:3]
        return render_template(
            "product_detail.html",
            product=product,
            specs=content.SPECS.get(slug),
            cabin_finishes=content.CABIN_FINISHES,
            fixtures=content.FIXTURES,
            related=related,
        )

    @app.route("/services")
    def services():
        return render_template(
            "services.html",
            services=content.SERVICES,
            cabin_finishes=content.CABIN_FINISHES,
            auto_doors=content.AUTO_DOOR_DESIGNS,
            manual_doors=content.MANUAL_DOOR_DESIGNS,
            fixtures=content.FIXTURES,
            machines=content.MACHINES,
        )

    @app.route("/projects")
    def projects():
        return render_template("projects.html", projects=content.PROJECTS)

    # -- Gallery (auto-lists any images dropped into static/img/gallery) ------
    def _gallery_photos():
        exts = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}
        base_folder = os.path.join(app.static_folder, "img", "gallery")
        # Scan the root folder (legacy/uncategorised) plus each category sub-folder.
        scan = [("", base_folder)] + [
            (slug, os.path.join(base_folder, slug)) for slug, _ in GALLERY_CATEGORIES
        ]
        photos = []
        for cat_slug, folder in scan:
            try:
                names = sorted(os.listdir(folder))
            except FileNotFoundError:
                continue
            for name in names:
                if name.startswith("."):
                    continue
                path = os.path.join(folder, name)
                if not os.path.isfile(path):
                    continue
                if os.path.splitext(name)[1].lower() not in exts:
                    continue
                # Strip any (possibly doubled) image extensions to derive a caption.
                base = name
                while os.path.splitext(base)[1].lower() in exts:
                    base = os.path.splitext(base)[0]
                words = base.replace("-", " ").replace("_", " ").strip()
                # Hash-style file names (random hex) get no caption.
                caption = "" if re.fullmatch(r"[0-9a-fA-F]{12,}", base) else words.title()
                rel = f"img/gallery/{cat_slug}/{name}" if cat_slug else f"img/gallery/{name}"
                photos.append({
                    "file": name,
                    "category": cat_slug,
                    "category_label": GALLERY_CAT_LABELS.get(cat_slug, ""),
                    "src": url_for("static", filename=rel),
                    "alt": caption or "Silex Elevator installation",
                    "caption": caption,
                })
        return photos

    @app.route("/gallery")
    def gallery():
        return render_template(
            "gallery.html",
            photos=_gallery_photos(),
            categories=GALLERY_CATEGORIES,
        )

    # -- AI site assistant (grounded in site content, no external API) --------
    @app.route("/api/chat", methods=["POST"])
    @security.rate_limit(30, 60)          # 30 chat messages / minute / IP
    def api_chat():
        data = request.get_json(silent=True) or {}
        message = (data.get("message") or "").strip()[:500]
        if not message:
            return {
                "reply": "Ask me anything about Silex elevators — products, pricing, AMC or contact.",
                "links": [],
                "chips": ["Products", "Get a quote", "AMC & maintenance", "Contact"],
            }
        res = chatbot.answer(message)
        links = []
        for lk in res.get("links", []):
            url = lk.get("url")
            if not url and lk.get("endpoint"):
                try:
                    url = url_for(lk["endpoint"], **lk.get("kwargs", {}))
                except Exception:
                    url = None
            if url:
                links.append({"label": lk["label"], "url": url})
        return {"reply": res["reply"], "links": links, "chips": res.get("chips", [])}

    @app.route("/why-us")
    def why_us():
        return render_template(
            "why_us.html",
            why_us=content.WHY_US,
            stats=content.STATS,
            partners=content.PARTNERS,
            testimonials=content.TESTIMONIALS,
        )

    @app.route("/blog")
    def blog():
        return render_template("blog.html", posts=content.BLOG_POSTS)

    @app.route("/blog/<slug>")
    def blog_post(slug):
        post = next((p for p in content.BLOG_POSTS if p["slug"] == slug), None)
        if post is None:
            abort(404)
        others = [p for p in content.BLOG_POSTS if p["slug"] != slug][:2]
        return render_template("blog_post.html", post=post, others=others)

    # -- Solutions by building segment ---------------------------------------
    def _products_by_slugs(slugs):
        by_slug = {p["slug"]: p for p in content.PRODUCTS}
        return [by_slug[s] for s in slugs if s in by_slug]

    @app.route("/solutions")
    def solutions():
        return render_template("solutions.html", segments=content.SEGMENTS)

    @app.route("/solutions/<slug>")
    def solution_detail(slug):
        segment = next((s for s in content.SEGMENTS if s["slug"] == slug), None)
        if segment is None:
            abort(404)
        return render_template(
            "solution_detail.html",
            segment=segment,
            seg_products=_products_by_slugs(segment["products"]),
            other_segments=[s for s in content.SEGMENTS if s["slug"] != slug],
        )

    # -- Services: AMC / Modernization / Technology --------------------------
    @app.route("/amc")
    def amc():
        return render_template(
            "amc.html",
            plans=content.AMC_PLANS,
            steps=content.SERVICE_STEPS,
        )

    @app.route("/modernization")
    def modernization():
        return render_template("modernization.html", items=content.MODERNIZATION)

    @app.route("/technology")
    def technology():
        return render_template("technology.html", innovations=content.INNOVATIONS)

    # -- Careers -------------------------------------------------------------
    @app.route("/careers", methods=["GET", "POST"])
    @security.rate_limit(6, 60)           # 6 applications / minute / IP
    def careers():
        if request.method == "POST":
            if (request.form.get("website") or "").strip():
                return redirect(url_for("careers"))
            if not csrf_ok():
                flash("Your session expired. Please try submitting again.", "error")
                return redirect(url_for("careers"))
            name = (request.form.get("name") or "").strip()
            phone = (request.form.get("phone") or "").strip()
            email = (request.form.get("email") or "").strip()
            position = (request.form.get("position") or "").strip()
            experience = (request.form.get("experience") or "").strip()
            message = (request.form.get("message") or "").strip()
            if not name or not phone:
                flash("Please provide at least your name and phone number.", "error")
            else:
                db.save_application(name, email, phone, position, experience, message)
                flash(
                    "Thank you for applying! Our HR team will review your "
                    "application and get back to you.",
                    "success",
                )
                return redirect(url_for("careers"))
        return render_template(
            "careers.html",
            openings=content.JOB_OPENINGS,
            why_join=content.WHY_JOIN,
            prefill=request.args.get("role", ""),
        )

    # -- FAQ -----------------------------------------------------------------
    @app.route("/faq")
    def faq():
        return render_template("faq.html", faqs=content.FAQS)

    # -- Legal ---------------------------------------------------------------
    @app.route("/terms")
    def terms():
        return render_template("terms.html")

    @app.route("/privacy")
    def privacy():
        return render_template("privacy.html")

    # -- Site search ---------------------------------------------------------
    @app.route("/search")
    def search():
        q = (request.args.get("q") or "").strip()
        results = []
        if q:
            ql = q.lower()

            def add(title, url, kind, snippet):
                results.append({"title": title, "url": url, "kind": kind, "snippet": snippet})

            for p in content.PRODUCTS:
                hay = " ".join([p["name"], p.get("short", ""), p.get("description", "")]).lower()
                if ql in hay:
                    add(p["name"], url_for("product_detail", slug=p["slug"]),
                        "Product", p.get("short", ""))
            for s in content.SEGMENTS:
                hay = " ".join([s["name"], s["tagline"], s["intro"]]).lower()
                if ql in hay:
                    add(s["name"] + " Solutions", url_for("solution_detail", slug=s["slug"]),
                        "Solution", s["tagline"])
            for b in content.BLOG_POSTS:
                hay = " ".join([b["title"], b["excerpt"]]).lower()
                if ql in hay:
                    add(b["title"], url_for("blog_post", slug=b["slug"]),
                        "Blog", b["excerpt"])
            for f in content.FAQS:
                if ql in (f["q"] + " " + f["a"]).lower():
                    add(f["q"], url_for("faq"), "FAQ", f["a"][:120] + "…")
            pages = [
                ("About Us", url_for("about"), "about silex company history"),
                ("Services", url_for("services"), "elevator services installation finishes doors"),
                ("AMC & Maintenance", url_for("amc"), "annual maintenance contract amc support breakdown"),
                ("Modernization", url_for("modernization"), "modernization upgrade retrofit existing elevator"),
                ("Technology & Innovations", url_for("technology"), "technology innovation gearless vvvf ard"),
                ("Careers", url_for("careers"), "careers jobs hiring vacancy"),
                ("Projects", url_for("projects"), "projects references installations"),
                ("Contact", url_for("contact"), "contact quote enquiry phone address"),
            ]
            for title, url, kw in pages:
                if ql in (title + " " + kw).lower():
                    add(title, url, "Page", "")
        return render_template("search.html", q=q, results=results)

    @app.route("/contact", methods=["GET", "POST"])
    @security.rate_limit(6, 60)           # 6 enquiry submits / minute / IP
    def contact():
        if request.method == "POST":
            # Honeypot: real users never fill the hidden "website" field.
            if (request.form.get("website") or "").strip():
                # Silently pretend success to bots.
                return redirect(url_for("contact"))

            if not csrf_ok():
                flash("Your session expired. Please try submitting again.", "error")
                return redirect(url_for("contact"))

            name = (request.form.get("name") or "").strip()
            phone = (request.form.get("phone") or "").strip()
            email = (request.form.get("email") or "").strip()
            city = (request.form.get("city") or "").strip()
            etype = (request.form.get("elevator_type") or "").strip()
            message = (request.form.get("message") or "").strip()

            if not name or not phone:
                flash("Please provide at least your name and phone number.", "error")
            else:
                db.save_enquiry(name, email, phone, city, etype, message)
                flash(
                    "Thank you! Your enquiry has been received. "
                    "Our team will contact you shortly.",
                    "success",
                )
                return redirect(url_for("contact"))

        return render_template(
            "contact.html",
            enquiry_types=content.ENQUIRY_TYPES,
            prefill=request.args.get("type", ""),
        )

    # -- Brochure download ---------------------------------------------------
    @app.route("/brochure")
    def brochure():
        return send_from_directory(
            app.static_folder,
            app.config["BROCHURE_FILE"],
            as_attachment=True,
            download_name="Silex-Elevator-Brochure.pdf",
        )

    # -- Admin ---------------------------------------------------------------
    def login_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get("admin"):
                return redirect(url_for("admin_login", next=request.path))
            return view(*args, **kwargs)
        return wrapped

    @app.route("/admin/login", methods=["GET", "POST"])
    @security.rate_limit(8, 300)          # 8 login attempts / 5 min / IP
    def admin_login():
        if session.get("admin"):
            return redirect(url_for("admin"))
        if request.method == "POST":
            if not csrf_ok():
                flash("Session expired, please try again.", "error")
                return redirect(url_for("admin_login"))
            user = (request.form.get("username") or "").strip()
            pw = request.form.get("password") or ""
            if (user == app.config["ADMIN_USER"]
                    and secrets.compare_digest(pw, app.config["ADMIN_PASSWORD"])):
                # Prevent session fixation: start a fresh session on login.
                session.clear()
                session["admin"] = True
                session.permanent = True
                nxt = request.args.get("next") or url_for("admin")
                # Only allow relative, same-site redirect targets.
                if not nxt.startswith("/") or nxt.startswith("//"):
                    nxt = url_for("admin")
                return redirect(nxt)
            flash("Invalid username or password.", "error")
        return render_template("admin_login.html")

    @app.route("/admin/logout")
    def admin_logout():
        session.pop("admin", None)
        return redirect(url_for("admin_login"))

    @app.route("/admin")
    @login_required
    def admin():
        enquiries = db.get_enquiries()
        applications = db.get_applications()
        return render_template(
            "admin.html",
            enquiries=enquiries,
            total=len(enquiries),
            applications=applications,
            gallery=_gallery_photos(),
            categories=GALLERY_CATEGORIES,
        )

    @app.route("/admin/export.csv")
    @login_required
    def admin_export():
        rows = db.get_enquiries()
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(
            ["id", "name", "email", "phone", "city",
             "elevator_type", "message", "created_at"]
        )
        for r in rows:
            writer.writerow([
                r["id"], r["name"], r["email"], r["phone"], r["city"],
                r["elevator_type"], r["message"], r["created_at"],
            ])
        out = make_response(buf.getvalue())
        out.headers["Content-Type"] = "text/csv"
        out.headers["Content-Disposition"] = (
            "attachment; filename=silex-enquiries.csv"
        )
        return out

    # -- Admin · Gallery management ------------------------------------------
    @app.route("/admin/gallery/upload", methods=["POST"])
    @login_required
    @security.rate_limit(30, 60)
    def admin_gallery_upload():
        if not csrf_ok():
            flash("Your session expired. Please try again.", "error")
            return redirect(url_for("admin") + "#gallery")
        category = (request.form.get("category") or "").strip()
        if category not in GALLERY_CAT_SLUGS:
            flash("Please choose a category for the photos.", "error")
            return redirect(url_for("admin") + "#gallery")
        folder = os.path.join(app.static_folder, "img", "gallery", category)
        os.makedirs(folder, exist_ok=True)
        saved, skipped = 0, 0
        for f in request.files.getlist("photos"):
            if not f or not f.filename:
                continue
            head = f.stream.read(32)
            f.stream.seek(0)
            if not _is_allowed_image(f.filename, head):
                skipped += 1
                continue
            name = secure_filename(f.filename)
            if not name:
                skipped += 1
                continue
            # Never overwrite an existing photo.
            dest = os.path.join(folder, name)
            if os.path.exists(dest):
                stem, ext = os.path.splitext(name)
                name = f"{stem}-{secrets.token_hex(4)}{ext}"
                dest = os.path.join(folder, name)
            f.save(dest)
            saved += 1
        if saved:
            flash(f"Uploaded {saved} photo(s) to {GALLERY_CAT_LABELS[category]}.", "success")
        if skipped:
            flash(f"Skipped {skipped} file(s) — only real image files are allowed.", "error")
        if not saved and not skipped:
            flash("Please choose at least one image to upload.", "error")
        return redirect(url_for("admin") + "#gallery")

    @app.route("/admin/gallery/delete", methods=["POST"])
    @login_required
    def admin_gallery_delete():
        if not csrf_ok():
            flash("Your session expired. Please try again.", "error")
            return redirect(url_for("admin") + "#gallery")
        base_folder = os.path.abspath(os.path.join(app.static_folder, "img", "gallery"))
        category = os.path.basename((request.form.get("category") or "").strip())
        folder = (os.path.join(base_folder, category)
                  if category in GALLERY_CAT_SLUGS else base_folder)
        safe = os.path.basename((request.form.get("file") or "").strip())
        target = os.path.abspath(os.path.join(folder, safe))
        # Path-traversal safe: the resolved target must sit inside the gallery tree.
        if (safe and target.startswith(base_folder + os.sep)
                and os.path.isfile(target)
                and os.path.splitext(safe)[1].lower() in GALLERY_EXTS):
            try:
                os.remove(target)
                flash("Photo removed from the gallery.", "success")
            except OSError:
                flash("Could not remove that photo.", "error")
        else:
            flash("That photo no longer exists.", "error")
        return redirect(url_for("admin") + "#gallery")

    # -- SEO -----------------------------------------------------------------
    @app.route("/robots.txt")
    def robots():
        lines = [
            "User-agent: *",
            "Allow: /",
            "Disallow: /admin",
            "Sitemap: {}/sitemap.xml".format(app.config["SITE_URL"].rstrip("/")),
        ]
        return Response("\n".join(lines), mimetype="text/plain")

    @app.route("/sitemap.xml")
    def sitemap():
        base = app.config["SITE_URL"].rstrip("/")
        urls = [
            url_for("home"), url_for("about"), url_for("products"),
            url_for("services"), url_for("projects"), url_for("why_us"),
            url_for("blog"), url_for("contact"), url_for("solutions"),
            url_for("amc"), url_for("modernization"), url_for("technology"),
            url_for("careers"), url_for("faq"), url_for("terms"), url_for("privacy"),
        ]
        urls += [url_for("product_detail", slug=p["slug"]) for p in content.PRODUCTS]
        urls += [url_for("solution_detail", slug=s["slug"]) for s in content.SEGMENTS]
        urls += [url_for("blog_post", slug=p["slug"]) for p in content.BLOG_POSTS]
        today = datetime.utcnow().strftime("%Y-%m-%d")
        items = "".join(
            "<url><loc>{}{}</loc><lastmod>{}</lastmod></url>".format(base, u, today)
            for u in urls
        )
        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            + items + "</urlset>"
        )
        return Response(xml, mimetype="application/xml")

    # -- Errors --------------------------------------------------------------
    @app.errorhandler(400)
    def bad_request(_e):
        return render_template("error.html", code=400,
                               title="Bad request",
                               message="We couldn't process that request."), 400

    @app.errorhandler(403)
    def forbidden(_e):
        return render_template("error.html", code=403,
                               title="Access denied",
                               message="You don't have permission to view this page."), 403

    @app.errorhandler(404)
    def not_found(_e):
        return render_template("404.html"), 404

    @app.errorhandler(413)
    def too_large(_e):
        return render_template("error.html", code=413,
                               title="Request too large",
                               message="The data you sent was too large."), 413

    @app.errorhandler(429)
    def too_many(_e):
        return render_template("429.html"), 429

    @app.errorhandler(500)
    def server_error(_e):
        # Never leak stack traces to visitors.
        return render_template("error.html", code=500,
                               title="Something went wrong",
                               message="An unexpected error occurred. Please try again."), 500

    return app


app = create_app()


if __name__ == "__main__":
    # Debug is opt-in via env only, so tracebacks never leak in production.
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes", "on")
    app.run(debug=debug)
