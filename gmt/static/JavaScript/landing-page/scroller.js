const scroller = document.getElementById('scroller');
scroller.addEventListener('click', () => {
   window.scrollTo({
      top: document.getElementById('what-do-we-offer').offsetTop,
      behavior: 'smooth'
   });
});

scroller.addEventListener('mouseover', () => {
   scroller.style.cursor = 'pointer';
});