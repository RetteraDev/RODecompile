#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/itemChooseProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
import events
from item import Item
from uiProxy import UIProxy
from guis.asObject import ASObject
from gameStrings import gameStrings
from data import consumable_item_data as CID
from cdata import item_select_data as ISD
X_OFFSET = 80
Y_OFFSET = 100
X_BEGIN = 0
Y_BEGIN = 0
REWARD_ITEM_CONTENT = 'ItemChoose_ItemContent'
LINE_MAX_NUM = 4
SHOW_TYPE_PREVIEW = 0
SHOW_TYPE_CHOOSE = 1
HIT_HEIGHT = 402
CFM_BTN_Y = 359
CHOOSEMC_HEIGHT = 49

class ItemChooseProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ItemChooseProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ITEM_CHOOSE, self.hide)

    def reset(self):
        self.itemNum = 0
        self.choosedNum = 0
        self.itemList = []
        self.choosedItemList = []
        self.choosedItemIndexes = []
        self.showType = 0
        self.itemData = {}
        self.rewardItems = []
        self.page = 0
        self.pos = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ITEM_CHOOSE:
            self.widget = widget
            self.initUI()

    def show(self, itemId, showType, page = 0, pos = 0):
        self.itemId = itemId
        self.showType = showType
        self.page = page
        self.pos = pos
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ITEM_CHOOSE)
        else:
            self.initUI()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ITEM_CHOOSE)
        self.widget = None
        self.reset()

    def initUI(self):
        p = BigWorld.player()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.numTitle.visible = self.showType == SHOW_TYPE_CHOOSE
        self.widget.counter.visible = self.showType == SHOW_TYPE_CHOOSE
        self.widget.maxBtn.visible = self.showType == SHOW_TYPE_CHOOSE
        if self.showType == SHOW_TYPE_PREVIEW:
            title = gameStrings.ITEM_CHOOSE_TYPE_PREVIEW
            btnLabel = gameStrings.ITEM_CHOOSE_TYPE_PREVIEW_BTN
            self.widget.hit.height = HIT_HEIGHT - CHOOSEMC_HEIGHT
            self.widget.confirmBtn.y = CFM_BTN_Y - CHOOSEMC_HEIGHT
        else:
            title = gameStrings.ITEM_CHOOSE_TYPE_CHOOSE
            btnLabel = gameStrings.ITEM_CHOOSE_TYPE_CHOOSE_BTN
            self.widget.hit.height = HIT_HEIGHT
            self.widget.confirmBtn.y = CFM_BTN_Y
            boxItem = p.inv.getQuickVal(self.page, self.pos)
            boxNum = boxItem.cwrap
            self.widget.counter.maxCount = max(1, boxNum)
            self.widget.counter.minCount = 1
            self.widget.maxBtn.addEventListener(events.BUTTON_CLICK, self.onMaxBtnClick)
        self.widget.title.textField.text = title
        self.widget.confirmBtn.label = btnLabel
        self.refreshPanel()

    def onMaxBtnClick(self, *args):
        self.widget.counter.count = self.widget.counter.maxCount

    def refreshPanel(self):
        itemInfo = CID.data.get(self.itemId)
        selectIndex = 0
        selectMaxNum = 0
        selectItemList = ()
        if itemInfo:
            selectIndex = itemInfo.get('selectIndex', 0)
        self.itemData = ISD.data.get(selectIndex, {})
        if self.itemData:
            selectMaxNum = self.itemData.get('selectMaxNum', 0)
            selectItemList = self.itemData.get('selectItemList', ())
        totalNum = len(selectItemList)
        self.widget.rule.text = gameStrings.ITEM_CHOOSE_NUMBER_DESC % (totalNum, selectMaxNum)
        self.widget.chooseNum.text = '%d/%d' % (self.choosedNum, self.itemData.get('selectMaxNum', 0))
        self.widget.removeAllInst(self.widget.rewardContent.canvas)
        for i in xrange(len(selectItemList)):
            item = self.widget.getInstByClsName(REWARD_ITEM_CONTENT)
            item.name = 'item%d' % i
            item.x = X_BEGIN + i % LINE_MAX_NUM * X_OFFSET
            if i >= LINE_MAX_NUM:
                item.y = Y_BEGIN + i / LINE_MAX_NUM * Y_OFFSET
            itemInfo = selectItemList[i]
            item.slot.setItemSlotData(uiUtils.getGfxItemById(itemInfo[0], itemInfo[1]))
            item.slot.itemId = itemInfo[0]
            item.slot.addEventListener(events.MOUSE_CLICK, self.handleShowFit)
            item.checkBox.selected = False
            item.checkBox.index = i
            item.checkBox.data = itemInfo[0]
            item.checkBox.addEventListener(events.BUTTON_CLICK, self.handleSelect)
            item.slot.dragable = False
            self.widget.rewardContent.canvas.addChild(item)
            self.rewardItems.append(item)

        self.widget.rewardContent.refreshHeight()
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleConfirm)
        self.widget.confirmBtn.enabled = False
        self.refreshCheckBoxEnabled()

    def refreshChooseNum(self):
        self.widget.chooseNum.text = '%d/%d' % (self.choosedNum, self.itemData.get('selectMaxNum', 0))

    def handleConfirm(self, *args):
        p = BigWorld.player()
        if self.page >= 0 and self.pos >= 0:
            boxItem = p.inv.getQuickVal(self.page, self.pos)
            if boxItem.id == self.itemId:
                p.cell.confirmSelectItemList(self.page, self.pos, self.widget.counter.count, self.choosedItemIndexes)
        self.hide()

    def refreshCheckBoxEnabled(self):
        if self.showType == SHOW_TYPE_PREVIEW:
            for i, rewardItem in enumerate(self.rewardItems):
                rewardItem.checkBox.enabled = False

        else:
            selectMaxNum = self.itemData.get('selectMaxNum', 0)
            if self.choosedNum >= selectMaxNum:
                for i, rewardItem in enumerate(self.rewardItems):
                    if i not in self.choosedItemIndexes:
                        rewardItem.checkBox.enabled = False

            else:
                for i, rewardItem in enumerate(self.rewardItems):
                    rewardItem.checkBox.enabled = True

    def handleSelect(self, *args):
        selectMaxNum = self.itemData.get('selectMaxNum', 0)
        e = ASObject(args[3][0])
        itemCheckBox = e.currentTarget
        itemCheckBox.focused = False
        if not itemCheckBox.selected:
            self.choosedNum -= 1
            self.choosedItemIndexes.remove(int(itemCheckBox.index))
            self.choosedItemList.remove(int(itemCheckBox.data))
        else:
            if self.choosedNum >= selectMaxNum:
                return
            self.choosedNum += 1
            self.choosedItemIndexes.append(int(itemCheckBox.index))
            self.choosedItemList.append(int(itemCheckBox.data))
        self.refreshChooseNum()
        self.refreshCheckBoxEnabled()
        if self.choosedNum == selectMaxNum:
            self.widget.confirmBtn.enabled = True
        else:
            self.widget.confirmBtn.enabled = False

    def handleShowFit(self, *args):
        e = ASObject(args[3][0])
        itemId = int(e.currentTarget.itemId)
        if itemId and e.ctrlKey and e.buttonIdx == uiConst.LEFT_BUTTON:
            cidData = CID.data.get(itemId, {})
            sType = cidData.get('sType', 0)
            if sType == Item.SUBTYPE_2_GET_SELECT_ITEM:
                gameglobal.rds.ui.itemChoose.show(itemId, showType=0)
            else:
                self.uiAdapter.fittingRoom.addItem(Item(itemId))
