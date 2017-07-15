import re
import threading
from queue import Queue

class SystemMessageProcessor:
    HOST_MODE = re.compile('.*HOSTTARGET #([^ ]+) :([^ ]+)')
    JOIN_MESSAGE = re.compile(':([^!]+)!.* JOIN #(.*)$')
    PART_MESSAGE = re.compile(':([^!]+)!.* PART #(.*)$')
    USERSTATE = re.compile('@badges=([^;]+);color=(#[^;]+);display-name=(#[^;]+);emote-sets=(#[^;]+);mod==(#[^;]+);subscriber==(#[^;]+);.*USERSTATE #(.*)')
    ROOMSTATE = re.compile('@broadcaster-lang=([^;]+)?;emote-only=([01]);followers-only=([^;]+);r9k=([01]);room-id=([^;]+);slow=([^;]+);subs-only=([01]).*ROOMSTATE #(.*)')
    NOTICE = re.compile('@msg-id=([^ ]+) .*NOTICE #([^ ]+) :(.*)')
    NAME_LIST = re.compile('tmi.twitch.tv 353 .*=#([^ ]+) :(.*)')
    SYSTEM_MODDING = re.compile(':jtv MODE #(.*) \+o (.*)')
    NAME_LIST = re.compile('.* 353 .* #(.*) :(.*)')

    def __init__(self, chatScreen):
        self.chatScreen = chatScreen
        self.jsonDecoderThread = chatScreen.jsonDecoder.jsonDecoderThread
        self.systemMessageThread = SystemMessageThread(self, self.chatScreen)
        self.systemMessageThread.start()
        self.jsonDecoderThread.start()

    def processMessage(self, message):
        if ' HOSTTARGET ' in message:
            result = re.search(SystemMessageProcessor.HOST_MODE, message)
            print(result.group(1) + ' is hosting ' + result.group(2))
        elif ' JOIN ' in message:
            result = re.search(SystemMessageProcessor.JOIN_MESSAGE, message)
            chatTab = self.chatScreen.tabs.get('#' + result.group(2))
            chatTab.userList.addUser(result.group(1))
        elif ' USERSTATE ' in message:
            result = re.search(SystemMessageProcessor.USERSTATE, message)
            print(message)
        elif ' ROOMSTATE ' in message:
            result = re.search(SystemMessageProcessor.ROOMSTATE, message)
            chatTab = self.chatScreen.tabs.get('#' + result.group(8))
            chatTab.setRoomState(result.group(1), result.group(2), result.group(3), result.group(4),
                                 result.group(5), result.group(6), result.group(7))
            #change later
            self.jsonDecoderThread.addJob(['set_badges', chatTab.channelChat.messageProcessor, result.group(5)])


        elif ' +o ' in message:
            result = re.search(SystemMessageProcessor.SYSTEM_MODDING, message)
            userList = self.chatScreen.tabs.get('#' + result.group(1)).userList
            userList.reIndexUserForSystemModding(result.group(2))
        elif ' 353 ' in message:
            result = re.search(SystemMessageProcessor.NAME_LIST, message)
            userList = self.chatScreen.tabs.get('#' + result.group(1)).userList
            for nick in result.group(2).split(' '):
                if userList.nickList.get(nick, None) is None:
                    userList.addUser(nick)
        else:
            print(message)


class SystemMessageThread(threading.Thread):
    def __init__(self, parent, chatScreen):
        super().__init__(target=self.run, args=('',))
        self.systemMessageProcessor = parent
        self.chatScreen = chatScreen
        self.messageToBeProcessed = Queue()
        self.daemon = True

    def newMessage(self, message):
        self.messageToBeProcessed.put(message)

    def run(self):
        while True:
            message = self.messageToBeProcessed.get()
            self.systemMessageProcessor.processMessage(message)



