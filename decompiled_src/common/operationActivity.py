#Embedded file name: I:/bag/tmp/tw2/res/entities\common/operationActivity.o
import gametypes
from userSoleType import UserSoleType
from userDictType import UserDictType

class OperationActivityInfoVal(UserSoleType):

    def __init__(self, id, progress = 0, status = False):
        self.id = id
        self.progress = progress
        self.status = status

    def _lateReload(self):
        super(OperationActivityInfoVal, self)._lateReload()


class OperationActivityInfo(UserDictType):

    def __init__(self):
        super(OperationActivityInfo, self).__init__()

    def _lateReload(self):
        super(OperationActivityInfo, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def addActivityProgress(self, id, progressAdd):
        if not self.has_key(id):
            self[id] = OperationActivityInfoVal(id, progressAdd)
            return
        self[id].progress += progressAdd

    def updateActivityStatus(self, id, status):
        if not self.has_key(id):
            self[id] = OperationActivityInfoVal(id, status=status)
            return
        self[id].status = status

    def updateActivityInfo(self, id, progress, status):
        if not self.has_key(id):
            self[id] = OperationActivityInfoVal(id, progress, status)
            return
        self[id].progress = progress
        self[id].status = status

    def delActivityInfo(self, id):
        self.pop(id, None)

    def checkProgress(self, id, progress):
        if not self.has_key(id):
            return False
        return self[id].progress >= progress

    def checkStatus(self, id):
        if not self.has_key(id):
            return True
        return self[id].status == False

    def listActivityInfo(self):
        info = []
        for tempInfo in self.itervalues():
            info.append({'id': tempInfo.id,
             'progress': tempInfo.progress,
             'status': tempInfo.status})

        return info
