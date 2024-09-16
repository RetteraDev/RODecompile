#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impNpcShaxing.o
import gametypes
import gameglobal
from sfx import sfx
from helpers import action
from data import sys_config_data as SCD
from data import npc_model_client_data as NMCD

class ImpNpcShaxing(object):

    def set_shaxingNpcStatus(self, old):
        if self.topLogo:
            self.topLogo.showTopIcon(self)
        if self.shaxingNpcStatus == gametypes.NPC_SHAXING_STATUS_DESTROY:
            lv = self.getSkillEffectLv()
            priority = self.getSkillEffectPriority()
            effId = SCD.data.get('shaXingNpcLeaveEff')
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (lv,
             priority,
             self.model,
             effId,
             sfx.EFFECT_UNLIMIT,
             gameglobal.EFFECT_LAST_TIME))
        if self.shaxingNpcStatus == gametypes.NPC_SHAXING_STATUS_DESTROY_SUCC_TRANSITION:
            shaXingDestroyAct = NMCD.data.get(self.npcId, {}).get('shaXingDestroyAct', None)
            shaXingDestroyEff = NMCD.data.get(self.npcId, {}).get('shaXingDestroyEff', None)
            if shaXingDestroyAct:
                playSeq = []
                effs = [shaXingDestroyEff] if shaXingDestroyEff else []
                playSeq.append((shaXingDestroyAct,
                 effs,
                 action.COUPLE_EMOTE_SHAXING_DESTROY_ACTION,
                 1,
                 1.0,
                 None))
                self.fashion.playActionWithFx(playSeq, action.COUPLE_EMOTE_SHAXING_DESTROY_ACTION, None, False, 0, 0)
                if hasattr(self, 'stopAttachedDataEffects'):
                    self.stopAttachedDataEffects()
        if self.shaxingNpcStatus == gametypes.NPC_SHAXING_STATUS_DESTROY_TIMEOUT_TRANSITION:
            shaXingDestroyTimeoutAct = NMCD.data.get(self.npcId, {}).get('shaXingDestroyTimeoutAct', None)
            shaXingDestroyTimeoutEff = NMCD.data.get(self.npcId, {}).get('shaXingDestroyTimeoutEff', None)
            if shaXingDestroyTimeoutAct:
                playSeq = []
                effs = [shaXingDestroyTimeoutEff] if shaXingDestroyTimeoutEff else []
                playSeq.append((shaXingDestroyTimeoutAct,
                 effs,
                 action.COUPLE_EMOTE_SHAXING_DESTROY_ACTION,
                 1,
                 1.0,
                 None))
                self.fashion.playActionWithFx(playSeq, action.COUPLE_EMOTE_SHAXING_DESTROY_ACTION, None, False, 0, 0)
                if hasattr(self, 'stopAttachedDataEffects'):
                    self.stopAttachedDataEffects()
