import os
from pathlib import Path

# المسار الأساسي للمشروع (SANAD)
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # 👈 يرتفع 3 مستويات
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "hadith-json-main", "db")

print(f"🔍 المسار الكامل للبيانات: {DATA_PATH}")
print(f"✅ المجلد موجود؟ {os.path.exists(DATA_PATH)}")

BY_BOOK_PATH = os.path.join(DATA_PATH, "by_book")
BOOK_CATEGORIES = ["the_9_books", "forties", "other_books"]

def get_all_book_paths():
    """إرجاع جميع ملفات JSON في مجلد by_book"""
    book_paths = []
    
    print(f"🔍 البحث في: {BY_BOOK_PATH}")
    
    if not os.path.exists(BY_BOOK_PATH):
        print(f"❌ المسار غير موجود: {BY_BOOK_PATH}")
        return book_paths
    
    for category in BOOK_CATEGORIES:
        category_path = os.path.join(BY_BOOK_PATH, category)
        if os.path.exists(category_path):
            files = os.listdir(category_path)
            json_files = [f for f in files if f.endswith('.json')]
            print(f"✅ {category}: {len(json_files)} ملف")
            
            for file in json_files:
                full_path = os.path.join(category_path, file)
                book_paths.append({
                    'path': full_path,
                    'category': category,
                    'book_id': file.replace('.json', '')
                })
        else:
            print(f"⚠️ مجلد غير موجود: {category_path}")
    
    return book_paths
