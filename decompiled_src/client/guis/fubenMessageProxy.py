#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fubenMessageProxy.o
from Scaleform import GfxValue
import gameglobal
import uiConst
from ui import gbk2unicode
from uiProxy import UIProxy
from helpers import capturePhoto
from guis import uiUtils
from data import npc_model_client_data as NMCD
from data import dialogs_data as DD

class FubenMessageProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FubenMessageProxy, self).__init__(uiAdapter)
        self.modelMap = {'getAutoQuestInfo': self.onGetAutoQuestInfo,
         'setUnitType': self.onSetUnitType,
         'setUnitIndex': self.onSetUnitIndex}
        self.headGen = None
        self.mediator = None
        self.destroyOnHide = True
        self.simpleInfo = None
        self.model = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_FUBEN_MESSAGE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FUBEN_MESSAGE:
            self.mediator = mediator
            self.initHeadGen()

    def onGetAutoQuestInfo(self, *arg):
        return self.onGetSimpleQuestInfo()

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FUBEN_MESSAGE)
        self.resetHeadGen()

    def reset(self):
        self.simpleInfo = None
        self.mediator = None
        self.model = None

    def takePhoto3D(self, npcId):
        if not self.headGen:
            self.headGen = capturePhoto.TinyPhotoGen.getInstance('gui/taskmask.tga', 74)
        uiUtils.takePhoto3D(self.headGen, None, npcId)

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.TinyPhotoGen.getInstance('gui/taskmask.tga', 74)
        self.headGen.initFlashMesh()

    def onSetUnitType(self, *arg):
        npcId = int(arg[3][0].GetString())
        self.takePhoto3D(npcId)

    def onSetUnitIndex(self, *arg):
        npcId, chatId = self.simpleInfo
        data = DD.data.get(chatId, {})
        soundId = data.get('soundId', 0)
        if soundId:
            gameglobal.rds.sound.playSound(soundId)

    def isShow(self):
        if self.mediator:
            return True
        return False

    def show(self, npcId, chatId):
        if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            return
        self.simpleInfo = (npcId, chatId)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FUBEN_MESSAGE)
        self.uiAdapter.loadWidget(uiConst.WIDGET_FUBEN_MESSAGE)

    def onGetSimpleQuestInfo(self):
        if not self.simpleInfo:
            return
        movie = self.movie
        obj = movie.CreateObject()
        questArray = movie.CreateArray()
        nullArray = movie.CreateArray()
        npcId, chatId = self.simpleInfo
        objat = movie.CreateObject()
        nameArr = movie.CreateArray()
        asideId = movie.CreateArray()
        interval = movie.CreateArray()
        idArr = movie.CreateArray()
        wordList = movie.CreateArray()
        nmcd = NMCD.data.get(npcId, {})
        nameArr.SetElement(0, GfxValue(gbk2unicode(nmcd.get('name', ''))))
        idArr.SetElement(0, GfxValue(npcId))
        data = DD.data.get(chatId, {})
        desc = data.get('details', '')
        interval0 = data.get('interval', 5)
        wordList.SetElement(0, GfxValue(gbk2unicode(desc)))
        interval.SetElement(0, GfxValue(interval0))
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
