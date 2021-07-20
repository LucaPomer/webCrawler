import re

import requests

from crawler import get_all_sub_links, search_and_write_badges


def main():
    site_to_crawl = "https://www.spree-liebe.de/hochzeitsfotograf-berlin-empfehlung/weddyplace/"
    result_csv = 'result_files/result.csv'
    try:
        soup_to_url_for_all_sub_pages = get_all_sub_links(site_to_crawl)
        search_and_write_badges(soup_to_url_for_all_sub_pages, re.compile('^https://www.weddyplace.com/vendors/'),
                                result_csv)
    except requests.ConnectionError as e:
        print("crawling not possible due to a connection error, please try again later")
        print(e)


if __name__ == "__main__":
    main()
