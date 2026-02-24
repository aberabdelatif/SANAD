from fastapi import APIRouter
from ..services.data_loader import data_loader
from ..config import TOTAL_HADITHS

router = APIRouter(prefix="/stats", tags=["الإحصائيات"])

@router.get("/")
async def get_stats():
    """إحصائيات عامة عن قاعدة البيانات"""
    stats = data_loader.get_stats()
    stats["total_hadiths_verified"] = TOTAL_HADITHS
    
    return stats

@router.get("/books")
async def get_books_stats():
    """إحصائيات الكتب"""
    books = data_loader.get_all_books()
    
    return {
        "total_books": len(books),
        "books_by_category": {
            "the_9_books": len([b for b in books if b["category"] == "the_9_books"]),
            "forties": len([b for b in books if b["category"] == "forties"]),
            "other_books": len([b for b in books if b["category"] == "other_books"])
        },
        "total_hadiths": sum(b["total_hadiths"] for b in books)
    }