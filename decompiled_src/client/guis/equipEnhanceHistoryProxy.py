#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipEnhanceHistoryProxy.o
import time
import BigWorld
import gameglobal
from guis import uiConst
from guis import uiUtils
from guis.uiProxy import UIProxy

class EquipEnhanceHistoryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipEnhanceHistoryProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.closeWidget,
         'refreshPanel': self.refreshPanel}
        self.mediator = None
        self.isShow = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_ENHANCE_HISTORY, self.hide)

    def closeWidget(self, *args):
        self.clearWidget()

    def clearWidget(self):
        self.mediator = None
        self.isShow = False
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_ENHANCE_HISTORY)

    def show(self):
        self.isShow = True
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_ENHANCE_HISTORY)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_ENHANCE_HISTORY:
            self.mediator = mediator

    def refreshHistoryInfo(self):
        if self.mediator:
            if gameglobal.rds.ui.equipChangeEnhance.panelMc:
                item = gameglobal.rds.ui.equipChangeEnhance.getEnhanceItem()
            else:
                item = gameglobal.rds.ui.equipEnhance.getEnhanceItem()
            if not item:
                return
            history = BigWorld.player().getEnhanceHistory(item.uuid)
            itemList = []
            for i in history:
                item = {}
                item['time'] = time.strftime('%Y.%m.%d  %H:%M', i[0])
                item['content'] = i[1]
                itemList.append(item)

            ret = uiUtils.array2GfxAarry(itemList, True)
            self.mediator.Invoke('setNowInfo', ret)

    def toggle(self):
        if self.isShow == False:
            self.show()
        else:
            self.clearWidget()

    def refreshPanel(self, *args):
        self.refreshHistoryInfo()
