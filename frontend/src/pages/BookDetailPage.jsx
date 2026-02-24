import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../api/client';
import { FaArrowRight, FaBook } from 'react-icons/fa';

const BookDetailPage = () => {
  const { bookId } = useParams();
  const [book, setBook] = useState(null);
  const [hadiths, setHadiths] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [displayCount, setDisplayCount] = useState(20);

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('جاري تحميل بيانات الكتاب:', bookId);
        const [bookData, hadithsData] = await Promise.all([
          api.getBook(bookId),
          api.getHadithsByBook(bookId)
        ]);
        console.log('بيانات الكتاب:', bookData);
        console.log('عدد الأحاديث:', hadithsData.length);
        setBook(bookData);
        setHadiths(hadithsData);
      } catch (err) {
        console.error('خطأ في تحميل البيانات:', err);
        setError('فشل تحميل البيانات');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [bookId]);

  const loadMore = () => {
    setDisplayCount(prev => prev + 20);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error || !book) {
    return (
      <div className="text-center py-12 text-red-600">
        {error || 'الكتاب غير موجود'}
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* معلومات الكتاب */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="flex items-center mb-4">
          <Link to="/books" className="text-primary-600 hover:text-primary-700 ml-4">
            <FaArrowRight size={20} />
          </Link>
          <FaBook className="text-3xl text-primary-600 ml-3" />
          <div>
            <h1 className="text-3xl font-bold">{book.name_ar}</h1>
            <p className="text-gray-600">{book.name_en}</p>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
          <div>
            <p className="text-gray-700"><span className="font-bold">المؤلف:</span> {book.author}</p>
            <p className="text-gray-700"><span className="font-bold">عدد الأحاديث:</span> {book.total_hadiths?.toLocaleString()}</p>
          </div>
          <div>
            <p className="text-gray-700"><span className="font-bold">التصنيف:</span> {
              book.category === 'the_9_books' ? 'الكتب التسعة' : 
              book.category === 'forties' ? 'الأربعينيات' : 
              'كتب أخرى'
            }</p>
          </div>
        </div>
      </div>

      {/* قائمة الأحاديث */}
      <h2 className="text-2xl font-bold mb-4">الأحاديث</h2>
      <div className="space-y-4">
        {hadiths.slice(0, displayCount).map((hadith) => (
          <div key={hadith.id} className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow">
            <div className="flex justify-between items-center mb-2">
              <span className="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm">
                الحديث {hadith.hadith_number}
              </span>
              {hadith.grade && (
                <span className="text-sm text-gray-500">{hadith.grade}</span>
              )}
            </div>
            <p className="text-gray-800 leading-loose text-lg font-arabic text-right">
              {hadith.arabic}
            </p>
            {hadith.english_narrator && (
              <p className="text-gray-600 mt-2 text-sm">الراوي: {hadith.english_narrator}</p>
            )}
          </div>
        ))}
      </div>
      
      {hadiths.length > displayCount && (
        <div className="text-center mt-8">
          <button
            onClick={loadMore}
            className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors"
          >
            عرض المزيد ({hadiths.length - displayCount} متبقي)
          </button>
        </div>
      )}
    </div>
  );
};

export default BookDetailPage;