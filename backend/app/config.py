import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "hadith-json-main", "db")
BY_BOOK_PATH = os.path.join(DATA_PATH, "by_book")

BOOK_CATEGORIES = ["the_9_books", "forties", "other_books"]

def get_all_book_paths():
    """إرجاع جميع ملفات JSON في مجلد by_book"""
    book_paths = []
    for category in BOOK_CATEGORIES:
        category_path = os.path.join(BY_BOOK_PATH, category)
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