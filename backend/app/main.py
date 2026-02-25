import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ===== التشخيص (يجب أن يكون قبل إنشاء التطبيق) =====
print("🔍 ===== بدء التشخيص ===== ")
print(f"📁 المجلد الحالي: {os.getcwd()}")
print("📁 محتويات المجلد الرئيسي:")
try:
    for item in os.listdir('.'):
        print(f"   - {item}")
except Exception as e:
    print(f"   خطأ: {e}")

print("\n📁 محتويات مجلد /app (إذا كان موجوداً):")
try:
    for item in os.listdir('/app'):
        print(f"   - {item}")
except:
    print("   لا يمكن قراءة /app")

print("\n📁 البحث عن مجلد البيانات:")
possible_paths = [
    '/app/data',
    '/app/données',
    '/app/backend/data',
    '/data',
    './data',
    './données'
]

for path in possible_paths:
    if os.path.exists(path):
        print(f"✅ موجود: {path}")
        if os.path.isdir(path):
            try:
                contents = os.listdir(path)[:5]
                print(f"   المحتويات: {contents}")
            except:
                print(f"   لا يمكن قراءة المحتويات")
    else:
        print(f"❌ غير موجود: {path}")
print("🔍 ===== نهاية التشخيص ===== \n")

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

# ===== استيراد المسارات (بعد إنشاء التطبيق) =====
from .routes import books, hadiths

app.include_router(books.router)
app.include_router(hadiths.router)

# ===== نقاط النهاية الأساسية =====
@app.get("/")
def root():
    # استيراد hadith_service هنا لتجنب circular imports
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
