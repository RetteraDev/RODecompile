#Embedded file name: /WORKSPACE/data/entities/common/teamendlesshistory.o
import gamelog
import random
import const
import BigWorld
from userSoleType import UserSoleType
from userDictType import UserDictType

class TeamEndlessHistoryVal(UserSoleType):

    def __init__(self, fbNo = 0, teamEndlessLv = 1, timeCost = 0, timestamp = 0, version = 0):
        super(TeamEndlessHistoryVal, self).__init__()
        self.fbNo = fbNo
        self.teamEndlessLv = teamEndlessLv
        self.timeCost = timeCost
        self.timestamp = timestamp
        self.version = version


class TeamEndlessHistory(UserDictType):

    def _lateReload(self):
        super(TeamEndlessHistory, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def pushVal(self, fbNo, teamEndlessLv, timeCost, timestamp, version = 0):
        self[fbNo] = TeamEndlessHistoryVal(fbNo=fbNo, teamEndlessLv=teamEndlessLv, timeCost=timeCost, timestamp=timestamp, version=version)

    def updateVal(self, fbNo, lv, timeCost, timestamp, version = 0):
        if not self.has_key(fbNo):
            return
        self[fbNo].teamEndlessLv = lv
        self[fbNo].timeCost = timeCost
        self[fbNo].timestamp = timestamp
        self[fbNo].version = version

    def getRecord(self, fbNo, gbId):
        if not self.has_key(fbNo):
            return (gbId,
             0,
             0,
             0)
        val = self[fbNo]
        return (gbId,
         val.teamEndlessLv,
         val.timeCost,
         val.timestamp)
