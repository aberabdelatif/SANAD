import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  FaSearch, 
  FaBook, 
  FaHome, 
  FaGlobe,
  FaBars,
  FaTimes,
  FaMosque,
  FaUser
} from 'react-icons/fa';
import { useLanguage } from '../context/LanguageContext';

const Navbar = () => {
  const { t, language, changeLanguage, dir } = useLanguage();
  const navigate = useNavigate();
  const [searchInput, setSearchInput] = useState('');
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  // تأثير التمرير
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchInput.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchInput)}`);
      setIsMenuOpen(false);
    }
  };

  const toggleLanguage = () => {
    changeLanguage(language === 'ar' ? 'en' : 'ar');
  };

  return (
    <nav className={`fixed top-0 w-full z-50 transition-all duration-300 ${
      isScrolled ? 'bg-white/95 backdrop-blur-md shadow-lg' : 'bg-white shadow-md'
    }`}>
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-20">
          {/* Logo مع تأثير */}
          <Link to="/" className="flex items-center group">
            <FaMosque className="text-3xl text-primary-600 group-hover:text-primary-700 transition-colors ml-2" />
            <span className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-accent-500 bg-clip-text text-transparent">
              {t('appName')}
            </span>
          </Link>

          {/* Search Bar (Desktop) - تصميم محسن */}
          <form onSubmit={handleSearch} className="hidden md:flex flex-1 max-w-xl mx-8">
            <div className="relative w-full group">
              <input
                type="text"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                placeholder={t('searchPlaceholder')}
                className="w-full px-6 py-3 pr-12 rounded-full border-2 border-gray-200 focus:border-primary-500 focus:outline-none transition-all group-hover:shadow-lg"
                dir={dir}
              />
              <button
                type="submit"
                className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-primary-600 transition-colors"
              >
                <FaSearch size={18} />
              </button>
            </div>
          </form>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6 rtl:space-x-reverse">
            <Link to="/" className="flex items-center text-gray-700 hover:text-primary-600 transition-colors">
              <FaHome className="ml-1 rtl:mr-1" />
              <span>{t('home')}</span>
            </Link>
            
            <Link to="/books" className="flex items-center text-gray-700 hover:text-primary-600 transition-colors">
              <FaBook className="ml-1 rtl:mr-1" />
              <span>{t('books')}</span>
            </Link>

            <button
              onClick={toggleLanguage}
              className="flex items-center px-4 py-2 bg-primary-50 text-primary-700 rounded-full hover:bg-primary-100 transition-colors"
            >
              <FaGlobe className="ml-1 rtl:mr-1" />
              <span>{language === 'ar' ? 'English' : 'العربية'}</span>
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            {isMenuOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 animate-slide-up">
            <form onSubmit={handleSearch} className="mb-4">
              <div className="relative">
                <input
                  type="text"
                  value={searchInput}
                  onChange={(e) => setSearchInput(e.target.value)}
                  placeholder={t('searchPlaceholder')}
                  className="w-full px-4 py-3 pr-10 rounded-lg border-2 border-gray-200 focus:border-primary-500 focus:outline-none"
                  dir={dir}
                  autoFocus
                />
                <button
                  type="submit"
                  className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
                >
                  <FaSearch />
                </button>
              </div>
            </form>

            <div className="space-y-2">
              <Link
                to="/"
                onClick={() => setIsMenuOpen(false)}
                className="flex items-center p-3 text-gray-700 hover:bg-primary-50 rounded-lg transition-colors"
              >
                <FaHome className="ml-2 rtl:mr-2" />
                <span>{t('home')}</span>
              </Link>
              
              <Link
                to="/books"
                onClick={() => setIsMenuOpen(false)}
                className="flex items-center p-3 text-gray-700 hover:bg-primary-50 rounded-lg transition-colors"
              >
                <FaBook className="ml-2 rtl:mr-2" />
                <span>{t('books')}</span>
              </Link>

              <button
                onClick={toggleLanguage}
                className="w-full flex items-center p-3 text-primary-700 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors"
              >
                <FaGlobe className="ml-2 rtl:mr-2" />
                <span>{language === 'ar' ? 'Switch to English' : 'التبديل إلى العربية'}</span>
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;