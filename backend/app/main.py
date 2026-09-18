"""
THEARA COLOR — Backend Application Root
Product: THEARA COLOR
Tagline: Create Your Look.
Founder: Krai Theara
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1 import auth, projects, assets, generations, looks, credits

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-powered color grading and LUT/preset generation platform for creators.",
    version=settings.VERSION,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Supports both localhost:3000 and production Vercel domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount local storage folder for uploaded assets and generated previews
app.mount("/storage", StaticFiles(directory=settings.STORAGE_DIR), name="storage")

# Register V1 API Routes
app.include_router(auth.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(assets.router, prefix="/api/v1")
app.include_router(generations.router, prefix="/api/v1")
app.include_router(looks.router, prefix="/api/v1")
app.include_router(credits.router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "product": settings.PROJECT_NAME,
        "tagline": settings.PRODUCT_TAGLINE,
        "founder": settings.FOUNDER,
        "version": settings.VERSION,
        "status": "operational",
        "color_engine": "online",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.BACKEND_HOST, port=settings.BACKEND_PORT, reload=True)

