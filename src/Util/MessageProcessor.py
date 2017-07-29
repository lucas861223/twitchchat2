import re

class MessageProcessor:
    EMOTE_PATTERN = re.compile('(\d+):(\d+-\d+,?)+')
    EMOTE_RANGE = re.compile('((\d+)-(\d+)),?')
    EMOTE_PREFIX = 'http://static-cdn.jtvnw.net/emoticons/v1/'
    MESSAGE_PATTERN = re.compile('(\d\d:\d\d:\d\d) @badges=([^;]*);.*(bits=(\d+);.*)?color=([^;]*);.*display-name=(([^A-Za-z]*)|([^;]*));.*emotes=([^;]*);.*user-id=(\d+);.*:([^!]+)!.*#[^ ]+ :( ACTION)?(.*)')
    def __init__(self, jsonDecoder, ):
        self.jsonDecoder = jsonDecoder
        self.bitsBadge = {}
        self.subBadge = {}

    def processMessage(self, response, channelChat, userList):
        message = re.search(MessageProcessor.MESSAGE_PATTERN, response)
        print(response)
        if message is not None:
            finalMessage = '[' + message.group(1) + '] '
            nameLink = message.group(11)
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
            finalMessage += 'style="color:' + user.color + '">'
            if message.group(6) is not None:
                if message.group(7) is not None:
                    displayName = message.group(7) + ' (' + nameLink + ')'
                else:
                    displayName = message.group(8)
            else:
                displayName = nameLink
            displayName = '<b>' + displayName + ': </b></a>'
            finalMessage += displayName

            finalMessage += MessageProcessor.insertEmote(message.group(13), message.group(9))
            #emotes = to be done
            print(finalMessage)
            channelChat.newMessage(finalMessage)

    @staticmethod
    def insertEmote(message, emotes):
        if emotes == '':
            return message
        emoteArray = MessageProcessor.constructEmoteArray(emotes)
        for i in range(len(emoteArray) - 1, 0, -1):
            message = message[0:emoteArray[i][1]-1] + '<img src="' +  MessageProcessor.EMOTE_PREFIX + emoteArray[i][0] + '/1.0">' + message[emoteArray[i][2]+1:]
        if (emoteArray[0][1] == 0):
            message = '<img src="' + MessageProcessor.EMOTE_PREFIX + emoteArray[0][0] + '/1.0">' + message[emoteArray[0][2] + 1:]
        else:
            message = message[0:emoteArray[0][1] - 1] + '<img src="' + MessageProcessor.EMOTE_PREFIX + emoteArray[0][0] + '/1.0">' + message[emoteArray[0][2] + 1:]
        return message

    @staticmethod
    def constructEmoteArray(emote):
        #add bttv and frankerz later
        emoteArray = []
        result = re.search(MessageProcessor.EMOTE_PATTERN, emote)
        while(result != None):
            emoteAndRanges = result.group(0)
            index = 0
            ranges = re.split(MessageProcessor.EMOTE_RANGE, emoteAndRanges)
            for i in range(2, len(ranges), 4):
                for x in range(len(emoteArray), 0, -1):
                    if int(ranges[i+1]) > emoteArray[x-1][2]:
                        index = x
                        break
                emoteArray.insert(index, [ranges[0][0:len(ranges[0]) - 1], int(ranges[i]), int(ranges[i + 1])])
            emote = emote[result.end():]
            result = re.search(MessageProcessor.EMOTE_PATTERN, emote)
        return emoteArray

    def setBadgesIcon(self, badges):
        if badges['badge_sets'].get('subscriber', None) is not None:
            for badge in badges['badge_sets']['subscriber']['versions']:
                self.subBadge[badge] = badges['badge_sets']['subscriber']['versions'][badge]['image_url_1x']
        if badges['badge_sets'].get('bits', None) is not None:
            for badge in badges['badge_sets']['bits']['versions']:
                self.bitsBadge[badge] = badges['badge_sets']['bits']['versions'][badge]['image_url_1x']
