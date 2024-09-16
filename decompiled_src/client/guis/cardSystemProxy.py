#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cardSystemProxy.o
import BigWorld
import math
import gameglobal
import gametypes
import const
import events
import utils
import gamelog
import uiConst
import gameconfigCommon
from card import Card
from uiTabProxy import UITabProxy
from asObject import ASUtils
from asObject import ASObject
from asObject import TipManager
from guis import uiUtils
from guis import tipUtils
from guis import ui
from callbackHelper import Functor
from gamestrings import gameStrings
from cdata import pskill_template_data as PTD
from data import prop_data as PD
from data import prop_ref_data as PRD
from data import base_card_data as BCD
from data import conditional_prop_data as CPD
from data import advance_card_data as ACD
from data import card_atlas_data as CAD
from data import card_suit_data as CSD
from data import skill_tips_desc_data as STDD
from data import consumable_item_data as CID
from data import sys_config_data as SCD
from data import card_wash_group_data as CWGD
from cdata import card_to_item as CTI
from cdata import pskill_data as PDD
from cdata import game_msg_def_data as GMDD
TAB_INDEX_CARD_COLLECTION = 0
TAB_INDEX_CARD_MAKE = 1
TAB_INDEX_CARD_SLOT = 2
TAB_INDEX_CARD_CHANGE = 3
TAB_INDEX_SET = (TAB_INDEX_CARD_COLLECTION,
 TAB_INDEX_CARD_MAKE,
 TAB_INDEX_CARD_SLOT,
 TAB_INDEX_CARD_CHANGE)
TEMP_ICON = 'summonedSprite/icon/1014.dds'
MAX_FREE_CARD_COUNT = 200
VER_TYPE_ALL = 0
STAR_LEVEL_MAX = 4
MOON_LEVEL_MAX = 8
PER_LEVEL_NUM = 4
DROP_DOWN_ROW_MAX = 5
PASSIVE_SKILL_COLOR = '#e59545'
PASSIVE_SKILL_GRAY_COLOR = '#676767'
VALID_TIME_COLOR = '#e53900'
PASSIVE_SKILL_LV_PHASE = 3
CARD_SCENE_TYPE_DESC = {1: 'cardSceneTypeNuLinDesc',
 2: 'cardSceneTypeDiSheDesc'}

class CardSystemProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(CardSystemProxy, self).__init__(uiAdapter)
        uiAdapter.registerEscFunc(uiConst.WIDGET_CARD_SYSTEM, self.hide)
        self.init()

    def init(self):
        self.cardItemClassNameDic = {TAB_INDEX_CARD_COLLECTION: ['CardCollection_NormalCardItem', 'CardCollection_GoldCardItem'],
         TAB_INDEX_CARD_SLOT: ['CardSlot_NormalCardItem', 'CardSlot_GoldCardItem'],
         TAB_INDEX_CARD_MAKE: ['CardCollection_NormalCardItem', 'CardCollection_GoldCardItem'],
         TAB_INDEX_CARD_CHANGE: ['CardCollection_NormalCardItem', 'CardCollection_GoldCardItem']}
        self.typeIconArray = ['lan',
         'lan',
         'zi',
         'cheng']
        self.allCardData = []
        self.allSuitData = {}
        self.suitComposeData = {}
        self.propMenuData = [{'label': gameStrings.CARD_SYSTEM_ALL_ORGANIZATION,
          'data': 0}]
        self.versionMenuData = [{'label': gameStrings.CARD_SYSTEM_ALL_COLLECTION,
          'data': 0}]
        self.typeMenuData = [{'label': gameStrings.CARD_SYSTEM_ALL_TYPE,
          'data': 0}]
        self.versionAtlasData = {}
        self.cardTypeColorList = ['white',
         'blue_2',
         'purple_3',
         'golden_4']
        self.tabIndexList = [TAB_INDEX_CARD_COLLECTION,
         TAB_INDEX_CARD_MAKE,
         TAB_INDEX_CARD_SLOT,
         TAB_INDEX_CARD_CHANGE]
        self.propertyColor = '#73d0ff'
        self.hasLoadAllCard = {}
        self.reset()

    def setTemplateTab(self):
        p = BigWorld.player()
        if p.isUsingTemp() and not p.inBalanceTemplateWhiteList():
            self.widget.cardMakeBtn.enabled = False
            self.widget.cardChangeBtn.enabled = False

    def reset(self):
        super(CardSystemProxy, self).reset()
        self.selectedCardId = None
        self.selectedCardItem = None
        self.scrollToCard = 0
        self.cacheCardListArg = ()
        self.eTypeFilters = []
        self.washNumFilters = []
        self.tempId = 0
        self.curVerMenuData = {}
        self.curVerMenuIdx = 0

    @property
    def cardBag(self):
        p = BigWorld.player()
        cardBag = p.allCardBags.get(self.tempId, {})
        return cardBag

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CARD_SYSTEM:
            self.widget = widget
            self.initUI()
            self.setTemplateTab()

    def clearWidget(self):
        super(CardSystemProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CARD_SYSTEM)

    def clearAll(self):
        self.hide()
        self.init()

    def _getTabList(self):
        return [{'tabIdx': TAB_INDEX_CARD_COLLECTION,
          'tabName': 'cardCollectionBtn',
          'view': 'CardCollectionWidget',
          'proxy': 'cardCollection'},
         {'tabIdx': TAB_INDEX_CARD_MAKE,
          'tabName': 'cardMakeBtn',
          'view': 'CardMakeWidget',
          'proxy': 'cardMake'},
         {'tabIdx': TAB_INDEX_CARD_SLOT,
          'tabName': 'cardSlotBtn',
          'view': 'CardSlotWidget',
          'proxy': 'cardSlot'},
         {'tabIdx': TAB_INDEX_CARD_CHANGE,
          'tabName': 'cardChangeBtn',
          'view': 'CardChangeWidget',
          'proxy': 'cardChange'}]

    def checkCanOpenCardSystem(self, tabIndex):
        if not gameglobal.rds.configData.get('enableCardSys', False):
            return False
        p = BigWorld.player()
        if not p.isBaseCardSysOpen():
            p.showGameMsg(GMDD.data.CARD_NOT_OPEN_LEVEL, (SCD.data.get('cardBaseFuncOpenLevel', 0),))
            return False
        if tabIndex in (TAB_INDEX_CARD_SLOT, TAB_INDEX_CARD_CHANGE):
            valid, errorGMDD = self.checkTabFunctionVaild(tabIndex)
            p = BigWorld.player()
            if not valid:
                p.showGameMsg(errorGMDD, ())
                return False
        return True

    def show(self, tabIndex = TAB_INDEX_CARD_COLLECTION, selectedCardId = 0, scrollToCard = 0, tempId = 0, vMenuSelectedIdx = 0, isSpecialChangeForChangeTab = False):
        tabIndex = tabIndex if tabIndex in self.tabIndexList else TAB_INDEX_CARD_COLLECTION
        self.showTabIndex = tabIndex
        if not self.checkCanOpenCardSystem(tabIndex):
            return
        if not self.widget:
            self.tempId = tempId
        self.uiAdapter.cardChange.isSpecialChange = isSpecialChangeForChangeTab
        self.loadAllCard()
        self.initAllSuitData()
        self.curVerMenuIdx = vMenuSelectedIdx
        if not scrollToCard:
            scrollToCard = selectedCardId
        self.selectedCardId = selectedCardId
        self.scrollToCard = scrollToCard
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CARD_SYSTEM)
        elif self.currentTabIndex != self.showTabIndex:
            ASUtils.DispatchButtonEvent(self.widget.tabButtons[self.showTabIndex])
        else:
            if scrollToCard:
                self.scrollToCardFunc(scrollToCard)
            if selectedCardId:
                self.setSelectedItemByCardId(selectedCardId)
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        p = BigWorld.player()
        self.initTabUI()
        if self.uiAdapter.cardChange.isSpecialChange or self.tempId:
            self.setTabBtnsVisible(False)
        self.refreshTabTips()
        self.widget.setTabIndex(self.showTabIndex)
        self.showTabIndex = -1

    def refreshInfo(self):
        if not self.widget:
            return
        currentProxy = self.getCurrentProxy()
        if currentProxy:
            currentProxy.refreshInfo()

    def refreshTabTips(self):
        for tabIndex in (TAB_INDEX_CARD_SLOT, TAB_INDEX_CARD_CHANGE):
            tabBtn = self._getTabList()[tabIndex].get('tabName', '')
            btn = getattr(self.widget, tabBtn, '')
            if btn:
                valid, errorGMDD = self.checkTabFunctionVaild(tabIndex)
                if not valid:
                    btn.enabled = False
                    btn.mouseEnabled = True
                    TipManager.addTip(btn, uiUtils.getTextFromGMD(errorGMDD))

    def checkTabFunctionVaild(self, tabIdx):
        p = BigWorld.player()
        opTypeTuple = ()
        errorGMDD = None
        if tabIdx == TAB_INDEX_CARD_SLOT:
            opTypeTuple = const.CARD_SLOTS_OPEN_OPTYPE_TUPLE
            errorGMDD = GMDD.data.CARD_SLOT_NOT_OPEN_BY_SERVER_PROGRESS
        elif tabIdx == TAB_INDEX_CARD_CHANGE:
            opTypeTuple = const.CARD_CHANGE_OPEN_OPTYPE_TUPLE
            errorGMDD = GMDD.data.CARD_CHANGE_NOT_OPEN_BY_SERVER_PROGRESS
        if opTypeTuple and errorGMDD:
            if not p.isAdvanceCardSysOpen(opTypeTuple):
                return (False, errorGMDD)
        return (True, None)

    def onTabChanged(self, *args):
        super(CardSystemProxy, self).onTabChanged(*args)
        self.eTypeFilters = []
        self.washNumFilters = []

    def getMenuMc(self):
        pMenu = getattr(self.currentView, 'propMenu', None)
        vMenu = getattr(self.currentView, 'versionMenu', None)
        tMenu = getattr(self.currentView, 'typeMenu', None)
        searchMc = getattr(self.currentView, 'searchInputTxt', None)
        return (pMenu,
         vMenu,
         tMenu,
         searchMc)

    def setMenuComm(self):
        pMenu, vMenu, tMenu, searchMc = self.getMenuMc()
        if pMenu:
            ASUtils.setDropdownMenuData(pMenu, self.propMenuData)
            pMenu.selectedIndex = 0
            pMenu.menuRowCount = min(len(self.propMenuData), DROP_DOWN_ROW_MAX)
            pMenu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handlePropMenuItemSelected, False, 0, True)
        if vMenu:
            ASUtils.setDropdownMenuData(vMenu, self.versionMenuData)
            vMenu.selectedIndex = 0
            vMenu.menuRowCount = min(len(self.versionMenuData), DROP_DOWN_ROW_MAX)
            vMenu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleVersionMenuItemSelected, False, 0, True)
        if tMenu:
            ASUtils.setDropdownMenuData(tMenu, self.typeMenuData)
            tMenu.selectedIndex = 0
            tMenu.menuRowCount = min(len(self.typeMenuData), DROP_DOWN_ROW_MAX)
            tMenu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleTypeMenuItemSelected, False, 0, True)
        if searchMc:
            searchMc.maxChars = 10
            searchMc.addEventListener(events.EVENT_CHANGE, self.handleSearchTxtChange, False, 0, True)
        self.refreshVersionMenuData(self.curVerMenuIdx)
        self.curVerMenuIdx = 0

    def refreshVersionMenuData(self, chooseVersionId = 0):
        pMenu = getattr(self.currentView, 'propMenu', None)
        propType = 0
        if pMenu and self.propMenuData:
            propType = self.propMenuData[pMenu.selectedIndex].get('data', '')
        vMenu = getattr(self.currentView, 'versionMenu', None)
        if not propType:
            newVersionData = self.versionMenuData
        else:
            newVersionData = self.getVersionMenuDataByPropType(propType)
        if vMenu:
            ASUtils.setDropdownMenuData(vMenu, newVersionData)
            self.curVerMenuData = newVersionData
            vMenu.selectedIndex = 0
            vMenu.menuRowCount = min(len(newVersionData), DROP_DOWN_ROW_MAX)
            if chooseVersionId:
                for idx, menuData in enumerate(self.versionMenuData):
                    if menuData['data'] == chooseVersionId:
                        vMenu.selectedIndex = idx
                        return

    def getVersionMenuDataByPropType(self, propType):
        versionData = []
        for vInfo in self.versionMenuData:
            _pType = vInfo.get('propType', 0)
            if propType == _pType:
                versionData.append(vInfo)

        CARD_SYSTEM_PROP_TYPE_DESC = SCD.data.get('CARD_SYSTEM_PROP_TYPE_DESC', {})
        fragmentName = CARD_SYSTEM_PROP_TYPE_DESC.get(propType, '')
        if propType:
            label = gameStrings.CARD_SYSTEM_ALL_PROPTYPE % fragmentName
        info = {'label': label,
         'data': 0,
         'propType': propType}
        versionData.insert(0, info)
        return versionData

    def getMenuSelectedData(self):
        pMenu, vMenu, tMenu, searchMc = self.getMenuMc()
        propType = 0
        if pMenu and self.propMenuData:
            propType = self.propMenuData[pMenu.selectedIndex].get('data', '')
        ver = 0
        if vMenu and self.curVerMenuData:
            ver = self.curVerMenuData[vMenu.selectedIndex].get('data', '')
        cType = 0
        if tMenu and self.typeMenuData:
            cType = self.typeMenuData[tMenu.selectedIndex].get('data', '')
        keyword = ''
        if searchMc:
            keyword = searchMc.text
        return (propType,
         ver,
         cType,
         keyword)

    def getAllCardListData(self, filterFunc = None, sortFunc = None):
        propType, ver, cType, keyword = self.getMenuSelectedData()
        p = BigWorld.player()
        self.allCardData = []
        expiredCardIds = []
        for cardId, itemData in BCD.data.iteritems():
            cardObj = p.getCard(cardId, tempId=self.tempId)
            if not cardObj:
                continue
            cardData = cardObj.getConfigData()
            cardAdvanceData = cardObj.getAdvanceData()
            if cardObj.isExpiredCard() or cardObj.isNoRenewalDueCard() or cardObj.isDueCard():
                expiredCardIds.append(cardId)
            if propType and propType != cardData.get('propType', 0):
                continue
            if ver and ver != cardData.get('versionId', 0):
                continue
            if cType and cType != cardData.get('type', 0):
                continue
            nowTime = utils.getNow()
            if cardObj.validTime and nowTime >= cardObj.expiredTime:
                continue
            if not cardObj.actived:
                if cardData.get('isHide', 0):
                    continue
            keyword = self.currentView.searchInputTxt.text
            if keyword:
                cardSlotPropDesc = self.getCardEffectDesc(cardObj)
                cardActivePropDesc = self.getCardEffectDesc(cardObj, False)
                if keyword not in cardData.get('name', '') and keyword not in cardSlotPropDesc and keyword not in cardActivePropDesc and keyword not in cardAdvanceData.get('matchField', '') and not (keyword == gameStrings.CARD_SYSTEM_ADVANCE and cardObj.isAdvanced):
                    continue
            if filterFunc and not filterFunc(cardObj):
                continue
            self.allCardData.append(cardId)

        if expiredCardIds:
            p.base.onCardExpired(expiredCardIds)

        def defaultSortFunc(cardId1, cardId2):
            cardObj1 = p.getCard(cardId1, tempId=self.tempId)
            cardObj2 = p.getCard(cardId2, tempId=self.tempId)
            if cardObj1.showPriority < cardObj2.showPriority:
                return 1
            if cardObj1.showPriority > cardObj2.showPriority:
                return -1
            return 0

        if sortFunc:
            self.allCardData = sortFunc(self.allCardData)
        else:
            self.allCardData.sort(cmp=defaultSortFunc, reverse=True)
        return self.allCardData

    @ui.callInCD(0.1)
    def setAllCardList(self, filterFunc = None, sortFunc = None):
        listMc = getattr(self.currentView, 'cardList', None)
        if listMc:
            dataList = self.getAllCardListData(filterFunc=filterFunc, sortFunc=sortFunc)
            listMc.labelFunction = self.cardListFunction
            listMc.dataArray = range(len(dataList))
            listMc.validateNow()
            self.cacheCardListArg = (filterFunc, sortFunc)
            if self.selectedCardId not in dataList:
                self.setSelectedItem(None)
            if self.scrollToCard:
                self.scrollToCardFunc(self.scrollToCard)
                self.scrollToCard = 0
            if not self.selectedCardId and len(dataList):
                self.setSelectedItem(listMc.items[0], inital=True)

    def cardListFunction(self, *arg):
        index = int(arg[3][0].GetNumber())
        itemMc = ASObject(arg[3][1])
        if itemMc and self.allCardData:
            if self.currentTabIndex == TAB_INDEX_CARD_CHANGE:
                itemMc.scaleX = 0.789
                itemMc.scaleY = 0.789
            else:
                itemMc.scaleX = 1
                itemMc.scaleY = 1
            p = BigWorld.player()
            cardId = self.allCardData[index]
            cardObj = p.getCard(cardId, tempId=self.tempId)
            if cardObj:
                itemMc.cardId = cardObj.id
                isBreakRank = cardObj.isBreakRank
                itemMc.normalCard.visible = not isBreakRank
                itemMc.goldCard.visible = isBreakRank
                currentCard = itemMc.goldCard if isBreakRank else itemMc.normalCard
                itemMc.curCard = currentCard
                self.setCardItem(currentCard, cardObj)
                TipManager.addTipByType(itemMc, tipUtils.TYPE_CARD_TIP, (cardObj.id,), False)
                itemMc.widgetId = uiConst.WIDGET_CARD_SYSTEM
                itemMc.addEventListener(events.MOUSE_CLICK, self.handleCardClick, False, 0, True)
                isSelCard = cardId == self.selectedCardId
                currentCard.selectedBg.visible = isSelCard
                if isSelCard:
                    self.selectedCardItem = itemMc

    def scrollToCardFunc(self, cardId):
        if not self.hasBaseData():
            return
        else:
            index = 0
            if cardId in self.allCardData:
                index = self.allCardData.index(cardId)
            listMc = getattr(self.currentView, 'cardList', None)
            if listMc:
                pos = listMc.getIndexPosY(index)
                listMc.scrollTo(pos)
            return

    def setCardItem(self, cardItem, cardObj):
        isLight = (not self.eTypeFilters or cardObj.equipType == self.eTypeFilters) and (not self.washNumFilters or cardObj.washNumId in self.washNumFilters) and cardObj.actived and cardObj.isValidCard()
        cardItem.gotoAndStop('jihuo' if isLight else 'weijihuo')
        self.setCardMc(cardItem.card, cardObj)
        if cardItem.advanceMask:
            cardItem.advanceMask.visible = False

    def setCardMc(self, cardMc, cardObj):
        curProxy = self.getCurrentProxy()
        itemData = cardObj.getConfigData()
        cType = itemData.get('type', 0)
        name = itemData.get('name', 0)
        cardMc.image.fitSize = True
        cardMc.image.loadImage(cardObj.cardIcon)
        cardMc.typeIcon.fitSize = True
        cardMc.typeIcon.loadImage(cardObj.qualityIcon)
        cardMc.nameTxt.text = name
        cardMc.cdMc.visible = cardObj.isCoolingDown and getattr(curProxy, 'showCardCd', False)
        isNew = getattr(cardObj, 'isNew', False)
        cardMc.newFlag.visible = isNew
        cardMc.usedFlag.visible = bool(not isNew and cardObj.slot and getattr(curProxy, 'showCardEquip', False))
        self.setCardLevel(cardMc, cardObj.advanceLvEx)
        pText = ''
        props = []
        if cardObj.noFixToSlot:
            props = cardObj.activeProps
            for propId, propVal in props:
                propertyName, propVal = self.uiAdapter.cardSystem.transPropVal(propId, propVal)
                pText += self.formatPropStr(propertyName, propVal)

        else:
            propDict = self.calcCardValidProp(cardObj)
            props = propDict.get('advanceProps', ())
            for propId, propVal, oriVal, addRatio in props:
                propertyName, propVal = self.uiAdapter.cardSystem.transPropVal(propId, propVal)
                pText += self.formatPropStr(propertyName, propVal)

        if len(props) <= 2:
            cardMc.desc.gotoAndStop('type2')
        else:
            cardMc.desc.gotoAndStop('type3')
        cardMc.desc.descTxt.htmlText = pText
        passiveSkills = self.getCardSkillInfo(cardObj)
        activeSkills = self.getCardSkillInfo(cardObj, False)
        for i in xrange(0, PASSIVE_SKILL_LV_PHASE):
            effectLvMc = getattr(cardMc.desc, 'effectLv' + str(i), None)
            if effectLvMc:
                if i < len(passiveSkills) or i < len(activeSkills):
                    skillTitle, sDesc, openLv = passiveSkills[i] if i < len(passiveSkills) else activeSkills[i]
                    effectLvMc.visible = True
                    effectLvTxt = gameStrings.CARD_SUIT_INACTIVE_RANK if cardObj.advanceLvEx < openLv else gameStrings.CARD_SUIT_ACTIVE_RANK
                    effectLvMc.htmlText = effectLvTxt % openLv
                else:
                    effectLvMc.visible = False

    def transPropVal(self, propId, propVal, nameType = 'name'):
        prdData = PRD.data.get(propId, {})
        propertyName = prdData.get(nameType, '')
        pId = prdData.get('property', '')
        showType = prdData.get('showType', '')
        numtype = PD.data.get(pId, {}).get('numtype', '')
        if showType == 0:
            propVal = int(propVal)
        if numtype == 'F':
            propVal = gameStrings.CARD_SYSTEM_PROP_PERCENT_STR % str(self.getRightPercentVal(propVal * 100))
        return (propertyName, propVal)

    def getVersionAtlasData(self):
        return self.versionAtlasData

    def getAtlasActivedNumData(self, verId):
        p = BigWorld.player()
        cardIds = self.versionAtlasData.get(verId, {}).get('cardIds', [])
        activedNum = 0
        for cardId in cardIds:
            cardObj = p.getCard(cardId, tempId=self.tempId)
            if cardObj and cardObj.actived:
                activedNum += 1

        return activedNum

    def getAtlasConMax(self, verId):
        atlasData = CAD.data.get(verId, {})
        conMax = 0
        for num in xrange(1, uiConst.CARD_ATLAS_PROP_NUM_MAX):
            cond = atlasData.get('cond' + str(num), 0)
            if cond and cond > conMax:
                conMax = cond

        return conMax

    def getAllAtlasProp(self, propType = 0, ver = 0):
        curAtlasPropDict = {}
        allAtlasPropDict = {}
        for verId, vData in self.versionAtlasData.iteritems():
            cardIds = vData.get('cardIds', [])
            atlasPropType = vData.get('propType', 0)
            activedNum = self.getAtlasActivedNumData(verId)
            atlasData = CAD.data.get(verId, {})
            for num in xrange(1, uiConst.CARD_ATLAS_PROP_NUM_MAX):
                cond = atlasData.get('cond' + str(num), 0)
                if cond and cond <= activedNum:
                    propArr = atlasData.get('prop' + str(num), ((0, 0),))
                    for propId, propVal in propArr:
                        if propId in allAtlasPropDict:
                            allAtlasPropDict[propId] += propVal
                        else:
                            allAtlasPropDict[propId] = propVal
                        if ver and verId != ver:
                            continue
                        if propType and atlasPropType != propType:
                            continue
                        if propId in curAtlasPropDict:
                            curAtlasPropDict[propId] += propVal
                        else:
                            curAtlasPropDict[propId] = propVal

        return (allAtlasPropDict, curAtlasPropDict)

    def getInvalidAtlasProp(self, cardObj):
        if not cardObj:
            return
        verId = cardObj.version
        activedNum = self.getAtlasActivedNumData(verId)
        atlasData = CAD.data.get(verId, {})
        for num in xrange(1, uiConst.CARD_ATLAS_PROP_NUM_MAX):
            cond = atlasData.get('cond' + str(num), 0)
            if cond and cond == activedNum:
                propArr = atlasData.get('prop' + str(num), ((0, 0),))
                return propArr

        return (0, 0)

    def formatPropStr(self, title, propVal, separator = '\n', op = '+', titleColor = uiConst.CARD_PROP_TITLE_COLOR, valColor = uiConst.CARD_PROP_VAL_COLOR):
        propVal = str(self.getRightPercentVal(propVal))
        if isinstance(title, int):
            title = PRD.data.get(title, {}).get('name')
        titleStr = uiUtils.toHtml(title, titleColor)
        strPropFormat = gameStrings.CARD_SYSTEM_PROP_ITEM_S_STR if isinstance(propVal, str) else gameStrings.CARD_SYSTEM_PROP_ITEM_STR
        val = uiUtils.toHtml(strPropFormat % (op, propVal), valColor)
        return titleStr + val + separator

    def getCurSelCardId(self):
        return self.selectedCardId

    def refreshCurCardList(self):
        if not self.hasBaseData():
            return
        currentProxy = self.getCurrentProxy()
        if currentProxy:
            currentProxy.refreshCardList()

    def hasBaseData(self):
        if not self.widget:
            return False
        return True

    def canCompoundCard(self, cardObj):
        p = BigWorld.player()
        if self.cardBag.get('fragment', {}).get(cardObj.propType, 0) >= cardObj.compoundFragmentCnt(0):
            return True
        itemId = cardObj.cardItemParentId
        count = p.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
        if count > 0:
            return True
        return False

    def handleSearchTxtChange(self, *args):
        self.setAllCardList(*self.cacheCardListArg)

    def handlePropMenuItemSelected(self, *args):
        self.refreshVersionMenuData()
        self.setAllCardList(*self.cacheCardListArg)
        self.getCurrentProxy().handlePropMenuSel(*args)

    def handleVersionMenuItemSelected(self, *args):
        self.setAllCardList(*self.cacheCardListArg)
        self.getCurrentProxy().handleVersionMenuSel(*args)

    def handleTypeMenuItemSelected(self, *args):
        self.setAllCardList(*self.cacheCardListArg)
        self.getCurrentProxy().handleTypeMenuSel(*args)

    def handleSearchBtnClick(self, *args):
        pass

    def handleHideInactiveBtnSelect(self, *args):
        self.refreshCardList()

    def getCardSkillInfo(self, cardObj, isSlotProp = True, fType = uiConst.CARD_SKILL_FORMAT_TYPE_RANK):
        skillDesc = []
        passivity, condSkill = self.getCardSkillsOpenLv(cardObj, isSlotProp)
        for (skillId, lv), openLv in passivity.iteritems():
            desc = PDD.data.get((skillId, lv), {}).get('desc', '')
            desc = desc.replace('<', '&lt;').replace('>', '&gt;')
            if fType == uiConst.CARD_SKILL_FORMAT_TYPE_RANK:
                desc = gameStrings.CARD_SKILL_OPENLV % (openLv, desc)
            elif fType == uiConst.CARD_SKILL_FORMAT_TYPE_DIAN:
                desc = gameStrings.CARD_SKILL_DIAN % (desc,)
            skillDesc.append((desc, STDD.data.get((skillId, lv), {}).get('mainEff', ''), openLv))

        for (skillId, propVal), openLv in condSkill.iteritems():
            condData = CPD.data.get(skillId, {})
            formatType = int(condData.get('formatType', 0))
            desc = condData.get('desc', '')
            desc = desc.replace('<', '&lt;').replace('>', '&gt;')
            if formatType == const.COND_PROP_NUM_PERCENT:
                desc = desc % (propVal * 100,)
            else:
                desc = desc % (propVal,)
            if fType == uiConst.CARD_SKILL_FORMAT_TYPE_RANK:
                desc = gameStrings.CARD_SKILL_OPENLV % (openLv, desc)
            elif fType == uiConst.CARD_SKILL_FORMAT_TYPE_DIAN:
                desc = gameStrings.CARD_SKILL_DIAN % (desc,)
            skillDesc.append((desc, '', openLv))

        skillDesc.sort(key=lambda x: x[2])
        return skillDesc

    def getCardSkillsOpenLv(self, cardObj, isSlotProp = True):
        passivity = {}
        condSkill = {}
        skillLvDict = {}
        for i in xrange(0, const.CARD_MAX_RANK + 1):
            cId = cardObj.id * const.CARD_PRESERVED_RANK + i
            acdData = ACD.data.get(cId, {})
            pData = ()
            cData = ()
            if isSlotProp:
                pData = acdData.get('passivity', ())
                cData = acdData.get('condProps', ())
            else:
                pData = acdData.get('activeEffect', ())
                cData = acdData.get('activeCondProps', ())
            for skillData in pData:
                if skillData not in passivity:
                    passivity[skillData] = i

            for skillData in cData:
                if skillData not in condSkill:
                    condSkill[skillData] = i

        return (passivity, condSkill)

    def handleCardClick(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.widgetId != uiConst.WIDGET_CARD_SYSTEM:
            return
        e.stopPropagation()
        self.setSelectedItem(e.currentTarget)
        if e.buttonIdx == uiConst.RIGHT_BUTTON:
            if self.currentTabIndex == TAB_INDEX_CARD_SLOT:
                self.getCurrentProxy().fixCard(e.currentTarget.cardId)

    def useCardItem(self, item, page, pos):
        if not item:
            return
        itemId = item.id
        behavior = CID.data.get(itemId, {}).get('param', 0)
        cardId = CID.data.get(item.id, {}).get('cardId', 0)
        if not behavior:
            return
        if behavior == const.CARD_ITEM_BEHAVIOR_OPEN_PANEL:
            self.show(tabIndex=TAB_INDEX_CARD_MAKE, selectedCardId=cardId)
        elif behavior == const.CARD_ITEM_BEHAVIOR_OPEN_CARD_SLOT_PANEL_VERSION:
            self.show(tabIndex=TAB_INDEX_CARD_MAKE, vMenuSelectedIdx=SCD.data.get('cardUseVersionId', 2700))
        else:
            p = BigWorld.player()
            p.cell.useCommonItemWithParam(page, pos, 'behavior', behavior)
            if behavior in (const.CARD_ITEM_BEHAVIOR_COMPOUND, const.CARD_ITEM_BEHAVIOR_LV_TO_TOP):
                BigWorld.callback(0.5, Functor(self.show, TAB_INDEX_CARD_MAKE, cardId))

    def showBindConfirmDialog(self, item, page, pos, behavior, cardId, dialogContent, comfirmDialogFlagName):
        if item.isForeverBind() or gameglobal.rds.ui.messageBox.getCheckOnceData(comfirmDialogFlagName):
            self.__useCardItem(page, pos, behavior, cardId)
        else:
            func = Functor(self.__useCardItem, page, pos, behavior, cardId)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(dialogContent, func, isShowCheckBox=True, checkOnceType=comfirmDialogFlagName)

    def __useCardItem(self, page, pos, behavior, cardId):
        p = BigWorld.player()
        cardObj = p.getCard(cardId, True, tempId=self.tempId)
        if behavior == const.CARD_ITEM_BEHAVIOR_PROGRESS and bool(cardObj.checkAdvance()) and not self.widget:
            self.show()
        p.cell.useCommonItemWithParam(page, pos, 'behavior', behavior)

    def setCardLevel(self, cardItem, level):
        for i in xrange(STAR_LEVEL_MAX):
            lvStar = getattr(cardItem.level, 'lvStar' + str(i))
            starMc = lvStar.star0
            if starMc:
                starMc.visible = i < level and level <= STAR_LEVEL_MAX or MOON_LEVEL_MAX >= level > STAR_LEVEL_MAX and level % PER_LEVEL_NUM and level % PER_LEVEL_NUM - 1 < i
            moonMc = lvStar.star1
            if moonMc:
                moonMc.visible = i + STAR_LEVEL_MAX < level and MOON_LEVEL_MAX >= level > STAR_LEVEL_MAX

    def getCardPropertyDesc(self, cardObj, separator = '\n', propertyColor = None, isAdd = True):
        cardEffectInfo = ''
        cardConf = cardObj.getConfigData()
        propertyArray = cardObj.activeProps + cardObj.advanceProps
        op = '+' if isAdd else '-'
        for attr in propertyArray:
            attrId = attr[0]
            propertyValue = attr[1]
            propertyName = PRD.data[attrId]['name']
            cardEffectInfo += self.formatPropStr(propertyName, propertyValue, separator=separator, op=op)

        return cardEffectInfo

    def onServerCallback(self, funcName, *args):
        pass

    def initAllSuitData(self):
        self.allSuitData = {}
        self.suitComposeData = {}
        for (sId, rank), v in CSD.data.iteritems():
            self.allSuitData.setdefault(sId, {})
            self.allSuitData[sId][rank] = v
            composeKey = list(v.get('compose', []))
            composeKey.sort()
            composeKey = tuple(composeKey)
            self.suitComposeData.setdefault(composeKey, set())
            self.suitComposeData[composeKey].add(sId)

    def loadAllCard(self):
        if self.hasLoadAllCard.get(self.tempId, False):
            return
        p = BigWorld.player()
        versionList = []
        for cardId, itemData in BCD.data.iteritems():
            cardObj = p.getCard(cardId, True, tempId=self.tempId)
            ver = itemData.get('version', '')
            verId = cardObj.version
            propType = cardObj.propType
            info = {'label': ver,
             'data': verId,
             'propType': propType}
            if verId and info not in self.versionMenuData:
                self.versionMenuData.append(info)
            info = {'label': gameStrings.CARD_SYSTEM_PROP_TYPE_DESC.get(propType, ''),
             'data': propType}
            if propType and info not in self.propMenuData:
                self.propMenuData.append(info)
            cardType = itemData.get('type', 0)
            cardSystemTypeDesc = SCD.data.get('cardSystemTypeDesc', gameStrings.CARD_SYSTEM_CARD_TYPE_DESC)
            info = {'label': cardSystemTypeDesc.get(cardType, ''),
             'data': cardType}
            if cardType and info not in self.typeMenuData:
                self.typeMenuData.append(info)
            self.propMenuData.sort(key=lambda x: x['data'])
            self.versionMenuData.sort(key=lambda x: x['data'])
            self.typeMenuData.sort(key=lambda x: x['data'])
            self.versionAtlasData.setdefault(verId, {})
            self.versionAtlasData[verId].setdefault('propType', 0)
            self.versionAtlasData[verId].setdefault('cardIds', [])
            self.versionAtlasData[verId]['cardIds'].append(cardId)
            self.versionAtlasData[verId]['propType'] = propType

        self.hasLoadAllCard[self.tempId] = True

    def getAllActivedScore(self):
        p = BigWorld.player()
        activedScore = 0
        cardEquipScoreLimit = SCD.data.get('cardEquipScoreLimit', {})
        limitScore = {}
        for cardId, itemData in BCD.data.iteritems():
            cardObj = p.getCard(cardId, tempId=self.tempId)
            if cardObj.version in cardEquipScoreLimit:
                limitScore.setdefault(cardObj.version, [])
                limitScore[cardObj.version].append(cardObj.cardActiveScore)
                continue
            if cardObj:
                activedScore += cardObj.cardActiveScore

        for version, scoreList in limitScore.iteritems():
            limitNum = cardEquipScoreLimit.get(version, 0)
            scoreList.sort(reverse=True)
            activedScore += sum(scoreList[:limitNum])

        return activedScore

    def getAllAtlasScore(self):
        p = BigWorld.player()
        atlasScore = 0
        for verId, atlasData in CAD.data.iteritems():
            activedNum = self.getAtlasActivedNumData(verId)
            for num in xrange(1, uiConst.CARD_ATLAS_PROP_NUM_MAX):
                cond = atlasData.get('cond' + str(num), 0)
                if cond and cond <= activedNum:
                    atlasScore += atlasData.get('score' + str(num), 0)

        return atlasScore

    def getValidSlotScores(self):
        equipSlot = self.cardBag.get('equipSlot', 0)
        return self.getCardSlotScores(equipSlot)

    def getCardSlotScores(self, equipSlot):
        p = BigWorld.player()
        slotNum = self.cardBag.get('slotNum', {}).get(equipSlot, 0)
        washScore = 0
        equipScore = 0
        suitScore = 0
        limitScore = {}
        cardEquipScoreLimit = SCD.data.get('cardEquipScoreLimit', {})
        for i in xrange(0, slotNum):
            slotId = equipSlot * const.CARD_SLOT_DIV_NUM + i + 1
            slotCardId = self.cardBag.get('cardSlots', {}).get(slotId, 0)
            cardObj = p.getCard(slotCardId, tempId=self.tempId)
            if cardObj:
                if cardObj.version in cardEquipScoreLimit:
                    limitScore.setdefault(cardObj.version, [])
                    limitScore[cardObj.version].append((cardObj.cardEquipScore, cardObj.cardWashScore))
                else:
                    equipScore += cardObj.cardEquipScore
                    if cardObj.advanceLv >= const.CARD_BREAK_RANK:
                        washScore += cardObj.cardWashScore

        for version, scoreList in limitScore.iteritems():
            limitNum = cardEquipScoreLimit.get(version, 0)
            scoreList.sort(key=lambda x: sum(x), reverse=True)
            validScoreList = scoreList[:limitNum]
            equipScore += sum([ x[0] for x in validScoreList ])
            washScore += sum([ x[1] for x in validScoreList ])

        suitInfo = self.uiAdapter.cardSlot.getPskillEffects(equipSlot)
        curSuitId, curSuitRank = self.cardBag.get('equipSuit', {}).get(equipSlot, (0, 0))
        if not gameglobal.rds.configData.get('enableChangeCardSuit', 0):
            for k, v in suitInfo.iteritems():
                suitScore += CSD.data.get(k, {}).get('score', 0)

        else:
            suitScore += CSD.data.get((curSuitId, curSuitRank), {}).get('score', 0)
        return (washScore, equipScore, suitScore)

    def setSelectedItemByCardId(self, cardId):
        oldCardId = self.selectedCardId
        newCardId = cardId
        listMc = getattr(self.currentView, 'cardList', None)
        items = []
        if listMc:
            items = listMc.items
        oldItem = None
        newItem = None
        for item in items:
            if newCardId == item.cardId:
                newItem = item
            if oldCardId == item.cardId:
                oldItem = item

        if cardId:
            if oldItem and self.selectedCardId and oldItem.cardId == self.selectedCardId:
                oldItem.curCard.selectedBg.visible = False
            self.selectedCardId = newCardId
            if newItem:
                self.selectedCardItem = newItem
            if self.selectedCardItem:
                self.selectedCardItem.curCard.selectedBg.visible = True
        else:
            self.selectedCardId = None
            self.selectedCardItem = None
        self.getCurrentProxy().onSelectedCard(newItem, True, oldCardId)

    def setSelectedItem(self, cardItem, inital = False):
        if not self.hasBaseData():
            return
        else:
            oldCardId = self.selectedCardId
            if cardItem:
                if self.selectedCardItem and self.selectedCardId and self.selectedCardItem.cardId == self.selectedCardId:
                    self.selectedCardItem.curCard.selectedBg.visible = False
                self.selectedCardId = cardItem.cardId
                self.selectedCardItem = cardItem
                if self.selectedCardItem:
                    self.selectedCardItem.curCard.selectedBg.visible = True
            else:
                self.selectedCardId = None
                self.selectedCardItem = None
            currentProxy = self.getCurrentProxy()
            if currentProxy:
                currentProxy.onSelectedCard(cardItem, inital, oldCardId)
            return

    def getCardEffectDesc(self, cardObj, isSlotProp = True):
        cardEffectInfo = self.getCardPropertyDesc(cardObj)
        skills = cardObj.passivitySkills
        skillDescArr = self.getCardSkillInfo(cardObj, isSlotProp=isSlotProp)
        for skillDesc, skillTipDesc, openLv in skillDescArr:
            cardEffectInfo += skillDesc + '\n'
            cardEffectInfo += skillTipDesc + '\n'

        return cardEffectInfo

    def getCardTipData(self, cardId, oriData = False, fullLv = False):
        p = BigWorld.player()
        cardObj = None
        if fullLv:
            cardObj = Card(cardId, actived=True, advanceLv=const.CARD_MAX_RANK)
        else:
            cardObj = p.getCard(cardId, True, tempId=self.tempId)
        data = {}
        if not cardObj:
            if oriData:
                return data
            return uiUtils.dict2GfxDict(data, True)
        cData = cardObj.getConfigData()
        cardType = cData.get('type', 0)
        activedNum = self.getAtlasActivedNumData(cardObj.version)
        conMax = self.getAtlasConMax(cardObj.version)
        numStr = uiUtils.convertNumStr(activedNum, conMax, enoughColor='', notEnoughColor='')
        data['bgColor'] = self.cardTypeColorList[cardType]
        data['icon'] = cardObj.cardIcon
        data['equipIcon'] = cardObj.equipIcon
        data['name'] = cData.get('name', '')
        data['nameColor'] = self.cardTypeColorList[cardType]
        data['atlasStr'] = cData.get('version', '') + ' ' + numStr if conMax else ''
        cardEquipTypeDict = SCD.data.get('cardEquipTypeDict', {})
        cardSceneType = CARD_SCENE_TYPE_DESC.get(cardObj.propType, '')
        cardSceneTypeDesc = SCD.data.get(cardSceneType, {})
        data['cardSceneTypeDesc'] = cardSceneTypeDesc
        cardEquipTypeDict = SCD.data.get('cardEquipTypeDict', {})
        data['equipTypeDesc'] = gameStrings.CARD_EQUIP_TYPE_DESC % cardEquipTypeDict.get(cardObj.equipType, '')
        validTimeTxt = ''
        if cardObj.expiredTime:
            validTimeTxt = gameStrings.CARD_VALID_TIME % utils.formatDatetime(cardObj.expiredTime)
        elif cardObj.dueTime:
            if cardObj.dueTime - utils.getNow() > 0:
                validTimeTxt = gameStrings.CARD_REMAIN_TIME_TXT + utils.formatDuration(cardObj.dueTime - utils.getNow())
            else:
                validTimeTxt = gameStrings.CARD_REMAIN_TIME_TXT + gameStrings.CARD_DUE_TIME_OUT
        validTimeTxt = uiUtils.toHtml(validTimeTxt, VALID_TIME_COLOR)
        data['validTimeTxt'] = validTimeTxt
        CARD_SYSTEM_PROP_TYPE_DESC = SCD.data.get('CARD_SYSTEM_PROP_TYPE_DESC', {})
        fragmentName = CARD_SYSTEM_PROP_TYPE_DESC.get(cardObj.propType, '')
        canActiveSuitList = []
        showPriorityDict = {}
        for k, v in CSD.data.iteritems():
            composeName = v.get('composeName', {})
            showPriority = v.get('showPriority', 0)
            suitId, slv = k
            if showPriority:
                showPriorityDict[suitId] = showPriority
            if cardObj.equipType in v.get('compose', []) and (composeName, suitId) not in canActiveSuitList:
                canActiveSuitList.append((composeName, suitId))

        canActiveSuitList.sort(key=lambda k: showPriorityDict.get(k[1], 0))
        canActiveSuit = ' '.join([ sItem[0] for sItem in canActiveSuitList ])
        if cardObj.noFixToSlot:
            data['canActiveSuit'] = ''
        else:
            data['canActiveSuit'] = gameStrings.CARD_TIPS_CAN_ACTIVE_SUIT_TXT % (canActiveSuit,)
        cardSystemTypeDesc = SCD.data.get('cardSystemTypeDesc', gameStrings.CARD_SYSTEM_CARD_TYPE_DESC)
        data['type'] = cardSystemTypeDesc.get(cardType, '')
        data['level'] = cardObj.advanceLvEx
        data['levelStr'] = gameStrings.CARD_SUIT_RANK % (cardObj.advanceLvEx,)
        data['bindType'] = ''
        data['propDesc'] = fragmentName + gameStrings.CARD_COMMON_NAME
        cardScore = cardObj.cardActiveScore + cardObj.cardEquipScore + cardObj.cardWashScore
        data['scroeTxt'] = int(cardScore)
        needProgress = 0
        if cardObj.actived:
            needProgress = cardObj.compoundFragmentCnt(cardObj.advanceLv + 1)
        else:
            needProgress = cardObj.compoundFragmentCnt(0)
        activeProps = cardObj.activeProps
        pText = ''
        for propId, propVal in activeProps:
            propertyName, propVal = self.uiAdapter.cardSystem.transPropVal(propId, propVal)
            pText += self.formatPropStr(propertyName, propVal)

        activeSkills = self.getCardSkillInfo(cardObj, False)
        for skillTitle, skillDesc, openLv in activeSkills:
            if skillTitle:
                color = PASSIVE_SKILL_COLOR if cardObj.advanceLvEx >= openLv else PASSIVE_SKILL_GRAY_COLOR
                skillTitle = uiUtils.toHtml(skillTitle, color)
                pText += skillTitle + '\n'

        data['activeProps'] = pText
        data['activeTitle'] = gameStrings.CARD_DIFF_ACTIVE_PROP_TITLE
        pText = ''
        propDict = self.calcCardValidProp(cardObj)
        advanceProps = propDict.get('advanceProps', ())
        for propId, propVal, oriVal, addRatio in advanceProps:
            propertyName = PRD.data.get(propId, {}).get('shortName', '')
            pId = PRD.data.get(propId, {}).get('property', '')
            numtype = PD.data.get(pId, {}).get('numtype', '')
            if numtype == 'F':
                if addRatio:
                    propVal = gameStrings.CARD_SYSTEM_PROP_PERCENT_STR_WITH_PERCENT % (str(self.getRightPercentVal(oriVal * 100)), str(self.getRightPercentVal(addRatio * 100)))
                else:
                    propVal = gameStrings.CARD_SYSTEM_PROP_PERCENT_STR % str(self.getRightPercentVal(oriVal * 100))
            elif addRatio:
                propVal = gameStrings.CARD_SYSTEM_PROP_PERCENT_INT_VAL_STR % (oriVal, str(self.getRightPercentVal(addRatio * 100)))
            pText += self.formatPropStr(propertyName, propVal)

        passiveSkills = self.getCardSkillInfo(cardObj)
        for skillTitle, skillDesc, openLv in passiveSkills:
            if skillTitle:
                color = PASSIVE_SKILL_COLOR if cardObj.advanceLvEx >= openLv else PASSIVE_SKILL_GRAY_COLOR
                skillTitle = uiUtils.toHtml(skillTitle, color)
                pText += skillTitle + '\n'

        data['advanceProps'] = pText
        extraTitleTxt = ''
        sceneType = p.getCardSceneType()
        equipSlot = self.cardBag.get('equipSlot', 0)
        isGray = False
        slotType, slotIndex = (0, 0)
        for slotId in cardObj.slot:
            slotType, slotIndex = self.parseSlotId(slotId)
            if slotType == equipSlot:
                break

        if not slotType or slotType != equipSlot:
            extraTitleTxt = gameStrings.CARD_TIPS_PROP_INVALID_TXT
        elif cardObj.propType != sceneType:
            extraTitleTxt = gameStrings.CARD_TIPS_PROP_NOT_IN_SCENE_TXT
        else:
            extraTitleTxt = gameStrings.CARD_TIPS_PROP_VALID_TXT
        data['advanceTitle'] = gameStrings.CARD_DIFF_ADVANCE_PROP_TITLE + extraTitleTxt
        extraTitleTxt = ''
        isGray = False
        sceneType = p.getCardSceneType()
        if not cardObj.isBreakRank:
            extraTitleTxt = gameStrings.CARD_TIPS_PROP_LOW_RANK_LV_TXT
            isGray = True
        elif not slotType or slotType != equipSlot:
            extraTitleTxt = gameStrings.CARD_TIPS_PROP_INVALID_TXT
        else:
            extraTitleTxt = gameStrings.CARD_TIPS_PROP_VALID_TXT
        washProps = cardObj.curWashProps if cardObj.curWashProps else {}
        pText = ''
        titleColor = uiConst.CARD_PROP_TITLE_COLOR
        valColor = uiConst.CARD_PROP_VAL_COLOR
        if isGray:
            titleColor = uiConst.CARD_PROP_GRAY_COLOR
            valColor = uiConst.CARD_PROP_GRAY_COLOR
        for k, v in washProps.iteritems():
            washGroupId = v.get('washGroupId', 0)
            sequence = k
            stage = v.get('stage', 0)
            sType = v.get('sType', 0)
            sId = v.get('sId', 0)
            sNum = v.get('sNum', 0)
            if sType == const.CARD_PROP_TYPE_PROPS:
                propertyName, sNum = self.uiAdapter.cardSystem.transPropVal(sId, sNum)
                pText += self.formatPropStr(propertyName, sNum, titleColor=titleColor, valColor=valColor)
            elif sType == const.CARD_PROP_TYPE_PASSIVE:
                color = titleColor
                pText += uiUtils.toHtml(PDD.data.get((sId, sNum), {}).get('desc', ''), color=color) + '\n'
            elif sType == const.CARD_PROP_TYPE_SPECIAL:
                wData = CWGD.data.get((washGroupId,
                 sequence,
                 stage,
                 sType,
                 sId), {})
                pName = wData.get('name', '')
                pText += uiUtils.toHtml(pName, titleColor) + '\n'
                seParam = wData.get('seParam', ())
            elif sType == const.CARD_PROP_TYPE_CONDITIONAL_PROPS:
                condData = CPD.data.get(sId, {})
                formatType = int(condData.get('formatType', 0))
                desc = condData.get('desc', '')
                desc = desc.replace('<', '&lt;').replace('>', '&gt;')
                if formatType == const.COND_PROP_NUM_PERCENT:
                    desc = desc % (sNum * 100,)
                else:
                    desc = desc % (sNum,)
                pText += uiUtils.toHtml(desc, color=titleColor) + '\n'

        data['washProps'] = pText
        extraTitleTxt = ''
        sceneType = p.getCardSceneType()
        if not cardObj.isBreakRank:
            extraTitleTxt = gameStrings.CARD_TIPS_PROP_LOW_RANK_LV_TXT
        elif not slotType or slotType != equipSlot:
            extraTitleTxt = gameStrings.CARD_TIPS_PROP_INVALID_TXT
        else:
            extraTitleTxt = gameStrings.CARD_TIPS_PROP_VALID_TXT
        washIndex = cardObj.washIndex
        washIndexStr = ''
        if gameconfigCommon.enableCardWashScheme():
            washIndexStr = gameStrings.CARD_WASH_INDEX.get(cardObj.washIndex, '')
            washIndexStr = gameStrings.CARD_TIPS_BRACKET_TXT % (gameStrings.CARD_CHANGE_WASH_SCHEME_TXT + washIndexStr,)
        data['washTitle'] = gameStrings.CARD_DIFF_WASH_PROP_SCHEME_TITLE % (washIndexStr,) + extraTitleTxt
        returnRate = self.getWashPointRetunRate(cardObj)
        washPoint = math.floor(cardObj.washNum * cardObj.washFragmentCnt * returnRate)
        data['washPointDesc'] = gameStrings.CARD_TIPS_WASH_POINT_TXT % (washPoint, fragmentName)
        data['progressCur'] = int(cardObj.progress)
        data['progressMax'] = needProgress
        data['isFullAdvance'] = cardObj.isFullAdvance
        forbiddenTip = ''
        if cardObj.validTime or cardObj.validTime:
            if not cardObj.canRenewal:
                forbiddenTip += gameStrings.CARD_CAN_NOT_RENEWAL + '\n'
        if cardObj.noFixToSlot:
            forbiddenTip += gameStrings.CARD_NO_FIX_TO_SLOT + '\n'
        if forbiddenTip:
            data['forbiddenTip'] = uiUtils.toHtml(forbiddenTip, color=uiConst.CARD_FORBIDDEN_COLOR)
        if cardObj.noFixToSlot and not data['advanceProps']:
            data['noFixToSlotValidTip'] = uiUtils.toHtml(gameStrings.CARD_NOFIXTOSLOT_VALID_TIP_TXT, color=uiConst.CARD_FORBIDDEN_COLOR)
        data['itemSourceTxtVisible'] = gameglobal.rds.configData.get('enableNewItemSearch', False)
        data['tipType'] = tipUtils.TYPE_CARD_TIP
        if not BigWorld.isPublishedVersion():
            data['cardIdDesc'] = gameStrings.CARD_ID_DESC % cardObj.id
        if oriData:
            return data
        else:
            return uiUtils.dict2GfxDict(data, True)

    def getWashPointRetunRate(self, cardObj):
        if not cardObj.validTime:
            return const.CARD_DEL_WASH_RETURN * 1.0 / const.CARD_DECOMPOSE_MUL
        return 1

    def getRightPercentVal(self, val):
        if isinstance(val, str):
            return val
        val = round(val, 1)
        if int(val) == val:
            return int(val)
        return str(val)

    def calcCardValidProp(self, cardObj):
        p = BigWorld.player()
        equipSlot = self.cardBag.get('equipSlot', 0)
        slotNum = self.cardBag.get('slotNum', {}).get(equipSlot, 0)
        advancePropAdd = 0

        def _calc(mCard):
            apAdd = 0
            washProps = mCard.washProps
            for k, v in washProps.iteritems():
                if not mCard.isBreakRank:
                    break
                washGroupId = v.get('washGroupId', 0)
                sequence = k
                stage = v.get('stage', 0)
                sType = v.get('sType', 0)
                sId = v.get('sId', 0)
                sNum = v.get('sNum', 0)
                if sType == const.CARD_PROP_TYPE_SPECIAL:
                    wData = CWGD.data.get((washGroupId,
                     sequence,
                     stage,
                     sType,
                     sId), {})
                    seParam = wData.get('seParam', ())
                    if isinstance(sId, tuple) and len(sId) and sId[0] == gametypes.CARD_SE_CARD_SYS_ADD_PCT:
                        sysType, version, pvpType, addPct, isSelf = seParam
                        if sysType == const.CARD_SUB_SYSTEM_EQUIP and (not version or version == cardObj.version) and (not pvpType or version == cardObj.version):
                            if isSelf and mCard.id == cardObj.id:
                                apAdd += addPct
                            elif not isSelf and cardObj.slot:
                                apAdd += addPct

            return apAdd

        if cardObj.slot:
            for i in xrange(0, slotNum):
                slotId = equipSlot * const.CARD_SLOT_DIV_NUM + i + 1
                slotCardId = self.cardBag.get('cardSlots', {}).get(slotId, 0)
                slotCard = p.getCard(slotCardId, tempId=self.tempId)
                if slotCard:
                    advancePropAdd += _calc(slotCard)

        else:
            advancePropAdd += _calc(cardObj)
        advancePropAdd += len(cardObj.washProps) * const.CARD_WASH_PROP_NUM_ADD_PCT * 1.0 / 100
        advanceProps = cardObj.advanceProps
        newAdvanceProp = []
        for propId, propVal in advanceProps:
            newAdvanceProp.append((propId,
             propVal * (1 + advancePropAdd),
             propVal,
             advancePropAdd))

        propDict = {'advanceProps': newAdvanceProp}
        return propDict

    def parseSlotId(self, slotId):
        if not slotId:
            return (0, 0)
        sType = int(slotId / const.CARD_SLOT_DIV_NUM)
        slotIndex = int(slotId % const.CARD_SLOT_DIV_NUM)
        return (sType, slotIndex)

    def getCardIcon(self, cData):
        return cData.get('icon', TEMP_ICON)

    def getSlotName(self, slot):
        return GlobalConfig.data.get('CARD_SYSTEM_SLOT_NAME_%d' % slot, '')

    def setEquipTypeFilter(self, eTypes):
        self.eTypeFilters = eTypes
        listMc = getattr(self.currentView, 'cardList', None)
        if listMc:
            p = BigWorld.player()
            items = listMc.items
            for itemMc in items:
                cardId = itemMc.cardId
                cardObj = p.getCard(cardId, tempId=self.tempId)
                self.setCardItem(itemMc.curCard, cardObj)

    def setWashNumIdFilter(self, washNumIds):
        self.washNumFilters = washNumIds
        listMc = getattr(self.currentView, 'cardList', None)
        if listMc:
            p = BigWorld.player()
            items = listMc.items
            for itemMc in items:
                cardId = itemMc.cardId
                cardObj = p.getCard(cardId, tempId=self.tempId)
                self.setCardItem(itemMc.curCard, cardObj)

    def setTabBtnsVisible(self, visible):
        if not self.hasBaseData():
            return
        for index in TAB_INDEX_SET:
            self.setTabVisible(index, visible, False)

        self.relayoutTab()

    def getCardSuitTipData(self, cardData):
        data = {}
        name = cardData.get('name', gameStrings.CARD_SUIT_TIP_NONE_SUIT_TITLE)
        data['suitName'] = name if name else gameStrings.CARD_SUIT_TIP_NONE_SUIT_TITLE
        data['isSuit'] = bool(name)
        suitId = cardData.get('suitId', gameStrings.CARD_SUIT_TIP_NONE_SUIT_TITLE)
        rank = cardData.get('rank', 0)
        quality = CSD.data.get((suitId, rank), {}).get('quality', 1)
        data['suitRankTxt'] = gameStrings.CARD_SUIT_RANK % (rank,)
        data['suitRank'] = rank
        score = cardData.get('score', 0)
        data['score'] = int(score)
        data['propTitleStr'] = gameStrings.CARD_DIFF_WASH_PROP_TITLE
        cards = []
        for cData in cardData.get('card', []):
            name, rank, washProps = cData
            props = self.genWashPropText(washProps)
            info = {'name': name,
             'rank': rank,
             'rankTxt': gameStrings.CARD_SUIT_RANK % (rank,),
             'props': props}
            cards.append(info)

        data['cards'] = cards
        data['bgColor'] = 'type' + str(quality)
        return data

    def genWashPropText(self, washProps):
        propArr = []
        pText = ''
        isShort = False
        for k, v in washProps.iteritems():
            propData = {}
            washGroupId = v.get('washGroupId', 0)
            sequence = k
            stage = v.get('stage', 0)
            sType = v.get('sType', 0)
            sId = v.get('sId', 0)
            sNum = v.get('sNum', 0)
            fullProp = v.get('fullProp', False)
            tips = ''
            washData = CWGD.data.get((washGroupId,
             sequence,
             stage,
             sType,
             sId), {})
            quality = washData.get('quality', 0)
            normalColor = uiConst.CARD_PROP_QUALITY_NORMAL_COLOR
            qualityColor = normalColor
            try:
                qualityColor = uiConst.CARD_COLORS[quality - 1]
            except:
                pass

            if sType == const.CARD_PROP_TYPE_PROPS:
                shortPropertyName = PRD.data.get(sId, {}).get('shortName', '')
                detailPropertyName = PRD.data.get(sId, {}).get('name', '')
                propertyName = shortPropertyName if isShort else detailPropertyName
                _, sNum = self.uiAdapter.cardSystem.transPropVal(sId, sNum)
                pText = self.uiAdapter.cardSystem.formatPropStr(propertyName, sNum, separator='', titleColor=normalColor, valColor=qualityColor)
            elif sType == const.CARD_PROP_TYPE_PASSIVE:
                shortDesc = PDD.data.get((sId, sNum), {}).get('mainEff', '')
                detailDesc = PDD.data.get((sId, sNum), {}).get('mainEnhEff', '')
                pText = shortDesc if isShort else detailDesc
                pText = pText % (qualityColor,)
                if isShort:
                    tips = detailDesc % (qualityColor,)
                pText = uiUtils.toHtml(pText, normalColor)
            elif sType == const.CARD_PROP_TYPE_SPECIAL:
                pName = CWGD.data.get((washGroupId,
                 sequence,
                 stage,
                 sType,
                 sId), {}).get('name', '')
                pText = uiUtils.toHtml(pName, normalColor)
            elif sType == const.CARD_PROP_TYPE_CONDITIONAL_PROPS:
                condData = CPD.data.get(sId, {})
                formatType = int(condData.get('formatType', 0))
                shortDesc = condData.get('cColorDesc', '')
                detailDesc = condData.get('colorDesc', '')

                def transDesc(desc, setColor = None):
                    if setColor:
                        if formatType == const.COND_PROP_NUM_PERCENT:
                            desc = desc % (setColor, sNum * 100)
                        else:
                            desc = desc % (setColor, sNum)
                    elif formatType == const.COND_PROP_NUM_PERCENT:
                        desc = desc % (sNum * 100,)
                    else:
                        desc = desc % (sNum,)
                    return desc

                pDesc = transDesc(detailDesc if not isShort else shortDesc, setColor=qualityColor)
                pText = uiUtils.toHtml(pDesc, color=normalColor)
            propData['pText'] = pText
            propData['fullProp'] = fullProp
            propArr.append(propData)

        return propArr

    def checkCardCanAdvance(self, cardObj, advanceLv = True):
        if cardObj:
            limitAdvanceLv = 0
            isNotAdvanceLv = False
            p = BigWorld.player()
            if cardObj.advanceLv == const.CARD_BREAK_RANK:
                if not p.isAdvanceCardSysOpen(const.CARD_OPTYPE_ADVANCE_BREAK):
                    isNotAdvanceLv = True
                    limitAdvanceLv = const.CARD_BREAK_RANK
            if cardObj.advanceLv == const.CARD_BREAK_RANK_HIGH:
                if not p.isAdvanceCardSysOpen(const.CARD_OPTYPE_ADVANCE_BREAK_HIGH):
                    isNotAdvanceLv = True
                    limitAdvanceLv = const.CARD_BREAK_RANK_HIGH
            if isNotAdvanceLv:
                if advanceLv:
                    return (False, gameStrings.CARD_MAKE_NOT_ADVANCE_CARD_BY_SERVER_PROGRESS % limitAdvanceLv)
                else:
                    return (False, gameStrings.CARD_MAKE_NOT_UPGRADE_CARD_PROGRESS_BY_SERVER_PROGRESS)
            else:
                return (True, '')
        return (False, '')

    def checkCardValidInSlot(self, cardObj):
        if not cardObj:
            return False
        equipSlot = self.cardBag.get('equipSlot', 0)
        for slotId in cardObj.slot:
            slotType, slotIndex = self.parseSlotId(slotId)
            if slotType == equipSlot:
                return True

        return False

    def getEquipNum(self, sType = None):
        curEquipNum = 0
        if not sType:
            equipSlot = self.cardBag.get('equipSlot', 0)
            sType = equipSlot
        slotNum = self.cardBag.get('slotNum', {}).get(sType, 0)
        for i in xrange(0, slotNum):
            slotId = sType * const.CARD_SLOT_DIV_NUM + i + 1
            slotCardId = self.cardBag.get('cardSlots', {}).get(slotId, 0)
            if slotCardId:
                curEquipNum += 1

        return curEquipNum

    def getCurSuitMenuData(self, slotType = 0):
        menuData = []
        p = BigWorld.player()
        sceneType = p.getCardSceneType()
        propertyData = []
        if not slotType:
            slotType = self.cardBag.get('equipSlot', 0)
        suitInfo = self.uiAdapter.cardSlot.getPskillEffects(slotType)
        propType = 0
        curSuitId, curSuitRank = self.cardBag.get('equipSuit', {}).get(slotType, (0, 0))
        hasFullSuit = False
        i = 0
        slotNumMax = SCD.data.get('cardSlotNowMaxNum', const.CARD_SLOT_NOW_MAX_NUM)
        for k, v in suitInfo.iteritems():
            suitData = CSD.data.get(k, {})
            if len(suitData.get('compose', ())) == slotNumMax:
                hasFullSuit = True
            i += 1

        if hasFullSuit:
            for k, v in suitInfo.iteritems():
                suitData = CSD.data.get(k, {})
                propType = suitData.get('propType', 0)
                titleName = suitData.get('name', '')
                _suitId, _suitRank = k
                info = {'label': titleName,
                 'iconType': 0,
                 'suitId': _suitId,
                 'suitRank': _suitRank}
                menuData.append(info)

        else:
            suitData = CSD.data.get((curSuitId, curSuitRank), {})
            propType = suitData.get('propType', 0)
            titleName = suitData.get('name', '')
            info = {'label': titleName,
             'iconType': 0,
             'suitId': curSuitId,
             'suitRank': curSuitRank}
            menuData.append(info)
        return menuData
