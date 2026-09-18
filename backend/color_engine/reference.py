"""
THEARA COLOR — Reference Image Statistical Color Matching & Extraction
Founder: Krai Theara | "Create Your Look"
"""

from typing import Tuple, List
import numpy as np
from PIL import Image
from .models import ColorGradeModel, LookDNA, ColorWheel


def _rgb_to_lab(rgb: np.ndarray) -> np.ndarray:
    """
    Converts RGB [0..1] to CIE L*a*b* (D65 illuminant standard).
    """
    # Inverse sRGB companding to linear RGB
    mask = rgb > 0.04045
    linear = np.where(mask, np.power((rgb + 0.055) / 1.055, 2.4), rgb / 12.92)

    # Convert to CIE XYZ
    # Matrix for sRGB D65
    m = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ], dtype=np.float32)

    xyz = np.dot(linear, m.T)

    # Reference white D65
    xyz_ref = np.array([0.95047, 1.00000, 1.08883], dtype=np.float32)
    normalized = xyz / xyz_ref

    epsilon = 0.008856
    kappa = 903.3
    f = np.where(normalized > epsilon, np.cbrt(normalized), (kappa * normalized + 16.0) / 116.0)

    l_star = (116.0 * f[..., 1]) - 16.0
    a_star = 500.0 * (f[..., 0] - f[..., 1])
    b_star = 200.0 * (f[..., 1] - f[..., 2])

    return np.stack([l_star, a_star, b_star], axis=-1)


def _extract_dominant_palette(img: Image.Image, num_colors: int = 5) -> List[str]:
    """Extracts top dominant colors as HEX strings."""
    # Resize small for fast quantization
    small = img.resize((50, 50)).convert("RGB")
    paletted = small.quantize(colors=num_colors, method=Image.Quantize.MEDIANCUT)
    palette = paletted.getpalette()[: num_colors * 3]
    hex_colors = []
    for i in range(0, len(palette), 3):
        r, g, b = palette[i], palette[i + 1], palette[i + 2]
        hex_colors.append(f"#{r:02x}{g:02x}{b:02x}")
    return hex_colors


def analyze_reference_match(
    original_img: Image.Image,
    reference_img: Image.Image,
) -> Tuple[ColorGradeModel, LookDNA]:
    """
    Analyzes visual differences between original and reference images,
    calculates statistical colorimetric differentials, and synthesizes
    a deterministic ColorGradeModel and LookDNA to match the reference look.
    """
    # Downsample for fast analysis
    orig_small = original_img.resize((128, 128)).convert("RGB")
    ref_small = reference_img.resize((128, 128)).convert("RGB")

    arr_orig = np.array(orig_small, dtype=np.float32) / 255.0
    arr_ref = np.array(ref_small, dtype=np.float32) / 255.0

    lab_orig = _rgb_to_lab(arr_orig)
    lab_ref = _rgb_to_lab(arr_ref)

    # Statistical moments
    mean_orig = np.mean(lab_orig, axis=(0, 1))
    std_orig = np.std(lab_orig, axis=(0, 1)) + 1e-6

    mean_ref = np.mean(lab_ref, axis=(0, 1))
    std_ref = np.std(lab_ref, axis=(0, 1)) + 1e-6

    # 1. Exposure shift (from L* differential)
    # L* range 0..100. 1 EV approx 15 units of L* in midtones
    l_diff = mean_ref[0] - mean_orig[0]
    exposure = float(np.clip(l_diff / 25.0, -2.5, 2.5))

    # 2. Contrast shift (from L* standard deviation ratio)
    std_ratio = std_ref[0] / std_orig[0]
    contrast = float(np.clip((std_ratio - 1.0) * 50.0, -50.0, 50.0))

    # 3. Temperature & Tint (b* = yellow/blue, a* = magenta/green)
    b_diff = mean_ref[2] - mean_orig[2]
    a_diff = mean_ref[1] - mean_orig[1]
    temperature = float(np.clip(b_diff * 2.0, -60.0, 60.0))
    tint = float(np.clip(a_diff * 2.0, -60.0, 60.0))

    # 4. Saturation (Chroma ratio: sqrt(a^2 + b^2))
    chroma_orig = np.mean(np.sqrt(lab_orig[..., 1]**2 + lab_orig[..., 2]**2))
    chroma_ref = np.mean(np.sqrt(lab_ref[..., 1]**2 + lab_ref[..., 2]**2))
    chroma_ratio = chroma_ref / (chroma_orig + 1e-6)
    saturation = float(np.clip((chroma_ratio - 1.0) * 60.0, -60.0, 60.0))

    # 5. Highlights and Shadows
    # Lum percentiles
    p10_orig, p90_orig = np.percentile(lab_orig[..., 0], [10, 90])
    p10_ref, p90_ref = np.percentile(lab_ref[..., 0], [10, 90])

    shadows = float(np.clip((p10_ref - p10_orig) * 1.5, -40.0, 40.0))
    highlights = float(np.clip((p90_ref - p90_orig) * 1.5, -40.0, 40.0))

    # 6. Color Wheels (Lift for shadows < 30% L*, Gain for highlights > 70% L*)
    shadow_mask = lab_ref[..., 0] < 30.0
    highlight_mask = lab_ref[..., 0] > 70.0

    lift_wheel = ColorWheel()
    if np.sum(shadow_mask) > 10:
        s_a = np.mean(lab_ref[shadow_mask, 1])
        s_b = np.mean(lab_ref[shadow_mask, 2])
        hue_rad = np.arctan2(s_b, s_a)
        lift_wheel.hue = float((np.degrees(hue_rad)) % 360.0)
        lift_wheel.saturation = float(np.clip(np.sqrt(s_a**2 + s_b**2) / 60.0, 0.0, 0.5))

    gain_wheel = ColorWheel()
    if np.sum(highlight_mask) > 10:
        h_a = np.mean(lab_ref[highlight_mask, 1])
        h_b = np.mean(lab_ref[highlight_mask, 2])
        hue_rad = np.arctan2(h_b, h_a)
        gain_wheel.hue = float((np.degrees(hue_rad)) % 360.0)
        gain_wheel.saturation = float(np.clip(np.sqrt(h_a**2 + h_b**2) / 60.0, 0.0, 0.5))

    grade = ColorGradeModel(
        exposure=exposure,
        contrast=contrast,
        highlights=highlights,
        shadows=shadows,
        temperature=temperature,
        tint=tint,
        saturation=saturation,
    )
    grade.color_wheels.lift = lift_wheel
    grade.color_wheels.gain = gain_wheel

    # Determine Look DNA
    palette = _extract_dominant_palette(reference_img, 5)
    mood = "Cinematic Match" if abs(contrast) > 15 else "Natural Reference"
    if temperature > 15:
        mood = "Warm " + mood
    elif temperature < -15:
        mood = "Cool " + mood

    dna = LookDNA(
        mood=mood,
        temperature_profile=f"{'Warm' if temperature >= 0 else 'Cool'} ({temperature:+.1f})",
        contrast_profile=f"{'High Dynamic' if contrast >= 0 else 'Soft Muted'} ({contrast:+.1f})",
        saturation_profile=f"{'Rich' if saturation >= 0 else 'Restrained'} ({saturation:+.1f})",
        highlight_character="Warm Tint" if gain_wheel.saturation > 0.1 else "Neutral Clean",
        shadow_character="Toned Shadow" if lift_wheel.saturation > 0.1 else "Deep Black",
        color_palette=palette,
        key_tags=["Reference Match", mood, "AI Match"],
    )

    return grade, dna

