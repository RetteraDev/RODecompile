#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bFReportChooseProxy.o
import BigWorld
import uiConst
import uiUtils
import gameglobal
from uiProxy import UIProxy

class BFReportChooseProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BFReportChooseProxy, self).__init__(uiAdapter)
        self.modelMap = {'reportPlayer': self.onReportPlayer}
        self.mediator = None
        self.initData = []
        self.playerName = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_BFREPORT_CHOOSE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_BFREPORT_CHOOSE:
            self.mediator = mediator
            self.initData = self._genInitData()
            return uiUtils.array2GfxAarry(self.initData, True)

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_BFREPORT_CHOOSE)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BFREPORT_CHOOSE)

    def reset(self):
        self.mediator = None
        self.initData = []
        self.playerName = ''

    def onReportPlayer(self, *arg):
        gbidstr = arg[3][0].GetString()
        if gbidstr:
            gbid = long(gbidstr)
            gameglobal.rds.ui.bFReportReason.show(gbid, self.getPlayerName(gbid))
            self.hide()

    def _genInitData(self):
        ret = []
        p = BigWorld.player()
        bfTeam = p.battleFieldTeam
        for key, value in bfTeam.items():
            sideNUID = value.get('sideNUID', 0)
            if sideNUID == p.bfSideNUID and key != p.gbId and value.get('isOn', False):
                data = {}
                data['gbid'] = str(key)
                data['playerName'] = value.get('roleName', '')
                ret.append(data)

        return ret

    def getPlayerName(self, gbid):
        name = ''
        p = BigWorld.player()
        bfTeam = p.battleFieldTeam
        for key, value in bfTeam.items():
            if key == gbid:
                name = value.get('roleName', '')

        return name
