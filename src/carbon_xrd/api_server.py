"""Simple Flask-based API server for Carbon XRD CLI integration."""

import os
import sys
import json
import tempfile
import subprocess
import base64
from pathlib import Path
from flask import Flask, request, jsonify
from typing import Dict, Any, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from carbon_xrd.cif_validator import CIFValidator
from carbon_xrd.xrd_calculator import XRDCalculator
from carbon_xrd.total_scattering import TotalScatteringCalculator

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def encode_image_to_base64(image_path: str) -> str:
    """Encode image file to base64 string."""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def create_sample_cif_from_description(description: str) -> Optional[str]:
    """
    Create a sample CIF structure from text description.
    This is a simplified placeholder - in production, use Claude API.
    """
    cif_templates = {
        "graphene": """data_graphene
_cell_length_a    2.4585
_cell_length_b    2.4585
_cell_length_c   10.0000
_cell_angle_alpha   90.00000
_cell_angle_beta    90.00000
_cell_angle_gamma  120.00000
_symmetry_Int_Tables_number   1
_chemical_formula_structural   C
_chemical_formula_sum   'C 2'
_cell_volume   51.98
_cell_formula_units_Z   2
loop_
_symmetry_equiv_pos_site_id
_symmetry_equiv_pos_as_xyz
  1  'x, y, z'
loop_
   _atom_site_label
   _atom_site_occupancy
   _atom_site_fract_x
   _atom_site_fract_y
   _atom_site_fract_z
   _atom_site_thermal_displace_type
   _atom_site_B_iso_or_equiv
   _atom_site_type_symbol
   C1     1.0000 0.33333  0.66667  0.00000  Biso   1.000  C
   C2     1.0000 0.66667  0.33333  0.00000  Biso   1.000  C
""",
        "graphite": """data_graphite
_cell_length_a    2.4614
_cell_length_b    2.4614
_cell_length_c    6.7079
_cell_angle_alpha   90.00000
_cell_angle_beta    90.00000
_cell_angle_gamma  120.00000
_symmetry_Int_Tables_number   194
_chemical_formula_structural   C
_chemical_formula_sum   'C 4'
_cell_volume   35.23
_cell_formula_units_Z   4
loop_
_symmetry_equiv_pos_site_id
_symmetry_equiv_pos_as_xyz
  1  'x, y, z'
  2  '-y, x-y, z'
  3  '-x+y, -x, z'
  4  'x, y, -z'
  5  '-y, x-y, -z'
  6  '-x+y, -x, -z'
loop_
   _atom_site_label
   _atom_site_occupancy
   _atom_site_fract_x
   _atom_site_fract_y
   _atom_site_fract_z
   _atom_site_thermal_displace_type
   _atom_site_B_iso_or_equiv
   _atom_site_type_symbol
   C1     1.0000 0.33333  0.66667  0.12500  Biso   1.000  C
""",
    }

    # Simple keyword matching for template selection
    description_lower = description.lower()
    for key, cif in cif_templates.items():
        if key in description_lower:
            return cif

    # Default to graphite
    return cif_templates["graphite"]


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "carbon-xrd-api"})


@app.route('/api/v1/generate-pattern', methods=['POST'])
def generate_pattern():
    """
    Generate XRD and total scattering patterns from CIF.

    Request JSON:
    {
        "cif_content": "CIF file content or 'graphene'/'graphite'",
        "include_pdf": true/false,
        "peak_threshold": 1.0
    }
    """
    try:
        data = request.get_json()

        # Validate input
        if not data or 'cif_content' not in data:
            return jsonify({"error": "Missing 'cif_content' field"}), 400

        cif_content = data.get('cif_content', '')
        include_pdf = data.get('include_pdf', False)
        peak_threshold = data.get('peak_threshold', 1.0)

        # If content is short, treat as template name
        if len(cif_content) < 100:
            cif_content = create_sample_cif_from_description(cif_content)
            if not cif_content:
                return jsonify({"error": "Unknown structure type"}), 400

        # Create temporary CIF file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cif', delete=False) as f:
            f.write(cif_content)
            cif_path = f.name

        # Create output directory
        with tempfile.TemporaryDirectory() as output_dir:
            try:
                # Validate CIF
                validator = CIFValidator()
                structure = validator.validate_and_load(cif_path)
                info = validator.get_structure_info(structure)

                # Calculate XRD
                xrd_calc = XRDCalculator()
                two_theta, intensity = xrd_calc.calculate_pattern(structure)
                peaks_df = xrd_calc.extract_peaks(two_theta, intensity, threshold=peak_threshold)

                # Plot XRD
                xrd_png = Path(output_dir) / "xrd_pattern.png"
                xrd_calc.plot_pattern(two_theta, intensity, str(xrd_png), dpi=150)

                # Calculate Total Scattering
                ts_calc = TotalScatteringCalculator()
                q, s_q = ts_calc.calculate_structure_factor(structure)

                # Plot Total Scattering
                ts_png = Path(output_dir) / "total_scattering.png"
                ts_calc.plot_scattering_pattern(q, s_q, str(ts_png), dpi=150)

                # Calculate PDF if requested
                pdf_b64 = None
                if include_pdf:
                    r, g_r = ts_calc.calculate_pdf(structure)
                    pdf_png = Path(output_dir) / "pdf_pattern.png"
                    ts_calc.plot_pdf(r, g_r, str(pdf_png), dpi=150)
                    pdf_b64 = encode_image_to_base64(str(pdf_png))

                # Encode images
                xrd_b64 = encode_image_to_base64(str(xrd_png))
                ts_b64 = encode_image_to_base64(str(ts_png))

                # Prepare response
                response = {
                    "success": True,
                    "structure_info": info,
                    "xrd_plot": f"data:image/png;base64,{xrd_b64}",
                    "total_scattering_plot": f"data:image/png;base64,{ts_b64}",
                    "peaks_data": peaks_df.to_dict(orient='records'),
                    "num_peaks": len(peaks_df),
                    "message": f"Successfully generated patterns for {info['formula']} with {len(peaks_df)} peaks detected.",
                }

                if include_pdf and pdf_b64:
                    response["pdf_plot"] = f"data:image/png;base64,{pdf_b64}"

                return jsonify(response)

            finally:
                # Cleanup temp CIF file
                if os.path.exists(cif_path):
                    os.remove(cif_path)

    except ValueError as e:
        return jsonify({"error": f"Validation error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route('/api/v1/structures', methods=['GET'])
def list_structures():
    """List available sample structures."""
    structures = [
        {
            "id": "graphene",
            "name": "Graphene (Single Layer)",
            "description": "Single-layer hexagonal carbon structure",
            "formula": "C2",
        },
        {
            "id": "graphite",
            "name": "Graphite (ABA Stacking)",
            "description": "Layered graphite with ordered ABA stacking",
            "formula": "C4",
        },
    ]
    return jsonify({"structures": structures})


@app.route('/api/v1/info', methods=['GET'])
def info():
    """Get API information."""
    return jsonify({
        "name": "Carbon XRD API",
        "version": "1.0.0",
        "description": "RESTful API for XRD pattern generation from carbon structures",
        "endpoints": [
            {"path": "/health", "method": "GET", "description": "Health check"},
            {
                "path": "/api/v1/generate-pattern",
                "method": "POST",
                "description": "Generate XRD and total scattering patterns",
            },
            {
                "path": "/api/v1/structures",
                "method": "GET",
                "description": "List available sample structures",
            },
            {"path": "/api/v1/info", "method": "GET", "description": "API information"},
        ],
    })


if __name__ == '__main__':
    # Set UTF-8 encoding for output
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    app.run(host='0.0.0.0', port=5000, debug=True)
