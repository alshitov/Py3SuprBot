import os
import json
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from user_input_modal_window import UserInfoModalWindow
from item_modal_window import ItemModalWindow
from sizing_window import SizingHelpModalWindow
from cart import Cart
from parser import Parser
from bot_help import BotHelpWindow
from bot import BotWindow


class SupremeApp(QWidget):
    def __init__(self):
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        super(SupremeApp, self).__init__()
        horizbox = QHBoxLayout()
        vertbox = QVBoxLayout()

        #             buttons               #
        self.init_user_btn = QPushButton('Users Actions', self)
        self.connect(self.init_user_btn,
                     SIGNAL('clicked()'),
                     lambda: self.create_user_info_modal_window())

        self.cart_btn = QPushButton('Cart', self)
        self.connect(self.cart_btn,
                     SIGNAL('clicked()'),
                     lambda: self.create_cart_window())

        self.sizing_btn = QPushButton('Sizing Help', self)
        self.connect(self.sizing_btn,
                     SIGNAL('clicked()'),
                     lambda: self.create_sizing_help_window())

        self.bot_help_btn = QPushButton('Bot Help', self)
        self.connect(self.bot_help_btn,
                     SIGNAL('clicked()'),
                     lambda: self.create_bot_help_window())

        self.start_btn = QPushButton('Start Bot', self)
        self.connect(self.start_btn,
                     SIGNAL('clicked()'),
                     lambda: self.start_bot())

        horizbox.addWidget(self.init_user_btn)
        horizbox.addWidget(self.cart_btn)
        horizbox.addWidget(self.sizing_btn)
        horizbox.addWidget(self.bot_help_btn)
        horizbox.addWidget(self.start_btn)

        #            items field            #
        self.field_layout = QGridLayout()

        # creating main window table with items
        self.create_table()

        area = QWidget()
        area.setLayout(self.field_layout)
        self.items_field = QScrollArea()
        self.items_field.setWidget(area)
        self.items_field.show()
        vertbox.addWidget(self.items_field)
        vertbox.addLayout(horizbox)

        #           main window           #
        self.setGeometry(2500, 100, 0, 675)
        self.setLayout(vertbox)
        self.setFixedWidth(1200)
        self.setWindowTitle('Py3SuprBot')

        self.setWindowIcon(QIcon(self.scriptDir + os.path.sep + 'img/logos/custom_logo.png'))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.show()


    def create_item_modal_window(self, args):
        window_modal = ItemModalWindow(args)


    def create_user_info_modal_window(self):
        user_window = UserInfoModalWindow()


    def create_sizing_help_window(self):
        sizing_window = SizingHelpModalWindow()


    def create_cart_window(self):
        cart_window = Cart()


    def create_bot_help_window(self):
        help_window = BotHelpWindow()


    def start_bot(self):
        bot_window = BotWindow()


    def create_table(self):
        # initializing parser
        parser_ = Parser()

        # parse_main_window_content() method first checks if latest drop has been changed
        # to do that, method finds a link to the latest droplist and compares it with a link that is saved in 'latest.txt'
        # if links differ, it parses droplist from community and saves it to json dump
        # also it writes down last used link to 'latest.txt'

        print('Checking for drop updates. Please, be patient!')
        # parser_.parse_main_window_content()

        # reading content from dump
        with open('json/current_drop.json', mode='r') as fin:
            self.drop = json.load(fin)

        # building table
        row = 0
        column = 0

        for index, item in enumerate(self.drop):
            # btn = QPushButton(item['name'])
            btn = QPushButton()
            btn.setIcon(QIcon('img/main/' + str(index)))
            btn.setIconSize(QSize(200, 200))

            self.field_layout.addWidget(btn, row, column)
            if column == 4:
                column = 0
                row += 1
            else:
                column += 1

        self.connect_buttons()


    def connect_buttons(self):
        buttons = [self.field_layout.itemAt(index).widget()
                   for index in range(self.field_layout.count())]

        for index, button in enumerate(buttons):
            self.conn(index, button)


    def conn(self, index, button):
        self.connect(button,
                     SIGNAL('clicked()'),
                     lambda: self.create_item_modal_window(self.drop[index]))