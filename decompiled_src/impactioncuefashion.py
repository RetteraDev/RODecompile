#Embedded file name: /WORKSPACE/data/entities/client/helpers/impactioncuefashion.o
import time
import math
import BigWorld
import ResMgr
import Sound
import const
import gametypes
import gameglobal
import gamelog
import random
import utils
import skillDataInfo
from callbackHelper import Functor
from sfx import sfx
from sfx import cameraEffect
from sfx import stateFX
from sfx import screenEffect
from helpers import tintalt
from helpers import scenario
from sfx import clientEffect
from helpers import attachedModel

class ImpActionCueFashion(object):

    def actionCueCallback(self, cueId, data, actionName):
        if not hasattr(self, 'owner'):
            return
        ent = BigWorld.entity(self.owner)
        p = BigWorld.player()
        if not (ent and ent.inWorld):
            return
        if gameglobal.rds.GameState > gametypes.GS_LOGIN and (ent.position - p.position).lengthSquared > gameglobal.MAX_DISTANCE_ACTION_CUE * gameglobal.MAX_DISTANCE_ACTION_CUE:
            if not getattr(ent, 'IsMonster', False) and not getattr(ent, 'IsCombatCreation', False) and gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_END:
                return
        if hasattr(ent, 'getOpacityValue'):
            opacityValue = ent.getOpacityValue()
            if opacityValue in [gameglobal.OPACITY_HIDE, gameglobal.OPACITY_HIDE_WITHOUT_NAME]:
                return
        if cueId == 1:
            self._playSound(data, actionName)
        elif cueId == 2:
            if data.startswith('s'):
                self._attachEffect(data, actionName)
            elif data.startswith('d'):
                self._swayCamera(data)
            elif data.startswith('f'):
                self._newSwayCamera(data)
            elif data.startswith('x'):
                self._shockCamera(data)
            elif data.startswith('c'):
                self._blurScreen(data)
            elif data.startswith('h'):
                self._hideModel(data)
            elif data.startswith('g'):
                self._cameraPush(data)
            elif data.startswith('i'):
                self._attachHintEffect(data)
        elif cueId == 12:
            self._screenBlack(data)
        elif cueId == 13:
            self._rotateCamera(data)
        elif cueId == 14:
            self._switchWeapon(data)
        elif cueId == 16:
            self._showSpecSkill(data)
        elif cueId == 17:
            self._cameraAnimate(data)
        elif cueId == 18:
            pass
        elif cueId == 19:
            self._scaleModel(data)
        elif cueId == 20:
            self._actionFreeze(data)
        elif cueId == 21:
            self._lockRightMouse(data)
        elif cueId == 22:
            self._attachTextureEffect(data)
        elif cueId == 23:
            self._fullScreenEffect(data)
        elif cueId == 24:
            self._changeActionSpeed(data)
        elif cueId == 25:
            self._playEffectBySchool(data)
        elif cueId == 26:
            self._playCircelEffect(data)
        elif cueId == 27:
            self._playSquareEffect(data)
        elif cueId == 28:
            self._fallGround(data)
        elif cueId == 29:
            self._behitFreeze(data)
        elif cueId == 30:
            self._leftRightAppel(data)
        elif cueId == 31:
            self._attachAndDetachLifeSkillModel(data)
        elif cueId == 33:
            self._jiDaoStartActionGround(data)
        elif cueId == 35:
            self.doFade(ent, data)
        elif cueId == 36:
            self.attachMidWeaponWithZhuShou(ent, data)
        elif cueId == 37:
            self.detachMidWeaponWithZhuShou(ent, data)
        elif cueId == 38:
            self.setEntityYaw(data)
        elif cueId == 39:
            self.setEntityActionEnableAlpha(data)
        elif cueId == 40:
            self.attachHorseTrail(data)
        elif cueId == 41:
            self._playVoice(data, actionName)

    def attachHorseTrail(self, data):
        ent = BigWorld.entity(self.owner)
        if not ent.inWorld:
            return
        if getattr(ent.model, 'dummyModel', False):
            return
        if not hasattr(BigWorld, 'TrailModel'):
            return
        params = data.split(':')
        try:
            attachType = int(params[0])
            length = float(params[1])
            interval = float(params[2])
            duration = float(params[3])
            name = 'effect/material/%s.xml' % str(params[4])
            onlyPlayer = True
            if len(params) > 5:
                onlyPlayer = bool(int(params[5]))
            if onlyPlayer and ent != BigWorld.player():
                return
            if attachType == 1:
                if ent.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
                    if not hasattr(ent.model, 'trail'):
                        tr = BigWorld.TrailModel(ent.model, length, interval, name)
                        ent.model.trail = tr
                    ent.model.trail.show(duration)
            elif attachType == 2:
                if not hasattr(ent.model, 'trail'):
                    tr = BigWorld.TrailModel(ent.model, length, interval, name)
                    ent.model.trail = tr
                ent.model.trail.show(duration)
        except Exception as e:
            gamelog.debug('-----m.l@ImpActionCueFashion.attachHorseTrail', e.message)

    def setEntityActionEnableAlpha(self, data):
        ent = BigWorld.entity(self.owner)
        if not ent.inWorld:
            return
        needEnable = bool(data)
        ent.model.enableAlphaAll(needEnable)

    def attachMidWeaponWithZhuShou(self, owner, data):
        enableAttachWeaponCue = gameglobal.rds.configData.get('enableAttachWeaponCue', False)
        if not enableAttachWeaponCue:
            return
        if utils.instanceof(owner, 'AvatarMonster'):
            return
        if data:
            params = data.split(':')
            attachType = int(params[0])
            actionId = str(params[1])
            if not hasattr(owner, 'switchWeaponState'):
                return
            owner.switchWeaponState(attachType, False)
            scale = owner.getCombatSpeedIncreseRatio()
            if attachType == gametypes.WEAPON_MIDATTACH_WITH_ZHUSHOU:
                owner.modelServer.playAllWeaponAction(actionId, scale)
            elif attachType == gametypes.WEAPON_MIDATTACH_WITH_ZHUSHOU_LEFT:
                owner.modelServer.playLeftWeaponAction(actionId, scale)
            elif attachType == gametypes.WEAPON_MIDATTACH_WITH_ZHUSHOU_RIGHT:
                owner.modelServer.playRightWeaponAction(actionId, scale)
            if owner == BigWorld.player():
                owner.invokeWeaponTimer()

    def detachMidWeaponWithZhuShou(self, owner, data):
        enableAttachWeaponCue = gameglobal.rds.configData.get('enableAttachWeaponCue', False)
        if not enableAttachWeaponCue:
            return
        if not hasattr(owner, 'switchWeaponState'):
            return
        attachType = int(data)
        if owner.modelServer.rightWeaponModel:
            owner.modelServer.rightWeaponModel.detachRightToLeft()
        owner.switchWeaponState(attachType, False)

    def doFade(self, ent, data):
        fadeTime = float(data)
        if ent.inWorld and getattr(ent, 'IsAvatar', False):
            ent.fadeToReal(fadeTime)

    def _setModelActionSpeed(self, ent, actionSpeed):
        if ent.inWorld:
            ent.model.actionSpeed = actionSpeed

    def _jiDaoStartActionGround(self, data):
        ent = BigWorld.entity(self.owner)
        if hasattr(ent, 'clearDaoDiAction'):
            ent.clearDaoDiAction()

    def _playSound(self, data, actionName):
        ent = BigWorld.entity(self.owner)
        if ent != None:
            if ent.IsSummonedSprite:
                if not BigWorld.player().checkSpriteCanPlaySound(ent.id):
                    return
            if scenario.scenarioIsForbidFx() and hasattr(ent, 'isScenario') and ent.isScenario in (gameglobal.SCENARIO_PLAY_NPC, gameglobal.SCENARIO_EDIT_NPC):
                return
            if hasattr(ent, 'inHiding') and ent.inHiding() and ent != BigWorld.player():
                return
            params = data.split(':')
            try:
                onlyPlayer = int(params[1])
                needBreak = int(params[2]) if len(params) >= 3 else False
            except:
                onlyPlayer, needBreak = False, False

            soundPath = str(params[0])
            if onlyPlayer and not ent.fashion.isPlayer:
                return
            if needBreak:
                handle = gameglobal.rds.sound.playFx(soundPath, ent.position, True, ent)
                if not self.cueSound.has_key(actionName):
                    self.cueSound[actionName] = []
                self.cueSound[actionName].append(handle)
            else:
                gameglobal.rds.sound.playFx(soundPath, ent.position, False, ent)
            if gameglobal.g_Print_SoundPath:
                gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SYSTEM, soundPath, '')

    def _attachEffect(self, data, actionName):
        ent = BigWorld.entity(self.owner)
        if ent != None:
            params = data[1:].split(':')
            effects = params[0][1:-1].split(',')
            delayTime = 0.0
            if len(params) > 1:
                delayTime = float(params[1])
            onlyPlayer = bool(float(params[2])) if len(params) > 2 else False
            needBreak = int(params[3]) if len(params) > 3 else False
            if onlyPlayer and ent != BigWorld.player():
                return
            for e in effects:
                tt = e.split('.xml-')
                if len(tt) == 2:
                    effect = tt[0].split('/')
                    effectIdStr = effect[-1]
                    if not effectIdStr.isdigit() and '_' in effectIdStr:
                        effectIdStr = effectIdStr.split('_')[-1]
                    if effectIdStr.isdigit():
                        effEnt = ent
                        if ent.__class__.__name__ == 'SummonedBeast' or getattr(ent, 'IsCreation', False) == True:
                            masterId = getattr(ent, 'ownerId', 0)
                            master = BigWorld.entities.get(masterId)
                            if master and master.inWorld:
                                effEnt = master
                        if getattr(effEnt, 'inCombat', 0):
                            effectLv = effEnt.getSkillEffectLv()
                            priority = effEnt.getSkillEffectPriority()
                        else:
                            effectLv = effEnt.getBasicEffectLv()
                            priority = effEnt.getBasicEffectPriority()

                        def _attachEffect():
                            fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (effectLv,
                             priority,
                             ent.model,
                             int(effectIdStr),
                             sfx.EFFECT_LIMIT,
                             float(tt[1]) / gameglobal.ACTION_FRAME))
                            if fxs != None and needBreak:
                                if not self.cueEffect.has_key(actionName):
                                    self.cueEffect[actionName] = []
                                self.cueEffect[actionName].append(fxs)

                        BigWorld.callback(delayTime, _attachEffect)

    def _swayCamera(self, data):
        ent = BigWorld.entity(self.owner)
        if gameglobal.rds.GameState > gametypes.GS_LOGIN:
            p = BigWorld.player()
            if p.excludeCam:
                return
            if ent.__class__.__name__ == 'Avatar':
                return
        params = data[1:].split(':')
        duration = float(params[0])
        frequency = float(params[1])
        verticalAmplitude = float(params[2])
        horizontalAmplitude = float(params[3])
        playerOnly = int(params[4])
        decayDist = float(params[5])
        delayTime = len(params) >= 7 and float(params[6]) or 0
        screenEffect.swayCamera(duration, frequency, verticalAmplitude, horizontalAmplitude, playerOnly, decayDist, delayTime, ent)

    def _newSwayCamera(self, data):
        ent = BigWorld.entity(self.owner)
        if gameglobal.rds.GameState > gametypes.GS_LOGIN:
            p = BigWorld.player()
            if p.excludeCam:
                return
            if ent.__class__.__name__ == 'Avatar':
                return
        params = data[1:].split(':')
        duration1 = float(params[0])
        duration2 = float(params[1])
        threshold = float(params[2])
        rotationAmp = float(params[3])
        amp = params[4].replace('(', '').replace(')', '').replace(',', ' ').strip().split(' ')
        if len(amp) != 3:
            amp = (0.0, 0.0, 0.0)
        else:
            amp = (float(amp[0]), float(amp[1]), float(amp[2]))
        frequency = float(params[5])
        controlPts = params[6].replace('(', '').replace(')', '').replace(',', ' ').strip().split(' ')
        if len(controlPts) != 2:
            controlPts = ((0.0, 0.0),)
        else:
            controlPts = ((float(controlPts[0]), float(controlPts[1])),)
        screenEffect.newSway(duration1, duration2, threshold, rotationAmp, amp, frequency, controlPts, ent, gameglobal.SWAY_PRIORITY_LOW)

    def _shockCamera(self, data):
        ent = BigWorld.entity(self.owner)
        if gameglobal.rds.GameState > gametypes.GS_LOGIN and gameglobal.SCENARIO_PLAYING != gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            p = BigWorld.player()
            if hasattr(p, 'excludeCam') and p.excludeCam:
                return
            if ent.__class__.__name__ == 'Avatar':
                return
        params = data[1:].split(':')
        duration = float(params[0])
        x = float(params[1])
        y = float(params[2])
        z = float(params[3])
        playerOnly = int(params[4])
        decayDist = float(params[5])
        delayTime = float(params[6])
        screenEffect.shakeCamera(duration, x, y, z, playerOnly, decayDist, delayTime, ent)

    def _blurScreen(self, data):
        ent = BigWorld.entity(self.owner)
        if gameglobal.rds.GameState > gametypes.GS_LOGIN and gameglobal.SCENARIO_PLAYING != gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            p = BigWorld.player()
            if hasattr(p, 'excludeCam') and p.excludeCam:
                return
            if ent.__class__.__name__ == 'Avatar':
                return
            if not gameglobal.ENABLE_SKILL_SCREEN_EFFECT:
                return
            if ent.getEffectLv() < gameglobal.EFFECT_MID:
                return
        cam = BigWorld.camera()
        params = data[1:].split(':')
        gamelog.debug('data:', params)
        if gameglobal.SCENARIO_PLAYING != gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            try:
                onlyPlayer = int(params[2])
            except:
                onlyPlayer = 1

            if onlyPlayer:
                if not self.isPlayer:
                    return
        if isinstance(cam, BigWorld.TrackCamera) or gameglobal.rds.GameState <= gametypes.GS_LOGIN or gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            BigWorld.motionBlurFilter(None, 0, float(params[0]), float(params[1]))
        else:
            dist = 50
            if (ent.position - BigWorld.player().position).length > dist:
                return
            BigWorld.motionBlurFilter(None, 0, float(params[0]), float(params[1]))

    def _hideModel(self, data):
        params = data[1:].split(':')
        gamelog.debug('data:', params)
        self.hide(True)
        hideTime = int(params[0]) * 1.0 / gameglobal.ACTION_FRAME
        BigWorld.callback(hideTime, Functor(self.hide, False))

    def _cameraPush(self, data):
        ent = BigWorld.entity(self.owner)
        if gameglobal.rds.GameState > gametypes.GS_LOGIN:
            p = BigWorld.player()
            if p.excludeCam:
                return
            if ent.__class__.__name__ == 'Avatar':
                return
            if not cameraEffect.checkEnableAnimateCamera():
                return
        params = data[1:].split(':')
        gamelog.debug('data:', params)
        onlyPlayer = params[4] == '1'
        if onlyPlayer:
            if not self.isPlayer:
                return
        screenEffect.playCameraPush(params)

    def _attachHintEffect(self, data):
        ent = BigWorld.entity(self.owner)
        if ent != None:
            params = data[1:].split(':')
            effects = params[0][1:-1].split(',')
            duration = float(params[1]) / gameglobal.ACTION_FRAME
            delayTime = float(params[2])
            onlyPlayer = bool(float(params[3]))
            if onlyPlayer and ent != BigWorld.player():
                return
            player = BigWorld.player()
            master = ent
            if ent.__class__.__name__ == 'SummonedBeast' or getattr(ent, 'IsCreation', False) == True:
                masterId = getattr(ent, 'ownerId', 0)
                master = BigWorld.entities.get(masterId)
            effect = effects[0] if player.isEnemy(master) else effects[1]
            tt = effect.split('.xml')
            if len(tt) == 2:
                effect = tt[0].split('/')
                effectIdStr = effect[-1]
                if not effectIdStr.isdigit() and '_' in effectIdStr:
                    effectIdStr = effectIdStr.split('_')[-1]
                if effectIdStr.isdigit():
                    effEnt = ent
                    if ent.__class__.__name__ == 'SummonedBeast' or getattr(ent, 'IsCreation', False) == True:
                        masterId = getattr(ent, 'ownerId', 0)
                        master = BigWorld.entities.get(masterId)
                        if master and master.inWorld:
                            effEnt = master
                    if getattr(effEnt, 'inCombat', 0):
                        effectLv = effEnt.getSkillEffectLv()
                        priority = effEnt.getSkillEffectPriority()
                    else:
                        effectLv = effEnt.getBasicEffectLv()
                        priority = effEnt.getBasicEffectPriority()

                    def _attachEffect():
                        fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (effectLv,
                         priority,
                         ent.model,
                         int(effectIdStr),
                         sfx.EFFECT_LIMIT,
                         duration))

                    BigWorld.callback(delayTime, _attachEffect)

    def _screenBlack(self, data):
        if gameglobal.rds.GameState > gametypes.GS_LOGIN:
            if not gameglobal.ENABLE_SKILL_SCREEN_EFFECT:
                return
            owner = BigWorld.entity(self.owner)
            if owner.getEffectLv() < gameglobal.EFFECT_MID:
                return
        dataList = data.split(':')
        gamelog.debug('dataList:', dataList[0], dataList[1], dataList[2], dataList[3], dataList[4], dataList[5])
        inTime = float(dataList[0])
        blackTime = float(dataList[1])
        outTime = float(dataList[2])
        percent = float(dataList[3])
        blackType = float(dataList[4])
        onlyPlayer = dataList[5] == '1'
        if onlyPlayer:
            if not self.isPlayer:
                return
        if blackType == 0:
            tintalt.ta_add(BigWorld.player().allModels, 'tiliang', [1.0], inTime + blackTime + outTime)
        else:
            models = []
            for id, e in BigWorld.entities.items():
                if not hasattr(e, 'allModels'):
                    continue
                models += e.allModels

            tintalt.ta_add(models, 'tiliang', [1.0], inTime + blackTime + outTime)
        BigWorld.setBlackTime(inTime, blackTime, outTime, percent, percent, percent)

    def _rotateCamera(self, data):
        if not cameraEffect.checkEnableAnimateCamera():
            return
        if self.isPlayer:
            ResMgr.purge(data)
            cameraScript = ResMgr.openSection(data)
            cameraEffect.rotateCameraFromScript(cameraScript)

    def _switchWeapon(self, data):
        gamelog.debug('bgf:weapon', data)
        if self.isPlayer:
            p = BigWorld.entities.get(self.owner)
            if p.school == const.SCHOOL_GUANGREN:
                t = data.split(':')
                if t[1] == '1':
                    p.switchWeaponState(gametypes.WEAPON_HANDFREE, False)
                if t[3] == '1':
                    p.switchWeaponState(gametypes.WEAPON_HANDFREE, False)
                if t[0] == '1':
                    p.switchWeaponState(gametypes.WEAPON_MIDATTACH, False)
                elif t[2] == '1':
                    p.switchWeaponState(gametypes.WEAPON_DOUBLEATTACH, False)

    def _showSpecSkill(self, data):
        if self.isPlayer:
            gamelog.debug('bgf:data', data)
            swfFile = data.split('/')[-1]
            gameglobal.rds.ui.showSpecSkill(swfFile)

    def _cameraAnimate(self, data):
        if not cameraEffect.checkEnableAnimateCamera():
            return
        if self.isPlayer:
            cameraEffect.startAnimateCamera(data)

    def _scaleModel(self, data):
        dataList = data.split(':')
        modelScale = float(dataList[0])
        keepTime = float(dataList[1])
        gradualScale = stateFX.GradualScale()
        gradualScale.startScale(self.owner, modelScale, keepTime)

    def _actionFreeze(self, data):
        ent = BigWorld.entity(self.owner)
        dataList = data.split(':')
        freezeNumber = float(dataList[0])
        actPlayRate = float(dataList[1])
        gamelog.debug('cueId', freezeNumber / actPlayRate, ent.id)
        ent.updateModelFreeze(freezeNumber / actPlayRate)
        ent.model.freezeType = gameglobal.FREEZE_TYPE_CUE

    def _lockRightMouse(self, data):
        if self.isPlayer:
            p = BigWorld.entities.get(self.owner)
            if data == '1':
                p.setRightMouseAble(False)
            else:
                p.setRightMouseAble(True)

    def _attachTextureEffect(self, data):
        ent = BigWorld.entity(self.owner)
        dataList = data.split(':')
        hitTintId = int(dataList[0])
        tintKeepTime = float(dataList[1])
        tintName, tintPrio, tint = skillDataInfo.getTintDataInfo(ent, hitTintId)
        if tintName:
            tintalt.ta_add(ent.allModels, tintName, [tint, BigWorld.shaderTime()], tintKeepTime)
        else:
            tintalt.ta_addHitGaoLiang(ent.allModels, gameglobal.STATE_HIGHLIGHT_BEGINTIME, gameglobal.FRESNEL_STATE_KEEPTIME, gameglobal.STATE_HIGHLIGHT_ENDTIME, tint)

    def _fullScreenEffect(self, data):
        if gameglobal.rds.GameState > gametypes.GS_LOGIN and gameglobal.SCENARIO_PLAYING != gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            if not self.isPlayer:
                return
        dataList = data.split(':')
        screenEffectPath = str(dataList[1])
        keepTime = float(dataList[0]) / gameglobal.ACTION_FRAME
        if gameglobal.ENABLE_SCREEN_EFFECT:
            ent = BigWorld.entity(self.owner)
            if ent.getEffectLv() >= gameglobal.EFFECT_MID:
                BigWorld.setScreenVisualEffects(screenEffectPath)
                if int(dataList[0]) != -1:
                    BigWorld.callback(keepTime, Functor(BigWorld.setScreenVisualEffects, None))

    def _changeActionSpeed(self, data):
        ent = BigWorld.entity(self.owner)
        dataList = data.split(':')
        actionSpeed = float(dataList[0])
        keepTime = float(dataList[1])
        self._setModelActionSpeed(ent, actionSpeed)
        BigWorld.callback(keepTime, Functor(self._setModelActionSpeed, ent, 1.0))

    def _playEffectBySchool(self, data):
        ent = BigWorld.entity(self.owner)
        if not self.isPlayer:
            return
        if ent and hasattr(ent, 'school'):
            effectId = data + str(ent.school)
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (ent.getBasicEffectLv(),
             ent.getBasicEffectPriority(),
             ent.model,
             int(effectId),
             sfx.EFFECT_LIMIT,
             gameglobal.EFFECT_LAST_TIME))

    def _playCircelEffect(self, data):
        ent = BigWorld.entity(self.owner)
        if not self.isPlayer:
            return
        dataList = data.split(':')
        skillId = int(dataList[0])
        skillLevel = int(dataList[1])
        radii = float(dataList[2])
        angle = float(dataList[3])
        force = float(dataList[4])
        speed = float(dataList[5])
        nodeName = str(dataList[6])
        try:
            keepTime = float(dataList[7])
        except:
            keepTime = 5.0

        try:
            offset = float(dataList[8])
        except:
            offset = 2.0

        clientEffect.playClientCircleEffect(skillId, skillLevel, ent, nodeName, angle, radii, speed, force, keepTime, offset)

    def _playSquareEffect(self, data):
        ent = BigWorld.entity(self.owner)
        if not self.isPlayer:
            return
        dataList = data.split(':')
        skillId = int(dataList[0])
        skillLevel = int(dataList[1])
        length = float(dataList[2])
        width = float(dataList[3])
        force = float(dataList[4])
        moveDirData = str(dataList[5]).split(',')
        moveDir = (int(moveDirData[0]), int(moveDirData[1]), int(moveDirData[2]))
        speed = float(dataList[6])
        nodeName = str(dataList[7])
        clientEffect.playClientSquareEffect(skillId, skillLevel, ent, nodeName, length, width, moveDir, speed, force)

    def _fallGround(self, data):
        ent = BigWorld.entity(self.owner)
        if ent.IsCombatUnit:
            ent.onFallGround()

    def _behitFreeze(self, data):
        ent = BigWorld.entity(self.owner)
        behitFreeze = getattr(ent, 'behitFreeze', (0, 0))
        validTime = behitFreeze[0]
        freezeTime = behitFreeze[1]
        if time.time() < validTime:
            if getattr(ent.model, 'freezeTime', 0) <= 0:
                ent.updateModelFreeze(freezeTime, gameglobal.FREEZE_TYPE_HIT)
                ent.model.quenchTime = random.uniform(0, 0.1)
                if hasattr(ent, 'freezeEffect'):
                    ent.freezeEffect(freezeTime)

    def _leftRightAppel(self, data):
        if gameglobal.gDisablePlayStartAction:
            return
        if not self.isPlayer:
            return
        owner = BigWorld.entity(self.owner)
        if hasattr(owner, '_checkNeedPlayStartAction'):
            velocity = owner.physics.velocity.length if hasattr(owner, 'physics') else 0
            if not owner._checkNeedPlayStartAction(velocity):
                return
        dataList = data.split(':')
        needLeftAction = int(dataList[0])
        needRightAction = int(dataList[1])
        if needRightAction and owner.ap.rightwardMagnitude:
            StartToRunRightAction = self.getStartToRunRightAction()
            if StartToRunRightAction:
                owner.model.action(StartToRunRightAction)()
        if needLeftAction and owner.ap.leftwardMagnitude:
            StartToRunLeftAction = self.getStartToRunLeftAction()
            if StartToRunLeftAction:
                owner.model.action(StartToRunLeftAction)()

    def _attachAndDetachLifeSkillModel(self, data):
        ent = BigWorld.entity(self.owner)
        if hasattr(ent, 'modelServer') and hasattr(ent.modelServer, 'lifeSkillModel'):
            dataList = data.split(':')
            rightAttach, leftAttach, rootAttach, rightDetach, leftDetach, rootDetach = [ int(item) for item in dataList ]
            attachType = attachedModel.DETACHED
            if rightAttach:
                attachType |= attachedModel.ATTACHED_RIGHT
            if leftAttach:
                attachType |= attachedModel.ATTACHED_LEFT
            if rootAttach:
                attachType |= attachedModel.ATTACHED_ROOT
            if attachType != attachedModel.DETACHED:
                if hasattr(ent, 'isDoingAction') and ent.isDoingAction == False:
                    return
                ent.modelServer.lifeSkillModel.attach(ent.model, attachType)
                return
            detachType = attachedModel.ATTACHED
            if rightDetach:
                detachType ^= attachedModel.ATTACHED_RIGHT
            if leftDetach:
                detachType ^= attachedModel.ATTACHED_LEFT
            if rootDetach:
                detachType ^= attachedModel.ATTACHED_ROOT
            if detachType != attachedModel.ATTACHED:
                ent.modelServer.lifeSkillModel.detach(detachType)
                return

    def _playVoice(self, data, actionName):
        ent = BigWorld.entity(self.owner)
        if ent != None:
            player = BigWorld.player()
            if ent.IsSummonedSprite:
                if not player.checkSpriteCanPlaySound(ent.id):
                    return
            if hasattr(ent, 'inHiding') and ent.inHiding() and ent != BigWorld.player():
                return
            params = data.split(':')
            try:
                onlyPlayer = int(params[1])
                needBreak = int(params[2]) if len(params) >= 3 else False
            except:
                onlyPlayer, needBreak = False, False

            soundPath = str(params[0])
            if onlyPlayer and not ent.fashion.isPlayer and not getattr(player, 'summonedSpriteInWorld', 0) == ent:
                return
            if needBreak:
                handle = Sound.playVoice(soundPath, ent.position)
                if not self.cueVoice.has_key(actionName):
                    self.cueVoice[actionName] = []
                self.cueVoice[actionName].append(handle)
            else:
                Sound.playVoice(soundPath, ent.position)
            if gameglobal.g_Print_SoundPath:
                gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SYSTEM, soundPath, '')

    def setEntityYaw(self, data):
        ent = BigWorld.entity(self.owner)
        if not ent.fashion.isPlayer:
            return
        deltaYawAngle = float(data)
        deltaYaw = math.radians(deltaYawAngle)
        targetYaw = ent.filter.yaw + deltaYaw
        ent.filter.setYaw(targetYaw)
