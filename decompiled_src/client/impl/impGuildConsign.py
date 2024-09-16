#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impGuildConsign.o
import copy
import random
import BigWorld
import const
import formula
import gamelog
import gametypes
import utils
import gameglobal

class ImpGuildConsign(object):

    def onGuildConsignStart(self):
        pass

    def onUpdateGuildConsignGoodDetail(self, goodDetail, ver):
        gameglobal.rds.ui.guildAuctionGuild.updateItemInfo(goodDetail)

    def onGuildConsignGoodSellOut(self, goodUUID, ver):
        gameglobal.rds.ui.guildAuctionGuild.deleteItemInfo(goodUUID)

    def onUpdateGuildConsignMaxProfit(self, maxProfit):
        gameglobal.rds.ui.guildAuctionGuild.updateMaxProfit(maxProfit)

    def onUpdateGuildConsignStates(self, states):
        gameglobal.rds.ui.guildAuctionGuild.updateStateDict(states)

    def onUpdateGuildConsignGoodsHistory(self, goodsHistory, ver):
        gameglobal.rds.ui.guildAuctionGuild.updateHistoryInfoList(goodsHistory, ver)

    def onGuildConsignGoodsOutOfData(self):
        gameglobal.rds.ui.guildAuctionGuild.queryInfo()
