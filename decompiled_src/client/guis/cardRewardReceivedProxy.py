#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cardRewardReceivedProxy.o
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

class CardRewardReceivedProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CardRewardReceivedProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CARD_REWARD_RECEIVED, self.hide)

    def reset(self):
        self.curPropType = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CARD_REWARD_RECEIVED:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.reset()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CARD_REWARD_RECEIVED)

    def show(self, pType):
        self.curPropType = pType
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CARD_REWARD_RECEIVED)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.titleMc.titleName.text = gameStrings.CARD_REWARD_ALREADY_GET_TITLE % gameStrings.CARD_SYSTEM_PROP_TYPE_DESC.get(self.curPropType, '')
        self.widget.rewardList.column = 4
        self.widget.rewardList.itemHeight = 127
        self.widget.rewardList.itemWidth = 184
        self.widget.rewardList.itemRenderer = 'CardRewardReceived_RewardItem'
        self.widget.rewardList.labelFunction = self.rewardListFunction
        self.widget.rewardList.dataArray = []
        self.refreshRewardList()

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

    def refreshRewardList(self):
        if not self.hasBaseData():
            return False
        dataList = self.getRewardListData()
        self.widget.rewardList.dataArray = dataList
        self.widget.rewardList.validateNow()

    def getRewardListData(self):
        p = BigWorld.player()
        curType = self.curPropType
        self.rewardData = []
        for (propType, needRank), rData in CRD.data.iteritems():
            if curType != propType:
                continue
            cardAwards = p.cardBag.get('cardAwards', {})
            if cardAwards.get(propType, 0) >= needRank:
                info = {'propType': propType,
                 'needRank': needRank,
                 'bonusId': rData.get('reward', 0)}
                self.rewardData.append(info)

        return self.rewardData

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshRewardList()

    def hasBaseData(self):
        if not self.widget:
            return False
        return True
