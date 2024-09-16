#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerVehicle.o
import Math
import BigWorld
import utils
import gamelog
from callbackHelper import Functor
from data import moving_platform_data as MPD

class ImpPlayerVehicle(object):

    def _checkVehicle(self):
        if getattr(self, 'alreadyCheckVehicle', False):
            return
        elif not self.inWorld:
            return
        else:
            if not self.vehicleKey:
                vehicles = utils.getEntityList('MovingPlatform')
                liftHeight = 0
                inVehicle = None
                for vehicle in vehicles:
                    liftHeight = max(vehicle.checkPlayerPos(), liftHeight)

                if liftHeight > 0 and inVehicle:
                    self.physics.teleport((self.position[0], inVehicle.position[1] + liftHeight, self.position[2]))
                    self.alreadyCheckVehicle = True
            if self.vehicleKey:
                self.alreadyCheckVehicle = True
                self.cell.loadVehicleInfo(True)
            return

    def searchSummonedSprite(self):
        sprites = utils.getEntityList('SummonedSprite')
        for ent in sprites:
            if ent.ownerId == self.id:
                return ent

    def enterVehicle(self, vehicleId):
        vehicle = BigWorld.entities.get(vehicleId)
        if vehicle and hasattr(vehicle, 'platNo'):
            sprite = self.searchSummonedSprite()
            if sprite and not self.inFly:
                self.suggestOwnerEnterVehicle()
                sprite.changeToFollowState()
            activatePlayerNum = MPD.data.get(vehicle.platNo, {}).get('activatePlayerNum', -1)
            if activatePlayerNum == -1:
                return
            self.cell.placeOnVehicle(vehicleId, True)

    def leaveVehicle(self, vehicleId):
        vehicle = BigWorld.entities.get(vehicleId)
        if vehicle and hasattr(vehicle, 'platNo'):
            sprite = self.searchSummonedSprite()
            if sprite and not self.inFly and not getattr(self, 'jumping', False):
                self.delaySuggestOwnerLeaveVehicle()
            activatePlayerNum = MPD.data.get(vehicle.platNo, {}).get('activatePlayerNum', -1)
            if activatePlayerNum == -1:
                return
            self.cell.placeOnVehicle(vehicleId, False)

    def teleportToVehicle(self, vehicleId, posOffset, yawOffset):
        self.loseGravity()
        BigWorld.callback(0.3, Functor(self._setVehicle, vehicleId, posOffset, yawOffset))

    def _setVehicle(self, vehicleId, posOffset, yawOffset):
        vehicle = BigWorld.entities.get(vehicleId)
        if vehicle:
            self.physics.teleportVehicle(vehicle)
            BigWorld.callback(0.0, Functor(self._doTeleportToVehicle, vehicleId, posOffset, yawOffset))

    def _doTeleportToVehicle(self, vehicleId, posOffset, yawOffset):
        vehicle = BigWorld.entities.get(vehicleId)
        if vehicle:
            m = Math.Matrix()
            m.setRotateYPR(Math.Vector3(vehicle.yaw, vehicle.pitch, vehicle.roll))
            pos = m.applyPoint(Math.Vector3(posOffset[0], posOffset[1], posOffset[2]))
            position = (vehicle.position[0] + pos[0], vehicle.position[1] + pos[1] + 3, vehicle.position[2] + pos[2])
            self.physics.teleport(position)
            self.filter.setYaw(vehicle.yaw + yawOffset)
            self.restoreGravity()
            gamelog.info('@PGF:ImpPlayerVehicle teleportToVehicle', self.id, vehicleId, vehicle, (self.position - vehicle.position).length, self.vehicle, position)
