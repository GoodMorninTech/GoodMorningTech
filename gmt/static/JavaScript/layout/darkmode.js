let toggle = null
let dark = null
let light = null

document.addEventListener('DOMContentLoaded', () => {
    toggle = document.getElementById('dark-mode-toggle');
    dark = document.getElementById('dark');
    light = document.getElementById('light');
})


toggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    if (document.body.classList.contains('dark')) {
        localStorage.setItem('dark-mode', 'enabled');
        dark.classList.remove('hidden');
        light.classList.add('hidden');
    }
})