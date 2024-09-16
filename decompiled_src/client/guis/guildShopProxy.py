#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/guildShopProxy.o
import BigWorld
from Scaleform import GfxValue
import ui
import gameglobal
import const
import gametypes
import utils
import uiConst
import uiUtils
import commGuild
from uiProxy import SlotDataProxy
from data import item_data as ID
from data import fame_data as FD
from data import sys_config_data as SCD
from data import guild_shop_data as GSD
from data import guild_building_data as GBD
from data import guild_building_upgrade_data as GBUD
from cdata import game_msg_def_data as GMDD

class GuildShopProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(GuildShopProxy, self).__init__(uiAdapter)
        self.bindType = 'guildShop'
        self.type = 'guildShop'
        self.modelMap = {'clickManager': self.onClickManager,
         'getInitData': self.onGetInitData,
         'initGuildShopItem': self.onInitGuildShopItem,
         'clickExtraPurchase': self.onClickExtraPurchase,
         'getItemDetail': self.onGetItemDetail,
         'setBuyItemNum': self.onSetBuyItemNum,
         'buyItem': self.onBuyItem}
        self.mediator = None
        self.markerId = 0
        self.buildType = 0
        self.buildLv = 0
        self.shopType = 0
        self.page = const.GUILD_SHOP_PAGE_ONE
        self.pos = 0
        self.buyItemNum = 0
        self.timer = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_SHOP, self.hide)

    def show(self, markerId):
        if not self.mediator:
            self.markerId = markerId
            gameglobal.rds.ui.guild.hideAllGuildBuilding()
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_SHOP)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_SHOP:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_SHOP)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        self.markerId = 0
        self.buildType = 0
        self.buildLv = 0
        self.shopType = 0
        self.page = const.GUILD_SHOP_PAGE_ONE
        self.pos = 0
        self.buyItemNum = 0
        self.stopTimer()

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def onGetInitData(self, *arg):
        guild = BigWorld.player().guild
        marker = guild.marker.get(self.markerId)
        buildValue = guild.building.get(marker.buildingNUID)
        self.buildLv = buildValue.level if buildValue else 0
        self.buildType = buildValue.buildingId
        self.shopType = gametypes.GUILD_SHOP_BUILDING[self.buildType] - 1
        info = {}
        info['nameTitle'] = GBD.data.get(buildValue.buildingId, {}).get('name', '')
        info['level'] = '%d级' % self.buildLv
        self.refreshExtraAble()
        return uiUtils.dict2GfxDict(info, True)

    def refreshExtraAble(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            maxCnt = commGuild.getMemberShopMaxRefreshCnt()
            if p.guildMemberShopRefreshCnt < maxCnt:
                info['btnEnabled'] = True
                info['btnTips'] = '每天可额外进货%d次' % maxCnt
            else:
                info['btnEnabled'] = False
                info['btnTips'] = '今天额外进货次数已满'
            self.mediator.Invoke('refreshExtraAble', uiUtils.dict2GfxDict(info, True))
            self.startShopTime()

    @ui.callInCD(1)
    def startShopTime(self, *arg):
        self.stopTimer()
        self.timestamp_datetime()

    def timestamp_datetime(self):
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            remainTime = guild.shop[self.shopType].tNextRefresh - int(p.getServerTime())
            if remainTime <= 0:
                remainTime = 0
            timeStr = utils.formatTimeStr(remainTime, 'h:m:s', zeroShow=True, sNum=2, mNum=2, hNum=2)
            self.mediator.Invoke('setTime', GfxValue(timeStr))
            if remainTime > 0:
                self.timer = BigWorld.callback(1.0, self.timestamp_datetime)
            else:
                p.cell.checkGuildShopRefresh(self.shopType + 1, guild.shop[self.shopType].tNextRefresh)

    def onInitGuildShopItem(self, *arg):
        self.page = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        guild = p.guild
        if not guild:
            return
        levelArray = []
        for i in xrange(10):
            slotArray = []
            posCountDict = GBUD.data.get((self.buildType, i + 1), {}).get('functions', None)
            if posCountDict:
                for j in xrange(4):
                    slotArray.append(posCountDict[0][1][j])

            levelArray.append(slotArray)

        if self.mediator:
            self.mediator.Invoke('setItemFlag', uiUtils.array2GfxAarry(levelArray))
        posCountDict = GBUD.data.get((self.buildType, self.buildLv), {}).get('functions', None)
        if posCountDict:
            validCount = posCountDict[0][1][self.page]
        else:
            validCount = 0
        self.setSlotCount(validCount)
        itemList = []
        for i in xrange(validCount):
            item = guild.shop[self.shopType].getQuickVal(self.page, i)
            itemInfo = {}
            if item:
                itemInfo = uiUtils.getGfxItemById(item.id)
                itemInfo['itemName'] = uiUtils.getItemColorName(item.id)
                itemInfo['count'] = str(item.cwrap)
                limit = GSD.data.get(item.gsid, {}).get('limit', 0)
                itemInfo['limit'] = '每天限购%d个' % limit if limit > 0 else '每天不限购买'
                itemInfo['isNone'] = False
            else:
                itemInfo['isNone'] = True
            itemList.append(itemInfo)

        if self.mediator:
            self.mediator.Invoke('refreshGuildShopItem', uiUtils.array2GfxAarry(itemList, True))

    def refreshShopCurPage(self):
        self.refreshShop(self.page)

    def refreshShop(self, pageNum):
        if self.mediator:
            self.mediator.Invoke('refreshShop', GfxValue(pageNum))

    def setSlotCount(self, slotCount):
        if self.mediator:
            self.mediator.Invoke('setSlotCount', GfxValue(slotCount))

    def onClickExtraPurchase(self, *arg):
        gameglobal.rds.ui.guildShopExtra.show(self.shopType + 1, self.buildLv)

    def onGetItemDetail(self, *arg):
        key = arg[3][0].GetString()
        self.pos = int(key[-1:])
        self.buyItemNum = 1
        self.refreshItemDetailInfo()
        self.refreshBuyItemDisplayData()

    def refreshItemDetailInfo(self):
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            shop = p.guild.shop[self.shopType]
            item = shop.getQuickVal(self.page, self.pos)
            if not item:
                return
            info = {}
            itemInfo = uiUtils.getGfxItemById(item.id)
            itemInfo['itemName'] = uiUtils.getItemColorName(item.id)
            info['itemInfo'] = itemInfo
            limit = GSD.data.get(item.gsid, {}).get('limit')
            if limit:
                limit = max(0, limit - shop.buyRecord.get(item.id, 0))
                info['maxNum'] = min(item.mwrap, item.cwrap, limit)
            else:
                info['maxNum'] = min(item.mwrap, item.cwrap)
            self.mediator.Invoke('refreshItemDetailInfo', uiUtils.dict2GfxDict(info, True))

    def onSetBuyItemNum(self, *arg):
        buyItemNum = int(arg[3][0].GetNumber())
        if self.buyItemNum == buyItemNum:
            return
        self.buyItemNum = buyItemNum
        self.refreshBuyItemDisplayData()

    def refreshBuyItemDisplayData(self):
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            item = p.guild.shop[self.shopType].getQuickVal(self.page, self.pos)
            if not item:
                return
            gsd = GSD.data.get(item.gsid, {})
            isValid = True
            consumeItemInfo = []
            if gsd.get('fame'):
                fameId, fameVal = gsd.get('fame')
                fameLv, extraFame = gameglobal.rds.ui.compositeShop._getFameLv(fameId, fameVal)
                fd = FD.data.get(fameId, {})
                if fd.has_key('lvDesc'):
                    maoxianFameName = fd.get('lvDesc', {}).get(fameLv, '')
                    itemName = '冒险家等级 达到 %s' % (maoxianFameName,)
                    if p.delegationRank >= fameVal:
                        consumeItemInfo.append([itemName, True, ''])
                    else:
                        consumeItemInfo.append([itemName, False, ''])
                        isValid = False
                else:
                    fameName = fd.get('shopTips', '')
                    fameLvName = SCD.data.get('fameLvName', {}).get(fameLv, '')
                    if fameLvName != '':
                        if extraFame <= 0:
                            itemName = '%s 达到 %s' % (fameName, fameLvName)
                        else:
                            extraFame = str(extraFame)
                            itemName = '%s 达到 %s + %s点' % (fameName, fameLvName, extraFame)
                        if p.getFame(fameId) >= fameVal:
                            consumeItemInfo.append([itemName, True, ''])
                        else:
                            consumeItemInfo.append([itemName, False, ''])
                            isValid = False
            consumeItems = gsd.get('consumeItems')
            if consumeItems:
                consumeItemList = {}
                for itemId, itemNum in consumeItems:
                    if not itemId:
                        continue
                    itemNum *= self.buyItemNum
                    itemName = ID.data.get(itemId, {}).get('name', '')
                    if itemId in consumeItemList:
                        curItemNum = consumeItemList[itemId]
                    else:
                        curItemNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
                        if curItemNum - itemNum < 0:
                            consumeItemList[itemId] = 0
                        else:
                            consumeItemList[itemId] = curItemNum - itemNum
                    if curItemNum >= itemNum:
                        consumeItemInfo.append([itemName,
                         True,
                         str(curItemNum) + '/' + str(itemNum),
                         itemId])
                    else:
                        consumeItemInfo.append([itemName,
                         False,
                         str(curItemNum) + '/' + str(itemNum),
                         itemId])
                        isValid = False

            if gsd.has_key('contrib'):
                fameName = '公会贡献'
                consumeContrib = guild.getShopItemContrib(item.gsid, self.buyItemNum)
                if p.guildContrib >= consumeContrib:
                    consumeItemInfo.append([fameName, True, format(p.guildContrib, ',') + '/' + format(consumeContrib, ',')])
                else:
                    consumeItemInfo.append([fameName, False, format(p.guildContrib, ',') + '/' + format(consumeContrib, ',')])
                    isValid = False
            consumeCash = guild.getShopItemCash(item.gsid, self.buyItemNum)
            consumeBindCash = guild.getShopItemBindCash(item.gsid, self.buyItemNum)
            if p.cash < consumeCash:
                isValid = False
            elif p.cash + p.bindCash < consumeCash + consumeBindCash:
                isValid = False
            ret = {'cash': consumeCash,
             'bindCash': consumeBindCash,
             'consumeItem': consumeItemInfo,
             'playerCash': p.cash,
             'playerBindCash': p.bindCash,
             'isValid': isValid}
            self.mediator.Invoke('refreshConsumeInfo', uiUtils.dict2GfxDict(ret, True))

    def onBuyItem(self, *arg):
        p = BigWorld.player()
        guild = p.guild
        if not guild:
            return
        shop = p.guild.shop[self.shopType]
        item = shop.getQuickVal(self.page, self.pos)
        if not item:
            return
        limit = GSD.data.get(item.gsid, {}).get('limit')
        if limit and limit <= shop.buyRecord.get(item.id, 0):
            p.showGameMsg(GMDD.data.GUILD_SHOP_BUY_LIMIT, ('',))
            return
        p.cell.buyGuildShopItem(self.shopType + 1, self.page, self.pos, item.uuid, self.buyItemNum, item.id, getattr(item, 'gsid'))

    def onClickManager(self, *arg):
        gameglobal.rds.ui.guildResidentManager.showOrHide(self.markerId)
