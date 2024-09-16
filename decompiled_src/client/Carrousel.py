#Embedded file name: I:/bag/tmp/tw2/res/entities\client/Carrousel.o
import BigWorld
from iDisplay import IDisplay
from iNpc import INpc
from data import carrousel_data as CD
from cdata import game_msg_def_data as GMDD

class Carrousel(INpc, IDisplay):

    def __init__(self):
        super(Carrousel, self).__init__()
        self.isLeaveWorld = False

    def getItemData(self):
        itemData = CD.data.get(self.carrouselId, {})
        return itemData

    def needBlackShadow(self):
        data = self.getItemData()
        noBlackUfo = data.get('noBlackUfo', False)
        return not noBlackUfo

    def set_seats(self, old):
        removeSet = set(old.keys()) - set(self.seats.keys())
        for k in removeSet:
            self.modelServer.removeCarrouselSeat(old.get(k, 0))

    def use(self):
        if self.isValidUse():
            BigWorld.player().cell.useCarrousel(self.id)

    def isValidUse(self):
        if BigWorld.player().id in self.seats:
            return False
        data = CD.data.get(self.carrouselId, {})
        seatNum = data.get('seatNum', 0)
        hasNum = len(self.seats.keys())
        if hasNum >= seatNum:
            BigWorld.player().showGameMsg(GMDD.data.CARROUSEL_SEAT_FULL, ())
            return False
        return True

    def enterWorld(self):
        super(Carrousel, self).enterWorld()
        self.initYaw = self.yaw
        self.roleName = CD.data.get(self.carrouselId, {}).get('name')

    def afterModelFinish(self):
        super(Carrousel, self).afterModelFinish()
        self.filter = BigWorld.DumbFilter()
        self.filter.clientYawMinDist = 0.0
        self.filter.setYaw(self.initYaw)
        itemData = CD.data.get(self.carrouselId, None)
        scale = itemData.get('modelScale', 1.0)
        self.model.scale = (scale, scale, scale)
        self.model.setModelNeedHide(False, 1.0)
        carrierAct = itemData.get('carrierAct', '1101')
        self.model.action(carrierAct)()
        self.setTargetCapsUse(self.canSelected())
        self.refreshSeatModel()
        clientEntityId = getattr(self, 'clientEntityId', None)
        if clientEntityId:
            BigWorld.player().hideClientShip(clientEntityId)

    def refreshSeatModel(self):
        if self.seats:
            for eid, seatIdx in self.seats.iteritems():
                entity = BigWorld.entities.get(eid, None)
                if entity and hasattr(entity, 'inCarrousel') and entity.inCarrousel():
                    entity.modelServer.enterCarrousel()

    def leaveWorld(self):
        super(Carrousel, self).leaveWorld()
        clientEntityId = getattr(self, 'clientEntityId', None)
        if clientEntityId:
            BigWorld.player().showClientShip(clientEntityId)

    def getOpacityValue(self):
        opacityVal = super(Carrousel, self).getOpacityValue()
        return opacityVal

    def canSelected(self):
        itemData = CD.data.get(self.carrouselId, None)
        return itemData.get('canselect', False)

    def canOutline(self):
        itemData = CD.data.get(self.carrouselId, None)
        return itemData.get('canOutline', False)

    def canSwitchCameraAni(self):
        itemData = CD.data.get(self.carrouselId, None)
        return itemData.get('cameraAni', None)
