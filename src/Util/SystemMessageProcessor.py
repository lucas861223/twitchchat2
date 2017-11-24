import re
from SystemMessageThread import SystemMessageThread
from User import UserListEntry
import random

class SystemMessageProcessor:
    HOST_MODE = re.compile('.*HOSTTARGET #([^ ]+) :([^ ]+)')
    JOIN_MESSAGE = re.compile(':([^!]+)!.* JOIN #(.*)$')
    PART_MESSAGE = re.compile(':([^!]+)!.* PART #(.*)$')
    USERSTATE = re.compile('@badges=([^;]+);.*color=(#[^;]+);.*display-name=(#[^;]+);.*emote-sets=(#[^;]+);.*mod=(#[^;]+);.*subscriber==(#[^;]+);.*USERSTATE #(.*)')
    ROOMSTATE = re.compile('@broadcaster-lang=([^;]+)?;.*emote-only=([01]);.*followers-only=([^;]+);.*r9k=([01]);.*room-id=([^;]+);.*slow=([^;]+);.*subs-only=([01]).*ROOMSTATE #(.*)')
    NOTICE = re.compile('@msg-id=([^ ]+) .*NOTICE #([^ ]+) :(.*)')
    NAME_LIST = re.compile('.* 353 .* #(.*) :(.*)')
    SYSTEM_MODDING = re.compile(':jtv MODE #(.*) \+o (.*)')
    GLOBALUSERSTATE = re.compile('color=([^;]*);display-name=([^;]*).*user-id=([\d]+)')

    def __init__(self, chatScreen):
        self.chatScreen = chatScreen
        self.internetRelatedThread = chatScreen.jsonDecoder.internetRelatedThread
        self.systemMessageThread = SystemMessageThread(self, self.chatScreen)
        self.systemMessageThread.start()
        self.internetRelatedThread.start()

    def processMessage(self, message):
        print(message)
        if ' PART ' in message:
            result = re.search(SystemMessageProcessor.PART_MESSAGE, message)
            if result.group(1) + '\n' != self.chatScreen.clientIRC.nickname:
                chatTab = self.chatScreen.tabs.get('#' + result.group(2))
                if chatTab.userList.nickList.get(result.group(1), None):
                    chatTab.userList.removeUser(chatTab.userList.nickList[result.group(1)], True)
        elif ' JOIN ' in message:
            result = re.search(SystemMessageProcessor.JOIN_MESSAGE, message)
            chatTab = self.chatScreen.tabs.get('#' + result.group(2))
            chatTab.userList.addUser(result.group(1))
        elif ' WHISPER ' in message:
            self.chatScreen.newWhisperSignal.emit(message)
        elif ' USERSTATE ' in message:
            result = re.search(SystemMessageProcessor.USERSTATE, message)
        elif ' ROOMSTATE ' in message:
            result = re.search(SystemMessageProcessor.ROOMSTATE, message)
            if result is not None:
                chatTab = self.chatScreen.tabs.get('#' + result.group(8))
                chatTab.setRoomState(result.group(1), result.group(2), result.group(3), result.group(4),
                                     result.group(5), result.group(6), result.group(7))
                #change later
                self.internetRelatedThread.addJob(['set_badges', chatTab.channelChat, result.group(5)])
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
        elif ' HOSTTARGET ' in message:
            result = re.search(SystemMessageProcessor.HOST_MODE, message)
        elif 'GLOBALUSERSTATE' in message:
            result = re.search(SystemMessageProcessor.GLOBALUSERSTATE, message)
            if result.group(1):
                self.chatScreen.clientIRC.userColor = result.group(1)
            else:
                self.chatScreen.clientIRC.userColor = random.choice(UserListEntry.DEFAULT_COLOR)
            if result.group(2):
                if (any(not character.isalpha() and not character.isdigit() for character in result.group(2))):
                    self.chatScreen.clientIRC.userDisplayName = result.group(2) + ' (' + self.chatScreen.clientIRC.nickname + ')'
                else:
                    self.chatScreen.clientIRC.userDisplayName = result.group(2)
            else:
                self.chatScreen.clientIRC.userDisplayName = self.chatScreen.clientIRC.nickname
            self.chatScreen.clientIRC.userID = result.group(3)
        else:
            print(message)



