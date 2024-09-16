#Embedded file name: I:/bag/tmp/tw2/res/entities\common/spriteChat.o
from userSoleType import UserSoleType
from userDictType import UserDictType

class SpriteChatVal(UserSoleType):

    def __init__(self, text = ''):
        super(SpriteChatVal, self).__init__()
        self.chatText = text


class SpriteChat(UserDictType):

    def __init__(self):
        super(SpriteChat, self).__init__()

    def _lateReload(self):
        super(SpriteChat, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()


class SpriteChatDict(UserDictType):

    def __init__(self):
        super(SpriteChatDict, self).__init__()

    def _lateReload(self):
        super(SpriteChatDict, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def transfer(self, owner):
        owner.client.onSyncSpriteChats(self)

    def getChatText(self, spriteIndex, chatNo):
        if self.has_key(spriteIndex) and self[spriteIndex].has_key(chatNo):
            return self[spriteIndex][chatNo].chatText

    def setChatText(self, spriteIndex, chatNo, text):
        if not self.has_key(spriteIndex):
            self[spriteIndex] = SpriteChat()
        self[spriteIndex][chatNo] = SpriteChatVal(text=text)

    def resetChatText(self, spriteIndex, chatNo):
        if self.has_key(spriteIndex):
            self[spriteIndex].pop(chatNo, None)
            if not self[spriteIndex]:
                self.pop(spriteIndex, None)

    def onDeleteSprite(self, spriteIndex):
        self.pop(spriteIndex, None)
