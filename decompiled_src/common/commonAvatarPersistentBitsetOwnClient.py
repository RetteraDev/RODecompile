#Embedded file name: I:/bag/tmp/tw2/res/entities\common/commonAvatarPersistentBitsetOwnClient.o
import BigWorld
import commcalc
import gameCommonBitset

class ImpAvatarPersistentBitSetOwnClient(object):

    def _persistentOwnClientFlagCheck(self):
        if BigWorld.component in ('client',):
            return False
        return True

    def _syncPersisitentOwnClientFlags(self):
        if not self._persistentOwnClientFlagCheck():
            return
        self.ownClientPersistentFlags = self.ownClientPersistentFlags

    @property
    def appBindRewarded(self):
        return commcalc.getBitDword(self.ownClientPersistentFlags, gameCommonBitset.AVT_OWN_CLIENT_PERSISTENT_FLAG_DWORD_APP_BIND_REWARDED)

    @appBindRewarded.setter
    def appBindRewarded(self, on):
        if not self._persistentOwnClientFlagCheck():
            return
        self.ownClientPersistentFlags = commcalc.calcBitDword(self.ownClientPersistentFlags, gameCommonBitset.AVT_OWN_CLIENT_PERSISTENT_FLAG_DWORD_APP_BIND_REWARDED, on)
        self._syncPersisitentOwnClientFlags()

    @property
    def weixinBindRewarded(self):
        return commcalc.getBitDword(self.ownClientPersistentFlags, gameCommonBitset.AVT_OWN_CLIENT_PERSISTENT_FLAG_DWORD_WEIXIN_BIND_REWARDED)

    @weixinBindRewarded.setter
    def weixinBindRewarded(self, on):
        if not self._persistentOwnClientFlagCheck():
            return
        self.ownClientPersistentFlags = commcalc.calcBitDword(self.ownClientPersistentFlags, gameCommonBitset.AVT_OWN_CLIENT_PERSISTENT_FLAG_DWORD_WEIXIN_BIND_REWARDED, on)
        self._syncPersisitentOwnClientFlags()

    @property
    def worldRefreshQuestRewarded(self):
        return commcalc.getBitDword(self.ownClientPersistentFlags, gameCommonBitset.AVT_OWN_CLIENT_PERSISTENT_FLAG_DWORD_WORLD_REFRESH_QUEST_REWARDED)

    @worldRefreshQuestRewarded.setter
    def worldRefreshQuestRewarded(self, on):
        if not self._persistentOwnClientFlagCheck():
            return
        self.ownClientPersistentFlags = commcalc.calcBitDword(self.ownClientPersistentFlags, gameCommonBitset.AVT_OWN_CLIENT_PERSISTENT_FLAG_DWORD_WORLD_REFRESH_QUEST_REWARDED, on)
        self._syncPersisitentOwnClientFlags()
