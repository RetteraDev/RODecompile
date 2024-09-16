#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mibaoProxy.o
from gamestrings import gameStrings
from Scaleform import GfxValue
import gameglobal
from guis import uiConst
from uiProxy import UIProxy

class MibaoProxy(UIProxy):
    gameStrings.TEXT_MIBAOPROXY_10
    TYPE_JIANGJUNLING = 1
    TYPE_MIBAO_CARD = 2

    def __init__(self, uiAdapter):
        super(MibaoProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.onCloseWidget,
         'getMibaoType': self.onGetMibaoType,
         'getExtraData': self.onGetExtraData,
         'confirmInput': self.onConfirmInput,
         'cancelInput': self.onCancelInput}
        self.mibaoMediator = None
        self.mibaoWidgetId = uiConst.WIDGET_MIBAO_INVALIDATION
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.mibaoWidgetId:
            self.mibaoMediator = mediator

    def showJiangJunLing(self, login):
        if self.isShow:
            return
        self.mibaoType = self.TYPE_JIANGJUNLING
        self.login = login
        self.isShow = True
        gameglobal.rds.ui.loadWidget(self.mibaoWidgetId)

    def showMibaoCard(self, login, coordinate):
        if self.isShow:
            return
        self.mibaoType = self.TYPE_MIBAO_CARD
        self.login = login
        self.isShow = True
        self.coordinate = coordinate
        gameglobal.rds.ui.loadWidget(self.mibaoWidgetId)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(self.mibaoWidgetId)
        self.mibaoMediator = None
        self.isShow = False

    def reset(self):
        gameStrings.TEXT_MIBAOPROXY_60
        self.mibaoType = self.TYPE_JIANGJUNLING
        self.login = None
        self.coordinate = ''
        self.isShow = False

    def checkSecurityInvalidation(self, input):
        if self.mibaoType == self.TYPE_JIANGJUNLING:
            self.login.logonClient.ekey(input)
        elif self.mibaoType == self.TYPE_MIBAO_CARD:
            self.login.logonClient.mimaka(input)

    def onCloseWidget(self, *arg):
        self.onCancelInput()

    def onGetMibaoType(self, *arg):
        return GfxValue(self.mibaoType)

    def onGetExtraData(self, *arg):
        if self.mibaoType == self.TYPE_JIANGJUNLING:
            return
        if self.mibaoType == self.TYPE_MIBAO_CARD:
            return GfxValue(self.coordinate)

    def onConfirmInput(self, *arg):
        if arg[3][0] is None:
            return
        else:
            self.checkSecurityInvalidation(arg[3][0].GetString())
            self.clearWidget()
            return

    def onCancelInput(self, *arg):
        self.clearWidget()
        self.login.gotoLoginPage()
