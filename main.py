from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup

from time import time


def get_func_time(func):
    def wrapper():
        start_time = time()
        func()
        end_time = time()
        result = round(end_time - start_time, 2)
        print(f'>>>> Done in {result} second(s)')

    return wrapper


def get_html(url):  # get HTML text
    ua = UserAgent()
    headers = {
        'useragent': ua.random
    }
    r = requests.get(url, headers=headers)
    return r.text


def get_total_pages(html):  # GET TOTAL PAGE COUNT
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('a', {"id": "pager_15"}).getText()
    return int(pages)


def get_all_page_links(url_list):  # GET ALL ITEM LINKS ON EACH PAGE
    base_url = 'https://ek.ua'
    links = []
    for url in url_list:
        print('Getting links for:', url)
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        elements = soup.select(".model-short-title.no-u")
        for el in elements:
            links.append(base_url + el.get('href'))
    return links


def get_all_pages_links(url, page_count):  # GET ALL LINKS FOR EACH PAGE IN PAGINATION
    result = []
    for i in range(page_count):
        url = 'https://ek.ua/ek-list.php?katalog_=122&page_={}&search_=samsung+galaxy'.format(i)
        result.append(url)
    return result


def get_all_links():
    url = 'https://ek.ua/ek-list.php?katalog_=122&page_=0&search_=samsung+galaxy'
    html = get_html(url)
    page_count = get_total_pages(html)
    page_link_list = get_all_pages_links(url, page_count)
    all_pages_links = get_all_page_links(page_link_list)
    return all_pages_links


def get_model_price(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    try:
        model = soup.find('b', {'class': 'ib'}).getText().replace(u'\xa0', ' ')
        price = soup.find('span', {'itemprop': "lowPrice", 'content': True})['content']
    except:
        try:
            model = soup.find('h1', {'itemprop': 'name'}).getText().replace(u'\xa0', ' ')
            price = soup.find('span', {'itemprop': "lowPrice", 'content': True})['content']
        except:
            model = None
            price = None
    if model is not None:
        print({'model': model, 'price': price})
    else:
        print(url)


# 23 sec
@get_func_time
def main():
    final_links_list = get_all_links()
    for link in final_links_list:
        get_model_price(link)


if __name__ == '__main__':
    main()
