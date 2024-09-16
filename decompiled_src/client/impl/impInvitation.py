#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impInvitation.o
import BigWorld
import gameglobal
import gametypes
import utils
from cdata import game_msg_def_data as GMDD

class ImpInvitation(object):

    def onInviteMate(self, result, inviteeURS):
        if result == gametypes.INVITE_SUC:
            self._updateInviteeInfo(inviteeURS)
            self.activedAccount = inviteeURS
            self.endTime = utils.getNow()
        else:
            self._showPopTips(result)

    def onAbandonInviteMate(self, isSuc, inviteeURS):
        pass

    def onDoInvitationReward(self, isSuc, inviteeURS, rewardId):
        if isSuc:
            self._updateRewardInfo(inviteeURS, rewardId)
        else:
            BigWorld.player().showGameMsg(GMDD.data.INVITE_FRIEND_GET_REWARD_FAILED, ())

    def onFetchAllInviteInfos(self, inviteeInfos):
        self._fetchInviteeInfos(inviteeInfos)

    def onFetchInvitationRewardInfos(self, rewardInfos):
        self._fetchRewardInfos(rewardInfos)

    def _fetchInviteeInfos(self, inviteeInfos):
        self.inviteeInfos = inviteeInfos
        for invitee in self.inviteeInfos:
            self.activedAccount = invitee
            self.endTime = self.inviteeInfos[invitee][0]
            break

    def _updateInviteeInfo(self, invitee):
        if not hasattr(self, 'inviteeInfos'):
            self.inviteeInfos = {}
        if not self.inviteeInfos.has_key(invitee):
            self.inviteeInfos[invitee] = {}
            self.inviteeInfos[invitee][0] = utils.getNow()
            self.inviteeInfos[invitee][1] = 0
            self.inviteeInfos[invitee][2] = True
        self.activedAccount = invitee

    def _fetchRewardInfos(self, rewardInfos):
        self.rewardInfos = rewardInfos

    def _updateRewardInfo(self, inviteeURS, rewardId):
        if not self.rewardInfos.has_key(inviteeURS):
            self.rewardInfos[inviteeURS] = {}
        for invitee in self.rewardInfos:
            if inviteeURS == invitee:
                self.rewardInfos[invitee][rewardId] = True

    def _showPopTips(self, result):
        p = BigWorld.player()
        if result == gametypes.INVITE_FAIL_BY_INVITED:
            p.showGameMsg(GMDD.data.INVITE_FAIL_BY_INVITED, ())
        elif result == gametypes.INVITE_FAIL_BY_EXPIRED:
            p.showGameMsg(GMDD.data.INVITE_FAIL_BY_EXPIRED, ())
        elif result == gametypes.INVITE_FAIL_BY_CONDITION:
            p.showGameMsg(GMDD.data.INVITE_FAIL_BY_CONDITION, ())
        elif result == gametypes.INVITE_FAIL_BY_ALIAS:
            p.showGameMsg(GMDD.data.INVITE_FAIL_BY_ALIAS, ())
        elif result == gametypes.INVITE_FAIL_BY_INVITING:
            p.showGameMsg(GMDD.data.INVITE_FAIL_BY_INVITING, ())
        elif result == gametypes.INVITE_FAIL_BY_SERVER_INNER:
            p.showGameMsg(GMDD.data.INVITE_FAIL_BY_SERVER_INNER, ())
        elif result == gametypes.INVITE_FAIL_BY_ALREADY_ACCOUNT:
            p.showGameMsg(GMDD.data.INVITE_FAIL_BY_ALREADY_ACCOUNT, ())
        elif result == gametypes.INVITE_FAIL_BY_BAN:
            p.showGameMsg(GMDD.data.INVITE_FAIL_BY_BAN, ())
        elif result == gametypes.INVITE_FAIL_BY_WHITE_LIST:
            p.showGameMsg(GMDD.data.INVITE_FAIL_BY_WHITE_LIST, ())
        elif result == gametypes.INVITE_FAIL_BY_INVITER_ACCOUNT:
            p.showGameMsg(GMDD.data.INVITE_FAIL_BY_INVITER_ACCOUNT, ())
        elif result == gametypes.INVITE_FAIL_BY_INVALID_URS:
            p.showGameMsg(GMDD.data.INVITE_FAIL_BY_INVALID_URS, ())
