#Embedded file name: /WORKSPACE/data/entities/client/helpers/navigator.o
import random
import math
import time
import BigWorld
import Math
import GUI
import ResMgr
import keys
import gametypes
import formula
import const
import gameglobal
import utils
import gamelog
import clientcom
import appSetting
import clientUtils
from sfx import sfx
from callbackHelper import Functor
from helpers import cellCmd
from helpers.quadTree import QuadTree
from helpers import qingGong
from helpers import protect
from sMath import distance2D, distance3D
from cdata import game_msg_def_data as GMDD
from data import zaiju_data as ZJD
from guis import events
from data import navigator_digong_data as NDD
from data import navigator_stone_data as NSD
from data import multiline_digong_data as MDD
from data import guild_config_data as GCD
from data import seeker_data as SD
from data import sys_config_data as SCD
from data import npc_teleport_data as NTD
from cdata import teleport_data as TD
LOG_TIME = 0
LAST_FUNC = 'None'

def logTime(func):

    def _deco(*args, **kwargs):
        global LOG_TIME
        global LAST_FUNC
        start = time.time()
        gamelog.debug('b.e.:logTime_prev %s --> %s (%f)' % (LAST_FUNC, func.__name__, start - LOG_TIME))
        LOG_TIME = start
        LAST_FUNC = func.__name__
        ret = func(*args, **kwargs)
        gamelog.debug('b.e.:logTime_end', func.__name__, start, time.time() - start)
        return ret

    return _deco


LAND_MOVE_MAX_DISTANCE = 500
SPACE_LAND_DISTANCE = {const.GUILD_SCENE_NO: 300}
STONE_NUM = 6
ROAD_NUM = 2
LADDER_NUM = 1
UNKNOWN_Y = 3000
EXTENT_Y = 100
EXTENT_NORMALY = 4
EXTENT_POSY = 20
VECTOR_ZERO = Math.Vector3(0, 0, 0)
RETRY_TIEMS = 5
LINES_CHUNK = 3
SUCCESS = 1
FAILED = 2
ARRIVED = 3
SEEKING = 4
FROMGROUNDDIST = 0.5
FROMWATERDIST = 0.5
gNavObj = None
gEnableScenePathfinding = None
gIsPublished = None
gCanLift = None
gCanInline = None
gCurrentSpaceNo = None
gFileList = []
gAvatarPhysics = None
gCanFly = True
gCanFixLandMove = True
gCanOptimizeFixLandMove = True
gCanTeleport = True
gCanLadder = False
gTeleportSwitch = True
gShowTrace = False
stoneMod = None

def getStoneMod():
    global stoneMod
    if stoneMod is None:
        import Transport
        stoneMod = Transport
    return stoneMod


worldMapMod = None

def getWorldMap():
    global worldMapMod
    return worldMapMod


stonesWaypointDataObj = None
g_moveTime = -1
g_firstMove = True

def getStonesWaypointDataM():
    global stonesWaypointDataObj
    if utils.enableBDB:
        return stonesWaypointDataObj
    if stonesWaypointDataObj is None:
        try:
            from data import stones_waypoint_data
            stonesWaypointDataObj = stones_waypoint_data
        except ImportError:
            stonesWaypointDataObj = None

    return stonesWaypointDataObj


landPointDataObj = None

def getLandPointDataM():
    global landPointDataObj
    if utils.enableBDB:
        return landPointDataObj
    if landPointDataObj is None:
        try:
            from data import land_points_data
            landPointDataObj = land_points_data
        except ImportError:
            landPointDataObj = None

    return landPointDataObj


landLineDataObj = None

def getLandLineDataM():
    global landLineDataObj
    if utils.enableBDB:
        return landLineDataObj
    if landLineDataObj is None:
        try:
            from data import land_lines_data
            landLineDataObj = land_lines_data
        except ImportError:
            landLineDataObj = None

    return landLineDataObj


g_landpathdatas = {}

def getLandPathsDataM(spaceNo = None):
    global g_landpathdatas
    if spaceNo is None:
        p = BigWorld.player()
        spaceNo = p.mapID
    spaceNo = getPhaseMappingNum(spaceNo)
    mod = g_landpathdatas.get(spaceNo, None)
    if mod is None:
        if utils.enableBDB:
            return
        try:
            mod = __import__('data.land_paths_data_%d' % spaceNo)
            mod = getattr(mod, 'land_paths_data_%d' % spaceNo)
            g_landpathdatas[spaceNo] = mod
        except ImportError:
            mod = None

    return mod


flyPointDataObj = None

def getFlyPointDataM():
    global flyPointDataObj
    if utils.enableBDB:
        return flyPointDataObj
    if flyPointDataObj is None:
        try:
            from data import flypoints_data
            flyPointDataObj = flypoints_data
        except ImportError:
            flyPointDataObj = None

    return flyPointDataObj


if utils.enableBDB:
    try:
        from data import land_points_data
        landPointDataObj = land_points_data
    except:
        pass

    try:
        from data import land_lines_data
        landLineDataObj = land_lines_data
    except:
        pass

    try:
        from data import flypoints_data
        flyPointDataObj = flypoints_data
    except:
        pass

    try:
        from data import stones_waypoint_data
        stonesWaypointDataObj = stones_waypoint_data
    except:
        pass

    try:
        ecd = ResMgr.openSection('entities/client/data')
        if ecd:
            cd = ecd.keys()
        else:
            cd = ()
        for name in cd:
            try:
                if name.startswith('land_paths_data_'):
                    dataname = name.split('.')[0]
                    mod = __import__('data.%s' % dataname)
                    mod = getattr(mod, dataname)
                    g_landpathdatas[int(dataname.replace('land_paths_data_', ''))] = mod
            except:
                continue

    except:
        pass

def isSameSpaceInPhaseMapping(spaceNo1, spaceNo2):
    pmn1 = getPhaseMappingNum(spaceNo1)
    pmn2 = getPhaseMappingNum(spaceNo2)
    return spaceNo1 == pmn2 or spaceNo2 == pmn1 or spaceNo1 == spaceNo2 or pmn1 == pmn2


def isPassingPhase(spaceNo1, spaceNo2):
    spaceNo1 = formula.getMapId(spaceNo1)
    spaceNo2 = formula.getMapId(spaceNo2)
    pmn1 = getPhaseMappingNum(spaceNo1)
    pmn2 = getPhaseMappingNum(spaceNo2)
    inPhase1 = pmn1 != spaceNo1
    inPhase2 = pmn2 != spaceNo2
    if inPhase1 and not inPhase2 or inPhase1 and not inPhase2:
        return True
    return False


def getPhaseMappingNum(spaceNo):
    if formula.spaceInWingCity(spaceNo):
        return formula.getWingCityMapId(spaceNo)
    mapName = getPhaseMappingNameBySpaceNo(spaceNo)
    spaceNo = formula.getMapId(spaceNo)
    return formula.getSpaceNo(mapName, spaceNo)


ladderData = {1: (-429,
     129.28,
     -880.6,
     3),
 2: (-429,
     8.34,
     -880.6,
     3)}
ladderInfo = {}

def initLadderInfo():
    global ladderInfo
    for id, info in ladderData.iteritems():
        x, y, z, spaceNo = info
        if not ladderInfo.has_key(spaceNo):
            ladderInfo[spaceNo] = {}
        ladderInfo[spaceNo][id] = (x,
         y,
         z,
         spaceNo)


def getLadderInfo(spaceNo):
    if not ladderInfo:
        initLadderInfo()
    ret = {}
    if ladderInfo.has_key(spaceNo):
        ladder = ladderInfo[spaceNo]
        for id, info in ladder.iteritems():
            ret[id] = info[:]

    return ret


schoolNpcInfo = {}

def initNpcInfo():
    global schoolNpcInfo
    for id, info in NTD.data.iteritems():
        npcTrack = info.get('npcTk', 0)
        sd = SD.data.get(npcTrack, {})
        if sd:
            spaceNo = sd['spaceNo']
            xpos = sd['xpos']
            ypos = sd['ypos']
            zpos = sd['zpos']
            schoolNpcInfo.setdefault(spaceNo, {})
            schoolNpcInfo[spaceNo][id] = (xpos,
             ypos,
             zpos,
             spaceNo)


def getNpcInfo(spaceNo):
    if not schoolNpcInfo:
        initNpcInfo()
    ret = {}
    if schoolNpcInfo.has_key(spaceNo):
        npcInfo = schoolNpcInfo[spaceNo]
        for id, info in npcInfo.iteritems():
            ret[id] = info[:]

    return ret


def isInSchoolArea(pos):
    schoolArea = SCD.data.get('schoolArea', [((3900, 2400), (6300, 4500))])
    for area in schoolArea:
        lb, rt = area
        if rt[0] >= pos[0] >= lb[0] and rt[1] >= pos[2] >= lb[1]:
            return True

    return False


def canUseNpcTeleport(seekPoint):
    return False
    player = BigWorld.player()
    if isInSchoolArea(player.position) and isInSchoolArea(seekPoint):
        return True
    return False


def cmpDist(pos1, pos2, targetpos):
    return cmp((Math.Vector3(pos1[0], pos1[1], pos1[2]) - targetpos).length, (Math.Vector3(pos2[0], pos2[1], pos2[2]) - targetpos).length)


def cmpDistTgtAndSrc(pos1, pos2, targetpos, pos3, pos4, srcPos):
    return cmp((Math.Vector3(pos1[0], pos1[1], pos1[2]) - targetpos).length + (Math.Vector3(pos3[0], pos3[1], pos3[2]) - srcPos).length, (Math.Vector3(pos2[0], pos2[1], pos2[2]) - targetpos).length + (Math.Vector3(pos4[0], pos4[1], pos4[2]) - srcPos).length)


def getStoneInfo(spaceNo, needVisited = True, seekPoints = None):
    if spaceNo in const.MULTI_CITY_SPACE_NO:
        return {}
    ret = {}
    if NSD.data.has_key(spaceNo):
        stone = NSD.data[spaceNo]
        for destId, info in stone.iteritems():
            if getStoneMod().isActiveStone(destId):
                if BigWorld.player().inGroupFollow and getStoneMod().getHiddenStone(destId):
                    continue
                if info[-1] == 0 or seekPoints == None or seekPoints and info[-1] > 0 and distance2D(info[:3], seekPoints) < info[-1]:
                    ret[destId] = info[:4]

    return ret


def getNearestDiGongStone(spaceNo):
    if not gameglobal.rds.configData.get('enableCrossDiGongNavigator', True):
        return None
    stone = NDD.data.get(spaceNo, {})
    p = BigWorld.player()
    if stone and p:
        ret = {}
        for key, value in stone.iteritems():
            if value[3] == p.mapID:
                ret[key] = value

        if not ret:
            return None
        ret = ret.items()
        ret.sort(cmp=lambda x, y: cmpDist(x[1], y[1], p.position))
        return ret[0][1]


def getBounds(spaceNo):
    path = formula.whatSpaceMap(spaceNo)
    spacesettings = path + '/space.settings'
    bounds = ResMgr.openSection(spacesettings)
    if bounds:
        ulx = bounds.readInt('bounds/minX') * 100.0
        uly = bounds.readInt('bounds/maxY') * 100.0 + 100.0
        drx = bounds.readInt('bounds/maxX') * 100.0 + 100.0
        dry = bounds.readInt('bounds/minY') * 100.0
        return (ulx,
         uly,
         drx,
         dry)
    else:
        return None


def _getPortDist(port1, port2):
    landL = getLandLineDataM()
    lidx = port1 < port2 and (port1, port2) or (port2, port1)
    if landL.data.has_key(lidx):
        points = list(landL.data[lidx][0][0]) + []
        if points[-1] == port1:
            points.reverse()
        return (landL.data[lidx][0][2], points)
    else:
        return None


def processPort(spaceNo, portid):
    return portid + spaceNo * 10000


def reload_me():
    initNav()
    p = BigWorld.player()
    if p and hasattr(p, 'spaceNo'):
        getNav().InitSeekNavsBySpaceNo(p.mapID)
        getNav().clearOtherNavs()


def cl():
    global lineQueue
    while len(lineQueue) > 0:
        for i in lineQueue:
            GUI.delRoot(i)
            lineQueue.remove(i)


def getVectorsByAngle(p1, p2, r, angle = 0):
    stdv = p2 - p1
    rotm = Math.Matrix()
    rotm.setRotateY(angle)
    tv = rotm.applyVector(stdv)
    tv.normalise()
    return tv * r


def initNav():
    global gCanInline
    global gFileList
    global gCanLift
    global gIsPublished
    gIsPublished = True
    gCanLift = False
    gCanInline = True
    dsfiles = ResMgr.openSection('navmesh')
    if dsfiles:
        dskeys = dsfiles.keys()
    else:
        dskeys = []
    gamelog.debug('l.b.@navigator initNav', dsfiles, dskeys)
    gFileList = []
    for name in dskeys:
        if clientcom.isFileExist('navmesh/%s/polysets.xml' % name):
            gFileList.append(name)

    gamelog.debug('l.b.@navigator initNav#2', gFileList)
    getNav()


def getNav():
    global gNavObj
    if gNavObj is None:
        gNavObj = navigator()
    return gNavObj


def getPhaseMappingName(mapName):
    mapName = BigWorld.getPhaseMapping('universes/eg/' + mapName)
    if mapName:
        mapName = mapName.split('/')[-1]
    return mapName


def getPhaseMappingNameBySpaceNo(spaceNo):
    mapName = formula.whatSpaceMap(spaceNo).split('/')[-1]
    phaseMapName = getPhaseMappingName(mapName)
    if phaseMapName:
        return phaseMapName
    return mapName


def checkWapPointHot(spaceNo):
    mapName = formula.whatSpaceMap(spaceNo).split('/')[-1]
    if mapName in gFileList:
        return True
    else:
        mapName = getPhaseMappingName(mapName)
        if mapName in gFileList:
            return True
        return False


def checkWayPoint():
    global gEnableScenePathfinding
    global gCurrentSpaceNo
    p = BigWorld.player()
    if gCurrentSpaceNo is None or gCurrentSpaceNo != p.mapID:
        gCurrentSpaceNo = p.mapID
        if not formula.canSpaceNavigate(gCurrentSpaceNo):
            gEnableScenePathfinding = False
            return
        mapName = formula.whatSpaceMap(gCurrentSpaceNo).split('/')[-1]
        if mapName in gFileList:
            gEnableScenePathfinding = True
        else:
            mapName = getPhaseMappingName(mapName)
            if mapName in gFileList:
                gEnableScenePathfinding = True
            else:
                gEnableScenePathfinding = False


def canScenePathfinding():
    checkWayPoint()
    return gEnableScenePathfinding


def getPointOnTheCircle(v1, v2, p, r):
    a = p - v1
    b = v2 - v1
    if b.length == 0:
        return None
    pab = a.dot(b) / b.length
    tl = pab - math.sqrt(math.fabs(r * r - a.length * a.length + pab * pab))
    return tl * b / b.length + v1


def get_vector_cos(v0, v1, v2):
    a = v1 - v0
    a.y = 0
    b = v2 - v1
    b.y = 0
    if a.length == 0 or b.length == 0:
        return 1.0
    return a.dot(b) / (a.length * b.length)


def get_vector_cos1(v0, v1, v2):
    a = v1 - v0
    a.y = 0
    b = v2 - v0
    b.y = 0
    if a.length == 0 or b.length == 0:
        return 1.0
    return a.dot(b) / (a.length * b.length)


def landPointsGeter_0(p1, p2):
    LPM = getLandPointDataM()
    return cmp(LPM.data[p1][0], LPM.data[p2][0])


def landPointsGeter_2(p1, p2):
    LPM = getLandPointDataM()
    return cmp(LPM.data[p1][2], LPM.data[p2][2])


lineQueue = []

def drawPoint(p, colour = (0,
 255,
 255,
 255)):
    global VECTOR_ZERO
    if p is None:
        return
    tp1 = p - VECTOR_ZERO
    tp2 = p - VECTOR_ZERO
    tp1.y += 0.0
    tp2.y += 0.10000000000000009
    point = GUI.WorldDebugGUI()
    point.startPos = tp1
    point.endPos = tp2
    point.colour = colour
    point.radius = 0.05
    lineQueue.append(point)
    GUI.addRoot(point)


def drawLine(p1, p2, color, Float = False):
    line = GUI.WorldDebugGUI()
    line.startPos = p1 - VECTOR_ZERO
    line.endPos = p2 - VECTOR_ZERO
    if Float:
        line.startPos.y += 0.5
        line.endPos.y += 0.5
    line.colour = color
    line.radius = 0.0001
    lineQueue.append(line)
    GUI.addRoot(line)


def clearLine():
    if gIsPublished:
        return
    while len(lineQueue):
        for l in lineQueue:
            GUI.delRoot(l)
            lineQueue.remove(l)


LANDMOVE = 0
FLYMOVE = 1
LANDTESTMOVE = 2
LANDFIXMOVE = 3
DELAYMOVE = 4
DIRECT_RIDEDIST = 80
EVAL_RIDEDIST = 299
FLYDIST = 10
DDISTFORTELEPORT = 200
NEEDRATE = 0.1
MOVEBACKDIST = 5
NEEDTESTDIST = 99
CANLANDFIXMOVEDIST = 150
FORCECANLANDFIXMOVEDIST = 30
CAN_RIDE = 1
HAVE_IN_RIDE = 2
TRY_RIDE_FAIL = 3

def getNeedTestDist():
    if getNav().forceFixLandMove:
        return 0
    return LAND_MOVE_MAX_DISTANCE


def getCanLandFixMovedDist():
    if getNav().forceFixLandMove:
        return 30
    return 150


def getLandMoveMaxDistance(mapId):
    return SPACE_LAND_DISTANCE.get(mapId, LAND_MOVE_MAX_DISTANCE)


TOLERATION_TIME = 6
START_TIME = 0
TOLERATION_DOWNTO_GROUND = 5.0

def startTimer():
    global START_TIME
    START_TIME = BigWorld.time()


def checkTimer():
    if BigWorld.time() - START_TIME > TOLERATION_TIME:
        return True
    else:
        return False


class navigator(object):

    def __init__(self):
        global gEnableScenePathfinding
        self.parent = None
        self.retryTimes = RETRY_TIEMS
        self.seekNavs = {}
        self.showNavs = {}
        self.qts = {}
        self.currentNav = None
        self.onSeek = False
        self.lastPos = None
        self.seekDest = None
        self.onRiding = None
        self.evalPosList = None
        self.evalIdList = None
        self.calculatePos = {}
        self.teleportDstDist = 0
        self.teleportSrcDist = 0
        self.seekMsgBox = None
        self.startPos = None
        self.disStatus = False
        self.collideFunc = BigWorld.collide
        self.dropFunc = BigWorld.findDropPoint
        self.pathTraceM = PathTraceManager()
        self.srcStoneIndex = None
        self.dstStoneIndex = None
        self.srcStoneDist = None
        self.dstStoneDist = None
        self.srcStonePos = None
        self.dstStonePos = None
        self.testDist = None
        self._distCache = {}
        self.lastPosCache = None
        self.delayData = {}
        self.midPartition = 0
        self.lastDirection = 0
        self.arriveCallback = None
        self.failedCallback = None
        self.ignorPflag = False
        self.endDist = 1.5
        self.traceVerNum = 0
        gEnableScenePathfinding = False
        self.onShowTrace = False
        self.startShowPos = None
        self.onShow = False
        self.currentShowNav = None
        self.lastShowPos = None
        self.currentTraceIdx = 0
        self.currentShowPos = None
        self.tracePosList = []
        self.navDropPoints = []
        self.showPoints = []
        self.readyToDrawPoints = []
        self.preShowPoint = []
        self.tryFlyFlag = False
        self.tryLandFlag = False
        self.pathFindingVer = 0
        self.currentMode = -1
        self.flyPoints = []
        self.infly = False
        self.upFlyVer = 0
        self.currentDst = None
        self.startDownToGroundTime = None
        self.lastFlyNavGroundDist = 0
        self.srcLandPorts = []
        self.dstLandPorts = []
        self.srcLandPortDists = {}
        self.dstLandPortDists = {}
        self.delayVer = 0
        self.forceFixLandMove = True
        self.moveQueue = []
        self.delayPathFindingCallback = None
        self.useLadderOnce = False
        self.buildAllQuadTree()
        initLadderInfo()
        self.lastPathFindTime = 0
        self.fromGroupFollow = False
        self.resetPathFindingCallBack = None

    def _clearDistThreadCache(self):
        self._distCache = {}

    def _evaluateDistThreadCache(self, dstX, dstY, dstZ, srcX, srcY, srcZ, res, key, callback, findbest = 0):
        distKey = '%.1f %.1f %.1f %.1f %.1f %.1f' % (dstX,
         dstY,
         dstZ,
         srcX,
         srcY,
         srcZ)
        distValue = self._distCache.get(distKey, None)
        if distValue != None:
            if res[0] == -1 or distValue < res[0]:
                gamelog.debug('l.b.@navigator hit distcache', distKey, distValue)
                res[0] = distValue
                res[1] = key
            if callback:
                BigWorld.callback(0, callback)
            return True
        return self.currentNav.evaluateDistThread(dstX, dstY, dstZ, srcX, srcY, srcZ, res, key, Functor(self._evaluateDistThreadCacheCallback, res, distKey, res[0], callback), findbest)

    def _evaluateDistThreadCacheCallback(self, res, distKey, prevDist, callback):
        if prevDist == -1 or res[0] < prevDist:
            self._distCache[distKey] = res[0]
        if callback:
            BigWorld.callback(0, callback)

    def findClosestPos(self, src, res, index, ver, findCallback, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback):
        self._findClosestPos(src, res, index, ver, findCallback, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback)

    def nepActionRoleMoveTo(self, seekPoint):
        now = time.time()
        if now - self.lastPathFindTime < 0.1:
            return
        if not seekPoint:
            return
        try:
            protect.nepActionRoleMoveTo(protect.eMove_AutoToPlace, seekPoint[0], seekPoint[2])
            self.lastPathFindTime = now
        except:
            pass

    def _findClosestPos(self, src, res, index, ver, findCallback, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback):
        gamelog.debug('b.e.@navigator _findClosestPos', src, res, index, ver, seekPoint, parent, showMsg)
        p = BigWorld.player()
        if not p.isPathfinding or ver != self.pathFindingVer:
            return
        if not self.evalPosList:
            return
        if index >= len(self.evalPosList):
            gamelog.debug('l.b.@navigator _findClosestPos case1', res, index, self.evalPosList, self.calculatePos)
            if res[1] != -1:
                gamelog.debug('l.b.@navigator _findClosestPos case2')
                findCallback(res, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback)
                return
            if self.calculatePos:
                for k, v in self.calculatePos.iteritems():
                    if v[0] > 0:
                        if res[0] < 0 or res[0] > v[0]:
                            res = [v[0], k]

                gamelog.debug('l.b.@navigator _findClosestPos case3', res, seekPoint)
                findCallback(res, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback)
                return
            gamelog.debug('l.b.@navigator _findClosestPos case4')
            if isSameSpaceInPhaseMapping(p.mapID, seekPoint[-1]):
                self._stopPathFinding(False)
                gamelog.debug('l.b.@navigator _findClosestPos case5')
                BigWorld.callback(0, Functor(self._pathFinding, seekPoint, parent, failedCallback, False, endDist, arriveCallback, None, False))
                return
            dis = p.qinggongMgr.getDistanceFromGround()
            if p.canFly() and dis and dis > 10:
                p.showGameMsg(GMDD.data.CAN_NOT_PATH_FIND_TOO_HIGH, ())
            else:
                p.showGameMsg(GMDD.data.NO_TELEPORT_IN_DEST_EX, (formula.whatSpaceName(p.spaceNo, False), formula.whatSpaceName(seekPoint[-1], False)))
            gamelog.debug('l.b.@navigator _findClosestPos case6')
            self.onFailedCall(showMsg=False)
            return
        pos = self.evalPosList[index]
        gamelog.debug('b.e.@navigator _findClosestPos#1', pos, index, self.evalPosList)
        self._evaluateDistThreadCache(src.x, src.y, src.z, pos[0], pos[1], pos[2], res, index, Functor(self._findClosestPos, src, res, index + 1, ver, findCallback, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback), 0)

    def pathFindingTeleport(self, evaldist, seekPoint, parent = None, failedCallback = None, showMsg = True, endDist = 1.5, arriveCallback = None, onRiding = None):
        gamelog.debug('b.e.@navigator step3 pathFindingTeleport', evaldist, seekPoint, parent, showMsg)
        p = BigWorld.player()
        if p.stateMachine.checkStatus(const.CT_AUTO_PATHFINDING):
            if canScenePathfinding():
                if p.isPathfinding:
                    self._stopPathFinding(showMsg)
                if evaldist == -1 and seekPoint[1] == UNKNOWN_Y:
                    stoneInfo = self._getNearbyGroundStone(seekPoint)
                    if stoneInfo:
                        pos_list = []
                        id_list = []
                        for id, pos in stoneInfo:
                            id_list.append(id)
                            pos_list.append(pos)

                        self.evalPosList = pos_list
                        self.evalIdList = id_list
                        res = [0, 0]
                        self.calculatePos = {}
                        gamelog.debug('b.e.@navigator step3.0 pathFindingTeleport, call _getNearbyGroundStone:', self.evalPosList, self.evalIdList)
                        BigWorld.callback(0, Functor(self.pathfindingTCallback, res, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback))
                        return SUCCESS
                if canUseNpcTeleport(seekPoint):
                    stoneInfo = getNpcInfo(getPhaseMappingNum(seekPoint[-1])).items()
                else:
                    stoneInfo = getStoneInfo(getPhaseMappingNum(seekPoint[-1]), True, seekPoint[:3]).items()
                if len(stoneInfo) == 0:
                    gamelog.debug('l.b.@navigator step3.1 pathFindingTeleport, has no stoneinfo')
                    if isSameSpaceInPhaseMapping(p.mapID, seekPoint[-1]):
                        self._stopPathFinding(False)
                        gamelog.debug('l.b.@navigator step3.1 pathFindingTeleport, has no stoneinfo, call _pathFinding', seekPoint)
                        BigWorld.callback(0, Functor(self._pathFinding, seekPoint, parent, failedCallback, False, endDist, arriveCallback, onRiding, False))
                        return SUCCESS
                    if p.canFly():
                        p.loseGravity()
                    p.showGameMsg(GMDD.data.NO_TELEPORT_IN_DEST_EX, (formula.whatSpaceName(p.spaceNo, False), formula.whatSpaceName(seekPoint[-1], False)))
                    return FAILED
                if evaldist > 0 and evaldist < getLandMoveMaxDistance(p.mapID):
                    if isSameSpaceInPhaseMapping(p.mapID, seekPoint[-1]):
                        self._stopPathFinding(False)
                        gamelog.debug('l.b.@navigator pathFindingTeleport, has stoneinfo, but evaldist is short, call _pathFinding', seekPoint, evaldist)
                        self.pathFindingInner(seekPoint, parent, failedCallback, False, endDist, arriveCallback, self.onRiding, False)
                        return SUCCESS
                    p.showGameMsg(GMDD.data.NO_TELEPORT_IN_DEST_EX, (formula.whatSpaceName(p.spaceNo, False), formula.whatSpaceName(seekPoint[-1], False)))
                    return FAILED
                gamelog.debug('l.b.@navigator pathFindingTeleport, has stoneinfo')
                stoneInfo.sort(cmp=lambda x, y: cmpDist(x[1], y[1], Math.Vector3(*seekPoint[:3])))
                stoneInfo = stoneInfo[:STONE_NUM]
                pos_list = []
                id_list = []
                for id, pos in stoneInfo:
                    id_list.append(id)
                    pos_list.append(pos)

                self.evalPosList = pos_list
                self.evalIdList = id_list
                self.currentNav = self.seekNavs.get(getPhaseMappingNum(seekPoint[-1]), None)
                gamelog.debug('b.e.@navigator pathFindingTeleport#1', pos_list, id_list)
                if not self.currentNav:
                    self.currentNav = self.seekNavs.get(getPhaseMappingNum(seekPoint[-1]), None)
                    if not self.currentNav:
                        if not showMsg:
                            self.onFailedCall()
                            return FAILED
                        p.isPathfinding = True
                        self.InitSeekNavsBySpaceNo(getPhaseMappingNum(seekPoint[-1]), False, Functor(self.pathFindingTeleport, evaldist, seekPoint, parent, failedCallback, False, endDist, arriveCallback, onRiding))
                        self.clearOtherNavs(getPhaseMappingNum(seekPoint[-1]))
                        return SUCCESS
                p.isPathfinding = True
                res = [-1, -1]
                self.pathFindingVer += 1
                gamelog.debug('b.e.@navigator pathFindingTeleport call findClosestPos', seekPoint)
                self.findClosestPos(Math.Vector3(*seekPoint[:3]), res, 0, self.pathFindingVer, self.pathfindingTCallback, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback)
                return SUCCESS
            else:
                if showMsg:
                    p.showGameMsg(GMDD.data.CAN_NOT_PATH_FIND_IN_CUR_SCENE, ())
                failedCallback and failedCallback()
                return FAILED
        else:
            p.showGameMsg(GMDD.data.CAN_NOT_AUTO_PATH_FIND, ())
            self.onFailedCall()
            return FAILED

    def _getNearbyGroundStone(self, seekPoint):
        targetpos = Math.Vector2(seekPoint[0], seekPoint[2])
        if canUseNpcTeleport(seekPoint):
            stoneInfo = getNpcInfo(getPhaseMappingNum(seekPoint[-1])).items()
        else:
            stoneInfo = getStoneInfo(getPhaseMappingNum(seekPoint[-1]), True, seekPoint[:3]).items()
        if len(stoneInfo) == 0:
            return None
        stoneInfo.sort(cmp=lambda x, y: self._cmpDistGround(x[1], y[1], targetpos))
        return stoneInfo[:1]

    def _cmpDistGround(self, pos1, pos2, targetpos):
        return cmp((Math.Vector2(pos1[0], pos1[2]) - targetpos).length, (Math.Vector2(pos2[0], pos2[2]) - targetpos).length)

    def pathfindingTCallback(self, res, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback):
        gamelog.debug('b.e.@navigator pathfindingTCallback', res, seekPoint, parent, showMsg)
        p = BigWorld.player()
        dist, index = res[:2]
        for k, v in self.calculatePos.iteritems():
            if v[0] != -1 and dist > v[0]:
                dist = v[0]
                index = k

        self.teleportDstDist = dist
        if self.evalIdList and index < len(self.evalIdList):
            self.dstStoneIndex = self.evalIdList[index]
            self.dstStonePos = self.evalPosList[index]
            self.dstStoneDist = dist
            gamelog.debug('b.e.@navigator pathfindingTCallback#1', self.dstStoneIndex, self.dstStonePos, self.dstStoneDist)
            spaceNo = getPhaseMappingNum(p.mapID)
            if canUseNpcTeleport(seekPoint):
                stoneInfo = getNpcInfo(getPhaseMappingNum(seekPoint[-1])).items()
            else:
                stoneInfo = getStoneInfo(spaceNo, False).items()
            if len(stoneInfo) == 0:
                p.showGameMsg(GMDD.data.NO_TELEPORT_IN_DEST_EX, (formula.whatSpaceName(p.spaceNo, False), formula.whatSpaceName(seekPoint[-1], False)))
                self.stopPathFinding(False)
                failedCallback and failedCallback()
                return
            stoneInfo.sort(cmp=lambda x, y: cmpDist(x[1], y[1], p.position))
            stoneInfo = stoneInfo[:STONE_NUM]
            pos_list = []
            id_list = []
            for id, pos in stoneInfo:
                id_list.append(id)
                pos_list.append(pos)

            self.evalPosList = pos_list
            self.evalIdList = id_list
            self.currentNav = self.seekNavs.get(spaceNo, None)
            if not self.currentNav:
                self.currentNav = self.seekNavs.get(getPhaseMappingNum(seekPoint[-1]), None)
                if not self.currentNav:
                    self.stopPathFinding()
                    return
            p.isPathfinding = True
            res = [-1, -1]
            self.pathFindingVer += 1
            self.findClosestPos(p.position, res, 0, self.pathFindingVer, self.pathfindingTCallback2, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback)
        else:
            p.showGameMsg(GMDD.data.PATH_FIND_ERROR, ())
            self.stopPathFinding()

    def pathfindingTCallback2(self, res, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback):
        gamelog.debug('b.e.@navigator pathfindingTCallback2', res, seekPoint, parent, showMsg)
        p = BigWorld.player()
        dist, index = res[:2]
        for k, v in self.calculatePos.iteritems():
            if v[0] != -1 and dist > v[0]:
                dist = v[0]
                index = k

        self.teleportSrcDist = dist
        if self.evalIdList and index < len(self.evalIdList):
            self.srcStoneIndex = self.evalIdList[index]
            self.srcStonePos = self.evalPosList[index]
            self.srcStoneDist = dist
            gamelog.debug('b.e.@navigator pathfindingTCallback2#1', self.srcStoneIndex, self.srcStonePos, self.srcStoneDist, self.dstStoneIndex)
            if self.srcStoneIndex == self.dstStoneIndex:
                self.pathFindingInner(seekPoint, parent, failedCallback, False, endDist, arriveCallback, self.onRiding, False)
            else:
                if isSameSpaceInPhaseMapping(p.mapID, seekPoint[-1]):
                    if self.testDist is None or self.testDist == -1 and (self.dstStoneDist == -1 or self.srcStoneDist == -1) or self.testDist >= 0 and self.dstStoneDist >= 0 and self.srcStoneDist >= 0 and self.testDist - DDISTFORTELEPORT < self.srcStoneDist + self.dstStoneDist:
                        self.pathFindingInner(seekPoint, parent, failedCallback, False, endDist, arriveCallback, self.onRiding, False)
                        return
                price = p.getTeleportCost(self.dstStoneIndex)
                if price > p.cash + p.bindCash or not p.checkInAutoQuest() and not p.stateMachine.checkStatus_check(const.CT_TELEPORT_BY_NPC):
                    gamelog.debug('b.e.@navigator pathfindingTCallback2#1~~~~~~~~~~~~~~~~~')
                    if getattr(p, 'groupNUID', None) and getattr(p, 'inGroupFollow', None):
                        p.cell.cancelGroupFollow()
                        p.showGameMsg(GMDD.data.GROUP_FOLLOW_NOT_ENOUGH_CASH, ())
                        return
                    if price > p.cash + p.bindCash:
                        p.showGameMsg(GMDD.data.NAVIGATOR_NOT_ENOHGU_CASH, ())
                    if isSameSpaceInPhaseMapping(p.mapID, seekPoint[-1]):
                        self.pathFindingInner(seekPoint, parent, failedCallback, False, endDist, arriveCallback, self.onRiding, False)
                        return
                    self.onFailedCall(False)
                    return
                if self.teleportSrcDist == -1 or self.teleportDstDist == -1:
                    evalDist = -1
                else:
                    evalDist = self.teleportSrcDist + self.teleportDstDist
                if evalDist == -1 or evalDist >= EVAL_RIDEDIST:
                    self.onRiding = CAN_RIDE
                spaceNo = getPhaseMappingNum(p.mapID)
                self.pathFindingInner(self.srcStonePos[:3] + (spaceNo,), parent, failedCallback, False, endDist, Functor(self.pathfindingTArriveCallback, self.dstStoneIndex, seekPoint, arriveCallback), self.onRiding, False)
        else:
            p.showGameMsg(GMDD.data.PATH_FIND_ERROR, ())
            self.stopPathFinding()

    def pathfindingTArriveCallback(self, stoneid, seekpoint, arriveCallback):
        p = BigWorld.player()
        dist = -1
        stoneEn = None
        stoneSet = getStoneMod().activeStoneSet
        if canUseNpcTeleport(p.position):
            npcEnts = BigWorld.entities.values()
            for stone in npcEnts:
                sdist = (stone.position - p.position).length
                if (dist == -1 or sdist < dist) and getattr(stone, 'npcInstance', False):
                    dist = sdist
                    stoneEn = stone

        else:
            for stone in stoneSet:
                sdist = (stone.position - p.position).length
                if dist == -1 or sdist < dist:
                    dist = sdist
                    stoneEn = stone

        gamelog.debug('bgf@navigator pathfindingTArriveCallback', stoneEn, stoneid, seekpoint)
        if stoneEn and hasattr(p, 'lockTarget'):
            p.lockTarget(stoneEn)
            if canUseNpcTeleport(seekpoint):
                ntd = NTD.data.get(stoneEn.npcId, {})
                index = -1
                if stoneid in ntd.get('npcTeleport', []):
                    index = ntd['npcTeleport'].index(stoneid)
                if index != -1:
                    spaceNo = p.spaceNo
                    if p.groupHeader == p.id:
                        p.syncHeaderClientGroundPos(force=True)
                        p.cell.startGroupHeaderFollowSync()
                    stoneEn.cell.npcTeleport(spaceNo, index)
            else:
                if p.groupHeader == p.id:
                    p.syncHeaderClientGroundPos(force=True)
                    p.cell.startGroupHeaderFollowSync()
                fun = Functor(p.cell.realUseTransportStone, stoneEn.id)
                clientUtils.teleportToStone(fun, stoneid, True)
            if self.canSetDelay():
                self.setDelayPathFinding(1, delaycondition=p.continueRideTogetherNavigate)
                self.delayData['seekPoint'] = seekpoint
                self.delayData['arriveCallback'] = arriveCallback

    def canSetDelay(self):
        return BigWorld.player().isPathfinding and self.seekDest

    def isDelayOn(self):
        return len(self.delayData)

    def clearDelay(self):
        if self.delayData:
            self.delayVer += 1
            self.delayData = {}

    def setDelayPathFinding(self, delaytime = 0.01, delaycondition = None, delaycancelcondition = None):
        p = BigWorld.player()
        if p.isPathfinding and self.seekDest:
            self.clearDelay()
            self.delayData['parent'] = self.parent
            self.delayData['failedCallback'] = self.failedCallback
            self.delayData['arriveCallback'] = self.arriveCallback
            self.delayData['endDist'] = self.endDist
            spaceNo = getPhaseMappingNum(p.mapID)
            self.delayData['seekPoint'] = (self.seekDest.x,
             self.seekDest.y,
             self.seekDest.z,
             spaceNo)
            self.delayData['onRiding'] = self.onRiding
            self.delayData['forceFixLandMove'] = self.forceFixLandMove
            self.delayData['delaycondition'] = delaycondition
            self.delayData['delaycancelcondition'] = delaycancelcondition
            self.delayData['firstCall'] = False
            if self.delayPathFindingCallback:
                BigWorld.cancelCallback(self.delayPathFindingCallback)
            self.delayPathFindingCallback = None
            BigWorld.callback(delaytime, Functor(self.doDelayPathFinding, delaytime, self.delayVer))
            return self.delayVer

    def inDelayPathFinding(self):
        if self.delayData:
            return True
        return False

    def forceDelayPathFinding(self):
        if len(self.delayData) == 0:
            return
        p = BigWorld.player()
        if not p.spellingType:
            delaycondition = self.delayData['delaycondition']
            delaycancelcondition = self.delayData['delaycancelcondition']
            if delaycancelcondition and delaycancelcondition():
                self.clearDelay()
                return
            if not p.spellingType and gameglobal.rds.GameState == gametypes.GS_PLAYGAME and (not delaycondition or delaycondition()):
                if p.stateMachine.check_status(const.CT_AUTO_PATHFINDING):
                    gamelog.debug('jjh@navigator forceDelayPathFinding')
                    self._pathFinding(seekPoint=self.delayData['seekPoint'], parent=self.delayData['parent'], failedCallback=self.delayData['failedCallback'], arriveCallback=self.delayData['arriveCallback'], endDist=self.delayData['endDist'], onRiding=self.delayData['onRiding'], firstCall=False)
                    self.clearDelay()

    def doDelayPathFinding(self, delaytime, ver):
        if self.delayVer != ver:
            self.clearDelay()
            return
        p = BigWorld.player()
        delaycondition = self.delayData['delaycondition']
        delaycancelcondition = self.delayData['delaycancelcondition']
        if delaycancelcondition and delaycancelcondition():
            self.clearDelay()
            return
        mapID = formula.getMapId(self.delayData['seekPoint'][-1]) if self.delayData['seekPoint'][-1] else p.mapID
        if not p.spellingType and gameglobal.rds.GameState == gametypes.GS_PLAYGAME and self.seekNavs.has_key(mapID) and (not delaycondition or delaycondition()):
            gamelog.debug('b.e.@navigator doDelayPathFinding')
            if p.stateMachine.checkStatus(const.CT_AUTO_PATHFINDING):
                delayData = dict(self.delayData)
                self.clearDelay()
                seekPoint = self.getDropPoint(delayData['seekPoint'])
                gamelog.debug('b.e.@navigator doDelayPathFinding#1', seekPoint)
                ret = self._pathFinding(seekPoint=seekPoint, parent=delayData['parent'], failedCallback=delayData['failedCallback'], arriveCallback=delayData['arriveCallback'], endDist=delayData['endDist'], onRiding=delayData['onRiding'], firstCall=delayData['firstCall'], forceFixLandMove=delayData['forceFixLandMove'])
                if ret == SUCCESS:
                    p.topLogo.setAutoPathingVisible(True)
            else:
                self.clearDelay()
                self.onFailedCall()
        else:
            self.delayPathFindingCallback = BigWorld.callback(delaytime, Functor(self.doDelayPathFinding, delaytime, ver))

    def getDropPoint(self, seekPoint):
        p = BigWorld.player()
        pos = None
        if seekPoint[-1] == p.mapID and seekPoint[1] == UNKNOWN_Y:
            heightArray = (400, 300, 200, 100, 75, 50, 25)
            for h in heightArray:
                pos = self.dropFunc(p.spaceID, Math.Vector3(seekPoint[0], h, seekPoint[2]))
                if pos:
                    pos = pos[0]
                    break

        if not pos:
            return seekPoint
        return (pos[0],
         pos[1],
         pos[2],
         seekPoint[-1])

    def InitSeekNavsBySpaceNo(self, spaceNo, initShowNav = True, callback = None):
        gamelog.debug('jjh@navigator InitSeekNavsBySpaceNo', spaceNo, self.seekNavs)
        if spaceNo <= 0:
            return
        if spaceNo in self.seekNavs:
            self.initSeekNavsCallback(initShowNav, callback, self.seekNavs)
            return
        tFileList = [getPhaseMappingNameBySpaceNo(spaceNo)]
        BigWorld.initAllNavigators(tFileList, Functor(self.initSeekNavsCallback, initShowNav, callback))

    def buildAllQuadTree(self):
        if not gCanFixLandMove:
            return
        LPM = getLandPointDataM()
        if LPM:
            for k, v in LPM.data.iteritems():
                spaceNo = k / 10000
                if not self.qts.has_key(spaceNo):
                    bounds = getBounds(spaceNo)
                    if bounds:
                        qt = QuadTree(bounds, 10)
                        self.qts[spaceNo] = qt
                qt = self.qts.get(spaceNo, None)
                if qt:
                    qt.addPoint(pointData(k, v[0], v[1], v[2]))

    def doInitSeekNavs(self):
        BigWorld.initAllNavigators(gFileList, self.initSeekNavsCallback)

    def initSeekNavsCallback(self, initShowNav, callback, navs):
        gamelog.debug('jjh@navigator initSeekNavsCallback', navs, self.seekNavs)
        p = BigWorld.player()
        if navs != self.seekNavs:
            for k, v in navs.iteritems():
                spaceNos = formula.whatAllSpaceNoByFileName(k)
                for spaceNo in spaceNos:
                    self.seekNavs[spaceNo] = v

        if callback and p.isPathfinding:
            callback()
        gamelog.debug('jjh@navigator initSeekNavsCallback end', navs, self.seekNavs)

    def landMove(self, src, dst, evaldist, ver):
        p = BigWorld.player()
        if not p.isPathfinding or ver != self.pathFindingVer:
            return
        self.retryTimes = RETRY_TIEMS
        testPos = src - VECTOR_ZERO
        testPos.y += 0.01
        srcPos = self.dropFunc(p.spaceID, testPos)
        if srcPos is None:
            srcPos = src
        else:
            srcPos = srcPos[0]
        dstPos = Math.Vector3(dst)
        self.currentDst = dstPos
        self.startPos = srcPos
        gamelog.debug('b.e.@navigator landMove ', srcPos, dstPos, evaldist, ver)
        if not self.pathTraceM.startUpdateLM(self.currentNav, srcPos, dstPos):
            return
        self.doKeepFinding(ver)

    def flyMove(self, points, ver):
        p = BigWorld.player()
        if not p.isPathfinding or ver != self.pathFindingVer:
            return
        self.retryTimes = RETRY_TIEMS
        self.flyPoints = list(points)
        self.currentDst = Math.Vector3(points[-1])
        self.doKeepFinding(ver)

    def pointDistance(self, point, refpoint):
        return distance3D(point, refpoint)

    def doKeepFinding(self, ver):
        p = BigWorld.player()
        p.filter.maxSlideAngle = 1.5325
        if not p.isPathfinding or ver != self.pathFindingVer:
            return
        self.keepPathFinding(ver, 1)

    def wingIsBetter(self):
        p = BigWorld.player()
        equip = p.equipment[gametypes.EQU_PART_WINGFLY]
        if p.inWingWarCity():
            return False
        if equip:
            if p.getWingFlyNormalSpeedForNav() > p.getHorseNormalSpeedForNav():
                if formula.mapLimit(formula.LIMIT_WINGFLY, formula.getMapId(p.spaceNo)):
                    return False
                if p.stateMachine.checkStatus(const.CT_OPEN_WINGFLY_CAST):
                    return True
        return False

    def keepPathFinding(self, ver, status):
        p = BigWorld.player()
        if not p.isPathfinding or ver != self.pathFindingVer:
            return
        gamelog.debug('b.e.@navigator: keepPathFinding', ver, status, p.position, self.lastPos, self.currentDst, self.seekDest, self.disStatus)
        if self.disStatus == True:
            self.disStatus = False
            diff = None
            if self.lastPos is not None:
                diff = p.position - self.lastPos
            if diff is None or diff.length < 0.5:
                self.disStatus = False
                self.runPathFinding(ver)
                return
        if self.onRiding == CAN_RIDE and not p.inSwim and not p.inCombat and not p.inRiding() and not p.inFly:
            if self.wingIsBetter():
                cellCmd.enterWingFly(False)
            elif p.upRiding():
                self.onRiding = HAVE_IN_RIDE
            else:
                self.onRiding = TRY_RIDE_FAIL
        if status in (-1, 1):
            pos = None
            nextPos = [None, None]
            diff = VECTOR_ZERO
            if self.lastPos is not None:
                diff = p.position - self.lastPos
            if diff.length > 0.5 and self.retryTimes and self.lastPos is not None and self.lastPosCache is not None and get_vector_cos(self.lastPosCache, self.lastPos, p.position) < 0:
                pos = self.lastPos
                self.retryTimes -= 1
                self.lastPos = self.lastPosCache
                gamelog.debug('b.e.@navigator keepPathFinding#1', pos, self.retryTimes, self.lastPos)
            else:
                if diff.length > 0.5 and self.retryTimes == 0:
                    gamelog.debug('b.e.@navigator keepPathFinding#2', diff, self.retryTimes, self.lastPos)
                    if self.lastPos:
                        if self.seekDest and (self.seekDest - p.position).length <= self.endDist + 0.5:
                            p.showGameMsg(GMDD.data.ARRIVE_DEST, ())
                            self.onArriveCall()
                        else:
                            self.moveBack(p.position, self.lastPos, ver)
                    else:
                        p.showGameMsg(GMDD.data.PATH_FIND_BLOCK, ())
                        self.onFailedCall()
                    return
                gamelog.debug('b.e.@navigator keepPathFinding#3', diff, self.seekDest, p.position)
                if self.seekDest and (self.seekDest - p.position).length <= self.endDist + 0.5:
                    gamelog.debug('l.b.@navigator keepPathFinding onArriveCall')
                    self.onArriveCall()
                    return
                self.retryTimes = RETRY_TIEMS
                pos = self.getNextPoint()
                if pos is not None and pos != -1 and pos[1] < 0:
                    try:
                        res = BigWorld.findWaterFromPoint(p.spaceID, pos)
                        if res is not None:
                            gamelog.debug('l.b.@navigator inFlyOverWater', pos, res[0])
                            if p.inFly:
                                pos[1] = res[0] + 0.5
                            elif self.seekDest.y > 0:
                                pos[1] = res[0] - 1.5
                    except:
                        pass

                nextPos[0] = self.getSecondNextPoint(1)
                nextPos[1] = self.getSecondNextPoint(2)
                isFailed = self.pathTraceM.isFailed()
                gamelog.debug('l.b.@navigator: keepPathFinding#4.1', isFailed)
                if isFailed:
                    p.showGameMsg(GMDD.data.PATH_FIND_ERROR, ())
                    self.onFailedCall()
                    return
            gamelog.debug('b.e.@navigator: keepPathFinding#4', pos, nextPos, self.lastPos)
            if pos is None:
                if self.pathTraceM.isPartial():
                    gamelog.debug('b.e.@navigator: keepPathFinding#4.2 is partial, insert a moveQueue')
                    self.moveQueue.insert(0, (LANDMOVE, self.seekDest, 1))
                self.runPathFinding(ver)
            else:
                if pos == -1:
                    BigWorld.callback(0.1, Functor(self.keepPathFinding, ver, 1))
                    return
                tVector = pos - self.startPos
                tVector.y = 0
                if not self.currentDst:
                    return
                diff = pos - self.currentDst
                if diff.length <= self.endDist:
                    if self.lastPos:
                        tpos = getPointOnTheCircle(self.lastPos, pos, self.currentDst, self.endDist)
                        if tpos is not None:
                            pos = tpos
                    self.disStatus = True
                if self.lastPos:
                    diff = pos - self.lastPos
                    diff.y = 0
                    if diff.length < 0.5:
                        gamelog.debug('b.e.@navigator: keepPathFinding#5', pos)
                        BigWorld.callback(0.1, Functor(self.keepPathFinding, ver, 1))
                        return
                gamelog.debug('b.e.@navigator: keepPathFinding call moveTo', pos, nextPos)
                if nextPos[0] and pos:
                    if get_vector_cos1(p.position, pos, nextPos[0]) < 0:
                        pos = self.getNextPoint()
                self.moveTo(pos, Functor(self.keepPathFinding, ver))
                if gShowTrace:
                    self.pushDrawPoint(pos, nextPos[0], nextPos[1])
        else:
            self.onFailedCall()

    def runPathFinding(self, ver, status = 0):
        gamelog.debug('b.e.@navigator step5 runPathFinding ', ver, self.moveQueue, self.lastPos)
        p = BigWorld.player()
        if not p.isPathfinding:
            return
        if len(self.moveQueue):
            move = self.moveQueue.pop(0)
            self.upFlyVer += 1
            if move[0] == LANDMOVE:
                self.currentMode = LANDMOVE
                gamelog.debug('l.b@navigator step5.1 runPathFinding call landMove', p.position, move[1], move[2])
                self.landMove(p.position, move[1], move[2], ver)
            elif move[0] == FLYMOVE:
                self.currentMode = FLYMOVE
                gamelog.debug('l.b@navigator step5.1 runPathFinding call flyMove', p.position, move[1])
                self.upToSky(Functor(self.flyMove, move[1], ver), ver, self.upFlyVer)
            elif move[0] == DELAYMOVE:
                self.currentMode = DELAYMOVE
                gamelog.debug('l.b@navigator step5.1 runPathFinding all setDelayPathFinding')
                self.setDelayPathFinding()
                self._stopPathFinding(False)
            else:
                self.onFailedCall()
        elif self.lastPos is None:
            gamelog.debug('l.b.@navigator step5.2 runPathFinding failed')
            p.showGameMsg(GMDD.data.PATH_FIND_ERROR, ())
            self.onFailedCall()
        else:
            tVector = self.seekDest - p.position
            tVector.y = 0
            if tVector.length > 5.0:
                gamelog.debug('l.b.@navigator runPathFinding case 2', self.seekDest, p.position, tVector)
                tVector = p.position - self.startPos
                tVector.y = 0
                if tVector.length < 2.0:
                    p.showGameMsg(GMDD.data.PATH_FIND_ERROR, ())
                else:
                    p.showGameMsg(GMDD.data.PATH_FIND_BLOCK, ())
                gamelog.debug('l.b.@navigator step5.3 runPathFinding failed')
                self.onFailedCall()
            else:
                gamelog.debug('l.b.@navigator step5.3 runPathFinding succ')
                p.showGameMsg(GMDD.data.ARRIVE_DEST, ())
                self.onArriveCall()

    def onFailedCall(self, showMsg = True):
        if self.failedCallback:
            self.failedCallback()
        self.stopPathFinding(showMsg)

    def onArriveCall(self, showMsg = True):
        if self.arriveCallback:
            self.arriveCallback()
        self.stopPathFinding(showMsg)

    def updateSmartPathfinding(self, v):
        global gTeleportSwitch
        gTeleportSwitch = v

    def _stopPathFinding(self, showMsg = True):
        p = BigWorld.player()
        if not p.isPathfinding or self.infly:
            return
        self.pathTraceM.stop_update()
        p.isPathfinding = False
        self.lastPos = None
        self.midPartition = 0
        self.lastDirection = 0
        self.arriveCallback = None
        self.seekDest = None
        self.disStatus = False
        self.pathFindingVer += 1
        self.upFlyVer += 1
        self.currentMode = -1
        self.flyPoints = []
        self.infly = False
        self.currentDst = None
        self.srcLandPorts = []
        self.dstLandPorts = []
        self.srcLandPortDists = {}
        self.dstLandPortDists = {}
        self.srcStoneIndex = None
        self.dstStoneIndex = None
        self.srcStoneDist = None
        self.dstStoneDist = None
        self.srcStonePos = None
        self.dstStonePos = None
        self.testDist = None
        self.calculatePos = {}
        self.teleportDstDist = 0
        self.teleportSrcDist = 0
        if self.resetPathFindingCallBack:
            BigWorld.cancelCallback(self.resetPathFindingCallBack)
            self.resetPathFindingCallBack = None
        gameglobal.rds.cam.cc.isBindToDirCursor = True

    def _realStopPathFinding(self, showMsg = True):
        p = BigWorld.player()
        if not p.isPathfinding or self.infly:
            return
        self._stopPathFinding(showMsg)
        if hasattr(p, 'ap') and hasattr(p.ap, 'physics'):
            p.ap.physics.seek(None, 0, 0, None)
        if hasattr(p, 'ap') and hasattr(p.ap, 'stopMove'):
            p.ap.stopMove()
        if hasattr(p, 'filter') and hasattr(p.filter, 'maxSlideAngle'):
            p.filter.maxSlideAngle = 0.7853975
        self.endShowPoint()
        p.startAutoQuestTimer()
        if showMsg:
            p.showGameMsg(GMDD.data.PATH_FIND_FINISH, ())

    def stopPathFinding(self, showMsg = True):
        global g_firstMove
        global g_moveTime
        if not BigWorld.isPublishedVersion():
            g_moveTime = -1
            g_firstMove = True
        self._realStopPathFinding(showMsg)
        gameglobal.rds.ui.littleMap.hideSeekTarget()
        gameglobal.rds.ui.questTrack.showPathFindingIcon(False)
        gameglobal.rds.ui.huntGhost.setNaviState(False)
        p = BigWorld.player()
        if hasattr(p, '_mousePhysics') and hasattr(p._mousePhysics, 'navigation') and hasattr(p._mousePhysics.navigation, 'stop'):
            p._mousePhysics.navigation.stop()
        if hasattr(p.filter, 'yaw') and self.seekDest:
            p.ap.setYaw((self.seekDest - p.position).yaw)
        if p.getOperationMode() == gameglobal.KEYBOARD_MODE and p.ap._msleft:
            p.ap._key_ml_down(0)
        self.setFakeFly(False)
        p.resetPhysicsModel()
        gameglobal.rds.ui.dispatchEvent(events.EVENT_FINDPOS_STOP)
        if gameglobal.rds.configData.get('enableGroupFollowHeaderPath'):
            p.syncHeaderClientGroundPos()
        self.fromGroupFollow = False

    def setFakeFly(self, enter):
        p = BigWorld.player()
        if not p.inFly:
            return
        if enter:
            p.setGravity(gametypes.WINGFLY_GRAVITY_DOWN, True)
            p.physics.swim(0)
        else:
            p.loseGravity()
            p.physics.swim(1, p.flyHeight)

    def clearOtherNavs(self, saveSpaceNo = const.SPACE_NO_BIG_WORLD):
        p = BigWorld.player()
        phaseSpaceNo = 0
        if p.mapID > 0:
            phaseSpaceNo = getPhaseMappingNum(p.mapID)
        if saveSpaceNo > 0:
            saveSpaceNo = getPhaseMappingNum(saveSpaceNo)
        for spaceNo in self.seekNavs.keys():
            if spaceNo == saveSpaceNo:
                continue
            if spaceNo != phaseSpaceNo:
                self.seekNavs[spaceNo] = None
                del self.seekNavs[spaceNo]

        for spaceNo in self.showNavs.keys():
            if spaceNo == saveSpaceNo:
                continue
            if spaceNo != phaseSpaceNo:
                self.showNavs[spaceNo] = None
                del self.showNavs[spaceNo]

    def downToGround(self, callback, ver):
        p = BigWorld.player()
        if not p.isPathfinding or ver != self.pathFindingVer:
            p.ap.stopMove()
            return
        if p.canFly():
            distanceFromGround = p.qinggongMgr.getDistanceFromGround()
            distanceFromWater = p.qinggongMgr.getDistanceFromWater()
            distance = None
            if distanceFromGround is not None and distanceFromWater is not None:
                distance = min(distanceFromGround, distanceFromWater)
            elif distanceFromGround is not None:
                distance = distanceFromGround
            elif distanceFromWater is not None:
                distance = distanceFromWater
            if self.lastFlyNavGroundDist and abs(distance - self.lastFlyNavGroundDist) < 0.1:
                self.lastFlyNavGroundDist = 0
                p.ap.flyDown(False)
                callback() if callback else None
                return
            self.lastFlyNavGroundDist = distance
            if not self.startDownToGroundTime:
                self.startDownToGroundTime = time.time()
            if time.time() - self.startDownToGroundTime > TOLERATION_DOWNTO_GROUND:
                self.startDownToGroundTime = None
                p.ap.flyDown(False)
                callback() if callback else None
                return
            if distance and distance > FROMGROUNDDIST:
                p.ap.flyDown(True)
                BigWorld.callback(0.1, Functor(self.downToGround, callback, ver))
            else:
                p.ap.flyDown(False)
                callback() if callback else None
        else:
            callback() if callback else None

    def downToGround2(self, callback, ver):
        p = BigWorld.player()
        if ver != self.pathFindingVer:
            p.ap.stopMove()
            return
        if p.canFly():
            distanceFromGround = p.qinggongMgr.getDistanceFromGround()
            distanceFromWater = p.qinggongMgr.getDistanceFromWater()
            distance = None
            if distanceFromGround is not None and distanceFromWater is not None:
                distance = min(distanceFromGround, distanceFromWater)
            elif distanceFromGround is not None:
                distance = distanceFromGround
            elif distanceFromWater is not None:
                distance = distanceFromWater
            if self.lastFlyNavGroundDist and abs(distance - self.lastFlyNavGroundDist) < 0.1:
                self.lastFlyNavGroundDist = 0
                p.ap.flyDown(False)
                callback() if callback else None
                return
            self.lastFlyNavGroundDist = distance
            if not self.startDownToGroundTime:
                self.startDownToGroundTime = time.time()
            if time.time() - self.startDownToGroundTime > TOLERATION_DOWNTO_GROUND:
                self.startDownToGroundTime = None
                p.ap.flyDown(False)
                callback() if callback else None
                return
            if distance and distance > FROMGROUNDDIST:
                p.ap.flyDown(True)
                BigWorld.callback(0.1, Functor(self.downToGround2, callback, ver))
            else:
                p.ap.flyDown(False)
                callback() if callback else None
        else:
            callback() if callback else None

    def setInfly(self, infly):
        self.infly = infly

    def upToSky(self, callback, ver, upflyver):
        p = BigWorld.player()
        if not p.isPathfinding or ver != self.pathFindingVer or upflyver != self.upFlyVer:
            self.infly = False
            self.upFlyVer += 1
            return
        BigWorld.callback(0.5, Functor(self.setInfly, False))
        if callback:
            callback()
        BigWorld.callback(1.0, Functor(self.upToSky, None, ver, upflyver))

    def getMove(self, seekDest, ver, parent = None, failedCallback = None, showMsg = True, endDist = 1.5, arriveCallback = None, evalDist = -1):
        gamelog.debug('b.e.@navigator step4 getMove', seekDest, ver, parent, showMsg, evalDist)
        if ver != self.pathFindingVer:
            return
        p = BigWorld.player()
        if (seekDest - p.position).length >= DIRECT_RIDEDIST or evalDist >= EVAL_RIDEDIST:
            self.onRiding = CAN_RIDE
        self.seekDest = seekDest
        gamelog.debug('l.b.@navigator step4.2 getMove direct land move %.2f' % evalDist)
        self.moveQueue = [(LANDMOVE, seekDest, evalDist)]
        self.parent = parent
        self.failedCallback = failedCallback
        self.arriveCallback = arriveCallback
        self.endDist = endDist
        self.runPathFinding(ver)

    def canEnterRideFly(self):
        p = BigWorld.player()
        if p.bianshen and p._isOnZaiju():
            flyZaiju = ZJD.data.get(p.bianshen[1], {}).get('flyZaiju', 0)
            if flyZaiju:
                return True
        return False

    def testConnection(self, res, seekDest, ver, parent = None, failedCallback = None, showMsg = True, endDist = 1.5, arriveCallback = None, firstCall = True):
        gamelog.debug('b.e.@navigator step2 testConnection', res, seekDest, ver, parent, showMsg, firstCall and gCanTeleport and gTeleportSwitch, self.pathFindingVer)
        if ver != self.pathFindingVer:
            return
        p = BigWorld.player()
        if not p or not p.inWorld:
            return
        if gCanFly and self.canEnterRideFly():
            self.tryFly(seekDest, ver, seekDest, parent, failedCallback, showMsg, endDist, arriveCallback)
        elif firstCall and gCanTeleport and gTeleportSwitch:
            pos = seekDest
            self.testDist = res[0]
            flag = p.isPathfinding
            p.isPathfinding = False
            self.seekDest = None
            spaceNo = getPhaseMappingNum(p.mapID)
            gamelog.debug('l.b.@navigator step3 check land mark & stone, testConnection, call pathFindingTeleport')
            self.pathFindingTeleport(res[0], (pos.x,
             pos.y,
             pos.z,
             spaceNo), parent, failedCallback, showMsg, endDist, arriveCallback, self.onRiding)
            p.isPathfinding = flag
        elif self.useLadderOnce:
            spaceNo = getPhaseMappingNum(p.mapID)
            gamelog.debug('l.b.@navigator testConnection, call pathFindingLadder')
            self.pathFindingLadder(res[0], (seekDest[0],
             seekDest[1],
             seekDest[2],
             spaceNo), parent, failedCallback, showMsg, endDist, arriveCallback, self.onRiding)
            self.useLadderOnce = False
        else:
            gamelog.debug('l.b.@navigator step4 begin move, testConnection, call getMove')
            self.getMove(seekDest, ver, parent, failedCallback, showMsg, endDist, arriveCallback, evalDist=res[0])

    def pathFinding(self, seekPoint, parent = None, failedCallback = None, showMsg = True, endDist = 1.5, arriveCallback = None, onRiding = None, firstCall = True, forceFixLandMove = False, fromGroupFollow = False, resetNavigator = False):
        self.failedCallback = None
        if resetNavigator:
            self.stopPathFinding(False)
            self.resetPathFindingCallBack = BigWorld.callback(0.2, Functor(self.pathFinding, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback, onRiding, firstCall, forceFixLandMove, fromGroupFollow, False))
            return
        if self.resetPathFindingCallBack:
            BigWorld.cancelCallback(self.resetPathFindingCallBack)
            self.resetPathFindingCallBack = None
        self.lastPathFindingArgs = (self.pathFinding, (seekPoint,
          parent,
          failedCallback,
          showMsg,
          endDist,
          arriveCallback,
          onRiding,
          firstCall,
          forceFixLandMove,
          fromGroupFollow))
        p = BigWorld.player()
        tDest = Math.Vector3(seekPoint[0], seekPoint[1], seekPoint[2])
        if p.inGroupFollow and p.isPathfinding and self.seekDest and tDest and self.seekDest[0] == tDest[0] and self.seekDest[2] == tDest[2]:
            return
        if p.inGroupFollow and not fromGroupFollow:
            if not p.checkTempGroupFollow(False):
                return
        self.fromGroupFollow = fromGroupFollow
        self._pathFinding(seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback, onRiding, firstCall, forceFixLandMove)

    def _pathFinding(self, seekPoint, parent = None, failedCallback = None, showMsg = True, endDist = 1.5, arriveCallback = None, onRiding = None, firstCall = True, forceFixLandMove = False):
        p = BigWorld.player()
        if firstCall and self.currentNav and hasattr(self.currentNav, 'setExtentY'):
            if seekPoint[1] == UNKNOWN_Y:
                seekPoint = (seekPoint[0],
                 EXTENT_POSY,
                 seekPoint[2],
                 seekPoint[3])
                self.currentNav.setExtentY(EXTENT_Y)
            else:
                self.currentNav.setExtentY(EXTENT_NORMALY)
        p.ap.breakDashStopAction()
        if p.inFly and p.stateMachine.checkStatus(const.CT_AUTO_PATHFINDING):
            self.startDownToGroundTime = None
            gamelog.debug('l.b.@navigator _pathFinding begin call downToGround', self.startDownToGroundTime)
            self.downToGround2(Functor(self.pathFindingInner, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback, onRiding, firstCall, forceFixLandMove), self.pathFindingVer)
        else:
            self.pathFindingInner(seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback, onRiding, firstCall, forceFixLandMove)

    def pathFindingInner(self, seekPoint, parent = None, failedCallback = None, showMsg = True, endDist = 1.5, arriveCallback = None, onRiding = None, firstCall = True, forceFixLandMove = False):
        global gCanLadder
        global g_moveTime
        gamelog.debug('b.e.@navigator-------------------------------------------')
        gamelog.debug('b.e.@navigator _pathFinding', self.inDelayPathFinding(), self.seekDest, seekPoint, parent, showMsg, firstCall, forceFixLandMove, endDist)
        if not BigWorld.isPublishedVersion():
            import keys
            if BigWorld.isKeyDown(keys.KEY_LSHIFT) or BigWorld.isKeyDown(keys.KEY_RSHIFT):
                pos = (seekPoint[0], seekPoint[1], seekPoint[2])
                spaceNo = seekPoint[3]
                if gameglobal.rds.isSinglePlayer:
                    BigWorld.player().physics.teleport(pos)
                return
            if g_moveTime < 0:
                g_moveTime = time.time()
        p = BigWorld.player()
        gameglobal.rds.ui.map.setSeekPos(seekPoint)
        if firstCall and gCanLadder:
            self.useLadderOnce = True
        tDest = Math.Vector3(seekPoint[0], seekPoint[1], seekPoint[2])
        gamelog.debug('b.e.@navigator _pathFinding ->', self.inDelayPathFinding(), self.seekDest, tDest)
        if self.inDelayPathFinding():
            gamelog.debug('l.b.@navigator, _pathFinding, delayPathFinding')
            return SEEKING
        if p.isPathfinding and self.seekDest == tDest:
            gamelog.debug('l.b.@navigator, _pathFinding, sameDestination')
            p.showGameMsg(GMDD.data.IN_WAY_TO_DEST, ())
            return SEEKING
        if p.stateMachine.checkStatus(const.CT_AUTO_PATHFINDING):
            if firstCall:
                self._clearDistThreadCache()
            self.forceFixLandMove = forceFixLandMove
            spaceNo = seekPoint[3]
            if isPassingPhase(spaceNo, p.mapID):
                digongStonePos = getNearestDiGongStone(formula.getMapId(spaceNo))
                if not (getattr(p, 'guildNUID', 0) and spaceNo == const.GUILD_SCENE_NO and p.mapID == const.SPACE_NO_BIG_WORLD or p.inGuildSpace() and spaceNo == const.SPACE_NO_BIG_WORLD):
                    p.showGameMsg(GMDD.data.NO_TELEPORT_IN_DEST_EX, (formula.whatSpaceName(p.spaceNo, False), formula.whatSpaceName(seekPoint[-1], False)))
                    return FAILED
                if not digongStonePos and formula.getMapId(spaceNo) != const.SPACE_NO_BIG_WORLD:
                    p.showGameMsg(GMDD.data.NO_TELEPORT_IN_DEST_EX, (formula.whatSpaceName(p.spaceNo, False), formula.whatSpaceName(seekPoint[-1], False)))
                    return FAILED
            if isSameSpaceInPhaseMapping(spaceNo, p.mapID):
                if canScenePathfinding():
                    self.seekDest = tDest
                    self.endDist = endDist
                    if onRiding is None:
                        self.onRiding = HAVE_IN_RIDE if p.inRiding() else None
                    else:
                        self.onRiding = onRiding
                    if (self.seekDest - p.position).length <= self.endDist + 0.5:
                        if showMsg:
                            p.showGameMsg(GMDD.data.BEGIN_PATH_FIND, ())
                            p.showGameMsg(GMDD.data.ARRIVE_DEST, ())
                        p.isPathfinding = True
                        self.arriveCallback = arriveCallback
                        self.onArriveCall(showMsg)
                        return ARRIVED
                    else:
                        srcPos = BigWorld.player().position
                        spaceNo = getPhaseMappingNum(p.mapID)
                        self.currentNav = self.seekNavs.get(spaceNo, None)
                        if not self.currentNav:
                            self.currentNav = self.seekNavs.get(p.mapID, None)
                            if not self.currentNav:
                                return FAILED
                        if p.isPathfinding:
                            self._stopPathFinding(showMsg)
                        if showMsg:
                            p.showGameMsg(GMDD.data.BEGIN_PATH_FIND, ())
                        self.setFakeFly(True)
                        p.resetPhysicsModel()
                        p.isPathfinding = True
                        p.ap.resetCameraAndDcursorRotate()
                        if firstCall and gameglobal.rds.configData.get('enableGroupFollowHeaderPath'):
                            p.syncHeaderClientGroundPos(seekPoint[0], seekPoint[1], seekPoint[2], seekPoint[3])
                        res = [-1, -1]
                        self.pathFindingVer += 1
                        gamelog.debug('l.b.@navigator: pathfinding, step1 evaldist:', seekPoint[0], seekPoint[1], seekPoint[2], srcPos.x, srcPos.y, srcPos.z)
                        res = self._evaluateDistThreadCache(seekPoint[0], seekPoint[1], seekPoint[2], srcPos.x, srcPos.y, srcPos.z, res, 0, Functor(self.testConnection, res, tDest, self.pathFindingVer, parent, failedCallback, showMsg, endDist, arriveCallback, firstCall), 0)
                        if res is None:
                            p.showGameMsg(GMDD.data.PLEASE_WAIT, ())
                            self._stopPathFinding(showMsg)
                            return FAILED
                        gameglobal.rds.ui.huntGhost.setNaviState(True)
                        return SUCCESS
                else:
                    if showMsg:
                        p.showGameMsg(GMDD.data.CAN_NOT_PATH_FIND_IN_CUR_SCENE, ())
                    return FAILED
            else:
                gamelog.debug('b.e.@navigator _pathFinding, xxxx', gCanTeleport, firstCall)
                if not gCanTeleport or not firstCall:
                    p.showGameMsg(GMDD.data.NO_TELEPORT_IN_DEST_EX, (formula.whatSpaceName(p.spaceNo, False), formula.whatSpaceName(seekPoint[-1], False)))
                    self.stopPathFinding(False)
                    return FAILED
                else:
                    if showMsg:
                        p.showGameMsg(GMDD.data.BEGIN_PATH_FIND, ())
                    gamelog.debug('b.e.@navigator _pathFinding, xxxx2', gCanTeleport, firstCall)
                    spaceNo = formula.getMapId(seekPoint[3])
                    digongStonePos = getNearestDiGongStone(spaceNo)
                    if gameglobal.rds.configData.get('enableCrossDiGongNavigator', True):
                        mlData = MDD.data.get(formula.getMLGNo(p.spaceNo), {})
                        canLeave = mlData.get('canLeave', True)
                        mlgNo = formula.getMLGNo(p.spaceNo)
                        if spaceNo == const.SPACE_NO_BIG_WORLD:
                            if canLeave and formula.inMultiLine(mlgNo) and not formula.isCrossServerML(mlgNo):
                                p.cell.exitLine()
                                p.isPathfinding = True
                                self.seekDest = Math.Vector3(seekPoint[:3])
                                if self.canSetDelay():
                                    self.setDelayPathFinding(1)
                                    self.delayData['seekPoint'] = seekPoint
                                    self.delayData['parent'] = parent
                                    self.delayData['failedCallback'] = failedCallback
                                    self.delayData['arriveCallback'] = arriveCallback
                                    self.delayData['endDist'] = endDist
                                    self.delayData['onRiding'] = onRiding
                                    self.delayData['forceFixLandMove'] = forceFixLandMove
                                    self.delayData['firstCall'] = True
                                    p.isPathfinding = False
                                return SUCCESS
                            if p.inGuildSpace():
                                p.cell.exitGuildScene()
                                p.isPathfinding = True
                                self.seekDest = Math.Vector3(seekPoint[:3])
                                if self.canSetDelay():
                                    self.setDelayPathFinding(1)
                                    self.delayData['seekPoint'] = seekPoint
                                    self.delayData['parent'] = parent
                                    self.delayData['failedCallback'] = failedCallback
                                    self.delayData['arriveCallback'] = arriveCallback
                                    self.delayData['endDist'] = endDist
                                    self.delayData['onRiding'] = onRiding
                                    self.delayData['forceFixLandMove'] = forceFixLandMove
                                    self.delayData['firstCall'] = True
                                    p.isPathfinding = False
                                return SUCCESS
                        if spaceNo == const.GUILD_SCENE_NO and getattr(p, 'guildNUID', 0) and p.mapID == const.SPACE_NO_BIG_WORLD:
                            from guis import uiUtils
                            trackId = uiUtils.findTrackId(GCD.data.get('GuildEnterNpc', (11015272,)))
                            sd = SD.data.get(trackId, {})
                            guildEnterPos = (sd['xpos'],
                             sd['ypos'],
                             sd['zpos'],
                             sd['spaceNo'])
                            newArriveCallback = Functor(self.pathfindingGuildArriveCallback, seekPoint, arriveCallback)
                            return self.pathFindingInner(guildEnterPos, parent, failedCallback, showMsg, 0, newArriveCallback, onRiding)
                        if digongStonePos:
                            newArriveCallback = Functor(self.pathfindingDiGongArriveCallback, seekPoint, arriveCallback)
                            return self.pathFindingInner(digongStonePos, parent, failedCallback, showMsg, endDist, newArriveCallback, onRiding)
                    return self.pathFindingTeleport(-1, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback, onRiding)
        else:
            self.onFailedCall()
            return FAILED

    def pathfindingDiGongArriveCallback(self, seekPoint, arriveCallback):
        BigWorld.callback(1, Functor(self._pathfindingDiGongArriveCallback, seekPoint, arriveCallback))

    def _pathfindingDiGongArriveCallback(self, seekPoint, arriveCallback):
        if gameglobal.rds.ui.diGong.isShow:
            gameglobal.rds.ui.diGong._onEnterLine()
            p = BigWorld.player()
            p.isPathfinding = True
            self.seekDest = Math.Vector3(seekPoint[:3])
            if self.canSetDelay():
                self.setDelayPathFinding(1)
                self.delayData['seekPoint'] = seekPoint
                self.delayData['arriveCallback'] = arriveCallback
                p.isPathfinding = False

    def pathfindingGuildArriveCallback(self, seekPoint, arriveCallback):
        BigWorld.callback(1, Functor(self._pathfindingGuildArriveCallback, seekPoint, arriveCallback))

    def _pathfindingGuildArriveCallback(self, seekPoint, arriveCallback):
        npc = gameglobal.rds.ui.pressKeyF.getTalkNpc()
        if npc:
            npc.cell.enterGuildScene()
            p = BigWorld.player()
            p.isPathfinding = True
            self.seekDest = Math.Vector3(seekPoint[:3])
            if self.canSetDelay():
                self.setDelayPathFinding(1)
                self.delayData['seekPoint'] = seekPoint
                self.delayData['arriveCallback'] = arriveCallback
                p.isPathfinding = False

    def doGetPosNearBy(self, src, res, index, ver, parent, failedCallback, showMsg, endDist, arriveCallback):
        gamelog.debug('jjh@navigator doGetPosNearBy')
        p = BigWorld.player()
        if not p.isPathfinding or ver != self.pathFindingVer:
            return
        if not self.evalPosList:
            return
        if index >= len(self.evalPosList) or len(self.evalPosList) == 1:
            if res[1] != -1:
                BigWorld.callback(0.1, Functor(self._pathFinding, self.evalPosList[res[1]], parent, failedCallback, showMsg, endDist, arriveCallback, False))
            elif len(self.evalPosList) == 1:
                BigWorld.callback(0.1, Functor(self._pathFinding, self.evalPosList[0], parent, failedCallback, showMsg, endDist, arriveCallback, False))
            else:
                p.showGameMsg(GMDD.data.CAN_NOT_FIND_CLOSEST_POS, ())
            self.onFailedCall(showMsg=False)
            return
        pos = self.evalPosList[index]
        BigWorld.callback(0, Functor(self.currentNav.evaluateDistThread, src.x, src.y, src.z, pos[0], pos[1], pos[2], res, index, Functor(self.doGetPosNearBy, src, res, index + 1, ver, parent, failedCallback, showMsg, endDist, arriveCallback), 0))

    def dropPoint(self, p, yaw = 0, effid = 2427, scale = 2.0):
        if len(self.showPoints) > 30:
            model = self.showPoints.pop(0)
            model.stop()
        else:
            model = sfx.Navigation(effid)
        model.model.yaw = yaw
        model.fx.scale(2.5)
        model.start(p, False)
        self.showPoints.append(model)

    def delDropPoints(self):
        for model in self.showPoints:
            model.stop()

    def getNextPoint(self):
        if len(self.flyPoints):
            return Math.Vector3(self.flyPoints.pop(0))
        return self.pathTraceM.getNextPos()

    def getSecondNextPoint(self, index):
        return self.pathTraceM.getNextNdPos(index)

    def doGetAriPortNearBy(self, pos, port, res, key, callback = None):
        if not self.tryFlyFlag:
            return
        port = Math.Vector3(port)
        dis = (pos - port).length
        if res[0] < 0 or res[0] > dis:
            res[0] = dis
            res[1] = key
        callback and callback()

    def getAirportNearby(self, pos, res, idx, ver, callback = None):
        if ver != self.pathFindingVer:
            return
        if not self.tryFlyFlag:
            return
        if idx >= len(self.pointNums):
            if callback:
                BigWorld.callback(0.2, callback)
            return
        k = self.pointNums[idx]
        v = self.fpdata['ports'][k]
        self.doGetAriPortNearBy(pos, v, res, k, Functor(self.getAirportNearby, pos, res, idx + 1, ver, callback))

    def testFly(self, srcPort, dstPort, ver, seekDest, parent, failedCallback, showMsg, endDist, arriveCallback):
        if ver != self.pathFindingVer:
            self.tryFlyFlag = False
            return
        if not self.tryFlyFlag:
            self.tryFlyFlag = False
            return
        p = BigWorld.player()
        gamelog.debug('bgf@navigator testFly', srcPort, dstPort)
        if srcPort[1] != -1 and dstPort[1] != -1 and (srcPort[0] <= FLYDIST or p.position.distTo(Math.Vector3(self.fpdata['ports'][srcPort[1]])) <= FLYDIST):
            p.showGameMsg(GMDD.data.CAN_FLY_ARRIVE, ())
            if self.getAirline(srcPort[1], dstPort[1]):
                tmovequeue = [(LANDMOVE, self.fpdata['ports'][srcPort[1]], srcPort[0]), (FLYMOVE, self.resline, 0), (LANDMOVE, (seekDest.x, seekDest.y, seekDest.z), srcPort[0])]
                self.moveQueue = tmovequeue
                self.seekDest = seekDest
                self.parent = parent
                self.failedCallback = failedCallback
                self.arriveCallback = arriveCallback
                self.endDist = endDist
                self.runPathFinding(ver)
            else:
                p.showGameMsg(GMDD.data.CAN_NOT_FLY_ARRIVE, ())
                self.getMove(seekDest, ver, parent, failedCallback, showMsg, endDist, arriveCallback)
        else:
            p.showGameMsg(GMDD.data.CAN_NOT_FLY_ARRIVE, ())
            self.getMove(seekDest, ver, parent, failedCallback, showMsg, endDist, arriveCallback)
        self.tryFlyFlag = False

    def tryFly(self, seekPoint, ver, seekDest, parent, failedCallback, showMsg, endDist, arriveCallback):
        gamelog.debug('bgf@navigator tryFly', self.tryFlyFlag)
        if ver != self.pathFindingVer:
            return
        self.tryFlyFlag = True
        p = BigWorld.player()
        if showMsg:
            p.showGameMsg(GMDD.data.TRY_FLY_PATH_FIND, ())
        p = BigWorld.player()
        FPD = getFlyPointDataM()
        spaceNo = getPhaseMappingNum(p.mapID)
        if FPD is None or not FPD.data.has_key(spaceNo):
            p.showGameMsg(GMDD.data.NO_FLY_POINT_DATA, ())
            return
        self.pointNums = [ x for x in list(FPD.data[spaceNo]['ports'].keys()) if x not in FPD.data[spaceNo].get('exclude_ports', []) ]
        self.fpdata = FPD.data[spaceNo]
        self.resline = []
        srcPort = [-1.0, -1]
        dstPort = [-1.0, -1]
        self.getAirportNearby(p.position, srcPort, 0, ver, Functor(self.getAirportNearby, seekPoint, dstPort, 0, ver, Functor(self.testFly, srcPort, dstPort, ver, seekDest, parent, failedCallback, showMsg, endDist, arriveCallback)))

    def getAirline(self, srcport, dstport):
        key = (min(srcport, dstport), max(srcport, dstport))
        path = self.fpdata['paths'].get(key, None)
        if path is None:
            return False
        path = list(path)
        if srcport == path[-1]:
            path.reverse()
        last = None
        cur = None
        self.resline = []
        for i in path:
            cur = i
            if last:
                key = (min(last, cur), max(last, cur))
                airline = self.fpdata['airlines'].get(key, None)
                if airline is None:
                    return False
                airline = list(airline)
                if self.fpdata['ports'][last] == airline[-1]:
                    airline.reverse()
                self.resline += airline[:-1]
            last = i

        self.resline.append(self.fpdata['ports'][last])
        return True

    def moveBack(self, p1, p2, ver):
        self.forceFixLandMove = True
        if self.tooCloseToLast(BigWorld.player().position):
            self.midPartition -= self.lastDirection
        if self.midPartition > 5:
            self.midPartition = 5
        elif self.midPartition < -5:
            self.midPartition = -5
        backpos = getPointOnTheCircle(p1, p2, p1, 0.5)
        d = random.randint(self.midPartition - 3, self.midPartition + 3)
        self.lastDirection = 0
        if d > 0:
            self.lastDirection = 1
        if d < 0:
            self.lastDirection = -1
        mv = getVectorsByAngle(p1, backpos, MOVEBACKDIST, d * math.pi / 16)
        pos = mv + p1
        self.currentMode = DELAYMOVE
        move = (self.currentMode, self.currentDst, 0)
        self.moveQueue = [move] + self.moveQueue
        self.moveTo(pos, Functor(self.runPathFinding, ver))

    def moveTo(self, point, callback):
        global g_firstMove
        p = BigWorld.player()
        if not BigWorld.isPublishedVersion():
            if g_firstMove:
                gamelog.debug('lb@navigator, movetime:', time.time() - g_moveTime, p.position, point)
                g_firstMove = False
        p._mousePhysics.navigation.stop()
        if not gIsPublished:
            p._mousePhysics.navigation.start(point, False)
        self.lastPosCache = self.lastPos
        self.lastPos = point
        pos = Math.Vector3(point[0], point[1], point[2])
        p.isPathfinding = False
        self.ignorPflag = True
        p.ap.seekPath(pos, callback)
        gameglobal.rds.cam.cc.isBindToDirCursor = False
        p.isPathfinding = True
        self.ignorPflag = False
        if not p.isDashing:
            mep = p.mep
            reStartDashEpValue = SCD.data.get('reStartDashEpValue', 0.5)
            if p.qinggongMgr.checkCanQingGongPathFinding() and p.ep * 1.0 / mep > reStartDashEpValue and gameglobal.rds.configData.get('enableQingGongPathFinding', False) and not p.isGroupSyncSpeed() and appSetting.Obj.get(keys.SET_QINGGONG_PATHFINDING, 1):
                if p.inFlyTypeWing():
                    qingGong.enterWingFlyDash(qingGong.GO_WINGFLY_DASH, p.qinggongMgr, shieldPathFinding=True)
                else:
                    qingGong.switchToDash(p, shieldPathFinding=True)
        p.ap.updateVelocity()
        self.nepActionRoleMoveTo(point)

    def getToGround(self, point, spaceID):
        fpoint = point - VECTOR_ZERO
        tpoint = point - VECTOR_ZERO
        fpoint.y = point.y + 5
        tpoint.y = point.y - 5
        res = self.collideFunc(spaceID, fpoint, tpoint)
        if res is None:
            return point
        else:
            return res[0]

    def tooCloseToLast(self, pos):
        tVector = pos - self.startPos
        tVector.y = 0
        return tVector.length < 5.0

    def initShowPoint(self):
        self.showPoints = []
        self.onShowTrace = False
        self.preShowPoint = []
        self.readyToDrawPoints = []

    def endShowPoint(self):
        self.delDropPoints()
        self.lastShowPos = None
        self.onShowTrace = False
        self.readyToDrawPoints = []

    def pushDrawPoint(self, pos, nextPos, nextNdPos):
        pos = Math.Vector3(pos)
        nextPos = nextPos != None and Math.Vector3(nextPos) or None
        nextNdPos = nextNdPos != None and Math.Vector3(nextNdPos) or None
        if nextPos and (nextPos - pos).length < 0.5:
            nextPos = None
        if nextNdPos and nextPos and (nextNdPos - nextPos).length < 0.5:
            nextNdPos = None
        curShowPoint = [pos, nextPos, nextNdPos]
        for point in curShowPoint:
            if point and point not in self.preShowPoint:
                self.readyToDrawPoints.append(point)

        self.preShowPoint = curShowPoint
        gamelog.debug('pushDrawPoint', pos, nextPos, nextNdPos)
        if not self.onShowTrace:
            self.onShowTrace = True
            self.beginDrawTrace()

    def beginDrawTrace(self):
        p = BigWorld.player()
        if not p.isPathfinding or len(self.readyToDrawPoints) == 0:
            self.onShowTrace = False
            return
        if len(self.readyToDrawPoints):
            pos = self.readyToDrawPoints.pop(0)
            self.drawTrace(pos)

    def drawTrace(self, pos):
        p = BigWorld.player()
        if not self.lastShowPos:
            self.lastShowPos = p.position
        dir = pos - self.lastShowPos
        yaw = dir.yaw
        len = dir.length
        dir.normalise()
        inteval = 3.0
        intevalDir = inteval * dir
        num = int(len / inteval)
        self._drawTrace(self.lastShowPos, yaw, intevalDir, 1, num)

    def _drawTrace(self, pos, yaw, dir, index, num):
        p = BigWorld.player()
        if not p.isPathfinding or not self.onShowTrace:
            return
        tpos = pos + index * dir
        srcPos = tpos
        srcPos[1] += 3
        srcPos = self.dropFunc(p.spaceID, srcPos)
        if srcPos:
            tpos = srcPos[0]
        gamelog.debug('_drawTrace', tpos, pos, index, num, dir)
        self.dropPoint(tpos, yaw)
        timeInteval = 0.15
        if index == num or num <= 1:
            self.lastShowPos = tpos
            BigWorld.callback(timeInteval, self.beginDrawTrace)
            return
        BigWorld.callback(timeInteval, Functor(self._drawTrace, pos, yaw, dir, index + 1, num))

    def _getNearByPointThread(self, srcX, srcY, srcZ, extentX, extentY, extentZ, res, callback):
        return self.currentNav.getNearPosThread(srcX, srcY, srcZ, extentX, extentY, extentZ, res, Functor(self._getNearPosThreadCallback, res, callback))

    def _getNearPosThreadCallback(self, res, callback):
        gamelog.debug('l.b.@fangkadian', res, callback)
        if callback:
            if res[0] < 0:
                callback(-2, 0, None)
            else:
                callback(1, res[0], res[1:])

    def getNearbyPoint(self, pos, spaceNo, callback, extent = (50.0, 200.0, 50.0), isTelport = False):
        p = BigWorld.player()
        if p.isPathfinding:
            callback(-2, 0, None)
            return
        spaceNo = getPhaseMappingNum(spaceNo)
        self.currentNav = self.seekNavs.get(spaceNo, None)
        if not self.currentNav:
            callback(-2, 0, None)
            return
        if not isTelport:
            qt = self.qts.get(spaceNo, None)
            points = qt and qt.getAroundPoints((pos.x, pos.y, pos.z)) or []
            if points:
                points.sort(lambda x, y: cmp(self.pointDistance(x, pos), self.pointDistance(y, pos)))
                if spaceNo in [const.SPACE_NO_WORLD_WAR]:
                    nearestPoint = random.choice(points)
                else:
                    nearestPoint = points[0]
                dist = distance2D(nearestPoint, pos)
                callback(nearestPoint.num, dist, (nearestPoint.x, nearestPoint.y, nearestPoint.z))
            else:
                callback(-2, 0, None)
        else:
            res = [-1,
             -1,
             -1,
             -1]
            self._getNearByPointThread(pos.x, pos.y, pos.z, extent[0], extent[1], extent[2], res, callback)

    def getRandomPos(self, pos, radius):
        p = BigWorld.player()
        if p is None:
            return
        spaceNo = getPhaseMappingNum(p.mapID)
        self.currentNav = self.seekNavs.get(spaceNo, None)
        if self.currentNav is None:
            gamelog.debug('l.b.@navigator getRandomPos, currentNav is None', spaceNo)
            return
        return self.currentNav.getRandomPos(pos.x, pos.y, pos.z, radius)

    def pathFindingLadder(self, evaldist, seekPoint, parent = None, failedCallback = None, showMsg = True, endDist = 1.5, arriveCallback = None, onRiding = None):
        gamelog.debug('b.e.@navigator pathFindingLadder', evaldist, seekPoint, parent, showMsg)
        p = BigWorld.player()
        if p.stateMachine.checkStatus(const.CT_AUTO_PATHFINDING):
            if canScenePathfinding():
                if p.isPathfinding:
                    self._stopPathFinding(showMsg)
                res = [-1, -1]
                self.pathFindingVer += 1
                stoneInfo = getLadderInfo(getPhaseMappingNum(seekPoint[-1])).items()
                if len(stoneInfo) == 0:
                    if isSameSpaceInPhaseMapping(p.mapID, seekPoint[-1]):
                        self._stopPathFinding(False)
                        BigWorld.callback(0, Functor(self._pathFinding, seekPoint, parent, failedCallback, False, endDist, arriveCallback, onRiding, False))
                        return SUCCESS
                    p.showGameMsg(GMDD.data.NO_TELEPORT_IN_DEST, ())
                    return FAILED
                stoneInfo.sort(cmp=lambda x, y: cmpDist(x[1], y[1], Math.Vector3(*seekPoint[:3])))
                stoneInfo = stoneInfo[:LADDER_NUM]
                pos_list = []
                id_list = []
                for id, pos in stoneInfo:
                    id_list.append(id)
                    pos_list.append(pos)

                self.evalPosList = pos_list
                self.evalIdList = id_list
                self.currentNav = self.seekNavs.get(getPhaseMappingNum(seekPoint[-1]), None)
                gamelog.debug('b.e.@navigator pathFindingLadder#1', pos_list, id_list)
                if not self.currentNav:
                    self.currentNav = self.seekNavs.get(getPhaseMappingNum(seekPoint[-1]), None)
                    if not self.currentNav:
                        if not showMsg:
                            self.onFailedCall()
                            return FAILED
                        p.isPathfinding = True
                        self.InitSeekNavsBySpaceNo(getPhaseMappingNum(seekPoint[-1]), False, Functor(self.pathFindingTeleport, evaldist, seekPoint, parent, failedCallback, False, endDist, arriveCallback, onRiding))
                        self.clearOtherNavs(getPhaseMappingNum(seekPoint[-1]))
                        return SUCCESS
                p.isPathfinding = True
                self.findClosestPos(Math.Vector3(*seekPoint[:3]), res, 0, self.pathFindingVer, self.pathfindingLadderCallback, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback)
                return SUCCESS
            else:
                if showMsg:
                    p.showGameMsg(GMDD.data.CAN_NOT_PATH_FIND_IN_CUR_SCENE, ())
                return FAILED
        else:
            p.showGameMsg(GMDD.data.CAN_NOT_AUTO_PATH_FIND, ())
            self.onFailedCall()
            return FAILED

    def pathfindingLadderCallback(self, res, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback):
        gamelog.debug('b.e.@navigator pathfindingLadderCallback', res, seekPoint, parent, showMsg)
        p = BigWorld.player()
        dist, index = res[:2]
        for k, v in self.calculatePos.iteritems():
            if v[0] != -1 and dist > v[0]:
                dist = v[0]
                index = k

        self.teleportDstDist = dist
        if self.evalIdList and index < len(self.evalIdList):
            self.dstStoneIndex = self.evalIdList[index]
            self.dstStonePos = self.evalPosList[index]
            self.dstStoneDist = dist
            gamelog.debug('b.e.@navigator pathfindingLadderCallback#1', self.dstStoneIndex, self.dstStonePos, self.dstStoneDist)
            spaceNo = getPhaseMappingNum(p.mapID)
            idx = self.getOtherPort(self.dstStoneIndex)
            stoneInfo = [(idx, ladderInfo[spaceNo][idx])]
            gamelog.debug('b.e.@navigator pathfindingLadderCallback#2', stoneInfo)
            pos_list = []
            id_list = []
            for id, pos in stoneInfo:
                id_list.append(id)
                pos_list.append(pos)

            self.evalPosList = pos_list
            self.evalIdList = id_list
            self.currentNav = self.seekNavs.get(spaceNo, None)
            if not self.currentNav:
                self.currentNav = self.seekNavs.get(getPhaseMappingNum(seekPoint[-1]), None)
                if not self.currentNav:
                    self.stopPathFinding()
                    return
            p.isPathfinding = True
            res = [-1, -1]
            self.pathFindingVer += 1
            currentPosition = p.position
            if p.canFly():
                tPos = self.getDropPoint((p.position[0],
                 UNKNOWN_Y,
                 p.position[2],
                 p.mapID))
                if tPos[1] != UNKNOWN_Y:
                    currentPosition = Math.Vector3(tPos[:3])
            self.findClosestPos(currentPosition, res, 0, self.pathFindingVer, self.pathfindingLadderCallback2, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback)
        else:
            p.showGameMsg(GMDD.data.PATH_FIND_ERROR, ())
            self.stopPathFinding()

    def pathfindingLadderCallback2(self, res, seekPoint, parent, failedCallback, showMsg, endDist, arriveCallback):
        gamelog.debug('b.e.@navigator pathfindingLadderCallback2', res, seekPoint, parent, showMsg)
        p = BigWorld.player()
        dist, index = res[:2]
        for k, v in self.calculatePos.iteritems():
            if v[0] != -1 and dist > v[0]:
                dist = v[0]
                index = k

        self.teleportSrcDist = dist
        if self.evalIdList and index < len(self.evalIdList):
            self.srcStoneIndex = self.evalIdList[index]
            self.srcStonePos = self.evalPosList[index]
            self.srcStoneDist = dist
            if self.teleportSrcDist == -1 or self.teleportDstDist == -1:
                evalDist = -1
            else:
                evalDist = self.teleportSrcDist + self.teleportDstDist
            if evalDist == -1 or evalDist >= EVAL_RIDEDIST:
                self.onRiding = CAN_RIDE
            spaceNo = getPhaseMappingNum(p.mapID)
            self.pathFindingInner(self.srcStonePos[:3] + (spaceNo,), parent, failedCallback, False, endDist, Functor(self.pathfindingLadderArriveCallback, self.dstStonePos, seekPoint, arriveCallback), self.onRiding, False)
        else:
            p.showGameMsg(GMDD.data.PATH_FIND_ERROR, ())
            self.stopPathFinding()

    def getOtherPort(self, idx):
        if idx % 2 == 0:
            return idx - 1
        return idx + 1

    def reachLadderPort(self, pos):
        p = BigWorld.player()
        if math.fabs(p.position.y - pos[1]) <= 0.1:
            return True
        return False

    def pathfindingLadderArriveCallback(self, dstStonePos, seekpoint, arriveCallback):
        if self.canSetDelay():
            self.setDelayPathFinding(0.5)
            self.delayData['seekPoint'] = seekpoint
            self.delayData['arriveCallback'] = arriveCallback
            self.delayData['delaycondition'] = Functor(self.reachLadderPort, dstStonePos)

    def testDist1(self, pos1, pos2):
        res = [-1, -1]
        callback = Functor(self._testDist1, res)
        if self.currentNav is None:
            p = BigWorld.player()
            self.currentNav = self.seekNavs.get(p.mapID, None)
        gamelog.debug('testDist', self.currentNav, callback)
        self.currentNav.evaluateDistThread(pos1[0], pos1[1], pos1[2], pos2[0], pos2[1], pos2[2], res, 0, callback, 0)

    def _testDist1(self, res):
        gamelog.debug('testDist', res)


class pointData(object):
    __slots__ = ['x',
     'y',
     'z',
     'num']

    def __init__(self, num, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.num = num

    def doPrint(self):
        gamelog.debug('[POINT] %d' % self.num)

    def __repr__(self):
        return '(%s, %s, %s, %s)' % (str(self.x),
         str(self.y),
         str(self.z),
         str(self.num))

    def __getitem__(self, index):
        if index >= 0 and index <= 2:
            return (self.x, self.y, self.z)[index]
        raise Exception('index out of Range %d' % index)


class PathTraceManager(object):

    def __init__(self):
        self.nav = None
        self.pathList = []
        self.isGoing = False
        self.updateVerNum = 0
        self.seekPointList = []
        self.startPos = None
        self.dstPos = None
        self.sleep = True
        self.failed = False
        self.partial = True

    def isFailed(self):
        return self.failed

    def isPartial(self):
        return self.partial

    def startUpdateLM(self, nav, src, dst):
        if nav is None:
            return False
        self.startPos = src
        self.dstPos = dst
        self.seekPointList = [-1, self.startPos]
        self.nav = nav
        self.pathList = [src, dst]
        self.navGo()
        return True

    def navGo(self):
        gamelog.debug('bgf@navigator PathTraceManager navGo', self.pathList)
        self.updateVerNum += 1
        self.navCancel()
        if len(self.pathList) <= 0:
            gamelog.debug('bgf@navigator PathTraceManager navGo case#1')
            self.stop_update(False)
            return
        self.sleep = False
        self.failed = False
        src = self.pathList.pop(0)
        seekDest = self.pathList.pop(0)
        self.isGoing = True
        gamelog.debug('bgf@navigator PathTraceManager navGo start', src, seekDest)
        res = self.nav.go(src.x, src.y, src.z, seekDest.x, seekDest.y, seekDest.z)
        self.startPos = seekDest
        if res is None:
            gamelog.debug('bgf@navigator PathTraceManager navGo case#2')
            self.navCancel()
            return
        gamelog.debug('bgf@navigator PathTraceManager navGo case#3', self.sleep)
        self.updateQueue(self.updateVerNum)

    def getNextPos(self):
        res = None
        if len(self.seekPointList) == 0:
            return res
        if self.seekPointList[0] == -1:
            if len(self.seekPointList) > 2:
                self.seekPointList.pop(0)
        if len(self.seekPointList) > 1:
            if self.seekPointList[0] == -1:
                res = -1
            else:
                res = self.seekPointList.pop(0)
        elif len(self.seekPointList) == 1:
            res = self.seekPointList.pop(0)
        gamelog.debug('bgf@navigator PathTraceManager getNextPos', res, self.seekPointList)
        return res

    def getNextNdPos(self, index):
        res = None
        if len(self.seekPointList) >= index and self.seekPointList[index - 1] != -1:
            res = self.seekPointList[index - 1]
        return res

    def _drawPoints(self, points):
        try:
            gameglobal.rds.ui.littleMap.drawPathTrace(points)
            gameglobal.rds.ui.map.drawPathTrace(points)
        except:
            pass

    def _endDraw(self):
        try:
            gameglobal.rds.ui.littleMap.endDrawPathTrace()
            gameglobal.rds.ui.map.endDrawPathTrace()
        except:
            pass

    def addPoints(self, points):
        self.partial = True
        dp = []
        for p in points:
            if len(self.seekPointList) > 0 and self.seekPointList[-1] == p:
                continue
            self.seekPointList.append(p)
            dp.append(p)
            if (p - self.dstPos).length < 0.2:
                self.partial = False
                gamelog.debug('bgf@navigator PathTraceManager addPoints is not partial')

        gamelog.debug('bgf@navigator PathTraceManager addPoints', dp, points)
        if dp:
            self._drawPoints(dp)

    def updateQueue(self, verNum):
        if verNum != self.updateVerNum:
            return
        if self.sleep:
            self.seekPointList = []
            return
        if self.isGoing:
            gamelog.debug('l.b.@navigator PathTraceManager begin call getNextPositions')
            positions = self.nav.getNextPositions()
            if positions is not None:
                gamelog.debug('l.b.@navigator PathTraceManager end call getNextPositions', len(positions), positions)
            else:
                gamelog.debug('l.b.@navigator PathTraceManager end call getNextPositions', positions)
                self.stop_update()
                self.failed = True
                return
        else:
            positions = None
        if not positions:
            self.navGo()
            return
        self.addPoints(positions)
        if len(positions) > 1:
            return
        BigWorld.callback(0, Functor(self.updateQueue, verNum))

    def navCancel(self):
        gamelog.debug('l.b.@navigator PathTraceManager navCancel', self.nav, self.isGoing)
        if self.nav and self.isGoing:
            self.isGoing = False
            self.nav.cancel()

    def stop_update(self, endDraw = True):
        gamelog.debug('bgf@navigator PathTraceManager stop_update', endDraw)
        self.sleep = True
        self.navCancel()
        if endDraw:
            self._endDraw()
