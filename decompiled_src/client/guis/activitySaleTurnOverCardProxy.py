#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleTurnOverCardProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import utils
import events
import gamelog
import random
import clientUtils
import const
from uiProxy import UIProxy
from guis import ui
from guis import uiUtils
from guis.asObject import ASObject
from asObject import ASUtils
from gamestrings import gameStrings
from callbackHelper import Functor
from data import sys_config_data as SCD
from data import random_turn_over_card_data as RTOCD
TURN_OVER_TYPE_FIX = 1
TURN_OVER_TYPE_RANDOM = 2
MAX_ITEM_NUM = 50

class ActivitySaleTurnOverCardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleTurnOverCardProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.widget = None
        self.timer = None
        self.totalTurnOverCount = 0
        self.pos = 0
        self.specialRewards = []
        self.imageIndex = 0
        self.newItemList = []
        gameglobal.rds.ui.messageBox.checkOnceMap[uiConst.CHECK_ONCE_TYPE_TURN_OVER_CARD_USE_COIN] = False

    def initTurnOverCard(self, widget):
        self.widget = widget
        p = BigWorld.player()
        p.cell.getTotalTurnOverCount()
        p.cell.getRandomTurnOverCardInfo()
        self.delTimer()
        self.initUI()

    def initUI(self):
        if not self.widget:
            return
        data = RTOCD.data.get(SCD.data.get('randomTurnOverCardActivityId', 1), {})
        self.widget.award.item.slot.dragable = False
        self.widget.award.awardQuest.addEventListener(events.MOUSE_CLICK, self.handleClickAwardQuest, False, 0, True)
        self.widget.award.awardQuest.textField.htmlText = data.get('awardQuestDesc', gameStrings.TURN_OVER_CARD_AWARD_QUEST_TITLE)
        self.widget.award.item.addEventListener(events.MOUSE_CLICK, self.handleClickAward, False, 0, True)
        self.widget.refreshBtn.addEventListener(events.BUTTON_CLICK, self.handleClickRefreshBtn, False, 0, True)
        self.widget.itemQuest.addEventListener(events.MOUSE_CLICK, self.handleClickItemQuest, False, 0, True)
        self.widget.itemQuest.textField.htmlText = data.get('itemQuestDesc', gameStrings.TURN_OVER_CARD_AWARD_QUEST_TITLE)
        self.widget.lotteryBtn.addEventListener(events.BUTTON_CLICK, self.handleClickLotteryBtn, False, 0, True)
        self.widget.addBtn.addEventListener(events.BUTTON_CLICK, self.handleClickaddBtn, False, 0, True)
        self.widget.rechargeBtn.addEventListener(events.BUTTON_CLICK, self.handleClickRechargeBtn, False, 0, True)
        BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.itemChange)
        BigWorld.player().registerEvent(const.EVENT_ITEM_REMOVE, self.itemChange)
        self.widget.cardCounter.count = 1
        self.widget.moneyIcon.bonusType = 'tianBi'
        self.widget.daojuIcon.bonusType = data.get('ticketIcon', 'choujiang')
        self.widget.itemIcon.bonusType = data.get('fixedIcon', 'zhounian')
        self.widget.consumeItemIcon.bonusType = data.get('ticketIcon', 'choujiang')
        self.addEvent(events.EVENT_TIANBI_COIN_CHANGED, self.refreshCoin)
        self.refreshCardCounter()
        self.refreshBtnCountDown(0)
        self.timerFunc()
        self.addTimer()

    def refreshPanel(self):
        if not self.widget:
            return
        data = RTOCD.data.get(SCD.data.get('randomTurnOverCardActivityId', 1), {})
        randomTurnOverCardInfo = BigWorld.player().randomTurnOverCardInfo
        randomTurnOverPosInfo = randomTurnOverCardInfo.get('randomTurnOverPosInfo', {})
        for pos, itemInfo in randomTurnOverPosInfo.iteritems():
            item = self.widget.getChildByName('item%d' % pos)
            if itemInfo:
                itemId = itemInfo.keys()[0]
                item.item.slot.itemId = itemInfo.keys()[0]
                item.item.slot.dragable = False
                item.item.slot.setItemSlotData(uiUtils.getGfxItemById(itemInfo.keys()[0], itemInfo.values()[0]))
                item.removeEventListener(events.BUTTON_CLICK, self.handleClickItem)
                if item.state == 'close':
                    item.state = 'open'
                    item.gotoAndStop(14)
                    item.item.newIcon.visible = item in self.newItemList
                if itemId in data.get('rareItems', []):
                    item.item.rare.visible = True
                    item.item.bling.visible = True
                    item.item.quality.gotoAndStop('xiyou')
                    item.item.rareIcon.visible = True
                else:
                    item.item.rare.visible = False
                    item.item.bling.visible = False
                    item.item.quality.gotoAndStop('putong')
                    item.item.rareIcon.visible = False

    def loadImage(self, imageIndex):
        self.widget.bgImage.loadImage('activitySale/activitysaleturnovercard/%s/bg.dds' % imageIndex)
        for i in xrange(MAX_ITEM_NUM):
            iconPath = 'activitySale/activitysaleturnovercard/%s/%s-%s.dds' % (imageIndex, imageIndex, str(i + 1))
            item = self.widget.getChildByName('item%d' % i)
            item.image.icon.loadImage(iconPath)
            item.image.icon.fitSize = True
            item.pos = i
            item.state = 'close'
            item.gotoAndStop(1)
            item.addEventListener(events.BUTTON_CLICK, self.handleClickItem, False, 0, True)

    def getImage(self):
        imageProbability = RTOCD.data.get(SCD.data.get('randomTurnOverCardActivityId', 1), {}).get('imageProbability', {})
        if imageProbability:
            x = int(random.uniform(0, 10000))
            curProb = 0
            for imageId, probability in imageProbability.iteritems():
                curProb += probability
                if x < curProb:
                    break

            return imageId

    def refreshAward(self):
        if not self.widget or not self.widget.award:
            return
        data = RTOCD.data.get(SCD.data.get('randomTurnOverCardActivityId', 1), {})
        self.widget.award.visible = data.get('totalRandomTurnOverCardRewardOp', 0)
        randomTurnOverCardInfo = BigWorld.player().randomTurnOverCardInfo
        finishRewardMargins = randomTurnOverCardInfo.get('finishRewardMargins', {})
        self.totalTurnOverCount = randomTurnOverCardInfo.get('totalTurnOverCount', 0)
        baseBonusIds = data.get('baseBonusIds', ())
        baseMargins = data.get('baseMargins', ())
        loopMargin = data.get('loopMargin', 0)
        loopBonus = data.get('loopBonusId', 0)
        loopBonus = clientUtils.genItemBonus(loopBonus)
        loopBonusId = loopBonus[0][0]
        loopBonusCount = loopBonus[0][1]
        baseMarginEnd = baseMargins[-1]
        finishRewardLoopMargin = finishRewardMargins.get('finishRewardLoopMargin', 0)
        if finishRewardLoopMargin:
            leftTimes = self.totalTurnOverCount - finishRewardLoopMargin
            self.widget.award.item.slot.itemId = loopBonusId
            self.widget.award.item.slot.setItemSlotData(uiUtils.getGfxItemById(loopBonusId, loopBonusCount))
            self.widget.award.progressBar.maxValue = loopMargin
            self.widget.award.progressBar.currentValue = leftTimes
            canReceive = leftTimes >= loopMargin and self.totalTurnOverCount <= data.get('maxNum', 100000)
        elif self.totalTurnOverCount >= baseMarginEnd and baseMarginEnd in finishRewardMargins.keys():
            leftTimes = self.totalTurnOverCount - baseMarginEnd
            self.widget.award.item.slot.itemId = loopBonusId
            self.widget.award.item.slot.setItemSlotData(uiUtils.getGfxItemById(loopBonusId, loopBonusCount))
            self.widget.award.progressBar.maxValue = loopMargin
            self.widget.award.progressBar.currentValue = leftTimes
            canReceive = leftTimes >= loopMargin
        else:
            index = 0
            lastMargin = 0
            currentMargin = baseMargins[index]
            for baseMargin in baseMargins:
                if baseMargin not in finishRewardMargins.keys():
                    currentMargin = baseMargin
                    index = baseMargins.index(baseMargin)
                    break
                index = -1
                currentMargin = baseMargins[index]

            if index > 0:
                lastMargin = baseMargins[index - 1]
            baseBonus = baseBonusIds[index]
            itemBonus = clientUtils.genItemBonus(baseBonus)
            baseBonusId = itemBonus[0][0]
            baseBonusCount = itemBonus[0][1]
            self.widget.award.item.slot.itemId = baseBonusId
            self.widget.award.item.slot.setItemSlotData(uiUtils.getGfxItemById(baseBonusId, baseBonusCount))
            self.widget.award.progressBar.maxValue = currentMargin - lastMargin
            self.widget.award.progressBar.currentValue = self.totalTurnOverCount - lastMargin
            canReceive = self.totalTurnOverCount >= currentMargin
        self.widget.award.item.canReceive.visible = canReceive
        gameglobal.rds.ui.activitySale.refreshInfo()

    def unRegisterTurnOverCard(self):
        self.delTimer()
        self.delEvent(events.EVENT_TIANBI_COIN_CHANGED, self.refreshCoin)
        BigWorld.player().unRegisterEvent(const.EVENT_ITEM_CHANGE, self.itemChange)
        BigWorld.player().unRegisterEvent(const.EVENT_ITEM_REMOVE, self.itemChange)
        self.onHideRareItem()
        self.resetItemState()
        self.reset()

    def resetItemState(self):
        for i in xrange(MAX_ITEM_NUM):
            item = self.widget.getChildByName('item%d' % i)
            item.state = 'close'
            item.gotoAndStop(1)

    def onSetRandomTurnOverCardInfo(self):
        if not self.widget:
            return
        self.refreshAward()
        self.refreshCoin()
        randomTurnOverCardInfo = BigWorld.player().randomTurnOverCardInfo
        randomTurnOverPosInfo = randomTurnOverCardInfo.get('randomTurnOverPosInfo', {})
        imageIndex = randomTurnOverCardInfo.get('imageIndex', 0)
        if not imageIndex:
            self.imageIndex = self.getImage()
            BigWorld.player().cell.randomTurnOverPosInfoRefresh(self.imageIndex)
            self.loadImage(self.imageIndex)
            self.refreshPanel()
        elif randomTurnOverPosInfo:
            self.imageIndex = imageIndex
            self.loadImage(self.imageIndex)
            self.refreshPanel()
        else:
            self.imageIndex = randomTurnOverCardInfo.get('imageIndex')
            self.resetItemState()
            self.refreshCardCounter()
            self.loadImage(self.imageIndex)
        lastTurnOverCount = randomTurnOverCardInfo.get('randomTurnOverCountEveryTime', 0)
        self.widget.cardCounter.count = lastTurnOverCount

    def handleClickRechargeBtn(self, *args):
        self.uiAdapter.tianyuMall.onOpenChargeWindow()

    def handleClickRefreshBtn(self, *args):
        msg = gameStrings.TURN_OVER_CARD_RESET_CARD
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.refreshCard, isModal=True)

    def refreshCard(self):
        imageIndex = self.getImage()
        BigWorld.player().cell.randomTurnOverPosInfoRefresh(imageIndex)
        self.refreshBtnCountDown(4)

    def refreshBtnCountDown(self, leftTime):
        if not self.widget:
            return
        if leftTime > 0:
            leftTime -= 1
            self.widget.refreshBtn.disabled = True
            self.widget.refreshBtn.label = gameStrings.TEXT_ACTIVITYSALETURNOVERCARDPROXY_262 % leftTime
            BigWorld.callback(1, Functor(self.refreshBtnCountDown, leftTime))
        if leftTime <= 0:
            self.widget.refreshBtn.disabled = False
            self.widget.refreshBtn.label = gameStrings.TURN_OVER_CARD_RESET_BTN_DESC

    def handleClickLotteryBtn(self, *args):
        data = RTOCD.data.get(SCD.data.get('randomTurnOverCardActivityId', 1), {})
        turnOverNum = int(self.widget.cardCounter.count)
        type = TURN_OVER_TYPE_RANDOM
        pos = 0
        if self.calConsumeItemTotalNum():
            BigWorld.player().cell.randomTurnOverCardRequest(type, turnOverNum, 0)
        elif not gameglobal.rds.ui.messageBox.checkOnceMap.get(uiConst.CHECK_ONCE_TYPE_TURN_OVER_CARD_USE_COIN, False):
            msg = gameStrings.TURN_OVER_CARD_FAILED_CONSUME_ITEM_NOT_ENOUGH % data.get('consumeCoins', 28)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.useCoinConfirm, type, turnOverNum, pos), isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_TURN_OVER_CARD_USE_COIN)
        else:
            self.useCoinConfirm(type, turnOverNum, pos)

    def handleClickaddBtn(self, *args):
        data = RTOCD.data.get(SCD.data.get('randomTurnOverCardActivityId', 1), {})
        mallName = data.get('mallName', '')
        if mallName:
            gameglobal.rds.ui.tianyuMall.show(keyWord=mallName)

    def handleClickAward(self, *args):
        BigWorld.player().cell.receiveRandomTurnOverCardTotalReward()
        BigWorld.player().cell.getTotalTurnOverCount()

    def handleClickAwardQuest(self, *args):
        gameglobal.rds.ui.turnOverCardAward.show(const.SHOW_TYPE_AWARD_QUEST_CARD)

    def handleClickItemQuest(self, *args):
        gameglobal.rds.ui.turnOverCardAward.show(const.SHOW_TYPE_ITEM_QUEST_CARD)

    def handleClickItem(self, *args):
        target = ASObject(args[3][0]).currentTarget
        pos = int(target.pos)
        turnOverNum = 1
        data = RTOCD.data.get(SCD.data.get('randomTurnOverCardActivityId', 1), {})
        type = TURN_OVER_TYPE_FIX
        if self.calConsumeItemTotalNum():
            BigWorld.player().cell.randomTurnOverCardRequest(type, 1, pos)
        elif not gameglobal.rds.ui.messageBox.checkOnceMap.get(uiConst.CHECK_ONCE_TYPE_TURN_OVER_CARD_USE_COIN, False):
            msg = gameStrings.TURN_OVER_CARD_FAILED_CONSUME_ITEM_NOT_ENOUGH % data.get('consumeCoins', 28)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.useCoinConfirm, type, turnOverNum, pos), isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_TURN_OVER_CARD_USE_COIN)
        else:
            self.useCoinConfirm(type, turnOverNum, pos)

    def onRandomTurnOverCardRequest(self, posInfo):
        if not self.widget:
            return
        data = RTOCD.data.get(SCD.data.get('randomTurnOverCardActivityId', 1), {})
        self.specialRewards = []
        self.newItemList = []
        for pos, itemInfo in posInfo.iteritems():
            if itemInfo:
                item = self.widget.getChildByName('item%d' % pos)
                itemId = itemInfo.keys()[0]
                item.item.slot.itemId = itemId
                item.item.slot.dragable = False
                item.item.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, itemInfo.values()[0]))
                item.removeEventListener(events.BUTTON_CLICK, self.handleClickItem)
                if item.state == 'close':
                    item.play()
                    item.state = 'open'
                    self.newItemList.append(item)
                    if itemId in data.get('rareItems', []):
                        item.item.rare.visible = True
                        item.item.bling.visible = True
                        item.item.quality.gotoAndStop('xiyou')
                        item.item.rareIcon.visible = True
                        self.specialRewards.append(itemId)
                    else:
                        item.item.rare.visible = False
                        item.item.bling.visible = False
                        item.item.rareIcon.visible = False
                        item.item.quality.gotoAndStop('putong')

        if self.specialRewards:
            itemId = self.specialRewards[0]
            self.openRareItem(itemId)
        BigWorld.player().cell.getRandomTurnOverCardInfo()

    def openRareItem(self, itemId):
        if self.widget and self.widget.stage:
            self.widget.stage.addEventListener(events.MOUSE_CLICK, self.onHideRareItem)
            rareMc = self.widget.getInstByClsName('ActivitySaleTurnOverCard_RareMc')
            rareMc.name = 'RareMc'
            self.widget.addChild(rareMc)
            rareMc.visible = False
            rareMc.x = 677
            rareMc.y = 210
            iconPath = uiUtils.getItemIconFile110(itemId)
            rareMc.item.icon.icon.loadImage(iconPath)
            rareMc.play()
            rareMc.visible = True
            self.specialRewards.remove(itemId)
            ASUtils.callbackAtFrame(rareMc, 110, self.afterShowReward)

    def afterShowReward(self, *args):
        if not self.widget:
            return
        rareMc = self.widget.getChildByName('RareMc')
        if rareMc:
            rareMc.visible = False
            self.widget.removeChild(rareMc)
        if self.specialRewards:
            item = self.specialRewards[0]
            self.openRareItem(item)

    def handleTempMsg(self):
        for msg in self.tempMsgList:
            BigWorld.player().showGameMsg(msg[0], msg[1])

        for item in self.tempItemList:
            BigWorld.player().resInsert(item[0], item[1], item[2], item[3])

        self.tempMsgList = []
        self.tempItemList = []

    def onHideRareItem(self, *args):
        if self.widget:
            self.widget.stage.removeEventListener(events.MOUSE_CLICK, self.onHideRareItem)
        self.afterShowReward()

    def canOpen(self):
        flag = False
        if not gameglobal.rds.configData.get('enableRandomTurnOverCard', False):
            return flag
        data = RTOCD.data.get(SCD.data.get('randomTurnOverCardActivityId', 1), {})
        if not data:
            return
        beginTime = data.get('crontabStart', '')
        endTime = data.get('crontabEnd', '')
        if beginTime and endTime and utils.getDisposableCronTabTimeStamp(beginTime) <= utils.getNow() < utils.getDisposableCronTabTimeStamp(endTime):
            flag = True
        return flag

    def getRedPointVisible(self):
        data = RTOCD.data.get(SCD.data.get('randomTurnOverCardActivityId', 1), {})
        if not data:
            return
        randomTurnOverCardInfo = BigWorld.player().randomTurnOverCardInfo
        finishRewardMargins = randomTurnOverCardInfo.get('finishRewardMargins', {})
        self.totalTurnOverCount = randomTurnOverCardInfo.get('totalTurnOverCount', 0)
        baseMargins = data.get('baseMargins', ())
        loopMargin = data.get('loopMargin', 0)
        baseMarginEnd = baseMargins[-1]
        finishRewardLoopMargin = finishRewardMargins.get('finishRewardLoopMargin', 0)
        if finishRewardLoopMargin:
            leftTimes = self.totalTurnOverCount - finishRewardLoopMargin
            canReceive = leftTimes >= loopMargin and self.totalTurnOverCount <= data.get('maxNum', 100000)
        elif self.totalTurnOverCount >= baseMarginEnd and baseMarginEnd in finishRewardMargins.keys():
            leftTimes = self.totalTurnOverCount - baseMarginEnd
            canReceive = leftTimes >= loopMargin
        else:
            index = 0
            currentMargin = baseMargins[index]
            for baseMargin in baseMargins:
                if baseMargin not in finishRewardMargins.keys():
                    currentMargin = baseMargin
                    break
                index = -1
                currentMargin = baseMargins[index]

            canReceive = self.totalTurnOverCount >= currentMargin
        return canReceive

    def refreshCoin(self):
        if not self.widget:
            return
        p = BigWorld.player()
        tianbi = format(p.unbindCoin + p.bindCoin + p.freeCoin, ',')
        self.widget.moneyTxt.htmlText = '%s' % tianbi
        consumeItemTotalNum = self.calConsumeItemTotalNum()
        self.widget.consumeItemNum.text = consumeItemTotalNum
        randomTurnOverPosInfo = BigWorld.player().randomTurnOverCardInfo.get('randomTurnOverPosInfo', {})
        turnOverCount = len(randomTurnOverPosInfo)
        self.widget.turnOverCount.text = gameStrings.TURN_OVER_CARD_TIME % (turnOverCount, MAX_ITEM_NUM)

    def calConsumeItemTotalNum(self):
        data = RTOCD.data.get(SCD.data.get('randomTurnOverCardActivityId', 1), {})
        consumeItemIds = data.get('consumeItemIds', (411415,))
        consumeItemTotalNum = 0
        for itemId in consumeItemIds:
            itemNum = BigWorld.player().inv.countItemInPages(itemId)
            consumeItemTotalNum += itemNum

        return consumeItemTotalNum

    def refreshCardCounter(self, maxCount = 0):
        if maxCount:
            self.widget.cardCounter.maxCount = maxCount
        else:
            randomTurnOverPosInfo = BigWorld.player().randomTurnOverCardInfo.get('randomTurnOverPosInfo', {})
            turnOverCount = len(randomTurnOverPosInfo)
            self.widget.cardCounter.maxCount = MAX_ITEM_NUM - turnOverCount

    def setLotteryBtn(self, isEnable):
        if self.widget and self.panelMCList:
            self.panelMCList[1].oneBtn.enabled = isEnable
            self.panelMCList[1].tenBtn.enabled = isEnable

    def addTimer(self):
        if not self.timer:
            self.timer = BigWorld.callback(1, self.timerFunc, -1)

    def timerFunc(self):
        if not self.widget:
            self.delTimer()
            return
        data = RTOCD.data.get(SCD.data.get('randomTurnOverCardActivityId', 1), {})
        endTime = data.get('crontabEnd', '')
        left = 0
        if utils.getDisposableCronTabTimeStamp(endTime) >= utils.getNow():
            left = utils.getDisposableCronTabTimeStamp(endTime) - utils.getNow()
        self.widget.leftTimeTxt.text = utils.formatDurationShortVersion(left)
        if left <= 0:
            gameglobal.rds.ui.activitySale.refreshInfo()

    def delTimer(self):
        self.timer and BigWorld.cancelCallback(self.timer)
        self.timer = None

    def pushTurnOverCardMessage(self):
        if BigWorld.player().lv < SCD.data.get('activitySaleMinLv', 0):
            return
        data = RTOCD.data.get(SCD.data.get('randomTurnOverCardActivityId', 1), {})
        pushId = data.get('pushId', uiConst.MESSAGE_TYPE_TURN_OVER_CARD)
        if pushId not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(pushId)
            gameglobal.rds.ui.pushMessage.setCallBack(pushId, {'click': self.onPushMsgClick})

    def removeTurnOverCardPushMsg(self):
        data = RTOCD.data.get(SCD.data.get('randomTurnOverCardActivityId', 1), {})
        pushId = data.get('pushId', uiConst.MESSAGE_TYPE_TURN_OVER_CARD)
        if pushId in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(pushId)

    def onPushMsgClick(self):
        if not self.widget:
            gameglobal.rds.ui.activitySale.show(uiConst.ACTIVITY_SALE_TAB_TURN_OVER_CARD)
        self.removeTurnOverCardPushMsg()

    @ui.checkInventoryLock()
    def useCoinConfirm(self, type, turnOverNum, pos):
        BigWorld.player().cell.randomTurnOverCardByCoinRequest(type, turnOverNum, pos)

    def itemChange(self, *args):
        self.refreshCoin()
