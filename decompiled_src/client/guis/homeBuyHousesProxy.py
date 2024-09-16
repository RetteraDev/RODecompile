#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/homeBuyHousesProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gametypes
import gameglobal
from callbackHelper import Functor
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from cdata import home_config_data as HCD
from cdata import game_msg_def_data as GMDD

class HomeBuyHousesProxy(UIProxy):
    ROOM_NUM = 9

    def __init__(self, uiAdapter):
        super(HomeBuyHousesProxy, self).__init__(uiAdapter)
        self.modelMap = {'getNeedCash': self.onGetNeedCash,
         'getMaxFloor': self.onGetMaxFloor,
         'confirmBuy': self.onConfirmBuy,
         'getColorByIndex': self.onGetColorByIndex,
         'initSelectIndex': self.onInitSelectIndex,
         'getDoorItemData': self.onGetDoorItemData}
        self.cashNeed = HCD.data.get('createHomeCashNeed', 0)
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_HOME_BUYHOUSES, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_HOME_BUYHOUSES:
            self.mediator = mediator

    def show(self, maxFloor, serverData):
        if len(serverData) == HomeBuyHousesProxy.ROOM_NUM:
            self.serverData = {}
            self.maxFloor = maxFloor + 1
        else:
            self.serverData = serverData
            self.maxFloor = maxFloor
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_HOME_BUYHOUSES)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_HOME_BUYHOUSES)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        self.maxFloor = 0
        self.serverData = {}

    def onGetMaxFloor(self, *args):
        msg = gameStrings.TEXT_HOMEBUYHOUSESPROXY_62 % str(self.maxFloor)
        return GfxValue(gbk2unicode(msg))

    def onGetNeedCash(self, *args):
        msg = gameStrings.TEXT_HOMEBUYHOUSESPROXY_66 % str(self.cashNeed)
        return GfxValue(gbk2unicode(msg))

    def onGetColorByIndex(self, *args):
        roomNo = int(args[3][0].GetNumber()) + 1
        return GfxValue(gbk2unicode(uiConst.ROOM_NO_COLOR.get(roomNo, '')))

    def onConfirmBuy(self, *args):
        roomNo = int(args[3][0].GetNumber()) + 1
        p = BigWorld.player()
        itemId = HCD.data.get('BUY_HOME_DEED_ID', 369800)
        itemData = uiUtils.getGfxItemById(itemId)
        count = p.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
        itemData['count'] = uiUtils.convertNumStr(count, 1)
        cash = HCD.data.get('createHomeCashNeed', 0)
        bonusIcon = {'bonusType': 'bindCash',
         'value': str(cash)}
        pg, ps = p.inv.findItemInPages(itemId)
        if p.cash + p.bindCash < cash:
            p.showGameMsg(GMDD.data.HOME_BUY_CASH_NOT_ENOUGH, ())
            return
        if pg == -1 or ps == -1:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_HOMEBUYHOUSESPROXY_88, itemData=itemData, bonusIcon=bonusIcon, yesBtnEnable=False, noCallback=p.openBuyHouse, style=uiConst.MSG_BOX_BUY_ITEM)
            self.hide()
            return
        _maxFloor = self.maxFloor

        def _buyCallFunc():
            self.confirmYesCallBack(p.myHome.curLineNo, _maxFloor, roomNo, pg, ps)

        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_HOMEBUYHOUSESPROXY_88, Functor(p.confirmCashPay, cash, _buyCallFunc), itemData=itemData, style=uiConst.MSG_BOX_BUY_ITEM, bonusIcon=bonusIcon, noCallback=p.openBuyHouse)
        self.hide()

    def confirmYesCallBack(self, lineNo, floor, roomNo, pg, ps):
        p = BigWorld.player()
        p.cell.createRoomApply(lineNo, floor, roomNo, pg, ps)

    def onInitSelectIndex(self, *args):
        if not self.serverData:
            return GfxValue(0)
        if len(self.serverData) == HomeBuyHousesProxy.ROOM_NUM:
            return GfxValue(-1)
        for n in xrange(0, HomeBuyHousesProxy.ROOM_NUM):
            if not self.serverData.get(n + 1, False):
                return GfxValue(n)

        return GfxValue(0)

    def onGetDoorItemData(self, *args):
        return uiUtils.dict2GfxDict(self.serverData, True)
