from pydantic import BaseModel, Field
from typing import Optional, Any

class Hadith(BaseModel):
    id: str
    book_id: str
    hadith_number: int
    chapter_id: Optional[Any] = None  # تغيير إلى Any لقبول null أو قيم أخرى
    arabic: str
    english_narrator: Optional[str] = None
    english_text: Optional[str] = None
    grade: Optional[str] = None
    
    class Config:
        # السماح بأسماء حقول إضافية
        extra = "allow"
        # تجاهل القيم الخاطئة
        coerce_numbers_to_str = True