# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import re

import requests
from bs4 import BeautifulSoup


## {"src": "https://cdn.weddyplace.com/static/misc/badges/badge-gelistet.png"}

def get_website_content(url):
    page = requests.get(url)
    print(page.status_code)
    # print(page.content)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_sub_sites = soup.findAll('a', href=True)
    # print(all_sub_sites)
    return soup
    # print(soup.prettify())


def find_tag_in_content(soup, tag):
    # print(soup.children)
    # print(soup.prettify())
    # all_p_tags = soup.find_all(tag)
    # print(all_p_tags)
    # print(all_p_tags[0].get_text())
    weddy_badge = soup.findAll("link")
    # print(weddy_badge)


def get_links(page_url, pages):
    # pages = set()
    # main_url = page_url.split('/')
    # main_page = "https://" + main_url[2]
    # print(main_page)
    pattern = re.compile("^(/)")
    html = requests.get(page_url)  # fstrings require Python 3.6+
    soup = BeautifulSoup(html.content, 'html.parser')
    # print(soup.prettify())
    # print(soup.findAll('a', href=True))
    for link in soup.find_all("a", href=True):
        new_link = link['href']
        print(new_link)
        if new_link not in pages and 'http' in new_link:
            pages.add(new_link)
            get_links(new_link,pages)

    print(pages)
        # href = link.attrs["href"]
        # print("link " + str(href))
        # if "href" in link.attrs:
        #     if main_page in href:
        #         new_page = href
        #         print("FOUND")
        #     else:
        #         new_page = main_page + link.attrs["href"]
        #     if new_page not in pages:
        #         print('new page ' + str(new_page))
        #         pages.add(new_page)
        #         print(pages)
        #         get_links(new_page, pages)


page_soup: BeautifulSoup = get_website_content(
    "https://www.spree-liebe.de/hochzeitsfotograf-berlin-empfehlung/weddyplace/")

find_tag_in_content(page_soup, 'p')
get_links("https://www.spree-liebe.de/hochzeitsfotograf-berlin-empfehlung/weddyplace/", set())
