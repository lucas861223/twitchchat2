from threading import Thread
from BotThread import BotThread
import re
import os.path
from pathlib import Path

class Bot():
    COMMAND_FOLDER_PATH = str(Path(__file__).parent.parent) + "\\Commands\\"
    def __init__(self, clientIRC):
        self.initializeCommands()
        self.botThread = BotThread(clientIRC, self.commands)

    def shutDownBot(self):
        self.botThread.deActivateBot()

    def initializeCommands(self):
        self.commands = [{}, {}]
        try:
            directories = [directory[1] for directory in os.walk(Bot.COMMAND_FOLDER_PATH)]
            for directory in directories[0]:
                directory_path = os.path.join(Bot.COMMAND_FOLDER_PATH, directory)
                files = [file[2] for file in os.walk(directory_path)]
                for file in files[0]:
                    lines = open(os.path.join(directory_path, file), 'r').readlines()
                    if 'On' in lines[0]:
                        command = lines[1]
                        response = self.compileResponsePattern(directory, lines[2])
                    if not str.startswith(command, '_'):
                        command = self.compileCommandPattern(command, lines[3:])
                        if not self.commands[0].get(directory, None):
                            self.commands[0][directory] = []
                        entry = len(self.commands[0][directory])
                        self.commands[0][directory].append([])
                        self.commands[0][directory][entry].append(command)
                        self.commands[0][directory][entry].append(response)
                    else:
                        self.commands[1][directory] = response
        except Exception as e:
            print(e.args)
            self.shutDownBot()

    def compileCommandPattern(self, command, extraParameters):
        commandPattern = '@badges=([^;]*);.*(bits=(\d+);.*)?.*display-name=(?P<displayName>([^A-Za-z]*)|([^;]*));.*user-id=(\d+);.*:(?P<user>[^!]+)!.*.tmi.twitch.tv PRIVMSG #(?P<channel>[^ ]+) :'
        commandPattern += re.sub('@(?P<variableName>[^ ]+)@', '(?P<\\g<variableName>>[^ ]+)', command[:-1])
        return re.compile(commandPattern + ".*")

    def compileResponsePattern(self, channelName, responsePattern):
        response = 'PRIVMSG #' + channelName + " :"
        response += re.sub('@(?P<variableName>[^@]+)@', '\\\\g<\\g<variableName>>', responsePattern)
        return response