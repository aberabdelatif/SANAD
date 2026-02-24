import React, { createContext, useState, useContext, useEffect } from 'react';

// إنشاء Context
const LanguageContext = createContext();

// الترجمات
export const translations = {
  ar: {
    // عام
    appName: 'سند',
    search: 'بحث',
    loading: 'جاري التحميل...',
    error: 'حدث خطأ',
    noResults: 'لا توجد نتائج',
    back: 'رجوع',
    next: 'التالي',
    previous: 'السابق',
    
    // الصفحات
    home: 'الرئيسية',
    books: 'الكتب',
    chapters: 'الأبواب',
    hadiths: 'الأحاديث',
    
    // الكتاب
    bookName: 'اسم الكتاب',
    author: 'المؤلف',
    totalHadiths: 'عدد الأحاديث',
    
    // الحديث
    hadithNumber: 'رقم الحديث',
    narrator: 'الراوي',
    grade: 'الدرجة',
    text: 'النص',
    
    // البحث
    searchPlaceholder: 'ابحث عن حديث...',
    searchResults: 'نتائج البحث',
    filters: 'التصفية',
    advancedSearch: 'بحث متقدم',
    suggestions: 'اقتراحات',
    
    // الأخطاء
    notFound: 'الصفحة غير موجودة',
    serverError: 'خطأ في الخادم',
  },
  en: {
    // General
    appName: 'SANAD',
    search: 'Search',
    loading: 'Loading...',
    error: 'Error occurred',
    noResults: 'No results found',
    back: 'Back',
    next: 'Next',
    previous: 'Previous',
    
    // Pages
    home: 'Home',
    books: 'Books',
    chapters: 'Chapters',
    hadiths: 'Hadiths',
    
    // Book
    bookName: 'Book Name',
    author: 'Author',
    totalHadiths: 'Total Hadiths',
    
    // Hadith
    hadithNumber: 'Hadith Number',
    narrator: 'Narrator',
    grade: 'Grade',
    text: 'Text',
    
    // Search
    searchPlaceholder: 'Search for hadith...',
    searchResults: 'Search Results',
    filters: 'Filters',
    advancedSearch: 'Advanced Search',
    suggestions: 'Suggestions',
    
    // Errors
    notFound: 'Page not found',
    serverError: 'Server error',
  }
};

// Provider Component
export const LanguageProvider = ({ children }) => {
  // محاولة استرجاع اللغة المحفوظة
  const savedLanguage = localStorage.getItem('language') || 'ar';
  const [language, setLanguage] = useState(savedLanguage);
  const [dir, setDir] = useState('rtl');

  // تغيير اللغة
  const changeLanguage = (lang) => {
    setLanguage(lang);
    setDir(lang === 'ar' ? 'rtl' : 'ltr');
    localStorage.setItem('language', lang);
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
  };

  useEffect(() => {
    // تطبيق اللغة عند التحميل
    changeLanguage(savedLanguage);
  }, []);

  // دالة للترجمة
  const t = (key) => {
    return translations[language]?.[key] || translations.ar[key] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, dir, changeLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

// Hook لاستخدام Context
export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within LanguageProvider');
  }
  return context;
}; 
