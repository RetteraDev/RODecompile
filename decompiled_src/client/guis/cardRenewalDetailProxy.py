#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cardRenewalDetailProxy.o
import BigWorld
import events
import utils
import gamelog
import uiConst
from uiProxy import UIProxy
from asObject import ASUtils
from asObject import ASObject
from asObject import TipManager
from guis import uiUtils
from guis import tipUtils
from guis import ui
from callbackHelper import Functor
from gamestrings import gameStrings
from data import base_card_data as BCD
from cdata import game_msg_def_data as GMDD
STAR_LEVEL_MAX = 4
MOON_LEVEL_MAX = 8
PER_LEVEL_NUM = 4
PASSIVE_SKILL_LV_PHASE = 3
SCALE_RATIO = 1.22
RIGHT_SCALE_RATIO = 1.3
CUR_CANVAS_POS_OFFSET = (10, 6)
OTHER_CANVAS_POS_OFFSET = (2, -3)

class CardRenewalDetailProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CardRenewalDetailProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CARD_RENEWAL_DETAIL, self.hide)

    def reset(self):
        super(CardRenewalDetailProxy, self).reset()
        self.curCardId = 0
        self.durationDay = 0
        self.itemIds = 0
        self.itemNums = 0
        self.allCardData = []
        self.selectedCardId = None
        self.selectedCardItem = None
        self.scrollToCard = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CARD_RENEWAL_DETAIL:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CARD_RENEWAL_DETAIL)

    def show(self, cardId, validCardList, durationDay, itemIds, itemNums):
        if not self.widget:
            self.curCardId = cardId
            self.allCardData = validCardList
            self.durationDay = durationDay
            self.itemIds = itemIds
            self.itemNums = itemNums
            self.uiAdapter.loadWidget(uiConst.WIDGET_CARD_RENEWAL_DETAIL)

    def initUI(self):
        self.widget.defaultCloseBtn = [self.widget.closeBtn, self.widget.cancelBtn]
        self.widget.confirmBtn.enabled = False
        self.widget.curValidNumTxt.text = gameStrings.CARD_RENEWAL_REMAIN_LIST_NUM_TXT % (len(self.allCardData),)
        self.widget.delayTxt.text = gameStrings.CARD_RENEWAL_TIME_TXT % (self.durationDay,)
        self.widget.cardList.column = 2
        self.widget.cardList.itemHeight = 276
        self.widget.cardList.itemWidth = 201
        self.widget.cardList.itemRenderer = 'CardSystem_CardContainer'
        self.setAllCardList()
        self.setCardCanvas(self.curCardId, self.widget.curCanvas, CUR_CANVAS_POS_OFFSET, RIGHT_SCALE_RATIO)

    def setCardCanvas(self, cardId, canvas, pos, scale):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        self.widget.removeAllInst(canvas)
        cardMc = self.widget.getInstByClsName('CardSystem_CardContainer')
        cardMc.x, cardMc.y = pos
        cardMc.scaleX = scale
        cardMc.scaleY = scale
        cardObj = p.getCard(cardId)
        if cardMc and cardObj:
            self.setCard(cardMc, cardObj, False)
            canvas.addChild(cardMc)

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        p.base.renewalCardWithItem(self.curCardId, self.itemIds, self.itemNums, [self.selectedCardId])
        self.hide()

    def setAllCardList(self):
        listMc = self.widget.cardList
        if listMc:
            dataList = self.getAllCardListData()
            listMc.labelFunction = self.cardListFunction
            listMc.dataArray = range(len(dataList))
            listMc.validateNow()
            if self.selectedCardId not in dataList:
                self.setSelectedItem(None)
            if self.scrollToCard:
                self.scrollToCardFunc(self.scrollToCard)
                self.scrollToCard = 0

    def getAllCardListData(self):
        p = BigWorld.player()

        def defaultSortFunc(cardId1, cardId2):
            cardObj1 = p.getCard(cardId1)
            cardObj2 = p.getCard(cardId2)
            if cardObj1.showPriority < cardObj2.showPriority:
                return 1
            if cardObj1.showPriority > cardObj2.showPriority:
                return -1
            return 0

        self.allCardData.sort(cmp=defaultSortFunc, reverse=True)
        return self.allCardData

    def setSelectedItemByCardId(self, cardId):
        oldCardId = self.selectedCardId
        newCardId = cardId
        listMc = self.widget.cardList
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
        self.onSelectedCard(newItem, True, oldCardId)

    def onSelectedCard(self, cardItem, inital = False, oldCardId = 0):
        if cardItem:
            self.setCardCanvas(getattr(cardItem, 'cardId', 0), self.widget.otherCanvas, OTHER_CANVAS_POS_OFFSET, RIGHT_SCALE_RATIO)
            self.widget.confirmBtn.enabled = True

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
            self.onSelectedCard(cardItem, inital, oldCardId)
            return

    def cardListFunction(self, *arg):
        index = int(arg[3][0].GetNumber())
        itemMc = ASObject(arg[3][1])
        if itemMc and self.allCardData:
            itemMc.scaleX = SCALE_RATIO
            itemMc.scaleY = SCALE_RATIO
            p = BigWorld.player()
            cardId = self.allCardData[index]
            cardObj = p.getCard(cardId)
            if cardObj:
                self.setCard(itemMc, cardObj)

    def setCard(self, itemMc, cardObj, canSelected = True):
        cardId = cardObj.id
        itemMc.cardId = cardObj.id
        isBreakRank = cardObj.isBreakRank
        itemMc.normalCard.visible = not isBreakRank
        itemMc.goldCard.visible = isBreakRank
        currentCard = itemMc.goldCard if isBreakRank else itemMc.normalCard
        itemMc.curCard = currentCard
        self.setCardItem(currentCard, cardObj)
        TipManager.addTipByType(itemMc, tipUtils.TYPE_CARD_TIP, (cardObj.id,), False)
        itemMc.widgetId = uiConst.WIDGET_CARD_RENEWAL_DETAIL
        if canSelected:
            itemMc.addEventListener(events.MOUSE_CLICK, self.handleCardClick, False, 0, True)
            isSelCard = cardId == self.selectedCardId
            currentCard.selectedBg.visible = isSelCard
            if isSelCard:
                self.selectedCardItem = itemMc
        else:
            currentCard.selectedBg.visible = False
            itemMc.removeEventListener(events.MOUSE_CLICK, self.handleCardClick)

    def setCardItem(self, cardItem, cardObj):
        isLight = cardObj.actived and cardObj.isValidCard()
        cardItem.gotoAndStop('jihuo' if isLight else 'weijihuo')
        self.setCardMc(cardItem.card, cardObj)
        if cardItem.advanceMask:
            cardItem.advanceMask.visible = False

    def setCardMc(self, cardMc, cardObj):
        itemData = cardObj.getConfigData()
        cType = itemData.get('type', 0)
        name = itemData.get('name', 0)
        cardMc.image.fitSize = True
        cardMc.image.loadImage(cardObj.cardIcon)
        cardMc.typeIcon.fitSize = True
        cardMc.typeIcon.loadImage(cardObj.qualityIcon)
        cardMc.nameTxt.text = name
        cardMc.cdMc.visible = False
        isNew = getattr(cardObj, 'isNew', False)
        cardMc.newFlag.visible = isNew
        cardMc.usedFlag.visible = False
        self.setCardLevel(cardMc, cardObj.advanceLvEx)
        pText = ''
        props = []
        if cardObj.noFixToSlot:
            props = cardObj.activeProps
            for propId, propVal in props:
                propertyName, propVal = self.uiAdapter.cardSystem.transPropVal(propId, propVal)
                pText += self.uiAdapter.cardSystem.formatPropStr(propertyName, propVal)

        else:
            propDict = self.uiAdapter.cardSystem.calcCardValidProp(cardObj)
            props = propDict.get('advanceProps', ())
            for propId, propVal, oriVal, addRatio in props:
                propertyName, propVal = self.uiAdapter.cardSystem.transPropVal(propId, propVal)
                pText += self.uiAdapter.cardSystem.formatPropStr(propertyName, propVal)

        if len(props) <= 2:
            cardMc.desc.gotoAndStop('type2')
        else:
            cardMc.desc.gotoAndStop('type3')
        cardMc.desc.descTxt.htmlText = pText
        passiveSkills = self.uiAdapter.cardSystem.getCardSkillInfo(cardObj)
        activeSkills = self.uiAdapter.cardSystem.getCardSkillInfo(cardObj, False)
        for i in xrange(0, PASSIVE_SKILL_LV_PHASE):
            skillDesc = getattr(cardMc.desc, 'skillDesc' + str(i), None)
            if skillDesc:
                if i < len(passiveSkills) or i < len(activeSkills):
                    skillTitle, sDesc, openLv = passiveSkills[i] if i < len(passiveSkills) else activeSkills[i]
                    skillDesc.visible = True
                    frameName = str(openLv) + 'jiehui' if cardObj.advanceLvEx < openLv else str(openLv) + 'jie'
                    skillDesc.gotoAndStop(frameName)
                else:
                    skillDesc.visible = False

    def setCardLevel(self, cardItem, level):
        for i in xrange(STAR_LEVEL_MAX):
            lvStar = getattr(cardItem.level, 'lvStar' + str(i))
            starMc = lvStar.star0
            if starMc:
                starMc.visible = i < level and level <= STAR_LEVEL_MAX or MOON_LEVEL_MAX >= level > STAR_LEVEL_MAX and level % PER_LEVEL_NUM and level % PER_LEVEL_NUM - 1 < i
            moonMc = lvStar.star1
            if moonMc:
                moonMc.visible = i + STAR_LEVEL_MAX < level and MOON_LEVEL_MAX >= level > STAR_LEVEL_MAX

    def scrollToCardFunc(self, cardId):
        if not self.hasBaseData():
            return
        index = 0
        if cardId in self.allCardData:
            index = self.allCardData.index(cardId)
        listMc = self.widget.cardList
        if listMc:
            pos = listMc.getIndexPosY(index)
            listMc.scrollTo(pos)

    def handleCardClick(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.widgetId != uiConst.WIDGET_CARD_RENEWAL_DETAIL:
            return
        e.stopPropagation()
        self.setSelectedItem(e.currentTarget)

    def hasBaseData(self):
        if not self.widget:
            return False
        return True
