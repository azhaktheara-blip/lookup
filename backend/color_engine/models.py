"""
THEARA COLOR — Internal Structured Color Model (V1 and V2)
Founder: Krai Theara | "Create Your Look"
"""

from typing import List, Tuple
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# V1 MODELS (Legacy / UI Internal Bridge)
# ============================================================================

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
    hue: float = Field(0.0, ge=0.0, le=360.0)
    saturation: float = Field(0.0, ge=0.0, le=1.0)
    luminance: float = Field(0.0, ge=-1.0, le=1.0)


class ColorWheelsSettings(BaseModel):
    lift: ColorWheel = Field(default_factory=lambda: ColorWheel(hue=0.0, saturation=0.0, luminance=0.0))    # Shadows
    gamma: ColorWheel = Field(default_factory=lambda: ColorWheel(hue=0.0, saturation=0.0, luminance=0.0))   # Midtones
    gain: ColorWheel = Field(default_factory=lambda: ColorWheel(hue=0.0, saturation=0.0, luminance=0.0))    # Highlights


class ColorGradeModel(BaseModel):
    exposure: float = Field(0.0, ge=-5.0, le=5.0, description="Exposure in EV stops (-5 to +5)")
    contrast: float = Field(0.0, ge=-100.0, le=100.0, description="Contrast (-100 to +100)")
    highlights: float = Field(0.0, ge=-100.0, le=100.0, description="Highlights recovery/boost (-100 to +100)")
    shadows: float = Field(0.0, ge=-100.0, le=100.0, description="Shadows lift/crush (-100 to +100)")
    whites: float = Field(0.0, ge=-100.0, le=100.0, description="Whites point (-100 to +100)")
    blacks: float = Field(0.0, ge=-100.0, le=100.0, description="Blacks point (-100 to +100)")

    temperature: float = Field(0.0, ge=-100.0, le=100.0, description="Temperature: Cool (-100) to Warm (+100)")
    tint: float = Field(0.0, ge=-100.0, le=100.0, description="Tint: Green (-100) to Magenta (+100)")

    saturation: float = Field(0.0, ge=-100.0, le=100.0, description="Master Saturation (-100 to +100)")
    vibrance: float = Field(0.0, ge=-100.0, le=100.0, description="Smart skin-preserving vibrance (-100 to +100)")
    fade: float = Field(0.0, ge=0.0, le=100.0, description="Black point lift for matte film look (0 to 100)")

    curves: CurveSettings = Field(default_factory=CurveSettings)
    hsl: HSLSettings = Field(default_factory=HSLSettings)
    color_wheels: ColorWheelsSettings = Field(default_factory=ColorWheelsSettings)

    grain: float = Field(0.0, ge=0.0, le=100.0, description="Film grain noise amount (0 to 100)")
    vignette: float = Field(0.0, ge=-100.0, le=100.0, description="Vignette darkening/lightening (-100 to +100)")
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


# ============================================================================
# V2 STYLE INTERPRETER SCHEMA (Production Style Interpreter v2 Contract)
# ============================================================================

class ColorWheelRGBV2(BaseModel):
    r: float = Field(0.0, ge=-1.0, le=1.0)
    g: float = Field(0.0, ge=-1.0, le=1.0)
    b: float = Field(0.0, ge=-1.0, le=1.0)


class ColorWheelsV2(BaseModel):
    lift: ColorWheelRGBV2 = Field(default_factory=ColorWheelRGBV2)
    gamma: ColorWheelRGBV2 = Field(default_factory=ColorWheelRGBV2)
    gain: ColorWheelRGBV2 = Field(default_factory=ColorWheelRGBV2)


class HSLBandEntryV2(BaseModel):
    hue: float = Field(0.0, ge=-180.0, le=180.0)
    sat: float = Field(0.0, ge=-1.0, le=1.0)
    lum: float = Field(0.0, ge=-1.0, le=1.0)


class HSLBandsV2(BaseModel):
    red: HSLBandEntryV2 = Field(default_factory=HSLBandEntryV2)
    orange: HSLBandEntryV2 = Field(default_factory=HSLBandEntryV2)
    yellow: HSLBandEntryV2 = Field(default_factory=HSLBandEntryV2)
    green: HSLBandEntryV2 = Field(default_factory=HSLBandEntryV2)
    aqua: HSLBandEntryV2 = Field(default_factory=HSLBandEntryV2)
    blue: HSLBandEntryV2 = Field(default_factory=HSLBandEntryV2)
    purple: HSLBandEntryV2 = Field(default_factory=HSLBandEntryV2)
    magenta: HSLBandEntryV2 = Field(default_factory=HSLBandEntryV2)


class VignetteV2(BaseModel):
    amount: float = Field(0.0, ge=-1.0, le=1.0)
    midpoint: float = Field(0.5, ge=0.0, le=1.0)
    feather: float = Field(0.5, ge=0.0, le=1.0)


class GrainV2(BaseModel):
    amount: float = Field(0.0, ge=0.0, le=1.0)
    size: float = Field(0.5, ge=0.0, le=1.0)


class LookDNASummaryV2(BaseModel):
    mood: str = Field(..., min_length=2, max_length=100)
    temperature_profile: str = Field(..., min_length=2, max_length=100)
    confidence: float = Field(..., ge=0.0, le=1.0)


class ColorGradeModelV2(BaseModel):
    temperature_kelvin: float = Field(6500.0, ge=2000.0, le=12000.0)
    tint: float = Field(0.0, ge=-1.0, le=1.0)
    exposure_ev: float = Field(0.0, ge=-2.0, le=2.0)
    contrast: float = Field(0.5, ge=0.0, le=1.0)
    color_wheels: ColorWheelsV2 = Field(default_factory=ColorWheelsV2)
    hsl_bands: HSLBandsV2 = Field(default_factory=HSLBandsV2)
    tone_curve_points: List[List[float]] = Field(
        default_factory=lambda: [
            [0.0, 0.0],
            [0.25, 0.25],
            [0.5, 0.5],
            [0.75, 0.75],
            [1.0, 1.0],
        ]
    )
    highlights_softknee: float = Field(0.0, ge=0.0, le=1.0)
    shadows_softknee: float = Field(0.0, ge=0.0, le=1.0)
    vignette: VignetteV2 = Field(default_factory=VignetteV2)
    grain: GrainV2 = Field(default_factory=GrainV2)
    matte_fade: float = Field(0.0, ge=0.0, le=1.0)
    look_dna_summary: LookDNASummaryV2 = Field(
        default_factory=lambda: LookDNASummaryV2(
            mood="neutral, natural",
            temperature_profile="neutral",
            confidence=0.0,
        )
    )

    @field_validator("tone_curve_points")
    @classmethod
    def validate_tone_curve(cls, points: List[List[float]]) -> List[List[float]]:
        if len(points) < 3 or len(points) > 6:
            raise ValueError("tone_curve_points must contain 3 to 6 points")
        for i in range(len(points)):
            if len(points[i]) != 2:
                raise ValueError(f"Each tone curve point must be [x, y], got {points[i]}")
            x, y = points[i][0], points[i][1]
            if not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0):
                raise ValueError(f"Tone curve coordinates must be within [0, 1], got [{x}, {y}]")
            if i > 0:
                if x <= points[i - 1][0]:
                    raise ValueError("tone_curve_points X values must be strictly increasing")
                if y < points[i - 1][1] - 1e-5:
                    raise ValueError("tone_curve_points Y values must be monotonically non-decreasing")
        return points

    def to_v1(self) -> ColorGradeModel:
        """Translates V2 structured parameters into V1 engine format."""
        # Temperature: 6500 is neutral 0. 2000 is cool (-100), 12000 is warm (+100)
        temp_norm = (self.temperature_kelvin - 6500.0) / 55.0
        contrast_norm = (self.contrast - 0.5) * 200.0  # 0.5 -> 0, 1.0 -> 100, 0.0 -> -100

        # Tone curves
        curve_pts = [CurvePoint(x=pt[0], y=pt[1]) for pt in self.tone_curve_points]
        curves = CurveSettings(
            master=curve_pts,
            red=[CurvePoint(x=0.0, y=0.0), CurvePoint(x=1.0, y=1.0)],
            green=[CurvePoint(x=0.0, y=0.0), CurvePoint(x=1.0, y=1.0)],
            blue=[CurvePoint(x=0.0, y=0.0), CurvePoint(x=1.0, y=1.0)],
        )

        # HSL mapping
        hsl = HSLSettings(
            red=HSLChannel(hue=self.hsl_bands.red.hue, saturation=self.hsl_bands.red.sat * 100.0, luminance=self.hsl_bands.red.lum * 100.0),
            orange=HSLChannel(hue=self.hsl_bands.orange.hue, saturation=self.hsl_bands.orange.sat * 100.0, luminance=self.hsl_bands.orange.lum * 100.0),
            yellow=HSLChannel(hue=self.hsl_bands.yellow.hue, saturation=self.hsl_bands.yellow.sat * 100.0, luminance=self.hsl_bands.yellow.lum * 100.0),
            green=HSLChannel(hue=self.hsl_bands.green.hue, saturation=self.hsl_bands.green.sat * 100.0, luminance=self.hsl_bands.green.lum * 100.0),
            aqua=HSLChannel(hue=self.hsl_bands.aqua.hue, saturation=self.hsl_bands.aqua.sat * 100.0, luminance=self.hsl_bands.aqua.lum * 100.0),
            blue=HSLChannel(hue=self.hsl_bands.blue.hue, saturation=self.hsl_bands.blue.sat * 100.0, luminance=self.hsl_bands.blue.lum * 100.0),
            purple=HSLChannel(hue=self.hsl_bands.purple.hue, saturation=self.hsl_bands.purple.sat * 100.0, luminance=self.hsl_bands.purple.lum * 100.0),
            magenta=HSLChannel(hue=self.hsl_bands.magenta.hue, saturation=self.hsl_bands.magenta.sat * 100.0, luminance=self.hsl_bands.magenta.lum * 100.0),
        )

        # Color wheels: convert RGB delta to Wheel (hue, sat, lum)
        import math
        def rgb_to_wheel(c: ColorWheelRGBV2) -> ColorWheel:
            sat = min(1.0, math.hypot(c.r - c.g, c.g - c.b))
            hue = (math.degrees(math.atan2(c.g - c.b, c.r - (c.g + c.b) / 2.0)) + 360.0) % 360.0
            lum = (c.r + c.g + c.b) / 3.0
            return ColorWheel(hue=hue, saturation=sat, luminance=lum)

        wheels = ColorWheelsSettings(
            lift=rgb_to_wheel(self.color_wheels.lift),
            gamma=rgb_to_wheel(self.color_wheels.gamma),
            gain=rgb_to_wheel(self.color_wheels.gain),
        )

        return ColorGradeModel(
            exposure=self.exposure_ev,
            contrast=contrast_norm,
            highlights=-self.highlights_softknee * 40.0,
            shadows=self.shadows_softknee * 40.0,
            temperature=temp_norm,
            tint=self.tint * 100.0,
            fade=self.matte_fade * 100.0,
            curves=curves,
            hsl=hsl,
            color_wheels=wheels,
            grain=self.grain.amount * 100.0,
            vignette=self.vignette.amount * 100.0,
            intensity=1.0,
        )
