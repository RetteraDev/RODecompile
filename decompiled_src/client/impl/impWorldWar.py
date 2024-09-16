#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impWorldWar.o
from gamestrings import gameStrings
import BigWorld
import math
import random
import const
import utils
import gametypes
import gameglobal
import commonWorldWar
import formula
import logicInfo
import npcConst
from guis import uiConst
from guis import uiUtils
from commonWorldWar import WWArmyCandidateVal, WWArmyPostVal, WWArmySkillVal
from cdata import game_msg_def_data as GMDD
from data import world_war_config_data as WWCD
from data import activity_basic_data as ABD
from data import world_war_fort_data as WWFD
from data import world_war_relive_board_data as WWRBD
from data import world_war_army_data as WWAD
from data import skill_general_data as SGD
from data import state_data as SD
SHOW_COUNT = [60, 30, 10]

def cmpHire(c1, c2):
    r = cmp(c1[1], c2[1])
    if r:
        return r
    r = cmp(c1[2], c2[2])
    if r:
        return r
    r = cmp(c1[-1], c2[-1])
    return r


class ImpWorldWar(object):

    def inWorldWar(self):
        return formula.spaceInWorldWar(self.spaceNo)

    def inWorldWarBattle(self):
        return formula.spaceInWorldWarBattle(self.spaceNo)

    def inWorldWarEx(self):
        return self.spaceNo in const.SPACE_NO_WORLD_WAR_ALL

    def getWorldWarCamp(self):
        if self.inWorldWarBattle():
            return self.worldWar.getBattleCamp()
        else:
            return self.worldWar.getCamp()

    def getWorldWarSide(self):
        if self._isSoul() or self._isReturn():
            if BigWorld.player().inWorldWarBattle():
                if self.wbHireHostId == utils.getCurrHostId():
                    return gametypes.WORLD_WAR_CAMP_DEFEND
                else:
                    return gametypes.WORLD_WAR_CAMP_ATTACK
            else:
                return gametypes.WORLD_WAR_CAMP_ATTACK
        else:
            return gametypes.WORLD_WAR_CAMP_DEFEND

    def getWorldWarSideByHostId(self, hostId):
        if not hostId:
            return 0
        elif hostId != utils.getCurrHostId():
            return gametypes.WORLD_WAR_CAMP_ATTACK
        else:
            return gametypes.WORLD_WAR_CAMP_DEFEND

    def getWBHostId(self):
        return self.wbHireHostId or utils.getHostId()

    def _getWBHireHostId(self):
        if self.wbHireHostId != utils.getHostId():
            return self.wbHireHostId
        else:
            return 0

    def getWBHireState(self):
        if self.wbHireHostId == 0:
            return gametypes.WB_HIRE_UNHIRED
        if self.wbHireHostId != utils.getHostId():
            return gametypes.WB_HIRE_OTHER_HOST
        return gametypes.WB_HIRE_OWN_HOST

    def getWorldWarTempCamp(self):
        return self.worldWar.getCurrCamp()

    def getWorldWarQuestStarLv(self):
        """
                        \xe8\x8e\xb7\xe5\x8f\x96\xe5\x9b\xbd\xe6\x88\x98\xe4\xbb\xbb\xe5\x8a\xa1\xe9\x9a\xbe\xe5\xba\xa6\xe7\xad\x89\xe7\xba\xa7
        """
        return self.worldWar.questStarLv or 1

    def onWorldWarStateUpdate(self, state):
        oldState = self.worldWar.state
        self.worldWar.state = state
        gameglobal.rds.ui.worldWar.onStateUpdate()
        if oldState != state:
            if state == gametypes.WORLD_WAR_STATE_APPLY_BID:
                self.worldWar.reset()
                self.showGameMsg(GMDD.data.WORLD_WAR_START_APPLY_BID, ())
            elif state == gametypes.WORLD_WAR_STATE_OPEN:
                self.showGameMsg(GMDD.data.WORLD_WAR_TURN_TO_OPEN, ())

    def onWorldWarBattleStateUpdate(self, state):
        self.worldWar.battleStateDict = state
        for wwtype, battleState in state.iteritems():
            if not gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
                if wwtype == gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG:
                    continue
            if formula.spaceInWorldWarBattleOld(self.spaceNo):
                if wwtype == gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG:
                    continue
            if formula.spaceInWorldWarBattleYoung(self.spaceNo):
                if wwtype == gametypes.WORLD_WAR_TYPE_BATTLE:
                    continue
            self._onWorldWarBattleStateUpdate(battleState, self.worldWar.battleState)

    def _onWorldWarBattleStateUpdate(self, state, oldState):
        self.worldWar.battleState = state
        if oldState != state:
            if state == gametypes.WORLD_WAR_BATTLE_STATE_APPLY:
                self.worldWar.battleHireStopped = False
                self.showGameMsg(GMDD.data.WORLD_WAR_BATTLE_START_APPLY, ())
            elif state == gametypes.WORLD_WAR_BATTLE_STATE_OPEN:
                self.worldWar.battleHireStopped = False
                self.showGameMsg(GMDD.data.WORLD_WAR_BATTLE_TURN_TO_OPEN, ())
                gameglobal.rds.ui.showPicTip(gametypes.WWB_TIP_START)
            gameglobal.rds.ui.worldWar.onBattleStateUpdate()

    def checkCanQuickJoinWorldWarGroup(self):
        if not gameglobal.rds.configData.get('enableWorldWarQuickJoinGroup', False):
            return False
        if not self.inWorldWar():
            return False
        if self.groupNUID > 0:
            return False
        return True

    def onWorldWarApplicantUpdate(self, applyGbId, applyRoleName):
        self.worldWar.applyGbId = applyGbId
        self.worldWar.applyRoleName = applyRoleName

    def onWorldWarNotifyState(self, state, roundNum):
        pushMsg = gameglobal.rds.ui.pushMessage
        if state == gametypes.WORLD_WAR_STATE_APPLY_BID:
            pushMsg.addPushMsg(uiConst.MESSAGE_TYPE_WW_NO_BID)
        elif state == gametypes.WORLD_WAR_STATE_APPLY_TARGETS:
            if not self.worldWar.isLucky():
                if roundNum == 1:
                    pushMsg.addPushMsg(uiConst.MESSAGE_TYPE_WW_APPLY_TARGET)
                else:
                    pushMsg.addPushMsg(uiConst.MESSAGE_TYPE_WW_MATCH_FAIL)

    def onWorldWarBeforeOpenNotify(self, tStart):
        self.wwStartTime = tStart
        self.wwCountDown()

    def wwCountDown(self):
        wwCountTimer = int(math.ceil(max(0, self.wwStartTime - self.getServerTime())))
        if getattr(self, 'wwCallback', None):
            BigWorld.cancelCallback(self.wwCallback)
        if wwCountTimer in SHOW_COUNT and self.inWorld:
            gameglobal.rds.ui.showPicTip(gametypes.WW_TIP_CAMP_WILL_CHANGE)
        if self.inWorld and wwCountTimer > 0:
            self.wwCallback = BigWorld.callback(1, self.wwCountDown)

    def onWorldWarSyncData(self, data):
        cdata = data.pop('country', None)
        if cdata:
            for hostId, hdata in cdata:
                c = self.worldWar.getCountry(hostId)
                c.updateData(hdata)

        for attr, v in data.iteritems():
            setattr(self.worldWar, attr, v)

        gameglobal.rds.ui.worldWar.refreshChallege()

    def onWorldWarApplyTargetsStart(self, applyTargetsRoundNum, applyTargetsEndTime):
        """
                        \xe9\x80\x9a\xe7\x9f\xa5\xe5\xbc\x80\xe5\xa7\x8b\xe5\x8f\x91\xe8\xb5\xb7\xe6\x8c\x91\xe6\x88\x98
        """
        self.worldWar.state = gametypes.WORLD_WAR_STATE_APPLY_TARGETS
        self.worldWar.intentTargets = []
        self.worldWar.applyTargetsRoundNum = applyTargetsRoundNum
        self.worldWar.applyTargetsEndTime = applyTargetsEndTime
        if self.worldWar.getEnemyHostId():
            return
        if self.worldWar.isLucky():
            return
        self.showGameMsg(GMDD.data.WORLD_WAR_START_APPLY_TARGETS, ())
        if applyTargetsRoundNum > 1:
            gameglobal.rds.ui.worldWar.applyEndTargetEnd()

    def onWorldWarApplyCamp(self, camp, luckyHostId):
        self.worldWar.getCountry().camp = camp
        self.worldWar.getCountry().currCamp = commonWorldWar.getEnemyCamp(camp)
        self.worldWar.luckyHostId = luckyHostId
        for country in self.worldWar.country.itervalues():
            country.resetRecord()

        gameglobal.rds.ui.worldWar.refreshChallege()

    def onWorldWarApplyCamps(self, camps, luckyHostId):
        """
                        \xe9\x80\x9a\xe7\x9f\xa5\xe5\x88\x86\xe9\x98\xb5\xe8\x90\xa5
        """
        self.worldWar.country.applyCamps(camps)
        self.worldWar.luckyHostId = luckyHostId
        if self.worldWar.isLucky():
            gameglobal.rds.ui.worldWar.showLucky()
        gameglobal.rds.ui.worldWar.refreshChallege()
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WW_BID_END)

    def onWorldWarApplyMatch(self, enemyHostId, questStarLv, enemyQuestStarLv):
        c = self.worldWar.getCountry()
        c.enemyHostId = enemyHostId
        self.worldWar.lastEnemyHostId = enemyHostId
        self.worldWar.questStarlv = questStarLv
        self.worldWar.enemyQuestStarLv = enemyQuestStarLv
        ec = self.worldWar.getCountry(enemyHostId)
        ec.enemyHostId = c.hostId
        ec.camp = commonWorldWar.getEnemyCamp(c.camp)
        gameglobal.rds.ui.worldWar.refreshChallege()
        if self.worldWar.applyGbId == self.gbId:
            gameglobal.rds.ui.worldWar.applyEndTargetEnd()

    def onWorldWarMatchNotify(self, enemyHostId, declarePoint, bidDeclarePoint, applyRoleName, monthRank, inBloodWeek):
        self.worldWar.bidDeclarePoint = bidDeclarePoint
        self.worldWar.applyRoleName = applyRoleName
        self.worldWar.monthRank = monthRank
        c = self.worldWar.getCountry()
        c.declarePoint = declarePoint
        c.enemyHostId = enemyHostId
        if inBloodWeek:
            msg = uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_IN_BLOOD_WEEK_MSG)
            gameglobal.rds.ui.messageBox.showAlertBox(msg)
        else:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WW_MATCH_SUCC)

    def onWorldWarApplyMatches(self, matches):
        """
                        \xe9\x80\x9a\xe7\x9f\xa5\xe6\x9c\x80\xe6\x96\xb0\xe5\x8c\xb9\xe9\x85\x8d\xe7\xbb\x93\xe6\x9e\x9c
        """
        self.worldWar.country.applyMatches(matches)
        gameglobal.rds.ui.worldWar.onApplyMatches()

    def onWorldWarApplyBidOK(self, params):
        """
                        \xe7\xab\x9e\xe4\xbb\xb7\xe6\x88\x90\xe5\x8a\x9f
        """
        declarePoint, bidDeclarePoint = params
        c = self.worldWar.getCountry()
        c.declarePoint = declarePoint
        c.bidDeclarePoint = bidDeclarePoint
        self.showGameMsg(GMDD.data.WORLD_WAR_APPLY_BID_OK, (bidDeclarePoint,))
        gameglobal.rds.ui.worldWar.refreshChallege()

    def onWorldWarApplyTargets(self, hostIds):
        """
                        \xe5\x8f\x91\xe8\xb5\xb7\xe6\x8c\x91\xe6\x88\x98\xe6\x88\x90\xe5\x8a\x9f
        """
        self.worldWar.intentTargets = hostIds
        gameglobal.rds.ui.worldWar.refreshChallege()
        self.showGameMsg(GMDD.data.WORLD_WAR_APPLY_TARGETS_OK, ())

    def onWorldWarSwitchCamp(self, currCamp):
        oldCamp = self.getWorldWarTempCamp()
        if self._isSoul():
            currCamp = commonWorldWar.getEnemyCamp(currCamp)
            self.worldWar.switchCamp(currCamp)
        else:
            self.worldWar.switchCamp(currCamp)
        self.onQuestInfoModifiedAtClient(const.QD_WW_CAMP, exData={'wwTempCamp': [oldCamp, currCamp]})
        if currCamp == gametypes.WORLD_WAR_CAMP_ATTACK:
            gameglobal.rds.ui.showPicTip(gametypes.WW_TIP_CAMP_ATTACK)
        elif currCamp == gametypes.WORLD_WAR_CAMP_DEFEND:
            gameglobal.rds.ui.showPicTip(gametypes.WW_TIP_CAMP_DEFEND)

    def onQueryWorldWar(self, dto, bInit, ver):
        """
                        \xe8\xbf\x94\xe5\x9b\x9e\xe6\x9f\xa5\xe8\xaf\xa2\xe5\x9f\xba\xe6\x9c\xac\xe4\xbf\xa1\xe6\x81\xaf
        """
        oldCamp = self.getWorldWarTempCamp()
        oldBattleState = self.worldWar.battleState
        self.worldWar.fromDTO(dto)
        self._onWorldWarBattleStateUpdate(self.worldWar.battleState, oldBattleState)
        self.worldWar.ver = ver
        currCamp = self.getWorldWarTempCamp()
        self.onQuestInfoModifiedAtClient(const.QD_WW_CAMP, exData={'wwTempCamp': [oldCamp, currCamp]})
        actIds = []
        for activityId in ABD.data.keys():
            activityData = ABD.data[activityId]
            if activityId in WWCD.data.get('scheduleBlackList', ()) and (not gameglobal.rds.configData.get('enableWorldWar') or self.worldWar.state == gametypes.WORLD_WAR_STATE_CLOSE):
                actIds.append(activityId)

        actIds and self.setupActivityNotify(actIds, includeWorldWarActs=True)
        if formula.spaceInWorldWarBattle(self.spaceNo) or formula.spaceInWorldWarRob(self.spaceNo):
            gameglobal.rds.ui.littleMap.addWWReliveIcon()
            if formula.spaceInWorldWarBattle(self.spaceNo):
                gameglobal.rds.ui.littleMap.addWWBattleIcon()
            else:
                gameglobal.rds.ui.littleMap.addWWRBattleIcon()

    def onQueryWorldWarVolatile(self, dto, ver):
        mp, mpUsedDTO = dto
        self.worldWar.volatileVer = ver
        c = self.worldWar.getCountry()
        c.mp = mp
        self.worldWar.clearMpUsed()
        for postId, mpUsed in mpUsedDTO:
            post = self.worldWar.getArmyByPostId(postId)
            if post:
                post.mpUsed = mpUsed

    def onQueryWorldWarKeep(self):
        pass

    def onQueryWorldWarCountries(self, dto, countryVer):
        """
                        \xe8\xbf\x94\xe5\x9b\x9e\xe6\x9f\xa5\xe8\xaf\xa2\xe5\x9b\xbd\xe5\xae\xb6\xe4\xbf\xa1\xe6\x81\xaf
        """
        self.worldWar.country.fromDTO(dto)
        self.worldWar.countryVer = countryVer
        gameglobal.rds.ui.worldWar.refreshChallege()

    def onQueryWorldWarCountriesKeep(self):
        pass

    def _enterWorldWarOwn(self):
        if not self.worldWar.isOpen():
            self.showGameMsg(GMDD.data.WORLD_WAR_NOT_OPEN, ())
            return
        if self.worldWar.isLucky():
            self.showGameMsg(GMDD.data.WORLD_WAR_ENTER_LUCKY, ())
            return
        self.cell.enterWorldWar(self.worldWar.getCamp())

    def _enterWorldWarEnemy(self):
        if not self.worldWar.isOpen():
            self.showGameMsg(GMDD.data.WORLD_WAR_NOT_OPEN, ())
            return
        if self.worldWar.isLucky():
            self.showGameMsg(GMDD.data.WORLD_WAR_ENTER_LUCKY, ())
            return
        self.cell.enterWorldWar(self.worldWar.getEnemyCamp())

    def onWorldWarQueueReady(self, wwtype, hostId, countDown, macResult):
        self.worldWar.wwqorders[wwtype] = (0, 0, 0)
        if wwtype == gametypes.WORLD_WAR_TYPE_NORMAL:
            gameglobal.rds.ui.worldWar.onWorldWarQueueReady(hostId, countDown, macResult)
        elif wwtype == gametypes.WORLD_WAR_TYPE_BATTLE or wwtype == gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG:
            gameglobal.rds.ui.worldWar.onWorldWarBattleQueueReady(wwtype, countDown, macResult)
        elif wwtype == gametypes.WORLD_WAR_TYPE_ROB or wwtype == gametypes.WORLD_WAR_TYPE_ROB_YOUNG:
            gameglobal.rds.ui.worldWar.onWorldWarRobQueueReady(wwtype, hostId, countDown, macResult)

    def onWorldWarQueueOrderUpdate(self, wwtype, orderInfo):
        self.worldWar.wwqorders[wwtype] = orderInfo.get('order')
        if wwtype == gametypes.WORLD_WAR_TYPE_NORMAL:
            gameglobal.rds.ui.worldWar.onWorldWarQueueOrderUpdate(wwtype)
        elif wwtype == gametypes.WORLD_WAR_TYPE_BATTLE or wwtype == gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG:
            self.worldWar.showBattleQueueMsg(wwtype)
            gameglobal.rds.ui.worldWar.onWorldWarQueueOrderUpdate(wwtype, orderInfo.get('macResult', 0))
        elif wwtype == gametypes.WORLD_WAR_TYPE_ROB or wwtype == gametypes.WORLD_WAR_TYPE_ROB_YOUNG:
            gameglobal.rds.ui.worldWar.onWorldWarQueueOrderUpdate(wwtype, orderInfo.get('macResult', 0))

    def onWorldWarEnterQueue(self, wwtype, orderInfo):
        self.worldWar.wwqorders[wwtype] = orderInfo.get('order')
        if wwtype == gametypes.WORLD_WAR_TYPE_NORMAL:
            gameglobal.rds.ui.worldWar.onWorldWarEnterQueue(wwtype)
            self.showGameMsg(GMDD.data.WORLD_WAR_ENTER_QUEUE_OK, ())
        elif wwtype == gametypes.WORLD_WAR_TYPE_BATTLE:
            gameglobal.rds.ui.worldWar.onWorldWarEnterQueue(wwtype, orderInfo.get('macResult', 0))
            self.showGameMsg(GMDD.data.WORLD_WAR_BATTLE_ENTER_QUEUE_OK, ())
        elif wwtype == gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG:
            gameglobal.rds.ui.worldWar.onWorldWarEnterQueue(wwtype, orderInfo.get('macResult', 0))
            self.showGameMsg(GMDD.data.WORLD_WAR_BATTLE_ENTER_QUEUE_OK, ())
        elif wwtype == gametypes.WORLD_WAR_TYPE_ROB:
            gameglobal.rds.ui.worldWar.onWorldWarEnterQueue(wwtype)
            self.showGameMsg(GMDD.data.WORLD_WAR_ROB_QUEUE_OK, ())
        elif wwtype == gametypes.WORLD_WAR_TYPE_ROB_YOUNG:
            gameglobal.rds.ui.worldWar.onWorldWarEnterQueue(wwtype)
            self.showGameMsg(GMDD.data.WORLD_WAR_ROB_QUEUE_OK, ())

    def onWorldWarComboKill(self, cnt):
        if cnt > 0:
            gameglobal.rds.ui.continuousHit.showCombokill(cnt)

    def sendWorldWarKillAvatar(self, killAvatarCnt, killAvatarCntTotal, wwscore, maxComboKill):
        self.worldWar.killAvatarCnt = killAvatarCnt
        self.worldWar.killAvatarCntTotal = killAvatarCntTotal
        self.worldWar.wwscore = wwscore
        self.worldWar.maxComboKill = maxComboKill

    def sendWorldWarBattleScore(self, score, kill, assist, res):
        self.worldWar.battleScore = score
        self.worldWar.battleKillAvatar = kill
        self.worldWar.battleAssist = assist
        self.worldWar.battleRes = res
        gameglobal.rds.ui.worldWar.refreshWWBattleScore()

    def onQueryWorldWarKillAvatarRank(self, weeklyRank, weeklySchoolRank, totalRank, totalSchoolRank):
        self.worldWar.weeklyKillAvatarRank = weeklyRank
        self.worldWar.weeklyKillAvatarSchoolRank = weeklySchoolRank
        self.worldWar.totalKillAvatarRank = totalRank
        self.worldWar.totalKillAvatarSchoolRank = totalSchoolRank

    def onWorldWarQueryRecordKeep(self):
        pass

    def onWorldWarQueryRecord(self, records, ver):
        for hostId, record in records.iteritems():
            self.worldWar.getCountry(hostId).record = record

        self.worldWar.recalcScore()
        self.worldWar.recordVer = ver

    def onQueryWorldWarRankKeep(self):
        pass

    def onQueryWorldWarRank(self, data, ver):
        self.worldWar.rank = data
        self.worldWar.rankVer = ver

    def onWorldWarGroupUpdate(self, groupId):
        self.worldWar.getCountry().groupId = groupId

    def onWorldWarGroupUpgrade(self, groupId):
        self.worldWar.getCountry().groupId = groupId

    def onWorldWarGroupDegrade(self, groupId):
        self.worldWar.getCountry().groupId = groupId

    def onWorldWarBattleFortUpdate(self, fortData, fortVer):
        self.worldWar.fortVer = fortVer
        for fortId, hostId, inCombat in fortData:
            fort = self.worldWar.getFort(fortId)
            oldHostId = fort.hostId
            fort.hostId = hostId
            fort.inCombat = inCombat
            if len(fortData) == 1 and self.inWorldWarBattle() and oldHostId != fort.hostId:
                if hostId == self.getWBHostId():
                    picTip = WWFD.data.get(fortId, {}).get('picTip', 0)
                    self.showGameMsg(GMDD.data.WORLD_WAR_BATTLE_OCCUPY, (WWFD.data.get(fortId, {}).get('name'),))
                else:
                    picTip = WWFD.data.get(fortId, {}).get('eneymyPicTip', 0)
                    self.showGameMsg(GMDD.data.WORLD_WAR_BATTLE_OCCUPY_BY_ENEMY, (WWFD.data.get(fortId, {}).get('name'),))
                gameglobal.rds.ui.showPicTip(picTip)

        gameglobal.rds.ui.worldWar.refreshWWBattleFort()

    def onWorldWarBattleReliveBoardUpdate(self, reliveBoardData, fortVer):
        self.worldWar.fortVer = fortVer
        for rbId, hostId in reliveBoardData:
            self.worldWar.reliveBoard[rbId] = hostId
            if len(reliveBoardData) == 1 and self.inWorldWarEx():
                if hostId == self.getWBHostId():
                    picTip = WWRBD.data.get(rbId, {}).get('picTip', 0)
                    self.showGameMsg(GMDD.data.WORLD_WAR_BATTLE_OCCUPY, (WWRBD.data.get(rbId, {}).get('name'),))
                else:
                    picTip = WWRBD.data.get(rbId, {}).get('eneymyPicTip', 0)
                    self.showGameMsg(GMDD.data.WORLD_WAR_BATTLE_OCCUPY_BY_ENEMY, (WWRBD.data.get(rbId, {}).get('name'),))
                gameglobal.rds.ui.showPicTip(picTip)

        gameglobal.rds.ui.worldWar.refreshWWBattleFort()

    def onWorldWarReliveBoardUpdate(self, reliveBoardData):
        self.onWorldWarBattleReliveBoardUpdate(reliveBoardData, 0)

    def onQueryWorldWarBattleFort(self, fortData, reliveBoardData, cdto, battleRes, battleMoraleIdx, battleEndTime, fortVer):
        if cdto:
            for dto in cdto:
                c = self.worldWar.getCountry(dto[0])
                c.fromSimpleDTO(dto)

        self.worldWar.getCountry().battleRes = battleRes
        oldBattleMoraleIdx = self.worldWar.battleMoraleIdx
        self.worldWar.battleMoraleIdx = battleMoraleIdx
        self.worldWar.battleEndTime = battleEndTime
        self.worldWar.fortVer = fortVer
        self.onWorldWarBattleFortUpdate(fortData, fortVer)
        self.onWorldWarBattleReliveBoardUpdate(reliveBoardData, fortVer)
        if oldBattleMoraleIdx != battleMoraleIdx:
            gameglobal.rds.ui.worldWar.refreshWWBattleScore()

    def onQueryWorldWarBattleFortKeep(self, battleRes):
        self.worldWar.getCountry().battleRes = battleRes

    def showOccupyItemIcon(self, entId):
        if self.inWingWarCity() and (not self.wingWorldPostId or not WWAD.data.has_key(self.wingWorldPostId)):
            return
        gameglobal.rds.ui.pressKeyF.targetId = entId
        gameglobal.rds.ui.pressKeyF.isOccupy = True
        gameglobal.rds.ui.pressKeyF.setType(const.F_OCCUPY)

    def hideOccupyItemIcon(self, entId):
        if gameglobal.rds.ui.pressKeyF.isOccupy == True:
            if gameglobal.rds.ui.pressKeyF.targetId == entId:
                gameglobal.rds.ui.pressKeyF.targetId = None
                gameglobal.rds.ui.pressKeyF.isOccupy = False
                gameglobal.rds.ui.pressKeyF.removeType(const.F_OCCUPY)

    def onStartWorldWarRelive(self, reliveInterval):
        gameglobal.rds.ui.deadAndRelive.hide()
        if gameglobal.rds.ui.fbDeadData.mediator:
            gameglobal.rds.ui.fbDeadData.hide()
        if gameglobal.rds.ui.fbDeadDetailData.mediator:
            gameglobal.rds.ui.fbDeadDetailData.hide()

    def onWorldWarBattleResult(self, tops, myRankAll, myRank, winnerCamp, scores, taskIds, attackHostId, defendHostId, wwtype):
        if gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
            if wwtype != self.recentEnterWWType:
                return
        wbHireHostId = self._getWBHireHostId()
        if wbHireHostId and wbHireHostId not in (attackHostId, defendHostId):
            return
        ww = gameglobal.rds.ui.worldWar
        ww.hideWorldWarBattle()
        ww.battleResultData = (tops,
         myRankAll,
         winnerCamp,
         scores,
         taskIds,
         myRank)
        ww.onShowWWBattleResult()
        if self.inWorldWarBattle():
            if winnerCamp == self.worldWar.getCamp():
                tip = gametypes.WWB_TIP_WIN
            else:
                tip = gametypes.WWB_TIP_LOSE
            gameglobal.rds.ui.showPicTip(tip)
        if self._getWBHireHostId():
            self.worldWar.battleHireStopped = True

    def reliveInWorldWar(self):
        self.cell.confirmRelive(gametypes.RELIVE_TYPE_BY_WORLD_WAR, True)

    def onQueryWorldWarArmyCandidate(self, data, ver, voteVer):
        self.worldWar.armyCandidate = []
        self.worldWar.gbId2AmryCandidate.clear()
        for dto in data:
            cVal = WWArmyCandidateVal(dto[0]).fromDTO(dto)
            self.worldWar.armyCandidate.append(cVal)
            self.worldWar.gbId2AmryCandidate[cVal.gbId] = cVal

        if self.worldWar.armyState == gametypes.WORLD_WAR_ARMY_STATE_VOTE:
            random.shuffle(self.worldWar.armyCandidate)
        else:
            self.worldWar.armyCandidate.sort(key=lambda x: x.votes * 100 - x.ctype * 10 - x.rank, reverse=True)
        self.worldWar.armyCandidateVer = ver
        self.worldWar.armyCandidateVoteVer = voteVer
        gameglobal.rds.ui.worldWar.refreshVoteList()

    def onQueryWorldWarArmyCandidateVote(self, voteData, voteVer):
        for gbId, votes, groupType in voteData:
            cVal = self.worldWar.gbId2AmryCandidate.get(gbId)
            if cVal:
                cVal.votes = votes

        self.worldWar.armyCandidateVoteVer = voteVer
        gameglobal.rds.ui.worldWar.refreshVoteList()

    def onQueryWorldWarArmy(self, dtos, voteResultEndTime, armyVer, armyOnlineVer):
        self.worldWar.getArmyFromDTO(dtos)
        self.worldWar.voteResultEndTime = voteResultEndTime
        self.worldWar.armyVer = armyVer
        self.worldWar.amryOnlineVer = armyOnlineVer
        self.worldWar.buildArmyIndex()

    def onQueryWorldWarArmyOnline(self, data, armyOnlineVer):
        for gbId, bOnline in data:
            val = self.worldWar.army.get(gbId)
            if val:
                val.bOnline = bOnline

        self.worldWar.amryOnlineVer = armyOnlineVer

    def onQueryWWArmyMark(self, armyMark, armyMarkVer):
        self.worldWar.armyMark.update(armyMark)
        self.worldWar.armyMarkVer = armyMarkVer

    def inWWBattleQueue(self):
        return sum(self.worldWar.wwqorders.get(gametypes.WORLD_WAR_TYPE_BATTLE, (0, 0, 0))) or self.worldWar.wwTicketHosts.get(gametypes.WORLD_WAR_TYPE_BATTLE, 0)

    def inWWQueue(self):
        return sum(self.worldWar.wwqorders.get(gametypes.WORLD_WAR_TYPE_BATTLE, (0, 0, 0))) or self.worldWar.wwTicketHosts.get(gametypes.WORLD_WAR_TYPE_NORMAL, 0)

    def inWWQueueByType(self, wwtype):
        return sum(self.worldWar.wwqorders.get(wwtype, (0, 0, 0))) or self.worldWar.wwTicketHosts.get(wwtype, 0)

    def onAppointWWArmyPostOK(self, gbId, dto):
        post = WWArmyPostVal().fromDTO(dto)
        self.worldWar.army[gbId] = post
        self.worldWar.buildArmyIndex()
        gameglobal.rds.ui.worldWar.onAppointWWArmyPostOK(gbId, post.postId)

    def onRemoveWWArmyPostOK(self, gbId, postId):
        if self.worldWar.army.has_key(gbId):
            self.worldWar.army.pop(gbId)
            subPostIds = WWAD.data.get(postId).get('subPostIds')
            if subPostIds:
                for subPostId in subPostIds:
                    self.worldWar.removeArmyByPostId(subPostId)

            self.worldWar.buildArmyIndex()
        gameglobal.rds.ui.worldWar.onRemoveWWArmyPostOK(gbId, postId)

    def onWWResignArmyPost(self, postId):
        self.onRemoveWWArmyPostOK(self.gbId, postId)

    def onSearchPlayerForArmyAppoint(self, infoList):
        gameglobal.rds.ui.wingWorldAppoint.setPlayerList(infoList)

    def onWWArmyVoteNotify(self):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WW_ARMY_VOTE_NOTIFY)

    def onGenWWArmyLeader(self):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WW_ARMY_VOTE_RESULT_NOTIFY)

    def onWWArmyMarkNotify(self):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WW_ARMY_MARK_NOTIFY)

    def onWWArmyCallNotify(self, srcPostId, srcRoleName):
        postName = WWAD.data.get(srcPostId, {}).get('name', '')
        msg = uiUtils.getTextFromGMD(GMDD.data.WW_ARMY_CALL_NOTIFY, '%s_%s') % (postName, srcRoleName)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.cell.acceptWWArmyCall, yesBtnText=gameStrings.TEXT_IMPSHUANGXIU_24, noCallback=self.cell.rejectWWArmyCall, noBtnText=gameStrings.TEXT_IMPSHUANGXIU_26)

    def _checkWWArmyCanFlyRide(self):
        it = self.equipment.get(gametypes.EQU_PART_RIDE)
        if not it:
            return False
        if it.id != WWCD.data.get('leaderRideItemId'):
            return False
        if not self.inWorldWar():
            return False
        return self._checkWWArmyRide(it.id, bNotify=False)

    def _checkWWArmyRide(self, itemId, bNotify = True):
        leaderRideItemId = WWCD.data.get('leaderRideItemId')
        if leaderRideItemId != itemId:
            return True
        if self.wwArmyPostId != gametypes.WW_ARMY_LEADER_POST_ID:
            bNotify and self.client.showGameMsg(GMDD.data.WW_ARMY_LEADER_RIDE_NOT_LEADER, ())
            return False
        return True

    def checkImpeachApply(self):
        """
        if self.worldWar.impeachState == gametypes.WW_ARMY_IMPEACH_STATE_VOTE:
            self.showGameMsg(GMDD.data.WW_ARMY_IMPEACH_ALREADY_IN_VOTE,())
            return False
        if self.worldWar.impeachState!=gametypes.WW_ARMY_IMPEACH_STATE_APPLY:
            self.showGameMsg(GMDD.data.WW_ARMY_IMPEACH_NOT_IN_APPLY,())
            return False
        if not self.gbId:
            self.showGameMsg(GMDD.data.WW_ARMY_AUTH_NO_POST)
            return False
        army = self.worldWar.getArmyByGbId(self.gbId)
        if getattr(army,'hasPrivilege',None)==None:
            self.showGameMsg(GMDD.data.WW_ARMY_AUTH_NO_PRIVILEGE,())
            return False
        if not army.hasPrivilege(gametypes.WW_ARMY_PRIVILEGE_IMPEACH):
            self.showGameMsg(GMDD.data.WW_ARMY_AUTH_NO_PRIVILEGE,())
        else:
            return True
        """
        return True

    def onQueryWWArmyImpeach(self, impeachState, dto, forUse):
        if self._isSoul() or self._isReturn():
            return
        self.worldWar.impeachState = impeachState
        if dto:
            impeachText, impeachVoteEndTime, impeachAgreeNum, impeachTotalNum, leaderDTO, applierDTO = dto
            self.worldWar.impeachText = impeachText
            self.worldWar.impeachVoteEndTime = impeachVoteEndTime
            self.worldWar.impeachAgreeNum = impeachAgreeNum
            self.worldWar.impeachTotalNum = impeachTotalNum
            impeachApplyGbId = applierDTO and applierDTO[0] or 0
            self.worldWar.impeachApplyGbId = impeachApplyGbId
            leaderGbId = leaderDTO and leaderDTO[0] or 0
            if leaderGbId:
                leader = self.worldWar.getArmyByGbId(leaderGbId)
                if not leader:
                    leader = WWArmyPostVal(gbId=leaderGbId, postId=gametypes.WW_ARMY_LEADER_POST_ID)
                    self.worldWar.army[leaderGbId] = leader
                leader.gbId, leader.name, leader.school, leader.sex, leader.photo = leaderDTO
            if impeachApplyGbId:
                post = self.worldWar.getArmyByGbId(impeachApplyGbId)
                if not post:
                    post = WWArmyPostVal(gbId=impeachApplyGbId)
                    self.worldWar.army[impeachApplyGbId] = post
                post.gbId, post.name, post.school, post.sex, post.photo, post.postId = applierDTO
            self.worldWar.buildArmyIndex()
        if forUse == gametypes.WW_ARMY_IMPEACH_QUERY_NPC:
            if self.checkImpeachApply():
                gameglobal.rds.ui.funcNpc.openFuncPanelState(npcConst.NPC_FUNC_IMPEACH_START)
                gameglobal.rds.ui.worldWar.showWWImpeachStart()
            else:
                gameglobal.rds.ui.funcNpc.onDefaultState()
            return
        gameglobal.rds.ui.worldWar.setImpeachVoteInfo(dto)
        if self.lv >= WWCD.data.get('voteLv', 0) and impeachState == gametypes.WW_ARMY_IMPEACH_STATE_VOTE:
            gameglobal.rds.ui.worldWar.showWWImpeachReview(dto)

    def onWWArmyImpeachApplyOK(self):
        gameglobal.rds.ui.worldWar.hideWWImpeachStart()
        BigWorld.player().cell.queryWWArmyImpeach(0)

    def onWWArmyImpeachVoteOK(self, agree):
        self.wwArmyImpeachVoted = agree
        gameglobal.rds.ui.worldWar.refreshImpeachReviewState(agree)
        self.cell.queryWWArmyImpeach(0)

    def onWWArmyImpeachEnd(self, impeachState, applyName, leaderName, applyPostId):
        self.worldWar.impeachState = impeachState
        title = gameStrings.TEXT_IMPWORLDWAR_752
        content = ''
        if impeachState == gametypes.WW_ARMY_IMPEACH_STATE_FINISHED_OK:
            applyPostName = WWAD.data.get(applyPostId, {}).get('name', '')
            leaderPostName = WWAD.data.get(gametypes.WW_ARMY_LEADER_POST_ID, {}).get('name', '')
            content = uiUtils.getTextFromGMD(GMDD.data.WW_ARMY_IMPEACH_OK, '%s_%s_%s_%s') % (applyPostName,
             applyName,
             leaderName,
             leaderPostName)
            gameglobal.rds.ui.messageBox.showAlertBox(content, title=title)
        gameglobal.rds.ui.worldWar.refreshImpeachReviewState()
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_IMPEACH_VOTE)

    def sendWWArmySkill(self, data, bRefresh = False):
        bwTime = BigWorld.time()
        serverTime = self.getServerTime()
        logicInfo.cooldownWWArmySkill = {}
        self.worldWar.armySkills.clear()
        for skillId, level, nextTime in data:
            self.worldWar.armySkills[skillId] = WWArmySkillVal(skillId=skillId, level=level, nextTime=nextTime)
            if nextTime > serverTime:
                skillcd = SGD.data.get((skillId, 1)).get('cd')
                end = nextTime - serverTime + bwTime
                logicInfo.cooldownWWArmySkill[skillId] = (end, skillcd)

        if bRefresh:
            gameglobal.rds.ui.actionbar.updateSlots()

    def onCastWWArmySkill(self, skillId, nextTime, mpUsed, mp):
        sk = self.worldWar.armySkills.get(skillId, None)
        if not sk:
            sk = WWArmySkillVal(skillId=skillId, level=1, nextTime=nextTime)
            self.worldWar.armySkills[skillId] = sk
        else:
            sk.nextTime = nextTime
        self.worldWar.mp = mp
        post = self.worldWar.getArmyByPostId(self.wwArmyPostId)
        if post:
            post.mpUsed = mpUsed
        bwTime = BigWorld.time()
        serverTime = self.getServerTime()
        if nextTime > serverTime:
            skillcd = SGD.data.get((skillId, 1)).get('cd')
            end = nextTime - serverTime + bwTime
            logicInfo.cooldownWWArmySkill[skillId] = (end, skillcd)
        gameglobal.rds.ui.actionbar.updateSlots()

    def onUpdateWWArmyPrivileges(self, gbId, privileges):
        post = self.worldWar.getArmyByGbId(gbId)
        if not post:
            return
        post.privileges = privileges

    def onUpdateAnnouncement(self, txt):
        self.worldWar.announcement = txt
        self.showGameMsg(GMDD.data.WW_UPDATE_ANNOUNCEMENT_OK, ())

    def onAddWorldWarBattleLessBuff(self, lv, stateId):
        data = SD.data.get(stateId)
        self.showGameMsg(GMDD.data.WW_BATTLE_LESS_BUFF, (data.get('name'),))

    def onQueryWBHireInfo(self, hireData, ver):
        self.worldWar.hireVer = ver
        c = self.worldWar.getCountry()
        hireData.pop(c.hostId, None)
        hireData.pop(c.enemyHostId, None)
        d = [ (hostId,
         hireState,
         queueHireLen,
         combatScore) for hostId, (hireState, queueHireLen, combatScore) in hireData.iteritems() if hireState ]
        d.sort(cmp=cmpHire, reverse=True)
        gameglobal.rds.ui.worldWar.setServerList(d)

    def onWWBattleResUpdate(self, battleRes):
        self.worldWar.getCountry().battleRes = battleRes
        gameglobal.rds.ui.worldWar.refreshWWBattleScore()

    def onQueryWWTournament(self, groupId, groupDTO, guildDTO, hostDTO, groupVer, guildVer):
        if guildDTO != None:
            self.worldWar.tournamentResult.fromGuildDTO(guildDTO)
        self.worldWar.tournamentResult.fromDTOByGroup(groupId, groupDTO)
        self.worldWar.tournamentResult.fromHostDTO(groupId, hostDTO)
        self.worldWar.tournamentResult.groupVer[groupId] = groupVer
        self.worldWar.tournamentResult.guildVer = guildVer
        gameglobal.rds.ui.guildWWTournamentResult.show(groupId)
        gameglobal.rds.ui.bFGuildTournamentLive.refreshAllInspirePraiseData()

    def onQueryWWTournamentKeep(self, groupId):
        gameglobal.rds.ui.guildWWTournamentResult.show(groupId)

    def isWBHired(self):
        return self._getWBHireHostId() or self.wbApplyHireHostId

    def onWorldWarBattleHireStop(self, stopped):
        self.worldWar.battleHireStopped = stopped

    def onUpdateCheckWWInactive(self, isNeed):
        self.worldWar.isNeedCheckInactive = isNeed
        if isNeed and self.inWorldWar():
            gameglobal.rds.ui.worldWar.startCheckInactive()

    def onUpdateTicketHost(self, ticketInfo):
        self.worldWar.wwTicketHosts.update(ticketInfo)

    def onQueryWWQLBHSelection(self, robOrBattle, val):
        self.worldWar.WWQLBHSelection[robOrBattle] = val
        if not val:
            gameglobal.rds.ui.worldWarLvChoose.show(robOrBattle)
        else:
            self.cell.enterWorldWarEvent(robOrBattle)
