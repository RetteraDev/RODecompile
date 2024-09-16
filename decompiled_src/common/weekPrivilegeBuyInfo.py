#Embedded file name: I:/bag/tmp/tw2/res/entities\common/weekPrivilegeBuyInfo.o
from userInfo import UserInfo
from weekPrivilegeBuy import *

class weekPrivilegeBuyInfo(UserInfo):

    def createObjFromDict(self, dict):
        obj = WeekPrivilegeBuyInfo()
        for child in dict['data']:
            tmpVal = WeekPrivilegeBuyInfoVal(child['group'], child['privilegeId'], child['privilegeStatus'])
            obj[tmpVal.group] = tmpVal

        return obj

    def getDictFromObj(self, obj):
        info = []
        for tempInfo in obj.itervalues():
            tempValue = {'group': tempInfo.group,
             'privilegeId': tempInfo.privilegeId,
             'privilegeStatus': tempInfo.privilegeStatus}
            info.append(tempValue)

        return {'data': info}

    def isSameType(self, obj):
        return type(obj) is WeekPrivilegeBuyInfo


instance = weekPrivilegeBuyInfo()
