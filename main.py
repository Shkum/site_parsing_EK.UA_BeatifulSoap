from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup



def get_html(url):
    ua = UserAgent()
    headers = {
        'useragent': ua.random
    }
    r = requests.get(url, headers=headers)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('a', {"id": "pager_15"}).getText()
    return int(pages)


def main():
    url = 'https://ek.ua/ek-list.php?katalog_=122&page_={0}&search_=samsung+galaxy'.format(0)
    html = get_html(url)
    page_count = get_total_pages(html)
    for i in range(page_count):
        url = 'https://ek.ua/ek-list.php?katalog_=122&page_={0}&search_=samsung+galaxy'.format(i)
        print(url)
    print(page_count)


if __name__ == '__main__':
    main()
