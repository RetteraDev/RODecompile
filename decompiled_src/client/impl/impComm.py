#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impComm.o
from gamestrings import gameStrings
import BigWorld
import const
import utils
import clientcom
import formula
import gameglobal
import gamelog
import gametypes
import keys
from appSetting import Obj as AppSettings
from helpers import modelServer
from helpers import ufo
from sfx import sfx
from sfx import flyEffect
from callbackHelper import Functor
from helpers import action
from data import char_toplogo_height_data as CTLHD
from data import horsewing_data as HWCD
from data import map_config_data as MCD
from data import multiline_digong_data as MDD
from data import physics_config_data as PCD
from data import sheng_si_chang_data as SSCD
from data import school_effect_data as SCED
from data import horsewing_effect_data as HWED
from data import title_data as TD
from data import apprentice_config_data as ACD
from data import sys_config_data as SCD
from data import equip_data as ED
from data import horsewing_camera_data as HCD
from data import pet_skill_data as PSD
from data import foot_dust_data as FDD
from data import zaiju_data as ZJD
from data import wing_world_carrier_data as WWCD
from data import fight_for_love_config_data as FFLCD
from data import clan_war_fort_data as CWFD

class ImpComm(object):

    def isQuickDashJump(self):
        if self.dashingInitTime and self.dashingStartTime - self.dashingInitTime < 0.2:
            return False
        return self.dashingJumpStartTime - self.dashingStartTime < PCD.data.get('jumpUpChangeTime', gametypes.JUMP_UP_CHANGE_TIME) and self.dashNormalJump

    def inFuben(self, fbNo_ = 0):
        if not hasattr(self, 'spaceNo'):
            return False
        if not formula.spaceInFbOrDuel(self.spaceNo):
            return False
        fbNo = formula.getFubenNo(self.spaceNo)
        if fbNo_ and fbNo_ != fbNo:
            return False
        return True

    def inFubens(self, fbNos_ = set()):
        if not hasattr(self, 'spaceNo'):
            return False
        if not formula.spaceInFbOrDuel(self.spaceNo):
            return False
        fbNo = formula.getFubenNo(self.spaceNo)
        if fbNos_ and fbNo not in fbNos_:
            return False
        return True

    def inFubenType(self, fbType_ = None):
        if not hasattr(self, 'spaceNo'):
            return False
        if not formula.spaceInFbOrDuel(self.spaceNo):
            return False
        fbNo = formula.getFubenNo(self.spaceNo)
        fbType = formula.whatFubenType(fbNo)
        if fbType_ and fbType_ != fbType:
            return False
        return True

    def inFubenTypes(self, fbTypes_ = set()):
        if not hasattr(self, 'spaceNo'):
            return False
        if not formula.spaceInFbOrDuel(self.spaceNo):
            return False
        fbNo = formula.getFubenNo(self.spaceNo)
        fbType = formula.whatFubenType(fbNo)
        if fbTypes_ and fbType not in fbTypes_:
            return False
        return True

    def inMLYaoLiSpace(self):
        if not hasattr(self, 'spaceNo'):
            return False
        if not self.inMLSpace():
            return False
        mlgNo = formula.getMLGNo(self.spaceNo)
        if not MDD.data.get(mlgNo, {}).get('calcYaoli'):
            return False
        return True

    def inMLDoubleExpSpace(self):
        if not hasattr(self, 'spaceNo'):
            return False
        if not self.inMLSpace():
            return False
        mlgNo = formula.getMLGNo(self.spaceNo)
        if not MDD.data.get(mlgNo, {}).get('doubleExp'):
            return False
        return True

    def needHideEntity(self):
        if self != BigWorld.player():
            spaceNo = getattr(BigWorld.player(), 'spaceNo', 0)
            mapId = formula.getMapId(spaceNo)
            if MCD.data.get(mapId, {}).get('hideAvatar', 0):
                return True
        return False

    def needDisableFootIK(self):
        gameStrings.TEXT_IMPCOMM_141
        if self.bianshen[0] != gametypes.BIANSHEN_HUMAN:
            return True
        if self.bsState:
            return True
        if self.inSwim:
            return True
        if self.inFly:
            return True
        if self.fashion.isStartJump:
            return True
        if self.fashion.isPlayer and gameglobal.rds.cam.currentScrollNum < 3:
            return True
        if self.weaponState:
            return True
        return False

    def resetFootIK(self):
        model = self.model
        if not hasattr(model, 'footIK') or not model.footIK:
            return
        if self.needDisableFootIK():
            model.footIK.enable = False
        else:
            model.footIK.enable = True
            if self.physique and self.physique.sex == const.SEX_FEMALE:
                model.footIK.footAngleLimit = 0.3

    def refreshTopLogo(self):
        if not self.inWorld or not self.topLogo:
            return
        p = BigWorld.player()
        targetName = self.roleName
        topLogoName = self.roleName
        nowFbNo = formula.getFubenNo(BigWorld.player().spaceNo)
        if nowFbNo in SSCD.data:
            targetName = const.SSC_ROLENAME
            topLogoName = const.SSC_ROLENAME
            self.topLogo.setAvatarTitle(const.SSC_TITLENAME, 1)
        elif p.bHideFightForLoveFighterName(self):
            nameInfo = self.getFightForLoveNameInfo()
            name = nameInfo.get('name', '')
            title = nameInfo.get('title', '')
            targetName = name
            topLogoName = name
            self.topLogo.setAvatarTitle(title, 1)
        elif hasattr(p, 'isBianShenZaiJuInPUBG') and p.isBianShenZaiJuInPUBG(self):
            targetName = ''
            topLogoName = ''
        elif getattr(self, 'jctSeq', 0) and p.inClanCourier():
            name = self.getJCTRoleName()
            self.topLogo.name = name
            self.topLogo.setAvatarTitle('', 1)
        else:
            targetName = p.anonymNameMgr.checkNeedAnonymousName(self, targetName)
            topLogoName = p.anonymNameMgr.checkNeedAnonymousName(self, topLogoName)
            if gameglobal.showEntityID and not BigWorld.isPublishedVersion():
                topLogoName += ':' + str(self.id)
        self.topLogo.name = topLogoName
        self.topLogo.updateRoleName(self.topLogo.name)
        if p.targetLocked == self:
            gameglobal.rds.ui.target.setName(targetName)
        if p.optionalTargetLocked == self:
            gameglobal.rds.ui.subTarget.setName(targetName)

    def refreshAvatarSummonedSpriteTopLogo(self):
        if not self.inWorld or not (hasattr(self, 'spriteObjId') and self.spriteObjId):
            return
        else:
            p = BigWorld.player()
            spriteEnt = BigWorld.entity(self.spriteObjId)
            if spriteEnt:
                spriteTopLogo = getattr(spriteEnt, 'topLogo', None)
                nameString = spriteEnt.roleName
                if gameglobal.showEntityID and not BigWorld.isPublishedVersion():
                    nameString += ':' + str(spriteEnt.id)
                if spriteTopLogo:
                    nameString = p.anonymNameMgr.checkNeedAnonymousName(spriteEnt, nameString)
                    spriteTopLogo.updateRoleName(nameString)
            return

    def resetShadowUfo(self):
        if self.inSwim or self.inFly or self.isJumping:
            if self.fashion.ufo and self.fashion.ufo.ufoType == ufo.UFO_SHADOW:
                self.fashion.attachUFO(ufo.UFO_NULL)
            elif self.fashion.ufo:
                if self.fashion.ufo.ufoType % 2 == 1:
                    self.fashion.attachUFO(self.fashion.ufo.ufoType + 1)
        elif not self.fashion.ufo:
            opVal = self.getOpacityValue()
            if opVal[0] == gameglobal.OPACITY_FULL:
                self.fashion.attachUFO(ufo.UFO_SHADOW)
        elif self.fashion.ufo.ufoType % 2 == 0:
            self.fashion.attachUFO(self.fashion.ufo.ufoType - 1)

    def resetTopLogoAfterAction(self, entity):
        entity.resetTopLogo()
        if entity == BigWorld.player():
            entity.resetCamera()

    def getTopLogoHeight(self):
        self.topLogoOffset = 0.0
        height = self.getModelHeight()
        if getattr(self, 'bsState', None):
            self.topLogoOffset = 0.4
        elif self.inFlyTypeWing():
            topLogoKey = self.modelServer.wingFlyModel.topLogoKey
            topLogoData = HWCD.data.get(topLogoKey, None)
            if topLogoData:
                self.topLogoOffset = topLogoData[0].get('heightOffset', 0.2)
        elif self.inFlyTypeFlyRide():
            topLogoKey = self.modelServer.rideAttached.topLogoKey
            topLogoData = HWCD.data.get(topLogoKey, None)
            if topLogoData:
                self.topLogoOffset = topLogoData[0].get('flyHeightOffset', 0.2)
        elif self.modelServer.state != modelServer.STATE_HUMAN:
            topLogoKey = self.modelServer.rideAttached.topLogoKey
            topLogoData = HWCD.data.get(topLogoKey, None)
            if topLogoData:
                self.topLogoOffset = topLogoData[0].get('heightOffset', 0.2)
        else:
            topLogoKey = self.fashion.modelID
            topLogoData = CTLHD.data.get(topLogoKey, None)
            if topLogoData:
                self.topLogoOffset = topLogoData.get('heightOffset', 0.2)
        if getattr(self.model, 'floatage', None):
            height = height + self.model.floatage.floatHeight
        gamelog.debug('getTopLogoHeight:', self.topLogoOffset, height)
        if self.life == gametypes.LIFE_DEAD:
            height = (height + self.topLogoOffset) / 2.0
        else:
            height = height + self.topLogoOffset
        return height

    def updateBodySlope(self):
        gamelog.debug('updateBodySlope', self.bianshen, self.life)
        if self.life == gametypes.LIFE_DEAD or self.inRiding() and not self.inFly:
            self.filter.enableBodyPitch = True
        else:
            self.filter.enableBodyPitch = False
        if self.filter.enableBodyPitch:
            self.filter.feetDist = self.getFeetDis()
        else:
            self.filter.feetDist = 0.1
        if self.model != None:
            if hasattr(self.model, 'straighten'):
                self.model.straighten()
        if FDD.data.get(self.fashion.modelID, {}).has_key('notEnableBodyPitch'):
            notEnableBodyPitch = FDD.data.get(self.fashion.modelID, {}).get('notEnableBodyPitch', 0)
            self.filter.enableBodyPitch = not notEnableBodyPitch

    def getFeetDis(self):
        if self.inRiding():
            if self.modelServer.rideID:
                feetDist = self.modelServer.getRideFeetDist()
                if feetDist:
                    return feetDist
        return 0.8

    def refreshToplogoTitle(self):
        p = BigWorld.player()
        if hasattr(self, 'topLogo') and self.topLogo:
            name, style = self.getActivateTitleStyle()
            realName = p.anonymNameMgr.checkNeedAnonymousTitle(self, name)
            self.topLogo.setAvatarTitle(realName, style)
            if self != BigWorld.player():
                self.topLogo.hideAvatarTitle(gameglobal.gHideAvatarTitle)
            if p.isPlayingFightForLoveScenario():
                self.topLogo.hideAvatarTitle(True)

    def getActivateTitleStyle(self):
        name = ''
        style = 1
        if self.activeTitleType == const.ACTIVE_TITLE_TYPE_COMMON:
            if const.TITLE_TYPE_WORLD < len(self.currTitle):
                prefixName = self.getTitleName(self.currTitle[const.TITLE_TYPE_PREFIX])
                colorName = self.getTitleName(self.currTitle[const.TITLE_TYPE_COLOR])
                basicName = self.getTitleName(self.currTitle[const.TITLE_TYPE_BASIC])
                name = prefixName + colorName + basicName
                if colorName:
                    style = TD.data.get(self.currTitle[const.TITLE_TYPE_COLOR], {}).get('style', 1)
                elif basicName:
                    style = TD.data.get(self.currTitle[const.TITLE_TYPE_BASIC], {}).get('style', 1)
                elif prefixName:
                    style = TD.data.get(self.currTitle[const.TITLE_TYPE_PREFIX], {}).get('style', 1)
        elif self.activeTitleType == const.ACTIVE_TITLE_TYPE_WORLD:
            if const.TITLE_TYPE_WORLD < len(self.currTitle):
                titleData = TD.data.get(self.currTitle[const.TITLE_TYPE_WORLD], {})
                if titleData:
                    name = self.getTitleName(self.currTitle[const.TITLE_TYPE_WORLD])
                    style = titleData.get('style', 1)
        return (name, style)

    def getMarriageTitleSex(self):
        if self.marriageTitleSex > 0:
            return self.marriageTitleSex
        return self.physique.sex

    def getTitleName(self, titleId = 0):
        tData = TD.data.get(titleId, {})
        name = ''
        if tData:
            if tData.get('gId', 0) == gametypes.FAME_GROUP_GUILD:
                name = tData.get('name', '') % self.guildName
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_MENTOR:
                mentor = ACD.data.get('apprenticeTitleList', {}).get(getattr(self, 'apprenticeTitleMentor', 0), {}).get(gametypes.APPRENTICE_KEY_MENTOR, '')
                name = tData.get('name', '') % mentor
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_APPRENTICE:
                apprentice = ACD.data.get('apprenticeTitleList', {}).get(getattr(self, 'apprenticeTitleApprentice', 0), {}).get(gametypes.APPRENTICE_KEY_APPRENTICE, '')
                name = tData.get('name', '') % apprentice
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_INTIMACY:
                p = BigWorld.player()
                if p == self:
                    if p.friend.intimacyTgt == 0:
                        tgtRoleName = ''
                    else:
                        f = p.friend.get(p.friend.intimacyTgt)
                        if f:
                            tgtRoleName = f.name
                        else:
                            tgtRoleName = ''
                else:
                    tgtRoleName = self.intimacyTgtName
                name = tData.get('name', '%s') % tgtRoleName
            elif tData.get('gId') == gametypes.TITLE_GROUP_PARTNER:
                name = self.getCurPartnerTitleName() if not self._isSoul() else ''
            elif tData.get('gId') == gametypes.TITLE_GROUP_MARRIAGE:
                if self.getMarriageTitleSex() == const.SEX_MALE:
                    name = tData.get('name', gameStrings.TEXT_FRIENDREQUESTPROXY_132) % (self.intimacyTgtName, gametypes.MARRIAGE_HASBAND_DESC)
                elif self.getMarriageTitleSex() == const.SEX_FEMALE:
                    name = tData.get('name', gameStrings.TEXT_FRIENDREQUESTPROXY_132) % (self.intimacyTgtName, gametypes.MARRIAGE_WIFE_DESC)
            elif tData.get('gId') == gametypes.TITLE_GROUP_ENGAGE:
                if self.getMarriageTitleSex() == const.SEX_MALE:
                    name = tData.get('name', gameStrings.TEXT_FRIENDREQUESTPROXY_132) % (self.intimacyTgtName, gametypes.ENGAGE_HASBAND_DESC)
                elif self.getMarriageTitleSex() == const.SEX_FEMALE:
                    name = tData.get('name', gameStrings.TEXT_FRIENDREQUESTPROXY_132) % (self.intimacyTgtName, gametypes.ENGAGE_WIFE_DESC)
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_SOLE_MENTOR:
                name = tData.get('name', '%s') % self.soleApprenticeNameEx
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_SOLE_APPRENTICE:
                name = tData.get('name', '%s') % self.soleMentorNameEx
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_GUILD_MERGER:
                name = tData.get('name', '%s') % self.lastGuildNameFromMerger
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_FIGHT_FOR_LOVE:
                titleInfo = self.fightForLoveTitleInfo.get(titleId, (0, '', 0))
                name = tData.get('name', '%s') % (titleInfo[1],)
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_CROSS_CLAN_WAR_OCCUPY:
                titleInfo = self.crossClanWarTitleInfo.get(titleId, (0, 0))
                name = tData.get('name', '%s,%s') % (gameglobal.rds.ui.crossClanWar.getServerName(titleInfo[0]), self.getFortName(titleInfo[1]))
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_CROSS_CLAN_WAR_KILL_HEADER:
                titleInfo = self.crossClanWarTitleInfo.get(titleId, (0, ''))
                name = tData.get('name', '%s') % titleInfo[1]
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_MISS_TIANYU_FANS:
                name = tData.get('name', '%s') % self.mtNameCache
            elif tData.get('gId', 0) in gametypes.TITLE_GROUP_AID_TITLE:
                if self == BigWorld.player():
                    aidArgs = self.aidTitleInfo.get(titleId, [''])
                else:
                    aidArgs = self.showAidTitleArgs.get(titleId, [''])
                name = tData.get('name', '%s') % aidArgs
            else:
                name = tData.get('name', '')
        return name

    def getFortName(self, fortId):
        data = CWFD.data.get(fortId)
        if not data:
            return ''
        return data.get('showName')

    def releaseEquipEnhanceEffects(self):
        if self.equipEnhanceEffects:
            for e in self.equipEnhanceEffects:
                if e:
                    e.stop()

        self.equipEnhanceEffects = []

    def getAllEnhanceRefining(self):
        refining = 0
        if hasattr(self, 'aspect'):
            refining = self.aspect.getEnhLvsSum()
        return refining

    def getEquipEnhanceEffects(self):
        enhanceRefining = self.getAllEnhanceRefining()
        if not enhanceRefining:
            return (None, None)
        else:
            enhanceEffect = SCED.data.get(self.school, {}).get('enhanceEffect', {})
            if not enhanceEffect:
                return (None, None)
            keys = [ refining for refining in enhanceEffect.keys() if refining <= enhanceRefining ]
            if not keys:
                return (None, None)
            maxKey = max(keys)
            scaleKey = clientcom.getAvatarWeaponModelScale(self)
            scale = SCED.data.get(self.school, {}).get(scaleKey, 1.0)
            return (enhanceEffect.get(maxKey, []), scale)

    def refreshEquipEnhanceEffects(self):
        self.releaseEquipEnhanceEffects()
        if not gameglobal.SHOW_EQUIP_ENHANCE_EFF and gameglobal.rds.GameState != gametypes.GS_LOGIN:
            return
        effs, eScale = self.getEquipEnhanceEffects()
        if not effs:
            return
        for ef in effs:
            effLv = self.getBasicEffectLv()
            priority = self.getBasicEffectPriority()
            model = self.modelServer.bodyModel
            efs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, [effLv,
             priority,
             model,
             ef,
             sfx.EFFECT_UNLIMIT])
            if efs:
                for ef in efs:
                    ef.scale(eScale)

                self.equipEnhanceEffects.extend(efs)

    def releaseHorseWingEffect(self, verticale = False):
        if self.horseGroundMoveEffects:
            for ef in self.horseGroundMoveEffects:
                if ef:
                    ef.stop()

            self.horseGroundMoveEffects = []
        if not verticale and self.horseDashEffects:
            for ef in self.horseDashEffects:
                if ef:
                    ef.stop()

            self.horseDashEffects = []
        if self.flyMoveEffects:
            for ef in self.flyMoveEffects:
                if ef:
                    ef.stop()

            self.flyMoveEffects = []
        if self.flyDashEffects:
            for ef in self.flyDashEffects:
                if ef:
                    ef.stop()

            self.flyDashEffects = []
        self.releaseWingHorseIdleEffect()

    def getHorseMoveEffect(self):
        itemId = self.bianshen[1]
        if not itemId:
            return None
        else:
            return HWED.data.get(itemId, {}).get('horseMoveEffect', [])

    def getHoseDashEffect(self):
        itemId = self.bianshen[1]
        if not itemId:
            return None
        else:
            return HWED.data.get(itemId, {}).get('horseDashEffect', [])

    def getFlyMoveEffect(self, itemId):
        if not itemId:
            return None
        else:
            effs = list(HWED.data.get(itemId, {}).get('flyMoveEffect', []))
            aspect = self.realAspect
            enhLv = aspect.wingFlyEnhLv()
            if enhLv:
                effs = list(HWED.data.get(itemId, {}).get('flyMoveEffect' + str(enhLv), effs))
            if self == BigWorld.player():
                if self.ap.forwardMagnitude:
                    forwardStartEffs = HWED.data.get(itemId, {}).get('flyMoveForwardStartEffect', [])
                    if forwardStartEffs:
                        effs.extend(forwardStartEffs)
                else:
                    startEffs = HWED.data.get(itemId, {}).get('flyMoveStartEffect', [])
                    if startEffs:
                        effs.extend(startEffs)
            else:
                startEffs = HWED.data.get(itemId, {}).get('flyMoveStartEffect', [])
                if startEffs:
                    effs.extend(startEffs)
            return effs

    def getFlyDashEffect(self, itemId):
        if not itemId:
            return None
        else:
            aspect = self.realAspect
            enhLv = aspect.wingFlyEnhLv()
            effs = HWED.data.get(itemId, {}).get('flyDashEffect', [])
            if enhLv:
                effs = HWED.data.get(itemId, {}).get('flyDashEffect' + str(enhLv), effs)
            return effs

    def playHorseWingMoveEffect(self, model, effs):
        if not model or not effs:
            return
        effLv = self.getBasicEffectLv()
        priority = self.getBasicEffectPriority()
        retEffs = []
        for ef in effs:
            efs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, [effLv,
             priority,
             model,
             ef,
             sfx.EFFECT_UNLIMIT])
            if efs:
                retEffs.extend(efs)

        return retEffs

    def refreshHorseWingEffect(self, verticale = False):
        self.releaseHorseWingEffect(verticale)
        isInHorse = self.inRiding() and self.bianshen[0] == gametypes.BIANSHEN_RIDING_RB
        self.refreshWingHorseIdleEffect(isInHorse)
        if isInHorse or self.inFly:
            if self.qinggongState == gametypes.QINGGONG_STATE_MOUNT_DASH:
                if not verticale:
                    effs = self.getHoseDashEffect()
                    self.horseDashEffects = self.playHorseWingMoveEffect(self.model, effs)
            elif self.qinggongState in gametypes.QINGGONG_WINGFLY_STATES:
                if self.inFlyTypeFlyRide():
                    itemId = self.bianshen[1]
                    effs = self.getFlyDashEffect(itemId)
                    self.flyDashEffects = self.playHorseWingMoveEffect(self.model, effs)
                elif self.inFlyTypeFlyZaiju():
                    itemId = self.bianshen[1]
                    effs = self.getFlyDashEffect(itemId)
                    self.flyDashEffects = self.playHorseWingMoveEffect(self.model, effs)
                else:
                    itemId = self.modelServer.wingFlyModel.key
                    effs = self.getFlyDashEffect(itemId)
                    self.flyDashEffects = self.playHorseWingMoveEffect(self.modelServer.wingFlyModel.model, effs)
            elif self.inMoving() or getattr(self, 'isVerticalMoving', False):
                if isInHorse:
                    if self.inFlyTypeFlyRide():
                        itemId = self.bianshen[1]
                        effs = self.getFlyMoveEffect(itemId)
                    else:
                        effs = self.getHorseMoveEffect()
                    self.horseGroundMoveEffects = self.playHorseWingMoveEffect(self.model, effs)
                elif self.inFlyTypeFlyZaiju():
                    itemId = self.bianshen[1]
                    effs = self.getFlyMoveEffect(itemId)
                    self.flyMoveEffects = self.playHorseWingMoveEffect(self.model, effs)
                elif self.inFlyTypeWing():
                    itemId = self.modelServer.wingFlyModel.key
                    effs = self.getFlyMoveEffect(itemId)
                    self.flyMoveEffects = self.playHorseWingMoveEffect(self.modelServer.wingFlyModel.model, effs)

    def refreshWingHorseIdleEffect(self, isInHorse = None):
        if not getattr(self, 'modelServer', None):
            return
        else:
            if not isInHorse:
                isInHorse = self.inRiding() and self.bianshen[0] == gametypes.BIANSHEN_RIDING_RB
            self.releaseWingHorseIdleEffect()
            if not self.inMoving() and self.qinggongState == gametypes.QINGGONG_STATE_DEFAULT:
                effs = []
                if isInHorse:
                    if self.inFly:
                        effs = self.getHorseFlyIdleEffect()
                    else:
                        effs = self.getHorseGroundIdleEffect()
                elif self.inFlyTypeWing():
                    effs = self.getWingFlyIdleEffect()
                self.wingHorseIdleEffect = self.playHorseWingIdleEffect(self.model, effs)
            return

    def releaseWingHorseIdleEffect(self):
        if self.wingHorseIdleEffect:
            for effId, fx in self.wingHorseIdleEffect.iteritems():
                sfx.detachEffect(self.model, effId, fx)

            self.wingHorseIdleEffect = {}

    def playHorseWingIdleEffect(self, model, effs):
        if not model or not effs:
            return
        effLv = self.getBasicEffectLv()
        priority = self.getBasicEffectPriority()
        retEffs = {}
        for ef in effs:
            efs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, [effLv,
             priority,
             model,
             ef,
             sfx.EFFECT_UNLIMIT])
            if efs:
                retEffs[ef] = efs

        return retEffs

    def getHorseFlyIdleEffect(self):
        itemId = self.bianshen[1]
        effs = HWED.data.get(itemId, {}).get('horseFlyIdleEffect', [])
        return effs

    def getHorseGroundIdleEffect(self):
        itemId = self.bianshen[1]
        effs = HWED.data.get(itemId, {}).get('horseGroundIdleEffect', [])
        return effs

    def getWingFlyIdleEffect(self):
        itemId = self.modelServer.wingFlyModel.key
        effs = HWED.data.get(itemId, {}).get('wingFlyIdleEffect', [])
        return effs

    def checkAvatarRange(self, tgt, enter = True):
        if self.friend and getattr(tgt, 'gbId', 0) == self.friend.intimacyTgt:
            self.intimacyTgtEnter = enter
            self.intimacyTgtId = getattr(tgt, 'id', None)
            if enter:
                delayTime = SCD.data.get('INTIMACY_INTERACTIVE_DELAY_TIME', 2)
                BigWorld.callback(delayTime, Functor(self._checkAvatarRange, tgt.id))
            else:
                self.cell.checkIntimacyTgt(tgt.id, False)

    def _checkAvatarRange(self, tgtId):
        if self.intimacyTgtEnter:
            self.cell.checkIntimacyTgt(tgtId, self.intimacyTgtEnter)

    def releaseIntimacyInterEffects(self):
        if self.intimacyInterEffects:
            try:
                for fx in self.intimacyInterEffects:
                    if fx:
                        fx.stop()

            except:
                pass

            self.intimacyInterEffects = []

    def playIntimacyInterEffects(self):
        self.releaseIntimacyInterEffects()
        fxId = SCD.data.get('INTIMACY_INTERACTIVE_EFFECT', 630021)
        fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getEquipEffectLv(),
         self.getEquipEffectPriority(),
         self.model,
         fxId,
         sfx.EFFECT_LIMIT_MISC))
        if fxs:
            self.intimacyInterEffects.extend(fxs)

    def notifyIntimacyTgt(self, tgtId, enter):
        tgt = BigWorld.entity(tgtId)
        if not tgt or not tgt.inWorld:
            return
        if enter:
            self.playIntimacyInterEffects()
            tgt.playIntimacyInterEffects()
        else:
            self.releaseIntimacyInterEffects()
            tgt.releaseIntimacyInterEffects()

    def getCameraFloatageHeight(self):
        floatage = 0
        if getattr(self.model, 'floatage', None):
            floatage = getattr(self.model.floatage, 'floatHeight', 0)
        if self.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            horsewingCameraId = ED.data.get(self.bianshen[1], {}).get('horsewingCameraId', None)
            horsewingCameraData = HCD.data.get(horsewingCameraId, {})
            floatOffset = horsewingCameraData.get('floatOffset', 0)
            if floatOffset:
                floatage = floatage + floatOffset
        return floatage

    def rideWingBagSlotEnlarge(self, page, pos):
        pass

    def needHideTopLogoName(self):
        try:
            p = BigWorld.player()
            if self == BigWorld.player():
                if not int(p.operation['commonSetting'][2]):
                    return True
            elif not int(p.operation['commonSetting'][5]):
                return True
            if hasattr(self, 'isRidingTogether') and self.isRidingTogether():
                main = self.tride.getHeader() if self.tride else self
                noViceTopLogo = ED.data.get(main.bianshen[1], {}).get('noViceTopLogo', False)
                if noViceTopLogo and self != main:
                    return True
            if self.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
                zjData = ZJD.data.get(self.bianshen[1], {})
                if zjData.get('hideName', 0):
                    return True
            if getattr(self, 'wingWorldCarrier', None):
                return True
            if hasattr(p, 'isBianShenZaiJuInPUBG') and p.isBianShenZaiJuInPUBG(self):
                return True
        except:
            pass

        return False

    def alwaysShowModel(self):
        if self.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            ed = ED.data.get(self.bianshen[1], {})
            return ed.get('alwaysShowModel', False)
        if self.tride:
            main = self.tride.getHeader()
            if main and hasattr(main, 'bianshen'):
                return ED.data.get(main.bianshen[1], {}).get('alwaysShowModel', False)
        return False

    def needHideTopLogoTitle(self):
        try:
            p = BigWorld.player()
            if self == BigWorld.player():
                if not AppSettings[keys.SET_HIDE_PLAYER_TITLE]:
                    return True
            elif not AppSettings[keys.SET_HIDE_AVATAR_TITLE]:
                return True
            if gameglobal.rds.ui.battleOfFortProgressBar.checkBattleFortNewFlag():
                return True
            if hasattr(p, 'isBianShenZaiJuInPUBG') and p.isBianShenZaiJuInPUBG(self):
                return True
            if hasattr(self, 'isRidingTogether') and self.isRidingTogether():
                main = self.tride.getHeader() if self.tride else self
                noViceTopLogo = ED.data.get(main.bianshen[1], {}).get('noViceTopLogo', False)
                if noViceTopLogo and self != main:
                    return True
            if self._isSchoolSwitch() and self.schoolSwitchName != self.realRoleName:
                return True
            if self.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
                zjData = ZJD.data.get(self.bianshen[1], {})
                if zjData.get('hideName', 0):
                    return True
            if self.isOnWingWorldCarrier():
                return True
        except:
            pass

        return False

    def needHideTopLogoGuildIcon(self):
        p = BigWorld.player()
        if self == p:
            if not AppSettings[keys.SET_HIDE_PLAYER_GUILD]:
                return True
        elif not AppSettings[keys.SET_HIDE_AVATAR_GUILD]:
            return True
        if gameglobal.rds.ui.battleOfFortProgressBar.checkBattleFortNewFlag():
            return True
        if hasattr(p, 'isBianShenZaiJuInPUBG') and p.isBianShenZaiJuInPUBG(self):
            return True
        anonymousType = p.anonymNameMgr.checkNeedAnonymity(entity=self)
        if anonymousType != gametypes.AnonymousType_None:
            if p.anonymNameMgr.getAnonymousData(anonymousType, gametypes.ANONYMOUS_GUILD_IMAGE_HIDE, False):
                return True
        return False

    def needHideTopLogoTitleEffect(self):
        p = BigWorld.player()
        if hasattr(p, 'isBianShenZaiJuInPUBG') and p.isBianShenZaiJuInPUBG(self):
            return True
        anonymousType = p.anonymNameMgr.checkNeedAnonymity(entity=self)
        if anonymousType != gametypes.AnonymousType_None:
            if p.anonymNameMgr.getAnonymousData(anonymousType, gametypes.ANONYMOUS_TOP_TITLE_EFFECT_HIDE, False):
                return True
        return False

    def refreshTopLogoName(self):
        self.refreshTopLogo()
        p = BigWorld.player()
        if p == self:
            gHideName = gameglobal.gHidePlayerName
            gHideTitle = gameglobal.gHidePlayerTitle
            gHideIcon = gameglobal.gHidePlayerGuild
        else:
            gHideName = gameglobal.gHideAvatarName
            gHideTitle = gameglobal.gHideAvatarTitle
            gHideIcon = gameglobal.gHideAvatarGuild
        needHideTopLogoName = self.needHideTopLogoName() or gHideName
        if self.topLogo:
            self.topLogo.hideName(needHideTopLogoName)
        needHideTopLogoTitle = self.needHideTopLogoTitle() or gHideTitle
        if self.topLogo:
            self.topLogo.hideAvatarTitle(needHideTopLogoTitle)
        needHideTopLogoGuildIcon = self.needHideTopLogoGuildIcon() or gHideIcon
        if self.topLogo:
            if self.guildFlag:
                self.topLogo.addGuildIcon(self.guildFlag)
            self.topLogo.hideGuildIcon(needHideTopLogoGuildIcon)
        needHideTopLogoTitleEffect = self.needHideTopLogoTitleEffect()
        if self.topLogo:
            self.topLogo.hideTitleEffect(needHideTopLogoTitleEffect)

    def onUnsummonPet(self, petCharType):
        if self == BigWorld.player():
            pet = self._getPet()
            if not pet:
                gameglobal.rds.ui.beastActionBar.hide()

    def onSummonPetSucc(self, beastEntId):
        pass

    def onUsePetSkillAfterMove(self, skillId):
        petSkillData = PSD.data.get(skillId, {})
        avatarAction = petSkillData.get('avatarAction')
        avatarEffect = petSkillData.get('avatarEffect')
        playSeq = []
        playSeq.append((avatarAction,
         avatarEffect,
         action.PET_ACTION,
         0,
         1.0,
         None))
        self.fashion.playActionWithFx(playSeq, action.PET_ACTION, None, 0, 0, 0, priority=self.getSkillEffectPriority())

    def _getPet(self, beastCharType = 0):
        beasts = []
        for pType, petList in self.summonedPets.iteritems():
            if beastCharType and pType != beastCharType:
                continue
            for entId, summonTime in petList:
                sb = BigWorld.entities.get(entId)
                if sb == None:
                    continue
                if sb.ownerId == self.id:
                    beasts.append(sb)

        if beasts:
            return beasts[0]
        else:
            return

    def inInteractiveObj(self):
        return self.interactiveObjectEntId

    def getInteractiveObj(self):
        if self.inInteractiveObj():
            return BigWorld.entities.get(self.interactiveObjectEntId)

    def showShaXingWaitMsgBox(self):
        pass

    def showChooseGroupFailMsgBox(self):
        pass

    def updateSprintStart(self):
        if self.sprintStartCB:
            BigWorld.cancelCallback(self.sprintStartCB)
        sprintStartCBTime = SCD.data.get('sprintStartCBTime', 1.5)
        self.sprintSpeeding = True
        self.sprintStartCB = BigWorld.callback(sprintStartCBTime, self.sprintSpeedingOver)

    def sprintSpeedingOver(self):
        self.sprintSpeeding = False
        self.sprintStartCB = None

    def breakForceMovement(self):
        if hasattr(self.model, 'beholded') and self.model.beholded:
            self.model.beholded = False
            self.updateModelFreeze(-1.0)
        if self == BigWorld.player():
            ap = self.ap
            if not ap.forceSeek:
                return
            ap._endForceMove(1)
            ap.setSpeed(self.speed[gametypes.SPEED_MOVE] / 60.0)
            flyEffect.setMoveControl(self, False)
            if getattr(self, 'castSkillBusy', None):
                self.castSkillBusy = False
            self.updateActionKeyState()
            self.isAscending = False
        else:
            self.am.moveNotifier = self.fashion.movingNotifier
            if self.IsAvatar and hasattr(self, 'fashion'):
                self.fashion.stopAction()

    def resetPhysicsModel(self):
        if self != BigWorld.player():
            return
        if self.bianshen[0] == gametypes.BIANSHEN_ZAIJU and not getattr(self, 'isPathfinding', False):
            zjData = ZJD.data.get(self.bianshen[1], {})
            self.physics.modelWidth = zjData.get('modelWidth', gameglobal.PHYSICS_MODEL_WIDTH)
            self.physics.modelDepth = zjData.get('modelDepth', gameglobal.PHYSICS_MODEL_DEPTH)
            self.physics.modelHeight = zjData.get('modelHeight', gameglobal.PHYSICS_MODEL_HEIGHT)
        elif self.isOnWingWorldCarrier() and self.wingWorldCarrier.get(self.id) == const.WING_WORLD_CARRIER_MAJOR_IDX:
            carrierNo = self.wingWorldCarrier.carrierNo
            data = WWCD.data.get(carrierNo, {})
            collideWidth = data.get('collideWidth', gameglobal.PHYSICS_MODEL_WIDTH)
            collideHeight = data.get('collideHeight', gameglobal.PHYSICS_MODEL_HEIGHT)
            collideDepth = data.get('collideDepth', gameglobal.PHYSICS_MODEL_DEPTH)
            self.physics.modelWidth = collideWidth
            self.physics.modelDepth = collideDepth
            self.physics.modelHeight = collideHeight
        else:
            self.physics.modelWidth = gameglobal.PHYSICS_MODEL_WIDTH
            self.physics.modelDepth = gameglobal.PHYSICS_MODEL_DEPTH
            self.physics.modelHeight = gameglobal.PHYSICS_MODEL_HEIGHT

    def clearAvatarDanDaoCancelCB(self):
        if self.avatarDanDaoCancelCB:
            BigWorld.cancelCallback(self.avatarDanDaoCancelCB)
            self.avatarDanDaoCancelCB = None

    def getIdByCarrierIdx(self, idx):
        for k, v in self.carrier.iteritems():
            if v == idx:
                return k

        return 0

    def isOnCarrier(self):
        return self.carrier.has_key(self.id)

    def isCarrierRunning(self):
        return self.carrier.carrierState == gametypes.MULTI_CARRIER_STATE_RUNNING

    def isCarrierReady(self):
        return self.carrier.carrierState == gametypes.MULTI_CARRIER_STATE_CHECK_READY

    def isInSSCorTeamSSC(self):
        return self.inFubenType(const.FB_TYPE_SHENGSICHANG) or self.inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG)

    def onTeleport(self, spaceID, pos):
        if clientcom.bfDotaAoIInfinity():
            self.setFilterSmooth(True)
            if self.filter:
                self.filter.reset(1)
            teleportCallback = getattr(self, 'teleportCallback', None)
            if teleportCallback:
                BigWorld.cancelCallback(teleportCallback)
                self.teleportCallback = None
            self.teleportCallback = BigWorld.callback(gameglobal.NOTIFY_TELEPORT_TIME, Functor(self.setFilterSmooth, False))

    def setFilterSmooth(self, value):
        if self.filter:
            self.filter.disableSmooth = value

    def isOnWingWorldCarrier(self):
        return self.wingWorldCarrier.has_key(self.id)
