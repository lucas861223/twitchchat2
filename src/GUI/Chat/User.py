from PyQt5.QtWidgets import QListWidgetItem
import random

class UserListEntry(QListWidgetItem):
    DEFAULT_COLOR = ['#FF0000', '#00FF00', '#0000FF', '#B22222', '#FF7F50', '#9ACD32', '#FF4500', '#2E8B57', '#DAA520', '#D2691E', '#5F9EA0', '#1E90FF', '#FF69B4', '#8A2BE2', '#00FF7F']

    def __init__(self, nick):
        super().__init__()
        self.userName = nick
        #CHANGE THIS LATER
        self.nick = nick
        self.setText(nick)
        self.point = 0
        self.hasSpoken = False
        self.modSet = False
        self.badges = ''

    def updateUserBadge(self, badges):
        self.userName = self.nick
        if 'turbo' in badges:
            self.userName = '+' + self.userName
        if 'premium' in badges:
            self.userName = '+' + self.userName
        if 'bits' in badges:
            self.userName = '$' + self.userName
        if 'subscriber' in badges:
            self.userName = '%' + self.userName
        if 'moderator' in badges:
            self.userName = '@' + self.userName
        if 'global_mod' in badges:
            self.userName = '*' + self.userName
        if 'admin' in badges:
            self.userName = '!' + self.userName
        if 'staff' in badges:
            self.userName = '&' + self.userName
        if 'broadcaster' in badges:
            self.userName = '~' + self.userName
        self.setText(self.userName)
        self.calculatePoint()
        self.badges = badges

    def updateUserColor(self, color):
        if color == '':
            self.randomColor = True
            self.color = random.choice(UserListEntry.DEFAULT_COLOR)
        else:
            self.randomColor = False
            self.color = color

    def setStreamer(self):
        self.userName = '~' + self.userName
        self.calculatePoint()
        self.setText(self.userName)

    def setMod(self):
        if self.modSet == False and self.hasSpoken == False:
            if self.userName[0] != '~':
                self.userName = '@' + self.userName
            self.setText(self.userName)
            self.calculatePoint()
            self.modSet = True


    def calculatePoint(self):
        self.point = 0
        if '~' in self.userName:
            self.point += 16
        if '&' in self.userName:
            self.point += 8
        if '!' in self.userName:
            self.point += 8
        if '*' in self.userName:
            self.point += 4
        if '@' in self.userName:
            self.point += 2
        if '%' in self.userName:
            self.point += 1

    def __lt__(self, other):
        if self.point == other.point:
            return self.nick < other.nick
        return self.point > other.point

    def __gt__(self, other):
        if self.point == other.point:
            return self.nick > other.nick
        return self.point < other.point

    def __eq__(self, other):
        return self.nick == other.nick

    def setUserChat(self, userChat):
        self.userChat = userChat