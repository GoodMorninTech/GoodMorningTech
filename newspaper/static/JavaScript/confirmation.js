const confirm_btn = document.querySelector('.confirmed');
const animation_container = document.querySelector('.animation-container');

//Upon clicking confirm_btn, the container will be removed from the DOM & the animation_container will be added to the DOM 
confirm_btn.addEventListener('click', () => {
    document.querySelector('.container').remove();
    animation_container.classList.remove('hidden');
    animation_container.classList.add('visible');
});