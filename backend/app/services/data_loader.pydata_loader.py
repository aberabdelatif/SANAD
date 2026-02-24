import json
import os
from typing import Dict, List, Any, Optional
from ..config import BY_BOOK_PATH, BOOKS_CATALOG
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """تحميل البيانات من ملفات JSON"""
    
    _instance = None
    _data = None
    _books_cache = {}
    _hadiths_cache = []
    _chapters_cache = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_all_data()
        return cls._instance
    
    def _load_all_data(self):
        """تحميل جميع البيانات من الملفات"""
        logger.info("🚀 بدء تحميل قاعدة البيانات...")
        
        all_hadiths = []
        all_chapters = []
        books_metadata = {}
        
        # تحميل كل كتاب
        for book_id, book_info in BOOKS_CATALOG.items():
            try:
                book_path = os.path.join(BY_BOOK_PATH, book_info["category"], book_info["file_name"])
                
                if not os.path.exists(book_path):
                    logger.warning(f"⚠️ ملف الكتاب غير موجود: {book_path}")
                    continue
                
                with open(book_path, 'r', encoding='utf-8') as f:
                    book_data = json.load(f)
                
                # تخزين بيانات الكتاب
                books_metadata[book_id] = {
                    "id": book_info["id"],
                    "name_ar": book_info["name_ar"],
                    "name_en": book_info["name_en"],
                    "author_ar": book_info["author_ar"],
                    "author_en": book_info["author_en"],
                    "category": book_info["category"],
                    "total_hadiths": book_info["total_hadiths"]
                }
                
                # تخزين الأبواب
                for chapter in book_data.get("chapters", []):
                    all_chapters.append({
                        "id": chapter["id"],
                        "bookId": book_info["id"],
                        "arabic": chapter["arabic"],
                        "english": chapter["english"]
                    })
                
                # تخزين الأحاديث
                for hadith in book_data.get("hadiths", []):
                    all_hadiths.append({
                        "id": hadith["id"],
                        "idInBook": hadith["idInBook"],
                        "bookId": hadith["bookId"],
                        "chapterId": hadith["chapterId"],
                        "arabic": hadith["arabic"],
                        "english": hadith["english"]
                    })
                
                logger.info(f"✅ تم تحميل {book_info['name_ar']}: {len(book_data.get('hadiths', []))} حديث")
                
            except Exception as e:
                logger.error(f"❌ خطأ في تحميل {book_id}: {str(e)}")
        
        self._books_cache = books_metadata
        self._hadiths_cache = all_hadiths
        self._chapters_cache = all_chapters
        
        logger.info(f"✅ تم تحميل {len(all_hadiths)} حديث من {len(books_metadata)} كتب")
    
    def get_all_books(self) -> List[Dict]:
        """الحصول على جميع الكتب"""
        return list(self._books_cache.values())
    
    def get_book(self, book_id: str) -> Optional[Dict]:
        """الحصول على كتاب محدد"""
        return self._books_cache.get(book_id)
    
    def get_book_by_id(self, book_id_int: int) -> Optional[Dict]:
        """الحصول على كتاب بواسطة الرقم"""
        for book in self._books_cache.values():
            if book["id"] == book_id_int:
                return book
        return None
    
    def get_all_hadiths(self) -> List[Dict]:
        """الحصول على جميع الأحاديث"""
        return self._hadiths_cache
    
    def get_hadith(self, hadith_id: int) -> Optional[Dict]:
        """الحصول على حديث محدد"""
        for hadith in self._hadiths_cache:
            if hadith["id"] == hadith_id:
                return hadith
        return None
    
    def get_hadiths_by_book(self, book_id: int, page: int = 1, limit: int = 20) -> Dict:
        """الحصول على أحاديث كتاب محدد"""
        book_hadiths = [h for h in self._hadiths_cache if h["bookId"] == book_id]
        
        total = len(book_hadiths)
        start = (page - 1) * limit
        end = start + limit
        
        return {
            "hadiths": book_hadiths[start:end],
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit
        }
    
    def get_hadiths_by_chapter(self, chapter_id: int, page: int = 1, limit: int = 20) -> Dict:
        """الحصول على أحاديث باب محدد"""
        chapter_hadiths = [h for h in self._hadiths_cache if h["chapterId"] == chapter_id]
        
        total = len(chapter_hadiths)
        start = (page - 1) * limit
        end = start + limit
        
        return {
            "hadiths": chapter_hadiths[start:end],
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit
        }
    
    def get_chapters_by_book(self, book_id: int) -> List[Dict]:
        """الحصول على أبواب كتاب محدد"""
        return [c for c in self._chapters_cache if c["bookId"] == book_id]
    
    def get_stats(self) -> Dict:
        """إحصائيات عامة"""
        return {
            "total_books": len(self._books_cache),
            "total_hadiths": len(self._hadiths_cache),
            "total_chapters": len(self._chapters_cache),
            "books_by_category": {
                "the_9_books": len([b for b in self._books_cache.values() if b["category"] == "the_9_books"]),
                "forties": len([b for b in self._books_cache.values() if b["category"] == "forties"]),
                "other_books": len([b for b in self._books_cache.values() if b["category"] == "other_books"])
            }
        }

# إنشاء كائن واحد للتحميل (Singleton)
data_loader = DataLoader()