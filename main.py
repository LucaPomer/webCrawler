# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import re

import requests
from bs4 import BeautifulSoup

# main_site =  "https://www.spree-liebe.de/hochzeitsfotograf-berlin-empfehlung/weddyplace/"
main_site = "http://www.andreaslemke.com/"
## {"src": "https://cdn.weddyplace.com/static/misc/badges/badge-gelistet.png"}


def find_tag_in_content(soup):
    # print(soup.children)
    # print(soup.prettify())
    all_p_tags = soup.find_all('a', href=re.compile('^https://www.weddyplace.com/vendors/'))
    for element in all_p_tags:
        print(element)
        ## todo: check if the source is the same



def page_is_sub_page(original_page, new_url):
    splitted_og_page = original_page.split('/')
    domain = splitted_og_page[2]
    if domain in new_url: ## todo: add checking if the new url is just a /something
        return True
    else:
        return False

def get_links(page_url, pages, start_page):
    html = requests.get(page_url)  # fstrings require Python 3.6+
    soup = BeautifulSoup(html.content, 'html.parser')
    # print(soup.prettify())
    # print(soup.findAll('a', href=True))
    for link in soup.find_all("a", href=True):
        new_link = link['href']
        if new_link not in pages and page_is_sub_page(start_page, new_link):
            print(new_link)
            pages.add(new_link)
            find_tag_in_content(soup)
            get_links(new_link,pages, start_page)

    return pages



# find_tag_in_content(page_soup, 'p')
all_sub_links = get_links(main_site, set(), main_site)
# print(all_sub_links)

