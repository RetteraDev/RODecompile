#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impNpcQuestMarker.o
import BigWorld
import gamelog
import gameglobal
import gametypes
import clientcom
import formula
import utils
import math
from sfx import sfx
from data import quest_marker_data as QMD
from data import skill_fx_data as SFD

class ImpNpcQuestMarker(object):

    def initQuestMarker(self):
        qmd = QMD.data[self.npcId]
        if qmd.get('trapSrc', gametypes.MARKER_NPC_TRAP_SERVER) == gametypes.MARKER_NPC_TRAP_CLIENT:
            trapWidth = qmd['clientTrapWidth']
            trapHeight = qmd['clientTrapHeight']
            BigWorld.addRectPot(self.matrix, trapWidth, trapHeight, self.onClientTrapCallback)
            self._checkClientTrap()

    def onClientTrapCallback(self, enteredTrap, handle):
        if self.inWorld and enteredTrap and self.isQuestMarkerValid():
            BigWorld.player().cell.onEnterQuestClientMarker(self.npcId, self.id)

    def spelledByAction(self):
        if not self.inWorld or not QMD.data.has_key(self.npcId):
            return
        elif not self.isQuestMarkerValid():
            return
        else:
            qmd = QMD.data[self.npcId]
            if not qmd.has_key('spellEff'):
                return
            eff = qmd['spellEff']
            fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             eff,
             sfx.EFFECT_UNLIMIT))
            gamelog.debug('bgf:spelledByUseItem', fxs, self.npcId, eff)
            if fxs:
                if SFD.data.get(eff, {}).get('modelKeepFx', False):
                    for fx in fxs:
                        fx.overCallback(None, -1)

                self.addFx(eff, fxs)
            return

    def cancelByAction(self):
        if not self.inWorld or not QMD.data.has_key(self.npcId):
            return
        qmd = QMD.data[self.npcId]
        if not qmd.has_key('spellEff'):
            return
        eff = qmd['spellEff']
        gamelog.debug('bgf:cancelByUseItem', self.npcId, eff)
        self.removeFx(eff)

    def getOpacityValueByMarker(self, opacityVal):
        if opacityVal[0] == gameglobal.OPACITY_HIDE:
            return opacityVal
        qmd = QMD.data[self.npcId]
        if self.markerFlag and qmd.get('triggerHide'):
            return (gameglobal.OPACITY_HIDE, False)
        player = BigWorld.player()
        if self.npcId in player.hideNpcs.keys():
            return (gameglobal.OPACITY_HIDE, False)
        visibility = opacityVal[0]
        qmd = QMD.data[self.npcId]
        questId = qmd.get('quest', 0)
        player = BigWorld.player()
        if qmd.get('hideUFO', 0) and (not questId or questId not in player.quests):
            visibility = gameglobal.OPACITY_HIDE
        return (visibility, opacityVal[1])

    def showViewRadii(self):
        qmd = QMD.data[self.npcId]
        if qmd.get('trapSrc', gametypes.MARKER_NPC_TRAP_SERVER) == gametypes.MARKER_NPC_TRAP_CLIENT:
            xscale = qmd['clientTrapWidth']
            zscale = qmd['clientTrapHeight']
            pos = clientcom.getRelativePosition(self.position, self.yaw, 0, -zscale / 2.0)
            xscale /= 5.0
            zscale /= 5.0
            yaw = self.yaw
        else:
            scope = qmd.get('scope', 0)
            pos = clientcom.getRelativePosition(self.position, 0, 0, -scope)
            xscale = zscale = scope * 2.0 / 5.0
            yaw = 0
        if pos:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (self.getSkillEffectLv(),
             self.getSkillEffectPriority(),
             None,
             3058,
             sfx.EFFECT_LIMIT_MISC,
             pos,
             0,
             yaw,
             0,
             sfx.MAXDELAYTIME))
        if fx:
            for fxItem in fx:
                fxItem.scale(xscale, 1, zscale)

    def isQuestMarkerValid(self):
        qmd = QMD.data[self.npcId]
        player = BigWorld.player()
        if self.markerFlag:
            return False
        if qmd.has_key('xingJiTimeIntervals'):
            if not formula.isInXingJiTimeIntervals(qmd.get('xingJiTimeIntervals')):
                return False
        if qmd.has_key('quest'):
            questId = qmd['quest']
            if questId in player.quests:
                return True
        if qmd.has_key('waQuest'):
            questId = qmd['waQuest']
            if questId in player.worldQuests:
                return True
        return False

    def _checkClientTrap(self):
        qmd = QMD.data[self.npcId]
        if qmd.get('trapSrc', gametypes.MARKER_NPC_TRAP_SERVER) == gametypes.MARKER_NPC_TRAP_CLIENT:
            trapWidth = qmd['clientTrapWidth']
            trapHeight = qmd['clientTrapHeight']
            rp1 = utils.getRelativePosition(self.position, self.yaw, 0, trapHeight)
            rp2 = utils.getRelativePosition(self.position, self.yaw, 180, trapHeight)
            pos = BigWorld.player().position
            p1 = utils.getRelativePosition(rp1, self.yaw, 90, trapWidth)
            p3 = utils.getRelativePosition(rp2, self.yaw, -90, trapWidth)
            if math.fabs(pos[0] - p1[0]) <= math.fabs(p3[0] - p1[0]) and math.fabs(pos[2] - p1[2]) <= math.fabs(p3[2] - p1[2]) and (pos[0] - p1[0]) * p3[0] - p1[0] > 0 and (pos[2] - p1[2]) * (p3[2] - p1[2]) > 0:
                self.onClientTrapCallback(True, None)

    def set_markerFlag(self, old):
        self.refreshOpacityState()
        if not self.markerFlag:
            self._checkClientTrap()
