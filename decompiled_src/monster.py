#Embedded file name: /WORKSPACE/data/entities/client/monster.o
import random
import inspect
import BigWorld
import Math
import Sound
import formula
import gametypes
import gameglobal
import keys
import utils
import gamelog
import const
import commQuest
import clientcom
import clientUtils
from impl.impPot import ImpPot
from impl import impPot
from sfx import sfx
from iPickable import IPickable
from callbackHelper import Functor
from helpers import ufo
from helpers import action
from helpers import modelServer
from helpers import charRes
from helpers import outlineHelper
from helpers import seqTask
from helpers import tintalt
from helpers import modelRobber
from helpers import monsterAction
from iCombatUnit import ICombatUnit
from iClient import IClient
from iDisplay import IDisplay
from iCombatUnit import IMonsterCombatUnit
from guis import uiUtils, uiConst
from sMath import limit, inRange3D
from data import monster_model_client_data as MMCD
from data import monster_data as MD
from data import dialogs_data as DD
from data import preload_effect_data as PED
from data import sys_config_data as SCD
from data import monster_event_trigger_data as METD
from data import sky_wing_challenge_config_data as SWCCD
TRIGGER_TYPE_NONE = 0
TRIGGER_TYPE_FKEY = 1
TRIGGER_TYPE_BIG_FKEY = 2

class Monster(IMonsterCombatUnit, IPickable, ImpPot):
    IsMonster = True
    IsCombatUnit = True
    HITDIEFLYPROBABILTY = 30

    def __init__(self):
        super(Monster, self).__init__()
        self.bodyeff = None
        self.doingShiftAction = False
        self.isFlyMonster = False
        self.noSelected = False
        self.hitFly = False
        self.dieMotor = None
        self.bornIdleActName = None
        self.trapEventId = None
        self.questItem = None
        self.inFrameScript = False
        self.bornSoundHandler = None
        self.isLeaveWorld = False
        self.triggerEffectCallback = None
        self.triggerTrapCallback = None
        self.isBlendIn = False
        self.potIdMap = {}
        self.bloodTimer = 0
        self.plusTime = 1.0
        self.lastUpdateTime = 0
        self.targetLockConnector = None
        self.lockedEffInRange = None
        self.lockedEffId = 0
        self.oldConnectTgtId = None
        self.fbEntityNo = 0
        self.isDmgMode = False

    def prerequisites(self):
        return []

    def afterModelFinish(self):
        super(Monster, self).afterModelFinish()
        if MMCD.data.get(self.charType, {}).get('canselect', 0) and not self.noSelected and self.life == gametypes.LIFE_ALIVE:
            self.noSelected = False
        else:
            self.noSelected = True
        self.setTargetCapsUse(not self.noSelected)
        self.forceUpdateEffect()
        if gameglobal.gHideMonsterTopLogo:
            self.topLogo.hideName(True)
        collideRadiusRatio = MMCD.data.get(self.charType, {}).get('collide', 0.0)
        if collideRadiusRatio > 0.0:
            opacityVal, _ = self.getOpacityValue()
            if opacityVal == gameglobal.OPACITY_FULL:
                self.collideWithPlayer = True
                self.am.collideWithPlayer = True
                self.am.collideRadius = collideRadiusRatio
            else:
                self.collideWithPlayer = False
                self.am.collideWithPlayer = False
        if self.inDying:
            self.noSelected = False
            self.setTargetCapsUse(not self.noSelected)
        if self.keepYaw:
            self.filter = BigWorld.DumbFilter()
        self.isFlyMonster = MD.data.get(self.charType, {}).get('flyMonster', 0)
        if self.isFlyMonster:
            self.filter = BigWorld.AvatarFilter()
        popDist = MMCD.data.get(self.charType, {}).get('popDist', 0.0)
        if popDist > 0:
            self.filter.popDist = popDist
        if MMCD.data.get(self.charType, {}).get('boredByServer', 0):
            self.fashion.setBoredController(2)
        if self.monsterStrengthType in gametypes.MONSTER_BOSS_TYPE:
            self.preloadEffect()
            needExpandVB = MMCD.data.get(self.charType, {}).get('needExpandVB', False)
            if needExpandVB and self.model:
                self.model.expandVisibilityBox(1000)
        self.preloadAction()
        if self.applyTints:
            self._modifyTints()
        if METD.data.has_key(self.charType):
            self._addEventTrap()
        if MMCD.data.get(self.charType, {}).get('latencyOptimize', 0):
            if hasattr(self.filter, 'latencyFrames'):
                self.filter.latencyFrames = 0.1
        if self.isSceneObj():
            self.model.isSceneObj = True
        clientEntityId = getattr(self, 'clientEntityId', None)
        if clientEntityId:
            BigWorld.player().hideClientShip(clientEntityId)
        if self.isShowConnectorFlag and self.getConnectorTgtId():
            self.updateConnectTgtId(self.getConnectorTgtId())
            self.addConnectEff()
        if MMCD.data.get(self.charType, {}).get('extraTint', ''):
            tintalt.ta_add(self.allModels, MMCD.data.get(self.charType, {}).get('extraTint', ''))

    def _addEventTrap(self):
        eventDataList = METD.data.get(self.charType, {})
        self.potIdMap = {}
        for index, eventData in enumerate(eventDataList):
            radii = eventData.get('radii', 0)
            if radii:
                potId = BigWorld.addPot(self.matrix, radii, self.entitiesChanged)
                self.potIdMap[potId] = index
                self.triggerTrap(True, potId)

        self._addTriggerEff()

    def _delEventTrap(self):
        potIdMap = getattr(self, 'potIdMap', {})
        for potId in potIdMap.iterkeys():
            BigWorld.delPot(potId)
        else:
            self.potIdMap = {}

        if gameglobal.rds.ui.pressKeyF.monster and gameglobal.rds.ui.pressKeyF.monster.id == self.id:
            self.triggerTrap(False)

    def _addTriggerEff(self):
        if not self.inWorld:
            return
        if commQuest.canTriggerEffect(BigWorld.player(), self):
            mmcd = MMCD.data.get(self.charType, {})
            triggerEff = mmcd.get('triggerEff', 0)
            if triggerEff:
                if triggerEff in self.attachFx:
                    return
                effScale = mmcd['effScale'] if mmcd.has_key('effScale') else mmcd.get('modelScale', 1)
                fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getEquipEffectLv(),
                 self.getEquipEffectPriority(),
                 self.model,
                 triggerEff,
                 sfx.EFFECT_UNLIMIT))
                if fxs:
                    for fx in fxs:
                        fx.scale(effScale, effScale, effScale)

                    self.addFx(triggerEff, fxs)

    def entitiesChanged(self, enteredTrap, handle = -1):
        if not self.inWorld:
            return
        eventDataList = METD.data.get(self.charType)
        if not eventDataList:
            return
        index = None
        if handle != -1:
            index = self.potIdMap.get(handle)
            eventDataList = (eventDataList[index],)
        for eventData in eventDataList:
            if eventData.get('triggerType') and self.trapCallback(enteredTrap, handle):
                break
            elif not eventData.has_key('actionId') and not eventData.has_key('useItem') or eventData.get('auto'):
                eventIndex = commQuest.canTriggerEvent(BigWorld.player(), self, index)
                if eventIndex >= 0 and enteredTrap:
                    BigWorld.player().cell.triggerMonsterEvent(self.id, eventIndex)
                    break

    def triggerTrap(self, enteredTrap, handle = -1):
        eventDataList = METD.data.get(self.charType)
        if not eventDataList:
            return
        if handle != -1:
            index = self.potIdMap.get(handle)
            eventDataList = (eventDataList[index],)
        radii = 0
        for eventData in eventDataList:
            radii = eventData.get('radii')
            if radii:
                break
        else:
            return

        if not inRange3D(radii, BigWorld.player().position, self.position) and not self.isLeaveWorld:
            return
        self.entitiesChanged(enteredTrap, handle)

    def trapCallback(self, enteredTrap, handle = -1):
        if not self.inWorld:
            return False
        entities = []
        p = BigWorld.player()
        triggerType = TRIGGER_TYPE_NONE
        for entity in BigWorld.entities.values():
            if not isinstance(entity, Monster):
                continue
            if not entity.inWorld:
                continue
            if entity.charType not in METD.data:
                continue
            if getattr(self, 'isLeaveWorld'):
                continue
            iEvent = commQuest.canTriggerEvent(BigWorld.player(), entity)
            if iEvent < 0:
                continue
            entity.triggerEventIndex = iEvent
            eventData = METD.data[entity.charType][iEvent]
            notShowTrigInCD = eventData.get('notShowTrigInCD', 0)
            if notShowTrigInCD and BigWorld.player().getServerTime() < entity.nextTriggerEventTime.get(iEvent, 0):
                continue
            radii = eventData.get('radii', 0)
            if not (entity.position - BigWorld.player().position).lengthSquared <= radii * radii:
                continue
            if not eventData.get('triggerType', 0):
                continue
            entities.append(entity)

        if not enteredTrap and self in entities:
            entities.remove(self)
        if not enteredTrap:
            if p.groupNUID and p.groupActionState:
                eventIndex = commQuest.getGroupActionMonsterEventIndex(self.charType)
                if eventIndex != -1:
                    p.cell.cancelMonsterEvent(self.id, eventIndex)
                    p.groupActionState = 0
        p.monsterTrapCallback(entities)
        return entities

    def preloadEffect(self):
        ped = PED.data.get(self.fashion.modelID, {})
        fxs = list(ped.get('preloadEffect', []))
        for fxId in fxs:
            sfx.gEffectMgr.preloadFx(fxId, self.getEffectLv())

    def preloadAction(self):
        hitActions = [str(gameglobal.MONSTER_HIT_ACTION_START), str(gameglobal.MONSTER_HIT_ACTION_END)]
        if self.model and hasattr(self.model, 'resideActions'):
            self.model.resideActions(*hitActions)

    def set_mp(self, old):
        super(Monster, self).set_mp(old)
        gameglobal.rds.ui.bossEnergy.setEnergy(self.id, int(100 * self.mp / self.mmp))

    def set_mmp(self, old):
        super(Monster, self).set_mmp(old)
        if self.mp > self.mmp:
            self.mp = self.mmp

    def leaveWorld(self):
        if hasattr(self.model, 'fadeShader'):
            self.model.fadeShader = None
        modelRobber.getInstance().tryReturnModel(self)
        if self.isRealModel:
            seqTask.modelMemoryCtrl().decMonsterModel()
        if self.dieMotor:
            if self.model and self.model.motors and self.dieMotor in self.model.motors:
                self.model.delMotor(self.dieMotor)
            self.dieMotor = None
        self.bodyeff = None
        self.doingShiftAction = False
        self.bornAction = None
        self.clearBodyEffect()
        self.isFlyMonster = False
        self.isLeaveWorld = True
        self.removeAllFx()
        BigWorld.player().removeInDyingEntityId(self.id)
        clientEntityId = getattr(self, 'clientEntityId', None)
        if clientEntityId:
            BigWorld.player().showClientShip(clientEntityId)
        for trapLengthType in xrange(1, impPot.TRAP_MAX_NUM):
            trapEventIdName = 'trapEventId'
            if trapLengthType != 1:
                trapEventIdName = trapEventIdName + str(trapLengthType)
            if hasattr(self, trapEventIdName):
                if getattr(self, trapEventIdName):
                    self.questItem = None
                    if gameglobal.rds.ui.npcSlot.isShow and gameglobal.rds.ui.npcSlot.type == uiConst.SLOT_FROM_MONSTER:
                        self.dealTrapOutEvent(trapLengthType)

        for trapLengthType in xrange(1, impPot.TRAP_MAX_NUM):
            trapSoundHandleName = 'trapSoundHandle'
            if trapLengthType != 1:
                trapSoundHandleName = trapSoundHandleName + str(trapLengthType)
            if hasattr(self, trapSoundHandleName):
                if getattr(self, trapSoundHandleName):
                    self.dealTrapOutEvent(trapLengthType)

        super(Monster, self).leaveWorld()
        self.delTrapEvent()
        soundId = MMCD.data.get(self.charType, {}).get('bornSoundId')
        if soundId:
            gameglobal.rds.sound.stopSound(soundId, self.bornSoundHandler)
        self._delEventTrap()
        if self.triggerEffectCallback:
            BigWorld.cancelCallback(self.triggerEffectCallback)
            self.triggerEffectCallback = None
        mdData = MD.data.get(self.charType, {})
        if mdData.get('energy') == 1:
            gameglobal.rds.ui.bossEnergy.hideUI(self.id)
        if mdData.get('groupMonster') == 1:
            gameglobal.rds.ui.monsterBlood.removeMonster(self.id)
        if mdData.get('needFightBlood'):
            gameglobal.rds.ui.fightObserve.removeMonster(self)
        p = BigWorld.player()
        if not clientcom.bfDotaAoIInfinity() and p.isEnemy(self) and getattr(self, 'isBattleFieldDotaTower', 0) and p.isInBfDota() and not p.vehicleId:
            p.cell.onMyLeaveRangeInBattleFieldDota()
        enemySet = p.bfDotaEntityIdRecord.get(const.DOTA_ENTITY_TYPE_ENEMY, set())
        enemySet and self.id in enemySet and enemySet.remove(self.id)
        teammMateSet = p.bfDotaEntityIdRecord.get(const.DOTA_ENTITY_TYPE_TEAMMATE, set())
        teammMateSet and self.id in teammMateSet and teammMateSet.remove(self.id)
        if self.bloodTimer:
            BigWorld.cancelCallback(self.bloodTimer)
            self.bloodTimer = 0
        if getattr(self, 'fallenRedGuardFlag', None):
            gameglobal.rds.ui.killFallenRedGuardRank.leaveMonster(self)
        isMonsterDead = self.hp <= 0
        if not isMonsterDead:
            if gameglobal.rds.ui.wingWorldAllSoulsRank.isWingSoulBoss(self) and hasattr(p, 'onLeaveSoulBossTrap'):
                age = formula.getWingCityGroupId(p.spaceNo)
                avatarId = getattr(self, 'charType', -1)
                bossId = gameglobal.rds.ui.wingWorldAllSoulsRank.getBossId(age, avatarId)
                p.onLeaveSoulBossTrap(bossId, avatarId)
        self.updateConnectTgtId(0)
        self.delConnnectEff()

    def enterWorld(self):
        if self.hideNpcId and modelRobber.getInstance().tryRobModel(self):
            self.initYaw = self.yaw
        else:
            super(Monster, self).enterWorld()
        if MMCD.data.get(self.charType, {}).get('canselect', 0) and not self.noSelected and self.life == gametypes.LIFE_ALIVE:
            self.noSelected = False
        else:
            self.noSelected = True
        self.setTargetCapsUse(not self.noSelected)
        if self.inDying:
            BigWorld.player().addInDyingEntityId(self.id)
        self.addTrapEvent()
        soundId = MMCD.data.get(self.charType, {}).get('bornSoundId')
        self.isDmgMode = bool(MMCD.data.get(self.charType, {}).get('isDmgMode', False))
        if soundId:
            self.bornSoundHandler = gameglobal.rds.sound.playSound(soundId, self)
        mdData = MD.data.get(self.charType, {})
        if mdData.get('energy') == 1:
            name = mdData.get('energyName')
            color = mdData.get('energyColor')
            gameglobal.rds.ui.bossEnergy.show(self.id, name, color, int(100 * self.mp / self.mmp))
        if mdData.get('groupMonster') == 1:
            gameglobal.rds.ui.monsterBlood.addMonster(self.id, self.roleName, self.hp, self.mhp)
            if gameglobal.rds.ui.monsterBlood.mediator == None:
                gameglobal.rds.ui.monsterBlood.show()
        if mdData.get('needFightBlood'):
            gameglobal.rds.ui.fightObserve.addMonster(self)
            if gameglobal.rds.ui.fightObserve.monsterBloodMediator == None:
                gameglobal.rds.ui.fightObserve.showMonsterBlood()
        p = BigWorld.player()
        self.isBattleFieldDotaTower = MD.data.get(self.charType, {}).get('isBattleFieldDotaTower', 0)
        isDotaPosTagMonster = MD.data.get(self.charType, {}).get('isBattleFieldDotaPosTag', 0)
        if isDotaPosTagMonster and p.isInBfDota() and not p.isEnemy(self):
            p.bfDotaEntityIdRecord.setdefault(const.DOTA_ENTITY_TYPE_TEAMMATE, set()).add(self.id)
        if self.isBattleFieldDotaTower and not p.isEnemy(self):
            p.bfDotaEntityIdRecord.setdefault(const.DOTA_ENTITY_TYPE_TEAMMATE, set()).add(self.id)
        if not clientcom.bfDotaAoIInfinity() and p.isEnemy(self) and self.isBattleFieldDotaTower and p.isInBfDota() and not p.vehicleId:
            p.cell.onMyEnterRangeInBattleFieldDota()
        if getattr(self, 'fallenRedGuardFlag', None) and gameglobal.rds.configData.get('enableKillFallenRedGuard', False):
            gameglobal.rds.ui.killFallenRedGuardRank.enterMonster(self.fallenRedGuardFlag)
        if gameglobal.rds.ui.wingWorldAllSoulsRank.isWingSoulBoss(self) and hasattr(p, 'onEnterSoulBossTrap'):
            age = formula.getWingCityGroupId(p.spaceNo)
            avatarId = getattr(self, 'charType', -1)
            bossId = gameglobal.rds.ui.wingWorldAllSoulsRank.getBossId(age, avatarId)
            p.onEnterSoulBossTrap(bossId, avatarId)
        if self.isShowConnectorFlag:
            self.lockedEffId = self.getConnectorSfxId()
            self.lockedEffInRange = clientUtils.pixieFetch(sfx.getPath(self.lockedEffId))
            self.lockedEffInRange.setAttachMode(0, 1, 0)
            self.lockedEffInRange.force()
            if self.getConnectorTgtId():
                self.updateConnectTgtId(self.getConnectorTgtId())
        if getattr(self.cell, 'syncFbEntityNo', None):
            self.cell.syncFbEntityNo()

    def getConnectorSfxId(self):
        md = MD.data.get(self.charType, {})
        connectorType = md.get('connectorType', 0)
        sfxId = 0
        if connectorType != 0:
            sfxId = SCD.data.get('targetLockedEffects', {}).get(connectorType, 0)
        else:
            sfxId = SCD.data.get('monsterTargetLockedEffectInRange', 0)
        return sfxId

    def set_inCombat(self, oldInCombat):
        super(Monster, self).set_inCombat(oldInCombat)
        if self.inCombat:
            self.playMonsterSoundByMMCD('enterCombatSound')
        else:
            self.playMonsterSoundByMMCD('leaveCombatSound')

    def attack(self, targetId):
        pass

    def set_life(self, old):
        super(Monster, self).set_life(old)
        if self.life == gametypes.LIFE_DEAD:
            self.collideWithPlayer = False
            if hasattr(self, 'am'):
                self.am.collideWithPlayer = False
            self.delConnnectEff()
            self.playMonsterSoundByMMCD('selfDieSound')
        elif self.life == gametypes.LIFE_ALIVE:
            collideRadiusRatio = MMCD.data.get(self.charType, {}).get('collide', 0.0)
            if collideRadiusRatio > 0.0:
                opacityVal, _ = self.getOpacityValue()
                if opacityVal == gameglobal.OPACITY_FULL:
                    self.collideWithPlayer = True
                    self.am.collideWithPlayer = True
                    self.am.collideRadius = collideRadiusRatio
                else:
                    self.collideWithPlayer = False
                    self.am.collideWithPlayer = False
            self.setTargetCapsUse(True)
            if self.model and len(self.model.motors) > 1:
                self.model.motors = []
                self.model.motors = [self.am]
                self.am.enable = True
            self.addConnectEff()
        self.doAttachEffect()

    def hide(self, fHide, retainTopLogo = False):
        if not self.inWorld:
            return
        super(Monster, self).hide(fHide, retainTopLogo)

    def setSelected(self, flag):
        self.noSelected = flag
        self.setTargetCapsUse(not self.noSelected)

    def shiftModel(self, charType = 10004, scale = 1.0):
        itemData = {'model': charType,
         'dye': 'Default'}
        modelServer.loadModelByItemData(self.id, gameglobal.URGENT_THREAD, self.shitfModelFinished, itemData)
        self.modelScale = scale

    def shitfModelFinished(self, model):
        self.modelServer._singlePartModelFinish(model)
        self.model.scale = (self.modelScale, self.modelScale, self.modelScale)
        self.resetTopLogo()

    def die(self, killer, clientSkillInfo = None):
        self.setTargetCapsUse(False)
        if clientSkillInfo and not self.isAvatarMonster() and not self.isMultiPartMonster():
            hitDieFlyAction = self.fashion.getHitDieFlyName()
            monsterShape = MMCD.data.get(self.charType, {}).get('monsterShape', None)
            skillForce = clientSkillInfo.getSkillData('skillForce', None)
            if hitDieFlyAction and monsterShape and skillForce and skillForce + 3 > monsterShape and self.fashion.doingActionType() not in [action.MOVING_ACTION,
             action.MOVINGSTOP_ACTION,
             action.AFTERMOVE_ACTION,
             action.AFTERMOVESTOP_ACTION]:
                self.hitDieFly(killer, hitDieFlyAction, clientSkillInfo, monsterShape, skillForce)
                return
        super(Monster, self).die(killer, clientSkillInfo)

    def hitDieFly(self, killer, hitDieFlyAction, clientSkillInfo, monsterShape, skillForce):
        self.updateModelFreeze(-1.0)
        self.fashion.stopAllActions()
        self.hitFly = True
        mot = BigWorld.Slider()
        flyLength = 9 + 3 * (skillForce - monsterShape)
        if flyLength >= 15:
            flyLength = 12
        if skillForce >= monsterShape:
            dif = skillForce - monsterShape + 1
            if dif > 2:
                dif = 2
            flyLength = flyLength + random.randint(-dif, dif)
        mot.keepTime = MMCD.data.get(self.charType, {}).get('hitDieFlyTime', 0.6)
        mot.speedAttenu = 0
        if monsterShape / 2 > 1:
            mot.speedAttenu = -monsterShape / 2
        mot.rotateSpeed = 0
        v = flyLength / mot.keepTime - 0.5 * mot.speedAttenu * mot.keepTime
        delayFlyTime = MMCD.data.get(self.charType, {}).get('delayFlyTime', 0.6)
        BigWorld.callback(delayFlyTime, Functor(self._resetMotorFlySpeed, mot, v * 0.5))
        mot.speed = v
        dirp = self.position - killer.position if killer and killer.inWorld else Math.Vector3(0, 0, 0)
        dirp.normalise()
        mot.slideDir = dirp
        self.dieMotor = mot
        self.am.enable = False
        if hitDieFlyAction in self.fashion.getActionNameList():
            self.fashion.setDoingActionType(action.HIT_DIEFLY_ACTION)
            self.model.action(hitDieFlyAction)(0.0, None, 0, 1.0, 9999.0)
            dieTime = self.fashion.getActionTime(hitDieFlyAction)
            BigWorld.callback(dieTime, self.playSpecialDie)
        self.model.addMotor(mot)
        if killer and killer.inWorld:
            self.afterDieEffect(self)

    def _resetMotorFlySpeed(self, motor, speed):
        motor.speed = speed

    def returnToNormal(self):
        pass

    def doAttachEffect(self):
        pass

    def check(self):
        if self.life != gametypes.LIFE_DEAD:
            return False
        return True

    def switchFilter(self, flag):
        if flag == 2:
            self.inFrameScript = True
            self.filter = BigWorld.AvatarFilter()
        else:
            self.inFrameScript = False
            self.filter = BigWorld.AvatarDropFilter()

    def playAction(self, num):
        if not self.inCombat and self.life == gametypes.LIFE_ALIVE:
            self.playActionEvent(num)

    def setYaw(self, yaw):
        BigWorld.callback(1.0, Functor(self._delaySetYaw, yaw))

    def _delaySetYaw(self, yaw):
        if self.inWorld:
            self.filter.setYaw(yaw)

    def afterDieAction(self):
        super(Monster, self).afterDieAction()
        if hasattr(self, 'topLogo') and self.topLogo != None:
            self.topLogo.hide(True)
        if not self.inWorld or not self.fashion:
            return
        self.playDieSpecialEffsAlone()
        self.fashion.attachUFO(ufo.UFO_NULL)
        data = MMCD.data.get(self.charType, None)
        if data != None and data.has_key('deadModel'):
            try:
                modelpath = gameglobal.charRes + str(data['deadModel']) + '/' + str(data['deadModel']) + '.model'
                charRes.getSimpleModel(modelpath, None, self._afterDeadModelFinished)
            except ValueError:
                gamelog.error('Error can not find body_model', data['deadModel'])
                return

    def _afterDeadModelFinished(self, model):
        oldModel = self.model
        oldYaw = oldModel.yaw
        self.model = model
        self.model.scale = self.getModelScale()
        self.model.yaw = oldYaw
        self.model.position = self.position
        try:
            model.action('2551')().action('2561')()
        except:
            gamelog.error('Error can not find death ation,model name:', model.sources)

        BigWorld.callback(1, Functor(self._bodyLeaveWorld, oldModel))

    def clearBodyEffect(self):
        if self.bodyeff:
            for i in self.bodyeff:
                i.stop()

            self.bodyeff = None

    def _bodyLeaveWorld(self, model):
        BigWorld.player().delModel(model)

    def enterTopLogoRange(self, rangeDist = -1):
        if not self.firstFetchFinished:
            return
        if self.getOpacityValue()[0] == gameglobal.OPACITY_HIDE:
            return
        super(Monster, self).enterTopLogoRange(rangeDist)
        if self.topLogo and self.fashion:
            self.fashion.setHeadTracker(self.inGuard)
            h = self.getTopLogoHeight()
            if h > 0:
                self.topLogo.setHeight(h)
        if self.topLogo:
            if gameglobal.gHideMonsterName:
                self.topLogo.hideName(True)
            elif not self.inCombat and self.hideTopLogoOutCombat():
                self.topLogo.hideName(True)
        mdata = MMCD.data.get(self.charType, {})
        musicParma = mdata.get('musicParam', None)
        if musicParma:
            value = mdata.get('musicValue', 0)
            Sound.setMusicParam(musicParma, value)

    def leaveTopLogoRange(self, rangeDist = -1):
        super(Monster, self).leaveTopLogoRange(rangeDist)
        mdata = MMCD.data.get(self.charType, {})
        musicParma = mdata.get('musicParam', None)
        if musicParma:
            Sound.setMusicParam(musicParma, 0)

    def setRenderFlag(self, flag):
        if self.pickModel:
            model = self.pickModel
        else:
            model = self.model
        if model == None or self.fashion == None:
            return
        model.renderFlag = flag

    def explodeEffect(self, effectNo):
        sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
         self.getSkillEffectPriority(),
         self.model,
         int(effectNo),
         sfx.EFFECT_LIMIT,
         gameglobal.EFFECT_LAST_TIME))

    def getSkillEffectPriority(self):
        if BigWorld.player().isRealInFuben():
            return gameglobal.EFF_PLAYER_SKILL_PRIORITY
        return super(Monster, self).getSkillEffectPriority()

    def getBuffEffectPriority(self, host):
        if BigWorld.player().isRealInFuben():
            return gameglobal.EFF_PLAYER_BUFF_PRIORITY
        return gameglobal.EFF_MONSTER_BUFF_PRIORITY

    def beHit(self, host, damage = None, callback = None, forceBeHitAct = False, clientSkillInfo = None):
        if self.doingShiftAction:
            return
        super(Monster, self).beHit(host, damage, callback, forceBeHitAct, clientSkillInfo)

    def resetShiftAction(self):
        self.doingShiftAction = False

    def playActions(self, actNames):
        if type(actNames) != tuple or len(actNames) < 1:
            return
        if self.life == gametypes.LIFE_DEAD:
            return
        if not self.fashion:
            return
        if self.fashion.doingActionType() in (action.DEAD_ACTION, action.DYING_ACTION):
            return
        self.fashion.stopAction()
        self.fashion.playAction(list(actNames), action.PROGRESS_ACTION)

    def stopPlayAction(self):
        self.fashion.stopAction()

    def playJumpAction(self, actNames):
        if not self.inWorld:
            return
        if not self.fashion:
            return
        isMovement = 0
        hideInJump = 0
        if len(actNames) == 2:
            jumpAct, jumpStopAct = actNames
        elif len(actNames) == 3:
            jumpAct, jumpStopAct, isMovement = actNames
        elif len(actNames) == 4:
            jumpAct, jumpStopAct, isMovement, hideInJump = actNames
        beLocked = False
        if hideInJump:
            beLocked = BigWorld.player().targetLocked.id == self.id if BigWorld.player().targetLocked else False
            self.hide(True)
        playSeq = []
        playSeq.append((jumpAct,
         [],
         action.MOVING_ACTION,
         isMovement,
         1.0,
         None))
        self.fashion.playActionWithFx(playSeq, action.MOVING_ACTION, Functor(self._endJumpAction, jumpAct, jumpStopAct, beLocked), False, keep=0.1)
        BigWorld.callback(2.0, Functor(self._refreshOpacityState, beLocked))

    def _endJumpAction(self, jumpAct, jumpStopAct, beLocked):
        self._refreshOpacityState(beLocked)
        if self.fashion.doingActionType() in [action.HITBACK_ACTION] or self.model.freezeTime > 0.0:
            return
        self.fashion.stopActionByName(self.model, jumpAct)
        playSeq = []
        playSeq.append((jumpStopAct,
         [],
         action.MOVING_ACTION,
         0,
         1.0,
         None))
        self.fashion.playActionWithFx(playSeq, action.MOVING_ACTION, None, False)

    def _refreshOpacityState(self, beLocked):
        if not self.inWorld:
            return
        self.refreshOpacityState()
        if beLocked:
            p = BigWorld.player()
            if not p.targetLocked:
                p.lockTarget(self)

    def refreshOpacityState(self):
        super(Monster, self).refreshOpacityState()
        if gameglobal.rds.ui.pressKeyF.monster and gameglobal.rds.ui.pressKeyF.monster.id == self.id:
            self.checkFKey()

    def playSpecialIdleAction(self):
        if not self.inWorld:
            return
        if not self.fashion:
            return
        self.fashion.playBoredAction()

    def stopActions(self):
        if self.inWorld:
            if action.FUKONG_START_ACTION <= self.fashion.doingActionType() <= action.FAINT_STOP_ACTION or self.fashion.doingActionType() == action.STANDUP_ACTION:
                return
            self.fashion.stopAction()
            BigWorld.callback(0.2, Functor(self._resetSkeleton))

    def _resetSkeleton(self):
        if self.model and hasattr(self.model, 'resetSkeleton'):
            self.model.resetSkeleton()

    def getModelScale(self):
        md = MMCD.data.get(self.charType, {})
        scale = md.get('modelScale', 1.0)
        if type(scale) == tuple:
            x, y, z = float(scale[0]), float(scale[1]), float(scale[2])
        else:
            x, y, z = float(scale), float(scale), float(scale)
        self.model.scale = (x, y, z)
        return (x, y, z)

    def playEffect(self, effectId, targetPos = None, pitch = 0, yaw = 0, roll = 0, maxDelayTime = -1, scale = 1.0):
        if targetPos is None:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
             self.getSkillEffectPriority(),
             self.model,
             effectId,
             sfx.EFFECT_LIMIT,
             maxDelayTime))
        else:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (self.getSkillEffectLv(),
             self.getSkillEffectPriority(),
             self.model,
             effectId,
             sfx.EFFECT_LIMIT,
             targetPos,
             pitch,
             yaw,
             roll,
             maxDelayTime))
        if fx:
            for fxItem in fx:
                fxItem.scale(scale, scale, scale)

    def moveCamera(self, tracks):
        pass

    def changeMonsterModel(self, changeType):
        self.modelServer.changeModelFromData(changeType)

    def monsterDying(self, charType):
        p = BigWorld.player()
        p.onMonsterDying(charType)

    def flyOffCliff(self, targetPosition, moveTime, downTime):
        gamelog.debug('jorsef2: flyOffCliff', targetPosition)
        self.am.enable = False
        self.downCliff = True
        self.fashion.stopAllActions()
        checkHeight = [3.0,
         5.0,
         10.0,
         15.0,
         20.0,
         30.0,
         50.0,
         100.0]
        startPos = self.model.position
        for height in checkHeight:
            tmpPosition = (targetPosition[0], targetPosition[1] + height, targetPosition[2])
            if not self._checkCollide(startPos, tmpPosition):
                endPos = tmpPosition + Math.Vector3(0, 1.5, 0)
                mot = BigWorld.Slider()
                mot.speed = 16
                mot.keepTime = 10
                mot.speedAttenu = 5
                mot.gravity = 4.9
                dirp = endPos - startPos
                dirp.normalise()
                mot.slideDir = dirp
                mot.slidingCallback = self.collideCallback
                self.model.addMotor(mot)
                self.dieMotor = mot
                break

    def collideCallback(self, collide):
        gamelog.debug('jorsef2: collideCallback', self.id, collide)
        if self.model and self.model.inWorld:
            self.model.delMotor(self.dieMotor)
            self.playDieAction()

    def _checkCollide(self, startPos, endPos):
        gamelog.debug('jorsef2: _checkCollide', self.id, startPos, endPos)
        p = BigWorld.player()
        dropPos = BigWorld.collide(p.spaceID, (startPos[0], startPos[1] + 0.01, startPos[2]), (endPos[0], endPos[1], endPos[2]))
        gamelog.debug('jorsef2: dropPos', self.id, dropPos)
        if dropPos:
            return True
        return False

    def flyOffCliff1(self, targetPosition, moveTime, downTime):
        gamelog.debug('jorsef2: flyOffCliff', self.id, targetPosition, moveTime, downTime)
        self.am.enable = False
        self.downCliff = True
        self.fashion.stopAllActions()
        candidatePoints = BigWorld.findDropPoint(self.spaceID, targetPosition + Math.Vector3(0, 5, 0))
        if candidatePoints:
            candidate = candidatePoints[0]
        if abs(targetPosition[1] - candidate[1]) < 10:
            self.fakeDown = True
        targetPosition = (targetPosition[0], targetPosition[1] + 2, targetPosition[2])
        launcher = BigWorld.Rlauncher()
        mat = Math.Matrix()
        mat.setTranslate((self.position[0], self.position[1] + 2, self.position[2]))
        launcher.speed = 12
        launcher.target = mat
        launcher.proximityCallback = Functor(self._downCliff, launcher, targetPosition)
        self.model.addMotor(launcher)

    def _downCliff(self, launcher, targetPosition):
        gamelog.debug('jorsef: _downCliff', targetPosition)
        self.model.delMotor(launcher)
        self.fashion.playActionSequence(self.model, ('1819',), None)
        startPos = self.model.position
        endPos = targetPosition + (targetPosition - startPos) * random.uniform(0.5, 5)
        mot = BigWorld.Slider()
        mot.speed = 16
        mot.keepTime = 2
        mot.speedAttenu = 5
        dirp = endPos - startPos
        dirp.normalise()
        mot.slideDir = dirp
        self.model.addMotor(mot)

    def set_hp(self, old):
        self.charType == SWCCD.data.get('challengeBossId', 0) and self.resetSkyWingMonsterHpAndMhp()
        super(Monster, self).set_hp(old)
        eventDataList = METD.data.get(self.charType, ())
        for eventData in eventDataList:
            if not eventData.has_key('hpPercent'):
                continue
            if self.hp > 0 and eventData and eventData['hpPercent'] < 1:
                lastFTriggerHp = getattr(self, '_lastFTriggerHp', self.mhp)
                hpFTriggerThreshold = 0.05
                if self.hp > lastFTriggerHp:
                    setattr(self, '_lastFTriggerHp', self.mhp)
                if (lastFTriggerHp - self.hp) * 1.0 / self.mhp >= hpFTriggerThreshold:
                    setattr(self, '_lastFTriggerHp', self.hp)
                    self.triggerTrap(True)

        if gameglobal.rds.ui.bossBlood.bloodOwner == self.id:
            if old - self.hp > 0 and old <= self.mhp:
                gameglobal.rds.ui.bossBlood.minusBlood(old - self.hp)
            else:
                gameglobal.rds.ui.bossBlood.initHp(self.hp, self.mhp, '', self.isDmgMode)
        self.showMonsterIcon()
        gameglobal.rds.ui.monsterBlood.setHp(self.id, self.hp, self.mhp)
        gameglobal.rds.ui.fightObserve.setHp(self.id, self.hp, self.mhp)
        clientcom.setDotaEntityBlood(self)

    def set_mhp(self, old):
        self.charType == SWCCD.data.get('challengeBossId', 0) and self.resetSkyWingMonsterHpAndMhp()
        super(Monster, self).set_mhp(old)
        if gameglobal.rds.ui.bossBlood.bloodOwner == self.id:
            gameglobal.rds.ui.bossBlood.initHp(self.hp, self.mhp, '', self.isDmgMode)
        gameglobal.rds.ui.fightObserve.setHp(self.id, self.hp, self.mhp)
        clientcom.setDotaEntityBlood(self)

    def set_lockedId(self, old):
        gamelog.debug('@hjx target#set_lockedId:', old, self.lockedId)
        if old == 0 and self.lockedId == 0:
            return
        if self.lockedId == BigWorld.player().id and hasattr(self, 'refreshPotKeepEffect'):
            self.refreshPotKeepEffect()
        if BigWorld.player().targetLocked == self:
            lockedId = getattr(self, 'lockedId', None)
            if lockedId != None:
                showBlood = uiUtils._isNeedShowBossBlood(self.charType)
                if self.inWorld and (showBlood == 1 and not self.inDying or showBlood == 2 and self.inDying):
                    gamelog.debug('@hjx target#set_lockedId1:', lockedId)
                    gameglobal.rds.ui.bossBlood.setBossTargetLockName(self.lockedId)
                else:
                    gameglobal.rds.ui.target.setTargetLockName(self.lockedId)
        if gameglobal.rds.ui.focusTarget.focusTarId == self.id:
            lockedId = getattr(self, 'lockedId', None)
            if lockedId != None:
                gameglobal.rds.ui.focusTarget.setTargetLockName(lockedId)
        if self.isShowConnectorFlag:
            self.updateConnectTgtId(self.getConnectorTgtId())
        self.refreshConnectEff()

    def updateConnectTgtId(self, newTgtId):
        oldTgtMonsterList = sfx.G_MONSTER_LOCKED.get(self.oldConnectTgtId, [])
        self.id in oldTgtMonsterList and oldTgtMonsterList.remove(self.id)
        if not oldTgtMonsterList and sfx.G_MONSTER_LOCKED.has_key(self.oldConnectTgtId):
            sfx.G_MONSTER_LOCKED.pop(self.oldConnectTgtId)
        self.oldConnectTgtId = newTgtId
        if newTgtId:
            sfx.G_MONSTER_LOCKED.setdefault(newTgtId, []).append(self.id)

    def lockEffect(self):
        showBlood = uiUtils._isNeedShowBossBlood(self.charType)
        gamelog.debug('@hjx target#Monster#lockEffect:', showBlood)
        if self.inWorld and (showBlood == 1 and not self.inDying or showBlood == 2 and self.inDying):
            if not gameglobal.rds.ui.isHideAllUI():
                gameglobal.rds.ui.bossBlood.showBossBlood(self.id, True)
            else:
                gameglobal.rds.ui.bossBlood.showBossBlood(self.id, False)
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_BOSSBLOOD, True)
            if self.inDying:
                gameglobal.rds.ui.bossBlood.setName(self.roleName + ' ±ôËÀ')
            else:
                gameglobal.rds.ui.bossBlood.setName(self.roleName)
            gameglobal.rds.ui.bossBlood.setPartName('')
            gameglobal.rds.ui.bossBlood.setLevel(self)
            gameglobal.rds.ui.bossBlood.initHp(self.hp, self.mhp, '', self.isDmgMode)
            gameglobal.rds.ui.bossBlood.setBossTargetLockName(self.lockedId)
        if self.inDying:
            gameglobal.rds.ui.target.hideTargetUnitFrame()

    def unlockEffect(self):
        if self.inWorld and gameglobal.rds.ui.bossBlood.bloodOwner == self.id:
            gameglobal.rds.ui.bossBlood.hideBossBlood()

    def needShowBossBlood(self):
        md = MMCD.data.get(self.charType, None)
        if md:
            showBlood = md.get('showBlood', 0)
            return showBlood
        else:
            return 0

    def set_specialStateVal(self, old):
        gameglobal.rds.ui.bossInfo.review()
        if BigWorld.player().targetLocked == self:
            gameglobal.rds.ui.bossBlood.setTargetQiJue()

    def set_inDying(self, old):
        super(Monster, self).set_inDying(old)
        p = BigWorld.player()
        if gameglobal.rds.ui.bossBlood.bloodOwner == self.id:
            if self.inDying:
                gameglobal.rds.ui.bossBlood.setPartName('')
                if p.targetLocked:
                    gameglobal.rds.ui.bossBlood.setName(p.targetLocked.roleName + ' ±ôËÀ')
            else:
                gameglobal.rds.ui.bossBlood.hideBossBlood()
                p.unlockTarget()
        if self.inDying:
            BigWorld.callback(0.2, Functor(self._resetSkeleton))

    def set_lv(self, old):
        if not self.inWorld:
            return
        if gameglobal.rds.ui.isHideAllUI():
            return
        if BigWorld.player().targetLocked == self or gameglobal.rds.ui.bossBlood.bloodOwner == self.id:
            if self.needShowBossBlood() and gameglobal.rds.ui.bossBlood:
                gameglobal.rds.ui.bossBlood.setLevel(self)
            elif gameglobal.rds.ui.target:
                gameglobal.rds.ui.target.setLevel(self.lv)

    def isMultiPartMonster(self):
        return self.getItemData().get('multiPart', False)

    def getAvatarMonsterCap(self):
        return self.getItemData().get('actCap', 1)

    def __checkActionNeedType(self):
        for act in self.model.queue:
            if act in self.fashion.getAlphaBeHitActions():
                return action.S_BLEND

        if self.fashion._doingActionType in (action.CAST_ACTION,
         action.ATTACK_ACTION,
         action.MOVING_ACTION,
         action.CAST_MOVING_ACTION):
            return action.S_BLEND
        if self.fashion._doingActionType in (action.UNKNOWN_ACTION,
         action.IDLE_ACTION,
         action.BORED_ACTION,
         action.CASTSTOP_ACTION,
         action.AFTERMOVESTOP_ACTION,
         action.MOVINGSTOP_ACTION,
         action.BEHIT_ACTION,
         action.ALERT_ACTION,
         action.INCOMBAT_START_ACTION):
            return action.S_BREAK
        return action.S_SLIDE

    def movingNotifier(self, isMoving, moveSpeed = 1.0):
        if not self.inWorld:
            return
        if self.inFrameScript:
            return
        super(Monster, self).movingNotifier(isMoving, moveSpeed)
        self.isMoving = isMoving
        movingType = self.__checkActionNeedType()
        if isMoving:
            self.breakBeHitAction()
            if movingType == action.S_BLEND:
                seq = self.fashion.playedAction.get(self.fashion.actionKey, None)
                if seq != None and seq.active == True and seq.blend:
                    for i in seq.action:
                        i.enableAlpha(True)
                        i.enableDummyTrack(False)

            elif movingType == action.S_BREAK:
                self.fashion.stopAllActions()
            if self.isMultiPartMonster() or self.isAvatarMonster():
                return
            if not self.inCombat and not self.inGuard:
                if self.fashion.action and hasattr(self.fashion.action, 'needSetIdleCaps') and self.fashion.action.needSetIdleCaps():
                    self.fashion.setMonsterIdleCaps(self.am)
                else:
                    self.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_GROUND]
            elif not self.inDying:
                self.fashion.setMonsterCombatCaps(self.am)
        else:
            if movingType == action.S_BLEND:
                seq = self.fashion.playedAction.get(self.fashion.actionKey, None)
                if seq != None and seq.active == True and seq.blend:
                    for i in seq.action:
                        i.enableAlpha(False)
                        i.enableDummyTrack(False)

            if self.isMultiPartMonster() or self.isAvatarMonster():
                return
            if not self.inCombat and not self.inGuard:
                if self.fashion.action and hasattr(self.fashion.action, 'needSetIdleCaps') and self.fashion.action.needSetIdleCaps():
                    self.fashion.setMonsterIdleCaps(self.am)
                else:
                    idleCap = self.fashion.getCapsIdle()
                    self.am.matchCaps = [idleCap, keys.CAPS_GROUND]
        self.setInFlyCaps()

    def setInFlyCaps(self):
        if getattr(self, 'inFly', 0):
            self.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_FLY]

    def set_firstAttacker(self, old):
        p = BigWorld.player()
        if formula.inDotaBattleField(getattr(p, 'mapID', 0)):
            self.topLogo.setMonsterColorInDota(self)
            return
        if self.firstAttacker:
            flag = False
            p = BigWorld.player()
            if p.gbId == self.firstAttacker[1]:
                flag = True
            if self.monsterOwnerGroupNUID != 0 and p.groupNUID == self.monsterOwnerGroupNUID or p.inFightForLoveFb():
                flag = True
            self.topLogo.setMonsterColor(flag)

    def set_monsterOwnerGroupNUID(self, old):
        p = BigWorld.player()
        if formula.inDotaBattleField(getattr(p, 'mapID', 0)):
            self.topLogo.setMonsterColorInDota(self)
            return
        if self.monsterOwnerGroupNUID != 0:
            flag = False
            p = BigWorld.player()
            if self.firstAttacker and p.gbId == self.firstAttacker[1]:
                flag = True
            if p.groupNUID == self.monsterOwnerGroupNUID or p.inFightForLoveFb():
                flag = True
            self.topLogo.setMonsterColor(flag)

    def modelModify(self, part, func, tp = 1):
        if self.model is not None:
            if tp == 1 and hasattr(self.model, part):
                tintalt.ta_add([self.model], func[0], None, 0, part)
            elif tp == 2:
                self.model.newFxName = func[1]
                tintalt.ta_set_static(self.allModels, func[0])

    def chatInScreen(self, msgId, color):
        msg = DD.data.get(msgId, {}).get('details')
        if not msg:
            return
        gameglobal.rds.ui.notify.showSysNotifyDirect(msg, color)

    def set_bianshiBonus(self, old):
        keyNew = self.bianshiBonus.keys()
        keyOld = old.keys()
        keyAdd = set(keyNew) - set(keyOld)
        for key in keyAdd:
            if len(self.bianshiBonus[key]):
                item = self.bianshiBonus[key][0]
                gameglobal.rds.ui.dying.showReward(key, item[0])

    def set_tempCamp(self, old):
        self.refreshUfo()
        if self.topLogo:
            self.topLogo.updateRoleName(self.topLogo.name)

    def refreshUfo(self):
        if hasattr(BigWorld.player(), 'targetLocked') and BigWorld.player().targetLocked == self:
            ufoType = ufo.UFO_NORMAL
            if BigWorld.player().isEnemy(self):
                ufoType = BigWorld.player().getTargetUfoType(self)
            self.fashion.attachUFO(ufoType)
            if self.topLogo:
                self.topLogo.showSelector(*ufo.SELECTOR_ARGS_MAP[ufoType])
            if self.isInHover:
                outlineHelper.setTarget(self)

    def playSound(self, soundId):
        if not self.inWorld:
            return
        BigWorld.player().playSound(soundId, self.position)

    def playMonsterSoundByMMCD(self, str):
        if str:
            soundId = self.getItemData().get(str, None)
            if soundId:
                gameglobal.rds.sound.playSound(soundId, self)

    def chatInChannel(self, msgId, duration = const.POPUP_MSG_SHOW_DURATION, channel = 0):
        chatFuncs = ('chatToNPC', 'chatToView', 'chatToShout')
        funcIdx = limit(channel, 0, len(chatFuncs) - 1)
        msg = DD.data.get(msgId, {}).get('details')
        if not msg:
            return
        player = BigWorld.player()
        func = getattr(player, chatFuncs[funcIdx], None)
        if chatFuncs[funcIdx] == 'chatToView':
            func and func(self.roleName, msg, self.id, duration, False, 0)
        elif chatFuncs[funcIdx] == 'chatToNPC':
            func and func(self.roleName, msg, self.id, duration)
        else:
            func and func(self.roleName, msg, self.id, duration, 0)
        chatRadii = self.getChatRadii()
        if chatRadii > const.CHAT_AROUND_RANGE:
            self.changeTopLogoFadeEnd(chatRadii)

    def popupMsg(self, msgId, duration = const.POPUP_MSG_SHOW_DURATION):
        msg = DD.data.get(msgId, {}).get('details')
        if not msg:
            return
        BigWorld.player().popupMsg(self.id, msg, duration)

    def chatToView(self, msgId, duration = const.POPUP_MSG_SHOW_DURATION):
        if not self.inWorld:
            return
        super(Monster, self).chatToView(msgId, duration)
        chatRadii = self.getChatRadii()
        if chatRadii > const.CHAT_AROUND_RANGE:
            self.changeTopLogoFadeEnd(chatRadii)

    def chatWithTgtName(self, msgId, channel, tgtName, bPopupMsg):
        if not self.inWorld:
            return
        msg = DD.data.get(msgId, {}).get('details')
        if not msg:
            return
        if tgtName:
            msg = msg % tgtName
        gameglobal.rds.ui.chat.addMessage(channel, msg, self.roleName)
        if bPopupMsg:
            BigWorld.player().popupMsg(self.id, msg, const.POPUP_MSG_SHOW_DURATION)

    def getChatRadii(self):
        return min(MD.data.get(self.charType, {}).get('chatRadii', const.CHAT_AROUND_RANGE), 70)

    def changeTopLogoFadeEnd(self, radii):
        if not self.inWorld:
            return
        if not self.topLogo:
            return
        if not self.topLogo.guiAni:
            return
        self.topLogo.guiAni.fadeEnd = radii

    def hideInGoHome(self):
        self.playShaderEffect(const.BLEND_OUT_TINT_ID)
        BigWorld.callback(2.5, Functor(self._resetAtHome))

    def _resetAtHome(self):
        self.playShaderEffect(const.BLEND_IN_TINT_ID)

    def playShaderEffect(self, tintId):
        if not self.inWorld:
            return
        tintTime = 0
        if tintId == const.BLEND_OUT_TINT_ID:
            if hasattr(self, 'topLogo') and self.topLogo != None:
                self.topLogo.release()
                self.topLogo = utils.MyNone
            if not self.fashion:
                return
            self.fashion.attachUFO(ufo.UFO_NULL)
            self.removeAllFx()
            tintTime = 0
        elif tintId == const.BLEND_IN_TINT_ID:
            self.modelServer.attachModelFromData()
            self.afterModelFinish()
            tintTime = 2.0
        self.addTint(tintId, self.allModels, tintTime)

    def bornFadeIn(self, tintId = const.BLEND_IN_TINT_ID, tintTime = 2.0):
        if not self.inWorld:
            return
        if not self.model:
            return
        if self.model.visible == False:
            return
        if modelRobber.getInstance().isMonsterRobber(self.id):
            return
        opValue = self.getOpacityValue()
        if opValue[0] == gameglobal.OPACITY_HIDE:
            return
        if self.getItemData().get('noBornFadeIn', False):
            return
        if not hasattr(self.model, 'fadeShader') or not self.model.fadeShader:
            fadeShader = BigWorld.BlendFashion()
            self.model.fadeShader = fadeShader
            self.model.fadeShader.current(0)
        self.isBlendIn = True
        if tintTime > 0:
            self.model.fadeShader.changeTime(tintTime)
            self.model.fadeShader.dest(255)
        BigWorld.callback(tintTime + 0.1, self.blendOver)

    def blendOver(self):
        self.isBlendIn = False

    def checkPrivate(self):
        return False

    def set_applyTints(self, old):
        self._modifyTints()

    def set_dyingAtkDict(self, old):
        for id in self.dyingAtkDict:
            if id in old:
                if self.dyingAtkDict[id] > old[id]:
                    gameglobal.rds.ui.teamComm.setHit(id, self.dyingAtkDict[id])
            else:
                gameglobal.rds.ui.teamComm.setHit(id, self.dyingAtkDict[id])

    def _modifyTints(self):
        tintalt.ta_reset(self.allModels)
        for part, func, tp in self.applyTints:
            self.modelModify(part, func, tp)

    def set_bornStage(self, old):
        if old == gametypes.MONSTER_BORN_STAGE_LEAVE_ACT:
            self.setSelected(False)
        if self.bornStage == gametypes.MONSTER_BORN_STAGE_LEAVE_ACT:
            self.fashion.stopActionByName(self.model, self.bornIdleActName)
            leaveBornActioName = self.fashion.getLeaveBornActionName()
            if leaveBornActioName:
                self.fashion.playSingleAction(leaveBornActioName, action.LEAVE_BORN_ACTION, 0, None, 0, 1, 0, False)
            self._addTintByName('leaveBornTint', self.getItemData())
        if self.bornStage == gametypes.MONSTER_BORN_STAGE_FINISH:
            self.resetTopLogo()

    def _hideQuestIcon(self, isHide):
        if not self.inWorld:
            return
        if self.charType in BigWorld.player().questMonsterInfo.keys():
            self.topLogo.setQuestIconVisible(not isHide)

    def resetTopLogo(self):
        if not self.inWorld:
            return
        if self.bornStage in (gametypes.MONSTER_BORN_STAGE_ACT, gametypes.MONSTER_BORN_STAGE_IDLE_ACT) and not getattr(self, 'IsOreSpawnPoint', False):
            if self.inWorld and self.model and self.topLogo and not MMCD.data.get(self.charType, {}).get('bornShowName', 0):
                self.topLogo.hideName(True)
                self.topLogo.hideTitleName(True)
                self._hideQuestIcon(True)
        elif self.inWorld and self.model and self.topLogo and not gameglobal.gHideMonsterName:
            if self.inCombat or not self.hideTopLogoOutCombat() and self.life == gametypes.LIFE_ALIVE:
                self.topLogo.hideName(False)
                self.topLogo.hideTitleName(False)
                self._hideQuestIcon(False)
            else:
                self.topLogo.hideName(True)
                self.topLogo.hideTitleName(True)
                self._hideQuestIcon(True)
        super(Monster, self).resetTopLogo()

    def set_titleName(self, old):
        if self.inWorld and self.model and self.topLogo:
            self.topLogo.titleName = self.titleName
            self.topLogo.setTitleName(self.titleName)

    def set_roleName(self, old):
        if self.inWorld and self.model and self.topLogo != None:
            self.topLogo.nameString = self.roleName
            self.topLogo.name = self.roleName
            self.topLogo.updateRoleName(self.roleName)

    def showBloodLabel(self, val, atkType):
        self.bloodLabel(val, atkType)

    def reloadModel(self):
        self.modelServer.release()
        self.modelServer = None
        self.modelServer = modelServer.SimpleModelServer(self)

    def showMonsterIcon(self):
        pass

    def dealTrapInEvent(self, trapLengthType = 1):
        super(Monster, self).dealTrapInEvent(trapLengthType)
        if self.questItem:
            path = uiUtils.getItemIconFile64(self.questItem)
            gameglobal.rds.ui.npcSlot.show(path, uiConst.SLOT_FROM_MONSTER, [self.questItem, True, self.questItem])

    def dealTrapOutEvent(self, trapLengthType = 1):
        super(Monster, self).dealTrapOutEvent(trapLengthType)
        if self.questItem:
            gameglobal.rds.ui.npcSlot.hide()

    def onGenLuckyBonus(self, entId, luckTime):
        gamelog.debug('onGenLuckyBonus', luckTime)
        ent = BigWorld.entity(entId)
        if ent and ent.inWorld and luckTime >= 0:
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (ent.getBasicEffectLv(),
             ent.getBasicEffectPriority(),
             ent.model,
             SCD.data.get('sfxBigLuck', 70001),
             sfx.EFFECT_LIMIT))
            BigWorld.callback(0.7, Functor(sfx.attachEffect, gameglobal.ATTACH_EFFECT_INPOS, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             SCD.data.get('sfxDropItem', 70002),
             sfx.EFFECT_LIMIT,
             self.position,
             0,
             0,
             0,
             luckTime)))
            BigWorld.callback(0.7 + luckTime, Functor(sfx.attachEffect, gameglobal.ATTACH_EFFECT_INPOS, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             SCD.data.get('sfxDropItemEnd', 70004),
             sfx.EFFECT_LIMIT,
             self.position,
             0,
             0,
             0,
             3)))

    def getFKey(self):
        iEvent = getattr(self, 'triggerEventIndex', -1)
        eventDataList = METD.data.get(self.charType, [])
        if iEvent < 0 or iEvent > len(eventDataList) - 1:
            return 0
        eventData = eventDataList[iEvent]
        p = BigWorld.player()
        if eventData.get('teamMode'):
            if not p.groupNUID:
                return 0
            if not p.groupActionState:
                if p.isGroupInAction():
                    fKey = eventData.get('joinF')
                    if fKey:
                        return fKey
                else:
                    fKey = eventData.get('readyF')
                    if fKey:
                        return fKey
            elif p.groupActionState == gametypes.GROUP_ACTION_STATE_PREPARE:
                fKey = eventData.get('cancelF')
                if fKey:
                    return fKey
            else:
                return 0
        return eventData.get('fKey', 0)

    def startNextTriggerCallback(self):
        if self.nextTriggerEventTime:
            tNext = min(self.nextTriggerEventTime.values())
        else:
            tNext = 0
        if tNext > utils.getNow():
            if self.triggerTrapCallback:
                BigWorld.cancelCallback(self.triggerTrapCallback)
                self.triggerTrapCallback = None
            self.triggerTrapCallback = BigWorld.callback(tNext - utils.getNow() + 0.2, self.onNextTriggerCallback)

    def onNextTriggerCallback(self):
        if not self.inWorld:
            return
        self.triggerTrap(True)
        self.triggerTrapCallback = None
        self.startNextTriggerCallback()

    def set_nextTriggerEventTime(self, old):
        self.checkFKey()
        mmcd = MMCD.data.get(self.charType, {})
        triggerEff = mmcd.get('triggerEff', 0)
        if triggerEff:
            if triggerEff in self.attachFx:
                self.removeFx(triggerEff)
            if self.triggerEffectCallback:
                BigWorld.cancelCallback(self.triggerEffectCallback)
                self.triggerEffectCallback = None
            if self.nextTriggerEventTime:
                tNext = min(self.nextTriggerEventTime.values())
            else:
                tNext = 0
            if tNext > utils.getNow():
                self.triggerEffectCallback = BigWorld.callback(tNext - utils.getNow() + 1.0, self._addTriggerEff)
        self.startNextTriggerCallback()

    def checkFKey(self):
        if not self.inWorld:
            return
        self.trapCallback(True)

    def needAddStateIcon(self):
        isWorldBoss = MD.data.get(self.charType, {}).get('isWorldBoss', False)
        return not isWorldBoss

    def canOutline(self):
        return self.getItemData().get('canOutline', True) and self.isBlendIn != True

    def isSceneObj(self):
        if getattr(self.model, 'isSceneObj', False):
            return self.getItemData().get('isSceneObj', False)
        return False

    def getUFOLod(self):
        return self.getItemData().get('ufoDist', gameglobal.UFO_DIST)

    def needHideTargetProxyLv(self):
        return self.getItemData().get('hideTargetProxyLv', False)

    def updateTimerBlood(self):
        oldHp = self.hp
        self.resetSkyWingMonsterHpAndMhp()
        self.set_hp(oldHp)
        if self.inWorld:
            self.bloodTimer = BigWorld.callback(0.15, self.updateTimerBlood)

    def set_fallenRedGuardFlag(self, old):
        if self.fallenRedGuardFlag and gameglobal.rds.configData.get('enableKillFallenRedGuard', False):
            gameglobal.rds.ui.killFallenRedGuardRank.enterMonster(self.fallenRedGuardFlag)

    def resetSkyWingMonsterHpAndMhp(self):
        left, total = gameglobal.rds.ui.baiDiShiLian.getTime()
        if left > 0 and self.lastUpdateTime != utils.getNow():
            self.lastUpdateTime = utils.getNow()
            self.plusTime = 1.0
        self.plusTime = max(0, self.plusTime - 0.03)
        left += self.plusTime
        leftPercent = left * 1.0 / total
        monsterMhp = SWCCD.data.get('bossMhp', 10000)
        self.mhp = monsterMhp
        self.hp = int(leftPercent * monsterMhp)

    def set_isShowConnector(self, old):
        if self.isShowConnector and not self.lockedEffInRange:
            self.lockedEffId = self.getConnectorSfxId()
            self.lockedEffInRange = clientUtils.pixieFetch(sfx.getPath(self.lockedEffId))
            self.lockedEffInRange.setAttachMode(0, 1, 0)
            self.lockedEffInRange.force()
        if self.isShowConnectorFlag:
            self.updateConnectTgtId(self.getConnectorTgtId())
        self.refreshConnectEff()

    def set_forceShowConnectorTgtId(self, old):
        if self.isShowConnectorFlag:
            self.updateConnectTgtId(self.getConnectorTgtId())
        self.refreshConnectEff()

    def getConnectorTgtId(self):
        return self.forceShowConnectorTgt or self.lockedId

    @property
    def isShowConnectorFlag(self):
        return getattr(self, 'isShowConnector', False)

    @property
    def forceShowConnectorTgt(self):
        return getattr(self, 'forceShowConnectorTgtId', 0)

    def refreshConnectEff(self):
        if self.isShowConnectorFlag:
            self.delConnnectEff()
            self.addConnectEff()
        else:
            self.delConnnectEff()

    def delConnnectEff(self):
        if self.targetLockConnector:
            self.targetLockConnector.release()
            self.targetLockConnector = None

    def addConnectEff(self):
        self.delConnnectEff()
        if not self.firstFetchFinished:
            return
        connectorTgtId = self.getConnectorTgtId()
        if not connectorTgtId:
            return
        if not self.isShowConnectorFlag:
            return
        if not self.inWorld:
            return
        if self.life != gametypes.LIFE_ALIVE:
            return
        target = BigWorld.entities.get(connectorTgtId, None)
        if target and target.firstFetchFinished:
            p = BigWorld.player()
            startNode = self.getgetTargetLockStartNode()
            endNode = self.getTargetLockEndNode()
            if not startNode or not endNode:
                return
            dist = (self.position - target.position).length
            effect = self.lockedEffInRange
            if effect:
                self.targetLockConnector = sfx.attachEffect(gameglobal.ATTACH_CACHED_EFFECT_CONNECTOR, (p.getSkillEffectLv(),
                 startNode,
                 effect,
                 endNode,
                 80,
                 p.getSkillEffectPriority()))

    def getgetTargetLockStartNode(self):
        nodeName = SCD.data.get('monsterTargetLockedEffStartNodeName', 'Scene Root')
        node = None
        try:
            node = self.model.node(nodeName)
            if not node:
                node = self.model.node('Scene Root')
        except:
            pass

        return node

    def getTargetLockEndNode(self):
        connectorTgtId = self.getConnectorTgtId()
        if not connectorTgtId:
            return
        target = BigWorld.entities.get(connectorTgtId, None)
        if not target or not target.inWorld:
            return
        nodeName = SCD.data.get('monsterTargetLockedEffEndNodeName', 'Scene Root')
        node = None
        try:
            if hasattr(target, 'isInCoupleRide') and target.isInCoupleRide():
                if target.isInCoupleRideAsRider():
                    horse = target.getCoupleRideHorse()
                    if horse:
                        node = horse.modelServer.bodyModel.node(nodeName)
                else:
                    node = target.modelServer.bodyModel.node(nodeName)
            elif hasattr(target, 'isRidingTogether') and target.isRidingTogether():
                if target.isRidingTogetherAsMain():
                    node = target.modelServer.bodyModel.node(nodeName)
                else:
                    main = target.getRidingTogetherMain()
                    if main:
                        node = main.modelServer.bodyModel.node(nodeName)
            else:
                node = target.model.node(nodeName)
            if not node:
                node = target.model.node('Scene Root')
        except:
            pass

        return node

    def onChangeStatus(self, no):
        """
        \xb9\xd6\xce\xef\xd0\xde\xb8\xc4\xb6\xaf\xd7\xf7\xd7\xe9\xa3\xa8\xc4\xbf\xc7\xb0\xd3\xc9\xb8\xb1\xb1\xbeAI\xb5\xc8\xb4\xa5\xb7\xa2\xa3\xa9
        :param no: \xb1\xe0\xba\xc5\xa3\xa8\xc8\xe7\xb9\xfbno==1\xd4\xf2\xca\xb9\xd3\xc3actGroupid idleGroupid\xa3\xac\xc8\xe7\xb9\xfbno==2\xd4\xf2\xca\xb9\xd3\xc3actGroupid2 idleGroupid2\xa3\xac\xc0\xe0\xcd\xc6\xa3\xa9
        """
        if not self.inWorld:
            return
        if not hasattr(self, 'fashion'):
            return
        actionList = self.fashion.action.actionList if self.fashion.action else []
        self.fashion.action = monsterAction.getMonsterActionGroup(self, no)
        self.fashion.action.actionList = actionList
        if not self.isMultiPartMonster():
            if not self.inCombat:
                self.fashion.setMonsterIdleCaps(self.am)
            else:
                self.fashion.setMonsterCombatCaps(self.am)
        else:
            self.fashion.setMonsterIdleCaps(self.am)


methodMap = {}

def loadFkMethod():
    modules = (ICombatUnit,
     IMonsterCombatUnit,
     IClient,
     IDisplay,
     IPickable,
     Monster)
    for module in modules:
        for name, fun in inspect.getmembers(module, inspect.ismethod):
            methodMap[name] = name


loadFkMethod()
