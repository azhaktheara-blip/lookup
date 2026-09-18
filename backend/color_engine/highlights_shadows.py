"""
THEARA COLOR — Highlights and Shadows Tonal Control Module
Founder: Krai Theara | "Create Your Look"
"""

import numpy as np


def apply_highlights_shadows(rgb: np.ndarray, highlights: float, shadows: float) -> np.ndarray:
    """
    Adjusts highlights (-100 to +100) and shadows (-100 to +100).
    Uses luminance-based smooth-knee weighting.
    """
    if highlights == 0.0 and shadows == 0.0:
        return rgb

    # ITU-R BT.709 Luminance
    lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    lum = np.clip(lum, 0.0, 1.0)

    # Smooth shadow mask (1 at 0, 0 at 0.6)
    shadow_weight = np.clip((0.6 - lum) / 0.6, 0.0, 1.0)
    shadow_weight = shadow_weight * shadow_weight * (3.0 - 2.0 * shadow_weight)  # smoothstep

    # Smooth highlight mask (0 at 0.4, 1 at 1.0)
    highlight_weight = np.clip((lum - 0.4) / 0.6, 0.0, 1.0)
    highlight_weight = highlight_weight * highlight_weight * (3.0 - 2.0 * highlight_weight)

    s_gain = (shadows / 100.0) * 0.35      # Up to +-35%
    h_gain = (highlights / 100.0) * 0.35   # Up to +-35%

    if rgb.ndim == 3:
        shadow_weight = shadow_weight[..., np.newaxis]
        highlight_weight = highlight_weight[..., np.newaxis]
    elif rgb.ndim == 2:
        shadow_weight = shadow_weight[:, np.newaxis]
        highlight_weight = highlight_weight[:, np.newaxis]

    delta = (shadow_weight * s_gain) + (highlight_weight * h_gain)
    return rgb + delta

