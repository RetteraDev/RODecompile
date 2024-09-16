#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/worldWarRobResultProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import uiConst
import events
import clientUtils
import formula
from uiProxy import UIProxy
from guis import uiUtils
from data import world_war_config_data as WWCD
CASH_ICON_OFFSET = 10

class WorldWarRobResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WorldWarRobResultProxy, self).__init__(uiAdapter)
        self.widget = None
        self.totalRes = 0
        self.bindCash = 0
        self.score = 0
        self.bonusId = 0
        self.lastRobState = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_WORLD_WAR_ROB_RESULT, self.clearWidget)

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        if not gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
            self.widget.confirm.addEventListener(events.MOUSE_CLICK, self.hidePanel)
        else:
            self.widget.confirm.addEventListener(events.MOUSE_CLICK, self.exitWWRob)
        p = BigWorld.player()
        camp = p.worldWar.getCurrCamp()
        resultTxtArray = WWCD.data.get('wwrResultText', {}).get(camp, ['', '', ''])
        if p.worldWar.robState == gametypes.WW_ROB_STATE_CLOSED:
            if self.lastRobState == gametypes.WW_ROB_STATE_OPEN:
                self.widget.resultText.text = resultTxtArray[0]
            elif self.lastRobState == gametypes.WW_ROB_STATE_OVERTIME:
                self.widget.resultText.text = resultTxtArray[1]
            else:
                self.widget.resultText.text = resultTxtArray[2]
        else:
            self.widget.resultText.text = gameStrings.TEXT_WORLDWARROBRESULTPROXY_50
        self.widget.totalRes.text = self.totalRes
        self.widget.personalCash.text = self.bindCash
        self.widget.cashIcon.x = self.widget.personalCash.x + self.widget.personalCash.textWidth + CASH_ICON_OFFSET
        self.widget.personalContribution.text = self.score
        if self.bonusId:
            itemId, cnt = clientUtils.genItemBonus(self.bonusId)[0]
            reward = uiUtils.getGfxItemById(itemId, cnt)
            self.widget.bonus.setItemSlotData(reward)
        else:
            self.widget.bonus.visible = False
            self.widget.bonusTxt.visible = False
        if gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
            if p.recentEnterWWType == gametypes.WORLD_WAR_TYPE_ROB:
                self.widget.groupType.gotoAndStop('qinglong')
            elif p.recentEnterWWType == gametypes.WORLD_WAR_TYPE_ROB_YOUNG:
                self.widget.groupType.gotoAndStop('baihu')
            else:
                self.widget.groupType.visible = False
        else:
            self.widget.groupType.visible = False

    def exitWWRob(self, *args):
        p = BigWorld.player()
        if formula.spaceInWorldWarRob(p.spaceNo):
            p.cell.exitWorldWar()
        else:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_RESULT)
        self.clearWidget()

    def hidePanel(self, *args):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_RESULT)
        self.clearWidget()

    def show(self, totalRes = 0, bindCash = 0, score = 0, bonusId = 0, lastRobState = 0):
        if not self.widget:
            self.totalRes = totalRes
            self.bindCash = bindCash
            self.score = score
            self.bonusId = bonusId
            self.lastRobState = lastRobState
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WORLD_WAR_ROB_RESULT)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WORLD_WAR_ROB_RESULT)
