import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { FaArrowRight, FaFolder } from 'react-icons/fa';
import { useLanguage } from '../context/LanguageContext';
import { api } from '../api/client';
import HadithCard from '../components/HadithCard';
import Pagination from '../components/Pagination';

const ChapterPage = () => {
  const { chapterId } = useParams();
  const { t } = useLanguage();
  const [chapter, setChapter] = useState(null);
  const [hadiths, setHadiths] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 20,
    total: 0,
    pages: 1
  });

  useEffect(() => {
    const fetchChapterData = async () => {
      setLoading(true);
      try {
        const [chapterData, hadithsData] = await Promise.all([
          api.getChapter(chapterId),
          api.getChapterHadiths(chapterId, pagination.page, pagination.limit)
        ]);
        
        setChapter(chapterData);
        setHadiths(hadithsData.items || []);
        setPagination({
          page: hadithsData.page || 1,
          limit: hadithsData.limit || 20,
          total: hadithsData.total || 0,
          pages: hadithsData.pages || 1
        });
      } catch (error) {
        console.error('Error fetching chapter:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchChapterData();
  }, [chapterId, pagination.page, pagination.limit]);

  const handlePageChange = (newPage) => {
    setPagination(prev => ({ ...prev, page: newPage }));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!chapter) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <p className="text-gray-600">{t('notFound')}</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Chapter Header */}
      <div className="bg-white rounded-xl shadow-md p-6 mb-8">
        <div className="flex items-center mb-4">
          <Link to={`/books/${chapter.book_id}`} className="text-primary-600 hover:text-primary-700 ml-4">
            <FaArrowRight />
          </Link>
          <FaFolder className="text-3xl text-primary-600 ml-3" />
          <div>
            <h1 className="text-3xl font-bold">{chapter.title_ar}</h1>
            <p className="text-gray-600 mt-1">
              {t('totalHadiths')}: {chapter.hadith_count}
            </p>
          </div>
        </div>
      </div>

      {/* Hadiths List */}
      <div className="space-y-4">
        {hadiths.map((hadith) => (
          <HadithCard key={hadith.id} hadith={hadith} />
        ))}
        
        <Pagination
          currentPage={pagination.page}
          totalPages={pagination.pages}
          onPageChange={handlePageChange}
        />
      </div>
    </div>
  );
};

export default ChapterPage; 
