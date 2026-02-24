from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..models.hadith import Hadith
from ..models.chapter import Chapter, ChapterSummary
from ..services.hadith_service import hadith_service
from ..core.pagination import paginate

router = APIRouter(prefix="/chapters", tags=["الأبواب"])

# بيانات تجريبية للأبواب (للهيكلة by_chapter)
# في المستقبل، سيتم قراءتها من JSON
SAMPLE_CHAPTERS = {
    "bukhari": [
        Chapter(
            id="bukhari_1",
            book_id="bukhari",
            chapter_number=1,
            title_ar="بدء الوحي",
            hadith_count=7
        ),
        Chapter(
            id="bukhari_2",
            book_id="bukhari",
            chapter_number=2,
            title_ar="الإيمان",
            hadith_count=50
        )
    ]
}

@router.get("/", response_model=List[ChapterSummary])
async def get_all_chapters(
    book_id: Optional[str] = Query(None, description="تصفية بكتاب محدد")
):
    """
    الحصول على جميع الأبواب
    - يمكن تصفيتها بكتاب محدد
    """
    if book_id:
        # إرجاع أبواب كتاب محدد
        chapters = SAMPLE_CHAPTERS.get(book_id, [])
        if not chapters:
            raise HTTPException(status_code=404, detail="لا توجد أبواب لهذا الكتاب")
    else:
        # إرجاع كل الأبواب (من جميع الكتب)
        chapters = []
        for book_chapters in SAMPLE_CHAPTERS.values():
            chapters.extend(book_chapters)
    
    # تحويل إلى ChapterSummary
    summary = [
        ChapterSummary(
            id=ch.id,
            title_ar=ch.title_ar,
            hadith_count=ch.hadith_count
        )
        for ch in chapters
    ]
    
    return summary

@router.get("/{chapter_id}", response_model=Chapter)
async def get_chapter(chapter_id: str):
    """
    الحصول على باب محدد بالمعرف
    المعرف يكون عادة: bookId_chapterNumber (مثال: bukhari_1)
    """
    # البحث عن الباب في جميع الكتب
    for book_chapters in SAMPLE_CHAPTERS.values():
        for chapter in book_chapters:
            if chapter.id == chapter_id:
                return chapter
    
    raise HTTPException(status_code=404, detail="الباب غير موجود")

@router.get("/{chapter_id}/hadiths", response_model=List[Hadith])
async def get_chapter_hadiths(
    chapter_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    """
    الحصول على أحاديث باب محدد
    ملاحظة: هذه ميزة تجريبية، تحتاج إلى بيانات حقيقية
    """
    # محاولة استخراج book_id من chapter_id
    # مثال: bukhari_1 -> book_id = bukhari
    parts = chapter_id.split('_')
    if len(parts) < 2:
        raise HTTPException(status_code=400, detail="صيغة chapter_id غير صحيحة")
    
    book_id = parts[0]
    
    # الحصول على أحاديث الكتاب
    all_hadiths = hadith_service.get_hadiths_by_book(book_id)
    
    # هنا يمكن إضافة فلترة حسب الباب إذا كانت البيانات تحتوي على chapter_id
    # حالياً نعيد كل أحاديث الكتاب
    
    if not all_hadiths:
        raise HTTPException(status_code=404, detail="لا توجد أحاديث لهذا الباب")
    
    # تطبيق التقسيم
    start = (page - 1) * limit
    end = start + limit
    
    return {
        "items": all_hadiths[start:end],
        "total": len(all_hadiths),
        "page": page,
        "limit": limit,
        "pages": (len(all_hadiths) + limit - 1) // limit
    }

@router.get("/book/{book_id}/chapters", response_model=List[ChapterSummary])
async def get_book_chapters(book_id: str):
    """
    الحصول على جميع أبواب كتاب محدد
    """
    chapters = SAMPLE_CHAPTERS.get(book_id, [])
    
    if not chapters:
        raise HTTPException(status_code=404, detail="لا توجد أبواب لهذا الكتاب")
    
    return [
        ChapterSummary(
            id=ch.id,
            title_ar=ch.title_ar,
            hadith_count=ch.hadith_count
        )
        for ch in chapters
    ] 
