import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import json


class Cart(QDialog):
    def __init__(self):
        super().__init__()
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.cart_window = QDialog()
        self.layout = QVBoxLayout()

        self.count_label = QLabel()
        self.subtotal_label = QLabel()

        self.cart_counter()

        self.items_list_layout = QVBoxLayout()
        self.items_list_layout.setContentsMargins(5, 5, 5, 5)
        self.items_list_layout.setAlignment(Qt.AlignTop)

        self.build_table()
        self.connect_buttons()

        self.area = QWidget()
        self.area.setLayout(self.items_list_layout)
        self.items_area = QScrollArea()
        self.items_area.setWidget(self.area)
        self.items_area.show()

        self.layout.addWidget(self.count_label)
        self.layout.addWidget(self.items_area)
        self.layout.addWidget(self.subtotal_label)

        self.count_label.setAlignment(Qt.AlignHCenter)
        self.subtotal_label.setAlignment(Qt.AlignHCenter)

        self.cart_window.setLayout(self.layout)
        self.cart_window.setFixedSize(900, 550)
        self.cart_window.setWindowTitle("Cart")
        self.cart_window.setModal(True)
        self.cart_window.exec_()


    def build_table(self):
        with open("items_to_buy.json", mode='r', encoding='utf-8') as fout:
            items = json.load(fout)

        for item in items:
            self.item_box = QWidget()
            self.item_layout = QHBoxLayout()

            self.item_image_label = QLabel()
            self.item_details_label = QLabel()
            self.item_remove_button = QPushButton()
            self.item_price_label = QLabel()

            self.item_layout.addWidget(self.item_image_label)
            self.item_layout.addWidget(self.item_details_label)
            self.item_layout.addWidget(self.item_remove_button)
            self.item_layout.addWidget(self.item_price_label)

            pixmap = QPixmap(self.scriptDir + '/TempPNGS/' + item['image'] + '.png')
            self.item_image_label.setPixmap(pixmap)
            self.item_details_label.setText(item['name'] + '\nStyle: ' + item['color'] + '\nSize: ' + item['size'])
            self.item_remove_button.setText('Remove')
            self.item_price_label.setText('Price: ' + str(item['price']))

            self.item_box.setLayout(self.item_layout)
            self.item_box.setFixedHeight(200)
            self.items_list_layout.addWidget(self.item_box)


    def cart_counter(self):
        with open("items_to_buy.json", mode='r', encoding='utf-8') as fout:
            items_to_buy = json.load(fout)

            self.count_label.setText('{} items in your basket.'.format(len(items_to_buy)))
            self.subtotal_label.setText('subtotal: €{}'.format(sum(int(item['price']) for item in items_to_buy)))


    def connect_buttons(self):
        buttons = [self.items_list_layout.itemAt(index).widget().children()[3]
                   for index in range(self.items_list_layout.count())]
        for button in buttons:
            self.conn(button)


    def conn(self, btn):
        self.connect(btn,
                     SIGNAL('clicked()'),
                     lambda: self.remove_item(btn))


    def remove_item(self, btn):
        btn.parent().deleteLater()
        with open("items_to_buy.json", mode='r', encoding='utf-8') as fout:
            feeds = json.load(fout)

        item = btn.parent().children()[2].text().split('\n')

        for feed in feeds:
            if feed['name'] == item[0]\
                    and feed['size'] == item[2].split(': ')[1]\
                    and feed['color'] == item[1].split(': ')[1]:
                feeds.remove(feed)
            else: continue

        with open("items_to_buy.json", mode='w', encoding='utf-8') as fin:
            json.dump(feeds, fin, ensure_ascii=False)