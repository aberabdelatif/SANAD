from fastapi import Header, HTTPException
from typing import Optional

# للاستخدام المستقبلي (مصادقة، معدلات، إلخ)
async def get_language_header(accept_language: Optional[str] = Header(None)):
    """تحديد لغة المستخدم"""
    if accept_language and accept_language.startswith("en"):
        return "en"
    return "ar" 
