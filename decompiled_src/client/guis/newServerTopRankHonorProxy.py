#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newServerTopRankHonorProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import utils
import gametypes
import events
from uiProxy import UIProxy
from gamestrings import gameStrings
from callbackHelper import Functor
from data import mail_template_data as MTD
from data import ns_honor_rank_act_data as NHRAD
from data import bonus_data as BD
PRIVIEGE_DAY_TO_SECOND = 86400
HONOR_IMAGE_NAME = ['chuanshi',
 'shehui',
 'jingshi',
 'gaishi',
 'jingluo',
 'nenggong',
 'gongcheng',
 'degao']

class NewServerTopRankHonorProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NewServerTopRankHonorProxy, self).__init__(uiAdapter)
        self.widget = None

    def reset(self):
        pass

    def initPanel(self, widget):
        self.widget = widget
        self.timer = None
        if not getattr(self, 'rankData', None):
            self.rankData = {}
        self.updateTimer()
        self.initUI()
        p = BigWorld.player()
        p.base.getNSHonorRank()

    def unRegisterPanel(self):
        self.widget = None
        self.cleanTimer()

    def setDataAndRefresh(self, rankData):
        self.rankData = rankData
        self.initUI()

    def initUI(self):
        self.initAllTop()

    def initAllTop(self):
        configData = NHRAD.data.values()[0]
        newServerHonorTopTitle = configData.get('newServerHonorTopTitle', {})
        newServerHonorTopTypes = configData.get('newServerHonorTopTypes', [])
        for i in range(0, 8):
            honorItem = getattr(self.widget.yushiNode, 'node%s' % i)
            if honorItem:
                if not newServerHonorTopTypes:
                    honorItem.detailBtn.roleName.text = gameStrings.NEW_SERVER_NOT_IN_RANK_2
                else:
                    topType = newServerHonorTopTypes[i]
                    rankInfo = self.rankData.get(topType, ())
                    if rankInfo:
                        honorItem.detailBtn.roleName.text = rankInfo[1]
                    else:
                        honorItem.detailBtn.roleName.text = gameStrings.NEW_SERVER_NOT_IN_RANK_2
                if not newServerHonorTopTitle:
                    honorItem.detailBtn.title.text = gameStrings.NEW_SERVER_NOT_IN_RANK_2
                else:
                    honorItem.detailBtn.title.text = newServerHonorTopTitle[i]
                bonusId = MTD.data.get(configData.get('newServerHonorRankMails')[i], {}).get('bonusId', 0)
                honorItem.slot.dragable = False
                fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', ())
                fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
                honorItem.slot.setItemSlotData(uiUtils.getGfxItemById(fixedBonus[0][1]))
                honorItem.detailBtn.addEventListener(events.BUTTON_CLICK, Functor(self.onGoToRankPanel, i), False, 0, True)
                honorItem.detailBtn.imageBtn.gotoAndPlay(HONOR_IMAGE_NAME[i])

    def onGoToRankPanel(self, *args):
        indexToRankIndexList = [0,
         1,
         2,
         3,
         5,
         6,
         4,
         7]
        index = args[0]
        ranking = gameglobal.rds.ui.ranking
        if ranking.mediator:
            ranking.setTab(indexToRankIndexList[index])
        else:
            ranking.show(indexToRankIndexList[index])

    def updateTimer(self):
        configData = NHRAD.data.values()[0]
        enableTime = configData.get('newServerHonorRankEanbleTime', None)
        if not enableTime:
            self.cleanTimer()
            return
        else:
            periodType, nWeeksOffset, nLastWeeks = enableTime
            tStart, tEnd = utils.calcTimeDuration(periodType, utils.getServerOpenTime(), nWeeksOffset, nLastWeeks)
            if tStart <= utils.getNow() <= tEnd:
                leftTime = tEnd - utils.getNow()
            else:
                leftTime = 0
            if leftTime > PRIVIEGE_DAY_TO_SECOND:
                timeText = utils.formatTimeStr(leftTime, formatStr=gameStrings.TEXT_NEWSERVERTOPRANKCOMBATSCOREANDLVPROXY_262)
            elif leftTime <= PRIVIEGE_DAY_TO_SECOND and leftTime >= 3600:
                timeText = utils.formatTimeStr(leftTime, formatStr=gameStrings.TEXT_NEWSERVERTOPRANKCOMBATSCOREANDLVPROXY_265)
            else:
                timeText = utils.formatTimeStr(leftTime, formatStr=gameStrings.TEXT_NEWSERVERTOPRANKCOMBATSCOREANDLVPROXY_267)
            if self.widget:
                if leftTime == 0:
                    self.widget.yushiNode.timeText.text = gameStrings.NEW_SERVER_TOP_RANK_END
                else:
                    self.widget.yushiNode.timeText.text = gameStrings.LEFT_TIME % timeText
            if leftTime > 0:
                self.timer = BigWorld.callback(1, self.updateTimer)
            else:
                self.cleanTimer()
            return

    def cleanTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None
