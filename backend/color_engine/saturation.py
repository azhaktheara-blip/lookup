"""
THEARA COLOR — Saturation and Vibrance Module
Founder: Krai Theara | "Create Your Look"
"""

import numpy as np


def apply_saturation_vibrance(rgb: np.ndarray, saturation: float, vibrance: float) -> np.ndarray:
    """
    Applies master saturation (-100 to +100) and smart vibrance (-100 to +100).
    Vibrance selectively boosts less saturated colors more, protecting skin tones.
    """
    if saturation == 0.0 and vibrance == 0.0:
        return rgb

    # Luminance
    lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    if rgb.ndim == 3:
        lum_expanded = lum[..., np.newaxis]
    else:
        lum_expanded = lum[:, np.newaxis]

    # Current saturation approximation: max(RGB) - min(RGB)
    c_max = np.max(rgb, axis=-1, keepdims=True)
    c_min = np.min(rgb, axis=-1, keepdims=True)
    current_sat = np.clip(c_max - c_min, 0.0, 1.0)

    # Master Saturation factor: -100 -> 0.0, 0 -> 1.0, 100 -> 2.0
    sat_factor = (saturation + 100.0) / 100.0

    # Vibrance factor: boosts lower saturated pixels more
    vib_norm = vibrance / 100.0
    # Inverse saturation weight: high for pastel/desaturated pixels
    vib_weight = (1.0 - current_sat) * vib_norm

    total_scale = np.maximum(0.0, sat_factor + vib_weight)

    # Blend between monochrome luminance and original color
    graded = lum_expanded + (rgb - lum_expanded) * total_scale
    return graded

