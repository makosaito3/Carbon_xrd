"""Total scattering pattern calculator."""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import Tuple
from pymatgen.core import Structure


class TotalScatteringCalculator:
    """Calculate and generate total scattering patterns (S(Q)) from structures."""

    def __init__(self, q_min: float = 0.1, q_max: float = 10.0):
        """
        Initialize Total Scattering Calculator.

        Args:
            q_min: Minimum Q value (Å⁻¹)
            q_max: Maximum Q value (Å⁻¹)
        """
        self.q_min = q_min
        self.q_max = q_max
        self.pattern = None
        self.q_values = None
        self.s_q = None

    def calculate_structure_factor(
        self, structure: Structure, num_points: int = 500
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate S(Q) - total scattering structure factor.

        This is a simplified calculation using the Debye scattering equation.

        Args:
            structure: pymatgen Structure object
            num_points: Number of Q points to calculate

        Returns:
            Tuple of (Q values, S(Q) values)
        """
        # Generate Q array
        q = np.linspace(self.q_min, self.q_max, num_points)

        # Get atomic positions and types
        positions = structure.cart_coords
        species = structure.species

        # Simplified S(Q) calculation using Debye equation
        # S(Q) = sum_i sum_j f_i(Q) * f_j(Q) * sin(Q * r_ij) / (Q * r_ij)
        # For simplicity, we use a Gaussian model

        s_q = np.ones_like(q)

        # Calculate pair distribution contributions
        n_atoms = len(structure)
        for i in range(n_atoms):
            for j in range(i + 1, n_atoms):
                r_ij = np.linalg.norm(positions[i] - positions[j])
                # Gaussian peak in Q space
                s_q += 2 * np.exp(-(q * r_ij / np.pi) ** 2)

        # Normalize
        s_q = s_q / n_atoms

        self.q_values = q
        self.s_q = s_q
        self.pattern = (q, s_q)

        return q, s_q

    def calculate_pdf(
        self, structure: Structure, r_max: float = 30.0, num_points: int = 300
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate G(r) - Pair Distribution Function.

        Args:
            structure: pymatgen Structure object
            r_max: Maximum r value (Å)
            num_points: Number of r points

        Returns:
            Tuple of (r values, G(r) values)
        """
        r = np.linspace(0.1, r_max, num_points)
        g_r = np.zeros_like(r)

        # Get atomic positions
        positions = structure.cart_coords
        n_atoms = len(structure)

        # Calculate all pairwise distances
        for i in range(n_atoms):
            for j in range(i + 1, n_atoms):
                r_ij = np.linalg.norm(positions[i] - positions[j])
                # Gaussian peak at each distance
                g_r += 2 * np.exp(-((r - r_ij) ** 2) / 0.1)

        # Normalize
        g_r = g_r / n_atoms

        return r, g_r

    def plot_scattering_pattern(
        self,
        q: np.ndarray,
        s_q: np.ndarray,
        output_path: str = "total_scattering.png",
        dpi: int = 300,
        figsize: Tuple[float, float] = (12, 6),
    ) -> None:
        """
        Plot total scattering pattern and save as PNG.

        Args:
            q: Q values (Å⁻¹)
            s_q: S(Q) values
            output_path: Output PNG file path
            dpi: DPI for output image
            figsize: Figure size (width, height) in inches
        """
        fig, ax = plt.subplots(figsize=figsize, dpi=100)

        # Plot pattern
        ax.plot(q, s_q, "r-", linewidth=1.5, label="S(Q)")
        ax.fill_between(q, s_q, alpha=0.3, color="red")

        # Formatting
        ax.set_xlabel("Q (Å⁻¹)", fontsize=12, fontweight="bold")
        ax.set_ylabel("S(Q)", fontsize=12, fontweight="bold")
        ax.set_title("Total Scattering Structure Factor S(Q)", fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.legend(fontsize=10)

        # Save with specified DPI
        plt.savefig(output_path, dpi=dpi, bbox_inches="tight")
        plt.close()

        print(f"[OK] Total scattering pattern saved: {output_path}")

    def plot_pdf(
        self,
        r: np.ndarray,
        g_r: np.ndarray,
        output_path: str = "pdf_pattern.png",
        dpi: int = 300,
        figsize: Tuple[float, float] = (12, 6),
    ) -> None:
        """
        Plot Pair Distribution Function and save as PNG.

        Args:
            r: r values (Å)
            g_r: G(r) values
            output_path: Output PNG file path
            dpi: DPI for output image
            figsize: Figure size (width, height) in inches
        """
        fig, ax = plt.subplots(figsize=figsize, dpi=100)

        # Plot pattern
        ax.plot(r, g_r, "g-", linewidth=1.5, label="G(r)")
        ax.fill_between(r, g_r, alpha=0.3, color="green")

        # Formatting
        ax.set_xlabel("r (Å)", fontsize=12, fontweight="bold")
        ax.set_ylabel("G(r)", fontsize=12, fontweight="bold")
        ax.set_title("Pair Distribution Function G(r)", fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.legend(fontsize=10)

        # Save with specified DPI
        plt.savefig(output_path, dpi=dpi, bbox_inches="tight")
        plt.close()

        print(f"[OK] PDF pattern saved: {output_path}")

    def export_csv(
        self,
        q: np.ndarray,
        s_q: np.ndarray,
        output_path: str = "total_scattering.csv",
    ) -> None:
        """
        Export S(Q) data to CSV.

        Args:
            q: Q values
            s_q: S(Q) values
            output_path: Output CSV file path
        """
        df = pd.DataFrame({
            "Q_inv_angstrom": q,
            "S_Q": s_q,
        })
        df.to_csv(output_path, index=False)
        print(f"[OK] S(Q) data saved: {output_path}")
