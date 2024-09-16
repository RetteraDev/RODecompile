#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mountsProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from data import ride_together_data as RTD

class MountsProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MountsProxy, self).__init__(uiAdapter)
        self.modelMap = {'getMountsInfo': self.onGetMountsInfo,
         'exitRideTogether': self.onExitRideTogether,
         'removeMember': self.onRemoveMember,
         'clickTarget': self.onClickTarget}
        self.mediator = None
        self.seatNum = 0
        self.uiPos = 0

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_MOUNTS:
            self.mediator = mediator

    def reset(self):
        self.mediator = None

    def show(self):
        if BigWorld.player().isOnRideTogetherHorse() or BigWorld.player().tride.inRide():
            mountId = self._getMountId()
            if mountId != 0 and not RTD.data.get(mountId, {}).get('ignore', 0):
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MOUNTS)
                self.refreshView()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MOUNTS)

    def rideInFly(self):
        inFly = False
        if BigWorld.player().tride.inRide():
            header = BigWorld.player().tride.getHeader()
            if header:
                inFly = getattr(header, 'inFly', False)
        elif BigWorld.player().isOnRideTogetherHorse():
            inFly = BigWorld.player().inFly
        return inFly

    def onGetMountsInfo(self, *arg):
        self.refreshView()

    def refresFlyView(self):
        mountId = self._getMountId()
        if mountId == 0:
            return
        rtdData = RTD.data.get(mountId, {})
        if not rtdData:
            return
        if not rtdData.has_key('inFlyPic'):
            return
        self.refreshView()

    def refreshView(self):
        mountId = self._getMountId()
        if mountId == 0:
            return
        else:
            icon = ''
            self.uiPos = []
            rtdData = RTD.data.get(mountId, {})
            if rtdData != None:
                icon = rtdData.get('pic', '')
                self.seatNum = rtdData.get('seatNum', 0)
                self.uiPos = rtdData.get('uiPos', {})
                if rtdData.has_key('inFlyPic') and self.rideInFly():
                    icon = rtdData.get('inFlyPic')
                    self.uiPos = rtdData.get('inFlyUiPos', self.uiPos)
            ret = {}
            ret['icon'] = icon
            ret['count'] = self.seatNum + 1
            ret['players'] = self.getRidingRoles()
            if self.mediator:
                self.mediator.Invoke('setData', uiUtils.dict2GfxDict(ret, True))
            return

    def getRidingRoles(self):
        list = []
        p = BigWorld.player()
        isHost = False
        isInit = True
        for i in self.uiPos:
            ret = {}
            entityId = p.getIdByTrideIdx(i)
            if entityId != 0 and entityId != None:
                ret['index'] = i
                ret['isEmpty'] = False
                ret['entityId'] = entityId
                ret['isEmpty'] = False
                entity = BigWorld.entities.get(int(entityId))
                if entity:
                    ret['name'] = entity.roleName
                else:
                    ret['name'] = ''
                ret['pos'] = self.uiPos[i]
                if isInit:
                    isHost = i == 0 and p.id == entityId
                    isInit = False
                ret['isHost'] = isHost
                ret['isSelf'] = entityId == p.id
            else:
                ret['isEmpty'] = True
                ret['pos'] = self.uiPos[i]
            list.append(ret)

        return uiUtils.array2GfxAarry(list, True)

    def onExitRideTogether(self, *arg):
        p = BigWorld.player()
        if not p.tride.inRide():
            p.leaveRide()
        else:
            p.cancelRideTogether()
            p.leaveRide()
        self.refreshView()

    def onRemoveMember(self, *arg):
        goAwayMember = arg[3][0].GetNumber()
        BigWorld.player().removeRideTogether(int(goAwayMember))

    def onClickTarget(self, *arg):
        entityId = arg[3][0].GetNumber()
        ent = BigWorld.entities.get(int(entityId))
        BigWorld.player().lockTarget(ent)

    def _getMountId(self):
        mountId = 0
        if BigWorld.player().tride.inRide():
            header = BigWorld.player().tride.getHeader()
            if header:
                mountId = header.bianshen[1]
        elif BigWorld.player().isOnRideTogetherHorse():
            mountId = BigWorld.player().bianshen[1]
        return mountId
