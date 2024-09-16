#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/shishenBoardProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
import gameglobal
from guis import uiConst
from guis import uiUtils
from data import fb_data as FD
from data import sys_config_data as SCD

class ShishenBoardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ShishenBoardProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.onClose,
         'getContent': self.onGetContent,
         'openHelp': self.onOpenHelp}
        self.mediator = None
        self.fbNo = 0
        self.currentValue = -1
        self.tryOpen = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_SHISHEN_BOARD, self.onClose)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SHISHEN_BOARD:
            self.mediator = mediator

    def show(self, fbNo):
        self.fbNo = fbNo
        self.currentValue = -1
        self.tryOpen = True
        BigWorld.player().cell.getHighShishenModeCnt(self.fbNo)

    def onGetContent(self, *arg):
        ret = {}
        fbData = FD.data.get(self.fbNo, {})
        title = fbData.get('title', gameStrings.TEXT_SHISHENBOARDPROXY_40)
        desc = fbData.get('desc', gameStrings.TEXT_SHISHENBOARDPROXY_41)
        maxValue = fbData.get('crazyShishenModelThreshold', 0)
        currentValue = self.currentValue
        ret['title'] = title
        ret['desc'] = desc
        ret['maxValue'] = maxValue
        ret['currentValue'] = currentValue
        ret['tip'] = SCD.data.get('shishenBoardTip', gameStrings.TEXT_SHISHENBOARDPROXY_49)
        return uiUtils.dict2GfxDict(ret, True)

    def onOpenHelp(self, *arg):
        keyword = SCD.data.get('shishenKeyword', gameStrings.TEXT_SHISHENBOARDPROXY_53)
        gameglobal.rds.ui.help.show(keyword)

    def updateCrazyShishenModeCnt(self, fbNo, cnt):
        if self.fbNo == fbNo:
            self.currentValue = cnt
        if self.currentValue != -1 and self.tryOpen == True:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SHISHEN_BOARD)

    def onClose(self, *arg):
        self.hide()

    def reset(self):
        self.tryOpen = False

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SHISHEN_BOARD)
