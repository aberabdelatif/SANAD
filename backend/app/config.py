import os
from pathlib import Path

# مسار هذا الملف
HERE = Path(__file__).resolve().parent

# ROOT المشروع
PROJECT_ROOT = HERE.parent.parent

# PATH البيانات من جذر المشروع
DATA_PATH = os.getenv(
    "DATA_PATH",
    os.path.join(PROJECT_ROOT, "data", "raw", "hadith-json-main", "db")
)

BY_BOOK_PATH = os.path.join(DATA_PATH, "by_book")

BOOK_CATEGORIES = ["the_9_books", "forties", "other_books"]

def get_all_book_paths():
    book_paths = []
    print("🔍 DATA_PATH:", DATA_PATH)

    for category in BOOK_CATEGORIES:
        category_path = os.path.join(BY_BOOK_PATH, category)
        if os.path.exists(category_path):
            for file in os.listdir(category_path):
                if file.endswith(".json"):
                    book_paths.append({
                        "path": os.path.join(category_path, file),
                        "category": category,
                        "book_id": file.replace(".json", "")
                    })
        else:
            print("⚠️ Folder missing:", category_path)

    return book_paths
