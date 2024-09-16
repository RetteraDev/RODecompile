#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleRandomCardDrawProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
import events
import gamelog
import clientUtils
import const
import gametypes
from uiProxy import UIProxy
from guis import ui
from gamestrings import gameStrings
from callbackHelper import Functor
from data import sys_config_data as SCD
from data import random_card_draw_data as RCDD
from cdata import game_msg_def_data as GMDD
DRAW_TPYE_BIND = 1
DRAW_TPYE_UNBIND = 2

class ActivitySaleRandomCardDrawProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleRandomCardDrawProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.widget = None
        self.timer = None
        self.totalCardDrawCount = 0
        self.canReceiveAward = False
        self.randomCardDrawInfo = {}
        self.isDiscount = True
        self.tempMsgList = []
        self.tempItemList = []
        self.isShowingResult = False
        gameglobal.rds.ui.messageBox.checkOnceMap[uiConst.CHECK_ONCE_TYPE_RANDOM_CARD_DRAW_BIND] = False
        gameglobal.rds.ui.messageBox.checkOnceMap[uiConst.CHECK_ONCE_TYPE_RANDOM_CARD_DRAW_UNBIND] = False
        gameglobal.rds.ui.messageBox.checkOnceMap[uiConst.CHECK_ONCE_TYPE_RANDOM_CARD_DRAW_TEN] = False

    def initRandomCardDraw(self, widget):
        self.widget = widget
        activityId = SCD.data.get('randomCardDrawActivityId', 1)
        p = BigWorld.player()
        p.cell.getRandomCardDrawInfo(activityId)
        p.cell.getTotalCardDrawCount(activityId)
        self.delTimer()
        self.initUI()

    def initUI(self):
        if not self.widget:
            return
        data = RCDD.data.get(SCD.data.get('randomCardDrawActivityId', 1), {})
        bgPath = data.get('bgPath', 'activitySale/randomCardDrawBg.dds')
        self.widget.bgImage.loadImage(bgPath)
        self.widget.awardBtn.addEventListener(events.BUTTON_CLICK, self.handleClickAwardQuest, False, 0, True)
        self.widget.awardBtn.desc.addEventListener(events.MOUSE_CLICK, self.handleClickAwardQuest, False, 0, True)
        self.widget.awardBtn.desc.htmlText = data.get('awardQuestDesc')
        self.widget.detailBtn.addEventListener(events.BUTTON_CLICK, self.handleClickItemQuest, False, 0, True)
        self.widget.detailBtn.desc.addEventListener(events.MOUSE_CLICK, self.handleClickItemQuest, False, 0, True)
        self.widget.detailBtn.desc.htmlText = data.get('itemQuestDesc')
        self.widget.shopBtn.addEventListener(events.BUTTON_CLICK, self.handleClickShopBtn, False, 0, True)
        self.widget.shopBtn.desc.addEventListener(events.MOUSE_CLICK, self.handleClickShopBtn, False, 0, True)
        self.widget.shopBtn.desc.htmlText = data.get('shopDesc')
        self.widget.bindOnce.btn.addEventListener(events.BUTTON_CLICK, self.handleClickBindOnceBtn, False, 0, True)
        self.widget.bindOnce.desc.moneyIcon.bonusType = data.get('bindTicketIcon', 'choujiang')
        self.widget.bindOnce.desc.numTxt.text = 1
        self.widget.unBindOnce.btn.addEventListener(events.BUTTON_CLICK, self.handleClickUnBindOnceBtn, False, 0, True)
        self.widget.unBindOnce.desc.moneyIcon.bonusType = data.get('ticketIcon', 'choujiang')
        self.widget.unBindOnce.desc.numTxt.text = 1
        self.widget.unBindTen.btn.addEventListener(events.BUTTON_CLICK, self.handleClickUnBindTenBtn, False, 0, True)
        self.widget.unBindTen.desc.moneyIcon.bonusType = data.get('ticketIcon', 'choujiang')
        self.widget.unBindTen.desc.numTxt.text = ''
        discountOp = data.get('discountOp', 0)
        discount = data.get('discount', 1)
        if discountOp == gametypes.RANDOM_CARD_DRAW_DISCOUNT_BY_DAY:
            self.widget.discountDesc.text = gameStrings.RANDOM_CARD_DRAW_DISCOUNT_DESC_DAY % (10 * discount)
        elif discountOp == gametypes.RANDOM_CARD_DRAW_DISCOUNT_BY_WEEK:
            self.widget.discountDesc.text = gameStrings.RANDOM_CARD_DRAW_DISCOUNT_DESC_WEEK % (10 * discount)
        elif discountOp == gametypes.RANDOM_CARD_DRAW_DISCOUNT_BY_ACTIVITY:
            self.widget.discountDesc.text = gameStrings.RANDOM_CARD_DRAW_DISCOUNT_DESC_ACTIVITY % (10 * discount)
        self.widget.bottom.addBtn.addEventListener(events.BUTTON_CLICK, self.handleClickaddBtn, False, 0, True)
        self.widget.bottom.rechargeBtn.addEventListener(events.BUTTON_CLICK, self.handleClickRechargeBtn, False, 0, True)
        BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.refreshCoin)
        BigWorld.player().registerEvent(const.EVENT_ITEM_REMOVE, self.refreshCoin)
        self.widget.bottom.moneyIcon.bonusType = 'tianBi'
        self.widget.bottom.bindConsumeItem.bonusType = data.get('bindTicketIcon', 'choujiang')
        self.widget.bottom.consumeItemIcon.bonusType = data.get('ticketIcon', 'choujiang')
        self.addEvent(events.EVENT_TIANBI_COIN_CHANGED, self.refreshCoin)
        self.refreshCoin()
        self.timerFunc()
        self.addTimer()

    def onSetRandomCardDrawInfo(self):
        self.refreshPanel()

    def refreshPanel(self):
        if not self.widget:
            return
        self.refreshCoin()
        activityId = SCD.data.get('randomCardDrawActivityId', 1)
        data = RCDD.data.get(activityId, {})
        self.widget.awardBtn.visible = data.get('totalRandomTurnOverCardRewardOp', 0)
        self.widget.progressTxt.visible = data.get('totalRandomTurnOverCardRewardOp', 0)
        self.randomCardDrawInfo = BigWorld.player().randomCardDrawInfo.get(activityId, {})
        finishRewardMargins = self.randomCardDrawInfo.get('finishRewardMargins', {})
        self.totalCount = self.randomCardDrawInfo.get('totalCardDrawCount', 0)
        baseMargins = data.get('baseMargins', ())
        loopMargin = data.get('loopMargin', 0)
        baseMarginEnd = baseMargins[-1]
        finishRewardLoopMargin = finishRewardMargins.get('finishRewardLoopMargin', 0)
        if finishRewardLoopMargin:
            leftTimes = self.totalCount - finishRewardLoopMargin
            self.widget.progressTxt.text = gameStrings.RANDOM_CARD_DRAW_CURRENT_SCHEDUAL % (self.totalCount, finishRewardLoopMargin + loopMargin)
            self.canReceiveAward = leftTimes >= loopMargin and self.totalCount <= data.get('maxNum', 100000)
        elif self.totalCount >= baseMarginEnd and baseMarginEnd in finishRewardMargins.keys():
            leftTimes = self.totalCount - baseMarginEnd
            self.widget.progressTxt.text = gameStrings.RANDOM_CARD_DRAW_CURRENT_SCHEDUAL % (self.totalCount, baseMarginEnd + loopMargin)
            self.canReceiveAward = leftTimes >= loopMargin
        else:
            index = 0
            currentMargin = baseMargins[index]
            for baseMargin in baseMargins:
                if baseMargin not in finishRewardMargins.keys():
                    currentMargin = baseMargin
                    break

            self.widget.progressTxt.text = gameStrings.RANDOM_CARD_DRAW_CURRENT_SCHEDUAL % (self.totalCount, currentMargin)
            self.canReceiveAward = self.totalCount >= currentMargin
        discountOp = data.get('discountOp', 0)
        discountTime = self.randomCardDrawInfo.get('discountTime', 0)
        if not discountTime:
            self.isDiscount = True
        elif discountOp == gametypes.RANDOM_CARD_DRAW_DISCOUNT_BY_DAY:
            if utils.isSameDay(utils.getNow(), discountTime):
                self.isDiscount = False
        elif discountOp == gametypes.RANDOM_CARD_DRAW_DISCOUNT_BY_WEEK:
            if utils.isSameWeek(utils.getNow(), discountTime):
                self.isDiscount = False
        elif discountOp == gametypes.RANDOM_CARD_DRAW_DISCOUNT_BY_ACTIVITY:
            beginTime = data.get('crontabStart', '')
            endTime = data.get('crontabEnd', '')
            if utils.getDisposableCronTabTimeStamp(beginTime) <= discountTime <= utils.getDisposableCronTabTimeStamp(endTime):
                self.isDiscount = False
        self.widget.discountDesc.visible = self.isDiscount
        discount = data.get('discount', 1) if self.isDiscount else 1
        self.widget.unBindTen.desc.numTxt.text = 10 * discount
        gameglobal.rds.ui.activitySale.refreshInfo()

    def unRegisterRandomCardDraw(self):
        self.delTimer()
        self.delEvent(events.EVENT_TIANBI_COIN_CHANGED, self.refreshCoin)
        p = BigWorld.player()
        if p:
            p.unRegisterEvent(const.EVENT_ITEM_CHANGE, self.refreshCoin)
            p.unRegisterEvent(const.EVENT_ITEM_REMOVE, self.refreshCoin)
            self.handleTempMsg()
        self.reset()

    def handleClickRechargeBtn(self, *args):
        self.uiAdapter.tianyuMall.onOpenChargeWindow()

    def handleClickaddBtn(self, *args):
        data = RCDD.data.get(SCD.data.get('randomCardDrawActivityId', 1), {})
        mallName = data.get('mallName', '')
        if mallName:
            gameglobal.rds.ui.tianyuMall.show(keyWord=mallName)

    def handleClickAwardQuest(self, *args):
        gameglobal.rds.ui.turnOverCardAward.show(const.SHOW_TYPE_AWARD_QUEST_RANDOM_CARD_DRAW)

    def handleClickItemQuest(self, *args):
        gameglobal.rds.ui.turnOverCardAward.show(const.SHOW_TYPE_ITEM_QUEST_RANDOM_CARD_DRAW)

    def handleClickShopBtn(self, *args):
        self.uiAdapter.compositeShop.closeShop()
        data = RCDD.data.get(SCD.data.get('randomCardDrawActivityId', 1), {})
        shopId = data.get('shopId', 10361)
        BigWorld.player().base.openPrivateShop(0, shopId)

    def handleClickBindOnceBtn(self, *args):
        p = BigWorld.player()
        activityId = SCD.data.get('randomCardDrawActivityId', 1)
        data = RCDD.data.get(activityId, {})
        consumeBindItemIds = data.get('consumeBindItemIds', (411415,))
        consumeBindItemNum = self.calItemNum(consumeBindItemIds)
        bindTicketIcon = data.get('bindTicketIcon', 'zhenhunjie')
        fixedIcon = data.get('fixedIcon', 'gift')
        fixedBonusId = data.get('fixedBindBonusId', 18688)
        fixedItemNum = clientUtils.genItemBonus(fixedBonusId)[0][1]
        if consumeBindItemNum > 0:
            msg = gameStrings.RANDOM_CARD_DRAW_MSG_BIND_ONCE % (bindTicketIcon, fixedIcon, fixedItemNum)
            if not gameglobal.rds.ui.messageBox.checkOnceMap.get(uiConst.CHECK_ONCE_TYPE_RANDOM_CARD_DRAW_BIND, False):
                gameglobal.rds.ui.messageBox.showRichTextMsgBox(msg, yesCallback=Functor(self.randomCardDrawRequest, activityId, DRAW_TPYE_BIND, 1), checkOnceType=uiConst.CHECK_ONCE_TYPE_RANDOM_CARD_DRAW_BIND)
            else:
                self.randomCardDrawRequest(activityId, DRAW_TPYE_BIND, 1)
        else:
            p.showGameMsg(GMDD.data.RANDOM_CARD_DRAW_FAILED_BY_CONSUME_ITEM_NOT_ENOUGH, ())

    def handleClickUnBindOnceBtn(self, *args):
        p = BigWorld.player()
        activityId = SCD.data.get('randomCardDrawActivityId', 1)
        data = RCDD.data.get(activityId, {})
        consumeItemIds = data.get('consumeItemIds', (411415,))
        consumeItemNum = self.calItemNum(consumeItemIds)
        ticketIcon = data.get('ticketIcon', 'zhenhunjie')
        fixedIcon = data.get('fixedIcon', 'gift')
        consumeCoins = data.get('consumeCoins', 28)
        fixedBonusId = data.get('fixedBonusId', 18687)
        fixedItemNum = clientUtils.genItemBonus(fixedBonusId)[0][1]
        if consumeItemNum > 0:
            msg = gameStrings.RANDOM_CARD_DRAW_MSG_UNBIND_ONCE_ITEM % (ticketIcon, fixedIcon, fixedItemNum)
        else:
            msg = gameStrings.RANDOM_CARD_DRAW_MSG_UNBIND_ONCE_COIN % (consumeCoins, fixedIcon, fixedItemNum)
        if not gameglobal.rds.ui.messageBox.checkOnceMap.get(uiConst.CHECK_ONCE_TYPE_RANDOM_CARD_DRAW_UNBIND, False):
            gameglobal.rds.ui.messageBox.showRichTextMsgBox(msg, yesCallback=Functor(self.randomCardDrawRequest, activityId, DRAW_TPYE_UNBIND, 1), checkOnceType=uiConst.CHECK_ONCE_TYPE_RANDOM_CARD_DRAW_UNBIND)
        else:
            self.randomCardDrawRequest(activityId, DRAW_TPYE_UNBIND, 1)

    def handleClickUnBindTenBtn(self, *args):
        p = BigWorld.player()
        activityId = SCD.data.get('randomCardDrawActivityId', 1)
        data = RCDD.data.get(activityId, {})
        consumeItemIds = data.get('consumeItemIds', (411415,))
        consumeItemNum = self.calItemNum(consumeItemIds)
        discount = data.get('discount', 1) if self.isDiscount else 1
        consumeCoins = data.get('consumeCoins', 28)
        fixedBonusId = data.get('fixedBonusId', 18687)
        ticketIcon = data.get('ticketIcon', 'zhenhunjie')
        fixedIcon = data.get('fixedIcon', 'gift')
        fixedItemNum = clientUtils.genItemBonus(fixedBonusId)[0][1]
        if consumeItemNum == 0:
            leftCoin = (10 * discount - consumeItemNum) * consumeCoins
            if self.isDiscount:
                msg = gameStrings.RANDOM_CARD_DRAW_MSG_UNBIND_TEN_COIN_DISCOUNT % (leftCoin,
                 10 * consumeCoins,
                 fixedIcon,
                 fixedItemNum * 10)
            else:
                msg = gameStrings.RANDOM_CARD_DRAW_MSG_UNBIND_TEN_COIN % (leftCoin, fixedIcon, fixedItemNum * 10)
        elif consumeItemNum < 10 * discount:
            leftCoin = (10 * discount - consumeItemNum) * consumeCoins
            msg = gameStrings.RANDOM_CARD_DRAW_MSG_UNBIND_TEN_ITEM_COIN % (ticketIcon,
             consumeItemNum,
             leftCoin,
             fixedIcon,
             fixedItemNum * 10)
        else:
            msg = gameStrings.RANDOM_CARD_DRAW_MSG_UNBIND_TEN_ITEM % (ticketIcon,
             10 * discount,
             fixedIcon,
             fixedItemNum * 10)
        if not gameglobal.rds.ui.messageBox.checkOnceMap.get(uiConst.CHECK_ONCE_TYPE_RANDOM_CARD_DRAW_TEN, False):
            gameglobal.rds.ui.messageBox.showRichTextMsgBox(msg, yesCallback=Functor(self.randomCardDrawRequest, activityId, DRAW_TPYE_UNBIND, 10), checkOnceType=uiConst.CHECK_ONCE_TYPE_RANDOM_CARD_DRAW_TEN)
        else:
            self.randomCardDrawRequest(activityId, DRAW_TPYE_UNBIND, 10)

    @ui.callFilter(2.5)
    @ui.checkInventoryLock()
    def randomCardDrawRequest(self, activityId, countType, count):
        p = BigWorld.player()
        p.cell.randomCardDrawRequest(activityId, countType, count, p.cipherOfPerson)

    def setCardDrawMsg(self, msgId, data):
        tempMsg = (msgId, data)
        self.tempMsgList.append(tempMsg)

    def setCardDrawItem(self, kind, item, page, pos):
        tempItem = (kind,
         item,
         page,
         pos)
        self.tempItemList.append(tempItem)

    def handleTempMsg(self):
        p = BigWorld.player()
        if not p:
            return
        for msg in self.tempMsgList:
            p.showGameMsg(msg[0], msg[1])

        for item in self.tempItemList:
            p.resInsert(item[0], item[1], item[2], item[3])

        self.tempMsgList = []
        self.tempItemList = []

    def canOpen(self):
        flag = False
        if not gameglobal.rds.configData.get('enableRandomCardDraw', False):
            return flag
        data = RCDD.data.get(SCD.data.get('randomCardDrawActivityId', 1), {})
        if not data:
            return
        beginTime = data.get('crontabStart', '')
        endTime = data.get('crontabEnd', '')
        if beginTime and endTime and utils.getDisposableCronTabTimeStamp(beginTime) <= utils.getNow() < utils.getDisposableCronTabTimeStamp(endTime):
            flag = True
        return flag

    def getRedPointVisible(self):
        return self.canReceiveAward

    def refreshCoin(self, *args):
        if not self.widget or not self.widget.bottom:
            return
        p = BigWorld.player()
        tianbi = format(p.unbindCoin + p.bindCoin + p.freeCoin, ',')
        self.widget.bottom.moneyTxt.htmlText = '%s' % tianbi
        data = RCDD.data.get(SCD.data.get('randomCardDrawActivityId', 1), {})
        consumeItemIds = data.get('consumeItemIds', (411415,))
        consumeItemNum = self.calItemNum(consumeItemIds)
        consumeBindItemIds = data.get('consumeBindItemIds', (411415,))
        consumeBindItemNum = self.calItemNum(consumeBindItemIds)
        self.widget.bottom.bindConsumeItemNum.text = consumeBindItemNum
        self.widget.bottom.consumeItemNum.text = consumeItemNum

    def calItemNum(self, itemIds):
        itemTotalNum = 0
        for itemId in itemIds:
            itemNum = BigWorld.player().inv.countItemInPages(itemId)
            itemTotalNum += itemNum

        return itemTotalNum

    def addTimer(self):
        if not self.timer:
            self.timer = BigWorld.callback(1, self.timerFunc, -1)

    def timerFunc(self):
        if not self.widget:
            self.delTimer()
            return
        data = RCDD.data.get(SCD.data.get('randomCardDrawActivityId', 1), {})
        endTime = data.get('crontabEnd', '')
        left = 0
        if utils.getDisposableCronTabTimeStamp(endTime) >= utils.getNow():
            left = utils.getDisposableCronTabTimeStamp(endTime) - utils.getNow()
        self.widget.bottom.leftTimeTxt.text = utils.formatDurationShortVersion(left)
        if left <= 0:
            gameglobal.rds.ui.activitySale.refreshInfo()

    def delTimer(self):
        self.timer and BigWorld.cancelCallback(self.timer)
        self.timer = None

    def pushRandomCardDrawMessage(self):
        if BigWorld.player().lv < SCD.data.get('activitySaleMinLv', 0):
            return
        data = RCDD.data.get(SCD.data.get('randomCardDrawActivityId', 1), {})
        pushId = data.get('pushId', uiConst.MESSAGE_TYPE_RANDOM_CARD_DRAW)
        if pushId not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(pushId)
            gameglobal.rds.ui.pushMessage.setCallBack(pushId, {'click': self.onPushMsgClick})

    def removeRandomCardDrawPushMsg(self):
        data = RCDD.data.get(SCD.data.get('randomCardDrawActivityId', 1), {})
        pushId = data.get('pushId', uiConst.MESSAGE_TYPE_RANDOM_CARD_DRAW)
        if pushId in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(pushId)

    def onPushMsgClick(self):
        if not self.widget:
            gameglobal.rds.ui.activitySale.show(uiConst.ACTIVITY_SALE_TAB_RANDOM_CARD_DRAW)
        self.removeRandomCardDrawPushMsg()
