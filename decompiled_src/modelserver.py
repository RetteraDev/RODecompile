#Embedded file name: /WORKSPACE/data/entities/client/helpers/modelserver.o
import time
import math
import random
import BigWorld
import Math
import gametypes
import gameglobal
import const
import charRes
import seqTask
import action
import weaponModel
import followModel
import attachedModel
import keys
import utils
import gamelog
import clientcom
import skillDataInfo
import clientUtils
from callbackHelper import Functor
from sfx import sfx
from helpers import tintalt
from helpers import faceEmote
from helpers import qingGong
from helpers import poseManager
from helpers import outlineHelper
from helpers import cameraControl as CC
from helpers import attachedModelCueFashion
from data import booth_skin_data as BSD
from data import equip_data as ED
from data import horsewing_data as HWCD
from data import sys_config_data as SCD
from data import couple_emote_data as CED
from data import couple_emote_basic_data as CEBD
from data import zaiju_data as ZJD
from data import ride_together_data as RTD
from data import carrousel_data as CD
from data import interactive_basic_action_data as IBAD
from data import interactive_data as IAD
from data import interactive_chat_data as IACD
from data import interactive_emote_data as IAED
from data import couple_emote_general_data as CEGD
from data import interactive_expend_action_data as IEAD
from data import foot_dust_data as FDD
from data import multi_carrier_data as MCAD
from data import wing_world_carrier_data as WWCD
from data import nun_form_data as NFD
STATE_EMPTY = 0
STATE_HUMAN = 1
STATE_HORSE = 2
STATE_WINGFLY = 3
STATE_REPLACE = 4
STATE_ATTACH = 5
STATE_BEAST = 6
BODY_UPDATE_STATUS_NORMAL = 0
BODY_UPDATE_STATUS_UPDATING = 1
BODY_UPDATE_STATUS_UPDATE_CACHING = 2
PRINCESS_CONTROL = 'princess_control'
PRINCESS_PASSIVE_CONTROL = 'princess_passive_control'
SCHOOL_ATTACH_RIGHT_WEAPON = (const.SCHOOL_GUANGREN,
 const.SCHOOL_YANTIAN,
 const.SCHOOL_YECHA,
 const.SCHOOL_LIUGUANG)
HAIR_NODE_NO_CHANGE = 0
HAIR_NODE_DETACH = 1
HAIR_NODE_CHANGE = 2
BIND_TYPE_ROUND_TABLE = 1
BIND_TYPE_INTERACTIVE_OBJ = 2
BIND_TYPE_CARRIER = 3
WEAR_EQU_PART_MAP = {gametypes.EQU_PART_HEADWEAR: 'headdress',
 gametypes.EQU_PART_HEADWEAR_RIGHT: 'headdressRight',
 gametypes.EQU_PART_HEADWEAR_LFET: 'headdressLeft',
 gametypes.EQU_PART_FACEWEAR: 'facewear',
 gametypes.EQU_PART_WAISTWEAR: 'waistwear',
 gametypes.EQU_PART_BACKWEAR: 'backwear',
 gametypes.EQU_PART_TAILWEAR: 'tailwear',
 gametypes.EQU_PART_CHESTWEAR: 'chestwear',
 gametypes.EQU_PART_EARWEAR: 'earwear',
 gametypes.EQU_PART_FASHION_CAPE: 'fashionCape'}

def getHairNodeModel(model = None):
    if model:
        for path in model.sources:
            if path.endswith('hair.model'):
                return path[:-10] + 'gd_hair.model'


def getEntityZaijuDataWithCustom(entity, zaijuId):
    if entity and hasattr(entity, 'getZaijuDataWithCustom'):
        return entity.getZaijuDataWithCustom(zaijuId)
    return ZJD.data.get(zaijuId, {})


class MultiModelServer(object):

    def __init__(self, entity):
        self.entity = entity
        self.threadID = gameglobal.getLoadThread()
        self.leftWeaponModel = weaponModel.WeaponModel(entity.id, self.threadID)
        self.rightWeaponModel = weaponModel.WeaponModel(entity.id, self.threadID)
        self.rightWeaponModel.setRightWeapon(True)
        self.avatarFollowModel = followModel.AvatarFollowModel(entity.id, self.threadID)
        self.yuanLing = weaponModel.WeaponModel(entity.id, self.threadID)
        self.yuanLing.setBias(0.5)
        self.headdress = attachedModel.WearAttachModel(entity.id, self.threadID, 'headdress', 'HP_headdress_front', 'f1', True)
        self.headdressRight = attachedModel.WearAttachModel(entity.id, self.threadID, 'headdress', 'HP_headdress_right', 'r1')
        self.headdressLeft = attachedModel.WearAttachModel(entity.id, self.threadID, 'headdress', 'HP_headdress_left', 'l1')
        self.facewear = attachedModel.WearAttachModel(entity.id, self.threadID, 'face', 'HP_face', None, True)
        self.waistwear = attachedModel.WearAttachModel(entity.id, self.threadID, 'waist')
        self.backwear = attachedModel.WearAttachModel(entity.id, self.threadID, 'back')
        self.tailwear = attachedModel.WearAttachModel(entity.id, self.threadID, 'tail')
        self.chestwear = attachedModel.WearAttachModel(entity.id, self.threadID, 'chest')
        self.earwear = attachedModel.WearAttachModel(entity.id, self.threadID)
        self.buffModel = attachedModel.BuffItemAttachModel(entity.id, self.threadID)
        self.hairNodeModel = None
        self.hairNodeCue = attachedModelCueFashion.HairNodeModelCue(entity.id)
        self.headdresses = ('headdress', 'headdressRight', 'headdressLeft')
        self.headwear = ('facewear', 'earwear')
        self.otherwears = ('waistwear', 'backwear', 'tailwear', 'chestwear')
        self.actionMatcherWears = set()
        self.leftWeaponBackup = []
        self.rightWeaponBackup = []
        self.tempWeaponModel = None
        self.bodyModelLoader = seqTask.SeqModelLoader(self.entity.id, self.threadID, self._bodyModelFinish)
        self.bodyModelUpdater = seqTask.SeqModelUpdater(None, self.threadID, self._bodyPartsUpdateFinish)
        self.bodyModel = None
        self.state = STATE_EMPTY
        self.urgent = False
        self.stateID = None
        self.onModelFinishedCall = None
        self.weaponCallback = None
        self.oldFootTwistSpeed = SCD.data.get('footTwistSpeed', gameglobal.FOOTTWISTSPEED)
        self.bodyUpdateStatus = BODY_UPDATE_STATUS_NORMAL
        self.hairChange = HAIR_NODE_NO_CHANGE
        self.roundTableIdx = -1
        self.carrierIdx = -1
        self.interactiveObjIdx = -1
        self.faceIdleAction = None
        self.gdHairEffects = []
        self.freezedEffs = []
        self.lastZaijuRideModelId = 0

    def freezeEffect(self, freezeTime):
        if self.leftWeaponModel:
            self.leftWeaponModel.freezeEffect(freezeTime)
        if self.rightWeaponModel:
            self.rightWeaponModel.freezeEffect(freezeTime)
        if self.wingFlyModel:
            self.wingFlyModel.freezeEffect(freezeTime)
        if self.fishingModel:
            self.fishingModel
        if self.lifeSkillModel:
            self.lifeSkillModel.freezeEffect(freezeTime)
        if self.buffModel:
            self.buffModel.freezeEffect(freezeTime)
        if self.socialActionModel:
            self.socialActionModel.freezeEffect(freezeTime)
        for wear in self.headdresses + self.headwear + self.otherwears:
            wearModel = getattr(self, wear)
            if wearModel and wearModel.state == attachedModel.ATTACHED:
                wearModel.freezeEffect(freezeTime)

    def clearFreezeEffect(self):
        if self.leftWeaponModel:
            self.leftWeaponModel.clearFreezeEffect()
        if self.rightWeaponModel:
            self.rightWeaponModel.clearFreezeEffect()
        if self.wingFlyModel:
            self.wingFlyModel.clearFreezeEffect()
        if self.fishingModel:
            self.fishingModel.clearFreezeEffect()
        if self.lifeSkillModel:
            self.lifeSkillModel.clearFreezeEffect()
        if self.buffModel:
            self.buffModel.clearFreezeEffect()
        if self.socialActionModel:
            self.socialActionModel.clearFreezeEffect()
        for wear in self.headdresses + self.headwear + self.otherwears:
            wearModel = getattr(self, wear)
            if wearModel:
                wearModel.clearFreezeEffect()

    def setUrgent(self, isUrgent):
        self.urgent = isUrgent
        if isUrgent:
            self.setThreadID(gameglobal.URGENT_THREAD)
        else:
            self.setThreadID(gameglobal.getLoadThread())

    def setThreadID(self, threadID):
        self.threadID = threadID
        self.leftWeaponModel.threadID = threadID
        self.rightWeaponModel.threadID = threadID
        self.yuanLing.threadID = threadID
        self.bodyModelLoader.threadID = threadID
        self.headdress.threadID = threadID
        self.headdressRight.threadID = threadID
        self.headdressLeft.threadID = threadID
        self.facewear.threadID = threadID
        self.waistwear.threadID = threadID
        self.backwear.threadID = threadID
        self.tailwear.threadID = threadID
        self.chestwear.threadID = threadID
        self.earwear.threadID = threadID
        self.buffModel.threadID = threadID

    def release(self):
        if self.entity:
            self.entity = None
        self.leftWeaponModel.release()
        self.leftWeaponModel = None
        self.rightWeaponModel.release()
        self.rightWeaponModel = None
        self.yuanLing.release()
        self.yuanLing = None
        self.bodyModelLoader.cancel()
        self.bodyModelLoader = None
        self.bodyModelUpdater.release()
        self.bodyModelUpdater = None
        self.headdress.release()
        self.headdress = None
        self.headdressRight.release()
        self.headdressRight = None
        self.headdressLeft.release()
        self.headdressLeft = None
        self.facewear.release()
        self.facewear = None
        self.waistwear.release()
        self.waistwear = None
        self.backwear.release()
        self.backwear = None
        self.tailwear.release()
        self.tailwear = None
        self.chestwear.release()
        self.chestwear = None
        self.earwear.release()
        self.earwear = None
        self.buffModel.release()
        self.buffModel = None
        self.bodyModel = None
        if self.hairNodeModel:
            self.hairNodeModel.soundCallback(None)
        self.hairNodeModel = None
        self.hairNodeCue.release()
        self.hairNodeCue = None
        self.state = STATE_EMPTY
        self.hairChange = HAIR_NODE_NO_CHANGE
        self.actionMatcherWears = set()
        self.releaseGdHairEffect()

    def weaponUpdate(self):
        if not self.entity.isRealModel:
            return
        aspect = self.entity.realAspect
        self.weaponTypes = {'leftWeapon': 0,
         'rightWeapon': 0}
        leftWeaponId = aspect.leftWeapon
        rightWeaponId = aspect.rightWeapon
        if self.entity.fashion.isPlayer:
            self.setWeaponType(leftWeaponId, 'leftWeapon')
            self.setWeaponType(rightWeaponId, 'rightWeapon')
        leftWeaponId = self.entity.getWeapon(True)
        leftWeaponEnhLv = self.entity.getWeaponEnhLv(True)
        if leftWeaponId:
            self.equipWeapon(leftWeaponId, True, leftWeaponEnhLv)
        rightWeaponId = self.entity.getWeapon(False)
        rightWeaponEnhLv = self.entity.getWeaponEnhLv(False)
        if rightWeaponId:
            self.equipWeapon(rightWeaponId, False, rightWeaponEnhLv)
        yuanLingModelId = self.entity.realAspect.yuanLing
        if yuanLingModelId:
            self.yuanLing.equipItem(yuanLingModelId)
            self.actionMatcherWears.add('yuanLing')
        elif 'yuanLing' in self.actionMatcherWears:
            self.actionMatcherWears.remove('yuanLing')
        if self.entity.realSchool == const.SCHOOL_GUANGREN:
            self.rightWeaponModel.setAttachType(weaponModel.ATTACHED_RIGHT)
        else:
            self.rightWeaponModel.setAttachType(weaponModel.ATTACHED)
        self.refreshWeaponState()
        if hasattr(self.entity, 'isInCoupleRide') and self.entity.isInCoupleRide():
            self.hangWomanOnMan()

    def updateGdHairEffect(self):
        entity = self.entity
        if not entity.inWorld:
            return
        if not entity.isRealModel:
            return
        if not hasattr(entity, 'getOpacityValue'):
            return
        opaVal = entity.getOpacityValue()[0]
        if opaVal in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
            return
        if not self.hairNodeModel or not self.hairNodeModel.inWorld:
            return
        self.releaseGdHairEffect()
        partId = getattr(entity.realAspect, 'fashionHead', 0)
        if partId:
            data = ED.data.get(partId, {})
            effects = data.get('gdHairEffect', ())
            for effectId in effects:
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
                 entity.getEquipEffectPriority(),
                 self.hairNodeModel,
                 effectId,
                 sfx.EFFECT_LIMIT_MISC))
                if fx:
                    self.gdHairEffects.extend(fx)

    def releaseGdHairEffect(self):
        if self.gdHairEffects:
            for fx in self.gdHairEffects:
                if fx:
                    fx.stop()

        self.gdHairEffects = []

    def playWearBoredActionRandomly(self):
        wears = list(self.actionMatcherWears)
        owner = self.entity
        if not owner.inWorld:
            return
        if wears:
            wearStr = random.choice(wears)
            wearModel = getattr(self, wearStr)
            if getattr(wearModel, 'boredActionMovingType', 0) == gameglobal.WEAR_ATTACH_MOVE_STOP_BORED_ACTION and owner.inMoving():
                return
            model = getattr(wearModel, 'model', None)
            if model:
                queue = model.queue
                if '1102' not in queue and '1101' in queue:
                    wearModel.doActions(('1102', '1101'))

    def stopWearBoredAction(self):
        wears = list(self.actionMatcherWears)
        owner = self.entity
        if not owner.inWorld:
            return
        for wearStr in wears:
            wearModel = getattr(self, wearStr)
            model = getattr(wearModel, 'model', None)
            if model and '1102' in model.queue:
                if getattr(wearModel, 'boredActionMovingType', 0) == gameglobal.WEAR_ATTACH_MOVE_STOP_BORED_ACTION and owner.inMoving():
                    wearModel.doActions(('1101',))

    def wearUpdate(self):
        if not self.entity.isRealModel:
            return
        self._wearUpdate(self.hairNodeModel)

    def detachHairNode(self):
        if self.bodyModel and self.bodyModel.inWorld:
            node = self.bodyModel.node('biped Head')
            if node:
                if self.hairNodeModel and self.hairNodeModel in node.attachments:
                    node.detach(self.hairNodeModel)
                    entity = self.entity
                    if entity.inWorld and self.hairNodeModel in entity.allModels:
                        entity.allModels.remove(self.hairNodeModel)
                    if 'hairNodeCue' in self.actionMatcherWears:
                        self.actionMatcherWears.remove('hairNodeCue')
                    self.hairNodeModel.soundCallback(None)
            self.hairNodeModel = None

    def loadHairNode(self, callback):
        self.detachHairNode()
        if self.bodyModel and self.bodyModel.inWorld:
            hairPath = self.getHairNode()
            if hairPath:
                clientUtils.fetchModel(self.threadID, callback, hairPath)

    def getHairNode(self, model = None):
        if model == None:
            model = self.bodyModel
        return getHairNodeModel(model)

    def attachHairNode(self, model):
        if model and self.bodyModel and self.bodyModel.inWorld:
            if self.hairNodeModel and self.hairNodeModel.sources == model.sources:
                return
            self.hairNodeModel = model
            node = self.bodyModel.node('biped Head')
            if node and model not in node.attachments:
                node.attach(self.hairNodeModel, 'biped Head')
                entity = self.entity
                if entity.inWorld and model not in entity.allModels:
                    entity.allModels.append(model)
                self.actionMatcherWears.add('hairNodeCue')
                try:
                    self.hairNodeCue.setModel(model)
                    model.soundCallback(self.hairNodeCue.actionCueCallback)
                except:
                    pass

            self.refreshHeaddressState()
            self.showHairNodeAction()
            self.updateGdHairEffect()
            clientcom.setHairNodeDye(self.entity, model)

    def showHairNodeAction(self):
        if self.hairNodeModel and self.hairNodeModel.inWorld:
            try:
                self.hairNodeModel.action('1101')()
            except:
                pass

    def showBackAndWaist(self, show = True):
        for wear in (self.backwear, self.waistwear):
            wear.updateBackWaist(show)

        for weapon in [self.leftWeaponModel, self.rightWeaponModel] + self.leftWeaponBackup + self.rightWeaponBackup:
            weapon.updateBackWaist(not show)

        self.entity.refreshWeaponVisible()
        if getattr(self.entity, 'hidingPower', None):
            self.entity.resetHiding()

    def _wearUpdate(self, hairNodeModel):
        self.attachHairNode(hairNodeModel)
        if self.entity and self.entity.inWorld:
            aspect = self.entity.realAspect
            self.actionMatcherWears = set()
            headdresses = list(self.headdresses)
            for wear in self.headdresses:
                wearId = getattr(aspect, wear)
                slotParts = ED.data.get(wearId, {}).get('slotParts', [])
                if slotParts:
                    for part in slotParts:
                        if part in headdresses:
                            headdresses.remove(part)

                    if wearId:
                        getattr(self, wear).equipItem(wearId)

            for wear in headdresses:
                wearId = getattr(aspect, wear)
                if wearId:
                    wearModel = getattr(self, wear)
                    wearModel.equipItem(wearId)
                    if wearModel.isActionAsEntityWear():
                        self.actionMatcherWears.add(wear)

            if aspect.yuanLing:
                self.actionMatcherWears.add('yuanLing')
            elif 'yuanLing' in self.actionMatcherWears:
                self.actionMatcherWears.remove('yuanLing')
            for wear in self.otherwears + self.headwear:
                wearId = getattr(aspect, wear)
                if wearId:
                    wearModel = getattr(self, wear)
                    wearModel.equipItem(wearId)
                    if wearModel.isActionAsEntityWear():
                        self.actionMatcherWears.add(wear)

            self.refreshWearState()

    def setWeaponType(self, weaponId, keyName):
        if weaponId == 0:
            self.entity.weaponTypes[keyName] = 0
            return
        if ED.data.has_key(weaponId):
            subId = ED.data[weaponId].get('subId', [0])[0]
            if self.entity.fashion.isPlayer:
                self.entity.weaponTypes[keyName] = subId

    def refreshWeaponState(self):
        entity = self.entity
        gamelog.debug('refreshWeaponState:', entity.weaponInHandState())
        weapon = self._getWeaponModel(entity.weaponInHandState())
        if entity.weaponInHandState() == gametypes.WEAPON_DOUBLEATTACH:
            self._setWeaponCaps(True, entity, weapon)
            if entity.realSchool in SCHOOL_ATTACH_RIGHT_WEAPON:
                self.attachWeapon1()
            else:
                self.attachWeapon()
        elif entity.weaponInHandState() == gametypes.WEAPON_HANDFREE:
            self._setWeaponCaps(False, entity, weapon)
            self.hangUpWeapon()
        elif entity.weaponInHandState() == gametypes.WEAPON_MIDATTACH:
            self._setWeaponCaps(True, entity, weapon)
            self.attachWeapon2()
        elif entity.weaponInHandState() == gametypes.WEAPON_DOUBLEATTACH_ALL:
            self._setWeaponCaps(True, entity, weapon)
            self.attachWeapon3()
        elif entity.weaponInHandState() >= gametypes.WEAPON_BACKUP_BOUND and entity.weaponInHandState() < gametypes.WEAPON_MIDATTACH_WITH_ZHUSHOU:
            self._setWeaponCaps(True, entity, weapon)
            self.attachWeaponBackup(weapon)
        elif entity.weaponInHandState() == gametypes.WEAPON_DOUBLEHIDE:
            self._setWeaponCaps(True, entity, weapon)
            self.hideWeapon1()
        elif entity.weaponInHandState() == gametypes.WEAPON_ALLATTACH:
            self._setWeaponCaps(True, entity, weapon)
            self.attachWeapon()
        elif entity.weaponInHandState() == gametypes.WEAR_BACK_ATTACH:
            if self.backwear and hasattr(self.backwear, 'isActionJustSkillWear') and self.backwear.isActionJustSkillWear():
                pass
            else:
                self._setWeaponCaps(True, entity, self.backwear)
                self._setWearModelCaps(True, entity, self.backwear)
                self.attachWear('backwear')
        elif entity.weaponInHandState() == gametypes.WEAR_WAIST_ATTACH:
            if self.waistwear and hasattr(self.waistwear, 'isActionJustSkillWear') and self.waistwear.isActionJustSkillWear():
                pass
            else:
                self._setWeaponCaps(True, entity, self.waistwear)
                self._setWearModelCaps(True, entity, self.waistwear)
                self.attachWear('waistwear')
        elif entity.weaponInHandState() == gametypes.WEAPON_CHANGE_CAPS:
            self._setWeaponCaps(True, entity, weapon)
            self.hangUpWeapon()
        elif entity.weaponInHandState() == gametypes.WEAPON_MIDATTACH_WITH_ZHUSHOU:
            self._setWeaponCaps(True, entity, weapon)
            self.attachWeapon4(weaponModel.ATTACHED_MID_WEAPON_ALL)
        elif entity.weaponInHandState() == gametypes.WEAPON_MIDATTACH_WITH_ZHUSHOU_LEFT:
            self._setWeaponCaps(True, entity, weapon)
        elif entity.weaponInHandState() == gametypes.WEAPON_MIDATTACH_WITH_ZHUSHOU_RIGHT:
            self._setWeaponCaps(True, entity, weapon)
        elif entity.weaponInHandState() == gametypes.WEAPON_BUFF_ATTACH:
            self._setWeaponCaps(True, entity, weapon)
            self.attachBuffWeapon(self.buffModel)
        leftWeaponId = self.entity.getWeapon(True)
        rightWeaponId = self.entity.getWeapon(False)
        if not leftWeaponId:
            self.leftWeaponModel.detach(False)
            for weapon in self.leftWeaponBackup:
                weapon.detach(False)

        if not rightWeaponId:
            self.rightWeaponModel.detach(False)
            for weapon in self.rightWeaponBackup:
                weapon.detach(False)

        yuanLingModelId = self.entity.realAspect.yuanLing
        if yuanLingModelId and hasattr(entity, 'isShowYuanLing') and entity.isShowYuanLing():
            self.yuanLing.hangUp(self.bodyModel)
        else:
            self.yuanLing.detach()

    def refreshYuanLing(self, isShowYuanLing):
        yuanLingModelId = self.entity.realAspect.yuanLing
        if yuanLingModelId and isShowYuanLing:
            self.yuanLing.hangUp(self.bodyModel)
        else:
            self.yuanLing.detach()

    def refreshHeaddressState(self):
        aspect = self.entity.realAspect
        headdresses = list(self.headdresses)
        for wear in self.headdresses:
            wearId = getattr(aspect, wear)
            slotParts = ED.data.get(wearId, {}).get('slotParts', [])
            for part in slotParts:
                if part in headdresses:
                    headdresses.remove(part)
                    getattr(self, part).detach()

        for wear in headdresses:
            wearId = getattr(aspect, wear)
            if wearId:
                getattr(self, wear).hangUp(self.hairNodeModel)
            else:
                getattr(self, wear).detach()

    def refreshOtherWearState(self):
        aspect = self.entity.realAspect
        for wear in self.otherwears:
            wearId = getattr(aspect, wear)
            if wearId:
                if self.entity.weaponInHandState() == gametypes.WEAR_BACK_ATTACH and wear == 'backwear':
                    getattr(self, wear).attach(self.bodyModel)
                elif self.entity.weaponInHandState() == gametypes.WEAR_WAIST_ATTACH and wear == 'waistwear':
                    getattr(self, wear).attach(self.bodyModel)
                else:
                    getattr(self, wear).hangUp(self.bodyModel)
            else:
                getattr(self, wear).detach()

    def refreshHeadWearState(self):
        aspect = self.entity.realAspect
        mpr = charRes.MultiPartRes()
        mpr.queryByAvatar(self.entity)
        headType, path = mpr.getHeadPath()
        for wear in self.headwear:
            wearId = getattr(aspect, wear)
            if wearId:
                if headType == charRes.HEAD_TYPE1 or path == None:
                    getattr(self, wear).detach()
                else:
                    getattr(self, wear).hangUp(self.bodyModel)
            else:
                getattr(self, wear).detach()

    def refreshWearState(self):
        self.refreshHeaddressState()
        self.refreshOtherWearState()
        self.refreshHeadWearState()

    def setWeaponEffectForbidden(self, value):
        self.leftWeaponModel.setEffectForbidden(value)
        self.rightWeaponModel.setEffectForbidden(value)
        weaponBackup = self.leftWeaponBackup + self.rightWeaponBackup
        for weapon in weaponBackup:
            weapon.setEffectForbidden(value)

    def _setWeaponCaps(self, attachWeapon, entity, weapon):
        equipType = None
        if attachWeapon and weapon:
            equipType = weapon.equipType
            if not (hasattr(entity, '_isOnZaiju') and entity._isOnZaiju()):
                if equipType and hasattr(weapon, 'getWeaponMatchCaps'):
                    if getattr(entity, 'schoolSwitchNo', None) and not entity.getWeapon(True) and not entity.getWeapon(False):
                        pass
                    else:
                        entity.fashion.setWeaponCaps([equipType])
                elif hasattr(weapon, 'isActionWear') and weapon.isActionWear():
                    entity.am.matchCaps = [equipType, keys.CAPS_WEAR]
            elif self.entity.weaponInHandState() == gametypes.WEAPON_BUFF_ATTACH:
                if hasattr(weapon, 'isActionWear') and weapon.isActionWear():
                    entity.am.matchCaps = [equipType, keys.CAPS_WEAR]
            entity.fashion.weaponType = equipType
        else:
            entity.fashion.weaponType = 0
            if hasattr(weapon, 'isActionWear') and weapon.isActionWear():
                caps = entity.am.matchCaps
                newCaps = [keys.CAPS_HAND_FREE]
                if keys.CAPS_WEAR in caps:
                    caps.remove(keys.CAPS_WEAR)
                if len(newCaps) == 1:
                    newCaps.append(keys.CAPS_GROUND)
                entity.am.matchCaps = newCaps
            else:
                entity.fashion.setWeaponCaps([keys.CAPS_HAND_FREE])

    def _setWearModelCaps(self, attachWeapon, entity, weapon):
        if weapon:
            if attachWeapon:
                for item in weapon.models:
                    model = item[0]
                    try:
                        am = model.motors[0]
                    except:
                        am = BigWorld.ActionMatcher(entity)
                        model.motors = (am,)

                    am.matchCaps = [weapon.equipType, keys.CAPS_WEAR]
                    am.matcherCoupled = False
                    am.footTwistSpeed = 0.0
                    entity.am.addChild(am)

            else:
                for item in weapon.models:
                    model = item[0]
                    if model.motors and model.motors[0].__name__ == 'ActionMatcher':
                        entity.am.delChild(model.motors[0])

    def _checkWeaponStateChanged(self, weapon, isLeftWeapon = False):
        oldState = weapon.state
        if oldState == weaponModel.DATA_ERROR:
            return False
        newState = weaponModel.ATTACHED
        if self.entity.weaponInHandState() == gametypes.WEAPON_DOUBLEATTACH:
            if isLeftWeapon:
                if self.entity.realSchool in (const.SCHOOL_GUANGREN, const.SCHOOL_YANTIAN):
                    newState = oldState
                elif self.entity.realSchool == const.SCHOOL_LIUGUANG:
                    newState = weaponModel.HANG_UP
                else:
                    newState = weapon.attachType
            else:
                newState = weapon.attachType
        elif self.entity.weaponInHandState() == gametypes.WEAPON_DOUBLEATTACH_ALL:
            newState = weaponModel.ATTACHED
        elif self.entity.weaponInHandState() == gametypes.WEAPON_HANDFREE:
            newState = weaponModel.HANG_UP
        elif self.entity.weaponInHandState() == gametypes.WEAPON_DOUBLEHIDE:
            newState = weaponModel.DETACHED
        elif self.entity.weaponInHandState() == gametypes.WEAPON_ALLATTACH:
            newState = weaponModel.ATTACHED
        elif self.entity.weaponInHandState() == gametypes.WEAPON_CHANGE_CAPS:
            newState = weaponModel.HANG_UP
        return newState != oldState

    def refreshWeaponStateWithAct(self, haveAct = True):
        entity = self.entity
        fashion = entity.fashion
        leftStateChanged = self._checkWeaponStateChanged(self.leftWeaponModel, True)
        rightStateChanged = self._checkWeaponStateChanged(self.rightWeaponModel)
        delayActTime = 0
        callback = None
        weapon = self._getWeaponModel(entity.weaponInHandState())
        if entity.weaponInHandState() == gametypes.WEAPON_DOUBLEATTACH:
            self._setWeaponCaps(True, entity, weapon)
            if leftStateChanged or rightStateChanged or fashion.doingActionType() == action.HANG_WEAPON_ACTION:
                if rightStateChanged:
                    weapon = self.rightWeaponModel
                elif leftStateChanged:
                    weapon = self.leftWeaponModel
                if haveAct and not entity.inMoving() and fashion.doingActionType() in (action.UNKNOWN_ACTION,) and not entity.bufActState:
                    actName = fashion.action.getShowWeaponAction(fashion)
                    try:
                        actObj = entity.model.action(actName)
                    except:
                        actObj = None

                    if actObj:
                        if self.backwear.isActionAsEntityWear():
                            self.backwear.doAction(actName)
                        fashion.doAction(actObj, action.SHOW_WEAPON_ACTION, 0, None, 0, 1, 0, True)
                        actObj.haveCue(2)
                if entity.realSchool in SCHOOL_ATTACH_RIGHT_WEAPON:
                    callback = Functor(self.attachWeapon1, haveAct)
                else:
                    callback = Functor(self.attachWeapon, haveAct)
                if fashion.weaponCallback:
                    BigWorld.cancelCallback(fashion.weaponCallback[0])
                    fashion.weaponCallback = None
                if delayActTime > 0:
                    handle = BigWorld.callback(delayActTime, callback)
                    fashion.weaponCallback = (handle, callback)
                else:
                    callback()
        elif entity.weaponInHandState() == gametypes.WEAPON_HANDFREE:
            if leftStateChanged or rightStateChanged or self.tempWeaponModel and self.tempWeaponModel.state == weaponModel.ATTACHED or fashion.doingActionType() == action.SHOW_WEAPON_ACTION:
                if haveAct and not entity.inMoving() and fashion.doingActionType() in (action.UNKNOWN_ACTION,) and not entity.bufActState:
                    actName = fashion.action.getHangWeaponAction(fashion)
                    try:
                        actObj = entity.model.action(actName)
                    except:
                        actObj = None

                    if actObj:
                        fashion.doAction(actObj, action.HANG_WEAPON_ACTION, 0, None, 0, 1, 0, True)
                        actObj.haveCue(2)
                        if self.backwear.isActionAsEntityWear():
                            self.backwear.doAction(actName)
                if fashion.weaponCallback:
                    BigWorld.cancelCallback(fashion.weaponCallback[0])
                    fashion.weaponCallback = None
                callback = Functor(self.hangUpWeapon, haveAct)
                if delayActTime:
                    handle = BigWorld.callback(delayActTime, callback)
                    fashion.weaponCallback = (handle, callback)
                else:
                    callback()
            if self.backwear.isAttached() or self.waistwear.isAttached():
                wear = None
                if self.backwear.isAttached():
                    wear = self.backwear
                else:
                    wear = self.waistwear
                self.hangUpBackAndWaist()
                if haveAct:
                    self.showWearAction(False, wear)
                self._setWeaponCaps(False, entity, wear)
            if self.buffModel.isAttached():
                self._setWeaponCaps(False, entity, self.buffModel)
            else:
                self._setWeaponCaps(False, entity, weapon)
        elif entity.weaponInHandState() == gametypes.WEAPON_MIDATTACH:
            self._setWeaponCaps(True, entity, weapon)
            self.attachWeapon2()
        elif entity.weaponInHandState() == gametypes.WEAPON_DOUBLEATTACH_ALL:
            self._setWeaponCaps(True, entity, weapon)
            self.attachWeapon3()
        elif entity.weaponInHandState() >= gametypes.WEAPON_BACKUP_BOUND and entity.weaponInHandState() < gametypes.WEAPON_MIDATTACH_WITH_ZHUSHOU:
            self._setWeaponCaps(True, entity, weapon)
            self.attachWeaponBackup(weapon)
        elif entity.weaponInHandState() == gametypes.WEAPON_DOUBLEHIDE:
            self._setWeaponCaps(True, entity, weapon)
            self.hideWeapon1()
        elif entity.weaponInHandState() == gametypes.WEAPON_ALLATTACH:
            self._setWeaponCaps(True, entity, weapon)
            self.attachWeapon()
        elif entity.weaponInHandState() == gametypes.WEAR_BACK_ATTACH:
            if self.backwear and hasattr(self.backwear, 'isActionJustSkillWear') and self.backwear.isActionJustSkillWear():
                pass
            else:
                self._setWeaponCaps(True, entity, self.backwear)
                self._setWearModelCaps(True, entity, self.backwear)
                self.attachWear('backwear')
                if haveAct:
                    self.showWearAction(True, self.backwear)
        elif entity.weaponInHandState() == gametypes.WEAR_WAIST_ATTACH:
            if self.waistwear and hasattr(self.waistwear, 'isActionJustSkillWear') and self.waistwear.isActionJustSkillWear():
                pass
            else:
                self._setWeaponCaps(True, entity, self.waistwear)
                self._setWearModelCaps(True, entity, self.waistwear)
                self.attachWear('waistwear')
                if haveAct:
                    self.showWearAction(True, self.waistwear)
        elif entity.weaponInHandState() == gametypes.WEAPON_CHANGE_CAPS:
            self._setWeaponCaps(True, entity, weapon)
            self.hangUpWeapon()
        elif entity.weaponInHandState() == gametypes.WEAPON_MIDATTACH_WITH_ZHUSHOU:
            self._setWeaponCaps(True, entity, weapon)
            self.attachWeapon4(weaponModel.ATTACHED_MID_WEAPON_ALL)
        elif entity.weaponInHandState() == gametypes.WEAPON_MIDATTACH_WITH_ZHUSHOU_LEFT:
            self._setWeaponCaps(True, entity, weapon)
            self.attachWeapon4(weaponModel.ATTACHED_MID_WEAPON_LEFT)
        elif entity.weaponInHandState() == gametypes.WEAPON_MIDATTACH_WITH_ZHUSHOU_RIGHT:
            self._setWeaponCaps(True, entity, weapon)
            self.attachWeapon4(weaponModel.ATTACHED_MID_WEAPON_RIGHT)
        elif entity.weaponInHandState() == gametypes.WEAPON_BUFF_ATTACH:
            self._setWeaponCaps(True, entity, weapon)
            self.attachBuffWeapon(self.buffModel)

    def showWearAction(self, attachWear, wear):
        entity = self.entity
        if not entity or not entity.inWorld:
            return
        fashion = entity.fashion
        actName = None
        actType = action.OPEN_WEAR_ACTION
        if attachWear:
            actName = fashion.action.getShowWeaponAction(fashion)
        else:
            actName = fashion.action.getHangWeaponAction(fashion)
            actType = action.CLOSE_WEAR_ACTION
        if actName:
            try:
                actObj = entity.model.action(actName)
            except:
                actObj = None

            if actObj:
                callback = lambda : (entity.updateActionKeyState() if entity == BigWorld.player() else None)
                fashion.doAction(actObj, actType, 0, callback, 0, 1, 0.1, True)
        for item in wear.models:
            model = item[0]
            callback = None
            if not attachWear:
                callback = lambda : (model.tpos() if model and model.inWorld else None)
            if actName:
                BigWorld.callback(0.2, Functor(self._showWearModelAction, model, actName, callback))
            elif callback:
                callback()

    def _showWearModelAction(self, model, actName, callback):
        try:
            if model and model.inWorld:
                model.action(actName)(0, callback, 0, 1.0, 0.1)
        except:
            pass

    def stopWearAction(self, attachWear, wear):
        entity = self.entity
        fashion = entity.fashion
        if not wear.models:
            return
        if entity.model:
            actions = entity.model.queue
            maxBlendOut = 0
            for actName in actions:
                actObj = entity.model.action(actName)
                maxBlendOut = max(maxBlendOut, actObj.blendOutTime)
                fashion.stopActionByName(entity.model, actName)

            BigWorld.callback(maxBlendOut, entity.model.resetSkeleton)
        for item in wear.models:
            model = item[0]
            for actName in model.queue:
                actObj = model.action(actName)
                actObj.stop()
                model.tpos()

    def getShowWear(self, equipPart = 0):
        if not equipPart:
            if self.entity.weaponInHandState() == gametypes.WEAR_BACK_ATTACH:
                if self.backwear.isAttached() or self.backwear.isActionJustSkillWear():
                    return self.backwear
            elif self.entity.weaponInHandState() == gametypes.WEAR_WAIST_ATTACH:
                if self.waistwear.isAttached() or self.waistwear.isActionJustSkillWear():
                    return self.waistwear
        wearName = WEAR_EQU_PART_MAP.get(equipPart, None)
        if wearName:
            return getattr(self, wearName, None)

    def attachWeapon(self, showAct = False):
        leftWeaponId = self.entity.getWeapon(True)
        rightWeaponId = self.entity.getWeapon(False)
        self.detachWeaponBackup()
        self.hangUpBackAndWaist()
        if leftWeaponId:
            self.leftWeaponModel.attach(self.bodyModel, False, haveAct=showAct)
        if rightWeaponId:
            self.rightWeaponModel.attach(self.bodyModel, False, haveAct=showAct)
        if self.entity:
            self.entity.fashion.weaponCallback = None

    def attachWeapon1(self, showAct = False):
        leftWeaponId = self.entity.getWeapon(True)
        rightWeaponId = self.entity.getWeapon(False)
        self.detachWeaponBackup()
        self.hangUpBackAndWaist()
        if leftWeaponId:
            self.leftWeaponModel.hangUp(self.bodyModel, False, haveAct=showAct)
        if rightWeaponId:
            self.rightWeaponModel.attach(self.bodyModel, False, True, haveAct=showAct)
        if self.entity:
            self.entity.fashion.weaponCallback = None

    def attachWeapon2(self, showAct = False):
        leftWeaponId = self.entity.getWeapon(True)
        rightWeaponId = self.entity.getWeapon(False)
        self.detachWeaponBackup()
        self.hangUpBackAndWaist()
        if leftWeaponId:
            self.rightWeaponModel.hangUp(self.bodyModel, False, haveAct=showAct)
        if rightWeaponId:
            self.leftWeaponModel.attach(self.bodyModel, False, haveAct=showAct)
        if self.entity:
            self.entity.fashion.weaponCallback = None

    def attachWeapon3(self, showAct = False):
        leftWeaponId = self.entity.getWeapon(True)
        rightWeaponId = self.entity.getWeapon(False)
        self.detachWeaponBackup()
        self.hangUpBackAndWaist()
        if leftWeaponId:
            self.leftWeaponModel.hangUp(self.bodyModel, False, haveAct=showAct)
        if rightWeaponId:
            self.rightWeaponModel.attach(self.bodyModel, False, haveAct=showAct)
        if self.entity:
            self.entity.fashion.weaponCallback = None

    def attachWeapon4(self, attachType, showAct = False):
        leftWeaponId = self.entity.getWeapon(True)
        rightWeaponId = self.entity.getWeapon(False)
        self.detachWeaponBackup()
        self.hangUpBackAndWaist()
        self.rightWeaponModel.state = weaponModel.ATTACHED_MID_WEAPON_RIGHT
        if leftWeaponId:
            self.leftWeaponModel.attach(self.bodyModel, False, haveAct=showAct, attachType=attachType)
        if self.entity:
            self.entity.fashion.weaponCallback = None

    def attachBuffWeapon(self, buffModel):
        if not self.entity:
            return
        self.detachWeaponBackup()
        self.hangUpWeapon()
        if buffModel:
            buffModel.attach(self.bodyModel)

    def getWeaponModelPart(self, zhuShou, rightHand):
        if zhuShou:
            if self.rightWeaponModel:
                return self.rightWeaponModel.getWeaponModelPart(rightHand)
        elif self.leftWeaponModel:
            return self.leftWeaponModel.getWeaponModelPart(rightHand)

    def hangUpWeapon(self, showAct = False):
        if not self.entity:
            return
        leftWeaponId = self.entity.getWeapon(True)
        rightWeaponId = self.entity.getWeapon(False)
        self.detachWeaponBackup()
        if leftWeaponId:
            self.leftWeaponModel.hangUp(self.bodyModel, haveAct=showAct)
        if rightWeaponId:
            self.rightWeaponModel.hangUp(self.bodyModel, haveAct=showAct)
        if self.entity:
            self.entity.fashion.weaponCallback = None

    def hangUpWear(self, wear):
        if not self.entity:
            return
        aspect = self.entity.realAspect
        wearId = getattr(aspect, wear)
        if wearId:
            getattr(self, wear).hangUp(self.bodyModel)

    def hangUpBackAndWaist(self):
        entity = self.entity
        self._setWearModelCaps(False, entity, self.backwear)
        self._setWearModelCaps(False, entity, self.waistwear)
        self.hangUpWear('backwear')
        self.hangUpWear('waistwear')

    def attachWear(self, wear):
        if not self.entity:
            return
        aspect = self.entity.realAspect
        wearId = getattr(aspect, wear)
        self.detachWeaponBackup()
        self.hangUpWeapon()
        if wearId:
            getattr(self, wear).attach(self.bodyModel)

    def bodyUpdate(self):
        gamelog.debug('jorsef: bodyUpdate', self.bodyUpdateStatus)
        entity = self.entity
        if not entity or not entity.inWorld:
            return
        if not seqTask.shouldLoadRealModel(entity):
            if not entity.model:
                model = sfx.getDummyModel(False)
                entity.model = model
            self.bodyUpdateStatus = BODY_UPDATE_STATUS_NORMAL
            entity.firstFetchFinished = True
            entity.afterModelFinish()
            return
        if self.bodyUpdateStatus == BODY_UPDATE_STATUS_NORMAL:
            self.bodyUpdateStatus = BODY_UPDATE_STATUS_UPDATING
        else:
            self.bodyUpdateStatus = BODY_UPDATE_STATUS_UPDATE_CACHING
            return
        if self.bodyModelLoader:
            mpr = charRes.MultiPartRes()
            mpr.queryByAvatar(self.entity)
            res = mpr.getPrerequisites()
            self.bodyModelLoader.modelOkCallback = self._bodyModelFinish
            self.bodyModelLoader.beginLoad(res, self.urgent)

    def isReady(self):
        return self.bodyUpdateStatus == BODY_UPDATE_STATUS_NORMAL

    def bodyPartsUpdate(self, fashionShowChanged, clanWarShowChanged = False, wenquanChanged = False, neiYiBuffChanged = False, fashionHeadChanged = False, interactiveChangeFashionIdOld = 0):
        if self.bodyUpdateStatus != BODY_UPDATE_STATUS_NORMAL:
            self.bodyUpdateStatus = BODY_UPDATE_STATUS_UPDATE_CACHING
            return
        if not self.entity.isRealModel:
            return
        showFashion = self.entity.isShowFashion()
        showClanWar = self.entity.isShowClanWar()
        inWenQuan = getattr(self.entity, 'inWenQuanState', False)
        neiYiBuffState = self.entity.checkNeiYiBuff()
        isHideFashionHead = self.entity.isHideFashionHead()
        interactiveChangeFashionId = getattr(self.entity, 'interactiveChangeFashionId', 0)
        mprOld = charRes.MultiPartRes()
        mprOld.applyConfig = False
        mprOld.isAvatar = True
        showFashionOld = not showFashion if fashionShowChanged else showFashion
        showClanWarOld = not showClanWar if clanWarShowChanged else showClanWar
        inWenQuanOld = not inWenQuan if wenquanChanged else inWenQuan
        neiYiBuffStateOld = not neiYiBuffState if neiYiBuffChanged else neiYiBuffState
        isHideFashionHeadOld = not isHideFashionHead if fashionHeadChanged else isHideFashionHead
        mprOld.queryByAttribute(self.entity.physiqueOld, self.entity.aspectOld, showFashionOld, None, showClanWarOld, inWenQuanOld, neiYiBuffStateOld, isHideFashionHeadOld, interactiveChangeFashionId=interactiveChangeFashionIdOld)
        resOld = mprOld.getPrerequisites()
        mpr = charRes.MultiPartRes()
        mpr.applyConfig = False
        mpr.isAvatar = True
        mpr.queryByAttribute(self.entity.realPhysique, self.entity.realAspect, showFashion, None, showClanWar, inWenQuan, neiYiBuffState, isHideFashionHead, interactiveChangeFashionId=interactiveChangeFashionId)
        res = mpr.getPrerequisites()
        model = self.bodyModel
        tints = tintalt._get_matter_tint_data(model)
        self.entity.partsUpdating = True
        self.bodyModelUpdater.model = model
        resOld, res = self._getRealBodyPartRes(resOld, res)
        if showClanWar and not showClanWarOld:
            for i, oldItem in enumerate(resOld):
                if oldItem.endswith('head.model'):
                    for item in model.sources:
                        if item.endswith('head.model'):
                            index = item.find('char')
                            if index != -1 and oldItem == item[index:]:
                                resOld[i] = item
                            break

                    break

        self.bodyModelUpdater.beginUpdate(resOld, res, mprOld.dyesDict, mpr.dyesDict, tints)

    def _getRealBodyPartRes(self, resOld, resNew):
        old = []
        new = []
        for res in resOld:
            if type(res) == str:
                old.append(res)

        for res in resNew:
            if type(res) == str:
                new.append(res)

        return (old, new)

    def _bodyPartsUpdateFinish(self):
        if not self.entity:
            return
        self.entity.partsUpdating = False
        self.entity.afterPartsUpdateFinish()
        if gameglobal.gEnableFootIK and self.entity.fashion.isPlayer:
            self.entity.model.footIK = BigWorld.FootIK()
            self.entity.resetFootIK()
        if hasattr(self.entity, 'isInCoupleRide') and self.entity.isInCoupleRideAsRider():
            self.hangWomanOnMan(False)
        mpr = charRes.MultiPartRes()
        mpr.queryByAvatar(self.entity)
        if mpr.headType == charRes.HEAD_TYPE1:
            self.hairChange = HAIR_NODE_DETACH
        elif self.hairNodeModel and self.hairNodeModel.sources[0] == mpr.getHairPath():
            self.hairChange = HAIR_NODE_NO_CHANGE
        else:
            self.hairChange = HAIR_NODE_CHANGE
        if self.hairChange == HAIR_NODE_CHANGE:
            self.loadHairNode(self.attachHairNode)
        elif self.hairChange == HAIR_NODE_DETACH:
            self.detachHairNode()
        self.refreshHeadWearState()

    def fadeToReal(self, fadeTime):
        if self.leftWeaponModel:
            self.leftWeaponModel.fadeToReal(fadeTime)
        if self.rightWeaponModel:
            self.rightWeaponModel.fadeToReal(fadeTime)

    def realToFade(self, fadeTime):
        if self.leftWeaponModel:
            self.leftWeaponModel.realToFade(fadeTime)
        if self.rightWeaponModel:
            self.rightWeaponModel.realToFade(fadeTime)

    def equipmentChanged(self, pos, value):
        self.weaponUpdate()

    def getMainModelAndID(self):
        owner = self.entity
        return (owner.fashion.modelID, owner.model)

    def _bodyModelFinish(self, model):
        if not self.entity or not self.entity.inWorld:
            return
        if not model:
            gamelog.error('Error _bodyModelFinish, model is None', self.entity.id)
            return
        weaponModels = [self.leftWeaponModel, self.rightWeaponModel]
        for m in weaponModels:
            if m.state != weaponModel.DATA_ERROR and m.state != weaponModel.DETACHED:
                m.detach()

        entity = self.entity
        self.bodyModel = model
        self.state = STATE_HUMAN
        entity.fashion.setupModel(model)
        self.refreshWeaponState()
        self.loadHairNode(self.attachHairNode)
        self.refreshOtherWearState()
        self.refreshHeadWearState()
        if self.onModelFinishedCall:
            self.onModelFinishedCall(model)
        entity.firstFetchFinished = True
        entity.afterModelFinish()
        if entity.fashion.isPlayer:
            self.eyeBallCtrl.setTargetModel(model)
            self.headCtrl.setTargetModel(model)
        if gameglobal.rds.GameState > gametypes.GS_LOGIN:
            entity.refreshOpacityState()
        self.updateHumanState()
        BigWorld.callback(0.1, self.checkBodyRefresh)
        if hasattr(entity, 'isInCoupleRide') and entity.isInCoupleRide():
            self.hangWomanOnMan()
        if hasattr(entity, 'isRidingTogether') and entity.isRidingTogether():
            if entity.tride.isMajor(entity.id):
                for mid, idx in entity.tride.iteritems():
                    self.hangViceOnMain(entity.id, mid, idx)

            else:
                header = entity.tride.header
                idx = entity.tride.get(entity.id, 0)
                if idx:
                    self.hangViceOnMain(header, entity.id, idx)
        if hasattr(entity, 'inCarrousel') and entity.inCarrousel():
            self.enterCarrousel()
        if hasattr(entity, 'refreshEquipEnhanceEffects'):
            entity.refreshEquipEnhanceEffects()
        if hasattr(entity, 'inRoundTable') and entity.inRoundTable():
            self.enterRoundTable()
        if hasattr(entity, 'attachSkillData') and entity.attachSkillData[0]:
            self.enterAttachSkill(entity.id, entity.attachSkillData[0])
        if hasattr(entity, 'inInteractiveObject') and entity.inInteractiveObject():
            self.enterInteractiveObject()
        if hasattr(entity, 'coupleEmote') and entity.isInCoupleRide():
            self.enterCoupleEmote()
        if hasattr(entity, 'carrier') and entity.carrier.isRunningState():
            if entity.carrier.has_key(entity.id):
                self.enterCarrier()
        if hasattr(entity, 'wingWorldCarrier') and entity.wingWorldCarrier.has_key(entity.id):
            self.enterWingWorldCarrier()

    def checkBodyRefresh(self):
        if self.bodyUpdateStatus == BODY_UPDATE_STATUS_UPDATE_CACHING:
            self.bodyUpdateStatus = BODY_UPDATE_STATUS_NORMAL
            self.bodyUpdate()
        else:
            self.bodyUpdateStatus = BODY_UPDATE_STATUS_NORMAL

    def checkCanSetPose(self):
        return self.bodyUpdateStatus == BODY_UPDATE_STATUS_UPDATING

    def updateHumanState(self):
        owner = self.entity
        owner.firstFetchFinished = True
        if owner.fashion == None or not owner.inWorld or not owner.IsAvatar:
            return
        self.state = STATE_HUMAN
        owner.fashion.setGuard(owner.inCombat)
        owner.updateBodySlope()
        owner.am.applyFlyRoll = False

    def equipWeapon(self, weaponId, isLeftWeapon, ehnLv):
        if isLeftWeapon:
            weapon = self.leftWeaponModel
            weaponBackup = self.leftWeaponBackup
        else:
            weapon = self.rightWeaponModel
            weaponBackup = self.rightWeaponBackup
        ed = ED.data.get(weaponId, {})
        subIdList = ed.get('subId', [])
        weapon.equipItem(weaponId, 0, ehnLv)
        for item in weaponBackup:
            item.release()

        for i in xrange(1, len(subIdList)):
            if i - 1 < len(weaponBackup):
                tempWeaponModel = weaponBackup[i - 1]
                tempWeaponModel.equipItem(weaponId, i, ehnLv)
            else:
                tempWeaponModel = weaponModel.WeaponModel(self.entity.id, self.threadID)
                tempWeaponModel.equipItem(weaponId, i, ehnLv)
                weaponBackup.append(tempWeaponModel)

    def detachWeaponBackup(self):
        if not self.entity:
            return
        leftWeaponId = self.entity.getWeapon(True)
        rightWeaponId = self.entity.getWeapon(False)
        if leftWeaponId:
            for weapon in self.leftWeaponBackup:
                weapon.hangUp(self.bodyModel)

        if rightWeaponId:
            for weapon in self.rightWeaponBackup:
                weapon.hangUp(self.bodyModel)

        self.tempWeaponModel = None

    def attachWeaponBackup(self, weapon):
        self.hangUpWeapon()
        self.detachWeaponBackup()
        if weapon:
            weapon.attach(self.bodyModel, False)
            self.tempWeaponModel = weapon

    def showOtherwears(self, show):
        models = self.getOtherWearModels()
        for m in models:
            m.visible = show

    def getOtherWearModels(self):
        models = []
        for wear in self.otherwears:
            wearAttachedModel = getattr(self, wear)
            if wearAttachedModel:
                for i in wearAttachedModel.models:
                    models.append(i[0])

        return models

    def hideWeapon1(self):
        leftWeaponId = self.entity.getWeapon(True)
        rightWeaponId = self.entity.getWeapon(False)
        self.detachWeaponBackup()
        if leftWeaponId:
            self.leftWeaponModel.hangUp(self.bodyModel, False)
        if rightWeaponId:
            self.rightWeaponModel.detach()
        if self.entity:
            self.entity.fashion.weaponCallback = None

    def _getWeaponModel(self, weaponState, weaponType = gameglobal.WEAPON_ALL):
        if weaponState in (gametypes.WEAPON_DOUBLEATTACH,
         gametypes.WEAPON_DOUBLEATTACH_ALL,
         gametypes.WEAPON_DOUBLEHIDE,
         gametypes.WEAPON_CHANGE_CAPS):
            if self.entity.realSchool in (const.SCHOOL_GUANGREN, const.SCHOOL_YANTIAN):
                return self.rightWeaponModel
            elif weaponType == gameglobal.WEAPON_LEFT:
                return self.leftWeaponModel
            else:
                return self.rightWeaponModel
        else:
            if weaponState in (gametypes.WEAPON_MIDATTACH,
             gametypes.WEAPON_MIDATTACH_WITH_ZHUSHOU,
             gametypes.WEAPON_MIDATTACH_WITH_ZHUSHOU_LEFT,
             gametypes.WEAPON_MIDATTACH_WITH_ZHUSHOU_RIGHT):
                return self.leftWeaponModel
            if weaponState == gametypes.WEAPON_ALLATTACH:
                return self.rightWeaponModel
            if weaponState == gametypes.WEAPON_HANDFREE:
                return None
            if weaponState == gametypes.WEAPON_BUFF_ATTACH:
                return self.buffModel
            state = weaponState / 10
            subState = weaponState % 10
            if state == gametypes.WEAPON_DOUBLEATTACH:
                weaponBackup = self.rightWeaponBackup
            else:
                weaponBackup = self.leftWeaponBackup
            if subState < len(weaponBackup):
                weapon = weaponBackup[subState]
                return weapon

    def _getAllWeaponModel(self):
        weaponBackup = self.leftWeaponBackup + self.rightWeaponBackup
        return weaponBackup + [self.leftWeaponModel, self.rightWeaponModel]

    def getAllWeaponModels(self):
        ms = []
        models = self._getAllWeaponModel()
        if models:
            for model in models:
                if model:
                    tms = model.getModels()
                    if tms:
                        ms.extend(tms)

        return ms

    def getAllAttachedModels(self):
        models = []
        wears = self.headdresses + self.headwear + self.otherwears
        for wear in wears:
            wearAttach = getattr(self, wear)
            if wearAttach and getattr(wearAttach, 'models'):
                for info in wearAttach.models:
                    if info and info[0]:
                        models.append(info[0])

        if hasattr(self, 'rideAttached') and self.rideAttached:
            models.extend(self.rideAttached.getAttachedModel())
        return models

    def updateWeaponAction(self):
        self.leftWeaponModel.updateWeaponAction()
        self.rightWeaponModel.updateWeaponAction()
        weaponBackup = self.leftWeaponBackup + self.rightWeaponBackup
        for weapon in weaponBackup:
            if weapon:
                weapon.updateWeaponAction()

        if self.yuanLing:
            self.yuanLing.updateWeaponAction()

    def updateWeaponEffect(self):
        self.leftWeaponModel.updateWeaponEffect()
        self.rightWeaponModel.updateWeaponEffect()
        weaponBackup = self.leftWeaponBackup + self.rightWeaponBackup
        for weapon in weaponBackup:
            if weapon:
                weapon.updateWeaponEffect()

    def updateWearEffect(self):
        wears = self.headdresses + self.headwear + self.otherwears
        for wear in wears:
            wearAttach = getattr(self, wear)
            wearAttach.updateWeaponEffect()
            if wearAttach.isActionAsEntityWear() and wearAttach.model:
                wearAttach.addActionMatcher(wearAttach.model)

        self.showHairNodeAction()
        self.updateGdHairEffect()

    def playWeaponAction(self, actions):
        models = self.entity.fashion.getWeaponModels()
        for model in models:
            if model:
                self.entity.fashion.playActionSequence(model, actions, None)

    def playAllWeaponAction(self, act, scale = 1):
        models = self.entity.fashion.getWeaponModels()
        for model in models:
            if model and model.inWorld and act in model.actionNameList():
                model.action(act)(0, None, 0, scale)

    def playLeftWeaponAction(self, act, scale = 1):
        models = self.entity.fashion.getWeaponModels(gameglobal.WEAPON_LEFT)
        for model in models:
            if model and model.inWorld and act in model.actionNameList():
                model.action(act)(0, None, 0, scale)

    def playRightWeaponAction(self, act, scale = 1):
        models = self.entity.fashion.getWeaponModels(gameglobal.WEAPON_RIGHT)
        for model in models:
            if model and model.inWorld and act in model.actionNameList():
                model.action(act)(0, None, 0, scale)


class IMonsterCommon(object):

    def attachHairModel(self, callback = None):
        entity = self.entity
        if not entity or not entity.inWorld:
            return
        hairNodePath = getHairNodeModel(entity.model)
        if hairNodePath:
            charRes.getSimpleModel(hairNodePath, None, Functor(self._afterHiarModelFinished, callback))
        elif callback:
            callback(None)

    def _afterHiarModelFinished(self, callback, hairModel):
        entity = self.entity
        if not entity or not entity.inWorld:
            return
        if hairModel:
            node = entity.model.node('biped Head')
            if node and hairModel not in node.attachments:
                node.attach(hairModel, 'biped Head')
            try:
                hairModel.action('1101')()
            except:
                pass

        if callback:
            callback(hairModel)

    def attachEffectFromData(self, model):
        entity = self.entity
        itemData = entity.getItemData()
        attaches = itemData.get('attaches', None)
        if attaches == None:
            return
        for attach in attaches:
            modelPrefix = 'item/model'
            if len(attach) == 6:
                attachHp, attachModel, attachEff, attachScale, attachEffScale, modelPrefix = attach
            else:
                attachHp, attachModel, attachEff, attachScale, attachEffScale = attach
            if attachEffScale <= 0:
                attachEffScale = 1
            if attachEff:
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
                 entity.getEquipEffectPriority(),
                 model,
                 attachEff,
                 sfx.EFFECT_LIMIT_MISC))
                if fx:
                    for fxItem in fx:
                        fxItem.scale(attachEffScale, attachEffScale, attachEffScale)

                    entity.attachedDataEffects = fx
                if hasattr(entity, 'addFx'):
                    entity.addFx(attachEff, fx)

    def attachModelFromData(self):
        entity = self.entity
        if not entity or not entity.inWorld:
            return
        self.attachHairModel(self._attachModelFromData)

    def _attachModelFromData(self, hairModel = None):
        entity = self.entity
        if not entity or not entity.inWorld:
            return
        itemData = entity.getItemData()
        attaches = itemData.get('attaches', None)
        if attaches == None:
            return
        try:
            if not entity.__class__.__name__ == 'DynamicSceneObject':
                self.attachEffectFromData(entity.model)
            for attach in attaches:
                modelPrefix = ''
                if len(attach) == 6:
                    attachHp, attachModel, attachEff, attachScale, attachEffScale, modelPrefix = attach
                else:
                    attachHp, attachModel, attachEff, attachScale, attachEffScale = attach
                if not modelPrefix:
                    modelPrefix = 'item/model'
                if attachEffScale <= 0:
                    attachEffScale = 1
                if attachScale <= 0:
                    attachScale = 1
                if attachModel and attachHp:
                    if self.attachModel.has_key(attachHp):
                        model = self.attachModel[attachHp][0]
                        hairModel = self.attachModel[attachHp][2]
                        bodyModel = entity.model.ride if self.state == STATE_HORSE else entity.model
                        node = bodyModel.node('biped Head')
                        if hairModel and node and hairModel not in node.attachments:
                            node.attach(hairModel, 'biped Head')
                        if hairModel:
                            bodyModel = hairModel
                        bodyModel.setHP(attachHp, None)
                        bodyModel.setHP(attachHp, model)
                        bodyModel.node(attachHp).scale(attachScale, attachScale, attachScale)
                        self.attachModel[attachHp] = (model, attachScale, hairModel)
                    else:
                        modelPath = '%s/%s' % (modelPrefix, attachModel)
                        callback = Functor(self._afterAttachModelFinished, entity, attachHp, attachScale, modelPath, modelPrefix, hairModel)
                        charRes.getSimpleModel(modelPath, None, callback)

        except:
            raise Exception('_attachModelFromData error %s,%s' % (entity.__class__.__name__, str(entity.getItemData())))

    def _afterAttachModelFinished(self, entity, attachHp, attachScale, modelPath, modelPrefix, hairModel, model):
        if not entity or not entity.model:
            return
        try:
            bodyModel = entity.model
            if modelPrefix and modelPrefix.endswith('headdress') and hairModel:
                bodyModel = hairModel
            elif self.state == STATE_HORSE:
                bodyModel = entity.model.ride
            bodyModel.setHP(attachHp, None)
            bodyModel.setHP(attachHp, model)
            bodyModel.node(attachHp).scale(attachScale, attachScale, attachScale)
            self.attachModel[attachHp] = (model, attachScale, hairModel)
        except:
            if BigWorld.isPublishedVersion():
                return
            entInfo = ''
            if hasattr(entity, 'npcId'):
                entInfo = 'npc %d:' % entity.npcId
            elif hasattr(entity, 'charType'):
                entInfo = 'monster %d:' % entity.charType
            if not model.node(attachHp):
                raise Exception('%s model %s hpPoint %s' % (entInfo, modelPath, attachHp))
            elif not bodyModel.node(attachHp):
                raise Exception('%s model %s hpPoint %s' % (entInfo, bodyModel.sources[0], attachHp))


class AvatarMonsterModelServer(MultiModelServer, IMonsterCommon):

    def __init__(self, entity):
        super(AvatarMonsterModelServer, self).__init__(entity)
        self.attachModel = {}

    def _bodyModelFinish(self, model):
        super(AvatarMonsterModelServer, self)._bodyModelFinish(model)
        self.entity.model.setModelNeedHide(True, 1.0)
        self.playBornAction()
        self.attachModelFromData()

    def playBornAction(self):
        entity = self.entity
        playSeq = []
        if hasattr(entity, 'bornActionName') and entity.bornActionName:
            playSeq.append(entity.bornActionName)
            entity.bornActionName = None
        if playSeq:
            entity.fashion.playActionSequence(entity.model, playSeq, None)

    def bodyUpdate(self):
        gamelog.debug('jorsef: bodyUpdate', self.bodyUpdateStatus)
        entity = self.entity
        if not entity or not entity.inWorld:
            return
        if self.bodyUpdateStatus == BODY_UPDATE_STATUS_NORMAL:
            self.bodyUpdateStatus = BODY_UPDATE_STATUS_UPDATING
        else:
            self.bodyUpdateStatus = BODY_UPDATE_STATUS_UPDATE_CACHING
            return
        if self.bodyModelLoader:
            if hasattr(self.entity, 'avatarInfo') and self.entity.avatarInfo:
                mpr = charRes.convertToMultiPartRes(self.entity.avatarInfo, self.entity.id)
            else:
                mpr = charRes.MultiPartRes()
                mpr.queryByAvatar(self.entity)
            res = mpr.getPrerequisites()
            self.bodyModelLoader.modelOkCallback = self._bodyModelFinish
            self.bodyModelLoader.beginLoad(res, self.urgent)


class AvatarModelServer(MultiModelServer):

    def __init__(self, entity):
        super(AvatarModelServer, self).__init__(entity)
        self.rideID = 0
        self.rideModel = None
        self.rideAttached = attachedModel.BeastAttachModel(entity.id, self.threadID)
        self.ridePitch = True
        self.boothModel = None
        self.wingFlyModel = attachedModel.WingFlyAttachModel(entity.id, self.threadID)
        self.fishingModel = attachedModel.FishingAttachModel(entity.id, self.threadID)
        self.lifeSkillModel = attachedModel.LifeSkillAttachModel(entity.id, self.threadID)
        self.socialActionModel = weaponModel.WeaponModel(entity.id, self.threadID)
        self.carrouselAniModel = None
        self.playingCarrouselAni = False
        self.playingCarrouselAniIdx = 0
        self.coupleEmoteEffects = []
        self.coupleEmoteKeepEffects = []
        self.coupleModel = None
        self.eyeBallCtrl = faceEmote.EyeBallCtrl()
        self.headCtrl = faceEmote.HeadCtrl()
        self.poseManager = poseManager.PoseManager(entity.id)
        self.cloneModel = None
        self.keepEffect = []
        self.horseAttachedEffect = []
        self.boothModelId = 0
        self.boothModelScale = 1.0
        self.fashionEffects = []
        self.oldInteractiveObjectEntId = -1
        self.coupleEmoteStartEffs = []
        self.fashionIdleEffects = {}
        self.rideFadeInOutCB = None
        self.rideFadeTintName = None

    def setThreadID(self, threadID):
        super(AvatarModelServer, self).setThreadID(threadID)
        self.wingFlyModel.threadID = threadID
        self.rideAttached.threadID = threadID
        self.fishingModel.threadID = threadID
        self.lifeSkillModel.threadID = threadID
        self.socialActionModel.threadID = threadID

    def release(self):
        super(AvatarModelServer, self).release()
        if self.poseManager:
            self.poseManager.release()
        self.eyeBallCtrl.releaseEyeCtrl()
        self.eyeBallCtrl = None
        self.headCtrl.releaseHeadCtrl()
        self.headCtrl = None
        self.rideModel = None
        self.rideAttached.release()
        self.rideAttached = None
        self.wingFlyModel.release()
        self.wingFlyModel = None
        self.fishingModel.release()
        self.fishingModel = None
        self.lifeSkillModel.release()
        self.lifeSkillModel = None
        self.socialActionModel.release()
        self.socialActionModel = None
        for ef in self.keepEffect:
            if ef:
                ef.stop()

        self.keepEffect = []
        self.releaseHorseAttachedEffect()
        self.releaseFashionEffect()

    def wingFlyModelUpdate(self, modelChange = True):
        if not self.entity.isRealModel:
            return
        aspect = self.entity.realAspect
        enableRandWingFly = gameglobal.rds.configData.get('enableRandWingFly', False)
        if enableRandWingFly:
            wingFlyModelId = self.entity.randWingId if self.entity.randWingId else aspect.wingFly
        else:
            wingFlyModelId = aspect.wingFly
        enhLv = aspect.wingFlyEnhLv()
        dyeList = aspect.wingFlyDyeList()
        if wingFlyModelId:
            if self.entity.isShowClanWar():
                wingFlyModelId = SCD.data.get('armorWingId', gameglobal.ARMOR_WING_ID)
                enhLv = 0
            if modelChange:
                self.wingFlyModel.equipItem(wingFlyModelId, enhLv, dyeList)
            else:
                self.wingFlyModel.updateEffect(wingFlyModelId, enhLv, dyeList)

    def wingModelNeedHide(self):
        needHide = False
        if getattr(self.entity, 'inWingTakeOff', False):
            needHide = True
        return needHide

    def refreshWingModelOpacity(self):
        if not self.wingFlyModel:
            return
        if not getattr(self.wingFlyModel, 'model'):
            return
        model = self.wingFlyModel.model
        if self.wingModelNeedHide():
            model.visible = False
        else:
            model.visible = True

    def refreshWingFlyState(self, withEffect = False, wingInAirEffect = False):
        entity = self.entity
        if entity.inFlyTypeWing():
            self.wingFlyModel.attach(self.bodyModel)
            if withEffect:
                self.wingFlyModel.refreshMountEffect(True)
            if wingInAirEffect:
                for effId in SCD.data.get('wingInAirEffect', ()):
                    sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getBasicEffectLv(),
                     entity.getBasicEffectPriority(),
                     entity.model,
                     effId,
                     sfx.EFFECT_LIMIT,
                     gameglobal.EFFECT_LAST_TIME))

        if entity.inFlyTypeFlyRide():
            self.rideAttached.refreshEffectInAir()
        self.rideAttached.refreshFlyRideMatrials()
        if not entity.inFly:
            if self.wingFlyModel.state != attachedModel.DETACHED:
                self.wingFlyModel.detach()
            if withEffect:
                self.wingFlyModel.refreshMountEffect(False)
            if self.rideAttached:
                self.rideAttached.releaseEffectInAir()
        if entity.inFlyTypeFlyRide():
            if self.rideAttached.flyRideIdleAction:
                entity.fashion.playActionSequence(self.bodyModel, [self.rideAttached.flyRideIdleAction], None)
                entity.playRideTogetherAction(self.rideAttached.flyRideIdleAction)

    def setWeaponCaps(self):
        if getattr(self, 'schoolSwitchNo', None) and not self.getWeapon(True) and not self.getWeapon(False):
            return
        weapon = self._getWeaponModel(self.entity.weaponState)
        self._setWeaponCaps(True, self.entity, weapon)

    def getRideFeetDist(self):
        if self.rideID:
            data = ED.data.get(self.rideID, {})
            subId = data.get('subId', None)
            try:
                subId = subId[0] if subId else subId
            except:
                pass

            horseData = HWCD.data.get(subId, None)
            if horseData:
                gamelog.debug('lihang@getRideFeetDist', horseData, self.rideAttached.scale)
                return horseData[0].get('feetDist', 0) * self.rideAttached.scale
        return 0

    def getMainModelAndID(self):
        entity = self.entity
        modelId = charRes.transBodyType(entity.realPhysique.sex, entity.realPhysique.bodyType)
        return (modelId, self.bodyModel)

    def _bodyModelFinish(self, model):
        super(AvatarModelServer, self)._bodyModelFinish(model)
        entity = self.entity
        if not entity or not entity.inWorld:
            return
        if not entity.fashion.isPlayer:
            entity.model.setModelNeedHide(True, 1.0)
        elif self.checkCanSetPose():
            self.poseManager.setPoseModel()
        if entity.bianshen and entity.bianshen[0] in (gametypes.BIANSHEN_RIDING_RB, gametypes.BIANSHEN_ZAIJU, gametypes.BIANSHEN_BIANYAO) and self.rideModel:
            self.rideOnHorse(False)
        elif entity.canFly():
            entity.resetFly(False)
        elif entity.inBoothing():
            self.enterBooth()
        elif entity.inFishing():
            entity.doStartFish()
        elif entity.inFishingReady() or entity.inFishingHold():
            entity.doReadyFish(entity.fishingStatus)
        elif entity.inDaZuo():
            entity.resetDaZuo()
        elif hasattr(entity, 'isInApprenticeTrain') and entity.isInApprenticeTrain() or entity.isInApprenticeBeTrain():
            entity.replayOtherApprenticeTrainEx()
        self.refreshWingFlyState(False)
        self.updateFashionEffect()
        self.updateFashionIdleEffect()

    def _bodyPartsUpdateFinish(self):
        super(AvatarModelServer, self)._bodyPartsUpdateFinish()
        self.updateFashionEffect()
        self.updateFashionIdleEffect()

    def updateHumanState(self):
        super(AvatarModelServer, self).updateHumanState()
        if self.entity == BigWorld.player():
            self.entity.resetCamera()

    def _wingFlyModelFinished(self, key, model):
        gamelog.debug('_wingFlyModelFinished')

    def enterRideHB(self, beastKey, showEffect = True, enhLv = 0, dyeList = []):
        self.prepareRideHB(beastKey, showEffect, enhLv, dyeList)

    def enterZaiju(self, zaijuKey, showEffect = True, enhLv = 0, dyeList = []):
        dataWithCustom = getEntityZaijuDataWithCustom(self.entity, zaijuKey)
        currentRideModelId = dataWithCustom.get('modelId', 0)
        if self.rideID == zaijuKey and self.rideModel and not self.rideModel.inWorld and self.lastZaijuRideModelId == currentRideModelId:
            if self.rideAttached.zaijuMode == attachedModel.ZAIJU_BEATTACHED:
                self.realAttachZaiju(zaijuKey, showEffect)
            else:
                self._rideModelFinish(self.rideID, showEffect, self.rideModel)
            self._refreshZaijuModel(dataWithCustom)
            return None
        p = BigWorld.player()
        if p.isInBfDota() and gameglobal.rds.configData.get('enableDotaZaijuPreLoad', False):
            zaijuId, preloadModel = p.holdPreloadDotaZaijuModel.get(self.entity.gbId, (0, None))
            if zaijuId == zaijuKey and preloadModel:
                gamelog.info('jbx:preloadSucc', self.entity.gbId, zaijuKey)
                self._rideModelFinish(zaijuKey, showEffect, preloadModel)
                return None
        self.lastZaijuRideModelId = currentRideModelId
        if not self.rideAttached.equipZaiju(zaijuKey, dataWithCustom, showEffect, enhLv, dyeList):
            self.updateHumanState()

    def prepareRideHB(self, beastKey, showEffect = True, enhLv = 0, dyeList = []):
        """if self.rideID == beastKey and self.rideModel and not self.rideModel.inWorld: #\xd7\xca\xd4\xb4\xd2\xd1\xbe\xad\xd7\xbc\xb1\xb8\xba\xc3\xc1\xcb\xa3\xac
        self.rideAttached.zaijuMode = attachedModel.ZAIJU_ATTACH
        self._rideModelFinish( self.rideID, showEffect, self.rideModel)
        return"""
        self.rideAttached.equipItem(beastKey, showEffect, enhLv, dyeList)

    def leaveRideHB(self, oldBianshen = None):
        gamelog.debug('zfride:leaveRideHB ', self.state)
        self.rideAttached.cancelTask()
        if self.state in (STATE_HORSE,
         STATE_REPLACE,
         STATE_ATTACH,
         STATE_BEAST):
            self.getDownHorse(oldBianshen)
        else:
            self.updateHumanState()
        self.loadHairNode(self.attachHairNode)
        self.entity.fashion.setIdleType(gametypes.IDLE_TYPE_NORMAL)

    def _rideModelFinish(self, rideID, showEffect, model):
        entity = self.entity
        if not entity or not entity.inWorld:
            return
        if entity.bianshen[0] == gametypes.BIANSHEN_HUMAN:
            self.state = STATE_HUMAN
            self.rideModel = None
            model = None
            self.rideID = 0
            return
        gamelog.debug('zfride:_rideModelFinish ', self.entity, self.bodyModel, rideID, model)
        if getattr(entity, 'IsAvatar', False) and BigWorld.player().isInBfDota():
            if len(entity.dotaLogList) < 10:
                entity.dotaLogList.append(('_rideModelFinish', entity.id, entity.firstFetchFinished))
        if self.state in (STATE_HORSE, STATE_BEAST):
            if self.rideID == rideID and self.rideModel == model:
                return
            if self.rideModel and self.rideID:
                try:
                    self.rideModel.setHP('HP_ride', None)
                except:
                    pass

                if self.rideModel in self.entity.allModels:
                    self.entity.allModels.remove(self.rideModel)
        self.rideModel = model
        self.rideID = rideID
        self.handleHorseFadeTint(entity, self.rideID, True)
        if entity.firstFetchFinished:
            self.rideOnHorse(showEffect)
        data = ZJD.data.get(rideID, {})
        actionIds = data.get('onAction', ())
        if entity.inFlyTypeFlyRide():
            self.rideAttached.refreshEffectInAir()
        self.rideAttached.refreshFlyRideMatrials()
        if hasattr(self.rideAttached, 'refreshAttachEffs'):
            self.rideAttached.refreshAttachEffs()
        if actionIds:
            if entity == BigWorld.player():
                entity.ap.stopMove()
            callback = entity.updateActionKeyState if entity == BigWorld.player() else None
            entity.fashion.playAction(actionIds, action.ZAIJU_ON_ACTION, callback)
        self.handleRideTogether(entity)
        self.setHorseFootTwistSpeed()
        if hasattr(entity, 'inCarrousel') and entity.inCarrousel():
            self.enterCarrousel()
        if hasattr(entity, 'inRoundTable') and entity.inRoundTable():
            self.enterRoundTable()
        if hasattr(entity, 'carrier') and entity.carrier.isRunningState():
            if entity.carrier.has_key(entity.id):
                self.enterCarrier()
        if hasattr(entity, 'attachSkillData') and entity.attachSkillData[0]:
            self.enterAttachSkill(entity.id, entity.attachSkillData[0])
        if hasattr(entity, 'inInteractiveObject') and entity.inInteractiveObject():
            self.enterInteractiveObject()
        if hasattr(entity, 'refreshEquipEnhanceEffects'):
            entity.refreshEquipEnhanceEffects()
        if entity.inFly:
            self.refreshWingFlyState()
        if entity.fashion:
            entity.fashion.autoSetStateCaps()
        p = BigWorld.player()
        if p.id == entity.id and p.isInBfDota():
            p.circleEffect.addSkillRangeCircleModel()
        if self.socialActionModel.state == weaponModel.ATTACHED:
            self.socialActionModel.detach()
        enableNewSchoolSummon = gameglobal.rds.configData.get('enableNewSchoolSummon', False)
        if enableNewSchoolSummon:
            entity.enterAvatarFollowModel()
        if p.id == entity.id:
            gameglobal.rds.cam.reset()

    def _refreshZaijuModel(self, zaijuData):
        if not self.rideAttached or not zaijuData:
            return
        self._refreshZaijuModelMaterial(zaijuData)

    def _refreshZaijuModelMaterial(self, zaijuData):
        materialsName = clientcom.getMatrialsName(self.entity, zaijuData)
        if not materialsName:
            materialsName = 'Default'
        if not self.rideModel:
            return
        tintalt.ta_set_static([self.rideModel], materialsName)

    def getTintDataInfo(self, tintData):
        if not tintData:
            return (None, None, None)
        tintFx = tintData[0]
        tintName, tintPrio, tint = skillDataInfo.getTintDataInfo(self.entity, tintFx)
        return (tintName, tintPrio, tint)

    def handleHorseFadeTint(self, entity, rideID, onHorse):
        if self.rideFadeInOutCB:
            BigWorld.cancelCallback(self.rideFadeInOutCB)
            self.rideFadeInOutCB = None
        fadeTintData = SCD.data.get('fadeTintData', {}).get(rideID, None)
        if fadeTintData:
            tintName, tintPrio, tint = self.getTintDataInfo(fadeTintData)
            self.rideModel.bkgLoadTint = False
            if tintName:
                fadeTime = SCD.data.get('horseFadeTime', 1)
                tintalt.ta_add([self.rideModel], tintName, [tint, BigWorld.shaderTime()], fadeTime, None, False, False, self.entity, self.entity, tintType=tintalt.AVATARTINT)

    def horseFadeToReal(self, fadeTime):
        if not self.rideModel:
            return
        model = self.rideModel
        if not hasattr(model, 'fadeShader') or not model.fadeShader:
            fadeShader = BigWorld.BlendFashion()
            model.fadeShader = fadeShader
        model.fadeShader.current(0)
        model.fadeShader.changeTime(fadeTime)
        model.fadeShader.dest(255)

    def horseRealToFade(self, fadeTime):
        if not self.rideModel:
            return
        model = self.rideModel
        if not hasattr(model, 'fadeShader') or not model.fadeShader:
            fadeShader = BigWorld.BlendFashion()
            model.fadeShader = fadeShader
        model.fadeShader.current(255)
        model.fadeShader.changeTime(fadeTime)
        model.fadeShader.dest(0)

    def clearHorseFadeShader(self):
        if not self.rideModel:
            return
        model = self.rideModel
        if hasattr(model, 'fadeShader') and model.fadeShader:
            model.fadeShader.current(128)
            model.fadeShader.changeTime(0.1)
            model.fadeShader.dest(255)

    def clearHorseFade(self):
        if self.rideFadeTintName:
            tintalt.ta_del([self.rideModel], self.rideFadeTintName, isTaAddCall=True, tintType=tintalt.AVATARTINT)
            self.clearHorseFadeShader()
            self.rideFadeTintName = None

    def handleRideTogether(self, entity):
        if hasattr(entity, 'isRidingTogether') and entity.isRidingTogether():
            if entity.tride.isMajor(entity.id):
                for mid, idx in entity.tride.iteritems():
                    self.hangViceOnMain(entity.id, mid, idx)

            else:
                header = entity.tride.header
                idx = entity.tride.get(entity.id, 0)
                if idx:
                    self.hangViceOnMain(header, entity.id, idx)

    def setHorseFootTwistSpeed(self):
        entity = self.entity
        if entity.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            footTwistSpeed = FDD.data.get(entity.fashion.modelID, {}).get('footTwistSpeed', 0)
            if footTwistSpeed:
                horseFootTwistSpeed = FDD.data.get(entity.fashion.modelID, {}).get('footTwistSpeed', 9)
                if entity.inFly:
                    horseFootTwistSpeed = FDD.data.get(entity.fashion.modelID, {}).get('flyFootTwistSpeed', 9)
                self.setModelFootTwistSpeed(entity.model, horseFootTwistSpeed)

    def rideOnHorse(self, showEffect = True):
        if not self.bodyModel or not self.rideModel:
            if getattr(self.entity, 'IsAvatar', False) and BigWorld.player().isInBfDota():
                if len(self.entity.dotaLogList) < 10:
                    self.entity.dotaLogList.append('rideOnHorse failed')
            gamelog.debug('rideOnHorse failed ', self.bodyModel, self.rideModel)
            self.entity.refreshStateEffect()
            return
        self.realRideOnHorse(self.bodyModel, showEffect)
        if self.entity == BigWorld.player():
            gameglobal.rds.ui.actionbar.setFirstRideShine()

    def releaseHorseAttachedEffect(self):
        for ef in self.horseAttachedEffect:
            if ef:
                ef.stop()

        self.horseAttachedEffect = []

    def addHorseAttachedEffect(self):
        entity = self.entity
        self.releaseHorseAttachedEffect()
        for m in getattr(self.rideAttached, 'models', []):
            try:
                if len(m) > 3 and m[3]:
                    for ef in m[3]:
                        ef = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getBasicEffectLv(),
                         entity.getBasicEffectPriority(),
                         m[0],
                         ef,
                         sfx.EFFECT_LIMIT_MISC,
                         -1,
                         0,
                         True))
                        if ef:
                            self.horseAttachedEffect.extend(ef)

            except:
                gamelog.error('error attach equip model failed!!!!!!!!!!!!!!!!!')

    def playMountAction(self, entity, showEffect, localBodyModel, upRideAction):
        if showEffect:
            mountAction = entity.fashion.getEnterHorseMountAction()
            if self.rideAttached.zaijuAction == attachedModel.ZAIJU_ATTACH_ACTION:
                if entity == BigWorld.player():
                    BigWorld.callback(0.05, Functor(self._playUpRideAction, upRideAction, mountAction))
                else:
                    entity.fashion.playActionSequence(self.bodyModel, [upRideAction], None)
                    entity.fashion.playActionSequence(entity.model, [mountAction], None)
            elif entity == BigWorld.player():
                localBodyModel.visible = True
            self.rideAttached.refreshMountEffect(True)

    def realRideOnHorse(self, localBodyModel, showEffect = True):
        entity = self.entity
        upRideAction = entity.fashion.getEnterHorseAction()
        data = getEntityZaijuDataWithCustom(self.entity, self.rideID)
        actionIds = data.get('onAction', ())
        upRideAction = actionIds[0] if actionIds else upRideAction
        if self.rideAttached.zaijuMode in (attachedModel.ZAIJU_ATTACH, attachedModel.ZAIJU_REPLACE):
            if self.rideModel and self.rideModel.attached:
                if entity and entity.inWorld:
                    try:
                        entity.delModel(self.rideModel)
                    except:
                        pass

        entity.fashion.setupModel(self.rideModel, False)
        addDotaLog = getattr(self.entity, 'IsAvatar', False) and BigWorld.player().isInBfDota()
        entity.refreshOpacityState()
        if addDotaLog:
            if len(entity.dotaLogList) < 10:
                entity.dotaLogList.append(('after', entity.model.visible, entity.getOpacityValue()))
        if self.rideAttached.zaijuMode == attachedModel.ZAIJU_ATTACH:
            if self.rideAttached.isRealHorse:
                self.state = STATE_HORSE
            else:
                self.state = STATE_BEAST
            try:
                if entity == BigWorld.player():
                    self.rideModel.visible = True
                    localBodyModel.visible = not showEffect
                hideMajorRide = ED.data.get(self.rideID, {}).get('hideMajorRide', 0)
                if not hideMajorRide:
                    self.rideModel.setHP('HP_ride', localBodyModel)
                riderScale = ED.data.get(self.rideID, {}).get('riderScale', None)
                if entity.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
                    riderScale = ZJD.data.get(entity.bianshen[1], {}).get('riderScale', None)
                if riderScale:
                    rScale = riderScale / self.rideAttached.scale
                    self.rideModel.node('HP_ride').scale(rScale, rScale, rScale)
                if self.rideAttached.faceIdleAction:
                    action = self.rideModel.action(self.rideAttached.faceIdleAction)
                    action.enableAlpha(True)
                    action()
                    self.faceIdleAction = self.rideAttached.faceIdleAction
            except Exception as e:
                gamelog.debug('m.l@realRideOnHorse error', e.message)

        elif self.rideAttached.zaijuMode == attachedModel.ZAIJU_REPLACE:
            self.state = STATE_REPLACE
        self.rideModel.scale = (self.rideAttached.scale, self.rideAttached.scale, self.rideAttached.scale)
        entity.zaijuScale = self.rideAttached.scale
        entity.am.matchScale = entity.getMatchScale(self.rideAttached.scale)
        entity.resetAmActionSpeed()
        if entity._isInBianyao():
            effects = SCD.data.get('bianYaoEff')
            if effects:
                for effect in effects:
                    sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
                     entity.getEquipEffectPriority(),
                     entity.model,
                     effect,
                     sfx.EFFECT_LIMIT,
                     gameglobal.EFFECT_LAST_TIME))

        keepEffect = data.get('effect', ())
        for ef in keepEffect:
            fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getBasicEffectLv(),
             entity.getBasicEffectPriority(),
             self.rideModel,
             ef,
             sfx.EFFECT_LIMIT_MISC,
             -1,
             0,
             True))
            if fxs:
                self.keepEffect.extend(fxs)

        self.addHorseAttachedEffect()
        self.playMountAction(entity, showEffect, localBodyModel, upRideAction)
        entity.fashion.setStateCaps([keys.CAPS_RIDE])
        if self.state == STATE_HORSE:
            try:
                am = localBodyModel.motors[0]
                gamelog.debug('zfride:set transparence.........', am)
            except:
                am = BigWorld.ActionMatcher(entity)
                am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_GROUND]
                localBodyModel.motors = (am,)

            am.matcherCoupled = False
            self.oldFootTwistSpeed = am.footTwistSpeed
            am.footTwistSpeed = 0.0
            utils.addMotorsChild(self.rideModel.motors, am)
        if not entity.topLogo:
            entity.enterTopLogoRange()
        else:
            BigWorld.callback(0.1, entity.resetTopLogo)
        if entity == BigWorld.player():
            if entity.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
                entity.oldCurrentScrollNum = gameglobal.rds.cam.currentScrollNum
            entity.resetCamera()
        if hasattr(entity, 'ap'):
            entity.ap.recalcSpeed()
            if entity.isDashing:
                qingGong.switchToDash(entity, shieldPathFinding=True)
        entity.forceUpdateEffect()
        if self.state in (STATE_HORSE, STATE_BEAST):
            entity.refreshWeaponVisible()
            self.updateWeaponAction()
            entity.updateBodySlope()
            self.updateModelEffect()
            if hasattr(entity, 'setFaceEmoteId'):
                entity.setFaceEmoteId()
        elif self.state == STATE_REPLACE:
            entity.refreshWeaponVisible()
        self.setFlyRideFloat()
        if entity.fashion.isPlayer:
            self.poseManager.setPoseModel()
        self.setHorseFootTwistSpeed()
        horseEnterHorseAction = entity.fashion.getHorseEnterHorseAction()
        if horseEnterHorseAction:
            if not entity.inMoving():
                self.playHorseAction(horseEnterHorseAction)
        if self.rideAttached.chairIdleAction:
            entity.fashion.playActionSequence(self.bodyModel, [self.rideAttached.chairIdleAction], None)
            BigWorld.callback(0.1, self.resetRiderNormalAction)

    def sitInChair(self, chairModel):
        entity = self.entity
        bodyModel = entity.modelServer.bodyModel
        dummyModel = sfx.getDummyModel(False)
        entity.fashion.setupModel(dummyModel, False)
        seatNode = chairModel.node('HP_chair01')
        if not bodyModel.attached:
            seatNode.attach(bodyModel, 'HP_ride')
        if entity == BigWorld.player():
            gameglobal.rds.cam.cc.set(bodyModel.matrix)
            gameglobal.rds.cam.cc.target = bodyModel.matrix
        entity.refreshWeaponVisible()
        entity.resetTopLogo()
        self.updateModelEffect()
        if entity == BigWorld.player():
            entity.resetCamera()
            BigWorld.simpleShaderDistance(gameglobal.LARGE_SIMPLE_SHADER_DISTANCE)

    def playRiderAction(self, actionId):
        if self.bodyModel:
            entity = self.entity
            entity.fashion.playActionSequence(self.bodyModel, [str(actionId)], self.resetRiderNormalAction)

    def resetRiderNormalAction(self):
        if self.rideAttached and self.rideAttached.chairIdleAction:
            entity = self.entity
            entity.fashion.playActionSequence(self.bodyModel, [self.rideAttached.chairIdleAction], None)
        else:
            entity = self.entity
            if not entity or not entity.inWorld:
                return
            if not entity.tride:
                return
            mainId = entity.tride.header
            main = BigWorld.entity(mainId)
            viceIdx = entity.tride.get(entity.id, 0)
            if not main:
                return
            driveActions = RTD.data.get(main.bianshen[1], {}).get('seatActions', ((11101, 0),))
            driveAction = ('11101', 0)
            try:
                driveAction = driveActions[viceIdx - 1]
            except:
                pass

            self.entity.fashion.playActionSequence(self.bodyModel, [driveAction[0]], None)

    def stopRiderAction(self):
        entity = self.entity
        entity.fashion.stopModelAction(self.bodyModel)
        self.resetRiderNormalAction()

    def playHorseAction(self, action):
        entity = self.entity
        try:
            if self.rideAttached.model:
                entity.fashion.playActionSequence(self.rideAttached.model, [action], None)
        except:
            pass

    def leaveChair(self, chairModel):
        entity = self.entity
        seatNode = chairModel.node('HP_chair01')
        for item in seatNode.attachments:
            seatNode.detach(item)

        bodyModel = entity.modelServer.bodyModel
        if bodyModel and not bodyModel.attached:
            entity.fashion.setupModel(bodyModel, False)
        entity.refreshWeaponVisible()
        self.updateModelEffect()
        entity.resetTopLogo()
        if entity == BigWorld.player():
            gameglobal.rds.cam.cc.set(entity.matrix)
            gameglobal.rds.cam.cc.target = BigWorld.PlayerMatrix()
            BigWorld.simpleShaderDistance(gameglobal.NORMAL_SIMPLE_SHADER_DISTANCE)
            if entity.model.outlineColor:
                outlineHelper.disableOutline(entity.model)

    def setFlyRideFloat(self):
        if not self.entity.isOnFlyRide():
            return
        flyRideFloat = ED.data.get(self.entity.bianshen[1], {}).get('flyRideFloat', 0)
        if flyRideFloat:
            floatage = BigWorld.PyPoseControl()
            self.rideModel.floatage = floatage
            floatage.floatHeight = flyRideFloat
            floatage.popToTerrain = False

    def _playUpRideAction(self, upRideAction, mountAction):
        self.bodyModel.visible = True
        self.entity.fashion.playActionSequence(self.bodyModel, [upRideAction], None)
        self.entity.fashion.playActionSequence(self.entity.model, [mountAction], None)

    def realAttachZaiju(self, zaijuNo, showEffect = True):
        entity = self.entity
        self.rideID = zaijuNo
        self.rideAttached.attach(self.bodyModel)
        self.state = STATE_ATTACH
        entity.refreshWeaponVisible()

    def resetTopLogoWhenDown(self, entity):
        entity.resetTopLogo()
        if entity == BigWorld.player():
            entity.resetCamera()

    def releaseKeepEffect(self):
        if self.keepEffect:
            for fx in self.keepEffect:
                if fx:
                    fx.stop()

        self.keepEffect = []

    def getDownHorse(self, oldBianshen = None):
        gamelog.debug('zf:getDownHorse........', self.entity, self.bodyModel, self.rideModel)
        entity = self.entity
        oldScale = getattr(self.rideModel, 'scale', (1, 1, 1))
        self.releaseKeepEffect()
        if self.state in (STATE_HORSE, STATE_BEAST) and self.rideModel:
            try:
                self.rideModel.setHP('HP_ride', None)
            except:
                pass

        self.state = STATE_HUMAN
        entity.zaijuScale = 1
        attachedMode = self.rideAttached.zaijuMode
        self.rideAttached.detach()
        if attachedMode == attachedModel.ZAIJU_ATTACH:
            if self.bodyModel and not self.bodyModel.attached:
                entity.fashion.setupModel(self.bodyModel, False)
            self.faceIdleAction = None
        elif attachedMode != attachedModel.ZAIJU_BEATTACHED:
            if self.bodyModel and not self.bodyModel.attached:
                entity.fashion.setupModel(self.bodyModel, False)
        entity.refreshOpacityState()
        self.rideAttached.refreshMountEffect(False)
        self.releaseHorseAttachedEffect()
        self.handleHorseFadeTint(self.entity, self.rideID, False)
        dieAction = None
        if oldBianshen:
            dieAction = ZJD.data.get(oldBianshen[1], {}).get('dieAction', None)
        if attachedMode == attachedModel.ZAIJU_ATTACH and not dieAction:
            if self.rideAttached.zaijuAction == attachedModel.ZAIJU_ATTACH_ACTION:
                downRideAction = entity.fashion.getLeaveHorseAction()
                downRideEndAction = entity.fashion.action.getLeaveHorseEndAction(entity.fashion)
                offAction = ZJD.data.get(self.rideID, {}).get('offAction', ())
                duration = 0
                if offAction:
                    actions = []
                    for act in offAction:
                        actions.append((act,
                         None,
                         0,
                         action.LEAVE_HORSE_ACTION))

                    entity.fashion.playActionSequence2(self.bodyModel, actions, action.LEAVE_HORSE_ACTION)
                else:
                    try:
                        duration = entity.model.action(downRideAction).duration + entity.model.action(downRideEndAction).duration
                    except:
                        pass

                    entity.fashion.playActionSequence2(self.bodyModel, [(downRideAction,
                      None,
                      0,
                      action.LEAVE_HORSE_ACTION), (downRideEndAction,
                      None,
                      0,
                      action.LEAVE_HORSE_END_ACTION)], action.LEAVE_HORSE_ACTION)
                    if entity.fashion.opacity:
                        self.horseRush(self.rideModel)
                BigWorld.callback(duration + 0.1, Functor(self.resetTopLogoWhenDown, entity))
        if oldBianshen and entity.fashion.opacity:
            createZaiju = BigWorld.player().createUsedZaijuData.get(entity.id)
            if createZaiju:
                disMountAction = ZJD.data.get(oldBianshen[1], {}).get('disMountAction', None)
                if False and disMountAction:
                    self.playDisMountAction(self.rideModel, disMountAction)
                else:
                    BigWorld.player().createUsedZaijuData[entity.id] = None
            else:
                dieAction = ZJD.data.get(oldBianshen[1], {}).get('dieAction', None)
                dieEff = ZJD.data.get(oldBianshen[1], {}).get('dieEff', None)
                if dieAction:
                    self.playZaiJuDieAction(self.rideModel, dieAction, oldScale)
                    avatarDismountAction = ZJD.data.get(oldBianshen[1], {}).get('avatarDismountAction', None)
                    if avatarDismountAction:
                        downRideAction = entity.fashion.action.getLeaveHorseAction(entity.fashion)
                        downRideEndAction = entity.fashion.action.getLeaveHorseEndAction(entity.fashion)
                        entity.fashion.playActionSequence2(self.bodyModel, [(downRideAction,
                          None,
                          0,
                          action.LEAVE_HORSE_ACTION), (downRideEndAction,
                          None,
                          0,
                          action.LEAVE_HORSE_END_ACTION)], action.LEAVE_HORSE_ACTION)
                if dieEff:
                    sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
                     entity.getEquipEffectPriority(),
                     self.rideModel,
                     dieEff,
                     sfx.EFFECT_LIMIT,
                     gameglobal.EFFECT_LAST_TIME))
        entity.afterModelFinish()
        if entity == BigWorld.player() and entity.oldCurrentScrollNum:
            gameglobal.rds.cam.currentScrollNum = entity.oldCurrentScrollNum
            entity.oldCurrentScrollNum = 0
        self.updateHumanState()
        self.setModelFootTwistSpeed(self.bodyModel, self.oldFootTwistSpeed)
        if hasattr(entity, 'ap'):
            entity.ap.recalcSpeed()
            if entity.isDashing:
                qingGong.switchToDash(entity, shieldPathFinding=True)
        entity.resetTopLogo()
        entity.refreshWeaponVisible()
        self.updateWeaponAction()
        self.updateModelEffect()
        entity.updateBodySlope()
        entity.qinggongMgr.setState(qingGong.STATE_IDLE)
        if hasattr(self.rideModel, 'floatage'):
            self.rideModel.floatage = None
        if hasattr(self.entity.model, 'floatage'):
            self.entity.model.floatage = None
        if entity.fashion.isPlayer:
            self.poseManager.setPoseModel()

    def setModelFootTwistSpeed(self, model, footTwistSpeed):
        if not model:
            return
        if not model.motors:
            return
        for motor in model.motors:
            if motor.__class__.__name__ == 'ActionMatcher':
                motor.footTwistSpeed = footTwistSpeed
                return

    def playZaiJuDieAction(self, model, dieAction, oldScale):
        if model and not model.inWorld:
            entity = self.entity
            model.motors = []
            entity.addModel(model)
            if dieAction in model.actionNameList():
                model.scale = oldScale
                model.yaw = entity.yaw
                model.position = entity.position
                entity.fashion.playActionSequence(model, [dieAction, dieAction], None)
                duration = model.action(dieAction).duration
                BigWorld.callback(duration, Functor(self.stopZaiJuDieAction, model))

    def stopZaiJuDieAction(self, model):
        entity = self.entity
        if entity and entity.inWorld:
            if model and model.inWorld:
                try:
                    entity.delModel(model)
                except:
                    pass

    def playDisMountAction(self, model, disMountAction):
        if model and not model.inWorld:
            self.rideModel = None
            self.rideAttached.resetAttachModel()
            entity = self.entity
            if model in entity.allModels:
                entity.allModels.remove(model)
            model.motors = []
            BigWorld.player().addModel(model)
            BigWorld.player().holdZaijuModel[entity.id] = entity.id
            if disMountAction in model.actionNameList():
                model.yaw = entity.yaw
                model.position = entity.position
                BigWorld.player().fashion.playActionSequence(model, [disMountAction, disMountAction], None)
                duration = model.action(disMountAction).duration
                BigWorld.callback(duration + 1, Functor(self.stopDisMountAction, model))

    def stopDisMountAction(self, model):
        entity = self.entity
        if entity and entity.inWorld:
            if model and model.inWorld:
                BigWorld.player().delModel(model)
                if entity.id in BigWorld.player().leavedZaiju:
                    ezjId = BigWorld.player().leavedZaiju.pop(entity.id, None)
                    emptyZaiju = BigWorld.entities.get(ezjId, None)
                    if emptyZaiju:
                        emptyZaiju.fashion.setupModel(model)
                        emptyZaiju.holdModelByPlayer = False
                        emptyZaiju.refreshOpacityState()
                        del BigWorld.player().holdZaijuModel[entity.id]
                        BigWorld.player().createUsedZaijuData[entity.id] = None

    def horseRush(self, model):
        if model and not model.inWorld:
            entity = self.entity
            dist = 20
            src = entity.position
            yaw = entity.yaw
            des = src + Math.Vector3(math.sin(yaw) * dist, 0, math.cos(yaw) * dist)
            flyer = sfx.SimpleFlyer()
            model.motors = []
            if model and not model.inWorld:
                entity.addModel(model)
                if hasattr(self.entity.model, 'floatage'):
                    src = (src[0], src[1] + self.entity.model.floatage.floatHeight, src[2])
                for act in gameglobal.BEAST_RUSH_ACTIONS:
                    if act in model.actionNameList():
                        entity.fashion.playActionSequence(model, [act, act], None)
                        break

                model.yaw = yaw
                model.position = src
                flyer.start(model, src, des, 18, Functor(self.stopHorseRush, model))

    def stopHorseRush(self, model):
        entity = self.entity
        if entity and entity.inWorld:
            if model and model.inWorld:
                entity.delModel(model)

    def horseUpdate(self):
        if not self.entity.isRealModel:
            return
        if self.entity.bianshen and self.entity.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            beastKey = self.entity.bianshen[1]
            enhLv = self.entity.realAspect.rideEnhLv()
            dyeList = self.entity.realAspect.rideDyeList()
            flyRide = ED.data.get(self.entity.bianshen[1], {}).get('flyRide', False)
            canRideTogether = RTD.data.get(self.entity.bianshen[1], {}).get('canRideTogether', False)
            if self.entity.isShowClanWar() and not flyRide and not canRideTogether:
                beastKey = SCD.data.get('armorHorseId', gameglobal.ARMOR_HORSE_ID)
            self.enterRideHB(beastKey, False, enhLv, dyeList)
        elif self.entity.bianshen and self.entity._isOnZaijuOrBianyao():
            beastKey = self.entity._getZaijuOrBianyaoNo()
            enhLv = self.entity.realAspect.rideEnhLv()
            dyeList = self.entity.realAspect.rideDyeList()
            self.enterZaiju(beastKey, False, enhLv, dyeList)

    def enterBooth(self):
        if self.entity.inBoothing():
            skinData = BSD.data.get(self.entity.curBoothModelId, {})
            modelId = SCD.data.get('boothModel', gameglobal.BOOTH_MODEL)
            self.boothModelScale = skinData.get('modelScale', 1.0)
            needModelId = skinData.get('ModeId', modelId)
            if self.boothModelId:
                if self.boothModelId != needModelId:
                    self.boothModel = None
            self.boothModelId = needModelId
            if not self.boothModel:
                modelPath = 'char/%d/%d.model' % (needModelId, needModelId)
                clientUtils.fetchModel(gameglobal.DEFAULT_THREAD, self._afterBoothModelFinished, modelPath)
            else:
                self._afterBoothModelFinished(self.boothModel)

    def _afterBoothModelFinished(self, model):
        if self.entity and self.entity.inWorld:
            self.boothModel = model
            if self.entity.firstFetchFinished:
                self.entity.fashion.setupModel(model)
                self.entity.refreshOpacityState()
            if self.boothModel:
                self.boothModel.scale = (self.boothModelScale, self.boothModelScale, self.boothModelScale)

    def leaveBooth(self):
        self.bodyUpdate()
        self.weaponUpdate()
        self.horseUpdate()
        self.wingFlyModelUpdate()
        self.boothModelScale = 1.0

    def bodyUpdateOffLine(self, res):
        self.bodyModelLoader.modelOkCallback = self._bodyModelFinish
        self.bodyModelLoader.beginLoad(res, self.urgent)

    def bodyUpdateFromData(self, itemData):
        mpr = charRes.convertToMultiPartRes(itemData)
        mpr.isAvatar = True
        res = mpr.getPrerequisites()
        self.bodyModelLoader.modelOkCallback = self._bodyModelFinish
        self.bodyModelLoader.beginLoad(res, self.urgent)

    def enterGmFollow(self):
        if not getattr(self.entity, 'gmFollow', None):
            return
        follow = BigWorld.entities.get(self.entity.gmFollow)
        if not follow:
            p = BigWorld.player()
            if p.isInBfDota():
                BigWorld.callback(0.2, self.enterGmFollow)
            return
        if self.entity == BigWorld.player():
            self.entity.physics.followTarget = follow.matrix
        self.updateFollowStyle()
        self.entity.refreshOpacityState()

    def leaveGmFollow(self):
        self.entity.physics.followTarget = None
        self.updateFollowStyle()
        self.entity.refreshOpacityState()

    def enterCoupleEmote(self):
        if self.entity.coupleEmote[2] == self.entity.id:
            self.enterCoupleEmoteAsRider()
        else:
            self.enterCoupleEmoteAsHorse()
        self.showCoupleEmoteEffect()

    def releaseCoupleEmoteEffects(self):
        if self.coupleEmoteEffects:
            try:
                for fx in self.coupleEmoteEffects:
                    if fx:
                        fx.stop()

            except:
                pass

            self.coupleEmoteEffects = []

    def showCoupleEmoteEffect(self):
        if not gameglobal.rds.configData.get('enableIntimacy', False):
            return
        self.releaseCoupleEmoteEffects()
        other = BigWorld.entity(self.entity.getOtherIDInCoupleEmote())
        entity = self.entity
        if getattr(entity, 'bindCoupleEffecct', 0) or getattr(other, 'bindCoupleEffecct', 0):
            lv = getattr(entity, 'bindCoupleEffecct', 0) if getattr(entity, 'bindCoupleEffecct', 0) else getattr(other, 'bindCoupleEffecct', 0)
            coupleEmoteEffects = SCD.data.get('coupleEmoteLvEffects', {}).get(lv, [])
            for effId in coupleEmoteEffects:
                bodyModel = entity.modelServer.bodyModel
                fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getSkillEffectLv(),
                 entity.getSkillEffectPriority(),
                 bodyModel,
                 effId,
                 sfx.EFFECT_UNLIMIT,
                 -1))
                if fxs:
                    self.coupleEmoteEffects.extend(fxs)

    def enterCoupleEmoteAsHorse(self):
        self.entity.fashion.autoSetStateCaps()
        self.hangWomanOnMan()
        actionId = self.getCoupleEmoteAction(True)
        BigWorld.callback(0, Functor(self.playCoupleEmoteAction, actionId))
        eff = self.getCoupleEmoteStartEff()
        self.playCoupleEmoteEff(eff)
        effs = self.getCoupleEmoteKeepEffs()
        self.playCoupleEmoteKeepEffs(effs)

    def leaveCoupleEmoteAsHorse(self, oldCoupleEmote):
        self.hangWomanOffMan(oldCoupleEmote)
        self.entity.fashion.autoSetStateCaps()
        self.entity.fashion.stopAllActions()
        self.releaseCoupleEmoteKeepEffs()

    def leaveCoupleEmote(self, oldCoupleEmote):
        if oldCoupleEmote[2] == self.entity.id:
            if self.entity == BigWorld.player():
                BigWorld.player().ap.ccamera.target = BigWorld.player().matrix
            self.leaveCoupleEmoteAsRider(oldCoupleEmote)
        else:
            self.leaveCoupleEmoteAsHorse(oldCoupleEmote)

    def leaveCoupleEmoteAsRider(self, oldCoupleEmote):
        self.hangWomanOffMan(oldCoupleEmote)
        self.updateFollowStyle()
        self.entity.refreshOpacityState()
        self.entity.fashion.stopAllActions()

    def needFollowStyle(self):
        if self.entity.isInCoupleRideAsRider():
            return True
        if self.entity.isRidingTogetherAsVice():
            return True
        if getattr(self.entity, 'gmFollow', None):
            return True
        if getattr(self.entity, 'attachSkillData', [0, 0])[0]:
            return True
        if self.entity.carrier.isRunningState() and self.entity.carrier.get(self.entity.id):
            return True
        if self.entity.isOnWingWorldCarrier() and self.entity.wingWorldCarrier.get(self.entity.id) != 1:
            return True
        return False

    def updateFollowStyle(self):
        if self.entity.id != BigWorld.player().id:
            return
        if self.needFollowStyle():
            self.entity.physics.style = 4
        else:
            self.entity.physics.style = 0

    def _setCoupleEmoteYaw(self, stamp):
        if self.entity.id == BigWorld.player().id and self.entity.isInCoupleEmote() == 2:
            self.updateFollowStyle()
        if self.coupleEmoteStamp != stamp or not self.entity.isInCoupleEmote():
            return
        if self.entity.id == BigWorld.player().id and self.entity.isInCoupleEmote() == 2:
            other = BigWorld.entity(self.entity.getOtherIDInCoupleEmote())
            if other is not None:
                self.entity.faceToDir(other.yaw, True)
                self.entity.model.yaw = self.entity.yaw
        BigWorld.callback(1.5, Functor(self.entity.set_emote, None))

    def getCoupleEmoteAction(self, passive = False):
        coupleKey = self.entity.getCoupleKey(True)
        if passive:
            return CEGD.data.get(coupleKey, {}).get('initAction', '')
        else:
            return CEGD.data.get(coupleKey, {}).get('passiveAction', '')

    def getCoupleEmoteStartEff(self):
        coupleKey = self.entity.getCoupleKey(True)
        return CEGD.data.get(coupleKey, {}).get('startEff')

    def getCoupleEmoteKeepEffs(self):
        coupleKey = self.entity.getCoupleKey(True)
        return CEGD.data.get(coupleKey, {}).get('keepEffs')

    def playCoupleEmoteAction(self, actionId):
        if not self.entity or not self.entity.inWorld:
            return
        if not self.entity.coupleEmote:
            return
        try:
            self.entity.fashion.playActionSequence2(self.bodyModel, [(actionId,
              None,
              0,
              action.COUPLE_EMOTE_NORMAL_ACTION)], action.COUPLE_EMOTE_NORMAL_ACTION)
        except:
            pass

    def releaseCoupleEmoteKeepEffs(self):
        if self.coupleEmoteKeepEffects:
            for ef in self.coupleEmoteKeepEffects:
                if ef:
                    ef.stop()

            self.coupleEmoteKeepEffects = []

    def playCoupleEmoteKeepEffs(self, effs):
        if not effs:
            return
        if not self.entity or not self.entity.inWorld:
            return
        entity = self.entity
        self.releaseCoupleEmoteKeepEffs()
        for eff in effs:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
             entity.getEquipEffectPriority(),
             self.bodyModel,
             eff,
             sfx.EFFECT_LIMIT_MISC))
            if fx:
                self.coupleEmoteKeepEffects.extend(fx)

    def releaseCoupleEmoteEff(self):
        if self.coupleEmoteStartEffs:
            for ef in self.coupleEmoteStartEffs:
                if ef:
                    ef.stop()

            self.coupleEmoteStartEffs = []

    def playCoupleEmoteEff(self, eff):
        if not eff:
            return
        if not self.entity or not self.entity.inWorld:
            return
        entity = self.entity
        self.releaseCoupleEmoteEff()
        fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
         entity.getEquipEffectPriority(),
         self.bodyModel,
         eff,
         sfx.EFFECT_LIMIT_MISC))
        if fx:
            self.coupleEmoteStartEffs.extend(fx)

    def enterCoupleEmoteAsRider(self):
        self.hangWomanOnMan()
        self.updateFollowStyle()
        if self.entity.id != BigWorld.player().id:
            self.entity.filter.followTarget = None
        self.entity.refreshOpacityState()
        self.updateHumanState()
        actionId = self.getCoupleEmoteAction(False)
        BigWorld.callback(0, Functor(self.playCoupleEmoteAction, actionId))
        if self.entity.coupleEmote[2] == self.entity.id and self.entity == BigWorld.player():
            hug = BigWorld.entities.get(self.entity.coupleEmote[1])
            if hug and hug.inWorld:
                BigWorld.player().ap.ccamera.target = hug.matrix
            if gameglobal.rds.ui.raffle.mediator:
                gameglobal.rds.ui.raffle.hide()

    def getCoupleMatchCaps(self):
        other = BigWorld.entity(self.entity.getOtherIDInCoupleEmote())
        if self.entity.coupleEmote[2] == self.entity.id:
            man = other
            woman = self.entity
        else:
            man = self.entity
            woman = other
        caps_middle = keys.CAPS_COUPLE_EMOTE
        if not man or not man.inWorld or not woman or not woman.inWorld:
            return [keys.CAPS_IDLE0, caps_middle]
        if hasattr(man, 'coupleEmote') and man.coupleEmote and man.coupleEmote[0] not in gametypes.COUPLE_EMOTE_TYPE_SPECIAL:
            return [keys.CAPS_IDLE0, caps_middle]
        caps_middle = keys.CAPS_FLY if man.canFly() else keys.CAPS_COUPLE_EMOTE
        if hasattr(man, 'coupleEmote') and man.coupleEmote and man.coupleEmote[0] == gametypes.COUPLE_EMOTE_TYPE_JUGAOGAO:
            caps_middle = keys.CAPS_COUPLE_EMOTE_JUGAOGAO
        coupleEmoteData = CED.data.get(man.getCoupleKey(), {})
        caps = coupleEmoteData.get('emoteCaps', keys.CAPS_COUPLE_EMOTE)
        return [keys.CAPS_IDLE0, caps_middle, caps]

    def hangWomanOnMan(self, needAction = True):
        other = BigWorld.entity(self.entity.getOtherIDInCoupleEmote())
        if getattr(other, 'modelServer', None) is None or getattr(other, 'model', None) is None:
            return
        if self.entity.coupleEmote[2] == self.entity.id:
            man = other
            woman = self.entity
        else:
            man = self.entity
            woman = other
        if not man or not man.inWorld:
            return
        if not woman or not woman.inWorld:
            return
        man.showLeftWeaponModels(False)
        man.showRightWeaponModels(False)
        woman.showLeftWeaponModels(False)
        woman.showRightWeaponModels(False)
        cloneModel = woman.modelServer.bodyModel
        noAttachModel = CEBD.data.get(self.entity.coupleEmote[0], {}).get('noAttachModel', 0)
        if not noAttachModel:
            dummyModel = sfx.getDummyModel(False)
            woman.coupleLoadDummy = True
            woman.fashion.setupModel(dummyModel, False)
            woman.coupleLoadDummy = False
            self.cloneModel = cloneModel
            if man.model.node(PRINCESS_CONTROL) is None:
                return
            cleanList = []
            for item in man.model.node(PRINCESS_CONTROL).attachments:
                cleanList.append(item)

            for item in cleanList:
                man.model.node(PRINCESS_CONTROL).detach(item)

            try:
                man.model.node(PRINCESS_CONTROL).attach(cloneModel, PRINCESS_PASSIVE_CONTROL)
            except:
                gamelog.error('hangWomanOnMan ', str(man.model.sources), str(cloneModel.sources))

        man.modelServer.coupleModel = cloneModel
        woman.modelServer.updateWearEffect()
        woman.modelServer.updateFashionEffect()
        if self.entity.coupleEmote[0] in gametypes.COUPLE_EMOTE_TYPE_SPECIAL:
            matchCaps = self.getCoupleMatchCaps()
            am = BigWorld.ActionMatcher(self.entity)
            am.matchCaps = matchCaps
            am.matcherCoupled = False
            am.footTwistSpeed = 0
            coupleKey = self.entity.getCoupleKey()
            newCoupleKey = coupleKey + (self.entity.coupleEmote[0],)
            carryActionList = CED.data.get(newCoupleKey, {}).get('landDriveActionMap', ())
            if not carryActionList:
                carryActionList = CED.data.get(coupleKey, {}).get('landDriveActionMap', ())
            driveActionMap = []
            if woman.physique.sex == const.SEX_FEMALE and woman.physique.bodyType == 5 or man.physique.sex == const.SEX_FEMALE and man.physique.bodyType == 5:
                if man.physique.sex == const.SEX_FEMALE and man.physique.bodyType == 5 and woman.physique.sex == const.SEX_FEMALE and woman.physique.bodyType == 5:
                    driveActionMap = [ (i, str(int(i) + 100000)) for i in carryActionList ]
                else:
                    driveActionMap = [ (i, str(int(i) + 10000)) for i in carryActionList ]
            else:
                driveActionMap = [ (i, str(int(i) + 1000)) for i in carryActionList ]
            extendDriveActionMap = CED.data.get(coupleKey, {}).get('extendDriveActionMap', ())
            driveActionMap.extend(extendDriveActionMap)
            am.driveActionMap = driveActionMap
            cloneModel.motors = (am,)
            if not man.model.motors:
                man.model.motors = (BigWorld.ActionMatcher(man),)
            if man.model.motors:
                for motor in man.model.motors:
                    if motor.__class__.__name__ == 'ActionMatcher':
                        motor.addChild(am)
                        motor.matchCaps = matchCaps
                        break

        if woman.id == BigWorld.player().id:
            woman.physics.followTarget = man.matrix
        else:
            woman.filter.followTarget = man.matrix
        if woman is not None:
            woman.refreshOpacityState()
            BigWorld.callback(0.1, Functor(self.afterHangWomanOnMan, woman, cloneModel))
        man.refreshOpacityState()
        self.addUpperIK(man.model, cloneModel)

    def afterHangWomanOnMan(self, woman, cloneModel):
        if woman and woman.inWorld and getattr(woman, 'IsAvatar', False):
            woman.resetTopLogo()
            clientcom.setModelPhysics(cloneModel)

    def addUpperIK(self, hugModel, beHugModel):
        if not gameglobal.ENABLE_UPPER_IK:
            return
        ik = clientcom.getRightUpperIK()
        ik.target = beHugModel.node('biped R Forearm')
        hugModel.ik = ik

    def hangWomanOffMan(self, oldCoupleEmote):
        other = BigWorld.entity(self.entity.getOtherIDInCoupleEmote(oldCoupleEmote))
        if oldCoupleEmote[2] == self.entity.id:
            man = other
            woman = self.entity
        else:
            man = self.entity
            woman = other
        if not man or not man.inWorld:
            return
        manBodyModel = getattr(getattr(man, 'modelServer', None), 'bodyModel', None)
        if manBodyModel is not None and manBodyModel.node(PRINCESS_CONTROL) is not None:
            cleanList = [ item for item in manBodyModel.node(PRINCESS_CONTROL).attachments ]
            for item in cleanList:
                manBodyModel.node(PRINCESS_CONTROL).detach(item)

        if not woman or not woman.inWorld:
            return
        man.model.motors[0].delChild(woman.am)
        woman.fashion.autoSetStateCaps()
        man.modelServer.coupleModel = None
        man.fashion.autoSetStateCaps()
        man.topLogo.updateRoleName(man.topLogo.name)
        man.refreshOpacityState()
        man.resetTopLogo()
        man.refreshWeaponVisible()
        if hasattr(man, 'refreshEquipEnhanceEffects'):
            man.refreshEquipEnhanceEffects()
        if woman is not None:
            woman.refreshOpacityState()
            woman.resetTopLogo()
            woman.refreshWeaponVisible()
        if woman.id == BigWorld.player().id:
            woman.physics.followTarget = None
        else:
            woman.filter.followTarget = None
        if not woman.modelServer.bodyModel.attached and not woman.bianshen[0]:
            woman.modelServer.bodyModel.motors = ()
            woman.fashion.setupModel(woman.modelServer.bodyModel)
            woman.forceUpdateEffect()
            woman.modelServer.updateModelEffect()
            if woman.modelServer.leftWeaponModel:
                woman.modelServer.leftWeaponModel.updateWeaponAction()
            if hasattr(woman, 'refreshEquipEnhanceEffects'):
                woman.refreshEquipEnhanceEffects()

    def enterAttachSkill(self, srcId, targetId):
        srcEnt = BigWorld.entities.get(srcId, None)
        tgtEnt = BigWorld.entities.get(targetId, None)
        if not srcEnt or not tgtEnt:
            return
        if srcEnt == BigWorld.player():
            srcEnt.physics.followTarget = tgtEnt.matrix
            srcEnt.ap.ccamera.target = tgtEnt.matrix
            srcEnt.physics.fall = False
        else:
            srcEnt.filter.followTarget = tgtEnt.matrix
        self.updateFollowStyle()
        self.addFollowMotor(srcEnt, tgtEnt)
        srcEnt.refreshWeaponVisible()

    def hasFollowMotor(self, ent):
        if not ent:
            return False
        if not ent.model:
            return False
        for motor in ent.model.motors:
            if motor.__class__.__name__ == 'Follow':
                return True

        return False

    def addFollowMotor(self, srcEnt, tgtEnt):
        self.clearFollowMotor(srcEnt)
        follow = BigWorld.Follow()
        follow.target = tgtEnt.matrix
        follow.biasTolerance = SCD.data.get('attachSkillBiasTolerance', 1)
        follow.biasPos = SCD.data.get('attachSkillBias', (-0.5, 1, -0.5))
        follow.clampPos = SCD.data.get('attachSkillClampPos', False)
        follow.speedHalflife = SCD.data.get('attachSkillSpeedHalflife', 1)
        follow.lineAttach = SCD.data.get('attachSkillLineAttach', True)
        follow.fixedSpeed = SCD.data.get('attachSkillFixedSpeed', 2.0)
        bm = srcEnt.model
        if bm:
            bm.addMotor(follow)

    def clearFollowMotor(self, ent):
        if not ent or not ent.inWorld:
            return
        try:
            model = ent.model
            if model and model.motors:
                for motor in list(model.motors):
                    if motor.__class__.__name__ == 'Follow':
                        model.delMotor(motor)

            model = ent.modelServer.bodyModel
            if model and model.motors:
                for motor in list(model.motors):
                    if motor.__class__.__name__ == 'Follow':
                        model.delMotor(motor)

        except:
            pass

    def leaveAttachSkill(self, srcId, targetId):
        srcEnt = BigWorld.entities.get(srcId, None)
        if not srcEnt:
            return
        self.clearFollowMotor(srcEnt)
        if srcEnt == BigWorld.player():
            srcEnt.physics.followTarget = None
            srcEnt.ap.ccamera.target = srcEnt.matrix
            srcEnt.physics.fall = True
            srcEnt.fashion.breakFall()
        else:
            srcEnt.filter.followTarget = None
        self.updateFollowStyle()
        srcEnt.refreshWeaponVisible()

    def refreshRideTogether(self, oldTride):
        onIds = set(self.entity.tride.keys()) - set(oldTride.keys())
        offIds = set(oldTride.keys()) - set(self.entity.tride.keys())
        for onId in onIds:
            header = self.entity.tride.header
            idx = self.entity.tride.get(onId, 0)
            if idx:
                self.hangViceOnMain(header, onId, idx)

        if not self.entity.tride.inRide() and oldTride.inRide() and not oldTride.isMajor(self.entity.id):
            idx = oldTride.get(self.entity.id, 0)
            self.takeOffViceFromMain(oldTride.header, self.entity.id, idx)
        else:
            for offId in offIds:
                header = oldTride.header
                idx = oldTride.get(offId, 0)
                if idx:
                    self.takeOffViceFromMain(header, offId, idx)

    def getRideTogetherNodeName(self, idx):
        return 'HP_ride0' + str(idx + 1)

    def getRideTogetherModelByIdx(self, idx):
        nodeName = self.getRideTogetherNodeName(idx)
        if self.rideModel and self.rideModel.node(nodeName):
            if len(self.rideModel.node(nodeName).attachments) != 0:
                return self.rideModel.node(nodeName).attachments[0]

    def resetRideTogetherBodyBias(self, main):
        if not main:
            return
        if not main.modelServer:
            return
        if main.tride:
            optRTHP = ED.data.get(main.modelServer.rideID, {}).get('optRTHP', None)
            try:
                if optRTHP:
                    bodyModel = main.modelServer.bodyModel
                    main.modelServer.rideModel.setHP('HP_ride', None)
                    if bodyModel and not bodyModel.attached:
                        hideMajorRide = ED.data.get(main.modelServer.rideID, {}).get('hideMajorRide', 0)
                        if not hideMajorRide:
                            main.modelServer.rideModel.node(optRTHP).attach(bodyModel, 'HP_ride')
                        riderScale = ED.data.get(main.modelServer.rideID, {}).get('riderScale', None)
                        if riderScale:
                            rScale = riderScale / main.modelServer.rideAttached.scale
                            main.modelServer.rideModel.node(optRTHP).scale(rScale, rScale, rScale)
                        chairIdleAction = getattr(main.modelServer.rideAttached, 'chairIdleAction', None)
                        if chairIdleAction:
                            bodyModel.action(chairIdleAction)()
            except:
                pass

        else:
            optRTHP = ED.data.get(main.modelServer.rideID, {}).get('optRTHP', None)
            try:
                mainBodyModel = getattr(main.modelServer, 'bodyModel', None)
                if optRTHP:
                    if hasattr(main.modelServer, 'rideModel'):
                        rideModel = main.modelServer.rideModel
                        if rideModel and rideModel.node(optRTHP) and mainBodyModel in rideModel.node(optRTHP).attachments:
                            rideModel.node(optRTHP).detach(mainBodyModel)
                if main.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
                    hideMajorRide = ED.data.get(main.modelServer.rideID, {}).get('hideMajorRide', 0)
                    if not hideMajorRide:
                        main.modelServer.rideModel.setHP('HP_ride', mainBodyModel)
            except:
                pass

    def hangViceOnMain(self, mainID, viceID, viceIdx, needFresh = True):
        main = BigWorld.entity(mainID)
        vice = BigWorld.entity(viceID)
        if not main or not vice:
            return
        if not main.inWorld or not vice.inWorld:
            return
        vice.fashion.stopAction()
        main.refreshWeaponVisible()
        nodeName = self.getRideTogetherNodeName(viceIdx)
        self.resetRideTogetherBodyBias(main)
        if getattr(getattr(main, 'modelServer', None), 'rideModel', None) and main.modelServer.rideModel.node(nodeName):
            if len(main.modelServer.rideModel.node(nodeName).attachments) != 0:
                for item in main.modelServer.rideModel.node(nodeName).attachments:
                    main.modelServer.rideModel.node(nodeName).detach(item)

            if vice and vice.modelServer:
                vice.refreshWeaponVisible()
                cloneModel = vice.modelServer.bodyModel
                dummyModel = sfx.getDummyModel(False)
                vice.fashion.setupModel(dummyModel, False)
                if not cloneModel.attached:
                    main.modelServer.rideModel.node(nodeName).attach(cloneModel, 'HP_ride')
                    riderScale = ED.data.get(main.modelServer.rideID, {}).get('riderScale', None)
                    if riderScale:
                        rScale = riderScale / main.modelServer.rideAttached.scale
                        main.modelServer.rideModel.node(nodeName).scale(rScale, rScale, rScale)
                    vice.modelServer.rideTogetherModel = cloneModel
                if len(main.modelServer.rideModel.motors) > 0:
                    try:
                        am = vice.motors[0]
                    except:
                        am = BigWorld.ActionMatcher(vice)
                        am.matchCaps = [keys.CAPS_IDLE0, keys.CAPS_HAND_FREE, keys.CAPS_GROUND]
                        vice.motors = (am,)

                    am.matcherCoupled = False
                    am.footTwistSpeed = 0
                    if am.owner:
                        am.owner.delMotor(am)
                    cloneModel.motors = (am,)
                    driveActions = RTD.data.get(main.bianshen[1], {}).get('seatActions', ((11101, 0),))
                    driveAction = ('11101', 0)
                    try:
                        driveAction = driveActions[viceIdx - 1]
                    except:
                        pass

                    if driveAction[1]:
                        am.driveActionMap = [ (i, i + '_' + str(viceIdx + 1)) for i in main.modelServer.rideModel.actionNameList() ]
                    else:
                        self.entity.fashion.playActionSequence(cloneModel, [driveAction[0]], None)
                    try:
                        mainSeatActionDiff = RTD.data.get(main.bianshen[1], {}).get('mainSeatActionDiff', 0)
                        if mainSeatActionDiff:
                            mainDriveActionMap = [ (i, i + '_1') for i in main.modelServer.rideModel.actionNameList() ]
                            mainAm = main.modelServer.bodyModel.motors[0]
                            mainAm.driveActionMap = mainDriveActionMap
                    except:
                        pass

                    if main.modelServer.rideModel.motors:
                        for motor in main.modelServer.rideModel.motors:
                            if motor.__class__.__name__ == 'ActionMatcher':
                                motor.addChild(am)
                                break

        if vice.id != BigWorld.player().id:
            vice.filter.followTarget = main.matrix
        else:
            vice.physics.followTarget = main.matrix
            gameglobal.rds.cam.cc.set(main.matrix)
            gameglobal.rds.cam.cc.target = main.matrix
            BigWorld.player().resetCamera()
        self.updateFollowStyle()
        main.resetTopLogo()
        BigWorld.callback(0.1, vice.resetTopLogo)
        vice.refreshOpacityState()

    def takeOffViceFromMain(self, mainID, viceID, idx):
        main = BigWorld.entity(mainID)
        self.resetRideTogetherBodyBias(main)
        if main and main.inWorld:
            main.refreshWeaponVisible()
            nodeName = self.getRideTogetherNodeName(idx)
            if main.modelServer.rideModel and main.modelServer.rideModel.node(nodeName):
                for model in main.modelServer.rideModel.node(nodeName).attachments:
                    main.modelServer.rideModel.node(nodeName).detach(model)

            try:
                mainSeatActionDiff = RTD.data.get(main.bianshen[1], {}).get('mainSeatActionDiff', 0)
                if mainSeatActionDiff:
                    mainAm = main.modelServer.bodyModel.motors[0]
                    mainAm.driveActionMap = []
            except:
                pass

        vice = BigWorld.entity(viceID)
        if vice is None:
            return
        if not vice.modelServer.bodyModel.attached and not vice.bianshen[0]:
            vice.modelServer.bodyModel.motors = ()
            vice.fashion.setupModel(vice.modelServer.bodyModel)
            vice.forceUpdateEffect()
            vice.modelServer.rideTogetherModel = None
            vice.rideTogetherDownHorse = True
            if hasattr(vice, 'refreshEquipEnhanceEffects'):
                vice.refreshEquipEnhanceEffects()
        else:
            vice.modelServer.bodyUpdate()
        if vice.id == BigWorld.player().id:
            vice.physics.followTarget = None
            gameglobal.rds.cam.cc.set(self.entity.matrix)
            gameglobal.rds.cam.cc.target = BigWorld.PlayerMatrix()
            BigWorld.player().resetCamera()
        else:
            vice.filter.followTarget = None
        self.updateFollowStyle()
        if not self.entity.bianshen[0]:
            self.updateHumanState()
        if main:
            main.resetTopLogo()
        vice.resetTopLogo()
        vice.refreshOpacityState()
        vice.refreshWeaponVisible()

    def enterCarrousel(self):
        entity = self.entity
        if not entity.inCarrousel():
            return
        carrousel = BigWorld.entities.get(entity.carrousel[0])
        if not carrousel:
            return
        bodyModel = entity.modelServer.bodyModel
        dummyModel = sfx.getDummyModel(False)
        entity.fashion.setupModel(dummyModel, False)
        seatNode = getCarrouselSeatNode(carrousel, entity)
        if carrousel.model.node(seatNode) is None:
            return
        cleanList = []
        for item in carrousel.model.node(seatNode).attachments:
            cleanList.append(item)

        for item in cleanList:
            carrousel.model.node(seatNode).detach(item)

        if not bodyModel.attached:
            carrousel.model.node(seatNode).attach(bodyModel, 'HP_ride')
        carrouselAction = CD.data.get(carrousel.carrouselId, {}).get('riderAct', '1101')
        try:
            bodyModel.action(carrouselAction)()
        except:
            pass

        if entity == BigWorld.player():
            gameglobal.rds.cam.cc.set(bodyModel.matrix)
            gameglobal.rds.cam.cc.target = bodyModel.matrix
        entity.refreshWeaponVisible()
        entity.resetTopLogo()
        if entity == BigWorld.player():
            if entity.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
                entity.oldCurrentScrollNum = gameglobal.rds.cam.currentScrollNum
            entity.resetCamera()
            BigWorld.simpleShaderDistance(gameglobal.LARGE_SIMPLE_SHADER_DISTANCE)
            cameraAni = CD.data.get(carrousel.carrouselId, {}).get('cameraAni', [])
            self.playCarrouselAni(cameraAni)
        if hasattr(BigWorld, 'setSmoothCameraAnimation'):
            BigWorld.setCameraAnimModel(carrousel.model)
            BigWorld.setSmoothCameraAnimation(True)

    def playCarrouselAni(self, cameraAni):
        if not cameraAni:
            return
        try:
            if not self.carrouselAniModel:
                self.carrouselAniModel = clientcom.model('item/model/99997/99997.model')
            p = BigWorld.player()
            p.modelServer.bodyModel.node('HP_ride').attach(self.carrouselAniModel, 'Scene Root')
            self.playingCarrouselAni = True
            CC.newFree()
            CC.TC.invViewProvider = self.carrouselAniModel.node('camBone')
            self.carrouselAniModel.action(cameraAni[self.playingCarrouselAniIdx])(0)
        except:
            pass

    def switchCarrouselAni(self):
        entity = self.entity
        cid = entity.carrousel[0]
        carrousel = BigWorld.entities.get(cid)
        if not carrousel:
            return
        cameraAni = CD.data.get(carrousel.carrouselId, {}).get('cameraAni', [])
        if not cameraAni:
            return
        self.playingCarrouselAniIdx = (self.playingCarrouselAniIdx + 1) % len(cameraAni)
        if not self.carrouselAniModel:
            return
        try:
            self.carrouselAniModel.action(cameraAni[self.playingCarrouselAniIdx])(0)
        except:
            pass

    def endCarrouselAni(self):
        if self.playingCarrouselAni:
            CC.endCamera()
            BigWorld.player().modelServer.bodyModel.node('HP_ride').detach(self.carrouselAniModel)
            self.playingCarrouselAni = False

    def leaveCarrousel(self, old):
        entity = self.entity
        carrousel = BigWorld.entities.get(old[0])
        if not carrousel:
            return
        carrouselModel = getattr(carrousel, 'model', None)
        seatNode = getCarrouselSeatNode(carrousel, entity, old[1])
        if carrouselModel is not None and carrouselModel.node(seatNode) is not None:
            cleanList = [ item for item in carrouselModel.node(seatNode).attachments ]
            for item in cleanList:
                carrouselModel.node(seatNode).detach(item)

        bodyModel = entity.modelServer.bodyModel
        if bodyModel and not bodyModel.attached:
            entity.fashion.setupModel(bodyModel, False)
        entity.refreshWeaponVisible()
        entity.resetTopLogo()
        if entity == BigWorld.player():
            gameglobal.rds.cam.cc.set(entity.matrix)
            gameglobal.rds.cam.cc.target = BigWorld.PlayerMatrix()
            if entity.oldCurrentScrollNum:
                gameglobal.rds.cam.currentScrollNum = entity.oldCurrentScrollNum
                entity.oldCurrentScrollNum = 0
            clientcom.resetLimitFps()
            BigWorld.simpleShaderDistance(gameglobal.NORMAL_SIMPLE_SHADER_DISTANCE)
            self.endCarrouselAni()
            if entity.model.outlineColor:
                outlineHelper.disableOutline(entity.model)
        if hasattr(BigWorld, 'setSmoothCameraAnimation'):
            BigWorld.setCameraAnimModel(None)
            BigWorld.setSmoothCameraAnimation(False)

    def getBindNode(self, bindEntity, bindType, bindIdx):
        if bindType == BIND_TYPE_ROUND_TABLE:
            return utils.getRoundTableSeatNodeName(bindIdx)
        if bindType == BIND_TYPE_INTERACTIVE_OBJ:
            return utils.getInteractiveNodeName(bindIdx)
        if bindType == BIND_TYPE_CARRIER:
            return utils.getCarrierNodeName(bindIdx)

    def getBindIdleAction(self, bindType):
        if bindType == BIND_TYPE_ROUND_TABLE:
            return '69002'
        if bindType == BIND_TYPE_INTERACTIVE_OBJ:
            owner = self.entity
            interObj = BigWorld.entities.get(owner.interactiveObjectEntId, None)
            if interObj and interObj.inWorld:
                basicActionExpendId = IAD.data.get(interObj.objectId, {}).get('basicActionExpendId', None)
                interBasicActionId = None
                idleActions = ()
                basicActionIds = IEAD.data.get(basicActionExpendId, {}).get('basicActionIds', None)
                if basicActionIds and self.interactiveObjIdx > -1 and self.interactiveObjIdx < len(basicActionIds):
                    interBasicActionId = basicActionIds[self.interactiveObjIdx]
                else:
                    interBasicActionId = IAD.data.get(interObj.objectId, {}).get('interactiveActionId', None)
                idleActions = IBAD.data.get(interBasicActionId, {}).get('idleActions', ())
                actions = []
                actionProbs = []
                for act in idleActions:
                    if act and act[0]:
                        actions.append(act[0])
                        actionProbs.append(act[1])

                if actions:
                    idx = utils.weighted_choice(actionProbs)
                    return actions[idx]
                else:
                    return '31101'
        if bindType == BIND_TYPE_CARRIER:
            if self.entity.isOnWingWorldCarrier():
                seatIdex = self.entity.wingWorldCarrier.get(self.entity.id)
                idleActions = WWCD.data.get(self.entity.wingWorldCarrier.carrierNo, {}).get('idleActions')
                idleAction = '69002'
                if idleActions:
                    idleAction = idleActions.get(seatIdex, '69002')
            else:
                idleAction = MCAD.data.get(self.entity.carrier.carrierNo, {}).get('idleAction', '69002')
            return idleAction

    def getBindEnterAction(self, bindType):
        if bindType == BIND_TYPE_INTERACTIVE_OBJ:
            owner = self.entity
            interObj = BigWorld.entities.get(owner.interactiveObjectEntId, None)
            if interObj and interObj.inWorld:
                basicActionExpendId = IAD.data.get(interObj.objectId, {}).get('basicActionExpendId', None)
                interBasicActionId = None
                enterAction = ''
                basicActionIds = IEAD.data.get(basicActionExpendId, {}).get('basicActionIds', None)
                if basicActionIds and self.interactiveObjIdx > -1 and self.interactiveObjIdx < len(basicActionIds):
                    interBasicActionId = basicActionIds[self.interactiveObjIdx]
                else:
                    interBasicActionId = IAD.data.get(interObj.objectId, {}).get('interactiveActionId', None)
                enterAction = IBAD.data.get(interBasicActionId, {}).get('enterAction')
                return enterAction

    def getBindLeaveAction(self, bindType):
        if bindType == BIND_TYPE_INTERACTIVE_OBJ:
            interObj = BigWorld.entities.get(self.oldInteractiveObjectEntId, None)
            if interObj and interObj.inWorld:
                basicActionExpendId = IAD.data.get(interObj.objectId, {}).get('basicActionExpendId', None)
                interBasicActionId = None
                leaveAction = ''
                basicActionIds = IEAD.data.get(basicActionExpendId, {}).get('basicActionIds', None)
                if basicActionIds and self.interactiveObjIdx > -1 and self.interactiveObjIdx < len(basicActionIds):
                    interBasicActionId = basicActionIds[self.interactiveObjIdx]
                else:
                    interBasicActionId = IAD.data.get(interObj.objectId, {}).get('interactiveActionId', None)
                leaveAction = IBAD.data.get(interBasicActionId, {}).get('leaveAction')
                return leaveAction

    def playBindEnterAction(self, bindType):
        actions = []
        enterAction = self.getBindEnterAction(bindType)
        if enterAction:
            actions.append((enterAction,
             None,
             0,
             action.INTERACTIVE_ENTER_ACTION))
        idleAction = self.getBindIdleAction(bindType)
        if idleAction:
            actions.append((idleAction,
             None,
             0,
             action.INTERACTIVE_ENTER_ACTION))
        owner = self.entity
        if actions:
            owner.fashion.playActionSequence2(owner.modelServer.bodyModel, actions, action.INTERACTIVE_ENTER_ACTION)
        if bindType == BIND_TYPE_INTERACTIVE_OBJ:
            self.playInteractiveEnterChatEmote()

    def playInteractiveIdleAction(self):
        idleAction = self.getBindIdleAction(BIND_TYPE_INTERACTIVE_OBJ)
        try:
            self.bodyModel.action(idleAction)()
        except:
            pass

    def playInteractiveEnterChatEmote(self):
        owner = self.entity
        interObj = BigWorld.entities.get(self.oldInteractiveObjectEntId, None)
        if interObj and interObj.inWorld:
            interBasicActionId = IAD.data.get(interObj.objectId, {}).get('interactiveActionId', None)
            enterChatId = IBAD.data.get(interBasicActionId, {}).get('enterChatId')
            chatData = IACD.data.get(enterChatId, {})
            msg = chatData.get('details', None)
            duration = chatData.get('duration', 1)
            if msg:
                owner.topLogo.setChatMsg(msg, duration)
            enterEmote = IBAD.data.get(interBasicActionId, {}).get('enterEmote')
            emoteData = IAED.data.get(enterEmote, {})
            res = emoteData.get('res', None)
            if res:
                owner.doEmote(res)

    def playInteractiveLeaveChatEmote(self):
        owner = self.entity
        interObj = BigWorld.entities.get(self.oldInteractiveObjectEntId, None)
        if interObj and interObj.inWorld:
            interBasicActionId = IAD.data.get(interObj.objectId, {}).get('interactiveActionId', None)
            leaveChatId = IBAD.data.get(interBasicActionId, {}).get('leaveChatId')
            chatData = IACD.data.get(leaveChatId, {})
            msg = chatData.get('details', None)
            duration = chatData.get('duration', 1)
            if msg:
                owner.topLogo.setChatMsg(msg, duration)
            leaveEmote = IBAD.data.get(interBasicActionId, {}).get('leaveEmote')
            emoteData = IAED.data.get(leaveEmote, {})
            res = emoteData.get('res', None)
            if res:
                owner.doEmote(res)

    def playBindLeaveAction(self, bindType):
        leaveAction = self.getBindLeaveAction(bindType)
        owner = self.entity
        owner.fashion.playActionSequence(owner.modelServer.bodyModel, [leaveAction], None)
        if bindType == BIND_TYPE_INTERACTIVE_OBJ:
            self.playInteractiveLeaveChatEmote()

    def getAttachScale(self, bindType):
        if bindType == BIND_TYPE_INTERACTIVE_OBJ:
            if self.entity:
                interactiveObj = self.entity.getInteractiveObj()
                if interactiveObj and interactiveObj.inWorld:
                    scale = interactiveObj.getAttachScale()
                    return scale

    def bindOtherEntity(self, bindEntity, bindType, bindIdx, avatarScale = 0.0):
        owner = self.entity
        if owner.fashion.doingActionType() == action.INTERACTIVE_ENTER_ACTION and bindType != BIND_TYPE_CARRIER:
            gamelog.debug('m.l@bindOtherEntity inAction return', owner.fashion.doingActionType())
            return
        bodyModel = owner.modelServer.bodyModel
        dummyModel = sfx.getDummyModel(False)
        owner.fashion.setupModel(dummyModel, False)
        seatNode = self.getBindNode(bindEntity, bindType, bindIdx)
        if bindEntity.model.node(seatNode) is None:
            return
        cleanList = []
        for item in bindEntity.model.node(seatNode).attachments:
            cleanList.append(item)

        for item in cleanList:
            bindEntity.model.node(seatNode).detach(item)

        if not bodyModel.attached:
            attachScale = self.getAttachScale(bindType)
            if attachScale:
                bindEntity.model.node(seatNode).scale(attachScale)
            bindEntity.model.node(seatNode).attach(bodyModel, 'HP_ride')
            if avatarScale:
                bindEntity.model.node(seatNode).scale(avatarScale)
        self.playBindEnterAction(bindType)
        if owner == BigWorld.player() and bodyModel.attached:
            if bindType != BIND_TYPE_CARRIER:
                gameglobal.rds.cam.cc.set(bodyModel.matrix)
                gameglobal.rds.cam.cc.target = bodyModel.matrix
        owner.refreshWeaponVisible()
        owner.resetTopLogo()
        self.updateFashionEffect()
        if owner == BigWorld.player():
            if owner.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
                owner.oldCurrentScrollNum = gameglobal.rds.cam.currentScrollNum
            owner.resetCamera()

    def unBindOtherEntity(self, bindedEntity, bindType, bindIdx):
        owner = self.entity
        bindedEntityModel = getattr(bindedEntity, 'model', None)
        seatNode = self.getBindNode(bindedEntity, bindType, bindIdx)
        if bindedEntityModel is not None and bindedEntityModel.node(seatNode) is not None:
            cleanList = [ item for item in bindedEntityModel.node(seatNode).attachments ]
            for item in cleanList:
                bindedEntityModel.node(seatNode).detach(item)

        bodyModel = owner.modelServer.bodyModel
        if bodyModel and not bodyModel.attached:
            owner.fashion.setupModel(bodyModel, False)
        owner.refreshWeaponVisible()
        BigWorld.callback(0.1, owner.resetTopLogo)
        self.playBindLeaveAction(bindType)
        self.updateFashionEffect()
        if owner == BigWorld.player():
            gameglobal.rds.cam.cc.set(owner.matrix)
            gameglobal.rds.cam.cc.target = BigWorld.PlayerMatrix()
            if owner.oldCurrentScrollNum:
                gameglobal.rds.cam.currentScrollNum = owner.oldCurrentScrollNum
                owner.oldCurrentScrollNum = 0
            if owner.model.outlineColor:
                outlineHelper.disableOutline(owner.model)

    def enterRoundTable(self):
        if not self.entity.inRoundTable():
            return
        roundTable = BigWorld.entities.get(self.entity.belongToRoundTable)
        if not roundTable or not roundTable.inWorld:
            return
        roundTableIdx = roundTable.getRoundTableIdx(self.entity)
        if roundTableIdx < 0:
            return
        self.roundTableIdx = roundTableIdx
        self.bindOtherEntity(roundTable, BIND_TYPE_ROUND_TABLE, self.roundTableIdx)
        self.updateModelEffect()

    def leaveRoundTable(self, old):
        owner = self.entity
        roundTable = BigWorld.entities.get(old)
        if not roundTable:
            bodyModel = owner.modelServer.bodyModel
            if bodyModel and not bodyModel.attached:
                owner.fashion.setupModel(bodyModel, False)
                BigWorld.callback(0.1, owner.resetTopLogo)
            self.roundTableIdx = 0
            return
        self.unBindOtherEntity(roundTable, BIND_TYPE_ROUND_TABLE, self.roundTableIdx)
        self.roundTableIdx = -1

    def detachBodyCarrier(self, carrier):
        if self.entity.oldCarrier:
            try:
                seatIdx = self.entity.oldCarrier.get(self.entity.id, -1)
                if seatIdx == -1:
                    return
                seatNode = self.getBindNode(carrier, BIND_TYPE_CARRIER, seatIdx)
                if carrier.model and carrier.model.node(seatNode):
                    if self.bodyModel in carrier.model.node(seatNode).attachments:
                        carrier.model.node(seatNode).detach(self.bodyModel)
            except Exception as e:
                pass

    def enterCarrier(self):
        if not self.entity.isOnCarrier():
            return
        if not self.entity.carrier.isRunningState():
            return
        carrier = BigWorld.entities.get(self.entity.carrier.carrierEntId)
        if not carrier or not carrier.inWorld:
            return
        seatIdex = self.entity.carrier.get(self.entity.id)
        if not seatIdex:
            return
        self.detachBodyCarrier(carrier)
        self.carrierIdx = seatIdex
        riderScale = carrier.getRiderScale()
        self.bindOtherEntity(carrier, BIND_TYPE_CARRIER, self.carrierIdx, riderScale)
        if self.entity == BigWorld.player():
            self.entity.physics.followTarget = carrier.matrix
            gameglobal.rds.ui.pressKeyF.isInteractiveAvatar = False
            gameglobal.rds.ui.pressKeyF.removeType(const.F_AVATAR)
        self.updateFollowStyle()
        self.updateModelEffect()

    def leaveCarrier(self, carrier):
        owner = self.entity
        self.updateFollowStyle()
        if self.entity == BigWorld.player():
            self.entity.physics.followTarget = None
        if not carrier:
            bodyModel = owner.modelServer.bodyModel
            if bodyModel and not bodyModel.attached:
                BigWorld.callback(0, Functor(owner.fashion.setupModel, bodyModel, False))
                BigWorld.callback(0.1, owner.resetTopLogo)
            self.carrierIdx = 0
            return
        self.unBindOtherEntity(carrier, BIND_TYPE_CARRIER, self.carrierIdx)
        self.carrierIdx = -1

    def onAmmoTypeChange(self):
        owner = self.entity
        if not hasattr(owner, 'ammoType'):
            return
        if owner.ammoType == gametypes.AMMO_TYPE_NONE:
            self._leaveAmmoTypeChange()
        else:
            self._enterAmmoTypeChange()

    def _enterAmmoTypeChange(self):
        owner = self.entity
        if not hasattr(owner, 'ammoType'):
            return
        modelPath = self._getAmmoModelPath(owner.ammoType)
        if not modelPath:
            return
        clientUtils.fetchModel(self.threadID, self._afterTransfigurationModelFinish, modelPath)

    def _leaveAmmoTypeChange(self):
        owner = self.entity
        bodyModel = owner.modelServer.bodyModel
        if bodyModel and not bodyModel.attached:
            BigWorld.callback(0, Functor(owner.fashion.setupModel, bodyModel, False))
            if hasattr(owner, 'fashion'):
                owner.fashion.setStateCaps([keys.CAPS_GROUND, keys.CAPS_GROUND])
            if hasattr(owner, 'modelServer'):
                owner.modelServer.weaponUpdate()
                owner.modelServer.bodyPartsUpdate(False, False, False)
                owner.modelServer.wearUpdate()
                owner.modelServer.bodyUpdate()
            if hasattr(owner, 'aspect'):
                modelChange = owner.aspect.wingFly != owner.aspectOld.wingFly or owner.aspect.wingFlyDyeList() != owner.aspectOld.wingFlyDyeList()
                owner.modelServer.wingFlyModelUpdate(modelChange)

    def _getAmmoModelPath(self, ammoType):
        modelId = NFD.data.get(ammoType, {}).get('model', -1)
        if modelId == -1:
            gamelog.debug('ypc@ _getAmmoModelPath modelId not found!', modelId)
            return ''
        return 'char/%d/%d.model' % (int(modelId), int(modelId))

    def _afterTransfigurationModelFinish(self, model):
        owner = self.entity
        owner.fashion.setupModel(model)
        owner.fashion.setStateCaps([keys.CAPS_RIDE])

    def enterWingWorldCarrier(self):
        if not self.bodyModel:
            return
        carrier = BigWorld.entities.get(self.entity.wingWorldCarrier.carrierEntId)
        if not carrier or not carrier.inWorld:
            return
        seatIdex = self.entity.wingWorldCarrier.get(self.entity.id)
        if not seatIdex:
            return
        if self.entity == BigWorld.player():
            if seatIdex == const.WING_WORLD_CARRIER_MAJOR_IDX:
                self.entity.ap.setYaw(carrier.yaw)
                carrier.filter.followTarget = self.entity.matrix
                self.entity.physics.followTarget = None
                self.entity.physics.followTargetDCursorYaw = False
                self.entity.physics.followTargetDCursorPitch = False
            else:
                self.updateFollowStyle()
                carrier.filter.followTarget = None
                self.entity.physics.followTarget = carrier.matrix
                self.entity.physics.followTargetDCursorYaw = True
                self.entity.physics.followTargetDCursorPitch = True
        else:
            self.entity.filter.followTarget = carrier.matrix
        self.detachBodyWingWorldCarrier(carrier)
        self.carrierIdx = seatIdex
        riderScale = carrier.getRiderScale()
        self.updateFollowStyle()
        self.updateModelEffect()
        if self.entity.topLogo:
            self.entity.topLogo.hide(True)

    def leaveWingWorldCarrier(self, carrier):
        owner = self.entity
        self.updateFollowStyle()
        if self.entity == BigWorld.player():
            self.entity.physics.followTarget = None
            self.entity.physics.followTargetDCursorYaw = False
            self.entity.physics.followTargetDCursorPitch = False
        else:
            self.entity.filter.followTarget = None
        if carrier and carrier.inWorld:
            if carrier.wingWorldCarrier.getCarrierHeaderEntId() == 0:
                carrier.filter.followTarget = None
        else:
            bodyModel = owner.modelServer.bodyModel
            if bodyModel and not bodyModel.attached:
                BigWorld.callback(0, Functor(owner.fashion.setupModel, bodyModel, False))
                BigWorld.callback(0.1, owner.resetTopLogo)
            self.carrierIdx = 0
            return
        self.carrierIdx = -1
        self.entity.topLogo and self.entity.topLogo.hideName(False)

    def detachBodyWingWorldCarrier(self, carrier):
        if self.entity.oldWingWorldCarrier:
            try:
                seatIdx = self.entity.oldWingWorldCarrier.get(self.entity.id, -1)
                if seatIdx == -1:
                    return
                seatNode = self.getBindNode(carrier, BIND_TYPE_CARRIER, seatIdx)
                if carrier.model and carrier.model.node(seatNode):
                    if self.bodyModel in carrier.model.node(seatNode).attachments:
                        carrier.model.node(seatNode).detach(self.bodyModel)
            except Exception as e:
                pass

    def enterInteractiveObject(self):
        if not self.entity.inInteractiveObject():
            return
        interObj = BigWorld.entities.get(self.entity.interactiveObjectEntId)
        if not interObj or not interObj.inWorld:
            return
        interactiveObjIdx = interObj.getInteractiveObjIdx(self.entity.id)
        if interactiveObjIdx < 0:
            return
        self.interactiveObjIdx = interactiveObjIdx
        self.oldInteractiveObjectEntId = self.entity.interactiveObjectEntId
        scale = interObj.getItemData().get('modelScale', 0)
        avatarScale = 1.0 / scale if scale else 0
        self.bindOtherEntity(interObj, BIND_TYPE_INTERACTIVE_OBJ, self.interactiveObjIdx, avatarScale)
        self.entity.playInteractiveSpecialIdle()
        if self.entity.interactiveActionId:
            self.entity.onPlayInteractiveAction(self.entity.interactiveActionId)
        self.updateModelEffect()

    def leaveInteractiveObject(self, old):
        owner = self.entity
        interObj = BigWorld.entities.get(old)
        if not interObj:
            bodyModel = owner.modelServer.bodyModel
            if bodyModel and not bodyModel.attached:
                owner.fashion.setupModel(bodyModel, False)
                BigWorld.callback(0.1, owner.resetTopLogo)
            self.interactiveObjIdx = 0
            return
        self.unBindOtherEntity(interObj, BIND_TYPE_INTERACTIVE_OBJ, self.interactiveObjIdx)
        self.interactiveObjIdx = -1
        self.oldInteractiveObjectEntId = -1

    def updateFashionEffect(self):
        entity = self.entity
        if not entity.inWorld:
            return
        if not entity.isRealModel:
            return
        if not hasattr(entity, 'getOpacityValue'):
            return
        opaVal = entity.getOpacityValue()[0]
        if opaVal in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
            return
        self.releaseFashionEffect()
        if entity.isShowClanWar():
            return
        fashionParts = charRes.PARTS_ASPECT_FASHION if entity.isShowFashion() else ['fashionHead']
        for partName in fashionParts:
            partId = getattr(entity.realAspect, partName, 0)
            if partId:
                data = ED.data.get(partId, {})
                isVisibleInWenQuan = data.get('isVisibleInWenQuan', False)
                if getattr(entity, 'inWenQuanState', False) and not isVisibleInWenQuan:
                    continue
                effects = data.get('effect', ())
                bodyTypeEffect = data.get('bodyTypeEffect', {}).get(self.getMainModelAndID()[0], ())
                for effectId in effects + bodyTypeEffect:
                    fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
                     entity.getEquipEffectPriority(),
                     self.bodyModel,
                     effectId,
                     sfx.EFFECT_LIMIT_MISC))
                    if fx:
                        self.fashionEffects.extend(fx)

    def releaseFashionEffect(self):
        if self.fashionEffects:
            for fx in self.fashionEffects:
                if fx:
                    fx.stop()

        self.fashionEffects = []

    def updateFashionIdleEffect(self):
        entity = self.entity
        if not entity.inWorld:
            return
        if not entity.isRealModel:
            return
        if not hasattr(entity, 'getOpacityValue'):
            return
        opaVal = entity.getOpacityValue()[0]
        if opaVal in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
            return
        self.releaseFashionIdleEffect()
        for partName in charRes.PARTS_ASPECT_FASHION:
            partId = getattr(entity.realAspect, partName, 0)
            if partId:
                data = ED.data.get(partId, {})
                isVisibleInWenQuan = data.get('isVisibleInWenQuan', False)
                if getattr(entity, 'inWenQuanState', False) and not isVisibleInWenQuan:
                    continue
                effects = data.get('idleEffect', [[], []])[getattr(entity, 'inFly', 0) != 0]
                for effectId in effects:
                    fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
                     entity.getEquipEffectPriority(),
                     self.bodyModel,
                     effectId,
                     sfx.EFFECT_LIMIT_MISC))
                    if fxs:
                        for fx in fxs:
                            fx.overCallback(None)

                        self.fashionIdleEffects[effectId] = fxs

        self.playFashionIdleEffect()

    def playFashionIdleEffect(self):
        entity = self.entity
        if not entity.inWorld:
            return
        inMoving = entity.inMoving() or entity.isVerticalMoving
        for fxs in self.fashionIdleEffects.itervalues():
            for fx in fxs:
                if inMoving:
                    fx.stop()
                else:
                    fx.force()

    def playFashionBoredEffect(self):
        owner = self.entity
        if not owner.inWorld:
            return
        if owner.inFly:
            return
        if owner.bianshen and owner.bianshen[0] != gametypes.BIANSHEN_HUMAN:
            return
        for partName in charRes.PARTS_ASPECT_FASHION:
            partId = getattr(owner.realAspect, partName, 0)
            if partId:
                effectIds = ED.data.get(partId, {}).get('boredEffect', [])
                for effId in effectIds:
                    owner.removeFx(effId)
                    fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (owner.getEquipEffectLv(),
                     owner.getEquipEffectPriority(),
                     owner.model,
                     effId,
                     sfx.EFFECT_LIMIT_MISC))
                    if fxs:
                        owner.addFx(effId, fxs)

    def releaseFashionIdleEffect(self):
        for effectId in self.fashionIdleEffects.keys():
            info = sfx.gEffectInfoMap.getInfo(effectId)
            fxs = self.fashionIdleEffects.pop(effectId)
            if info:
                nodeInfo = info[0]
                for item in nodeInfo:
                    nodeType = item[0]
                    nodeStr = item[1]
                    if nodeType == sfx.ATTACH_ROOT:
                        node = self.bodyModel.root
                    else:
                        node = self.bodyModel.node(nodeStr)
                    for fx in fxs:
                        sfx.gEffectMgr.giveBack(effectId, fx, node, sfx.EFFECT_LIMIT_MISC)

    def updateModelEffect(self):
        self.updateWeaponEffect()
        self.updateFashionEffect()
        self.updateWearEffect()
        self.updateFashionIdleEffect()

    def refreshBackWearVisible(self):
        self.backwear.refreshOpacityState()


class SimpleModelServer(IMonsterCommon):

    def __init__(self, entity, urgent = False, immediateLoad = True, setTint = True):
        self.entity = entity
        self.startTime = time.clock()
        self.model = None
        self.attachModel = {}
        self.attachNewModel = {}
        self.avatarConfig = None
        self.rideModel = None
        self.rideAttached = None
        self.wingFlyModel = None
        self.lifeSkillModel = None
        self.rideID = None
        self.wingID = None
        self.state = STATE_EMPTY
        self.setTint = setTint
        itemData = entity.getItemData()
        multiPart = itemData.get('multiPart', False)
        if urgent:
            threadId = gameglobal.URGENT_THREAD
        else:
            threadId = gameglobal.getLoadThread()
        if immediateLoad:
            modelId = itemData.get('model', None)
            if not modelId and not multiPart and not itemData.get('fullPath', None) or entity.IsSummonedSprite and not seqTask.shouldLoadRealModel(entity):
                entity.firstFetchFinished = True
                BigWorld.callback(0, entity.afterModelFinish)
                return
            if modelId > const.MODEL_AVATAR_BORDER:
                clientcom.ConfigCache.fetchConfig('%s/%d.xml' % (gameglobal.AVATAR_TEMPLATE_PATH, modelId), Functor(self._onLoadAvatarConfig, entity.id, threadId, itemData, urgent))
            elif itemData.get('collide', 0) != 0 and itemData.get('dynamicObstacle', False):
                loadObstacleModelByItemData(entity, self._singlePartModelFinish, itemData)
            else:
                loadModelByItemData(entity.id, threadId, self._singlePartModelFinish, itemData, multiPart, urgent)
        self.rideID = itemData.get('rideId', 0)
        if self.rideID:
            self.rideAttached = attachedModel.BeastAttachModel(entity.id, threadId)
            self.rideAttached.equipItem(self.rideID)
        self.wingID = itemData.get('wingId', 0)
        if self.wingID:
            self.wingFlyModel = attachedModel.WingFlyAttachModel(entity.id, threadId)
            self.wingFlyModel.equipItem(self.wingID)
        self.lifeSkillModel = attachedModel.LifeSkillAttachModel(entity.id, threadId)

    def freezeEffect(self, freezeTime):
        pass

    def clearFreezeEffect(self):
        pass

    def refreshWingFlyState(self, withEffect = True, wingInAirEffect = False):
        entity = self.entity
        if entity.model:
            self.wingFlyModel.attach(entity.model)
        if withEffect:
            self.wingFlyModel.refreshMountEffect(True)

    def _wingFlyModelFinished(self, key, model):
        pass

    def _rideModelFinish(self, rideID, showEffect, model):
        entity = self.entity
        if not entity or not entity.inWorld:
            return
        self.rideModel = model
        if getattr(entity, 'firstFetchFinished', False):
            localBodyModel = entity.model
            entity.fashion.setupModel(self.rideModel, False)
            try:
                self.rideModel.setHP('HP_ride', localBodyModel)
            except:
                return

            self.rideModel.scale = (self.rideAttached.scale, self.rideAttached.scale, self.rideAttached.scale)
            entity.fashion.setStateCaps([keys.CAPS_RIDE])
            try:
                am = localBodyModel.motors[0]
            except:
                am = BigWorld.ActionMatcher(entity)
                am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_GROUND]
                localBodyModel.motors = (am,)

            am.matcherCoupled = False
            am.footTwistSpeed = 0.0
            utils.addMotorsChild(self.rideModel.motors, am)
            self.state = STATE_HORSE
            if utils.instanceof(entity, 'Npc'):
                if entity._isQuestNpc():
                    entity.taskEffect = None
                    entity.questTopLogoRefresh()

    def _onLoadAvatarConfig(self, eId, threadId, itemData, urgent, avatarInfo):
        modelId = itemData.get('model')
        en = BigWorld.entities.get(eId)
        if not en or not en.inWorld:
            return
        self.avatarConfig = avatarInfo
        loadModelByItemData(eId, threadId, self._singlePartModelFinish, avatarInfo, True, urgent, modelId)

    def fadeToReal(self, fadeTime):
        pass

    def realToFade(self, fadeTime):
        pass

    def getAllWeaponModels(self):
        return []

    def getAllAttachedModels(self):
        return []

    def release(self):
        for i in self.attachModel:
            gamelog.debug('release:', self.attachModel[i], i, self.attachModel[i][0])
            self.attachModel[i] = None

        for i in self.attachNewModel:
            self.attachNewModel[i] = None

        self.model = None
        self.entity = None
        if self.rideAttached:
            self.rideAttached.release()
            self.rideModel = None
            self.rideID = None
        if self.wingFlyModel:
            self.wingFlyModel.release()
            self.wingID = None
        self.state = STATE_EMPTY
        self.attachNewModel = {}
        self.attachModel = {}
        if self.lifeSkillModel:
            self.lifeSkillModel.release()

    def _singlePartModelFinish(self, model):
        if not self.entity or not hasattr(self.entity, 'allModels'):
            return
        if not model:
            gamelog.error('Error _modelLoadFinish, model is None', self.entity.id)
            return
        entity = self.entity
        self.model = model
        itemData = entity.getItemData()
        if not utils.instanceof(entity, 'LoginModel'):
            entity.setEntityFilter()
        if itemData.get('collide', 0) != 0 and itemData.get('dynamicObstacle', False):
            entity.fashion.setupObstacleModel(model)
        else:
            entity.fashion.setupModel(model)
            entity.model.scale = entity.getModelScale()
            tintName = clientcom.getMatrialsName(entity, itemData)
            multiPart = itemData.get('multiPart', False)
            if self.setTint and not multiPart and tintName:
                if entity.needSetStaticStates():
                    tintalt.ta_set_static_states(model, tintName, needBuildName=False)
                else:
                    tintalt.setContentStateNoUse(tintName)
        boredProbability = itemData.get('boredProbability', (5.0, 80))
        entity.fashion.boredTime = boredProbability[0]
        entity.fashion.boredIdleProbability = boredProbability[1]
        self.state = STATE_HUMAN
        if itemData.get('noIcon', 0):
            entity.noIcon = 1
        floatHeight = itemData.get('floatHeight', None)
        if floatHeight:
            floatage = BigWorld.PyPoseControl()
            floatage.floatHeight = floatHeight
            setattr(entity.model, 'floatage', floatage)
        modelNeedHide = itemData.get('modelShow', 0)
        if hasattr(entity.model, 'setModelNeedHide'):
            entity.model.setModelNeedHide(not modelNeedHide, 1.0)
        self.attachModelFromData()
        if getattr(entity, 'bindHostNode', None) and getattr(entity, 'hostId', None):
            self.enterHostNode()
        entity.firstFetchFinished = True
        entity.afterModelFinish()
        if self.rideModel:
            self._rideModelFinish(self.rideID, False, self.rideModel)
        if hasattr(entity, 'forceUpdateEffect'):
            entity.forceUpdateEffect()
        self.playBornAction(entity, itemData)
        if self.wingID:
            self.refreshWingFlyState()

    def enterHostNode(self):
        owner = self.entity
        hostEnt = BigWorld.entity(owner.hostId)
        if not hostEnt or not hostEnt.inWorld:
            return
        bodyModel = owner.model
        dummyModel = sfx.getDummyModel(False)
        owner.fashion.setupModel(dummyModel, False)
        seatNode = owner.bindHostNode
        if hostEnt.model.node(seatNode) is None:
            return
        cleanList = []
        for item in hostEnt.model.node(seatNode).attachments:
            cleanList.append(item)

        for item in cleanList:
            hostEnt.model.node(seatNode).detach(item)

        if not bodyModel.attached:
            hostEnt.model.node(seatNode).attach(bodyModel, 'HP_ride')
            avatarScale = 1
            if hasattr(hostEnt, 'getItemData'):
                itemData = hostEnt.getItemData()
                avatarScale = itemData.get('riderScale', 1)
            if avatarScale:
                hostEnt.model.node(seatNode).scale(avatarScale)

    def playWeaponAction(self, actions):
        pass

    def playLeftWeaponAction(self, actions):
        pass

    def playRightWeaponAction(self, actions):
        pass

    def playBornAction(self, entity, itemData):
        playSeq = []
        if hasattr(entity, 'bornActionName') and entity.bornActionName:
            playSeq.append(entity.bornActionName)
            entity.bornActionName = None
        if entity.IsMonster or entity.IsSummonedBeast or getattr(entity, 'IsOreSpawnPoint', False):
            if entity.bornStage in (gametypes.MONSTER_BORN_STAGE_ACT, gametypes.MONSTER_BORN_STAGE_IDLE_ACT):
                self.attachBornEffectAndTint(itemData)
                bornIdleActName = entity.fashion.getBornIdleActionName()
                if bornIdleActName:
                    entity.bornIdleActName = bornIdleActName
                    playSeq.append(bornIdleActName)
                    entity.fashion.setDoingActionType(action.BORN_IDLE_ACTION)
                    entity.setSelected(True)
            else:
                entity.bornFadeIn()
        idleActName = itemData.get('idleAct', None)
        if idleActName:
            entity.idleActName = idleActName
            playSeq.append(idleActName)
        gamelog.debug('playBornAction', playSeq)
        if playSeq:
            entity.fashion.playActionSequence(self.model, playSeq, None)
            if hasattr(entity, 'playBornEff'):
                entity.playBornEff()

    def attachBornEffectAndTint(self, itemData):
        entity = self.entity
        bornAttaches = itemData.get('bornAttaches', None)
        if bornAttaches:
            for attachHp, attachEff, attachEffScale in bornAttaches:
                node = entity.model.node(attachHp)
                if node == None:
                    gamelog.error('zf attachHp node is not exit:', attachHp)
                    continue
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_ONNODE, (entity.getEquipEffectLv(),
                 entity.getEquipEffectPriority(),
                 entity.model,
                 attachHp,
                 attachEff,
                 sfx.EFFECT_LIMIT,
                 gameglobal.EFFECT_LAST_TIME))
                if fx:
                    for fxItem in fx:
                        fxItem.scale(attachEffScale, attachEffScale, attachEffScale)

        if hasattr(entity, '_addTintByName'):
            entity._addTintByName('bornTint', itemData)

    def getMainModelAndID(self):
        owner = self.entity
        return (owner.fashion.modelID, owner.model)

    def refreshWeaponState(self):
        pass

    def changeModelFromData(self, changeType):
        entity = self.entity
        itemData = entity.getItemData()
        if changeType:
            dmgDfMap = itemData.get('dmgDfMap', None)
            dmgSpMap = itemData.get('dmgSpMap', None)
            dmgNmMap = itemData.get('dmgNmMap', None)
            if dmgDfMap and dmgSpMap and dmgNmMap:
                tintalt.ta_add(entity.allModels, 'texture', [dmgDfMap, dmgSpMap, dmgNmMap])
            dmgAvatar = itemData.get('dmgAvatar', None)
            if dmgAvatar == None:
                return
            for attachHp, cType, attachModel, attachEff, attachScale in dmgAvatar:
                if not attachHp:
                    return
                node = entity.model.node(attachHp)
                if not node:
                    gamelog.error('zf:attachHp is not exit')
                    return
                entity.model.setHP(attachHp, None)
                if cType:
                    if attachEff:
                        sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
                         entity.getEquipEffectPriority(),
                         entity.model,
                         attachEff,
                         sfx.EFFECT_LIMIT))
                    if attachScale <= 0:
                        attachScale = 1
                    modelPath = 'char/' + str(attachModel) + '/' + str(attachModel) + '.model'
                    charRes.getSimpleModel(modelPath, None, Functor(self._afterAttachModelFinished, entity, attachHp, attachScale, modelPath, None, None))

        else:
            for i in self.attachNewModel:
                attachHp = self.attachNewModel[i][0]
                attachScale = self.attachNewModel[i][1]
                entity.model.setHP(attachHp, None)
                node = entity.model.node(attachHp)
                node.scale(attachScale)

        self.attachModelFromData()
        entity.resetTopLogo()

    def removeCarrouselSeat(self, idx):
        carrousel = self.entity
        seatNode = getCarrouselSeatNode(carrousel, None, idx)
        carrouselModel = getattr(carrousel, 'model', None)
        if carrouselModel is not None and carrouselModel.node(seatNode) is not None:
            cleanList = [ item for item in carrouselModel.node(seatNode).attachments ]
            for item in cleanList:
                carrouselModel.node(seatNode).detach(item)

    def sitInChair(self, chairModel):
        entity = self.entity
        bodyModel = entity.model
        entity.modelServer.bodyModel = bodyModel
        dummyModel = sfx.getDummyModel(False)
        entity.fashion.setupModel(dummyModel, False)
        seatNode = chairModel.node('HP_chair01')
        if not bodyModel.attached:
            seatNode.attach(bodyModel, 'HP_ride')
        entity.resetTopLogo()

    def leaveChair(self, chairModel):
        entity = self.entity
        seatNode = chairModel.node('HP_chair01')
        for item in seatNode.attachments:
            seatNode.detach(item)

        bodyModel = entity.model
        if bodyModel and not bodyModel.attached:
            entity.fashion.setupModel(bodyModel, False)
        entity.modelServer.bodyModel = None
        entity.resetTopLogo()


class DroppedItemModelServer(SimpleModelServer):

    def __init__(self, entity, urgent = False):
        super(DroppedItemModelServer, self).__init__(entity, urgent)

    def _singlePartModelFinish(self, model):
        charRes.getSimpleModel(gameglobal.COMMON_MODEL_PATH, None, Functor(self._afterCommonModelFinish, model))

    def _afterCommonModelFinish(self, dropModel, commModel):
        entity = self.entity
        if not entity.inWorld:
            dropModel = None
            commModel = None
            return
        entity.filter = BigWorld.DumbFilter()
        try:
            if dropModel and commModel:
                node = commModel.node('biped_Obj')
                node.attach(dropModel)
                commModel.visble = False
        except:
            raise Exception('_afterCommonModelFinish %s %s %s' % (str(getattr(dropModel, 'attached', -1)), str(dropModel.sources), str(commModel.sources)))

        if hasattr(entity, 'fashion') and commModel:
            entity.fashion.setupModel(commModel)
        entity.firstFetchFinished = True
        entity.afterModelFinish()
        entity.resetTopLogo()


def getCarrouselSeatNode(carrousel, entity, idx = None):
    carrierAttachList = CD.data.get(carrousel.carrouselId, {}).get('carrierAttachList', [])
    if idx:
        return carrierAttachList[idx - 1]
    else:
        return carrierAttachList[entity.carrousel[1] - 1]


def loadModelByItemData(entityid, threadID, callback, itemData, multiPart = False, urgent = False, modelId = None):
    entity = BigWorld.entities.get(entityid)
    if itemData != None:
        if not multiPart:
            if itemData.has_key('fullPathWithMatter'):
                res = itemData.get('fullPathWithMatter', None)
                dye = None
            else:
                res = itemData.get('fullPath', None)
                if not res:
                    modelId = itemData.get('model', 0)
                    res = 'char/%i/%i.model' % (modelId, modelId)
                dye = clientcom.getMatrialsName(entity, itemData)
        else:
            clientcom.fetchSimpleTintEffectsContents(entityid, threadID, itemData, callback, realParseCharRes)
            return
    else:
        res = gameglobal.defaultModelName
        dye = 'Default'
    realLoaderByItemData(entityid, threadID, res, dye, callback)


def realParseCharRes(entityid, threadID, itemData, callback, tintAvatarTas, tintAvatarName, tintEffects):
    entity = BigWorld.entities.get(entityid)
    if not entity or not entity.inWorld:
        return
    clientcom.tintSectionsToCache(entity, tintAvatarTas, tintAvatarName, tintEffects)
    mpr = charRes.convertToMultiPartRes(itemData, entity.id)
    res = mpr.getPrerequisites()
    dye = None
    realLoaderByItemData(entityid, threadID, res, dye, callback)


def realLoaderByItemData(entityid, threadID, res, dye, callback):
    if dye:
        res = (res, ('*', dye))
    loader = seqTask.SeqModelLoader(entityid, threadID, callback)
    entity = BigWorld.entities.get(entityid)
    isUrgentLoad = False
    if entity and entity.__class__.__name__ == 'Transport':
        isUrgentLoad = True
    loader.beginLoad(res, isUrgentLoad)


def loadObstacleModelByItemData(entity, callback, itemData):
    modelName = itemData.get('fullPath', None) or 'char/%i/%i.model' % (itemData['model'], itemData['model'])
    scale = itemData.get('scale', 1.0)
    scaleMatrix = Math.Matrix()
    scaleMatrix.setScale((scale, scale, scale))
    mp = Math.MatrixProduct()
    mp.a = scaleMatrix
    mp.b = entity.matrix
    needLoadNow = itemData.get('needLoadNow', False)
    if not needLoadNow:
        BigWorld.fetchObstacleModel(modelName, mp, True, callback)
    else:
        model = BigWorld.PyModelObstacle(modelName, mp, True)
        callback(model)
