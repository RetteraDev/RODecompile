#Embedded file name: I:/bag/tmp/tw2/res/entities\common/commOpenServerBonus.o
import utils
import const
from userSoleType import UserSoleType
from userDictType import UserDictType
from data import open_server_bonus_data as OSBD

class OpenServerBonusVal(UserSoleType):

    def __init__(self, day = 0, vpLv = 0, state = 0, tPass = 0, tCreate = 0, tEnd = 0):
        self.day = day
        self.vpLv = vpLv
        self.state = state
        self.tPass = tPass
        self.tCreate = tCreate
        self.tEnd = tEnd

    def checkReady(self, owner, lastTime):
        if self.state != const.OPEN_SERVER_BONUS_STATE_WAITING:
            return False
        lastTime = max(lastTime, self.tCreate)
        now = utils.getNow()
        tPass = max(0, now - lastTime)
        if self.tPass + tPass >= const.OPEN_SERVER_READY_TIME:
            self.tPass = const.OPEN_SERVER_READY_TIME
            self.state = const.OPEN_SERVER_BONUS_STATE_READY
            return True
        self.tPass += tPass
        return False

    def getBonusId(self):
        data = OSBD.data.get(self.day)
        bonusIds = data.get('bonusId', 0)
        if not bonusIds:
            return 0
        bonusIdsDict = dict(bonusIds)
        bonusLevels = bonusIdsDict.keys()
        bonusLevels.sort()
        idx = utils.getListIndexInclude(self.vpLv, bonusLevels)
        if idx >= len(bonusLevels):
            return 0
        bonusId = bonusIdsDict.get(bonusLevels[idx])
        return bonusId

    def getLeftTime(self, lastTime):
        lastTime = max(self.tCreate, lastTime)
        now = utils.getNow()
        tPass = max(0, now - lastTime)
        return max(0, const.OPEN_SERVER_READY_TIME - (self.tPass + tPass))

    def getDTO(self):
        return (self.day,
         self.vpLv,
         self.state,
         self.tPass,
         self.tCreate)

    def fromDTO(self, dto):
        self.day, self.vpLv, self.state, self.tPass, self.tCreate = dto
        return self

    def getVpStorageAdd(self):
        data = OSBD.data.get(self.day)
        vpStorageAdd = data.get('vpStorage', ())
        if not vpStorageAdd:
            return 0
        vpStorageDict = dict(vpStorageAdd)
        bonusLevels = vpStorageDict.keys()
        bonusLevels.sort()
        idx = utils.getListIndexInclude(self.vpLv, bonusLevels)
        if idx >= len(bonusLevels):
            return 0
        res = vpStorageDict.get(bonusLevels[idx])
        return res


class OpenServerBonus(UserDictType):

    def __init__(self, lastTime = 0):
        self.lastTime = lastTime

    def _lateReload(self):
        super(OpenServerBonus, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def checkReady(self, owner):
        if not owner.enterTimeOfDayNoPersist:
            return
        if self.lastTime < owner.enterTimeOfDayNoPersist:
            self.lastTime = owner.enterTimeOfDayNoPersist
        days = self.keys()
        days.sort()
        for day in days:
            openServerBonus = self.get(day)
            tPass = openServerBonus.tPass
            openServerBonus.checkReady(owner, self.lastTime)
            self.lastTime += max(0, openServerBonus.tPass - tPass)

    def getMinLeftTime(self, owner):
        self.checkReady(owner)
        minLeftTime = -1
        days = self.keys()
        days.sort()
        openServerBonus = None
        for day in days:
            openServerBonus = self[day]
            if openServerBonus.state == const.OPEN_SERVER_BONUS_STATE_WAITING:
                minLeftTime = openServerBonus.getLeftTime(self.lastTime)
                break

        return (minLeftTime, openServerBonus and openServerBonus.day or 0)

    def transfer(self, owner):
        owner.client.onSendOpenServerBonus([ x.getDTO() for x in self.itervalues() ])

    def recalcTEnd(self):
        days = self.keys()
        days.sort()
        tEnd = utils.getNow()
        for day in days:
            openServerBonus = self[day]
            if openServerBonus.state == const.OPEN_SERVER_BONUS_STATE_WAITING:
                if not openServerBonus.tEnd:
                    openServerBonus.tEnd = tEnd + (const.OPEN_SERVER_READY_TIME - openServerBonus.tPass)
                tEnd = openServerBonus.tEnd
