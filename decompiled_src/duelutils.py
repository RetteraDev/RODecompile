#Embedded file name: /WORKSPACE/data/entities/common/duelutils.o
import BigWorld
import time
import const
import formula
import gamelog
import gametypes
import utils
from cdata import arena_playoffs_schedule_data as APSD
from data import arena_playoffs_bet_time_data as APBTD
from data import arena_playoffs_5v5_bet_time_data as APBTD5
from data import duel_config_data as DCD
if BigWorld.component in ('base', 'cell'):
    import gameconst
    import gameengine
    import Netease

def getArenaPlayoffsBetTbl(lvKey):
    if formula.is5v5PlayoffsLvKey(lvKey):
        return APBTD5
    else:
        return APBTD


BET_5V5_LVKEY_INDEX_MAP = {gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_60_69: 0,
 gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_70_79: 1}

def getBeLvKeyIndex(lvKey):
    if formula.is5v5PlayoffsLvKey(lvKey):
        return BET_5V5_LVKEY_INDEX_MAP.get(lvKey)
    else:
        return gametypes.CROSS_ARENA_PLAYOFFS_LV_KEYS.index(lvKey)


def getArenaPlayoffsBetCandidate(lvKey, bType, betId):
    PLAYOFFS_BET_TBL = getArenaPlayoffsBetTbl(lvKey)
    return PLAYOFFS_BET_TBL.data.get((bType, betId), {}).get('candidateNum', 0)


def isPlayoffsBetRound(lvKey, isGroup = True, roundNum = 0):
    if isGroup:
        if formula.is5v5PlayoffsLvKey(lvKey):
            return True
        else:
            return roundNum % 2 == 0
    else:
        return True


def getPlayoffsBetId(lvKey, isGroup = True, roundNum = 0):
    PLAYOFFS_BET_TBL = getArenaPlayoffsBetTbl(lvKey)
    duelType = 1 if isGroup else 2
    for (bType, betId), data in PLAYOFFS_BET_TBL.data.iteritems():
        if bType != gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL:
            continue
        if duelType != data.get('duelType', 0):
            continue
        if roundNum in data.get('roundNums', ()):
            return betId

    return 0


def checkArenaMatchSchoolLimit(arenaMode, school, schoolNum, sideNum = 1):
    if arenaMode not in const.ARENA_MODE_3V3:
        return True
    elif school == const.SCHOOL_LINGLONG:
        return schoolNum <= sideNum * const.ARENA_3V3_MAX_LINGLONG_ONE_SIDE
    else:
        return True


LVKEY_2_GLOBAL_AWRAD_TYPE = {gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_1_59: gametypes.GLOBAL_AWARD_TYPE_ARENA_PLAYOFFS_BET,
 gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_60_69: gametypes.GLOBAL_AWARD_TYPE_ARENA_PLAYOFFS_BET_69,
 gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_70_79: gametypes.GLOBAL_AWARD_TYPE_ARENA_PLAYOFFS_BET_79,
 gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_BALANCE: gametypes.GLOBAL_AWARD_TYPE_ARENA_PLAYOFFS_BET,
 gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_60_69: gametypes.GLOBAL_AWARD_TYPE_ARENA_PLAYOFFS_BET_69,
 gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_70_79: gametypes.GLOBAL_AWARD_TYPE_ARENA_PLAYOFFS_BET_79}

def getPlayoffsBetGlobalAwardType(lvKey):
    return LVKEY_2_GLOBAL_AWRAD_TYPE.get(lvKey, 0)


def isArenaSeasonBegining(nowTime = None):
    import utils
    nowTime = utils.getNow() if nowTime is None else nowTime
    st = time.localtime(nowTime)
    if st.tm_hour == 0 and st.tm_min == 0 and st.tm_mday == 1 and st.tm_mon in (1, 4, 7, 10):
        return True
    return False


def calcStartCrontabDayNum(curSeasonIndex):
    if curSeasonIndex == 0:
        return 0
    startCrontab = DCD.data['CROSS_ARENA_PLAYOFFS_START_CRONTABS'][curSeasonIndex - 1]
    timestamp = utils.getDisposableCronTabTimeStamp(startCrontab)
    lTime = time.localtime(timestamp)
    if lTime.tm_wday == 0:
        return 7
    else:
        return 7 + (7 - lTime.tm_wday)


def calcPrepareCrontabDayNum(curSeasonIndex):
    if curSeasonIndex == 0:
        return 0
    startCrontab = DCD.data['CROSS_ARENA_PLAYOFFS_START_CRONTABS'][curSeasonIndex - 1]
    timestamp = utils.getDisposableCronTabTimeStamp(startCrontab)
    lTime = time.localtime(timestamp)
    return 7 - lTime.tm_wday


def getLvKeyIndex(playoffsType):
    for lvKey in gametypes.ARENA_PLAYOFFS_OPEN_LV_KEYS.get(playoffsType, ()):
        if lvKey in gametypes.ARENA_PLAYOFFS_LVKEY_2_SCHEDULE_INDEX.iterkeys():
            return gametypes.ARENA_PLAYOFFS_LVKEY_2_SCHEDULE_INDEX.get(lvKey, {}).get('scheduleIndex', -1)

    return -1


def genArenaPlayoffsCrontabStr(curSeasonIndex, index, playoffsType = None):
    if playoffsType == gametypes.ARENA_PLAYOFFS_TYPE_5V5:
        return _genArenaPlayoffsCrontabStr5v5(curSeasonIndex, index)
    elif playoffsType == gametypes.ARENA_PLAYOFFS_TYPE_BALANCE:
        return _genArenaPlayoffsCrontabStrBalance(curSeasonIndex, index, playoffsType)
    elif not const.CROSS_ARENA_PLAYOFFS_CRONTAB_MAP.has_key(index):
        return ''
    else:
        startCrantabDayNum = calcStartCrontabDayNum(curSeasonIndex)
        if startCrantabDayNum == 0:
            return ''
        startCrontab = DCD.data['CROSS_ARENA_PLAYOFFS_START_CRONTABS'][curSeasonIndex - 1]
        startTime = utils.parseCrontabPatternWithYear(startCrontab)
        rawCrontab = const.CROSS_ARENA_PLAYOFFS_CRONTAB_MAP[index]['crontab']
        offset = const.CROSS_ARENA_PLAYOFFS_CRONTAB_MAP[index]['offset']
        if index == max(const.CROSS_ARENA_PLAYOFFS_CRONTAB_MAP.keys()):
            return rawCrontab % (30, startTime[utils.MONTH][0])
        st = time.localtime(utils.getDisposableCronTabTimeStamp(startCrontab) + (startCrantabDayNum + offset - 1) * const.SECONDS_PER_DAY)
        return rawCrontab % (st.tm_mday, st.tm_mon)


def _genArenaPlayoffsCrontabStrBalance(curSeasonIndex, index, playoffsType):
    if not const.CROSS_ARENA_PLAYOFFS_CRONTAB_MAP.has_key(index):
        return ''
    crontabData = const.CROSS_ARENA_PLAYOFFS_CRONTAB_MAP[index]
    startCrantabDayNum = calcPrepareCrontabDayNum(curSeasonIndex)
    if startCrantabDayNum == 0:
        return ''
    if crontabData.has_key('playoffsType') and playoffsType not in crontabData['playoffsType']:
        return
    startCrontab = DCD.data['CROSS_ARENA_PLAYOFFS_START_CRONTABS'][curSeasonIndex - 1]
    lvKeyIndex = getLvKeyIndex(playoffsType)
    if BigWorld.component in ('base', 'cell'):
        try:
            tblData = APSD.data.get(index)['crontab'][lvKeyIndex] if lvKeyIndex >= 0 else None
            if tblData:
                args = tblData.split(' ')
                rawCrontab = '%d %d' % (int(args[0]), int(args[1])) + ' %d %d *'
            else:
                rawCrontab = crontabData['crontab']
        except Exception as e:
            rawCrontab = crontabData['crontab']
            if BigWorld.component in ('base', 'cell'):
                gameengine.reportCritical('@xjw _genArenaPlayoffsCrontabStrBalance exception %s' % e.message)

    else:
        rawCrontab = crontabData['crontab']
    offset = crontabData['offset']
    if index <= 22:
        offset += 7
    if crontabData.get('configTag'):
        args = [ int(x) for x in startCrontab.split(' ')[:4] ]
        args[0] += 1
        rawCrontab = '%d %d %d %d *' % tuple(args)
        return rawCrontab
    if crontabData.get('startTag'):
        startCrantabDayNum = 1
    if not rawCrontab:
        return ''
    st = time.localtime(utils.getDisposableCronTabTimeStamp(startCrontab) + (startCrantabDayNum + offset - 1) * const.SECONDS_PER_DAY)
    return rawCrontab % (st.tm_mday, st.tm_mon)


def _genArenaPlayoffsCrontabStr5v5(curSeasonIndex, index):
    if not const.CROSS_ARENA_PLAYOFFS_CRONTAB_MAP_EX.has_key(index):
        return ''
    crontabData = const.CROSS_ARENA_PLAYOFFS_CRONTAB_MAP_EX[index]
    startCrantabDayNum = calcPrepareCrontabDayNum(curSeasonIndex)
    if startCrantabDayNum == 0:
        return ''
    if crontabData.has_key('playoffsType') and gametypes.ARENA_PLAYOFFS_TYPE_5V5 not in crontabData['playoffsType']:
        return None
    startCrontab = DCD.data['CROSS_ARENA_PLAYOFFS_START_CRONTABS'][curSeasonIndex - 1]
    if BigWorld.component in ('base', 'cell'):
        try:
            tblData = APSD.data.get(index)['crontab'][4]
            if tblData:
                args = tblData.split(' ')
                rawCrontab = '%d %d' % (int(args[0]), int(args[1])) + ' %d %d *'
            else:
                rawCrontab = crontabData['crontab']
        except Exception as e:
            rawCrontab = crontabData['crontab']
            if BigWorld.component in ('base', 'cell'):
                gameengine.reportCritical('@xjw _genArenaPlayoffsCrontabStr5v5 exception %s' % e.message)

    else:
        rawCrontab = crontabData['crontab']
    offset = crontabData['offset']
    if crontabData.get('configTag'):
        args = [ int(x) for x in startCrontab.split(' ')[:4] ]
        args[0] += 1
        rawCrontab = '%d %d %d %d *' % tuple(args)
        return rawCrontab
    if crontabData.get('startTag'):
        startCrantabDayNum = 1
    st = time.localtime(utils.getDisposableCronTabTimeStamp(startCrontab) + (startCrantabDayNum + offset - 1) * const.SECONDS_PER_DAY)
    return rawCrontab % (st.tm_mday, st.tm_mon)


def genArenaPlayoffsBetCrontabStr(curSeasonIndex, lvKeyIndex, bType, bId, typeStr, lvKey = None):
    if lvKey not in gametypes.CROSS_ARENA_PLAYOFFS_LV_KEYS:
        return ''
    if formula.is5v5PlayoffsLvKey(lvKey):
        return _genArenaPlayoffsBetCrontabStr5v5(curSeasonIndex, lvKeyIndex, bType, bId, typeStr, lvKey)
    if lvKey == gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_BALANCE:
        return _genArenaPlayoffsBalanceCrontabStr(curSeasonIndex, lvKeyIndex, bType, bId, typeStr, lvKey)
    key = (bType, bId)
    if not const.CROSS_ARENA_PLAYOFFS_BET_CRONTAB_MAP.has_key(key):
        return ''
    startCrantabDayNum = calcStartCrontabDayNum(curSeasonIndex)
    if startCrantabDayNum == 0:
        return ''
    startCrontab = DCD.data['CROSS_ARENA_PLAYOFFS_START_CRONTABS'][curSeasonIndex - 1]
    startTime = utils.parseCrontabPatternWithYear(startCrontab)
    rawCrontab = const.CROSS_ARENA_PLAYOFFS_BET_CRONTAB_MAP[key][typeStr][lvKeyIndex]
    offsetStr = ''
    if typeStr == 'crontab':
        offsetStr = 'crontabOffset'
    elif typeStr == 'tBetStart':
        offsetStr = 'startOffset'
    elif typeStr == 'tBetEnd':
        offsetStr = 'endOffset'
    offset = const.CROSS_ARENA_PLAYOFFS_BET_CRONTAB_MAP[key][offsetStr]
    return rawCrontab % (startTime[utils.DAY][0] + startCrantabDayNum + offset - 1, startTime[utils.MONTH][0])


def _genArenaPlayoffsBetCrontabStr5v5(curSeasonIndex, lvKeyIndex, bType, bId, typeStr, lvKey):
    key = (bType, bId)
    if not const.CROSS_ARENA_PLAYOFFS_BET_CRONTAB_MAP_5V5.has_key(key):
        return ''
    startCrantabDayNum = calcPrepareCrontabDayNum(curSeasonIndex)
    if startCrantabDayNum == 0:
        return ''
    startCrontab = DCD.data['CROSS_ARENA_PLAYOFFS_START_CRONTABS'][curSeasonIndex - 1]
    lvKeyIndex = 0 if lvKey == gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_60_69 else 1
    try:
        tblData = const.CROSS_ARENA_PLAYOFFS_BET_CRONTAB_MAP_5V5[key][typeStr]
        args = tblData.split(' ')
        rawCrontab = '%d %d' % (int(args[0]), int(args[1])) + ' %d %d *'
    except Exception as e:
        return ''

    offsetStr = ''
    if typeStr == 'crontab':
        offsetStr = 'crontabOffset'
    elif typeStr == 'tBetStart':
        offsetStr = 'startOffset'
    elif typeStr == 'tBetEnd':
        offsetStr = 'endOffset'
    offset = const.CROSS_ARENA_PLAYOFFS_BET_CRONTAB_MAP_5V5[key][offsetStr]
    st = time.localtime(utils.getDisposableCronTabTimeStamp(startCrontab) + (startCrantabDayNum + offset - 1) * const.SECONDS_PER_DAY)
    return rawCrontab % (st.tm_mday, st.tm_mon)


def _genArenaPlayoffsBalanceCrontabStr(curSeasonIndex, lvKeyIndex, bType, bId, typeStr, lvKey):
    key = (bType, bId)
    if not const.CROSS_ARENA_PLAYOFFS_BET_CRONTAB_MAP_BALANCE.has_key(key):
        return ''
    startCrantabDayNum = calcStartCrontabDayNum(curSeasonIndex)
    if startCrantabDayNum == 0:
        return ''
    startCrontab = DCD.data['CROSS_ARENA_PLAYOFFS_START_CRONTABS'][curSeasonIndex - 1]
    try:
        tblData = const.CROSS_ARENA_PLAYOFFS_BET_CRONTAB_MAP_BALANCE[key][typeStr]
        args = tblData.split(' ')
        rawCrontab = '%d %d' % (int(args[0]), int(args[1])) + ' %d %d *'
    except Exception as e:
        return ''

    offsetStr = ''
    if typeStr == 'crontab':
        offsetStr = 'crontabOffset'
    elif typeStr == 'tBetStart':
        offsetStr = 'startOffset'
    elif typeStr == 'tBetEnd':
        offsetStr = 'endOffset'
    offset = const.CROSS_ARENA_PLAYOFFS_BET_CRONTAB_MAP_BALANCE[key][offsetStr]
    st = time.localtime(utils.getDisposableCronTabTimeStamp(startCrontab) + (startCrantabDayNum + offset - 1) * const.SECONDS_PER_DAY)
    return rawCrontab % (st.tm_mday, st.tm_mon)


def getCrontabIdByPlayoffsState(playoffsType, state):
    lvKeyIndex = getLvKeyIndex(playoffsType)
    for index, val in APSD.data.iteritems():
        try:
            if val.get('state', ())[lvKeyIndex] == state:
                return index
        except Exception as e:
            gamelog.info('xjw## getCrontabIdByPlayoffsState except! ', playoffsType, state, index, e.message)


def getCrontabIdByPlayoffsGroupIdx(playoffsType, gorupIdx):
    lvKeyIndex = getLvKeyIndex(playoffsType)
    state = gametypes.CROSS_ARENA_PLAYOFFS_STATE_GROUP_MATCH_RUNNING
    for index, val in APSD.data.iteritems():
        try:
            if val.get('state', ())[lvKeyIndex] == state and val.get('round', ())[lvKeyIndex] == gorupIdx + 1:
                return index
        except Exception as e:
            gamelog.info('xjw## getCrontabIdByPlayoffsState except! ', playoffsType, state, index, e.message)


def getCrontabIdByPlayoffsFinalIdx(playoffsType, finalIdx):
    lvKeyIndex = getLvKeyIndex(playoffsType)
    state = gametypes.CROSS_ARENA_PLAYOFFS_STATE_FINAL_MATCH_RUNNING
    for index, val in APSD.data.iteritems():
        try:
            if val.get('state', ())[lvKeyIndex] == state and val.get('round', ())[lvKeyIndex] == finalIdx * 3 + 1:
                return index
        except Exception as e:
            gamelog.info('xjw## getCrontabIdByPlayoffsState except! ', playoffsType, state, index, e.message)


LV_KEY_DESC_MAP = {gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_1_59: '69等级段',
 gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_60_69: '69等级段',
 gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_70_79: '79等级段',
 gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_BALANCE: '',
 gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_60_69: '69等级段',
 gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_70_79: '79等级段'}

def getLvKeyDesc(lvKey):
    return LV_KEY_DESC_MAP.get(lvKey, '')


ROUND_DESC_MAP = {1: '8强',
 2: '4强',
 3: '半决赛',
 4: '决赛',
 5: '冠军'}

def getFinalRoundDesc(round):
    return ROUND_DESC_MAP.get(round, '')


ARENA_PLAYOFFS_STAGE_DESC = {1: '收集入选战队',
 2: '小组赛分组',
 3: '小组赛第1轮',
 4: '小组赛第2轮',
 5: '小组赛第3轮',
 6: '小组赛第4轮',
 7: '小组赛第5轮',
 8: '小组赛第6轮',
 9: '小组赛第7轮',
 10: '淘汰赛第1轮',
 11: '淘汰赛第2轮',
 12: '淘汰赛第3轮',
 13: '淘汰赛第4轮',
 14: '淘汰赛第5轮',
 15: '淘汰赛第6轮',
 16: '淘汰赛第7轮',
 17: '淘汰赛第8轮',
 18: '淘汰赛第9轮',
 19: '淘汰赛第10轮',
 20: '淘汰赛第11轮',
 21: '淘汰赛第12轮',
 22: '武道会结束',
 23: '开始组队',
 24: '结束组队',
 25: '开始投票',
 26: '结束投票'}

def getPlayoffsStageDesc(stage):
    return ARENA_PLAYOFFS_STAGE_DESC.get(stage, '')


def getPlayoffsAidAccuRewardTag(playoffsType):
    if BigWorld.component != 'base':
        return False
    lvKeys = gametypes.ARENA_PLAYOFFS_OPEN_LV_KEYS.get(playoffsType)
    if not lvKeys:
        return False
    for lvKey in lvKeys:
        if not Netease.arenaPlayoffsAidAccuReward.get(lvKey, False):
            return False

    return True


def getPlayoffsAidAccuRewardMail(val, limitVal):
    rewardMap = DCD.data.get('arenaPlayoffsAidRewardList')
    if not rewardMap:
        return []
    mailList = []
    for accuVal, mailId in rewardMap.iteritems():
        if limitVal < accuVal <= val:
            mailList.append(mailId)

    return mailList
