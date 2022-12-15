const button = document.querySelector('#hamburger-menu');
const menu = document.querySelector('#navigation-items');

button.addEventListener('click', () => {
menu.classList.toggle('hidden');
});

const subscribe = document.querySelector('#subscribe');
const heroSection = document.querySelector('#hero-section');