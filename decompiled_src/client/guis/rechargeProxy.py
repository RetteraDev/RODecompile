#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/rechargeProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
from Scaleform import GfxValue
import gameglobal
from helpers import remoteInterface
from guis import uiConst
from guis import uiUtils
from callbackHelper import Functor

class RechargeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RechargeProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.onClose,
         'charge': self.onCharge,
         'gotoWeb': self.onGotoWeb,
         'submit': self.onSubmit,
         'checkCount': self.checkCount,
         'showMessageBox': self.showMessageBox,
         'gotoChargeWeb': self.gotoChargeWeb,
         'gotoCardIntroWeb': self.onGotoCardIntroWeb,
         'setApState': self.setApState}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_RECHARGE, self.onClose)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_RECHARGE:
            self.mediator = mediator
            ret = {}
            ret['myAccount'] = getattr(BigWorld.player(), 'roleURS', gameStrings.TEXT_RECHARGEPROXY_34)
            return uiUtils.dict2GfxDict(ret, True)

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RECHARGE, True, True)

    def onClose(self, *arg):
        self.hide()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_RECHARGE)

    def onCharge(self, *arg):
        cardNumber = arg[3][0].GetString()
        password = arg[3][1].GetString()
        p = BigWorld.player()
        p.base.dianKaCharge(cardNumber, password)

    def onGotoWeb(self, *arg):
        BigWorld.openUrl('http://ecard.163.com/ecard')

    def gotoChargeWeb(self, *arg):
        BigWorld.openUrl('http://pay.163.com/index.jsp')

    def onGotoCardIntroWeb(self, *arg):
        BigWorld.openUrl('http://pay.163.com/jsp/cardintro.jsp')

    def onSubmit(self, *arg):
        account = arg[3][0].GetString()
        password = arg[3][1].GetString()
        amount = int(arg[3][2].GetString())
        remoteInterface.getChargeUrl(account, password, amount, remoteInterface.onGetChargeUrl)

    def checkCount(self, *arg):
        count = arg[3][0].GetString()
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_RECHARGEPROXY_74 % count, Functor(self.updateCheckCount, count))

    def updateCheckCount(self, count):
        if self.mediator:
            self.mediator.Invoke('updateCheckCount', GfxValue(count))

    def showMessageBox(self, *arg):
        type = arg[3][0].GetString()
        if type == 'account':
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_RECHARGEPROXY_83, Functor(self.focusInput, type))
        elif type == 'wangyinpassword':
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_RECHARGEPROXY_85, Functor(self.focusInput, type))
        elif type == 'cardNumber':
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_RECHARGEPROXY_87, Functor(self.focusInput, type))
        elif type == 'cardpassword':
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_RECHARGEPROXY_89, Functor(self.focusInput, type))
        elif type == 'count':
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_RECHARGEPROXY_91, Functor(self.focusInput, type))

    def focusInput(self, type):
        if self.mediator:
            self.mediator.Invoke('focusInput', GfxValue(type))

    def setApState(self, *arg):
        uiUtils.setApState(True)

    def getRechargeState(self):
        if self.mediator:
            return True
