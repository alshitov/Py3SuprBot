import sys
import os
import requests
import json
import time
from re import search

from requests.utils import dict_from_cookiejar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        # here to collect user and time
        # and process them to bot init
        bot_ = Bot()
        bot_.find_items()



class Bot():
    def __init__(self):
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
        self.driver = webdriver.Chrome(os.path.dirname(os.path.realpath(__file__)) + '/chromedriver')

    # получаем информацию о пользователе из файла
    def get_user_billing_info(self, filename):
        with open(filename, mode='r') as fout:
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


    def checkout(self):
        self.driver.get('https://www.supremenewyork.com/checkout')

        print(self.driver.get_cookies())

        user = self.get_user_billing_info('something')

        name_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="order_billing_name"]')))
        name_input.send_keys(user['name'])

        email_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="order_email"]')))
        email_input.send_keys(user['email'])

        tel_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="order_tel"]')))
        tel_input.send_keys(user['tel'])

        address_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="bo"]')))
        address_input.send_keys(user['address'])

        address2_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="oba3"]')))
        address2_input.send_keys(user['address2'])

        address3_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="order_billing_address_3"]')))
        address3_input.send_keys(user['address3'])

        city_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="order_billing_city"]')))
        city_input.send_keys(user['city'])

        zip_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="order_billing_zip"]')))
        zip_input.send_keys(user['postcode'])

        self.driver.find_element_by_xpath('//*[@id="order_billing_country"]').send_keys(user['country'])
        self.driver.find_element_by_xpath('//*[@id="credit_card_type"]').send_keys(user['card_type'])

        card_n_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="cnb"]')))
        card_n_input.send_keys(user['card_number'])

        self.driver.find_element_by_xpath('//*[@id="credit_card_month"]').send_keys(user['card_month'])
        self.driver.find_element_by_xpath('//*[@id="credit_card_year"]').send_keys(user['card_year'])

        card_cvv_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="vval"]')))
        card_cvv_input.send_keys(user['card_cvv'])

        self.driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/form/div[2]/div[2]/fieldset/p/label/div/ins').click()

        time.sleep(200)


    def continue_to_cart(self, response):
        self.driver.get('http://www.supremenewyork.com/shop/cart')  # commonly carts
        self.driver.delete_all_cookies()
        for key, value in dict_from_cookiejar(response.cookies).items():
            self.driver.add_cookie({'name': key, 'value': value})
        self.driver.refresh()
        self.checkout()


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
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.supremenewyork.com',
            'referer': 'https://www.supremenewyork.com/shop/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'x-csrf-token': 'cIwuKktS3yIn2yodqGwBOvutPdY8DVWk0R3QqUkWwQLmtNm09HJ2uca6XA6t22NI3y6RZYWJk1jiCNrTGG/j7g==',
            'x-requested-with': 'XMLHttpRequest',
        }

        response = requests.request('POST', 'https://www.supremenewyork.com/shop/{}/add.json'.format(product_id),
                                        data=form_data, headers=headers)

        if response.status_code != 200:
            print('Status code != 200')
            sys.exit()
        else:
            # print(response.json())
            if response.json() == {}:
                print('Responce empty!')

        # self.show_cookies(response)
        self.continue_to_cart(response)


    def find_items(self):
        items_to_buy = self.get_buy_list()
        # for item, index in enumerate(items_to_buy):
        item_found = 0
        while item_found == 0:
            # refreshing stock
            stock = self.fetch_stock()
            # loop through items in concrete type list
            for item in stock['products_and_categories'][items_to_buy[0]['type'].title()]:
                # if names match up
                if item['name'] == items_to_buy[0]['name']:
                    # go to url/shop/%id%.json
                    item_info = self.get_item_info(item['id'])
                    # loop through item colors
                    for index in item_info['styles']:
                        # if colors match up
                        if index['name'] == items_to_buy[0]['color']:
                            # loop throught sizes
                            for size in index['sizes']:
                                # if sizes match up
                                if size['name'] == items_to_buy[0]['size']:
                                    item_found = 1

                                    print('Found!')

                                    item_id = item['id']
                                    item_color_id = index['id']
                                    item_size_id  = size['id']

                                    self.add_to_cart(item_id, item_color_id, item_size_id)
                                    break
                            break
                    break
                else: # if no item name match found
                    print('Not found. Refreshing...') # wait for several secs, thus not to get banned maybe?