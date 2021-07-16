import re
import requests
from bs4 import BeautifulSoup
from helpers.data_writer import write_multiple_lines, write_data


def find_badge_in_content(soup):
    badge_tag = soup.find('a', href=re.compile('^https://www.weddyplace.com/vendors/'))
    if badge_tag is None:
        return None
    badge_element = []
    img = badge_tag.find('img')
    image_src = img['data-src']
    badge_element.append(badge_tag['href'])
    badge_element.append(image_src)
    return badge_element


def page_is_sub_page(original_page, new_url):
    splitted_og_page = original_page.split('/')
    domain = splitted_og_page[2]
    if domain in new_url:
        return True
    else:
        return False


def get_all_sub_links(page_url, start_page, all_urls, soups_to_url):
    try:
        html = requests.get(page_url, timeout=10)
        soup = BeautifulSoup(html.content, 'html.parser')
        soups_to_url.append([soup, page_url])
        for link in soup.find_all("a", href=True):
            new_link = link['href']
            if new_link not in all_urls and page_is_sub_page(start_page, new_link):
                # print(new_link)
                all_urls.add(new_link)
                get_all_sub_links(new_link, start_page, all_urls, soups_to_url)
    except requests.ConnectionError as e:
        print(
            "OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
    except requests.Timeout as e:
        print("OOPS!! Timeout Error")
        print(str(e))
    except requests.exceptions.MissingSchema as e:
        print('Wrong URL scema: URL = ' + str(page_url))
    except requests.RequestException as e:
        print("OOPS!! General Error")
        print(str(e))
    except KeyboardInterrupt:
        print("Someone closed the program")

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


