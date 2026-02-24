 import { useState, useEffect, useCallback } from 'react';
import { api } from '../api/client';
import { useLanguage } from '../context/LanguageContext';

export const useSearch = (initialQuery = '') => {
  const { language } = useLanguage();
  const [query, setQuery] = useState(initialQuery);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 20,
    total: 0,
    pages: 1
  });

  // تنفيذ البحث
  const performSearch = useCallback(async (searchQuery = query, page = 1) => {
    if (!searchQuery.trim()) {
      setResults([]);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await api.searchAdvanced(searchQuery, {
        page,
        limit: pagination.limit,
        fields: language === 'ar' ? 'text_ar' : 'text_ar,text_en'
      });

      setResults(response.results || []);
      setPagination({
        page: response.page || 1,
        limit: response.limit || 20,
        total: response.total || 0,
        pages: response.pages || 1
      });

      // جلب الاقتراحات إذا لم توجد نتائج
      if (response.total === 0) {
        const suggResponse = await api.getSuggestions(searchQuery);
        setSuggestions(suggResponse.suggestions || []);
      } else {
        setSuggestions([]);
      }
    } catch (err) {
      setError(err.message);
      setResults([]);
    } finally {
      setLoading(false);
    }
  }, [query, pagination.limit, language]);

  // البحث مع التأخير (debounce)
  const debouncedSearch = useCallback(
    debounce((searchQuery) => {
      performSearch(searchQuery, 1);
    }, 500),
    [performSearch]
  );

  // تحديث query وتنفيذ البحث
  const handleSearch = (newQuery) => {
    setQuery(newQuery);
    setPagination(prev => ({ ...prev, page: 1 }));
    debouncedSearch(newQuery);
  };

  // تغيير الصفحة
  const changePage = (newPage) => {
    setPagination(prev => ({ ...prev, page: newPage }));
    performSearch(query, newPage);
  };

  // تصفية النتائج
  const filterResults = useCallback(async (filters) => {
    setLoading(true);
    try {
      const response = await api.searchSimple(query, filters);
      setResults(response);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [query]);

  // تنظيف
  useEffect(() => {
    return () => {
      setResults([]);
      setError(null);
    };
  }, []);

  return {
    query,
    results,
    loading,
    error,
    suggestions,
    pagination,
    handleSearch,
    changePage,
    filterResults,
    performSearch
  };
};

// دالة debounce المساعدة
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}
