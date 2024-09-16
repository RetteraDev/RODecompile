#Embedded file name: I:/bag/tmp/tw2/res/entities\common/multiCarrier.o
import BigWorld
import const
import gametypes
from userDictType import UserDictType
from data import multi_carrier_data as MCD

class MultiCarrierCopy(UserDictType):

    def __init__(self, spaceNo = 0, position = (0, 0, 0), direction = (0, 0, 0), carrierBox = None):
        self.initData(spaceNo, position, direction)
        self.carrierBox = carrierBox

    def resetAll(self):
        self.spaceNo = 0
        self.position = (0, 0, 0)
        self.direction = (0, 0, 0)
        self.carrierBox = None

    def initData(self, spaceNo, position, direction):
        self.spaceNo = spaceNo
        self.position = position
        self.direction = direction


class MultiCarrier(UserDictType):

    def __init__(self, carrierEntId = 0, carrierNo = 0, carrierEnterType = 0, carrierState = 0):
        super(MultiCarrier, self).__init__()
        self.carrierEntId = carrierEntId
        self.carrierNo = carrierNo
        self.carrierEnterType = carrierEnterType
        self.carrierState = carrierState

    def _lateReload(self):
        super(MultiCarrier, self)._lateReload()

    def isCarrierMajor(self, ownerID):
        if not ownerID:
            return False
        return ownerID == self.getCarrierHeaderEntId()

    def isCarrierZaijuNo(self, zaijuNo):
        return zaijuNo in MCD.data.get(self.carrierNo, {}).get('bianshenOfPlace', {}).values()

    def isMarriageMultiCarrier(self):
        return MCD.data.get(self.carrierNo, {}).get('isMarriageUse', 0)

    def getCamDist(self):
        return MCD.data.get(self.carrierNo, {}).get('camDist', [])

    def getCamScrollRange(self):
        return MCD.data.get(self.carrierNo, {}).get('camScrollRange', ())

    def getCamHeight(self):
        return MCD.data.get(self.carrierNo, {}).get('camHeight', ())

    def getCamKey(self):
        return MCD.data.get(self.carrierNo, {}).get('camKey', ())

    def getCarrierHeaderEnt(self):
        return BigWorld.entities.get(self.getCarrierHeaderEntId())

    def getCarrierHeaderEntId(self):
        return self.getEntIdByIdx(const.CARRIER_MAJOR_IDX)

    def getMajorPrivilegeType(self):
        majorPrivilege = MCD.data.get(self.carrierNo, {}).get('isMajorBind', 0)
        return majorPrivilege

    def isCarrierFull(self, isAllowMajor):
        maxNum = MCD.data.get(self.carrierNo, {}).get('maxPlaceNum', 0)
        majorPrivilege = self.getMajorPrivilegeType()
        idxList = self.values()
        if majorPrivilege != gametypes.MULTI_CARRIER_MAJOR_PRIVILEGE_NONE and not isAllowMajor:
            if const.CARRIER_MAJOR_IDX not in idxList:
                if len(idxList) >= maxNum - 1:
                    return gametypes.MULTI_CARRIER_IS_DUMMY_FULL
                else:
                    return gametypes.MULTI_CARRIER_IS_PLACE_AVAILABLE
        if len(idxList) >= maxNum:
            return gametypes.MULTI_CARRIER_IS_REAL_FULL
        else:
            return gametypes.MULTI_CARRIER_IS_PLACE_AVAILABLE

    def isReachCreateNum(self):
        maxNum = MCD.data.get(self.carrierNo, {}).get('carrierStartNum', 0)
        if len(self) >= maxNum:
            return True
        return False

    def isAutoStart(self):
        if MCD.data.get(self.carrierNo, {}).get('isAutoStart'):
            return True
        return False

    def isSingleMultiCarrier(self):
        maxNum = MCD.data.get(self.carrierNo, {}).get('maxPlaceNum', 0)
        if maxNum == const.MULTI_CARRIER_SINGLE_NUM:
            return True
        return False

    def isReachDisbandNum(self):
        minNum = MCD.data.get(self.carrierNo, {}).get('minPlaceNum', 0)
        if not minNum or len(self) >= minNum:
            return False
        return True

    def checkAllMemberIsNear(self):
        for entId in self.iterkeys():
            if not BigWorld.entities.get(entId):
                return False

        return True

    def getEntIdByIdx(self, idx):
        for entId, entIdx in self.iteritems():
            if entIdx == idx:
                return entId

        return 0

    def getCarrierEnt(self):
        return BigWorld.entities.get(self.carrierEntId)

    def exchangeIdx(self, lIdx, rIdx, lEntId, rEntId = 0):
        if lEntId != self.getEntIdByIdx(lIdx) or rEntId != self.getEntIdByIdx(rIdx):
            return False
        self[lEntId] = rIdx
        if rEntId:
            self[rEntId] = lIdx
        return True

    def exchange(self, fEntId, tEntId):
        if fEntId not in self or tEntId not in self:
            return False
        fIdx = self[fEntId]
        self[fEntId] = self[tEntId]
        self[tEntId] = fIdx
        return True

    def joinCarrier(self, memberId, isAllowMajor, idx = None):
        if self.isCarrierFull(isAllowMajor):
            return False
        if not idx:
            idx = self.autoAssignInx(isAllowMajor)
            if not idx:
                return False
        elif self.getEntIdByIdx(idx):
            return False
        if not self.has_key(memberId):
            self[memberId] = idx
            return True
        return True

    def autoAssignInx(self, isAllowMajor):
        maxNum = MCD.data.get(self.carrierNo, {}).get('maxPlaceNum', 0)
        majorPrivilege = self.getMajorPrivilegeType()
        startIdx = const.CARRIER_MAJOR_IDX
        if majorPrivilege and not isAllowMajor:
            startIdx += 1
        for idx in xrange(startIdx, maxNum + 1):
            if not self.getEntIdByIdx(idx):
                return idx

        return 0

    def leave(self, leaveId):
        self.pop(leaveId, None)

    def resetAll(self):
        self.carrierEntId = 0
        self.carrierEnterType = 0
        self.carrierState = 0
        self.clear()

    def isReadyState(self):
        return self.carrierState == gametypes.MULTI_CARRIER_STATE_CHECK_READY

    def isRunningState(self):
        return self.carrierState == gametypes.MULTI_CARRIER_STATE_RUNNING

    def isNoneState(self):
        return self.carrierState == gametypes.MULTI_CARRIER_STATE_NONE

    def getCarrierHp(self):
        ent = BigWorld.entities.get(self.carrierEntId)
        if ent:
            return ent.carrierHpPercent

    def copyContents(self, carrier):
        if id(self) == id(carrier):
            return
        self.clear()
        self.update(carrier)
        self.carrierEntId = carrier.carrierEntId
        self.carrierNo = carrier.carrierNo
        self.carrierEnterType = carrier.carrierEnterType
        self.carrierState = carrier.carrierState
