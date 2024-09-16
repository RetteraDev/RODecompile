#Embedded file name: I:/bag/tmp/tw2/res/entities\common/homePerson.o
import const
from userSoleType import UserSoleType

class HomePerson(UserSoleType):

    def __init__(self, roomId = 0, state = const.HOME_ROOM_STATE_NONE, tcreate = 0, ownerGbID = 0, ownerName = ''):
        super(HomePerson, self).__init__()
        self.roomId = roomId
        self.state = state
        self.tcreate = tcreate
        self.ownerGbID = ownerGbID
        self.ownerName = ownerName
        self.curLineNo = 0
        self.curFloorNo = 0
        self.curRoomNo = 0
        self.curRoomId = 0
        self.lineNo = 0
        self.floorNo = 0
        self.roomNo = 0
        self.fittingRoomLv = 1
        self.roomBox = None
        self.roomAccessRecord = []
        self.lastUseBackHomeSkillTime = 0
        self.erooms = []
        self.eRoomAuthDict = {}
        self.eroomAuthType = 0
        self.roomSpaceType = 0

    def isOwner(self, gbID):
        return self.ownerGbID == gbID

    def isIn(self):
        return self.ownerGbID != 0

    def getCT(self):
        return self.tcreate

    def hasHome(self):
        return self.roomId > 0 or self.tcreate > 0

    def isActive(self):
        return self.state == const.HOME_ROOM_STATE_ACTIVE

    def exitHome(self):
        self.ownerGbID = 0
        self.ownerName = ''

    def inHomeRoom(self):
        return self.curLineNo > 0 and self.curFloorNo != 0 and self.curRoomNo > 0

    def inHomeFloor(self):
        return self.curLineNo > 0 and self.curFloorNo != 0 and self.curRoomNo == 0

    def inHomeEntrance(self):
        return self.curLineNo > 0 and not self.curFloorNo and not self.curRoomNo

    def enterRoom(self, owner, roomNo, roomBox, gbID, roleName):
        self.curRoomNo = roomNo
        self.roomBox = roomBox
        if gbID == 0:
            return
        if gbID not in (owner.gbId, owner.cellOfIntimacyTgt):
            newVisitor = True
            for tgbid, _ in self.roomAccessRecord:
                if tgbid == gbID:
                    newVisitor = False
                    break

            if newVisitor:
                self.roomAccessRecord.append((gbID, roleName))
                if len(self.roomAccessRecord) > const.MAX_HOME_ACCESS_RECORD_NUM:
                    self.roomAccessRecord = self.roomAccessRecord[1:]

    def leaveRoom(self, owner):
        self.curRoomNo = 0
        self.roomBox = None

    def reset(self):
        self.typ = 0
        self.tcreate = 0
        self.ownerGbID = 0
        self.ownerName = ''
