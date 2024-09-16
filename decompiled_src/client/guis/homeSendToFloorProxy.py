#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/homeSendToFloorProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from data import home_data as HD

class HomeSendToFloorProxy(UIProxy):
    ROOM_NUM = 9

    def __init__(self, uiAdapter):
        super(HomeSendToFloorProxy, self).__init__(uiAdapter)
        self.modelMap = {'getFloorInfo': self.onGetFloorInfo,
         'getMaxFloor': self.onGetMaxFloor,
         'transferFloor': self.onTransferFloor}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_HOME_SENDTO_FLOOR, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_HOME_SENDTO_FLOOR:
            self.mediator = mediator
            self.refreshItems(-1, {})

    def show(self, maxFloorNum):
        self.maxFloorNum = maxFloorNum
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_HOME_SENDTO_FLOOR)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_HOME_SENDTO_FLOOR)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        self.maxFloorNum = 0
        self.serverData = {}

    def refreshItems(self, floorNo, serverData):
        self.serverData = serverData
        if self.mediator:
            ret = {}
            for key in serverData:
                roomId = serverData.get(key, {}).get(const.HOME_DATA_TYPE_ROOM_ID, 0)
                roomNo = serverData.get(key, {}).get(const.HOME_DATA_TYPE_ROOM_NO, 1)
                _wealth = serverData.get(key, {}).get(const.HOME_DATA_TYPE_ROOM_WEALTH, 0)
                wealthLv = gameglobal.rds.ui.homeCheckHouses.getWealthLv(_wealth)
                itemData = {'name': serverData.get(key, {}).get(const.HOME_DATA_TYPE_NAME, ''),
                 'sex': serverData.get(key, {}).get(const.HOME_DATA_TYPE_SEX, 1),
                 'roomNo': roomNo,
                 'wealth': wealthLv,
                 'housingType': HD.data.get(roomId, {}).get('housingType', 0),
                 'housingTypeTips': HD.data.get(roomId, {}).get('housingTypeTips', '')}
                ret[roomNo - 1] = itemData

            self.mediator.Invoke('setItem', uiUtils.dict2GfxDict(ret, True))

    def onGetFloorInfo(self, *args):
        floorNo = int(args[3][0].GetNumber())
        p = BigWorld.player()
        p.cell.queryFloorInfo(p.myHome.curLineNo, floorNo)

    def onGetMaxFloor(self, *args):
        return GfxValue(self.maxFloorNum)

    def onTransferFloor(self, *args):
        floorNo = int(args[3][0].GetNumber())
        p = BigWorld.player()
        p.cell.enterFloor(floorNo)
        self.hide()
