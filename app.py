"""Silex Elevator — Flask application.

A lightweight company website with a working enquiry form backed by SQLite,
an admin dashboard, email notifications, SEO endpoints and a brochure
download. Designed to deploy cleanly on PythonAnywhere.
"""
import csv
import io
import os
import secrets
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for, flash, abort,
    session, send_from_directory, Response, make_response,
)

import content
import db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

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
            scenes=content.SHOWROOM_SCENES,
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
        folder = os.path.join(app.static_folder, "img", "gallery")
        try:
            names = sorted(os.listdir(folder))
        except FileNotFoundError:
            names = []
        photos = []
        for name in names:
            if name.startswith("."):
                continue
            if os.path.splitext(name)[1].lower() in exts:
                photos.append({
                    "src": url_for("static", filename=f"img/gallery/{name}"),
                    "alt": os.path.splitext(name)[0].replace("-", " ").replace("_", " ").title(),
                })
        return photos

    @app.route("/gallery")
    def gallery():
        return render_template("gallery.html", photos=_gallery_photos())

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
                session["admin"] = True
                nxt = request.args.get("next") or url_for("admin")
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
    @app.errorhandler(404)
    def not_found(_e):
        return render_template("404.html"), 404

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
