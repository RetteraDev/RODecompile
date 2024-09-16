#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/itemSourceInforProxy.o
import BigWorld
import gameglobal
import gametypes
import uiUtils
import uiConst
import events
import ui
import const
import copy
import itemToolTipUtils
from guis import asObject
from guis.asObject import ASObject
from guis.asObject import TipManager
from uiProxy import UIProxy
from data import item_data as ID
from data import first_item_source_data as FISD
from data import second_item_source_data as SISD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
ITEM_SLOT = 'typeSlot'
SLOT_STATE = 'slot%d'
ITEM_SOURCE_ICON_DIR = 'itemSource/%s.dds'
ITEM_SLOT_OFFESET_Y = 10
ITEM_SLOT_BEGIN_Y = 169
ITEM_SLOT_OFFESET_X = 65
ITEM_SLOT_BEGIN_X = 15
ITEM_SLOT_INIT_Y = 94
SUCCESS = 1
FAILED = 2
SPRITE_SEARCH_WITH_ITEM = 1
SPRITE_SEARCH_WITH_TYPE = 2
SPRITE_SEARCH_WITH_WORD = 3
RANK_PATH_TYPE = 1
RANK_FUBEN_TYPE = 2
RANK_TEAM_TYPE = 3
RANK_GUILD_TYPE = 4
RANK_FUBEN_TAB_IDX = 1
RANK_TEAM_TAB_IDX = 2
RANK_GUILD_TAB_IDX = 4
TIP_ITEM_TYPE = 1
INIT_BG_HEIGHT = 190
INIT_LINE_Y = 173

class ItemSourceInforProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ItemSourceInforProxy, self).__init__(uiAdapter)
        self.widget = None
        self.sourceTypeInfos = []
        self.itemTip = None
        self.isShow = False
        self.clickMap = {gametypes.CLICK_DEFAULT_SOURCE_TYPE: self.handleClickDefaultSprite,
         gametypes.CLICK_FUBEN_SOURCE_TYPE: self.handleClickFuben,
         gametypes.CLICK_AUCTION_SOURCE_TYPE: self.handleClickAuction,
         gametypes.CLICK_PATH_SOURCE_TYPE: self.handleClickPath,
         gametypes.CLICK_MALL_SOURCE_TYPE: self.handleClickMall,
         gametypes.CLICK_SPRITE_SOURCE_TYPE: self.handleClickSprite,
         gametypes.CLICK_MSG_SOURCE_TYPE: self.handleClickMsg,
         gametypes.CLICK_RANK_SOURCE_TYPE: self.handleClickRank,
         gametypes.CLICK_YUNCHUI_SHOP_SOURCE_TYPE: self.handleClickPrivateShop,
         gametypes.CLICK_RECOMMEND_SOURCE_TYPE: self.handleClickRecommend,
         gametypes.CLICK_LIFE_SKILL_SOURCE_TYPE: self.handleClickLifeSkill,
         gametypes.CLICK_RUNE_TO_ITEM_SOURCE_TYPE: self.handleClickRuneToItem}
        uiAdapter.registerEscFunc(uiConst.WIDGET_ITEM_SOURCE_INFOR, self.clearWidget)

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.typeLength = 0
        self.initUI()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ITEM_SOURCE_INFOR)
        self.widget = None
        self.sourceTypeInfos = []
        self.itemId = 0
        self.itemTip = None
        self.isShow = False

    def show(self, itemId):
        p = BigWorld.player()
        if not itemId:
            p.showGameMsg(GMDD.data.NO_ITEM_SOURCE_MSG, ())
            return
        self.itemTip = TipManager.getTargetTip()
        self.itemId = self.getItemId(itemId)
        self.initData()
        if not self.sourceTypeInfos:
            gameglobal.rds.ui.help.showByItemId(itemId)
            return
        self.isShow = True
        self.uiAdapter.loadWidget(uiConst.WIDGET_ITEM_SOURCE_INFOR)

    def getItemId(self, itemId):
        if not gameglobal.rds.configData.get('enableNewItemSearch', False):
            gameglobal.rds.ui.help.showByItemId(itemId)
            return
        while ID.data.get(itemId, {}).get('parentId', 0):
            if ID.data.get(itemId, {}).get('sourceIds', ()):
                break
            itemId = ID.data.get(itemId, {}).get('parentId', 0)

        return itemId

    def openPanel(self):
        currentTip = TipManager.getTargetTip()
        if currentTip and currentTip.tipType == 33:
            gameglobal.rds.ui.help.show(currentTip.cardName.textField.text)
            return
        p = BigWorld.player()
        if not self.isItemTip():
            return
        itemId = TipManager.getCurrentItemId()
        if self.isShow:
            if self.widget:
                self.refreshPanel(itemId)
            return
        if itemId:
            self.show(itemId)
        else:
            p.showGameMsg(GMDD.data.NO_ITEM_SOURCE_MSG, ())

    def isItemTip(self):
        tip = TipManager.getTargetTip()
        if not tip or hasattr(tip, 'tipType') and tip.tipType != TIP_ITEM_TYPE:
            return False
        return True

    def initTip(self):
        if self.itemTip:
            self.widget.tip.tipType = self.itemTip.tipType
            self.widget.tip.tipData = self.itemTip.tipData

    def initData(self):
        sourceIds = ID.data.get(self.itemId, {}).get('sourceIds', ())
        hasFunbenType = False
        for sourceId in sourceIds:
            sourceTypeInfo = {}
            firstSourceInfo = self.getFirstSourceInfo(sourceId)
            secondSourceInfo = SISD.data.get(sourceId, {})
            if firstSourceInfo['fistId'] == gametypes.ITEM_SOURCE_FUBEN:
                if hasFunbenType:
                    continue
                sourceTypeInfo['sourceName'] = firstSourceInfo.get('firstSourceName', '')
                hasFunbenType = True
            else:
                sourceTypeInfo['sourceName'] = secondSourceInfo.get('secondSourceName', '')
            secondClickType = secondSourceInfo.get('clickType', 0)
            sourceTypeInfo['clickType'] = secondClickType if secondClickType else firstSourceInfo.get('clickType', 0)
            secondTip = secondSourceInfo.get('tip', 0)
            sourceTypeInfo['tip'] = secondTip if secondTip else firstSourceInfo.get('tip', '')
            secondArgs = secondSourceInfo.get('args', ())
            sourceTypeInfo['args'] = secondArgs if secondArgs else firstSourceInfo.get('args', ())
            if not secondSourceInfo.get('icon', ''):
                sourceTypeInfo['icon'] = firstSourceInfo.get('icon', '')
            else:
                sourceTypeInfo['icon'] = secondSourceInfo.get('icon', '')
            sourceTypeInfo['firstType'] = firstSourceInfo.get('fistId', 0)
            self.sourceTypeInfos.append(sourceTypeInfo)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.itemInforPanel.closeBtn
        self.initTip()
        self._setItemTitle()
        self._switchPanel()
        self._fillTypeSlot()

    def refreshPanel(self, itemId):
        itemId = self.getItemId(itemId)
        p = BigWorld.player()
        sourceIds = ID.data.get(itemId, {}).get('sourceIds', ())
        if not itemId:
            p.showGameMsg(GMDD.data.NO_ITEM_SOURCE_MSG, ())
            return
        if not sourceIds:
            gameglobal.rds.ui.help.showByItemId(itemId)
            return
        self.itemTip = TipManager.getTargetTip()
        self.resetUI()
        self.itemId = itemId
        self.initData()
        self.initUI()

    def resetUI(self):
        self.clearSlot()
        self.resetSize()
        self.sourceTypeInfos = []

    def resetSize(self):
        self.widget.itemInforPanel.bgOut.height = INIT_BG_HEIGHT
        self.widget.itemInforPanel.baoShiDownLine.y = INIT_LINE_Y

    def clearSlot(self):
        length = len(self.sourceTypeInfos)
        for index in xrange(0, min(length, 4)):
            slot = self.widget.itemInforPanel.getChildByName(ITEM_SLOT + str(index))
            if not slot or not slot.icon.data:
                continue
            idx = int(slot.icon.data)
            clickType = self.sourceTypeInfos[idx].get('clickType', 0)
            slot.icon.removeEventListener(events.MOUSE_CLICK, self.clickMap.get(clickType, self.handleClickDefaultSprite))

        if length > 4:
            for index in xrange(4, length):
                slot = self.widget.itemInforPanel.getChildByName(ITEM_SLOT + str(index))
                if slot:
                    self.widget.itemInforPanel.removeChild(slot)

    def getFirstSourceInfo(self, secondId):
        firstSourceInfos = FISD.data
        firstSourceInfo = {}
        for firstId, info in firstSourceInfos.items():
            if secondId in info.get('secondSourceIds', ()):
                firstSourceInfo = copy.deepcopy(info)
                firstSourceInfo['fistId'] = firstId
                return firstSourceInfo

        return firstSourceInfo

    def _setItemTitle(self):
        qualityColor = itemToolTipUtils.getQualityColorById(self.itemId)
        self.widget.itemInforPanel.itemName.gotoAndStop(qualityColor)
        self.widget.itemInforPanel.bgOut.gotoAndStop(qualityColor)
        iconPath = uiUtils.getItemIconPath(self.itemId)
        self.widget.itemInforPanel.icon.icon.loadImage(iconPath)
        self.widget.itemInforPanel.itemName.txt.text = ID.data.get(self.itemId, {}).get('name', '')

    def _switchPanel(self):
        self.typeLength = len(self.sourceTypeInfos)
        if self.typeLength <= 3:
            self.widget.itemInforPanel.gotoAndStop(SLOT_STATE % self.typeLength)
        else:
            self.widget.itemInforPanel.gotoAndStop('slot4')

    def _fillTypeSlot(self):
        length = len(self.sourceTypeInfos)
        if length <= 4:
            for index, sourceInfo in enumerate(self.sourceTypeInfos):
                slot = self.widget.itemInforPanel.getChildByName(ITEM_SLOT + str(index))
                self.setSourceSlotData(slot, index)

        else:
            slotX = ITEM_SLOT_BEGIN_X
            slotY = ITEM_SLOT_BEGIN_Y
            preSlotY = ITEM_SLOT_BEGIN_Y
            for index in xrange(0, 4):
                slot = self.widget.itemInforPanel.getChildByName(ITEM_SLOT + str(index))
                self.setSourceSlotData(slot, index)

            for index in xrange(4, length):
                slot = self.widget.getInstByClsName('ItemSourceInfor_SourceType_Slot')
                slot.name = ITEM_SLOT + str(index)
                slot.x = slotX
                slot.y = slotY
                if index % 4 == 3:
                    slotX = ITEM_SLOT_BEGIN_X
                    preSlotY = slotY
                    slotY = slotY + slot.height + ITEM_SLOT_OFFESET_Y
                else:
                    slotX = slotX + ITEM_SLOT_OFFESET_X
                self.setSourceSlotData(slot, index)
                self.widget.itemInforPanel.addChild(slot)

            if length % 4:
                offset = slotY - ITEM_SLOT_INIT_Y
            else:
                offset = preSlotY - ITEM_SLOT_INIT_Y
            self.widget.itemInforPanel.bgOut.height = self.widget.itemInforPanel.bgOut.height + offset
            self.widget.itemInforPanel.baoShiDownLine.y = self.widget.itemInforPanel.baoShiDownLine.y + offset

    def setSourceSlotData(self, slot, idx):
        sourceInfo = self.sourceTypeInfos[idx]
        iconId = sourceInfo.get('icon', '')
        typeName = sourceInfo.get('sourceName', '')
        slot.fixedSize = True
        slot.icon.contentCanvas.fitSize = True
        slot.icon.contentCanvas.loadImage(ITEM_SOURCE_ICON_DIR % str(iconId))
        slot.typeName.text = typeName
        if sourceInfo.get('tip', ''):
            TipManager.addTip(slot.icon, sourceInfo['tip'])
        clickType = sourceInfo.get('clickType', 0)
        slot.icon.data = idx
        slot.icon.addEventListener(events.MOUSE_CLICK, self.clickMap.get(clickType, self.handleClickDefaultSprite))

    def handleClickRecommend(self, *args):
        self.closeQuestPanel()
        e = ASObject(args[3][0])
        target = e.currentTarget
        p = BigWorld.player()
        idx = int(target.data)
        sourceTypeInfo = self.sourceTypeInfos[idx]
        args = sourceTypeInfo['args']
        if args:
            tabIdx = args[0]
            page = uiConst.PLAY_RECOMM_TAB_DICT.get(tabIdx, 0)
            avaliable = True
            if page == uiConst.PLAY_RECOMM_DAILY_PANEL:
                if not gameglobal.rds.ui.playRecommActivation.showDailyPanel():
                    avaliable = False
            elif page == uiConst.PLAY_RECOMM_WEEK_PANEL:
                if not gameglobal.rds.ui.playRecommActivation.showWeekPanel():
                    avaliable = False
            elif page == uiConst.PLAY_RECOMM_LV_UP_PANEL:
                if not gameglobal.rds.ui.playRecommActivation.showLvUpPanel():
                    avaliable = False
            elif not gameglobal.rds.ui.playRecomm.showStrongerPanel():
                avaliable = False
            if avaliable:
                gameglobal.rds.ui.playRecomm.showInPage(page, 0)
            else:
                p.showGameMsg(GMDD.data.ITEM_SOURCE_NOT_AVALIABLE_LV, ())

    def handleClickRuneToItem(self, *args):
        self.uiAdapter.equipChange.show(uiConst.EQUIPCHANGE_TAB_RUNE, 3)

    def handleClickLifeSkill(self, *args):
        self.closeQuestPanel()
        e = ASObject(args[3][0])
        target = e.currentTarget
        idx = int(target.data)
        sourceTypeInfo = self.sourceTypeInfos[idx]
        args = sourceTypeInfo['args']
        if args:
            lifeTabId = args[0]
            if len(args) > 1:
                subTabs = args[1:]
                if lifeTabId == uiConst.LIFE_SKILL_MAKE_SKILL_TAB_IDX:
                    gameglobal.rds.ui.lifeSkillNew.openMakeSkillPanel(subTabs)
                else:
                    gameglobal.rds.ui.lifeSkillNew.openProduceSkillPanel(lifeTabId, subTabs)
            else:
                gameglobal.rds.ui.lifeSkillNew.show(lifeTabId)

    def handleClickMall(self, *args):
        self.closeQuestPanel()
        e = ASObject(args[3][0])
        target = e.currentTarget
        idx = int(target.data)
        sourceTypeInfo = self.sourceTypeInfos[idx]
        args = sourceTypeInfo['args']
        if args:
            gameglobal.rds.ui.tianyuMall.show(keyWord=args[0])
            return
        itemName = ID.data.get(self.itemId, {}).get('name', '')
        gameglobal.rds.ui.tianyuMall.show(keyWord=itemName)

    def handleClickRank(self, *args):
        self.closeQuestPanel()
        e = ASObject(args[3][0])
        target = e.currentTarget
        idx = int(target.data)
        sourceTypeInfo = self.sourceTypeInfos[idx]
        args = sourceTypeInfo['args']
        rankType = args[0]
        if rankType == RANK_PATH_TYPE:
            seekId = args[1]
            self.findPath(seekId)
        elif rankType == RANK_FUBEN_TYPE or rankType == RANK_TEAM_TYPE:
            fubenNo = 0
            if len(args) > 1:
                fubenNo = args[1]
            if rankType == RANK_FUBEN_TYPE:
                gameglobal.rds.ui.ranking.show(tabId=RANK_FUBEN_TAB_IDX, fbNo=fubenNo)
            else:
                gameglobal.rds.ui.ranking.showTeamRankPanel(rankTeamFbNo=fubenNo)
        elif rankType == RANK_GUILD_TYPE:
            guildActivity = 0
            if len(args) > 1:
                guildActivity = args[1]
            gameglobal.rds.ui.ranking.showGuildRankPanel(guildActivity=guildActivity)
        else:
            return

    def handleClickPrivateShop(self, *args):
        self.closeQuestPanel()
        e = ASObject(args[3][0])
        p = BigWorld.player()
        target = e.currentTarget
        idx = int(target.data)
        sourceTypeInfo = self.sourceTypeInfos[idx]
        args = sourceTypeInfo['args']
        if not args:
            return
        shopId = args[0]
        yunChuiShopId = SCD.data.get('privateCompositeShopId', 0)
        activityShopId = SCD.data.get('PRIVATE_SHOP_ID', 0)
        if shopId == yunChuiShopId:
            tabIdx = 0
            if len(args) > 1:
                tabIdx = args[1]
            yunChuiShopProxy = gameglobal.rds.ui.yunChuiShop
            yunChuiShopProxy.initTabIdx = tabIdx
            gameglobal.rds.ui.inventory.openYunChuiShop()
        elif shopId == activityShopId:
            p.getCurrPrivateShop()
        else:
            p.showGameMsg(GMDD.data.PRIVATE_SHOP_ID_ERROR, ())

    def handleClickMsg(self, *args):
        p = BigWorld.player()
        e = ASObject(args[3][0])
        target = e.currentTarget
        idx = int(target.data)
        sourceTypeInfo = self.sourceTypeInfos[idx]
        args = sourceTypeInfo['args']
        p.showGameMsg(args[0], ())

    def handleClickFuben(self, *args):
        fubenItems = []
        sourceIds = ID.data.get(self.itemId, {}).get('sourceIds', ())
        for sourceId in sourceIds:
            firstSourceInfo = self.getFirstSourceInfo(sourceId)
            secondSourceInfo = SISD.data.get(sourceId, {})
            if firstSourceInfo['fistId'] == gametypes.ITEM_SOURCE_FUBEN and secondSourceInfo.get('args', ()):
                fubenItem = {}
                fubenItem['fubenName'] = secondSourceInfo['secondSourceName']
                fubenItem['fubenArgs'] = secondSourceInfo.get('args', ())
                fubenItems.append(fubenItem)

        gameglobal.rds.ui.fubenSource.show(self.itemId, fubenItems)

    def handleClickSprite(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        idx = int(target.data)
        sourceTypeInfo = self.sourceTypeInfos[idx]
        args = sourceTypeInfo['args']
        if not args:
            gameglobal.rds.ui.help.show(sourceTypeInfo['sourceName'])
            return
        if args[0] == SPRITE_SEARCH_WITH_ITEM:
            gameglobal.rds.ui.help.showByItemId(self.itemId)
        elif args[0] == SPRITE_SEARCH_WITH_TYPE:
            gameglobal.rds.ui.help.show(sourceTypeInfo['sourceName'])
        elif args[0] == SPRITE_SEARCH_WITH_WORD:
            gameglobal.rds.ui.help.show(args[1])
        else:
            return

    def handleClickDefaultSprite(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        idx = int(target.data)
        sourceTypeInfo = self.sourceTypeInfos[idx]
        gameglobal.rds.ui.help.showByItemId(sourceTypeInfo['sourceName'])

    def handleClickAuction(self, *args):
        self.closeQuestPanel()
        itemName = ID.data.get(self.itemId, {}).get('name', '')
        if gameglobal.rds.configData.get('enableTabAuction', False):
            gameglobal.rds.ui.tabAuctionConsign.show(searchItemName=itemName)
        else:
            gameglobal.rds.ui.consign.show(searchItemName=itemName)

    def handleClickPath(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        idx = int(target.data)
        sourceTypeInfo = self.sourceTypeInfos[idx]
        seekId = sourceTypeInfo['args'][0]
        self.findPath(seekId)

    def closeQuestPanel(self):
        if gameglobal.rds.ui.quest.isShow or gameglobal.rds.ui.npcV2.isShow:
            gameglobal.rds.ui.funcNpc.closeByInv()

    def findPath(self, seekId):
        realSeekId = 0
        if type(seekId) == int or type(seekId) == str:
            realSeekId = int(seekId)
        elif type(seekId) == tuple:
            realSeekId = uiUtils.findTrackId(seekId)
        uiUtils.findPosById(realSeekId)
