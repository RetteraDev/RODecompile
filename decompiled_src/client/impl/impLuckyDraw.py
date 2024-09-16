#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impLuckyDraw.o
import BigWorld
import gameglobal
import gametypes

class ImpLuckyDraw(object):

    def onRequestLuckyDraw(self, RLLDId, drawConditionIdx, allItemDataList, code):
        if code == gametypes.LUCKY_DRAW_SUCCESS:
            gameglobal.rds.ui.activitySaleLuckyLottery.refreshTreasureBox()
            gameglobal.rds.ui.activitySaleLuckyLottery.startSelectItem(RLLDId, drawConditionIdx, allItemDataList)
            gameglobal.rds.ui.activitySaleLuckyLottery.refreshDrawCnt()
        elif code == gametypes.LUCKY_DRAW_FAILE:
            gameglobal.rds.ui.activitySaleLuckyLottery.processDrawingInfo(False)

    def onRequestLuckyDrawTreasureBox(self):
        gameglobal.rds.ui.activitySaleLuckyLottery.refreshTreasureBox()
        gameglobal.rds.ui.activitySale.refreshInfo()

    def pushOpenLuckyDraw(self, openDrawIdList):
        for RLLDId in openDrawIdList:
            gameglobal.rds.ui.activitySaleLuckyLottery.setLuckyLotteryPushMsgCallBack(RLLDId)
            gameglobal.rds.ui.activitySaleLuckyLottery.pushLuckylotteryMsg(RLLDId)
