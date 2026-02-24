#!/usr/bin/env python
"""
سكريبت استيراد البيانات من مجلد forties
يمكن تشغيله مستقبلاً لتحميل البيانات إلى MongoDB
"""

import os
import sys
import json
from pathlib import Path

# إضافة المسار إلى PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from app.services.hadith_service import HadithService

def main():
    """استيراد البيانات وعرض إحصائيات"""
    print("🔄 بدء استيراد بيانات الأحاديث الأربعينية...")
    
    service = HadithService()
    
    print("\n📊 الإحصائيات:")
    print(f"عدد الكتب: {len(service.books)}")
    print(f"عدد الأحاديث: {len(service.hadiths)}")
    
    print("\n📚 الكتب المتوفرة:")
    for book in service.get_all_books():
        print(f"  • {book.name_ar}: {book.total_hadiths} حديث")
    
    print("\n✅ تم الاستيراد بنجاح!")

if __name__ == "__main__":
    main() 
