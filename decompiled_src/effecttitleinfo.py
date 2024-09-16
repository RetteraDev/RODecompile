#Embedded file name: /WORKSPACE/data/entities/common/effecttitleinfo.o
import BigWorld
if BigWorld.component != 'database':
    from effectTitle import EffectTitle, EffectTitleVal
from userInfo import UserInfo

class EffectTitleInfo(UserInfo):

    def createObjFromDict(self, dict):
        titles = EffectTitle()
        for val in dict['titles']:
            titles[val['title']] = EffectTitleVal(val)

        return titles

    def getDictFromObj(self, obj):
        vals = []
        for v in obj.itervalues():
            vals.append({'title': v.title,
             'tGain': v.tGain,
             'tExpired': v.tExpired,
             'effectLv': v.effectLv,
             'tAttr': v.tAttr})

        return {'titles': vals}

    def isSameType(self, obj):
        return type(obj) is EffectTitle


instance = EffectTitleInfo()
