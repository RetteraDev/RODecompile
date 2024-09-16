#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/boothProxy.o
from gamestrings import gameStrings
import re
import time
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import gametypes
import utils
import uiUtils
import tipUtils
import item
import gameconfigCommon
from helpers import taboo
from guis import uiConst
from guis import pinyinConvert
from uiProxy import SlotDataProxy
from guis import menuManager
from ui import gbk2unicode
from ui import unicode2gbk
from item import Item
from guis import ui
from guis import events
from cdata import game_msg_def_data as GMDD
from data import item_data as ID
from cdata import font_config_data as FCD
from data import sys_config_data as SYCD
from data import booth_skin_data as BSD
UGCForceLimit = [89,
 64,
 8964,
 6489]

class BoothProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(BoothProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.bindType = 'booth'
        self.type = 'booth'
        self.modelMap = {'cancelBuy': self.onCancelBuy,
         'cancelSell': self.onCancelSell,
         'buy': self.onBuy,
         'fitting': self.onFitting,
         'sell': self.onSell,
         'openInventory': self.onOpenInventory,
         'getBuyItemInfo': self.onGetBuyItemInfo,
         'getSellItemInfo': self.onGetSellItemInfo,
         'closeRename': self.onCloseRename,
         'renameBooth': self.onRenameBooth,
         'requestSearch': self.onRequestSearch,
         'addBuy': self.onAddBuy,
         'reName': self.onReName,
         'closeBooth': self.onCloseBooth,
         'changePrice': self.onChangePrice,
         'showRecord': self.onShowRecord,
         'closeBoothWin': self.onCloseBoothWin,
         'getBoothInfo': self.onGetBoothInfo,
         'getDefaultName': self.onGetDefaultName,
         'confirmSell': self.onConfirmSell,
         'closeSellSetting': self.onCloseSellSetting,
         'confirmBuy': self.onConfirmBuy,
         'closeBuySetting': self.onCloseBuySetting,
         'getSearchList': self.onGetSearchList,
         'recieveItem': self.onRecieveItem,
         'closeQuantity': self.onCloseQuantity,
         'buyItem': self.onBuyItem,
         'confirmNumber': self.onConfirmNumber,
         'cancelNumber': self.onCancelNumber,
         'submitMessage': self.onSubmitMessage,
         'linkLeftClick': self.onLinkLeftClick,
         'clearSum': self.onClearSum,
         'clearChatlog': self.onClearChatlog,
         'closeBoothRecord': self.onCloseBoothRecord,
         'getBoothRecord': self.onGetBoothRecord,
         'getNumber': self.onGetNumber,
         'getBoothTax': self.onGetBoothTax,
         'getCustomPageInfo': self.onGetCustomPageInfo,
         'getCustomSelItem': self.onGetCustomSelItem,
         'getCustomItemNum': self.onGetCustomItemNum,
         'setCustomItem': self.onSetCustomItem,
         'closeCustomWin': self.onCloseCustomWin,
         'openCustomWin': self.onOpenCustomWin}
        self.boothMediator = None
        self.boothRecord = None
        self.customWin = None
        self.sellingItem = None
        self.buyingItem = None
        self.changPricing = False
        self.boothType = True
        self.otherBoothInfo = None
        self.quantityItem = None
        self.numberItem = None
        self.word = None
        self.logs = None
        self.ownerLogs = []
        self.searchList = []
        self.diffTimeList = []
        self.priceSellMap = {}
        self.priceBuyMap = {}
        self.itemNameDict = {}
        self.cusTopLogo = []
        self.cusModel = []
        self.getCustomNum()
        uiAdapter.registerEscFunc(uiConst.WIDGET_BOOTH, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_BOOTH_RECORD, self.closeBoothRecord)
        uiAdapter.registerEscFunc(uiConst.WIDGET_BOOTH_CUSTOM, self.closeCustomWin)

    def showQuantity(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_BOOTH_QUANTITY, True)

    def closeQuantity(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BOOTH_QUANTITY)

    def showNumber(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_BOOTH_NUMBER, True)

    def closeNumber(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BOOTH_NUMBER)

    def showCustomWin(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_BOOTH_CUSTOM)

    def closeCustomWin(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BOOTH_CUSTOM)

    def onCloseCustomWin(self, *args):
        self.closeCustomWin()

    def onOpenCustomWin(self, *args):
        self.showCustomWin()

    def onGetBoothTax(self, *arg):
        tax = int(SYCD.data.get('boothTaxRate', 0.03) * 100)
        return GfxValue(str(tax) + '%')

    def onGetCustomPageInfo(self, *args):
        sType = int(args[3][0].GetNumber())
        page = int(args[3][1].GetNumber())
        info = []
        if sType == uiConst.BOOTH_CUS_TOPLOGO:
            data = self.cusTopLogo
        else:
            data = self.cusModel
        nowInfo = data[page * 9:page * 9 + 9]
        for itemId in nowInfo:
            pageInfo = BSD.data.get(itemId)
            labaType = pageInfo['type']
            pageInfo['itemId'] = itemId
            if labaType == uiConst.BOOTH_CUS_ITEM_TYPE:
                endTime = BigWorld.player().boothSkinExTime.get(itemId, 0)
                pageInfo['isNew'] = False
                if self.diffTimeList:
                    if itemId in self.diffTimeList:
                        pageInfo['isNew'] = True
                if endTime > utils.getNow():
                    timeText = time.strftime('%Y.%m.%d  %H:%M', time.localtime(endTime))
                    pageInfo['desc'] = gameStrings.TEXT_BOOTHPROXY_168 % timeText
                    pageInfo['descMid'] = False
                else:
                    pageInfo['desc'] = ''
                    pageInfo['descMid'] = True
            elif labaType == uiConst.BOOTH_CUS_FREE_TYPE:
                pageInfo['descMid'] = False
            elif labaType == uiConst.BOOTH_CUS_TIME_TYPE:
                configData = pageInfo.get('configData', {})
                if not configData:
                    pageInfo['descMid'] = True
                    continue
                startCrons = configData['startTimes']
                endCrons = configData['endTimes']
                for i in xrange(len(startCrons)):
                    if utils.inCrontabRange(startCrons[i], endCrons[i]):
                        pageInfo['descMid'] = False
                    else:
                        continue

                if pageInfo.get('descMid') == None:
                    pageInfo['descMid'] = True
            elif labaType == gametypes.LABA_CROSS_SERVER:
                continue
            info.append(pageInfo)

        info.sort(key=lambda item: item['itemId'])
        return uiUtils.array2GfxAarry(info, True)

    def onGetCustomSelItem(self, *arg):
        sType = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if sType == uiConst.BOOTH_CUS_TOPLOGO:
            ret = p.curBoothToplogoId
        elif sType == uiConst.BOOTH_CUS_MODEL:
            ret = p.curBoothModelId
        return GfxValue(ret)

    def getCustomNum(self):
        for itemId in BSD.data.iterkeys():
            data = BSD.data.get(itemId)
            if data['stype'] == uiConst.BOOTH_CUS_TOPLOGO:
                self.cusTopLogo.append(itemId)
            else:
                self.cusModel.append(itemId)

    def onGetCustomItemNum(self, *arg):
        customType = arg[3][0].GetNumber()
        ret = 0
        if customType == uiConst.BOOTH_CUS_TOPLOGO:
            ret = len(self.cusTopLogo)
        elif customType == uiConst.BOOTH_CUS_MODEL:
            ret = len(self.cusModel)
        return GfxValue(ret)

    def refreshCustomWin(self):
        if self.customWin:
            self.customWin.Invoke('refreshView')

    @ui.callFilter(6)
    def onSetCustomItem(self, *arg):
        customType = int(arg[3][0].GetNumber())
        skinId = int(arg[3][1].GetNumber())
        if skinId in self.diffTimeList:
            self.diffTimeList.remove(skinId)
        self.setBoothNewIcon()
        p = BigWorld.player()
        if customType == gametypes.BOOTH_SKIN_TYPE_TOPLOGO:
            p.cell.setBoothSkinTopLogoId(skinId)
        elif customType == gametypes.BOOTH_SKIN_TYPE_MODEL:
            p.cell.setBoothSkinModelId(skinId)

    def onGetBoothRecord(self, *arg):
        ret = [self.boothType]
        ret.append(gbk2unicode(self.formatMessage(self.word)))
        retLogs = []
        for log in self.logs:
            retLog = {}
            retLog['who'] = gbk2unicode(log[0])
            retLog['when'] = self.getTime(log[1])
            retLog['itemName'] = gbk2unicode(log[2].name)
            retLog['many'] = log[2].cwrap
            retLog['cost'] = log[3]
            retLog['total'] = int(log[4])
            retLog['tax'] = int(log[5])
            retLog['b'] = log[6]
            retLogs.append(retLog)

        ret.append(retLogs)
        return uiUtils.array2GfxAarry(ret)

    def onConfirmNumber(self, *arg):
        num = int(arg[3][0].GetString())
        it = self.numberItem[2]
        if it:
            gameglobal.rds.ui.consign.checkLowPrice(it, it.price, self._onConfirmNumber, (it, num))

    @ui.checkInventoryLock()
    def _onConfirmNumber(self, it, num):
        if not self.otherBoothInfo:
            return
        itemId = it.id
        cost = it.price
        BigWorld.player().cell.sellBoothBuyItem(self.otherBoothInfo[0], itemId, num, cost, self.numberItem[0], self.numberItem[1], 0, BigWorld.player().cipherOfPerson)
        self.closeNumber()
        gameglobal.rds.sound.playSound(gameglobal.SD_26)

    def onCancelNumber(self, *arg):
        self.closeNumber()

    def onRecieveItem(self, *arg):
        itemVal = self.quantityItem[2]
        return self.initQuantityInfo(itemVal)

    def onGetNumber(self, *arg):
        itemVal = self.numberItem[2]
        return self.initQuantityInfo(itemVal)

    def initQuantityInfo(self, item):
        obj = self.movie.CreateObject()
        name = ID.data.get(item.id, {}).get('name', '')
        p = BigWorld.player()
        path = uiUtils.getItemIconPath(item.id, uiConst.ICON_SIZE40)
        obj.SetMember('name', GfxValue(gbk2unicode(name)))
        obj.SetMember('value', GfxValue(str(item.price)))
        obj.SetMember('path', GfxValue(path))
        if hasattr(item, 'quality'):
            quality = item.quality
        else:
            quality = ID.data.get(item.id, {}).get('quality', 1)
        color = '0x' + FCD.data.get(('item', quality), {}).get('color', '#ffffff')[1:]
        qualitycolor = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        obj.SetMember('qualitycolor', GfxValue(qualitycolor))
        obj.SetMember('color', GfxValue(color))
        if not item.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
            obj.SetMember('state', GfxValue(uiConst.EQUIP_NOT_USE))
        else:
            obj.SetMember('state', GfxValue(uiConst.ITEM_NORMAL))
        num = 1
        obj.SetMember('num', GfxValue(num))
        obj.SetMember('maxNum', GfxValue(min(item.mwrap, item.cwrap)))
        obj.SetMember('money', self.onGetMoney())
        p.base.queryConsignItemPrice(item.id, gametypes.CONSIGN_QUERY_PRICE_FOR_BOOTH_BUY)
        return obj

    def onCloseBoothRecord(self, *arg):
        self.closeBoothRecord()

    def onClearSum(self, *arg):
        BigWorld.player().cell.clearBoothLogs()

    def onClearChatlog(self, *arg):
        BigWorld.player().cell.clearBoothWord()

    def onGetMoney(self, *arg):
        return GfxValue(str(BigWorld.player().cash))

    def onCloseQuantity(self, *arg):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BOOTH_QUANTITY)

    def onBuyItem(self, *arg):
        try:
            num = int(arg[3][0].GetNumber())
        except:
            return

        it = self.quantityItem[2]
        bagPage, bagPos = self.quantityItem[3], self.quantityItem[4]
        if bagPage == const.CONT_NO_PAGE or bagPos == const.CONT_NO_POS:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.SHOP_BAG_FULL, ())
            return
        payout = it.price * num
        gameglobal.rds.ui.consign.checkOverPrice(it, it.price, self._onBuyItem, (it,
         num,
         bagPage,
         bagPos,
         payout))

    @ui.checkInventoryLock()
    def _onBuyItem(self, it, num, bagPage, bagPos, payout):
        if payout < 4294967296L and self.otherBoothInfo and self.quantityItem:
            BigWorld.player().cell.buyBoothSellItem(self.otherBoothInfo[0], self.quantityItem[0], self.quantityItem[1], it.id, it.uuid, num, bagPage, bagPos, payout, 0, BigWorld.player().cipherOfPerson)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BOOTH_QUANTITY)
        gameglobal.rds.sound.playSound(gameglobal.SD_26)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_BOOTH:
            self.boothMediator = mediator
            self.refreshCustom()
        elif widgetId == uiConst.WIDGET_BOOTH_RECORD:
            self.boothRecord = mediator
        elif widgetId == uiConst.WIDGET_BOOTH_CUSTOM:
            self.customWin = mediator

    def getSlotID(self, key):
        page, idItem = key.split('.')
        nPage = int(page[5:])
        nItem = int(idItem[4:])
        return (nPage, nItem)

    def reset(self):
        self.sellingItem = None
        self.buyingItem = None
        self.changPricing = False
        self.boothType = True
        self.otherBoothInfo = None
        self.quantityItem = None
        self.numberItem = None
        self.word = None
        self.logs = None
        self.searchList = []
        self.itemNameDict = {}

    def show(self, boothType = True, data = None):
        self.boothType = boothType
        if not boothType:
            self.otherBoothInfo = data
        if not self.boothMediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BOOTH)
        else:
            self.updateBoothData()

    def updateBoothData(self):
        if self.boothMediator:
            self.boothMediator.Invoke('updateData')

    def refreshCustom(self):
        self.setTips()
        self.setBoothNewIcon()
        if self.boothMediator:
            enable = gameglobal.rds.configData.get('enableBoothCustom', True)
            self.boothMediator.Invoke('enableCustom', GfxValue(enable))

    def setBoothNewIcon(self):
        ret = False
        if self.diffTimeList:
            ret = True
        if self.boothMediator:
            self.boothMediator.Invoke('enableBoothNewIcon', GfxValue(ret))

    def setTips(self):
        tips = {}
        tips['changeName'] = SYCD.data.get('BOOTH_CHANGE_NANE_BTN_TIPS', gameStrings.TEXT_BOOTHPROXY_408)
        tips['custom'] = SYCD.data.get('BOOTH_CUSTOM_BTN_TIPS', gameStrings.TEXT_BOOTHPROXY_409)
        tips['overBooth'] = SYCD.data.get('BOOTH_OVER_BTN_TIPS', gameStrings.TEXT_BOOTHPROXY_410)
        if self.boothMediator:
            self.boothMediator.Invoke('setTips', uiUtils.dict2GfxDict(tips, True))

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        page, itemSlot = self.getSlotID(key)
        if self.boothType:
            i = BigWorld.player().booth.getQuickVal(page, itemSlot)
        else:
            i = self.getItemByOtherInfo(page, itemSlot)
        if i == None:
            return
        else:
            return self.GfxToolTip(i, page)

    def onGetSearchListToolTip(self, *arg):
        key = arg[3][0].GetString()
        page, idItem = key.split('.')
        index = int(idItem[4:])
        return tipUtils.getItemTipById(index)

    def onGetRecordToolTip(self, *arg):
        key = arg[3][0].GetString()
        page, idItem = key.split('.')
        index = int(idItem[4:])
        if index >= len(self.logs):
            return
        it = self.logs[index][2]
        return self.uiAdapter.inventory.GfxToolTip(it)

    def getItemByOtherInfo(self, page, pos):
        i = None
        if page == uiConst.BOOTH_SLOTS_SELL:
            otherSellInfo = self.otherBoothInfo[2]
            for itemInfo in otherSellInfo:
                if pos == itemInfo[1]:
                    i = itemInfo[2]
                    i.price = itemInfo[3]
                    break

        else:
            otherBuyInfo = self.otherBoothInfo[3]
            for itemInfo in otherBuyInfo:
                if pos == itemInfo[1]:
                    i = item.Item(itemInfo[2], itemInfo[3])
                    i.canOverMax = True
                    i.price = itemInfo[4]
                    i.cwrap = itemInfo[3]
                    break

        return i

    def GfxToolTip(self, item, page):
        location = const.ITEM_IN_BOOTH_SELL if page == uiConst.BOOTH_SLOTS_SELL else const.ITEM_IN_BOOTH_BUY
        return self.uiAdapter.inventory.GfxToolTip(item, location)

    def clearWidget(self):
        self.boothMediator = None
        self.customWin = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BOOTH)
        self.closeSellSetting()
        self.closeBoothRecord()
        self.closeNumber()
        self.closeQuantity()
        self.closeCustomWin()

    def _getKey(self, page, pos):
        return 'booth%d.slot%d' % (page, pos)

    def addItem(self, item, page, pos):
        if item is not None:
            key = self._getKey(page, pos)
            if self.binding.get(key, None) is not None:
                data = uiUtils.getGfxItem(item)
                if hasattr(item, 'quality'):
                    quality = item.quality
                else:
                    quality = ID.data.get(item.id, {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                self.binding[key][0].Invoke('setSlotColor', GfxValue(color))
                self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
                self.updateSlotState(page, pos)

    def updateSlotState(self, page, pos):
        p = BigWorld.player()
        item = p.booth.getQuickVal(page, pos)
        if item == const.CONT_EMPTY_VAL:
            return
        key = self._getKey(page, pos)
        if not self.binding.has_key(key):
            return
        if not item.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.EQUIP_NOT_USE))
        else:
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))

    def removeItem(self, page, pos):
        key = self._getKey(page, pos)
        if self.binding.get(key, None) is not None and self.boothMediator:
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            self.binding[key][1].InvokeSelf(data)
            self.boothMediator.Invoke('setSelIconNull', GfxValue(key))

    def onGetSearchList(self, *arg):
        text = unicode2gbk(arg[3][0].GetString())
        self.searchList = []
        if text == '':
            return uiUtils.array2GfxAarry(self.searchList)
        text = text.lower()
        isPinyinAndHanzi = utils.isPinyinAndHanzi(text)
        if isPinyinAndHanzi == const.STR_HANZI_PINYIN:
            return uiUtils.array2GfxAarry(self.searchList)
        if not self.itemNameDict:
            self.itemNameDict = self.getItemNameDict()
        for itemData in self.itemNameDict.items():
            name = itemData[1].get('name', '')
            if isPinyinAndHanzi == const.STR_ONLY_PINYIN:
                name2 = pinyinConvert.strPinyinFirst(name)
                isFind = name2.find(text) != -1
            else:
                isFind = name.find(text) != -1
            if isFind:
                quality = itemData[1].get('quality', 1)
                color = '0x' + FCD.data.get(('item', quality), {}).get('color', '#ffffff')[1:]
                qualitycolor = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                path = uiUtils.getItemIconPath(itemData[0], uiConst.ICON_SIZE40)
                self.searchList.append((gbk2unicode(name),
                 path,
                 itemData[0],
                 color,
                 qualitycolor))

        return uiUtils.array2GfxAarry(self.searchList)

    def getItemNameDict(self):
        ret = {}
        for itemId in ID.data.iterkeys():
            item = ID.data.get(itemId)
            if utils.getItemNoBooth(item):
                continue
            if utils.getItemNoBoothBuy(item):
                continue
            ret[itemId] = item

        return ret

    def onConfirmSell(self, *arg):
        price = arg[3][0].GetNumber()
        num = arg[3][1].GetNumber()
        if utils.needDisableUGC() and (num in UGCForceLimit or price in UGCForceLimit):
            BigWorld.player().showGameMsg(GMDD.data.UGC_FORCE_LIMIT_MSG, ())
            return
        p = BigWorld.player()
        if self.changPricing:
            it = p.booth.getQuickVal(self.sellingItem[0], self.sellingItem[1])
            if it:
                gameglobal.rds.ui.consign.checkLowPrice(it, price, self._onConfirmSell, (it, price, num), opName=gameStrings.TEXT_BOOTHPROXY_566)
        else:
            it = p.inv.getQuickVal(self.sellingItem[0], self.sellingItem[1])
            if it:
                gameglobal.rds.ui.consign.checkLowPrice(it, price, self._onConfirmSell, (it, price, num))

    @ui.checkInventoryLock()
    def _onConfirmSell(self, it, price, num):
        p = BigWorld.player()
        if self.changPricing:
            p.cell.changeBoothPrice(self.sellingItem[0], self.sellingItem[1], price, BigWorld.player().cipherOfPerson)
        else:
            p.cell.addBoothSellItem(self.sellingItem[0], self.sellingItem[1], self.sellingItem[2], self.sellingItem[3], num, price, BigWorld.player().cipherOfPerson)
        if it:
            self.priceSellMap[it.id] = price
        self.closeSellSetting()

    @ui.checkInventoryLock()
    def onConfirmBuy(self, *arg):
        price = arg[3][0].GetNumber()
        num = arg[3][1].GetNumber()
        if utils.needDisableUGC() and (num in UGCForceLimit or price in UGCForceLimit):
            BigWorld.player().showGameMsg(GMDD.data.UGC_FORCE_LIMIT_MSG, ())
            return
        if not self.buyingItem:
            return
        self.priceBuyMap[self.buyingItem[0]] = price
        p = BigWorld.player()
        if self.changPricing and self.buyingItem:
            p.cell.changeBoothPrice(self.buyingItem[1], self.buyingItem[2], price, BigWorld.player().cipherOfPerson)
        else:
            p.cell.addBoothBuyItem(self.buyingItem[0], num, price, self.buyingItem[1], self.buyingItem[2], BigWorld.player().cipherOfPerson)
        self.closeBuySetting()

    def onCloseBuySetting(self, *arg):
        self.closeBuySetting()

    def showBoothRecord(self, word, logs):
        self.word = word
        self.logs = logs
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BOOTH_RECORD)

    def closeBoothRecord(self):
        self.boothRecord = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BOOTH_RECORD)

    def parseMessage(self, msg):
        msg = re.sub('</?TEXTFORMAT.*?>', '', msg, 0, re.DOTALL)
        msg = re.sub('</?P.*?>', '', msg, 0, re.DOTALL)
        msg = re.sub('</?B.*?>', '', msg, 0, re.DOTALL)
        msg = gameglobal.rds.ui.chat.extractFontColor(msg)
        return msg

    def setMessage(self, msg):
        self.word = msg
        ret = self.formatMessage(msg)
        if self.boothRecord:
            self.boothRecord.Invoke('setMessage', GfxValue(gbk2unicode(ret)))

    def setRecord(self, record):
        self.logs = record
        retLogs = []
        for itemData in record:
            retLog = {}
            retLog['who'] = gbk2unicode(itemData[0])
            retLog['when'] = self.getTime(itemData[1])
            retLog['itemName'] = gbk2unicode(itemData[2].name)
            retLog['many'] = itemData[2].cwrap
            retLog['cost'] = itemData[3]
            retLog['total'] = int(itemData[4])
            retLog['tax'] = int(itemData[5])
            retLog['b'] = itemData[6]
            retLogs.append(retLog)

        if self.boothRecord:
            self.boothRecord.Invoke('setRecord', uiUtils.array2GfxAarry(retLogs))

    def formatMessage(self, msg):
        ret = ''
        for itemData in msg:
            eventName = 'role' + itemData[0]
            itemStr = "[<a href = \'event:%s\'><u>%s</u></a>][%s]:%s" % (eventName + '$',
             itemData[0],
             self.getTime(int(itemData[2])),
             itemData[1])
            ret = ret + itemStr + '\n'

        return ret

    def getTime(self, localTime):
        return time.strftime('%m-%d %H:%M', time.localtime(localTime))

    def onSubmitMessage(self, *arg):
        msg = arg[3][0].GetString()
        if msg == '':
            return
        else:
            msg = self.parseMessage(msg)
            msg = msg.decode('utf-8').encode(utils.defaultEncoding())
            p = BigWorld.player()
            isNormal, msg = taboo.checkDisbWord(msg)
            if not isNormal:
                p.showGameMsg(GMDD.data.CHAT_TABOO_WORD, ())
                return
            msg = re.compile('#([0-9]{1})').sub('!$\\1', msg)
            msg = re.compile('!\\$([A-Fa-f0-9]{6})').sub('#\\1', msg)
            ent = None
            if self.boothType:
                ent = BigWorld.player()
            else:
                ent = BigWorld.entity(self.otherBoothInfo[0])
            if ent:
                ent.cell.leaveBoothWord(msg)
            return

    def setChatText(self, msgText):
        if self.boothRecord != None:
            self.boothRecord.Invoke('settfInput', GfxValue(gbk2unicode(msgText)))

    def onLinkLeftClick(self, *arg):
        p = BigWorld.player()
        roleName = unicode2gbk(arg[3][0].GetString())
        isRightClick = arg[3][1].GetBool()
        if isRightClick:
            if roleName[:4] == 'role' and roleName[4:] != gameStrings.TEXT_BOOTHPROXY_694 and roleName[4:-1] != p.realRoleName:
                menuManager.getInstance().menuTarget.apply(roleName=roleName[4:-1])
                data = menuManager.getInstance().getMenuListById(uiConst.MENU_CHAT)
                self.boothRecord.Invoke('showRightMenu', uiUtils.dict2GfxDict(data, True))
        elif roleName[:3] == 'ret':
            retCode = int(roleName[3:])
            p.base.chatToItem(retCode, 'booth')
        elif roleName[:4] == 'item':
            self.showTooltip(const.CHAT_TIPS_ITEM, gameglobal.rds.ui.inventory.GfxToolTip(Item(int(roleName[4:]), 1, False)))
        elif roleName[:4] == 'task':
            self.showTooltip(const.CHAT_TIPS_TASK, gameglobal.rds.ui.chat.taskToolTip(int(roleName[4:])))
        elif roleName[:4] == 'achv':
            self.showTooltip(const.CHAT_TIPS_ACHIEVEMENT, gameglobal.rds.ui.chat.achieveToolTip(roleName[4:]))
        elif roleName.startswith('sprite'):
            p.base.chatToSprite(int(roleName[len('sprite'):]), 'booth')

    def showTooltip(self, tipsType, gfxTipData):
        if self.boothRecord:
            self.boothRecord.Invoke('showTooltip', (GfxValue(tipsType), gfxTipData))

    def showSellSetting(self, item):
        self.sellingItem = item
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BOOTH_SELL, True)
        p = BigWorld.player()
        if self.changPricing:
            it = p.booth.getQuickVal(self.sellingItem[0], self.sellingItem[1])
        else:
            it = p.inv.getQuickVal(self.sellingItem[0], self.sellingItem[1])
        p = BigWorld.player()
        p.base.queryConsignItemPrice(it.id, gametypes.CONSIGN_QUERY_PRICE_FOR_BOOTH_BUY)

    def closeSellSetting(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BOOTH_SELL)
        self.changPricing = False

    def showBuySetting(self, item):
        self.buyingItem = item
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BOOTH_BUY, True)

    def closeBuySetting(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BOOTH_BUY)
        self.changPricing = False

    def onCloseSellSetting(self, *arg):
        self.closeSellSetting()

    def onCancelBuy(self, *arg):
        binding = arg[3][0].GetString()
        page, pos = self.getSlotID(binding)
        BigWorld.player().cell.delBoothBuyItem(page, pos)

    def onCancelSell(self, *arg):
        binding = arg[3][0].GetString()
        page, pos = self.getSlotID(binding)
        self.startCancelSell(page, pos)

    def startCancelSell(self, page, pos):
        it = BigWorld.player().booth.getQuickVal(page, pos)
        if it:
            BigWorld.player().cell.revertBoothSellItem(page, pos, it.cwrap)

    def onBuy(self, *arg):
        binding = arg[3][0].GetString()
        page, pos = self.getSlotID(binding)
        self.startBuy(page, pos)

    def onFitting(self, *arg):
        if not self.otherBoothInfo:
            return
        else:
            binding = arg[3][0].GetString()
            page, pos = self.getSlotID(binding)
            otherSellInfo = self.otherBoothInfo[2]
            it = None
            for itemInfo in otherSellInfo:
                if pos == itemInfo[1]:
                    it = itemInfo[2]
                    break

            if it:
                gameglobal.rds.ui.fittingRoom.addItem(it)
            return

    def startBuy(self, page, pos, bagPage = None, bagPos = None):
        otherSellInfo = self.otherBoothInfo[2]
        it = None
        for itemInfo in otherSellInfo:
            if pos == itemInfo[1]:
                it = itemInfo[2]
                it.price = itemInfo[3]
                break

        if not it:
            return
        else:
            if bagPage == None and bagPos == None:
                bagPage, bagPos = BigWorld.player().inv.searchBestInPages(it.id, it.cwrap, it)
            self.quantityItem = (page,
             pos,
             it,
             bagPage,
             bagPos)
            if it:
                self.showQuantity()
            return

    def onSell(self, *arg):
        binding = arg[3][0].GetString()
        page, pos = self.getSlotID(binding)
        otherBuyInfo = self.otherBoothInfo[3]
        it = None
        for itemInfo in otherBuyInfo:
            if pos == itemInfo[1]:
                it = item.Item(itemInfo[2], itemInfo[3])
                it.cwrap = itemInfo[3]
                it.price = itemInfo[4]
                break

        self.numberItem = (page, pos, it)
        if it:
            self.showNumber()

    def onOpenInventory(self, *arg):
        pass

    def onGetBuyItemInfo(self, *arg):
        itemInfo = {}
        itemId = int(self.buyingItem[0])
        if self.changPricing:
            item = BigWorld.player().booth.getQuickVal(self.buyingItem[1], self.buyingItem[2])
            if item:
                itemInfo['num'] = item.cwrap
                itemInfo['price'] = item.price
        else:
            itemInfo['num'] = 1
            itemInfo['price'] = self.getRemBuyPrice(itemId)
        if ID.data.get(itemId) == None:
            raise Exception('item data is not found: %d' % itemId)
            return uiUtils.dict2GfxDict(itemInfo)
        else:
            quality = ID.data.get(itemId, {}).get('quality', 1)
            color = '0x' + FCD.data.get(('item', quality), {}).get('color', '#ffffff')[1:]
            qualitycolor = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            itemInfo['qualitycolor'] = qualitycolor
            itemInfo['color'] = color
            itemInfo['maxNum'] = uiUtils.getItemMaxNumById(itemId)
            itemInfo['name'] = gbk2unicode(self._getItemName(itemId))
            itemInfo['path'] = uiUtils.getItemIconFile40(itemId)
            itemInfo['type'] = self.changPricing
            return uiUtils.dict2GfxDict(itemInfo)

    def getRemSellPrice(self, itemId):
        return self.priceSellMap.get(itemId, 1)

    def getRemBuyPrice(self, itemId):
        return self.priceBuyMap.get(itemId, 1)

    def onGetSellItemInfo(self, *arg):
        itemInfo = {}
        if self.changPricing:
            item = BigWorld.player().booth.getQuickVal(self.sellingItem[0], self.sellingItem[1])
            if item:
                itemInfo['num'] = item.cwrap
                itemInfo['maxNum'] = 0
                itemInfo['price'] = item.price
        else:
            item = BigWorld.player().inv.getQuickVal(self.sellingItem[0], self.sellingItem[1])
            if item:
                itemInfo['num'] = item.cwrap
                itemInfo['maxNum'] = item.cwrap
                itemInfo['price'] = self.getRemSellPrice(item.id)
        if item:
            if hasattr(item, 'quality'):
                quality = item.quality
            else:
                quality = ID.data.get(item.id, {}).get('quality', 1)
            color = '0x' + FCD.data.get(('item', quality), {}).get('color', '#ffffff')[1:]
            qualitycolor = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            itemInfo['qualitycolor'] = qualitycolor
            itemInfo['color'] = color
            itemInfo['name'] = gbk2unicode(item.name)
            itemInfo['path'] = uiUtils.getItemIconFile40(item.id)
            itemInfo['type'] = self.changPricing
        return uiUtils.dict2GfxDict(itemInfo)

    def _getItemName(self, id):
        return ID.data.get(id, {}).get('name', '')

    def onCloseRename(self, *arg):
        pass

    def onRenameBooth(self, *arg):
        pass

    def onRequestSearch(self, *arg):
        pass

    def onAddBuy(self, *arg):
        itemId = arg[3][0].GetNumber()
        page = uiConst.BOOTH_SLOTS_BUY
        pos = BigWorld.player().booth.searchEmpty(page)
        if pos < 0:
            BigWorld.player().showGameMsg(GMDD.data.BOOTH_BUY_ITEMS_FULL, ())
            return
        gameglobal.rds.ui.booth.showBuySetting((itemId, page, pos))

    def onReName(self, *arg):
        name = unicode2gbk(arg[3][0].GetString())
        p = BigWorld.player()
        result, _ = taboo.checkNameDisWord(name)
        if not result:
            p.showGameMsg(GMDD.data.CHAT_TABOO_WORD, ())
            return
        p.cell.changeBoothName(name)

    def onCloseBooth(self, *arg):
        p = BigWorld.player()
        p.cell.shutUpBooth()

    def onChangePrice(self, *arg):
        binding = arg[3][0].GetString()
        page, pos = self.getSlotID(binding)
        self.changPricing = True
        if page == uiConst.BOOTH_SLOTS_SELL:
            it = BigWorld.player().booth.getQuickVal(page, pos)
            if it:
                gameglobal.rds.ui.booth.showSellSetting((page, pos))
            else:
                self.changPricing = False
        else:
            item = BigWorld.player().booth.getQuickVal(page, pos)
            if item:
                gameglobal.rds.ui.booth.showBuySetting((item.id, page, pos))
            else:
                self.changPricing = False

    def onShowRecord(self, *arg):
        if self.boothType:
            BigWorld.player().cell.readBoothWordAndLogs()
        else:
            ent = BigWorld.entities.get(self.otherBoothInfo[0])
            ent.cell.readBoothWordAndLogs()

    def onCloseBoothWin(self, *arg):
        self.hide()

    def onGetBoothInfo(self, *arg):
        if self.boothType:
            return self.initPlayerBoothInfo()
        else:
            return self.initOtherBoothInfo()

    def onGetDefaultName(self, *arg):
        if self.boothType:
            p = BigWorld.player()
            return GfxValue(gbk2unicode(p.boothName))
        else:
            boothName = ''
            ent = BigWorld.entities.get(self.otherBoothInfo[0])
            if ent:
                boothName = ent.boothName
            return GfxValue(gbk2unicode(boothName))

    def setBoothName(self, name):
        if self.boothMediator:
            self.boothMediator.Invoke('setBoothName', GfxValue(gbk2unicode(name)))

    def initItemArr(self, it, pos):
        p = BigWorld.player()
        itemInfo = []
        obj = {}
        itemInfo.append(pos)
        obj = uiUtils.getGfxItem(it)
        itemInfo.append(obj)
        if it.type == Item.BASETYPE_EQUIP and (hasattr(it, 'cdura') and it.cdura == 0 or it.canEquip(p, it.whereEquip()[0])):
            itemInfo.append(uiConst.EQUIP_BROKEN)
        elif not it.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
            itemInfo.append(uiConst.EQUIP_NOT_USE)
        else:
            itemInfo.append(uiConst.ITEM_NORMAL)
        if hasattr(it, 'quality'):
            quality = it.quality
        else:
            quality = ID.data.get(it.id, {}).get('quality', 1)
        color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        itemInfo.append(color)
        return itemInfo

    def initPlayerBoothInfo(self):
        p = BigWorld.player()
        ret = [self.boothType]
        sellInfo = []
        buyInfo = []
        for ps in xrange(p.booth.posCount):
            it = p.booth.getQuickVal(uiConst.BOOTH_SLOTS_SELL, ps)
            if it == const.CONT_EMPTY_VAL:
                self.removeItem(uiConst.BOOTH_SLOTS_SELL, ps)
                continue
            arr = self.initItemArr(it, ps)
            sellInfo.append(arr)

        for ps in xrange(p.booth.posCount):
            it = p.booth.getQuickVal(uiConst.BOOTH_SLOTS_BUY, ps)
            if it == const.CONT_EMPTY_VAL:
                self.removeItem(uiConst.BOOTH_SLOTS_BUY, ps)
                continue
            arr = self.initItemArr(it, ps)
            buyInfo.append(arr)

        ret.append(sellInfo)
        ret.append(buyInfo)
        return uiUtils.array2GfxAarry(ret)

    def initOtherBoothInfo(self):
        otherSellInfo = self.otherBoothInfo[2]
        otherBuyInfo = self.otherBoothInfo[3]
        sellInfo = []
        buyInfo = []
        ret = [self.boothType]
        p = BigWorld.player()
        for ps in xrange(p.booth.posCount):
            self.removeItem(uiConst.BOOTH_SLOTS_SELL, ps)

        for ps in xrange(p.booth.posCount):
            self.removeItem(uiConst.BOOTH_SLOTS_BUY, ps)

        for itemInfo in otherSellInfo:
            it = itemInfo[2]
            it.price = itemInfo[3]
            arr = self.initItemArr(it, itemInfo[1])
            sellInfo.append(arr)

        for itemInfo in otherBuyInfo:
            it = item.Item(itemInfo[2], itemInfo[3])
            it.canOverMax = True
            it.cwrap = itemInfo[3]
            it.price = itemInfo[4]
            arr = self.initItemArr(it, itemInfo[1])
            buyInfo.append(arr)

        ret.append(sellInfo)
        ret.append(buyInfo)
        return uiUtils.array2GfxAarry(ret)

    @ui.uiEvent(uiConst.WIDGET_BOOTH, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        else:
            pos = BigWorld.player().booth.searchEmpty(uiConst.BOOTH_SLOTS_SELL)
            self.onSetItem(nPage, nItem, uiConst.BOOTH_SLOTS_SELL, pos)
            return

    def onSetItem(self, nPageSrc, nItemSrc, nPageDes, nItemDes):
        if not self.boothType:
            return
        itSrc = BigWorld.player().inv.getQuickVal(nPageSrc, nItemSrc)
        isValid = BigWorld.player().booth._isValid(nPageDes, nItemDes)
        if itSrc.isRuneHasRuneData():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_BOOTH_RUNE_EQUIP, ())
            return
        if nPageDes == uiConst.BOOTH_SLOTS_SELL and itSrc.isItemNoTrade():
            BigWorld.player().showGameMsg(GMDD.data.BOOTH_CANNOT_SELL, ())
            return
        if nPageDes == uiConst.BOOTH_SLOTS_BUY and (itSrc.isItemNoTrade() or not itSrc.canBooth() or itSrc.isEquip()):
            BigWorld.player().showGameMsg(GMDD.data.BOOTH_CANNOT_BUY, ())
            return
        if not isValid:
            BigWorld.player().showGameMsg(GMDD.data.SHOP_INVALID_POS, ())
            return
        itDes = BigWorld.player().booth.getQuickVal(nPageDes, nItemDes)
        if itDes:
            BigWorld.player().showGameMsg(GMDD.data.SHOP_INVALID_POS, ())
            return
        if nPageDes == uiConst.BOOTH_SLOTS_SELL:
            isNoBooth = utils.getItemNoBooth(ID.data.get(itSrc.id, {}))
            if isNoBooth:
                BigWorld.player().showGameMsg(GMDD.data.BOOTH_CANNOT_SELL, (itSrc.name,))
                return
            if itSrc.isForeverBind():
                BigWorld.player().showGameMsg(GMDD.data.BOOTH_ITEM_BIND, (itSrc.name,))
                return
            self.showSellSetting((nPageSrc,
             nItemSrc,
             nPageDes,
             nItemDes))
        elif nPageDes == uiConst.BOOTH_SLOTS_BUY:
            it = BigWorld.player().inv.getQuickVal(nPageSrc, nItemSrc)
            self.showBuySetting((it.id, nPageDes, nItemDes))

    def setOldBoothSkinExTime(self, oldBoothSkinExTime):
        endTimeKeys = BigWorld.player().boothSkinExTime.keys()
        newTimeKeys = oldBoothSkinExTime.keys()
        diff = list(set(endTimeKeys) - set(newTimeKeys))
        if diff:
            self.diffTimeList.append(diff[0])
