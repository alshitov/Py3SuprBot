import requests
from bs4 import BeautifulSoup

def get_html(url):
    request = requests.get(url)
    return request.text


def parse_pxoxies():
    url = 'https://www.free-proxy-list.net/'
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    proxy_table = soup.find('table', id='proxylisttable')
    rows = proxy_table.find_all('tr')
    proxies = []

    for row in rows:
        tds = row.find_all('td')
        tds = [td.text.strip() for td in tds]
        if tds:
            proxy = 'http://' + str(tds[0]) + ':' + str(tds[1])
            proxies.append(proxy)

    return proxies


def dump_proxies(list, filename):
    with open(filename, mode='w', encoding='utf-8') as fin:
        fin.write('\n'.join(list))

if __name__ == '__main__':
    proxies = parse_pxoxies()
    dump = 'proxies.txt'
    dump_proxies(proxies, dump)