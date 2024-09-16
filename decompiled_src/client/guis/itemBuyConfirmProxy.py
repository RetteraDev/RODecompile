#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/itemBuyConfirmProxy.o
import uiUtils
import uiConst
import events
from uiProxy import UIProxy

class ItemBuyConfirmProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ItemBuyConfirmProxy, self).__init__(uiAdapter)
        self.resetData()
        self.widget = None

    def resetData(self):
        self.frameinfo = {}
        self.widget = None

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        self.widget.basicBox.mallScoreLimit.visible = False
        if self.frameinfo.has_key('yesLabel'):
            self.widget.yesBtn.label = self.frameinfo['yesLabel']
        if self.frameinfo.has_key('noLabel'):
            self.widget.noBtn.label = self.frameinfo['noLabel']
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.onCloseClick, False, 0, True)
        self.widget.yesBtn.addEventListener(events.MOUSE_CLICK, self.onYesClick, False, 0, True)
        self.widget.noBtn.addEventListener(events.MOUSE_CLICK, self.onNoClick, False, 0, True)
        itemInfo = self.frameinfo.get('itemInfo', {})
        if itemInfo:
            tag = itemInfo.get('tag', '')
            if tag:
                self.widget.basicBox.itemLabel.gotoAndStop('tag')
            else:
                self.widget.basicBox.itemLabel.visible = False
            self.widget.basicBox.itemName.nameText.htmlText = uiUtils.getItemColorName(itemInfo['itemId'])
            count = itemInfo.get('count', 0)
            self.widget.basicBox.buyNumber.text = str(count)
            price = itemInfo.get('price', 0)
            self.widget.basicBox.priceValue.textField.text = str(price)
            self.widget.basicBox.priceAll.text = str(price * count)
            self.widget.basicBox.itemSlot.setItemSlotData(itemInfo)
            if itemInfo.has_key('bonusType'):
                self.widget.basicBox.valIcon.bonusType = itemInfo['bonusType']
                self.widget.basicBox.allIcon.bonusType = itemInfo['bonusType']

    def onYesClick(self, *args):
        if self.frameinfo.has_key('yesFun'):
            self.frameinfo['yesFun']()
        self.hide()

    def onNoClick(self, *args):
        if self.frameinfo.has_key('noFun'):
            self.frameinfo['noFun']()
        self.hide()

    def onCloseClick(self, *args):
        self.hide()

    def show(self, framInfo):
        if not framInfo:
            return
        self.frameinfo = framInfo
        self.uiAdapter.loadWidget(uiConst.WIDGET_ITEM_BUY_CONFIRM)

    def clearWidget(self):
        self.resetData()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ITEM_BUY_CONFIRM)
