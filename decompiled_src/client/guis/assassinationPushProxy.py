#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/assassinationPushProxy.o
import BigWorld
import math
import gameglobal
import uiConst
import utils
import events
import assassinationUtils as assUtils
import const
import ui
from sfx import screenEffect
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from gamestrings import gameStrings
from callbackHelper import Functor
import clientUtils
from cdata import assassination_config_data as ACD
from data import sys_config_data as SCD

class AssassinationPushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AssassinationPushProxy, self).__init__(uiAdapter)
        self.widget = None
        self.timeCountDownCallBack = None
        self.reset()

    def reset(self):
        self.tipsRollEffectEnable = False

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ASSASSINATION_PUSH:
            self.widget = widget
            self.reset()
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ASSASSINATION_PUSH)

    def show(self):
        if not gameglobal.rds.configData.get('enableAssassination', False):
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ASSASSINATION_PUSH)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.pushIcon.icon.addEventListener(events.BUTTON_CLICK, self.handleExpandBtnClick, False, 0, True)
        self.widget.pushIcon.expandBtn.addEventListener(events.BUTTON_CLICK, self.handleExpandBtnClick, False, 0, True)
        self.widget.pushIcon.tipsText.textMc.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleCloseBtnClick, False, 0, True)
        self.widget.pushIcon.expandBtn.visible = True
        self.widget.pushIcon.tipsText.visible = False
        self.tipsRollEffect(True)
        self.tipsRollEffectEnable = True

    def handleExpandBtnClick(self, *args):
        if self.tipsRollEffectEnable:
            self.tipsRollEffect(False)
            self.tipsRollEffectEnable = False
        else:
            self.tipsRollEffect(True)
            self.tipsRollEffectEnable = True

    def handleCloseBtnClick(self, *args):
        self.tipsRollEffect(False)
        self.tipsRollEffectEnable = False

    def tipsRollEffect(self, enable):
        if enable:
            self.widget.pushIcon.tipsText.gotoAndPlay('on')
            self.showTips(enable)
        else:
            self.widget.pushIcon.tipsText.gotoAndPlay('off')
            ASUtils.callbackAtFrame(self.widget.pushIcon.tipsText, 31, self.tipsRollEffectCallback, enable)

    def tipsRollEffectCallback(self, *args):
        asObject = ASObject(args[3][0])
        enable = asObject[0]
        self.showTips(bool(enable))

    def showTips(self, enable):
        self.widget.pushIcon.expandBtn.visible = not enable
        self.widget.pushIcon.tipsText.visible = enable

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        tOffTimeLimit = ACD.data.get('assassinationToffInterval', 14400)
        killTimeLimit = ACD.data.get('assassinationKillTimeLimit', 300)
        failTimeLimit = ACD.data.get('assassinationFailPushTimeLimit', 600)
        if hasattr(p, 'myAssOffBoardData') and p.myAssOffBoardData and 'state' in p.myAssOffBoardData:
            if p.myAssOffBoardData['state'] == assUtils.CURRENT_OFF_BOARD_FAIL:
                if utils.getNow() - p.myAssOffBoardData[assUtils.OFF_BOARD_TIME_END] <= failTimeLimit:
                    countDown = failTimeLimit - (utils.getNow() - p.myAssOffBoardData[assUtils.OFF_BOARD_TIME_END])
                    self.showFail(countDown)
                else:
                    self.hide()
            elif p.myAssOffBoardData['state'] == assUtils.CURRENT_OFF_BOARD_SUCCESS:
                self.hide()
            elif p.myAssOffBoardData['state'] == assUtils.CURRENT_OFF_BOARD_NOT_START:
                if utils.getNow() - p.myAssOffBoardData[assUtils.OFF_BOARD_TIME_OFF] <= tOffTimeLimit:
                    countDownStamp = tOffTimeLimit - (utils.getNow() - p.myAssOffBoardData[assUtils.OFF_BOARD_TIME_OFF])
                    self.showCountDownTime(True, countDownStamp, isShowFail=True)
                elif utils.getNow() - p.myAssOffBoardData[assUtils.OFF_BOARD_TIME_OFF] <= tOffTimeLimit + failTimeLimit:
                    countDown = tOffTimeLimit + failTimeLimit - (utils.getNow() - p.myAssOffBoardData[assUtils.OFF_BOARD_TIME_OFF])
                    self.showFail(countDown)
                else:
                    self.hide()
            elif p.myAssOffBoardData['state'] == assUtils.CURRENT_OFF_BOARD_KILLING:
                if utils.getNow() - p.myAssOffBoardData[assUtils.OFF_BOARD_TIME_OFF] <= tOffTimeLimit:
                    countDownStamp = tOffTimeLimit - (utils.getNow() - p.myAssOffBoardData[assUtils.OFF_BOARD_TIME_OFF])
                    self.showCountDownTime(True, countDownStamp=countDownStamp, isShowZero=True)
                else:
                    self.showCountDownTime(True, isShowZero=True)
            else:
                self.hide()
        else:
            self.hide()

    def showCountDownTime(self, enable, countDownStamp = 0, isShowFail = False, isShowZero = False):
        if not self.widget:
            return
        self.widget.pushIcon.countdown.visible = enable
        if enable:
            if countDownStamp > 0:
                self.widget.pushIcon.countdown.textField.text = self.getCountDownStrFromStamp(countDownStamp)
                self.refreshTipsText(False, countDownStamp)
                if self.timeCountDownCallBack:
                    BigWorld.cancelCallback(self.timeCountDownCallBack)
                self.timeCountDownCallBack = BigWorld.callback(1, Functor(self.showCountDownTime, enable, countDownStamp - 1, isShowFail, isShowZero))
            else:
                if isShowFail:
                    self.showFail(ACD.data.get('assassinationFailPushTimeLimit', 600))
                if isShowZero:
                    self.widget.pushIcon.countdown.textField.text = self.getCountDownStrFromStamp(0)

    def showFail(self, countDown):
        if self.timeCountDownCallBack:
            BigWorld.cancelCallback(self.timeCountDownCallBack)
        self.showCountDownTime(False)
        self.refreshTipsText(True)
        BigWorld.callback(countDown, self.hide)

    def refreshTipsText(self, isFail, countDownStamp = 0):
        if isFail:
            self.widget.pushIcon.tipsText.textMc.timeTipsMc.visible = False
            self.widget.pushIcon.tipsText.textMc.itemTipsMc.visible = False
            self.widget.pushIcon.tipsText.textMc.failTipsMc.visible = True
            self.widget.pushIcon.tipsText.textMc.failTipsMc.text = gameStrings.ASSASSINATION_PUSH_FAIL_TIPS
        else:
            hourStamp = ACD.data.get('assassinationToffInterval', 14400)
            hour = math.ceil(hourStamp / 3600)
            self.widget.pushIcon.tipsText.textMc.timeTipsMc.visible = True
            self.widget.pushIcon.tipsText.textMc.itemTipsMc.visible = True
            self.widget.pushIcon.tipsText.textMc.failTipsMc.visible = False
            self.widget.pushIcon.tipsText.textMc.timeTipsMc.htmlText = gameStrings.ASSASSINATION_PUSH_TIME_TIPS % hour
            self.widget.pushIcon.tipsText.textMc.itemTipsMc.text = gameStrings.ASSASSINATION_PUSH_ITEM_TIPS

    def getCountDownStrFromStamp(self, stamp):
        hours = stamp // 3600
        minute = math.ceil((stamp - hours * 60 * 60) / 60)
        return '%.2d:%.2d' % (hours, minute)
