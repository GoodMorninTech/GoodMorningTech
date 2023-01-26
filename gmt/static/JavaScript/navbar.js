const button = document.querySelector('#hamburger-menu');
const menu = document.querySelector('#navigation-items');

button.addEventListener('click', () => {
menu.classList.toggle('hidden');
});


document.addEventListener('DOMContentLoaded', () => {
    const navbarItem = document.getElementById(document.title);
    if (navbarItem) {
        navbarItem.classList.add('md:border-t-gmt-red-primary', 'md:border-b-0');
        navbarItem.classList.remove('md:border-t-gmt-navbar-bg');
    }
})