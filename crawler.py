import functools
import re
import requests
from bs4 import BeautifulSoup
from helpers.data_writer import write_multiple_lines, write_data
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type, wait_exponential


class NoBadgeFoundError(Exception):
    """Raised when there is no badge found"""
    pass


def find_badge_in_content(soup):
    badge_tag = soup.find('a', href=re.compile('^https://www.weddyplace.com/vendors/'))
    if badge_tag is None:
        raise NoBadgeFoundError
    badge_element = []
    img = badge_tag.find('img')
    image_src = img['data-src']
    badge_element.append(badge_tag['href'])
    badge_element.append(image_src)
    return badge_element


def page_is_sub_page(original_page, new_url):  # todo: find a library that checks if is a sub library + add docs
    splitted_og_page = original_page.split('/')
    domain = splitted_og_page[2]
    if domain in new_url:
        return True
    else:
        return False


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=60),
       retry=retry_if_exception_type(requests.ConnectionError))
def get_all_sub_links(page_url, start_page=None, traversed_urls=None, soups_to_url=None):
    # initializing variables for head of recursive function
    global is_sub_page
    if soups_to_url is None:
        soups_to_url = dict()
    if start_page is None:
        start_page = page_url
        is_sub_page = functools.partial(page_is_sub_page, page_url)
    if traversed_urls is None:
        traversed_urls = set()

    try:
        html = requests.get(page_url, timeout=10)
        soup = BeautifulSoup(html.content, 'html.parser')
        soups_to_url[soup] = page_url
        for link in soup.find_all("a", href=True):
            new_link = link['href']
            # link was already traversed
            if new_link in traversed_urls:
                continue
            # link is not part of domain
            if not is_sub_page(new_link):
                continue

            traversed_urls.add(new_link)
            get_all_sub_links(new_link, start_page, traversed_urls, soups_to_url)

    except requests.ConnectionError as e:
        print(
            "OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
        raise
    except requests.Timeout as e:
        print("OOPS!! Timeout Error")
        print(str(e))
    except requests.exceptions.MissingSchema as e:
        print('Wrong URL scema: URL = ' + str(page_url))
    except requests.RequestException as e:
        print("OOPS!! General Error")
        print(page_url + " was not successful")
        print(str(e))

    return soups_to_url


def search_and_write_badges(page_soupes_to_url, csv_file_path):
    num_badges = 0
    for elem in page_soupes_to_url:
        soup = elem[0]
        url = elem[1]
        found_badge = find_badge_in_content(soup)
        if found_badge:
            num_badges += 1
            found_badge.append(url)
            write_data(found_badge, csv_file_path)
    write_data(['Found Badges ', str(num_badges)], csv_file_path)
