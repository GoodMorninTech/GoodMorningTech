import json

import re
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
    print(feed.entries)

    return feed.entries


def convert_posts(posts, source, limit=8):
    """Convert the posts to a dict"""
    # Get the data from the posts
    data = []
    for post in posts[:limit]:
        link = re.sub(r"[^\x00-\x7F]+", "", post.link)
        raw = requests.get(f"https://parser.goodmorningtech.news/parse?url={link}")
        try:
            raw = raw.json()
        except json.decoder.JSONDecodeError:
            continue
        image = raw["lead_image_url"]
        title = raw["title"]
        description = raw["content"]
        date = raw["date_published"]
        author = raw["author"]

        # Check if the post is from today UTC, the date is in YYYY-MM-DDTHH:MM:SS.000Z format
        from datetime import datetime
        from time import sleep

        if not date or date[:10] == datetime.utcnow().strftime("%Y-%m-%d"):
            data.append(
                {
                    "title": title,
                    "description": description,
                    "url": post.link,
                    "thumbnail": image,
                    "author": author,
                    "source": source,
                }
            )
        else:
            continue
        sleep(1)

    return data


def get_news(choice, limit=8):
    """Get the news"""
    # Get the posts
    posts = get_posts(choice)
    # Convert the posts to a dict
    data = convert_posts(posts, source=choice, limit=limit)
    return data
