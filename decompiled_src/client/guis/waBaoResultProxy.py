#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/waBaoResultProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
from uiProxy import UIProxy
from data import item_data as ID

class WaBaoResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WaBaoResultProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.mediator = None
        self.itemId = 0
        self.itemNum = 0
        self.timer = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_WABAO_RESULT, self.hideAll)
        uiAdapter.registerEscFunc(uiConst.WIDGET_WABAO_RESULT_RARE, self.hideAll)

    def _registerMediator(self, widgetId, mediator):
        if widgetId in (uiConst.WIDGET_WABAO_RESULT, uiConst.WIDGET_WABAO_RESULT_RARE):
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WABAO_RESULT)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WABAO_RESULT_RARE)

    def reset(self):
        self.itemId = 0
        self.itemNum = 0
        self.stopTimer()
        gameglobal.rds.sound.stopSound(3986)
        gameglobal.rds.sound.stopSound(3987)

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def show(self, itemId, itemNum, isTreasure):
        self.itemId = itemId
        self.itemNum = itemNum
        if not self.mediator:
            if not isTreasure:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WABAO_RESULT, isModal=True)
                gameglobal.rds.sound.playSound(3986)
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WABAO_RESULT_RARE, isModal=True)
                gameglobal.rds.sound.playSound(3987)
        BigWorld.callback(0.2, BigWorld.player().cell.wabaoTurnDone)

    def refreshInfo(self):
        if self.mediator:
            info = {}
            info['itemId'] = self.itemId
            info['itemName'] = ID.data.get(self.itemId, {}).get('name', '')
            info['itemNum'] = self.itemNum if self.itemNum > 1 else ''
            info['iconPath'] = uiUtils.getItemIconFile150(self.itemId)
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
            self.timer = BigWorld.callback(5.0, self.hideAll)

    def hideAll(self):
        self.hide()
        gameglobal.rds.ui.waBao.hide()
