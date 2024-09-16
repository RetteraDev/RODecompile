#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerLottery.o
import gameglobal

class ImpPlayerLottery(object):

    def onGetRewardByLottery(self, page, pos, lotteryId, issueTime, nuid, flag, rank):
        gameglobal.rds.ui.lottery.onGetRewardByLottery(page, pos, lotteryId, issueTime, nuid, flag, rank)

    def onQueryLottery(self, page, pos, lotteryId, issueTime, nuid, flag, rank):
        gameglobal.rds.ui.lottery.onQueryLottery(page, pos, lotteryId, issueTime, nuid, flag, rank)
