#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client/GuildDawdler.o
from gamestrings import gameStrings
import copy
import BigWorld
import gametypes
import gameglobal
import npcConst
from Dawdler import Dawdler
from cdata import game_msg_def_data as GMDD
from data import guild_job_data as GJD
from data import guild_building_marker_data as GBMD
from data import guild_config_data as GCD

class GuildDawdler(Dawdler):

    def use(self):
        p = BigWorld.player()
        if p.life == gametypes.LIFE_DEAD:
            p.showGameMsg(GMDD.data.FORBIDDEN_WRONG_LIFE, ())
            return
        if self.forbidUse():
            return
        if p.inBooth():
            return
        self.cell.useGuildDawdler()
        soundIdx = self.getItemData().get('useNpcSound', 0)
        gameglobal.rds.sound.playSound(soundIdx)

    def onUseGuildDawdler(self):
        p = BigWorld.player()
        if p.life == gametypes.LIFE_DEAD:
            p.showGameMsg(GMDD.data.FORBIDDEN_WRONG_LIFE, ())
            return
        if not self.checkDistSqr(25) or self.forbidUse():
            return
        if self.guildNUID and self.guildNUID != p.guildNUID:
            p.showGameMsg(GMDD.data.FORBIDDEN_WRONG_GUILD, ())
            return
        if hasattr(p, 'isTrading') and p.isTrading:
            p.showGameMsg(GMDD.data.ITEM_TRADE_NO_NPC_CHAT, ())
            return
        options = self.parseFunctions()
        if options:
            p.npcDialog(self.id, options)
        else:
            self.showMultiNpcChatWin(False)

    def getNpcPriority(self):
        return gameglobal.NPC_WITH_FUNC

    def parseFunctions(self):
        options = {}
        functions = self.filterFunctions()
        for funcName, func, funcId in functions:
            self.addToOption(options, (func, funcName), funcId)

        return options

    def filterFunctions(self):
        p = BigWorld.player()
        if p.guildNUID != self.guildNUID:
            return []
        if self.jobId:
            functions = copy.copy(GJD.data.get(self.jobId).get('functions', []))
        else:
            functions = []
        functions.append((gameStrings.TEXT_GUILDDAWDLER_75, npcConst.NPC_FUNC_GUILD, gametypes.GUILD_NPC_OPTION_VIEW_HIRED_RESIDENT))
        functions.append((gameStrings.TEXT_GUILDDAWDLER_76, npcConst.NPC_FUNC_GUILD, gametypes.GUILD_NPC_OPTION_ASSIGN_JOB))
        functions.append((gameStrings.TEXT_GUILDDAWDLER_77, npcConst.NPC_FUNC_GUILD_RESIDENT_TIRED, 0))
        return functions

    def addToOption(self, options, funcId, value):
        if options.has_key(funcId):
            options[funcId].append(value)
        else:
            options[funcId] = [value]

    @property
    def buildingNUID(self):
        p = BigWorld.player()
        if not p.guild or not p.guild.inSpace(p):
            return 0
        if not self.jobId:
            return 0
        jdata = GJD.data.get(self.jobId)
        if jdata.get('placeType') == gametypes.GUILD_JOB_PLACE_MARKER:
            buildingId = GBMD.data.get(jdata.get('placeId'), {}).get('buildingId', 0)
            building = p.guild.getBuildingById(buildingId)
            if building:
                return building.nuid
        return 0

    def playEvent(self, trapEvent, trapLengthType):
        super(GuildDawdler, self).playEvent(trapEvent, trapLengthType)
        p = BigWorld.player()
        if not hasattr(p, 'guild') or not p.guild:
            return
        elif not p.guild.hiredResident.has_key(self.residentNUID):
            return
        else:
            tiredStep = GCD.data.get('DawdlerTiredStep', [])
            if tiredStep:
                tired = p.guild.hiredResident[self.residentNUID].tired
                for minTired, maxTired, iconId in tiredStep:
                    if tired >= minTired and tired <= maxTired:
                        self.topLogo.showBigEmote(iconId) if self.topLogo else None
                        break

            return
