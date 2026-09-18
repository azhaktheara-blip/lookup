"""
THEARA COLOR — 3-Way Color Wheels Module (Lift, Gamma, Gain)
Founder: Krai Theara | "Create Your Look"
"""

import numpy as np
from .models import ColorWheelsSettings, ColorWheel


def _wheel_to_rgb(wheel: ColorWheel) -> np.ndarray:
    """Converts wheel (hue deg, saturation [0..1], luminance [-1..1]) to RGB delta."""
    if wheel.saturation == 0.0 and wheel.luminance == 0.0:
        return np.array([0.0, 0.0, 0.0], dtype=np.float32)

    h_rad = np.radians(wheel.hue)
    # Chromatic shift vectors
    r = wheel.saturation * np.cos(h_rad)
    g = wheel.saturation * np.cos(h_rad - 2.0 * np.pi / 3.0)
    b = wheel.saturation * np.cos(h_rad + 2.0 * np.pi / 3.0)

    # Add master luminance offset
    lum_offset = wheel.luminance * 0.2
    return np.array([r + lum_offset, g + lum_offset, b + lum_offset], dtype=np.float32)


def apply_color_wheels(rgb: np.ndarray, wheels: ColorWheelsSettings) -> np.ndarray:
    """
    Applies 3-way color grading:
    - Lift (Shadows): weight = (1 - Y)^2
    - Gamma (Midtones): weight = 4 * Y * (1 - Y)
    - Gain (Highlights): weight = Y^2
    """
    lift_rgb = _wheel_to_rgb(wheels.lift)
    gamma_rgb = _wheel_to_rgb(wheels.gamma)
    gain_rgb = _wheel_to_rgb(wheels.gain)

    if np.all(lift_rgb == 0.0) and np.all(gamma_rgb == 0.0) and np.all(gain_rgb == 0.0):
        return rgb

    # Luminance Y
    lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    lum = np.clip(lum, 0.0, 1.0)

    # Tonal weights
    w_lift = np.power(1.0 - lum, 2.0)
    w_gamma = 4.0 * lum * (1.0 - lum)
    w_gain = np.power(lum, 2.0)

    if rgb.ndim == 3:
        w_lift = w_lift[..., np.newaxis]
        w_gamma = w_gamma[..., np.newaxis]
        w_gain = w_gain[..., np.newaxis]
    elif rgb.ndim == 2:
        w_lift = w_lift[:, np.newaxis]
        w_gamma = w_gamma[:, np.newaxis]
        w_gain = w_gain[:, np.newaxis]

    delta = (w_lift * lift_rgb * 0.4) + (w_gamma * gamma_rgb * 0.4) + (w_gain * gain_rgb * 0.4)
    return rgb + delta

