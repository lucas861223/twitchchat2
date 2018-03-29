from BotThread import BotThread
import re
import os.path
from pathlib import Path
from queue import Queue

class Bot():
    SPECIFIC_USER_SPLIT = re.compile("[ ,]+")
    COMMAND_FOLDER_PATH = str(Path(__file__).parent.parent) + "\\Commands\\"
    def __init__(self):
        self.commands = None
        self.clientIRC = None
        self.botThread = None
        self.messageQueue = Queue()

    def connectIRC(self, clientIRC):
        self.clientIRC = clientIRC

    def shutDownBot(self):
        self.botThread.deActivateBotThread()
        del(self.botThread)

    def startBot(self):
        self.messageQueue.queue.clear()
        self.initializeCommands()
        self.botThread = BotThread(self.clientIRC, self.messageQueue)
        self.botThread.activateBotThread(self.commands)

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
                        response = self.compileResponsePattern(directory, lines[4:])
                        if not command.startswith('_'):
                            command = self.compileCommandPattern(command, lines[2][:-1], lines[3][:-1])
                            if not self.commands[0].get(directory, None):
                                self.commands[0][directory] = []
                            entry = len(self.commands[0][directory])
                            self.commands[0][directory].append([])
                            self.commands[0][directory][entry].append(command[0])
                            if len(command) > 1:
                                self.commands[0][directory][entry].append(command[1])
                            else:
                                self.commands[0][directory][entry].append(None)
                            self.commands[0][directory][entry].append(response)
                        else:
                            self.commands[1][directory] = response
        except Exception as e:
            print(e.args)
            self.shutDownBot()

    def compileCommandPattern(self, command, userGroup, specificUser):
        commands = []
        commandPattern = ''
        if userGroup == '1':
            commandPattern += '@badges=broadcaster/1'
        commandPattern += '.*(bits=(\d+);.*)?.*display-name=(?P<displayName>([^A-Za-z]*)|([^;]*));.*'
        if userGroup == '2':
            commandPattern += 'mod=1;'
        commandPattern += ".*"
        if userGroup == '3':
            commandPattern += 'subscriber=1;'
        commandPattern += ".*;.*user-id=(\d+);.*!(?P<user>[^@]+)@"
        if specificUser != '' and userGroup == '5':
            commandPattern += "(" + str("|").join(Bot.SPECIFIC_USER_SPLIT.split(specificUser)) + ")"
        elif specificUser != '' and not userGroup == '4':
            #need a better solution
            temp = ".*(bits=(\d+);.*)?.*display-name=(?P<displayName>([^A-Za-z]*)|([^;]*));.*user-id=(\d+);.*!(?P<user>[^@]+)@(" + str("|").join(Bot.SPECIFIC_USER_SPLIT.split(specificUser)) + ")\.tmi\.twitch\.tv PRIVMSG #(?P<channel>[^ ]+) :" + re.sub('@(?P<variableName>[^ ]+)@', '(?P<\\g<variableName>>[^ ]+)', command[:-1] + '( |$)') + ".*"
            commands.append(re.compile(temp))
            commandPattern += ".*"
        else:
            commandPattern += ".*"

        commandPattern += "\.tmi\.twitch\.tv PRIVMSG #(?P<channel>[^ ]+) :"
        commandPattern += re.sub('@(?P<variableName>[^ ]+)@', '(?P<\\g<variableName>>[^ ]+)', command[:-1] + '( |$)')
        commandPattern = re.sub("\.\*(\.\*)+", ".*", commandPattern)
        commands.append(re.compile(commandPattern + ".*"))
        return commands

    def compileResponsePattern(self, channelName, responsePattern):
        response = ''
        for lines in responsePattern:
            response += 'PRIVMSG #' + channelName + " :"
            response += re.sub('@(?P<variableName>[^@]+)@', '\\\\g<\\g<variableName>>', lines)
        return response