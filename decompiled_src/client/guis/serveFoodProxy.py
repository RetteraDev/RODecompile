#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/serveFoodProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
from uiProxy import UIProxy
from data import guild_config_data as GCD

class ServeFoodProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ServeFoodProxy, self).__init__(uiAdapter)
        self.modelMap = {'serveFood': self.onServeFood}
        self.mediator = None
        self.entId = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SERVE_FOOD, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SERVE_FOOD:
            self.mediator = mediator
            fee = GCD.data.get('treatFee', const.GUILD_RESTAURANT_TREAT_FEE)
            return GfxValue(fee)

    def show(self, entId):
        self.entId = entId
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SERVE_FOOD)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SERVE_FOOD)

    def onServeFood(self, *arg):
        if not self.entId:
            return
        ent = BigWorld.entities.get(self.entId)
        if not ent:
            return
        BigWorld.player().cell.guildTreatResident(ent.geId, self.entId)
        gameglobal.rds.ui.pressKeyF.isGuildEntity = False
        gameglobal.rds.ui.pressKeyF.removeType(const.F_GUILDTREAT)
        gameglobal.rds.ui.guild.residentNpcId = 0
        gameglobal.rds.ui.guild.bNeedTreat = False
        self.hide()
