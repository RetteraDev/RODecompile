#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteFightSelectProxy.o
import BigWorld
import uiConst
import events
import tipUtils
import utils
import gameglobal
from uiProxy import UIProxy
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import ASUtils
from gamestrings import gameStrings
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'

class SummonedWarSpriteFightSelectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteFightSelectProxy, self).__init__(uiAdapter)
        self.widget = None
        self.spriteIndex = 0
        self.pos = 0
        self.selectedCallback = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_FIGHT_SELECT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_FIGHT_SELECT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_FIGHT_SELECT)

    def reset(self):
        self.pos = 0

    def show(self, spriteIndex, pos, selectedCallback = None):
        self.spriteIndex = spriteIndex
        self.pos = pos
        if self.widget:
            self.refreshInfo()
            return
        self.selectedCallback = selectedCallback
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_FIGHT_SELECT, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.spriteTypeDropdown.addEventListener(events.INDEX_CHANGE, self.handleSelectWarSpriteType, False, 0, True)
        self.widget.spriteList.itemRenderer = 'SummonedWarSpriteReadyFightSelect_spriteItem'
        self.widget.spriteList.barAlwaysVisible = True
        self.widget.spriteList.dataArray = []
        self.widget.spriteList.lableFunction = self.itemFunction
        self.typeToSort = SCD.data.get('spriteMajorAbility', [])
        typeList = []
        for i, vlaue in enumerate(self.typeToSort):
            typeInfo = {}
            typeInfo['label'] = gameStrings.SUMMONED_WAR_SPRITE_TXT1 + '<font color=\"#de5900\">' + vlaue + '</font>' + gameStrings.SUMMONED_WAR_SPRITE_TXT2
            typeInfo['typeIndex'] = i
            typeList.append(typeInfo)

        ASUtils.setDropdownMenuData(self.widget.spriteTypeDropdown, typeList)
        self.widget.spriteTypeDropdown.menuRowCount = min(len(typeList), 5)
        if self.widget.spriteTypeDropdown.selectedIndex == -1:
            self.widget.spriteTypeDropdown.selectedIndex = 0

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        spriteNumLimit = SCD.data.get('spriteNumLimit', 20)
        self.widget.holdSpritesText.text = '%d/%d' % (len(p.summonSpriteList), spriteNumLimit)
        self.updateWarSpritesTypeList(self.widget.spriteTypeDropdown.selectedIndex)

    def handleSelectWarSpriteType(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.selectedIndex != -1:
            self.updateWarSpritesTypeList(itemMc.selectedIndex)

    def handleSelSpriteDown(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        target.selected = True
        p = BigWorld.player()
        if self.selectedCallback:
            self.selectedCallback(target.spriteIndex, self.pos)
        else:
            p.base.insertPendingSprite(target.spriteIndex, self.pos)

    def updateWarSpritesTypeList(self, typeIndex):
        p = BigWorld.player()
        warSpriteList = gameglobal.rds.ui.summonedWarSpriteMine.sortWarSpriteList(typeIndex)
        spriteItemList = []
        for i in xrange(len(warSpriteList)):
            spriteInfo = warSpriteList[i]
            props = spriteInfo.get('props', {})
            spriteIndex = spriteInfo.get('index', 0)
            itemInfo = {}
            itemInfo['spriteIndex'] = spriteIndex
            itemInfo['spriteId'] = spriteInfo.get('spriteId', 0)
            itemInfo['name'] = spriteInfo.get('name', '')
            itemInfo['lv'] = props.get('lv', 0)
            itemInfo['familiar'] = props.get('familiar', 0)
            itemInfo['famiEffAdd'] = props.get('famiEffAdd', 0)
            itemInfo['beReadyFight'] = gameglobal.rds.ui.summonedWarSpriteFight.checkSpriteReadyFightState(spriteIndex)
            spriteItemList.append(itemInfo)

        self.widget.spriteList.dataArray = spriteItemList
        self.widget.spriteList.validateNow()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.spriteIndex = itemData.spriteIndex
        itemMc.groupName = 'empty'
        itemMc.groupName = 'summonedWarSpriteFightSelect%s'
        itemMc.spriteIndex = itemData.spriteIndex
        szFamiVal = '%d+%d' % (itemData.familiar, itemData.famiEffAdd)
        itemMc.labels = [itemData.name, itemData.lv, szFamiVal]
        iconId = SSID.data.get(itemData.spriteId, {}).get('spriteIcon', '000')
        iconPath = SPRITE_ICON_PATH % str(iconId)
        itemMc.itemSlot.slot.setItemSlotData({'iconPath': iconPath})
        itemMc.readyFight.visible = itemData.beReadyFight
        if utils.getSpriteBattleState(itemMc.warSpriteIndex) and utils.getSpriteAccessoryState(itemMc.warSpriteIndex):
            itemMc.spriteState.visible = True
            itemMc.spriteState.gotoAndStop('zhanAndfu')
        elif utils.getSpriteBattleState(itemMc.warSpriteIndex):
            itemMc.spriteState.visible = True
            itemMc.spriteState.gotoAndStop('zhan')
        elif utils.getSpriteAccessoryState(itemMc.warSpriteIndex):
            itemMc.spriteState.visible = True
            itemMc.spriteState.gotoAndStop('fu')
        else:
            itemMc.spriteState.visible = False
        if self.spriteIndex and self.spriteIndex == itemData.spriteIndex:
            itemMc.enabled = False
            itemMc.removeEventListener(events.MOUSE_DOWN, self.handleSelSpriteDown)
        else:
            itemMc.enabled = True
            itemMc.addEventListener(events.MOUSE_DOWN, self.handleSelSpriteDown, False, 0, True)
        itemMc.validateNow()
        itemMc.mouseChildren = True
        itemMc.itemSlot.slot.validateNow()
        TipManager.addTipByType(itemMc.itemSlot.slot, tipUtils.TYPE_SPRITE_HEAD_TIP, (itemData.spriteIndex,), False, 'upLeft')
