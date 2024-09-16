#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/itemMsgBoxProxy.o
import BigWorld
import events
import keys
import const
import ui
import uiConst
import uiUtils
import ItemMsgBoxExtend
from gamestrings import gameStrings
from uiProxy import SlotDataProxy
from asObject import ASObject
EXTEND_NAME_MAP = {uiConst.ITEM_MSG_BOX_EXTEND_FASHION: 'FashionExtend'}

class ItemMsgBoxProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(ItemMsgBoxProxy, self).__init__(uiAdapter)
        self.widget = None
        self.bindType = 'itemMsgBox'
        self.type = 'itemMsgBox'
        self.extendMap = {}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ITEM_MSG_BOX, self.escFunc)

    def reset(self):
        self.title = ''
        self.msg = ''
        self.slotNum = 1
        self.yesCallback = None
        self.yesBtnText = ''
        self.noCallback = None
        self.noBtnText = ''
        self.escCallBack = None
        self.itemDisabledFunc = None
        self.checkSetItemFunc = None
        self.findEmptyPosFunc = None
        self.posMap = {}
        self.itemIdList = []

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ITEM_MSG_BOX:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ITEM_MSG_BOX)
        self.uiAdapter.inventory.updateCurrentPageSlotState()
        self.uiAdapter.fashionBag.updateCurrentPageSlotState()

    def escFunc(self):
        if self.escCallBack:
            self.escCallBack()
        else:
            self.hide()

    def showExtend(self, extendType):
        if self.widget:
            self.widget.swapPanelToFront()
            return
        if extendType not in EXTEND_NAME_MAP:
            return
        if extendType not in self.extendMap:
            self.extendMap[extendType] = getattr(ItemMsgBoxExtend, EXTEND_NAME_MAP[extendType])(self)
        self.extendMap[extendType].show()

    def show(self, title = '', msg = '', slotNum = 1, yesCallback = None, yesBtnText = '', noCallback = None, noBtnText = '', escCallBack = None, itemDisabledFunc = None, checkSetItemFunc = None, findEmptyPosFunc = None):
        if self.widget:
            self.widget.swapPanelToFront()
            return
        self.title = title
        self.msg = msg
        self.slotNum = slotNum
        self.yesCallback = yesCallback
        self.yesBtnText = yesBtnText
        self.noCallback = noCallback
        self.noBtnText = noBtnText
        self.escCallBack = escCallBack
        self.itemDisabledFunc = itemDisabledFunc
        self.checkSetItemFunc = checkSetItemFunc
        self.findEmptyPosFunc = findEmptyPosFunc
        self.posMap = {}
        self.itemIdList = []
        self.uiAdapter.loadWidget(uiConst.WIDGET_ITEM_MSG_BOX)

    def initUI(self):
        self.widget.title.textField.text = self.title if self.title else gameStrings.ITEM_MSG_BOX_TITLE_DEFAULT
        self.widget.contenttext.htmlText = self.msg
        self.widget.contenttext.height = self.widget.contenttext.textHeight + 5
        self.widget.removeAllInst(self.widget.itemList)
        posX = int((self.widget.hit.width - 54 * self.slotNum) / 2 - (self.slotNum - 1) * 3)
        posY = int(self.widget.contenttext.y + self.widget.contenttext.height + 10)
        for i in xrange(self.slotNum):
            itemMc = self.widget.getInstByClsName('M12_InventorySlot')
            if not itemMc:
                continue
            itemMc.name = 'itemSlot%d' % i
            itemMc.idx = i
            itemMc.binding = self._getKey(i)
            itemMc.dragable = False
            itemMc.x = posX
            itemMc.y = posY
            posX += 60
            itemMc.addEventListener(events.MOUSE_CLICK, self.handleClickItem, False, 0, True)
            self.widget.itemList.addChild(itemMc)

        self.widget.yesBtn.label = self.yesBtnText if self.yesBtnText else gameStrings.ITEM_MSG_BOX_YESBTN_LABEL_DEFAULT
        self.widget.noBtn.label = self.noBtnText if self.noBtnText else gameStrings.ITEM_MSG_BOX_NOBTN_LABEL_DEFAULT
        self.widget.line.y = posY + 70
        self.widget.yesBtn.y = posY + 76
        self.widget.noBtn.y = posY + 76
        self.widget.bottom.y = posY + 101
        self.widget.hit.height = posY + 119
        BigWorld.callback(0.1, self.uiAdapter.inventory.updateCurrentPageSlotState)
        BigWorld.callback(0.1, self.uiAdapter.fashionBag.updateCurrentPageSlotState)

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            self.itemIdList = []
            for i in xrange(self.slotNum):
                itemMc = getattr(self.widget.itemList, 'itemSlot%d' % i)
                if not itemMc:
                    continue
                item = self.getItemByPos(i)
                if item:
                    self.itemIdList.append(item.id)
                    kind, _, _ = self.posMap.get(i, (0, 0, 0))
                    if kind == const.RES_KIND_INV:
                        itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
                    elif kind == const.RES_KIND_FASHION_BAG:
                        itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_FASHION_BAG)
                    else:
                        itemInfo = uiUtils.getGfxItem(item)
                    itemInfo['state'] = self.calcSlotState(item)
                    itemMc.setItemSlotData(itemInfo)
                else:
                    itemMc.setItemSlotData(None)

            return

    def calcSlotState(self, item):
        p = BigWorld.player()
        if hasattr(item, 'shihun') and item.shihun == True:
            state = uiConst.EQUIP_SHIHUN_REPAIR
        elif not item.canUseNow(p.physique.sex, p.realSchool, p.physique.bodyType, p.lv, p):
            state = uiConst.EQUIP_NOT_USE
        else:
            state = uiConst.ITEM_NORMAL
        return state

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[10:]), int(idItem[4:]))

    def _getKey(self, slot):
        return 'itemMsgBox0.slot%d' % slot

    def _onYesBtnClick(self, e):
        if self.yesCallback:
            self.yesCallback()

    def _onNoBtnClick(self, e):
        if self.noCallback:
            self.noCallback()
        else:
            self.hide()

    def isItemDisabled(self, kind, page, pos, item):
        if not self.widget:
            return False
        if self.itemDisabledFunc:
            return self.itemDisabledFunc(kind, page, pos, item)
        return False

    def findEmptyPos(self):
        if self.findEmptyPosFunc:
            return self.findEmptyPosFunc()
        for pos in xrange(self.slotNum):
            if pos not in self.posMap:
                return pos

        return -1

    def getItem(self, kind, page, pos):
        p = BigWorld.player()
        if kind == const.RES_KIND_INV:
            item = p.inv.getQuickVal(page, pos)
        elif kind == const.RES_KIND_FASHION_BAG:
            item = p.fashionBag.getQuickVal(page, pos)
        else:
            item = None
        return item

    def getItemByPos(self, pos):
        if pos not in self.posMap:
            return None
        else:
            kind, page, pos = self.posMap.get(pos)
            return self.getItem(kind, page, pos)

    def trySetItem(self, kind, page, pos, desPos):
        if not self.widget:
            return
        if desPos < 0 or desPos >= self.slotNum:
            return
        srcItem = self.getItem(kind, page, pos)
        if not srcItem:
            return
        if not self.checkSetItemFunc or self.checkSetItemFunc(srcItem):
            self.setItem(kind, page, pos, desPos)

    def setItem(self, kind, page, pos, desPos):
        if not self.widget:
            return
        if desPos in self.posMap:
            resKind, _, _ = self.posMap.pop(desPos)
        else:
            resKind = kind
        self.posMap[desPos] = (kind, page, pos)
        self.refreshInfo()
        if resKind != kind:
            self.updateResSlotState(resKind)
        self.updateResSlotState(kind)

    def handleClickItem(self, *args):
        e = ASObject(args[3][0])
        if e.buttonIdx == uiConst.RIGHT_BUTTON:
            itemMc = e.currentTarget
            self.removeItem(itemMc.idx)

    def removeItem(self, pos):
        if pos not in self.posMap:
            return
        resKind, resPage, resPos = self.posMap.pop(pos)
        self.refreshInfo()
        self.updateResSlotState(resKind)

    def updateResSlotState(self, kind):
        if kind == const.RES_KIND_INV:
            self.uiAdapter.inventory.updateCurrentPageSlotState()
        elif kind == const.RES_KIND_FASHION_BAG:
            self.uiAdapter.fashionBag.updateCurrentPageSlotState()

    @ui.uiEvent(uiConst.WIDGET_ITEM_MSG_BOX, (events.EVENT_INVENTORY_ITEM_CLICKED, events.EVENT_FASHION_ITEM_CLICKED))
    def onRightClick(self, event):
        if event.name == events.EVENT_INVENTORY_ITEM_CLICKED:
            kind = const.RES_KIND_INV
        elif event.name == events.EVENT_FASHION_ITEM_CLICKED:
            kind = const.RES_KIND_FASHION_BAG
        else:
            return
        event.stop()
        item = event.data['item']
        page = event.data['page']
        pos = event.data['pos']
        if item == None:
            return
        else:
            desPos = self.findEmptyPos()
            self.trySetItem(kind, page, pos, desPos)
            return
