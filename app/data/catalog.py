"""
Service Catalog Data
====================

Master service catalog extracted from salon management system.
Source: Vagaro screenshots (v1 import)

Categories:
    - hair: Hair services (cuts, color, styling, treatments)
    - lashes_brows: Lash extensions, brow services, microblading
    - waxing: Body and facial waxing
    - nails: Manicures, acrylics, dip nails
    - massage_body: Massage and body treatments
    - skincare_facials: Facials, peels, skin treatments
    - makeup: Makeup application services
    - consultation_admin: Consultations, fees, deposits
"""

CATEGORIES = [
    {"slug": "hair", "name": "Hair", "sort_order": 1, "color_tag": "#8b5cf6"},
    {"slug": "lashes_brows", "name": "Lashes & Brows", "sort_order": 2, "color_tag": "#ec4899"},
    {"slug": "waxing", "name": "Waxing", "sort_order": 3, "color_tag": "#f59e0b"},
    {"slug": "nails", "name": "Nails", "sort_order": 4, "color_tag": "#ef4444"},
    {"slug": "massage_body", "name": "Massage & Body", "sort_order": 5, "color_tag": "#10b981"},
    {"slug": "skincare_facials", "name": "Skincare & Facials", "sort_order": 6, "color_tag": "#06b6d4"},
    {"slug": "makeup", "name": "Makeup", "sort_order": 7, "color_tag": "#f43f5e"},
    {"slug": "consultation_admin", "name": "Consultations & Admin", "sort_order": 8, "color_tag": "#6b7280", "is_bookable_default": False},
]

# Service format: (name, duration_min, price_usd, tags)
# Tags: "favorite" = starred in Vagaro, "men" = men's service, "kids" = children's service

SERVICES = {
    "hair": [
        ("90 Minute Massage", 105, 110.00, None),
        ("90 Minute Massage", 90, 100.00, None),
        ("Balayage", 180, 140.00, "favorite"),
        ("Blowout", 60, 40.00, "favorite"),
        ("Braid", 30, 15.00, "favorite"),
        ("Brazilian Blowout", 120, 250.00, "favorite"),
        ("Bleach Touch Up w/Toner", 150, 110.00, "favorite"),
        ("Color Only", 45, 70.00, "favorite"),
        ("Conditioning Treatment", 45, 25.00, "favorite"),
        ("Corrective Color", 120, 170.00, "favorite"),
        ("Cut and Color", 60, 115.00, "favorite"),
        ("Curling Style", 60, 35.00, None),
        ("Dreadlocks", 60, 85.00, None),
        ("Double Process Partial Foil", 150, 120.00, "favorite"),
        ("Double Process w/ Haircut", 90, 165.00, None),
        ("Extensions", 120, 140.00, "favorite"),
        ("Extension Consultation", 30, 0.00, "favorite,consultation"),
        ("Fashion Color", 60, 100.00, "favorite"),
        ("Full Babylights", 180, 130.00, "favorite"),
        ("Full Color", 60, 80.00, "favorite"),
        ("Full Color & Cut", 135, 145.00, "favorite"),
        ("Full Double Process", 90, 125.00, "favorite"),
        ("Full Foil", 180, 130.00, "favorite"),
        ("Full Foil and Cut", 180, 155.00, "favorite"),
        ("Full Highlight + Lowlight", 180, 165.00, "favorite"),
        ("Glaze", 60, 55.00, None),
        ("Girl's Haircut (Under 10)", 45, 35.00, "favorite,kids"),
        ("Hair Tinsel", 15, 15.00, "favorite"),
        ("5 Hair Tinsels", 30, 25.00, None),
        ("Hair Consultation", 30, 0.00, "consultation"),
        ("Halo Application", 30, 0.00, None),
        ("Halo Consultation", 30, 0.00, "consultation"),
        ("Keratin Treatment", 120, 140.00, "favorite"),
        ("Men's Color & Cut", 60, 55.00, "men"),
        ("Men's Haircut", 30, 25.00, "men"),
        ("Men's Perm", 90, 85.00, "men"),
        ("Multi Process Only", 90, 130.00, None),
        ("Color Consultation", 15, 15.00, "favorite,consultation"),
        ("Child Haircut", 30, 25.00, "kids"),
        ("Bang Trim", 15, 10.00, "favorite"),
        ("Beard/Mustache Trim", 15, 5.00, "men"),
    ],

    "lashes_brows": [
        ("3 Day Lashes", 30, 35.00, None),
        ("Brow Lamination", 35, 55.00, None),
        ("Brow Lamination", 60, 75.00, None),
        ("Brow Lamination Wax", 50, 70.00, None),
        ("Brow Lamination w/ Tint", 75, 95.00, None),
        ("Brow Lam Wax Tint", 60, 80.00, None),
        ("Classic 2wk Lash Fill", 90, 60.00, None),
        ("Classic 3wk Fill Lashes", 90, 75.00, None),
        ("Classic Lashes Full Set", 120, 130.00, None),
        ("Eyebrow Wax", 15, 15.00, "favorite"),
        ("Eyebrow Tinting", 30, 20.00, None),
        ("False Lashes", 30, 15.00, None),
        ("Henna Brow Tint", 45, 30.00, None),
        ("Henna Lash Tint", 45, 20.00, None),
        ("Hybrid Full Set Lashes", 120, 150.00, None),
        ("Hybrid 2wk Fill Lashes", 90, 70.00, None),
        ("Hybrid 3wk Fill Lashes", 90, 85.00, None),
        ("Lash Fill Less Than 40%", 0, 15.00, "add-on"),
        ("Lash Lift and Tint", 75, 100.00, None),
        ("Lash/Brow Tint", 30, 45.00, None),
        ("Lash Lift", 60, 90.00, None),
        ("Lash Consultation", 30, 0.00, "consultation"),
        ("Lash Removal", 30, 25.00, None),
        ("Light Volume 3wk Fill Lashes", 90, 115.00, None),
        ("Light Volume 2wk Fill Lashes", 90, 90.00, None),
        ("Light Volume Lashes Full", 120, 190.00, None),
        ("Mega Volume 2 Week Fill", 90, 130.00, None),
        ("Mega Volume 3 Weeks Fill", 90, 145.00, None),
        ("Mega Volume Full Lash", 120, 230.00, None),
        ("Mini Fill Light Volume Lashes (7 Days)", 60, 75.00, None),
        ("Mini Fill Wispy Lashes (7 Days)", 60, 65.00, None),
        ("Lift Only", 45, 50.00, None),
        ("Microblade", 180, 400.00, None),
        ("Microblade Consultation", 30, 0.00, "consultation"),
        ("Microblade Ombre Powder Brows", 180, 400.00, None),
        ("Microblade Retouch", 90, 150.00, None),
        ("Microblade Deposit", 0, 50.00, "deposit"),
    ],

    "waxing": [
        ("Bikini Wax", 15, 50.00, None),
        ("Brazilian Male Wax", 75, 65.00, "men"),
        ("Brazilian Wax", 45, 65.00, None),
        ("Brazilian Wax", 60, 60.00, None),
        ("Brow and Lip Wax", 15, 25.00, None),
        ("Chest Wax", 30, 55.00, "men"),
        ("Chin Neck Cheeks", 60, 62.00, None),
        ("Chin Lip Brow Wax", 30, 40.00, None),
        ("Chin Wax", 15, 11.00, None),
        ("Ear Wax", 15, 14.00, None),
        ("Facial Hair Removal", 45, 35.00, "favorite"),
        ("Full Back Wax", 60, 80.00, "men"),
        ("Full Face Wax", 45, 50.00, None),
        ("Full Face Eyebrow Wax", 30, 47.00, None),
        ("Full Leg Wax", 45, 90.00, None),
        ("Full Arm Wax", 30, 45.00, None),
        ("Half Arm Wax", 30, 30.00, None),
        ("Lip Wax", 15, 12.00, None),
        ("Lower Back Wax", 30, 30.00, None),
        ("Lower Half Leg Wax (Below Knee)", 30, 45.00, None),
        ("Beard Cheeks", 45, 40.00, "men"),
        ("Face Bleach", 30, 22.00, None),
        ("Arm Bleaching", 30, 42.00, None),
    ],

    "nails": [
        ("Acrylic Removal", 60, 25.00, None),
        ("Acrylic Fill", 90, 30.00, None),
        ("Acrylic Fill with Brow Wax", 60, 37.00, None),
        ("Acrylic Fill and Brow Arch", 90, 55.00, None),
        ("Acrylic Fill + Shellac Overlay", 90, 40.00, None),
        ("Dipped Nails", 60, 40.00, None),
        ("Dip Nail Removal", 30, 20.00, None),
        ("Exfoliating Sea Salt Manicure", 30, 30.00, None),
        ("Fill with Color Tips", 90, 40.00, None),
        ("Full Set", 120, 45.00, None),
        ("Full Set + Shellac Overlay", 90, 65.00, None),
        ("Full Set Acrylics", 90, 55.00, None),
        ("Little Princess Manicure", 30, 15.00, "kids"),
        ("Little Princess Pedicure", 30, 25.00, "kids"),
        ("Manicure", 30, 30.00, None),
    ],

    "massage_body": [
        ("Aromatherapy Massage", 75, 65.00, None),
        ("Body Wrap", 60, 60.00, None),
        ("Cupping Only", 30, 40.00, None),
        ("Deep Tissue Massage", 75, 75.00, None),
        ("Detoxing Wrap", 90, 75.00, None),
        ("Full Body Cupping", 40, 60.00, None),
        ("60 Massage - Existing Client", 75, 75.00, None),
        ("60 Massage w/Cupping", 75, 100.00, None),
        ("60 Minute Massage - New Client", 75, 60.00, None),
        ("90 Min Massage w/Cupping", 120, 140.00, None),
        ("Half Hour Swedish Massage", 30, 35.00, None),
        ("Hour Swedish Massage", 75, 65.00, None),
        ("Hour Swedish Massage with CBD", 30, 85.00, None),
        ("Massage Add On", 15, 15.00, "add-on"),
    ],

    "skincare_facials": [
        ("30 Min Glow On Go Facial", 45, 55.00, None),
        ("60 Min Glow Facial", 75, 80.00, None),
        ("Bacne Facial", 75, 75.00, None),
        ("Basic Facial", 45, 55.00, None),
        ("BIO Facial 60", 75, 80.00, None),
        ("BioFacial Pro 90", 115, 100.00, None),
        ("Bioelement Lip Treatment", 5, 10.00, "add-on"),
        ("Botched Ink Removal", 120, 150.00, None),
        ("Botox", 15, 0.00, "consultation"),
        ("Enzyme/Pro 30 Peel", 45, 70.00, None),
        ("Facefit", 15, 10.00, "add-on"),
        ("High Frequency", 15, 0.00, "add-on"),
        ("Keraglaze Spray Restructurant", 30, 10.00, "add-on"),
        ("LED Facial", 75, 90.00, None),
        ("Lip Blushing", 180, 350.00, None),
        ("Micro Current", 10, 20.00, "add-on"),
        ("Micro Current Facial", 90, 110.00, None),
        ("Microcurrent Gloves Only", 40, 55.00, None),
    ],

    "makeup": [
        ("Airbrush Foundation Only Makeup", 30, 50.00, None),
        ("Eyes Only Makeup", 30, 30.00, "favorite"),
        ("Full Face Airbrush Makeup", 60, 85.00, None),
        ("Full Face Traditional Makeup", 60, 70.00, "favorite"),
    ],

    "consultation_admin": [
        ("1 Extra Bowl of Color", 0, 30.00, "favorite,add-on"),
        ("Credit Card Fee", 0, 1.00, "fee"),
        ("Filler", 30, 0.00, "consultation"),
    ],
}


def get_all_services_flat() -> list:
    """Return all services as flat list with category info."""
    result = []
    for category_slug, services in SERVICES.items():
        for name, duration, price, tags in services:
            result.append({
                "category_slug": category_slug,
                "name": name,
                "default_duration_min": duration,
                "default_price_usd": price,
                "tags": tags,
                "bookable": "consultation" not in (tags or "") and "fee" not in (tags or "") and "deposit" not in (tags or ""),
            })
    return result


def get_catalog_stats() -> dict:
    """Return statistics about the catalog."""
    all_services = get_all_services_flat()
    prices = [s["default_price_usd"] for s in all_services]
    durations = [s["default_duration_min"] for s in all_services if s["default_duration_min"] > 0]

    by_category = {}
    for category_slug, services in SERVICES.items():
        by_category[category_slug] = len(services)

    return {
        "total_services": len(all_services),
        "bookable_services": len([s for s in all_services if s["bookable"]]),
        "by_category": by_category,
        "price_range": {"min": min(prices), "max": max(prices), "avg": sum(prices) / len(prices)},
        "duration_range": {"min": min(durations), "max": max(durations), "avg": sum(durations) / len(durations)},
    }
