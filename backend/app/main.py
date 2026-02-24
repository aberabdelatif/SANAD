from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import books, hadiths, search
from .services.hadith_service import hadith_service

app = FastAPI(title="SANAD ENGINE", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)
app.include_router(hadiths.router)
app.include_router(search.router)  # إضافة البحث

@app.get("/")
def root():
    return {
        "message": "SANAD ENGINE is running",
        "status": "healthy",
        "total_books": len(hadith_service.books),
        "total_hadiths": len(hadith_service.hadiths)
    }

@app.get("/stats")
def stats():
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