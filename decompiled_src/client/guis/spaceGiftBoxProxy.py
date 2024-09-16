#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/spaceGiftBoxProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import const
from guis.uiProxy import DataProxy
from guis import uiConst
from guis import uiUtils
from gamestrings import gameStrings
from data import personal_zone_gift_data as PZGD
from data import sys_config_data as SCD
LABELTYPE = {0: gameStrings.TEXT_ACTIVITYFACTORY_107,
 1: gameStrings.TEXT_SPACEGIFTBOXPROXY_17,
 2: gameStrings.TEXT_SPACEGIFTBOXPROXY_18,
 3: gameStrings.TEXT_SPACEGIFTBOXPROXY_19,
 4: gameStrings.TEXT_SPACEGIFTBOXPROXY_20}
SENDSTR = {0: gameStrings.TEXT_SPACEGIFTBOXPROXY_24,
 1: gameStrings.TEXT_SPACEGIFTBOXPROXY_25}

class SpaceGiftBoxProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(SpaceGiftBoxProxy, self).__init__(uiAdapter)
        self.bindType = 'spaceGiftBox'
        self.modelMap = {'getInitInfo': self.onGetInitInfo,
         'openFriendList': self.onOpenFriendList,
         'setCurTab': self.onSetCurTab,
         'getTopListData': self.onGetTopListData,
         'openGiftGiving': self.onOpenGiftGiving}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SPACE_GIFTBOX, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SPACE_GIFTBOX:
            self.mediator = mediator

    def onSetCurTab(self, *arg):
        self.curTab = int(arg[3][0].GetNumber())

    def onOpenFriendList(self, *arg):
        p = BigWorld.player()
        if self.ownerGbID:
            p.base.getZoneGiftHistory(self.ownerGbID)

    def onGetTopListData(self, *arg):
        if not self.mediator:
            return
        _data = self.baseInfo.get('giftTop', {}).get(self.curTab, 0)
        ret = []
        if _data:
            for mGbId in _data:
                mName = _data[mGbId][0]
                photo = _data[mGbId][1]
                giftNum = _data[mGbId][2]
                hostId = 0
                if photo.find('##') != -1:
                    photo, hostId = photo.split('##')
                    hostId = int(hostId)
                if giftNum == 0:
                    continue
                spaceType = self.baseInfo.get('spaceType', 0)
                sendStr = SENDSTR.get(spaceType, '') + gameStrings.PERSONAL_ZONE_GIFT_MSG if spaceType else '%d%s'
                ret.append({'nameTxt': mName,
                 'photo': photo,
                 'hostId': hostId,
                 'giftNum': giftNum,
                 'dateTxt': '',
                 'msgTxt': sendStr % (giftNum, LABELTYPE.get(self.curTab, '') if self.curTab else gameStrings.TEXT_SPACEGIFTBOXPROXY_74),
                 'gbId': str(mGbId)})

            ret.sort(cmp=lambda x, y: cmp(x['giftNum'], y['giftNum']), reverse=True)
            for i in xrange(len(ret)):
                ret[i]['topRank'] = i + 1

        return uiUtils.array2GfxAarry(ret, True)

    def onOpenGiftGiving(self, *arg):
        gameglobal.rds.ui.spaceGiftGiving.show(self.ownerGbID, self.baseInfo['roleName'])

    def onGetZoneGiftHistory(self, data):
        if not self.mediator:
            return
        p = BigWorld.player()
        ret = []
        for value in data:
            mGbId = 0
            mName = ''
            photo = ''
            giftId = 0
            giftNum = 0
            mGbIdd = 0
            borderId = 0
            if len(value) == 6:
                mGbId, mName, photo, giftId, giftNum, mGbIdd = value
            elif len(value) == 7:
                mGbId, mName, photo, giftId, giftNum, mGbIdd, borderId = value
            if not borderId:
                borderId = SCD.data.get('defaultBorderId', 0)
            if giftNum == 0:
                continue
            if self.curTab == 0 or PZGD.data.get(giftId, {}).get('type', '') == self.curTab:
                spaceType = self.baseInfo.get('spaceType', 0)
                sendStr = SENDSTR.get(spaceType, '') + gameStrings.PERSONAL_ZONE_GIFT_MSG if spaceType else '%d%s'
                ret.append({'nameTxt': mName,
                 'photo': photo,
                 'dateTxt': '',
                 'msgTxt': sendStr % (giftNum, PZGD.data.get(giftId, {}).get('name', '')),
                 'newIcon': False,
                 'gbId': str(mGbId),
                 'isShow': 1,
                 'photoBorderIcon': p.getPhotoBorderIcon(borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)})

        gameglobal.rds.ui.friendList.show(ret)

    def typeGiftInfo(self):
        labelData = []
        for key in LABELTYPE:
            tempItem = {'labelName': LABELTYPE[key],
             'items': []}
            labelData.append(tempItem)

        for _id in self.baseInfo['giftDict']:
            if self.baseInfo['giftDict'][_id] == 0:
                continue
            itemId = PZGD.data.get(_id, {}).get('itemId', 0)
            itemDetail = uiUtils.getGfxItemById(itemId, self.baseInfo['giftDict'][_id], uiConst.ICON_SIZE64)
            _type = PZGD.data.get(_id, {}).get('type', 0)
            labelItem = {'giftId': _id,
             'itemDetail': itemDetail}
            labelData[_type]['items'].append(labelItem)
            labelData[0]['items'].append(labelItem)

        self.baseInfo['itemData'] = labelData

    def onGetInitInfo(self, *arg):
        self.typeGiftInfo()
        return uiUtils.dict2GfxDict(self.baseInfo, True)

    def show(self, ownerGbID, roleName, data, num, spaceType, hostId = 0):
        self.ownerGbID = ownerGbID
        self.hostId = hostId
        self.baseInfo['roleName'] = roleName
        self.baseInfo['spaceType'] = spaceType
        self.baseInfo['giftDict'] = data.get(const.PERSONAL_ZONE_DATA_GIFT_DICT, {})
        self.baseInfo['weekGiftNum'] = data.get(const.PERSONAL_ZONE_DATA_GIFT_WEEK_NUM, 0)
        self.baseInfo['giftTop'] = data.get(const.PERSONAL_ZONE_DATA_GIFT_TOP, {})
        self.baseInfo['giftNum'] = num
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SPACE_GIFTBOX)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SPACE_GIFTBOX)

    def reset(self):
        self.baseInfo = {}
        self.curTab = 0
        self.hostId = 0
