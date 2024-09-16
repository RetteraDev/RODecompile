#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ItemPreviewSelectProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import uiUtils
import const
from item import Item
from helpers import fittingModel
from guis.asObject import ASObject
from uiProxy import UIProxy
from callbackHelper import Functor
from gameStrings import gameStrings
from guis.asObject import ASUtils
from data import item_data as ID
from data import sys_config_data as SCD
TOLTAL_SLOT_NUM = 3

class ItemPreviewSelectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ItemPreviewSelectProxy, self).__init__(uiAdapter)
        self.widget = None
        self.currSelectIndex = 0
        self.currSelectItemId = 0
        self.currSelectItemName = ''
        self.statePanel = ''
        self.randomItemList = []
        self.page = const.CONT_NO_PAGE
        self.pos = const.CONT_NO_POS
        self.fittingModel = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_ITEM_PREVIEW_SELECT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ITEM_PREVIEW_SELECT:
            self.widget = widget
            self.refreshInfo()

    def show(self, randomItemList, page, pos):
        self.randomItemList = randomItemList
        self.page = page
        self.pos = pos
        if self.widget:
            self.refreshInfo()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ITEM_PREVIEW_SELECT)

    def clearWidget(self):
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ITEM_PREVIEW_SELECT)
        if self.fittingModel:
            self.fittingModel.resetHeadGen()
        self.fittingModel = None

    def reset(self):
        self.currSelectIndex = 0
        self.currSelectItemId = 0
        self.currSelectItemName = ''
        self.statePanel = ''
        self.page = const.CONT_NO_PAGE
        self.pos = const.CONT_NO_POS

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.main.closeBtn
        self.widget.main.confirm.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            self.statePanel = ''
            for itemId in self.randomItemList:
                item = Item(itemId)
                if gameglobal.rds.ui.fittingRoom.checkItemPreview(item, False):
                    self.statePanel = 'yulan'
                else:
                    self.statePanel = 'wupin'
                break

            if self.statePanel == 'yulan':
                self.widget.gotoAndStop(self.statePanel)
                self.initUI()
                self.updateDescribeInfo()
                self.updateSlotInfo()
                self.updateSelectState()
                self.fittingModel = fittingModel.FittingModel('ItemPreviewSelectPhotoGen', 422, None, self)
                self.fittingModel.initHeadGeen()
                self.fittingModel.restorePhoto3D()
                self.updateItemPreview()
                self.widget.main.leftRotateBtn.autoRepeat = True
                self.widget.main.rightRotateBtn.autoRepeat = True
                self.widget.main.leftRotateBtn.repeatDelay = 100
                self.widget.main.rightRotateBtn.repeatDelay = 100
                self.widget.main.leftRotateBtn.repeatInterval = 100
                self.widget.main.rightRotateBtn.repeatInterval = 100
                self.widget.main.leftRotateBtn.addEventListener(events.BUTTON_CLICK, self.handleLeftRotateClick, False, 0, True)
                self.widget.main.rightRotateBtn.addEventListener(events.BUTTON_CLICK, self.handleRightRotateClick, False, 0, True)
            elif self.statePanel == 'wupin':
                self.widget.gotoAndStop(self.statePanel)
                self.initUI()
                self.updateDescribeInfo()
                self.updateSlotInfo()
                self.updateSelectState()
            return

    def handleBtnClick(self, *args):
        msg = gameStrings.ITEM_PREVIEW_CONFIRM_SELECT % self.currSelectItemName
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.onClickConfirmSelect))

    def handleItemClick(self, *args):
        e = ASObject(args[3][0])
        self.currSelectIndex = e.currentTarget.nIndex
        self.updateSelectState()
        if self.statePanel == 'yulan':
            self.updateItemPreview()

    def handleLeftRotateClick(self, *args):
        index = -1
        deltaYaw = -0.104 * index
        headGen = self.fittingModel.headGen if self.fittingModel else None
        if headGen:
            headGen.rotateYaw(deltaYaw)

    def handleRightRotateClick(self, *args):
        index = 1
        deltaYaw = -0.104 * index
        headGen = self.fittingModel.headGen if self.fittingModel else None
        if headGen:
            headGen.rotateYaw(deltaYaw)

    def onClickConfirmSelect(self):
        p = BigWorld.player()
        if self.page != const.CONT_NO_PAGE and self.pos != const.CONT_NO_POS:
            p.cell.confirmGetXinshouItem(self.currSelectItemId, self.page, self.pos)
            self.hide()

    def updateSlotInfo(self):
        for i in range(0, TOLTAL_SLOT_NUM):
            itemSlot = self.widget.main.getChildByName('item%d' % i)
            messageText = self.widget.main.getChildByName('message%d' % i)
            messageText.visible = False
            itemId = self.randomItemList[i]
            itemInfo = uiUtils.getGfxItemById(itemId)
            ASUtils.setHitTestDisable(itemSlot.selectBg, True)
            if itemInfo:
                itemSlot.visible = True
                itemSlot.selectBg.visible = False
                itemSlot.iconSlot.dragable = False
                itemSlot.iconSlot.setItemSlotData(itemInfo)
                itemSlot.addEventListener(events.MOUSE_CLICK, self.handleItemClick, False, 0, True)
            else:
                itemSlot.visible = False
            itemSlot.nIndex = i
            itemSlot.itemId = itemId
            itemSlot.itemName = ID.data.get(itemId, {}).get('name', '')

    def updateSelectState(self):
        for i in range(0, TOLTAL_SLOT_NUM):
            itemSlot = self.widget.main.getChildByName('item%d' % i)
            messageText = self.widget.main.getChildByName('message%d' % i)
            if self.currSelectIndex == itemSlot.nIndex:
                itemSlot.selectBg.visible = True
                messageText.visible = True
                messageText.tiptext.text = gameStrings.ITEM_PREVIEW_SELECTED % itemSlot.itemName
                messageText.tiptext.width = messageText.tiptext.textWidth + 14
                messageText.tipbg.width = messageText.tiptext.textWidth + 14
                self.currSelectItemId = itemSlot.itemId
                self.currSelectItemName = itemSlot.itemName
            else:
                itemSlot.selectBg.visible = False
                messageText.visible = False

    def updateItemPreview(self):
        self.setLoadingMcVisible(False)
        item = Item(self.randomItemList[self.currSelectIndex])
        if self.fittingModel:
            self.fittingModel.addItem(item)

    def updateDescribeInfo(self):
        p = BigWorld.player()
        item = p.inv.getQuickVal(self.page, self.pos)
        if not item:
            self.widget.main.describe.visible = False
            self.widget.main.linkText.visible = False
            return
        itemId = item.id
        previewDesc = ID.data.get(itemId, {}).get('previewItemDesc', '')
        self.widget.main.describe.visible = True
        self.widget.main.describe.text = previewDesc
        previewItemLinkText = ID.data.get(itemId, {}).get('previewItemLinkText', '')
        if previewItemLinkText == '':
            self.widget.main.linkText.visible = False
        else:
            self.widget.main.linkText.htmlText = previewItemLinkText
            self.widget.main.linkText.visible = True
        self.widget.main.title.titleName.text = item.name

    def setLoadingMcVisible(self, bVisible):
        if self.widget:
            self.widget.main.loadingMc.visible = bVisible
