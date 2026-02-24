from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict
from ..services.search_service import search_service
from ..models.hadith import Hadith

router = APIRouter(prefix="/search", tags=["البحث"])

@router.get("/")
async def search(
    q: str = Query(..., description="نص البحث"),
    book_id: Optional[str] = Query(None, description="فلتر بمعرف الكتاب"),
    grade: Optional[str] = Query(None, description="فلتر بدرجة الحديث"),
    narrator: Optional[str] = Query(None, description="فلتر بالراوي"),
    page: int = Query(1, ge=1, description="رقم الصفحة"),
    limit: int = Query(20, ge=1, le=100, description="عدد النتائج في الصفحة")
):
    """بحث متقدم في الأحاديث"""
    filters = {}
    if book_id:
        filters['book_id'] = book_id
    if grade:
        filters['grade'] = grade
    if narrator:
        filters['narrator'] = narrator
    
    options = {
        "filters": filters,
        "page": page,
        "limit": limit
    }
    
    result = search_service.advanced_search(q, options)
    return result

@router.get("/simple")
async def simple_search(
    q: str = Query(..., description="نص البحث"),
    book_id: Optional[str] = None
):
    """بحث بسيط وسريع"""
    filters = {}
    if book_id:
        filters['book_id'] = book_id
    
    results = search_service.simple_search(q, filters)
    return results

@router.get("/suggestions")
async def get_suggestions(
    q: str = Query(..., description="النص لاقتراحات البحث")
):
    """اقتراحات كلمات للبحث"""
    suggestions = search_service.get_suggestions(q)
    return {"query": q, "suggestions": suggestions}

@router.get("/filters")
async def get_filter_options():
    """الحصول على خيارات الفلاتر المتاحة"""
    return search_service.get_filters_options()