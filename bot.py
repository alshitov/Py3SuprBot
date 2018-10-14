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

        # Пересечение представленных в магазине цветов с заданными пользователем цветами
        user_intersection = [x for x in [color['name'] for color in represented_colors] if x in [element['color']]]
        prior_intersection = [x for x in [color['name'] for color in represented_colors] if x in priority_colors]

        print('User Intersections: ', user_intersection)
        print('Prior Intersections: ', prior_intersection)

        found_color = found_size = None
        found = False
        # Если пересечений нет - ищем в приоритетных
        if len(user_intersection) == 0:
            print('No intersections found. Choosing from priority colors.')
            for repr_color in represented_colors:
                if repr_color['name'] in priority_colors:
                    print('Found priority color -', repr_color['name'])
                    # Если размер задан
                    if element['size'] != '' and 'Any' not in element['size']:
                        for size in repr_color['sizes']:     # По размерам, представленным в данном цвете
                            if size['name'] in element['size'] and size['stock_level'] != 0:
                                print(repr_color['name'], size['name'])
                                found_color = repr_color['id']
                                found_size = size['id']
                                return {'color_id': found_color, 'size_id': found_size}
                    else: # Размер не задан - берем перый доступный
                        for size in repr_color['sizes']:
                            if size['stock_level'] != 0:
                                print(repr_color['name'], size['name'])
                                found_color = repr_color['id']
                                found_size = size['id']
                                return {'color_id': found_color, 'size_id': found_size}

        # Пересечения есть, ищем среди них
        else:
            print('Intersections found. Choosing from intersections.')
            for repr_color in represented_colors:
                if repr_color['name'] in user_intersection:
                    print('Found color -', repr_color['name'])
                    # Если размер задан
                    if element['size'] != '' and 'Any' not in element['size']:
                        print('Size was set.')
                        for size in repr_color['sizes']:  # По размерам, представленным в данном цвете
                            if size['name'] in element['size'] and size['stock_level'] != 0:
                                found = True
                                found_color = repr_color['id']
                                found_size = size['id']
                                return {'color_id': found_color, 'size_id': found_size}
                    else:  # Размер не задан - берем перый доступный
                        print('Size was not set.')
                        for size in repr_color['sizes']:
                            if size['stock_level'] != 0:
                                print(repr_color['name'], size['name'])
                                found_color = repr_color['id']
                                found_size = size['id']
                                return {'color_id': found_color, 'size_id': found_size}

            else:
                print('Intersections found, but none of them fit.')
                for repr_color in represented_colors:
                    for size in repr_color['sizes']:
                        if size['stock_level'] != 0:
                            print(repr_color['name'], size['name'])
                            found_color = repr_color['id']
                            found_size = size['id']
                            return {'color_id': found_color, 'size_id': found_size}

        return {'color_id': found_color, 'size_id': found_size}


    def find_items(self):
        my_items = self.get_buy_list()

        item_found = False
        for element in my_items:

            while item_found is False:
                # вещи, доступные на сайте
                print('***********Refreshing stock.**************')
                stock = self.fetch_stock()

                for item in stock['products_and_categories'][element['type'].title()]:
                    if item['name'] == element['name']:
                        print(item['name'], 'found!')
                        item_found = True

                        item_info = self.get_item_info(item['id'])
                        print(item['name'], 'id is:', item['id'])

                        index = self.choose_size_and_color(element, item_info)
                        print(item['id'], index['color_id'], index['size_id'])

                        self.add_to_cart(item['id'], index['color_id'], index['size_id'])
                        break


























        # items_to_buy = self.get_buy_list()
        # for element in items_to_buy:
        #     print(element)
        #     item_found = color_found = size_found = False
        #     while item_found is False:
        #         # refreshing stock
        #         stock = self.fetch_stock()
        #         # loop through items in concrete type list
        #         for item in stock['products_and_categories'][element['type'].title()]:
        #             # if names match up
        #             if item['name'] == element['name']:
        #                 item_found = True
        #                 # go to url/shop/%id%.json
        #                 item_info = self.get_item_info(item['id'])
        #                 # loop through item colors
        #                 for index in item_info['styles']:
        #                     # if colors match up
        #                     if index['name'] == element['color']:
        #                         color_found = True
        #                         # loop throught sizes
        #                         for size in index['sizes']:
        #                             # if sizes match up
        #                             if size['name'] == ['size']:
        #                                 size_found = True
        #
        #                                 print('Found!')
        #
        #                                 item_id = item['id']
        #                                 item_color_id = index['id']
        #                                 item_size_id  = size['id']
        #
        #                                 self.add_to_cart(item_id, item_color_id, item_size_id)
        #                                 break
        #                         break
        #                 break
        #             else: # if no item name match found
        #                 print('Not found. Refreshing...')