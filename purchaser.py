import os
from selenium.common.exceptions import *
from selenium.webdriver import Chrome
import json
import time
import requests
from bs4 import BeautifulSoup


def get_user_billing_info(filename):
    with open('user_Victor_Vasin.json', mode='r') as fout:
        user = json.load(fout)
    return user


def get_buy_list():
    with open('items_to_buy.json', mode='r') as fout:
        return json.load(fout)


def start_session():
    BINARY = os.path.dirname(os.path.realpath(__file__)) + '/chromedriver'
    browser = Chrome(BINARY)
    return browser


def detect_drop(link):
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'html.parser')

    # remember first item in list
    first_item = soup.find('a', class_='name-link').text

    # check if first item has changed. If so - items has been dropped
    while first_item == soup.find('a', class_='name-link').text:
        print(soup.find('a', class_='name-link').text)
        time.sleep(1)
    else:
        return True


def main():
    # init driver
    browser = start_session()
    market_url = 'https://supremenewyork.com/shop/all'
    browser.get(market_url)

    # getting info
    user = get_user_billing_info('sas')
    buy_list = get_buy_list()

    # main loop. Sequence = items ptiority
    for item in buy_list:
        # link to item type shop branch
        link = market_url + '/' + item['type'] \
            if item['type'] != 'tops-sweaters' \
            else market_url + '/tops_sweaters'

        # get to item type shop branch
        browser.get(link)

        # waiting for drop - reload every 1 sec.
        # if detect_drop(link):
        shop_list = browser.find_elements_by_css_selector('a.name-link')
        for index, element in enumerate(shop_list):
            try:
                if shop_list[index].text == item['name'] and shop_list[index+1].text == item['color']:
                    # go to item page
                    browser.get(element.get_attribute('href'))

                    # size choice
                    size_select = browser.find_element_by_css_selector('select#size')
                    size_select.send_keys(item['size'])

                    # add to basket button
                    add_to_basket = browser.find_element_by_name('commit')
                    add_to_basket.click()

                    # wait for 'checkout now' button to appear
                    time.sleep(0.5)

                    # go to checkout page
                    checkout_now = browser.find_element_by_css_selector('a.checkout')
                    checkout_now.click()

                    # finding billing info fields
                    order_billing_name = browser.find_element_by_id('order_billing_name')
                    order_email = browser.find_element_by_id('order_email')
                    order_tel = browser.find_element_by_id('order_billing_name')
                    bo = browser.find_element_by_id('order_tel')
                    oba3 = browser.find_element_by_id('oba3')
                    order_billing_address_3 = browser.find_element_by_id('order_billing_address_3')
                    order_billing_city = browser.find_element_by_id('order_billing_city')
                    order_billing_zip = browser.find_element_by_id('order_billing_zip')
                    order_billing_country = browser.find_element_by_id('order_billing_country')
                    credit_card_type = browser.find_element_by_id('credit_card_type')
                    cnb = browser.find_element_by_id('cnb')
                    credit_card_month = browser.find_element_by_id('credit_card_month')
                    credit_card_year = browser.find_element_by_id('credit_card_year')
                    vval = browser.find_element_by_id('vval')

                    # sending billing info keys
                    order_billing_name.send_keys(user['name'])
                    order_email.send_keys(user['email'])
                    order_tel.send_keys(user['tel'])
                    bo.send_keys(user['address'])
                    oba3.send_keys(user['address2'])
                    order_billing_address_3.send_keys(user['address3'])
                    order_billing_city.send_keys(user['city'])
                    order_billing_zip.send_keys(user['postcode'])
                    order_billing_country.send_keys(user['country'])
                    credit_card_type.send_keys(user['card_type'])
                    cnb.send_keys(user['card_number'])
                    credit_card_month.send_keys(user['card_month'])
                    credit_card_year.send_keys(user['card_year'])
                    vval.send_keys(user['card_cvv'])


                    # process payment
                    # process_payment = browser.find_element_by_css_selector('input.checkout')
                    # process_payment.click()

            except StaleElementReferenceException:
                pass








if __name__ == '__main__':
    main()