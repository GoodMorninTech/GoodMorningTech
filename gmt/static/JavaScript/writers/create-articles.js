const checkbox = document.getElementById('is_published');
const submitBtn = document.getElementById('submit-btn');
checkbox.addEventListener('change', (event) => {
    if (event.target.checked) {
        submitBtn.disabled = false;
    } else {
        submitBtn.disabled = true;
    }
});
const preview = document.getElementById('wmd-preview');
const input = document.getElementById('wmd-input');

preview.addEventListener('DOMSubtreeModified', () => {
    if (preview.offsetHeight > 300) {
        input.style.height = preview.offsetHeight + 'px';
    }
});

input.addEventListener('input', () => {
    if (input.value == '') {
        input.style.height = '300px';
    }
});

const iconPackSpan =  document.querySelector('.wmd-button > span')
// on load function
// window.onload = function() {
//     iconPackSpan.style.backgroundImage = "url('https://cdn.goodmorningtech.news/website/writers/iconpack.png')"
//     iconPackSpan.style.backgroundrepeat = 'no-repeat'
//     iconPackSpan.style.backgroundSize = '20px 20px'
//     iconPackSpan.style.backgroundPosition = 'center'
//     iconPackSpan.style.display = 'inline-block'
// }
// @LevaniVashadze Could you please fix this? I don't know how to do it.    Thanks


// Flares:

// const gadget_news = document.getElementById('gadget-news');
// const gadget_news_add = document.getElementById('gadget-news-add');
// const ai_news = document.getElementById('ai-news');
// const ai_news_add = document.getElementById('ai-news-add');
// const robot_news = document.getElementById('robotics-news');
// const robot_news_add = document.getElementById('robotics-news-add');
// const crypto_news = document.getElementById('crypto-news');
// const crypto_news_add = document.getElementById('crypto-news-add');
// const corporation_news = document.getElementById('corporation-news');
// const corporation_news_add = document.getElementById('corporation-news-add');
// const gaming_news = document.getElementById('gaming-news');
// const gaming_news_add = document.getElementById('gaming-news-add');
// const science_news = document.getElementById('science-news');
// const science_news_add = document.getElementById('science-news-add');
// const space_news = document.getElementById('space-news');
// const space_news_add = document.getElementById('space-news-add');
// const other_news = document.getElementById('other-news');
// const other_news_add = document.getElementById('other-news-add');

// const selected_flare_container = document.getElementById('flare-container');
