#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/worldWarRobInfoProxy.o
from gamestrings import gameStrings
import time
import BigWorld
from uiProxy import UIProxy
import gameglobal
import gametypes
import uiConst
import events
import utils
from guis.asObject import TipManager
from guis import ui
from data import world_war_config_data as WWCD
from data import world_war_fort_data as WWFD
from data import world_war_relive_board_data as WWRBD
FORT_NUM = 8
GREEN_COLOR = '#7acc29'
RED_COLOR = '#cc2929'
YELLOW_COLOR = '#e59545'

class WorldWarRobInfoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WorldWarRobInfoProxy, self).__init__(uiAdapter)
        self.widget = None
        self.fortData = []
        self.clockId = None
        self.timeEnd = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_WORLD_WAR_ROB_INFO, self.clearWidget)

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.getFortData()
        self.initUI()

    def refreshTime(self):
        p = BigWorld.player()
        self.timeEnd = BigWorld.player().worldWar.tRobStateEnd - utils.getNow()
        if self.timeEnd < 0:
            self.timeEnd = 0
        color = YELLOW_COLOR
        timeTxt = time.strftime('%M:%S', time.localtime(self.timeEnd))
        if p.worldWar.robState == gametypes.WW_ROB_STATE_OVERTIME:
            if self.camp == gametypes.WORLD_WAR_CAMP_ATTACK:
                color = RED_COLOR
            else:
                color = GREEN_COLOR
            timeTxt = '-' + timeTxt
        self.widget.timeLeft.htmlText = "<font color = \'%s\'>%s</font>" % (color, timeTxt)
        self.clockId = BigWorld.callback(1, self.refreshTime)

    def getFortData(self):
        for fortId, val in WWFD.data.iteritems():
            if val.get('type', -1) == gametypes.WW_ROB_FORT_TYPE and val.get('robAreaMapId', ()):
                fortInfo = val
                fortInfo['fortId'] = fortId
                self.fortData.append(fortInfo)

    def initUI(self):
        p = BigWorld.player()
        self.camp = p.worldWar.getCurrCamp()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        BigWorld.callback(0, self.refreshPanel)

    def refreshPanel(self):
        if not self.widget:
            return
        p = BigWorld.player()
        robZaiju = p.worldWar.robZaiju
        wwData = WWCD.data
        self.setResource()
        self.setScore()
        self.widget.ruleArea.rule.htmlText = wwData.get('wwrRule', '').get(self.camp, '')
        self.widget.ruleArea.rule.wordWrap = True
        self.setLocation()
        self.setFort()
        self.setTime()
        self.setReliveBoard()

    def resetTime(self):
        self.timeEnd = BigWorld.player().worldWar.tRobStateEnd - utils.getNow()
        self.seconds = 0

    def setTime(self):
        self.timeEnd = BigWorld.player().worldWar.tRobStateEnd - utils.getNow()
        if self.clockId:
            BigWorld.cancelCallback(self.clockId)
        self.refreshTime()

    def setScore(self):
        p = BigWorld.player()
        self.widget.contributionNum.text = p.worldWar.robScore
        self.widget.cashNum.text = p.worldWar.getRobBindCash()

    def setReliveBoard(self):
        p = BigWorld.player()
        ww = p.worldWar
        idx = 0
        for reliveId, val in WWRBD.data.iteritems():
            if val.get('canOccupy', 0):
                camp = 0
                hostId = ww.reliveBoard.get(reliveId, 0)
                if hostId:
                    camp = ww.getCountry(hostId).currCamp
                relive = self.widget.getChildByName('relive%d' % idx)
                relive.gotoAndStop('type%d' % camp)
                relive.textField.text = val.get('shortName', '')
                relive.effect.visible = False
                idx += 1

    def setLocation(self):
        p = BigWorld.player()
        robZaiju = p.worldWar.robZaiju
        wwData = WWCD.data
        if self.camp == gametypes.WORLD_WAR_CAMP_ATTACK:
            if wwData.get('wwrAimTxt', ()):
                self.widget.aimInfo.destinationInfo.locationTxt.text = wwData.get('wwrAimTxt', ())[0]
            position = robZaiju.position
            destinationP = wwData.get('wwrDestination', (0, 0, 0))
            self.widget.aimInfo.destinationInfo.location.text = '(%d,%d,%d)' % (destinationP[0], destinationP[1], destinationP[2])
            self.widget.aimInfo.locationInfo.location.text = '(%d,%d,%d)' % (position[0], position[1], position[2])
            self.widget.aimInfo.locationInfo.locationTxt.text = gameStrings.TEXT_WORLDWARROBINFOPROXY_131
        else:
            if wwData.get('wwrAimTxt', ()):
                self.widget.aimInfo.destinationInfo.locationTxt.text = wwData.get('wwrAimTxt', ())[1]
            self.widget.aimInfo.destinationInfo.location.visible = False
            self.widget.aimInfo.locationInfo.visible = False

    def setResource(self):
        p = BigWorld.player()
        robZaiju = p.worldWar.robZaiju
        wwData = WWCD.data
        if self.camp == gametypes.WORLD_WAR_CAMP_ATTACK:
            self.widget.resource1.text = gameStrings.TEXT_WORLDWARROBINFOPROXY_143
            self.widget.resource2.text = gameStrings.TEXT_WORLDWARROBINFOPROXY_144
        else:
            self.widget.resource1.text = gameStrings.TEXT_WORLDWARROBINFOPROXY_146
            self.widget.resource2.text = gameStrings.TEXT_WORLDWARROBINFOPROXY_147
        self.widget.resourceNum1.text = robZaiju.mineRobRes
        self.widget.resourceNum2.text = robZaiju.enemyRobRes
        self.widget.resourceNum1.x = self.widget.resource1.x + self.widget.resource1.textWidth
        self.widget.resourceNum2.x = self.widget.resource2.x + self.widget.resource2.textWidth

    def setFort(self):
        p = BigWorld.player()
        robEachFortRes = p.worldWar.robZaiju.robEachFortRes
        hostId = utils.getHostId()
        for i in range(0, FORT_NUM):
            fortWidget = self.widget.getChildByName('aim%d' % i)
            fortId = self.fortData[i].get('fortId', 0)
            fort = p.worldWar.getFort(fortId)
            fortTips = WWCD.data.get('wwrFortStateTips', {}).get(self.camp, ('', '', ''))
            if robEachFortRes.has_key(fortId):
                fortWidget.icon.validateNow()
                fortWidget.icon.currentValue = robEachFortRes.get(fortId, 0)
                fortWidget.icon.maxValue = WWFD.data.get(fortId, {}).get('robBossRes', 0)
            if self.camp == gametypes.WORLD_WAR_CAMP_ATTACK:
                if hostId == fort.hostId:
                    fortWidget.icon.bar.visible = False
                    fortWidget.icon.bg.visible = True
                    if WWFD.data.get(fortId, {}).get('initRobCamp', 1) == gametypes.WORLD_WAR_CAMP_ATTACK:
                        TipManager.addTip(fortWidget, fortTips[2])
                    else:
                        TipManager.addTip(fortWidget, fortTips[1])
                else:
                    TipManager.addTip(fortWidget, fortTips[0])
                    fortWidget.icon.bar.gotoAndStop('red')
            elif hostId == fort.hostId:
                TipManager.addTip(fortWidget, fortTips[0])
                fortWidget.icon.bar.gotoAndStop('red')
            else:
                fortWidget.icon.bar.visible = False
                fortWidget.icon.bg.visible = True
                if WWFD.data.get(fortId, {}).get('initRobCamp', 1) == gametypes.WORLD_WAR_CAMP_ATTACK:
                    TipManager.addTip(fortWidget, fortTips[2])
                else:
                    TipManager.addTip(fortWidget, fortTips[1])
            fortWidget.fortName.text = self.fortData[i].get('shortName', '')
            if fort.inCombat:
                fortWidget.effect.visible = True
            else:
                fortWidget.effect.visible = False

    def show(self):
        p = BigWorld.player()
        ww = BigWorld.player().worldWar
        if not p.isWWRInRightState():
            self.clearWidget()
            return
        if not self.widget:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WORLD_WAR_ROB_INFO)
        else:
            self.refreshPanel()

    @ui.uiEvent(uiConst.WIDGET_WORLD_WAR_ROB_INFO, events.EVENT_PLAYER_SPACE_NO_CHANGED)
    def onExitWorldWarSpace(self):
        self.clearWidget()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.widget = None
        self.timeEnd = 0
        if self.clockId:
            BigWorld.cancelCallback(self.clockId)
            clockId = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WORLD_WAR_ROB_INFO)
