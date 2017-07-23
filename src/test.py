import sys
import ctypes
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QPoint
from CentralWidget import CentralWidget
from MenuBar import MenuBar


class MainWindowTest(QMainWindow):
    def __init__(self):
        user32 = ctypes.windll.user32
        super().__init__()
        self.setWindowTitle('Twitch chat')



        self.show()

    def getPopUpPosition(self, x, y):
        pos = self.mapToGlobal(QPoint(self.width/2, self.height/2))
        pos -= QPoint(x / 2, y / 2)
        return pos


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindowTest()
    sys.exit(app.exec_())
