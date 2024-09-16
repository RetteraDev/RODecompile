#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/itemSelectProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
from guis import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from data import item_data as ID
from cdata import font_config_data as FCD

class ItemSelectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ItemSelectProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.onCloseWidget,
         'getItemsInfo': self.onGetItemsInfo,
         'selectItem': self.onSelectItem,
         'confirm': self.onConfirm}
        self.mediator = None
        self.itemList = []
        self.title = ''
        self.selCallback = None
        self.okCallback = None
        self.selIndx = 0
        self.widgetId = uiConst.WIDGET_ITEM_SELECT
        uiAdapter.registerEscFunc(self.widgetId, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.widgetId:
            self.mediator = mediator

    def show(self, itemList, title, selCallback = None, okCallback = None, isModal = True, tips = None):
        self.itemList = itemList
        self.selCallback = selCallback
        self.okCallback = okCallback
        self.title = title
        self.tips = tips
        gameglobal.rds.ui.loadWidget(self.widgetId, isModal=isModal)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(self.widgetId)
        self.mediator = None

    def reset(self):
        self.itemList = []
        self.selCallback = None
        self.okCallback = None
        self.title = ''
        self.selIndx = 0

    def refreshItemList(self):
        if self.mediator is not None:
            self.mediator.Invoke('refreshItemList')

    def onCloseWidget(self, *arg):
        self.clearWidget()

    def onGetItemsInfo(self, *arg):
        ret = {}
        ret['title'] = self.title
        ret['tips'] = self.tips
        itemsInfo = []
        for item in self.itemList:
            info = {}
            info['itemId'] = item[0]
            info['description'] = item[1]
            info['useNum'] = item[2] if item[2] else 1
            if len(item) >= 4:
                info['description2'] = item[3]
            info['ownNum'] = BigWorld.player().inv.countItemInPages(item[0], enableParentCheck=True)
            self.appendBasicItemInfo(info)
            if info['ownNum'] >= info['useNum']:
                info['state'] = uiConst.ITEM_NORMAL
            else:
                info['state'] = uiConst.COMPLETE_ITEM_LEAKED
            itemsInfo.append(info)

        ret['itemsInfo'] = itemsInfo
        return uiUtils.dict2GfxDict(ret, True)

    def onSelectItem(self, *arg):
        self.selIndx = int(arg[3][0].GetNumber())
        if self.selCallback is not None and self.selIndx < len(self.itemList):
            self.selCallback(self.itemList[self.selIndx])

    def onConfirm(self, *arg):
        if self.okCallback is not None and self.selIndx < len(self.itemList):
            self.okCallback(self.itemList[self.selIndx])

    def appendBasicItemInfo(self, info):
        itemId = info.get('itemId', 0)
        itemInfo = ID.data.get(itemId, {})
        quality = itemInfo.get('quality', 1)
        color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        icon = uiUtils.getItemIconFile64(itemId)
        name = itemInfo.get('name', gameStrings.TEXT_TIANYUMALLPROXY_1455)
        info['name'] = name
        info['color'] = color
        info['iconPath'] = icon
