import os
from pathlib import Path

# ===== التشخيص =====
print("🔍 ===== تشخيص المسارات ===== ")
print(f"📁 الموقع الحالي: {os.getcwd()}")
print("📁 محتويات /app:")
try:
    for item in os.listdir('/app'):
        print(f"   - {item}")
except:
    print("   لا يمكن القراءة")

print("\n📁 محتويات /app/data (إذا موجود):")
if os.path.exists('/app/data'):
    try:
        for item in os.listdir('/app/data'):
            print(f"   - {item}")
    except:
        print("   خطأ في القراءة")
else:
    print("   ❌ مجلد data غير موجود في /app/data")
print("🔍 ===== نهاية التشخيص ===== \n")

# ===== إنشاء تطبيق FastAPI =====
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# هذا هو المتغير المهم جداً
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

# ===== استيراد المسارات (بعد إنشاء التطبيق) =====
from .routes import books, hadiths

app.include_router(books.router)
app.include_router(hadiths.router)

# ===== نقاط النهاية الأساسية =====
@app.get("/")
def root():
    # استيراد الخدمة هنا لتجنب circular imports
    from .services.hadith_service import hadith_service
    return {
        "message": "SANAD ENGINE is running",
        "status": "healthy",
        "total_books": len(hadith_service.books),
        "total_hadiths": len(hadith_service.hadiths)
    }

@app.get("/stats")
def stats():
    from .services.hadith_service import hadith_service
    books = hadith_service.get_all_books()
    return {
        "total_books": len(books),
        "total_hadiths": len(hadith_service.hadiths),
        "categories": {
            "the_9_books": len([b for b in books if b.category == 'the_9_books']),
            "forties": len([b for b in books if b.category == 'forties']),
            "other_books": len([b for b in books if b.category == 'other_books'])
        }
    }
