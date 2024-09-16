#Embedded file name: I:/bag/tmp/tw2/res/entities\client/ClientGuildBuilding.o
import BigWorld
import sMath
import const
import commGuild
from BaseClientEntity import BaseClientEntity
from data import guild_building_data as GBD
from data import guild_building_upgrade_data as GBUD
from data import guild_building_marker_data as GBMD

class ClientGuildBuilding(BaseClientEntity):

    def isUsingPrefabPosDir(self):
        return True

    def getPrefabId(self):
        extraPrefabId = self._getUpgradingPrefabId()
        if extraPrefabId:
            return [self._getPrefabId(), extraPrefabId]
        else:
            return self._getPrefabId()

    def _getUpgradingPrefabId(self):
        if self.tStart and self.buildingLevel > 0:
            mdata = GBMD.data.get(self.markerId)
            return mdata.get('upgradingEffect')
        else:
            return 0

    def _getPrefabId(self, level = None):
        if level == None:
            level = self.buildingLevel
        if commGuild.isMultiBuilding(self.buildingId):
            mdata = GBMD.data.get(self.markerId)
            if commGuild.isMultiBuildingMarker(self.markerId):
                if level == 0:
                    if isinstance(mdata.get('baseModelId'), tuple):
                        idx = mdata.get('buildingId').index(self.buildingId)
                        return mdata.get('baseModelId')[idx]
                    else:
                        return mdata.get('baseModelId', BaseClientEntity.DEFAULTPREFABID)
                elif isinstance(mdata.get('buildingModelId'), tuple):
                    idx = mdata.get('buildingId').index(self.buildingId)
                    return mdata.get('buildingModelId')[idx]
                else:
                    return mdata.get('buildingModelId', BaseClientEntity.DEFAULTPREFABID)

            elif level == 0:
                return mdata.get('baseModelId', BaseClientEntity.DEFAULTPREFABID)
            else:
                return mdata.get('buildingModelId', BaseClientEntity.DEFAULTPREFABID)

        else:
            if level <= 0:
                return GBD.data.get(self.buildingId).get('modelId', BaseClientEntity.DEFAULTPREFABID)
            return GBUD.data.get((self.buildingId, level)).get('modelId', BaseClientEntity.DEFAULTPREFABID)

    def getPrefabIdPath(self, prefabId):
        path = 'scene/common/building/prefab/%d.prefab' % prefabId
        return path

    def checkPending(self):
        if self.getPrefabId() != BaseClientEntity.DEFAULTPREFABID:
            bfound = False
            p = BigWorld.player()
            if not commGuild.isMultiBuilding(self.buildingId):
                data = GBD.data.get(self.buildingId)
                bound = data.get('bound')
            else:
                data = GBMD.data.get(self.markerId)
                bound = data.get('bound')
            if bound:
                x, _, z = p.position
                minx, _, minz = bound[0]
                maxx, _, maxz = bound[1]
                _x, _, _z = self.position
                x -= _x
                z -= _z
                if x >= minx and x <= maxx and z >= minz and z <= maxz:
                    p.pendingGuildEntIds.append(self.id)
                    bfound = True
            if not bfound:
                if sMath.distance2D(self.position, p.position) <= const.GUILD_BUILDING_PENDING_DIST:
                    p.pendingGuildEntIds.append(self.id)
            if self.markerId in p.pendingGuildMarkerIds:
                p.pendingGuildMarkerIds.remove(self.markerId)

    def enterWorld(self):
        super(ClientGuildBuilding, self).enterWorld()

    def loadImmediately(self):
        return True

    def setBuildingLevel(self, oldBuildingLevel):
        oldPrefabId = self._getPrefabId(oldBuildingLevel)
        newPrefabId = self._getPrefabId(self.buildingLevel)
        if oldPrefabId != newPrefabId:
            self.refreshModel(newPrefabId)

    def setTStart(self, oldTStart):
        if self.ownerModels == None:
            return
        prefabId = self._getUpgradingPrefabId()
        if not prefabId:
            self.clearExtraModels()
        else:
            self._loadPrefabs([prefabId], bExtra=True)

    def refreshModel(self, prefabId):
        if self.prefabId == prefabId:
            return
        self.clearModels()
        self.createModels()

    def getModelNameList(self):
        prefabId = self._getPrefabId()
        self._registerPrefabMap(prefabId)
        return ClientGuildBuilding.PREFAB_MAP[prefabId]['models']

    def setupFilter(self):
        self.filter = BigWorld.ClientFilter()
        self.filter.applyDrop = True
