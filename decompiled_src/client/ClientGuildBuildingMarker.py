#Embedded file name: I:/bag/tmp/tw2/res/entities\client/ClientGuildBuildingMarker.o
import sMath
import BigWorld
from BaseClientEntity import BaseClientEntity
from data import guild_building_marker_data as GBMD

class ClientGuildBuildingMarker(BaseClientEntity):

    def __init__(self):
        super(ClientGuildBuildingMarker, self).__init__()

    def isUsingPrefabPosDir(self):
        return True

    def getPrefabId(self):
        data = GBMD.data.get(self.markerId)
        if self.hasBuilding and data.get('afterBuildingModelId'):
            return data.get('afterBuildingModelId')
        else:
            stepModels = GBMD.data.get(self.markerId).get('stepModels')
            if stepModels:
                return stepModels[self.step]
            return self.DEFAULTPREFABID

    def getPrefabIdPath(self, prefabId):
        path = 'scene/common/building/prefab/%d.prefab' % prefabId
        return path

    def checkPending(self):
        if self.getPrefabId() != self.DEFAULTPREFABID:
            p = BigWorld.player()
            if sMath.distance2D(self.position, p.position) <= 100:
                p.pendingGuildEntIds.append(self.id)

    def enterWorld(self):
        if self.getPrefabId() == self.DEFAULTPREFABID:
            return
        super(ClientGuildBuildingMarker, self).enterWorld()

    def setupFilter(self):
        self.filter = BigWorld.ClientFilter()
        self.filter.applyDrop = True

    def leaveWorld(self):
        super(ClientGuildBuildingMarker, self).leaveWorld()

    def setStep(self, old):
        self.clearModels()
        self.createModels()

    def setHasBuilding(self, old):
        self.clearModels()
        self.createModels()
