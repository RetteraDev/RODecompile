#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/frozenPunishProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
from guis import uiConst, uiUtils
from uiProxy import UIProxy
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD

class FrozenPunishProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FrozenPunishProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirmPayBail': self.onConfirmPayBail,
         'getinitData': self.onGetinitData}
        uiAdapter.registerEscFunc(uiConst.WIDGET_FROZEN_PUNISH, self.hide)

    def _registerMediator(self, widgetId, mediator):
        pass

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FROZEN_PUNISH)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def onConfirmPayBail(self, *args):
        p = BigWorld.player()
        p.cell.unfreezeCashByBail()
        gameglobal.rds.ui.funcNpc.close()
        self.clearWidget()

    def isShowFrozenPunish(self):
        ret = False
        p = BigWorld.player()
        freezeCash = getattr(p, 'freezeCash')
        maxFreezeCash = getattr(p, 'maxFreezeCash')
        notEnoughCash = maxFreezeCash - freezeCash
        if freezeCash != 0 or notEnoughCash != 0:
            ret = True
        return ret

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FROZEN_PUNISH)

    def onGetinitData(self, *args):
        ret = {}
        p = BigWorld.player()
        freezeCash = getattr(p, 'freezeCash')
        freezeCashBail = getattr(p, 'freezeCashBail')
        msg = GMD.data.get(GMDD.data.FROZEN_PUNISH_MSG, {}).get('text', gameStrings.TEXT_FROZENPUNISHPROXY_51)
        msg = msg % (freezeCash, freezeCashBail)
        ret['msg'] = msg
        ret['cash'] = str(freezeCashBail)
        return uiUtils.dict2GfxDict(ret, True)
