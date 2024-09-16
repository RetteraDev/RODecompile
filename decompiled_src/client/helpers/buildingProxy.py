#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/buildingProxy.o
import zlib
import cPickle
import BigWorld
import Math
import const
import gamelog
from data import moving_platform_data as MPD
from data import client_building_proxy_data as CBPD

class BaseProxy(object):
    BEGIN_LOAD_DIST = 700
    BEGIN_DEL_DIST = 800
    PROXY_EMPTY = 0
    PROXY_LOADING = 1
    PROXY_LOADED = 2
    PROXY_NO_RES = 3

    def __init__(self, entityID, spaceID, proxyInfo):
        super(BaseProxy, self).__init__()
        self.entityID = entityID
        self.spaceID = spaceID
        self.proxyInfo = proxyInfo
        self.models = []
        self.bindEntity = None
        self.proxyState = BaseProxy.PROXY_EMPTY
        self.preloadID = 0
        self.checkUnfinish = False

    def resetProxyInfo(self, proxyInfo):
        gamelog.debug('resetProxyInfo......................', self, self.proxyInfo, proxyInfo)
        self.proxyInfo.update(proxyInfo)

    def extraChange(self, newExtra):
        self.proxyInfo['extra'].update(newExtra)

    def position(self):
        return Math.Vector3(self.proxyInfo['pos'][0], self.proxyInfo['pos'][1], self.proxyInfo['pos'][2])

    def direction(self):
        return Math.Vector3(self.proxyInfo['dir'][0], self.proxyInfo['dir'][1], self.proxyInfo['dir'][2])

    def yaw(self):
        return self.proxyInfo['dir'][2]

    def getModelNameList(self):
        return []

    def checkSelf(self):
        p = BigWorld.player()
        if p == None:
            return
        ppos = p.position
        spaceID = p.spaceID
        if spaceID == self.spaceID:
            dist = (self.position() - ppos).length
            if dist > self.BEGIN_DEL_DIST:
                if self.proxyState != BaseProxy.PROXY_EMPTY:
                    self.unload()
            elif dist < self.BEGIN_LOAD_DIST:
                if self.checkUnfinish or self.proxyState == BaseProxy.PROXY_EMPTY:
                    self.checkUnfinish = False
                    self.load()

    def unload(self):
        self.clearModels()
        self.clearEntity()
        self.cancelModelLoading()
        self.proxyState = BaseProxy.PROXY_EMPTY

    def load(self):
        self.createEntity()
        self.beginPreLoadModel()

    def createEntity(self):
        pass

    def beginPreLoadModel(self):
        pass

    def endPreLoadModel(self, preloadid, model):
        pass

    def cancelModelLoading(self):
        self.preloadID += 1

    def createModels(self):
        pass

    def clearModels(self):
        p = BigWorld.player()
        for i in self.models:
            if i and i.inWorld:
                p.delModel(i)

        self.models = []

    def clearEntity(self):
        pass

    def destroy(self):
        self.clearModels()
        self.cancelModelLoading()
        self.proxyState = BaseProxy.PROXY_EMPTY

    def collideCheck(self):
        pass

    def kickCheck(self):
        pass

    def hide(self, flag = True):
        if len(self.models) <= 0:
            return
        for model in self.models:
            model.visible = not flag

    def entityEnterWorld(self, info, bHide = True):
        self.proxyInfo.update(info)
        self.hide(bHide)

    def entityLeaveWorld(self, info):
        self.proxyInfo.update(info)
        self.hide(False)


class MovingPlatformProxy(BaseProxy):

    def __init__(self, entityID, spaceID, proxyInfo):
        super(MovingPlatformProxy, self).__init__(entityID, spaceID, proxyInfo)
        self.checkSelf()

    def resetProxyInfo(self, proxyInfo):
        self.extraChange(proxyInfo['extra'])

    def extraChange(self, newExtra):
        gamelog.debug('@PGF:MovingPlatformProxy.extraChange 2', newExtra)
        super(MovingPlatformProxy, self).extraChange(newExtra)
        if not self.bindEntity:
            return
        self._refreshPosition()

    def _refreshPosition(self, checkMoving = True):
        gamelog.debug('@PGF:MovingPlatformProxy._refreshPosition', self.proxyInfo, self.bindEntity.filter.position)
        isMoving = self.getExtraDataByKey('moving')
        if isMoving:
            destPos = Math.Vector3(self.getExtraDataByKey('destPos'))
            speed = self.getExtraDataByKey('speed')
            self.bindEntity.filter.position = self.position(checkMoving)
            self.bindEntity.seekTo(destPos, speed)
            en = BigWorld.entities.get(self.entityID)
            if en and en.inWorld and not en.isMoving:
                en.movingNotifier(True)
        else:
            position = self.getExtraDataByKey('pos')
            direction = self.getExtraDataByKey('dir')
            if self.bindEntity:
                self.bindEntity.filter.position = position
                self.bindEntity.filter.yaw = direction[2]
                self.bindEntity.seekTo(position, 4)
        gamelog.debug('@PGF:MovingPlatformProxy._refreshPosition after', self.bindEntity.filter.position)

    def getExtraDataByKey(self, key):
        return self.proxyInfo.get('extra', {}).get(key, None)

    def position(self, checkMoving = True):
        isMoving = self.proxyInfo.get('extra', {}).get('moving', False)
        if isMoving and checkMoving:
            startPos = self.getExtraDataByKey('pos')
            startTime = self.getExtraDataByKey('startTime')
            destPos = Math.Vector3(self.getExtraDataByKey('destPos'))
            speed = self.getExtraDataByKey('speed')
            currentTime = BigWorld.player().getServerTime()
            length = (destPos - startPos).length
            if length <= 0.0:
                position = destPos
            else:
                l = float(min(speed * (currentTime - startTime + 0.2), length))
                x = (destPos[0] - startPos[0]) * l / length + startPos[0]
                y = (destPos[1] - startPos[1]) * l / length + startPos[1]
                z = (destPos[2] - startPos[2]) * l / length + startPos[2]
                position = Math.Vector3(x, y, z)
        else:
            position = Math.Vector3(self.getExtraDataByKey('pos'))
        return position

    def direction(self):
        isMoving = self.proxyInfo.get('extra', {}).get('moving', False)
        if isMoving:
            startPos = self.getExtraDataByKey('pos')
            destPos = Math.Vector3(self.getExtraDataByKey('destPos'))
            return Math.Vector3(0, 0, (destPos - startPos).yaw)
        else:
            return Math.Vector3(self.getExtraDataByKey('dir'))

    def createEntity(self):
        if self.bindEntity:
            gamelog.debug('@PGF:MovingPlatformProxy.createEntity already has binding entity', self.proxyInfo)
            return
        platNo = self.getExtraDataByKey('platNo')
        if platNo not in MPD.data:
            gamelog.debug('@PGF:MovingPlatformProxy.createEntity platNo error', self.proxyInfo)
            return
        modelName = MPD.data.get(platNo).get('sightModel')
        scale = 1.0
        position = self.position()
        direction = self.direction()
        attrs = {}
        for key in self.proxyInfo.get('extra', {}).keys():
            attrs[key] = self.getExtraDataByKey(key)

        attrs['modelName'] = modelName
        attrs['scale'] = scale
        attrs['entityID'] = self.entityID
        try:
            entID = BigWorld.createEntity('ClientShip', self.spaceID, 0, position, direction, {'attrs': attrs})
            self.bindEntity = BigWorld.entities.get(entID)
            if self.bindEntity:
                self.proxyState = BaseProxy.PROXY_LOADED
        except:
            gamelog.debug('@PGF:createEntity, ERROR bindEntity', self.spaceID, self.entityID, position, direction, {'attrs': attrs})

    def destroy(self):
        if self.bindEntity:
            gamelog.debug('@PGF:MovingPlatformProxy.destroy', self.bindEntity.id)
            self.bindEntity.leaveWorld()
            BigWorld.destroyEntity(self.bindEntity.id)
            self.bindEntity = None
        self.proxyState = BaseProxy.PROXY_EMPTY

    def clearEntity(self):
        self.destroy()

    def hide(self, flag = True):
        if not self.bindEntity:
            return
        if not self.bindEntity.model:
            return
        self.bindEntity.model.visible = not flag

    def entityEnterWorld(self, info, bHide = True):
        self._updatePartInfo(info)
        entity = BigWorld.entities.get(self.entityID)
        gamelog.debug('@PGF:BaseProxy.entityEnterWorld', self.entityID, info, bHide, entity.position)
        if not self.bindEntity:
            return
        self.bindEntity.filter.yaw = entity.yaw
        if bHide and self.getExtraDataByKey('moving') and entity:
            entity.isMoving = True
            entity.playActWithAniModel()
        self.hide(bHide)
        gamelog.debug('@PGF:BaseProxy.entityEnterWorld after', self.entityID, info, bHide, entity.position, self.bindEntity.position)

    def entityLeaveWorld(self, info):
        gamelog.debug('@PGF:BaseProxy.entityLeaveWorld', self.entityID, info)
        self._updatePartInfo(info)
        entity = BigWorld.entities.get(self.entityID)
        gamelog.debug('@PGF:BaseProxy.entityLeaveWorld', self.entityID, info, entity.position)
        if not self.bindEntity:
            return
        self.bindEntity.filter.yaw = entity.yaw
        self._refreshPosition(False)
        self.hide(False)
        gamelog.debug('@PGF:BaseProxy.entityLeaveWorld after', self.entityID, info, entity.position, self.bindEntity.position)

    def _updatePartInfo(self, info):
        extraInfo = info.pop('extra')
        self.proxyInfo['pos'] = extraInfo['pos']
        self.proxyInfo['dir'] = extraInfo['dir']
        self.proxyInfo['extra']['pos'] = extraInfo['pos']
        self.proxyInfo['extra']['dir'] = extraInfo['dir']


class GuildBuildingProxy(BaseProxy):

    def __init__(self, entityID, spaceID, proxyInfo):
        super(GuildBuildingProxy, self).__init__(entityID, spaceID, proxyInfo)
        self.checkSelf()

    def resetProxyInfo(self, proxyInfo):
        self.extraChange(proxyInfo['extra'])

    def extraChange(self, newExtra):
        oldBuildingValue = self.getExtraDataByKey('buildingLevel') or 0
        oldTStart = self.getExtraDataByKey('tStart') or 0
        super(GuildBuildingProxy, self).extraChange(newExtra)
        if not self.bindEntity:
            return
        self.bindEntity.attrs.update(newExtra)
        if newExtra.has_key('tStart'):
            self.bindEntity.setTStart(oldTStart)
        if newExtra.has_key('buildingLevel'):
            self.bindEntity.setBuildingLevel(oldBuildingValue)

    def getExtraDataByKey(self, key):
        return self.proxyInfo.get('extra', {}).get(key, None)

    def createEntity(self):
        if self.bindEntity:
            gamelog.debug('@CF:GuildBuildingProxy.createEntity already has binding entity', self.proxyInfo)
            return
        scale = 1.0
        position = self.position()
        direction = self.direction()
        attrs = {}
        for key in self.proxyInfo.get('extra', {}).keys():
            attrs[key] = self.getExtraDataByKey(key)

        attrs['scale'] = scale
        try:
            entID = BigWorld.createEntity('ClientGuildBuilding', self.spaceID, 0, position, direction, {'attrs': attrs})
            self.bindEntity = BigWorld.entities.get(entID)
            if self.bindEntity:
                self.proxyState = BaseProxy.PROXY_LOADED
                self.bindEntity.checkPending()
        except:
            gamelog.debug('@CF:createEntity, ERROR bindEntity', self.spaceID, self.entityID, position, direction, {'attrs': attrs})

    def destroy(self):
        if self.bindEntity:
            gamelog.debug('@CF:GuildBuildingProxy.destroy', self.bindEntity.id)
            self.bindEntity.leaveWorld()
            BigWorld.destroyEntity(self.bindEntity.id)
            self.bindEntity = None
        self.proxyState = BaseProxy.PROXY_EMPTY

    def clearEntity(self):
        self.destroy()

    def hide(self, flag = True):
        if not self.bindEntity:
            return
        if not self.bindEntity.model:
            return
        self.bindEntity.model.visible = not flag


class GuildBuildingMarkerProxy(BaseProxy):

    def __init__(self, entityID, spaceID, proxyInfo):
        super(GuildBuildingMarkerProxy, self).__init__(entityID, spaceID, proxyInfo)
        self.checkSelf()

    def resetProxyInfo(self, proxyInfo):
        self.extraChange(proxyInfo['extra'])

    def extraChange(self, newExtra):
        oldStep = self.getExtraDataByKey('step') or 0
        oldHasBuilding = self.getExtraDataByKey('hasBuilding') or 0
        super(GuildBuildingMarkerProxy, self).extraChange(newExtra)
        if not self.bindEntity:
            return
        self.bindEntity.attrs.update(newExtra)
        if newExtra.has_key('step'):
            self.bindEntity.setStep(oldStep)
        if newExtra.has_key('hasBuilding'):
            self.bindEntity.setHasBuilding(oldHasBuilding)

    def getExtraDataByKey(self, key):
        return self.proxyInfo.get('extra', {}).get(key, None)

    def createEntity(self):
        if self.bindEntity:
            gamelog.debug('@CF:GuildBuildingMarkerProxy.createEntity already has binding entity', self.proxyInfo)
            return
        scale = 1.0
        position = self.position()
        direction = self.direction()
        attrs = {}
        for key in self.proxyInfo.get('extra', {}).keys():
            attrs[key] = self.getExtraDataByKey(key)

        attrs['scale'] = scale
        try:
            entID = BigWorld.createEntity('ClientGuildBuildingMarker', self.spaceID, 0, position, direction, {'attrs': attrs})
            self.bindEntity = BigWorld.entities.get(entID)
            if self.bindEntity:
                self.proxyState = BaseProxy.PROXY_LOADED
        except:
            gamelog.debug('@CF:createEntity, ERROR bindEntity', self.spaceID, self.entityID, position, direction, {'attrs': attrs})

    def destroy(self):
        if self.bindEntity:
            gamelog.debug('@CF:GuildBuildingMarkerProxy.destroy', self.bindEntity.id)
            self.bindEntity.leaveWorld()
            BigWorld.destroyEntity(self.bindEntity.id)
            self.bindEntity = None
        self.proxyState = BaseProxy.PROXY_EMPTY

    def clearEntity(self):
        self.destroy()

    def hide(self, flag = True):
        if not self.bindEntity:
            return


class ClientTransportProxy(BaseProxy):

    def __init__(self, entityID, spaceID, proxyInfo):
        super(ClientTransportProxy, self).__init__(entityID, spaceID, proxyInfo)
        self.checkSelf()

    def createEntity(self):
        if self.bindEntity:
            gamelog.debug('@PGF:ClientTransportProxy.createEntity already has binding entity', self.proxyInfo)
            return
        position = self.position()
        direction = self.direction()
        attrs = {}
        for key in self.proxyInfo.keys():
            attrs[key] = self.proxyInfo.get(key)

        attrs['cid'] = self.entityID
        attrs['spaceID'] = self.spaceID
        try:
            entID = BigWorld.createEntity('ClientTransport', self.spaceID, 0, position, direction, {'attrs': attrs})
            self.bindEntity = BigWorld.entities.get(entID)
            if self.bindEntity:
                self.proxyState = BaseProxy.PROXY_LOADED
        except:
            gamelog.debug('@PGF:ClientTransportProxy, ERROR bindEntity', self.spaceID, self.entityID, position, direction, {'attrs': attrs})

    def position(self):
        cbpd = CBPD.data.get(self.entityID, {})
        if 'pos' in cbpd:
            return Math.Vector3(cbpd['pos'][0], cbpd['pos'][1], cbpd['pos'][2])
        else:
            return Math.Vector3(0, 0, 0)

    def direction(self):
        cbpd = CBPD.data.get(self.entityID, {})
        if 'dir' in cbpd:
            return Math.Vector3(cbpd['dir'][0], cbpd['dir'][1], cbpd['dir'][2])
        else:
            return Math.Vector3(0, 0, 0)

    def destroy(self):
        if self.bindEntity:
            gamelog.debug('@PGF:ClientTransportProxy.destroy', self.bindEntity.id)
            self.bindEntity.leaveWorld()
            BigWorld.destroyEntity(self.bindEntity.id)
            self.bindEntity = None
        self.proxyState = BaseProxy.PROXY_EMPTY

    def clearEntity(self):
        self.destroy()


class WingCityBuildingProxy(BaseProxy):

    def __init__(self, entityID, spaceID, proxyInfo):
        super(WingCityBuildingProxy, self).__init__(entityID, spaceID, proxyInfo)
        self.checkSelf()

    def resetProxyInfo(self, proxyInfo):
        self.extraChange(proxyInfo['extra'])

    def extraChange(self, newExtra):
        if 'gateStatus' in newExtra:
            oldGateStatus = self.getExtraDataByKey('gateStatus') or 0
        if 'buildingStatus' in newExtra:
            oldBuildingStatus = self.getExtraDataByKey('buildingStatus') or 0
        if 'ownerHostId' in newExtra:
            oldOwnerHostId = self.getExtraDataByKey('ownerHostId') or 0
        super(WingCityBuildingProxy, self).extraChange(newExtra)
        if not self.bindEntity:
            return
        self.bindEntity.attrs.update(newExtra)
        if 'gateStatus' in newExtra:
            self.bindEntity.setGateStatus(oldGateStatus)
        if 'buildingStatus' in newExtra:
            self.bindEntity.setBuildingStatus(oldBuildingStatus)
        if 'ownerHostId' in newExtra:
            self.bindEntity.setOwnerHostId(oldOwnerHostId)

    def getExtraDataByKey(self, key):
        return self.proxyInfo.get('extra', {}).get(key, None)

    def createEntity(self):
        if self.bindEntity:
            gamelog.debug('@CF:WingCityBuildingProxy.createEntity already has binding entity', self.proxyInfo)
            return
        scale = 1.0
        position = self.position()
        direction = self.direction()
        attrs = {}
        for key in self.proxyInfo.get('extra', {}).keys():
            attrs[key] = self.getExtraDataByKey(key)

        attrs['scale'] = scale
        try:
            entID = BigWorld.createEntity('ClientWingCityBuilding', self.spaceID, 0, position, direction, {'attrs': attrs})
            self.bindEntity = BigWorld.entities.get(entID)
            if self.bindEntity:
                self.proxyState = BaseProxy.PROXY_LOADED
        except Exception as e:
            gamelog.debug('@CF:createEntity, ERROR bindEntity', e.message, self.spaceID, self.entityID, position, direction, {'attrs': attrs})

    def destroy(self):
        if self.bindEntity:
            gamelog.debug('@CF:WingCityBuildingProxy.destroy', self.bindEntity.id)
            self.bindEntity.leaveWorld()
            BigWorld.destroyEntity(self.bindEntity.id)
            self.bindEntity = None
        self.proxyState = BaseProxy.PROXY_EMPTY

    def clearEntity(self):
        self.destroy()

    def hide(self, flag = True):
        if not self.bindEntity:
            return
        if not self.bindEntity.model:
            return
        self.bindEntity.model.visible = not flag


class BuildingProxyMgr(object):

    @staticmethod
    def WrapSight(info):
        return {'cls': info[0],
         'pos': Math.Vector3(info[1]),
         'dir': Math.Vector3(info[2]),
         'extra': info[3]}

    CYCLE_INTERVAL = 10

    def __init__(self):
        super(BuildingProxyMgr, self).__init__()
        self.proxies = {}
        self.cProxies = {}
        self.bCycleCheck = True
        self.cycleCheck()
        self.sightCache = {}
        self.loadWorldClientOnlyProxy()

    def clearAll(self):
        self.bCycleCheck = False
        for i in self.proxies.iterkeys():
            self.proxies[i].destroy()

        self.proxies = {}
        for i in self.cProxies.iterkeys():
            self.cProxies[i].destroy()

        self.cProxies = {}

    def cycleCheck(self):
        if not self.bCycleCheck:
            return
        for i in self.proxies.iterkeys():
            self.proxies[i].checkSelf()

        for i in self.cProxies.iterkeys():
            self.cProxies[i].checkSelf()

        BigWorld.callback(self.CYCLE_INTERVAL, self.cycleCheck)

    def spaceChanged(self):
        spaceID = BigWorld.player().spaceID
        destroyIds = []
        for i in self.proxies.iterkeys():
            if self.proxies[i].spaceID != spaceID:
                self.proxies[i].destroy()
                destroyIds.append(i)
            else:
                self.proxies[i].checkSelf()

        for i in destroyIds:
            self.proxies.pop(i)

        cDestroyIds = []
        for i in self.cProxies.iterkeys():
            if self.cProxies[i].spaceID != spaceID:
                self.cProxies[i].destroy()
                cDestroyIds.append(i)
            else:
                self.cProxies[i].checkSelf()

        for i in cDestroyIds:
            self.cProxies.pop(i)

        self.loadWorldClientOnlyProxy()

    def querySpace(self):
        spaceID = BigWorld.player().spaceID
        cache = self.sightCache.get(spaceID, (0, {}))
        gamelog.debug('@PGF:buildingProxyMgr: querySpace ...............', cache, self.sightCache)

    def sightAll(self, spaceID, ver, info):
        gamelog.debug('@PGF: sightAll...........', spaceID, ver, info, BigWorld.player().spaceID, self.proxies)
        cacheInfo = self.sightCache.get(spaceID, (0, {}))
        if ver > cacheInfo[0]:
            info = cPickle.loads(zlib.decompress(info))
            self.sightCache[spaceID] = (ver, info)
        else:
            info = cacheInfo[1]
        for id, val in info.iteritems():
            data = self.WrapSight(val)
            self.updateProxy(id, spaceID, data)

        removeProxies = []
        for i in self.proxies.iterkeys():
            if i not in info:
                removeProxies.append(i)

        for i in removeProxies:
            self.proxies[i].destroy()
            self.proxies.pop(i)

    def sightEnter(self, spaceID, oldID, info):
        gamelog.debug('@PGF: sightEnter:', spaceID, oldID, info)
        self.updateProxy(oldID, spaceID, info)

    def sightLeave(self, oldID):
        gamelog.debug('@PGF: sightLeave:', oldID)
        if self.proxies.has_key(oldID):
            self.proxies[oldID].destroy()
            self.proxies.pop(oldID)

    def sightAlterExtra(self, oldID, newInfo):
        gamelog.debug('@PGF: sightAlterExtra:', oldID, newInfo)
        if self.proxies.has_key(oldID):
            self.proxies[oldID].extraChange(newInfo)

    def updateProxy(self, entityID, spaceID, proxyInfo):
        gamelog.debug('@PGF:updateProxy', entityID, spaceID, proxyInfo)
        if self.proxies.has_key(entityID):
            self.proxies[entityID].resetProxyInfo(proxyInfo)
        else:
            self.createProxy(entityID, spaceID, proxyInfo)

    def createProxy(self, entityID, spaceID, proxyInfo):
        clsName = proxyInfo['cls']
        if clsName == 'MovingPlatform':
            self.proxies[entityID] = MovingPlatformProxy(entityID, spaceID, proxyInfo)
        elif clsName == 'GuildBuilding':
            self.proxies[entityID] = GuildBuildingProxy(entityID, spaceID, proxyInfo)
        elif clsName == 'GuildBuildingMarker':
            self.proxies[entityID] = GuildBuildingMarkerProxy(entityID, spaceID, proxyInfo)
        elif clsName == 'WingCityBuilding':
            self.proxies[entityID] = WingCityBuildingProxy(entityID, spaceID, proxyInfo)

    def hideProxy(self, entityID, flag = True):
        proxy = self.proxies.get(entityID)
        if proxy:
            proxy.hide(flag=flag)

    def loadWorldClientOnlyProxy(self):
        player = BigWorld.player()
        if not player or not player.inWorld:
            return
        player.clearClientTransportPot()
        spaceNo = player.spaceNo
        spaceID = player.spaceID
        if spaceNo not in (const.SPACE_NO_BIG_WORLD, const.SPACE_NO_AMST):
            return
        for cid, info in CBPD.data.iteritems():
            if cid in self.cProxies:
                continue
            if info:
                cproxyInfo = info.get('extra', {})
                cproxyType = info.get('type', 0)
                if cproxyType == 0:
                    self.cProxies[cid] = ClientTransportProxy(cid, spaceID, cproxyInfo)
