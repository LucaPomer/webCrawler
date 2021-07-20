import functools
import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from helpers.data_writer import write_multiple_lines, write_data
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type, wait_exponential


class NoBadgeFoundError(Exception):
    """Raised when there is no badge found"""
    pass


###
# checks weather the content contains the badge tag
# input: soup - BeautifulSoup, href_regex - regex
# output: [badge_tag - string, image_src - string]
###
def find_badge_in_content(soup, href_regex):
    badge_tag = soup.find('a', href=href_regex)
    if badge_tag is None:
        raise NoBadgeFoundError()
    img = badge_tag.find('img')
    image_src = img['data-src']
    return [badge_tag['href'], image_src]


###
# checks weather the new link is part of the original domain
# input: original_page - string, new_url - string
# output: boolean
###
def page_is_part_of_domain(original_page, new_url):
    domain = urlparse(original_page).netloc
    return domain in new_url


###
# defines which href elements in the HTML content are desired
# input: href-string
# output: boolean
###
def desired_links(href):
    parsed = urlparse(href)
    # ignore if href is not set
    if not href:
        return False

    # ignore if it is just a link to the same page
    if href.startswith("#"):
        return False

    # ignore if it does not contain a proper protocol (http/https)
    if not bool(parsed.scheme):
        return False

    return True


###
# sends a request to get the html
# input: url-string
# output: html.content
###
@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=60),
       retry=retry_if_exception_type(requests.ConnectionError))
def get_html_content(url):
    try:
        html = requests.get(url, timeout=10)
        return html.content

    except requests.ConnectionError as e:
        print(
            "OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
        raise
    except requests.Timeout as e:
        print("OOPS!! Timeout Error")
        print(str(e))
        raise
    except requests.exceptions.MissingSchema as e:
        print(f'Wrong URL schema: {url}')
        raise
    except requests.RequestException as e:
        print("OOPS!! General Error")
        print(f"{url} content was not retrieved")
        print(str(e))
        raise


###
# gets all sub links and their soup for a url
# input: url-string
# output: soup to string dictionary
###
def get_all_sub_links(page_url, is_sub_page=None, traversed_urls=None, soups_to_url=None):
    # initializing variables for head of recursive function
    if soups_to_url is None:
        soups_to_url = dict()
    if is_sub_page is None:
        is_sub_page = functools.partial(page_is_part_of_domain, page_url)
    if traversed_urls is None:
        traversed_urls = set()

    try:
        html_content = get_html_content(page_url)

    except requests.exceptions as e:
        print("there was an error, crawling stopped")
        print(str(e))
        return soups_to_url

    soup = BeautifulSoup(html_content, 'html.parser')
    soups_to_url[soup] = page_url
    for link in soup.find_all("a", href=desired_links):
        new_link = link['href']
        # link was already traversed or is not part of domain
        if new_link in traversed_urls or not is_sub_page(new_link):
            continue
        traversed_urls.add(new_link)
        get_all_sub_links(new_link, is_sub_page, traversed_urls, soups_to_url)

    return soups_to_url


###
# delegates the searching of the badges and prints the result
# input: page_soups_to_url-dictionary, badge_tag_regex-regex, csv_file_path-string
# output: none
###
def search_and_write_badges(page_soups_to_url, badge_tag_regex, csv_file_path):
    all_badges = get_badges(page_soups_to_url, badge_tag_regex)
    write_multiple_lines(all_badges, csv_file_path)
    write_data(['Found Badges ', str(len(all_badges))], csv_file_path)


###
# goes over all pages and searches for the badge
# input: page_soups_to_url-dictionary, badge_tag_regex-regex
# output: an array of string arrays
###
def get_badges(page_soups_to_url, badge_tag_regex):
    all_badges = []
    for soup, url in page_soups_to_url.items():
        try:
            found_badge = find_badge_in_content(soup, badge_tag_regex)
            found_badge.append(url)
            all_badges.append(found_badge)
        except NoBadgeFoundError:
            continue
    return all_badges
