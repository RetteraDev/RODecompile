#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/dyePanelProxy.o
import gameglobal
from uiProxy import SlotDataProxy
from guis import uiConst

class DyePanelProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(DyePanelProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.bindType = 'dyePanel'
        self.type = 'dyePanel'
        self.modelMap = {}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_DYE_PANEL, self.hide)

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DYE_PANEL)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DYE_PANEL:
            self.mediator = mediator

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        if self.mediator:
            self.mediator = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DYE_PANEL)

    def reset(self):
        super(self.__class__, self).reset()
        self.mediator = None
