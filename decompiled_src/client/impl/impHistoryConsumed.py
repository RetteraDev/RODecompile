#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impHistoryConsumed.o
from gamestrings import gameStrings
import gamelog
import gameglobal
import utils
import gametypes

class ImpHistoryConsumed(object):
    """
    \xe5\x8e\x86\xe5\x8f\xb2\xe6\xb6\x88\xe8\xb4\xb9\xe8\xbf\x94\xe8\xbf\x98
    """

    def onQueryHistoryConsumedReward(self, rewardData):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe5\x8e\x86\xe5\x8f\xb2\xe6\xb6\x88\xe8\xb4\xb9\xe8\xbf\x94\xe8\xbf\x98\xe5\xa5\x96\xe5\x8a\xb1
        :param rewardData:
        {'actId':\xe6\xb4\xbb\xe5\x8a\xa8ID, 'status\xe2\x80\x99\xef\xbc\x9a\xe6\xb4\xbb\xe5\x8a\xa8\xe7\x8a\xb6\xe6\x80\x81(\xe8\xa7\x81HISTORY_CONSUMED_STATUS_NONE),returnPoint: \xe8\xbf\x94\xe8\xbf\x98\xe7\x82\xb9\xef\xbc\x8c
        \xe2\x80\x98remainScore\xe2\x80\x99\xef\xbc\x9a\xe5\x8f\xaf\xe5\x85\x91\xe6\x8d\xa2\xe7\xa7\xaf\xe5\x88\x86\xef\xbc\x8c\xe2\x80\x98gbIdgameStrings.TEXT_IMPHISTORYCONSUMED_16:{\xe5\x8f\xaf\xe7\x94\xa8\xe7\x9a\x84\xe5\xa5\x96\xe5\x8a\xb1\xe7\x9a\x84ID: (\xe5\xb7\xb2\xe9\xa2\x86\xe5\x8f\x96\xe6\xac\xa1\xe6\x95\xb0, \xe4\xbb\x8a\xe5\xa4\xa9\xe6\x98\xaf\xe5\x90\xa6\xe9\xa2\x86\xe5\x8f\x96\xe8\xbf\x87)}},
        'charge':\xe7\xb4\xaf\xe8\xae\xa1\xe5\x85\x85\xe5\x80\xbc\xe9\x9d\x9e\xe7\xbb\x91\xe5\xae\x9a\xe5\x85\x83\xe5\xae\x9d
        :return:
        """
        gameglobal.rds.ui.historyConsumed.onQueryHistoryConsumedReward(rewardData)
        gamelog.debug('@zhangkuo onQueryHistoryConsumedReward [rewardData]', str(rewardData))

    def onQueryHistoryConsumedStatus(self, data):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe5\x8e\x86\xe5\x8f\xb2\xe6\xb6\x88\xe8\xb4\xb9\xe8\xbf\x94\xe8\xbf\x98\xe7\x8a\xb6\xe6\x80\x81
        :param data:
        {'actId':\xe6\xb4\xbb\xe5\x8a\xa8ID, 'status\xe2\x80\x99\xef\xbc\x9a\xe6\xb4\xbb\xe5\x8a\xa8\xe7\x8a\xb6\xe6\x80\x81(\xe6\x96\xb0\xe5\xa2\x9e\xe5\x85\xa8\xe6\x96\xb0\xe7\x8a\xb6\xe6\x80\x81 HISTORY_CONSUMED_STATUS_JOINED_BY_MALL)}
        :return:
        """
        gamelog.debug('@zmm onQueryHistoryConsumedStatus [data]', str(data))
        if data and utils.checkHistoryConsumedActId(data.get('actId', 0)):
            status = data.get('status', 0)
            gameglobal.rds.ui.tianyuMall.historyConsumedStatus = status
            if status == gametypes.HISTORY_CONSUMED_STATUS_JOINED_BY_MALL:
                gameglobal.rds.ui.historyConsumed.banHistoryCosumeByMall()

    def onQueryHistoryConsumedFreezePlayer(self, gbId, roleName, hostId):
        """\xe6\x9f\xa5\xe8\xaf\xa2\xe8\xa2\xab\xe5\x86\xbb\xe7\xbb\x93\xe8\xa7\x92\xe8\x89\xb2\xe7\x9a\x84\xe8\xa7\x92\xe8\x89\xb2\xe5\x90\x8d\xe5\x92\x8c\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8ID"""
        gameglobal.rds.ui.historyConsumed.onQueryHistoryConsumedFreezePlayer(gbId, roleName, hostId)
        gamelog.debug('@zhangkuo onQueryHistoryConsumedFreezePlayer [gbId][roleName][hostId]', gbId, roleName, hostId)

    def onConfirmJoinHistoryConsumed(self):
        """\xe7\xa1\xae\xe8\xae\xa4\xe5\x8f\x82\xe4\xb8\x8e\xe5\x8e\x86\xe5\x8f\xb2\xe6\xb6\x88\xe8\xb4\xb9\xe8\xbf\x94\xe8\xbf\x98\xe6\xb4\xbb\xe5\x8a\xa8,\xe5\x86\xbb\xe7\xbb\x93\xe8\xb4\xa6\xe5\x8f\xb7\xe6\x88\x90\xe5\x8a\x9f"""
        gameglobal.rds.ui.historyConsumed.onConfirmJoinHistoryConsumed()
        gamelog.debug('@zhangkuo onConfirmJoinHistoryConsumed')

    def onTakeHistoryConsumedFixedReward(self, rewardId):
        """\xe9\xa2\x86\xe5\x8f\x96\xe5\x9b\xba\xe5\xae\x9a\xe5\xa5\x96\xe5\x8a\xb1"""
        gameglobal.rds.ui.historyConsumed.refreshRewardInfo(rewardId)
        gameglobal.rds.ui.historyConsumed.refreshInfo()
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        gamelog.debug('@zhangkuo onTakeHistoryConsumedFixedReward [rewardId]', rewardId)

    def onTakeHistoryConsumedVolatileReward(self, remainScore, items):
        """\xe9\xa2\x86\xe5\x8f\x96\xe5\x8f\xaf\xe9\x80\x89\xe5\xa5\x96\xe5\x8a\xb1"""
        gameglobal.rds.ui.historyConsumed.onTakeHistoryConsumedVolatileReward(remainScore, items)
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        gamelog.debug('@zhangkuo onTakeHistoryConsumedVolatileReward [remainScore][items]', remainScore, items)

    def onHistoryConsumedEnd(self, actId):
        """\xe5\x8e\x86\xe5\x8f\xb2\xe6\xb6\x88\xe8\xb4\xb9\xe8\xbf\x94\xe8\xbf\x98\xe6\xb4\xbb\xe5\x8a\xa8\xe7\xbb\x93\xe6\x9d\x9f"""
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        gameglobal.rds.ui.historyConsumed.hide()
        gamelog.debug('@zhangkuo onHistoryConsumedEnd [actId]', actId)

    def notifyApplyHistoryConsumed(self, actId, returnPoint, availableScore, isApplyed, isChoosedFromWeb):
        """
        \xe9\x80\x9a\xe7\x9f\xa5\xe6\x9c\x89\xe8\xb5\x84\xe6\xa0\xbc\xe5\x8f\x82\xe4\xb8\x8e\xe6\xb4\xbb\xe5\x8a\xa8\xe7\x9a\x84\xe7\x8e\xa9\xe5\xae\xb6\xe6\x98\xaf\xe5\x90\xa6\xe5\x8f\x82\xe4\xb8\x8e\xe6\xb4\xbb\xe5\x8a\xa8
        :param actId: \xe6\xb4\xbb\xe5\x8a\xa8ID
        :param returnPoint: \xe8\xbf\x94\xe8\xbf\x98\xe7\x82\xb9
        :param availableScore: \xe5\x8f\xaf\xe5\x85\x91\xe6\x8d\xa2\xe7\xa7\xaf\xe5\x88\x86
        :param isApplyed: \xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe7\xbb\x8f\xe5\x8f\x82\xe4\xb8\x8e\xe8\xbf\x87\xe6\xb4\xbb\xe5\x8a\xa8\xe4\xba\x86
        :param isChoosedFromWeb: \xe7\xbd\x91\xe9\xa1\xb5\xe7\xab\xaf\xe6\x98\xaf\xe5\x90\xa6\xe9\x80\x89\xe6\x8b\xa9\xe8\xbf\x87\xe4\xba\x86
        """
        gameglobal.rds.ui.historyConsumed.pushHistoryConsumedMessage(actId, returnPoint, availableScore, isApplyed, isChoosedFromWeb)
        gamelog.debug('@zhangkuo notifyApplyHistoryConsumed [actId][returnPoint][availableScore][isApplyed][isChoosedFromWeb]', actId, returnPoint, availableScore, isApplyed, isChoosedFromWeb)

    def updateHistoryConsumedRewardState(self, isAvailable):
        """\xe6\x9b\xb4\xe6\x96\xb0\xe6\x98\xaf\xe5\x90\xa6\xe6\x9c\x89\xe5\x8f\xaf\xe9\xa2\x86\xe5\x8f\x96\xe7\x9a\x84\xe5\x9b\xba\xe5\xae\x9a\xe5\xa5\x96\xe5\x8a\xb1"""
        gameglobal.rds.ui.historyConsumed.setAvailable(isAvailable)
        gamelog.debug('@zhangkuo updateHistoryConsumedRewardState', isAvailable)