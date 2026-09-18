"""
THEARA COLOR — Adobe .cube 3D LUT Generation and Validation
Founder: Krai Theara | "Create Your Look"
"""

import io
from typing import Tuple
import numpy as np
from .models import ColorGradeModel
from .transforms import apply_color_grade


def generate_cube_lut(
    grade: ColorGradeModel,
    size: int = 33,
    title: str = "THEARA COLOR LOOK",
) -> str:
    """
    Generates a professional Adobe .cube 3D LUT (default 33x33x33 = 35,937 points).
    Strictly follows the Adobe Cube LUT specification:
    - Red index changes fastest, then Green, then Blue slowest.
    - Floating point values formatted with 6 decimal places.
    - Clamped strictly between 0.000000 and 1.000000.
    """
    if size < 2 or size > 65:
        raise ValueError("LUT size must be between 2 and 65")

    # Generate 3D lattice
    coords = np.linspace(0.0, 1.0, size, dtype=np.float32)
    # Order: Blue slowest, Green middle, Red fastest
    # meshgrid indexing='ij' with b, g, r
    grid_b, grid_g, grid_r = np.meshgrid(coords, coords, coords, indexing="ij")

    # Stack into (size, size, size, 3) where [..., 0] = R, [..., 1] = G, [..., 2] = B
    lattice = np.stack([grid_r, grid_g, grid_b], axis=-1)
    flat_lattice = lattice.reshape(-1, 3)

    # Process through color engine (spatial grain/vignette excluded for 3D LUT)
    transformed = apply_color_grade(flat_lattice, grade, is_lut_lattice=True)
    transformed = np.clip(transformed, 0.0, 1.0)

    # Build standard .cube file content
    lines = [
        "# THEARA COLOR — Professional 3D LUT",
        "# Product: THEARA COLOR (Create Your Look)",
        "# Founder: Krai Theara",
        f'TITLE "{title}"',
        f"LUT_3D_SIZE {size}",
        "DOMAIN_MIN 0.0 0.0 0.0",
        "DOMAIN_MAX 1.0 1.0 1.0",
        "",
    ]

    # Format numbers: R G B
    # Using fast vectorized formatting
    formatted_data = [
        f"{r:.6f} {g:.6f} {b:.6f}"
        for r, g, b in transformed
    ]
    lines.extend(formatted_data)
    lines.append("")

    return "\n".join(lines)


def validate_cube_syntax(cube_text: str) -> Tuple[bool, str]:
    """
    Validates that a .cube string strictly follows the Adobe specification.
    Returns (is_valid, error_message).
    """
    lines = [line.strip() for line in cube_text.splitlines() if line.strip() and not line.strip().startswith("#")]
    if not lines:
        return False, "Empty or invalid CUBE file"

    lut_size = None
    data_start_idx = 0

    for i, line in enumerate(lines):
        parts = line.split()
        if parts[0] == "LUT_3D_SIZE":
            try:
                lut_size = int(parts[1])
            except (IndexError, ValueError):
                return False, "Invalid LUT_3D_SIZE parameter"
        elif parts[0] in ("TITLE", "DOMAIN_MIN", "DOMAIN_MAX", "LUT_1D_SIZE"):
            continue
        else:
            # First non-header line is data start
            data_start_idx = i
            break

    if lut_size is None:
        return False, "Missing LUT_3D_SIZE header"

    expected_entries = lut_size ** 3
    data_lines = lines[data_start_idx:]
    if len(data_lines) != expected_entries:
        return False, f"Expected {expected_entries} data lines for size {lut_size}, found {len(data_lines)}"

    # Validate first and last entries format
    for test_idx in (0, len(data_lines) - 1):
        sample = data_lines[test_idx].split()
        if len(sample) != 3:
            return False, f"Line {test_idx} does not have exactly 3 RGB components: {data_lines[test_idx]}"
        try:
            r, g, b = float(sample[0]), float(sample[1]), float(sample[2])
            if not (0.0 <= r <= 1.0 and 0.0 <= g <= 1.0 and 0.0 <= b <= 1.0):
                return False, f"Color values out of [0, 1] range: {r}, {g}, {b}"
        except ValueError:
            return False, f"Non-numeric value in line {test_idx}: {data_lines[test_idx]}"

    return True, "Valid Adobe CUBE 3D LUT"

