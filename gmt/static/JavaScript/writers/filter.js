document.addEventListener('DOMContentLoaded', () => {
    setFilter('newest')
})

setFilter = (filter) => {
    let articles = document.querySelectorAll('#articles')
    let articlesArray = Array.from(articles[0].children)
    let articlesSorted = articlesArray.sort((a, b) => {
        return b.querySelector('.article-date').querySelector('.publish-date').textContent.localeCompare(a.querySelector('.article-date').querySelector('.publish-date').textContent)
    })
    if (filter === 'oldest') {
        articlesSorted.reverse()
    } else if (filter === 'popularity') {
        articlesSorted.sort((a, b) => {
            return parseInt(b.querySelector('.views').textContent) - parseInt(a.querySelector('.views').textContent)
        })
    }
    articlesSorted.forEach(article => {
        articles[0].appendChild(article)
    })
}