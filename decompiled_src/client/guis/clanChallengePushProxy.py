#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/clanChallengePushProxy.o
import BigWorld
from guis import generalPushProxy
import const
import gameconfigCommon
from guis import uiConst
import gameglobal

class ClanChallengePushProxy(generalPushProxy.GeneralPushItemProxy):

    def __init__(self, uiAdapter):
        super(ClanChallengePushProxy, self).__init__(uiAdapter)

    def isShowHintEff(self):
        return const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_ROUND1 <= self.pushState <= const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_ROUND5

    def onClickItem(self, *args):
        if const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_ROUND1 > self.pushState >= const.CLAN_WAR_CHALLENGE_STAGE_APPLY:
            self.uiAdapter.clanChallenge.jumpIdx = 1
            self.uiAdapter.guild.show(uiConst.GUILDINFO_TAB_CHALLENGE)
        elif const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_ROUND1 <= self.pushState < const.CLAN_WAR_CHALLENGE_STAGE_END:
            self.uiAdapter.clanChallengeObList.show()
        elif self.pushState == const.CLAN_WAR_CHALLENGE_STAGE_END:
            self.uiAdapter.clanChallenge.jumpIdx = 1
            self.uiAdapter.guild.show(uiConst.GUILDINFO_TAB_CHALLENGE)

    def inShowState(self):
        return const.CLAN_WAR_CHALLENGE_STAGE_APPLY <= getattr(BigWorld.player(), 'clanWarChallengeState', 0) <= const.CLAN_WAR_CHALLENGE_STAGE_END

    def isPushItemEnabled(self, state):
        return gameconfigCommon.enableClanWarChallenge() and const.CLAN_WAR_CHALLENGE_STAGE_APPLY <= state <= const.CLAN_WAR_CHALLENGE_STAGE_END
