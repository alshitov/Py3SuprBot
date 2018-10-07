import os
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json
import time


def get_buy_list():
    with open('items_to_buy.json', mode='r') as fout:
        return json.load(fout)


def start_session():
    options = Options()
    # options.headless = True
    BINARY = os.path.dirname(os.path.realpath(__file__)) + '/chromedriver'
    browser = Chrome(BINARY)
    return browser


def main():
    buy_list = get_buy_list()
    for index, item in enumerate(buy_list):
        print("Item {}:".format(index))
        for opt in item:
            if opt != 'image':
                print(opt, '-', item[opt])

    browser = start_session()
    market_url = 'https://supremenewyork.com/shop/all'
    browser.get(market_url)



if __name__ == '__main__':
    main()