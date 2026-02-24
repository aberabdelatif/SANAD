# 🕌 SANAD ENGINE - محرك بحث الحديث النبوي الشريف

**SANAD ENGINE** is a high-performance search engine for Hadith (Prophetic traditions) that provides fast and accurate access to over **50,000 hadiths** from **17 major Hadith collections**. It is designed for researchers, students, and anyone interested in the Sunnah.

**محرك سند** هو محرك بحث عالي الأداء للأحاديث النبوية يتيح الوصول السريع والدقيق إلى أكثر من **٥٠ ألف حديث** من **١٧ كتاباً** من كتب السنة النبوية. صُمم للباحثين والطلاب وكل مهتم بالسنة النبوية.

---

## ✨ Features | المميزات

### ✅ Current Features | المميزات الحالية
- **Comprehensive Collection**: 50,884 hadiths from 17 books (Sahih al-Bukhari, Sahih Muslim, Sunan Abi Dawud, Jami` at-Tirmidhi, Sunan an-Nasa'i, Sunan Ibn Majah, Muwatta Malik, Musnad Ahmad, Sunan ad-Darimi, Riyad as-Salihin, Shamail al-Muhammadiyah, Bulugh al-Maram, Al-Adab Al-Mufrad, Mishkat al-Masabih, Al-Nawawi's Forty, Forty Qudsi, Shah Waliullah's Forty).
- **Advanced Search**: Full-text search with relevance ranking (TF-IDF), filters by book, narrator, grade.
- **Smart Suggestions**: Real‑time search suggestions as you type.
- **Bilingual**: Fully supports Arabic and English interfaces.
- **Fast & Scalable**: Built with FastAPI and React, optimized for performance.

### 🔮 Planned Features | المميزات المستقبلية
- **Friday Sermon Generator**: AI‑assisted generation of Khutbah (Friday sermon) based on selected hadiths and themes.  
  **توليد خطبة الجمعة**: توليد خطبة الجمعة بمساعدة الذكاء الاصطناعي بناءً على أحاديث ومواضيع مختارة.
- **Daily Wisdom**: Random daily hadith or wise saying with explanation.  
  **حكمة اليوم**: حديث أو حكمة يومية عشوائية مع شرح.
- **Semantic Search**: Search by meaning using embeddings.
- **User Accounts**: Save favorite hadiths and create collections.
- **Mobile App**: React Native version for iOS and Android.

---

## 🚀 Quick Start | التشغيل السريع

### Prerequisites | المتطلبات
- Python 3.10+
- Node.js 18+
- npm / yarn

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`. Interactive docs at `/docs`.

### Frontend (React)
```bash
cd frontend
npm install
npm start
```
The app will open at `http://localhost:3000`.

---

## 🗂 Project Structure | هيكل المشروع

```
sanad-project/
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── models/        # Pydantic models
│   │   ├── routes/        # API endpoints
│   │   ├── services/      # Business logic (search, data loading)
│   │   └── main.py
│   └── requirements.txt
├── frontend/              # React application
│   ├── public/
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components
│   │   └── App.jsx
│   └── package.json
├── data/                  # Raw JSON hadith files (not included in repo)
└── README.md
```

---

## 📊 Statistics | الإحصائيات
| | |
|---|---|
| Total Hadiths | 50,884 |
| Total Books | 17 |
| The Nine Books | 9 |
| Forties (Arba‘een) | 3 |
| Other Books | 5 |

---

## 🛠 Technology Stack | التقنيات المستخدمة

- **Backend**: FastAPI, Pydantic, Uvicorn
- **Frontend**: React, React Router, Tailwind CSS, Axios
- **Data**: JSON (source: [hadith-json](https://github.com/ceeren/hadith-json))
- **Search Algorithm**: TF‑IDF with custom Arabic normalizer

---

## 🤝 Contributing | المساهمة

Contributions are welcome! Please open an issue or pull request.

نرحب بالمساهمات! يرجى فتح issue أو pull request.

---

## 📜 License | الترخيص

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

هذا المشروع مرخص تحت رخصة MIT.

---

**Made with ❤️ for the Ummah** | **صنع بحب للأمة**
