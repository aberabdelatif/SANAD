import re
import unicodedata

def normalize_arabic(text: str) -> str:
    """تطبيع النص العربي (إزالة التشكيل، توحيد الأحرف)"""
    if not text:
        return ""
    
    # إزالة الحركات والتشكيل
    text = re.sub(r'[ًٌٍَُِّْ]', '', text)
    
    # توحيد أشكال الألف
    text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
    
    # توحيد التاء المربوطة والهاء
    text = text.replace('ة', 'ه')
    
    # إزالة التطويل (الكشيدة)
    text = text.replace('ـ', '')
    
    return text.strip()

def extract_keywords(text: str) -> list:
    """استخراج الكلمات المفتاحية من النص"""
    if not text:
        return []
    
    # تنظيف النص
    text = normalize_arabic(text)
    
    # تقسيم النص إلى كلمات
    words = text.split()
    
    # إزالة الكلمات القصيرة جداً
    keywords = [w for w in words if len(w) > 2]
    
    return keywords 
