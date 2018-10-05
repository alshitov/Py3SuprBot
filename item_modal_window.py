import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import json


class ItemModalWindow(QDialog):
    def __init__(self, arguments):
        super().__init__()
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))

        self.dialog_window = QDialog(self)
        # self.dialog_window.setStyleSheet('font-family: Courier;')
        self.horizbox = QHBoxLayout()
        self.vertbox = QVBoxLayout()

        # image
        self.item_image = QLabel()
        pixmap = QPixmap(self.scriptDir + '/img/500px/' + str(arguments['image']))
        self.item_image.setPixmap(pixmap)

        # description
        self.description = QLabel()
        self.description.setWordWrap(True)
        self.description.setFixedSize(300, 360)
        self.description.setText(arguments['description'])

        #             button                #
        self.add_to_cart_button = QPushButton()
        self.add_to_cart_button.setText("Add to Cart")

        #            dropdown lists        #
        self.color_combo = QComboBox()
        self.size_combo = QComboBox()
        self.size_combo.addItems(['Small', 'Medium', 'Lagre', 'XLarge'])
        self.color_combo.addItems(['Black', 'White', 'Yellow']) # temp

        self.connect(self.add_to_cart_button,
                     SIGNAL('clicked()'),
                     lambda: self.add_to_cart(arguments))

        #              placing             #
        self.horizbox.addWidget(self.item_image)
        self.horizbox.addLayout(self.vertbox)
        self.vertbox.addWidget(self.description)
        self.vertbox.addWidget(self.color_combo)
        self.vertbox.addWidget(self.size_combo)
        self.vertbox.addWidget(self.add_to_cart_button)
        self.dialog_window.setLayout(self.horizbox)
        self.dialog_window.setFixedSize(850, 550)
        self.dialog_window.setWindowTitle(arguments['name'])
        self.dialog_window.setModal(True)
        self.dialog_window.exec_()


    def add_to_cart(self, arguments):
        self.item_to_buy = {
            'name': arguments['name'],
            'color': str(self.color_combo.currentText()),
            'size': str(self.size_combo.currentText()),
            'price': arguments['price'],
            'image': arguments['image']
        }

        with open("items_to_buy.json", mode='r', encoding='utf-8') as fout:
            items = json.load(fout)

        with open("items_to_buy.json", mode='w', encoding='utf-8') as fin:
            items.append(self.item_to_buy)
            json.dump(items, fin, ensure_ascii=False)