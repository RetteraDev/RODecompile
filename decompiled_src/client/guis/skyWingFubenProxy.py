#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/skyWingFubenProxy.o
import BigWorld
import uiConst
import utils
import events
import gamelog
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis import baiDiShiLianProxy
from guis.asObject import ASUtils

class SkyWingFubenProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SkyWingFubenProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SKY_WING_FUBEN:
            self.widget = widget
            self.initUI()
            self.updateTimer()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SKY_WING_FUBEN)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SKY_WING_FUBEN)

    def updateTimer(self):
        if not self.widget:
            return
        self.refreshInfo()
        BigWorld.callback(1, self.updateTimer)

    def initUI(self):
        self.widget.challengeBtn.addEventListener(events.BUTTON_CLICK, self.handleChannlengeBtnClick, False, 0, True)
        self.widget.ransackBtn.addEventListener(events.BUTTON_CLICK, self.handleRansackBtnClick, False, 0, True)
        ASUtils.setHitTestDisable(self.widget.txtTitle, True)

    def refreshInfo(self):
        if not self.widget:
            return
        if utils.getNow() - self.uiAdapter.baiDiShiLian.lastChallengeTime < baiDiShiLianProxy.CHALLENGE_BTN_CD:
            self.widget.challengeBtn.enabled = False
            self.widget.challengeBtn.label = gameStrings.BAIDI_SHILIAN_CHALLENGE_IN_CD % (self.uiAdapter.baiDiShiLian.lastChallengeTime + baiDiShiLianProxy.CHALLENGE_BTN_CD - utils.getNow())
        else:
            self.widget.challengeBtn.enabled = True
            self.widget.challengeBtn.label = gameStrings.BAIDI_SHILIAN_CHALLENGE
        if utils.getNow() - self.uiAdapter.baiDiShiLian.lastRansackTime < baiDiShiLianProxy.RANSACK_BTN_CD:
            self.widget.ransackBtn.enabled = False
            self.widget.ransackBtn.label = gameStrings.BAIDI_SHILIAN_RANSACK_IN_CD % (self.uiAdapter.baiDiShiLian.lastRansackTime + baiDiShiLianProxy.RANSACK_BTN_CD - utils.getNow())
        else:
            self.widget.ransackBtn.enabled = True
            self.widget.ransackBtn.label = gameStrings.BAIDI_SHILIAN_RANSACK

    def handleChannlengeBtnClick(self, *args):
        gamelog.info('jbx:handleChannlengeBtnClick')
        if utils.getNow() - self.uiAdapter.baiDiShiLian.lastChallengeTime < baiDiShiLianProxy.CHALLENGE_BTN_CD:
            return
        p = BigWorld.player()
        p.cell.applySkyWingChallenge()

    def handleRansackBtnClick(self, *args):
        gamelog.info('jbx:handleRansackBtnClick')
        if utils.getNow() - self.uiAdapter.baiDiShiLian.lastRansackTime < baiDiShiLianProxy.RANSACK_BTN_CD:
            return
        self.uiAdapter.ransack.show()
