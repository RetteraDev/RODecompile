#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleLuckyLotteryProxy.o
import BigWorld
import sMath
import gameglobal
import uiConst
import const
import utils
import events
import math
import random
import ui
from guis.asObject import ASUtils
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASObject
from gamestrings import gameStrings
from item import Item
from callbackHelper import Functor
from guis.asObject import TipManager
from data import composite_shop_data as CSD
from cdata import game_msg_def_data as GMDD
from data import random_lucky_lottery_data as RLLD
from data import item_data as ID
from data import sys_config_data as SCD
LUCKY_DRAW_SINGLE_IDX = 0
LUCKY_DRAW_MULTI_IDX = 1
LUCKY_TREASURE_BOX_MAX_NUM = 5
LUCKY_MULTI_DRAW_DISPLAY_MAX_NUM = 5
MAX_LUCKY_ITEM_NUM = 14
LUCKY_NUM_PROGRESS_LOAD_SPEED = 10

class ActivitySaleLuckyLotteryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleLuckyLotteryProxy, self).__init__(uiAdapter)
        self.widget = None
        self.curShowDrawAnimTimes = 0
        self.showDrawConfirmPanel = True
        self.tabSubIdxToRLLDId = {}
        self.tempReceiveItemList = []
        self.tempReceiveItemMsgList = []
        self.reset()

    def reset(self):
        self.tabIdx = 0
        self.leftTimer = None
        self.lastLuckyNum = 0
        self.luckyNumTimer = None
        self.drawing = False
        self.drawResetTimer = True

    def checkAndHide(self):
        self.tabSubIdxToRLLDId = {}
        self.showDrawConfirmPanel = True

    def clearAll(self):
        self.curShowDrawAnimTimes = 0

    def unRegister(self):
        self.widget = None
        self.leftTimer and BigWorld.cancelCallback(self.leftTimer)
        self.luckyNumTimer and BigWorld.cancelCallback(self.luckyNumTimer)
        self.drawResetTimer and BigWorld.cancelCallback(self.drawResetTimer)
        BigWorld.player().unRegisterEvent(const.EVENT_ITEM_CHANGE, self.itemChange)
        BigWorld.player().unRegisterEvent(const.EVENT_ITEM_REMOVE, self.itemChange)
        self.delEvent(events.EVENT_TIANBI_COIN_CHANGED, self.refreshDrawItem)
        self.processDrawingInfo(False)
        self.reset()

    def initPanel(self, tabIdx, widget):
        self.widget = widget
        self.tabIdx = tabIdx
        if not self.curRLLDId:
            return
        self.initLeftPanel()
        self.initRightPanel()

    @property
    def curRLLDId(self):
        return self.tabSubIdxToRLLDId.get(self.tabIdx, 0)

    @property
    def curLuckyLotteryInfo(self):
        return self.getLuckyLotteryInfoById(self.curRLLDId)

    @property
    def curLuckyDrawCount(self):
        return self.curLuckyLotteryInfo.get('drawCnt', 0)

    def isPanelVisible(self):
        if not self.widget:
            return False
        return True

    def getRedPointVisible(self, RLLDId):
        allDrawCnt = self.getLuckyLotteryInfoById(RLLDId).get('drawCnt', 0)
        curTreasureBoxData = self.getLuckyLotteryInfoById(RLLDId).get('treasureBoxes', [])
        allTreasureBoxData = RLLD.data.get(RLLDId, {}).get('treasureBoxBonus', ())
        for treasureBoxIdx, treasureBoxData in enumerate(allTreasureBoxData):
            if allDrawCnt >= treasureBoxData[0] and treasureBoxIdx not in curTreasureBoxData:
                return True

        return False

    def checkCanOpen(self, RLLDId):
        if not gameglobal.rds.configData.get('enableLuckyLottery'):
            return False
        startTime = RLLD.data.get(RLLDId, {}).get('startTime', None)
        endTime = RLLD.data.get(RLLDId, {}).get('endTime', None)
        if not startTime or not endTime:
            return False
        elif not utils.inCrontabRange(startTime, endTime):
            return False
        else:
            return True

    def draw(self, drawConditionIdx, showDrawConfirmPanel):
        drawCondition = self.getDrawCondition(drawConditionIdx)
        if not self.checkItemEnough(drawCondition['drawItemId'], drawCondition['drawItemNum']):
            self.widget.drawConfirmPanel.visible = True
            self.widget.drawConfirmPanel.checkBox.visible = False
            self.widget.drawConfirmPanel.title.text = uiUtils.getTextFromGMD(GMDD.data.LUCKY_LOTTERY_DRAW_ITEM_NOT_ENOUGH_HINT, '') % utils.getItemName(drawCondition['drawItemId'])
            self.widget.drawConfirmPanel.type = 'CountLimit'
            self.widget.drawConfirmPanel.drawConditionIdx = drawConditionIdx
            self.widget.blackBG.visible = True
            return
        if drawConditionIdx == LUCKY_DRAW_MULTI_IDX and showDrawConfirmPanel:
            self.widget.drawConfirmPanel.visible = True
            self.widget.drawConfirmPanel.checkBox.visible = True
            self.widget.drawConfirmPanel.title.text = gameStrings.LUCKY_LOTTERY_CONFIRM_DRAW_MULTI % drawCondition['drawNum']
            self.widget.drawConfirmPanel.type = 'DrawMultiConfirm'
            self.widget.drawConfirmPanel.drawConditionIdx = drawConditionIdx
            self.widget.blackBG.visible = True
            return
        self.realDraw(drawConditionIdx)
        self.processDrawingInfo(True)
        self.drawResetTimer and BigWorld.cancelCallback(self.drawResetTimer)
        self.drawResetTimer = BigWorld.callback(2, Functor(self.processDrawingInfo, False))

    @ui.checkInventoryLock()
    def realDraw(self, drawConditionIdx):
        p = BigWorld.player()
        p.cell.requestLuckyDraw(self.curRLLDId, drawConditionIdx, p.cipherOfPerson)

    def realGetTreasureBox(self, treasureBoxIdx):
        BigWorld.player().cell.requestLuckyDrawTreasureBox(self.curRLLDId, treasureBoxIdx)

    def itemChange(self, *args):
        self.refreshDrawItem()

    def handleOpenShopBtnClick(self, *args):
        uiUtils.closeCompositeShop()
        shopId = RLLD.data.get(self.curRLLDId, {}).get('compositeShopId', 0)
        shopId and BigWorld.player().base.openPrivateShop(0, shopId)

    def handleAddMoneyBtnClick(self, *args):
        gameglobal.rds.ui.tianyuMall.onOpenChargeWindow()

    def handleAddDrawItemBtnClick(self, *args):
        drawItemKeyWord = str(RLLD.data.get(self.curRLLDId, {}).get('drawItemKeyWord', ''))
        if not drawItemKeyWord:
            return
        gameglobal.rds.ui.tianyuMall.show(keyWord=drawItemKeyWord)

    def handleDrawBtnClick(self, *args):
        btn = ASObject(args[3][0]).currentTarget
        drawConditionIdx = int(btn.drawConditionIdx)
        self.draw(drawConditionIdx, self.showDrawConfirmPanel)

    def handleShowDrawConfirmPanelCheckBox(self, *args):
        checkBoxMc = ASObject(args[3][0]).currentTarget
        self.showDrawConfirmPanel = not bool(checkBoxMc.selected)

    def handleDrawConfrimClick(self, *args):
        btn = ASObject(args[3][0]).currentTarget
        self.widget.drawConfirmPanel.visible = False
        self.widget.blackBG.visible = False
        if btn.name == 'confirmBtn':
            drawCondition = self.getDrawCondition(self.widget.drawConfirmPanel.drawConditionIdx)
            if self.widget.drawConfirmPanel.type == 'CountLimit':
                self.openTianyuMall(drawCondition['mallKeyWord'])
            if self.widget.drawConfirmPanel.type == 'DrawMultiConfirm':
                self.draw(LUCKY_DRAW_MULTI_IDX, False)
        if btn.name == 'cancelBtn':
            if self.widget.drawConfirmPanel.type == 'DrawMultiConfirm':
                self.showDrawConfirmPanel = True
                self.widget.drawConfirmPanel.checkBox.selected = not self.showDrawConfirmPanel

    def handleTreasureBoxClick(self, *args):
        treasureBoxMc = ASObject(args[3][0]).currentTarget.parent
        self.realGetTreasureBox(int(treasureBoxMc.treasureBoxIdx))

    def handleSuccessPanelConfirmClick(self, *args):
        self.refreshLuckyNumProgress()
        successPanel = ASObject(args[3][0]).currentTarget.parent.parent
        successPanel.visible = False
        successPanel.stop()
        self.widget.blackBG.visible = False

    def handleSuccessPanelAgainDrawClick(self, *args):
        self.refreshLuckyNumProgress()
        againDrawBtn = ASObject(args[3][0]).currentTarget
        successPanel = againDrawBtn.parent.parent
        successPanel.visible = False
        successPanel.stop()
        self.widget.blackBG.visible = False
        drawConditionIdx = int(againDrawBtn.drawConditionIdx)
        self.draw(drawConditionIdx, self.showDrawConfirmPanel)

    def initLeftPanel(self):
        if not self.widget:
            return
        BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.itemChange)
        BigWorld.player().registerEvent(const.EVENT_ITEM_REMOVE, self.itemChange)
        self.addEvent(events.EVENT_TIANBI_COIN_CHANGED, self.refreshDrawItem)
        self.widget.AddMoneyBtn.addEventListener(events.MOUSE_CLICK, self.handleAddMoneyBtnClick, False, 0, True)
        self.widget.AddDrawItemBtn.addEventListener(events.MOUSE_CLICK, self.handleAddDrawItemBtnClick, False, 0, True)
        self.widget.lotteryPanel.helpIcon.helpKey = RLLD.data.get(self.curRLLDId, {}).get('helpKey', 0)
        self.widget.lotteryPanel.luckyNumProgress.luckyNumNameTxt.text = RLLD.data.get(self.curRLLDId, {}).get('luckyNumName', '')
        self.widget.lotteryPanel.luckyNumProgress.maxValue = int(RLLD.data.get(self.curRLLDId, {}).get('totalLuckyNum', 1))
        self.widget.lotteryPanel.singleDrawBtn.addEventListener(events.MOUSE_CLICK, self.handleDrawBtnClick, False, 0, True)
        self.widget.lotteryPanel.multiDrawBtn.addEventListener(events.MOUSE_CLICK, self.handleDrawBtnClick, False, 0, True)
        singleDrawCondition = self.getDrawCondition(LUCKY_DRAW_SINGLE_IDX)
        multiDrawCondition = self.getDrawCondition(LUCKY_DRAW_MULTI_IDX)
        self.widget.lotteryPanel.singleDrawBtn.itemIcon.bonusType = singleDrawCondition['bonusType']
        self.widget.lotteryPanel.singleDrawBtn.label = singleDrawCondition['drawBtnLabel']
        self.widget.lotteryPanel.singleDrawBtn.itemNum.text = singleDrawCondition['drawItemNum']
        self.widget.lotteryPanel.singleDrawBtn.drawConditionIdx = LUCKY_DRAW_SINGLE_IDX
        self.widget.lotteryPanel.multiDrawBtn.itemIcon.bonusType = multiDrawCondition['bonusType']
        self.widget.lotteryPanel.multiDrawBtn.label = multiDrawCondition['drawBtnLabel']
        self.widget.lotteryPanel.multiDrawBtn.itemNum.text = multiDrawCondition['drawItemNum']
        self.widget.lotteryPanel.multiDrawBtn.drawConditionIdx = LUCKY_DRAW_MULTI_IDX
        self.widget.drawConfirmPanel.visible = False
        self.widget.drawConfirmPanel.checkBox.selected = not self.showDrawConfirmPanel
        self.widget.drawConfirmPanel.checkBox.addEventListener(events.EVENT_SELECT, self.handleShowDrawConfirmPanelCheckBox, False, 0, True)
        self.widget.drawConfirmPanel.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleDrawConfrimClick, False, 0, True)
        self.widget.drawConfirmPanel.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleDrawConfrimClick, False, 0, True)
        self.widget.singleSuccessPanel.visible = False
        self.widget.singleSuccessPanel.items.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleSuccessPanelConfirmClick, False, 0, True)
        self.widget.singleSuccessPanel.items.againDrawBtn.addEventListener(events.MOUSE_CLICK, self.handleSuccessPanelAgainDrawClick, False, 0, True)
        self.widget.singleSuccessPanel.items.againDrawBtn.label = gameStrings.LUCKY_LOTTERY_AGAIN_DRAW_BTN_LABEL % int(singleDrawCondition['drawNum'])
        self.widget.singleSuccessPanel.items.againDrawBtn.drawConditionIdx = LUCKY_DRAW_SINGLE_IDX
        self.widget.multiSuccessPanel.visible = False
        self.widget.multiSuccessPanel.items.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleSuccessPanelConfirmClick, False, 0, True)
        self.widget.multiSuccessPanel.items.againDrawBtn.addEventListener(events.MOUSE_CLICK, self.handleSuccessPanelAgainDrawClick, False, 0, True)
        self.widget.multiSuccessPanel.items.againDrawBtn.label = gameStrings.LUCKY_LOTTERY_AGAIN_DRAW_BTN_LABEL % int(multiDrawCondition['drawNum'])
        self.widget.multiSuccessPanel.items.againDrawBtn.drawConditionIdx = LUCKY_DRAW_MULTI_IDX
        self.widget.blackBG.visible = False
        self.refreshAllLuckyItems()
        self.refreshDrawItem()
        self.refreshLuckyNumProgress()
        self.hideAllSelectItemEffect()
        self.processDrawingInfo(False)

    def initRightPanel(self):
        if not self.widget:
            return
        self.refreshLeftTime()
        self.refreshTreasureBox()
        self.refreshDrawCnt()

    def hideAllSelectItemEffect(self):
        if not self.widget:
            return
        for idx in xrange(MAX_LUCKY_ITEM_NUM):
            itemSelectMc = getattr(self.widget.lotteryPanel, 'selectMc%d' % idx)
            itemSelectMc.visible = False
            ASUtils.setHitTestDisable(itemSelectMc, True)

    def checkIsDrawingLuckyItem(self, itemData, page, pos):
        if not self.widget:
            return False
        if not self.drawing:
            return False
        if not itemData:
            return False
        itemCount = itemData.cwrap
        itemId = itemData.id
        allLuckyItems = RLLD.data.get(self.curRLLDId, {}).get('showLuckyItems', ())
        if (itemId, itemCount) in allLuckyItems:
            self.tempReceiveItemList.append((itemData, page, pos))
            return True
        return False

    def checkTempBagDataValid(self):
        p = BigWorld.player()
        if not self.widget:
            return False
        if not self.drawing:
            return False
        if not self.tempReceiveItemList:
            return False
        for tempItemData, tempPage, tempPos in self.tempReceiveItemList:
            curItemData = p.tempBag.getQuickVal(tempPage, tempPos)
            if not curItemData or not tempItemData:
                del self.tempReceiveItemList[:]
                return False
            if tempItemData.id == curItemData.id and tempItemData.cwrap == curItemData.cwrap:
                continue
            else:
                del self.tempReceiveItemList[:]
                return False

        return True

    def outQueueLotteryItem(self):
        if self.tempReceiveItemList:
            gameglobal.rds.ui.inventory.forceUpdateTempBag()
        del self.tempReceiveItemList[:]

    def enQueueLotteryMsg(self, msgId, data):
        tempMsg = (msgId, data)
        self.tempReceiveItemMsgList.append(tempMsg)

    def outQueueLotteryMsg(self):
        for msg in self.tempReceiveItemMsgList:
            BigWorld.player().showGameMsg(msg[0], msg[1])

        del self.tempReceiveItemMsgList[:]

    def processDrawingInfo(self, isSuccessDrawing):
        self.drawing = isSuccessDrawing
        self.setOtherInValid(not isSuccessDrawing)
        if not isSuccessDrawing:
            self.outQueueLotteryItem()
            self.outQueueLotteryMsg()

    def startSelectItem(self, RLLDId, drawConditionIdx, allItemDataList):
        drawCondition = self.getDrawCondition(drawConditionIdx)
        self.curShowDrawAnimTimes += drawCondition['drawNum']
        self.drawResetTimer and BigWorld.cancelCallback(self.drawResetTimer)
        curItemDataList = list(allItemDataList)
        drawResultData = {'drawConditionIdx': drawConditionIdx,
         'allItemDataList': allItemDataList,
         'RLLDId': RLLDId}
        if self.curRLLDId == RLLDId:
            if self.curShowDrawAnimTimes > RLLD.data.get(self.curRLLDId, {}).get('showDrawAnimTimes', ()):
                self.afterSelectItem(drawResultData)
            else:
                self.processDrawingInfo(True)
                self.startRecurveItemEffect(curItemDataList, drawResultData, isFirstItem=True, lastItemIdx=-1)
        else:
            self.afterSelectItem(drawResultData)

    def startRecurveItemEffect(self, curItemDataList, drawResultData, isFirstItem = True, lastItemIdx = -1):
        if not curItemDataList:
            self.afterSelectItem(drawResultData)
        else:
            itemData = curItemDataList.pop()
            itemIdx = self.getItemIdxInAllLuckyItems(drawResultData.get('RLLDId', 0), itemData)
            leftTime = itemIdx
            if lastItemIdx != -1:
                if lastItemIdx < itemIdx:
                    leftTime = itemIdx - lastItemIdx - 1
                else:
                    leftTime = MAX_LUCKY_ITEM_NUM - lastItemIdx + itemIdx - 1
                if leftTime < MAX_LUCKY_ITEM_NUM / 2:
                    leftTime += MAX_LUCKY_ITEM_NUM
            if isFirstItem:
                leftTime += 3 * MAX_LUCKY_ITEM_NUM
            self.RecurveItemEffect(leftTime, lastItemIdx, curItemDataList, drawResultData)

    def RecurveItemEffect(self, leftTime, lastItemIdx, curItemDataList, drawResultData):
        if not self.widget or drawResultData.get('RLLDId', 0) != self.curRLLDId:
            self.afterSelectItem(drawResultData)
            return
        lastItemIdx = (lastItemIdx + 1) % MAX_LUCKY_ITEM_NUM
        lastItemSelectMc = getattr(self.widget.lotteryPanel, 'selectMc%d' % lastItemIdx)
        lastItemSelectMc.visible = True
        lastItemSelectMc.gotoAndPlay('select')
        leftTime -= 1
        if leftTime == -1:
            lastItemSelectMc.gotoAndPlay('end')
            BigWorld.callback(0.75, Functor(self.startRecurveItemEffect, curItemDataList, drawResultData, False, lastItemIdx))
            return
        BigWorld.callback(0.02, Functor(self.RecurveItemEffect, leftTime, lastItemIdx, curItemDataList, drawResultData))

    def afterSelectItem(self, drawResultData):
        self.processDrawingInfo(False)
        self.showDrawSuccessPanel(drawResultData)
        self.refreshTreasureBox()

    def showDrawSuccessPanel(self, drawResultData):
        if not self.widget:
            return
        allItemDataList = drawResultData['allItemDataList']
        if not allItemDataList:
            return
        if drawResultData['drawConditionIdx'] == LUCKY_DRAW_SINGLE_IDX:
            self.showSingleSuccessPanel(allItemDataList[0])
        if drawResultData['drawConditionIdx'] == LUCKY_DRAW_MULTI_IDX:
            self.showMultiSuccessPanel(allItemDataList)

    def setOtherInValid(self, valid):
        if not self.widget:
            return
        self.widget.lotteryPanel.singleDrawBtn.enabled = valid
        self.widget.lotteryPanel.multiDrawBtn.enabled = valid

    def refreshAllLuckyItems(self):
        if not self.widget:
            return
        allLuckyItems = RLLD.data.get(self.curRLLDId, {}).get('showLuckyItems', ())
        for luckyItemIdx in xrange(MAX_LUCKY_ITEM_NUM):
            luckyItemMc = self.widget.lotteryPanel.getChildByName('item%d' % luckyItemIdx)
            if luckyItemIdx >= len(allLuckyItems):
                luckyItemMc.visible = False
                continue
            else:
                luckyItemData = allLuckyItems[luckyItemIdx]
                luckyItemMc.visible = True
                luckyItemMc.slot.dragable = False
                luckyItemMc.slot.setItemSlotData(uiUtils.getGfxItemById(luckyItemData[0], count=luckyItemData[1]))
                luckyItemMc.rare.visible = luckyItemMc.quality.visible = self.checkItemIsRare(luckyItemData[0], luckyItemData[1])

    def showMultiSuccessPanel(self, itemList):
        if not self.widget:
            return
        self.widget.blackBG.visible = True
        self.widget.multiSuccessPanel.visible = True
        self.widget.multiSuccessPanel.gotoAndPlay(2)
        for idx in xrange(LUCKY_MULTI_DRAW_DISPLAY_MAX_NUM):
            itemMc = self.widget.multiSuccessPanel.items.getChildByName('item%d' % idx)
            if idx >= len(itemList):
                itemMc.visible = False
                continue
            else:
                itemData = itemList[idx]
                itemMc.visible = True
                itemMc.slot.dragable = False
                itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemData[0], count=itemData[1]))
                itemMc.rare.visible = itemMc.quality.visible = self.checkItemIsRare(itemData[0], itemData[1])

    def showSingleSuccessPanel(self, itemData):
        if not self.widget:
            return
        itemId, itemNum = itemData
        self.widget.blackBG.visible = True
        self.widget.singleSuccessPanel.visible = True
        self.widget.singleSuccessPanel.gotoAndPlay(2)
        itemMc = self.widget.singleSuccessPanel.items.item
        itemMc.slot.dragable = False
        itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, count=itemNum))
        itemMc.rare.visible = itemMc.quality.visible = self.checkItemIsRare(itemId, itemNum)

    def refreshLuckyNumProgress(self):
        if not self.widget:
            return
        curLuckyNums = self.curLuckyLotteryInfo.get('luckyNum', 0)
        self.setLuckyNumProgress(last=self.lastLuckyNum, current=curLuckyNums, speed=LUCKY_NUM_PROGRESS_LOAD_SPEED)

    def setLuckyNumProgress(self, last, current, speed):
        self.luckyNumTimer and BigWorld.cancelCallback(self.luckyNumTimer)
        self.luckyNumTimer = None
        if not self.widget:
            return
        else:
            totalLuckyNum = RLLD.data.get(self.curRLLDId, {}).get('totalLuckyNum', 1)
            if last > totalLuckyNum or last < 0:
                self.setLuckyNumsProgress(current)
                self.lastLuckyNum = current
                return
            if last == current:
                self.setLuckyNumsProgress(current)
                self.lastLuckyNum = current
                return
            if last > current:
                speed = -abs(speed)
            elif last < current:
                speed = abs(speed)
            newLast = last + speed
            if speed < 0 and newLast < current or speed > 0 and newLast > current:
                self.setLuckyNumsProgress(current)
                self.lastLuckyNum = current
                return
            self.lastLuckyNum = newLast
            self.setLuckyNumsProgress(newLast)
            self.luckyNumTimer = BigWorld.callback(0.05, Functor(self.setLuckyNumProgress, self.lastLuckyNum, current, speed))
            return

    def setLuckyNumsProgress(self, currentNum):
        totalLuckyNum = RLLD.data.get(self.curRLLDId, {}).get('totalLuckyNum', 1)
        currentProgressNum = sMath.clamp(currentNum, 0, totalLuckyNum)
        if totalLuckyNum - 15 < currentProgressNum < totalLuckyNum:
            currentProgressNum = totalLuckyNum - 15
        self.widget.lotteryPanel.luckyNumProgress.currentValue = currentProgressNum
        self.widget.lotteryPanel.luckyNumProgress.currentValueText.text = str(currentNum)

    def refreshTreasureBox(self):
        if not self.widget:
            return
        allTreasureBoxIdxList = []
        allTreasureBoxData = RLLD.data.get(self.curRLLDId, {}).get('treasureBoxBonus', ())
        for index in xrange(len(allTreasureBoxData)):
            allTreasureBoxIdxList.append(index)

        treasureBoxScroll = self.widget.lotteryPanel.treasureBoxScroll
        treasureBoxScroll.itemRenderer = 'ActivitySaleLuckyLottery_treasureBoxScrollItem'
        treasureBoxScroll.lableFunction = self.treasureBoxScrollLabelFunction
        treasureBoxScroll.column = 1
        treasureBoxScroll.itemWidth = 110
        treasureBoxScroll.itemHeight = 73
        treasureBoxScroll.dataArray = allTreasureBoxIdxList
        treasureBoxScroll.validateNow()

    def treasureBoxScrollLabelFunction(self, *args):
        curTreasureBoxData = self.curLuckyLotteryInfo.get('treasureBoxes', [])
        allTreasureBoxData = RLLD.data.get(self.curRLLDId, {}).get('treasureBoxBonus', ())
        treasureBoxIdx = int(args[3][0].GetNumber())
        treasureBoxData = allTreasureBoxData[treasureBoxIdx]
        treasureBoxMc = ASObject(args[3][1])
        treasureBoxMc.treasureBoxNum.htmlText = treasureBoxData[0]
        treasureBoxMc.treasureBoxIdx = treasureBoxIdx
        TipManager.addItemTipById(treasureBoxMc, treasureBoxData[1])
        if treasureBoxIdx in curTreasureBoxData:
            treasureBoxMc.Button.enabled = True
            treasureBoxMc.Button.removeEventListener(events.MOUSE_CLICK, self.handleTreasureBoxClick)
            treasureBoxMc.received.visible = True
            ASUtils.setHitTestDisable(treasureBoxMc.Button, True)
        else:
            treasureBoxMc.received.visible = False
            if self.curLuckyDrawCount >= allTreasureBoxData[treasureBoxIdx][0]:
                treasureBoxMc.Button.enabled = True
                treasureBoxMc.Button.addEventListener(events.MOUSE_CLICK, self.handleTreasureBoxClick, False, 0, True)
                ASUtils.setHitTestDisable(treasureBoxMc.Button, False)
            else:
                treasureBoxMc.Button.enabled = False

    def refreshDrawCnt(self):
        if not self.widget:
            return
        self.widget.drawCnt.text = gameStrings.LUCKY_LOTTERY_TREASURE_BOX_COUNT % str(self.curLuckyDrawCount)

    def refreshDrawItem(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.moneyIcon.bonusType = 'tianBi'
        self.widget.leftMoneyNums.text = str(p.unbindCoin + p.bindCoin + p.freeCoin)
        drawItemIcon = RLLD.data.get(self.curRLLDId, {}).get('showDrawItemIcon', 'tianBi')
        drawItemId = RLLD.data.get(self.curRLLDId, {}).get('showDrawItemId', 0)
        self.widget.drawItemIcon.bonusType = drawItemIcon
        self.widget.leftDrawItemNums.text = str(p.inv.countItemInPages(drawItemId, enableParentCheck=True))
        self.widget.openShopBtn.addEventListener(events.MOUSE_CLICK, self.handleOpenShopBtnClick, False, 0, True)
        self.widget.openShopBtn.label = self.getCurCompositeShopName()

    def refreshLeftTime(self):
        self.leftTimer and BigWorld.cancelCallback(self.leftTimer)
        self.leftTimer = None
        if not self.widget:
            return
        else:
            endTime = RLLD.data.get(self.curRLLDId, {}).get('endTime', None)
            leftTime = 0
            if utils.getDisposableCronTabTimeStamp(endTime) >= utils.getNow():
                leftTime = utils.getDisposableCronTabTimeStamp(endTime) - utils.getNow()
            if leftTime > 0:
                showLeftTimeByDay = RLLD.data.get(self.curRLLDId, {}).get('showLeftTimeByDay', 0)
                if showLeftTimeByDay == 0 or utils.getFormatDurationList(leftTime)[0] >= showLeftTimeByDay:
                    self.widget.leftTimeTxt.visible = False
                    self.widget.leftTime.visible = False
                    return
                self.widget.leftTime.visible = True
                self.widget.leftTimeTxt.visible = True
                self.widget.leftTimeTxt.text = utils.formatDurationV2(leftTime, showNums=2)
                self.leftTimer = BigWorld.callback(1, self.refreshLeftTime)
            else:
                gameglobal.rds.ui.activitySale.refreshInfo()
            return

    def getDrawCondition(self, drawConditionIdx):
        drawBtnInfo = RLLD.data.get(self.curRLLDId, {}).get('drawBtnInfo', (('tianbi', '', ''), ('tianbi', '', '')))
        drawCondition = RLLD.data.get(self.curRLLDId, {}).get('drawCondition', ((1, 0, 1), (5, 0, 5)))
        result = dict()
        result['bonusType'] = drawBtnInfo[drawConditionIdx][0]
        result['drawBtnLabel'] = drawBtnInfo[drawConditionIdx][1]
        result['mallKeyWord'] = drawBtnInfo[drawConditionIdx][2]
        result['drawNum'] = drawCondition[drawConditionIdx][0]
        result['drawItemId'] = drawCondition[drawConditionIdx][1]
        result['drawItemNum'] = drawCondition[drawConditionIdx][2]
        return result

    def checkItemEnough(self, itemId, needItemNums):
        p = BigWorld.player()
        curItemNums = p.inv.countItemInPages(itemId, enableParentCheck=True)
        return curItemNums >= needItemNums

    def openTianyuMall(self, keyWord):
        gameglobal.rds.ui.tianyuMall.show(keyWord=keyWord)

    def checkItemIsRare(self, itemId, itemNums):
        rareItem = RLLD.data.get(self.curRLLDId, {}).get('rareItem', ())
        if not rareItem:
            return False
        if itemId == rareItem[0] and itemNums == rareItem[1]:
            return True
        return False

    def getCurCompositeShopName(self):
        shopId = RLLD.data.get(self.curRLLDId, {}).get('compositeShopId', 0)
        return CSD.data.get(shopId, {}).get('shopName', gameStrings.BF_DOTA_OPEN_SHOP)

    def getItemIdxInAllLuckyItems(self, curRLLDId, itemData):
        showLuckyItems = RLLD.data.get(curRLLDId, {}).get('showLuckyItems', ())
        allIdxList = list()
        for idx, luckyItemData in enumerate(showLuckyItems):
            if itemData[0] == luckyItemData[0] and itemData[1] == luckyItemData[1]:
                allIdxList.append(idx)

        if not allIdxList:
            return None
        else:
            return random.choice(allIdxList)

    def getLuckyLotteryInfoById(self, RLLDId):
        p = BigWorld.player()
        if not hasattr(p, 'luckyLotteryInfo') or not p.luckyLotteryInfo:
            return {}
        return p.luckyLotteryInfo.get(RLLDId, {})

    def pushLuckylotteryMsg(self, RLLDId):
        if not self.checkCanOpen(RLLDId):
            return
        pushId = RLLD.data.get(RLLDId, {}).get('pushId', 0)
        pushId and gameglobal.rds.ui.pushMessage.addPushMsg(pushId)

    def setLuckyLotteryPushMsgCallBack(self, RLLDId):
        if not self.checkCanOpen(RLLDId):
            return
        pushId = RLLD.data.get(RLLDId, {}).get('pushId', 0)
        pushId and gameglobal.rds.ui.pushMessage.setCallBack(pushId, {'click': Functor(self.luckyLotteryMsgCallBack, RLLDId)})

    def luckyLotteryMsgCallBack(self, RLLDId):
        self.removeLuckylotteryPushMsg(RLLDId=RLLDId)
        gameglobal.rds.ui.activitySale.show(uiConst.ACTIVITY_SALE_TAB_LUCKY_LOTTERY)

    def removeLuckylotteryPushMsg(self, RLLDId = 0):
        pushId = RLLD.data.get(RLLDId, {}).get('pushId', 0)
        if pushId:
            gameglobal.rds.ui.pushMessage.removePushMsg(pushId)
            return
        for RLLDData in RLLD.data.itervalues():
            pushId = RLLDData.get('pushId', 0)
            pushId and gameglobal.rds.ui.pushMessage.removePushMsg(pushId)
