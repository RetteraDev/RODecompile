#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/tianyuMallBuyV2Proxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import events
from gamestrings import gameStrings
import clientUtils
from uiProxy import UIProxy
from guis import uiUtils
from guis import ui
from guis.asObject import ASUtils
from guis.asObject import ASObject
from data import mall_item_data as MID
from data import item_data as ID
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD

class TianyuMallBuyV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TianyuMallBuyV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.resetData()
        uiAdapter.registerEscFunc(uiConst.WIDGET_TIANYU_MALL_BUY_V2, self.hide)

    def resetData(self):
        self.displayMode = uiConst.TIANYU_MALL_BUY_MODE_BUY
        self.activityId = 0
        self.mallId = 0
        self.buyCnt = 1
        self.priceVal = 0
        self.friendList = []
        self.sendFriendIdx = -1
        self.sendMsg = ''

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_TIANYU_MALL_BUY_V2:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_TIANYU_MALL_BUY_V2)

    def show(self, activityId, mallId, buyCnt = 1, displayMode = uiConst.TIANYU_MALL_BUY_MODE_BUY):
        self.resetData()
        self.mallId = mallId
        self.activityId = activityId
        self.displayMode = displayMode
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_TIANYU_MALL_BUY_V2)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.gotoAndStop('buy' if self.displayMode == uiConst.TIANYU_MALL_BUY_MODE_BUY else 'send')
        self.widget.defaultCloseBtn = self.widget.closeBtn
        itemId = MID.data.get(self.mallId, {}).get('itemId', 0)
        self.widget.itemSlot.setItemSlotData(uiUtils.getGfxItemById(itemId))
        self.widget.txtItemName.htmlText = uiUtils.getItemColorName(itemId)
        self.widget.bonusIcon.bonusType = 'tianBi'
        self.widget.bonusIcon2.bonusType = 'tianBi'
        self.widget.numStepper.count = self.buyCnt
        self.widget.numStepper.maxCount = ID.data.get(itemId, {}).get('mwrap', 1)
        self.widget.numStepper.addEventListener(events.EVENT_COUNT_CHANGE, self.handleConterChange, False, 0, True)
        self.widget.txtTitle.text = gameStrings.TIANYU_MALL_BUY_V2_BUY if self.displayMode == uiConst.TIANYU_MALL_BUY_MODE_BUY else gameStrings.TIANYU_MALL_BUY_V2_SEND
        self.priceVal = MID.data.get(self.mallId, {}).get('priceVal', 0)
        self.widget.txtPrice.text = str(self.priceVal)
        if self.displayMode == uiConst.TIANYU_MALL_BUY_MODE_SEND:
            self.widget.dropDown.labelFunction = self.dropDownlabelFunction
            self.widget.dropDown.defaultText = gameStrings.TIANYU_MALL_BUY_V2_DORP_DOWN_DEFAULT_TXT
            self.widget.dropDown.addEventListener(events.INDEX_CHANGE, self.handleIndexChange, False, 0, True)
            self.widget.dropDown.dropdown = 'M12_DefaultScrollingList'
            self.widget.dropDown.itemRenderer = 'M12_DefaultListItemRenderer'
            ASUtils.setDropdownMenuData(self.widget.dropDown, self.getFriendList())
            self.widget.txtMsg.maxChars = 160
            self.widget.txtMsg.defaultText = gameStrings.TIANYU_MALL_BUY_V2_TEXT_INPUT_DEFAULT_TXT
            self.widget.txtMsg.addEventListener(events.EVENT_CHANGE, self.handleInputTxtChange, False, 0, True)
        self.refreshInfo()

    def getFriendList(self):
        p = BigWorld.player()
        friendGroups = p.getFriendGroupOrder()
        friendList = []
        for gbId, friendInfo in p.friend.iteritems():
            if friendInfo.group not in friendGroups:
                continue
            info = {}
            info['gbId'] = gbId
            info['label'] = friendInfo.getFullName()
            friendList.append(info)

        self.friendList = friendList
        return friendList

    def dropDownlabelFunction(self, *args):
        label = ASObject(args[3][0]).label
        return GfxValue(ui.gbk2unicode(label))

    def handleIndexChange(self, *args):
        self.sendFriendIdx = int(self.widget.dropDown.selectedIndex)

    def handleInputTxtChange(self, *args):
        self.sendMsg = self.widget.txtMsg.text
        self.widget.txtDesc.text = gameStrings.TIANYU_MALL_BUY_V2_LEFT_TEXT_CNT % (160 - int(self.widget.txtMsg.length))

    def handleConterChange(self, *args):
        self.buyCnt = int(self.widget.numStepper.count)
        self.refreshInfo()

    def _onYesBtnClick(self, *args):
        if self.buyCnt < 1:
            return
        p = BigWorld.player()
        if self.priceVal * self.buyCnt > p.unbindCoin + p.bindCoin + p.freeCoin:
            p.showGameMsg(GMDD.data.NOT_ENOUGH_COIN, ())
            return
        itemName = MID.data.get(self.mallId, {}).get('itemName', '')
        if self.displayMode == uiConst.TIANYU_MALL_BUY_MODE_SEND:
            if self.sendFriendIdx < 0:
                return
            friendName = self.friendList[self.sendFriendIdx]['label']
            self.hide()
            self.sendConfirmCallback()
        else:
            self.hide()
            self.buyConfirmCallback()

    @ui.checkInventoryLock()
    def buyConfirmCallback(self):
        discountInfo = clientUtils.getMallItemDiscountInfo([self.mallId])
        p = BigWorld.player()
        p.base.preferentialActivityBuy(self.activityId, [self.mallId], [self.buyCnt], p.cipherOfPerson, 0, discountInfo)

    def sendConfirmCallback(self):
        if self.sendFriendIdx >= len(self.friendList):
            return
        p = BigWorld.player()
        friendGbId = self.friendList[self.sendFriendIdx]['gbId']
        p.base.preferentialActivityGivePay(self.activityId, friendGbId, [self.mallId], [self.buyCnt], self.sendMsg, p.cipherOfPerson)

    def _onNoBtnClick(self, *args):
        self.hide()

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.txtTotalCost.text = str(self.buyCnt * self.priceVal)
