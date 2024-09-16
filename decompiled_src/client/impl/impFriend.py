#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impFriend.o
from gamestrings import gameStrings
import copy
import zlib
import cPickle
import os
import json
import random
import BigWorld
import gamelog
import gameglobal
import gametypes
import const
import utils
import formula
from helpers.intimacyEvent import IntimacyEvent, EventVal
from guis import events, uiUtils
from friend import FriendVal, IntimacySkillVal
from helpers import workerQueue
from helpers import taboo
from helpers.eventDispatcher import Event
from gameStrings import gameStrings
from sfx import sfx
from guis import uiConst
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD
from data import title_data as TD
from data import intimacy_data as ID
from data import game_msg_data as GMD
from data import sys_config_data as SCD
from data import us_player_tag_data as UPTD
from data import photo_border_data as PBD
from data import nf_npc_data as NND
MAX_TAG_DISPLAY_NUM = 3

class ChatHistoryAdaptor(object):
    VERSION = 1.1

    def __init__(self):
        self.workerQueue = workerQueue.SimpleWorkerQueue()

    def init(self):
        pass

    def upgrade(self, ownerGbId):
        chatdir = '../game/chat'
        if not os.path.exists(chatdir):
            os.mkdir(chatdir)
        avatarchatdir = '%s/%s' % (chatdir, ownerGbId)
        if os.path.exists(avatarchatdir):
            return
        ownerGbIdStr = str(ownerGbId)
        dpaths = []
        for dname in os.listdir(chatdir):
            dpath = '%s/%s' % (chatdir, dname)
            if os.path.isdir(dpath):
                _gbIdStr = dname.split('_')[0]
                if _gbIdStr == ownerGbIdStr:
                    dpaths.append((dname, os.stat(dpath).st_ctime))

        dpaths.sort(key=lambda x: x[1], reverse=True)
        if dpaths:
            dname = dpaths[0][0]
            if not os.path.exists(avatarchatdir):
                os.rename('%s/%s' % (chatdir, dname), avatarchatdir)
                fpaths = []
                for fname in os.listdir(avatarchatdir):
                    fpath = '%s/%s' % (avatarchatdir, fname)
                    if os.path.isfile(fpath):
                        fpaths.append((fname, os.stat(fpath).st_ctime))

                fpaths.sort(key=lambda x: x[1], reverse=True)
                for fname, _ in fpaths:
                    _friendGbIdStr = fname.split('_')[0]
                    if _friendGbIdStr:
                        friendchatfile = '%s/%s.js' % (avatarchatdir, _friendGbIdStr)
                        if not os.path.exists(friendchatfile):
                            os.rename('%s/%s' % (avatarchatdir, fname), friendchatfile)

        if not os.path.exists(avatarchatdir):
            os.mkdir(avatarchatdir)

    def saveMsg(self, gbId, role, name, isMe, photo, msg, createdTime):
        self.workerQueue.applyAsync(self._saveMsg, (gbId,
         role,
         name,
         isMe,
         photo,
         msg,
         createdTime))

    def saveNpcMsg(self, gbId, npcPid, msg, createTime):
        self.workerQueue.applyAsync(self._saveNpcMsg, (gbId,
         npcPid,
         msg,
         createTime))

    def _saveNpcMsg(self, gbId, npcId, msg, createdTime):
        chatdir = '../game/chat'
        if not os.path.exists(chatdir):
            os.mkdir(chatdir)
        p = BigWorld.player()
        path = '../game/chat/npc/%s' % gbId
        if not os.path.exists(path):
            os.makedirs(path)
        fileName = '%s/%s.js' % (path, npcId)
        fmode = 'a'
        photo = uiUtils.getPNpcIcon(npcId)
        name = NND.data.get(npcId, {}).get('name', '')
        newLine = json.dumps((0,
         name,
         0,
         photo,
         msg,
         createdTime), ensure_ascii=False, encoding=utils.defaultEncoding()) + '\n'
        if os.path.exists(fileName):
            statInfo = os.stat(fileName)
            if statInfo.st_size > const.CHAT_HISTORY_FILE_SIZE_LIMIT:
                halfSize = int(const.CHAT_HISTORY_FILE_SIZE_LIMIT / 2)
                lines = []
                with open(fileName, 'r') as f:
                    while True:
                        line = f.readline(1024)
                        if not line:
                            break
                        if not lines:
                            lines.append(line)
                        if f.tell() > halfSize:
                            lines.append(line)

                lines.append(newLine)
                with open(fileName, 'w') as f:
                    f.writelines(lines)
                return
            lines = [newLine]
        else:
            fmode = 'w'
            lines = [newLine]
        with open(fileName, fmode) as f:
            f.writelines(lines)

    def _saveMsg(self, gbId, role, name, isMe, photo, msg, createdTime):
        chatdir = '../game/chat'
        if not os.path.exists(chatdir):
            os.mkdir(chatdir)
        p = BigWorld.player()
        path = '%s/%s' % (chatdir, p.gbId)
        if not os.path.exists(path):
            os.mkdir(path)
        fileName = '%s/%s.js' % (path, gbId)
        fmode = 'a'
        newLine = 'd.push(%s);\n' % json.dumps((isMe and 1 or 0,
         photo,
         msg,
         createdTime), ensure_ascii=False, encoding=utils.defaultEncoding())
        newLine = newLine.encode(utils.defaultEncoding())
        if os.path.exists(fileName):
            statInfo = os.stat(fileName)
            if statInfo.st_size > const.CHAT_HISTORY_FILE_SIZE_LIMIT:
                halfSize = int(const.CHAT_HISTORY_FILE_SIZE_LIMIT / 2)
                lines = []
                with open(fileName, 'r') as f:
                    while True:
                        line = f.readline(1024)
                        if not line:
                            break
                        if not lines:
                            lines.append(line)
                        if f.tell() > halfSize:
                            lines.append(line)

                lines.append(newLine)
                with open(fileName, 'w') as f:
                    f.writelines(lines)
                return
            lines = [newLine]
        else:
            fmode = 'w'
            lines = ['var d=data=[];\n', newLine]
        with open(fileName, fmode) as f:
            f.writelines(lines)

    def getMsgs(self, gbId, name, offset, limit, callback = None):
        self.workerQueue.applyAsync(self._getMsgs, (gbId,
         name,
         offset,
         limit), callback)

    def getNpcMsgs(self, gbId, npcPid, offset, limit, callback = None):
        self.workerQueue.applyAsync(self._getNpcMsgs, (gbId,
         npcPid,
         offset,
         limit), callback)

    def _getNpcMsgs(self, gbId, npcPId, offset, limit):
        fileName = '../game/chat/npc/%s/%s.js' % (gbId, npcPId)
        if not os.path.exists(fileName):
            return ([], 0)
        with open(fileName, 'rb') as f:
            lines = f.readlines()
        lines.reverse()
        total = len(lines)
        msgs = []
        lines = lines[offset:offset + limit]
        for line in lines:
            line = line.decode(utils.defaultEncoding())
            msg = json.loads(line, encoding=utils.defaultEncoding())
            msgs.append(msg)

        msgs.reverse()
        return (msgs, total)

    def _getMsgs(self, gbId, name, offset, limit):
        p = BigWorld.player()
        fileName = '../game/chat/%s/%s.js' % (p.gbId, gbId)
        if not os.path.exists(fileName):
            return ([], 0)
        with open(fileName, 'rb') as f:
            lines = f.readlines()
        lines.pop(0)
        lines.reverse()
        total = len(lines)
        msgs = []
        lines = lines[offset:offset + limit]
        for line in lines:
            line = line.decode(utils.defaultEncoding())
            line = line[line.index('(') + 1:line.rindex(')')]
            msg = json.loads(line, encoding=utils.defaultEncoding())
            if msg[0]:
                msg.insert(0, p.realRoleName)
            else:
                msg.insert(0, name)
            msg.insert(0, gbId)
            msgs.append(msg)

        msgs.reverse()
        return (msgs, total)

    def saveSysMsg(self, gbId, msgId, createdTime, args):
        self.workerQueue.applyAsync(self._saveSysMsgEx, (gbId, [(msgId, createdTime, args)]))

    def saveSysMsgs(self, gbId, msgs):
        self.workerQueue.applyAsync(self._saveSysMsgEx, (gbId, msgs))

    def _saveSysMsgEx(self, gbId, msgs):
        chatdir = '../game/sysmsg'
        if not os.path.exists(chatdir):
            os.mkdir(chatdir)
        fileName = '%s/%s.js' % (chatdir, gbId)
        fmode = 'a'
        try:
            newLines = [ '%s\n' % repr(x) for x in msgs ]
        except:
            import traceback, sys
            traceback.print_exception(*sys.exc_info())
            return

        if os.path.exists(fileName):
            statInfo = os.stat(fileName)
            if statInfo.st_size > const.CHAT_HISTORY_FILE_SIZE_LIMIT:
                halfSize = int(const.CHAT_HISTORY_FILE_SIZE_LIMIT / 2)
                lines = []
                with open(fileName, 'r') as f:
                    while True:
                        line = f.readline(1024)
                        if not line:
                            break
                        if not lines:
                            lines.append(line)
                        if f.tell() > halfSize:
                            lines.append(line)

                lines.extend(newLines)
                with open(fileName, 'w') as f:
                    f.writelines(lines)
                return
            lines = newLines
        else:
            fmode = 'w'
            lines = newLines
        with open(fileName, fmode) as f:
            f.writelines(lines)

    def getSysMsgs(self, gbId, offset, limit, callback = None):
        self.workerQueue.applyAsync(self._getSysMsgs, (gbId, offset, limit), callback)

    def _getSysMsgs(self, gbId, offset, limit):
        fileName = '../game/sysmsg/%s.js' % gbId
        if not os.path.exists(fileName):
            return ([], 0)
        with open(fileName, 'rb') as f:
            lines = f.readlines()
        lines.reverse()
        total = len(lines)
        msgs = []
        lines = lines[offset:offset + limit]
        for line in lines:
            try:
                msg = eval(line)
                msgs.append(msg)
            except:
                pass

        msgs.reverse()
        return (msgs, total)

    def saveGroupMsg(self, nuId, playerName, msg, isMe, createdTime):
        self.workerQueue.applyAsync(self._saveGroupMsg, (nuId, [(isMe and 1 or 0,
           playerName,
           msg,
           createdTime)]))

    def saveGroupMsgs(self, nuId, membersMsgs):
        self.workerQueue.applyAsync(self._saveGroupMsg, (nuId, membersMsgs))

    def _saveGroupMsg(self, nuId, membersMsgs):
        p = BigWorld.player()
        chatdir = '../game/chat/groupChat/%s' % p.gbId
        if not os.path.exists(chatdir):
            os.makedirs(chatdir)
        fileName = '%s/%s.js' % (chatdir, nuId)
        fmode = 'a'
        try:
            newLines = [ '%s\n' % repr(x) for x in membersMsgs ]
        except:
            import traceback, sys
            traceback.print_exception(*sys.exc_info())
            return

        if os.path.exists(fileName):
            statInfo = os.stat(fileName)
            if statInfo.st_size > const.CHAT_HISTORY_FILE_SIZE_LIMIT:
                halfSize = int(const.CHAT_HISTORY_FILE_SIZE_LIMIT / 2)
                lines = []
                with open(fileName, 'r') as f:
                    while True:
                        line = f.readline(1024)
                        if not line:
                            break
                        if not lines:
                            lines.append(line)
                        if f.tell() > halfSize:
                            lines.append(line)

                lines.append(newLines)
                with open(fileName, 'w') as f:
                    f.writelines(lines)
                return
            lines = newLines
        else:
            fmode = 'w'
            lines = newLines
        with open(fileName, fmode) as f:
            f.writelines(lines)

    def getGroupMsgs(self, nuId, offset, limit, callback = None):
        self.workerQueue.applyAsync(self._getGroupMsgs, (nuId, offset, limit), callback)

    def _getGroupMsgs(self, nuId, offset, limit):
        p = BigWorld.player()
        fileName = '../game/chat/groupChat/%s/%s.js' % (p.gbId, nuId)
        if not os.path.exists(fileName):
            return ([], 0)
        with open(fileName, 'rb') as f:
            lines = f.readlines()
        lines.reverse()
        total = len(lines)
        membersMsgs = []
        lines = lines[offset:offset + limit]
        for line in lines:
            try:
                msg = eval(line)
                membersMsgs.append(msg)
            except:
                pass

        membersMsgs.reverse()
        return (membersMsgs, total)

    def close(self):
        self.workerQueue.close()


class ImpFriend(object):

    def initFriend(self, groups, friends, options, signature, showsig, state, profile, oldFriendActive, intimacyTgt, tBuildIntimacy, defaultGroup, groupOrder, intimacyTgtNickName, tempFriendList, recentFriendList):
        self.friend.groups = groups
        self.friend.signature = signature
        self.friend.showsig = showsig
        self.friend.state = state
        self.friend.intimacyTgt = intimacyTgt
        self.friend.tBuildIntimacy = tBuildIntimacy
        self.friend.defaultGroup = defaultGroup
        self.friend.groupOrder = groupOrder
        self.friend.tempFriendList = tempFriendList
        self.friend.recentFriendList = recentFriendList
        self.chatDB = ChatHistoryAdaptor()
        self.intimacyTgtNickName = intimacyTgtNickName
        self.chatDB.init()
        try:
            self.chatDB.upgrade(self.gbId)
        except Exception as e:
            pass

        for option, checked in options.iteritems():
            self.friend.setOption(option, checked)

        self.friend.clear()
        for dto in friends:
            fVal = self._createFriendVal(dto)
            self.friend[fVal.gbId] = fVal

        sysVal = FriendVal(name=gameStrings.SYSTEM_MESSAGE_FRIEND_NAME, gbId=const.FRIEND_SYSTEM_NOTIFY_ID)
        sysVal.temp = False
        sysVal.recent = False
        sysVal.time = utils.getNow()
        sysVal.eid = 0
        sysVal.photo = 'systemMessageIcon/systemMsgNew.dds'
        fVal = FriendVal(name=gameStrings.TEXT_BOOTHPROXY_694, gbId=const.FRIEND_SYSTEM_ID)
        fVal.temp = False
        fVal.recent = False
        fVal.time = utils.getNow()
        fVal.eid = 0
        gameglobal.rds.ui.friend.inited = True
        self.onProfileUpdate(profile)
        self.friend[const.FRIEND_SYSTEM_ID] = fVal
        self.friend[const.FRIEND_SYSTEM_NOTIFY_ID] = sysVal
        self.updateOldFriendActive(oldFriendActive)
        self._processFriendMsgsBeforeInit()
        if self.friend.intimacyTgt and self.activeTitleType == const.ACTIVE_TITLE_TYPE_WORLD:
            currTitleId = self.currTitle[const.TITLE_TYPE_WORLD]
            if currTitleId and TD.data.get(currTitleId, {}).get('gId') == gametypes.TITLE_GROUP_INTIMACY:
                self.refreshToplogoTitle()
        self.friend.inited = True
        BigWorld.callback(10, self.initCheckRecommendFriend)
        BigWorld.callback(10, self._checkHomeOnlineNotify)
        numTempInfo = len(self.friend.tempContactInfoBeforeInit)
        if numTempInfo:
            for i, (gbId, info) in enumerate(self.friend.tempContactInfoBeforeInit):
                self.contactUpdated(gbId, info, i == numTempInfo - 1)

    def _checkHomeOnlineNotify(self):
        if not hasattr(self, 'operation'):
            return
        notifyFriend = self.operation['commonSetting'][const.COMMON_SETTING_INDEX_ENABLE_NOTIFY_FRIEND_ONLINE_STATUS]
        if notifyFriend >= 0:
            if notifyFriend != self.friend.getOption(gametypes.FRIEND_OPTION_HOME_ONLINE_NOTIFY):
                self.base.setFriendOption(gametypes.FRIEND_OPTION_HOME_ONLINE_NOTIFY, notifyFriend)
            self.operation['commonSetting'][const.COMMON_SETTING_INDEX_ENABLE_NOTIFY_FRIEND_ONLINE_STATUS] = -1

    def _processFriendMsgsBeforeInit(self):
        if gameglobal.rds.ui.friend.messagesBeforeInit:
            for func, args in gameglobal.rds.ui.friend.messagesBeforeInit:
                func(*args)

        gameglobal.rds.ui.friend.messagesBeforeInit = []

    def onSetIntimacyTgtNickName(self, nickName):
        self.intimacyTgtNickName = nickName
        self.showGameMsg(GMDD.data.SET_INTIMACY_TGT_NICK_NAME_SUCC, ())

    def onNotifyIntimacyTgtShowIntimate(self, entityId):
        gamelog.debug('@hjx onNotifyIntimacyTgtShowIntimate:', entityId)
        if not gameglobal.rds.configData.get('enableIntimacyTgtNickName', False):
            return
        effId = SCD.data.get('jieQiNickNameSfxId', 0)
        if effId:
            p = BigWorld.player()
            entity = BigWorld.entity(entityId)
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (p.getSkillEffectLv(),
             p.getSkillEffectPriority(),
             entity.model,
             effId,
             sfx.EFFECT_UNLIMIT,
             5))

    def addIntimacyEvent(self, key, eType, chunkName, msg, when, picList):
        gamelog.debug('@hjx intimacyEvent#addIntimacyEvent:', key, eType, chunkName, msg, when, picList)
        if not hasattr(self, 'intimacyEvent'):
            self.intimacyEvent = IntimacyEvent()
        eVal = EventVal(self.roleName, chunkName, msg, eType, when, picList)
        self.intimacyEvent.addEvent(key, eVal)
        if eType in gametypes.INTIMACY_EVENT_NOTIFY_TYPE:
            self.showGameMsg(GMDD.data.ADD_INTIMACY_EVENT_SUCC, ())

    def getBuildIntimacyCnt(self):
        if self.isOldBuildIntimacy:
            return int(self.buildIntimacyCnt * 2.2)
        else:
            return self.buildIntimacyCnt

    def onQeuryIntimacyEvent(self, intimacyEvent, version, isOld, buildIntimacyCnt):
        intimacyEvent = cPickle.loads(zlib.decompress(intimacyEvent))
        gamelog.debug('@hjx intimacyEvent#onQeuryIntimacyEvent:', intimacyEvent, version)
        self.intimacyEvent = IntimacyEvent().fromDTO(intimacyEvent)
        self.buildIntimacyCnt = buildIntimacyCnt
        self.isOldBuildIntimacy = isOld
        gameglobal.rds.ui.jieQi.refresh(version)
        gameglobal.rds.ui.jieQiV2.refresh(version)

    def removeIntimacyEvent(self, when):
        gamelog.debug('@hjx intimacyEvent#removeIntimacyEvent:', when)
        if not hasattr(self, 'intimacyEvent'):
            return
        key = utils.genIntimacyEventKey(when)
        event = self.intimacyEvent.removeEvent(key, when)
        if event and event.msgType in gametypes.INTIMACY_EVENT_NOTIFY_TYPE:
            self.showGameMsg(GMDD.data.REMOVE_INTIMACY_EVENT_SUCC, ())

    def refreshFriend(self, friends):
        friends = cPickle.loads(zlib.decompress(friends))
        for dto in friends:
            fVal = self._updateFriendVal(dto)
            self.friend[fVal.gbId] = fVal

        self._refreshFriendList()

    def tempFriendAdded(self, dto):
        fVal = self._updateFriendVal(dto)
        if self.friend.has_key(fVal.gbId):
            self.friend.temp.pop(fVal.name, None)
            return
        else:
            self.friend[fVal.gbId] = fVal
            fVal.temp = True
            fVal.time = utils.getNow()
            if self._getTempFriendsCount() > const.FRIEND_TEMP_MAX:
                self._removeFirstTempFriend()
            self.friend.temp.pop(fVal.name, None)
            self._refreshFriendList('temp')
            gameglobal.rds.ui.friend.onTempFriendAdded(fVal.name, fVal.gbId)
            return

    def recentFriendAdded(self, dto):
        fVal = self._updateFriendVal(dto)
        if self.friend.has_key(fVal.gbId):
            self.friend.temp.pop(fVal.name, None)
            return
        else:
            self.friend[fVal.gbId] = fVal
            if not self.friend.isFriend(fVal.gbId):
                fVal.temp = True
                fVal.time = utils.getNow()
                if self._getTempFriendsCount() > const.FRIEND_TEMP_MAX:
                    self._removeFirstTempFriend()
            fVal.recent = True
            fVal.time = utils.getNow()
            if self._getRecentFriendsCount() > const.FRIEND_RECENT_MAX:
                self._removeFirstRecentFriend()
            self.friend.temp.pop(fVal.name, None)
            self._refreshFriendList('temp')
            self.handleFriendMsgAsync(fVal.gbId)
            return

    def recentFriendAddedByGbId(self, recentFriendList):
        self.friend.recentFriendList = recentFriendList
        gameglobal.rds.ui.friend.refreshFriendList('recent')

    def _createFriendVal(self, dto):
        eid, gbId, dbID, group, level, acknowledge, fstate, spaceNo, areaId, name, fsignature, school, sex, hatred, pally, showsig, photo, apprentice, yixinOpenId, deleted, toHostID, flowbackType, intimacy, remarkName, intimacyLv, srcId, mingpaiId, appearanceCollectPoint, endlessChallengeInfo, recallState, recallInfo, borderId, activityDict = dto
        if utils.isRenameString(name):
            name = utils.getDisplayName(name)
        fVal = FriendVal(gbId=gbId, dbID=dbID, group=group, level=level, acknowledge=acknowledge, state=fstate, spaceNo=spaceNo, areaId=areaId, name=name, signature=fsignature, school=school, sex=sex, hatred=hatred, pally=pally, showsig=showsig, photo=photo, apprentice=apprentice, yixinOpenId=yixinOpenId, deleted=deleted, toHostID=toHostID, flowbackType=flowbackType, intimacy=intimacy, remarkName=remarkName, intimacyLv=intimacyLv, srcId=srcId, mingpaiId=mingpaiId, appearanceCollectPoint=appearanceCollectPoint, endlessChallengeInfo=endlessChallengeInfo, recallState=recallState, recallInfo=recallInfo, borderId=borderId, activityDict=activityDict)
        fVal.temp = False
        fVal.recent = False
        fVal.time = utils.getNow()
        fVal.eid = eid
        return fVal

    def _updateFriendVal(self, dto):
        eid, gbId, dbID, group, level, acknowledge, fstate, spaceNo, areaId, name, fsignature, school, sex, hatred, pally, showsig, photo, apprentice, yixinOpenId, deleted, toHostID, flowbackType, intimacy, remarkName, intimacyLv, srcId, mingpaiId, appearanceCollectPoint, endlessChallengeInfo, recallState, recallInfo, borderId, activityID = dto
        fVal = self.friend.get(gbId)
        if not fVal:
            return self._createFriendVal(dto)
        if utils.isRenameString(name):
            name = utils.getDisplayName(name)
        fVal.gbId = gbId
        fVal.dbID = dbID
        fVal.group = group
        fVal.level = level
        fVal.acknowledge = acknowledge
        fVal.state = fstate
        fVal.spaceNo = spaceNo
        fVal.areaId = areaId
        fVal.name = name
        fVal.signature = fsignature
        fVal.school = school
        fVal.sex = sex
        fVal.hatred = hatred
        fVal.pally = pally
        fVal.eid = eid
        fVal.showsig = showsig
        fVal.photo = photo
        fVal.apprentice = apprentice
        fVal.yixinOpenId = yixinOpenId
        fVal.deleted = deleted
        fVal.toHostID = toHostID
        fVal.flowbackType = flowbackType
        fVal.intimacy = intimacy
        fVal.remarkName = remarkName
        fVal.intimacyLv = intimacyLv
        fVal.srcId = srcId
        fVal.mingpaiId = mingpaiId
        fVal.endlessChallengeInfo = endlessChallengeInfo
        fVal.recallState = recallState
        fVal.recallInfo = recallInfo
        fVal.borderId = borderId
        fVal.activityDict = activityDict
        return fVal

    def contactAdded(self, dto):
        gamelog.info('jbx:contactAdded', dto)
        fVal = self._createFriendVal(dto)
        self.friend.temp.pop(fVal.gbId, None)
        if self.friend.isTempGroup(fVal.group):
            if fVal.gbId not in self.friend.tempFriendList:
                self.friend.tempFriendList.append(fVal.gbId)
            if fVal.gbId not in self.friend.recentFriendList:
                self.friend.recentFriendList.insert(0, fVal.gbId)
        self.friend[fVal.gbId] = fVal
        self._refreshFriendList()
        gameglobal.rds.ui.friend.onFriendAdded(fVal.gbId)
        if fVal.acknowledge:
            self.onQuestInfoModifiedAtClient(const.QD_JIEQI, exData={'refreshAll': 1})
        gameglobal.rds.ui.npcInteractive.refreshInfo()

    def contactUpdated(self, gbId, info, doRefresh = True):
        if not self.friend.inited:
            self.friend.tempContactInfoBeforeInit.append((gbId, info))
        fVal = self.friend.get(gbId)
        if not fVal:
            return
        bUpdate = False
        bRefreshAll = False
        bUpdateEnemy = False
        if info.has_key('eid'):
            fVal.eid = info['eid']
        if info.has_key('state'):
            if self.friend.updateState(gbId, info['state']):
                bUpdate = True
                bRefreshAll = True
        if info.has_key('spaceNo'):
            self.friend.updateSpaceNo(gbId, info['spaceNo'])
        if info.has_key('areaId'):
            self.friend.updateAreaId(gbId, 0, info['areaId'])
        if info.has_key('pally'):
            if self.friend.updatePally(gbId, info['pally']):
                bUpdate = True
        if info.has_key('intimacy'):
            f = self.friend.get(gbId)
            oldIntimacy = f.intimacy if f else 0
            if self.friend.updateIntimacy(gbId, info['intimacy']):
                bUpdate = True
                self.updateQuestWithIntimacyChange(oldIntimacy, f.intimacy, f.intimacyLv)
        if info.has_key('intimacyLv'):
            if self.friend.updateIntimacyLv(gbId, info['intimacyLv']):
                bUpdate = True
                self.updateTeamQuestWithIntimacy()
        if info.has_key('hatred'):
            if self.friend.updateHatred(gbId, info['hatred']):
                bUpdateEnemy = True
        if info.has_key('group'):
            if self.friend.updateGroup(gbId, info['group']):
                bUpdate = True
                bRefreshAll = True
        if info.has_key('acknowledge'):
            if self.friend.updateAcknowledge(gbId, info['acknowledge']):
                bUpdate = True
                self.onQuestInfoModifiedAtClient(const.QD_JIEQI, exData={'refreshAll': 1})
        if info.has_key('showsig'):
            if self.friend.updateShowsig(gbId, info['showsig']):
                bUpdate = True
        if info.has_key('signature'):
            self.friend.updateSignature(gbId, info['signature'])
        if info.has_key('name'):
            if self.friend.updateName(gbId, utils.getDisplayName(info['name'])):
                bUpdate = True
        if info.has_key('level'):
            if self.friend.updateLevel(gbId, info['level']):
                bUpdate = True
        if info.has_key('yixinOpenId'):
            if self.friend.updateYixinStatus(gbId, info['yixinOpenId']):
                bUpdate = True
        if info.has_key('apprentice'):
            if self.friend.updateApprentice(gbId, info['apprentice']):
                bUpdate = True
        if info.has_key('sex'):
            if self.friend.updateSex(gbId, info['sex']):
                bUpdate = True
        if info.has_key('flowbackType'):
            if self.friend.updateFlowbackType(gbId, info['flowbackType']):
                bUpdate = True
        if info.has_key('remarkName'):
            if self.friend.updateRemarkName(gbId, info['remarkName']):
                bUpdate = True
        if info.has_key('srcId'):
            if self.friend.updateSrcId(gbId, info['srcId']):
                bUpdate = True
        if info.has_key('mingpaiId'):
            if self.friend.updateMingpaiId(gbId, info['mingpaiId']):
                bUpdate = True
        if info.has_key('appearanceCollectPoint'):
            if self.friend.updateAppearanceCollectPoint(gbId, info['appearanceCollectPoint']):
                bUpdate = True
        if info.has_key('endlessChallengeInfo'):
            if self.friend.updateEndlessChallengeInfo(gbId, info['endlessChallengeInfo']):
                bUpdate = True
        if info.has_key('spriteChallengeInfo'):
            if self.friend.updateSpriteChallengeInfo(gbId, info['spriteChallengeInfo']):
                bUpdate = True
        if info.has_key('recallState'):
            if self.friend.updateRecallState(gbId, info['recallState']):
                bUpdate = True
        if info.has_key('recallInfo'):
            if self.friend.updateRecallInfo(gbId, info['recallInfo']):
                bUpdate = True
        if info.has_key('school'):
            if self.friend.updateSchool(gbId, info['school']):
                bUpdate = True
        if info.has_key('activityDict'):
            if self.friend.updateActivityDict(gbId, info['activityDict']):
                bUpdate = True
        if not doRefresh:
            return
        if bUpdate:
            if bRefreshAll:
                self._refreshFriendList()
                gameglobal.rds.ui.groupChat.onUpdataFriendInfo(gbId)
            else:
                self._refreshFriendListWithoutIcon()
        if bUpdateEnemy:
            self._refreshFriendList('enemy')
        data = self._createFriendData(fVal)
        gameglobal.rds.ui.chatToFriend.updateStatus(gbId, data)

    def updateTeamQuestWithIntimacy(self):
        if len(self.members) == 2:
            intimacyVal = self.getMemberIntimacy(self.members)
            self.onQuestInfoModifiedAtClient(const.QD_JIEQI, exData={'intimacy': intimacyVal})

    def updateQuestWithIntimacyChange(self, oldIntimacy, curIntimacy, intimacyLv):
        maxVal = ID.data.get(intimacyLv, {}).get('maxVal', 0)
        if oldIntimacy < maxVal and curIntimacy >= maxVal:
            self.updateTeamQuestWithIntimacy()

    def contactsUpdated(self, infoList):
        bUpdate = False
        bChangeGroup = False
        bUpdateEnemy = False
        for info in infoList:
            gbId = info['gbId']
            if info.has_key('state'):
                if self.friend.updateState(gbId, info['state']):
                    bUpdate = True
            if info.has_key('spaceNo'):
                self.friend.updateSpaceNo(gbId, info['spaceNo'])
            if info.has_key('areaId'):
                self.friend.updateAreaId(gbId, 0, info['areaId'])
            if info.has_key('pally'):
                if self.friend.updatePally(gbId, info['pally']):
                    bUpdate = True
            if info.has_key('intimacy'):
                f = self.friend.get(gbId)
                oldIntimacy = f.intimacy if f else 0
                if self.friend.updateIntimacy(gbId, info['intimacy']):
                    bUpdate = True
                    self.updateQuestWithIntimacyChange(oldIntimacy, f.intimacy, f.intimacyLv)
            if info.has_key('intimacyLv'):
                if self.friend.updateIntimacyLv(gbId, info['intimacyLv']):
                    bUpdate = True
                    self.updateTeamQuestWithIntimacy()
            if info.has_key('hatred'):
                if self.friend.updateHatred(gbId, info['hatred']):
                    bUpdateEnemy = True
            if info.has_key('group'):
                if self.friend.updateGroup(gbId, info['group']):
                    bUpdate = True
                    bChangeGroup = True
            if info.has_key('acknowledge'):
                if self.friend.updateAcknowledge(gbId, info['acknowledge']):
                    bUpdate = True
            if info.has_key('showsig'):
                if self.friend.updateShowsig(gbId, info['showsig']):
                    bUpdate = True
            if info.has_key('signature'):
                self.friend.updateSignature(gbId, info['signature'])
            if info.has_key('name'):
                if self.friend.updateName(gbId, utils.getDisplayName(info['name'])):
                    bUpdate = True
            if info.has_key('level'):
                if self.friend.updateLevel(gbId, info['level']):
                    bUpdate = True
            if info.has_key('yixinOpenId'):
                if self.friend.updateYixinStatus(gbId, info['yixinOpenId']):
                    bUpdate = True
            if info.has_key('apprentice'):
                if self.friend.updateApprentice(gbId, info['apprentice']):
                    bUpdate = True
            if info.has_key('sex'):
                if self.friend.updateSex(gbId, info['sex']):
                    bUpdate = True
            if info.has_key('flowbackType'):
                if self.friend.updateFlowbackType(gbId, info['flowbackType']):
                    bUpdate = True
            if info.has_key('remarkName'):
                if self.friend.updateRemarkName(gbId, info['remarkName']):
                    bUpdate = True
            if info.has_key('srcId'):
                if self.friend.updateSrcId(gbId, info['srcId']):
                    bUpdate = True
            if info.has_key('mingpaiId'):
                if self.friend.updateMingpaiId(gbId, info['mingpaiId']):
                    bUpdate = True
            if info.has_key('school'):
                if self.friend.updateSchool(gbId, info['school']):
                    bUpdate = True
            if info.has_key('activityDict'):
                if self.friend.updateActivityDict(gbId, info['activityDict']):
                    bUpdate = True

        if bUpdate:
            if bChangeGroup:
                self._refreshFriendList()
            else:
                self._refreshFriendListWithoutIcon()
        if bUpdateEnemy:
            self._refreshFriendList('enemy')

    def contactDeleted(self, gbId):
        fVal = self.friend.get(gbId)
        if fVal:
            self.friend.pop(gbId)
            if fVal.acknowledge:
                self.onQuestInfoModifiedAtClient(const.QD_JIEQI, exData={'refreshAll': 1})
            fVal.group = 0
            if gbId in self.friend.tempFriendList:
                self.friend.tempFriendList.remove(gbId)
            if gbId in self.friend.recentFriendList:
                self.friend.recentFriendList.remove(gbId)
        self._refreshFriendList()

    def friendAddedBy(self, fGbId, fRole, fSchool, srcId, msgType):
        gamelog.debug('@hjx friend#friendAddedBy:', fRole, fSchool, srcId)
        if self.friend.isFriend(fGbId):
            return
        msgs = {'roleName': fRole,
         'school': fSchool,
         'srcId': srcId}
        self._addTempMsg(fGbId, msgType, msgs)

    def addEnemyPrompt(self, infoList):
        for gbId, role, lv in infoList:
            if self.friend.isEnemy(gbId):
                continue
            gameglobal.rds.ui.addEnemy.pushEnemyMessage(gbId, role, lv)

    def _showFriendAddedMsg(self, fGbId, fRole, msgType):
        if self.friend.isFriend(fGbId):
            return
        msg = gameStrings.TEXT_IMPFRIEND_925 % fRole
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.onFriendAccept, fGbId, msgType), yesBtnText=gameStrings.TEXT_IMPFRIEND_926, noCallback=Functor(self.onFriendIngore, fGbId, msgType), noBtnText=gameStrings.TEXT_IMPFRIEND_927)

    def _showPromptMsg(self, msg):
        gameglobal.rds.ui.messageBox.showMsgBox(msg)

    def onQueryFiendInfo(self, info):
        gamelog.debug('@hjx friend#onQueryFiendInfo:', info)
        gbId = info.get('gbId', 0)
        info['onlineTime'] = ''
        keys = ['pvisibility',
         'photo',
         'constellation',
         'birthmonth',
         'birthday',
         'sex',
         'bloodType',
         'province',
         'city',
         'qq',
         'desc',
         'onlineTime',
         'roleName',
         'lv',
         'school',
         'guildName']
        data = [ info[key] for key in keys ]
        if self.friend and not data[1]:
            data[1] = self.friend.getDefaultPhoto(info['school'], info['sex'])
        gameglobal.rds.ui.friend.showOtherProfile(gbId, data)

    def onFriendAccept(self, who, msgType):
        BigWorld.player().base.addContactByGbId(who, gametypes.FRIEND_GROUP_FRIEND, 0)
        gameglobal.rds.sound.playSound(gameglobal.SD_2)
        if msgType == gametypes.FRIEND_MSG_TYPE_OFFLINE_ADD:
            self.base.rmOfflineFriendInvite(who)

    def onFriendIngore(self, who, msgType):
        if msgType == gametypes.FRIEND_MSG_TYPE_OFFLINE_ADD:
            self.base.rmOfflineFriendInvite(who)

    def _showDeleteEnemyPrompt(self, gbId, group, opNuid):
        fVal = self.friend.get(gbId)
        if not fVal:
            return
        msg = gameStrings.TEXT_IMPFRIEND_961 % fVal.name
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.onDeleteEnemyAccept, gbId, group, opNuid), yesBtnText=gameStrings.TEXT_IMPFRIEND_962, noCallback=Functor(self.onDeleteEnemyReject, gbId, opNuid), noBtnText=gameStrings.TEXT_IMPFRIEND_963)

    def onDeleteEnemyAccept(self, gbId, group, opNuid):
        self.base.confirmDeleteEnemy(gbId, group, opNuid)

    def onDeleteEnemyReject(self, gbId, opNuid):
        self.base.rejectDeleteEnemy(gbId, opNuid)

    def friendGroupAdded(self, group, name):
        self.friend.addGroup(group, name)
        if group not in self.friend.groupOrder:
            self.friend.groupOrder.append(group)
        self._refreshFriendList()
        gameglobal.rds.ui.friend.checkFriendToMove(group, name)

    def friendGroupUpdated(self, group, name):
        self.friend.setGroupName(group, name)
        self._refreshFriendList()
        groupEvent = Event(events.EVENT_RENAME_GROUP, {'groupId': group,
         'groupName': name})
        gameglobal.rds.ui.dispatchEvent(groupEvent)

    def friendGroupDeleted(self, group):
        for fVal in self.friend.itervalues():
            if fVal.group == group:
                fVal.group = gametypes.FRIEND_GROUP_FRIEND

        self.friend.groups.pop(group, None)
        if group in self.friend.groupOrder:
            self.friend.groupOrder.remove(group)
        if group == self.friend.defaultGroup:
            self.friend.defaultGroup = gametypes.FRIEND_GROUP_FRIEND
        self._refreshFriendList()
        gameglobal.rds.ui.chatToFriend.friendGroupDeleted(group)

    def onUpdateFriendDefaultGroup(self, groupId):
        self.friend.defaultGroup = groupId

    def onUpdateFriendGroupOrder(self, groupOrder):
        self.friend.groupOrder = groupOrder
        self._refreshFriendListWithoutIcon()

    def movedToFriendGroup(self, gbId, group):
        fVal = self.friend.get(gbId)
        if fVal:
            fVal.group = group

    def friendOptionUpdated(self, option, checked):
        self.friend.setOption(option, checked)

    def _addTempMsg(self, gbId, type, msg):
        gamelog.debug('yedawang### _addTempMsg', gbId, type, msg)
        self.friend.tempMsgIdx += 1
        idx = self.friend.tempMsgIdx
        if self.friend.isSystemSpecialMsg(type):
            self.friend.tempMsgs.append((gbId,
             type,
             msg,
             idx))
            self.friend.tempMsgOther.append((idx, gbId, gameStrings.TEXT_IMPFRIEND_1037))
            gameglobal.rds.sound.playSound(gameglobal.SD_402)
        elif self.friend.isFriendAddMsg(type):
            for i in xrange(len(self.friend.tempMsgs)):
                tGbId, _type, msgs, _idx = self.friend.tempMsgs[i]
                if tGbId == gbId and _type == type:
                    self.friend.tempMsgs[i] = (gbId,
                     type,
                     msg,
                     _idx)
                    break
            else:
                self.friend.tempMsgs.append((gbId,
                 type,
                 msg,
                 idx))
                self.friend.tempMsgOther.append((idx, gbId, gametypes.FRIEND_ADD_MSG_DESC))
                gameglobal.rds.sound.playSound(gameglobal.SD_402)

        elif type == gametypes.FRIEND_MSG_TYPE_DEL_ENEMY:
            for i in xrange(len(self.friend.tempMsgs)):
                tGbId, _type, msgs, _idx = self.friend.tempMsgs[i]
                if tGbId == gbId and _type == type:
                    self.friend.tempMsgs[i] = (gbId,
                     type,
                     msg,
                     _idx)
                    break
            else:
                self.friend.tempMsgs.append((gbId,
                 type,
                 msg,
                 idx))
                self.friend.tempMsgOther.append((idx, gbId, gameStrings.TEXT_IMPFRIEND_1037))
                gameglobal.rds.sound.playSound(gameglobal.SD_402)

        elif type == gametypes.NPC_FRIEND_MSG_TYPE:
            for tGbId, _type, msgs, _idx in self.friend.tempMsgs:
                if tGbId == gbId and _type == type:
                    msgs.append(msg)
                    self.friend.tempMsgCount[gbId] = len(msgs)
                    self.friend.updateMsgChatIdx(idx, gbId, gameStrings.TEXT_IMPFRIEND_1037)
                    break
            else:
                self.friend.tempMsgs.append((gbId,
                 type,
                 [msg],
                 idx))
                self.friend.tempMsgCount[gbId] = idx
                self.friend.tempMsgOther.append((idx, gbId, gameStrings.TEXT_IMPFRIEND_1037))

            self._refreshFriendList()
        elif type == gametypes.FRIEND_MSG_TYPE_CHAT:
            for tGbId, _type, msgs, _idx in self.friend.tempMsgs:
                if tGbId == gbId and _type == type:
                    msgs.append(msg)
                    self.friend.tempMsgCount[gbId] = len(msgs)
                    self.friend.updateMsgChatIdx(0, gbId, msg.get('name', ''))
                    break
            else:
                self.friend.tempMsgs.append((gbId,
                 type,
                 [msg],
                 0))
                self.friend.tempMsgChat.append((0, gbId, msg.get('name', '')))
                self.friend.tempMsgCount[gbId] = 1

            self._refreshFriendList()
            if gameglobal.rds.ui.groupChat.widget:
                gameglobal.rds.ui.groupChat.updateItemMsgsCount(gbId, msg, False)
                gameglobal.rds.ui.groupChat.updateInGroupChatData(gbId, None)
                gameglobal.rds.ui.groupChat.refreshInfo()
        elif type == gametypes.FRIEND_MSG_TYPE_SYSTEM_NOTIFY:
            for tGbId, _type, msgs, _idx in self.friend.tempMsgs:
                if tGbId == gbId and _type == type:
                    msgs.append(msg)
                    self.friend.tempMsgCount[gbId] = len(msgs)
                    self.friend.updateMsgChatIdx(0, gbId, msg.get('name', ''))
                    break
            else:
                self.friend.tempMsgs.append((gbId,
                 type,
                 [msg],
                 0))
                self.friend.tempMsgChat.append((0, gbId, msg.get('name', '')))
                self.friend.tempMsgCount[gbId] = 1

            if gameglobal.rds.ui.groupChat.widget:
                gameglobal.rds.ui.groupChat.updateItemMsgsCount(gbId, msg, False)
                gameglobal.rds.ui.groupChat.updateInGroupChatData(gbId, None)
                gameglobal.rds.ui.groupChat.refreshInfo()
            self._refreshFriendList()
        else:
            return
        self._checkBlink()

    def _checkBlink(self):
        friendTmpMsg = bool(self.friend.tempMsgs)
        groupChatTempMsg = False
        if self.groupUnreadMsgs:
            for nuId, msgs in self.groupUnreadMsgs.iteritems():
                chatData = self.groupChatData.get(nuId)
                try:
                    acceptOp = chatData['members'][self.gbId][3]
                except:
                    acceptOp = False

                if acceptOp:
                    continue
                if len(msgs) > 0:
                    groupChatTempMsg = True

        gameglobal.rds.ui.systemButton.showFriendShine(friendTmpMsg or groupChatTempMsg)

    def _createChatMsg(self, gbId, role, school, sex, msg, when = None, photo = None):
        if not when:
            when = utils.getNow()
        ent = self if gbId == self.gbId else self.getFValByGbId(gbId)
        return {'name': role,
         'time': when,
         'msg': msg,
         'photo': photo or self._getFriendPhoto(ent, school, sex),
         'isMe': gbId == self.gbId,
         'photoBorderIcon': self._getFriendPhotoBorderIcon(ent)}

    def _createFriendData(self, fVal):
        descValue = fVal.signature
        if not fVal.showsig:
            descValue = gameglobal.rds.ui.friend._getLastPlace(fVal.spaceNo, fVal.areaId)
        return {'id': str(fVal.gbId),
         'name': fVal.name,
         'photo': self._getFriendPhoto(fVal),
         'signature': descValue,
         'state': fVal.state,
         'yixinOpenId': fVal.yixinOpenId,
         'fullName': fVal.getFullName(),
         'photoBorderIcon': self.getPhotoBorderIcon(fVal.borderId, uiConst.PHOTO_BORDER_ICON_SIZE40),
         'level': fVal.level,
         'school': fVal.school}

    def _createNpcFriendData(self, npcInfo):
        descValue = ''
        return {'id': str(npcInfo['id']),
         'name': npcInfo['name'],
         'photo': npcInfo['headIcon'],
         'signature': descValue,
         'state': 1,
         'yixinOpenId': 0,
         'fullName': npcInfo['name'],
         'photoBorderIcon': npcInfo['borderImg'],
         'level': '',
         'school': 0,
         'npcId': npcInfo['npcId']}

    def createNpcChatMsg(self, npcId, msg):
        cfgData = NND.data.get(npcId, {})
        role = uiUtils.getNpcName(npcId)
        when = utils.getNow()
        photo = uiUtils.getPNpcIcon(npcId)
        return {'name': role,
         'time': when,
         'msg': msg,
         'photo': photo,
         'isMe': 0,
         'photoBorderIcon': self.getPhotoBorderIcon(cfgData.get('borderId', 1), uiConst.PHOTO_BORDER_ICON_SIZE40)}

    def _createSystemNotifyData(self):
        time = utils.getNow()
        return {'id': str(const.FRIEND_SYSTEM_NOTIFY_ID),
         'time': time,
         'name': gameStrings.SYSTEM_MESSAGE_FRIEND_NAME,
         'state': 1}

    def chatFromFriend(self, gbId, role, school, sex, photo, msg, tWhen):
        if not gameglobal.rds.ui.friend.inited and not self.friend:
            if gameglobal.rds.ui.friend.messagesBeforeInit != None:
                gameglobal.rds.ui.friend.messagesBeforeInit.append((self.chatFromFriend, (gbId,
                  role,
                  school,
                  sex,
                  photo,
                  msg,
                  tWhen)))
            return
        else:
            if not utils.isRedPacket(msg):
                if not self.inWorld:
                    return
                if self.friend.isBlock(gbId):
                    return
                isNormal, msg = taboo.checkDisbWord(msg)
                if not isNormal:
                    return
                isNormal, msg = taboo.checkBSingle(msg)
            self.addRecentFriend(gbId)
            m = self._createChatMsg(gbId, role, school, sex, msg, tWhen, photo=photo)
            if gameglobal.rds.ui.chatToFriend.isOpened(gbId):
                gameglobal.rds.ui.chatToFriend.receiveMsg(gbId, m)
            elif gameglobal.rds.ui.groupChat.checkCurrentChated(gbId):
                gameglobal.rds.ui.groupChat.addMsgByPlayer(gbId, m, isSave=True)
            else:
                self._addTempMsg(gbId, gametypes.FRIEND_MSG_TYPE_CHAT, m)
                gameglobal.rds.ui.friend.minChatShine(gbId, True)
            self.chatDB.saveMsg(gbId, role, role, False, m['photo'], msg, m['time'])
            gameglobal.rds.sound.playSound(gameglobal.SD_403)
            return

    def chatFromXinyiManager(self, msg):
        self.chatFromMe(const.XINYI_MANAGER_ID, '', msg, utils.getNow())

    def chatFromMe(self, gbId, role, msg, tWhen):
        isNormal, msg = taboo.checkDisbWord(msg)
        if not isNormal:
            return
        isNormal, msg = taboo.checkBSingle(msg)
        fVal = self.friend.get(gbId)
        if fVal:
            self.addRecentFriend(gbId)
        if gameglobal.rds.ui.chatToFriend.isOpened(gbId):
            m = self._createChatMsg(self.gbId, self.roleName, self.physique.school, self.physique.sex, msg, tWhen)
            gameglobal.rds.ui.chatToFriend.receiveMsg(gbId, m)
            self.chatSaveMsg(gbId, role, msg, m)
        elif gameglobal.rds.ui.groupChat.checkCurrentChated(gbId):
            m = self._createChatMsg(self.gbId, self.roleName, self.physique.school, self.physique.sex, msg, tWhen)
            gameglobal.rds.ui.groupChat.addMsgByPlayer(gbId, m, isSave=True)
            self.chatSaveMsg(gbId, role, msg, m)

    def chatSaveMsg(self, gbId, role, msg, m):
        if not gbId == const.XINYI_MANAGER_ID:
            self.chatDB.saveMsg(gbId, role, self.roleName, True, m['photo'], msg, m['time'])
        else:
            self.chatDB.saveMsg(gbId, self.xinYiManager['name'], self.xinYiManager['name'], True, self.getXinYiMsgPhoto(), msg, m['time'])

    def chatFromGroup(self, groupId, msg, tWhen):
        if not gameglobal.rds.ui.friend.inited and not self.friend:
            if gameglobal.rds.ui.friend.messagesBeforeInit != None:
                gameglobal.rds.ui.friend.messagesBeforeInit.append((self.chatFromGroup, (groupId, msg, tWhen)))
            return
        elif not self.inWorld:
            return
        else:
            isNormal, msg = taboo.checkDisbWord(msg)
            if not isNormal:
                return
            isNormal, msg = taboo.checkBSingle(msg)
            if isNormal and gameglobal.rds.ui.chatToFriend.isGroupOpened(groupId):
                m = self._createChatMsg(self.gbId, self.roleName, self.physique.school, self.physique.sex, msg, tWhen)
                gameglobal.rds.ui.chatToFriend.groupReceiveMsg(groupId, m, tWhen)
            for friend in self.friend.getGroupMembers(groupId):
                if friend.state == gametypes.FRIEND_STATE_ONLINE and not gameglobal.rds.ui.chatToFriend.isOpened(friend.gbId):
                    m = self._createChatMsg(self.gbId, self.roleName, self.physique.school, self.physique.sex, msg, tWhen)
                    self.chatDB.saveMsg(friend.gbId, friend.name, self.roleName, True, m['photo'], msg, m['time'])

            return

    def chatFromSystem(self, when, mtype, msg):
        if not len(self.friend):
            return
        gbId = const.FRIEND_SYSTEM_ID
        fVal = self.friend.get(gbId)
        if mtype == gametypes.FRIEND_MSG_TYPE_PROMPT:
            m = self._createChatMsg(gbId, fVal.name, fVal.school, fVal.sex, msg, when)
            self._addTempMsg(gbId, mtype, m)
            return
        msg = '<FONT color=\"#FFFFFF\">' + msg + '</FONT>'
        m = self._createChatMsg(gbId, fVal.name, fVal.school, fVal.sex, msg, when)
        if gameglobal.rds.ui.chatToFriend.isOpened(gbId):
            gameglobal.rds.ui.chatToFriend.receiveMsg(gbId, m)
        else:
            if mtype == gametypes.FRIEND_MSG_TYPE_SYSTEM:
                mtype = gametypes.FRIEND_MSG_TYPE_CHAT
            self._addTempMsg(gbId, mtype, m)
            gameglobal.rds.ui.friend.minChatShine(gbId, True)
        self.chatDB.saveMsg(gbId, fVal.name, fVal.name, False, m['photo'], msg, when)
        gameglobal.rds.sound.playSound(gameglobal.SD_403)

    def chatFromSystemNotify(self, gbId, msgId, createdTime, args):
        self.chatDB.saveSysMsg(gbId, msgId, createdTime, args)
        gameglobal.rds.ui.systemMessage.reocrdSystemNewMsg(msgId, createdTime)
        if gameglobal.rds.ui.systemMessage.widget:
            gameglobal.rds.ui.systemMessage.appendNewSystemNotifyMsg()
        elif gameglobal.rds.ui.groupChat.checkCurrentChated(const.FRIEND_SYSTEM_NOTIFY_ID):
            gameglobal.rds.ui.groupChat.appendNewSystemNotifyMsg()
        else:
            self._addTempMsg(const.FRIEND_SYSTEM_NOTIFY_ID, gametypes.FRIEND_MSG_TYPE_SYSTEM_NOTIFY, {'name': gameStrings.SYSTEM_MESSAGE_FRIEND_NAME})
            self.addRecentFriend(const.FRIEND_SYSTEM_NOTIFY_ID)
            gameglobal.rds.ui.friend.minChatShine(const.FRIEND_SYSTEM_NOTIFY_ID, True)

    def fetchSystemNotifyHistory(self, gbId, offset = 0, limit = 0):
        if not limit:
            limit = const.CHAT_HISTORY_LIMIT
        if gbId != const.XINYI_MANAGER_ID:
            self.chatDB.getSysMsgs(gbId, offset, limit, lambda results, gbId = gbId, offset = offset, limit = limit: self._onGetSystemNotifyHistory(gbId, results[0], results[1], offset, limit))

    def _onGetSystemNotifyHistory(self, gbId, msgs, total, offset, limit):
        tMsgs = []
        for m in msgs:
            msgId, createdTime, args = m
            tMsgs.append({'msgId': msgId,
             'time': createdTime,
             'args': args})

        gameglobal.rds.ui.systemMessage.appendSystemNotifyHistoryMsg(gbId, tMsgs, total, offset, limit)
        return tMsgs

    def handleFriendMsg(self, idx, gbId):
        gamelog.debug('yedawang### handleFriendMsg', idx, gbId)
        if idx == 0 and gbId == 0:
            if gameglobal.rds.ui.friendRequest.checkNewFriendRequest():
                gameglobal.rds.ui.friendRequest.show()
                return True
        if not self.friend.tempMsgs:
            return False
        else:
            if idx == 0 and gbId == 0:
                if len(self.friend.tempMsgOther) > 0:
                    idx = self.friend.tempMsgOther[-1][0]
                    gbId = self.friend.tempMsgOther[-1][1]
                elif len(self.friend.tempMsgChat) > 0:
                    idx = self.friend.tempMsgChat[-1][0]
                    gbId = self.friend.tempMsgChat[-1][1]
                else:
                    return False
            tempIdx = -1
            if idx > 0:
                for _idx, _gbId, _ in self.friend.tempMsgOther:
                    tempIdx += 1
                    if _idx == idx:
                        self.friend.tempMsgOther.pop(tempIdx)
                        break

            else:
                for _idx, _gbId, _ in self.friend.tempMsgChat:
                    tempIdx += 1
                    if _gbId == gbId:
                        self.friend.tempMsgChat.pop(tempIdx)
                        break

            for tempIdx, tempInfo in enumerate(self.friend.tempMsgs):
                _gbId, type, msgs, _idx = tempInfo
                if _gbId == gbId and _idx == idx:
                    if type == gametypes.FRIEND_MSG_TYPE_ADD or type == gametypes.FRIEND_MSG_TYPE_OFFLINE_ADD:
                        self._showFriendAddedMsg(gbId, msgs.get('roleName', ''), type)
                    if type == gametypes.FRIEND_MSG_TYPE_DEL_ENEMY:
                        group, opNuid = msgs
                        self._showDeleteEnemyPrompt(gbId, group, opNuid)
                    elif type == gametypes.FRIEND_MSG_TYPE_PROMPT:
                        self._showPromptMsg(msgs['msg'])
                    elif type == gametypes.FRIEND_MSG_TYPE_CHAT:
                        if gameglobal.rds.ui.chatToFriend.isOpened(gbId):
                            for msg in msgs:
                                gameglobal.rds.ui.chatToFriend.receiveMsg(gbId, msg)

                            self.friend.tempMsgCount.pop(gbId, None)
                        elif gameglobal.rds.ui.groupChat.checkCurrentChated(gbId):
                            for msg in msgs:
                                gameglobal.rds.ui.groupChat.addMsgByPlayer(gbId, msg)

                            self.friend.tempMsgCount.pop(gbId, None)
                        elif gbId != const.XINYI_MANAGER_ID:
                            fVal = self.getFValByGbId(gbId)
                            if not fVal:
                                if self._isSoul():
                                    if msgs:
                                        msg = msgs[0]
                                        gfxData = {'id': str(gbId),
                                         'name': msg.get('name', ''),
                                         'photo': msg.get('photo', ''),
                                         'signature': '',
                                         'state': 1,
                                         'yixinOpenId': 0}
                                        gameglobal.rds.ui.chatToFriend.show(msgs, gfxData, False)
                                        gameglobal.rds.ui.friend.removeMinChat(gbId)
                                else:
                                    self.friend.tempMsgsAsync.append((gbId,
                                     type,
                                     msgs,
                                     0))
                                    self.addRecentFriend(gbId)
                            else:
                                gameglobal.rds.ui.chatToFriend.show(msgs, self._createFriendData(fVal), False, True)
                                gameglobal.rds.ui.friend.removeMinChat(gbId)
                            self.friend.tempMsgCount.pop(gbId, None)
                        else:
                            gameglobal.rds.ui.chatToFriend.show(msgs, gameglobal.rds.ui.friend.createXinYiManagerData(), False)
                            gameglobal.rds.ui.friend.removeMinChat(gbId)
                            self.friend.tempMsgCount.pop(gbId, None)
                        self._refreshFriendList()
                    elif type == gametypes.FRIEND_MSG_TYPE_SYSTEM_NOTIFY:
                        gameglobal.rds.ui.systemMessage.show()
                        gameglobal.rds.ui.friend.removeMinChat(gbId)
                        self.friend.tempMsgCount.pop(gbId, None)
                        self._refreshFriendList()
                    elif type == gametypes.NPC_FRIEND_MSG_TYPE:
                        self.npcFavor.npcMsgDic[_gbId] = msgs
                        gameglobal.rds.ui.friend.beginChat(const.FRIEND_NPC_ID, gbId)
                        self.friend.tempMsgCount.pop(gbId, None)
                    if self.friend.tempMsgs:
                        if tempInfo in self.friend.tempMsgs:
                            self.friend.tempMsgs.remove(tempInfo)
                    break
            else:
                return False

            self._checkBlink()
            return True

    def handleAcceptFriendMsg(self):
        if gameglobal.rds.ui.friendRequest.checkNewFriendRequest():
            gameglobal.rds.ui.friendRequest.show()
        if not self.friend.tempMsgs:
            return
        for gbId, type, msgs, _idx in self.friend.tempMsgs:
            if type == gametypes.FRIEND_MSG_TYPE_ADD or type == gametypes.FRIEND_MSG_TYPE_OFFLINE_ADD:
                self._showFriendAddedMsg(gbId, msgs.get('roleName', ''), type)
            if type == gametypes.FRIEND_MSG_TYPE_DEL_ENEMY:
                group, opNuid = msgs
                self._showDeleteEnemyPrompt(gbId, group, opNuid)
            elif type == gametypes.FRIEND_MSG_TYPE_PROMPT:
                self._showPromptMsg(msgs['msg'])
            elif type == gametypes.FRIEND_MSG_TYPE_CHAT:
                if gameglobal.rds.ui.chatToFriend.isOpened(gbId):
                    for msg in msgs:
                        gameglobal.rds.ui.chatToFriend.receiveMsg(gbId, msg)

                elif gbId != const.XINYI_MANAGER_ID:
                    fVal = self.getFValByGbId(gbId)
                    if not fVal:
                        self.friend.tempMsgsAsync.append((gbId,
                         type,
                         msgs,
                         0))
                        self.addRecentFriend(gbId)
                    else:
                        gameglobal.rds.ui.chatToFriend.show(msgs, self._createFriendData(fVal), False)
                        gameglobal.rds.ui.friend.removeMinChat(gbId)
                elif self.xinYiManager:
                    gameglobal.rds.ui.chatToFriend.show(msgs, gameglobal.rds.ui.friend.createXinYiManagerData(), False)
                    gameglobal.rds.ui.friend.removeMinChat(gbId)

        self.friend.clearTempMsg()
        self._refreshFriendList()
        self._checkBlink()

    def handleIgnoreFriendMsg(self):
        for gbId, type, msgs, idx in self.friend.tempMsgs:
            gameglobal.rds.ui.friend.minChatShine(gbId, False)

        self.friend.clearTempMsg()
        gameglobal.rds.ui.friendRequest.onClearRequest()
        self._refreshFriendList()
        self._checkBlink()

    def handleFriendMsgAsync(self, gbId):
        tempIdx = -1
        for _gbId, type, msgs, _idx in self.friend.tempMsgsAsync:
            tempIdx += 1
            if _gbId == gbId:
                if gameglobal.rds.ui.chatToFriend.isOpened(gbId):
                    for msg in msgs:
                        gameglobal.rds.ui.chatToFriend.receiveMsg(gbId, msg)

                else:
                    fVal = self.getFValByGbId(gbId)
                    if not fVal:
                        return
                    gameglobal.rds.ui.chatToFriend.show(msgs, self._createFriendData(fVal), False)
                    gameglobal.rds.ui.friend.removeMinChat(gbId)
                self.friend.tempMsgsAsync.pop(tempIdx)
                break

    def handleOfflineSystemNotifies(self, msgs):
        if not gameglobal.rds.configData.get('enableSystemMessage', False):
            return
        if not msgs:
            return
        if not self.chatDB:
            return
        d = []
        for tWhen, mdata in msgs:
            msgId, args = cPickle.loads(mdata)
            d.append((msgId, tWhen, args))
            gameglobal.rds.ui.systemMessage.reocrdSystemNewMsg(msgId, tWhen)
            self._addTempMsg(const.FRIEND_SYSTEM_NOTIFY_ID, gametypes.FRIEND_MSG_TYPE_SYSTEM_NOTIFY, {'name': gameStrings.SYSTEM_MESSAGE_FRIEND_NAME})

        self.chatDB.saveSysMsgs(self.gbId, d)

    def friendStateUpdated(self, gbId, state):
        if gbId == self.gbId:
            self.friend.updateMyState(state)
            gameglobal.rds.ui.friend.updateState(state)
        elif self.friend.updateState(gbId, state):
            self._refreshFriendList()
            fVal = self.getFValByGbId(gbId)
            data = self._createFriendData(fVal)
            gameglobal.rds.ui.chatToFriend.updateStatus(gbId, data)
            gameglobal.rds.ui.groupChat.onUpdataFriendInfo(gbId)

    def friendSignatureUpdated(self, gbId, signature):
        if gbId == self.gbId:
            self.friend.updateMySignature(signature)
            gameglobal.rds.ui.friend.updateSignature(signature)
        elif self.friend.updateSignature(gbId, signature):
            self._refreshFriendList()

    def friendShowsigUpdated(self, gbId, showsig):
        if gbId == self.gbId:
            self.friend.updateMyShowsig(showsig)
            gameglobal.rds.ui.friend.setShowsig(showsig)
        elif self.friend.updateShowsig(gbId, showsig):
            self._refreshFriendList()

    def friendIntimacyTgtUpdated(self, gbId, intimacyTgt):
        if gbId == self.gbId:
            if self.friend.intimacyTgt > 0 and intimacyTgt == 0:
                self.onQuestInfoModifiedAtClient(const.QD_JIEQI, exData={'refreshAll': 1})
                self.intimacyEvent = IntimacyEvent()
            self.friend.updateIntimacyTgt(self, intimacyTgt)

    def friendLevelUpdated(self, gbId, level):
        self.friend.updateLevel(gbId, level)
        self._refreshFriendListWithoutIcon()

    def friendSpaceNoUpdated(self, gbId, spaceNo):
        return self.friend.updateSpaceNo(gbId, spaceNo)

    def friendAreaIdUpdated(self, gbId, spaceNo, areaId):
        return self.friend.updateAreaId(gbId, spaceNo, areaId)

    def friendPhotoUpdated(self, gbId, photo):
        res = self.friend.updatePhoto(gbId, photo)
        if res:
            self._refreshFriendList()
        return res

    def friendSexUpdated(self, gbId, sex):
        res = self.friend.updateSex(gbId, sex)
        if res:
            self._refreshFriendList()
        return res

    def friendYixinUpdated(self, gbId, yixinOpenId):
        res = self.friend.updateYixinStatus(gbId, yixinOpenId)
        if res:
            self._refreshFriendList()
        return res

    def friendFlowbackUpdated(self, gbId, flowbackType):
        fVal = self.getFValByGbId(gbId)
        if fVal:
            oldFlowbackType = fVal.flowbackType
            if not oldFlowbackType and flowbackType:
                self.notifyFlowbackAvatarAvail(fVal)
        res = self.friend.updateFlowbackType(gbId, flowbackType)
        if res:
            self._refreshFriendList()
        return res

    def friendMingpaiUpdated(self, gbId, mingpaiId):
        res = self.friend.updateMingpaiId(gbId, mingpaiId)
        if res:
            self._refreshFriendList()
        return res

    def friendActivityDictUpdated(self, gbId, activityDict):
        self.friend.updateActivityDict(gbId, activityDict)

    def _getTempFriends(self):
        r = []
        for fVal in self.friend.itervalues():
            if fVal.temp:
                r.append(fVal)

        return fVal

    def _getTempFriendsCount(self):
        cnt = 0
        for fVal in self.friend.itervalues():
            if fVal.temp:
                cnt += 1

        return cnt

    def _getFirstTempFriend(self):
        r = None
        for fVal in self.friend.itervalues():
            if fVal.temp and (not r or fVal.time < r.time):
                r = fVal

        return fVal

    def _removeFirstTempFriend(self):
        fVal = self._getFirstTempFriend()
        if fVal:
            fVal.temp = False

    def _getRecentFriends(self):
        r = []
        for fVal in self.friend.itervalues():
            if fVal.recent:
                r.append(fVal)

        return fVal

    def _getRecentFriendsCount(self):
        cnt = 0
        for fVal in self.friend.itervalues():
            if fVal.recent:
                cnt += 1

        return cnt

    def _getFirstRecentFriend(self):
        r = None
        for fVal in self.friend.itervalues():
            if fVal.recent and (not r or fVal.time < r.time):
                r = fVal

        return fVal

    def _removeFirstRecentFriend(self):
        fVal = self._getFirstRecentFriend()
        if fVal:
            fVal.recent = False

    def onQueryTempFriend(self, gbId, status):
        fVal = self.friend.get(gbId, None)
        if fVal:
            fVal.state = status
            self._refreshFriendList()
            data = self._createFriendData(fVal)
            gameglobal.rds.ui.chatToFriend.updateStatus(gbId, data)

    def addTempFriend(self, role, useForMsgBoard = False):
        return
        if role == self.roleName:
            return False
        fVal = self.friend.findByRole(role)
        if fVal:
            if self.friend.isFriend(fVal.gbId):
                return False
            if not fVal.temp:
                if self._getTempFriendsCount() >= const.FRIEND_TEMP_MAX:
                    self._removeFirstTempFriend()
                fVal.temp = True
                fVal.time = utils.getNow()
                self._refreshFriendList()
                return True
        elif not self.friend.temp.has_key(role):
            if useForMsgBoard:
                self.base.addTempFriendByMsgBoard(role)
            else:
                self.friend.temp[role] = True
                self.base.addTempFriend(role)
            return False

    def addRecentFriend(self, gbId):
        fVal = self.friend.get(gbId, None)
        if fVal or gbId == const.FRIEND_SYSTEM_NOTIFY_ID:
            self.base.addRecentFriendByGbId(gbId)
        elif not self.friend.temp.has_key(gbId):
            self.friend.temp[gbId] = True
            self.base.addContactByGbId(gbId, gametypes.FRIEND_GROUP_TEMP, 0)

    def _refreshFriendList(self, tabName = None):
        gameglobal.rds.ui.friend.refreshFriendList(None, tabName)
        gameglobal.rds.ui.tianyuMall.refreshFriendList()
        gameglobal.rds.ui.mail.refreshFriendList()
        gameglobal.rds.ui.summonFriend.refreshWidget()
        gameglobal.rds.ui.summonFriendNew.refreshWidget()
        gameglobal.rds.ui.summonFriendBGV2.refreshInfo()

    def _refreshFriendListWithoutIcon(self, tabName = None):
        gameglobal.rds.ui.friend.refreshFriendListWithoutIcon(None, tabName)

    def _getFriendPhoto(self, owner, school = 3, sex = 0):
        if owner == None:
            return 'headIcon/%s.dds' % str(school * 10 + sex)
        else:
            if owner == self:
                if owner.friend.photo:
                    return owner.friend.photo
                else:
                    return 'headIcon/%s.dds' % str(owner.school * 10 + owner.physique.sex)
            else:
                if owner.photo:
                    return owner.photo
                if owner.school and owner.sex:
                    return 'headIcon/%s.dds' % str(owner.school * 10 + owner.sex)
                return 'headIcon/%s.dds' % str(school * 10 + sex)
            return

    def _getFriendPhotoBorderIcon(self, owner, picSize = uiConst.PHOTO_BORDER_ICON_SIZE40):
        if owner == None:
            return self.getPhotoBorderIcon()
        elif owner == self:
            return self.getPhotoBorderIcon(self.photoBorder.borderId, picSize)
        else:
            return self.getPhotoBorderIcon(owner.borderId, picSize)

    def getPhotoBorderIcon(self, borderId = 0, picSize = uiConst.PHOTO_BORDER_ICON_SIZE40):
        if not borderId:
            return ''
        iconId = PBD.data.get(borderId, {}).get('iconId', '')
        iconPath = 'touxiangkuangIcon/%s/%s.dds' % (str(picSize), str(iconId))
        return iconPath

    def fetchChatHistory(self, gbId, offset = 0, limit = 0, npcPid = 0):
        if not limit:
            limit = const.CHAT_HISTORY_LIMIT
        if npcPid != 0:
            self.chatDB.getNpcMsgs(self.gbId, npcPid, offset, limit, lambda results, gbId = gbId, offset = offset, limit = limit: self._onGetChatHistory(gbId, results[0], results[1], offset, limit, 1))
            return
        if gbId != const.XINYI_MANAGER_ID:
            fVal = self.getFValByGbId(gbId)
            if not fVal:
                return
            self.chatDB.getMsgs(gbId, fVal.name, offset, limit, lambda results, gbId = gbId, offset = offset, limit = limit: self._onGetChatHistory(gbId, results[0], results[1], offset, limit, fVal.borderId))
        elif self.xinYiManager:
            self.chatDB.getMsgs(gbId, self.xinYiManager['name'], offset, limit, lambda results, gbId = gbId, offset = offset, limit = limit: self._onGetChatHistory(gbId, results[0], results[1], offset, limit, fVal.borderId))

    def _onGetChatHistory(self, gbId, msgs, total, offset, limit, borderId):
        if msgs:
            tMsgs = []
            for m in msgs:
                _, name, isMe, photo, msg, createdTime = m
                if photo:
                    tMsgs.append({'name': name,
                     'time': createdTime,
                     'msg': msg.encode(utils.defaultEncoding()),
                     'photo': photo.decode(utils.defaultEncoding()),
                     'isMe': isMe,
                     'photoBorderIcon': self.getPhotoBorderIcon(borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)})
                else:
                    tMsgs.append({'name': name,
                     'time': createdTime,
                     'msg': msg.encode(utils.defaultEncoding()),
                     'photo': '',
                     'isMe': isMe,
                     'photoBorderIcon': self.getPhotoBorderIcon(borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)})

            gameglobal.rds.ui.chatToFriend.appendHistoryMsg(gbId, tMsgs, total, offset, limit)
            return tMsgs
        else:
            return []

    def fetchLastChatHistory(self, gbId, isSysHistory = False):
        offset = 0
        limit = 1
        if isSysHistory:
            if gbId != const.XINYI_MANAGER_ID:
                self.chatDB.getSysMsgs(gbId, offset, limit, lambda results: self.onFetchLastSysHistory(results[0]))
        elif gbId != const.XINYI_MANAGER_ID:
            fVal = self.getFValByGbId(gbId)
            if not fVal:
                return
            self.chatDB.getMsgs(gbId, fVal.name, offset, limit, lambda results: self.onFetchLastChatHistory(results[0]))
        elif self.xinYiManager:
            self.chatDB.getMsgs(gbId, self.xinYiManager['name'], offset, limit, lambda results: self.onFetchLastChatHistory(results[0]))

    def onFetchLastChatHistory(self, msgs):
        if not msgs:
            return
        lastMsg = msgs[0]
        gbId, name, isMe, _, msg, createdTime = lastMsg
        msgText = msg.encode(utils.defaultEncoding())
        gameglobal.rds.ui.friend.updateRecentData(gbId, msgText)

    def onFetchLastSysHistory(self, msgs):
        if not msgs:
            return
        lastMsg = msgs[-1]
        msgId, createdTime, args = lastMsg
        args = gameglobal.rds.ui.systemMessage.changeCoding(args)
        text = GMD.data.get(msgId, {}).get('text', '')
        msgText = ''
        try:
            msgText = self.formatMsg(text, args)
        except:
            gamelog.error('onFetchLastSysHistory: formatMsg error')

        gameglobal.rds.ui.friend.updateRecentData(const.FRIEND_SYSTEM_NOTIFY_ID, msgText)

    def removeFriend(self, gbId, group, cipher = ''):
        fVal = self.friend.get(gbId)
        if fVal:
            if group == gametypes.FRIEND_GROUP_FRIEND:
                if cipher != '':
                    self.base.deleteFriendWithCipher(gbId, cipher)
                else:
                    self.base.deleteFriend(gbId)
            elif self.friend.isBlockGroup(group):
                self.base.unblockFriend(gbId)
            elif self.friend.isEnemyGroup(group):
                self.base.deleteEnemy(gbId, 0)
            elif self.friend.isTempGroup(group):
                self.base.deleteFriend(gbId)

    def onSearchPlayer(self, infoList, usedFor):
        if usedFor == gametypes.SEARCH_PLAYER_FOR_FRIEND:
            self.onSearchFriend(infoList)
        elif usedFor == gametypes.SEARCH_PLAYER_FOR_ARMY_APPOINT:
            self.onSearchPlayerForArmyAppoint(infoList)

    def onSearchFriend(self, infoList):
        for i, d in enumerate(infoList):
            gbId, name, level, spaceNo, areaId, school, isOnline, photo, sex, combatScore = d
            if not photo:
                photo = self.friend.getDefaultPhoto(school, sex)
                if not isinstance(d, list):
                    d = list(d)
                    infoList[i] = d
                d[7] = photo

        if not gameglobal.rds.configData.get('enableRecommendFriend', False):
            gameglobal.rds.ui.friend.setSearchResult(infoList)
        else:
            gameglobal.rds.ui.recommendSearchFriend.setSearchResult(infoList)
        gameglobal.rds.ui.assassinationEnemy.setSearchResult(infoList)
        BigWorld.player().onSearchAssassinationTargetByRoleName(infoList)

    def filterRecommendTags(self, tagIds):
        if tagIds:
            tagIds = [ int(x) for x in tagIds ]
        else:
            tagIds = []
        tagIds.sort(key=lambda x: UPTD.data.get(x, {}).get('order', const.MAX_INT32))
        types = {}
        realTags = []
        for tagId in tagIds:
            data = UPTD.data.get(tagId)
            if not data:
                continue
            tp = data.get('type')
            if types.has_key(tp):
                continue
            types[tp] = True
            realTags.append(data.get('tag'))
            if len(realTags) >= MAX_TAG_DISPLAY_NUM:
                break

        return ' '.join(realTags)

    def onRecommendFriend(self, infoList):
        random.shuffle(infoList)
        for d in infoList:
            gbId, name, level, spaceNo, areaId, school, isOnline, photo, sex, tagIds = d
            if not photo:
                photo = self.friend.getDefaultPhoto(school, sex)
                d[7] = photo
            d[9] = self.filterRecommendTags(tagIds)

        gameglobal.rds.ui.recommendSearchFriend.setRecommendResult(infoList)

    def onRecommendFriendNotifyIfLittle(self):
        if not self.inWorld:
            return
        cnt = self.friend.getFriendCount()[0] + self.friend.getAcknowledgeFriendCount()[0]
        if cnt < SCD.data.get('recommendFriendLessThan', 5):
            self.onRecommendFriendNotify()

    def onRecommendFriendNotify(self):
        if not self.inWorld:
            return
        if not gameglobal.rds.configData.get('enableRecommendFriend', False):
            return
        gameglobal.rds.ui.recommendSearchFriend.showRecommendSearchFriendPush()

    def onAddAcknowledgeFriend(self, gbId):
        fVal = self.friend.get(gbId)
        if not fVal:
            return
        msg = self._createChatMsg(gbId, fVal.name, fVal.school, fVal.sex, gameStrings.TEXT_IMPFRIEND_1944 % fVal.name, utils.getNow())
        systemMsgProxy = gameglobal.rds.ui.systemMessage
        systemMsgProxy.appendTempSystemNotifyMsg(msg, GMDD.data.GROUP_CHAT_MANAGER_TRANSFER_ME)
        if systemMsgProxy.widget:
            systemMsgProxy.refreshInfo()
        else:
            self._addTempMsg(const.FRIEND_SYSTEM_NOTIFY_ID, gametypes.FRIEND_MSG_TYPE_SYSTEM_NOTIFY, {'name': gameStrings.SYSTEM_MESSAGE_FRIEND_NAME})
        sayHelloTxt = SCD.data.get('SAY_HELLO_TEXT', gameStrings.TEXT_IMPFRIEND_1952 % self.roleName)
        gameglobal.rds.ui.chatToFriend._sendMsgToFid(gbId, sayHelloTxt)

    def onReqDeleteEnemy(self, gbId, group, opNuid):
        self._addTempMsg(gbId, gametypes.FRIEND_MSG_TYPE_DEL_ENEMY, (group, opNuid))

    def checkFriendState(self):
        if not self.friend.getOption(gametypes.FRIEND_OPTION_AUTO_AWAY):
            return
        lastActionTime = BigWorld.get_last_input_time()
        now = BigWorld.time()
        idleTime = now - lastActionTime
        oldState = self.friend.state
        if oldState == gametypes.FRIEND_STATE_AWAY:
            if idleTime < const.FRIEND_AWAY_TIME:
                self.base.updateFriendState(self.friend.oldState)
        elif idleTime > const.FRIEND_AWAY_TIME:
            self.friend.oldState = oldState
            self.base.updateFriendState(gametypes.FRIEND_STATE_AWAY)

    def onOpenActivateOldFriend(self, npcId, oldPlayerNames, oldFriendActive, data):
        pass

    def onGetOldFriendList(self, oldPlayerName, data):
        pass

    def updateOldFriendActive(self, oldFriendActive):
        self.friend.oldFriendActive = oldFriendActive

    def onProfileUpdate(self, data):
        pvisibility, photo, constellation, birthmonth, birthday, sex, bloodType, province, city, qq, description, onlineTime = data
        self.friend.pvisibility = pvisibility
        self.friend.photo = photo
        self.friend.constellation = constellation
        self.friend.birthmonth = birthmonth
        self.friend.birthday = birthday
        self.friend.sex = sex
        self.friend.bloodType = bloodType
        self.friend.province = province
        self.friend.city = city
        self.friend.qq = qq
        self.friend.description = description
        self.friend.onlineTime = onlineTime
        imagePath = 'headIcon/%s.dds' % str(self.school * 10 + self.physique.sex)
        if photo != '':
            BigWorld.callback(1, Functor(self.downloadNOSFile, const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, gameglobal.rds.ui.friend.onDownloadPhoto, (None,)))
        else:
            gameglobal.rds.ui.friend.refreshRoleIcon(imagePath)

    def onViewFriendProfile(self, gbId, data):
        gameglobal.rds.ui.friend.showOtherProfile(gbId, data)

    def refreshUserDefineStatus(self, refreshIcon = False):
        if refreshIcon:
            photoPath = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + BigWorld.player().profileIcon + '.dds'
            gameglobal.rds.ui.friend.refreshIcon(photoPath)

    def onQueryPlayerLocation(self, playerName, spaceNo, mapAreaId, chunkName, position, error):
        gameglobal.rds.ui.queryLocation.setQueryResutl(spaceNo, mapAreaId, chunkName, position, error)

    def onSyncXinYiManagerInfo(self, info):
        old = self.xinYiManager
        self.xinYiManager = info
        if not old and self.xinYiManager:
            BigWorld.player().showGameMsg(GMDD.data.XINYI_MANAGER_ADD, self.xinYiManager['name'])
        gameglobal.rds.ui.friend.refreshFriendList()
        if not self.xinYiManager:
            gameglobal.rds.ui.friend.removeMinChat(const.XINYI_MANAGER_ID)
            gameglobal.rds.ui.chatToFriend.closeChatByFid(const.XINYI_MANAGER_ID)
            return
        data = gameglobal.rds.ui.friend.createXinYiManagerData()
        if data:
            gameglobal.rds.ui.chatToFriend.updateStatus(const.XINYI_MANAGER_ID, data)

    def onXinyiManagerOfflineMsg(self):
        returnMsg = uiUtils.getTextFromGMD(GMDD.data.RETURN_XINYI_MSG, gameStrings.TEXT_IMPFRIEND_2040)
        BigWorld.player().chatFromXinYi(returnMsg)

    def notifyFlowbackAvatarAvail(self, fVal):
        pass

    def pushFlowbackFriendOnline(self, gbId, lostTime):
        gameglobal.rds.ui.friendFlowBack.setFlowBackData(lostTime, gbId)

    def pushFlowbackFriendOnlineSuccess(self, gbId):
        pass

    def onLoadGlobalFriends(self, friends):
        self.globalFriends = friends

    def globalFriendInfoUpdate(self, gbId, info):
        if hasattr(self, 'globalFriends'):
            self.globalFriends.friends[gbId] = info
            self._refreshFriendListWithoutIcon()

    def globalFriendAdd(self, info):
        if hasattr(self, 'globalFriends'):
            self.globalFriends.friends.addFriend(*info)
            self._refreshFriendList()

    def globalFriendDelete(self, gbId):
        if hasattr(self, 'globalFriends'):
            if gbId not in self.globalFriends.friends:
                return
            del self.globalFriends.friends[gbId]
            self._refreshFriendList()

    def onGlobalFriendChatTo(self, gbId, msg):
        gVal = self.getGlobalFriend(gbId)
        if not gVal:
            gamelog.error('@zhp onGlobalFriendChatTo not globalFriend id:%s' % gbId)
            return
        role = gVal.roleName
        school = gVal.extraInfo.get('school', 0)
        sex = gVal.extraInfo.get('sex', 0)
        photo = gVal.extraInfo.get('photo', '')
        tWhen = utils.getNow()
        self.chatFromFriend(gbId, role, school, sex, photo, msg, tWhen)

    def onApplyGlobalServerFriend(self, info):
        gbId = info.get('gbId', 0)
        self._addTempMsg(gbId, gametypes.FRIEND_MSG_TYPE_GLOBAL_SERVER_ADD, info)

    def onRequestAddGlobalFriendDeny(self, info):
        self.showGameMsg(GMDD.data.REQUEST_ADD_GLOBAL_FRIEND_DENY, (info.get('roleName', ''),))

    def onQueryGlobalFriendByName(self, players):
        if not gameglobal.rds.configData.get('enableRecommendFriend', False):
            gameglobal.rds.ui.friend.setSearchResult(players)
        else:
            gameglobal.rds.ui.recommendSearchFriend.setSearchResult(players)

    def onQueryFriendSocInfo(self, gbId, data):
        jingJie, socLv, junJieLv, qumoLv, arenaScore, combatScore, achievePoint, vipInfo, combatScoreTop10, renpinVal, sm_appearanceItemCollectPoint = data
        data = (jingJie,
         socLv,
         junJieLv,
         qumoLv,
         arenaScore,
         vipInfo,
         combatScoreTop10,
         combatScore,
         achievePoint,
         renpinVal,
         sm_appearanceItemCollectPoint)
        gamelog.debug('!!!onQueryFriendSocInfo', jingJie, socLv, junJieLv, qumoLv, arenaScore, vipInfo, combatScoreTop10, combatScore, achievePoint, renpinVal, sm_appearanceItemCollectPoint)
        gameglobal.rds.ui.friend.addFriendScoInfo(gbId, data)

    def getGlobalFriend(self, tgtGbId):
        if hasattr(self, 'globalFriends') and self.globalFriends:
            return self.globalFriends.friends.get(tgtGbId)

    def isGobalFirendGbId(self, tgtGbId):
        if hasattr(self, 'globalFriends') and self.globalFriends:
            return self.globalFriends.friends.has_key(tgtGbId)
        return False

    def isGlobalFriendVal(self, fVal):
        return fVal and fVal.group == gametypes.FRIEND_GROUP_GLOBAL_FRIEND

    def getFValByGbId(self, tgtGbId):
        if self.isGobalFirendGbId(tgtGbId):
            return uiUtils.globalFriend2FriendVal(self.getGlobalFriend(tgtGbId))
        else:
            return self.friend.get(tgtGbId, None)

    def getFriendGroupOrder(self):
        if not self.friend.groupOrder or gametypes.FRIEND_GROUP_FRIEND not in self.friend.groupOrder:
            groupOrder = filter(lambda g: self.friend.isOrderAbleGroup(g), self.friend.groups.keys())
        else:
            groupOrder = copy.deepcopy(self.friend.groupOrder)
            orderAbleGroup = filter(lambda g: self.friend.isOrderAbleGroup(g), self.friend.groups.keys())
            if sorted(orderAbleGroup) != sorted(groupOrder):
                for g in orderAbleGroup:
                    if g not in groupOrder:
                        groupOrder.append(g)

        if gameglobal.rds.ui.friend.enableGlobalFriend():
            if gametypes.FRIEND_GROUP_GLOBAL_FRIEND not in groupOrder:
                groupOrder.append(gametypes.FRIEND_GROUP_GLOBAL_FRIEND)
        return groupOrder

    def getMiniGameInviteGroup(self):
        groupOrder = []
        if not self.friend.groupOrder or gametypes.FRIEND_GROUP_FRIEND not in self.friend.groupOrder:
            groupOrder = filter(lambda g: self.friend.isOrderAbleGroup(g), self.friend.groups.keys())
        else:
            groupOrder = copy.deepcopy(self.friend.groupOrder)
            orderAbleGroup = filter(lambda g: self.friend.isOrderAbleGroup(g), self.friend.groups.keys())
            if sorted(orderAbleGroup) != sorted(groupOrder):
                for g in orderAbleGroup:
                    if g not in groupOrder:
                        groupOrder.append(g)

        return groupOrder

    def onGetRemotePlayerInfo(self, info):
        pass

    def onSendInvitationSucc(self, gbId):
        if gbId in self.inviteList:
            p = BigWorld.player()
            fVal = p.getFValByGbId(gbId)
            fName = fVal.name
            p.showGameMsg(GMDD.data.SEND_INVITATION_SUCC_MSG, (fName,))
            self.inviteList.remove(gbId)
            gameglobal.rds.ui.friend.refreshCallFriendsList(self.inviteList)
            gameglobal.rds.ui.summonFriendNew.refreshCallFriendsList(self.inviteList)
            gameglobal.rds.ui.summonFriendBackV2.refreshCallFriendsList(self.inviteList)

    def onSendInvitationFail(self, gbId):
        if gbId:
            p = BigWorld.player()
            fVal = p.getFValByGbId(gbId)
            fName = fVal.name
            p.showGameMsg(GMDD.data.SEND_INVITATION_FAIL_MSG, (fName,))

    def onLoadFlowbackInvitationList(self, inviteList, canPush):
        self.inviteList = inviteList
        gameglobal.rds.ui.friend.setInviteList(self.inviteList, canPush)
        gameglobal.rds.ui.summonFriendNew.setSummonFriendList(inviteList)
        gameglobal.rds.ui.summonFriendBackV2.setSummonFriendList(inviteList)

    def flowbackInviteStatsUpdated(self, stat):
        gameglobal.rds.ui.summonFriend.setSummonRewards(stat)

    def sendIntimacySkills(self, skills):
        gamelog.debug('zt: sendIntimacySkills', skills)
        for skill in skills:
            self.intimacySkills[skill['skillId']] = IntimacySkillVal(skill['skillId'], skill['nextTime'], skill['useCnt'])

    def updateIntimacySkill(self, skillInfoDict):
        for sid, skillInfo in skillInfoDict.iteritems():
            if not self.intimacySkills.has_key(sid):
                self.intimacySkills[sid] = IntimacySkillVal(sid, skillInfo['nextTime'], skillInfo['useCnt'])
                continue
            for attr, attrVal in skillInfo.iteritems():
                setattr(self.intimacySkills[sid], attr, attrVal)

        gameglobal.rds.ui.actionbar.updateSlots()
        gameglobal.rds.ui.skill.refreshIntimacyPanel()

    def pulledByIntimacy(self, skillId, args, spaceNo, position):
        if getattr(self, 'intimacyPullConfirm', 0):
            return
        msgText = gameStrings.TEXT_IMPFRIEND_2208
        msg = GMD.data.get(GMDD.data.INTIMACY_PULL_CONFIRM, {}).get('text', msgText)
        self.intimacyPullConfirm = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.onConfirmIntimacyPull, skillId, args, True), yesBtnText=gameStrings.TEXT_IMPFRIEND_2211, noCallback=Functor(self.onConfirmIntimacyPull, skillId, args, False), noBtnText=gameStrings.TEXT_IMPFRIEND_927)

    def onConfirmIntimacyPull(self, skillId, args, ok):
        self.intimacyPullConfirm = 0
        self.cell.confirmPulledByIntimacy(skillId, args, ok)

    def pulledByApprentice(self, skillId, args, spaceNo, position, name, gbId):
        if not hasattr(self, 'apprenticePullIds'):
            self.apprenticePullIds = []
        if gbId in self.apprenticePullIds:
            return
        msgText = gameStrings.TEXT_IMPFRIEND_2222 % name
        msg = GMD.data.get(GMDD.data.PULL_MENTOR_CONFIRM, {}).get('text', msgText)
        self.apprenticePullIds.append(gbId)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.onConfirmApprenticePull, skillId, args, True, gbId), yesBtnText=gameStrings.TEXT_IMPFRIEND_2211, noCallback=Functor(self.onConfirmApprenticePull, skillId, args, False, gbId), noBtnText=gameStrings.TEXT_IMPFRIEND_927)

    def onConfirmApprenticePull(self, skillId, args, ok, gbId):
        if gbId in self.apprenticePullIds:
            self.apprenticePullIds.remove(gbId)
        self.cell.confirmPulledByApprentice(skillId, args, ok, gbId)

    def initCheckRecommendFriend(self):
        if not self.inWorld:
            return
        if not hasattr(self, 'birthTime') or not hasattr(self, 'onlineTime'):
            return
        ft = max(utils.getServerOpenTime(), self.birthTime)
        tpass = utils.getNow() - self.onlineTime
        if utils.isSameDay(ft):
            t = SCD.data.get('recommendFriendTimeOnFirstDay', 7200)
            if tpass < t:
                BigWorld.callback(t - tpass, self.onRecommendFriendNotify)
        else:
            t = SCD.data.get('recommendFriendTimeIfLittle', 3600)
            if tpass < t:
                BigWorld.callback(t - tpass, self.onRecommendFriendNotifyIfLittle)

    def recommendFriendOnLeaveMap(self, oldSpaceNo, spaceNo):
        if formula.getMLGNo(oldSpaceNo) == const.ML_GROUP_NO_2018_XINSHOUCUN and spaceNo == const.SPACE_NO_BIG_WORLD:
            if not hasattr(self, 'birthTime'):
                return
            ft = max(utils.getServerOpenTime(), self.birthTime)
            if utils.isSameDay(ft):
                BigWorld.callback(5, self.onRecommendFriendNotify)
