import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # عدنا إلى مجلد SANAD
DATA_PATH = os.path.join(BASE_DIR, "données", "brut", "hadith-json-main", "base de données")

print(f"🔍 المسار الكامل للبيانات: {DATA_PATH}")

# التحقق من وجود المجلد
if os.path.exists(DATA_PATH):
    print(f"✅ المجلد موجود: {DATA_PATH}")
else:
    print(f"❌ المجلد غير موجود: {DATA_PATH}")

BY_BOOK_PATH = os.path.join(DATA_PATH, "par_livre")
BOOK_CATEGORIES = ["the_9_books", "forties", "other_books"]

def get_all_book_paths():
    """إرجاع جميع ملفات JSON في مجلد par_livre"""
    book_paths = []
    
    print(f"🔍 البحث في: {BY_BOOK_PATH}")
    
    if not os.path.exists(BY_BOOK_PATH):
        print(f"❌ المسار غير موجود: {BY_BOOK_PATH}")
        return book_paths
    
    for category in BOOK_CATEGORIES:
        category_path = os.path.join(BY_BOOK_PATH, category)
        print(f"📁 فحص مجلد: {category_path}")
        
        if os.path.exists(category_path):
            files = os.listdir(category_path)
            json_files = [f for f in files if f.endswith('.json')]
            print(f"   ✅ وجدنا {len(json_files)} ملف JSON في {category}")
            
            for file in json_files:
                full_path = os.path.join(category_path, file)
                book_paths.append({
                    'path': full_path,
                    'category': category,
                    'book_id': file.replace('.json', '')
                })
        else:
            print(f"⚠️ مجلد غير موجود: {category_path}")
    
    print(f"📊 إجمالي ملفات JSON التي وجدناها: {len(book_paths)}")
    return book_paths
