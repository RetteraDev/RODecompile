#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleLotteryProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
import events
import gamelog
import gametypes
import random
import clientUtils
import copy
import const
from uiProxy import UIProxy
from guis import ui
from guis import uiUtils
from guis.asObject import ASObject
from asObject import ASUtils
from gamestrings import gameStrings
from item import Item
from callbackHelper import Functor
from guis.asObject import TipManager
from data import item_data as ID
from data import sys_config_data as SCD
from data import random_lottery_group_data as RLGD
from data import random_lottery_data as RLD
from cdata import game_msg_def_data as GMDD
from data import consumable_item_data as CID
ITEM_START_Y = 0
ITEM_OFFSET_Y = 78
STATE_AWARDS_CHOOSE = 0
STATE_LOTTERY = 1
MAX_CHOOSE_NUM = 8

class ActivitySaleLotteryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleLotteryProxy, self).__init__(uiAdapter)
        self.widget = None
        self.currentPanel = 0
        self.reset()

    def reset(self):
        self.widget = None
        self.panelMCList = []
        self.timer = None
        self.groupRenderMcList = []
        self.selectedNumber = 0
        self.selectedItemList = []
        self.selectedGroupItemList = []
        self.selectedTypeDict = {}
        self.randomLotteryItems = {}
        self.itemSelectMcList = []
        self.lotteryIndex = 0
        self.isLotterying = False
        self.tempMsgList = []
        self.tempItemList = []
        self.remindAgain = True
        self.selectType = 0

    def initLottery(self, widget, initPanel):
        self.currentPanel = initPanel
        p = BigWorld.player()
        p.cell.getRandomLotteryInfo()
        self.widget = widget
        self.delTimer()
        self.initUI()

    def initUI(self):
        if not self.widget:
            return
        self.panelMCList = []
        self.widget.blackBG.visible = False
        data = RLD.data.get(SCD.data.get('randomLotteryActivityId', gametypes.RANDOM_LOTTERY_SYSCONFIG_ID), {})
        awardsChoosePanelMC = self.widget.getChildByName('awardsChoosePanel')
        lotteryPanelMC = self.widget.getChildByName('lotteryPanel')
        self.panelMCList.append(awardsChoosePanelMC)
        self.panelMCList.append(lotteryPanelMC)
        for panelMC in self.panelMCList:
            panelMC.visible = False

        self.panelMCList[self.currentPanel].visible = True
        self.widget.rechargeBtn.addEventListener(events.BUTTON_CLICK, self.handleClickRechargeBtn, False, 0, True)
        awardsChoosePanelMC.title.text = data.get('chooseAwardTitle', gameStrings.RANDOM_LOTTERY_CHOOSE_AWARD)
        awardsChoosePanelMC.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleClickConfirmBtn, False, 0, True)
        awardsChoosePanelMC.cleanBtn.addEventListener(events.BUTTON_CLICK, self.handleClickCleanBtn, False, 0, True)
        lotteryPanelMC.title.text = data.get('lotteryTitle', gameStrings.RANDOM_LOTTERY_LOTTERY)
        lotteryPanelMC.changeAwards.addEventListener(events.BUTTON_CLICK, self.handleClickChangeBtn, False, 0, True)
        lotteryPanelMC.oneBtn.addEventListener(events.BUTTON_CLICK, self.handleClickOneBtn, False, 0, True)
        lotteryPanelMC.tenBtn.addEventListener(events.BUTTON_CLICK, self.handleClickTenBtn, False, 0, True)
        lotteryPanelMC.getAwardsBtn.addEventListener(events.BUTTON_CLICK, self.handleClickAwardsBtn, False, 0, True)
        lotteryPanelMC.awardQuest.addEventListener(events.MOUSE_CLICK, self.handleClickAwardQuest, False, 0, True)
        lotteryPanelMC.awardQuest.textField.htmlText = data.get('awardQuestDesc', gameStrings.TURN_OVER_CARD_AWARD_QUEST_TITLE)
        if self.currentPanel == STATE_AWARDS_CHOOSE:
            self.refreshAwardsChoosePanel()
        else:
            self.refreshLotteryPanel()
        self.addEvent(events.EVENT_TIANBI_COIN_CHANGED, self.refreshCoin)
        self.refreshCoin()
        self.timerFunc()
        self.addTimer()

    def refreshAwardsChoosePanel(self):
        panelMC = self.panelMCList[0]
        if not panelMC:
            return
        self.clearGroupItem(panelMC)
        self.randomLotteryItems = BigWorld.player().randomLotteryInfo.get('randomLotteryItems', {})
        posY = ITEM_START_Y
        for type, groupInfo in RLGD.data.iteritems():
            itemNum = groupInfo.get('itemNum', 0)
            if itemNum == 0:
                continue
            if itemNum <= 6:
                groupRenderMc = self.widget.getInstByClsName('ActivitySaleLottery_smallItem')
                ITEM_OFFSET_Y = 68
                ItemMaxNum = 6
            else:
                groupRenderMc = self.widget.getInstByClsName('ActivitySaleLottery_bigItem')
                ITEM_OFFSET_Y = 129
                ItemMaxNum = 12
            panelMC.awardsChooseWnd.canvas.addChild(groupRenderMc)
            groupRenderMc.x = 0
            groupRenderMc.y = posY
            posY += ITEM_OFFSET_Y - 1
            self.groupRenderMcList.append(groupRenderMc)
            score = groupInfo.get('requireSelectNum', 0)
            groupRenderMc.score.text = score
            groupRenderMc.desc.text = groupInfo.get('desc', '')
            itemInfo = groupInfo.get('itemIds', '')
            itemIds = itemInfo.keys()
            itemCounts = itemInfo.values()
            for i in xrange(ItemMaxNum):
                itemMc = getattr(groupRenderMc, 'item%d' % i)
                if i < itemNum:
                    itemMc.visible = True
                    itemMc.slot.dragable = False
                    itemMc.slot.itemId = itemIds[i]
                    itemMc.slot.itemCount = itemCounts[i]
                    itemMc.slot.type = type
                    itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemIds[i], itemCounts[i]))
                    itemMc.slot.addEventListener(events.MOUSE_CLICK, self.handleShowFit, False, 0, True)
                    itemMc.slot.valueAmount.text = str(itemCounts[i])
                    itemMc.itemCheckBox.selected = False
                    if self.selectedGroupItemList:
                        for groupInfo in self.selectedGroupItemList:
                            if groupInfo['groupId'] == type and itemIds[i] in groupInfo['itemIds']:
                                itemMc.itemCheckBox.selected = True

                    itemMc.itemCheckBox.addEventListener(events.EVENT_SELECT, self.handleSelect, False, 0, True)
                else:
                    itemMc.visible = False

        panelMC.awardsChooseWnd.validateNow()
        panelMC.awardsChooseWnd.refreshHeight(posY)

    def unRegisterLottery(self):
        self.clearGroupItem(self.panelMCList[0])
        self.delTimer()
        self.delEvent(events.EVENT_TIANBI_COIN_CHANGED, self.refreshCoin)
        self.isLotterying = False
        self.handleTempMsg()
        self.onHideSelectMode()
        self.setLotteryBtn(True)
        self.reset()

    def refreshLotteryPanel(self):
        if not self.widget:
            return
        panelMC = self.panelMCList[1]
        if not panelMC:
            return
        p = BigWorld.player()
        randomLotteryInfo = p.randomLotteryInfo
        data = RLD.data.get(SCD.data.get('randomLotteryActivityId', gametypes.RANDOM_LOTTERY_SYSCONFIG_ID), {})
        if not data.get('totalRancomLotteryRewardOp', 0):
            panelMC.base.visible = False
            panelMC.loop.visible = False
            panelMC.getAwardsBtn.visible = False
            panelMC.line.visible = False
            panelMC.noBonusDesc.visible = True
            panelMC.noBonusDesc.desc.text = data.get('noBonusDesc', '')
        elif not data.get('loopOp', 0):
            panelMC.base.visible = True
            panelMC.loop.visible = False
            panelMC.getAwardsBtn.visible = True
            panelMC.line.visible = True
            panelMC.noBonusDesc.visible = False
        else:
            panelMC.base.visible = True
            panelMC.loop.visible = True
            panelMC.getAwardsBtn.visible = True
            panelMC.line.visible = True
            panelMC.noBonusDesc.visible = False
        baseBonusIds = data.get('baseBonusIds', ())
        loopBonus = data.get('loopBonusId', 0)
        itemBonus = clientUtils.genItemBonus(loopBonus)
        loopBonusId = itemBonus[0][0]
        loopBonusCount = itemBonus[0][1]
        lotteryCount = randomLotteryInfo.get('totalLotteryCount', 0)
        panelMC.base.lotteryCount.text = lotteryCount
        panelMC.daojuIcon.bonusType = data.get('ticketIcon', 'choujiang')
        panelMC.itemIcon.bonusType = data.get('fixedIcon')
        fixedItem = data.get('fixedItem', ((411423, 8),))
        panelMC.remindTxt.text = gameStrings.RANDOM_LOTTERY_REMIND_TEXT % fixedItem[0][1]
        baseMargins = data.get('baseMargins', ())
        loopMargin = data.get('loopMargin', 0)
        finishRewardMargins = randomLotteryInfo.get('finishRewardMargins', {})
        i = 0
        rewardAvailable = False
        for baseBonus in baseBonusIds:
            itemBonus = clientUtils.genItemBonus(baseBonus)
            baseBonusId = itemBonus[0][0]
            baseBonusCount = itemBonus[0][1]
            awardMc = getattr(panelMC.base, 'award%d' % i)
            awardMc.slot.itemId = baseBonusId
            awardMc.slot.dragable = False
            baseMargin = baseMargins[i]
            if finishRewardMargins.get(baseMargin, 0):
                awardMc.isReceived.visible = True
                awardMc.canReceive.visible = False
            elif lotteryCount >= baseMargin:
                awardMc.isReceived.visible = False
                awardMc.canReceive.visible = True
                rewardAvailable = True
            else:
                awardMc.isReceived.visible = False
                awardMc.canReceive.visible = False
            awardMc.slot.setItemSlotData(uiUtils.getGfxItemById(baseBonusId, baseBonusCount))
            awardMc.slot.addEventListener(events.MOUSE_CLICK, self.handleShowFit, False, 0, True)
            i += 1

        for i in xrange(len(baseMargins)):
            progressBar = getattr(panelMC.base, 'progressBar%d' % i)
            marginVal = baseMargins[i]
            if i == 0:
                progressBar.maxValue = marginVal
                if lotteryCount > marginVal:
                    progressBar.currentValue = progressBar.maxValue
                else:
                    progressBar.currentValue = lotteryCount
            else:
                progressBar.maxValue = baseMargins[i] - baseMargins[i - 1]
                if lotteryCount >= baseMargins[i - 1] and lotteryCount <= baseMargins[i]:
                    progressBar.currentValue = lotteryCount - baseMargins[i - 1]
                elif lotteryCount >= baseMargins[i]:
                    progressBar.currentValue = progressBar.maxValue
                else:
                    progressBar.currentValue = 0
            progressTip = getattr(panelMC.base, 'tip%d' % i)
            TipManager.addTip(progressTip, baseMargins[i])

        finishRewardLoopMargin = finishRewardMargins.get('finishRewardLoopMargin', 0)
        panelMC.loop.award.slot.itemId = loopBonusId
        panelMC.loop.award.slot.dragable = False
        panelMC.loop.award.slot.setItemSlotData(uiUtils.getGfxItemById(loopBonusId, loopBonusCount))
        panelMC.loop.award.slot.addEventListener(events.MOUSE_CLICK, self.handleShowFit, False, 0, True)
        loopProgressBar = panelMC.loop.progressBar
        loopProgressBar.maxValue = loopMargin
        panelMC.loop.award.isReceived.visible = False
        if finishRewardLoopMargin:
            leftTimes = lotteryCount - finishRewardLoopMargin
            loopProgressBar.currentValue = leftTimes
            rewardAvailable = leftTimes >= loopMargin
            panelMC.loop.award.canReceive.visible = rewardAvailable
        elif lotteryCount > baseMargins[-1]:
            loopRewardAvailable = lotteryCount >= baseMargins[-1] + loopMargin
            panelMC.loop.award.canReceive.visible = loopRewardAvailable
            if loopRewardAvailable:
                rewardAvailable = True
            loopProgressBar.currentValue = lotteryCount - baseMargins[-1]
        else:
            loopProgressBar.currentValue = 0
            panelMC.loop.award.canReceive.visible = False
        panelMC.getAwardsBtn.enabled = rewardAvailable
        self.onRandomLotterySelectionRequest()

    def getCurrentPanel(self):
        self.randomLotteryItems = BigWorld.player().randomLotteryInfo.get('randomLotteryItems', {})
        if self.randomLotteryItems:
            self.selectedNumber = 0
            self.selectedTypeDict = {}
            self.currentPanel = STATE_LOTTERY
            for groupId, groupItems in self.randomLotteryItems.iteritems():
                itemsInfo = RLGD.data.get(groupId, {}).get('itemIds')
                itemIds = itemsInfo.keys()
                groupInfo = {}
                for itemId in groupItems:
                    itemInfo = {}
                    if itemId in itemIds:
                        itemInfo['itemId'] = itemId
                        itemInfo['itemCount'] = itemsInfo.get(itemId, 0)
                        self.selectedItemList.append(itemInfo)
                        self.selectedNumber += 1
                        typeNum = self.selectedTypeDict.get(groupId, 0)
                        typeNum += 1
                        self.selectedTypeDict[groupId] = typeNum

                groupInfo['groupId'] = groupId
                groupInfo['itemIds'] = groupItems
                self.selectedGroupItemList.append(groupInfo)

        else:
            self.selectedNumber = 0
            self.selectedTypeDict = {}
            self.currentPanel = STATE_AWARDS_CHOOSE
            self.randomLotteryItems = copy.deepcopy(RLD.data.get(SCD.data.get('randomLotteryActivityId', gametypes.RANDOM_LOTTERY_SYSCONFIG_ID), {}).get('preLotteryItems', {}))
            for groupId, groupItems in self.randomLotteryItems.iteritems():
                itemsInfo = RLGD.data.get(groupId, {}).get('itemIds')
                itemIds = itemsInfo.keys()
                groupInfo = {}
                for itemId in groupItems:
                    itemInfo = {}
                    if itemId in itemIds:
                        itemInfo['itemId'] = itemId
                        itemInfo['itemCount'] = itemsInfo.get(itemId, 0)
                        self.selectedItemList.append(itemInfo)
                        self.selectedNumber += 1
                    typeNum = self.selectedTypeDict.get(groupId, 0)
                    typeNum += 1
                    self.selectedTypeDict[groupId] = typeNum

                groupInfo['groupId'] = groupId
                groupInfo['itemIds'] = groupItems
                self.selectedGroupItemList.append(groupInfo)

        if self.selectedItemList:
            random.shuffle(self.selectedItemList)
        return self.currentPanel

    def clearGroupItem(self, panel):
        if self.widget and panel:
            for itemRenderMc in self.groupRenderMcList:
                panel.awardsChooseWnd.canvas.removeChild(itemRenderMc)

        self.groupRenderMcList = []

    def handleClickRechargeBtn(self, *args):
        self.uiAdapter.tianyuMall.onOpenChargeWindow()

    def handleClickConfirmBtn(self, *args):
        p = BigWorld.player()
        if self.selectedNumber != MAX_CHOOSE_NUM:
            p.showGameMsg(GMDD.data.NOT_CHOOSE_ENOUGH_AWARD, ())
            return
        BigWorld.player().cell.randomLotterySelectionRequest(self.selectedGroupItemList)
        random.shuffle(self.selectedItemList)
        self.refreshLotteryPanel()

    def handleClickCleanBtn(self, *args):
        self.selectedGroupItemList = []
        self.selectedItemList = []
        self.selectedNumber = 0
        self.selectedTypeDict = {}
        self.refreshAwardsChoosePanel()

    def onRandomLotterySelectionRequest(self):
        if not self.panelMCList:
            return
        lotteryPanelMC = self.panelMCList[1]
        i = 0
        self.itemSelectMcList = []
        if self.selectedItemList:
            for itemInfo in self.selectedItemList:
                itemMc = getattr(lotteryPanelMC, 'item%d' % i)
                itemSelectMc = getattr(lotteryPanelMC, 'selectMc%d' % i)
                self.itemSelectMcList.append(itemSelectMc)
                itemSelectMc.visible = False
                itemId = itemInfo['itemId']
                itemMc.slot.dragable = False
                itemMc.slot.itemId = itemId
                itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, itemInfo['itemCount']))
                itemMc.slot.addEventListener(events.MOUSE_CLICK, self.handleShowFit, False, 0, True)
                itemMc.slot.valueAmount.text = str(itemInfo['itemCount'])
                i += 1

            self.panelMCList[0].visible = False
            self.panelMCList[1].visible = True
            self.currentPanel = STATE_LOTTERY

    def handleClickChangeBtn(self, *args):
        self.refreshAwardsChoosePanel()
        self.panelMCList[1].visible = False
        self.panelMCList[0].visible = True

    def handleClickOneBtn(self, *args):
        if gameglobal.rds.configData.get('enableRandomLotteryOptimize', False):
            if self.remindAgain:
                gameglobal.rds.ui.activitySaleLotteryConfirm.show(1)
            else:
                self.setLotteryBtn(False)
                BigWorld.player().cell.randomLotteryDrawOptimizeRequest(1, self.selectType)
        else:
            self.setLotteryBtn(False)
            BigWorld.player().cell.randomLotteryDrawRequest(1)

    def handleClickTenBtn(self, *args):
        if gameglobal.rds.configData.get('enableRandomLotteryOptimize', False):
            if self.remindAgain:
                gameglobal.rds.ui.activitySaleLotteryConfirm.show(10)
            else:
                self.setLotteryBtn(False)
                BigWorld.player().cell.randomLotteryDrawOptimizeRequest(10, self.selectType)
        else:
            self.setLotteryBtn(False)
            BigWorld.player().cell.randomLotteryDrawRequest(10)

    def showLotteryEffect(self, leftTime, openMc, isOne = False):
        if not self.widget:
            return
        if self.itemSelectMcList:
            for itemSelectMc in self.itemSelectMcList:
                itemSelectMc.visible = False

        if leftTime > 0:
            self.isLotterying = True
            self.itemSelectMcList[(self.lotteryIndex - leftTime) % MAX_CHOOSE_NUM].visible = True
            leftTime -= 1
            if isOne:
                BigWorld.callback(0.2, Functor(self.showLotteryEffect, leftTime, openMc, isOne))
            else:
                BigWorld.callback(0.025, Functor(self.showLotteryEffect, leftTime, openMc, isOne))
        elif leftTime == 0:
            if isOne:
                self.itemSelectMcList[(self.lotteryIndex - leftTime) % MAX_CHOOSE_NUM].visible = True
            openMc.play()
            self.widget.blackBG.visible = True
            openMc.visible = True
            ASUtils.callbackAtFrame(openMc, 32, self.afterOpenOne)

    def setLotteryMsg(self, msgId, data):
        tempMsg = (msgId, data)
        self.tempMsgList.append(tempMsg)

    def setLotteryItem(self, kind, item, page, pos):
        tempItem = (kind,
         item,
         page,
         pos)
        self.tempItemList.append(tempItem)

    def onRandomLotteryDrawRequest(self, items):
        if gameglobal.rds.configData.get('enableRandomLotteryOptimize', False):
            gameglobal.rds.ui.activitySaleLotteryConfirm.hide()
        if not self.widget:
            return
        itemList = []
        for group, groupItems in items.iteritems():
            itemsInfo = RLGD.data.get(group, {}).get('itemIds', {})
            bindItemIds = RLGD.data.get(group, {}).get('bindItemIds', {})
            itemIds = itemsInfo.keys()
            for itemId in groupItems:
                itemInfo = {}
                if itemId in itemIds:
                    itemInfo['itemId'] = itemId
                    itemInfo['itemCount'] = itemsInfo.get(itemId, 0)
                    itemList.append(itemInfo)
                else:
                    for itemid, bindItemid in bindItemIds.iteritems():
                        if itemId == bindItemid and itemid in itemIds:
                            itemInfo['itemId'] = itemId
                            itemInfo['itemCount'] = itemsInfo.get(itemid, 0)
                            itemInfo['unBindId'] = itemid
                            itemList.append(itemInfo)

        fixedItem = items.get('fixedItem', (411423, 8))
        gamelog.debug('yedawang### itemList', itemList)
        data = RLD.data.get(SCD.data.get('randomLotteryActivityId', gametypes.RANDOM_LOTTERY_SYSCONFIG_ID), {})
        rareItemIds = data.get('rareItemIds', [])
        if len(itemList) == 1:
            openOneMc = self.widget.getInstByClsName('ActivitySaleLottery_openOneReward')
            openOneMc.name = 'openOneReward'
            self.widget.addChild(openOneMc)
            openOneMc.visible = False
            openOneMc.x = 517
            openOneMc.y = 199
            fixedItemMc = openOneMc.item0
            fixedItemMc.rare.visible = False
            fixedItemMc.itemIcon.dragable = False
            fixedItemMc.itemIcon.itemId = fixedItem[0]
            fixedItemMc.itemIcon.setItemSlotData(uiUtils.getGfxItemById(fixedItem[0], fixedItem[1]))
            item = itemList[0]
            itemMc = openOneMc.item
            itemMc.itemIcon.dragable = False
            itemMc.itemIcon.itemId = item['itemId']
            unbindId = item.get('unBindId', 0) if item.get('unBindId', 0) else item.get('itemId', 0)
            if unbindId in rareItemIds:
                itemMc.rare.visible = True
            else:
                itemMc.rare.visible = False
            itemMc.itemIcon.setItemSlotData(uiUtils.getGfxItemById(item['itemId'], item['itemCount']))
            itemMc.itemIcon.valueAmount.text = str(item['itemCount'])
            itemIndex = -1
            for i, itemInfo in enumerate(self.selectedItemList):
                if item.get('unBindId', 0) == itemInfo['itemId'] or item['itemId'] == itemInfo['itemId']:
                    if item.get('itemCount', 0) == itemInfo['itemCount']:
                        itemIndex = i

            if itemIndex >= 0:
                self.lotteryIndex = MAX_CHOOSE_NUM + itemIndex
                self.showLotteryEffect(MAX_CHOOSE_NUM + itemIndex, openOneMc, isOne=True)
            else:
                openOneMc.play()
                openOneMc.visible = True
                ASUtils.callbackAtFrame(openOneMc, 32, self.afterOpenOne)
        elif len(itemList) == 10:
            openTenMc = self.widget.getInstByClsName('ActivitySaleLottery_openTenReward')
            openTenMc.name = 'openTenReward'
            self.widget.addChild(openTenMc)
            openTenMc.visible = False
            openTenMc.x = 517
            openTenMc.y = 199
            fixedItemMc = openTenMc.items.item
            fixedItemMc.rare.visible = False
            fixedItemMc.itemIcon.dragable = False
            fixedItemMc.itemIcon.itemId = fixedItem[0]
            fixedItemMc.itemIcon.setItemSlotData(uiUtils.getGfxItemById(fixedItem[0], fixedItem[1]))
            i = 0
            random.shuffle(itemList)
            for itemInfo in itemList:
                itemMc = getattr(openTenMc.items, 'item%d' % i)
                itemId = itemInfo['itemId']
                itemMc.itemIcon.dragable = False
                itemMc.itemIcon.itemId = itemId
                unbindId = itemInfo.get('unBindId', 0) if itemInfo.get('unBindId', 0) else itemInfo.get('itemId', 0)
                if unbindId in rareItemIds:
                    itemMc.rare.visible = True
                else:
                    itemMc.rare.visible = False
                itemMc.itemIcon.setItemSlotData(uiUtils.getGfxItemById(itemId, itemInfo['itemCount']))
                itemMc.itemIcon.valueAmount.text = str(itemInfo['itemCount'])
                i += 1

            self.lotteryIndex = MAX_CHOOSE_NUM * 4
            self.showLotteryEffect(MAX_CHOOSE_NUM * 4, openTenMc, isOne=False)
        self.refreshLotteryPanel()

    def afterOpenOne(self, *args):
        self.isLotterying = False
        self.handleTempMsg()
        self.setLotteryBtn(True)
        if self.widget and self.widget.stage:
            self.widget.stage.addEventListener(events.MOUSE_CLICK, self.onHideSelectMode)

    def afterOpenTen(self, *args):
        self.isLotterying = False
        self.handleTempMsg()
        self.setLotteryBtn(True)
        if self.widget and self.widget.stage:
            self.widget.stage.addEventListener(events.MOUSE_CLICK, self.onHideSelectMode)

    def handleTempMsg(self):
        for msg in self.tempMsgList:
            BigWorld.player().showGameMsg(msg[0], msg[1])

        for item in self.tempItemList:
            BigWorld.player().resInsert(item[0], item[1], item[2], item[3])

        self.tempMsgList = []
        self.tempItemList = []

    def onHideSelectMode(self, *args):
        self.widget.blackBG.visible = False
        self.widget.stage.removeEventListener(events.MOUSE_CLICK, self.onHideSelectMode)
        openOneReward = self.widget.getChildByName('openOneReward')
        openTenReward = self.widget.getChildByName('openTenReward')
        if openOneReward:
            openOneReward.visible = False
            self.widget.removeChild(openOneReward)
        if openTenReward:
            openTenReward.visible = False
            self.widget.removeChild(openTenReward)

    def handleClickAwardsBtn(self, *args):
        BigWorld.player().cell.receiveRandomLotteryDrawTotalReward()

    def handleSelect(self, *args):
        target = ASObject(args[3][0]).currentTarget
        itemInfo = {}
        itemInfo['itemId'] = target.parent.slot.itemId
        itemInfo['itemCount'] = target.parent.slot.itemCount
        type = target.parent.slot.type
        groupItems = {}
        hasKey = False
        if target.selected == True:
            self.selectedNumber += 1
            self.selectedItemList.append(itemInfo)
            if self.selectedGroupItemList:
                for groupInfo in self.selectedGroupItemList:
                    if groupInfo['groupId'] == type:
                        hasKey = True
                        groupItems['itemIds'] = groupInfo.get('itemIds', [])
                        groupItems['itemIds'].append(itemInfo['itemId'])

                if hasKey == False:
                    groupItems['groupId'] = type
                    groupItems['itemIds'] = [itemInfo['itemId']]
                    self.selectedGroupItemList.append(groupItems)
            else:
                groupItems['groupId'] = type
                groupItems['itemIds'] = [itemInfo['itemId']]
                self.selectedGroupItemList.append(groupItems)
            typeNum = self.selectedTypeDict.get(type, 0)
            typeNum += 1
            self.selectedTypeDict[type] = typeNum
        elif target.selected == False:
            self.selectedNumber -= 1
            self.selectedItemList.remove(itemInfo)
            if self.selectedGroupItemList:
                for groupInfo in self.selectedGroupItemList:
                    if groupInfo['groupId'] == type:
                        groupItems['itemIds'] = groupInfo.get('itemIds', [])
                        groupItems['itemIds'].remove(itemInfo['itemId'])

            typeNum = self.selectedTypeDict.get(type, 0)
            typeNum -= 1
            self.selectedTypeDict[type] = typeNum
        for type, num in self.selectedTypeDict.iteritems():
            score = RLGD.data.get(type, {}).get('requireSelectNum', 0)
            if num > score:
                target.selected = False
                p = BigWorld.player()
                p.showGameMsg(GMDD.data.CAN_NOT_CHOOSE_MORE_AWARD_INGROUP, ())

        if self.selectedNumber > MAX_CHOOSE_NUM:
            target.selected = False
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.CAN_NOT_CHOOSE_MORE_AWARD, ())

    def canOpen(self):
        flag = False
        if not gameglobal.rds.configData.get('enableRandomLottery', False):
            return flag
        data = RLD.data.get(SCD.data.get('randomLotteryActivityId', gametypes.RANDOM_LOTTERY_SYSCONFIG_ID), {})
        beginTime = data.get('crontabStart', '')
        endTime = data.get('crontabEnd', '')
        if beginTime and endTime and utils.getDisposableCronTabTimeStamp(beginTime) <= utils.getNow() <= utils.getDisposableCronTabTimeStamp(endTime):
            flag = True
        return flag

    def refreshCoin(self):
        if not self.widget:
            return
        p = BigWorld.player()
        tianbi = format(p.unbindCoin + p.bindCoin + p.freeCoin, ',')
        self.widget.moneyTxt.htmlText = '%s' % tianbi

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
        data = RLD.data.get(SCD.data.get('randomLotteryActivityId', gametypes.RANDOM_LOTTERY_SYSCONFIG_ID), {})
        endTime = data.get('crontabEnd', '')
        left = 0
        if utils.getDisposableCronTabTimeStamp(endTime) >= utils.getNow():
            left = utils.getDisposableCronTabTimeStamp(endTime) - utils.getNow()
        self.widget.leftTimeTxt.text = utils.formatDurationShortVersion(left)

    def delTimer(self):
        self.timer and BigWorld.cancelCallback(self.timer)
        self.timer = None

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

    def pushLotteryMessage(self):
        if BigWorld.player().lv < SCD.data.get('activitySaleMinLv', 0):
            return
        data = RLD.data.get(SCD.data.get('randomLotteryActivityId', gametypes.RANDOM_LOTTERY_SYSCONFIG_ID), {})
        pushId = data.get('pushId', uiConst.MESSAGE_TYPE_RANDOM_LOTTERY)
        if pushId not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(pushId)
            gameglobal.rds.ui.pushMessage.setCallBack(pushId, {'click': self.onPushMsgClick})

    def removeLotteryPushMsg(self):
        data = RLD.data.get(SCD.data.get('randomLotteryActivityId', gametypes.RANDOM_LOTTERY_SYSCONFIG_ID), {})
        pushId = data.get('pushId', uiConst.MESSAGE_TYPE_RANDOM_LOTTERY)
        if pushId in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(pushId)

    def onPushMsgClick(self):
        if not self.widget:
            gameglobal.rds.ui.activitySale.show(uiConst.ACTIVITY_SALE_TAB_LOTTERY)
        self.removeLotteryPushMsg()

    def handleClickAwardQuest(self, *args):
        gameglobal.rds.ui.turnOverCardAward.show(const.SHOW_TYPE_AWARD_QUEST_LOTTERY)
