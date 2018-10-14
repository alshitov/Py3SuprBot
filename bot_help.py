import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class BotHelpWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.bot_help_window = QDialog()
        self.layout = QVBoxLayout()

        self.info_list_layout = QVBoxLayout()
        self.info_list_layout.setContentsMargins(10, 5, 5, 5)
        self.info_list_layout.setAlignment(Qt.AlignTop)

        # creating buttons
        self.info_button_1 = QPushButton("How to choose colors?")
        self.info_button_2 = QPushButton("How to choose sizings?")
        self.info_button_3 = QPushButton("How to manage users?")
        self.info_button_4 = QPushButton("Work with cart")
        self.info_button_5 = QPushButton("Info5")

        '''        if arguments['type'] == 'shoes':
            sizes = ['US 9 / UK 8', 'US 9.5 / UK 8.5',
                     'US 10 / UK 9', 'US 10.5 / UK 9.5',
                     'US 11 / UK 10', 'US 11.5 / UK 10.5',
                     'US 12 / UK 11', 'US 13 / UK 12']
        elif arguments['type'] == 'hats':
            sizes = ['S/M', 'M/L']
        elif arguments['type'] == 'bags':
            self.size_combo.setVisible(False)
        else:
            sizes = ['30', '32','34', '36', 'Small', 'Medium', 'Lagre', 'XLarge']'''

        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignHCenter)
        self.logo_label.setPixmap(QPixmap(self.scriptDir + '/img/logos/help.png'))
        self.layout.addWidget(self.logo_label)

        # text infos
        how_to_colors = '\n'.join(['When filling in "Choose color" field, you have the following options:\n' ,
                                  'Color_1, Color_2, ... \t= Include(add) colors to list. Priority by index in list.',
                                  '!Color \t\t\t= Exclude(forbid) particular color.',
                                  'Any \t\t\t= Choose first available color.'
                                   ])

        how_to_users = '\n'.join(['When choosing/adding user:\n',
                                  '1. Steps to define your billing information (only if you have not done it earlier):',
                                  '    - fill in every field',
                                  '    - press "Accept and Save"',
                                  '    - your data will be written into json file named as Your_Name',
                                  '2. Press "Cancel" to close window.',
                                  '3. Choose your name from the saved users list and press "Load" to check if your billing information is correct.',
                                  '    3.1. Make corrections and press "Accept And Save" if your have changed some piece of data.',
                                  '           Information will be overwritten.',
                                  '4. Choose your name from the saved users list and press "Delete" to remove your billing information.'
                                  ])

        how_to_sizes = '\n'.join(['First, go to Sizing Help and examine individual Supreme sizings on item you are interested in.',
                                  '\nWhen filling in "Choose size" field, you have the following options same as "Choose color" options:\n',
                                  'Size_1, Size_2, ... \t\t= Include(add) sizes to list. Priority by index in list.',
                                  '!Size \t\t\t= Exclude(forbid) particular size.',
                                  'Any \t\t\t= Choose first available size.'
                                  ])
        # pref_sizes
        # Any - bot selects first size in a list (which is actually the smallest available one)
        # Small - particular
        # Medium - particular
        # Large - particular
        # XLarge - particular
        # Biggest - bot selects the biggest available size in a list

        how_to_cart = '\n'.join(['1. Press "Delete" button to delete item from basket.',
                                 '2. Specify items priority by choosing the corresponding index in dropdown list next to price label. '
                                 'Then click "Remember Choice" to remember priorities.'])

        self.info1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod " \
                    "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim " \
                    "veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea " \
                    "commodo consequat. Duis aute irure dolor in reprehenderit in voluptate " \
                    "velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat " \
                    "cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

        # creating labels
        self.info_label_1 = QLabel()
        self.info_label_2 = QLabel()
        self.info_label_3 = QLabel()
        self.info_label_4 = QLabel()
        self.info_label_5 = QLabel()

        # setting line breaks
        self.info_label_1.setWordWrap(True)
        self.info_label_2.setWordWrap(True)
        self.info_label_3.setWordWrap(True)
        self.info_label_4.setWordWrap(True)
        self.info_label_5.setWordWrap(True)

        self.info_label_1.setFixedHeight(100)
        self.info_label_2.setFixedHeight(180)
        self.info_label_3.setFixedHeight(260)
        self.info_label_4.setFixedHeight(80)
        self.info_label_5.setFixedHeight(100)

        # labels info
        self.info_label_1.setText(how_to_colors)
        self.info_label_2.setText(how_to_sizes)
        self.info_label_3.setText(how_to_users)
        self.info_label_4.setText(how_to_cart)
        self.info_label_5.setText(self.info1)

        # original labels state - non visible
        self.info_label_1.setVisible(False)
        self.info_label_2.setVisible(False)
        self.info_label_3.setVisible(False)
        self.info_label_4.setVisible(False)
        self.info_label_5.setVisible(False)

        # switching labels visibility on button click
        self.connect_buttons()

        # placing elements
        self.info_list_layout.addWidget(self.info_button_1)
        self.info_list_layout.addWidget(self.info_label_1)
        self.info_list_layout.addWidget(self.info_button_2)
        self.info_list_layout.addWidget(self.info_label_2)
        self.info_list_layout.addWidget(self.info_button_3)
        self.info_list_layout.addWidget(self.info_label_3)
        self.info_list_layout.addWidget(self.info_button_4)
        self.info_list_layout.addWidget(self.info_label_4)
        self.info_list_layout.addWidget(self.info_button_5)
        self.info_list_layout.addWidget(self.info_label_5)

        # setting scroll area
        self.area = QWidget()
        self.area.setFixedWidth(680)
        self.area.setFixedHeight(200)
        self.area.setLayout(self.info_list_layout)

        self.scroll_area = QScrollArea()
        # self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setWidget(self.area)

        # adding scroll area to main layout
        self.layout.addWidget(self.scroll_area)

        # window settings
        self.bot_help_window.setLayout(self.layout)
        self.bot_help_window.setFixedSize(730, 450)
        self.bot_help_window.setWindowTitle("Bot Help")
        self.bot_help_window.setModal(True)
        self.bot_help_window.exec_()


    def connect_buttons(self):
        # for every button - switch_visibility argument - corresponding text label
        self.connect(self.info_button_1,
                     SIGNAL('clicked()'),
                     lambda: self.switch_visibility(self.info_label_1))

        self.connect(self.info_button_2,
                     SIGNAL('clicked()'),
                     lambda: self.switch_visibility(self.info_label_2))

        self.connect(self.info_button_3,
                     SIGNAL('clicked()'),
                     lambda: self.switch_visibility(self.info_label_3))

        self.connect(self.info_button_4,
                     SIGNAL('clicked()'),
                     lambda: self.switch_visibility(self.info_label_4))

        self.connect(self.info_button_5,
                     SIGNAL('clicked()'),
                     lambda: self.switch_visibility(self.info_label_5))


    def switch_visibility(self, label):
        # if label visible - make it hidden and visa versa
        if label.isVisible():
            label.setVisible(False)
            self.area.setFixedHeight(self.area.height() - label.height())
        else:
            label.setVisible(True)
            self.area.setFixedHeight(self.area.height() + label.height())