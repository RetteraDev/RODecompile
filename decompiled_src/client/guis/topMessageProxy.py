#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/topMessageProxy.o
from Scaleform import GfxValue
import uiConst
import gameglobal
import ui
from uiProxy import UIProxy
from ui import gbk2unicode
MSG_TYPE_RED = 1
MSG_TYPE_BLUE = 2

class TopMessageProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TopMessageProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.mediator = None
        self.msgMed2 = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_TOP_MESSAGE:
            self.mediator = mediator
        elif widgetId == uiConst.WIDGET_TOP_MESSAGE2:
            self.msgMed2 = mediator

    def showTopMsg(self, msg):
        if self.mediator != None:
            self.mediator.Invoke('showTopMessage', GfxValue(gbk2unicode(msg)))

    @ui.checkWidgetLoaded(uiConst.WIDGET_TOP_MESSAGE2)
    def showTopRedMsg(self, msg):
        if self.msgMed2:
            self.msgMed2.Invoke('showTopMessage', (GfxValue(gbk2unicode(msg)), GfxValue(MSG_TYPE_RED)))

    @ui.checkWidgetLoaded(uiConst.WIDGET_TOP_MESSAGE2)
    def showTopBlueMsg(self, msg):
        if self.msgMed2:
            self.msgMed2.Invoke('showTopMessage', (GfxValue(gbk2unicode(msg)), GfxValue(MSG_TYPE_BLUE)))

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TOP_MESSAGE)
