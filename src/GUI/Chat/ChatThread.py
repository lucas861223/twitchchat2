import threading


class ChatThread(threading.Thread):
    def __init__(self, channelChat):
        super().__init__(target=self.run, args=('',))
        self.channelChat = channelChat
        self.messageProcessor = channelChat.messageProcessor
        self.userList = channelChat.chatTab.userList
        self.daemon = True


    def run(self, message):
        self.messageProcessor.processMessage(message, self.channelChat, self.userList)
