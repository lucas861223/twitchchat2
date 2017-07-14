import re
import threading

class SystemMessageProcessor:
    HOST_MODE = re.compile('.*HOSTTARGET #([^ ]+) :([^ ]+)')
    JOIN_MESSAGE = re.compile(':([^!]+)!.* JOIN #(.*)$')
    PART_MESSAGE = re.compile(':([^!]+)!.* PART #(.*)$')
    USERSTATE = re.compile('@badges=([^;]+);color=(#[^;]+);display-name=(#[^;]+);emote-sets=(#[^;]+);mod==(#[^;]+);subscriber==(#[^;]+);.*USERSTATE #(.*)')
    ROOMSTATE = re.compile('@broadcaster-lang=([^;]+)?;emote-only=([01]);followers-only=([^;]+);r9k=([01]);room-id=([^;]+);slow=([^;]+);subs-only=([01]).*ROOMSTATE #(.*)@broadcaster-lang=([^;]+);emote-only=([^;]+);followers-only=([^;]+);r9k=([^;]+);room-id=([^;]+);slow==([^;]+);subs-only=([^ ]+).*ROOMSTATE #(.*)')
    NOTICE = re.compile('@msg-id=([^ ]+) .*NOTICE #([^ ]+) :(.*)')
    NAME_LIST = re.compile('tmi.twitch.tv 353 .*=#([^ ]+) :(.*)')
    SYSTEM_MODDING = re.compile(':jtv MODE #(.*) \+o (.*)')
    NAME_LIST = re.compile('.* 353 .* #(.*) :(.*)')

    def __init__(self, chatScreen):
        self.chatScreen = chatScreen
        self.systemMessageThread = SystemMessageThread(self, self.chatScreen)

    def processMessage(self, message):
        print(message)
        result = re.search(SystemMessageProcessor.HOST_MODE, message)
        if result is not None:
            print(result.group(1) + ' is hosting ' + result.group(2))
        else:
            result = re.search(SystemMessageProcessor.JOIN_MESSAGE, message)
            if result is not None:
                chatTab = self.chatScreen.tabs.get('#' + result.group(2))
                chatTab.userList.addUser(result.group(1))
            else:
                result = re.search(SystemMessageProcessor.USERSTATE, message)
                if result is not None:
                    print(message)
                else:
                    result = re.search(SystemMessageProcessor.ROOMSTATE, message)
                    if result is not None:
                        chatTab = self.chatScreen.tabs.get('#' + result.group(8))
                        chatTab.setRoomState(result.group(1), result.group(2), result.group(3), result.group(4), result.group(5), result.group(6), result.group(7))
                    else:
                        result = re.search(SystemMessageProcessor.SYSTEM_MODDING, message)
                        if result is not None:
                            userList = self.chatScreen.tabs.get('#' + result.group(1)).userList
                            userList.reIndexUserForSystemModding(result.group(2))
                        else:
                            result = re.search(SystemMessageProcessor.NAME_LIST, message)
                            if result is not None:
                                userList = self.chatScreen.tabs.get('#' + result.group(1)).userList
                                for nick in result.group(2).split(' '):
                                    if userList.nickList.get(nick, None) is None:
                                        userList.addUser(nick)



class SystemMessageThread(threading.Thread):
    def __init__(self, parent, chatScreen):
        super().__init__(target=self.run, args=('',))
        self.systemMessageProcessor = parent
        self.chatScreen = chatScreen
        self.daemon = True

    def run(self, message):
        self.systemMessageProcessor.processMessage(message)
