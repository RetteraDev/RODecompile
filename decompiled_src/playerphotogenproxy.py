#Embedded file name: /WORKSPACE/data/entities/client/debug/playerphotogenproxy.o
import BigWorld
import Math
from Scaleform import GfxValue
import gamelog
import gameglobal
import keys
import clientUtils
from helpers import capturePhoto
from helpers import cameraControl
from guis.uiProxy import DataProxy
from guis import uiConst

class PlayerPhotoGenProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(PlayerPhotoGenProxy, self).__init__(uiAdapter)
        self.bindType = 'playerPhotoGen'
        self.modelMap = {'startBigPhotCapture': self.onStartBigPhotCapture,
         'startSmallPhotCapture': self.onStartSmallPhotCapture,
         'endCapture': self.onEndCapture,
         'saveData': self.onSaveData,
         'adjustLight': self.onAdjustLight,
         'adjustAction': self.onAdjustAction}
        self.destroyOnHide = True
        self.model = None
        self.tc = None
        self.ins = None
        self.mediator = None

    def hide(self, destroy = False):
        super(PlayerPhotoGenProxy, self).hide(destroy)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PLAYER_PHOTO_GEN)
        self.onEndCapture()
        self.mediator = None

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_PLAYER_PHOTO_GEN)

    def initCapture(self, matrix, light, light1, actionId, lightDir):
        p = BigWorld.player()
        self.model = clientUtils.model(*p.model.sources)
        self.tc = cameraControl.TC
        if self.tc == None:
            cameraControl.TC = BigWorld.TrackCamera()
            self.tc = cameraControl.TC
        BigWorld.camera(self.tc)
        self.tc.set(matrix)
        if self.ins == capturePhoto.bigPhoto:
            self.movie.invoke(('_root.showBigPlayerPhoto', GfxValue(2)))
        else:
            self.movie.invoke(('_root.showSmallPlayerPhoto', GfxValue(3)))
        self.ins.setModelDirectly(self.model)
        self.ins.adjustMatrix(matrix)
        self.ins.light = light
        self.ins.light1 = light1
        self.ins.lightDir = lightDir
        self.ins.dynamic = True
        self.ins.doAction(actionId)
        self.ins.refresh()

    def onStartBigPhotCapture(self, *arg):
        self.onEndCapture()
        self.ins = capturePhoto.bigPhoto
        matrix, light, light1, lightDir = self.ins.getPlayerMatrixAndLight()
        if arg[3][0].GetString():
            light = int(arg[3][0].GetString())
        if arg[3][1].GetString():
            light1 = int(arg[3][1].GetString())
        actionId = '1101'
        if arg[3][2].GetString():
            actionId = arg[3][2].GetString()
        if arg[3][3].GetString():
            lightDirStr = arg[3][3].GetString().split(',')
            for i, item in enumerate(lightDirStr):
                lightDir[i] = float(item)

        print 'onStartBigPhotCapture', light, light1, actionId
        self.initCapture(matrix, light, light1, actionId, lightDir)

    def onStartSmallPhotCapture(self, *arg):
        self.onEndCapture()
        self.ins = capturePhoto.SmallPhotoGen.getInstance()
        matrix, light, light1, lightDir = self.ins.getPlayerMatrixAndLight()
        if arg[3][0].GetString():
            light = int(arg[3][0].GetString())
        if arg[3][1].GetString():
            light1 = int(arg[3][1].GetString())
        actionId = '1101'
        if arg[3][2].GetString():
            actionId = arg[3][2].GetString()
        if arg[3][3].GetString():
            lightDirStr = arg[3][3].GetString().split(',')
            for i, item in enumerate(lightDirStr):
                lightDir[i] = float(item)

        print 'onStartBigPhotCapture1', light, light1, actionId
        self.initCapture(matrix, light, light1, actionId, lightDir)

    def onEndCapture(self, *arg):
        if self.ins:
            if self.ins == capturePhoto.bigPhoto:
                self.movie.invoke('_root.closeBigPlayerPhoto')
            else:
                self.movie.invoke('_root.closeSmallPlayerPhoto')
            self.ins.endCapture()
            BigWorld.camera(gameglobal.rds.cam.cc)
            self.model = None

    def onSaveData(self, *arg):
        if self.ins:
            self.ins.saveData()
            self.onEndCapture()

    def onAdjustLight(self, *arg):
        if arg[3][0].GetString():
            light = int(arg[3][0].GetString())
            if self.ins:
                self.ins.adjustLight(light)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def isShow(self):
        if self.mediator:
            return True
        return False

    def handleKeyEvent(self, down, key, vk, mods):
        gamelog.debug('handleKeyEvent', down, key, vk, mods)
        if key == keys.KEY_RIGHTMOUSE:
            self.tc.locked = down
        if key == keys.KEY_Z and down:
            self.onSaveData()
            return True
        if key == keys.KEY_C and self.light:
            if down and self.ins:
                self.ins.adjustLight(self.light)
            return True
        self.tc.handleTrackKeyEvent(down, key, vk, mods)
        m = Math.Matrix(self.tc.matrix)
        self.ins.adjustMatrix(m)
        return True

    def onAdjustAction(self, *arg):
        if arg[3][0].GetString():
            actionId = arg[3][0].GetString()
            if self.ins:
                self.ins.doAction(actionId)
