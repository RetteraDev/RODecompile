#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impQieCuo.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import const
import formula
from helpers import ufo
from sMath import distance3D
from callbackHelper import Functor
from guis import messageBoxProxy
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD

class ImpQieCuo(object):

    def qieCuoRequest(self, who):
        e = BigWorld.entities.get(who)
        if not e or not e.inWorld:
            return
        else:
            if not hasattr(self, 'qieCuoQueue'):
                self.qieCuoQueue = {}
                self.qieCuoCallbackHandler = {}
            if self.qieCuoQueue.has_key(who):
                return
            MBButton = messageBoxProxy.MBButton
            acceptBtn = MBButton(gameStrings.TEXT_IMPFRIEND_2211, Functor(self.onQieCuoAccept, who))
            rejectBtn = MBButton(gameStrings.TEXT_IMPFRIEND_963, Functor(self.onQieCuoReject, who))
            msgBoxId = gameglobal.rds.ui.messageBox.show(False, '', gameStrings.TEXT_IMPQIECUO_34 % e.roleName, [acceptBtn, rejectBtn])
            t = int(BigWorld.time())
            name = e.roleName
            if name == None:
                return
            self.qieCuoQueue[who] = (t, name)
            self.qieCuoCallbackHandler[who] = BigWorld.callback(const.QIECUO_REQ_TIMEOUT, Functor(self.autoCancelQieCuoRequest, msgBoxId, who, t))
            gameglobal.rds.sound.playSound(gameglobal.SD_32)
            return

    def set_qieCuoTargetTemp(self, old):
        if self.qieCuoTargetTemp:
            self.startQieCuoPrepareCountdown()

    def set_qieCuoTarget(self, oldTarget):
        if self.topLogo:
            self.topLogo.updateRoleName(self.topLogo.name)
        p = BigWorld.player()
        targetId = self.qieCuoTarget or oldTarget
        target = BigWorld.entities.get(targetId)
        if target and target.topLogo:
            target.topLogo.updateRoleName(target.topLogo.name)
            target.refreshOpacityState()
        if p.targetLocked == target:
            ufoType = ufo.UFO_NORMAL
            if p.isEnemy(target):
                ufoType = p.getTargetUfoType(target)
            self.setTargetUfo(target, ufoType)
        p.updateTargetFocus(target)
        if self.qieCuoTarget:
            gameglobal.rds.ui.surrender.show()
        else:
            gameglobal.rds.ui.surrender.hide()
            surrenderBoxId = getattr(gameglobal.rds.ui.surrender, 'surrenderBoxId', None)
            if surrenderBoxId:
                gameglobal.rds.ui.surrender.surrenderBoxId = None
                gameglobal.rds.ui.messageBox.dismiss(surrenderBoxId)
        gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_SKILL_TGT)

    def qieCuoStart(self):
        pass

    def qieCuoEnd(self, result):
        gameglobal.rds.ui.arena.closeArenaCountDown()

    def isInQieCuo(self):
        return self.qieCuoTarget != 0

    def isInQieCuoOrPrepare(self):
        return self.qieCuoTarget != 0 or self.qieCuoTargetTemp != 0

    def isQieCuoWith(self, targetId):
        target = BigWorld.entities.get(targetId)
        if target and target.IsSummonedBeast:
            targetId = target.ownerId
        elif target and target.IsCreation and target.IsCombatCreation:
            targetId = target.ownerId
        return self.isInQieCuo() and self.qieCuoTarget == targetId

    def sendQieCuoRequest(self, targetId):
        p = BigWorld.player()
        target = BigWorld.entities.get(targetId)
        if target:
            if distance3D(p.position, target.position) > const.QIECUO_REQ_DIST:
                p.showGameMsg(GMDD.data.QIECUO_REQ_DIST_EXCEED, ())
                return
            if formula.mapLimit(formula.LIMIT_QIECUO, formula.getMapId(self.spaceNo)):
                p.showGameMsg(GMDD.data.QIECUO_FORBID_IN_MAP, ())
                return
            p.cell.qieCuoRequest(targetId)

    def autoCancelQieCuoRequest(self, msgBoxId, who, time):
        if not hasattr(self, 'qieCuoQueue'):
            return
        if self.qieCuoQueue.has_key(who) and self.qieCuoQueue[who][0] == time:
            self.qieCuoQueue.pop(who)
            gameglobal.rds.ui.messageBox.dismiss(msgBoxId)
            BigWorld.player().cell.qieCuoReject(who, True)

    def onQieCuoAccept(self, who):
        BigWorld.player().cell.qieCuoAccept(who)
        if self.qieCuoCallbackHandler.has_key(who):
            BigWorld.cancelCallback(self.qieCuoCallbackHandler.pop(who))
        if self.qieCuoQueue.has_key(who):
            self.qieCuoQueue.pop(who)
        gameglobal.rds.sound.playSound(gameglobal.SD_2)

    def onQieCuoReject(self, who):
        BigWorld.player().cell.qieCuoReject(who, False)
        if self.qieCuoCallbackHandler.has_key(who):
            BigWorld.cancelCallback(self.qieCuoCallbackHandler.pop(who))
        if self.qieCuoQueue.has_key(who):
            self.qieCuoQueue.pop(who)
        gameglobal.rds.sound.playSound(gameglobal.SD_3)

    def qieCuoPrepareCountdown(self):
        if not hasattr(self, 'qieCuoCountTimer'):
            return
        if not gameglobal.rds.ui.arena.arenaCountDownMed:
            self.setArenaCallback(BigWorld.callback(1, Functor(self.qieCuoPrepareCountdown)))
            return
        self.callArenaMsg('showCountDown5', (self.qieCuoCountTimer,))
        gameglobal.rds.sound.playSound(gameglobal.SD_60)
        self.qieCuoCountTimer -= 1
        if self.qieCuoCountTimer > 0:
            self.setArenaCallback(BigWorld.callback(1, Functor(self.qieCuoPrepareCountdown)))

    def startQieCuoPrepareCountdown(self):
        self.qieCuoCountTimer = const.QIECUO_PREPARE_DISPLAY_INTERVAL
        gameglobal.rds.ui.arena.openArenaMsg()
        BigWorld.callback(0.5, Functor(self.qieCuoPrepareCountdown))

    def confirmQieCuoSurrender(self):
        if getattr(gameglobal.rds.ui.surrender, 'surrenderBoxId', None):
            return
        else:
            MBButton = messageBoxProxy.MBButton
            okBtn = MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.sendQieCuoSurrenderRequest))
            cancelBtn = MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, Functor(self.cancelQieCuoSurrenderRequest))
            gameglobal.rds.ui.surrender.surrenderBoxId = gameglobal.rds.ui.messageBox.show(False, '', gameStrings.TEXT_IMPQIECUO_187, [okBtn, cancelBtn])
            return

    def sendQieCuoSurrenderRequest(self):
        gameglobal.rds.ui.surrender.surrenderBoxId = None
        if self.isInQieCuo():
            self.cell.qieCuoSurrender()

    def cancelQieCuoSurrenderRequest(self):
        gameglobal.rds.ui.surrender.surrenderBoxId = None

    def onQieCuoResult(self, msgId, args):
        msg = GMD.data.get(msgId).get('text') % args
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_VIEW, msg, '')
