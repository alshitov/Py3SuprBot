import requests
from bs4 import BeautifulSoup


class Parser():
    def __init__(self):
        pass


    def get_html(self, url, headers=None, proxies=None, cookies=None):
        request = requests.get(url)
        return request.text


    def parse_proxies(self):
        url = 'https://www.free-proxy-list.net/'
        self.html = self.get_html(url)
        self.soup = BeautifulSoup(self.html, 'html.parser')

        proxy_table = self.soup.find('table', id='proxylisttable')
        rows = proxy_table.find_all('tr')
        self.proxies = []

        for row in rows:
            tds = row.find_all('td')
            tds = [td.text.strip() for td in tds]
            if tds:
                proxy = 'http://' + str(tds[0]) + ':' + str(tds[1])
                self.proxies.append(proxy)

        return self.proxies


    def dump_proxies(self, list, filename):
        with open(filename, mode='w', encoding='utf-8') as fin:
            fin.write('\n'.join(list))


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