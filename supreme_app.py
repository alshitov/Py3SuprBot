import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from user_input_modal_window import *
from item_modal_window import *


class SupremeApp(QWidget):
    def __init__(self):
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        super(SupremeApp, self).__init__()
        horizbox = QHBoxLayout()
        vertbox = QVBoxLayout()

        #             buttons               #
        self.init_user_btn = QPushButton('Initialize User', self)
        self.connect(self.init_user_btn, SIGNAL('clicked()'),
                     lambda: self.createUserInfoModalWindow())
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
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.show()


    def createItemModalWindow(self, args):
        window_modal = ItemModalWindow(args)


    def createUserInfoModalWindow(self):
        window_modal = UserInfoModalWindow()


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
                    # temp #
                    item_name = 'Supreme®/Comme des Garçons SHIRT® Split Box Logo Tee'
                    colorways = ['White', 'Black', 'Red']
                    descr = 'Description: All cotton crewneck with vertical seam at front and diagonal seam at lower back.'\
                            '\nPrinted logos on front and on back.'\
                            '\nMade exclusively for Supreme.'\
                            '\n\nPrice: 54doll, 48pounds, 54eur, 9720y'
                    image_num = str(i) + str(j)
                    argsz = [item_name, colorways, descr, image_num]
                    self.connect(btn,
                                 SIGNAL('clicked()'),
                                 lambda: self.createItemModalWindow(argsz))