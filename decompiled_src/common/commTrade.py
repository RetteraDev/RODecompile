#Embedded file name: I:/bag/tmp/tw2/res/entities\common/commTrade.o
import copy
import const
from userSoleType import UserSoleType
from data import sys_config_data as SCD

class ValuableTradeVal(UserSoleType):

    def __init__(self, nuid = 0, tradeType = 0, items = [], peerGbId = 0, peerRole = '', tTrade = 0, cash = 0):
        super(ValuableTradeVal, self).__init__()
        self.nuid = nuid
        self.tradeType = tradeType
        self.items = copy.deepcopy(items)
        self.peerGbId = peerGbId
        self.peerRole = peerRole
        self.tTrade = tTrade
        self.cash = cash

    def _lateReload(self):
        super(ValuableTradeVal, self)._lateReload()
        for v in self.items:
            v.reloadScript()

    def getAvailTime(self):
        return self.tTrade + SCD.data.get('valuableItemLatchTime', const.VALUABLE_ITEM_LATCH_TIME)

    def getDTO(self):
        return (self.nuid,
         self.tradeType,
         self.items,
         self.peerGbId,
         self.peerRole,
         self.tTrade,
         self.cash)

    def fromDTO(self, dto):
        self.nuid, self.tradeType, self.items, self.peerGbId, self.peerRole, self.tTrade, self.cash = dto
        return self
