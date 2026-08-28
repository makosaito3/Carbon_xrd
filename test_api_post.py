#!/usr/bin/env python
"""Test generate-pattern API endpoint."""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "src"))

from carbon_xrd.api_server import app

# Test the generate-pattern endpoint
test_payload = {
    "cif_content": "graphene",
    "include_pdf": False,
    "peak_threshold": 1.0,
}

print("Testing POST /api/v1/generate-pattern endpoint...")
print(f"Payload: {json.dumps(test_payload, indent=2)}\n")

with app.test_client() as client:
    resp = client.post(
        "/api/v1/generate-pattern",
        json=test_payload,
        content_type="application/json",
    )
    
    print(f"Response Status: {resp.status_code}")
    
    if resp.status_code == 200:
        try:
            if hasattr(resp, 'get_json'):
                data = resp.get_json()
            else:
                data = resp.json
            
            print(f"\nResponse Data:")
            print(f"  Success: {data.get('success')}")
            print(f"  Formula: {data['structure_info'].get('formula')}")
            print(f"  Atoms: {data['structure_info'].get('num_atoms')}")
            print(f"  Peaks found: {data.get('num_peaks')}")
            print(f"  XRD plot: {'Yes' if 'xrd_plot' in data and data['xrd_plot'] else 'No'}")
            print(f"  Total scattering plot: {'Yes' if 'total_scattering_plot' in data else 'No'}")
            print(f"  Message: {data.get('message')}")
            
            if data.get('peaks_data'):
                print(f"\n  Peak data (first 3 peaks):")
                for peak in data['peaks_data'][:3]:
                    print(f"    2θ={peak['2theta_deg']:.2f}°, d={peak['d_spacing_angstrom']:.4f}Å, I={peak['intensity_percent']:.2f}%")
            
            print("\n✓ POST endpoint test passed!")
        except Exception as e:
            print(f"Error parsing response: {e}")
    else:
        print(f"Error: {resp.data.decode('utf-8') if resp.data else 'No error message'}")
