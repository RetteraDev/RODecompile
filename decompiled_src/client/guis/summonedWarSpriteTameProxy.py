#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/summonedWarSpriteTameProxy.o
import BigWorld
import uiConst
import events
import utils
import const
import tipUtils
import gameglobal
from uiProxy import UIProxy
from gameStrings import gameStrings
from asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
from data import summon_sprite_familiar_data as SSFD
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'

class SummonedWarSpriteTameProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteTameProxy, self).__init__(uiAdapter)
        self.widget = None
        self.selSpriteIndex = 0
        self.selSpriteNumber = 0
        self.spriteItemList = []
        self.currSelectItem = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_TAME, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_TAME:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_TAME)

    def reset(self):
        self.selSpriteIndex = 0
        self.selSpriteNumber = 0
        self.spriteItemList = []
        self.currSelectItem = None

    def show(self):
        if not gameglobal.rds.configData.get('enableTrainingSprite', False):
            return
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_TAME)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.help.helpKey = SCD.data.get('spriteTrainHelpKey', 0)
        self.widget.spriteList.itemRenderer = 'SummonedWarSpriteTame_LeftItem'
        self.widget.spriteList.itemHeight = 65
        self.widget.spriteList.dataArray = []
        self.widget.spriteList.labelFunction = self.itemFunction
        self.widget.typeDropdown.addEventListener(events.INDEX_CHANGE, self.handleSelectWarSpriteType, False, 0, True)
        self.typeToSort = SCD.data.get('spriteMajorAbility', [])
        typeList = []
        for i, vlaue in enumerate(self.typeToSort):
            typeInfo = {}
            typeInfo['label'] = vlaue
            typeInfo['typeIndex'] = i
            typeList.append(typeInfo)

        ASUtils.setDropdownMenuData(self.widget.typeDropdown, typeList)
        self.widget.typeDropdown.menuRowCount = min(len(typeList), 5)
        if self.widget.typeDropdown.selectedIndex == -1:
            self.widget.typeDropdown.selectedIndex = 0

    def refreshInfo(self):
        if not self.widget:
            return
        self.updateWarSpritesTypeList(self.widget.typeDropdown.selectedIndex)

    def _onBeginBtnClick(self, e):
        if not self.selSpriteIndex:
            return
        p = BigWorld.player()
        p.base.trainSprite(self.selSpriteIndex)
        totalTrainedCntDay = p.spriteExtraDict['totalTrainedCntDay']
        spriteInfo = p.summonSpriteList[self.selSpriteIndex]
        trainedCntDay = spriteInfo.get('trainedCntDay', 0)
        sLv = spriteInfo.get('props', {}).get('lv', 0)
        totalLimitDay, singleListDay = utils.getSpriteTrainLimit(p.lv, sLv)
        if totalTrainedCntDay >= totalLimitDay or trainedCntDay >= singleListDay:
            return
        self.hide()

    def handleSelectWarSpriteType(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.selectedIndex != -1:
            self.updateWarSpritesTypeList(itemMc.selectedIndex)

    def sortWarSpriteList(self, typeIndex):
        p = BigWorld.player()
        if typeIndex == 0:
            sortList = sorted(p.summonSpriteList.values(), key=lambda d: d['props']['lv'], reverse=True)
        else:
            sortList = sorted(p.summonSpriteList.values(), key=lambda d: d['props']['vPropCache'][typeIndex - 1], reverse=True)
        tameFinList = []
        noTameFinList = []
        for spriteInfo in sortList:
            sLv = spriteInfo.get('props', {}).get('lv', 0)
            totalLimitDay, singleListDay = utils.getSpriteTrainLimit(p.lv, sLv)
            if spriteInfo['trainedCntDay'] == singleListDay:
                tameFinList.append(spriteInfo)
            else:
                noTameFinList.append(spriteInfo)

        return noTameFinList + tameFinList

    def updateWarSpritesTypeList(self, typeIndex):
        p = BigWorld.player()
        warSpriteList = self.sortWarSpriteList(typeIndex)
        self.spriteItemList = []
        for i in xrange(len(warSpriteList)):
            spriteInfo = warSpriteList[i]
            spriteIndex = spriteInfo.get('index', -1)
            spriteId = spriteInfo.get('spriteId', 0)
            name = spriteInfo.get('name', '')
            sLv = spriteInfo.get('props', {}).get('lv', 0)
            totalLimitDay, singleListDay = utils.getSpriteTrainLimit(p.lv, sLv)
            trainedCntDay = p.summonSpriteList[spriteIndex]['trainedCntDay']
            isShowIcon = True if trainedCntDay >= singleListDay else False
            itemInfo = {}
            itemInfo['numberId'] = i
            itemInfo['spriteIndex'] = spriteIndex
            itemInfo['spriteId'] = spriteId
            itemInfo['name'] = name
            itemInfo['lv'] = sLv
            itemInfo['trainedCntDay'] = trainedCntDay
            itemInfo['isShowIcon'] = isShowIcon
            self.spriteItemList.append(itemInfo)

        self.widget.spriteList.dataArray = self.spriteItemList
        self.widget.spriteList.validateNow()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.numberId = itemData.numberId
        itemMc.spriteIndex = itemData.spriteIndex
        itemMc.addEventListener(events.MOUSE_DOWN, self.handleSelSpriteClick, False, 0, True)
        szName = itemData.name
        szLv = 'lv %d' % itemData.lv
        itemMc.labels = [szName, szLv]
        iconId = SSID.data.get(itemData.spriteId, {}).get('spriteIcon', '000')
        iconPath = SPRITE_ICON_PATH % str(iconId)
        itemMc.iconPath = iconPath
        itemMc.itemSlot.slot.fitSize = True
        itemMc.itemSlot.slot.dragable = False
        itemMc.itemSlot.slot.setItemSlotData({'iconPath': iconPath})
        itemMc.countIcon.visible = itemData.isShowIcon
        itemMc.selected = False
        if self.selSpriteIndex == itemData.spriteIndex:
            itemMc.selected = True
        elif not self.selSpriteIndex and itemData.numberId == 0:
            itemMc.selected = True
        if itemMc.selected:
            self.currSelectItem = itemMc
            self.selSpriteNumber = itemData.numberId
            self.selSpriteIndex = itemData.spriteIndex
            self.updateSelSprite()

    def handleSelSpriteClick(self, *args):
        target = ASObject(args[3][0]).currentTarget
        if self.currSelectItem:
            self.currSelectItem.selected = False
        target.selected = True
        self.currSelectItem = target
        self.selSpriteNumber = target.numberId
        self.selSpriteIndex = target.spriteIndex
        self.updateSelSprite()

    def updateSelSprite(self):
        itemInfo = self.spriteItemList[self.selSpriteNumber]
        if not itemInfo:
            return
        sLv = itemInfo.get('lv', 0)
        spriteId = itemInfo.get('spriteId')
        iconPath = SPRITE_ICON_PATH % str(SSID.data.get(spriteId, {}).get('spriteIcon', '000'))
        trainedCntDay = itemInfo.get('trainedCntDay', 0)
        isShowIcon = itemInfo.get('isShowIcon', False)
        p = BigWorld.player()
        totalLimitDay, singleListDay = utils.getSpriteTrainLimit(p.lv, sLv)
        totalTrainedCntDay = p.spriteExtraDict['totalTrainedCntDay']
        self.widget.desc0.text = gameStrings.SPRITE_TAME_TODAY_LEFT_TIMES % max(totalLimitDay - totalTrainedCntDay, 0)
        self.widget.spriteSlot.slot.fitSize = True
        self.widget.spriteSlot.slot.dragable = False
        self.widget.spriteSlot.slot.setItemSlotData({'iconPath': iconPath})
        self.widget.desc2.visible = isShowIcon
        moneyCost, timeCost = utils.getSpriteTrainCost(p.lv, sLv)
        self.widget.consumeMc.visible = not isShowIcon
        self.widget.consumeMc.icon.bonusType = 'bindCash'
        self.widget.consumeMc.bindCash.text = moneyCost
        self.widget.consumeMc.desc.text = gameStrings.SPRITE_TAME_SINGLE_LEFT_TIMES % trainedCntDay
        hours = '%.1f' % (timeCost * 1.0 / const.TIME_INTERVAL_HOUR)
        cueMsg = SCD.data.get('spriteTrainDesc', '%s%d%d')
        self.widget.desc1.text = cueMsg % (hours, totalLimitDay, singleListDay)
        self.widget.icon.bonusType = 'bindCash'
        self.widget.bindCash.text = p.bindCash
        self.updateFamiBar()
        self.updateExpBar()

    def updateFamiBar(self):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList[self.selSpriteIndex]
        props = spriteInfo.get('props', {})
        slv = props.get('lv', 0)
        famiBar = self.widget.famiBar
        famiText = famiBar.valueText
        curValue = int(props.get('famiExp', 0))
        maxValue = int(props.get('famiMaxExp', 1))
        familiar = int(props.get('familiar', 0))
        famiAdd = int(props.get('famiEffAdd', 0))
        famiEffLv = int(props.get('famiEffLv', 0))
        expReward, famiReward = utils.getSpriteTrainReward(p.lv, slv)
        famiBar.maxValue = maxValue
        famiBar.currentValues = [curValue, curValue + famiReward]
        self.widget.famiValT.text = familiar
        famiText.text = '+%d' % famiReward
        if famiEffLv < const.MAX_SKILL_LV_SPRITE_FAMILIAR:
            self.widget.famiIcon.gotoAndStop('fami1')
        elif famiEffLv >= const.MAX_SKILL_LV_SPRITE_FAMILIAR:
            self.widget.famiIcon.gotoAndStop('fami3')
        tip = SCD.data.get('spriteFamiTip', '%s, %s, %s') % (famiEffLv, familiar, famiAdd) + SSFD.data.get(famiEffLv, {}).get('tipDesc', '')
        TipManager.addTip(self.widget.famiIcon, tip, tipUtils.TYPE_DEFAULT_BLACK)

    def updateExpBar(self):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList[self.selSpriteIndex]
        props = spriteInfo.get('props', {})
        slv = props.get('lv', 0)
        expBar = self.widget.expBar
        expText = expBar.valueText
        curValue = int(props.get('exp', 0))
        maxValue = int(props.get('maxExp', 1))
        expLv = props.get('lv', 0)
        expReward, famiReward = utils.getSpriteTrainReward(p.lv, slv)
        expBar.maxValue = maxValue
        expBar.currentValues = [curValue, curValue + expReward]
        self.widget.expValT.text = expLv
        expText.text = '+%d' % expReward
        TipManager.addTip(self.widget.lvIcon, SCD.data.get('spriteLvTip'), tipUtils.TYPE_DEFAULT_BLACK)
