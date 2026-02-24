/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f5f0',
          100: '#dae6da',
          200: '#b5cdb5',
          300: '#8fb48f',
          400: '#6a9b6a',
          500: '#4A7A4A', // لون أخضر إسلامي أنيق
          600: '#3b623b',
          700: '#2c492c',
          800: '#1e311e',
          900: '#0f180f',
        },
        secondary: {
          50: '#f5f0f0',
          100: '#e6dada',
          200: '#cdb5b5',
          300: '#b48f8f',
          400: '#9b6a6a',
          500: '#7A4A4A', // لون بني محايد
          600: '#623b3b',
          700: '#492c2c',
          800: '#311e1e',
          900: '#180f0f',
        },
        accent: {
          500: '#C9A959', // لون ذهبي للتميز
        },
        dark: '#1E2A3A',
        light: '#F8F9FA',
      },
      fontFamily: {
        'arabic': ['"Amiri"', '"Traditional Arabic"', 'serif'],
        'sans': ['"Inter"', 'system-ui', 'sans-serif'],
        'title': ['"Poppins"', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-slow': 'pulse 3s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'islamic-pattern': "url('/src/assets/islamic-pattern.svg')",
      },
    },
  },
  plugins: [],
}