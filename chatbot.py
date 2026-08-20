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
        "reply": ("Yes — we offer three Annual Maintenance Contracts (AMC):\n"
                  "• Essential (Basic Cover) — ₹8,500 + 18% GST / year\n"
                  "• Comprehensive (Most Popular) — ₹12,000 + 18% GST / year\n"
                  "• Premium Care (Total Peace of Mind) — ₹26,500 + 18% GST / year\n"
                  "All plans include scheduled preventive visits, genuine spares and "
                  "24×7 breakdown support to keep your lift safe and smooth."),
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


# ---------------------------------------------------------------------------
# Curated Q&A — hand-written answers to (almost) every visitor question.
# Matched by substring on the raw message; the longest matching phrase wins,
# so specific questions beat generic ones. This is the "trained" knowledge
# layer that sits on top of the auto-built product/segment/FAQ index.
# ---------------------------------------------------------------------------
def _plink(slug, label=None):
    prod = next((p for p in content.PRODUCTS if p["slug"] == slug), None)
    lbl = label or (prod["name"].split("—")[0].strip() if prod else slug)
    return {"label": lbl, "endpoint": "product_detail", "kwargs": {"slug": slug}}


_CONTACT_LINK = {"label": "Contact us", "endpoint": "contact", "kwargs": {}}
_CALL_LINK = {"label": "Call now", "url": f"tel:{Config.PHONE.replace(' ', '')}"}
_WA_LINK = {"label": "WhatsApp us", "url": f"https://wa.me/{Config.WHATSAPP}"}
_QUOTE_LINK = {"label": "Get a free quote", "endpoint": "contact", "kwargs": {}}

_QA = [
    # ---- AMC plans & pricing ---------------------------------------------
    {
        "patterns": ["amc price", "amc cost", "amc plan", "amc charge", "amc rate",
                     "annual maintenance", "maintenance contract", "maintenance plan",
                     "maintenance cost", "maintenance price", "service contract", "amc"],
        "reply": ("Our Annual Maintenance Contracts keep your lift safe and smooth. Three "
                  "plans (per lift, per year, + 18% GST):\n"
                  "• Essential (Basic Cover) — ₹8,500\n"
                  "• Comprehensive (Most Popular) — ₹12,000\n"
                  "• Premium Care (Total Peace of Mind) — ₹26,500\n"
                  "All include scheduled preventive visits; Comprehensive & Premium add "
                  "genuine spares and priority 24×7 breakdown support."),
        "links": [{"label": "AMC & Maintenance", "endpoint": "amc", "kwargs": {}}, _CONTACT_LINK],
        "chips": ["Get a quote", "Book AMC", "Contact"],
    },
    # ---- Warranty & guarantees -------------------------------------------
    {
        "patterns": ["warranty", "warrantee", "guarantee", "guaranty", "guarentee"],
        "reply": ("Every Silex elevator comes with a comprehensive manufacturer's "
                  "warranty (typically 12 months from commissioning) covering "
                  "manufacturing defects, along with free service visits during the "
                  "warranty period. You can extend cover afterwards with one of our "
                  "AMC plans."),
        "links": [{"label": "AMC & Maintenance", "endpoint": "amc", "kwargs": {}}, _CONTACT_LINK],
        "chips": ["AMC plans", "Get a quote", "Contact"],
    },
    # ---- Safety features --------------------------------------------------
    {
        "patterns": ["safety feature", "how safe", "is it safe", "safety", "secure",
                     "overspeed", "governor", "interlock", "emergency brake", "fireman"],
        "reply": ("Safety is built into every Silex lift: Automatic Rescue Device (ARD) "
                  "that levels the car to the nearest floor on power failure, overload "
                  "warning, infrared door sensors, emergency alarm & intercom, door "
                  "interlocks, and an overspeed governor with safety gear. Optional "
                  "fireman's/emergency operation is available too."),
        "links": [{"label": "Technology", "endpoint": "technology", "kwargs": {}}, _CONTACT_LINK],
        "chips": ["Power backup (ARD)", "Get a quote", "Contact"],
    },
    # ---- Power backup / ARD / power cut -----------------------------------
    {
        "patterns": ["power backup", "power failure", "power cut", "power goes",
                     "ard", "rescue device", "battery backup", "generator", "load shedding",
                     "electricity goes", "bijli"],
        "reply": ("Yes — our lifts can be fitted with an Automatic Rescue Device (ARD). "
                  "If the mains power fails, the ARD automatically moves the car to the "
                  "nearest floor and opens the doors so no one is ever trapped. It works "
                  "with or without a building generator."),
        "links": [{"label": "Technology", "endpoint": "technology", "kwargs": {}}, _CONTACT_LINK],
        "chips": ["Safety features", "Get a quote", "Contact"],
    },
    # ---- Energy / electricity consumption ---------------------------------
    {
        "patterns": ["energy", "electricity", "power consumption", "units consumed",
                     "efficient", "save power", "save electricity", "running cost",
                     "eco", "green"],
        "reply": ("Silex lifts are engineered to be energy-smart. Our gearless MRL range "
                  "saves up to ~25% electricity versus conventional lifts, and VVVF drives, "
                  "LED cabin lighting and standby/sleep mode cut running costs further. "
                  "Regenerative drive options are available for high-traffic buildings."),
        "links": [_plink("mrl"), {"label": "Technology", "endpoint": "technology", "kwargs": {}}],
        "chips": ["MRL elevators", "Get a quote", "Contact"],
    },
    # ---- Machine room / MRL ----------------------------------------------
    {
        "patterns": ["machine room", "machineroom", "room less", "roomless", "room-less",
                     "need a room", "terrace room", "no machine room", "mrl"],
        "reply": ("Our Machine Room-Less (MRL) elevators mount a compact gearless motor "
                  "inside the shaft, so you don't need a separate machine room on the "
                  "terrace. That reclaims building space, lowers cost and gives a quieter, "
                  "greener ride — perfect for modern homes and towers."),
        "links": [_plink("mrl")],
        "chips": ["Get a quote", "Home lift", "Contact"],
    },
    # ---- Dimensions / space / pit / headroom ------------------------------
    {
        "patterns": ["dimension", "shaft size", "shaft", "pit depth", "pit", "headroom",
                     "head room", "space required", "how much space", "area required",
                     "measurement", "clear opening", "size of lift", "how much area"],
        "reply": ("Exact dimensions depend on the model and capacity, but as a guide: a "
                  "small home lift can fit a shaft from about 1000×1000 mm, pit depths "
                  "typically range 350–1500 mm and headroom 3500–4500 mm. MRL models "
                  "need no machine room. Share your available shaft size and we'll advise "
                  "the best fit — a free site survey confirms everything."),
        "links": [_QUOTE_LINK, {"label": "All products", "endpoint": "products", "kwargs": {}}],
        "chips": ["Book a site survey", "Home lift", "Get a quote"],
    },
    # ---- Speed ------------------------------------------------------------
    {
        "patterns": ["how fast", "speed", "m/s", "meter per second", "metre per second",
                     "fast lift", "how quick"],
        "reply": ("Speeds vary by range: home/hydraulic lifts run around 0.3–0.5 m/s, "
                  "MRL up to 1.0 m/s, and auto-door passenger lifts up to 1.5 m/s. We size "
                  "the drive to your building height for a smooth, quick ride."),
        "links": [{"label": "All products", "endpoint": "products", "kwargs": {}}],
        "chips": ["Capacity", "Get a quote", "Contact"],
    },
    # ---- Capacity / persons / load ----------------------------------------
    {
        "patterns": ["capacity", "how many person", "how many people", "how many passenger",
                     "load", "kg", "weight", "seater", "occupant", "6 person", "8 person",
                     "10 person", "13 person", "tonne", "ton"],
        "reply": ("Passenger ranges carry 6–13 persons (about 408–884 kg). Home lifts can "
                  "start from just 2–3 persons, while goods and industrial lifts handle "
                  "loads from 500 kg up to several tonnes. Custom capacities are available "
                  "on request."),
        "links": [{"label": "All products", "endpoint": "products", "kwargs": {}}, _QUOTE_LINK],
        "chips": ["Which lift suits me?", "Get a quote", "Contact"],
    },
    # ---- Floors / stops / travel ------------------------------------------
    {
        "patterns": ["how many floors", "number of floors", "how many stops", "stops",
                     "travel height", "g+", "storey", "story", "high rise", "highrise",
                     "building height", "floors can"],
        "reply": ("We build lifts for everything from a 2-stop home to high-rise towers. "
                  "Hydraulic suits low-rise (2–5 stops), while MRL and traction passenger "
                  "lifts serve mid- and high-rise buildings. Tell me your number of floors "
                  "and I'll suggest the right range."),
        "links": [{"label": "All products", "endpoint": "products", "kwargs": {}}, _CONTACT_LINK],
        "chips": ["Home lift", "Which lift suits me?", "Get a quote"],
    },
    # ---- Home / residential -----------------------------------------------
    {
        "patterns": ["home lift", "home elevator", "house lift", "residential", "villa",
                     "bungalow", "duplex", "private lift", "domestic lift", "2 person lift",
                     "3 person", "small lift", "compact lift", "for my home", "for home"],
        "reply": ("For homes we recommend our compact MRL or hydraulic lifts — 2–6 "
                  "persons, quiet gearless motion, shallow-pit options and stylish, fully "
                  "customisable cabins. They're space-saving and energy-efficient, ideal "
                  "for villas, bungalows and duplexes."),
        "links": [_plink("mrl"), _plink("hydraulic")],
        "chips": ["Cabin finishes", "Get a quote", "Book a site survey"],
    },
    # ---- Capsule / glass / panoramic --------------------------------------
    {
        "patterns": ["capsule", "glass lift", "glass elevator", "panoramic", "scenic",
                     "see through", "see-through", "transparent lift"],
        "reply": ("Our Capsule and Round Capsule elevators are panoramic glass lifts that "
                  "become a design centrepiece — perfect for malls, hotels, showrooms and "
                  "premium homes. Choose full or half-round glass with LED-lit cabins."),
        "links": [_plink("capsule"), _plink("round-capsule", "Round Capsule")],
        "chips": ["Gallery", "Get a quote", "Contact"],
    },
    # ---- Hospital ---------------------------------------------------------
    {
        "patterns": ["hospital", "stretcher", "patient", "bed lift", "medical", "clinic",
                     "ambulance", "nursing home"],
        "reply": ("Hospital elevators feature extra-wide, deep cabins to take a stretcher "
                  "or bed with attendants, ultra-smooth micro-levelling, anti-bacterial "
                  "finishes and wheelchair-friendly controls for safe patient transfer."),
        "links": [_plink("hospital")],
        "chips": ["Wheelchair access", "Get a quote", "Contact"],
    },
    # ---- Goods / freight --------------------------------------------------
    {
        "patterns": ["goods lift", "goods elevator", "freight", "cargo", "material lift",
                     "heavy load", "pallet"],
        "reply": ("Goods elevators are heavy-duty lifts built to move stock, pallets and "
                  "materials reliably — rugged cabins, wide loading doors and capacities "
                  "from 500 kg to several tonnes."),
        "links": [_plink("goods")],
        "chips": ["Industrial lift", "Get a quote", "Contact"],
    },
    # ---- Industrial -------------------------------------------------------
    {
        "patterns": ["industrial", "factory lift", "warehouse", "plant lift", "godown"],
        "reply": ("Our Industrial elevators are engineered for factories and warehouses — "
                  "high load capacities, robust construction and multi-level shaft designs "
                  "for demanding environments."),
        "links": [_plink("industrial")],
        "chips": ["Goods lift", "Get a quote", "Contact"],
    },
    # ---- Car parking ------------------------------------------------------
    {
        "patterns": ["car lift", "car elevator", "parking", "vehicle lift", "car parking"],
        "reply": ("Car parking lifts move vehicles between levels safely and space-"
                  "efficiently — ideal for showrooms, basements and multi-level parking."),
        "links": [_plink("car-parking", "Car Parking")],
        "chips": ["Get a quote", "Contact", "All products"],
    },
    # ---- Hydraulic --------------------------------------------------------
    {
        "patterns": ["hydraulic", "hydrolic", "hydrolics", "oil lift"],
        "reply": ("Hydraulic elevators are perfect for low-rise buildings (2–5 stops). "
                  "They need only a shallow pit and no overhead machine room, making them "
                  "a great, cost-effective choice for homes, villas and small commercial "
                  "buildings."),
        "links": [_plink("hydraulic")],
        "chips": ["Home lift", "Get a quote", "Contact"],
    },
    # ---- Cabin finishes / interior ----------------------------------------
    {
        "patterns": ["cabin finish", "finish", "interior", "colour", "color", "cabin design",
                     "stainless", "mirror", "wooden", "false ceiling", "flooring",
                     "customize", "customise", "custom cabin", "look of"],
        "reply": ("Cabins are fully customisable: hairline/mirror/gold stainless steel, "
                  "glass, wood-look laminates, designer LED false ceilings and premium "
                  "flooring. Explore finishes in our 360° Virtual Showroom and Gallery, or "
                  "share your theme and we'll match it."),
        "links": [{"label": "Gallery", "endpoint": "gallery", "kwargs": {}}, _CONTACT_LINK],
        "chips": ["Virtual Showroom", "Get a quote", "Contact"],
    },
    # ---- Doors ------------------------------------------------------------
    {
        "patterns": ["door type", "auto door", "manual door", "telescopic", "centre opening",
                     "center opening", "collapsible door", "which door", "door option",
                     "swing door"],
        "reply": ("Choose from automatic doors (centre-opening or telescopic side-opening) "
                  "with infrared safety sensors, or manual swing/collapsible doors in MS, "
                  "stainless steel or glass. We use trusted door gear from Fermator and "
                  "Wittur."),
        "links": [_plink("passenger-auto", "Auto-Door Passenger"), _plink("passenger-manual", "Manual-Door Passenger")],
        "chips": ["Get a quote", "All products", "Contact"],
    },
    # ---- Brands / components ----------------------------------------------
    {
        "patterns": ["brand", "component", "montanari", "wittur", "fermator", "yaskawa",
                     "which parts", "made of", "imported part", "spare brand"],
        "reply": ("Silex lifts are built with world-class components — Montanari, Wittur, "
                  "Fermator and Yaskawa among others — combined with in-house R&D and "
                  "computer-aided design for reliability and a silky ride."),
        "links": [{"label": "Technology", "endpoint": "technology", "kwargs": {}},
                  {"label": "Why Silex", "endpoint": "why_us", "kwargs": {}}],
        "chips": ["Why choose Silex?", "Get a quote", "Contact"],
    },
    # ---- Delivery / lead time / installation time -------------------------
    {
        "patterns": ["how long", "lead time", "delivery time", "delivery", "time to install",
                     "installation time", "how many days", "how many weeks", "duration",
                     "timeline", "when can you", "kitna time", "ready by", "install in"],
        "reply": ("Typical timelines are about 4–8 weeks from order confirmation and shaft "
                  "readiness, depending on the model, number of floors and finishes. We "
                  "start with a free site survey, then manufacture and install with our "
                  "own trained engineers."),
        "links": [_QUOTE_LINK, _CALL_LINK],
        "chips": ["Book a site survey", "Get a quote", "Contact"],
    },
    # ---- Payment / GST / EMI ----------------------------------------------
    {
        "patterns": ["payment", "gst", "tax", "emi", "installment", "instalment", "finance",
                     "advance", "payment term", "how to pay", "pay in", "down payment"],
        "reply": ("Quotes are transparent and itemised. GST is charged at 18% as "
                  "applicable. Payments are milestone-based — an advance to start, stages "
                  "during manufacturing/installation and a balance on commissioning. Talk "
                  "to our team for exact terms for your project."),
        "links": [_CONTACT_LINK, _CALL_LINK],
        "chips": ["Get a quote", "AMC plans", "Contact"],
    },
    # ---- Site survey / free quote / appointment ---------------------------
    {
        "patterns": ["site survey", "survey", "site visit", "inspection", "come to",
                     "book appointment", "appointment", "schedule a", "meeting", "demo",
                     "visit us", "free estimate", "free quote", "estimate"],
        "reply": ("Absolutely — we offer a free, no-obligation site survey and quotation. "
                  "Our engineer assesses your building, traffic and shaft, then prepares a "
                  "tailored recommendation, usually within 1–2 working days."),
        "links": [_QUOTE_LINK, _CALL_LINK, _WA_LINK],
        "chips": ["Get a quote", "Call us", "Contact"],
    },
    # ---- Working hours / timings ------------------------------------------
    {
        "patterns": ["working hour", "office hour", "timing", "what time", "open time",
                     "are you open", "opening hour", "business hour", "kab khula",
                     "monday", "sunday", "holiday"],
        "reply": ("Our office is open Monday to Saturday, 9:30 am – 6:30 pm. AMC customers "
                  "also get a 24×7 emergency breakdown helpline, so help is always a call "
                  "away."),
        "links": [_CONTACT_LINK, _CALL_LINK],
        "chips": ["Contact", "Emergency help", "Get a quote"],
    },
    # ---- Emergency / breakdown / stuck ------------------------------------
    {
        "patterns": ["emergency", "breakdown", "break down", "stuck", "trapped", "not working",
                     "lift stopped", "lift stuck", "urgent", "complaint", "complain",
                     "problem with", "lift down", "out of order"],
        "reply": (f"For any breakdown or emergency, call our helpline right away at "
                  f"{Config.EMERGENCY_PHONE}. AMC customers get priority 24×7 response and "
                  f"our engineer will assist immediately. If anyone is inside, stay calm — "
                  f"the doors stay safely shut until we reach the car."),
        "links": [_CALL_LINK, _CONTACT_LINK],
        "chips": ["AMC plans", "Call now", "Contact"],
    },
    # ---- Spare parts ------------------------------------------------------
    {
        "patterns": ["spare part", "spares", "spare", "replacement part", "parts available",
                     "availability of part"],
        "reply": ("We stock genuine spare parts and supply them promptly — included under "
                  "Comprehensive/Premium AMC cover, or available on demand. Using original "
                  "parts keeps your lift safe and under warranty."),
        "links": [{"label": "AMC & Maintenance", "endpoint": "amc", "kwargs": {}}, _CONTACT_LINK],
        "chips": ["AMC plans", "Get a quote", "Contact"],
    },
    # ---- Maintenance frequency --------------------------------------------
    {
        "patterns": ["how often", "maintenance schedule", "service frequency", "how many visits",
                     "monthly service", "preventive", "service interval"],
        "reply": ("Under our AMC we carry out scheduled preventive visits (typically "
                  "monthly, or as per your plan) plus 24×7 breakdown support — lubrication, "
                  "safety checks, adjustments and genuine spares to keep the ride smooth."),
        "links": [{"label": "AMC & Maintenance", "endpoint": "amc", "kwargs": {}}],
        "chips": ["AMC plans", "Get a quote", "Contact"],
    },
    # ---- Export / countries -----------------------------------------------
    {
        "patterns": ["export", "which countries", "countries", "international", "abroad",
                     "overseas", "outside india", "global"],
        "reply": ("Yes — proudly engineered in India, Silex exports to 10+ countries while "
                  "serving 20+ cities at home. Tell us your location and we'll guide you on "
                  "supply and installation."),
        "links": [{"label": "About us", "endpoint": "about", "kwargs": {}}, _CONTACT_LINK],
        "chips": ["Get a quote", "Contact", "Products"],
    },
    # ---- Cities / branches / coverage -------------------------------------
    {
        "patterns": ["which city", "which cities", "branch", "branches", "do you serve",
                     "service area", "near me", "available in", "do you cover", "cover my",
                     "which area", "serve in"],
        "reply": ("Our head office is in Surat, and we serve 20+ cities across India with "
                  "branch presence in Surat, Vadodara, Bhavnagar, Panoli and Navapur. Share "
                  "your city and we'll connect you with the nearest team."),
        "links": [_CONTACT_LINK],
        "chips": ["Get a quote", "Call us", "Contact"],
    },
    # ---- Recommendation / which lift --------------------------------------
    {
        "patterns": ["which lift", "which elevator", "recommend", "suggest", "suitable",
                     "best lift", "what should i", "help me choose", "which one", "confused",
                     "need a lift for", "what do you suggest"],
        "reply": ("Happy to help you choose! As a quick guide:\n"
                  "• Home/villa → compact MRL or Hydraulic\n"
                  "• Apartment/office → Auto-door Passenger (MRL)\n"
                  "• Hospital → Hospital/stretcher lift\n"
                  "• Mall/hotel/showroom → Capsule (panoramic)\n"
                  "• Factory/warehouse → Goods or Industrial\n"
                  "Tell me your building type and floors and I'll narrow it down."),
        "links": [{"label": "All products", "endpoint": "products", "kwargs": {}}, _QUOTE_LINK],
        "chips": ["Home lift", "Capsule lift", "Get a quote"],
    },
    # ---- Why Silex / advantages -------------------------------------------
    {
        "patterns": ["why silex", "why choose", "why you", "advantage", "benefit",
                     "what makes", "different", "usp", "better than", "why should"],
        "reply": ("Why Silex? We're ISO 9001:2008 certified with in-house R&D, two "
                  "well-developed factories, world-class components and computer-aided "
                  "design — delivering silky motion at an affordable cost. Add 20+ cities, "
                  "10+ export countries and strong after-sales AMC support, and you get a "
                  "partner you can trust to the top."),
        "links": [{"label": "Why Silex", "endpoint": "why_us", "kwargs": {}},
                  {"label": "About us", "endpoint": "about", "kwargs": {}}],
        "chips": ["Products", "Get a quote", "Contact"],
    },
    # ---- Owner / founder / directors --------------------------------------
    {
        "patterns": ["owner", "founder", "director", "ceo", "who is behind", "proprietor",
                     "promoter", "who runs", "who owns", "managing director"],
        "reply": (f"Silex Elevators is led by {Config.CONTACT_PERSON} and "
                  f"{Config.CONTACT_PERSON_ALT}. You're welcome to reach them directly "
                  f"through our contact page or on WhatsApp."),
        "links": [_CONTACT_LINK, _WA_LINK],
        "chips": ["About us", "Contact", "Get a quote"],
    },
    # ---- Virtual showroom / 360 -------------------------------------------
    {
        "patterns": ["virtual showroom", "360", "showroom", "virtual tour", "view cabins",
                     "see cabins", "3d tour"],
        "reply": ("Explore our cabins in the 360° Virtual Showroom — tap the "
                  "\"Virtual Showroom\" button just below the header on any page. You can "
                  "also browse real installations in our Gallery."),
        "links": [{"label": "Gallery", "endpoint": "gallery", "kwargs": {}}],
        "chips": ["Gallery", "Get a quote", "Contact"],
    },
    # ---- Noise / smoothness -----------------------------------------------
    {
        "patterns": ["noise", "noisy", "sound", "silent", "quiet", "vibration", "jerk",
                     "smooth ride", "smooth"],
        "reply": ("Silex lifts are famously smooth and quiet. Permanent-magnet gearless "
                  "machines, VVVF drives and micro-levelling deliver a silky, jerk-free "
                  "ride with very low noise and vibration."),
        "links": [_plink("mrl")],
        "chips": ["MRL elevators", "Get a quote", "Contact"],
    },
    # ---- Wheelchair / accessibility ---------------------------------------
    {
        "patterns": ["wheelchair", "disabled", "handicap", "accessibility", "accessible",
                     "divyang", "differently abled", "braille", "voice announcement"],
        "reply": ("Yes — we build fully accessible lifts with braille/tactile buttons, "
                  "handrails, wide clear-opening doors, audio-visual floor announcements "
                  "and wheelchair-friendly cabin sizes, meeting universal-access needs."),
        "links": [_plink("hospital"), _CONTACT_LINK],
        "chips": ["Hospital lift", "Get a quote", "Contact"],
    },
    # ---- Certification / quality / standards ------------------------------
    {
        "patterns": ["iso", "certification", "certified", "quality standard", "standard",
                     "is 14665", "compliance", "certificate"],
        "reply": ("Silex is ISO 9001:2008 certified, with quality assured across design, "
                  "manufacturing and service. Our elevators are built to Indian elevator "
                  "safety standards (IS 14665) using world-class components."),
        "links": [{"label": "About us", "endpoint": "about", "kwargs": {}},
                  {"label": "Why Silex", "endpoint": "why_us", "kwargs": {}}],
        "chips": ["Why choose Silex?", "Get a quote", "Contact"],
    },
    # ---- Contact details (phone / email / whatsapp / address) -------------
    {
        "patterns": ["phone number", "contact number", "mobile number", "your number",
                     "call you", "email id", "email address", "your email", "gmail",
                     "whatsapp number", "whatsapp", "your address", "office address",
                     "where are you located", "where is your office", "directions", "map",
                     "reach you", "get in touch", "how to contact"],
        "reply": (f"Here's how to reach Silex Elevators:\n"
                  f"📞 {Config.PHONE} / {Config.PHONE_ALT}\n"
                  f"💬 WhatsApp: {Config.PHONE}\n"
                  f"✉️ {Config.EMAIL}\n"
                  f"📍 {Config.ADDRESS}\n"
                  f"We'd love to hear from you!"),
        "links": [_CALL_LINK, _WA_LINK, _CONTACT_LINK],
        "chips": ["Call now", "WhatsApp", "Get a quote"],
    },
    # ---- Talk to a human / callback ---------------------------------------
    {
        "patterns": ["talk to human", "talk to a human", "talk to a person", "real person",
                     "speak to someone", "speak to a", "call me back", "callback",
                     "call back", "someone call me", "human agent", "human", "sales team",
                     "representative", "connect me", "agent"],
        "reply": (f"Of course — our team is happy to help personally. Call us at "
                  f"{Config.PHONE}, message us on WhatsApp, or drop your details on the "
                  f"contact page and we'll call you back shortly."),
        "links": [_CALL_LINK, _WA_LINK, _CONTACT_LINK],
        "chips": ["Call now", "WhatsApp", "Contact"],
    },
    # ---- Company experience / since when / how many installs --------------
    {
        "patterns": ["how long have you", "since when", "established", "how old is",
                     "years of experience", "experience", "how many installation",
                     "how many lift", "track record", "when did you start", "founded in"],
        "reply": ("Silex is an established, ISO-certified elevator manufacturer with a "
                  "strong track record across 20+ cities in India and exports to 10+ "
                  "countries, backed by in-house R&D and two manufacturing facilities. "
                  "Ask us for reference installations near you."),
        "links": [{"label": "Projects", "endpoint": "projects", "kwargs": {}},
                  {"label": "About us", "endpoint": "about", "kwargs": {}}],
        "chips": ["Our projects", "Why choose Silex?", "Contact"],
    },
    # ---- Reviews / testimonials / clients / references --------------------
    {
        "patterns": ["review", "testimonial", "feedback", "clients", "customer", "reference",
                     "who are your client", "past project", "completed project", "portfolio",
                     "rating", "trustworthy", "reliable"],
        "reply": ("We're proud of our happy customers across homes, hospitals, hotels, "
                  "malls and factories. Browse real installations in our Projects and "
                  "Gallery, and we'll gladly share reference sites near you on request."),
        "links": [{"label": "Projects", "endpoint": "projects", "kwargs": {}},
                  {"label": "Gallery", "endpoint": "gallery", "kwargs": {}}],
        "chips": ["Our projects", "Gallery", "Contact"],
    },
    # ---- Buying process / how to order ------------------------------------
    {
        "patterns": ["how to order", "how do i buy", "buying process", "how to buy",
                     "process to", "steps to", "how to get one", "how to purchase",
                     "what is the process", "next step", "how to proceed", "how to book"],
        "reply": ("It's simple: 1) Share your requirement or book a free site survey, "
                  "2) We assess the building and recommend the right lift, 3) You get a "
                  "transparent quotation, 4) On confirmation we manufacture, install and "
                  "commission with our own engineers, 5) Ongoing AMC support. Shall we "
                  "start with a free survey?"),
        "links": [_QUOTE_LINK, _CALL_LINK],
        "chips": ["Book a site survey", "Get a quote", "Contact"],
    },
    # ---- Approximate price / budget / cheapest ----------------------------
    {
        "patterns": ["approximate cost", "approximate price", "rough cost", "rough price",
                     "price range", "starting price", "budget", "cheapest", "lowest price",
                     "how much does a lift cost", "how much is a lift", "how much for a lift",
                     "minimum cost", "affordable", "economical"],
        "reply": ("Every Silex lift is custom-built, so the price depends on the type, "
                  "capacity, number of floors, doors and cabin finish. We keep options for "
                  "every budget and give a clear, itemised quote after a quick (free) site "
                  "survey. Tell me your building type and floors for a tailored estimate."),
        "links": [_QUOTE_LINK, {"label": "All products", "endpoint": "products", "kwargs": {}}],
        "chips": ["Book a site survey", "Which lift suits me?", "Contact"],
    },
    # ---- Discount / offer -------------------------------------------------
    {
        "patterns": ["discount", "offer", "deal", "scheme", "best price", "any offer",
                     "reduce price", "negotiable", "lower the price"],
        "reply": ("We always aim for the best value for money. For current offers, bulk or "
                  "builder pricing, please share your requirement — our team will give you "
                  "the sharpest quote we can."),
        "links": [_QUOTE_LINK, _CALL_LINK],
        "chips": ["Get a quote", "Call now", "Contact"],
    },
    # ---- Service / AMC for other brand lifts ------------------------------
    {
        "patterns": ["other brand", "existing lift", "another company", "other company lift",
                     "not silex", "otis lift", "kone lift", "different brand", "take over",
                     "service my lift", "maintain my existing", "amc for existing"],
        "reply": ("Yes — in most cases we can inspect and take over the maintenance of your "
                  "existing lift regardless of the original brand. Our engineer will assess "
                  "it and suggest a suitable AMC plan or upgrades."),
        "links": [{"label": "AMC & Maintenance", "endpoint": "amc", "kwargs": {}}, _CONTACT_LINK],
        "chips": ["AMC plans", "Book a survey", "Contact"],
    },
    # ---- Competitor comparison --------------------------------------------
    {
        "patterns": ["otis", "kone", "schindler", "johnson", "compare with", "better than",
                     "vs ", "versus", "how do you compare", "than other"],
        "reply": ("We focus on delivering world-class components (Montanari, Wittur, "
                  "Fermator, Yaskawa), silky-smooth motion and strong local service — at a "
                  "genuinely affordable cost. Many customers choose Silex for that mix of "
                  "quality, personal support and value. Happy to arrange a demo or "
                  "reference site so you can judge for yourself."),
        "links": [{"label": "Why Silex", "endpoint": "why_us", "kwargs": {}},
                  {"label": "Technology", "endpoint": "technology", "kwargs": {}}],
        "chips": ["Why choose Silex?", "Get a quote", "Contact"],
    },
    # ---- Modernization / upgrade old lift ---------------------------------
    {
        "patterns": ["modernization", "modernisation", "upgrade", "old lift", "replace lift",
                     "renovate lift", "retrofit", "revamp", "outdated lift", "improve my lift"],
        "reply": ("Our modernization service breathes new life into ageing lifts — new "
                  "controllers, gearless machines, VVVF drives, doors, cabins and safety "
                  "upgrades — improving safety, ride quality and energy use without a full "
                  "rebuild. We assess and upgrade lifts of most brands."),
        "links": [{"label": "Modernization", "endpoint": "modernization", "kwargs": {}}, _CONTACT_LINK],
        "chips": ["Book a survey", "Get a quote", "Contact"],
    },
    # ---- Civil work / shaft / structure -----------------------------------
    {
        "patterns": ["civil work", "who builds the shaft", "build the shaft", "structure",
                     "do you do civil", "masonry", "shaft construction", "need to build",
                     "structural work", "steel structure", "do i need a shaft", "make the shaft"],
        "reply": ("You typically provide the lift shaft/well as per our drawings, and we "
                  "supply, install and commission the complete elevator. If you don't have "
                  "a masonry shaft, we can supply an elegant structural steel-and-glass "
                  "shaft too. We share exact civil requirements after the site survey."),
        "links": [_QUOTE_LINK, {"label": "All products", "endpoint": "products", "kwargs": {}}],
        "chips": ["Book a site survey", "Dimensions", "Contact"],
    },
    # ---- Pit-less / low pit -----------------------------------------------
    {
        "patterns": ["pit less", "pitless", "pit-less", "no pit", "low pit", "shallow pit",
                     "without pit", "minimum pit", "low headroom", "low ceiling"],
        "reply": ("Yes — we offer low-pit and reduced-headroom solutions (and hydraulic "
                  "home lifts that need only a shallow pit), ideal for retrofits and homes "
                  "with limited civil space. Share your available pit/headroom and we'll "
                  "recommend the best model."),
        "links": [_plink("hydraulic"), _plink("mrl")],
        "chips": ["Home lift", "Dimensions", "Get a quote"],
    },
    # ---- Traction vs hydraulic / geared vs gearless -----------------------
    {
        "patterns": ["traction vs", "hydraulic vs", "difference between", "geared", "gearless",
                     "traction or hydraulic", "which technology", "counterweight", "rope lift"],
        "reply": ("Quick guide: Gearless traction (MRL) lifts are smooth, efficient and "
                  "great for low- to high-rise — no machine room needed. Hydraulic lifts "
                  "are cost-effective for low-rise (2–5 stops), need only a shallow pit and "
                  "no overhead room. Tell me your floors and I'll suggest the right one."),
        "links": [_plink("mrl"), _plink("hydraulic")],
        "chips": ["Which lift suits me?", "Get a quote", "Contact"],
    },
    # ---- Auto vs manual door ----------------------------------------------
    {
        "patterns": ["auto vs manual", "auto or manual", "automatic or manual",
                     "manual or automatic", "manual or auto", "difference between auto",
                     "auto door or manual", "which door is better"],
        "reply": ("Automatic doors open and close on their own with safety sensors — "
                  "convenient, premium and hands-free (great for hospitals, offices, homes). "
                  "Manual (swing/collapsible) doors cost less and suit budget or industrial "
                  "use. We'll help you pick based on usage and budget."),
        "links": [_plink("passenger-auto", "Auto-Door Passenger"), _plink("passenger-manual", "Manual-Door Passenger")],
        "chips": ["Get a quote", "Products", "Contact"],
    },
    # ---- Dumbwaiter / kitchen / small goods lift --------------------------
    {
        "patterns": ["dumbwaiter", "dumb waiter", "kitchen lift", "food lift", "small goods lift",
                     "restaurant lift", "service lift", "mini lift"],
        "reply": ("Yes — we make compact dumbwaiter / kitchen (service) lifts to move food, "
                  "documents or small goods between floors in restaurants, hotels, homes "
                  "and offices. Tell us the load and floors and we'll size one for you."),
        "links": [_plink("goods"), _CONTACT_LINK],
        "chips": ["Get a quote", "Goods lift", "Contact"],
    },
    # ---- Fireman / fire-rated ---------------------------------------------
    {
        "patterns": ["fireman", "fireman lift", "fireman's lift", "fire lift", "fire rated",
                     "fire fighting", "fire operation", "fire emergency lift", "firefighter",
                     "fire safety lift"],
        "reply": ("We provide fireman's / emergency operation and fire-rated lift options "
                  "that comply with fire-safety requirements — the lift returns to the "
                  "designated floor and switches to firefighter control during an alarm. "
                  "We'll configure it to your building's fire NOC needs."),
        "links": [{"label": "Technology", "endpoint": "technology", "kwargs": {}}, _CONTACT_LINK],
        "chips": ["Safety features", "Get a quote", "Contact"],
    },
    # ---- Outdoor / weatherproof -------------------------------------------
    {
        "patterns": ["outdoor lift", "outside lift", "weatherproof", "weather proof",
                     "open area", "external lift", "rain proof", "exterior elevator"],
        "reply": ("Yes — we build outdoor/external lifts with weather-resistant finishes, "
                  "sealed cabins and protected components, ideal for building exteriors, "
                  "resorts and industrial yards. Share the location and exposure and we'll "
                  "spec it accordingly."),
        "links": [_plink("capsule"), _CONTACT_LINK],
        "chips": ["Get a quote", "Capsule lift", "Contact"],
    },
    # ---- Smart / IoT / remote monitoring ----------------------------------
    {
        "patterns": ["smart lift", "iot", "remote monitoring", "mobile app", "app control",
                     "internet", "connected lift", "digital", "predictive"],
        "reply": ("Our modern controllers support smart features like remote diagnostics "
                  "and condition monitoring, so issues can be spotted early and downtime "
                  "reduced. Ask us about smart/connected options for your project."),
        "links": [{"label": "Technology", "endpoint": "technology", "kwargs": {}}, _CONTACT_LINK],
        "chips": ["Technology", "Get a quote", "Contact"],
    },
    # ---- Touchless / hygiene ----------------------------------------------
    {
        "patterns": ["touchless", "touch less", "hygiene", "antimicrobial", "anti bacterial",
                     "sanitiz", "covid", "contactless", "foot operated", "no touch"],
        "reply": ("We offer hygienic options like touchless/gesture or foot-operated "
                  "buttons, antimicrobial surfaces and UV/air-purifier add-ons for a "
                  "safer, cleaner ride — popular for hospitals and high-traffic buildings."),
        "links": [_plink("hospital"), _CONTACT_LINK],
        "chips": ["Hospital lift", "Get a quote", "Contact"],
    },
    # ---- Government approval / license / statutory ------------------------
    {
        "patterns": ["government approval", "license", "licence", "inspector", "statutory",
                     "lift act", "registration", "legal", "permit", "noc", "approval",
                     "load test", "inspection certificate", "pwd"],
        "reply": ("We build to Indian elevator safety standards (IS 14665) and assist with "
                  "the statutory paperwork — load testing, inspection and the licensing/"
                  "registration required in your state — so your lift is fully compliant "
                  "before handover."),
        "links": [_CONTACT_LINK, {"label": "About us", "endpoint": "about", "kwargs": {}}],
        "chips": ["Safety features", "Get a quote", "Contact"],
    },
    # ---- Earthquake / seismic ---------------------------------------------
    {
        "patterns": ["earthquake", "seismic", "tremor", "quake"],
        "reply": ("Our controllers can include a seismic/earthquake operation that safely "
                  "brings the car to the nearest floor and holds it during tremors. We "
                  "configure this for seismic-zone buildings on request."),
        "links": [{"label": "Technology", "endpoint": "technology", "kwargs": {}}, _CONTACT_LINK],
        "chips": ["Safety features", "Get a quote", "Contact"],
    },
    # ---- Dealer / franchise / partnership ---------------------------------
    {
        "patterns": ["dealer", "franchise", "partnership", "become a partner", "distributor",
                     "reseller", "channel partner", "business opportunity", "tie up",
                     "builder tie", "architect"],
        "reply": ("We're always keen to work with builders, architects and channel "
                  "partners. Share your details on the contact page or call us, and our "
                  "team will discuss partnership, project and bulk-supply opportunities."),
        "links": [_CONTACT_LINK, _CALL_LINK],
        "chips": ["Contact", "Call now", "About us"],
    },
    # ---- Warranty extension / AMC after warranty --------------------------
    {
        "patterns": ["extend warranty", "warranty extension", "after warranty", "extended cover",
                     "warranty over", "warranty finished"],
        "reply": ("Once the standard warranty ends, keep full protection with one of our "
                  "AMC plans — preventive visits, genuine spares and priority breakdown "
                  "support. It's the best way to protect your investment long-term."),
        "links": [{"label": "AMC & Maintenance", "endpoint": "amc", "kwargs": {}}, _CONTACT_LINK],
        "chips": ["AMC plans", "Get a quote", "Contact"],
    },
    # ---- Elderly / stair / platform lift ----------------------------------
    {
        "patterns": ["elderly", "senior citizen", "old parent", "stair lift", "stairlift",
                     "platform lift", "for grandparent", "aged", "mobility"],
        "reply": ("For elderly or reduced-mobility users we recommend a quiet, easy-access "
                  "home lift (compact MRL or hydraulic) with wide doors, handrails, a seat "
                  "option and braille controls. We'll tailor it for comfort and safety."),
        "links": [_plink("hydraulic"), _plink("mrl")],
        "chips": ["Home lift", "Wheelchair access", "Get a quote"],
    },
]


def _match_qa(raw_lower):
    """Return the curated Q&A entry whose longest phrase matches the message."""
    best, best_len = None, 0
    for entry in _QA:
        for pat in entry["patterns"]:
            if pat in raw_lower and len(pat) > best_len:
                best, best_len = entry, len(pat)
    if best:
        return {"reply": best["reply"], "links": best["links"], "chips": best["chips"]}
    return None


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
    raw_lower = raw.lower()

    # Exact greeting / thanks first, then curated Q&A, then keyword intents.
    if raw.strip().lower() in {"hi", "hii", "hey", "hello", "helo", "yo", "hola",
                               "namaste", "good morning", "good evening",
                               "good afternoon", "start", "menu"}:
        return _greeting()

    qa = _match_qa(raw_lower)
    if qa:
        return qa

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
