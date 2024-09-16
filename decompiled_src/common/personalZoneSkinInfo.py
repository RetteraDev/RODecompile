#Embedded file name: I:/bag/tmp/tw2/res/entities\common/personalZoneSkinInfo.o
from personalZoneSkin import PersonalZoneSkinVal, PersonalZoneSkinDict
from userInfo import UserInfo

class PersonalZoneSkinDictInfo(UserInfo):

    def createObjFromDict(self, dict):
        skinDict = PersonalZoneSkinDict()
        if dict:
            if dict.has_key('data') and dict['data']:
                for sVal in dict['data']:
                    skin = PersonalZoneSkinVal(sVal['skinId'])
                    skin.expireTime = sVal['expireTime']
                    skinDict[sVal['skinId']] = skin

            if dict.has_key('curUseSkinId'):
                skinDict.curUseSkinId = dict['curUseSkinId']
        return skinDict

    def getDictFromObj(self, obj):
        data = []
        for skin in obj.itervalues():
            data.append({'skinId': skin.skinId,
             'expireTime': skin.expireTime})

        return {'data': data,
         'curUseSkinId': obj.curUseSkinId}

    def isSameType(self, obj):
        return type(obj) is PersonalZoneSkinDict


instance = PersonalZoneSkinDictInfo()
