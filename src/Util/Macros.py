import re
import os.path
from pathlib import Path

class Macros():
    MACRO_FOLDER_PATH = str(Path(__file__).parent.parent) + "\\Macros\\"
    def __init__(self, clientIRC):
        self.compileAllMacros()

    def compileAllMacros(self):
        self.macros = {}
        self.macros['global'] = []
        try:
            directories = [directory[1] for directory in os.walk(Macros.MACRO_FOLDER_PATH)]
            for directory in directories[0]:
                directory_path = os.path.join(Macros.MACRO_FOLDER_PATH, directory)
                files = [file[2] for file in os.walk(directory_path)]
                for file in files[0]:
                    lines = open(os.path.join(directory_path, file), 'r').readlines()
                    macro = lines[0]
                    response = self.compileResponsePattern(directory, lines[2])
                    command = self.compileCommandPattern(command, lines[3:] + '(| )')
                    if not self.commands[0].get(directory, None):
                        self.commands[0][directory] = []
                    entry = len(self.commands[0][directory])
                    self.commands[0][directory].append([])
                    self.commands[0][directory][entry].append(command)
                    self.commands[0][directory][entry].append(response)

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