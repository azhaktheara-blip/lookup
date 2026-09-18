"""
THEARA COLOR — Film Effects Module (Fade, Vignette, Grain)
Founder: Krai Theara | "Create Your Look"
"""

import numpy as np


def apply_fade(rgb: np.ndarray, fade: float) -> np.ndarray:
    """
    Lifts black levels for a vintage matte film aesthetic.
    Fade: 0 to 100
    """
    if fade <= 0.0:
        return rgb
    lift = (fade / 100.0) * 0.18  # up to 18% black lift
    return lift + rgb * (1.0 - lift)


def apply_vignette(rgb: np.ndarray, vignette: float) -> np.ndarray:
    """
    Applies radial cosine vignette falloff.
    Vignette: -100 (white/light) to +100 (dark)
    Only applicable to 2D image frames (H, W, 3).
    """
    if vignette == 0.0 or rgb.ndim != 3:
        return rgb

    h, w = rgb.shape[:2]
    y = np.linspace(-1.0, 1.0, h, dtype=np.float32)
    x = np.linspace(-1.0, 1.0, w, dtype=np.float32)
    xx, yy = np.meshgrid(x, y)

    # Normalized radius from center
    radius = np.sqrt(xx * xx + yy * yy)
    # Cosine falloff starting from radius 0.5 to 1.4
    falloff = np.clip((radius - 0.4) / 1.0, 0.0, 1.0)
    falloff = 0.5 * (1.0 - np.cos(np.pi * falloff))

    strength = (vignette / 100.0) * 0.6
    # If positive: darken edges. If negative: lighten edges
    vignette_mask = 1.0 - (strength * falloff[..., np.newaxis])
    return rgb * np.clip(vignette_mask, 0.0, 2.0)


def apply_grain(rgb: np.ndarray, grain: float, seed: int = 42) -> np.ndarray:
    """
    Simulates organic silver halide film grain noise.
    More visible in midtones, less in pure shadows and highlights.
    Grain: 0 to 100
    Only applicable to 2D image frames (H, W, 3).
    """
    if grain <= 0.0 or rgb.ndim != 3:
        return rgb

    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, 1.0, rgb.shape).astype(np.float32)

    lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    # Midtone bell curve: 4 * lum * (1 - lum)
    mid_weight = 4.0 * lum * (1.0 - lum)
    mid_weight = np.clip(mid_weight, 0.0, 1.0)[..., np.newaxis]

    strength = (grain / 100.0) * 0.12  # up to 12% noise
    return rgb + (noise * strength * mid_weight)

