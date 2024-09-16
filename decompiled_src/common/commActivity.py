#Embedded file name: I:/bag/tmp/tw2/res/entities\common/commActivity.o
import gametypes
from userDictType import UserDictType
from userSoleType import UserSoleType
from userType import UserDispatch, UserMultiDispatch
from cdata import activity_reverse_data as ARRD
from data import activity_basic_data as ABD
from data import group_luck_joy_data as GLJD

def getActivityIdByRef(refId, refType):
    if not ARRD.data.has_key(refType):
        return 0
    arrd = ARRD.data[refType]
    if not arrd.has_key(refId):
        return 0
    return arrd[refId]


def canExtraActivity(refId, refType, points, rewardExtraEvents):
    activityId = getActivityIdByRef(refId, refType)
    if not ABD.data.has_key(activityId):
        return False
    abd = ABD.data[activityId]
    extraCnt = abd.get('extraCnt', 0)
    curExtraCnt = rewardExtraEvents.get(activityId, 0)
    if extraCnt == 0 or extraCnt > 0 and extraCnt <= curExtraCnt:
        return False
    rewardPoints = abd.get('extraPoint', 0)
    if rewardPoints == 0 or rewardPoints > points:
        return False
    return True


class GroupLuckJoySlotVal(UserSoleType):

    def __init__(self, tp = 0, itemId = 0, cnt = 0, gbId = 0, stype = 0, sid = 0):
        self.tp = tp
        self.itemId = itemId
        self.cnt = cnt
        self.gbId = gbId
        self.stype = stype
        self.sid = sid

    def getDTO(self):
        return (self.tp,
         self.gbId,
         self.stype,
         self.sid,
         self.cnt)

    def fromDTO(self, dto):
        self.tp, self.gbId, self.stype, self.sid, self.cnt = dto
        self.itemId = self.sid


class GroupLuckJoyMemberVal(UserSoleType, UserDispatch):

    def __init__(self, name = '', box = None, readOnly = False):
        self.name = name
        self.box = box
        self.readOnly = readOnly


class GroupLuckJoyVal(UserSoleType):

    def __init__(self, nuid = 0, aid = 0, leaderGbId = 0):
        self.nuid = nuid
        self.aid = aid
        self.leaderGbId = leaderGbId
        self.members = {}
        self.slots = []

    def genInitSlots(self):
        data = GLJD.data.get(self.aid)
        num = data.get('normalNum', 0) + data.get('specialNum', 0)
        for i in range(num):
            self.slots.append(GroupLuckJoySlotVal())

    def getMember(self, gbId):
        mVal = self.members.get(gbId)
        if not mVal:
            mVal = GroupLuckJoyMemberVal()
            self.members[gbId] = mVal
        return mVal
