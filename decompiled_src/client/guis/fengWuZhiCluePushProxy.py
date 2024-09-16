#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fengWuZhiCluePushProxy.o
from gamestrings import gameStrings
import gameglobal
import uiConst
import uiUtils
from uiProxy import UIProxy
from data import fengwuzhi_item_data as FID
from cdata import game_msg_def_data as GMDD

class FengWuZhiCluePushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FengWuZhiCluePushProxy, self).__init__(uiAdapter)
        self.modelMap = {'showDetail': self.onShowDetail}
        self.mediator = None
        self.itemId = 0

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FENG_WU_ZHI_CLUE_PUSH:
            self.mediator = mediator
            self.refreshInfo()

    def reset(self):
        self.itemId = 0

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FENG_WU_ZHI_CLUE_PUSH)

    def show(self, itemId):
        if not gameglobal.rds.configData.get('enableFengWuZhi', False):
            return
        self.itemId = itemId
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FENG_WU_ZHI_CLUE_PUSH)

    def refreshInfo(self):
        if self.mediator:
            info = {}
            fid = FID.data.get(self.itemId, {})
            if not fid:
                return
            info['itemId'] = self.itemId
            info['name'] = fid.get('name', '')
            info['desc'] = uiUtils.getTextFromGMD(GMDD.data.FENG_WU_ZHI_CLUE_PUSH_HINT, gameStrings.TEXT_FENGWUZHICLUEPUSHPROXY_51)
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onShowDetail(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.fengWuZhi.showDetailCluePanel(itemId)
        self.hide()
