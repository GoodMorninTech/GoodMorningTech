import json

import bs4
import requests


def get_posts():
    """Get the posts from The Verge Tech"""
    res = requests.get("https://www.theverge.com/tech")
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    # Removes everything and only keeps the JSON data
    soup = soup.find("script", {"id": "__NEXT_DATA__"}).string
    soup = soup.split('{"props":{"pageProps":{"initialState":')[0]
    soup = soup.split(',"pageProps":')[0]

    # Parse the JSON
    soup = json.loads(soup)

    # Get the posts
    posts = soup["props"]["pageProps"]["hydration"]["responses"][0]["data"]["entity"][
        "hubPage"
    ]["placements"]
    print("Posts retrieved")
    return posts


def get_count(posts):
    """Get the number of posts"""
    numbers = 0
    for post in posts:
        numbers += 1
        try:
            post["placeable"]["title"][numbers]
        except IndexError:
            break
        except KeyError:
            numbers -= 1
            break
    print("Number of posts retrieved")
    return numbers


def save_to_html():
    """Send the newspaper to the user"""
    # Get the posts
    print("Sending newspaper")
    with open("temp.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        # Set up an HTML file to send to the user
        with open("templates/newspaper.html", "w", encoding="utf-8") as f:
            f.write(
                '<!DOCTYPE html> <html lang="en"> <head> <title>The Tech Morning Newspaper</title> <link '
                'href="https://fonts.gstatic.com" rel="preconnect"/> <link '
                'href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;600&display=swap" '
                'rel="stylesheet"/> <style> body { margin: 0; } td, p { font-size: 13px; color: #878787; } ul { '
                "margin: 0 0 10px 25px; padding: 0; } li { margin: 0 0 3px 0; } h1, h2 { color: black; } h1 { "
                "font-size: 25px; } h2 { font-size: 20px; } a { color: #2F82DE; font-weight: bold; text-decoration: "
                "none; } .entire-page { background: #C7C7C7; width: 100%; padding: 20px 0; font-family: Lucida "
                "Grande, Lucida Sans Unicode, Verdana, sans-serif; line-height: 1.5; } .email-body { max-width: "
                "600px; min-width: 320px; margin: 0 auto; background: white; border-collapse: collapse; } img { "
                "max-width: 100%; } .email-header { background: black; padding: 30px; } .news-section { padding: 20px "
                "30px; } .footer { background: #eee; padding: 10px; font-size: 10px; text-align: center; } </style> "
                '</head> <table class="entire-page"> <tr> <td> <table class="email-body"> <tr> <td '
                'class="email-header"> <a> <h1 style="color:white;">The Tech Morning Newspaper</h1> </a> </td> </tr> '
                '<tr> <td class="news-section"> <h2>Good morning</h2> <p>We are a new open source newspaper, '
                "and we want feedback. Reply to this email with your opinion about this mail, so we can improve! "
                "Happy reading! "
                "</p> <ul>"
            )
            for post in data:
                f.write(
                    f' <tr> <td class="news-section"> <h1>{post["title"]}</h1> <a><img src="{post["thumbnail"]}"></a> '
                    f'<p>{post["description"]}</p> <p><a href="{post["url"]}">Read Now &rarr;</a></p> </td> </tr>'
                )
            f.write(
                '<tr> <td class="footer"> You are receiving this email because you subscribed to The Tech Morning '
                'Newspaper. You can <a href="TODO: Add unsubscribe">instantly opt out</a> any time. </td> </tr> '
                "</table> </td> </tr> </table>"
            )
            f.close()
        print("Newspaper sent")


def save_posts():
    """Saves Posts to a JSON file and a HTML file"""
    # Get the posts
    posts = get_posts()
    # Get the number of posts
    numbers = get_count(posts)
    # Get the data from the posts
    data = []
    for i in range(numbers):
        if (
            posts[i]["placeable"]["title"] is not None
            and len(posts[i]["placeable"]["title"]) > 5
        ):
            try:
                thumbnail = posts[i]["placeable"]["leadComponent"]["standard"]["url"]
                description = posts[i]["placeable"]["dek"]["html"]
            except:
                continue
            data.append(
                {
                    "title": posts[i]["placeable"]["title"],
                    "description": description,
                    "author": posts[i]["placeable"]["author"],
                    "url": posts[i]["placeable"]["url"],
                    "thumbnail": thumbnail,
                }
            )

    # with open('temp.json', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, indent=4)
    #     f.close()
    #
    # # Save it also in case it is duplicated
    # with open('posts.json', 'a', encoding='utf-8') as f:
    #     print('Saving posts')
    #     json.dump(data, f, indent=4)
    #     f.close()

    return data
