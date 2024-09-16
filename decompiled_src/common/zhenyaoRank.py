#Embedded file name: I:/bag/tmp/tw2/res/entities\common/zhenyaoRank.o
import copy
from userSoleType import UserSoleType
from userDictType import UserDictType
from userListType import UserListType

class ZhenyaoScore(UserSoleType):

    def __init__(self, score = 0, interval = 0, tWhen = 0):
        super(ZhenyaoScore, self).__init__()
        self.score = score
        self.interval = interval
        self.tWhen = tWhen

    def _lateReload(self):
        super(ZhenyaoScore, self)._lateReload()


class ZhenyaoRankVal(UserSoleType):

    def __init__(self, groupNUID = 0, scoreInfo = ZhenyaoScore(), groupName = ''):
        super(ZhenyaoRankVal, self).__init__()
        self.groupNUID = groupNUID
        self.scoreInfo = scoreInfo
        self.groupName = groupName

    def _lateReload(self):
        self.scoreInfo.reloadScript()

    def formatRet(self):
        return {'groupNUID': self.groupNUID,
         'groupName': self.groupName,
         'score': self.scoreInfo.score,
         'interval': self.scoreInfo.interval,
         'tWhen': self.scoreInfo.tWhen}


def cmpZhenyaoRankVal(x, y):
    if x.scoreInfo.score > y.scoreInfo.score:
        return 1
    if x.scoreInfo.score < y.scoreInfo.score:
        return -1
    if x.scoreInfo.interval < y.scoreInfo.interval:
        return 1
    if x.scoreInfo.interval > y.scoreInfo.interval:
        return -1
    if x.scoreInfo.tWhen < y.scoreInfo.tWhen:
        return 1
    if x.scoreInfo.tWhen > y.scoreInfo.tWhen:
        return -1
    return 0


class ZhenyaoRank(UserSoleType):

    def __init__(self):
        self.rankList = []
        self.recordGroupNUIDs = set()

    def _lateReload(self):
        for v in self.rankList:
            if hasattr(v, 'reloadScript'):
                v.reloadScript()


class ZhenyaoSnapshotRankList(UserListType):

    def _lateReload(self):
        super(ZhenyaoSnapshotRankList, self)._lateReload()
        for v in self:
            if hasattr(v, 'reloadScript'):
                v.reloadScript()


class ZhenyaoSnapShotRank(UserDictType):

    def _lateReload(self):
        for v in self.itervalues():
            if hasattr(v, 'reloadScript'):
                v.reloadScript()


class ZhenyaoGroupMemberVal(UserSoleType):

    def __init__(self, isHeader = False, roleName = '', school = 0, lv = 0):
        super(ZhenyaoGroupMemberVal, self).__init__()
        self.isHeader = isHeader
        self.roleName = roleName
        self.school = school
        self.lv = lv


class ZhenyaoGroupMember(UserDictType):

    def _lateReload(self):
        super(ZhenyaoGroupMember, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def reset(self):
        self.clear()

    def pushMember(self, gbId, isHeader, roleName, school, lv):
        self[gbId] = ZhenyaoGroupMemberVal(isHeader, roleName, school, lv)

    def getMemberDTO(self):
        info = []
        for k, mVal in self.iteritems():
            info.append({'isHeader': mVal.isHeader,
             'roleName': mVal.roleName,
             'school': mVal.school,
             'level': mVal.lv})

        return info


class ZhenyaoGroupVal(UserSoleType):

    def __init__(self, groupName = '', groupMembers = ZhenyaoGroupMember()):
        super(ZhenyaoGroupVal, self).__init__()
        self.groupName = groupName
        self.groupMember = copy.deepcopy(groupMembers)

    def _lateReload(self):
        self.groupMember.reloadScript()


class ZhenyaoGroup(UserDictType):

    def _lateReload(self):
        for v in self.itervalues():
            if hasattr(v, 'reloadScript'):
                v.reloadScript()


class ZhenyaoFinalRankVal(UserSoleType):

    def __init__(self, scoreInfo = ZhenyaoScore(), group = ZhenyaoGroupVal(), groupNUID = 0):
        self.scoreInfo = scoreInfo
        self.group = group
        self.groupNUID = groupNUID

    def _lateReload(self):
        self.scoreInfo.reloadScript()
        self.group.reloadScript()


class ZhenyaoFinalRankList(UserSoleType):

    def __init__(self, finalScores = {}, finalRank = [], rankVersion = 1, scoreVersion = 1):
        self.finalScores = copy.deepcopy(finalScores)
        self.finalRank = finalRank
        self.rankVersion = rankVersion
        self.scoreVersion = scoreVersion

    def _lateReload(self):
        for k, v in self.finalScores.iteritems():
            if hasattr(v, 'reloadScript'):
                v.reloadScript()

        for v in self.finalRank:
            if hasattr(v, 'reloadScript'):
                v.reloadScript()


class ZhenyaoFinalRank(UserDictType):

    def _lateReload(self):
        for v in self.itervalues():
            if hasattr(v, 'reloadScript'):
                v.reloadScript()
