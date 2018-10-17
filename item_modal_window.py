import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import json


class ItemModalWindow(QDialog):
    def __init__(self, arguments):
        super().__init__()
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))

        self.dialog_window = QDialog(self)
        self.horizbox = QHBoxLayout()
        self.vertbox = QVBoxLayout()

        self.vertbox.setContentsMargins(0, 0, 0, 15)

        # image
        self.item_image = QLabel()
        pixmap = QPixmap(self.scriptDir + '/img/500px/' + str(arguments['image']))
        self.item_image.setPixmap(pixmap)

        # description
        self.description = QLabel()
        self.description.setWordWrap(True)
        self.description.setFixedSize(300, 360)
        self.description.setText('Description: '+ arguments['description'] + \
                                 '\n\nType: ' + arguments['type'] + \
                                 '\n\nPrice: ' + arguments['price'])
        self.description.setContentsMargins(10, 0, 0, 10)

        # button
        self.add_to_cart_button = QPushButton()
        self.add_to_cart_button.setText("Add to Cart")

        # user choose labels
        self.info_color_input = QLabel('<b>Choose color:</b>')
        self.info_size_input = QLabel('<b>Choose size:</b>')
        self.color_input = QLineEdit()
        self.size_input = QLineEdit()
        self.warning = QLabel('')

        text_re = QRegExp("[a-zA-Z \!,]+")

        # color input settings
        self.color_input.setPlaceholderText("E.g.: Black, !Red, Green (*hover for help*)")
        color_input_validator = QRegExpValidator(text_re, self.color_input)
        self.color_input.setValidator(color_input_validator)

        self.color_input.setToolTip('''
        COLORS I FOUND RECENTLY:
        RED SHADES:
            Red, Orange, Yellow, Burgundy, Magenta, Mustard, Pink, Lime, Gold, Cardinal, Brown

        GREEN SHADES:
            Olive, Beige, Clay, Green, Green, Khaki, Green, Woodland Camo, Camo

        BLUE SHADES:
            Navy, Cranberry, Maroon, Blue, Purple, Pink, Blue Denim, Royal, Violet, Plum, Panther, Slate, Cyan

        BLACK/WHITE SHADES:
            Black, Grey, White, Off-White, Ash Grey, Heather Grey, Natural, Teal, Panther, Tan, Multicolor

        COMBINATIONS (+ Color): #### E.g. Dark Purple, Pink Polka Dot, Pale Red etc. ####
            Dark, Light, Dusty, Rust, Bright, Fluorescent, Neon, Washed, Pale, (Color +) Polka Dot;
            
        SEE RULES IN BOT HELP! 
        ''')

        # size combo settings
        self.size_input.setPlaceholderText("E.g.: 32, !XLarge, Small (*hover for help*)")
        size_input_validator = QRegExpValidator(text_re, self.size_input)
        self.size_input.setValidator(size_input_validator)

        self.size_input.setToolTip('Use Sizing Help to check Supreme sizing on current droplist.')

        self.connect(self.add_to_cart_button,
                     SIGNAL('clicked()'),
                     lambda: self.add_to_cart(arguments))

        self.check_limit_per_product(arguments)

        # placing
        self.horizbox.addWidget(self.item_image)
        self.horizbox.addLayout(self.vertbox)
        self.vertbox.addWidget(self.description)
        self.vertbox.addWidget(self.info_color_input)
        self.vertbox.addWidget(self.color_input)
        self.vertbox.addWidget(self.info_size_input)
        self.vertbox.addWidget(self.size_input)
        self.vertbox.addWidget(self.warning)
        self.vertbox.addWidget(self.add_to_cart_button)

        self.dialog_window.setLayout(self.horizbox)
        self.dialog_window.setFixedSize(850, 550)
        self.dialog_window.setWindowTitle(arguments['name'])
        self.dialog_window.setModal(True)
        self.dialog_window.exec_()


    def check_limit_per_product(self, arguments):
        with open('json/items_to_buy.json', mode='r', encoding='utf-8') as f:
            items = json.load(f)

        for item in items:
            if item['name'] == arguments['name']:
                self.warning.setText('Limited to 1 per product')
                self.warning.setStyleSheet('color: red')
                self.add_to_cart_button.setDisabled(True)
        else:
            pass


    def add_to_cart(self, arguments):
        self.item_to_buy = {
            'name': arguments['name'],
            'type': arguments['type'],
            'color': str(self.color_input.text()),
            'size': str(self.size_input.text()),
            'price': arguments['price'],
            'image': arguments['image']
        }

        with open("json/items_to_buy.json", mode='r', encoding='utf-8') as fout:
            items = json.load(fout)

        with open("json/items_to_buy.json", mode='w', encoding='utf-8') as fin:
            items.append(self.item_to_buy)
            json.dump(items, fin, ensure_ascii=False)

        self.dialog_window.close()