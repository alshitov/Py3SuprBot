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
        self.setGeometry(2500, 100, 1186, 875)
        self.setLayout(vertbox)
        self.setFixedWidth(1186)
        self.setWindowTitle('PySupBot')

        self.setWindowIcon(QIcon(self.scriptDir + os.path.sep + 'supr.png'))
        self.show()

        self.setStyleSheet("""

            QPushButton:hover {
                background-color: red;
                color: white;
                outline: none
            }
        """)

    def createItemModalWindow(self, args):
        win = NewItemModalWindow(args)


    def create_table(self):
        images_path = self.scriptDir + '/TempPNGS'
        for i in range(6):
            for j in range(5):
                img_name = str(i) + str(j) + '.png'
                if img_name in os.listdir(images_path):
                    btn = QPushButton()
                    btn.setIcon(QIcon('TempPNGS/' + img_name))
                    btn.setIconSize(QSize(200, 200))
                    self.field_layout.addWidget(btn, i, j)
                    argsz = [img_name]
                    self.connect(btn, SIGNAL('clicked()'), lambda: self.createItemModalWindow(argsz))



class NewItemModalWindow(QDialog):
    def __init__(self, args):
        super().__init__()
        print(args)
        self.dialog_window = QDialog(self)

        self.horizbox = QHBoxLayout()

        self.item_image = QLabel()
        self.vertbox = QVBoxLayout()

        self.description = QLabel() # text --> args[2] --> parse from site
        self.color_combo = QComboBox() # options --> args[1] --> parse from site
        self.size_combo = QComboBox()
        self.add_to_cart = QPushButton()

        #            temp options            #
        color_combo_opts = ['Red',
                            'White',
                            'Olive',
                            'Navy',
                            'Black',
                            'Purple']

        size_combo_opts = ['Small',
                           'Medium',
                           'Lagre',
                           'XLarge']
        self.size_combo.addItems(size_combo_opts)
        self.color_combo.addItems(color_combo_opts)

        self.add_to_cart.setText("Add to Cart")

        self.horizbox.addWidget(self.item_image)
        self.horizbox.addLayout(self.vertbox)

        self.vertbox.addWidget(self.description)
        self.vertbox.addWidget(self.color_combo)
        self.vertbox.addWidget(self.size_combo)
        self.vertbox.addWidget(self.add_to_cart)

        self.dialog_window.setLayout(self.horizbox)

        self.dialog_window.setFixedSize(700, 400)
        self.dialog_window.setWindowTitle("Name of item") # args[0] --> name
        self.dialog_window.setModal(True)
        self.dialog_window.exec_()


def mainApp():
    app = QApplication(sys.argv)
    GUI = SupremeApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    mainApp()