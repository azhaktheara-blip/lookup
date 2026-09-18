"""
THEARA COLOR — 8-Channel HSL Module
Founder: Krai Theara | "Create Your Look"
"""

import numpy as np
from .models import HSLSettings, HSLChannel


def _rgb_to_hsv(rgb: np.ndarray) -> np.ndarray:
    """Vectorized RGB [0..1] to HSV [H 0..360, S 0..1, V 0..1]"""
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    maxc = np.maximum(np.maximum(r, g), b)
    minc = np.minimum(np.minimum(r, g), b)
    v = maxc
    deltac = maxc - minc

    s = np.where(maxc != 0, deltac / (maxc + 1e-8), 0.0)

    # Hue calculation
    rc = np.where(deltac != 0, (maxc - r) / (deltac + 1e-8), 0.0)
    gc = np.where(deltac != 0, (maxc - g) / (deltac + 1e-8), 0.0)
    bc = np.where(deltac != 0, (maxc - b) / (deltac + 1e-8), 0.0)

    h = np.zeros_like(r)
    mask_r = (r == maxc) & (deltac != 0)
    mask_g = (g == maxc) & (deltac != 0) & (~mask_r)
    mask_b = (b == maxc) & (deltac != 0) & (~mask_r) & (~mask_g)

    h[mask_r] = (bc[mask_r] - gc[mask_r])
    h[mask_g] = 2.0 + (rc[mask_g] - bc[mask_g])
    h[mask_b] = 4.0 + (gc[mask_b] - rc[mask_b])

    h = (h / 6.0) % 1.0
    h_deg = h * 360.0

    return np.stack([h_deg, s, v], axis=-1)


def _hsv_to_rgb(hsv: np.ndarray) -> np.ndarray:
    """Vectorized HSV [H 0..360, S 0..1, V 0..1] to RGB [0..1]"""
    h_deg, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    h = (h_deg / 360.0) % 1.0

    i = np.floor(h * 6.0).astype(np.int32)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))

    i_mod = i % 6
    r = np.select([i_mod == 0, i_mod == 1, i_mod == 2, i_mod == 3, i_mod == 4, i_mod == 5], [v, q, p, p, t, v])
    g = np.select([i_mod == 0, i_mod == 1, i_mod == 2, i_mod == 3, i_mod == 4, i_mod == 5], [t, v, v, q, p, p])
    b = np.select([i_mod == 0, i_mod == 1, i_mod == 2, i_mod == 3, i_mod == 4, i_mod == 5], [p, p, t, v, v, q])

    return np.stack([r, g, b], axis=-1)


def _angular_dist(h: np.ndarray, target: float) -> np.ndarray:
    diff = np.abs(h - target) % 360.0
    return np.minimum(diff, 360.0 - diff)


def apply_hsl(rgb: np.ndarray, hsl_settings: HSLSettings) -> np.ndarray:
    """
    Applies 8-band HSL adjustments.
    Channels: Red(0°), Orange(30°), Yellow(60°), Green(120°), Aqua(180°), Blue(240°), Purple(285°), Magenta(330°)
    """
    channels = [
        ("red", 0.0, hsl_settings.red),
        ("orange", 30.0, hsl_settings.orange),
        ("yellow", 60.0, hsl_settings.yellow),
        ("green", 120.0, hsl_settings.green),
        ("aqua", 180.0, hsl_settings.aqua),
        ("blue", 240.0, hsl_settings.blue),
        ("purple", 285.0, hsl_settings.purple),
        ("magenta", 330.0, hsl_settings.magenta),
    ]

    # Check if all 0
    all_zero = True
    for _, _, ch in channels:
        if ch.hue != 0.0 or ch.saturation != 0.0 or ch.luminance != 0.0:
            all_zero = False
            break
    if all_zero:
        return rgb

    hsv = _rgb_to_hsv(rgb)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    h_delta = np.zeros_like(h)
    s_scale = np.zeros_like(s)
    v_scale = np.zeros_like(v)

    # Blend bandwidth per color (approx 30 deg half-width)
    bandwidth = 35.0

    for _, center_deg, ch in channels:
        if ch.hue == 0.0 and ch.saturation == 0.0 and ch.luminance == 0.0:
            continue
        dist = _angular_dist(h, center_deg)
        # Cosine bell weight
        weight = np.clip(1.0 - (dist / bandwidth), 0.0, 1.0)
        weight = 0.5 * (1.0 - np.cos(np.pi * weight)) * (s > 0.05)

        h_delta += weight * (ch.hue * 0.3)             # up to +-30 deg shift
        s_scale += weight * (ch.saturation / 100.0)    # up to +-100%
        v_scale += weight * (ch.luminance / 100.0)     # up to +-100%

    new_h = (h + h_delta) % 360.0
    new_s = np.clip(s * (1.0 + s_scale), 0.0, 1.0)
    new_v = np.clip(v * (1.0 + v_scale * 0.5), 0.0, 1.0)

    new_hsv = np.stack([new_h, new_s, new_v], axis=-1)
    return _hsv_to_rgb(new_hsv)

