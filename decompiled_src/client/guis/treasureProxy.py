#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/treasureProxy.o
import BigWorld
import const
import gameglobal
import utils
import gametypes
from callbackHelper import Functor
from guis import events
from guis import ui
from guis import uiConst
from guis import uiUtils
from guis import tianyuMallProxy
from uiProxy import UIProxy
from ui import unicode2gbk
from data import cbg_config_data as CCD
from cdata import game_msg_def_data as GMDD
CASH_ITEM_ID = 2
CBG_TRADE_UNIT = 10000
CBG_RMB_UNIT = 100

class TreasureProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TreasureProxy, self).__init__(uiAdapter)
        self.modelMap = {'getMyMoneyInfo': self.onGetMyMoneyInfo,
         'getTreasureInfo': self.onGetTreasureInfo,
         'closeTreasure': self.onCloseTreasure,
         'openConfirmWidget': self.onOpenConfirmWidget,
         'closeConfirmWidget': self.onCloseConfirmWidget,
         'confirmSellItem': self.onConfirmSellItem,
         'cancelCbgItem': self.onCancelCbgItem,
         'openTreasureWeb': self.onOpenTreasureWeb,
         'queryAllData': self.onQueryAllData}
        self.treasureMediator = None
        self.confirmMediator = None
        self.treasureWidgetId = uiConst.WIDGET_TREASURE
        self.confirmWidgetId = uiConst.WIDGET_TREASURE_CONFIRM
        uiAdapter.registerEscFunc(self.treasureWidgetId, self.onCloseTreasure)
        uiAdapter.registerEscFunc(self.confirmWidgetId, self.onCloseConfirmWidget)
        self.addEvent(events.EVENT_UPDATE_OWN_CBG_DATA, self.onUpdateCbgDataOwn, isGlobal=True)
        self.addEvent(events.EVENT_REMOVE_OWN_CBG_DATA, self.onReomveCbgDataOwn, isGlobal=True)
        self.addEvent(events.EVENT_UPDATE_BOUGHT_CBG_DATA, self.onUpdateCbgDataBought, isGlobal=True)
        self.addEvent(events.EVENT_REMOVE_BOUGHT_CBG_DATA, self.onRemoveCbgDataBought, isGlobal=True)
        self.addEvent(events.EVENT_UPDATE_QUERY_ALL_DATA, self.onQueryCbgDataAll, isGlobal=True)
        self.entId = 0
        self.treasureInfo = {}
        self.autoGoHome = False
        self.cbgDataOwn = {}
        self.cbgDataBought = {}
        self.cbgDataAll = []

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.treasureWidgetId:
            self.mall = gameglobal.rds.ui.tianyuMall
            self.treasureMediator = mediator
            BigWorld.player().base.searchCBGBought()
            BigWorld.player().base.searchOwnCBG()
        elif widgetId == self.confirmWidgetId:
            self.confirmMediator = mediator
            return uiUtils.dict2GfxDict(self.genTreasureConfirmInfo(), True)

    def onUpdateClientCfg(self):
        if not self.showTreasureConfig() and self.treasureMediator:
            self.onCloseTreasure()
        if not self.isTreasureNew():
            gameglobal.rds.ui.cbgMain.onCloseTreasure()

    def show(self, entId):
        if not self.showTreasureConfig():
            return
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableCBGOpenURLSkip', False) and utils.getAccountType(p.roleURS) != gametypes.ACCOUNT_TYPE_URS:
            msg = uiUtils.getTextFromGMD(GMDD.data.CBG_OPEN_URL_HINT, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=p.base.fastLogonCbg, noCallback=self.hide)
            return
        self.entId = entId
        if self.isShowNewCbg():
            gameglobal.rds.ui.cbgMain.show(entId)
        else:
            gameglobal.rds.ui.loadWidget(self.treasureWidgetId, False, True)

    def isShowNewCbg(self):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableCBGRole', False):
            return False
        if gameglobal.rds.configData.get('enableCBGRoleWhiteList', False) and not utils.isCbgRoleSameWhiteGbId(p.gbId):
            return False
        return True

    def clearWidget(self):
        self.treasureMediator = None
        gameglobal.rds.ui.unLoadWidget(self.treasureWidgetId)

    def hide(self, destroy = True):
        self.onCloseTreasure()

    def reset(self):
        self.cbgDataOwn = {}
        self.cbgDataBought = {}
        self.cbgDataAll = []

    def showTreasureConfig(self):
        return gameglobal.rds.configData.get('enableCBG', True)

    def isTreasureNew(self):
        return self.isShowNewCbg()

    def onUpdateCbgDataOwn(self, event):
        if self.isTreasureNew():
            gameglobal.rds.ui.cbgMain.onUpdateCbgDataOwn(event)
        else:
            self.cbgDataOwn.update(event.data)
            self.refreshTresurePanel()

    def onUpdateCbgDataBought(self, event):
        if self.isTreasureNew():
            gameglobal.rds.ui.cbgMain.onUpdateCbgDataBought(event)
        else:
            self.cbgDataBought.update(event.data)
            self.refreshTresurePanel()

    def onReomveCbgDataOwn(self, event):
        if self.isTreasureNew():
            gameglobal.rds.ui.cbgMain.onReomveCbgDataOwn(event)
        else:
            cbgId = event.data.get('cbgId', 0)
            self.cbgDataOwn.pop(cbgId, None)
            self.refreshTresurePanel()

    def onRemoveCbgDataBought(self, event):
        if self.isTreasureNew():
            gameglobal.rds.ui.cbgMain.onRemoveCbgDataBought(event)
        else:
            cbgId = event.data.get('cbgId', 0)
            self.cbgDataBought.pop(cbgId, None)
            self.refreshTresurePanel()

    def onQueryCbgDataAll(self, event):
        if self.isTreasureNew():
            gameglobal.rds.ui.cbgMain.onQueryCbgDataAll(event)
        else:
            self.cbgDataAll = event.data
            self.refreshTresurePanel()

    @ui.uiEvent(uiConst.WIDGET_TREASURE_CONFIRM, events.EVENT_SELL_CASH_DONE)
    def onSellCashDone(self):
        self.onCloseConfirmWidget()
        if not self.treasureMediator:
            return
        self.treasureInfo.clear()
        self.treasureMediator.Invoke('sellCashDone')
        if self.autoGoHome:
            self.treasureMediator.Invoke('gotoHomePanel')

    def refreshTresurePanel(self):
        if self.treasureMediator:
            self.treasureMediator.Invoke('refreshSelTabContent')

    def genTreasureHomeInfo(self):
        ret = {}
        adInfo = CCD.data.get('treasureAdIcon', {})
        ret['adIcon'] = tianyuMallProxy.AD_ICON_TEMPLATE % adInfo.get('home', 'cbg_home')
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
        for k in self.cbgDataOwn:
            ci = self.cbgDataOwn[k]
            info = uiUtils.getGfxItemById(CASH_ITEM_ID, picSize=uiConst.ICON_SIZE40)
            info.update(ci)
            info['tradeType'] = const.CBG_SEARCH_TYPE_OWN
            info['itemName'] = str(int(ci['cnt'] / CBG_TRADE_UNIT)) + '万'
            info['tExpire'] = ci['tLong'] * const.TIME_INTERVAL_DAY - (utils.getNow() - ci['tBegin'])
            info['cbgId'] = k
            info['canOper'] = ci['opType'] == const.CBG_OP_TYPE_SELL
            ret.append(info)

        return ret

    def genBoughtCbgData(self):
        ret = []
        for k in self.cbgDataBought:
            ci = self.cbgDataBought[k]
            info = uiUtils.getGfxItemById(CASH_ITEM_ID, picSize=uiConst.ICON_SIZE40)
            info.update(ci)
            info['tradeType'] = const.CBG_SEARCH_TYPE_BUY
            info['itemName'] = str(int(ci['cnt'] / CBG_TRADE_UNIT)) + '万'
            info['tExpire'] = ci['tLong'] * const.TIME_INTERVAL_DAY - (utils.getNow() - ci['tBegin'])
            info['canOper'] = True
            info['cbgId'] = k
            ret.append(info)

        return ret

    def genTreasureBuyInfo(self):
        ret = {}
        ccdd = CCD.data
        infoList = []
        for i in range(len(self.cbgDataAll)):
            ci = self.cbgDataAll[i]
            info = uiUtils.getGfxItemById(CASH_ITEM_ID, picSize=uiConst.ICON_SIZE40)
            info['itemName'] = str(int(ci['cnt'] / CBG_TRADE_UNIT)) + '万'
            info['price'] = ci['price']
            info['itemType'] = ci['itemType']
            info['tExpire'] = ci['tLong'] * const.TIME_INTERVAL_DAY - (utils.getNow() - ci['tBegin'])
            info['singlePrice'] = self.getSinglePrice(ci['price'], ci['cnt'])
            if info['tExpire'] > 0:
                infoList.append(info)

        ret['infoList'] = infoList
        ret['buyTips'] = ccdd.get('buyTips', ())
        return ret

    def genTreasureSellInfo(self):
        ret = {}
        ccdd = CCD.data
        adInfo = ccdd.get('treasureAdIcon', {})
        ret['adIcon'] = tianyuMallProxy.AD_ICON_TEMPLATE % adInfo.get('sell', 'cbg_sell')
        ret['priceRange'] = ccdd.get('priceRange', (10, 300000))
        ret['cashRange'] = ccdd.get('cashRange', (10, 1000))
        ret['priceMaxChars'] = ccdd.get('priceMaxChars', 6)
        ret['cashMaxChars'] = ccdd.get('cashMaxChars', 4)
        ret['sellTips'] = ccdd.get('sellTips', ())
        ret['minPrice'] = 1.0 / CCD.data.get('maxSinglePrice', 5)
        ret['friendList'] = self.mall.getFriendList()
        ret.update(self.getColorConfigs())
        return ret

    def genTreasureConfirmInfo(self):
        ccdd = CCD.data
        ret = uiUtils.getGfxItemById(CASH_ITEM_ID, picSize=uiConst.ICON_SIZE40)
        ret['taxRate'] = ccdd.get('taxRate', 0.05)
        ret['taxRange'] = ccdd.get('taxRange', (1, 10000))
        ret.update(self.treasureInfo)
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

    def getSinglePrice(self, price, cnt):
        price = float(price)
        cnt = max(float(cnt), float(CBG_TRADE_UNIT))
        return price / CBG_RMB_UNIT / (cnt / CBG_TRADE_UNIT)

    @ui.uiEvent(uiConst.WIDGET_TREASURE, events.EVENT_CASH_CHANGED)
    def onMoneyInfoUpdate(self):
        if self.treasureMediator:
            self.treasureMediator.Invoke('refreshMyMoney')

    def onGetMyMoneyInfo(self, *arg):
        return uiUtils.dict2GfxDict(self.mall.getMyMoneyInfo(), True)

    def onGetTreasureInfo(self, *arg):
        ret = {}
        ret['home'] = self.genTreasureHomeInfo()
        ret['buy'] = self.genTreasureBuyInfo()
        ret['sell'] = self.genTreasureSellInfo()
        return uiUtils.dict2GfxDict(ret, True)

    def onCloseTreasure(self, *arg):
        self.entId = 0
        self.treasureInfo = {}
        self.autoGoHome = False
        gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.inventoryPassword.hide()
        self.onCloseConfirmWidget()
        self.clearWidget()

    def onOpenConfirmWidget(self, *arg):
        cash = int(arg[3][0].GetNumber()) * CBG_TRADE_UNIT
        price = arg[3][1].GetNumber() * CBG_RMB_UNIT
        targetRoleName = arg[3][2].GetString()
        targetRoleGbId = arg[3][3].GetString()
        singlePrice = self.getSinglePrice(price, cash)
        minPrice = 1.0 / CCD.data.get('maxSinglePrice', 5)
        if singlePrice < minPrice:
            gameglobal.rds.ui.messageBox.showMsgBox('云币寄售单价不能小于%s元/万云币，当前价格是%s元/万云币' % (round(minPrice, 4), round(singlePrice, 4)))
            return
        self.treasureInfo['cash'] = cash
        self.treasureInfo['price'] = price
        self.treasureInfo['targetRoleName'] = unicode2gbk(targetRoleName)
        self.treasureInfo['targetRoleGbId'] = unicode2gbk(targetRoleGbId)
        gameglobal.rds.ui.loadWidget(self.confirmWidgetId, True, True)

    def onCloseConfirmWidget(self, *arg):
        gameglobal.rds.ui.unLoadWidget(self.confirmWidgetId)
        self.confirmMediator = None

    @ui.callFilter(2, False)
    @ui.checkInventoryLock()
    def onConfirmSellItem(self, *arg):
        if not self.entId:
            return
        ent = BigWorld.entities.get(self.entId)
        if not ent:
            return
        if not self.treasureInfo:
            return
        self.autoGoHome = arg[3][0].GetBool()
        p = BigWorld.player()
        cash = int(self.treasureInfo['cash'])
        price = int(self.treasureInfo['price'])
        if self.treasureInfo['targetRoleGbId']:
            targetRoleGBID = int(self.treasureInfo['targetRoleGbId'])
        else:
            targetRoleGBID = 0
        interval = CCD.data.get('cbgInterval', (2,))
        ent.cell.sellCashInCBG(cash, targetRoleGBID, price, interval[0], p.cipherOfPerson)

    def onCancelCbgItem(self, *arg):
        tradeType = int(arg[3][0].GetNumber())
        cbgId = int(arg[3][1].GetNumber())
        if tradeType == const.CBG_SEARCH_TYPE_OWN:
            msg = '确定要撤销这笔挂单嘛?'
        else:
            msg = '确定要收取买到的云币嘛?'
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onConfirmCancelCbgItem, tradeType, cbgId))

    def onOpenTreasureWeb(self, *arg):
        cbgUrl = 'http://tianyu.cbg.163.com'
        BigWorld.openUrl(cbgUrl)

    @ui.callFilter(15, False)
    def onQueryAllData(self, *arg):
        BigWorld.player().base.queryAllCbgData()

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

    @ui.uiEvent(uiConst.WIDGET_TREASURE, events.EVENT_TAKE_BACK_FAILED)
    def onTakeBackCBGCashFailed(self):
        msg = '需要在藏宝阁网站下架后，才能撤销并取回云币，确认去网站下架嘛?'
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onOpenTreasureWeb))
