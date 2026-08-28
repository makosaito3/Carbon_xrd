# Phase 2: Copilot Agent Development

## Overview

This folder contains the M365 Copilot declarative agent configuration for the Carbon XRD Structure Assistant.

## Files

- **declarativeAgent.json** - Agent manifest defining name, instructions, conversation starters, and capabilities
- **openapi.yaml** - OpenAPI 3.0 specification for the Carbon XRD API
- **DESIGN.md** - Detailed design documentation
- **README.md** - This file

## Architecture

```
┌─────────────────────────────────────┐
│  M365 Copilot Chat                  │
│  (User Interface)                   │
└──────────────┬──────────────────────┘
               │
       (Calls agent via LLM)
               │
┌──────────────▼──────────────────────┐
│  Carbon XRD Structure Assistant      │
│  (Declarative Agent)                │
│  - Interprets user description       │
│  - Generates CIF structures          │
│  - Orchestrates API calls            │
└──────────────┬──────────────────────┘
               │
      (HTTP API calls)
               │
┌──────────────▼──────────────────────┐
│  Carbon XRD API Server               │
│  (Flask, http://localhost:5000)     │
│  - /api/v1/generate-pattern (POST)  │
│  - /api/v1/structures (GET)         │
│  - /api/v1/info (GET)               │
│  - /health (GET)                     │
└──────────────┬──────────────────────┘
               │
       (Calls Python modules)
               │
┌──────────────▼──────────────────────┐
│  Carbon XRD CLI (Python)             │
│  - XRD calculation                   │
│  - Total scattering (S(Q))           │
│  - PDF calculation (G(r))            │
│  - Visualization (PNG)               │
│  - Data export (CSV)                 │
└─────────────────────────────────────┘
```

## Setup

### 1. Install Dependencies

```bash
cd Carbon_xrd
pip install -r requirements.txt
```

### 2. Start the API Server

```bash
# Set UTF-8 encoding (Windows)
$env:PYTHONIOENCODING = "utf-8"

# Run the Flask server
cd src
python -m carbon_xrd.api_server
```

Server will be available at `http://localhost:5000`

Test the server:
```bash
curl http://localhost:5000/health
```

### 3. Deploy to Copilot

**Option A: Using ATK CLI (Recommended)**

```bash
# Install M365 Agents Toolkit
npm install -g @microsoft/m365agentstoolkit-cli

# Navigate to this directory
cd copilot_agent

# Create and deploy the agent
atk new --name "Carbon XRD" --type "agent"
atk add action --api-plugin-type api-spec --openapi-spec-location ./openapi.yaml
atk provision --env local
```

**Option B: Manual Configuration**

1. Go to M365 Copilot admin console
2. Create new declarative agent
3. Upload `declarativeAgent.json`
4. Register API plugin using `openapi.yaml`
5. Test in Copilot Chat

## Testing the Agent

### Local Testing

Test the API endpoints directly:

```bash
# Get available structures
curl http://localhost:5000/api/v1/structures

# Generate graphene XRD
curl -X POST http://localhost:5000/api/v1/generate-pattern \
  -H "Content-Type: application/json" \
  -d '{
    "cif_content": "graphene",
    "include_pdf": false,
    "peak_threshold": 1.0
  }'
```

### In Copilot Chat

Once deployed, try these prompts:

1. **"Analyze graphene"**
   - Generates single-layer graphene XRD pattern
   - Shows peak positions and d-spacings

2. **"Compare graphite structures"**
   - Shows ordered (ABA) vs. turbostratic (random) patterns
   - Explains how disorder broadens peaks

3. **"My carbon has 15% defects"**
   - Generates pattern with defects
   - Interprets peak changes

4. **"Show me total scattering"**
   - Generates S(Q) and G(r) plots
   - Explains short-range order features

## Agent Instructions

The agent's instructions (in `declarativeAgent.json`) guide the LLM to:

1. **Listen** to user's material description
2. **Interpret** into crystallographic parameters
3. **Generate** CIF structures
4. **Call** the API to compute patterns
5. **Visualize** and interpret results

### Key Concepts Embedded

- **2θ angle**: X-ray scattering angle (higher → smaller d-spacing)
- **d-spacing**: Distance between atomic planes
- **Peak broadening**: Indicates disorder/defects/small crystallites
- **Total Scattering S(Q)**: Shows both long-range and short-range order
- **PDF G(r)**: Atomic pair distances (useful for amorphous materials)

## API Specification

See `openapi.yaml` for complete API details:

### POST /api/v1/generate-pattern

Generates XRD, total scattering, and optionally PDF patterns.

**Request:**
```json
{
  "cif_content": "graphene|graphite|<full CIF content>",
  "include_pdf": false,
  "peak_threshold": 1.0
}
```

**Response:**
```json
{
  "success": true,
  "structure_info": {
    "formula": "C2",
    "num_atoms": 2,
    "volume": 51.98,
    "density": 0.762,
    "lattice_params": {...}
  },
  "xrd_plot": "data:image/png;base64,...",
  "total_scattering_plot": "data:image/png;base64,...",
  "peaks_data": [...],
  "num_peaks": 2,
  "message": "Successfully generated patterns..."
}
```

### GET /api/v1/structures

List available sample structures.

**Response:**
```json
{
  "structures": [
    {
      "id": "graphene",
      "name": "Graphene (Single Layer)",
      "description": "Single-layer hexagonal carbon structure",
      "formula": "C2"
    },
    {
      "id": "graphite",
      "name": "Graphite (ABA Stacking)",
      "description": "Layered graphite with ordered ABA stacking",
      "formula": "C4"
    }
  ]
}
```

## Customization

### Adding New Structures

Add templates to `api_server.py` in the `create_sample_cif_from_description()` function:

```python
cif_templates = {
    "graphene": "...",
    "graphite": "...",
    "amorphous": "...",  # Add new structure
}
```

### Changing Instructions

Edit the `"instructions"` field in `declarativeAgent.json` to adjust:
- How the agent interprets user input
- What analyses to prioritize
- How to explain results

### Updating Conversation Starters

Modify `"conversationStarters"` array in `declarativeAgent.json` to add common user queries.

## Limitations & Future Work

### Current Limitations
- Simplified structure templates (graphene, graphite only)
- API server must run on localhost:5000
- No authentication/authorization yet
- Single wavelength (Cu Kα) only

### Future Enhancements
- [ ] Deploy API server to cloud (Azure, AWS)
- [ ] Add OAuth authentication
- [ ] Support multiple wavelengths (Mo Kα, synchrotron)
- [ ] Advanced CIF generation from user descriptions
- [ ] Integration with Materials Project database
- [ ] Machine learning for structure optimization
- [ ] Rietveld refinement capabilities

## Troubleshooting

### API Server Won't Start
```bash
# Check if port 5000 is in use
netstat -a -n -o | find "5000"

# Kill the process using port 5000
taskkill /PID <PID> /F

# Restart
python -m carbon_xrd.api_server
```

### Copilot Agent Not Responding
1. Check API server health: `curl http://localhost:5000/health`
2. Verify agent manifest JSON syntax
3. Check Copilot agent logs in admin console
4. Try a simpler prompt first (e.g., "Show me graphene")

### Pattern Generation Failed
1. Check API server error logs
2. Verify CIF syntax if using custom input
3. Check memory usage (large structures may need more resources)
4. Reduce peak_threshold value if no peaks detected

## References

- **M365 Agents Toolkit**: https://github.com/microsoft/m365agentstoolkit-cli
- **Declarative Agents**: https://learn.microsoft.com/copilot/platform/agent-declarative
- **OpenAPI Specification**: https://spec.openapis.org/
- **pymatgen Diffraction**: https://pymatgen.org/
- **CIF Format**: https://www.iucr.org/resources/cif/spec

## Support

For issues or questions:
- Check `DESIGN.md` for architectural details
- Review `../README.md` for CLI usage
- Open issue on GitHub: https://github.com/makosaito3/Carbon_xrd/issues
