#Embedded file name: /WORKSPACE/data/entities/common/assassinationutils.o
import utils
import const
import random
import math
from crontab import CronTab
from cdata import assassination_config_data as ACD
EXTRA_BE_ON_STAMP = 1
EXTRA_OFF_CNT = 2
EXTRA_OFF_STAMP = 3
EXTRA_FASHION_RES = 7
EXTRA_CHANGE_ITEM = 8
EXTRA_ON_CNT = 9
EXTRA_ON_STAMP = 10
EXTRA_RECENT_FROM_ROLENAME = 11
EXTRA_RECENT_FROM_MSG = 12
OFF_BOARD_TIME_OFF = 1
OFF_BOARD_TIME_KILL = 2
OFF_BOARD_FROM_GBID = 3
OFF_BOARD_GBID = 4
OFF_BOARD_TIME_END = 5
OFF_BOARD_END_RESULT = 6
OFF_BOARD_ID = 7
STUB_PROTECT_STAMP = 1
STUB_PROTECT_CNT = 2
ASSASSINATION_KILLER = 1
ASSASSINATION_TARGET = 2
ASSASSINATION_STATE_START = 0
ASSASSINATION_STATE_FAIL = 1
ASSASSINATION_STATE_SUCC = 2
ASSASSINATION_SYNC_LOG_ON = 1
ASSASSINATION_SYNC_ON_BOARD = 2
ASSASSINATION_SYNC_OFF_BOARD = 3
ASSASSINATION_SYNC_KILL_START = 4
ASSASSINATION_SYNC_KILL_END = 5
OFF_BOARD_END_RESULT_FAIL = 0
OFF_BOARD_END_RESULT_SUCC = 1
CURRENT_OFF_BOARD_NONE = 0
CURRENT_OFF_BOARD_FAIL = 1
CURRENT_OFF_BOARD_SUCCESS = 2
CURRENT_OFF_BOARD_NOT_START = 3
CURRENT_OFF_BOARD_KILLING = 4
ASSASSINATION_FAIL_QUEST_EXPIRE = 1
ASSASSINATION_FAIL_BE_KILLED = 2
ASSASSINATION_FAIL_KILL_EXPIRE = 3
ASSASSINATION_ALL_BACK_GM_INTERVAL = 330
ASSASSINATION_MODIFY_ON_BOARD_CNT = 1
ASSASSINATION_MODIFY_OFF_BOARD_CNT = 2
ASSASSINATION_NPC_OFFSET_MIN = 300
ASSASSINATION_NPC_OFFSET_MAX = 600
ASSASSINATION_NPC_OFFSET_BASE = 100
ASSASSINATION_NPC_OFFSET_RADIAN = math.pi / 2.0

def getRandomTombPos(basePos, baseDir):
    randomRadian = random.random() * ASSASSINATION_NPC_OFFSET_RADIAN
    if randomRadian < ASSASSINATION_NPC_OFFSET_RADIAN / 2.0:
        randomRadian = -(ASSASSINATION_NPC_OFFSET_RADIAN / 2.0 - randomRadian)
    else:
        randomRadian = randomRadian - ASSASSINATION_NPC_OFFSET_RADIAN / 2.0
    baseYaw = baseDir[2] - randomRadian
    realDir = (math.sin(baseYaw), 0, math.cos(baseYaw))
    randomDistance = random.randint(ASSASSINATION_NPC_OFFSET_MIN, ASSASSINATION_NPC_OFFSET_MAX) * 1.0 / ASSASSINATION_NPC_OFFSET_BASE
    realDirWithDist = map(lambda x: x * randomDistance, realDir)
    realPos = tuple(map(lambda x: x[0] + x[1], zip(basePos, realDirWithDist)))
    return realPos


def inKillTime(sec):
    return utils.getNow() - sec <= ACD.data.get('assassinationKillTimeLimit', 300)


def inOnBoardTime(sec):
    return utils.getNow() - sec <= ACD.data.get('assassinationTonInterval', const.TIME_INTERVAL_DAY)


def inOffBoardTime(sec):
    return utils.getNow() - sec <= ACD.data.get('assassinationToffInterval', 14400)


def getOffBoardStateByData(offBoard):
    if not offBoard:
        return CURRENT_OFF_BOARD_NONE
    offTime = offBoard.get(OFF_BOARD_TIME_OFF, 0)
    killGbId = offBoard.get(OFF_BOARD_GBID, 0)
    fromGbId = offBoard.get(OFF_BOARD_FROM_GBID, 0)
    tkillTime = 0
    tkillEndTime = 0
    tkillResult = 0
    if OFF_BOARD_TIME_KILL in offBoard:
        tkillTime = offBoard.get(OFF_BOARD_TIME_KILL, 0)
    if OFF_BOARD_TIME_END in offBoard:
        tkillEndTime = offBoard.get(OFF_BOARD_TIME_END, 0)
    if OFF_BOARD_END_RESULT in offBoard:
        tkillResult = offBoard.get(OFF_BOARD_END_RESULT, 0)
    if tkillEndTime != 0:
        if tkillResult == OFF_BOARD_END_RESULT_SUCC:
            return CURRENT_OFF_BOARD_SUCCESS
        if tkillResult == OFF_BOARD_END_RESULT_FAIL:
            return CURRENT_OFF_BOARD_FAIL
    if tkillTime != 0:
        return CURRENT_OFF_BOARD_KILLING
    else:
        return CURRENT_OFF_BOARD_NOT_START


def inProtectTime(sec):
    return utils.getNow() - sec <= ACD.data.get('assassinationProtectionBuffTime', 7200)


def inAbandonTime(sec = None):
    sec = sec or utils.getNow()
    tBegins, tEnds = ACD.data.get('assassinationAbandonBegin'), ACD.data.get('assassinationAbandonEnd')
    if not tBegins or not tEnds or len(tBegins) != len(tEnds):
        return False
    for idx, tBegin in enumerate(tBegins):
        tEnd = tEnds[idx]
        tBegin = CronTab(tBegin)
        tEnd = CronTab(tEnd)
        if tBegin.next(sec) > tEnd.next(sec):
            return True

    return False


def inMaxValidTime(sec):
    tOn = ACD.data.get('assassinationTonInterval', const.TIME_INTERVAL_DAY)
    tOff = ACD.data.get('assassinationToffInterval', 14400)
    tKill = ACD.data.get('assassinationKillTimeLimit', 300)
    return utils.getNow() - sec <= tOn + tOff + tKill
