import requests
from bs4 import BeautifulSoup


def get_html(url):
    request = requests.get(url)
    return request.text


def parse_table():
    url = 'https://supremenewyork.com/shop/sizing'
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    title_ths = soup.find_all('th')
    titles = [t_th.text for t_th in title_ths]
    idx = 0
    separate_item_titles = []
    while idx != len(titles):
        separate_item_titles.append(titles[idx:idx + 5])
        idx += 5

    measure_tds = soup.find_all('td')
    measures = [m_td.text for m_td in measure_tds]
    idx = 0
    separate_item_measures = []
    while idx != len(measures):
        separate_item_measures.append(measures[idx:idx + 5])
        idx += 5

    #       forming objects     #
    objects = []
    i = 0
    for index in range(len(separate_item_titles)):
        object_ = {}
        object_['name'] = separate_item_titles[index]
        object_['sizes'] = []
        object_['sizes'].append(separate_item_measures[i:i+3])
        i += 3
        objects.append(object_)

    # for object in objects:
    #     print(object, '\n\n')
    return objects


if __name__ == '__main__':
    parse_table()