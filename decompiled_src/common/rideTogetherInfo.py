#Embedded file name: I:/bag/tmp/tw2/res/entities\common/rideTogetherInfo.o
"""
Created on 2014-7-4

@author: Administrator
"""
from userInfo import UserInfo
from rideTogether import RideTogether

class RideTogetherInfo(UserInfo):

    def createObjFromDict(self, dict):
        tride = RideTogether(header=dict['header'], typ=dict['typ'])
        for mval in dict['member']:
            tride[mval['id']] = mval['inx']

        return tride

    def getDictFromObj(self, obj):
        mvals = []
        for k, v in obj.iteritems():
            mvals.append({'id': k,
             'inx': v})

        return {'header': obj.header,
         'typ': obj.typ,
         'member': mvals}

    def isSameType(self, obj):
        return type(obj) is RideTogether


instance = RideTogetherInfo()
