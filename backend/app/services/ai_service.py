"""
THEARA COLOR — AI Style Interpreter & Provider Abstraction
Founder: Krai Theara | "Create Your Look"
"""

import json
import re
from typing import Tuple, Optional
import httpx
from color_engine.models import (
    ColorGradeModel,
    LookDNA,
    CurveSettings,
    CurvePoint,
    HSLSettings,
    HSLChannel,
    ColorWheelsSettings,
    ColorWheel,
)
from app.core.config import settings


class AIStyleInterpreter:
    """
    Translates creator natural language prompts into structured ColorGradeModel parameters and Look DNA.
    Supports live LLM providers (Gemini / OpenAI) and includes a deterministic semantic color intelligence engine.
    """

    @classmethod
    async def interpret_prompt(
        cls,
        prompt: str,
        base_grade: Optional[ColorGradeModel] = None,
    ) -> Tuple[ColorGradeModel, LookDNA]:
        prompt_lower = prompt.lower().strip()

        # Try Live LLM if API key is configured
        if settings.GEMINI_API_KEY and settings.AI_PROVIDER in ("auto", "gemini"):
            try:
                res = await cls._call_gemini(prompt)
                if res:
                    return res
            except Exception as e:
                print(f"[AI Service] Gemini fallback due to: {e}")

        if settings.OPENAI_API_KEY and settings.AI_PROVIDER in ("auto", "openai"):
            try:
                res = await cls._call_openai(prompt)
                if res:
                    return res
            except Exception as e:
                print(f"[AI Service] OpenAI fallback due to: {e}")

        # Deterministic Semantic Color Intelligence Engine
        return cls._semantic_color_engine(prompt_lower, base_grade)

    @classmethod
    def _semantic_color_engine(
        cls,
        prompt: str,
        base_grade: Optional[ColorGradeModel] = None,
    ) -> Tuple[ColorGradeModel, LookDNA]:
        grade = base_grade.model_copy(deep=True) if base_grade else ColorGradeModel()

        # Extract emotional & aesthetic dimensions
        is_warm = any(w in prompt for w in ["warm", "golden", "sunset", "amber", "summer", "sunlit", "desert", "fire", "glow", "resort"])
        is_cool = any(w in prompt for w in ["cool", "cold", "blue", "ice", "winter", "slate", "nordic", "scandinavian", "frost", "cyber"])
        is_cinematic = any(w in prompt for w in ["cinematic", "film", "movie", "hollywood", "anamorphic", "35mm", "kodak", "blockbuster"])
        is_moody = any(w in prompt for w in ["moody", "dark", "dramatic", "shadow", "deep", "mysterious", "melancholy", "night", "noir"])
        is_luxury = any(w in prompt for w in ["luxury", "editorial", "vogue", "commercial", "high-end", "premium", "fashion", "magazine"])
        is_vintage = any(w in prompt for w in ["vintage", "retro", "nostalgic", "grain", "polaroid", "matte", "fade", "70s", "80s", "analog"])
        is_clean = any(w in prompt for w in ["clean", "natural", "neutral", "minimal", "fresh", "bright", "crisp", "true to life", "wedding"])
        is_muted = any(w in prompt for w in ["muted", "desaturated", "pastel", "soft", "faded", "subtle", "understated"])
        is_vibrant = any(w in prompt for w in ["vibrant", "punchy", "colorful", "tropical", "rich", "saturated", "pop"])
        is_teal_orange = any(w in prompt for w in ["teal and orange", "teal & orange", "blockbuster", "hollywood teal"])

        # 1. Exposure & Contrast
        if is_moody:
            grade.exposure -= 0.4
            grade.contrast += 25.0
            grade.shadows -= 25.0
            grade.highlights -= 10.0
            grade.blacks -= 15.0
            grade.vignette += 25.0
        elif is_clean or "bright" in prompt or "high key" in prompt:
            grade.exposure += 0.35
            grade.contrast += 8.0
            grade.highlights -= 15.0  # soft highlight recovery
            grade.shadows += 15.0     # open shadows
            grade.whites += 10.0
        elif is_luxury:
            grade.contrast += 18.0
            grade.highlights -= 20.0
            grade.shadows += 10.0
            grade.whites += 12.0
            grade.blacks -= 10.0

        if is_cinematic:
            grade.contrast += 15.0
            grade.shadows -= 15.0

        # 2. Temperature & Tint
        if is_warm:
            grade.temperature += 28.0
            grade.tint += 4.0
        elif is_cool:
            grade.temperature -= 26.0
            grade.tint -= 6.0

        if "golden hour" in prompt or "sunset" in prompt:
            grade.temperature += 35.0
            grade.tint += 8.0
            grade.highlights += 5.0

        # 3. Saturation & Vibrance
        if is_muted:
            grade.saturation -= 22.0
            grade.vibrance -= 10.0
        elif is_vibrant:
            grade.saturation += 18.0
            grade.vibrance += 25.0
        else:
            # Default tasteful commercial saturation
            grade.vibrance += 10.0

        # 4. Matte Fade & Grain
        if is_vintage:
            grade.fade = 28.0
            grade.grain = 32.0
            grade.contrast -= 10.0
            grade.highlights -= 25.0
        elif is_cinematic:
            grade.grain = 16.0
            grade.fade = 10.0

        # 5. Selective 8-Vector HSL
        if "muted greens" in prompt or is_cinematic or is_luxury or is_moody:
            grade.hsl.green.saturation = -38.0
            grade.hsl.green.luminance = -10.0
            grade.hsl.yellow.saturation = -18.0

        if "skin" in prompt or is_luxury or is_clean:
            # Protect / warm skin tones (Orange & Red vectors)
            grade.hsl.orange.saturation = +12.0
            grade.hsl.orange.luminance = +8.0
            grade.hsl.red.saturation = +6.0

        if "deep sky" in prompt or "ocean" in prompt or is_cinematic:
            grade.hsl.blue.luminance = -22.0
            grade.hsl.blue.saturation = +10.0
            grade.hsl.aqua.luminance = -15.0

        # 6. Color Wheels (Split Toning / 3-Way)
        if is_teal_orange or (is_cinematic and is_warm):
            # Teal shadows: Hue ~195° (Cyan-Teal)
            grade.color_wheels.lift = ColorWheel(hue=195.0, saturation=0.22, luminance=-0.05)
            # Orange highlights: Hue ~35° (Amber-Orange)
            grade.color_wheels.gain = ColorWheel(hue=35.0, saturation=0.26, luminance=0.05)
            # Neutral warm midtones
            grade.color_wheels.gamma = ColorWheel(hue=45.0, saturation=0.08, luminance=0.0)
        elif is_cool or is_moody:
            # Deep slate blue shadows: Hue ~215°
            grade.color_wheels.lift = ColorWheel(hue=215.0, saturation=0.20, luminance=-0.08)
            grade.color_wheels.gain = ColorWheel(hue=50.0, saturation=0.08, luminance=0.02)
        elif is_warm:
            grade.color_wheels.lift = ColorWheel(hue=30.0, saturation=0.10, luminance=-0.02)
            grade.color_wheels.gain = ColorWheel(hue=40.0, saturation=0.22, luminance=0.04)

        # 7. S-Curve in Tone Curves
        if is_cinematic or is_luxury:
            grade.curves.master = [
                CurvePoint(x=0.0, y=0.0),
                CurvePoint(x=0.25, y=0.20),  # Toe compression
                CurvePoint(x=0.5, y=0.50),   # Linear midtone
                CurvePoint(x=0.75, y=0.82),  # Shoulder boost
                CurvePoint(x=1.0, y=1.0),
            ]

        # Determine Look DNA
        mood_title = "Cinematic Look"
        if is_warm and is_luxury:
            mood_title = "Warm Luxury Cinema"
        elif is_warm and is_moody:
            mood_title = "Golden Hour Noir"
        elif is_cool and is_moody:
            mood_title = "Moody Nordic Slate"
        elif is_vintage:
            mood_title = "35mm Analog Vintage"
        elif is_clean:
            mood_title = "Pristine Commercial Clean"
        elif is_warm:
            mood_title = "Golden Sunset Glow"
        elif is_cool:
            mood_title = "Cool Cyber Film"

        palette = cls._generate_palette_from_grade(grade)

        tags = []
        if is_cinematic: tags.append("Cinematic")
        if is_warm: tags.append("Golden Hour")
        if is_cool: tags.append("Cool Tones")
        if is_vintage: tags.append("35mm Film")
        if is_luxury: tags.append("Luxury")
        if is_moody: tags.append("Moody")
        if is_clean: tags.append("Clean")
        if not tags: tags = ["Creative", "Creator Grade"]

        dna = LookDNA(
            mood=mood_title,
            temperature_profile=f"{'Warm Golden' if grade.temperature > 0 else 'Cool Slate'} ({grade.temperature:+.0f})",
            contrast_profile=f"{'High Dynamic S-Curve' if grade.contrast > 10 else 'Soft Filmic'} ({grade.contrast:+.0f})",
            saturation_profile=f"{'Muted Selective' if grade.saturation < 0 else 'Rich Balanced'}",
            highlight_character="Soft Amber Rolloff" if grade.color_wheels.gain.saturation > 0.1 else "Clean Specular",
            shadow_character="Deep Teal Shadows" if grade.color_wheels.lift.saturation > 0.1 else "Natural Black",
            color_palette=palette,
            key_tags=tags[:5],
        )

        return grade, dna

    @staticmethod
    def _generate_palette_from_grade(grade: ColorGradeModel) -> list[str]:
        # Generate 5 characteristic hex colors reflecting the grade's shadow, midtone, skin, highlight, and accent
        lift_sat = grade.color_wheels.lift.saturation
        gain_sat = grade.color_wheels.gain.saturation
        temp = grade.temperature

        # Shadow color
        if lift_sat > 0.1:
            shadow_hex = "#121e24" if grade.color_wheels.lift.hue > 150 else "#1f1814"
        else:
            shadow_hex = "#161616"

        # Midtone
        mid_hex = "#5c554e" if temp > 10 else ("#47525a" if temp < -10 else "#545454")

        # Foliage / Green vector
        green_hex = "#485344" if grade.hsl.green.saturation < -20 else "#40693a"

        # Skin tone
        skin_hex = "#c89474" if temp > 0 else "#ba8f78"

        # Highlight
        highlight_hex = "#f5ebd4" if (gain_sat > 0.1 or temp > 10) else "#eaeef2"

        return [shadow_hex, mid_hex, green_hex, skin_hex, highlight_hex]

    @classmethod
    async def _call_gemini(cls, prompt: str) -> Optional[Tuple[ColorGradeModel, LookDNA]]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
        system_instruction = (
            "You are THEARA COLOR AI, a professional colorist engine. "
            "Convert the user's natural language color grading request into a structured JSON ColorGradeModel and LookDNA. "
            "Return valid JSON ONLY with keys: exposure (-5..5), contrast (-100..100), highlights (-100..100), shadows (-100..100), "
            "whites (-100..100), blacks (-100..100), temperature (-100..100), tint (-100..100), saturation (-100..100), "
            "vibrance (-100..100), fade (0..100), grain (0..100), vignette (-100..100), mood, temperature_profile, "
            "contrast_profile, saturation_profile, highlight_character, shadow_character, color_palette (5 hex strings), key_tags."
        )
        payload = {
            "contents": [{"parts": [{"text": f"{system_instruction}\n\nUser Request: {prompt}"}]}],
            "generationConfig": {"response_mime_type": "application/json"},
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(text)
                grade = ColorGradeModel(**{k: parsed[k] for k in ColorGradeModel.model_fields if k in parsed})
                dna = LookDNA(**{k: parsed[k] for k in LookDNA.model_fields if k in parsed})
                return grade, dna
        return None

    @classmethod
    async def _call_openai(cls, prompt: str) -> Optional[Tuple[ColorGradeModel, LookDNA]]:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are THEARA COLOR AI colorist engine. Output JSON matching ColorGradeModel and LookDNA."},
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_object"},
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                parsed = json.loads(data["choices"][0]["message"]["content"])
                grade = ColorGradeModel(**{k: parsed[k] for k in ColorGradeModel.model_fields if k in parsed})
                dna = LookDNA(**{k: parsed[k] for k in LookDNA.model_fields if k in parsed})
                return grade, dna
        return None

