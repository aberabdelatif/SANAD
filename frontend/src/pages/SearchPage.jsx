import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { api } from '../api/client';
import SearchBar from '../components/SearchBar';
import HadithCard from '../components/HadithCard';
import { FaFilter, FaTimes, FaSearch } from 'react-icons/fa';

const SearchPage = () => {
  const [searchParams] = useSearchParams();
  const initialQuery = searchParams.get('q') || '';
  
  const [query, setQuery] = useState(initialQuery);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 20,
    total: 0,
    pages: 1
  });
  const [suggestions, setSuggestions] = useState([]);
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    book_id: '',
    grade: '',
    narrator: ''
  });
  const [filterOptions, setFilterOptions] = useState({
    books: [],
    grades: [],
    narrators: []
  });

  // تحميل خيارات الفلاتر
  useEffect(() => {
    const fetchFilters = async () => {
      try {
        const data = await api.getFilterOptions();
        setFilterOptions(data);
      } catch (error) {
        console.error('Error fetching filter options:', error);
      }
    };
    fetchFilters();
  }, []);

  // تنفيذ البحث
  useEffect(() => {
    if (!initialQuery) return;
    
    const performSearch = async () => {
      setLoading(true);
      setError(null);
      try {
        const params = {
          q: initialQuery,
          page: pagination.page,
          limit: pagination.limit,
          ...(filters.book_id && { book_id: filters.book_id }),
          ...(filters.grade && { grade: filters.grade }),
          ...(filters.narrator && { narrator: filters.narrator })
        };
        
        const data = await api.advancedSearch(params);
        setResults(data.results || []);
        setPagination({
          page: data.page || 1,
          limit: data.limit || 20,
          total: data.total || 0,
          pages: data.pages || 1
        });
        setSuggestions(data.suggestions || []);
      } catch (err) {
        setError('حدث خطأ في البحث');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    performSearch();
  }, [initialQuery, pagination.page, filters]);

  const handlePageChange = (newPage) => {
    setPagination(prev => ({ ...prev, page: newPage }));
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
    setPagination(prev => ({ ...prev, page: 1 })); // إعادة تعيين الصفحة
  };

  const clearFilters = () => {
    setFilters({ book_id: '', grade: '', narrator: '' });
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const activeFiltersCount = Object.values(filters).filter(v => v).length;

  return (
    <div className="container mx-auto px-4 py-8">
      {/* رأس البحث */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-4 flex items-center">
          <FaSearch className="ml-2 text-primary-600" />
          البحث في الأحاديث
        </h1>
        <SearchBar initialValue={initialQuery} autoFocus />
      </div>

      {/* شريط الفلاتر */}
      <div className="mb-6">
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="flex items-center space-x-2 rtl:space-x-reverse bg-gray-100 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors"
        >
          <FaFilter />
          <span>فلاتر البحث</span>
          {activeFiltersCount > 0 && (
            <span className="bg-primary-600 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center">
              {activeFiltersCount}
            </span>
          )}
        </button>

        {showFilters && (
          <div className="mt-4 bg-white rounded-lg shadow-lg p-6 border border-gray-200">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-bold text-lg">خيارات التصفية</h3>
              <button
                onClick={clearFilters}
                className="text-sm text-gray-500 hover:text-primary-600 flex items-center"
              >
                <FaTimes className="ml-1" /> مسح الكل
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* فلتر الكتاب */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">الكتاب</label>
                <select
                  value={filters.book_id}
                  onChange={(e) => handleFilterChange('book_id', e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                >
                  <option value="">الكل</option>
                  {filterOptions.books.map(book => (
                    <option key={book.id} value={book.id}>{book.name}</option>
                  ))}
                </select>
              </div>

              {/* فلتر الدرجة */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">درجة الحديث</label>
                <select
                  value={filters.grade}
                  onChange={(e) => handleFilterChange('grade', e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                >
                  <option value="">الكل</option>
                  {filterOptions.grades.map(grade => (
                    <option key={grade} value={grade}>{grade}</option>
                  ))}
                </select>
              </div>

              {/* فلتر الراوي */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">الراوي</label>
                <select
                  value={filters.narrator}
                  onChange={(e) => handleFilterChange('narrator', e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                >
                  <option value="">الكل</option>
                  {filterOptions.narrators.map(narrator => (
                    <option key={narrator} value={narrator}>{narrator}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* نتائج البحث */}
      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">جاري البحث...</p>
        </div>
      ) : error ? (
        <div className="text-center py-12 text-red-600">{error}</div>
      ) : results.length > 0 ? (
        <>
          <div className="mb-4 text-gray-600">
            تم العثور على {pagination.total.toLocaleString()} نتيجة
            {activeFiltersCount > 0 && ' (مع تطبيق الفلاتر)'}
          </div>

          <div className="space-y-4">
            {results.map(hadith => (
              <HadithCard key={hadith.id} hadith={hadith} />
            ))}
          </div>

          {/* Pagination */}
          {pagination.pages > 1 && (
            <div className="flex justify-center mt-8 space-x-2 rtl:space-x-reverse">
              <button
                onClick={() => handlePageChange(pagination.page - 1)}
                disabled={pagination.page === 1}
                className="px-4 py-2 bg-gray-200 rounded-lg disabled:opacity-50 hover:bg-gray-300 transition-colors"
              >
                السابق
              </button>
              {[...Array(pagination.pages)].map((_, i) => {
                const pageNum = i + 1;
                if (
                  pageNum === 1 ||
                  pageNum === pagination.pages ||
                  (pageNum >= pagination.page - 2 && pageNum <= pagination.page + 2)
                ) {
                  return (
                    <button
                      key={i}
                      onClick={() => handlePageChange(pageNum)}
                      className={`px-4 py-2 rounded-lg transition-colors ${
                        pageNum === pagination.page
                          ? 'bg-primary-600 text-white'
                          : 'bg-gray-200 hover:bg-gray-300'
                      }`}
                    >
                      {pageNum}
                    </button>
                  );
                } else if (pageNum === pagination.page - 3 || pageNum === pagination.page + 3) {
                  return <span key={i} className="px-2 py-2">...</span>;
                }
                return null;
              })}
              <button
                onClick={() => handlePageChange(pagination.page + 1)}
                disabled={pagination.page === pagination.pages}
                className="px-4 py-2 bg-gray-200 rounded-lg disabled:opacity-50 hover:bg-gray-300 transition-colors"
              >
                التالي
              </button>
            </div>
          )}
        </>
      ) : initialQuery ? (
        <div className="text-center py-12">
          <p className="text-gray-600 mb-4">لا توجد نتائج لـ "{initialQuery}"</p>
          {suggestions.length > 0 && (
            <div>
              <p className="text-sm text-gray-500 mb-2">اقتراحات:</p>
              <div className="flex flex-wrap justify-center gap-2">
                {suggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => {
                      window.location.href = `/search?q=${encodeURIComponent(suggestion)}`;
                    }}
                    className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : null}
    </div>
  );
};

export default SearchPage;