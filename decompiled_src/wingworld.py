#Embedded file name: /WORKSPACE/data/entities/client/helpers/wingworld.o
import cPickle
import zlib
import BigWorld
import Math
import commonWingWorld
import utils
import formula
import const
import gamelog
import wingWorldUtils
import gameglobal
import gametypes
from sMath import distance2D, distance3D
from checkResult import CheckResult
from commonWingWorld import WWArmyPostVal
from callbackHelper import Functor
import gameconfigCommon
from userDictType import UserDictType
from data import wing_world_city_data as WWCTD
from data import wing_world_config_data as WWCD
from data import region_server_config_data as RSCD
from data import wing_city_building_data as WCBD
from data import wing_city_building_static_data as WCBSD
from data import wing_city_npc_teleport_data as WCNTD
from data import navigator_stone_data as NSD
from cdata import game_msg_def_data as GMDD

class WingCityAdminGuildVal(commonWingWorld.WingCityAdminGuildVal):

    def __init__(self, rank = 0, guildNUID = 0, guildName = '', guildFlag = '', memberCount = 0, campId = 0, fromHostId = 0):
        super(WingCityAdminGuildVal, self).__init__(rank, guildNUID, guildName, guildFlag, memberCount, campId, fromHostId)

    def fromClientDTO(self, dto):
        self.rank, self.guildNUID, self.guildName, self.guildFlag, self.memberCount, self.campId, self.fromHostId = dto


class WingCityAdminGuildValMap(commonWingWorld.WingCityAdminGuildValMap):

    def updateMasterGuildVal(self, dto):
        for guildVal in self.itervalues():
            if guildVal.rank == 1:
                guildVal.fromClientDTO(dto)
                return

        self.fromClientDTO([dto])

    def deleteMasterGuildVal(self):
        masterGuildId = 0
        for guildVal in self.itervalues():
            if guildVal.rank == 1:
                masterGuildId = guildVal.guildNUID
                break

        if masterGuildId:
            self.pop(masterGuildId)

    def fromClientDTO(self, dtos):
        for dto in dtos:
            guildNUID = dto[1]
            if self.has_key(guildNUID):
                self[guildNUID].fromClientDTO(dto)
            else:
                val = WingCityAdminGuildVal()
                val.fromClientDTO(dto)
                self[guildNUID] = val


class WingWorldPeaceCityVal(commonWingWorld.WingWorldCityVal):

    def __init__(self, cityId = 0, ownerHostId = 0, ownerCampId = 0):
        super(WingWorldPeaceCityVal, self).__init__(cityType=const.WING_CITY_TYPE_PEACE, cityId=cityId, ownerHostId=ownerHostId, ownerCampId=ownerCampId)
        self.declaredNum = 0
        self.declaredCampNum = 0
        self.adminGuildMap = WingCityAdminGuildValMap()
        self.resourcePoints = {}
        self.buildingStates = {}

    def fromDTO(self, dto):
        isFull = dto[2]
        if isFull:
            _, self.cityId, _, self.ownerHostId, self.declaredNum, self.ownerCampId, self.declaredCampNum, adminGuildDTO, resPointsDTO, self.buildingStates = dto
            self.adminGuildMap = WingCityAdminGuildValMap()
            self.adminGuildMap.fromClientDTO(adminGuildDTO)
            self.resourcePoints = {}
            for dto in resPointsDTO:
                val = WingCityResourcePointVal()
                val.fromDTO(dto)
                self.resourcePoints[val.pointId] = val

        else:
            _, self.cityId, _, self.ownerHostId, self.declaredNum, self.ownerCampId, self.declaredCampNum, masterGuildDTO = dto
            if not self.adminGuildMap:
                self.adminGuildMap = WingCityAdminGuildValMap()
            if masterGuildDTO:
                self.adminGuildMap.updateMasterGuildVal(masterGuildDTO[0])
            else:
                self.adminGuildMap.deleteMasterGuildVal()
        return self


class WingWorldWarCityVal(commonWingWorld.WingWorldCityVal):

    def __init__(self, cityId = 0, ownerHostId = 0, ownerCampId = 0):
        super(WingWorldWarCityVal, self).__init__(cityType=const.WING_CITY_TYPE_WAR, cityId=cityId, ownerHostId=ownerHostId, ownerCampId=ownerCampId)
        self.attackHostIds = []
        self.isDirectSettlement = False

    def fromDTO(self, dto):
        _, self.cityId, self.ownerHostId, self.isDirectSettlement, self.attackHostIds = dto
        return self

    def openAttack(self, hostId):
        self.attackHostIds.append(hostId)


class WingWorldCity(commonWingWorld.WingWorldCity):

    def getCity(self, cityType, cityId):
        if cityId not in WWCTD.data:
            raise Exception('WingWorldCity.getCity invalid cityId %s' % cityId)
        city = self.cityVals[cityType].get(cityId)
        if not city:
            if cityType == const.WING_CITY_TYPE_PEACE:
                city = WingWorldPeaceCityVal(cityId=cityId)
            else:
                city = WingWorldWarCityVal(cityId=cityId)
            self.cityVals[cityType][cityId] = city
        return city

    def fromDTO(self, dtos):
        for dto in dtos:
            cityType = dto[0]
            cityId = dto[1]
            self.getCity(cityType, cityId).fromDTO(dto)


class WingWorldCityWorldMap(object):

    def __init__(self):
        self.ownerHostId = 0
        self.attendHost2ColorIdx = {}
        self.buildDic = {}

    def fromDTO(self, dto):
        self.ownerHostId, self.attendHost2ColorIdx, buildingdtos = dto
        if buildingdtos:
            for buildingDTO in buildingdtos:
                building = WingWorldCityBuildingMinMap()
                building.fromDTO(buildingDTO)
                self.buildDic[building.entNo] = building


class WingWorldCountryVal(commonWingWorld.WingWorldCountryVal):

    def __init__(self, hostId, campId = 0):
        super(WingWorldCountryVal, self).__init__(hostId, campId=campId)
        self.events = []
        self.resourcePointMap = WingHostResourcePointMap()
        self.lostCityIdsLastWeek = set()
        self.notice = ''

    def onReset(self):
        super(WingWorldCountryVal, self).onReset()

    def fromDTO(self, dto):
        self.hostId, self.power, self.flagId, self.postInfo, self.neighborCityId, self.ownedCityIds, self.allowAttackCityIds, self.declaredCityId2PostId, self.titleLevel, self.trendIds, self.resourceRecords, self.buildingScore, self.destroyScore, self.scoreRank, self.lostCityIdsLastWeek = dto

    def openAttack(self, cityId):
        if cityId not in self.allowAttackCityIds:
            self.allowAttackCityIds.append(cityId)

    def updateEvents(self, eventBlob):
        self.eventsBlob = eventBlob
        if not self.eventsBlob:
            self.events = []
            return
        self.events = cPickle.loads(zlib.decompress(self.eventsBlob))

    def getEvents(self):
        return self.events

    def triggerTrend(self, trendId):
        if trendId in self.trendIds:
            return True
        self.trendIds.append(trendId)
        return True

    def updateNotice(self, notice):
        self.notice = notice


class WingWorldCountry(commonWingWorld.WingWorldCountry):

    def getCountry(self, hostId):
        if gameconfigCommon.enableWingWorldWarCampMode() and hostId in gametypes.WING_WORLD_CAMP_ALL_HOSTIDS:
            if hostId not in gametypes.WING_WORLD_CAMPS:
                raise Exception('WingWorldCountry.getCountry invalid campId %s' % hostId)
            c = self.get(hostId)
            if not c:
                c = WingWorldCountryVal(hostId=hostId, campId=hostId)
                self[hostId] = c
            return c
        elif not hostId:
            return WingWorldCountryVal(hostId=0)
        else:
            if hostId not in RSCD.data:
                raise Exception('WingWorldCountry.getCountry invalid hostId %s' % hostId)
            c = self.get(hostId)
            if not c:
                c = WingWorldCountryVal(hostId=hostId)
                self[hostId] = c
            return c

    def isNormalHostId(self, hostId):
        return hostId and not self.isCampHostId(hostId)

    def isCampHostId(self, hostId):
        return hostId in gametypes.WING_WORLD_CAMP_ALL_HOSTIDS

    def fromDTO(self, dtos):
        for dto in dtos:
            hostId = dto[0]
            self.getCountry(hostId).fromDTO(dto)

    def getOwn(self):
        return self.getCountry(BigWorld.player().getOriginHostId())

    def getOwnCamp(self):
        return self.getCamp(BigWorld.player().wingWorldCamp)

    def getCamp(self, campId):
        if not campId:
            return WingWorldCountryVal(hostId=0)
        return self.getCountry(campId)


class WWCampLeaderVal(object):

    def __init__(self, info):
        super(WWCampLeaderVal, self).__init__()
        self.gbId = info[0]
        self.name = info[1]
        self.postId = info[2]
        self.guildNUID = 0
        self.guildName = ''
        if len(info) > 3:
            self.guildNUID = info[3]
            self.guildName = info[4]


class WingWorldCampVal(commonWingWorld.WingWorldCampVal):

    def __init__(self, campId):
        super(WingWorldCampVal, self).__init__(campId)
        self.events = []
        self.lostCityIdsLastWeek = set()
        self.notice = ''

    def onReset(self):
        super(WingWorldCampVal, self).onReset()

    def fromDTO(self, dto):
        self.campId, self.power, self.flagId, self.postInfo, self.neighborCityId, self.ownedCityIds, self.allowAttackCityIds, self.declaredCityId2PostId, self.titleLevel, self.trendIds, self.resourceRecords, self.buildingScore, self.destroyScore, self.scoreRank, self.lostCityIdsLastWeek = dto

    def openAttack(self, cityId):
        if cityId not in self.allowAttackCityIds:
            self.allowAttackCityIds.append(cityId)

    def updateEvents(self, eventBlob):
        self.eventsBlob = eventBlob
        if not self.eventsBlob:
            self.events = []
            return
        self.events = cPickle.loads(zlib.decompress(self.eventsBlob))

    def getEvents(self):
        return self.events

    def triggerTrend(self, trendId):
        if trendId in self.trendIds:
            return True
        self.trendIds.append(trendId)
        return True

    def updateNotice(self, notice):
        self.notice = notice


class WingWorldCamp(commonWingWorld.WingWorldCamp):

    def getCamp(self, campId):
        if campId == 0:
            return WingWorldCampVal(campId=campId)
        if campId not in gametypes.WING_WORLD_CAMPS:
            raise Exception('WingWorldCountry.WingWorldCamp invalid campId %s' % campId)
        c = self.get(campId)
        if not c:
            c = WingWorldCampVal(campId=campId)
            self[campId] = c
        return c

    def fromDTO(self, dtos):
        for dto in dtos:
            hostId = dto[0]
            self.getCamp(hostId).fromDTO(dto)

    def getOwn(self):
        return self.getCamp(BigWorld.player().wingWorldCamp)


class WingWorld(object):

    def __init__(self, state = 0, step = 0):
        self.state = state
        self.opennessLevel = 0
        self.briefVer = 0
        self.countryVer = 0
        self.campVer = 0
        self.cityVer = 0
        self.city = WingWorldCity()
        self.country = WingWorldCountry()
        self.camp = WingWorldCamp()
        self.worldMapCache = {}
        self.events = []
        self.armyVer = -1
        self.armyOnlineVer = -1
        self.army = {}
        self.postId2gbId = {}
        self.armyState = 0
        self.step = 0
        self.trendId = 0
        self.volatileVer = -1
        self.pendingStaticBuildings = {}
        self.extraCanVoteGbIds = {}
        self.pendingSeekPoint = None
        self.failedPathFindingInMultiCitySpace = False
        self.armySkills = {}

    def setWorldMapCache(self, cityId, worldMapCity):
        if worldMapCity:
            self.worldMapCache[cityId] = worldMapCity
        elif self.worldMapCache.has_key(cityId):
            self.worldMapCache.pop(cityId)
        gameglobal.rds.ui.wingWorldBuilding.refreshCityInfo()

    def createClientEntity(self, owner, entityId, cityEntityNo, extra = None):
        sdata = WCBSD.data.get(cityEntityNo)
        if extra is None:
            extra = {}
        extra.update({'cityEntityNo': cityEntityNo,
         'entityID': entityId})
        attrs = {'cls': 'WingCityBuilding',
         'pos': sdata.get('position'),
         'dir': sdata.get('direction', (0, 0, 0)),
         'extra': extra}
        owner.sightEnter(owner.spaceID, entityId, zlib.compress(cPickle.dumps(attrs, -1)))

    def getCityKingName(self, ownerHostId):
        if BigWorld.player().isWingWorldCampMode():
            return self.camp.getCamp(ownerHostId).postInfo.get(wingWorldUtils.wingPostIdData.ARMY_LEADER_POST_ID, ('', ''))[1]
        else:
            return self.country.getCountry(ownerHostId).postInfo.get(wingWorldUtils.wingPostIdData.ARMY_LEADER_POST_ID, ('', ''))[1]

    def getArmyFromDTO(self, dtos):
        self.army.clear()
        for dto in dtos:
            val = WWArmyPostVal().fromDTO(dto)
            self.army[val.gbId] = val

        return self.army

    def buildArmyIndex(self):
        self.postId2gbId.clear()
        for gbId, post in self.army.iteritems():
            if self.postId2gbId.has_key(post.postId):
                self.postId2gbId[post.postId].append(gbId)
            else:
                self.postId2gbId[post.postId] = [post.gbId]

    def getArmyByPostId(self, postId, index = 0):
        gbIds = self.postId2gbId.get(postId)
        if not gbIds:
            return
        if index >= len(gbIds):
            return
        return self.army.get(gbIds[index])

    def getArmyByGbId(self, gbId):
        post = self.army.get(gbId)
        if post:
            return post
        p = BigWorld.player()
        if p.gbId == gbId and p.wingWorldPostId:
            post = WWArmyPostVal(gbId=gbId, postId=p.wingWorldPostId, name=p.roleName, school=p.school, sex=p.physique.sex, lv=p.lv, photo=p.friend.photo)
            self.army[gbId] = post
            self.buildArmyIndex()
        return post

    def getPostByGbId(self, gbId = 0):
        if not gbId:
            gbId = BigWorld.player().gbId
        val = self.getArmyByGbId(gbId)
        if val:
            return val.postId
        return 0

    def isPlayerGeneral(self, gbId):
        armyInfo = self.getArmyByGbId(gbId)
        if armyInfo:
            return WWArmyPostVal.isGeneralEx(armyInfo.postId) or WWArmyPostVal.isLeadersEx(armyInfo.postId)
        else:
            return False

    def refreshArmy(self, gbId, dto):
        post = WWArmyPostVal().fromDTO(dto)
        self.army[gbId] = post
        self.buildArmyIndex()

    def clearMpUsed(self):
        for post in self.army.itervalues():
            post.mpUsed = 0

    def findRouteToPeaceCity(self, owner, toSpaceNo):
        if not owner.inWingPeaceCity():
            return []
        groupId = owner.getWingWorldGroupId()
        links = {}
        for cityId, data in WWCTD.data.iteritems():
            spaceNo = formula.getWingCitySpaceNo(groupId, const.WING_CITY_TYPE_PEACE, cityId)
            tlinks = [ formula.getWingCitySpaceNo(groupId, const.WING_CITY_TYPE_PEACE, x) for x in data['linkCities'] ]
            if spaceNo not in links:
                links[spaceNo] = tlinks
            else:
                links[spaceNo].extend(tlinks)

        return _findRouteBetweenPeaceCitySpaces(owner.spaceNo, toSpaceNo, links)

    def getPeaceCityOwnerHostId(self, cityId):
        return self.city.getCity(const.WING_CITY_TYPE_PEACE, cityId).ownerHostId


class WingWorldMinMapPosInfo(object):

    def __init__(self):
        self.type = 0
        self.pos = None

    def fromDTO(self, dto):
        self.type, self.pos, self.args = dto


class WingWorldMinMapCaptainPos(WingWorldMinMapPosInfo):

    def __init__(self):
        super(WingWorldMinMapCaptainPos, self).__init__()
        self.name = ''

    def fromDTO(self, dto):
        self.type, self.pos, args = dto
        self.name, = args


class WingWorldMinMapGroupPos(WingWorldMinMapPosInfo):

    def __init__(self):
        super(WingWorldMinMapGroupPos, self).__init__()
        self.name = ''

    def fromDTO(self, dto):
        self.type, self.pos, args = dto
        self.gbId, self.name = args


class WingWorldMinMapCarrierPos(WingWorldMinMapPosInfo):

    def __init__(self):
        super(WingWorldMinMapCarrierPos, self).__init__()
        self.tempalteId = 0

    def fromDTO(self, dto):
        self.type, self.pos, args = dto
        self.tempalteId, = args


class WingWorldCityHostMinMap(commonWingWorld.WingWorldCityHostMinMap):

    def __init__(self):
        self.defaultReliveBoardEntNo = 0
        self.posData = []
        self.points = ()
        self.colorIdx = 0

    def fromDTO(self, dto):
        self.colorIdx, self.defaultReliveBoardEntNo, self.points, posDTO = dto
        self.posData = []
        for dto in posDTO:
            posType = dto[0]
            if posType == gametypes.WING_MIN_MAP_POS_TYPE_CAPTAIN:
                posInfo = WingWorldMinMapCaptainPos()
            elif posType == gametypes.WING_MIN_MAP_POS_TYPE_GROUP:
                posInfo = WingWorldMinMapGroupPos()
            elif posType == gametypes.WING_MIN_MAP_POS_TYPE_CARRIER:
                posInfo = WingWorldMinMapCarrierPos()
            else:
                gamelog.error('@hxm error WingWorld MinMapPosType', posType)
                posInfo = WingWorldMinMapPosInfo()
            posInfo.fromDTO(dto)
            self.posData.append(posInfo)


class WingWorldCityBuildingMinMap(commonWingWorld.WingWorldCityBuildingMinMap):

    def __init__(self, buildingId = 0, pos = (), ownHostId = 0, entNo = 0):
        super(WingWorldCityBuildingMinMap, self).__init__(buildingId, pos, ownHostId, entNo)

    def fromDTO(self, dto):
        self.buildingId, self.position, self.ownHostId, self.entNo, self.hpPercent = dto


class WingWorldCityMinMap(object):

    def __init__(self):
        self.buildings = []
        self.buildDic = {}
        self.attendHost2ColorIdx = {}
        self.ownerHostId = 0
        self.hostMinMap = WingWorldCityHostMinMap()
        self.airStoneEnergy = 0

    def fromDTO(self, dto):
        self.ownerHostId, buildingsDTO, hostMinMapDTO, self.attendHost2ColorIdx, self.airStoneEnergy = dto
        self.hostMinMap.fromDTO(hostMinMapDTO)
        self.buildDic.clear()
        self.buildings = []
        for buildingDTO in buildingsDTO:
            building = WingWorldCityBuildingMinMap()
            building.fromDTO(buildingDTO)
            self.buildDic[building.entNo] = building
            self.buildings.append(building)


class WingCityResourcePointVal(commonWingWorld.WingCityResourcePointVal):

    def __init__(self):
        super(WingCityResourcePointVal, self).__init__()


class WingHostResourcePointMap(UserDictType):

    def __init__(self, points = None):
        self.typeCounts = [0] * gametypes.WING_RESOURCE_TYPE_COUNT
        if not points:
            return
        for dto in points:
            val = WingCityResourcePointVal()
            val.fromDTO(dto)
            self[val.pointId] = val
            resType = wingWorldUtils.getResourcePointType(val.pointId)
            self.typeCounts[resType] += 1

    def getResourceCountByType(self, resType):
        return self.typeCounts[resType]

    def getResourceCountByGuild(self, guildNUID, resType):
        cnt = 0
        for pointVal in self.itervalues():
            if pointVal.guildNUID != guildNUID:
                continue
            if wingWorldUtils.getResourcePointType(pointVal.pointId) != resType:
                continue
            cnt += 1

        return cnt

    def getResourceCount(self, resType):
        cnt = 0
        for pointVal in self.itervalues():
            if wingWorldUtils.getResourcePointType(pointVal.pointId) != resType:
                continue
            cnt += 1

        return cnt


def findRouteToPeaceCity(toSpaceNo):
    owner = BigWorld.player()
    if not owner.inWingPeaceCity():
        return []
    groupId = owner.getWingWorldGroupId()
    links = {}
    for cityId, data in WWCTD.data.iteritems():
        spaceNo = formula.getWingCitySpaceNo(groupId, const.WING_CITY_TYPE_PEACE, cityId)
        tlinks = [ formula.getWingCitySpaceNo(groupId, const.WING_CITY_TYPE_PEACE, x) for x in data['linkCities'] ]
        if spaceNo not in links:
            links[spaceNo] = tlinks
        else:
            links[spaceNo].extend(tlinks)

    return _findRouteBetweenPeaceCitySpaces(owner.spaceNo, toSpaceNo, links)


def _findRouteBetweenPeaceCitySpaces(fromSpaceNo, toSpaceNo, links):
    if fromSpaceNo == toSpaceNo:
        return [toSpaceNo]
    if toSpaceNo not in links:
        return []
    routes = {toSpaceNo: 0}
    candidates = [toSpaceNo]
    maxCnt = len(links)
    while candidates:
        nextSpaceNo = candidates.pop(0)
        for spaceNo in links[nextSpaceNo]:
            if spaceNo in routes:
                continue
            routes[spaceNo] = nextSpaceNo
            candidates.append(spaceNo)
            if spaceNo == fromSpaceNo:
                results = []
                cid = spaceNo
                cnt = 0
                while cid in routes:
                    results.append(cid)
                    ncid = routes[cid]
                    cid = ncid
                    cnt += 1
                    if cnt > maxCnt:
                        gamelog.warning('dead loop in _findRouteBetweenCities', routes)
                        return []

                return results

    gamelog.warning('_findRouteBetweenCities failed to find path', routes)
    return []


def _findRouteBetweenPeaceCities(groupId, hostId, cities, fromCityId, toCityId, links, bTransport = False):
    if cities[toCityId].ownerHostId == hostId:
        return [toCityId]
    routes = {toCityId: 0}
    candidates = [toCityId]
    maxCnt = len(cities)
    while candidates:
        nextCityId = candidates.pop(0)
        for cityId in links[nextCityId]:
            if cityId in routes:
                continue
            routes[cityId] = nextCityId
            candidates.append(cityId)
            if cityId == fromCityId or bTransport and cities[cityId].ownerHostId == hostId:
                results = []
                cid = cityId
                cnt = 0
                while cid in routes:
                    spaceNo = formula.getWingCitySpaceNo(groupId, const.WING_CITY_TYPE_PEACE, cid)
                    results.append((cid, spaceNo))
                    ncid = routes[cid]
                    cid = ncid
                    cnt += 1
                    if cnt > maxCnt:
                        gamelog.warning('dead loop in _findRouteBetweenCities', routes)
                        return []

                return results

    gamelog.warning('_findRouteBetweenCities failed to find path', routes)
    return []


def getNearestXinmoEntryPos(tp):
    from data import wing_world_xinmo_entry_entity_data as WWXEED
    import navigator
    p = BigWorld.player()
    if p.inWingPeaceCity():
        chunkName = BigWorld.ChunkInfoAt(p.position)
        cityId = formula.getWingCityId(p.spaceNo, chunkName)
    elif p.spaceNo == const.SPACE_NO_BIG_WORLD or formula.spaceInWingBornIsland(p.spaceNo):
        cityId = wingWorldUtils.getDefaultNeighborCityId(utils.getHostId())
    else:
        return
    ret = [ x.get('position') for x in WWXEED.data.itervalues() if x.get('type') == tp and x.get('cityId') == cityId ]
    if not ret:
        return
    ret.sort(cmp=lambda x, y: navigator.cmpDist(x, y, p.position))
    return (ret[0], formula.getWingCitySpaceNo(p.getWingWorldGroupId(), const.WING_CITY_TYPE_PEACE, cityId))


def getNearestTeleportNpc(toSpaceNo, finalSpaceNo = 0, finalPos = None):
    p = BigWorld.player()
    ret = []
    mapId = formula.getMapId(p.spaceNo)
    toMapId = formula.getMapId(toSpaceNo)
    for data in WCNTD.data.get(mapId, ()):
        if data[3] == toMapId:
            ret.append(data)

    if not ret:
        return
    import navigator
    ret.sort(cmp=lambda x, y: navigator.cmpDist(x, y, p.position))
    v = ret[0]
    return (v[:3],
     v[3],
     v[9],
     v[8])


def getTransportInBornIsland():
    spaceNo = const.SPACE_NO_WING_WORLD_ISLAND
    k = NSD.data[spaceNo].keys()[0]
    v = NSD.data[spaceNo].get(k)
    return (v[:3], v[4])


def getTransportInCity(pos, spaceNo):
    ret = {}
    if NSD.data.has_key(spaceNo):
        stone = NSD.data[spaceNo]
        for destId, info in stone.iteritems():
            if info[-1] == 0 or pos == None or pos and info[-1] > 0 and distance2D(info[:3], pos) < info[-1]:
                ret[destId] = info

    ret = ret.items()
    import navigator
    ret.sort(cmp=lambda x, y: navigator.cmpDist(x[1], y[1], Math.Vector3(*pos)))
    if ret and len(ret[0]):
        v = ret[0][1]
        return (v[:3], v[4])
    else:
        return (None, None)


def pathFinding(seekPoint, bDelayed = False, endDist = 1.5, showMsg = True, fromGroupFollow = False, failedCallback = None, bForceByNpc = False):
    gamelog.debug('@navigator wingWorld#pathFinding', seekPoint, bDelayed, bForceByNpc)
    p = BigWorld.player()
    toSpaceNo = seekPoint[-1]
    realToSpaceNo = p.getRealWingCitySpaceNo(toSpaceNo)
    if toSpaceNo != realToSpaceNo:
        if not isinstance(seekPoint, list):
            seekPoint = list(seekPoint)
        seekPoint[-1] = realToSpaceNo
        toSpaceNo = realToSpaceNo
    if (p.inWingPeaceCity() or p.inWingBornIsland()) and toSpaceNo == const.SPACE_NO_BIG_WORLD:
        p.cell.teleportToBigWorldFromWingWorldForSeek(tuple(seekPoint[:3]))
        return
    import navigator
    if p.spaceNo == const.SPACE_NO_BIG_WORLD and (formula.spaceInWingBornIsland(toSpaceNo) or formula.spaceInWingPeaceCity(toSpaceNo)):
        nv = getNearestTeleportNpc(const.SPACE_NO_WING_WORLD_ISLAND)
        if not nv:
            gamelog.warning('@navigator wingWorld#pathFinding no npc in world to born island')
            return
        pos, nextSpaceNo, npcId, index = nv
        finalArriveCallback = Functor(onNavigateToWorldNpcForBornIsland, seekPoint, npcId)
        if bDelayed:
            p.isPathfinding = True
            navigator.getNav().seekDest = Math.Vector3(seekPoint[:3])
            navigator.getNav().setDelayPathFinding(1)
            navigator.getNav().delayData['seekPoint'] = pos + (p.spaceNo,)
            navigator.getNav().delayData['arriveCallback'] = finalArriveCallback
            navigator.getNav().delayData['failedCallback'] = failedCallback
            navigator.getNav().delayData['endDist'] = endDist
            p.isPathfinding = False
        else:
            navigator.getNav().pathFinding(pos + (p.spaceNo,), failedCallback=failedCallback, showMsg=showMsg, endDist=endDist, fromGroupFollow=fromGroupFollow, arriveCallback=finalArriveCallback)
        return
    if fromGroupFollow:
        showMsg = False
    if not (p.spaceNo == const.SPACE_NO_BIG_WORLD and toSpaceNo == const.SPACE_NO_BIG_WORLD):
        if not p.inWingPeaceCity() and not p.inWingBornIsland():
            gamelog.warning('@navigator wingWorld#pathFinding neither in peace city nor born island')
            return
        if not formula.spaceInWingPeaceCity(toSpaceNo) and not formula.spaceInWingBornIsland(toSpaceNo):
            gamelog.warning('@navigator wingWorld#pathFinding not to peace city')
            return
    if p.spaceNo == toSpaceNo and not bForceByNpc:
        finalArriveCallback = Functor(onNavigateToFinalSeekPoint)
        if toSpaceNo in const.MULTI_CITY_SPACE_NO and not p.wingWorld.failedPathFindingInMultiCitySpace:
            finalFailedCallback = Functor(onFailedPathFindingInMultiCitySpace, seekPoint, bDelayed, endDist, showMsg, fromGroupFollow, failedCallback, True)
        else:
            finalFailedCallback = Functor(onFailedPathFindingInSameSpace, failedCallback)
        if bDelayed:
            p.isPathfinding = True
            navigator.getNav().seekDest = Math.Vector3(seekPoint[:3])
            navigator.getNav().setDelayPathFinding(1)
            navigator.getNav().delayData['seekPoint'] = seekPoint
            navigator.getNav().delayData['arriveCallback'] = finalArriveCallback
            navigator.getNav().delayData['failedCallback'] = finalFailedCallback
            navigator.getNav().delayData['endDist'] = endDist
            p.isPathfinding = False
        else:
            navigator.getNav().pathFinding(seekPoint, failedCallback=finalFailedCallback, showMsg=showMsg, endDist=endDist, fromGroupFollow=fromGroupFollow, arriveCallback=finalArriveCallback)
        return
    if p.inWingBornIsland() and formula.spaceInWingPeaceCity(toSpaceNo):
        pos, transportId = getTransportInBornIsland()
        finalArriveCallback = Functor(onNavigateToBornIslandTransport, seekPoint, transportId)
        if bDelayed:
            p.isPathfinding = True
            navigator.getNav().seekDest = Math.Vector3(seekPoint[:3])
            navigator.getNav().setDelayPathFinding(1)
            navigator.getNav().delayData['seekPoint'] = pos + (p.spaceNo,)
            navigator.getNav().delayData['arriveCallback'] = finalArriveCallback
            navigator.getNav().delayData['failedCallback'] = failedCallback
            navigator.getNav().delayData['endDist'] = endDist
            p.isPathfinding = False
        else:
            navigator.getNav().pathFinding(pos + (p.spaceNo,), failedCallback=failedCallback, showMsg=showMsg, endDist=endDist, fromGroupFollow=fromGroupFollow, arriveCallback=finalArriveCallback)
        return
    if formula.spaceInWingBornIsland(toSpaceNo) and p.inWingPeaceCity():
        pos, transportId = getTransportInCity(p.position, p.getRealWingCitySpaceNo(p.spaceNo))
        if not pos and not transportId:
            return
        finalArriveCallback = Functor(onNavigateToCityTransportForBornIsland, seekPoint, transportId)
        if bDelayed:
            p.isPathfinding = True
            navigator.getNav().seekDest = Math.Vector3(seekPoint[:3])
            navigator.getNav().setDelayPathFinding(1)
            navigator.getNav().delayData['seekPoint'] = pos + (p.spaceNo,)
            navigator.getNav().delayData['arriveCallback'] = finalArriveCallback
            navigator.getNav().delayData['failedCallback'] = failedCallback
            navigator.getNav().delayData['endDist'] = endDist
            p.isPathfinding = False
        else:
            navigator.getNav().pathFinding(pos + (p.spaceNo,), failedCallback=failedCallback, showMsg=showMsg, endDist=endDist, fromGroupFollow=fromGroupFollow, arriveCallback=finalArriveCallback)
        return
    if p.spaceNo == toSpaceNo and bForceByNpc:
        spaceNoList = [p.spaceNo, toSpaceNo]
    else:
        spaceNoList = findRouteToPeaceCity(toSpaceNo)
    gamelog.debug('@navigator wingWorld#pathFinding spaceNoList', spaceNoList, p.spaceNo, toSpaceNo)
    if not spaceNoList or len(spaceNoList) < 2:
        gamelog.warning('@navigator wingWorld#pathFinding no spaceNoList', p.spaceNo, toSpaceNo, spaceNoList)
        return
    if len(spaceNoList) == 2:
        nv = getNearestTeleportNpc(spaceNoList[1], finalSpaceNo=toSpaceNo, finalPos=seekPoint[:3])
    else:
        nv = getNearestTeleportNpc(spaceNoList[1])
    if not nv:
        gamelog.error('@navigator wingWorld#pathFinding no npc', p.spaceNo, spaceNoList)
        return
    pos, nextSpaceNo, npcId, index = nv
    if spaceNoList.pop(0) != p.spaceNo:
        gamelog.error('@navigator wingWorld#pathFinding error', p.spaceNo, spaceNoList)
        return
    arriveCallback = Functor(onNavigateToNpc, seekPoint, nextSpaceNo, npcId, index, spaceNoList)
    nextSeekPoint = pos + (p.spaceNo,)
    finalFailedCallback = Functor(onFailedPathFindingInSameSpace, failedCallback)
    if bDelayed:
        p.isPathfinding = True
        navigator.getNav().seekDest = Math.Vector3(pos)
        navigator.getNav().setDelayPathFinding(1)
        navigator.getNav().delayData['seekPoint'] = nextSeekPoint
        navigator.getNav().delayData['arriveCallback'] = arriveCallback
        navigator.getNav().delayData['failedCallback'] = failedCallback
        navigator.getNav().delayData['endDist'] = endDist
        p.isPathfinding = False
    else:
        navigator.getNav().pathFinding(nextSeekPoint, None, failedCallback=finalFailedCallback, showMsg=False, endDist=endDist, fromGroupFollow=fromGroupFollow, arriveCallback=arriveCallback)


def onNavigateToNpc(seekPoint, nextSpaceNo, npcId, index, spaceNoList):
    gamelog.debug('@navigator wingWorld#onNavigateToNpc', seekPoint, npcId, index, spaceNoList)
    p = BigWorld.player()
    for e in p.entitiesInRange(10, 'Npc'):
        if e.npcId == npcId:
            gamelog.debug('@navigator wingWorld#npcTeleportWingWorld', nextSpaceNo, index, seekPoint[:3], seekPoint[-1])
            e.cell.npcTeleportWingWorld(nextSpaceNo, index, tuple(seekPoint[:3]), seekPoint[-1])
            break


def onNavigateToWorldNpcForBornIsland(seekPoint, npcId):
    gamelog.debug('@navigator wingWorld#onNavigateToWorldNpcForBornIsland', npcId, seekPoint[:3], seekPoint[-1])
    p = BigWorld.player()
    for e in p.entitiesInRange(10, 'Npc'):
        if e.npcId == npcId:
            gamelog.debug('@navigator wingWorld#onNavigateToWorldNpcForBornIsland', npcId, seekPoint[:3], seekPoint[-1])
            e.cell.enterToWingBornIslandForTeleport(tuple(seekPoint[:3]), seekPoint[-1])


def onNavigateToBornIslandTransport(seekPoint, transportId):
    gamelog.debug('@navigator wingWorld#onNavigateToBornIslandTransport', transportId, seekPoint[:3], seekPoint[-1])
    p = BigWorld.player()
    for e in p.entitiesInRange(10, 'Transport'):
        if e.charType == transportId:
            cityId = wingWorldUtils.getDefaultNeighborCityId(utils.getHostId())
            gamelog.debug('@navigator wingWorld#onWingWorldStoneTeleportConfirmed', transportId, seekPoint[:3], seekPoint[-1])
            p.cell.onWingWorldStoneTeleportConfirmed(wingWorldUtils.getPeaceCityDestId(transportId, cityId), tuple(seekPoint[:3]), seekPoint[-1])
            break


def onNavigateToCityTransportForBornIsland(seekPoint, transportId):
    gamelog.debug('@navigator wingWorld#onNavigateToBornIslandTransport', transportId, seekPoint[:3], seekPoint[-1])
    p = BigWorld.player()
    for e in p.entitiesInRange(10, 'Transport'):
        if e.charType == transportId:
            destId = NSD.data.get(const.SPACE_NO_WING_WORLD_ISLAND, {}).keys()[0]
            gamelog.debug('@navigator wingWorld#onWingWorldStoneTeleportConfirmed', transportId, seekPoint[:3], seekPoint[-1], destId)
            p.cell.onWingWorldStoneTeleportConfirmed(destId, tuple(seekPoint[:3]), seekPoint[-1])


def onNavigateToFinalSeekPoint():
    p = BigWorld.player()
    gamelog.debug('@navigator wingWorld#onNavigateToFinalSeekPoint', p.isRealGroupFollow())
    if p.isRealGroupFollow():
        p.updateGroupFollowPathFinding()
    gameglobal.rds.ui.map.hideSeekPos()
    gameglobal.rds.ui.littleMap.hideSeekTarget()
    gameglobal.rds.ui.questTrack.showPathFindingIcon(False)
    p.topLogo.setAutoPathingVisible(False)
    p.wingWorld.failedPathFindingInMultiCitySpace = False


def onFailedPathFindingInMultiCitySpace(seekPoint, bDelayed, endDist, showMsg, fromGroupFollow, failedCallback, bForceByNpc):
    gamelog.debug('@navigator onFailedPathFindingInMultiCitySpace', bForceByNpc)
    p = BigWorld.player()
    if p and p.inWorld:
        p.wingWorld.failedPathFindingInMultiCitySpace = True
        BigWorld.callback(0, Functor(pathFinding, seekPoint, bDelayed, endDist, showMsg, fromGroupFollow, failedCallback, bForceByNpc))


def onFailedPathFindingInSameSpace(failedCallback):
    gamelog.debug('@navigator onFailedPathFindingInSameSpace')
    p = BigWorld.player()
    if p and p.inWorld:
        gamelog.debug('@navigator onFailedPathFindingInSameSpace old failed:', p.wingWorld.failedPathFindingInMultiCitySpace)
        p.wingWorld.failedPathFindingInMultiCitySpace = False
        if failedCallback:
            BigWorld.callback(0, Functor(failedCallback))
