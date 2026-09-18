"""
THEARA COLOR — Exposure, Contrast & Tone Mapping Module
Founder: Krai Theara | "Create Your Look"
"""

import numpy as np


def apply_exposure(rgb: np.ndarray, exposure_ev: float) -> np.ndarray:
    """
    Applies photographic exposure in EV stops.
    Formula: I_out = I_in * 2^(exposure)
    """
    if exposure_ev == 0.0:
        return rgb
    scale = float(2.0 ** exposure_ev)
    return rgb * scale


def apply_contrast(rgb: np.ndarray, contrast_val: float) -> np.ndarray:
    """
    Applies S-curve contrast centered at mid-gray 0.5.
    Range: -100 to +100
    """
    if contrast_val == 0.0:
        return rgb

    # Map -100..100 to slope factor 0.3..2.5
    factor = (contrast_val + 100.0) / 100.0
    if factor < 0.01:
        factor = 0.01

    # S-curve approximation using power function around 0.5
    # For positive contrast: steepen around 0.5
    # For negative contrast: flatten towards 0.5
    mid = 0.5
    result = np.where(
        rgb <= mid,
        mid * np.power(np.maximum(rgb / mid, 0.0), factor),
        1.0 - (1.0 - mid) * np.power(np.maximum((1.0 - rgb) / (1.0 - mid), 0.0), factor),
    )
    return result


def apply_whites_blacks(rgb: np.ndarray, whites: float, blacks: float) -> np.ndarray:
    """
    Adjusts white and black clipping thresholds.
    Whites (-100 to +100), Blacks (-100 to +100)
    """
    if whites == 0.0 and blacks == 0.0:
        return rgb

    w_shift = whites * 0.002   # up to +-0.2
    b_shift = blacks * 0.002   # up to +-0.2

    # Black point shift in shadows
    # White point shift in highlights
    result = rgb.copy()
    if b_shift != 0.0:
        # Affects values < 0.4
        shadow_weight = np.clip((0.4 - rgb) / 0.4, 0.0, 1.0)
        result += b_shift * shadow_weight

    if w_shift != 0.0:
        # Affects values > 0.6
        highlight_weight = np.clip((rgb - 0.6) / 0.4, 0.0, 1.0)
        result += w_shift * highlight_weight

    return result

