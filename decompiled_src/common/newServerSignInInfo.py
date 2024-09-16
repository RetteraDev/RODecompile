#Embedded file name: I:/bag/tmp/tw2/res/entities\common/newServerSignInInfo.o
from newServerSignIn import NewServerSignIn, NewServerSignInVal
from userInfo import UserInfo

class NewServerSignInInfo(UserInfo):

    def createObjFromDict(self, dic):
        obj = NewServerSignIn()
        for k, v in zip(dic['ids'], dic['vals']):
            val = NewServerSignInVal(k)
            val.dates = v['dates']
            if v.has_key('resignCnt'):
                val.resignCnt = v['resignCnt']
            if v.has_key('exactDayBonus'):
                val.exactDayBonus = v['exactDayBonus']
            obj[k] = val

        return obj

    def getDictFromObj(self, obj):
        keys = []
        vals = []
        for k, v in obj.iteritems():
            keys.append(k)
            vals.append({'id': v.id,
             'dates': v.dates,
             'resignCnt': v.resignCnt,
             'exactDayBonus': v.exactDayBonus})

        return {'ids': keys,
         'vals': vals}

    def isSameType(self, obj):
        return type(obj) is NewServerSignIn


instance = NewServerSignInInfo()
