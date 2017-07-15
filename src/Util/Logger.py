import time


class Logger:
    def  __inti__(self, channel):
        #there the config fil is stored
        strSaveLocation = 'test\\'
        self.file = open(strSaveLocation + channel)

    def logMessage(self, message):
        self.file.write('message')

    def close(self):
        self.file.write('Log closed')
        self.file.close()
