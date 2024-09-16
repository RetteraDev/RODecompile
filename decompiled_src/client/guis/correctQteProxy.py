#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/correctQteProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
from uiProxy import UIProxy
from data import qte_data as QTED

class CorrectQteProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CorrectQteProxy, self).__init__(uiAdapter)
        self.modelMap = {'initData': self.onInitData,
         'qteSuccess': self.onQteSuccess,
         'qteFail': self.onQteFail}
        self.mediator = None
        self.qteId = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CORRECT_QTE:
            self.mediator = mediator

    def show(self, id):
        if self.mediator:
            self.hide(False)
        self.qteId = id
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CORRECT_QTE)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CORRECT_QTE)

    def reset(self):
        super(self.__class__, self).reset()
        if QTED.data[self.qteId].get('hideUI', 0):
            gameglobal.rds.ui.setQTEHideUI(False)
        gameglobal.rds.ui.inQTE = False
        self.qteId = None

    def onInitData(self, *arg):
        movie = arg[0]
        obj = movie.CreateObject()
        qteData = QTED.data[self.qteId]
        obj.SetMember('correctKey', GfxValue(qteData['correctKey'].upper()))
        obj.SetMember('interval', GfxValue(qteData['interval']))
        return obj

    def onQteSuccess(self, *arg):
        BigWorld.player().uploadQTEInfo(self.qteId, True)
        self.reset()

    def onQteFail(self, *arg):
        BigWorld.player().uploadQTEInfo(self.qteId, False)
        self.reset()
