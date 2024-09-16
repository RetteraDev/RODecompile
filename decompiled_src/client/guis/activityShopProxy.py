#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activityShopProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import uiConst
import events
import const
import utils
import compositeShopHelpFunc
import commShop
from item import Item
from uiProxy import UIProxy
from asObject import ASObject
from gameStrings import gameStrings
from guis.asObject import ASUtils
from guis.asObject import TipManager
from data import sys_config_data as SCD
from data import private_shop_data as PSD
from cdata import game_msg_def_data as GMDD
from cdata import composite_shop_trade_data as CSTD
from data import consumable_item_data as CID
ITEM_COUNT_MAX = 10
COST0_POS_Y = 130
COST1_POS_Y = 148
COST_POS_MID = 18
TEXT_COLOR_RED = '#F43804'
TEXT_COLOR_NORMAL = '#FFFFE7'
COUNT_DOWN_COLOR_RED = '#CC2929'
COUNT_DOWN_COLOR_NORMAL = '#FFFFF5'
MAOXIANJIA_FAMEID = 410
YUNCHUI_FAME_ID = 453
DIJIA_ITEM_TO_FAME = 0
DIJIA_ITEM_TO_ITEM = 1
BONUS_TYPES = ['yunChui',
 'tianBi',
 'cash',
 'bindCash']
BONUS_DESC = [gameStrings.TEXT_INVENTORYPROXY_3299,
 gameStrings.TEXT_INVENTORYPROXY_3298,
 gameStrings.TEXT_INVENTORYPROXY_3296,
 gameStrings.TEXT_INVENTORYPROXY_3297]
CONSUME_ITEM_MAX_COUNT = 2
CONSUME_MAX_COUNT = 2

class ActivityShopProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivityShopProxy, self).__init__(uiAdapter)
        self.widget = None
        self.resetData()
        self.uiAdapter.registerEscFunc(uiConst.WIDGET_ACTIVITY_SHOP, self.hide)

    def refreshCurrPrivateShop(self):
        if self.shopId and self.shopInv != None:
            self.refreshPrivateShop(self.shopId, self.shopInv)

    def refreshPrivateShop(self, shopId, shopInv, forceOpen = False):
        self.shopInv = shopInv
        self.shopId = shopId
        self.tRefreshFree = shopInv.tRefreshFree
        self.refreshCnt = shopInv.refreshCnt
        self.itemList = [ x for x in shopInv.pages[0] if x != const.CONT_EMPTY_VAL ]
        if (not self.widget or not self.widget.stage) and forceOpen:
            self.show()
        else:
            self.refreshFrame()
            self.setRefreshConsume()

    def refreshSingleItems(self, page, pos, item):
        if not self.widget or not self.widget.stage:
            return
        if pos < len(self.itemMCList):
            self.itemList[pos] = item
            mc = self.itemMCList[pos]
            self.setItemMC(mc, item)
            self.refreshBuySetting()

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self._initUI()
        BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.refreshBuySetting)
        BigWorld.player().registerEvent(const.EVENT_ITEM_REMOVE, self.refreshBuySetting)

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_ACTIVITY_SHOP)

    def getCurrPrivateShop(self):
        BigWorld.player().getCurrPrivateShop()

    def clearWidget(self):
        self.widget = None
        self.timer = None
        p = BigWorld.player()
        if p:
            BigWorld.player().base.closePrivateShop(self.shopId)
            BigWorld.player().unRegisterEvent(const.EVENT_ITEM_CHANGE, self.refreshBuySetting)
            BigWorld.player().unRegisterEvent(const.EVENT_ITEM_REMOVE, self.refreshBuySetting)
        self.resetData()
        gameglobal.rds.ui.messageBox.checkOnceMap[uiConst.CHECK_ONCE_TYPE_ACTIVITY_SHOP_REFRESH] = False
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ACTIVITY_SHOP)

    def resetData(self):
        self.shopId = 0
        self.shopInv = None
        self.itemMCList = []
        self.lastSelectedMC = None
        self.buyItemCount = 1
        self.diJiaItemNum = 0
        self.diJiaItemToItemNum = 0
        self.discountMC = None
        self.timer = None
        self.dynamicMcList = []
        self.lastBuySettingId = 0

    def setItemList(self):
        if not self.widget or not self.widget.stage:
            return
        if not self.widget.mainFrame:
            return
        self.itemMCList = []
        for i in xrange(10):
            mc = self.widget.mainFrame.getChildByName('item%d' % i)
            mc.removeEventListener(events.MOUSE_CLICK, self.onItemClick)
            self.itemMCList.append(mc)

        itemList = self.itemList
        for i, itemData in enumerate(itemList):
            if i >= ITEM_COUNT_MAX:
                break
            mc = self.itemMCList[i]
            self.setItemMC(mc, itemData)
            mc.addEventListener(events.MOUSE_CLICK, self.onItemClick, False, 0, True)

        self.refreshBuySetting()

    def refreshFrame(self):
        if not self.widget or not self.widget.stage:
            return
        for item in self.itemMCList:
            item.removeEventListener(events.MOUSE_CLICK, self.onItemClick)

        self.widget.mainFrame.gotoAndStop(self.widget.mainFrame.totalFrames)
        if self.lastSelectedMC:
            if self.lastSelectedMC.item:
                self.lastSelectedMC.item.selected = False
                self.widget.buySetting.visible = False
        BigWorld.callback(0.05, self.setItemList)
        if not self.timer:
            self.addTick()

    def addTick(self):
        if not self.widget or not self.widget.stage:
            if self.timer:
                BigWorld.cancelCallback(self.timer)
                self.timer = None
            return
        elif not self.widget.countDown:
            return
        else:
            left = self.getLeftTime()
            shopData = PSD.data.get(self.shopId, {})
            if not shopData:
                return
            if left == 0:
                timeDesc = gameStrings.ACTIVITY_SHOP_ZERO_SECOND
                self.widget.countDown.text = gameStrings.ACTIVITY_SHOP_COUNT_DOWN
                self.widget.refreshBtn.label = gameStrings.ACTIVITY_SHOP_REFRESH_BTN1
            else:
                timeDesc = utils.formatTimeStr(left)
                self.widget.refreshBtn.label = gameStrings.ACTIVITY_SHOP_REFRESH_BTN2
            if self.shopInv.refreshCnt >= len(shopData.get('refreshConsumes', {})):
                timeDesc = uiUtils.toHtml(timeDesc, COUNT_DOWN_COLOR_RED)
            else:
                timeDesc = uiUtils.toHtml(timeDesc, COUNT_DOWN_COLOR_NORMAL)
            leftDesc = gameStrings.ACTIVITY_SHOP_LEFT_TIME % timeDesc
            self.widget.countDown.htmlText = leftDesc
            self.timer = BigWorld.callback(0.2, self.addTick)
            return

    def setRefreshConsume(self):
        if not self.widget or not self.widget.stage:
            return
        left = self.getLeftTime()
        if left == 0:
            self.widget.refreshConsumeDesc.visible = False
            self.widget.refreshConsume.visible = False
            self.widget.costIcon.visible = False
            self.widget.costItem.visible = False
        else:
            self.widget.refreshConsumeDesc.visible = True
            self.widget.refreshConsume.visible = True
            shopData = PSD.data.get(self.shopId, {})
            if not shopData:
                return
            refreshConsumes = shopData.get('refreshConsumes', ())
            if refreshConsumes:
                if self.shopInv and self.shopInv.refreshCnt < len(refreshConsumes):
                    consume = refreshConsumes[self.shopInv.refreshCnt]
                else:
                    consume = refreshConsumes[-1]
                consumeItems, cash, bindCash, coin = consume[:4]
                fame = len(consume) > 4 and consume[4] or 0
                consumeCount = 0
                if consumeItems:
                    itemId, consumeCount = consumeItems[0]
                    path = uiUtils.getItemIconPath(itemId)
                    self.widget.costIcon.visible = False
                    self.widget.costItem.visible = True
                    self.widget.costItem.fitSize = True
                    self.widget.costItem.loadImage(path)
                    TipManager.addItemTipById(self.widget.costItem, itemId)
                else:
                    bonusType = 'cash'
                    if cash:
                        bonusType = 'cash'
                        consumeCount = cash
                    elif bindCash:
                        bonusType = 'bindCash'
                        consumeCount = bindCash
                    elif coin:
                        bonusType = 'tianBi'
                        consumeCount = coin
                    elif fame:
                        bonusType = 'yunChui'
                        consumeCount = fame
                    self.widget.costIcon.visible = True
                    self.widget.costItem.visible = False
                    self.widget.costIcon.bonusType = bonusType
                    TipManager.removeTip(self.widget.costItem)
                self.widget.refreshConsume.text = '*' + str(consumeCount)
        if self.shopInv:
            self.widget.refreshTimes.text = gameStrings.ACTIVITY_SHOP_REFRESH_TIMES % self.shopInv.refreshCnt

    def getLeftTime(self):
        if not self.shopInv:
            return 0
        tNext = commShop.calcPrivateShopNextRefreshFreeTime(self.shopInv.tRefreshFree)
        now = utils.getNow()
        left = max(0, tNext - now)
        return left

    def setItemMC(self, mc, itemData):
        compositeId = itemData.compositeId
        compositeData = CSTD.data.get(compositeId, None)
        if not compositeData:
            return
        else:
            tag = compositeData.get('tag', '')
            rare = tag == 'rare'
            itemInfo = uiUtils.getGfxItemById(itemData.id)
            mc.item.itemSllot.setItemSlotData(itemInfo)
            mc.item.itemSllot.dragable = False
            mc.item.itemSllot.itemId = itemData.id
            mc.item.itemSllot.addEventListener(events.MOUSE_CLICK, self.handleShowFit, False, 0, True)
            itemName = uiUtils.getItemColorName(itemData.id)
            mc.item.itemBuyName.htmlText = self._getLimitStr(itemData)
            mc.item.itemName.htmlText = itemName
            mc.item.data = self.itemList.index(itemData)
            cost0, cost1 = self.getItemCostNoDiKou(compositeData)
            if cost1:
                mc.item.cost0.y = COST0_POS_Y
                mc.item.cost1.y = COST1_POS_Y
                mc.item.cost1.visible = True
                self.setCost(mc.item.cost0, cost0)
                self.setCost(mc.item.cost1, cost1)
            else:
                mc.item.cost0.y = (COST0_POS_Y + COST1_POS_Y) / 2
                mc.item.cost1.visible = False
                self.setCost(mc.item.cost0, cost0)
            if rare:
                mc.gotoAndPlay('effect')
                mc.bg.gotoAndPlay(1)
                mc.effect.gotoAndPlay(1)
            else:
                mc.gotoAndStop('normal')
                mc.effect.gotoAndPlay(1)
                self.widget.setChildIndex(mc, self.widget.numChildren - 1)
            ASUtils.setHitTestDisable(mc.effect, True)
            if tag:
                mc.item.tag.visible = True
                mc.item.tag.gotoAndStop(tag)
            else:
                mc.item.tag.visible = False
            discountRate = compositeData.get('discountRate', 0)
            if discountRate:
                mc.item.discountLabel.visible = True
                intPart = int(discountRate * 10.0)
                floatPart = int((discountRate * 10.0 - intPart) * 10.0)
                if floatPart:
                    subText = '.%d%s' % (floatPart, gameStrings.ACTIVITY_SHOP_PROXY_DISCOUNT)
                else:
                    subText = gameStrings.ACTIVITY_SHOP_PROXY_DISCOUNT
                mc.item.discountLabel.mainText.text = str(intPart)
                mc.item.discountLabel.subText.text = subText
            else:
                mc.item.discountLabel.visible = False
            mc.item.mouseChildren = True
            return

    def _getLimitStr(self, item):
        ret = ''
        remainNum = item.remainNum
        p = BigWorld.player()
        if remainNum != const.ITEM_NUM_INFINITE:
            buyCount = self.shopInv.buyCount.get(item.compositeId, 0)
            buyLimitCount = remainNum + buyCount
            if remainNum <= 0:
                remainBuyCountStr = uiUtils.toHtml(str(remainNum), '#F43804')
            else:
                remainBuyCountStr = str(remainNum)
            ret = gameStrings.ACTIVITY_SHOP_CAN_BUY_DESC % (remainBuyCountStr, buyLimitCount)
        return ret

    def getItemCostNoDiKou(self, compositeData):
        costFame = 0
        consumeFame = compositeData.get('consumeFame', [])
        discountRate = compositeData.get('discountRate', 0)
        cashType = compositeData.get('cashType', 2)
        for fameId, cost in consumeFame:
            if fameId == const.YUN_CHUI_JI_FEN_FAME_ID:
                costFame = cost
                break

        consumeItem = compositeData.get('consumeItem', [])
        costTianBi = compositeData.get('consumeCoin', 0)
        costBindCash = 0
        costCash = 0
        if cashType == 1 or cashType == 0:
            costBindCash = compositeData.get('consumeCash', 0)
        elif cashType == 2:
            costCash = compositeData.get('consumeCash', 0)
        if discountRate:
            costFame = commShop._applyDiscount(costFame, discountRate)
            costTianBi = commShop._applyDiscount(costTianBi, discountRate)
            costCash = commShop._applyDiscount(costCash, discountRate)
            costBindCash = commShop._applyDiscount(costBindCash, discountRate)
        costList = []
        for itemId, cnt in consumeItem:
            if len(costList) >= CONSUME_ITEM_MAX_COUNT:
                break
            if discountRate:
                cnt = commShop._applyDiscount(cnt, discountRate)
            costList.append(('item', (itemId, cnt)))

        if costTianBi and len(costList) < CONSUME_MAX_COUNT:
            costList.append(('tianBi', costTianBi))
        if costCash and len(costList) < CONSUME_MAX_COUNT:
            costList.append(('cash', costCash))
        if costFame and len(costList) < CONSUME_MAX_COUNT:
            costList.append(('yunChui', costFame))
        if costBindCash and len(costList) < CONSUME_MAX_COUNT:
            costList.append(('bindCash', costBindCash))
        while len(costList) < CONSUME_MAX_COUNT:
            costList.append(None)

        return costList

    def getItemCost(self):
        costs = [None, None]
        index = 0
        p = BigWorld.player()
        costTianBi = self.consumeInfo['tianBi']
        tianBi = p.unbindCoin + p.bindCoin + p.freeCoin
        costCash = self.consumeInfo['consumeCash']
        cash = p.cash
        costBindCash = self.consumeInfo['consumeBindCash']
        bindCash = p.bindCash
        costFame = 0
        if self.consumeInfo['fameInfo']:
            if self.consumeInfo['fameInfo'][0]:
                costFame = self.consumeInfo['fameInfo'][0][2]
        fame = p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
        costList = [costFame,
         costTianBi,
         costCash,
         costBindCash]
        ownList = [fame,
         tianBi,
         cash,
         bindCash]
        leftList = []
        for i in range(len(costList)):
            if costList[i] > 0:
                result = ownList[i] >= self.getIntCost(costList[i])
                costs[index] = (BONUS_TYPES[i],
                 BONUS_DESC[i],
                 costList[i],
                 result)
                index += 1
            else:
                leftList.append(i)
            if index >= CONSUME_MAX_COUNT:
                break

        i = 0
        while index < CONSUME_MAX_COUNT:
            costs[index] = [BONUS_TYPES[leftList[i]],
             BONUS_DESC[leftList[i]],
             0,
             True]
            i += 1
            index += 1

        return costs

    def getIntCost(self, cost):
        if isinstance(cost, int):
            return cost
        else:
            return int(cost.replace(',', ''))

    def setCost(self, mc, data):
        if not data:
            data = ('cash', 0)
        if data[0] == 'item':
            costMc = mc.costItem
            mc.costIcon.visible = False
            mc.costItem.visible = True
            itemId, cnt = data[1]
            path = uiUtils.getItemIconPath(itemId)
            mc.costItem.fitSize = True
            mc.costItem.loadImage(path)
            mc.costCount.text = str(cnt)
            TipManager.addItemTipById(mc.costItem, itemId)
        else:
            costMc = mc.costIcon
            mc.costItem.visible = False
            mc.costIcon.visible = True
            mc.costIcon.bonusType = data[0]
            mc.costCount.text = str(data[1])
            TipManager.removeTip(mc.costItem)
        width = int(mc.costCount.textWidth)
        width += 5
        mc.costCount.width = width
        startPos = (78 - width) / 2
        mc.costCount.x = startPos
        costMc.x = startPos + width + 1

    def _initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.buySetting.visible = False
        self.widget.shopName.text = SCD.data.get('activityShopName', '')
        TipManager.addTip(self.widget.question, self.widget.question.textField.text)
        TipManager.addTip(self.widget.countDown, SCD.data.get('REFRESH_TIME_DES', ''))
        self.widget.question.textField.visible = False
        self.widget.refreshBtn.addEventListener(events.MOUSE_CLICK, self.onRefreshClick, False, 0, True)
        self.widget.buySetting.closeBtn.addEventListener(events.MOUSE_CLICK, self.onBuySetCloseBtnClick, False, 0, True)
        self.widget.buySetting.buyBtn.addEventListener(events.MOUSE_CLICK, self.onBuyBtnClick, False, 0, True)
        self.widget.buySetting.numStepper.minCount = 0
        self.refreshFrame()
        self.setRefreshConsume()

    def onRefreshClick(self, *args):
        if not self.canOpen():
            self.hide()
            BigWorld.player().showGameMsg(GMDD.data.ACTIVITY_SHOP_CLOSED, ())
            return
        else:
            left = self.getLeftTime()
            if left == 0:
                msg = SCD.data.get('FRER_REFRESH_TIP', gameStrings.ACTIVITY_SHOP_IS_REFRESH)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.refreshFunc)
            else:
                shopData = PSD.data.get(self.shopId, {})
                if not shopData:
                    return
                refreshConsumes = shopData.get('refreshConsumes', ())
                if not refreshConsumes:
                    return
                consume = None
                if self.shopInv.refreshCnt < len(refreshConsumes):
                    consume = refreshConsumes[self.shopInv.refreshCnt]
                else:
                    consume = refreshConsumes[-1]
                consumeItems, cash, bindCash, coin = consume[:4]
                fame = len(consume) > 4 and consume[4] or 0
                title = gameStrings.ACTIVITY_SHOP_REMIND_MSG_TITLE
                content = gameStrings.ACTIVITY_SHOP_REMIND_MSG_CONTENT % (self.shopInv.refreshCnt + 1)
                itemdata = None
                bonusIcon = None
                itemDataList = []
                if consumeItems:
                    for itemId, consumeCount in consumeItems:
                        itemdata = uiUtils.getGfxItemById(itemId)
                        count = BigWorld.player().inv.countItemInPages(itemId, enableParentCheck=True)
                        countDesc = '%d/%d' % (count, consumeCount)
                        if consumeCount <= count:
                            countDesc = uiUtils.toHtml(countDesc, TEXT_COLOR_NORMAL)
                        else:
                            countDesc = uiUtils.toHtml(countDesc, TEXT_COLOR_RED)
                        itemdata['count'] = countDesc
                        itemDataList.append(itemdata)

                if cash:
                    bonusIcon = {'bonusType': 'cash',
                     'value': str(cash)}
                elif bindCash:
                    bonusIcon = {'bonusType': 'bindCash',
                     'value': str(bindCash)}
                elif coin:
                    bonusIcon = {'bonusType': 'tianBi',
                     'value': str(coin)}
                elif fame:
                    bonusIcon = {'bonusType': 'yunChui',
                     'value': str(fame)}
                if not gameglobal.rds.ui.messageBox.checkOnceMap.get(uiConst.CHECK_ONCE_TYPE_ACTIVITY_SHOP_REFRESH, False):
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(content, yesCallback=self.refreshFunc, itemData=itemDataList, bonusIcon=bonusIcon, title=title, isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_ACTIVITY_SHOP_REFRESH)
                else:
                    self.refreshFunc()
            return

    def refreshFunc(self):
        self.buyItemCount = 1
        self.diJiaItemNum = 0
        self.diJiaItemToItemNum = 0
        BigWorld.player().base.refreshPrivateShop(self.shopId)

    def buyItemFunc(self):
        item = self.getSelectedMCData()
        compositeShopHelpFunc.buyItem(self.shopId, item, self.buyItemCount, self.diJiaItemNum, self.diJiaItemToItemNum)

    def onBuyBtnClick(self, *args):
        item = self.getSelectedMCData()
        pos = int(self.lastSelectedMC.item.data)
        if not item or self.buyItemCount <= 0:
            return
        compositeShopHelpFunc.buyItem(self.shopId, item, self.buyItemCount, self.diJiaItemNum, self.diJiaItemToItemNum, 0, pos)

    def onBuySetCloseBtnClick(self, *args):
        self.widget.buySetting.visible = False

    def onItemClick(self, *args):
        e = ASObject(args[3][0])
        if e.buttonIdx != uiConst.LEFT_BUTTON:
            return
        if self.lastSelectedMC:
            if self.lastSelectedMC.name == e.currentTarget.name and self.widget.buySetting.visible == True:
                return
            if self.lastSelectedMC.item:
                self.lastSelectedMC.item.selected = False
        self.lastSelectedMC = e.currentTarget
        self.lastSelectedMC.item.selected = True
        self.buyItemCount = 1
        self.diJiaItemNum = 0
        self.diJiaItemToItemNum = 0
        self.widget.buySetting.visible = True
        self.refreshBuySetting()

    def refreshBuySetting(self, *args):
        if not self.widget or not self.widget.stage:
            return
        if not self.widget.buySetting.visible:
            return
        widget = self.widget
        self.consumeInfo = self.getConsumeInfo()
        info = self.consumeInfo
        if not widget.buySetting.visible:
            return
        costInfo = self.getItemCost()
        for i in range(len(costInfo)):
            self.setBuyCost(i, costInfo[i])

        self.setConsumeInfo(info)
        text = widget.buySetting.numStepper.numInput.textField
        if info['isValid']:
            text.htmlText = uiUtils.toHtml(text.text, TEXT_COLOR_NORMAL)
            widget.buySetting.buyBtn.enabled = True
        else:
            text.htmlText = uiUtils.toHtml(text.text, TEXT_COLOR_RED)
            widget.buySetting.buyBtn.enabled = False

    def setBuyCost(self, costIndex, costInfo):
        cashIcon = self.widget.buySetting.getChildByName('cashIcon%d' % costIndex)
        cashText = self.widget.buySetting.getChildByName('cash%d' % costIndex)
        costDesc = self.widget.buySetting.getChildByName('costDesc%d' % costIndex)
        if costInfo:
            cashIcon.bonusType = costInfo[0]
            costDesc.text = costInfo[1]
            if not costInfo[3]:
                cashText.htmlText = uiUtils.toHtml(str(costInfo[2]), TEXT_COLOR_RED)
            else:
                cashText.htmlText = uiUtils.toHtml(str(costInfo[2]), TEXT_COLOR_NORMAL)

    def setConsumeInfo(self, consumeInfo):
        conditionList = consumeInfo['conditionList']
        scrollWnd = self.widget.buySetting.scrollWind
        diJiaInfo = consumeInfo['consumeDiJiaInfo']
        posY = 0
        if self.lastBuySettingId != consumeInfo['compositeId']:
            while scrollWnd.canvas.numChildren > 0:
                scrollWnd.canvas.removeChildAt(0)

            self.dynamicMcList = []
        for i in range(len(conditionList)):
            needReIns = i >= len(self.dynamicMcList)
            if conditionList[i][0] == 'addDijia' and diJiaInfo['visible']:
                if needReIns:
                    itemMC = self.widget.getInstByClsName('ActivityShop_BuyItemDiKou')
                    scrollWnd.canvas.addChild(itemMC)
                    self.dynamicMcList.append(itemMC)
                else:
                    itemMC = self.dynamicMcList[i]
                self.setDiJiaInfo(itemMC, diJiaInfo, posY)
            else:
                if needReIns:
                    itemMC = self.widget.getInstByClsName('ActivityShop_BuyLimit')
                    scrollWnd.canvas.addChild(itemMC)
                    self.dynamicMcList.append(itemMC)
                else:
                    itemMC = self.dynamicMcList[i]
                self.setLimitMC(itemMC, conditionList[i])
            itemMC.visible = True
            itemMC.y = posY
            if itemMC:
                posY += itemMC.height

        self.updateBuyItemInfo(consumeInfo)
        scrollWnd.refreshHeight()
        self.lastBuySettingId = consumeInfo['compositeId']

    def setLimitMC(self, mc, data):
        mc.yes.visible = data[1]
        mc.no.visible = not data[1]
        ASUtils.textFieldAutoSize(mc.desc, data[0])
        if len(data) > 2:
            mc.descNum.text = data[2]
        else:
            mc.descNum.text = ''
        if len(data) > 3:
            TipManager.addItemTipById(mc.desc, data[3])

    def updateBuyItemInfo(self, consumeInfo):
        widget = self.widget
        selectedData = self.getSelectedMCData()
        itemInfo = uiUtils.getGfxItemById(selectedData.id)
        itemName = uiUtils.getItemColorName(selectedData.id)
        if not widget.buySetting.numSet.slot.data:
            widget.buySetting.numSet.slot.setItemSlotData(itemInfo)
        elif int(widget.buySetting.numSet.slot.data.id) == itemInfo['id']:
            widget.buySetting.numSet.slot.setValueAmountTxt(itemInfo['count'])
        else:
            widget.buySetting.numSet.slot.setItemSlotData(itemInfo)
        widget.buySetting.numSet.slot.dragable = False
        widget.buySetting.numSet.slot.valueAmount.visible = False
        widget.buySetting.numSet.nameField.textField.htmlText = itemName
        ASUtils.autoSizeWithFont(widget.buySetting.numSet.nameField.textField)
        mwarp = Item.maxWrap(selectedData.id)
        count = 999 if selectedData.remainNum == const.ITEM_NUM_INFINITE else selectedData.remainNum
        widget.buySetting.numStepper.removeEventListener(events.EVENT_COUNT_CHANGE, self.handleCountChange)
        widget.buySetting.numStepper.minCount = 1
        widget.buySetting.numStepper.maxCount = max(1, min(mwarp, count, compositeShopHelpFunc.getConsumeMaxNum(selectedData)))
        widget.buySetting.numStepper.count = consumeInfo['count']
        widget.buySetting.numStepper.addEventListener(events.EVENT_COUNT_CHANGE, self.handleCountChange, False, 0, True)
        widget.buySetting.numStepper.nextBtn.enabled = widget.buySetting.numStepper.count < widget.buySetting.numStepper.maxCount
        widget.buySetting.maxBtn.addEventListener(events.MOUSE_CLICK, self.handleMaxBtn, False, 0, True)

    def handleMaxBtn(self, *args):
        self.widget.buySetting.numStepper.count = int(self.widget.buySetting.numStepper.maxCount)

    def getSelectedMCData(self):
        if self.lastSelectedMC:
            index = int(self.lastSelectedMC.item.data)
            item = self.itemList[index]
            return item
        else:
            return None

    def handleCountChange(self, *args):
        e = ASObject(args[3][0])
        self.buyItemCount = int(e.currentTarget.count)
        self.refreshBuySetting()

    def setDiJiaInfo(self, itemMC, diJiaInfo, posY):
        if diJiaInfo['visible']:
            itemMC.y = posY
            itemMC.yes.visible = diJiaInfo['check']
            itemMC.no.visible = not diJiaInfo['check']
            itemMC.itemName.text = diJiaInfo['itemName']
            ASUtils.textFieldAutoSize(itemMC.desc1, diJiaInfo['diJiaDesc1'])
            TipManager.addItemTipById(itemMC.desc1, diJiaInfo['diJiaItemId1'])
            itemMC.desc2.htmlText = diJiaInfo['diJiaDesc2']
            itemMC.desc2.height = itemMC.desc2.textHeight + 5
            itemMC.itemNum.htmlText = diJiaInfo['diJiaNumStr']
            if diJiaInfo['diJiaItemId2']:
                TipManager.addItemTipById(itemMC.desc2, diJiaInfo['diJiaItemId2'])
            else:
                TipManager.removeTip(itemMC.desc2)
            posY = itemMC.desc2.y + itemMC.desc2.height + 5
            itemMC.itemNum.y = posY
            itemMC.numStepper.y = posY - 3
            itemMC.maxBtn.y = posY - 3
            itemMC.bg.height = posY + 25
            itemMC.numStepper.removeEventListener(events.EVENT_COUNT_CHANGE, self.handleDiJiaCountChange)
            itemMC.maxBtn.removeEventListener(events.MOUSE_CLICK, self.handleDiJiaMaxBtn)
            itemMC.numStepper.maxCount = diJiaInfo['numLimit']
            itemMC.numStepper.minCount = 0
            itemMC.numStepper.count = diJiaInfo['itemNum']
            itemMC.numStepper.enableMouseWheel = False
            itemMC.numStepper.validateNow()
            itemMC.numStepper.addEventListener(events.EVENT_COUNT_CHANGE, self.handleDiJiaCountChange, False, 0, True)
            itemMC.maxBtn.addEventListener(events.MOUSE_CLICK, self.handleDiJiaMaxBtn, False, 0, True)
            self.discountMC = itemMC

    def handleDiJiaMaxBtn(self, *args):
        e = ASObject(args[3][0])
        mc = e.currentTarget
        mc.parent.numStepper.count = mc.parent.numStepper.maxCount

    def handleDiJiaCountChange(self, *args):
        e = ASObject(args[3][0])
        num = int(e.currentTarget.count)
        data = self.getSelectedMCData()
        compositeId = data.compositeId
        compositeData = CSTD.data.get(compositeId, {})
        diJiaType = compositeShopHelpFunc._getDijiaType(compositeData)
        if diJiaType == DIJIA_ITEM_TO_FAME:
            if self.diJiaItemNum == num:
                return
            self.diJiaItemNum = int(self.discountMC.numStepper.count)
            self.diJiaItemToItemNum = 0
        elif diJiaType == DIJIA_ITEM_TO_ITEM:
            if num == self.diJiaItemToItemNum:
                return
            self.diJiaItemNum = 0
            self.diJiaItemToItemNum = int(self.discountMC.numStepper.count)
        self.refreshBuySetting()

    def getConsumeInfo(self):
        data = self.getSelectedMCData()
        compositeId = data.compositeId
        consumeInfo = compositeShopHelpFunc.getConsumeInfo(compositeId, self.buyItemCount, self.diJiaItemNum, self.diJiaItemToItemNum)
        return consumeInfo

    def onEnterFrame(self, *args):
        e = ASObject(args[3][0])
        mc = e.currentTarget
        if mc.currentFrame >= mc.totalFrames:
            mc.removeEventListener(events.EVENT_ENTER_FRAME, self.onEnterFrame)
            self.setItemList()

    def onCloseClick(self, *args):
        self.autoClose = True
        self.hide()

    def getNRefreshTime(self):
        shpId = BigWorld.player()._getCurrPrivateShopId()
        shopInv = BigWorld.player().getPrivateShop(shpId)
        if not shopInv:
            return
        tNext = commShop.calcPrivateShopNextRefreshFreeTime(shopInv.tRefreshFree)
        return tNext

    def hasNewInfo(self):
        return False

    def canOpen(self):
        if not gameglobal.rds.configData.get('enablePrivateShop', False):
            return False
        shopId = SCD.data.get('PRIVATE_SHOP_ID', 0)
        if not shopId:
            return False
        openLv = PSD.data.get(shopId, {}).get('minLv', 0)
        if BigWorld.player().lv < openLv:
            return False
        startTime = PSD.data.get(shopId, {}).get('startTime', None)
        endTime = PSD.data.get(shopId, {}).get('endTime', None)
        if not startTime or not endTime:
            return False
        elif True not in [ utils.inTimeTupleRangeWithYear(startTime[i], endTime[i]) for i in xrange(len(startTime)) ]:
            return False
        else:
            return True

    def handleShowFit(self, *args):
        e = ASObject(args[3][0])
        itemId = int(e.currentTarget.itemId)
        if e.ctrlKey and e.buttonIdx == uiConst.LEFT_BUTTON:
            cidData = CID.data.get(itemId, {})
            sType = cidData.get('sType', 0)
            if sType == Item.SUBTYPE_2_GET_SELECT_ITEM:
                gameglobal.rds.ui.itemChoose.show(itemId, showType=0)
            else:
                self.uiAdapter.fittingRoom.addItem(Item(itemId))
