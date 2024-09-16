#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/catchUpDetailProxy.o
from gamestrings import gameStrings
import BigWorld
import math
import uiConst
import events
from asObject import ASObject
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import TipManager
from cdata import game_msg_def_data as GMDD
from data import fame_data as FD
REWARD_ITEM_MAX_CNT = 6
REWARD_ICON_MAX_CNT = 4

class CatchUpDetailProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CatchUpDetailProxy, self).__init__(uiAdapter)
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CATCH_UP_DETAIL, self.hide)

    def reset(self):
        self.widget = None
        self.itemData = None
        self.catchUpNum = 0
        self.rewardId = 0
        self.consumeCoins = 0
        self.totalCost = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CATCH_UP_DETAIL:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CATCH_UP_DETAIL)

    def show(self, itemData):
        self.itemData = itemData
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CATCH_UP_DETAIL)
        else:
            self.initUI()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.title.text = gameStrings.CATCH_UP_DETAIL_TITLE
        self.widget.costDesc.text = gameStrings.CATCH_UP_DETAIL_TITLE
        self.widget.timesDesc.text = gameStrings.CATCH_UP_DETAIL_TIEMS
        self.widget.totalDesc.text = gameStrings.CATCH_UP_DETAIL_TOTAL
        self.widget.timesCounter.minCount = 1
        self.catchUpNum = self.widget.timesCounter.count
        self.widget.timesCounter.addEventListener(events.EVENT_COUNT_CHANGE, self.handleBuyCounterChange, False, 0, True)
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        self.widget.rechargeBtn.addEventListener(events.BUTTON_CLICK, self.handleRechargeBtnClick, False, 0, True)
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        if not self.itemData:
            return
        rewardMc = self.widget.rewardMc
        itemData = self.itemData
        self.rewardId = itemData.rewardId
        rewardMc.txtTitile.text = itemData.title
        itemList = itemData.itemList
        for i in xrange(REWARD_ITEM_MAX_CNT):
            itemSlot = rewardMc.getChildByName('item%d' % i)
            if i >= len(itemList):
                itemSlot.visible = False
                continue
            itemSlot.visible = True
            itemSlot.dragable = False
            itemSlot.setItemSlotData(itemList[i])

        for i in xrange(REWARD_ICON_MAX_CNT):
            bonusIcon = rewardMc.getChildByName('rewardIcon%d' % i)
            rewardTxt = rewardMc.getChildByName('rewardTxt%d' % i)
            bonusIcon.visible = False
            rewardTxt.visible = False

        iconList = itemData.iconList
        index = 0
        for j in xrange(len(iconList)):
            if iconList[j][1] == 0:
                continue
            bonusIcon = rewardMc.getChildByName('rewardIcon%d' % index)
            rewardTxt = rewardMc.getChildByName('rewardTxt%d' % index)
            bonusIcon.visible = True
            rewardTxt.visible = True
            index = index + 1
            bonusIcon.bonusType = iconList[j][0]
            rewardTxt.text = str(int(iconList[j][1]))
            if iconList[j][0] == 'shenwang':
                TipManager.addTip(bonusIcon, FD.data.get(iconList[j][2], {}).get('name', ''))

        self.consumeCoins = itemData.consumeCoins
        self.refreshCost()
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)

    def refreshCost(self):
        if not self.widget:
            return
        p = BigWorld.player()
        rewardCatchUpInfo = p.rewardCatchUpInfo.values()
        rewardInfo = ()
        if rewardCatchUpInfo:
            rewardInfo = rewardCatchUpInfo[0].get(self.rewardId, ())
        if not rewardInfo:
            return
        freeCnt, payCnt, discount = rewardInfo[:3]
        self.widget.rewardMc.txtTitile.text = self.itemData.title % (freeCnt + payCnt)
        discount = min(discount, 1)
        if discount and discount < 1:
            self.widget.discount.visible = True
            self.widget.originCost.visible = True
            self.widget.delFlag.visible = True
            self.widget.costNum.text = math.ceil(int(self.consumeCoins) * discount)
            discountShow = discount * 10
            discountShow = int(discountShow) if discountShow == int(discountShow) else discountShow
            self.widget.discount.htmlText = gameStrings.TEXT_CATCHUPDETAILPROXY_139 % str(discountShow)
            self.widget.originCost.text = gameStrings.TEXT_CATCHUPDETAILPROXY_140 % int(self.consumeCoins)
            self.widget.delFlag.width = len(str(self.consumeCoins)) * 7.5
        else:
            self.widget.discount.visible = False
            self.widget.originCost.visible = False
            self.widget.delFlag.visible = False
            self.widget.costNum.text = int(self.consumeCoins)
        self.widget.timesCounter.maxCount = freeCnt + payCnt
        self.widget.timesDetail.htmlText = gameStrings.TEXT_CATCHUPDETAILPROXY_149 % freeCnt
        if self.catchUpNum <= freeCnt:
            totalCost = 0
        else:
            if freeCnt > 0:
                catchUpPayNum = self.catchUpNum - freeCnt
            else:
                catchUpPayNum = self.catchUpNum
            if discount and discount < 1:
                totalCost = int(math.ceil(int(self.consumeCoins) * discount)) * catchUpPayNum
            else:
                totalCost = int(self.consumeCoins) * catchUpPayNum
        self.totalCost = totalCost
        if totalCost == 0:
            self.widget.totalType.visible = False
            self.widget.totalNum.text = gameStrings.TEXT_CATCHUPDETAILPROXY_165
        else:
            self.widget.totalType.visible = True
            self.widget.totalNum.text = str(totalCost)

    def handleConfirmBtnClick(self, *args):
        p = BigWorld.player()
        totalTianbi = p.unbindCoin + p.bindCoin + p.freeCoin
        if self.totalCost > totalTianbi:
            p.showGameMsg(GMDD.data.NOT_ENOUGH_COIN, ())
        else:
            p.cell.getCatchUpActivityReward(int(self.rewardId), int(self.catchUpNum), True, True)

    def handleRechargeBtnClick(self, *args):
        self.uiAdapter.tianyuMall.onOpenChargeWindow()

    def handleBuyCounterChange(self, *args):
        e = ASObject(args[3][0])
        self.catchUpNum = int(e.currentTarget.count)
        self.refreshCost()
