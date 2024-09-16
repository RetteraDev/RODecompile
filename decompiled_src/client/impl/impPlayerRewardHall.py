#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerRewardHall.o
import BigWorld
import const
import utils
import commInvitation
import gameglobal
from guis import uiConst
import gametypes
from data import sys_config_data as SCD
from data import activity_state_config_data as ASCD
from data import junjie_config_data as JCD
from data import friend_invitation_reward_data as FIRD
from cdata import lv_up_award_data as LUAD
from cdata import skill_enhance_bonus_data as SEBD
checkMapFunc = {}

def funcMapWrap(k):

    def fwrap(f):
        if checkMapFunc.has_key(k):
            raise ValueError('duplicate key: ', k)
        checkMapFunc[k] = f.__name__
        return f

    return fwrap


class ImpPlayerRewardHall(object):

    @funcMapWrap(uiConst.REWARD_SHENJI)
    def _checkLvUp(self):
        p = BigWorld.player()
        for k in LUAD.data.keys():
            if not p.lvUpRewardData.get(k[0]) and k[0] <= p.lv:
                return True

        return False

    @funcMapWrap(uiConst.REWARD_QUMO)
    def _checkQumo(self):
        p = BigWorld.player()
        gongxianData = SCD.data.get('pointsToFame', [])
        gongxianPoint = [180, 300, 560]
        if len(gongxianData) > 0:
            gongxianPoint[0] = gongxianData[0][0]
            gongxianPoint[1] = gongxianData[1][0]
            gongxianPoint[2] = gongxianData[2][0]
        gotGongxian = p.weeklyQumoCollectPoints if p.weeklyQumoCollectPoints else []
        if len(gotGongxian) == 0 and p.weeklyQumoPoints >= gongxianPoint[0]:
            return True
        if len(gotGongxian) == 1 and p.weeklyQumoPoints >= gongxianPoint[1]:
            return True
        if len(gotGongxian) == 2 and p.weeklyQumoPoints >= gongxianPoint[2]:
            return True
        qumoActId = getattr(p, 'qumoActivityId', 0)
        if qumoActId:
            qmDataList = ASCD.data.get(qumoActId, {}).get('pointsToFame', {})
            coverBonus = []
            for qmData in qmDataList:
                if qmData[0] <= p.weeklyQumoPoints:
                    coverBonus.append(qmData[0])

            if len(coverBonus):
                for canGetPoint in coverBonus:
                    canGet = True
                    for wcItem in p.weeklyQumoCollectPointsForActivity:
                        getedPoint = wcItem[0]
                        if getedPoint == canGetPoint:
                            canGet = False

                    if canGet:
                        return True

        return False

    @funcMapWrap(uiConst.REWARD_JUNJIE)
    def _checkJunjie(self):
        p = BigWorld.player()
        lv = p.junJieLv
        nowLevelData = JCD.data.get(lv, {})
        weekZhanxunFame = p.fameWeek.get(const.ZHAN_XUN_FAME_ID, (0, 0))
        rewardZXScores = nowLevelData.get('rewardZXScores', [])
        for i in xrange(len(rewardZXScores)):
            if weekZhanxunFame[0] >= rewardZXScores[i]:
                if not p.zhanXunReward.get((p.junJieLv, i), False):
                    return True

        if getattr(p, 'zxActivityId', 0):
            zxData = ASCD.data.get(p.zxActivityId, {}).get('rewardZXInfo', {}).get(p.junJieLv, None)
            if zxData:
                needPoint = zxData[0]
                if weekZhanxunFame[0] >= needPoint and not p.zhanXunActivityBonusApplied:
                    return True
        return False

    @funcMapWrap(uiConst.REWARD_ANQUAN)
    def _checkBing(self):
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableBindReward', False):
            if p.bindPhoneNum and not p.hasPhoneRewardReceived or p.securityTypeOfCell and not p.hasEkeyRewardReceived or p.appBindStatus == gametypes.BIND_STATUS_SUCC and not p.appBindRewarded or p.weixinBindStatus == gametypes.BIND_STATUS_SUCC and not p.weixinBindRewarded or utils.isCipherBinding(p) and not p.hasCipherRewardReceived:
                return True
            return False
        elif p.bindPhoneNum and not p.hasPhoneRewardReceived or p.securityTypeOfCell and not p.hasEkeyRewardReceived or utils.isCipherBinding(p) and not p.hasCipherRewardReceived:
            return True
        else:
            return False
        return False

    @funcMapWrap(uiConst.REWARD_XIULIAN)
    def _checkXiulian(self):
        p = BigWorld.player()
        totalPoint = utils.getTotalSkillEnhancePoint(p)
        for k, v in SEBD.data.iteritems():
            if totalPoint < k:
                continue
            if k in p.skillEnhancePointBonus:
                continue
            questId = v.get('questId')
            if questId and p.getQuestFlag(questId):
                continue
            bonusId = v.get('bonusId')
            if not bonusId:
                continue
            return True

        return False

    @funcMapWrap(uiConst.REWARD_DUIHUAN)
    def _checkDuijiang(self):
        return False

    @funcMapWrap(uiConst.REWARD_ZHIYOU)
    def _checkFriend(self):
        p = BigWorld.player()
        for rewardId in FIRD.data.iterkeys():
            for fgbId in p.friendInviteInfo.iterkeys():
                if commInvitation.gainFriendInviteRewardCheck(p, fgbId, rewardId):
                    return True

        return False

    def rewardHallLogonCheck(self):
        for k in uiConst.REWARD_HALL_SET:
            BigWorld.player().updateRewardHallInfo(k)

    def updateRewardHallInfo(self, key):
        if key not in uiConst.REWARD_HALL_SET:
            return
        p = BigWorld.player()
        if p.rewardHall.get(key) != getattr(p, checkMapFunc[key])():
            p.rewardHall[key] = getattr(p, checkMapFunc[key])()
            gameglobal.rds.ui.rewardHall.updateRewardHall()
            gameglobal.rds.ui.welfareRewardHall.updateRewardHall()

    def checkNeedPushMsg(self):
        p = BigWorld.player()
        for key in p.rewardHall:
            if p.rewardHall[key]:
                return True

        return False

    def getPushMsgInfo(self):
        info = []
        index = 0
        p = BigWorld.player()
        for key in p.rewardHall:
            if p.rewardHall[key]:
                info.append(key)
            index = index + 1

        return info
