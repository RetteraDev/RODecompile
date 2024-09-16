#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impWingWorldCamp.o
from gamestrings import gameStrings
import gametypes
import gamelog
import const
import gameglobal
from guis import uiConst
import wingWorldUtils
from gamestrings import gameStrings

class ImpWingWorldCamp(object):

    def onSignUpWingWorldCampSucc(self, bGuild, bSignUp):
        gameglobal.rds.ui.wingWorldCamp.refreshInfo()
        gameglobal.rds.ui.wingCampGuildList.refreshInfo()

    def onGuildSignUpSucc(self):
        gameglobal.rds.ui.wingWorldCamp.refreshInfo()

    def canEnterWWCamp(self):
        if gameglobal.rds.configData.get('enableWingWorldWarCamp', False):
            return self.lv > wingWorldUtils.getEnterWingWorldMapMinLevel()
        return False

    def isWingWorldCamp(self):
        return gameglobal.rds.configData.get('enableWingWorldWarCamp', False)

    def isWingWorldCampMode(self):
        return gameglobal.rds.configData.get('enableWingWorldWarCampMode', False)

    def isWingWorldCampArmy(self):
        return gameglobal.rds.configData.get('enableWingWorldCampArmy', False)

    def set_bWWCampMemberSignUp(self, oldVal):
        gamelog.debug('dxk@ impWingWorldCamp bWWCampMemberSignUp', self.bWWCampMemberSignUp)
        gameglobal.rds.ui.wingWorldCamp.refreshInfo()
        if self.isWWCampSignUp():
            self.removeWWCampStatePush()

    def set_bWWCampFollowGuild(self, oldVal):
        gamelog.debug('dxk@ impWingWorldCamp bWWCampFollowGuild', self.bWWCampFollowGuild)
        gameglobal.rds.ui.wingCampGuildList.refreshInfo()
        gameglobal.rds.ui.wingWorldCamp.refreshInfo()
        if self.isWWCampSignUp():
            self.removeWWCampStatePush()

    def onSetWingWorldCamp(self, oldVal):
        gameglobal.rds.ui.wingWorldCamp.refreshInfo()
        gameglobal.rds.ui.wingWorld.reflowTabBtns()

    def set_wingWorldCampState(self, oldVal):
        if not self.isWingWorldCamp():
            return
        gameglobal.rds.ui.wingWorldCamp.refreshInfo()
        if not self.isWWCampSignUp() and self.wingWorldCampState in (gametypes.WW_CAMP_STATE_SIGNUP_START, gametypes.WW_CAMP_STATE_START):
            if self.lv >= 69:
                gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WING_WORLD_CAMP_START_SIGN, {'click': self.onNotifyWWCampConfirmClick})
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_CAMP_START_SIGN)

    def removeWWCampStatePush(self):
        if uiConst.MESSAGE_TYPE_WING_WORLD_CAMP_START_SIGN in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_CAMP_START_SIGN)

    def onNotifyWWCampConfirmClick(self):
        self.removeWWCampStatePush()
        if self.isWingWorldCamp():
            gameglobal.rds.ui.wingWorld.show(uiConst.WING_WORLD_TAB_CAMP)

    def isWWCampSignUp(self):
        return getattr(self, 'bWWCampMemberSignUp', False) or getattr(self, 'bWWCampFollowGuild', False)

    def isWWCampSingleSignUp(self):
        return getattr(self, 'bWWCampMemberSignUp', False)

    def isWWCampFollowGuildSignUp(self):
        return getattr(self, 'bWWCampFollowGuild', False)

    def isInWingWorldCamp(self):
        return getattr(self, 'wingWorldCamp', 0) != 0

    def isWWCampGuildCampSame(self):
        if self.guild and self.isInWingWorldCamp():
            return getattr(self.guild, 'wingWorldCamp', 0) == self.wingWorldCamp
        return False

    def canEditWingCampNotice(self):
        return getattr(self, 'wingWorldPostId', 0) == 1 and self.isWingWorldCampArmy()

    def onQueryWingWorldCampLeader(self, campId, guildLeader, personLeader):
        pass

    def onQueryWWGuildContri(self, groupId, campId, ver, topData):
        gamelog.debug('dxk@onQueryWWGuildContri', groupId, campId, ver, topData)
        gameglobal.rds.ui.wingWorldCamp.updateGuildRank(groupId, campId, ver, topData)

    def onQueryWWPersonContri(self, groupId, campId, ver, topData):
        gamelog.debug('dxk@onQueryWWPersonContri', groupId, campId, ver, topData)
        gameglobal.rds.ui.wingWorldCamp.updatePersonRank(groupId, campId, ver, topData)

    def onQueryWWCNotification(self, campId, msg):
        gamelog.debug('dxk@onQueryWWCNotification', campId, msg)
        self.wingWorld.country.getCamp(campId).updateNotice(msg)
        gameglobal.rds.ui.wingWorldOverView.refreshCampNotice()

    def addCampNoticeMessage(self):
        if self.isWingWorldCampMode() and self.wingWorldCamp:
            if self.wingWorldCampState not in (gametypes.WW_CAMP_STATE_START,):
                return
            msg = self.wingWorld.country.getCamp(self.wingWorldCamp).notice
            if msg and self.wingWorldCamp == self.wingWorldCamp:
                if self.wingWorld.country.getCamp(self.wingWorldCamp).notice:
                    if self.inWingWarCity() or self.inWingBornIsland():
                        if self.canEditWingCampNotice():
                            msg += gameStrings.TEXT_IMPWINGWORLDCAMP_125 % gameStrings.EDIT
                        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_WING_WORLD_CAMP, msg, gameStrings.WING_WORLD_CAMP_NOTICE)

    def onQueryWingWorldCampCities(self, data):
        for campId, cityList in (data or {}).iteritems():
            campVal = self.wingWorld.country.getCamp(campId)
            campVal.ownedCityIds = cityList

        gameglobal.rds.ui.wingWorldCamp.refreshCityMc()
