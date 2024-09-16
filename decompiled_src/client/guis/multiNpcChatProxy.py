#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/multiNpcChatProxy.o
from gamestrings import gameStrings
import random
import BigWorld
from Scaleform import GfxValue
import uiConst
import gamelog
import gameglobal
from ui import gbk2unicode
from uiProxy import UIProxy
from helpers import capturePhoto
from guis import uiUtils
from data import dialogs_data as GD
from data import dawdler_data as DD

class MultiNpcChatProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MultiNpcChatProxy, self).__init__(uiAdapter)
        self.modelMap = {'getMultiNpcChatInfo': self.onGetMultiNpcChatInfo,
         'getChatString': self.onGetChatString,
         'clickCloseBtn': self.onClickCloseBtn,
         'isQuestChat': self.onIsQuestChat,
         'accMultiNpcQuest': self.onAccMultiNpcQuest}
        self.modelId = 0
        self.entityId = None
        self.npcId = None
        self.choice = 0
        self.isQuestChat = True
        self.isShow = False
        self.isDawdler = True
        self.headGen = None
        self.hasQuest = False
        self.chatOption = []

    def openMultiNpcChatWindow(self, entityId, npcId, defaultChatId, isQuestChat, isDawdler = True, hasQuest = False):
        self.isDawdler = isDawdler
        self.entityId = entityId
        self.npcId = npcId
        self.isQuestChat = isQuestChat
        self.defaultChatId = defaultChatId
        self.hasQuest = hasQuest
        self.uiAdapter.openQuestWindow(uiConst.NPC_MULTI)

    def _getNpcName(self):
        try:
            npc = BigWorld.entity(self.entityId)
            if npc and npc.inWorld:
                return npc.roleName
            return uiUtils.getNpcName(self.npcId)
        except:
            gamelog.error(gameStrings.TEXT_FUNCNPCPROXY_128)

    def _getNpcChat(self):
        if len(self.defaultChatId):
            index = random.randint(0, len(self.defaultChatId) - 1)
            data = GD.data.get(self.defaultChatId[index], {})
            uiUtils.dealNpcSpeakEvents(data.get('speakEvent', None), self.entityId)
            return (data.get('details', ''), self.defaultChatId[index])
        else:
            return ('', -1)

    def _getOptionChat(self, index):
        if index < len(self.chatOption):
            try:
                chatIdList = self.chatOption[index][1]
                i = random.randint(0, len(chatIdList) - 1)
                self.choice = chatIdList[i]
                return GD.data.get(chatIdList[i], {}).get('details', '')
            except:
                gamelog.error(gameStrings.TEXT_FUNCNPCPROXY_128)

    def _getNpcOptions(self, movie):
        optionArray = movie.CreateArray()
        self.chatOption = DD.data.get(self.npcId, {}).get('chatOption', 0)
        if self.hasQuest:
            self.chatOption = list(self.chatOption)
            self.chatOption.append((gameStrings.TEXT_GROUPDETAILFACTORY_30, (4,)))
            self.chatOption = tuple(self.chatOption)
        if self.chatOption != 0:
            for index, item in enumerate(self.chatOption):
                optionArray.SetElement(index, GfxValue(gbk2unicode(item[0])))

        return optionArray

    def onGetMultiNpcChatInfo(self, *arg):
        movie = self.movie
        obj = movie.CreateObject()
        npcName = self._getNpcName()
        chat, chatId = self._getNpcChat()
        npc = BigWorld.entity(self.entityId)
        p = BigWorld.player()
        p.triggerNpcChat(npc.npcId, chatId)
        options = movie.CreateArray()
        obj.SetMember('name', GfxValue(gbk2unicode(npcName)))
        obj.SetMember('chat', GfxValue(gbk2unicode(chat)))
        obj.SetMember('options', options)
        self.initHeadGen(npc)
        return obj

    def onGetMultiNpcChatInfoPy(self):
        obj = {}
        npcName = self._getNpcName()
        chat, chatId = self._getNpcChat()
        npc = BigWorld.entity(self.entityId)
        p = BigWorld.player()
        p.triggerNpcChat(npc.npcId, chatId)
        options = []
        obj['npcId'] = self.entityId
        obj['name'] = npcName
        obj['chat'] = chat
        obj['options'] = options
        return obj

    def onGetChatString(self, *arg):
        movie = arg[0]
        index = int(arg[3][0].GetNumber())
        if self.isDawdler == True:
            chatArray = movie.CreateArray()
            npcName = self._getNpcName()
            chatStr = self._getOptionChat(index)
            gamelog.debug('hjx debug onGetChatString:', index, chatStr)
            dawdler = BigWorld.entities.get(self.entityId)
            gamelog.debug('@szh: onGetChatString', self.entityId, self.choice)
            if dawdler is not None:
                dawdler.onChatChoice(self.choice)
            chatArray.SetElement(0, GfxValue(gbk2unicode(npcName)))
            chatArray.SetElement(1, GfxValue(gbk2unicode(chatStr)))
            return chatArray
        else:
            return

    def close(self):
        if gameglobal.rds.ui.quest.isShow:
            self.uiAdapter.closeQuestWindow()
        if gameglobal.rds.ui.npcV2.isShow:
            gameglobal.rds.ui.npcV2.leaveStage()
        if self.isQuestChat:
            dawdler = BigWorld.entity(self.entityId)
            if dawdler:
                dawdler.onChatChoice(self.defaultChatId[0])

    def onAccMultiNpcQuest(self, *arg):
        self.close()

    def onClickCloseBtn(self, *arg):
        self.close()

    def onIsQuestChat(self, *arg):
        return GfxValue(self.isQuestChat)

    def onIsQuestChatPy(self):
        return self.isQuestChat

    def initHeadGen(self, npc):
        if not npc or not npc.inWorld:
            return
        if not self.headGen:
            self.headGen = capturePhoto.LargePhotoGen.getInstance('gui/taskmask.tga', 700)
        uiUtils.takePhoto3D(self.headGen, npc, npc.npcId)

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()
