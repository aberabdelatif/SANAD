from typing import List, Dict, Optional, Any
import json
import os
from ..models.hadith import Hadith
from ..models.book import Book
from ..config import get_all_book_paths

class HadithService:
    def __init__(self):
        self.books: Dict[str, Book] = {}
        self.hadiths: List[Hadith] = []
        self.load_all_data()
    
    def load_all_data(self):
        """تحميل جميع الكتب والأحاديث من ملفات JSON"""
        book_paths = get_all_book_paths()
        
        # أولاً: إنشاء الكتب
        for item in book_paths:
            book_id = item['book_id']
            category = item['category']
            
            # إنشاء كائن الكتاب
            book = Book(
                id=book_id,
                name_ar=self.get_book_name_ar(book_id),
                name_en=self.get_book_name_en(book_id),
                author=self.get_book_author(book_id),
                category=category,
                total_hadiths=0,
                description=""
            )
            self.books[book_id] = book
        
        # ثانياً: قراءة الأحاديث من كل ملف
        for item in book_paths:
            try:
                with open(item['path'], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                book_id = item['book_id']
                
                # الملفات هي Objects (dict) تحتوي على مفتاح 'hadiths' أو 'chapters'
                # نحتاج إلى استخراج قائمة الأحاديث
                
                hadiths_list = []
                
                # محاولة استخراج الأحاديث من هياكل مختلفة
                if isinstance(data, dict):
                    # هيكل 1: { "hadiths": [...] }
                    if 'hadiths' in data and isinstance(data['hadiths'], list):
                        hadiths_list = data['hadiths']
                    
                    # هيكل 2: { "chapters": [ { "hadiths": [...] } ] }
                    elif 'chapters' in data and isinstance(data['chapters'], list):
                        for chapter in data['chapters']:
                            if 'hadiths' in chapter and isinstance(chapter['hadiths'], list):
                                hadiths_list.extend(chapter['hadiths'])
                    
                    # هيكل 3: { "data": [...] }
                    elif 'data' in data and isinstance(data['data'], list):
                        hadiths_list = data['data']
                    
                    # هيكل 4: { "result": { "hadiths": [...] } }
                    elif 'result' in data and isinstance(data['result'], dict):
                        if 'hadiths' in data['result'] and isinstance(data['result']['hadiths'], list):
                            hadiths_list = data['result']['hadiths']
                    
                    # إذا لم نجد أي هيكل معروف، نحاول أخذ أول قيمة قائمة في الـ object
                    else:
                        for key, value in data.items():
                            if isinstance(value, list) and len(value) > 0:
                                # نتأكد أن العناصر تحتوي على حقول حديث
                                if len(value) > 0 and isinstance(value[0], dict):
                                    sample = value[0]
                                    if 'arabic' in sample or 'text' in sample or 'hadith' in sample:
                                        hadiths_list = value
                                        print(f"📌 وجدنا قائمة في المفتاح: {key}")
                                        break
                
                elif isinstance(data, list):
                    # إذا كان الملف قائمة مباشرة
                    hadiths_list = data
                
                # معالجة الأحاديث المستخرجة
                if hadiths_list:
                    book_hadiths = []
                    for idx, hadith_data in enumerate(hadiths_list):
                        hadith = self.parse_hadith(hadith_data, book_id, idx+1)
                        if hadith:
                            self.hadiths.append(hadith)
                            book_hadiths.append(hadith)
                    
                    # تحديث عدد الأحاديث في الكتاب
                    if book_id in self.books:
                        self.books[book_id].total_hadiths = len(book_hadiths)
                    
                    print(f"✅ {self.books[book_id].name_ar}: {len(book_hadiths)} حديث")
                else:
                    print(f"⚠️ لم نجد أحاديث في {item['path']}")
                
            except json.JSONDecodeError as e:
                print(f"❌ خطأ في JSON {item['path']}: {e}")
            except Exception as e:
                print(f"❌ خطأ في تحميل {item['path']}: {e}")
        
        print(f"\n📊 الإجمالي: {len(self.books)} كتب, {len(self.hadiths)} حديث")
    
    def parse_hadith(self, data: dict, book_id: str, default_number: int) -> Optional[Hadith]:
        """تحويل JSON إلى كائن Hadith"""
        try:
            # محاولة استخراج رقم الحديث
            hadith_number = data.get('id') or data.get('number') or data.get('hadithNumber') or default_number
            
            # النص العربي - جرب الحقول المختلفة
            arabic = data.get('arabic') or data.get('text_ar') or data.get('text') or data.get('hadith') or ''
            
            # النص الإنجليزي
            english_data = data.get('english', {})
            if isinstance(english_data, dict):
                english_text = english_data.get('text', '')
                english_narrator = english_data.get('narrator', '')
            else:
                english_text = data.get('english', '')
                english_narrator = data.get('narrator', '')
            
            # إنشاء معرف فريد
            hadith_id = f"{book_id}_{hadith_number}"
            
            # معالجة chapter_id
            chapter_id = data.get('chapterId') or data.get('chapter') or data.get('chapter_id')
            
            # درجة الحديث
            grade = data.get('grade') or data.get('grad') or data.get('classification')
            
            return Hadith(
                id=hadith_id,
                book_id=book_id,
                hadith_number=int(hadith_number) if hadith_number else default_number,
                chapter_id=chapter_id,
                arabic=arabic,
                english_narrator=english_narrator,
                english_text=english_text,
                grade=grade
            )
        except Exception as e:
            return None
    
    def get_book_name_ar(self, book_id: str) -> str:
        """تحويل معرف الكتاب إلى اسم عربي"""
        names = {
            'abudawud': 'سنن أبي داود',
            'ahmed': 'مسند أحمد',
            'bukhari': 'صحيح البخاري',
            'darimi': 'سنن الدارمي',
            'ibnmajah': 'سنن ابن ماجه',
            'malik': 'موطأ مالك',
            'muslim': 'صحيح مسلم',
            'nasai': 'سنن النسائي',
            'tirmidhi': 'جامع الترمذي',
            'nawawi40': 'الأربعون النووية',
            'qudsi40': 'الأربعون القدسية',
            'shahwaliullah40': 'أربعون الشاه ولي الله',
            'aladab_almufrad': 'الأدب المفرد',
            'bulugh_almaram': 'بلوغ المرام',
            'mishkat_almasabih': 'مشكاة المصابيح',
            'riyad_assalihin': 'رياض الصالحين',
            'shamail_muhammadiyah': 'الشمائل المحمدية'
        }
        return names.get(book_id, book_id.replace('_', ' '))
    
    def get_book_name_en(self, book_id: str) -> str:
        names = {
            'abudawud': 'Sunan Abi Dawud',
            'ahmed': 'Musnad Ahmad',
            'bukhari': 'Sahih al-Bukhari',
            'darimi': 'Sunan ad-Darimi',
            'ibnmajah': 'Sunan Ibn Majah',
            'malik': 'Muwatta Malik',
            'muslim': 'Sahih Muslim',
            'nasai': 'Sunan an-Nasa\'i',
            'tirmidhi': 'Jami` at-Tirmidhi',
            'nawawi40': 'Al-Nawawi\'s Forty Hadith',
            'qudsi40': 'Forty Qudsi Hadith',
            'shahwaliullah40': 'Shah Waliullah\'s Forty',
            'aladab_almufrad': 'Al-Adab Al-Mufrad',
            'bulugh_almaram': 'Bulugh al-Maram',
            'mishkat_almasabih': 'Mishkat al-Masabih',
            'riyad_assalihin': 'Riyad as-Salihin',
            'shamail_muhammadiyah': 'Shamail Muhammadiyah'
        }
        return names.get(book_id, book_id.replace('_', ' ').title())
    
    def get_book_author(self, book_id: str) -> str:
        """الحصول على اسم المؤلف"""
        authors = {
            'abudawud': 'أبو داود السجستاني',
            'ahmed': 'أحمد بن حنبل',
            'bukhari': 'محمد بن إسماعيل البخاري',
            'darimi': 'عبد الله بن عبد الرحمن الدارمي',
            'ibnmajah': 'محمد بن يزيد القزويني',
            'malik': 'مالك بن أنس',
            'muslim': 'مسلم بن الحجاج',
            'nasai': 'أحمد بن شعيب النسائي',
            'tirmidhi': 'محمد بن عيسى الترمذي',
            'nawawi40': 'يحيى بن شرف النووي',
            'qudsi40': 'محيي الدين بن عربي',
            'shahwaliullah40': 'شاه ولي الله الدهلوي',
            'aladab_almufrad': 'محمد بن إسماعيل البخاري',
            'bulugh_almaram': 'ابن حجر العسقلاني',
            'mishkat_almasabih': 'التبريزي',
            'riyad_assalihin': 'يحيى بن شرف النووي',
            'shamail_muhammadiyah': 'أبو عيسى الترمذي'
        }
        return authors.get(book_id, '')
    
    def get_all_books(self) -> List[Book]:
        return list(self.books.values())
    
    def get_book(self, book_id: str) -> Optional[Book]:
        return self.books.get(book_id)
    
    def get_all_hadiths(self) -> List[Hadith]:
        return self.hadiths
    
    def get_hadiths_by_book(self, book_id: str) -> List[Hadith]:
        return [h for h in self.hadiths if h.book_id == book_id]
    
    def get_hadith_by_id(self, hadith_id: str) -> Optional[Hadith]:
        for h in self.hadiths:
            if h.id == hadith_id:
                return h
        return None

# إنشاء نسخة وحيدة
hadith_service = HadithService()