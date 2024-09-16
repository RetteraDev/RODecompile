#Embedded file name: I:/bag/tmp/tw2/res/entities\common/spriteChatInfo.o
from spriteChat import SpriteChatVal, SpriteChat, SpriteChatDict
from userInfo import UserInfo

class SpriteChatInfo(UserInfo):

    def createObjFromDict(self, fDict):
        sChat = SpriteChat()
        for val in fDict['data']:
            sChatVal = SpriteChatVal(val['chatText'])
            sChat[val['chatNo']] = sChatVal

        return sChat

    def getDictFromObj(self, obj):
        tVals = []
        for chatNo, tVal in obj.iteritems():
            tVals.append({'chatNo': chatNo,
             'chatText': tVal.chatText})

        return {'data': tVals}

    def isSameType(self, obj):
        return type(obj) is SpriteChat


chatInfoInstance = SpriteChatInfo()

class SpriteChatDictInfo(UserInfo):

    def createObjFromDict(self, fDict):
        sChatDict = SpriteChatDict()
        for i, tVal in enumerate(fDict['data']):
            sChatDict[fDict['spriteIndexes'][i]] = tVal

        return sChatDict

    def getDictFromObj(self, obj):
        spriteIndexes = []
        tVals = []
        for spriteIndex, spriteChat in obj.iteritems():
            spriteIndexes.append(spriteIndex)
            tVals.append(spriteChat)

        return {'data': tVals,
         'spriteIndexes': spriteIndexes}

    def isSameType(self, obj):
        return type(obj) is SpriteChatDict


chatDictInfoInstance = SpriteChatDictInfo()
