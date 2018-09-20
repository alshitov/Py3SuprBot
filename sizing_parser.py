import requests
from bs4 import BeautifulSoup


def get_html(url):
    request = requests.get(url)
    return request.text


def parse_table():
    url = 'https://supremenewyork.com/shop/sizing'
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    objects = []
    tables = soup.find_all('table')

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

        object_ = {
            'headers': titles,
            'data': data
        }

        objects.append(object_)
    return objects


if __name__ == '__main__':
    parse_table()