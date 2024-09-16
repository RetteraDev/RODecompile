#Embedded file name: I:/bag/tmp/tw2/res/entities\common/weekPrivilegeBuy.o
import gametypes
from userSoleType import UserSoleType
from userDictType import UserDictType

class WeekPrivilegeBuyInfoVal(UserSoleType):

    def __init__(self, group, privilegeId, privilegeStatus):
        self.group = group
        self.privilegeId = privilegeId
        self.privilegeStatus = privilegeStatus

    def _lateReload(self):
        super(WeekPrivilegeBuyInfoVal, self)._lateReload()


class WeekPrivilegeBuyInfo(UserDictType):

    def __init__(self):
        super(WeekPrivilegeBuyInfo, self).__init__()

    def _lateReload(self):
        super(WeekPrivilegeBuyInfo, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def checkGroupOpened(self, group):
        if not self.has_key(group):
            return False
        return True

    def checkGroupHasBuy(self, group):
        if not self.has_key(group):
            return False
        return self[group].privilegeStatus == gametypes.WEEK_PRIVILEGE_BUY_STATE_HAS_BUY

    def delWeekPrivilegeBuyInfo(self, group):
        self.pop(group, None)

    def updatePrivilegeBuyInfo(self, group, privilegeId, status):
        if not self.has_key(group):
            self[group] = WeekPrivilegeBuyInfoVal(group, privilegeId, status)
            return
        self[group].privilegeId = privilegeId
        self[group].privilegeStatus = status

    def getPrivilegeId(self, group):
        if not self.has_key(group):
            return 0
        return self[group].privilegeId

    def listPrivilegeBuyInfo(self):
        info = []
        for buyInfo in self.itervalues():
            info.append({'group': buyInfo.group,
             'privilegeId': buyInfo.privilegeId,
             'privilegeStatus': buyInfo.privilegeStatus})

        return info
