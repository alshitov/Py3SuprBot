import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import json
import re


class UserInfoModalWindow(QDialog):
    def __init__(self):
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        super().__init__()
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
        self.users_list_combo = QComboBox()
        self.load_user_button = QPushButton()
        self.delete_user_button = QPushButton()

        #         placing elements in a grid       #
        self.grid.addWidget(self.name_input,         0, 0, 1, 2)
        self.grid.addWidget(self.email_input,        1, 0, 1, 2)
        self.grid.addWidget(self.telephone_input,    2, 0, 1, 2)
        self.grid.addWidget(self.address_input,      3, 0, 1, 1)
        self.grid.addWidget(self.address2_input,     3, 1, 1, 1)
        self.grid.addWidget(self.address3_input,     4, 0, 1, 2)
        self.grid.addWidget(self.city_input,         5, 0, 1, 2)
        self.grid.addWidget(self.postcode_input,     6, 0, 1, 1)
        self.grid.addWidget(self.country_combo,      6, 1, 1, 1)
        self.grid.addWidget(self.card_type_combo,    0, 2, 1, 3)
        self.grid.addWidget(self.card_number_input,  1, 2, 1, 3)
        self.grid.addWidget(self.card_month_combo,   2, 2, 1, 1)
        self.grid.addWidget(self.card_year_combo,    2, 3, 1, 1)
        self.grid.addWidget(self.card_cvv_input,     2, 4, 1, 1)
        self.grid.addWidget(self.cancel_button,      6, 2, 1, 1)
        self.grid.addWidget(self.save_button,        6, 3, 1, 2)
        self.grid.addWidget(self.users_list_combo,   5, 2, 1, 1)
        self.grid.addWidget(self.load_user_button,   5, 3, 1, 1)
        self.grid.addWidget(self.delete_user_button, 5, 4, 1, 1)

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

        self.countries = ['GB', 'NB', 'AT', 'BY', 'BE', 'BG', 'HR', 'CZ', 'DK', 'EE', 'FI',
                          'FR', 'DE', 'GR', 'HU', 'IS', 'IE', 'IT', 'LV', 'LT', 'LU', 'MC',
                          'NL', 'NO', 'PL', 'PT', 'RO', 'RU', 'SK', 'SI', 'ES', 'SE', 'CH', 'TR']
        self.country_combo.addItems(self.countries)
        self.cards = ['Visa', 'American Express', 'Mastercard', 'Solo', 'PayPal']
        self.card_type_combo.addItems(self.cards)
        self.months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        self.card_month_combo.addItems(self.months)
        self.years = ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028']
        self.card_year_combo.addItems(self.years)

        self.cancel_button.setText('Cancel')
        self.save_button.setText('Accept And Save')
        self.load_user_button.setText('Load')
        self.delete_user_button.setText('Delete')
        self.delete_user_icon = QIcon(self.scriptDir + '/delete.png')
        self.delete_user_icon_size = QSize(20, 20)
        self.delete_user_button.setIcon(self.delete_user_icon)
        self.delete_user_button.setIconSize(self.delete_user_icon_size)

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
        self.connect(self.delete_user_button,
                     SIGNAL('clicked()'),
                     lambda: self.warning("delete"))

        self.connect(self.load_user_button,
                     SIGNAL('clicked()'),
                     lambda: self.insert_user_info())

        self.connect(self.cancel_button,
                     SIGNAL('clicked()'),
                     lambda: self.warning("close"))

        self.connect(self.save_button,
                     SIGNAL('clicked()'),
                     lambda: self.save_user_info())

        self.load_users_list()

        self.dialog_window.setLayout(self.grid)
        self.dialog_window.setFixedSize(656, 369)
        self.dialog_window.setWindowTitle("User billing information")
        self.dialog_window.setModal(True)
        self.dialog_window.exec_()


    def warning(self, option):
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
        self.accept_dialog.setModal(True)

        if option == "close":
            self.connect(self.accept_button,
                         SIGNAL('clicked()'),
                         lambda: self.quit())

        elif option == "delete":
            self.connect(self.accept_button,
                         SIGNAL('clicked()'),
                         lambda: self.delete_user())

        self.connect(self.cancel_button,
                     SIGNAL('clicked()'),
                     self.accept_dialog.close)
        self.accept_dialog.exec_()


    def quit(self):
        self.accept_dialog.close()
        self.dialog_window.close()


    def save_user_info(self):
        user = {
            'name': str(self.name_input.text()),
            'email': str(self.email_input.text()),
            'tel': str(self.telephone_input.text()),
            'address': str(self.address_input.text()),
            'address2': str(self.address2_input.text()),
            'address3': str(self.address3_input.text()),
            'city': str(self.city_input.text()),
            'postcode': str(self.postcode_input.text()),
            'country': str(self.country_combo.currentText()),
            'card_type': str(self.card_type_combo.currentText()),
            'card_number': str(self.card_number_input.text()),
            'card_month': str(self.card_month_combo.currentText()),
            'card_year': str(self.card_year_combo.currentText()),
            'card_cvv': str(self.card_cvv_input.text())
        }

        if any(user[field] == '' for field in user):
            print('Input Error!')
        else:
            dump_name = 'user_' + '_'.join(user['name'].split(' ')) + '.json'
            with open(dump_name, mode='w', encoding='utf-8') as f:
                json.dump(user, f)
            self.dialog_window.close()


    def load_users_list(self):
        files = os.listdir(self.scriptDir)
        users = [file[5:-5]
                 for file in files if re.search('user_(.*?).json', file)]
        self.users_list_combo.addItems(users)


    def insert_user_info(self):
        user = self.users_list_combo.currentText()
        try:
            with open('user_' + user + '.json', mode='r') as fout:
                user_data = json.load(fout)
                self.name_input.setText(user_data['name'])
                self.email_input.setText(user_data['email'])
                self.telephone_input.setText(user_data['tel'])
                self.address_input.setText(user_data['address'])
                self.address2_input.setText(user_data['address2'])
                self.address3_input.setText(user_data['address3'])
                self.city_input.setText(user_data['city'])
                self.postcode_input.setText(user_data['postcode'])
                self.country_combo.setCurrentIndex(self.countries.index(user_data['country']))
                self.card_type_combo.setCurrentIndex(self.cards.index(user_data['card_type']))
                self.card_number_input.setText(user_data['card_number'])
                self.card_month_combo.setCurrentIndex(self.months.index(user_data['card_month']))
                self.card_year_combo.setCurrentIndex(self.years.index(user_data['card_year']))
                self.card_cvv_input.setText(user_data['card_cvv'])
        except FileNotFoundError:
            print("No user selected!")


    def delete_user(self):
        user = self.users_list_combo.currentText()
        try:
            os.remove(self.scriptDir + '/user_' + user + '.json')
            print("User", user, "deleted!")
            all_items = [self.users_list_combo.itemText(i) for i in range(self.users_list_combo.count())]
            self.users_list_combo.removeItem(all_items.index(user))
            #      clearing fields      #
            self.accept_dialog.close()
            self.name_input.clear()
            self.email_input.clear()
            self.telephone_input.clear()
            self.address_input.clear()
            self.address2_input.clear()
            self.address3_input.clear()
            self.city_input.clear()
            self.postcode_input.clear()
            self.country_combo.clear()
            self.card_type_combo.clear()
            self.card_number_input.clear()
            self.card_month_combo.clear()
            self.card_year_combo.clear()
            self.card_cvv_input.clear()
        except FileNotFoundError:
            print("No user selected!")