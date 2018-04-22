from PyQt5.QtWidgets import QCheckBox, QComboBox, QDialog, QPushButton, QLabel, QTreeView, QLineEdit, QGridLayout, QTextEdit, QFileSystemModel
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
        self.commandsTreeView.doubleClicked.connect(self.editCommand)
        layout.addWidget(self.commandsTreeView, 2, 1, 7, 3)
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
        layout.addWidget(addCommandButton, 9, 1)
        layout.addWidget(editCommandButton, 9, 2)
        layout.addWidget(deleteCommandButton, 9, 3)

        layout.addWidget(QLabel('Command:'), 2, 4, 1, 1)
        self.commandName = QTextEdit(self)
        layout.addWidget(self.commandName, 3, 4, 1, 5)

        self.permissionGroup = QComboBox(self)
        layout.addWidget(self.permissionGroup, 4, 4, 1, 1)
        self.permissionGroup.addItems(["Twitch only", "streamer only", "mods", "subs", "everyone", "specific only"])
        #remove from list
        self.permissionGroup.model().item(0).setEnabled(False)
        self.permissionGroup.setCurrentIndex(4)
        self.permissionGroup.activated[str].connect(self.changePermissionGroup)
        self.exceptionLabel = QLabel('Exception:')
        self.exceptionLabel.setAlignment(Qt.AlignRight)
        layout.addWidget(self.exceptionLabel, 4, 5, 1, 1)
        self.exceptionUsersLineEdit = QLineEdit(self)
        self.exceptionUsersLineEdit.setEnabled(False)
        layout.addWidget(self.exceptionUsersLineEdit, 4, 6, 1, 3)

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

        layout.addWidget(QLabel('Response:'), 5, 4, 1, 2)
        self.enabledCheckBox = QCheckBox("Enabled")
        layout.addWidget(self.enabledCheckBox, 5, 7, 1, 2)
        self.responseEditor = QTextEdit(self)
        layout.addWidget(self.responseEditor, 6, 4, 3, 5)

        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.saveCommand)
        resetButton = QPushButton("Reset")
        resetButton.clicked.connect(self.resetCommand)
        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.close)
        layout.addWidget(saveButton, 9, 4)
        layout.addWidget(resetButton, 9, 5)
        layout.addWidget(cancelButton, 9, 7, 1, 2)

        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 1)
        layout.setRowStretch(4, 1)
        layout.setRowStretch(5, 1)
        layout.setRowStretch(6, 20)
        layout.setRowStretch(9, 1)
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
        self.permissionGroup.setCurrentIndex(5)
        self.permissionGroup.setEnabled(False)
        self.exceptionUsersLineEdit.setText("")
        self.exceptionUsersLineEdit.setEnabled(False)
        self.commandName.setText("_follower_ @user@ has just followed @channel@")
        self.commandName.setReadOnly(True)
        self.responseEditor.clear()

    def subTemplate(self):
        self.commandName.clear()
        self.permissionGroup.setCurrentIndex(5)
        self.permissionGroup.setEnabled(False)
        self.exceptionUsersLineEdit.setText("")
        self.exceptionUsersLineEdit.setEnabled(False)
        self.commandName.setText("_new_sub_ @user@ has just subscribed to @channel@ for @month@ in a row, with @tier@")
        self.commandName.setReadOnly(True)
        self.responseEditor.clear()

    def emptyTemplate(self):
        self.commandName.clear()
        self.commandName.setReadOnly(False)
        self.permissionGroup.setCurrentIndex(4)
        self.permissionGroup.setEnabled(True)
        self.exceptionUsersLineEdit.setText("")
        self.exceptionUsersLineEdit.setEnabled(False)
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

    def changePermissionGroup(self, group):
        if group == 'everyone':
            self.exceptionUsersLineEdit.setText("")
            self.exceptionUsersLineEdit.setEnabled(False)
        elif self.file:
            self.exceptionUsersLineEdit.setEnabled(True)
            self.file.seek(0)
            lines = sum(1 for _ in self.file)
            if lines > 2:
                self.file.seek(0)
                self.file.readline()
                self.file.readline()
                self.file.readline()
                exceptionUsers = self.file.readline()
                if exceptionUsers:
                    self.exceptionUsersLineEdit.setText(exceptionUsers[:-1])
                else:
                    self.exceptionUsersLineEdit.setText("")
            else:
                self.exceptionUsersLineEdit.setText("")
        else:
            self.exceptionUsersLineEdit.setEnabled(True)
            self.exceptionUsersLineEdit.setText("")


    def deleteCommand(self):
        arr = self.commandsTreeView.selectionModel().selectedIndexes()
        if len(arr) is not 0:
            if arr[0].parent().data() != 'Commands':
                filePath = self.COMMAND_FOLDER_PATH + arr[0].parent().data() + '\\' + arr[0].data()
                if filePath == self.file.name:
                    self.file.close()
                    self.emptyTemplate()
                    self.file = None
                if os.path.exists(filePath):
                    os.remove(filePath)

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
            self.enabledCheckBox.setChecked(True)
            self.permissionGroup.setEnabled(True)
            self.permissionGroup.setCurrentIndex(4)
            self.exceptionUsersLineEdit.setText("")
            self.exceptionUsersLineEdit.setEnabled(False)
            self.responseEditor.clear()
            self.commandName.setReadOnly(False)

    def editCommand(self):
        arr = self.commandsTreeView.selectionModel().selectedIndexes()
        if len(arr) is not 0:
            if arr[0].parent().data() != 'Commands':
                if self.file is not None:
                    self.file.close()
                self.file = open(self.COMMAND_FOLDER_PATH + arr[0].parent().data() + '\\' + arr[0].data(), 'r+')
                self.fillFormFromFile()

    def fillFormFromFile(self):
        self.file.seek(0)
        lines = sum(1 for _ in self.file)
        if lines > 0:
            self.file.seek(0)
            checkState = self.file.readline()
            if checkState == 'On\n':
                self.enabledCheckBox.setChecked(True)
            else:
                self.enabledCheckBox.setChecked(False)
            self.commandName.setText(self.file.readline()[0:-1])
            if (BotDialog.isDefaultCommand(self.commandName.toPlainText())):
                self.commandName.setReadOnly(True)
            else:
                self.commandName.setReadOnly(False)
            self.permissionGroup.setEnabled(True)
            self.permissionGroup.setCurrentIndex(int(self.file.readline()[0:-1]))
            if self.permissionGroup.currentIndex() == 4 or self.permissionGroup.currentIndex() == 0:
                self.exceptionUsersLineEdit.setText("")
                self.exceptionUsersLineEdit.setEnabled(False)
                if self.permissionGroup.currentIndex() == 0:
                    self.permissionGroup.setEnabled(False)
                self.file.readline()
            else:
                self.exceptionUsersLineEdit.setEnabled(True)
                self.exceptionUsersLineEdit.setText(self.file.readline()[0:-1])
            if lines > 4:
                self.responseEditor.setText(str('').join(self.file.readlines()))
        else:
            self.emptyTemplate()
            self.commandName.setText("NewCommand")
            self.enabledCheckBox.setChecked(True)

    def resetCommand(self):
        if self.file.name[self.file.name.rfind('\\') + 1:] == "NewCommand":
            self.commandName.clear()
            self.responseEditor.clear()
            self.permissionGroup.setEnabled(True)
            self.permissionGroup.setCurrentIndex(4)
            self.exceptionUsersLineEdit.setText("")
            self.exceptionUsersLineEdit.setEnabled(False)
        elif self.file is not None:
            self.fillFormFromFile()

    def saveCommand(self):
        if self.file is not None and self.commandName.toPlainText() != "":
            fileName = self.commandName.toPlainText()
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
                if self.enabledCheckBox.isChecked():
                    self.file.write('On\n')
                else:
                    self.file.write('Off\n')
                self.file.write(self.commandName.toPlainText() + '\n')
                self.file.write(str(self.permissionGroup.currentIndex()) + '\n')
                self.file.write(self.exceptionUsersLineEdit.text() + '\n')
                self.file.write(self.responseEditor.toPlainText())
                self.file.truncate()

    def closeEvent(self, event):
        if self.file is not None:
            self.file.close()
        for files in os.walk(BotDialog.COMMAND_FOLDER_PATH):
            if os.path.exists(files[0] + "\\NewCommand"):
                os.remove(files[0] + "\\NewCommand")
        event.accept()

    @staticmethod
    def isDefaultCommand(commandName):
        return commandName[0] == "_"