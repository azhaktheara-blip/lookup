"""
Generates beautiful sample images for THEARA COLOR demo & initial state.
"""

import os
import numpy as np
from PIL import Image, ImageDraw

storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend", "storage"))
uploads_dir = os.path.join(storage_dir, "uploads")
previews_dir = os.path.join(storage_dir, "previews")
os.makedirs(uploads_dir, exist_ok=True)
os.makedirs(previews_dir, exist_ok=True)

# Generate a 800x533 sunset landscape with horizon, mountains, and sun
w, h = 800, 533
y = np.linspace(0, 1, h, dtype=np.float32)[:, np.newaxis]
x = np.linspace(0, 1, w, dtype=np.float32)[np.newaxis, :]

# Sky gradient
sky_r = 0.85 - 0.5 * y
sky_g = 0.65 - 0.4 * y
sky_b = 0.50 + 0.3 * (1.0 - y)
sky = np.stack([sky_r, sky_g, sky_b], axis=-1)

# Mountain silhouette
mountain_h = 0.55 + 0.15 * np.sin(x * 12.0) + 0.08 * np.cos(x * 24.0)
mountain_mask = (y > mountain_h)[..., np.newaxis]

mountain_color = np.array([0.18, 0.22, 0.28], dtype=np.float32).reshape(1, 1, 3)
mountain_shading = (mountain_color * (1.2 - 0.4 * y[..., np.newaxis])).repeat(w, axis=1)

landscape = np.where(mountain_mask, mountain_shading, sky)
landscape = np.clip(landscape, 0.0, 1.0)

# Sun glow
sun_x, sun_y = 0.65, 0.48
dist_sun = np.sqrt((x - sun_x)**2 + (y - sun_y)**2)
glow = np.exp(-dist_sun * 8.0)[..., np.newaxis]
landscape += glow * np.array([0.4, 0.25, 0.05]).reshape(1, 1, 3)
landscape = np.clip(landscape, 0.0, 1.0)

raw_uint8 = (landscape * 255).astype(np.uint8)
raw_img = Image.fromarray(raw_uint8, mode="RGB")

# Save as demo_original.jpg
orig_path = os.path.join(uploads_dir, "demo_original.jpg")
raw_img.save(orig_path, "JPEG", quality=95)

# Generate Graded version using Color Engine
import sys
sys.path.insert(0, os.path.abspath("backend"))
from color_engine import ColorGradeModel, process_image, ColorWheel
from app.db.database import get_db

demo_grade = ColorGradeModel(
    exposure=0.15,
    contrast=22.0,
    highlights=-15.0,
    shadows=-10.0,
    temperature=32.0,
    tint=5.0,
    saturation=12.0,
    vibrance=20.0,
    fade=8.0,
    grain=12.0,
    vignette=18.0,
)
demo_grade.color_wheels.lift = ColorWheel(hue=195.0, saturation=0.18, luminance=-0.04)
demo_grade.color_wheels.gain = ColorWheel(hue=38.0, saturation=0.25, luminance=0.04)

graded_img = process_image(raw_img, demo_grade)
graded_path = os.path.join(previews_dir, "demo_graded.webp")
graded_img.save(graded_path, "WEBP", quality=92)

# Insert sample asset & public looks into DB
conn = get_db()
cursor = conn.cursor()
cursor.execute("SELECT id FROM assets WHERE id = 'demo-asset-001'")
if not cursor.fetchone():
    cursor.execute("""
        INSERT INTO assets (id, project_id, user_id, asset_type, storage_path, filename, mime_type, file_size, width, height)
        VALUES ('demo-asset-001', NULL, '00000000-0000-0000-0000-000000000001', 'original', 'uploads/demo_original.jpg', 'golden_mountain.jpg', 'image/jpeg', 85000, 800, 533)
    """)

# Add curated public looks
curated_looks = [
    ("Golden Hour Cinema", "golden-hour-cinema", "Warm cinematic commercial grade with amber highlights, teal shadows, and rich contrast.", "Cinematic", demo_grade.model_dump_json(), '{"mood":"Warm Golden Cinema","temperature_profile":"Golden Warm (+32)","contrast_profile":"Punchy S-Curve (+22)","saturation_profile":"Rich Commercial (+12)","highlight_character":"Soft Amber Glow","shadow_character":"Deep Cinematic Teal","color_palette":["#131e24","#5c554e","#485344","#c89474","#f5ebd4"],"key_tags":["Cinematic","Golden Hour","Teal & Orange"]}'),
    ("Nordic Thriller 35mm", "nordic-thriller-35mm", "Moody cool Scandinavian cinema aesthetic with slate blue shadows and desaturated foliage.", "Moody", '{"exposure":-0.2,"contrast":28.0,"temperature":-25.0,"tint":-6.0,"saturation":-20.0,"fade":12.0,"grain":24.0,"vignette":22.0}', '{"mood":"Moody Nordic Slate","temperature_profile":"Cool Slate (-25)","contrast_profile":"High Dynamic (+28)","saturation_profile":"Muted Selective (-20)","highlight_character":"Cold Specular","shadow_character":"Slate Charcoal","color_palette":["#10151a","#36414a","#3f4842","#92a1a8","#e0e8ed"],"key_tags":["Moody","Nordic","35mm"]}'),
    ("Vogue Luxury Minimal", "vogue-luxury-minimal", "High-fashion editorial grade with pristine skin tones, softened highlights, and deep velvet blacks.", "Fashion", '{"exposure":0.1,"contrast":16.0,"highlights":-20.0,"shadows":8.0,"temperature":8.0,"vibrance":14.0,"whites":12.0,"blacks":-8.0}', '{"mood":"Luxury Editorial","temperature_profile":"Neutral Warm (+8)","contrast_profile":"Clean Contrast (+16)","saturation_profile":"Balanced Skin","highlight_character":"Soft Roll-off","shadow_character":"Velvet Black","color_palette":["#1a1918","#4a4744","#7a7671","#c49d83","#faf7f2"],"key_tags":["Luxury","Fashion","Editorial"]}'),
    ("35mm Portra Vintage", "35mm-portra-vintage", "Analog film emulation inspired by Kodak Portra 400 with lifted matte shadows and organic silver grain.", "Vintage", '{"exposure":0.05,"contrast":-8.0,"temperature":18.0,"tint":6.0,"saturation":-10.0,"vibrance":12.0,"fade":25.0,"grain":30.0}', '{"mood":"Analog Film Portra","temperature_profile":"Warm Analog (+18)","contrast_profile":"Matte Lifted (-8)","saturation_profile":"Pastel Rolloff","highlight_character":"Creamy Whites","shadow_character":"Lifted Matte","color_palette":["#2b2824","#574e44","#8c7f6f","#d4aa8b","#fdf5eb"],"key_tags":["Vintage","35mm Film","Portra"]}')
]

for title, slug, prompt, cat, params_json, dna_json in curated_looks:
    cursor.execute("SELECT id FROM looks WHERE slug = ?", (slug,))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO looks (id, project_id, user_id, title, slug, prompt, parameters, look_dna, original_asset_id, preview_url, is_public, category, downloads_count)
            VALUES (?, NULL, '00000000-0000-0000-0000-000000000001', ?, ?, ?, ?, ?, 'demo-asset-001', '/storage/previews/demo_graded.webp', 1, ?, 142)
        """, (f"look-{slug}", title, slug, prompt, params_json, dna_json, cat))

conn.commit()
conn.close()
print("Sample demo assets and curated community looks generated successfully!")
