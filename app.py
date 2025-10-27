from pathlib import Path
from flask import Flask, render_template, abort

app = Flask(__name__)

# === Single source of truth for project cards (home + dropdown) ===
# Add/rename slugs here; "image" is the cover on the home page.
PROJECTS = [
    {
    "slug": "fidget-spinner",
    "title": "Precision Fidget Spinner",
    "desc": "Precision bat spinner with press-fit bearings and mass symmetry.",
    "image": "fidget-spinner/05-assembly.png",   # <-- cover image
},

{
    "slug": "haptic-glove",
    "title": "VR Haptic Glove",
    "desc": "Lightweight glove: flex sensing + vibro feedback for convincing touch cues.",
    "image": "haptic-glove/01-haptic-glove.png",   # cover
    "images": [                                     # gallery
        {"src": "haptic-glove/02-motors.png",         "alt": "Motor layout"},
        {"src": "haptic-glove/03-vr-hand.png",        "alt": "VR hand view"},
        {"src": "haptic-glove/04-breadboard.jpeg",    "alt": "Breadboard"},
        {"src": "haptic-glove/05-bottom-sketch.jpeg", "alt": "Palm sketch"},
        {"src": "haptic-glove/06-top-sketch.jpeg",    "alt": "Top sketch"},
        {"src": "haptic-glove/07-bom.png",            "alt": "BOM"}
    ]
}
,
{
    "slug": "cat-speaker",
    "title": "Bluetooth Speaker (Cat)",
    "desc": "Cat-shaped enclosure, compact layout, clear everyday sound.",
    "image": "cat-speaker/speaker-enclosure.png",
    "video_id": "wSyVJ7xkt0Q",
}

,
    {
    "slug": "dispensing-aid",
    "title": "Material Dispensing Aid",
    "desc": "Ergonomic tool for precise adhesive dispensing; rapid prototypes + test rigs.",
    "image": "dispensing-aid/01-model.png",   # cover + main
    # no need to list images; list_images() will auto-scan /static/img/dispensing-aid
},

    {
        "slug": "other-projects",
        "title": "Other Projects",
        "desc": "A collection of smaller builds and experiments.",
        "image": "misc-collage.jpg",
    },
]

PROJECT_MAP = {p["slug"]: p for p in PROJECTS}

# === Auto-scan helpers ===
ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".jifi"}

# Map for quick lookup (you may already have this — keep it)
PROJECT_MAP = {p["slug"]: p for p in PROJECTS}

# ---- ADD THESE TWO ----
ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

def list_images(slug: str, cover: str | None = None):
    """
    Scan /static/img/<slug>/ for images and return a list of dicts.
    If 'cover' is provided, skip that file so it doesn't show twice.
    """
    base = Path(app.static_folder) / "img" / slug
    if not base.exists():
        return []
    files = sorted([p for p in base.iterdir() if p.suffix.lower() in ALLOWED_EXTS])

    cover_name = Path(cover).name if cover else None
    items = []
    for p in files:
        if cover_name and p.name == cover_name:
            continue  # skip the cover in the grid
        items.append({
            "src": f"{slug}/{p.name}",
            "alt": p.stem.replace("-", " ").replace("_", " ").title()
        })
    return items
# === Routes ===
@app.route("/")
def index():
    return render_template("index.html", projects=PROJECTS)

@app.route("/project/<slug>")
def project(slug):
    p = PROJECT_MAP.get(slug)
    if not p:
        abort(404)
    images = p.get("images") or list_images(slug, cover=p.get("image"))
    return render_template("project.html", p={**p, "images": images})

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# Make {{ projects }} available in all templates (for the dropdown)
@app.context_processor
def inject_projects():
    return {"projects": PROJECTS}

if __name__ == "__main__":
    app.run(debug=True)
