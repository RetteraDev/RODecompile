#Embedded file name: I:/bag/tmp/tw2/res/entities\common/avoidDoingActivity.o
import BigWorld
import const
import gametypes
import utils
import copy
from userDictType import UserDictType
from userSoleType import UserSoleType
from data import avoid_doing_activity_data as ADAD
from data import world_quest_refresh_data as WQRD
from data import quest_loop_data as QLD
if BigWorld.component in ('base', 'cell'):
    import gameconfig
    import gameengine
    import gamebonus
    import gameconst
    import serverProgress
    from data import log_src_def_data as LSDD
    from data import formula_server_data as FMD
elif BigWorld.component in ('client',):
    import gameglobal
    if not getattr(BigWorld, 'isBot', False):
        from data import formula_client_data as FMD

class AvoidDoingActivity(UserDictType):

    def _lateReload(self):
        super(AvoidDoingActivity, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def isActivityTypeValid(self, activityType):
        activityTypes = [ v.get('activityType') for k, v in ADAD.data.iteritems() ]
        if activityType not in activityTypes:
            return False
        return True

    def onGetActivity(self, activityType):
        v = None
        if activityType in [gametypes.AVOID_DOING_ACTIVITY_TYPE_SCHOOL_INHERIT,
         gametypes.AVOID_DOING_ACTIVITY_TYPE_GUILD_DAILY_QUEST,
         gametypes.AVOID_DOING_ACTIVITY_TYPE_DEATH_ISLAND_BOX_QUEST,
         gametypes.AVOID_DOING_ACTIVITY_TYPE_DEATH_ISLAND_SOUL_QUEST,
         gametypes.AVOID_DOING_ACTIVITY_TYPE_SECRET_MARKET]:
            v = CommonQuestLoopAvoidDoing(activityType=activityType)
        elif activityType in [gametypes.AVOID_DOING_ACTIVITY_TYPE_THERMAL_SPRINT_FOR_WINE, gametypes.AVOID_DOING_ACTIVITY_TYPE_THERMAL_SPRINT_FOR_FOOD]:
            v = thermalSprintAvoidDoing(activityType=activityType)
        elif activityType in [gametypes.AVOID_DOING_ACTIVITY_TYPE_XIN_MO_FOR_LOW_LEVEL, gametypes.AVOID_DOING_ACTIVITY_TYPE_XIN_MO_FOR_MIDDLE_LEVEL, gametypes.AVOID_DOING_ACTIVITY_TYPE_XIN_MO_FOR_HIGH_LEVEL]:
            v = xinMoAvoidDoing(activityType=activityType)
        return v

    def getActivity(self, activityType = 0):
        if not activityType or not self.isActivityTypeValid(activityType):
            return None
        v = self.get(activityType)
        if not v:
            v = self.onGetActivity(activityType)
            self[activityType] = v
        return v

    def refreshDaily(self, owner):
        for activityKey, val in ADAD.data.iteritems():
            activityType = val.get('activityType', 0)
            if activityType == gametypes.AVOID_DOING_ACTIVITY_TYPE_SECRET_MARKET:
                if BigWorld.component in 'client':
                    continue
                stubInfo = owner.getWorldRefreshAppData()
                if not stubInfo or WQRD.data.get(stubInfo.get(gametypes.WORLD_QUEST_REFRESH_EXCLUDE, 0), {}).get('para', 0) != val.get('qeustLoopId', 0):
                    continue
            school = val.get('school', 0)
            conditionLv = val.get('conditionLv', ())
            ownerSchool = owner.school
            if school and ownerSchool != school:
                continue
            if conditionLv and (owner.lv < conditionLv[0] or owner.lv > conditionLv[1]):
                continue
            v = self.getActivity(activityType)
            v.activityKey = activityKey

        for activityType, val in self.iteritems():
            val.refreshDaily(owner, activityType)

    def refresh(self, owner):
        for activityKey, val in ADAD.data.iteritems():
            activityType = val.get('activityType', 0)
            if activityType == gametypes.AVOID_DOING_ACTIVITY_TYPE_SECRET_MARKET:
                if BigWorld.component in 'client':
                    continue
                stubInfo = owner.getWorldRefreshAppData()
                if not stubInfo or WQRD.data.get(stubInfo.get(gametypes.WORLD_QUEST_REFRESH_EXCLUDE, 0), {}).get('para', 0) != val.get('qeustLoopId', 0):
                    continue
            school = val.get('school', 0)
            conditionLv = val.get('conditionLv', ())
            ownerSchool = owner.school
            if school and ownerSchool != school:
                continue
            if conditionLv and (owner.lv < conditionLv[0] or owner.lv > conditionLv[1]):
                continue
            v = self.getActivity(activityType)
            v.activityKey = activityKey

        for activityType, val in self.iteritems():
            val.refresh(owner, activityType)

    def transfer(self, owner):
        if not gameconfig.enableAvoidDoingActivity():
            return
        owner.client.onSendAvoidDoingActivity(self.getDTO())

    def getDTO(self):
        return [ (activityType, x.getDTO()) for activityType, x in self.iteritems() ]

    def fromDTO(self, dto):
        if not dto:
            self.clear()
            return self
        for activityType, d in dto:
            v = self.onGetActivity(activityType)
            if not v:
                continue
            self[activityType] = v.fromDTO(d)

        return self


class IAvoidDoingActivityCommon(UserSoleType):

    def __init__(self, activityType = 0):
        self.activityKey = 0
        self.avoidDoneCount = 0

    def _lateReload(self):
        super(IAvoidDoingActivityCommon, self)._lateReload()

    def getActivityKey(self):
        return self.activityKey

    def updateActivityKey(self, activityKey):
        self.activityKey = activityKey

    def onUpdateDoneCount(self, count):
        self.avoidDoneCount += count

    def refresh(self, owner, activityType):
        if not owner:
            return
        if not self.isAvoidDoingInValidTime():
            return
        self.transfer(owner, activityType)

    def refreshDaily(self, owner, activityType):
        self.avoidDoneCount = 0
        self.transfer(owner, activityType)

    def getDTO(self):
        return (self.activityKey, self.avoidDoneCount)

    def fromDTO(self, dto):
        self.activityKey, self.avoidDoneCount = dto
        return self

    def transfer(self, owner, activityType):
        if BigWorld.component in ('base', 'cell'):
            owner.client.onSendAvoidDoingActivity([(activityType, self.getDTO())])
        elif BigWorld.component in 'client':
            owner.onSendAvoidDoingActivity([(activityType, self.getDTO())])

    def isAvoidDoingInValidTime(self):
        flag = False
        if BigWorld.component in ('base', 'cell'):
            if not gameconfig.enableAvoidDoingActivity() or not self.isAvoidDoingInOpenTime():
                return flag
        elif not gameglobal.rds.configData.get('enableAvoidDoingActivity', False) or not self.isAvoidDoingInOpenTime():
            return flag
        flag = True
        return flag

    def isAvoidDoingInOpenTime(self):
        adad = ADAD.data.get(self.activityKey, {})
        openTime = adad.get('openTime', None)
        closeTime = adad.get('closeTime', None)
        tWhen = utils.getNow()
        if openTime and closeTime and utils.getDisposableCronTabTimeStamp(openTime) <= tWhen <= utils.getDisposableCronTabTimeStamp(closeTime):
            return True
        return False

    def getEnableAvoidDoingActivity(self):
        if BigWorld.component == 'client':
            import gameglobal
            enableRewardRecovery = gameglobal.rds.configData.get('enableAvoidDoingActivity', 0)
        else:
            enableRewardRecovery = gameconfig.enableAvoidDoingActivity()
        return enableRewardRecovery

    def calcActivityAvoidDoingFlag(self, owner):
        adad = ADAD.data.get(self.activityKey, {})
        avoidDoingFlag = False
        if self.isConditionValCanAvoidDoing(owner, adad):
            avoidDoingFlag = True
        return avoidDoingFlag


class CommonQuestLoopAvoidDoing(IAvoidDoingActivityCommon):

    def isConditionValCanAvoidDoing(self, owner, adad):
        flag = False
        conditionLv = adad.get('conditionLv', ())
        maxCount = adad.get('count', 0)
        questLoopId = adad.get('qeustLoopId', 0)
        eIds = adad.get('eId', ())
        for eId in eIds:
            if eId and not serverProgress.isMileStoneFinished(eId):
                return flag

        if conditionLv and (owner.lv < conditionLv[0] or owner.lv > conditionLv[1]) or self.avoidDoneCount >= maxCount or owner.questLoopInfo.has_key(questLoopId) and owner.questLoopInfo[questLoopId].questInfo:
            return flag
        if not self.isAvoidDoingInValidTime():
            return flag
        flag = True
        return flag

    def ruduceActivityAvoidDoingCD(self, owner, adad):
        questLoopId = adad.get('qeustLoopId', 0)
        if not owner.questLoopInfo.has_key(questLoopId):
            from questLoops import QuestLoopVal
            owner.questLoopInfo[questLoopId] = QuestLoopVal(questLoopId)
        else:
            owner.questLoopInfo[questLoopId].questInfo = []
        owner.questLoopInfo[questLoopId]._finishLoop(owner)
        owner.questLoopInfo[questLoopId].loopCnt += 1
        owner.questLoopInfo = owner.questLoopInfo
        self.onUpdateDoneCount(1)
        qld = QLD.data[questLoopId]
        activityId = qld.get('rewardGetBackActivityId', 0)
        if activityId:
            owner.base.onRewardRecoveryActivityCompleted(activityId, (questLoopId, owner.questLoopInfo[questLoopId].getQuestLoopCnt(owner, questLoopId), owner.questLoopInfo[questLoopId].getCurrentStep()))

    def addActivityAvoidDoingActivation(self, owner, activationIds, amount):
        owner.addActivation(gametypes.ACTIVATION_TYPE_ITEM, activationIds, amount * 1000, gametypes.ACTIVATION_SRC_QUEST)


class thermalSprintAvoidDoing(IAvoidDoingActivityCommon):

    def isConditionValCanAvoidDoing(self, owner, adad):
        flag = False
        conditionLv = adad.get('conditionLv', ())
        maxCount = adad.get('count', 0)
        fameId = adad.get('fameId', 0)
        eIds = adad.get('eId', ())
        for eId in eIds:
            if eId and not serverProgress.isMileStoneFinished(eId):
                return flag

        if BigWorld.component in 'client':
            curFameVal = owner.fame.get(fameId, 0)
        elif BigWorld.component in ('base', 'cell'):
            curFameVal = owner.fame.getFame(fameId)
        if owner.lv < conditionLv[0] or owner.lv > conditionLv[1] or curFameVal < 100:
            return flag
        if not self.isAvoidDoingInValidTime():
            return flag
        flag = True
        return flag

    def ruduceActivityAvoidDoingCD(self, owner, adad):
        fameId = adad.get('fameId', 0)
        owner.reduceFame(fameId, 100, LSDD.data.LOG_SRC_EXP_BONUS)
        self.onUpdateDoneCount(1)

    def addActivityAvoidDoingActivation(self, owner, activationIds, amount):
        owner.addActivation(gametypes.ACTIVATION_TYPE_ITEM, activationIds, amount * 1000, gametypes.ACTIVATION_SRC_ITEM)


class xinMoAvoidDoing(IAvoidDoingActivityCommon):

    def isConditionValCanAvoidDoing(self, owner, adad):
        flag = False
        conditionLv = adad.get('conditionLv', ())
        maxCount = adad.get('count', 0)
        bonusHistoryId = adad.get('bonusHistoryId', 0)
        eIds = adad.get('eId', ())
        for eId in eIds:
            if eId and not serverProgress.isMileStoneFinished(eId):
                return flag

        if owner.lv < conditionLv[0] or owner.lv > conditionLv[1] or self.avoidDoneCount >= maxCount:
            return flag
        if BigWorld.component in 'cell' and owner.getBonusHistory(bonusHistoryId) >= maxCount:
            return flag
        if not self.isAvoidDoingInValidTime():
            return flag
        flag = True
        return flag

    def ruduceActivityAvoidDoingCD(self, owner, adad):
        bonusHistoryId = adad.get('bonusHistoryId', 0)
        treasureBoxId = adad.get('treasureBoxId', 0)
        owner.addBonusHistory(bonusHistoryId, gamebonus.BAG_FULL_MAIL, mailTemplateId='bonusHistoryRewardMail', logSrc=LSDD.data.LOG_SRC_BONUS_HISTORY_AWARD, giveReward=False)
        self.onUpdateDoneCount(1)
        if treasureBoxId:
            owner.statsTrigger(gameconst.ST_OPEN_BOX, (), (treasureBoxId,))

    def addActivityAvoidDoingActivation(self, owner, activationIds, amount):
        owner.addActivation(gametypes.ACTIVATION_TYPE_ITEM, activationIds, amount * 1000, gametypes.ACTIVATION_SRC_TREASUREBOX)
