import React from 'react';
import { Link } from 'react-router-dom';
import { FaBook, FaList, FaStar, FaCheckCircle } from 'react-icons/fa';
import { useLanguage } from '../context/LanguageContext';

const BookCard = ({ book, featured = false }) => {
  const { t, language } = useLanguage();
  
  // تحديد لون الكتاب حسب الفئة
  const getCategoryColor = () => {
    switch(book.category) {
      case 'the_9_books':
        return 'border-primary-500 hover:shadow-primary-200';
      case 'forties':
        return 'border-accent-500 hover:shadow-accent-200';
      default:
        return 'border-secondary-500 hover:shadow-secondary-200';
    }
  };

  return (
    <Link to={`/books/${book.id}`}>
      <div className={`bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 p-6 border-t-4 ${getCategoryColor()} transform hover:-translate-y-2 group`}>
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-xl font-bold text-gray-800 mb-2 group-hover:text-primary-600 transition-colors">
              {language === 'ar' ? book.name_ar : book.name_en || book.name_ar}
            </h3>
            
            {book.author && (
              <p className="text-gray-500 text-sm mb-2">
                {book.author}
              </p>
            )}
            
            {/* درجة الحديث إن وجدت */}
            {book.grade && (
              <div className="flex items-center mb-2">
                <FaCheckCircle className="text-green-500 ml-1 text-sm" />
                <span className="text-xs text-green-600 bg-green-50 px-2 py-1 rounded-full">
                  {book.grade}
                </span>
              </div>
            )}
            
            <div className="flex items-center space-x-4 rtl:space-x-reverse mt-3">
              <div className="flex items-center text-primary-600">
                <FaList className="ml-1 rtl:mr-1" />
                <span className="text-sm font-medium">
                  {book.total_hadiths?.toLocaleString()} {t('hadiths')}
                </span>
              </div>
              
              {featured && (
                <div className="flex items-center text-accent-500">
                  <FaStar className="ml-1" />
                  <span className="text-sm font-medium">مميز</span>
                </div>
              )}
            </div>
          </div>
          
          <div className="relative">
            <FaBook className={`text-5xl ${featured ? 'text-primary-300' : 'text-gray-300'}`} />
            {featured && (
              <div className="absolute -top-2 -right-2 w-4 h-4 bg-accent-500 rounded-full animate-pulse"></div>
            )}
          </div>
        </div>

        {/* Progress bar - مثال على تقدم القراءة (يمكن تفعيله لاحقاً) */}
        <div className="w-full bg-gray-200 rounded-full h-1.5 mt-4">
          <div 
            className="bg-primary-500 h-1.5 rounded-full transition-all duration-500"
            style={{ width: `${Math.random() * 100}%` }}
          ></div>
        </div>
      </div>
    </Link>
  );
};

export default BookCard;