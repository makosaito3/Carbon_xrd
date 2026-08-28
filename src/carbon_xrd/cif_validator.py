"""CIF file validator and parser."""

import os
from pathlib import Path
from typing import Optional
from pymatgen.core import Structure


class CIFValidator:
    """Validates and loads CIF files."""

    def __init__(self):
        """Initialize CIF validator."""
        pass

    def validate_and_load(self, cif_path: str) -> Optional[Structure]:
        """
        Validate CIF file and load as pymatgen Structure.

        Args:
            cif_path: Path to CIF file

        Returns:
            pymatgen.core.Structure object or None if validation fails

        Raises:
            FileNotFoundError: If CIF file does not exist
            ValueError: If CIF file is invalid or cannot be parsed
        """
        cif_path = Path(cif_path)

        # Check file existence
        if not cif_path.exists():
            raise FileNotFoundError(f"CIF file not found: {cif_path}")

        # Check file extension
        if cif_path.suffix.lower() != ".cif":
            raise ValueError(f"File must have .cif extension: {cif_path}")

        try:
            # Load structure using pymatgen
            structure = Structure.from_file(str(cif_path))

            # Validate basic structure properties
            if len(structure) == 0:
                raise ValueError("Structure contains no atoms")

            return structure

        except Exception as e:
            raise ValueError(f"Failed to parse CIF file: {str(e)}")

    def get_structure_info(self, structure: Structure) -> dict:
        """
        Get basic information about the structure.

        Args:
            structure: pymatgen Structure object

        Returns:
            Dictionary with structure information
        """
        return {
            "formula": structure.composition.formula,
            "num_atoms": len(structure),
            "volume": structure.volume,
            "density": structure.density,
            "lattice_params": {
                "a": structure.lattice.a,
                "b": structure.lattice.b,
                "c": structure.lattice.c,
                "alpha": structure.lattice.alpha,
                "beta": structure.lattice.beta,
                "gamma": structure.lattice.gamma,
            },
        }
