#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonFriendInviteRecomme.o
from gamestrings import gameStrings
import BigWorld
import const
import events
import ui
import gametypes
from guis import uiUtils
from guis.asObject import ASUtils
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class SummonFriendInviteRecomme(object):

    def __init__(self, proxy):
        super(SummonFriendInviteRecomme, self).__init__()
        self.parentProxy = proxy

    def getWidget(self):
        return self.parentProxy.widget

    def hideWidget(self):
        pass

    def showWidget(self):
        widget = self.getWidget()
        if not widget:
            return
        self.parentProxy.updateTabBtnState()

    def refreshWidget(self):
        widget = self.getWidget()
        if not widget:
            return
        recommeMc = widget.invitePanel.recommeMc
        recommeMc.tab2_1.confirmBind.addEventListener(events.MOUSE_CLICK, self.onSendConfirmBind, False, 0, True)
        recommeMc.tab2_1.addFriend.addEventListener(events.MOUSE_CLICK, self.onAddFriend, False, 0, True)
        self.refreshMyReferrer()

    def refreshMyReferrer(self):
        widget = self.getWidget()
        if not widget:
            return
        elif not widget.invitePanel:
            return
        elif not widget.invitePanel.recommeMc:
            return
        else:
            recommeMc = widget.invitePanel.recommeMc
            data = self.getMyReferrerData()
            self.setInvited(data['invited'])
            recommeMc.tab2_1.nameText.visible = data['showContent']
            recommeMc.tab2_1.onLine.visible = data['showContent']
            recommeMc.tab2_1.lvAndSchool.visible = data['showContent']
            recommeMc.tab2_1.headIcon.visible = data['showContent']
            recommeMc.tab2_1.confirmBind.visible = data['showContent']
            recommeMc.tab2_1.addFriend.visible = data['showContent']
            friendInfo = data.get('friendInfo', None)
            if friendInfo:
                recommeMc.tab2_1.headIcon.tag = friendInfo['fid']
                recommeMc.tab2_1.headIcon.icon.fitSize = True
                recommeMc.tab2_1.headIcon.icon.loadImage(friendInfo['photo'])
                recommeMc.tab2_1.headIcon.status.gotoAndStop(friendInfo['stateName2'])
                if friendInfo['state'] == 0:
                    ASUtils.setMcEffect(recommeMc.tab2_1.headIcon, 'gray')
                else:
                    ASUtils.setMcEffect(recommeMc.tab2_1.headIcon)
                recommeMc.tab2_1.nameText.htmlText = friendInfo['name']
                recommeMc.tab2_1.onLine.htmlText = friendInfo['stateName']
                recommeMc.tab2_1.lvAndSchool.htmlText = friendInfo['school'] + '  ' + friendInfo['Lv']
            else:
                recommeMc.tab2_1.nameText.visible = False
                recommeMc.tab2_1.onLine.visible = False
                recommeMc.tab2_1.lvAndSchool.visible = False
                recommeMc.tab2_1.headIcon.visible = False
            recommeMc.tab2_1.confirmBind.enabled = not data['hasBinded']
            recommeMc.tab2_1.addFriend.enabled = data['addFriend']
            recommeMc.tab2_1.bindhint.htmlText = data['friendInfoHint']
            if not friendInfo:
                recommeMc.tab2_1.confirmBind.enabled = False
                recommeMc.tab2_1.addFriend.enabled = False
            return

    def setInvited(self, hadInvited):
        widget = self.getWidget()
        if not widget:
            return
        recommeMc = widget.invitePanel.recommeMc
        recommeMc.tab2_2.visible = hadInvited
        recommeMc.tab2_1.visible = not hadInvited

    def getMyReferrerData(self):
        p = BigWorld.player()
        hasOtherInvited = False
        data = {}
        if BigWorld.player().friendInviterGbId:
            data['hasBinded'] = True
        else:
            data['hasBinded'] = False
        inviteId = 0
        hasDeleted = False
        if BigWorld.player().friendInviterGbId:
            inviteId = p.friendInviterGbId
            if p.friendInviteInfo.get(inviteId, {}).get('status', gametypes.FRIEND_INVITE_STATUS_ROLE_DROP) == gametypes.FRIEND_INVITE_STATUS_ROLE_DROP:
                hasDeleted = True
                inviteId = 0
        else:
            for fid in p.friendInviteInfo:
                if p.friendInviteInfo[fid]['status'] == gametypes.FRIEND_INVITE_STATUS_PRE_INVITER:
                    inviteId = fid
                    break
                if p.friendInviteInfo[fid]['status'] == gametypes.FRIEND_INVITE_STATUS_ROLE_DROP:
                    if fid not in p.friendInvitees:
                        inviteId = 0
                        hasDeleted = True

        if inviteId:
            data['friendInfo'] = self.parentProxy.friendProxy.getFriendInfo(inviteId)
            if BigWorld.player().friend.get(inviteId):
                data['addFriend'] = False
            else:
                data['addFriend'] = True
        else:
            data['addFriend'] = True
        if not data['hasBinded']:
            if inviteId and not hasDeleted:
                msg = uiUtils.getTextFromGMD(GMDD.data.BIND_HINT, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_138)
                msg = msg % data['friendInfo']['name']
                data['friendInfoHint'] = msg
            else:
                msg = uiUtils.getTextFromGMD(GMDD.data.NOT_INVITE_HINT, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_142)
                data['friendInfoHint'] = msg
        elif not hasDeleted:
            msg = uiUtils.getTextFromGMD(GMDD.data.BIND_OK_HINT, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_146)
            msg = msg % data['friendInfo']['name']
            data['friendInfoHint'] = msg
        data['showContent'] = True
        if BigWorld.player().lv > SCD.data.get('friendInviteeLv') and not BigWorld.player().friendInviterGbId:
            data['hasBinded'] = True
            msg = uiUtils.getTextFromGMD(GMDD.data.BIND_FAILED_HINT_LV, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_152)
            data['friendInfoHint'] = msg
            data['showContent'] = False
        if hasDeleted == True:
            msg = uiUtils.getTextFromGMD(GMDD.data.INVITER_FRIEND_DELETE, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_156)
            data['friendInfoHint'] = msg
            data['showContent'] = False
        data['invited'] = hasOtherInvited
        return data

    def onSendConfirmBind(self, *args):
        p = BigWorld.player()
        if not p.friendInviterGbId:
            inviteId = 0
            for fid in p.friendInviteInfo:
                if p.friendInviteInfo[fid].get('status') == gametypes.FRIEND_INVITE_STATUS_PRE_INVITER:
                    inviteId = fid
                    break

            if inviteId:
                BigWorld.player().base.invitedFriendByGbId(inviteId)
            else:
                return

    @ui.callFilter(1, True)
    def onAddFriend(self, *args):
        p = BigWorld.player()
        inviteId = 0
        if p.friendInviterGbId:
            inviteId = p.friendInviterGbId
        else:
            for fid in p.friendInviteInfo:
                if p.friendInviteInfo[fid].get('status') == gametypes.FRIEND_INVITE_STATUS_PRE_INVITER:
                    inviteId = fid
                    break

        if inviteId:
            name = p.friendInviteInfo[inviteId].get('playerName', '')
            p.base.addContact(name, gametypes.FRIEND_GROUP_FRIEND, const.FRIEND_SRC_SUMMON)
