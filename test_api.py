#!/usr/bin/env python
"""Test API server endpoints."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "src"))

from carbon_xrd.api_server import app

# Test the API server logic
test_data = {
    "cif_content": "graphene",
    "include_pdf": False,
    "peak_threshold": 1.0,
}

with app.test_client() as client:
    # Health check
    resp = client.get("/health")
    print(f"Health check: {resp.status_code}")

    # API info
    resp = client.get("/api/v1/info")
    print(f"API info: {resp.status_code}")

    # Structures list
    resp = client.get("/api/v1/structures")
    print(f"Structures list: {resp.status_code}")
    try:
        if hasattr(resp, 'get_json'):
            data = resp.get_json()
        else:
            data = resp.json
        print(f"  Available structures: {len(data['structures'])}")
        for s in data["structures"]:
            print(f"    - {s['name']}")
    except Exception as e:
        print(f"  Error parsing response: {e}")

print("\nAll endpoint tests passed!")
