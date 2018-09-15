import os
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class SupremeApp(QWidget):

    def __init__(self):
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

        #            test adding items to table    #
        cell_1 = QLabel(self)
        pixmap = QPixmap('TempPNGS/' + 'new01.png')
        cell_1.setPixmap(pixmap)
        self.field_layout.addWidget(cell_1, 0, 0)
        cell_2 = QLabel(self)
        pixmap = QPixmap('TempPNGS/' + 'new02.png')
        cell_2.setPixmap(pixmap)
        self.field_layout.addWidget(cell_2, 0, 1)

        area = QWidget()
        area.setLayout(self.field_layout)
        self.items_field = QScrollArea()
        self.items_field.setWidget(area)
        self.items_field.show()
        vertbox.addWidget(self.items_field)
        vertbox.addLayout(horizbox)

        #           main window           #
        self.setGeometry(2500, 100, 1040, 875)
        self.setLayout(vertbox)
        self.setFixedWidth(1040)
        self.setWindowTitle('PySupBot')
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(self.scriptDir + os.path.sep + 'supr.png'))
        self.show()
        # self.create_table()

    #        edit method!          #
    def create_table(self):
        images_path = self.scriptDir + '/TempPNGS'
        images = os.listdir(images_path)

        for idx, img in enumerate(images):
            cell = QLabel(self)
            cell.setGeometry(10 + (idx - 1) * 210, 5, 210, 210)
            pixmap = QPixmap('TempPNGS/' + 'new' + str(0) + str(idx) + '.png')
            cell.setPixmap(pixmap)
            self.field_layout.addWidget(cell, idx, idx)



def mainApp():
    app = QApplication(sys.argv)
    GUI = SupremeApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    mainApp()