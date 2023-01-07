/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./newspaper/**/*.{html,js}"],
    theme: {
      fontFamily: {
        'gmt-fira': ['Fira Sans', 'sans-serif'],
        'gmt-karla': ['Karla', 'sans-serif'],
        'gmt-cormorant': ['Cormorant', 'serif'],
        'gmt-anonymous-pro': ['Anonymous Pro', 'monospace'],
        'gmt-open-sans': ['Open Sans', 'sans-serif'],
      },
      extend: {
        colors: {
          'gmt-red-primary': '#CF3333',
          'gmt-red-secondary': '#D02B2B',
          'gmt-black-primary': '#272727',
          'gmt-yellow-primary': '#FFD037',
          'gmt-teal-primary': '#1FC59D',
          'gmt-gray-primary': '#646464',
          'gmt-background': '#F6F4F0',
          'gmt-background-secondary': '#EBE9E4',
          'gmt-selected-navbar': '#E6E6E6'
        },
        spacing:  {
          'gmt-112': '28rem',
          'gmt-128': '42rem',
        }
      },
    },
    plugins: [],
  }