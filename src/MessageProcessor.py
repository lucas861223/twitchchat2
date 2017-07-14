import re
import random
import requests
from User import *

class MessageProcessor:

    def __init__(self):
        self.message_pattern = re.compile('(\d\d:\d\d:\d\d) @badges=([^;]*);(bits=(\d+);)?color=([^;]*);display-name=(([^A-Za-z]+)|([^;]+));.*subscriber=([01]);.*turbo=([01]);user-id=(\d+);user-type=([^ ]*) :([^!]+)!.*PRIVMSG[^:]*:( ACTION)?(.*)')

    def processMessage(self, response, channelChat, userList):
        message = re.search(self.message_pattern, response)
        print(response)
        if message is not None:
            finalMessage = '[' + message.group(1) + '] '
            nameLink = message.group(13)
            user = userList.nickList.get(nameLink, None)
            if user is None:
                userList.addUser(nameLink)
                user = userList.nickList.get(nameLink)
            if user.hasSpoken == False:
                userList.updateUser(user.nick, message.group(2))
            else:
                if user.badges != message.group(2):
                    userList.updateUser(user.nick, message.group(2))
            finalMessage += self.getBadgesIcon(message.group(2))
            badges = 'group 2, to me done'
            bits = 'group 3, to be done'
            finalMessage += '<a href="' + nameLink + '" style="text-decoration:none" '
            if message.group(5) is not '':
                color = 'style="color:' + message.group(5) + '"'
            else:
                color = 'style="color:' + random.choice(UserListEntry.DEFAULT_COLOR) + '"'
            finalMessage += color + '>'
            if message.group(6) is not None:
                if message.group(7) is not None:
                    displayName = message.group(7) + ' (' + message.group(13) + ')'
                else:
                    displayName = message.group(8)
            else:
                displayName = nameLink
            displayName = '<b>' + displayName + ': </b></a>'
            finalMessage += displayName
            finalMessage += message.group(15)
            print(finalMessage)
            channelChat.newMessage(finalMessage)

    def getBadgesIcon(self, badges):
        return ''

