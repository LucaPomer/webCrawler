import re
from badge_finder import search_and_write_badges
from crawler import get_all_sub_links


def main():
    site_to_crawl = "https://www.spree-liebe.de/hochzeitsfotograf-berlin-empfehlung/weddyplace/"
    result_csv = 'result_files/result.csv'
    soup_to_url_for_all_sub_pages = get_all_sub_links(site_to_crawl)
    search_and_write_badges(soup_to_url_for_all_sub_pages, re.compile('^https://www.weddyplace.com/vendors/'),
                            result_csv)


if __name__ == "__main__":
    main()
