import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader


def normalize_images(container: list[dict[str, Any]], key: str = "images") -> None:
    """Ensure each object's images field is always a list of dicts.

    If a single mapping is provided, wrap it in a list so the template
    can safely iterate without needing conditional logic.
    """
    for obj in container:
        imgs = obj.get(key)
        if isinstance(imgs, dict):
            obj[key] = [imgs]


def collect_missing_assets(image_specs: list[tuple[str, Path]]) -> list[str]:
    missing: list[str] = []
    for logical_path, path_obj in image_specs:
        if not path_obj.exists():
            missing.append(logical_path)
    return missing


def sanitize_path(p: str) -> str:
    """Return a cleaned asset path relative to the generator root.

    - Normalizes separators to '/'
    - Strips leading './'
    - Removes an accidental duplicated top-level folder (e.g. 'portfolio_generator/')
    """
    # Normalize separators
    clean = p.replace("\\", "/")
    # Remove leading ./
    if clean.startswith("./"):
        clean = clean[2:]
    # If the path starts with the project folder name, strip it (duplication from some runs)
    if clean.startswith("portfolio_generator/"):
        clean = clean[len("portfolio_generator/") :]
    return clean


def main() -> None:
    root = Path(__file__).parent
    json_path = root / "doruk_portfolio.json"
    if not json_path.exists():
        raise FileNotFoundError(f"Portfolio JSON not found at {json_path}")

    with json_path.open(encoding="utf-8") as f:
        data = json.load(f)

    # Add defaults / derived fields
    data["current_year"] = datetime.now(tz=UTC).year
    data.setdefault("base_url", "")  # safe default for template

    # Inline SVGs for social links if paths exist
    for link in data.get("social_links", []):
        svg_path = link.get("svg_path")
        if svg_path:
            try:
                with (root / svg_path).open(encoding="utf-8") as svg_file:
                    link["svg_data"] = svg_file.read()
            except FileNotFoundError:
                print(f"[warn] SVG not found: {svg_path}")

    # Normalize images for projects & interests so template can always iterate
    normalize_images(data.get("projects", []))
    normalize_images(data.get("interests", []))

    # Track missing image assets (projects + interests + profile image)
    image_specs: list[tuple[str, Path]] = []

    # Profile image
    if data.get("image_path"):
        data["image_path"] = sanitize_path(
            data["image_path"]
        )  # mutate to cleaned version
        image_specs.append((data["image_path"], root / data["image_path"]))

    # Project images
    for proj in data.get("projects", []):
        for img in proj.get("images", []) or []:
            if isinstance(img, dict) and img.get("img_path"):
                img["img_path"] = sanitize_path(img["img_path"])  # normalize in-place
                image_specs.append((img["img_path"], root / img["img_path"]))

    # Interest images
    for intr in data.get("interests", []):
        for img in intr.get("images", []) or []:
            if isinstance(img, dict) and img.get("img_path"):
                img["img_path"] = sanitize_path(img["img_path"])  # normalize in-place
                image_specs.append((img["img_path"], root / img["img_path"]))

    missing = collect_missing_assets(image_specs)
    if missing:
        print("[info] Missing image assets (will appear as broken images in browser):")
        for m in missing:
            print(f"  - {m}")

    # Set up Jinja environment
    env = Environment(loader=FileSystemLoader(str(root)), autoescape=True)
    portfolio_template = env.get_template("index_template.html")
    # resume_template = env.get_template("resume_template.html")

    portfolio_output = portfolio_template.render(**data)

    out_file = root / "index.html"
    out_file.write_text(portfolio_output, encoding="utf-8")

    print(f"[ok] HTML file generated: {out_file}")


if __name__ == "__main__":
    main()
