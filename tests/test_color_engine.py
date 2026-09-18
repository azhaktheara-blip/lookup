"""
Unit tests for THEARA COLOR pure mathematical color engine.
"""

import sys
import os
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.abspath("backend"))

from color_engine import (
    ColorGradeModel,
    apply_color_grade,
    process_image,
    generate_cube_lut,
    validate_cube_syntax,
    generate_xmp_preset,
    validate_and_clamp_grade,
    CurvePoint,
)
from color_engine.reference import analyze_reference_match


def test_identity_grade():
    """Default parameters should not alter RGB values."""
    grade = ColorGradeModel()
    dummy_rgb = np.array([[[0.2, 0.4, 0.8], [0.5, 0.5, 0.5]]], dtype=np.float32)
    output = apply_color_grade(dummy_rgb, grade)
    assert np.allclose(dummy_rgb, output, atol=1e-3)


def test_exposure_doubling():
    """+1 EV exposure should double linear values (bounded by 1.0)."""
    grade = ColorGradeModel(exposure=1.0)
    dummy_rgb = np.array([[[0.25, 0.4, 0.1]]], dtype=np.float32)
    output = apply_color_grade(dummy_rgb, grade)
    assert np.isclose(output[0, 0, 0], 0.5, atol=1e-3)
    assert np.isclose(output[0, 0, 1], 0.8, atol=1e-3)
    assert np.isclose(output[0, 0, 2], 0.2, atol=1e-3)


def test_temperature_warmth():
    """Warm temperature should increase Red and decrease Blue."""
    grade = ColorGradeModel(temperature=50.0)
    neutral_gray = np.array([[[0.5, 0.5, 0.5]]], dtype=np.float32)
    output = apply_color_grade(neutral_gray, grade)
    assert output[0, 0, 0] > 0.5   # R boosted
    assert output[0, 0, 2] < 0.5   # B reduced


def test_cube_lut_validity():
    """Generates a 33x33x33 LUT and validates format and row count."""
    grade = ColorGradeModel(
        exposure=0.5,
        contrast=15.0,
        temperature=20.0,
        saturation=10.0,
    )
    cube_text = generate_cube_lut(grade, size=33, title="Test Look")
    is_valid, msg = validate_cube_syntax(cube_text)
    assert is_valid is True, f"Validation failed: {msg}"
    assert "LUT_3D_SIZE 33" in cube_text
    assert "TITLE \"Test Look\"" in cube_text


def test_xmp_preset_generation():
    """Generates Adobe XMP preset XML and asserts required crs tags exist."""
    grade = ColorGradeModel(
        exposure=0.3,
        contrast=10.0,
        highlights=-20.0,
        shadows=15.0,
    )
    xmp_text = generate_xmp_preset(grade, preset_name="Nordic Film")
    assert "<x:xmpmeta" in xmp_text
    assert 'crs:Exposure2012="+0.30"' in xmp_text
    assert 'crs:Contrast2012="10"' in xmp_text
    assert 'crs:Highlights2012="-20"' in xmp_text
    assert 'crs:Shadows2012="15"' in xmp_text
    assert "Nordic Film" in xmp_text


def test_image_processing_bounds():
    """Ensure PIL Image processing preserves dimensions and bounds within 0-255."""
    img = Image.new("RGB", (64, 64), color=(128, 100, 80))
    grade = ColorGradeModel(exposure=2.0, contrast=50.0, grain=30.0, vignette=20.0)
    out_img = process_image(img, grade)
    assert out_img.size == (64, 64)
    assert out_img.mode == "RGB"
    arr = np.array(out_img)
    assert arr.min() >= 0
    assert arr.max() <= 255


def test_reference_analysis():
    """Ensure reference matching produces coherent ColorGradeModel and LookDNA."""
    orig = Image.new("RGB", (64, 64), color=(150, 120, 100))
    ref = Image.new("RGB", (64, 64), color=(60, 140, 210))
    grade, dna = analyze_reference_match(orig, ref)
    assert grade is not None
    assert dna.mood is not None
    assert len(dna.color_palette) > 0


if __name__ == "__main__":
    test_identity_grade()
    test_exposure_doubling()
    test_temperature_warmth()
    test_cube_lut_validity()
    test_xmp_preset_generation()
    test_image_processing_bounds()
    test_reference_analysis()
    print("ALL COLOR TESTS PASSED!")

