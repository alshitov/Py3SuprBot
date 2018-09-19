import sys
from PyQt4.QtGui import *
import supreme_app


def mainApp():
    app = QApplication(sys.argv)
    GUI = supreme_app.SupremeApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    mainApp()