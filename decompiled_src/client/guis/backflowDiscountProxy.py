#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/backflowDiscountProxy.o
import BigWorld
import utils
import events
import uiConst
import clientUtils
import gameglobal
import const
from uiProxy import UIProxy
from asObject import ASObject
from asObject import ASUtils
from guis import uiUtils
from gameStrings import gameStrings
from gameclass import ClientMallVal
from asObject import RedPotManager
from guis.asObject import TipManager
from data import mall_item_data as MID
from cdata import flowback_group_recharge_data as FGRD
ITEM_WIDTH = 145
ITEM_HEIGHT = 200
FLOW_BACK_GROUP_RECHARGE_ID = 1
REWARD_BONUSID_NUM = 5
MONEY_TYPE_MAP = {uiConst.MONEY_TYPE_TIANBI: 'tianBi',
 uiConst.MONEY_TYPE_TIANQUAN: 'tianQuan',
 uiConst.MONEY_TYPE_JIFEN: 'jiFenBi'}

class BackflowDiscountProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BackflowDiscountProxy, self).__init__(uiAdapter)
        self.widget = None
        self.callback = None
        self.fgrdData = None
        self.mallItemList = []

    def reset(self):
        self.callback = None
        self.fgrdData = None
        self.mallItemList = []

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        self.widget.discountPanel.getRewardBtn.addEventListener(events.MOUSE_CLICK, self.handleGetRewardBtnClick, False, 0, True)
        self.widget.discountPanel.gotoBtn.addEventListener(events.MOUSE_CLICK, self.handleGotoBtnClick, False, 0, True)
        self.widget.discountPanel.scrollWndList.column = 3
        self.widget.discountPanel.scrollWndList.itemWidth = ITEM_WIDTH
        self.widget.discountPanel.scrollWndList.itemHeight = ITEM_HEIGHT
        self.widget.discountPanel.scrollWndList.itemRenderer = 'BackflowDiscount_Item'
        self.widget.discountPanel.scrollWndList.dataArray = []
        self.widget.discountPanel.scrollWndList.lableFunction = self.itemFunction

    def refreshInfo(self):
        if not self.widget:
            return
        self.fgrdData = FGRD.data.get(FLOW_BACK_GROUP_RECHARGE_ID, {})
        self.updateLeftTime()
        self.updateRechargeRewards()
        self.updateRechargeBuy()

    def handleGetRewardBtnClick(self, *args):
        e = ASObject(args[3][0])
        p = BigWorld.player()
        p.cell.receiveFlowbackGroupRechargeReward()

    def handleGotoBtnClick(self, *args):
        p = BigWorld.player()
        p.openRechargeFunc()

    def handleBuyBtnClick(self, *args):
        e = ASObject(args[3][0])
        mallId = e.currentTarget.parent.mallItemId
        gameglobal.rds.ui.tianyuMall.mallBuyConfirm(mallId, 1, 'huiliu.0')

    def handleRollOverItem(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        itemMc.gotoAndStop('over')
        if itemMc.leftNum:
            itemMc.buyBtn.label = gameStrings.BACK_FLOW_DISCOUNT_BUY_BTN_LABEL
            itemMc.buyBtn.enabled = True
        else:
            itemMc.buyBtn.label = gameStrings.BACK_FLOW_DISCOUNT_BUY_BTN_ENABLED_LABEL
            itemMc.buyBtn.enabled = False
        ASUtils.setHitTestDisable(itemMc.overBg, True)
        itemMc.buyBtn.addEventListener(events.MOUSE_CLICK, self.handleBuyBtnClick, False, 0, True)

    def handleRollOutItem(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        itemMc.gotoAndStop('normal')

    def updateLeftTime(self):
        if not self.widget:
            self.stopCallback()
            return
        p = BigWorld.player()
        startTime = p.flowbackGroupBonus.startTime
        curTime = utils.getNow()
        day = self.fgrdData.get('duration', 0)
        endTime = startTime + day * const.TIME_INTERVAL_DAY
        leftTime = max(endTime - curTime, 0)
        if leftTime < 0:
            self.stopCallback()
            return
        day = utils.formatDurationLeftDay(leftTime)
        hour = utils.formatDurationLeftHour(leftTime)
        minute = utils.formatDurationLeftMin(leftTime)
        srtTime = gameStrings.BACK_FLOW_LEFT_TIME % (day, hour, minute)
        self.widget.discountPanel.leftTimeT.htmlText = gameStrings.BACK_FLOW_LEFT_TIME_TITLE % uiUtils.toHtml(srtTime, '#d34024')
        self.callback = BigWorld.callback(1, self.updateLeftTime)

    def stopCallback(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
            self.callback = None

    def updateRechargeRewards(self):
        if not self.widget:
            return
        discountPanel = self.widget.discountPanel
        p = BigWorld.player()
        rechargeRewards = p.flowbackGroupBonus.rechargeRewards
        rechargeAmount = p.flowbackGroupBonus.rechargeAmount
        bonusIds = self.fgrdData.get('bonusIds', ())
        points = self.fgrdData.get('rechargeAmounts', ())
        tipMsg = gameStrings.BACK_FLOW_DISCOUNT_RECHARGE_AMOUNT % rechargeAmount
        TipManager.addTip(discountPanel.rechargeIcon, tipMsg)
        discountPanel.rechargeValueT.text = rechargeAmount
        for i in range(REWARD_BONUSID_NUM):
            rewardItem = discountPanel.getChildByName('rewardItem%d' % i)
            pointPic = discountPanel.pointsMc.getChildByName('pointPic%d' % i)
            pointIcon = discountPanel.pointsMc.getChildByName('pointIcon%d' % i)
            pointValT = discountPanel.pointsMc.getChildByName('pointValT%d' % i)
            arrow = discountPanel.pointsMc.getChildByName('arrow%d' % i)
            pointIcon.bonusType = 'tianBi'
            bonusId = bonusIds[i] if i < len(bonusIds) else 0
            itemBonus = clientUtils.genItemBonus(bonusId)
            itemId, num = itemBonus[0] if itemBonus else (0, 0)
            itemInfo = uiUtils.getGfxItemById(itemId, num)
            rewardItem.slot.fitSize = True
            rewardItem.slot.dragable = False
            rewardItem.slot.setItemSlotData(itemInfo)
            rewardItem.getedPic.visible = False
            ASUtils.setHitTestDisable(rewardItem.getedPic, True)
            rewardItem.sfx.visible = False
            ASUtils.setHitTestDisable(rewardItem.sfx, True)
            rewardItem.slot.setSlotState(uiConst.ITEM_NORMAL)
            if bonusId in rechargeRewards:
                rewardItem.getedPic.visible = True
                rewardItem.slot.setSlotState(uiConst.ITEM_GRAY)
            else:
                iPoint = points[i] if i < len(points) else 0
                rewardItem.sfx.visible = True if rechargeAmount >= iPoint else False
            pointValT.text = points[i] if i < len(points) else 0
            if rechargeAmount < points[i]:
                pointPic.gotoAndStop('disable')
            else:
                pointPic.gotoAndStop('up')
            if rechargeAmount >= points[i]:
                arrow.gotoAndStop('dislight')
            elif i > 0 and rechargeAmount > points[i - 1] or i == 0 and rechargeAmount > 0:
                arrow.gotoAndStop('half')
            else:
                arrow.gotoAndStop('light')

        getedRewards = len(rechargeRewards)
        nextPoint = 0
        if getedRewards + 1 <= len(points):
            nextPoint = points[getedRewards]
        discountPanel.getRewardBtn.enabled = True if rechargeAmount and nextPoint and rechargeAmount >= nextPoint else False
        discountPanel.gotoBtn.visible = True if len(rechargeRewards) < REWARD_BONUSID_NUM else False

    def updateRechargeBuy(self):
        if not self.widget:
            return
        p = BigWorld.player()
        mallItemIds = self.fgrdData.get('mallItemIds', ())
        self.mallItemList = []
        for mallItemId in mallItemIds:
            midData = MID.data.get(mallItemId, {})
            itemName = '%sx%s' % (midData.get('itemName', ''), str(midData.get('many', 0)))
            itemId = midData.get('itemId', 0)
            priceType = midData.get('priceType', 1)
            priceVal = midData.get('priceVal', 0)
            originalPrice = int(midData.get('originalPrice', 0))
            totalLimit = int(midData.get('totalLimit', 1))
            leftNum = max(0, totalLimit - p.mallInfo.get(mallItemId, ClientMallVal()).nTotal)
            discountRate = priceVal * 1.0 / originalPrice if originalPrice else 0
            if discountRate < 1.0:
                intPart = int(discountRate * 10.0)
                floatPart = int((discountRate * 10.0 - intPart) * 10.0)
                if floatPart:
                    subText = '.%d%s' % (floatPart, gameStrings.ACTIVITY_SHOP_PROXY_DISCOUNT)
                else:
                    subText = gameStrings.ACTIVITY_SHOP_PROXY_DISCOUNT
            else:
                intPart = 0
                subText = 0
            itemInfo = {}
            itemInfo['mallItemId'] = mallItemId
            itemInfo['itemName'] = itemName
            itemInfo['itemId'] = itemId
            itemInfo['leftNum'] = leftNum
            itemInfo['totalLimit'] = totalLimit
            itemInfo['bonusType'] = MONEY_TYPE_MAP[priceType]
            itemInfo['priceVal'] = priceVal
            itemInfo['originalPrice'] = originalPrice
            itemInfo['intPart'] = str(intPart)
            itemInfo['subText'] = subText
            self.mallItemList.append(itemInfo)

        self.widget.discountPanel.scrollWndList.dataArray = self.mallItemList
        self.widget.discountPanel.scrollWndList.validateNow()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.mallItemId = itemData.mallItemId
        itemMc.leftNum = itemData.leftNum
        if itemData.leftNum:
            color = '#FFFFE5'
        else:
            color = '#d34024'
        itemMc.itemNum.htmlText = '%s/%d' % (uiUtils.toHtml(itemData.leftNum, color), itemData.totalLimit)
        itemMc.itemSlot.fitSize = True
        itemMc.itemSlot.dragable = False
        itemMc.itemSlot.setItemSlotData(uiUtils.getGfxItemById(itemData.itemId))
        if not itemData.intPart and not itemData.subText:
            itemMc.discountLabel.visible = False
        else:
            itemMc.discountLabel.visible = True
            itemMc.discountLabel.mainText.text = itemData.intPart
            itemMc.discountLabel.subText.text = itemData.subText
        itemMc.itemName.text = itemData.itemName
        itemMc.costMc.costCount.text = itemData.priceVal
        itemMc.costMc.costIcon.bonusType = itemData.bonusType
        if itemData.originalPrice:
            itemMc.priceOrig.visible = True
            itemMc.priceOrig.textField.text = gameStrings.BACK_FLOW_DISCOUNT_BUY_ITEM_DESC % itemData.originalPrice
            itemMc.priceOrig.textField.width = itemMc.priceOrig.textField.textWidth + 4
            itemMc.priceOrig.delFlag.width = itemMc.priceOrig.textField.width
            itemMc.priceOrig.delFlag.x = 0
        else:
            itemMc.priceOrig.visible = False
        itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleRollOverItem, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleRollOutItem, False, 0, True)

    def checkRedPoint(self):
        p = BigWorld.player()
        rechargeRewards = p.flowbackGroupBonus.rechargeRewards
        rechargeAmount = p.flowbackGroupBonus.rechargeAmount
        points = FGRD.data.get(FLOW_BACK_GROUP_RECHARGE_ID, {}).get('rechargeAmounts', ())
        getedRewards = len(rechargeRewards)
        nextPoint = 0
        if getedRewards + 1 <= len(points):
            nextPoint = points[getedRewards]
        isRedPot = True if rechargeAmount and nextPoint and rechargeAmount >= nextPoint else False
        return isRedPot and not self.checkTimeEnd()

    def updateRedPot(self):
        RedPotManager.updateRedPot(uiConst.BACK_FLOW_DISCOUNT_RED_POT)

    def checkTimeEnd(self):
        p = BigWorld.player()
        startTime = p.flowbackGroupBonus.startTime
        curTime = utils.getNow()
        day = FGRD.data.get(FLOW_BACK_GROUP_RECHARGE_ID, {}).get('duration', 0)
        endTime = startTime + day * const.TIME_INTERVAL_DAY
        leftTime = max(endTime - curTime, 0)
        if leftTime <= 0:
            return True
        return False
