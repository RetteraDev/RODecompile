#Embedded file name: /WORKSPACE/data/entities/common/ftbutils.o
import const
import gametypes
from data import ftb_config_data as FCD
from data import ftb_power_config_data as FPCD
from cdata import ftb_power_config_reverse_data as FPCRD

def getShowTaskId(taskId):
    if FPCD.data.has_key(taskId):
        return taskId
    for taskType in gametypes.FTB_TASK_SHOW_SET:
        showIds = FPCRD.data.get(taskType, [])
        for showId in showIds:
            taskRange = FPCD.data.get(showId, {}).get('taskRange')
            if not taskRange:
                continue
            if taskRange[0] <= taskId <= taskRange[1]:
                return showId

    return 0


def isShowTaskId(taskId):
    if FPCD.data.has_key(taskId):
        return FPCD.data.get(taskId, {}).get('taskType', 0) in gametypes.FTB_TASK_SHOW_SET
    for taskType in gametypes.FTB_TASK_SHOW_SET:
        showIds = FPCRD.data.get(taskType, [])
        for showId in showIds:
            taskRange = FPCD.data.get(showId, {}).get('taskRange')
            if not taskRange:
                continue
            if taskRange[0] <= taskId <= taskRange[1]:
                return True

    return False


def getTaskType(taskId):
    taskType = FPCD.data.get(taskId, {}).get('taskType')
    if taskType:
        return taskType
    for taskType in gametypes.FTB_TASK_SHOW_SET:
        showIds = FPCRD.data.get(taskType, [])
        if not showIds or not showIds[0]:
            continue
        taskRange = FPCD.data.get(showIds[0], {}).get('taskRange')
        if not taskRange:
            continue
        if taskRange[0] <= taskId <= taskRange[1]:
            return taskType

    return 0
