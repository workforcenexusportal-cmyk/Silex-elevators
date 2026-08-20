# Silex Elevator — Website

Premium marketing website for **Silex Elevator PVT. LTD** (ISO 9001:2008 certified
elevator manufacturer, Surat, Gujarat, India). Built with **Flask 3** + Jinja2, a
custom design system (navy / steel-silver / titanium-gold), a working enquiry &
careers pipeline backed by SQLite, an interactive **360° Virtual Showroom**, a
photo **Gallery** with an admin management panel, and a lightweight rule-based
chatbot. Designed to deploy on **PythonAnywhere**.

> Slogan: *Your Trusted Partner to the Top.*
> Tagline: *Elevating spaces with precision and trust.*

---

## ✨ Features

- Fully responsive, animated single-brand site (navy + gold, elevator-motion motif)
- Full-bleed hero with real elevator photography, animated reveals and a sticky navbar
- Two floating quick-link pills under the header: **Gallery** and **Virtual Showroom**
- **360° Virtual Showroom** — interactive panorama viewer available site-wide
- **Gallery** with three categories (Cabin · Control Operating Panel · Landing
  Operating Panel) and client-side category filtering
- **Admin panel** (`/admin`) — login-protected dashboard to:
  - View & CSV-export **enquiries**
  - Review **career applications**
  - **Upload / delete gallery photos** per category
- Working **Get a Quote / Contact** form with an inline **cost estimator**
- **Careers** page with a job-application form (saved to SQLite)
- **AMC & Maintenance** page with three transparent annual plans (₹ pricing + GST)
- **Solutions** (by segment), **Products** (per-product detail), **Services**,
  **Modernization**, **Technology**, **Projects**, **Why Us**, **Blog** (+ post),
  **FAQ**, site **Search**, **Terms**, **Privacy**, custom **404**
- Rule-based **chatbot** API (`/api/chat`) for common visitor questions
- Brochure download endpoint (`/brochure`)
- PWA web manifest, floating WhatsApp button, scroll-reveal animations
- Security hardening: CSRF tokens, per-IP rate limiting, honeypot fields,
  CSP nonces, session-fixation protection
- All copy lives in [`content.py`](content.py); brand/contact in [`config.py`](config.py)

---

## 🧱 Tech stack

| Layer | Choice | Why |
|---|---|---|
| Backend | Flask 3.0.3 | Lightweight, first-class on PythonAnywhere |
| Templating | Jinja2 | Ships with Flask |
| Styling | Custom CSS | Unique look, no framework bloat |
| Data | SQLite (stdlib `sqlite3`) | Zero-setup enquiry / application storage |
| Fonts | Sora + Inter (Google Fonts) | Premium display + clean body |

---

## 🗺️ Routes

| Path | Purpose |
|---|---|
| `/` | Home (hero, stats, showroom, panels) |
| `/about` · `/why-us` | Company info |
| `/products` · `/products/<slug>` | Product ranges + detail |
| `/solutions` · `/solutions/<slug>` | Segment solutions + detail |
| `/services` · `/amc` · `/modernization` · `/technology` | Service pages |
| `/gallery` | Photo gallery (Cabin / COP / LOP) |
| `/projects` · `/blog` · `/blog/<slug>` | References & articles |
| `/careers` | Jobs + application form |
| `/faq` · `/terms` · `/privacy` · `/search` | Utility pages |
| `/contact` | Enquiry form (+ estimator prefill) |
| `/brochure` | PDF brochure download |
| `/api/chat` | Chatbot endpoint (POST) |
| `/admin/login` · `/admin` · `/admin/logout` | Admin auth + dashboard |
| `/admin/export.csv` | Enquiries CSV export |
| `/admin/gallery/upload` · `/admin/gallery/delete` | Gallery management (POST) |

---

## 🚀 Run locally (Windows / PowerShell)

```powershell
cd C:\Users\Katana\Desktop\Silex-elevators

# 1. Create & activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python app.py
```

Then open <http://127.0.0.1:5000> in your browser.

On macOS/Linux use `source venv/bin/activate` instead of the Activate.ps1 line.

---

## 🔐 Configuration & environment variables

Defaults live in [`config.py`](config.py) and can be overridden with environment
variables (recommended for anything secret in production):

| Variable | Default (dev) | Purpose |
|---|---|---|
| `SILEX_SECRET_KEY` | dev fallback | Flask session signing key — **set a long random value in production** |
| `SILEX_ADMIN_USER` | `rajvasani` | Admin login username |
| `SILEX_ADMIN_PASSWORD` | *(set in config)* | Admin login password — **override in production** |

> On PythonAnywhere the web app reads these from the **WSGI file** (or the Web
> tab environment variables), which **override** the defaults in `config.py`.
> Setting them only in a Bash console does **not** affect the running web app.

---

## ☁️ Deploy on PythonAnywhere

1. On PythonAnywhere open a **Bash console** and clone the repo:
   ```bash
   git clone https://github.com/workforcenexusportal-cmyk/Silex-elevators.git
   ```
2. **Create a virtualenv** and install deps:
   ```bash
   cd Silex-elevators
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Web tab → Add a new web app → Manual configuration** (matching Python 3.x).
4. In the web app settings:
   - **Source code:** `/home/<youruser>/Silex-elevators`
   - **Virtualenv:** `/home/<youruser>/Silex-elevators/venv`
5. **Edit the WSGI file** (link on the Web tab) so it points at the app and sets
   the secrets:
   ```python
   import sys, os
   path = '/home/<youruser>/Silex-elevators'
   if path not in sys.path:
       sys.path.insert(0, path)

   os.environ['SILEX_SECRET_KEY']     = '<a long random string>'
   os.environ['SILEX_ADMIN_USER']     = 'rajvasani'
   os.environ['SILEX_ADMIN_PASSWORD'] = '<your admin password>'

   from wsgi import application
   ```
6. Click **Reload**. The site is live at `https://<youruser>.pythonanywhere.com`.

### Deploying updates

```bash
cd ~/Silex-elevators
git pull origin main
# reload the web app
touch /var/www/<youruser>_pythonanywhere_com_wsgi.py
```

> The SQLite database is created automatically in the `instance/` folder on first
> run. To keep the live database when pulling, `git stash` any local DB changes first.

---

## 🛠️ Admin panel

- Log in at `/admin/login` with `SILEX_ADMIN_USER` / `SILEX_ADMIN_PASSWORD`.
- Dashboard shows all **enquiries** and **career applications**; export enquiries
  via **Download CSV** (`/admin/export.csv`).
- **Gallery management:** upload photos into a category (Cabin / Control Operating
  Panel / Landing Operating Panel) or delete existing ones. Files are stored under
  `static/img/gallery/<category>/`.

---

## 📝 Editing content

- **Contact details / brand / admin creds:** [`config.py`](config.py)
- **Products, solutions, services, projects, blog, testimonials, FAQs, showroom
  scenes, plans:** [`content.py`](content.py)
- **Colours / fonts / spacing:** CSS variables at the top of
  [`static/css/style.css`](static/css/style.css)
- **Chatbot answers:** [`chatbot.py`](chatbot.py)

No template editing needed for routine content changes.

---

## 📂 Project structure

```
Silex-elevators/
├─ app.py              # Flask routes & app factory
├─ wsgi.py             # PythonAnywhere entry point
├─ config.py           # Brand, contact & admin config
├─ content.py          # All site copy/data
├─ db.py               # SQLite enquiry & application storage
├─ security.py         # CSRF, rate limiting, headers/CSP helpers
├─ chatbot.py          # Rule-based chatbot logic
├─ requirements.txt
├─ instance/
│  └─ silex.sqlite3    # Auto-created database
├─ static/
│  ├─ css/style.css    # Design system
│  ├─ js/main.js       # Nav, scroll reveal, hero, showroom, gallery filters
│  ├─ site.webmanifest # PWA manifest
│  └─ img/             # Logos, hero/section photos, gallery/<category>/
└─ templates/
   ├─ base.html        # Layout, navbar, quick-links, footer, showroom modal
   ├─ _icons.html      # Inline SVG icon macros
   ├─ _cta.html  _estimator.html
   ├─ index.html  about.html  why_us.html
   ├─ products.html  product_detail.html
   ├─ solutions.html  solution_detail.html
   ├─ services.html  amc.html  modernization.html  technology.html
   ├─ gallery.html  projects.html  blog.html  blog_post.html
   ├─ careers.html  faq.html  contact.html  search.html
   ├─ terms.html  privacy.html  404.html
   ├─ admin_login.html  admin.html
```

---

## 🔎 Viewing enquiries

Submitted quotes are stored in `instance/silex.sqlite3`, table `enquiries`
(career applications are in `applications`). Use the admin dashboard, the CSV
export, or a Python shell:

```python
import sqlite3
con = sqlite3.connect("instance/silex.sqlite3")
con.row_factory = sqlite3.Row
for row in con.execute("SELECT * FROM enquiries ORDER BY id DESC"):
    print(dict(row))
```

---

*Presentation build. Product specs and contact details are taken from the official
Silex brochure; projects, testimonials and blog posts are illustrative placeholders
to be confirmed with the client.*
