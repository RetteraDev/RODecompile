#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fameCashExchangeProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
import gameglobal
from guis import uiConst
from guis import uiUtils
from cdata import fame_cash_exchange_data as FCED
from data import fame_data as FD

class FameCashExchangeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FameCashExchangeProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirmExchange': self.onConfirmExchange}
        self.mediator = None
        self.npcId = 0
        self.fameId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_FAME_CASH_EXCHANGE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FAME_CASH_EXCHANGE:
            self.mediator = mediator
            return self._getFameCashData()

    def show(self, npcId, fameId):
        self.npcId = npcId
        self.fameId = fameId
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FAME_CASH_EXCHANGE)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FAME_CASH_EXCHANGE)
        gameglobal.rds.ui.funcNpc.close()

    def _getFameCashData(self):
        p = BigWorld.player()
        data = FCED.data.get(self.fameId, {})
        needToken = data.get('needToken', [0, 0])
        needCer = data.get('needCer', [0, 0])
        getCash = data.get('getCash', 0)
        fameName1 = FD.data.get(needToken[0], {}).get('name', gameStrings.TEXT_CHALLENGEPROXY_199_1)
        fameNeed1 = needToken[1]
        fameOwn1 = p.fame.get(needToken[0], 0)
        fameName2 = FD.data.get(needCer[0], {}).get('name', gameStrings.TEXT_CHALLENGEPROXY_199_1)
        fameNeed2 = needCer[1]
        fameOwn2 = p.fame.get(needCer[0], 0)
        ret = {}
        ret['fameName1'] = fameName1
        ret['fameNeed1'] = fameNeed1
        ret['fameOwn1'] = fameOwn1
        ret['fameName2'] = fameName2
        ret['fameNeed2'] = fameNeed2
        ret['fameOwn2'] = fameOwn2
        ret['getCash'] = getCash
        return uiUtils.dict2GfxDict(ret, True)

    def onConfirmExchange(self, *arg):
        amount = int(arg[3][0].GetNumber())
        if self.fameId == 0:
            return
        BigWorld.player().cell.fameToCash(int(self.fameId), amount)
        self.hide()
