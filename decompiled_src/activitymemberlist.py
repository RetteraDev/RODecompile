#Embedded file name: /WORKSPACE/data/entities/common/activitymemberlist.o
import const
import gametypes
import utils
from userType import UserDispatch, UserMultiDispatch
from userSoleType import UserSoleType
from userDictType import UserDictType

class MemberListVal(UserSoleType, UserDispatch):

    def __init__(self, gbId = 0):
        super(MemberListVal, self).__init__()
        self.gbId = gbId


class MemberList(UserDictType, UserMultiDispatch):

    def __init__(self, leaderGbId = 0):
        super(MemberList, self).__init__()
        self.leaderGbId = leaderGbId

    def _lateReload(self):
        super(MemberList, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()
