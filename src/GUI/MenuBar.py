from PyQt5.QtWidgets import QAction, QMenuBar
from SubWindows.JoinChannelDialog import JoinChannelDialog
from SubWindows.SettingDialog import SettingDialog
from SubWindows.BotDialog import BotDialog

class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__()
        self.mainWindow = parent
        self.fileMenu = self.addMenu('&Main')
        self.setUpMainAction()
        self.fileMenu = self.addMenu('&View')
        self.fileMenu = self.addMenu('&Bot')
        self.setUpBotAction()
        self.fileMenu = self.addMenu('&Channels')
        self.setUpChannelAction()
        self.fileMenu = self.addMenu('&Extra')
        self.setUpExtraAction()
        self.bot = self.mainWindow.centralWidget.chatUI.chatScreen.bot


    def setUpMainAction(self):
        settingAction = QAction('&Settings', self)
        settingAction.triggered.connect(self.openSettings)
        self.fileMenu.addAction(settingAction)

    def openSettings(self):
        SettingDialog(self.mainWindow)

    def setUpChannelAction(self):
        joinAction = QAction('&JoinChannel', self)
        joinAction.setShortcut('Ctrl+J')
        joinAction.triggered.connect(self.joinChannel)
        self.fileMenu.addAction(joinAction)

    def setUpBotAction(self):
        botSetting = QAction('&Bot', self)
        #botSetting.triggered.connect(self.joinChannel)
        botSetting.triggered.connect(self.openBotSetting)
        self.fileMenu.addAction(botSetting)

        botOnAndOff = QAction('&Bot Running', self)
        botOnAndOff.setCheckable(True)
        #change later
        botOnAndOff.setChecked(False)
        self.botRunning = botOnAndOff.isChecked()
        botOnAndOff.triggered.connect(self.initializeBot)
        self.fileMenu.addAction(botOnAndOff)

    def setUpExtraAction(self):
        hideMessages = QAction('&Hide Messages', self)
        hideMessages.setCheckable(True)
        hideMessages.setChecked(False)
        hideMessages.triggered.connect(self.toggleMessageButton)
        self.fileMenu.addAction(hideMessages)

    def openBotSetting(self):
        BotDialog(self.mainWindow)

    def toggleMessageButton(self):
        self.mainWindow.centralWidget.chatUI.chatScreen.hideMessage()

    def initializeBot(self):
        self.botRunning = not self.botRunning
        if self.botRunning:
            self.bot.startBot()
        else:
            self.bot.shutDownBot()

    def joinChannel(self):
        JoinChannelDialog(self.mainWindow.centralWidget.chatUI)
        #self.mainWindow.centralWidget.chatUI.joinChannel()
