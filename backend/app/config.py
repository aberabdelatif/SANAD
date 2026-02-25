import os
from pathlib import Path

# Get the absolute path to the directory where this script is located
# This resolves to: /opt/render/project/src/backend/app/config.py (or similar on Render)
CURRENT_FILE_DIR = Path(__file__).resolve().parent

# Go up three levels: from /app/backend/app to /app
# This is the root of your application inside the container (/app)
APP_ROOT = CURRENT_FILE_DIR.parent.parent.parent

# Construct the data path relative to the APP_ROOT
# We assume the 'data' folder is inside the 'backend' folder, which is inside APP_ROOT
# Path: /app/backend/data/raw/hadith-json-main/db
DATA_PATH = os.path.join(APP_ROOT, "backend", "data", "raw", "hadith-json-main", "db")

print(f"🔍 [Config] APP_ROOT calculated as: {APP_ROOT}")
print(f"🔍 [Config] Looking for data in: {DATA_PATH}")

if os.path.exists(DATA_PATH):
    print(f"✅ [Config] Data path EXISTS.")
else:
    print(f"❌ [Config] Data path DOES NOT EXIST. Checking alternative locations...")
    # Fallback: if the structure is different (e.g., data is at the same level as backend)
    alt_path = os.path.join(APP_ROOT, "data", "raw", "hadith-json-main", "db")
    if os.path.exists(alt_path):
        print(f"✅ [Config] Found data at alternative path: {alt_path}")
        DATA_PATH = alt_path
    else:
        print(f"❌ [Config] Alternative path also not found: {alt_path}")

BY_BOOK_PATH = os.path.join(DATA_PATH, "by_book")
BOOK_CATEGORIES = ["the_9_books", "forties", "other_books"]

def get_all_book_paths():
    """إرجاع جميع ملفات JSON في مجلد by_book"""
    book_paths = []
    print(f"🔍 [Config] Searching for books in: {BY_BOOK_PATH}")

    if not os.path.exists(BY_BOOK_PATH):
        print(f"❌ [Config] BY_BOOK_PATH does not exist: {BY_BOOK_PATH}")
        return book_paths

    for category in BOOK_CATEGORIES:
        category_path = os.path.join(BY_BOOK_PATH, category)
        if os.path.exists(category_path):
            files = [f for f in os.listdir(category_path) if f.endswith('.json')]
            print(f"✅ [Config] Found {len(files)} files in {category}")
            for file in files:
                full_path = os.path.join(category_path, file)
                book_paths.append({
                    'path': full_path,
                    'category': category,
                    'book_id': file.replace('.json', '')
                })
        else:
            print(f"⚠️ [Config] Category folder not found: {category_path}")

    print(f"📊 [Config] Total book files found: {len(book_paths)}")
    return book_paths
