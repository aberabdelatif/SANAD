import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import { FaBook, FaList } from 'react-icons/fa';

const BooksPage = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        console.log('جاري تحميل الكتب...');
        const data = await api.getBooks();
        console.log('الكتب المستلمة:', data);
        setBooks(data);
      } catch (err) {
        console.error('خطأ في تحميل الكتب:', err);
        setError('فشل تحميل الكتب');
      } finally {
        setLoading(false);
      }
    };
    fetchBooks();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12 text-red-600">
        {error}
      </div>
    );
  }

  // تنظيم الكتب حسب الفئة
  const the9Books = books.filter(b => b.category === 'the_9_books');
  const fortiesBooks = books.filter(b => b.category === 'forties');
  const otherBooks = books.filter(b => b.category === 'other_books');

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-center">جميع الكتب</h1>
      
      {the9Books.length > 0 && (
        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-4 text-primary-600 border-r-4 border-primary-600 pr-4">
            الكتب التسعة
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {the9Books.map(book => (
              <Link key={book.id} to={`/books/${book.id}`}>
                <div className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow p-6 border border-gray-200 hover:border-primary-400">
                  <div className="flex items-center mb-4">
                    <FaBook className="text-3xl text-primary-500 ml-3" />
                    <h3 className="text-xl font-bold text-gray-800">{book.name_ar}</h3>
                  </div>
                  <p className="text-gray-600 mb-2 text-sm">{book.name_en}</p>
                  <p className="text-sm text-gray-500 mb-4">{book.author}</p>
                  <div className="flex items-center text-primary-600">
                    <FaList className="ml-2" />
                    <span className="font-medium">{book.total_hadiths?.toLocaleString()} حديث</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}

      {fortiesBooks.length > 0 && (
        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-4 text-amber-600 border-r-4 border-amber-600 pr-4">
            الأربعينيات
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {fortiesBooks.map(book => (
              <Link key={book.id} to={`/books/${book.id}`}>
                <div className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow p-6 border border-gray-200 hover:border-amber-400">
                  <div className="flex items-center mb-4">
                    <FaBook className="text-3xl text-amber-500 ml-3" />
                    <h3 className="text-xl font-bold text-gray-800">{book.name_ar}</h3>
                  </div>
                  <p className="text-gray-600 mb-2 text-sm">{book.name_en}</p>
                  <p className="text-sm text-gray-500 mb-4">{book.author}</p>
                  <div className="flex items-center text-amber-600">
                    <FaList className="ml-2" />
                    <span className="font-medium">{book.total_hadiths?.toLocaleString()} حديث</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}

      {otherBooks.length > 0 && (
        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-4 text-secondary-600 border-r-4 border-secondary-600 pr-4">
            كتب أخرى
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {otherBooks.map(book => (
              <Link key={book.id} to={`/books/${book.id}`}>
                <div className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow p-6 border border-gray-200 hover:border-secondary-400">
                  <div className="flex items-center mb-4">
                    <FaBook className="text-3xl text-secondary-500 ml-3" />
                    <h3 className="text-xl font-bold text-gray-800">{book.name_ar}</h3>
                  </div>
                  <p className="text-gray-600 mb-2 text-sm">{book.name_en}</p>
                  <p className="text-sm text-gray-500 mb-4">{book.author}</p>
                  <div className="flex items-center text-secondary-600">
                    <FaList className="ml-2" />
                    <span className="font-medium">{book.total_hadiths?.toLocaleString()} حديث</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default BooksPage;