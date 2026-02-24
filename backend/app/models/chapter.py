from pydantic import BaseModel
from typing import Optional, List

class Chapter(BaseModel):
    """نموذج الباب (Chapter) - للاستخدام المستقبلي مع هيكلة by_chapter"""
    id: str
    book_id: str
    chapter_number: int
    title_ar: str
    title_en: Optional[str] = None
    hadith_count: int = 0
    first_hadith: Optional[int] = None
    last_hadith: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "bukhari_1",
                "book_id": "bukhari",
                "chapter_number": 1,
                "title_ar": "بدء الوحي",
                "title_en": "Revelation",
                "hadith_count": 7
            }
        }

class ChapterSummary(BaseModel):
    """ملخص الباب (للقوائم)"""
    id: str
    title_ar: str
    hadith_count: int 

