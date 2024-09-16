#Embedded file name: I:/bag/tmp/tw2/res/entities\common/delegationRecordList.o
from userSoleType import UserSoleType
from userListType import UserListType

class DelegationRecordListValue(UserSoleType):

    def __init__(self, rid = 0, time = 0):
        super(DelegationRecordListValue, self).__init__()
        self.rid = rid
        self.time = time


class DelegationRecordList(UserListType):

    def _lateReload(self):
        super(DelegationRecordList, self)._lateReload()
        for pos in xrange(len(self)):
            self[pos].reloadScript()
