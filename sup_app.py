import os
import sys
from PyQt4 import QtGui, QtCore


class SupremeApp(QtGui.QWidget):

    def __init__(self):
        super(SupremeApp, self).__init__()

        #             buttons               #
        self.init_user_btn = QtGui.QPushButton('Initialize User', self)
        self.cart_btn = QtGui.QPushButton('Cart', self)
        self.sizing_btn = QtGui.QPushButton('Sizing', self)
        self.bot_help_btn = QtGui.QPushButton('Bot Help', self)
        self.start_btn = QtGui.QPushButton('Start Bot', self)

        self.init_user_btn.move(4, 540)
        self.cart_btn.move(207, 540)
        self.sizing_btn.move(410, 540)
        self.bot_help_btn.move(613, 540)
        self.start_btn.move(816, 540)

        self.init_user_btn.setFixedSize(200, 30)
        self.cart_btn.setFixedSize(200, 30)
        self.sizing_btn.setFixedSize(200, 30)
        self.bot_help_btn.setFixedSize(200, 30)
        self.start_btn.setFixedSize(200, 30)

        #           set stylesheet          #
        # self.setStyleSheet("""
        #     QWidget {
        #         background-image: url("supr.png");
        #     }
        #
        #     QPushButton {
        #         background-color: red;
        #         border-radius: 2px;
        #     }
        # """)

        # example for painting image

        # image = QtGui.QLabel(self)
        # image.setGeometry(50, 40, 250, 250)
        # pixmap = QtGui.QPixmap("supr.png")
        # image.setPixmap(pixmap)
        # image.show()

        #           main window           #
        self.setGeometry(2500, 200, 1024, 576) # 169
        self.setFixedSize(1024, 576)
        self.setWindowTitle('PySupBot')
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'supr.png'))
        self.show()


def mainApp():
    app = QtGui.QApplication(sys.argv)
    GUI = SupremeApp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    mainApp()