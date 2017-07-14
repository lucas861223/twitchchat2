from PyQt5.QtWidgets import QLineEdit, QPushButton
from User import *


class EntryBox(QLineEdit):
    def __init__(self, parent, chatScreen):
        super(EntryBox, self).__init__(parent)
        self.chatScreen = chatScreen
        self.returnPressed.connect(self.send)

    def send(self):
        self.chatScreen.clientIRC.sendMessage('PRIVMSG ' + self.chatScreen.widget(self.chatScreen.currentIndex()).channelName + " :" + self.text() + '\r\n')
        self.setText('')