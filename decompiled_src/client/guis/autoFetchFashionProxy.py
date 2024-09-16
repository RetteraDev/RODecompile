#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/autoFetchFashionProxy.o
import BigWorld
import gameglobal
from item import Item
from uiProxy import SlotDataProxy
from guis import uiConst
from guis import uiUtils
FILTERS = {1: Item.FASHION_BAG_FASHION,
 2: Item.FASHION_BAG_JEWELRY,
 3: Item.FASHION_BAG_PENDANT,
 4: [Item.EQUIP_BASETYPE_ARMOR, 8]}

class AutoFetchFashionProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(AutoFetchFashionProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.bindType = 'autoFetchFashion'
        self.type = 'autoFetchFashion'
        self.modelMap = {'close': self.onClose,
         'confirm': self.onConfirm,
         'getSelectList': self.onGetSelectList}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_AUTO_FETCH_FASHION, self.hide)

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_AUTO_FETCH_FASHION)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_AUTO_FETCH_FASHION:
            self.mediator = mediator

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        if self.mediator:
            self.mediator = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_AUTO_FETCH_FASHION)

    def onGetSelectList(self, *args):
        p = BigWorld.player()
        return uiUtils.array2GfxAarry(p.fashionBag.selectList)

    def reset(self):
        super(self.__class__, self).reset()
        self.mediator = None

    def onClose(self, *arg):
        self.hide()

    def onConfirm(self, *arg):
        arLen = int(arg[3][0].GetNumber())
        ar = arg[3][1]
        selectList = []
        for id in range(0, arLen):
            selectList.append(int(ar.GetElement(id).GetNumber()))

        p = BigWorld.player()
        p.fashionBag.selectList = selectList
        p.base.inv2fashionBagFilter(selectList)
        self.hide()
