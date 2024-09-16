#Embedded file name: I:/bag/tmp/tw2/res/entities\common/wingWorldCarrierInfo.o
from userInfo import UserInfo
from wingWorldCarrierData import WingWorldCarrierData

class WingWorldCarrierInfo(UserInfo):

    def createObjFromDict(self, dict):
        carrier = WingWorldCarrierData(carrierEntId=dict['carrierEntId'], carrierNo=dict['carrierNo'], enterTypeOption=dict['enterTypeOption'], isBecomeLadder=dict['isBecomeLadder'])
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
         'enterTypeOption': obj.enterTypeOption,
         'member': mvals,
         'isBecomeLadder': obj.isBecomeLadder}

    def isSameType(self, obj):
        return type(obj) is WingWorldCarrierData


instance = WingWorldCarrierInfo()
