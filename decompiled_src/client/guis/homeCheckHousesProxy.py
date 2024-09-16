#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/homeCheckHousesProxy.o
import BigWorld
import gameglobal
import const
from Scaleform import GfxValue
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from gameStrings import gameStrings
from data import home_data as HD
from data import enlarge_room_data as ERD
from data import home_wealth_value_data as HWVD
from data import fitting_room_upgrade_data as FRUD
from cdata import game_msg_def_data as GMDD

class HomeCheckHousesProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(HomeCheckHousesProxy, self).__init__(uiAdapter)
        self.modelMap = {'getKeyList': self.onGetKeyList,
         'getContentInfo': self.onGetContentInfo,
         'transferToRoom': self.onTransferToRoom,
         'giveBackKey': self.onGiveBackKey}
        self.mediator = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_HOME_CHECKHOUSES, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_HOME_CHECKHOUSES:
            self.mediator = mediator

    def show(self, b):
        self.jieqiHasHome = b
        p = BigWorld.player()
        p.base.queryReceivedRoomAuth()

    def openPanel(self, data):
        self.receivedData = data
        self.getKeyList()
        if not self.keyInfo:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.PLAYER_NO_HOME_KEYS, ())
            if gameglobal.rds.ui.funcNpc.isOnFuncState():
                gameglobal.rds.ui.funcNpc.onDefaultState()
            return
        if self.mediator:
            self.refreshList()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_HOME_CHECKHOUSES)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_HOME_CHECKHOUSES)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        self.receivedData = {}
        self.keyInfo = []
        self.curSelData = {}
        self.curSelGbId = None
        self.jieqiHasHome = False

    def onGetKeyList(self, *args):
        self.getKeyList()
        return uiUtils.array2GfxAarry(self.keyInfo, True)

    def getKeyList(self, data = {}):
        self.keyInfo = []
        p = BigWorld.player()
        if p.myHome.hasHome():
            hostInfo = {'gbId': p.gbId,
             'name': gameStrings.HOME_CHECK_HOUSE_KEY2 % p.roleName,
             'keyType': 'host'}
            self.keyInfo.append(hostInfo)
        if self.jieqiHasHome and p.friend.intimacyTgt:
            jieqiInfo = {'gbId': p.friend.intimacyTgt,
             'name': gameStrings.HOME_CHECK_HOUSE_KEY2 % p.friend[p.friend.intimacyTgt].name,
             'keyType': 'jieqi'}
            self.keyInfo.append(jieqiInfo)
        if self.receivedData:
            for gbId, name in self.receivedData.iteritems():
                guestInfo = {'gbId': gbId,
                 'name': gameStrings.HOME_CHECK_HOUSE_KEY % name,
                 'keyType': 'guest'}
                self.keyInfo.append(guestInfo)

    def onGetContentInfo(self, *args):
        _index = int(args[3][0].GetNumber())
        p = BigWorld.player()
        p.cell.queryRoomInfo(const.HOME_QUERY_HOME_KEY, self.keyInfo[_index]['gbId'])

    def setCurData(self, gbId, data):
        self.curSelData = data
        self.curSelGbId = gbId

    def refreshCurContent(self):
        contentData = {}
        contentData['lv'] = self.curSelData.get(const.HOME_DATA_TYPE_LV, 0)
        contentData['name'] = self.curSelData.get(const.HOME_DATA_TYPE_NAME, '')
        contentData['sex'] = self.curSelData.get(const.HOME_DATA_TYPE_SEX, 0)
        _school = self.curSelData.get(const.HOME_DATA_TYPE_SCHOOL, 0)
        contentData['school'] = const.SCHOOL_DICT.get(_school, '')
        contentData['floorNo'] = self.curSelData.get(const.HOME_DATA_TYPE_FLOOR_NO, 1)
        roomNo = self.curSelData.get(const.HOME_DATA_TYPE_ROOM_NO, 1)
        contentData['roomNo'] = self._getColorByRoomNo(roomNo)
        contentData['roomId'] = self.curSelData.get(const.HOME_DATA_TYPE_ROOM_ID, 0)
        _wealthValue = self.curSelData.get(const.HOME_DATA_TYPE_ROOM_WEALTH, 0)
        contentData['wealth'] = self.getWealthLv(_wealthValue)
        contentData['housingType'] = HD.data.get(contentData['roomId'], {}).get('housingType', 0)
        contentData['housingTypeTips'] = HD.data.get(contentData['roomId'], {}).get('housingTypeTips', '')
        p = BigWorld.player()
        contentData['bGiveBackKey'] = self.curSelGbId != p.gbId and self.curSelGbId != p.friend.intimacyTgt or self.curSelGbId in self.receivedData
        contentData['fittingRoomLv'] = self.curSelData.get(const.HOME_DATA_TYPE_FITTINGROOM_LV, 0)
        contentData['enlargeRoomId'] = self.curSelData.get(const.HOME_DATA_TYPE_ENLARGED_ROOM, 0)
        if self.mediator:
            self.mediator.Invoke('refreshCurContent', uiUtils.dict2GfxDict(contentData, True))

    def _getColorByRoomNo(self, roomNo):
        return uiConst.ROOM_NO_COLOR.get(roomNo, '')

    def onTransferToRoom(self, *args):
        _index = int(args[3][0].GetNumber())
        if _index < len(self.keyInfo):
            p = BigWorld.player()
            p.cell.enterRoomDirectlyByGbID(self.keyInfo[_index].get('gbId', 0))
            self.hide()

    def onGiveBackKey(self, *args):
        _index = int(args[3][0].GetNumber())
        if _index < len(self.keyInfo):
            p = BigWorld.player()
            p.cell.giveupRoomAuth(self.keyInfo[_index].get('gbId', 0))

    def getWealthLv(self, value):
        _data = HWVD.data
        beginNum = 0
        maxNum = 0
        lv = 0
        for key, item in _data.items():
            maxNum = item.get('maxVal')
            if value >= beginNum and value <= maxNum:
                lv = key
            beginNum = maxNum + 1

        if value > maxNum:
            lv = len(_data)
        return _data.get(lv, {}).get('name', 'Lv1')

    def getWealthLvMaxVal(self, value):
        _data = HWVD.data
        beginNum = 0
        maxNum = 0
        lv = 0
        for key, item in _data.items():
            maxNum = item.get('maxVal')
            if value >= beginNum and value <= maxNum:
                lv = key
            beginNum = maxNum + 1

        if value > maxNum:
            lv = len(_data)
        return _data.get(lv, {}).get('maxVal', 0)

    def refreshList(self):
        self.mediator.Invoke('refreshList')
