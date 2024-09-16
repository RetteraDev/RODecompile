#Embedded file name: I:/bag/tmp/tw2/res/entities\common/itemRedemption.o
from userSoleType import UserSoleType
from userDictType import UserDictType

class ItemRedemptionVal(UserSoleType):

    def __init__(self, item = None, tStart = 0, tEnd = 0, cash = 0, coin = 0, fromGbId = 0, fromRole = '', toGbId = 0, toRole = '', tDeliver = 0, lock = False, opNUID = 0):
        self.item = item
        self.tStart = tStart
        self.tEnd = tEnd
        self.tDeliver = tDeliver
        self.cash = cash
        self.coin = coin
        self.fromGbId = fromGbId
        self.fromRole = fromRole
        self.toGbId = toGbId
        self.toRole = toRole
        self.lock = lock
        self.opNUID = opNUID

    def _lateReload(self):
        super(ItemRedemptionVal, self)._lateReload()
        if self.item:
            self.item.reloadScript()

    def getScheduleTime(self):
        return self.tDeliver or self.tEnd

    def getDTO(self):
        return (self.item,
         self.tStart,
         self.tEnd,
         self.tDeliver,
         self.cash,
         self.coin,
         self.fromGbId,
         self.fromRole,
         self.toGbId,
         self.toRole)

    def fromDTO(self, dto):
        self.item, self.tStart, self.tEnd, self.tDeliver, self.cash, self.coin, self.fromGbId, self.fromRole, self.toGbId, self.toRole = dto
        return self


class ItemRedemption(UserDictType):

    def _lateReload(self):
        super(ItemRedemption, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()
