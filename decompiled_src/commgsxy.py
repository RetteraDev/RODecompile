#Embedded file name: /WORKSPACE/data/entities/common/commgsxy.o
import BigWorld
import utils
import const
if BigWorld.component in ('base', 'cell'):
    import Netease
from data import digong_clanwar_config_data as DGCWCD
from data import multiline_digong_data as MDD
GLOBAL_SXY_ML_STAGE_PREPARE = 1
GLOBAL_SXY_ML_STAGE_COMBAT = 2
GLOBAL_SXY_ML_STAGE_END = 3

def checkStartWeek():
    gsxyCreateTime = DGCWCD.data.get('gsxyCreateTime', '')
    return utils.getIntervalWeek(utils.getNow(), utils.getPreCrontabTime(gsxyCreateTime)) == 0


def checkTopEndWeek():
    gsxyTopEndTime = DGCWCD.data.get('gsxyTopEndTime', '')
    return utils.getIntervalWeek(utils.getNow(), utils.getPreCrontabTime(gsxyTopEndTime)) == 0


def checkEndWeek():
    gsxyEndTime = DGCWCD.data.get('gsxyEndTime', '')
    return utils.getIntervalWeek(utils.getNow(), utils.getPreCrontabTime(gsxyEndTime)) == 0


def checkInTopWeek():
    gsxyCreateTime = DGCWCD.data.get('gsxyCreateTime', '')
    weekIndex = utils.getIntervalWeek(utils.getNow(), utils.getPreCrontabTime(gsxyCreateTime))
    return 0 <= weekIndex <= 2


def checkInSetMemberPeriod():
    gsxyTopEndTime = DGCWCD.data.get('gsxyTopEndTime', '')
    gsxyEndTime = DGCWCD.data.get('gsxyEndTime', '')
    return utils.inCrontabRange(gsxyTopEndTime, gsxyEndTime)


def checkInAddContribPeriod():
    gsxyCreateTime = DGCWCD.data.get('gsxyActivityCreateTime', '')
    gsxyMLCreateTime = DGCWCD.data.get('gsxyMLCreateTime', '')
    return utils.inCrontabRange(gsxyCreateTime, gsxyMLCreateTime)


def checkInMLPeriod():
    md = MDD.data.get(const.ML_GROUP_NO_GSXY)
    createTime = md.get('createTime', '')
    destroyTime = md.get('destroyTime', '')
    return utils.inCrontabRange(createTime, destroyTime)


def setMLStage(stage):
    Netease.gsxyMLStage = stage
