#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/annal.o
import annalUtils

class AnnalReplay(object):

    def __init__(self, serverId = '', host = '', port = '', uuid = '', index = 0, live = False, fromStart = False):
        self.serverId = serverId
        self.host = host
        self.port = port
        self.uuid = uuid
        self.index = index
        self.live = live
        self.fromStart = fromStart
        self.waitingTimerId = 0
        self.promptTimerId = 0
        self.lastSpaceID = 0
        self.clientSpaceID = 0
        self.clientMap = ''
        self.locked = False
        self.messageBoxId = None

    def resetSpace(self):
        self.lastSpaceID = 0
        self.clientSpaceID = 0
        self.clientMap = ''

    def startReplay(self):
        annalUtils.playAnnal(self.serverId, self.uuid, host=self.host, port=self.port, index=self.index, live=self.live, fromStart=self.fromStart)
