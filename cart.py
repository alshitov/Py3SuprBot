from PyQt4.QtGui import *
from PyQt4.QtCore import *

import json


class Cart(QDialog):
    def __init__(self):
        super().__init__()
        self.cart_window = QDialog()
        self.layout = QHBoxLayout()

        self.count_label = QLabel()
        self.subtotal_label = QLabel()

        self.items_list_layout = QVBoxLayout()
        self.items_list_layout.setContentsMargins(5, 5, 5, 5)

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

        self.build_table()

        self.cart_window.setLayout(self.layout)
        self.cart_window.setFixedSize(850, 550)
        self.cart_window.setWindowTitle("Cart")
        self.cart_window.setModal(True)
        self.cart_window.exec_()


    def build_table(self):
        with open("items_to_buy.json", mode='r', encoding='utf-8') as fout:
            items = json.load(fout)

        print(items[0]['name'])

        self.items_list = QTableWidget()
        self.items_list.setFixedSize(665, 150)
        self.items_list_layout.addWidget(self.items_list)

        self.items_list.setColumnCount(4)
        self.items_list.setRowCount(len(items[0]))

        for index, item in enumerate(items):
            self.items_list.setItem(index, 0, QTableWidgetItem(items[index]['color']))

        self.items_list.setFixedSize(665, 150)
        self.items_list_layout.addWidget(self.items_list)
