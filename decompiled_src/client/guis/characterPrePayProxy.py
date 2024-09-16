#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/characterPrePayProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
from uiProxy import UIProxy
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class CharacterPrePayProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CharacterPrePayProxy, self).__init__(uiAdapter)
        self.modelMap = {'refresh': self.onRefresh,
         'prePay': self.onPrePay,
         'gotoPay': self.onGotoPay}
        self.mediator = None
        self.timer = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHARACTER_PREPAY, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CHARACTER_PREPAY:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHARACTER_PREPAY)

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHARACTER_PREPAY)

    def reset(self):
        self.stopTimer()

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def refreshInfo(self):
        if self.mediator:
            info = {}
            info['prePayHint'] = uiUtils.getTextFromGMD(GMDD.data.CHARACTER_PREPAY_HINT, '')
            accountPrePayCoinAmount = SCD.data.get('accountPrePayCoinAmount', 1)
            info['pointHint'] = gameStrings.TEXT_CHARACTERPREPAYPROXY_52 % accountPrePayCoinAmount
            commonPoints = getattr(BigWorld.player(), 'commonPoints', 0)
            if commonPoints < accountPrePayCoinAmount:
                info['curPoint'] = gameStrings.TEXT_CHARACTERPREPAYPROXY_56 % commonPoints
                info['pointSatisfy'] = False
            else:
                info['curPoint'] = gameStrings.TEXT_CHARACTERPREPAYPROXY_59 % commonPoints
                info['pointSatisfy'] = True
            info['refreshBtnTips'] = uiUtils.getTextFromGMD(GMDD.data.CHARACTER_PREPAY_REFRESH_BTN_TIPS, gameStrings.TEXT_CHARACTERPREPAYPROXY_62)
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onRefresh(self, *arg):
        BigWorld.player().base.queryUrsPointData()
        if self.timer:
            self.refreshInfo()
        else:
            self.timer = BigWorld.callback(3, self.refreshInfo)

    def onPrePay(self, *arg):
        BigWorld.player().base.prePayCharge()
        self.hide()

    def onGotoPay(self, *arg):
        BigWorld.openUrl('http://ecard.163.com/')
