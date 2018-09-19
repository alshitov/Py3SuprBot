import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import json


class UserInfoModalWindow(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.dialog_window = QDialog(self)
        self.dialog_window.setStyleSheet('font-family: Courier;')
        self.grid = QGridLayout()

        #           user input fields            #
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.telephone_input = QLineEdit()
        self.address_input = QLineEdit()
        self.address2_input = QLineEdit()
        self.address3_input = QLineEdit()
        self.city_input = QLineEdit()
        self.postcode_input = QLineEdit()
        self.country_combo = QComboBox()
        self.card_type_combo = QComboBox()
        self.card_number_input = QLineEdit()
        self.card_month_combo = QComboBox()
        self.card_year_combo = QComboBox()
        self.card_cvv_input = QLineEdit()
        self.cancel_button = QPushButton()
        self.save_button = QPushButton()

        #         placing elements in a grid       #
        self.grid.addWidget(self.name_input,        0, 0, 1, 2)
        self.grid.addWidget(self.email_input,       1, 0, 1, 2)
        self.grid.addWidget(self.telephone_input,   2, 0, 1, 2)
        self.grid.addWidget(self.address_input,     3, 0, 1, 1)
        self.grid.addWidget(self.address2_input,    3, 1, 1, 1)
        self.grid.addWidget(self.address3_input,    4, 0, 1, 2)
        self.grid.addWidget(self.city_input,        5, 0, 1, 2)
        self.grid.addWidget(self.postcode_input,    6, 0, 1, 1)
        self.grid.addWidget(self.country_combo,     6, 1, 1, 1)
        self.grid.addWidget(self.card_type_combo,   0, 2, 1, 3)
        self.grid.addWidget(self.card_number_input, 1, 2, 1, 3)
        self.grid.addWidget(self.card_month_combo,  2, 2, 1, 1)
        self.grid.addWidget(self.card_year_combo,   2, 3, 1, 1)
        self.grid.addWidget(self.card_cvv_input,    2, 4, 1, 1)
        self.grid.addWidget(self.cancel_button,     6, 2, 1, 1)
        self.grid.addWidget(self.save_button,       6, 3, 1, 2)

        #        setting parameters for user inputs      #
        self.name_input.setPlaceholderText("Full name")
        self.email_input.setPlaceholderText("E-mail")
        self.telephone_input.setPlaceholderText("Telephone number")
        self.address_input.setPlaceholderText("Address")
        self.address2_input.setPlaceholderText("Address 2")
        self.address3_input.setPlaceholderText("Address 3")
        self.city_input.setPlaceholderText("City")
        self.postcode_input.setPlaceholderText("Postcode")
        self.card_number_input.setPlaceholderText("Card number")
        self.card_cvv_input.setPlaceholderText("CVV")

        self.country_combo.addItems(['GB', 'NB', 'AT', 'BY', 'BE', 'BG', 'HR', 'CZ', 'DK', 'EE', 'FI',
                                     'FR', 'DE', 'GR', 'HU', 'IS', 'IE', 'IT', 'LV', 'LT', 'LU', 'MC',
                                     'NL', 'NO', 'PL', 'PT', 'RO', 'RU', 'SK', 'SI', 'ES', 'SE', 'CH', 'TR'])
        self.card_type_combo.addItems(['Visa', 'American Express', 'Mastercard', 'Solo', 'PayPal'])
        self.card_month_combo.addItems(['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13'])
        self.card_year_combo.addItems(['2018', '2019', '2020', '2021', '2022', '2023',
                                       '2024', '2025', '2026', '2027', '2028'])

        self.cancel_button.setText('Cancel')
        self.save_button.setText('Accept And Save')

        #           setting validators           #
        self.onlyInt = QIntValidator()
        self.onlyLong = QDoubleValidator()

        name_re = QRegExp("[a-zA-Z ]+")
        name_input_validator = QRegExpValidator(name_re, self.name_input)
        self.name_input.setValidator(name_input_validator)

        self.telephone_input.setValidator(self.onlyLong)

        city_re = QRegExp("[a-zA-Z, ]+")
        city_input_validator = QRegExpValidator(city_re, self.city_input)
        self.city_input.setValidator(city_input_validator)

        self.postcode_input.setValidator(self.onlyInt)

        card_number_re = QRegExp("[0-9]{,16}")
        card_number_validator = QRegExpValidator(card_number_re, self.card_cvv_input)
        self.card_number_input.setValidator(card_number_validator)

        card_cvv_re = QRegExp("[0-9]{,3}")
        card_cvv_validator = QRegExpValidator(card_cvv_re, self.card_cvv_input)
        self.card_cvv_input.setValidator(card_cvv_validator)

        #            connecting slots           #
        self.connect(self.cancel_button,
                     SIGNAL('clicked()'),
                     lambda: self.cancel_button_clicked())

        self.connect(self.save_button,
                     SIGNAL('clicked()'),
                     lambda: self.save_user_info())

        self.dialog_window.setLayout(self.grid)
        self.dialog_window.setFixedSize(656, 369)
        self.dialog_window.setWindowTitle("User billing information")
        self.dialog_window.setModal(True)
        self.dialog_window.exec_()


    def cancel_button_clicked(self):
        self.accept_dialog = QDialog()
        self.grid = QGridLayout()
        self.warning_text = QLabel()
        self.accept_button = QPushButton()
        self.cancel_button = QPushButton()

        self.grid.addWidget(self.warning_text, 0, 0, 1, 2)
        self.grid.addWidget(self.accept_button, 1, 1, 1, 1)
        self.grid.addWidget(self.cancel_button, 1, 0, 1, 1)

        self.warning_text.setText('Are you sure? \nInformation will be lost.')
        self.warning_text.setAlignment(Qt.AlignCenter)
        self.accept_button.setText('Accept')
        self.cancel_button.setText('Cancel')

        self.accept_dialog.setLayout(self.grid)
        self.accept_dialog.setFixedSize(250, 150)
        self.accept_dialog.setWindowTitle('Accept action')
        # self.accept_dialog.setModal(True)

        self.connect(self.accept_button,
                     SIGNAL('clicked()'),
                     lambda: self.quit())
        self.connect(self.cancel_button,
                     SIGNAL('clicked()'),
                     self.accept_dialog.close)
        self.accept_dialog.exec_()


    def quit(self):
        self.accept_dialog.close()
        self.dialog_window.close()


    def save_user_info(self):
        user = {}
        user['name'] = str(self.name_input.text())
        user['email'] = str(self.email_input.text())
        user['tel'] = str(self.telephone_input.text())
        user['address'] = str(self.address_input.text())
        user['address2'] = str(self.address2_input.text())
        user['address3'] = str(self.address3_input.text())
        user['city'] = str(self.city_input.text())
        user['postcode'] = str(self.postcode_input.text())
        user['country'] = str(self.country_combo.currentText())
        user['card_type'] = str(self.card_type_combo.currentText())
        user['card_number'] = str(self.card_number_input.text())
        user['card_month'] = str(self.card_month_combo.currentText())
        user['card_year'] = str(self.card_year_combo.currentText())
        user['card_cvv'] = str(self.card_cvv_input.text())

        if any(user[field] == '' for field in user):
            print('Input Error!')
        else:
            dump_name = '_'.join(user['name'].split(' ')) + '.json'
            with open(dump_name, mode='w', encoding='utf-8') as f:
                json.dump(user, f)
            self.dialog_window.close()