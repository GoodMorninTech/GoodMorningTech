import bs4


def filter_articles(raw_html: str) -> str:
    """Filters HTML out, which is not enclosed by article-tags.
    Beautifulsoup is inaccurate and slow when applied on a larger
    HTML string, this filtration fixes this.
    """
    raw_html_lst = raw_html.split("\n")

    # count number of article tags within the document (varies from 0 to 50):
    article_tags_count = 0
    tag = "article"
    for line in raw_html_lst:
        if tag in line:
            article_tags_count += 1

    # copy HTML enclosed by first and last article-tag:
    articles_arrays, is_article = [], False
    for line in raw_html_lst:
        if tag in line:
            article_tags_count -= 1
            is_article = True
        if is_article:
            articles_arrays.append(line)
        if not article_tags_count:
            is_article = False
    return "".join(articles_arrays)


def make_soup(articles_html: str) -> bs4.element.ResultSet:
    """HTML enclosed by article-tags is converted into a
    soup for further data extraction.
    """
    soup = bs4.BeautifulSoup(articles_html, "lxml")
    return soup.find_all("article", class_="Box-row")


def scraping_repositories(
    matches: bs4.element.ResultSet,
    since: str,
):
    """Data about all trending repositories are extracted."""
    trending_repositories = []
    for rank, match in enumerate(matches):

        # description
        if match.p:
            description = match.p.get_text(strip=True)
        else:
            description = None

        # relative url
        rel_url = match.h1.a["href"]

        # absolute url:
        repo_url = "https://github.com" + rel_url

        # name of repo
        repository_name = rel_url.split("/")[-1]

        # author (username):
        username = rel_url.split("/")[-2]

        # language and color
        progr_language = match.find("span", itemprop="programmingLanguage")
        if progr_language:
            language = progr_language.get_text(strip=True)
            lang_color_tag = match.find("span", class_="repo-language-color")
            lang_color = lang_color_tag["style"].split()[-1]
        else:
            lang_color, language = None, None

        stars_built_section = match.div.findNextSibling("div")

        # total stars:
        if stars_built_section.a:
            raw_total_stars = stars_built_section.a.get_text(strip=True)
            if "," in raw_total_stars:
                raw_total_stars = raw_total_stars.replace(",", "")
        if raw_total_stars:
            total_stars: int
            try:
                total_stars = int(raw_total_stars)
            except ValueError as missing_number:
                print(missing_number)
        else:
            total_stars = None

        # forks
        if stars_built_section.a.findNextSibling("a"):
            raw_forks = stars_built_section.a.findNextSibling(
                "a",
            ).get_text(strip=True)
            if "," in raw_forks:
                raw_forks = raw_forks.replace(",", "")
        if raw_forks:
            forks: int
            try:
                forks = int(raw_forks)
            except ValueError as missing_number:
                print(missing_number)
        else:
            forks = None

        # stars in period
        if stars_built_section.find(
            "span",
            class_="d-inline-block float-sm-right",
        ):
            raw_stars_since = (
                stars_built_section.find(
                    "span",
                    class_="d-inline-block float-sm-right",
                )
                .get_text(strip=True)
                .split()[0]
            )
            if "," in raw_stars_since:
                raw_stars_since = raw_stars_since.replace(",", "")
        if raw_stars_since:
            stars_since: int
            try:
                stars_since = int(raw_stars_since)
            except ValueError as missing_number:
                print(missing_number)
        else:
            stars_since = None

        # builtby
        built_section = stars_built_section.find(
            "span",
            class_="d-inline-block mr-3",
        )
        if built_section:
            contributors = stars_built_section.find(
                "span",
                class_="d-inline-block mr-3",
            ).find_all("a")
            built_by = []
            for contributor in contributors:
                contr_data = {}
                contr_data["username"] = contributor["href"].strip("/")
                contr_data["url"] = "https://github.com" + contributor["href"]
                contr_data["avatar"] = contributor.img["src"]
                built_by.append(dict(contr_data))

        repositories = {
            "rank": rank + 1,
            "username": username,
            "repositoryName": repository_name,
            "whole_name": username + "/" + repository_name,
            "url": repo_url,
            "description": description,
            "language": language,
            "languageColor": lang_color,
            "totalStars": total_stars,
            "forks": forks,
            "starsSince": stars_since,
            "since": since,
            # "builtBy": built_by, ## Not needed for now
        }
        trending_repositories.append(repositories)
    return trending_repositories
