"""
Template Fayllar Handler
PPTX shablonlarini ochish va AI content bilan to'ldirish
"""

import os
import glob
import shutil
from pptx import Presentation
from pptx.util import Pt
from pptx.enum.text import PP_ALIGN
import logging

logger = logging.getLogger(__name__)

# Template papka
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

# Fayl nomlari mapping (ID → fayl nomi pattern)
TEMPLATE_FILENAMES = {
    "1_biznes_moliya": {
        1: "1_*",
        2: "2_*",
        3: "3_*",
        4: "4_*",
        5: "5_*",
        6: "6_*",
        7: "7_*",
        8: "8_*",
        9: "9_*",
        10: "10_*"
    },
    "2_talim_pedagogika": {i: f"{i}_*" for i in range(1, 11)},
    "3_texnologiya_it": {i: f"{i}_*" for i in range(1, 12)},
    "4_tibbiyot_soglik": {i: f"{i}_*" for i in range(1, 11)},
    "5_adabiyot_tilshunoslik": {i: f"{i}_*" for i in range(1, 11)},
    "6_ijtimoiy_fanlar": {i: f"{i}_*" for i in range(1, 12)},
    "7_fan_tadqiqot": {i: f"{i}_*" for i in range(1, 10)},
    "8_tarix_madaniyat": {i: f"{i}_*" for i in range(1, 11)},
    "9_tabiat_ekologiya": {i: f"{i}_*" for i in range(1, 11)},
    "10_kreativ_universal": {i: f"{i}_*" for i in range(1, 11)}
}


def find_template_file(category: str, template_id: int) -> str | None:
    """Template faylni topish"""
    try:
        # Category papkasi
        category_dir = os.path.join(TEMPLATES_DIR, category.replace("_", " "))
        
        if not os.path.exists(category_dir):
            logger.error(f"Template papka topilmadi: {category_dir}")
            return None
        
        # Fayl pattern
        pattern = TEMPLATE_FILENAMES.get(category, {}).get(template_id)
        if not pattern:
            logger.error(f"Template ID topilmadi: {category}/{template_id}")
            return None
        
        # Glob bilan qidirish
        search_pattern = os.path.join(category_dir, f"{pattern}.pptx")
        files = glob.glob(search_pattern)
        
        if files:
            logger.info(f"✅ Template topildi: {files[0]}")
            return files[0]
        else:
            logger.error(f"Template fayl topilmadi: {search_pattern}")
            return None
            
    except Exception as e:
        logger.error(f"Template qidirishda xato: {e}")
        return None


def fill_template_slides(template_path: str, content_data: dict, output_path: str) -> bool:
    """
    Template faylni AI content bilan to'ldirish
    
    Args:
        template_path: Template PPTX fayl yo'li
        content_data: AI dan kelgan content {title, subtitle, slides: [...]}
        output_path: Natija fayl yo'li
    
    Returns:
        bool: Muvaffaqiyatli yoki yo'q
    """
    try:
        # Template ni ochish
        prs = Presentation(template_path)
        logger.info(f"✅ Template ochildi: {len(prs.slides)} ta slayd")
        
        # 1. Title slide (birinchi slayd)
        if len(prs.slides) > 0:
            slide = prs.slides[0]
            _fill_title_slide(slide, content_data.get("title", ""), content_data.get("subtitle", ""))
        
        # 2. Content slides
        slides_data = content_data.get("slides", [])
        for idx, slide_content in enumerate(slides_data, start=1):
            if idx < len(prs.slides):
                slide = prs.slides[idx]
                _fill_content_slide(slide, slide_content)
        
        # 3. Saqlash
        prs.save(output_path)
        logger.info(f"✅ Taqdimot saqlandi: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Template to'ldirishda xato: {e}")
        return False


def _fill_title_slide(slide, title: str, subtitle: str):
    """Title slide ni to'ldirish"""
    try:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            
            text_frame = shape.text_frame
            
            # Title placeholder
            if shape.is_placeholder:
                ph_type = shape.placeholder_format.type
                
                # Title (1) yoki Center Title (3)
                if ph_type in [1, 3]:
                    text_frame.clear()
                    p = text_frame.paragraphs[0]
                    p.text = title
                    p.alignment = PP_ALIGN.CENTER
                    for run in p.runs:
                        run.font.bold = True
                        run.font.size = Pt(44)
                
                # Subtitle (2)
                elif ph_type == 2:
                    text_frame.clear()
                    p = text_frame.paragraphs[0]
                    p.text = subtitle
                    p.alignment = PP_ALIGN.CENTER
                    for run in p.runs:
                        run.font.size = Pt(20)
            
            # Agar placeholder bo'lmasa, birinchi 2 ta text shape
            elif not text_frame.text.strip():
                text_frame.text = title if not title else subtitle
                
    except Exception as e:
        logger.warning(f"Title slide xatosi: {e}")


def _fill_content_slide(slide, content: dict):
    """Content slide ni to'ldirish"""
    try:
        title = content.get("title", "")
        points = content.get("points", [])
        
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            
            text_frame = shape.text_frame
            
            # Title placeholder
            if shape.is_placeholder:
                ph_type = shape.placeholder_format.type
                
                # Title (1)
                if ph_type == 1:
                    text_frame.clear()
                    p = text_frame.paragraphs[0]
                    p.text = title
                    p.alignment = PP_ALIGN.LEFT
                    for run in p.runs:
                        run.font.bold = True
                        run.font.size = Pt(32)
                
                # Content/Body (2)
                elif ph_type == 2:
                    text_frame.clear()
                    for point in points:
                        p = text_frame.add_paragraph()
                        p.text = point
                        p.level = 0
                        p.space_before = Pt(6)
                        for run in p.runs:
                            run.font.size = Pt(18)
            
            # Generic text box
            elif text_frame.text.strip() == "":
                # Bo'sh text box ni birinchi point bilan to'ldirish
                if points:
                    text_frame.text = "\n".join(f"• {p}" for p in points[:3])
                    
    except Exception as e:
        logger.warning(f"Content slide xatosi: {e}")


def create_presentation_from_template(
    category: str,
    template_id: int,
    content_data: dict,
    output_filename: str
) -> str | None:
    """
    Template asosida taqdimot yaratish
    
    Returns:
        str | None: Output fayl yo'li yoki None
    """
    try:
        # 1. Template faylni topish
        template_path = find_template_file(category, template_id)
        if not template_path:
            logger.error("Template fayl topilmadi!")
            return None
        
        # 2. Output yo'lini tayyorlash
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_filename)
        
        # 3. Template ni to'ldirish
        success = fill_template_slides(template_path, content_data, output_path)
        
        if success:
            return output_path
        else:
            return None
            
    except Exception as e:
        logger.error(f"Presentation yaratishda xato: {e}")
        return None
