from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QTreeView, QLineEdit, QGridLayout, QTextEdit, QFileSystemModel
from PyQt5.QtCore import Qt
from pathlib import Path
import os.path
import shutil

class BotDialog(QDialog):
    COMMAND_FOLDER_PATH = str(Path(__file__).parent.parent.parent) + "\\Commands\\"
    def __init__(self, mainWindow):
        super(BotDialog, self).__init__()
        self.file = None
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.mainWindow = mainWindow
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle('Bot Setting')
        layout = QGridLayout()
        self.commandsTreeView = QTreeView()
        self.populateChannelsCommands()
        self.commandsTreeView.setContentsMargins(0, 0, 0, 0)
        self.commandsTreeView.hideColumn(3)
        self.commandsTreeView.hideColumn(2)
        self.commandsTreeView.hideColumn(1)
        layout.addWidget(self.commandsTreeView, 2, 1, 6, 3)
        self.commandsTreeView.setHeaderHidden(True)
        self.commandsTreeView.doubleClicked.connect(self.editCommand)
        addChannelButton = QPushButton("Add Channel")
        addChannelButton.clicked.connect(self.addChannel)
        deleteChannelButton = QPushButton("Delete Channel")
        deleteChannelButton.clicked.connect(self.deleteChannel)
        #too add a yes or no option
        self.channelName = QLineEdit(self)
        layout.addWidget(addChannelButton, 1, 2)
        layout.addWidget(deleteChannelButton, 1, 3)
        layout.addWidget(self.channelName, 1, 1)

        addCommandButton = QPushButton("New")
        addCommandButton.clicked.connect(self.addCommand)
        editCommandButton = QPushButton("Edit")
        editCommandButton.clicked.connect(self.editCommand)
        deleteCommandButton = QPushButton("Delete")
        deleteCommandButton.clicked.connect(self.deleteCommand)
        layout.addWidget(addCommandButton, 8, 1)
        layout.addWidget(editCommandButton, 8, 2)
        layout.addWidget(deleteCommandButton, 8, 3)

        layout.addWidget(QLabel('Command:'), 2, 4)
        self.commandName = QLineEdit(self)
        layout.addWidget(self.commandName, 2, 5, 1, 4)

        subscriberTemplateButton = QPushButton("Subscriber")
        subscriberTemplateButton.clicked.connect(self.subTemplate)
        followerTemplateButton = QPushButton("Follower")
        #follower to be completed
        followerTemplateButton.clicked.connect(self.followerTemplate)
        EmptyTemplateButton = QPushButton("Empty")
        EmptyTemplateButton.clicked.connect(self.emptyTemplate)
        layout.addWidget(subscriberTemplateButton, 1, 4, 1, 2)
        layout.addWidget(followerTemplateButton, 1, 6)
        layout.addWidget(EmptyTemplateButton, 1, 7, 1, 2)

        layout.addWidget(QLabel('Response:'), 3, 4, 1, 5)
        self.responseEditor = QTextEdit(self)
        layout.addWidget(self.responseEditor, 4, 4, 4, 5)

        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.saveCommand)
        resetButton = QPushButton("Reset")
        resetButton.clicked.connect(self.resetCommand)
        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.close)
        layout.addWidget(saveButton, 8, 4)
        layout.addWidget(resetButton, 8, 5)
        layout.addWidget(cancelButton, 8, 7, 1, 2)

        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 1)
        layout.setRowStretch(4, 1)
        layout.setRowStretch(5, 20)
        layout.setRowStretch(8, 1)
        self.setLayout(layout)
        #make it able to import data from another folder
        position = self.mainWindow.getPopUpPosition(870, 480)
        self.setGeometry(position.x(), position.y(), 870, 480)

        self.exec()

    def populateChannelsCommands(self):
        directoryModel = QFileSystemModel()
        directoryModel.setRootPath(self.COMMAND_FOLDER_PATH)
        self.commandsTreeView.setModel(directoryModel)
        self.commandsTreeView.setRootIndex(directoryModel.index(self.COMMAND_FOLDER_PATH))

    def followerTemplate(self):
        self.commandName.clear()
        self.commandName.setText("_follower_ @user@ has just followed @channel@")
        self.commandName.setReadOnly(True)
        self.responseEditor.clear()

    def subTemplate(self):
        self.commandName.clear()
        self.commandName.setText("_new_sub_ @user@ has just subscribed to @channel@ for @month@ in a row, with @tier@")
        self.commandName.setReadOnly(True)
        self.responseEditor.clear()

    def emptyTemplate(self):
        self.commandName.clear()
        self.commandName.setReadOnly(False)
        self.responseEditor.clear()

    def addChannel(self):
        channelName = self.channelName.text().lower()
        if not os.path.exists(self.COMMAND_FOLDER_PATH + channelName):
            os.mkdir(self.COMMAND_FOLDER_PATH + channelName)
        else:
            self.commandsTreeView.keyboardSearch(channelName)
        self.channelName.clear()

    def deleteChannel(self):
        arr = self.commandsTreeView.selectionModel().selectedIndexes()
        if len(arr) is not 0:
            if arr[0].parent().data() == 'Commands':
                shutil.rmtree(self.COMMAND_FOLDER_PATH + arr[0].data())

    def deleteCommand(self):
        arr = self.commandsTreeView.selectionModel().selectedIndexes()
        if len(arr) is not 0:
            if arr[0].parent().data() != 'Commands':
                os.remove(self.COMMAND_FOLDER_PATH + arr[0].parent().data() + '\\' + arr[0].data())

    def addCommand(self):
        arr = self.commandsTreeView.selectionModel().selectedIndexes()
        if len(arr) is not 0:
            channel = arr[0].parent().data()
            if channel == 'Commands':
                channel = arr[0].data()
            if self.file is not None:
                self.file.close()
            self.file = open(self.COMMAND_FOLDER_PATH + channel + '\\NewCommand', 'w')
            self.commandName.setText("NewCommand")
            self.responseEditor.clear()
            self.commandName.setReadOnly(False)

    def editCommand(self):
        arr = self.commandsTreeView.selectionModel().selectedIndexes()
        if len(arr) is not 0:
            if arr[0].parent().data() != 'Commands':
                if self.file is not None:
                    self.file.close()
                self.file = open(self.COMMAND_FOLDER_PATH + arr[0].parent().data() + '\\' + arr[0].data(), 'r+')
                lines = sum(1 for _ in self.file)
                self.file.seek(0)
                self.commandName.setText(self.file.readline())
                if (BotDialog.isDefaultCommand(self.commandName.text())):
                    self.commandName.setReadOnly(True)
                else:
                    self.commandName.setReadOnly(False)
                if lines >= 2:
                    self.responseEditor.setText(self.file.readline())


    def resetCommand(self):
        if self.file.name[self.file.name.rfind('\\') + 1:] == "NewCommand":
            self.commandName.clear()
            self.responseEditor.clear()
        elif self.file is not None:
            self.file.seek(0)
            lines = sum(1 for _ in self.file)
            self.file.seek(0)
            self.commandName.setText(self.file.readline()[0:-1])
            if (BotDialog.isDefaultCommand(self.commandName.text())):
                self.commandName.setReadOnly(True)
            else:
                self.commandName.setReadOnly(False)
            if lines >= 2:
                self.responseEditor.setText(self.file.readline())

    def saveCommand(self):
        if self.file is not None and self.commandName.text() != "":
            fileName = self.commandName.text()
            if ' ' in fileName:
                fileName = fileName[0:fileName.index(' ')]
            currentFileName = self.file.name[self.file.name.rfind('\\') + 1:]
            if currentFileName == "NewCommand" and fileName != currentFileName:
                folder = self.file.name[:self.file.name.rfind('\\')+1]
                temp = self.file.name
                self.file.close()
                os.rename(temp, folder + fileName)
                self.file = open(folder + fileName, 'r+')
                currentFileName = fileName

            if  currentFileName == fileName:
                self.file.seek(0)
                self.file.write(self.commandName.text() + '\n')
                self.file.write(self.responseEditor.toPlainText())
                self.file.truncate()

    def closeEvent(self, event):
        if self.file is not None:
            self.file.close()
        for x in os.walk(BotDialog.COMMAND_FOLDER_PATH):
            if os.path.exists(x[0] + "\\NewCommand"):
                os.remove(x[0] + "\\NewCommand")
        event.accept()

    @staticmethod
    def isDefaultCommand(commandName):
        if commandName[0] == "_":
            return True
