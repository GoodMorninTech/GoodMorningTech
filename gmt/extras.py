import bs4
import requests
from .utils import format_html


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

        # relative url:
        rel_url = match.select_one("h2 > a")["href"]

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
            "name": repository_name,
            "whole_name": username + "/" + repository_name,
            "url": repo_url,
            "description": description,
            "language": language,
            "language_color": lang_color,
            "total_stars": total_stars,
            "forks": forks,
            "stars_since": stars_since,
            "since": since,
            "built_by": built_by,
        }
        trending_repositories.append(repositories)

    return trending_repositories


def get_trending_repos(since="daily"):
    payload = {"since": since}  # "daily", "weekly", "monthly", "yearly"

    url = "https://github.com/trending"
    raw_html = requests.get(url, params=payload).text

    articles_html = filter_articles(raw_html)
    soup = make_soup(articles_html)
    trending_repos = scraping_repositories(soup, since=payload["since"])

    return trending_repos[:4]


def get_daily_coding_challenge():
    headers = {
        "Content-Type": "application/json",
    }

    json_data = {
        "query": "query questionOfToday {\n\tactiveDailyCodingChallengeQuestion {\n\t\tdate\n\t\tuserStatus\n\t\tlink\n\t\tquestion {\n\t\t\tacRate\n\t\t\tdifficulty\n\t\t\tfreqBar\n\t\t\tfrontendQuestionId: questionFrontendId\n\t\t\tisFavor\n\t\t\tpaidOnly: isPaidOnly\n\t\t\tstatus\n\t\t\ttitle\n\t\t\ttitleSlug\n\t\t\thasVideoSolution\n\t\t\thasSolution\n\t\t\ttopicTags {\n\t\t\t\tname\n\t\t\t\tid\n\t\t\t\tslug\n\t\t\t}\n\t\t}\n\t}\n}\n",
        "operationName": "questionOfToday",
    }

    response = requests.post(
        "https://leetcode.com/graphql", headers=headers, json=json_data
    )
    json_response = response.json()
    title_slug = json_response["data"]["activeDailyCodingChallengeQuestion"][
        "question"
    ]["titleSlug"]

    json_data = {
        "query": "\n    query questionContent($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    content\n    mysqlSchemas\n  }\n}\n    ",
        "variables": {"titleSlug": title_slug},
        "operationName": "questionContent",
    }

    response = requests.post(
        "https://leetcode.com/graphql", headers=headers, json=json_data
    )
    json_response = response.json()

    title = " ".join(word.capitalize() for word in title_slug.split("-"))
    raw_content = json_response["data"]["question"]["content"]
    description = format_html(raw_content)
    return {"title": title, "description": description}
