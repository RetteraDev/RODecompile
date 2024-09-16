#Embedded file name: /WORKSPACE/data/entities/common/teamendlesshistoryinfo.o
from userInfo import UserInfo
from teamEndlessHistory import TeamEndlessHistory

class TeamEndlessHistoryInfo(UserInfo):

    def createObjFromDict(self, d):
        obj = TeamEndlessHistory()
        for tVal in d['history']:
            obj.pushVal(fbNo=tVal['fbNo'], teamEndlessLv=tVal['teamEndlessLv'], timeCost=tVal['timeCost'], timestamp=tVal['timestamp'], version=tVal['version'])

        return obj

    def getDictFromObj(self, obj):
        data = []
        for fbNo, item in obj.iteritems():
            data.append({'fbNo': fbNo,
             'teamEndlessLv': item.teamEndlessLv,
             'timeCost': item.timeCost,
             'timestamp': item.timestamp,
             'version': item.version})

        return {'history': data}

    def isSameType(self, obj):
        return type(obj) is TeamEndlessHistory


instance = TeamEndlessHistoryInfo()
