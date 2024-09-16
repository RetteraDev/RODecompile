#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/deepLearningMsgBoxProxy.o
import BigWorld
import uiConst
from guis import uiUtils
from uiProxy import UIProxy
from data import item_data as ID
from cdata import deep_learning_data_apply_item_data as DLDAID

class DeepLearningMsgBoxProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DeepLearningMsgBoxProxy, self).__init__(uiAdapter)
        self.widget = None
        self.itemId = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_DEEP_LEARNING_MSG_BOX, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_DEEP_LEARNING_MSG_BOX:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_DEEP_LEARNING_MSG_BOX)

    def reset(self):
        self.itemId = None

    def show(self, itemId):
        self.itemId = itemId
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_DEEP_LEARNING_MSG_BOX, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.itemSlot.fitSize = True
        self.widget.itemSlot.dragable = False
        self.widget.itemSlot.setItemSlotData(uiUtils.getGfxItemById(self.itemId))
        idData = ID.data.get(self.itemId, {})
        itemName = idData.get('name', '')
        buyCount = 1
        self.widget.itemName.text = itemName
        self.widget.countT.text = str(buyCount)
        deepData = DLDAID.data.get(self.itemId, {})
        priceVal = deepData.get('nowPrice', 0)
        self.widget.txtPrice.text = str(priceVal)
        self.widget.txtTotalCost.text = str(priceVal * buyCount)

    def _onCancelBtnClick(self, e):
        self.hide()

    def _onConfirmBtnClick(self, e):
        p = BigWorld.player()
        p.cell.buyDeepLearningPushItem(self.itemId)
        self.hide()
