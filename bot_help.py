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
        self.info_button_5 = QPushButton("Drop time")

        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignHCenter)
        self.logo_label.setPixmap(QPixmap(self.scriptDir + '/img/logos/help.png'))
        self.layout.addWidget(self.logo_label)

        # text infos
        how_to_colors = '\n'.join(['When filling in "Choose color" field, you have the following options:\n' ,
                                  '▶ Color_1, Color_2, ... \t= Include(add) colors to list. Priority by index in list.',
                                  '▶ Any \t\t\t= Choose first available color.'
                                   ])

        how_to_users = '\n'.join(['▶ When choosing/adding user:\n',
                                  '▶ Steps to define your billing information (only if you have not done it earlier):',
                                  '    - fill in information fields',
                                  '    - press "Accept and Save"',
                                  '    - your data will be saved in json file named as Name_Surname',
                                  '▶ Press "Cancel" to close window.',
                                  '▶ Choose your name from the saved users list and press "Load" to check if your billing information is correct.',
                                  '    3.1. Make corrections and press "Accept And Save" if your have changed some piece of data.',
                                  '           Information will be overwritten.',
                                  '▶ Choose your name from the saved users list and press "Delete" to remove your billing information.'
                                  ])

        how_to_sizes = '\n'.join(['First, go to Sizing Help and examine individual Supreme sizings on item you are interested in.',
                                  '\nWhen filling in "Choose size" field, you have the following options same as "Choose color" options:\n',
                                  '▶ Size_1, Size_2, ... \t\t= Include(add) sizes to list. Priority by index in list.',
                                  '▶ Any \t\t\t= Choose first available size.'
                                  ])

        how_to_cart = '\n'.join(['▶ Press "Delete" button to delete item from basket.',
                                 '▶ Specify items priority by choosing the corresponding index in dropdown list next to price label. '
                                 'Then click "Remember Choice" to remember priorities.'])

        how_to_time = '\n'.join(['▶ When starting the Bot, you are to specify drop time (12-hour format).',
                                 '▶ I recommend setting 1 minute earlier official drop time. '
                                 'The Bot will start refreshing stock every 0.5 sec. and will buy your desired item in time.'])

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
        self.info_label_3.setFixedHeight(270)
        self.info_label_4.setFixedHeight(80)
        self.info_label_5.setFixedHeight(100)

        # labels info
        self.info_label_1.setText(how_to_colors)
        self.info_label_2.setText(how_to_sizes)
        self.info_label_3.setText(how_to_users)
        self.info_label_4.setText(how_to_cart)
        self.info_label_5.setText(how_to_time)

        # original labels state - non visible
        self.info_label_1.setVisible(False)
        self.info_label_2.setVisible(False)
        self.info_label_3.setVisible(False)
        self.info_label_4.setVisible(False)
        self.info_label_5.setVisible(False)

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
        self.area.setProperty('class', 'scroll_area')
        self.area.setFixedWidth(680)
        self.area.setFixedHeight(200)
        self.area.setLayout(self.info_list_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.area)

        # below buttons
        self.horizbox = QHBoxLayout()
        self.settings_button = QPushButton('Settings')
        self.exit_button = QPushButton('Close')

        # adding scroll area to main layout
        self.layout.addWidget(self.scroll_area)
        self.horizbox.addWidget(self.settings_button)
        self.horizbox.addWidget(self.exit_button)

        self.layout.addLayout(self.horizbox)

        # switching labels visibility on button click
        self.connect_buttons()

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

        self.connect(self.exit_button,
                     SIGNAL('clicked()'),
                     lambda: self.bot_help_window.close())

        self.connect(self.settings_button,
                     SIGNAL('clicked()'),
                     lambda: self.cfg())


    def switch_visibility(self, label):
        # if label visible - make it hidden and visa versa
        if label.isVisible():
            label.setVisible(False)
            self.area.setFixedHeight(self.area.height() - label.height())
        else:
            label.setVisible(True)
            self.area.setFixedHeight(self.area.height() + label.height())

    def cfg(self):
        cfg_window = Configuration()


class Configuration(QDialog):
    def __init__(self):
        super().__init__()
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.settings_window = QDialog()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.contents_layout = QVBoxLayout()

        # setting scroll area
        self.area = QWidget()
        self.area.setFixedWidth(280)
        self.area.setFixedHeight(250)
        self.area.setLayout(self.contents_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.area)
        self.layout.addWidget(self.scroll_area)

        self.save_button = QPushButton('Save')
        self.exit_button = QPushButton('Close')

        self.horizbox = QHBoxLayout()
        self.horizbox.addWidget(self.save_button)
        self.horizbox.addWidget(self.exit_button)

        self.layout.addLayout(self.horizbox)

        self.connect_buttons()
        self.settings_window.setLayout(self.layout)
        self.settings_window.setFixedSize(300, 350)
        self.settings_window.setWindowTitle("Bot Config")
        self.settings_window.setModal(True)
        self.settings_window.exec_()

    def connect_buttons(self):

        self.connect(self.exit_button,
                     SIGNAL('clicked()'),
                     lambda: self.settings_window.close())