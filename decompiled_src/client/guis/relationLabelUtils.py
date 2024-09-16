#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/relationLabelUtils.o
import BigWorld
import sys
import uiUtils
import uiConst
from data import sys_config_data as SCD

def isGuild(gbId):
    return uiUtils.isSameGuild(gbId)


def isFriend(gbId):
    return BigWorld.player().friend.isFriend(gbId)


def isCouple(gbId):
    return uiUtils.isJieQiTgt(gbId)


def isMentor(gbId):
    return uiUtils.isZhenChuanTgt(gbId)


def isPartner(gbId):
    return uiUtils.isPartner(gbId)


def getValidLabelsName(gbId):
    gbId = long(gbId)
    inviteLabels = SCD.data.get('relationLabels', [])
    validLabels = []
    for groupLabel in inviteLabels:
        if len(validLabels) == uiConst.PLAYER_ITEM_MAX_LABEL:
            break
        for labelFuncName in groupLabel:
            func = getattr(sys.modules[__name__], labelFuncName)
            if func(gbId):
                validLabels.append(labelFuncName)
                break

    return validLabels
