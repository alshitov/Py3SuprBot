import requests
from bs4 import BeautifulSoup


class Parser():
    def __init__(self):
        pass


    def get_html(self, url, headers=None, proxies=None, cookies=None):
        request = requests.get(url)
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