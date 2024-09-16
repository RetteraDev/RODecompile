#Embedded file name: /WORKSPACE/data/entities/client/virtualmonster.o
import BigWorld
import gametypes
import clientcom
import gameglobal
import gamelog
from guis import uiUtils, uiConst
from iCombatUnit import IMonsterCombatUnit

class VirtualMonster(IMonsterCombatUnit):
    IsCombatUnit = True
    IsMonster = True
    IsVirtualMonster = True
    CIRCLE_SET = set([0, 1, 2])

    def __init__(self):
        super(VirtualMonster, self).__init__()
        self._isLocked = False
        if len(VirtualMonster.CIRCLE_SET) > 0:
            self.circleNum = VirtualMonster.CIRCLE_SET.pop()
        else:
            self.circleNum = -1
        self.updatePosCallback = None

    def isMultiPartMonster(self):
        return False

    def _updatePos(self):
        if gameglobal.SCENARIO_PLAYING:
            return
        if not self.inWorld:
            return
        if self.updatePosCallback:
            BigWorld.cancelCallback(self.updatePosCallback)
        if self.circleNum == -1:
            if len(VirtualMonster.CIRCLE_SET) == 0:
                self.updatePosCallback = BigWorld.callback(0.2, self._updatePos)
                return
            self.circleNum = VirtualMonster.CIRCLE_SET.pop()
        if hasattr(self, 'life') and self.life == gametypes.LIFE_ALIVE:
            try:
                masterMonster = BigWorld.entities.get(self.masterMonsterID)
                if masterMonster == None:
                    gameglobal.rds.ui.targetCircle.hide(self.circleNum)
                    self.updatePosCallback = BigWorld.callback(0, self._updatePos)
                    return
                masterModel = masterMonster.model
                nodePosition = clientcom.getModeNodePosition(masterModel, self.nodeName)
                self.filter.position = nodePosition
                ents = BigWorld.inCameraEntity(80)
                if self._isLocked:
                    if ents is not None and self.masterMonsterID in [ e.id for e in ents ]:
                        x, y = clientcom.worldPointToScreen(self.filter.position)
                        gameglobal.rds.ui.targetCircle.show(x - 40, y - 40, self.circleNum)
                        gameglobal.rds.ui.bossBlood.selectVMBtn(self.charType)
                    else:
                        gameglobal.rds.ui.targetCircle.hide(self.circleNum)
                elif ents is not None and self.masterMonsterID in [ e.id for e in ents ]:
                    x, y = clientcom.worldPointToScreen(self.filter.position)
                    gameglobal.rds.ui.targetCircle.showNoActive(self.circleNum, x - 40, y - 40)
                else:
                    gameglobal.rds.ui.targetCircle.hide(self.circleNum)
                self._setLockedId()
            except Exception as e:
                pass

            self.updatePosCallback = BigWorld.callback(0, self._updatePos)

    def afterModelFinish(self):
        super(VirtualMonster, self).afterModelFinish()
        self.filter = BigWorld.ClientFilter()
        self._updatePos()
        self.refreshOpacityState()

    def leaveWorld(self):
        super(VirtualMonster, self).leaveWorld()
        VirtualMonster.CIRCLE_SET.add(self.circleNum)
        if self.life == gametypes.LIFE_ALIVE:
            gameglobal.rds.ui.targetCircle.hide(self.circleNum)
            if self.inWorld and gameglobal.rds.ui.bossBlood.bloodOwner == self.masterMonsterID and BigWorld.player().targetId == self.id:
                gameglobal.rds.ui.bossBlood.hideBossBlood()

    def enterWorld(self):
        super(VirtualMonster, self).enterWorld()

    def _setLockedId(self):
        if BigWorld.player().targetLocked == self:
            master = BigWorld.entities.get(self.masterMonsterID)
            if master and master.lockedId:
                showBlood = uiUtils._isNeedShowBossBlood(master.charType)
                if self.inWorld and (showBlood == 1 and not self.inDying or showBlood == 2 and self.inDying):
                    gameglobal.rds.ui.bossBlood.setBossTargetLockName(master.lockedId)

    def set_lockedId(self, old):
        if old == 0 and self.lockedId == 0:
            return
        self._setLockedId()

    def set_specialStateVal(self, old):
        gameglobal.rds.ui.bossInfo.review()
        if BigWorld.player().targetLocked == self:
            gameglobal.rds.ui.bossBlood.setTargetQiJue()

    def lockEffect(self):
        self._isLocked = True
        if BigWorld.player().isChangeMasterMonsterPart:
            gameglobal.rds.ui.bossBlood.setPartName(self.roleName)
            return
        master = BigWorld.entities.get(self.masterMonsterID)
        if not master:
            return
        showBlood = uiUtils._isNeedShowBossBlood(master.charType)
        if showBlood == 1 and not master.inDying or master.inDying and showBlood == 2:
            if not gameglobal.rds.ui.isHideAllUI():
                gameglobal.rds.ui.bossBlood.showBossBlood(self.masterMonsterID, True)
            else:
                gameglobal.rds.ui.bossBlood.showBossBlood(self.masterMonsterID, False)
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_BOSSBLOOD, True)
            gamelog.debug('lockEffect2')
            gameglobal.rds.ui.bossBlood.setPartName(self.roleName)
            if master.inDying:
                gameglobal.rds.ui.bossBlood.setName(master.roleName + ' ±ÙÀ¿')
            else:
                gameglobal.rds.ui.bossBlood.setName(master.roleName)
            gameglobal.rds.ui.bossBlood.setLevel(master)
            gameglobal.rds.ui.bossBlood.initHp(master.hp, master.mhp, '', getattr(master, 'isDmgMode', False))
            gameglobal.rds.ui.bossBlood.setBossTargetLockName(master.lockedId)
        if master.inDying:
            gameglobal.rds.ui.target.hideTargetUnitFrame()

    def unlockEffect(self):
        self._isLocked = False
        if BigWorld.player().isChangeMasterMonsterPart:
            return
        if self.inWorld and gameglobal.rds.ui.bossBlood.bloodOwner == self.masterMonsterID:
            gameglobal.rds.ui.bossBlood.hideBossBlood()

    def set_life(self, old):
        super(VirtualMonster, self).set_life(old)
        player = BigWorld.player()
        if self.life == gametypes.LIFE_DEAD:
            gameglobal.rds.ui.targetCircle.hide(self.circleNum)
            gameglobal.rds.ui.bossInfo.review()
        if self.life == gametypes.LIFE_DEAD and player.targetLocked != None and player.targetLocked.id == self.id and gameglobal.rds.ui.bossBlood.bloodOwner == self.masterMonsterID:
            gameglobal.rds.ui.bossBlood.hideBossBlood()

    def playDieAction(self, needDieAction = True, forcePlayAction = False):
        pass

    def set_inDying(self, old):
        super(VirtualMonster, self).set_inDying(old)
        p = BigWorld.player()
        master = BigWorld.entities.get(self.masterMonsterID)
        if gameglobal.rds.ui.bossBlood.bloodOwner == self.id:
            if self.inDying:
                gameglobal.rds.ui.bossBlood.setPartName('')
                gameglobal.rds.ui.bossBlood.setName(master.roleName + ' ±ÙÀ¿')
            else:
                gameglobal.rds.ui.bossBlood.hideBossBlood()
                p.unlockTarget()

    def hide(self, bHide, retainTopLogo = False):
        if not self.inWorld:
            return
        super(VirtualMonster, self).hide(bHide, retainTopLogo)
        if bHide:
            if self.updatePosCallback:
                BigWorld.cancelCallback(self.updatePosCallback)
            gameglobal.rds.ui.targetCircle.hide(self.circleNum)
        else:
            self._updatePos()

    def showTargetUnitFrame(self):
        return False
