import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import json


#TODO: regroup table after deleting item


class Cart(QDialog):
    def __init__(self):
        super().__init__()
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.cart_window = QDialog()
        self.layout = QVBoxLayout()

        self.count_label = QLabel()
        self.subtotal_label = QLabel()

        self.count_of_items()
        self.subtotal_count()

        self.items_list_layout = QVBoxLayout()
        self.items_list_layout.setContentsMargins(5, 5, 5, 5)

        self.build_table()

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
        self.cart_window.setFixedSize(850, 550)
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
            self.item_details_label.setText(item['name'] + '\n' +item['color'] + '\n' + item['size'])
            self.item_remove_button.setText('Remove')

            self.connect(self.item_remove_button,
                         SIGNAL('clicked()'),
                         lambda: self.remove_item(item, items.index(item)))

            self.item_price_label.setText(str(item['price']))

            self.item_box.setLayout(self.item_layout)
            self.items_list_layout.addWidget(self.item_box)


    def count_of_items(self):
        with open("items_to_buy.json", mode='r', encoding='utf-8') as fout:
            self.count_label.setText('{} items in your basket.'.format(len(json.load(fout))))


    def subtotal_count(self):
        with open("items_to_buy.json", mode='r', encoding='utf-8') as fout:
            self.subtotal_label.setText('subtotal: €{}'.format(sum(int(item['price']) for item in json.load(fout))))


    def remove_item(self, item, index):
        self.items_list_layout.itemAt(index).widget().deleteLater()

        with open("items_to_buy.json", mode='r', encoding='utf-8') as fout:
            feeds = json.load(fout)

        for feed in feeds:
            if feed['name'] == item['name'] \
                and feed['size'] == item['size'] \
                and feed['color'] == item['color'] \
                and feed['price'] == item['price']:
                feeds.remove(feed)

        with open("items_to_buy.json", mode='w', encoding='utf-8') as fin:
            json.dump(feeds, fin, ensure_ascii=False)

        self.count_of_items()
        self.subtotal_count()

