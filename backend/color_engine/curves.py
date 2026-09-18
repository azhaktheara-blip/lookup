"""
THEARA COLOR — Tone Curves Module (RGB & Luminance Splines)
Founder: Krai Theara | "Create Your Look"
"""

from typing import List
import numpy as np
from scipy.interpolate import PchipInterpolator
from .models import CurveSettings, CurvePoint


def _build_lut_from_points(points: List[CurvePoint], lut_size: int = 1024) -> np.ndarray:
    """
    Builds a 1D lookup table of size `lut_size` from a list of CurvePoint(x, y)
    using PCHIP (Piecewise Cubic Hermite Interpolating Polynomial) to guarantee monotonicity.
    """
    if len(points) < 2:
        return np.linspace(0.0, 1.0, lut_size, dtype=np.float32)

    # Sort points by x
    sorted_pts = sorted(points, key=lambda p: p.x)
    xs = [p.x for p in sorted_pts]
    ys = [p.y for p in sorted_pts]

    # Ensure endpoints 0.0 and 1.0 exist
    if xs[0] > 0.0:
        xs.insert(0, 0.0)
        ys.insert(0, ys[0])
    if xs[-1] < 1.0:
        xs.append(1.0)
        ys.append(ys[-1])

    # Deduplicate consecutive xs
    unique_xs = [xs[0]]
    unique_ys = [ys[0]]
    for i in range(1, len(xs)):
        if xs[i] > unique_xs[-1] + 1e-6:
            unique_xs.append(xs[i])
            unique_ys.append(ys[i])

    if len(unique_xs) < 2:
        return np.linspace(0.0, 1.0, lut_size, dtype=np.float32)

    interpolator = PchipInterpolator(unique_xs, unique_ys, extrapolate=True)
    grid_x = np.linspace(0.0, 1.0, lut_size, dtype=np.float32)
    eval_y = interpolator(grid_x)
    return np.clip(eval_y, 0.0, 1.0).astype(np.float32)


def apply_curves(rgb: np.ndarray, curve_settings: CurveSettings) -> np.ndarray:
    """
    Applies Master, Red, Green, and Blue curves using 1024-point PCHIP LUTs.
    """
    is_identity = (
        len(curve_settings.master) <= 2 and curve_settings.master[0].y == 0.0 and curve_settings.master[-1].y == 1.0
        and len(curve_settings.red) <= 2 and curve_settings.red[0].y == 0.0 and curve_settings.red[-1].y == 1.0
        and len(curve_settings.green) <= 2 and curve_settings.green[0].y == 0.0 and curve_settings.green[-1].y == 1.0
        and len(curve_settings.blue) <= 2 and curve_settings.blue[0].y == 0.0 and curve_settings.blue[-1].y == 1.0
    )
    if is_identity:
        return rgb

    lut_m = _build_lut_from_points(curve_settings.master)
    lut_r = _build_lut_from_points(curve_settings.red)
    lut_g = _build_lut_from_points(curve_settings.green)
    lut_b = _build_lut_from_points(curve_settings.blue)

    # Fast 1D index mapping: index = clip(val * 1023, 0, 1023)
    def map_channel(vals: np.ndarray, lut: np.ndarray) -> np.ndarray:
        idx = np.clip(np.round(vals * 1023.0).astype(np.int32), 0, 1023)
        return lut[idx]

    result = rgb.copy()
    # Apply individual color curves
    result[..., 0] = map_channel(result[..., 0], lut_r)
    result[..., 1] = map_channel(result[..., 1], lut_g)
    result[..., 2] = map_channel(result[..., 2], lut_b)

    # Apply master curve to all channels
    result[..., 0] = map_channel(result[..., 0], lut_m)
    result[..., 1] = map_channel(result[..., 1], lut_m)
    result[..., 2] = map_channel(result[..., 2], lut_m)

    return result

