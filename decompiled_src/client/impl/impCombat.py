#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impCombat.o
import BigWorld
import copy
import gameglobal
import gametypes
import gamelog
import const
import utils
from helpers import action
from guis import uiConst, uiUtils
from cdata import balance_method_data as BMD
from data import conditional_prop_data as CPD
from data import prop_ref_data as PRD
from cdata import game_msg_def_data as GMDD

class ImpCombat(object):

    def switchWeaponState(self, weaponState, haveAct = True, forceSwitch = False):
        if self.weaponState != weaponState or forceSwitch:
            self.weaponState = weaponState
            if self.isDoingAction:
                return
            self.modelServer.refreshWeaponStateWithAct(haveAct)

    def weaponInHandState(self):
        return self.weaponState

    def isGuarding(self):
        return self.inCombat

    def invokeWeaponTimer(self):
        if self.inWeaponCallback:
            BigWorld.cancelCallback(self.inWeaponCallback)
            self.inWeaponCallback = None
        self.inWeaponCallback = BigWorld.callback(gameglobal.COMBAT_TIME, self._hangUpWeapon)

    def _hangUpWeapon(self):
        self.inWeaponCallback = None
        if self.inWorld:
            if self.life == gametypes.LIFE_DEAD:
                return
            if self.skillPlayer.inWeaponBuff or self.bufActState or self.weaponState == gametypes.WEAPON_HANDFREE:
                return
            if self.fashion.doingActionType() in (action.CHARGE_ACTION,
             action.GUIDE_ACTION,
             action.CASTSTOP_ACTION,
             action.MOVINGSTOP_ACTION,
             action.AFTERMOVESTOP_ACTION):
                self.inWeaponCallback = BigWorld.callback(gameglobal.COMBAT_CONTINUE_TIME, self._hangUpWeapon)
            elif self.fashion.doingActionType() == action.ROLL_ACTION or self.qinggongMgr.isJumping():
                self.inWeaponCallback = BigWorld.callback(gameglobal.COMBAT_CONTINUE_TIME, self._hangUpWeapon)
                self.delayHangupWeapon = True
            elif not self.inCombat:
                if self.weaponInHandState() == gametypes.WEAR_BACK_ATTACH:
                    self.innerUpdateBackWear(True)
                elif self.weaponInHandState() == gametypes.WEAR_WAIST_ATTACH:
                    self.innerUpdateWaistWear(True)
                else:
                    self.switchWeaponState(gametypes.WEAPON_HANDFREE, True)

    def cancelWeaponTimer(self):
        if not self.inCombat:
            if self.inWeaponCallback:
                BigWorld.cancelCallback(self.inWeaponCallback)
                self.inWeaponCallback = None

    def cancelWeaponTimerAndHangUpWeapon(self):
        if not self.inCombat:
            if self.inWeaponCallback:
                BigWorld.cancelCallback(self.inWeaponCallback)
                self.inWeaponCallback = None
            self.switchWeaponState(gametypes.WEAPON_HANDFREE, False)

    def delayCancelWeaponTimerAndHangUpWeapon(self):
        if self.delayHangupWeapon:
            self.cancelWeaponTimerAndHangUpWeapon()
            self.delayHangupWeapon = False

    def propSchemeSend(self, data):
        pass

    def onSkillEnhancePointBonus(self, nPoint, skillEnhancePointBonus):
        self.skillEnhancePointBonus = skillEnhancePointBonus
        if gameglobal.rds.ui.xiuLianAward.mediator:
            gameglobal.rds.ui.xiuLianAward.refreshIcon(nPoint)
        self.updateRewardHallInfo(uiConst.REWARD_XIULIAN)

    def equipSoulSchemeSend(self, data):
        pass

    def onThrownIsolatedCreationPos(self, pos):
        pass

    def onThrownIsolatedCreationEff(self, data):
        pass

    def pathFindingTo(self, seekPos, spaceNo):
        pass

    def getMethodFactorByModeID(self, subSysID, modeID):
        rebalanceData = BMD.data.get(subSysID, {})
        if not rebalanceData.get('method') or not rebalanceData.get('factor'):
            return (0, 0)
        methodID = rebalanceData.get('method')[modeID - 1]
        factor = rebalanceData.get('factor')[modeID - 1]
        return (methodID, factor)

    def onGetCanRemoveSkillEnhances(self, data):
        """
        \xe8\x8e\xb7\xe5\xbe\x97\xe5\x8f\xaf\xe5\x8d\xb8\xe4\xb8\x8b\xe6\x8a\x80\xe8\x83\xbd\xe4\xbf\xae\xe7\x82\xbc\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param data: \xe4\xb8\x80\xe4\xb8\xaadict\xef\xbc\x8cdata[school][skillId] = [part1, part2, ...]
        """
        gamelog.debug('@xzh onGetCanRemoveSkillEnhances', data)
        self.canRemoveSkillEnhances = data
        gameglobal.rds.ui.skill.refreshSkillPracticeInfo(gameglobal.rds.ui.skill.skillId)

    def onRemoveSkillEnhance(self, school, skillId, part):
        """
        \xe6\x88\x90\xe5\x8a\x9f\xe5\x8d\xb8\xe4\xb8\x8b\xe6\x8a\x80\xe8\x83\xbd\xe4\xbf\xae\xe7\x82\xbc\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83\xef\xbc\x8c\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe6\x8a\x80\xe8\x83\xbd\xe4\xbf\xae\xe7\x82\xbc\xe5\x92\x8c\xe6\x8a\x80\xe8\x83\xbd\xe9\xa1\xb5\xe6\x95\xb0\xe6\x8d\xae\xe7\x9a\x84\xe4\xbf\xae\xe6\x94\xb9\xe5\x86\x8d\xe6\xac\xa1\xe4\xb9\x8b\xe5\x89\x8d\xe5\xb7\xb2\xe5\xae\x8c\xe6\x88\x90
        :param school: 
        :param skillId: 
        :param part: 
        """
        gamelog.debug('@xzh onRemoveSkillEnhance', school, skillId, part)
        if self.canRemoveSkillEnhances.has_key(school) and self.canRemoveSkillEnhances[school].has_key(skillId) and part in self.canRemoveSkillEnhances[school][skillId]:
            self.canRemoveSkillEnhances.setdefault(school, {})[skillId].remove(part)
        gameglobal.rds.ui.skill.refreshSkillPracticeInfo(gameglobal.rds.ui.skill.skillId)

    def onConditionalPropEnable(self, condPropId, condPropVal):
        """
        \xe6\x9d\xa1\xe4\xbb\xb6\xe5\xb1\x9e\xe6\x80\xa7\xe7\x94\x9f\xe6\x95\x88\xe6\x97\xb6\xe8\xb0\x83\xe7\x94\xa8     
        :param condPropId: \xe6\x9d\xa1\xe4\xbb\xb6\xe5\xb1\x9e\xe6\x80\xa7id\xef\xbc\x88\xe5\x8f\xaf\xe8\x83\xbd\xe6\x8d\x86\xe7\xbb\x91\xe5\xa4\x9a\xe6\x9d\xa1\xe5\xb1\x9e\xe6\x80\xa7\xef\xbc\x8c\xe8\xa7\x81attrIds\xe5\xad\x97\xe6\xae\xb5\xef\xbc\x89 
        :param condPropVal: \xe6\x9d\xa1\xe4\xbb\xb6\xe5\xb1\x9e\xe6\x80\xa7\xe5\x80\xbc
        """
        gamelog.debug('@zq onConditionalPropEnable', condPropId, condPropVal)
        if not condPropVal:
            return
        else:
            msgArgs = self._getConditionPropMsgArgs(condPropId, condPropVal, True, None)
            if msgArgs:
                self.handleCombatMsg(msgArgs)
                if not hasattr(self, 'conditionalPropTips'):
                    self.conditionalPropTips = {}
                self.conditionalPropTips[condPropId] = msgArgs
                if not hasattr(self, 'conditionalPropTime'):
                    self.conditionalPropTime = {}
                self.conditionalPropTime[condPropId] = utils.getNow()
            self.refreshConditionalIcon()
            gameglobal.rds.ui.buffListenerShow.refreshInfo()
            return

    def onConditionalPropDisable(self, condPropId, condPropVal):
        """
        \xe6\x9d\xa1\xe4\xbb\xb6\xe5\xb1\x9e\xe6\x80\xa7\xe5\xa4\xb1\xe6\x95\x88\xe6\x97\xb6\xe8\xb0\x83\xe7\x94\xa8
        :param condPropId: \xe6\x9d\xa1\xe4\xbb\xb6\xe5\xb1\x9e\xe6\x80\xa7id\xef\xbc\x88\xe5\x8f\xaf\xe8\x83\xbd\xe6\x8d\x86\xe7\xbb\x91\xe5\xa4\x9a\xe6\x9d\xa1\xe5\xb1\x9e\xe6\x80\xa7\xef\xbc\x8c\xe8\xa7\x81attrIds\xe5\xad\x97\xe6\xae\xb5\xef\xbc\x89 
        :param condPropVal: \xe6\x9d\xa1\xe4\xbb\xb6\xe5\xb1\x9e\xe6\x80\xa7\xe5\x80\xbc
        """
        msgArgs = self._getConditionPropMsgArgs(condPropId, condPropVal, False, None)
        if msgArgs:
            self.handleCombatMsg(msgArgs)
        if getattr(self, 'conditionalPropTips', None) and condPropId in self.conditionalPropTips:
            del self.conditionalPropTips[condPropId]
        if getattr(self, 'conditionalPropTime', None) and condPropId in self.conditionalPropTime:
            del self.conditionalPropTime[condPropId]
        self.refreshConditionalIcon()
        gameglobal.rds.ui.buffListenerShow.refreshInfo()

    def onConditionalPropUpdate(self, condPropId, condPropVal, currPropVal, isEnable):
        """
        \xe6\x9d\xa1\xe4\xbb\xb6\xe5\xb1\x9e\xe6\x80\xa7\xe5\xa4\xb1\xe6\x95\x88\xe6\x97\xb6\xe8\xb0\x83\xe7\x94\xa8
        :param condPropId: \xe6\x9d\xa1\xe4\xbb\xb6\xe5\xb1\x9e\xe6\x80\xa7id\xef\xbc\x88\xe5\x8f\xaf\xe8\x83\xbd\xe6\x8d\x86\xe7\xbb\x91\xe5\xa4\x9a\xe6\x9d\xa1\xe5\xb1\x9e\xe6\x80\xa7\xef\xbc\x8c\xe8\xa7\x81attrIds\xe5\xad\x97\xe6\xae\xb5\xef\xbc\x89
        :param condPropVal: \xe5\x8f\x98\xe5\x8c\x96\xe5\x80\xbc
        :param currPropVal \xe5\xbd\x93\xe5\x89\x8d\xe5\x80\xbc
        :param isEnable \xe5\xb1\x9e\xe6\x80\xa7\xe6\x98\xaf\xe5\x90\xa6\xe6\x98\xaf\xe5\x8a\xa0
        """
        msgArgs = self._getConditionPropMsgArgs(condPropId, condPropVal, isEnable, None)
        currArgs = self._getConditionPropMsgArgs(condPropId, currPropVal, isEnable, None)
        if msgArgs:
            self.handleCombatMsg(msgArgs)
            if not hasattr(self, 'conditionalPropTips'):
                self.conditionalPropTips = {}
            self.conditionalPropTips[condPropId] = currArgs
            if not hasattr(self, 'conditionalPropTime'):
                self.conditionalPropTime = {}
            self.conditionalPropTime[condPropId] = utils.getNow()
        self.refreshConditionalIcon()
        gameglobal.rds.ui.buffListenerShow.refreshInfo()

    def onSpriteConditionalPropEnable(self, condPropId, condPropVal, name):
        """
        \xe8\x8b\xb1\xe7\x81\xb5\xe6\x9d\xa1\xe4\xbb\xb6\xe5\xb1\x9e\xe6\x80\xa7\xe7\x94\x9f\xe6\x95\x88\xe6\x97\xb6\xe8\xb0\x83\xe7\x94\xa8
        """
        if not condPropVal:
            return
        msgArgs = self._getConditionPropMsgArgs(condPropId, condPropVal, True, name)
        if msgArgs:
            self.handleCombatMsg(msgArgs)

    def onSpriteConditionalPropDisable(self, condPropId, condPropVal, name):
        """
        \xe8\x8b\xb1\xe7\x81\xb5\xe6\x9d\xa1\xe4\xbb\xb6\xe5\xb1\x9e\xe6\x80\xa7\xe5\xa4\xb1\xe6\x95\x88\xe6\x97\xb6\xe8\xb0\x83\xe7\x94\xa8
        """
        msgArgs = self._getConditionPropMsgArgs(condPropId, condPropVal, False, name)
        if msgArgs:
            self.handleCombatMsg(msgArgs)

    def onSpriteConditionalPropUpdate(self, condPropId, condPropVal, currPropVal, name, isEnable):
        """
        \xe8\x8b\xb1\xe7\x81\xb5\xe6\x9d\xa1\xe4\xbb\xb6\xe5\xb1\x9e\xe6\x80\xa7\xe5\x8f\x98\xe6\x9b\xb4\xe6\x97\xb6\xe8\xb0\x83\xe7\x94\xa8
        """
        if not condPropVal:
            return
        msgArgs = self._getConditionPropMsgArgs(condPropId, condPropVal, isEnable, name)
        if msgArgs:
            self.handleCombatMsg(msgArgs)

    def refreshConditionalIcon(self):
        tmpDict = self.conditionalPropTips
        self.conditionalPropTips = {}
        self.delConditionalStateIcon()
        self.conditionalPropTips = tmpDict
        if self.conditionalPropTips:
            self.addConditionalPropStateIcon()

    def _getConditionPropMsgArgs(self, condPropId, condPropVal, isEnable, name):
        condPropData = CPD.data.get(condPropId, {})
        lastTime = condPropData.get('lastTime')
        msgArgs = []
        for propRefId in condPropData.get('attrIds', ()):
            PRData = PRD.data.get(propRefId, {})
            shortName = PRData.get('shortName', '')
            showType = PRData.get('showType', 0)
            showVal = uiUtils.formatProp(condPropVal, 0, showType)
            if name:
                if isEnable:
                    if lastTime:
                        msgArgs.append((GMDD.data.COMBAT_MSG_SPRITE_CONDITIONAL_PROP_ENABLE_WITH_LASTTIME, (name,
                          shortName,
                          showVal,
                          lastTime)))
                    else:
                        msgArgs.append((GMDD.data.COMBAT_MSG_SPRITE_CONDITIONAL_PROP_ENABLE, (name, shortName, showVal)))
                else:
                    msgArgs.append((GMDD.data.COMBAT_MSG_SPRITE_CONDITIONAL_PROP_DISABLE, (name, shortName, showVal)))
            elif isEnable:
                if lastTime:
                    msgArgs.append((GMDD.data.COMBAT_MSG_CONDITIONAL_PROP_ENABLE_WITH_LASTTIME, (shortName, showVal, lastTime)))
                else:
                    msgArgs.append((GMDD.data.COMBAT_MSG_CONDITIONAL_PROP_ENABLE, (shortName, showVal)))
            else:
                msgArgs.append((GMDD.data.COMBAT_MSG_CONDITIONAL_PROP_DISABLE, (shortName, showVal)))

        return msgArgs

    def onGetTempPskill(self, data):
        gamelog.debug('@dxk onGetArenaTempPskill', data)
        gameglobal.rds.ui.arenaPskillHover.onGetArenaTempPskill(data)

    def onQueryCombatDetail(self, data):
        gamelog.debug('@zhangkuo onQueryCombatDetail', data)
        gameglobal.rds.ui.fubenStat.updateTempStat(self.gbId, data)
        gameglobal.rds.ui.fubenStat.refreshSelfDpsSkillWnd()

    def onSendSpecialSkipVal(self, pType, pNum, pVal):
        """
        :param pType: \xe5\x8f\x82\xe8\x80\x83gametypes.py HEALTYPE_HP_STATE
        :param pNum: stateId \xe6\x88\x96\xe8\x80\x85 effectId\xef\xbc\x8c\xe7\x9c\x8btype
        :param pVal: \xe5\x85\xb7\xe4\xbd\x93\xe5\x80\xbc
        :return:
        """
        gamelog.debug('dxk onSendSpecialSkipVal', pType, pNum, pVal)
        if pType == gametypes.HEALTYPE_HP_STATE:
            gamelog.debug('healHp')
            self.otherHeal(pVal, pNum)
        else:
            gamelog.debug('healHp')
            self.otherHeal(pVal, 0)

    def onSyncRemainSkillCnt(self, remainCnt, stateId):
        """
        :param remianCnt: \xe5\xb1\x9e\xe6\x80\xa7\xe6\x8f\x90\xe5\x8d\x87\xe5\x89\xa9\xe4\xbd\x99\xe6\x8a\x80\xe8\x83\xbd\xe4\xbd\xbf\xe7\x94\xa8\xe6\xac\xa1\xe6\x95\xb0
        :param stateId:
        :return:
        """
        gamelog.debug('dxk@onSyncRemainSkillCnt', remainCnt, stateId)
        if remainCnt <= 0 and self.stateSECount.has_key(stateId):
            del self.stateSECount[stateId]
            self.set_statesServerAndOwn(self.statesServerAndOwn)
        elif remainCnt > 0:
            self.stateSECount[stateId] = remainCnt
            self.set_statesServerAndOwn(self.statesServerAndOwn)

    def onUpdateNoMpSpecialState(self, remainCnt):
        gamelog.info('jbx:onUpdateNoMpSpecialState', remainCnt)
        setattr(self, 'noMpSpecialStateCnt', remainCnt)
        gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_LACK_ENERGY)

    def updateSkillCDDecrease(self, param):
        gamelog.info('jbx:updateSkillCDDecrease', param)
        self.skillCDDecrease = param
