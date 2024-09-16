#Embedded file name: /WORKSPACE/data/entities/common/mapgamecommon.o
import BigWorld
import utils
import formula
import gametypes
import copy
import gameconfigCommon
if BigWorld.component in ('base', 'cell'):
    import Netease
    import gameconfig
from data import fb_data as FD
from data import sys_config_data as SCD
from data import map_game_grid_data as MGGD
from data import map_game_grid_pos_data as MGGPD
from cdata import map_game_pos_reverse_data as MGPRD
from cdata import map_game_fuben_reverse_data as MGFRD
from data import map_game_config_data as MGCD

def onMapGameStart():
    if BigWorld.component in ('base', 'cell'):
        Netease.mapGameIsOpen = True


def onMapGameEnd():
    if BigWorld.component in ('base', 'cell'):
        Netease.mapGameIsOpen = False


def updateFinishedEvent(finishedEvent):
    if BigWorld.component in ('cell',):
        Netease.mapGameFinishedEvent = finishedEvent


def getMapGameStartTime(tz = None):
    cur = utils.getNow()
    if not checkinMapGameTime(cur):
        return 0
    startStr = MGCD.data.get('mapGameStartTime')
    if not startStr:
        return 0
    return utils.getTimeSecondFromStr(startStr, tz)


def checkinMapGameTime(timeStamp = 0, useCache = True, tz = None):
    if BigWorld.component in ('base', 'cell') and useCache:
        return Netease.mapGameIsOpen
    timeStamp = timeStamp or utils.getNow()
    startStr, endStr = MGCD.data.get('mapGameStartTime'), MGCD.data.get('mapGameEndTime')
    if not startStr or not endStr:
        return False
    else:
        return utils.getTimeSecondFromStr(startStr, tz) <= timeStamp <= utils.getTimeSecondFromStr(endStr, tz)


def checkInMapGameActiveTime(timeStamp = 0, useCache = True, tz = None):
    timeStamp = timeStamp or utils.getNow()
    startStr, finishStr = MGCD.data.get('mapGameStartTime'), MGCD.data.get('mapGameFinishTime')
    if not startStr or not finishStr:
        return False
    return utils.getTimeSecondFromStr(startStr, tz) <= timeStamp <= utils.getTimeSecondFromStr(finishStr, tz)


def getDaysFromMapGameStart():
    cur = utils.getNow()
    if not checkinMapGameTime(cur):
        return 0
    startStr = MGCD.data.get('mapGameStartTime')
    if not startStr:
        return 0
    startTimeStamp = utils.getTimeSecondFromStr(startStr)
    if startTimeStamp > 0:
        return utils.getIntervalDay(cur, startTimeStamp)
    else:
        return 0


def getConfigVal(gridId, attr, default = 0):
    contentId = MGGPD.data.get(gridId, {}).get('contentId', 0)
    if not contentId:
        return default
    contentVal = MGGD.data.get(contentId)
    if not contentVal:
        return default
    return contentVal.get(attr, default)


def isNieghbourGrid(srcId, tgtId):
    if srcId == tgtId:
        return False
    if srcId in MGGPD.data.get(tgtId, {}).get('neighbour', ()) or tgtId in MGGPD.data.get(srcId, {}).get('neighbour', ()):
        return True
    srcPos = MGGPD.data.get(srcId, {}).get('pos')
    tgtPos = MGGPD.data.get(tgtId, {}).get('pos')
    if not srcPos or not tgtPos:
        return False
    if srcPos[1] == tgtPos[1] and abs(srcPos[0] - tgtPos[0]) == 1:
        return True
    if abs(srcPos[1] - tgtPos[1]) == 1:
        if srcPos[0] == tgtPos[0]:
            return True
        elif srcPos[1] % 2 == 0:
            return srcPos[0] == tgtPos[0] + 1
        else:
            return srcPos[0] + 1 == tgtPos[0]
    return False


def getNiehbourGrids(gridId):
    grids = []
    neighbours = MGGPD.data.get(gridId, {}).get('neighbour', ())
    if type(neighbours) not in (list, tuple):
        neighbours = [neighbours]
    for neighbourId in neighbours:
        grids.append(neighbourId)

    myPos = MGGPD.data.get(gridId, {}).get('pos')
    if not myPos:
        return grids
    xPos, yPos = myPos
    posList = []
    posList.append((xPos - 1, yPos))
    posList.append((xPos + 1, yPos))
    posList.append((xPos, yPos - 1))
    posList.append((xPos, yPos + 1))
    if yPos % 2 == 1:
        posList.append((xPos + 1, yPos - 1))
        posList.append((xPos + 1, yPos + 1))
    else:
        posList.append((xPos - 1, yPos - 1))
        posList.append((xPos - 1, yPos + 1))
    for x, y in posList:
        if x < 0 or y < 0:
            continue
        id = MGPRD.data.get((x, y))
        if not id:
            continue
        grids.append(id)

    return grids


def calMineNum(gridId):
    if not MGCD.data.get('specialGridIdList', None):
        return 0
    neighbourList = getNiehbourGrids(gridId)
    tempList = copy.deepcopy(neighbourList)
    for id in tempList:
        neighbourList.extend(getNiehbourGrids(id))

    neighbour = set(neighbourList)
    if gridId in neighbour:
        neighbour.remove(gridId)
    mineNum = 0
    for id in neighbour:
        if id in MGCD.data.get('specialGridIdList', []):
            mineNum += 1

    return mineNum


def getMapGameRewardFame(gridId, dmg):
    contentId = MGGPD.data.get(gridId, {}).get('contentId', 0)
    if not contentId:
        return 0
    data = MGGD.data.get(contentId)
    if not data:
        return 0
    fame = 0
    fame += data.get('addFame', 0)
    if data.get('addFameFormula'):
        fame += formula.calcFormulaById(data['addFameFormula'], {'dmg': dmg,
         'Tdmg': dmg})
    return fame


def getMapGameMultiply(gridType = 0, fbNo = 0, useCache = True):
    defaultVal = gameconfigCommon.mapGameFubenMultiply()
    if not gridType and fbNo:
        gridType = MGFRD.data.get(fbNo, {}).get('type', 0)
    if not gridType:
        return defaultVal
    if useCache and BigWorld.component in ('base', 'cell'):
        return Netease.mapGameMultiplyDict.get(gridType, defaultVal)
    extraStr = gameconfigCommon.mapGameFubenMultiplyEx()
    extraList = extraStr.split(',')
    try:
        for strVal in extraList:
            if not strVal:
                continue
            val = strVal.split(':')
            if not val:
                continue
            if int(val[0]) == gridType:
                return int(val[1])

    except Exception as e:
        print 'Exception:', e.message
        return defaultVal

    return defaultVal


def getMapGameFubenConsumeFame(gridId):
    fbNo = getConfigVal(gridId, 'fubenid', 0)
    if not fbNo:
        return None
    return FD.data.get(fbNo, {}).get('reqFame', None)


def checkVersion():
    if not gameconfigCommon.enableMapGame():
        return 0
    if gameconfigCommon.enableMapGameV1():
        return 1
    if gameconfigCommon.enableMapGameV2():
        return 2


def _checkGridCamp(initCampId, myCampId, eventList = None):
    if not gameconfigCommon.enableMapGameCamp():
        return True
    if not initCampId or initCampId == myCampId:
        return True
    eventIds = MGCD.data.get('otherCampMilestone', {}).get(myCampId, ())
    if type(eventIds) not in (list, tuple):
        eventIds = (eventIds,)
    if eventList and type(eventList) in (list, tuple):
        finishEvents = eventList
    else:
        finishEvents = (eventList or {}).keys()
    if eventIds and set(eventIds) & set(finishEvents):
        return True
    return False


def checkGridCampWithGridId(gridId, campId, eventList = None):
    if not gameconfigCommon.enableMapGameCamp():
        return True
    gd = MGGPD.data.get(gridId)
    if not gd:
        return False
    elif _checkGridCamp(gd.get('initCampId', 0), campId, eventList):
        return True
    else:
        return False


if BigWorld.component in ('base', 'cell'):

    def refreshMapGameMultiplyCache():
        Netease.mapGameMultiplyDict.clear()
        extraStr = gameconfigCommon.mapGameFubenMultiplyEx()
        extraList = extraStr.split(',')
        try:
            for strVal in extraList:
                if not strVal:
                    continue
                val = strVal.split(':')
                Netease.mapGameMultiplyDict[int(val[0])] = int(val[1])

        except Exception as e:
            import gameengine
            gameengine.reportCritical('@xjw refreshMapGameMultiplyCache Exception:', e.message)
            return False

        return True


    def setMapGameMultiplyConfigAndRefresh(configStr, bNotify = False):
        gameconfig.setConfig('mapGameFubenMultiplyEx', configStr, bNotify)
        refreshMapGameMultiplyCache()


    def refreshMapGameDmgLimitCache():
        Netease.mapGameDmgLimitDict.clear()
        extraStr = gameconfigCommon.mapGameFubenDmgLimit()
        extraList = extraStr.split(',')
        try:
            for strVal in extraList:
                if not strVal:
                    continue
                val = strVal.split(':')
                if val[0] in DEFAULT_DMG_LIMIT_MULTI_MAP.iterkeys():
                    name = val[0]
                else:
                    name = int(val[0])
                Netease.mapGameDmgLimitDict[name] = long(val[1])

        except Exception as e:
            import gameengine
            gameengine.reportCritical('@xjw refreshMapGameDmgLimitCache Exception:', e.message)
            return False

        return True


    def setMapGameDmgLimitConfigAndRefresh(configStr, bNotify = False):
        gameconfig.setConfig('mapGameFubenDmgLimit', configStr, bNotify)
        refreshMapGameDmgLimitCache()


    DEFAULT_DMG_LIMIT_MAP = {gametypes.MAP_GAME_GRID_TYPE_BOSS: 5820207116L,
     gametypes.MAP_GAME_GRID_TYPE_ELITE: 755871054,
     gametypes.MAP_GAME_GRID_TYPE_SPRITE_FB: 610421858}
    DEFAULT_DMG_LIMIT_MULTI_MAP = {'single': (gametypes.MAP_GAME_GRID_TYPES_SINGLE_FBS, 1511742108),
     'group': (gametypes.MAP_GAME_GRID_TYPES_GROUP_FBS, 4812929962L)}
    DMG_LIMIT_TAGE = DEFAULT_DMG_LIMIT_MULTI_MAP.keys()

    def getMapGameMaxDamage(gridId = 0, gridType = 0):
        if not gridType:
            gridType = getConfigVal(gridId, 'type', 0)
        if Netease.mapGameDmgLimitDict.has_key(gridType):
            return Netease.mapGameDmgLimitDict.get(gridType)
        defaultValList = []
        for tag, (gridTypes, defaultVal) in DEFAULT_DMG_LIMIT_MULTI_MAP.iteritems():
            if gridType not in gridTypes:
                continue
            if Netease.mapGameDmgLimitDict.has_key(tag):
                return Netease.mapGameDmgLimitDict.get(tag)
            defaultValList.append(defaultVal)

        if gridType in DEFAULT_DMG_LIMIT_MAP.iterkeys():
            return DEFAULT_DMG_LIMIT_MAP.get(gridType)
        if defaultValList:
            return max(defaultValList)
        return 0
