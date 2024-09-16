#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client/game.o
from gamestrings import gameStrings
import copy
import sys
import os
import subprocess
import stat
import cPickle
import zlib
import md5
import random
import asyncore
import traceback
import hashlib
import Crypto.Hash
import Crypto.Cipher
try:
    Crypto.Hash.MD2 = sys.modules['Crypto.Hash._MD2']
    Crypto.Hash.RIPEMD160 = sys.modules['Crypto.Hash._RIPEMD160']
    Crypto.Hash.MD4 = sys.modules['Crypto.Hash._MD4']
    Crypto.Hash.SHA256 = sys.modules['Crypto.Hash._SHA256']
    Crypto.Cipher.XOR = sys.modules['Crypto.Cipher._XOR']
    Crypto.Cipher.ARC4 = sys.modules['Crypto.Cipher._ARC4']
    Crypto.Cipher.CAST = sys.modules['Crypto.Cipher._CAST']
    Crypto.Cipher.AES = sys.modules['Crypto.Cipher._AES']
    Crypto.Cipher.DES = sys.modules['Crypto.Cipher._DES']
    Crypto.Cipher.ARC2 = sys.modules['Crypto.Cipher._ARC2']
    Crypto.Cipher.DES3 = sys.modules['Crypto.Cipher._DES3']
    Crypto.Cipher.Blowfish = sys.modules['Crypto.Cipher._Blowfish']
except:
    Crypto.Hash.MD2 = sys.modules['Crypto.Hash.MD2']
    Crypto.Hash.RIPEMD160 = sys.modules['Crypto.Hash.RIPEMD160']
    Crypto.Hash.MD4 = sys.modules['Crypto.Hash.MD4']
    Crypto.Hash.SHA256 = sys.modules['Crypto.Hash.SHA256']
    Crypto.Cipher.XOR = sys.modules['Crypto.Cipher.XOR']
    Crypto.Cipher.ARC4 = sys.modules['Crypto.Cipher.ARC4']
    Crypto.Cipher.CAST = sys.modules['Crypto.Cipher.CAST']
    Crypto.Cipher.AES = sys.modules['Crypto.Cipher.AES']
    Crypto.Cipher.DES = sys.modules['Crypto.Cipher.DES']
    Crypto.Cipher.ARC2 = sys.modules['Crypto.Cipher.ARC2']
    Crypto.Cipher.DES3 = sys.modules['Crypto.Cipher.DES3']
    Crypto.Cipher.Blowfish = sys.modules['Crypto.Cipher.Blowfish']

import Crypto.Util
Crypto.Util.strxor = sys.modules['strxor']
Crypto.Util._counter = sys.modules['_counter']
import utils
import re
import uuid
import subprocess
import hashlib
import datetime
import GUI
import BigWorld
import C_ui
import Sound
import Math
import ResMgr
try:
    import MemoryDB
except:
    pass

import appSetting
from appSetting import Obj as AppSettings
import soundManager
import cacheBDB
import cacheMDB
import gameglobal
import gameconfigCommon
import gametypes
import const
import keys
import clientcom
import gamelog
import Hijack
import formula
import clientUtils
import netWork
import MDBUtils
from helpers import protect
from helpers import navigator
from helpers import camera
from helpers import updateAmbientMusic
from helpers import pyBgTask
from helpers import stateSafe
from helpers import avatarMorpher
from helpers import loadingProgress
from helpers import capturePhoto
from helpers import scenario
from helpers import cameraControl as CC
from helpers import cgPlayer
from helpers import mdbDataConverter
from helpers.eventDispatcher import Event
from helpers import editorHelper
from helpers import gameAntiCheatingManager
from clientInfo import ClientInfo
from sfx import screenEffect
from sfx import sfx
from sfx import keyboardEffect
from helpers import PNGEncode
from callbackHelper import Functor
from guis import uiAdapter
from guis import ui
from guis import uiUtils
from guis import uiConst
from guis import tutorial
from guis import login
from guis import hotkey as HK
from guis import characterDetailAdjustProxy
from guis import ime
from guis import events
from guis import chickenFoodFactory
from guis import groupDetailFactory
from data import ability_data
from data import puzzle_data
from data import ws_daoheng_data
from data import fb_entity_data
import miniclient
renderFeatures = {}
logOnAttemptKey = hex(random.getrandbits(64))[2:-1]
gameglobal.rds.logOnAttemptKey = logOnAttemptKey
cgMovie = None
COLORGRADING_TEXTURE = 'env/colormap/dljm_n/dljm_n_cch.tga'
GMAE_IS_PRELOAD = False
GMAE_IS_START = False

def reloadClass(cls):
    if cls.__module__ == '__builtin__':
        return
    else:
        mod = sys.modules.get(cls.__module__, None)
        if not mod:
            gamelog.error('reload failed: can not find <%s> in sys.modules' % cls.__module__)
            return
        gamelog.info('reload module: %s' % cls.__module__)
        return reloadex(mod)


def gamereload(inst, reloadMRO = False):
    if not inst:
        gamelog.error('reload failed: NoneType')
        return
    else:
        cls = getattr(inst, '__class__', None)
        if not cls:
            gamelog.error('reload failed: invalid instance')
            return
        newMod = reloadClass(cls)
        if not newMod:
            return
        if reloadMRO:
            loaded = [cls.__module__]
            for base in cls.__mro__:
                if base.__module__ in loaded:
                    continue
                loaded.append(base.__module__)
                reloadClass(base)

        return newMod


def dataCacheInitErrorCB():
    path = mdbDataConverter.getBinaryCachePath()
    try:
        os.remove(path)
    except:
        pass


def valideMDBModules(MDBModules):
    modules = []
    for module in MDBModules:
        if not hasattr(module, 'keyType'):
            continue
        if module.keyType not in (cacheMDB.KEY_TYPE_INT, cacheMDB.KEY_TYPE_TUPLE_INT):
            continue
        if not hasattr(module, 'valueAttrs'):
            continue
        modules.append(module)

    return modules


def initMemoryDBCache():
    from utils import newMDB
    if newMDB:
        from helpers import newMDBConverter
        newMDBConverter.MDBConverter.writeMDBEnd()
        MDBUtils.initNewMDB(disableConvert=True)
        return
    else:
        return


tickCallback = None

def init(scriptsConfig):
    gamelog.info('=================game init begin=================')
    formula.initFBTypes()
    gameglobal.rds.enablePlanb = clientcom.enablePlanb()
    gameglobal.rds.isFeiHuo = AppSettings.get(keys.SET_FEIHUO_SUFFIX, '')
    gameglobal.rds.isYiYou = AppSettings.get(keys.SET_YIYOU_SUFFIX, '')
    gameglobal.rds.isShunWang = AppSettings.get(keys.SET_SHUNWANG_SUFFIX, '')
    gameglobal.rds.loginAuthType = const.LOGIN_AUTH_RU_GC if scriptsConfig.readBool('login/MRGCLogin', False) else scriptsConfig.readString('login/authType', '')
    gameglobal.rds.loginType = gameglobal.GAME_LOGIN_TYPE_DEFAULT
    gameglobal.rds.enableNewLoginScene = clientcom.enableNewLoginScene()
    gameglobal.rds.enableBinkLogoCG = clientcom.enableBinkLogoCG()
    gameglobal.rds.useCEFLogin = clientcom.useCEFLogin()
    gameglobal.rds.loginIndex = 3
    uiConst.YIYOU_WEB_URL = uiConst.NEW_YIYOU_WEB_URL
    gameglobal.rds.clientSpace = None
    gameglobal.rds.clientSpaceMapping = None
    uiConst.WIDGET_LOGIN_WIN = uiConst.WIDGET_LOGIN_WIN2
    uiConst.WIDGET_LOGINLOGO = uiConst.WIDGET_LOGINLOGO2
    uiConst.WIDGET_LOGIN_WIN_RIGHT_BOTTOM = uiConst.WIDGET_LOGIN_WIN_RIGHT_BOTTOM2
    uiConst.WIDGET_LOGIN_WIN_LEFT_BOTTOM = uiConst.WIDGET_LOGIN_WIN_LEFT_BOTTOM2
    BigWorld.getPhaseMapping('universes/eg/test')
    pyBgTask.init()
    gameglobal.rds.isSinglePlayer = False
    gameglobal.rds.GameState = gametypes.GS_START
    gameglobal.rds.disconnectCB = None
    gameglobal.rds.offline = True
    gameglobal.rds.loginManager = None
    gameglobal.rds.configSect = scriptsConfig
    gameglobal.rds.cam = camera.instance()
    gameglobal.rds.reTryLoginOnTransferTimer = 0
    gameglobal.rds.reTryLoginOnTransferCnt = 0
    gameglobal.rds.macaddrs = clientcom.getMacAddress()
    gameglobal.rds.minShowUfoDist = gameglobal.NEED_BLACKUFO_DIST
    gameglobal.rds.needSendInfoToHttp = False
    AppSettings.load()
    _delPatchCache()
    _delAvatarConfig()
    from guis import cursor
    gameglobal.rds.UICursor = cursor.UICursor()
    gameglobal.rds.loginManager = login.getInstance()
    gameglobal.rds.ui = uiAdapter.getInstance()
    try:
        from helpers import gfeManager
        gameglobal.rds.gfe = gfeManager.getInstance()
    except:
        pass

    gameglobal.rds.tutorial = tutorial.initTutorManager()
    gameglobal.rds.sound = soundManager.SoundManager.getInstance()
    gameglobal.rds.uiLog = Hijack.UILogRecorder.getInstance()
    BigWorld.footSoundTag((1, 'grass'), (2, 'stone'), (3, 'water'), (4, 'wood'), (10, 'air'), (13, 'goldCoin'), (14, 'snow'), (15, 'metal'), (130, 'stone'), (132, 'lava'), (133, 'die'))
    BigWorld.footPlotterTag(('grass', 4294901760L), ('gravel', 4294901760L))
    BigWorld.entityPickerIgnoreMaterialKind(gameglobal.GLASS, gameglobal.DIE, gameglobal.TREE)
    BigWorld.loadingStep(100)
    BigWorld.limitForegroundFPS(60)
    if utils.getGameLanuage() not in ('en',):
        BigWorld.showWatermark(True, 'system/maps/logo_a.tga', uiConst.WATERMARK_LOGO_WIDTH, uiConst.WATERMARK_LOGO_HEIGHT)
    BigWorld.timeOrigin = BigWorld.time
    BigWorld.get_last_input_time_origin = BigWorld.get_last_input_time
    BigWorld.timeProxy = 0
    BigWorld.timeStill = 0
    gameglobal.rds.avatarModelCnt = appSetting.VideoQualitySettingObj.getAvatarCntWithVQ()
    gameglobal.rds.gameCode = AppSettings.get(keys.SET_GAME_CODE, '')
    _setRenderFeatures()
    if True:
        __import__('__main__').gamereload = gamereload
    C_ui.enableUI(True)
    tick()
    updateAmbientMusic.initSoundMap()
    capturePhoto.reloadPhotoXml()
    protect.nepInit()
    try:
        _preLoadAvatarConfig()
        initClientInfo()
    except:
        gamelog.error('zf:Error: _preLoadAvatarConfig is error')

    imeGUI = ime.ImeMainGUI()
    BigWorld.setImeGUI(imeGUI)
    gameglobal.rds.logLoginState = gameglobal.GAME_INIT
    netWork.sendInfoForLianYun(gameglobal.rds.logLoginState)


def tick():
    global GMAE_IS_PRELOAD
    global GMAE_IS_START
    global tickCallback
    if tickCallback:
        BigWorld.cancelCallback(tickCallback)
    asyncore.loop(0, True, None, 1)
    if gameglobal.rds.loginManager is not None:
        gameglobal.rds.loginManager.checkLogonState()
    if gameglobal.rds.GameState == gametypes.GS_START:
        if not GMAE_IS_START:
            GMAE_IS_START = True
            _setRenderFeatures()
        p = BigWorld.spaceLoadStatus(400)
        if p >= 0.9:
            if not GMAE_IS_PRELOAD:
                GMAE_IS_PRELOAD = True
                gamePreload()
                screenEffect.showDarkAngle(1)
                BigWorld.darkWorld(0)
                BigWorld.openApp(True)
    elif not GMAE_IS_PRELOAD:
        GMAE_IS_PRELOAD = True
        BigWorld.darkWorld(1)
        BigWorld.openApp(True)
    tickCallback = BigWorld.callback(0.2, tick)


def tickAsyncCore():
    global tickCallback
    if tickCallback:
        BigWorld.cancelCallback(tickCallback)
    asyncore.loop(0, True, None, 1)
    tickCallback = BigWorld.callback(1, tickAsyncCore)


def gamePreload():
    _preloadMiscEffect()
    xrjmSfx = []
    from data import char_show_new_data as CSND
    for school, schoolData in CSND.data.iteritems():
        for bodyData in schoolData:
            for effect in bodyData.get('MODEL_SCHOOL_LOGIN_NEW_EFFECT', {}).values():
                if type(effect) == tuple:
                    xrjmSfx.extend(effect)
                else:
                    xrjmSfx.append(effect)

    gamelog.info('jbx: gamePreload xrjmSfx', xrjmSfx)
    for fxId in xrjmSfx:
        sfx.gEffectMgr.preloadFx(fxId, gameglobal.EFFECT_HIGH)


def cancelTick():
    global tickCallback
    if tickCallback:
        BigWorld.cancelCallback(tickCallback)
        tickCallback = 0


def _preLoadAvatarConfig():
    from helpers import charRes
    avatarMorpher.preloadAllAvatarConfig(charRes.ALL_AVAIABLE_MODELS)


def _fcmp(x, y):
    xx = '../download/' + x
    yy = '../download/' + y
    ix = os.stat(xx)[stat.ST_MTIME]
    iy = os.stat(yy)[stat.ST_MTIME]
    return cmp(ix, iy)


def _delPatchCache():
    lst = []
    try:
        lst = os.listdir('../download')
    except:
        pass

    if len(lst) <= 3:
        return
    lst.sort(cmp=_fcmp)
    lst = lst[:len(lst) - 3]
    for i in lst:
        try:
            os.remove('../download/' + i)
        except:
            pass


def _delAvatarConfig():
    lst = []
    section = ResMgr.openSection(characterDetailAdjustProxy.PATH)
    if section:
        lst = section.keys()
        lst = [ item for item in lst if item.find(characterDetailAdjustProxy.AUTO_SAVE) != -1 ]
    l = len(lst)
    if l <= 5:
        return
    lst.sort()
    lst = lst[:l - 5]
    for i in lst:
        try:
            os.remove('./avatar/' + i)
        except:
            pass


def start():
    appSetting.SoundSettingObj.apply()
    appSetting.setScreenSize()
    navigator.initNav()
    BigWorld.enableVolumetricCloud(True)
    BigWorld.newAnimationMemoryLimit(True, 50)
    BigWorld.enableImposter(not gameglobal.gDisableImposter)
    if gameglobal.rds.enableBinkLogoCG:
        playBinkTitleCg(None, 'logo', Functor(endLogoCg, True))
    else:
        playTitleCg(None, 'logo', Functor(endLogoCg, True))
    gameglobal.rds.logLoginState = gameglobal.GAME_START
    netWork.sendInfoForLianYun(gameglobal.rds.logLoginState)
    if hasattr(BigWorld, 'enableNotifyclipboardMsg'):
        BigWorld.enableNotifyclipboardMsg(True)


def clearMusic():
    global isQuiting
    isQuiting = False
    gamelog.debug('game.clearMusic')
    Sound.clearMusic()
    Sound.turnoffReverb()
    updateAmbientMusic.endAmbientSound()


def fini():
    onQuit()
    netWork.sendInfoForLianYun(gameglobal.rds.logLoginState, True)
    miniclient.flushAllReports()
    protect.nepShutdown()
    return True


def cameraType(idx):
    newcam = gameglobal.rds.cam.camera(idx)
    newcam.set(BigWorld.camera().matrix)
    BigWorld.camera(newcam)


def onChangeEnvironments(inside):
    pass


def handleCharEvent(char):
    return False


def handleKeyEvent(down, key, vk, mods):
    rt = processKeyEvent(down, key, vk, mods)
    return rt


def handleMouseEvent(dx, dy, dz):
    GUI.handleMouseEvent(dx, dy, dz)
    if gameglobal.rds.loginScene.handleMouseEvent(dx, dy, dz):
        return True
    if gameglobal.rds.GameState == gametypes.GS_PLAYGAME:
        if not gameglobal.rds.configData.get('enableNewCamera', False) and gameglobal.rds.ui.camera.handleMouseEvent(dx, dy, dz):
            return True
        if gameglobal.rds.configData.get('enableNewCamera', False) and gameglobal.rds.ui.cameraV2.handleMouseEvent(dx, dy, dz):
            return True
        if editorHelper.instance().handleMouseEvent(dx, dy, dz):
            return True
        if dz < 0 and HK.checkMouseRollDown() or dz > 0 and HK.checkMouseRollUp():
            gameglobal.rds.cam.handleMouseEvent(dx, dy, dz)
    return False


def onQueryClose():
    uiUtils.onQuit()


isQuiting = False

def onQuit(muteMusic = True, isCrossServer = False):
    global isQuiting
    gamelog.debug('jjh@onQuit.......................')
    if isQuiting:
        return
    else:
        isQuiting = True
        if hasattr(gameglobal.rds, 'tutorial'):
            gameglobal.rds.tutorial.save()
        if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            scenario.Scenario.getInstanceInPlay().stopPlay()
        if muteMusic:
            BigWorld.callback(2, clearMusic)
        w, h, windowed, _ = BigWorld.getScreenState()
        if w < 800 or h < 600:
            w = 800
            h = 600
            windowed = 1
        if BigWorld.realFullScreen():
            windowed = 2
        appSetting.saveScreenSize(w, h, windowed)
        if getattr(gameglobal.rds, 'ccBox', None) and not isCrossServer:
            gameglobal.rds.ccBox.closeCCBox()
        return


def onRecreateDevice():
    gameglobal.rds.cam.setAdaptiveFov()


def _setRenderFeatures():
    global renderFeatures
    renderFeatures['deferred'] = True
    renderFeatures['vsm'] = True
    renderFeatures['hdr'] = True
    renderFeatures['hiQuality'] = True
    renderFeatures['plsm'] = True
    renderFeatures['cmdbuff'] = True
    renderFeatures['-dp'] = False
    BigWorld.renderFeatures('deferred', True)
    BigWorld.renderFeatures('vsm', False)
    BigWorld.renderFeatures('hdr', True)
    BigWorld.renderFeatures('hiQuality', True)
    BigWorld.renderFeatures('plsm', True)
    BigWorld.floraOption(True, 0)
    BigWorld.enableLODAll(False)
    BigWorld.enablePBRPointLight(True)
    BigWorld.enableSeaReflection(False)
    BigWorld.setVideoQuality(3)
    BigWorld.setForestSwitchDist(15000)
    BigWorld.TextureStreamingPrio(0)
    BigWorld.setViewFactor(0.21)


def onAppActivate(act):
    p = BigWorld.player()
    try:
        if gameglobal.rds.ui.loginWin.mc and act:
            gameglobal.rds.ui.loginWin.setCapsTip()
        if gameglobal.rds.GameState == gametypes.GS_PLAYGAME:
            if C_ui.cursor_in_clientRect():
                p and hasattr(p, 'ap') and p.ap.reset()
            else:
                p and hasattr(p, 'ap') and hasattr(p.ap, '_resumeCursor') and p.ap._resumeCursor(1, False)
        if act and p and hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE and p.ap.showCursor:
            p.ap._changeCursor(False)
        if p and act and (gameglobal.gIsAppActive == False or getattr(p, 'isPathfinding', False)) and hasattr(p, 'inCombat') and p.inCombat:
            BigWorld.flashWindow(0)
        gameglobal.gIsAppActive = act
        gameAntiCheatingManager.getInstance().recordLoseFocusData(act)
    except Exception as e:
        print 'error:', e


def toggleRenderFeature(feature):
    if feature not in ('hiQuality', 'deferred', 'hdr', 'vsm', 'cmdbuff', '-dp'):
        gamelog.error('ERROR: wrong render feature <%s>' % feature)
    cur = renderFeatures.get(feature, False)
    cur = not cur
    renderFeatures[feature] = cur
    if feature == 'cmdbuff':
        BigWorld.openCmdBuffer(cur)
    elif feature == '-dp':
        BigWorld.disableDrawCall(cur)
    else:
        BigWorld.renderFeatures(feature, cur)


org_inner_screen_size = 1.0
DAT_FILE = '../game/user.dat'

def hash(s):
    sha = hashlib.sha256()
    sha.update(s)
    return sha.hexdigest()[:8]


def afterScreenShotFinish(s):
    global org_inner_screen_size
    msg = gameStrings.TEXT_GAME_619 % (clientUtils.relativePath2AbsolutePath(s),)
    gameglobal.rds.ui.chat.addSystemMessage(msg)
    BigWorld.setInnerScreenSize(org_inner_screen_size)
    if not gameglobal.rds.configData.get('enableNewCamera', False):
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_CAMERA, True)
    else:
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_CAMERA_V2, True)
    BigWorld.callback(0, _setFov)
    cameraVersion = None
    if not gameglobal.rds.configData.get('enableNewCamera', False):
        cameraVersion = gameglobal.rds.ui.camera
    else:
        cameraVersion = gameglobal.rds.ui.cameraV2
    if cameraVersion.photoStyle and not gameglobal.rds.configData.get('enableNewCamera', False):
        try:
            from PIL import Image
            img = Image.open(s)
            w = img.size[0]
            h = img.size[1]
            newImg = img.crop((0 if h > w else int(w / 2 - h / 2),
             0 if w > h else int(h / 2 - w / 2),
             w if h > w else int(w / 2 + h / 2),
             h if w > h else int(w / 2 + h / 2)))
            newImg.save(s)
        except:
            pass

    elif gameglobal.rds.configData.get('enableNewCamera', False) and gameglobal.rds.ui.cameraV2.widget:
        selectedIndex = cameraVersion.widget.bg.content.cameraMode.selectedIndex
        if selectedIndex == 1 or selectedIndex == 2 or selectedIndex == 3:
            try:
                from PIL import Image
                img = Image.open(s)
                newImg = img.crop((int(cameraVersion.widget.leftShader.x + cameraVersion.widget.x),
                 0,
                 int(cameraVersion.widget.rightShader.x + cameraVersion.widget.x),
                 int(BigWorld.getScreenState()[1])))
                print newImg.size, newImg.mode, newImg.format
                newImg.save(s)
            except:
                pass

        elif selectedIndex == 4:
            try:
                from PIL import Image
                ima = Image.open(s)
                size = ima.size
                r2 = min(size[0], size[1])
                w = ima.size[0]
                h = ima.size[1]
                if size[0] != size[1]:
                    ima = ima.crop((0 if h > w else int(w / 2 - h / 2),
                     0 if w > h else int(h / 2 - w / 2),
                     w if h > w else int(w / 2 + h / 2),
                     h if w > h else int(w / 2 + h / 2)))
                r3 = r2 / 2
                imb = Image.new('RGBA', (r2, r2), (255, 255, 255, 0))
                pima = ima.load()
                pimb = imb.load()
                r = float(r2 / 2)
                for i in range(r2):
                    for j in range(r2):
                        lx = abs(i - r)
                        ly = abs(j - r)
                        l = (pow(lx, 2) + pow(ly, 2)) ** 0.5
                        if l < r3:
                            pimb[i - (r - r3), j - (r - r3)] = pima[i, j]

                imb.save(s)
            except:
                pass

    coord = gameglobal.rds.ui.needCutScreen()
    if coord:
        gameglobal.rds.ui.clearScreenCoord()
        try:
            from PIL import Image
            img = Image.open(s)
            newImage = img.crop(coord[0] + coord[1])
            newImage.save(s)
        except:
            pass

    BigWorld.callback(0.1, Functor(hijackImage, s))
    if cameraVersion.inPhotoing:
        if cameraVersion.isShow:
            cameraVersion.setPhotoPath(s)
        cameraVersion.inPhotoing = False
    BigWorld.callback(1, Functor(gameglobal.rds.ui.qrCodeAppScanShare.onScreenShotFinished, s))


def hijackImage(path):
    pngEncode = PNGEncode.PNGEncode()
    pngEncode.open(path)
    pngEncode.insertMD5()
    pngEncode.save()


def _setFov():
    if not gameglobal.rds.configData.get('enableNewCamera', False):
        if gameglobal.rds.ui.camera.fovCurrent:
            BigWorld.projection().fov = gameglobal.rds.ui.camera.fovCurrent
    elif gameglobal.rds.ui.cameraV2.fovCurrent:
        BigWorld.projection().fov = gameglobal.rds.ui.cameraV2.fovCurrent


def startSetLoginCamera():
    gameglobal.rds.loginScene.spaceID = None
    from helpers import cameraControl
    m = BigWorld.camera().matrix
    cameraControl.newTrack()
    BigWorld.camera().set(m)


def processKeyEvent(down, key, vk, mods, isReplay = False):
    global cgMovie
    gameglobal.rds.lastKey = key
    gameglobal.rds.ui.ziXunInfo.recordTime()
    gameAntiCheatingManager.getInstance().recordKeyData(key, down)
    if key == keys.KEY_P and down and mods == 6:
        if utils.getGameLanuage() in ('en',):
            projectId = AppSettings.get('conf/projectId', '13.2000026')
            cmd = 'start mycomgames://demandgamingform/%s' % projectId
            subprocess.Popen(cmd, shell=True)
    if key == keys.KEY_SYSRQ:
        if gameglobal.rds.ui.isHideAllUI():
            return True
        if not gameglobal.rds.configData.get('enableNewCamera', False):
            gameglobal.rds.ui.camera.takePhoto()
        else:
            gameglobal.rds.ui.cameraV2.onBeginTakePhoto()
        return True
    elif key == keys.KEY_SCROLL:
        if hasattr(BigWorld, 'hdrCaptureThisFrame'):
            BigWorld.hdrCaptureThisFrame()
        return True
    if key == keys.KEY_ESCAPE:
        if cgMovie and cgMovie.isPlaying:
            if cgMovie.cgName in ('intro_1', 'logo'):
                endLogoCg()
                return True
            if cgMovie.cgName == 'bw':
                gameglobal.rds.ui.characterCreate.endTitleCg()
            elif cgMovie.cgName == 'xuanren' and BigWorld.player():
                BigWorld.player().endVideo()
                return True
        if gameglobal.rds.ui.clearState():
            return True
        if gameglobal.rds.loginScene.inSelectOneStage() and isinstance(CC.TC, BigWorld.FreeCamera):
            gameglobal.rds.loginScene._directlyEnterCharacterSelectTwo()
            return True
    if hasattr(gameglobal.rds, 'tutorial'):
        gameglobal.rds.tutorial.onKeyEvent(down, key, vk, mods)
    if gameglobal.rds.GameState == gametypes.GS_LOADING:
        return 1
    if key == keys.KEY_LEFTMOUSE:
        if down:
            gameglobal.rds.UICursor.downCursor()
        else:
            gameglobal.rds.UICursor.upCursor()
    if key == keys.KEY_Y or key == keys.KEY_N:
        if down == True:
            topWidget = gameglobal.rds.ui.getTopWidgetId()
            if topWidget[0] in (uiConst.WIDGET_MESSAGEBOX, uiConst.WIDGET_MESSAGEBOX_LOW):
                if gameglobal.rds.ui.messageBox.loadeds.get(topWidget[1]):
                    if gameglobal.rds.ui.messageBox.onClickKey(topWidget[1], key):
                        return True
            if topWidget[0] == uiConst.WIDGET_USE_ITEM:
                if gameglobal.rds.ui.itemUse.onClickKey(key):
                    return True
            if topWidget[0] == uiConst.WIDGET_MONEY_CONVERT_COMFIRM:
                if gameglobal.rds.ui.moneyConvertConfirm.mediator:
                    if key == keys.KEY_Y:
                        gameglobal.rds.ui.moneyConvertConfirm.doYes()
                    else:
                        gameglobal.rds.ui.moneyConvertConfirm.hide()
                    return True
            if topWidget[0] in (uiConst.WIDGET_CONSIGN_BID, uiConst.WIDGET_CONSIGN_BUY):
                gameglobal.rds.ui.consign.shortKeyDown(key)
                return True
            if topWidget[0] in (uiConst.WIDGET_TAB_CONSIGN_BID, uiConst.WIDGET_TAB_CONSIGN_BUY):
                gameglobal.rds.ui.tabAuctionConsign.shortKeyDown(key)
                return True
            if topWidget[0] in (uiConst.WIDGET_TAB_CROSS_SERVER_BID,):
                gameglobal.rds.ui.tabAuctionCrossServer.shortKeyDown(key)
                return True
            if topWidget[0] == uiConst.WIDGET_INTERACTIVE_CONFIRM:
                gameglobal.rds.ui.interactiveObjConfirm.onClickKey(key)
                return True
    if down:
        event = Event(events.EVENT_KEY_DOWN, (key, mods))
        gameglobal.rds.ui.dispatchEvent(event)
        if event.handled:
            return True
    gameglobal.rds.ui.zaijuV2.handleKey(down, key, vk, mods)
    rt = C_ui.handleKeyEvent(down, key, vk, mods)
    if rt:
        return rt
    elif gameglobal.rds.ui.handleKeyEvent(down, key, vk, mods):
        return 1
    elif GUI.handleKeyEvent(down, key, mods):
        return 1
    if hasattr(BigWorld.camera(), 'handleTrackKeyEvent') and gameglobal.rds.loginScene.spaceID == None and gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_END and not gameglobal.rds.ui.bfDotaChooseHeroBottom.widget:
        _tc = BigWorld.camera()
        if key == keys.KEY_RIGHTMOUSE:
            _tc.locked = down
        if not gameglobal.rds.configData.get('enableNewCamera', False):
            if gameglobal.rds.ui.camera.isShow or gameglobal.rds.ui.storyEditDebug.cameraIsOpen:
                mods = keys.MODIFIER_SHIFT
        elif gameglobal.rds.ui.cameraV2.isShow or gameglobal.rds.ui.storyEditDebug.cameraIsOpen:
            mods = keys.MODIFIER_SHIFT
        _processed = _tc.handleTrackKeyEvent(down, key, vk, mods)
        if _processed:
            return True
    if hasattr(gameglobal.rds, 'loginScene') and (gameglobal.rds.loginScene.player or gameglobal.rds.loginScene.loginModel or gameglobal.rds.loginScene.multiModels or gameglobal.rds.loginScene.inCreateSelectNewStage()):
        if gameglobal.rds.loginScene.handleKeyEvent(down, key, vk, mods):
            return True
    cameraVersion = gameglobal.rds.ui.cameraV2
    if not gameglobal.rds.configData.get('enableNewCamera', False):
        cameraVersion = gameglobal.rds.ui.camera
    if cameraVersion.handleKeyEvent(down, key, vk, mods):
        return True
    elif editorHelper.instance().handleKeyEvent(down, key, vk, mods):
        return True
    else:
        return False


def handleMouseEventDebug(dx, dy, dz):
    return 0


def onProxyDataDownloadComplete(proxyID, datum):
    data = cPickle.loads(zlib.decompress(datum))
    if proxyID == const.PROXY_KEY_TOP_EQUIP_SCORE:
        info = processTopData(data)
        info = [ (gbId,
         name,
         school,
         int(val)) for gbId, name, school, val in info ][:500]
        lastWeekRankInfo = data[2]
        gameglobal.rds.ui.ranking.updateEquipData(data[0], info, lvKeyStr=data[-1])
    elif proxyID == const.PROXY_KEY_TOP_UNIVERSAL:
        gameglobal.rds.ui.ranking.updateCommnonRankData(data)
        gamelog.debug('@zhangkuo ', str(data))
    elif proxyID == const.PROXY_KEY_TOP_COMBAT_SCORE:
        info = processTopData(data)
        info = [ (gbId,
         name,
         school,
         int(val[0])) for gbId, name, school, val in info ][:500]
        lastWeekRankInfo = data[2]
        gameglobal.rds.ui.ranking.updateCombatData(data[0], info, lastWeekRankInfo, lvKeyStr=data[-1])
    elif proxyID == const.PROXY_KEY_TOP_LEVEL:
        info = processTopData(data)
        info = info[:500]
        lastWeekRankInfo = data[2]
        gameglobal.rds.ui.ranking.updateLvData(data[0], info)
    elif proxyID == const.PROXY_KEY_TOP_ARENA_SCORE:
        gameglobal.rds.ui.arenaRankList.refreshArenaInfo(data['version'], data['data'], data['key'], data['myRank'])
    elif proxyID == const.PROXY_KEY_TOP_FB_TIME:

        def fbCmp(a, b):
            vala = a[3]
            valb = b[3]
            if vala[0] > valb[0] or vala[0] == valb[0] and vala[1] < valb[1] or vala[:2] == valb[:2] and vala[2] < valb[2]:
                return 1
            if vala == valb:
                return 0
            return -1

        info = data[1]
        if info:
            info.sort(cmp=fbCmp)
            info.reverse()
            info = info[:100]
        lastWeekRankInfo = data[2]
        gameglobal.rds.ui.ranking.updateFubenData(data[0], info, lastWeekRankInfo, data[3], data[4])
    elif proxyID == const.PROXY_KEY_TOP_CLAN_WAR_SCORE:
        info = data[1]
        info.sort(key=lambda a: a[2])
        info.reverse()
        gameglobal.rds.ui.ranking.updateGuildData(proxyID, data[0], info, [])
    elif proxyID == const.PROXY_KEY_TOP_GUILD_PROSPERITY:
        info = data[1]
        info.sort(key=lambda a: a[2])
        info.reverse()
        lastWeekRankInfo = data[2]
        gameglobal.rds.ui.ranking.updateGuildData(proxyID, data[0], info, lastWeekRankInfo)
    elif proxyID == const.PROXY_KEY_TOP_GUILD_MATCH:
        info = data[1]
        info.sort(key=lambda a: a[2])
        info.reverse()
        lastWeekRankInfo = data[2]
        gameglobal.rds.ui.ranking.updateGuildData(proxyID, data[0], info, lastWeekRankInfo)
    elif proxyID == const.PROXY_KEY_TOP_GUILD_HUNT:
        info = data[1]
        info.sort(key=lambda a: a[2])
        info.reverse()
        for a in info:
            a[2] = -a[2]

        lastWeekRankInfo = data[2]
        gameglobal.rds.ui.ranking.updateGuildData(proxyID, data[0], info, lastWeekRankInfo)
    elif proxyID == const.PROXY_KEY_TOP_GUILD_ROBBER_RANK:
        info = data[1]
        info.sort(key=lambda a: a[2])
        lastWeekRankInfo = data[2]
        gameglobal.rds.ui.ranking.updateGuildData(proxyID, data[0], info, lastWeekRankInfo)
    elif proxyID == const.PROXY_KEY_TOP_GUILD_KINDNESS:
        info = data[1]
        info.sort(key=lambda a: a[2])
        info.reverse()
        lastWeekRankInfo = data[2]
        gameglobal.rds.ui.ranking.updateGuildData(proxyID, data[0], info, lastWeekRankInfo)
    elif proxyID == const.PROXY_KEY_TOP_GUILD_CHICKEN_MEAL:
        gamelog.debug('@zqx PROXY_KEY_TOP_GUILD_CHICKEN_MEAL ', data)
        info = data[1]
        info.sort(key=lambda a: a[2])
        info.reverse()
        lastWeekRankInfo = data[2]
        gameglobal.rds.ui.ranking.updateGuildData(proxyID, data[0], info, lastWeekRankInfo)
    elif proxyID == const.PROXY_KEY_TOP_GUILD_MONSTER_CLAN_WAR:
        gamelog.debug('@jbx PROXY_KEY_TOP_GUILD_MONSTER_CLAN_WAR ', data)
        info = data[1]
        info.sort(key=lambda a: a[2])
        info.reverse()
        lastWeekRankInfo = data[2]
        gameglobal.rds.ui.ranking.updateGuildData(proxyID, data[0], info, lastWeekRankInfo)
    elif proxyID == const.PROXY_KEY_TOP_GUILD_FISH_ACTIVITY:
        gamelog.debug('@zqx PROXY_KEY_TOP_GUILD_FISH_ACTIVITY ', data)
        info = data[1]
        info.sort(key=lambda a: a[2])
        info.reverse()
        lastWeekRankInfo = data[2]
        gameglobal.rds.ui.ranking.updateGuildData(proxyID, data[0], info, lastWeekRankInfo)
    elif proxyID == const.PROXY_KEY_TOP_GUILD_YMF:
        gamelog.debug('@zqx PROXY_KEY_TOP_GUILD_YMF ', data)
        gameglobal.rds.ui.yumufengGuildRank.updateData(data[0], data[1], data[2])
    elif proxyID == const.PROXY_KEY_GUILD_TOURNAMENT:
        BigWorld.player().onQueryGuildTournament(data[0], data[1], data[2])
    elif proxyID == const.PROXY_KEY_GUILD_TOURNAMENT_RANKS:
        BigWorld.player().onQueryGuildTournamentRanks(data[0], data[1], data[2])
    elif proxyID == const.PROXY_KEY_WW_GUILD_TOURNAMENT_RANKS:
        BigWorld.player().onQueryWWGuildTournamentRanks(data[0], data[1], data[2], data[3])
    elif proxyID == const.PROXY_KEY_CROSS_GTN:
        BigWorld.player().onQueryCrossGtn(data[0], data[1], data[2])
    elif proxyID == const.PROXY_KEY_GUILD_NOVICE_BOOST:
        BigWorld.player().onQueryGuildNoviceBoost(data[0], data[1], data[2])
    elif proxyID == const.PROXY_KEY_WORLD_WAR_QUERY:
        BigWorld.player().onQueryWorldWar(data[0], data[1], data[2])
    elif proxyID == const.PROXY_KEY_WORLD_WAR_QUERY_COUNTRIES:
        BigWorld.player().onQueryWorldWarCountries(data[0], data[1])
    elif proxyID == const.PROXY_KEY_WORLD_WAR_QUERY_RANK:
        BigWorld.player().onQueryWorldWarRank(data[0], data[1])
    elif proxyID == const.PROXY_KEY_WORLD_WAR_ARMY_QUERY:
        BigWorld.player().onQueryWorldWarArmy(data[0], data[1], data[2], data[3])
    elif proxyID == const.PROXY_KEY_WORLD_WAR_ARMY_ONLINE_QUERY:
        BigWorld.player().onQueryWorldWarArmyOnline(data[0], data[1])
    elif proxyID == const.PROXY_KEY_TOP_SOCAIL_LEVEL:
        info = processTopData(data)
        info = info[:500]
        gameglobal.rds.ui.ranking.updateSocietyData(data[0], info, data[-1])
    elif proxyID == const.PROXY_KEY_HOTFIX:
        hotfixMD5 = md5.md5(datum).digest()
        runHotfix(data, hotfixMD5)
    elif proxyID == const.PROXY_KEY_PLAYER_LOGON_DATA:
        if gameglobal.rds.configData.get('enableSendAvatarDataOptimization', True):
            k, v = data
            if k == '_begin_':
                gameglobal.rds.playerLogonData = {}
                mapName = C_ui.get_map_name()[0]
                if gameglobal.loadingSpaceNo:
                    mapName = formula.whatSpaceMap(gameglobal.loadingSpaceNo)
                if mapName:
                    mapName = mapName.split('/')[2].strip()
                loadingProgress.instance().show(True, mapName, True)
            elif k == '_end_':
                if gameglobal.rds.configData.get('enableSendAvatarDataNoChangeToItem', True):
                    parsePlayerLogonData(gameglobal.rds.playerLogonData)
                BigWorld.player().base.onSendAvatarData()
            else:
                gameglobal.rds.playerLogonData[k] = v
        else:
            gameglobal.rds.playerLogonData = data
            if gameglobal.rds.configData.get('enableSendAvatarDataNoChangeToItem', True):
                parsePlayerLogonData(gameglobal.rds.playerLogonData)
            mapName = C_ui.get_map_name()[0]
            if gameglobal.loadingSpaceNo:
                mapName = formula.whatSpaceMap(gameglobal.loadingSpaceNo)
            if mapName:
                mapName = mapName.split('/')[2].strip()
            loadingProgress.instance().show(True, mapName, True)
            BigWorld.player().base.onSendAvatarData()
    elif proxyID == const.PROXY_KEY_TOP_ACHIEVE_POINTS:
        info = processTopData(data)
        info = info[:const.TOP_ACHIEVE_POINTS_NUM]
        lastWeekRankInfo = data[2]
        gameglobal.rds.ui.ranking.updateAchieveData(data[0], info, lastWeekRankInfo, lvKeyStr=data[-1])
    elif proxyID == const.PROXY_KEY_TOP_FISHING_SCORE:
        info = data[1]
        info.sort(key=lambda k: k[3].get('score', 0))
        info.reverse()
        gamelog.debug('zt: fishing top data', data)
        gameglobal.rds.ui.fishingGame.setRank(proxyID, data[0], info)
    elif proxyID == const.PROXY_KEY_REG_DATA:
        from helpers import taboo
        if data[0]:
            for kw in data[0]:
                taboo.keywordToCheck([kw])

    elif proxyID == const.PROXY_KEY_CONSIGN_OTHERS:
        BigWorld.player().onConsignShowOthers(data)
    elif proxyID == const.PROXY_KEY_COIN_CONSIGN_OTHERS:
        BigWorld.player().onCoinConsignShowOthers(data)
    elif proxyID == const.PROXY_KEY_TOP_CLANWAR_GUILD:
        p = BigWorld.player()
        if p:
            p.clanWarGuildRank = data
        gameglobal.rds.ui.clanWar.setClanWarGuildRank(data)
        gameglobal.rds.ui.crossClanWar.refreshCommonInfo()
        gameglobal.rds.ui.crossClanWarRank.refreshClanWarGuildRank()
    elif proxyID == const.PROXY_KEY_TOP_CLANWAR_PLAYER:
        p = BigWorld.player()
        if p:
            p.clanWarPlayerRank = data
        gameglobal.rds.ui.clanWar.setClanWarPlayerRank(data)
        gameglobal.rds.ui.crossClanWar.refreshInfo()
        gameglobal.rds.ui.crossClanWarRank.refreshClanWarGuildRank()
    elif proxyID == const.PROXY_KEY_CLANWAR_PLAYER_INFO:
        p = BigWorld.player()
        if p:
            p.clanWarPlayerInfo = data
        gameglobal.rds.ui.clanWar.setClanWarPlayerInfo(data)
        gameglobal.rds.ui.crossClanWar.refreshCommonInfo()
    elif proxyID == const.PROXY_KEY_CLANWAR_PLAYER_RESULT:
        gameglobal.rds.ui.clanWar.setClanWorResult(data)
    elif proxyID == const.PROXY_KEY_CLANWAR_FORT_DATA:
        BigWorld.player().onLoadClanWarData(data)
    elif proxyID == const.PROXY_KEY_CLAN_ALL:
        BigWorld.player().onGetAllClan(data)
    elif proxyID == const.PROXY_KEY_CLAN:
        BigWorld.player().onGetClan(data)
    elif proxyID == const.PROXY_KEY_CLAN_APPLY:
        BigWorld.player().onGetClanApply(data)
    elif proxyID == const.PROXY_KEY_GUILD:
        BigWorld.player().onLoadGuild(data[0], data[1], False)
        BigWorld.player().base.onRecvGuildDataOnLogon()
    elif proxyID == const.PROXY_KEY_GUILD_STATS:
        BigWorld.player().onQueryGuildStats(data[0], data[1], data[2], data[3])
    elif proxyID == const.PROXY_KEY_GUILD_PAYROLL:
        BigWorld.player().onQueryGuildPayroll(data)
    elif proxyID == const.PROXY_KEY_GUILD_MEMBER_PAYMENTS:
        BigWorld.player().onQueryGuildMemberPayments(data)
    elif proxyID == const.PROXY_KEY_CLAN_ALL_GUILD:
        BigWorld.player().onGetClanAllGuild(data)
    elif proxyID == const.PROXY_KEY_DECLARE_WAR_ALL_GUILD:
        BigWorld.player().onGetDeclareWarAllGuild(data)
    elif proxyID == const.PROXY_KEY_ALL_GUILD_LIMIT_INFO:
        gameglobal.rds.ui.guild.challengeSearchBack(data.get('queryStr', ''), data.get('data', []))
    elif proxyID == const.PROXY_KEY_GUILD_CHALLENGE_RESULT:
        gameglobal.rds.ui.guild.refreshChallengeListInfo(data.get('version', 0), data.get('data', []))
    elif proxyID == const.PROXY_KEY_GUILD_MY_CHALLENGE_RESULT:
        gameglobal.rds.ui.guild.refreshBuffListInfo(data.get('version', 0), data.get('data', []))
    elif proxyID == const.PROXY_KEY_MD5_DATA:
        Hijack.on_md5_hotfix(data[0])
    elif proxyID == const.PROXY_KEY_BATTLE_FIELD_ALL:
        BigWorld.player().battleFieldQuery(*data)
    elif proxyID == const.PROXY_KEY_QINGGONG_JINGSU_DATA:
        gameglobal.rds.ui.qingGongJingSu.show(data)
    elif proxyID == const.PROXY_KEY_TOP_ML_CLANWAR_SCORE:
        gameglobal.rds.ui.suiXingYu.onGetResultData(data)
    elif proxyID == const.PROXY_KEY_ML_CLANWAR_GUILD_RANK:
        gameglobal.rds.ui.suiXingYu.onGetGuildRankData(data)
    elif proxyID == const.PROXY_KEY_MLWMD_GUILD_RANK:
        gameglobal.rds.ui.wmdRankList.updateGuildData(data)
    elif proxyID == const.PROXY_KEY_MLWMD_MEMBER_RANK:
        gameglobal.rds.ui.wmdRankList.updatePersonalData(data)
    elif proxyID == const.PROXY_KEY_MLWMD_KILL_RANK:
        gameglobal.rds.ui.wmdRankList.updateKillData(data)
    elif proxyID == const.PROXY_KEY_TOP_YUNCHUI_HISTORY_KEY:
        gameglobal.rds.ui.ycwzRankList.updateSeasonList(data)
    elif proxyID == const.PROXY_KEY_TOP_YUNCHUI_GUILD_RANK:
        if len(data) > 0:
            if data[3] == '0':
                gameglobal.rds.ui.ycwzRankList.updateCurrentData(data)
            else:
                gameglobal.rds.ui.ycwzRankList.updateHistoryData(data)
    elif proxyID == const.PROXY_KEY_TOP_ZHAN_XUN_RANK:
        gameglobal.rds.ui.famousRankList.refreshZhanxunRankInfo(data)
        gameglobal.rds.ui.roleInformationJunjie.setFamousGeneralVal(data)
    elif proxyID == const.PROXY_KEY_SERVER_PROGRESS:
        BigWorld.player().onServerProgressData(data)
    elif proxyID == const.PROXY_KEY_TOP_GLOBAL_ARENA_SCORE:
        gameglobal.rds.ui.arenaRankList.refreshCrossArenaInfo(data['version'], data['data'], data['key'], data['myRank'])
        if gameglobal.rds.ui.pvPPanel.getPlayerTopRankKey() == data['key']:
            gameglobal.rds.ui.pvpArenaV2.setSeverRank(data['myRank'])
    elif proxyID == const.PROXY_KEY_TOP_WW_COMBO_KILL:
        pass
    elif proxyID == const.PROXY_KEY_QUERY_PARTNERS_EQUIPMENT:
        gamelog.debug('@zq PROXY_KEY_QUERY_PARTNERS_EQUIPMENT:', data)
        BigWorld.player().partnerEquipment = data
        gameglobal.rds.ui.partnerMain.refreshInfo()
    elif proxyID == const.PROXY_KEY_QUERY_SINGLE_PARTNER_EQUIPMENT:
        gamelog.debug('@zq PROXY_KEY_QUERY_SINGLE_PARTNER_EQUIPMENT:', data)
        BigWorld.player().partnerEquipment.update(data)
        for gbId in data.keys():
            gameglobal.rds.ui.partnerMain.refreshPhotoByGbId(gbId)

    elif proxyID == const.PROXY_KEY_TOP_WW_ROB_SCORE or proxyID == const.PROXY_KEY_TOP_WW_ROB_SCORE:
        gameglobal.rds.ui.worldWarRobRank.setWWRobTopData(data)
    elif proxyID == const.PROXY_KEY_GROUP_FB_RANK:
        data = cPickle.loads(zlib.decompress(data))
        gameglobal.rds.ui.ranking.updateTeamData(data['version'], data['data'], data['fbNo'])
    elif proxyID == const.PROXY_KEY_GROUP_FB_RANK_BAK:
        data = cPickle.loads(zlib.decompress(data))
        gameglobal.rds.ui.ranking.updateLastWeekRankList(data['data'], data['fbNo'])
    elif proxyID == const.PROXY_KEY_GROUP_JINGSU_FB_RANK:
        gameglobal.rds.ui.newServiceFubenRace.updateTeamData(data['version'], data['data'], data['fbNo'])
    elif proxyID == const.PROXY_KEY_GROUP_JINGSU_FB_RANK_BAK:
        gameglobal.rds.ui.newServiceFubenRace.updateTeamData(-1, data['data'], data['fbNo'], isBak=True)
    elif proxyID in (const.PROXY_KEY_TOP_RENPIN,
     const.PROXY_KEY_TOP_HAOQI,
     const.PROXY_KEY_TOP_PERSONAL_ZONE_GIFT,
     const.PROXY_KEY_TOP_PERSONAL_ZONE_POPULARITY):
        info = processTopData(data)
        info = info[:100]
        gameglobal.rds.ui.ranking.updateShejiaoData(proxyID, data[0], info, data[2])
    elif proxyID == const.PROXY_KEY_MONSTER_CLAN_WAR_RESULT:
        gameglobal.rds.ui.monsterClanWarActivity.updateMonsterAttackData(data)
    elif proxyID == const.PROXY_KEY_TOP_APPEARANCE_POINT:
        info = processTopData(data)
        info = info[:100]
        gameglobal.rds.ui.ranking.updateShejiaoData(proxyID, data[0], info, data[2])
    elif proxyID == const.PROXY_KEY_YMF_MEMBER_POS:
        info, isFinished = data
        BigWorld.player().onGetYmfMemberInfo(info, isFinished)
    elif proxyID == const.PROXY_KEY_LOTTERY_RESULT:
        gameglobal.rds.ui.lottery.setHistoryInfo(data)
    elif proxyID == const.PROXY_KEY_BONUS_HISTORY:
        gameglobal.rds.ui.fubenAwardTimes.setInfo(data)
        gameglobal.rds.ui.playRecommActivation.setBonusHistory(data)
        gameglobal.rds.ui.guild.setBonusHistory(data)
        gameglobal.rds.ui.voidDreamland.updateLeftChallengeCount(data)
        chickenFoodFactory.getInstance().setTopRankData(data, 0)
        gameglobal.rds.ui.avoidDoingActivity.setBonusHistory(data)
        _, updateBonusHistory = data
        BigWorld.player().bonusHistory.update(updateBonusHistory)
        gameglobal.rds.ui.spriteChallenge.refreshRemainRewardTime()
    elif proxyID == const.PROXY_KEY_TOP_APPRENTICE_VAL:
        info = processTopData(data)
        info = info[:100]
        gameglobal.rds.ui.ranking.updateShejiaoData(proxyID, data[0], info, data[2])
    elif proxyID == const.PROXY_KEY_SEARCH_PLAYER:
        BigWorld.player().onSearchPlayer(data[0], data[1])
    elif proxyID == const.PROXY_KEY_RECOMMEND_FRIEND:
        BigWorld.player().onRecommendFriend(data)
    elif proxyID == const.PROXY_KEY_CLIENT_PACKAGE_DATA:
        print 'jorsef: getClientPackageCheckData', data
        gameglobal.rds.clientPackageCheckData = data
    elif proxyID == const.PROXY_KEY_CLANWAR_GUILD_ZAIJU_USEDLIST:
        gameglobal.rds.ui.zhancheInfo.setItemInfo(data)
    elif proxyID == const.PROXY_KEY_TOP_CHICKEN_MAIL:
        gamelog.debug('@zq PROXY_KEY_TOP_CHICKEN_MAIL', data)
        chickenFoodFactory.getInstance().setTopRankData(data, 1)
    elif proxyID == const.PROXY_KEY_XCONSIGN_CURRENT_INFO:
        gamelog.debug('@smj PROXY_KEY_XCONSIGN_CURRENT_INFO')
        BigWorld.player().onGetXConsignInfoByCurDBIDs(data[0], data[1], data[2], data[3])
    elif proxyID == const.PROXY_KEY_XCONSIGN_CLEAR_INFO:
        gamelog.debug('@smj PROXY_KEY_XCONSIGN_CLEAR_INFO')
        BigWorld.player().onXConsignInfoByResultClrDBIDs(data[0], data[1])
    elif proxyID == const.PROXY_KEY_TOP_HOME_WEALTH:
        gamelog.debug('@xzh PROXY_KEY_TOP_HOME_WEALTH', data)
        info = processTopDataWithTimestamp(data)
        info = info[:100]
        gameglobal.rds.ui.ranking.updateShejiaoData(proxyID, data[0], info, data[2])
    elif proxyID == const.PROXY_KEY_TOP_FAMOUS_GENERAL_LV:
        gameglobal.rds.ui.famousRankList.refreshFamousRankInfo(data)
    elif proxyID == const.PROXY_KEY_OFFLINE_SYSTEM_NOTIFY:
        BigWorld.player().handleOfflineSystemNotifies(data[0])
    elif proxyID == const.PROXY_KEY_SPRITE_LIST_SEND:
        BigWorld.player().summonSpriteUpdate(data[0], data[1], False, False)
        BigWorld.player().updateLastSummonedSpriteIndex(data[2])
        BigWorld.player().updateSummonSpriteExtraDict(data[3])
    elif proxyID == const.PROXY_KEY_ENDLESS_CHALLENGE:
        info = {'ver': data[0],
         'season': data[3],
         'lvKey': data[-1],
         'info': data[1],
         'season': data[-2]}
        gameglobal.rds.ui.ranking.updateHuanjingData(info)
    elif proxyID == const.PROXY_KEY_TOP_FAMOUS_GENERAL_RECORD:
        gamelog.debug('@lhb PROXY_KEY_TOP_FAMOUS_GENERAL_RECORD ', data)
        gameglobal.rds.ui.famousRecordCommList.show(data=data)
    elif proxyID == const.PROXY_KEY_PRIVATE_SHOP_DATA:
        gamelog.debug('@smj private shop data', data)
        BigWorld.player().privateShopItemsUpdate(data[0], data[1:])
    elif proxyID == const.PROXY_KEY_SKILL_INFO:
        gamelog.debug('@zqx skill info data ', data)
        BigWorld.player().sharedSkillData = data
        gameglobal.rds.ui.skillShareBG.show()
    elif proxyID == const.PROXY_KEY_CLIENT_PERFORMANCE_FILTER:
        gamelog.debug('@zqx client performance filter data ', data)
        BigWorld.player().monitor.init(data)
    elif proxyID == const.PROXY_KEY_INIT_FRIEND_LIST:
        BigWorld.player().initFriend(*data)
    elif proxyID == const.PROXY_KEY_GET_ACHIEVEMENT:
        BigWorld.player().resSetAchievement(*data)
    elif proxyID == const.PROXY_KEY_GET_ACHIEVEMENT_OTHER:
        BigWorld.player().resSetOtherAchievement(*data)
    elif proxyID == const.PROXY_KEY_CONFIG_DATA:
        BigWorld.player().updateClientConfig(data)
    elif proxyID in [const.PROXY_KEY_HALL_OF_FAME_XIUWEI,
     const.PROXY_KEY_HALL_OF_FAME_SHENBING,
     const.PROXY_KEY_HALL_OF_FAME_HONGYAN,
     const.PROXY_KEY_HALL_OF_FAME_YINGCAI,
     const.PROXY_KEY_HALL_OF_FAME_QIAOJIANG,
     const.PROXY_KEY_HALL_OF_FAME_GUIBAO,
     const.PROXY_KEY_HALL_OF_FAME_MINGSHI]:
        gameglobal.rds.ui.celebrityRank.updateData(data, proxyID)
        if proxyID == const.PROXY_KEY_HALL_OF_FAME_XIUWEI:
            gameglobal.rds.ui.celebrityXiuWeiRank.getXiuWeiValue()
        elif proxyID == const.PROXY_KEY_HALL_OF_FAME_SHENBING:
            gameglobal.rds.ui.celebrityEquipmentRank.getShenBingValue()
        else:
            gameglobal.rds.ui.celebrityVoteRank.getVoteValue()
    elif proxyID == const.PROXY_KEY_HISTORY_HALL_OF_FAME:
        gameglobal.rds.ui.famerRankHistory.onGetRankData(data[0], data[1], data[2])
    elif proxyID == const.PROXY_KEY_GET_INTERACT_TEAMS:
        BigWorld.player().onGetInteractTeams(data)
    elif proxyID == const.PROXY_KEY_GUILD_CONSIGNMENT_GOODS_DATA:
        gameglobal.rds.ui.guildAuctionGuild.updateItemListInfo(data[0], data[1], data[2])
    elif proxyID == const.PROXY_KEY_WORLD_CONSIGNMENT_GOODS_DATA:
        gameglobal.rds.ui.guildAuctionWorld.updateItemListInfo(data[0], data[1])
    elif proxyID == const.PROXY_KEY_QUERY_ALL_GUILD_RED_PACKET:
        BigWorld.player().onQueryAllGuildRedPacket(*data)
    elif proxyID == const.PROXY_KEY_QUERY_GUILD_RED_PACKET:
        BigWorld.player().onQueryGuildRedPacket(*data)
    elif proxyID == const.PROXY_KEY_QUERY_GUILD_RED_PACKET_POOL:
        BigWorld.player().onQueryGuildAchieveRedPacketPool(*data)
    elif proxyID == const.PROXY_KEY_TOP_GUILD_PRESTIGE:
        info = data[1]
        info.sort(cmp=lambda a, b: cmp(a[2][0], b[2][0]) or cmp(a[2][1], b[2][1]) or -cmp(a[5], b[5]), reverse=True)
        gameglobal.rds.ui.ranking.updateGuildData(proxyID, data[0], info, data[2])
    elif proxyID == const.PROXY_MARRIAGE_RED_PACKET:
        gamelog.debug('@zq PROXY_MARRIAGE_RED_PACKET', data)
        BigWorld.player().onSyncRedPacketInfo(data[0])
    elif proxyID == const.PROXY_KEY_WING_WORLD_BOSS_DAMAGE:
        gameglobal.rds.ui.bossDamageRank.onGetTopWingWorldBoss(data)
    elif proxyID == const.PROXY_KEY_WING_WORLD_OPEN_DONATE:
        gameglobal.rds.ui.removeSealRank.onGetTopWingWorldOpenDonate(data)
    elif proxyID == const.PROXY_KEY_TOP_GUILD_LADY_RANK:
        info = data[1]
        info.sort(key=lambda a: (a[3][0], a[3][3], a[3][1]))
        info.reverse()
        gameglobal.rds.ui.ranking.updateShejiaoData(proxyID, data[0], info, data[2])
    elif proxyID == const.PROXY_KEY_REWARD_RECOVERY:
        BigWorld.player().onProxySendRewardRecoveryActivity(data)
    elif proxyID in (const.PROXY_KEY_TOP_SKY_WING_CHALLENGE, const.PROXY_KEY_TOP_GUILD_SKY_WING_CHALLENGE):
        gameglobal.rds.ui.baiDiShiLian.onProxyDataSend(proxyID, data)
    elif proxyID == const.PROXY_KEY_TOP_SKY_WING_ROB_TEMP:
        gameglobal.rds.ui.ransack.onReceiveRankData(data)
    elif proxyID == const.PROXY_KEY_MARRIAGE_OFFLINE_EQUIMENT:
        gamelog.debug('@zq PROXY_KEY_MARRIAGE_OFFLINE_EQUIMENT:', data)
        BigWorld.player().syncMarriageIntimacyTgtEquipment(data)
    elif proxyID == const.PROXY_KEY_WING_WORLD_INIT:
        BigWorld.player().onInitWingWorld(*data)
    elif proxyID in (const.PROXY_KEY_TOP_TOTAL_GONGJI_FAME, const.PROXY_KEY_TOP_TOTAL_POPULARITY_MALE, const.PROXY_KEY_TOP_TOTAL_POPULARITY_FEMALE):
        info = processTopData(data)
        info = info[:100]
        gameglobal.rds.ui.ranking.updateShejiaoData(proxyID, data[0], info)
    elif proxyID == const.PROXY_KEY_TOP_SPRITE_COMBAT_SCORE:
        info = data[1]
        info.sort(key=lambda a: -a[8])
        gameglobal.rds.ui.ranking.updateSpriteData(data[2], data[0], info)
    elif proxyID == const.PROXY_KEY_SPRITE_INFO:
        gameglobal.rds.ui.summonedWarSpriteOther.show(data)
    elif proxyID == const.PROXY_KEY_QUERY_FALLEN_RED_GUARD:
        BigWorld.player().updateFallenRedGuardDamageInfo(*data)
    elif proxyID == const.PROXY_KEY_WING_WORLD_ARMY_QUERY:
        BigWorld.player().onQueryWingWorldArmy(data[0], data[1], data[2], data[3], data[4])
    elif proxyID == const.PROXY_KEY_QUIZZES_ROUND_START_INFO:
        BigWorld.player().onQuizzesRoundStart(data)
    elif proxyID == const.PROXY_KEY_QUIZZES_INFO:
        BigWorld.player().onQueryQuizzesInfo(data)
    elif proxyID == const.PROXY_KEY_WING_WORLD_XINMO_ARENA:
        gamelog.debug('dxk @game arena data:', data)
        gameglobal.rds.ui.wingStageChoose.onGetServerData(data)
    elif proxyID == const.PROXY_KEY_WING_WORLD_XINMO_ARENA_HISTORY:
        gamelog.debug('dxk @game arena history data:', data)
        gameglobal.rds.ui.combatHistory.onGetServerData(data)
    elif proxyID == const.PROXY_KEY_WING_WORLD_XINMO_ARENA_ROUND_MATCH:
        gamelog.debug('dxk @game match info', data)
        gameglobal.rds.ui.zhiQiangDuiJue.onGetDuiJueServerData(data)
    elif proxyID == const.PROXY_KEY_WING_WORLD_XINMO_UNIQUE_BOSS:
        gamelog.debug('dxk @game unique boss info', data)
        gameglobal.rds.ui.zhiQiangDuiJue.onGetBossServerData(data)
    elif proxyID == const.PROXY_KEY_TOP_WING_WORLD_XINMO_FB:
        gamelog.debug('dxk @game common boss info', data)
        gameglobal.rds.ui.teamRankingList.onGetServerData(data)
    elif proxyID == const.PROXY_KEY_ANNAL_CHAT_DATA:
        BigWorld.player().onGetAnnalChatData(data)
    elif proxyID == const.PROXY_KEY_CHAR_TEMP_DATA:
        gameglobal.rds.ui.balanceArenaPreview.onGetServerData(data)
    elif proxyID == const.PROXY_KEY_CHAR_TEMP_SPRITE_INFO:
        gameglobal.rds.ui.summonedWarSpriteOther.hide()
        if data.has_key('tempId'):
            data.pop('tempId')
        gameglobal.rds.ui.summonedWarSpriteOther.show(data)
    elif proxyID == const.PROXY_KEY_PERSONAL_CHAR_TEMP_INFO:
        gameglobal.rds.ui.balanceArenaTemplate.onGetServerData(data)
    elif proxyID == const.PROXY_KEY_CHAR_TEMP_SKILL_INFO:
        BigWorld.player().onGetSkillData(data)
    elif proxyID == const.PROXY_KEY_CHAR_TEMP_BASIC_INFO:
        gameglobal.rds.ui.balanceArenaPreview.onGetServerData(data)
    elif proxyID == const.PROXY_KEY_CHAR_TEMP_CARD_INFO:
        BigWorld.player().initCardBag(data)
        tempId = data.get('tempId', 0)
        if tempId:
            gameglobal.rds.ui.cardSlot.showTemplate(tempId)
    elif proxyID == const.PROXY_KEY_CHAR_TEMP_EQUIPMENT_INFO:
        parsePlayerArrayData(data)
        if data:
            BigWorld.player().batchInsertEquip(data)
    elif proxyID == const.PROXY_KEY_CBG_INFO:
        gameglobal.rds.ui.cbgMain.onUpdateCbgOnSaleRoleData(data)
    elif proxyID == const.PROXY_KEY_PERSONAL_CHAR_TEMP_HEAT_RANK:
        gameglobal.rds.ui.balanceArenaTemplate.onGetTotalRankData(data)
    elif proxyID == const.PROXY_KEY_SCHOOL_TOP_CANDIDATES:
        BigWorld.player().onQueryCandidates(data)
    elif proxyID == const.PROXY_KEY_NEW_SERVER_ACTIVITY_SELF_LOTTERY:
        gameglobal.rds.ui.newServiceLotterySelf.onGetNewServiceLotteryData(data)
    elif proxyID == const.PROXY_KEY_CLANWAR_GUILD_RECORD:
        BigWorld.player().crossClanWarHistory = data
        gameglobal.rds.ui.crossClanWarHistory.refreshInfo()
    elif proxyID == const.PROXY_KEY_ARENA_PLAYOFFS_TEAM_VOTE_DATA:
        gameglobal.rds.ui.pvpPlayoffs5v5Vote.onGetVoteData(data)
    elif proxyID == const.PROXY_KEY_GUILD_BOSS_ELITE_DATA:
        gameglobal.rds.ui.guildMembersFbSort.show(data)
    elif proxyID == const.PROXY_KEY_TOP_CLAN_WAR_RECORD_SCORE:
        BigWorld.player().crossClanWarRecordRank = data
        gameglobal.rds.ui.crossClanWarRank.refreshClanWarGuildRank()
        gameglobal.rds.ui.clanWar.setClanWarGuildRank([])
    elif proxyID == const.PROXY_KEY_TEAM_ENDLESS:
        from teamEndlessInfo import instance as TeamEndlessInstance
        BigWorld.player().teamEndless = TeamEndlessInstance.createObjFromDict(data)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_TEAMENDLESS_CHANGED)
    elif proxyID == const.PROXY_KEY_MISS_TIANYU_GROUP:
        gameglobal.rds.ui.dispatchEvent(events.EVENT_MISS_TIANYU_GROUP_PRELIMINARY_DATA, data)
    elif proxyID == const.PROXY_KEY_MISS_TIANYU_PLAYOFF:
        gameglobal.rds.ui.dispatchEvent(events.EVENT_MISS_TIANYU_GROUP_FINALS_DATA, data)
    elif proxyID == const.PROXY_KEY_ARENA_AID_TEAM_RANK:
        gameglobal.rds.ui.arenaPlayoffsSupport.onGetServerTeamData(data)
    elif proxyID == const.PROXY_KEY_ARENA_AID_PLAYER_TOP_RANK:
        gameglobal.rds.ui.arenaPlayoffsSupport.onGetServerRankData(data)
    elif proxyID == const.PROXY_KEY_BATTLE_FIELD_RESULT:
        BigWorld.player().showFinalStaticDetail(data)
    elif proxyID == const.PROXY_KEY_ASSASSINATION:
        gameglobal.rds.ui.assassinationMain.refreshInfo(data)
    elif proxyID == const.PROXY_KEY_ASSASSINATION_TOMB:
        gameglobal.rds.ui.assassinationTombstone.refreshAll(data)
    elif proxyID == const.PROXY_KEY_BET_STUB:
        BigWorld.player().onGetBetInfo(data)


def processTopData(data):
    info = data[1]
    info.sort(key=lambda k: k[3])
    info.reverse()
    return info


def processTopDataWithTimestamp(data):
    info = data[1]
    info.sort(cmp=lambda x, y: (cmp(y[3], x[3]) if x[3] != y[3] else cmp(x[-1], y[-1])))
    return info


def runHotfix(s, smd5):
    if gameglobal.gHotfixMD5 == smd5:
        gamelog.debug('jorsef runHotfix no need')
        return
    import BigWorld
    BigWorld.player().exception.clear()
    import __main__
    code = compile(s, 'hotfix', 'exec')
    try:
        lock = cacheBDB.lock_get()
        exec code in __main__.__dict__
        gameglobal.gHotfixMD5 = smd5
    finally:
        cacheBDB.lock_put(lock)


def clearAll(showLoginWin = True, isCrossServer = False, needClearCharacterList = True):
    global GMAE_IS_START
    gamelog.debug('game clearAll')
    GMAE_IS_START = False
    filters = []
    if hasattr(BigWorld, 'setEnableGatherInputCacheNew'):
        BigWorld.setEnableGatherInputCacheNew(False)
    gameglobal.resetConfigData()
    if needClearCharacterList:
        gameglobal.rds.loginManager.characterList.clearAll()
    gameglobal.rds.loginScene.gotoCreateStage()
    gameglobal.rds.loginScene.clearPlayer()
    if gameglobal.rds.loginScene.effectManager:
        gameglobal.rds.loginScene.effectManager.removeAllEffect()
    gameglobal.rds.ui.characterCreate.reset()
    gameglobal.rds.ui.characterDetailAdjust.reset()
    gameglobal.rds.ui.arena.reset()
    gameglobal.rds.ui.team.reset()
    gameglobal.rds.ui.fuben.reset()
    gameglobal.rds.ui.teamComm.reset()
    gameglobal.rds.ui.teamEnemyArena.reset()
    gameglobal.rds.ui.arena.reset()
    gameglobal.rds.ui.target.reset()
    gameglobal.rds.ui.pressKeyF.reset()
    gameglobal.rds.ui.inventory.reset()
    gameglobal.rds.ui.actionbar.reset()
    gameglobal.rds.ui.littleMap.reset()
    gameglobal.rds.ui.trade.reset()
    gameglobal.rds.ui.assign.reset()
    gameglobal.rds.ui.ranking.clearAllData()
    gameglobal.rds.ui.guibaoge.clearData()
    gameglobal.rds.ui.fubenLogin.reset()
    gameglobal.rds.ui.guildPuzzle.hide()
    if isCrossServer:
        filters.append(uiConst.WIDGET_CHAT_LOG)
        gameglobal.rds.ui.friend.saveTeampMsg()
    else:
        gameglobal.rds.ui.chat.reset()
        gameglobal.rds.ui.friend.clearTempMsg()
    gameglobal.rds.ui.systemSettingV2.reset()
    gameglobal.rds.ui.pushMessage.reset()
    gameglobal.rds.ui.skillPush.reset()
    gameglobal.rds.ui.gmChat.reset()
    gameglobal.rds.ui.map.realClose(False)
    gameglobal.rds.ui.expbar.hide()
    gameglobal.rds.ui.player.hide()
    gameglobal.rds.ui.fubenStat.reset()
    gameglobal.rds.ui.fubenGuide.reset()
    gameglobal.rds.ui.battleField.reset()
    gameglobal.rds.ui.shengSiChang.hide()
    gameglobal.rds.ui.battleField.resetBattleFieldData()
    gameglobal.rds.ui.feedback.reset()
    gameglobal.rds.ui.yingXiaoFeedback.reset()
    gameglobal.rds.ui.emote.reset()
    gameglobal.rds.ui.tianyuMall.clearAll()
    gameglobal.rds.ui.cbgMain.reset()
    gameglobal.rds.ui.lifeSkillNew.reset()
    gameglobal.rds.ui.friend.reset()
    gameglobal.rds.ui.fuben.closeFubenQueue()
    gameglobal.rds.ui.wmdRankList.clearData()
    gameglobal.rds.ui.ycwzRankList.clearData()
    gameglobal.rds.ui.playRecomm.clearAll()
    gameglobal.rds.ui.rolecard.clearAll()
    gameglobal.rds.ui.autoQuest.hide()
    gameglobal.rds.ui.arenaRankList.clearData()
    gameglobal.rds.ui.questLog.resetData()
    gameglobal.rds.ui.chargeReward.clearAll()
    gameglobal.rds.ui.easyPay.clearAll()
    gameglobal.rds.ui.migrateServer.clearData()
    gameglobal.rds.ui.friendFlowBack.clearData()
    gameglobal.rds.ui.pvpEnhance.clearAll()
    gameglobal.rds.ui.fubenAwardTimes.clearData()
    gameglobal.rds.ui.guideGoal.clearData()
    gameglobal.rds.ui.newbieGuide.clearAll()
    gameglobal.rds.ui.guildRobberActivityPush.clearAll()
    gameglobal.rds.ui.rewardGiftActivityIcons.clearAll()
    gameglobal.rds.ui.zmjBigBossPanel.clearData()
    gameglobal.rds.ui.welfare.clearAll()
    gameglobal.rds.ui.activitySale.clearAll()
    gameglobal.rds.ui.arenaPlayoffsBet.clearAll()
    gameglobal.rds.ui.schoolTransferSelect.clearAll()
    gameglobal.rds.ui.schoolTransferCondition.clearAll()
    gameglobal.rds.ui.equipChange.clearAll()
    gameglobal.rds.ui.offlineIncome.clearAll()
    gameglobal.rds.ui.tabAuctionCrossServer.clearPushData()
    gameglobal.rds.ui.recommendSearchFriend.clearAll()
    gameglobal.rds.ui.mentorEx.clearAll()
    gameglobal.rds.ui.findBeastRecover.clearAll()
    gameglobal.rds.ui.celebrityRank.clearAll()
    gameglobal.rds.ui.guildAuction.clearAll()
    gameglobal.rds.ui.guildRedPacketHistory.clearAll()
    gameglobal.rds.ui.summonedWarSprite.clearAll()
    gameglobal.rds.ui.wingWorldRemoveSeal.clearAll()
    gameglobal.rds.ui.questionnaire.clearAll()
    gameglobal.rds.ui.summonedWarSpriteExplore.clearAll()
    gameglobal.rds.ui.historyConsumed.clearAll()
    gameglobal.rds.ui.wingCombatPush.clearAll()
    gameglobal.rds.ui.wardrobe.clearAll()
    gameglobal.rds.ui.groupChat.clearAll()
    if hasattr(gameglobal.rds.ui, 'callbackHandler') and gameglobal.rds.ui.callbackHandler:
        BigWorld.cancelCallback(gameglobal.rds.ui.callbackHandler)
    filterWidget = []
    if hasattr(gameglobal.rds, 'transServerInfo') and gameglobal.rds.transServerInfo:
        filterWidget.append(uiConst.WIDGET_LOADING)
        if gameglobal.rds.ui.arenaWait.isShow:
            filterWidget.append(uiConst.WIDGET_ARENA_WAIT_BG)
            filterWidget.append(uiConst.WIDGET_ARENA_WAIT_LEFT)
            filterWidget.append(uiConst.WIDGET_ARENA_WAIT_RIGHT)
    gameglobal.rds.ui.unLoadAllWidget(filterWidget, includeLoading=True)
    gameglobal.rds.ui.roleInfo.titleNewTime = 0
    if showLoginWin:
        gameglobal.rds.loginManager.onDisconnect()
        if not gameglobal.rds.loginManager.isGtLogonMode():
            BigWorld.callback(1, gameglobal.rds.ui.loginSelectServer.onClickBack)
        if hasattr(gameglobal.rds, 'cipherOfPerson'):
            del gameglobal.rds.cipherOfPerson
        if hasattr(gameglobal.rds, 'crossGuild'):
            del gameglobal.rds.crossGuild
    if gameglobal.rds.ui.quest.isShow:
        gameglobal.rds.ui.quest.close()
    if gameglobal.rds.ui.npcV2.isShow:
        gameglobal.rds.ui.npcV2.leaveStage()
    if gameglobal.rds.loginScene.spaceID == None:
        BigWorld.callback(0, gameglobal.rds.loginScene.loadSpace)
    ui.reset_cursor()
    CC.TC = None
    BigWorld.enableU3DOF(False)
    gameglobal.rds.loginScene.cc = None
    stateSafe.stopCheck()
    gameglobal.isModalDlgShow = False
    gameglobal.rds.uiLog.clear()
    screenEffect.ins.clear()
    gameglobal.rds.ui.hideAimCross(True, True)
    gameglobal.rds.ui.hideAimCross(True, False)
    gameglobal.rds.ui.hideAimCross(False)
    gameglobal.rds.ui.storage.clearPassWordHint()
    gameglobal.rds.ui.consign.clearData()
    if getattr(gameglobal.rds, 'ccBox', None) and not isCrossServer:
        gameglobal.rds.ccBox.closeCCBox()
    gameglobal.rds.ui.zhanQi.morpherFactory.reset()
    gameglobal.rds.ui.fullscreenFittingRoom.mediator = None
    gameglobal.rds.ui.setUIHitEnabled(True, True)
    gameglobal.rds.ui.monsterClanWarActivity.clearData()
    gameglobal.rds.ui.expBonus.clearData()
    gameglobal.rds.ui.activityPush.reset()
    loadingProgress.instance().clearLoadingData()
    keyboardEffect.clearAllEffect()
    groupDetailFactory.getActAvlInstance().reset()
    gameglobal.rds.ui.friend.clearRecent()
    gameglobal.rds.ui.activitySaleLoopCharge.clearAll()
    gameglobal.rds.ui.baiDiShiLian.clearAll()
    gameglobal.rds.ui.ransack.clearAll()
    gameglobal.rds.ui.killFallenRedGuardReward.clearAll()
    gameglobal.rds.ui.achvment.clearAll()
    gameglobal.rds.ui.achvmentDiff.clearAll()
    gameglobal.rds.ui.cardSystem.clearAll()
    gameglobal.rds.ui.achvmentOverview.clearAll()
    gameglobal.rds.ui.wingWorldPush.clearAll()
    gameglobal.rds.ui.schoolTopPush.clearAll()
    gameglobal.rds.ui.wingWorldResult.clearAll()
    gameglobal.rds.ui.newServiceFubenRace.clearAll()
    if hasattr(BigWorld, 'ignoreSpaceId'):
        BigWorld.ignoreSpaceId(False)
    gameglobal.rds.ui.activityGuide.clearAll()
    gameAntiCheatingManager.getInstance().clearAll()


__ISPRINT_RE = re.compile('[a-zA-z0-9\\-\\.\\:]+')

def isprint(s):
    global __ISPRINT_RE
    m = __ISPRINT_RE.match(s)
    if m == None:
        return ''
    else:
        return m.group(0)


def initClientInfo():
    gameglobal.rds.clientInfo = ClientInfo({})
    gameglobal.rds.clientInfo.os_info = BigWorld.OSDesc().strip()
    gameglobal.rds.clientInfo.cpu_info = BigWorld.CPUDesc().strip()
    gameglobal.rds.clientInfo.cpu_num = BigWorld.CPUCores()
    gameglobal.rds.clientInfo.cpu_hz = BigWorld.CPUFrequency(0)
    gameglobal.rds.clientInfo.ram = BigWorld.PhysicsMemoryTotal()
    gameglobal.rds.clientInfo.wow64 = hasattr(BigWorld, 'isWow64') and BigWorld.isWow64()
    gameglobal.rds.clientInfo.exe64 = hasattr(BigWorld, 'isExe64') and BigWorld.isExe64()
    gameglobal.rds.clientInfo.netdelay = BigWorld.LatencyInfo().value[3]
    ckeyStr = AppSettings.get(keys.SET_GAME_CEKY, '')
    if not ckeyStr:
        ckeyStr = uuid.uuid1().hex
        AppSettings[keys.SET_GAME_CEKY] = ckeyStr
        AppSettings.save()
    gameglobal.rds.clientInfo.ckey = ckeyStr
    gameglobal.rds.clientInfo.cpu_serial = BigWorld.CPUSerial()
    cType = AppSettings.get(keys.SET_GAME_CTYPE, 0)
    gameglobal.rds.clientInfo.ctype = cType
    if not gameglobal.rds.clientInfo.wow64 or gameglobal.rds.clientInfo.ram < gameglobal.MEMORY_SIZE:
        gameglobal.MEMORY_LIMIT_FLAG = True
    mac_string = gameStrings.TEXT_GAME_1747
    macs = BigWorld.get_mac_addr()
    if macs:
        for _, mac in macs:
            if mac and mac != '00:00:00:00:00:00':
                mac_string = mac
                break

    gameglobal.rds.clientInfo.mac_info = mac_string.strip()
    gpu_info = BigWorld.VideoCardDesc()
    if gpu_info:
        gameglobal.rds.clientInfo.gpu_info = gpu_info[0].strip()
    gameglobal.rds.clientInfo.gpu_ram = BigWorld.VideoLocalMemoryTotal()
    hd = ''
    serial, model = BigWorld.get_machine_serial()
    serial = serial.strip().replace(' ', '-')
    model = model.strip().replace(' ', '-')
    hd = serial + model
    hd = isprint(hd).strip()
    if not hd:
        serials = BigWorld.get_wmi_prop('cimv2', 'PhysicalMedia', 'SerialNumber')
        if serials:
            for serial in serials:
                hd += serial.strip().replace(' ', '-')

            hd = isprint(hd).strip()
        else:
            hd = gameStrings.TEXT_GAME_1747
    gameglobal.rds.clientInfo.harddisk = hd
    gameglobal.rds.clientInfo.cengine = BigWorld.getCompileTimeString() if hasattr(BigWorld, 'getCompileTimeString') else ''


lastScene = ''
lastSpaceID = 0

def teleport(scn, pos):
    global lastScene
    global lastSpaceID
    if scn == lastScene:
        BigWorld.player().physics.teleport(pos, (1, 0, 0))
        return
    spaceID = BigWorld.createSpace()
    addSpaceGeo(spaceID, scn, True)
    BigWorld.player().physics.teleportSpace(spaceID)
    BigWorld.player().physics.teleport(pos, (1, 0, 0))
    lastScene = scn
    lastSpaceID = spaceID


def addSpaceGeo(spaceID, name, delOld = False):
    if gameglobal.rds.clientSpaceMapping != None and gameglobal.rds.clientSpace != None and delOld:
        BigWorld.delSpaceGeometryMapping(gameglobal.rds.clientSpace, gameglobal.rds.clientSpaceMapping)
        BigWorld.clearSpace(gameglobal.rds.clientSpace)
        BigWorld.releaseSpace(gameglobal.rds.clientSpace)
    if spaceID != None:
        gameglobal.rds.clientSpaceMapping = BigWorld.addSpaceGeometryMapping(spaceID, None, 'universes/eg/' + name)
    else:
        gameglobal.rds.clientSpaceMapping = None
    gameglobal.rds.clientSpace = spaceID


def reloadData(data):
    if utils.enableBDB:
        oldVal = cacheBDB._ignoreBDBCache
        cacheBDB._ignoreBDBCache = True
        reload(data)
        cacheBDB._ignoreBDBCache = oldVal
    else:
        reload(data)


def reloadAllData():
    for name, v in sys.modules.iteritems():
        if not name.startswith(('data.', 'cdata.')):
            continue
        if not v or not hasattr(v, '__file__'):
            continue
        f = v.__file__.rsplit('.', 1)[0].replace('/', os.path.sep)
        n = name.replace('.', os.path.sep)
        if name.startswith('data.') and not f.endswith(os.path.join('entities', 'client', n)):
            continue
        if name.startswith('cdata.') and not f.endswith(os.path.join('entities', 'common', n)):
            continue
        if utils.enableBDB:
            _, dataTime = cacheBDB.get_version(name.split('.')[1])
            reloadData(v)
            _, newDataTime = cacheBDB.get_version(name.split('.')[1])
            if newDataTime > dataTime:
                print 'reload data success: ', name
        else:
            reloadData(v)


def playTitleCg(keySeting, cgName, callback):
    global cgMovie
    BigWorld.worldDrawEnabled(False)
    if cgName == 'logo':
        BigWorld.callback(10.0, logoCgTimeOut)
    cgMovie = cgPlayer.CGPlayer()
    config = {'position': (0, 0, 0),
     'w': 2,
     'h': 2,
     'loop': False,
     'callback': callback}
    cgMovie.playMovie(cgName, config)
    Sound.enableMusic(False)
    if keySeting:
        AppSettings[keySeting] = 1
        AppSettings.save()


def playBinkTitleCg(keySeting, cgName, callback = None):
    global cgMovie
    BigWorld.worldDrawEnabled(False)
    if cgName == 'logo':
        BigWorld.callback(10.0, logoCgTimeOut)
    cgMovie = cgPlayer.CGBinkPlayer()
    config = {'position': (0, 0, 0),
     'w': 2,
     'h': 2,
     'loop': False,
     'callback': callback}
    cgMovie.playMovie(cgName, config)
    Sound.enableMusic(False)
    if keySeting:
        AppSettings[keySeting] = 1
        AppSettings.save()


def playBinkCg(cgName, callback = None):
    global cgMovie
    BigWorld.worldDrawEnabled(False)
    if not cgMovie:
        cgMovie = cgPlayer.CGBinkPlayer()
        config = {'position': (0, 0, 0),
         'w': 2,
         'h': 2,
         'loop': True,
         'callback': callback,
         'inBackOfUI': 1}
        cgMovie.playMovie(cgName, config)
        gameglobal.rds.ui.loginWinBottom.playLoginMusic()


def endLogoCg(enableMusic = False):
    endTitleCg(enableMusic)
    if gameglobal.rds.enableBinkLogoCG:
        BigWorld.worldDrawEnabled(False)
        BigWorld.callback(0.0, Functor(playBinkCg, 'login'))


def endTitleCg(enableMusic = True):
    global cgMovie
    C_ui.enableUI(True)
    if enableMusic:
        Sound.enableMusic(True)
    if cgMovie:
        cgMovie.endMovie()
        cgMovie = None
    if gameglobal.rds.loginScene.spaceID == None:
        gameglobal.rds.loginScene.loadSpace()


def logoCgTimeOut():
    BigWorld.worldDrawEnabled(True)
    if cgMovie and cgMovie.cgName == 'logo':
        endLogoCg(True)


def setCameraToNPC(npcId, dis = 2.5, fov = 0.5, h = 1.57):
    e = BigWorld.entities.get(npcId)
    height = h
    import math
    yaw = e.yaw
    dir = (math.sin(yaw), 0, math.cos(yaw))
    dir = Math.Vector3(dir)
    gamelog.debug('bgf:camera', dir)
    pos = e.model.position + Math.Vector3(dir[0] * dis, height, dir[2] * dis)
    dir *= -1
    gamelog.debug('bgf:camera1', dir)
    m = Math.Matrix()
    gamelog.debug('bgf:camera', e.position, height, dir, pos)
    m.lookAt(pos, dir, (0, 1, 0))
    pro = BigWorld.projection()
    pro.fov = fov
    ca = BigWorld.TrackCamera()
    ca.set(m)
    BigWorld.camera(ca)


def _preloadMiscEffect():
    try:
        import Pixie
        for effectId in gameglobal.BASE_EFFECT:
            realFxId, fxPath = sfx._getRealFxInfo(effectId)
            for i in xrange(0, gameglobal.TASKINDICATOR_CNT):
                fx = clientUtils.pixieFetch(fxPath, gameglobal.EFFECT_HIGH)
                if gameglobal.TASKINDICATOR_CACHE.has_key(effectId):
                    if len(gameglobal.TASKINDICATOR_CACHE[effectId]) <= gameglobal.TASKINDICATOR_CNT:
                        gameglobal.TASKINDICATOR_CACHE[effectId].append(fx)
                else:
                    gameglobal.TASKINDICATOR_CACHE[effectId] = [fx]

    except:
        pass


def enableCiKe():
    gameglobal.rds.ui.characterDetailAdjust.openCreateCiKe()


def sendLoadingProcessInfo():
    if gameglobal.rds.loginType == gameglobal.GAME_LOGIN_TYPE_FEIHUO:
        gameglobal.rds.logLoginState = gameglobal.GAME_FEIHUO_LOADING
    elif gameglobal.rds.loginType == gameglobal.GAME_LOGIN_TYPE_YIYOU:
        gameglobal.rds.logLoginState = gameglobal.GAME_YIYOU_LOADING
    elif gameglobal.rds.loginType == gameglobal.GAME_LOGIN_TYPE_SHUNWANG:
        gameglobal.rds.logLoginState = gameglobal.GAME_SHUNWANG_LOADING
    else:
        gameglobal.rds.logLoginState = gameglobal.GAME_LOADING
    netWork.sendInfoForLianYun(gameglobal.rds.logLoginState)


def enableLog(enable):
    if enable:
        gamelog.LOG_LEVEL = gamelog.DEBUG
    else:
        gamelog.LOG_LEVEL = 1000


def teleportEx(spaceID, scn, pos, dir = (1, 0, 0)):
    global lastScene
    global lastSpaceID
    if spaceID == lastSpaceID:
        BigWorld.player().physics.teleport(pos, dir)
        return
    spaceID = BigWorld.createSpaceEx(spaceID)
    addSpaceGeo(spaceID, scn, True)
    BigWorld.player().physics.teleportSpace(spaceID)
    BigWorld.player().physics.teleport(pos, dir)
    lastScene = scn
    lastSpaceID = spaceID


def receiveClipboardDataMsg(filePath):
    if not hasattr(BigWorld, 'enableNotifyclipboardMsg'):
        return
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    loginUserName = 'unknow'
    if hasattr(gameglobal.rds, 'loginUserName'):
        loginUserName = gameglobal.rds.loginUserName
    fileName = str(loginUserName) + '-' + str(now) + '-' + str(gameglobal.rds.macaddrs) + '.bmp'


def parsePlayerLogonData(data):
    if data.has_key('inv'):
        parsePlayer2DArrayData(data['inv'][0])
        parsePlayerArrayData(data['inv'][1])
    if data.has_key('crossInv'):
        parsePlayer2DArrayData(data['crossInv'][0])
        parsePlayerArrayData(data['crossInv'][1])
    if data.has_key('equipment'):
        parsePlayerArrayData(data['equipment'])
    if data.has_key('fashionBag'):
        parsePlayer2DArrayData(data['fashionBag'][1])
        parsePlayerArrayData(data['fashionBag'][2])
    if data.has_key('materialBag'):
        parsePlayer2DArrayData(data['materialBag'][1])
        parsePlayerArrayData(data['materialBag'][2])
    if data.has_key('spriteMaterialBag'):
        parsePlayer2DArrayData(data['spriteMaterialBag'][1])
        parsePlayerArrayData(data['spriteMaterialBag'][2])
    if data.has_key('cart'):
        parsePlayer2DArrayData(data['cart'])
    if data.has_key('tempBag'):
        parsePlayer2DArrayData(data['tempBag'])
    if data.has_key('storage'):
        parsePlayer2DArrayData(data['storage'][0])
        parsePlayerArrayData(data['storage'][1])
    if data.has_key('fishingEquip'):
        parsePlayerArrayData(data['fishingEquip'])
    if data.has_key('questBag'):
        parsePlayer2DArrayData(data['questBag'])
    if data.has_key('exploreEquip'):
        parsePlayerArrayData(data['exploreEquip'])
    if data.has_key('lifeEquipment'):
        parsePlayerArrayData(data['lifeEquipment'])
    if data.has_key('mallBag'):
        parsePlayer2DArrayData(data['mallBag'])
    if data.has_key('rideWingBag'):
        parsePlayer2DArrayData(data['rideWingBag'][0])
    if data.has_key('zaijuBag'):
        parsePlayer2DArrayData(data['zaijuBag'])
    if data.has_key('subEquipment'):
        parsePlayer2DArrayData(data['subEquipment'])
    if data.has_key('wardrobeBag'):
        parsePlayerArrayData(data['wardrobeBag'])
    if data.has_key('hierogramBag'):
        parsePlayer2DArrayData(data['hierogramBag'][1])
        parsePlayerArrayData(data['hierogramBag'][2])


def parsePlayerArrayData(d):
    if isinstance(d, list):
        for i, _v in enumerate(d):
            if _v and isinstance(_v, dict) and _v.get('minutia'):
                it = utils.doCreateItemObjFromDict(_v, doConsistant=True)
                d[i] = copy.deepcopy(it.__dict__)

    elif isinstance(d, dict):
        for k, _v in d.items():
            if _v and isinstance(_v, dict) and _v.get('minutia'):
                it = utils.doCreateItemObjFromDict(_v, doConsistant=True)
                d[k] = copy.deepcopy(it.__dict__)


def parsePlayer2DArrayData(d):
    for i, _vi in enumerate(d):
        if _vi is None:
            continue
        for j, _vj in enumerate(_vi):
            if _vj and isinstance(_vj, dict) and _vj.get('minutia'):
                it = utils.doCreateItemObjFromDict(_vj, doConsistant=True)
                d[i][j] = copy.deepcopy(it.__dict__)


def reloadSwf(uid):
    path = gameglobal.rds.ui.getWidgetPath(uid)
    if not path:
        gamelog.info('bgf@reloadSwf not valid uid %d' % uid)
        return
    path = 'gui/' + path
    ResMgr.purge(path)
    gameglobal.rds.ui.unLoadWidget(uid)
    BigWorld.setMovieDefModified(path)


def reloadSwfByPath(path):
    path = 'gui/' + path
    ResMgr.purge(path)
    BigWorld.setMovieDefModified(path)


class GfxValueCallData(object):

    def __init__(self):
        self.map = {}
        self.reportCallback = None
        self.isReprot = False

    def addLog(self, frame, funcName, count, digest, stack):
        self.map[digest] = (frame,
         funcName,
         count,
         stack)

    def startReport(self):
        if self.isReprot:
            return
        self.isReprot = True
        self._report()

    def _report(self):
        if not self.map:
            self.isReprot = False
            return
        else:
            p = BigWorld.player()
            if not p:
                return
            if self.reportCallback:
                BigWorld.cancelCallback(self.reportCallback)
                self.reportCallback = None
            msg = gameStrings.TEXT_GAME_2123
            for digest in self.map.keys():
                info = self.map.pop(digest, None)
                if info:
                    frame, funcName, count, stack = info
                    msg += 'frame: %d gfxValueCall: %s %d\n' % (frame, funcName[:300], count)
                    p.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, [msg, stack], 0, {'digest': digest})
                break

            self.reportCallback = BigWorld.callback(1.5, self._report)
            return


gfxValueCall = GfxValueCallData()

def reportGfxValueCall(*args):
    if gameglobal.rds.GameState == gametypes.GS_PLAYGAME:
        funcName, count, frame = args
        whiteNameList = ('getInstByClsName',)
        for whiteName in whiteNameList:
            if funcName.find(whiteName) != -1:
                return

        md5 = hashlib.md5()
        md5.update(funcName)
        hexdigest = md5.hexdigest()
        stack = traceback.format_stack()
        if len(stack) >= 3:
            stack = stack[-3]
        else:
            stack = ''
        gfxValueCall.addLog(frame, funcName, count, hexdigest, stack)
        gfxValueCall.startReport()
