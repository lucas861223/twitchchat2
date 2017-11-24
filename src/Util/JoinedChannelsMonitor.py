class JoinedChannelsMonitor:
    def __init__(self):
        self.joinedChannels = []
        self.subscriber = []

    def getJoinedChannel(self):
        return self.joinedChannels

    def joinChannel(self, channelName):
        self.joinedChannels.append(channelName)
        self.notifyChannelsChanged(True, channelName)

    def leaveChannel(self, channelName):
        self.joinedChannels.remove(channelName[1:])
        self.notifyChannelsChanged(False, channelName)

    def notifyChannelsChanged(self, join, channelName):
        for object in self.subscriber:
            object.notifyChannelsChanged(join, channelName)

    def subscribe(self, subscriber):
        self.subscriber.append(subscriber)