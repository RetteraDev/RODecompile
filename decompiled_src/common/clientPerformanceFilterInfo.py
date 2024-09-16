#Embedded file name: I:/bag/tmp/tw2/res/entities\common/clientPerformanceFilterInfo.o
from userInfo import UserInfo
from clientPerformanceFilter import *

class clientPerformanceFilterInfo(UserInfo):

    def createObjFromDict(self, dict):
        obj = ClientPerformanceFilterInfo()
        for child in dict['data']:
            tmpVal = ClientPerformanceFilterVal(child['id'], child['name'], child['condition'], child['interval'], child['prob'], child['gbId'], child['urs'])
            obj[tmpVal.id] = tmpVal

        return obj

    def getDictFromObj(self, obj):
        info = []
        for tempInfo in obj.itervalues():
            tempValue = {'id': tempInfo.id,
             'name': tempInfo.name,
             'condition': tempInfo.condition,
             'interval': tempInfo.interval,
             'prob': tempInfo.prob,
             'gbId': tempInfo.gbId,
             'urs': tempInfo.urs}
            info.append(tempValue)

        return {'data': info}

    def isSameType(self, obj):
        return type(obj) is ClientPerformanceFilterInfo


instance = clientPerformanceFilterInfo()
