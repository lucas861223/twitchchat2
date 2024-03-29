import socket
import threading
import time
import re
from GUI.SubWindows.GeneralLoginDialog import GeneralLoginDialog
from Util.SystemMessageProcessor import SystemMessageProcessor
from Util.SettingManager import SettingManager


class ClientIRC:
    def __init__(self, chatScreen, bot):
        self.nickname = ""
        self.password = ""
        self.refreshToken = ""
        self.refreshTimer = 0

        self.chatScreen = chatScreen
        if not SettingManager.checkLoginFilesAreCompleted() or GeneralLoginDialog.reFreshTokenAndGetLogin() is None:
            generalDialog = GeneralLoginDialog(self)
            generalDialog.exec()
            if not SettingManager.checkLoginFilesAreCompleted():
                self.chatScreen.chatUI.centralWidget.mainWindow.close()
        [self.nickname, self.password, self.refreshToken] = SettingManager.getSettingFileContent(SettingManager.LOGIN_FILE)
        self.receiveSocket = socket.socket()
        self.sendSocket = socket.socket()
        self.receiveSocketRunning = False
        self.systemMessageProcessor = SystemMessageProcessor(self.chatScreen, bot.messageQueue)
        self.systemMessageThread = self.systemMessageProcessor.systemMessageThread
        self.isHoldingMessage = False
        self.heldMessage = ''
        self.channelMessagePattern = re.compile('.*PRIVMSG (#[^ ]*) :')
        bot.connectIRC(self)

    def openLogin(self):
        generalLoginDialog = GeneralLoginDialog(self)
        generalLoginDialog.accepted.connect(self.reconnect)
        generalLoginDialog.exec()

    def reconnect(self):
        old_nickName = self.nickname
        [self.nickname, self.password, self.refreshToken] = SettingManager.getSettingFileContent(SettingManager.LOGIN_FILE)
        if old_nickName != self.nickname:
            while self.chatScreen.count() > 0:
                self.chatScreen.closeTab(False)
            self.reLogin()
        self.chatScreen.joinDefaultChannel()

    def closeClientIRC(self):
        self.systemMessageThread.stopThread()
        self.systemMessageThread.newMessage("")
        self.systemMessageThread.join()
        self.receiveSocketRunning = False
        self.receiveSocket.close()
        self.receiveThread.join()
        self.sendSocket.close()

    def reLogin(self):
        self.closeClientIRC()
        self.receiveSocket = socket.socket()
        self.sendSocket = socket.socket()
        self.start()


    def start(self):
        self.activateSocket(self.receiveSocket)
        self.activateSocket(self.sendSocket)
        self.receiveSocketRunning = True
        response = self.receiveSocket.recv(1024).decode('utf-8')
        if response == ':tmi.twitch.tv NOTICE * :Login authentication failed\r\n':
            self.stop()
            raise RuntimeError('Login authentication failed')
        self.receiveThread = threading.Thread(target=self.receivingMessage)
        self.receiveThread.setDaemon(True)
        self.receiveThread.setName('receiveThread')
        self.receiveThread.start()
        self.sendSocket.setblocking(False)

    def receivingMessage(self):
        while self.receiveSocketRunning:
            try:
                response = self.receiveSocket.recv(1024)
                if len(response) == 0:
                    print('disconnected')
                    self.stop()
                response = response.decode('utf-8')
                if self.isHoldingMessage:
                    response = self.heldMessage + response
                if response.endswith('\r\n') == False:
                    self.isHoldingMessage = True
                    self.heldMessage = response[response.rfind('\r\n'):]
                    response = response[0:response.rfind('\r\n')]
                else:
                    self.isHoldingMessage = False
                for responses in response.split('\r\n'):
                    message = re.search(self.channelMessagePattern, responses)
                    if message is None:
                        if ' WHISPER ' in responses:
                            self.systemMessageThread.newMessage(time.strftime('%H:%M:%S') + ' ' + responses)
                        else:
                            if responses.startswith('PING'):
                                self.receiveSocket.send((responses.replace('PING', 'PONG') + '\r\n').encode('utf-8'))
                                self.sendSocket.send((responses.replace('PING', 'PONG') + '\r\n').encode('utf-8'))
                            else:
                                self.systemMessageThread.newMessage(responses)
                    else:
                        self.chatScreen.newMessage(message.group(1), time.strftime('%H:%M:%S') + ' ' + responses)
            except OSError:
                pass

    def stop(self):
        sock = self.receiveSocket
        self.receiveSocket = None
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        self.receiveSocketRunning = False
        sock = self.sendSocket
        self.sendSocket = None
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        if self.receiveThread:
            worker = self.receiveThread
            self.receiveThread = None
            worker.join()

    def activateSocket(self, socket):
        socket.connect(('irc.chat.twitch.tv', 6667))
        socket.send('CAP REQ :twitch.tv/membership\r\n'.encode('utf-8'))
        socket.send('CAP REQ :twitch.tv/commands\r\n'.encode('utf-8'))
        socket.send('CAP REQ :twitch.tv/tags\r\n'.encode('utf-8'))
        socket.send('PASS {}\r\n'.format(self.password).encode('utf-8'))
        socket.send('NICK {}\r\n'.format(self.nickname).encode('utf-8'))
        return socket

    def sendMessage(self, message):
        self.sendSocket.send(message.encode('utf-8'))

    def leaveChannel(self, channelName):
        self.leaveChannelWithSocket(self.receiveSocket, channelName)

    def leaveChannelWithSocket(self, socket, channelName):
        socket.send('PART {}\r\n'.format(channelName).encode('utf-8'))

    def joinChannel(self, channelName):
        self.joinChannelWithSocket(self.receiveSocket, channelName)

    def joinChannelWithSocket(self, socket, channelName):
        socket.send('JOIN #{}\r\n'.format(channelName).encode('utf-8'))
