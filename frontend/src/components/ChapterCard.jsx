import React from 'react';
import { Link } from 'react-router-dom';
import { FaFolder, FaList } from 'react-icons/fa'; // تغيير FaHadith إلى FaList
import { useLanguage } from '../context/LanguageContext';

const ChapterCard = ({ chapter }) => {
  const { t } = useLanguage();
  
  return (
    <Link to={`/chapters/${chapter.id}`}>
      <div className="bg-white rounded-lg shadow hover:shadow-md transition-shadow p-4 border border-gray-100">
        <div className="flex items-center space-x-3 rtl:space-x-reverse">
          <FaFolder className="text-primary-400 text-xl" />
          <div className="flex-1">
            <h4 className="font-semibold text-gray-800">{chapter.title_ar}</h4>
            <div className="flex items-center mt-1 text-sm text-gray-500">
              <FaList className="ml-1 rtl:mr-1" /> {/* تغيير FaHadith إلى FaList */}
              <span>{chapter.hadith_count} {t('hadiths')}</span>
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default ChapterCard;