from crawler import get_all_sub_links, search_and_write_badges

site_to_crawl = "https://www.spree-liebe.de/hochzeitsfotograf-berlin-empfehlung/weddyplace/"
# site_to_crawl = "http://www.andreaslemke.com/"
result_csv = 'result_files/result.csv'

sub_pages = {site_to_crawl}
soups_to_url = []

soup_to_url_for_all_sub_pages = get_all_sub_links(site_to_crawl, site_to_crawl, sub_pages, soups_to_url)
search_and_write_badges(soup_to_url_for_all_sub_pages, result_csv)
