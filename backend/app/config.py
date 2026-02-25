import os
from pathlib import Path

# تحديد المسار الأساسي
BASE_DIR = Path(__file__).resolve().parent.parent

# استخدام متغير البيئة إذا موجود، وإلا استخدم المسار الافتراضي
DATA_PATH = os.environ.get("DATA_PATH", str(BASE_DIR / "data"))

# المسار الكامل لملفات JSON
RAW_DATA_PATH = os.path.join(DATA_PATH, "raw", "hadith-json-main", "db")

BOOK_CATEGORIES = ["the_9_books", "forties", "other_books"]

def get_all_book_paths():
    """إرجاع جميع ملفات JSON في مجلد by_book"""
    book_paths = []
    by_book_path = os.path.join(RAW_DATA_PATH, "by_book")
    
    print(f"🔍 البحث عن البيانات في: {by_book_path}")
    
    if not os.path.exists(by_book_path):
        print(f"❌ المسار غير موجود: {by_book_path}")
        return book_paths
    
    for category in BOOK_CATEGORIES:
        category_path = os.path.join(by_book_path, category)
        if os.path.exists(category_path):
            for file in os.listdir(category_path):
                if file.endswith('.json'):
                    full_path = os.path.join(category_path, file)
                    print(f"✅ Found: {category}/{file}")
                    book_paths.append({
                        'path': full_path,
                        'category': category,
                        'book_id': file.replace('.json', '')
                    })
        else:
            print(f"⚠️ مجلد غير موجود: {category_path}")
    
    return book_paths
