#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildAuctionWorldProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiUtils
import uiConst
import ui
import events
import utils
import gametypes
from uiProxy import UIProxy
from asObject import ASObject
from gamestrings import gameStrings
from guis.asObject import ASUtils
from data import item_data as ID
from data import guild_config_data as GCD
from cdata import game_msg_def_data as GMDD
from cdata import guild_consign_item_data as GCID

class GuildAuctionWorldProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildAuctionWorldProxy, self).__init__(uiAdapter)
        self.itemNameList = []
        self.reset()
        self.clearAll()

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.selectTab(uiConst.GUILD_AUCTION_SECOND_TAB_BUY)

    def unRegisterPanel(self):
        self.reset()

    def reset(self):
        self.widget = None
        self.currentTabIndex = -1
        self.filterKey = 0
        self.itemNameList = []
        self.selectedItemUUID = 0
        self.selectedMc = None
        self.sortDict = {'buyPanelPrice': True,
         'bidPanelPrice': True}

    def clearAll(self):
        self.stateDict = {}
        self.itemInfoDict = {}
        self.itemInfolVer = 0
        self.historyInfoList = []
        self.historyInfoVer = 0

    def initUI(self):
        self.widget.buyBtn.groupName = 'tab'
        self.widget.buyBtn.tabIdx = uiConst.GUILD_AUCTION_SECOND_TAB_BUY
        self.widget.buyBtn.addEventListener(events.BUTTON_CLICK, self.handleClickTab, False, 0, True)
        self.widget.bidBtn.groupName = 'tab'
        self.widget.bidBtn.tabIdx = uiConst.GUILD_AUCTION_SECOND_TAB_BID
        self.widget.bidBtn.addEventListener(events.BUTTON_CLICK, self.handleClickTab, False, 0, True)
        self.widget.timeOutHint.htmlText = uiUtils.getTextFromGMD(GMDD.data.GUILD_AUCTION_WORLD_TIME_OUT_HINT, '')
        buyPanel = self.widget.buyPanel
        buyPanel.scrollWndList.itemRenderer = 'GuildAuctionWorld_BuyItem'
        buyPanel.scrollWndList.dataArray = []
        buyPanel.scrollWndList.lableFunction = self.buyItemFunction
        buyPanel.scrollWndList.itemHeight = 55
        buyPanel.input.labelFunction = self.inputLabelFunction
        buyPanel.input.labelField = None
        buyPanel.input.addEventListener(events.EVENT_CHANGE, self.handleInputChange, False, 0, True)
        buyPanel.input.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleInputKeyUp, 0, uiConst.AS_INT_MIN_VALUE)
        buyPanel.input.addEventListener(events.FOCUS_EVENT_FOCUS_IN, self.handleInputFocusIn, False, 0, True)
        buyPanel.searchBtn.addEventListener(events.BUTTON_CLICK, self.handleClickSearchBtn, False, 0, True)
        self.widget.removeAllInst(buyPanel.typeView.canvas)
        posY = 0
        for label, filterKey in GCD.data.get('guildAuctionTypeViewList', ()):
            itemMc = self.widget.getInstByClsName('GuildAuctionWorld_TypeItem')
            itemMc.label = label
            itemMc.filterKey = filterKey
            itemMc.selected = posY == 0
            itemMc.groupName = 'empty'
            itemMc.groupName = 'typeView'
            itemMc.addEventListener(events.BUTTON_CLICK, self.handleClickTypeItem, False, 0, True)
            itemMc.y = posY
            posY += 26
            buyPanel.typeView.canvas.addChild(itemMc)

        buyPanel.typeView.refreshHeight()
        buyPanel.priceBtn.data = 'buyPanelPrice'
        buyPanel.priceBtn.addEventListener(events.BUTTON_CLICK, self.handleClickSortBtn, False, 0, True)
        buyPanel.bidItemBtn.addEventListener(events.BUTTON_CLICK, self.handleClickBidItemBtn, False, 0, True)
        buyPanel.buyItemBtn.addEventListener(events.BUTTON_CLICK, self.handleClickBuyItemBtn, False, 0, True)
        bidPanel = self.widget.bidPanel
        bidPanel.scrollWndList.itemRenderer = 'GuildAuctionWorld_BidItem'
        bidPanel.scrollWndList.dataArray = []
        bidPanel.scrollWndList.lableFunction = self.bidItemFunction
        bidPanel.scrollWndList.itemHeight = 55
        bidPanel.priceBtn.data = 'bidPanelPrice'
        bidPanel.priceBtn.addEventListener(events.BUTTON_CLICK, self.handleClickSortBtn, False, 0, True)
        bidPanel.bidItemBtn.addEventListener(events.BUTTON_CLICK, self.handleClickBidItemBtn, False, 0, True)
        bidPanel.buyItemBtn.addEventListener(events.BUTTON_CLICK, self.handleClickBuyItemBtn, False, 0, True)

    def queryInfo(self):
        if self.checkAuctionClose():
            return
        BigWorld.player().base.getAllWorldConsignments(self.itemInfolVer)

    def checkAuctionClose(self):
        if not self.stateDict:
            return True
        for val in self.stateDict.itervalues():
            if val != gametypes.WORLD_CONSIGN_STATE_CLOSE:
                return False

        return True

    def updateItemListInfo(self, itemInfoList, itemInfolVer):
        self.itemInfoDict = {}
        for itemInfo in itemInfoList:
            itemId = itemInfo[1]
            source = itemInfo[2]
            if source in gametypes.WING_WORLD_COUNTRY_CONSIGN_SOURCE_RANGE:
                fixedPriceKey = 'guildFixPrice'
                bidPriceKey = 'guildBidPrice'
                makeUpKey = 'guildBidMakup'
            else:
                fixedPriceKey = 'worldFixPrice'
                bidPriceKey = 'worldBidPrice'
                makeUpKey = 'worldBidMakup'
            serverProgress = itemInfo[10]
            gcidData = GCID.data.get((itemId, serverProgress), {})
            self.itemInfoDict[itemInfo[0]] = {'itemId': itemId,
             'serverProgress': serverProgress,
             'bidPrice': gcidData.get(bidPriceKey, 0),
             'fixedPrice': gcidData.get(fixedPriceKey, 0),
             'bidMakup': gcidData.get(makeUpKey, 0),
             'vendorSource': itemInfo[2],
             'tBegin': itemInfo[3],
             'tEnd': itemInfo[4],
             'currBidPrice': itemInfo[5],
             'bidderRole': itemInfo[6],
             'bidderGbId': itemInfo[7],
             'bidCount': itemInfo[8],
             'onceBid': itemInfo[9]}

        self.itemInfolVer = itemInfolVer
        self.refreshInfoInCD()

    def updateItemInfo(self, itemInfo):
        itemId = itemInfo[1]
        serverProgress = itemInfo[10]
        gcidData = GCID.data.get((itemId, serverProgress), {})
        source = itemInfo[2]
        if source in gametypes.WING_WORLD_COUNTRY_CONSIGN_SOURCE_RANGE:
            fixedPriceKey = 'guildFixPrice'
            bidPriceKey = 'guildBidPrice'
            makeUpKey = 'guildBidMakup'
        else:
            fixedPriceKey = 'worldFixPrice'
            bidPriceKey = 'worldBidPrice'
            makeUpKey = 'worldBidMakup'
        self.itemInfoDict[itemInfo[0]] = {'itemId': itemId,
         'serverProgress': serverProgress,
         'bidPrice': gcidData.get(bidPriceKey, 0),
         'fixedPrice': gcidData.get(fixedPriceKey, 0),
         'bidMakup': gcidData.get(makeUpKey, 0),
         'vendorSource': itemInfo[2],
         'tBegin': itemInfo[3],
         'tEnd': itemInfo[4],
         'currBidPrice': itemInfo[5],
         'bidderRole': itemInfo[6],
         'bidderGbId': itemInfo[7],
         'bidCount': itemInfo[8],
         'onceBid': itemInfo[9]}
        self.refreshInfoInCD()

    def deleteItemInfo(self, itemUUID):
        self.itemInfoDict.pop(long(itemUUID), None)
        self.refreshInfoInCD()

    def updateStateDict(self, stateDict):
        self.stateDict = stateDict
        self.queryInfo()
        self.updateOpenPushMsg()
        self.refreshInfoInCD()

    def updateOpenPushMsg(self):
        if not gameglobal.rds.configData.get('enableWorldConsign', False) or self.checkAuctionClose() or gameglobal.rds.ui.guildAuctionGuild.checkIsSoul():
            self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_AUCTION_WORLD_OPEN)
        else:
            self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_AUCTION_WORLD_OPEN)

    def handleClickTab(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.selected:
            return
        self.selectTab(itemMc.tabIdx)

    def selectTab(self, tabIdx):
        if tabIdx == uiConst.GUILD_AUCTION_SECOND_TAB_BUY:
            self.widget.buyBtn.selected = True
            self.queryInfo()
        elif tabIdx == uiConst.GUILD_AUCTION_SECOND_TAB_BID:
            self.widget.bidBtn.selected = True
        self.selectedItemUUID = 0
        self.selectedMc = None
        self.currentTabIndex = tabIdx
        self.refreshInfo()

    @ui.callInCD(0.5)
    def refreshInfoInCD(self):
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        if self.currentTabIndex == uiConst.GUILD_AUCTION_SECOND_TAB_BUY:
            self.refreshBuyInfo()
        elif self.currentTabIndex == uiConst.GUILD_AUCTION_SECOND_TAB_BID:
            self.refreshBidInfo()
        self.refreshTianbiInfo()

    def refreshBuyInfo(self):
        if not self.widget:
            return
        if self.currentTabIndex != uiConst.GUILD_AUCTION_SECOND_TAB_BUY:
            return
        buyPanel = self.widget.buyPanel
        if self.checkAuctionClose():
            self.widget.timeOutHint.visible = True
            buyPanel.visible = False
            self.widget.bidPanel.visible = False
            return
        self.widget.timeOutHint.visible = False
        buyPanel.visible = True
        self.widget.bidPanel.visible = False
        if self.sortDict.get('buyPanelPrice', True):
            buyPanel.priceBtn.sortIcon.gotoAndStop('down')
        else:
            buyPanel.priceBtn.sortIcon.gotoAndStop('up')
        itemNameSet = set()
        inputStr = buyPanel.input.text
        buyList = []
        for uuid, itemDetail in self.itemInfoDict.iteritems():
            itemId = itemDetail.get('itemId', 0)
            serverProgress = itemDetail.get('serverProgress', 0)
            if self.filterKey and self.filterKey != GCID.data.get((itemId, serverProgress), {}).get('filterKey', 0):
                continue
            itemName = ID.data.get(itemId, {}).get('name', '')
            itemNameSet.add(itemName)
            if inputStr != '' and not uiUtils.filterPinYin(inputStr, itemName):
                continue
            buyList.append({'uuid': uuid,
             'fixedPrice': itemDetail.get('fixedPrice', 0)})

        buyList.sort(key=lambda x: x['fixedPrice'], reverse=self.sortDict.get('buyPanelPrice', True))
        buyPanel.scrollWndList.dataArray = buyList
        buyPanel.scrollWndList.validateNow()
        buyPanel.emptyHint.visible = len(buyList) == 0
        self.itemNameList = list(itemNameSet)
        self.updateSelectedItemBtnState()

    def buyItemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        uuid = long(itemData.uuid)
        itemDetail = self.itemInfoDict.get(uuid, {})
        if not itemDetail:
            itemMc.visible = False
            return
        itemMc.visible = True
        itemMc.uuid = uuid
        itemMc.overMc.visible = False
        if self.selectedItemUUID == uuid:
            self.selectedMc = itemMc
            itemMc.selectMc.visible = True
        else:
            itemMc.selectMc.visible = False
        itemId = itemDetail.get('itemId', 0)
        itemMc.itemSlot.dragable = False
        itemMc.itemSlot.setItemSlotData(uiUtils.getGfxItemById(itemId, stateFlag=True))
        itemMc.itemName.htmlText = uiUtils.getItemColorName(itemId)
        idData = ID.data.get(itemId, {})
        itemMc.itemLv.text = idData.get('lvReq', 0)
        if idData.get('bindType', 0) == gametypes.ITEM_BIND_TYPE_FOREVER:
            itemMc.bindType.text = gameStrings.GUILD_AUCTION_BIND_TYPE_FOREVER
        else:
            itemMc.bindType.text = gameStrings.GUILD_AUCTION_BIND_TYPE_NOT_FOREVER
        if itemDetail.get('bidCount', 0):
            itemMc.paiIcon.visible = True
            if itemDetail.get('bidderGbId', 0) == BigWorld.player().gbId:
                itemMc.paiIcon.gotoAndStop('me')
            else:
                itemMc.paiIcon.gotoAndStop('other')
        else:
            itemMc.paiIcon.visible = False
        now = utils.getNow()
        leftBeginTime = max(0, itemDetail.get('tBegin', 0) - now)
        leftEndTime = max(0, itemDetail.get('tEnd', 0) - now)
        if leftBeginTime > 0:
            itemMc.time.gotoAndStop('ready')
            itemMc.time.readyTime.text = gameStrings.GUILD_AUCTION_READY_TIME_STR % uiUtils.formatTimeShort(leftBeginTime)
            itemMc.time.totalTime.text = uiUtils.formatTimeShort(leftEndTime - leftBeginTime)
        else:
            itemMc.time.gotoAndStop('normal')
            itemMc.time.totalTime.text = uiUtils.formatTimeShort(leftEndTime)
        itemMc.currentBidPrice.text = format(self.getCurBidPrice(uuid), ',')
        itemMc.fixedPrice.text = format(itemDetail.get('fixedPrice', 0), ',')
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleClickItem, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleOverItem, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleOutItem, False, 0, True)

    def getCurBidPrice(self, itemUUID):
        itemDetail = self.itemInfoDict.get(itemUUID, {})
        if not itemDetail:
            return 0
        elif itemDetail.get('bidCount', 0):
            return itemDetail.get('currBidPrice', 0) + itemDetail.get('bidMakup', 0)
        else:
            return itemDetail.get('bidPrice', 0)

    def handleClickTypeItem(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.selected:
            return
        itemMc.selected = True
        self.filterKey = itemMc.filterKey
        self.refreshInfo()

    @ui.callFilter(1, False)
    def handleClickSortBtn(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        key = itemMc.data
        self.sortDict[key] = not self.sortDict.get(key, False)
        self.refreshInfoInCD()

    def refreshBidInfo(self):
        if not self.widget:
            return
        if self.currentTabIndex != uiConst.GUILD_AUCTION_SECOND_TAB_BID:
            return
        bidPanel = self.widget.bidPanel
        if self.checkAuctionClose():
            self.widget.timeOutHint.visible = True
            self.widget.buyPanel.visible = False
            bidPanel.visible = False
            return
        self.widget.timeOutHint.visible = False
        self.widget.buyPanel.visible = False
        bidPanel.visible = True
        if self.sortDict.get('bidPanelPrice', True):
            bidPanel.priceBtn.sortIcon.gotoAndStop('down')
        else:
            bidPanel.priceBtn.sortIcon.gotoAndStop('up')
        bidList = []
        for uuid, itemDetail in self.itemInfoDict.iteritems():
            if not itemDetail.get('onceBid', False):
                continue
            bidList.append({'uuid': uuid,
             'fixedPrice': itemDetail.get('fixedPrice', 0)})

        bidList.sort(key=lambda x: x['fixedPrice'], reverse=self.sortDict.get('bidPanelPrice', True))
        bidPanel.scrollWndList.dataArray = bidList
        bidPanel.scrollWndList.validateNow()
        self.updateSelectedItemBtnState()

    def bidItemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        uuid = long(itemData.uuid)
        itemDetail = self.itemInfoDict.get(uuid, {})
        if not itemDetail:
            itemMc.visible = False
            return
        itemMc.visible = True
        itemMc.uuid = uuid
        itemMc.overMc.visible = False
        if self.selectedItemUUID == uuid:
            self.selectedMc = itemMc
            itemMc.selectMc.visible = True
        else:
            itemMc.selectMc.visible = False
        itemId = itemDetail.get('itemId', 0)
        itemMc.itemSlot.dragable = False
        itemMc.itemSlot.setItemSlotData(uiUtils.getGfxItemById(itemId, stateFlag=True))
        itemMc.itemName.htmlText = uiUtils.getItemColorName(itemId)
        itemMc.currentBidPrice.text = format(self.getCurBidPrice(uuid), ',')
        itemMc.fixedPrice.text = format(itemDetail.get('fixedPrice', 0), ',')
        if itemDetail.get('bidderGbId', 0) == BigWorld.player().gbId:
            itemMc.paiIcon.gotoAndStop('me')
            itemMc.bidState.gotoAndStop('win')
        else:
            itemMc.paiIcon.gotoAndStop('other')
            itemMc.bidState.gotoAndStop('lose')
        itemMc.time.text = uiUtils.formatTime(max(0, itemDetail.get('tEnd', 0) - utils.getNow()))
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleClickItem, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleOverItem, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleOutItem, False, 0, True)

    def refreshTianbiInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.tianbi.htmlText = gameStrings.GUILD_AUCTION_OWN_TIANBI_STR % (format(p.unbindCoin + p.bindCoin + p.freeCoin, ','), format(p.unbindCoin, ','))

    def handleClickItem(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if long(itemMc.uuid) == self.selectedItemUUID:
            return
        else:
            self.selectedItemUUID = long(itemMc.uuid)
            if self.selectedMc != None:
                self.selectedMc.selectMc.visible = False
            self.selectedMc = itemMc
            self.selectedMc.selectMc.visible = True
            self.selectedMc.overMc.visible = False
            self.updateSelectedItemBtnState()
            return

    def updateSelectedItemBtnState(self):
        if not self.widget:
            return
        if self.currentTabIndex == uiConst.GUILD_AUCTION_SECOND_TAB_BUY:
            curPanel = self.widget.buyPanel
        elif self.currentTabIndex == uiConst.GUILD_AUCTION_SECOND_TAB_BID:
            curPanel = self.widget.bidPanel
        else:
            return
        if self.selectedItemUUID:
            curPanel.bidItemBtn.enabled = True
            curPanel.buyItemBtn.enabled = True
        else:
            curPanel.bidItemBtn.enabled = False
            curPanel.buyItemBtn.enabled = False

    def handleOverItem(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.selectMc != None and itemMc.selectMc.visible:
            return
        else:
            itemMc.overMc.visible = True
            return

    def handleOutItem(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.selectMc != None and itemMc.selectMc.visible:
            return
        else:
            itemMc.overMc.visible = False
            return

    def handleClickBidItemBtn(self, *args):
        itemDetail = self.itemInfoDict.get(self.selectedItemUUID, {})
        if not itemDetail:
            return
        curBidPrice = self.getCurBidPrice(self.selectedItemUUID)
        if curBidPrice >= itemDetail.get('fixedPrice', 0):
            BigWorld.player().showGameMsg(GMDD.data.CONSIGN_BID_BIGER_THAN_FIXED, ())
            return
        itemInfo = {'uuid': self.selectedItemUUID,
         'itemId': itemDetail.get('itemId', 0),
         'price': curBidPrice,
         'vendorSource': itemDetail.get('vendorSource', 0)}
        self.uiAdapter.guildAuctionBuy.show(uiConst.GUILD_AUCTION_BUY_TYPE_WORLD_BID, itemInfo)

    def handleClickBuyItemBtn(self, *args):
        itemDetail = self.itemInfoDict.get(self.selectedItemUUID, {})
        if not itemDetail:
            return
        itemInfo = {'uuid': self.selectedItemUUID,
         'itemId': itemDetail.get('itemId', 0),
         'price': itemDetail.get('fixedPrice', 0),
         'vendorSource': itemDetail.get('vendorSource', 0)}
        self.uiAdapter.guildAuctionBuy.show(uiConst.GUILD_AUCTION_BUY_TYPE_WORLD_BUY, itemInfo)

    def inputLabelFunction(self, *args):
        return GfxValue(ui.gbk2unicode(ASObject(args[3][0]).label))

    def handleInputFocusIn(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget != e.target:
            return
        self.showInputDropItems(True)

    def handleInputChange(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget == e.target:
            return
        self.showInputDropItems(False)

    def showInputDropItems(self, isHistory):
        inputMc = self.widget.buyPanel.input
        inputStr = inputMc.text
        tmpList = []
        for tmpName in self.itemNameList:
            if inputStr == '' or uiUtils.filterPinYin(inputStr, tmpName):
                tmpList.append({'label': tmpName})

        if isHistory:
            ASUtils.setDropdownMenuHistoryData(inputMc, tmpList)
        else:
            ASUtils.setDropdownMenuData(inputMc, tmpList)
            if inputStr == '':
                inputMc.open()

    def handleInputKeyUp(self, *args):
        e = ASObject(args[3][0])
        if int(e.keyCode) in (events.KEYBOARD_CODE_ENTER, events.KEYBOARD_CODE_NUMPAD_ENTER):
            self.searchItems()

    def handleClickSearchBtn(self, *args):
        self.searchItems()

    @ui.callAfterTime()
    def searchItems(self):
        self.refreshBuyInfo()
