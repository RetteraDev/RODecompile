#Embedded file name: /WORKSPACE/data/entities/common/friend.o
import copy
import BigWorld
import const
import gametypes
import commcalc
import utils
import gamelog
from userType import UserDispatch, UserMultiDispatch
from userDictType import UserDictType
from userSoleType import UserSoleType
from data import intimacy_config_data as ICD
from data import intimacy_data as ID
from data import partner_config_data as PCD
if BigWorld.component == 'base':
    import Netease
    import gameconfig
    import cPickle
    import gameengine
elif BigWorld.component == 'client':
    from helpers.intimacyEvent import IntimacyEvent

class FriendTeamEndlessVal(UserSoleType):

    def __init__(self, fbNo = 0, teamEndlessLv = 1, timeCost = 0, timestamp = 0, version = 0):
        super(FriendTeamEndlessVal, self).__init__()
        self.fbNo = fbNo
        self.teamEndlessLv = teamEndlessLv
        self.timeCost = timeCost
        self.timestamp = timestamp
        self.version = version


class FriendTeamEndless(UserDictType):

    def __init__(self):
        super(FriendTeamEndless, self).__init__()

    def setItem(self, fbNo, item):
        self[fbNo] = item

    def pushVal(self, fbNo, teamEndless, timeCost, timestamp = utils.getNow(), version = 0):
        self[fbNo] = FriendTeamEndlessVal(fbNo=fbNo, teamEndlessLv=teamEndless, timeCost=timeCost, timestamp=timestamp, version=version)


class FriendVal(UserSoleType, UserDispatch):

    def __init__(self, name = '', dbID = 0, gbId = 0, pally = 0, group = 0, box = None, school = 0, sex = const.SEX_MALE, level = 0, signature = '', acknowledge = False, state = gametypes.FRIEND_STATE_ONLINE, spaceNo = 0, areaId = 0, showsig = True, hatred = 0, offlineMsgCnt = 0, photo = '', opNuid = 0, apprentice = False, yixinOpenId = '', deleted = False, toHostID = 0, flowbackType = 0, intimacy = 0, intimacySrc = {}, intimacyLv = 1, remarkName = '', srcId = 0, mingpaiId = 0, appearanceCollectPoint = 0, endlessChallengeInfo = {}, recallState = 0, recallInfo = {}, borderId = 0, teamEndless = None, spriteChallengeInfo = {}, activityDict = {}):
        super(FriendVal, self).__init__()
        self.name = name
        self.dbID = dbID
        self.gbId = gbId
        self.pally = pally
        self.hatred = hatred
        self.group = group
        self.box = box
        self.school = school
        self.sex = sex
        self.level = level
        self.acknowledge = acknowledge
        self.signature = signature
        self.showsig = showsig
        self.state = state
        self.spaceNo = spaceNo
        self.areaId = areaId
        self.offlineMsgCnt = offlineMsgCnt
        self.photo = photo
        self.opNuid = opNuid
        self.apprentice = apprentice
        self.yixinOpenId = yixinOpenId
        self.deleted = deleted
        self.toHostID = toHostID
        self.flowbackType = flowbackType
        self.intimacy = intimacy
        self.intimacySrc = copy.copy(intimacySrc)
        self.intimacyLv = intimacyLv
        self.remarkName = remarkName
        self.srcId = srcId
        self.mingpaiId = mingpaiId
        self.appearanceCollectPoint = appearanceCollectPoint
        self.endlessChallengeInfo = endlessChallengeInfo
        self.recallState = recallState
        self.recallInfo = recallInfo
        self.borderId = borderId
        self.teamEndlessInfo = FriendTeamEndless() if teamEndless is None else teamEndless
        self.spriteChallengeInfo = copy.deepcopy(spriteChallengeInfo)
        self.activityDict = copy.deepcopy(activityDict)

    def getRemoteContactInfo(self):
        return {'roleName': self.name,
         'gbId': self.gbId,
         'school': self.school,
         'level': self.level,
         'sex': self.sex,
         'hostId': int(gameconfig.getHostId()),
         'serverName': gameconfig.getServerName(),
         'photo': self.photo,
         'signature': self.signature,
         'mingpaiId': self.mingpaiId}

    def getEntityId(self):
        if self.box:
            eid = self.box.id
        else:
            eid = 0
        return eid

    def getSimpleDict(self):
        eid = self.getEntityId()
        return {'name': self.name,
         'id': eid,
         'group': self.group,
         'school': self.school,
         'level': self.level,
         'signature': self.signature,
         'showsig': self.showsig,
         'acknowledge': self.acknowledge,
         'intimacyLv': self.intimacyLv,
         'state': self.state,
         'pally': self.pally,
         'hatred': self.hatred,
         'yixinOpenId': self.yixinOpenId,
         'flowbackType': self.flowbackType,
         'intimacy': self.intimacy,
         'mingpaiId': self.mingpaiId,
         'srcId': self.srcId,
         'appearanceCollectPoint': self.appearanceCollectPoint,
         'activityDict': self.activityDict}

    def getSimpleDataObj(self):
        eid = self.getEntityId()
        return (eid,
         self.gbId,
         self.level,
         self.acknowledge,
         self.state,
         self.spaceNo,
         self.areaId,
         self.yixinOpenId)

    def getFullDataObj(self):
        eid = self.getEntityId()
        return (eid,
         self.gbId,
         self.dbID,
         self.group,
         self.level,
         self.acknowledge,
         self.state,
         self.spaceNo,
         self.areaId,
         self.name,
         self.signature,
         self.school,
         self.sex,
         self.hatred,
         self.pally,
         self.showsig,
         self.photo,
         self.apprentice,
         self.yixinOpenId,
         self.deleted,
         self.toHostID,
         self.flowbackType,
         self.intimacy,
         self.remarkName,
         self.intimacyLv,
         self.srcId,
         self.mingpaiId,
         self.appearanceCollectPoint,
         self.endlessChallengeInfo,
         self.recallState,
         self.recallInfo,
         self.borderId,
         self.activityDict)

    def offline(self):
        return not self.box

    def present(self):
        return self.box != None

    def getEntity(self):
        if self.box:
            return BigWorld.entities.get(self.box.id, None)
        if hasattr(self, 'eid'):
            ent = BigWorld.entities.get(self.eid, None)
            if ent and ent.__class__.__name__ == 'Avatar' and ent.gbId == self.gbId:
                return ent

    def getFullName(self):
        if self.remarkName:
            return self.remarkName
        return self.name


class Friend(UserDictType, UserMultiDispatch):

    def __init__(self):
        super(Friend, self).__init__()
        self.groups = copy.deepcopy(const.FRIEND_GROUP_DEFAULT)
        self.signature = ''
        self.showsig = True
        self.state = gametypes.FRIEND_STATE_ONLINE
        self.constellation = 0
        self.birthmonth = 1
        self.birthday = 1
        self.sex = 0
        self.bloodType = 0
        self.province = 0
        self.city = 0
        self.qq = ''
        self.photo = ''
        self.description = ''
        self.pvisibility = 0
        self.onlineTime = ''
        self.intimacyTgt = 0
        self.tBuildIntimacy = 0
        self.defaultGroup = 0
        self.groupOrder = []

    def initClient(self):
        self.inited = False
        self.temp = {}
        self.tempMsgIdx = 0
        self.tempMsgs = []
        self.tempMsgsAsync = []
        self.tempMsgChat = []
        self.tempMsgOther = []
        self.tempMsgCount = {}
        self.options = bytearray('')
        self.oldState = gametypes.FRIEND_STATE_ONLINE
        self.tempContactInfoBeforeInit = []
        return self

    def clearTempMsg(self):
        self.tempMsgIdx = 0
        self.tempMsgs = []
        self.tempMsgChat = []
        self.tempMsgOther = []
        self.tempMsgCount = {}

    def getTempMsg(self):
        return (self.tempMsgIdx,
         self.tempMsgs,
         self.tempMsgChat,
         self.tempMsgOther,
         self.tempMsgCount)

    def initTempMsg(self, val):
        if val:
            self.tempMsgIdx, self.tempMsgs, self.tempMsgChat, self.tempMsgOther, self.tempMsgCount = val

    def _lateReload(self):
        super(Friend, self)._lateReload()
        for fVal in self.itervalues():
            fVal.reloadScript()

    def isValidGroup(self, group):
        return self.groups.has_key(group)

    def isEmpty(self):
        return len(self) == 0

    def isFriendGroup(self, group):
        return group == gametypes.FRIEND_GROUP_FRIEND or group >= const.FRIEND_CUSTOM_GROUP_BEGIN

    def isEnemyGroup(self, group):
        return group == gametypes.FRIEND_GROUP_ENEMY or group == gametypes.FRIEND_GROUP_BLOCK_ENEMY

    def isBlockGroup(self, group):
        return group == gametypes.FRIEND_GROUP_BLOCK or group == gametypes.FRIEND_GROUP_BLOCK_ENEMY

    def isApprenticeGroup(self, group):
        return group == gametypes.FRIEND_GROUP_APPRENTICE

    def isTempGroup(self, group):
        return group == gametypes.FRIEND_GROUP_TEMP

    def isCustomGroup(self, group):
        return group >= const.FRIEND_CUSTOM_GROUP_BEGIN

    def isOrderAbleGroup(self, group):
        return self.isFriendGroup(group) or self.isApprenticeGroup(group) or group == gametypes.FRIEND_GROUP_GLOBAL_FRIEND

    def isNpcGroup(self, group):
        return group == gametypes.FRIEND_GROUP_NPC

    def isFriend(self, who):
        if self.has_key(who):
            return self.isFriendGroup(self[who].group)
        return False

    def isEnemy(self, who):
        if self.has_key(who):
            return self.isEnemyGroup(self[who].group)
        return False

    def isBlock(self, who):
        if self.has_key(who):
            return self.isBlockGroup(self[who].group)
        return False

    def isApprentice(self, who):
        if self.has_key(who):
            return self[who].apprentice
        return False

    def calcFriendCnt(self, isOn):
        cnt = 0
        for val in self.itervalues():
            if isOn and val.box == None:
                continue
            if self.isFriendGroup(val.group):
                cnt += 1

        return cnt

    def calcEnemyCnt(self, isOn):
        cnt = 0
        for val in self.itervalues():
            if isOn and val.box == None:
                continue
            if self.isEnemyGroup(val.group):
                cnt += 1

        return cnt

    def getAvailGroup(self):
        for i in range(const.FRIEND_CUSTOM_GROUP_BEGIN, const.FRIEND_CUSTOM_GROUP_BEGIN + const.FRIEND_CUSTOM_GROUP_MAX):
            if not self.groups.has_key(i):
                return i

        return 0

    def getGroupMembers(self, group):
        fVals = []
        for v in self.itervalues():
            if v.group == group:
                fVals.append(v)

        return fVals

    def getGroupMembersName(self, group):
        fVals = []
        for v in self.itervalues():
            if v.group == group:
                fVals.append(v.name)

        return fVals

    def getApprenticeMemberGbIds(self):
        gbIds = []
        for gbId, v in self.iteritems():
            if v.apprentice:
                gbIds.append(gbId)

        return gbIds

    def hasFriendInCustomGroup(self, group):
        if not self.isCustomGroup(group):
            return False
        for v in self.itervalues():
            if v.group == group:
                return True

        return False

    def hasContact(self, who):
        return self.has_key(who)

    def canAddOffline(self, group):
        return group == gametypes.FRIEND_GROUP_APPRENTICE or group == gametypes.FRIEND_GROUP_FRIEND

    def setFriendsExInfo(self, owner, data):
        for v in data:
            f = self.get(v['gbId'])
            if f:
                if BigWorld.component == 'base' and not owner._isSoul():
                    f.name = v['name']
                f.school = v['school']
                f.sex = v['sex']
                f.level = v['level']
                f.spaceNo = v['spaceNo']
                f.areaId = v['areaId']
                f.signature = v['signature']
                f.showsig = v['showsig']
                f.photo = v['photo']
                f.yixinOpenId = v['yixinOpenId']
                f.deleted = v['deleted']
                f.toHostID = v['toHostID']
                f.mingpaiId = v['mingpaiId']
                f.appearanceCollectPoint = v['appearanceCollectPoint']
                f.endlessChallengeInfo = v['endlessChallengeInfo']
                f.borderId = v.get('borderId', 0)

    def updateLevel(self, gbId, level):
        f = self.get(gbId)
        if f and f.level != level:
            f.level = level
            return True
        return False

    def updateSchool(self, gbId, school):
        f = self.get(gbId)
        if f and f.school != school:
            f.school = school
            return True
        return False

    def updateSignature(self, gbId, signature):
        f = self.get(gbId)
        if f and f.signature != signature:
            f.signature = signature
            return True
        return False

    def updateShowsig(self, gbId, showsig):
        f = self.get(gbId)
        if f and f.showsig != showsig:
            f.showsig = showsig
            return True
        return False

    def updateState(self, gbId, state):
        f = self.get(gbId)
        if f and f.state != state:
            f.state = state
            return True
        return False

    def updateSpaceNo(self, gbId, spaceNo):
        f = self.get(gbId)
        if f and f.spaceNo != spaceNo:
            f.spaceNo = spaceNo
            return True
        return False

    def updateAreaId(self, gbId, spaceNo, areaId):
        f = self.get(gbId)
        updated = False
        if f:
            if spaceNo and f.spaceNo != spaceNo:
                f.spaceNo = spaceNo
                updated = True
            if f.areaId != areaId:
                f.areaId = areaId
                updated = True
        return updated

    def updateYixinStatus(self, gbId, bindStatus):
        f = self.get(gbId)
        if f and f.yixinOpenId != bindStatus:
            f.yixinOpenId = bindStatus
            return True
        return False

    def updatePhoto(self, gbId, photo):
        f = self.get(gbId)
        if f and f.photo != photo:
            f.photo = photo
            return True
        return False

    def updateName(self, gbId, name):
        f = self.get(gbId)
        if f and f.name != name:
            f.name = name
            return True
        return False

    def updateApprentice(self, gbId, apprentice):
        f = self.get(gbId)
        if f and f.apprentice != apprentice:
            f.apprentice = apprentice
            return True
        return False

    def updateSex(self, gbId, sex):
        f = self.get(gbId)
        if f and f.sex != sex:
            f.sex = sex
            return True
        return False

    def updateFlowbackType(self, gbId, flowbackType):
        f = self.get(gbId)
        if f and f.flowbackType != flowbackType:
            f.flowbackType = flowbackType
            return True
        return False

    def updateMingpaiId(self, gbId, mingpaiId):
        f = self.get(gbId)
        if f and f.mingpaiId != mingpaiId:
            f.mingpaiId = mingpaiId
            return True
        return False

    def updatePhotoBorderId(self, gbId, borderId):
        f = self.get(gbId)
        if f and f.borderId != borderId:
            f.borderId = borderId
            return True
        return False

    def updateRemarkName(self, gbId, remarkName):
        f = self.get(gbId)
        if f and f.remarkName != remarkName:
            f.remarkName = remarkName
            return True
        return False

    def updateSrcId(self, gbId, srcId):
        f = self.get(gbId)
        if f and f.srcId != srcId:
            f.srcId = srcId
            return True
        return False

    def updatePally(self, gbId, pally):
        f = self.get(gbId)
        if f and f.pally != pally:
            f.pally = pally
            return True
        return False

    def updateIntimacy(self, gbId, intimacy):
        f = self.get(gbId)
        if f and f.intimacy != intimacy:
            f.intimacy = intimacy
            return True
        return False

    def updateIntimacyLv(self, gbId, intimacyLv):
        f = self.get(gbId)
        if f and f.intimacyLv != intimacyLv:
            f.intimacyLv = intimacyLv
            return True
        return False

    def updateHatred(self, gbId, hatred):
        f = self.get(gbId)
        if f and f.hatred != hatred:
            f.hatred = hatred
            return True
        return False

    def updateGroup(self, gbId, group):
        f = self.get(gbId)
        if f and f.group != group:
            f.group = group
            return True
        return False

    def updateAcknowledge(self, gbId, acknowledge):
        f = self.get(gbId)
        if f and f.acknowledge != acknowledge:
            f.acknowledge = acknowledge
            return True
        return False

    def updateAppearanceCollectPoint(self, gbId, appearanceCollectPoint):
        f = self.get(gbId)
        if f and f.appearanceCollectPoint != appearanceCollectPoint:
            f.appearanceCollectPoint = appearanceCollectPoint
            return True
        return False

    def updateEndlessChallengeInfo(self, gbId, endlessChallengeInfo):
        f = self.get(gbId)
        if f and f.endlessChallengeInfo != endlessChallengeInfo:
            f.endlessChallengeInfo = endlessChallengeInfo
            return True
        return False

    def updateSpriteChallengeInfo(self, gbId, spriteChallengeInfo):
        f = self.get(gbId)
        if f and f.spriteChallengeInfo != spriteChallengeInfo:
            f.spriteChallengeInfo = spriteChallengeInfo
            return True
        return False

    def updateRecallState(self, gbId, state):
        f = self.get(gbId)
        if f and f.recallState != state:
            f.recallState = state
            return True
        return False

    def updateRecallInfo(self, gbId, recallInfo):
        f = self.get(gbId)
        if f and f.recallInfo != recallInfo:
            f.recallInfo = recallInfo
            return True
        return False

    def updateActivityDict(self, gbId, activityDict):
        f = self.get(gbId)
        if f and activityDict:
            f.activityDict.update(activityDict)
            return True
        return False

    def updateMySignature(self, signature):
        self.signature = signature

    def reCalcIntimacyLv(self, owner, tgtGbId, srcType):
        """
        \xb5\xb1\xbd\xe2\xc6\xf5\xa1\xa2\xbd\xe2\xb3\xfd\xca\xa6\xcd\xbd\xb9\xd8\xcf\xb5\xa1\xa2\xbd\xe2\xb3\xfd\xbd\xe1\xb0\xe9\xb9\xd8\xcf\xb5\xca\xb1\xd0\xe8\xd2\xaa\xd6\xd8\xd0\xc2\xbc\xc6\xcb\xe3\xcd\xe6\xbc\xd2\xb5\xc4\xc7\xd7\xc3\xdc\xb6\xc8\xd6\xb5
        Args:
            owner:
            tgtGbId:
        
        Returns:
        
        """
        gamelog.info('@hjx intimacyLv#reCalcIntimacyLv:', owner.id, tgtGbId, srcType, self.intimacyTgt)
        flag = False
        beInPartner = False
        if tgtGbId == 0:
            if BigWorld.component == 'base':
                if self.intimacyTgt > 0:
                    if self.intimacyTgt not in owner.apprenticeBaseEx or not owner.apprenticeBaseEx[self.intimacyTgt].isSole():
                        flag = True
                    if self.intimacyTgt in owner.partnerSetOfBase:
                        beInPartner = True
            elif BigWorld.component == 'client':
                if self.intimacyTgt > 0:
                    if self.intimacyTgt not in (owner.soleMentorGbId, owner.soleApprenticeGbId):
                        flag = True
                    if self.intimacyTgt in owner.partner.keys():
                        flag = True
                        beInPartner = True
            f = self.get(self.intimacyTgt)
        else:
            if srcType == gametypes.INTIMACY_LV_RECALC_SRC_TYPE_APPRENTICE:
                if self.intimacyTgt != tgtGbId:
                    flag = True
            elif srcType == gametypes.INTIMACY_LV_RECALC_SRC_TYPE_PARTNER:
                if BigWorld.component == 'base':
                    if self.intimacyTgt != tgtGbId and (tgtGbId not in owner.apprenticeBaseEx or not owner.apprenticeBaseEx[tgtGbId].isSole()):
                        flag = True
                elif BigWorld.component == 'client':
                    if self.intimacyTgt != tgtGbId and tgtGbId not in (owner.soleMentorGbId, owner.soleApprenticeGbId):
                        flag = True
            if BigWorld.component == 'base':
                if tgtGbId in owner.partnerSetOfBase:
                    beInPartner = True
            elif BigWorld.component == 'client':
                if tgtGbId in owner.partner.keys():
                    beInPartner = True
            f = self.get(tgtGbId)
        INTIMACY_RESET_LV_LIMIT_BY_REMOVE = ICD.data.get('INTIMACY_RESET_LV_LIMIT_BY_REMOVE', 5)
        partnerIntimacyLvLimit = PCD.data.get('partnerIntimacyLvLimit', 8)
        if f and flag:
            if beInPartner:
                if f.intimacyLv > partnerIntimacyLvLimit:
                    f.intimacyLv = partnerIntimacyLvLimit
                    f.intimacy = ID.data[partnerIntimacyLvLimit]['maxVal'] if partnerIntimacyLvLimit > 1 else 0
            elif f.intimacyLv >= INTIMACY_RESET_LV_LIMIT_BY_REMOVE:
                f.intimacyLv = INTIMACY_RESET_LV_LIMIT_BY_REMOVE
                f.intimacy = ID.data[INTIMACY_RESET_LV_LIMIT_BY_REMOVE - 1]['maxVal'] if INTIMACY_RESET_LV_LIMIT_BY_REMOVE > 1 else 0
        return flag

    def syncToHomeRoom(self, owner, intimacyTgt, intimacyName):
        if BigWorld.component == 'base':
            gameengine.getGlobalBase('HomeStub').syncPlayerData(owner.gbID, {const.HOME_DATA_TYPE_INTIMACY_TGT: intimacyTgt,
             const.HOME_DATA_TYPE_INTIMACY_NAME: intimacyName})
            gameengine.getGlobalBase('HomeStub').syncPlayerData(intimacyTgt, {const.HOME_DATA_TYPE_INTIMACY_TGT: owner.gbID,
             const.HOME_DATA_TYPE_INTIMACY_NAME: owner.playerName})

    def updateIntimacyTgt(self, owner, intimacyTgt):
        if intimacyTgt == 0:
            flag = self.reCalcIntimacyLv(owner, intimacyTgt, gametypes.INTIMACY_LV_RECALC_SRC_TYPE_INTIMACY)
            self.tBuildIntimacy = 0
            if BigWorld.component == 'base':
                owner.resetIntimacyTgtInfo()
                gameengine.getGlobalBase('HomeStub').resetIntimacyTgt(owner.gbID, self.intimacyTgt)
                gameengine.getGlobalBase('HomeStub').resetIntimacyTgt(self.intimacyTgt, owner.gbID)
                owner.setBaseMiscProperty(gametypes.MISC_VAR_BPRI_BUILD_INTIMACY_CNT, 0)
                if owner.friend.has_key(self.intimacyTgt):
                    owner.cell.updateMemberIntimacyProp([{'gbId': self.intimacyTgt,
                      'intimacyLv': owner.friend[self.intimacyTgt].intimacyLv,
                      'isFullIntimacy': True}])
                if gameconfig.enableFullScreenFireworks():
                    fVal = self.get(self.intimacyTgt, None)
                    tgtIntimacy = fVal.intimacy if fVal else 0
                    owner.cell.checkRemoveTitleOnRemoveIntimacy(tgtIntimacy)
            elif BigWorld.component == 'client':
                owner.intimacyEvent = IntimacyEvent()
            owner.intimacyTgtNickName = ''
        else:
            self.tBuildIntimacy = utils.getNow()
            intimacyName = self[intimacyTgt].name if intimacyTgt in self else ''
            self.syncToHomeRoom(owner, intimacyTgt, intimacyName)
            if BigWorld.component == 'base' and gameconfig.enableFullScreenFireworks():
                fVal = self.get(intimacyTgt, None)
                tgtIntimacy = fVal.intimacy if fVal else 0
                owner.cell.checkAddTitleOnAddIntimacy(tgtIntimacy)
        self.intimacyTgt = intimacyTgt

    def updateMyShowsig(self, showsig):
        self.showsig = showsig

    def updateMyState(self, state):
        self.state = state

    def updateMsgChatIdx(self, idx, gbId, name):
        for value in self.tempMsgChat:
            if value[1] == gbId:
                self.tempMsgChat.remove(value)
                self.tempMsgChat.append((idx, gbId, name))
                break

    def getAcknowledgeFriendGbIds(self, includeApprentice = False, onlineOnly = False, exclude = None, intimacyLv = 0):
        gbIds = []
        for v in self.itervalues():
            if v.acknowledge or includeApprentice and v.apprentice:
                if not onlineOnly or v.state in gametypes.FRIEND_VISIBLE_STATES:
                    if (not exclude or v.gbId not in exclude) and (not intimacyLv or v.intimacyLv >= intimacyLv):
                        gbIds.append(v.gbId)

        return gbIds

    def getAcknowledgeFriends(self):
        fVals = []
        for v in self.itervalues():
            if v.acknowledge:
                fVals.append(v)

        return fVals

    def checkAcknowledgeFriend(self, gbId):
        if not self.has_key(gbId):
            return False
        if self[gbId].acknowledge:
            return True
        return False

    def getFriendCount(self):
        cnt = 0
        cntMale = 0
        cntFemale = 0
        cntMale2 = 0
        cntFemale2 = 0
        for k, v in self.iteritems():
            if self.isFriend(k):
                if not v.acknowledge:
                    cnt += 1
                    if v.sex == const.SEX_MALE:
                        cntMale += 1
                    elif v.sex == const.SEX_FEMALE:
                        cntFemale += 1
                if v.sex == const.SEX_MALE:
                    cntMale2 += 1
                elif v.sex == const.SEX_FEMALE:
                    cntFemale2 += 1

        return (cnt,
         cntMale,
         cntFemale,
         cntMale2,
         cntFemale2)

    def getAcknowledgeFriendCount(self):
        cnt = 0
        cntMale = 0
        cntFemale = 0
        for v in self.itervalues():
            if v.acknowledge:
                cnt += 1
                if v.sex == const.SEX_MALE:
                    cntMale += 1
                elif v.sex == const.SEX_FEMALE:
                    cntFemale += 1

        return (cnt, cntMale, cntFemale)

    def getUnacknowledgeFriendGbIds(self):
        gbIds = []
        for v in self.itervalues():
            if not v.acknowledge:
                gbIds.append(v.gbId)

        return gbIds

    def getUnacknowledgeFriends(self):
        fVals = []
        for v in self.itervalues():
            if not v.acknowledge:
                fVals.append(v)

        return fVals

    def isSimilarGroup(self, g1, g2):
        return g1 == g2 or self.isFriendGroup(g1) and self.isFriendGroup(g2) or self.isEnemyGroup(g1) and self.isEnemyGroup(g2) or self.isBlockGroup(g1) and self.isBlockGroup(g2)

    def isInGroup(self, gbId, group):
        fVal = self.get(gbId)
        if not fVal:
            return False
        return fVal.group == group

    def getGroupMemberCount(self, group):
        cnt = 0
        for v in self.itervalues():
            if self.isSimilarGroup(v.group, group):
                cnt += 1

        return cnt

    def isGroupFull(self, group, owner):
        cnt = self.getGroupMemberCount(group)
        if self.isFriendGroup(group):
            return cnt + owner.globalFriend.friendCount() >= owner.vipRevise(gametypes.VIP_SERVICE_FRIEND_MAX, const.FRIEND_MAX + owner.getAbilityData(gametypes.ABILITY_FRIEND_MAX_ADD))
        elif self.isBlockGroup(group):
            return cnt >= const.FRIEND_BLOCK_MAX
        elif self.isEnemyGroup(group):
            return cnt >= const.FRIEND_ENENY_MAX + owner.getAbilityData(gametypes.ABILITY_ENEMY_MAX_ADD)
        elif self.isApprenticeGroup(group):
            return cnt >= const.FRIEND_MAX
        elif self.isNpcGroup(group):
            return cnt >= const.FRIEND_NPC_MAX
        else:
            return False

    def getGroupName(self, group, useDefault = False):
        if useDefault and not self.isCustomGroup(group) or group == gametypes.FRIEND_GROUP_BLOCK_ENEMY:
            return const.FRIEND_GROUP_DEFAULT.get(group)
        else:
            return self.groups.get(group)

    def setGroupName(self, group, name):
        if self.groups.has_key(group):
            self.groups[group] = name

    def addGroup(self, group, name):
        self.groups[group] = name

    def add(self, gbId, fInfo, group, acknowledge = False, pally = 0, hatred = 0, intimacy = 0, intimacyLv = 1, owner = None, srcId = 0):
        dbId, name, state, school, sex, level, signature, showsig, spaceNo, areaId, photo, yixinOpenId, box, flowbackType, mingpaiId, appearanceCollectPoint, endlessChallengeInfo, borderId = fInfo
        fVal = self.get(gbId)
        if not self.has_key(gbId):
            fVal = FriendVal(name=name, dbID=dbId, gbId=gbId, state=state, school=school, pally=pally, hatred=hatred, acknowledge=acknowledge, sex=sex, level=level, box=box, group=group, signature=signature, showsig=showsig, spaceNo=spaceNo, areaId=areaId, photo=photo, yixinOpenId=yixinOpenId, flowbackType=flowbackType, intimacy=intimacy, intimacyLv=intimacyLv, mingpaiId=mingpaiId, srcId=srcId, appearanceCollectPoint=appearanceCollectPoint, endlessChallengeInfo=endlessChallengeInfo, borderId=borderId)
            self[gbId] = fVal
            if self.isEnemyGroup(group):
                fVal.hatred = const.FRIEND_INIT_HATRED
        else:
            fVal = self[gbId]
            fVal.group = group
            fVal.state = state
            fVal.acknowledge = acknowledge
            if BigWorld.component == 'base' and owner:
                owner.cell.updateMemberPally(gbId, acknowledge)
            fVal.spaceNo = spaceNo
            if pally > 0:
                fVal.pally = pally
            if hatred > 0:
                fVal.hatred = hatred
            if intimacy > 0:
                fVal.intimacy = intimacy
            if intimacyLv > 1:
                fVal.intimacyLv = intimacyLv
            if mingpaiId:
                fVal.mingpaiId = mingpaiId
            if appearanceCollectPoint:
                fVal.appearanceCollectPoint = appearanceCollectPoint
            if endlessChallengeInfo:
                fVal.endlessChallengeInfo = endlessChallengeInfo
            if borderId > 0:
                fVal.borderId = borderId
            fVal.showsig = showsig
            fVal.signature = signature
            if self.isEnemyGroup(group) and fVal.hatred == 0:
                fVal.hatred = const.FRIEND_INIT_HATRED
            fVal.yixinOpenId = yixinOpenId
        return fVal

    def changeGroup(self, owner, gbId, group):
        fVal = self.get(gbId)
        if not fVal:
            return False
        if fVal.group != group:
            fVal.group = group
            if not self.isFriendGroup(group):
                fVal.acknowledge = False
                if BigWorld.component == 'base':
                    owner.cell.updateMemberPally(gbId, False)
            return True
        return False

    def canDelete(self, gbId):
        fVal = self.get(gbId, None)
        return fVal and not fVal.group and not fVal.apprentice

    def deleteFriend(self, gbId):
        fVal = self.get(gbId, None)
        if fVal:
            fVal.group = 0
            fVal.acknowledge = False
            fVal.pally = 0
            fVal.intimacy = 0
            fVal.intimacyLv = 1
            fVal.intimacySrc = {}
            if self.canDelete(gbId):
                self.pop(gbId)
                return (True, fVal)
        return (False, fVal)

    def unblockFriend(self, gbId):
        fVal = self.get(gbId, None)
        if fVal and self.isBlockGroup(fVal.group):
            if fVal.group == gametypes.FRIEND_GROUP_BLOCK_ENEMY:
                fVal.group = gametypes.FRIEND_GROUP_ENEMY
            else:
                fVal.group = 0
            if self.canDelete(gbId):
                self.pop(gbId)
                return (True, fVal)
        return (False, fVal)

    def deleteEnemy(self, gbId):
        fVal = self.get(gbId, None)
        if fVal and self.isEnemyGroup(fVal.group):
            if fVal.group == gametypes.FRIEND_GROUP_BLOCK_ENEMY:
                fVal.group = gametypes.FRIEND_GROUP_BLOCK
            else:
                fVal.group = 0
            if self.canDelete(gbId):
                self.pop(gbId)
                return (True, fVal)
        return (False, fVal)

    def deleteApprentice(self, gbId):
        fVal = self.get(gbId, None)
        if fVal and fVal.apprentice:
            fVal.apprentice = False
            if self.canDelete(gbId):
                self.pop(gbId)
                return (True, fVal)
        return (False, fVal)

    def deleteNpc(self, gbId):
        fVal = self.get(gbId, None)
        if fVal and self.isNpcGroup(fVal.group):
            fVal.group = 0
            if self.canDelete(gbId):
                self.pop(gbId)
                return (True, fVal)
        return (False, fVal)

    def isValidOption(self, option):
        return option >= const.FRIEND_OPTION_BEGIN and option <= const.FRIEND_OPTION_END

    def getOption(self, option):
        return commcalc.getBit(self.options, option)

    def setOption(self, option, checked):
        commcalc.setBit(self.options, option, checked)

    def getOptions(self):
        options = {}
        for op in gametypes.FRIEND_OPTIONS:
            options[op] = self.getOption(op)

        return options

    def findByRole(self, role):
        for fVal in self.itervalues():
            if fVal.name == role:
                return fVal

    def roleName2GbId(self, roleName):
        for gbId, fVal in self.iteritems():
            if fVal.name == roleName:
                return gbId

    def getFriendGroups(self):
        groups = [gametypes.FRIEND_GROUP_FRIEND]
        for group in range(const.FRIEND_CUSTOM_GROUP_BEGIN, const.FRIEND_CUSTOM_GROUP_BEGIN + const.FRIEND_CUSTOM_GROUP_MAX):
            name = self.groups.get(group)
            if not name:
                continue
            groups.append(group)

        return groups

    def getFriendGroupNames(self):
        groups = [gametypes.FRIEND_GROUP_FRIEND]
        for group in range(const.FRIEND_CUSTOM_GROUP_BEGIN, const.FRIEND_CUSTOM_GROUP_BEGIN + const.FRIEND_CUSTOM_GROUP_MAX):
            name = self.groups.get(group)
            if not name:
                continue
            groups.append(name)

        return groups

    def getGroupByName(self, name):
        for id, gname in self.groups.iteritems():
            if gname == name:
                return id

        for id, gname in const.FRIEND_GROUP_EXTRA.iteritems():
            if gname == name:
                return id

    def getNameByGroupId(self, groupId):
        if self.groups.has_key(groupId):
            return self.groups[groupId]
        else:
            return const.FRIEND_GROUP_NAME_DICT.get(groupId, None)

    def isVisible(self, state):
        return state == gametypes.FRIEND_STATE_ONLINE or state == gametypes.FRIEND_STATE_AWAY or state == gametypes.FRIEND_STATE_BUSY

    def isSystem(self, gbId):
        return gbId == const.FRIEND_SYSTEM_ID

    def isSystemSpecialMsg(self, mtype):
        return mtype >= gametypes.FRIEND_MSG_TYPE_SPECIAL

    def isFriendSpecialMsg(self, mtype):
        return mtype in gametypes.FRIEND_SPEICAL_MSG_TYPES

    def isFriendAddMsg(self, mtype):
        return mtype in gametypes.FRIEND_ADD_MSG_TYPES

    def _getProfile(self):
        return (self.pvisibility,
         self.photo,
         self.constellation,
         self.birthmonth,
         self.birthday,
         self.sex,
         self.bloodType,
         self.province,
         self.city,
         self.qq,
         self.description,
         self.onlineTime)

    def notifyProfileUpate(self, owner):
        owner.client.onProfileUpdate(self._getProfile())

    def getDefaultPhoto(self, school, sex):
        photo = 'headIcon/%s.dds' % str(school * 10 + sex)
        return photo

    def createRemoteContactInfo(self, owner):
        """
        \xd5\xe2\xca\xc7\xb8\xf8\xbf\xe7\xb7\xfe\xba\xc3\xd3\xd1\xd3\xc3\xb5\xc4\xba\xc3\xd3\xd1\xd0\xc5\xcf\xa2\xa3\xac\xba\xf3\xd0\xf8\xbf\xc9\xd4\xda\xd5\xe2\xc0\xef\xcc\xed\xbc\xd3
        :return:
        """
        roll = Netease.rollCache[owner.id]
        return {'roleName': owner.roleName,
         'gbId': owner.gbID,
         'school': roll.school,
         'level': roll.level,
         'sex': roll.sex,
         'hostId': int(gameconfig.getHostId()),
         'serverName': gameconfig.getServerName(),
         'photo': self.photo,
         'signature': self.signature,
         'mingpaiId': owner.mingpai.selectedId}

    def transferAckToRemote(self, owner):
        if not gameconfig.enableGlobalFriend():
            return
        serverId = int(gameconfig.getHostId())
        myInfo = (owner.gbID,
         owner.roleName,
         serverId,
         cPickle.dumps(self.createRemoteContactInfo(owner), -1))
        friendInfos = []
        for fVal in self.getAcknowledgeFriends():
            friendInfos.append((fVal.gbId,
             fVal.name,
             serverId,
             cPickle.dumps(fVal.getRemoteContactInfo(), -1)))

        if not friendInfos:
            return
        gameengine.getGlobalBase('GlobalFriendStub').moveLocalFriendToRemote(myInfo, friendInfos)

    def getFriendIntimacy(self, gbId):
        """\xbb\xf1\xb5\xc3\xd3\xeb\xba\xc3\xd3\xd1\xb5\xc4\xc7\xd7\xc3\xdc\xb6\xc8"""
        p = self.get(gbId)
        if not p or not p.acknowledge:
            return 0
        return p.intimacy


class IntimacySkillVal(UserSoleType):

    def __init__(self, skillId, nextTime = 0, useCnt = 0):
        self.id = skillId
        self.nextTime = nextTime
        self.useCnt = useCnt

    def collect(self):
        return {'nextTime': self.nextTime,
         'useCnt': self.useCnt}


class IntimacySkill(UserDictType):

    def _lateReload(self):
        super(IntimacySkill, self)._lateReload()
        for sVal in self.itervalues():
            sVal.reloadScript()

    def transfer(self, owner):
        skills = []
        for skVal in self.values():
            skills.append({'skillId': skVal.id,
             'nextTime': skVal.nextTime,
             'useCnt': skVal.useCnt})

        owner.client.sendIntimacySkills(skills)
