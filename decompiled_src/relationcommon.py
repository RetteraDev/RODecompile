#Embedded file name: /WORKSPACE/data/entities/common/relationcommon.o
import utils
import gametypes
import formula
import const
import commcalc
import gameconfigCommon
import assassinationUtils
from gameChunk import resideInSafetyZone
import BigWorld
from cdata import pk_relation_data as PRD
from data import map_config_data as MCD
from data import zaiju_data as ZD
from cdata import world_camp_data as WCD
if BigWorld.component in ('base', 'cell'):
    import Netease
    import gameengine
    import gameconfig
    IN_CLIENT = False
else:
    IN_CLIENT = True
    import gameglobal

def isEnemy_Avatar(src, tgt):
    import commGSXY
    if tgt.IsMonster:
        if _checkCannotBeAtkType(tgt.beAtkType, src):
            return False
        if getattr(tgt, 'isRedGuard', None):
            return False
        if src.inWorldWarEx():
            r = _checkEnemyWorldWar(src, tgt)
            if r != None:
                return r
        else:
            if not src.inFuben() and utils.isOccupied(tgt) and not utils.hasOccupiedRelation(src, tgt) and not utils.occupiedSame(src, tgt):
                return False
            if src.inMLYaoLiSpace():
                r = _checkYaoLiEnemy(src, tgt)
                if r != None:
                    return r
            elif src.inFuben():
                r = _checkEnemyInFuben(src, tgt)
                if r != None:
                    return r
            elif src.inWingCity():
                r = _checkEnemyWingCity(src, tgt)
                if r != None:
                    return r
            else:
                if getattr(tgt, 'InClanCourier', False):
                    if hasattr(src, 'isClanCourierAvatar') and src.isClanCourierAvatar():
                        return getattr(tgt, 'IsCourierEnemy', False)
                    if getattr(src, 'isJct', False):
                        return not getattr(tgt, 'IsCourierEnemy', False)
                    return False
                if src.inMLSpace(const.ML_GROUP_NO_GSXY):
                    if IN_CLIENT:
                        if src.gsxyMLStage == commGSXY.GLOBAL_SXY_ML_STAGE_PREPARE:
                            return False
                        return True
                    elif Netease.gsxyMLStage == commGSXY.GLOBAL_SXY_ML_STAGE_PREPARE:
                        return False
                    else:
                        return True
                else:
                    r = _checkEnemyPvpTempCamp(src, tgt)
                    if r != None:
                        return r
    else:
        if tgt.IsAvatar or tgt.IsAvatarRobot or tgt.IsPuppet:
            return isEnemy_Avatar_check(src, tgt)
        if tgt.IsFragileObject:
            if src.inFuben():
                if src.tCamp and tgt.tCamp:
                    return formula.tmpCampIdRelation(src.tCamp, tgt.tCamp, formula.getFubenNo(src.spaceNo), gametypes.RELATION_ENEMY)
        elif tgt.IsClanWarUnit:
            if _checkCannotBeAtkType(tgt.beAtkType, src):
                return False
            if IN_CLIENT:
                if src.clanWarStatus:
                    if tgt.guildNUID in src.declareWarGuild:
                        return True
                    elif _checkClanWarStatus_1(src):
                        return not isSameClan(src, tgt)
                    elif src.pkMode in (const.PK_MODE_KILL, const.PK_MODE_HOSTILE) and not isSameClan(src, tgt):
                        return True
                    else:
                        return False
                elif tgt.buildingType != gametypes.CLAN_WAR_BUILDING_RELIVE_BOARD:
                    return False
                elif src.pkMode in (const.PK_MODE_KILL, const.PK_MODE_HOSTILE) and not isSameClan(src, tgt):
                    return True
                else:
                    return False
            elif Netease.clanWarCache.inWar:
                if Netease.declareWarCache.has_key((src.guildNUID, tgt.guildNUID)):
                    return True
                elif _checkClanWarStatus_1(src):
                    return not isSameClan(src, tgt)
                elif src.pkMode in (const.PK_MODE_KILL, const.PK_MODE_HOSTILE) and not isSameClan(src, tgt):
                    return True
                else:
                    return False
            elif tgt.buildingType != gametypes.CLAN_WAR_BUILDING_RELIVE_BOARD:
                return False
            elif src.pkMode in (const.PK_MODE_KILL, const.PK_MODE_HOSTILE) and not isSameClan(src, tgt):
                return True
            else:
                return False
        else:
            if getattr(tgt, 'IsPuppet', None):
                return True
            if hasattr(tgt, 'beAtkType') and _checkCannotBeAtkType(tgt.beAtkType, src):
                return False
            if src.inFuben():
                r = _checkEnemyInFuben(src, tgt)
                if r != None:
                    return r
            if src.inWorldWarEx():
                r = _checkEnemyWorldWar(src, tgt)
                if r != None:
                    return r
            if src.inWingCity():
                r = _checkEnemyWingCity(src, tgt)
                if r != None:
                    return r
            r = _checkEnemyPvpTempCamp(src, tgt)
            if r != None:
                return r
            if getattr(tgt, 'inClanWar', False):
                if IN_CLIENT:
                    if src.clanWarStatus:
                        if src.clanWarStatus and tgt.guildNUID in src.declareWarGuild:
                            return True
                elif Netease.declareWarCache.has_key((src.guildNUID, tgt.guildNUID)):
                    return True
                if _checkClanWarStatus_1(src):
                    return not isSameClan(src, tgt)
    if not hasattr(tgt, 'camp'):
        return False
    return isEnemyRelation(src.camp, tgt.camp)


def isEnemy_Avatar_check(src, tgt):
    newVal = isEnemy_Avatar_new(src, tgt)
    if not IN_CLIENT and gameconfig.enableRelationCheck():
        newRelVal = _getRelation(src, tgt) == gametypes.RELATION_ENEMY
        if not IN_CLIENT and newVal != newRelVal:
            _getRelation2(src, tgt)
            gameengine.reportCritical('is_enemy_avatar check failed! new: %d, newRel: %d, spaceNo: %d, sid: %d, tid: %d' % (newVal,
             newRelVal,
             src.spaceNo,
             src.id,
             tgt.id))
    return newVal


def isEnemy_Avatar_old(src, tgt):
    global _checkAllPkModeEnemy
    if IN_CLIENT:
        if src.clanWarStatus:
            if tgt.IsAvatar and tgt.guildNUID in src.declareWarGuild:
                if not resideInSafetyZone(src) and not resideInSafetyZone(tgt):
                    return True
            if _checkClanWarStatus_2(src, tgt):
                return not isSameClan(src, tgt)
    elif Netease.clanWarCache.inWar and src.inClanWarSpace():
        if Netease.declareWarCache.has_key((src.guildNUID, tgt.guildNUID)):
            if not resideInSafetyZone(src) and not resideInSafetyZone(tgt):
                return True
        if _checkClanWarStatus_2(src, tgt):
            return not isSameClan(src, tgt)
    if src.inMLYaoLiSpace():
        r = _checkYaoLiEnemy(src, tgt)
        if r != None:
            return r
    elif src.inFuben():
        r = _checkEnemyInFuben(src, tgt)
        if r != None:
            return r
    else:
        r = _checkEnemyPvpTempCamp(src, tgt)
        if r != None:
            return r
    return _checkAllPkModeEnemy(src, tgt)


def isEnemy_Avatar_new(src, tgt):
    return getRelation(src, tgt) == gametypes.RELATION_ENEMY


def _getRelation(src, tgt):
    global _checkWorldWarRelation
    spaceNo = src.spaceNo
    if formula.spaceInWorldWarEx(spaceNo):
        r = _checkWorldWarRelation(src, tgt)
        if r != None:
            return r
    elif formula.spaceInWingCity(spaceNo):
        r = _checkWingCityRelation(src, tgt)
        if r != None:
            return r
    else:
        if formula.spaceInWorld(spaceNo):
            if IN_CLIENT:
                if src.clanWarStatus:
                    if tgt.guildNUID in src.declareWarGuild:
                        if not resideInSafetyZone(src) and not resideInSafetyZone(tgt):
                            return gametypes.RELATION_ENEMY
                        else:
                            return gametypes.RELATION_FRIENDLY
                    if _checkClanWarStatus_2(src, tgt):
                        sameClan = isSameClan(src, tgt)
                        if not sameClan:
                            return gametypes.RELATION_ENEMY
                        return gametypes.RELATION_FRIENDLY
                if spaceNo == const.SPACE_NO_BIG_WORLD:
                    group1, group2 = getattr(src, 'groupNUID', 0), getattr(tgt, 'groupNUID', 0)
                    if getattr(tgt, 'isJct', False):
                        if group1 and group2 and group1 == group2:
                            return gametypes.RELATION_FRIENDLY
                        elif hasattr(src, 'isClanCourierAvatar') and src.isClanCourierAvatar():
                            if resideInSafetyZone(src) or resideInSafetyZone(tgt):
                                return gametypes.RELATION_FRIENDLY
                            return gametypes.RELATION_ENEMY
                        else:
                            return gametypes.RELATION_FRIENDLY
                    if hasattr(tgt, 'isClanCourierAvatar') and tgt.isClanCourierAvatar() and hasattr(src, 'isClanCourierAvatar') and src.isClanCourierAvatar():
                        return gametypes.RELATION_FRIENDLY
                    if hasattr(tgt, 'isClanCourierAvatar') and tgt.isClanCourierAvatar() and getattr(src, 'isJct', False):
                        if group1 and group2 and group1 == group2:
                            return gametypes.RELATION_FRIENDLY
                        if resideInSafetyZone(src) or resideInSafetyZone(tgt):
                            return gametypes.RELATION_FRIENDLY
                        return gametypes.RELATION_ENEMY
                    if not (hasattr(tgt, 'isClanCourierAvatar') and tgt.isClanCourierAvatar() or getattr(tgt, 'isJct', False)) and getattr(src, 'isJct', False):
                        return gametypes.RELATION_FRIENDLY
            else:
                if Netease.clanWarCache.inWar and src.inClanWarSpace():
                    if Netease.declareWarCache.has_key((src.guildNUID, tgt.guildNUID)):
                        if not resideInSafetyZone(src) and not resideInSafetyZone(tgt):
                            return gametypes.RELATION_ENEMY
                    if _checkClanWarStatus_2(src, tgt):
                        sameClan = isSameClan(src, tgt)
                        if not sameClan:
                            return gametypes.RELATION_ENEMY
                        return gametypes.RELATION_FRIENDLY
                if spaceNo == const.SPACE_NO_BIG_WORLD:
                    group1, group2 = getattr(src, 'groupNUID', 0), getattr(tgt, 'groupNUID', 0)
                    if getattr(tgt, 'isJct', False):
                        if group1 and group2 and group1 == group2:
                            return gametypes.RELATION_FRIENDLY
                        elif hasattr(src, 'isClanCourierAvatar') and src.isClanCourierAvatar():
                            if resideInSafetyZone(src) or resideInSafetyZone(tgt):
                                return gametypes.RELATION_FRIENDLY
                            return gametypes.RELATION_ENEMY
                        else:
                            return gametypes.RELATION_FRIENDLY
                    if hasattr(tgt, 'isClanCourierAvatar') and tgt.isClanCourierAvatar() and hasattr(src, 'isClanCourierAvatar') and src.isClanCourierAvatar():
                        return gametypes.RELATION_FRIENDLY
                    if hasattr(tgt, 'isClanCourierAvatar') and tgt.isClanCourierAvatar() and getattr(src, 'isJct', False):
                        if group1 and group2 and group1 == group2:
                            return gametypes.RELATION_FRIENDLY
                        if resideInSafetyZone(src) or resideInSafetyZone(tgt):
                            return gametypes.RELATION_FRIENDLY
                        return gametypes.RELATION_ENEMY
                    if not (hasattr(tgt, 'isClanCourierAvatar') and tgt.isClanCourierAvatar() or getattr(tgt, 'isJct', False)) and getattr(src, 'isJct', False):
                        return gametypes.RELATION_FRIENDLY
            if gameconfigCommon.enableAssassination() and getattr(tgt, 'assassinationKillTargetGbId', 0) and tgt.assassinationKillTargetGbId != src.gbId and assassinationUtils.inKillTime(tgt.assassinationKillTargetStamp):
                return gametypes.RELATION_NEUTRAL
            _isEnemy = _checkAllPkModeEnemy(src, tgt)
            if _isEnemy:
                return gametypes.RELATION_ENEMY
            return gametypes.RELATION_FRIENDLY
        if formula.spaceInMultiLine(spaceNo):
            if src.inMLYaoLiSpace():
                r = _checkYaoLiRelation(src, tgt)
                if r != None:
                    return r
            elif src.inMLSpace(const.ML_GROUP_NO_GSXY):
                r = _checkGSXYRelation(src, tgt)
                if r != None:
                    return r
            else:
                r = _checkPvpTempCampRelation(src, tgt)
                if r != None:
                    return r
            _isEnemy = _checkAllPkModeEnemy(src, tgt)
            if _isEnemy:
                return gametypes.RELATION_ENEMY
            return gametypes.RELATION_FRIENDLY
        if formula.spaceInFbOrDuel(spaceNo):
            r = _checkRelationInFuben(src, tgt)
            if r != None:
                return r
            _isEnemy = _checkAllPkModeEnemy(src, tgt)
            if _isEnemy:
                return gametypes.RELATION_ENEMY
            return gametypes.RELATION_FRIENDLY
        _isEnemy = _checkAllPkModeEnemy(src, tgt)
        if _isEnemy:
            return gametypes.RELATION_ENEMY
        return gametypes.RELATION_FRIENDLY


def _getRelation2(src, tgt):
    spaceNo = src.spaceNo
    if formula.spaceInWorldWarEx(spaceNo):
        r = _checkWorldWarRelation(src, tgt)
        if r != None:
            return r
    elif formula.spaceInWingCity(spaceNo):
        r = _checkWingCityRelation(src, tgt)
        if r != None:
            return r
    else:
        if formula.spaceInWorld(spaceNo):
            if IN_CLIENT:
                if src.clanWarStatus:
                    if tgt.guildNUID in src.declareWarGuild:
                        if not resideInSafetyZone(src) and not resideInSafetyZone(tgt):
                            return gametypes.RELATION_ENEMY
                        else:
                            return gametypes.RELATION_FRIENDLY
                    if _checkClanWarStatus_2(src, tgt):
                        sameClan = isSameClan(src, tgt)
                        if not sameClan:
                            return gametypes.RELATION_ENEMY
                        return gametypes.RELATION_FRIENDLY
                if spaceNo == const.SPACE_NO_BIG_WORLD:
                    group1, group2 = getattr(src, 'groupNUID', 0), getattr(tgt, 'groupNUID', 0)
                    if getattr(tgt, 'isJct', False):
                        if group1 and group2 and group1 == group2:
                            return gametypes.RELATION_FRIENDLY
                        elif hasattr(src, 'isClanCourierAvatar') and src.isClanCourierAvatar():
                            if resideInSafetyZone(src) or resideInSafetyZone(tgt):
                                return gametypes.RELATION_FRIENDLY
                            return gametypes.RELATION_ENEMY
                        else:
                            return gametypes.RELATION_FRIENDLY
                    if hasattr(tgt, 'isClanCourierAvatar') and tgt.isClanCourierAvatar() and hasattr(src, 'isClanCourierAvatar') and src.isClanCourierAvatar():
                        return gametypes.RELATION_FRIENDLY
                    if hasattr(tgt, 'isClanCourierAvatar') and tgt.isClanCourierAvatar() and getattr(src, 'isJct', False):
                        if group1 and group2 and group1 == group2:
                            return gametypes.RELATION_FRIENDLY
                        if resideInSafetyZone(src) or resideInSafetyZone(tgt):
                            return gametypes.RELATION_FRIENDLY
                        return gametypes.RELATION_ENEMY
                    if not (hasattr(tgt, 'isClanCourierAvatar') and tgt.isClanCourierAvatar() or getattr(tgt, 'isJct', False)) and getattr(src, 'isJct', False):
                        return gametypes.RELATION_FRIENDLY
            else:
                if Netease.clanWarCache.inWar and src.inClanWarSpace():
                    if Netease.declareWarCache.has_key((src.guildNUID, tgt.guildNUID)):
                        if not resideInSafetyZone(src) and not resideInSafetyZone(tgt):
                            return gametypes.RELATION_ENEMY
                    if _checkClanWarStatus_2(src, tgt):
                        sameClan = isSameClan(src, tgt)
                        if not sameClan:
                            return gametypes.RELATION_ENEMY
                        return gametypes.RELATION_FRIENDLY
                if spaceNo == const.SPACE_NO_BIG_WORLD:
                    group1, group2 = getattr(src, 'groupNUID', 0), getattr(tgt, 'groupNUID', 0)
                    if getattr(tgt, 'isJct', False):
                        if group1 and group2 and group1 == group2:
                            return gametypes.RELATION_FRIENDLY
                        elif hasattr(src, 'isClanCourierAvatar') and src.isClanCourierAvatar():
                            if resideInSafetyZone(src) or resideInSafetyZone(tgt):
                                return gametypes.RELATION_FRIENDLY
                            return gametypes.RELATION_ENEMY
                        else:
                            return gametypes.RELATION_FRIENDLY
                    if hasattr(tgt, 'isClanCourierAvatar') and tgt.isClanCourierAvatar() and hasattr(src, 'isClanCourierAvatar') and src.isClanCourierAvatar():
                        return gametypes.RELATION_FRIENDLY
                    if hasattr(tgt, 'isClanCourierAvatar') and tgt.isClanCourierAvatar() and getattr(src, 'isJct', False):
                        if group1 and group2 and group1 == group2:
                            return gametypes.RELATION_FRIENDLY
                        if resideInSafetyZone(src) or resideInSafetyZone(tgt):
                            return gametypes.RELATION_FRIENDLY
                        return gametypes.RELATION_ENEMY
                    if not (hasattr(tgt, 'isClanCourierAvatar') and tgt.isClanCourierAvatar() or getattr(tgt, 'isJct', False)) and getattr(src, 'isJct', False):
                        return gametypes.RELATION_FRIENDLY
            _isEnemy = _checkAllPkModeEnemy(src, tgt)
            if _isEnemy:
                return gametypes.RELATION_ENEMY
            return gametypes.RELATION_FRIENDLY
        if formula.spaceInMultiLine(spaceNo):
            if src.inMLYaoLiSpace():
                r = _checkYaoLiRelation(src, tgt)
                if r != None:
                    return r
            elif src.inMLSpace(const.ML_GROUP_NO_GSXY):
                r = _checkGSXYRelation(src, tgt)
                if r != None:
                    return r
            else:
                r = _checkPvpTempCampRelation(src, tgt)
                if r != None:
                    return r
            _isEnemy = _checkAllPkModeEnemy(src, tgt)
            if _isEnemy:
                return gametypes.RELATION_ENEMY
            return gametypes.RELATION_FRIENDLY
        if formula.spaceInFbOrDuel(spaceNo):
            r = _checkRelationInFuben(src, tgt)
            if r != None:
                return r
            _isEnemy = _checkAllPkModeEnemy(src, tgt)
            if _isEnemy:
                return gametypes.RELATION_ENEMY
            return gametypes.RELATION_FRIENDLY
        _isEnemy = _checkAllPkModeEnemy(src, tgt)
        if _isEnemy:
            return gametypes.RELATION_ENEMY
        return gametypes.RELATION_FRIENDLY


if BigWorld.component == 'cell':
    Netease.relationCache = {}

    def getRelation(src, tgt):
        ids = (src.id, tgt.id)
        retTuple = Netease.relationCache.get(ids)
        if retTuple:
            srcVer, tgtVer, ret = retTuple
            if srcVer == src.relationVer and tgtVer == tgt.relationVer:
                return ret
        ret = _getRelation(src, tgt)
        Netease.relationCache[ids] = (src.relationVer, tgt.relationVer, ret)
        return ret


elif BigWorld.component == 'client':

    def getRelation(src, tgt):
        return _getRelation(src, tgt)


def isFriend_Avatar(src, tgt):
    import commGSXY
    if tgt.IsMonster or tgt.IsVirtualMonster:
        if src.inWorldWarEx():
            r = _checkFriendWorldWar(src, tgt)
            if r != None:
                return r
        if src.inWingCity():
            r = _checkFriendWingCity(src, tgt)
            if r != None:
                return r
        elif src.inMLYaoLiSpace():
            r = _checkYaoLiFriend(src, tgt)
            if r != None:
                return r
        elif src.inFuben():
            if src.inFubenType(const.FB_TYPE_SHENGSICHANG):
                return False
            if src.inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
                return src.tempCamp == tgt.tempCamp
            if src.inFubenType(const.FB_TYPE_FIGHT_FOR_LOVE):
                if src.tempCamp == const.DEFAULT_CAMP or tgt.tempCamp == const.DEFAULT_CAMP:
                    return True
                elif src.tempCamp == tgt.tempCamp:
                    return True
                else:
                    return False
            if src.tCamp and tgt.tCamp:
                return formula.tmpCampIdRelation(src.tCamp, tgt.tCamp, formula.getFubenNo(src.spaceNo), gametypes.RELATION_FRIENDLY)
        else:
            if getattr(tgt, 'InClanCourier', False):
                if hasattr(src, 'isClanCourierAvatar') and src.isClanCourierAvatar():
                    return not getattr(tgt, 'IsCourierEnemy', False)
                if getattr(src, 'isJct', False):
                    return getattr(tgt, 'IsCourierEnemy', False)
                return True
            if src.inMLSpace(const.ML_GROUP_NO_GSXY):
                if IN_CLIENT:
                    if src.gsxyMLStage == commGSXY.GLOBAL_SXY_ML_STAGE_PREPARE:
                        return False
                    return True
                elif Netease.gsxyMLStage == commGSXY.GLOBAL_SXY_ML_STAGE_PREPARE:
                    return False
                else:
                    return True
            else:
                r = _checkFriendPvpTempCamp(src, tgt)
                if r != None:
                    return r
    else:
        if tgt.IsAvatar or tgt.IsAvatarRobot or tgt.IsPuppet:
            return isFriend_Avatar_check(src, tgt)
        if tgt.IsClanWarUnit:
            return False
        if getattr(tgt, 'IsPuppet', None):
            return False
    if not hasattr(tgt, 'camp'):
        return True
    return isFriendlyRelation(src.camp, tgt.camp)


def isFriend_Avatar_check(src, tgt):
    newVal = isFriend_Avatar_new(src, tgt)
    if not IN_CLIENT and gameconfig.enableRelationCheck():
        newRelVal = _getRelation(src, tgt) == gametypes.RELATION_FRIENDLY
        if not IN_CLIENT and newVal != newRelVal:
            _getRelation2(src, tgt)
            gameengine.reportCritical('is_friend_avatar check failed! new: %d, newRel: %d, spaceNo: %d, sid: %d, tid: %d' % (newVal,
             newRelVal,
             src.spaceNo,
             src.id,
             tgt.id))
    return newVal


def isFriend_Avatar_old(src, tgt):
    if IN_CLIENT:
        if src.clanWarStatus:
            if tgt.guildNUID in src.declareWarGuild:
                return False
            if _checkClanWarStatus_2(src, tgt):
                return isSameClan(src, tgt)
    elif Netease.clanWarCache.inWar and src.inClanWarSpace():
        if Netease.declareWarCache.has_key((src.guildNUID, tgt.guildNUID)):
            return False
        if _checkClanWarStatus_2(src, tgt):
            return isSameClan(src, tgt)
    if src.inMLYaoLiSpace():
        r = _checkYaoLiFriend(src, tgt)
        if r != None:
            return r
    elif src.inFuben():
        if src.inFubenType(const.FB_TYPE_SHENGSICHANG):
            return False
        if src.inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
            return src.tempCamp == tgt.tempCamp
        if src.inFubenType(const.FB_TYPE_FIGHT_FOR_LOVE):
            if src.tempCamp == const.DEFAULT_CAMP or tgt.tempCamp == const.DEFAULT_CAMP:
                return True
            elif src.tempCamp == tgt.tempCamp:
                return True
            else:
                return False
        if src.tCamp and tgt.tCamp:
            return formula.tmpCampIdRelation(src.tCamp, tgt.tCamp, formula.getFubenNo(src.spaceNo), gametypes.RELATION_FRIENDLY)
    else:
        r = _checkFriendPvpTempCamp(src, tgt)
        if r != None:
            return r
    if _checkAllPkModeEnemy(src, tgt):
        return False
    return True


def isFriend_Avatar_new(src, tgt):
    return getRelation(src, tgt) == gametypes.RELATION_FRIENDLY


def isSameGroup(src, tgt):
    if not src.IsAvatar or not tgt.IsAvatar:
        return False
    if not src.groupNUID:
        return False
    return src.groupNUID == tgt.groupNUID


def _checkCannotBeAtkType(beAtkType, src):
    if beAtkType == gametypes.BE_ATK_TYPE_NOBODY or beAtkType == gametypes.BE_ATK_TYPE_MONSTER and src.IsAvatar or beAtkType == gametypes.BE_ATK_TYPE_PLAYER and not src.IsAvatar:
        return True
    else:
        return False


def _checkYaoLiEnemy(src, tgt):
    mlRelation = (mlSpaceForceWithMonster(src), mlSpaceForceWithMonster(tgt))
    if all(mlRelation):
        return False
    elif any(mlRelation):
        return True
    else:
        return None


def _checkYaoLiFriend(src, tgt):
    mlRelation = (mlSpaceForceWithMonster(src), mlSpaceForceWithMonster(tgt))
    if all(mlRelation):
        return True
    elif any(mlRelation):
        return False
    else:
        return None


def _checkYaoLiRelation(src, tgt):
    mlRelation = (mlSpaceForceWithMonster(src), mlSpaceForceWithMonster(tgt))
    if all(mlRelation):
        return gametypes.RELATION_FRIENDLY
    elif any(mlRelation):
        return gametypes.RELATION_ENEMY
    else:
        return None


def _checkGSXYRelation(src, tgt):
    import commGSXY
    if IN_CLIENT:
        if src.gsxyMLStage == commGSXY.GLOBAL_SXY_ML_STAGE_PREPARE:
            return gametypes.RELATION_FRIENDLY
        if src.gsxyMLStage == commGSXY.GLOBAL_SXY_ML_STAGE_COMBAT:
            if src.guildNUID == tgt.guildNUID:
                return gametypes.RELATION_FRIENDLY
            else:
                return gametypes.RELATION_ENEMY
        else:
            return
    else:
        if Netease.gsxyMLStage == commGSXY.GLOBAL_SXY_ML_STAGE_PREPARE:
            return gametypes.RELATION_FRIENDLY
        if Netease.gsxyMLStage == commGSXY.GLOBAL_SXY_ML_STAGE_COMBAT:
            if src.guildNUID == tgt.guildNUID:
                return gametypes.RELATION_FRIENDLY
            else:
                return gametypes.RELATION_ENEMY
        else:
            return


def mlSpaceForceWithMonster(tgt):
    return tgt.IsAvatar and tgt._isInBianyao() or tgt.IsMonster


def _checkPkProtectMode(flags, protectMode):
    if protectMode not in const.ALL_PK_PROTECT_MODE:
        return False
    return commcalc.getBitDword(flags, protectMode) > 0


def _checkYBProtectMode(src, tgt):
    if src._isOnZaiju():
        zaijuNo = src._getZaijuNo()
        zjd = ZD.data[zaijuNo]
        if zjd.get('onlySoulEnemy') and not tgt._isSoul():
            return True
    if tgt._isOnZaiju():
        zaijuNo = tgt._getZaijuNo()
        zjd = ZD.data[zaijuNo]
        if zjd.get('onlySoulEnemy') and not src._isSoul():
            return True
    return False


def _checkRelationInFuben(src, tgt):
    if src.inFubenType(const.FB_TYPE_SHENGSICHANG):
        if src == tgt:
            return gametypes.RELATION_FRIENDLY
        else:
            return gametypes.RELATION_ENEMY
    if src.inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
        if src.tempCamp == tgt.tempCamp:
            return gametypes.RELATION_FRIENDLY
        else:
            return gametypes.RELATION_ENEMY
    if src.inFubenType(const.FB_TYPE_FIGHT_FOR_LOVE):
        if src.tempCamp == const.DEFAULT_CAMP or tgt.tempCamp == const.DEFAULT_CAMP:
            return gametypes.RELATION_FRIENDLY
        elif src.tempCamp == tgt.tempCamp:
            return gametypes.RELATION_FRIENDLY
        else:
            return gametypes.RELATION_ENEMY
    if src.tCamp and tgt.tCamp:
        return formula.getTmpCampIdRelation(src.tCamp, tgt.tCamp, formula.getFubenNo(src.spaceNo))


def _checkEnemyInFuben(src, tgt):
    if src.inFubenType(const.FB_TYPE_SHENGSICHANG):
        return True
    if src.inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
        return src.tempCamp != tgt.tempCamp
    if src.inFubenType(const.FB_TYPE_FIGHT_FOR_LOVE):
        if src.tempCamp == const.DEFAULT_CAMP or tgt.tempCamp == const.DEFAULT_CAMP:
            return False
        elif src.tempCamp == tgt.tempCamp:
            return False
        else:
            return True
    if src.tCamp and tgt.tCamp:
        return formula.tmpCampIdRelation(src.tCamp, tgt.tCamp, formula.getFubenNo(src.spaceNo), gametypes.RELATION_ENEMY)


def _checkEnemyPvpTempCamp(src, tgt):
    mapId = formula.getMapId(src.spaceNo)
    mapData = MCD.data.get(mapId)
    if mapData and mapData.get('usePvpTempCamp'):
        srcCamp = src.pvpTempCamp if src.IsAvatar else getattr(src, 'tempCamp', -1)
        tgtCamp = tgt.pvpTempCamp if tgt.IsAvatar else getattr(tgt, 'tempCamp', -1)
        if srcCamp >= 0 and tgtCamp >= 0:
            return formula.tmpCampIdRelation(srcCamp, tgtCamp, mapId, gametypes.RELATION_ENEMY)


def _checkFriendPvpTempCamp(src, tgt):
    mapId = formula.getMapId(src.spaceNo)
    mapData = MCD.data.get(mapId)
    if mapData and mapData.get('usePvpTempCamp'):
        srcCamp = src.pvpTempCamp if src.IsAvatar else getattr(src, 'tempCamp', -1)
        tgtCamp = tgt.pvpTempCamp if tgt.IsAvatar else getattr(tgt, 'tempCamp', -1)
        if srcCamp >= 0 and tgtCamp >= 0:
            return formula.tmpCampIdRelation(srcCamp, tgtCamp, mapId, gametypes.RELATION_FRIENDLY)


def _checkPvpTempCampRelation(src, tgt):
    mapId = formula.getMapId(src.spaceNo)
    mapData = MCD.data.get(mapId)
    if mapData and mapData.get('usePvpTempCamp'):
        srcCamp = src.pvpTempCamp if src.IsAvatar else getattr(src, 'tempCamp', -1)
        tgtCamp = tgt.pvpTempCamp if tgt.IsAvatar else getattr(tgt, 'tempCamp', -1)
        if srcCamp >= 0 and tgtCamp >= 0:
            return formula.getTmpCampIdRelation(srcCamp, tgtCamp, mapId)


def _checkWorldWarRelation(src, tgt):
    if not src.inWorldWarEx():
        return None
    srcCamp = src.getWorldWarSide() if src.IsAvatar else getattr(src, 'tempCamp', -1)
    tgtCamp = tgt.getWorldWarSide() if tgt.IsAvatar or tgt.IsEmptyZaiju else getattr(tgt, 'tempCamp', -1)
    if srcCamp >= 0 and tgtCamp >= 0:
        if srcCamp == tgtCamp:
            return gametypes.RELATION_FRIENDLY
        return gametypes.RELATION_ENEMY
    else:
        return None


def _checkFriendWorldWar(src, tgt):
    r = _checkWorldWarRelation(src, tgt)
    if r != None:
        return r == gametypes.RELATION_FRIENDLY
    else:
        return


def _checkEnemyWorldWar(src, tgt):
    r = _checkWorldWarRelation(src, tgt)
    if r != None:
        return r == gametypes.RELATION_ENEMY
    else:
        return


def _checkWingCityRelation(src, tgt):
    if not src.inWingCity():
        return None
    elif src.inWingWarCity():
        return _checkWingWarCityRelation(src, tgt)
    else:
        return _checkWingPeaceCityRelation(src, tgt)


def _checkWingPeaceCityRelation(src, tgt):
    if not src.inWingPeaceCity():
        return None
    srcHostId = _getOwnerHostIdInWingCity(src, isWar=False)
    tgtHostId = _getOwnerHostIdInWingCity(tgt, isWar=False)
    if srcHostId >= 0 and tgtHostId >= 0:
        if srcHostId == tgtHostId:
            return gametypes.RELATION_FRIENDLY
        return gametypes.RELATION_ENEMY
    else:
        return None


def _checkWingWarCityRelation(src, tgt):
    if not src.inWingWarCity():
        return None
    srcTempCamp = _getOwnerHostIdInWingCity(src, isWar=True)
    tgtTempCamp = _getOwnerHostIdInWingCity(tgt, isWar=True)
    if srcTempCamp >= 0 and tgtTempCamp >= 0:
        if srcTempCamp == tgtTempCamp:
            return gametypes.RELATION_FRIENDLY
        return gametypes.RELATION_ENEMY
    else:
        return None


def _getOwnerHostIdInWingCity(ent, isWar = False):
    if ent.IsAvatar:
        if commcalc.getBitDword(ent.avatarAllClientFlags, gametypes.AVATAR_ALL_CLIENT_FLAG_WING_GATE_SWITCH):
            return const.WING_WAR_CAMP_GATE_SWITCH
        elif isWar:
            return ent.getCountryId()
        else:
            return ent.getOriginHostId()
    else:
        if ent.IsWingCityWarBuilding:
            return ent.ownerHostId
        if ent.IsVirtualCalcUnit:
            owner = BigWorld.entities.get(ent.ownerId)
            if owner and owner.IsWingCityWarBuilding:
                return owner.ownerHostId
        else:
            if ent.IsWingWorldCarrier:
                return ent.ownerHostId
            if ent.IsEmptyZaiju:
                return ent.wingWorldOwnerHostId
    return const.WING_WAR_CAMP_MONSTER


def _checkFriendWingCity(src, tgt):
    r = _checkWingCityRelation(src, tgt)
    if r != None:
        return r == gametypes.RELATION_FRIENDLY
    else:
        return


def _checkEnemyWingCity(src, tgt):
    r = _checkWingCityRelation(src, tgt)
    if r != None:
        return r == gametypes.RELATION_ENEMY
    else:
        return


def _checkFriendInFuben(src, tgt):
    if src.inFubenType(const.FB_TYPE_SHENGSICHANG):
        return False
    if src.inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
        return src.tempCamp == tgt.tempCamp
    if src.inFubenType(const.FB_TYPE_FIGHT_FOR_LOVE):
        if src.tempCamp == const.DEFAULT_CAMP or tgt.tempCamp == const.DEFAULT_CAMP:
            return True
        elif src.tempCamp == tgt.tempCamp:
            return True
        else:
            return False
    if src.tCamp and tgt.tCamp:
        return formula.tmpCampIdRelation(src.tCamp, tgt.tCamp, formula.getFubenNo(src.spaceNo), gametypes.RELATION_FRIENDLY)


def _checkEnemyInWorld(src, tgt):
    if IN_CLIENT:
        if not gameglobal.rds.configData.get('enableWorldCamp', False):
            return None
    elif not gameconfig.enableWorldCamp():
        return None
    return formula.worldCampIdRelation(src, tgt, gametypes.RELATION_ENEMY)


def checkPkProtect(src, tgt):
    if src.pkMode not in (const.PK_MODE_PEACE,
     const.PK_MODE_DEFENSE,
     const.PK_MODE_KILL,
     const.PK_MODE_POLICE,
     const.PK_MODE_HOSTILE):
        return False
    if _checkPkProtectMode(src.pkProtectMode, const.PK_PROTECT_MODE_GROUP):
        if src.groupNUID != 0 and tgt.groupNUID != 0 and src.groupNUID == tgt.groupNUID:
            return True
    if _checkPkProtectMode(src.pkProtectMode, const.PK_PROTECT_MODE_GUILD):
        if src.guildNUID != 0 and tgt.guildNUID != 0 and src.guildNUID == tgt.guildNUID:
            return True
    if _checkPkProtectMode(src.pkProtectMode, const.PK_PROTECT_MODE_CLAN):
        if src.clanNUID != 0 and tgt.clanNUID != 0 and src.clanNUID == tgt.clanNUID:
            return True
    if _checkPkProtectMode(src.pkProtectMode, const.PK_PROTECT_MODE_GREEN):
        pkStatus = formula.whatRealPkStatus(tgt.pkStatus, tgt.lastPkTime)
        if pkStatus in (const.PK_STATUS_GREEN, const.PK_STATUS_DARK_GREEN):
            return True
    if _checkYBProtectMode(src, tgt):
        return True
    if src.pkProtectLv != 0:
        lvLowerLimit = utils.getLvLimit(src)
        if tgt.lv < lvLowerLimit and tgt.pkStatus in (const.PK_STATUS_RED, const.PK_STATUS_PINK):
            return False
        if tgt.lv < src.pkProtectLv:
            return True
    return False


def isPkEnemy(src, tgt):
    if not src or not tgt or src.id == tgt.id:
        return False
    if resideInSafetyZone(src) or resideInSafetyZone(tgt):
        return False
    mapId = formula.getMapId(src.spaceNo)
    mData = MCD.data.get(mapId)
    if mData and mData.get('limitPk'):
        return False
    if checkPkProtect(src, tgt):
        return False
    if gameconfigCommon.enableAssassination():
        if getattr(tgt, 'assassinationKillTargetGbId', 0) and tgt.assassinationKillTargetGbId != src.gbId and assassinationUtils.inKillTime(tgt.assassinationKillTargetStamp):
            return False
        if getattr(src, 'assassinationKillTargetGbId', 0) and src.assassinationKillTargetGbId != tgt.gbId and assassinationUtils.inKillTime(src.assassinationKillTargetStamp):
            return False
    if src.pkMode == const.PK_MODE_DEFENSE:
        if tgt.gbId not in src.pkDefenseGbIdList:
            if tgt.pkStatus in (const.PK_STATUS_RED, const.PK_STATUS_PINK):
                return commcalc.getBitDword(src.pkProtectMode, const.PK_PROTECT_MODE_WHITE_ATTRACK_RED) > 0
        else:
            return True
    if src.pkMode in (const.PK_MODE_PEACE, const.PK_MODE_DEFENSE) and src.pkStatus == const.PK_STATUS_WHITE and tgt.pkStatus in (const.PK_STATUS_RED, const.PK_STATUS_PINK):
        return commcalc.getBitDword(src.pkProtectMode, const.PK_PROTECT_MODE_WHITE_ATTRACK_RED) > 0
    if src.pkMode == const.PK_MODE_HOSTILE:
        if IN_CLIENT:
            if src.guildNUID and src.guild:
                if tgt.guildNUID and tgt.guildNUID in src.guild.enemyGuildNUIDs:
                    return True
                if tgt.clanNUID and tgt.clanNUID in src.guild.enemyClanNUIDs:
                    return True
        elif Netease.guildPkEnemy.isGuildPkEnemy(src.guildNUID, tgt.guildNUID, tgt.clanNUID):
            return True
    pkData = PRD.data.get((src.pkMode, tgt.pkStatus))
    if pkData == None:
        return False
    return pkData.get('canAtk', 0)


def isQieCuoEnemy(src, target):
    return src.isQieCuoWith(target.id)


def isCampEnemy(src, target):
    if src.crossServerGoal == gametypes.SOUL_OUT_GOAL_BY_NPC_FOR_ACTIVITY and target.crossServerGoal == gametypes.SOUL_OUT_GOAL_BY_NPC_FOR_ACTIVITY:
        return src.camp != target.camp
    return False


def isAssassinationEnemy(src, target):
    if not gameconfigCommon.enableAssassination():
        return False
    if getattr(src, 'assassinationKillTargetGbId', 0) and src.assassinationKillTargetGbId == target.gbId and assassinationUtils.inKillTime(src.assassinationKillTargetStamp):
        return True
    if getattr(target, 'assassinationKillTargetGbId', 0) and target.assassinationKillTargetGbId == src.gbId and assassinationUtils.inKillTime(target.assassinationKillTargetStamp):
        return True
    return False


def _checkAllPkModeEnemy(src, tgt):
    return isPkEnemy(src, tgt) or isQieCuoEnemy(src, tgt) or isCampEnemy(src, tgt) or isAssassinationEnemy(src, tgt)


def isSameClan(src, target):
    return src.guildNUID and src.guildNUID == target.guildNUID or src.clanNUID and src.clanNUID == target.clanNUID


def isEnemyRelation(srcCamp, tgtCamp):
    if BigWorld.component == 'client' and not gameglobal.rds.configData.get('enableNewCampRelation', False):
        return srcCamp != tgtCamp
    if BigWorld.component in ('base', 'cell') and not gameconfig.enableNewCampRelation():
        return srcCamp != tgtCamp
    relationInfo = WCD.data.get(int(srcCamp), {})
    if relationInfo.get(str(tgtCamp), const.CAMP_RELATION_ENEMY) > 0:
        return False
    return True


def isFriendlyRelation(srcCamp, tgtCamp):
    if BigWorld.component == 'client' and not gameglobal.rds.configData.get('enableNewCampRelation', False):
        return srcCamp == tgtCamp
    if BigWorld.component in ('base', 'cell') and not gameconfig.enableNewCampRelation():
        return srcCamp == tgtCamp
    relationInfo = WCD.data.get(int(srcCamp), {})
    if relationInfo.get(str(tgtCamp), const.CAMP_RELATION_ENEMY) == const.CAMP_RELATION_FRIENDLY:
        return True
    return False


_checkWorldWarRelationBak = _checkWorldWarRelation
_checkAllPkModeEnemyBak = _checkAllPkModeEnemy

def _checkWorldWarRelationByCamp(src, tgt):
    if src.IsAvatar and tgt.IsAvatar:
        if src.camp == tgt.camp:
            return gametypes.RELATION_FRIENDLY
        return gametypes.RELATION_ENEMY
    else:
        return _checkWorldWarRelationBak(src, tgt)


def _checkAllPkModeEnemyByCamp(src, tgt):
    if src.IsAvatar and tgt.IsAvatar:
        return src.camp != tgt.camp
    else:
        return _checkAllPkModeEnemyBak(src, tgt)


def switchAvatarRelationByCamp(enable):
    global _checkAllPkModeEnemy
    global _checkWorldWarRelation
    if enable:
        _checkWorldWarRelation = _checkWorldWarRelationByCamp
        _checkAllPkModeEnemy = _checkAllPkModeEnemyByCamp
    else:
        _checkWorldWarRelation = _checkWorldWarRelationBak
        _checkAllPkModeEnemy = _checkAllPkModeEnemyBak


def _checkClanWarStatus_1(ent):
    if ent.inClanWar:
        return True
    if utils.getCommonGameConfig('enableCrossClanWarRelation'):
        if resideInSafetyZone(ent):
            return False
        if ent.IsAvatar and ent.isInCrossClanWarStatus():
            return True
    return False


def _checkClanWarStatus_2(src, tgt):
    if src.inClanWar and tgt.inClanWar:
        return True
    if utils.getCommonGameConfig('enableCrossClanWarRelation'):
        if resideInSafetyZone(src) or resideInSafetyZone(tgt):
            return False
        if src.IsAvatar and src.isInCrossClanWarStatus():
            return True
        if tgt.IsAvatar and tgt.isInCrossClanWarStatus():
            return True
    return False
