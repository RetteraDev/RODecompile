#Embedded file name: /WORKSPACE/data/entities/common/commonavatarbitsetownclient.o
import BigWorld
import commcalc
import gameCommonBitset

class ImpAvatarBitSetOwnClient(object):

    @property
    def usingLifeSkill(self):
        return commcalc.getBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_USING_LIFE_SKILL)

    @usingLifeSkill.setter
    def usingLifeSkill(self, on):
        if not self._preCheckSet():
            return
        self.avatarOwnClientFlags = commcalc.calcBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_USING_LIFE_SKILL, on)

    @property
    def repairingLifeEquipment(self):
        return commcalc.getBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_REPAIRING_LIFE_EQUIPMENT)

    @repairingLifeEquipment.setter
    def repairingLifeEquipment(self, on):
        if not self._preCheckSet():
            return
        self.avatarOwnClientFlags = commcalc.calcBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_REPAIRING_LIFE_EQUIPMENT, on)

    @property
    def hasInvPassword(self):
        return commcalc.getBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_HAS_INV_PASSWORD)

    @hasInvPassword.setter
    def hasInvPassword(self, on):
        if not self._preCheckSet():
            return
        self.avatarOwnClientFlags = commcalc.calcBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_HAS_INV_PASSWORD, on)

    @property
    def hasPhoneBinding(self):
        return commcalc.getBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_HAS_PHONE_BINDING)

    @hasPhoneBinding.setter
    def hasPhoneBinding(self, on):
        if not self._preCheckSet():
            return
        self.avatarOwnClientFlags = commcalc.calcBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_HAS_PHONE_BINDING, on)

    @property
    def isQuestZaiju(self):
        return commcalc.getBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_IS_QUEST_ZAIJU)

    @isQuestZaiju.setter
    def isQuestZaiju(self, on):
        if not self._preCheckSet():
            return
        self.avatarOwnClientFlags = commcalc.calcBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_IS_QUEST_ZAIJU, on)

    @property
    def hasIntimacyTgt(self):
        return commcalc.getBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_HAS_INTIMACY_TGT)

    @hasIntimacyTgt.setter
    def hasIntimacyTgt(self, on):
        if not self._preCheckSet():
            return
        self.avatarOwnClientFlags = commcalc.calcBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_HAS_INTIMACY_TGT, on)

    @property
    def isFbGuideMode(self):
        return commcalc.getBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_IS_FB_GUIDE_MODE)

    @isFbGuideMode.setter
    def isFbGuideMode(self, on):
        if not self._preCheckSet():
            return
        self.avatarOwnClientFlags = commcalc.calcBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_IS_FB_GUIDE_MODE, on)

    @property
    def clanWarStatus(self):
        return commcalc.getBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_CLAN_WAR_STATUS)

    @clanWarStatus.setter
    def clanWarStatus(self, on):
        if not self._preCheckSet():
            return
        self.avatarOwnClientFlags = commcalc.calcBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_CLAN_WAR_STATUS, on)

    @property
    def worldAreaValid(self):
        return commcalc.getBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_WORLD_AREA_VALID)

    @worldAreaValid.setter
    def worldAreaValid(self, on):
        if not self._preCheckSet():
            return
        self.avatarOwnClientFlags = commcalc.calcBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_WORLD_AREA_VALID, on)

    @property
    def canReliveByGuild(self):
        return commcalc.getBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_CAN_RELIVE_BY_GUILD)

    @canReliveByGuild.setter
    def canReliveByGuild(self, on):
        if not self._preCheckSet():
            return
        self.avatarOwnClientFlags = commcalc.calcBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_CAN_RELIVE_BY_GUILD, on)

    @property
    def guildBusiness(self):
        return commcalc.getBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_GUILD_BUSINESS)

    @guildBusiness.setter
    def guildBusiness(self, on):
        if not self._preCheckSet():
            return
        self.avatarOwnClientFlags = commcalc.calcBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_GUILD_BUSINESS, on)

    @property
    def isFbAssister(self):
        return commcalc.getBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_IS_FB_ASSITER)

    @isFbAssister.setter
    def isFbAssister(self, on):
        if not self._preCheckSet():
            return
        self.avatarOwnClientFlags = commcalc.calcBitDword(self.avatarOwnClientFlags, gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_IS_FB_ASSITER, on)

    def _preCheckSet(self):
        if BigWorld.component in ('client',):
            return False
        return True
