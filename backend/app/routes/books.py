from fastapi import APIRouter, HTTPException
from typing import List
from ..services.hadith_service import hadith_service

router = APIRouter(prefix="/books", tags=["الكتب"])

@router.get("/")
async def get_all_books():
    """إرجاع جميع الكتب"""
    books = hadith_service.get_all_books()
    if not books:
        raise HTTPException(status_code=404, detail="لا توجد كتب")
    return books

@router.get("/{book_id}")
async def get_book(book_id: str):
    """إرجاع كتاب محدد"""
    book = hadith_service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="الكتاب غير موجود")
    return book