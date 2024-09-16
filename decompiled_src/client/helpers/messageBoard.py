#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/messageBoard.o
import copy
import commonMessageBoard
from commonMessageBoard import FbMessageBoardBase, ConnectionInfo, MessageBoardEvent, MessageBoardMsg
import gametypes

class FbMessageBoard(FbMessageBoardBase):

    def __init__(self, fbNo = 0, hard = 0, publishType = gametypes.FB_PUBLISH_TYPE_DEFAULT, hasNum = 0, challengeWeekList = [], challengeTimeStr = '', desc = '', num = 0, connections = ConnectionInfo(), events = MessageBoardEvent(), msgs = MessageBoardMsg()):
        super(FbMessageBoard, self).__init__(fbNo, hard, hasNum, challengeWeekList, challengeTimeStr, desc, num)
        self.publishType = publishType
        self.connections = copy.deepcopy(connections)
        self.events = copy.deepcopy(events)
        self.msgs = copy.deepcopy(msgs)

    def fromDTO(self, dto):
        self.__init__(fbNo=dto.get('fbNo', 0), hard=dto.get('hard', 0), publishType=dto.get('publishType', 0), hasNum=dto.get('hasNum', 0), challengeWeekList=dto.get('challengeWeekList', ()), challengeTimeStr=dto.get('challengeTimeStr', ''), desc=dto.get('desc', ''), num=dto.get('num', 0), connections=ConnectionInfo().fromDTO(dto.get('connections', {})), events=MessageBoardEvent().fromDTO(dto.get('events', [])), msgs=MessageBoardMsg().fromDTO(dto.get('msgs', [])))
        return self

    def updateMessageBoard(self, dto):
        self.publishType = dto.get('publishType', 0)
        self.fbNo = dto.get('fbNo', 0)
        self.hard = dto.get('hard', 0)
        self.hasNum = dto.get('hasNum', 0)
        self.challengeWeekList = dto.get('challengeWeekList', ())
        self.challengeTimeStr = dto.get('challengeTimeStr', '')
        self.desc = dto.get('desc', '')
        self.num = dto.get('num', 0)

    def addEvent(self, event):
        if self.events != None:
            self.events.append(event)

    def sortEvent(self):
        self.events.sort(cmp=commonMessageBoard._cmpMessageBoardEvent)

    def addMsg(self, msg):
        if self.msgs != None:
            self.msgs.append(msg)

    def sortMsg(self):
        self.msgs.sort(cmp=commonMessageBoard._cmpMessageBoardMessage)

    def recoverMsgs(self, dto):
        self.msgs = MessageBoardMsg().fromDTO(dto)

    def addConnection(self, gbId, con):
        self.connections[gbId] = con

    def removeConnection(self, gbId, con):
        self.connections.pop(gbId, None)

    def updateConnectionOnlineStatus(self, gbId, isOn):
        if not self.connections.has_key(gbId):
            return
        item = self.connections[gbId]
        item.isOn = isOn

    def _lateReload(self):
        super(FbMessageBoard, self)._lateReload()
        self.connection.reloadScript()
