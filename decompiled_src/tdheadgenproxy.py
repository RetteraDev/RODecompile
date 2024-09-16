#Embedded file name: /WORKSPACE/data/entities/client/debug/tdheadgenproxy.o
import Math
import BigWorld
import ResMgr
from Scaleform import GfxValue
import gameglobal
import const
import gamelog
import keys
import clientcom
import clientUtils
from guis.ui import gbk2unicode
from guis.uiProxy import DataProxy
from guis import uiConst
from guis import uiUtils
from helpers import capturePhoto
from helpers import cameraControl
from helpers import modelServer
from callbackHelper import Functor
from HomeFurniture import HomeFurniture
from data import npc_model_client_data as NCD
from data import equip_data as ED
from data import item_furniture_data as IFD

class TdHeadGenProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(TdHeadGenProxy, self).__init__(uiAdapter)
        self.bindType = 'tdHeadGen'
        self.modelMap = {'startCapture': self.onStartCapture,
         'saveData': self.onSaveData,
         'endCapture': self.onEndCapture,
         'showLight': self.onShowLight,
         'adjustPhotoSize': self.onAdjustPhotoSize,
         'playAction': self.onPlayAction,
         'searchNpcId': self.onSearchNpcId}
        self.roleList = []
        self.rolePath = None
        self.modelID = None
        self.headGen = None
        self.headGenMode = False
        self.tc = None
        self.oldCamera = None
        self.entityId = None
        self.npc = None
        self.lightInfo = None
        self.photoWidth = None
        self.photoHeight = None
        self.photoSize = uiConst.PHOTO_SIZE_BIG

    def scanRoleFile(self):
        prefixPath = 'char/'
        topSection = ResMgr.openSection(prefixPath)
        for key, value in topSection.iteritems():
            if str.isdigit(key):
                for i in value.iterkeys():
                    if i in ('base.model', 'a1.model'):
                        self.roleList.append(prefixPath + key + '/' + i)

    def scanNCD(self):
        dataTable = (NCD, ED, IFD)
        for i, table in enumerate(dataTable):
            if i == 1:
                keysVal = filter(lambda x: table.data[x].get('armorSType', 0) == 7, table.data.keys())
            else:
                keysVal = table.data.keys()
            keysVal.sort()
            modelSet = set([])
            for id in keysVal:
                data = table.data[id]
                modelId = data.get('model', 0) if data.get('model', 0) else data.get('modelId', 0)
                name = data.get('name', '')
                if modelId and modelId not in modelSet:
                    modelSet.add(modelId)
                    self.roleList.append(str(id) + ':' + name + ':' + str(modelId))

    def getRoleArray(self):
        i = 0
        ar = self.movie.CreateArray()
        if not self.roleList:
            self.scanNCD()
        for item in self.roleList:
            value = GfxValue(gbk2unicode(self.roleList[i]))
            ar.SetElement(i, value)
            i = i + 1

        return ar

    def getValue(self, key):
        if key == 'tdHeadGen.roleList':
            ar = self.getRoleArray()
            return ar

    def onStartCapture(self, *arg):
        btnName = arg[3][0].GetString()
        data = arg[3][1].GetString()
        if data:
            self.npcId = int(arg[3][1].GetString().split(':')[0])
            self.modelID = arg[3][1].GetString().split(':')[-1]
        else:
            self.npcId = NCD.data.iterkeys()[0]
        if arg[3][2].GetString():
            self.modelID = arg[3][2].GetString()
        if btnName == 'btnStart':
            self.photoSize = uiConst.PHOTO_SIZE_BIG
        elif btnName == 'btnSmallStart':
            self.photoSize = uiConst.PHOTO_SIZE_SMALL
        elif btnName == 'btnNpcStart':
            self.photoSize = uiConst.PHOTO_SIZE_NPC
        elif btnName == 'btnLeftLook':
            self.photoSize = uiConst.PHOTO_SIZE_LEFT
        elif btnName == 'btnRightLook':
            self.photoSize = uiConst.PHOTO_SIZE_RIGHT
        elif btnName == 'btnRide':
            self.photoSize = uiConst.PHOTO_SIZE_RIDE
        if not self.headGenMode:
            self.hidePlayer(True)
            self.createNpc()

    def onSaveData(self, *arg):
        if self.headGenMode:
            if self.photoSize == uiConst.PHOTO_SIZE_NPC:
                self.savePhoto()
            else:
                self.headGen.saveData(str(self.modelID), self.photoWidth, self.photoHeight)
                self._endCapture()
            self.headGenMode = False
            self.photoWidth = self.photoHeight = None

    def savePhoto(self):
        self.headGen.take()
        BigWorld.callback(1, self._savePhoto)

    def _savePhoto(self):
        if hasattr(self.headGen.adaptor, 'saveFrame'):
            modelId = NCD.data.get(self.npcId, {}).get('model', 0)
            self.headGen.adaptor.saveFrame('.\\headPhoto\\%d.png' % modelId)
        BigWorld.callback(1, self.endSavePhoto)

    def endSavePhoto(self):
        self._endCapture()

    def onEndCapture(self, *arg):
        if self.headGenMode:
            self._endCapture()
            self.headGenMode = False

    def _endCapture(self):
        self.hidePlayer(False)
        self.headGen.adaptor.attachment = None
        self.headGen.adaptor.transform = None
        self.destroyNpc()
        BigWorld.camera(self.oldCamera)
        self.uiAdapter.questPhoto.closeQuestPhoto()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_NPC_QUEST)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_AUTO_QUEST)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WIN_AND_MOUNT_UPGRADE)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_NPC_V2)

    def hidePlayer(self, flag):
        p = BigWorld.player()
        p.model.visible = not flag
        if flag:
            p.lockKey(gameglobal.KEY_POS_OFFLINE)
        else:
            p.unlockKey(gameglobal.KEY_POS_OFFLINE)

    def createNpc(self):
        gamelog.debug('bgf:createNpc', self.npcId)
        pos = Math.Vector3(0, 0, 0)
        faceDir = Math.Vector3(1, 0, 0)
        p = BigWorld.player()
        prop = {'npcId': self.npcId,
         'isScenario': gameglobal.SCENARIO_PLAY_NPC}
        self.entityId = BigWorld.createEntity('Npc', p.spaceID, 0, pos, faceDir, prop)
        self.npc = BigWorld.entity(self.entityId)
        gamelog.debug('bgf:createNpc', self.npc.firstFetchFinished)
        BigWorld.callback(0.5, self._testModelFinished)

    def _testModelFinished(self):
        npc = BigWorld.entity(self.entityId)
        gamelog.debug('bgf:_testModelFinished', npc.firstFetchFinished, npc.model)
        self.headGenMode = True
        if self.modelID and self.modelID.isdigit():
            if self.npcId in IFD.data:
                path = HomeFurniture.getModelPath(self.npcId).get('fullPath', None)
                if path:
                    model = clientUtils.model(path)
                    self.modelID = path.split('/')[-1].split('.')[0]
                else:
                    model = clientcom.getModel(int(self.modelID))
            else:
                model = clientcom.getModel(int(self.modelID))
            npc.fashion.setupModel(model)
            npc.modelServer = modelServer.SimpleModelServer(npc, False, False)
            npc.modelServer.attachModelFromData()
        npc.model.scale = (1, 1, 1)
        BigWorld.callback(0.5, Functor(self._showQuestPhoto, npc))

    def _showQuestPhoto(self, npc):
        if self.photoSize == uiConst.PHOTO_SIZE_SMALL:
            self.headGen = capturePhoto.SmallPhotoGen.getInstance('gui/taskmask.tga', 300)
            self.uiAdapter.loadWidget(uiConst.WIDGET_AUTO_QUEST)
        elif self.photoSize == uiConst.PHOTO_SIZE_BIG:
            self.headGen = capturePhoto.NpcV2LargePhotoGen.getInstance('gui/taskmask.tga', 1014, 1014)
            self.uiAdapter.loadWidget(uiConst.WIDGET_NPC_V2)
        elif self.photoSize == uiConst.PHOTO_SIZE_RIDE:
            self.headGen = capturePhoto.WingAndMountUpgradePhotoGen.getInstance('gui/taskmask.tga', 408)
            self.uiAdapter.loadWidget(uiConst.WIDGET_WIN_AND_MOUNT_UPGRADE)
        elif self.photoSize == uiConst.PHOTO_SIZE_NPC:
            self.headGen = capturePhoto.NpcV2PhotoGen.getInstance('gui/taskmask.tga', 110)
            self.uiAdapter.loadWidget(uiConst.WIDGET_NPC_V2)
        self.useTrackCamera()
        npc.am.patience = 1000

    def destroyNpc(self):
        BigWorld.destroyEntity(self.entityId)

    def useTrackCamera(self):
        self.tc = cameraControl.TC
        if self.tc == None:
            cameraControl.TC = BigWorld.TrackCamera()
            self.tc = cameraControl.TC
        self.oldCamera = gameglobal.rds.cam.cc
        self.tc.set(self.getCameraMatrix(self.npc.model))
        self.tc.needDecay = True
        BigWorld.camera(self.tc)
        BigWorld.enableCharLod(False)
        BigWorld.projection().nearPlane = 0.1

    def getCameraMatrix(self, model, dis = 2.5):
        return self.headGen.getDefaultMatrix(model)

    def checkMatrix(self):
        modelID = int(self.modelID)
        mat, light = self.headGen.getInfoFromXML(modelID)
        gamelog.debug('bgf:checkMatrix', mat)
        self.headGen.adjustMatrix(mat)
        self.tc.set(mat)

    def startCapture(self):
        gamelog.debug('bgf:startCapture')
        self.headGen.dynamic = True
        m = Math.Matrix(self.tc.matrix)
        self.headGen.adjustMatrix(m)
        npc = BigWorld.entity(self.entityId)
        self.headGen.setModelDirectly(npc)
        self.headGen.refresh()

    def handleKeyEvent(self, down, key, vk, mods):
        gamelog.debug('handleKeyEvent', down, key, vk, mods)
        if key == keys.KEY_RIGHTMOUSE:
            self.tc.locked = down
        if key == keys.KEY_Z and down:
            self.onSaveData()
            return True
        if key == keys.KEY_X:
            if down:
                self.checkMatrix()
            return True
        if key == keys.KEY_C and self.lightInfo:
            if down:
                self.headGen.adjustLight(*self.lightInfo)
            return True
        self.tc.handleTrackKeyEvent(down, key, vk, mods)
        m = Math.Matrix(self.tc.matrix)
        self.headGen.adjustMatrix(m)
        return True

    def showTdHeadGen(self):
        self.uiAdapter.movie.invoke(('_root.loadWidget', GfxValue(uiConst.WIDGET_DEBUG_TDHEADGEN)))

    def onShowLight(self, *arg):
        light1 = arg[3][0].GetString()
        light2 = arg[3][1].GetString()
        light2Dir = arg[3][2].GetString()
        exposure = arg[3][3].GetString()
        light1 = [ int(item) for item in light1.split(',') ]
        light2 = [ int(item) for item in light2.split(',') ]
        light2Dir = [ float(item) for item in light2Dir.split(',') ]
        exposure = [ float(item) for item in exposure.split(',') ]
        self.lightInfo = (light1,
         light2,
         light2Dir,
         exposure)
        self.headGen.adjustLight(light1, light2, light2Dir, exposure)

    def onAdjustPhotoSize(self, *arg):
        gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SYSTEM, '别挣扎了，调大小的功能已经废掉了，只是没空去掉ui而已', 'system')

    def onPlayAction(self, *arg):
        actionStr = arg[3][0].GetString()
        if actionStr:
            model = self.headGen.adaptor.attachment
            if model:
                model.action(actionStr)()

    def onSearchNpcId(self, *arg):
        prefix = arg[3][0].GetString()
        if prefix == '':
            return self.getRoleArray()
        if not self.roleList:
            self.scanNCD()
        ret = []
        for item in self.roleList:
            if item.find(prefix) != -1:
                ret.append(item)

        return uiUtils.array2GfxAarry(ret, True)
