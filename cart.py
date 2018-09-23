from PyQt4.QtGui import *
from PyQt4.QtCore import *

import json


class Cart(QDialog):
    def __init__(self):
        super().__init__()
        self.cart_window = QDialog()
        self.layout = QVBoxLayout()

        self.count_label = QLabel()
        self.subtotal_label = QLabel()

        self.count_label.setText('{} items in your basket.'.format(self.count_of_items()))
        self.subtotal_label.setText('subtotal: €{}'.format(self.subtotal_count()))

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

        self.items_list = QTableWidget()
        self.items_list.setFixedSize(665, 150)
        self.items_list_layout.addWidget(self.items_list)

        self.items_list.setColumnCount(5)
        self.items_list.setRowCount(len(items[0]))

        for i in range(len(items)):
            for index, key in enumerate(items[i]):
                self.items_list.setItem(i, index, QTableWidgetItem(items[i][key]))

        self.items_list.setFixedSize(665, 150)
        self.items_list_layout.addWidget(self.items_list)


    def count_of_items(self):
        with open("items_to_buy.json", mode='r', encoding='utf-8') as fout:
            return len(json.load(fout))


    def subtotal_count(self):
        with open("items_to_buy.json", mode='r', encoding='utf-8') as fout:
            return sum(int(item['price']) for item in json.load(fout))


