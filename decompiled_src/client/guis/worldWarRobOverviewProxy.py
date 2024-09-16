#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/worldWarRobOverviewProxy.o
import time
import BigWorld
import gameglobal
import utils
import gametypes
import uiConst
import events
import formula
import const
from guis.asObject import TipManager
from callbackHelper import Functor
from uiProxy import UIProxy
from data import world_war_config_data as WWCD
from data import ww_rob_zaiju_level_data as WRZLD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
ATTACK_WIDGET = 'WorldWarRobOverview_Attacker'
DEFEND_WIDGET = 'WorldWarRobOverview_Defender'
GREEN_COLOR = '#7acc29'
RED_COLOR = '#cc2929'
YELLOW_COLOR = '#e59545'

class WorldWarRobOverviewProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WorldWarRobOverviewProxy, self).__init__(uiAdapter)
        self.widget = None
        self.infoWidget = None
        self.timeEnd = 0
        self.clockId = None
        self.isWWRStartMsgPushed = False
        self.isWWRApplyMsgPushed = False
        self.force = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_WORLD_WAR_ROB_OVERVIEW, self.clearWidget)
        self.addEvent(events.EVENT_PLAYER_SPACE_NO_CHANGED, self.onSpaceNoChanged, 0, True)

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        p = BigWorld.player()
        if not p.isWWRInRightState():
            if not gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
                if not self.force:
                    self.clearWidget()
                    return
            else:
                self.clearWidget()
                return
        self.force = False
        self.initUI()

    def initUI(self):
        p = BigWorld.player()
        self.camp = p.worldWar.getCurrCamp()
        if self.camp == gametypes.WORLD_WAR_CAMP_ATTACK:
            self.infoWidget = self.widget.getInstByClsName(ATTACK_WIDGET)
            self.widget.addChild(self.infoWidget)
            self.infoWidget.transmit.addEventListener(events.MOUSE_CLICK, self.handleTransmit)
            tips = WWCD.data.get('wwrTeleportTip', '')
            TipManager.addTip(self.infoWidget.transmit, tips)
        elif self.camp == gametypes.WORLD_WAR_CAMP_DEFEND:
            self.infoWidget = self.widget.getInstByClsName(DEFEND_WIDGET)
            self.widget.addChild(self.infoWidget)
            self.infoWidget.hint.visible = False
        else:
            self.clearWidget()
        self.refreshPanel()

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
        self.infoWidget.timeLeft.htmlText = "<font color = \'%s\'>%s</font>" % (color, timeTxt)
        self.clockId = BigWorld.callback(1, self.refreshTime)

    def resetTime(self):
        self.timeEnd = BigWorld.player().worldWar.tRobStateEnd - utils.getNow()

    def setTime(self):
        self.resetTime()
        if self.clockId:
            BigWorld.cancelCallback(self.clockId)
        self.refreshTime()
        p = BigWorld.player()
        timeTips = WWCD.data.get('wwrTimeTips', ('', '', '', ''))
        if p.worldWar.robState == gametypes.WW_ROB_STATE_READY:
            TipManager.addTip(self.infoWidget.timeLeft, timeTips[0])
        elif p.worldWar.robState == gametypes.WW_ROB_STATE_OPEN:
            TipManager.addTip(self.infoWidget.timeLeft, timeTips[1])
        elif p.worldWar.robState == gametypes.WW_ROB_STATE_OVERTIME:
            TipManager.addTip(self.infoWidget.timeLeft, timeTips[2])
        elif p.worldWar.robState == gametypes.WW_ROB_STATE_ZAIJU_BROKEN:
            TipManager.addTip(self.infoWidget.timeLeft, timeTips[3])

    def refreshPanel(self):
        if not self.widget:
            return
        self.setLv()
        self.setHp()
        self.setRes()
        self.setScore()
        self.setTime()
        self.infoWidget.info.addEventListener(events.MOUSE_CLICK, self.handleInfo)
        self.infoWidget.rank.addEventListener(events.MOUSE_CLICK, self.handleRank)

    def setScore(self):
        p = BigWorld.player()
        self.infoWidget.cash.text = p.worldWar.getRobBindCash()
        tips = WWCD.data.get('wwrCashTip', '')
        TipManager.addTip(self.infoWidget.cash, tips)
        TipManager.addTip(self.infoWidget.cashIcon, tips)

    def setRes(self):
        p = BigWorld.player()
        robZaiju = p.worldWar.robZaiju
        wwData = WWCD.data
        if p.worldWar.robState == gametypes.WW_ROB_STATE_OVERTIME:
            self.infoWidget.resProgress.bar.gotoAndStop('jiashi')
        else:
            self.infoWidget.resProgress.bar.gotoAndStop('normal')
        self.infoWidget.resProgress.currentValue = robZaiju.mineRobRes
        self.infoWidget.resProgress.maxValue = wwData.get('robMaxRes', 0)
        tips = WWCD.data.get('wwrResTip', {}).get(self.camp, '')
        TipManager.addTip(self.infoWidget.resProgress, tips)
        self.infoWidget.resProgress.validateNow()

    def setHp(self):
        p = BigWorld.player()
        robZaiju = p.worldWar.robZaiju
        if self.camp == gametypes.WORLD_WAR_CAMP_ATTACK:
            tips = WWCD.data.get('wwrHpTip', '')
            TipManager.addTip(self.infoWidget.hpIcon, tips)
            TipManager.addTip(self.infoWidget.hpProgress, tips)
            self.infoWidget.hpProgress.currentValue = robZaiju.hp
            self.infoWidget.hpProgress.maxValue = robZaiju.mhp
            self.infoWidget.hpProgress.validateNow()

    def setLv(self):
        p = BigWorld.player()
        robZaiju = p.worldWar.robZaiju
        if self.camp == gametypes.WORLD_WAR_CAMP_ATTACK:
            tips = WWCD.data.get('wwrLvTip', '')
            TipManager.addTip(self.infoWidget.lv, tips)
            TipManager.addTip(self.infoWidget.lvProgress, tips)
            self.infoWidget.lv.text = 'lv.%d' % robZaiju.level
            levelData = WRZLD.data
            if levelData.get(robZaiju.level).get('playerDieNum', 0):
                if robZaiju.level == 1:
                    self.infoWidget.lvProgress.currentValue = robZaiju.playerDieNum
                    self.infoWidget.lvProgress.maxValue = levelData.get(robZaiju.level).get('playerDieNum', 0)
                else:
                    preLevel = robZaiju.level - 1
                    self.infoWidget.lvProgress.currentValue = robZaiju.playerDieNum - levelData.get(preLevel).get('playerDieNum', 0)
                    self.infoWidget.lvProgress.maxValue = levelData.get(robZaiju.level).get('playerDieNum', 0) - levelData.get(preLevel).get('playerDieNum', 0)
            else:
                self.infoWidget.lvProgress.currentValue = 1
                self.infoWidget.lvProgress.maxValue = 1
            self.infoWidget.lvProgress.validateNow()

    def pushLeaderMessage(self):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_START)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_START, {'click': self.onClickWWRStartMsg})

    def pushMessage(self, wwType):
        p = BigWorld.player()
        robState = p.worldWar.robStateDict[wwType]
        if gameglobal.rds.configData.get('enableWorldWarYoungGroup', False) and p.lv >= const.WORLD_WAR_ARMY_MINLV:
            if robState in gametypes.WW_ROB_STATE_APPLY_STATES:
                if p.isHaveRobStartPrivilege():
                    return
                if p.lv > const.WORLD_WAR_ARMY_MINLV:
                    if wwType == gametypes.WORLD_WAR_TYPE_ROB_YOUNG:
                        return
                if not self.isWWRApplyMsgPushed:
                    self.isWWRApplyMsgPushed = True
                    gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_ROB_APPLY)
                    gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_ROB_APPLY, {'click': Functor(self.onClickShowWorldWarPanel, uiConst.MESSAGE_TYPE_ROB_APPLY)})
                return
        if robState not in gametypes.WW_ROB_STATE_NOT_OPEN and p.lv >= const.WORLD_WAR_ARMY_MINLV:
            if not self.isWWRStartMsgPushed:
                self.isWWRStartMsgPushed = True
                clickFunc = None
                if gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
                    clickFunc = self.onClickShowWorldWarPanel
                    gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_START_ATTACK, {'click': Functor(clickFunc, uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_START_ATTACK)})
                    gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_START_DEFEND, {'click': Functor(clickFunc, uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_START_DEFEND)})
                else:
                    clickFunc = self.onClickWWRTeleportMsg
                    gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_START_ATTACK, {'click': clickFunc})
                    gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_START_DEFEND, {'click': clickFunc})
                if p.worldWar.getCurrCamp() == gametypes.WORLD_WAR_CAMP_ATTACK:
                    attachMsgId = uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_START_ATTACK
                    gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_START_ATTACK)
                else:
                    gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_START_DEFEND)
        if robState == gametypes.WW_ROB_STATE_OVERTIME:
            if p.id == p.worldWar.robZaijuEntID:
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_OVERTIME)
                gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_OVERTIME, {'click': self.onClickWWROverTimeMsg})
        if robState == gametypes.WW_ROB_STATE_ZAIJU_BROKEN:
            if p.id == p.worldWar.robZaijuEntID:
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_BROKEN)
                gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_BROKEN, {'click': self.onClickWWRBrokenTimeMsg})

    def pushResultPanelMsg(self, totalRes, bindCash, score, bonusIds, lastRobState):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_RESULT)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_RESULT, {'click': Functor(self.onClickWWRResultPanelMsg, totalRes, bindCash, score, bonusIds, lastRobState)})

    def onClickWWRResultPanelMsg(self, totalRes, bindCash, score, bonusIds, lastRobState):
        gameglobal.rds.ui.worldWarRobResult.show(totalRes, bindCash, score, bonusIds, lastRobState)

    def onClickWWRBrokenTimeMsg(self):
        msg = GMD.data.get(GMDD.data.WORLD_WAR_ROB_BROKEN, {}).get('text', '')
        gameglobal.rds.ui.messageBox.showMsgBox(msg)
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_BROKEN)

    def onClickWWROverTimeMsg(self):
        msg = GMD.data.get(GMDD.data.WORLD_WAR_ROB_OVERTIME, {}).get('text', '')
        gameglobal.rds.ui.messageBox.showMsgBox(msg)
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_OVERTIME)

    def onClickShowWorldWarPanel(self, msg):
        gameglobal.rds.ui.worldWar.show()
        gameglobal.rds.ui.pushMessage.removePushMsg(msg)

    def onClickWWRStartMsg(self):
        p = BigWorld.player()
        msgTele = GMD.data.get(GMDD.data.WORLD_WAR_ROB_START, {}).get('text', '')
        msgOpen = GMD.data.get(GMDD.data.WORLD_WAR_ROB_OPEN_CONFIRM, {}).get('text', '')
        wwType = 0
        if p.checkRobStartPrivilege(gametypes.WORLD_WAR_TYPE_ROB):
            wwType = gametypes.WORLD_WAR_TYPE_ROB
        elif p.checkRobStartPrivilege(gametypes.WORLD_WAR_TYPE_ROB_YOUNG):
            wwType = gametypes.WORLD_WAR_TYPE_ROB_YOUNG
        if gameglobal.rds.configData.get('enableWorldWarYoungGroup'):
            groupType = gametypes.WORLD_WAR_TYPE_GROUP_TXT[wwType]
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msgOpen % groupType, yesCallback=Functor(p.onClickOpenWorldWarRob, wwType))
        else:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msgTele, yesCallback=self.onClickLeaderWWRTeleport)

    def onClickLeaderWWRTeleport(self):
        self.onClickWWRTeleport()

    def onClickWWRTeleportMsg(self):
        p = BigWorld.player()
        if p.worldWar.getCurrCamp() == gametypes.WORLD_WAR_CAMP_ATTACK:
            msg = GMD.data.get(GMDD.data.WORLD_WAR_ROB_START_ATTACK, {}).get('text', '')
        else:
            msg = GMD.data.get(GMDD.data.WORLD_WAR_ROB_START_DEFEND, {}).get('text', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.onClickWWRTeleport, noCallback=self.onClickCancelWWRTeleport)

    def onClickWWRTeleport(self):
        p = BigWorld.player()
        wwtype = 0
        if not gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
            p.cell.enterWorldWarRob()
            return
        if p.lv > const.WORLD_WAR_ARMY_MINLV:
            wwtype = gametypes.WORLD_WAR_TYPE_ROB
        else:
            wwtype = gametypes.WORLD_WAR_TYPE_ROB_YOUNG
        p.cell.enterWorldWarEvent(wwtype)

    def onClickCancelWWRTeleport(self):
        self.removeWWRStartMsg()

    def removeWWRStartMsg(self):
        p = BigWorld.player()
        if p.worldWar.getCurrCamp() == gametypes.WORLD_WAR_CAMP_ATTACK:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_START_ATTACK)
        else:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_START_DEFEND)

    def handleInfo(self, *args):
        gameglobal.rds.ui.worldWarRobInfo.show()

    def handleRank(self, *args):
        gameglobal.rds.ui.worldWarRobRank.show()

    def handleTransmit(self, *args):
        BigWorld.player().cell.teleportToWWRobZaiju()

    def refreshHint(self, inCombat):
        if not self.defender:
            return
        self.defender.hint.visible = inCombat

    def show(self, force = False):
        p = BigWorld.player()
        ww = BigWorld.player().worldWar
        self.force = force
        if not p.isWWRInRightState():
            if not gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
                if not force:
                    self.clearWidget()
                    return
            else:
                self.clearWidget()
                return
        if not self.widget:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WORLD_WAR_ROB_OVERVIEW)
        else:
            self.refreshPanel()

    def onSpaceNoChanged(self, e):
        p = BigWorld.player()
        ww = BigWorld.player().worldWar
        if ww.robState in gametypes.WW_ROB_STATE_NOT_OPEN or not formula.spaceInWorldWar(p.spaceNo):
            self.clearWidget()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.widget = None
        self.infoWidget = None
        self.camp = None
        if self.clockId:
            BigWorld.cancelCallback(self.clockId)
            clockId = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WORLD_WAR_ROB_OVERVIEW)

    def exitWorldWarRob(self):
        msg = GMD.data.get(GMDD.data.WORLD_WAR_ROB_EXIT_CONFIRM, {}).get('text', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.confirmExitWorldWarRob)

    def confirmExitWorldWarRob(self):
        BigWorld.player().cell.exitWorldWar()
