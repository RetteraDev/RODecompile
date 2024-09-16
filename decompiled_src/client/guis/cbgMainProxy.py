#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cbgMainProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import events
import const
import utils
import math
import gametypes
from uiTabProxy import UITabProxy
from guis import uiUtils
from guis import cbgUtils
from guis import ui
from ui import unicode2gbk
from gamestrings import gameStrings
from callbackHelper import Functor
from data import cbg_config_data as CCD
from cdata import game_msg_def_data as GMDD
import gamelog
TAB_HOME_IDX = 0
TAB_BUY_IDX = 1
TAB_SELL_IDX = 2
TIP_NUM = 5
TIP_START_Y = 39

class CbgMainProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(CbgMainProxy, self).__init__(uiAdapter)
        self.addEvent(events.EVENT_UPDATE_OWN_CBG_DATA, self.onUpdateCbgDataOwn, isGlobal=True)
        self.addEvent(events.EVENT_UPDATE_BOUGHT_CBG_DATA, self.onUpdateCbgDataBought, isGlobal=True)
        self.addEvent(events.EVENT_REMOVE_OWN_CBG_DATA, self.onReomveCbgDataOwn, isGlobal=True)
        self.addEvent(events.EVENT_REMOVE_BOUGHT_CBG_DATA, self.onRemoveCbgDataBought, isGlobal=True)
        self.addEvent(events.EVENT_UPDATE_QUERY_ALL_DATA, self.onQueryCbgDataAll, isGlobal=True)
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CBG_BACKGROUND, self.onCloseTreasure)

    def reset(self):
        self.entId = 0
        self.treasureInfo = {}
        self.autoGoHome = False
        self.cbgDataOwn = {}
        self.cbgDataBought = {}
        self.cbgDataAll = []
        self.roleSaleData = {}
        self.conditionDic = {}
        self.cbgOnSaleRoleData = []

    def hide(self, destroy = True):
        self.onCloseTreasure()

    def onCloseTreasure(self, *arg):
        self.entId = 0
        self.treasureInfo = {}
        self.autoGoHome = False
        gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.inventoryPassword.hide()
        self.clearWidget()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CBG_BACKGROUND:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        super(CbgMainProxy, self).clearWidget()
        self.widget = None
        self.entId = 0
        self.roleSaleData = {}
        self.conditionDic = {}
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CBG_BACKGROUND)

    def _getTabList(self):
        return [{'tabIdx': TAB_HOME_IDX,
          'tabName': 'tabHome',
          'view': 'CBGHomeWidget',
          'proxy': 'cbgHome'}, {'tabIdx': TAB_BUY_IDX,
          'tabName': 'tabBuy',
          'view': 'CBGWannaBuyWidget',
          'proxy': 'cbgWannaBuy'}, {'tabIdx': TAB_SELL_IDX,
          'tabName': 'tabSell',
          'view': 'CBGWannaSellWidget',
          'proxy': 'cbgWannaSell'}]

    def show(self, entId):
        if not gameglobal.rds.configData.get('enableCBG', False) or not gameglobal.rds.configData.get('enableCBGRole', False):
            return
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableCBGOpenURLSkip', False) and utils.getAccountType(p.roleURS) != gametypes.ACCOUNT_TYPE_URS:
            msg = uiUtils.getTextFromGMD(GMDD.data.CBG_OPEN_URL_HINT, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=p.base.fastLogonCbg, noCallback=self.hide)
            return
        self.entId = entId
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CBG_BACKGROUND)

    def initUI(self):
        self.mall = gameglobal.rds.ui.tianyuMall
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTabUI()
        if self.showTabIndex == -1:
            self.widget.setTabIndex(TAB_HOME_IDX)
        gameStrings.TEXT_CBGMAINPROXY_117
        BigWorld.player().base.searchCBGBought()
        BigWorld.player().base.searchOwnCBG()

    def refreshInfo(self):
        if not self.widget:
            return
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'refreshInfo'):
            proxy.refreshInfo()

    def onTabChanged(self, *args):
        super(CbgMainProxy, self).onTabChanged(*args)

    def _onTabBtn0Click(self, e):
        print 'onTabBtn0Click', e.target, e.type

    def onUpdateCbgDataOwn(self, event):
        self.cbgDataOwn.update(event.data)
        self.refreshInfo()

    def onUpdateCbgDataBought(self, event):
        self.cbgDataBought.update(event.data)
        self.refreshInfo()

    def onReomveCbgDataOwn(self, event):
        cbgId = event.data.get('cbgId', 0)
        self.cbgDataOwn.pop(cbgId, None)
        self.refreshInfo()

    def onRemoveCbgDataBought(self, event):
        cbgId = event.data.get('cbgId', 0)
        self.cbgDataBought.pop(cbgId, None)
        self.refreshInfo()

    def onQueryCbgDataAll(self, event):
        self.cbgDataAll = event.data
        self.refreshInfo()

    def genTreasureHomeInfo(self):
        ret = {}
        cbgData = []
        cbgData.extend(self.genOwnCbgData())
        cbgData.extend(self.genBoughtCbgData())
        cbgData.sort(self.cbgItemCmp)
        ret['infoList'] = cbgData
        return ret

    def cbgItemCmp(self, item1, item2):
        if item1['canOper'] != item2['canOper']:
            return -(item1['canOper'] - item2['canOper'])
        return -(item1['tExpire'] - item2['tExpire'])

    def genOwnCbgData(self):
        ret = []
        p = BigWorld.player()
        for k in self.cbgDataOwn:
            ci = self.cbgDataOwn[k]
            info = uiUtils.getGfxItemById(cbgUtils.CASH_ITEM_ID, picSize=uiConst.ICON_SIZE40)
            info.update(ci)
            info['itemType'] = cbgUtils.CBG_ITEM_TYPE_CASH
            info['tradeType'] = const.CBG_SEARCH_TYPE_OWN
            info['itemName'] = str(int(ci['cnt'] / cbgUtils.CBG_TRADE_UNIT)) + gameStrings.CBG_TEN_THOUSANDS
            info['tExpire'] = ci['tLong'] * const.TIME_INTERVAL_DAY - (utils.getNow() - ci['tBegin'])
            info['cbgId'] = k
            info['canOper'] = ci['goodsType'] != const.CBG_GOODS_TYPE_ROLE and ci['opType'] == const.CBG_OP_TYPE_SELL
            if ci['goodsType'] == const.CBG_GOODS_TYPE_ROLE:
                info['roleName'] = p.roleName
                info['roleSchool'] = p.physique.school
                info['roleLevel'] = p.lv
                info['roleSex'] = p.physique.sex
                info['roleCombat'] = p.combatScoreList[const.COMBAT_SCORE]
            ret.append(info)

        return ret

    def genBoughtCbgData(self):
        ret = []
        for k in self.cbgDataBought:
            ci = self.cbgDataBought[k]
            info = uiUtils.getGfxItemById(cbgUtils.CASH_ITEM_ID, picSize=uiConst.ICON_SIZE40)
            info.update(ci)
            info['itemType'] = cbgUtils.CBG_ITEM_TYPE_CASH
            info['tradeType'] = const.CBG_SEARCH_TYPE_BUY
            info['itemName'] = str(int(ci['cnt'] / cbgUtils.CBG_TRADE_UNIT)) + gameStrings.CBG_TEN_THOUSANDS
            info['tExpire'] = ci['tLong'] * const.TIME_INTERVAL_DAY - (utils.getNow() - ci['tBegin'])
            info['canOper'] = ci['goodsType'] != const.CBG_GOODS_TYPE_ROLE
            info['cbgId'] = k
            if ci['goodsType'] == const.CBG_GOODS_TYPE_ROLE and 'roleData' in ci:
                info.pop('roleData')
                info['roleName'] = ci['roleData'].get(const.CBG_ROLE_EXTRA_INDEX_NAME, '')
                info['roleSchool'] = ci['roleData'].get(const.CBG_ROLE_EXTRA_INDEX_SCHOOL, 0)
                info['roleLevel'] = ci['roleData'].get(const.CBG_ROLE_EXTRA_INDEX_LEVEL, 0)
                info['roleSex'] = ci['roleData'].get(const.CBG_ROLE_EXTRA_INDEX_SEX, 0)
                info['roleCombat'] = ci['roleData'].get(const.CBG_ROLE_EXTRA_INDEX_COMBAT_SCORE, 0)
            ret.append(info)

        return ret

    def genTreasureSellInfo(self):
        ret = {}
        ccdd = CCD.data
        ret['priceRange'] = ccdd.get('priceRange', (10, 300000))
        ret['cashRange'] = ccdd.get('cashRange', (10, 1000))
        ret['priceMaxChars'] = ccdd.get('priceMaxChars', 6)
        ret['cashMaxChars'] = ccdd.get('cashMaxChars', 4)
        ret['sellTips'] = ccdd.get('sellTips', ())
        ret['minPrice'] = 1.0 / CCD.data.get('maxSinglePrice', 5)
        ret['friendList'] = self.mall.getFriendList()
        ret.update(self.getColorConfigs())
        return ret

    def getColorConfigs(self):
        ret = {}
        ccdd = CCD.data
        DEF_TEXT_COLOR = 12563609
        ret['defaultCashColor'] = ccdd.get('defaultCashColor', DEF_TEXT_COLOR)
        ret['defaultPriceColor'] = ccdd.get('defaultPriceColor', DEF_TEXT_COLOR)
        cashColorList = ccdd.get('cashColorList', {})
        priceColorList = ccdd.get('priceColorList', {})
        cashColorKeys = []
        cashColorVals = []
        for k in cashColorList:
            cashColorKeys.append(k)
            cashColorVals.append(cashColorList[k])

        priceColorKeys = []
        priceColorVals = []
        for k in priceColorList:
            priceColorKeys.append(k)
            priceColorVals.append(priceColorList[k])

        ret['cashColorKeys'] = cashColorKeys
        ret['cashColorVals'] = cashColorVals
        ret['priceColorKeys'] = priceColorKeys
        ret['priceColorVals'] = priceColorVals
        return ret

    def genTreasureBuyInfo(self):
        ret = {}
        ccdd = CCD.data
        infoList = []
        for i in range(len(self.cbgDataAll)):
            ci = self.cbgDataAll[i]
            info = uiUtils.getGfxItemById(cbgUtils.CASH_ITEM_ID, picSize=uiConst.ICON_SIZE40)
            info['itemName'] = str(int(ci['cnt'] / cbgUtils.CBG_TRADE_UNIT)) + gameStrings.TEXT_CBGMAINPROXY_273
            info['price'] = ci['price']
            info['itemType'] = ci['itemType']
            info['tExpire'] = ci['tLong'] * const.TIME_INTERVAL_DAY - (utils.getNow() - ci['tBegin'])
            info['singlePrice'] = self.getSinglePrice(ci['price'], ci['cnt'])
            if info['tExpire'] > 0:
                infoList.append(info)

        ret['infoList'] = infoList
        ret['buyTips'] = ccdd.get('buyTips', ())
        return ret

    @ui.uiEvent(uiConst.WIDGET_CBG_BACKGROUND, events.EVENT_CASH_CHANGED)
    def onMoneyInfoUpdate(self):
        if hasattr(self.getCurrentProxy(), 'refreshMyMoney'):
            self.getCurrentProxy().refreshMyMoney()

    @ui.uiEvent(uiConst.WIDGET_CBG_BACKGROUND, events.EVENT_SELL_CASH_DONE)
    def onSellCashDone(self):
        gamelog.debug('ypc@ cbgMain onSellCashDone!')
        gameglobal.rds.ui.cbgSellConfirm.hide()
        self.treasureInfo.clear()
        if hasattr(self.getCurrentProxy(), 'sellCashDone'):
            self.getCurrentProxy().sellCashDone()
        self.widget.setTabIndex(TAB_HOME_IDX)

    def getMyMoneyInfo(self, *arg):
        return self.mall.getMyMoneyInfo()

    def openConfirmWidget(self, cash, price, targetRoleName, targetRoleGbId):
        cash *= cbgUtils.CBG_TRADE_UNIT
        price *= cbgUtils.CBG_RMB_UNIT
        singlePrice = self.getSinglePrice(price, cash)
        minPrice = 1.0 / CCD.data.get('maxSinglePrice', 5)
        if singlePrice < minPrice:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.CBG_MSG_TIP % (round(minPrice, 4), round(singlePrice, 4)))
            return
        self.treasureInfo['cash'] = cash
        self.treasureInfo['price'] = price
        self.treasureInfo['targetRoleName'] = unicode2gbk(targetRoleName)
        self.treasureInfo['targetRoleGbId'] = unicode2gbk(targetRoleGbId)
        gameglobal.rds.ui.cbgSellConfirm.show(cbgUtils.CBG_CONFIRM_SHOW_TYPE_MONEY)

    def getSinglePrice(self, price, cnt):
        price = float(price)
        cnt = max(float(cnt), float(cbgUtils.CBG_TRADE_UNIT))
        return price / cbgUtils.CBG_RMB_UNIT / (cnt / cbgUtils.CBG_TRADE_UNIT)

    def genTreasureMoneyConfirmInfo(self):
        ccdd = CCD.data
        ret = uiUtils.getGfxItemById(cbgUtils.CASH_ITEM_ID, picSize=uiConst.ICON_SIZE40)
        ret['taxRate'] = ccdd.get('taxRate', 0.05)
        ret['taxRange'] = ccdd.get('taxRange', (1, 10000))
        ret.update(self.treasureInfo)
        ret.update(self.getColorConfigs())
        return ret

    @ui.callFilter(2, False)
    @ui.checkInventoryLock()
    def confirmSellItem(self):
        if not self.entId:
            return
        ent = BigWorld.entities.get(self.entId)
        if not ent:
            return
        if not self.treasureInfo:
            return
        p = BigWorld.player()
        cash = int(self.treasureInfo['cash'])
        price = int(self.treasureInfo['price'])
        if self.treasureInfo['targetRoleGbId']:
            targetRoleGBID = int(self.treasureInfo['targetRoleGbId'])
        else:
            targetRoleGBID = 0
        interval = CCD.data.get('cbgInterval', (2,))
        ent.cell.sellCashInCBG(cash, targetRoleGBID, price, interval[0], p.cipherOfPerson)

    def fillTips(self, tipMc, tips):
        height = 0
        for i in range(TIP_NUM):
            tipText = tipMc['tips%d' % i]
            flagText = tipMc['flag%d' % i]
            if i < len(tips):
                tipText.htmlText = tips[i]
                flagText.visible = True
                tipText.height = tipText.textHeight + 5
            else:
                tipText.htmlText = ''
                flagText.visible = False
                tipText.height = 0
            flagText.y = tipText.y = TIP_START_Y + height
            height += tipText.height + 5

    @ui.checkInventoryLock()
    def onConfirmCancelCbgItem(self, tradeType, cbgId):
        p = BigWorld.player()
        if not self.entId:
            return
        ent = BigWorld.entities.get(self.entId)
        if not ent:
            return
        if tradeType == const.CBG_SEARCH_TYPE_OWN:
            ent.cell.takeBackCBGCash(cbgId, p.cipherOfPerson)
        else:
            ent.cell.takeAwayCBGCash(cbgId, p.cipherOfPerson)

    @ui.uiEvent(uiConst.WIDGET_CBG_BACKGROUND, events.EVENT_TAKE_BACK_FAILED)
    def onTakeBackCBGCashFailed(self):
        msg = gameStrings.CBG_TAKE_BACK_TIP
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.openTreasureWeb))

    def openTreasureWeb(self):
        cbgUrl = 'http://tianyu.cbg.163.com'
        BigWorld.openUrl(cbgUrl)

    @ui.uiEvent(uiConst.WIDGET_CBG_BACKGROUND, events.EVENT_CBG_ROLE_UNREGIST_SALE)
    def onApplyUnRegisterSaleRole(self, event):
        gamelog.debug('ypc@ onApplyUnRegisterSaleRole!')
        isOk = event.data
        if isOk:
            if self.currentTabIndex == TAB_SELL_IDX:
                self.getCurrentProxy().refreshInfo()
        else:
            gamelog.debug('ypc@ error:onApplyUnRegisterSaleRole failed!')

    @ui.uiEvent(uiConst.WIDGET_CBG_BACKGROUND, events.EVENT_CBG_ROLE_REGIST)
    def onApplyRegisterSaleRole(self, event):
        isOk = event.data.get('isOk', False)
        conditions = event.data.get('conditions', {})
        if isOk:
            gamelog.debug('ypc@ onApplyRegisterSaleRole success!')
            self.conditionDic[cbgUtils.CBG_CONDITION_TYPE_REGIST] = conditions.copy()
            if self.currentTabIndex == TAB_SELL_IDX:
                self.getCurrentProxy().refreshInfo()
        else:
            gamelog.debug('ypc@ error:onApplyRegisterSaleRole failed!', event.data.get('conditions', None))

    @ui.uiEvent(uiConst.WIDGET_CBG_BACKGROUND, events.EVENT_CBG_ROLE_SALE)
    def onApplySellSaleRole(self, event):
        isOk = event.data.get('isOk', False)
        conditions = event.data.get('conditions', {})
        if isOk:
            if conditions:
                self.conditionDic[cbgUtils.CBG_CONDITION_TYPE_SALE] = conditions.copy()
            if self.currentTabIndex == TAB_SELL_IDX:
                self.getCurrentProxy().refreshInfo()
        else:
            gamelog.debug('ypc@ error:onApplyRegisterSaleRole failed!', event.data.get('conditions', None))

    @ui.callFilter(1, True)
    @ui.checkInventoryLock()
    def startRegistRole(self):
        p = BigWorld.player()
        p.base.queryRegisterSaleRoleConditions(p.cipherOfPerson)

    def onRegistConditionsConfirm(self):
        gameglobal.rds.ui.cbgRule.show(cbgUtils.CBG_RULE_TYPE_REGIST, self._onRegistRuleConfirm)

    def _onRegistRuleConfirm(self):
        gamelog.debug('ypc@ _onRuleConfirmFromRegist!')
        gameglobal.rds.ui.cbgSafeInfoConfirm.show(self._realStartRegistRole)

    def _realStartRegistRole(self):
        if not self.entId:
            gamelog.debug('ypc@ realStartRegistRole entId is None error!')
            return
        ent = BigWorld.entities.get(self.entId)
        if not ent:
            gamelog.debug('ypc@ realStartRegistRole entId error!')
            return
        p = BigWorld.player()
        ent.cell.applyRegisterSaleRole(p.cipherOfPerson)

    def onQueryRegisterConditions(self, conditions):
        self.conditionDic[cbgUtils.CBG_CONDITION_TYPE_REGIST] = conditions
        gameglobal.rds.ui.cbgRoleConditions.show(cbgUtils.CBG_CONDITION_TYPE_REGIST)

    @ui.checkInventoryLock()
    @ui.callFilter(1, True)
    def startSellRole(self, saleData):
        self.roleSaleData = saleData
        self._querySaleRoleConditions()
        self.saveFigurePhoto()

    def onSellConditionsConfirm(self):
        gameglobal.rds.ui.cbgRule.show(cbgUtils.CBG_RULE_TYPE_SALE, self._onSellRuleConfirm)

    def _onSellRuleConfirm(self):
        gameglobal.rds.ui.cbgSafeInfoConfirm.show(self._onSafeInfoConfirm)

    def _onSafeInfoConfirm(self):
        gameglobal.rds.ui.cbgSellConfirm.show(cbgUtils.CBG_CONFIRM_SHOW_TYPE_ROLE)

    def _querySaleRoleConditions(self):
        if not self.roleSaleData:
            gamelog.debug('ypc@ cbgMain roleSaleData error!')
            return
        price = self.roleSaleData['price']
        days = self.roleSaleData['days']
        friendGbId = self.roleSaleData['friendGbId']
        p = BigWorld.player()
        p.base.querySaleRoleConditions(p.cipherOfPerson, price, days, friendGbId)

    def realSellRole(self):
        if not self.roleSaleData:
            gamelog.debug('ypc@ cbgMain roleSaleData error!')
            return
        if not self.entId:
            gamelog.debug('ypc@ realStartSellRole entId is None error!')
            return
        ent = BigWorld.entities.get(self.entId)
        if not ent:
            gamelog.debug('ypc@ realStartSellRole entId error!')
            return
        p = BigWorld.player()
        price = self.roleSaleData['price']
        days = self.roleSaleData['days']
        friendGbId = self.roleSaleData['friendGbId']
        if gameglobal.rds.configData.get('enableCBGRoleDefaultFriendTarget', False):
            if not friendGbId:
                p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.CBG_SELL_FRIENDLIST_DEFAULT_WARNING)
                gamelog.debug('ypc@ realStartSellRole must specify a friend!')
                return
        if gameglobal.rds.configData.get('enableCBGRoleNotFriendTarget', False):
            if friendGbId:
                p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.CBG_SELL_FRIENDLIST_NOT_TARGET_WARNING)
                gamelog.debug('ypc@ realStartSellRole must specify no friend!')
                return
        ent.cell.applySaleRole(p.cipherOfPerson, price, days, friendGbId)
        gamelog.debug('ypc@ realStartSellRole ', price, days, friendGbId)
        p.onCbgRoleStartSelling()
        self.showWaitingMsg(gameStrings.CBG_ROLE_SALE_SELLING)

    def onQuerySellConditions(self, conditions):
        self.conditionDic[cbgUtils.CBG_CONDITION_TYPE_SALE] = conditions
        gameglobal.rds.ui.cbgRoleConditions.show(cbgUtils.CBG_CONDITION_TYPE_SALE)

    def getConditionByType(self, type):
        return self.conditionDic.get(type, {})

    def onUpdateCbgOnSaleRoleData(self, dataList):
        viewData = []
        p = BigWorld.player()
        for d in dataList:
            rData = d.get('roleData', None)
            if not rData:
                continue
            leftTime = self._genLeftTime(d.get('tBegin', 0), d.get('tLong', 0))
            leftDays = max(0, math.ceil(leftTime / const.TIME_INTERVAL_DAY))
            isTargetSelf = d.get('vendeeGbId', 0) == p.gbId
            if isTargetSelf:
                gamelog.debug('ypc@ onUpdateCbgOnSaleRoleData! target self!!!')
            viewData.append({'roleName': rData.get(const.CBG_ROLE_EXTRA_INDEX_NAME, ''),
             'school': rData.get(const.CBG_ROLE_EXTRA_INDEX_SCHOOL, 0),
             'level': rData.get(const.CBG_ROLE_EXTRA_INDEX_LEVEL, 0),
             'sex': rData.get(const.CBG_ROLE_EXTRA_INDEX_SEX, 0),
             'combat': rData.get(const.CBG_ROLE_EXTRA_INDEX_COMBAT_SCORE, 0),
             'leftTime': leftTime,
             'leftDays': leftDays,
             'price': int(d.get('price', 0)),
             'isTarget': isTargetSelf,
             'vendeeName': d.get('vendeeName', ''),
             'roleGbId': d.get('vendorGbId', 0)})

        self.cbgOnSaleRoleData = viewData
        if self.currentTabIndex == TAB_BUY_IDX:
            self.getCurrentProxy().refreshRole()

    def _genLeftTime(self, begin, lastDays):
        now = utils.getNow()
        lastTime = lastDays * const.TIME_INTERVAL_DAY
        return max(0, math.ceil(begin + lastTime - now))

    def getCbgOnSaleRoleData(self):
        return self.cbgOnSaleRoleData

    def checkUnRegistTime(self):
        p = BigWorld.player()
        if p.roleSaleData.saleStatus != gametypes.ROLE_SALE_STATUS_REGISTER:
            return False
        now = utils.getNow()
        deadline = CCD.data.get('roleSaleUnRegisterDays', 1) * const.TIME_INTERVAL_DAY
        if now - (p.roleSaleData.saleStatusTime + deadline) > 0:
            return True
        return False

    def checkSaleTime(self):
        p = BigWorld.player()
        if p.roleSaleData.saleStatus != gametypes.ROLE_SALE_STATUS_REGISTER:
            return False
        now = utils.getNow()
        deadline = CCD.data.get('roleSaleRegisterDays', 1) * const.TIME_INTERVAL_DAY
        if p.roleSaleData.saleStatusTime + deadline - now <= 0:
            gamelog.debug('ypc@ checkSaleTime!!!', p.roleSaleData.saleStatusTime, deadline, now)
            return True
        return False

    @ui.callFilter(1, False)
    @ui.checkInventoryLock()
    def requestCancelRegist(self):
        p = BigWorld.player()
        if not gameglobal.rds.ui.cbgMain.checkUnRegistTime():
            p.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.CBG_SELL_UNREGIST_WARNING % CCD.data.get('roleSaleUnRegisterDays', 1),))
            return
        gamelog.debug('ypc@ request applyUnRegisterSaleRole!')
        if not self.entId:
            gamelog.debug('ypc@ requestCancelRegist entId is None error!')
            return
        ent = BigWorld.entities.get(self.entId)
        if not ent:
            gamelog.debug('ypc@ requestCancelRegist entId error!')
            return
        ent.cell.applyUnRegisterSaleRole(p.cipherOfPerson)

    def showWaitingMsg(self, msg):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TIP, True)
        gameglobal.rds.ui.characterDetailAdjust.showTips(msg, 1)

    def closeWaitingMsg(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TIP)

    def saveFigurePhoto(self):
        p = BigWorld.player()
        if not hasattr(p, 'charSnapshotTime'):
            return
        snapTime = p.charSnapshotTime
        now = utils.getNow()
        if utils.isSameDay(snapTime, now):
            return
        p.takeFigurePhoto()

    def isShowNewCbg(self):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableCBGRole', False):
            return False
        if gameglobal.rds.configData.get('enableCBGRoleWhiteList', False) and not utils.isCbgRoleSameWhiteGbId(p.gbId):
            return False
        return True

    def onUpdateClientCfg(self):
        if self.isShowNewCbg():
            self.onCloseTreasure()
