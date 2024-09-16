#Embedded file name: I:/bag/tmp/tw2/res/entities\common/globalFriend.o
import BigWorld
import cPickle
if BigWorld.component in ('base', 'cell'):
    import gameengine
    import gametypes
    from globalMailBox import GlobalFriendMailBox
from userSoleType import UserSoleType
from userDictType import UserDictType

class GroupInfo(UserDictType):

    def __init__(self, lastGroupId = 1):
        super(GroupInfo, self).__init__()
        self.lastGroupId = 1

    def _lateReload(self):
        super(GroupInfo, self)._lateReload()

    def add(self, groupName):
        self.lastGroupId += 1
        self[self.lastGroupId] = groupName
        return self.lastGroupId

    def rename(self, groupId, groupName):
        if groupId not in self:
            return
        self[groupId] = groupName

    def remove(self, groupId):
        if groupId not in self:
            return
        del self[groupId]

    def fromDTO(self, dict):
        self.lastGroupId = dict.get('lastGroupId', 0)
        self.clear()
        for k, v in dict.get('data', {}):
            self[k] = v

    def getDTO(self):
        return {'lastGroupId': self.lastGroupId,
         'data': {k:v for k, v in self.iteritems()}}


class GlobalFriendVal(UserSoleType):

    def __init__(self, gbId, relationData, online, roleName, server, extraInfo):
        super(GlobalFriendVal, self).__init__()
        self.gbId = gbId
        if isinstance(relationData, basestring):
            if relationData:
                self.relationData = cPickle.loads(relationData)
            else:
                self.relationData = {'group': 0}
        else:
            self.relationData = relationData
        self.online = online
        self.roleName = roleName
        self.server = server
        if isinstance(extraInfo, basestring):
            if extraInfo:
                self.extraInfo = cPickle.loads(extraInfo)
            else:
                self.extraInfo = {}
        else:
            self.extraInfo = extraInfo

    def extraInfoData(self):
        return cPickle.dumps(self.extraInfo, -1)

    def relationInfoData(self):
        return cPickle.dumps(self.relationData, -1)

    def moveGroup(self, owner, grp):
        self.relationData['group'] = grp
        gameengine.getGlobalBase('GlobalFriendStub').updateFriendRelationInfo(owner.gbID, self.gbId, self.relationInfoData())

    def _lateReload(self):
        super(GlobalFriendVal, self)._lateReload()


class FriendDict(UserDictType):

    def __init__(self):
        super(FriendDict, self).__init__()

    def _lateReload(self):
        super(FriendDict, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def getDTO(self):
        return {k:v for k, v in self.iteritems()}

    def addFriend(self, gbId, relationData, online, roleName, server, extraInfo):
        self[gbId] = GlobalFriendVal(gbId, relationData, online, roleName, server, extraInfo)

    def fromDTO(self, dict):
        self.clear()
        for k, v in dict.iteritems():
            self[k] = v

    def load(self, friends):
        self.clear()
        for args in friends:
            self.addFriend(*args)


class GlobalFriend(UserSoleType):

    def __init__(self):
        self.groupInfo = GroupInfo()
        self.friends = FriendDict()

    def _lateReload(self):
        super(GlobalFriend, self)._lateReload()
        self.groupInfo.reloadScript()
        self.friends.reloadScript()

    @staticmethod
    def createInstance(d):
        obj = GlobalFriend()
        obj.groupInfo.fromDTO(d['groupInfo'])
        obj.friends.fromDTO(d['friends'])
        return obj

    def getDTO(self):
        return {'groupInfo': self.groupInfo.getDTO(),
         'friends': self.friends.getDTO()}

    def hasAnyFriend(self):
        return len(self.friends) > 0

    def friendCount(self):
        return len(self.friends)

    def isFull(self, owner):
        return owner.friend.isGroupFull(gametypes.FRIEND_GROUP_FRIEND, owner)

    def addGroup(self, owner, groupName):
        return self.groupInfo.add(groupName)

    def renameGroup(self, owner, groupId, groupName):
        return self.groupInfo.rename(groupId, groupName)

    def delGroup(self, owner, groupId):
        return self.groupInfo.remove(groupId)

    def moveGroup(self, owner, gbId, groupId):
        if gbId not in self.friends:
            return
        self.friends[gbId].moveGroup(owner, groupId)

    def insertFriend(self, owner, gbId, info):
        self.friends.addFriend(*info)
        owner.client.globalFriendAdd(info)

    def updateFriend(self, owner, gbId, info):
        if gbId not in self.friends:
            self.friends.addFriend(gbId, '', True, info.roleName, info.server, info.data)
        else:
            d = self.friends.get(gbId)
            self.friends.addFriend(gbId, d.relationData, d.online, info.roleName, info.server, info.data)
        owner.client.globalFriendInfoUpdate(gbId, self.friends.get(gbId))

    def delFriend(self, owner, gbId):
        if gbId not in self.friends:
            return
        del self.friends[gbId]
        owner.client.globalFriendDelete(gbId)

    def initFriends(self, owner, friends):
        self.friends.load(friends)
        self.transToClient(owner)

    def friendOnline(self, owner, gbId):
        if gbId not in self.friends:
            return
        self.friends[gbId].online = True
        self.transFriendInfoToClient(owner, gbId)

    def friendOffline(self, owner, gbId):
        if gbId not in self.friends:
            return
        self.friends[gbId].online = False
        self.transFriendInfoToClient(owner, gbId)

    def chatToFriend(self, owner, gbId, msg):
        if gbId not in self.friends:
            return
        friend = self.friends[gbId]
        GlobalFriendMailBox(self.friends[gbId].server, gbId).onRemoteChatTo(owner.gbID, msg)
        owner.cell.logChatToRemoteFriendMsg(msg, gbId, friend.roleName, friend.server)

    def transFriendInfoToClient(self, owner, gbId):
        owner.client.globalFriendInfoUpdate(gbId, self.friends[gbId])

    def transToClient(self, owner):
        owner.client.onLoadGlobalFriends(self)

    def hasFriendByName(self, hostId, name):
        for v in self.friends.itervalues():
            if hostId == v.server and name == v.roleName:
                return True

        return False
