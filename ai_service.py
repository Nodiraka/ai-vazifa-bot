"""Suniy intellekt xizmatlari - taqdimot yaratish va matn yozish"""

import os
import json
import asyncio
from openai import OpenAI
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from config import AI_MODEL

# OpenAI client
client = OpenAI()

# ===== Ranglar palitrasi =====
THEME_COLORS = {
    "title_bg": RGBColor(0x1A, 0x23, 0x7E),       # Quyuq ko'k
    "title_text": RGBColor(0xFF, 0xFF, 0xFF),       # Oq
    "slide_bg": RGBColor(0xF5, 0xF5, 0xF5),         # Och kulrang
    "heading_color": RGBColor(0x1A, 0x23, 0x7E),    # Quyuq ko'k
    "body_color": RGBColor(0x33, 0x33, 0x33),       # Qora-kulrang
    "accent_color": RGBColor(0x00, 0x96, 0xD6),     # Ko'k accent
    "footer_color": RGBColor(0x99, 0x99, 0x99),     # Kulrang
}


async def generate_presentation_content(topic: str, slides_count: int, language: str) -> dict:
    """AI yordamida taqdimot kontentini yaratish"""
    
    lang_names = {"uz": "o'zbek", "ru": "русский", "en": "English"}
    lang_name = lang_names.get(language, "o'zbek")
    
    prompt = f"""Create a professional presentation about: "{topic}"

Requirements:
- Language: {lang_name}
- Number of slides: {slides_count}
- First slide: Title slide with the topic and subtitle
- Last slide: Summary/Conclusion slide
- Each slide should have a clear title and 3-5 bullet points
- Content should be informative, well-structured, and professional

Return ONLY valid JSON in this exact format:
{{
    "title": "Presentation Title",
    "subtitle": "Subtitle text",
    "slides": [
        {{
            "title": "Slide Title",
            "points": ["Point 1", "Point 2", "Point 3"]
        }}
    ]
}}

Make sure to include exactly {slides_count} slides (including title and conclusion).
All text must be in {lang_name} language."""

    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {"role": "system", "content": "You are a professional presentation creator. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4000
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


def create_pptx(content: dict, output_path: str) -> str:
    """PowerPoint faylini yaratish"""
    
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    slide_width = prs.slide_width
    slide_height = prs.slide_height
    
    # ===== 1. Titul slayd =====
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Fon - gradient effekt uchun to'q rang
    bg_shape = slide.shapes.add_shape(
        1, 0, 0, slide_width, slide_height
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = THEME_COLORS["title_bg"]
    bg_shape.line.fill.background()
    
    # Dekorativ chiziq (accent)
    accent_line = slide.shapes.add_shape(
        1, Inches(1), Inches(2.8), Inches(2), Inches(0.06)
    )
    accent_line.fill.solid()
    accent_line.fill.fore_color.rgb = THEME_COLORS["accent_color"]
    accent_line.line.fill.background()
    
    # Sarlavha
    title_box = slide.shapes.add_textbox(
        Inches(1), Inches(1.5), Inches(11), Inches(2.5)
    )
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = content.get("title", "Presentation")
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = THEME_COLORS["title_text"]
    p.alignment = PP_ALIGN.LEFT
    
    # Subtitle
    subtitle_box = slide.shapes.add_textbox(
        Inches(1), Inches(3.2), Inches(11), Inches(1.5)
    )
    tf2 = subtitle_box.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = content.get("subtitle", "")
    p2.font.size = Pt(22)
    p2.font.color.rgb = RGBColor(0xBB, 0xBB, 0xBB)
    p2.alignment = PP_ALIGN.LEFT
    
    # ===== 2-N. Kontent slaydlari =====
    slides_data = content.get("slides", [])
    
    for i, slide_data in enumerate(slides_data):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Oq fon
        bg = slide.shapes.add_shape(1, 0, 0, slide_width, slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        bg.line.fill.background()
        
        # Chap tomonda rang chizig'i
        left_bar = slide.shapes.add_shape(
            1, 0, 0, Inches(0.15), slide_height
        )
        left_bar.fill.solid()
        left_bar.fill.fore_color.rgb = THEME_COLORS["title_bg"]
        left_bar.line.fill.background()
        
        # Yuqori chiziq (accent)
        top_line = slide.shapes.add_shape(
            1, Inches(0.15), 0, slide_width - Inches(0.15), Inches(0.04)
        )
        top_line.fill.solid()
        top_line.fill.fore_color.rgb = THEME_COLORS["accent_color"]
        top_line.line.fill.background()
        
        # Slayd raqami
        num_box = slide.shapes.add_textbox(
            Inches(11.5), Inches(6.8), Inches(1.5), Inches(0.5)
        )
        ntf = num_box.text_frame
        np_ = ntf.paragraphs[0]
        np_.text = f"{i + 1}/{len(slides_data)}"
        np_.font.size = Pt(12)
        np_.font.color.rgb = THEME_COLORS["footer_color"]
        np_.alignment = PP_ALIGN.RIGHT
        
        # Sarlavha
        title_box = slide.shapes.add_textbox(
            Inches(0.8), Inches(0.4), Inches(11.5), Inches(1.2)
        )
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = slide_data.get("title", f"Slide {i+1}")
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = THEME_COLORS["heading_color"]
        p.alignment = PP_ALIGN.LEFT
        
        # Sarlavha ostidagi chiziq
        underline = slide.shapes.add_shape(
            1, Inches(0.8), Inches(1.5), Inches(4), Inches(0.04)
        )
        underline.fill.solid()
        underline.fill.fore_color.rgb = THEME_COLORS["accent_color"]
        underline.line.fill.background()
        
        # Bullet pointlar
        points = slide_data.get("points", [])
        content_box = slide.shapes.add_textbox(
            Inches(0.8), Inches(1.9), Inches(11.5), Inches(4.5)
        )
        tf_content = content_box.text_frame
        tf_content.word_wrap = True
        
        for j, point in enumerate(points):
            if j == 0:
                p = tf_content.paragraphs[0]
            else:
                p = tf_content.add_paragraph()
            
            p.text = f"●  {point}"
            p.font.size = Pt(20)
            p.font.color.rgb = THEME_COLORS["body_color"]
            p.space_after = Pt(14)
            p.alignment = PP_ALIGN.LEFT
    
    # Faylni saqlash
    prs.save(output_path)
    return output_path


async def generate_presentation(topic: str, slides_count: int, language: str, output_dir: str) -> str:
    """To'liq taqdimot yaratish jarayoni"""
    
    # AI kontentni yaratish
    content = await generate_presentation_content(topic, slides_count, language)
    
    # Fayl nomini yaratish
    safe_topic = "".join(c for c in topic[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_topic = safe_topic.replace(' ', '_')
    filename = f"presentation_{safe_topic}.pptx"
    output_path = os.path.join(output_dir, filename)
    
    # PPTX yaratish
    create_pptx(content, output_path)
    
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
