#Embedded file name: /WORKSPACE/data/entities/common/challengepassportutils.o
import utils
import gametypes
import gamelog
import gameconfigCommon
from cdata import challenge_passport_season_data as CPSD
from data import challenge_passport_target_data as CPTD
from data import challenge_passport_config_data as CPCD
OPTIONAL_TARGET_INIT = 0

def challengePassportIsInNewServerDays(sec = None):
    weekInterval = utils.getIntervalWeek(sec, utils.getServerOpenTime()) if sec else utils.getServerOpenWeeks()
    return weekInterval < CPCD.data.get('challengePassportNewServerWeeks', 0)


def challengePassportIsInNewServerWeek(idx):
    gamelog.debug('@hqx_pass_challengePassportIsInNewServerWeek', idx, utils.getServerOpenWeeks())
    return idx == utils.getServerOpenWeeks()


def challengePassportIsNewServerSeason(season):
    return season == CPCD.data.get('challengePassportNewServerSeasonId', -1)


def challengePassportIsInSeason(season):
    if gameconfigCommon.enableNewServerChallengePassport() and challengePassportIsNewServerSeason(season):
        return challengePassportIsInNewServerDays()
    sData = CPSD.data.get(season, {})
    beginTime, endTime = sData.get('beginTime', 0), sData.get('endTime', 0)
    if not beginTime or not endTime:
        return False
    beginTime, endTime = utils.getTimeSecondFromStr(beginTime), utils.getTimeSecondFromStr(endTime)
    if utils.getNow() < beginTime or utils.getNow() > endTime:
        return False
    if gameconfigCommon.enableNewServerChallengePassport() and challengePassportIsInNewServerDays(beginTime):
        return False
    return True


def challengePassportTargetIsInWeek(season, targetId):
    tType = CPTD.data.get(targetId, {}).get('type', 0)
    if tType not in gametypes.CHALLENGE_PASSPORT_TYPE_WEEK:
        return True
    idx = gametypes.CHALLENGE_PASSPORT_TYPE_WEEK.index(tType)
    if gameconfigCommon.enableNewServerChallengePassport() and challengePassportIsNewServerSeason(season):
        return challengePassportIsInNewServerWeek(idx)
    beginTime = CPSD.data.get(season, {}).get('beginTime', 0)
    if not beginTime:
        return False
    beginTime = utils.getTimeSecondFromStr(beginTime)
    weekSecond = beginTime + idx * gametypes.CHALLENGE_PASSPORT_WEEK_SECOND
    weekSecond = utils.getWeekSecond(weekSecond)
    gamelog.debug('@hqx_pass__challengePassportTargetIsInWeek', targetId, tType, idx, weekSecond, utils.getWeekSecond())
    if weekSecond != utils.getWeekSecond():
        return False
    return True


def challengePassportTargetIsInSeason(season, targetId):
    gamelog.debug('@hqx_pass__challengePassportTargetIsInSeason', targetId)
    seasons = CPTD.data.get(targetId, {}).get('season', [])
    if season not in seasons:
        return False
    return True


def challengePassportMaxLv(season):
    if gameconfigCommon.enableNewServerChallengePassport() and challengePassportIsNewServerSeason(season):
        return CPCD.data.get('challengePassportNewServerMaxLv', 100)
    else:
        return CPCD.data.get('challengePassportMaxLv', 100)
