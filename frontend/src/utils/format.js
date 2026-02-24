 /**
 * تنسيق النصوص والأرقام
 */

// تنسيق رقم الحديث
export const formatHadithNumber = (number, bookId = '') => {
  if (!number) return '';
  return `#${number}`;
};

// تنسيق اسم الراوي
export const formatNarrator = (narrator) => {
  if (!narrator) return 'غير معروف';
  return narrator;
};

// تنسيق درجة الحديث
export const formatGrade = (grade) => {
  const grades = {
    'sahih': 'صحيح',
    'hasan': 'حسن',
    'daif': 'ضعيف',
    'sahih': 'Sahih',
    'hasan': 'Hasan',
    'daif': 'Daif'
  };
  return grades[grade?.toLowerCase()] || grade || 'غير محدد';
};

// الحصول على لون الدرجة
export const getGradeColor = (grade) => {
  const gradeLower = grade?.toLowerCase() || '';
  if (gradeLower.includes('صحيح') || gradeLower.includes('sahih')) {
    return 'text-green-600 bg-green-100';
  }
  if (gradeLower.includes('حسن') || gradeLower.includes('hasan')) {
    return 'text-blue-600 bg-blue-100';
  }
  if (gradeLower.includes('ضعيف') || gradeLower.includes('daif')) {
    return 'text-yellow-600 bg-yellow-100';
  }
  return 'text-gray-600 bg-gray-100';
};

// اختصار النص الطويل
export const truncateText = (text, maxLength = 200) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
};

// تنسيق التاريخ
export const formatDate = (date) => {
  if (!date) return '';
  return new Date(date).toLocaleDateString('ar-SA', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

// إنشاء Slug من النص
export const createSlug = (text) => {
  return text
    .toLowerCase()
    .replace(/[^\w\s]/gi, '')
    .replace(/\s+/g, '-');
};

// تنظيف النص للبحث
export const normalizeForSearch = (text) => {
  return text
    .toLowerCase()
    .replace(/[أإآ]/g, 'ا')
    .replace(/[ة]/g, 'ه')
    .replace(/[ى]/g, 'ي')
    .replace(/[^a-z\u0600-\u06FF\s]/gi, '');
};
