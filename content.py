"""All static site content for Silex Elevator.

Keeping copy here (instead of hard-coded in templates) makes it easy to hand
the client a single file to review or edit later, and keeps templates clean.

Product & section imagery is served from the Unsplash CDN (curated real
elevator / lift photography) so the whole site is fully data-driven — swap a
single URL here to change a picture everywhere it appears.
"""


def _img(pid, w=1600):
    """Build a curated Unsplash CDN image URL from a photo id."""
    return (
        "https://images.unsplash.com/photo-"
        f"{pid}?auto=format&fit=crop&w={w}&q=80"
    )


# ---------------------------------------------------------------------------
# Curated photography (real lift / elevator imagery, Unsplash CDN)
# ---------------------------------------------------------------------------
# One id per product slug — matched to what each product actually is.
PRODUCT_PHOTOS = {
    "mrl":              _img("1525273177952-67455d25871f"),  # clean minimalist lobby
    "passenger-auto":   _img("1758448721149-aa0ce8e1b2c9"),  # office lift lobby
    "passenger-manual": _img("1785005670379-88abacb8a6cf"),  # simple twin lift doors
    "capsule":          _img("1564771752795-1f9c48984c44"),  # glowing glass atrium lifts
    "round-capsule":    _img("1774801890542-c875dab300ea"),  # panoramic glass capsule
    "hospital":         _img("1764213077578-eab0ab29f949"),  # accessible lift, red doors
    "goods":            _img("1595392312388-38d093a975e3"),  # industrial goods hoist
    "car-parking":      _img("1556537696-dc5627064044"),     # multi-level industrial shaft
    "hydraulic":        _img("1709942772983-e8e9c04ad50b"),  # hydraulic machinery
}

# Site-wide section imagery.
MEDIA = {
    "hero":          _img("1564771789713-8586b829cbeb", 2000),  # night glass lifts
    "about":         _img("1735178181188-855a87e83dca"),        # warm gold lift doors
    "cabin":         _img("1774294925489-68f75e2b3b05"),        # modern empty cabin
    "doors":         _img("1665285255745-f1d9453d109c"),        # ornate luxury doors
    "components":    _img("1709942772983-e8e9c04ad50b"),        # lift machinery
    "technology":    _img("1595601265373-612a09303582"),        # futuristic glass shaft
    "modernization": _img("1746702475459-89ff401cafd8"),        # warm wood cabin interior
}

# Virtual showroom — cabin finishes & designs (horizontal gallery on Home).
SHOWROOM = [
    {
        "name": "Panoramic Glass Capsule",
        "tag": "Signature",
        "note": "360° glass cabin that turns every ride into a landmark view.",
        "photo": _img("1564771752795-1f9c48984c44"),
    },
    {
        "name": "Titanium Gold Mirror",
        "tag": "Luxury",
        "note": "Warm gold-mirror walls for hotels, malls and flagship lobbies.",
        "photo": _img("1735178181188-855a87e83dca"),
    },
    {
        "name": "Brushed Steel Cabin",
        "tag": "Modern",
        "note": "Clean hairline stainless that hides fingerprints in busy towers.",
        "photo": _img("1774294925489-68f75e2b3b05"),
    },
    {
        "name": "Ornate Heritage Doors",
        "tag": "Bespoke",
        "note": "Detailed metalwork landing doors for premium residences.",
        "photo": _img("1665285255745-f1d9453d109c"),
    },
    {
        "name": "Night Glass Atrium",
        "tag": "Statement",
        "note": "Backlit panoramic lifts that glow across a building at night.",
        "photo": _img("1564771789713-8586b829cbeb"),
    },
    {
        "name": "Minimalist Lobby Line",
        "tag": "Residential",
        "note": "Understated finishes engineered for quiet homes and villas.",
        "photo": _img("1525273177952-67455d25871f"),
    },
]

# Virtual showroom SCENES — the same lifts placed in real environments.
# Powers the circular "step inside" 360° gallery room on the Home page.
SHOWROOM_SCENES = [
    {
        "place": "Luxury Hotel",
        "lift": "Titanium Gold Capsule",
        "note": "Warm gold-mirror cabins that make a five-star lobby feel even grander.",
        "photo": _img("1735178181188-855a87e83dca", 1800),
    },
    {
        "place": "Private Villa",
        "lift": "Home Elevator",
        "note": "A whisper-quiet minimalist lift that blends into modern living spaces.",
        "photo": _img("1525273177952-67455d25871f", 1800),
    },
    {
        "place": "Hospital",
        "lift": "Bed & Stretcher Lift",
        "note": "Wide, smooth-stopping cabins built for beds, wheelchairs and quick care.",
        "photo": _img("1764213077578-eab0ab29f949", 1800),
    },
    {
        "place": "Shopping Mall",
        "lift": "Panoramic Glass Capsule",
        "note": "360° glass rides that turn footfall into a landmark experience.",
        "photo": _img("1564771752795-1f9c48984c44", 1800),
    },
    {
        "place": "Corporate Office",
        "lift": "Passenger Auto-Door",
        "note": "High-traffic lifts with fast, level stops for busy business towers.",
        "photo": _img("1758448721149-aa0ce8e1b2c9", 1800),
    },
    {
        "place": "Industrial Plant",
        "lift": "Goods & Freight Lift",
        "note": "Heavy-duty platforms that move tonnes between factory floors safely.",
        "photo": _img("1595392312388-38d093a975e3", 1800),
    },
    {
        "place": "Skyline Tower",
        "lift": "Night Glass Atrium",
        "note": "Backlit panoramic lifts that glow across a skyline after dark.",
        "photo": _img("1564771789713-8586b829cbeb", 1800),
    },
    {
        "place": "Heritage Residence",
        "lift": "Ornate Bespoke Lift",
        "note": "Hand-detailed metalwork doors crafted for premium heritage homes.",
        "photo": _img("1665285255745-f1d9453d109c", 1800),
    },
]

# ---------------------------------------------------------------------------
# Headline stats (shown on Home + About)
# ---------------------------------------------------------------------------
STATS = [
    {"value": "20+", "label": "Cities Served Across India"},
    {"value": "9", "label": "Elevator Product Lines"},
    {"value": "10+", "label": "Countries in Global Network"},
    {"value": "ISO", "label": "9001:2008 Certified"},
]

# ---------------------------------------------------------------------------
# Product catalogue (from brochure pages 2-8)
# ---------------------------------------------------------------------------
PRODUCTS = [
    {
        "slug": "mrl",
        "name": "Machine Room-Less (MRL) Elevators",
        "short": "Gearless, energy-smart lifts that need no dedicated machine room.",
        "capacity": "6 – 13 Passengers",
        "speed": "Up to 1.0 m/s",
        "icon": "mrl",
        "tag": "Most Efficient",
        "highlights": [
            "Saves up to 25% electricity vs. conventional lifts",
            "Reclaims ~10% of construction area",
            "28% reduction in required equipment area",
            "Permanent-magnet gearless traction machine",
        ],
        "description": (
            "Our flagship Machine Room-Less range removes the need for a separate "
            "machine room by mounting a compact gearless motor inside the shaft. "
            "The result is a quieter, greener ride that frees up valuable rooftop "
            "and building space — ideal for modern residential towers and "
            "commercial complexes."
        ),
    },
    {
        "slug": "passenger-auto",
        "name": "Passenger Elevators — Auto Doors",
        "short": "Smooth, high-speed automatic-door lifts for apartments and offices.",
        "capacity": "6 – 13 Passengers",
        "speed": "Up to 1.5 m/s",
        "icon": "passenger",
        "tag": "Best Seller",
        "highlights": [
            "Auto centre-opening doors with safety sensors",
            "VVVF drive for silky acceleration",
            "Speeds up to 1.5 m/s",
            "Wide range of cabin finishes",
        ],
        "description": (
            "Automatic-door passenger elevators combine comfort, safety and speed. "
            "Infrared door sensors, micro-levelling and VVVF drives deliver a "
            "premium ride that suits residential apartments, hospitals, hotels and "
            "corporate buildings."
        ),
    },
    {
        "slug": "passenger-manual",
        "name": "Passenger Elevators — Manual Doors",
        "short": "Reliable, cost-effective lifts with manual/collapsible doors.",
        "capacity": "5 – 13 Passengers",
        "speed": "Up to 0.68 m/s",
        "icon": "passenger",
        "tag": "Value",
        "highlights": [
            "Economical solution for low & mid-rise buildings",
            "Sturdy MS collapsible / imperforated doors",
            "Easy maintenance and long service life",
            "Multiple cabin design options",
        ],
        "description": (
            "A dependable, budget-friendly choice for homes and smaller buildings. "
            "Manual-door passenger elevators offer proven mechanics with a wide "
            "selection of doors and cabin finishes at an affordable price point."
        ),
    },
    {
        "slug": "capsule",
        "name": "Capsule Elevators",
        "short": "Ultra-modern panoramic lifts that become an architectural centrepiece.",
        "capacity": "10 – 16 Passengers",
        "speed": "Up to 1.5 m/s",
        "icon": "capsule",
        "tag": "Signature",
        "highlights": [
            "Glass vision panels for panoramic views",
            "Stainless / mild-steel structural options",
            "VVVF drive for smooth motion",
            "Custom lighting & finishes",
        ],
        "description": (
            "Make a statement. Capsule elevators fuse engineering with design, "
            "offering panoramic glass cabins that transform malls, hotels and "
            "showrooms into landmarks while carrying passengers in style."
        ),
    },
    {
        "slug": "round-capsule",
        "name": "Round Capsule Elevators",
        "short": "Full-glass circular capsules for a truly premium arrival experience.",
        "capacity": "10 – 16 Passengers",
        "speed": "Up to 1.5 m/s",
        "icon": "capsule",
        "tag": "Premium",
        "highlights": [
            "360° curved-glass cabin",
            "Three-side glass viewing options",
            "Bespoke lighting packages",
            "Statement piece for luxury spaces",
        ],
        "description": (
            "The round capsule elevator is the pinnacle of panoramic vertical "
            "transport — a curved, full-glass cabin that turns every ride into an "
            "experience. Perfect for luxury hotels, malls and flagship showrooms."
        ),
    },
    {
        "slug": "hospital",
        "name": "Hospital / Stretcher Elevators",
        "short": "Spacious, gentle-motion lifts engineered for healthcare.",
        "capacity": "8 – 12 Passengers",
        "speed": "Up to 1.0 m/s",
        "icon": "hospital",
        "tag": "Healthcare",
        "highlights": [
            "Deep cabins sized for stretchers & beds",
            "Ultra-smooth, jerk-free levelling",
            "Anti-bacterial cabin finishes available",
            "Battery-backed Automatic Rescue Device (ARD)",
        ],
        "description": (
            "Designed for hospitals and nursing homes, these elevators offer deep "
            "cabins to accommodate stretchers, beds and medical staff, with "
            "exceptionally smooth motion and precise floor levelling for patient "
            "comfort and safety."
        ),
    },
    {
        "slug": "goods",
        "name": "Goods / Freight Elevators",
        "short": "Heavy-duty workhorses for warehouses, factories and retail.",
        "capacity": "500 – 3000 kg",
        "speed": "0.25 – 1.0 m/s",
        "icon": "goods",
        "tag": "Industrial",
        "highlights": [
            "Rugged load capacities from 500 kg to 3 tonnes",
            "Reinforced cabin flooring & bumpers",
            "Wide door openings for pallets",
            "Overload protection system",
        ],
        "description": (
            "Built to move materials, not people around them. Our goods elevators "
            "handle demanding industrial and commercial loads with reinforced "
            "structures and dependable drives for years of heavy use."
        ),
    },
    {
        "slug": "car-parking",
        "name": "Car Parking Elevators",
        "short": "Vertical car lifts that unlock parking in tight urban plots.",
        "capacity": "500 – 5000 kg",
        "speed": "Up to 0.5 m/s",
        "icon": "parking",
        "tag": "Space Saver",
        "highlights": [
            "Travel heights up to 100 m",
            "Handles vehicles up to 5 tonnes",
            "Ideal for stack & multi-level parking",
            "Robust safety interlocks",
        ],
        "description": (
            "Turn limited ground area into multi-level parking. Silex car parking "
            "elevators move vehicles safely between levels, maximising real-estate "
            "value in dense Indian cities."
        ),
    },
    {
        "slug": "hydraulic",
        "name": "Hydraulic Elevators",
        "short": "Compact low-rise lifts with a soft, whisper-quiet ride.",
        "capacity": "225 – 1600 kg (3 – 20 persons)",
        "speed": "Up to 0.5 m/s",
        "icon": "hydraulic",
        "tag": "Low-Rise",
        "highlights": [
            "No overhead machine room required",
            "Smooth, quiet operation",
            "Pipe-rupture & overload safety valves",
            "Great for villas, showrooms & low buildings",
        ],
        "description": (
            "Hydraulic elevators are the perfect low-rise solution, using a piston "
            "drive for exceptionally smooth, quiet travel. With no rooftop machine "
            "room needed, they fit beautifully into villas, boutiques and heritage "
            "buildings."
        ),
    },
]

# ---------------------------------------------------------------------------
# Services (installation, AMC/maintenance, modernization, etc.)
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "icon": "install",
        "title": "Supply & Installation",
        "text": (
            "End-to-end manufacturing, supply and professional installation by "
            "qualified engineers — from shaft survey to final commissioning."
        ),
    },
    {
        "icon": "amc",
        "title": "AMC & Maintenance",
        "text": (
            "Annual Maintenance Contracts with scheduled preventive servicing to "
            "keep your lifts running safely, smoothly and reliably year-round."
        ),
    },
    {
        "icon": "modernize",
        "title": "Modernization & Upgrades",
        "text": (
            "Breathe new life into ageing elevators with modern VVVF drives, "
            "controllers, cabins and safety systems — without a full replacement."
        ),
    },
    {
        "icon": "support",
        "title": "24×7 Emergency Support",
        "text": (
            "A responsive service network across Gujarat and beyond, backed by "
            "genuine spares and Automatic Rescue Devices for peace of mind."
        ),
    },
    {
        "icon": "design",
        "title": "Custom Design & Consultation",
        "text": (
            "In-house R&D and computer-aided design to tailor capacity, speed and "
            "finishes to your building and budget."
        ),
    },
    {
        "icon": "safety",
        "title": "Safety Audits & Compliance",
        "text": (
            "Inspections and safety retrofits that bring your vertical transport up "
            "to current standards and licensing requirements."
        ),
    },
]

# ---------------------------------------------------------------------------
# "Why Us" pillars
# ---------------------------------------------------------------------------
WHY_US = [
    {
        "icon": "iso",
        "title": "ISO 9001:2008 Certified",
        "text": "Certified quality management across manufacturing and service.",
    },
    {
        "icon": "factory",
        "title": "In-House Manufacturing",
        "text": "Two well-developed factories with modern, computer-enabled machinery.",
    },
    {
        "icon": "rnd",
        "title": "Dedicated R&D",
        "text": "An in-house research team continuously refining performance & safety.",
    },
    {
        "icon": "rupee",
        "title": "Affordable Excellence",
        "text": "Premium 'silky motion' engineering at genuinely competitive prices.",
    },
    {
        "icon": "globe",
        "title": "Proven Global Reach",
        "text": "Trusted across 20+ Indian cities and a 10-country export network.",
    },
    {
        "icon": "handshake",
        "title": "World-Class Partners",
        "text": "Components from Montanari, Wittur, Fermator, Yaskawa, Torin Drive & more.",
    },
]

# ---------------------------------------------------------------------------
# Cabin & door finish options (Optional Cabin Design pages)
# ---------------------------------------------------------------------------
CABIN_FINISHES = [
    "Titanium Gold with Stainless Steel Finish",
    "Golden with Mirror Finish",
    "Stainless Steel with Mirror Finish",
    "Stainless Steel with Decorative Finish",
    "Stainless Steel Hairline Finish",
    "S.S. Hairline with Mirror Finish",
    "M.S. Powder Coated",
    "Glass Car",
]

AUTO_DOOR_DESIGNS = [
    "Stainless Steel Hairline Finish Auto Door",
    "Glass with Stainless Steel Framed Auto Door",
    "Gold Finish Decorative Door",
    "M.S. Powder Coated Auto Door",
]

MANUAL_DOOR_DESIGNS = [
    "M.S. Collapsible Door",
    "M.S. Powder Coated Imperforated Door",
    "M.S. Powder Coated Swing Door",
    "Manual Powder Coated Telescopic Door",
]

# ---------------------------------------------------------------------------
# Fixtures & control options (COP/LOP, machines)
# ---------------------------------------------------------------------------
FIXTURES = [
    "Car Operation Panel (COP)",
    "Landing Push Button (LOP)",
    "Touch COP / LOP",
    "Automatic Rescue Device (ARD)",
    "Microprocessor Elevator Control Panel",
    "Over Speed Governor",
]

MACHINES = [
    "Montanari", "Sharp", "Single-Phase Gearless",
    "Bharat Bijlee Gearless", "Torin Drive",
]

# ---------------------------------------------------------------------------
# Technology partners (page 12)
# ---------------------------------------------------------------------------
PARTNERS = [
    "INSAT Controls", "Monarch / Inovance", "Fermator", "Montanari Giulio & C.",
    "Wittur", "Sharp Engineers", "Blain Hydraulics", "Yaskawa",
    "L&T", "Usha Martin", "Moris Hellas", "Marazzi",
    "Bharat Bijlee", "Monteferro", "Jindal Steel & Power", "Torin Drive International",
]

# ---------------------------------------------------------------------------
# Reach
# ---------------------------------------------------------------------------
INDIA_BRANCHES = [
    "Baroda", "Rajkot", "Surat", "Anand", "Mumbai", "Dahod", "Godhra",
    "Kutch-Bhuj", "Mehsana", "Palanpur", "Pali", "Shirohi", "Abu",
    "Jodhpur", "Ajmer", "Udaipur", "Indore", "Bhopal", "Jamshedpur",
    "Nashik", "Jalgaon", "Nandurbar",
]

GLOBAL_NETWORK = [
    "Australia", "Turkey", "Singapore", "Canada", "Nepal", "Bhutan",
    "Dubai", "Thailand", "Congo", "Somalia", "Uganda", "Kenya", "Tanzania",
]

# ---------------------------------------------------------------------------
# Projects / gallery (illustrative dummy references)
# ---------------------------------------------------------------------------
PROJECTS = [
    {"title": "Riverfront Residency", "city": "Surat", "type": "MRL Elevator", "photo": _img("1626628202501-0c11fde58ebf")},
    {"title": "Elifenta Business Hub", "city": "Surat", "type": "Passenger Auto-Door", "photo": _img("1758518731135-6d9af1849b25")},
    {"title": "Skyline Mall", "city": "Ahmedabad", "type": "Round Capsule", "photo": _img("1619155631589-89db583e0bcb")},
    {"title": "City Care Hospital", "city": "Rajkot", "type": "Hospital Elevator", "photo": _img("1606388653150-62e3347056aa")},
    {"title": "Metro Logistics Park", "city": "Mumbai", "type": "Goods Elevator", "photo": _img("1556537696-dc5627064044")},
    {"title": "Grand Palace Hotel", "city": "Udaipur", "type": "Capsule Elevator", "photo": _img("1763898260685-1a5b10346ba9")},
    {"title": "Green Valley Villas", "city": "Anand", "type": "Hydraulic Elevator", "photo": _img("1602339764055-2fa72b7d0475")},
    {"title": "Central Parking Tower", "city": "Indore", "type": "Car Parking Elevator", "photo": _img("1595392312388-38d093a975e3")},
]

# ---------------------------------------------------------------------------
# Testimonials (illustrative)
# ---------------------------------------------------------------------------
TESTIMONIALS = [
    {
        "quote": "The MRL lift Silex installed is whisper-quiet and our electricity "
                 "bill actually dropped. Truly silky motion.",
        "name": "Rajesh Patel", "role": "Builder, Surat",
    },
    {
        "quote": "From site survey to commissioning, the Silex engineers were "
                 "professional and on-time. Our capsule lift is the talk of the mall.",
        "name": "Meena Shah", "role": "Mall Operations, Ahmedabad",
    },
    {
        "quote": "Their 24×7 support and AMC give us complete peace of mind for a "
                 "hospital where every second counts.",
        "name": "Dr. Anil Verma", "role": "Facility Head, Rajkot",
    },
]

# ---------------------------------------------------------------------------
# Blog / news (dummy content)
# ---------------------------------------------------------------------------
BLOG_POSTS = [
    {
        "slug": "mrl-vs-conventional",
        "title": "MRL vs. Conventional Elevators: Which Is Right for Your Building?",
        "date": "2026-07-28",
        "category": "Guides",
        "excerpt": "Machine Room-Less lifts are reshaping Indian construction. Here's "
                   "how they save space, energy and cost compared to traditional systems.",
        "gradient": "g1",
        "photo": _img("1595601265373-612a09303582"),
        "body": [
            "Machine Room-Less (MRL) elevators place a compact gearless traction "
            "machine inside the hoistway itself, eliminating the separate machine "
            "room that conventional lifts require on the rooftop.",
            "For developers, that means reclaiming valuable construction area — "
            "often around 10% — along with up to 25% lower running costs thanks to "
            "efficient permanent-magnet motors.",
            "Conventional geared systems still make sense for certain heavy-duty or "
            "very high-rise applications, but for most residential and commercial "
            "buildings in India, MRL is now the smart default.",
        ],
    },
    {
        "slug": "elevator-safety-checklist",
        "title": "A 7-Point Elevator Safety Checklist Every Building Owner Should Know",
        "date": "2026-07-10",
        "category": "Safety",
        "excerpt": "Regular checks and an Automatic Rescue Device can prevent most "
                   "elevator emergencies. Use this simple checklist to stay compliant.",
        "gradient": "g4",
        "photo": _img("1746702475459-89ff401cafd8"),
        "body": [
            "Elevator safety starts with routine preventive maintenance. Frayed "
            "ropes, worn guide shoes and drifting door sensors are the usual "
            "culprits behind avoidable breakdowns.",
            "An Automatic Rescue Device (ARD) automatically brings the car to the "
            "nearest floor and opens the doors during a power failure — a must-have "
            "for Indian buildings with variable supply.",
            "Pair scheduled AMC visits with annual third-party safety audits to keep "
            "your vertical transport compliant and your residents protected.",
        ],
    },
    {
        "slug": "choosing-cabin-finish",
        "title": "Titanium Gold to Hairline Steel: Choosing the Right Cabin Finish",
        "date": "2026-06-22",
        "category": "Design",
        "excerpt": "Your elevator cabin is a first impression. Explore the finishes "
                   "that balance luxury, durability and easy maintenance.",
        "gradient": "g6",
        "photo": _img("1774801890542-c875dab300ea"),
        "body": [
            "The cabin interior is often the first thing a visitor experiences in a "
            "premium building. Silex offers finishes from Titanium Gold and mirror "
            "steel to understated hairline stainless.",
            "High-traffic commercial lobbies benefit from hairline or powder-coated "
            "finishes that hide fingerprints, while hospitality projects lean toward "
            "gold and mirror treatments for impact.",
            "Whatever the look, every finish is engineered for durability and easy "
            "cleaning so it stays impressive for years.",
        ],
    },
]

# ---------------------------------------------------------------------------
# Dropdown options for the enquiry form
# ---------------------------------------------------------------------------
ENQUIRY_TYPES = [p["name"] for p in PRODUCTS] + [
    "AMC / Maintenance", "Modernization", "Careers", "General Enquiry",
]

# ---------------------------------------------------------------------------
# Solutions by building segment (inspired by Schindler's "Segments")
# ---------------------------------------------------------------------------
SEGMENTS = [
    {
        "slug": "residential",
        "name": "Residential",
        "icon": "building",
        "img": _img("1525273177952-67455d25871f"),
        "tagline": "Silky, energy-smart mobility for homes & apartments",
        "intro": (
            "From independent villas to high-rise apartment towers, Silex "
            "residential elevators blend whisper-quiet comfort with everyday "
            "reliability — engineered to save space, energy and running cost."
        ),
        "benefits": [
            "Machine-Room-Less designs reclaim rooftop & shaft space",
            "Up to 25% lower electricity bills with gearless drives",
            "Automatic Rescue Device brings you home during power cuts",
            "Premium cabin finishes to match your interiors",
        ],
        "products": ["mrl", "passenger-auto", "hydraulic"],
    },
    {
        "slug": "commercial",
        "name": "Office & Commercial",
        "icon": "briefcase",
        "img": _img("1758448721149-aa0ce8e1b2c9"),
        "tagline": "High-traffic performance for offices & complexes",
        "intro": (
            "Commercial buildings demand fast, dependable vertical transport. "
            "Silex passenger elevators deliver smooth VVVF rides, efficient "
            "dispatch and durable finishes built for constant footfall."
        ),
        "benefits": [
            "Speeds up to 1.5 m/s for shorter wait times",
            "Robust hairline & powder-coated finishes hide wear",
            "Micro-levelling for step-free, accessible boarding",
            "Optional destination-ready control panels",
        ],
        "products": ["passenger-auto", "mrl", "goods"],
    },
    {
        "slug": "hotel",
        "name": "Hotel & Hospitality",
        "icon": "star",
        "img": _img("1564771789713-8586b829cbeb"),
        "tagline": "A grand first impression on every floor",
        "intro": (
            "Hospitality is about the experience. Silex capsule and premium "
            "passenger elevators turn a routine ride into a signature moment "
            "with panoramic glass cars and luxurious gold & mirror finishes."
        ),
        "benefits": [
            "Panoramic capsule & round-capsule showpieces",
            "Titanium-gold and mirror cabin treatments",
            "Silent operation for restful guest floors",
            "Custom lighting & fixture options",
        ],
        "products": ["capsule", "round-capsule", "passenger-auto"],
    },
    {
        "slug": "retail",
        "name": "Retail & Malls",
        "icon": "cart",
        "img": _img("1619155631589-89db583e0bcb"),
        "tagline": "Move crowds in style and safety",
        "intro": (
            "Shopping centres need to move large volumes of people smoothly. "
            "Silex offers panoramic capsules for showcase atriums and heavy-duty "
            "passenger lifts for reliable, high-capacity crowd flow."
        ),
        "benefits": [
            "High-capacity cars for peak footfall",
            "Panoramic glass to showcase your atrium",
            "Durable finishes for heavy public use",
            "Priority AMC to minimise downtime",
        ],
        "products": ["round-capsule", "passenger-auto", "goods"],
    },
    {
        "slug": "healthcare",
        "name": "Healthcare",
        "icon": "cross",
        "img": _img("1764213077578-eab0ab29f949"),
        "tagline": "Stretcher-ready lifts where every second counts",
        "intro": (
            "Hospitals rely on dependable, spacious elevators for patients, "
            "stretchers and equipment. Silex hospital elevators deliver deep "
            "cars, gentle levelling and 24×7 supported reliability."
        ),
        "benefits": [
            "Deep cars sized for stretchers & beds",
            "Smooth, jerk-free levelling for patient comfort",
            "Antibacterial-friendly stainless finishes",
            "Priority 24×7 breakdown support & AMC",
        ],
        "products": ["hospital", "goods", "passenger-auto"],
    },
    {
        "slug": "public-transport",
        "name": "Public & Infrastructure",
        "icon": "transit",
        "img": _img("1595392312388-38d093a975e3"),
        "tagline": "Rugged mobility for stations & public spaces",
        "intro": (
            "Metro stations, parking towers and public infrastructure need "
            "rugged, high-throughput vertical transport. Silex goods, parking "
            "and heavy passenger elevators are built to keep cities moving."
        ),
        "benefits": [
            "Heavy-duty goods & freight capacities",
            "Automated car-parking elevator systems",
            "Weather-tough construction for public sites",
            "Scheduled preventive maintenance programs",
        ],
        "products": ["goods", "car-parking", "passenger-auto"],
    },
]

# ---------------------------------------------------------------------------
# AMC / Maintenance plans (inspired by Schindler "Services")
# ---------------------------------------------------------------------------
AMC_PLANS = [
    {
        "name": "Essential",
        "price": "Basic Cover",
        "best": "Homes & small buildings",
        "featured": False,
        "features": [
            "Scheduled preventive visits",
            "Lubrication & safety checks",
            "Breakdown call-out support",
            "Genuine spare parts (billed)",
        ],
    },
    {
        "name": "Comprehensive",
        "price": "Most Popular",
        "best": "Apartments & offices",
        "featured": True,
        "features": [
            "Everything in Essential",
            "Priority 24×7 breakdown response",
            "Wear-and-tear parts included",
            "ARD & safety-device testing",
            "Half-yearly detailed audit",
        ],
    },
    {
        "name": "Premium Care",
        "price": "Total Peace of Mind",
        "best": "Hospitals, malls & hotels",
        "featured": False,
        "features": [
            "Everything in Comprehensive",
            "Dedicated response engineer",
            "Guaranteed uptime SLA",
            "Remote health monitoring ready",
            "Annual modernization review",
        ],
    },
]

SERVICE_STEPS = [
    {"icon": "search", "title": "Site Survey", "text": "Free assessment of your building, traffic and shaft."},
    {"icon": "layers", "title": "Design & Quote", "text": "Tailored elevator recommendation with transparent pricing."},
    {"icon": "wrench", "title": "Installation", "text": "Precise, safe installation by trained Silex engineers."},
    {"icon": "shield", "title": "AMC & Support", "text": "Ongoing maintenance and 24×7 breakdown support."},
]

# ---------------------------------------------------------------------------
# Modernization scope
# ---------------------------------------------------------------------------
MODERNIZATION = [
    {"title": "Drive & Control Upgrade", "text": "Swap old relay logic for a smooth microprocessor VVVF drive — quieter rides and lower bills."},
    {"title": "Cabin Makeover", "text": "Refresh tired interiors with new finishes, lighting, flooring and fixtures."},
    {"title": "Door Modernization", "text": "Upgrade to automatic doors with infrared sensors for safety and convenience."},
    {"title": "Safety Retrofit", "text": "Add an Automatic Rescue Device, overspeed governor and modern safety gear."},
    {"title": "Energy Efficiency", "text": "Move to gearless permanent-magnet machines and LED lighting to cut power use."},
    {"title": "Accessibility", "text": "Micro-levelling, braille COP and voice announcements for step-free, inclusive access."},
]

# ---------------------------------------------------------------------------
# Technology & Innovations (inspired by Schindler "Innovations")
# ---------------------------------------------------------------------------
INNOVATIONS = [
    {"icon": "bolt", "name": "Gearless PM Drive", "text": "Permanent-magnet gearless traction for silky, energy-efficient motion with minimal maintenance."},
    {"icon": "wave", "name": "VVVF Control", "text": "Variable-voltage, variable-frequency drives deliver smooth acceleration and precise floor levelling."},
    {"icon": "shield", "name": "Automatic Rescue Device", "text": "On power failure, the ARD moves the car to the nearest floor and opens the doors automatically."},
    {"icon": "cpu", "name": "Microprocessor Control", "text": "Intelligent control panels optimise dispatch, diagnostics and ride comfort."},
    {"icon": "gauge", "name": "Overspeed Governor", "text": "Mechanical safety system that engages instantly if the car exceeds safe speed."},
    {"icon": "leaf", "name": "Eco & Space Saving", "text": "MRL design plus LED lighting and standby modes reclaim space and cut energy up to 25%."},
]

# ---------------------------------------------------------------------------
# Careers (inspired by Schindler "Careers")
# ---------------------------------------------------------------------------
JOB_OPENINGS = [
    {"title": "Elevator Installation Engineer", "location": "Surat, Gujarat", "type": "Full-time", "exp": "1–4 yrs",
     "summary": "Lead on-site installation and commissioning of Silex elevators across Gujarat."},
    {"title": "Service & AMC Technician", "location": "Baroda / Rajkot", "type": "Full-time", "exp": "1–3 yrs",
     "summary": "Perform preventive maintenance and breakdown support for our AMC customers."},
    {"title": "Sales Executive — Elevators", "location": "Surat, Gujarat", "type": "Full-time", "exp": "0–3 yrs",
     "summary": "Drive new enquiries, site surveys and quotations for residential & commercial projects."},
    {"title": "Design / CAD Engineer", "location": "Surat (HO)", "type": "Full-time", "exp": "1–5 yrs",
     "summary": "Prepare layout drawings, GA drawings and customised cabin designs."},
]

WHY_JOIN = [
    "ISO 9001:2008 certified, growing Indian elevator brand",
    "Hands-on training with modern gearless & MRL technology",
    "Pan-India project exposure across 20+ cities",
    "Supportive team culture and clear growth path",
]

# ---------------------------------------------------------------------------
# FAQ (inspired by Schindler support content)
# ---------------------------------------------------------------------------
FAQS = [
    {"q": "What is a Machine-Room-Less (MRL) elevator?",
     "a": "An MRL elevator houses a compact gearless motor inside the shaft itself, so no separate machine room is needed. It saves construction space and reduces energy consumption by up to 25%."},
    {"q": "How long does installation take?",
     "a": "For a typical low-rise residential building, installation and commissioning usually take a few weeks after site readiness. We share an exact timeline after the free site survey."},
    {"q": "Do you provide Annual Maintenance Contracts (AMC)?",
     "a": "Yes. We offer Essential, Comprehensive and Premium Care AMC plans with scheduled preventive visits and 24×7 breakdown support. See our AMC & Maintenance page for details."},
    {"q": "What happens during a power failure?",
     "a": "Elevators fitted with an Automatic Rescue Device (ARD) automatically move to the nearest floor and open the doors, so passengers are never stranded."},
    {"q": "Can you modernize my existing elevator?",
     "a": "Absolutely. We upgrade drives, controls, doors, cabins and safety systems on most existing elevators — often without replacing the entire unit."},
    {"q": "Which areas do you serve?",
     "a": "We serve 20+ cities across India from our Surat headquarters, with a supply network reaching 10+ countries worldwide."},
    {"q": "How do I get a price quote?",
     "a": "Request a free site survey through our Contact page or WhatsApp us. We assess your building and share a transparent, tailored quotation."},
    {"q": "Are Silex elevators safe and certified?",
     "a": "Yes. Silex is an ISO 9001:2008 certified manufacturer, and our elevators include overspeed governors, ARD and modern safety gear as standard."},
]

# ---------------------------------------------------------------------------
# Social media
# ---------------------------------------------------------------------------
SOCIAL_LINKS = [
    {"name": "Instagram", "icon": "instagram", "url": "https://www.instagram.com/silex.elevator?igsh=MWF6cnFhMGdjOW5kZw=="},
    {"name": "LinkedIn", "icon": "linkedin", "url": "https://www.linkedin.com/in/silex-elevator-969a3042a?utm_source=share_via&utm_content=profile&utm_medium=member_android"},
]

# ---------------------------------------------------------------------------
# Technical specifications per product (transcribed from the Silex brochure).
# Each entry has a `summary` (key facts) and an optional dimensional `table`,
# so the full brochure detail lives on-site and clients never need the PDF.
# All linear dimensions are in millimetres unless stated otherwise.
# ---------------------------------------------------------------------------
_SPEC_NOTE = (
    "All dimensions in mm. Hoistway walls should be minimum 230 mm brick or "
    "150 mm RCC. General data — may change without notice; contact us for a "
    "project-specific drawing."
)

SPECS = {
    "mrl": {
        "summary": [
            ["Capacity", "6 – 13 passengers (408 – 884 kg)"],
            ["Drive", "Permanent-magnet gearless traction, VVVF"],
            ["Door options", "Auto centre-opening or manual telescopic"],
            ["Rated speed", "Up to 1.0 m/s"],
            ["Machine room", "Not required (machine-room-less)"],
        ],
        "table": {
            "headers": ["Persons", "Load (kg)", "Car A", "Car B", "Shaft C",
                        "Shaft D", "Entrance E", "Auto door W×H", "Manual door W×H"],
            "rows": [
                ["6", "408", "1200", "900", "1800", "1400", "700", "780×2100", "1450×2350"],
                ["8", "544", "1300", "1100", "1900", "1600", "800", "880×2100", "1600×2350"],
                ["10", "680", "1300", "1300", "1900", "1800", "800", "880×2100", "1600×2350"],
                ["13", "884", "1600", "1400", "2200", "1900", "900", "980×2100", "1700×2350"],
            ],
            "note": _SPEC_NOTE,
        },
    },
    "passenger-auto": {
        "summary": [
            ["Capacity", "6 – 13 passengers (408 – 884 kg)"],
            ["Door type", "Automatic centre-opening"],
            ["Drive", "VVVF variable-speed, collective operation"],
            ["Rated speed", "Up to 1.5 m/s"],
            ["Pit / Overhead", "1600 / 4900"],
        ],
        "table": {
            "headers": ["Persons", "Load (kg)", "Platform A", "Platform B",
                        "Shaft C", "Shaft D", "Entrance E", "Machine room K", "Machine room L"],
            "rows": [
                ["6", "408", "1200", "1300", "1700", "1800", "700", "300+C+300", "600+D+1500"],
                ["8", "544", "1500", "1330", "2000", "1800", "800", "300+C+300", "600+D+1500"],
                ["10", "680", "1650", "1450", "2150", "2000", "800", "600+C+600", "600+D+1500"],
                ["13", "884", "1900", "1500", "2400", "2000", "900", "600+C+600", "600+D+1500"],
            ],
            "note": _SPEC_NOTE,
        },
    },
    "passenger-manual": {
        "summary": [
            ["Capacity", "5 – 13 passengers (340 – 884 kg)"],
            ["Door type", "Collapsible / swing / imperforated"],
            ["Drive", "Geared machine, VVVF"],
            ["Rated speed", "Up to 0.68 m/s"],
            ["Pit / Overhead", "1600 / 4900"],
        ],
        "table": {
            "headers": ["Persons", "Load (kg)", "Platform A", "Platform B",
                        "Shaft C", "Shaft D", "Entrance E", "Machine room K", "Machine room L"],
            "rows": [
                ["5", "340", "950", "1300", "1350", "1650", "760", "600+C+600", "300+D+1500"],
                ["5", "340", "1300", "1000", "1700", "1300", "760", "300+C+300", "600+D+1500"],
                ["6", "408", "1200", "1200", "1600", "1500", "800", "300+C+300", "600+D+1500"],
                ["6", "544", "1500", "1200", "1900", "1500", "800", "300+C+300", "600+D+1500"],
                ["13", "884", "1900", "1500", "2400", "1850", "900", "600+C+600", "300+D+1500"],
            ],
            "note": _SPEC_NOTE,
        },
    },
    "capsule": {
        "summary": [
            ["Capacity", "10 – 16 passengers (680 – 1088 kg)"],
            ["Cabin", "SS / MS with glass vision panels"],
            ["Drive", "AC VVVF for jerk-free ride"],
            ["Controller", "PLC full-proof, fully collective-selective"],
            ["Rated speed", "Up to 1.5 m/s"],
        ],
        "table": {
            "headers": ["Persons", "Load (kg)", "Car A", "Car B", "Car G",
                        "Shaft C", "Shaft D", "Shaft F", "Shaft H", "Entrance E"],
            "rows": [
                ["10", "680", "1250", "1300", "250", "2200", "1450", "1480", "580", "800"],
                ["13", "884", "1400", "1400", "300", "2400", "1550", "1630", "650", "900"],
                ["16", "1088", "1550", "1500", "350", "2800", "1780", "1650", "790", "1000"],
            ],
            "note": _SPEC_NOTE + " Table shown for three-side-glass capsule cabins.",
        },
    },
    "round-capsule": {
        "summary": [
            ["Capacity", "10 – 16 passengers (680 – 1088 kg)"],
            ["Cabin", "360° curved-glass panoramic capsule"],
            ["Drive", "AC VVVF for smooth motion"],
            ["Rated speed", "Up to 1.5 m/s"],
            ["Finish", "Bespoke lighting packages available"],
        ],
        "table": {
            "headers": ["Persons", "Load (kg)", "Car A", "Car B", "Car J", "Car G",
                        "Shaft C", "Shaft D", "Shaft F", "Shaft H", "Entrance E"],
            "rows": [
                ["10", "680", "1100", "1300", "1400", "650", "2200", "1325", "1330", "1100", "800"],
                ["13", "884", "1200", "1400", "1550", "700", "2400", "1425", "1430", "1100", "900"],
                ["16", "1088", "1300", "1500", "1700", "750", "2800", "1530", "1530", "1200", "1000"],
            ],
            "note": _SPEC_NOTE,
        },
    },
    "hospital": {
        "summary": [
            ["Capacity", "8 – 12 passengers (544 – 816 kg)"],
            ["Door type", "Collapsible"],
            ["Rated speed", "0.3 – 0.5 m/s"],
            ["Pit / Overhead", "1600 / 1600"],
            ["Hoisting beam", "3500 kg capacity"],
        ],
        "table": {
            "headers": ["Persons", "Load (kg)", "Platform A", "Platform B",
                        "Shaft C", "Shaft D", "Entrance E", "Machine room K", "Machine room L"],
            "rows": [
                ["8 – 12", "544 – 816", "1200", "2300", "1900", "2400", "1600", "600+C+600", "600+D+1800"],
            ],
            "note": _SPEC_NOTE,
        },
    },
    "goods": {
        "summary": [
            ["Capacity", "500 – 3000 kg"],
            ["Rated speed", "0.25 – 1.0 m/s"],
            ["Pit / Overhead", "1600 / 5100"],
            ["Loading hook", "1-tonne machine-room hook"],
            ["Doors", "Wide openings for pallets & trolleys"],
        ],
        "table": {
            "headers": ["Load (kg)", "Car A", "Car B", "Shaft C", "Shaft D",
                        "Entrance E", "Machine room K", "Machine room L"],
            "rows": [
                ["500", "1500", "1200", "1900", "1600", "1500", "2500", "4100"],
                ["1000", "1500", "1800", "2300", "2000", "1800", "2500", "4700"],
                ["1500", "1700", "2000", "2600", "2300", "2100", "2600", "4900"],
                ["2000", "1700", "2500", "2600", "2900", "2400", "2600", "5400"],
                ["2500", "2000", "2500", "2900", "2900", "2700", "2900", "5400"],
                ["3000", "2000", "3000", "2900", "3400", "2700", "2900", "5900"],
            ],
            "note": _SPEC_NOTE,
        },
    },
    "car-parking": {
        "summary": [
            ["Segment", "Industrial applications & car parks"],
            ["Max. travel", "100 m (higher travel on request)"],
            ["Max. load", "500 – 5000 kg per vehicle"],
            ["Max. speed", "0.5 m/s (other speeds on request)"],
            ["Group size", "Simplex"],
        ],
    },
    "hydraulic": {
        "summary": [
            ["Capacity", "225 – 1600 kg (3 – 20 persons)"],
            ["Drive", "Hydraulic piston power-pack"],
            ["Machine room", "No overhead room required"],
            ["Rated speed", "Up to 0.5 m/s"],
            ["Safety", "Pipe-rupture & overload valves"],
        ],
        "components": [
            "EV-100 control valve", "Hand pump", "Guide rail",
            "Overload system", "Pipe-rupture valve", "Screw pump",
            "Elevator rope", "Door sensor",
        ],
    },
}

# ---------------------------------------------------------------------------
# Attach curated photography to each product so templates stay data-driven.
# ---------------------------------------------------------------------------
_FALLBACK_PHOTO = _img("1758448721149-aa0ce8e1b2c9")
for _product in PRODUCTS:
    _product["photo"] = PRODUCT_PHOTOS.get(_product["slug"], _FALLBACK_PHOTO)
