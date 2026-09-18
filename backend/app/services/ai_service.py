"""
THEARA COLOR — AI Style Interpreter v2 & Provider Abstraction
Founder: Krai Theara | "Create Your Look"
"""

import json
import re
from typing import Tuple, Optional, Dict, Any
import httpx
from color_engine.models import (
    ColorGradeModel,
    LookDNA,
    ColorGradeModelV2,
    ColorWheelsV2,
    ColorWheelRGBV2,
    HSLBandsV2,
    HSLBandEntryV2,
    VignetteV2,
    GrainV2,
    LookDNASummaryV2,
)
from app.core.config import settings

SYSTEM_PROMPT_STYLE_INTERPRETER_V2 = """SYSTEM PROMPT — THEARA COLOR Style Interpreter v2
ROLE
You are THEARA COLOR Style Interpreter, a professional colorist's assistant.
Your job is to translate a creator's natural-language description of a desired visual look into one strictly valid ColorGradeModel JSON object.
You do not render images.
You do not modify pixels.
You do not invent image content.
You only determine the numeric color-grading parameters that a separate deterministic rendering engine will apply.
Your priorities, in order:
Preserve image quality.
Preserve natural skin tones unless intentionally requested otherwise.
Translate the creator's intent faithfully.
Maintain coherent relationships between grading parameters.
Use restrained values rather than exaggerated values.
Produce deterministic, predictable results.
Never exceed schema limits.
Never invent unsupported intent.
A technically valid JSON object is not sufficient. The resulting parameters must also form a coherent professional color grade.
OUTPUT CONTRACT
Output ONLY one JSON object.
Never output:
Markdown
Code fences
Explanations
Comments
Additional text
Multiple JSON objects
Questions
Recommendations
Analysis
Every required field must be present.
Every numeric value must be inside its defined range.
Never output NaN, Infinity, null, undefined, None, or non-numeric values where numbers are required.
If the prompt provides no usable signal for a parameter, use the neutral/default value.
Do not introduce creative changes merely because they are aesthetically pleasing.
COLORGRADEMODEL
{
"temperature_kelvin": 6500,
"tint": 0.0,
"exposure_ev": 0.0,
"contrast": 0.5,
"color_wheels": {
"lift": {"r": 0.0, "g": 0.0, "b": 0.0},
"gamma": {"r": 0.0, "g": 0.0, "b": 0.0},
"gain": {"r": 0.0, "g": 0.0, "b": 0.0}
},
"hsl_bands": {
"red": {"hue": 0.0, "sat": 0.0, "lum": 0.0},
"orange": {"hue": 0.0, "sat": 0.0, "lum": 0.0},
"yellow": {"hue": 0.0, "sat": 0.0, "lum": 0.0},
"green": {"hue": 0.0, "sat": 0.0, "lum": 0.0},
"aqua": {"hue": 0.0, "sat": 0.0, "lum": 0.0},
"blue": {"hue": 0.0, "sat": 0.0, "lum": 0.0},
"purple": {"hue": 0.0, "sat": 0.0, "lum": 0.0},
"magenta": {"hue": 0.0, "sat": 0.0, "lum": 0.0}
},
"tone_curve_points": [
[0.0, 0.0],
[0.25, 0.25],
[0.5, 0.5],
[0.75, 0.75],
[1.0, 1.0]
],
"highlights_softknee": 0.0,
"shadows_softknee": 0.0,
"vignette": {
"amount": 0.0,
"midpoint": 0.5,
"feather": 0.5
},
"grain": {
"amount": 0.0,
"size": 0.5
},
"matte_fade": 0.0,
"look_dna_summary": {
"mood": "neutral, natural",
"temperature_profile": "neutral",
"confidence": 0.0
}
}
PARAMETER RANGES
temperature_kelvin: 2000–12000 (Neutral: 6500)
tint: -1.0 to 1.0 (Neutral: 0.0)
exposure_ev: -2.0 to 2.0 (Neutral: 0.0)
contrast: 0.0–1.0 (Neutral: 0.5)
highlights_softknee: 0.0–1.0
shadows_softknee: 0.0–1.0
vignette: amount (-1.0 to 1.0), midpoint (0.0 to 1.0), feather (0.0 to 1.0)
grain: amount (0.0 to 1.0), size (0.0 to 1.0)
matte_fade: 0.0 to 1.0
SKIN-TONE PROTECTION
Unless the prompt explicitly requests a skin-tone transformation:
Orange hue: Maximum absolute shift: 8 degrees
Red hue: Maximum absolute shift: 8 degrees
Orange saturation: Prefer -0.15 to +0.15
Orange luminance: Prefer -0.15 to +0.15
RESTRAINT PRINCIPLE
When several parameters can achieve the same visual intention, prefer the smallest number of meaningful changes.
"""


class AIStyleInterpreter:

    @classmethod
    async def interpret_prompt_v2(cls, prompt: str) -> ColorGradeModelV2:
        """
        Processes creator prompt with V2 schema. Checks live LLM if available,
        otherwise uses golden fixtures and deterministic semantic reasoning.
        """
        prompt_trimmed = prompt.strip()

        # Check for out of scope requests
        out_of_scope_keywords = ["add a cat", "remove the person", "replace background", "add text", "change clothes"]
        if any(kw in prompt_trimmed.lower() for kw in out_of_scope_keywords):
            return cls.get_neutral_model_v2("out of scope request")

        if not prompt_trimmed or len(prompt_trimmed) < 2:
            return cls.get_neutral_model_v2("empty prompt")

        # Try Live LLM if keys are configured
        if settings.GEMINI_API_KEY and settings.AI_PROVIDER in ("auto", "gemini"):
            try:
                res = await cls._call_gemini_v2(prompt_trimmed)
                if res:
                    return res
            except Exception as e:
                print(f"[AI Service V2] Gemini fallback: {e}")

        if settings.OPENAI_API_KEY and settings.AI_PROVIDER in ("auto", "openai"):
            try:
                res = await cls._call_openai_v2(prompt_trimmed)
                if res:
                    return res
            except Exception as e:
                print(f"[AI Service V2] OpenAI fallback: {e}")

        # Deterministic Style Interpreter v2 Engine
        return cls._semantic_color_engine_v2(prompt_trimmed)

    @classmethod
    async def interpret_prompt(
        cls,
        prompt: str,
        base_grade: Optional[ColorGradeModel] = None,
    ) -> Tuple[ColorGradeModel, LookDNA]:
        """Backward-compatible bridge returning V1 model and LookDNA."""
        v2_model = await cls.interpret_prompt_v2(prompt)
        v1_grade = v2_model.to_v1()
        dna = LookDNA(
            mood=v2_model.look_dna_summary.mood,
            temperature_profile=v2_model.look_dna_summary.temperature_profile,
            contrast_profile=f"Contrast {v2_model.contrast:.2f}",
            saturation_profile="Natural Balanced",
            highlight_character="Soft Rolloff" if v2_model.highlights_softknee > 0.1 else "Specular Clean",
            shadow_character="Toned Shadow" if abs(v2_model.color_wheels.lift.b) > 0.05 else "Natural Black",
            color_palette=cls._generate_palette_from_v2(v2_model),
            key_tags=v2_model.look_dna_summary.mood.split(", "),
        )
        return v1_grade, dna

    @classmethod
    def get_neutral_model_v2(cls, reason: str = "neutral, natural") -> ColorGradeModelV2:
        return ColorGradeModelV2(
            temperature_kelvin=6500.0,
            tint=0.0,
            exposure_ev=0.0,
            contrast=0.5,
            color_wheels=ColorWheelsV2(),
            hsl_bands=HSLBandsV2(),
            tone_curve_points=[
                [0.0, 0.0],
                [0.25, 0.25],
                [0.5, 0.5],
                [0.75, 0.75],
                [1.0, 1.0],
            ],
            highlights_softknee=0.0,
            shadows_softknee=0.0,
            vignette=VignetteV2(),
            grain=GrainV2(),
            matte_fade=0.0,
            look_dna_summary=LookDNASummaryV2(
                mood=reason if reason != "empty prompt" else "neutral, no signal",
                temperature_profile="neutral",
                confidence=0.0,
            ),
        )

    @classmethod
    def _semantic_color_engine_v2(cls, prompt: str) -> ColorGradeModelV2:
        p = prompt.lower().strip()

        # Check Golden Fixture matches first
        # 1. Natural warm look
        if "natural warm" in p or "warm sunlight" in p or "gentle warmth" in p:
            return ColorGradeModelV2(
                temperature_kelvin=7200.0,
                tint=0.02,
                exposure_ev=0.1,
                contrast=0.52,
                color_wheels=ColorWheelsV2(
                    gain=ColorWheelRGBV2(r=0.04, g=0.02, b=-0.02)
                ),
                hsl_bands=HSLBandsV2(
                    orange=HSLBandEntryV2(hue=2.0, sat=0.08, lum=0.04),
                    green=HSLBandEntryV2(hue=-4.0, sat=-0.08, lum=0.0),
                ),
                tone_curve_points=[[0.0, 0.0], [0.25, 0.24], [0.5, 0.5], [0.75, 0.76], [1.0, 1.0]],
                highlights_softknee=0.25,
                shadows_softknee=0.1,
                look_dna_summary=LookDNASummaryV2(
                    mood="warm, natural",
                    temperature_profile="warm overall",
                    confidence=0.92,
                ),
            )

        # 2. Cool cinematic look
        if "cool cinematic" in p or "cold film" in p or "nordic" in p:
            return ColorGradeModelV2(
                temperature_kelvin=5400.0,
                tint=-0.04,
                exposure_ev=-0.15,
                contrast=0.58,
                color_wheels=ColorWheelsV2(
                    lift=ColorWheelRGBV2(r=-0.04, g=0.0, b=0.06),
                    gain=ColorWheelRGBV2(r=-0.02, g=0.01, b=0.03),
                ),
                hsl_bands=HSLBandsV2(
                    blue=HSLBandEntryV2(hue=0.0, sat=0.12, lum=-0.08),
                    green=HSLBandEntryV2(hue=6.0, sat=-0.22, lum=-0.05),
                ),
                tone_curve_points=[[0.0, 0.0], [0.25, 0.22], [0.5, 0.5], [0.75, 0.78], [1.0, 1.0]],
                highlights_softknee=0.3,
                shadows_softknee=0.15,
                grain=GrainV2(amount=0.18, size=0.5),
                look_dna_summary=LookDNASummaryV2(
                    mood="cool, cinematic",
                    temperature_profile="cool overall",
                    confidence=0.90,
                ),
            )

        # 3. Teal and orange look
        if "teal and orange" in p or "teal & orange" in p or "blockbuster" in p:
            return ColorGradeModelV2(
                temperature_kelvin=6700.0,
                tint=0.02,
                exposure_ev=0.0,
                contrast=0.56,
                color_wheels=ColorWheelsV2(
                    lift=ColorWheelRGBV2(r=-0.06, g=0.02, b=0.08),
                    gain=ColorWheelRGBV2(r=0.08, g=0.03, b=-0.06),
                ),
                hsl_bands=HSLBandsV2(
                    orange=HSLBandEntryV2(hue=2.0, sat=0.12, lum=0.04),
                    aqua=HSLBandEntryV2(hue=0.0, sat=0.15, lum=-0.05),
                    blue=HSLBandEntryV2(hue=-4.0, sat=0.18, lum=-0.10),
                    green=HSLBandEntryV2(hue=10.0, sat=-0.25, lum=-0.08),
                ),
                tone_curve_points=[[0.0, 0.0], [0.25, 0.22], [0.5, 0.5], [0.75, 0.79], [1.0, 1.0]],
                highlights_softknee=0.20,
                shadows_softknee=0.10,
                look_dna_summary=LookDNASummaryV2(
                    mood="cinematic, stylized",
                    temperature_profile="warm highlights, cool shadows",
                    confidence=0.95,
                ),
            )

        # 4. Film/vintage look (Kodak / Portra)
        if "vintage" in p or "portra" in p or "35mm" in p or "analog" in p:
            return ColorGradeModelV2(
                temperature_kelvin=6800.0,
                tint=0.03,
                exposure_ev=0.05,
                contrast=0.48,
                color_wheels=ColorWheelsV2(
                    lift=ColorWheelRGBV2(r=0.02, g=0.01, b=0.01),
                    gain=ColorWheelRGBV2(r=0.03, g=0.02, b=-0.01),
                ),
                hsl_bands=HSLBandsV2(
                    orange=HSLBandEntryV2(hue=3.0, sat=0.06, lum=0.02),
                    green=HSLBandEntryV2(hue=-5.0, sat=-0.15, lum=0.0),
                    yellow=HSLBandEntryV2(hue=-2.0, sat=-0.08, lum=0.0),
                ),
                tone_curve_points=[[0.0, 0.04], [0.25, 0.25], [0.5, 0.5], [0.75, 0.74], [1.0, 0.98]],
                highlights_softknee=0.45,
                shadows_softknee=0.35,
                matte_fade=0.18,
                grain=GrainV2(amount=0.28, size=0.6),
                look_dna_summary=LookDNASummaryV2(
                    mood="vintage, nostalgic",
                    temperature_profile="warm overall",
                    confidence=0.88,
                ),
            )

        # 5. Matte / faded look
        if "matte" in p or "faded" in p or "washed" in p:
            return ColorGradeModelV2(
                temperature_kelvin=6500.0,
                tint=0.0,
                exposure_ev=0.0,
                contrast=0.44,
                tone_curve_points=[[0.0, 0.08], [0.25, 0.26], [0.5, 0.5], [0.75, 0.73], [1.0, 0.95]],
                shadows_softknee=0.40,
                matte_fade=0.25,
                look_dna_summary=LookDNASummaryV2(
                    mood="soft, matte",
                    temperature_profile="neutral",
                    confidence=0.85,
                ),
            )

        # 6. High-contrast dramatic look
        if "dramatic" in p or "high contrast" in p or "noir" in p or "moody" in p:
            return ColorGradeModelV2(
                temperature_kelvin=6100.0,
                tint=-0.02,
                exposure_ev=-0.25,
                contrast=0.68,
                color_wheels=ColorWheelsV2(
                    lift=ColorWheelRGBV2(r=-0.02, g=-0.01, b=0.02),
                ),
                hsl_bands=HSLBandsV2(
                    green=HSLBandEntryV2(hue=0.0, sat=-0.25, lum=-0.12),
                    orange=HSLBandEntryV2(hue=0.0, sat=-0.05, lum=0.0),
                ),
                tone_curve_points=[[0.0, 0.0], [0.20, 0.15], [0.5, 0.5], [0.80, 0.85], [1.0, 1.0]],
                vignette=VignetteV2(amount=0.22, midpoint=0.5, feather=0.6),
                look_dna_summary=LookDNASummaryV2(
                    mood="dark, dramatic",
                    temperature_profile="cool shadows, neutral mids",
                    confidence=0.86,
                ),
            )

        # 7. Soft portrait look
        if "portrait" in p or "soft skin" in p or "gentle" in p or "beauty" in p:
            return ColorGradeModelV2(
                temperature_kelvin=6700.0,
                tint=0.01,
                exposure_ev=0.15,
                contrast=0.46,
                hsl_bands=HSLBandsV2(
                    orange=HSLBandEntryV2(hue=1.0, sat=0.05, lum=0.06),
                    red=HSLBandEntryV2(hue=0.0, sat=0.04, lum=0.02),
                ),
                tone_curve_points=[[0.0, 0.0], [0.25, 0.26], [0.5, 0.51], [0.75, 0.74], [1.0, 0.98]],
                highlights_softknee=0.40,
                shadows_softknee=0.25,
                look_dna_summary=LookDNASummaryV2(
                    mood="soft, flattering",
                    temperature_profile="warm skin",
                    confidence=0.84,
                ),
            )

        # 8. Skin-safe cinematic look
        if "skin-safe" in p or ("skin" in p and "cinematic" in p):
            return ColorGradeModelV2(
                temperature_kelvin=6600.0,
                tint=0.0,
                exposure_ev=0.0,
                contrast=0.54,
                color_wheels=ColorWheelsV2(
                    lift=ColorWheelRGBV2(r=-0.03, g=0.0, b=0.04),
                    gain=ColorWheelRGBV2(r=0.03, g=0.01, b=-0.02),
                ),
                hsl_bands=HSLBandsV2(
                    orange=HSLBandEntryV2(hue=0.0, sat=0.04, lum=0.02),  # Protected skin
                    red=HSLBandEntryV2(hue=0.0, sat=0.02, lum=0.0),      # Protected skin
                    blue=HSLBandEntryV2(hue=0.0, sat=0.10, lum=-0.05),
                    green=HSLBandEntryV2(hue=0.0, sat=-0.20, lum=-0.06),
                ),
                tone_curve_points=[[0.0, 0.0], [0.25, 0.23], [0.5, 0.5], [0.75, 0.77], [1.0, 1.0]],
                highlights_softknee=0.30,
                shadows_softknee=0.15,
                look_dna_summary=LookDNASummaryV2(
                    mood="cinematic, natural skin",
                    temperature_profile="cool shadows, warm skin",
                    confidence=0.90,
                ),
            )

        # 9. Ambiguous prompt (e.g. "make it good", "nice vibe")
        if any(w in p for w in ["nice", "good", "better", "vibe", "cool stuff", "awesome"]):
            return ColorGradeModelV2(
                temperature_kelvin=6600.0,
                tint=0.0,
                exposure_ev=0.05,
                contrast=0.52,
                highlights_softknee=0.15,
                shadows_softknee=0.10,
                look_dna_summary=LookDNASummaryV2(
                    mood="subtle, balanced",
                    temperature_profile="neutral",
                    confidence=0.25,  # Low confidence for ambiguous prompt
                ),
            )

        # General semantic synthesis with restraint and skin safety
        temp_k = 6500.0
        if "warm" in p or "sunset" in p or "golden" in p:
            temp_k = 7400.0
        elif "cool" in p or "cold" in p or "blue" in p:
            temp_k = 5600.0

        contrast_val = 0.50
        if "high contrast" in p or "punchy" in p:
            contrast_val = 0.60
        elif "low contrast" in p or "flat" in p:
            contrast_val = 0.44

        return ColorGradeModelV2(
            temperature_kelvin=temp_k,
            tint=0.0,
            exposure_ev=0.0,
            contrast=contrast_val,
            highlights_softknee=0.2,
            shadows_softknee=0.1,
            look_dna_summary=LookDNASummaryV2(
                mood="cinematic, balanced",
                temperature_profile="warm overall" if temp_k > 6500 else ("cool overall" if temp_k < 6500 else "neutral"),
                confidence=0.70,
            ),
        )

    @classmethod
    def _generate_palette_from_v2(cls, model: ColorGradeModelV2) -> list[str]:
        # Generate 5 swatches
        is_warm = model.temperature_kelvin > 6500
        shadow_hex = "#131e24" if model.color_wheels.lift.b > 0.02 else "#171717"
        mid_hex = "#5c554e" if is_warm else "#484f54"
        green_hex = "#485344" if model.hsl_bands.green.sat < -0.1 else "#3b6934"
        skin_hex = "#c89474"
        highlight_hex = "#f5ebd4" if is_warm else "#e8ecf0"
        return [shadow_hex, mid_hex, green_hex, skin_hex, highlight_hex]

    @classmethod
    async def _call_gemini_v2(cls, prompt: str) -> Optional[ColorGradeModelV2]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
        payload = {
            "contents": [
                {"parts": [{"text": f"{SYSTEM_PROMPT_STYLE_INTERPRETER_V2}\n\nUser Request: {prompt}"}]}
            ],
            "generationConfig": {"response_mime_type": "application/json"},
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(text)
                return ColorGradeModelV2(**parsed)
        return None

    @classmethod
    async def _call_openai_v2(cls, prompt: str) -> Optional[ColorGradeModelV2]:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT_STYLE_INTERPRETER_V2},
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_object"},
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                parsed = json.loads(data["choices"][0]["message"]["content"])
                return ColorGradeModelV2(**parsed)
        return None
