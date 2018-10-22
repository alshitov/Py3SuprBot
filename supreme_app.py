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


#TODO: create droplists combobox

class SupremeApp(QWidget):
    def __init__(self):
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.parser_ = Parser()

        super(SupremeApp, self).__init__()
        horizbox = QHBoxLayout()
        vertbox = QVBoxLayout()

        #             buttons               #
        self.change_droplist = QComboBox()
        self.change_droplist.addItems(['16th August 18', '20th August 18', '30th August 18',
                                       '6th September 18', '13th September 18', '20th September 18',
                                       '27th September 18', '4th October 18', '11th October 18',
                                       '18th October 18'])
        self.change_droplist.setObjectName('droplists_box')
        self.change_droplist.setFixedSize(200, 30)

        self.init_user_btn = QPushButton('User Actions', self)
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

        self.init_user_btn.setProperty('class', 'custom_button')
        self.cart_btn.setProperty('class', 'custom_button')
        self.sizing_btn.setProperty('class', 'custom_button')
        self.bot_help_btn.setProperty('class', 'custom_button')
        self.start_btn.setProperty('class', 'custom_button')

        self.init_user_btn.setCursor(Qt.PointingHandCursor)
        self.cart_btn.setCursor(Qt.PointingHandCursor)
        self.sizing_btn.setCursor(Qt.PointingHandCursor)
        self.bot_help_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.setCursor(Qt.PointingHandCursor)

        #            items field            #
        self.field_layout = QGridLayout()

        # creating main window table with items
        self.create_table()

        area = QWidget()
        area.setProperty('class', 'scroll_area')
        area.setLayout(self.field_layout)
        self.items_field = QScrollArea()
        self.items_field.setWidget(area)
        self.items_field.show()

        vertbox.addWidget(self.change_droplist)
        vertbox.addWidget(self.items_field)
        vertbox.addLayout(horizbox)

        #           main window           #
        self.setLayout(vertbox)
        self.setProperty('id', 'main_window')
        self.setFixedWidth(1200)
        self.setGeometry(0,0,0,675)
        self.center()
        self.setWindowTitle('Py3SuprBot')

        self.setWindowIcon(QIcon(self.scriptDir + os.path.sep + 'img/logos/custom_logo.png'))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.show()


    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


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
        # parse_main_window_content() method first checks if latest drop has been changed
        # to do that, method finds a link to the latest droplist and compares it with a link that is saved in 'latest.txt'
        # if links differ, it parses droplist from community and saves it to json dump
        # also it writes down last used link to 'latest.txt'

        print('Checking for drop updates. Please, be patient!')
        # self.parser_.parse_main_window_content()

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
            btn.setProperty('class', 'item_button')
            btn.setCursor(Qt.PointingHandCursor)

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

    def refresh_droplists(self):
        pass