#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/welfareAppVipProxy.o
from gamestrings import gameStrings
import BigWorld
import utils
import time
import const
import clientUtils
import events
import gameglobal
import gametypes
import commNewServerActivity
from guis import uiConst
from uiProxy import UIProxy
from asObject import ASObject
from guis import uiUtils
from guis import messageBoxProxy
from gamestrings import gameStrings
from helpers import remoteInterface
from callbackHelper import Functor
from guis import neteaseAppVipHelper
from data import netease_membership_config_data as NMCD
from guis import tianyuMallProxy
from cdata import game_msg_def_data as GMDD
DEFAULT_VIP_ACTIVATEINFO = [(gameStrings.TEXT_WELFAREAPPVIPPROXY_26,
  '',
  False,
  328),
 (gameStrings.TEXT_WELFAREAPPVIPPROXY_26,
  gameStrings.TEXT_WELFAREAPPVIPPROXY_27,
  False,
  98),
 (gameStrings.TEXT_WELFAREAPPVIPPROXY_28,
  gameStrings.TEXT_WELFAREAPPVIPPROXY_28_1,
  True,
  898),
 (gameStrings.TEXT_WELFAREAPPVIPPROXY_28,
  gameStrings.TEXT_WELFAREAPPVIPPROXY_29,
  True,
  98)]
TabMcs = ('mallList', 'bonusList', 'rightList', 'rebetMc')
TabPos = (300, 468, 635, 803)
TopTabPos = (1, 185)
TopTabMcs = ['commonBtn', 'superBtn']
APPLIST_NUM = 4
BONUS_ITEM_NUM = 6
TABNUM = 4
ACTIVATE_TYPE_NUM = 2
MALLITEM_HEIGHT = 85
BONUSITEM_HEIGHT = 126

class WelfareAppVipProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WelfareAppVipProxy, self).__init__(uiAdapter)
        self.widget = None
        self.currentPage = 0
        self.currentType = 0
        self.recommendWndShowed = False
        self.adLink = ''

    def reset(self):
        self.currentPage = 0
        self.currentType = 0
        self.adLink = ''

    def initAppVip(self, widget):
        self.widget = ASObject(widget)
        self.initUI()
        self.refreshInfo()
        self.checkShowRecommendWnd()
        self.queryAd()

    def unRegistAppVip(self):
        self.widget = None
        self.reset()

    def checkShowRecommendWnd(self):
        if not self.widget:
            return
        if self.recommendWndShowed:
            return
        if not neteaseAppVipHelper.getInstance().isAppVip():
            level = neteaseAppVipHelper.getInstance().getVipLevel()
            if level >= 5:
                self.showRecommendWnd()
                self.recommendWndShowed = True

    def showRecommendWnd(self):
        p = BigWorld.player()
        msg = gameStrings.APPVIP_RECOMMEND_TEXT
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.openQRCode, 'appVip/vip.png', gameStrings.APPVIP_ACTIVATE_DESC), yesBtnText=gameStrings.APPVIP_ACTIVATE_IMMEDIATE, noBtnText=gameStrings.SPRITE_RERANDOM_SAVE_CANCEL)

    def getAppVipLabel(self):
        if neteaseAppVipHelper.getInstance().isSuperVip():
            return gameStrings.APPVIP_SUPERVIP_NAME
        if neteaseAppVipHelper.getInstance().isCommonVip():
            return gameStrings.APPVIP_NORMAL_VIP
        return gameStrings.APPVIP_NETEASE_VIP

    def isOpen(self):
        return gameglobal.rds.configData.get('enableNeteaseGameMembershipRights', False)

    def onTopTabClick(self, *args):
        e = ASObject(args[3][0])
        tabName = e.target.name
        self.currentType = e.target.index
        for topName in TopTabMcs:
            self.widget.vipTabs.getChildByName(topName).selected = topName == tabName

        self.refreshActivateInfo(self.currentType)

    def initTopTabs(self):
        for i, topName in enumerate(TopTabMcs):
            tabMc = self.widget.vipTabs.getChildByName(topName)
            tabMc.index = i
            tabMc.addEventListener(events.BUTTON_CLICK, self.onTopTabClick)
            if i == self.currentType:
                tabMc.selected = True
            else:
                tabMc.selected = False

    def initActivateAppList(self):
        for i in xrange(APPLIST_NUM):
            self.widget.buyMc.superVipMc.getChildByName('app%d' % i).textField.text = gameStrings.APPVIP_SUPERVIP_APPLIST[i]

    def initTabs(self):
        for i in xrange(TABNUM):
            tabMc = self.widget.getChildByName('btn%d' % i)
            if tabMc:
                tabMc.index = i
                tabMc.addEventListener(events.BUTTON_CLICK, self.onTabClick)
                if i == self.currentPage:
                    tabMc.selected = True
                else:
                    tabMc.selected = False

    def initLists(self):
        self.widget.mallList.itemRenderer = 'WelfareAppVip_mallItem'
        self.widget.mallList.labelFunction = self.mallItemLabelFunction
        self.widget.mallList.itemHeight = MALLITEM_HEIGHT
        self.widget.rightList.itemRenderer = 'WelfareAppVip_rightItem'
        self.widget.rightList.labelFunction = self.rightItemLabelFunction
        self.widget.rightList.itemHeight = MALLITEM_HEIGHT
        self.widget.bonusList.itemRenderer = 'WelfareAppVip_bonusItem'
        self.widget.bonusList.labelFunction = self.bonusItemLabelFunction
        self.widget.bonusList.itemHeight = BONUSITEM_HEIGHT

    def initUI(self):
        if not self.widget:
            return
        self.initTabIndex()
        self.initTopTabs()
        self.initActivateAppList()
        self.initTabs()
        self.initLists()
        self.widget.buyMc.activateBtn.addEventListener(events.BUTTON_CLICK, self.onBtnClick)
        self.widget.activateMc.mainMC.closeBtn.addEventListener(events.BUTTON_CLICK, self.onBtnClick)
        self.widget.openAppMc.linkText.addEventListener(events.MOUSE_CLICK, self.onBtnClick)
        self.widget.activateMc.visible = False

    def initTabIndex(self):
        if not neteaseAppVipHelper.getInstance().isAppVip():
            self.widget.btn0.x = TabPos[2]
            self.widget.btn2.x = TabPos[0]
            self.currentPage = 2
        else:
            self.widget.btn0.x = TabPos[0]
            self.widget.btn2.x = TabPos[2]
            self.currentPage = 0
        level = neteaseAppVipHelper.getInstance().getVipLevel()
        if level >= 5:
            self.widget.vipTabs.getChildByName(TopTabMcs[0]).x = TopTabPos[1]
            self.widget.vipTabs.getChildByName(TopTabMcs[1]).x = TopTabPos[0]
            self.currentType = 1
        else:
            self.widget.vipTabs.getChildByName(TopTabMcs[1]).x = TopTabPos[1]
            self.widget.vipTabs.getChildByName(TopTabMcs[0]).x = TopTabPos[0]
            self.currentType = 0

    def onBtnClick(self, *args):
        e = ASObject(args[3][0])
        btnName = e.target.name
        if btnName == 'closeBtn':
            self.widget.activateMc.visible = False
        elif btnName == 'activateBtn':
            self.openQRCode('appVip/vip.png', gameStrings.APPVIP_ACTIVATE_DESC)
        elif btnName == 'linkText':
            self.openQRCode('appVip/app.png', gameStrings.APPVIP_OPENAPP_DESC)

    def onTabClick(self, *args):
        e = ASObject(args[3][0])
        index = e.target.index
        self.currentPage = index
        for i in xrange(TABNUM):
            tabMc = self.widget.getChildByName('btn%d' % i)
            if tabMc:
                tabMc.selected = i == self.currentPage

        self.refreshBindInfo()
        self.refreshContent()

    def refreshVipInfo(self):
        p = BigWorld.player()
        if neteaseAppVipHelper.getInstance().isAppVip():
            self.widget.vipInfo.visible = True
            self.widget.vipTabs.visible = False
            if neteaseAppVipHelper.getInstance().isSuperVip():
                self.widget.vipInfo.welcomeText.htmlText = gameStrings.APPVIP_SUPERVIP_WELCOME_TEXT
            elif neteaseAppVipHelper.getInstance().isCommonVip():
                self.widget.vipInfo.welcomeText.htmlText = gameStrings.APPVIP_COMMONVIP_WELCOME_TEXT
            timeArray = time.localtime(p.neteaseMembershipInfo.getMembershpExpireDate())
            self.widget.vipInfo.validTimeText.htmlText = gameStrings.MALL_APP_EXPIRE_DATE % str(time.strftime('%Y/%m/%d', timeArray))
            self.widget.vipInfo.helpIcon.addEventListener(events.MOUSE_CLICK, self.onHelpIconClick)
        else:
            self.widget.vipInfo.visible = False
            self.widget.vipTabs.visible = True

    def onHelpIconClick(self, *args):
        BigWorld.openUrl(NMCD.data.get('vipUrl', ''))

    def refreshBindInfo(self):
        if neteaseAppVipHelper.getInstance().isAppVip():
            self.widget.bindInfo.visible = True
            self.widget.bindInfo.bindBtn.visible = False
            self.widget.bindInfo.infoText.visible = True
            bind = neteaseAppVipHelper.getInstance().isBind()
            if bind:
                self.widget.bindInfo.bindBtn.enabled = False
                self.widget.bindInfo.bindBtn.label = gameStrings.MALL_BIND
            else:
                self.widget.bindInfo.bindBtn.enabled = True
                self.widget.bindInfo.bindBtn.label = gameStrings.APPVIP_DOBIND
                self.widget.bindInfo.bindBtn.addEventListener(events.BUTTON_CLICK, self.showPrivilegeBindWnd)
            if self.currentPage == 0:
                if bind:
                    self.widget.bindInfo.infoText.text = gameStrings.APPVIP_MALL_BIND_TEXT
                else:
                    self.widget.bindInfo.infoText.text = gameStrings.APPVIP_MALL_UNBIND_TEXT
                self.widget.bindInfo.bindBtn.visible = True
            elif self.currentPage == 1:
                self.widget.bindInfo.infoText.text = gameStrings.APPVIP_BONUS_BIND_TEXT
            elif self.currentPage == 2:
                self.widget.bindInfo.infoText.text = gameStrings.APPVIP_REIGHT_BIND_TEXT
            elif self.currentPage == 3:
                if neteaseAppVipHelper.getInstance().hasRebet():
                    self.widget.bindInfo.infoText.text = gameStrings.APPVIP_REBET_BIND_TEXT
                else:
                    self.widget.bindInfo.infoText.text = gameStrings.APPVIP_REBET_BIND_NO_TIME_TEXT
        else:
            self.widget.bindInfo.visible = False

    def refreshActivateInfo(self, type = 0):
        if neteaseAppVipHelper.getInstance().isAppVip():
            self.widget.buyMc.visible = False
            self.widget.openAppMc.visible = True
        else:
            self.widget.buyMc.visible = True
            self.widget.openAppMc.visible = False
            activateInfo = NMCD.data.get('vipActivateInfo', DEFAULT_VIP_ACTIVATEINFO)
            activateIndex = 0
            level = neteaseAppVipHelper.getInstance().getVipLevel()
            if level >= 5:
                activateIndex = 1
            info = activateInfo[activateIndex + type * ACTIVATE_TYPE_NUM]
            buyMc = self.widget.buyMc
            buyMc.superVipMc.visible = info[2]
            buyMc.vipNameText.text = info[0]
            buyMc.vipDescText.text = info[1]
            if not info[1]:
                buyMc.vipNameText.y = 12
            else:
                buyMc.vipNameText.y = 3
            buyMc.priceText.text = gameStrings.APPVIP_ACTIVATE_PRICE_TEXT % info[3]

    def refreshContent(self):
        if not self.widget:
            return
        for i, mcName in enumerate(TabMcs):
            itemMc = self.widget.getChildByName(mcName)
            if itemMc:
                if i == self.currentPage:
                    itemMc.visible = True
                else:
                    itemMc.visible = False

        if self.currentPage == 0:
            self.refreshMallList()
        elif self.currentPage == 1:
            self.refreshBonusList()
        elif self.currentPage == 2:
            self.refreshRightList()
        elif self.currentPage == 3:
            self.refreshRebetInfo()

    def bindAppPrivilege(self):
        p = BigWorld.player()
        p.base.applyMembershipInGame(gametypes.RIGHT_TYPE_BINDING_GAME)

    def showPrivilegeBindWnd(self, *args):
        p = BigWorld.player()
        if hasattr(p, 'neteaseMembershipInfo'):
            if neteaseAppVipHelper.getInstance().isBind():
                return True
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.MALL_BIND_CONFIRM, self.bindAppPrivilege), MBButton(gameStrings.CBG_HOME_GUANBI, None)]
            gameglobal.rds.ui.messageBox.show(True, gameStrings.MALL_BIND_TITLE, gameStrings.MALL_BIND_MSG, buttons)
        return False

    def mallItemLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        if itemData.isTip:
            itemMc.gotoAndStop('downTip')
            itemMc.tipText.htmlText = gameStrings.APPVIP_MALL_DOWN_TEXT
            return
        itemMc.gotoAndStop('normal')
        itemInfo = uiUtils.getGfxItemById(itemData.itemId, itemData.many)
        itemMc.slot.dragable = False
        itemMc.slot.setItemSlotData(itemInfo)
        itemMc.nameText.text = itemData.name
        if itemData.originalPrice:
            itemMc.discontLine.visible = True
            itemMc.discount.visible = True
            itemMc.originalPrice.typeText.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_ORIGINAL_PRICE
            itemMc.originalPrice.price.text = str(itemData.originalPrice)
            itemMc.originalPrice.coinIcon.bonusType = uiConst.MONEY_TYPE_MAP.get(int(itemData.priceType))
            itemMc.realPrice.visible = True
            itemMc.realPrice.typeText.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_CURRENT_PRICE
            itemMc.realPrice.price.text = str(itemData.priceVal)
            itemMc.realPrice.coinIcon.bonusType = uiConst.MONEY_TYPE_MAP.get(int(itemData.priceType))
            rate = round(itemData.priceVal * 10.0 / itemData.originalPrice, 1)
            itemMc.discount.textField.text = str(rate) + gameStrings.ACTIVITY_SHOP_PROXY_DISCOUNT
        else:
            itemMc.discontLine.visible = False
            itemMc.discount.visible = False
            itemMc.discount.textField.text = ''
            itemMc.originalPrice.typeText.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_CURRENT_PRICE
            itemMc.originalPrice.price.text = str(itemData.priceVal)
            itemMc.originalPrice.coinIcon.bonusType = uiConst.MONEY_TYPE_MAP.get(int(itemData.priceType))
            itemMc.realPrice.visible = False
        limitType = int(itemData.limitType)
        leftNum = itemData.leftNum
        if limitType == tianyuMallProxy.LIMIT_TYPE_NONE:
            itemMc.limit.text = ''
        elif limitType == tianyuMallProxy.LIMIT_TYPE_DAY:
            totalNum = itemData.dayLimit
            itemMc.limit.text = gameStrings.REMAIN_DAY_2 % (leftNum, totalNum)
        elif limitType == tianyuMallProxy.LIMIT_TYPE_WEEK:
            totalNum = itemData.weekLimit
            itemMc.limit.text = gameStrings.REMAIN_WEEK_2 % (leftNum, totalNum)
        elif limitType == tianyuMallProxy.LIMIT_TYPE_MONTH:
            totalNum = itemData.monthLimit
            itemMc.limit.text = gameStrings.REMAIN_MONTH_2 % (leftNum, totalNum)
        elif limitType == tianyuMallProxy.LIMIT_TYPE_FIRST_BUY:
            totalNum = itemData.totalLimit
            itemMc.limit.text = gameStrings.REMAIN_TOTAL_2 % (leftNum, totalNum)
        if neteaseAppVipHelper.getInstance().isAppVip():
            itemMc.buyBtn.mallId = itemData.mallId
            itemMc.buyBtn.label = gameStrings.ACTIVITY_SALE_GROUP_BUY_PURCHASE_NOW
            itemMc.buyBtn.enabled = limitType == tianyuMallProxy.LIMIT_TYPE_NONE or leftNum > 0
            itemMc.buyBtn.addEventListener(events.BUTTON_CLICK, self.onBuyMallItemClick)
        else:
            itemMc.buyBtn.label = gameStrings.APPVIP_ONLY_VIP
            itemMc.buyBtn.enabled = False

    def onBuyMallItemClick(self, *args):
        p = BigWorld.player()
        mallRequireLv = gameglobal.rds.ui.tianyuMall.getMallUseableMinLv()
        if p.lv < mallRequireLv:
            p.showGameMsg(GMDD.data.MALL_REQUIRE_HIGHER_LEVEL, ())
            return
        e = ASObject(args[3][0])
        mallId = e.target.mallId
        if not neteaseAppVipHelper.getInstance().isBind():
            self.showPrivilegeBindWnd()
            return
        gameglobal.rds.ui.tianyuMall.mallBuyConfirm(mallId, 1, 'appVip.' + str(mallId))

    def refreshMallList(self):
        itemInfo = neteaseAppVipHelper.getInstance().getVipMallItemInfo()
        if not neteaseAppVipHelper.getInstance().isAppVip():
            itemInfo.append({'isTip': True})
        self.widget.mallList.dataArray = itemInfo
        self.widget.mallList.validateNow()

    def bonusItemLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        if itemData.isTip:
            itemMc.gotoAndStop('downTip')
            itemMc.tipText.htmlText = gameStrings.APPVIP_BONUS_DOWN_TEXT
            return
        itemMc.gotoAndStop('normal')
        itemList = itemData.itemList
        itemMc.title.text = itemData.name
        itemMc.desc.htmlText = itemData.desc
        for i in xrange(BONUS_ITEM_NUM):
            slotMc = itemMc.getChildByName('slot%d' % i)
            slotMc.dragable = False
            if i < len(itemList):
                bType, itemId, itemNum = itemList[i]
                itemInfo = uiUtils.getGfxItemById(itemId, itemNum)
                slotMc.setItemSlotData(itemInfo)
                slotMc.visible = True
            else:
                slotMc.visible = False

        if not neteaseAppVipHelper.getInstance().isAppVip():
            itemMc.getBtn.enabled = False
            itemMc.getBtn.label = gameStrings.APPVIP_ONLY_VIP
            itemMc.bindText.text = ''
        else:
            rightType = int(itemData.bonusType)
            bonusState = neteaseAppVipHelper.getInstance().getVipBonusState(rightType)
            bindMax = 1
            bindCurr = 0
            if neteaseAppVipHelper.getInstance().isBind():
                bindCurr = 1
            if rightType == gametypes.RIGHT_TYPE_RECV_SEQUENT_GIFT:
                bindMax = 3
                bindCurr = neteaseAppVipHelper.getInstance().getSequenceBindTime()
            if rightType == gametypes.RIGHT_TYPE_RECV_ACTIVATION_GIFT:
                itemMc.bindText.visible = False
            else:
                itemMc.bindText.visible = True
            if bonusState == neteaseAppVipHelper.BONUS_AVALIABLE:
                itemMc.getBtn.enabled = True
                itemMc.getBtn.label = gameStrings.ACHVMENT_WEEKLY_AWARD_GET
                itemMc.bindText.text = gameStrings.APPVIP_BONUS_BIND_TIME % (bindCurr, bindMax)
            else:
                itemMc.getBtn.enabled = False
                if bonusState == neteaseAppVipHelper.BONUS_GETED:
                    itemMc.bindText.text = gameStrings.APPVIP_BONUS_BIND_TIME % (bindCurr, bindMax)
                    itemMc.getBtn.label = gameStrings.ACHVMENT_WEEKLY_AWARD_ALREADYGOT
                else:
                    if neteaseAppVipHelper.getInstance().isBind():
                        itemMc.bindText.text = gameStrings.APPVIP_BONUS_BIND_TIME % (bindCurr, bindMax)
                    else:
                        itemMc.bindText.text = gameStrings.APPVIP_BONUS_BIND_TIME % (bindCurr, bindMax)
                    itemMc.getBtn.label = gameStrings.ACHVMENT_WEEKLY_AWARD_GET
            itemMc.getBtn.bonusType = rightType
            itemMc.getBtn.addEventListener(events.BUTTON_CLICK, self.getVipBonus)

    def getVipBonus(self, *args):
        e = ASObject(args[3][0])
        bonusType = int(e.target.bonusType)
        p = BigWorld.player()
        p.base.applyMembershipInGame(bonusType)

    def refreshBonusList(self):
        itemInfo = neteaseAppVipHelper.getInstance().getVipBonusItemInfo()
        if not neteaseAppVipHelper.getInstance().isAppVip():
            itemInfo.append({'isTip': True})
        self.widget.bonusList.dataArray = itemInfo
        self.widget.bonusList.validateNow()

    def refreshRebetInfo(self):
        if neteaseAppVipHelper.getInstance().isAppVip():
            self.widget.rebetMc.descText.htmlText = NMCD.data.get('rebetVipDesc', '')
            self.widget.rebetMc.rechargeBtn.label = gameStrings.APPVIP_RECHARGET
            self.widget.rebetMc.rechargeBtn.addEventListener(events.BUTTON_CLICK, self.onRechargeBtnClick)
            self.widget.rebetMc.rechargeBtn.enabled = neteaseAppVipHelper.getInstance().hasRebet()
        else:
            self.widget.rebetMc.descText.htmlText = NMCD.data.get('rebetNotVipDesc', '')
            self.widget.rebetMc.rechargeBtn.label = gameStrings.APPVIP_ONLY_VIP
            self.widget.rebetMc.rechargeBtn.enabled = False

    def onRechargeBtnClick(self, *args):
        p = BigWorld.player()
        mallRequireLv = gameglobal.rds.ui.tianyuMall.getMallUseableMinLv()
        if p.lv < mallRequireLv:
            p.showGameMsg(GMDD.data.MALL_REQUIRE_HIGHER_LEVEL, ())
            return
        gameglobal.rds.ui.newRecharge.confrimRebet()

    def getIconPath(self, iconId):
        return 'item/icon64/' + str(iconId) + '.dds'

    def rightItemLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        if itemData.isTip:
            itemMc.gotoAndStop('downTip')
            itemMc.tipText.htmlText = gameStrings.APPVIP_RIGHT_DOWN_TEXT
            return
        itemMc.gotoAndStop('normal')
        itemMc.title.text = itemData.name
        itemMc.icon.fitSize = True
        itemMc.icon.loadImage(self.getIconPath(itemData.icon))
        itemMc.desc.htmlText = itemData.desc
        if not itemData.isGet:
            itemMc.getBtn.enabled = False
            if neteaseAppVipHelper.getInstance().isAppVip():
                itemMc.getBtn.label = gameStrings.APPVIP_ACTIVATE
            else:
                itemMc.getBtn.label = gameStrings.APPVIP_ONLY_VIP
        else:
            state = neteaseAppVipHelper.getInstance().getTitleRecieveState()
            if not neteaseAppVipHelper.getInstance().isAppVip():
                itemMc.getBtn.enabled = False
                itemMc.getBtn.label = gameStrings.APPVIP_ONLY_VIP
                return
            if state == -1:
                itemMc.getBtn.enabled = False
                itemMc.getBtn.label = gameStrings.MALL_HAVE_RECIEVE
            elif state == 0:
                itemMc.getBtn.enabled = False
                itemMc.getBtn.label = gameStrings.HISTORY_CONSUMED_DRAW
            else:
                itemMc.getBtn.enabled = True
                itemMc.getBtn.label = gameStrings.HISTORY_CONSUMED_DRAW
                itemMc.getBtn.addEventListener(events.BUTTON_CLICK, self.onGetTitleBtnClick)

    def onGetTitleBtnClick(self, *args):
        neteaseAppVipHelper.getInstance().getUnRecieveTitles()

    def getRedFlagVisible(self):
        return neteaseAppVipHelper.getInstance().needShowNewIcon()

    def refreshRightList(self):
        rightList = []
        rightInfo = NMCD.data.get('vipRightList', [])
        for info in rightInfo:
            rightItem = {'icon': info[0],
             'name': info[1],
             'desc': info[2],
             'isGet': info[3] if len(info) > 3 else False}
            rightList.append(rightItem)

        if not neteaseAppVipHelper.getInstance().isAppVip():
            rightList.append({'isTip': True})
        self.widget.rightList.dataArray = rightList
        self.widget.rightList.validateNow()

    def openQRCode(self, path, desc = ''):
        if not self.widget:
            return
        mainMc = self.widget.activateMc.mainMC
        mainMc.pic.fitSize = True
        mainMc.pic.loadImage(path)
        mainMc.descText.htmlText = desc
        self.widget.activateMc.visible = True

    def queryAd(self):
        adPos = NMCD.data.get('vipAdPos', 'wangyiyouxihuiyuanjulebu-changgui-955750')
        remoteInterface.getNeteaseVipAdInfo(adPos, self.onGetAdInfo)

    def onGetAdInfo(self, retCode, data):
        if not self.widget:
            return
        if retCode == 0:
            contents = data.get('result', {}).get('content', {}).values()[0]
            content = contents[0]
            photoUrl = content.get('src', '')
            banner = self.widget.banner
            if photoUrl and banner:
                banner.fitSize = True
                banner.imgType = uiConst.IMG_TYPE_HTTP_IMG
                banner.url = str(photoUrl)
                self.adLink = content.get('url', '')
                banner.addEventListener(events.MOUSE_CLICK, self.onAdMcClick)

    def onAdMcClick(self, *args):
        if self.adLink:
            BigWorld.openUrl(self.adLink)

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshVipInfo()
        self.refreshBindInfo()
        self.refreshActivateInfo(self.currentType)
        self.refreshContent()
