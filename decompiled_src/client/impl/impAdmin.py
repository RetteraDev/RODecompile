#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impAdmin.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import utils
from guis import uiConst
from data import npc_model_client_data as NMCD
from cdata import game_msg_def_data as GMDD
from data import monster_model_client_data as MMCD
from data import state_data as SD

class ImpAdmin(object):

    def onGMClearSkills(self):
        self.skills.clear()

    def searchNpc(self, keyName):
        found = False
        keyName = keyName.decode(utils.defaultEncoding())
        for npcId, npcInfo in NMCD.data.iteritems():
            npcName = npcInfo.get('name')
            npcModelId = npcInfo.get('model')
            if npcName and keyName in npcName.decode(utils.defaultEncoding()):
                found = True
                self.chatToGm('%d: %d: %s' % (npcId, npcModelId, npcName))

        if not found:
            self.chatToGm(gameStrings.TEXT_IMPADMIN_26)

    def searchMonsterModel(self, monsterIdDict):
        if not monsterIdDict:
            self.chatToGm(gameStrings.TEXT_IMPADMIN_30)
        for monsterId in monsterIdDict.keys():
            modelId = MMCD.data.get(monsterId, {}).get('model', 0)
            monsterName = monsterIdDict.get(monsterId)
            self.chatToGm('%d: %d: %s' % (monsterId, modelId, monsterName))

    def gmFollowOtherAvatar(self, entityId):
        entity = BigWorld.entities.get(entityId)
        if entity:
            if not self.ap.isTracing:
                self.followOtherAvatarWithDist(entity, 2.0)

    def gmFollowAvatarClient(self):
        ent = BigWorld.entities.get(self.gmFollow, None)
        if ent:
            self.refreshFollowAvatarClient()
        else:
            self.checkFollowLoad()

    def checkFollowLoad(self):
        if not self.gmFollow:
            return
        else:
            ent = BigWorld.entities.get(self.gmFollow, None)
            if ent:
                self.refreshFollowAvatarClient()
                return
            BigWorld.callback(0.3, self.checkFollowLoad)
            return

    def refreshFollowAvatarClient(self):
        if self.isInBfDota():
            self.physics.followTarget = None
        if self.gmFollow:
            self.modelServer.enterGmFollow()
        else:
            self.modelServer.leaveGmFollow()

    def onAvatarPeekAnotherFail(self, msg):
        BigWorld.player().showGameMsg(GMDD.data.COMMON_MSG, msg)

    def onAvatarPeekAnotherSucc(self):
        gameglobal.rds.ui.characterCopy.clearWidget()

    def showGuildTournamentPKList(self, gType):
        self.gtnLiveType = gType
        if gType == gametypes.BATTLE_FIELD_DOMAIN_GUILD_TOURNAMENT:
            gameglobal.rds.ui.guildMatch.show()
        elif gType == gametypes.BATTLE_FIELD_DOMAIN_CROSS_GTN:
            gameglobal.rds.ui.guild.show(uiConst.GUILDINFO_TAB_CROSS_TOURNAMENT)

    def updateShowViewInfo(self, showViewInfo):
        gametypes.NO_SHOW_SCOPE, gametypes.ENABLE_SHOW_GLOBAL_CALC_SCOPE, gameglobal.rds.showScopeViewIds = showViewInfo

    def onSearchState(self, stateSet):
        if not stateSet:
            self.chatToGm(gameStrings.TEXT_IMPADMIN_89)
            return
        for stateId in stateSet:
            stateInfo = SD.data.get(stateId, {})
            stateName = stateInfo.get('name', '')
            stateDesc = stateInfo.get('desc', '')
            self.chatToGm('%d: %s: %s' % (stateId, stateName, stateDesc))

    def onGetEntitySkill(self, skillList):
        if not skillList:
            self.chatToGm(gameStrings.TEXT_IMPADMIN_99)
            return
        for skillId, skillName in skillList:
            self.chatToGm('%d: %s' % (skillId, skillName))
