from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..services.hadith_service import hadith_service
from ..models.hadith import Hadith

router = APIRouter(prefix="/hadiths", tags=["الأحاديث"])

@router.get("/", response_model=List[Hadith])
async def get_all_hadiths(
    book_id: Optional[str] = Query(None, description="تصفية حسب الكتاب")
):
    if book_id:
        return hadith_service.get_hadiths_by_book(book_id)
    return hadith_service.get_all_hadiths()

@router.get("/{hadith_id}", response_model=Hadith)
async def get_hadith(hadith_id: str):
    hadith = hadith_service.get_hadith_by_id(hadith_id)
    if not hadith:
        raise HTTPException(status_code=404, detail="الحديث غير موجود")
    return hadith

@router.get("/book/{book_id}", response_model=List[Hadith])
async def get_hadiths_by_book(book_id: str):
    hadiths = hadith_service.get_hadiths_by_book(book_id)
    if not hadiths:
        raise HTTPException(status_code=404, detail="لا توجد أحاديث لهذا الكتاب")
    return hadiths