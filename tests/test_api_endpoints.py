"""
Unit & Integration tests for THEARA COLOR FastAPI endpoints and Credit transactional integrity.
"""

import sys
import os
import io
from PIL import Image

sys.path.insert(0, os.path.abspath("backend"))

from fastapi.testclient import TestClient
from app.main import app
from app.services.credit_service import CreditService

client = TestClient(app)


def test_root_endpoint():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["product"] == "THEARA COLOR"
    assert data["founder"] == "Krai Theara"
    assert data["color_engine"] == "online"


def test_credit_deduction_and_refund():
    test_user_id = "test-user-credit-001"
    # Seed user credit
    bal = CreditService.get_balance(test_user_id)
    initial_balance = bal["balance"]

    # Deduct
    success, msg = CreditService.deduct_credits(test_user_id, 10, "generation", description="Test deduct")
    assert success is True
    updated_bal = CreditService.get_balance(test_user_id)
    assert updated_bal["balance"] == initial_balance - 10

    # Over-deduction should fail
    fail_success, fail_msg = CreditService.deduct_credits(test_user_id, 999999, "generation")
    assert fail_success is False

    # Refund
    refund_res = CreditService.refund_credits(test_user_id, 10, reason="Test refund")
    assert refund_res is True
    refunded_bal = CreditService.get_balance(test_user_id)
    assert refunded_bal["balance"] == initial_balance


def test_full_generation_pipeline():
    # 1. Upload a dummy test image
    img = Image.new("RGB", (100, 100), color=(180, 120, 90))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    upload_resp = client.post(
        "/api/v1/assets/upload",
        files={"file": ("sample.jpg", buf, "image/jpeg")},
        data={"asset_type": "original"},
    )
    assert upload_resp.status_code == 200
    asset_data = upload_resp.json()
    asset_id = asset_data["id"]

    # 2. Trigger AI generation
    gen_resp = client.post(
        "/api/v1/generations",
        json={
            "prompt": "Golden hour cinematic commercial with warm highlights and deep shadows",
            "original_asset_id": asset_id,
            "intensity": 1.0,
        }
    )
    assert gen_resp.status_code == 200
    gen_data = gen_resp.json()
    assert "parameters" in gen_data
    assert "look_dna" in gen_data
    assert "preview_url" in gen_data
    assert len(gen_data["look_dna"]["color_palette"]) > 0

    # 3. Save look
    save_resp = client.post(
        "/api/v1/looks",
        json={
            "title": "Golden Sunset Cinema",
            "prompt": "Golden hour cinematic commercial",
            "parameters": gen_data["parameters"],
            "look_dna": gen_data["look_dna"],
            "original_asset_id": asset_id,
            "preview_url": gen_data["preview_url"],
            "is_public": True,
            "category": "Cinematic",
        }
    )
    assert save_resp.status_code == 200
    look_data = save_resp.json()
    look_id = look_data["id"]

    # 4. Export .cube LUT
    export_resp = client.post(
        f"/api/v1/looks/{look_id}/export",
        json={"format": "cube", "lut_size": 17},
    )
    assert export_resp.status_code == 200
    cube_content = export_resp.text
    assert "LUT_3D_SIZE 17" in cube_content
    assert "TITLE \"Golden Sunset Cinema\"" in cube_content

    # 5. Export .xmp Preset
    xmp_resp = client.post(
        f"/api/v1/looks/{look_id}/export",
        json={"format": "xmp"},
    )
    assert xmp_resp.status_code == 200
    xmp_content = xmp_resp.text
    assert "<x:xmpmeta" in xmp_content
    assert "Golden Sunset Cinema" in xmp_content


if __name__ == "__main__":
    test_root_endpoint()
    test_credit_deduction_and_refund()
    test_full_generation_pipeline()
    print("ALL API AND SERVICE INTEGRATION TESTS PASSED!")

