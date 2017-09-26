from PyQt5.QtWidgets import QLineEdit
import re

class EntryBox(QLineEdit):
    whisperSentFormat = '/w ([^ ]+) (.*)'
    def __init__(self, parent, chatScreen):
        super(EntryBox, self).__init__(parent)
        self.chatScreen = chatScreen
        self.returnPressed.connect(self.send)
        self.setFont(self.chatScreen.font)

    def send(self):
        channelName = self.chatScreen.widget(self.chatScreen.currentIndex()).channelName
        self.setText(self.text().strip())
        if self.text().startswith('/w'):
            if self.text().count(' ') > 1:
                result = re.search(EntryBox.whisperSentFormat, self.text())
                whisperReciver = result.group(1).lower()
                whisperChat = self.chatScreen.tabs.get('$' + whisperReciver, None)
                if whisperChat is None:
                    whisperChat = self.chatScreen.newWhisperChat(whisperReciver)
                whisperChat.newSentMessage(result.group(2))
                self.chatScreen.clientIRC.sendMessage('PRIVMSG #jtv :/w ' + whisperReciver + ' ' + result.group(2) + '\r\n')
        elif '#' in channelName:
            self.chatScreen.clientIRC.sendMessage('PRIVMSG ' + channelName + " :" + self.text() + '\r\n')
        else:
            self.chatScreen.clientIRC.sendMessage('PRIVMSG #jtv :/w ' + channelName[1:] + ' ' + self.text() + '\r\n')
            whisperChat = self.chatScreen.tabs[channelName]
            whisperChat.newSentMessage(self.text())
        self.setText('')