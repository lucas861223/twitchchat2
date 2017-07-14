import socket
import re
import threading
import time
from SystemMessageProcessor import *

class ClientIRC:
    def __init__(self, chatScreen):
        file = open('C:\\Users\\lucas\\Python Workspace\\TwitchChat\\src\\login', 'r')
        self.nickname = file.readline()
        self.password = file.readline()
        file.close()
        self.receiveSocket = socket.socket()
        self.sendSocket = socket.socket()
        self.receiveSocketRunning = False
        self.chatScreen = chatScreen
        self.systemMessagePocessor = SystemMessageProcessor(self.chatScreen)
        self.systemMessageThread = self.systemMessagePocessor.systemMessageThread
        self.holdMessage = False
        self.heldMessage = ''
        self.channelMessagePattern = re.compile('.*PRIVMSG (#[^ ]*) :')

    def start(self):
        self.receiveSocket.connect(('irc.chat.twitch.tv', 6667))
        self.receiveSocket.send('CAP REQ :twitch.tv/membership\r\n'.encode('utf-8'))
        self.receiveSocket.send('CAP REQ :twitch.tv/commands\r\n'.encode('utf-8'))
        self.receiveSocket.send('CAP REQ :twitch.tv/tags\r\n'.encode('utf-8'))
        self.sendSocket.connect(('irc.chat.twitch.tv', 6667))
        self.sendSocket.send('CAP REQ :twitch.tv/membership\r\n'.encode('utf-8'))
        self.sendSocket.send('CAP REQ :twitch.tv/commands\r\n'.encode('utf-8'))
        self.sendSocket.send('CAP REQ :twitch.tv/tags\r\n'.encode('utf-8'))
        self.sendSocket.send('PASS {}\r\n'.format(self.password).encode('utf-8'))
        self.sendSocket.send('NICK {}\r\n'.format(self.nickname).encode('utf-8'))
        self.receiveSocket.send('PASS {}\r\n'.format(self.password).encode('utf-8'))
        self.receiveSocket.send('NICK {}\r\n'.format(self.nickname).encode('utf-8'))
        self.receiveSocketRunning = True

        response = self.receiveSocket.recv(1024).decode('utf-8')
        if response == ':tmi.twitch.tv NOTICE * :Login authentication failed\r\n':
            self.stop()
            raise RuntimeError('Login authentication failed')


        self.receiveThread = threading.Thread(target=self.receivingMessage)
        self.receiveThread.setDaemon(True)
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
                if self.holdMessage:
                    response = self.heldMessage + response
                    self.holdMessage = False
                if response.endswith('\r\n') == False:
                    self.holdMessage = True
                    self.heldMessage = response[response.rfind('\r\n'):]
                    response = response[0:response.rfind('\r\n')]

                for responses in response.split('\r\n'):
                    if responses.startswith('PING'):
                        self.receiveSocket.send((responses.replace('PING', 'PONG') + '\r\n').encode('utf-8'))
                    else:
                        message = re.search(self.channelMessagePattern, responses)
                        if message is None:
                            self.systemMessageThread.run(responses)
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

    def sendMessage(self, message):
        self.sendSocket.send(message.encode('utf-8'))

    def leaveChannel(self, channelName):
        self.receiveSocket.send('PART {}\r\n'.format(channelName).encode('utf-8'))

    def joinChannel(self, channelName):
        self.receiveSocket.send('JOIN #{}\r\n'.format(channelName).encode('utf-8'))