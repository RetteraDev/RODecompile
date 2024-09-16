#Embedded file name: I:/bag/tmp/tw2/res/entities\common/carrouselSeatsInfo.o
"""
Created on 2014-7-4

@author: Administrator
"""
from userInfo import UserInfo
from carrouselSeats import CarrouselSeats

class CarrouselSeatsInfo(UserInfo):

    def createObjFromDict(self, dict):
        seats = CarrouselSeats()
        for mval in dict['member']:
            seats[mval['id']] = mval['inx']

        return seats

    def getDictFromObj(self, obj):
        mvals = []
        for k, v in obj.iteritems():
            mvals.append({'id': k,
             'inx': v})

        return {'member': mvals}

    def isSameType(self, obj):
        return type(obj) is CarrouselSeats


instance = CarrouselSeatsInfo()
