import os
import requests
import json
import time
from re import search, findall
from re import split as re_s
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from seleniumrequests import Chrome



class BotWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.bot_window = QDialog(self)
        self.vert_layout = QVBoxLayout()
        self.horiz_layout = QHBoxLayout()

        self.info_label_check_items = QLabel('<b>Check your buy list:</b>')
        self.info_label_choose_user = QLabel('<b>Choose user:</b>')
        self.info_label_choose_time = QLabel('<b>Choose drop time(GMT):</b>')

        self.check_items_label = QLabel()
        self.choose_user_combobox = QComboBox()
        self.choose_time_label = QTimeEdit()
        self.cancel_button = QPushButton('Cancel')
        self.process_button = QPushButton('Process')

        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignHCenter)
        self.logo_label.setPixmap(QPixmap(self.scriptDir + '/img/logos/checkout.png'))
        self.vert_layout.addWidget(self.logo_label)

        self.vert_layout.addWidget(self.info_label_check_items)
        self.vert_layout.addWidget(self.check_items_label)
        self.vert_layout.addWidget(self.info_label_choose_user)
        self.vert_layout.addWidget(self.choose_user_combobox)
        self.vert_layout.addWidget(self.info_label_choose_time)
        self.vert_layout.addWidget(self.choose_time_label)
        self.vert_layout.addLayout(self.horiz_layout)
        self.horiz_layout.addWidget(self.cancel_button)
        self.horiz_layout.addWidget(self.process_button)

        self.check_items_label.setAlignment(Qt.AlignTop)

        self.load_buy_list()
        self.load_users_list()
        self.connect_buttons()

        self.bot_window.setLayout(self.vert_layout)
        self.bot_window.setFixedSize(640, 360)
        self.bot_window.setWindowTitle('Check Bot Settings')
        self.bot_window.setModal(True)
        self.bot_window.exec_()


    def connect_buttons(self):
        self.connect(self.cancel_button,
                     SIGNAL('clicked()'),
                     self.bot_window.close)

        self.connect(self.process_button,
                     SIGNAL('clicked()'),
                     lambda: self.process_payment())


    def load_buy_list(self):
        with open("json/items_to_buy.json", mode='r', encoding='utf-8') as fout:
            items = json.load(fout)

        if len(items) == 0:
            self.check_items_label.setText('You have not chosen any products yet!')

        else:
            text = ''
            for index, item in enumerate(items):
                text += str(index + 1) + '. ' \
                        + item['name'] + ' / ' \
                        + item['color'] + ' / ' \
                        + item['size'] + '\n'

            self.check_items_label.setText(text)


    def load_users_list(self):
        files = os.listdir(self.scriptDir + '/json/')
        users = [file[5:-5]
                 for file in files if search('user_(.*?).json', file)]
        self.choose_user_combobox.addItems(users)


    def process_payment(self):
        current_user = 'user_' + self.choose_user_combobox.currentText() + '.json'
        drop_time = self.choose_time_label.text()

        bot_ = Bot(current_user, drop_time)
        bot_.find_items()


class Bot:
    def __init__(self, current_user, drop_time):
        self.current_user = current_user
        self.drop_time = drop_time

        self.headers = {
            "Authority": "www.supremenewyork.com",
            "Method": "GET",
            "Path": "/",
            "Scheme": "https",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,br",
            "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)"
        }


    # получаем информацию о пользователе из файла
    @staticmethod
    def get_user_billing_info(filename):
        with open('json/' + filename, mode='r') as fout:
            user = json.load(fout)
        return user


    # получаем список вещей на покупку из файла
    @staticmethod
    def get_buy_list():
        with open('json/items_to_buy.json', mode='r') as fout:
            return json.load(fout)


    # получаем список всех вещей, находящихся на данный момент в продаже
    def fetch_stock(self):
        return requests.request('GET', 'http://www.supremenewyork.com/mobile_stock.json', headers=self.headers).json()


    def get_item_info(self, id):
        return requests.request('GET', 'http://www.supremenewyork.com/shop/{}.json'.format(id), headers=self.headers).json()


    def pure_cart_generator(self, data):
        sizes = ''
        total = 0
        sizes_colors = ''

        for piece in data:
            total += int(piece[3])
            sizes += '"{}":1,'.format(piece[2])
            sizes_colors += '{},{}-'.format(piece[2], piece[1])

        count = len(data)
        if count == 1:
            cookie = '"cookie":"1 item--"'
        else:
            cookie = '"cookie":"{}+items--{}"'.format(count, sizes_colors[:-1])

        from urllib.request import quote
        return quote('{' + sizes + cookie + ',"total":"€{}"'.format(total) + '}', safe='')


    def checkout(self, response, data):
        sess = cart = ''

        for item in re_s('[;,]', response.headers['Set-Cookie']):
            if item[:9] == ' _supreme':
                sess = item
                break

        for item in re_s('[;,]', response.headers['Set-Cookie']):
            if item[:4] == 'cart':
                cart = item
                break

        pure_cart = self.pure_cart_generator(data)

        url = 'https://www.supremenewyork.com/checkout'

        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch, br',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive',
                   'Cookie': 'pure_cart={};'.format(pure_cart) + 'cart={};'.format(cart) + '_supreme_sess={};'.format(
                       sess),
                   'Host': 'www.supremenewyork.com',
                   'If-None-Match': 'W/"7cd6c2d3c1278e6ec2f8f895e92dc2dd"',
                   'Referer': 'https:/www.supremenewyork.com/checkout',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
                   }

        auth_r = requests.post(url=url, headers=headers, timeout=2)

        x_csrf_token = findall('<meta name="csrf-token" content="(.*==)" />', auth_r.text)[0]

        user = self.get_user_billing_info(self.current_user)

        form_data = {
            'authenticity_token': x_csrf_token,
            'order[billing_name]': user['name'],
            'order[email]': user['email'],
            'order[tel]': user['tel'],
            'order[billing_address]': user['address'],
            'order[billing_address_2]': user['address2'],
            'order[billing_address_3]': user['address3'],
            'order[billing_city]': user['city'],
            'order[billing_zip]': user['postcode'],
            'order[billing_country]': user['country'],
            'same_as_billing_address': '1',
            'store_credit_id': '0',
            'credit_card[type]': user['card_type'],
            'credit_card[cnb]': user['card_number'],
            'credit_card[month]': user['card_month'],
            'credit_card[year]': user['card_year'],
            'credit_card[vval]': user['card_cvv'],
            'order[terms]': '1',
            'hpcvv': ''
        }

        browser = Chrome(os.path.dirname(os.path.realpath(__file__)) + '/chromedriver')
        browser.get(url='https://www.supremenewyork.com/shop/cart')
        browser.delete_all_cookies()

        for key, value in requests.utils.dict_from_cookiejar(response.cookies).items():
            browser.add_cookie({'name': key, 'value': value})

        browser.refresh()
        browser.get(url='https://www.supremenewyork.com/checkout')
        response = browser.request('POST', 'https://www.supremenewyork.com/checkout', data=form_data)

        print(response.content)

    @staticmethod
    def show_cookies(response):
        cookie_dict_wrapper = []
        for key, value in requests.utils.dict_from_cookiejar(response.cookies).items():
            dict_template = {
                'domain': '.supremenewyork.com',
                'expiry': int(time.time()+7200),
                'httpOnly': False,
                'path': '/',
                'secure': False,
                'name': key,
                'value': value
            }
            cookie_dict_wrapper.append(dict_template)
        print('Cookies:', json.dumps(cookie_dict_wrapper, indent=4))


    def add_to_cart(self, data):
        print('Adding to cart...')
        response = None
        cookies = {}

        for element in data:
            product_id = element[0]
            color_id = element[1]
            size_id = element[2]

            form_data = {
                'utf8': '%E2%9C%93',
                'style': str(color_id),
                'size': str(size_id),
                'commit': 'add+to+basket'
            }

            headers = {
                'Authotiry': 'www.supremenewyork.com',
                'Method': 'POST',
                'Path': '/shop/{}/add'.format(product_id),
                'Scheme': 'https',
                'accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, '
                          'application/x-ecmascript',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'content-length': '58',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://www.supremenewyork.com',
                'referer': 'https://www.supremenewyork.com/shop/',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/69.0.3497.100 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }

            response = requests.request('POST',
                                        'https://www.supremenewyork.com/shop/{}/add.json'.format(product_id),
                                        data=form_data,
                                        headers=headers,
                                        cookies=cookies)
            cookies = response.cookies


        # self.show_cookies(response)
        self.checkout(response, data)


    @staticmethod
    def choose_size_and_color(element, item_info):
        print('**************Choosing color and size**************')
        # Приоритетные цвета, если цвет не задан или задан любой цвет
        priority_colors = ['White', 'Black', 'Red', 'Green', 'Blue']

        # Представленные в магазине цвета по данной вещи
        represented_colors = item_info['styles']

        # Флаги цвета и размера
        color_is_not_set = 'Any' in element['color'] or element['color'] == ''
        size_is_not_set = 'Any' in element['size'] or element['size'] == ''

        # Начало выбора
        # Цвет не задан
        if color_is_not_set:
            # Итерация по представленным цветам
            for color in represented_colors:
                # Проверка на присутствие представленного в магазине цвета в приоритетных
                if color['name'] in priority_colors:
                    # Если размер не выставлен
                    if size_is_not_set:
                        for size in color['sizes']:
                            # Проверка только на доступность данного размера
                            if size['stock_level'] is not 0:
                                return {'color_id': color['id'], 'size_id': size['id']}
                    # Размер выставлен
                    else:
                        for size in color['sizes']:
                            # Проверка на доступность данного размера и на присутствие его в списке пользователя
                            if size['name'] in element['size'] and size['stock_level'] is not 0:
                                return {'color_id': color['id'], 'size_id': size['id']}
            # Если не найдено в приоритетных - идем по всем
            else:
                for color in represented_colors:
                    if color['name'] not in priority_colors:
                        # Размер не выставлен
                        if size_is_not_set:
                            for size in color['sizes']:
                                if size['stock_level'] is not 0:
                                    return {'color_id': color['id'], 'size_id': size['id']}
                        # Размер выставлен
                        else:
                            for size in color['sizes']:
                                # Проверка на доступность данного размера и на присутствие его в списке пользователя
                                if size['name'] in element['size'] and size['stock_level'] is not 0:
                                    return {'color_id': color['id'], 'size_id': size['id']}
                else:
                    for color in represented_colors:
                        for size in color['sizes']:
                            if size['name'] in element['size'] and size['stock_level'] is not 0:
                                return {'color_id': color['id'], 'size_id': size['id']}

        # Цвет задан
        else:
            # Итерация по представленным цветам
            for color in represented_colors:
                # Проверка на присутствие представленного в магазине цвета в пользовательских цветах
                if color['name'] in element['color']:
                    # Если размер не выставлен
                    if size_is_not_set:
                        for size in color['sizes']:
                            # Проверка только на доступность данного размера
                            if size['stock_level'] is not 0:
                                return {'color_id': color['id'], 'size_id': size['id']}
                    # Размер выставлен
                    else:
                        for size in color['sizes']:
                            # Проверка на доступность данного размера и на присутствие его в списке пользователя
                            if size['name'] in element['size'] and size['stock_level'] is not 0:
                                return {'color_id': color['id'], 'size_id': size['id']}
            # Ни одного пользовательского цвета не найдено - идем по приоритетным
            else:
                # Итерация по приоритетным цветам
                for color in represented_colors:
                    # Проверка на присутствие представленного в магазине цвета в приоритетных
                    if color['name'] in priority_colors:
                        # Если размер не выставлен
                        if size_is_not_set:
                            for size in color['sizes']:
                                # Проверка только на доступность данного размера
                                if size['stock_level'] is not 0:
                                    return {'color_id': color['id'], 'size_id': size['id']}
                        # Размер выставлен
                        else:
                            for size in color['sizes']:
                                # Проверка на доступность данного размера и на присутствие его в списке пользователя
                                if size['name'] in element['size'] and size['stock_level'] is not 0:
                                    return {'color_id': color['id'], 'size_id': size['id']}
                # Если не найдено в приоритетных - идем по всем
                else:
                    for color in represented_colors:
                        if color['name'] not in priority_colors:
                            if size_is_not_set:
                                for size in color['sizes']:
                                    if size['stock_level'] is not 0:
                                        return {'color_id': color['id'], 'size_id': size['id']}
                    else:
                        for color in represented_colors:
                            for size in color['sizes']:
                                if size['name'] in element['size'] and size['stock_level'] is not 0:
                                    return {'color_id': color['id'], 'size_id': size['id']}

        # Конец выбора

        # Если предмет не найден
        return {'color_id': None, 'size_id': None}


    def find_items(self):
        my_items = self.get_buy_list()
        requests_data = []

        for element in my_items:

            item_found = False
            while not item_found:
                print('Refreshing stock.')
                # вещи, доступные на сайте
                stock = self.fetch_stock()
                element['type'] = 'Tops/Sweaters' if element['type'] == 'tops-sweaters' else element['type'].title()
                for item in stock['products_and_categories'][element['type']]:
                    if item['name'] == element['name']:
                        item_found = True
                        price = round(item['price_euro'] / 100)
                        print(price)
                        item_info = self.get_item_info(item['id'])
                        color_and_size = self.choose_size_and_color(element, item_info)
                        if color_and_size['color_id'] is None or color_and_size['size_id'] is None:
                            print('Desired item has been sold out')
                            # TODO: create algorithm(add to bot config) that will buy item with any color and size if desired item was sold out
                        else:
                            requests_data.append([item['id'], color_and_size['color_id'], color_and_size['size_id'], price])

                time.sleep(1) if not item_found else None

        if len(requests_data) == len(my_items):
            self.add_to_cart(requests_data)