#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impFriendRecall.o
import BigWorld
import gamelog
import gametypes
import gameglobal
import BigWorld
from cdata import game_msg_def_data as GMDD

class ImpFriendRecall(object):

    def onGetFriendsRecallData(self, ret, friendsRecallData):
        gamelog.debug('@zmm onGetFriendsRecallData', ret, friendsRecallData)
        if ret == gametypes.GET_FRIENDS_RECALL_DATA_FAIL_BY_NOT_IN_VALID_TIME:
            self.showGameMsg(GMDD.data.FRIEND_RECALL_NOT_IN_VALID_TIME, ())
        elif ret == gametypes.GET_FRIENDS_RECALL_DATA_SUC:
            p = BigWorld.player()
            for gbId, recallData in friendsRecallData.iteritems():
                fVal = p.friend.get(gbId, None)
                if not fVal:
                    continue
                fVal.recallState = recallData.get('recallState', 0)
                fVal.recallInfo = recallData.get('recallInfo', {})

            return

    def onSyncFriendRecallActivity(self):
        gameglobal.rds.ui.summonFriendBGV2.pushFriendRecallMessage()

    def onSendFriendRecallInfo(self, gbId, recallInfo):
        gamelog.info('@zmm onSendFriendRecallInfo', gbId, recallInfo)
        p = BigWorld.player()
        fVal = p.getFValByGbId(gbId)
        if not fVal:
            return
        fVal.recallInfo = recallInfo
        gameglobal.rds.ui.summonFriendBackV2.refreshInfo()

    def onSendFriendRecallStaticsInfo(self, friendRecallStatics):
        gamelog.info('@zmm onSendFriendRecallStaticsInfo', friendRecallStatics)
        self.friendRecallStatics = friendRecallStatics
        gameglobal.rds.ui.summonFriendBackV2.refreshInfo()
        gameglobal.rds.ui.summonFriendBGV2.updateRedPotBtns()

    def onsendRecallRequest(self, gbId, ret):
        gamelog.info('@zmm onsendRecallRequest', gbId)
        if ret == gametypes.SEND_RECALL_REQUEST_CHECK_FAIL_BY_NOT_IN_VALID_TIME:
            self.showGameMsg(GMDD.data.FRIEND_RECALL_NOT_IN_VALID_TIME, ())
        elif ret == gametypes.SEND_RECALL_REQUEST_CHECK_FAIL_BY_NOT_IN_VALID_STATE:
            self.showGameMsg(GMDD.data.FRIEND_RECALL_NOT_IN_VALID_STATE, ())
        elif ret == gametypes.SEND_RECALL_REQUEST_CHECK_SUC:
            gameglobal.rds.ui.summonFriendLetter.show(gbId)
            return

    def onSendFriendRecallInvitationSucc(self, gbId):
        if gbId:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.SEND_INVITATION_MSG_SUCC, ())

    def onSendFriendRecallInvitationFail(self, gbId):
        if gbId:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.SEND_INVITATION_MSG_FAIL, ())

    def onReceiveFriendRecallReward(self, ret, friendRecallStatics):
        gamelog.info('@zmm onReceiveFlowbackTargetReward', ret, friendRecallStatics)
        if ret == gametypes.FRIEND_RECALL_REWARD_REC_SUC:
            self.showGameMsg(GMDD.data.RECEIVE_FRIEND_RECALL_REWARD_SUC, ())
            self.friendRecallStatics = friendRecallStatics
            gameglobal.rds.ui.summonFriendBackV2.refreshInfo()
            gameglobal.rds.ui.summonFriendBGV2.updateRedPotBtns()
        elif ret == gametypes.FRIEND_RECALL_REWARD_REC_FAIL_BY_INV_LOCK:
            self.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
        elif ret == gametypes.FRIEND_RECALL_REWARD_REC_FAIL_BY_INV_FULL:
            self.showGameMsg(GMDD.data.ITEM_GET_BAG_FULL, ())
        elif ret == gametypes.FRIEND_RECALL_REWARD_REC_FAIL_BY_NOT_IN_VALID_TIME:
            self.showGameMsg(GMDD.data.FRIEND_RECALL_NOT_IN_VALID_TIME, ())
        else:
            self.showGameMsg(GMDD.data.RECEIVE_FRIEND_RECALL_REWARD_FAIL, ())
