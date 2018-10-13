import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import supreme_app
from multiprocessing import Pool


class MySplashScreen(QSplashScreen):
    def __init__(self, animation, flags):
        # run event dispatching in another thread
        QSplashScreen.__init__(self, QPixmap(), flags)
        self.movie = QMovie(animation)
        self.connect(self.movie, SIGNAL('frameChanged(int)'), SLOT('onNextFrame()'))
        self.movie.start()

    @pyqtSlot()
    def onNextFrame(self):
        pixmap = self.movie.currentPixmap()
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())

def longInitialization(arg):
    import time
    time.sleep(0.1)
    return 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = MySplashScreen('img/logos/custom_logo.png', Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()
    initLoop = QEventLoop()
    pool = Pool(processes=1)
    pool.apply_async(longInitialization, [2], callback=lambda exitCode: initLoop.exit(exitCode))
    initLoop.exec_()

    GUI = supreme_app.SupremeApp()
    splash.finish(GUI)

    app.exec_()


































'''import sys
from PyQt4.QtGui import *
import supreme_app


def mainApp():
    app = QApplication(sys.argv)
    GUI = supreme_app.SupremeApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    mainApp()'''