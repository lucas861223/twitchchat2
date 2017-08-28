from PyQt5.QtWidgets import QAction, QMenuBar
from SubWindows.JoinChannelDialog import JoinChannelDialog
from SubWindows.SettingDialog import SettingDialog
from SubWindows.BotDialog import BotDialog

class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__()
        self.mainWindow = parent
        fileMenu = self.addMenu('&Main')
        self.setUpMainAction(fileMenu)
        fileMenu = self.addMenu('&View')
        fileMenu = self.addMenu('&Bot')
        self.setUpBotAction(fileMenu)
        fileMenu = self.addMenu('&Channels')
        self.setUpChannelAction(fileMenu)
        fileMenu = self.addMenu('&Extra')


    def setUpMainAction(self, fileMenu):
        settingAction = QAction('&Settings', self)
        settingAction.triggered.connect(self.openSettings)
        fileMenu.addAction(settingAction)

    def openSettings(self):
        SettingDialog(self.mainWindow)

    def setUpChannelAction(self, fileMenu):
        joinAction = QAction('&JoinChannel', self)
        joinAction.setShortcut('Ctrl+J')
        joinAction.triggered.connect(self.joinChannel)
        fileMenu.addAction(joinAction)

    def setUpBotAction(self, fileMenu):
        botSetting = QAction('&Bot', self)
        #botSetting.triggered.connect(self.joinChannel)
        botSetting.triggered.connect(self.openBotSetting)
        fileMenu.addAction(botSetting)

        botOnAndOff = QAction('&Bot Running', self)
        botOnAndOff.setCheckable(True)
        #change later
        botOnAndOff.setChecked(False)
        self.botRunning = botOnAndOff.isChecked()
        botOnAndOff.triggered.connect(self.initializeBot)
        fileMenu.addAction(botOnAndOff)

    def openBotSetting(self):
        BotDialog(self.mainWindow)

    def initializeBot(self):
        self.botRunning = not self.botRunning

        if self.botRunning:
            print("test?!")
        else:
            print("okay")

    def joinChannel(self):
        JoinChannelDialog(self.mainWindow.centralWidget.chatUI)
        #self.mainWindow.centralWidget.chatUI.joinChannel()
