import requests
from bs4 import BeautifulSoup
from random import choice


class Parser():
    def __init__(self):
        pass


    def get_html(self, url, headers=None, proxies=None):
        request = requests.get(url, headers=headers, proxies=proxies)
        return request.text


    def parse_http_proxies(self):
        url = 'https://www.free-proxy-list.net/'
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'html.parser')

        proxy_table = soup.find('table', id='proxylisttable')
        rows = proxy_table.find_all('tr')
        self.http_proxies = []

        for row in rows:
            tds = row.find_all('td')
            tds = [td.text.strip() for td in tds]
            if tds:
                proxy = 'http://' + str(tds[0]) + ':' + str(tds[1])
                self.http_proxies.append(proxy)

        with open('http_proxies.txt', mode='w', encoding='utf-8') as fin:
            fin.write('\n'.join(self.http_proxies))


    def parse_ssl_https_proxies(self):
        url = 'https://www.sslproxies.org/'
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'html.parser')

        proxy_table = soup.find('table', id='proxylisttable')
        rows = proxy_table.find_all('tr')
        self.https_proxies = []

        for row in rows:
            tds = row.find_all('td')
            tds = [td.text.strip() for td in tds]
            if tds:
                proxy = 'http://' + str(tds[0]) + ':' + str(tds[1])
                self.https_proxies.append(proxy)

        with open('https_proxies.txt', mode='w', encoding='utf-8') as fin:
            fin.write('\n'.join(self.https_proxies))


    def parse_sizing_tables(self):
        url = 'https://supremenewyork.com/shop/sizing'
        self.html = self.get_html(url)
        self.soup = BeautifulSoup(self.html, 'html.parser')

        self.objects = []
        tables = self.soup.find_all('table')

        for table in tables:

            table_head = table.find('thead')
            headers = table_head.find_all('th')
            titles = [header.text for header in headers]

            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            data = []
            for row in rows:
                cols = row.find_all('td')
                cols = [cell.text.strip() for cell in cols]
                data.append([cell for cell in cols if cell])

            self.object_ = {
                'headers': titles,
                'data': data
            }

            self.objects.append(self.object_)

        article = self.soup.find('article', class_='blurb')
        current_title = article.find('h2').text

        return [self.objects, current_title]


    def parse_main_window_content(self):
        # first, refreshing proxy lists
        self.parse_http_proxies()
        self.parse_ssl_https_proxies()
        # target url
        url = 'https://www.supremecommunity.com'
        # reading (already refreshed) proxies and user-agents for request
        agents_list = open('useragents.txt').read().split('\n')
        http_proxies = open('http_proxies.txt').read().split('\n')
        https_proxies = open('https_proxies.txt').read().split('\n')
        # setting up proxy dict
        proxies = {
            'http': choice(http_proxies),
            'https': choice(https_proxies)
        }
        # headers like from normal browser
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
            html = self.get_html(url + '/season/latest/droplists', headers, proxies)

            # init bs object
            soup = BeautifulSoup(html, 'html.parser')

            # find latest(future) droplist link
            latest = soup.find('a', class_='block').get('href')

            # forming latest(future) droplist link
            link_to_items = url + latest

            # get to latest(future) froplist
            html = self.get_html(link_to_items, headers, proxies)

            # re-init bs object with new content
            soup = BeautifulSoup(html, 'html.parser')

            # find items divs which contain items type, name, picture (and price)
            items_divs = soup.select('div.masonry__item')

            # forming dicrtionaries with items description
            drop = []
            for div in items_divs:
                drop_elem = {}
                # e.g.:<div class="masonry__item col-sm-4 col-xs-6 filter-sweatshirts"...>
                drop_elem['type'] = div.get('class')[3][7:]

                img = div.find('img')
                img_alt_split = img.get('alt').split(' - ')

                drop_elem['name'] = img_alt_split[0].strip()
                drop_elem['description'] = img_alt_split[1].strip()
                drop_elem['price'] = div.select_one('span.label-price').text.strip()
                drop_elem['image'] = url + str(img.get('src'))  # links to images, download later!

                drop.append(drop_elem)

            for i in drop:
                print(i)

        except requests.exceptions.ConnectionError:
            print('Error! SSL: {}, HTTP: {}'.format(proxies['https'], proxies['http']))
            # if error occurred, try parsing once again until success
            self.parse_main_window_content()
