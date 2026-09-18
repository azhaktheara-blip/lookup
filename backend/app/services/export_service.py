"""
THEARA COLOR — Export Service (.cube 33x33x33 & .xmp presets)
Founder: Krai Theara | "Create Your Look"
"""

import uuid
import os
from typing import Dict, Any, Tuple
from app.db.database import get_db
from app.core.config import settings
from color_engine.models import ColorGradeModel
from color_engine.lut import generate_cube_lut, validate_cube_syntax
from color_engine.xmp import generate_xmp_preset


class ExportService:

    @classmethod
    def export_look(
        cls,
        user_id: str,
        look_id: str,
        export_format: str,  # "cube" or "xmp"
        grade: ColorGradeModel,
        look_title: str = "THEARA COLOR LOOK",
        lut_size: int = 33,
    ) -> Tuple[str, str, str]:
        """
        Generates the export file, validates syntax, records in database,
        and returns (export_id, storage_relative_path, filename).
        """
        export_id = str(uuid.uuid4())

        if export_format.lower() == "cube":
            filename = f"{look_title.replace(' ', '_')}_{lut_size}x.cube"
            content = generate_cube_lut(grade, size=lut_size, title=look_title)
            is_valid, msg = validate_cube_syntax(content)
            if not is_valid:
                raise ValueError(f"Generated LUT failed syntax validation: {msg}")
            file_bytes = content.encode("utf-8")
        elif export_format.lower() == "xmp":
            filename = f"{look_title.replace(' ', '_')}.xmp"
            content = generate_xmp_preset(grade, preset_name=look_title)
            file_bytes = content.encode("utf-8")
        else:
            raise ValueError(f"Unsupported export format: {export_format}")

        rel_path = os.path.join("exports", f"{export_id}_{filename}")
        abs_path = os.path.join(settings.STORAGE_DIR, rel_path)

        with open(abs_path, "wb") as f:
            f.write(file_bytes)

        # Record in DB
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO exports (id, look_id, user_id, format, lut_size, storage_path)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (export_id, look_id, user_id, export_format.lower(), lut_size, rel_path))

        # Increment download count on the look
        cursor.execute("UPDATE looks SET downloads_count = downloads_count + 1 WHERE id = ?", (look_id,))
        conn.commit()
        conn.close()

        return export_id, abs_path, filename

