const checkbox = document.getElementById('is_published');
const submitBtn = document.getElementById('submit-btn');
checkbox.addEventListener('change', (event) => {
    submitBtn.disabled = !event.target.checked;
});
const preview = document.getElementById('wmd-preview');
const input = document.getElementById('wmd-input');

preview.addEventListener('DOMSubtreeModified', () => {
    if (preview.offsetHeight > 300) {
        input.style.height = preview.offsetHeight + 'px';
    }
});

input.addEventListener('input', () => {
    if (input.value === '') {
        input.style.height = '300px';
    }
});

// on load function
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        // gets the ul element which contains li items with span children(the icons)
        const iconList = document.getElementById('wmd-button-row');
        for (let i = 0; i < iconList.children.length; i++) {
            // checks if the item is a button
            if (iconList.children[i].classList.contains('wmd-button'))
                // sets the background image of the span child
                iconList.children[i].children[0].style.backgroundImage = "url('https://cdn.goodmorningtech.news/website/writers/iconpack.png')";
        }
    })

})
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
