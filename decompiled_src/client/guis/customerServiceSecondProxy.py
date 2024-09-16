#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/customerServiceSecondProxy.o
import BigWorld
import gameglobal
from ui import gbk2unicode
from Scaleform import GfxValue
from guis import uiConst
from guis.uiProxy import UIProxy

class CustomerServiceSecondProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CustomerServiceSecondProxy, self).__init__(uiAdapter)
        self.modelMap = {'refreshContent': self.onRefreshContent}
        self.contentData = []
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_CUSTOMER_SERVICE_SECOND, self.clearWidget)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CUSTOMER_SERVICE_SECOND:
            self.mediator = mediator

    def show(self, contentData):
        self.contentData = contentData
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CUSTOMER_SERVICE_SECOND)

    def closeWidget(self, *args):
        self.clearWidget()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CUSTOMER_SERVICE_SECOND)

    def onRefreshContent(self, *args):
        txt = self.getContentDataString()
        if txt:
            self.mediator.Invoke('setContent', GfxValue(gbk2unicode(txt)))

    def getContentDataString(self):
        return self.contentData['content']

    def queryToShow(self, key):
        p = BigWorld.player()
        if p:
            if p.__class__.__name__ == 'PlayerAvatar':
                p.base.getCustomerServiceCategory(key)
