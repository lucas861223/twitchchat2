from PyQt5.QtWidgets import QTextBrowser
import random
from Chat.User import  UserListEntry

class WhisperChat(QTextBrowser):
    def __init__(self, chatScreen, whisperer, clientIRC):
        super(WhisperChat, self).__init__(chatScreen)
        self.chatScreen = chatScreen
        self.clientIRC = clientIRC
        self.scrollToBottom = True
        self.lastSent = ''
        self.setReadOnly(True)
        self.anchorClicked.connect(self.checkClick)
        self.setAcceptRichText(True)
        self.setOpenLinks(False)
        self.verticalScrollBar().rangeChanged.connect(self.scrollBar)
        self.verticalScrollBar().sliderReleased.connect(self.shouldKeepScrolling)
        self.channelName = '$' + whisperer
        #add wheel event

    def setUpWhisperChat(self, color):
        self.userColor = random.choice(UserListEntry.DEFAULT_COLOR)

    def checkClick(self, link):
        print(link.toString())

    def newMessage(self, message):
        self.append(message)

    def shouldKeepScrolling(self):
        if self.verticalScrollBar().value() == self.verticalScrollBar().maximum():
            self.scrollToBottom = True
        else:
            self.scrollToBottom = False

    def scrollBar(self):
        if self.scrollToBottom:
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
