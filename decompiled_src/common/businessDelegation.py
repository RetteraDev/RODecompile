#Embedded file name: I:/bag/tmp/tw2/res/entities\common/businessDelegation.o
import BigWorld
if BigWorld.component != 'client':
    import Netease
import utils
from userSoleType import UserSoleType
from userDictType import UserDictType
from data import business_config_data as BCD

class AccBusiness(UserSoleType):

    def __init__(self, nuid, gbId, roleName):
        super(AccBusiness, self).__init__()
        self.acNUID = nuid
        self.acGbId = gbId
        self.acRoleName = roleName
        self.acWhen = utils.getNow()
        self.compWhen = 0

    def isFinish(self):
        return self.compWhen > 0


class BusinessDelegationVal(UserDictType):

    def __init__(self, gbId, roleName, questLoopId, dgtCnt, loopCashReward):
        super(BusinessDelegationVal, self).__init__()
        self.gbId = gbId
        self.roleName = roleName
        self.questLoopId = questLoopId
        self.dgtCnt = dgtCnt
        self.loopCashReward = loopCashReward
        self.tWhen = utils.getNow()

    def getUnfinishCnt(self):
        finishCnt = 0
        for accBusiness in self.itervalues():
            if accBusiness.isFinish():
                finishCnt += 1

        return self.dgtCnt - finishCnt

    def hasUnfinishBusiness(self, acGbId):
        for accBusiness in self.itervalues():
            if accBusiness.acGbId == acGbId and not accBusiness.isFinish():
                return True

        return False

    def _lateReload(self):
        super(BusinessDelegationVal, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()


class BusinessDelegations(UserDictType):

    def __init__(self):
        super(BusinessDelegations, self).__init__()
        self.dailyDgtCnt = BCD.data.get('daliyDgtCnt', 0)
        self.curDgtCnt = 0

    def hasDgtByGbId(self, questLoopId, gbId):
        for bdVal in self.itervalues():
            if gbId == bdVal.gbId and bdVal.questLoopId == questLoopId:
                return True

        return False

    def addBusinessDgt(self, gbId, roleName, questLoopId, dgtCnt, loopCashReward):
        nuid = Netease.getNUID()
        val = BusinessDelegationVal(gbId, roleName, questLoopId, dgtCnt, loopCashReward)
        self[nuid] = val
        self.curDgtCnt += dgtCnt
        return nuid

    def accBusinesDgt(self, nuid, gbId, roleName, questLoopId):
        if not self.has_key(nuid):
            return False
        if self[nuid].dgtCnt <= len(self[nuid]):
            return False
        if self[nuid].questLoopId != questLoopId:
            return False
        for accBusiness in self[nuid].itervalues():
            if accBusiness.acGbId == gbId and not accBusiness.isFinish():
                return False

        if self[nuid].gbId == gbId:
            return False
        acNUID = Netease.getNUID()
        self[nuid][acNUID] = AccBusiness(acNUID, gbId, roleName)
        return True

    def compBusinessDgt(self, nuid, gbId, questLoopId):
        if not self.has_key(nuid):
            return False
        if self[nuid].questLoopId != questLoopId:
            return False
        for accBusiness in self[nuid].itervalues():
            if accBusiness.acGbId == gbId and not accBusiness.isFinish():
                accBusiness.compWhen = utils.getNow()

        finishCnt = 0
        for accBusiness in self[nuid].itervalues():
            if not accBusiness.isFinish():
                break
            else:
                finishCnt += 1
        else:
            if self[nuid].dgtCnt == finishCnt:
                self.pop(nuid)

    def _lateReload(self):
        super(BusinessDelegations, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()
