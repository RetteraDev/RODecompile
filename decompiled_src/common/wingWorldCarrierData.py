#Embedded file name: I:/bag/tmp/tw2/res/entities\common/wingWorldCarrierData.o
import BigWorld
import gametypes
import const
import wingWorldUtils
import sMath
from data import wing_world_carrier_data as WWCD
from userDictType import UserDictType

class WingWorldCarrierData(UserDictType):

    def __init__(self, carrierEntId = 0, carrierNo = 0, enterTypeOption = None, isBecomeLadder = False):
        self.carrierEntId = carrierEntId
        self.carrierNo = carrierNo
        if enterTypeOption is None:
            enterTypeOption = [0, 0, 1]
        self.enterTypeOption = enterTypeOption
        self.isBecomeLadder = isBecomeLadder
        super(WingWorldCarrierData, self).__init__()

    def initData(self, carrierEntId, carrierNo):
        self.carrierEntId = carrierEntId
        self.carrierNo = carrierNo

    def resetAll(self):
        self.carrierEntId = 0
        self.enterTypeOption = [0, 0, 1]
        self.carrierNo = 0
        self.isBecomeLadder = False
        self.clear()

    def getCarrierHeaderEnt(self):
        return BigWorld.entities.get(self.getCarrierHeaderEntId())

    def getCarrierHeaderEntId(self):
        return self.getEntIdByIdx(const.WING_WORLD_CARRIER_MAJOR_IDX)

    def getEntIdByIdx(self, idx):
        for entId, entIdx in self.iteritems():
            if entIdx == idx:
                return entId

        return 0

    def getEntByIdx(self, idx):
        return BigWorld.entities.get(self.getEntIdByIdx(idx))

    def isEmpty(self):
        return len(self) == 0

    def getCarrierEnt(self):
        return BigWorld.entities.get(self.carrierEntId)

    def joinCarrier(self, entId, isAllowMajor):
        if entId in self:
            return False
        idx = self.autoAssignIdx(isAllowMajor)
        if not idx:
            return False
        self[entId] = idx
        return idx

    def autoAssignIdx(self, isAllowMajor):
        maxNum = WWCD.data.get(self.carrierNo, {}).get('maxPlaceNum', 0)
        startIdx = const.WING_WORLD_CARRIER_MAJOR_IDX
        if not isAllowMajor:
            startIdx += 1
        for idx in xrange(startIdx, maxNum + 1):
            if not self.getEntIdByIdx(idx):
                return idx

        return 0

    def getBianshenIdByIdx(self, tgtEntId):
        tgtIdx = self.get(tgtEntId, 0)
        if not tgtIdx:
            return tgtIdx
        data = wingWorldUtils.getWingWorldCarrierConfigByNo(self.carrierNo)
        bianshenId = data.get('bianshenOfPlace', {}).get(tgtIdx, 0)
        return bianshenId

    def checkPlayerLeavedCarrier(self):
        inVaildPlayers = []
        carrierEnt = self.getCarrierEnt()
        if not carrierEnt:
            return inVaildPlayers
        for entId, idx in self.items():
            ent = BigWorld.entities.get(entId)
            if not ent or not sMath.inRange2D(40, ent.position, carrierEnt.position):
                self.pop(entId)
                inVaildPlayers.append(entId)

        return inVaildPlayers

    def dispatchCarrierInfoToPlayer(self, excludeEntId = ()):
        self.checkPlayerLeavedCarrier()
        for entId, idx in self.iteritems():
            if entId in excludeEntId:
                continue
            ent = BigWorld.entities.get(entId)
            ent.onDispatchCarrierInfoToPlayer(self)

    def leave(self, leaveId):
        if leaveId not in self:
            return False
        return self.pop(leaveId)

    def __repr__(self):
        return 'carrierEntId: {}, carrierNo: {}, enterTypeOption: {}, isLadder: {} idx: {}'.format(self.carrierEntId, self.carrierNo, self.enterTypeOption, self.isBecomeLadder, self.items())

    __str__ = __repr__
