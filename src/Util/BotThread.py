import requests
import threading
from time import sleep
import socket
import re

class BotThread(threading.Thread):
    TEMP_PATTERN = re.compile('liaaaGiggle (?P<name>([^ ]+)) just cheered with (?P<amount>([\d]+)), and has cheered a total of (?P<totalAmount>([\d]+))! liaaaGiggle')
    TEMP_PATTERN2 = re.compile('liaaaPanda (?P<name>([^ ]+)), Thank you for the donation of (?P<donation>([\d\.]+)) USD! liaaaPanda')
    MESSAGE_PATTERN = re.compile('@badges=([^;]*);(bits=(\d+).*)?color=[^;]*;.*display-name=(?P<displayName>([^A-Za-z]*)|([^;]*));.*user-id=(\d+);.*:(?P<user>[^!]+)!.*#(?P<channel>[^ ]+) :(ACTION )?(.*)')
    def __init__(self, clientIRC, messageQueue):
        super().__init__(target=self.run)
        # self.students = {}
        # self.studentCount = 1
        self.setDaemon(True)
        self.setName('BotThread')
        self.clientIRC = None
        self.isRunning = False
        self.isHoldingMessage = False
        self.subMessage = re.compile('.*display-name=(?P<displayName>[^;]*).*;login=(?P<id>[^;]*).*;msg-id=(?P<messageId>[^;]*)(;msg-param-months=(?P<month>[\d]+))?.*;msg-param-sub-plan-name=(?P<subPlanName>[^;]+)(;msg-param-sub-plan=(?P<subPlan>[\d]+))?.*;.* USERNOTICE #(?P<channelName>[^ ]+).*')
        self.messageQueue = messageQueue
        self.clientIRC = clientIRC

    def activateBotThread(self, commands):
        self.isRunning = True
        self.commands = commands
        self.start()

    def deActivateBotThread(self):
        self.isRunning = False

    def run(self):
        while self.isRunning:
            message = self.messageQueue.get()
            if message[0] == 'message':
                self.checkChannelMessage(message[1])
            elif message[0] == 'Part':
                pass
            elif message[0] == 'Join':
                pass
            elif message[0] == "Sub":
                self.checkSubMessage(message[1])

    #change to react to ! only
    def checkChannelMessage(self, message):
        if message.group('message').startswith("!"):
            if self.commands[0].get(message.group('channel'), None):
                for command in self.commands[0][message.group('channel')]:
                    if re.search(command[0], message.string):
                        for lines in command[2].split('\n'):
                            self.sendReply(self.executeCommand(command[0], lines, message.string))
                            sleep(0.1)
                            continue
                    if command[1]:
                        if re.search(command[1], message.string):
                            for lines in command[2].split('\n'):
                                self.sendReply(self.executeCommand(command[0], lines, message.string))
                                sleep(0.1)
                                continue
            # print(components.group('channel') is "lucas861223")
            # if components.group('channel') == "lucas861223":
            #     if components.group(11).startswith("!點名"):
            #         if not self.students.get(components.group("displayName")):
            #             self.students[components.group("displayName")] = self.studentCount
            #             self.sendReply('PRIVMSG #lucas861223 :' + components.group("displayName") + '你是第' + str(self.studentCount) + '號')
            #             self.studentCount = self.studentCount + 1
            #         else:
            #             self.sendReply(
            #                 'PRIVMSG #lucas861223 :' + components.group("displayName") + '你是第' + str(self.students.get(components.group("displayName"))) + '號')
            #         print(self.students)

    def checkSubMessage(self, message):
        print("aaaaaaaaaaaaaaaaaa")
        if self.commands[1].get(message.group("channelName"), None):
            print("bbbbbbbbbbbbbbbbbbbb")
            for lines in self.commands[1][message.group("channelName")].split('\n'):
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                self.sendReply(self.executeCommand(self.subMessage, lines, message.string))
                print(lines)
                sleep(0.1)

    def sendReply(self, message):
        self.clientIRC.sendMessage(message + ' \r\n')

    def executeCommand(self, command, reply, message):
        return re.sub(command, reply, message)
