#Embedded file name: /WORKSPACE/data/entities/common/formula.o
import md5
import math
import time
import sys
import cPickle
import json
import re
import random
import BigWorld
import const
import gametypes
import utils
if BigWorld.component in ('base', 'cell'):
    import gameengine
    import Netease
import gamelog
import gameconfigCommon
from sMath import distance2D, distance3D
from Math import Vector2
from crontab import defaultTimezone
from datetime import datetime
from data import fb_data as FD
from data import arena_data as AD
from data import arena_mode_data as AMD
from data import battle_field_data as BFD
from data import map_config_data as MCD
from data import sys_config_data as SCD
from cdata import fb_temp_camp_data as FTCD
from cdata import special_camp_data as PCD
from data import sheng_si_chang_data as SSCD
from data import battle_field_mode_data as BFMD
from data import chunk_mapping_data as CMD
from cdata import mapSearch_iii_data as MIII
from data import world_area_data as WAAD
from data import guild_challenge_data as GCD
from data import guild_config_data as GCFGD
from data import monster_data as MD
from data import monster_clan_war_config_data as MCWCD
from cdata import endless_challenge_config_reverse_data as ECCRD
from cdata import apprentice_target_lv_data as ATLD
from data import apprentice_new_config_data as ANCD
from cdata import endless_challenge_map_config_data as ECMCD
from data import marriage_package_data as MPD
from data import marriage_theme_data as MTD
from data import wing_world_config_data as WDCD
from data import wing_world_city_data as WWCTD
from data import sprite_upgrade_data as SUD
from data import fight_for_love_config_data as FFLCD
from data import personal_zone_gift_data as PZGD
from data import school_top_config_data as STCD
from data import map_game_config_data as MGCD
if BigWorld.component in ('base', 'cell'):
    import gameconst
    from data import fb_progress_entity_data as FPED
    from gamescript import FormularEvalEnv
    from data import formula_server_data as FMD
    from data import log_src_def_data as LSDD
    import gameconfig
elif BigWorld.component in ('client',):
    if not getattr(BigWorld, 'isBot', False):
        from data import formula_client_data as FMD

def _whatFubenTypeInternal(fbNo):
    if fbNo > const.FB_NO_ARENA_START:
        if fbNo in const.FB_NO_ARENA_TDM:
            return const.FB_TYPE_ARENA_TDM
        if fbNo in const.FB_NO_ARENA_ROUND:
            return const.FB_TYPE_ARENA_ROUND
        if fbNo == const.FB_NO_WING_WORLD_XINMO_ARENA:
            return const.FB_TYPE_ARENA_WING_WORLD_XINMO
        if fbNo in const.FB_NO_CROSS_LUN_ZHAN_YUN_DIAN or fbNo in const.FB_NO_40_LUN_ZHAN_YUN_DIAN or fbNo in const.FB_NO_60_LUN_ZHAN_YUN_DIAN:
            return const.FB_TYPE_ARENA_LZYD
    if fbNo == const.FB_NO_SHENG_SI_CHANG:
        return const.FB_TYPE_SHENGSICHANG
    if fbNo in const.FB_NO_MARRIAGE_HALL_SET:
        return const.FB_TYPE_MARRIAGE_HALL
    if fbNo in const.FB_NO_MARRIAGE_ROOM_SET:
        return const.FB_TYPE_MARRIAGE_ROOM
    if fbNo == const.FB_NO_TEAM_SHENG_SI_CHANG:
        return const.FB_TYPE_TEAM_SHENGSICHANG
    if fbNo == const.FB_NO_FIGHT_FOR_LOVE:
        return const.FB_TYPE_FIGHT_FOR_LOVE
    if fbNo == const.FB_NO_SCHOOL_TOP_MATCH:
        return const.FB_TYPE_SCHOOL_TOP_MATCH
    if fbNo > const.FB_NO_BATTLE_FIELD_START and fbNo < const.FB_NO_BATTLE_FIELD_FLAG_START and fbNo in BFD.data:
        return const.FB_TYPE_BATTLE_FIELD_RES
    if fbNo > const.FB_NO_BATTLE_FIELD_FLAG_START and fbNo < const.FB_NO_CROSS_BATTLE_FIELD_FLAG_START and fbNo in BFD.data:
        return const.FB_TYPE_BATTLE_FIELD_FLAG
    if fbNo >= const.FB_NO_CROSS_BATTLE_FIELD_FLAG_START and fbNo < const.FB_NO_CROSS_BATTLE_FIELD_RES_START and fbNo in BFD.data:
        return const.FB_TYPE_BATTLE_FIELD_FLAG
    if fbNo >= const.FB_NO_CROSS_BATTLE_FIELD_RES_START and fbNo < const.FB_NO_BATTLE_FIELD_FORT_START and fbNo in BFD.data:
        return const.FB_TYPE_BATTLE_FIELD_RES
    if fbNo >= const.FB_NO_BATTLE_FIELD_FORT_START and fbNo < const.FB_NO_CROSS_BATTLE_FIELD_FORT_START and fbNo in BFD.data:
        return const.FB_TYPE_BATTLE_FIELD_FORT
    if fbNo >= const.FB_NO_CROSS_BATTLE_FIELD_FORT_START and fbNo < const.FB_NO_BATTLE_FIELD_HOOK_START and fbNo in BFD.data:
        return const.FB_TYPE_BATTLE_FIELD_FORT
    if fbNo >= const.FB_NO_BATTLE_FIELD_HOOK_START and fbNo < const.FB_NO_CROSS_BATTLE_FIELD_HOOK_START and fbNo in BFD.data:
        return const.FB_TYPE_BATTLE_FIELD_HOOK
    if fbNo >= const.FB_NO_CROSS_BATTLE_FIELD_HOOK_START and fbNo < const.FB_NO_BATTLE_FIELD_HUNT_START and fbNo in BFD.data:
        return const.FB_TYPE_BATTLE_FIELD_HOOK
    if const.FB_NO_BATTLE_FIELD_HUNT_START <= fbNo < const.FB_NO_CROSS_BATTLE_FIELD_HUNT_START and fbNo in BFD.data:
        return const.FB_TYPE_BATTLE_FIELD_HUNT
    if const.FB_NO_CROSS_BATTLE_FIELD_HUNT_START <= fbNo < const.FB_NO_BATTLE_FIELD_DOTA_START and fbNo in BFD.data:
        return const.FB_TYPE_BATTLE_FIELD_HUNT
    if const.FB_NO_BATTLE_FIELD_DOTA_START <= fbNo < const.FB_NO_CROSS_BATTLE_FIELD_DOTA_START and fbNo in BFD.data:
        return const.FB_TYPE_BATTLE_FIELD_DOTA
    if const.FB_NO_CROSS_BATTLE_FIELD_DOTA_START <= fbNo < const.FB_NO_BATTLE_FIELD_NEW_FLAG_START and fbNo in BFD.data:
        return const.FB_TYPE_BATTLE_FIELD_DOTA
    if fbNo in const.FB_NO_BATTLE_FIELD_NEW_FLAG and fbNo in BFD.data:
        return const.FB_TYPE_BATTLE_FIELD_NEW_FLAG
    if fbNo in const.FB_NO_BATTLE_FIELD_CQZZ:
        return const.FB_TYPE_BATTLE_FIELD_CQZZ
    if fbNo in const.FB_NO_CROSS_BATTLE_FIELD_CHAOS_FLAG:
        return const.FB_TYPE_BATTLE_FIELD_FLAG
    if fbNo == const.FB_NO_BATTLE_FIELD_PUBG:
        return const.FB_TYPE_BATTLE_FIELD_PUBG
    if fbNo == const.FB_NO_BATTLE_FIELD_TIMING_PUBG:
        return const.FB_TYPE_BATTLE_FIELD_TIMING_PUBG
    if fbNo == const.FB_NO_BATTLE_FIELD_CROSS_WYSL:
        return const.FB_TYPE_BATTLE_FIELD_WYSL
    if const.FB_NO_BATTLE_FIELD_RACE_START <= fbNo < const.FB_NO_BATTLE_FIELD_END and fbNo in BFD.data:
        return const.FB_TYPE_BATTLE_FIELD_RACE
    if fbNo > const.FB_NO_GUILD_CHALLENGE_START and fbNo < const.FB_NO_GUILD_CHALLENGE_END and fbNo in GCD.data:
        return const.FB_TYPE_GUILD_CHALLENGE_YMF
    if const.FB_NO_BATTLE_FIELD_LZS_1 <= fbNo <= const.FB_NO_BATTLE_FIELD_CROSS_LZS_1 and fbNo in BFD.data:
        return const.FB_TYPE_BATTLE_FIELD_LZS
    if fbNo in FD.data:
        fbData = FD.data[fbNo]
    else:
        return const.FB_TYPE_COMMON
    return fbData['type']


def genFubenType():
    for no in const.spaceDict.iterkeys():
        fbType = _whatFubenTypeInternal(no)
        const.spaceDict[no]['fbType'] = fbType
        if fbType in const.FB_TYPE_ARENA or fbType in const.FB_TYPE_ALL_BATTLE_FIELD or fbType in const.FB_TYPE_GUILD_CHALLENGE:
            const.spaceDict[no]['fbIsDuel'] = True


genFubenType()

def getRealSpaceNo(spaceNo):
    if spaceInFbOrDuel(spaceNo):
        spaceNo = spaceNo - spaceNo % const.FB_SPACE_BORDER
    elif spaceInMultiLine(spaceNo):
        spaceNo = getMLNo(spaceNo)
    return spaceNo


def whatAllSpaceNoByFileName(filename):
    res = []
    for key, item in const.spaceDict.iteritems():
        mapname = item['map'].split('/')
        if filename == mapname[-1]:
            res.append(key)

    return res


def whatSpaceNoByFileName(filename):
    for key, item in const.spaceDict.iteritems():
        mapname = item['map'].split('/')
        if filename == mapname[-1]:
            return key

    return 0


def whatSpaceCellNum(spaceNo):
    oriSpaceNo = getMapId(spaceNo)
    if gameconfig.enableSingleCellMobaDotaSpace() and oriSpaceNo in const.ALL_MOBA_DOTA_FB_NOS:
        return (1, 1)
    else:
        spaceInfo = const.spaceDict[oriSpaceNo]
        if oriSpaceNo == const.SPACE_NO_BIG_WORLD and gameconfig.defaultBigWorldMinCellNum():
            return (gameconfig.defaultBigWorldMinCellNum(), spaceInfo.get('maxCellNum', 0))
        return (spaceInfo.get('minCellNum', 0), spaceInfo.get('maxCellNum', 0))


def whatSpaceCellNumNewBalanceBaryCenter(spaceNo):
    oriSpaceNo = getMapId(spaceNo)
    if gameconfig.enableSingleCellMobaDotaSpace() and oriSpaceNo in const.ALL_MOBA_DOTA_FB_NOS:
        return (1, 1)
    elif oriSpaceNo in const.newBalanceSpaceDict:
        return (const.newBalanceSpaceDict[oriSpaceNo].get('minCellNum', 0), const.newBalanceSpaceDict[oriSpaceNo].get('maxCellNum', 0))
    else:
        return whatSpaceCellNum(spaceNo)


def whatSpaceMaxCellNum(spaceNo):
    oriSpaceNo = getMapId(spaceNo)
    return const.spaceDict[oriSpaceNo].get('maxCellNum', 0)


def whatSpaceMap(spaceNo):
    spaceNo = getMapId(spaceNo)
    return const.spaceDict.get(spaceNo, {}).get('map', '')


def whatSpaceBounds(spaceNo):
    spaceNo = getMapId(spaceNo)
    return const.spaceDict.get(spaceNo, {}).get('bounds', None)


def whatSpaceName(spaceNo, isRealSpaceNo = False):
    try:
        mapId = spaceNo if isRealSpaceNo else getMapId(spaceNo)
        return MCD.data[mapId]['name']
    except KeyError:
        return ''


def canSpaceNavigate(spaceNo, isRealSpaceNo = False):
    try:
        mapId = spaceNo if isRealSpaceNo else getMapId(spaceNo)
        return MCD.data[mapId].get('canNavigate', True)
    except KeyError:
        return True


def whatLocationName(spaceNo, chunk = None, isRealSpaceNo = False, includeMLInfo = False):
    name = _whatLocationName(spaceNo, chunk, isRealSpaceNo)
    if not includeMLInfo:
        return name
    elif not inMultiLine(getRealSpaceNo(spaceNo)):
        return name
    else:
        lineNo, _ = getMLInfo(spaceNo)
        return '%s(分线%s)' % (name, lineNo + 1)


def _whatLocationName(spaceNo, chunk = None, isRealSpaceNo = False):
    name = ''
    if spaceNo == const.SPACE_NO_BIG_WORLD:
        if chunk:
            name = CMD.data.get(chunk, {}).get('chunkNameZhongwen', '')
        if name:
            return name
        else:
            return whatSpaceName(spaceNo, isRealSpaceNo)
    else:
        mapId = spaceNo if isRealSpaceNo else getMapId(spaceNo)
        mapping = MCD.data.get(mapId, {}).get('chunknameMapping')
        if mapping:
            if isinstance(mapping, basestring):
                name = CMD.data.get(mapping, {}).get('chunkNameZhongwen', '')
            elif chunk and mapping.has_key(chunk):
                name = CMD.data.get(mapping[chunk], {}).get('chunkNameZhongwen', '')
        if name:
            return name
        fbNo = getFubenNo(spaceNo)
        if fbNo:
            name = whatFubenName(fbNo)
        if name:
            return name
        if chunk:
            name = CMD.data.get(chunk, {}).get('chunkNameZhongwen', '')
        if name:
            return name
        return whatSpaceName(spaceNo, isRealSpaceNo)


def whatAreaName(spaceNo, areaId = None, isRealSpaceNo = False, includeMLInfo = False):
    name = _whatAreaName(spaceNo, areaId, isRealSpaceNo)
    if not includeMLInfo:
        return name
    elif not inMultiLine(getRealSpaceNo(spaceNo)):
        return name
    else:
        lineNo, _ = getMLInfo(spaceNo)
        return '%s(分线%s)' % (name, lineNo + 1)


def _whatAreaName(spaceNo, areaId = None, isRealSpaceNo = False):
    name = ''
    if spaceNo == const.SPACE_NO_BIG_WORLD:
        if areaId:
            name = MIII.data.get(areaId, {}).get('mapName_iii', '')
        if name:
            return name
        else:
            return whatSpaceName(spaceNo, isRealSpaceNo)
    else:
        mapId = spaceNo if isRealSpaceNo else getMapId(spaceNo)
        mapping = MCD.data.get(mapId, {}).get('chunknameMapping')
        if mapping:
            if isinstance(mapping, basestring):
                name = CMD.data.get(mapping, {}).get('chunkNameZhongwen', '')
        if name:
            return name
        fbNo = getFubenNo(spaceNo)
        if inEndlessChallengeFuben(fbNo):
            name = FD.data.get(fbNo, {}).get('name', '')
        elif fbNo:
            name = whatFubenName(fbNo)
        if name:
            return name
        return whatSpaceName(spaceNo, isRealSpaceNo)


def whatFubenManager(spaceNo):
    try:
        if isSplitSpace(spaceNo):
            return const.MULTICELL_FUBEN_MANAGER
        return const.SINGLE_FUBEN_MANAGER
    except KeyError:
        return const.MULTICELL_FUBEN_MANAGER


def whatStaticSpace():
    spaces = []
    for spaceNo, sVal in const.spaceDict.iteritems():
        if sVal['load'] == const.SPACE_LOAD_STATIC:
            spaces.append(spaceNo)

    return spaces


def isSplitSpace(spaceNo):
    try:
        if whatSpaceMaxCellNum(spaceNo) == 1:
            return False
        return True
    except KeyError:
        return True


def isStaticSpace(spaceNo):
    spaceNo = getMapId(spaceNo)
    if spaceNo >= const.WING_CITY_SPACENO_RANGE[0] and spaceNo <= const.WING_CITY_SPACENO_RANGE[1]:
        mapId = getWingCityMapId(spaceNo)
        return const.spaceDict.has_key(mapId)
    if const.spaceDict.has_key(spaceNo):
        return const.spaceDict[spaceNo]['load'] == const.SPACE_LOAD_STATIC
    return False


def getSpaceNo(mapName, default = 0):
    return const.spaceMapNoDict.get(mapName, default)


def getAllSpaceMap():
    map = []
    for spaceNo, sVal in const.spaceDict.iteritems():
        if sVal['load'] == const.SPACE_LOAD_UNLOAD:
            continue
        if sVal['map'] not in map:
            map.append(sVal['map'])

    for key in ECMCD.data.keys():
        tmpMap = 'universes/eg/' + key
        if tmpMap not in map:
            map.append(tmpMap)

    return map


def whatFubenRange(fbNo):
    return (fbNo * const.FB_SPACE_INTERNAL, fbNo * const.FB_SPACE_INTERNAL + (const.FB_SPACE_INTERNAL - 1))


def whatAnnalFubenRange(fbNo):
    return (const.ANNAL_SPACE_NO_START + fbNo * const.FB_SPACE_INTERNAL, const.ANNAL_SPACE_NO_START + fbNo * const.FB_SPACE_INTERNAL + (const.FB_SPACE_INTERNAL - 1))


def whatFubenIn():
    return const.fbDict.keys()


def whatFubenCls(fbNo):
    fbType = whatFubenType(fbNo)
    return const.FB_TYPE_TO_CLASS[fbType]


def whatFubenName(fbNo):
    if fbNo > const.FB_NO_ARENA_START and fbNo in AD.data:
        fbData = AD.data[fbNo]
    elif fbNo > const.FB_NO_BATTLE_FIELD_START and fbNo in BFD.data:
        fbData = BFD.data[fbNo]
    else:
        if fbNo in FD.data:
            return getFbDetailName(fbNo)
        return ''
    if fbData['name'] == '':
        return const.fbDict[fbNo]['name']
    else:
        return fbData['name']


def getFbDetailName(fbNo):
    data = FD.data.get(fbNo, None)
    if not data:
        return ''
    name = data.get('name', None)
    if not name:
        return ''
    detailName = name
    primaryLevelName = data.get('primaryLevelName', None)
    modeName = data.get('modeName', None)
    if BigWorld.component == 'client' and inEndlessChallengeFuben(fbNo):
        p = BigWorld.player()
        voidDreamlandConfigId = getattr(p, 'voidDreamlandConfigId', 0)
        voidDreamlandProgress = getattr(p, 'voidDreamlandProgress', 0)
        primaryLevelName = ECCRD.data.get(voidDreamlandConfigId, {}).get('primaryLevelName', '')
        modeName = str(voidDreamlandProgress)
    elif BigWorld.component == 'client' and inTeamEndlessFuben(fbNo):
        primaryLevelName = name
        from gamestrings import gameStrings
        detailName = gameStrings.VOID_LUNHUI_NAME
        import gameglobal
        if gameglobal.rds.GameState > gametypes.GS_LOGIN:
            p = BigWorld.player()
            if inTeamEndlessFubenSpace(p.spaceNo):
                teamEndlessProgress = getattr(p, 'teamEndlessFubenData', {}).get(gametypes.TEAM_ENDLESS_INFO_LV, 0)
                if teamEndlessProgress:
                    modeName = str(teamEndlessProgress)
        else:
            modeName = ''
    elif BigWorld.component == 'client' and inSpriteChallengeFb(fbNo):
        primaryLevelName = ''
        from gamestrings import gameStrings
        detailName = gameStrings.SPRITE_CHALLENGE_NAME
        import gameglobal
        if gameglobal.rds.GameState > gametypes.GS_LOGIN:
            p = BigWorld.player()
            if getattr(p, 'spriteChallengeProgress', 0):
                modeName = gameStrings.SPRITE_CHALLENGE_DIFF_TEXT % p.spriteChallengeProgress
            else:
                modeName = ''
        else:
            modeName = ''
    if primaryLevelName:
        detailName = detailName + '·' + primaryLevelName
    if modeName:
        detailName = detailName + '(' + modeName + ')'
    return detailName


def whatFubenType(fbNo):
    if BigWorld.component == 'client':
        return const.spaceDict.get(fbNo, {}).get('fbType', const.FB_TYPE_COMMON)
    elif fbNo not in const.spaceDict:
        return const.FB_TYPE_COMMON
    else:
        fbType = const.spaceDict.get(fbNo, {}).get('fbType', None)
        if fbType != None:
            return fbType
        genFubenType()
        return const.spaceDict.get(fbNo, {}).get('fbType', const.FB_TYPE_COMMON)


def getFubenData(fbNo):
    if fbNo > const.FB_NO_BATTLE_FIELD_START and fbNo < const.FB_NO_ARENA_START:
        data = BFD.data.get(fbNo)
    elif fbNo > const.FB_NO_ARENA_START:
        data = AD.data.get(fbNo)
    else:
        data = FD.data.get(fbNo)
    return data


def whatFubenMode(fbNo):
    if fbNo > const.FB_NO_ARENA_START:
        return const.FB_MODE_EASY_SINGLE
    if fbNo > const.FB_NO_BATTLE_FIELD_START and fbNo in BFD.data:
        return const.FB_MODE_EASY_SINGLE
    if fbNo in FD.data:
        fbData = FD.data[fbNo]
    else:
        return const.FB_MODE_EASY_SINGLE
    return fbData.get('fbMode', const.FB_MODE_NONE)


def _getPosAndDir(sd, index):
    pos = sd.get('campPos', None)
    directory = sd.get('campDir', None)
    if pos == None or directory == None or index not in pos or index not in directory:
        return (const.SPACE_FIX_POS, const.SPACE_FIX_DIR)
    else:
        return (pos[index], directory[index])


def whatFubenEntry(fbNo, index, ownerBox = None):
    gamelog.debug('@hjx ssc#whatFubenEntry0:', fbNo, index)
    if fbNo > const.FB_NO_BATTLE_FIELD_START and fbNo < const.FB_NO_BATTLE_FIELD_END and fbNo in BFD.data:
        index = str(index + 1)
        sd = BFD.data.get(fbNo)
        if sd:
            if fbNo == const.FB_NO_BATTLE_FIELD_PUBG or fbNo == const.FB_NO_BATTLE_FIELD_TIMING_PUBG:
                return (random.choice(sd['campPos'].values()), random.choice(sd['campDir'].values()))
            else:
                return _getPosAndDir(sd, index)
    else:
        if fbNo > const.FB_NO_ARENA_START and fbNo < const.FB_NO_ARENA_END and fbNo in AD.data:
            index = str(index + 1)
            sd = AD.data[fbNo]
            return _getPosAndDir(sd, index)
        if fbNo > const.FB_NO_GUILD_CHALLENGE_START and fbNo < const.FB_NO_GUILD_CHALLENGE_END and fbNo in GCD.data:
            camp, pIndex = guildChallengePos2Camp(index)
            gd = GCD.data.get(fbNo)
            try:
                return (gd['campPos'][str(camp + 1)][pIndex], gd['campDir'][str(camp + 1)][pIndex])
            except:
                return (const.SPACE_FIX_POS, const.SPACE_FIX_DIR)

        elif fbNo == const.FB_NO_SHENG_SI_CHANG or fbNo == const.FB_NO_TEAM_SHENG_SI_CHANG:
            sd = SSCD.data.get(fbNo)
            index = str(index + 1)
            if sd:
                gamelog.debug('@hjx ssc#whatFubenEntry1:', index, _getPosAndDir(sd, index))
                return _getPosAndDir(sd, index)
        else:
            if fbNo in const.FB_NO_MARRIAGE_HALL_SET:
                mData = MTD.data.get(fbNo, {})
                hallPos = mData.get('pos', (0, 0, 0))
                hallDir = mData.get('dir', (0, 0, 0))
                return (hallPos, hallDir)
            if fbNo in const.FB_NO_MARRIAGE_ROOM_SET:
                mtype = getattr(ownerBox, 'marriageType', None)
                subType = getattr(ownerBox, 'marriageSubType', None)
                mData = MPD.data.get((mtype, subType), {})
                roomPos = mData.get('roomPos', (0, 0, 0))
                roomDir = mData.get('roomDir', (0, 0, 0))
                return (roomPos, roomDir)
            if fbNo == const.FB_NO_FIGHT_FOR_LOVE:
                enterPos1, enterPos2 = FFLCD.data.get('enterPos', ((0, 0, 0), (0, 0, 0)))
                enterPos = (random.uniform(enterPos1[0], enterPos2[0]), random.uniform(enterPos1[1], enterPos2[1]), random.uniform(enterPos1[2], enterPos2[2]))
                enterDir = FFLCD.data.get('enterDir', (0, 0, 0))
                return (enterPos, enterDir)
            if fbNo == const.FB_NO_SCHOOL_TOP_MATCH:
                if index == gametypes.SCHOOL_TOP_CAMP_TOP_PLAYER:
                    pos = STCD.data.get('schoolTopPos', (0, 0, 0))
                    dire = STCD.data.get('schoolTopDir', (0, 0, 0))
                    return (pos, dire)
                else:
                    pos = STCD.data.get('pos', (0, 0, 0))
                    dire = STCD.data.get('dir', (0, 0, 0))
                    return (pos, dire)
            else:
                try:
                    sd = FD.data[fbNo]
                    keepEnterBounds = sd.get('keepEnterBounds')
                    if keepEnterBounds:
                        maxX = max(keepEnterBounds[0], keepEnterBounds[2])
                        minX = min(keepEnterBounds[0], keepEnterBounds[2])
                        maxZ = max(keepEnterBounds[1], keepEnterBounds[3])
                        minZ = min(keepEnterBounds[1], keepEnterBounds[3])
                        if ownerBox and minX < ownerBox.position[0] < maxX and minZ < ownerBox.position[2] < maxZ:
                            return (ownerBox.position, ownerBox.direction)
                    if ownerBox and inEndlessChallengeFuben(fbNo) and hasattr(ownerBox, 'MISC_VAR_CPRI') and ownerBox.getCellPrivateMiscProperty(gametypes.MISC_VAR_CPRI_ENDLESS_CHALLENGE_FUBEN_ENTRY, ()):
                        entryPos, entryDir = ownerBox.getCellPrivateMiscProperty(gametypes.MISC_VAR_CPRI_ENDLESS_CHALLENGE_FUBEN_ENTRY, ())
                        return (entryPos, entryDir)
                    return (sd['inPos'], sd['inDir'])
                except (KeyError, IndexError):
                    return (const.SPACE_FIX_POS, const.SPACE_FIX_DIR)


def _getFubenExitPos(data, groupNUID):
    exitPosType = data.get('exitPosType', 0)
    exitPosList = data.get('exitPosList', ())
    if exitPosType == 1 and exitPosList:
        return random.choice(exitPosList)
    if exitPosType == 2 and exitPosList:
        return exitPosList[groupNUID % len(exitPosList)]
    return (data['outPos'], data['outDir'])


def whatFubenExit(fbNo, ownerInfo, groupNUID):
    try:
        sd = FD.data[fbNo]
        if sd.get('outToEnterPos'):
            return (ownerInfo['spaceNo'], ownerInfo['position'], ownerInfo['direction'])
        keepLeaveBounds = sd.get('keepLeaveBounds')
        if keepLeaveBounds:
            maxX = max(keepLeaveBounds[0], keepLeaveBounds[2])
            minX = min(keepLeaveBounds[0], keepLeaveBounds[2])
            maxZ = max(keepLeaveBounds[1], keepLeaveBounds[3])
            minZ = min(keepLeaveBounds[1], keepLeaveBounds[3])
            if minX < ownerInfo['position'][0] < maxX and minZ < ownerInfo['position'][2] < maxZ:
                return (sd['outSpaceNo'], ownerInfo['position'], ownerInfo['direction'])
        outPos, outDir = _getFubenExitPos(sd, groupNUID)
        return (sd['outSpaceNo'], outPos, outDir)
    except (KeyError, IndexError):
        return (gameconst.DEFAULT_SPACE, gameconst.DEFAULT_POSITION, gameconst.DEFAULT_DIRECTION)


def getFubenNo(spaceNo):
    if not spaceInFbOrDuel(spaceNo):
        return 0
    return spaceNo // const.FB_SPACE_INTERNAL


def getAnnalFubenNo(spaceNo):
    if not spaceInAnnalReplay(spaceNo):
        return 0
    return getFubenNo(spaceNo - const.ANNAL_SPACE_NO_START)


def getWingCityMapId(spaceNo):
    cityType = getWingCityType(spaceNo)
    return const.WING_CITY_MAP_ID_START[cityType] + spaceNo % const.WING_CITY_MAX_ID


def isMultiCarrierFubenNo(fbNo):
    from data import multi_carrier_config_data as MCCD
    return fbNo in MCCD.data.get('multiCarrierFbNo', (1667,))


def isMultiCarrierMonsterTag(tag):
    if tag == 'multi_carrier':
        return True
    return False


def canObserveFB(spaceNo):
    fbId = getFubenNo(spaceNo)
    return FD.data.get(fbId, {}).get('canObserve')


def whatWorldAreaIn():
    return WAAD.data.keys()


def validWorldArea(areaId):
    return areaId in whatWorldAreaIn()


def getGuildSceneNo(spaceNo):
    if not spaceInGuild(spaceNo):
        return
    return const.GUILD_SCENE_NO


def getGuildSpaceNo(guildDBID):
    return const.GUILD_SPACE_NO_START + guildDBID


def getHomeFloorNo(spaceNo):
    return spaceNo


def getHomeRoomNo(spaceNo):
    return spaceNo


def getMLNo(spaceNo):
    if not utils.inRange(const.ML_SPACENO_RANGE, spaceNo):
        return 0
    return spaceNo / const.ML_SPACE_INTERVAL


def getMLGNo(spaceNo):
    if not utils.inRange(const.ML_SPACENO_RANGE, spaceNo):
        return 0
    mlNo = getMLNo(spaceNo)
    for mlgNo, mlgData in const.ML_GROUP.iteritems():
        if mlNo in mlgData['floorSpaces']:
            return mlgNo

    return 0


def getMLFloorNo(spaceNo):
    if not utils.inRange(const.ML_SPACENO_RANGE, spaceNo):
        return -1
    mlNo = getMLNo(spaceNo)
    return getMLFloorNoByMLNo(mlNo)


def getMLFloorNoByMLNo(mlNo):
    for mlgNo, mlgData in const.ML_GROUP.iteritems():
        if mlNo in mlgData['floorSpaces']:
            return mlgData['floorSpaces'].index(mlNo)

    return -1


def getMLGNoByMLNo(mlNo):
    for mlgNo, mlgData in const.ML_GROUP.iteritems():
        if mlNo in mlgData['floorSpaces']:
            return mlgNo

    return 0


def getMLNoByMLGNoAndFloorNo(mlgNo, floorNo):
    floorSpaces = const.ML_GROUP.get(mlgNo, {}).get('floorSpaces', [])
    if floorNo < len(floorSpaces):
        return floorSpaces[floorNo]
    return 0


def getMLInfo(spaceNo):
    if not utils.inRange(const.ML_SPACENO_RANGE, spaceNo):
        return (-1, -1)
    lineNo = spaceNo % const.ML_SPACE_INTERVAL
    floorNo = getMLFloorNo(spaceNo)
    return (lineNo, floorNo)


def getMLSpaceNo(mlgNo, lineNo, floorNo):
    floorBaseSpaceNo = const.ML_GROUP[mlgNo]['floorSpaces'][floorNo]
    return floorBaseSpaceNo * const.ML_SPACE_INTERVAL + lineNo


def getAnnalSceneNo(spaceNo):
    if not spaceInAnnalReplay(spaceNo):
        return
    return const.ANNAL_SCENE_NO


def getAnnalSrcSceneNo(spaceNo):
    if not spaceInAnnalReplay(spaceNo):
        return
    return spaceNo - const.ANNAL_SPACE_NO_START


def needDigongMgr(spaceNo):
    mlgNo = getMLGNo(spaceNo)
    return const.ML_GROUP[mlgNo].get('mgr', 0)


def inDuelZone(fbNo):
    return const.spaceDict.get(fbNo, {}).get('fbIsDuel', False)


def spaceInFbOrDuel(spaceNo):
    return utils.inRange(const.FB_DUEL_SPACENO_RANGE, spaceNo)


def spaceInFuben(spaceNo):
    return utils.inRange(const.FB_SPACENO_RANGE, spaceNo)


def spaceInBattleField(spaceNo):
    return utils.inRange(const.BF_SPACENO_RANGE, spaceNo)


def spaceInArena(spaceNo):
    return utils.inRange(const.ARENA_SPACENO_RANGE, spaceNo)


def spaceInChaosFlagsBattleField(spaceNo):
    return utils.inRange(const.CHAOS_FLAGS_SPACENO_RANGE, spaceNo)


def spaceInMarriage(spaceNo):
    return utils.inRange(const.MARRIAGE_SPACENO_RANGE, spaceNo)


def spaceInMarriageCrossHall(spaceNo):
    fbNo = getFubenNo(spaceNo)
    return fbNo == const.FB_NO_MARRIAGE_GREAT_HALL


def spaceInDuel(spaceNo):
    return utils.inRange(const.DUEL_SPACENO_RANGE, spaceNo)


def spaceInHomeCommunity(spaceNo):
    return utils.inRange(const.HOME_COMMUNITY_SPACENO_RANGE, spaceNo)


def spaceInHomeFloor(spaceNo):
    return utils.inRange(const.HOME_FLOOR_SPACENO_RANGE, spaceNo)


def spaceInHomeRoom(spaceNo):
    return utils.inRange(const.HOME_ROOM_SPACENO_RANGE, spaceNo)


def spaceInHome(spaceNo):
    return spaceInHomeCommunity(spaceNo) or spaceInHomeFloor(spaceNo) or spaceInHomeRoom(spaceNo) or spaceInHomeEnlargedRoom(spaceNo)


def spaceInHomeEnlargedRoom(spaceNo):
    return utils.inRange(const.HOME_ENLARGED_ROOM_SPACENO_RANGE, spaceNo)


def spaceInClanWarPhase(spaceNo):
    return spaceNo in SCD.data.get('clanWarPhase', ())


def spaceInWorld(spaceNo):
    return 1 <= spaceNo < const.ML_SPACE_BORDER or const.WM_SPACE_BORDER <= spaceNo < const.FB_SPACE_BORDER


def spaceInWorldWar(spaceNo):
    return spaceNo == utils.getWorldWarSpaceNo()


def spaceInWorldWarBattle(spaceNo):
    return spaceNo == const.SPACE_NO_WORLD_WAR_BATTLE or spaceNo == const.SPACE_NO_WORLD_WAR_BATTLE_YOUNG


def spaceInWorldWarBattleOld(spaceNo):
    return spaceNo == const.SPACE_NO_WORLD_WAR_BATTLE


def spaceInWorldWarBattleYoung(spaceNo):
    return spaceNo == const.SPACE_NO_WORLD_WAR_BATTLE_YOUNG


def spaceInWorldWarRob(spaceNo):
    return spaceNo == const.SPACE_NO_WORLD_WAR_ROB or spaceNo == const.SPACE_NO_WORLD_WAR_ROB_YOUNG


def spaceInWorldWarRobYoung(spaceNo):
    return spaceNo == const.SPACE_NO_WORLD_WAR_ROB_YOUNG


def spaceInWorldWarRobOld(spaceNo):
    return spaceNo == const.SPACE_NO_WORLD_WAR_ROB


def spaceInWorldWarEx(spaceNo):
    return spaceNo in const.SPACE_NO_WORLD_WAR_ALL


def spaceInMultiLine(spaceNo):
    return utils.inRange(const.ML_SPACENO_RANGE, spaceNo)


def spaceInGuild(spaceNo):
    return utils.inRange(const.GUILD_SPACENO_RANGE, spaceNo)


def spaceInWingCity(spaceNo):
    if spaceNo >= const.WING_CITY_SPACENO_RANGE[0] and spaceNo <= const.WING_CITY_SPACENO_RANGE[1]:
        mapId = getWingCityMapId(spaceNo)
        return const.spaceDict.has_key(mapId)
    return False


def spaceInWingWarCity(spaceNo):
    if spaceNo >= const.WING_CITY_SPACENO_RANGE[0] and spaceNo <= const.WING_CITY_SPACENO_RANGE[1]:
        cityType = getWingCityType(spaceNo)
        if cityType != const.WING_CITY_TYPE_WAR:
            return False
        mapId = getWingCityMapId(spaceNo)
        return const.spaceDict.has_key(mapId)
    return False


def spaceInWingPeaceCity(spaceNo):
    if spaceNo >= const.WING_CITY_SPACENO_RANGE[0] and spaceNo <= const.WING_CITY_SPACENO_RANGE[1]:
        cityType = getWingCityType(spaceNo)
        if cityType != const.WING_CITY_TYPE_PEACE:
            return False
        mapId = getWingCityMapId(spaceNo)
        return const.spaceDict.has_key(mapId)
    return False


def spaceInWingBornIsland(spaceNo):
    return spaceNo == const.SPACE_NO_WING_WORLD_ISLAND


def spaceInWingBornIslandOrPeaceCity(spaceNo):
    return spaceNo == const.SPACE_NO_WING_WORLD_ISLAND or spaceInWingPeaceCity(spaceNo)


def spaceInBornIslandOrWingCity(spaceNo):
    return spaceNo == const.SPACE_NO_WING_WORLD_ISLAND or spaceInWingCity(spaceNo)


def wingPeaceCityInSpace(cityId, spaceNo):
    no = WWCTD.data.get(cityId, {}).get('spaceNos', (0, 0))[const.WING_CITY_TYPE_PEACE] + const.WING_CITY_SPACE_START[const.WING_CITY_TYPE_PEACE]
    return no == transToGroupWingCitySpaceNo(spaceNo, 1)


def spaceInAnnalReplay(spaceNo):
    return spaceNo > const.ANNAL_SPACE_NO_START and spaceNo < const.ANNAL_SPACE_NO_END


def spaceInWingWorldXinMoML(spaceNo):
    mlgNo = getMLGNo(spaceNo)
    return mlgNo == const.ML_GROUP_NO_WING_WORLD_XINMO


def spaceInWingWorldXinMoTeamLimit(spaceNo):
    fbNo = getFubenNo(spaceNo)
    return spaceInWingWorldXinMoML(spaceNo) or fbNo == const.FB_NO_WING_WORLD_XINMO_ARENA


def isWingWorldXinMoArenaFb(fbNo):
    return fbNo == const.FB_NO_WING_WORLD_XINMO_ARENA


def isLzydArenaFb(fbNo):
    return fbNo in const.FB_NO_CROSS_LUN_ZHAN_YUN_DIAN


def isBalanceAreanFb(fbNo):
    return fbNo in const.FB_NO_BALANCE_ARENA


def isDoubleArenaFb(fbNo):
    return fbNo in const.FB_NO_DOUBLE_ARENA


def isClanWarChallengeFb(fbNo):
    return fbNo in const.FB_NO_CLAN_WAR_CHALLENGE


def isSoulBackArenaFbStatus(fbNo):
    from data import duel_config_data as DCD
    if not gameconfig.enableBalanceReLogon():
        return False
    if fbNo in const.FB_NO_BALANCE_ARENA and fbNo in DCD.data.get('soulBackArenaFbStatus', []):
        return True
    return False


def isBalanceArenaMode(arenaMode):
    return arenaMode in const.CROSS_BALANCE_ARENA or arenaMode in const.CROSS_BALANCE_ARENA_SCORE


def macLimitArenaMode(arenaMode):
    return isBalanceArenaMode(arenaMode) and arenaMode not in (const.ARENA_MODE_CROSS_MS_ROUND_3V3_BALANCE_GROUP, const.ARENA_MODE_CROSS_MS_ROUND_3V3_BALANCE_FINAL)


def isArenaScoreMode(arenaMode):
    return arenaMode in const.CROSS_BALANCE_ARENA_SCORE


def isDoubleArenaMode(arenaMode):
    return arenaMode in const.CROSS_DOUBLE_ARENA


def spaceInWingWorldXinMoArena(spaceNo):
    return isWingWorldXinMoArenaFb(getFubenNo(spaceNo))


def isWingWorldXinMoUniqueBossFb(fbNo):
    return fbNo in const.FB_NO_WING_WORLD_XINMO_UNIQUE_BOSS_LIST


def spaceInWingWorldXinMoUniqueBoss(spaceNo):
    fbNo = getFubenNo(spaceNo)
    return isWingWorldXinMoUniqueBossFb(fbNo)


def isWingWorldXinMoNormalBossFb(fbNo):
    return fbNo in const.FB_NO_WING_WORLD_XINMO_NORMAL_BOSS_LIST


def spaceInWingWorldXinMoNormalBoss(spaceNo):
    fbNo = getFubenNo(spaceNo)
    return isWingWorldXinMoNormalBossFb(fbNo)


def isWingWorldXinMoCanAnnalFb(fbNo):
    return isWingWorldXinMoArenaFb(fbNo) or isWingWorldXinMoUniqueBossFb(fbNo)


def inWorld(sceneNo):
    return sceneNo < const.ML_SPACE_BORDER or const.WM_SPACE_BORDER <= sceneNo < const.FB_SPACE_BORDER


def inFuben(sceneNo):
    return const.FB_SPACE_BORDER <= sceneNo < const.FB_NO_BATTLE_FIELD_START


def inBattleField(sceneNo):
    return const.FB_NO_BATTLE_FIELD_START <= sceneNo <= const.FB_NO_BATTLE_FIELD_END


def inBattleFieldSpace(spaceNo):
    return inBattleField(getFubenNo(spaceNo))


def inResBattleField(fbNo):
    return fbNo in const.FB_NO_BATTLE_FIELD_RES


def inFlagBattleField(fbNo):
    return fbNo in const.FB_NO_BATTLE_FIELD_FLAG


def inFortBattleField(fbNo):
    return fbNo in const.FB_NO_BATTLE_FIELD_FORT


def inHookBattleField(fbNo):
    return fbNo in const.FB_NO_BATTLE_FIELD_HOOK


def inHuntBattleField(fbNo):
    return fbNo in const.FB_NO_BATTLE_FIELD_HUNT


def inDotaBattleField(fbNo):
    return fbNo in const.FB_NO_BATTLE_FIELD_DOTA


def inNewFlagBattleField(fbNo):
    return fbNo in const.FB_NO_BATTLE_FIELD_NEW_FLAG


def inCqzzBattleField(fbNo):
    return fbNo in const.FB_NO_BATTLE_FIELD_CQZZ


def inRaceBattleField(fbNo):
    return fbNo in const.FB_NO_BATTLE_FIELD_RACE


def inLZSBattleField(fbNo):
    return fbNo in const.FB_NO_BATTLE_FIELD_LZS


def inChaosFlagsBattleField(fbNo):
    return fbNo in const.FB_NO_CROSS_BATTLE_FIELD_CHAOS_FLAG


def inCqzzBattleFieldSpace(spaceNo):
    return inCqzzBattleField(getFubenNo(spaceNo))


def inCommonBattleField(fbNo):
    return inResBattleField(fbNo) or inFlagBattleField(fbNo) or inFortBattleField(fbNo) or inCqzzBattleField(fbNo)


def inCommonBattleFieldSpace(spaceNo):
    return inCommonBattleField(getFubenNo(spaceNo))


def relogonBattleField(fbNo):
    if inRaceBattleField(fbNo):
        return False
    return True


def relogonArena(fbNo):
    if fbNo in const.FB_NO_CROSS_5V5_ROUND_APD and gameconfigCommon.enableNoRenter5v5Playoffs():
        return False
    return True


def inGuildTournamentQL(fbNo):
    return fbNo == const.FB_NO_GUILD_TOURNAMENT_BATTLE_FIELD_FORT_1


def inGuildTournamentBH(fbNo):
    return fbNo == const.FB_NO_GUILD_TOURNAMENT_BATTLE_FIELD_FLAG_1


def inNewGuildTournamentQL(fbNo):
    from data import guild_tournament_data as GTD
    return fbNo in GTD.data.get(gametypes.GUILD_TOURNAMENT_GROUP_QL, {}).get('fbNoList', [])


def inNewGuildTournamentBH(fbNo):
    from data import guild_tournament_data as GTD
    return fbNo in GTD.data.get(gametypes.GUILD_TOURNAMENT_GROUP_BH, {}).get('fbNoList', [])


def inNewGuildTournmanetFORT(fbNo):
    return fbNo in (const.FB_NO_NEW_GTN_BATTLE_FIELD_6,)


def inNewGuildTournmanetFLAG(fbNo):
    return fbNo in (const.FB_NO_NEW_GTN_BATTLE_FIELD_3, const.FB_NO_NEW_GTN_BATTLE_FIELD_5)


def inNewGuildTournmanetCQZZ(fbNo):
    return fbNo in (const.FB_NO_NEW_GTN_BATTLE_FIELD_4, const.FB_NO_NEW_GTN_BATTLE_FIELD_2)


def inNewGuildTournmanetLYG(fbNo):
    return fbNo in (const.FB_NO_NEW_GTN_BATTLE_FIELD_1,)


def inArena(sceneNo):
    return const.FB_NO_ARENA_START <= sceneNo <= const.FB_NO_ARENA_END


def inShengSiChang(sceneNo):
    return sceneNo == const.FB_NO_SHENG_SI_CHANG


def inTeamShengSiChang(sceneNo):
    return sceneNo == const.FB_NO_TEAM_SHENG_SI_CHANG


def inEndlessChallengeFuben(fbNo):
    return fbNo in const.FB_TYPE_ENDLESS_CHALLENGE_LIST


def inEndlessChallengeSpace(spaceNo):
    return inEndlessChallengeFuben(getFubenNo(spaceNo))


def inSkyWingChallengeFuben(fbNo):
    return fbNo in const.FB_NO_SKY_WING_CHALLENG_LIST


def inSkyWingChallengeSpace(spaceNo):
    return inSkyWingChallengeFuben(getFubenNo(spaceNo))


def inSkyWingRobFuben(fbNo):
    return fbNo in const.FB_NO_SKY_WING_ROB_LIST


def inSkyWingRobSpace(spaceNo):
    return inSkyWingRobFuben(getFubenNo(spaceNo))


def inSkyWingFuben(fbNo):
    return fbNo in const.FB_NO_SKY_WING_LIST


def inSkyWingFubenSpace(spaceNo):
    return inSkyWingFuben(getFubenNo(spaceNo))


def inSchoolTopDpsFuben(fbNo):
    return fbNo == const.FB_NO_SCHOOL_TOP_DPS


def inSchoolTopFubenSpace(spaceNo):
    return inSchoolTopDpsFuben(getFubenNo(spaceNo))


def inZMJFuben(fbNo):
    return fbNo in const.FB_NOS_ZMJ


def inZMJFubenSpace(spaceNo):
    return inZMJFuben(getFubenNo(spaceNo))


def inZMJLowFuben(fbNo):
    return fbNo in const.FB_NOS_ZMJ_LOW


def inZMJLowFubenSpace(spaceNo):
    return inZMJLowFuben(getFubenNo(spaceNo))


def inZMJHighFuben(fbNo):
    return fbNo in const.FB_NOS_ZMJ_HIGH


def inZMJHighFubenSpace(spaceNo):
    return inZMJHighFuben(getFubenNo(spaceNo))


def inZMJStarBossFuben(fbNo):
    return fbNo in const.FB_NOS_ZMJ_STAR


def inZMJStarBossFubenSpace(spaceNo):
    return inZMJStarBossFuben(getFubenNo(spaceNo))


def inTeamEndlessFuben(fbNo):
    return fbNo in const.FB_NO_TEAM_ENDLESS


def inTeamEndlessFubenSpace(spaceNo):
    return inTeamEndlessFuben(getFubenNo(spaceNo))


def inJumpQueueSchoolBalanceBF(fbNo):
    if fbNo in const.FB_NO_JUMP_QUEUE_NO_SCHOOL_BALANCE:
        return False
    return True


def inJumpQueueBF(fbNo):
    if fbNo in const.FB_NO_NO_JUNP_BATTLE_FIELD:
        return False
    return True


def inMapGameFuben(fbNo):
    return fbNo in MGCD.data.get('FB_NO_MAP_GAME_FB', const.FB_NO_MAP_GAME_FB)


def inMapGameBossFuben(fbNo):
    return fbNo in MGCD.data.get('FB_NO_DTWF_BOSSES', const.FB_NO_DTWF_BOSSES)


def inMapGameEliteFuben(fbNo):
    return fbNo in MGCD.data.get('FB_NO_DTWF_ELITES', const.FB_NO_DTWF_ELITES)


def inMapGameSingleFuben(fbNo):
    return fbNo in MGCD.data.get('FB_NO_DTWF_SINGLES', const.FB_NO_DTWF_SINGLES)


def inMapGameSyncHpFuben(fbNo):
    return fbNo in MGCD.data.get('FB_NO_MAP_GAME_FB', const.FB_NO_MAP_GAME_FB)


def inMapGameNormalFuben():
    return False


def inMapGameGroupFuben(fbNo):
    return fbNo in MGCD.data.get('MAP_GAME_GROUP_FB', const.MAP_GAME_GROUP_FB_SET)


def inDuel(sceneNo):
    return const.FB_NO_DUEL_START <= sceneNo <= const.FB_NO_DUEL_END


def inMultiLine(sceneNo):
    return const.ML_SPACE_BORDER <= sceneNo <= const.WM_SPACE_BORDER


def inWorldWar(spaceNo):
    return spaceInWorldWar(spaceNo)


def inIsolatedMap(spaceNo):
    mapId = getMapId(spaceNo)
    mapData = MCD.data.get(mapId)
    return mapData and mapData.get('isolated', 0)


def inSpaceOfSplitFbMgr(spaceNo):
    return inFubenOfSplitFbMgr(getFubenNo(spaceNo))


def inFubenOfSplitFbMgr(fbNo):
    if not gameconfig.enableSplitFbMgr():
        return False
    return fbNo in const.FB_TYPE_SPLIT_FB_MGR_LIST


def inWingWorldOpenSpace(spaceNo):
    if not spaceInMultiLine(spaceNo):
        return False
    mlgNo = getMLGNo(spaceNo)
    if not mlgNo:
        return False
    if mlgNo not in WDCD.data.get('wingWorldDGList', []):
        return False
    return True


def whatFubenProgress(fbNo):
    result = []
    if fbNo in FPED.data:
        result = FPED.data[fbNo].keys()
    if 0 in result:
        result.remove(0)
    return result


def howManyFubenProgress(fbNo):
    return len(whatFubenProgress(fbNo))


def whatFubenProgressName(fbNo, pgNo):
    from data import fb_progress_relations as FPR
    if (fbNo, pgNo) in FPR.data:
        desc = FPR.data[fbNo, pgNo].get('desc')
        if desc != None:
            return desc
    return str(pgNo)


def fitFubenLv(fbNo, level):
    if fbNo > const.FB_NO_BATTLE_FIELD_START and fbNo in BFD.data:
        fbData = BFD.data[fbNo]
    elif fbNo in FD.data:
        fbData = FD.data[fbNo]
    else:
        return False
    if fbData['lvMin'] <= level <= fbData['lvMax']:
        return True
    return False


def whatFubenDesc(fbNo):
    fbType = whatFubenType(fbNo)
    return const.FB_TYPE_DESC[fbType]


def fbNo2ArenaMode(fbNo):
    if not inArena(fbNo):
        return 0
    for key, value in const.fbDict.iteritems():
        if key == fbNo:
            return value.get('mode', 0)

    return const.ARENA_MODE_ALL


def inExcludeFubenList(fbNo, fbList):
    if not fbList:
        return False
    for tmpFb in fbList:
        if fbNo == tmpFb:
            return True
        if fbNo in FD.data.get(tmpFb, {}).get('excludeCurrFbs', ()):
            return True

    return False


def isCrossServerLzyd(fbNo):
    if fbNo in const.FB_NO_CROSS_LUN_ZHAN_YUN_DIAN:
        return True
    return False


def isCrossServerArena(arenaMode):
    return arenaMode in const.FB_NO_ARENA_CROSS_SERVER_MODES


def isCrossServerBattleField(fbNo):
    return fbNo in const.FB_NO_CROSS_BATTLE_FIELD_RES + const.FB_NO_CROSS_BATTLE_FIELD_FLAG + const.FB_NO_CROSS_BATTLE_FIELD_FORT + const.FB_NO_CROSS_BATTLE_FIELD_HOOK + const.FB_NO_CROSS_BATTLE_FIELD_HUNT + const.FB_NO_CROSS_BATTLE_FIELD_DOTA + const.FB_NO_CROSS_BATTLE_FIELD_CQZZ + const.FB_NO_CROSS_BATTLE_FIELD_RACE + const.FB_NO_CROSS_BATTLE_FIELD_NEW_FLAG + const.FB_NO_CROSS_BATTLE_FIELD_CHAOS_FLAG + [const.FB_NO_BATTLE_FIELD_PUBG, const.FB_NO_BATTLE_FIELD_TIMING_PUBG, const.FB_NO_BATTLE_FIELD_CROSS_WYSL] + const.FB_NO_CROSS_BATTLE_FIELD_LZS


def isCrossServerGuildTournament(fbNo):
    return fbNo in const.FB_NO_CROSS_GTN_BATTLE_FIELD_FORT


def isCrossServerML(mlgNo):
    return mlgNo in const.CROSS_ML_GRUOP_NO


def isWingWorldCrossServerML(mlgNo):
    return mlgNo in const.WIGN_WORLD_CROSS_ML_GROUP_NO


def isDoubleArenaCrossServerML(mlgNo):
    return mlgNo in const.CROSS_DOUBLE_ARENA_ML_GROUP_NO


def isPlayoffsArenaCrossServerML(mlgNo):
    return mlgNo in const.CROSS_BALANCE_PLAYOFFS_ML_GROUP_NO


def isBalanceArenaCrossServerML(mlgNo):
    return mlgNo in const.CROSS_BALANCE_ARENA_ML_GROUP_NO


def isInBalanceReadyRoom(spaceNo):
    return isBalanceArenaCrossServerML(getMLGNo(spaceNo))


def isGroupValidMultiLine(spaceNo):
    return getMLGNo(spaceNo) in const.CROSS_ML_GROUP_VALID


def isCrackSpaceML(mlgNo):
    return mlgNo in const.CRACK_SPACE_ML_GROUP_NO


def isInCrackSpace(spaceNo):
    return isCrackSpaceML(getMLGNo(spaceNo))


def getMlNoByArenaMode(arenaMode):
    if arenaMode == const.ARENA_MODE_CROSS_MS_ROUND_3V3_PRACTISE_BALANCE:
        return const.ML_SPACE_NO_JJC_READY_HOUSE_FLOOR1
    if arenaMode == const.ARENA_MODE_CROSS_MS_ROUND_3V3_PRACTISE_BALANCE_LX:
        return const.ML_SPACE_NO_JJC_READY_HOUSE_FLOOR1
    if arenaMode == const.ARENA_MODE_CROSS_MS_ROUND_3V3_SCORE:
        return const.ML_GROUP_NO_ARENA_SCORE_READY_HOUSE_FLOOR1
    if arenaMode == const.ARENA_MODE_CROSS_MS_ROUND_2V2_DOUBLE_ARENA:
        return const.ML_SPACE_NO_DOUBLE_ARENA_READY_HOUSE_FLOOR1
    if arenaMode == const.ARENA_MODE_CROSS_MS_ROUND_2V2_DOUBLE_ARENA_PLAYOFF:
        return const.ML_SPACE_NO_DOUBLE_ARENA_READY_HOUSE_FLOOR1
    if arenaMode == const.ARENA_MODE_CROSS_MS_ROUND_3V3_BALANCE_GROUP:
        return const.ML_GROUP_NO_ARENA_SCORE_READY_HOUSE_FLOOR1
    if arenaMode == const.ARENA_MODE_CROSS_MS_ROUND_3V3_BALANCE_FINAL:
        return const.ML_GROUP_NO_ARENA_SCORE_READY_HOUSE_FLOOR1


def arenaMode2TeamType(arenaMode):
    if arenaMode == const.ARENA_MODE_CROSS_MS_ROUND_3V3_SCORE:
        return const.ARENA_SCORE_TYPE_1
    return 0


def arenaScoreName(teamType):
    return const.ARENA_SCORE_TYPE_NAME.get(teamType, '')


def arenaScoreNum(teamType):
    return const.ARENA_SCORE_MEMBER_NUM.get(teamType, 0)


def arenaScoreMaxNum(teamType):
    return const.ARENA_SCORE_MEMBER_MAX_NUM.get(teamType) or arenaScoreName(teamType)


def isGuildTournament(fbNo):
    return fbNo in const.FB_NO_GUILD_TOURNAMENT


def isNativeGuildTournament(fbNo):
    return fbNo in const.FB_NO_NATIVE_GTN_BATTLE_FIELD_FORT


def isRankGuildTournament(fbNo):
    return fbNo in const.FB_NO_RANK_GTN_BATTLE_FIELD_FORT


def isEnableNativeGtLive(fbNo):
    return fbNo in const.FB_NO_NATIVE_GTN_BATTLE_FIELD_FORT and gameconfig.enableGuildTournamentLiveAndInspire()


def isSoulOutGoalWithGroupInfo(goal):
    return goal in gametypes.SOUL_OUT_GOALS_NEED_WITH_GROUP_INFO


def isCrossServerFbNo(fbNo):
    return fbNo in const.FB_NO_CROSS_SERVER


def isCanCrossServerApplyArena(arenaMode):
    return arenaMode in const.ARENA_CAN_CROSS_SERVER_APPLY_MODES


def guildChallengeCamp2Pos(sideIndex, sideOffset):
    return sideIndex * 10 + sideOffset


def guildChallengePos2Camp(posIndex):
    return (posIndex / 10, posIndex % 10)


def getArenaLvByMode(mode):
    minLv = const.MAX_LEVEL
    maxLv = 0
    lv = AMD.data.get(mode, {}).get('lv', ())
    for tmpMinLv, tmpMaxLv in lv:
        if tmpMaxLv > maxLv:
            maxLv = tmpMaxLv
        if tmpMinLv < minLv:
            minLv = tmpMinLv

    return (minLv, maxLv)


def getArenaLvTag(mode, lv):
    index = 0
    limitLv = AMD.data.get(mode, {}).get('lv', ())
    for tmpMinLv, tmpMaxLv in limitLv:
        if lv >= tmpMinLv and lv <= tmpMaxLv:
            return index
        index += 1

    return -1


def calcArenaLv(mode, lv):
    index = getArenaLvTag(mode, lv)
    if index == -1:
        return 0
    arenaLvList = AMD.data.get(mode, {}).get('arenaLv', ())
    if index >= len(arenaLvList):
        return 0
    return arenaLvList[index]


def fbNo2BattleFieldMode(fbNo):
    for key, value in const.fbDict.iteritems():
        if key == fbNo:
            return value['mode']

    return const.BATTLE_FIELD_MODE_RES


def getBattleFieldLvReq(key):
    minLv = const.MAX_LEVEL
    maxLv = 0
    fbs = BFMD.data.get(key, {}).get('fbs', [])
    for fbNo in fbs:
        val = BFD.data.get(fbNo, {})
        if not val.get('enableLv', 1):
            continue
        tmpMinLv, tmpMaxLv = val.get('lv', (0, const.MAX_LEVEL))
        if tmpMaxLv > maxLv:
            maxLv = tmpMaxLv
        if tmpMinLv < minLv:
            minLv = tmpMinLv

    return (minLv, maxLv)


def genBattleFieldFbNoByLv(lv, key, enableCrossServerBF = False, isTodayActivity = False):
    fbs = BFMD.data.get(key, {}).get('fbs', [])
    crossFbs = BFMD.data.get(key, {}).get('crossServerFbs', [])
    if enableCrossServerBF:
        fbs = BFMD.data.get(key, {}).get('crossServerFbs', [])
    if isTodayActivity:
        fbs = BFMD.data.get(key, {}).get('todayActivityFbs', [])
    if BigWorld.component in ('base', 'cell'):
        enableCrossServerBF = gameconfig.enableCrossServerBF()
    else:
        import gameglobal
        enableCrossServerBF = gameglobal.rds.configData.get('enableCrossServerBF', False)
    for fbNo in fbs:
        if fbNo in crossFbs and (utils.getBattleFieldRegionInfo(fbNo) == (0, 0, 0) or not enableCrossServerBF):
            continue
        val = BFD.data.get(fbNo, {})
        minLv, maxLv = val.get('lv', (const.MAX_LEVEL, const.MAX_LEVEL))
        if not val.get('enableLv', 1):
            continue
        if val.get('include') and utils.getHostId() not in val.get('include'):
            continue
        if val.get('exclude') and utils.getHostId() in val.get('exclude'):
            continue
        if lv >= minLv and lv <= maxLv:
            return fbNo


def getBattleFieldReliveInterval(fbNo, timePass):
    index = 0
    reliveTime = BFD.data.get(fbNo, {}).get('reliveInterval', [])
    for timeInterval in reliveTime:
        if len(timeInterval) < 2:
            timeMin, timeMax = timeInterval[0], sys.maxint
        else:
            timeMin, timeMax = timeInterval
        if timePass >= timeMin and timePass <= timeMax:
            gamelog.debug('@hjx relive#getBattleFieldReliveInterval:', timeMin, timeMax, timePass)
            return index
        index += 1

    return -1


def inPhaseSpace(spaceNo):
    realSpaceNo = getMapId(spaceNo)
    return realSpaceNo in const.SPACE_PHASE


if BigWorld.component in ('base', 'cell'):
    globalKeyPrefix = '|'.join(gameconst.GLOBAL_KEYS_ALL + tuple(gameconst.BATTLE_FIELD_TEAM_STUB))
    globalKeyPattern = re.compile('^(%s)_(\\d+)(_\\d+)?$' % (globalKeyPrefix,))
    globalKeyPatternEx = re.compile('^(%s)_([A-Za-z0-9]+)(_\\d+)?(_\\d+)?$' % (globalKeyPrefix,))

    def getClsByName(name):
        if globalKeyPattern.match(name):
            prefix, no, _ = globalKeyPattern.findall(name)[0]
            no = int(no)
            if prefix == gameconst.GLOBAL_KEY_PREFIX_ML:
                return const.ML_GROUP_NO_TO_CLASS[no]
            if prefix == gameconst.GLOBAL_KEY_PREFIX_ACTIVITY:
                activityType = whatActivityType(no)
                activityCls = whatActivityCls(activityType)
                return activityCls
            if prefix == gameconst.GLOBAL_KEY_PREFIX_FB:
                return whatFubenCls(no)
            if prefix == gameconst.GLOBAL_KEY_PREFIX_VEHICLE:
                pass
            else:
                if prefix == gameconst.GLOBAL_KEY_PREFIX_WAREA:
                    return 'WorldAreaManager'
                if prefix == gameconst.GLOBAL_KEY_PREFIX_FB_STAT:
                    return 'GroupFbStatShard'
                if prefix in gameconst.BATTLE_FIELD_TEAM_STUB:
                    return prefix
                if prefix == gameconst.GLOBAL_KEY_PREFIX_GUILD_TOURNAMENT:
                    return 'GuildTournament'
                if prefix == gameconst.GLOBAL_KEY_PREFIX_CROSS_GUILD_TOURNAMENT:
                    return 'CrossGuildTournament'
                if prefix == gameconst.GLOBAL_KEY_PREFIX_CROSS_WORLD_WAR:
                    return 'CrossWorldWar'
                if prefix == gameconst.GLOBAL_KEY_PREFIX_WORLD_WAR_MGR:
                    return 'WorldWarMgr'
                if prefix == gameconst.GLOBAL_KEY_PREFIX_CROSS_ARENA_PLAYOFFS:
                    return 'CrossArenaPlayoffsDuelStub'
                if prefix == gameconst.PREFIX_PERSONAL_STUB_PREFIX:
                    return 'PersonalZoneStub'
                if prefix == gameconst.CHAT_GROUP_STUB_PREFIX:
                    return 'ChatGroupStub'
                if prefix == gameconst.GLOBAL_KEY_PREFIX_DYNAMIC_SHOP_STUB:
                    return 'DynamicShopStub'
                if prefix == gameconst.GLOBAL_KEY_PREFIX_WING_WORLD_MGR:
                    return 'WingWorldGlobalStub'
                if prefix == gameconst.GLOBAL_KEY_PREFIX_WING_WORLD_XINMO:
                    return 'WingWorldXinMoStub'
                if prefix == gameconst.GLOBAL_KEY_PREFIX_PROPERTY_CACHE_STUB:
                    return 'PropertyCacheStub'
                if prefix == gameconst.GLOBAL_KEY_PREFIX_WING_WORLD_CAMP:
                    return 'CrossWingWorldCampStub'
                if prefix == gameconst.GLOBAL_KEY_PREFIX_WING_WORLD_CONTRI_TOP:
                    return 'WWPContriTopRank'
                if prefix == gameconst.GLOBAL_KEY_PREFIX_WING_WORLD_GUILD_CONTRI_TOP:
                    return 'WWGContriTopRank'
                if prefix == gameconst.GLOBAL_KEY_PREFIX_NEW_GUILD_TOURNAMENT:
                    return 'NewGuildTournament'
        elif globalKeyPatternEx.match(name):
            prefix = globalKeyPatternEx.findall(name)[0][0]
            if prefix == gameconst.GLOBAL_KEY_PREFIX_CROSS_ARENA_PLAYOFFS:
                return 'CrossArenaPlayoffsDuelStub'
        return name


def toInterval(sec):
    sec = int(sec)
    day = sec / 86400
    hour = sec % 86400 / 3600
    rest = sec % 3600
    minute = rest / 60
    second = rest % 60
    return (day,
     hour,
     minute,
     second)


def toIntervalDesc(sec):
    day, hour, minute, second = toInterval(sec)
    if day == 0 and hour == 0 and minute == 0 and second == 0:
        return '0秒'
    desc = ''
    if day != 0:
        desc += str(day) + '天'
    if hour != 0:
        desc += str(hour) + '小时'
    if minute != 0:
        if second != 0:
            desc += str(minute) + '分'
        else:
            desc += str(minute) + '分钟'
    if second != 0:
        desc += str(second) + '秒'
    return desc


def toYearDesc(date, detail = 3):
    date = int(date)
    year, month, day, hour, minute, sec = time.localtime(date)[0:6]
    if detail == 1:
        return '%d年%d月%d日' % (year, month, day)
    if detail == 2:
        if sec == 0:
            if minute == 0:
                return '%d时' % (hour,)
            else:
                return '%d时%d分' % (hour, minute)
        return '%d时%d分%d秒' % (hour, minute, sec)
    if detail == 3:
        if sec == 0:
            if minute == 0:
                return '%d年%d月%d日%d时' % (year,
                 month,
                 day,
                 hour)
            else:
                return '%d年%d月%d日%d时%d分' % (year,
                 month,
                 day,
                 hour,
                 minute)
        return '%d年%d月%d日%d时%d分%d秒' % (year,
         month,
         day,
         hour,
         minute,
         sec)
    if detail == 4:
        if minute == 0:
            return '%d年%d月%d日%d时' % (year,
             month,
             day,
             hour)
        else:
            return '%d年%d月%d日%d时%d分' % (year,
             month,
             day,
             hour,
             minute)


def getFloatDayTime(timeFloat = None):
    if not timeFloat:
        if BigWorld.component in ('base', 'cell'):
            timeFloat = time.time()
        else:
            timeFloat = BigWorld.player().getServerTime()
    tplSec = time.gmtime(timeFloat)
    offset = int(datetime.now(defaultTimezone()).utcoffset().total_seconds() / 3600)
    hour = (tplSec[3] + offset) % 24
    minute = tplSec[4]
    second = tplSec[5]
    return float(hour * 60 * 60 + minute * 60 + second + timeFloat - int(timeFloat)) / 3600.0


DEFAULT_XINGJI_TIME_DYA_PERIOD = 4.0
DEFAULT_XINGJI_TIME_SUNRISE_TIME = 2.0

def getXingJiTime(curTime = None):
    if not curTime:
        curTime = getFloatDayTime()
    sunriseTime = SCD.data.get('sunriseTime', DEFAULT_XINGJI_TIME_SUNRISE_TIME)
    dayInterval = SCD.data.get('dayInterval', DEFAULT_XINGJI_TIME_DYA_PERIOD)
    return (float((curTime - sunriseTime) % dayInterval * 24) / dayInterval + 6) % 24


def getSecondsPerXingJiHour():
    dayInterval = SCD.data.get('dayInterval', DEFAULT_XINGJI_TIME_DYA_PERIOD)
    return dayInterval * 3600.0 / 24.0


def getXingJiHourMinute(timeFloat = None):
    if not timeFloat:
        curTime = getXingJiTime()
    else:
        curTime = getXingJiTime(getFloatDayTime(timeFloat))
    hour = int(curTime)
    mintue = int((curTime - hour) * 60)
    return (hour, mintue)


def xingJiTimeIntervalToRealTime(interval):
    return interval * SCD.data.get('dayInterval', DEFAULT_XINGJI_TIME_DYA_PERIOD) * 3600 / 24.0


def xingJiTimeDayPeriod():
    return SCD.data.get('dayInterval', DEFAULT_XINGJI_TIME_DYA_PERIOD) * 3600


def xingJiTimeCronCheckInterval():
    return xingJiTimeDayPeriod() * 0.5 / 24


def getRealTimeToAXingJiMoment(xingJiTime, curTime = None, nextT = +1):
    if not curTime:
        curTime = getFloatDayTime()
    curXingJiTime = getXingJiTime(curTime)
    return xingJiTimeIntervalToRealTime(nextT * (xingJiTime - curXingJiTime) % 24)


def isInXingJiTimeInterval(beginXingJiTime, endXingJiTime, curXingJiTime = None):
    if not curXingJiTime:
        curXingJiTime = getXingJiTime()
    if beginXingJiTime <= endXingJiTime:
        return beginXingJiTime <= curXingJiTime <= endXingJiTime
    else:
        return beginXingJiTime <= curXingJiTime <= 24 or 0 <= curXingJiTime <= endXingJiTime


def isInXingJiTimeIntervals(xingJiTimeIntervals):
    if not xingJiTimeIntervals:
        return False
    flag = False
    curXingjiTime = getXingJiTime()
    for st, ed in xingJiTimeIntervals:
        if isInXingJiTimeInterval(st, ed, curXingjiTime):
            flag = True
            break

    return flag


def calcIntervalNextXingJiWordIdx():
    xingJiHour, xingJiMinute = getXingJiHourMinute()
    if xingJiHour % 2 == 1:
        if xingJiMinute == 0:
            return 0
        else:
            return (60 + (60 - xingJiMinute)) / 60.0
    else:
        return (60 - xingJiMinute) / 60.0


def evalScript(lv, script):
    if not isinstance(script, str):
        return script
    if len(script.strip()) == 0:
        return 0
    return FormularEvalEnv.evaluate(script, {const.FORMULA_SKL_LV: lv})


def isInAreas(p, areas):
    if not areas:
        return True
    for area in areas:
        if isInArea(p, area):
            return True

    return False


def isInArea(p, area):
    if not area or len(area) < 3:
        return True
    for i in range(1, len(area) - 1):
        if isInTriangle(p, area[0], area[i], area[i + 1]):
            return True

    return False


def isInTriangle(p, a, b, c):
    p = Vector2(p.x, p.z)
    a = Vector2(a[0], a[2])
    b = Vector2(b[0], b[2])
    c = Vector2(c[0], c[2])
    return isSameSide(p, a, b, c) and isSameSide(p, b, c, a) and isSameSide(p, c, a, b)


def isSameSide(p, a, b, c):
    ab = Vector2(b.x - a.x, b.y - a.y)
    ac = Vector2(c.x - a.x, c.y - a.y)
    ap = Vector2(p.x - a.x, p.y - a.y)
    v1 = ab.cross2D(ac)
    v2 = ab.cross2D(ap)
    return v1 >= 0 and v2 >= 0 or v1 <= 0 and v2 <= 0


def pitchYawToVector(pitchInRadians, yawInRadians):
    cosPitch = math.cos(pitchInRadians)
    sinPitch = math.sin(-pitchInRadians)
    cosYaw = math.cos(yawInRadians)
    sinYaw = math.sin(yawInRadians)
    x = float(cosPitch * sinYaw)
    y = float(sinPitch)
    z = float(cosPitch * cosYaw)
    return (x, y, z)


def tmpCampRelation(src, tgt, fbNo, compare):
    return tmpCampIdRelation(src.tCamp, tgt.tCamp, fbNo, compare)


def tmpCampIdRelation(srcTmpCamp, targetTmpCamp, fbNo, compare):
    campData = getFbTempCampData(fbNo)
    if not campData:
        return False
    relation = -1
    for data in campData:
        if data['campId'] == srcTmpCamp:
            enemy = data.get('enemy', ())
            if targetTmpCamp in enemy:
                relation = gametypes.RELATION_ENEMY
                break
            neutual = data.get('neutral', ())
            if targetTmpCamp in neutual:
                relation = gametypes.RELATION_NEUTRAL
                break
            hostile = data.get('hostile', ())
            if targetTmpCamp in hostile:
                relation = gametypes.RELATION_HOSTILE
                break
            friendly = data.get('friendly', ())
            if targetTmpCamp in friendly:
                relation = gametypes.RELATION_FRIENDLY
                break

    if relation == -1 and compare == gametypes.RELATION_ENEMY:
        return not srcTmpCamp == targetTmpCamp
    return relation == compare


def getTmpCampIdRelation(srcTmpCamp, targetTmpCamp, fbNo):
    campData = getFbTempCampData(fbNo)
    if not campData:
        if srcTmpCamp == targetTmpCamp:
            return gametypes.RELATION_FRIENDLY
        return gametypes.RELATION_ENEMY
    relation = -1
    for data in campData:
        if data['campId'] == srcTmpCamp:
            enemy = data.get('enemy', ())
            if targetTmpCamp in enemy:
                relation = gametypes.RELATION_ENEMY
                break
            neutual = data.get('neutral', ())
            if targetTmpCamp in neutual:
                relation = gametypes.RELATION_NEUTRAL
                break
            hostile = data.get('hostile', ())
            if targetTmpCamp in hostile:
                relation = gametypes.RELATION_HOSTILE
                break
            friendly = data.get('friendly', ())
            if targetTmpCamp in friendly:
                relation = gametypes.RELATION_FRIENDLY
                break

    if relation == -1:
        if srcTmpCamp == targetTmpCamp:
            return gametypes.RELATION_FRIENDLY
        return gametypes.RELATION_ENEMY
    else:
        return relation


def worldCampIdRelation(src, tgt, campare):
    srcCampId = _calcWorldCampId(src)
    tgtCampId = _calcWorldCampId(tgt)
    return _worldCampIdRelation(srcCampId, tgtCampId, campare)


def _calcWorldCampId(src):
    worldCampId = src.camp * gametypes.WORLD_CAMP_RANGE
    if src.IsAvatar:
        if src.pkPunishTime > 0:
            worldCampId += gametypes.WORLD_CAMP_AVATAR_OFFSET_PK_RED
    elif src.IsMonster:
        campOffset = MD.data.get(src.charType, {}).get('worldCampSubId', 0)
        worldCampId += campOffset
    return worldCampId


def _worldCampIdRelation(srcCampId, tgtCampId, campare):
    relationData = PCD.data.get(srcCampId, {})
    enemy = relationData.get('enemy', ())
    friendly = relationData.get('friendly', ())
    if tgtCampId not in enemy and tgtCampId not in friendly:
        return None
    if campare == gametypes.RELATION_ENEMY:
        if tgtCampId in enemy:
            return True
        else:
            return False
    elif campare == gametypes.RELATION_FRIENDLY:
        if tgtCampId in friendly:
            return True
        else:
            return False
    return False


if BigWorld.component in ('cell', 'client'):

    def inProtect(e):
        import commcalc
        if hasattr(e, 'protectStatus') and commcalc.getSingleBit(e.protectStatus, gametypes.PROTECT_STATUS_TYPE_ALL):
            return True
        return False


if BigWorld.component in ('cell', 'client'):

    def inPVPProtect(e):
        import commcalc
        if hasattr(e, 'protectStatus') and commcalc.getSingleBit(e.protectStatus, gametypes.PROTECT_STATUS_TYPE_PVP):
            return True
        return False


def buildGmJsonResult(result, encoding = utils.defaultEncoding()):
    return str(json.dumps(result, ensure_ascii=False, indent=4, encoding=encoding))


def buildGmcPickleResult(result):
    return cPickle.dumps(result)


def passFbQinggongCheck(fbNo, eventDict, event):
    fbdata = getFubenData(fbNo)
    if not fbdata:
        return True
    limitQinggong = fbdata.get('limitQinggong')
    if not limitQinggong:
        return True
    if event in eventDict.get(limitQinggong, {}):
        return False
    return True


def passFbWingCheck(fbNo):
    fbdata = getFubenData(fbNo)
    if not fbdata:
        return True
    limitWingFly = fbdata.get('limitWingFly')
    if limitWingFly:
        return False
    return True


def whatRealPkStatus(pkStatus, lastPkTime):
    if pkStatus in (const.PK_STATUS_PINK, const.PK_STATUS_RED):
        return pkStatus
    if BigWorld.component in ('base', 'cell'):
        now = utils.getNow()
    elif BigWorld.component == 'client':
        now = BigWorld.player().getServerTime()
    if pkStatus == const.PK_STATUS_WHITE:
        interval = now - lastPkTime
        if interval < const.PK_GREEN_STATUS_LOWER_LIMIT:
            return const.PK_STATUS_WHITE
        elif interval >= const.PK_GREEN_STATUS_LOWER_LIMIT and interval < const.PK_DARK_GREEN_STATUS_LOWER_LIMIT:
            return const.PK_STATUS_GREEN
        else:
            return const.PK_STATUS_DARK_GREEN
    return const.PK_STATUS_WHITE


LIMIT_RIDE = 1
LIMIT_QINGONG_LV = 2
LIMIT_WINGFLY = 3
LIMIT_QIECUO = 4
LIMIT_PK = 5
LIMIT_DIE = 6
LIMIT_PROTECT = 7
LIMIT_USE_SKILL = 8
LIMIT_MONSTER_LUCKY_BONUS = 9
LIMIT_PK_MODE = 10
LIMIT_KEYS = {LIMIT_RIDE: 'limitRide',
 LIMIT_QINGONG_LV: 'limitQinggong',
 LIMIT_WINGFLY: 'limitWingFly',
 LIMIT_QIECUO: 'limitQiecuo',
 LIMIT_PK: 'limitPK',
 LIMIT_DIE: 'limitDie',
 LIMIT_PROTECT: 'limitProtect',
 LIMIT_USE_SKILL: 'limitUseSkill',
 LIMIT_MONSTER_LUCKY_BONUS: 'limitMonsterLuckyBonus',
 LIMIT_PK_MODE: 'limitPKMode'}
ALLOW_MONSTER_LUCKY_BONUS = 1
ALLOW_KEYS = {ALLOW_MONSTER_LUCKY_BONUS: 'allowMonsterLuckyBonus'}

def mapAllow(allowId, mapId):
    mapData = MCD.data.get(mapId)
    if not mapData:
        return False
    if allowId not in ALLOW_KEYS:
        return False
    allowKey = ALLOW_KEYS[allowId]
    if mapData.get(allowKey):
        return True
    return False


def mapLimit(limitId, mapId, limitVal = 1):
    mapData = MCD.data.get(mapId)
    if not mapData:
        return False
    if limitId not in LIMIT_KEYS:
        return False
    limitKey = LIMIT_KEYS[limitId]
    if LIMIT_QINGONG_LV == limitId:
        if limitVal in mapData.get(limitKey, ()):
            return True
    elif LIMIT_PK_MODE == limitId:
        if limitVal in mapData.get(limitKey, ()):
            return True
    elif mapData.get(limitKey, 0) == limitVal:
        return True
    return False


def getMapId(spaceNo):
    if spaceNo < const.ML_SPACE_BORDER:
        return spaceNo
    elif spaceInFbOrDuel(spaceNo):
        return getFubenNo(spaceNo)
    elif spaceInMultiLine(spaceNo):
        return getMLNo(spaceNo)
    elif spaceInGuild(spaceNo):
        return const.GUILD_SCENE_NO
    elif spaceInHomeCommunity(spaceNo):
        return const.HOME_COMMUNITY_SCENE_NO
    elif spaceInHomeFloor(spaceNo):
        return const.HOME_FLOOR_SCENE_NO
    elif spaceInHomeRoom(spaceNo):
        return getHomeRoomMapId(spaceNo)
    elif spaceInHomeEnlargedRoom(spaceNo):
        return getHomeEnlargedRoomMapId(spaceNo)
    elif BigWorld.component == 'client' and spaceInClanWarPhase(spaceNo):
        return const.CLAN_WAR_SPACE_NO
    elif spaceInAnnalReplay(spaceNo):
        return getAnnalFubenNo(spaceNo)
    elif spaceInWingCity(spaceNo):
        return getWingCityMapId(spaceNo)
    else:
        return spaceNo


def getHomeRoomMapId(spaceNo):
    roomType = getHomeRoomTypeBySpaceNo(spaceNo)
    if BigWorld.component in ('base', 'cell') and gameconfig.debugHomeMap() and roomType == 2:
        return const.HOME_ROOM_ENLARGED_SCENE_NO_1_TEST
    return const.HOME_ROOM_TYPE_TO_MAP_ID_DICT[roomType]


def getHomeEnlargedRoomMapId(spaceNo):
    roomType = getHomeEnlargedRoomTypeBySpaceNo(spaceNo)
    return const.HOME_ENLARGED_ROOM_TYPE_TO_MAP_ID_DICT[roomType]


def getNearbyRelivePosForPkPunish(spaceNo, position, direction, owner = None):
    mapData = MCD.data.get(getMapId(spaceNo), {})
    pkPunishRelivePos = mapData.get('pkPunishRelivePos', None)
    if not pkPunishRelivePos:
        return getNearbyRelivePos(spaceNo, position, direction, owner)
    basePoints = pkPunishRelivePos.keys()
    minIdx = 0
    minDist = distance2D(position, basePoints[minIdx])
    for idx, pos in enumerate(basePoints):
        dist = distance2D(position, pos)
        if dist < minDist:
            minIdx = idx
            minDist = dist

    relivePos = pkPunishRelivePos.get(basePoints[minIdx], [])
    resPos = random.choice(relivePos)
    return (spaceNo, resPos, direction)


def getNearbyRelivePos(spaceNo, position, direction, owner = None):
    if owner and inEndlessChallengeSpace(spaceNo) and hasattr(owner, 'MISC_VAR_CPRI') and owner.getCellPrivateMiscProperty(gametypes.MISC_VAR_CPRI_ENDLESS_CHALLENGE_FUBEN_ENTRY, ()):
        position, direction = owner.getCellPrivateMiscProperty(gametypes.MISC_VAR_CPRI_ENDLESS_CHALLENGE_FUBEN_ENTRY, ())
        return (owner.spaceNo, position, direction)
    else:
        mapConfig = MCD.data.get(getMapId(spaceNo), {})
        reliveSpace = mapConfig.get('reliveSpaceNo', 0)
        reliveSpace = spaceNo if reliveSpace == 0 else reliveSpace
        relivePos = mapConfig.get('relivePos')
        reliveDir = mapConfig.get('reliveDir', ((0, 0, 0),))
        if not relivePos:
            return (reliveSpace, position, direction)
        if reliveSpace != spaceNo:
            return (reliveSpace, relivePos[0], reliveDir[0])
        minIdx = 0
        minDist = distance3D(position, relivePos[minIdx])
        for idx, pos in enumerate(relivePos):
            dist = distance3D(position, pos)
            if dist < minDist:
                minIdx = idx
                minDist = dist

        resPos = relivePos[minIdx]
        resDir = reliveDir[minIdx] if len(reliveDir) > minIdx else direction
        return (spaceNo, resPos, resDir)


def getRelivePosInPVPArea(spaceNo, tempCamp):
    mapConfig = MCD.data.get(getMapId(spaceNo), {})
    posDict = mapConfig.get('pvpAreaRelivePos')
    dirDict = mapConfig.get('pvpAreaReliveDir')
    if not posDict or not dirDict:
        return ((0, 0, 0), (0, 0, 0))
    pos = posDict.get(tempCamp, (0, 0, 0))
    dir = dirDict.get(tempCamp, (0, 0, 0))
    return (pos, dir)


def whatSchoolName(school):
    return const.SCHOOL_DICT.get(school, '没门派')


def getConsignStorageFee(durationType, price = 0):
    v = math.ceil(price * float(SCD.data.get('consignStorageFeeRate', 1.0)) / 100)
    v = max(SCD.data.get('consignStorageFeeMin', const.ITEM_CONSIGN_STORAGE_FEE_MIN), v)
    v = min(v, SCD.data.get('consignStorageFeeMax', const.ITEM_CONSIGN_STORAGE_FEE_MAX))
    v = v * SCD.data.get('consignStorageFeeCoef', const.ITEM_CONSIGN_STORAGE_FEE_COEF)[durationType]
    return int(v)


def getConsignIncome(income):
    v = int(income * (1 - SCD.data.get('consignTaxRate', const.ITEM_CONSIGN_TAX_RATE)))
    return max(v, 1)


def getMinBidPrice(basePrice):
    return min(basePrice + const.ITEM_CONSIGN_MAX_ADD_PRICE, int(math.ceil(basePrice * (1 + const.ITEM_CONSIGN_ADD_PRICE_COEF))))


def ceilIntDivide(a, b):
    return a / b + (a % b > 0 and 1 or 0)


def calcValueByFormulaData(fData, vars):
    if not vars:
        return 0
    fId = fData[0]
    if fId == 0:
        value = fData[1]
    else:
        params = fData[1:]
        for i in range(len(params)):
            param = params[i]
            vars['p%d' % (i + 1,)] = param

        value = calcFormulaById(fId, vars)
    return value


def calcFormulaById(fId, vars):
    if not FMD.data.has_key(fId):
        if BigWorld.component in ('base', 'cell'):
            gameengine.reportCritical('wrong formula id: %d' % (fId,))
        else:
            gamelog.error('jbx:wrong formula id: %d' % fId)
        return
    fData = FMD.data[fId]
    func = fData['formula']
    res = func(vars)
    return res


FB_TYPE_ARENA_TDM = []
FB_TYPE_ARENA_ROUND = []
FB_TYPE_FB_GROUP = []
FB_TYPE_FB_SINGLE = []
FB_TYPE_BATTLE_FIELD = []
FB_TYPE_ARENA_LZYD = []

def initFBTypes():
    for fbNo, value in const.fbDict.iteritems():
        tp = whatFubenType(fbNo)
        if tp == const.FB_TYPE_ARENA_TDM:
            FB_TYPE_ARENA_TDM.append(fbNo)
        elif tp == const.FB_TYPE_ARENA_ROUND:
            FB_TYPE_ARENA_ROUND.append(fbNo)
        elif tp == const.FB_TYPE_BATTLE_FIELD_RES:
            FB_TYPE_BATTLE_FIELD.append(fbNo)
        elif tp == const.FB_TYPE_BATTLE_FIELD_FLAG:
            FB_TYPE_BATTLE_FIELD.append(fbNo)
        elif tp == const.FB_TYPE_BATTLE_FIELD_CQZZ:
            FB_TYPE_BATTLE_FIELD.append(fbNo)
        elif tp == const.FB_TYPE_BATTLE_FIELD_NEW_FLAG:
            FB_TYPE_BATTLE_FIELD.append(fbNo)
        elif tp == const.FB_TYPE_BATTLE_FIELD_HOOK:
            FB_TYPE_BATTLE_FIELD.append(fbNo)
        elif tp == const.FB_TYPE_BATTLE_FIELD_HUNT:
            FB_TYPE_BATTLE_FIELD.append(fbNo)
        elif tp == const.FB_TYPE_BATTLE_FIELD_DOTA:
            FB_TYPE_BATTLE_FIELD.append(fbNo)
        elif tp in const.FB_TYPE_SINGLE_SET:
            FB_TYPE_FB_SINGLE.append(fbNo)
        elif tp == const.FB_TYPE_GROUP:
            FB_TYPE_FB_GROUP.append(fbNo)
        elif tp == const.FB_TYPE_ARENA_LZYD:
            FB_TYPE_ARENA_LZYD.append(fbNo)


if BigWorld.component in ('base', 'cell'):
    initFBTypes()

def whatActivityType(activityNo):
    return const.ACTIVITY_DICT[activityNo]['type']


def whatActivityCls(activityType):
    return const.ACTIVITY_TYPE_TO_CLASS[activityType]


def angleToRadian(angle):
    return math.pi * angle / 180.0


def lv2SkillLv(lv):
    return max(1, lv * const.MAX_SKILL_LEVEL / const.MAX_LEVEL)


def lv2SkillLvEx(lv):
    return max(int((lv - 25) / 5), 0)


def calcDeclareWarEffect(v1, v2, segment, segmentValue, base):
    if len(segment) + 1 != len(segmentValue):
        gamelog.error('calcDeclareWarEffect invalid segment', segment, segmentValue)
        return (0, 0)
    elif v1 + v2 < base:
        return (0, 0)
    else:
        a = v1 * 1.0 / (v1 + v2)
        b = v2 * 1.0 / (v1 + v2)
        return (segmentValue[utils.getListIndex(a, segment)], segmentValue[utils.getListIndex(b, segment)])


def getSkillEnhancePart(row, col):
    return row * 10 + col


def getSkillEnhanceType(part):
    tp = part % 10
    if tp in const.SKILL_ENHANCE_LEFT:
        return const.SKILL_ENHANCE_LEFT
    if tp in const.SKILL_ENHANCE_MID:
        return const.SKILL_ENHANCE_MID
    if tp in const.SKILL_ENHANCE_RIGHT:
        return const.SKILL_ENHANCE_RIGHT
    return ()


def calcReducePKPunishTime(pkPunishTime1, pkPunishTime2):
    return max(0, pkPunishTime2 - pkPunishTime1)


def sameSign(a, b):
    if a > 0 and b > 0:
        return True
    if a < 0 and b < 0:
        return True
    if a == 0 and b == 0:
        return True
    return False


def getStrMD5(rawStr):
    return md5.new(rawStr).hexdigest()


def getMonsterClanWarContribute(fame, monsterKills, bossDmg):
    divisor = MCWCD.data.get('dmgDivisor', 1)
    if divisor == 0:
        divisor = 1
    return fame + int(bossDmg / divisor)


def getHomeRoomSpaceRange(roomType):
    begin = const.HOME_ROOM_SPACE_NO_START + roomType * const.HOME_ROOM_SCENE_MULTI_BASE
    end = const.HOME_ROOM_SPACE_NO_START + (roomType + 1) * const.HOME_ROOM_SCENE_MULTI_BASE
    return (begin, end)


def getHomeRoomTypeBySpaceNo(spaceNo):
    return int((spaceNo - const.HOME_ROOM_SPACE_NO_START) / const.HOME_ROOM_SCENE_MULTI_BASE)


def getHomeEnlargedRoomTypeBySpaceNo(spaceNo):
    return int((spaceNo - const.HOME_ENLARGED_ROOM_SPACE_NO_START) / const.HOME_ROOM_SCENE_MULTI_BASE)


holdrand = 0

def getApprenticeTargetPoolBySeed(seed, lv):
    targetIds = []
    for minLv, maxLv in ATLD.data.keys():
        if minLv <= lv <= maxLv:
            targetIds.extend(ATLD.data[minLv, maxLv])

    targetIds.sort()
    setCustomSeed(seed)
    res = customSample(targetIds, min(ANCD.data.get('apprenticeTargetPoolCnt', 6), len(targetIds)))
    return res


def setCustomSeed(seed):
    global holdrand
    holdrand = seed


def customRandom():
    global holdrand
    holdrand = holdrand * 214013L + 2531011L
    return holdrand >> 16 & 32767


def customSample(population, k):
    n = len(population)
    if not 0 <= k <= n:
        raise ValueError('customSample larger than population or is negative')
    if k == n:
        return population
    ret = []
    for i in xrange(0, k):
        r = customRandom()
        ret.append(population.pop(r % n))
        n = n - 1

    return ret


def getRealFbEntityNo(no, spaceNo):
    if no <= 9999:
        fbNo = getFubenNo(spaceNo)
        fedNo = fbNo * 10000 + no
        return fedNo
    else:
        return no


def getSpriteUpgradeRatio(spriteId, upgradeStage):
    """\xbc\xc6\xcb\xe3\xb5\xb1\xc7\xb0\xd3\xa2\xc1\xe9\xbd\xd7\xca\xfd\xb5\xc4\xbd\xf8\xbd\xd7\xbc\xd3\xb3\xc9\xcf\xb5\xca\xfd"""
    upgradeRatio = 0.0
    for i in xrange(1, upgradeStage + 1):
        upgradeRatio += SUD.data.get((spriteId, upgradeStage), {}).get('aptitudeUpgradeAdd', 0)

    return upgradeRatio


def getSpriteAptitudeVal(oriValue, clever, juexing, spriteId = 0, upgradeStage = 0):
    cleverBonusRatio = SCD.data.get('cleverBonusRatio', 0.1)
    juexingBonusRatio = SCD.data.get('juexingBonusRatio', 0.1)
    if not clever:
        cleverBonusRatio = 0.0
    if not juexing:
        juexingBonusRatio = 0.0
    upgradeRatio = 0.0
    if upgradeStage:
        upgradeRatio = getSpriteUpgradeRatio(spriteId, upgradeStage)
    addRatio = (1 + cleverBonusRatio + upgradeRatio) * (1 + juexingBonusRatio)
    return int(round(oriValue * addRatio))


def calcFormulaWithPArg(funcInfo, args, default = None):
    """
    \xb4\xf8\xd3\xd0\xc5\xe4\xb1\xed\xd7\xd4\xb6\xa8\xd2\xe5\xb2\xce\xca\xfd\xb5\xc4\xba\xaf\xca\xfd\xbc\xc6\xcb\xe3
    :param funcInfo: \xb4\xd3\xb1\xed\xd6\xd0\xb6\xc1\xb3\xf6\xb5\xc4tuple\xa3\xac(formulaId, p1, p2, p3, ...)
    :param args: \xb3\xcc\xd0\xf2\xb4\xab\xc8\xeb\xb5\xc4\xb2\xce\xca\xfd\xd7\xd6\xb5\xe4
    :param default: \xc4\xac\xc8\xcf\xb7\xb5\xbb\xd8\xd6\xb5
    :return: \xb7\xb5\xbb\xd8\xb9\xab\xca\xbd\xbc\xc6\xcb\xe3\xbd\xe1\xb9\xfb\xbb\xf2\xc4\xac\xc8\xcf\xb7\xb5\xbb\xd8\xd6\xb5
    """
    fId = funcInfo[0] if len(funcInfo) > 0 else 0
    if fId:
        argDict = {}
        for i in xrange(1, len(funcInfo)):
            argDict['p{0}'.format(i)] = funcInfo[i]

        argDict.update(args)
        return calcFormulaById(fId, argDict)
    return default


def getWingCityInfo(spaceNo):
    cityIds = []
    cityType = getWingCityType(spaceNo)
    groupId = getWingCityGroupId(spaceNo)
    spaceNo = spaceNo % 100
    for cityId, data in WWCTD.data.items():
        if data['spaceNos'][cityType] == spaceNo:
            cityIds.append(cityId)

    return (groupId, cityType, tuple(cityIds))


def getWingCityGroupId(spaceNo):
    cityType = getWingCityType(spaceNo)
    groupId = int((spaceNo - const.WING_CITY_SPACE_START[cityType]) / const.WING_CITY_MAX_ID) + 1
    return groupId


def getWingCityType(spaceNo):
    cityType = const.WING_CITY_TYPE_WAR if spaceNo >= const.WING_CITY_SPACE_START[const.WING_CITY_TYPE_WAR] else const.WING_CITY_TYPE_PEACE
    return cityType


def getWingCitySpaceNo(groupId, cityType, cityId):
    if cityId not in WWCTD.data:
        return -1
    indices = WWCTD.data[cityId].get('spaceNos', ())
    if not indices or cityType not in range(len(indices)):
        return -1
    return WWCTD.data.get(cityId)['spaceNos'][cityType] + const.WING_CITY_SPACE_START[cityType] + (groupId - 1) * const.WING_CITY_MAX_ID


def getWingWorldSoulBossSpaceNo(cfgId):
    from data import wing_soul_boss_data as WSBD
    cfgData = WSBD.data.get(cfgId)
    if not cfgData:
        return -1
    return getWingCitySpaceNo(cfgData.get('age'), const.WING_CITY_TYPE_PEACE, cfgData.get('city'))


def getWingCityId(spaceNo, chunkName):
    _, cityType, cityIds = getWingCityInfo(spaceNo)
    if cityType == const.WING_CITY_TYPE_WAR:
        return cityIds[0]
    elif len(cityIds) == 1:
        return cityIds[0]
    else:
        for cityId in cityIds:
            if chunkName in WWCTD.data.get(cityId, {}).get('cityChunks', ()):
                return cityId

        gamelog.error('@hxm city chunk name error')
        return cityIds[0]


def transToGroupWingCitySpaceNo(spaceNo, assginGroupId):
    groupId = getWingCityGroupId(spaceNo)
    return spaceNo + (assginGroupId - groupId) * const.WING_CITY_MAX_ID


def getFbTempCampData(fbNo):
    if fbNo not in FTCD.data:
        fbNo = SCD.data.get('defaultTempCampFbNo', 1000)
    return FTCD.data.get(fbNo, [])


def inCrossArenaMode(arenaMode, isRaw, fromHostId = 0, tgtHostId = 0):
    if arenaMode in const.ARENA_MODE_CLAN_WAR_CHALLENGE:
        return tgtHostId and tgtHostId != utils.getHostId()
    return isCrossServerArena(arenaMode) and isRaw or isCanCrossServerApplyArena(arenaMode) and utils.getRegionHostId(arenaMode, fromHostId) != utils.getHostId()


def getItemForbidMapType(spaceNo):
    if spaceInWorld(spaceNo):
        mapType = const.ITEM_FORBID_MAP_WORLD
    elif spaceInMultiLine(spaceNo):
        mapType = const.ITEM_FORBID_MAP_TYPE_DIGONG
    elif spaceInGuild(spaceNo):
        mapType = const.ITEM_FORBID_MAP_TYPE_GUILD
    elif spaceInWorldWarEx(spaceNo) or spaceInWingCity(spaceNo):
        mapType = const.ITEM_FORBID_MAP_TYPE_WORLD_WAR
    elif spaceInHome(spaceNo):
        mapType = const.ITEM_FORBID_MAP_TYPE_HOME
    else:
        fbNo = getFubenNo(spaceNo)
        fbType = whatFubenType(fbNo)
        mapType = const.ITEM_FORBID_MAP.get(fbType, -1)
    return mapType


def getPlayoffsSeason(now = None):
    if gameconfigCommon.arenaPlayoffsSeason() != -1:
        return gameconfigCommon.arenaPlayoffsSeason()
    from data import duel_config_data as DCD
    crontab = DCD.data.get('CROSS_ARENA_PLAYOFFS_START_CRONTABS', ('1 0 1 1 * 2019', '1 0 1 4 * 2019', '1 0 1 7 * 2019', '1 0 1 10 * 2019'))
    if not crontab:
        return 0
    season = 4
    for index, crontabStr in enumerate(crontab):
        if not utils.isExpireCrontab(crontabStr, now):
            return season
        season = index + 1

    return season


def getPlayoffsTypeByLvKey(lvKey):
    for playoffsType, lvKeys in gametypes.ARENA_PLAYOFFS_OPEN_LV_KEYS.iteritems():
        if lvKey in lvKeys:
            return playoffsType

    return 0


def getPlayoffsType(time = None):
    arenaSeasonIndex = getPlayoffsSeason(time)
    if arenaSeasonIndex < 1:
        return 0
    from data import duel_config_data as DCD
    return DCD.data.get('CROSS_ARENA_PLAYOFFS_TYPE', (2, 1, 2, 1))[arenaSeasonIndex - 1]


def is3v3Playoffs(time = None):
    return getPlayoffsType(time) == gametypes.ARENA_PLAYOFFS_TYPE_3V3


def isBalancePlayoffs(time = None):
    return getPlayoffsType(time) == gametypes.ARENA_PLAYOFFS_TYPE_BALANCE


def is5v5Playoffs(time = None):
    return getPlayoffsType(time) == gametypes.ARENA_PLAYOFFS_TYPE_5V5


def is5v5PlayoffsLvKey(lvKey):
    return lvKey in (gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_60_69, gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_70_79)


def isOpenPlayoffsType(lvKey, time = None):
    return lvKey in gametypes.ARENA_PLAYOFFS_OPEN_LV_KEYS.get(getPlayoffsType(time), ())


def isArenaScoreOpen():
    if BigWorld.component in ('base', 'cell'):
        return Netease.arenaScoreState.get(const.ARENA_SCORE_TYPE_1, 0) == const.ARENA_SCORE_STATE_START


def getArenaScoreState():
    if BigWorld.component in ('base', 'cell'):
        return Netease.arenaScoreState.get(const.ARENA_SCORE_TYPE_1, 0)


def canBuildArenaScoreTeam(teamType = 1):
    if BigWorld.component in ('base', 'cell'):
        return Netease.arenaScoreState.get(teamType, 0) == const.ARENA_SCORE_STATE_READY


def canBuildArenaPlayoffsTeam(playoffsType, stage = 0, lvKey = ''):
    if BigWorld.component in ('base', 'cell'):
        if not playoffsInPrepareStage(stage):
            return False
        if playoffsType == gametypes.ARENA_PLAYOFFS_TYPE_3V3:
            return stage == gameconst.CROSS_ARENA_PLAYOFFS_STAGE_PREPARE
        if playoffsType == gametypes.ARENA_PLAYOFFS_TYPE_5V5:
            return Netease.playoffsScheduleState.get(lvKey, None) == gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_BUILD
        return False


def playoffsInPrepareStage(stage):
    return stage in (gameconst.CROSS_ARENA_PLAYOFFS_STAGE_DEFAULT, gameconst.CROSS_ARENA_PLAYOFFS_STAGE_PREPARE)


def getArenaTeamNUID(arenaMode, owner):
    if BigWorld.component != 'cell' or not owner:
        return 0
    teamType = arenaMode2TeamType(arenaMode)
    if not teamType:
        return 0
    scoreTeam = owner.arenaScoreTeam.get(teamType)
    if not scoreTeam or not scoreTeam.teamNUID:
        return 0
    return scoreTeam.teamNUID


def getCharTempName(tempId):
    if BigWorld.component == 'base':
        import Netease
        baseCharTemp = Netease.charTempCache.get(tempId)
        return baseCharTemp and baseCharTemp.roleName or ''
    elif BigWorld.component == 'cell':
        import Netease
        cellCharTemp = Netease.charTempCache.get(tempId)
        return cellCharTemp and cellCharTemp.roleName or ''
    else:
        return ''


def getCharTempBasicInfo(tempId):
    if BigWorld.component not in ('base', 'cell'):
        return {}
    import Netease
    charTempInfo = {'tempId': tempId}
    if BigWorld.component == 'base':
        baseCharTemp = Netease.charTempCache.get(tempId)
        if baseCharTemp:
            charTempInfo['roleName'] = baseCharTemp.roleName
            charTempInfo['hostId'] = baseCharTemp.hostId
    elif BigWorld.component == 'cell':
        cellCharTemp = Netease.cellCharTempCache.get(tempId)
        if cellCharTemp:
            charTempInfo['roleName'] = cellCharTemp.roleName
            charTempInfo['hostId'] = cellCharTemp.hostId
    return charTempInfo


def inSchoolTopAnnal(spaceNo):
    if not spaceInAnnalReplay(spaceNo):
        return False
    return getAnnalFubenNo(spaceNo) == const.FB_NO_SCHOOL_TOP_MATCH


PLAYOFFS_SCHEDULE_2_ARENA_SCORE_STATE = {gametypes.CROSS_ARENA_PLAYOFFS_STATE_DEFAULT: const.ARENA_SCORE_STATE_DEFULT,
 gametypes.CROSS_ARENA_PLAYOFFS_STATE_APPLY_END: const.ARENA_SCORE_STATE_MATCH,
 gametypes.CROSS_ARENA_PLAYOFFS_STATE_GROUP_MATCH_RUNNING: const.ARENA_SCORE_STATE_START_PLAYOFFS_64,
 gametypes.CROSS_ARENA_PLAYOFFS_STATE_GROUP_MATCH_FINISHED: const.ARENA_SCORE_STATE_END_PLAYOFFS_64,
 gametypes.CROSS_ARENA_PLAYOFFS_STATE_FINAL_MATCH_RUNNING: const.ARENA_SCORE_STATE_START_PLAYOFFS_16,
 gametypes.CROSS_ARENA_PLAYOFFS_STATE_FINISHED: const.ARENA_SCORE_STATE_END,
 gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_BUILD: const.ARENA_SCORE_STATE_READY,
 gametypes.CROSS_ARENA_PLAYOFFS_STATE_END_BUILD: const.ARENA_SCORE_STATE_END_BUILD,
 gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_VOTE: const.ARENA_SCORE_STATE_START,
 gametypes.CROSS_ARENA_PLAYOFFS_STATE_END_VOTE: const.ARENA_SCORE_STATE_FREEZE}

def ArenaPlayoffs2Score(state):
    if state in PLAYOFFS_SCHEDULE_2_ARENA_SCORE_STATE.keys():
        return PLAYOFFS_SCHEDULE_2_ARENA_SCORE_STATE[state]


def isPlayoffsChampionStatue(lvKey):
    return lvKey in gametypes.ARENA_PLAYOFFS_CHAMPION_STATUE_LV_KEY


def getArenaPunishTime(fbNo):
    if whatFubenType(fbNo) not in (const.FB_TYPE_ARENA_TDM, const.FB_TYPE_ARENA_ROUND, const.FB_TYPE_ARENA_LZYD):
        return 0
    freezeTime = SCD.data.get('arenaExitFreezeEx', {}).get(fbNo2ArenaMode(fbNo), None)
    if freezeTime is None:
        freezeTime = SCD.data.get('arenaExitFreeze', 0)
    return freezeTime


def getTopReward(topKey, rank):
    from cdata import top_reward_data as TRD
    rewardList = TRD.data.get(topKey)
    if rewardList and rank:
        for rewardData in rewardList:
            rankRange = rewardData.get('rankRange', (0, 0))
            if rank >= rankRange[0] and rank <= rankRange[1]:
                return rewardData.get('mailTemplateId', 0)

    return 0


def getGuildFubenState():
    if BigWorld.component in ('base', 'cell'):
        import Netease
        return Netease.guildFubenState


def getGuildFubenTypeByFbNo(fbNo):
    if fbNo == const.FB_NO_GUILD_FUBEN:
        return const.GUILD_FUBEN_TYPE_NORMAL
    elif fbNo == const.FB_NO_GUILD_FUBEN_ELITE:
        return const.GUILD_FUBEN_TYPE_ELITE
    else:
        return 0


def isNormalGuildFuben(fbNo):
    return getGuildFubenTypeByFbNo(fbNo) == const.GUILD_FUBEN_TYPE_NORMAL


def isEliteGuildFuben(fbNo):
    return getGuildFubenTypeByFbNo(fbNo) == const.GUILD_FUBEN_TYPE_ELITE


def isGuildFuben(fbNo):
    return fbNo in const.GUILD_FUBEN_NOS


def getGuildFubenTotalMember(fbNo):
    if gameconfig.enableGuildFubenNoCheck() and not gameconfig.publicServer():
        return 0
    fbTp = getGuildFubenTypeByFbNo(fbNo)
    if fbTp == const.GUILD_FUBEN_TYPE_NORMAL:
        return GCFGD.data.get('guildFubenToalMember', const.GUILD_FUBEN_TOTAL_MEMBER)
    if fbTp == const.GUILD_FUBEN_TYPE_ELITE:
        return GCFGD.data.get('guildFubenEliteToalMember', const.GUILD_FUBEN_ELITE_TOTAL_MEMBER)
    return 0


def getGuildFubenOnlineMember(fbNo):
    if gameconfig.enableGuildFubenNoCheck() and not gameconfig.publicServer():
        return 0
    fbTp = getGuildFubenTypeByFbNo(fbNo)
    if fbTp == const.GUILD_FUBEN_TYPE_NORMAL:
        return GCFGD.data.get('guildFubenOnlineMember', const.GUILD_FUBEN_ONLINE_MEMBER)
    if fbTp == const.GUILD_FUBEN_TYPE_ELITE:
        return GCFGD.data.get('guildFubenEliteOnlineMember', const.GUILD_FUBEN_ELITE_ONLINE_MEMBER)
    return 0


def getGuildFubenWeeklyCnt(fbNo):
    fbTp = getGuildFubenTypeByFbNo(fbNo)
    if fbTp == const.GUILD_FUBEN_TYPE_NORMAL:
        return GCFGD.data.get('guildFubenCountWeek', const.GUILD_FUBEN_COUNT_WEEKLY)
    if fbTp == const.GUILD_FUBEN_TYPE_ELITE:
        return GCFGD.data.get('guildFubenEliteCountWeek', const.GUILD_FUBEN_ELITE_COUNT_WEEKLY)
    return 0


def getGuildFubenMaxMember(fbNo):
    fbTp = getGuildFubenTypeByFbNo(fbNo)
    if fbTp == const.GUILD_FUBEN_TYPE_NORMAL:
        return GCFGD.data.get('guildFubenMaxMember', const.GUILD_FUBEN_MAX_MEMBER)
    if fbTp == const.GUILD_FUBEN_TYPE_ELITE:
        return GCFGD.data.get('guildFubenEliteMaxMember', const.GUILD_FUBEN_ELITE_MAX_MEMBER)
    return 0


def getGuildFubenOpenBindCash(fbNo):
    fbTp = getGuildFubenTypeByFbNo(fbNo)
    if fbTp == const.GUILD_FUBEN_TYPE_NORMAL:
        return GCFGD.data.get('guildFubenConstBindCash', const.GUILD_FUBEN_COST_BIND_CASH)
    if fbTp == const.GUILD_FUBEN_TYPE_ELITE:
        return GCFGD.data.get('guildFubenEliteConstBindCash', const.GUILD_FUBEN_ELITE_COST_BIND_CASH)
    return 0


def getGuildFubenModeName(fbNo):
    fbTp = getGuildFubenTypeByFbNo(fbNo)
    if fbTp == const.GUILD_FUBEN_TYPE_NORMAL:
        return '普通'
    if fbTp == const.GUILD_FUBEN_TYPE_ELITE:
        return '精英'
    return ''


def getWeeklyCrontabStr(weekDay, hour, minute):
    if weekDay < 0 or weekDay > 6:
        return ''
    if hour < 0 or hour > 24:
        return ''
    if minute < 0 or minute > 59:
        return ''
    return const.WEEKLY_CRONTAB_FROMAT % (minute, hour, weekDay)


def getLogSrcByTopType(topType):
    if BigWorld.component in ('base', 'cell'):
        if topType == gametypes.TOP_TYPE_ARENA_SCORES_BALANCE:
            return LSDD.data.LOG_SRC_ARENA_TOP_BALANCE_LOCAL_REWARD
        if topType == gametypes.TOP_TYPE_ARENA_SCORES_GLOBAL_BALANCE:
            return LSDD.data.LOG_SRC_ARENA_TOP_BALANCE_GLOBAL_REWARD
        if topType == gametypes.TOP_TYPE_GUILD_BOSS_FOR_ELITE:
            return LSDD.data.LOG_SRC_GUILD_FUBEN_ELITE_RANK
        if topType == gametypes.TOP_TYPE_NPC_FAVOR:
            return LSDD.data.LOG_SRC_NF_WEEKLY_TOP_REWARD
    return 0


def getArenaPlayoffsNumData(lvKey, argName):
    if lvKey not in gametypes.CROSS_ARENA_PLAYOFFS_LV_KEYS:
        return 0
    if lvKey in const.ARENA_PLAYOFFS_NUM_DATA_MAP:
        return const.ARENA_PLAYOFFS_NUM_DATA_MAP[lvKey].get(argName, 0)
    return const.ARENA_PLAYOFFS_NUM_DATA_MAP['defalut'].get(argName, 0)


def getArenaPlayoffsMinMemberByLvKey(lvKey):
    return getArenaPlayoffsNumData(lvKey, 'minMemberNum')


def getArenaPlayoffsMaxMemberByLvKey(lvKey):
    return getArenaPlayoffsNumData(lvKey, 'maxMemberNum')


def getPlayoffsFinalNumEachGroup(lvKey):
    return getArenaPlayoffsNumData(lvKey, 'groupOut')


def getPlayoffsFinalNeedWinCnt(lvKey):
    from data import duel_config_data as DCD
    playoffsType = utils.arenaPlayoffsKey2playoffsType(lvKey)
    if playoffsType == gametypes.ARENA_PLAYOFFS_TYPE_5V5:
        return DCD.data.get('ARENA_PLAYOFFS_5V5_FINAL_DUEL_NEED_WIN_CNT', 1)
    else:
        return DCD.data.get('ARENA_PLAYOFFS_FINAL_DUEL_NEED_WIN_CNT', 2)


def getPlayoffsFinalNum(lvKey):
    return getArenaPlayoffsNumData(lvKey, 'groupOut') * const.CROSS_ARENA_PLAYOFFS_GROUP_NUM


def getPlayoffsStatuesMLNos(lvKey = None):
    playoffsType = utils.arenaPlayoffsKey2playoffsType(lvKey) if lvKey else getPlayoffsType()
    return const.PLAYOFFS_CHAMPION_ML_NOS_FLOORS_BY_TYPES.get(playoffsType, ())


def getFbsByBattleId(battleId):
    return BFMD.data.get(battleId, {}).get('fbs', [])


def getCrossFbsByBattleId(battleId):
    return BFMD.data.get(battleId, {}).get('crossServerFbs', [])


def getDailyActivityFbsByBattleId(battleId):
    return BFMD.data.get(battleId, {}).get('todayActivityFbs', [])


def getNewFlagFbNoByLv(battleId, lv):
    import formula
    import serverProgress
    from data import duel_config_data as DCD
    fbs = formula.getFbsByBattleId(battleId)
    lvLimits = {}
    for fNo in fbs:
        lvLimits[fNo] = BFD.data.get(fNo, {}).get('lv', (40, 79))

    for eventId, fbNo in DCD.data.get('newFlagServerProgressID', {}).get(battleId, []):
        if not lvLimits.has_key(fbNo):
            continue
        if serverProgress.isMileStoneFinished(eventId) and lvLimits[fbNo][0] <= lv <= lvLimits[fbNo][1]:
            return fbNo

    for fNo in fbs:
        if lvLimits[fNo][0] <= lv <= lvLimits[fNo][1]:
            return fNo

    return 0


def getFbNoByLv(battleId, lv):
    import formula
    fbs = formula.getFbsByBattleId(battleId)
    lvLimits = {}
    for fNo in fbs:
        lvLimits[fNo] = BFD.data.get(fNo, {}).get('lv', (40, 89))

    for fNo in fbs:
        if lvLimits[fNo][0] <= lv <= lvLimits[fNo][1]:
            return fNo

    return 0


def getBattleIdByFbNo(fbNo):
    from data import battle_field_mode_reverse_data as BFMRD
    mode = fbNo2BattleFieldMode(fbNo)
    for battleId in BFMRD.data.get(mode, []):
        if fbNo in getFbsByBattleId(battleId) or fbNo in getCrossFbsByBattleId(battleId) or fbNo in getDailyActivityFbsByBattleId(battleId):
            return battleId

    return 0


def isNewFlagMode(battleId):
    import const
    from data import battle_field_mode_reverse_data as BFMRD
    return battleId in BFMRD.data.get(const.BATTLE_FIELD_MODE_NEW_FLAG, [])


def isNewFlagModeByFb(fbNo):
    battleId = getBattleIdByFbNo(fbNo)
    return isNewFlagMode(battleId)


def isTimingPUBGMode(battleId):
    import const
    from data import battle_field_mode_reverse_data as BFMRD
    return battleId in BFMRD.data.get(const.BATTLE_FIELD_MODE_TIMING_PUBG, [])


def isTimingPUBGModeByFb(fbNo):
    battleId = getBattleIdByFbNo(fbNo)
    return isTimingPUBGMode(battleId)


def hasBindRemovedItem(removedItems):
    for _, _, it in removedItems:
        if it.isForeverBind():
            return True

    return False


def getHieroCrystalComposeCoin(feedCount):
    formulaId = SCD.data.get('hierogramFeedRetCoin', 0)
    return calcFormulaById(formulaId, {'feedCount': feedCount})


def calcCombatScoreType(baseScoreType, coeffType, addScoreTypes, val, op):
    """
    \xcd\xe6\xbc\xd2\xd5\xbd\xc1\xa6\xc7\xf8\xb7\xd6\xa3\xba\xc7\xf8\xb7\xd6\xb3\xf6 pvp\xb9\xa5\xbb\xf7\xd5\xbd\xc1\xa6\xa1\xa2pve\xb9\xa5\xbb\xf7\xd5\xbd\xc1\xa6\xa1\xa2pvp\xb7\xc0\xd3\xf9\xd5\xbd\xc1\xa6\xa1\xa2pve\xb7\xc0\xd3\xf9\xd5\xbd\xc1\xa6\xa3\xa81,2,3,4\xa3\xa9
    :param baseScoreType:\xbb\xf9\xb4\xa1\xd6\xb5[0,0,0,0]
    :param coeffType:\xb7\xd6\xc5\xe4\xc2\xca[0,0,0,0]
    :param addScoreTypes:\xb5\xfe\xbc\xd3\xd6\xb5[[0,0,0,0], [0,0,0,0], ...]
    :param val: x
    :param op: 1:baseScoreType + coeffType * val
     param op: 2: baseScoreType * val
     param op: 3: baseScoreType + addScoreTypes[0] + addScoreTypes[1] + ...
    :return:
    """
    baseScoreType = baseScoreType or [0,
     0,
     0,
     0]
    coeffType = coeffType or [25,
     25,
     25,
     25]
    for i in xrange(len(addScoreTypes)):
        if not addScoreTypes[i]:
            addScoreTypes[i] = [0,
             0,
             0,
             0]

    if op == const.COMBAT_SCORE_TYPE_OP_COEFF:
        baseScoreType = [ x[0] + float(val) * x[1] / 100 for x in zip(baseScoreType, coeffType) ]
    elif op == const.COMBAT_SCORE_TYPE_OP_MUL:
        baseScoreType = [ x * val for x in baseScoreType ]
    elif op == const.COMBAT_SCORE_TYPE_OP_ADD:
        baseScoreType = [ sum(x) for x in zip(baseScoreType, *addScoreTypes) ]
    return baseScoreType


def guideModeNeedInGroup(spaceNo):
    if isInCrackSpace(spaceNo):
        return False
    return True


def getWingWorldCampPower(combatScore):
    return combatScore


def getAdvanceCardEvents(opType):
    cardAdvanceFuncOpenEvents = SCD.data.get('cardAdvanceFuncOpenEvents', {})
    if type(cardAdvanceFuncOpenEvents) in (tuple, list):
        cardAdvanceFuncOpenEvents = {const.CARD_ADVANCE_OPTYPE: cardAdvanceFuncOpenEvents}
    for opTypes, events in cardAdvanceFuncOpenEvents.iteritems():
        if type(opTypes) == int:
            opTypes = (opTypes,)
        if opType not in opTypes:
            continue
        if type(events) == int:
            return (events,)
        return events

    return ()


def inSpriteChallengeFb(fbNo):
    from data import sprite_challenge_config_data as SCCD
    for challengeInfo in SCCD.data.get('spriteChallengeRankInfo', {}).itervalues():
        if fbNo and fbNo == challengeInfo.get('fbNo', 0):
            return True

    return False


def inSpriteChallengeSpace(spaceNo):
    fbNo = getFubenNo(spaceNo)
    return inSpriteChallengeFb(fbNo)


def inPUBG(fbNo):
    return fbNo == const.FB_NO_BATTLE_FIELD_PUBG or fbNo == const.FB_NO_BATTLE_FIELD_TIMING_PUBG


def inTimingPUBG(fbNo):
    return fbNo == const.FB_NO_BATTLE_FIELD_TIMING_PUBG


def inPUBGSpace(spaceNo):
    fbNo = getFubenNo(spaceNo)
    return inPUBG(fbNo)


def inFuxiAiTestSpace(spaceNo):
    fbNo = getFubenNo(spaceNo)
    return fbNo == const.FB_NO_TEST_FUXI_ROB_TEST_1 or fbNo == const.FB_NO_TEST_FUXI_ROB_TEST_2
