import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaBook, FaSearch, FaStar, FaQuran } from 'react-icons/fa';
import SearchBar from '../components/SearchBar';
import BookCard from '../components/BookCard';
import { useLanguage } from '../context/LanguageContext';
import { api } from '../api/client';

const Home = () => {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const [featuredBooks, setFeaturedBooks] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // جلب الكتب أولاً
        const booksData = await api.getBooks();
        setFeaturedBooks(booksData.slice(0, 6));
        
        // حساب الإحصائيات يدوياً من الكتب
        const totalHadiths = booksData.reduce((sum, book) => sum + (book.total_hadiths || 0), 0);
        
        setStats({
          total_hadiths: totalHadiths,
          total_books: booksData.length,
          the_9_books: booksData.filter(b => b.category === 'the_9_books').length,
          forties: booksData.filter(b => b.category === 'forties').length,
          other_books: booksData.filter(b => b.category === 'other_books').length
        });
        
        // محاولة جلب الإحصائيات من الـ API إذا كانت موجودة
        try {
          const statsData = await api.getStats();
          if (statsData) {
            setStats(statsData);
          }
        } catch (error) {
          console.log('Stats endpoint not available, using calculated stats');
        }
        
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleSearch = (query) => {
    navigate(`/search?q=${encodeURIComponent(query)}`);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">{t('loading')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-700 to-primary-500 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-4">{t('appName')}</h1>
          <p className="text-xl mb-8 opacity-90">محرك بحث متقدم للأحاديث النبوية</p>
          
          <div className="max-w-2xl mx-auto">
            <SearchBar onSearch={handleSearch} />
          </div>
        </div>
      </div>

      {/* Stats Section */}
      {stats && (
        <div className="container mx-auto px-4 -mt-10">
          <div className="bg-white rounded-xl shadow-lg p-8 grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <FaBook className="text-3xl text-primary-600 mx-auto mb-2" />
              <div className="text-3xl font-bold text-primary-600">{stats.total_books || 17}</div>
              <div className="text-gray-600">إجمالي الكتب</div>
            </div>
            <div className="text-center">
              <FaQuran className="text-3xl text-primary-600 mx-auto mb-2" />
              <div className="text-3xl font-bold text-primary-600">{(stats.total_hadiths || 50884).toLocaleString()}</div>
              <div className="text-gray-600">إجمالي الأحاديث</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary-600">{stats.the_9_books || 9}</div>
              <div className="text-gray-600">الكتب التسعة</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary-600">{stats.forties || 3}</div>
              <div className="text-gray-600">الأربعينيات</div>
            </div>
          </div>
        </div>
      )}

      {/* Featured Books */}
      <div className="container mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold mb-8 flex items-center">
          <FaBook className="ml-2 rtl:mr-2 text-primary-600" />
          الكتب المتوفرة
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {featuredBooks.map((book) => (
            <BookCard key={book.id} book={book} />
          ))}
        </div>
        
        <div className="text-center mt-8">
          <button
            onClick={() => navigate('/books')}
            className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors"
          >
            عرض جميع الكتب
          </button>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-white py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold mb-12 text-center">مميزات ساناد</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-primary-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                <FaSearch className="text-3xl text-primary-600" />
              </div>
              <h3 className="text-xl font-bold mb-2">بحث متقدم</h3>
              <p className="text-gray-600">ابحث في {stats?.total_hadiths?.toLocaleString() || 'آلاف'} الأحاديث بسرعة ودقة</p>
            </div>
            
            <div className="text-center">
              <div className="bg-primary-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                <FaBook className="text-3xl text-primary-600" />
              </div>
              <h3 className="text-xl font-bold mb-2">مكتبة شاملة</h3>
              <p className="text-gray-600">أهم {stats?.total_books || 17} كتاباً من كتب الحديث في مكان واحد</p>
            </div>
            
            <div className="text-center">
              <div className="bg-primary-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                <FaStar className="text-3xl text-primary-600" />
              </div>
              <h3 className="text-xl font-bold mb-2">دقيق وموثوق</h3>
              <p className="text-gray-600">مصادر موثوقة وتخريج دقيق للأحاديث</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;