import os
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class SupremeApp(QWidget):

    def __init__(self):
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        super(SupremeApp, self).__init__()
        horizbox = QHBoxLayout()
        vertbox = QVBoxLayout()

        #             buttons               #
        self.init_user_btn = QPushButton('Initialize User', self)
        self.cart_btn = QPushButton('Cart', self)
        self.sizing_btn = QPushButton('Sizing', self)
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
        self.setGeometry(2500, 100, 1086, 875)
        self.setLayout(vertbox)
        self.setFixedWidth(1086)
        self.setWindowTitle('PySupBot')

        self.setWindowIcon(QIcon(self.scriptDir + os.path.sep + 'supr.png'))
        self.show()


    def create_table(self):
        images_path = self.scriptDir + '/TempPNGS'
        for i in range(6):
            for j in range(5):
                img_name = str(i) + str(j) + '.png'
                print(img_name)
                if img_name in os.listdir(images_path):
                    cell = QLabel(self)
                    pixmap = QPixmap('TempPNGS/' + img_name)
                    cell.setPixmap(pixmap)
                    self.field_layout.addWidget(cell, i, j)


def mainApp():
    app = QApplication(sys.argv)
    GUI = SupremeApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    mainApp()