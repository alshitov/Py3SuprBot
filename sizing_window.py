import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class SizingHelpModalWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.dialog_window = QDialog(self)
        self.dialog_window.setStyleSheet('font-family: Courier;')
        self.layout = QVBoxLayout()

        #       information fields      #
        self.logo_label = QLabel()
        self.current_season_label = QLabel()
        self.sizing_table = QTableWidget()

        #       placing widgets         #
        self.layout.addWidget(self.logo_label)
        self.layout.addWidget(self.current_season_label)
        self.layout.addWidget(self.sizing_table)

        #      configuring table        #
        self.sizing_table.setColumnCount(5)
        self.sizing_table.setRowCount(50)
        self.sizing_table.verticalHeader().hide()

        headers = ['Item / Measure', 'S', 'M', 'L', 'XL']

        self.sizing_table.setHorizontalHeaderLabels(headers)
        self.sizing_table.setColumnWidth(0, 335)
        self.sizing_table.setColumnWidth(1, 80)
        self.sizing_table.setColumnWidth(2, 80)
        self.sizing_table.setColumnWidth(3, 80)
        self.sizing_table.setColumnWidth(4, 80)

        #           alignment           #
        self.logo_label.setAlignment(Qt.AlignHCenter)
        self.current_season_label.setAlignment(Qt.AlignHCenter)

        #          widget contents      #
        pixmap = QPixmap('logo.png')
        self.logo_label.setPixmap(pixmap)
        self.current_season_label.setText('Fall/Winter 2018 Sizing')
        # for table - parse items info from https://www.supremenewyork.com/shop/sizing

        self.dialog_window.setLayout(self.layout)
        self.dialog_window.setFixedSize(700, 450)
        self.dialog_window.setWindowTitle("Supreme Sizing")
        self.dialog_window.setModal(True)
        self.dialog_window.exec_()