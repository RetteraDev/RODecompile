#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impFriendInvitation.o
import BigWorld
import gameglobal
import gametypes
import gamelog
from guis import uiConst
from cdata import game_msg_def_data as GMDD

class ImpFriendInvitation(object):

    def onInvitedFriendByVerifyCode(self, retType):
        gamelog.info('@szh onInvitedFriendByVerifyCode', retType)
        if retType == gametypes.FRIEND_INVITE_SUC:
            BigWorld.player().showGameMsg(GMDD.data.FRIEND_INVITE_BIND_SUCC, ())
        else:
            msg = {gametypes.FRIEND_INVITE_FAIL_BY_INVITED: GMDD.data.FRIEND_INVITE_ERROR_HAS_INVITED,
             gametypes.FRIEND_INVITE_FAIL_BY_SERVER_INNER: GMDD.data.FRIEND_INVITE_ERROR_SYS_ERROR,
             gametypes.FRIEND_INVITE_FAIL_BY_GBID_INVALID: GMDD.data.FRIEND_INVITE_ERROR_WRONG_GBID,
             gametypes.FRIEND_INVITE_FAIL_BY_LV: GMDD.data.FRIEND_INVITE_ERROR_WRONG_LV,
             gametypes.FRIEND_INVITE_FAIL_BY_INVALID_VERIFYCODE: GMDD.data.FRIEND_INVITE_ERROR_WRONG_CODE,
             gametypes.FRIEND_INVITE_FALY_BY_DIFF_SERVERID: GMDD.data.FRIEND_INVITE_ERROR_WRONG_SERVER,
             gametypes.FRIEND_INVITE_FALY_BY_UNMATCH_VERIFYCODE: GMDD.data.FRIEND_INVITE_ERROR_UNMATCH_CODE,
             gametypes.FRIEND_INVITE_FAIL_BY_HAS_INVITE: GMDD.data.FRIEND_INVITE_ERROR_HAS_INVITE_OTHER,
             gametypes.FRIEND_INVITE_FAIL_BY_GS: GMDD.data.FRIEND_INVITE_ERROR_HAS_INVITE_IN_GS}
            if msg.has_key(retType):
                BigWorld.player().showGameMsg(msg[retType], ())
            else:
                BigWorld.player().showGameMsg(GMDD.data.FRIEND_INVITE_ERROR_SYS_ERROR, ())

    def onDoFriendInvitationReward(self, isSuc, inviteeGbId, rewardId):
        gamelog.info('@szh onDoFriendInvitationReward', isSuc, inviteeGbId, rewardId)
        if isSuc:
            fid = gameglobal.rds.ui.summonFriend.selectFid
            gameglobal.rds.ui.summonFriend.refreshSelectFriend(fid)
        else:
            BigWorld.player().showGameMsg(GMDD.data.FRIEND_INVITE_GETREWARD_FAIL, ())

    def sendFlowbackedFriendSet(self, flowbackedFriendSet):
        summonedFriendList = list(flowbackedFriendSet)
        gameglobal.rds.ui.summonFriendNew.setSummonedFriendList(summonedFriendList)
        gameglobal.rds.ui.summonFriendBackV2.setSummonedFriendList(summonedFriendList)

    def onGenFriendInviteVerifyCode(self, verifyCode):
        gamelog.info('@szh onGenFriendInviteVerifyCode', verifyCode)
        self.friendInviteVerifyCode = verifyCode
        gameglobal.rds.ui.summonFriend.refreshIwantSummon()
        gameglobal.rds.ui.summonFriendNew.refreshInvite()
        gameglobal.rds.ui.summonFriendInviteV2.refreshInvite()

    def set_friendInviteInfo(self, old):
        gameglobal.rds.ui.summonFriend.refreshWidget()
        gameglobal.rds.ui.summonFriendNew.refreshWidget()
        gameglobal.rds.ui.summonFriendBGV2.refreshInfo()
        self.updateRewardHallInfo(uiConst.REWARD_ZHIYOU)

    def onFriendInvitationSummary(self, data):
        self.friendInvitationSummary = {}
        for rid, num, rewarded in data:
            self.friendInvitationSummary[rid] = [num, rewarded]

        gameglobal.rds.ui.summonFriend.refreshFriendInviteActivity()
        gameglobal.rds.ui.summonFriend.pushSummonFriendRewardBonus()
        gameglobal.rds.ui.summonFriendNew.refreshWidget()
        gameglobal.rds.ui.summonFriendBGV2.refreshInfo()

    def onFriendInvitationSummaryNotify(self):
        gameglobal.rds.ui.summonFriend.pushSummonFriendActivity()
        gameglobal.rds.ui.summonFriendNew.refreshWidget()
        gameglobal.rds.ui.summonFriendBGV2.refreshInfo()
