#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impNpcGuildRobber.o
import gametypes

class ImpNpcGuildRobber(object):

    def set_robberNpcStatus(self, old):
        if not self.topLogo:
            return
        iconpath = '../npcIcon/Robber.dds'
        if self.robberNpcStatus == gametypes.NPC_GUILD_ROBBER_STATUS_OWNER or self.robberNpcStatus == gametypes.NPC_GUILD_ROBBER_STATUS_CHALLENGE:
            self.topLogo.hide(False)
            self.topLogo.setTaskIndicator(iconpath)
            self.topLogo.showTaskIndicator(True)
        elif self.robberNpcStatus == gametypes.NPC_GUILD_ROBBER_STATUS_FREE:
            self.topLogo.hide(True)

    def getNpcChatId(self):
        for key, data in gametypes.NPC_GUILD_ROBBER_STATUS_CHAT_ID.items():
            if self.robberNpcStatus == key:
                return data
