import requests
import threading
from queue import Queue
import socket
import re

class BotThread(threading.Thread):
    MESSAGE_PATTERN = re.compile('@badges=([^;]*);.*(bits=(\d+);.*)?.*display-name=(?P<displayName>([^A-Za-z]*)|([^;]*));.*user-id=(\d+);.*:(?P<user>[^!]+)!.*#(?P<channel>[^ ]+) :(ACTION )?(.*)')
    def __init__(self, clientIRC, commands):
        super().__init__(target=self.run)
        self.setDaemon(True)
        self.setName('BotThread')
        self.channelMessagePattern = clientIRC.channelMessagePattern
        self.senderSocket = clientIRC.sendSocket
        self.clientIRC = clientIRC
        self.receiveSocket = clientIRC.activateSocket(socket.socket())
        self.isRunning = True
        self.commands = commands
        self.isHoldingMessage = False
        self.joinedChannel = clientIRC.joinedChannel
        self.joinedChannel.subscribe(self)
        self.subMessage = re.compile('.*display-name=(?P<displayName>[^;]*).*;login=(?P<id>[^;]*).*;msg-id=(?P<messageId>[^;]*)(;msg-param-months=(?P<month>[\d]+))?.*;msg-param-sub-plan-name=(?P<subPlanName>[^;]+)(;msg-param-sub-plan=(?P<subPlan>[\d]+))?.*;.* USERNOTICE #(?P<channelName>[^ ]+).*')
        for channel in self.joinedChannel.getJoinedChannel():
            self.notifyChannelsChanged(True, channel)
        self.start()

    def deActivateBot(self):
        self.isRunning = False
        for channelName in self.joinedChannel.getJoinedChannel():
            self.notifyChannelsChanged(False, channelName)
        self.join()
        self.stop()

    def run(self):
        while self.isRunning:
            try:
                rawMessage = self.receiveSocket.recv(1024)
                if len(rawMessage) == 0:
                    print('bot thread disconnected')
                    self.deActivateBot()
                rawMessage = rawMessage.decode('utf-8')
                if self.isHoldingMessage:
                    rawMessage = self.heldMessage + rawMessage
                    self.isHoldingMessage = False
                if rawMessage.endswith('\r\n') == False:
                    self.isHoldingMessage = True
                    self.heldMessage = rawMessage[rawMessage.rfind('\r\n'):]
                    rawMessage = rawMessage[0:rawMessage.rfind('\r\n')]
                for message in rawMessage.split('\r\n'):
                    channelMessage = re.search(self.channelMessagePattern, message)
                    if channelMessage:
                        self.checkChannelMessage(message)
                    #not doing whisper yet
                    elif ' USERNOTICE ' in message:
                        self.checkSubMessage(message)
                    elif message.startswith('PING'):
                        self.receiveSocket.send((message.replace('PING', 'PONG') + '\r\n').encode('utf-8'))

            except OSError:
                pass
    #change to react to ! only
    def checkChannelMessage(self, message):
        components = re.search(BotThread.MESSAGE_PATTERN, message)
        if components.group(11).startswith("!"):
            if self.commands[0].get(components.group(9), None):
                for command in self.commands[0][components.group(9)]:
                    if re.search(command[0], message):
                        self.sendReply(self.executeCommand(command[0], command[1], message))

    def checkSubMessage(self, message):
        for command in self.commands[1]:
            if '#' + command in message:
                self.sendReply(self.executeCommand(self.subMessage, self.commands[1][command], message))

    def sendReply(self, message):
        self.clientIRC.sendMessage(message + ' \r\n')

    def executeCommand(self, command, reply, message):
        return re.sub(command, reply, message)

    def stop(self):
        sock = self.receiveSocket
        self.receiveSocket = None
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        self.receiveSocketRunning = False
        self.join()

    def notifyChannelsChanged(self, join, channelName):
        if join:
            if self.commands[1].get(channelName, None) or self.commands[0].get(channelName, None):
                self.clientIRC.joinChannelWithSocket(self.receiveSocket, channelName)
        else:
            self.clientIRC.leaveChannelWithSocket(self.receiveSocket, channelName)