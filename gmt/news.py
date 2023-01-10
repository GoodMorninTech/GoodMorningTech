import json

import bs4
import feedparser
import requests


def get_posts(choice):
    """Get the posts from different RSS feeds."""
    # Read the JSON file to get the variables and URL of the RSS feed, it looks like this
    # load the JSON file in the Flask app
    with open("rss.json") as f:
        rss = json.load(f)

    # Get the URL of the RSS feed
    url = rss[choice]["url"]
    # Get the feed
    feed = feedparser.parse(url)

    return feed.entries


def convert_posts(posts, limit=10):
    """Convert the posts to a dict"""
    # Get the data from the posts
    data = []
    for post in posts[:limit]:
        # Get the image from the embedded image
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


def get_news(choice):
    """Get the news"""
    # Get the posts
    posts = get_posts(choice)
    # Convert the posts to a dict
    data = convert_posts(posts, 10)
    return data
