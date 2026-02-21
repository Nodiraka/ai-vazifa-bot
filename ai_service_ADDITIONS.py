"""
ai_service.py ga qo'shish kerak - YANGILANGAN generate_presentation_with_template
"""

# Yangi funksiya - author va plan bilan
async def generate_presentation_with_template(
    topic: str, author: str, slides_count: int, language: str,
    output_dir: str, template_category: str, template_id: int,
    has_ai_images: bool = False, progress_callback=None,
    plan_mode: str = "auto", plan_1: str = None, plan_2: str = None, plan_3: str = None
) -> str:
    """Template fayl asosida taqdimot yaratish - YANGILANGAN"""
    
    # 1-qadam: AI kontentni yaratish
    if progress_callback:
        await progress_callback(1, "content")
    
    # YANGI: Plan ma'lumotlari
    plans = None
    if plan_mode == "manual" and plan_1 and plan_2 and plan_3:
        plans = {
            "plan_1": plan_1,
            "plan_2": plan_2,
            "plan_3": plan_3
        }
    
    # AI Content - author va plans bilan
    content = await generate_presentation_content_new(
        topic=topic,
        author=author,
        slides_count=slides_count,
        language=language,
        has_images=False,
        plans=plans
    )
    
    # 2-qadam: Template asosida yaratish
    if progress_callback:
        await progress_callback(2, "template")
    
    safe_topic = "".join(c for c in topic[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_topic = safe_topic.replace(' ', '_')
    filename = f"presentation_{safe_topic}.pptx"
    
    # Template handler orqali yaratish
    output_path = create_presentation_from_template(
        category=template_category,
        template_id=template_id,
        content_data=content,
        output_filename=filename
    )
    
    if output_path:
        if progress_callback:
            await progress_callback(4, "done")
        return output_path
    else:
        # Fallback: scratch dan yaratish
        logger.warning("Template topilmadi, scratch dan yaratilmoqda...")
        return await generate_presentation(
            topic=topic,
            slides_count=slides_count,
            language=language,
            output_dir=output_dir,
            has_ai_images=has_ai_images,
            progress_callback=progress_callback
        )


# YANGI AI Content Generator
async def generate_presentation_content_new(
    topic: str, author: str, slides_count: int, language: str,
    has_images: bool = False, plans: dict = None
) -> dict:
    """
    AI bilan taqdimot kontentini yaratish
    
    YANGI STRUKTURA:
    - SAHIFA 1: Sarlavha (topic + author)
    - SAHIFA 2: Mavzu va reja (topic + 3 plan)
    - SAHIFA 3 to slides_count+2: Asosiy kontent (slides_count ta)
    - SAHIFA slides_count+3: Xulosa (rahmat + author)
    
    JAMI: slides_count + 3 sahifa
    """
    
    # Prompt yaratish
    if plans:
        plan_text = f"""
REJA (Foydalanuvchi kiritgan):
1. {plans['plan_1']}
2. {plans['plan_2']}
3. {plans['plan_3']}

Iltimos, shu rejaga rioya qilib kontent yarating.
"""
    else:
        plan_text = """
REJA: O'zingiz 3 ta mantiqiy reja tuzing va shu asosda kontent yarating.
"""
    
    prompt = f"""
Taqdimot yaratish uchun kontent yarating.

MAVZU: {topic}
MUALLIF: {author}
TIL: {language}
ASOSIY SAHIFALAR: {slides_count} ta
JAMI SAHIFALAR: {slides_count + 3} ta

STRUKTURA:
1. SAHIFA 1 (Sarlavha):
   - Faqat mavzu nomi
   - Muallif ismi
   
2. SAHIFA 2 (Reja):
   - Tepada: Mavzu
   - Pastda: 3 ta reja punkti

{plan_text}

3. SAHIFA 3 - {slides_count + 2} (Asosiy kontent - {slides_count} ta sahifa):
   - Rejaga muvofiq kontent
   - Har bir sahifada:
     * Sarlavha
     * 3-5 ta asosiy punkt
     
4. SAHIFA {slides_count + 3} (Xulosa):
   - "Etiboringiz uchun rahmat!"
   - Muallif ismi

JSON FORMAT:
{{
  "title": "Mavzu nomi",
  "author": "Muallif ismi",
  "subtitle": "Qisqa tavsif",
  "plan": ["Reja 1", "Reja 2", "Reja 3"],
  "slides": [
    {{"title": "Sahifa sarlavhasi", "points": ["Punkt 1", "Punkt 2", ...]}},
    ...
  ]
}}

Iltimos, faqat JSON qaytaring.
"""
    
    try:
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": f"Siz professional taqdimot yaratuvchi yordamchisiz. Javobni faqat JSON formatda bering. Til: {language}"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        content_text = response.choices[0].message.content.strip()
        
        # JSON ni parse qilish
        import re
        json_match = re.search(r'\{.*\}', content_text, re.DOTALL)
        if json_match:
            content_data = json.loads(json_match.group())
        else:
            content_data = json.loads(content_text)
        
        return content_data
        
    except Exception as e:
        logger.error(f"AI content generation error: {e}")
        # Fallback - oddiy struktura
        return {
            "title": topic,
            "author": author,
            "subtitle": "",
            "plan": plans.values() if plans else ["Kirish", "Asosiy qism", "Xulosa"],
            "slides": [
                {"title": f"Sahifa {i+1}", "points": ["Punkt 1", "Punkt 2", "Punkt 3"]}
                for i in range(slides_count)
            ]
        }

print("✅ Yangi ai_service funksiyalari tayyor")


"""
ai_service.py ga qo'shish kerak - YANGILANGAN generate_presentation_with_template
"""

# Yangi funksiya - author va plan bilan
async def generate_presentation_with_template(
    topic: str, author: str, slides_count: int, language: str,
    output_dir: str, template_category: str, template_id: int,
    has_ai_images: bool = False, progress_callback=None,
    plan_mode: str = "auto", plan_1: str = None, plan_2: str = None, plan_3: str = None
) -> str:
    """Template fayl asosida taqdimot yaratish - YANGILANGAN"""
    
    # 1-qadam: AI kontentni yaratish
    if progress_callback:
        await progress_callback(1, "content")
    
    # YANGI: Plan ma'lumotlari
    plans = None
    if plan_mode == "manual" and plan_1 and plan_2 and plan_3:
        plans = {
            "plan_1": plan_1,
            "plan_2": plan_2,
            "plan_3": plan_3
        }
    
    # AI Content - author va plans bilan
    content = await generate_presentation_content_new(
        topic=topic,
        author=author,
        slides_count=slides_count,
        language=language,
        has_images=False,
        plans=plans
    )
    
    # 2-qadam: Template asosida yaratish
    if progress_callback:
        await progress_callback(2, "template")
    
    safe_topic = "".join(c for c in topic[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_topic = safe_topic.replace(' ', '_')
    filename = f"presentation_{safe_topic}.pptx"
    
    # Template handler orqali yaratish
    output_path = create_presentation_from_template(
        category=template_category,
        template_id=template_id,
        content_data=content,
        output_filename=filename
    )
    
    if output_path:
        if progress_callback:
            await progress_callback(4, "done")
        return output_path
    else:
        # Fallback: scratch dan yaratish
        logger.warning("Template topilmadi, scratch dan yaratilmoqda...")
        return await generate_presentation(
            topic=topic,
            slides_count=slides_count,
            language=language,
            output_dir=output_dir,
            has_ai_images=has_ai_images,
            progress_callback=progress_callback
        )


# YANGI AI Content Generator
async def generate_presentation_content_new(
    topic: str, author: str, slides_count: int, language: str,
    has_images: bool = False, plans: dict = None
) -> dict:
    """
    AI bilan taqdimot kontentini yaratish
    
    YANGI STRUKTURA:
    - SAHIFA 1: Sarlavha (topic + author)
    - SAHIFA 2: Mavzu va reja (topic + 3 plan)
    - SAHIFA 3 to slides_count+2: Asosiy kontent (slides_count ta)
    - SAHIFA slides_count+3: Xulosa (rahmat + author)
    
    JAMI: slides_count + 3 sahifa
    """
    
    # Prompt yaratish
    if plans:
        plan_text = f"""
REJA (Foydalanuvchi kiritgan):
1. {plans['plan_1']}
2. {plans['plan_2']}
3. {plans['plan_3']}

Iltimos, shu rejaga rioya qilib kontent yarating.
"""
    else:
        plan_text = """
REJA: O'zingiz 3 ta mantiqiy reja tuzing va shu asosda kontent yarating.
"""
    
    prompt = f"""
Taqdimot yaratish uchun kontent yarating.

MAVZU: {topic}
MUALLIF: {author}
TIL: {language}
ASOSIY SAHIFALAR: {slides_count} ta
JAMI SAHIFALAR: {slides_count + 3} ta

STRUKTURA:
1. SAHIFA 1 (Sarlavha):
   - Faqat mavzu nomi
   - Muallif ismi
   
2. SAHIFA 2 (Reja):
   - Tepada: Mavzu
   - Pastda: 3 ta reja punkti

{plan_text}

3. SAHIFA 3 - {slides_count + 2} (Asosiy kontent - {slides_count} ta sahifa):
   - Rejaga muvofiq kontent
   - Har bir sahifada:
     * Sarlavha
     * 3-5 ta asosiy punkt
     
4. SAHIFA {slides_count + 3} (Xulosa):
   - "Etiboringiz uchun rahmat!"
   - Muallif ismi

JSON FORMAT:
{{
  "title": "Mavzu nomi",
  "author": "Muallif ismi",
  "subtitle": "Qisqa tavsif",
  "plan": ["Reja 1", "Reja 2", "Reja 3"],
  "slides": [
    {{"title": "Sahifa sarlavhasi", "points": ["Punkt 1", "Punkt 2", ...]}},
    ...
  ]
}}

Iltimos, faqat JSON qaytaring.
"""
    
    try:
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": f"Siz professional taqdimot yaratuvchi yordamchisiz. Javobni faqat JSON formatda bering. Til: {language}"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        content_text = response.choices[0].message.content.strip()
        
        # JSON ni parse qilish
        import re
        json_match = re.search(r'\{.*\}', content_text, re.DOTALL)
        if json_match:
            content_data = json.loads(json_match.group())
        else:
            content_data = json.loads(content_text)
        
        return content_data
        
    except Exception as e:
        logger.error(f"AI content generation error: {e}")
        # Fallback - oddiy struktura
        return {
            "title": topic,
            "author": author,
            "subtitle": "",
            "plan": plans.values() if plans else ["Kirish", "Asosiy qism", "Xulosa"],
            "slides": [
                {"title": f"Sahifa {i+1}", "points": ["Punkt 1", "Punkt 2", "Punkt 3"]}
                for i in range(slides_count)
            ]
        }

print("✅ Yangi ai_service funksiyalari tayyor")
