#Embedded file name: /WORKSPACE/data/entities/client/sfx/physicseffect.o
import Sound
import BigWorld
import gamelog
import gameconfigCommon
import gameglobal
import gametypes
import const
import screenEffect
import sfx
import utils
from callbackHelper import Functor
from gameclass import Singleton
from data import consumable_item_data as CID
from data import act_appearance_reverse_data as AARD
from data import act_appearance_data as AAD
from data import basic_action_effect_data as BAED
from data import sys_config_data as SYSCD
from data import skill_fx_data as SFD
DELAY_STOP_TIME = 0.1
AWAIT_EFFECT_TIME = 2
SPECIAL_AWAIT_EFFECT_DUR_TIME = 10.0
GROUP_STAND = 1
GROUP_MOVE = 2
GROUP_FAST_RUN = 3
GROUP_JUMP = 4
GROUP_IN_THE_AIR = 5
GROUP_SPECIAL = 6
AE_AWAIT = 1
AE_SPECIAL_AWAIT = 2
AE_MOVING = 3
AE_ROLL_FORWARD = 4
AE_DASH_START = 5
AE_DASH_DURATION = 6
AE_DASH_STOP = 7
AE_JUMP_UP = 8
AE_DOUBLE_JUMP = 9
AE_FALL_TO_LAND = 10
AE_FAST_JUMP = 11
AE_FAST_RUN_DOUBLE_JUMP = 12
AE_SLIDE_DASH_START = 13
AE_SLIDE_DASH_DURATION = 14
AE_SLIDE = 15
AE_RUSH_DOWN = 16
AE_SLIDE_DASH_STOP = 17
AE_FAST_FALL_TO_LAND = 18
AE_DEAD = 19
AE_REBORN = 20
AE_EXIT_AWAIT = 21
AE_HORSE_DASH_START = 22
AE_HORSE_DASH_DURATION = 23
AE_WING_SLIDE_DASH_START = 24
AE_WING_SLIDE_DASH_DURATION = 25
AE_WINGFLY_UP_DURATION = 26
AE_WINGFLY_DOWN_DURATION = 27
AE_WINGFLY_LANDUP_DURATION = 28
AE_WINGFLY_LEFT_DURATION = 29
AE_WINGFLY_RIGHT_DURATION = 30
AE_WINGFLY_BACK_DURATION = 31
AE_FAST_RUN_BIG_JUMP = 32
AE_FAST_JUMP_STATE = 33
AE_FAST_RUN_BIG_JUMP_STATE = 34
AE_ROLL_LEFT = 35
AE_ROLL_RIGHT = 36
AE_ROLL_BACK = 37
AE_AIR_FALL_TO_LAND = 38
AE_FAST_FALL_TO_LAND_STATE = 39
AE_HORSE_SLIDE_DASH_START = 40
AE_HORSE_SLIDE_DASH_DURATION = 41
AE_HORSEFLY_UP_DURATION = 42
AE_HORSEFLY_DOWN_DURATION = 43
AE_HORSEFLY_LANDUP_DURATION = 44
AE_HORSEFLY_LEFT_DURATION = 45
AE_HORSEFLY_RIGHT_DURATION = 46
AE_HORSEFLY_BACK_DURATION = 47
NO_APPEARANCE_DICT = {AE_HORSE_DASH_START: 'HORSE_DASH_START',
 AE_HORSE_DASH_DURATION: 'HORSE_DASH_DURATION',
 AE_WING_SLIDE_DASH_START: 'WING_SLIDE_DASH_START',
 AE_WING_SLIDE_DASH_DURATION: 'WING_SLIDE_DASH_DURATION',
 AE_WINGFLY_UP_DURATION: 'WINGFLY_UP_DURATION',
 AE_WINGFLY_DOWN_DURATION: 'WINGFLY_DOWN_DURATION',
 AE_WINGFLY_LANDUP_DURATION: 'WINGFLY_LANDUP_DURATION',
 AE_WINGFLY_LEFT_DURATION: 'WINGFLY_LEFT_DURATION',
 AE_WINGFLY_RIGHT_DURATION: 'WINGFLY_RIGHT_DURATION',
 AE_WINGFLY_BACK_DURATION: 'WINGFLY_BACK_DURATION',
 AE_HORSE_SLIDE_DASH_START: 'HORSE_SLIDE_DASH_START',
 AE_HORSE_SLIDE_DASH_DURATION: 'HORSE_SLIDE_DASH_DURATION',
 AE_HORSEFLY_UP_DURATION: 'HORSEFLY_UP_DURATION',
 AE_HORSEFLY_DOWN_DURATION: 'HORSEFLY_DOWN_DURATION',
 AE_HORSEFLY_LANDUP_DURATION: 'HORSEFLY_LANDUP_DURATION',
 AE_HORSEFLY_LEFT_DURATION: 'HORSEFLY_LEFT_DURATION',
 AE_HORSEFLY_RIGHT_DURATION: 'HORSEFLY_RIGHT_DURATION',
 AE_HORSEFLY_BACK_DURATION: 'HORSEFLY_BACK_DURATION'}
EFFECT_MIN_TIME = {AE_AWAIT: 3}
AWAIT_EFFECT_NUM = 3
EFFECT_ONCE_TIME = 5.0

def getEffectByAeType(aeTypes, owner, isAppearance = True):
    if not owner.inWorld:
        return ([],
         [],
         [],
         ())
    basicActEffectIds = getBasicEffectId(aeTypes, owner, isAppearance)
    if basicActEffectIds:
        return getInfo(basicActEffectIds)
    return ([],
     [],
     [],
     ())


def checkActAppearanceValid(owner):
    p = BigWorld.player()
    if hasattr(p, 'anonymNameMgr') and p.anonymNameMgr:
        anonymousType = p.anonymNameMgr.checkNeedAnonymity(entity=owner)
        if anonymousType != gametypes.AnonymousType_None:
            if p.anonymNameMgr.getAnonymousData(anonymousType, gametypes.ANONYMOUS_ACT_APPEARANCE_HIDE, False):
                return False
    return True


def getBasicEffectId(aeTypes, owner, isAppearance = True):
    basicActEffectIds = []
    for aeType in aeTypes:
        if not isAppearance:
            baeId = NO_APPEARANCE_DICT.get(aeType, '')
            basicActEffectIds.append(baeId)
        else:
            actEffectTypeToGroup = SYSCD.data.get('actEffectTypeToGroup', {})
            groupId = actEffectTypeToGroup.get(aeType, 0)
            if groupId:
                appId = 0
                if gameconfigCommon.enableActAppearance() and checkActAppearanceValid(owner):
                    trialActEffectDict = getattr(owner, 'trialActEffectDict', {})
                    tData = trialActEffectDict.get(groupId, {})
                    if tData.get('trialEndTime', 0) - utils.getNow() > 0:
                        appId = tData.get('appearanceId', 0)
                    if not appId:
                        aeDict = owner.actAppearances.get(const.ACT_APPEARANCE_ACTIVE_ACT, {})
                        appId = aeDict.get(groupId, 0)
                    if not appId:
                        appId = getDefaultAppearanceId(groupId)
                else:
                    appId = getDefaultAppearanceId(groupId)
                if appId:
                    aaData = AAD.data.get(appId, {})
                    baeId = aaData.get('effects', {}).get(aeType, None)
                    if baeId:
                        basicActEffectIds.append(baeId)
                else:
                    gamelog.error('@zq physicsEffect no appearanceId', owner.id, aeType, groupId)

    return basicActEffectIds


def trialActEffectAppearance(appearanceId):
    p = BigWorld.player()
    actEffectTrialTime = SYSCD.data.get('actEffectTrialTime', 0)
    groupId = AAD.data.get(appearanceId, {}).get('groupId', {})
    p.trialActEffectDict[groupId] = {'appearanceId': appearanceId,
     'trialEndTime': utils.getNow() + actEffectTrialTime}
    p.apEffectEx.resetEffect()
    if p.trialEffectCallback:
        BigWorld.cancelCallback(p.trialEffectCallback)
        p.trialEffectCallback = None
    time = 0
    for groupId, data in p.trialActEffectDict.iteritems():
        trialEndTime = data.get('trialEndTime', 0)
        if not time:
            if trialEndTime > utils.getNow():
                time = trialEndTime
            continue
        if trialEndTime and trialEndTime < time:
            if trialEndTime > utils.getNow():
                time = trialEndTime

    if time:
        p.trialEffectCallback = BigWorld.callback(time - utils.getNow() + 1, Functor(trialEnd, groupId))


def trialEnd(groupId):
    p = BigWorld.player()
    if p.trialEffectCallback:
        BigWorld.cancelCallback(p.trialEffectCallback)
        p.trialEffectCallback = None
    if groupId in p.trialActEffectDict:
        del p.trialActEffectDict[groupId]
        p.apEffectEx.resetEffect()


def checkItemCanUse(item):
    if not item or not hasattr(item, 'isActEffectAppearanceItem') or not item.isActEffectAppearanceItem():
        return False
    aid = CID.data.get(item.id, {}).get('appearanceId', None)
    if aid is None:
        return False
    itemIds = AAD.data.get(aid, {}).get('useitems', ())
    return item.id in itemIds


def getDefaultAppearanceId(groupId):
    defaultId = AARD.data.get(groupId, {}).get('default', [0])[0]
    return defaultId


def inDate(appearanceId):
    p = BigWorld.player()
    itemId = getItemIdByAppearanceId(appearanceId)
    if itemId:
        time = p.actAppearances.get(const.ACT_APPEARANCE_ACTIVE_ITEM, {}).get(appearanceId, 0)
        if time:
            if time > utils.getNow():
                return True
    return False


def isActive(appearanceId):
    p = BigWorld.player()
    aData = AAD.data.get(appearanceId)
    if aData.get('default', 0):
        return True
    itemId = getItemIdByAppearanceId(appearanceId)
    if itemId:
        time = p.actAppearances.get(const.ACT_APPEARANCE_ACTIVE_ITEM, {}).get(appearanceId, 0)
        if time != 0:
            return True
    return False


def getAppearanceDeadLineTime(appearanceId):
    p = BigWorld.player()
    itemId = getItemIdByAppearanceId(appearanceId)
    if itemId:
        time = p.actAppearances.get(const.ACT_APPEARANCE_ACTIVE_ITEM, {}).get(appearanceId, 0)
        if time:
            return time
    return 0


def getItemIdByAppearanceId(appearanceId):
    aData = AAD.data.get(appearanceId)
    itemIds = aData.get('useitems', ())
    for itemId in itemIds:
        if itemId:
            return itemId

    return 0


def getAppearanceIcon(appId):
    iconId = AAD.data.get(appId, {}).get('icon', 0)
    return 'skill/icon64/%d.dds' % (iconId,)


def getInfo(tags):
    screenEffs = []
    effs = []
    soundFxs = []
    for tag in tags:
        data = BAED.data.get(tag, {})
        screenEff = data.get('screenEff', 0)
        eff = data.get('eff', [])
        soundFx = data.get('soundFx', [])
        motionBlur = data.get('motionEff', None)
        if screenEff:
            screenEffs.append(screenEff)
        effs.extend(eff)
        soundFxs.extend(soundFx)

    return (screenEffs,
     effs,
     soundFxs,
     motionBlur)


class EffectUnit(object):
    MOTIONBLURTIME = 60000.0

    def __init__(self, player, tag, isMultiUnit = True):
        super(EffectUnit, self).__init__()
        self.tag = tag
        self.player = player
        self.soundHandle = []
        self.fxArray = []
        self.attachFx = {}
        self.delayStopCallback = None
        self.startTime = 0
        self.startPosition = None
        self.startYaw = None
        self.isMultiUnit = isMultiUnit

    def start(self, screenEffs, eff, soundFx, motionBlur = None, targetYaw = None):
        self.startPosition = self.player.position
        self.startYaw = self.player.yaw
        self.startTime = utils.getNow(isInt=False)
        if self.player == BigWorld.player():
            screenEffect.startEffects(self.tag, screenEffs, True, self.player)
            if gameglobal.ENABLE_MOTION_BLUR:
                if motionBlur and self.player.getEffectLv() >= gameglobal.EFFECT_MID:
                    blurIntense = motionBlur[0]
                    blurTime = motionBlur[1] <= 0 and EffectUnit.MOTIONBLURTIME or motionBlur[1]
                    BigWorld.motionBlurFilter(None, 0, blurTime, blurIntense)
            for soundIdx in soundFx:
                if soundIdx:
                    gameglobal.rds.sound.playSound(soundIdx)
                    self.soundHandle.append(soundIdx)

        self.fxArray = eff
        for effId in self.fxArray:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.player.getBasicEffectLv(),
             self.player.getBasicEffectPriority(),
             self.player.model,
             effId,
             sfx.EFFECT_LIMIT,
             -1,
             0,
             False,
             None,
             targetYaw))
            if fx:
                if self.isMultiUnit:
                    self.addFx(effId, fx)
                else:
                    self.player.addFx(effId, fx)

    def stop(self):
        self.startTime = 0
        self.startPosition = None
        self.startYaw = None
        if self.delayStopCallback:
            BigWorld.cancelCallback(self.delayStopCallback)
            self.delayStopCallback = None
        screenEffect.delEffect(self.tag)
        BigWorld.motionBlurFilter(None, 0, 0.0, 0.0)
        for effId in self.fxArray:
            if self.isMultiUnit:
                self.removeFx(effId)
            else:
                self.player.removeFx(effId)

        for soundIdx in self.soundHandle:
            gameglobal.rds.sound.stopSound(soundIdx)

        self.fxArray = []
        self.soundHandle = []

    def delayStop(self, delayTime = -1):
        if not self.delayStopCallback:
            screenEffect.delEffect(self.tag)
            BigWorld.motionBlurFilter(None, 0, 0.0, 0.0)
            for soundIdx in self.soundHandle:
                gameglobal.rds.sound.stopSound(soundIdx)

            if delayTime == -1:
                delayTime = DELAY_STOP_TIME
            self.delayStopCallback = BigWorld.callback(delayTime, self.stop)

    def addFx(self, effectId, fx):
        if fx:
            self.attachFx[effectId] = fx

    def getFx(self, effectId):
        if effectId:
            return self.attachFx.get(effectId, None)

    def removeFx(self, effectId):
        if self.attachFx.has_key(effectId):
            sfx.detachEffect(self.player.model, effectId, self.attachFx[effectId])
            del self.attachFx[effectId]


class PhysicsEffectMgrEx(object):

    def __init__(self, player):
        super(PhysicsEffectMgrEx, self).__init__()
        self.player = player
        self.effectUnitDict = {}
        self.lastTag = None
        self.breathHandle = None
        self.flagDict = {}
        self.isMoving = 0
        self.isVerticalMove = 0
        self.awaitEffectCallback = None
        self.movingEffectCallback = None
        self.awaitEffectList = []
        for i in xrange(AWAIT_EFFECT_NUM):
            self.awaitEffectList.append(EffectUnit(self.player, AE_AWAIT, isMultiUnit=True))

        self.specialDurTime = 0
        self.specialBeginTime = 0

    def setPlayer(self, player):
        self.player = player

    def getEffectUnit(self, tag):
        if not self.effectUnitDict.has_key(tag):
            unit = EffectUnit(self.player, tag)
            self.effectUnitDict[tag] = unit
        return self.effectUnitDict[tag]

    def getAwaitEffectUnit(self):
        last = self.awaitEffectList[-1]
        new = self.awaitEffectList.pop(0)
        self.awaitEffectList.append(new)
        return (last, new)

    def getLastAwaitEffectUnit(self):
        last = self.awaitEffectList[-1]
        return last

    def set_inDying(self, old):
        pass

    def isPlayerAvatar(self):
        return utils.instanceof(self.player, 'PlayerAvatar')

    def inHiding(self):
        if hasattr(self.player, 'inHiding') and self.player.inHiding():
            return True
        return False

    def set_life(self, old):
        if self.player.life:
            screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_REBORN,), self.player)
            if not self.isPlayerAvatar():
                screenEffs = []
                soundFxs = []
                motionBlur = []
            tag = AE_REBORN
            unit = self.getEffectUnit(tag)
            unit.stop()
            deadUnit = self.getEffectUnit(AE_DEAD)
            if deadUnit:
                deadUnit.stop()
            unit.start(screenEffs, effs, soundFxs, motionBlur)
        else:
            screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_DEAD,), self.player)
            if not self.isPlayerAvatar():
                screenEffs = []
                soundFxs = []
                motionBlur = []
            tag = AE_DEAD
            unit = self.getEffectUnit(tag)
            unit.stop()
            unit.start(screenEffs, effs, soundFxs, motionBlur)
        self.delAwaitEffect(immediatelyStop=True, forceDel=True)
        self.delMovingEffect(immediatelyStop=True, forceDel=True)
        self.refreshMovingEffect()

    def refreshDeadEffect(self):
        if getattr(self.player, 'life', 0) == gametypes.LIFE_DEAD:
            screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_DEAD,), self.player)
            if not self.isPlayerAvatar():
                screenEffs = []
                soundFxs = []
                motionBlur = []
            tag = AE_DEAD
            unit = self.getEffectUnit(tag)
            unit.stop()
            unit.start(screenEffs, effs, soundFxs, motionBlur)

    def getJingJieSchoolEff(self, basicId):
        jingJieSchoolEffs = BAED.data.get(basicId, {}).get('jingJieSchoolEffs', {}).get(self.player.school, {})
        if jingJieSchoolEffs:
            keys = [ i for i in jingJieSchoolEffs.keys() if i <= self.player.jingJie ]
            if keys:
                maxJingJie = max(keys)
                return jingJieSchoolEffs.get(maxJingJie, [])
        return []

    def getInFlyType(self):
        return getattr(self.player, 'inFly', 0)

    def set_qinggongState(self, old):
        if self.lastTag:
            unit = self.getEffectUnit(self.lastTag)
            unit.delayStop()
        screenEffs, effs, soundFxs, motionBlur = ([],
         [],
         [],
         ())
        onceEffs = []
        self.flagDict['fastRun'] = False
        tag = None
        if self.player.qinggongState == gametypes.QINGGONG_STATE_DEFAULT:
            self.refreshMovingEffect()
            if self.flagDict.get('fallType', 0) == AE_FAST_FALL_TO_LAND:
                screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_FAST_FALL_TO_LAND_STATE,), self.player)
                tag = AE_FAST_FALL_TO_LAND_STATE
        else:
            self.cancelAwaitEffCallback()
            self.delAwaitEffect(immediatelyStop=True, forceDel=True)
            self.cancelMovingEffCallback()
            self.delMovingEffect(immediatelyStop=True, forceDel=True)
        flyType = self.getInFlyType()
        if self.player.qinggongState == gametypes.QINGGONG_STATE_FAST_RUN:
            self.flagDict['fastRun'] = True
            self.delMovingEffect(forceDel=True)
            screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_DASH_START, AE_DASH_DURATION), self.player)
            basicIds = getBasicEffectId((AE_DASH_START, AE_DASH_DURATION), self.player)
            for bId in basicIds:
                schoolEff = BAED.data.get(bId, {}).get('schoolEff', {}).get(self.player.school, [])
                effs.extend(schoolEff)
                jingJieSchoolEff = self.getJingJieSchoolEff(bId)
                if jingJieSchoolEff:
                    effs.extend(jingJieSchoolEff)

            if not self.player.inSwim:
                tag = AE_DASH_DURATION
        elif self.player.qinggongState == gametypes.QINGGONG_STATE_MOUNT_DASH:
            screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_HORSE_DASH_START, AE_HORSE_DASH_DURATION), self.player, False)
            tag = AE_HORSE_DASH_DURATION
        elif self.player.qinggongState == gametypes.QINGGONG_STATE_FAST_SLIDING:
            screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_SLIDE_DASH_START, AE_SLIDE_DASH_DURATION), self.player, False)
            tag = AE_SLIDE_DASH_DURATION
        elif self.player.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_DASH:
            if flyType == gametypes.IN_FLY_TYPE_FLY_RIDE:
                screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_HORSE_SLIDE_DASH_START, AE_HORSE_SLIDE_DASH_DURATION), self.player, False)
                tag = AE_HORSE_SLIDE_DASH_DURATION
            else:
                screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_WING_SLIDE_DASH_START, AE_WING_SLIDE_DASH_DURATION), self.player, False)
                tag = AE_WING_SLIDE_DASH_DURATION
        elif self.player.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_UP:
            if flyType == gametypes.IN_FLY_TYPE_FLY_RIDE:
                screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_HORSEFLY_UP_DURATION,), self.player, False)
                tag = AE_HORSEFLY_UP_DURATION
            else:
                screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_WINGFLY_UP_DURATION,), self.player, False)
                tag = AE_WINGFLY_UP_DURATION
        elif self.player.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_DOWN:
            if flyType == gametypes.IN_FLY_TYPE_FLY_RIDE:
                screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_HORSEFLY_DOWN_DURATION,), self.player, False)
                tag = AE_HORSEFLY_DOWN_DURATION
            else:
                screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_WINGFLY_DOWN_DURATION,), self.player, False)
                tag = AE_WINGFLY_DOWN_DURATION
        elif self.player.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_LANDUP:
            if flyType == gametypes.IN_FLY_TYPE_FLY_RIDE:
                screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_HORSEFLY_LANDUP_DURATION,), self.player, False)
                tag = AE_HORSEFLY_LANDUP_DURATION
            else:
                screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_WINGFLY_LANDUP_DURATION,), self.player, False)
                tag = AE_WINGFLY_LANDUP_DURATION
        elif self.player.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_LEFT:
            if flyType == gametypes.IN_FLY_TYPE_FLY_RIDE:
                screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_HORSEFLY_LEFT_DURATION,), self.player, False)
                tag = AE_HORSEFLY_LEFT_DURATION
            else:
                screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_WINGFLY_LEFT_DURATION,), self.player, False)
                tag = AE_WINGFLY_LEFT_DURATION
        elif self.player.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_RIGHT:
            if flyType == gametypes.IN_FLY_TYPE_FLY_RIDE:
                screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_HORSEFLY_RIGHT_DURATION,), self.player, False)
                tag = AE_HORSEFLY_RIGHT_DURATION
            else:
                screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_WINGFLY_RIGHT_DURATION,), self.player, False)
                tag = AE_WINGFLY_RIGHT_DURATION
        elif self.player.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_BACK:
            if flyType == gametypes.IN_FLY_TYPE_FLY_RIDE:
                screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_HORSEFLY_BACK_DURATION,), self.player, False)
                tag = AE_HORSEFLY_BACK_DURATION
            else:
                screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_WINGFLY_BACK_DURATION,), self.player, False)
                tag = AE_WINGFLY_BACK_DURATION
        elif self.player.qinggongState == gametypes.QINGGONG_STATE_SLIDING:
            screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_SLIDE,), self.player)
            tag = AE_SLIDE
            self.flagDict['fallType'] = AE_AIR_FALL_TO_LAND
        elif self.player.qinggongState == gametypes.QINGGONG_STATE_FAST_JUMP:
            screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_FAST_JUMP_STATE,), self.player)
            tag = AE_FAST_JUMP_STATE
            self.flagDict['fallType'] = AE_AIR_FALL_TO_LAND
        elif self.player.qinggongState == gametypes.QINGGONG_STATE_FAST_BIG_JUMP:
            screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_FAST_RUN_BIG_JUMP_STATE,), self.player)
            tag = AE_FAST_RUN_BIG_JUMP_STATE
            self.flagDict['fallType'] = AE_AIR_FALL_TO_LAND
        elif self.player.qinggongState == gametypes.QINGGONG_STATE_RUSH_DOWN:
            screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_RUSH_DOWN,), self.player)
            tag = AE_RUSH_DOWN
            self.flagDict['fallType'] = AE_AIR_FALL_TO_LAND
        elif self.player.qinggongState == gametypes.QINGGONG_STATE_DEFAULT:
            if old == gametypes.QINGGONG_STATE_FAST_RUN and not self.player.inSwim:
                _, onceEffs, _, _ = getEffectByAeType((AE_DASH_STOP,), self.player)
                tag = AE_DASH_STOP
        if old == gametypes.QINGGONG_STATE_FAST_SLIDING:
            _, onceEffs, _, _ = getEffectByAeType((AE_SLIDE_DASH_STOP,), self.player)
        if self.isPlayerAvatar():
            self.switchBreathFx(old)
        else:
            screenEffs = []
            soundFxs = []
            motionBlur = []
        if self.inHiding():
            return
        for _eff in onceEffs:
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.player.getBasicEffectLv(),
             self.player.getBasicEffectPriority(),
             self.player.model,
             _eff,
             sfx.EFFECT_LIMIT,
             EFFECT_ONCE_TIME))

        if tag:
            unit = self.getEffectUnit(tag)
            self.lastTag = tag
            unit.stop()
            unit.start(screenEffs, effs, soundFxs, motionBlur)

    def doQinggongAction(self, qtype):
        if self.inHiding():
            return
        effs = []
        if qtype == gametypes.QINGGONG_DOUBLE_JUMP:
            _, effs, _, _ = getEffectByAeType((AE_DOUBLE_JUMP,), self.player)
        elif qtype == gametypes.QINGGONG_FAST_RUN_JUMP:
            _, effs, _, _ = getEffectByAeType((AE_FAST_JUMP,), self.player)
        elif qtype == gametypes.QINGGONG_FAST_RUN_BIG_JUMP:
            _, effs, _, _ = getEffectByAeType((AE_FAST_RUN_BIG_JUMP,), self.player)
        elif qtype == gametypes.QINGGONG_FAST_RUN_DOUBLE_JUMP:
            _, effs, _, _ = getEffectByAeType((AE_FAST_RUN_DOUBLE_JUMP,), self.player)
        elif qtype == gametypes.QINGGONG_FAST_DOWN:
            self.flagDict['fallType'] = AE_FAST_FALL_TO_LAND
        elif qtype == gametypes.QINGGONG_ROLL_FORWARD:
            _, effs, _, _ = getEffectByAeType((AE_ROLL_FORWARD,), self.player)
        elif qtype == gametypes.QINGGONG_ROLL_LEFT:
            _, effs, _, _ = getEffectByAeType((AE_ROLL_LEFT,), self.player)
        elif qtype == gametypes.QINGGONG_ROLL_RIGHT:
            _, effs, _, _ = getEffectByAeType((AE_ROLL_RIGHT,), self.player)
        elif qtype == gametypes.QINGGONG_ROLL_BACK:
            _, effs, _, _ = getEffectByAeType((AE_ROLL_BACK,), self.player)
        if qtype in (gametypes.QINGGONG_ROLL_LEFT,
         gametypes.QINGGONG_ROLL_RIGHT,
         gametypes.QINGGONG_ROLL_BACK,
         gametypes.QINGGONG_ROLL_FORWARD):
            if not self.isPlayerAvatar():
                self.delAwaitEffect(forceDel=True)
                BigWorld.callback(0.5, self.refreshMovingEffect)
        for eff in effs:
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.player.getBasicEffectLv(),
             self.player.getBasicEffectPriority(),
             self.player.model,
             eff,
             sfx.EFFECT_LIMIT,
             EFFECT_ONCE_TIME))

    def playBoredAction(self):
        if self.inHiding():
            return
        if self.player.canFly():
            return
        if getattr(self.player, 'bianshen', (0, 0))[0]:
            return
        nowTime = utils.getNow()
        if self.specialBeginTime:
            if nowTime - self.specialBeginTime < self.specialDurTime:
                return
        self.specialDurTime = 0
        self.specialBeginTime = 0
        _, effs, _, _ = getEffectByAeType((AE_SPECIAL_AWAIT,), self.player)
        if effs:
            for eff in effs:
                durTime = SFD.data.get(eff, {}).get('modelKeepFx', SPECIAL_AWAIT_EFFECT_DUR_TIME)
                if not self.specialDurTime and durTime > self.specialDurTime:
                    self.specialDurTime = durTime
                sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.player.getBasicEffectLv(),
                 self.player.getBasicEffectPriority(),
                 self.player.model,
                 eff,
                 sfx.EFFECT_LIMIT,
                 durTime))

            self.specialBeginTime = utils.getNow()

    def movingNotifier(self, isMoving):
        self.isMoving = isMoving
        self.refreshMovingEffect()

    def verticalMoveNotifier(self, isVerticalMove):
        if not self.isPlayerAvatar():
            self.isVerticalMove = isVerticalMove
            if self.isVerticalMove:
                if self.awaitEffectCallback:
                    BigWorld.cancelCallback(self.awaitEffectCallback)
                    self.awaitEffectCallback = None
                self.delAwaitEffect(forceDel=True)
            else:
                self.refreshMovingEffect()

    def physicsMovingNotifier(self, isMoving):
        if self.isPlayerAvatar():
            self.isMoving = isMoving
            self.refreshMovingEffect()

    def refreshMovingEffect(self):
        if self.inHiding():
            return
        if not self.player.inWorld:
            return
        if self.isMoving:
            self.cancelMovingEffCallback()
            self.delAwaitEffect()
            if getattr(self.player, 'life', 0) == gametypes.LIFE_DEAD:
                return
            if not getattr(self.player, 'bianshen', (0, 0))[0]:
                self.movingEffectCallback = BigWorld.callback(0.5, self.addMovingEffect)
        else:
            self.cancelAwaitEffCallback()
            self.delMovingEffect()
            if getattr(self.player, 'life', 0) == gametypes.LIFE_DEAD:
                return
            if not getattr(self.player, 'bianshen', (0, 0))[0] and not self.player.canFly():
                if self.isPlayerAvatar() or not self.isVerticalMove:
                    self.awaitEffectCallback = BigWorld.callback(AWAIT_EFFECT_TIME, self.addAwaitEffect)

    def cancelMovingEffCallback(self):
        if self.movingEffectCallback:
            BigWorld.cancelCallback(self.movingEffectCallback)
            self.movingEffectCallback = None

    def cancelAwaitEffCallback(self):
        if self.awaitEffectCallback:
            BigWorld.cancelCallback(self.awaitEffectCallback)
            self.awaitEffectCallback = None

    def jumpUp(self):
        if self.inHiding():
            return
        if self.player.canFly():
            return
        _, effs, _, _ = getEffectByAeType((AE_JUMP_UP,), self.player)
        if effs:
            for eff in effs:
                sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.player.getBasicEffectLv(),
                 self.player.getBasicEffectPriority(),
                 self.player.model,
                 eff,
                 sfx.EFFECT_LIMIT,
                 EFFECT_ONCE_TIME))

    def fallToLand(self):
        if self.inHiding():
            return
        if self.player.canFly():
            return
        fallType = self.flagDict.get('fallType', AE_FALL_TO_LAND)
        unit = self.getEffectUnit(AE_FAST_FALL_TO_LAND_STATE)
        unit.delayStop()
        effs = []
        _, effs, _, _ = getEffectByAeType((fallType,), self.player)
        if effs:
            for eff in effs:
                sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.player.getBasicEffectLv(),
                 self.player.getBasicEffectPriority(),
                 self.player.model,
                 eff,
                 sfx.EFFECT_LIMIT,
                 EFFECT_ONCE_TIME))

        self.flagDict['fallType'] = AE_FALL_TO_LAND

    def switchBreathFx(self, old):
        modelID = self.player.fashion.modelID
        path = None
        if old == gametypes.QINGGONG_STATE_FAST_RUN:
            if self.breathHandle:
                Sound.stopFx(self.breathHandle)
            path = 'fx/protagonist/%s_vo/%s_breath_end' % (modelID, modelID)
        if self.player.qinggongState == gametypes.QINGGONG_STATE_FAST_RUN and not self.player.inSwim:
            if self.breathHandle:
                Sound.stopFx(self.breathHandle)
            path = 'fx/protagonist/%s_vo/%s_breath_start' % (modelID, modelID)
        if path:
            self.breathHandle = gameglobal.rds.sound.playFx(path, self.player.position, True, self.player)

    def getFallToLandEffect(self, velocity):
        eff = None
        fallToLandEffect = SYSCD.data.get('fallToLandEffect', {})
        for keySpeed in fallToLandEffect.keys():
            if keySpeed and len(keySpeed) == 2:
                if velocity > keySpeed[0] and velocity <= keySpeed[1]:
                    eff = fallToLandEffect.get(keySpeed, ())
                    break

        return eff

    def stopAllEffect(self):
        self.cancelAwaitEffCallback()
        self.cancelMovingEffCallback()
        for k, v in self.effectUnitDict.iteritems():
            v.stop()

        for v in self.awaitEffectList:
            v.stop()

        self.lastTag = None
        self.effectUnitDict = {}

    def addAwaitEffect(self):
        lastUnit, newUnit = self.getAwaitEffectUnit()
        newUnit.stop()
        if getattr(self.player, 'life', 0) == gametypes.LIFE_DEAD:
            return
        if self.inHiding():
            return
        if self.player.canFly():
            return
        if self.player.life == gametypes.LIFE_DEAD:
            return
        if not self.isMoving:
            screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_AWAIT,), self.player)
            targetYaw = self.player.yaw
            newUnit.start(screenEffs, effs, soundFxs, motionBlur, targetYaw)
            self.flagDict['awaitEffect'] = True

    def delAwaitEffect(self, immediatelyStop = False, forceDel = False):
        if self.isMoving or forceDel:
            lastUnit = self.getLastAwaitEffectUnit()
            minTime = 0
            durTime = 0
            lastPos = None
            lastYaw = None
            if lastUnit:
                lastYaw = lastUnit.startYaw if lastUnit else None
                lastPos = lastUnit.startPosition if lastUnit else 0
                minTime = self.getEffectMinTime(lastUnit.tag)
                durTime = utils.getNow(isInt=False) - lastUnit.startTime
                self.stopUnitWithMinTime(lastUnit)
            if self.flagDict.get('awaitEffect', None) and not immediatelyStop:

                def _addDelEffect(lPos, lYaw):
                    _, effs, _, _ = getEffectByAeType((AE_EXIT_AWAIT,), self.player)
                    if effs:
                        for eff in effs:
                            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.player.getBasicEffectLv(),
                             self.player.getBasicEffectPriority(),
                             self.player.model,
                             eff,
                             sfx.EFFECT_LIMIT,
                             EFFECT_ONCE_TIME,
                             lPos,
                             False,
                             None,
                             lYaw))

                if durTime < minTime:
                    BigWorld.callback(minTime - durTime, Functor(_addDelEffect, lastPos, lastYaw))
                else:
                    _addDelEffect(lastPos, lastYaw)
            self.flagDict['awaitEffect'] = False

    def getEffectMinTime(self, tag):
        if self.isPlayerAvatar():
            return EFFECT_MIN_TIME.get(tag, 0)
        return 0

    def stopUnitWithMinTime(self, unit):
        minTime = self.getEffectMinTime(unit.tag)
        durTime = utils.getNow(isInt=False) - unit.startTime
        if unit.startTime and durTime < minTime:
            unit.delayStop(minTime - durTime + 0.1)
        else:
            unit.delayStop()

    def addMovingEffect(self):
        unit = self.getEffectUnit(AE_MOVING)
        unit.stop()
        if getattr(self.player, 'life', 0) == gametypes.LIFE_DEAD:
            return
        if self.inHiding():
            return
        if self.player.canFly():
            return
        if self.isMoving:
            screenEffs = []
            effs = []
            soundFxs = []
            motionBlur = ()
            if not self.flagDict.get('fastRun', None):
                screenEffs, effs, soundFxs, motionBlur = getEffectByAeType((AE_MOVING,), self.player)
                unit.start(screenEffs, effs, soundFxs, motionBlur)

    def delMovingEffect(self, immediatelyStop = False, forceDel = False):
        if not self.isMoving or forceDel:
            unit = self.getEffectUnit(AE_MOVING)
            if immediatelyStop:
                unit.stop()
            else:
                unit.delayStop()

    def resetEffect(self):
        self.delAwaitEffect(immediatelyStop=True, forceDel=True)
        self.delMovingEffect(immediatelyStop=True, forceDel=True)
        self.stopAllEffect()
        self.refreshMovingEffect()
        self.refreshDeadEffect()
