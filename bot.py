import sys
import os
import requests
import json
import time
from re import search
from requests.utils import dict_from_cookiejar

from PyQt4.QtGui import *
from PyQt4.QtCore import *


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


class Bot():
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
    def get_user_billing_info(self, filename):
        with open('json/' + filename, mode='r') as fout:
            user = json.load(fout)
        return user


    # получаем список вещей на покупку из файла
    def get_buy_list(self):
        with open('json/items_to_buy.json', mode='r') as fout:
            return json.load(fout)


    # получаем список всех вещей, находящихся на данный момент в продаже
    def fetch_stock(self):
        return requests.request('GET', 'http://www.supremenewyork.com/mobile_stock.json', headers=self.headers).json()


    def get_item_info(self, id):
        return requests.request('GET', 'http://www.supremenewyork.com/shop/{}.json'.format(id), headers=self.headers).json()


    def continue_to_cart(self, response):
        # self.driver.get('http://www.supremenewyork.com/shop/cart')  # commonly carts
        # self.driver.delete_all_cookies()
        # for key, value in dict_from_cookiejar(response.cookies).items():
        #     self.driver.add_cookie({'name': key, 'value': value})
        # self.driver.refresh()
        # self.checkout()
        pass


    def show_cookies(self, response):
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


    def add_to_cart(self, product_id, color_id, size_id):
        print('Adding to cart...')

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
            'accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-length': '58',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.supremenewyork.com',
            'referer': 'https://www.supremenewyork.com/shop/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        response = requests.request('POST', 'https://www.supremenewyork.com/shop/{}/add.json'.format(product_id),
                                        data=form_data, headers=headers)

        if response.status_code != 200:
            print('Status code != 200')
            sys.exit()
        elif response.json() == {}:
                print('Response is empty!')
        else:
            pass

        self.show_cookies(response)
        self.continue_to_cart(response)


    def choose_size_and_color(self, element, item_info):
        print('**************Choosing color and size**************')
        # Приоритетные цвета, если цвет не задан или задан любой цвет
        priority_colors = ['White', 'Black', 'Red', 'Green', 'Blue']

        # Представленные в магазине цвета по данной вещи
        represented_colors = item_info['styles']

        # Флаги цвета и размера
        color_is_not_set = 'Any' in element['color'] or element['color'] == ''
        size_is_not_set = 'Any' in element['size'] or element['size'] == ''

        ###################### Начало перебора ######################
        # Цвет не задан
        if color_is_not_set:
            for color in represented_colors: # Итерация по представленным цветам
                if color['name'] in priority_colors: # Проверка на присутствие представленного в магазине цвета в приоритетных
                    if size_is_not_set: # Если размер не выставлен
                        for size in color['sizes']:
                            if size['stock_level'] is not 0: # Проверка только на доступность данного размера
                                print(color['name'], size['name'])
                                return {'color_id': color['id'], 'size_id': size['id']}
                    else: # Размер выставлен
                        for size in color['sizes']:
                            # Проверка на доступность данного размера и на присутствие его в списке пользователя
                            if size['name'] in element['size'] and size['stock_level'] is not 0:
                                print(color['name'], size['name'])
                                return {'color_id': color['id'], 'size_id': size['id']}

            else: # Если не найдено в приоритетных - идем по всем
                print('Not found in priority')
                for color in represented_colors:
                    if color['name'] not in priority_colors:
                        if size_is_not_set:
                            for size in color['sizes']:
                                if size['stock_level'] is not 0:
                                    print(color['name'], size['name'])
                                    print('return 246')
                                    return {'color_id': color['id'], 'size_id': size['id']}
                        else:  # Размер выставлен
                            for size in color['sizes']:
                                # Проверка на доступность данного размера и на присутствие его в списке пользователя
                                if size['name'] in element['size'] and size['stock_level'] is not 0:
                                    print(color['name'], size['name'])
                                    print('return 253')
                                    return {'color_id': color['id'], 'size_id': size['id']}
                else:
                    for color in represented_colors:
                        for size in color['sizes']:
                            if size['name'] in element['size'] and size['stock_level'] is not 0:
                                print(color['name'], size['name'])
                                print('return 260')
                                return {'color_id': color['id'], 'size_id': size['id']}

        # Цвет задан
        else:
            for color in represented_colors: # Итерация по представленным цветам
                if color['name'] in element['color']: # Проверка на присутствие представленного в магазине цвета в пользовательских цветах
                    if size_is_not_set: # Если размер не выставлен
                        for size in color['sizes']:
                            if size['stock_level'] is not '0': # Проверка только на доступность данного размера
                                print(color['name'], size['name'])
                                print('return 270')
                                return {'color_id': color['id'], 'size_id': size['id']}
                    else: # Размер выставлен
                        for size in color['sizes']:
                            # Проверка на доступность данного размера и на присутствие его в списке пользователя
                            if size['name'] in element['size'] and size['stock_level'] is not 0:
                                print(color['name'], size['name'])
                                print('return 277')
                                return {'color_id': color['id'], 'size_id': size['id']}

            else: # Ни одного пользовательского цвета не найдено - идем по приоритетным
                for color in represented_colors:  # Итерация по приоритетным цветам
                    if color['name'] in priority_colors:  # Проверка на присутствие представленного в магазине цвета в приоритетных
                        if size_is_not_set:  # Если размер не выставлен
                            for size in color['sizes']:
                                if size['stock_level'] is not '0':  # Проверка только на доступность данного размера
                                    print(color['name'], size['name'])
                                    print('return 287')
                                    return {'color_id': color['id'], 'size_id': size['id']}
                        else:
                            for size in color['sizes']:
                                # Проверка на доступность данного размера и на присутствие его в списке пользователя
                                if size['name'] in element['size'] and size['stock_level'] is not 0:
                                    print(color['name'], size['name'])
                                    print('return 293')
                                    return {'color_id': color['id'], 'size_id': size['id']}
                else:  # Если не найдено в приоритетных - идем по всем
                    for color in represented_colors:
                        if color['name'] not in priority_colors:
                            if size_is_not_set:
                                for size in color['sizes']:
                                    if size['stock_level'] is not '0':
                                        print(color['name'], size['name'])
                                        print('return 303')
                                        return {'color_id': color['id'], 'size_id': size['id']}
                    else:
                        for color in represented_colors:
                            for size in color['sizes']:
                                if size['name'] in element['size'] and size['stock_level'] is not 0:
                                    print(color['name'], size['name'])
                                    print('return 310')
                                    return {'color_id': color['id'], 'size_id': size['id']}

        ###################### Конец перебора ######################
        return {'color_id': None, 'size_id': None}


    def find_items(self):
        my_items = self.get_buy_list()

        item_found = False
        for element in my_items:

            while item_found is False:
                # вещи, доступные на сайте
                print('***********Refreshing stock.**************')
                stock = self.fetch_stock()
                element['type'] = 'Tops/Sweaters' if element['type'] == 'tops-sweaters' else element['type'].title()

                for item in stock['products_and_categories'][element['type']]:
                    if item['name'] == element['name']:
                        print(item['name'], 'found!')
                        item_found = True

                        item_info = self.get_item_info(item['id'])
                        print(item['name'], 'id is:', item['id'])

                        index = self.choose_size_and_color(element, item_info)
                        if index['color_id'] is None or index['size_id'] is None:
                            print('Desired item has been sold out')
                            # TODO: create algorithm(add to bot config) that will buy item with any color and size if desired item was sold out
                        else:
                            print('Info to request: ', item['id'], index['color_id'], index['size_id'])

                        # self.add_to_cart(item['id'], index['color_id'], index['size_id'])