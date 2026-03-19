#!/usr/bin/env python3
"""Inject ev_data.json into index.html to create a self-contained page."""

import json

with open("ev_data.json") as f:
    data = json.load(f)

with open("index.html") as f:
    html = f.read()

# Replace placeholder with actual data
output = html.replace("EV_DATA_PLACEHOLDER", json.dumps(data))

with open("ev_finder.html", "w") as f:
    f.write(output)

print(f"Built ev_finder.html with {len(data)} EVs ({len(output)//1024} KB)")
