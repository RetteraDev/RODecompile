#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impWorldWarRob.o
import utils
import gametypes
import gameglobal
import BigWorld
import formula
import const
from guis import uiConst
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import world_war_config_data as WWCD
from data import world_war_army_data as WWAD

class ImpWorldWarRob(object):

    def onWWRobStateUpdate(self, robState, tRobStateEnd, wwtype):
        self.setRobState(wwtype, robState, tRobStateEnd)
        self.worldWar.robStateDict[wwtype] = robState
        gameglobal.rds.ui.worldWarRobOverview.resetTime()
        gameglobal.rds.ui.worldWarRobInfo.resetTime()
        if robState == gametypes.WW_ROB_STATE_OPEN:
            self.onCheckWWRobAura(False)
        self.onCheckBossHint()
        self.showPicTipAndSound(wwtype)
        gameglobal.rds.ui.worldWarRobOverview.pushMessage(wwtype)
        gameglobal.rds.ui.worldWarRobOverview.show()
        gameglobal.rds.ui.littleMap.addRobZaiju()

    def onNotifyWWRobState(self, robState, tRobStateEnd, wwtype):
        self.setRobState(wwtype, robState, tRobStateEnd)
        self.worldWar.robStateDict[wwtype] = robState
        if robState == gametypes.WW_ROB_STATE_OPEN:
            self.onCheckWWRobAura(False)
        gameglobal.rds.ui.worldWarRobOverview.pushMessage(wwtype)

    def setRobState(self, wwtype, robState, tRobStateEnd):
        if formula.spaceInWorldWarRobOld(self.spaceNo):
            if wwtype == gametypes.WORLD_WAR_TYPE_ROB:
                self.worldWar.robState = robState
                self.worldWar.tRobStateEnd = tRobStateEnd
        elif formula.spaceInWorldWarRobYoung(self.spaceNo):
            if wwtype == gametypes.WORLD_WAR_TYPE_ROB_YOUNG:
                self.worldWar.robState = robState
                self.worldWar.tRobStateEnd = tRobStateEnd
        else:
            self.worldWar.robState = robState
            self.worldWar.tRobStateEnd = tRobStateEnd

    def showPicTipAndSound(self, wwtype = 0):
        wwRobSoundIds = WWCD.data.get('wwRobSoundIds', {})
        robState = self.worldWar.robStateDict[wwtype]
        camp = self.worldWar.getCurrCamp()
        wwRobPicTxt = WWCD.data.get('wwRobPicTxt', {})
        wwRobPicList = wwRobPicTxt.get(wwtype, [])
        timeDelay = 0
        if wwtype == gametypes.WORLD_WAR_TYPE_ROB_YOUNG:
            timeDelay = 5
        if robState == gametypes.WW_ROB_STATE_CLOSED:
            self.worldWar.isInRobAura = False
        if robState == gametypes.WW_ROB_STATE_READY:
            if camp == gametypes.WORLD_WAR_CAMP_ATTACK:
                BigWorld.callback(timeDelay, Functor(gameglobal.rds.sound.playSound, wwRobSoundIds[gametypes.WW_TIP_ROB_MINE_OPEN]))
                BigWorld.callback(timeDelay, Functor(gameglobal.rds.ui.showPicTip, wwRobPicList[gametypes.WW_TIP_ROB_MINE_OPEN]))
            else:
                BigWorld.callback(timeDelay, Functor(gameglobal.rds.sound.playSound, wwRobSoundIds[gametypes.WW_TIP_ROB_ENEMY_OPEN]))
                BigWorld.callback(timeDelay, Functor(gameglobal.rds.ui.showPicTip, wwRobPicList[gametypes.WW_TIP_ROB_ENEMY_OPEN]))
            BigWorld.callback(timeDelay + 5, Functor(gameglobal.rds.ui.showPicTip, wwRobPicList[gametypes.WW_TIP_ROB_PREPARE]))
        elif robState == gametypes.WW_ROB_STATE_OPEN:
            BigWorld.callback(timeDelay, Functor(gameglobal.rds.sound.playSound, wwRobSoundIds[gametypes.WW_TIP_ROB_START]))
            BigWorld.callback(timeDelay, Functor(gameglobal.rds.ui.showPicTip, wwRobPicList[gametypes.WW_TIP_ROB_START]))
        elif robState == gametypes.WW_ROB_STATE_ZAIJU_BROKEN and camp == gametypes.WORLD_WAR_CAMP_ATTACK:
            BigWorld.callback(timeDelay, Functor(gameglobal.rds.sound.playSound, wwRobSoundIds[gametypes.WW_TIP_ROB_MINE_ZAIJU_HURT]))
            BigWorld.callback(timeDelay, Functor(gameglobal.rds.ui.showPicTip, wwRobPicList[gametypes.WW_TIP_ROB_MINE_ZAIJU_HURT]))
        elif robState == gametypes.WW_ROB_STATE_ZAIJU_BROKEN and camp == gametypes.WORLD_WAR_CAMP_DEFEND:
            BigWorld.callback(timeDelay, Functor(gameglobal.rds.sound.playSound, wwRobSoundIds[gametypes.WW_TIP_ROB_ENEMY_ZAIJU_HURT]))
            BigWorld.callback(timeDelay, Functor(gameglobal.rds.ui.showPicTip, wwRobPicList[gametypes.WW_TIP_ROB_ENEMY_ZAIJU_HURT]))

    def onWWRobPreopenNotify(self):
        gameglobal.rds.ui.worldWarRobOverview.pushLeaderMessage()

    def onWWRobFortOccupied(self, fortId, hostId):
        fort = self.worldWar.getFort(fortId)
        fort.hostId = hostId
        self.onWWRobFortUpdate([(fortId,
          hostId,
          False,
          0)])

    def onQueryWWRobAll(self, robDTO, playerDTO):
        tNextTeleport, robScore, totalRobScore, totalRobAttends = playerDTO
        self.worldWar.tNextTeleport = tNextTeleport
        self.worldWar.robScore = robScore
        self.worldWar.totalRobScore = totalRobScore
        self.worldWar.totalRobAttends = totalRobAttends
        self.onQueryWWRob(*robDTO)

    def onQueryWWRob(self, robState, tRobStateEnd, robZaijuEntID, fortDTO, zaijuLevel, zaijuMHP, zaijuDto):
        self.worldWar.robState = robState
        self.worldWar.tRobStateEnd = tRobStateEnd
        self.onUpdateWWRobZaijuEnt(robZaijuEntID)
        self.worldWar.robZaiju.level = zaijuLevel
        self.worldWar.robZaiju.mhp = zaijuMHP
        self.worldWar.robZaiju.fromDTO(zaijuDto)
        self.onWWRobFortUpdate(fortDTO)
        gameglobal.rds.ui.worldWarRobOverview.removeWWRStartMsg()
        if robState in gametypes.WW_ROB_STATE_ACTIVE or robState == gametypes.WW_ROB_STATE_READY:
            self.onCheckBossHint(True)
            gameglobal.rds.ui.worldWarRobOverview.show(True)
            gameglobal.rds.ui.littleMap.addRobZaiju(True)

    def onQueryWWRobZaiju(self, dto):
        self.worldWar.robZaiju.fromDTO(dto)
        gameglobal.rds.ui.map.refreshRobZaiju()
        gameglobal.rds.ui.littleMap.addRobZaiju()
        gameglobal.rds.ui.worldWarRobOverview.show()
        gameglobal.rds.ui.worldWarRobInfo.refreshPanel()

    def onWWRobZaijuUpgrade(self, level):
        self.worldWar.robZaiju.level = level
        gameglobal.rds.ui.worldWarRobOverview.show()

    def onWWRobFortUpdate(self, fortData):
        for fortId, hostId, inCombat, bossEntId in fortData:
            fort = self.worldWar.getFort(fortId)
            oldHostId = fort.hostId
            fort.hostId = hostId
            fort.inCombat = inCombat
            fort.bossEntId = bossEntId
            gameglobal.rds.ui.map.addWWRBattleIcon()
            gameglobal.rds.ui.littleMap.addWWRBattleIcon()
            gameglobal.rds.ui.worldWarRobInfo.refreshPanel()
            if len(fortData) == 1 and self.inWorldWarBattle() and oldHostId != fort.hostId:
                if hostId == utils.getHostId():
                    pass

    def onUpdateRobNextTeleportTime(self, tNextTeleport):
        self.worldWar.tNextTeleport = tNextTeleport

    def onUpdateWWRobScore(self, score, totalRobScore, totalRobAttends):
        self.worldWar.robScore = score
        self.worldWar.totalRobScore = totalRobScore
        self.worldWar.totalRobAttends = totalRobAttends
        gameglobal.rds.ui.worldWarRobInfo.refreshPanel()
        gameglobal.rds.ui.worldWarRobOverview.show()

    def onUpdateWWRobZaijuEnt(self, newEntID):
        self.worldWar.robZaijuEntID = newEntID

    def onCheckBossHint(self, force = False):
        if not BigWorld.player():
            return
        if self.id != BigWorld.player().id:
            if self.worldWar.robBossHintTimeID:
                BigWorld.cancelCallback(self.worldWar.robBossHintTimeID)
            return
        robBossInZaiju = self.worldWar.robBossInZaiju
        if not force:
            if not self.isWWRInRightState():
                if self.worldWar.robBossHintTimeID:
                    BigWorld.cancelCallback(self.worldWar.robBossHintTimeID)
                return
        if self.worldWar.robZaijuEntID:
            for fortId, fort in self.worldWar.fort.iteritems():
                if fort.bossEntId:
                    robZaijuEnt = BigWorld.entities.get(self.worldWar.robZaijuEntID)
                    bossEnt = BigWorld.entities.get(fort.bossEntId)
                    if robZaijuEnt and robZaijuEnt.inWorld and bossEnt and bossEnt.inWorld:
                        if bossEnt.position.distTo(robZaijuEnt.position) <= WWCD.data.get('robZaijuAuraRange', 50):
                            robBossInZaiju = True
                            break
                        else:
                            robBossInZaiju = False

        if robBossInZaiju != self.worldWar.robBossInZaiju:
            if robBossInZaiju:
                self.showGameMsg(GMDD.data.WORLD_WAR_ROB_BOSS_IN_ZAIJU, ())
            else:
                self.showGameMsg(GMDD.data.WORLD_WAR_ROB_BOSS_OUT_ZAIJU, ())
            self.worldWar.robBossInZaiju = robBossInZaiju
        if self.worldWar.robBossHintTimeID:
            BigWorld.cancelCallback(self.worldWar.robBossHintTimeID)
        self.worldWar.robBossHintTimeID = BigWorld.callback(1, self.onCheckBossHint)

    def onCheckWWRobAura(self, isFinish):
        auraId = WWCD.data.get('robAuraBuffID', 0)
        p = BigWorld.player()
        if self.id != p.id:
            if self.worldWar.robAuraCheckTimeID:
                BigWorld.cancelCallback(self.worldWar.robAuraCheckTimeID)
            return
        if not self.isInRobSpace() or self.worldWar.robState not in gametypes.WW_ROB_STATE_ACTIVE:
            self.removeState(auraId, self.id)
            if self.worldWar.robAuraCheckTimeID:
                BigWorld.cancelCallback(self.worldWar.robAuraCheckTimeID)
            self.worldWar.robAuraCheckTimeID = 0
            gameglobal.rds.ui.wWRZaijuBlood.clearWidget()
            return
        if not isFinish and self.worldWar.robAuraCheckTimeID:
            BigWorld.cancelCallback(self.worldWar.robAuraCheckTimeID)
        self.worldWar.robAuraCheckTimeID = BigWorld.callback(1, Functor(self.onCheckWWRobAura, True))
        ent = BigWorld.entities.get(self.worldWar.robZaijuEntID)
        if ent and ent.inWorld and self.position.distTo(ent.position) <= WWCD.data.get('robZaijuAuraRange', 50):
            gameglobal.rds.ui.wWRZaijuBlood.show(ent)
            if not self._isHasStateInclClientPub(self, auraId):
                self.showGameMsg(GMDD.data.WORLD_WAR_ROB_ENTER_AURA_TIP, ())
                self.addState(auraId, -1, self.id, 1)
        else:
            gameglobal.rds.ui.wWRZaijuBlood.clearWidget()
            if self._isHasStateInclClientPub(self, auraId):
                self.showGameMsg(GMDD.data.WORLD_WAR_ROB_LEAVE_AURA_TIP, ())
                self.removeState(auraId, self.id)

    def onWWRobEndNotified(self, totalRes, bindCash, score, bonusIds, lastRobState):
        if not gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
            gameglobal.rds.ui.worldWarRobOverview.pushResultPanelMsg(totalRes, bindCash, score, bonusIds, lastRobState)
        else:
            gameglobal.rds.ui.worldWarRobResult.show(totalRes, bindCash, score, bonusIds, lastRobState)
            gameglobal.rds.ui.worldWarRobOverview.pushResultPanelMsg(totalRes, bindCash, score, bonusIds, lastRobState)

    def onClickOpenWorldWarRob(self, wwType):
        self.cell.applyStartWorldWarRob(wwType)
        if not gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
            gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WORLD_WAR_ROB_START)

    def isWWRInRightState(self):
        ww = self.worldWar
        if not gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
            if ww.robState in gametypes.WW_ROB_STATE_NOT_OPEN or not formula.spaceInWorldWar(self.spaceNo):
                return False
            if ww.getCurrCamp() == gametypes.WORLD_WAR_CAMP_ATTACK:
                if not self._isSoul() and not self._isReturn():
                    return False
            elif self._isSoul() or self._isReturn():
                return False
            return True
        if ww.robState in gametypes.WW_ROB_STATE_NOT_OPEN or not formula.spaceInWorldWarRob(self.spaceNo):
            return False
        return True

    def checkRobStartPrivilege(self, wwType):
        if not hasattr(self, 'wwArmyPostId'):
            return False
        if wwType == gametypes.WORLD_WAR_TYPE_ROB:
            privilegeId = gametypes.WW_ARMY_PRIVILEGE_START_ROB
        elif wwType == gametypes.WORLD_WAR_TYPE_ROB_YOUNG:
            privilegeId = gametypes.WW_ARMY_PRIVILEGE_START_ROB_YOUNG
        privileges = ()
        if gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
            privileges = WWAD.data.get(self.wwArmyPostId, {}).get('fixedPrivilegesNew', ())
        else:
            privileges = WWAD.data.get(self.wwArmyPostId, {}).get('fixedPrivileges', ())
        if privilegeId not in privileges:
            return False
        else:
            return True

    def isHaveRobStartPrivilege(self):
        if not hasattr(self, 'wwArmyPostId'):
            return False
        if self.checkRobStartPrivilege(gametypes.WORLD_WAR_TYPE_ROB_YOUNG) or self.checkRobStartPrivilege(gametypes.WORLD_WAR_TYPE_ROB):
            return True
        return False

    def startRob(self, npc):
        if self.checkRobStartPrivilege(gametypes.WORLD_WAR_TYPE_ROB):
            msg = GMD.data.get(GMDD.data.WORLD_WAR_ROB_OPEN_CONFIRM, {}).get('text', '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg % '', yesCallback=Functor(self.onClickOpenWorldWarRob, gametypes.WORLD_WAR_TYPE_ROB), noCallback=Functor(self.onClickOpenWorldWarRob, None))
        else:
            self.showGameMsg(GMDD.data.WW_ROB_START_NOT_LEADER, ())
            gameglobal.rds.ui.funcNpc.close()

    def isInRobSpace(self):
        isInRobSpace = False
        if not gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
            isInRobSpace = formula.spaceInWorldWar(self.spaceNo)
        else:
            isInRobSpace = formula.spaceInWorldWarRob(self.spaceNo)
        return isInRobSpace
