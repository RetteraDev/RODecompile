#Embedded file name: I:/bag/tmp/tw2/res/entities\common/flowbackGroup.o
import BigWorld
from userSoleType import UserSoleType
import time
if BigWorld.component in ('base', 'cell'):
    import gameconfig
    import gameconst
import utils
import const
import gametypes
from data import sys_config_data as SCD
from cdata import flowback_group_data as FGD
from data import flowback_group_target_data as FGTD
from data import flowback_group_privilege_data as FGPD
from cdata import flowback_group_recharge_data as FGRD
from data import skill_auras_data as SAD
FLOW_BACK_GROUP_RECHARGE_ID = 1

def getFlowbackType(lostTime):
    lostDays = lostTime / const.SECONDS_PER_DAY
    for k, v in FGD.data.iteritems():
        if v['days'][0] <= lostDays <= v['days'][1]:
            return k

    return 0


class FlowbackGroup(UserSoleType):

    def _lateReload(self):
        super(FlowbackGroup, self)._lateReload()

    def __init__(self):
        super(FlowbackGroup, self).__init__()
        self.flowbackGroupType = 0
        self.startTime = 0
        self.endTime = 0
        self.rechargeOp = 0
        self.totalExp = 0
        self.restExp = 0
        self.totalBindCash = 0
        self.restBindCash = 0
        self.targetPoints = 0
        self.targetPointsRewards = {}
        self.targetsStateInfo = {}
        self.flowbackGroupGoalVars = {}
        self.flowbackGroupDailyGoalVarNames = []
        self.flowbackGroupAlreadyFinishedGoalIds = []
        self.privilegesInfo = {}
        self.rechargeAmount = 0
        self.rechargeRewards = {}
        self.auraEndTimerId = 0

    def resetFlowbackGroupInfo(self, owner):
        self.resetFlowbackGroupAura(owner)
        self.flowbackGroupType = 0
        self.startTime = 0
        self.endTime = 0
        self.rechargeOp = 0
        self.totalExp = 0
        self.restExp = 0
        self.totalBindCash = 0
        self.restBindCash = 0
        self.targetPoints = 0
        self.targetPointsRewards = {}
        self.targetsStateInfo = {}
        self.flowbackGroupGoalVars = {}
        self.flowbackGroupDailyGoalVarNames = []
        self.flowbackGroupAlreadyFinishedGoalIds = []
        self.privilegesInfo = {}
        self.rechargeAmount = 0
        self.rechargeRewards = {}
        owner.base.updateMallItemsBuyInfo(FGRD.data.get(FLOW_BACK_GROUP_RECHARGE_ID, {}).get('mallItemIds', ()))
        owner.syncFlowbackGroupBonus()

    def resetFlowbackGroupAura(self, owner):
        fgpd = FGPD.data
        if not owner or not fgpd:
            return
        for privilegeId, value in self.privilegesInfo.iteritems():
            auraId = fgpd.get(privilegeId, {}).get('auraId', 0)
            if not auraId:
                continue
            owner.removeAura(auraId)
            effects = SAD.data.get(auraId, {}).get('effects', [])
            for stateId, _ in effects:
                owner.removeState(stateId)

    def reloadOnLogin(self, owner):
        if not gameconfig.enableFlowbackGroup():
            self.resetFlowbackGroupInfo(owner)
            return
        if not owner.lastLogoffTime:
            return
        if owner.lv < SCD.data.get('FLOWBACK_MIN_LV', 20):
            return
        self.recalcFlowbackGroupInfo(owner)
        owner.flowbackGroupBonus = owner.flowbackGroupBonus

    def calcFlowbackGroupEndTime(self, curTime):
        duration = FGD.data.get(self.flowbackGroupType, {}).get('flowbackGroupDuration', 0)
        endTime = curTime + duration * const.TIME_INTERVAL_DAY
        return endTime

    def recalcFlowbackGroupInfo(self, owner):
        if not owner:
            return
        curTime = utils.getNow()
        lastLogoffTime = owner.lastLogoffTime
        if self.endTime < curTime:
            if self.endTime:
                self.resetFlowbackGroupInfo(owner)
            lostTime = curTime - lastLogoffTime
            flowbackGroupType = getFlowbackType(lostTime)
            if flowbackGroupType:
                serverOpenTime = utils.getNow() - utils.getServerOpenTime()
                panelsOpOfServerOpenTime = SCD.data.get('flowbackGroupPanelsOpOfServerOpenTime', {})
                expCatchUpPanelOpTime = panelsOpOfServerOpenTime.get(const.FLOWBACK_PANEL_EXP_CATCH_UP, 0) * const.SECONDS_PER_DAY
                privilegePanelOpTime = panelsOpOfServerOpenTime.get(const.FLOWBACK_PANEL_PRIVILEGE, 0) * const.SECONDS_PER_DAY
                rechargePanelOpTime = panelsOpOfServerOpenTime.get(const.FLOWBACK_PANEL_RECHARGE, 0) * const.SECONDS_PER_DAY
                minPanelOpTime = min(expCatchUpPanelOpTime, privilegePanelOpTime, rechargePanelOpTime)
                if serverOpenTime < minPanelOpTime:
                    return
                self.flowbackGroupType = flowbackGroupType
                self.startTime = curTime
                self.endTime = self.calcFlowbackGroupEndTime(curTime)
                if serverOpenTime >= expCatchUpPanelOpTime:
                    self.recalcExpCatchUpInfo(owner)
                if serverOpenTime >= privilegePanelOpTime:
                    self.recalcPrivilegeInfo(owner)
                if serverOpenTime >= rechargePanelOpTime:
                    self.recalcRechargeInfo()
                owner.statsTrigger(gameconst.ST_LOGIN_ON_ONCE_DAILY, (), ())
            else:
                return
        else:
            self.addAura(owner)
            return

    def addAura(self, owner):
        if not self.isValid(owner):
            return
        fgpd = FGPD.data
        if not fgpd:
            return
        for privilegeId, status in self.privilegesInfo.iteritems():
            value = fgpd.get(privilegeId, {})
            if value.get('privilegeType', 0) == const.FLOWBACK_PRIVILEGE_TYPE_AURA:
                auraId = value.get('auraId')
                duration = value.get('duration')
                if auraId:
                    leftTime = duration * const.TIME_INTERVAL_DAY - (utils.getNow() - self.startTime)
                    if leftTime > 0:
                        owner.addAura(auraId, 1, owner.id)
                        if self.auraEndTimerId:
                            owner._cancelCallback(self.auraEndTimerId)
                        self.auraEndTimerId = owner._callback(leftTime, 'removeAura', (auraId, gametypes.REMOVE_AURA_BY_TTL))
                        effects = SAD.data.get(auraId, {}).get('effects', [])
                        for stateId, _ in effects:
                            owner.addState(stateId, 1, leftTime, gametypes.ADD_STATE_FROM_FLOWBACK, owner.id, 0)

    def addFlowbackGroupAura(self, owner):
        if not self.isValid(owner):
            return
        if not owner.lastLogoffTime:
            return
        if owner.lv < SCD.data.get('FLOWBACK_MIN_LV', 20):
            return
        curTime = utils.getNow()
        if self.endTime >= curTime:
            self.addAura(owner)

    def recalcExpCatchUpInfo(self, owner):
        d = FGD.data.get(self.flowbackGroupType)
        if not d:
            return
        if not d.get('duration', 0):
            return
        overflowExp = owner.overflowExp
        overflowExpFactor = d.get('overflowExpFactor', 0)
        self.totalExp = int(overflowExp * overflowExpFactor)
        self.restExp = self.totalExp
        bindCashFormula = d.get('bindCashFormula', lambda c: 0)
        if not bindCashFormula:
            self.totalBindCash = int(self.restBindCash * 0.7)
            self.restBindCash = self.totalBindCash
            return
        duration = (utils.getNow() - owner.lastLogoffTime) / const.SECONDS_PER_DAY
        btx = {'lv': owner.lv,
         'd': duration}
        bindCashAmount = int(bindCashFormula(btx))
        self.totalBindCash = bindCashAmount + int(self.restBindCash * 0.7)
        self.restBindCash = self.totalBindCash
        targetIds = d.get('targetIds', ())
        for index in xrange(len(targetIds)):
            targetId = targetIds[index]
            if targetId in self.targetsStateInfo:
                continue
            if self.flowbackGroupType not in FGTD.data.get(targetId, {}).get('typeGroup', ()):
                continue
            self.targetsStateInfo[targetId] = const.FLOWBACK_STATE_NO_COMPLETE

    def resetExpCatchUpInfo(self):
        self.totalExp = 0
        self.restExp = 0
        self.totalBindCash = 0
        self.restBindCash = 0
        self.targetPoints = 0
        self.targetPointsRewards = {}
        self.targetsStateInfo = {}
        self.flowbackGroupGoalVars = {}
        self.flowbackGroupDailyGoalVarNames = []
        self.flowbackGroupAlreadyFinishedGoalIds = []

    def isExpCatchUpTimeValid(self, owner):
        fgd = FGD.data
        duration = fgd.get(self.flowbackGroupType, {}).get('duration', 0)
        if utils.getNow() > self.startTime + duration * const.SECONDS_PER_DAY:
            self.resetExpCatchUpInfo()
            owner.syncFlowbackGroupBonus()
            return False
        return True

    def isValid(self, owner):
        if not owner or not gameconfig.enableFlowbackGroup() or self.endTime < utils.getNow() or not self.flowbackGroupType:
            self.resetFlowbackGroupInfo(owner)
            return False
        return True

    def recalcPrivilegeInfo(self, owner):
        fgpd = FGPD.data
        if not owner or not fgpd:
            return
        for privilegeId, value in fgpd.iteritems():
            type = value.get('type', 0)
            if type != self.flowbackGroupType:
                continue
            if privilegeId in self.privilegesInfo:
                continue
            privilegeType = value.get('privilegeType', 0)
            if privilegeType == const.FLOWBACK_PRIVILEGE_TYPE_AURA:
                auraId = value.get('auraId')
                duration = value.get('duration')
                if auraId:
                    leftTime = duration * const.TIME_INTERVAL_DAY - (utils.getNow() - self.startTime)
                    if leftTime > 0:
                        owner.addAura(auraId, 1, owner.id)
                        if self.auraEndTimerId:
                            owner._cancelCallback(self.auraEndTimerId)
                        self.auraEndTimerId = owner._callback(leftTime, 'removeAura', (auraId, gametypes.REMOVE_AURA_BY_TTL))
                        effects = SAD.data.get(auraId, {}).get('effects', [])
                        for stateId, _ in effects:
                            owner.addState(stateId, 1, leftTime, gametypes.ADD_STATE_FROM_FLOWBACK, owner.id, 0)

                self.privilegesInfo[privilegeId] = const.FLOWBACK_PRIVILEGE_STATE_ALREADY_AWARD_BUT_VALID
            elif privilegeType == const.FLOWBACK_PRIVILEGE_TYPE_MULTI_FUBEN_TREASURE_BOX:
                self.privilegesInfo[privilegeId] = const.FLOWBACK_PRIVILEGE_STATE_ALREADY_AWARD_BUT_VALID
            else:
                self.privilegesInfo[privilegeId] = const.FLOWBACK_PRIVILEGE_STATE_NO_AWARD

    def recalcRechargeInfo(self):
        self.rechargeOp = FGD.data.get(self.flowbackGroupType, {}).get('rechargeOp', 0)
