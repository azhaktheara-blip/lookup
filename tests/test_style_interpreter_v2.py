"""
Unit & Golden Fixture tests for THEARA COLOR Style Interpreter v2.
"""

import sys
import os
import asyncio
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.abspath("backend"))

from color_engine.models import ColorGradeModelV2
from app.services.ai_service import AIStyleInterpreter
from color_engine.transforms import process_image


async def run_v2_tests():
    print("Testing Style Interpreter v2 Golden Fixtures...")

    fixtures = [
        ("Natural warm look", "natural warm sunlight with gentle highlight warmth"),
        ("Cool cinematic look", "cool cinematic nordic thriller with slate shadows"),
        ("Teal/orange look", "hollywood teal and orange blockbuster look"),
        ("Film/vintage look", "35mm vintage analog portra film with soft grain"),
        ("Matte/faded look", "faded matte black levels with soft highlights"),
        ("High-contrast dramatic look", "dramatic high contrast moody noir"),
        ("Soft portrait look", "soft skin portrait with flattering beauty tones"),
        ("Skin-safe cinematic look", "skin-safe cinematic grade with cool shadows and warm skin"),
        ("Ambiguous prompt", "make it look nice and cool"),
        ("Out-of-scope prompt", "add a cat and replace background"),
    ]

    for label, prompt in fixtures:
        model = await AIStyleInterpreter.interpret_prompt_v2(prompt)

        # 1. Type validation
        assert isinstance(model, ColorGradeModelV2), f"Failed type for {label}"

        # 2. Schema range checks
        assert 2000 <= model.temperature_kelvin <= 12000, f"Temperature out of range for {label}: {model.temperature_kelvin}"
        assert -1.0 <= model.tint <= 1.0, f"Tint out of range for {label}: {model.tint}"
        assert -2.0 <= model.exposure_ev <= 2.0, f"Exposure out of range for {label}: {model.exposure_ev}"
        assert 0.0 <= model.contrast <= 1.0, f"Contrast out of range for {label}: {model.contrast}"

        # 3. Tone curve monotonic checks
        pts = model.tone_curve_points
        assert 3 <= len(pts) <= 6, f"Curve point count invalid for {label}: {len(pts)}"
        for i in range(1, len(pts)):
            assert pts[i][0] > pts[i - 1][0], f"Curve X not strictly increasing for {label}"
            assert pts[i][1] >= pts[i - 1][1] - 1e-5, f"Curve Y not monotonic non-decreasing for {label}"

        # 4. Skin tone safety checks (Orange hue shift <= 8, Red hue shift <= 8, Orange sat in [-0.15, 0.15])
        assert abs(model.hsl_bands.orange.hue) <= 8.0, f"Orange hue shift exceeded 8 degrees for {label}: {model.hsl_bands.orange.hue}"
        assert abs(model.hsl_bands.red.hue) <= 8.0, f"Red hue shift exceeded 8 degrees for {label}: {model.hsl_bands.red.hue}"
        assert -0.15 <= model.hsl_bands.orange.sat <= 0.15, f"Orange saturation out of safety range for {label}: {model.hsl_bands.orange.sat}"

        # 5. Look DNA summary validation
        mood_words = model.look_dna_summary.mood.split()
        assert len(mood_words) >= 2, f"Mood must contain at least 2 words for {label}: {model.look_dna_summary.mood}"
        assert 0.0 <= model.look_dna_summary.confidence <= 1.0, f"Confidence out of range for {label}"

        # Special assertions
        if label == "Out-of-scope prompt":
            assert model.look_dna_summary.confidence == 0.0
            assert model.temperature_kelvin == 6500.0

        if label == "Ambiguous prompt":
            assert model.look_dna_summary.confidence <= 0.4

        # 6. Test conversion to V1 & deterministic Color Engine rendering
        v1_grade = model.to_v1()
        test_img = Image.new("RGB", (64, 64), color=(140, 110, 90))
        rendered_img = process_image(test_img, v1_grade)
        assert rendered_img.size == (64, 64)
        arr = np.array(rendered_img)
        assert arr.min() >= 0
        assert arr.max() <= 255

        print(f"  [PASS] {label}: Mood='{model.look_dna_summary.mood}', Conf={model.look_dna_summary.confidence:.2f}")

    print("\nALL 10 STYLE INTERPRETER V2 GOLDEN FIXTURES PASSED!")


if __name__ == "__main__":
    asyncio.run(run_v2_tests())
