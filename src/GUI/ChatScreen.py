from PyQt5.QtWidgets import QShortcut, QTextBrowser, QSplitter, QMainWindow, QHBoxLayout, QTextEdit, QWidget, QTabWidget, QVBoxLayout, QLineEdit, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from UserList import UserList
from Util.ClientIRC import ClientIRC
from Util.MessageProcessor import MessageProcessor
from Chat.ChatThread import *
from Util.JSONDecoder import JSONDecoder

class ChatScreen(QTabWidget):
    def __init__(self, parent):
        super(ChatScreen, self).__init__(parent)
        self.jsonDecoder = JSONDecoder()
        self.tabs = {}
        self.clientIRC = ClientIRC(self)
        self.clientIRC.start()
        self.setAutoFillBackground(True)
        default_channel = open('../setting/default_channel', 'r')
        for line in default_channel:
            self.joinChannel(line.replace('\n', ''))
        default_channel.close()
        QShortcut(QKeySequence('Ctrl+Tab'), self, self.nextTab)
        QShortcut(QKeySequence('Ctrl+W'), self, self.closeTab)

    def joinChannel(self, channelName):
        chatTab = self.tabs.get('#' + channelName, None)
        if chatTab is None:
            chatTab = ChatTab(channelName, self.clientIRC, self.jsonDecoder)
            self.tabs['#' + channelName] = chatTab
            self.addTab(chatTab, '#' + channelName)
            self.setCurrentIndex(self.count() - 1)
        else:
            index = 0
            for index in range(0, self.count()):
                if self.widget(index).channelName == '#' + channelName:
                    break
            self.setCurrentIndex(index)

    def newMessage(self, channelName, message):
        chatTab = self.tabs.get(channelName, None)
        chatTab.channelChat.chatThread.processMessage(message)

    def nextTab(self):
        if self.currentIndex() == self.count() - 1:
            self.setCurrentIndex(0)
        else:
            self.setCurrentIndex(self.currentIndex() + 1)

    def closeTab(self):
        if self.count() > 1:
            self.clientIRC.leaveChannel(self.widget(self.currentIndex()).channelName)
            self.tabs.pop(self.widget(self.currentIndex()).channelName)
            if self.currentIndex() == 0:
                self.setCurrentIndex(1)
                self.widget(0).close()
                self.removeTab(0)
            else:
                self.setCurrentIndex(self.currentIndex() - 1)
                self.widget(self.currentIndex() + 1).close()
                self.removeTab(self.currentIndex() + 1)

class ChatTab(QWidget):
    def __init__(self, channelName, clientIRC, jsonDecoder):
        super(ChatTab, self).__init__()
        userList = UserList(self)
        self.userList = userList
        channelChat = ChannelChat(self, channelName, jsonDecoder)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(channelChat)
        splitter.addWidget(userList)
        splitter.setContentsMargins(0, 0, 0, 0)
        splitter.setHandleWidth(0)
        splitter.setStretchFactor(0, 7)
        splitter.setStretchFactor(1, 1)
        splitter.setChildrenCollapsible(False)
        layout.addWidget(splitter)
        self.jsonDecoder = jsonDecoder
        self.clientIRC = clientIRC
        self.clientIRC.joinChannel(channelName)
        self.setLayout(layout)
        self.channelChat = channelChat
        self.channelName = '#' + channelName

    def setRoomState(self, language, emotesOnly, followersOnly, r9k, roomID, slow, subsOnly):
        self.language = language
        self.emotesOnly = emotesOnly
        self.followersOnly = followersOnly
        self.r9k = r9k
        self.roomID = roomID
        self.slow = slow
        self.subsOnly = subsOnly



class ChannelChat(QTextBrowser):
    def __init__(self, chatTab, channelName, jsonDecoder):
        super(ChannelChat, self).__init__(chatTab)
        self.chatTab = chatTab
        self.messageProcessor = MessageProcessor(jsonDecoder)
        self.chatThread = ChatThread(self, channelName)
        self.chatThread.start()
        self.setReadOnly(True)
        self.anchorClicked.connect(self.checkClick)
        self.setAcceptRichText(True)
        self.setOpenLinks(False)
        self.scrollToBottom = True
        self.lastSent = ''
        self.verticalScrollBar().rangeChanged.connect(self.scrollBar)
        self.verticalScrollBar().sliderReleased.connect(self.shouldKeepScrolling)

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
