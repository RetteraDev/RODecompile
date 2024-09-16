#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteLunhuiItemsProxy.o
import BigWorld
import uiConst
import events
import utils
import tipUtils
import ui
import gameglobal
import const
from guis import uiUtils
from uiProxy import UIProxy
from guis.asObject import TipManager
from guis.asObject import ASObject
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
from data import sprite_upgrade_data as SUD
from cdata import game_msg_def_data as GMDD
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'

class SummonedWarSpriteLunhuiItemsProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteLunhuiItemsProxy, self).__init__(uiAdapter)
        self.widget = None
        self.spriteIndex = None
        self.curSelSpriteIndex = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_SPRITE_LUNHUI_ITEMS, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_SPRITE_LUNHUI_ITEMS:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_SPRITE_LUNHUI_ITEMS)
        gameglobal.rds.ui.summonedWarSpriteLunhui.refreshInfo()

    def reset(self):
        self.spriteIndex = None
        self.curSelSpriteIndex = None

    def show(self, spriteIndex):
        self.spriteIndex = spriteIndex
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_SPRITE_LUNHUI_ITEMS)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.help.helpKey = SCD.data.get('spriteLunhuiItemsHelpKey', 0)
        self.widget.desc0.text = uiUtils.getTextFromGMD(GMDD.data.SPRITE_HUNLUN_ITEMS_DESC, '')
        self.widget.spriteList.itemHeight = 65
        self.widget.spriteList.itemRenderer = 'SummonedWarSpriteLunhuiItems_spriteItem'
        self.widget.spriteList.barAlwaysVisible = True
        self.widget.spriteList.dataArray = []
        self.widget.spriteList.lableFunction = self.itemFunction

    def refreshInfo(self):
        if not self.widget:
            return
        spriteList = self.filterSprite()
        if not spriteList:
            self.widget.desc1.visible = True
            self.widget.itemsMc.visible = False
        else:
            self.widget.desc1.visible = False
            self.widget.itemsMc.visible = True
        self.widget.spriteList.dataArray = spriteList

    def _onCancelBtnClick(self, e):
        self.hide()

    def _onTurnBtnClick(self, e):
        if not self.curSelSpriteIndex:
            return
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.curSelSpriteIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        spriteName = spriteInfo.get('name', '')
        props = spriteInfo.get('props', {})
        lv = int(props.get('lv', 0))
        ssidData = SSID.data.get(spriteId, {})
        name = ssidData.get('name', '')
        removeToLunhuiItems = ssidData.get('removeToLunhuiItems', (0, 0))
        items = removeToLunhuiItems[1]
        title = uiUtils.getTextFromGMD(GMDD.data.SPRITE_TURN_TO_GET_ITEMS_TITLE, '')
        msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_TURN_TO_GET_ITEMS, '%s(%s,%d)%d') % (spriteName,
         name,
         lv,
         items)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.realTurn, title=title)

    @ui.checkInventoryLock()
    def realTurn(self):
        p = BigWorld.player()
        p.base.abandonSpriteForLunhuiItem(self.curSelSpriteIndex, p.cipherOfPerson)

    def handleSelSpriteDown(self, *args):
        target = ASObject(args[3][0]).currentTarget
        if target.selected:
            return
        target.selected = True
        self.curSelSpriteIndex = target.spriteIndex
        self.updateLunhuiItems(target.spriteId)

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.spriteIndex = itemData.index
        itemMc.spriteId = itemData.spriteId
        itemMc.groupName = 'empty'
        itemMc.groupName = 'summonedWarSpriteHunlunItems%s'
        itemMc.addEventListener(events.MOUSE_DOWN, self.handleSelSpriteDown, False, 0, True)
        itemMc.szName = itemData.name
        itemMc.szLv = 'lv %d' % itemData.props.lv
        itemMc.labels = [itemMc.szName, itemMc.szLv]
        iconId = SSID.data.get(itemData.spriteId, {}).get('spriteIcon', '000')
        iconPath = SPRITE_ICON_PATH % str(iconId)
        itemMc.itemSlot.slot.setItemSlotData({'iconPath': iconPath})
        itemMc.itemSlot.slot.dragable = False
        if not self.curSelSpriteIndex:
            itemMc.selected = True
        if itemMc.selected:
            self.curSelSpriteIndex = itemData.index
            self.updateLunhuiItems(itemData.spriteId)
        itemMc.validateNow()
        itemMc.mouseChildren = True
        itemMc.itemSlot.slot.validateNow()
        TipManager.addTipByType(itemMc.itemSlot.slot, tipUtils.TYPE_SPRITE_HEAD_TIP, (itemData.index,), False, 'upLeft')

    def filterSprite(self):
        spriteList = []
        p = BigWorld.player()
        for spriteInfo in p.summonSpriteList.values():
            if spriteInfo['index'] == self.spriteIndex:
                continue
            if utils.getSpriteBattleState(spriteInfo['index']):
                continue
            if utils.getSpriteAccessoryState(spriteInfo['index']):
                continue
            naturals = spriteInfo.get('skills', {}).get('naturals', [])
            if len(naturals) != const.SSPRITE_NATURAM_SKILL_NUM_LIMIT:
                continue
            spriteId = spriteInfo.get('spriteId', 0)
            grade = spriteInfo.get('upgradeStage', 0)
            if (spriteId, grade) in SUD.data:
                continue
            spriteList.append(spriteInfo)

        return sorted(spriteList, key=lambda d: d['props']['lv'], reverse=True)

    def updateLunhuiItems(self, spriteId):
        ssidData = SSID.data.get(spriteId, {})
        removeToLunhuiItems = ssidData.get('removeToLunhuiItems', (0, 0))
        items = removeToLunhuiItems[1]
        self.widget.itemsMc.itemsT.text = items

    def turnItemsSucc(self, index):
        if index and self.curSelSpriteIndex == index:
            self.curSelSpriteIndex = None
            self.refreshInfo()
