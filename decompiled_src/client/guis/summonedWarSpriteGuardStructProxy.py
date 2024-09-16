#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteGuardStructProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import ASObject
from data import summon_sprite_accessory_template_data as SSATD

class SummonedWarSpriteGuardStructProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteGuardStructProxy, self).__init__(uiAdapter)
        self.widget = None
        self.selectIdx = None
        self.selectItem = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_VOID_SUMMONED_WAR_SPRITE_GUARD_STRUCT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_VOID_SUMMONED_WAR_SPRITE_GUARD_STRUCT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def show(self):
        if self.widget:
            self.refreshInfo()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_VOID_SUMMONED_WAR_SPRITE_GUARD_STRUCT, True)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_VOID_SUMMONED_WAR_SPRITE_GUARD_STRUCT)

    def reset(self):
        self.selectIdx = None
        self.selectItem = None

    def initUI(self):
        self.widget.scrollWndList.itemRenderer = 'SummonedWarSpriteGuardStruct_structItem'
        self.widget.scrollWndList.dataArray = []
        self.widget.scrollWndList.lableFunction = self.itemFunction
        self.widget.scrollWndList.itemHeight = 66

    def _onSureBtnClick(self, e):
        p = BigWorld.player()
        p.base.setAccessoryTemplate(self.selectIdx)
        self.hide()

    def _onCancelBtnClick(self, e):
        self.hide()

    def updateItemMcClick(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if not itemMc.structItem.enabled:
            return
        if self.selectItem and self.selectItem.idx == itemMc.idx:
            return
        if self.selectItem:
            self.selectItem.structItem.selected = False
        itemMc.structItem.selected = True
        self.selectItem = itemMc
        self.selectIdx = itemMc.idx

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        learnedList = p.summonedSpriteAccessory.learnedTemplate
        templateId = p.summonedSpriteAccessory.templateId
        itemList = []
        data = SSATD.data
        for i, idx in enumerate(data):
            itemInfo = {}
            itemInfo['idx'] = idx
            itemInfo['name'] = data[idx].get('name', '')
            itemInfo['icon'] = data[idx].get('icon', '')
            itemInfo['type'] = data[idx].get('type', '')
            itemInfo['templateId'] = 0
            if templateId and templateId == idx:
                itemInfo['templateId'] = templateId
            itemInfo['unlock'] = False
            if idx in learnedList:
                itemInfo['unlock'] = True
            itemList.append(itemInfo)

        self.widget.scrollWndList.dataArray = itemList

    def handleStateChange(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        target.structName.text = target.szName
        target.structTypeText.text = target.typeName

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.idx = itemData.idx
        iconPath = uiConst.ITEM_ICON_IMAGE_RES_40 + str(itemData.icon) + '.dds'
        itemMc.icon.clear()
        itemMc.icon.fitSize = True
        itemMc.icon.loadImage(iconPath)
        if itemData.unlock:
            itemMc.structItem.enabled = True
            szName = itemData.name
        else:
            itemMc.structItem.enabled = False
            szName = '%s%s' % (itemData.name, gameStrings.SUMMONED_WAR_SPRITE_SRTUCT_NOT_AVALIABLE)
        itemMc.structItem.szName = szName
        itemMc.structItem.typeName = itemData.type
        itemMc.structItem.structName.text = szName
        itemMc.structItem.structTypeText.text = itemData.type
        itemMc.structItem.addEventListener(events.COMPONENT_STATE_CHANGE, self.handleStateChange)
        itemMc.structItem.selected = False
        if itemMc.structItem.enabled and itemData.templateId and itemData.templateId == itemData.idx:
            itemMc.structItem.selected = True
            self.selectIdx = itemMc.idx
            self.selectItem = itemMc
        itemMc.addEventListener(events.MOUSE_DOWN, self.updateItemMcClick, False, 0, True)
