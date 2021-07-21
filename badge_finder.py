from re import Pattern
from typing import List, Dict

from bs4 import BeautifulSoup

from helpers.data_writer import write_multiple_lines, write_data


class NoBadgeFoundError(Exception):
    """Raised when there is no badge found"""
    pass


def find_badge_in_content(soup: BeautifulSoup, href_regex: Pattern) -> List[str]:
    """checks weather the content contains the badge tag"""
    badge_tag = soup.find('a', href=href_regex)
    if badge_tag is None:
        raise NoBadgeFoundError()
    img = badge_tag.find('img')
    image_src = img['data-src']
    return [badge_tag['href'], image_src]


def search_and_write_badges(page_soups_to_url: Dict[BeautifulSoup, str], badge_tag_regex: Pattern, csv_file_path: str):
    """delegates the searching of the badges and prints the result"""
    all_badges = get_badges(page_soups_to_url, badge_tag_regex)
    write_multiple_lines(all_badges, csv_file_path)
    write_data(['Found Badges ', str(len(all_badges))], csv_file_path)


def get_badges(page_soups_to_url: Dict[BeautifulSoup, str], badge_tag_regex: Pattern) -> List[List[str]]:
    """goes over all pages and searches for the badge"""
    all_badges = []
    for soup, url in page_soups_to_url.items():
        try:
            found_badge = find_badge_in_content(soup, badge_tag_regex)
            found_badge.append(url)
            all_badges.append(found_badge)
        except NoBadgeFoundError:
            continue
    return all_badges
