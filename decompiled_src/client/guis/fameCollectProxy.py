#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fameCollectProxy.o
import gameglobal
import uiUtils
from uiProxy import UIProxy
from guis import ui
from guis import uiConst
from data import fame_data as FD

class FameCollectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FameCollectProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FAME_COLLECT_TIP:
            self.tipMed = mediator
            return uiUtils.dict2GfxDict(self.fameCollectData, True)

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_FAME_COLLECT_TIP:
            self.tipMed = None
            self.fameCollectData = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FAME_COLLECT_TIP)

    @ui.scenarioCallFilter()
    def showTip(self, fameData):
        self.fameCollectData = {'desc': fameData.get('name', ''),
         'name': FD.data.get(fameData.get('fameId', 0)).get('name', ''),
         'type': fameData.get('type', 0)}
        if self.tipMed:
            self.tipMed.Invoke('refreshTip', uiUtils.dict2GfxDict(self.fameCollectData, True))
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FAME_COLLECT_TIP)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FAME_COLLECT_TIP)

    def reset(self):
        self.tipMed = None
        self.fameCollectData = None
