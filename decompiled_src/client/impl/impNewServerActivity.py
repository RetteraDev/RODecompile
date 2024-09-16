#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impNewServerActivity.o
import gameglobal
import gametypes
import const
import gamelog
from guis import events
from data import new_server_activity_data as NSAD
from helpers.eventDispatcher import Event

class ImpNewServerActivity(object):

    def onNewServerJingSuFubenEnd(self, data):
        pass

    def onQueryFirstKillData(self, data):
        gamelog.debug('ypc@ onQueryFirstKillData!', data)
        evt = Event(events.EVENT_NEW_SERVICE_FIRST_KILL, {'data': data})
        gameglobal.rds.ui.dispatchEvent(evt)

    def onQueryNSDailyGiftData(self, data):
        gameglobal.rds.ui.newServiceSecretMerchant.rewardData = data
        gameglobal.rds.ui.newServiceSecretMerchant.showRewards()

    def onQueryNSLotteryIssueData(self, lotteryId, lotteryTime, data):
        gamelog.debug('@yj onQueryNSLotteryIssueData!', lotteryId, lotteryTime, data)
        nsLotteryId = NSAD.data.get('lotteryId', 0)
        globalLotteryId = NSAD.data.get('globalLotteryId', 0)
        if lotteryId == nsLotteryId:
            gameglobal.rds.ui.newServiceLottery.updateLotteryData(lotteryId, lotteryTime, data)
        elif lotteryId == globalLotteryId:
            gameglobal.rds.ui.welfareLottery.updateLotteryData(lotteryId, lotteryTime, data)

    def onGetTreasureBoxWithExtraBonus(self, data):
        if not data:
            return
        buffTreasureBoxIds = []
        for boxId, bonusType in data:
            buffTreasureBoxIds.append((boxId, bonusType))

        self.buffTreasureBoxIds = buffTreasureBoxIds
