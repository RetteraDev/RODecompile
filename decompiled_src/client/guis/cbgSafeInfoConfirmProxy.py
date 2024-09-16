#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cbgSafeInfoConfirmProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from gamestrings import gameStrings
from cdata import game_msg_def_data as GMDD
from data import cbg_config_data as CCD
SAFEINFO_STAGE_FIRST = 0
SAFEINFO_STAGE_SECOND = 1
SAFEINFO_STAGE_THIRD = 2

class CbgSafeInfoConfirmProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CbgSafeInfoConfirmProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CBG_SAFE_INFO_CONFIRM, self.hide)

    def reset(self):
        self.completeCallback = None
        self.stage = SAFEINFO_STAGE_FIRST

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CBG_SAFE_INFO_CONFIRM:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CBG_SAFE_INFO_CONFIRM)
        self.reset()

    def show(self, completeCallback):
        self.completeCallback = completeCallback
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CBG_SAFE_INFO_CONFIRM, True)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        self.gotoStageFirst()

    def _checkInputValid(self):
        if not self.widget:
            return False
        inputStr = self.widget.confirmInput.input.text
        template = self.widget.confirmInput.template.text
        if inputStr == template:
            return True
        return False

    def handleConfirmBtnClick(self, *args):
        if self.stage == SAFEINFO_STAGE_FIRST:
            self.gotoStageSecond()
        elif self.stage == SAFEINFO_STAGE_SECOND:
            if self._checkInputValid():
                self.gotoStageThird()
            else:
                BigWorld.player().showGameMsg(GMDD.data.COMMON_MSG, gameStrings.CBG_INPUT_WRONG_TIP)
                self.widget.confirmInput.input.text = ''
        elif self.stage == SAFEINFO_STAGE_THIRD:
            if self._checkInputValid():
                if self.completeCallback:
                    self.completeCallback()
                self.hide()
            else:
                BigWorld.player().showGameMsg(GMDD.data.COMMON_MSG, gameStrings.CBG_INPUT_WRONG_TIP)
                self.widget.confirmInput.input.text = ''

    def handleCancelBtnClick(self, *args):
        self.hide()

    def gotoStageFirst(self):
        self.stage = SAFEINFO_STAGE_FIRST
        self.widget.warning.visible = True
        self.widget.confirmInput.visible = False
        self.widget.confirmBtn.label = gameStrings.CBG_RLUE_AGREE
        self.widget.cancelBtn.label = gameStrings.CBG_RLUE_DISAGREE
        self.widget.warning.topText.htmlText = CCD.data.get('roleSellSafeInfoTextTop')
        self.widget.warning.bottomText.htmlText = CCD.data.get('roleSellSafeInfoTextBottom')

    def gotoStageSecond(self):
        self.stage = SAFEINFO_STAGE_SECOND
        self.widget.warning.visible = False
        self.widget.confirmInput.visible = True
        self.widget.confirmBtn.label = gameStrings.COMMON_CONFIRM
        self.widget.cancelBtn.label = gameStrings.COMMON_CANCEL
        self.widget.confirmInput.template.htmlText = CCD.data.get('roleSellSafeInfoInput1', 'None')
        self.widget.confirmInput.input.text = ''

    def gotoStageThird(self):
        self.stage = SAFEINFO_STAGE_THIRD
        self.widget.warning.visible = False
        self.widget.confirmInput.visible = True
        self.widget.confirmBtn.label = gameStrings.COMMON_CONFIRM
        self.widget.cancelBtn.label = gameStrings.COMMON_CANCEL
        self.widget.confirmInput.template.htmlText = CCD.data.get('roleSellSafeInfoInput2', 'None')
        self.widget.confirmInput.input.text = ''
