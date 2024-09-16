#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonFriendNewProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import uiConst
import events
import ui
import const
import utils
import qrcode
import base64
import gametypes
import keys
from guis import messageBoxProxy
from callbackHelper import Functor
from uiProxy import UIProxy
from asObject import ASObject
from guis.asObject import ASUtils
from cdata import game_msg_def_data as GMDD
from data import school_data as SD
from data import friend_invitation_reward_data as FIRD
from data import invitation_extra_reward_data as IERD
from data import sys_config_data as SCD
from data import composite_shop_item_set_data as CSISD
from cdata import composite_shop_trade_data as CSTD
TIMED_SHOP_INDEX = 0
SHOP_INDEX = 1
INVITED_INDEX = 2
MY_FRIEND_INDEX = 3
MY_REFERRER_INDEX = 4
SUMMON_FRIEND_INDEX = 5
TAB_MAX_COUNT = 6
INVITE_SHOP_ID = 308
AD_ICON_TEMPLATE = 'advertisement/%s.dds'

class SummonFriendNewProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonFriendNewProxy, self).__init__(uiAdapter)
        self.firstShow = True
        self.summonFriendList = []
        self.summonedFriendList = []
        self.resetData()
        self.stateMap = {0: gameStrings.TEXT_UIUTILS_1414,
         1: gameStrings.TEXT_FRIENDPROXY_293_1,
         2: gameStrings.TEXT_FRIENDPROXY_293_2,
         3: gameStrings.TEXT_FRIENDPROXY_293_3,
         4: gameStrings.TEXT_FRIENDPROXY_293_4}
        self.photoDict = {}

    def resetData(self):
        self.widget = None
        self.lastTabIndex = -1
        self.tabIndex = -1
        self.tabList = []
        self.tabMCList = []
        self.tabContentMCList = []
        self.timer = None
        self.timedShopData = {}
        self.showTabIndex = None
        self.lastSelectedFIndex = -1
        self.invitedFriendList = []
        self.inviteShopBuyCount = 1
        self.canBuyCount = 0
        self.lastInviteShopSelected = None

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initUI()

    def show(self, tabIndex = SHOP_INDEX):
        self.tabIndex = tabIndex
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMON_FRIEND_NEW)

    def clearWidget(self):
        self.resetData()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMON_FRIEND_NEW)

    def initUI(self):
        self.timer = None
        self.tabMCList = []
        self.tabContentMCList = []
        for i in range(TAB_MAX_COUNT):
            tabMC = self.widget.getChildByName('tab' + str(i))
            if i == TIMED_SHOP_INDEX:
                if self.enableActivity():
                    self.tabMCList.append(tabMC)
                    tabMC.visible = True
                else:
                    tabMC.visible = False
            elif i == MY_REFERRER_INDEX:
                if self.enableMyInvitor():
                    self.tabMCList.append(tabMC)
                    tabMC.visible = True
                else:
                    tabMC.visible = False
            else:
                self.tabMCList.append(tabMC)
            tabMC.addEventListener(events.MOUSE_CLICK, self.onTabClick, False, 0, True)
            frameMC = self.widget.getChildByName('frame%d' % i)
            self.tabContentMCList.append(frameMC)

        self.refreshTabs()
        self.widget.oldPanel.visible = False
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.onCloseClick, False, 0, True)
        self.widget.frame0.list.childItem = 'SummonFriendNew_AcitivityItem'
        self.widget.frame0.list.childWidth = 229
        self.widget.frame0.list.pageItemFunc = self.activityItemFunc
        adPageView = self.widget.frame0.advertisement
        self.widget.pageRenderFunc = self.advertisementRendFunc
        self.widget.frame1.iconScore.bonusType = 'invite'
        self.widget.frame1.count.text = str(BigWorld.player().invitePoint)
        self.widget.frame1.buyBtn.addEventListener(events.MOUSE_CLICK, self.showHelp, False, 0, True)
        self.widget.frame1.scrollList.itemRenderer = 'SummonFriendNew_Item'
        self.widget.frame1.scrollList.lableFunction = self.inviteShopLabelFun
        self.widget.frame1.scrollList.column = 3
        self.widget.frame1.scrollList.itemWidth = 242
        self.widget.frame1.scrollList.itemHeight = 148
        self.widget.frame2.confirmCopyWeb.addEventListener(events.MOUSE_CLICK, self.onCopyWebToClipBoard, False, 0, True)
        self.widget.frame3.itemList.itemRenderer = 'SummonFriendNew_PlayerItem_New'
        self.widget.frame3.itemList.lableFunction = self.lableFunPlayerIem
        self.widget.frame3.priceType0.bonusType = 'tianBi'
        self.widget.frame3.priceType1.bonusType = 'invite'
        self.widget.frame4.tab2_1.confirmBind.addEventListener(events.MOUSE_CLICK, self.onSendConfirmBind, False, 0, True)
        self.widget.frame4.tab2_1.addFriend.addEventListener(events.MOUSE_CLICK, self.onAddFriend, False, 0, True)
        self.widget.frame5.textField.text = str(SCD.data.get('INVITE_POINT_WITH_FLOWBACK_SEND_MSG', 0))
        self.widget.frame5.textField2.text = str(SCD.data.get('INVITE_POINT_WITH_FLOWBACK_SUCC', 0))
        self.widget.frame5.summonFrame.itemRenderer = 'SummonFriendNew_PlayerItem'
        self.widget.frame5.summonFrame.lableFunction = self.summonFirendLabelFun
        self.widget.frame5.summonedFrame.itemRenderer = 'SummonFriendNew_PlayerItem'
        self.widget.frame5.summonedFrame.lableFunction = self.summonedFriendLabelFun
        self.setTabIndex(self.tabIndex)

    @ui.callFilter(1, True)
    def onCopyWebToClipBoard(self, *args):
        myCode = getattr(BigWorld.player(), 'friendInviteVerifyCode', '')
        if myCode:
            if BigWorld.isPublishedVersion():
                webUrl = SCD.data.get('Summon_Friend_Web_addr', 'http://tianyu.163.com/?=%s') % myCode
            else:
                webUrl = 'http://hd-test-qc.tianyu.163.com/2015/friend?code=%s' % myCode
            BigWorld.setClipBoardText(webUrl)
            msg = uiUtils.getTextFromGMD(GMDD.data.COPY_URL_SUCCESS, gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_221)
            gameglobal.rds.ui.messageBox.showMsgBox(msg)

    def setTabIndex(self, index):
        if index == self.lastTabIndex:
            return
        self.lastTabIndex = index
        self.tabIndex = index
        for tabMC in self.tabMCList:
            if int(tabMC.data) == index:
                tabMC.selected = True
            else:
                tabMC.selected = False

        for tabContentMC in self.tabContentMCList:
            tabContentMC.visible = False

        self.tabContentMCList[index].visible = True
        if index == TIMED_SHOP_INDEX:
            self.refreshTimedShop()
        elif index == SHOP_INDEX:
            self.refreshShop()
        elif index == INVITED_INDEX:
            self.refreshInvite()
        elif index == MY_FRIEND_INDEX:
            self.refreshFriend()
        elif index == MY_REFERRER_INDEX:
            self.refreshMyReferrer()
        elif index == SUMMON_FRIEND_INDEX:
            self.refreshSummonFriend()

    def refreshTimedShop(self):
        if not self.widget:
            return
        if not self.widget.frame0:
            return
        self.widget.frame0.list.prevBtn.x = -15
        self.widget.frame0.list.nextBtn.x = 753
        adPageView = self.widget.frame0.advertisement
        data = self.getTimedShopData()
        self.widget.frame0.list.data = data['rewardInfo']
        if len(data['advertisements']) > 0:
            tmp = data['advertisements']
            adPageView.data = tmp
        self.addTimer()

    def advertisementRendFunc(self, *args):
        convertMc = ASObject(args[3][0])
        data = ASObject(args[3][1])
        if args[3][0].IsNull():
            convertMc = self.widget.getInstByClsName('SummonFriendNew_AdIcon')
        adIcon = convertMc
        adIcon.adInfo = data
        adIcon.fitSize = True
        adIcon.loadImage(data.iconPath)
        adIcon.addEventListener(events.MOUSE_CLICK, self.onAdClick, False, 0, True)

    def onAdClick(self, *args):
        self.setTabIndex(2)

    def activityItemFunc(self, *args):
        item = ASObject(args[3][0])
        data = ASObject(args[3][1])
        item.itemName.mouseEnabled = True
        item.condition.mouseEnabled = False
        item.finishLabel.mouseEnabled = False
        item.restTime.mouseEnabled = False
        item.name = str(int(data.activityId))
        item.activityId = data.activityId
        item.itemName.htmlText = data.itemName
        item.condition.htmlText = data.condition
        if data.isFinished:
            item.finishLabel.htmlText = gameStrings.TEXT_SUMMONFRIENDINVITEACTIVITY_81
        else:
            item.finishLabel.htmlText = gameStrings.TEXT_SUMMONFRIENDINVITEACTIVITY_83
        item.restTime.visible = not data.isFinished
        item.restTime.htmlText = uiUtils.formatTime(data.restTime)
        item.itemSlot.setItemSlotData(data.itemData)
        item.itemSlot.dragable = False
        item.getRewardBtn.enabled = not data.hasReward and data.reachGoal
        item.getRewardBtn.label = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_187 if data.hasReward else gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_192
        item.getRewardBtn.addEventListener(events.MOUSE_CLICK, self.onGetActivityReward, False, 0, True)

    def onGetActivityReward(self, *args):
        e = ASObject(args[3][0])
        activityID = int(e.currentTarget.parent.name)
        BigWorld.player().cell.gainFriendInvitationSummaryReward(activityID)

    def getTimedShopData(self):
        ret = {}
        rewardData = IERD.data
        friendActivityData = getattr(BigWorld.player(), 'friendInvitationSummary', {})
        ret['advertisements'] = []
        ret['rewardInfo'] = []
        now = utils.getNow()
        for key, value in rewardData.items():
            startStamp = value.get('tStart', 1442455200)
            endStamp = value.get('tEnd', 1445472000)
            if now < startStamp:
                continue
            adItems = {}
            adItems['iconPath'] = AD_ICON_TEMPLATE % value.get('adName', '3')
            ret['advertisements'].append(adItems)
            item = {}
            rewardId = value.get('rewardId', 0)
            item['activityId'] = key
            item['condition'] = value.get('conditionDesc', gameStrings.TEXT_SUMMONFRIENDINVITEACTIVITY_138)
            item['itemData'] = uiUtils.getGfxItemById(rewardId)
            item['itemName'] = uiUtils.getItemColorName(rewardId)
            item['isFinished'] = now > endStamp
            item['restTime'] = endStamp - now
            reqNum = value.get('num', 0)
            curNum = friendActivityData.get(key, [0, 0])[0]
            hasReward = friendActivityData.get(key, [0, 0])[1]
            item['reachGoal'] = reqNum <= curNum
            item['hasReward'] = hasReward
            ret['rewardInfo'].append(item)

        self.timedShopData = ret
        return ret

    def addTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None
        self.updateTimer()

    def updateTimer(self):
        if not self.widget or self.tabIndex != TIMED_SHOP_INDEX:
            self.removeTimer()
            return
        arrLen = len(self.timedShopData['rewardInfo'])
        for i in range(arrLen):
            tempData = self.timedShopData['rewardInfo'][i]
            tempData['restTime'] -= 1
            item = self.widget.frame0.list.canvas.getChildByName(str(tempData['activityId']))
            if tempData['restTime'] > 0:
                if item:
                    item.restTime.htmlText = uiUtils.formatTime(tempData['restTime'])
            elif item:
                item.finishLabel.htmlText = gameStrings.TEXT_SUMMONFRIENDINVITEACTIVITY_81
                item.restTime.visible = False

        self.timer = BigWorld.callback(1, self.updateTimer)

    def removeTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    @ui.uiEvent(uiConst.WIDGET_SUMMON_FRIEND_NEW, events.EVENT_INVITE_POINT_CHANGE)
    def refreshShop(self):
        if not self.widget or self.tabIndex != SHOP_INDEX:
            return
        else:
            self.lastInviteShopSelected = None
            self.widget.frame1.count.text = str(BigWorld.player().invitePoint)
            itemList = self.getInviteShopItemList()
            self.widget.frame1.scrollList.dataArray = itemList
            return

    def getInviteShopItemList(self):
        itemList = []
        list0 = CSISD.data.get(INVITE_SHOP_ID, [])
        for value in list0:
            compositeId = value.get('compositeId', 0)
            cfgData = CSTD.data.get(compositeId, {})
            itemId = cfgData.get('itemId', 0)
            itemInfo = uiUtils.getGfxItemById(itemId)
            itemInfo['tag'] = cfgData.get('tag', '')
            itemInfo['itemName'] = uiUtils.getItemColorName(itemId)
            itemInfo['invitePoint'] = cfgData.get('consumeInvitePoint', 1)
            itemInfo['buyLimitType'] = cfgData.get('buyLimitType', 0)
            itemInfo['buyLimitCount'] = cfgData.get('buyLimitCount', 0)
            itemInfo['compositeId'] = compositeId
            itemList.append(itemInfo)

        return itemList

    def inviteShopLabelFun(self, *args):
        data = ASObject(args[3][0])
        mc = ASObject(args[3][1])
        mc.name = str(int(data.compositeId))
        mc.selBg.visible = False
        mc.selBg.mouseEnabled = False
        mc.addEventListener(events.MOUSE_ROLL_OVER, self.onItemRollOver, False, 0, True)
        mc.addEventListener(events.MOUSE_ROLL_OUT, self.onItemRollOut, False, 0, True)
        mc.addEventListener(events.MOUSE_CLICK, self.onInviteShopItemClick, True, 0, True)
        if data.tag == '':
            mc.basicBox.itemLabel.visible = False
        elif data.tag == 'new':
            mc.basicBox.itemLabel.gotoAndStop('new')
        elif data.tag == 'hot':
            mc.basicBox.itemLabel.gotoAndStop('hot')
        mc.basicBox.itemSlot.setItemSlotData(data)
        mc.basicBox.itemSlot.dragable = False
        mc.basicBox.priceValue.textField.text = str(int(data.invitePoint))
        mc.basicBox.itemName.nameText.htmlText = data.itemName

    def onInviteShopItemClick(self, *args):
        e = ASObject(args[3][0])
        if self.lastInviteShopSelected:
            self.lastInviteShopSelected.selBg.visible = False
            if self.lastInviteShopSelected.name != e.currentTarget.name:
                self.inviteShopBuyCount = 1
        e.currentTarget.selBg.visible = True
        self.lastInviteShopSelected = e.currentTarget

    def onItemRollOver(self, *args):
        e = ASObject(args[3][0])
        mc = e.currentTarget
        mc.gotoAndStop('over')
        mc.overBg.mouseEnabled = False
        mc.overBg.visible = False
        compositeId = int(mc.name)
        cfgInfo = CSTD.data.get(compositeId, {})
        if not cfgInfo:
            return
        invitePoint = cfgInfo.get('consumeInvitePoint', 0)
        self.canBuyCount = BigWorld.player().invitePoint / invitePoint
        mc.counter.minCount = 0
        mc.counter.maxCount = max(1, self.canBuyCount)
        if self.lastInviteShopSelected:
            if e.currentTarget.name != self.lastInviteShopSelected.name:
                mc.counter.count = 1
            else:
                mc.counter.count = self.inviteShopBuyCount
        else:
            mc.counter.count = 1
        mc.counter.addEventListener(events.EVENT_COUNT_CHANGE, self.inviteShopCountChange, False, 0, True)
        mc.buyBtn.addEventListener(events.MOUSE_CLICK, self.buyInviteShopItem, False, 0, True)

    def getCompositeRemainBuyCount(self, compositeId):
        p = BigWorld.player()
        dataKey = self._getCompositeItemLimitKey(compositeId)
        if dataKey not in p.compositeShopItemBuyLimit:
            buyCount = 0
            lastBuyTime = 0
        else:
            buyCount, lastBuyTime = p.compositeShopItemBuyLimit[dataKey]
        buyLimitType = CSTD.data.get(compositeId, {}).get('buyLimitType', 0)
        buyLimitCount = CSTD.data.get(compositeId, {}).get('buyLimitCount', -1)
        if lastBuyTime:
            samePeriod = False
            now = utils.getNow()
            if buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_DAY:
                samePeriod = utils.isSameDay(lastBuyTime, now)
            elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_WEEK:
                samePeriod = utils.isSameWeek(lastBuyTime, now)
            elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_MONTH:
                samePeriod = utils.isSameMonth(lastBuyTime, now)
            elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_FOREVER:
                samePeriod = True
            if not samePeriod:
                buyCount = 0
        return buyLimitCount - buyCount

    def _getLimitStr(self, compositeId):
        ret = ''
        buyLimitType = CSTD.data.get(compositeId, {}).get('buyLimitType', 0)
        buyLimitCount = CSTD.data.get(compositeId, {}).get('buyLimitCount', -1)
        if buyLimitType != const.COMPOSITE_BUY_LIMIT_TYPE_NO:
            remainBuyCount = max(0, self.getCompositeRemainBuyCount(compositeId))
            if remainBuyCount <= 0:
                remainBuyCountStr = uiUtils.toHtml(str(remainBuyCount), '#F43804')
            else:
                remainBuyCountStr = str(remainBuyCount)
            if buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_DAY:
                ret = gameStrings.TEXT_COMPOSITESHOPPROXY_530 % (remainBuyCountStr, buyLimitCount)
            elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_WEEK:
                ret = gameStrings.TEXT_COMPOSITESHOPPROXY_532 % (remainBuyCountStr, buyLimitCount)
            elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_MONTH:
                ret = gameStrings.TEXT_COMPOSITESHOPPROXY_534 % (remainBuyCountStr, buyLimitCount)
            elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_FOREVER:
                ret = gameStrings.TEXT_COMPOSITESHOPPROXY_536 % (remainBuyCountStr, buyLimitCount)
        return ret

    def _getCompositeItemLimitKey(self, compositeId):
        compositeData = CSTD.data[compositeId]
        if 'buyLimitGroup' in compositeData:
            return 'g%d' % (compositeData['buyLimitGroup'],)
        else:
            return 'i%d' % (compositeId,)

    def inviteShopCountChange(self, *args):
        e = ASObject(args[3][0])
        if self.lastInviteShopSelected:
            if self.lastInviteShopSelected.name == e.currentTarget.parent.name:
                self.inviteShopBuyCount = int(e.currentTarget.count)

    def buyInviteShopItem(self, *args):
        e = ASObject(args[3][0])
        counter = e.currentTarget.parent.counter
        self.inviteShopBuyCount = int(counter.count)
        if self.inviteShopBuyCount == 0:
            if self.canBuyCount == 0:
                BigWorld.player().showGameMsg(GMDD.data.INVITE_POINT_NOT_ENOUGH, ())
            counter.count = 1
        if self.inviteShopBuyCount > self.canBuyCount:
            BigWorld.player().showGameMsg(GMDD.data.INVITE_POINT_NOT_ENOUGH, ())
            return
        compositeId = int(e.currentTarget.parent.name)
        cfgData = CSTD.data.get(compositeId, {})
        if not cfgData:
            return
        canBuyCount = self.getCompositeRemainBuyCount(compositeId)
        itemId = cfgData.get('itemId', 0)
        itemInfo = uiUtils.getGfxItemById(itemId)
        if self.inviteShopBuyCount > canBuyCount:
            msg = self._getLimitStr(compositeId)
            gameglobal.rds.ui.messageBox.showMsgBox(msg)
            return
        frameInfo = {}
        itemInfo['itemId'] = cfgData.get('itemId', 0)
        itemInfo['price'] = cfgData.get('consumeInvitePoint', 0)
        itemInfo['count'] = self.inviteShopBuyCount
        itemInfo['bonusType'] = 'invite'
        frameInfo['itemInfo'] = itemInfo
        yesFun = Functor(self.yesFun, compositeId, self.inviteShopBuyCount)
        frameInfo['yesFun'] = yesFun
        frameInfo['yesLabel'] = gameStrings.TEXT_SUMMONFRIENDNEWPROXY_502
        frameInfo['noLabel'] = gameStrings.TEXT_PLAYRECOMMPROXY_494_1
        gameglobal.rds.ui.itemBuyConfirm.show(frameInfo)

    def yesFun(self, id, count):
        BigWorld.player().cell.buyItemWithInvitePoint(id, count)

    def onItemRollOut(self, *args):
        e = ASObject(args[3][0])
        mc = e.currentTarget
        mc.gotoAndStop('normal')

    def refreshInvite(self):
        if not self.widget:
            return
        if self.tabIndex != INVITED_INDEX:
            return
        if SCD.data.get('friendInviterLv', 40) > BigWorld.player().lv:
            BigWorld.player().showGameMsg(GMDD.data.INVITE_FRIEND_LV_WRONG, ())
            self.setTabIndex(SHOP_INDEX)
            return
        if not getattr(BigWorld.player(), 'friendInviteVerifyCode', ''):
            BigWorld.player().cell.genFriendInviteVerifyCode()
            return
        data = self.getIWantSummonData()
        self.widget.frame2.ruleWeb.htmlText = data['webRule']
        self.widget.frame2.qrCodeRule.htmlText = data['QRRule']
        self.widget.frame2.qrcode.fitSize = True
        self.widget.frame2.qrcode.loadImageByBase64(data['QRCode'])

    def getIWantSummonData(self):
        data = {}
        data['webRule'] = uiUtils.getTextFromGMD(GMDD.data.WEB_SUMMON_RULE, gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_195)
        data['myCode'] = getattr(BigWorld.player(), 'friendInviteVerifyCode', '')
        data['webUrl'] = SCD.data.get('Summon_Friend_Web_addr', 'http://tianyu.163.com/?=%s') % data['myCode']
        data['qrUrl'] = SCD.data.get('Summon_Friend_QR_addr', 'http://tianyu.163.com/?=%s') % data['myCode']
        data['QRRule'] = uiUtils.getTextFromGMD(GMDD.data.QR_SUMMON_RULE, gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_199)
        codeMaker = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=2, border=1)
        codeMaker.add_data(data['qrUrl'])
        codeMaker.make(fit=True)
        img = codeMaker.make_image()
        pngUrl = img.convert('RGB').tostring('jpeg', 'RGB', 90)
        data['QRCode'] = base64.encodestring(pngUrl)
        return data

    def refreshFriend(self):
        if not self.widget or self.tabIndex != MY_FRIEND_INDEX:
            return
        self.lastSelectedFIndex = -1
        playerData = self.getSummedPlayersData()
        self.refreshSummedPlyaers(playerData)

    def refreshSummedPlyaers(self, playersData):
        self.widget.frame3.total.text = '%d/%d' % (playersData['onlineCount'], playersData['totalCount'])
        plyerList = playersData['playerList']
        if len(plyerList) > 0:
            if self.lastSelectedFIndex == -1:
                self.lastSelectedFIndex = plyerList[0]['index']
        else:
            self.selectedFriendFun(None)
        self.widget.frame3.itemList.dataArray = plyerList

    def getSummedPlayersData(self):
        data = {}
        list = []
        onlineCount = 0
        totalCount = 0
        p = BigWorld.player()
        for fid in p.friendInviteInfo:
            if p.friendInviteInfo[fid].get('status') == gametypes.FRIEND_INVITE_STATUS_BUILD or p.friendInviteInfo[fid].get('status') == gametypes.FRIEND_INVITE_STATUS_ROLE_DROP and fid in p.friendInvitees:
                friendInfo = self.getFriendInfo(fid)
                friendInfo['index'] = totalCount
                if friendInfo['state'] in (1, 2, 3):
                    onlineCount += 1
                totalCount += 1
                list.append(friendInfo)

        self.invitedFriendList = list[:]
        list.sort(cmp=self.cmpFriend)
        data['playerList'] = list
        data['onlineCount'] = onlineCount
        data['totalCount'] = totalCount
        return data

    def cmpFriend(self, x, y):
        p = BigWorld.player()
        xFid = int(x['fid'])
        yFid = int(y['fid'])
        xLv = p.friendInviteInfo[xFid].get('lv', 1)
        yLv = p.friendInviteInfo[yFid].get('lv', 1)
        xNums = self.getCanGetRewardNums(xFid)
        yNums = self.getCanGetRewardNums(yFid)
        onLineCmp = cmp(p.friendInviteInfo[yFid].get('on', False), p.friendInviteInfo[xFid].get('on', False))
        if onLineCmp == 0:
            numsCmp = cmp(yNums, xNums)
            if numsCmp == 0:
                lvCmp = cmp(yLv, xLv)
                return lvCmp
            else:
                return numsCmp
        else:
            return onLineCmp
        return 0

    def getCanGetRewardNums(self, fid):
        rewardData = self.getRewardData(fid)
        reward = rewardData['lvPercent'] + rewardData['combatScorePercent']
        return reward

    def lableFunPlayerIem(self, *args):
        data = ASObject(args[3][0])
        item = ASObject(args[3][1])
        item.nameText.htmlText = data.name
        item.name = str(int(data.index))
        item.isOnLine.htmlText = data.stateName
        item.combatScore.htmlText = data.school
        item.lvAndSchool.htmlText = data.Lv
        item.selected = False
        item.enabled = True
        item.playerHead.playerIcon.icon.fitSize = True
        item.playerHead.playerIcon.icon.loadImage(data.photo)
        item.playerHead.gotoAndStop('stop')
        if data.state != 0:
            item.playerHead.playerIcon.gotoAndStop('normal')
        else:
            item.playerHead.playerIcon.gotoAndStop('gray')
        item.playerHead.status.gotoAndStop(data.stateName2)
        item.addEventListener(events.MOUSE_CLICK, self.onSelectFriendClick, False, 0, True)
        if self.lastSelectedFIndex >= 0:
            if int(data.index) == int(self.lastSelectedFIndex):
                item.selected = True
                item.enabled = False
                self.selectedFriendFun(item)

    def onSelectFriendClick(self, *args):
        e = ASObject(args[3][0])
        self.selectedFriendFun(e.currentTarget)

    def selectedFriendFun(self, newMC):
        fid = 0
        if self.lastSelectedFIndex >= 0:
            lastMC = self.widget.frame3.itemList.canvas.getChildByName('%d' % self.lastSelectedFIndex)
            if lastMC:
                lastMC.selected = False
                lastMC.enabled = True
        if newMC:
            newMC.selected = True
            newMC.enabled = False
            self.lastSelectedFIndex = int(newMC.name)
            index = int(newMC.name)
            fid = self.invitedFriendList[index]['fid']
        self.refreshRewardView(fid)

    def refreshRewardView(self, fid):
        rewardData = self.getRewardData(fid)
        friendInfo = self.getFriendInfo(fid)
        frame = self.widget.frame3
        frame.headIcon.icon.fitSize = True
        frame.headIcon.icon.loadImage(friendInfo['photo'])
        frame.nameText.htmlText = friendInfo['name']
        frame.headIcon.status.gotoAndStop(friendInfo['stateName2'])
        ASUtils.setMcEffect(frame.headIcon, 'gray')
        frame.txtCost.visible = False
        frame.priceType0.visible = False
        frame.txtDesc0.visible = False
        frame.txtGained.visible = False
        frame.priceType1.visible = False
        frame.txtDesc1.visible = False
        if friendInfo['state'] == 0:
            ASUtils.setMcEffect(frame.headIcon, 'gray')
        else:
            ASUtils.setMcEffect(frame.headIcon)
        frame.txtCost.text = rewardData['tianBi']
        frame.txtGained.text = rewardData['invitePoint']
        frame.awardList.canvas.lvProgress.currentValue = rewardData['lvPercent'] * 100
        frame.awardList.canvas.scroeProgress.currentValue = rewardData['combatScorePercent'] * 100
        for i in range(len(rewardData['lvRewardList'])):
            lvRewardData = rewardData['lvRewardList'][i]
            item = frame.awardList.canvas.getChildByName('item%d' % i)
            combatRewardData = rewardData['combatScoreRewardList'][i]
            item.txtLv.text = 'LV.%d' % lvRewardData['needLv']
            item.txtCombatScore.text = combatRewardData['needCombatScore']
            item.txtLvReward.text = lvRewardData['rewardScore']
            item.priceType0.bonusType = 'invite'
            item.priceType1.bonusType = 'invite'
            if lvRewardData['done']:
                item.lvRule.htmlText = uiUtils.toHtml(gameStrings.TEXT_SUMMONFRIENDINVITEFRIEND_146, '#FFFFE5')
                item.txtLvReward.htmlText = uiUtils.toHtml(str(lvRewardData['rewardScore']), '#FFFFE5')
            else:
                item.lvRule.htmlText = uiUtils.toHtml(gameStrings.TEXT_SUMMONFRIENDINVITEFRIEND_146, '#CC2929')
                item.txtLvReward.htmlText = uiUtils.toHtml(str(lvRewardData['rewardScore']), '#CC2929')
            if combatRewardData['done']:
                item.txtRule2.htmlText = uiUtils.toHtml(gameStrings.TEXT_SUMMONFRIENDINVITEFRIEND_146, '#FFFFE5')
                item.txtCombatScoreReward.htmlText = uiUtils.toHtml(str(combatRewardData['rewardScore']), '#FFFFE5')
            else:
                item.txtRule2.htmlText = uiUtils.toHtml(gameStrings.TEXT_SUMMONFRIENDINVITEFRIEND_146, '#CC2929')
                item.txtCombatScoreReward.htmlText = uiUtils.toHtml(str(combatRewardData['rewardScore']), '#CC2929')

    def getRewardData(self, fid):
        rewardData = {}
        lvRewardList = []
        combatRewardList = []
        p = BigWorld.player()
        friendInfo = p.friendInviteInfo.get(fid, {})
        inviteFriendConsumeRecord = getattr(p, 'inviteFriendConsumeRecord', {})
        tianBi = inviteFriendConsumeRecord.get(fid, 0)
        factor = SCD.data.get('COIN_2_INVITE_POINT_RATIO', 0)
        invitePoint = int(tianBi * factor)
        inviteReward = p.friendInviteRewards.get(fid, {})
        lvDoneCount = 0
        combatDoneCount = 0
        for key, data in FIRD.data.iteritems():
            if data.has_key('lv'):
                lvRewardData = {}
                lvRewardData['rewardScore'] = data.get('invitePoint', 0)
                needLv = data.get('lv', 0)
                lvRewardData['needLv'] = needLv
                done = friendInfo.get('lv', 1) >= needLv
                lvRewardData['done'] = done
                lvRewardList.append(lvRewardData)
                if done:
                    lvDoneCount += 1
            if data.has_key('needCombatScore'):
                scoreRewardData = {}
                needCombatScore = data.get('needCombatScore', 0)
                scoreRewardData['needCombatScore'] = needCombatScore
                scoreRewardData['rewardScore'] = data.get('invitePoint', 0)
                done = inviteReward.has_key(key)
                scoreRewardData['done'] = done
                if done:
                    combatDoneCount += 1
                combatRewardList.append(scoreRewardData)

        lvRewardList.sort(key=lambda x: x['needLv'], reverse=True)
        combatRewardList.sort(key=lambda x: x['needCombatScore'], reverse=True)
        rewardData['lvPercent'] = lvDoneCount / (len(lvRewardList) * 1.0)
        rewardData['combatScorePercent'] = combatDoneCount / (len(combatRewardList) * 1.0)
        rewardData['lvRewardList'] = lvRewardList
        rewardData['combatScoreRewardList'] = combatRewardList
        rewardData['tianBi'] = tianBi
        rewardData['invitePoint'] = invitePoint
        return rewardData

    def getFriendInfo(self, fid):
        p = BigWorld.player()
        friendInfo = {}
        friendInfo['fid'] = fid
        inviteInfo = p.friendInviteInfo.get(fid, {})
        friendInfo['name'] = utils.getDisplayName(inviteInfo.get('playerName', ''))
        stateMap = {0: gameStrings.TEXT_UIUTILS_1414,
         1: gameStrings.TEXT_FRIENDPROXY_293_1,
         2: gameStrings.TEXT_FRIENDPROXY_293_2,
         3: gameStrings.TEXT_FRIENDPROXY_293_3,
         4: gameStrings.TEXT_FRIENDPROXY_293_4}
        stateMap2 = {0: 'online',
         1: 'online',
         2: 'busy',
         3: 'leave',
         4: 'hide'}
        if inviteInfo.get('on', ''):
            friendInfo['state'] = 1
        else:
            friendInfo['state'] = 0
        friendInfo['stateName'] = stateMap[friendInfo['state']]
        if inviteInfo.get('status', 0) == gametypes.FRIEND_INVITE_STATUS_ROLE_DROP:
            friendInfo['stateName'] = gameStrings.TEXT_SUMMONFRIENDINVITEFRIEND_299
        friendInfo['stateName2'] = stateMap2[friendInfo['state']]
        friendInfo['combatScore'] = 0
        school = inviteInfo.get('school', 3)
        schoolName = SD.data.get(school, {}).get('name', '')
        lv = inviteInfo.get('lv', 1)
        friendInfo['school'] = schoolName
        friendInfo['Lv'] = 'Lv.%d' % lv
        sex = inviteInfo.get('sex', 1)
        if inviteInfo.get('profileIcon', ''):
            photo = inviteInfo.get('profileIcon', '')
        else:
            photo = 'headIcon/%s.dds' % str(school * 10 + sex)
        if uiUtils.isDownloadImage(photo):
            if self.photoDict.has_key(fid):
                photo = self.photoDict[fid]
            else:
                p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, self.onDownloadOtherPhoto, (friendInfo.get('fid', 0), photo))
                photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
        friendInfo['photo'] = photo
        return friendInfo

    def onDownloadOtherPhoto(self, status, fid, photoName):
        photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photoName + '.dds'
        self.photoDict[fid] = photo
        self.refreshWidget()

    def refreshMyReferrer(self):
        if not self.widget or self.tabIndex != MY_REFERRER_INDEX:
            return
        else:
            data = self.getMyReferrerData()
            self.setInvited(data['invited'])
            frame = self.widget.frame4
            frame.tab2_1.nameText.visible = data['showContent']
            frame.tab2_1.onLine.visible = data['showContent']
            frame.tab2_1.lvAndSchool.visible = data['showContent']
            frame.tab2_1.headIcon.visible = data['showContent']
            frame.tab2_1.confirmBind.visible = data['showContent']
            frame.tab2_1.addFriend.visible = data['showContent']
            friendInfo = data.get('friendInfo', None)
            if friendInfo:
                frame.tab2_1.headIcon.tag = friendInfo['fid']
                frame.tab2_1.headIcon.icon.fitSize = True
                frame.tab2_1.headIcon.icon.loadImage(friendInfo['photo'])
                frame.tab2_1.headIcon.status.gotoAndStop(friendInfo['stateName2'])
                if friendInfo['state'] == 0:
                    ASUtils.setMcEffect(frame.tab2_1.headIcon, 'gray')
                else:
                    ASUtils.setMcEffect(frame.tab2_1.headIcon)
                frame.tab2_1.nameText.htmlText = friendInfo['name']
                frame.tab2_1.onLine.htmlText = friendInfo['stateName']
                frame.tab2_1.lvAndSchool.htmlText = friendInfo['school'] + '  ' + friendInfo['Lv']
            else:
                frame.tab2_1.nameText.visible = False
                frame.tab2_1.onLine.visible = False
                frame.tab2_1.lvAndSchool.visible = False
                frame.tab2_1.headIcon.visible = False
            frame.tab2_1.confirmBind.enabled = not data['hasBinded']
            frame.tab2_1.addFriend.enabled = data['addFriend']
            frame.tab2_1.bindhint.htmlText = data['friendInfoHint']
            if not friendInfo:
                frame.tab2_1.confirmBind.enabled = False
                frame.tab2_1.addFriend.enabled = False
            return

    def getMyReferrerData(self):
        p = BigWorld.player()
        hasOtherInvited = False
        data = {}
        if BigWorld.player().friendInviterGbId:
            data['hasBinded'] = True
        else:
            data['hasBinded'] = False
        inviteId = 0
        hasDeleted = False
        if BigWorld.player().friendInviterGbId:
            inviteId = p.friendInviterGbId
            if p.friendInviteInfo.get(inviteId, {}).get('status', gametypes.FRIEND_INVITE_STATUS_ROLE_DROP) == gametypes.FRIEND_INVITE_STATUS_ROLE_DROP:
                hasDeleted = True
                inviteId = 0
        else:
            for fid in p.friendInviteInfo:
                if p.friendInviteInfo[fid]['status'] == gametypes.FRIEND_INVITE_STATUS_PRE_INVITER:
                    inviteId = fid
                    break
                if p.friendInviteInfo[fid]['status'] == gametypes.FRIEND_INVITE_STATUS_ROLE_DROP:
                    if fid not in p.friendInvitees:
                        inviteId = 0
                        hasDeleted = True

        if inviteId:
            data['friendInfo'] = self.getFriendInfo(inviteId)
            if BigWorld.player().friend.get(inviteId):
                data['addFriend'] = False
            else:
                data['addFriend'] = True
        else:
            data['addFriend'] = True
        if not data['hasBinded']:
            if inviteId and not hasDeleted:
                msg = uiUtils.getTextFromGMD(GMDD.data.BIND_HINT, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_138)
                msg = msg % data['friendInfo']['name']
                data['friendInfoHint'] = msg
            else:
                msg = uiUtils.getTextFromGMD(GMDD.data.NOT_INVITE_HINT, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_142)
                data['friendInfoHint'] = msg
        elif not hasDeleted:
            msg = uiUtils.getTextFromGMD(GMDD.data.BIND_OK_HINT, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_146)
            msg = msg % data['friendInfo']['name']
            data['friendInfoHint'] = msg
        data['showContent'] = True
        if BigWorld.player().lv > SCD.data.get('friendInviteeLv') and not BigWorld.player().friendInviterGbId:
            data['hasBinded'] = True
            msg = uiUtils.getTextFromGMD(GMDD.data.BIND_FAILED_HINT_LV, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_152)
            data['friendInfoHint'] = msg
            data['showContent'] = False
        if hasDeleted == True:
            msg = uiUtils.getTextFromGMD(GMDD.data.INVITER_FRIEND_DELETE, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_156)
            data['friendInfoHint'] = msg
            data['showContent'] = False
        data['invited'] = hasOtherInvited
        return data

    def onSendConfirmBind(self, *args):
        p = BigWorld.player()
        if not p.friendInviterGbId:
            inviteId = 0
            for fid in p.friendInviteInfo:
                if p.friendInviteInfo[fid].get('status') == gametypes.FRIEND_INVITE_STATUS_PRE_INVITER:
                    inviteId = fid
                    break

            if inviteId:
                BigWorld.player().base.invitedFriendByGbId(inviteId)
            else:
                return

    @ui.callFilter(1, True)
    def onAddFriend(self, *args):
        p = BigWorld.player()
        inviteId = 0
        if p.friendInviterGbId:
            inviteId = p.friendInviterGbId
        else:
            for fid in p.friendInviteInfo:
                if p.friendInviteInfo[fid].get('status') == gametypes.FRIEND_INVITE_STATUS_PRE_INVITER:
                    inviteId = fid
                    break

        if inviteId:
            name = p.friendInviteInfo[inviteId].get('playerName', '')
            p.base.addContact(name, gametypes.FRIEND_GROUP_FRIEND, const.FRIEND_SRC_SUMMON)

    def setInvited(self, hadInvited):
        self.widget.frame4.tab2_2.visible = hadInvited
        self.widget.frame4.tab2_1.visible = not hadInvited

    def refreshSummonFriend(self):
        if not self.widget or self.tabIndex != SUMMON_FRIEND_INDEX:
            return
        self.summonFriendList = self.friendListFilter(self.summonFriendList)
        self.summonedFriendList = self.friendListFilter(self.summonedFriendList)
        self.widget.frame5.summonFrame.dataArray = range(len(self.summonFriendList))
        self.widget.frame5.summonFrame.validateNow()
        self.widget.frame5.summonedFrame.dataArray = range(len(self.summonedFriendList))
        self.widget.frame5.summonedFrame.validateNow()
        self.widget.frame5.onLineCount.text = '%d/%d' % (self.getOnLineCount(self.summonedFriendList), len(self.summonedFriendList))

    def getSummonedFirendOnLineInfo(self):
        onLineCount = 0
        for id in self.summonedFriendList:
            if self.isOnLine(id):
                onLineCount += 1

        return onLineCount

    def summonFirendLabelFun(self, *args):
        index = int(args[3][0].GetNumber())
        id = self.summonFriendList[index]
        mc = ASObject(args[3][1])
        friendInfo = BigWorld.player().friend.get(id, None)
        if not friendInfo:
            return
        else:
            mc.isOnLine.visible = False
            mc.name = str(index)
            mc.ruleIcon.fitSize = True
            photo = 'headIcon/%s.dds' % str(friendInfo.school * 10 + friendInfo.sex)
            mc.ruleIcon.loadImage(photo)
            mc.txtName.text = friendInfo.name
            mc.txtSchool.text = SD.data[friendInfo.school]['name']
            mc.txtLv.text = 'LV.%d' % friendInfo.level
            mc.chatBtn.label = gameStrings.TEXT_SUMMONFRIENDBACKV2PROXY_222
            mc.chatBtn.removeEventListener(events.MOUSE_CLICK, self.onChatClick)
            mc.chatBtn.addEventListener(events.MOUSE_CLICK, self.onCallBackClick, False, 0, True)
            return

    def onCallBackClick(self, *args):
        e = ASObject(args[3][0])
        index = int(e.currentTarget.parent.name)
        fid = self.summonFriendList[index]
        gameglobal.rds.ui.callFriend.show(fid)

    def summonedFriendLabelFun(self, *args):
        index = int(args[3][0].GetNumber())
        id = self.summonedFriendList[index]
        mc = ASObject(args[3][1])
        friendInfo = BigWorld.player().getFValByGbId(id)
        stateName = self.stateMap[friendInfo.state]
        mc.isOnLine.visible = True
        mc.isOnLine.text = stateName
        mc.name = str(index)
        mc.ruleIcon.fitSize = True
        photo = 'headIcon/%s.dds' % str(friendInfo.school * 10 + friendInfo.sex)
        mc.ruleIcon.loadImage(photo)
        mc.txtName.text = friendInfo.name
        mc.txtSchool.text = SD.data[friendInfo.school]['name']
        mc.txtLv.text = 'LV.%d' % friendInfo.level
        mc.chatBtn.label = gameStrings.TEXT_GAMECONST_116
        mc.chatBtn.removeEventListener(events.MOUSE_CLICK, self.onCallBackClick)
        mc.chatBtn.addEventListener(events.MOUSE_CLICK, self.onChatClick, False, 0, True)

    def onChatClick(self, *args):
        e = ASObject(args[3][0])
        index = int(e.currentTarget.parent.name)
        fid = self.summonedFriendList[index]
        gameglobal.rds.ui.friend.beginChat(fid)

    def onOldPanelClick(self, *args):
        gameglobal.rds.ui.summonFriend.show()

    def onCloseClick(self, *args):
        self.hide()

    def onTabClick(self, *args):
        e = ASObject(args[3][0])
        self.setTabIndex(int(e.currentTarget.data))

    def enableActivity(self):
        enable = gameglobal.rds.configData.get('enableFriendInviteActivity', False)
        return enable

    def enableMyInvitor(self, *arg):
        playerLv = BigWorld.player().lv
        limitLv = SCD.data.get('summonFriendInvitedLimitLv', 20)
        return playerLv <= limitLv

    def refreshTabs(self):
        self.tabList = []
        if self.enableActivity():
            self.tabList.append((TIMED_SHOP_INDEX, gameStrings.TEXT_SUMMONFRIENDNEWPROXY_1036))
        self.tabList.append((SHOP_INDEX, gameStrings.TEXT_SUMMONFRIENDNEWPROXY_1037))
        self.tabList.append((INVITED_INDEX, gameStrings.TEXT_SUMMONFRIENDNEWPROXY_1038))
        self.tabList.append((MY_FRIEND_INDEX, gameStrings.TEXT_SUMMONFRIENDNEWPROXY_1039))
        if self.enableMyInvitor():
            self.tabList.append((MY_REFERRER_INDEX, gameStrings.TEXT_SUMMONFRIENDNEWPROXY_1041))
        self.tabList.append((SUMMON_FRIEND_INDEX, gameStrings.TEXT_SUMMONFRIENDNEWPROXY_1042))
        tabCount = len(self.tabList)
        for i in range(tabCount):
            tabMC = self.tabMCList[i]
            tabMC.x = 53 + 107 * i
            tabMC.y = 76
            tabMC.label = self.tabList[i][1]
            tabMC.data = self.tabList[i][0]
            tabMC.focusable = False

    def showMessageBox(self):
        if not gameglobal.rds.configData.get('enableInvitePoint', False):
            gameglobal.rds.ui.summonFriend.showMessageBox()
            return
        if self.firstShow:
            self.firstShow = False
        else:
            return
        p = BigWorld.player()
        inviteId = 0
        summedData = self.getSummedPlayersData()
        canShow = True
        if BigWorld.player().lv > SCD.data.get('friendInviteeLv') or summedData.get('totalCount', 0) > 0:
            canShow = False
        if canShow:
            for fid in p.friendInviteInfo:
                if p.friendInviteInfo[fid].get('status') == gametypes.FRIEND_INVITE_STATUS_PRE_INVITER:
                    inviteId = fid

            if not inviteId:
                return
            MBButton = messageBoxProxy.MBButton
            title = uiUtils.getTextFromGMD(GMDD.data.BIND_HINT_TITLE, gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_252)
            msg = uiUtils.getTextFromGMD(GMDD.data.BIND_HINT_MESSAGEBOX, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_138) % p.friendInviteInfo[inviteId].get('playerName', '')
            buttons = [MBButton(gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_254, Functor(self.sendConfirmBind, ''), fastKey=keys.KEY_Y), MBButton(gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_254_1, fastKey=keys.KEY_N), MBButton(gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_254_2, self.onKnowSummon)]
            gameglobal.rds.ui.messageBox.show(True, title, msg, buttons)

    def onKnowSummon(self):
        self.show(tabIndex=MY_REFERRER_INDEX)

    def sendConfirmBind(self, code):
        p = BigWorld.player()
        if not code:
            if not p.friendInviterGbId:
                inviteId = 0
                for fid in p.friendInviteInfo:
                    if p.friendInviteInfo[fid].get('status') == gametypes.FRIEND_INVITE_STATUS_PRE_INVITER:
                        inviteId = fid
                        break

                if inviteId:
                    BigWorld.player().base.invitedFriendByGbId(inviteId)
            else:
                return
        BigWorld.player().base.invitedFriendByVerifyCode(code)

    def refreshWidget(self):
        self.refreshTimedShop()
        self.refreshShop()
        self.refreshSummonFriend()
        self.refreshFriend()
        self.refreshInvite()
        self.refreshMyReferrer()

    def setSummonFriendList(self, summonFriendList):
        self.summonFriendList = self.removeKuaFuFriend(summonFriendList)
        self.refreshSummonFriend()

    def removeKuaFuFriend(self, friendList):
        list = []
        p = BigWorld.player()
        for id in friendList:
            if not p.isGobalFirendGbId(id):
                list.append(id)

        return list

    def setSummonedFriendList(self, summonedFriendList):
        self.summonedFriendList = summonedFriendList
        self.refreshSummonFriend()

    def refreshCallFriendsList(self, inviteList):
        self.summonFriendList = self.removeKuaFuFriend(inviteList)
        self.refreshSummonFriend()

    def getOnLineCount(self, list):
        count = 0
        for fid in self.summonedFriendList:
            friendInfo = BigWorld.player().getFValByGbId(fid)
            if friendInfo.state == gametypes.FRIEND_STATE_ONLINE:
                count += 1

        return count

    def isDeleted(self, fid):
        friendInfo = BigWorld.player().getFValByGbId(fid)
        if friendInfo:
            return False
        else:
            return True

    def isOnLine(self, fid):
        friendInfo = BigWorld.player().getFValByGbId(fid)
        if not friendInfo:
            return False
        return friendInfo.state == gametypes.FRIEND_STATE_ONLINE

    def friendListFilter(self, list):
        list = [ element for element in list if not self.isDeleted(element) ]
        return list

    def showHelp(self, *args):
        gameglobal.rds.ui.showHelpByKey(304)
