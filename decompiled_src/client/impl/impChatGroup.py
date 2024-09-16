#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impChatGroup.o
import zlib
import cPickle
import BigWorld
import gameglobal
import gamelog
import const
import utils
import gametypes
import os
import json
from guis import uiUtils
from gamestrings import gameStrings
from data import personal_zone_touch_data as PZTD
from data import personal_zone_gift_data as PZGD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class ImpChatGroup(object):

    def updateChatGroupData(self, ownerGbId, op, data):
        """
        \xe6\x9b\xb4\xe6\x96\xb0\xe7\xbe\xa4\xe8\x81\x8a\xe6\x95\xb0\xe6\x8d\xae
        :param ownerGbId: \xe7\xbe\xa4\xe8\x81\x8a\xe7\xae\xa1\xe7\x90\x86\xe5\x91\x98gbId
        :param op: \xe7\xb1\xbb\xe5\x9e\x8b CHAT_GROUP_OP_CREATE\xef\xbc\x8cCHAT_GROUP_OP_INVITE\xef\xbc\x8cCHAT_GROUP_OP_BE_INVITE
        :param data: \xe7\xbe\xa4\xe8\x81\x8a\xe6\x95\xb0\xe6\x8d\xae {'name': 'firstChatGroup', 'type': 9, 'managerGbId': 6492250675399884801L, 'publicAnnouncement': '',
        'members': {gbId1:(nickName, level, photo, msgAcceptOp, box, borderId, school, sex), ..., gbIdN:(nickName, level, photo, msgAcceptOp, box, borderId, school, sex), }}
        :return:
        """
        p = BigWorld.player()
        groupData = cPickle.loads(zlib.decompress(data))
        gamelog.debug('yedawang### updateChatGroupData', ownerGbId, op, groupData)
        self.updateGroupData(groupData)
        gamelog.debug('@zmm updateChatGroupData', ownerGbId, op, groupData)
        if op == gametypes.CHAT_GROUP_OP_CREATE:
            print 'zmm: please CHAT_GROUP_OP_CREATE added'
            if ownerGbId == self.gbId:
                gameglobal.rds.ui.groupChat.addGroupChatItem(cPickle.loads(zlib.decompress(data)))
            else:
                inviterGbId = groupData.get('managerGbId', 0)
                nuid = groupData.get('nuId', 0)
                if inviterGbId and nuid:
                    inviterName = self.getGroupMemberName(nuid, inviterGbId)
                    groupName = groupData.get('name', '')
                    self.showGameMsg(GMDD.data.GROUP_CHAT_BE_INVITE, (inviterName, groupName))
            gameglobal.rds.ui.groupChatMembers.hide()
            p._refreshFriendList()
        elif op == gametypes.CHAT_GROUP_OP_INVITE:
            gameglobal.rds.ui.groupChat.addGroupChatItem(cPickle.loads(zlib.decompress(data)))
            print 'zmm: please CHAT_GROUP_OP_INVITE added'
        elif op == gametypes.CHAT_GROUP_OP_BE_INVITE:
            inviterGbId = groupData.get('managerGbId', 0)
            nuid = groupData.get('nuId', 0)
            if inviterGbId and nuid:
                inviterName = self.getGroupMemberName(nuid, inviterGbId)
                groupName = groupData.get('name', '')
                self.showGameMsg(GMDD.data.GROUP_CHAT_BE_INVITE, (inviterName, groupName))
            print 'zmm: please CHAT_GROUP_OP_BE_INVITE added'
        elif op == gametypes.CHAT_GROUP_OP_LOGIN:
            print 'zmm: please CHAT_GROUP_OP_BE_LOGIN added'

    def updateGroupData(self, groupData):
        nuId = groupData.get('nuId')
        self.groupChatData[nuId] = groupData
        self._refreshFriendList()

    def onRefreshChatGroupOnlineData(self, nuid, mGbId, data):
        """
        \xe7\xbe\xa4\xe6\x88\x90\xe5\x91\x98\xe6\x9f\x90\xe4\xb8\xaa\xe7\x8e\xa9\xe5\xae\xb6\xe4\xb8\x8a\xe7\xba\xbf\xe5\x90\x8e\xef\xbc\x8c\xe4\xbc\x9a\xe9\x80\x9a\xe8\xbf\x87\xe6\xad\xa4\xe6\x8e\xa5\xe5\x8f\xa3\xe9\x80\x9a\xe7\x9f\xa5\xe5\x85\xb6\xe4\xbb\x96\xe7\xbe\xa4\xe6\x88\x90\xe5\x91\x98\xe6\x9b\xb4\xe6\x96\xb0\xe8\xaf\xa5\xe6\x88\x90\xe5\x91\x98\xe7\x9a\x84\xe5\x9c\xa8\xe7\xba\xbf\xe6\x95\xb0\xe6\x8d\xae
        :param nuid: \xe7\xbe\xa4id
        :param mGbId: mGbId\xe4\xb8\xba\xe6\x96\xb0\xe4\xb8\x8a\xe7\xba\xbf\xe7\x9a\x84\xe7\xbe\xa4\xe6\x88\x90\xe5\x91\x98
        :param data: data=(nickName, level, photo, msgAcceptOp, box, borderId, school, sex)
        nickName, level, photo, msgAcceptOp, box, borderId, school, sex = data \xe8\xbf\x99\xe6\xa0\xb7\xe5\x8f\x96\xe6\x95\xb0\xe6\x8d\xae\xe5\x8d\xb3\xe5\x8f\xaf
        :return:
        """
        gamelog.debug('@zmm onRefreshChatGroupOnlineData', nuid, data)
        if nuid in self.groupChatData:
            members = self.groupChatData[nuid]['members']
            if mGbId in members:
                self.groupChatData[nuid]['members'][mGbId] = data
        if gameglobal.rds.ui.groupChatRoom.isOpened(nuid):
            gameglobal.rds.ui.groupChatRoom.updateGroupChatRoomMembers(nuid)
        elif gameglobal.rds.ui.groupChat.checkCurrentGroupChated(nuid):
            gameglobal.rds.ui.groupChat.updateGroupChatInfo(nuid)

    def onCreateChatGroupFailed(self, ret, data):
        """
        \xe5\xbb\xba\xe7\xbe\xa4\xe5\xa4\xb1\xe8\xb4\xa5
        :param ret: CHAT_GROUP_INVITE_FAILED
        :param data:
        :return:
        """
        gamelog.debug('@zmm onCreateChatGroupFailed', ret, data)

    def onInviteChatGroup(self, nuid, ret, data):
        """
        \xe9\x82\x80\xe8\xaf\xb7\xe5\x8a\xa0\xe5\x85\xa5\xe7\xbe\xa4\xe8\x81\x8a, \xe9\x82\x80\xe8\xaf\xb7\xe8\x80\x85\xe6\x94\xb6\xe5\x88\xb0\xe7\x9a\x84\xe9\x82\x80\xe8\xaf\xb7\xe7\xbb\x93\xe6\x9e\x9c\xef\xbc\x9aret=CHAT_GROUP_INVITE_FAILED\xef\xbc\x9a\xe9\x82\x80\xe8\xaf\xb7\xe5\xa4\xb1\xe8\xb4\xa5 \xef\xbc\x8cret=CHAT_GROUP_INVITE_SUCCESS\xef\xbc\x9a\xe9\x82\x80\xe8\xaf\xb7\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c
        :param nuid:\xe7\xbe\xa4\xe8\x81\x8aid
        :param ret: \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc CHAT_GROUP_INVITE_SUCCESS CHAT_GROUP_INVITE_FAILED
        :param data: \xe9\x82\x80\xe8\xaf\xb7\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8cdata={}\xef\xbc\x8c \xe9\x82\x80\xe8\xaf\xb7\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8cdata={beInviteGbId1:(nickName, level, photo, msgAcceptOp, box, borderId, school, sex), beInviteGbId2:(nickName, level, photo, msgAcceptOp, box, borderId, school, sex),}
        :return:
        """
        gamelog.debug('@zmm onInviteChatGroup', nuid, ret, data)
        if ret == gametypes.CHAT_GROUP_INVITE_FAILED:
            self.showGameMsg(GMDD.data.GROUP_CHAT_INVITE_FAIL, ())
        elif ret == gametypes.CHAT_GROUP_INVITE_SUCCESS:
            self.showGameMsg(GMDD.data.GROUP_CHAT_INVITE_SUCCESS, ())
            if nuid in self.groupChatData:
                self.groupChatData[nuid]['members'].update(data)
            gameglobal.rds.ui.groupChatMembers.hide()
            gameglobal.rds.ui.groupChatSetup.hide()
            mGbId = self.groupChatData.get(nuid, {}).get('managerGbId', 0)
            if gameglobal.rds.ui.groupChatRoom.isOpened(nuid):
                gameglobal.rds.ui.groupChatRoom.updateGroupChatRoomMembers(nuid)
                inviterName = self.getGroupMemberName(nuid, mGbId)
                beInviteNames = self.getBeInviteNames(data)
                infoTips = gameStrings.GROUP_CHAT_IVBITE_MEMBERS % (inviterName, beInviteNames)
                gameglobal.rds.ui.groupChatRoom.addGroupMsgByPlayer(nuid, infoTips, True)
            elif gameglobal.rds.ui.groupChat.checkCurrentGroupChated(nuid):
                gameglobal.rds.ui.groupChat.updateGroupChatInfo(nuid)
                inviterName = self.getGroupMemberName(nuid, mGbId)
                beInviteNames = self.getBeInviteNames(data)
                infoTips = gameStrings.GROUP_CHAT_IVBITE_MEMBERS % (inviterName, beInviteNames)
                gameglobal.rds.ui.groupChat.addMsgByGroup(nuid, infoTips, True)

    def getBeInviteNames(self, inviters):
        beInviteNames = ''
        for gbId, member in inviters.items():
            if not beInviteNames:
                beInviteNames = member[0]
            else:
                beInviteNames = beInviteNames + ',' + member[0]

        return beInviteNames

    def onInviteNewChatGroupMembers(self, nuid, inviterGbId, inviters):
        """
        \xe6\x9c\x89\xe6\x96\xb0\xe7\x9a\x84\xe7\x8e\xa9\xe5\xae\xb6\xe8\xa2\xab\xe9\x82\x80\xe8\xaf\xb7\xe5\x8a\xa0\xe5\x85\xa5\xe7\xbe\xa4\xe8\x81\x8a
        :param nuid: \xe7\xbe\xa4\xe8\x81\x8aid
        :param inviterGbId: \xe9\x82\x80\xe8\xaf\xb7\xe8\x80\x85gbId
        :param inviters: \xe8\xa2\xab\xe9\x82\x80\xe8\xaf\xb7\xe8\x80\x85\xe6\x95\xb0\xe6\x8d\xae = {beInviteGbId1:(nickName, level, photo, msgAcceptOp, box, borderId, school, sex), beInviteGbId2:(nickName, level, photo, msgAcceptOp, box, borderId, school, sex),}
        :return:
        """
        gamelog.debug('@zmm onInviteNewChatGroupMembers', nuid, inviterGbId, inviters)
        if nuid in self.groupChatData:
            self.groupChatData[nuid]['members'].update(inviters)
        inviterName = self.getGroupMemberName(nuid, inviterGbId)
        groupName = self.groupChatData.get(nuid, {}).get('name', '')
        for gbId, member in inviters.items():
            beInviteNames = member[0]
            self.showGameMsg(GMDD.data.GROUP_CHAT_INVITE_NEW_PEOPLE, (inviterName, beInviteNames, groupName))

        if gameglobal.rds.ui.groupChatRoom.isOpened(nuid):
            gameglobal.rds.ui.groupChatRoom.updateGroupChatRoomMembers(nuid)
            beInviteNames = self.getBeInviteNames(inviters)
            infoTips = gameStrings.GROUP_CHAT_IVBITE_MEMBERS % (inviterName, beInviteNames)
            gameglobal.rds.ui.groupChatRoom.addGroupMsgByPlayer(nuid, infoTips, True)
        elif gameglobal.rds.ui.groupChat.checkCurrentGroupChated(nuid):
            gameglobal.rds.ui.groupChat.updateGroupChatInfo(nuid)
            beInviteNames = self.getBeInviteNames(inviters)
            infoTips = gameStrings.GROUP_CHAT_IVBITE_MEMBERS % (inviterName, beInviteNames)
            gameglobal.rds.ui.groupChat.addMsgByGroup(nuid, infoTips, True)

    def onCommitChatGroupMsg(self, nuid, senderGbId, msgId, msgContent, time):
        """
        \xe5\x8f\x91\xe9\x80\x81\xe7\xbe\xa4\xe8\x81\x8a\xe6\xb6\x88\xe6\x81\xaf \xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param nuid: \xe7\xbe\xa4\xe8\x81\x8aid
        :param senderGbId: \xe5\x8f\x91\xe9\x80\x81\xe6\xb6\x88\xe6\x81\xaf\xe7\x9a\x84\xe7\x8e\xa9\xe5\xae\xb6gbId
        :param msgId: \xe6\xb6\x88\xe6\x81\xaf\xe7\xbc\x96\xe5\x8f\xb7
        :param msgContent: \xe6\xb6\x88\xe6\x81\xaf\xe5\x86\x85\xe5\xae\xb9
        :param time: \xe5\x8f\x91\xe9\x80\x81\xe6\xb6\x88\xe6\x81\xaf\xe6\x97\xb6\xe9\x97\xb4
        :return:
        """
        gamelog.debug('@zmm onCommitChatGroupMsg', nuid, senderGbId, msgId, msgContent, time)
        p = BigWorld.player()
        m = self._createGroupChatMsg(nuid, senderGbId, msgId, msgContent, time)
        if gameglobal.rds.ui.groupChatRoom.isOpened(nuid):
            gameglobal.rds.ui.groupChatRoom.addGroupMsgByPlayer(nuid, m)
        elif gameglobal.rds.ui.groupChat.checkCurrentGroupChated(nuid):
            gameglobal.rds.ui.groupChat.addMsgByGroup(nuid, m)
        else:
            self._addGroupUnreadMsg(nuid, m)
            gameglobal.rds.ui.friend.minChatShine(nuid, True)
        playerName = self.getGroupMemberName(nuid, senderGbId)
        p.chatDB.saveGroupMsg(nuid, playerName, msgContent, m['isMe'], m['time'])

    def getGroupMemberName(self, nuId, gbId):
        p = BigWorld.player()
        members = p.groupChatData.get(nuId, {}).get('members', {})
        playerName = members.get(gbId, ('',))[0]
        return playerName

    def _createGroupChatMsg(self, nuId, senderGbId, msgId, msg, time):
        if not time:
            time = utils.getNow()
        p = BigWorld.player()
        return {'nuId': nuId,
         'senderGbId': senderGbId,
         'msgId': msgId,
         'time': time,
         'msg': msg,
         'isMe': senderGbId == p.gbId}

    def _addGroupUnreadMsg(self, groupNUID, msg):
        gamelog.debug('yedawang### _addGroupUnreadMsg', groupNUID, msg)
        p = BigWorld.player()
        if groupNUID in self.groupUnreadMsgs:
            self.groupUnreadMsgs[groupNUID].append(msg)
        else:
            self.groupUnreadMsgs[groupNUID] = []
            self.groupUnreadMsgs[groupNUID].append(msg)
        p._refreshFriendList()
        p._checkBlink()
        gameglobal.rds.ui.groupChat.updateItemMsgsCount(groupNUID, msg, True)
        gameglobal.rds.ui.groupChat.updateInGroupChatData(groupNUID, None)
        gameglobal.rds.ui.groupChat.refreshInfo()

    def handleGroupUnreadMsgs(self):
        if not self.groupUnreadMsgs:
            return
        checkHasNewMsg = False
        for nuId, msgs in self.groupUnreadMsgs.iteritems():
            if not msgs:
                continue
            if gameglobal.rds.ui.groupChat.checkChatedId(nuId):
                continue
            checkHasNewMsg = True
            groupInfo = self.groupChatData.get(nuId, {})
            gfxMsgs = self.getGroupUnreadMsgs(nuId)
            gameglobal.rds.ui.groupChat.addGroupChatItem(groupInfo, gfxMsgs, needSelect=False)
            self._refreshFriendList()

        return checkHasNewMsg

    def clearGroupUnreadMsg(self, groupNUID):
        if groupNUID in self.groupUnreadMsgs:
            self.groupUnreadMsgs[groupNUID] = []

    def fetchGroupChatHistory(self, nuId, offset = 0, limit = 0):
        if not limit:
            limit = const.CHAT_HISTORY_LIMIT
        p = BigWorld.player()
        p.chatDB.getGroupMsgs(nuId, offset, limit, lambda results, nuId = nuId, offset = offset, limit = limit: self._onGetGroupChatHistory(nuId, results[0], results[1], offset, limit))

    def _onGetGroupChatHistory(self, nuId, msgs, total, offset, limit):
        tMsgs = []
        for m in msgs:
            isMe, playerName, msg, createdTime = m
            tMsgs.append({'isMe': isMe,
             'name': playerName,
             'time': createdTime,
             'msg': msg})

        gameglobal.rds.ui.groupChatRoom.appendHistoryMsg(nuId, tMsgs, total, offset, limit)
        return tMsgs

    def onGetChatGroupMessages(self, nuid, messages):
        """
        \xe7\x8e\xa9\xe5\xae\xb6\xe7\x99\xbb\xe5\xbd\x95\xe5\x90\x8e\xe6\x8b\x89\xe5\x8f\x96\xe6\xaf\x8f\xe4\xb8\xaa\xe7\xbe\xa4\xe8\x81\x8a\xe7\x9a\x84\xe7\xa6\xbb\xe7\xba\xbf\xe8\x81\x8a\xe5\xa4\xa9\xe6\x95\xb0\xe6\x8d\xae
        :param nuid: \xe7\xbe\xa4\xe8\x81\x8aid
        :param messages: \xe7\xbe\xa4\xe8\x81\x8a\xe6\xb6\x88\xe6\x81\xaf
        :return:
        """
        gamelog.debug('@zmm onGetChatGroupMessages', nuid, messages)
        p = BigWorld.player()
        d = []
        for msgId, gbId, msg, createdTime in messages:
            isMe = gbId == self.gbId
            playerName = self.getGroupMemberName(nuid, gbId)
            d.append((isMe and 1 or 0,
             playerName,
             msg,
             createdTime))
            m = self._createGroupChatMsg(nuid, gbId, msgId, msg, createdTime)
            self._addGroupUnreadMsg(nuid, m)

        if not gameglobal.rds.ui.friend.inited and not self.friend:
            if gameglobal.rds.ui.friend.messagesBeforeInit != None:
                gameglobal.rds.ui.friend.messagesBeforeInit.append((self.saveGroupMsgs, (nuid, d)))
            return
        else:
            if hasattr(p, 'chatDB'):
                self.saveGroupMsgs(nuid, d)
            return

    def saveGroupMsgs(self, nuid, d):
        self.chatDB.saveGroupMsgs(nuid, d)

    def onQuitChatGroup(self, nuid, gbId):
        """
        \xe9\x80\x80\xe5\x87\xba\xe7\xbe\xa4\xe8\x81\x8a\xe8\xbf\x94\xe5\x9b\x9e
        :param nuid: \xe7\xbe\xa4\xe8\x81\x8aid
        :param gbId: \xe9\x80\x80\xe5\x87\xba\xe7\xbe\xa4\xe8\x81\x8a\xe7\x9a\x84\xe7\x8e\xa9\xe5\xae\xb6gbId
        :return:
        """
        gamelog.debug('@zmm onQuitChatGroup', nuid, gbId)
        if gbId == self.gbId:
            self.showGameMsg(GMDD.data.GROUP_CHAT_QUIT_SUCCESS, ())
            gameglobal.rds.ui.groupChat.deleteGroupData(nuid)
        else:
            quitMemberName = self.getGroupMemberName(nuid, gbId)
            infoTips = gameStrings.GROUP_CHAT_MEMBER_QUIT % (quitMemberName,)
            if gameglobal.rds.ui.groupChatRoom.isOpened(nuid):
                gameglobal.rds.ui.groupChatRoom.addGroupMsgByPlayer(nuid, infoTips, True)
            elif gameglobal.rds.ui.groupChat.checkCurrentGroupChated(nuid):
                gameglobal.rds.ui.groupChat.addMsgByGroup(nuid, infoTips, True)
        if nuid in self.groupChatData:
            groupInfo = self.groupChatData[nuid]
            if gbId in groupInfo.get('members'):
                groupInfo['members'].pop(gbId)
        if gameglobal.rds.ui.groupChatRoom.isOpened(nuid):
            gameglobal.rds.ui.groupChatRoom.updateGroupChatRoomMembers(nuid)
        elif gameglobal.rds.ui.groupChat.checkCurrentGroupChated(nuid):
            gameglobal.rds.ui.groupChat.updateGroupChatInfo(nuid)

    def onDisbandChatGroup(self, nuid, managerGbId):
        """
        \xe8\xa7\xa3\xe6\x95\xa3\xe7\xbe\xa4\xe8\x81\x8a
        :param nuid: \xe7\xbe\xa4\xe8\x81\x8aid
        :param managerGbId: \xe7\xae\xa1\xe7\x90\x86\xe5\x91\x98gbId
        :return:
        """
        gamelog.debug('@zmm onDisbandChatGroup', nuid, managerGbId)
        playerName = ''
        groupName = ''
        if nuid in self.groupChatData:
            groupInfo = self.groupChatData[nuid]
            groupName = groupInfo.get('name', '')
            playerName = self.getGroupMemberName(nuid, managerGbId)
        if managerGbId == self.gbId:
            self.showGameMsg(GMDD.data.GROUP_CHAT_DISBAND_SUCCESS, ())
        else:
            self.showGameMsg(GMDD.data.GROUP_CHAT_DISBAND_CHAT_GROUP, (playerName, groupName))
        if gameglobal.rds.ui.groupChatRoom.isOpened(nuid):
            gameglobal.rds.ui.groupChatRoom.hide()
        gameglobal.rds.ui.groupChat.deleteGroupData(nuid)
        p = BigWorld.player()
        p._refreshFriendList()

    def clearChatGroupData(self, nuid):
        """
        \xe6\xb8\x85\xe9\x99\xa4\xe7\xbe\xa4\xe6\x95\xb0\xe6\x8d\xae
        :param nuid: \xe7\xbe\xa4\xe8\x81\x8aid
        :return:
        """
        gamelog.debug('@zmm clearChatGroupData', nuid)
        if nuid in self.groupChatData:
            self.groupChatData.pop(nuid)
        if gameglobal.rds.ui.groupChatRoom.isOpened(nuid):
            gameglobal.rds.ui.groupChatRoom.hide()
        elif gameglobal.rds.ui.groupChat.checkCurrentGroupChated(nuid):
            gameglobal.rds.ui.groupChat.deleteGroupData(nuid)
        p = BigWorld.player()
        p._refreshFriendList()

    def onUpdateChatGroupNickName(self, nuid, mGbId, newName):
        """
        \xe4\xbf\xae\xe6\x94\xb9\xe7\xbe\xa4\xe8\x81\x8a\xe6\x98\xb5\xe7\xa7\xb0\xe8\xbf\x94\xe5\x9b\x9e
        :param nuid: \xe7\xbe\xa4\xe8\x81\x8aid
        :param mGbId: \xe4\xbf\xae\xe6\x94\xb9\xe6\x98\xb5\xe7\xa7\xb0\xe7\x9a\x84\xe7\x8e\xa9\xe5\xae\xb6gbId
        :param newName: \xe6\x96\xb0\xe6\x98\xb5\xe7\xa7\xb0
        :return:
        """
        gamelog.debug('@zmm onUpdateChatGroupNickName', nuid, mGbId, newName)

    def onUpdateChatGroupMsgAcceptOp(self, nuid, acceptOp):
        """
        \xe4\xbf\xae\xe6\x94\xb9\xe7\xbe\xa4\xe6\xb6\x88\xe6\x81\xaf\xe6\x8e\xa5\xe6\x94\xb6\xe5\xbc\x80\xe5\x85\xb3\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe5\x85\xb3\xe9\x97\xad CHAT_GROUP_AVOID_ACCEPT_OP_CLOSE\xef\xbc\x8c\xe6\xb6\x88\xe6\x81\xaf\xe9\x9a\x8f\xe6\x97\xb6\xe9\x80\x9a\xe7\x9f\xa5; CHAT_GROUP_AVOID_ACCEPT_OP_OPEN,\xe6\x8e\xa5\xe6\x94\xb6\xe6\xb6\x88\xe6\x81\xaf\xe4\xbd\x86\xe4\xb8\x8d\xe9\x80\x9a\xe7\x9f\xa5
        :param nuid:
        :param acceptOp:
        :return:
        """
        gamelog.debug('@zmm onUpdateChatGroupMsgAcceptOp', nuid, acceptOp)
        p = BigWorld.player()
        if nuid in self.groupChatData:
            members = self.groupChatData[nuid]['members']
            if p.gbId in members:
                self.groupChatData[nuid]['members'][p.gbId][3] = acceptOp
                gameglobal.rds.ui.groupChatSetup.changedAcceptOpSuccess(nuid)
                gameglobal.rds.ui.groupChat.onUpdateChatGroupMsgAcceptOp(nuid, acceptOp)
        p._refreshFriendList()

    def onUpdateChatGroupPublicAnnouncement(self, nuid, mGbId, publicAnnouncement):
        """
        \xe6\x9b\xb4\xe6\x96\xb0\xe7\xbe\xa4\xe8\x81\x8a\xe5\x85\xac\xe5\x91\x8a\xe5\x86\x85\xe5\xae\xb9
        :param nuid: \xe7\xbe\xa4\xe8\x81\x8aid
        :param mGbId: \xe7\xae\xa1\xe7\x90\x86\xe5\x91\x98gbId
        :param publicAnnouncement: \xe5\x85\xac\xe5\x91\x8a\xe5\x86\x85\xe5\xae\xb9
        :return:
        """
        gamelog.debug('@zmm onUpdateChatGroupPublicAnnouncement', nuid, mGbId, publicAnnouncement)
        if nuid in self.groupChatData:
            self.groupChatData[nuid]['publicAnnouncement'] = publicAnnouncement
        if self.gbId == mGbId:
            self.showGameMsg(GMDD.data.GROUP_CHAT_CHANGE_ANNOUNCEMENT_SUCCESS, ())
        else:
            self.showGameMsg(GMDD.data.GROUP_CHAT_CHANGE_ANNOUNCEMENT_CHANGED, (publicAnnouncement,))
        gameglobal.rds.ui.groupChatSetup.setAnnouncementSuccess(nuid, publicAnnouncement)

    def onUpdateChatGroupName(self, nuid, mGbId, newName):
        """
        \xe6\x9b\xb4\xe6\x96\xb0\xe7\xbe\xa4\xe5\x90\x8d\xe7\xa7\xb0
        :param nuid: \xe7\xbe\xa4\xe8\x81\x8aid
        :param mGbId: \xe7\xae\xa1\xe7\x90\x86\xe5\x91\x98gbId
        :param newName: \xe6\x96\xb0\xe7\x9a\x84\xe7\xbe\xa4\xe5\x90\x8d\xe7\xa7\xb0
        :return:
        """
        gamelog.debug('@zmm onUpdateChatGroupName', nuid, mGbId, newName)
        if nuid in self.groupChatData:
            self.groupChatData[nuid]['name'] = newName
        if self.gbId == mGbId:
            self.showGameMsg(GMDD.data.GROUP_CHAT_CHANGE_GROUP_NAME_SUCCESS, ())
        else:
            self.showGameMsg(GMDD.data.GROUP_CHAT_CHANGE_GROUP_NAME_CHANGED, (newName,))
        gameglobal.rds.ui.groupChatSetup.setGroupNameSuccess(nuid, newName)
        gameglobal.rds.ui.groupChat.updateGroupName(nuid, newName)
        p = BigWorld.player()
        p._refreshFriendList()

    def onSetRejectChatGroupInviteOp(self, opType):
        """
        \xe6\x8b\x92\xe7\xbb\x9d\xe7\xbe\xa4\xe9\x82\x80\xe8\xaf\xb7\xe5\xbc\x80\xe5\x85\xb3\xe8\xae\xbe\xe7\xbd\xae\xef\xbc\x8c
        :param opType: \xe5\x8f\xaf\xe4\xbb\xa5\xe9\x82\x80\xe8\xaf\xb7\xef\xbc\x9a\xe9\xbb\x98\xe8\xae\xa4CHAT_GROUP_INVITE_REJECT_CLOSE\xef\xbc\x8c \xe4\xb8\x8d\xe5\x8f\xaf\xe4\xbb\xa5\xe8\xa2\xab\xe9\x82\x80\xe8\xaf\xb7\xef\xbc\x9aCHAT_GROUP_INVITE_REJECT_OPEN=1
        :return:
        """
        gamelog.debug('@zmm onSetRejectChatGroupInviteOp', opType)
        self.rejectChatGroupInviteOp = opType

    def onTransferChatGroupManager(self, nuid, mGbId, toGbId):
        """
        \xe7\xbe\xa4\xe8\x81\x8a\xe7\xae\xa1\xe7\x90\x86\xe5\x91\x98\xe8\xbd\xac\xe7\xa7\xbb\xe8\xbf\x94\xe5\x9b\x9e
        :param nuid: \xe7\xbe\xa4\xe8\x81\x8aid
        :param mGbId: \xe5\x8e\x9f\xe7\xae\xa1\xe7\x90\x86\xe5\x91\x98gbId
        :param toGbId: \xe6\x96\xb0\xe7\xae\xa1\xe7\x90\x86\xe5\x91\x98gbId
        :return:
        """
        gamelog.debug('@zmm onTransferChatGroupManager', nuid, mGbId, toGbId)
        if self.gbId == mGbId:
            self.showGameMsg(GMDD.data.GROUP_CHAT_TRANSFER_SUCCESS, ())
        elif self.gbId == toGbId:
            groupName = self.groupChatData.get(nuid, {}).get('name', '')
            self.showGameMsg(GMDD.data.GROUP_CHAT_MANAGER_TRANSFER_ME, (groupName,))
        else:
            managerName = self.getGroupMemberName(nuid, mGbId)
            playerName = self.getGroupMemberName(nuid, toGbId)
            self.showGameMsg(GMDD.data.GROUP_CHAT_MANAGER_TRANSFER_PEOPLE, (managerName, playerName))
        if nuid in self.groupChatData:
            self.groupChatData[nuid]['managerGbId'] = toGbId
        gameglobal.rds.ui.groupChatMembers.hide()
        if gameglobal.rds.ui.groupChatRoom.isOpened(nuid):
            gameglobal.rds.ui.groupChatRoom.refreshInfo(nuid)
        elif gameglobal.rds.ui.groupChat.checkCurrentGroupChated(nuid):
            gameglobal.rds.ui.groupChat.updateGroupChatInfo(nuid)

    def onKickOutChatGroupMember(self, nuid, mGbId, toGbIds):
        """
        \xe8\xb8\xa2\xe5\x87\xba\xe7\xbe\xa4\xe8\x81\x8a\xe8\xbf\x94\xe5\x9b\x9e
        :param nuid: \xe7\xbe\xa4\xe8\x81\x8aid
        :param mGbId: \xe7\xae\xa1\xe7\x90\x86\xe5\x91\x98gbId
        :param toGbIds: \xe8\xa2\xab\xe8\xb8\xa2\xe7\xbe\xa4\xe6\x88\x90\xe5\x91\x98gbId \xe5\x88\x97\xe8\xa1\xa8
        :return:
        """
        gamelog.debug('@zmm onKickOutChatGroupMember', self.gbId, nuid, mGbId, toGbIds)
        managerName = self.getGroupMemberName(nuid, mGbId)
        if self.gbId == mGbId:
            pNames = ''
            for gbId in toGbIds:
                name = self.getGroupMemberName(nuid, gbId)
                if not pNames:
                    pNames = name
                else:
                    pNames = pNames + ',' + name

            self.showGameMsg(GMDD.data.GROUP_CHAT_MANAGE_KICK_SUCCESS, (pNames,))
            self.updateGroupInformationTips(nuid, managerName, toGbIds)
        elif self.gbId in toGbIds:
            groupName = self.groupChatData.get(nuid, {}).get('name', '')
            self.showGameMsg(GMDD.data.GROUP_CHAT_MEMBER_BE_KICKED, (managerName, groupName))
        else:
            self.updateGroupInformationTips(nuid, managerName, toGbIds)
        if nuid in self.groupChatData:
            members = self.groupChatData[nuid]['members']
            for gbId in toGbIds:
                if gbId in members:
                    self.groupChatData[nuid]['members'].pop(gbId)

        gameglobal.rds.ui.groupChatMembers.hide()
        gameglobal.rds.ui.groupChatSetup.hide()
        if gameglobal.rds.ui.groupChatRoom.isOpened(nuid):
            gameglobal.rds.ui.groupChatRoom.updateGroupChatRoomMembers(nuid)
        elif gameglobal.rds.ui.groupChat.checkCurrentGroupChated(nuid):
            gameglobal.rds.ui.groupChat.updateGroupChatInfo(nuid)

    def updateGroupInformationTips(self, nuid, managerName, toGbIds):
        pNames = ''
        for gbId in toGbIds:
            name = self.getGroupMemberName(nuid, gbId)
            if not pNames:
                pNames = name
            else:
                pNames = pNames + ',' + name

        infoTips = gameStrings.GROUP_CHAT_REMOVE_MEMBERS % (managerName, pNames)
        if gameglobal.rds.ui.groupChatRoom.isOpened(nuid):
            gameglobal.rds.ui.groupChatRoom.addGroupMsgByPlayer(nuid, infoTips, True)
        elif gameglobal.rds.ui.groupChat.checkCurrentGroupChated(nuid):
            gameglobal.rds.ui.groupChat.addMsgByGroup(nuid, infoTips, True)

    def getGroupUnreadMsgs(self, nuId):
        groupInfo = self.groupChatData.get(nuId, {})
        unreadMsgs = self.groupUnreadMsgs.get(nuId, [])
        gfxMsgs = []
        if unreadMsgs:
            members = groupInfo.get('members', {})
            for msg in unreadMsgs:
                senderGbId = msg.get('senderGbId', 0)
                member = members.get(senderGbId, ())
                gfxMsg = {}
                if member:
                    gfxMsg = gameglobal.rds.ui.groupChatRoom.setGMsgData(member, msg)
                gfxMsgs.append(gfxMsg)

            if gfxMsgs:
                self.clearGroupUnreadMsg(nuId)
        return gfxMsgs
