#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/qingGongJingSuTimeProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
from uiProxy import SlotDataProxy
from guis import uiConst

class QingGongJingSuTimeProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(QingGongJingSuTimeProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.modelMap = {'showRank': self.onShowRank,
         'refreshTime': self.onRefreshTime}
        self.mediator = None
        self.beginTime = 0
        self.handle = None
        self.potTime = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_QING_GONG_JING_SU_TIME, self.hide)

    def show(self):
        if not self.mediator:
            self.beginTime = int(BigWorld.player().getServerTime())
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_QING_GONG_JING_SU_TIME)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_QING_GONG_JING_SU_TIME:
            self.mediator = mediator

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        if self.mediator:
            self.mediator = None
            self.beginTime = 0
            self.potTime = 0
            if self.handle:
                BigWorld.cancelCallback(self.handle)
                self.handle = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_QING_GONG_JING_SU_TIME)

    def reset(self):
        super(self.__class__, self).reset()
        self.mediator = None
        self.beginTime = 0
        self.potTime = 0
        if self.handle:
            BigWorld.cancelCallback(self.handle)
            self.handle = None

    def onShowRank(self, *arg):
        gameglobal.rds.ui.qingGongJingSu.showResult()

    def setPotTime(self, time):
        self.potTime += time

    def onRefreshTime(self, *arg):
        self.setTime()

    def close(self):
        self.hide()

    def setTime(self):
        p = BigWorld.player()
        keepTime = p.getServerTime() - self.beginTime + self.potTime
        if keepTime < 0:
            keepTime = 0
        if self.mediator:
            self.mediator.Invoke('setTime', GfxValue(keepTime))
        self.handle = BigWorld.callback(0.5, self.setTime)
