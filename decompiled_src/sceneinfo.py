#Embedded file name: /WORKSPACE/data/entities/client/helpers/sceneinfo.o
import BigWorld
import Math
import gameglobal
import gametypes
import gamelog
import formula
import appSetting
import clientUtils
from gameclass import Singleton
from gameChunk import resideInSafetyZone, resideInBorderZone
from helpers.stateSafe import checkInterval
from helpers import protect
from callbackHelper import Functor
from sfx import sfx
from data import wing_world_config_data as WWCD
from data import area_event_data as AVD
from data import map_config_data as MCD
from data import chunk_mapping_data as CMD
from data import sys_config_data as SCD
from data import clan_war_fort_data as CWFD
from cdata import game_msg_def_data as GMDD
gAreaInfoInited = False

def startShowInfo():
    global gAreaInfoInited
    if gAreaInfoInited:
        return
    gAreaInfoInited = True
    showInfoName()


def showInfoName():
    global gAreaInfoObj
    TIME_SPAN = 1
    gAreaInfoObj.showAreaInfo()
    BigWorld.callback(TIME_SPAN, showInfoName)


class AreaInfo(object):
    __metaclass__ = Singleton
    TIME_SPAN = 5
    WORD_NUM = 20

    def __init__(self):
        self.lastName = ''
        self.lastShowName = ''
        self.lastSpaceNo = 0
        self.fadeinid = 0
        self.hideid = 0
        self.inSafetyZone = False
        self.inBorderZone = False
        self.lastNepMapId = 0
        self.lastSkyboxInfo = {}

    def showAreaInfo(self):
        if gameglobal.rds.GameState != gametypes.GS_PLAYGAME:
            return False
        name = self.getAreaInfo()
        if name == 'chuhaigangkou':
            BigWorld.setViewFactor(0.33)
        elif name == 'fb_mh':
            BigWorld.setViewFactor(1.1)
        else:
            factor = appSetting.VideoQualitySettingObj.getViewFactor()
            BigWorld.setViewFactor(factor)
        p = BigWorld.player()
        rs = False
        if not name:
            pass
        elif len(name) > AreaInfo.WORD_NUM * 2:
            gamelog.debug('err area name len > 8 word')
        elif name != self.lastName or self.lastSpaceNo != p.spaceNo:
            gamelog.debug('jjh@sceneInfo.showAreaInfo ', name, self.lastName)
            mapdId = formula.getMapId(p.spaceNo)
            mapData = MCD.data.get(mapdId)
            try:
                unDoneArea = SCD.data.get('unDoneChunk', ())
                if name in unDoneArea and self.lastName not in unDoneArea:
                    gameglobal.rds.ui.showUndoneMark(True)
                    if gameglobal.F12_MODE == gameglobal.F12_MODE_NOUI:
                        p.showUI(True)
                elif name not in unDoneArea and self.lastName in unDoneArea:
                    gameglobal.rds.ui.showUndoneMark(False)
                fortId = CMD.data.get(name, {}).get('fortId', 0)
                noAreaName = mapData.get('noAreaName', 0)
                showName = CMD.data.get(name, {}).get('showName', '')
                if CMD.data.get(name, {}).get('showNameByMapId', 0):
                    showName = '%s_%d' % (showName, mapdId)
                if not noAreaName and showName and showName != self.lastShowName:
                    if p.clanWarStatus:
                        if fortId:
                            gameglobal.rds.ui.showMapName(showName, '领地之战进行中', 'red')
                        else:
                            gameglobal.rds.ui.showMapName(showName)
                    elif fortId:
                        fortName = p.clanWar.fort[fortId].ownerGuildName
                        gameglobal.rds.ui.showMapName(showName, fortName, 'yellow')
                    else:
                        gameglobal.rds.ui.showMapName(showName)
                self.lastShowName = showName
            except:
                gamelog.error('cd@sceneInfo.showAreaInfo')

            rs = True
            gameglobal.rds.tutorial.onChunkNameTrigger(name)
            if mapData and mapData.has_key('noPkPunish'):
                p.showGameMsg(GMDD.data.NO_PK_PUNISHI_IN_MAP, ())
            p.cell.updateChunk(name)
            self.modifySkyBox(name)
            self.lastName = name
            self.lastSpaceNo = p.spaceNo
        elif name != BigWorld.player().chunk:
            BigWorld.player().cell.updateChunk(name)
        else:
            fortId = CMD.data.get(name, {}).get('fortId')
            if fortId:
                phaseSpaceNo = CWFD.data.get(fortId, {}).get('phaseSpaceNo')
                if phaseSpaceNo and formula.spaceInClanWarPhase(phaseSpaceNo) and BigWorld.player().spaceNo != phaseSpaceNo:
                    BigWorld.player().cell.updateChunk(name)
        self._updatePkDisplay()
        p = BigWorld.player()
        if resideInSafetyZone(p):
            if not self.inSafetyZone:
                p.showGameMsg(GMDD.data.PK_ENTER_SAFETY_ZONE, ())
            self.inSafetyZone = True
        else:
            if self.inSafetyZone:
                p.showGameMsg(GMDD.data.PK_LEAVE_SAFETY_ZONE, ())
            self.inSafetyZone = False
        if resideInBorderZone(p):
            if not self.inBorderZone:
                p.showGameMsg(GMDD.data.ENTER_BORDER_ZONE, ())
            self.inBorderZone = True
        else:
            if self.inBorderZone:
                p.showGameMsg(GMDD.data.LEAVE_BORDER_ZONE, ())
            self.inBorderZone = False
        gAreaEventObj.startAreaEvent(p.mapID, p.position)
        self.nepUpdateMap()
        gameglobal.rds.ui.killFallenRedGuardRank.checkTrunk(name)
        return rs

    def nepUpdateMap(self):
        try:
            enableNepSync = gameglobal.rds.configData.get('enableNepSync', False)
            if not enableNepSync:
                return
            p = BigWorld.player()
            mapType = protect.NEMAP_UNKOWN
            if p.inFuben():
                mapType = protect.NEMAP_FB
            mapId = formula.getMapId(p.spaceNo)
            chunkName = BigWorld.ChunkInfoAt(p.position)
            firstKey = CMD.data.get(chunkName, {}).get('mapAreaId', 0)
            nepMapId = (mapId << 16) + firstKey
            if nepMapId != self.lastNepMapId:
                protect.nepActionUpdateMap(mapType, nepMapId)
                self.lastNepMapId = nepMapId
        except:
            pass

    def getAreaInfo(self):
        p = BigWorld.player()
        st = ''
        if p:
            st = BigWorld.ChunkInfoAt((p.position.x, p.position.y + 1, p.position.z))
        return st

    def _updatePkDisplay(self):
        p = BigWorld.player()
        if not p.targetLocked or not p.targetLocked.IsAvatar:
            return
        en = p.targetLocked
        if not en.topLogo:
            return
        en.topLogo.updateRoleName(en.topLogo.name)

    def modifySkyBox(self, chunkName = None):
        if not chunkName:
            chunkName = self.getAreaInfo()
        if self.lastSkyboxInfo:
            skyboxName, baseWeight, targetWeight = self.lastSkyboxInfo
            BigWorld.setZonePriority(skyboxName, baseWeight)
        if CMD.data.get(chunkName, {}).get('dynamicSkybox', False):
            skyboxInfo = self.getSkyboxByAreaState(chunkName)
        else:
            skyboxInfo = CMD.data.get(chunkName, {}).get('skyboxInfo')
        if skyboxInfo:
            skyboxName, baseWeight, targetWeight = skyboxInfo
            BigWorld.setZonePriority(skyboxName, targetWeight)
        self.lastSkyboxInfo = skyboxInfo

    def getSkyboxByAreaState(self, chunkName):
        skyboxInfo = {}
        p = BigWorld.player()
        if chunkName in WWCD.data.get('dynamicSkyboxAreas', ()):
            openedStage = getattr(p, 'wingWorldOpenedStage', 0)
            skyboxInfo = WWCD.data.get('dynamicSkyboxInfos', {}).get(openedStage)
        return skyboxInfo


LEAVE_WORLD_DIST = 1500
MODEL_NONE = 0
MODEL_LOADING = 1
MODEL_LOADED = 2

class AreaEvent(object):
    __metaclass__ = Singleton

    def __init__(self):
        super(AreaEvent, self).__init__()
        self.areaDict = {}
        self.genAreaEvent()

    def genAreaEvent(self):
        for key, item in AVD.data.items():
            spaceNo = item.get('spaceNo', '')
            if not self.areaDict.has_key(spaceNo):
                self.areaDict[spaceNo] = {}
            item['start'] = MODEL_NONE
            item['modelInWorld'] = None
            self.areaDict[spaceNo][key] = item

    def release(self):
        self.deleteAreaEvent(0)

    @checkInterval(5)
    def startAreaEvent(self, spaceNo, pos):
        if not self.areaDict.has_key(spaceNo):
            return
        for key in self.areaDict[spaceNo]:
            self._start(key, self.areaDict[spaceNo][key], pos)

    def deleteAreaEvent(self, excludeSpaceNo):
        p = BigWorld.player()
        excludeSpaceNo = formula.getMapId(excludeSpaceNo)
        for num in self.areaDict:
            if num != excludeSpaceNo:
                data = self.areaDict.get(num, {})
                for key in data:
                    data[key]['start'] = MODEL_NONE
                    model = data[key]['modelInWorld']
                    if model and model.inWorld:
                        model.soundCallback(None)
                        p.delModel(model)
                        data[key]['modelInWorld'] = None

    def _start(self, index, item, pos):
        bornPos = Math.Vector3(item['position'])
        dist = (bornPos - pos).length
        if item['start'] == MODEL_LOADED:
            if dist >= LEAVE_WORLD_DIST:
                model = item['modelInWorld']
                if model and model.inWorld:
                    model.soundCallback(None)
                    p = BigWorld.player()
                    p.delModel(model) if p else None
                    item['modelInWorld'] = None
                    item['start'] = MODEL_NONE
            return
        if item['start'] != MODEL_NONE or dist > item['dist']:
            return
        gamelog.debug('sceneInfo@_start')
        modelID = item['model']
        modelPath = gameglobal.charRes + '%d/%d.model' % (modelID, modelID)
        threadID = gameglobal.getLoadThread()
        item['start'] = MODEL_LOADING
        clientUtils.fetchModel(threadID, Functor(self._afterModelFinished, index, item), modelPath)

    def _afterModelFinished(self, index, item, model):
        delay = item.get('delay', 0)
        gamelog.debug('_afterModelFinished', index, item, model)
        BigWorld.callback(delay, Functor(self._processModelFinished, item, model))

    def _processModelFinished(self, item, model):
        p = BigWorld.player()
        gamelog.debug('sceneInfo@_processModelFinished', item['spaceNo'], p.spaceNo)
        if item['spaceNo'] != formula.getMapId(p.spaceNo):
            model = None
            item['start'] = MODEL_NONE
            return
        if not model:
            return
        item['start'] = MODEL_LOADED
        scale = item.get('scale', 1)
        pos = item.get('position', (0, 0, 0))
        yaw = item.get('yaw', 0)
        act = str(item.get('idleAct', 0))
        model.effectId = item.get('effectId', None)
        if getattr(model, 'effectId', None):
            model.soundCallback(self.actionCueCallback)
        p.addModel(model)
        model.position = pos
        model.expandVisibilityBox(1000)
        if scale != 1:
            model.scale = (scale, scale, scale)
        model.yaw = yaw
        item['modelInWorld'] = model
        if act in model.actionNameList():
            model.action(act)()

    def actionCueCallback(self, cueId, data, actionName):
        if cueId == 1:
            self._playSound(data)
        elif cueId == 2:
            if data.startswith('s'):
                params = data[1:].split(':')
                effects = params[0][1:-1].split(',')
                delayTime = 0.0
                if len(params) > 1:
                    delayTime = float(params[1])
                for e in effects:
                    tt = e.split('.xml-')
                    if len(tt) == 2:
                        effect = tt[0].split('/')
                        if effect[len(effect) - 1].isdigit():
                            effectId = int(effect[len(effect) - 1])
                            model = self.findModelByEffectId(effectId)
                            if model:
                                BigWorld.callback(delayTime, Functor(sfx.attachEffect, gameglobal.ATTACH_EFFECT_NORMAL, (1,
                                 gameglobal.EFF_DEFAULT_PRIORITY,
                                 model,
                                 effectId,
                                 sfx.EFFECT_UNLIMIT,
                                 float(tt[1]) / gameglobal.ACTION_FRAME)))

    def findModelByEffectId(self, effectId):
        for num in self.areaDict:
            data = self.areaDict.get(num, {})
            for key in data:
                model = data[key]['modelInWorld']
                if model and model.inWorld:
                    if getattr(model, 'effectId', None) == effectId:
                        return model

    def findModel(self):
        for num in self.areaDict:
            data = self.areaDict.get(num, {})
            for key in data:
                model = data[key]['modelInWorld']
                if model and model.inWorld:
                    return model

    def _playSound(self, data):
        model = self.findModel()
        params = data.split(':')
        soundPath = str(params[0])
        if model.node('biped'):
            gameglobal.rds.sound.playFx(soundPath, model.node('biped').position, False)


gAreaInfoObj = AreaInfo.getInstance()
gAreaEventObj = AreaEvent.getInstance()
