import requests
import threading
from queue import Queue


class JSONDecoderThread(threading.Thread):

    def __init__(self, JSONDecoder):
        super().__init__(target=self.run)
        self.jsonDecoder = JSONDecoder
        self.queuedCall = Queue()
        self.setDaemon(True)
        self.setName('JSONDecoderThread')

    def addJob(self, call):
        self.queuedCall.put(call)

    def run(self):
        while True:
            event = self.queuedCall.get()
            if event[0] == 'set_badges':
                badges = requests.get(self.jsonDecoder.channelBadge.replace('channelID', event[2]),
                                      headers=self.jsonDecoder.headers).json()
                event[1].setBadgesIcon(badges)