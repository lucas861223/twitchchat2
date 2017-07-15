import requests
import threading

class JSONDecoder:
    headers = {'Accept': 'application/vnd.twitchtv.v5+json'}
    channelBadge = 'https://api.twitch.tv/kraken/chat/channelID/badges'
    def __init__(self):
        file = open('../setting/clientID', 'r')
        JSONDecoder.headers['Client-ID'] = file.readline()
        file.close()
        self.jsonDecoderThread = JSONDecoderThread(JSONDecoder)



class JSONDecoderThread(threading.Thread):

    def __init__(self, JSONDecoder):
        super().__init__(target=self.run, args=('',))
        self.jsonDecoder = JSONDecoder
        self.daemon = True

    def run(self, call):
        if call[0] == 'set_badges':
            call[1].setBadgesIcon(requests.get(self.jsonDecoder.channelBadge.replace('channelID', call[2]), headers=self.jsonDecoder.headers).json())


