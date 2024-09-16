#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/randomTreasureBagMainProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import events
import sMath
import utils
import const
import clientUtils
import random
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import TipManager
from guis.asObject import ASUtils
from guis.asObject import ASObject
from guis import uiUtils
from callbackHelper import Functor
from item import Item
from uiProxy import UIProxy
from data import consumable_item_data as CID
from data import random_treasure_bag_lottery_data as RTBLD
from data import random_treasure_bag_lottery_group_data as RTBLGD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
TEMP_ICON_PATH = 'item/icon/42236.dds'
MAX_ITEM_NUM = 9
ADD_ICON_TYPE_MALL = 1
ADD_ICON_TYPE_ACTIVITY_SALE = 2
ADD_ICON_TYPE_RANDOM_TREASURE_BAG = 3
ADD_ICON_TYPE_PLAY_RECOMM = 4

class RandomTreasureBagMainProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RandomTreasureBagMainProxy, self).__init__(uiAdapter)
        self.widget = None
        self.enableScrollToCurBag = False
        self._allDataDict = {}
        self.curBagId = 0
        self.tempItemList = []
        self.tempMsgList = []
        self.drawing = False
        self.timer = None
        self._maxBagIdPushId = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_RANDOM_TREASURE_BAG_MAIN, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_RANDOM_TREASURE_BAG_MAIN:
            self.widget = widget
            self.reset()
            self.initUI()
            self.refreshAll()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RANDOM_TREASURE_BAG_MAIN)
        BigWorld.player().unRegisterEvent(const.EVENT_ITEM_CHANGE, self.itemChange)
        BigWorld.player().unRegisterEvent(const.EVENT_ITEM_REMOVE, self.itemChange)

    def show(self, bagId = 0, checkHaveNewReward = False, enableScrollToCurBag = False):
        if not gameglobal.rds.configData.get('enableRandomTreasureBagMain', False):
            return
        self.enableScrollToCurBag = enableScrollToCurBag
        self.initAllDataDict()
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        self.removeNewUpdateMsg()
        if self.checkCanOpenMainProxy():
            self.requestAllData()
            if bagId:
                self.curBagId = bagId
            else:
                self.curBagId = self.allDataDict.iterkeys().next()
                if checkHaveNewReward:
                    canGetReward, bagId = self.getOneHaveNewRewardBagId()
                    if canGetReward:
                        self.curBagId = bagId
            bagValid, bagId = self.checkBagIdValid(self.curBagId, defaultId=True, showBagIdError=True)
            if not bagValid:
                self.hide()
                return
            self.curBagId = bagId
            if not self.widget:
                self.uiAdapter.loadWidget(uiConst.WIDGET_RANDOM_TREASURE_BAG_MAIN)
            else:
                self.refreshAll()
        else:
            self.hide()
            BigWorld.player().showGameMsg(GMDD.data.RANDOM_TREASURE_BAG_MAIN_NOT_BAG_NOW, ())
            return

    def requestAllData(self):
        BigWorld.player().getPlayerAllTreasureBagData(forceRefresh=False)
        BigWorld.player().cell.getRandomItemsLotteryInfo()

    def requestRandomItemsSelection(self, bagId, selectGroupItemIds):
        BigWorld.player().cell.randomItemsSelectionRequest(bagId, selectGroupItemIds)

    def requestResetItemsSelection(self, bagId):
        BigWorld.player().cell.randomItemsSelectionReset(bagId)

    def requestDrawItems(self, bagId):
        BigWorld.player().cell.randomItemsLotteryDrawRequest(bagId)

    def requesGetAccumulativeReward(self, bagId):
        BigWorld.player().cell.receiveRandomItemsLotteryDrawTotalReward(bagId)

    def requesGetAccumulativeRewardData(self, bagId):
        BigWorld.player().cell.getRoundFinishRewardMarginsData(bagId)

    def initAllDataDict(self):
        if self._allDataDict is None:
            self._allDataDict = dict()
        else:
            self._allDataDict.clear()
        for bagId, value in RTBLD.data.iteritems():
            startTime = value.get('crontabStart', '')
            endTIme = value.get('crontabEnd', '')
            if utils.inCrontabRange(startTime, endTIme):
                dataDict = dict()
                dataDict['startTime'] = value.get('crontabStart', '')
                dataDict['endTIme'] = value.get('crontabEnd', '')
                dataDict['bagName'] = value.get('tabLabel', '')
                dataDict['tabIconPath'] = value.get('tabIconPath', TEMP_ICON_PATH)
                dataDict['startTime'] = value.get('crontabStart', '')
                dataDict['endTime'] = value.get('crontabEnd', '')
                dataDict['consumeItemDataList'] = self.getConsumeItemDataListByBagId(bagId)
                dataDict['consumeItemBonusTypeDict'] = value.get('ticketIcon', {})
                dataDict['pushId'] = value.get('pushId', 0)
                dataDict['helpKey'] = value.get('helpKey', 0)
                dataDict['addIconClick'] = value.get('addIconClick', {})
                dataDict['isAutoSelected'] = value.get('isAutoSelected', 0)
                dataDict['canResetOp'] = value.get('resetOp', 0)
                dataDict['resetConsumeItemData'] = self.getResetConsumeItemDataByBagId(bagId, dataDict['canResetOp'])
                dataDict['groupIdList'] = self.getGroupIdListByBagId(bagId)
                dataDict['rareItemIdList'] = value.get('rareItemIds', ())
                dataDict['rareItemIdNumsList'] = value.get('rareItemIdNums', ())
                dataDict['presetGroupItemDataDict'] = value.get('preLotteryItems', {})
                dataDict['canAccumulativeRewardOp'] = value.get('totalRancomLotteryRewardOp', 0)
                dataDict['baseRewardDict'], dataDict['baseRewardMaxRonudIndex'] = self.getBaseAccumulativeRewardDataDictByBagId(bagId, dataDict['canAccumulativeRewardOp'])
                dataDict['canAccumulativeLoopRewardOp'] = value.get('loopOp', 0)
                dataDict['loopNumsForGetReward'] = value.get('loopMargin', 1)
                dataDict['loopBonusId'] = value.get('loopBonusId', 0)
                dataDict['loopLimitNums'] = value.get('maxNum', 9999999)
                dataDict['awardQuest'] = value.get('awardQuest', ())
                dataDict['awardQuestDesc'] = value.get('awardQuestDesc', '')
                self._allDataDict[bagId] = dataDict

    def initUI(self):
        self.initMain()
        self.initOtherUI()

    def initOtherUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.rareItemOpenMc.visible = False

    def initMain(self):
        BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.itemChange)
        BigWorld.player().registerEvent(const.EVENT_ITEM_REMOVE, self.itemChange)

    def itemChange(self, *args):
        self.refreshLeftDaoJuIcon()

    def handleClickAwardQuest(self, *args):
        gameglobal.rds.ui.turnOverCardAward.show(const.SHOW_TYPE_RANDOM_TREASURE_BAG_MAIN)

    def handleClickGetAccumulativeReward(self, *args):
        if not self.drawing:
            self.requesGetAccumulativeReward(self.curBagId)

    def tabLabelFunction(self, *args):
        bagId = int(args[3][0].GetNumber())
        bagTabMc = ASObject(args[3][1])
        dataDict = self.getBagDataById(bagId)
        if dataDict:
            bagTabMc.bagId = bagId
            bagTabMc.label = str(dataDict['bagName'])
            bagTabMc.tabIcon.fitSize = True
            _, isCanGet, _ = self.getAccumulativeRewardData(bagId)
            bagTabMc.redPoint.visible = isCanGet
            bagTabMc.tabIcon.loadImage(dataDict['tabIconPath'])
            bagTabMc.addEventListener(events.MOUSE_CLICK, self.handleTabItemClick, False, 0, True)
            bagTabMc.selected = bagId == self.curBagId

    def handleTabItemClick(self, *args):
        if not self.drawing:
            e = ASObject(args[3][0])
            if self.curBagId != int(e.currentTarget.bagId):
                self.curBagId = int(e.currentTarget.bagId)
                self.refreshAll()

    def handleDaojuBtnClick(self, *args):
        if not self.drawing:
            pass
        addIconClickData = self.curBagData.get('addIconClick', {})
        if addIconClickData:
            if addIconClickData[0] == ADD_ICON_TYPE_MALL:
                keyWord = str(addIconClickData[1])
                gameglobal.rds.ui.tianyuMall.show(keyWord=keyWord)
            elif addIconClickData[0] == ADD_ICON_TYPE_ACTIVITY_SALE:
                if not gameglobal.rds.configData.get('enableActivitySale', False):
                    return
                if BigWorld.player().lv < SCD.data.get('activitySaleMinLv', 0):
                    return
                if not gameglobal.rds.ui.activitySale.checkPanelVisible():
                    return
                tabIdx = addIconClickData[1]
                if gameglobal.rds.ui.activitySale.checkTabIdxValid(tabIdx):
                    gameglobal.rds.ui.activitySale.show(tabIdx)
                else:
                    BigWorld.player().showGameMsg(GMDD.data.RANDOM_TREASURE_BAG_MAIN_SKIP_ERROR, ())
            elif addIconClickData[0] == ADD_ICON_TYPE_RANDOM_TREASURE_BAG:
                bagId = addIconClickData[1]
                bagValid, bagId = self.checkBagIdValid(bagId, defaultId=False, showBagIdError=False)
                if bagValid:
                    self.show(bagId=bagId)
                else:
                    BigWorld.player().showGameMsg(GMDD.data.RANDOM_TREASURE_BAG_MAIN_SKIP_ERROR, ())
            elif addIconClickData[0] == ADD_ICON_TYPE_PLAY_RECOMM:
                subTabIdx = addIconClickData[1]
                gameglobal.rds.ui.playRecomm.show(tabIdx=uiConst.PLAY_RECOMMV2_TAB_ACTIVITY_IDX, subTabIdx=subTabIdx)

    def handleAddItemGroup(self, *args):
        if not self.drawing:
            if not self.curBagData['isAutoSelected']:
                gameglobal.rds.ui.randomTreasureBagSelect.show(self.curBagId)
            else:
                allSelectData = gameglobal.rds.ui.randomTreasureBagSelect.processStaticData(self.curBagData['presetGroupItemDataDict'])
                self.addGroupItemData(self.curBagId, allSelectData)

    def handleDrawClick(self, *args):
        if not self.drawing:
            self.requestDrawItems(self.curBagId)

    def handleResetClick(self, *args):
        if not self.drawing:
            resetMsgId = GMDD.data.RANDOM_TREASURE_BAG_MAIN_RESET_CONFIRM_HINT
            msg = GMD.data.get(resetMsgId, {}).get('text', '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.requestResetItemsSelection, self.curBagId))

    def refreshAll(self):
        if not self.widget:
            return
        bagValid = self.refreshAllData()
        if bagValid:
            self.refreshUI()
        else:
            self.hide()
            return

    def refreshAllData(self):
        if not self.widget:
            return
        self.initAllDataDict()
        bagValid, newBagId = self.checkBagIdValid(self.curBagId, defaultId=True, showBagIdError=False)
        if bagValid:
            self.curBagId = newBagId
        return bagValid

    def refreshUI(self):
        if not self.widget:
            return
        self.refreshTabUI()
        self.refreshaAccumulativeReward()
        self.refreshConsumeDaoJuIcon()
        self.refreshLeftTimeMc()
        self.refreshHelpKey()
        self.refreshGroupItem()
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def refreshTabUI(self):
        listMc = self.widget.tabList
        curScrollPos = listMc.getScrollToPos()
        listMc.itemRenderer = 'RandomTreasureBagMain_tabItem'
        listMc.lableFunction = self.tabLabelFunction
        listMc.column = 1
        listMc.itemWidth = 113
        listMc.itemHeight = 112
        listMc.dataArray = list(self.allDataDict.keys())
        listMc.validateNow()
        listMc.scrollTo(curScrollPos)
        if self.enableScrollToCurBag and self.curBagScrollIndex != -1:
            self.enableScrollToCurBag = False
            posY = listMc.getIndexPosY(self.curBagScrollIndex)
            listMc.scrollTo(posY)

    def refreshaAccumulativeReward(self):
        self.widget.accumulativeRewardTitle.visible = False
        self.widget.accumulativeReward.visible = False
        self.widget.accumulativeRewardQuest.visible = False
        self.widget.canReceive.visible = False
        bonusId, isCanGet, haveGot = self.getAccumulativeRewardData(self.curBagId)
        if bonusId:
            itemId, itemNums = self.getOneItemDataByBonusID(bonusId)
            isRare = self.checkItemIsRare(itemId, itemNums)
            self.widget.canReceive.visible = isCanGet
            self.setRewardItemMc(self.widget.accumulativeReward, itemId, itemNums, haveGot=haveGot, isRare=isRare, isCanShowFit=False)
            self.widget.accumulativeReward.addEventListener(events.MOUSE_CLICK, self.handleClickGetAccumulativeReward, False, 0, True)
            self.widget.accumulativeRewardTitle.visible = True
            self.widget.accumulativeRewardTitle.text = gameStrings.RANDOM_TREASURE_BAG_MAIN_AWARD_ALL_GET if haveGot else gameStrings.RANDOM_TREASURE_BAG_MAIN_AWARD_CAN_GET
            self.widget.accumulativeReward.visible = True
            self.widget.accumulativeRewardQuest.visible = True
            self.widget.accumulativeRewardQuest.addEventListener(events.MOUSE_CLICK, self.handleClickAwardQuest, False, 0, True)
            self.widget.accumulativeRewardQuest.htmlText = self.curBagData.get('awardQuestDesc', gameStrings.RANDOM_TREASURE_BAG_MAIN_AWARD_QUEST_TITLE)

    def refreshConsumeDaoJuIcon(self):
        self.widget.AddDaoJuBtn.enabled = len(self.curBagData.get('addIconClick', {})) > 0
        self.widget.AddDaoJuBtn.addEventListener(events.MOUSE_CLICK, self.handleDaojuBtnClick, False, 0, True)
        self.refreshLeftDaoJuIcon()
        self.widget.drawDaoJuIcon.bonusType = self.curConsumeItemBonusType
        self.widget.drawNums.text = 'X %d' % self.curConsumeItemNums
        self.widget.drawDaoJuIcon.visible = not self.isCurFreeDraw and self.IsCanDrawAndReset and self.IsCanRealDraw
        self.widget.drawNums.visible = not self.isCurFreeDraw and self.IsCanDrawAndReset and self.IsCanRealDraw
        self.widget.drawBtn.label = gameStrings.RANDOM_TREASURE_BAG_MAIN_FREE_DRAW if self.isCurFreeDraw and self.IsCanRealDraw else gameStrings.RANDOM_TREASURE_BAG_MAIN_NORMAL_DRAW
        self.widget.drawBtn.addEventListener(events.BUTTON_CLICK, self.handleDrawClick, False, 0, True)
        self.widget.drawBtn.enabled = self.IsCanDrawAndReset and self.IsCanRealDraw
        self.widget.drawBtn.visible = self.IsCanDrawAndReset
        if self.curBagData['canResetOp']:
            self.widget.resetDaoJuIcon.bonusType = self.curResetItemBonusType
            self.widget.resetDaoJuIcon.visible = self.IsCanDrawAndReset and self.IsCanRealDraw and self.curResetItemNums != 0
            self.widget.resetNums.visible = self.IsCanDrawAndReset and self.IsCanRealDraw and self.curResetItemNums != 0
            self.widget.resetNums.text = 'X %d' % self.curResetItemNums
            self.widget.resetBtn.visible = self.IsCanDrawAndReset
            resetBtnLabel = gameStrings.RANDOM_TREASURE_BAG_MAIN_NORMAL_RESET
            if self.curResetItemNums == 0:
                resetBtnLabel = gameStrings.RANDOM_TREASURE_BAG_MAIN_FREE_RESET
            if not self.IsCanRealDraw:
                resetBtnLabel = gameStrings.RANDOM_TREASURE_BAG_MAIN_NEW_RESET
            self.widget.resetBtn.label = resetBtnLabel
            self.widget.resetBtn.addEventListener(events.BUTTON_CLICK, self.handleResetClick, False, 0, True)
            self.widget.resetBtn.enabled = self.IsCanDrawAndReset
        else:
            self.widget.resetDaoJuIcon.visible = False
            self.widget.resetNums.visible = False
            self.widget.resetBtn.visible = False

    def refreshLeftDaoJuIcon(self):
        if not self.widget:
            return
        self.widget.leftDrawDaoJuIcon.bonusType = self.curConsumeItemBonusType
        self.widget.leftDaoJuNums.text = self.getItemNumsByID(self.curConsumeItemId)

    def refreshLeftTimeMc(self):
        self.timer and BigWorld.cancelCallback(self.timer)
        self.timer = None
        if not self.widget:
            return
        else:
            endTime = self.curBagData.get('endTime', '')
            left = 0
            if utils.getDisposableCronTabTimeStamp(endTime) >= utils.getNow():
                left = utils.getDisposableCronTabTimeStamp(endTime) - utils.getNow()
            if left > 0:
                self.widget.leftTime.visible = True
                self.widget.leftTime.text = gameStrings.RANDOM_TREASURE_BAG_MAIN_LEFT_TIME + utils.formatDurationShortVersion(left)
                self.timer = BigWorld.callback(1, self.refreshLeftTimeMc)
            else:
                self.widget.leftTime.visible = False
            return

    def refreshHelpKey(self):
        self.widget.helpIcon.helpKey = self.curBagData.get('helpKey', 0)

    def refreshGroupItem(self):
        if self.IsCanDrawAndReset:
            self.widget.addGroupBtn.visible = False
            self.widget.addGroupBtnHint.visible = False
            self.widget.itemGroup.visible = True
            self.hideAllSelectItemEffect()
            self.refreshSelectedGroupItem()
        else:
            self.widget.addGroupBtn.visible = True
            self.widget.addGroupBtnHint.visible = True
            self.widget.addGroupBtnHint.addGroupBtnHintText.text = gameStrings.RANDOM_TREASURE_BAG_MAIN_ADD_GROUP_BTN_HINT if not self.curBagData['isAutoSelected'] else gameStrings.RANDOM_TREASURE_BAG_MAIN_ADD_GROUP_BTN_HINT_WITHOUT_SELECT
            self.widget.addGroupBtn.addEventListener(events.MOUSE_CLICK, self.handleAddItemGroup, False, 0, True)
            self.widget.itemGroup.visible = False

    def refreshSelectedGroupItem(self):
        for groupId, itemsData in self.curRandomSelectData.iteritems():
            for itemdata in itemsData:
                itemId = itemdata[0]
                itemPos = itemdata[1]
                itemNums = self.getSelectItemNumsFromRTBLGD(groupId=groupId, itemId=itemId)
                itemMc = getattr(self.widget.itemGroup, 'item%d' % itemPos)
                itemMc.gotoAndStop(1)
                isRare = self.checkItemIsRare(itemId, itemNums)
                isGray = itemPos in self.curFinishPosList
                isNew = False
                if self.curBagDrawNums > 0 and self.curFinishPosList[-1] == itemPos:
                    isNew = True
                self.setRewardItemMc(itemMc.itemOutside.itemInside, itemId, itemNums=itemNums, isRare=isRare, isGray=isGray, isNew=isNew)

    def addGroupItemData(self, bagId, allSelectItemData):
        if not self.widget:
            return
        randomPosList = self.randomIntergerList(MAX_ITEM_NUM)
        posOfListIdx = 0
        selectGroupItemIdsList = []
        for groupId, groupSelectData in allSelectItemData.iteritems():
            selectGroupItemDict = dict()
            selectGroupItemDict['groupId'] = groupId
            selectGroupItemDict['itemIds'] = list()
            for itemId, itemNums in groupSelectData.iteritems():
                for idx in xrange(itemNums):
                    if posOfListIdx >= MAX_ITEM_NUM:
                        break
                    dictData = {'itemId': itemId,
                     'pos': randomPosList[posOfListIdx]}
                    selectGroupItemDict['itemIds'].append(dictData)
                    posOfListIdx += 1

            selectGroupItemIdsList.append(selectGroupItemDict)

        self.requestRandomItemsSelection(bagId, selectGroupItemIdsList)

    def randomIntergerList(self, maxNums):
        resultList = [ value for value in xrange(maxNums) ]
        random.shuffle(resultList)
        return resultList

    def checkHaveNewReward(self):
        for bagId in self.allDataDict.iterkeys():
            bonusId, isCanGet, haveGot = self.getAccumulativeRewardData(bagId)
            if isCanGet:
                return True

        return False

    def getOneHaveNewRewardBagId(self):
        for bagId in self.allDataDict.iterkeys():
            bonusId, isCanGet, haveGot = self.getAccumulativeRewardData(bagId)
            if isCanGet:
                return (True, bagId)

        return (False, 0)

    def setRewardItemMc(self, itemMc, itemId, itemNums = 1, iconSize = uiConst.ICON_SIZE110, isGray = False, haveGot = False, isRare = False, isNew = False, isCanShowFit = True):
        rewardMc = itemMc.rewardMc
        iconPath = uiUtils.getItemIconPath(itemId, iconSize)
        quality = uiUtils.getItemQuality(itemId)
        color = uiUtils.getColorByQuality(quality)
        rewardMc.itemIconMc.fitSize = True
        rewardMc.itemIconMc.loadImage(iconPath)
        rewardMc.itemQualityIcon.gotoAndStop(color)
        rewardMc.grayMc.visible = isGray
        rewardMc.hasGotMc.visible = haveGot
        rewardMc.valueAmountMc.visible = False
        rewardMc.newMc.visible = isNew
        rewardMc.rare1Mc.visible = isRare
        rewardMc.rare2Mc.visible = isRare
        itemMc.itemId = itemId
        if isCanShowFit:
            itemMc.addEventListener(events.BUTTON_CLICK, self.handleShowFit, False, 0, True)
        else:
            itemMc.removeEventListener(events.BUTTON_CLICK, self.handleShowFit)
        TipManager.addItemTipById(itemMc, itemId)
        if itemNums > 1:
            rewardMc.valueAmountMc.visible = True
            rewardMc.valueAmountMc.text = itemNums

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

    def hideAllSelectItemEffect(self):
        if not self.widget:
            return
        for idx in xrange(MAX_ITEM_NUM):
            itemSelectMc = getattr(self.widget.itemGroup, 'itemSelect%d' % idx)
            itemSelectMc.visible = False

    def enQueueLotteryItem(self, kind, item, page, pos):
        tempItem = (kind,
         item,
         page,
         pos)
        self.tempItemList.append(tempItem)

    def outQueueLotteryItem(self):
        for item in self.tempItemList:
            BigWorld.player().resInsertNew(item[0], item[1], item[2], item[3])

        del self.tempItemList[:]

    def enQueueLotteryMsg(self, msgId, data):
        tempMsg = (msgId, data)
        self.tempMsgList.append(tempMsg)

    def outQueueLotteryMsg(self):
        for msg in self.tempMsgList:
            BigWorld.player().showGameMsg(msg[0], msg[1])

        del self.tempMsgList[:]

    def startSelectItem(self, bagId, itemData):
        groupId = itemData[0][0]
        itemId = itemData[0][1]
        itemPos = itemData[0][2]
        if self.curBagId == bagId:
            leftTime = self.beforeSelectItem(itemPos)
            self.RecurveItemEffect(groupId, itemId, leftTime, itemPos, lastItemIdx=-1)
        else:
            self.afterSelectItem(groupId, itemId, -1)

    def beforeSelectItem(self, selectedIdx):
        self.drawing = True
        self.setOtherInValid(False)
        return selectedIdx + MAX_ITEM_NUM

    def RecurveItemEffect(self, groupId, itemId, leftTime, selectedIdx, lastItemIdx = -1):
        if not self.widget:
            self.afterSelectItem(groupId, itemId, lastItemIdx)
            return
        if lastItemIdx != -1:
            lastItemSelectMc = getattr(self.widget.itemGroup, 'itemSelect%d' % lastItemIdx)
            lastItemSelectMc.visible = False
        while leftTime >= 0:
            lastItemIdx = (lastItemIdx + 1) % MAX_ITEM_NUM
            if lastItemIdx in self.curFinishPosList and lastItemIdx != selectedIdx:
                leftTime -= 1
            else:
                lastItemSelectMc = getattr(self.widget.itemGroup, 'itemSelect%d' % lastItemIdx)
                lastItemSelectMc.visible = True
                leftTime -= 1
                break

        if leftTime == -1:
            BigWorld.callback(0.25, Functor(self.afterSelectItem, groupId, itemId, lastItemIdx))
            return
        BigWorld.callback(0.25, Functor(self.RecurveItemEffect, groupId, itemId, leftTime, selectedIdx, lastItemIdx))

    def afterSelectItem(self, groupId, itemId, lastItemIdx):
        self.drawing = False
        self.playPitchOnItemAni(itemId, lastItemIdx)
        self.outQueueLotteryItem()
        self.outQueueLotteryMsg()
        self.openRareItem(groupId, itemId)

    def playPitchOnItemAni(self, itemId, lastItemIdx):
        if not self.widget:
            return
        elif lastItemIdx == -1:
            return
        else:
            lastItemSelectMc = getattr(self.widget.itemGroup, 'itemSelect%d' % lastItemIdx, None)
            if lastItemSelectMc:
                lastItemSelectMc.visible = False
            itemMc = getattr(self.widget.itemGroup, 'item%d' % lastItemIdx)
            if itemMc:
                itemMc.gotoAndPlay(1)
                ASUtils.callbackAtFrame(itemMc, 27, self.itemPlayEndCB)
            return

    def itemPlayEndCB(self, *arg):
        self.setOtherInValid(True)
        self.refreshAll()

    def setOtherInValid(self, valid):
        if not self.widget:
            return
        self.widget.AddDaoJuBtn.enabled = valid
        self.widget.resetBtn.enabled = valid
        self.widget.drawBtn.enabled = valid

    def openRareItem(self, groupId, itemId):
        if not self.widget:
            return
        self.widget.stage.addEventListener(events.MOUSE_CLICK, self.afterShowRareItem)
        itemNums = self.getSelectItemNumsFromRTBLGD(groupId=groupId, itemId=itemId)
        if self.checkItemIsRare(itemId, itemNums):
            rareMc = self.widget.rareItemOpenMc
            rareMc.visible = True
            iconPath = uiUtils.getItemIconFile110(itemId)
            rareMc.item.icon.icon.fitSize = True
            rareMc.item.icon.icon.loadImage(iconPath)
            rareMc.play()
            ASUtils.callbackAtFrame(rareMc, 110, self.afterShowRareItem)

    def afterShowRareItem(self, *args):
        if not self.widget:
            return
        self.widget.stage.removeEventListener(events.MOUSE_CLICK, self.afterShowRareItem)
        rareMc = self.widget.rareItemOpenMc
        rareMc.visible = False

    @property
    def maxBagId(self):
        if self.allDataDict.keys():
            return max(self.allDataDict.keys())
        return 0

    @property
    def maxPushIdWithBagId(self):
        realPushId = 0
        realBagId = 0
        for bagId, data in self.allDataDict.iteritems():
            if realPushId < data['pushId']:
                realPushId = data['pushId']
                realBagId = bagId

        return (realPushId, realBagId)

    def pushNewUpdateMsg(self):
        if gameglobal.rds.configData.get('enableRandomTreasureBagMainMessagePush', False):
            pushId, _ = self.maxPushIdWithBagId
            if pushId:
                gameglobal.rds.ui.pushMessage.addPushMsg(pushId)

    def removeNewUpdateMsg(self):
        pushId, _ = self.maxPushIdWithBagId
        if pushId:
            gameglobal.rds.ui.pushMessage.removePushMsg(pushId)

    def setNewUpdateMsgCallBack(self):
        if gameglobal.rds.configData.get('enableRandomTreasureBagMainMessagePush', False):
            pushId, bagId = self.maxPushIdWithBagId
            if pushId:
                gameglobal.rds.ui.pushMessage.setCallBack(pushId, {'click': Functor(self.show, bagId)})

    def checkCanOpenMainProxy(self):
        p = BigWorld.player()
        if len(self.allDataDict) <= 0:
            return False
        if p.lv < SCD.data.get('activitySaleMinLv', 17):
            return False
        return True

    def checkBagIdValid(self, BagId, defaultId = True, showBagIdError = False):
        self.initAllDataDict()
        newBagId = 0
        if len(self.allDataDict) > 0:
            if BagId not in self.allDataDict.keys():
                if showBagIdError:
                    BigWorld.player().showGameMsg(GMDD.data.RANDOM_TREASURE_BAG_MAIN_NOT_BAG_NOW, ())
                if defaultId:
                    newBagId = self.allDataDict.iterkeys().next()
                    return (True, newBagId)
                else:
                    return (False, 0)
            else:
                return (True, BagId)
        else:
            if showBagIdError:
                BigWorld.player().showGameMsg(GMDD.data.RANDOM_TREASURE_BAG_MAIN_NOT_BAG_NOW, ())
            return (False, 0)

    def getConsumeItemDataListByBagId(self, bagId):
        consumeItemIds = RTBLD.data[bagId].get('consumeItemIds', ())
        consumeNums = RTBLD.data[bagId].get('consumeNums', ())
        result = list()
        for index, val in enumerate(consumeItemIds):
            itemId = val[0]
            itemNums = consumeNums[index]
            result.append((itemId, itemNums))

        return result

    def getResetConsumeItemDataByBagId(self, bagId, canResetOp):
        result = (0, 0)
        if canResetOp:
            resetConsumeItemIds = RTBLD.data[bagId].get('resetConsumeItemIds', ())
            resetConsumeNum = RTBLD.data[bagId].get('resetConsumeNum', 0)
            result = (resetConsumeItemIds[-1], resetConsumeNum)
        return result

    def getGroupIdListByBagId(self, bagId):
        return RTBLD.data[bagId].get('groupList', ())

    def getBaseAccumulativeRewardDataDictByBagId(self, bagId, canAccumulativeRewardOp):
        result = dict()
        maxBaseRoundIndex = 0
        if canAccumulativeRewardOp:
            baseRoundIndexs = RTBLD.data[bagId].get('baseMargins', ())
            baseBonusIds = RTBLD.data[bagId].get('baseBonusIds', ())
            for index, roundIndex in enumerate(baseRoundIndexs):
                bonusId = baseBonusIds[index]
                result[roundIndex] = bonusId
                maxBaseRoundIndex = max(maxBaseRoundIndex, roundIndex)

        return (result, maxBaseRoundIndex)

    def getOneItemDataByBonusID(self, bonusID):
        itemDataList = clientUtils.genItemBonus(bonusID)
        if itemDataList:
            return (itemDataList[0][0], itemDataList[0][1])
        else:
            return (0, 0)

    def getItemNumsByID(self, itemID):
        p = BigWorld.player()
        return p.inv.countItemInPages(itemID, enableParentCheck=True)

    def checkItemIsRare(self, itemId, itemNums, bagId = 0):
        bagData = self.curBagData
        if bagId:
            bagData = self.getBagDataById(bagId)
        if itemId in bagData['rareItemIdList']:
            return True
        for rareItemIdNums in bagData['rareItemIdNumsList']:
            rareItemId = rareItemIdNums[0]
            rareItemNumsList = rareItemIdNums[1]
            if rareItemId == itemId and itemNums in rareItemNumsList:
                return True

        return False

    def getAccumulativeRewardData(self, bagId):
        bonusId = 0
        isCanGet = False
        haveGot = False
        if self.getBagDataById(bagId)['canAccumulativeRewardOp']:
            bonusId, isCanGet, haveGot = self.getBonusDataOfBaseRewardValidById(bagId)
        if self.getBagDataById(bagId)['canAccumulativeLoopRewardOp']:
            if self.checkBagIsInLoopRewardById(bagId):
                bonusId, isCanGet, haveGot = self.getCurBonusDataOfLoopRewardValid(bagId)
        return (bonusId, isCanGet, haveGot)

    def getBonusDataOfBaseRewardValidById(self, bagId):
        bagData = self.getBagDataById(bagId)
        bagServerData = self.getBagServerDataById(bagId)
        baseRewardIdxList = [ key for key in sorted(bagData['baseRewardDict'].iterkeys(), cmp=lambda x, y: x - y) ]
        curHaveGetBaseBonusIdx = -1
        for idx in xrange(len(baseRewardIdxList)):
            if bagServerData.get('curBaseBonusIndex', 0) == baseRewardIdxList[idx]:
                curHaveGetBaseBonusIdx = idx
                break

        nextCanGetBaseBonusIdx = len(baseRewardIdxList) - 1
        if curHaveGetBaseBonusIdx < len(baseRewardIdxList) - 1:
            nextCanGetBaseBonusIdx = curHaveGetBaseBonusIdx + 1
        isCanGet = False
        haveGot = False
        showBonusIdx = nextCanGetBaseBonusIdx
        if self.getBagTotalRoundCountById(bagId) >= baseRewardIdxList[nextCanGetBaseBonusIdx]:
            isCanGet = True
        else:
            isCanGet = False
        if curHaveGetBaseBonusIdx == nextCanGetBaseBonusIdx:
            isCanGet = False
            haveGot = True
            showBonusIdx = curHaveGetBaseBonusIdx
        curIdxOfBaseRewardDict = baseRewardIdxList[showBonusIdx]
        bonusId = bagData['baseRewardDict'].get(curIdxOfBaseRewardDict, 0)
        return (bonusId, isCanGet, haveGot)

    def getCurBonusDataOfLoopRewardValid(self, bagId):
        bagData = self.getBagDataById(bagId)
        bagServerData = self.getBagServerDataById(bagId)
        isCanGet = False
        haveGot = False
        bonusId = bagData['loopBonusId']
        bagLoopBonusIndex = bagServerData.get('curLoopBonusIndex', 0)
        if bagLoopBonusIndex:
            curLoopNums = self.getBagTotalRoundCountById(bagId) - bagLoopBonusIndex
            curLoopGetRewardNums = (bagLoopBonusIndex - bagData['baseRewardMaxRonudIndex']) // bagData['loopNumsForGetReward']
            if curLoopNums >= bagData['loopNumsForGetReward']:
                isCanGet = True
                if curLoopNums // bagData['loopNumsForGetReward'] == 1 and curLoopGetRewardNums > bagData['loopLimitNums']:
                    isCanGet = False
                    haveGot = True
        elif self.getBagTotalRoundCountById(bagId) - bagData['baseRewardMaxRonudIndex'] >= bagData['loopNumsForGetReward']:
            isCanGet = True
        return (bonusId, isCanGet, haveGot)

    def getSelectItemNumsFromRTBLGD(self, groupId, itemId):
        itemData = RTBLGD.data.get(groupId, {}).get('itemIds', {}).get(itemId, ())
        if not itemData:
            return 1
        else:
            return itemData[0]

    def getCurShowBagId(self):
        if self.curBagId == 0:
            return 1
        return self.curBagId

    def getCurShowAwardQuestData(self):
        return self.curBagData.get('awardQuest', ())

    @property
    def allDataDict(self):
        if not self._allDataDict:
            self.initAllDataDict()
        return self._allDataDict

    def getBagDataById(self, bagId):
        return self.allDataDict.get(bagId, {})

    @property
    def curBagData(self):
        return self.allDataDict.get(self.getCurShowBagId(), {})

    @property
    def curBagScrollIndex(self):
        for idx, bagId in enumerate(self.allDataDict.keys()):
            if bagId == self.curBagId:
                return idx

        return -1

    @property
    def curConsumeItemId(self):
        if self.IsCanRealDraw:
            itemData = self.curBagData['consumeItemDataList'][self.curBagDrawNums]
            itemId = itemData[0]
            return itemId
        else:
            return self.curBagData['consumeItemDataList'][0][0]

    @property
    def curConsumeItemNums(self):
        if self.IsCanRealDraw:
            itemData = self.curBagData['consumeItemDataList'][self.curBagDrawNums]
            itemNums = itemData[1]
            return itemNums
        else:
            return self.curBagData['consumeItemDataList'][0][1]

    @property
    def curConsumeItemBonusType(self):
        bonusType = self.curBagData['consumeItemBonusTypeDict'].get(self.curConsumeItemId, 'cash')
        return bonusType

    @property
    def curResetItemId(self):
        itemId = self.curBagData['resetConsumeItemData'][0]
        return itemId

    @property
    def curResetItemNums(self):
        itemNums = self.curBagData['resetConsumeItemData'][1]
        return itemNums

    @property
    def curResetItemBonusType(self):
        bonusType = self.curBagData['consumeItemBonusTypeDict'].get(self.curResetItemId, 'cash')
        return bonusType

    @property
    def isCurFreeDraw(self):
        if self.curConsumeItemNums == 0:
            return True
        else:
            return False

    def getBagServerDataById(self, bagId):
        p = BigWorld.player()
        allData = getattr(p, 'randomTreasureBag', {})
        if allData is None:
            return dict()
        else:
            return allData.get(bagId, {})

    def getBagTotalRoundCountById(self, bagId):
        return self.getBagServerDataById(bagId).get('totalLotteryCount', 0)

    def checkBagIsInLoopRewardById(self, bagId):
        curBaseBonusIndex = self.getBagServerDataById(bagId).get('curBaseBonusIndex', 0)
        if curBaseBonusIndex < self.getBagDataById(bagId)['baseRewardMaxRonudIndex']:
            return False
        return True

    @property
    def curBagServerData(self):
        return self.getBagServerDataById(self.curBagId)

    @property
    def IsCanDrawAndReset(self):
        if not self.curRandomSelectData:
            return False
        else:
            return True

    @property
    def IsCanRealDraw(self):
        if self.curBagDrawNums == MAX_ITEM_NUM:
            return False
        else:
            return True

    @property
    def curRandomSelectData(self):
        return self.curBagServerData.get('randomLotteryItems', {})

    @property
    def curFinishPosList(self):
        return self.curBagServerData.get('finishPosList', [])

    @property
    def curBagRoundNums(self):
        return self.curBagServerData.get('totalLotteryCount', 0)

    @property
    def curBagDrawNums(self):
        return len(self.curFinishPosList)

    @property
    def curBaseBonusIndex(self):
        return self.curBagServerData.get('curBaseBonusIndex', 0)

    @property
    def curLoopBonusIndex(self):
        return self.curBagServerData.get('curLoopBonusIndex', 0)

    @property
    def isCurLoopBonus(self):
        if self.curBaseBonusIndex < self.curBagData['baseRewardMaxRonudIndex']:
            return False
        return True
