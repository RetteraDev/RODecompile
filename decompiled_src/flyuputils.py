#Embedded file name: /WORKSPACE/data/entities/common/flyuputils.o
import gameconfigCommon
import utils
import gametypes
from data import fly_up_exp_data as FUED

def enableFlyUp():
    if not gameconfigCommon.enableFlyUp():
        return False
    if gameconfigCommon.enableIgnoreFlyUpGroupCheck():
        return True
    from cdata import fly_up_config_data as fucd
    groupId = utils.getWingWorldGroupId(utils.getHostId())
    if groupId == gametypes.FLY_UP_GROUP_ONE:
        return True
    if groupId == gametypes.FLY_UP_GROUP_TWO and utils.getServerOpenDays() >= fucd.data.get('flyUpServerOpenDays', 0):
        return True
    return False


def calcSkillPoints(lv, flyUpLv):
    if not enableFlyUp() or not flyUpLv:
        return 0
    skillPointData = FUED.data.get(flyUpLv, {}).get('skillPoint', ())
    if not skillPointData:
        return 0
    for lvRange, skillPoint in skillPointData:
        if lvRange[0] <= lv <= lvRange[1]:
            return skillPoint

    return 0
