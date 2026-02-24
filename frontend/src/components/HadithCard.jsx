import React, { useState } from 'react';
import { FaUser, FaStar, FaCopy, FaCheck } from 'react-icons/fa';
import { useLanguage } from '../context/LanguageContext';
// إزالة الدوال غير المستخدمة مؤقتاً
// import { formatGrade, getGradeColor, truncateText } from '../utils/format';

// دوال مؤقتة للتنسيق
const formatGrade = (grade) => grade || 'غير محدد';
const getGradeColor = (grade) => {
  const gradeLower = grade?.toLowerCase() || '';
  if (gradeLower.includes('صحيح') || gradeLower.includes('sahih')) {
    return 'text-green-600 bg-green-100';
  }
  if (gradeLower.includes('حسن') || gradeLower.includes('hasan')) {
    return 'text-blue-600 bg-blue-100';
  }
  return 'text-gray-600 bg-gray-100';
};
const truncateText = (text, maxLength = 150) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
};

const HadithCard = ({ hadith, showFullText = false }) => {
  const { t, language } = useLanguage();
  const [copied, setCopied] = useState(false);
  const [expanded, setExpanded] = useState(showFullText);

  // التحقق من وجود hadith وخصائصه
  if (!hadith) {
    return null; // لا تعرض شيئاً إذا لم يكن هناك حديث
  }

  const handleCopy = () => {
    if (hadith.arabic) {
      navigator.clipboard.writeText(hadith.arabic);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // التأكد من وجود النص
  const arabicText = hadith.arabic || '';
  const textToShow = expanded ? arabicText : truncateText(arabicText, 150);
  const gradeColor = getGradeColor(hadith.grade);

  return (
    <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow">
      {/* رأس الحديث */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3 rtl:space-x-reverse">
          <span className="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm font-medium">
            {t('hadithNumber')} {hadith.hadith_number || '?'}
          </span>
          
          {hadith.grade && (
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${gradeColor}`}>
              {formatGrade(hadith.grade)}
            </span>
          )}
        </div>
        
        {arabicText && (
          <button
            onClick={handleCopy}
            className="text-gray-400 hover:text-primary-600 transition-colors"
            title="نسخ النص"
          >
            {copied ? <FaCheck className="text-green-500" /> : <FaCopy />}
          </button>
        )}
      </div>

      {/* نص الحديث */}
      {arabicText ? (
        <div className="mb-4">
          <p className="text-gray-800 text-lg leading-loose arabic-text text-right">
            {textToShow}
            {!showFullText && arabicText.length > 150 && (
              <button
                onClick={() => setExpanded(!expanded)}
                className="mr-2 text-primary-600 hover:text-primary-700 text-sm font-medium"
              >
                {expanded ? 'عرض أقل' : '...عرض المزيد'}
              </button>
            )}
          </p>
        </div>
      ) : (
        <p className="text-gray-500 mb-4">لا يوجد نص للحديث</p>
      )}

      {/* معلومات إضافية */}
      <div className="flex items-center justify-between text-sm text-gray-500 pt-4 border-t border-gray-100">
        {hadith.english_narrator && (
          <div className="flex items-center">
            <FaUser className="ml-1 rtl:mr-1" />
            <span>{hadith.english_narrator}</span>
          </div>
        )}
        
        {hadith.book_id && (
          <div className="flex items-center">
            <FaStar className="ml-1 rtl:mr-1" />
            <span>{hadith.book_id}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default HadithCard;