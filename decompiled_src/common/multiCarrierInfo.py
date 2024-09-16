#Embedded file name: I:/bag/tmp/tw2/res/entities\common/multiCarrierInfo.o
import gamelog
from userInfo import UserInfo
from multiCarrier import MultiCarrier, MultiCarrierCopy

class MultiCarrierInfo(UserInfo):

    def createObjFromDict(self, dict):
        carrier = MultiCarrier(carrierEntId=dict['carrierEntId'], carrierNo=dict['carrierNo'], carrierEnterType=dict['carrierEnterType'], carrierState=dict['carrierState'])
        for mval in dict['member']:
            carrier[mval['id']] = mval['idx']

        return carrier

    def getDictFromObj(self, obj):
        mvals = []
        for k, v in obj.iteritems():
            mvals.append({'id': k,
             'idx': v})

        return {'carrierEntId': obj.carrierEntId,
         'carrierNo': obj.carrierNo,
         'carrierEnterType': obj.carrierEnterType,
         'carrierState': obj.carrierState,
         'member': mvals}

    def isSameType(self, obj):
        return type(obj) is MultiCarrier


instance = MultiCarrierInfo()

class MultiCarrierCopyInfo(UserInfo):

    def createObjFromDict(self, dict):
        carrierCopy = MultiCarrierCopy(dict['spaceNo'], dict['position'], dict['direction'], dict['carrierBox'])
        return carrierCopy

    def getDictFromObj(self, obj):
        return {'spaceNo': obj.spaceNo,
         'position': obj.position,
         'direction': obj.direction,
         'carrierBox': obj.carrierBox}

    def isSameType(self, obj):
        return type(obj) is MultiCarrierCopy


copyInstance = MultiCarrierCopyInfo()
