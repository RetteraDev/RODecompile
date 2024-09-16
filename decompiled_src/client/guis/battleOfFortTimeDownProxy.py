#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/battleOfFortTimeDownProxy.o
import BigWorld
import uiConst
import gameglobal
import utils
import const
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis import events
from data import duel_config_data as DCD
from data import battle_field_mode_data as BFMD

class BattleOfFortTimeDownProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BattleOfFortTimeDownProxy, self).__init__(uiAdapter)
        self.widget = None
        self.battleId = 0
        self.actId = 0
        self.nextTimestamp = 0
        self.callback = None
        self.sureSignUp = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_BATTLE_OF_FORT_TIME_DOWN, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BATTLE_OF_FORT_TIME_DOWN:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BATTLE_OF_FORT_TIME_DOWN)
        p = BigWorld.player()
        p.unlockKey(gameglobal.KEY_POS_UI)

    def reset(self):
        self.battleId = 0
        self.actId = 0
        self.nextTimestamp = 0
        self.callback = None

    @property
    def battleData(self):
        return BFMD.data.get(self.battleId, {})

    def show(self, battleId, actId, nextTimestamp):
        p = BigWorld.player()
        if p._isSoul():
            return
        self.battleId = battleId
        self.actId = actId
        self.nextTimestamp = nextTimestamp
        if not self.battleId:
            return
        battleMode = self.battleData.get('mode', 0)
        if battleMode == const.BATTLE_FIELD_MODE_NEW_FLAG:
            if not gameglobal.rds.configData.get('enableNewFlagBF', False):
                return
        elif battleMode == const.BATTLE_FIELD_MODE_TIMING_PUBG:
            if not p.isCanJoinTimingPUBG():
                return
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_BATTLE_OF_FORT_TIME_DOWN, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.typeMc.okBtn.addEventListener(events.BUTTON_CLICK, self.handleOkBtnClick, False, 0, True)
        self.widget.typeMc.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick, False, 0, True)

    def handleOkBtnClick(self, *args):
        self.confirmEnterRequest(True)

    def handleCancelBtnClick(self, *args):
        self.confirmEnterRequest(False)

    def confirmEnterRequest(self, isOK):
        p = BigWorld.player()
        battleMode = self.battleData.get('mode', 0)
        if battleMode == const.BATTLE_FIELD_MODE_NEW_FLAG:
            p.cell.confirmEnterNewFlagBattleField(self.battleId, self.actId, isOK)
        elif battleMode == const.BATTLE_FIELD_MODE_TIMING_PUBG:
            p.cell.confirmEnterTimingPUBGBattleField(self.battleId, self.actId, isOK)

    def refreshInfo(self):
        if not self.widget:
            return
        self.updateDescAndBtn()
        self.updateTimeDown()

    def updateDescAndBtn(self):
        if self.sureSignUp:
            self.widget.typeMc.desc.htmlText = gameStrings.BATTLE_OF_FORT_WAIT_FOR_PLAYER
        else:
            self.widget.typeMc.desc.htmlText = self.battleData.get('battleOfFortTimeDownDesc', '')
        self.widget.typeMc.okBtn.visible = not self.sureSignUp
        self.widget.typeMc.cancelBtn.visible = not self.sureSignUp

    def updateTimeDown(self):
        if not self.widget:
            self.stopCallback()
            return
        leftTime = self.nextTimestamp - utils.getNow()
        if leftTime < 0:
            self.sureSignUp = False
            self.stopCallback()
            self.removePushMsg()
            self.hideProxy()
            return
        self.widget.typeMc.loading.maxValue = self.battleData.get('timingBattleConfirmEnterTime', 60)
        self.widget.typeMc.loading.currentValue = leftTime
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        self.callback = BigWorld.callback(1, self.updateTimeDown)

    def stopCallback(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
            self.callback = None

    def removePushMsg(self):
        pushId = BFMD.data.get(self.battleId, {}).get('battleStartSurePushId', 11545)
        if pushId in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(pushId)

    def setSureSignUpDesc(self):
        if not self.widget:
            return
        p = BigWorld.player()
        p.ap.stopMove()
        p.ap.forceAllKeysUp()
        p.lockKey(gameglobal.KEY_POS_UI, False)
        self.sureSignUp = True
        self.updateDescAndBtn()

    def hideProxy(self):
        self.hide()
        gameglobal.rds.ui.battleOfFortSignUp.hide()

    def cancelSignUp(self):
        self.removePushMsg()
        self.hideProxy()
