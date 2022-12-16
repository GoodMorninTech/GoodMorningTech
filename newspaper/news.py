import json

import bs4
import requests


def get_posts(choice):
    """Get the posts from different RSS feeds."""
    # Read the JSON file to get the variables and URL of the RSS feed, it looks like this
    # load the JSON file in the Flask app
    with open("newspaper/rss.json") as f:
        rss = json.load(f)

    # Get the URL of the RSS feed
    url = rss[0][choice]["url"]
    # Get the posts
    response = requests.get(url)
    # Convert the RSS feed to a dict
    posts = bs4.BeautifulSoup(response.text, "xml")
    # Get the posts
    posts = posts.find_all("item")
    return posts


def convert_posts(choice, posts):
    """Convert the posts to a dict"""
    # Get the number of posts
    numbers = 10
    # Get the data from the posts
    data = []
    for i in range(numbers):
        urlraw = requests.get(posts[i].link.text).text
        soup = bs4.BeautifulSoup(urlraw, "html.parser")
        # Get the image from the embedded image
        image = soup.find("meta", property="og:image")
        if image:
            image = image["content"]
        else:
            image = None
        data.append({"title": posts[i].title.text, "description": posts[i].description.text, "url": posts[i].link.text,
                     "thumbnail": image})

    return data


def get_news(choice):
    """Get the news"""
    # Get the posts
    posts = get_posts(choice)
    # Convert the posts to a dict
    data = convert_posts(choice, posts)
    return data
