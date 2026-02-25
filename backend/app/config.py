from pathlib import Path

# هذا يشير إلى /app/app
BASE_DIR = Path(__file__).resolve().parent

# هذا يصعد إلى /app
PROJECT_ROOT = BASE_DIR.parent

# المسار الحقيقي داخل Docker
DATA_PATH = PROJECT_ROOT / "backend" / "data" / "raw" / "hadith-json-main" / "db"

print(f"🔍 DATA_PATH: {DATA_PATH}")

BY_BOOK_PATH = DATA_PATH / "by_book"

BOOK_CATEGORIES = ["the_9_books", "forties", "other_books"]


def get_all_book_paths():
    book_paths = []

    print(f"🔍 Searching in: {BY_BOOK_PATH}")

    if not BY_BOOK_PATH.exists():
        print("❌ by_book folder not found")
        return book_paths

    for category in BOOK_CATEGORIES:
        category_path = BY_BOOK_PATH / category

        if category_path.exists():
            files = list(category_path.glob("*.json"))
            print(f"✅ Found {len(files)} files in {category}")

            for file in files:
                book_paths.append({
                    "path": str(file),
                    "category": category,
                    "book_id": file.stem
                })
        else:
            print(f"⚠️ Category not found: {category_path}")

    print(f"📊 Total books found: {len(book_paths)}")
    return book_paths
