from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QLineEdit, QWidget, QHBoxLayout, QGridLayout, QVBoxLayout
from ChatScreen import ChatScreen
from PyQt5.QtCore import Qt
from EntryBox import EntryBox


class CentralWidget(QWidget):
    def __init__(self, parent):
        super(CentralWidget, self).__init__(parent)
        self.mainWindow = parent
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        chatUI = ChatUI(self)
        self.chatUI = chatUI
        layout.addWidget(chatUI)
        entryBox = EntryBox(self, chatUI.chatScreen)
        layout.addWidget(entryBox)

    def newMessage(self, channelName, messageType, user, message):
        self.chatUI.chat.newMessage(channelName, messageType, user, message)


class ChatUI(QWidget):
    def __init__(self, parent):
        super(ChatUI, self).__init__(parent)
        self.centralWidget = parent
        layout = QHBoxLayout()
        chatScreen = ChatScreen(self)
        self.chatScreen = chatScreen
        layout.addWidget(chatScreen)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)

    def joinChannel(self):
        global joinChannelDialog
        joinChannelDialog = QDialog()
        joinChannelDialog.setWindowFlags(Qt.WindowCloseButtonHint)
        joinChannelDialog.setWindowTitle('Join Channel')
        position = self.centralWidget.mainWindow.getPopUpPosition(300, 200)
        joinChannelDialog.setGeometry(position.x(),position.y(), 300, 200)

        layout = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()

        label = QLabel()
        label.setText('Channel: ')
        entryBox = QLineEdit()
        joinButton = QPushButton()
        joinButton.setText('Join Channel')
        joinButton.clicked.connect(self.joinChannelMessage)
        cancelButton = QPushButton()
        cancelButton.setText('Cancel')
        cancelButton.clicked.connect(joinChannelDialog.close)

        layout2.addWidget(label, 1)
        layout2.addWidget(entryBox, 5)
        layout3.addWidget(joinButton, 4)
        layout3.addWidget(cancelButton, 2)

        layout.addLayout(layout2)
        layout.addLayout(layout3)
        joinChannelDialog.entryBox = entryBox
        joinChannelDialog.setLayout(layout)
        joinChannelDialog.exec()

    def joinChannelMessage(self):
        message = joinChannelDialog.entryBox.text().lower()
        if message is not '':
                self.chatScreen.joinChannel(message)
        joinChannelDialog.close()