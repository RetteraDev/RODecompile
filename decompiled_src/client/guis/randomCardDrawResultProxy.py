#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/randomCardDrawResultProxy.o
import BigWorld
import uiConst
import events
import gamelog
import utils
import gameglobal
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis import uiUtils
from asObject import ASObject
from asObject import ASUtils
from data import random_card_draw_data as RCDD
SHOW_TYPE_ONE = 0
SHOW_TYPE_TEN = 1

class RandomCardDrawResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RandomCardDrawResultProxy, self).__init__(uiAdapter)
        self.resultList = []
        self.activityId = 0
        self.reset()

    def reset(self):
        self.widget = None
        self.showType = 0
        self.tenItemList = []
        self.callBackId = []
        self.lastSoundId = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_RANDOM_CARD_DRAW_RESULT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RANDOM_CARD_DRAW_RESULT)
        gameglobal.rds.ui.activitySaleRandomCardDraw.isShowingResult = False
        gameglobal.rds.ui.activitySaleRandomCardDraw.handleTempMsg()

    def show(self, activityId, resultList):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_RANDOM_CARD_DRAW_RESULT)
        self.resultList = resultList
        self.activityId = activityId
        self.refreshInfo()

    def initUI(self):
        gameglobal.rds.ui.activitySaleRandomCardDraw.isShowingResult = True
        self.hideAllMc()

    def hideAllMc(self):
        self.widget.oneIconMc.visible = False
        self.widget.tenIconMc.visible = False
        self.widget.cardMc.visible = False

    def refreshInfo(self):
        if not self.widget or not self.resultList:
            return
        data = RCDD.data.get(self.activityId, {})
        itemList = data.get('itemList')
        cardList = data.get('cardList')
        if len(self.resultList) == 1:
            self.showType = SHOW_TYPE_ONE
            itemId, _ = self.resultList[0]
            if itemId in itemList.keys():
                self.showItem(self.resultList[0])
                item = self.widget.oneIconMc.oneIcon
                ASUtils.callbackAtFrame(item, 95, self.afterShowReward, item)
            elif itemId in cardList.keys():
                self.showCard(self.resultList[0])
                item = self.widget.cardMc.card
                ASUtils.callbackAtFrame(item, 95, self.afterShowReward, item)
        elif len(self.resultList) == 10:
            self.showType = SHOW_TYPE_TEN
            self.showTenResult()

    def showCard(self, itemInfo):
        self.hideAllMc()
        cardMc = self.widget.cardMc
        data = RCDD.data.get(self.activityId, {})
        cardList = data.get('cardList')
        cardId, quality = cardList.get(itemInfo[0])
        cardCount = itemInfo[1]
        iconPath = 'activitySale/activityCard/%d.dds' % cardId
        cardMc.card.card.icon.fitSize = True
        cardMc.card.card.icon.loadImage(iconPath)
        if cardCount > 1:
            cardMc.card.count.txt.text = cardCount
        else:
            cardMc.card.count.txt.text = ''
        itemName = utils.getItemName(itemInfo[0])
        cardMc.card.itemName.txt.text = itemName
        cardMc.card.quality.gotoAndStop('a%d' % quality)
        ASUtils.setHitTestDisable(cardMc.card.quality, True)
        if self.showType == SHOW_TYPE_ONE:
            cardMc.card.desc.visible = False
        elif self.showType == SHOW_TYPE_TEN:
            cardMc.card.desc.visible = True
            cardMc.card.desc.txt.text = gameStrings.RANDOM_CARD_DRAW_RESULT_JUMP
        cardMc.card.gotoAndPlay(1)
        cardQualitySound = data.get('cardQualitySound', {2: 7201})
        soundId = cardQualitySound.get(quality, 7201)
        gameglobal.rds.sound.playSound(soundId)
        self.lastSoundId = soundId
        cardMc.visible = True

    def showItem(self, itemInfo):
        self.hideAllMc()
        itemMc = self.widget.oneIconMc
        data = RCDD.data.get(self.activityId, {})
        itemList = data.get('itemList')
        itemId = itemInfo[0]
        itemCount = itemInfo[1]
        _, quality = itemList.get(itemId)
        itemMc.oneIcon.item.icon.itemId = itemId
        itemMc.oneIcon.item.icon.setItemSlotData(uiUtils.getGfxItemById(itemId, itemCount))
        itemName = utils.getItemName(itemId)
        itemMc.oneIcon.itemName.txt.text = itemName
        itemMc.oneIcon.quality.gotoAndStop('a%d' % quality)
        ASUtils.setHitTestDisable(itemMc.oneIcon.quality, True)
        ASUtils.setHitTestDisable(itemMc.oneIcon.light, True)
        if self.showType == SHOW_TYPE_ONE:
            itemMc.oneIcon.desc.visible = False
        elif self.showType == SHOW_TYPE_TEN:
            itemMc.oneIcon.desc.visible = True
            itemMc.oneIcon.desc.txt.text = gameStrings.RANDOM_CARD_DRAW_RESULT_JUMP
        itemMc.oneIcon.gotoAndPlay(1)
        gameglobal.rds.sound.stopSound(self.lastSoundId)
        itemQualitySound = data.get('itemQualitySound', {2: 7201})
        soundId = itemQualitySound.get(quality, 7201)
        gameglobal.rds.sound.playSound(soundId)
        self.lastSoundId = soundId
        itemMc.visible = True

    def showTenResult(self):
        if not self.widget or not self.widget.stage:
            return
        data = RCDD.data.get(self.activityId, {})
        itemList = data.get('itemList')
        cardList = data.get('cardList')
        if self.resultList:
            self.widget.stage.addEventListener(events.MOUSE_CLICK, self.onClickNext)
            itemId, itemCount = self.resultList[0]
            if itemId in itemList.keys():
                self.showItem(self.resultList[0])
                callBackId = ASUtils.callbackAtFrame(self.widget.oneIconMc.oneIcon, 95, self.onClickNextAtResult)
                self.callBackId.append(callBackId)
            elif itemId in cardList.keys():
                self.showCard(self.resultList[0])
                callBackId = ASUtils.callbackAtFrame(self.widget.cardMc.card, 95, self.onClickNextAtResult)
                self.callBackId.append(callBackId)
            self.tenItemList.append(self.resultList[0])
            self.resultList.remove(self.resultList[0])
        else:
            self.widget.stage.removeEventListener(events.MOUSE_CLICK, self.onClickNext)
            self.hideAllMc()
            tenIconMc = self.widget.tenIconMc
            i = 0
            for itemId, itemCount in self.tenItemList:
                itemMc = getattr(tenIconMc.iconList, 'item%d' % i)
                itemMc.item.dragable = False
                itemMc.item.itemId = itemId
                itemMc.item.setItemSlotData(uiUtils.getGfxItemById(itemId, itemCount))
                if itemId in itemList.keys():
                    _, quality = itemList.get(itemId)
                elif itemId in cardList.keys():
                    _, quality = cardList.get(itemId)
                itemMc.quality.gotoAndStop('a%d' % quality)
                ASUtils.setHitTestDisable(itemMc.quality, True)
                i += 1

            self.tenItemList = []
            self.widget.tenIconMc.visible = True
            self.widget.tenIconMc.desc.txt.text = gameStrings.RANDOM_CARD_DRAW_RESULT_CLOSE
            self.widget.stage.addEventListener(events.MOUSE_CLICK, self.onHideResult)

    def afterShowReward(self, *args):
        if self.widget and self.widget.stage:
            self.widget.stage.addEventListener(events.MOUSE_CLICK, self.onHideResult)
        asObject = ASObject(args[3][0])
        item = asObject[0]
        item.desc.visible = True
        item.desc.txt.text = gameStrings.RANDOM_CARD_DRAW_RESULT_CLOSE

    def onHideResult(self, *args):
        self.widget.stage.removeEventListener(events.MOUSE_CLICK, self.onHideResult)
        self.hide()

    def onClickNext(self, *args):
        if not self.widget:
            return
        self.widget.stage.removeEventListener(events.MOUSE_CLICK, self.onClickNext)
        if self.widget.oneIconMc.visible == True:
            self.widget.oneIconMc.oneIcon.gotoAndStop(95)
        elif self.widget.cardMc.visible == True:
            self.widget.cardMc.card.gotoAndStop(95)
        gameglobal.rds.sound.stopSound(self.lastSoundId)
        self.widget.stage.addEventListener(events.MOUSE_CLICK, self.showNext)

    def onClickNextAtResult(self, *args):
        for id in reversed(self.callBackId):
            ASUtils.cancelCallBack(id)
            self.callBackId.remove(id)

        if not self.widget:
            return
        self.widget.stage.addEventListener(events.MOUSE_CLICK, self.showNext)

    def showNext(self, *args):
        if self.widget:
            self.widget.stage.removeEventListener(events.MOUSE_CLICK, self.showNext)
        self.showTenResult()
