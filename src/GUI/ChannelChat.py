from Util.MessageProcessor import MessageProcessor
from Chat.ChatThread import ChatThread
from PyQt5.QtWidgets import QTextBrowser


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
        #add wheel event

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
