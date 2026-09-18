"""
THEARA COLOR — Color Parameter Validation and Sanitization
Founder: Krai Theara | "Create Your Look"
"""

from .models import ColorGradeModel


def validate_and_clamp_grade(grade: ColorGradeModel) -> ColorGradeModel:
    """
    Guarantees all parameters in a ColorGradeModel strictly conform to allowable domains,
    preventing non-physical artifacts or numerical overflows.
    """
    grade.exposure = max(-5.0, min(5.0, float(grade.exposure)))
    grade.contrast = max(-100.0, min(100.0, float(grade.contrast)))
    grade.highlights = max(-100.0, min(100.0, float(grade.highlights)))
    grade.shadows = max(-100.0, min(100.0, float(grade.shadows)))
    grade.whites = max(-100.0, min(100.0, float(grade.whites)))
    grade.blacks = max(-100.0, min(100.0, float(grade.blacks)))

    grade.temperature = max(-100.0, min(100.0, float(grade.temperature)))
    grade.tint = max(-100.0, min(100.0, float(grade.tint)))
    grade.saturation = max(-100.0, min(100.0, float(grade.saturation)))
    grade.vibrance = max(-100.0, min(100.0, float(grade.vibrance)))
    grade.fade = max(0.0, min(100.0, float(grade.fade)))

    grade.grain = max(0.0, min(100.0, float(grade.grain)))
    grade.vignette = max(-100.0, min(100.0, float(grade.vignette)))
    grade.intensity = max(0.0, min(2.0, float(grade.intensity)))

    # Validate curves points
    for curve in (grade.curves.master, grade.curves.red, grade.curves.green, grade.curves.blue):
        for pt in curve:
            pt.x = max(0.0, min(1.0, float(pt.x)))
            pt.y = max(0.0, min(1.0, float(pt.y)))

    # Validate wheels
    for wheel in (grade.color_wheels.lift, grade.color_wheels.gamma, grade.color_wheels.gain):
        wheel.hue = max(0.0, min(360.0, float(wheel.hue)))
        wheel.saturation = max(0.0, min(1.0, float(wheel.saturation)))
        wheel.luminance = max(-1.0, min(1.0, float(wheel.luminance)))

    return grade

