import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import user_input_modal_window
import item_modal_window
import sizing_window
from cart import Cart
import json
from parser import Parser # parse main window content


#TODO: limit items per type when adding to backet

class SupremeApp(QWidget):
    def __init__(self):
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        super(SupremeApp, self).__init__()
        horizbox = QHBoxLayout()
        vertbox = QVBoxLayout()

        #             buttons               #
        self.init_user_btn = QPushButton('Initialize User', self)
        self.connect(self.init_user_btn,
                     SIGNAL('clicked()'),
                     lambda: self.create_user_info_modal_window())

        self.cart_btn = QPushButton('Cart', self)
        self.connect(self.cart_btn,
                     SIGNAL('clicked()'),
                     lambda: self.create_cart_window())

        self.sizing_btn = QPushButton('Sizing', self)

        self.connect(self.sizing_btn,
                     SIGNAL('clicked()'),
                     lambda: self.create_sizing_help_window())

        self.bot_help_btn = QPushButton('Bot Help', self)

        self.start_btn = QPushButton('Start Bot', self)

        horizbox.addWidget(self.init_user_btn)
        horizbox.addWidget(self.cart_btn)
        horizbox.addWidget(self.sizing_btn)
        horizbox.addWidget(self.bot_help_btn)
        horizbox.addWidget(self.start_btn)

        #            items field            #
        self.field_layout = QGridLayout()

        self.create_table()

        area = QWidget()
        area.setLayout(self.field_layout)
        self.items_field = QScrollArea()
        self.items_field.setWidget(area)
        self.items_field.show()
        vertbox.addWidget(self.items_field)
        vertbox.addLayout(horizbox)

        #           main window           #
        self.setGeometry(2500, 100, 1186, 875)
        self.setLayout(vertbox)
        self.setFixedWidth(1186)
        self.setWindowTitle('PySupBot')

        self.setWindowIcon(QIcon(self.scriptDir + os.path.sep + 'logo.png'))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.show()


    def create_item_modal_window(self, args):
        if os.path.isfile(self.scriptDir + "/items_to_buy.json"):
            pass
        else:
            os.system("touch items_to_buy.json")
            with open("items_to_buy.json", mode='r', encoding='utf-8') as f:
                json.dump([], f)

        window_modal = item_modal_window.ItemModalWindow(args)


    def create_user_info_modal_window(self):
        window_modal = user_input_modal_window.UserInfoModalWindow()


    def create_sizing_help_window(self):
        window_modal = sizing_window.SizingHelpModalWindow()


    def create_cart_window(self):
        window_modal = Cart()


    def create_table(self):
        images_path = self.scriptDir + '/TempPNGS'
        for i in range(6):
            for j in range(5):
                img_name = str(i) + str(j) + '.png'
                if img_name in os.listdir(images_path):
                    btn = QPushButton()
                    btn.setIcon(QIcon('TempPNGS/' + img_name))
                    btn.setIconSize(QSize(200, 200))
                    self.field_layout.addWidget(btn, i, j)
                    # temp #
                    item_name = 'Supreme®/Comme des Garçons SHIRT® Split Box Logo Tee'
                    colorways = ['White', 'Black', 'Red']
                    descr = 'Description: All cotton crewneck with vertical seam at front and diagonal seam at lower back.'\
                            '\nPrinted logos on front and on back.'\
                            '\nMade exclusively for Supreme.'
                    price = '\n\nPrice: 54doll, 48pounds, 54eur, 9720y'

                    image_num = str(i) + str(j)
                    argsz = [item_name, colorways, descr, image_num, price]
                    self.connect(btn,
                                 SIGNAL('clicked()'),
                                 lambda: self.create_item_modal_window(argsz))