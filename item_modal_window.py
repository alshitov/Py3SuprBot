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
        self.description.setText('Description: '+ arguments['description'] + \
                                 '\n\nType: ' + arguments['type'] + \
                                 '\n\nPrice: ' + arguments['price'])
        self.description.setContentsMargins(10, 0, 0, 10)

        # button
        self.add_to_cart_button = QPushButton()
        self.add_to_cart_button.setText("Add to Cart")

        # user choose labels
        self.color_input = QLineEdit()
        self.size_combo = QComboBox()

        # size combo settings
        if arguments['type'] == 'shoes':
            self.size_combo.addItems(['US 9 / UK 8', 'US 9.5 / UK 8.5',
                                      'US 10 / UK 9', 'US 10.5 / UK 9.5',
                                      'US 11 / UK 10', 'US 11.5 / UK 10.5',
                                      'US 12 / UK 11', 'US 13 / UK 12'])
        elif arguments['type'] == 'hats' or arguments['type'] == 'bags':
            self.size_combo.setVisible(False)
        elif arguments['type'] == 'pants':
            self.size_combo.addItems(['30', '32','34', '36'])
        else:
            self.size_combo.addItems(['Small', 'Medium', 'Lagre', 'XLarge'])

        self.size_combo.setToolTip('Use Sizing Help to check Supreme sizing on current droplist.')

        # color input settings
        self.color_input.setPlaceholderText("Choose color (hover for help)")
        color_re = QRegExp("[a-zA-Z \!,]+")
        color_input_validator = QRegExpValidator(color_re, self.color_input)
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

        self.connect(self.add_to_cart_button,
                     SIGNAL('clicked()'),
                     lambda: self.add_to_cart(arguments))

        # placing
        self.horizbox.addWidget(self.item_image)
        self.horizbox.addLayout(self.vertbox)
        self.vertbox.addWidget(self.description)
        self.vertbox.addWidget(self.color_input)
        self.vertbox.addWidget(self.size_combo)
        self.vertbox.addWidget(self.add_to_cart_button)
        # self.vertbox.addWidget(self.question_label)

        self.dialog_window.setLayout(self.horizbox)
        self.dialog_window.setFixedSize(850, 550)
        self.dialog_window.setWindowTitle(arguments['name'])
        self.dialog_window.setModal(True)
        self.dialog_window.exec_()


    def add_to_cart(self, arguments):
        self.item_to_buy = {
            'name': arguments['name'],
            'type': arguments['type'],
            'color': str(self.color_input.text()),
            'size': str(self.size_combo.currentText()),
            'price': arguments['price'],
            'image': arguments['image']
        }

        with open("items_to_buy.json", mode='r', encoding='utf-8') as fout:
            items = json.load(fout)

        with open("items_to_buy.json", mode='w', encoding='utf-8') as fin:
            items.append(self.item_to_buy)
            json.dump(items, fin, ensure_ascii=False)

        self.dialog_window.close()