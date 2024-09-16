#Embedded file name: /WORKSPACE/data/entities/client/helpers/statesafe.o
import time
import random
import math
import hashlib
import BigWorld
import Math
import C_ui
import utils
import appSetting
import clientcom
import traceback
import gametypes
import gameglobal
import formula
import keys
import const
import gamelog
from sfx import sfx
from helpers import cellCmd
from helpers import impJumpFashion
from helpers import seqTask
from helpers import tintalt
from helpers import editorHelper
from helpers import loadingProgress
from callbackHelper import Functor
from helpers import protect
from guis import uiUtils
from guis import uiConst
from guis import cursor
from data import sys_config_data as SCD
from data import map_config_data as MCD
from data import qinggong_cost_data as QCD
from cdata import game_msg_def_data as GMDD
from data import chunk_mapping_data as CMD
from data import physics_config_data as PCD
from data import battle_field_mode_data as BFMD
from data import game_msg_data as GMD
from data import tutorial_config_data as TCD
gChecking = False
gCheckInterval = 5
gBattleFieldCnt = 0
gCurFame = 0
gFrameCnt = 0
gLoadedCnt = 0
frameLimit = 15
frameLoadedTotalCnt = 10
IDLE_TIMEOUT = 120
IDLE_SYNC_INTERVAL = 60
G_MAX_Y = 400
LATENCY_CNT = 0
LATENCY_TOTAL = 0.0
FUNC_INTERVAL_MAP = {}

def checkInterval(times):

    def _checkInterval(func):
        funcName = func.func_code.co_name

        def _func(*args):
            if FUNC_INTERVAL_MAP.has_key(funcName):
                FUNC_INTERVAL_MAP[funcName] += 1
                if FUNC_INTERVAL_MAP[funcName] >= times:
                    FUNC_INTERVAL_MAP[funcName] = 0
                    func(*args)
            else:
                FUNC_INTERVAL_MAP[funcName] = 0

        return _func

    return _checkInterval


def beginCheck():
    global gChecking
    if gameglobal.rds.isSinglePlayer:
        return
    if not gChecking:
        gamelog.debug('jorsef::beginCheck..........................')
        gChecking = True
        _cycleCheck()


def stopCheck():
    global gChecking
    gChecking = False
    FUNC_INTERVAL_MAP.clear()
    gamelog.debug('jorsef::stopCheck..........................')


def _cycleCheck():
    if gChecking:
        try:
            _stateSafe()
        except:
            traceback.print_exc()

        BigWorld.callback(gCheckInterval, _cycleCheck)


def _stateSafe():
    p = BigWorld.player()
    if not p.isMoving:
        p.isAscending = False
    if p.life == gametypes.LIFE_DEAD and p.touchAirWallProcess != 1:
        p.ap.stopMove()
        if p.fashion:
            p.fashion.breakJump()
        return
    if hasattr(p, 'navigatorRouter'):
        p.navigatorRouter.selfCheck()
    _checkAvatarY()
    _checkQinggongState()
    _checkOnDieMaterial((gametypes.MATERIAL_TYPE_LAVA,))
    if not BigWorld.isPublishedVersion():
        _checkMemorySize()
    p.checkFriendState()
    _bfInCombatCheck()
    _sscInCombatCheck()
    _checkWingTakeOff()
    _checkServerTime()
    _checkVideoQualityLv()
    _checkAvatarModelCnt()
    _checkGravityState()
    _checkAvatarIdleTime()
    _checkAvatarRideTogether()
    _checkAvatarSpeed()
    _checkTintContent()
    _checkCameraDirection()
    _checkEffectCache()
    _checkMarkNpcFKey()
    _checkMultiPeopleState()
    _checkFollowAvatar()
    _checkFlyRide()
    _checkUseAccelerator()
    _checkClientPerformance()
    _checkLatency()
    _checkHostileMode()
    _checkFall()
    _checkFrame()
    _checkAvatarCnt()
    _checkNpcModelCnt()
    _checkOberserFly()
    _checkOutHomeRoom()
    _checkTrapInHomeLoading()
    _checkKejuGuide()
    _checkCursor()
    _checkForbidRideFly()
    _checkLastInput()
    _checkInAutoQuest()
    _checkGroupFollowAutoAttack()
    _checkPerformanceMonitor()
    _reportClientProfile()
    _enableCheckGmFollow()
    _checkDotaAvatarVisible()
    if utils.isInternationalVersion():
        _checkInactivePlayer()
    _checkBelowTerrain()
    _checkDummyKeepEffect()


class checker(object):

    def __init__(self, timeCnt, func):
        self.time = 0
        if timeCnt:
            self.timeCnt = timeCnt
        else:
            self.timeCnt = 1
        self.func = func

    def update(self):
        if self.time == 0:
            self.func() if self.func else None
        self.time = (self.time + 1) % self.timeCnt


def _setFrame(val):
    global gCurFame
    gCurFame = val


homeRoomCallback = None

def _checkOutHomeRoom():
    global homeRoomCallback
    if homeRoomCallback:
        BigWorld.cancelCallback(homeRoomCallback)
        homeRoomCallback = None
    _checkPlayerOutHomeRoom(5)


def _checkPerformanceMonitor():
    if not gameglobal.rds.configData.get('enableClientPerformanceFilter', False):
        return
    if not gameglobal.gIsAppActive:
        return
    p = BigWorld.player()
    if getattr(p, 'monitor', None):
        p.monitor.check()


@checkInterval(3)
def _reportClientProfile():
    perFormanceInfo = BigWorld.getPerformanceInfo()
    if not perFormanceInfo:
        return
    p = BigWorld.player()
    mem = perFormanceInfo.get('commitedmem', 0)
    fps = BigWorld.getFps()
    if not gameglobal.gIsAppActive and fps == gameglobal.BACKGROUND_FPS:
        fps = 0
    p.base.reportClientProfile(fps, int(mem))


def _enableCheckGmFollow():
    if not gameglobal.rds.configData.get('enableCheckGmFollow', True):
        return
    p = BigWorld.player()
    inDota = formula.inDotaBattleField(getattr(p, 'mapID', 0))
    if inDota and not p.modelServer.needFollowStyle() and p.physics.style == 4:
        p.modelServer.updateFollowStyle()


def _checkPlayerOutHomeRoom(cnt):
    global homeRoomCallback
    if cnt == 0:
        return
    if not gChecking:
        return
    player = BigWorld.player()
    if formula.spaceInHome(player.spaceNo):
        if not player.inHomeRoomValidArea(player.position):
            player.homeRoomFangKaDian()
        if player.spaceInHomeOrLargeRoom():
            if player.position.y > editorHelper.getFloorHeightMax() or player.position.y < editorHelper.getFloorHeightMin() - 2:
                player.homeRoomFangKaDian()
    homeRoomCallback = BigWorld.callback(1, Functor(_checkPlayerOutHomeRoom, cnt - 1))


def _checkTrapInHomeLoading():
    player = BigWorld.player()
    if player.spaceInHomeOrLargeRoom() and player.ap.inLoadingProgress:
        ins = loadingProgress.instance()
        if ins.lastPercent <= 0.2 and BigWorld.time() - ins.loadingTime >= 200:
            player.cell.leaveRoom()


def _checkCursor():
    p = BigWorld.player()
    if p.isInBfDota() and getattr(p, 'isInBfDotaChooseHero', False):
        if C_ui.get_cursor_pos()[0] < 0:
            C_ui.cursor_pos(100, 100)


def _checkDotaAvatarVisible():
    p = BigWorld.player()
    enableCheckLog = gameglobal.rds.configData.get('enableDotaAvatarVisibleCheck', False)
    if p.isInBfDota() and gameglobal.rds.configData.get('enableFixDotaModelVisible', False):
        for gbId, mInfo in p.battleFieldTeam.iteritems():
            if gbId != p.gbId:
                entity = BigWorld.entities.get(mInfo['id'], None)
                if entity and entity.getOpacityValue()[0] == gameglobal.OPACITY_FULL and not entity.model.visible:
                    entity.model.visible = True
                    entity.refreshOpacityState()
                    if enableCheckLog:
                        msg = ('jbx:dotaAvatar',
                         gbId,
                         entity.model.sources,
                         entity.inWorld,
                         entity.fashion,
                         entity.id,
                         entity.fashion.owner,
                         entity.fashion and entity.fashion.owner and BigWorld.entities.has_key(entity.fashion.owner),
                         entity.dotaLogList)
                        p.base.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, [str(msg)], 0, '', p.roleName, '')


def _checkKejuGuide():
    player = BigWorld.player()
    if not player.kejuInfo:
        return
    if gameglobal.rds.ui.pushMessage.hasMsgType(uiConst.MESSAGE_TYPE_KEJU_GUIDE) or gameglobal.rds.ui.kejuGuide.mediator:
        return
    gameglobal.rds.ui.kejuGuide.checkKejuState()


def _checkGameLoaded():
    global gCurFame
    global gLoadedCnt
    gCurFame = 0
    pInfo = BigWorld.getPerformanceInfo()
    for key, val in pInfo.iteritems():
        if isinstance(key, str) and key.startswith('fps_'):
            gCurFame += int(val)

    if gameglobal.gIsAppActive:
        if gCurFame / 5 <= frameLimit:
            gLoadedCnt += 1
        else:
            gLoadedCnt = 0
    else:
        gLoadedCnt = 0
    if gLoadedCnt >= frameLoadedTotalCnt:
        gLoadedCnt = 0
        return True
    else:
        return False


def _checkFrame():
    global gFrameCnt
    if BigWorld.player().lv > 40:
        return
    if appSetting.VideoQualitySettingObj.getVideoQualityLv() > 0:
        return
    if appSetting.VideoQualitySettingObj.getMinimalist():
        return
    if gFrameCnt % 2 == 0:
        if _checkGameLoaded():
            gamelog.info('@hjx frame#ok:', time.time(), gFrameCnt)
            gFrameCnt = 0
            gameglobal.rds.tutorial.onGameLoaded()
    gFrameCnt += 1


@checkInterval(60)
def _checkVideoQualityLv():
    qualityLv = int(appSetting.VideoQualitySettingObj.getVideoQualityLv())
    effNumLimit = gameglobal.VIDEO_QUALITY_EFFECT_LV.get(qualityLv, 20)
    nowEffNum = sfx.gEffectMgr.effCounter.sumEffCount + sfx.gEffectMgr.effCounter.sumMiscEffCount
    gamelog.debug('_checkVideoQualityLv', qualityLv, effNumLimit, nowEffNum, clientcom.getEffectPriority())
    if nowEffNum > effNumLimit:
        clientcom.highAllowEffectPriority()
    if nowEffNum <= effNumLimit:
        clientcom.allowLowerPriority()


def _bfInCombatCheck():
    global gBattleFieldCnt
    p = BigWorld.player()
    if not p.lastNotInCombatTime:
        gBattleFieldCnt = 0
        return
    if formula.spaceInWingWarCity(p.spaceNo):
        if p.hasState(const.WING_WORLD_WAR_FREEZE_STATE_ID):
            if gBattleFieldCnt % 2 == 0:
                p.showGameMsg(GMDD.data.WING_WORLD_WAR_STATE_ALERT, ())
            gBattleFieldCnt += 1
            return
    if not p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
        gBattleFieldCnt = 0
        return
    if not p._isBattleFieldReady():
        gBattleFieldCnt = 0
        return
    if p.hasState(const.BATTLE_FIELD_FREEZE_STATE_ID):
        if gBattleFieldCnt % 2 == 0:
            if formula.inHuntBattleField(p.mapID):
                if p.bfSideIndex == const.BATTLE_FIELD_HUNT_PROTECT_SIDE_INDEX:
                    p.showGameMsg(GMDD.data.BATTLE_FIELD_STATE_ALERT_HUNT_PROTECTER, ())
                else:
                    p.showGameMsg(GMDD.data.BATTLE_FIELD_STATE_ALERT_HUNT_SPRITE, ())
            else:
                p.showGameMsg(GMDD.data.BATTLE_FIELD_STATE_ALERT, ())
        gBattleFieldCnt += 1
        return


def _sscInCombatCheck():
    p = BigWorld.player()
    if not p.lastNotInCombatTime:
        return
    if not p.isInSSCorTeamSSC():
        return
    if not p.hasState(const.SHENG_SI_CHANG_TIAN_LEI_STATE_ID):
        return
    deltaOfTime = utils.getNow() - p.lastNotInCombatTime
    gamelog.debug('@hjx tianlei#_inCombatCheck:', p.id, p.lastNotInCombatTime, deltaOfTime)
    if deltaOfTime >= 10 and deltaOfTime < 10 + gCheckInterval:
        p.showGameMsg(GMDD.data.SHENG_SI_CHANG_STATE_ALERT, ())
    elif deltaOfTime >= 30 and deltaOfTime < 30 + gCheckInterval:
        p.showGameMsg(GMDD.data.SHENG_SI_CHANG_STATE_ALERT, ())


gNeedCheckMemory = False

def _checkMemorySize():
    global gNeedCheckMemory
    if not gNeedCheckMemory:
        return
    memorySize = BigWorld.getMemoryInfo()[0]
    if memorySize > gameglobal.MEMORY_LIMIT_SUM:
        gNeedCheckMemory = False
        msg = '%s out of memory' % gameglobal.rds.loginUserName
        BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, [msg], 0, {})
        return


def _checkHostileMode():
    p = BigWorld.player()
    enableGuildEnemy = gameglobal.rds.configData.get('enableGuildEnemy', False)
    if p and p.pkMode == const.PK_MODE_HOSTILE and not enableGuildEnemy:
        p.cell.switchPkMode(const.PK_MODE_KILL, p.cipherOfPerson)


def _checkFall():
    p = BigWorld.player()
    if p.isFalling:
        distance = p.qinggongMgr.getDistanceFromGround()
        if distance and distance < 0.1:
            p.isFalling = False


def _checkForbidRideFly():
    p = BigWorld.player()
    if not p.isForbidRideFly():
        return
    if p.inFly:
        p.cell.leaveWingFly()
    elif p.inRiding():
        p.cell.leaveRide()


def _checkWingTakeOff():
    p = BigWorld.player()
    if hasattr(p, 'wingStateTime') and hasattr(p, 'inWingTakeOff'):
        inFly, startTime = getattr(p, 'wingStateTime', (0, 0))
        if p.inFly and time.time() - startTime > 2:
            if p.inWingTakeOff:
                p.inWingTakeOff = False
                p.fashion.stopAllActions()


def _checkGravityState():
    if gameglobal.rds.GameState <= gametypes.GS_LOADING:
        return
    p = BigWorld.player()
    if p.isLoseGravity():
        if p.canFly() or p.canSwim() or p.canFloatage():
            return
        if p.qinggongState in [gametypes.QINGGONG_STATE_FAST_SLIDING, gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND]:
            return
        if p.qinggongState == gametypes.QINGGONG_STATE_FAST_RUN and p.isInsideWater:
            return
        p.setGravity(gametypes.NOMAL_DOWNGRAVITY)


def _checkAvatarY():
    p = BigWorld.player()
    defaultMaxYLimit = MCD.data.get(p.mapID, {}).get('maxYLimit', G_MAX_Y)
    maxYLimit = CMD.data.get(BigWorld.ChunkInfoAt(p.position), {}).get('yLimit', defaultMaxYLimit) * 1.2
    if p and p.position.y > maxYLimit:
        p.ap.endFlyAccelerate(True)
        cellCmd.endUpQinggongState()
        p.physics.velocity.y = 0
        p.fashion.stopAllActions()
        p.qinggongMgr.stopWingFlyModelAction()
        p.physics.teleport((p.position.x, maxYLimit, p.position.z))


def _checkOnDieMaterial(matrialIds):
    p = BigWorld.player()
    collideRes = BigWorld.collide(p.spaceID, p.position + Math.Vector3(0, 1, 0), p.position + Math.Vector3(0, -0.25, 0))
    if collideRes and collideRes[2] == gametypes.MATERIAL_TYPE_LAVA:
        envHurtInterval = SCD.data.get('envHurtInterval', 1.0)
        if p.envHurtTimerId == 0:
            p.envHurtTimerId = BigWorld.callback(envHurtInterval, p.onEnvHurt)
    elif p.envHurtTimerId != 0:
        BigWorld.cancelCallback(p.envHurtTimerId)
        p.envHurtTimerId = 0
    if collideRes:
        if gametypes.MATERIAL_TYPE_LAVA in matrialIds:
            return True
        if gametypes.MATERIAL_TYPE_DIE in matrialIds and collideRes[2] == gametypes.MATERIAL_TYPE_DIE:
            gamelog.debug('jorsef: CLIENT_DIE........................')
            p.cell.selfInjure(gametypes.CLIENT_HURT_DIE, 1.0, 0)
            return True
    return False


def _checkAvatarIdleTime():
    p = BigWorld.player()
    lastActionTime = max(BigWorld.get_last_input_time() + IDLE_TIMEOUT, p.idleLastCheckTime)
    now = BigWorld.time()
    idleTime = now - lastActionTime
    if idleTime > 0:
        p.isGuaJiState = True
        p.idleTimeCount += idleTime
    else:
        p.isGuaJiState = False
    p.idleLastCheckTime = now
    if now - p.lastSyncTime > IDLE_SYNC_INTERVAL:
        p.cell.syncIdleTime(p.idleTimeCount)
        p.lastSyncTime = now
        p.idleTimeCount = 0


def _checkAvatarRideTogether():
    p = BigWorld.player()
    if not getattr(p, 'isWaitingRideTogether', False) and p.tride.inRide() and not p.tride.isMajor(p.id):
        header = p.tride.getHeader()
        if header:
            dist = (p.position - header.position).length
            if dist > 20:
                p.cancelRideTogether()


def _checkAvatarSpeed():
    if gameglobal.rds.isSinglePlayer:
        return
    BigWorld.player().ap.resetAvatarTopSpeed()


def _checkCameraDirection():
    if not gameglobal.rds.configData.get('enableNewCamera', False):
        if not BigWorld.player().inCombat and hasattr(BigWorld.camera(), 'uprightDirection') and not gameglobal.rds.ui.camera.isShow:
            BigWorld.camera().uprightDirection = (0, 1, 0)
    elif not BigWorld.player().inCombat and hasattr(BigWorld.camera(), 'uprightDirection') and not gameglobal.rds.ui.cameraV2.isShow:
        BigWorld.camera().uprightDirection = (0, 1, 0)


def _checkQinggongState():
    p = BigWorld.player()
    if p.qinggongState == gametypes.QINGGONG_STATE_DEFAULT:
        if not p.canFly():
            dashForwardSpeed = max(PCD.data.get('dashForwardSpeed', 12), p.ap.getDashForwardSpeed(), p.ap.runFwdSpeed) * 1.1
            if p.ap.physics.velocity[2] > dashForwardSpeed:
                p.setGravity(gametypes.NOMAL_DOWNGRAVITY)
                p.ap.needForceEndQingGong = True
                cellCmd.endUpQinggongState()
    elif hasattr(p, 'qingGongTimePair') and p.qingGongTimePair and p.qingGongTimePair[0]:
        lv = p.getQingGongSkillLv(p.qinggongState)
        costData = QCD.data.get((p.qinggongState, lv)).get('nonCombatCost', (0, 0))
        qstype = p.qinggongState
        if qstype in gametypes.HORSE_QINGGONG:
            equipment = p.equipment.get(gametypes.EQU_PART_RIDE)
            if equipment:
                adjustPer = utils.getHorseQinggongAdjust(equipment)
                costData = (int(costData[0] * adjustPer), int(costData[1] * adjustPer))
        if qstype in gametypes.QINGGONG_WINGFLY_STATES:
            if p.inFlyTypeFlyRide():
                equipment = p.equipment.get(gametypes.EQU_PART_RIDE)
            else:
                equipment = p.equipment.get(gametypes.EQU_PART_WINGFLY)
            if equipment:
                adjustPer = utils.getWingQinggongAdjust(equipment)
                costData = (int(costData[0] * adjustPer), int(costData[1] * adjustPer))
        if costData[1] > 0 and costData[1] > p.nonCombatEpRegenFix * 2 and not p.gmMode:
            qinggongState, startTime, oldEp = p.qingGongTimePair
            if time.time() - startTime > 3 and p.ep > oldEp:
                p.setGravity(gametypes.NOMAL_DOWNGRAVITY)
                p.ap.needForceEndQingGong = True
                cellCmd.endUpQinggongState()
    if p.qinggongState == gametypes.QINGGONG_STATE_RUSH_DOWN:
        if p.qinggongMgr.getDistanceFromGround() < 0.5 or not p.physics.jumping and not p.isFalling:
            p.ap.needForceEndQingGong = True
            p.setGravity(gametypes.NOMAL_DOWNGRAVITY)
            cellCmd.endUpQinggongState()
            p.ap.updateVelocity()
    if p.inSwim:
        p.physics.keepJumpVelocity = False
    if p.qinggongState != gametypes.QINGGONG_STATE_DEFAULT:
        return
    if (p.isJumping or p.physics.jumping) and not p.inDanDao:
        actQueue = p.model.queue
        if len(actQueue) == 0:
            return
        for actionName in ['1225',
         '1212',
         '1123',
         '1223',
         '1231']:
            if actionName in actQueue:
                p.jumpActionMgr.jumpPhase = impJumpFashion.JUMP_UP_PHASE
                p.fashion.isStartJump = True
                p.ap.jumpEnd(True)


def _checkServerTime():
    p = BigWorld.player()
    t = p.getServerTime()
    p.base.checkServerTime(t, p.serverBootTime)


@checkInterval(2)
def _checkAvatarModelCnt():
    operation = getattr(BigWorld.player(), 'operation', None)
    showClanWarArmor = False
    if operation:
        showClanWarArmor = operation['commonSetting'][17]
    seqTask.modelMemoryCtrl().avatarModelCnt = getRealAvatarCnt()
    gameglobal.rds.avatarModelCnt = appSetting.VideoQualitySettingObj.getAvatarCntWithVQ()
    if showClanWarArmor:
        gameglobal.rds.avatarModelCnt *= gameglobal.MODEL_IN_WARARMOR_RATE
    refreshRealModelState(showClanWarArmor)


def getInCameraRealModelEntityCnt(ents):
    if not ents:
        return 0
    return len([ e for e in ents if e.__class__.__name__ == 'Avatar' and e.isRealModel ])


def getRealAvatarCnt():
    return len([ e for e in BigWorld.entities.values() if e.__class__.__name__ == 'Avatar' and e.isRealModel ])


def getAvatarCnt():
    return len([ e for e in BigWorld.entities.values() if e.__class__.__name__ == 'Avatar' ])


def refreshRealModelState(showClanWarArmor):
    return
    if gameglobal.rds.GameState < gametypes.GS_PLAYGAME:
        return
    p = BigWorld.player()
    if p.isMoving and not showClanWarArmor or not BigWorld.isWow64():
        return
    ents = BigWorld.inCameraEntity(gameglobal.MODEL_REFRESH_DIST)
    cnt = getInCameraRealModelEntityCnt(ents)
    if seqTask.modelMemoryCtrl().avatarModelCnt >= gameglobal.rds.avatarModelCnt and cnt > gameglobal.INCAMERA_ENTITIES:
        return
    if not ents:
        return
    for en in ents:
        if canReLoadModel(en):
            en.reloadModel()


def canReLoadModel(entity):
    if not entity or not entity.inWorld:
        return False
    if entity.id == BigWorld.player().id:
        return False
    if not entity.IsAvatar:
        return False
    if entity.isRealModel:
        return False
    opValue = entity.getOpacityValue()
    if opValue in [gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE, gameglobal.OPACITY_HIDE_WITHOUT_NAME]:
        return False
    if not getattr(entity.model, 'visible', True):
        return False
    return True


gAccountChecking = False

def startAccountCheck():
    global gAccountChecking
    if gameglobal.rds.isSinglePlayer:
        return
    if not gAccountChecking:
        gamelog.debug('@zs::begin account Check..........................')
        gAccountChecking = True
        _cycleAccountCheck()


def stopAccountCheck():
    global gAccountChecking
    gAccountChecking = False


def _cycleAccountCheck():
    if not gAccountChecking:
        return
    try:
        _checkAccountIdleTime()
    except:
        traceback.print_exc()

    BigWorld.callback(gCheckInterval, _cycleAccountCheck)


def _checkAccountIdleTime():
    p = BigWorld.player()
    if not p:
        stopAccountCheck()
        return
    if p.__class__.__name__ == 'PlayerAccount':
        lastActionTime = BigWorld.get_last_input_time()
        now = BigWorld.time()
        idleTime = now - lastActionTime
        if idleTime > SCD.data.get('accountMaxIdleTime', 60):
            p.base.syncIdleTime(int(idleTime))
    else:
        stopAccountCheck()


@checkInterval(20)
def _checkTintContent():
    tintalt.clear_ta_content_map()


@checkInterval(12)
def _checkEffectCache():
    sfx.gEffectMgr.effectCache.clearEffectCache()


def _checkMultiPeopleState():
    try:
        p = BigWorld.player()
        if p.isInCoupleRide():
            e1 = BigWorld.entities.get(p.coupleEmote[1])
            e2 = BigWorld.entities.get(p.coupleEmote[2])
            if not e1 or not e1.inWorld or not e2 or not e2.inWorld:
                p.cell.cancelCoupleEmote()
            length = (e1.position - e2.position).length
            if e1 != p and length > 30:
                p.cell.cancelCoupleEmote()
        if p.isRidingTogetherAsVice() and not getattr(p, 'isWaitingRideTogether', False):
            header = p.tride.getHeader()
            if not header or not header.inWorld:
                p.cancelRideTogether()
            else:
                length = (p.position - header.position).length
                if length > 20:
                    p.cancelRideTogether()
    except:
        pass


def _checkAvatarCnt():
    p = clientcom.getPlayerAvatar()
    if p is None:
        return
    checkAvatarRadius = TCD.data.get('CHECK_AVATAR_RADIUS', 30)
    if checkAvatarRadius <= 0:
        return
    avatarList = p.entitiesInRange(checkAvatarRadius, 'Avatar')
    if hasattr(gameglobal.rds, 'tutorial'):
        gameglobal.rds.tutorial.onCheckAvatarCnt(len(avatarList))


def _checkOberserFly():
    p = clientcom.getPlayerAvatar()
    if not p.gmMode:
        if p.inFlyTypeObserver():
            p.cell.leaveObserverFly()


def _checkFollowAvatar():
    try:
        pass
    except:
        pass


def _checkFlyRide():
    p = BigWorld.player()
    disFromGround = p.qinggongMgr.getDistanceFromGround()
    disFromWater = p.qinggongMgr.getDistanceFromWater()
    if disFromWater and disFromWater > 5 or not disFromWater and disFromGround > 5:
        if p.inSwim:
            p.cell.leaveSwim()
        if keys.CAPS_SWIM in p.am.matchCaps:
            p.fashion.autoSetStateCaps()


def _checkMarkNpcFKey():
    p = clientcom.getPlayerAvatar()
    if p and gameglobal.rds.ui.pressKeyF.type == const.F_MARKERNPC:
        entIds = list(gameglobal.rds.ui.pressKeyF.markers)
        for entId in entIds:
            ent = BigWorld.entity(entId)
            if not ent or not ent.inWorld:
                gameglobal.rds.ui.pressKeyF.removeMarker(entId)


def _checkNpcModelCnt():
    gameglobal.CURRENT_NPC_MODEL_CNT = clientcom.getShowNpcCnt()


@checkInterval(6)
def _checkUseAccelerator():
    useAccelerator = protect.nepCheckAccelerator()
    if useAccelerator:
        BigWorld.callback(random.randint(1, 10), Functor(clientcom.quitGameByNeprot, gameglobal.EXIT_ACCELERATOR))


@checkInterval(60)
def _checkClientPerformance():
    p = BigWorld.player()
    if random.randint(0, 100) <= 10:
        p.logClientPerFormace()


@checkInterval(10)
def _checkLatency():
    global LATENCY_TOTAL
    global LATENCY_CNT
    latency = BigWorld.LatencyInfo().value[3] * 100.0
    LATENCY_TOTAL += latency
    LATENCY_CNT += 1
    if LATENCY_CNT % 10 == 0:
        p = BigWorld.player()
        p.checkLatency(LATENCY_TOTAL)
        LATENCY_TOTAL = 0.0
        LATENCY_CNT = 0


def _checkInactivePlayer():
    if not gameglobal.rds.configData.get('enableKickInactivePlayer', False):
        return
    p = BigWorld.player()
    lastInputTime = BigWorld.get_last_input_time()
    kickTimeIndex = int(p.thisEnterWorldTime < lastInputTime)
    inActiveTime = BigWorld.time() - max(p.thisEnterWorldTime, lastInputTime)
    inActiveTimeStr = gameglobal.rds.configData.get('kickInactiveTime', '1800,900|600')
    try:
        tmp = inActiveTimeStr.split('|')
        kickTimes = list(tmp[0].split(','))
        msgInterVal = int(tmp[1])
        kickTime = int(kickTimes[kickTimeIndex])
    except:
        kickTimes = (1800, 900)
        msgInterVal = 20
        kickTime = kickTimes[kickTimeIndex]

    if inActiveTime > kickTime:
        p.base.setOfflineType(gametypes.PLAYER_OFFLINE_TYPE_INACTIVE)
        gameglobal.rds.loginManager.disconnectFromGame()
    elif inActiveTime > msgInterVal and inActiveTime % msgInterVal < gCheckInterval:
        passMin = int(inActiveTime / const.TIME_INTERVAL_MINUTE)
        leftMin = int(math.ceil((kickTime - inActiveTime) / const.TIME_INTERVAL_MINUTE))
        p.showGameMsg(GMDD.data.KICK_INACTIVE_PLAYER_MSG, (passMin, leftMin))


@checkInterval(720)
def _checkLastInput():
    p = BigWorld.player()
    if formula.spaceInHome(p.spaceNo):
        lastInputTime = BigWorld.get_last_input_time()
        p.cell.genHomeIdleStateLog(lastInputTime)


def _checkInAutoQuest():
    p = BigWorld.player()
    if not p.checkInAutoQuest():
        return
    if p.inCombat and not p.inMoving() and not p.isPathfinding and p.autoSkill and not p.autoSkill.inSkillMacroTimer():
        if not hasattr(p, 'lastHpChangeAutoQuestTime'):
            p.lastHpChangeAutoQuestTime = 0
        now = utils.getNow()
        if p.lastHpChangeAutoQuestTime + 3 < now:
            p.lastHpChangeAutoQuestTime = now
            p.delayQuestSimpleFindPos()


def _checkGroupFollowAutoAttack():
    BigWorld.player().startGroupFollowAutoAttack()


def _checkBelowTerrain():
    if not gameglobal.rds.configData.get('enableCheckBelowTerrain', True):
        return
    p = clientcom.getPlayerAvatar()
    if not p:
        return
    if p.spaceNo != const.SPACE_NO_BIG_WORLD:
        return
    if gameglobal.rds.GameState != gametypes.GS_PLAYGAME:
        return
    groundSurfaceY = -500
    if hasattr(BigWorld, 'getTerrainHeight'):
        groundSurfaceY = BigWorld.getTerrainHeight(p.position[0], p.position[2])
    if groundSurfaceY > -1000000:
        if p.inWorld and groundSurfaceY - p.position.y > 2:
            posFrom = Math.Vector3(p.position)
            posFrom.y += 1
            posTo = Math.Vector3(p.position)
            posTo.y -= 10000
            res = BigWorld.collide(p.spaceID, posFrom, posTo, gameglobal.GLASSMATTERKINDS)
            if not res:
                msg = 'invalid position (%.2f %.2f %.2f)' % (p.position.x, p.position.y, p.position.z)
                p.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, [msg], 0, {})


def _checkDummyKeepEffect():
    sfx.gEffectMgr.checkDummyEffects()
