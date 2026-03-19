#!/usr/bin/env python3
"""
Scrape all EV data from evdb.nz/evs and save as JSON.
Extracts the allVariants data from React Server Component stream.
"""

import json
import re
from urllib.request import urlopen, Request

URL = "https://evdb.nz/evs"
OUTPUT = "ev_data.json"

FIELDS = {
    "id": str,
    "name": str,
    "slug": str,
    "make_name": str,
    "model_name": str,
    "model_slug": str,
    "year": str,
    "price": float,
    "price_used": float,
    "powertrain": str,
    "shape": str,
    "drivetrain": str,
    "battery": float,
    "usable": float,
    "chem": str,
    "range": float,
    "efficiency": float,
    "power": float,
    "torque": float,
    "speed": float,
    "topspeed": float,
    "charger": float,
    "dccharger": float,
    "seats": int,
    "boot": float,
    "boot_all": float,
    "frunk": float,
    "weight": float,
    "lengthmm": float,
    "width": float,
    "height": float,
    "ground": float,
    "tow_unbrake": float,
    "tow_brake": float,
    "v2l": str,
    "v2linternal": str,
    "v2lexternal": str,
    "safetyscore": str,
    "price_per_km": float,
    "future": bool,
    "used_only": bool,
    "mia": bool,
    "country_code": str,
    "image_url": str,
}


def fetch_page(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; EVScraper/1.0)"})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def extract_variants_from_rsc(html):
    """Extract allVariants array from React Server Component stream."""
    # The RSC stream uses double-escaped JSON inside script tags:
    # self.__next_f.push([1,"...\\"allVariants\\":[...]..."])
    # First find the position of allVariants
    idx = html.find('allVariants')
    if idx < 0:
        raise ValueError("Could not find allVariants in page")

    # Get a large chunk starting from allVariants
    # The data is double-escaped: \\" for quotes, \\\\ for backslashes
    chunk = html[idx:]

    # Find the script tag boundary
    script_end = chunk.find('</script>')
    if script_end > 0:
        chunk = chunk[:script_end]

    # The format is: allVariants\\":[{...}]
    # We need to unescape: \\" -> " and \\\\ -> \\
    # First, extract just the array portion
    # Pattern: allVariants\\":[
    array_start = chunk.find('[')
    if array_start < 0:
        raise ValueError("Could not find array start after allVariants")

    text = chunk[array_start:]

    # Unescape the double-escaped JSON
    # \\\" -> \"  (escaped quote in JSON string)
    # \\" -> "   (regular quote delimiter)
    # \\\\ -> \\
    # \\n -> \n
    unescaped = text.replace('\\\\"', '\x00ESCAPED_QUOTE\x00')
    unescaped = unescaped.replace('\\"', '"')
    unescaped = unescaped.replace('\x00ESCAPED_QUOTE\x00', '\\"')
    unescaped = unescaped.replace('\\\\', '\\')

    # Find the end of the allVariants array by bracket matching
    depth = 0
    for i, c in enumerate(unescaped):
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(unescaped[:i + 1])
                except json.JSONDecodeError as e:
                    print(f"JSON parse error at position {e.pos}: {e.msg}")
                    # Try to show context around the error
                    pos = e.pos if hasattr(e, 'pos') and e.pos else 0
                    print(f"Context: ...{unescaped[max(0,pos-50):pos+50]}...")
                    raise

    raise ValueError("Could not find end of allVariants array")


def clean_value(value, target_type):
    if value is None or value == "" or value == "null":
        return None
    if target_type == bool:
        if isinstance(value, bool):
            return value
        return str(value).lower() in ("true", "1", "yes")
    if target_type == float:
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    if target_type == int:
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None
    return str(value) if value else None


def extract_image_url(variant):
    images = variant.get("variant_images", [])
    if images:
        for img in images:
            if img.get("is_primary"):
                return img.get("image_url")
        return images[0].get("image_url")
    return variant.get("image_url")


def process_variants(variants):
    print(f"Found {len(variants)} raw variants")
    cleaned = []
    for v in variants:
        ev = {}
        for field, ftype in FIELDS.items():
            if field == "image_url":
                ev[field] = extract_image_url(v)
            else:
                ev[field] = clean_value(v.get(field), ftype)

        if ev.get("model_slug"):
            ev["url"] = f"https://evdb.nz/v/{ev['model_slug']}"
        else:
            ev["url"] = None

        if ev.get("name") and ev.get("price"):
            cleaned.append(ev)

    return cleaned


def main():
    print(f"Fetching {URL}...")
    html = fetch_page(URL)
    print(f"Page fetched: {len(html)} bytes")

    print("Extracting variant data from RSC stream...")
    variants = extract_variants_from_rsc(html)

    print("Processing variants...")
    evs = process_variants(variants)

    evs.sort(key=lambda x: x.get("price") or 999999)
    print(f"Cleaned {len(evs)} EVs")

    with open(OUTPUT, "w") as f:
        json.dump(evs, f, indent=2)
    print(f"Saved to {OUTPUT}")

    prices = [e["price"] for e in evs if e.get("price")]
    makes = set(e["make_name"] for e in evs if e.get("make_name"))
    shapes = set(e["shape"] for e in evs if e.get("shape"))
    print(f"\nSummary:")
    print(f"  Makes: {len(makes)} ({', '.join(sorted(makes))})")
    print(f"  Shapes: {', '.join(sorted(shapes))}")
    print(f"  Price range: ${min(prices):,.0f} - ${max(prices):,.0f}")


if __name__ == "__main__":
    main()
