#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/goHomeProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
from uiProxy import UIProxy

class GoHomeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GoHomeProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm,
         'getMultiDestination': self.onGetMultiDestination}
        self.mediator = None
        self.destData = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_GO_HOME, self.hide)

    def show(self, destData):
        self.destData = destData
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GO_HOME)

    def reset(self):
        self.destData = {}

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GO_HOME:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GO_HOME)

    def onConfirm(self, *arg):
        destination = arg[3][0].GetString()
        BigWorld.player().cell.useGuildMemberSkillWithParam(uiConst.GUILD_SKILL_HC, (destination,))
        self.hide()

    def onGetMultiDestination(self, *arg):
        obj = self.movie.CreateObject()
        for key, value in self.destData.iteritems():
            obj.SetMember(key, GfxValue(value))

        return obj
