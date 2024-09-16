#Embedded file name: /WORKSPACE/data/entities/client/helpers/loadingprogress.o
import time
import random
import zlib
import cPickle
import BigWorld
import Sound
import game
import appSetting
import gameglobal
import gametypes
import formula
import gamelog
import clientcom
import utils
import const
from guis import uiUtils
from helpers import ccControl
from helpers import seqTask
from sfx import keyboardEffect
from gameclass import Singleton
from data import loading_tips_data as LTD
from data import loading_item_data as LID
from data import loading_map_data as LMD
from data import map_config_data as MCD
from data import chunk_tip_data as CTD
from data import sys_config_data as SCD
from data import chunk_mapping_data as CMD
gLastSpace = ''
gOptimizeLoading = True
gDisableVisualStreaming = 0.5

def instance():
    return LoadingProgress.getInstance()


class LoadingProgress(object):
    __metaclass__ = Singleton
    LOADING_PIC = {'ycdg': 'world',
     'jjc_pt': 'jingjichang',
     'fb_jdc': 'jingjichang',
     'fb_ssc_01': 'shengsichang',
     'fb_bg_01': 'sidi',
     'fb_bg_02': 'sidi',
     'zc_ycj': 'zhanchang',
     '00_xsc': 'xinshou',
     'dg_xsc_02': 'xinshou',
     'dg_xsc_03': 'xinshou',
     'dg_xsc_04': 'xinshou',
     'fb_xscdx': 'xinshou',
     'dishicheng': 'dishi',
     'yanhuijun': 'dishi',
     'shiluohai': 'dishi',
     'yanhuixia': 'dishi',
     'huashulin': 'dishi',
     'yanhuishilin': 'dishi',
     'yanchuiyaosai': 'dishi',
     'mimiyingdi': 'dishi',
     'chidifengyin': 'dishi',
     'buguihuangmo': 'dishi',
     'shiluocun': 'dishi',
     'liushazhidi': 'dishi',
     'chiyantianqian': 'dishi',
     'yinglingjun': 'didu',
     'didu': 'didu',
     'fb_mmyd': 'changcheng',
     'fb_mmyd_01': 'changcheng',
     'fb_hhcc': 'chenchuan',
     'dg_hhcc_01': 'chenchuan',
     'dg_hhcc_03': 'chenchuan',
     'fb_jxmc_01': 'micheng',
     'dg_jxmc_01': 'micheng',
     'fb_hqsc': 'shenci',
     'dg_thhj_01': 'tianhuang',
     'dg_thhj_02': 'tianhuang',
     'dg_thhj_03': 'tianhuang',
     'dg_thhj_04': 'tianhuang',
     'dg_thhj_05': 'tianhuang',
     'fb_wg': 'wugu',
     'fb_wg_01': 'wugu',
     'fb_wg_02': 'wugu',
     'fb_zy_01': 'zhenyao',
     'fb_lx': 'lingxu',
     'fb_dsyw': 'zc_ycdb',
     'fb_jxtw_01': 'micheng',
     'zc_wjzd': 'wujiezhidi',
     'fb_ly_01': 'Longyuan',
     'fushengjuchang': 'fushengjuchang',
     'dgbj': 'diguobianjing',
     'dgbj_02': 'diguobianjing',
     'fb_ycwdh_01': 'wudaohui',
     'fb_ycwdh_02': 'wudaohui',
     'jddt01': 'jiayuan',
     'jddt02': 'jiayuan',
     'fwhx232_01': 'jiayuan',
     'fwhx425_01': 'jiayuan',
     'fwhx697_01': 'jiayuan',
     'fwhx_hj_01': 'jiayuan',
     'fb_12gong_01': 'shiergong'}
    LOAD_DISTANCE = 200

    def __init__(self):
        global Obj
        self.loadingTime = 0
        self.startLoading = 0
        self.visible = False
        self.callback = None
        self.lastPercent = 0.0
        self.roleName = ''
        self.checkCallBack = None
        self.inLoading = False
        self.fServerLoaded = False
        self.enableGuildloadCheck = False
        self.clearLoadingData()
        Obj = self

    def reset(self):
        pass

    def fadeTo(self, mapName = None, mapId = 0):
        if gameglobal.rds.ui.arenaWait.isShow:
            return
        if not self.visible:
            return
        picPath, dynamicPath, _ = self.getRandomPicPath(mapName, mapId)
        gameglobal.rds.ui.loading.fadeTo(picPath, dynamicPath, 1.2)

    def fadeTo2(self, spaceNo):
        p = BigWorld.player()
        if not self.visible:
            return
        mapId = formula.getMapId(spaceNo)
        if mapId in SCD.data.get('JUQING_MAP_LIST', []):
            mapName = 'fushengjuchang'
        else:
            mapName = formula.whatSpaceMap(spaceNo)
            if mapName:
                mapName = mapName.split('/')[2].strip()
            if mapId == const.SPACE_NO_BIG_WORLD:
                mapName = uiUtils.getChunkName(p.position[0], p.position[2])
        gamelog.debug('@zmk loadingProgress - fadeto2: %s' % mapName)
        self.fadeTo(mapName, mapId)

    def __fading(self, shad):
        shad.speed = 1
        shad.alpha = 1

    def clearLoadingData(self):
        self.specialLoadingNum = 0
        self.specialLoadingTimestamp = 0
        self.loadingPicMap = {}

    def checkLoadingIdValid(self, loadingId):
        p = BigWorld.player()
        lidData = LID.data.get(loadingId, {})
        startTime = lidData.get('startTime', '')
        endTime = lidData.get('endTime', '')
        if startTime != '' and endTime != '':
            if not utils.inCrontabRange(startTime, endTime):
                return False
        level = lidData.get('level', ())
        if level and p and hasattr(p, 'lv'):
            if p.lv < level[0]:
                return False
            if p.lv > level[1]:
                return False
        return True

    def getRandomPicPath(self, mapName, mapId = 0):
        resultLoadingId = 0
        if gameglobal.rds.configData.get('enableRandomLoadingPic', False):
            if self.specialLoadingNum < SCD.data.get('specialLoadingPicNum', 0):
                specialLoadingList = SCD.data.get('specialLoadingList', ())
                validList = [ loadingId for loadingId in specialLoadingList if self.checkLoadingIdValid(loadingId) ]
                validLen = len(validList)
                if validLen > 0:
                    resultLoadingId = validList[(self.specialLoadingNum - 1) % validLen]
            if resultLoadingId == 0 and mapId:
                loadingPicList = MCD.data.get(mapId, {}).get('loadingPicList', ())
                if loadingPicList:
                    validLoadingIdList = [ loadingId for loadingId in loadingPicList if self.checkLoadingIdValid(loadingId) ]
                    if len(validLoadingIdList) > 0:
                        resultLoadingId = random.choice(validLoadingIdList)
            if resultLoadingId == 0:
                lmdData = LMD.data.get(mapName, {})
                randomLoadingList = lmdData.get('randomLoadingList', ())
                validList = [ loadingId for loadingId in randomLoadingList if self.checkLoadingIdValid(loadingId) ]
                if len(validList) > 0:
                    timestamp = self.loadingPicMap.get(mapName, {}).get('timestamp', 0)
                    now = utils.getNow()
                    if now > timestamp + 45:
                        resultLoadingId = random.choice(validList)
                        self.loadingPicMap[mapName] = {'loadingId': resultLoadingId,
                         'timestamp': now}
                    else:
                        resultLoadingId = self.loadingPicMap.get(mapName, {}).get('loadingId', 0)
        return self.getPicPathByLoadingId(resultLoadingId, mapName)

    def getPicPathByLoadingId(self, loadingId, mapName):
        lidData = LID.data.get(loadingId, {})
        lmdData = LMD.data.get(mapName, {})
        picName = lidData.get('loadingPic', '')
        needHideTips = lidData.get('hideTips', 0) > 0
        useDynamic = lmdData.get('useDynamic', 0) > 0
        if picName == '':
            picName = self.LOADING_PIC.get(mapName, 'world')
        picPath = 'loading/%s.dds' % picName
        dynamicPath = 'loading/dynamic/%s.swf' % picName if useDynamic else ''
        return (picPath, dynamicPath, needHideTips)

    def getRandomTips(self, mapName):
        p = BigWorld.player()
        if p.inFuben():
            spaceKey = formula.getFubenNo(p.spaceNo)
        elif p.inMLSpace():
            spaceKey = formula.getMLGNo(p.spaceNo)
        else:
            spaceKey = mapName
        tipsIds = CTD.data.get(str(spaceKey), {}).get('tipsIds', [])
        if not tipsIds:
            tipsIds = []
            for key in LTD.data.keys():
                if LTD.data[key].get('ignore', 0) != 1:
                    tipsIds.append(key)

        keyList = []
        if p and hasattr(p, 'lv'):
            for key in tipsIds:
                level = LTD.data.get(key, {}).get('level', (-1, 999))
                if level[0] <= p.lv <= level[1]:
                    keyList.append(key)

        else:
            keyList = tipsIds
        return random.choice(keyList)

    def getLoadingPicAndTips(self, mapName = None):
        now = utils.getNow()
        if now > self.specialLoadingTimestamp + 45:
            self.specialLoadingNum += 1
            self.specialLoadingTimestamp = now
        picPath, dynamicPath, needHideTips = self.getRandomPicPath(mapName)
        if needHideTips:
            tips = ''
        else:
            try:
                randKey = self.getRandomTips(mapName)
            except:
                randKey = 1

            tips = LTD.data.get(randKey, {}).get('tips', '')
        return (picPath, dynamicPath, tips)

    def preLoad(self):
        gameglobal.rds.ui.loading.setMode('pre')
        picPath, _, tips = self.getLoadingPicAndTips('ycdg')
        gameglobal.rds.ui.loading.setText(tips)
        gameglobal.rds.ui.loading.setFirstPic(picPath)
        gameglobal.rds.ui.loading.show(True)

    def _showLoadingUI(self, vis, mapName):
        if vis:
            clientcom.resetLimitFps(True)
            BigWorld.loadingWorld(True)
            gameglobal.rds.ui.loading.setMode('normal')
            picPath, _, tips = self.getLoadingPicAndTips(mapName)
            gameglobal.rds.ui.loading.setText(tips)
            gameglobal.rds.ui.loading.setFirstPic(picPath)
            gameglobal.rds.ui.loading.show(True)
            gameglobal.rds.ui.loading.play()
            ccControl.setCCVisible(False)
            keyboardEffect.addKeyboardEffect('effect_loading')
        else:
            gameglobal.rds.ui.loading.show(False)
            clientcom.resetLimitFps(False)
            BigWorld.loadingWorld(False)
            ccControl.setCCVisible(True)
            keyboardEffect.removeKeyboardEffect('effect_loading')
        gameglobal.rds.cam.reset()

    def show(self, vis, mapName = None, logonLoading = False):
        gamelog.debug('jorsef: show loading:', self.visible, vis, mapName)
        p = BigWorld.player()
        if self.visible == vis:
            if logonLoading:
                if not gameglobal.rds.ui.arenaWait.isShow:
                    self._showLoadingUI(vis, mapName)
                if gameglobal.rds.ui.fubenLogin.isShow:
                    gameglobal.rds.ui.fubenLogin.dismiss()
            return
        if vis:
            if gameglobal.rds.ui.map.mc:
                gameglobal.rds.ui.map.openMap(False)
            Sound.enableCategory(gametypes.CATEGORY_CHAR, False)
            Sound.enableCategory(gametypes.CATEGORY_CREATURE, False)
            self.oldState = gameglobal.rds.GameState
            gameglobal.rds.GameState = gametypes.GS_LOADING
            if p:
                p.losePhysics()
                p.loseGravity()
                if hasattr(p, 'leaveScreenMoiveMode'):
                    p.leaveScreenMoiveMode()
            self._forceShowNormal()
        else:
            gameglobal.rds.GameState = self.oldState
            if p:
                p.restorePhysics()
                p.restoreGravity()
            if appSetting.SoundSettingObj.getEnableByCategory(gametypes.CATEGORY_CHAR):
                Sound.enableCategory(gametypes.CATEGORY_CHAR, True)
            if appSetting.SoundSettingObj.getEnableByCategory(gametypes.CATEGORY_CREATURE):
                Sound.enableCategory(gametypes.CATEGORY_CREATURE, True)
            if p and p.__class__.__name__ != 'PlayerAccount':
                fbNo = formula.getFubenNo(p.spaceNo)
                p.cell.enterFubenLoadingProgressDone(fbNo)
            gamelog.debug('use time:Loading time: ', BigWorld.time() - self.startLoading)
        if not gameglobal.rds.ui.arenaWait.isShow:
            self._showLoadingUI(vis, mapName)
        self.visible = vis
        if gameglobal.rds.ui.fubenLogin.isShow:
            gameglobal.rds.ui.fubenLogin.dismiss()

    def onServerLoaded(self, fLoaded = True):
        self.fServerLoaded = fLoaded

    def startProgress(self, callback = None):
        gamelog.debug('@zmk LoadingProgress call startProgress')
        game.sendLoadingProcessInfo()
        p = BigWorld.player()
        if p and self.visible:
            p.losePhysics()
            p.loseGravity()
            if hasattr(p, 'leaveScreenMoiveMode'):
                p.leaveScreenMoiveMode()
            if hasattr(p, 'ap'):
                p.ap.restore()
                p.ap.inLoadingProgress = True
        self.loadingTime = max(BigWorld.time(), 0)
        self.startLoading = BigWorld.time()
        self.callback = callback
        self.lastPercent = 0
        self.inLoading = True
        Sound.enableFx(False)
        if hasattr(BigWorld, 'enableVisualStreaming'):
            BigWorld.enableVisualStreaming(False)
        if getattr(self, 'checkCallBack', 0):
            BigWorld.cancelCallback(self.checkCallBack)
        self.checkCallBack = BigWorld.callback(0.1, self._checkProgress)
        hasattr(p, 'startProgressLoading') and p.startProgressLoading()
        if formula.spaceInGuild(BigWorld.player().spaceNo):
            BigWorld.callback(10, self.beginGuildLoadCheck)

    def _checkProgress(self):
        global gOptimizeLoading
        dist = BigWorld.spaceMaxLoadPath() / 1.414
        if dist < LoadingProgress.LOAD_DISTANCE:
            dist = LoadingProgress.LOAD_DISTANCE
        if gOptimizeLoading:
            if dist > 350:
                dist = 350
        p = BigWorld.spaceLoadStatus(dist)
        usedTime = BigWorld.time() - self.loadingTime
        gamelog.debug('jorsef: loading percent ', p, dist, self.lastPercent, usedTime, BigWorld.time())
        if usedTime <= 0:
            usedTime = 0.5
            self.loadingTime = BigWorld.time()
        if p < 1.0 and (p <= self.lastPercent or usedTime < 0.5):
            self.checkCallBack = BigWorld.callback(0.2, self._checkProgress)
            return
        player = BigWorld.player()
        if player and gOptimizeLoading and player.inFuben() and p > 0.8 and not self.fServerLoaded:
            if p > self.lastPercent:
                p = max(self.lastPercent, 0.01 * p + 0.99 * self.lastPercent)
            if usedTime > 15:
                gamelog.debug('@PGF:loadingProgress, fServerLoaded', usedTime, self.fServerLoaded)
                self.fServerLoaded = True
        p = max(p, self.lastPercent)
        if self.lastPercent < gDisableVisualStreaming <= p:
            if hasattr(BigWorld, 'enableVisualStreaming'):
                BigWorld.enableVisualStreaming(True)
        self.lastPercent = p
        fakePercent = 100 * p
        forceLoad = False
        isModelsLoaded = False
        if hasattr(player, 'spaceNo'):
            if not formula.spaceInGuild(player.spaceNo) and not player.spaceInHomeOrLargeRoom():
                isModelsLoaded = True
            elif formula.spaceInGuild(player.spaceNo):
                isModelsLoaded = self.checkGuildModelsLoaded()
                fakePercent = 90 * p
            elif player.spaceInHomeOrLargeRoom():
                fakePercent = self.calcFurnitureLoadedPercent()
                isModelsLoaded = True if fakePercent >= 1.0 else False
                fakePercent = 90 * fakePercent
                if p >= 1.0:
                    forceLoad = True
            if formula.inDotaBattleField(player.mapID) and getattr(player, 'isInBfDotaChooseHero', False) and fakePercent >= 90:
                if not player.isChooseHeroLoadedCompletd:
                    fakePercent = 90 * p
        if seqTask.gTaskMgr:
            seqTask.gTaskMgr.setForceLoad(forceLoad)
        gameglobal.rds.ui.arenaWait.setProgress(fakePercent)
        gameglobal.rds.ui.loading.setProgress(fakePercent)
        if p >= 1.0 and usedTime > 0.5 and isModelsLoaded:
            gameglobal.rds.ui.loading.setProgress(100)
            self.lastPercent = 0
            if player:
                player._checkVehicle()
            BigWorld.callback(2, self.onProgressEnd)
            player.pendingGuildEntIds = []
            player.pendingGuildMarkerIds = []
            return
        self.checkCallBack = BigWorld.callback(0.3, self._checkProgress)

    def beginGuildLoadCheck(self):
        self.enableGuildloadCheck = True

    def checkGuildModelsLoaded(self):
        if not self.enableGuildloadCheck:
            return False
        if formula.spaceInGuild(BigWorld.player().lastSpaceNo):
            return True
        t = BigWorld.time() - self.loadingTime
        if t < 15:
            return False
        pendingGuildEntIds = getattr(BigWorld.player(), 'pendingGuildEntIds', None)
        pendingGuildMarkerIds = getattr(BigWorld.player(), 'pendingGuildMarkerIds', None)
        if not pendingGuildEntIds and not pendingGuildMarkerIds:
            return True
        if t > 50:
            return True
        for eid in pendingGuildEntIds:
            ent = BigWorld.entities.get(eid, None)
            if not ent:
                return False
            if not hasattr(ent, 'isAllModelsLoaded'):
                continue
            if not ent.isAllModelsLoaded():
                return False

        return True

    def calcFurnitureLoadedPercent(self):
        p = BigWorld.player()
        if not p.spaceInHomeOrLargeRoom():
            return 1.0
        t = BigWorld.time() - self.loadingTime
        if t < 5:
            return 0.0
        ents = BigWorld.entities.values()
        totalFurnitureNum = 0
        loadedFurnitureNum = 0
        for en in ents:
            if utils.instanceof(en, 'HomeFurniture'):
                if (en.position - p.position).length <= 80:
                    totalFurnitureNum += 1
                    if getattr(en, 'firstFetchFinished', False):
                        loadedFurnitureNum += 1

        percent = loadedFurnitureNum * 1.0 / totalFurnitureNum if totalFurnitureNum else 0.0
        if totalFurnitureNum < 10 or loadedFurnitureNum * 1.0 / totalFurnitureNum > 0.8:
            return 1.0
        if t >= 30 and self.lastPercent >= 1.0:
            return 1.0
        return percent

    def onProgressEnd(self):
        if hasattr(BigWorld, 'enableVisualStreaming'):
            BigWorld.enableVisualStreaming(True)
        if self.checkCallBack:
            BigWorld.cancelCallback(self.checkCallBack)
        self.show(False)
        self.lastPercent = 0
        self.fServerLoaded = False
        clientcom.resetLimitFps(False)
        BigWorld.loadingWorld(False)
        gamelog.debug('chaos: loading completed.')
        p = BigWorld.player()
        if p:
            if formula.inPhaseSpace(p.spaceNo):
                mapId = formula.getMapId(p.spaceNo)
                if MCD.data.get(mapId, {}).has_key('setSkyZonePriority'):
                    zoneName, basepri, tgtpri = MCD.data[mapId]['setSkyZonePriority']
                    BigWorld.setZonePriority(zoneName, tgtpri)
            p.faceToDirWidthCamera(p.yaw)
        if self.callback != None:
            self.callback()
            self.callback = None
        hasattr(p, 'endProgressLoading') and p.endProgressLoading()
        hasattr(p, 'sendFeiHuoInfo') and p.sendFeiHuoInfo()
        getattr(p, 'notifyWingWorldStep', 0) and p.onWingWorldStepChange(p.notifyWingWorldStep)
        self.logLoadSpaceTime()

    def logLoadSpaceTime(self):
        prop = gameglobal.rds.configData.get('propOfLogLoadSpaceTime', 0)
        if random.random() <= prop:
            p = BigWorld.player()
            loadTime = BigWorld.time() - self.startLoading
            chunkName = BigWorld.ChunkInfoAt(p.position)
            areaId = CMD.data.get(chunkName, {}).get('mapAreaId', 0)
            data = {'loadTime': loadTime,
             'chunkName': chunkName,
             'spaceNo': p.spaceNo,
             'areaId': areaId,
             'position': str(p.position),
             'gbId': p.gbId,
             'mapId': p.mapID,
             'lastSpaceNo': p.lastSpaceNo}
            data = zlib.compress(cPickle.dumps(data, -1))
            p.base.logLoadSpaceTime(data)

    def _forceShowNormal(self):
        p = BigWorld.player()
        if p != None and hasattr(p, 'ap') and p.ap != None:
            if p.ap.__class__.__name__ == 'KeyboardPhysics':
                p.ap.forceAllKeysUp()
            p.ap.ccamera.canRotate = False
            p.ap.dcursor.canRotate = False
            p.ap.stopMove()


instance()
