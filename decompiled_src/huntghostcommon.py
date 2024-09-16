#Embedded file name: /WORKSPACE/data/entities/common/huntghostcommon.o
import BigWorld
import utils
import formula
import gameconfigCommon
if BigWorld.component in ('base', 'cell'):
    import Netease
    import gameconfig
from data import fb_data as FD
from data import hunt_ghost_config_data as HGCD

def onHuntGhostStart():
    if BigWorld.component in ('base', 'cell'):
        Netease.huntGhostIsOpen = True


def onHuntGhostEnd():
    if BigWorld.component in ('base', 'cell'):
        Netease.huntGhostIsOpen = False
        Netease.huntGhostAreas = {}
        Netease.huntGhostGroupAreas = {}
        Netease.bigGhostBoxInfo = {}
        Netease.huntGhostGroups = []


def onSyncHuntGhostAreas(areas, groupPoints, bigGhostBoxInfo):
    if BigWorld.component in ('base', 'cell'):
        Netease.huntGhostAreas = areas
        Netease.huntGhostGroupAreas = groupPoints
        Netease.bigGhostBoxInfo = bigGhostBoxInfo
        Netease.huntGhostGroups = []
        tempGroups = []
        for groupNUID, data in groupPoints.iteritems():
            if groupNUID not in tempGroups:
                tempGroups.append(groupNUID)
            otherGroupNUIDs = data.get('otherGroupNUIDs', [])
            for otherGroupNUID in otherGroupNUIDs:
                if otherGroupNUID not in tempGroups:
                    tempGroups.append(otherGroupNUID)

        Netease.huntGhostGroups = tempGroups


def checkAlreadyInHuntGhost(groupNUID):
    if groupNUID in Netease.huntGhostGroups:
        return True
    return False


def getGroupPoint(groupNUID):
    if BigWorld.component in ('base', 'cell'):
        if Netease.huntGhostGroupAreas.has_key(groupNUID):
            areaId = Netease.huntGhostGroupAreas[groupNUID].get('areaId', 0)
            findPoint = Netease.huntGhostGroupAreas[groupNUID].get('findPoint', 0)
            flagMailBox = Netease.huntGhostGroupAreas[groupNUID].get('flagMailBox', None)
            return (areaId, findPoint, flagMailBox)
        return (0, 0, 0)


def onSyncHuntGhostBigGhostInfo(bigGhostBoxInfo):
    if BigWorld.component in ('base', 'cell'):
        Netease.bigGhostBoxInfo = bigGhostBoxInfo


def checkinHuntGhostTime(timeStamp = 0, useCache = True, tz = None):
    if BigWorld.component in ('base', 'cell'):
        return Netease.huntGhostIsOpen
    else:
        startStr, endStr = HGCD.data.get('huntGhostStartTime'), HGCD.data.get('huntGhostEndTime')
        if not startStr or not endStr:
            return False
        return utils.inCrontabRange(startStr, endStr)
