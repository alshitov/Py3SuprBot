import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import json


class ItemModalWindow(QDialog):
    def __init__(self, args):
        super().__init__()
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.dialog_window = QDialog(self)
        self.dialog_window.setStyleSheet('font-family: Courier;')
        self.horizbox = QHBoxLayout()
        self.vertbox = QVBoxLayout()

        self.item = {'name': args[0],
                     'colorways': args[1],
                     'description': args[2],
                     'picture': args[3],
                     'price': args[4]}
        #                image              #
        self.item_image = QLabel()
        pixmap = QPixmap(self.scriptDir + '/NewJPGS/' + str(self.item['picture']) + '.jpg')
        self.item_image.setPixmap(pixmap)

        #              description          #
        self.description = QLabel()
        self.description.setWordWrap(True)
        self.description.setFixedSize(300, 360)
        self.description.setText(self.item['description'] + self.item['price'])

        #             button                #
        self.add_to_cart_button = QPushButton()
        self.add_to_cart_button.setText("Add to Cart")

        #            dropdown lists        #
        self.color_combo = QComboBox()
        self.size_combo = QComboBox()
        color_combo_opts = self.item['colorways']
        size_combo_opts = ['Small', 'Medium', 'Lagre', 'XLarge']
        self.size_combo.addItems(size_combo_opts)
        self.color_combo.addItems(color_combo_opts)

        self.connect(self.add_to_cart_button,
                     SIGNAL('clicked()'),
                     lambda: self.add_to_cart())

        #              placing             #
        self.horizbox.addWidget(self.item_image)
        self.horizbox.addLayout(self.vertbox)
        self.vertbox.addWidget(self.description)
        self.vertbox.addWidget(self.color_combo)
        self.vertbox.addWidget(self.size_combo)
        self.vertbox.addWidget(self.add_to_cart_button)
        self.dialog_window.setLayout(self.horizbox)
        self.dialog_window.setFixedSize(850, 550)
        self.dialog_window.setWindowTitle(self.item['name'])
        self.dialog_window.setModal(True)
        self.dialog_window.exec_()

    def add_to_cart(self):
        self.item_to_buy = {'name': self.item['name'],
                            'color': str(self.color_combo.currentText()),
                            'size': str(self.size_combo.currentText()),
                            'image': str(self.item['picture']),
                            'price': 220}

        with open("items_to_buy.json", mode='r', encoding='utf-8') as fout:
            items = json.load(fout)

        print("Before ->", items)

        with open("items_to_buy.json", mode='w', encoding='utf-8') as fin:
            items.append(self.item_to_buy)
            json.dump(items, fin, ensure_ascii=False)

        print("After ->", items)
