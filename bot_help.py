from PyQt4.QtGui import *
from PyQt4.QtCore import *


class BotHelpWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.bot_help_window = QDialog()
        self.layout = QVBoxLayout()

        self.info_list_layout = QVBoxLayout()
        self.info_list_layout.setContentsMargins(5, 5, 5, 5)
        self.info_list_layout.setAlignment(Qt.AlignTop)

        # creating buttons
        self.info_button_1 = QPushButton("Info1")
        self.info_button_2 = QPushButton("Info2")
        self.info_button_3 = QPushButton("Info3")
        self.info_button_4 = QPushButton("Info4")
        self.info_button_5 = QPushButton("Info5")

        # temp
        self.info = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod " \
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
        self.info_label_2.setFixedHeight(100)
        self.info_label_3.setFixedHeight(100)
        self.info_label_4.setFixedHeight(100)
        self.info_label_5.setFixedHeight(100)

        # labels info - temp
        self.info_label_1.setText(self.info)
        self.info_label_2.setText(self.info)
        self.info_label_3.setText(self.info)
        self.info_label_4.setText(self.info)
        self.info_label_5.setText(self.info)

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
        self.bot_help_window.setFixedSize(720, 450)
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