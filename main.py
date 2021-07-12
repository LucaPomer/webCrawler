# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup

## {"src": "https://cdn.weddyplace.com/static/misc/badges/badge-gelistet.png"}

def get_website_content(url):
    page = requests.get(url)
    print(page.status_code)
    # print(page.content)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup
    # print(soup.prettify())


def find_tag_in_content(soup, tag):
    # print(soup.children)
    # print(soup.prettify())
    # all_p_tags = soup.find_all(tag)
    # print(all_p_tags)
    # print(all_p_tags[0].get_text())
    weddy_badge = soup.findAll("link")
    print(weddy_badge)


page_soup: BeautifulSoup = get_website_content(
    "https://www.spree-liebe.de/hochzeitsfotograf-berlin-empfehlung/weddyplace/")

find_tag_in_content(page_soup, 'p')

