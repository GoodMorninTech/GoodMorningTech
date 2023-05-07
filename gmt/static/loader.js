const loader = document.querySelector('#loader-wrapper');
const isReduced = window.matchMedia(`(prefers-reduced-motion: reduce)`) === true || window.matchMedia(`(prefers-reduced-motion: reduce)`).matches === true;

if (!isReduced) {
    setTimeout(() => {
   loader.style.opacity = 0;
   loader.style.display = 'none';
}, 3000);
} else {
    loader.style.display = 'none';
}

