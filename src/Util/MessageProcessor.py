import re
import random
from User import *

class MessageProcessor:

    def __init__(self, jsonDecoder, ):
        self.message_pattern = re.compile('(\d\d:\d\d:\d\d) @badges=([^;]*);(bits=(\d+);)?color=([^;]*);display-name=(([^A-Za-z]+)|([^;]+));.*subscriber=([01]);.*turbo=([01]);user-id=(\d+);user-type=([^ ]*) :([^!]+)!.*PRIVMSG[^:]*:( ACTION)?(.*)')
        self.jsonDecoder = jsonDecoder
        self.bitsBadge = {}
        self.subBadge = {}

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
                user.hasSpoken = True
                userList.updateUser(user.nick, message.group(2), self.subBadge, self.bitsBadge)
                user.updateUserColor(message.group(5))
            else:
                if user.badges != message.group(2):
                    userList.updateUser(user.nick, message.group(2))
            finalMessage += user.badgesImage
            bits = 'group 3, to be done'
            finalMessage += '<a href="' + nameLink + '" style="text-decoration:none" '
            if message.group(5):
                if user.color != message.group(5):
                    user.updateUserColor(message.group(5))
            color = 'style="color:' + user.color + '"'
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
            #emotes = to be done
            print(finalMessage)
            channelChat.newMessage(finalMessage)

    def setBadgesIcon(self, badges):
        if badges['badge_sets'].get('subscriber', None) is not None:
            for badge in badges['badge_sets']['subscriber']['versions']:
                self.subBadge[badge] = badges['badge_sets']['subscriber']['versions'][badge]['image_url_1x']
        if badges['badge_sets'].get('bits', None) is not None:
            for badge in badges['badge_sets']['bits']['versions']:
                self.bitsBadge[badge] = badges['badge_sets']['bits']['versions'][badge]['image_url_1x']
