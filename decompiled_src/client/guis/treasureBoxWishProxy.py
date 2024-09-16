#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/treasureBoxWishProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import uiUtils
import cPickle
from item import Item
from guis.asObject import ASObject
from uiProxy import UIProxy
from data import sys_config_data as SCD
from data import use_item_wish_data as UIWD
TOLTAL_SLOT_NUM = 8

class TreasureBoxWishProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TreasureBoxWishProxy, self).__init__(uiAdapter)
        self.widget = None
        self.itemId = None
        self.curSelectItem = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_TREASURE_BOX_WISH, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_TREASURE_BOX_WISH:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def show(self, itemId):
        if not gameglobal.rds.configData.get('enableUseItemWish', False):
            return
        self.itemId = itemId
        if self.widget:
            self.refreshInfo()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TREASURE_BOX_WISH)

    def clearWidget(self):
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TREASURE_BOX_WISH)

    def reset(self):
        self.itemId = None
        self.curSelectItem = None

    def _onWishBtnClick(self, e):
        p = BigWorld.player()
        if self.curSelectItem and self.curSelectItem.wishType:
            p.cell.makeItemWish(self.itemId, self.curSelectItem.wishType)
            self.hide()

    def _onCancelWishBtnClick(self, e):
        p = BigWorld.player()
        p.cell.makeItemWish(self.itemId, 0)
        self.hide()

    def handleItemClick(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if self.curSelectItem and self.curSelectItem == itemMc.index:
            return
        if self.curSelectItem:
            self.curSelectItem.selectP.visible = False
        itemMc.selectP.visible = True
        self.curSelectItem = itemMc

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.wishDesc1.text = SCD.data.get('treasureBoxWishDesc1', '')
        self.widget.wishDesc2.text = SCD.data.get('treasureBoxWishDesc2', '')
        self.getCurWishDesc()
        self.updateItemSlotMc()

    def getCurWishDesc(self):
        p = BigWorld.player()
        selectedWishType = None
        if self.itemId in p.useItemWish:
            selectedWishType = p.useItemWish[self.itemId]
        desc = None
        itemList = UIWD.data.get(self.itemId, [])
        for data in itemList:
            wishType = data.get('wishType', 0)
            if selectedWishType and selectedWishType == wishType:
                desc = data.get('wishDesc', '')

        if desc:
            self.widget.curWish.visible = True
            self.widget.curWish.text = desc
        else:
            self.widget.curWish.visible = False

    def updateItemSlotMc(self):
        itemList = UIWD.data.get(self.itemId, [])
        itemNum = len(itemList)
        self.widget.diffArraySlotMc.gotoAndStop('array%d' % itemNum)
        for i in range(itemNum):
            itemMc = self.widget.diffArraySlotMc.itemSlotMc.getChildByName('item%d' % i)
            itemMc.addEventListener(events.MOUSE_CLICK, self.handleItemClick, False, 0, True)
            if i < len(itemList):
                itemMc.visible = True
                data = itemList[i]
                itemMc.index = data.get('id', 0)
                itemMc.wishType = data.get('wishType', 0)
                wishItemId = data.get('wishItemId', 0)
                itemMc.slot.fitSize = True
                itemMc.slot.dragable = False
                itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(wishItemId))
                itemMc.nameText.text = data.get('wishDesc', '')
                itemMc.selectP.visible = False
            else:
                itemMc.visible = False

    def getWishRaffleItemSetInfo(self, itemId):
        p = BigWorld.player()
        if UIWD.data.has_key(itemId) and p.useItemWish.has_key(itemId):
            for data in UIWD.data[itemId]:
                if data['wishType'] == p.useItemWish[itemId]:
                    return data.get('raffleItemSetInfo')

    def checkShowTreasureBoxWish(self, itemId):
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableUseItemWish', False) and itemId in UIWD.data and itemId not in p.useItemWish:
            if itemId not in p.itemWishConfirmInfo:
                p.itemWishConfirmInfo[itemId] = 0
            if p.itemWishConfirmInfo[itemId] < SCD.data.get('itemWishConfirmMaxNum', 0):
                return True
        return False

    def checkShowMessageBox(self, i, cstype, onceType):
        if hasattr(i, 'cstype') and i.cstype and i.cstype == cstype and not gameglobal.rds.ui.messageBox.getCheckOnceData(onceType):
            return True
        return False

    def saveUseItemWishConfirm(self, itemId):
        p = BigWorld.player()
        p.itemWishConfirmInfo[itemId] = p.itemWishConfirmInfo[itemId] + 1
        saveData = cPickle.dumps(p.itemWishConfirmInfo)
        p.base.saveUseItemWishConfirmInfo(saveData)

    def getTreasureBoxWishDesc(self, itemId):
        p = BigWorld.player()
        selectedWishType = None
        itemId = Item.parentId(itemId)
        if itemId in p.useItemWish:
            selectedWishType = p.useItemWish[itemId]
        wishDesc = None
        itemList = UIWD.data.get(itemId, [])
        for data in itemList:
            wishType = data.get('wishType', 0)
            if selectedWishType and selectedWishType == wishType:
                wishDesc = data.get('wishDesc', '')

        return wishDesc
