/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./gmt/**/*.{html,js}",
    ],
    theme: {
        fontFamily: {
            'gmt-fira': ['Fira Sans', 'sans-serif'],
            'gmt-karla': ['Karla', 'sans-serif'],
            'gmt-anonymous-pro': ['Anonymous Pro', 'monospace'],
            'gmt-open-sans': ['Open Sans', 'sans-serif'],
        },
        extend: {
            colors: {
                'gmt-red-primary': '#CF3333',
                'gmt-red-secondary': '#D02B2B',
                'gmt-pink': '#FE7C84',
                'gmt-black-primary': '#272727',
                'gmt-yellow-primary': '#FFD037',
                'gmt-teal-primary': '#1FC59D',
                'gmt-teal-secondary': '#4A686C',
                'gmt-gray-primary': '#646464',
                'gmt-gray-secondary': '#CCCCCC',
                'gmt-bg': '#F6F4F0',
                'gmt-dark-bg': '#131313',
                'gmt-bg-secondary': '#EBE9E4',
                'gmt-dark-bg-secondary': '#333333',
                'gmt-selected-navbar': '#E6E6E6',
                'gmt-navbar-bg': '#F6F4F0',
                'discord': '#5869E9',
            },
            spacing: {
                'gmt-112': '28rem',
                'gmt-card': '40rem',
                'gmt-128': '42rem',
                'gmt-144': '56rem',
            },
            screens: {
                '3xl': '1920px',
            },
            backgroundImage: {
                'contactPageBg': "url('https://cdn.goodmorningtech.news/website/contact/backgroundImageContactPage.png')",
            }
        },
    },
    darkMode: 'class',
    plugins: [
        require('@tailwindcss/typography'),
    ],
}