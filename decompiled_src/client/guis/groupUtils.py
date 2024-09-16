#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/groupUtils.o
import BigWorld
import const

def isInSameTeam(srcGbId, tgtGbId):
    p = BigWorld.player()
    try:
        srcIndex = p.arrangeDict[srcGbId]
        tgtIndex = p.arrangeDict[tgtGbId]
    except:
        return False

    if srcIndex / const.TEAM_MAX_NUMBER == tgtIndex / const.TEAM_MAX_NUMBER:
        return True
    else:
        return False
