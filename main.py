import bs4
import requests
import json


def get_posts():
    """ Get the posts from The Verge Tech"""
    res = requests.get('https://www.theverge.com/tech')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Removes everything and only keeps the JSON data
    soup = soup.find('script', {'id': '__NEXT_DATA__'}).string
    soup = soup.split('{"props":{"pageProps":{"initialState":')[0]
    soup = soup.split(',"pageProps":')[0]

    # Parse the JSON
    soup = json.loads(soup)

    # Get the posts
    posts = soup['props']['pageProps']['hydration']['responses'][0]['data']['entity']['hubPage']['placements']
    print('Posts retrieved')
    return posts


def get_count(posts):
    """ Get the number of posts """
    numbers = 0
    for post in posts:
        numbers += 1
        try:
            post['placeable']['title'][numbers]
        except IndexError:
            break
        except KeyError:
            numbers -= 1
            break
    print('Number of posts retrieved')
    return numbers


def main():
    """ Main function """
    # Get the posts
    posts = get_posts()
    # Get the number of posts
    numbers = get_count(posts)
    # Get the data from the posts
    data = []
    for i in range(numbers):
        if posts[i]['placeable']['title'] is not None and len(posts[i]['placeable']['title']) > 5:
            try:
                thumbnail = posts[i]['placeable']['leadComponent']['standard']['url']
                description = posts[i]['placeable']['dek']['html']
            except:
                thumbnail = None
                description = None
            data.append({'title': posts[i]['placeable']['title'],
                         'description': description,
                         'author': posts[i]['placeable']['author'],
                         'url': posts[i]['placeable']['url'],
                         'thumbnail': thumbnail})

    with open('temp.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        f.close()

    # Save it also in case it is duplicated
    with open('posts.json', 'a', encoding='utf-8') as f:
        print('Saving posts')
        json.dump(data, f, indent=4)
        f.close()

    # Send the newspaper to the user
    send_newspaper()


def send_newspaper():
    """ Send the newspaper to the user """
    # Get the posts
    print('Sending newspaper')
    with open('temp.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Set up an HTML file to send to the user
        with open('newspaper.html', 'w', encoding='utf-8') as f:
            f.write('<html><head><title>News</title></head><body>')
            # Give the page some CSS
            f.write(
                '<style>body {background-color: #000000; color: #ffffff; font-family: Arial, Helvetica, sans-serif; '
                'font-size: 20px;}</style>')
            for post in data:
                f.write(f'<h1>{post["title"]}</h1>')
                f.write(f'<p>By {post["author"]["fullName"]}</p>')
                f.write(f'<p>{post["description"]}</p>')
                f.write(f'<a href="{post["url"]}">Read more</a>')
                if post['thumbnail'] is not None:
                    f.write(f'<img src="{post["thumbnail"]}">')
            f.write('</body></html>')
            f.close()
        print('Newspaper sent')


if __name__ == '__main__':
    main()
