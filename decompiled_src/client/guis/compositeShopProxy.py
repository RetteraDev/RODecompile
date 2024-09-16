#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/compositeShopProxy.o
from gamestrings import gameStrings
import copy
import BigWorld
from Scaleform import GfxValue
import const
import keys
import gameglobal
import gametypes
import uiConst
import commShop
import utils
import gamelog
from item import Item
from uiProxy import SlotDataProxy
from guis import ui
from callbackHelper import Functor
from appSetting import Obj as AppSettings
from guis import uiUtils
from guis import compositeShopHelpFunc
from ui import gbk2unicode
from helpers import capturePhoto
from helpers import charRes
from gamestrings import gameStrings
from cdata import game_msg_def_data as GMDD
from cdata import composite_shop_trade_data as CSTD
from data import item_data as ID
from data import sys_config_data as SCD
from data import composite_shop_data as CSD
from data import composite_shop_item_set_data as CSISD
from data import fame_data as FD
MAOXIANJIA_FAMEID = 410

class CompositeShopProxy(SlotDataProxy):
    OPTION_SHOP = 0
    OPTION_BUY_BACK = 99
    OPTION_SHOP_BUY_BACK = 100
    MAX_PAGE_ITEM_NUM = 36

    def __init__(self, uiAdapter):
        super(CompositeShopProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeShop': self.onCloseShop,
         'changePage': self.onChangePage,
         'getPageCount': self.onGetPageCount,
         'buyItem': self.onBuyItem,
         'fitting': self.onFitting,
         'setBuyItem': self.onSetBuyItem,
         'setBuyItemNum': self.onSetBuyItemNum,
         'clickBuyItemMaxNum': self.onClickBuyItemMaxNum,
         'setDiJiaItemNum': self.onSetDiJiaItemNum,
         'clickDiJiaItemMaxNum': self.onClickDiJiaItemMaxNum,
         'getDiJiaInfo': self.onGetDiJiaInfo,
         'getConsumeMaxNum': self.onGetConsumeMaxNum,
         'setOption': self.onSetOption,
         'getOption': self.onGetOption,
         'buyBackItem': self.onBuyBackItem,
         'confirmSelectChange': self.onConfirmSelectChange,
         'rotateFigure': self.onRotateFigure,
         'canShowFashion': self.onCanShowFashion,
         'showFashion': self.onShowFashion,
         'closeFashion': self.onCloseFashion,
         'getBuyBackShopFlag': self.onGetBuyBackShopFlag,
         'isShowShopBuyBackTab': self.onIsShowShopBuyBackTab,
         'startView': self.onStartView,
         'getCompositeType': self.onGetCompositeType,
         'getItemPosList': self.onGetItemPosList,
         'getMaxBtnTips': self.onGetMaxBtnTips}
        self.DIJIA_ITEM_TO_FAME = 0
        self.DIJIA_ITEM_TO_ITEM = 1
        self.bindType = 'compositeShop'
        self.type = 'compositeShop'
        self.mediator = None
        self.isOpen = False
        self.shopItemInfo = {}
        self.buyBackItemInfo = {}
        self.page = None
        self.pos = None
        self.currPage = None
        self.currPageShow = 0
        self.buyBackCurrPage = None
        self.buyBackPageStamp = {}
        self.npcId = None
        self.pageStamp = {}
        self.diJiaItemNum = 0
        self.diJiaItemToItemNum = 0
        self.buyItemNum = 1
        self.itemPage = None
        self.dijiaItem = None
        self.option = -1
        self.headGen = None
        self.buybackShopId = 0
        self.buyBackItemList = []
        self.buyBackItemIdList = []
        self.customDict = {}
        self.pageList = {}
        self.compositeShopType = 0
        self.lastPage = 0
        self.lastStamp = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_COMPOSITE_SHOP, Functor(self.hide, None))
        self.confirmStatus = AppSettings.get(keys.SET_COMPOSITE_SHOP_CONFIRM, 'Default')
        if self.confirmStatus == 'Default':
            self.confirmStatus = False
            AppSettings[keys.SET_COMPOSITE_SHOP_CONFIRM] = self.confirmStatus
            AppSettings.save()
        else:
            self.confirmStatus = self.confirmStatus == 'True'

    def onStartView(self, *args):
        if not self.mediator:
            return
        else:
            self.mediator.Invoke('updateCheckBox', GfxValue(self.confirmStatus))
            nameArray = []
            self.pageList = {}
            i = 0
            customDictkeys = sorted(self.customDict.keys())
            for key in customDictkeys:
                if len(self.customDict[key]) > 0:
                    nameArray.append(key[3:])
                    self.pageList[i] = self.customDict[key]
                    i = i + 1

            if self.itemPage:
                self.mediator.Invoke('setPageItem', self.itemPage)
                self.itemPage = None
            self.initTab(nameArray)
            return

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_COMPOSITE_SHOP:
            self.mediator = mediator

    def onSetOption(self, *arg):
        self.setOption(int(arg[3][0].GetNumber()))

    def setOption(self, option, currPage = 0):
        if self.option == option:
            return
        p = BigWorld.player()
        self.option = option
        if self.option != self.OPTION_BUY_BACK:
            ent = BigWorld.entities.get(self.npcId)
            self.currPage = self.pageList[option][currPage]
            stamp = self.pageStamp.get(self.currPage, 0)
            if ent:
                ent.cell.compositeShopTurnPage(BigWorld.player().openShopId, self.currPage, stamp)
            elif self.isPrivateShop():
                p.compositeShopTurnPage(BigWorld.player().openShopId, self.currPage, stamp)
        elif self.option == self.OPTION_BUY_BACK:
            self._setBuyBackItem()
            if self.mediator:
                self.mediator.Invoke('hideExtra')

    def onGetOption(self, *arg):
        return GfxValue(self.option)

    def onIsShowShopBuyBackTab(self, *arg):
        enableBuyBackTab = gameglobal.rds.configData.get('enableBuyBackTab', False)
        return GfxValue(enableBuyBackTab)

    def onGetBuyBackShopFlag(self, *arg):
        return GfxValue(False)

    def updateBuyBackItem(self):
        if self.option != self.OPTION_BUY_BACK:
            return
        self._setBuyBackItem()

    def setPageCount(self):
        self.mediator.Invoke('setPageCount', GfxValue(self.pageCount))

    def _calcConsumeCash(self, compositeData, buyNum = 0):
        cash = 0
        bindCash = 0
        consumeCash = compositeData.get('consumeCash', 0)
        if consumeCash == 0:
            return (cash, bindCash)
        consumeCashType = compositeData.get('cashType', gametypes.CONSUME_CASH_TYPE_NO_LIMIT)
        if buyNum == 0:
            consumeCash *= self.buyItemNum
        else:
            consumeCash *= buyNum
        p = BigWorld.player()
        if consumeCashType == gametypes.CONSUME_CASH_TYPE_NO_LIMIT:
            bindCash = min(consumeCash, p.bindCash)
            cash = max(consumeCash - bindCash, 0)
        elif consumeCashType == gametypes.CONSUME_CASH_TYPE_BIND_CASH:
            bindCash = consumeCash
        elif consumeCashType == gametypes.CONSUME_CASH_TYPE_CASH:
            cash = consumeCash
        return (cash, bindCash)

    @ui.callAfterTime()
    def refreshBuyItemDisplayData(self):
        self.refreshBuyItemDisplayDataNow()

    def refreshBuyItemDisplayDataNow(self):
        if self.mediator:
            compositeData = self._getCompositeData()
            if not compositeData:
                return
            newConsumeInfo = self.getNewConsumeInfo()
            self.mediator.Invoke('refreshConsumeInfo', uiUtils.dict2GfxDict(newConsumeInfo, True))

    def getNewConsumeInfo(self):
        p = BigWorld.player()
        compositeId = self.getCompositeId()
        itemNum = self.buyItemNum if self.buyItemNum > 0 else 1
        totalConsumeInfo = compositeShopHelpFunc.getConsumeInfo(compositeId, itemNum, self.diJiaItemNum, self.diJiaItemToItemNum, True)
        consumeCash = totalConsumeInfo['consumeCash']
        consumeBindCash = totalConsumeInfo['consumeBindCash']
        consumeItemInfo = totalConsumeInfo['conditionList']
        consumeDiJiaInfo = totalConsumeInfo['consumeDiJiaInfo']
        isValid = totalConsumeInfo['isValid']
        consumeInfo = {'cash': consumeCash,
         'bindCash': consumeBindCash,
         'playerCash': p.cash,
         'playerBindCash': p.bindCash,
         'consumeItem': consumeItemInfo,
         'consumeDiJiaInfo': consumeDiJiaInfo,
         'isValid': isValid}
        return consumeInfo

    def getColorFrameFlag(self, page, pos):
        if self.option != self.OPTION_BUY_BACK:
            item = self.shopItemInfo[page][pos]
        p = BigWorld.player()
        compositeData = CSTD.data.get(item.compositeId, {})
        schReq = ID.data.get(item.id, {}).get('schReq', ())
        if schReq and p.school not in schReq:
            return False
        if compositeData.has_key('sexLimit'):
            sexLimit = compositeData['sexLimit']
            if p.realPhysique.sex != sexLimit:
                return False
        return True

    def _isValidShopItemPos(self, page, pos):
        try:
            self.shopItemInfo[page][pos]
        except:
            return False

        return True

    def hasSelectedShopItem(self):
        try:
            self.shopItemInfo[self.page][self.pos]
        except:
            return False

        return True

    @ui.callFilter(0.5, False)
    def onBuyBackItem(self, *arg):
        pos = int(arg[3][0].GetNumber())
        ent = BigWorld.entity(self.npcId)
        if self.isPrivateShop():
            BigWorld.player().base.compositeShopRetrieve(BigWorld.player().openShopId, pos)
            return
        elif ent == None or pos < 0:
            return
        else:
            ent.cell.compositeShopRetrieve(BigWorld.player().openShopId, pos)
            return

    def onSetBuyItem(self, *arg):
        PurPage = int(arg[3][0].GetNumber())
        if self.option != self.OPTION_BUY_BACK:
            if self.option < len(self.pageList) and PurPage < len(self.pageList[self.option]):
                page = self.pageList[self.option][PurPage]
            else:
                return
        else:
            page = PurPage
        pos = int(arg[3][1].GetNumber())
        self.page = page
        self.pos = pos
        self.buyItemNum = 1
        self.diJiaItemNum = 0
        self.diJiaItemToItemNum = 0
        if self._isValidShopItemPos(page, pos):
            self.refreshBuyItemDisplayDataNow()

    def getSlotID(self, key):
        return (self.currPage, int(key[18:]))

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        if self.option != self.OPTION_BUY_BACK:
            if pos == self.MAX_PAGE_ITEM_NUM:
                it = self.shopItemInfo.get(self.page, {}).get(self.pos, None)
            else:
                if pos == self.MAX_PAGE_ITEM_NUM + 1:
                    it = self.dijiaItem
                    if not it:
                        return GfxValue('')
                    ret = gameglobal.rds.ui.inventory.GfxToolTip(it)
                    return ret
                try:
                    it = self.shopItemInfo[page][pos]
                except:
                    return GfxValue('')

        elif self.option == self.OPTION_BUY_BACK:
            p = BigWorld.player()
            ent = BigWorld.entities.get(self.npcId)
            it = None
            if ent:
                it = p.buyBackDict[BigWorld.player().openShopId][pos]
            if it == None:
                return GfxValue('')
            ret = gameglobal.rds.ui.inventory.GfxToolTip(it)
            return ret
        if it:
            data = ID.data.get(it.id, {})
            if data.get('quality') == 0 and data.get('type') == Item.BASETYPE_EQUIP:
                it = Item(it.id)
        ret = gameglobal.rds.ui.inventory.GfxToolTip(it, const.ITEM_IN_COMPOSITESHOP)
        return ret

    def _getFameLv(self, fameId, fameVal):
        fd = FD.data.get(fameId)
        ret = 1
        if fd.has_key('lvUpCondition'):
            lvUpCondition = fd.get('lvUpCondition', [])
            if lvUpCondition:
                lvArray = lvUpCondition[1].items()
            else:
                lvArray = []
        else:
            lvArray = fd.get('lvUpNeed', {}).items()
        lvArray.sort(key=lambda k: k[1], reverse=True)
        for key, val in lvArray:
            if fameVal >= val:
                ret = key + 1
                break

        return (ret, fameVal - val)

    def onGetPageCount(self, *arg):
        if self.option != self.OPTION_BUY_BACK:
            self.isOpen = True
            self.updateCheckBox()
            return GfxValue(len(self.pageList[self.option]))

    def refreshMoney(self):
        if self.mediator != None:
            self.mediator.Invoke('refreshMoney')

    @ui.callInCD(0.2)
    def openShop(self, npcId, compositeShopId, pageCount, customDict, buybackShopPageCount = 0, layoutType = uiConst.LAYOUT_DEFAULT):
        yunChuiShopProxy = gameglobal.rds.ui.yunChuiShop
        yunChuiShopProxy.npcId = npcId
        yunChuiShopProxy.shopId = compositeShopId
        if yunChuiShopProxy.needOpen(compositeShopId):
            yunChuiShopProxy.openShop(npcId, compositeShopId, pageCount, customDict, buybackShopPageCount, layoutType)
            return True
        else:
            self.npcId = npcId
            BigWorld.player().openShopId = compositeShopId
            BigWorld.player().openShopType = const.SHOP_TYPE_COMPOSITE
            self.pageCount = pageCount
            self.buybackPageCount = buybackShopPageCount
            self.pageStamp = {}
            self.buyBackPageStamp = {}
            self.currPage = 0
            self.currPageShow = 0
            self.buyBackCurrPage = 0
            self.diJiaItemNum = 0
            self.diJiaItemToItemNum = 0
            self.buyItemNum = 1
            self.isOpen = True
            self.customDict = customDict
            self.compositeShopType = CSD.data.get(compositeShopId, {}).get('compositeShopType', -1)
            if not self.mediator:
                self.uiAdapter.loadWidget(uiConst.WIDGET_COMPOSITE_SHOP, layoutType=layoutType)
            elif self.isPrivateShop():
                BigWorld.player().compositeShopTurnPage(compositeShopId, self.currPage, None)
            return True

    def closeShop(self):
        self.hide()

    def clearWidget(self):
        self.mediator = None
        self.isOpen = False
        self.pageStamp = {}
        self.buyBackPageStamp = {}
        self.diJiaItemNum = 0
        self.diJiaItemToItemNum = 0
        self.page = None
        self.pos = None
        self.currPage = None
        self.currPageShow = 0
        self.buyBackCurrPage = None
        self.option = -1
        BigWorld.player().openShopId = 0
        BigWorld.player().openShopType = 0
        self.buyItemNum = 1
        self.buyBackItemList = []
        self.buyBackItemIdList = []
        self.lastPage = 0
        self.lastStamp = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_COMPOSITE_SHOP)
        if self.npcId:
            ent = BigWorld.entity(self.npcId)
            if ent:
                ent.cell.closeCompositeShop(BigWorld.player().openShopId)
        else:
            BigWorld.player().base.closePrivateShop(BigWorld.player().openShopId)
        self.uiAdapter.playLeaveAction(self.npcId)
        if gameglobal.rds.ui.funcNpc.isOnFuncState() and self.npcId:
            gameglobal.rds.ui.funcNpc.close()
        if gameglobal.rds.ui.compositeShopConfirm.mediator:
            gameglobal.rds.ui.compositeShopConfirm.hide()
        self.npcId = 0

    def onCloseShop(self, *arg):
        yunChuiShopProxy = gameglobal.rds.ui.yunChuiShop
        if yunChuiShopProxy.mediator:
            yunChuiShopProxy.hide()
            return
        self.hide()

    def onChangePage(self, *arg):
        ent = BigWorld.entities.get(self.npcId)
        if BigWorld.player().openShopId:
            if self.option != self.OPTION_BUY_BACK:
                self.currPage = self.pageList[self.option][int(arg[3][0].GetNumber())]
                self.currPageShow = int(arg[3][0].GetNumber())
                stamp = self.pageStamp.get(self.currPage, 0)
                if self.isPrivateShop():
                    BigWorld.player().compositeShopTurnPage(BigWorld.player().openShopId, self.currPage, stamp)
                elif ent:
                    ent.cell.compositeShopTurnPage(BigWorld.player().openShopId, self.currPage, stamp)

    def getBuyBackPrice(self, buybackShopId, itemId):
        sFamePrice = 0
        sPrice = 0
        itemRecord = ID.data.get(itemId, '')
        if itemRecord == '':
            return (sFamePrice, sPrice)
        famePriceDict = itemRecord.get('buybackFamePrice') or itemRecord.get('famePrice', '')
        if famePriceDict != '':
            for key in famePriceDict.keys():
                if buybackShopId in key:
                    fameData = famePriceDict[key]
                    fameId = fameData[0]
                    sFamePrice = fameData[1]
                    if len(fameData) > 2:
                        fprices = fameData[2]
                        fameLv = BigWorld.player().getFameLv(fameId)
                        for i in xrange(0, len(fprices), 2):
                            if fameLv >= fprices[i]:
                                sFamePrice = fprices[i + 1]
                            else:
                                break

                    break

        sPrice = itemRecord['sPrice']
        return (sFamePrice, sPrice)

    def refreshPageItem(self, shopInv):
        gamelog.info('@jbx:refreshPageItem')
        if not self.mediator:
            return
        itemInfo = shopInv.pages[self.lastPage]
        self.setNormalPageItem(BigWorld.player().openShopId, self.lastPage, self.lastStamp, itemInfo, True)

    def setNormalPageItem(self, compositeShopId, page, stamp, itemInfo = None, forceUpdate = False):
        if gameglobal.rds.ui.yunChuiShop.needOpen(compositeShopId):
            gameglobal.rds.ui.yunChuiShop.setNormalPageItem(page, stamp, itemInfo, forceUpdate)
            return
        else:
            if self.option != self.OPTION_BUY_BACK:
                if itemInfo != None:
                    self.shopItemInfo[page] = {}
                    pos = 0
                    for item in itemInfo:
                        self.shopItemInfo[page][pos] = item
                        pos += 1

                pageInfo = self.shopItemInfo[page]
                self.pageStamp[page] = stamp
                self.currPage = page
                self.setPageItem(page, stamp, pageInfo)
            return

    def isPrivateShop(self):
        return self.mediator and self.npcId == 0

    def _getLimitStr(self, item):
        ret = ''
        if hasattr(item, 'compositeId'):
            buyLimitType = CSTD.data.get(item.compositeId, {}).get('buyLimitType', 0)
            buyLimitCount = CSTD.data.get(item.compositeId, {}).get('buyLimitCount', -1)
            if buyLimitType != const.COMPOSITE_BUY_LIMIT_TYPE_NO:
                remainBuyCount = max(0, compositeShopHelpFunc.getCompositeRemainBuyCount(item))
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
                elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_FAMOUS_GENERAL_SEASON:
                    ret = gameStrings.TEXT_COMPOSITESHOPPROXY_538 % (remainBuyCountStr, buyLimitCount)
                elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_ENDLESS_CHALLENGE_SEASON:
                    ret = gameStrings.TEXT_COMPOSITESHOPPROXY_538 % (remainBuyCountStr, buyLimitCount)
                elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_SPRITE_CHALLENGE_SEASON:
                    ret = gameStrings.TEXT_COMPOSITESHOPPROXY_538 % (remainBuyCountStr, buyLimitCount)
                elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_PUBG_SEASON:
                    ret = gameStrings.PUBG_COMPOSITE_SHOP_SEASON_BUY_LIMIT_DES % (remainBuyCountStr, buyLimitCount)
        return ret

    def _getLimitStrDesc(self, item):
        buyLimitDesc = ''
        if hasattr(item, 'compositeId'):
            buyLimitType = CSTD.data.get(item.compositeId, {}).get('buyLimitType', 0)
            buyLimitCount = CSTD.data.get(item.compositeId, {}).get('buyLimitCount', -1)
            if buyLimitType != const.COMPOSITE_BUY_LIMIT_TYPE_NO and buyLimitCount != -1:
                buyLimitDesc = gameStrings.TEXT_COMPOSITESHOPPROXY_553 % CSTD.data.get(item.compositeId, {}).get('buyLimitDesc', '')
        return buyLimitDesc

    @ui.callAfterTime()
    def refreshInfoByCache(self):
        if not self.mediator:
            return
        if self.option != self.OPTION_BUY_BACK:
            stamp = self.pageStamp.get(self.currPage, 0)
            pageInfo = self.shopItemInfo.get(self.currPage, {})
            self.setPageItem(self.currPage, stamp, pageInfo)

    def setPageItem(self, page, stamp, pageInfo):
        itemArray = []
        p = BigWorld.player()
        questItemIdList = p.getUnfinishedQuestNeedItemIdList()
        self.lastPage = page
        self.lastStamp = stamp
        for pos in xrange(len(pageInfo)):
            it = pageInfo[pos]
            if not it:
                continue
            data = ID.data.get(it.id, {})
            if data.get('quality') == 0 and data.get('type') == Item.BASETYPE_EQUIP:
                it = Item(it.id)
            itemInfo = uiUtils.getGfxItem(it)
            itemInfo['name'] = uiUtils.getItemColorNameByItem(it)
            itemInfo['value'] = str(it.bPrice)
            itemInfo['limitStr'] = self._getLimitStr(it)
            itemInfo['limitStrDesc'] = self._getLimitStrDesc(it)
            itemInfo['count'] = 999 if it.remainNum == const.ITEM_NUM_INFINITE else it.remainNum
            itemInfo['hasDiKou'] = compositeShopHelpFunc.hasDiJiaInfo(it.compositeId)
            itemInfo['maxCnt'] = compositeShopHelpFunc.getMaxBuyCnt(it)
            if not self.getColorFrameFlag(page, pos):
                itemInfo['state'] = uiConst.EQUIP_NOT_USE
            else:
                itemInfo['state'] = uiConst.ITEM_NORMAL
                itemInfo['questionMark'] = CSTD.data.get(it.compositeId, {}).get('questionMark', 0)
            itemInfo['priceType'] = data.get('bPriceType', gametypes.ITEM_PRICE_TYPE_BIND_CASH)
            if self.option == self.OPTION_SHOP_BUY_BACK:
                sFamePrice, sPrice = self.getBuyBackPrice(self.buybackShopId, it.id)
                itemInfo['sFameprice'] = sFamePrice
                itemInfo['sPrice'] = sPrice
            itemInfo['questFlagVisible'] = it.id in questItemIdList
            itemArray.append(itemInfo)

        otherInfo = {}
        otherInfo['cash'] = str(p.cash)
        otherInfo['bindCash'] = str(p.bindCash)
        otherInfo['page'] = page + 1
        itemArray.append(otherInfo)
        if self.mediator:
            self.mediator.Invoke('setPageItem', uiUtils.array2GfxAarry(itemArray, True))
        else:
            self.itemPage = uiUtils.array2GfxAarry(itemArray, True)

    def _setBuyBackItem(self):
        p = BigWorld.player()
        ent = BigWorld.entities.get(self.npcId)
        compositeShopId = BigWorld.player().openShopId
        if compositeShopId in p.buyBackDict:
            itemList = p.buyBackDict[compositeShopId]
        else:
            itemList = []
        itemArray = []
        for it in itemList:
            if it == None:
                continue
            data = ID.data.get(it.id, {})
            itemInfo = uiUtils.getGfxItem(it)
            itemInfo['name'] = uiUtils.getItemColorNameByItem(it)
            canSell, fameData = it.canSellToCompositeShopId(p.openShopId)
            if canSell:
                itemInfo['value'] = fameData[1]
                itemInfo['priceType'] = fameData[0]
                itemInfo['tipsInfo'] = FD.data.get(fameData[0], {}).get('name', '')
                itemInfo['isEnough'] = fameData[1] <= p.fame.get(fameData[0], 0)
            else:
                itemInfo['value'] = str(it.sPrice)
                itemInfo['priceType'] = data.get('sPriceType', gametypes.ITEM_PRICE_TYPE_BIND_CASH)
            if not it.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
                itemInfo['state'] = uiConst.EQUIP_NOT_USE
            else:
                itemInfo['state'] = uiConst.ITEM_NORMAL
            itemArray.append(itemInfo)

        otherInfo = {}
        otherInfo['cash'] = str(p.cash)
        otherInfo['bindCash'] = str(p.bindCash)
        otherInfo['page'] = 0
        itemArray.append(otherInfo)
        self.mediator.Invoke('setPageItem', uiUtils.array2GfxAarry(itemArray, True))

    def setSingleItem(self, page, pos, item):
        if page == self.currPage and self.mediator:
            if self.option != self.OPTION_SHOP_BUY_BACK:
                if self.shopItemInfo:
                    it = self.shopItemInfo.get(page, {}).get(pos)
                    if not it:
                        it = item
                    num = item.remainNum
                    if num == const.ITEM_NUM_INFINITE:
                        num = 999
                    it.remainNum = num
                    if not self.shopItemInfo.get(page):
                        self.shopItemInfo[page] = {}
                    self.shopItemInfo[page][pos] = it
                    self.mediator.Invoke('setSingleItem', (GfxValue(page), GfxValue(pos), GfxValue(num)))
            elif self.buyBackItemInfo:
                it = self.buyBackItemInfo.get(page, {}).get(pos)
                if not it:
                    it = item
                num = item.remainNum
                if num == const.ITEM_NUM_INFINITE:
                    num = 999
                it.remainNum = num
                if not self.buyBackItemInfo.get(page):
                    self.buyBackItemInfo[page] = {}
                self.buyBackItemInfo[page][pos] = it
                self.mediator.Invoke('setBuyBackSingleItem', (GfxValue(page), GfxValue(pos), GfxValue(num)))

    def refreshBuyLimitInfo(self):
        if not self.mediator:
            return
        if self.option != self.OPTION_SHOP_BUY_BACK:
            if self.shopItemInfo:
                itemList = []
                pageInfo = self.shopItemInfo.get(self.currPage, {})
                for pos in pageInfo.iterkeys():
                    it = self.shopItemInfo.get(self.currPage, {}).get(pos)
                    itemInfo = {}
                    itemInfo['pos'] = pos
                    itemInfo['limitStr'] = self._getLimitStr(it)
                    itemList.append(itemInfo)

                self.mediator.Invoke('refreshBuyLimitInfo', uiUtils.array2GfxAarry(itemList, True))

    def _checkdiJiaItem(self, compositeData):
        diJiaType = self._getDijiaType()
        if diJiaType == self.DIJIA_ITEM_TO_FAME and self.diJiaItemNum == 0:
            return True
        if diJiaType == self.DIJIA_ITEM_TO_ITEM and self.diJiaItemToItemNum == 0:
            return True
        p = BigWorld.player()
        diJiaItemId = self._getDijiaItemId()
        if diJiaItemId == 0:
            return True
        curCnt = p.inv.countItemInPages(diJiaItemId, enableParentCheck=True)
        if self.diJiaItemNum > curCnt:
            p.showGameMsg(GMDD.data.COMPOSITE_SHOP_BUY_FORBIDDEN_DIJIA_ITEM_NUM, ())
            return False
        return True

    def onFitting(self, *arg):
        p = BigWorld.player()
        page = int(arg[3][0].GetNumber())
        pos = int(arg[3][1].GetNumber())
        page = self.pageList[self.option][page]
        if not self._isValidShopItemPos(page, pos):
            p.showGameMsg(GMDD.data.COMPOSITE_SHOP_BUY_FORBIDDEN_CHOOSE_ITEM, ())
            return
        else:
            it = self.shopItemInfo.get(self.currPage, {}).get(pos, None)
            if it:
                gameglobal.rds.ui.fittingRoom.addItem(it)
            return

    @ui.callFilter(0.5, False)
    def onBuyItem(self, *arg):
        p = BigWorld.player()
        if not self._isValidShopItemPos(self.page, self.pos):
            p.showGameMsg(GMDD.data.COMPOSITE_SHOP_BUY_FORBIDDEN_CHOOSE_ITEM, ())
            return
        else:
            compositeShopId = getattr(p, 'openShopId', 0)
            alertMessage = CSD.data.get(compositeShopId, {}).get('alertMessage', None)
            if alertMessage:
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(alertMessage, self.realBuyItem)
            else:
                self.realBuyItem()
            return

    def realBuyItem(self):
        p = BigWorld.player()
        itemNum = self.buyItemNum
        item = self.shopItemInfo[self.page][self.pos]
        npcEnt = BigWorld.entities.get(self.npcId, None)
        if compositeShopHelpFunc.buyItem(p.openShopId, item, itemNum, self.diJiaItemNum, self.diJiaItemToItemNum, self.page, self.pos, npcEnt):
            self.setOption(self.option, self.currPageShow)
            self.mediator.Invoke('clearClickDiJiaNum', ())

    def onSetBuyItemNum(self, *arg):
        self.buyItemNum = int(arg[3][0].GetNumber())
        self.refreshBuyItemDisplayData()

    def _findMaxItemNumCanBuy(self, shopItem, compositeData):
        p = BigWorld.player()
        if not commShop._checkCompositeShopPreLimit(p, compositeData, self.buyItemNum):
            return 0
        if not self._checkdiJiaItem(compositeData):
            return 0
        if shopItem.remainNum == 0:
            return 0
        maxNum = shopItem.remainNum
        if maxNum < 0:
            maxNum = ID.data.get(shopItem.id, {}).get('mwrap', 1)
        while True:
            if commShop._checkBuyItemConsume(p, compositeData, maxNum, self.diJiaItemNum, 0, False):
                return maxNum
            maxNum -= 1
            if maxNum == 0:
                break

        return 0

    def onClickBuyItemMaxNum(self, *arg):
        try:
            shopItem = self.shopItemInfo[self.page][self.pos]
        except:
            return

        compositeId = shopItem.compositeId
        if not CSTD.data.has_key(compositeId):
            return False
        compositeData = CSTD.data.get(compositeId, {})
        maxItemNum = self._findMaxItemNumCanBuy(shopItem, compositeData)
        self.buyItemNum = maxItemNum
        self.mediator.Invoke('setBuyItemMaxNum', GfxValue(maxItemNum))
        self.refreshBuyItemDisplayData()

    def _getCompositeData(self):
        try:
            shopItem = self.shopItemInfo[self.page][self.pos]
        except:
            return None

        if not shopItem:
            return False
        else:
            compositeId = shopItem.compositeId
            if not CSTD.data.has_key(compositeId):
                return False
            compositeData = CSTD.data.get(compositeId, {})
            return compositeData

    def getCompositeId(self):
        try:
            shopItem = self.shopItemInfo[self.page][self.pos]
        except:
            return None

        return shopItem.compositeId

    def onSetDiJiaItemNum(self, *arg):
        diJiaType = self._getDijiaType()
        if diJiaType == self.DIJIA_ITEM_TO_FAME:
            self.diJiaItemNum = int(arg[3][0].GetNumber())
            self.diJiaItemToItemNum = 0
        elif diJiaType == self.DIJIA_ITEM_TO_ITEM:
            self.diJiaItemNum = 0
            self.diJiaItemToItemNum = int(arg[3][0].GetNumber())
        self.refreshBuyItemDisplayData()

    def onClickDiJiaItemMaxNum(self, *arg):
        compositeData = self._getCompositeData()
        if not compositeData:
            return
        diJiaItemId = self._getDijiaItemId()
        if diJiaItemId == 0:
            return
        diJiaType = self._getDijiaType()
        if diJiaType == self.DIJIA_ITEM_TO_FAME:
            dijiaConfigMaxNum = compositeData.get('diJiaItemMaxNum', 0)
        elif diJiaType == self.DIJIA_ITEM_TO_ITEM:
            dijiaConfigMaxNum = compositeData.get('diJiaSrcMaxNum', 0)
        diJiaItemMaxNum = dijiaConfigMaxNum * self.buyItemNum
        if diJiaItemMaxNum == 0:
            return
        p = BigWorld.player()
        invDiJiaItemNum = p.inv.countItemInPages(diJiaItemId, enableParentCheck=True)
        res = min(diJiaItemMaxNum, invDiJiaItemNum)
        if diJiaType == self.DIJIA_ITEM_TO_FAME:
            self.diJiaItemNum = res
            self.diJiaItemToItemNum = 0
        elif diJiaType == self.DIJIA_ITEM_TO_ITEM:
            self.diJiaItemToItemNum = res
            self.diJiaItemNum = 0
        self.mediator.Invoke('setDiJiaItemMaxNum', GfxValue(res))
        self.refreshBuyItemDisplayData()

    def onGetDiJiaInfo(self, *arg):
        return uiUtils.dict2GfxDict(self.getDiJiInfo(), True)

    def getDiJiInfo(self):
        ret = {}
        if not self.hasSelectedShopItem():
            return ret
        compositeData = self._getCompositeData()
        if not compositeData:
            return ret
        diJiaItemId = self._getDijiaItemId()
        if diJiaItemId == 0:
            return ret
        diJiaType = self._getDijiaType()
        if diJiaType == self.DIJIA_ITEM_TO_FAME:
            diJiaItemMaxNum = compositeData.get('diJiaItemMaxNum', 0)
        elif diJiaType == self.DIJIA_ITEM_TO_ITEM:
            diJiaItemMaxNum = compositeData.get('diJiaSrcMaxNum', 0)
        if diJiaItemMaxNum == 0:
            return ret
        item = Item(diJiaItemId)
        self.dijiaItem = item
        self.diJiaItemNum = 0
        self.diJiaItemToItemNum = 0
        ret = {'diJiaItemNumLimit': diJiaItemMaxNum * self.buyItemNum}
        return ret

    def onGetConsumeMaxNum(self, *arg):
        try:
            item = self.shopItemInfo[self.page][self.pos]
        except:
            return GfxValue(0)

        ret = compositeShopHelpFunc.getConsumeMaxNum(item)
        return GfxValue(ret)

    def onConfirmSelectChange(self, *arg):
        confirmStatus = arg[3][0].GetBool()
        self.confirmStatus = confirmStatus
        AppSettings[keys.SET_COMPOSITE_SHOP_CONFIRM] = self.confirmStatus
        AppSettings.save()
        gameglobal.rds.ui.compositeShopConfirm.updateCheckBox()

    def updateCheckBox(self):
        if not self.mediator:
            return
        self.mediator.Invoke('updateCheckBox', GfxValue(self.confirmStatus))

    def onRotateFigure(self, *arg):
        index = arg[3][0].GetNumber()
        deltaYaw = -0.104 * index
        if self.headGen:
            self.headGen.rotateYaw(deltaYaw)

    def onCanShowFashion(self, *arg):
        return GfxValue(False)

    def onShowFashion(self, *arg):
        pass

    def _showFashion(self):
        item = self.shopItemInfo[self.page][self.pos]
        p = BigWorld.player()
        physique = copy.deepcopy(p.realPhysique)
        aspect = copy.deepcopy(p.realAspect)
        parts = list(item.whereEquip())
        parts.extend(uiUtils.getAspectParts(item.id))
        for part in parts:
            aspect.set(part, item.id)

        mpr = charRes.MultiPartRes()
        mpr.queryByAttribute(physique, aspect, True, p.avatarConfig)
        res = mpr.getPrerequisites()
        self.initHeadGen()
        self.takePhoto3D(res)

    def onCloseFashion(self, *arg):
        self.resetHeadGen()

    def takePhoto3D(self, res):
        if not self.headGen:
            self.headGen = capturePhoto.ShopPhotoGen.getInstance('gui/taskmask.tga', 442)
        self.headGen.startCaptureEntAndRes(BigWorld.player(), res)

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.ShopPhotoGen.getInstance('gui/taskmask.tga', 442)
        self.headGen.initFlashMesh()

    def initTab(self, tabNameArray):
        self.mediator.Invoke('setTabArray', uiUtils.array2GfxAarry(tabNameArray, True))
        self.mediator.Invoke('setTextBtnState', GfxValue(0))

    def _getDijiaType(self):
        compositeData = self._getCompositeData()
        if not compositeData:
            return self.DIJIA_ITEM_TO_ITEM
        diJiaItemid = compositeData.get('diJiaItemid', 0)
        diJiaSrcItemid = compositeData.get('diJiaSrcItemId', 0)
        if diJiaItemid > 0:
            return self.DIJIA_ITEM_TO_FAME
        if diJiaSrcItemid > 0:
            return self.DIJIA_ITEM_TO_ITEM
        return self.DIJIA_ITEM_TO_FAME

    def _getDijiaItemId(self):
        compositeData = self._getCompositeData()
        if not compositeData:
            return 0
        diJiaType = self._getDijiaType()
        if diJiaType == self.DIJIA_ITEM_TO_FAME:
            return compositeData.get('diJiaItemid', 0)
        if diJiaType == self.DIJIA_ITEM_TO_ITEM:
            return compositeData.get('diJiaSrcItemId', 0)

    def onGetCompositeType(self, *args):
        return GfxValue(self.compositeShopType)

    def onGetItemPosList(self, *args):
        itemPosList = []
        compositeSetId = CSD.data.get(BigWorld.player().openShopId, {}).get('compositeSetId', ())
        if compositeSetId and len(compositeSetId) >= self.currPage:
            compositeShopItemSetId = compositeSetId[self.currPage][1]
            itemPosList = CSISD.data.get(compositeShopItemSetId, [])
        return uiUtils.array2GfxAarry(itemPosList)

    def getPos(self, itemPos):
        return itemPos.get('compositeItemRow') * 6 + itemPos.get('compositeItemColumn')

    def getCompositeShopId(self):
        return BigWorld.player().openShopId

    def onGetMaxBtnTips(self, *args):
        str = SCD.data.get('compositeShopMaxBtnTips', 'compositeShopMaxBtnTips not found')
        return GfxValue(gbk2unicode(str))
