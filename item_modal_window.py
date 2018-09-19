import os
from PyQt4.QtGui import *


class ItemModalWindow(QDialog):
    def __init__(self, args):
        super(ItemModalWindow, self).__init__()
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.dialog_window = QDialog(self)
        self.dialog_window.setStyleSheet('font-family: Courier;')
        self.horizbox = QHBoxLayout()

        self.item_image = QLabel()
        pixmap = QPixmap(self.scriptDir + '/NewJPGS/' + args[3] + '.jpg')
        self.item_image.setPixmap(pixmap)
        self.vertbox = QVBoxLayout()

        self.description = QLabel()
        self.description.setWordWrap(True)
        self.description.setFixedSize(300, 360)
        self.description.setText(args[2])
        # font = QFont()
        # font.setFamily('Courier')
        # self.description.setFont(font)
        self.color_combo = QComboBox()
        self.size_combo = QComboBox()
        self.add_to_cart = QPushButton()
        self.add_to_cart.setText("Add to Cart")

        #            temp options            #
        color_combo_opts = args[1]
        size_combo_opts = ['Small',
                           'Medium',
                           'Lagre',
                           'XLarge']
        self.size_combo.addItems(size_combo_opts)
        self.color_combo.addItems(color_combo_opts)

        self.horizbox.addWidget(self.item_image)
        self.horizbox.addLayout(self.vertbox)

        self.vertbox.addWidget(self.description)
        self.vertbox.addWidget(self.color_combo)
        self.vertbox.addWidget(self.size_combo)
        self.vertbox.addWidget(self.add_to_cart)

        self.dialog_window.setLayout(self.horizbox)

        self.dialog_window.setFixedSize(850, 550)
        self.dialog_window.setWindowTitle(args[0])
        self.dialog_window.setModal(True)
        self.dialog_window.exec_()