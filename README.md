# Carbon XRD Structure Tool

X-ray diffraction (XRD) and total scattering patterns from carbon material structures.

## Overview

This tool helps carbon material researchers and developers visualize how structural changes (lattice parameters, defects, disorder) manifest in XRD and total scattering patterns.

**Workflow**:
1. Input: CIF file (crystallographic information)
2. Processing: Calculate XRD patterns, total scattering S(Q), pair distribution G(r)
3. Output: PNG plots + CSV data

## Features

- **XRD Pattern Calculation**: Generate 2θ vs. intensity plots from CIF structures
- **Total Scattering**: Calculate S(Q) structure factor in reciprocal space
- **Pair Distribution**: Generate G(r) showing atomic pair distances
- **Peak Extraction**: Identify and export peak information (2θ, d-spacing, intensity)
- **Flexible Output**: PNG (300 dpi) + CSV format

## 📖 Documentation

**Start here depending on your needs:**

| Document | Best for | Time |
|----------|----------|------|
| **[QUICKSTART.md](QUICKSTART.md)** | 🚀 Get running in 5 minutes | 5 min |
| **[PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)** | 📋 Complete operations manual | 15 min |
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | 📚 Full detailed guide with examples | 30 min |
| **[DESIGN.md](copilot_agent/DESIGN.md)** | 🔧 Architecture & technical details | 20 min |

**Quick links:**
- [3 usage methods (CLI / API / Copilot Agent)](#usage)
- [Installation steps](#installation)
- [Troubleshooting](#troubleshooting)

---

## Installation

### Requirements
- Python 3.9+
- Dependencies: pymatgen, matplotlib, pandas, numpy, scipy

### Quick Setup

**Windows:**
```powershell
cd Carbon_xrd
setup.bat
```

**macOS/Linux:**
```bash
cd Carbon_xrd
chmod +x setup.sh
./setup.sh
```

### Manual Setup

```bash
# Clone the repository
git clone https://github.com/makosaito3/Carbon_xrd.git
cd Carbon_xrd

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -m pytest tests/test_carbon_xrd.py
```

**Note:** On Windows, set UTF-8 encoding:
```powershell
$env:PYTHONIOENCODING = "utf-8"
```

⚠️ **First time?** → See [QUICKSTART.md](QUICKSTART.md) for step-by-step guide

## Usage

### 🎯 3 Ways to Use This Tool

#### Method 1: CLI (Command Line) - Simplest

```bash
export PYTHONPATH="${PWD}/src"  # macOS/Linux
# or
$env:PYTHONPATH = "$PWD\src"   # Windows PowerShell

python -m carbon_xrd.cli generate-pattern --cif structure.cif --output results/
```

**Best for:** Standalone execution, batch processing

---

#### Method 2: REST API Server - Most Flexible

```bash
# Start server
python -m carbon_xrd.api_server

# Call API (in another terminal)
curl -X POST http://localhost:5000/api/v1/generate-pattern \
  -H "Content-Type: application/json" \
  -d '{"cif_content": "graphene", "include_pdf": false}'
```

**Best for:** Web apps, multi-user access, network sharing

---

#### Method 3: M365 Copilot Agent - Most Intuitive

```bash
# Deploy to M365 Copilot
atk provision --env local

# Then open Copilot Chat and type:
# "Generate XRD pattern for graphene"
```

**Best for:** Non-technical users, natural language queries

---

### Basic Command (CLI)

```bash
python -m carbon_xrd.cli generate-pattern --cif <path/to/structure.cif> --output <output_dir>
```

### Example

```bash
python -m carbon_xrd.cli generate-pattern \
  --cif tests/graphene.cif \
  --output ./results \
  --include-pdf
```

### Command Options

```
  --cif FILE                      Path to CIF file (required)
  --output DIR                    Output directory (default: ./results)
  --wavelength FLOAT              X-ray wavelength in Angstrom
                                  (default: 1.54184 for Cu Kα)
  --xrd-range "MIN MAX"           2θ range for XRD plot (default: "5 120")
  --peak-threshold FLOAT          Peak detection threshold in % (default: 1.0)
  --include-pdf                   Calculate Pair Distribution Function
  --formats STR                   Output formats: png,csv,json (default: "png,csv")
  --dpi INT                       PNG resolution (default: 300)
```

## Output Files

Generated in `--output` directory:

### PNG Images
- **xrd_pattern.png** - XRD diffraction pattern (2θ vs. intensity)
- **total_scattering.png** - Total scattering S(Q) pattern
- **pdf_pattern.png** - Pair distribution function G(r) [if --include-pdf]

### CSV Data
- **xrd_peaks.csv** - Extracted peaks: 2θ, d-spacing, intensity
- **xrd_pattern.csv** - Full XRD pattern data
- **total_scattering.csv** - Q vs. S(Q) data

## Example: Graphite vs. Graphene

Compare two carbon structures:

```bash
# Graphene (single layer)
python -m carbon_xrd.cli generate-pattern \
  --cif tests/graphene.cif \
  --output ./results_graphene

# Graphite (layered structure)
python -m carbon_xrd.cli generate-pattern \
  --cif tests/graphite.cif \
  --output ./results_graphite \
  --include-pdf
```

The different XRD patterns reveal:
- **Graphene**: Broad peaks due to single-layer structure
- **Graphite**: Sharp peaks due to ordered layer stacking

## Testing

Run unit tests:

```bash
python -m pytest tests/test_carbon_xrd.py -v
```

Tests cover:
- CIF file validation and loading
- XRD pattern calculation
- Total scattering calculation
- CSV export functionality

## Project Structure

```
carbon_xrd/
├── src/carbon_xrd/
│   ├── __init__.py              # Package initialization
│   ├── cli.py                   # Command-line interface
│   ├── cif_validator.py         # CIF file validation
│   ├── xrd_calculator.py        # XRD pattern calculation
│   └── total_scattering.py      # Total scattering & PDF
├── tests/
│   ├── test_carbon_xrd.py       # Unit tests
│   ├── graphene.cif             # Test: graphene structure
│   └── graphite.cif             # Test: graphite structure
├── setup.py                     # Package configuration
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## How It Works

### 1. CIF Loading
- Parse crystallographic information from CIF files
- Validate atomic positions and lattice parameters using pymatgen

### 2. XRD Calculation
- Use pymatgen's XRDCalculator to compute X-ray diffraction
- Calculate peak positions from Bragg's law: d = λ / (2 sin θ)
- Normalize intensities to 0-100%

### 3. Total Scattering
- Simplified S(Q) using Debye scattering equation
- Pair distribution G(r) from atomic distance distributions
- Output in both reciprocal (Q) and real (r) space

### 4. Visualization
- matplotlib for high-quality plots (300 dpi)
- Formatted with labels, grids, and legends

## Limitations & Future Work

### Current Limitations
- Simplified total scattering calculation (Debye approximation)
- Does not account for thermal factors (Debye-Waller)
- Single wavelength per run

### Future Enhancements
- [ ] Full Pair Distribution Function (PDF) analysis
- [ ] Rietveld refinement integration
- [ ] Temperature-dependent calculations
- [ ] Multiple wavelengths (synchrotron data)
- [ ] Disorder/defect modeling
- [ ] Integration with Copilot App for UI

## Contributing

Contributions welcome! Please submit issues or PRs.

## License

MIT License - see LICENSE file for details

## Author

Carbon XRD Team  
makosaito3/Carbon_xrd

## References

- **pymatgen**: Structural and diffraction calculations
  - https://pymatgen.org/
- **CIF Format**: Crystallographic Information File
  - https://www.iucr.org/resources/cif/spec
- **X-ray Diffraction**: Bragg's law, peak indexing
  - https://en.wikipedia.org/wiki/X-ray_crystallography