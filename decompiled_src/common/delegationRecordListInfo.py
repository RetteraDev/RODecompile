#Embedded file name: I:/bag/tmp/tw2/res/entities\common/delegationRecordListInfo.o
from userInfo import UserInfo
from delegationRecordList import DelegationRecordListValue, DelegationRecordList

class DelegationRecordListInfo(UserInfo):

    def createObjFromDict(self, dict):
        delegations = DelegationRecordList()
        for child in dict['delegationRecords']:
            cVal = DelegationRecordListValue(rid=child['rid'], time=child['time'])
            delegations.append(cVal)

        return delegations

    def getDictFromObj(self, obj):
        dVals = []
        for pos in xrange(len(obj)):
            dVals.append({'rid': obj[pos].rid,
             'time': obj[pos].time})

        return {'delegationRecords': dVals}

    def isSameType(self, obj):
        return type(obj) is DelegationRecordList


instance = DelegationRecordListInfo()
