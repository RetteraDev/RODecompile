#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/aimCross.o
from gamestrings import gameStrings
import BigWorld
import GUI
import Math
import clientcom
import gameglobal
import gametypes
import math
from ui import gbk2unicode
from data import school_data as SD
from data import state_data as STATED
from data import zaiju_data as ZD

class AimCross(object):
    TARGET_DIR_X_OFFSET = 30
    TARGET_DIR_Y_PER = 0.5
    S_TYPE_START = 'start'
    S_TYPE_RED = 'red'
    S_TYPE_NORMAL = 'normal'
    IN_CAMERA_DIST = 120

    def __init__(self):
        super(AimCross, self).__init__()
        self.modelMap = {}
        self.cursorAim = GUI.Simple('gui/cursor/cursor_aim.dds')
        self.cursorAim.heightRelative = False
        self.cursorAim.widthRelative = False
        self.cursorAim.size = (40, 40)
        self.cursorAim.verticalAnchor = 'CENTER'
        self.cursorAim.horizontalAnchor = 'CENTER'
        currentScrollNum = gameglobal.rds.cam.currentScrollNum
        offsets = BigWorld.player().getPhysicsYOffset()
        yOffset = offsets[currentScrollNum] if currentScrollNum < len(offsets) else 0
        self.cursorAim.position = (0, yOffset, 0)
        self.cursorAimed = GUI.Simple('gui/cursor/cursor_aimed.dds')
        self.cursorAimed.heightRelative = False
        self.cursorAimed.widthRelative = False
        self.cursorAimed.size = (48, 48)
        self.cursorAimed.verticalAnchor = 'CENTER'
        self.cursorAimed.horizontalAnchor = 'CENTER'
        self.cursorAimed.position = (0, yOffset, 0)
        self.released = False
        self.resetTargetDirCord()
        self.outCameraState = {}
        self.handle = None
        self.oldPos = [0, 0]

    def resetTargetDirCord(self):
        self.targetDirRightX = BigWorld.screenWidth() - AimCross.TARGET_DIR_X_OFFSET - 80
        self.targetDirY = BigWorld.screenHeight() * AimCross.TARGET_DIR_Y_PER

    def setAimCrossOffset(self, offset):
        self.cursorAim.position = (0, offset, 0)
        self.cursorAimed.position = (0, offset, 0)

    def hide(self):
        GUI.delRoot(self.cursorAim)
        GUI.delRoot(self.cursorAimed)

    def noNeedAimGUI(self):
        if self.released or BigWorld.player().ap.showCursor or gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA or gameglobal.isWidgetNeedShowCursor or BigWorld.player().ap.inLoadingProgress or gameglobal.rds.GameState == gametypes.GS_LOADING or not gameglobal.rds.ui.enableUI:
            return True
        return False

    def turnToAimState(self):
        if self.noNeedAimGUI():
            return
        else:
            gameglobal.rds.ui.pushMessage.setHitTestDisable(True)
            BigWorld.player().ap.refreshUIEnabled()
            GUI.delRoot(self.cursorAimed)
            GUI.delRoot(self.cursorAim)
            GUI.addRoot(self.cursorAim)
            gameglobal.rds.ui.hideAimCross(True)
            gameglobal.rds.ui.hideAimCross(False)
            gameglobal.rds.ui.hideTargetDir()
            BigWorld.player().optionalTargetLocked = None
            gameglobal.rds.ui.subTarget.hideSubTargetUnitFrame()
            return

    def turnToAimedState(self, start = True):
        if self.noNeedAimGUI():
            return
        else:
            pos = self._getFramePos(BigWorld.player().targetLocked)
            if not pos or len(pos) != 2:
                return
            BigWorld.player().ap.refreshUIEnabled()
            GUI.delRoot(self.cursorAim)
            GUI.delRoot(self.cursorAimed)
            GUI.addRoot(self.cursorAimed)
            dist = self.getTargetLockDist()
            distStr = self.getDistStr(dist)
            sType = self.getDistType(dist)
            sType = sType if sType else AimCross.S_TYPE_START
            isLockAim = self.isLockAim()
            color = self.getAimCrossColor(BigWorld.player().targetLocked)
            if not start:
                gameglobal.rds.ui.setAimCrossPos(pos[0], pos[1], distStr, sType, True, color, isLockAim)
                self.setOptionalTargetAimCross()
            else:
                gameglobal.rds.ui.showAimCross(pos[0], pos[1], distStr, sType, True, color, isLockAim)
                self.showOptionalTargetAimCross()
                if BigWorld.player().targetLocked:
                    self.refreshStateIcon(BigWorld.player().targetLocked.id)
                if BigWorld.player().optionalTargetLocked:
                    self.refreshStateIcon(BigWorld.player().optionalTargetLocked.id)
            self.resetTargetDirCord()
            if self.handle:
                BigWorld.cancelCallback(self.handle)
                self.handle = None
            if gameglobal.rds.configData.get('enableNewAimCross', True):
                self.newUpdateCrossFrame()
            else:
                self.updateCrossFrame()
            return

    def showOptionalTargetAimCross(self):
        p = BigWorld.player()
        if p.optionalTargetLocked:
            pos = self._getFramePos(p.optionalTargetLocked)
            if not pos:
                return
            dist = int((p.optionalTargetLocked.position - p.position).length)
            distStr = self.getDistStr(dist)
            sType = self.getDistType(dist)
            color = self.getAimCrossColor(p.optionalTargetLocked)
            gameglobal.rds.ui.showAimCross(pos[0], pos[1], distStr, sType, False, color)

    def showBackupTargetAimCross(self):
        p = BigWorld.player()
        target = p.ap.backupTarget
        if target:
            pos = self._getFramePos(target)
            if not pos:
                return
            dist = int((target.position - p.position).length)
            distStr = self.getDistStr(dist)
            sType = self.getDistType(dist)
            gameglobal.rds.ui.showAimCross(pos[0], pos[1], distStr, sType, False, 'gray')
        else:
            gameglobal.rds.ui.hideAimCross(isGray=True)

    def isLockAim(self):
        return BigWorld.player().ap.lockAim

    def getAimCrossColor(self, target):
        isEnemy = BigWorld.player().isEnemy(target)
        if isEnemy:
            return 'red'
        else:
            return 'green'

    def setOptionalTargetAimCross(self):
        p = BigWorld.player()
        target = p.optionalTargetLocked
        if not target or not target.inWorld or hasattr(target, 'life') and target.life == gametypes.LIFE_DEAD:
            gameglobal.rds.ui.hideOptionalAimCross()
            return
        if target:
            dist = int((target.position - p.position).length)
            distStr = self.getDistStr(dist)
            sType = self.getDistType(dist)
            sType = sType if sType else AimCross.S_TYPE_NORMAL
            pos = self._getFramePos(p.optionalTargetLocked)
            if pos:
                color = self.getAimCrossColor(target)
                gameglobal.rds.ui.setAimCrossPos(pos[0], pos[1], distStr, sType, False, color)
            else:
                gameglobal.rds.ui.hideOptionalAimCross()

    def setBackupTargetAimCross(self):
        p = BigWorld.player()
        target = p.ap.backupTarget
        if not target or not target.inWorld or hasattr(target, 'life') and target.life == gametypes.LIFE_DEAD:
            gameglobal.rds.ui.hideAimCross(isGray=True)
            return
        if target:
            dist = int((target.position - p.position).length)
            distStr = self.getDistStr(dist)
            sType = self.getDistType(dist)
            sType = sType if sType else AimCross.S_TYPE_NORMAL
            pos = self._getFramePos(target)
            if pos:
                gameglobal.rds.ui.setAimCrossPos(pos[0], pos[1], distStr, sType, False, 'gray')
            else:
                gameglobal.rds.ui.hideAimCross(isGray=True)

    def _getFramePos(self, targetLocked):
        if not targetLocked:
            return None
        elif not targetLocked.model:
            return None
        else:
            node = targetLocked.model.node('HP_hit_default')
            if not node:
                node = targetLocked.model.root
            if not node:
                return None
            m = Math.Matrix(node)
            x, y = clientcom.worldPointToScreen(m.applyToOrigin())
            return (x - 24, y - 24)

    def _getOptionalFramePos(self):
        targetLocked = BigWorld.player().optionalTargetLocked
        node = targetLocked.model.node('HP_hit_default')
        if not node:
            node = targetLocked.model.root
        if not node:
            return None
        else:
            m = Math.Matrix(node)
            x, y = clientcom.worldPointToScreen(m.applyToOrigin())
            return (x - 24, y - 24)

    def _noNeedFrame(self):
        targetLocked = BigWorld.player().targetLocked
        if getattr(BigWorld.player().ap, 'showCursor', True):
            return True
        if not targetLocked or not targetLocked.inWorld:
            return True
        if not hasattr(targetLocked, 'IsCombatUnit') or not targetLocked.IsCombatUnit:
            return True
        return False

    def getTargetLockDist(self):
        p = BigWorld.player()
        dist = 0
        try:
            dist = int((p.targetLocked.position - p.position).length)
        except:
            pass

        return dist

    def getDistStr(self, dist):
        return str(dist) + gbk2unicode(gameStrings.TEXT_AIMCROSS_248)

    def refreshStateIcon(self, eid):
        p = BigWorld.player()
        if p.targetLocked and p.targetLocked.id == eid:
            path = self.getShowStateIconPath(p.targetLocked)
            gameglobal.rds.ui.setAimCrossBuff(path, True)
        if p.optionalTargetLocked and p.optionalTargetLocked.id == eid:
            path = self.getShowStateIconPath(p.optionalTargetLocked)
            gameglobal.rds.ui.setAimCrossBuff(path, False)

    def getShowStateIconPath(self, ent):
        if not ent or not ent.inWorld:
            return [None, None]
        stateIds = []
        if ent == BigWorld.player():
            stateIds = getattr(ent, 'statesServerAndOwn', {}).keys()
        else:
            stateIds = getattr(ent, 'statesClientPub', {}).keys()
        if len(stateIds):
            stateIdset = set(stateIds)
            path = []
            for sid in stateIdset:
                iconId = STATED.data.get(sid, {}).get('iconId', 0)
                if STATED.data.get(sid, {}).get('iconUnshow', 0):
                    continue
                path.append(['state/40/%d.dds' % iconId, stateIds.count(sid)])

            length = len(path)
            if length > 2:
                path = path[:2]
            if length < 2:
                path = path[:2]
                path[length:] = [None, None][length:]
            return path
        else:
            return [None, None]

    def entityNotInCamera(self, targetLocked):
        notInCamera = False
        inCameraEnts = BigWorld.inCameraEntity(AimCross.IN_CAMERA_DIST)
        if not inCameraEnts:
            notInCamera = True
        else:
            notInCamera = targetLocked not in inCameraEnts
        if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            notInCamera = False
        return notInCamera

    def updateCrossFrame(self):
        if self.released:
            return
        if self._noNeedFrame():
            gameglobal.rds.ui.hideAimCross(True)
            gameglobal.rds.ui.hideAimCross(False)
            return
        if BigWorld.player() and BigWorld.player().id == BigWorld.player().targetLocked.id:
            gameglobal.rds.ui.hideAimCross(True)
        targetLocked = BigWorld.player().targetLocked
        notInCamera = self.entityNotInCamera(targetLocked)
        dist = self.getTargetLockDist()
        distStr = self.getDistStr(dist)
        if notInCamera:
            if targetLocked:
                self.outCameraState[targetLocked.id] = True
            p = BigWorld.player()
            gameglobal.rds.ui.hideAimCross()
            yaw = p.yaw - (targetLocked.position - p.position).yaw
            if yaw < -math.pi or yaw > 0 and yaw < math.pi:
                gameglobal.rds.ui.showTargetDir(AimCross.TARGET_DIR_X_OFFSET, self.targetDirY, distStr, 'left')
            else:
                gameglobal.rds.ui.showTargetDir(self.targetDirRightX, self.targetDirY, distStr, 'right')
        else:
            gameglobal.rds.ui.hideTargetDir()
            pos = self._getFramePos(targetLocked)
            if pos:
                cType = self.getDistType(dist)
                if cType == AimCross.S_TYPE_START:
                    cType = AimCross.S_TYPE_NORMAL
                isLockAim = self.isLockAim()
                color = self.getAimCrossColor(targetLocked)
                if self.outCameraState.get(targetLocked.id, False):
                    gameglobal.rds.ui.showAimCross(pos[0], pos[1], distStr, cType, True, color, isLockAim)
                    self.outCameraState[targetLocked.id] = False
                gameglobal.rds.ui.setAimCrossPos(pos[0], pos[1], distStr, cType, True, color, isLockAim)
        self.setOptionalTargetAimCross()
        self.setBackupTargetAimCross()
        delay = 0.2 if BigWorld.getFps() <= 30 else 0.1
        if BigWorld.getFps() > 50 or self.isLockAim():
            delay = 0
        self.handle = BigWorld.callback(delay, self.updateCrossFrame)

    def newUpdateCrossFrame(self):
        if self.released:
            return
        if self._noNeedFrame():
            gameglobal.rds.ui.hideAimCross(True)
            gameglobal.rds.ui.hideAimCross(False)
            return
        if BigWorld.player() and BigWorld.player().id == BigWorld.player().targetLocked.id:
            gameglobal.rds.ui.hideAimCross(True)
        targetLocked = BigWorld.player().targetLocked
        notInCamera = self.entityNotInCamera(targetLocked)
        dist = self.getTargetLockDist()
        distStr = self.getDistStr(dist)
        if notInCamera:
            if targetLocked:
                self.outCameraState[targetLocked.id] = True
            p = BigWorld.player()
            gameglobal.rds.ui.hideAimCross()
            yaw = p.yaw - (targetLocked.position - p.position).yaw
            if yaw < -math.pi or yaw > 0 and yaw < math.pi:
                gameglobal.rds.ui.showTargetDir(AimCross.TARGET_DIR_X_OFFSET, self.targetDirY, distStr, 'left')
            else:
                gameglobal.rds.ui.showTargetDir(self.targetDirRightX, self.targetDirY, distStr, 'right')
        else:
            gameglobal.rds.ui.hideTargetDir()
            pos = self._getFramePos(targetLocked)
            if pos and self.oldPos and (int(self.oldPos[0]) != int(pos[0]) or int(self.oldPos[1]) != int(pos[1])):
                self.oldPos[0] = pos[0]
                self.oldPos[1] = pos[1]
                cType = self.getDistType(dist)
                if cType == AimCross.S_TYPE_START:
                    cType = AimCross.S_TYPE_NORMAL
                isLockAim = self.isLockAim()
                color = self.getAimCrossColor(targetLocked)
                if self.outCameraState.get(targetLocked.id, False):
                    gameglobal.rds.ui.showAimCross(pos[0], pos[1], distStr, cType, True, color, isLockAim)
                    self.outCameraState[targetLocked.id] = False
                gameglobal.rds.ui.setAimCrossPos(pos[0], pos[1], distStr, cType, True, color, isLockAim)
        self.setOptionalTargetAimCross()
        self.setBackupTargetAimCross()
        self.handle = BigWorld.callback(0.0, self.newUpdateCrossFrame)

    def getDistType(self, dist):
        p = BigWorld.player()
        if p.isInBfDota() and p.bianshen[1]:
            skillMaxDist = ZD.data.get(p.bianshen[1], {}).get('skillMaxDist', 20)
        else:
            skillMaxDist = SD.data[BigWorld.player().school].get('skillMaxDist', 20)
        if dist > skillMaxDist:
            cType = AimCross.S_TYPE_RED
        else:
            cType = AimCross.S_TYPE_NORMAL
        return cType

    def release(self):
        GUI.delRoot(self.cursorAim)
        GUI.delRoot(self.cursorAimed)
        self.released = True
