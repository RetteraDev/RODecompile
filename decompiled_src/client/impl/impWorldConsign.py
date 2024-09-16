#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impWorldConsign.o
import copy
import random
import BigWorld
import const
import formula
import gamelog
import gametypes
import utils
import gameglobal

class ImpWorldConsign(object):

    def onUpdateWorldConsignGoodDetail(self, goodDetail, ver):
        gameglobal.rds.ui.guildAuctionWorld.updateItemInfo(goodDetail)

    def onWorldConsignGoodSellOut(self, goodUUID, ver):
        gameglobal.rds.ui.guildAuctionWorld.deleteItemInfo(goodUUID)

    def onUpdateWorldConsignStates(self, states):
        gameglobal.rds.ui.guildAuctionWorld.updateStateDict(states)

    def onWorldConsignGoodsOutOfData(self):
        gameglobal.rds.ui.guildAuctionWorld.queryInfo()
