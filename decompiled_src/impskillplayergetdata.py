#Embedded file name: /WORKSPACE/data/entities/client/helpers/impskillplayergetdata.o
import BigWorld
import gameglobal
import skillDataInfo
import gamelog
from skillDataInfo import ClientSkillInfo
from skillDataInfo import AppearanceSkillInfo

class ImpSkillPlayerGetData(object):

    def getActionName(self, stage, skillInfo, changeCastNo = True, clientSkillInfo = None):
        if not clientSkillInfo:
            try:
                clientSkillInfo = ClientSkillInfo(skillInfo.num, skillInfo.lv)
            except:
                gamelog.debug("can\'t find skillID:", skillInfo.num, skillInfo.lv)
                return None

        res = skillDataInfo.getSkillActionName(clientSkillInfo, stage, self.stateKit)
        if res:
            res = list(res)
            num = res.pop(0)
            if num == gameglobal.RAND_CAST:
                if self.skillKit < len(res) and self.skillKit >= 0:
                    res = res[self.skillKit]
                else:
                    res = res[0]
                return res
            if num == gameglobal.QUEUE_CAST:
                if self.skillStart and self.castIndex[0] == skillInfo.num:
                    skillStep = (self.castIndex[2] + 1) % len(res)
                    self.skillStart = False
                else:
                    skillStep = self.castIndex[2]
                if changeCastNo:
                    self.castIndex[0] = skillInfo.num
                    self.castIndex[2] = skillStep
                if skillStep < len(res) and skillStep >= 0:
                    res = res[skillStep]
                else:
                    res = res[0]
                return res
        if changeCastNo:
            self.castIndex[0] = skillInfo.num
            self.castIndex[1] = 0
            self.castIndex[2] = -1
        return res

    def getEffect(self, stage, clientSkillInfo):
        res = skillDataInfo.getSkillEffects(clientSkillInfo, stage, self.stateKit)
        gamelog.debug('getEffect', res, stage, self.castIndex)
        if res:
            res = list(res)
            num = res.pop(0)
            if num == gameglobal.RAND_CAST:
                if self.skillKit < len(res) and self.skillKit >= 0:
                    return [res[self.skillKit]]
                else:
                    return [res[0]]
            else:
                if num == gameglobal.QUEUE_CAST:
                    step = self.castIndex[2]
                    if stage == gameglobal.S_FLY:
                        self.castIndex[2] = (self.castIndex[2] + 1) % len(res)
                        step = self.castIndex[2]
                    if step < len(res):
                        res = [res[step]]
                    else:
                        res = [res[0]]
                    return res
                if num == gameglobal.ALL_CAST:
                    return res
        return res

    def getTintEffect(self, stage, clientSkillInfo):
        return skillDataInfo.getSkillTintEffect(clientSkillInfo, stage)

    def getActionWithEffect(self, stage, skillInfo, clientSkillInfo = None):
        actionName = self.getActionName(stage, skillInfo, clientSkillInfo=clientSkillInfo)
        effects = self.getEffect(stage, clientSkillInfo)
        if effects == None:
            effects = []
        tintEffect = self.getTintEffect(stage, clientSkillInfo)
        return (actionName, effects, tintEffect)

    def getActEffectByState(self, clientSkillInfo):
        selfStates = skillDataInfo.getSelfStates(clientSkillInfo)
        if not selfStates:
            return -1
        owner = BigWorld.entity(self.owner)
        states = owner.getStates()
        for stateId in states.keys():
            for stateNo in xrange(len(selfStates)):
                if selfStates[stateNo] == stateId:
                    return stateNo

        return -1

    def getActEffectBySkillFlag(self, owner, clientSkillInfo):
        selfSkillFlags = skillDataInfo.getSelfSkillFlags(clientSkillInfo)
        if not selfSkillFlags:
            return (False, -1)
        owner = BigWorld.entity(self.owner)
        for flagNo in xrange(len(selfSkillFlags)):
            if owner.skillFlagState.checkInFlagState(owner, selfSkillFlags[flagNo]):
                return (True, flagNo)

        return (False, -1)

    def getActEffectByAmmoType(self, owner, clientSkillInfo):
        ammoTypes = skillDataInfo.getSelfAmmoTypes(clientSkillInfo)
        if not ammoTypes:
            return (False, -1)
        owner = BigWorld.entity(self.owner)
        for index in xrange(len(ammoTypes)):
            if owner.ammoType and owner.ammoType == ammoTypes[index]:
                return (True, index)

        return (False, -1)

    def getActEffectByHostState(self, host, clientSkillInfo):
        selfStates = skillDataInfo.getSelfStates(clientSkillInfo)
        if not selfStates or not hasattr(BigWorld.player(), 'effect'):
            return -1
        if not host or not host.inWorld:
            return -1
        gamelog.debug('---lihang@getActEffectByState', host.id, selfStates)
        for stateId in host.statesClientPub.keys():
            for stateNo in xrange(len(selfStates)):
                if selfStates[stateNo] == stateId:
                    return stateNo

        return -1

    def getMoveType(self, stage, skillInfo):
        return skillDataInfo.getMoveType(stage, skillInfo)

    def getFlyEffect(self, clientSkillInfo):
        res = self.getEffect(gameglobal.S_FLY, clientSkillInfo)
        return res

    def getSkillStateInfo(self, clientSkillInfo, owner = None):
        isAppearanceSkill = isinstance(clientSkillInfo, AppearanceSkillInfo)
        if owner:
            hasFlag, kit = self.getActEffectBySkillFlag(owner, clientSkillInfo)
            if hasFlag:
                self.stateKit = kit
                skillFlags = skillDataInfo.getSelfSkillFlags(clientSkillInfo)
                try:
                    if isAppearanceSkill:
                        skillStateInfo = AppearanceSkillInfo(clientSkillInfo.num, clientSkillInfo.appearanceId, AppearanceSkillInfo.SKILL_TYPE_STATE, skillFlags[kit])
                    else:
                        skillStateInfo = ClientSkillInfo(clientSkillInfo.num, clientSkillInfo.lv, 3, skillFlags[kit])
                except:
                    return clientSkillInfo

                return skillStateInfo
        if owner:
            hasFlag, kit = self.getActEffectByAmmoType(owner, clientSkillInfo)
            if hasFlag:
                self.stateKit = kit
                ammoTypes = skillDataInfo.getSelfAmmoTypes(clientSkillInfo)
                try:
                    if isAppearanceSkill:
                        skillStateInfo = AppearanceSkillInfo(clientSkillInfo.num, clientSkillInfo.appearanceId, AppearanceSkillInfo.SKILL_TYPE_STATE, ammoTypes[kit])
                    else:
                        skillStateInfo = ClientSkillInfo(clientSkillInfo.num, clientSkillInfo.lv, 3, ammoTypes[kit])
                except:
                    return clientSkillInfo

                return skillStateInfo
        self.stateKit = self.getActEffectByState(clientSkillInfo)
        selfStates = skillDataInfo.getSelfStates(clientSkillInfo)
        if self.stateKit != -1 and selfStates:
            self.castIndex[1] = selfStates[self.stateKit]
            try:
                if isAppearanceSkill:
                    skillStateInfo = AppearanceSkillInfo(clientSkillInfo.num, clientSkillInfo.appearanceId, AppearanceSkillInfo.SKILL_TYPE_STATE, self.castIndex[1])
                else:
                    skillStateInfo = ClientSkillInfo(clientSkillInfo.num, clientSkillInfo.lv, 3, self.castIndex[1])
            except:
                return clientSkillInfo

            return skillStateInfo
        else:
            self.castIndex[1] = 0
        return clientSkillInfo
