import React from 'react';
import { FaChevronRight, FaChevronLeft } from 'react-icons/fa';
import { useLanguage } from '../context/LanguageContext';

const Pagination = ({ currentPage, totalPages, onPageChange }) => {
  const { t, dir } = useLanguage();
  
  const getPageNumbers = () => {
    const delta = 2;
    const range = [];
    const rangeWithDots = [];
    let l;

    for (let i = 1; i <= totalPages; i++) {
      if (i === 1 || i === totalPages || (i >= currentPage - delta && i <= currentPage + delta)) {
        range.push(i);
      }
    }

    range.forEach((i) => {
      if (l) {
        if (i - l === 2) {
          rangeWithDots.push(l + 1);
        } else if (i - l !== 1) {
          rangeWithDots.push('...');
        }
      }
      rangeWithDots.push(i);
      l = i;
    });

    return rangeWithDots;
  };

  if (totalPages <= 1) return null;

  return (
    <div className="flex items-center justify-center space-x-2 rtl:space-x-reverse mt-8">
      {/* Previous Button */}
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className={`p-2 rounded-lg ${
          currentPage === 1
            ? 'text-gray-300 cursor-not-allowed'
            : 'text-primary-600 hover:bg-primary-50'
        }`}
      >
        {dir === 'rtl' ? <FaChevronRight /> : <FaChevronLeft />}
      </button>

      {/* Page Numbers */}
      {getPageNumbers().map((page, index) => (
        <button
          key={index}
          onClick={() => typeof page === 'number' && onPageChange(page)}
          className={`px-4 py-2 rounded-lg ${
            page === currentPage
              ? 'bg-primary-600 text-white'
              : page === '...'
              ? 'cursor-default'
              : 'text-gray-600 hover:bg-primary-50'
          }`}
        >
          {page}
        </button>
      ))}

      {/* Next Button */}
      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className={`p-2 rounded-lg ${
          currentPage === totalPages
            ? 'text-gray-300 cursor-not-allowed'
            : 'text-primary-600 hover:bg-primary-50'
        }`}
      >
        {dir === 'rtl' ? <FaChevronLeft /> : <FaChevronRight />}
      </button>
    </div>
  );
};

export default Pagination; 
