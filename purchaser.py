import os
from selenium.common.exceptions import *
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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
                    checkout_now = WebDriverWait(browser, 3).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.checkout')))

                    # go to checkout page
                    checkout_now.click()

                    # finding billing info fields and sending billing info keys
                    name_input = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="order_billing_name"]')))
                    name_input.send_keys(user['name'])

                    email_input = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="order_email"]')))
                    email_input.send_keys(user['email'])

                    tel_input = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="order_tel"]')))
                    tel_input.send_keys(user['tel'])

                    address_input= WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="bo"]')))
                    address_input.send_keys(user['address'])

                    address2_input = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="oba3"]')))
                    address2_input.send_keys(user['address2'])

                    address3_input = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="order_billing_address_3"]')))
                    address3_input.send_keys(user['address3'])

                    city_input = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="order_billing_city"]')))
                    city_input.send_keys(user['city'])

                    zip_input = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="order_billing_zip"]')))
                    zip_input.send_keys(user['postcode'])

                    browser.find_element_by_xpath('//*[@id="order_billing_country"]').send_keys(user['country'])
                    browser.find_element_by_xpath('//*[@id="credit_card_type"]').send_keys(user['card_type'])

                    card_n_input = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="cnb"]')))
                    card_n_input.send_keys(user['card_number'])

                    browser.find_element_by_xpath('//*[@id="credit_card_month"]').send_keys(user['card_month'])
                    browser.find_element_by_xpath('//*[@id="credit_card_year"]').send_keys(user['card_year'])

                    card_cvv_input = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="vval"]')))
                    card_cvv_input.send_keys(user['card_cvv'])

                    # process payment

                    # confirmation
                    browser.find_element_by_xpath(
                        '/html/body/div[2]/div[1]/form/div[2]/div[2]/fieldset/p/label/div/ins').click()

                    process_payment = browser.find_element_by_css_selector('input.checkout')
                    process_payment.click()
                    time.sleep(10)


            except StaleElementReferenceException:
                pass

if __name__ == '__main__':
    main()