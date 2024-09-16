#Embedded file name: I:/bag/tmp/tw2/res/entities\common/noviceDailyOnlineInfo.o
from noviceDailyOnline import NoviceDailyOnline
from userInfo import UserInfo

class NoviceDailyOnlineInfo(UserInfo):

    def createObjFromDict(self, dict):
        obj = NoviceDailyOnline(dict['phase'], dict['total'], dict['start'])
        return obj

    def getDictFromObj(self, obj):
        return {'phase': obj.phase,
         'start': obj.start,
         'total': obj.total}

    def isSameType(self, obj):
        return type(obj) is NoviceDailyOnline


instance = NoviceDailyOnlineInfo()
