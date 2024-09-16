#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impGuildMemberSkill.o
import BigWorld
import gameglobal
import gametypes
import logicInfo
import const
from guis import uiUtils
from helpers.guild import GuildMemberSkill
from data import guild_pskill_data as GPD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from cdata import item_fame_score_cost_data as IFSCD

class ImpGuildMemberSkill(object):

    def sendGuildMemberSkill(self, data):
        bwTime = BigWorld.time()
        serverTime = self.getServerTime()
        logicInfo.cooldownGuildMemberSkill = {}
        self.guildMemberSkills.clear()
        for skillId, level, nextTime in data:
            self.guildMemberSkills[skillId] = GuildMemberSkill(skillId=skillId, level=level, nextTime=nextTime)
            if nextTime > serverTime:
                skillcd = gameglobal.rds.ui.skill.getGuildSkillCd(skillId, level)
                end = nextTime - serverTime + bwTime
                logicInfo.cooldownGuildMemberSkill[skillId] = (end, skillcd)
            gameglobal.rds.tutorial.onGuildMemberSkillTrigger(skillId)

    def onLearnGuildMemberSkill(self, skillId, level):
        if not self.guildMemberSkills.has_key(skillId):
            self.guildMemberSkills[skillId] = GuildMemberSkill(skillId=skillId, level=level)
        else:
            self.guildMemberSkills[skillId].level = level
            self.guildMemberSkills[skillId].nextTime = 0
        logicInfo.cooldownGuildMemberSkill.pop(skillId, None)
        gameglobal.rds.ui.skill.refreshGuildSkillPanel()
        gameglobal.rds.ui.actionbar.updateSlots()
        gameglobal.rds.tutorial.onGuildMemberSkillTrigger(skillId)

    def onCastGuildMemberSkill(self, skillId, nextTime):
        sk = self.guildMemberSkills.get(skillId, None)
        if not sk:
            return
        else:
            bwTime = BigWorld.time()
            serverTime = self.getServerTime()
            if nextTime > serverTime:
                skillcd = gameglobal.rds.ui.skill.getGuildSkillCd(skillId, sk.level)
                end = nextTime - serverTime + bwTime
                logicInfo.cooldownGuildMemberSkill[skillId] = (end, skillcd)
            gameglobal.rds.ui.skill.refreshGuildSkillPanel()
            gameglobal.rds.ui.actionbar.updateSlots()
            return

    def onResetGuildSKillCD(self, skillId, args):
        logicInfo.cooldownGuildMemberSkill.pop(skillId, None)
        gameglobal.rds.ui.skill.refreshGuildSkillPanel()
        gameglobal.rds.ui.actionbar.updateSlots()
        sk = self.guildMemberSkills.get(skillId, None)
        if not sk:
            return
        data = GPD.data.get((skillId, sk.level))
        if not data:
            return
        funcs = data.get('functions')
        if not funcs:
            return
        funcIds = [ f[0] for f in funcs ]
        if gametypes.GUILD_PSKILL_FUNCTION_SEEK_TELEPORT in funcIds:
            if len(args) > 0:
                if args[0].startswith('#'):
                    self.visitRoom(*args)
                else:
                    uiUtils._gotoTrack(args[0])
            return
        elif gametypes.GUILD_PSKILL_FUNCTION_TELEPORT in funcIds:
            self.showGameMsg(GMDD.data.RESET_TELEPORT_CD, ())
            return
        else:
            return

    def canResetCD(self, skillId):
        sk = self.guildMemberSkills.get(skillId, None)
        if not sk:
            return False
        else:
            data = GPD.data.get((skillId, sk.level))
            if not data:
                return False
            funcs = data.get('functions')
            if not funcs:
                return False
            funcIds = [ f[0] for f in funcs ]
            if gametypes.GUILD_PSKILL_FUNCTION_SEEK_TELEPORT in funcIds:
                resetCDItems = SCD.data.get('resetGuildTrackSkillCDItems', ())
                if resetCDItems:
                    itemId, numNeed = resetCDItems
                    itemHold = self.inv.countItemInPages(itemId, enableParentCheck=True)
                    if gameglobal.rds.configData.get('enableYunChuiScoreDikou', False):
                        return itemHold >= numNeed or self.fame.get(const.YUN_CHUI_JI_FEN_FAME_ID, 0) >= IFSCD.data.get(itemId, {}).get(const.YUN_CHUI_JI_FEN_FAME_ID, 0) * numNeed
                    else:
                        return itemHold >= numNeed
            if gametypes.GUILD_PSKILL_FUNCTION_TELEPORT in funcIds:
                resetCDItems = SCD.data.get('resetGuildTeleportSkillCDItems', ())
                resetCDBindCash = SCD.data.get('resetGuildTeleportSkillBindCash', 0)
                if resetCDItems:
                    itemId, numNeed = resetCDItems
                    itemHold = self.inv.countItemInPages(itemId, enableParentCheck=True)
                    if itemHold >= numNeed:
                        return True
                    if resetCDBindCash and self._canPay(resetCDBindCash):
                        return True
            if gametypes.GUILD_PSKILL_FUNCTION_ENTER_SCENE in funcIds:
                resetCDItems = SCD.data.get('resetGuildEnterSceneSkillCDItems', ())
                for itemId in resetCDItems:
                    itemHold = self.inv.countItemInPages(itemId, enableParentCheck=True)
                    if itemHold:
                        return True

            return False

    def onGuildCallTeamMateConfirm(self, gbId):
        gameglobal.rds.ui.callTeammate.beCalled(gbId)
