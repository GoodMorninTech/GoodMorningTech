import json

import bs4
import feedparser
import requests


def get_posts(choice):
    """Get the posts from different RSS feeds."""
    with open("newspaper/rss.json") as f:
        rss = json.load(f)

    url = rss[choice]["url"]
    feed = feedparser.parse(url)

    return feed.entries


def convert_posts(posts, limit=10):
    """Convert the posts to a dict."""
    data = []
    for post in posts[:limit]:
        text = requests.get(post.link).text
        soup = bs4.BeautifulSoup(text, "html.parser")
        image = soup.find("meta", property="og:image")
        image = image["content"] if image else None

        data.append(
            {
                "title": post.title,
                "description": post.description,
                "url": post.link,
                "thumbnail": image,
            }
        )

    return data


def get_news(choice="BBC"):
    """Get the news."""
    posts = get_posts(choice)
    data = convert_posts(posts, 10)

    return data
