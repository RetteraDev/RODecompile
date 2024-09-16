#Embedded file name: I:/bag/tmp/tw2/res/entities\common/commInvitation.o
import BigWorld
import gametypes
from cdata import invite_precondition_data as IPCD
from cdata import invite_data as IMD
from data import friend_invitation_reward_data as FIRD
if BigWorld.component in 'cell':
    import gameconfig
elif BigWorld.component in 'client':
    import gameglobal

def inviteMateCheck(owner, inviteId, bMsg = True):
    if BigWorld.component in 'cell':
        channel = owner.client
    elif BigWorld.component in 'client':
        channel = owner
    if not IMD.data.has_key(inviteId):
        return False
    imd = IMD.data[inviteId]
    conditionIds = imd['preConditionIds']
    for conditionId in conditionIds:
        if not IPCD.data.has_key(conditionId):
            continue
        ipcd = IPCD.data[conditionId]
        conType = ipcd['conditionType']
        if conType == gametypes.INVITE_CONDITION_LV_LARGER:
            if BigWorld.component in 'cell':
                lv = gameconfig.inviterLevel()
            elif BigWorld.component in 'client':
                lv = gameglobal.rds.configData.get('inviterLevel')
            if owner.lv < lv:
                if bMsg and ipcd.has_key('failMsgId'):
                    channel.showGameMsg(ipcd['failMsgId'], (lv,))
                return False
        elif conType == gametypes.INVITE_CONDITION_STATS:
            statId = ipcd['value']
            if statId not in owner.invitePreConditions:
                if bMsg and ipcd.has_key('failMsgId'):
                    channel.showGameMsg(ipcd['failMsgId'], ())
                return False

    return True


def getInvalidInviteCondition(owner, inviteId):
    if not IMD.data.has_key(inviteId):
        return []
    retIds = []
    imd = IMD.data[inviteId]
    conditionIds = imd['preConditionIds']
    for conditionId in conditionIds:
        if not IPCD.data.has_key(conditionId):
            continue
        ipcd = IPCD.data[conditionId]
        conType = ipcd['conditionType']
        if conType == gametypes.INVITE_CONDITION_LV_LARGER:
            if owner.lv < ipcd['value']:
                retIds.append(conditionId)
        elif conType == gametypes.INVITE_CONDITION_STATS:
            statId = ipcd['value']
            if statId not in owner.invitePreConditions:
                retIds.append(conditionId)

    return retIds


def gainFriendInviteRewardCheck(owner, inviteeGbId, rewardId):
    if not FIRD.data.has_key(rewardId):
        return False
    if not owner.friendInviteInfo.has_key(inviteeGbId):
        return False
    if owner.friendInviteInfo[inviteeGbId]['status'] != gametypes.FRIEND_INVITE_STATUS_BUILD:
        return False
    if inviteeGbId not in owner.friendInvitees:
        return False
    if owner.friendInviteRewards.has_key(inviteeGbId) and owner.friendInviteRewards[inviteeGbId].has_key(rewardId) and owner.friendInviteRewards[inviteeGbId][rewardId]:
        return False
    fird = FIRD.data[rewardId]
    if fird.get('stats', 0):
        if not owner.friendInviteRewards.has_key(inviteeGbId):
            return False
        if not owner.friendInviteRewards[inviteeGbId].has_key(rewardId):
            return False
    if fird.has_key('lv'):
        lv = fird['lv']
        if owner.friendInviteInfo[inviteeGbId].get('lv', 0) < lv:
            return False
    return True


def getCurLvRewardPointList(owner, lv, gbId):
    rewardList = []
    for rId, val in FIRD.data.iteritems():
        if owner.inviteFriendRewardRecord.has_key(gbId) and owner.inviteFriendRewardRecord[gbId].has_key(rId):
            continue
        if val.get('lv', None) is None:
            continue
        if val.get('stats') == 1:
            continue
        if lv >= val['lv']:
            rewardList.append(rId)

    return rewardList
