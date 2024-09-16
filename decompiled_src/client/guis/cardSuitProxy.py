#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cardSuitProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import const
import events
import gameglobal
import uiConst
import uiUtils
from asObject import ASUtils
from asObject import ASObject
from asObject import TipManager
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import sys_config_data as SCD
from cdata import pskill_template_data as PTD
from cdata import pskill_data as PDD
from data import card_suit_data as CSD
from data import card_equip_type_data as CETD
DROP_DOWN_ROW_MAX = 5
ICON_WIDTH = 30
EFFECT_MAX_NUM = 6
PROP_ITEM_HEIGHT = 23
PROP_MENU_OFFSETX_1 = 321
PROP_MENU_OFFSETX_2 = 176

class CardSuitProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CardSuitProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CARD_SUIT, self.hide)

    def reset(self):
        self.eMenuData = []
        self.numMenuData = []
        self.propMenuData = []
        self.allSuitData = {}
        self.selectedSId = None
        self.selectedItem = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CARD_SUIT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.reset()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CARD_SUIT)

    @property
    def tempId(self):
        return self.uiAdapter.cardSystem.tempId

    @property
    def cardBag(self):
        p = BigWorld.player()
        cardBag = p.allCardBags.get(self.tempId, {})
        return cardBag

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CARD_SUIT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initData()
        self.setMenu()
        self.setNumMenu()
        self.setPropMenu()
        self.widget.leftList.column = 2
        self.widget.leftList.itemHeight = 93
        self.widget.leftList.itemWidth = 172
        self.widget.leftList.itemRenderer = 'CardSuit_LeftListItem'
        self.widget.leftList.labelFunction = self.leftListFunction
        self.widget.leftList.dataArray = []
        self.setLeftList()
        self.widget.rightList.itemWidth = 200
        self.widget.rightList.itemRenderer = 'CardSuit_PropItem'
        self.widget.rightList.labelFunction = self.rightListFunction
        self.widget.rightList.itemHeightFunction = self.rightItemHeightFunction
        self.widget.rightList.dataArray = []
        self.setRightList()

    def initData(self):
        self.allSuitData = {}
        for (sId, rank), v in CSD.data.iteritems():
            self.allSuitData.setdefault(sId, {})
            self.allSuitData[sId][rank] = v

    def getAllSuitData(self):
        return self.uiAdapter.cardSystem.getAllSuitData()

    def setLeftList(self):
        if not self.hasBaseData():
            return
        dataList = self.getLeftListData()
        self.widget.leftList.dataArray = dataList
        self.widget.leftList.validateNow()
        if not self.selectedSId and dataList:
            self.setSelectedItem(self.widget.leftList.items[0])

    def getLeftListData(self):
        lData = []
        eType, numType, propType = self.getMenuData()
        for k, v in self.allSuitData.iteritems():
            compose = v[0].get('compose', [])
            if eType and eType not in compose:
                continue
            if propType and propType != v[0].get('propType', 1):
                continue
            if numType and len(compose) != numType:
                continue
            lData.append(k)

        lData.sort(cmp=self.dirtSortByShowPriorityFunc)
        return lData

    def dirtSortByShowPriorityFunc(self, sId1, sId2):
        sId1ShowPriority = self.allSuitData.get(sId1, {}).get(0, {}).get('showPriority', 0)
        sId2ShowPriority = self.allSuitData.get(sId2, {}).get(0, {}).get('showPriority', 0)
        if sId1ShowPriority < sId2ShowPriority:
            return -1
        elif sId1ShowPriority > sId2ShowPriority:
            return 1
        elif sId1 < sId2:
            return -1
        else:
            return 1

    def leftListFunction(self, *arg):
        sId = int(arg[3][0].GetNumber())
        itemMc = ASObject(arg[3][1])
        if itemMc and sId:
            p = BigWorld.player()
            itemMc.sId = sId
            itemMc.canActiveIcon.visible = False
            if gameglobal.rds.configData.get('enableChangeCardSuit', 0):
                suitMenuData = self.uiAdapter.cardSystem.getCurSuitMenuData()
                for sData in suitMenuData:
                    suitId = sData.get('suitId', {})
                    if suitId == sId:
                        itemMc.canActiveIcon.visible = True
                        TipManager.addTip(itemMc.canActiveIcon, gameStrings.CARD_SUIT_CAN_ACTIVE)

            suitData = self.allSuitData.get(sId, {})
            compose = suitData.get(0, {}).get('compose', ())
            cardEquipTypeDict = SCD.data.get('cardEquipTypeDict', {})
            nameStr = suitData.get(0, {}).get('composeName', '')
            quality = suitData.get(0, {}).get('quality', 1)
            self.widget.removeAllInst(itemMc.iconCanvas)
            sType = self.uiAdapter.cardSlot.getCurSlotType()
            equipNum = self.uiAdapter.cardSystem.getEquipNum(sType)
            for i, eType in enumerate(compose):
                lItem = self.widget.getInstByClsName('CardSuit_IconItem')
                lItem.gotoAndStop('disable')
                equipSlot = self.cardBag.get('equipSlot', 0)
                slotNum = self.cardBag.get('slotNum', {}).get(sType, 0)
                for j in xrange(0, slotNum):
                    slotId = sType * const.CARD_SLOT_DIV_NUM + j + 1
                    slotCardId = self.cardBag.get('cardSlots', {}).get(slotId, 0)
                    cardObj = p.getCard(slotCardId, tempId=self.tempId)
                    if cardObj:
                        if eType == cardObj.equipType:
                            if gameglobal.rds.configData.get('enableChangeCardSuit', 0):
                                if equipNum <= len(compose):
                                    lItem.gotoAndStop('up')
                            else:
                                lItem.gotoAndStop('up')

                lItem.icon.fitSize = True
                iconId = CETD.data.get(eType, {}).get('icon', 'notFound')
                lItem.icon.loadImage(''.join(('card/cardtype/', str(iconId), '.dds')))
                TipManager.addTip(lItem, cardEquipTypeDict.get(eType, ''))
                halfNum = len(compose) / 2.0
                lItem.x = ICON_WIDTH * i - ICON_WIDTH * halfNum
                itemMc.iconCanvas.addChild(lItem)

            itemMc.titleMc.gotoAndStop('type' + str(quality))
            itemMc.titleMc.titleName.text = nameStr
            isSel = sId == self.selectedSId
            itemMc.selectedMc.visible = isSel
            if isSel:
                self.selectedSlotItem = itemMc
            itemMc.addEventListener(events.MOUSE_CLICK, self.handleSuitItemClick, False, 0, True)

    def handleSuitItemClick(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.currentTarget
        self.setSelectedItem(t)

    def setRightList(self):
        if not self.hasBaseData():
            return
        dataList = self.getRightListData()
        self.widget.rightList.dataArray = dataList
        self.widget.rightList.validateNow()

    def getRightListData(self):
        p = BigWorld.player()
        suitData = self.allSuitData.get(self.selectedSId, {})
        rData = []
        equipSlot = self.cardBag.get('equipSlot', 0)
        suitInfo = self.uiAdapter.cardSlot.getPskillEffects(equipSlot)
        school = self.cardBag.get('school', 0)
        for rank, data in suitData.iteritems():
            isHighlight = (self.selectedSId, rank) in suitInfo
            name = data.get('name', '')
            propText = name
            if isHighlight:
                propText = uiUtils.toHtml(propText, uiConst.CARD_PROP_HIGHLIGHT_COLOR)
            info = {'label': propText,
             'rank': rank,
             'iconType': 0}
            rData.append(info)
            suitEffect = data.get('effect', [])
            for effectDict in suitEffect:
                effect = effectDict.get(school, None)
                if not effect:
                    effect = effectDict.get(0, None)
                if effect:
                    eId, eLv = effect
                    sname = PDD.data.get(effect, {}).get('desc', '')
                    propText = sname
                    if isHighlight:
                        propText = uiUtils.toHtml(propText, uiConst.CARD_PROP_HIGHLIGHT_COLOR)
                    info = {'label': propText,
                     'rank': rank,
                     'iconType': 1}
                    rData.append(info)

            info = {'label': '  ',
             'rank': 0,
             'iconType': 0}
            rData.append(info)

        return rData

    def rightListFunction(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and info:
            itemMc.contentTxt.htmlText = info.label
            itemMc.normalIcon.visible = info.iconType

    def rightItemHeightFunction(self, *arg):
        info = ASObject(arg[3][0])
        if info:
            item = self.widget.getInstByClsName('CardSuit_PropItem')
            item.contentTxt.htmlText = info.label
            height = max(PROP_ITEM_HEIGHT, item.contentTxt.textHeight)
            return GfxValue(height)

    def refreshInfo(self):
        if not self.widget:
            return

    def setMenu(self):
        eMenu = getattr(self.widget, 'equipTypeMenu', None)
        if eMenu:
            if gameglobal.rds.configData.get('enableChangeCardSuit', 0):
                eMenu.x = PROP_MENU_OFFSETX_1
            else:
                eMenu.x = PROP_MENU_OFFSETX_2
            cardEquipTypeDict = SCD.data.get('cardEquipTypeDict', {1: gameStrings.TEXT_CARDSUITPROXY_335,
             2: gameStrings.TEXT_CARDSUITPROXY_335_1,
             3: gameStrings.TEXT_CARDSUITPROXY_335_2})
            eMenuData = []
            info = {'label': gameStrings.CARD_SYSTEM_ALL,
             'data': 0}
            eMenuData.append(info)
            for equipType, name in cardEquipTypeDict.iteritems():
                info = {'label': name,
                 'data': equipType}
                cardEquipTypeShow = SCD.data.get('cardEquipTypeShow', ())
                if equipType in cardEquipTypeShow:
                    eMenuData.append(info)

            eMenuData.sort(key=lambda x: x['data'])
            self.eMenuData = eMenuData
            ASUtils.setDropdownMenuData(eMenu, eMenuData)
            eMenu.selectedIndex = 0
            eMenu.menuRowCount = min(len(eMenuData), DROP_DOWN_ROW_MAX)
            eMenu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleEquipTypeMenuItemSelected, False, 0, True)

    def setNumMenu(self):
        numMenuMc = getattr(self.widget, 'numMenu', None)
        if not numMenuMc:
            return
        else:
            numMenuMc.visible = gameglobal.rds.configData.get('enableChangeCardSuit', 0)
            self.numMenuData = [{'label': gameStrings.CARD_SUIT_NUM_TYPE,
              'data': 0}]
            for typeData, typeName in gameStrings.CARD_SUIT_NUM_TYPE_DESC.items():
                self.numMenuData.append({'label': typeName,
                 'data': typeData})

            self.numMenuData.sort(key=lambda x: x['data'])
            ASUtils.setDropdownMenuData(numMenuMc, self.numMenuData)
            numMenuMc.selectedIndex = 0
            numMenuMc.menuRowCount = min(len(self.numMenuData), DROP_DOWN_ROW_MAX)
            numMenuMc.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleNumMenuItemSelected, False, 0, True)
            return

    def setPropMenu(self):
        propMenuMC = getattr(self.widget, 'propMenu', None)
        if not propMenuMC:
            return
        else:
            self.propMenuData = [{'label': gameStrings.CARD_SYSTEM_ALL_ORGANIZATION,
              'data': 0}]
            for typeData, typeName in gameStrings.CARD_SYSTEM_PROP_TYPE_DESC.items():
                self.propMenuData.append({'label': typeName,
                 'data': typeData})

            self.propMenuData.sort(key=lambda x: x['data'])
            ASUtils.setDropdownMenuData(propMenuMC, self.propMenuData)
            propMenuMC.selectedIndex = 0
            propMenuMC.menuRowCount = min(len(self.propMenuData), DROP_DOWN_ROW_MAX)
            propMenuMC.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handlePropMenuItemSelected, False, 0, True)
            return

    def getMenuData(self):
        eType = 0
        eMenu = getattr(self.widget, 'equipTypeMenu')
        if eMenu and self.eMenuData:
            eType = self.eMenuData[eMenu.selectedIndex].get('data', '')
        nType = 0
        nMenu = getattr(self.widget, 'numMenu')
        if nMenu and self.numMenuData:
            nType = self.numMenuData[nMenu.selectedIndex].get('data', '')
        propType = 0
        propMenuMC = getattr(self.widget, 'propMenu', None)
        if propMenuMC and self.propMenuData:
            propType = self.propMenuData[propMenuMC.selectedIndex].get('data', 0)
        return (eType, nType, propType)

    def handleNumMenuItemSelected(self, *args):
        if not self.hasBaseData():
            return
        else:
            self.selectedSId = None
            self.setLeftList()
            self.setRightList()
            return

    def handlePropMenuItemSelected(self, *args):
        if not self.hasBaseData():
            return
        else:
            self.selectedSId = None
            self.setLeftList()
            self.setRightList()
            return

    def handleEquipTypeMenuItemSelected(self, *arg):
        if not self.hasBaseData():
            return
        else:
            self.selectedSId = None
            self.setLeftList()
            self.setRightList()
            return

    def setSelectedItem(self, leftItem):
        if not leftItem:
            return
        if self.selectedItem and self.selectedSId and self.selectedItem.sId == self.selectedSId:
            self.selectedItem.selectedMc.visible = False
        self.selectedSId = leftItem.sId
        self.selectedItem = leftItem
        if self.selectedItem:
            self.selectedItem.selectedMc.visible = True
        self.setRightList()

    def hasBaseData(self):
        if not self.widget:
            return False
        return True

    def _onPreviewBtnClick(self, e):
        if not self.hasBaseData():
            return
        compose = CSD.data.get((self.selectedSId, 0), {}).get('compose', ())
        self.uiAdapter.cardSlot.setPreviewIcon(compose)
