#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteSelectProxy.o
import BigWorld
import uiConst
import events
import tipUtils
import summonSpriteExplore
import gameglobal
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import ASUtils
from gamestrings import gameStrings
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
from cdata import game_msg_def_data as GMDD
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'

class SummonedWarSpriteSelectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteSelectProxy, self).__init__(uiAdapter)
        self.widget = None
        self.curSelSpriteIndex = None
        self.selectedIndexs = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_SELECT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_SELECT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_SELECT)

    def reset(self):
        self.curSelSpriteIndex = None
        self.selectedIndexs = []

    def show(self, selectedIndexs):
        self.selectedIndexs = selectedIndexs
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_SELECT, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.spriteTypeDropdown.addEventListener(events.INDEX_CHANGE, self.handleSelectWarSpriteType, False, 0, True)
        self.widget.spriteList.itemRenderer = 'SummonedWarSpriteSelect_spriteItem'
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

    def _onSureBtnClick(self, e):
        gameglobal.rds.ui.summonedWarSpriteExplore.updateSelectedPhoto(self.curSelSpriteIndex)
        self.hide()

    def _onCancelBtnClick(self, e):
        self.hide()

    def handleSelectWarSpriteType(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.selectedIndex != -1:
            self.updateWarSpritesTypeList(itemMc.selectedIndex)

    def handleSelSpriteDown(self, *args):
        target = ASObject(args[3][0]).currentTarget
        if target.selected:
            return
        target.selected = True
        self.curSelSpriteIndex = target.spriteIndex
        self.updateExploredCnt()

    def filterSprite(self, warSpriteList):
        singleLimit = summonSpriteExplore.getExploreSpriteSingleLimit()
        exploredCnts = []
        noExploredCnts = []
        for i in xrange(len(warSpriteList)):
            spriteInfo = warSpriteList[i]
            index = spriteInfo.get('index', 0)
            if index in self.selectedIndexs:
                continue
            exploredCntDay = spriteInfo.get('exploredCntDay', 0)
            if exploredCntDay < singleLimit:
                exploredCnts.append(spriteInfo)
            else:
                noExploredCnts.append(spriteInfo)

        return exploredCnts + noExploredCnts

    def updateWarSpritesTypeList(self, typeIndex):
        warSpriteList = gameglobal.rds.ui.summonedWarSpriteMine.sortWarSpriteList(typeIndex)
        warSpriteList = self.filterSprite(warSpriteList)
        spriteItemList = []
        for i in xrange(len(warSpriteList)):
            spriteInfo = warSpriteList[i]
            props = spriteInfo.get('props', {})
            itemInfo = {}
            itemInfo['spriteIndex'] = spriteInfo.get('index', -1)
            itemInfo['spriteId'] = spriteInfo.get('spriteId', 0)
            itemInfo['name'] = spriteInfo.get('name', '')
            itemInfo['lv'] = props.get('lv', 0)
            itemInfo['familiar'] = props.get('familiar', 0)
            itemInfo['famiEffAdd'] = props.get('famiEffAdd', 0)
            spriteItemList.append(itemInfo)

        self.widget.spriteList.dataArray = spriteItemList
        self.widget.spriteList.validateNow()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.spriteIndex = itemData.spriteIndex
        itemMc.groupName = 'empty'
        itemMc.groupName = 'summonedWarSpriteSelect%s'
        itemMc.addEventListener(events.MOUSE_DOWN, self.handleSelSpriteDown, False, 0, True)
        szFamiVal = '%d + %d' % (itemData.familiar, itemData.famiEffAdd)
        itemMc.labels = [itemData.name, itemData.lv, szFamiVal]
        iconId = SSID.data.get(itemData.spriteId, {}).get('spriteIcon', '000')
        iconPath = SPRITE_ICON_PATH % str(iconId)
        itemMc.itemSlot.slot.setItemSlotData({'iconPath': iconPath})
        itemMc.selected = False
        if not self.curSelSpriteIndex:
            itemMc.selected = True
        elif self.curSelSpriteIndex and self.curSelSpriteIndex == itemData.spriteIndex:
            itemMc.selected = True
        if itemMc.selected:
            self.curSelSpriteIndex = itemData.spriteIndex
            self.updateExploredCnt()
        itemMc.validateNow()
        itemMc.mouseChildren = True
        itemMc.itemSlot.slot.validateNow()
        TipManager.addTipByType(itemMc.itemSlot.slot, tipUtils.TYPE_SPRITE_HEAD_TIP, (itemData.spriteIndex,), False, 'upLeft')

    def updateExploredCnt(self):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList[self.curSelSpriteIndex]
        exploredCntDay = spriteInfo.get('exploredCntDay', 0)
        singleLimit = summonSpriteExplore.getExploreSpriteSingleLimit()
        leftNum = max(0, singleLimit - exploredCntDay)
        desc = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_EXPLORE_CNT_DAY, '%d')
        self.widget.desc.text = desc % leftNum
