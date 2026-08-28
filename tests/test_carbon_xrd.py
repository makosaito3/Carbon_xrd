"""Unit tests for Carbon XRD tool."""

import pytest
import sys
from pathlib import Path
import tempfile
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from carbon_xrd.cif_validator import CIFValidator
from carbon_xrd.xrd_calculator import XRDCalculator
from carbon_xrd.total_scattering import TotalScatteringCalculator


class TestCIFValidator:
    """Test CIF validation functionality."""

    def test_load_graphene_cif(self):
        """Test loading graphene CIF file."""
        cif_path = Path(__file__).parent / "graphene.cif"
        validator = CIFValidator()
        structure = validator.validate_and_load(str(cif_path))

        assert structure is not None
        assert len(structure) == 2
        assert "C" in structure.composition.elements[0].symbol

    def test_load_graphite_cif(self):
        """Test loading graphite CIF file."""
        cif_path = Path(__file__).parent / "graphite.cif"
        validator = CIFValidator()
        structure = validator.validate_and_load(str(cif_path))

        assert structure is not None
        assert len(structure) >= 1

    def test_invalid_cif_path(self):
        """Test error handling for invalid CIF path."""
        validator = CIFValidator()
        with pytest.raises(FileNotFoundError):
            validator.validate_and_load("nonexistent.cif")

    def test_get_structure_info(self):
        """Test extracting structure information."""
        cif_path = Path(__file__).parent / "graphene.cif"
        validator = CIFValidator()
        structure = validator.validate_and_load(str(cif_path))
        info = validator.get_structure_info(structure)

        assert "formula" in info
        assert "num_atoms" in info
        assert "volume" in info
        assert info["num_atoms"] == 2


class TestXRDCalculator:
    """Test XRD calculation functionality."""

    def test_calculate_xrd_pattern(self):
        """Test XRD pattern calculation."""
        cif_path = Path(__file__).parent / "graphene.cif"
        validator = CIFValidator()
        structure = validator.validate_and_load(str(cif_path))

        xrd = XRDCalculator()
        two_theta, intensity = xrd.calculate_pattern(structure)

        assert len(two_theta) > 0
        assert len(intensity) == len(two_theta)
        assert np.max(intensity) <= 100
        assert np.min(intensity) >= 0

    def test_extract_peaks(self):
        """Test peak extraction."""
        cif_path = Path(__file__).parent / "graphene.cif"
        validator = CIFValidator()
        structure = validator.validate_and_load(str(cif_path))

        xrd = XRDCalculator()
        two_theta, intensity = xrd.calculate_pattern(structure)
        peaks = xrd.extract_peaks(two_theta, intensity, threshold=1.0)

        assert len(peaks) > 0
        assert "2theta_deg" in peaks.columns
        assert "d_spacing_angstrom" in peaks.columns

    def test_export_csv(self):
        """Test CSV export functionality."""
        cif_path = Path(__file__).parent / "graphene.cif"
        validator = CIFValidator()
        structure = validator.validate_and_load(str(cif_path))

        xrd = XRDCalculator()
        two_theta, intensity = xrd.calculate_pattern(structure)
        xrd.extract_peaks(two_theta, intensity)

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "test.csv"
            xrd.export_peaks_csv(str(csv_path))
            assert csv_path.exists()


class TestTotalScatteringCalculator:
    """Test total scattering calculation functionality."""

    def test_calculate_structure_factor(self):
        """Test S(Q) calculation."""
        cif_path = Path(__file__).parent / "graphene.cif"
        validator = CIFValidator()
        structure = validator.validate_and_load(str(cif_path))

        ts = TotalScatteringCalculator()
        q, s_q = ts.calculate_structure_factor(structure)

        assert len(q) > 0
        assert len(s_q) == len(q)
        assert np.all(np.isfinite(s_q))

    def test_calculate_pdf(self):
        """Test PDF calculation."""
        cif_path = Path(__file__).parent / "graphene.cif"
        validator = CIFValidator()
        structure = validator.validate_and_load(str(cif_path))

        ts = TotalScatteringCalculator()
        r, g_r = ts.calculate_pdf(structure)

        assert len(r) > 0
        assert len(g_r) == len(r)
        assert np.all(np.isfinite(g_r))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
