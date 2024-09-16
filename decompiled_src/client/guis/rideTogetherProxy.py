#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/rideTogetherProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
from guis import uiConst
from uiProxy import UIProxy
from guis import uiUtils

class RideTogetherProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RideTogetherProxy, self).__init__(uiAdapter)
        self.modelMap = {'exitRideTogether': self.onExitRideTogether,
         'closeWidget': self.onCloseWidget,
         'handleSubmitClick': self.onSubmitClick,
         'handleCancelClick': self.onCancelClick,
         'getRidingRoles': self.onGetRidingRoles,
         'getRidingMode': self.onGetRidingMode}
        self.bRTListShow = False
        self.btnMediator = None
        self.listMediator = None
        self.widgetBtnId = uiConst.WIDGET_RIDE_TOGETHER
        self.widgetListId = uiConst.WIDGET_RIDE_TOGETHER_LIST

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.widgetBtnId:
            self.btnMediator = mediator
        elif widgetId == self.widgetListId:
            self.listMediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(self.widgetBtnId)

    def clearWidget(self):
        self.btnMediator = None
        gameglobal.rds.ui.unLoadWidget(self.widgetBtnId)

    def reset(self):
        pass

    def setRTListVisible(self, visible):
        self.bRTListShow = visible
        if visible:
            gameglobal.rds.ui.loadWidget(self.widgetListId)
        else:
            gameglobal.rds.ui.unLoadWidget(self.widgetListId)

    def refreshRTlist(self):
        if not self.bRTListShow:
            return
        if len(BigWorld.player().tride.keys()) <= 0:
            self.setRTListVisible(False)
            return
        if self.listMediator:
            self.listMediator.Invoke('updateMemberList')

    def onExitRideTogether(self, *arg):
        p = BigWorld.player()
        if p.isOnRideTogetherHorse():
            self.setRTListVisible(True)
        else:
            p.cancelRideTogether()

    def onCloseWidget(self, *arg):
        self.setRTListVisible(False)

    def onSubmitClick(self, *arg):
        goAwayList = uiUtils.gfxArray2Array(arg[3][0])
        if goAwayList is not None:
            for item in goAwayList:
                BigWorld.player().removeRideTogether(int(item.GetNumber()))

        self.setRTListVisible(False)

    def onCancelClick(self, *arg):
        self.setRTListVisible(False)

    def onGetRidingRoles(self, *arg):
        others = BigWorld.player().tride.keys()
        ret = []
        for i in xrange(len(others)):
            tmp = {}
            otherPlayer = BigWorld.entities.get(others[i])
            if not otherPlayer:
                continue
            tmp['id'] = others[i]
            tmp['name'] = otherPlayer.roleName
            ret.append(tmp)

        return uiUtils.array2GfxAarry(ret, True)

    def onGetRidingMode(self, *arg):
        ret = 1 if BigWorld.player().isOnRideTogetherHorse() else 2
        return GfxValue(ret)
