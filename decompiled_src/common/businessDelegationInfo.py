#Embedded file name: I:/bag/tmp/tw2/res/entities\common/businessDelegationInfo.o
from userInfo import UserInfo
from businessDelegation import AccBusiness, BusinessDelegations, BusinessDelegationVal

class AccBusinessInfo(UserInfo):

    def createObjFromDict(self, acDict):
        accBusiness = AccBusiness(acDict['acNUID'], acDict['acGbId'], acDict['acRoleName'])
        accBusiness.acWhen = acDict['acWhen']
        accBusiness.compWhen = acDict['compWhen']
        return accBusiness

    def getDictFromObj(self, obj):
        accBusinessInfo = {'acNUID': obj.acNUID,
         'acGbId': obj.acGbId,
         'acRoleName': obj.acRoleName,
         'acWhen': obj.acWhen,
         'compWhen': obj.compWhen}
        return accBusinessInfo

    def isSameType(self, obj):
        return type(obj) is AccBusiness


accBusinessInstance = AccBusinessInfo()

class BusinessDelegationInfo(UserInfo):

    def createObjFromDict(self, busDict):
        businessDelegations = BusinessDelegations()
        businessDelegations.dailyDgtCnt = busDict['dailyDgtCnt']
        businessDelegations.curDgtCnt = busDict['curDgtCnt']
        for businessDelegationsInfo in busDict['businessDelegations']:
            nuid = businessDelegationsInfo['nuid']
            employerGbId = businessDelegationsInfo['employerGbId']
            employerRoleName = businessDelegationsInfo['employerRoleName']
            questLoopId = businessDelegationsInfo['questLoopId']
            dgtCnt = businessDelegationsInfo['dgtCnt']
            loopCashReward = businessDelegationsInfo['loopCashReward']
            tWhen = businessDelegationsInfo['tWhen']
            businessDelegationVal = BusinessDelegationVal(employerGbId, employerRoleName, questLoopId, dgtCnt, loopCashReward)
            businessDelegationVal.tWhen = tWhen
            for accBusiness in businessDelegationsInfo['accBusiness']:
                businessDelegationVal[accBusiness.acNUID] = accBusiness

            businessDelegations[nuid] = businessDelegationVal

        return businessDelegations

    def getDictFromObj(self, obj):
        businessDelegationsInfos = []
        for nuid, businessDelegationVal in obj.iteritems():
            employerGbId = businessDelegationVal.gbId
            employerRoleName = businessDelegationVal.roleName
            questLoopId = businessDelegationVal.questLoopId
            loopCashReward = businessDelegationVal.loopCashReward
            dgtCnt = businessDelegationVal.dgtCnt
            tWhen = businessDelegationVal.tWhen
            businessDelegationsInfos.append({'nuid': nuid,
             'employerGbId': employerGbId,
             'employerRoleName': employerRoleName,
             'questLoopId': questLoopId,
             'loopCashReward': loopCashReward,
             'dgtCnt': dgtCnt,
             'tWhen': tWhen,
             'accBusiness': [ x for x in businessDelegationVal.itervalues() ]})

        return {'businessDelegations': businessDelegationsInfos,
         'dailyDgtCnt': obj.dailyDgtCnt,
         'curDgtCnt': obj.curDgtCnt}

    def isSameType(self, obj):
        return type(obj) is BusinessDelegations


instance = BusinessDelegationInfo()
