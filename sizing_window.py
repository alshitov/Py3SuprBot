import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from parser import Parser


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

        #      scroll area for tables    #
        self.tables_layout = QVBoxLayout()
        self.tables_layout.setContentsMargins(5, 5, 5, 5)

        self.create_tables()

        self.area = QWidget()
        self.area.setLayout(self.tables_layout)
        self.tables_area = QScrollArea()
        self.tables_area.setWidget(self.area)
        self.tables_area.show()

        #       placing widgets         #
        self.layout.addWidget(self.logo_label)
        self.layout.addWidget(self.current_season_label)
        self.layout.addWidget(self.tables_area)

        #           alignment           #
        self.logo_label.setAlignment(Qt.AlignHCenter)
        self.current_season_label.setAlignment(Qt.AlignHCenter)

        #          widget contents      #
        pixmap = QPixmap('logo.png')
        self.logo_label.setPixmap(pixmap)

        self.dialog_window.setLayout(self.layout)
        self.dialog_window.setFixedSize(720, 450)
        self.dialog_window.setWindowTitle("Supreme Sizing")
        self.dialog_window.setModal(True)
        self.dialog_window.exec_()


    def create_tables(self):
        #    getting contents for tables    #
        self.parser = Parser()
        self.objects = self.parser.parse_sizing_tables()[0]

        self.current_season_label.setText(self.parser.parse_sizing_tables()[1])

        #      creating separate table      #
        for object_ in self.objects:
            self.sizing_table = QTableWidget()
            self.sizing_table.setFixedSize(665, 150)
            self.tables_layout.addWidget(self.sizing_table)

            self.sizing_table.setColumnCount(5)
            self.sizing_table.setRowCount(len(object_['data']))
            self.sizing_table.verticalHeader().hide()

            headers = object_['headers']
            self.sizing_table.setHorizontalHeaderLabels(headers)

            for i in range(len(object_['data'])):
                for j in range(len(object_['data'][i])):
                    self.sizing_table.setItem(i, j, QTableWidgetItem(object_['data'][i][j]))

            self.sizing_table.setColumnWidth(0, 340)
            self.sizing_table.setColumnWidth(1, 80)
            self.sizing_table.setColumnWidth(2, 80)
            self.sizing_table.setColumnWidth(3, 80)
            self.sizing_table.setColumnWidth(4, 80)