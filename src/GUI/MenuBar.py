from PyQt5.QtWidgets import QAction, QMenuBar
from PyQt5.QtGui import QIcon

class MenuBar(QMenuBar):

    def __init__(self, parent):
        super().__init__()
        self.mainWindow = parent
        fileMenu = self.addMenu('&Main')
        fileMenu = self.addMenu('&View')
        fileMenu = self.addMenu('&Bot')
        fileMenu = self.addMenu('&Channels')
        self.setUpChannelAction(fileMenu)
        fileMenu = self.addMenu('&Extra')
        self.setStyleSheet('background: #ffffff')

    def setUpChannelAction(self, fileMenu):
        joinAction = QAction('&JoinChannel', self)
        joinAction.setShortcut('Ctrl+J')
        joinAction.triggered.connect(self.joinChannel)
        fileMenu.addAction(joinAction)

    def joinChannel(self):
        self.mainWindow.centralWidget.chatUI.joinChannel()
