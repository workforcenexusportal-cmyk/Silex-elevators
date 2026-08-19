"""Silex site assistant — a lightweight, dependency-free retrieval chatbot.

It answers visitor questions using only the site's own content (products,
specs, services, FAQs, solutions and contact details), so it needs no external
API keys, no network calls and no paid model — it works fully offline. Think of
it as a well-trained virtual receptionist that knows the entire Silex catalogue.

The public entry point is ``answer(message) -> dict`` returning::

    {"reply": str, "links": [{"label", "endpoint", "kwargs"}], "chips": [str]}

The Flask route resolves the endpoint links into real URLs with ``url_for``.
"""
import re

import content
from config import Config

_WORD = re.compile(r"[a-z0-9]+")

_STOP = {
    "a", "an", "the", "is", "are", "am", "do", "does", "did", "of", "for", "to",
    "in", "on", "at", "and", "or", "my", "your", "you", "i", "we", "it", "this",
    "that", "with", "can", "could", "would", "should", "please", "me", "us",
    "have", "has", "want", "need", "get", "give", "tell", "about", "what", "whats",
    "how", "which", "there", "their", "be", "will", "any", "some", "from", "by",
}

# Normalise everyday words to the vocabulary used across the catalogue.
_SYNONYMS = {
    "lift": "elevator", "lifts": "elevator", "elevators": "elevator",
    "elevater": "elevator", "elavator": "elevator",
    "price": "cost", "prices": "cost", "pricing": "cost", "quote": "cost",
    "quotation": "cost", "rate": "cost", "rates": "cost", "budget": "cost",
    "buy": "cost", "purchase": "cost", "cheap": "cost", "affordable": "cost",
    "amc": "maintenance", "servicing": "maintenance", "service": "maintenance",
    "repair": "maintenance", "breakdown": "maintenance", "support": "maintenance",
    "freight": "goods", "cargo": "goods", "material": "goods",
    "stretcher": "hospital", "bed": "hospital", "patient": "hospital",
    "medical": "hospital", "clinic": "hospital",
    "glass": "capsule", "panoramic": "capsule", "scenic": "capsule",
    "home": "residential", "house": "residential", "villa": "residential",
    "bungalow": "residential", "apartment": "residential", "flat": "residential",
    "office": "commercial", "corporate": "commercial", "business": "commercial",
    "mall": "retail", "shop": "retail", "showroom": "retail", "store": "retail",
    "hotel": "hotel", "resort": "hotel", "hospitality": "hotel",
    "factory": "industrial", "warehouse": "industrial", "plant": "industrial",
    "godown": "industrial", "parking": "parking", "car": "parking",
    "gearless": "mrl", "machineroom": "mrl",
    "phone": "contact", "call": "contact", "mobile": "contact", "number": "contact",
    "email": "contact", "mail": "contact", "whatsapp": "contact", "reach": "contact",
    "products": "product", "types": "type", "kinds": "type", "kind": "type",
    "ranges": "range", "models": "product", "model": "product", "catalogues": "brochure",
    "offerings": "offer", "offering": "offer", "options": "product", "sell": "product",
    "address": "location", "where": "location", "located": "location",
    "city": "location", "cities": "location", "area": "location", "serve": "location",
    "brochure": "brochure", "pdf": "brochure", "catalogue": "brochure",
    "catalog": "brochure", "download": "brochure",
    "job": "careers", "jobs": "careers", "hiring": "careers", "vacancy": "careers",
    "career": "careers", "work": "careers", "recruitment": "careers",
    "upgrade": "modernization", "retrofit": "modernization", "modernize": "modernization",
    "modernise": "modernization", "renovate": "modernization",
    "photo": "gallery", "photos": "gallery", "pictures": "gallery", "images": "gallery",
    "project": "projects", "projects": "projects", "installation": "projects",
    "company": "about", "who": "about", "history": "about", "iso": "about",
    "certified": "about", "certificate": "about", "experience": "about",
    "capacity": "capacity", "persons": "capacity", "person": "capacity",
    "people": "capacity", "kg": "capacity", "load": "capacity", "weight": "capacity",
    "speed": "speed", "fast": "speed", "warranty": "warranty", "guarantee": "warranty",
    "safe": "safety", "safety": "safety", "power": "safety", "ard": "safety",
}


def _tokens(text):
    out = set()
    for w in _WORD.findall((text or "").lower()):
        w = _SYNONYMS.get(w, w)
        if w not in _STOP and len(w) > 1:
            out.add(w)
    return out


# ---------------------------------------------------------------------------
# Knowledge base — built once from the site content
# ---------------------------------------------------------------------------
def _build_kb():
    docs = []

    for p in content.PRODUCTS:
        spec = content.SPECS.get(p["slug"], {})
        summary = "; ".join(f"{k}: {v}" for k, v in (spec.get("summary") or []))
        highlights = " ".join(p.get("highlights", [])[:2])
        reply = (
            f"{p['name']} — {p.get('short','')} "
            f"Capacity: {p.get('capacity','—')}. Speed: {p.get('speed','—')}. "
            f"Highlights: {highlights}."
        )
        docs.append({
            "kind": "product",
            "tokens": _tokens(
                p["name"] + " " + p["slug"].replace("-", " ") + " elevator " +
                p.get("short", "") + " " + " ".join(p.get("highlights", [])) + " " + summary
            ),
            "reply": reply,
            "links": [{"label": f"View {p['name'].split('—')[0].strip()}",
                       "endpoint": "product_detail", "kwargs": {"slug": p["slug"]}}],
            "chips": ["Get a quote", "Capacity & speed", "AMC & maintenance"],
        })

    for s in content.SEGMENTS:
        docs.append({
            "kind": "segment",
            "tokens": _tokens(s["name"] + " " + s["tagline"] + " " + s["intro"] + " solution segment"),
            "reply": f"{s['name']} — {s['tagline']}. {s['intro']}",
            "links": [{"label": f"{s['name']} solutions",
                       "endpoint": "solution_detail", "kwargs": {"slug": s["slug"]}}],
            "chips": ["See products", "Get a quote", "Contact us"],
        })

    for f in content.FAQS:
        links = []
        low = (f["q"] + f["a"]).lower()
        if "amc" in low or "maintenance" in low:
            links.append({"label": "AMC & Maintenance", "endpoint": "amc", "kwargs": {}})
        elif "moderniz" in low:
            links.append({"label": "Modernization", "endpoint": "modernization", "kwargs": {}})
        docs.append({
            "kind": "faq",
            "tokens": _tokens(f["q"] + " " + f["a"]),
            "reply": f["a"],
            "links": links,
            "chips": ["Get a quote", "Talk to a human", "More FAQs"],
        })

    return docs


_KB = _build_kb()


# ---------------------------------------------------------------------------
# Intent handlers (canned, high-confidence answers)
# ---------------------------------------------------------------------------
def _greeting():
    return {
        "reply": ("Hi! 👋 I'm the Silex Assistant. I can help you explore our "
                  "elevator range, share specs, pricing guidance, AMC plans or "
                  "connect you with our team. What are you looking for?"),
        "links": [{"label": "Browse products", "endpoint": "products", "kwargs": {}}],
        "chips": ["Products", "Get a quote", "AMC & maintenance", "Contact"],
    }


def _contact():
    return {
        "reply": (f"You can reach Silex Elevator here:\n"
                  f"📞 {Config.PHONE} / {Config.PHONE_ALT}\n"
                  f"✉️ {Config.EMAIL}\n"
                  f"📍 {Config.ADDRESS}\n"
                  f"Contact persons: {Config.CONTACT_PERSON} & {Config.CONTACT_PERSON_ALT}."),
        "links": [
            {"label": "Contact page", "endpoint": "contact", "kwargs": {}},
            {"label": "WhatsApp us", "url": f"https://wa.me/{Config.WHATSAPP}"},
        ],
        "chips": ["Get a quote", "Where are you located?", "Products"],
    }


def _location():
    return {
        "reply": (f"Our head office is at {Config.ADDRESS}. We're {Config.CERTIFICATION} "
                  f"and serve 20+ cities across India from Surat, with a network reaching "
                  f"10+ countries. Tell me your city and I'll help you get started."),
        "links": [{"label": "Contact us", "endpoint": "contact", "kwargs": {}}],
        "chips": ["Get a quote", "Call us", "Products"],
    }


def _quote():
    return {
        "reply": ("Every Silex elevator is custom-engineered, so pricing depends on the "
                  "type, capacity, travel height, finishes and site conditions. Share a "
                  "few details and we'll prepare a free, no-obligation quote after a site "
                  "survey — usually within 1–2 working days."),
        "links": [
            {"label": "Get a free quote", "endpoint": "contact", "kwargs": {}},
            {"label": "Call now", "url": f"tel:{Config.PHONE.replace(' ', '')}"},
        ],
        "chips": ["Products", "AMC plans", "Which lift suits me?"],
    }


def _brochure():
    return {
        "reply": ("You can download the full Silex Elevator brochure (PDF) with every "
                  "product, dimension table and finish option here."),
        "links": [{"label": "Download brochure (PDF)", "endpoint": "brochure", "kwargs": {}}],
        "chips": ["Products", "Get a quote", "Contact"],
    }


def _amc():
    return {
        "reply": ("Yes — we offer Essential, Comprehensive and Premium Care Annual "
                  "Maintenance Contracts (AMC) with scheduled preventive visits, genuine "
                  "spares and 24×7 breakdown support to keep your lift safe and smooth."),
        "links": [{"label": "AMC & Maintenance", "endpoint": "amc", "kwargs": {}}],
        "chips": ["Get a quote", "Modernization", "Contact"],
    }


def _modernization():
    return {
        "reply": ("We modernize ageing elevators — upgrading drives, controllers, doors, "
                  "cabins and safety systems — often without replacing the whole unit, for "
                  "a smoother, safer and more efficient ride."),
        "links": [{"label": "Modernization", "endpoint": "modernization", "kwargs": {}}],
        "chips": ["Get a quote", "AMC & maintenance", "Contact"],
    }


def _careers():
    roles = ", ".join(j["title"] for j in content.JOB_OPENINGS[:4])
    return {
        "reply": (f"We're growing! Current openings include: {roles}. "
                  f"You can view roles and apply online on our Careers page."),
        "links": [{"label": "View careers", "endpoint": "careers", "kwargs": {}}],
        "chips": ["Contact HR", "About Silex", "Products"],
    }


def _products_overview():
    names = [p["name"].split("—")[0].strip() for p in content.PRODUCTS]
    listed = ", ".join(names)
    return {
        "reply": (f"We manufacture {len(names)} elevator ranges: {listed}. "
                  f"Tell me your building type (home, office, hospital, mall, factory…) "
                  f"and I'll recommend the right one."),
        "links": [{"label": "All products", "endpoint": "products", "kwargs": {}}],
        "chips": ["Home elevator", "Capsule lift", "Goods lift", "Get a quote"],
    }


def _about():
    return {
        "reply": (f"Silex Elevator is an {Config.CERTIFICATION} manufacturer, supplier and "
                  f"exporter of premium elevators, proudly engineered in India. {Config.COMPANY_TAGLINE}. "
                  f"We cover 20+ cities and 10+ countries with a full range from MRL to "
                  f"panoramic capsules, hospital, goods and hydraulic lifts."),
        "links": [{"label": "About us", "endpoint": "about", "kwargs": {}}],
        "chips": ["Products", "Why choose Silex?", "Get a quote"],
    }


def _gallery():
    return {
        "reply": ("Take a look at our photo gallery and completed projects to see Silex "
                  "cabins, finishes and real installations."),
        "links": [
            {"label": "Photo gallery", "endpoint": "gallery", "kwargs": {}},
            {"label": "Projects", "endpoint": "projects", "kwargs": {}},
        ],
        "chips": ["Products", "Get a quote", "Contact"],
    }


def _fallback():
    return {
        "reply": ("I'm not fully sure about that one, but I'd love to help. You can ask me "
                  "about our elevator types, capacity & speed, pricing, AMC plans, or our "
                  "location — or I can connect you with the Silex team directly."),
        "links": [{"label": "Talk to our team", "endpoint": "contact", "kwargs": {}}],
        "chips": ["Products", "Get a quote", "AMC & maintenance", "Contact"],
    }


# Intent keyword sets → handler. Order matters (first strong match wins).
_INTENTS = [
    (lambda t, raw: raw.strip().lower() in {"hi", "hii", "hey", "hello", "helo",
        "yo", "hola", "namaste", "good morning", "good evening", "good afternoon",
        "start", "menu"}, _greeting),
    (lambda t, raw: {"thanks", "thank", "thankyou", "thx", "great", "awesome"}
        & set(_WORD.findall(raw.lower())) and len(t) <= 2,
        lambda: {"reply": "You're welcome! 😊 Anything else I can help you with?",
                 "links": [], "chips": ["Products", "Get a quote", "Contact"]}),
    (lambda t, raw: "brochure" in t, _brochure),
    (lambda t, raw: "cost" in t, _quote),
    (lambda t, raw: "careers" in t, _careers),
    (lambda t, raw: "maintenance" in t and "modernization" not in t, _amc),
    (lambda t, raw: "modernization" in t, _modernization),
    (lambda t, raw: "gallery" in t or "projects" in t, _gallery),
    (lambda t, raw: "contact" in t, _contact),
    (lambda t, raw: "location" in t, _location),
    (lambda t, raw: "about" in t, _about),
    (lambda t, raw: ("product" in t or "range" in t or "type" in t or "offer" in t
        or "catalogue" in t) and not (t & {"capsule", "hospital", "goods", "hydraulic",
        "mrl", "industrial", "parking", "residential"}), _products_overview),
]


def answer(message):
    """Return a grounded answer dict for the visitor's message."""
    raw = message or ""
    t = _tokens(raw)

    for match, handler in _INTENTS:
        try:
            if match(t, raw):
                return handler()
        except Exception:
            pass

    # Retrieval over the knowledge base (products, segments, FAQs).
    best, best_score = None, 0
    for doc in _KB:
        overlap = t & doc["tokens"]
        if not overlap:
            continue
        score = len(overlap)
        # Boost strong product/segment signals.
        if doc["kind"] in ("product", "segment"):
            score += 0.5
        if score > best_score:
            best, best_score = doc, score

    if best and best_score >= 1.5:
        return {"reply": best["reply"], "links": best["links"], "chips": best["chips"]}

    return _fallback()
