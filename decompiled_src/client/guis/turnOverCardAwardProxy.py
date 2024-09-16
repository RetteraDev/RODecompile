#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/turnOverCardAwardProxy.o
import BigWorld
import uiConst
import gamelog
import gameglobal
import events
import math
import gametypes
import const
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASObject
from item import Item
from guis import uiUtils
from data import sys_config_data as SCD
from data import random_turn_over_card_data as RTOCD
from data import consumable_item_data as CID
from data import random_lottery_data as RLD
from data import random_card_draw_data as RCDD
from data import random_treasure_bag_lottery_data as RTBLD
ITEM_START_X = 0
ITEM_START_Y = 0
TITLE_OFFSET_Y = 30
ITEM_OFFSET_Y = 63
ITEM_NUM_PER_LINE = 6

class TurnOverCardAwardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TurnOverCardAwardProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_TURN_OVER_CARD_AWARD, self.hide)

    def reset(self):
        self.widget = None
        self.showType = -1

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_TURN_OVER_CARD_AWARD:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_TURN_OVER_CARD_AWARD)

    def show(self, showType):
        self.showType = showType
        if self.showType < 0:
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_TURN_OVER_CARD_AWARD)
        else:
            self.refreshInfo()

    def initUI(self):
        if self.showType == const.SHOW_TYPE_AWARD_QUEST_CARD or self.showType == const.SHOW_TYPE_ITEM_QUEST_CARD:
            BigWorld.player().cell.getTotalTurnOverCount()
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        turnOverCardData = RTOCD.data.get(SCD.data.get('randomTurnOverCardActivityId', 1), {})
        lotteryData = RLD.data.get(SCD.data.get('randomLotteryActivityId', gametypes.RANDOM_LOTTERY_SYSCONFIG_ID), {})
        randomCardDrawData = RCDD.data.get(SCD.data.get('randomCardDrawActivityId', 1), {})
        itemList = {}
        curCount = 0
        curCountText = gameStrings.TURN_OVER_CARD_TOTAL_TIME
        if self.showType == const.SHOW_TYPE_AWARD_QUEST_CARD:
            self.widget.title.textField.text = gameStrings.TURN_OVER_CARD_AWARD_QUEST_TITLE
            itemList = turnOverCardData.get('awardQuest', {})
            self.widget.currentCount.visible = True
            curCount = p.randomLotteryInfo.get('totalTurnOverCount', 0)
        elif self.showType == const.SHOW_TYPE_ITEM_QUEST_CARD:
            self.widget.title.textField.text = gameStrings.TURN_OVER_CARD_ITEM_QUEST_TITLE
            itemList = turnOverCardData.get('itemQuest', {})
            self.widget.currentCount.visible = False
            curCount = p.randomLotteryInfo.get('totalTurnOverCount', 0)
        elif self.showType == const.SHOW_TYPE_AWARD_QUEST_LOTTERY:
            self.widget.title.textField.text = gameStrings.TURN_OVER_CARD_AWARD_QUEST_TITLE
            itemList = lotteryData.get('awardQuest', {})
            self.widget.currentCount.visible = True
            curCount = p.randomLotteryInfo.get('totalLotteryCount', 0)
        elif self.showType == const.SHOW_TYPE_ITEM_QUEST_RANDOM_CARD_DRAW:
            self.widget.title.textField.htmlText = randomCardDrawData.get('itemQuestDesc')
            itemList = randomCardDrawData.get('itemQuest', {})
            self.widget.currentCount.visible = False
            info = p.randomCardDrawInfo.get(SCD.data.get('randomCardDrawActivityId', 1), {})
            curCount = info.get('totalCardDrawCount', 0) if info else 0
        elif self.showType == const.SHOW_TYPE_AWARD_QUEST_RANDOM_CARD_DRAW:
            self.widget.title.textField.htmlText = randomCardDrawData.get('awardQuestDesc')
            itemList = randomCardDrawData.get('awardQuest', {})
            self.widget.currentCount.visible = True
            info = p.randomCardDrawInfo.get(SCD.data.get('randomCardDrawActivityId', 1), {})
            curCount = info.get('totalCardDrawCount', 0) if info else 0
        elif self.showType == const.SHOW_TYPE_RANDOM_TREASURE_BAG_MAIN:
            self.widget.title.textField.text = gameStrings.RANDOM_TREASURE_BAG_MAIN_AWARD_QUEST_TITLE
            itemList = gameglobal.rds.ui.randomTreasureBagMain.getCurShowAwardQuestData()
            self.widget.currentCount.visible = True
            curCount = gameglobal.rds.ui.randomTreasureBagMain.curBagRoundNums
            curCountText = gameStrings.RANDOM_TREASURE_BAG_MAIN_TOTAL_ROUND
        self.widget.currentCount.text = curCountText % curCount
        self.removeAllChild(self.widget.itemPanel.canvas)
        posY = ITEM_START_Y
        for title, itemsInfo in itemList:
            titleMc = self.widget.getInstByClsName('TurnOverCardAward_title')
            self.widget.itemPanel.canvas.addChild(titleMc)
            titleMc.textField.text = title
            titleMc.x = ITEM_START_X
            titleMc.y = posY
            posY += TITLE_OFFSET_Y
            itemNum = len(itemsInfo)
            groupNum = int(math.ceil(float(itemNum) / ITEM_NUM_PER_LINE))
            currentItemIndex = 0
            for i in xrange(groupNum):
                groupItemMc = self.widget.getInstByClsName('TurnOverCardAward_items')
                self.widget.itemPanel.canvas.addChild(groupItemMc)
                groupItemMc.x = ITEM_START_X
                groupItemMc.y = posY
                posY += ITEM_OFFSET_Y
                for i in xrange(ITEM_NUM_PER_LINE):
                    itemMc = getattr(groupItemMc, 'item%d' % i)
                    if currentItemIndex < itemNum:
                        item = itemsInfo[currentItemIndex]
                        itemMc.visible = True
                        itemMc.dragable = False
                        itemMc.itemId = item[0]
                        itemMc.itemCount = item[1]
                        itemMc.setItemSlotData(uiUtils.getGfxItemById(item[0], item[1]))
                        itemMc.addEventListener(events.MOUSE_CLICK, self.handleShowFit, False, 0, True)
                    else:
                        itemMc.visible = False
                    currentItemIndex += 1

    def handleShowFit(self, *args):
        e = ASObject(args[3][0])
        itemId = int(e.currentTarget.itemId)
        if e.buttonIdx == uiConst.LEFT_BUTTON:
            cidData = CID.data.get(itemId, {})
            sType = cidData.get('sType', 0)
            if sType == Item.SUBTYPE_2_GET_SELECT_ITEM:
                gameglobal.rds.ui.itemChoose.show(itemId, showType=0)
            else:
                self.uiAdapter.fittingRoom.addItem(Item(itemId))

    def removeAllChild(self, canvasMc):
        while canvasMc.numChildren > 0:
            canvasMc.removeChildAt(0)
