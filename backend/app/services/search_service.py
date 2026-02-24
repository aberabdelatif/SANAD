import re
import math
from typing import List, Dict, Optional, Tuple
from collections import Counter
from ..models.hadith import Hadith
from .hadith_service import hadith_service

class SearchService:
    def __init__(self):
        self.hadiths = hadith_service.get_all_hadiths()
        self.build_index()
    
    def build_index(self):
        """بناء فهرس للبحث السريع"""
        print("🔍 بناء فهرس البحث...")
        self.word_index = {}
        self.hadith_lengths = []
        
        for hadith in self.hadiths:
            words = self.tokenize(hadith.arabic)
            self.hadith_lengths.append(len(words))
            
            # إضافة إلى فهرس الكلمات
            for word in set(words):
                if len(word) > 2:  # تجاهل الكلمات القصيرة جداً
                    if word not in self.word_index:
                        self.word_index[word] = []
                    self.word_index[word].append(hadith.id)
        
        # حساب IDF (Inverse Document Frequency)
        self.idf = {}
        total_hadiths = len(self.hadiths)
        for word, hadith_ids in self.word_index.items():
            self.idf[word] = math.log(total_hadiths / (len(hadith_ids) + 1))
        
        print(f"✅ فهرس البحث جاهز: {len(self.word_index)} كلمة فريدة")
    
    def tokenize(self, text: str) -> List[str]:
        """تقسيم النص إلى كلمات مع تطبيع"""
        if not text:
            return []
        # تنظيف النص من علامات الترقيم والتشكيل
        text = re.sub(r'[^\w\s]', '', text)
        # تقسيم إلى كلمات
        words = text.split()
        return words
    
    def normalize_arabic(self, text: str) -> str:
        """تطبيع النص العربي للبحث"""
        if not text:
            return ""
        # إزالة التشكيل
        text = re.sub(r'[ًٌٍَُِّْ]', '', text)
        # توحيد الألف
        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
        # توحيد التاء المربوطة والهاء
        text = text.replace('ة', 'ه')
        return text
    
    def simple_search(self, query: str, filters: Optional[Dict] = None) -> List[Hadith]:
        """بحث بسيط (تطابق جزئي)"""
        if not query:
            return []
        
        query_normalized = self.normalize_arabic(query)
        results = []
        
        for hadith in self.hadiths:
            # تطبيق الفلاتر أولاً
            if filters:
                if not self.apply_filters(hadith, filters):
                    continue
            
            # البحث في النص العربي
            text_normalized = self.normalize_arabic(hadith.arabic)
            if query_normalized in text_normalized:
                results.append(hadith)
                continue
            
            # البحث في النص الإنجليزي (إذا وجد)
            if hadith.english_text and query.lower() in hadith.english_text.lower():
                results.append(hadith)
        
        return results
    
    def advanced_search(self, query: str, options: Optional[Dict] = None) -> Dict:
        """بحث متقدم مع ترتيب حسب الصلة"""
        if not query:
            return {"results": [], "total": 0, "suggestions": []}
        
        options = options or {}
        filters = options.get('filters', {})
        page = options.get('page', 1)
        limit = options.get('limit', 20)
        
        # تطبيع الاستعلام
        query_normalized = self.normalize_arabic(query)
        query_words = self.tokenize(query_normalized)
        
        # حساب الصلة لكل حديث
        scored_results = []
        for hadith in self.hadiths:
            # تطبيق الفلاتر
            if filters and not self.apply_filters(hadith, filters):
                continue
            
            # حساب درجة الصلة
            score = self.calculate_relevance(hadith, query_normalized, query_words)
            if score > 0:
                scored_results.append((hadith, score))
        
        # ترتيب حسب الصلة
        scored_results.sort(key=lambda x: x[1], reverse=True)
        
        # تطبيق التقسيم
        total = len(scored_results)
        start = (page - 1) * limit
        end = start + limit
        paginated = [item[0] for item in scored_results[start:end]]
        
        # اقتراحات إذا لم توجد نتائج
        suggestions = []
        if total == 0:
            suggestions = self.get_suggestions(query)
        
        return {
            "results": paginated,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": math.ceil(total / limit) if total > 0 else 0,
            "suggestions": suggestions,
            "query": query
        }
    
    def calculate_relevance(self, hadith: Hadith, query_normalized: str, query_words: List[str]) -> float:
        """حساب درجة صلة الحديث بالاستعلام"""
        score = 0.0
        text_normalized = self.normalize_arabic(hadith.arabic)
        
        # 1. تطابق تام (أعلى درجة)
        if query_normalized in text_normalized:
            score += 10.0
        
        # 2. تطابق الكلمات
        text_words = self.tokenize(text_normalized)
        for q_word in query_words:
            if q_word in text_words:
                # استخدام IDF للكلمة (الكلمات النادرة أهم)
                word_idf = self.idf.get(q_word, 1.0)
                score += word_idf
            elif len(q_word) > 3 and q_word[:-1] in text_words:  # تطابق جزئي (بدون آخر حرف)
                score += 0.5
        
        # 3. مكافأة للحديث القصير (أكثر دقة)
        if len(text_words) < 20:
            score *= 1.2
        elif len(text_words) > 100:
            score *= 0.8
        
        # 4. مكافأة إذا كان الحديث في الكتاب المطلوب (إذا وجد)
        # لا نحتاجها هنا لأن الفلاتر تطبق قبل الحساب
        
        return score
    
    def apply_filters(self, hadith: Hadith, filters: Dict) -> bool:
        """تطبيق الفلاتر على الحديث"""
        for key, value in filters.items():
            if key == 'book_id' and hadith.book_id != value:
                return False
            elif key == 'grade' and hadith.grade and value not in hadith.grade:
                return False
            elif key == 'narrator' and hadith.english_narrator:
                if value not in hadith.english_narrator:
                    return False
        return True
    
    def get_suggestions(self, query: str, max_suggestions: int = 5) -> List[str]:
        """اقتراحات للبحث بناءً على الكلمات الموجودة في الفهرس"""
        query_normalized = self.normalize_arabic(query)
        if len(query_normalized) < 2:
            return []
        
        suggestions = []
        # البحث عن كلمات تبدأ بنفس الحروف
        for word in self.word_index.keys():
            if word.startswith(query_normalized) and word != query_normalized:
                suggestions.append(word)
                if len(suggestions) >= max_suggestions:
                    break
        
        # إذا لم نجد، نبحث عن كلمات تحتوي على الاستعلام
        if not suggestions:
            for word in self.word_index.keys():
                if query_normalized in word and word != query_normalized:
                    suggestions.append(word)
                    if len(suggestions) >= max_suggestions:
                        break
        
        return suggestions
    
    def get_filters_options(self) -> Dict:
        """الحصول على خيارات الفلاتر المتاحة"""
        books = hadith_service.get_all_books()
        grades = set()
        narrators = set()
        
        for hadith in self.hadiths[:1000]:  # نأخذ عينة لتجنب التكلفة العالية
            if hadith.grade:
                grades.add(hadith.grade)
            if hadith.english_narrator:
                narrators.add(hadith.english_narrator)
        
        return {
            "books": [{"id": b.id, "name": b.name_ar} for b in books],
            "grades": list(grades)[:50],
            "narrators": list(narrators)[:50]
        }

# إنشاء كائن الخدمة
search_service = SearchService()