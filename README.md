# THEARA COLOR

> **Create Your Look.**
> Founded by **Krai Theara**

AI-powered color grading and 3D LUT/preset generation SaaS platform for creators, cinematographers, and photographers.

---

## Key Capabilities

1. **Deterministic Mathematical Color Engine (`backend/color_engine/`)**:
   - Independent Python color science package.
   - Converts natural language into a structured, bounded color model (`ColorGradeModel`).
   - 3-Way Color Wheels (Lift / Gamma / Gain), 8-Band Vector HSL, Cubic Spline Tone Curves, Soft-Knee Highlights/Shadows, Matte Film Fade, Organic Silver Grain, and Vignette falloff.
2. **Industry-Standard 33×33×33 3D LUT Generation**:
   - Generates Adobe `.cube` 3D LUTs (35,937 points) with sub-100ms compilation time and strict syntax validation.
   - Generates Adobe Camera Raw / Lightroom `.xmp` presets.
3. **Reference Image Color Matching**:
   - Statistical CIE L\*a\*b\* moment differentials, Reinhard color transfer estimation, and luminance percentile ratio analysis.
4. **Look DNA**:
   - Analytical fingerprint of every look displaying mood, temperature profile, contrast profile, shadow/highlight toning, and a 5-color harmonic palette.
5. **Transactional Credit Economics**:
   - Atomic balance check and deduction preventing race conditions, with automatic refund on pipeline errors.
6. **Supabase PostgreSQL Schema & Security**:
   - Full Row-Level Security (RLS) policies, atomic PL/pgSQL deduction function, and storage segregation.
7. **Creator Workstation UI (`frontend/`)**:
   - Next.js 14 App Router, TypeScript, Tailwind CSS.
   - Interactive Before/After split comparison slider with touch/mouse drag, side-by-side, and press-and-hold modes.
   - Zoom (Fit, 100%, 200%) and Fullscreen toggles.
   - Public looks community explorer with "Try This Look" functionality and shareable `/look/[slug]` URLs.

---

## Quick Start Guide

### Prerequisites
- Node.js 18+ (Tested on v24.18.0)
- Python 3.10+ (Tested on v3.12.9)

### 1. Backend Setup

```bash
# Navigate to backend and install dependencies
cd backend
pip install -r requirements.txt

# Seed initial demo assets & community looks
python seed_demo.py

# Launch FastAPI backend server (port 8000)
python app/main.py
```

FastAPI server runs at `http://127.0.0.1:8000` with Swagger docs at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup

```bash
# Navigate to frontend and install dependencies
cd frontend
npm install

# Start Next.js development server (port 3000)
npm run dev
```

Open `http://localhost:3000` to access THEARA COLOR Studio.

---

## Running the Automated Test Suite

```bash
# Run Color Engine & LUT validity tests
python tests/test_color_engine.py

# Run API & Credit transactional integration tests
python tests/test_api_endpoints.py
```

---

## Project Structure

```
.
├── backend/
│   ├── color_engine/           # Pure mathematical color processing engine
│   │   ├── models.py           # ColorGradeModel, LookDNA, CurveSettings
│   │   ├── transforms.py       # Deterministic master rendering pipeline
│   │   ├── exposure.py         # EV compensation, contrast, whites/blacks
│   │   ├── temperature.py      # White balance Kelvin & tint
│   │   ├── highlights_shadows.py # Soft-knee tonal weighting
│   │   ├── curves.py           # PCHIP monotonic spline interpolation
│   │   ├── hsl.py              # 8-band vector HSL processing
│   │   ├── color_wheels.py     # 3-way Lift, Gamma, Gain
│   │   ├── film_effects.py     # Grain, matte fade, vignette
│   │   ├── lut.py              # Adobe .cube 33x33x33 generator & validator
│   │   ├── xmp.py              # Adobe Camera Raw .xmp preset generator
│   │   └── reference.py        # Statistical color matching
│   ├── app/
│   │   ├── api/v1/             # FastAPI route controllers (auth, assets, generations, looks, credits)
│   │   ├── core/               # Security, settings, JWT
│   │   ├── db/                 # SQLite / Supabase database adapter
│   │   └── services/           # AI style interpreter, credit service, project service, export service
│   ├── supabase/
│   │   └── schema.sql          # Production Supabase PostgreSQL schema with RLS & functions
│   └── seed_demo.py            # Initial test assets and curated look generator
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx            # Marketing Landing Page with live Before/After hero
│   │   ├── generator/page.tsx  # 3-Pane Creative Workstation
│   │   ├── dashboard/page.tsx  # Projects, saved looks, credit balance
│   │   ├── explore/page.tsx    # Public looks community library
│   │   └── look/[slug]/page.tsx# Shareable look page
│   ├── components/
│   │   ├── Navbar.tsx          # Global navigation with credits indicator
│   │   └── generator/          # BeforeAfterSlider, LookDNACard, BasicControls, AdvancedControls
│   └── lib/                    # API client and TypeScript types
│
└── tests/
    ├── test_color_engine.py    # Unit tests for transforms, LUT syntax, XMP XML
    └── test_api_endpoints.py   # Integration tests for upload, generation, credits, exports
```

