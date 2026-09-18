"""
THEARA COLOR — Internal Structured Color Model
Founder: Krai Theara | "Create Your Look"
"""

from typing import List, Tuple
from pydantic import BaseModel, Field


class CurvePoint(BaseModel):
    x: float = Field(..., ge=0.0, le=1.0)
    y: float = Field(..., ge=0.0, le=1.0)


class CurveSettings(BaseModel):
    master: List[CurvePoint] = Field(
        default_factory=lambda: [CurvePoint(x=0.0, y=0.0), CurvePoint(x=1.0, y=1.0)]
    )
    red: List[CurvePoint] = Field(
        default_factory=lambda: [CurvePoint(x=0.0, y=0.0), CurvePoint(x=1.0, y=1.0)]
    )
    green: List[CurvePoint] = Field(
        default_factory=lambda: [CurvePoint(x=0.0, y=0.0), CurvePoint(x=1.0, y=1.0)]
    )
    blue: List[CurvePoint] = Field(
        default_factory=lambda: [CurvePoint(x=0.0, y=0.0), CurvePoint(x=1.0, y=1.0)]
    )


class HSLChannel(BaseModel):
    hue: float = Field(0.0, ge=-100.0, le=100.0, description="Hue rotation delta")
    saturation: float = Field(0.0, ge=-100.0, le=100.0, description="Saturation delta")
    luminance: float = Field(0.0, ge=-100.0, le=100.0, description="Luminance delta")


class HSLSettings(BaseModel):
    red: HSLChannel = Field(default_factory=HSLChannel)
    orange: HSLChannel = Field(default_factory=HSLChannel)
    yellow: HSLChannel = Field(default_factory=HSLChannel)
    green: HSLChannel = Field(default_factory=HSLChannel)
    aqua: HSLChannel = Field(default_factory=HSLChannel)
    blue: HSLChannel = Field(default_factory=HSLChannel)
    purple: HSLChannel = Field(default_factory=HSLChannel)
    magenta: HSLChannel = Field(default_factory=HSLChannel)


class ColorWheel(BaseModel):
    # Hue: 0-360 degrees, Saturation: 0-1, Luminance: -1 to 1
    hue: float = Field(0.0, ge=0.0, le=360.0)
    saturation: float = Field(0.0, ge=0.0, le=1.0)
    luminance: float = Field(0.0, ge=-1.0, le=1.0)


class ColorWheelsSettings(BaseModel):
    lift: ColorWheel = Field(default_factory=lambda: ColorWheel(hue=0.0, saturation=0.0, luminance=0.0))    # Shadows
    gamma: ColorWheel = Field(default_factory=lambda: ColorWheel(hue=0.0, saturation=0.0, luminance=0.0))   # Midtones
    gain: ColorWheel = Field(default_factory=lambda: ColorWheel(hue=0.0, saturation=0.0, luminance=0.0))    # Highlights


class ColorGradeModel(BaseModel):
    # Basic Tone & Exposure
    exposure: float = Field(0.0, ge=-5.0, le=5.0, description="Exposure in EV stops (-5 to +5)")
    contrast: float = Field(0.0, ge=-100.0, le=100.0, description="Contrast (-100 to +100)")
    highlights: float = Field(0.0, ge=-100.0, le=100.0, description="Highlights recovery/boost (-100 to +100)")
    shadows: float = Field(0.0, ge=-100.0, le=100.0, description="Shadows lift/crush (-100 to +100)")
    whites: float = Field(0.0, ge=-100.0, le=100.0, description="Whites point (-100 to +100)")
    blacks: float = Field(0.0, ge=-100.0, le=100.0, description="Blacks point (-100 to +100)")

    # White Balance
    temperature: float = Field(0.0, ge=-100.0, le=100.0, description="Temperature: Cool (-100) to Warm (+100)")
    tint: float = Field(0.0, ge=-100.0, le=100.0, description="Tint: Green (-100) to Magenta (+100)")

    # Color Intensity & Matte
    saturation: float = Field(0.0, ge=-100.0, le=100.0, description="Master Saturation (-100 to +100)")
    vibrance: float = Field(0.0, ge=-100.0, le=100.0, description="Smart skin-preserving vibrance (-100 to +100)")
    fade: float = Field(0.0, ge=0.0, le=100.0, description="Black point lift for matte film look (0 to 100)")

    # Advanced Grading Modules
    curves: CurveSettings = Field(default_factory=CurveSettings)
    hsl: HSLSettings = Field(default_factory=HSLSettings)
    color_wheels: ColorWheelsSettings = Field(default_factory=ColorWheelsSettings)

    # Stylistic Texture
    grain: float = Field(0.0, ge=0.0, le=100.0, description="Film grain noise amount (0 to 100)")
    vignette: float = Field(0.0, ge=-100.0, le=100.0, description="Vignette darkening/lightening (-100 to +100)")

    # Overall Blend Intensity
    intensity: float = Field(1.0, ge=0.0, le=2.0, description="Global grade opacity / intensity (0.0 to 2.0)")


class LookDNA(BaseModel):
    mood: str = Field(..., description="E.g., 'Warm Cinematic', 'Moody Nordic', 'Vintage Luxury'")
    temperature_profile: str = Field(..., description="E.g., 'Golden Warm (+2200K)', 'Cool Slate'")
    contrast_profile: str = Field(..., description="E.g., 'High Dynamic Range', 'Matte S-Curve'")
    saturation_profile: str = Field(..., description="E.g., 'Selective Desaturation', 'Rich Kodachrome'")
    highlight_character: str = Field(..., description="E.g., 'Soft Amber Rolloff', 'Pristine Clean'")
    shadow_character: str = Field(..., description="E.g., 'Deep Teal Cyan', 'Lifted Charcoal'")
    color_palette: List[str] = Field(default_factory=list, description="5 HEX colors representing key grade hues")
    key_tags: List[str] = Field(default_factory=list, description="Tags like 'Cinematic', '35mm', 'Golden Hour'")

