import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# دالة للبحث عن مجلد by_book في أي مكان
def find_by_book_path():
    # المسارات المحتملة للبحث
    search_paths = [
        os.path.join(BASE_DIR, "data"),
        "/app/data",
        "/data",
        os.path.join(BASE_DIR, "data", "raw"),
        "/app/data/raw",
    ]
    
    print("🔍 البحث عن مجلد by_book...")
    
    for base_path in search_paths:
        if not os.path.exists(base_path):
            continue
            
        print(f"📁 فحص: {base_path}")
        
        # ابحث عن أي مسار ينتهي بـ by_book
        for root, dirs, files in os.walk(base_path):
            if "by_book" in dirs:
                by_book_path = os.path.join(root, "by_book")
                print(f"✅ وجدنا by_book في: {by_book_path}")
                return by_book_path
            
            # ابحث عن المجلدات التي تحتوي على ملفات JSON
            for dir_name in dirs:
                if dir_name in ["the_9_books", "forties", "other_books"]:
                    parent_path = os.path.join(root, dir_name, "..")
                    by_book_path = os.path.abspath(parent_path)
                    print(f"✅ وجدنا مجلد كتب في: {by_book_path}")
                    return by_book_path
    
    print("❌ لم نجد مجلد by_book!")
    return None

# ابحث عن المسار الصحيح
BY_BOOK_PATH = find_by_book_path()

if BY_BOOK_PATH:
    print(f"✅ المسار النهائي: {BY_BOOK_PATH}")
else:
    BY_BOOK_PATH = "/app/data/raw"  # مسار افتراضي
    print(f"⚠️ استخدام المسار الافتراضي: {BY_BOOK_PATH}")

BOOK_CATEGORIES = ["the_9_books", "forties", "other_books"]

def get_all_book_paths():
    """إرجاع جميع ملفات JSON في مجلد by_book"""
    book_paths = []
    
    print(f"🔍 البحث في: {BY_BOOK_PATH}")
    
    if not os.path.exists(BY_BOOK_PATH):
        print(f"❌ المسار غير موجود: {BY_BOOK_PATH}")
        return book_paths
    
    # ابحث في المسار نفسه
    for category in BOOK_CATEGORIES:
        category_path = os.path.join(BY_BOOK_PATH, category)
        
        # إذا لم يكن موجوداً، ابحث في مسارات أخرى
        if not os.path.exists(category_path):
            alt_path = os.path.join(BY_BOOK_PATH, "..", category)
            if os.path.exists(alt_path):
                category_path = alt_path
        
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
