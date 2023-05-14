document.addEventListener('DOMContentLoaded', () => {
    // if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    //     document.documentElement.classList.add('dark')
    //     toggleVisuals()
    // } else {
    //     document.documentElement.classList.remove('dark')
    //     toggleVisuals()
    // }
})

toggleDarkMode = () => {
    document.documentElement.classList.toggle('dark');
    if (document.documentElement.classList.contains('dark')) {
        localStorage.theme = 'dark'
    } else {
        localStorage.theme = 'light'
    }
    toggleVisuals()
}

toggleVisuals = () => {
    let toggle = document.getElementById('dark-mode-toggle');
    let dark = document.getElementById('dark-mode');
    let light = document.getElementById('light-mode');
    if (document.documentElement.classList.contains('dark')) {
        light.classList.remove('hidden');
        dark.classList.add('hidden');
        toggle.classList.remove('bg-gmt-pink')
        toggle.classList.add('bg-gmt-teal-secondary')
    } else {
        light.classList.add('hidden');
        dark.classList.remove('hidden');
        toggle.classList.remove('bg-gmt-teal-secondary')
        toggle.classList.add('bg-gmt-pink')
    }
}