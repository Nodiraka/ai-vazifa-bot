"""Suniy intellekt xizmatlari - taqdimot yaratish va matn yozish"""

import os
import io
import json
import asyncio
import logging
import requests
from openai import OpenAI
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from config import AI_MODEL, OPENAI_API_KEY, OPENAI_BASE_URL, PEXELS_API_KEY, PRESENTATION_TEMPLATES

logger = logging.getLogger(__name__)

# OpenAI client
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL if OPENAI_BASE_URL else "https://api.openai.com/v1"
)


def hex_to_rgb(hex_str: str) -> RGBColor:
    """Hex rangni RGBColor ga o'tkazish"""
    return RGBColor(int(hex_str[:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))


def get_template_colors(template_key: str) -> dict:
    """Shablon ranglarini olish"""
    template = PRESENTATION_TEMPLATES.get(template_key, PRESENTATION_TEMPLATES["business"])
    return {
        "primary": hex_to_rgb(template["color_primary"]),
        "secondary": hex_to_rgb(template["color_secondary"]),
        "accent": hex_to_rgb(template["color_accent"]),
        "text_on_primary": hex_to_rgb(template["color_text"]),
        "heading": hex_to_rgb(template["color_primary"]),
        "body": RGBColor(0x33, 0x33, 0x33),
        "light_bg": RGBColor(0xF8, 0xF9, 0xFA),
        "white": RGBColor(0xFF, 0xFF, 0xFF),
        "footer": RGBColor(0x99, 0x99, 0x99),
    }


# ===== Pexels API - bepul stock fotolar =====
def search_pexels_image(query: str, per_page: int = 1) -> str | None:
    """Pexels dan rasm qidirish va yuklab olish"""
    if not PEXELS_API_KEY or PEXELS_API_KEY == "placeholder":
        return None
    
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        params = {"query": query, "per_page": per_page, "size": "medium", "orientation": "landscape"}
        resp = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get("photos"):
                photo = data["photos"][0]
                img_url = photo["src"]["medium"]
                img_resp = requests.get(img_url, timeout=15)
                if img_resp.status_code == 200:
                    return img_resp.content
    except Exception as e:
        logger.error(f"Pexels xatolik: {e}")
    
    return None


async def search_image_async(query: str) -> bytes | None:
    """Asinxron rasm qidirish"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: search_pexels_image(query))


# ===== AI kontent yaratish =====
async def generate_presentation_content(topic: str, slides_count: int, language: str, has_images: bool = False) -> dict:
    """AI yordamida taqdimot kontentini yaratish"""
    
    lang_names = {"uz": "o'zbek", "ru": "русский", "en": "English"}
    lang_name = lang_names.get(language, "o'zbek")
    
    image_instruction = ""
    if has_images:
        image_instruction = """
- For each slide, provide an "image_query" field with 2-3 English keywords for finding a relevant image.
  Example: "image_query": "business meeting office"
"""
    
    prompt = f"""Create a professional presentation about: "{topic}"

Requirements:
- Language: {lang_name}
- Number of slides: {slides_count}
- First slide: Title slide with the topic and subtitle
- Last slide: Summary/Conclusion slide with key takeaways
- Each content slide should have a clear title and 3-5 detailed bullet points
- Content should be informative, well-structured, and professional
- Make bullet points detailed and meaningful, not just short phrases
{image_instruction}
Return ONLY valid JSON in this exact format:
{{
    "title": "Presentation Title",
    "subtitle": "Subtitle text",
    "slides": [
        {{
            "title": "Slide Title",
            "points": ["Detailed point 1", "Detailed point 2", "Detailed point 3"]{', "image_query": "relevant english keywords"' if has_images else ''}
        }}
    ]
}}

Make sure to include exactly {slides_count} slides (including title and conclusion).
All text must be in {lang_name} language.{' Image queries must be in English.' if has_images else ''}"""

    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {"role": "system", "content": "You are a professional presentation creator. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=6000
    ))
    
    content = response.choices[0].message.content.strip()
    
    # JSON ni tozalash
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()
    
    return json.loads(content)


def add_image_to_slide(slide, image_bytes: bytes, left, top, width, height):
    """Slaydga rasm qo'shish"""
    try:
        image_stream = io.BytesIO(image_bytes)
        slide.shapes.add_picture(image_stream, left, top, width, height)
        return True
    except Exception as e:
        logger.error(f"Rasm qo'shishda xatolik: {e}")
        return False


def create_pptx(content: dict, output_path: str, template_key: str = "business",
                images: dict = None) -> str:
    """Professional PowerPoint faylini yaratish"""
    
    colors = get_template_colors(template_key)
    
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    slide_width = prs.slide_width
    slide_height = prs.slide_height
    
    # ===== 1. TITUL SLAYD =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Fon
    bg_shape = slide.shapes.add_shape(1, 0, 0, slide_width, slide_height)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = colors["primary"]
    bg_shape.line.fill.background()
    
    # Dekorativ pastki chiziq
    bottom_bar = slide.shapes.add_shape(
        1, 0, slide_height - Inches(0.8), slide_width, Inches(0.8)
    )
    bottom_bar.fill.solid()
    bottom_bar.fill.fore_color.rgb = colors["secondary"]
    bottom_bar.line.fill.background()
    
    # Dekorativ accent chiziq
    accent_line = slide.shapes.add_shape(
        1, Inches(1), Inches(3.0), Inches(3), Inches(0.08)
    )
    accent_line.fill.solid()
    accent_line.fill.fore_color.rgb = colors["accent"]
    accent_line.line.fill.background()
    
    # Sarlavha
    title_box = slide.shapes.add_textbox(Inches(1), Inches(1.2), Inches(11), Inches(2.5))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = content.get("title", "Presentation")
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = colors["text_on_primary"]
    p.alignment = PP_ALIGN.LEFT
    
    # Subtitle
    subtitle_box = slide.shapes.add_textbox(Inches(1), Inches(3.5), Inches(11), Inches(1.5))
    tf2 = subtitle_box.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = content.get("subtitle", "")
    p2.font.size = Pt(24)
    p2.font.color.rgb = colors["accent"]
    p2.alignment = PP_ALIGN.LEFT
    
    # Titul slaydga rasm (agar mavjud bo'lsa)
    if images and images.get(0):
        try:
            add_image_to_slide(slide, images[0], Inches(8.5), Inches(1.5), Inches(4), Inches(3))
        except:
            pass
    
    # ===== 2-N. KONTENT SLAYDLARI =====
    slides_data = content.get("slides", [])
    
    for i, slide_data in enumerate(slides_data):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        has_image = images and images.get(i + 1)
        
        # Oq fon
        bg = slide.shapes.add_shape(1, 0, 0, slide_width, slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = colors["white"]
        bg.line.fill.background()
        
        # Chap tomonda rang chizig'i
        left_bar = slide.shapes.add_shape(1, 0, 0, Inches(0.12), slide_height)
        left_bar.fill.solid()
        left_bar.fill.fore_color.rgb = colors["primary"]
        left_bar.line.fill.background()
        
        # Yuqori sarlavha foni
        header_bg = slide.shapes.add_shape(
            1, Inches(0.12), 0, slide_width - Inches(0.12), Inches(1.3)
        )
        header_bg.fill.solid()
        header_bg.fill.fore_color.rgb = colors["light_bg"]
        header_bg.line.fill.background()
        
        # Sarlavha ostidagi accent chiziq
        header_line = slide.shapes.add_shape(
            1, Inches(0.12), Inches(1.3), slide_width - Inches(0.12), Inches(0.05)
        )
        header_line.fill.solid()
        header_line.fill.fore_color.rgb = colors["secondary"]
        header_line.line.fill.background()
        
        # Slayd raqami (chap yuqori)
        num_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(1), Inches(0.7))
        ntf = num_box.text_frame
        np_ = ntf.paragraphs[0]
        np_.text = f"{i + 1:02d}"
        np_.font.size = Pt(28)
        np_.font.bold = True
        np_.font.color.rgb = colors["secondary"]
        np_.alignment = PP_ALIGN.LEFT
        
        # Sarlavha
        title_left = Inches(1.8)
        title_box = slide.shapes.add_textbox(title_left, Inches(0.25), Inches(10), Inches(1.0))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = slide_data.get("title", f"Slide {i+1}")
        p.font.size = Pt(30)
        p.font.bold = True
        p.font.color.rgb = colors["heading"]
        p.alignment = PP_ALIGN.LEFT
        
        # Kontent maydoni - rasmga qarab kenglik o'zgaradi
        if has_image:
            content_width = Inches(7.5)
        else:
            content_width = Inches(11.5)
        
        # Bullet pointlar
        points = slide_data.get("points", [])
        content_box = slide.shapes.add_textbox(
            Inches(0.8), Inches(1.7), content_width, Inches(5.0)
        )
        tf_content = content_box.text_frame
        tf_content.word_wrap = True
        
        for j, point in enumerate(points):
            if j == 0:
                p = tf_content.paragraphs[0]
            else:
                p = tf_content.add_paragraph()
            
            p.text = f"●  {point}"
            p.font.size = Pt(18)
            p.font.color.rgb = colors["body"]
            p.space_after = Pt(16)
            p.space_before = Pt(4)
            p.alignment = PP_ALIGN.LEFT
        
        # Rasm qo'shish (agar mavjud bo'lsa)
        if has_image:
            try:
                add_image_to_slide(
                    slide, images[i + 1],
                    Inches(8.8), Inches(1.7), Inches(4.0), Inches(4.5)
                )
            except:
                pass
        
        # Pastki qism - slayd raqami
        footer_box = slide.shapes.add_textbox(
            Inches(11.5), Inches(6.9), Inches(1.5), Inches(0.4)
        )
        ftf = footer_box.text_frame
        fp = ftf.paragraphs[0]
        fp.text = f"{i + 1} / {len(slides_data)}"
        fp.font.size = Pt(11)
        fp.font.color.rgb = colors["footer"]
        fp.alignment = PP_ALIGN.RIGHT
    
    # Faylni saqlash
    prs.save(output_path)
    return output_path


async def generate_presentation(topic: str, slides_count: int, language: str,
                                 output_dir: str, template_key: str = "business",
                                 has_ai_images: bool = False) -> str:
    """To'liq taqdimot yaratish jarayoni"""
    
    # AI kontentni yaratish
    has_images = has_ai_images or bool(PEXELS_API_KEY and PEXELS_API_KEY != "placeholder")
    content = await generate_presentation_content(topic, slides_count, language, has_images=has_images)
    
    # Rasmlarni yig'ish
    images = {}
    if has_images:
        slides_data = content.get("slides", [])
        # Har 2-3 slaydda 1 ta rasm (hammaga emas)
        image_indices = []
        for idx in range(len(slides_data)):
            if idx == 0:  # Birinchi slayd
                image_indices.append(idx)
            elif idx == len(slides_data) - 1:  # Oxirgi slayd
                image_indices.append(idx)
            elif idx % 2 == 0:  # Har 2-chi slayd
                image_indices.append(idx)
        
        for idx in image_indices:
            slide_data = slides_data[idx]
            query = slide_data.get("image_query", topic)
            
            img_data = await search_image_async(query)
            if img_data:
                images[idx + 1] = img_data  # +1 chunki titul slayd 0
        
        # Titul slayd uchun ham rasm
        title_query = content.get("slides", [{}])[0].get("image_query", topic) if slides_data else topic
        title_img = await search_image_async(title_query)
        if title_img:
            images[0] = title_img
    
    # Fayl nomini yaratish
    safe_topic = "".join(c for c in topic[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_topic = safe_topic.replace(' ', '_')
    filename = f"presentation_{safe_topic}.pptx"
    output_path = os.path.join(output_dir, filename)
    
    # PPTX yaratish
    create_pptx(content, output_path, template_key=template_key, images=images)
    
    return output_path


async def generate_text(topic: str, text_type: str, language: str) -> str:
    """AI yordamida matn yozish"""
    
    lang_names = {"uz": "o'zbek", "ru": "русский", "en": "English"}
    lang_name = lang_names.get(language, "o'zbek")
    
    type_instructions = {
        "essay": {
            "uz": "Esse yozing. Kirish, asosiy qism va xulosa bo'lsin. Kamida 500 so'z.",
            "ru": "Напишите эссе. Введение, основная часть и заключение. Минимум 500 слов.",
            "en": "Write an essay. Include introduction, body, and conclusion. At least 500 words."
        },
        "article": {
            "uz": "Maqola yozing. Professional va ilmiy uslubda. Kamida 800 so'z.",
            "ru": "Напишите статью. Профессиональный и научный стиль. Минимум 800 слов.",
            "en": "Write an article. Professional and academic style. At least 800 words."
        },
        "report": {
            "uz": "Referat yozing. Kirish, nazariy qism, amaliy qism va xulosa bo'lsin. Kamida 1000 so'z.",
            "ru": "Напишите реферат. Введение, теоретическая часть, практическая часть и заключение. Минимум 1000 слов.",
            "en": "Write a report. Include introduction, theoretical part, practical part, and conclusion. At least 1000 words."
        }
    }
    
    instruction = type_instructions.get(text_type, type_instructions["essay"])
    inst_text = instruction.get(language, instruction.get("uz"))
    
    prompt = f"""Topic: "{topic}"

{inst_text}

Language: {lang_name}

Write a high-quality, well-structured text. Use proper formatting with headings and paragraphs.
All text must be in {lang_name} language."""

    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {"role": "system", "content": f"You are a professional writer. Write all content in {lang_name} language."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4000
    ))
    
    return response.choices[0].message.content.strip()
