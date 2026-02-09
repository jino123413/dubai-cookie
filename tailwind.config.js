/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{ts,tsx}', './index.html'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#8B6914',
          light: '#B8901A',
          dark: '#5C4610',
        },
        accent: {
          DEFAULT: '#D4A574',
          light: '#F0DCC8',
        },
        bg: {
          DEFAULT: '#FFF8F0',
          card: '#FFFFFF',
        },
        surface: {
          DEFAULT: '#FEF0E1',
          light: '#FFF5EB',
        },
      },
      fontFamily: {
        jalnan: ['Jalnan2', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
