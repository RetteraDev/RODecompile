#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/spaceGiftGivingProxy.o
from gamestrings import gameStrings
import BigWorld
import gametypes
import gamelog
import gameglobal
import const
from item import Item
from guis.uiProxy import SlotDataProxy
from guis import uiConst
from guis import uiUtils
from gamestrings import gameStrings
from ui import unicode2gbk
from data import item_data as ID
from data import personal_zone_gift_data as PZGD
from cdata import game_msg_def_data as GMDD
LABELTYPE = {1: gameStrings.TEXT_SPACEGIFTBOXPROXY_17,
 2: gameStrings.TEXT_SPACEGIFTBOXPROXY_18,
 3: gameStrings.TEXT_SPACEGIFTBOXPROXY_19,
 4: gameStrings.TEXT_SPACEGIFTBOXPROXY_20}
PERPAGE_ITEM_NUM_MAX = 12

class SpaceGiftGivingProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(SpaceGiftGivingProxy, self).__init__(uiAdapter)
        self.bindType = 'spaceGiftGiving'
        self.showType = gametypes.SPACE_GIFT_GIVING_POPULARITY
        self.modelMap = {'initState': self.onInitState,
         'countArray': self.onCountArray,
         'countArrayAll': self.onCountArrayAll,
         'sendGift': self.onSendGift,
         'openHelp': self.onOpenHelp,
         'showMsg': self.onShowMsg}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SPACEGIFT_GIVING, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SPACEGIFT_GIVING:
            self.mediator = mediator
            BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
            BigWorld.player().registerEvent(const.EVENT_ITEM_REMOVE, self.onItemRemove)
            return uiUtils.dict2GfxDict(self.getMediatorInitData(), True)

    def onInitState(self, *args):
        self.initCountInfo()
        self.initItemInfo()
        return uiUtils.dict2GfxDict(self.baseInfo, True)

    def onShowMsg(self, *arg):
        msg = unicode2gbk(arg[3][0].GetString())
        if msg:
            gameglobal.rds.ui.systemTips.show(msg)

    def initItemInfo(self):
        labelData = []
        newGood = {'labelName': gameStrings.TEXT_SPACEGIFTGIVINGPROXY_68,
         'items': []}
        hotGood = {'labelName': gameStrings.TEXT_SPACEGIFTGIVINGPROXY_72,
         'items': []}
        for key in LABELTYPE:
            tempItem = {'labelName': LABELTYPE[key],
             'items': []}
            labelData.append(tempItem)

        for key in PZGD.data:
            itemId = PZGD.data.get(key, {}).get('itemId', 0)
            parentItemId = Item.parentId(itemId)
            if not self.filterItemByShowType(key, self.showType):
                continue
            _type = PZGD.data[key]['type'] - 1
            cashNeed = PZGD.data.get(key, {}).get('cashNeed', 0)
            bCashNeed = PZGD.data.get(key, {}).get('bCashNeed', 0)
            if self.showType == gametypes.SPACE_GIFT_GIVING_POPULARITY:
                giftValue = PZGD.data.get(key, {}).get('popularity', 0)
            elif self.showType == gametypes.SPACE_GIFT_GIVING_MISS_GROUP_VOTE:
                giftValue = PZGD.data.get(key, {}).get('missTianyuVal', 0)
            else:
                giftValue = PZGD.data.get(key, {}).get('popularity', 0)
            recommendType = PZGD.data.get(key, {}).get('recommendType', 0)
            useDesc = PZGD.data.get(key, {}).get('useDesc', '')
            desc = PZGD.data.get(key, {}).get('desc', '')
            limitStr = self._getLimitStr(PZGD.data.get(key, {}))
            p = BigWorld.player()
            count = p.inv.countItemInPages(parentItemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
            itemDetail = uiUtils.getGfxItemById(parentItemId, count, uiConst.ICON_SIZE64)
            itemDetail['count'] = str(itemDetail['count'])
            iconPath64 = uiUtils.getItemIconPath(parentItemId, uiConst.ICON_SIZE64)
            needItems = PZGD.data.get(key, {}).get('cItems', ())
            labelItem = {'giftId': key,
             'itemDetail': itemDetail,
             'giftValue': giftValue,
             'recommendType': recommendType}
            if recommendType == 1:
                newGood['items'].append(labelItem)
            elif recommendType == 2:
                hotGood['items'].append(labelItem)
            else:
                labelData[_type]['items'].append(labelItem)

        for v in labelData:
            v['items'].sort(cmp=lambda x, y: cmp(x['giftValue'], y['giftValue']), reverse=True)

        newGood['items'].sort(cmp=lambda x, y: cmp(x['giftValue'], y['giftValue']), reverse=True)
        hotGood['items'].sort(cmp=lambda x, y: cmp(x['giftValue'], y['giftValue']), reverse=True)
        labelData.insert(0, hotGood)
        labelData.insert(0, newGood)
        self.baseInfo['itemData'] = labelData

    def onOpenHelp(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        keyWord = ID.data.get(itemId, []).get('name', '')
        if keyWord:
            gameglobal.rds.ui.help.show(keyWord)

    def initCountInfo(self):
        self.countInfo = [[10, gameStrings.TEXT_SPACEGIFTGIVINGPROXY_142],
         [30, gameStrings.TEXT_SPACEGIFTGIVINGPROXY_143],
         [66, gameStrings.TEXT_SPACEGIFTGIVINGPROXY_144],
         [188, gameStrings.TEXT_SPACEGIFTGIVINGPROXY_145],
         [520, gameStrings.TEXT_SPACEGIFTGIVINGPROXY_146],
         [1314, gameStrings.TEXT_SPACEGIFTGIVINGPROXY_147]]

    def onCountArray(self, *arg):
        numStr = unicode2gbk(arg[3][0].GetString().strip())
        ret = []
        for fVal in self.countInfo:
            if fVal[1].find(numStr) != -1:
                ret.append({'label': fVal[1]})

        return uiUtils.array2GfxAarry(ret, True)

    def onItemChange(self, _info):
        gamelog.debug('itemChangeEvent')
        gamelog.debug(_info)
        item = _info[3]
        itemId = item.id
        itemId = Item.parentId(itemId)
        itemData = self.findItemDataByItemId(itemId)
        gamelog.debug(itemData)
        if itemData:
            p = BigWorld.player()
            count = p.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
            itemData['itemDetail']['count'] = str(count)
            if self.mediator:
                gamelog.debug(itemData)
                self.mediator.Invoke('updateItemData', uiUtils.dict2GfxDict(itemData['itemDetail'], True))

    def onItemRemove(self, _info):
        gamelog.debug('itemRemoveEvent')
        gamelog.debug(_info)
        for _typeData in self.baseInfo['itemData']:
            for item in _typeData['items']:
                itemId = item['itemDetail']['itemId']
                p = BigWorld.player()
                count = p.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
                if item['itemDetail']['count'] != str(count):
                    item['itemDetail']['count'] = str(count)
                    if self.mediator:
                        self.mediator.Invoke('updateItemData', uiUtils.dict2GfxDict(item['itemDetail'], True))

    def onCountArrayAll(self, *arg):
        ret = []
        for fVal in self.countInfo:
            ret.append({'label': fVal[1]})

        return uiUtils.array2GfxAarry(ret, True)

    def _getLimitStr(self, itemData):
        ret = ''
        if itemData.get('limitType', 0):
            buyLimitType = itemData.get('limitType', 0)
            buyLimitCount = itemData.get('limitNum', -1)
            if buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_DAY:
                ret = gameStrings.TEXT_SPACEGIFTGIVINGPROXY_203 + str(buyLimitCount) + gameStrings.TEXT_SPACEGIFTGIVINGPROXY_203_1
            elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_WEEK:
                ret = gameStrings.TEXT_SPACEGIFTGIVINGPROXY_203 + str(buyLimitCount) + gameStrings.TEXT_SPACEGIFTGIVINGPROXY_205
            elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_MONTH:
                ret = gameStrings.TEXT_SPACEGIFTGIVINGPROXY_203 + str(buyLimitCount) + gameStrings.TEXT_SPACEGIFTGIVINGPROXY_207
            elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_FOREVER:
                ret = gameStrings.TEXT_SPACEGIFTGIVINGPROXY_203 + str(buyLimitCount) + gameStrings.TEXT_SPACEGIFTGIVINGPROXY_209
        return ret

    def onSendGift(self, *arg):
        giftId = int(arg[3][0].GetNumber())
        num = int(arg[3][1].GetNumber())
        if num == 0:
            return
        p = BigWorld.player()
        pData = PZGD.data.get(giftId, {})
        crossServerType = pData.get('crossServerType')
        if self.hostId and int(gameglobal.rds.gServerid) != self.hostId:
            if not crossServerType:
                p.showGameMsg(GMDD.data.PERSONAL_ZONE_GIFT_CROSS_SERVER_FORBID, ())
                return
        self.__sendGift(giftId, num)

    def __sendGift(self, giftId, num):
        p = BigWorld.player()
        p.cell.sendZoneGift(self.ownerGbID, giftId, num, self.hostId)

    def findItemDataByGiftId(self, giftId):
        for _typeData in self.baseInfo['itemData']:
            for item in _typeData['items']:
                if item['giftId'] == giftId:
                    return item

    def findItemDataByItemId(self, itemId):
        for _typeData in self.baseInfo['itemData']:
            for item in _typeData['items']:
                if item['itemDetail']['itemId'] == itemId:
                    return item

    def getValue(self, key):
        if key == '':
            return uiUtils.array2GfxAarry([], True)

    def show(self, ownerGbID, ownerName, hostId = 0, giftId = 0, showType = gametypes.SPACE_GIFT_GIVING_POPULARITY):
        self.showType = showType
        self.ownerGbID = int(ownerGbID)
        self.hostId = int(hostId)
        self.baseInfo['roleName'] = ownerName
        self.baseInfo['selectedGiftId'] = giftId
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SPACEGIFT_GIVING)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SPACEGIFT_GIVING)
        if BigWorld.player():
            if BigWorld.player().__class__.__name__ == 'PlayerAvatar':
                BigWorld.player().unRegisterEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
                BigWorld.player().unRegisterEvent(const.EVENT_ITEM_REMOVE, self.onItemRemove)
                gamelog.debug('unRegisterEvent')

    def reset(self):
        self.baseInfo = {}
        self.option = 0
        self.page = 0
        self.pos = None
        self.curPage = None
        self.pageList = {}
        self.countInfo = []
        self.hostId = 0

    def getMediatorInitData(self):
        if self.showType == gametypes.SPACE_GIFT_GIVING_POPULARITY:
            return {'titleName': gameStrings.SPACE_GIFT_GIVING_TITLE,
             'valueLabel': gameStrings.SPACE_GIFT_GIVING_VALUE_LABEL}
        if self.showType == gametypes.SPACE_GIFT_GIVING_MISS_GROUP_VOTE:
            return {'titleName': gameStrings.MISS_GROUP_VOTE_TITLE,
             'valueLabel': gameStrings.MISS_GROUP_VOTE_VALUE_LABEL}

    def isGiftForVote(self, giftId):
        return bool(PZGD.data.get(giftId, {}).get('missTianyuVal', None))

    def filterItemByShowType(self, giftId, showType):
        if showType == gametypes.SPACE_GIFT_GIVING_POPULARITY:
            return True
        if showType == gametypes.SPACE_GIFT_GIVING_MISS_GROUP_VOTE:
            return self.isGiftForVote(giftId)
        return True
