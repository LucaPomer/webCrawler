import functools
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_exponential
from typing import Dict, Callable, Set


def page_is_part_of_domain(original_page: str, new_url: str) -> bool:
    """checks weather the new link is part of the original domain"""
    domain = urlparse(original_page).netloc
    return domain in new_url


def desired_links(href: str) -> bool:
    """defines which href elements in the HTML content are wanted"""
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


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=60),
       retry=retry_if_exception_type(requests.ConnectionError))
def get_html_content(url: str) -> bytes:
    """sends a request to get the html"""
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


def get_all_sub_links(page_url: str, is_sub_page: Callable[[str], bool] = None, traversed_urls: Set[str] = None,
                      soups_to_url: Dict[BeautifulSoup, str] = None) -> Dict[BeautifulSoup, str]:
    """gets all sub links and their soup for a initial url"""
    # initializing variables for head of recursive function
    if soups_to_url is None:
        soups_to_url = dict()
    if is_sub_page is None:
        is_sub_page = functools.partial(page_is_part_of_domain, page_url)
    if traversed_urls is None:
        traversed_urls = {page_url}

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
