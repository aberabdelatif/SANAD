from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: str
    name_ar: str
    name_en: Optional[str] = None
    author: Optional[str] = None
    category: str
    total_hadiths: int = 0
    description: Optional[str] = ""