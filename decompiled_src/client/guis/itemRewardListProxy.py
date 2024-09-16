#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/itemRewardListProxy.o
import BigWorld
import math
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis import events
from guis import uiUtils
from item import Item
from guis.asObject import ASObject
from data import consumable_item_data as CID
from data import item_data as ID
from gamestrings import gameStrings
ITEM_START_X = 0
ITEM_START_Y = 0
TITLE_OFFSET_Y = 30
ITEM_OFFSET_Y = 63
ITEM_NUM_PER_LINE = 6

class ItemRewardListProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ItemRewardListProxy, self).__init__(uiAdapter)
        self.widget = None
        self.itemId = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ITEM_REWARD_LIST, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ITEM_REWARD_LIST:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ITEM_REWARD_LIST)

    def show(self, itemId):
        self.itemId = itemId
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ITEM_REWARD_LIST)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshList()

    def refreshList(self):
        itemList = CID.data.get(self.itemId, {}).get('itemQuest', [])
        self.removeAllChild(self.widget.itemPanel.canvas)
        posY = ITEM_START_Y
        for title, itemsInfo in itemList:
            titleMc = self.widget.getInstByClsName('ItemRewardList_title')
            self.widget.itemPanel.canvas.addChild(titleMc)
            titleMc.textField.text = title
            titleMc.x = ITEM_START_X
            titleMc.y = posY
            posY += TITLE_OFFSET_Y
            itemNum = len(itemsInfo)
            groupNum = int(math.ceil(float(itemNum) / ITEM_NUM_PER_LINE))
            currentItemIndex = 0
            for i in xrange(groupNum):
                groupItemMc = self.widget.getInstByClsName('ItemRewardList_items')
                self.widget.itemPanel.canvas.addChild(groupItemMc)
                groupItemMc.x = ITEM_START_X
                groupItemMc.y = posY
                posY += ITEM_OFFSET_Y
                for i in xrange(ITEM_NUM_PER_LINE):
                    itemMc = getattr(groupItemMc, 'item%d' % i)
                    if currentItemIndex < itemNum:
                        item = itemsInfo[currentItemIndex]
                        itemMc.visible = True
                        itemMc.dragable = False
                        itemMc.itemId = item[0]
                        itemMc.itemCount = item[1]
                        itemMc.setItemSlotData(uiUtils.getGfxItemById(item[0], item[1]))
                        itemMc.addEventListener(events.MOUSE_CLICK, self.handleShowFit, False, 0, True)
                    else:
                        itemMc.visible = False
                    currentItemIndex += 1

    def handleShowFit(self, *args):
        e = ASObject(args[3][0])
        itemId = int(e.currentTarget.itemId)
        if e.buttonIdx == uiConst.LEFT_BUTTON:
            cidData = CID.data.get(itemId, {})
            sType = cidData.get('sType', 0)
            if sType == Item.SUBTYPE_2_GET_SELECT_ITEM:
                gameglobal.rds.ui.itemChoose.show(itemId, showType=0)
            else:
                self.uiAdapter.fittingRoom.addItem(Item(itemId))

    def removeAllChild(self, itemMc):
        while itemMc.numChildren > 0:
            itemMc.removeChildAt(0)
