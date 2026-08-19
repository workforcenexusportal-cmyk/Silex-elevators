# Silex Elevator — Website

Premium marketing website for **Silex Elevator** (ISO 9001:2008 certified elevator
manufacturer, Surat, Gujarat, India). Built with **Flask** + Jinja2, a custom
design system (navy / steel-silver / titanium-gold), and a working enquiry form
backed by SQLite. Designed to deploy on **PythonAnywhere**.

> Tagline: *Enjoy Silky Motion at Affordable Cost.*

---

## ✨ Features

- Fully responsive, animated single-brand site (navy + gold, elevator-motion motif)
- Pages: Home, About, Products (+ per-product detail), Services, Projects, Why Us,
  Blog (+ post detail), Contact, custom 404
- 10 elevator product lines sourced from the official brochure
- Working **Get a Quote / Contact** form that saves enquiries to SQLite
- Floating WhatsApp button, sticky navbar, scroll-reveal animations
- No external image dependencies — all visuals are CSS/SVG (fast + reliable)
- All copy lives in [`content.py`](content.py); contact details in [`config.py`](config.py)

---

## 🧱 Tech stack

| Layer | Choice | Why |
|---|---|---|
| Backend | Flask 3 | Lightweight, perfect for a company site, first-class on PythonAnywhere |
| Templating | Jinja2 | Ships with Flask |
| Styling | Custom CSS | Unique look, no framework bloat |
| Data | SQLite (stdlib `sqlite3`) | Zero-setup enquiry storage |
| Fonts | Sora + Inter (Google Fonts) | Premium display + clean body |

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

## ☁️ Deploy on PythonAnywhere

1. **Push this project to GitHub** (see below), then on PythonAnywhere open a
   **Bash console** and clone it:
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
5. **Edit the WSGI file** (link on the Web tab) and replace its contents with:
   ```python
   import sys
   path = '/home/<youruser>/Silex-elevators'
   if path not in sys.path:
       sys.path.insert(0, path)
   from wsgi import application
   ```
6. (Recommended) In the **Web tab → Environment variables**, set a real secret:
   `SILEX_SECRET_KEY = <a long random string>`
7. Click **Reload**. Your site is live at `https://<youruser>.pythonanywhere.com`.

> The SQLite database is created automatically in the `instance/` folder on first run.

---

## 📤 Push to GitHub

```powershell
cd C:\Users\Katana\Desktop\Silex-elevators
git init
git add .
git commit -m "Initial Silex Elevator website"
git branch -M main
git remote add origin https://github.com/workforcenexusportal-cmyk/Silex-elevators.git
git push -u origin main
```

---

## 📝 Editing content

- **Contact details / brand:** [`config.py`](config.py)
- **Products, services, projects, blog, testimonials:** [`content.py`](content.py)
- **Colours / fonts / spacing:** CSS variables at the top of
  [`static/css/style.css`](static/css/style.css)

No template editing needed for routine content changes.

---

## 📂 Project structure

```
Silex-elevators/
├─ app.py              # Flask routes
├─ wsgi.py             # PythonAnywhere entry point
├─ config.py           # Brand + contact config
├─ content.py          # All site copy/data
├─ db.py               # SQLite enquiry storage
├─ requirements.txt
├─ static/
│  ├─ css/style.css    # Design system
│  └─ js/main.js       # Nav, scroll reveal, hero animation
└─ templates/
   ├─ base.html        # Layout, navbar, footer
   ├─ _icons.html      # Inline SVG icon macros
   ├─ _cta.html        # Reusable call-to-action
   ├─ index.html  about.html  products.html  product_detail.html
   ├─ services.html  projects.html  why_us.html
   ├─ blog.html  blog_post.html  contact.html  404.html
```

---

## 🔎 Viewing enquiries

Submitted quotes are stored in `instance/silex.sqlite3`, table `enquiries`.
Inspect them from a Python shell:

```python
import sqlite3
con = sqlite3.connect("instance/silex.sqlite3")
con.row_factory = sqlite3.Row
for row in con.execute("SELECT * FROM enquiries ORDER BY id DESC"):
    print(dict(row))
```

---

*Dummy presentation build. Product specs and contact details are taken from the
official Silex brochure; projects, testimonials and blog posts are illustrative
placeholders to be confirmed with the client.*
