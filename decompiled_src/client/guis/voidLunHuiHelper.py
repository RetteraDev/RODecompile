#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/voidLunHuiHelper.o
import BigWorld
import gametypes
from gameclass import Singleton
from guis.asObject import TipManager
from guis import tipUtils
from data import team_endless_config_data as TECD
from data import monster_random_prop_data as MRPD
from data import bonus_history_check_data as BHCD

def getInstance():
    return voidLunHuiHelper.getInstance()


MAX_AVAILABLE_FLOOR = 5

class voidLunHuiHelper(object):
    __metaclass__ = Singleton

    def __init__(self):
        super(voidLunHuiHelper, self).__init__()

    def getLvKey(self, fbId):
        fbInfo = TECD.data.get('fbNos', {})
        for key in fbInfo:
            if fbId in fbInfo.get(key, []):
                return key[1]

        return 0

    def setCiZhuiInfo(self, propMc, propId):
        propInfo = MRPD.data.get(propId, {})
        name = propInfo.get('name', '')
        desc = propInfo.get('desc', '')
        icon = propInfo.get('icon', 0)
        propMc.fitSize = True
        propMc.loadImage(self.getIconPath(icon))
        tipText = "<font color = \'#F99348\'>%s</font>\n%s" % (name, desc)
        TipManager.addTip(propMc, tipText, tipUtils.TYPE_DEFAULT_BLACK)

    def getCiZhuiByDiffIdx(self, props, diffIdx):
        affix = TECD.data.get('affix', {})
        diffIdxs = affix.keys()
        diffIdxs.sort()
        propList = []
        for idx in diffIdxs:
            if idx <= diffIdx:
                for propId in affix.get(idx, []):
                    if propId in props:
                        propList.append(propId)

            else:
                break

        return propList

    def getRankDropDownKey(self):
        p = BigWorld.player()
        teamEndlessGlobalInfo = getattr(p, 'teamEndlessGlobalInfo', {})
        fbType = teamEndlessGlobalInfo.get('fbType', 0)
        return fbType

    def getPropList(self, diffIdx):
        p = BigWorld.player()
        teamEndlessInfo = getattr(p, 'teamEndlessGlobalInfo', {})
        affix = teamEndlessInfo.get('affix', [])
        return self.getCiZhuiByDiffIdx(affix, diffIdx)

    def getIconPath(self, iconId):
        return 'state/40/' + str(iconId) + '.dds'

    def getFbIdBytype(self, fbType, lvKey):
        fbIds = TECD.data.get('fbTypes', {}).get(fbType, [])
        fbRanges = TECD.data.get('fbNos', {}).keys()
        rangeKey = []
        for range in fbRanges:
            if lvKey >= range[0] and lvKey <= range[1]:
                rangeKey = range
                break

        rankIds = TECD.data.get('fbNos', {}).get(rangeKey, [])
        for fbId in fbIds:
            if fbId in rankIds:
                return fbId

        return 0

    def getOnceRewardState(self, lvKey, diffIdx):
        p = BigWorld.player()
        teamEndlessVal = p.teamEndless.get(lvKey, None)
        if teamEndlessVal:
            progress = getattr(teamEndlessVal, 'progress')
            if progress:
                return progress.get(diffIdx, gametypes.TEAM_ENDLESS_REWARD_STATE_DEFAULT)
        return gametypes.TEAM_ENDLESS_REWARD_STATE_DEFAULT

    def getThisWeekFbId(self, lvKey):
        p = BigWorld.player()
        teamEndlessGlobalInfo = getattr(p, 'teamEndlessGlobalInfo', {})
        fbType = teamEndlessGlobalInfo.get('fbType', 0)
        return self.getFbIdBytype(fbType, lvKey)

    def getMaxProgress(self, lvKey):
        p = BigWorld.player()
        floorLimit = TECD.data.get('teamEndlessDefaultFloorLimit ', 20)
        serverMaxLv = getattr(p, 'teamEndlessMaxLvs', {}).get(lvKey, 0)
        maxProgress = max(serverMaxLv + MAX_AVAILABLE_FLOOR, floorLimit)
        return maxProgress

    def getAvailableLv(self, lvKey):
        p = BigWorld.player()
        teamEndlessVal = p.teamEndless.get(lvKey, None)
        if teamEndlessVal:
            return teamEndlessVal.maxEnableLv
        else:
            return 1

    def getCurrentProgress(self, lvKey):
        p = BigWorld.player()
        teamEndlessVal = p.teamEndless.get(lvKey, None)
        if teamEndlessVal:
            return teamEndlessVal.maxLv
        else:
            return 0

    def getRemainRewardTime(self, lvKey):
        p = BigWorld.player()
        cid = TECD.data.get('rewardTimes', {}).get(lvKey)
        if not cid:
            return 0
        totalRewardTimes = BHCD.data.get(cid, {}).get('times', 0)
        return max(totalRewardTimes - p.teamEndlessRewardTimes.get(lvKey, 0), 0)
