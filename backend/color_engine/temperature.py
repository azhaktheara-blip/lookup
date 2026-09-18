"""
THEARA COLOR — Temperature and White Balance Module
Founder: Krai Theara | "Create Your Look"
"""

import numpy as np


def apply_temperature_and_tint(rgb: np.ndarray, temp: float, tint: float) -> np.ndarray:
    """
    Adjusts color temperature (-100 to +100) and tint (-100 to +100).
    - Positive temp = warmer (more red, less blue)
    - Negative temp = cooler (more blue, less red)
    - Positive tint = magenta (more red & blue, less green)
    - Negative tint = green (more green, less red & blue)
    """
    if temp == 0.0 and tint == 0.0:
        return rgb

    t_norm = temp / 100.0  # -1.0 to +1.0
    ti_norm = tint / 100.0  # -1.0 to +1.0

    # Red channel gain
    r_gain = 1.0 + (t_norm * 0.25) + (ti_norm * 0.15)
    # Green channel gain
    g_gain = 1.0 - (ti_norm * 0.25)
    # Blue channel gain
    b_gain = 1.0 - (t_norm * 0.25) + (ti_norm * 0.15)

    result = rgb.copy()
    result[..., 0] *= r_gain
    result[..., 1] *= g_gain
    result[..., 2] *= b_gain

    return result

