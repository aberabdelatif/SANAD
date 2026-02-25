import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ===== إنشاء تطبيق FastAPI =====
app = FastAPI(title="SANAD ENGINE", version="2.0")

# ===== إعداد CORS =====
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== استيراد config و services =====
from .config import get_all_book_paths
from .services.hadith_service import HadithService

# ===== إنشاء service =====
hadith_service = HadithService(get_all_book_paths())

# ===== نقاط النهاية الأساسية =====
@app.get("/")
def root():
    return {
        "message": "SANAD ENGINE is running",
        "status": "healthy",
        "total_books": len(hadith_service.books),
        "total_hadiths": len(hadith_service.hadiths)
    }

@app.get("/stats")
def stats():
    books = hadith_service.get_all_books()
    return {
        "total_books": len(books),
        "total_hadiths": len(hadith_service.hadiths),
        "categories": {
            "the_9_books": len([b for b in books if b['category'] == 'the_9_books']),
            "forties": len([b for b in books if b['category'] == 'forties']),
            "other_books": len([b for b in books if b['category'] == 'other_books'])
        }
    }

# ===== Health check endpoint =====
@app.get("/health")
def health():
    return {"status": "ok"}
