"""Command-line interface for Carbon XRD tool."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .cif_validator import CIFValidator
from .xrd_calculator import XRDCalculator
from .total_scattering import TotalScatteringCalculator


def setup_output_dir(output_dir: str) -> Path:
    """
    Create output directory if it doesn't exist.

    Args:
        output_dir: Path to output directory

    Returns:
        Path object for output directory
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Carbon material structure to XRD/Total Scattering visualization tool"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # generate-pattern subcommand
    gen_parser = subparsers.add_parser(
        "generate-pattern", help="Generate XRD and total scattering patterns from CIF"
    )
    gen_parser.add_argument("--cif", required=True, help="Path to CIF file")
    gen_parser.add_argument(
        "--output",
        default="./results",
        help="Output directory (default: ./results)",
    )
    gen_parser.add_argument(
        "--wavelength",
        type=float,
        default=1.54184,
        help="X-ray wavelength in Angstrom (default: 1.54184 for Cu Kα)",
    )
    gen_parser.add_argument(
        "--xrd-range",
        type=str,
        default="5 120",
        help="2θ range as 'min max' (default: '5 120')",
    )
    gen_parser.add_argument(
        "--peak-threshold",
        type=float,
        default=1.0,
        help="Peak detection threshold in % (default: 1.0)",
    )
    gen_parser.add_argument(
        "--include-pdf",
        action="store_true",
        help="Include Pair Distribution Function",
    )
    gen_parser.add_argument(
        "--formats",
        type=str,
        default="png,csv",
        help="Output formats (png, csv, json) - default: 'png,csv'",
    )
    gen_parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="PNG DPI (default: 300)",
    )

    args = parser.parse_args()

    if args.command == "generate-pattern":
        generate_pattern(args)
    elif args.command is None:
        parser.print_help()
        sys.exit(0)
    else:
        parser.print_help()
        sys.exit(1)


def generate_pattern(args):
    """Generate XRD and total scattering patterns."""
    try:
        # Setup output directory
        output_dir = setup_output_dir(args.output)
        print(f"[OUTPUT] Output directory: {output_dir}")

        # Validate and load CIF
        print(f"[LOAD] Loading CIF: {args.cif}")
        validator = CIFValidator()
        structure = validator.validate_and_load(args.cif)
        print(f"[OK] Structure loaded successfully")

        # Print structure info
        info = validator.get_structure_info(structure)
        print(f"\n[INFO] Structure Information:")
        print(f"   Formula: {info['formula']}")
        print(f"   Atoms: {info['num_atoms']}")
        print(f"   Volume: {info['volume']:.2f} A^3")
        print(f"   Density: {info['density']:.3f} g/cm3")
        print(f"   Lattice: a={info['lattice_params']['a']:.3f}, "
              f"b={info['lattice_params']['b']:.3f}, "
              f"c={info['lattice_params']['c']:.3f} A")

        # Calculate XRD pattern
        print(f"\n[CALC] Calculating XRD pattern (wavelength: {args.wavelength} Å)...")
        xrd_calc = XRDCalculator(wavelength=args.wavelength)
        two_theta, intensity = xrd_calc.calculate_pattern(structure)

        # Extract peaks
        print(f"[PEAKS] Extracting peaks (threshold: {args.peak_threshold}%)...")
        peaks_df = xrd_calc.extract_peaks(two_theta, intensity, threshold=args.peak_threshold)
        print(f"[OK] Found {len(peaks_df)} peaks")

        # Plot XRD
        xrd_png = output_dir / "xrd_pattern.png"
        xrd_calc.plot_pattern(two_theta, intensity, str(xrd_png), dpi=args.dpi)

        # Calculate Total Scattering
        print(f"\n[CALC] Calculating total scattering pattern...")
        ts_calc = TotalScatteringCalculator(q_min=0.1, q_max=10.0)
        q, s_q = ts_calc.calculate_structure_factor(structure)

        # Plot Total Scattering
        ts_png = output_dir / "total_scattering.png"
        ts_calc.plot_scattering_pattern(q, s_q, str(ts_png), dpi=args.dpi)

        # Calculate and plot PDF if requested
        if args.include_pdf:
            print(f"[CALC] Calculating Pair Distribution Function...")
            r, g_r = ts_calc.calculate_pdf(structure)
            pdf_png = output_dir / "pdf_pattern.png"
            ts_calc.plot_pdf(r, g_r, str(pdf_png), dpi=args.dpi)

        # Export CSV files
        print(f"\n[SAVE] Exporting data files...")
        if "csv" in args.formats.lower():
            xrd_peaks_csv = output_dir / "xrd_peaks.csv"
            xrd_calc.export_peaks_csv(str(xrd_peaks_csv))

            xrd_full_csv = output_dir / "xrd_pattern.csv"
            xrd_calc.export_pattern_csv(two_theta, intensity, str(xrd_full_csv))

            ts_csv = output_dir / "total_scattering.csv"
            ts_calc.export_csv(q, s_q, str(ts_csv))

        print(f"\n[SUCCESS] Pattern generation completed successfully!")
        print(f"[PATH] All output files saved to: {output_dir}")

    except FileNotFoundError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"[ERROR] Validation error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
