from typing import List, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """هيكل الاستجابة المقسمة"""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

def paginate(items: List, page: int = 1, size: int = 10) -> PaginatedResponse:
    """تقسيم النتائج"""
    start = (page - 1) * size
    end = start + size
    
    return PaginatedResponse(
        items=items[start:end],
        total=len(items),
        page=page,
        size=size,
        pages=(len(items) + size - 1) // size
    ) 
