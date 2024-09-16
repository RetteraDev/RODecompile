#Embedded file name: I:/bag/tmp/tw2/res/entities\client/Goblin.o
import BigWorld
import gameglobal
from Monster import Monster
from helpers import action
from sfx import sfx
from data import goblin_data as GD

class Goblin(Monster):
    IsMonster = True
    IsSummonedBeast = False

    def __init__(self):
        super(Goblin, self).__init__()
        self.vanishStartEffID = GD.data.get(self.goblinId, {}).get('vanishStartEff', None)
        self.vanishEffID = GD.data.get(self.goblinId, {}).get('vanishEff', None)
        self.stopVanishEffID = GD.data.get(self.goblinId, {}).get('stopVanishEff', None)
        self.vanishStartEffFx = None

    def enterVanish(self):
        BigWorld.callback(0.2, self._playVanishStartAct)

    def _playVanishStartAct(self):
        if not self.inWorld:
            return
        playSeq = []
        vanishStartAct = GD.data.get(self.goblinId, {}).get('vanishStartAct', None)
        vanishAct = GD.data.get(self.goblinId, {}).get('vanishAct', None)
        if vanishStartAct and vanishAct:
            playSeq.append((vanishStartAct,
             [],
             action.CAST_ACTION,
             0,
             1.0,
             None))
            playSeq.append((vanishAct,
             [],
             action.CAST_ACTION,
             0,
             1.0,
             None))
            self.fashion.playActionWithFx(playSeq, action.CAST_ACTION, None, False, 0, 1.0)
        self.vanishStartEffFx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
         self.getBasicEffectPriority(),
         self.model,
         self.vanishStartEffID,
         sfx.EFFECT_UNLIMIT,
         5.5))

    def realVanish(self):
        playSeq = []
        act = GD.data.get(self.goblinId, {}).get('vanishAct', None)
        if act != None:
            playSeq.append((act,
             [self.vanishEffID],
             action.CAST_ACTION,
             0,
             1.0,
             None))
            self.fashion.playActionWithFx(playSeq, action.CAST_ACTION, None, False, 0, 1.0)

    def leaveVanish(self):
        if self.vanishStartEffFx:
            sfx.detachEffect(self.model, self.vanishStartEffID, self.vanishStartEffFx)
            self.vanishStartEffFx = None
        self.fashion.stopAllActions()
        playSeq = []
        act = GD.data.get(self.goblinId, {}).get('stopVanishAct', None)
        if act != None:
            playSeq.append((act,
             [self.stopVanishEffID],
             action.CAST_ACTION,
             0,
             1.0,
             None))
            self.fashion.playActionWithFx(playSeq, action.CAST_ACTION, None, False)

    def playDieAction(self, needDieAction = True, forcePlayAction = False):
        super(Goblin, self).playDieAction(needDieAction, forcePlayAction)
        self.fashion._releaseFx()
        if self.vanishStartEffFx:
            sfx.detachEffect(self.model, self.vanishStartEffID, self.vanishStartEffFx)
            self.vanishStartEffFx = None
            if self.stopVanishEffID:
                self.stopVanishEffFx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                 self.getBasicEffectPriority(),
                 self.model,
                 self.stopVanishEffID,
                 sfx.EFFECT_UNLIMIT,
                 gameglobal.EFFECT_LAST_TIME))
                self.addFx(self.stopVanishEffID, self.stopVanishEffFx)
