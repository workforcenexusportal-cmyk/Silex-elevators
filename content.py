"""All static site content for Silex Elevator, sourced from the official brochure.

Keeping copy here (instead of hard-coded in templates) makes it easy to hand
the client a single file to review or edit later, and keeps templates clean.
"""

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
    {"title": "Riverfront Residency", "city": "Surat", "type": "MRL Elevator", "img": "prod_mrl.jpg"},
    {"title": "Elifenta Business Hub", "city": "Surat", "type": "Passenger Auto-Door", "img": "prod_passenger-auto.jpg"},
    {"title": "Skyline Mall", "city": "Ahmedabad", "type": "Round Capsule", "img": "prod_round-capsule.jpg"},
    {"title": "City Care Hospital", "city": "Rajkot", "type": "Hospital Elevator", "img": "prod_hospital.jpg"},
    {"title": "Metro Logistics Park", "city": "Mumbai", "type": "Goods Elevator", "img": "prod_goods.jpg"},
    {"title": "Grand Palace Hotel", "city": "Udaipur", "type": "Capsule Elevator", "img": "prod_capsule.jpg"},
    {"title": "Green Valley Villas", "city": "Anand", "type": "Hydraulic Elevator", "img": "prod_hydraulic.jpg"},
    {"title": "Central Parking Tower", "city": "Indore", "type": "Car Parking Elevator", "img": "prod_car-parking.jpg"},
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
        "img": "prod_mrl.jpg",
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
        "img": "prod_passenger-auto.jpg",
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
        "img": "prod_capsule.jpg",
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
        "img": "prod_round-capsule.jpg",
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
        "img": "prod_hospital.jpg",
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
        "img": "prod_goods.jpg",
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
# Social media (dummy handles for the demo site)
# ---------------------------------------------------------------------------
SOCIAL_LINKS = [
    {"name": "Facebook", "icon": "facebook", "url": "https://www.facebook.com/"},
    {"name": "Instagram", "icon": "instagram", "url": "https://www.instagram.com/"},
    {"name": "LinkedIn", "icon": "linkedin", "url": "https://www.linkedin.com/"},
    {"name": "YouTube", "icon": "youtube", "url": "https://www.youtube.com/"},
]
