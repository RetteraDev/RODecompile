#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/historyConsumedProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import utils
import events
import uiUtils
import clientUtils
import gametypes
import gamelog
from gamestrings import gameStrings
from uiTabProxy import UITabProxy
from guis.asObject import ASObject
from callbackHelper import Functor
from data import sys_config_data as SCD
from data import history_consumed_config_data as HCCD
from data import item_data as ID
from data import history_consumed_reward_data as HCRD
TAB_FIX_REWARD_INDEX = 0
TAB_CHOOSE_REWARD_INDEX = 1
FIXED_ITEM_INIT_X = 0
FIXED_ITEM_INIT_Y = 0
FIXED_ITEM_OFFSET_Y = 72
CHOOSE_ITEM_NUM_PER_LINE = 3

class HistoryConsumedProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(HistoryConsumedProxy, self).__init__(uiAdapter)
        self.tabType = UITabProxy.TAB_TYPE_CLS
        self.isRedPot = False
        self.clearAll()
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_HISTORY_CONSUMED, self.hide)

    def reset(self):
        super(HistoryConsumedProxy, self).reset()
        self.timer = None
        self.widget = None
        self.itemRenderMcList = []
        self.chooseItem = {}
        self.currentCost = 0

    def clearAll(self):
        self.actId = 0
        self.status = 0
        self.returnPoint = 0
        self.remainScore = 0
        self.rewardInfo = {}
        self.items = {}
        self.characterGbId = 0
        self.charge = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_HISTORY_CONSUMED:
            self.widget = widget
            self.delTimer()
            self.initUI()

    def clearWidget(self):
        super(HistoryConsumedProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_HISTORY_CONSUMED)

    def _getTabList(self):
        return [{'tabIdx': TAB_FIX_REWARD_INDEX,
          'tabName': 'btn0',
          'view': 'HistoryConsumed_tab0',
          'pos': (29, 96)}, {'tabIdx': TAB_CHOOSE_REWARD_INDEX,
          'tabName': 'btn1',
          'view': 'HistoryConsumed_tab1',
          'pos': (29, 96)}]

    def show(self):
        BigWorld.player().base.queryHistoryConsumedReward()
        self.removeHistoryConsumedPushMsg()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTabUI()
        self.timerFunc()
        self.addTimer()

    def refreshInfo(self):
        if not self.widget or not self.currentView:
            return
        volatileRewardPointLimit = HCCD.data.get(self.actId, {}).get('volatileRewardPointLimit', 0)
        if volatileRewardPointLimit and self.returnPoint < volatileRewardPointLimit:
            self.widget.setTabIndex(0)
            self.setTabVisible(1, False, True)
        if self.currentTabIndex == TAB_FIX_REWARD_INDEX:
            self.refreshFixItemPanel()
        elif self.currentTabIndex == TAB_CHOOSE_REWARD_INDEX:
            self.refreshChooseItemPanel()

    def onQueryHistoryConsumedReward(self, rewardData):
        self.actId = rewardData.get('actId', 0)
        self.status = rewardData.get('status', 0)
        self.returnPoint = rewardData.get('returnPoint', 0)
        self.remainScore = rewardData.get('remainScore', 0)
        self.rewardInfo = rewardData.get('rewardInfo', {})
        self.items = rewardData.get('items', {})
        self.characterGbId = rewardData.get('gbId')
        self.charge = rewardData.get('charge', 0)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_HISTORY_CONSUMED)
        else:
            self.initUI()
        if self.returnPoint:
            gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        self.refreshInfo()

    def onTabChanged(self, *args):
        super(HistoryConsumedProxy, self).onTabChanged(*args)
        self.refreshInfo()

    def refreshFixItemPanel(self):
        fixPanel = self.currentView
        fixPanel.banner.addEventListener(events.MOUSE_CLICK, self.handleClickBanner, False, 0, True)
        self.clearItem()
        data = HCCD.data.get(self.actId)
        posY = FIXED_ITEM_INIT_Y
        for index in data.get('fixedReward', ()):
            rewardInfo = HCRD.data.get(index, {})
            pointLimit = rewardInfo.get('pointLimit', (0, 0))
            lowLimit, upLimit = pointLimit
            if pointLimit and self.returnPoint < pointLimit[0]:
                continue
            itemRenderMc = self.widget.getInstByClsName('HistoryConsumed_rewardItem')
            fixPanel.rewardList.canvas.addChild(itemRenderMc)
            if pointLimit and pointLimit[0] > 0:
                itemRenderMc.pointLimitDesc.text = gameStrings.HISTORY_CONSUMED_POINT_LIMIT_DESC % (pointLimit[0] - 1)
            else:
                itemRenderMc.pointLimitDesc.visible = False
            self.itemRenderMcList.append(itemRenderMc)
            itemRenderMc.x = FIXED_ITEM_INIT_X
            itemRenderMc.y = posY
            posY += FIXED_ITEM_OFFSET_Y
            itemRenderMc.index = index
            itemRenderMc.rewardDesc.text = rewardInfo.get('rewardDesc', '')
            itemRenderMc.item0.visible = False
            itemRenderMc.item1.visible = False
            itemRenderMc.item2.visible = False
            money = rewardInfo.get('money')
            itemBonusId = rewardInfo.get('itemBonusId')
            timesLimit = rewardInfo.get('timesLimit', 1)
            totalChargeLimit = rewardInfo.get('totalChargeLimit', 0)
            currentItemIdx = 0
            if money:
                type = money[0]
                moneyLimit = money[1]
                rate = min(float(self.returnPoint - lowLimit + 1) / (upLimit - lowLimit), 1)
                realNum = int(rate * moneyLimit)
                iconId = SCD.data.get('historyConsumedMoneyIcon').get(type)
                itemMc = itemRenderMc.getChildByName('item%d' % currentItemIdx)
                itemMc.visible = True
                currentItemIdx += 1
                itemMc.setItemSlotData(uiUtils.getGfxItemById(iconId, realNum))
            if itemBonusId:
                itemBonus = clientUtils.genItemBonus(itemBonusId)
                itemMc = itemRenderMc.getChildByName('item%d' % currentItemIdx)
                itemMc.visible = True
                currentItemIdx += 1
                itemMc.setItemSlotData(uiUtils.getGfxItemById(itemBonus[0][0], itemBonus[0][1]))
                itemNum = len(itemBonus)
                if itemNum > 1:
                    itemMc = itemRenderMc.getChildByName('item%d' % currentItemIdx)
                    itemMc.visible = True
                    currentItemIdx += 1
                    itemMc.setItemSlotData(uiUtils.getGfxItemById(itemBonus[1][0], itemBonus[1][1]))
            if self.status == gametypes.HISTORY_CONSUMED_STATUS_CAN:
                itemRenderMc.receiveBtn.disabled = True
                itemRenderMc.receiveBtn.label = gameStrings.HISTORY_CONSUMED_DRAW
            elif self.status == gametypes.HISTORY_CONSUMED_STATUS_JOINED:
                if totalChargeLimit:
                    itemRenderMc.canReceive.text = gameStrings.HISTORY_CONSUMED_CHARGE_TIMES % (self.charge, int(totalChargeLimit))
                if timesLimit > 1:
                    itemRenderMc.canReceive.text = gameStrings.HISTORY_CONSUMED_RECEIVE_TIMES % (0, timesLimit)
                if index in self.rewardInfo.keys():
                    receivedInfo = self.rewardInfo.get(index, (0, 0, 0))
                    receivedTimes = receivedInfo[0]
                    isReceived = receivedInfo[1]
                    canReceive = receivedInfo[2]
                    if isReceived or timesLimit == receivedTimes:
                        itemRenderMc.receiveBtn.disabled = True
                        itemRenderMc.receiveBtn.label = gameStrings.HISTORY_CONSUMED_HAS_DRAW
                    elif canReceive:
                        itemRenderMc.receiveBtn.disabled = False
                        itemRenderMc.receiveBtn.label = gameStrings.HISTORY_CONSUMED_DRAW
                    else:
                        itemRenderMc.receiveBtn.disabled = True
                        itemRenderMc.receiveBtn.label = gameStrings.HISTORY_CONSUMED_NOT_ACHIEVE
                    if timesLimit > 1:
                        itemRenderMc.canReceive.text = gameStrings.HISTORY_CONSUMED_RECEIVE_TIMES % (receivedTimes, timesLimit)
                else:
                    itemRenderMc.receiveBtn.disabled = True
                    itemRenderMc.receiveBtn.label = gameStrings.HISTORY_CONSUMED_NOT_ACHIEVE
                itemRenderMc.receiveBtn.addEventListener(events.BUTTON_CLICK, self.handleClickReceiveBtn, False, 0, True)
                fixPanel.confirmBtn.disabled = True
                fixPanel.confirmBtn.label = gameStrings.HISTORY_CONSUMED_JIONED_ACTIVITY

        fixPanel.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleClickConfirmBtn, False, 0, True)

    def handleClickBanner(self, *args):
        url = SCD.data.get('historyConsumedWebUrl', 'https://ty.163.com/index.html')
        BigWorld.openUrl(url)

    def refreshChooseItemPanel(self):
        choosePanel = self.currentView
        if self.status == gametypes.HISTORY_CONSUMED_STATUS_CAN:
            choosePanel.chooseBtn.label = gameStrings.HISTORY_CONSUMED_JION_ACTIVITY
            choosePanel.chooseTxt.visible = False
            choosePanel.chooseBtn.disabled = False
        elif self.status == gametypes.HISTORY_CONSUMED_STATUS_JOINED:
            choosePanel.chooseBtn.label = gameStrings.HISTORY_CONSUMED_CONFIRM_CHOOSE
            choosePanel.chooseTxt.visible = True
            choosePanel.chooseTxt.text = gameStrings.HISTORY_CONSUMED_CHOOSE_TXT % (0, self.remainScore)
            choosePanel.chooseBtn.disabled = True
        choosePanel.moneyIcon.bonusType = SCD.data.get('historyConsumedIconType', 'bindCash')
        choosePanel.moneyTxt.text = self.remainScore
        choosePanel.itemList.itemRenderer = 'HistoryConsumed_chooseItem'
        choosePanel.itemList.lableFunction = self.itemLabelFunc
        choosePanel.itemList.column = CHOOSE_ITEM_NUM_PER_LINE
        self.setChooseItemList(choosePanel)
        choosePanel.itemList.validateNow()
        choosePanel.chooseBtn.addEventListener(events.BUTTON_CLICK, self.handleClickChooseBtn, False, 0, True)

    def clearItem(self):
        if self.widget and self.currentView == TAB_FIX_REWARD_INDEX:
            for itemRenderMc in self.itemRenderMcList:
                self.currentView.itemList.canvas.removeChild(itemRenderMc)

    def setChooseItemList(self, panel):
        data = HCCD.data.get(self.actId, {})
        itemList = []
        index = 0
        for itemId, cost, limitNum in data.get('volatileReward', ()):
            item = {}
            itemInfo = ID.data.get(itemId, {})
            icon = uiUtils.getItemIconFile64(itemId)
            iconLarge = uiConst.ITEM_ICON_IMAGE_RES_110 + str(itemInfo.get('icon', 'notFound')) + '.dds'
            name = itemInfo.get('name', '')
            mwrap = itemInfo.get('mwrap', 1)
            if item.get('many', 0) > 1:
                mwrap = mwrap / item.get('many', 1)
                name = name + gameStrings.TEXT_HISTORYCONSUMEDPROXY_256 + str(item.get('many', 0))
            item['name'] = name
            item['qualityColor'] = 'white'
            item['iconPath'] = icon
            item['iconPathLarge'] = iconLarge
            boughtNum = self.items.get(itemId, 0)
            if limitNum:
                item['leftNum'] = limitNum - boughtNum
                item['globalLimitTxt'] = gameStrings.HISTORY_CONSUMED_LIMIT % (limitNum - boughtNum, limitNum)
            item['mwrap'] = mwrap
            item['priceVal'] = cost
            item['canBuy'] = 1
            item['state'] = uiConst.ITEM_NORMAL
            item['hasPermission'] = True
            item['itemId'] = itemId
            index += 1
            itemList.append(item)

        panel.itemList.dataArray = itemList

    def itemLabelFunc(self, *args):
        itemInfo = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        self.setBoxData(itemMc, itemInfo)

    def setBoxData(self, mc, boxData):
        if mc.selBg:
            mc.selBg.visible = False
        mc.basicBox.itemName.gotoAndStop(boxData.qualityColor)
        mc.basicBox.itemName.nameText.text = boxData.name
        mc.basicBox.itemSlot.setItemSlotData(boxData)
        mc.basicBox.globalLimit.text = boxData.globalLimitTxt
        mc.basicBox.globalLimit.width = mc.basicBox.globalLimit.textWidth + 10
        mc.basicBox.globalLimit.wordWrap = False
        mc.basicBox.priceValue.textField.text = boxData.priceVal
        mc.basicBox.priceType.bonusType = SCD.data.get('historyConsumedIconType', 'bindCash')
        mc.itemId = boxData.itemId
        mc.data = boxData
        if self.status == gametypes.HISTORY_CONSUMED_STATUS_CAN:
            mc.gotoAndStop('over')
            mc.counter.visible = False
            mc.jionDesc.visible = True
        elif self.status == gametypes.HISTORY_CONSUMED_STATUS_JOINED:
            if mc.itemId in self.chooseItem.keys():
                mc.gotoAndStop('over')
                mc.counter.visible = True
                mc.overBg.visible = False
                mc.jionDesc.visible = False
                mc.counter.count = self.chooseItem.get(mc.itemId)
                mc.basicBox.priceValue.textField.text = boxData.priceVal * mc.counter.count
            else:
                mc.gotoAndStop('normal')
                mc.basicBox.priceValue.textField.text = boxData.priceVal
            mc.addEventListener(events.MOUSE_ROLL_OVER, self.rollOverListener)
            mc.addEventListener(events.MOUSE_ROLL_OUT, self.rollOutListener)

    def rollOverListener(self, *args):
        e = ASObject(args[3][0])
        mc = e.currentTarget
        boxData = mc.data
        mc.gotoAndStop('over')
        mc.jionDesc.visible = False
        mc.counter.visible = True
        mc.overBg.visible = False
        if mc.counter:
            mc.counter.minCount = 0
            if boxData.has_key('leftNum'):
                maxCount = min(boxData.leftNum, boxData.mwrap)
            else:
                maxCount = boxData.mwrap
            curItemMaxCount = mc.counter.count + (self.remainScore - self.currentCost) / boxData.priceVal
            maxCount = min(maxCount, curItemMaxCount)
            mc.counter.maxCount = maxCount
            mc.counter.enableMouseWheel = False
            if mc.counter.count:
                mc.basicBox.priceValue.textField.text = boxData.priceVal * mc.counter.count
            else:
                mc.basicBox.priceValue.textField.text = boxData.priceVal
            mc.itemCount = mc.counter.count
            mc.counter.addEventListener(events.EVENT_COUNT_CHANGE, self.counterChangeListener)

    def rollOutListener(self, *args):
        e = ASObject(args[3][0])
        mc = e.currentTarget
        boxData = mc.data
        if mc.itemCount >= 1:
            mc.basicBox.priceValue.textField.text = boxData.priceVal * mc.counter.count
            return
        mc.gotoAndStop('normal')
        mc.basicBox.priceValue.textField.text = boxData.priceVal

    def counterChangeListener(self, *args):
        e = ASObject(args[3][0])
        counter = e.currentTarget
        mc = counter.parent
        boxData = mc.data
        if mc.counter.count:
            mc.basicBox.priceValue.textField.text = boxData.priceVal * mc.counter.count
        else:
            mc.basicBox.priceValue.textField.text = boxData.priceVal
        mc.itemCount = mc.counter.count
        self.chooseItem[mc.data.itemId] = mc.itemCount
        volatileReward = HCCD.data.get(self.actId).get('volatileReward', ())
        self.currentCost = 0
        for itemId, cost, limitNum in volatileReward:
            if self.chooseItem.has_key(itemId):
                self.currentCost += cost * self.chooseItem[itemId]
            if boxData.has_key('leftNum'):
                maxCount = min(boxData.leftNum, boxData.mwrap)
            else:
                maxCount = boxData.mwrap
            curItemMaxCount = mc.counter.count + (self.remainScore - self.currentCost) / boxData.priceVal
            counter.maxCount = min(maxCount, curItemMaxCount)

        if self.currentTabIndex == TAB_CHOOSE_REWARD_INDEX:
            if self.currentCost > 0:
                self.currentView.chooseBtn.disabled = False
            else:
                self.currentView.chooseBtn.disabled = True
            self.currentView.chooseTxt.text = gameStrings.HISTORY_CONSUMED_CHOOSE_TXT % (self.currentCost, self.remainScore - self.currentCost)

    def handleClickConfirmBtn(self, *args):
        if self.isChoosedFromWeb:
            BigWorld.player().base.confirmHistoryConsumedEx()
        else:
            BigWorld.player().base.queryHistoryConsumedFreezePlayer(self.characterGbId)

    def onQueryHistoryConsumedFreezePlayer(self, gbId, roleName, hostId):
        fullName = utils.getServerName(hostId) + '-' + roleName
        msg = SCD.data.get('HISTORY_CONSUMED_JOIN_CONFIRM_MSG', gameStrings.HISTORY_CONSUMED_JOIN_CONFIRM_MSG) % fullName
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(BigWorld.player().base.confirmJoinHistoryConsumed, gbId, hostId))

    def onConfirmJoinHistoryConsumed(self):
        self.status = gametypes.HISTORY_CONSUMED_STATUS_JOINED
        BigWorld.player().base.queryHistoryConsumedReward()

    def handleClickReceiveBtn(self, *args):
        e = ASObject(args[3][0])
        rewardId = e.currentTarget.parent.index
        BigWorld.player().base.takeHistoryConsumedFixedReward(rewardId)

    def refreshRewardInfo(self, rewardId):
        self.rewardInfo[rewardId][0] += 1
        self.rewardInfo[rewardId][1] = True

    def handleClickChooseBtn(self, *args):
        if self.status == gametypes.HISTORY_CONSUMED_STATUS_CAN:
            if self.isChoosedFromWeb:
                BigWorld.player().base.confirmHistoryConsumedEx()
            else:
                BigWorld.player().base.queryHistoryConsumedFreezePlayer(self.characterGbId)
        elif self.status == gametypes.HISTORY_CONSUMED_STATUS_JOINED:
            itemIdList = []
            itemNumList = []
            chooseItems = []
            for itemId, itemNum in self.chooseItem.iteritems():
                if itemNum > 0:
                    itemIdList.append(itemId)
                    itemNumList.append(itemNum)
                    itemName = utils.getItemName(itemId)
                    itemStr = itemName + '*' + str(itemNum)
                    chooseItems.append(itemStr)

            chooseItemNames = gameStrings.TEXT_CHATPROXY_403.join(chooseItems)
            costPoint = self.currentCost
            msg = gameStrings.HISTORY_CONSUMED_CHOOSE_CONFIRM_DESC % costPoint
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(BigWorld.player().base.takeHistoryConsumedVolatileReward, itemIdList, itemNumList))

    def onTakeHistoryConsumedVolatileReward(self, remainScore, items):
        self.remainScore = remainScore
        self.currentCost = 0
        self.items = items
        self.chooseItem = {}
        self.refreshInfo()

    def addTimer(self):
        if not self.timer:
            self.timer = BigWorld.callback(1, self.timerFunc, -1)

    def timerFunc(self):
        if not self.widget:
            self.delTimer()
            return
        data = HCCD.data.get(self.actId, {})
        endTime = data.get('endDay', '')
        left = 0
        if utils.getTimeSecondFromStr(endTime) >= utils.getNow():
            left = utils.getTimeSecondFromStr(endTime) - utils.getNow()
        if self.currentView:
            self.currentView.leftTime.text = gameStrings.HISTORY_CONSUMED_LEFT_TIME + utils.formatDurationShortVersion(left)
        if left <= 0:
            self.hide()
            gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def delTimer(self):
        self.timer and BigWorld.cancelCallback(self.timer)
        self.timer = None

    def isOpen(self):
        if not self.returnPoint:
            return False
        if self.status == gametypes.HISTORY_CONSUMED_STATUS_JOINED_BY_MALL:
            return False
        self.actId = utils.getHistoryConsumedActId()
        data = HCCD.data.get(self.actId, {})
        includeHosts = data.get('includeHosts', ())
        if utils.getHostId() not in includeHosts:
            return False
        beginTime = data.get('startDay', '')
        endTime = data.get('endDay', '')
        curTime = utils.getNow()
        if utils.getTimeSecondFromStr(beginTime) <= curTime <= utils.getTimeSecondFromStr(endTime):
            return True
        return False

    def setAvailable(self, isAvailable):
        self.isRedPot = isAvailable
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def checkRedFlag(self):
        return self.isRedPot

    def pushHistoryConsumedMessage(self, actId, returnPoint, availableScore, isApplyed, isChoosedFromWeb):
        pushId = uiConst.MESSAGE_HISTORY_CONSUMED
        self.returnPoint = returnPoint
        self.isChoosedFromWeb = isChoosedFromWeb
        self.isApplyed = isApplyed
        if pushId not in gameglobal.rds.ui.pushMessage.msgs and not isApplyed:
            gameglobal.rds.ui.pushMessage.addPushMsg(pushId)
            gameglobal.rds.ui.pushMessage.setCallBack(pushId, {'click': self.onPushMsgClick})

    def removeHistoryConsumedPushMsg(self):
        pushId = uiConst.MESSAGE_HISTORY_CONSUMED
        if pushId in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(pushId)

    def onPushMsgClick(self):
        if not self.widget:
            if self.isChoosedFromWeb and not self.isApplyed:
                msg = gameStrings.HISTORY_CONSUMED_WEB_JOINED_MSG
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, BigWorld.player().base.confirmHistoryConsumedEx, yesBtnText=gameStrings.HISTORY_CONSUMED_INFORM_YES_2, noBtnText=gameStrings.HISTORY_CONSUMED_INFORM_NO)
            elif not self.isChoosedFromWeb:
                msg = gameStrings.HISTORY_CONSUMED_INFORM_MSG % self.returnPoint
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.show, yesBtnText=gameStrings.HISTORY_CONSUMED_INFORM_YES, noBtnText=gameStrings.HISTORY_CONSUMED_INFORM_NO)
        self.removeHistoryConsumedPushMsg()

    def banHistoryCosumeByMall(self):
        if self.widget:
            self.hide()
        self.status = gametypes.HISTORY_CONSUMED_STATUS_JOINED_BY_MALL
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        self.removeHistoryConsumedPushMsg()
