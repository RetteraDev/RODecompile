#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fubenAwardTimesProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import gametypes
from uiProxy import UIProxy
from data import bonus_history_check_data as BHCD
from cdata import bonus_history_reverse_data as BHRD
from cdata import game_msg_def_data as GMDD

class FubenAwardTimesProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FubenAwardTimesProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.mediator = None
        self.groupId = 0
        self.resData = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_FUBEN_AWARD_TIMES, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FUBEN_AWARD_TIMES:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_AWARD_TIMES)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def clearData(self):
        self.resData = {}

    def setInfo(self, data):
        if data[0] in self.resData and self.resData[data[0]] == data[1]:
            return
        self.resData[data[0]] = data[1]
        self.refreshInfo()

    def show(self, groupId):
        self.groupId = groupId
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_AWARD_TIMES)
        BigWorld.player().cell.queryBonusHistory(self.groupId)

    def refreshInfo(self):
        if self.mediator:
            info = {}
            bhrd = BHRD.data.get(self.groupId, [])
            if not bhrd:
                return
            bossList = []
            for bid in bhrd:
                bhcd = BHCD.data.get(bid, {})
                if not bhcd:
                    continue
                bossInfo = {}
                bossInfo['bossPhoto'] = 'fubenAwardTimes/%s.dds' % bhcd.get('icon', '')
                bossInfo['bossName'] = bhcd.get('name', '')
                period = bhcd.get('period', 0)
                if period == gametypes.BONUS_HISTORY_CD_TYPE_DAY:
                    bossInfo['periodIcon'] = 'day'
                else:
                    bossInfo['periodIcon'] = 'week'
                nowTimes = self.resData.get(self.groupId, {}).get(bid, 0)
                limitTimes = bhcd.get('times', 0)
                if nowTimes < limitTimes:
                    bossInfo['times'] = '%d/%d' % (nowTimes, limitTimes)
                    if period == gametypes.BONUS_HISTORY_CD_TYPE_DAY:
                        bossInfo['timesTips'] = uiUtils.getTextFromGMD(GMDD.data.FUBEN_AWARD_TIMES_DAY_USEABLE, '')
                    else:
                        bossInfo['timesTips'] = uiUtils.getTextFromGMD(GMDD.data.FUBEN_AWARD_TIMES_WEEK_USEABLE, '')
                    bossInfo['redVisible'] = False
                else:
                    bossInfo['times'] = "<font color = \'#F43804\'>%d/%d</font>" % (nowTimes, limitTimes)
                    if period == gametypes.BONUS_HISTORY_CD_TYPE_DAY:
                        bossInfo['timesTips'] = uiUtils.getTextFromGMD(GMDD.data.FUBEN_AWARD_TIMES_DAY_DISABLE, '')
                    else:
                        bossInfo['timesTips'] = uiUtils.getTextFromGMD(GMDD.data.FUBEN_AWARD_TIMES_WEEK_DISABLE, '')
                    bossInfo['redVisible'] = True
                bossInfo['order'] = bhcd.get('order', 0)
                rewardIcons = bhcd.get('rewardIcons', ())
                itemList = []
                if rewardIcons:
                    for itemId in rewardIcons:
                        itemList.append(uiUtils.getGfxItemById(itemId))

                bossInfo['itemList'] = itemList
                bossList.append(bossInfo)

            bossList.sort(key=lambda x: x['order'])
            info['bossList'] = bossList
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
