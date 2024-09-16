#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cardRankRewardProxy.o
import BigWorld
import events
import gameglobal
import uiConst
import uiUtils
import const
import clientUtils
from asObject import ASUtils
from asObject import ASObject
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import card_reward_data as CRD
from data import base_card_data as BCD
ICON_WIDTH = 70
TAB_NUM = 2

class CardRankRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CardRankRewardProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CARD_RANK_REWARD, self.hide)

    def reset(self):
        self.rewardData = []

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CARD_RANK_REWARD:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.reset()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CARD_RANK_REWARD)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CARD_RANK_REWARD)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.tabBtn0.groupName = 'slotTab'
        self.widget.tabBtn0.data = 1
        self.widget.tabBtn1.groupName = 'slotTab'
        self.widget.tabBtn1.data = 2
        self.widget.tabBtn0.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)
        self.widget.tabBtn1.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)
        self.widget.tabBtn0.selected = True
        self.widget.rewardList.column = 4
        self.widget.rewardList.itemHeight = 127
        self.widget.rewardList.itemWidth = 184
        self.widget.rewardList.itemRenderer = 'CardRankReward_RewardItem'
        self.widget.rewardList.labelFunction = self.rewardListFunction
        self.widget.rewardList.dataArray = []
        self.refreshInfo()

    def refreshRewardList(self):
        if not self.hasBaseData():
            return False
        dataList = self.getRewardListData()
        self.widget.rewardList.dataArray = dataList
        self.widget.rewardList.validateNow()

    def getCurRankValue(self, curType = 0):
        p = BigWorld.player()
        maxRankValue = 0
        curRankValue = 0
        if not curType:
            curType = self.getCurSelType()
        for cardId, bData in BCD.data.iteritems():
            if curType != bData.get('propType', 0):
                continue
            if not bData.get('canRenewal', None) and not bData.get('canRenewal', None):
                maxRankValue += const.CARD_MAX_RANK
            cardObj = p.getCard(cardId)
            if not cardObj.notValid:
                curRankValue += cardObj.advanceLv

        maxRankValue += const.CARD_MAX_RANK * const.CARD_MAX_RENEWAL_EFFECT_NUM
        return (curRankValue, maxRankValue)

    def getHasRewardInfo(self):
        p = BigWorld.player()
        rewardInfo = {}
        for (propType, needRank), rData in CRD.data.iteritems():
            curRankValue, maxRankValue = self.getCurRankValue(propType)
            cardAwards = p.cardBag.get('cardAwards', {})
            if cardAwards.get(propType, 0) < needRank and needRank <= curRankValue and propType not in rewardInfo:
                rewardInfo[propType] = True

        return rewardInfo

    def getRewardListData(self):
        p = BigWorld.player()
        curType = self.getCurSelType()
        self.rewardData = []
        curRankValue, maxRankValue = self.getCurRankValue()
        for (propType, needRank), rData in CRD.data.iteritems():
            if curType != propType:
                continue
            cardAwards = p.cardBag.get('cardAwards', {})
            if cardAwards.get(propType, 0) < needRank:
                info = {'propType': propType,
                 'needRank': needRank,
                 'canGetReward': curRankValue >= needRank,
                 'bonusId': rData.get('reward', 0)}
                self.rewardData.append(info)

        return self.rewardData

    def getCurSelType(self):
        if not self.hasBaseData():
            return False
        return int(self.widget.tabBtn0.group.selectedButton.data)

    def rewardListFunction(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and info:
            bonusId = info.bonusId
            bonus = clientUtils.genItemBonus(bonusId)
            itemMc.titleName.text = gameStrings.CARD_RANK_REWARD_TITLE % (info.needRank,)
            self.widget.removeAllInst(itemMc.canvas)
            for i, (itemId, itemNum) in enumerate(bonus):
                slotItem = self.widget.getInstByClsName('M12_InventorySlot')
                halfNum = len(bonus) / 2.0
                slotItem.x = ICON_WIDTH * i - ICON_WIDTH * halfNum + 10
                itemInfo = uiUtils.getGfxItemById(itemId, itemNum)
                slotItem.setItemSlotData(itemInfo)
                slotItem.dragable = False
                itemMc.canvas.addChild(slotItem)

            itemMc.canGet.visible = info.canGetReward

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshRewardList()
        curRankValue, maxRankValue = self.getCurRankValue()
        self.widget.rankProgress.maxValue = maxRankValue
        self.widget.rankProgress.currentValue = curRankValue
        tmpTabBtnList = (self.widget.tabBtn0, self.widget.tabBtn1)
        rewardInfo = self.getHasRewardInfo()
        curType = self.getCurSelType()
        for i in xrange(TAB_NUM):
            tabBtn = getattr(self.widget, 'tabBtn' + str(i))
            tabRedPoint = getattr(self.widget, 'tabRedPoint' + str(i))
            if tabBtn and tabRedPoint:
                tabRedPoint.visible = rewardInfo.get(tabBtn.data, False)

        hasReward = rewardInfo.get(curType, False)
        self.widget.getRedPoint.visible = hasReward

    def hasBaseData(self):
        if not self.widget:
            return False
        return True

    def handleTabBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        t.selected = True
        self.refreshInfo()

    def _onGetBtnClick(self, e):
        p = BigWorld.player()
        p.base.getCardAward(self.getCurSelType())

    def _onReviewBtnClick(self, e):
        self.uiAdapter.cardRewardReceived.show(self.getCurSelType())
