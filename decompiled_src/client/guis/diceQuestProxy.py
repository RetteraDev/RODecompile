#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/diceQuestProxy.o
import BigWorld
import gameglobal
import uiConst
import gamelog
from uiProxy import UIProxy
from helpers import capturePhoto
from guis import uiUtils
from data import quest_dialog_data as QDD

class DiceQuestProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DiceQuestProxy, self).__init__(uiAdapter)
        self.modelMap = {'getDiceQuestInfo': self.onGetDiceQuestInfo,
         'setUnitType': self.onSetUnitType,
         'setUnitIndex': self.onSetUnitIndex,
         'acceptDiceQuest': self.onAcceptDiceQuest}
        self.headGen = None
        self.mediator = None
        self.destroyOnHide = True
        self.chatId = None
        self.model = None
        self.questLoopId = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_DICE_QUEST, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DICE_QUEST:
            self.mediator = mediator

    def onGetDiceQuestInfo(self, *arg):
        return self.onGetSimpleQuestInfo()

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_DICE_QUEST)
        self.resetHeadGen()

    def reset(self):
        self.chatId = None
        self.mediator = None
        self.model = None
        self.questLoopId = None

    def takePhoto3D(self, npcId):
        if not self.headGen:
            self.headGen = capturePhoto.TinyPhotoGen.getInstance('gui/taskmask.tga', 190)
        uiUtils.takePhoto3D(self.headGen, None, npcId)

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def onSetUnitType(self, *arg):
        return
        npcId = int(arg[3][0].GetString())
        gamelog.debug('wy:onSetUnitType', npcId)
        self.takePhoto3D(npcId)

    def onSetUnitIndex(self, *arg):
        return
        data = QDD.data.get(self.chatId, {})
        soundId = data.get('soundId', 0)
        if soundId:
            gameglobal.rds.sound.playSound(soundId)

    def isShow(self):
        if self.mediator:
            return True
        return False

    def show(self, questLoopId, chatId):
        if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            return
        self.questLoopId = questLoopId
        self.chatId = chatId
        self.uiAdapter.loadWidget(uiConst.WIDGET_DICE_QUEST)

    def onGetSimpleQuestInfo(self):
        if not self.chatId:
            return
        movie = self.movie
        obj = movie.CreateObject()
        questArray = movie.CreateArray()
        nullArray = movie.CreateArray()
        objat = movie.CreateObject()
        data = QDD.data.get(self.chatId, {})
        asideId = uiUtils.array2GfxAarry(data.get('aside', []), True)
        interval = uiUtils.array2GfxAarry(data.get('interval', []), True)
        idArr = uiUtils.array2GfxAarry(data.get('npcId', []), True)
        npcIds = data.get('npcId', [])
        nameArr = []
        for npcId in npcIds:
            if npcId == 0:
                nameArr.append(BigWorld.player().realRoleName)
            else:
                nameArr.append(uiUtils.getNpcName(npcId))

        nameArr = uiUtils.array2GfxAarry(nameArr, True)
        wordList = list(data.get('chat', []))
        for i, chat in enumerate(wordList):
            wordList[i] = chat.replace('$p', BigWorld.player().realRoleName)

        wordList = uiUtils.array2GfxAarry(wordList, True)
        objat.SetMember('speakerName', nameArr)
        objat.SetMember('asideIds', asideId)
        objat.SetMember('interval', interval)
        objat.SetMember('idList', idArr)
        objat.SetMember('words', wordList)
        questArray.SetElement(0, objat)
        obj.SetMember('available_tasks', questArray)
        obj.SetMember('unfinished_tasks', nullArray)
        obj.SetMember('complete_tasks', nullArray)
        obj.SetMember('available_taskLoops', nullArray)
        obj.SetMember('unfinished_taskLoops', nullArray)
        obj.SetMember('complete_taskLoops', nullArray)
        return obj

    def onAcceptDiceQuest(self, *arg):
        gamelog.debug('onAcceptDiceQuest', self.questLoopId)
        if self.questLoopId:
            p = BigWorld.player()
            p.cell.acceptQuestLoopByDice(self.questLoopId)
            self.hide()
