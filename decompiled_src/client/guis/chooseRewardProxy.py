#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/chooseRewardProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import uiConst
import utils
import events
import clientUtils
from item import Item
from uiProxy import UIProxy
from guis.asObject import ASObject
from data import coin_charge_reward_data as CCRD
from data import item_data as ID
import gamelog
from data import consumable_item_data as CID
X_OFFSET = 80
Y_OFFSET = 100
X_BEGIN = 0
Y_BEGIN = 0
REWARD_ITEM_CONTENT = 'ChooseReward_ItemContent'
LINE_MAX_NUM = 11
DOUBLE_LINE_MAX_NUM = 8

class ChooseRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChooseRewardProxy, self).__init__(uiAdapter)
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHOOSE_REWARD, self.hidePanel)
        self.bonusItems = []
        self.bonusNum = 0
        self.rewards = ()
        self.choosedNum = 0
        self.choosedItems = []
        self.rewardItems = []

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self._getData()
        self.refreshPanel()

    def refreshPanel(self):
        if self.isChooseReward:
            self.widget.titleArea.title.text = gameStrings.TEXT_ACTIVITYSALELOOPCHARGEPROXY_151
        else:
            self.widget.titleArea.title.text = gameStrings.TEXT_ACTIVITYSALELOOPCHARGEPROXY_154
        self.widget.rule.text = gameStrings.TEXT_CHOOSEREWARDPROXY_52 % (self.bonusNum, self.rewards[1])
        if self.bonusNum > LINE_MAX_NUM:
            self.widget.gotoAndStop('up4')
            if self.bonusNum > DOUBLE_LINE_MAX_NUM:
                self.widget.rewardContent.visible = False
                self.widget.rewardList.visible = True
                rewardContentMc = self.widget.rewardList.canvas
            else:
                self.widget.rewardContent.visible = True
                self.widget.rewardList.visible = False
                rewardContentMc = self.widget.rewardContent
        else:
            self.widget.gotoAndStop('below4')
            rewardContentMc = self.widget.rewardContent
        self.widget.chooseNum.text = '%d/%d' % (self.choosedNum, self.rewards[1])
        self.widget.removeAllInst(rewardContentMc)
        for i in range(0, self.bonusNum):
            itemContent = self.widget.getInstByClsName(REWARD_ITEM_CONTENT)
            itemContent.x = X_BEGIN + i % LINE_MAX_NUM * X_OFFSET
            if i >= LINE_MAX_NUM:
                itemContent.y = itemContent.y = Y_BEGIN + i / LINE_MAX_NUM * Y_OFFSET
            bonusItem = self.bonusItems[i]
            itemContent.slot.setItemSlotData(uiUtils.getGfxItemById(bonusItem[0], bonusItem[1]))
            itemContent.checkBox.selected = False
            itemContent.checkBox.data = i
            itemContent.checkBox.addEventListener(events.BUTTON_CLICK, self.handleSelect)
            itemContent.slot.dragable = False
            itemContent.slot.itemId = bonusItem[0]
            itemContent.slot.addEventListener(events.MOUSE_CLICK, self.handleShowFit)
            rewardContentMc.addChild(itemContent)
            self.rewardItems.append(itemContent)

        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleConfirm)
        self.widget.confirmBtn.enabled = False

    def refreshChooseNum(self):
        self.widget.chooseNum.text = '%d/%d' % (self.choosedNum, self.rewards[1])

    def handleConfirm(self, *args):
        msg = gameStrings.TEXT_CHOOSEREWARDPROXY_93
        for i in xrange(len(self.choosedItems)):
            itemIndex = self.choosedItems[i]
            itemId = self.bonusItems[itemIndex][0]
            name = ID.data.get(itemId, {}).get('name', '')
            if i == len(self.choosedItems) - 1:
                msg = msg + name + gameStrings.TEXT_CHOOSEREWARDPROXY_100
            else:
                msg = msg + name + ','

        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.onClickChooseReward)

    def onClickChooseReward(self):
        p = BigWorld.player()
        crId, crData = self.chargeRewardInfo()
        costValue = 0
        chargeValue = 0
        for info in p.chargeRewardInfo:
            if info[0] == crId:
                chargeValue = info[1]
                costValue = info[2]

        rewardInfo = crData.get('chargeCoins', [])[self.index]
        if chargeValue < rewardInfo[0]:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_CHOOSEREWARDPROXY_117)
            return
        if costValue < rewardInfo[1]:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_CHOOSEREWARDPROXY_120)
            return
        p.base.getChargeReward(self.crId, self.index, self.choosedItems)
        self.hidePanel()

    def refreshCheckBoxEnabled(self):
        if self.choosedNum >= self.rewards[1]:
            for i in range(0, len(self.rewardItems)):
                if i not in self.choosedItems:
                    self.rewardItems[i].checkBox.enabled = False

        else:
            for i in range(0, len(self.rewardItems)):
                self.rewardItems[i].checkBox.enabled = True

    def handleSelect(self, *args):
        e = ASObject(args[3][0])
        itemCheckBox = e.currentTarget
        itemCheckBox.focused = False
        if not itemCheckBox.selected:
            self.choosedNum -= 1
            self.choosedItems.remove(int(itemCheckBox.data))
        else:
            if self.choosedNum >= self.rewards[1]:
                return
            self.choosedNum += 1
            self.choosedItems.append(int(itemCheckBox.data))
        self.refreshChooseNum()
        self.refreshCheckBoxEnabled()
        if self.choosedNum == self.rewards[1]:
            self.widget.confirmBtn.enabled = True
        else:
            self.widget.confirmBtn.enabled = False

    def _getData(self):
        crId, crData = self.chargeRewardInfo()
        self.crId = crId
        rewardsForChoose = crData.get('rewardsForChoose', [])
        if len(rewardsForChoose) > 0:
            self.rewards = rewardsForChoose[self.index]
        else:
            self.rewards = ()
            self.bonusItems = []
            self.bonusNum = 0
            return
        bonusId = self.rewards[0]
        self.bonusItems = clientUtils.genItemBonus(bonusId, True)
        self.bonusNum = len(self.bonusItems)

    def show(self, index, isChooseReward):
        self.index = index
        self.isChooseReward = isChooseReward
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CHOOSE_REWARD, True)

    def hidePanel(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHOOSE_REWARD)
        self.widget = None
        self.clearData()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHOOSE_REWARD)
        self.widget = None
        self.clearData()

    def clearData(self):
        self.bonusItems = []
        self.bonusNum = 0
        self.rewards = ()
        self.choosedNum = 0
        self.choosedItems = []
        self.rewardItems = []

    def chargeRewardInfo(self):
        now = utils.getNow()
        for key, val in CCRD.data.iteritems():
            beginTime = utils.getTimeSecondFromStr(val.get('beginTime', ''))
            endTime = utils.getTimeSecondFromStr(val.get('endTime', ''))
            whiteList = val.get('whiteList', None)
            if whiteList and utils.getHostId() not in whiteList:
                continue
            if now >= beginTime and now <= endTime:
                return (key, val)

        return (0, {})

    def handleShowFit(self, *args):
        e = ASObject(args[3][0])
        itemId = int(e.currentTarget.itemId)
        if itemId and e.buttonIdx == uiConst.LEFT_BUTTON:
            cidData = CID.data.get(itemId, {})
            sType = cidData.get('sType', 0)
            if sType == Item.SUBTYPE_2_GET_SELECT_ITEM:
                gameglobal.rds.ui.itemChoose.show(itemId, showType=0)
            else:
                self.uiAdapter.fittingRoom.addItem(Item(itemId))
