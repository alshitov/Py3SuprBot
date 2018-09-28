from random import choice
import requests
from bs4 import BeautifulSoup
from parser import Parser


# refreshing proxy lists
def parse_proxies():
    prs = Parser()
    prs.parse_http_proxies()
    prs.parse_ssl_https_proxies()


def get_html(url, headers=None, proxies=None):
    r = requests.get(url, headers=headers, proxies=proxies)
    return r.text


def parse_items():
    url = 'https://www.supremecommunity.com'

    agents_list = open('useragents.txt').read().split('\n')
    http_proxies = open('http_proxies.txt').read().split('\n')
    https_proxies = open('https_proxies.txt').read().split('\n')

    proxies = {
        'http': choice(http_proxies),
        'https': choice(https_proxies)
    }

    headers = {
        "Authority": "www.supremecommunity.com",
        "Method": "GET",
        "Path": "/",
        "Scheme": "https",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip,deflate,br",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": choice(agents_list)
    }

    try:
        # get to page with droplists
        html = get_html(url + '/season/latest/droplists', headers, proxies)

        # init bs object
        soup = BeautifulSoup(html, 'html.parser')

        # find latest(future) droplist link
        latest = soup.find('a', class_='block').get('href')

        # forming latest(future) droplist link
        link_to_items = url + latest

        # get to latest(future) froplist
        html = get_html(link_to_items, headers, proxies)

        # re-init bs object with new content
        soup = BeautifulSoup(html, 'html.parser')

        # find items divs which contain items type, name, picture (and price)
        items_divs = soup.select('div.masonry__item')

        # forming dicrtionaries with items description
        drop = []
        for div in items_divs:
            drop_elem = {}

            drop_elem['type'] = div.get('class')[3][7:] # e.g.:<div class="masonry__item col-sm-4 col-xs-6 filter-sweatshirts"...>
            drop_elem['name'] = div.select_one('h5.name.item-details').text.strip()
            drop_elem['price'] = div.select_one('span.label-price').text.strip()
            drop_elem['image'] = url + str(div.find('img').get('src')) # links to images, download later!

            drop.append(drop_elem)

        for i in drop:
            print(i)

    except requests.exceptions.ConnectionError:
        print('Error! SSL: {}, HTTP: {}'.format(proxies['https'], proxies['http']))
        parse_items()


if __name__ == '__main__':
    parse_items()