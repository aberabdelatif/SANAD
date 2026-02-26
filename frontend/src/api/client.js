import axios from 'axios';

// استخدم URL الخاص بالاستضافة إذا لم يكن هناك متغير بيئي
const API = axios.create({
  baseURL: 'https://sanad-yq9s.onrender.com',
  timeout: 30000,
});

API.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error);
    throw error;
  }
);

export const api = {
  // الكتب
  getBooks: () => API.get('/books'),
  getBook: (id) => API.get(`/books/${id}`),

  // الأحاديث
  getAllHadiths: () => API.get('/hadiths'),
  getHadith: (id) => API.get(`/hadiths/${id}`),
  getHadithsByBook: (bookId) => API.get(`/hadiths/book/${bookId}`),

  // البحث
  searchSimple: (params) => {
    const queryParams = new URLSearchParams(params).toString();
    return API.get(`/search/simple?${queryParams}`);
  },

  advancedSearch: (params) => {
    const queryParams = new URLSearchParams(params).toString();
    return API.get(`/search?${queryParams}`);
  },

  getSuggestions: (q) => API.get(`/search/suggestions?q=${q}`),

  getFilterOptions: () => API.get('/search/filters'),

  // الإحصائيات
  getStats: () => API.get('/stats'),
};

export default API;

