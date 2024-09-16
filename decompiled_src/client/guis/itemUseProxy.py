#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/itemUseProxy.o
import BigWorld
import keys
from guis import uiConst
from uiProxy import UIProxy
from guis import uiUtils

class ItemUseProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ItemUseProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirmUse': self.onConfirmUseItem}
        self.mediator = None
        self.widgetId = uiConst.WIDGET_USE_ITEM
        self.reset()
        uiAdapter.registerEscFunc(self.widgetId, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.widgetId:
            self.mediator = mediator
            return self._getGfxData()

    def clearWidget(self):
        self.mediator = None
        self.uiAdapter.unLoadWidget(self.widgetId)

    def reset(self):
        self.itemId = 0
        self.msg = ''
        self.maxNum = 0
        self.yesCall = None
        self.showType = 'normal'
        self.skillId = 0

    def show(self, itemId, msg, maxNum = 0, yesCall = None, showType = 'normal', skillId = 0):
        self.itemId = itemId
        self.msg = msg
        self.maxNum = maxNum
        self.yesCall = yesCall
        self.showType = showType
        self.skillId = skillId
        if self.mediator:
            self.refresh()
        else:
            self.uiAdapter.loadWidget(self.widgetId)

    def refresh(self):
        if self.mediator:
            self.mediator.Invoke('refresh', self._getGfxData)

    def _getGfxData(self):
        itemNum = BigWorld.player().inv.countItemInPages(self.itemId, enableParentCheck=True)
        itemData = uiUtils.getGfxItemById(self.itemId, itemNum)
        if not itemNum:
            itemData['state'] = uiConst.COMPLETE_ITEM_LEAKED
        else:
            itemData['state'] = uiConst.ITEM_NORMAL
        ret = {'itemData': itemData,
         'msg': self.msg,
         'maxNum': self.maxNum,
         'itemNum': itemNum,
         'showType': self.showType}
        return uiUtils.dict2GfxDict(ret, True)

    def onConfirmUseItem(self, *args):
        if args[3]:
            num = int(args[3][0].GetNumber())
            if num and self.itemId and self.yesCall:
                self.yesCall(self.itemId, num)
        else:
            self.yesCall(self.skillId)
        self.hide()

    def onClickKey(self, key):
        if self.mediator:
            if key == keys.KEY_Y:
                self.mediator.Invoke('handleConfirm')
                return True
            if key == keys.KEY_N:
                self.hide()
                return True
