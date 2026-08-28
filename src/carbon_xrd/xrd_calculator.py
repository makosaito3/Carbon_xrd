"""XRD pattern calculator using pymatgen."""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from typing import Tuple, List, Dict
from pymatgen.core import Structure
from pymatgen.analysis.diffraction.xrd import XRDCalculator as PymatgenXRDCalculator


class XRDCalculator:
    """Calculate and generate XRD patterns from crystal structures."""

    def __init__(self, wavelength: float = 1.54184):
        """
        Initialize XRD Calculator.

        Args:
            wavelength: X-ray wavelength in Angstrom (default: Cu Kα, 1.54184)
        """
        self.wavelength = wavelength
        self.calculator = PymatgenXRDCalculator(wavelength=wavelength)
        self.pattern = None
        self.peaks = None

    def calculate_pattern(self, structure: Structure) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate XRD pattern for the given structure.

        Args:
            structure: pymatgen Structure object

        Returns:
            Tuple of (2theta angles, intensities)
        """
        # Get XRD pattern
        pattern = self.calculator.get_pattern(structure)

        # Extract theta and intensity
        two_theta = pattern.x
        intensity = pattern.y

        # Normalize intensity to 100
        intensity_normalized = (intensity / np.max(intensity)) * 100

        self.pattern = (two_theta, intensity_normalized)

        return two_theta, intensity_normalized

    def extract_peaks(
        self, two_theta: np.ndarray, intensity: np.ndarray, threshold: float = 1.0
    ) -> pd.DataFrame:
        """
        Extract peak information from XRD pattern.

        Args:
            two_theta: 2theta angles
            intensity: Intensities
            threshold: Relative intensity threshold (%) for peak detection

        Returns:
            DataFrame with peak information
        """
        # Find local maxima
        peaks_idx = []
        for i in range(1, len(intensity) - 1):
            if intensity[i] > intensity[i - 1] and intensity[i] > intensity[i + 1]:
                if intensity[i] >= threshold:
                    peaks_idx.append(i)

        # Extract peak data
        peaks_data = []
        for idx in peaks_idx:
            two_theta_val = two_theta[idx]
            intensity_val = intensity[idx]
            # Calculate d-spacing using Bragg's law: d = λ / (2 * sin(θ))
            d_spacing = self.wavelength / (2 * np.sin(np.radians(two_theta_val / 2)))

            peaks_data.append({
                "2theta_deg": round(two_theta_val, 3),
                "intensity_percent": round(intensity_val, 2),
                "d_spacing_angstrom": round(d_spacing, 4),
            })

        peaks_df = pd.DataFrame(peaks_data)
        self.peaks = peaks_df

        return peaks_df

    def plot_pattern(
        self,
        two_theta: np.ndarray,
        intensity: np.ndarray,
        output_path: str = "xrd_pattern.png",
        dpi: int = 300,
        figsize: Tuple[float, float] = (12, 6),
    ) -> None:
        """
        Plot XRD pattern and save as PNG.

        Args:
            two_theta: 2theta angles
            intensity: Intensities
            output_path: Output PNG file path
            dpi: DPI for output image
            figsize: Figure size (width, height) in inches
        """
        fig, ax = plt.subplots(figsize=figsize, dpi=100)

        # Plot pattern
        ax.plot(two_theta, intensity, "b-", linewidth=1.5, label="XRD Pattern")
        ax.fill_between(two_theta, intensity, alpha=0.3)

        # Formatting
        ax.set_xlabel("2θ (degrees)", fontsize=12, fontweight="bold")
        ax.set_ylabel("Intensity (%)", fontsize=12, fontweight="bold")
        ax.set_title("X-ray Diffraction Pattern", fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.legend(fontsize=10)

        # Set reasonable x-axis limits
        ax.set_xlim(0, 120)
        ax.set_ylim(0, 110)

        # Save with specified DPI
        plt.savefig(output_path, dpi=dpi, bbox_inches="tight")
        plt.close()

        print(f"[OK] XRD pattern saved: {output_path}")

    def export_peaks_csv(self, output_path: str = "xrd_peaks.csv") -> None:
        """
        Export peak data to CSV.

        Args:
            output_path: Output CSV file path
        """
        if self.peaks is None:
            raise ValueError("No peaks extracted. Call extract_peaks() first.")

        self.peaks.to_csv(output_path, index=False)
        print(f"[OK] Peak data saved: {output_path}")

    def export_pattern_csv(
        self,
        two_theta: np.ndarray,
        intensity: np.ndarray,
        output_path: str = "xrd_pattern.csv",
    ) -> None:
        """
        Export full pattern data to CSV.

        Args:
            two_theta: 2theta angles
            intensity: Intensities
            output_path: Output CSV file path
        """
        df = pd.DataFrame({
            "2theta_deg": two_theta,
            "intensity_percent": intensity,
        })
        df.to_csv(output_path, index=False)
        print(f"[OK] Full pattern data saved: {output_path}")
