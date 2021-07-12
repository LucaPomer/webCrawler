# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup


def get_website_content(url):
    page = requests.get(url)
    print(page.status_code)
    # print(page.content)
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify())
    html = list(soup.children)[2]
    print(html)

    all_p_tags = soup.find_all('p')
    print(all_p_tags)
    print(all_p_tags[0].get_text())


get_website_content("https://dataquestio.github.io/web-scraping-pages/simple.html")
