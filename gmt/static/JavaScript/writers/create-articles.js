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
    }, 1000)
});

toggleCategory = (category) => {
    const element = document.getElementById(category);
    const cross = element.parentElement.getElementsByClassName('fas ml-2')[0]
    if (cross.classList.contains('fa-plus')) {
        if (categories === maxCategories) {
            element.checked = false;
            alert('You can only add 3 categories to an article. To add more remove other ones.');
            return;
        } else {
            categories++;
        }
    } else {
        categories--;
    }
    element.parentElement.classList.toggle('border-[1px]');
    element.parentElement.classList.toggle('border-[2px]');
    element.parentElement.classList.toggle('shadow-lg');
    element.parentElement.classList.toggle('border-black');

    // gets text-somecolor-800 class from parent and adds a border with that color
    const color = element.parentElement.classList.toString().split(' ').filter((item) => item.includes('text-')).filter((item) => item.includes('-800'))[0].split('text-')[1];
    element.parentElement.classList.toggle(`border-${color}`);

    cross.classList.toggle('fa-plus');
    cross.classList.toggle('fa-xmark');
}

const categoryList = document.getElementById('category-list');
const maxCategories = 3;
let categories = 0;
