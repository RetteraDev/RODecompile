#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/questPhotoProxy.o
from gamestrings import gameStrings
from Scaleform import GfxValue
import gameglobal
import uiConst
import gamelog
from ui import gbk2unicode
from uiProxy import UIProxy
from helpers import capturePhoto
HIDE_PLAYER_PHOTO = -1
HIDE_ALL_PHOTO = -2

class QuestPhotoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QuestPhotoProxy, self).__init__(uiAdapter)
        self.modelMap = {'config': self.onConfig,
         'regisiter': self.onRegisiter,
         'regisiterSmall': self.onRegisiterSmall}
        self.mc = None
        self.npcId = []
        self.hideFlag = False
        self.isShow = False
        self.headGen = None
        self.isConfig = False
        self.countNum = 0

    def onRegisiter(self, *arg):
        self.mc = arg[3][0]

    def onRegisiterSmall(self, *arg):
        self.mc = arg[3][0]

    def onConfig(self, *arg):
        self.isConfig = True
        if len(self.npcId) == 1:
            value = self.npcId.pop(0)
        elif len(self.npcId) >= 2:
            beforeValue, value = self.npcId[-2], self.npcId[-1]
            self.npcId = []
            if beforeValue == 0 and value == HIDE_PLAYER_PHOTO:
                value = HIDE_ALL_PHOTO
            else:
                value = beforeValue
        else:
            value = HIDE_ALL_PHOTO
        title = ''
        name = ''
        obj = self.movie.CreateObject()
        obj.SetMember('titleText', GfxValue(gbk2unicode(title)))
        obj.SetMember('nameText', GfxValue(gbk2unicode(name)))
        obj.SetMember('isLeft', GfxValue(value))
        gamelog.debug('onConfig', self.npcId, title)
        if gameglobal.rds.isSinglePlayer:
            obj.SetMember('titleText', GfxValue(gameStrings.TEXT_QUESTPHOTOPROXY_64))
            self.uiAdapter.tdHeadGen.startCapture()
        return obj

    def showQuestPhoto(self, npcId, photoSize = uiConst.PHOTO_SIZE_BIG):
        gamelog.debug('showQuestPhoto', npcId)
        if self.npcId and self.npcId[-1] == npcId:
            return
        if not self.countNum and npcId in (HIDE_PLAYER_PHOTO, HIDE_ALL_PHOTO):
            return
        self.countNum += 1
        self.npcId.append(npcId)
        if self.mc and self.isConfig:
            self.mc.Invoke('setContent', self.onConfig())
        elif npcId not in (HIDE_PLAYER_PHOTO, HIDE_ALL_PHOTO):
            if photoSize == uiConst.PHOTO_SIZE_BIG:
                self.uiAdapter.movie.invoke('_root.showTDPhoto')
            elif photoSize == uiConst.PHOTO_SIZE_SMALL:
                self.uiAdapter.movie.invoke('_root.showTDSmallPhoto')
            self.isShow = True
            self.isConfig = False

    def closeQuestPhoto(self):
        gamelog.debug('closeQuestPhoto', self.isShow)
        if self.isShow:
            self.uiAdapter.movie.invoke('_root.closeTDPhoto')
            self.uiAdapter.movie.invoke('_root.closeTDSmallPhoto')
            self.isShow = False
            self.mc = None
            self.countNum = 0
            self.npcId = []

    def adjustSize(self, w, h):
        if self.mc:
            self.mc.Invoke('adjustSize', (GfxValue(w), GfxValue(h)))

    def initHeadGen(self, modelId = 3001, tintMs = None, photoAction = None):
        if not self.headGen:
            self.headGen = capturePhoto.LargePhotoGen.getInstance('gui/taskmask.tga', 700)
        self.headGen.startCapture(modelId, tintMs, photoAction)

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()
