#Embedded file name: I:/bag/tmp/tw2/res/entities\common/operationActivityInfo.o
from userInfo import UserInfo
from operationActivity import *

class operationActivityInfo(UserInfo):

    def createObjFromDict(self, dict):
        obj = OperationActivityInfo()
        for child in dict['data']:
            tmpVal = OperationActivityInfoVal(child['id'], child['progress'], child['status'])
            obj[tmpVal.id] = tmpVal

        return obj

    def getDictFromObj(self, obj):
        info = []
        for tempInfo in obj.itervalues():
            tempValue = {'id': tempInfo.id,
             'progress': tempInfo.progress,
             'status': tempInfo.status}
            info.append(tempValue)

        return {'data': info}

    def isSameType(self, obj):
        return type(obj) is OperationActivityInfo


instance = operationActivityInfo()
