"""
THEARA COLOR — Master Color Transformation Pipeline
Founder: Krai Theara | "Create Your Look"
"""

import numpy as np
from PIL import Image
from .models import ColorGradeModel
from .exposure import apply_exposure, apply_contrast, apply_whites_blacks
from .temperature import apply_temperature_and_tint
from .highlights_shadows import apply_highlights_shadows
from .saturation import apply_saturation_vibrance
from .curves import apply_curves
from .hsl import apply_hsl
from .color_wheels import apply_color_wheels
from .film_effects import apply_fade, apply_vignette, apply_grain


def apply_color_grade(
    rgb: np.ndarray,
    grade: ColorGradeModel,
    is_lut_lattice: bool = False,
) -> np.ndarray:
    """
    Applies the full structured color grading pipeline to an RGB float32 array [0.0, 1.0].
    Deterministic and mathematically bounded.
    """
    original = rgb.copy()
    current = rgb.copy()

    # 1. Exposure
    current = apply_exposure(current, grade.exposure)

    # 2. Contrast
    current = apply_contrast(current, grade.contrast)

    # 3. Whites & Blacks
    current = apply_whites_blacks(current, grade.whites, grade.blacks)

    # 4. Temperature & Tint
    current = apply_temperature_and_tint(current, grade.temperature, grade.tint)

    # 5. Highlights & Shadows
    current = apply_highlights_shadows(current, grade.highlights, grade.shadows)

    # 6. Tone Curves (Cubic Splines)
    current = apply_curves(current, grade.curves)

    # 7. 3-Way Color Wheels
    current = apply_color_wheels(current, grade.color_wheels)

    # 8. 8-Vector HSL
    current = apply_hsl(current, grade.hsl)

    # 9. Saturation & Vibrance
    current = apply_saturation_vibrance(current, grade.saturation, grade.vibrance)

    # 10. Matte Fade
    current = apply_fade(current, grade.fade)

    # 11. Spatial Effects (only for 2D images, not 3D LUT lattices)
    if not is_lut_lattice and rgb.ndim == 3:
        current = apply_vignette(current, grade.vignette)
        current = apply_grain(current, grade.grain)

    # 12. Global Intensity Blending
    if grade.intensity != 1.0:
        # alpha = grade.intensity
        current = original + grade.intensity * (current - original)

    # 13. Deterministic Clamping
    return np.clip(current, 0.0, 1.0).astype(np.float32)


def process_image(img: Image.Image, grade: ColorGradeModel) -> Image.Image:
    """
    Processes a PIL Image through the color pipeline and returns a graded PIL Image.
    """
    # Ensure RGB
    if img.mode != "RGB":
        img = img.convert("RGB")

    arr = np.array(img, dtype=np.float32) / 255.0
    graded = apply_color_grade(arr, grade, is_lut_lattice=False)
    out_uint8 = np.clip(np.round(graded * 255.0), 0, 255).astype(np.uint8)
    return Image.fromarray(out_uint8, mode="RGB")

