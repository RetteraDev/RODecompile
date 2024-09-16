#Embedded file name: /WORKSPACE/data/entities/client/npc.o
import inspect
import BigWorld
import Sound
import copy
import commNpcFavor
import const
import npcConst
import gameglobal
import commcalc
import gamelog
import gametypes
import formula
import utils
import clientcom
import appSetting
import gameconfigCommon
from helpers import fashion
from helpers import scenario
from iNpc import INpc
from iDisplay import IDisplay
from sfx import sfx
from helpers import modelRobber
from callbackHelper import Functor
from helpers import tintalt as TA
from helpers import charRes
from helpers import tintalt
from guis import uiUtils
from random import choice
from helpers import modelServer
from impl.impNpcQuest import ImpNpcQuest
from impl.impNpcQuestMarker import ImpNpcQuestMarker
from impl.impNpcFubenAI import ImpNpcFubenAI
from impl.impNpcShop import ImpNpcShop
from impl.impPot import ImpPot
from impl.impNpcCompositeShop import ImpNpcCompositeShop
from impl.impNpcBusiness import ImpNpcBusiness
from impl import impPot
from impl.impNpcBusinessSpy import ImpNpcBusinessSpy
from impl.impNpcPuzzle import ImpNpcPuzzle
from impl.impNpcContract import ImpNpcContract
from impl.impNpcItemCommit import ImpNpcItemCommit
from impl.impNpcShaxing import ImpNpcShaxing
from impl.impNpcGuild import ImpNpcGuild
from impl.impNpcGuildRobber import ImpNpcGuildRobber
from impl.impNpcWorldWar import ImpNpcWorldWar
from impl.impPairPuzzle import ImpPairPuzzle
from data import fight_for_love_config_data as FFLCD
from data import dialogs_data as DD
from data import npc_data as ND
from data import npc_model_client_data as NMCD
from data import quest_marker_data as QMD
from data import sys_config_data as SCD
from data import quest_data as QD
from cdata import game_msg_def_data as GMDD
from cdata import teleport_data as TD
from data import wmd_config_data as WCD
from cdata import npc_limit_data as NLD
from cdata import qiren_clue_reverse_data as QCRD
from data import qiren_clue_data as QCD
from data import home_data as HD
from data import item_data as ID
from cdata import quest_npc_relation as QNR
from data import dawdler_data as DRD
from guis import ui
from data import nf_npc_data as NND
from cdata import double_plant_tree_config_data as DPTCD

class NpcClientMeta(type):

    def __init__(cls, name, bases, dic):
        super(NpcClientMeta, cls).__init__(name, bases, dic)
        inherits = (ImpNpcQuest,
         ImpNpcFubenAI,
         ImpNpcShop,
         ImpNpcCompositeShop,
         ImpNpcQuestMarker,
         ImpNpcBusiness,
         ImpNpcBusinessSpy,
         ImpNpcPuzzle,
         ImpNpcContract,
         ImpNpcItemCommit,
         ImpNpcShaxing,
         ImpNpcGuild,
         ImpNpcGuildRobber,
         ImpNpcWorldWar,
         ImpPairPuzzle)
        for inherit in inherits:
            for name, fun in inspect.getmembers(inherit, inspect.ismethod):
                if not getattr(cls, name, None):
                    setattr(cls, name, fun.im_func)

            for name, memb in inspect.getmembers(inherit):
                if name == '__module__':
                    continue
                if memb.__class__.__name__ in const.BUILTIN_OBJS:
                    setattr(cls, name, memb)


class Npc(INpc, IDisplay, ImpPot):
    __metaclass__ = NpcClientMeta

    def __init__(self):
        super(Npc, self).__init__()
        self.noSelected = False
        self.inScenario = False
        self.trapId = None
        self.trapChatId = None
        self.mhp = 10000
        self.hp = 10000
        self.mp = 10000
        self.mmp = 10000
        self.npcHasFunc = None
        self.awardInfo = {}
        self.validInBianyao = ND.data.get(self.npcId, {}).get('validInBianyao', gametypes.FUNCTION_INVALID_FOR_YAO)
        self.refreshOnTimerHandle = None
        self.npcFunctions = {}

    def prerequisites(self):
        return []

    @property
    def realAspect(self):
        return self.aspect

    @property
    def realPhysique(self):
        return self.physique

    @property
    def realAvatarConfig(self):
        return self.avatarConfig

    @property
    def realSchool(self):
        return self.physique.school

    def isShowFashion(self):
        return not not commcalc.getSingleBit(self.signal, gametypes.SIGNAL_SHOW_FASHION)

    def isShowFashionWeapon(self):
        return not not commcalc.getSingleBit(self.signal, gametypes.SIGNAL_SHOW_FASHION_WEAPON)

    def getWeapon(self, isLeft):
        if self.isShowFashionWeapon():
            if isLeft:
                if self.realAspect.leftFashionWeapon:
                    return self.realAspect.leftFashionWeapon
                return self.realAspect.leftWeapon
            elif self.realAspect.rightFashionWeapon:
                return self.realAspect.rightFashionWeapon
            else:
                return self.realAspect.rightWeapon
        if isLeft:
            return self.realAspect.leftWeapon
        return self.realAspect.rightWeapon

    def getWeaponEnhLv(self, isLeft):
        if self.isShowFashionWeapon():
            if isLeft:
                if self.realAspect.leftFashionWeapon:
                    return self.realAspect.leftFashionWeaponEnhLv()
                return self.realAspect.leftWeaponEnhLv()
            elif self.realAspect.rightFashionWeapon:
                return self.realAspect.rightFashionWeaponEnhLv()
            else:
                return self.realAspect.rightWeaponEnhLv()
        if isLeft:
            return self.realAspect.leftWeaponEnhLv()
        return self.realAspect.rightWeaponEnhLv()

    def weaponInHandState(self):
        weaponState = self.getItemData().get('weaponState', gametypes.WEAPON_HANDFREE)
        return weaponState

    def afterWeaponUpdate(self, weapon):
        if not self.inWorld:
            return
        if self.getItemData().get('extraTint', None):
            models = weapon.getModels()
            tint = self.getItemData()['extraTint']
            TA.ta_add(models, tint)

    def afterWearUpdate(self, wear):
        pass

    def isUseAvatarModelServer(self):
        data = self.getItemData()
        modelId = data.get('model', 0)
        if data.get('useAvatarModelServer', 0) and modelId > const.MODEL_AVATAR_BORDER:
            return True
        return False

    def enterWorld(self):
        if self.isScenario in (gameglobal.NORMAL_NPC, gameglobal.SCENARIO_EDIT_NPC):
            if self.isUseAvatarModelServer():
                data = self.getItemData()
                modelId = data.get('model', 0)
                self.avatarInfo = clientcom.ConfigCache.getConfig('%s/%d.xml' % (gameglobal.AVATAR_TEMPLATE_PATH, modelId))
                wingId = data.get('wingId', 0)
                rideId = data.get('rideId', 0)
                rightWeapon = data.get('rightWeapon', 0)
                leftWeapon = data.get('leftWeapon', 0)
                self.realAspect.wingFly = wingId
                self.realAspect.ride = rideId
                self.realAspect.rightWeapon = rightWeapon
                self.realAspect.leftWeapon = leftWeapon
                weaponId = rightWeapon if rightWeapon else leftWeapon
                schReq = ID.data.get(weaponId, {}).get('schReq', (0,))
                self.realPhysique.school = schReq[0]
            super(Npc, self).enterWorld()
            data = self.getItemData()
            modelId = data.get('model', 0)
            if modelId > const.MODEL_AVATAR_BORDER:
                avatarInfo = clientcom.ConfigCache.getConfig('%s/%d.xml' % (gameglobal.AVATAR_TEMPLATE_PATH, modelId))
                if avatarInfo and not self.realPhysique.bodyType:
                    self.realPhysique.bodyType = avatarInfo.get('bodyType', 0)
                    self.realPhysique.sex = avatarInfo.get('sex', 0)
                    self.realPhysique.source = modelId
        else:
            gamelog.debug('@szh: enterWorld', self.id)
            self.fashion = fashion.Fashion(self.id)
            self.fashion.loadDummyModel()
            if self.filterType == gametypes.NPC_FILTER_TYPE_AVATARDROP:
                self.filter = BigWorld.AvatarDropFilter()
            else:
                self.filter = BigWorld.DumbFilter()
        self.initYaw = self.yaw
        if self.isScenario != gameglobal.NORMAL_NPC:
            self.afterModelFinish()
        if self._isPickNpc():
            npcDialogLength = NMCD.data.get(self.npcId, {}).get('npcDialogLength', SCD.data.get('npcDialogLength', 4) + ND.data.get(self.npcId, {}).get('bodysize', 0))
            self.trapId = BigWorld.addPot(self.matrix, npcDialogLength, self.trapCallback)
            self.addTrapEvent()
        if self._isMarkerNpc():
            self.initQuestMarker()
        if self._isBusinessNpc():
            self.initBusiness()
        if self._isQuestNpc():
            self.trapChatId = BigWorld.addPot(self.matrix, SCD.data.get('questCompleteNpcTriggerChatDistance', 10), self.trapChatCallback)

    def _trySitInChair(self):
        if not self.inWorld:
            return
        ge = BigWorld.player()._getGuildEntity(self.attachedGuildSeId)
        if not ge or not ge.ownerModels:
            BigWorld.callback(1, Functor(self._trySitInChair))
            return
        self.modelServer.sitInChair(ge.ownerModels[0])
        self.fashion.playActionSequence(self.modelServer.bodyModel, const.GUILD_RESTAURANT_NPC_SIT_ACTIONS, None, keep=1)

    def leaveWorld(self):
        if self.attachedGuildSeId:
            ge = BigWorld.player()._getGuildEntity(self.attachedGuildSeId)
            if ge and ge.ownerModels:
                self.modelServer.leaveChair(ge.ownerModels[0])
        if ui.entityClicked == self:
            if gameglobal.rds.ui.npcPanel.inFullScreen:
                gameglobal.rds.ui.npcPanel.hideNpcFullScreen()
            elif gameglobal.rds.ui.shop.mediator:
                gameglobal.rds.ui.shop.hide()
            elif gameglobal.rds.ui.quest.isShow:
                gameglobal.rds.ui.quest.close()
            elif gameglobal.rds.ui.npcV2.isShow:
                gameglobal.rds.ui.npcV2.leaveStage()
            elif gameglobal.rds.ui.trainingArea.isShow:
                gameglobal.rds.ui.trainingArea.onLeaveTrain(None)
            elif gameglobal.rds.ui.trainingAreaAward.isShow:
                gameglobal.rds.ui.trainingAreaAward.hide(True)
            elif gameglobal.rds.ui.dyePlane.med:
                gameglobal.rds.ui.dyePlane.hide()
        self.npcTrapCallback(True)
        for trapLengthType in xrange(1, impPot.TRAP_MAX_NUM):
            trapEventIdName = 'trapEventId'
            if trapLengthType != 1:
                trapEventIdName = trapEventIdName + str(trapLengthType)
            if hasattr(self, trapEventIdName):
                if getattr(self, trapEventIdName):
                    self.dealTrapOutEvent(trapLengthType)

        super(Npc, self).leaveWorld()
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None
        if self.trapChatId != None:
            BigWorld.delPot(self.trapChatId)
            self.trapChatId = None
        self.delTrapEvent()
        if self.refreshOnTimerHandle:
            BigWorld.cancelCallback(self.refreshOnTimerHandle)
            self.refreshOnTimerHandle = None
        if self._isQuestNpc() and hasattr(self, 'questTopLogoTimer'):
            BigWorld.cancelCallback(self.questTopLogoTimer)
        modelRobber.getInstance().removeRobInfoByNpc(self.id)
        self.delLingShiExtraTint()

    def afterModelFinish(self):
        super(Npc, self).afterModelFinish()
        if NMCD.data.get(self.npcId, {}).get('collideRadius', False):
            self.collideWithPlayer = True
        self.refreshOpacityOnTimer()
        if self.yaw != self.initYaw:
            gamelog.debug('JJH yaw changed ', self.id, self.yaw, self.initYaw)
        if self.isScenario in (gameglobal.SCENARIO_PLAY_NPC, gameglobal.SCENARIO_EDIT_NPC):
            self.filter = BigWorld.ClientFilter()
        elif self.filterType == gametypes.NPC_FILTER_TYPE_AVATARDROP:
            self.filter = BigWorld.AvatarDropFilter()
        else:
            self.filter = BigWorld.DumbFilter()
            self.filter.clientYawMinDist = 0.0
            self.filter.setYaw(self.initYaw)
        if self.isScenario == gameglobal.SCENARIO_PLAY_NPC or not ND.data.get(self.npcId, {}).get('canselect', 1):
            self.setTargetCapsUse(False)
            self.noSelected = True
        if hasattr(self.modelServer, 'avatarConfig') and self.modelServer.avatarConfig:
            self.setAvatarConfig(self.modelServer.avatarConfig.get('avatarConfig', ''))
        elif self.isMultiModel:
            self.setAvatarConfig(self.avatarConfig)
            act = self.getSchoolIdleAct()
            self.fashion.playActionSequence(self.model, [act], None)
        if self.getItemData().get('extraTint', None):
            tint = self.getItemData()['extraTint']
            TA.ta_add(self.allModels, tint)
        self._addTriggerEff()
        if self._isQuestNpc():
            self.questTopLogoRefresh()
        if self.attachedGuildSeId:
            self._trySitInChair()
        self.updateTopFadeDist()
        floatHeight = self.getItemData().get('floatHeight', 0)
        if self.inFlyTypeWing() and floatHeight:
            floatage = BigWorld.PyPoseControl()
            self.model.floatage = floatage
            floatage.floatHeight = floatHeight
        torchIdx = getattr(self, 'torchIdx', -1)
        p = BigWorld.player()
        if torchIdx and p and getattr(p, 'guild', None) and p.guild.bonfire.isTorchOn(torchIdx):
            gameglobal.rds.ui.guildBonfire.lightBonfireSucc(torchIdx)
        self.addLingShiExtraTint()

    def setRongGuang(self, needXuanren = False):
        if not self.isRealModel:
            return
        rongGuang = charRes.RongGuangRes()
        rongGuang.queryByAvatar(self)
        rongGuang.apply(self.modelServer.bodyModel, needXuanren)

    def updateTopFadeDist(self):
        if self.topLogo:
            if getattr(self, 'npcId', None):
                if NMCD.data.get(self.npcId, {}).has_key('topDist'):
                    topDist = NMCD.data.get(self.npcId, {})['topDist']
                    if self.topLogo.gui:
                        self.topLogo.gui.fadeStart = topDist[0]
                        self.topLogo.gui.fadeEnd = topDist[1]
                    if self.topLogo.guiAni:
                        self.topLogo.guiAni.fadeStart = topDist[0]
                        self.topLogo.guiAni.fadeEnd = topDist[1]

    def getSchoolIdleAct(self):
        schoolIdleAct = self.getItemData().get('schoolIdleAct', {})
        idleAct = self.getItemData().get('idleAct')
        return schoolIdleAct.get(self.realSchool, idleAct)

    def _addTriggerEff(self):
        p = BigWorld.player()
        nmcd = NMCD.data.get(self.npcId, {})
        if gameglobal.GM_NPC_HIGHLIGHT_ALL:
            clientcom.highlightEntity(self, True)
        if nmcd.get('triggerEff') in self.attachFx:
            return
        if p and p.quests and nmcd and nmcd.has_key('triggerEff'):
            for questId in p.quests:
                if p.getQuestData(questId, const.QD_FAIL, False):
                    continue
                effScale = nmcd['effScale'] if nmcd.has_key('effScale') else nmcd.get('modelScale', 1)
                markerInfo, _ = p.getQuestData(questId, const.QD_QUEST_MARKER, ({}, None))
                chaterInfo = p.getQuestData(questId, const.QD_QUEST_CHAT, {})
                isTriggered = markerInfo and markerInfo.get(self.npcId, 1) > 0
                isChatTriggered = chaterInfo and chaterInfo.get(self.npcId, 1) > 0
                gamelog.debug('zt: Npc.afterModelFinish', questId, self.npcId, markerInfo, isTriggered)
                if chaterInfo.has_key(self.npcId):
                    if isChatTriggered:
                        continue
                elif isTriggered:
                    continue
                qmd = QMD.data.get(self.npcId, {})
                needUseItems = False
                if qmd.has_key('useItems'):
                    useItems = qmd['useItems']
                    for itemId, cnt in useItems:
                        amount = p.questBag.countItemInPages(itemId)
                        if amount < cnt:
                            needUseItems = True
                            break

                if needUseItems:
                    continue
                needGainItems = False
                if qmd.has_key('itemGain'):
                    useItems = qmd['itemGain']
                    for itemId, cnt in useItems:
                        amount = p.questBag.countItemInPages(itemId)
                        if amount >= cnt:
                            needGainItems = True
                            break

                if needGainItems:
                    continue
                isDebated = p.getQuestData(questId, const.QD_QUEST_DEBATE, False)
                if self.npcId in markerInfo.keys() or self.npcId in chaterInfo.keys() or p._needJobStats(questId, gametypes.JOB_STATS_QUESTMARKER, self.npcId) or questId in QMD.data.get(self.npcId, {}).get('needAcceptQuests', []) or not isDebated and self._isDebateNpc(questId):
                    if nmcd['triggerEff'] not in self.attachFx:
                        fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getEquipEffectLv(),
                         self.getEquipEffectPriority(),
                         self.model,
                         nmcd['triggerEff'],
                         sfx.EFFECT_UNLIMIT))
                        if fxs:
                            for fx in fxs:
                                fx.scale(effScale, effScale, effScale)

                            self.addFx(nmcd['triggerEff'], fxs)
                self._addFunNpcPlayFx(questId)

        if self._isCommonMarkerNpc():
            self._addNormalTriggerEff()
        if self._isRunManNpc() and nmcd.get('triggerEff') and p.runMan.isMarkerActive(self.npcId):
            self._addNormalTriggerEff()

    def _addNormalTriggerEff(self):
        nmcd = NMCD.data.get(self.npcId, {})
        effectId = nmcd.get('triggerEff', 0)
        if not effectId or self.attachFx.has_key(effectId):
            return
        effScale = nmcd['effScale'] if nmcd.has_key('effScale') else nmcd.get('modelScale', 1)
        fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getEquipEffectLv(),
         self.getEquipEffectPriority(),
         self.model,
         nmcd['triggerEff'],
         sfx.EFFECT_UNLIMIT))
        if fxs:
            for fx in fxs:
                fx.scale(effScale, effScale, effScale)

            self.addFx(effectId, fxs)

    def _addFunNpcPlayFx(self, questId):
        p = BigWorld.player()
        monsterInfo = p.getQuestData(questId, const.QD_MONSTER_KILL, {})
        if not monsterInfo:
            return
        for mType in monsterInfo:
            killNum = monsterInfo.get(mType, 0)
            if not killNum:
                funNpcInfo = p.getQuestData(questId, const.QD_QUEST_QIECUO, {})
                if mType in funNpcInfo:
                    npcId = funNpcInfo[mType]
                    if npcId and npcId == self.npcId:
                        self._addNormalTriggerEff()

    def _isDebateNpc(self, questId):
        qd = QD.data.get(questId, {})
        return self.npcId == qd.get('debateNpc', 0)

    def isFuncNpc(self, npcFunc):
        if not self.npcFunctions:
            npcData = ND.data.get(self.npcId, {})
            functions = npcData.get('functions', [])
            self.npcFunctions = {func[1]:func[2] for func in functions}
        return self.npcFunctions.has_key(npcFunc)

    def _isQuestNpc(self):
        if self.isScenario == gameglobal.SCENARIO_PLAY_NPC:
            return False
        return self.isFuncNpc(npcConst.NPC_FUNC_QUEST)

    def _isPuzzleNpc(self):
        if self.isScenario == gameglobal.SCENARIO_PLAY_NPC:
            return False
        return self.isFuncNpc(npcConst.NPC_FUNC_PUZZLE)

    def _isMarkerNpc(self):
        if self.isScenario == gameglobal.SCENARIO_PLAY_NPC:
            return False
        return self.isFuncNpc(npcConst.NPC_FUNC_MARKER)

    def _isBusinessNpc(self):
        if self.isScenario == gameglobal.SCENARIO_PLAY_NPC:
            return False
        return self.isFuncNpc(npcConst.NPC_FUNC_BUSINESS)

    def _isBusinessNpcSpy(self):
        if self.isScenario == gameglobal.SCENARIO_PLAY_NPC:
            return False
        return self.isFuncNpc(npcConst.NPC_FUNC_BUSINESS_SPY)

    def _isCommonMarkerNpc(self):
        if self.isScenario == gameglobal.SCENARIO_PLAY_NPC:
            return False
        return self.isFuncNpc(npcConst.NPC_FUNC_COMMON_MARKER)

    def _isPickNpc(self):
        if self.isScenario == gameglobal.SCENARIO_PLAY_NPC:
            return False
        functions = self.filterFunctions()
        if len(functions) == 0:
            return True
        funcs = [ x[1] for x in functions ]
        for funId in funcs:
            if funId in npcConst.NPC_PICK_GROUP:
                return True

        return False

    def _isRunManNpc(self):
        if self.isScenario == gameglobal.SCENARIO_PLAY_NPC:
            return False
        if self.isFuncNpc(npcConst.NPC_FUNC_GUILD_RUN_MAN):
            if not self.npcFunctions[npcConst.NPC_FUNC_GUILD_RUN_MAN]:
                return True
        return False

    def needMoveNotifier(self):
        return self.getItemData().get('idleAct') != None

    def movingNotifier(self, isMoving, moveSpeed = 1.0):
        self.isMoving = isMoving
        if isMoving:
            self.fashion.stopAction()
        elif self.isPlaySchemedIdleAct():
            self.fashion.playSingleAction(self.idleActName)

    def isPlaySchemedIdleAct(self):
        if self.idleActName and not self.isMoving:
            return True
        return False

    def enterTopLogoRange(self, rangeDist = -1):
        super(Npc, self).enterTopLogoRange(rangeDist)
        if self.isScenario == gameglobal.NORMAL_NPC:
            notTurn = NMCD.data.get(self.npcId, {}).get('notTurn', 0)
            if not notTurn:
                self.fashion.beginHeadTracker(False)
        if self.inWorld and self.topLogo and self.titleName:
            self.topLogo.titleName = self.titleName
            self.topLogo.setTitleName(self.titleName)
        if self.topLogo:
            if gameglobal.gHideNpcName:
                self.topLogo.hideName(True)
            if gameglobal.gHideNpcTitle:
                self.topLogo.hideTitleName(True)
            self.set_robberNpcStatus(0)
        npcData = NMCD.data.get(self.npcId, {})
        musicParma = npcData.get('musicParam', None)
        if musicParma:
            value = npcData.get('musicValue', 0)
            Sound.setMusicParam(musicParma, value)
        self.refreshOpacityState()

    def resetTopLogo(self):
        if not self.inWorld or not self.topLogo:
            return
        if self._isMarkerNpc() and BigWorld.isPublishedVersion():
            functions = self.filterFunctions()
            if len(functions) == 1:
                return
        super(Npc, self).resetTopLogo()

    def leaveTopLogoRange(self, rangeDist = -1):
        if self.isScenario == gameglobal.SCENARIO_PLAY_NPC:
            return
        self.fashion.stopHeadTracker()
        super(Npc, self).leaveTopLogoRange(rangeDist)
        npcData = NMCD.data.get(self.npcId, {})
        musicParma = npcData.get('musicParam', None)
        if musicParma:
            Sound.setMusicParam(musicParma, 0)

    def faceTo(self, target):
        if not target:
            return
        if not self.inWorld:
            return
        nd = NMCD.data.get(self.npcId, None)
        if not nd:
            return
        keepYaw = nd.get('keepYaw', 0)
        if keepYaw:
            return
        if self.actGroupId == const.GUILD_RESIDENT_RESTAURANT_ACT_GROUP_ID:
            return
        self.filter.setYaw((target.position - self.position).yaw)

    def parseFunctions(self):
        options = {}
        functions = self.filterFunctions()
        for funcName, func, funcId in functions:
            if func in (npcConst.NPC_FUNC_TELEPORT, npcConst.NPC_FUNC_DIRECT_TRANFER):
                d = TD.data.get(funcId, None)
                if d == None:
                    continue
                teleport = d.get('teleport')
                for idx, value in enumerate(teleport):
                    name, fbId = value[0], value[1]
                    if not self.getFuncDisabled(npcConst.NPC_FUNC_TELEPORT, idx):
                        self.addToOption(options, (func, funcName), (name, fbId, idx))

            else:
                self.addToOption(options, (func, funcName), funcId)

        return options

    def isFuncLocked(self, func, funcId):
        if self.blackFuncList.get((func, funcId), False):
            return True
        if not gameglobal.rds.configData.get('enableServerProgress', False):
            return False
        key = (func, funcId or 0)
        if NLD.data.has_key(key):
            if self.unlockedFuncIds.has_key(key):
                return self.unlockedFuncIds.get(key) == npcConst.NpcFuncLock
            else:
                return NLD.data[key].get('initStatus', npcConst.NpcFuncUnlock) == npcConst.NpcFuncLock
        else:
            return False

    def hasFuncClosed(self):
        npcData = ND.data.get(self.npcId, {})
        functions = npcData.get('functions', [])
        for funcName, func, funcId in functions:
            if self.isFuncLocked(func, funcId):
                return True

        return False

    def filterFunctions(self):
        player = BigWorld.player()
        npcData = ND.data.get(self.npcId, {})
        functions = npcData.get('functions', [])
        fameConds = npcData.get('funcFame', {})
        funcXingjiTimes = npcData.get('funcXingjiTimes', {})
        funcConfigIds = npcData.get('funcConfigIds', {})
        filterFuncs = []
        for funcName, func, funcId in functions:
            if funcConfigIds.has_key(func):
                if utils.getEnableCheckServerConfig() and not utils.checkInCorrectServer(funcConfigIds[func]):
                    continue
            if self.isFuncLocked(func, funcId):
                continue
            if fameConds.has_key(func):
                if not player.enoughFame(fameConds[func]):
                    continue
            if funcXingjiTimes.has_key(func):
                xingjiTimes = funcXingjiTimes[func]
                if not formula.isInXingJiTimeIntervals(xingjiTimes):
                    continue
            if func == npcConst.NPC_FUNC_SOCIAL_SCHOOL_REJOIN:
                if not (player.curSocSchool == 0 and player.socSchools.has_key(funcId)):
                    continue
            if func == npcConst.NPC_FUNC_FUBEN_DIFFICULTY_ADJUST:
                if not (gameglobal.rds.ui.currentShishenMode != 0 and player.isInTeamOrGroup() and player.isTeamLeader()):
                    continue
            if func == npcConst.NPC_FUNC_GET_EXP_BONUS:
                if not gameglobal.rds.ui.expBonus.hasAvaliableExpBonus(funcId):
                    continue
            if func == npcConst.NPC_FUNC_SHOW_SUI_XING_YU_RESULT:
                if gameglobal.rds.ui.suiXingYu.isSuiXingYuTime():
                    continue
            if func == npcConst.NPC_FUNC_WMD_KILL_RANK:
                if not WCD.data.get('wmdRankSwitcher', 0):
                    continue
            if func == npcConst.NPC_FUNC_WMD_SHANGJIN_RANK:
                if not WCD.data.get('wmdRankSwitcher', 0):
                    continue
            if func == npcConst.NPC_FUNC_YCWZ_RANK:
                if not gameglobal.rds.configData.get('enableYunchuiTopRank', False):
                    continue
            if func == npcConst.NPC_FUNC_CBG:
                if not gameglobal.rds.configData.get('enableCBG', True):
                    continue
            if func == npcConst.NPC_FUNC_WORLD_CHALLENGE:
                if not gameglobal.rds.ui.challenge.showChallengeConfig():
                    continue
            if func == npcConst.NPC_FUNC_EXCHANGE_EQUIP_PRE_PROP:
                if not gameglobal.rds.configData.get('enableExchangeEquipPreProp', False):
                    continue
            if func == npcConst.NPC_FUNC_TRANSFER_EQUIP_PROPS:
                if not gameglobal.rds.configData.get('enableTransferEquipProps', False):
                    continue
            if func == npcConst.NPC_FUNC_RECYCLE_ITEM:
                if not gameglobal.rds.configData.get('enableItemRecall', False):
                    continue
            if func == npcConst.NPC_FUNC_FREE_FB_PUNISH_BY_BAIL:
                if not player.inFbPunish():
                    continue
            if func == npcConst.NPC_FUNC_FREE_CHAT_BY_BAIL:
                if not player.isBlockChat():
                    continue
            if func == npcConst.NPC_FUNC_PAY_BAIL:
                if player.isolateType == gametypes.ISOLATE_TYPE_NONE:
                    continue
            if func == npcConst.NPC_FUNC_GUILD_SALARY_ASSIGN:
                if not gameglobal.rds.configData.get('enableGuildPayCash', False) and not gameglobal.rds.configData.get('enableGuildPayCoin', False):
                    continue
                if player.guildNUID == 0:
                    continue
                if player.guildNUID > 0 and player.guild == None:
                    continue
                if player.guildNUID > 0 and player.gbId != player.guild.leaderGbId:
                    continue
            if func == npcConst.NPC_FUNC_GUILD_SALARY_RECEIVE:
                if not gameglobal.rds.configData.get('enableGuildPayCash', False) and not gameglobal.rds.configData.get('enableGuildPayCoin', False):
                    continue
                if player.guildNUID == 0:
                    continue
            if func == npcConst.NPC_FUNC_HOME_CHECK_INFO:
                if not gameglobal.rds.configData.get('enableHomePermissionSet', False):
                    continue
            if func == npcConst.NPC_FUNC_GUILD_SALARY_HISTORY:
                if player.guildNUID == 0:
                    continue
                if player.guildNUID > 0 and player.guild == None:
                    continue
                if player.guildNUID > 0 and player.gbId != player.guild.leaderGbId:
                    continue
            if func == npcConst.NPC_FUNC_ACTIVITY_REWARD:
                hideTypes = [ int(x.strip()) for x in gameglobal.rds.configData.get('hideActivityRewardTypes', '').split(',') if x.isdigit() ]
                if funcId in hideTypes:
                    continue
            if func == npcConst.NPC_FUNC_MIGRATE and not gameglobal.rds.configData.get('enableMigrateOut', False):
                continue
            if func == npcConst.NPC_FUNC_FROZEN_PUNISH:
                if not gameglobal.rds.ui.frozenPunish.isShowFrozenPunish():
                    continue
            if func == npcConst.NPC_FUNC_METERIAL_BAG:
                if not gameglobal.rds.configData.get('enableMeterialNpc', False):
                    continue
            if func == npcConst.NPC_FUNC_WISH_MADE:
                if not gameglobal.rds.configData.get('enableWish', False):
                    continue
            if func == npcConst.NPC_FUNC_WISH_VIEW:
                if not gameglobal.rds.configData.get('enableWish', False):
                    continue
            if func == npcConst.NPC_FUNC_HOME_BUY:
                if player.myHome.hasHome():
                    continue
            if func == npcConst.NPC_FUNC_HOME_GOTO_MYFLOOR:
                if not player.myHome.hasHome():
                    continue
            if func == npcConst.NPC_FUNC_HOME_REMOVE_ROOM:
                if not player.myHome.hasHome():
                    continue
                if not gameglobal.rds.configData.get('enableRemoveHome', False):
                    continue
            if func == npcConst.NPC_FUNC_HOME_EXTENSION:
                if not player.myHome.hasHome() or not HD.data.get(player.myHome.roomId, {}).get('expandHomeId', None):
                    continue
            if func == npcConst.NPC_FUNC_SHARE_CHAR_CONF:
                if not gameglobal.rds.configData.get('enableUploadCharacterPhoto', False):
                    continue
            if func == npcConst.NPC_FUNC_SCHOOL_ENTRUST and not funcId == player.school:
                continue
            if func in (npcConst.NPC_FUNC_QUEST_LEARN,
             npcConst.NPC_FUNC_QUEST_DIALOG,
             npcConst.NPC_FUNC_QUEST_DEBATE,
             npcConst.NPC_FUNC_QUEST_PUZZLE):
                if funcId not in player.quests:
                    continue
            if func == npcConst.NPC_FUNC_OPEN_DYNAMIC_SHOP and not gameglobal.rds.configData.get('enableDynamicShop', False):
                continue
            if func == npcConst.NPC_FUNC_PERSONAL_SPACE and not getattr(self, 'statueOwnerGbId', 0):
                continue
            if func in (npcConst.NPC_FUMC_TREASURE_BOX_WISH_NORMAL, npcConst.NPC_FUMC_TREASURE_BOX_WISH_CBT, npcConst.NPC_FUMC_TREASURE_BOX_WISH_RAFFLE):
                if not gameglobal.rds.configData.get('enableUseItemWish', False):
                    continue
            if func == npcConst.NPC_FUNC_SPRITE_MATERIAL_BAG:
                if not gameglobal.rds.configData.get('enableSpriteMaterialBag', False) or not BigWorld.player().summonSpriteList:
                    continue
            if func == npcConst.NPC_FUNC_SPRITE_EXPLORE:
                if not gameglobal.rds.configData.get('enableExploreSprite', False):
                    continue
            if func in (npcConst.NPC_FUNC_ENTER_GUILD_FUBEN_NORMAL,
             npcConst.NPC_FUNC_ENTER_GUILD_FUBEN_ELITE,
             npcConst.NPC_FUNC_OPEN_GUILD_FUBEN,
             npcConst.NPC_FUNC_GUILD_FUBEN_SET_MEMBERS):
                if not gameglobal.rds.configData.get('enableGuildFuben', False):
                    continue
            if func == npcConst.NPC_FUNC_GUILD:
                if funcId == gametypes.GUILD_NPC_OPTION_RECV_INHERIT_FROM_NPC:
                    serverProgressMsId = SCD.data.get('serverExpAddProgressId', 0)
                    if gameconfigCommon.enableServerExpAddLimit() and serverProgressMsId and not player.checkServerProgress(serverProgressMsId, False):
                        continue
            if (not gameconfigCommon.enableNpcFavor() or not BigWorld.player().checkNpcFrindLv() or BigWorld.player().checkInAutoQuest()) and func in (npcConst.NPC_FUNC_INTERACTIVE,
             npcConst.NPC_FUNC_NF_RECEIVE_GIFT,
             npcConst.NPC_FUNC_NF_ACTOR_ROLE,
             npcConst.NPC_FUNC_NF_INTERACTIVE,
             npcConst.NPC_FUNC_NF_ACCEPT_LOOP_QUEST,
             npcConst.NPC_FUNC_NF_ACCEPT_LOOP_QUEST_WEEKLY,
             npcConst.NPC_FUNC_NF_ACCEPT_LOOP_QUEST_MONTHLY,
             npcConst.NPC_FUNC_NF_ACCEPT_QUEST):
                continue
            if func == npcConst.NPC_FUNC_NF_INTERACTIVE:
                npcPId = commNpcFavor.getNpcPId(self.npcId)
                if not NND.data.get(npcPId, {}).get('isGift', 0):
                    continue
            filterFuncs.append((funcName, func, funcId))

        return filterFuncs

    def addToOption(self, options, funcId, value):
        if options.has_key(funcId):
            options[funcId].append(value)
        else:
            options[funcId] = [value]

    def use(self):
        p = BigWorld.player()
        if p.life == gametypes.LIFE_DEAD:
            p.showGameMsg(GMDD.data.FORBIDDEN_WRONG_LIFE, ())
            return
        if not self.checkDistSqr(25):
            return
        if self.forbidUse():
            return
        if self.guildNUID and self.guildNUID != p.guildNUID:
            p.showGameMsg(GMDD.data.FORBIDDEN_WRONG_GUILD, ())
            return
        if hasattr(p, 'isTrading') and p.isTrading:
            p.showGameMsg(GMDD.data.ITEM_TRADE_NO_NPC_CHAT, ())
            return
        if gameglobal.rds.configData.get('enableForbidNpcAndDawdler', False):
            if hasattr(self, 'getOpacityValue'):
                opacityValue = self.getOpacityValue()
                if opacityValue[0] != gameglobal.OPACITY_FULL:
                    return
            if hasattr(self, '_isMarkerNpc') and self._isMarkerNpc():
                return
            nd = NMCD.data.get(self.npcId, None)
            if nd:
                p.showGameMsg(GMDD.data.FORBIDDEN_MAP_GAME_GRAVE, nd.get('name', ''))
            return
        super(Npc, self).use()
        gamelog.debug('JJH: use in Npc')
        self.faceTo(p)
        if not self._isTriggered():
            holdTime = QMD.data.get(self.npcId, {}).get('holdTime', 0)
            indirectTime = QMD.data.get(self.npcId, {}).get('indirectTime', ())
            if not holdTime and not indirectTime:
                p.useMarkerNpc(self.npcId)
            elif holdTime:
                gameglobal.rds.ui.dynamicFCastBar.startHoldPress(p.getServerTime(), holdTime, self.npcId)
                gameglobal.rds.ui.dynamicFCastBar.recordHoldPressUpTime(False, p.getServerTime() + 1)
            elif indirectTime:
                gameglobal.rds.ui.dynamicFCastBar.startIndirectPress(p.getServerTime(), indirectTime, self.npcId)
            return
        options = self.parseFunctions()
        p.npcDialog(self.id, options)
        soundIdx = self.getItemData().get('useNpcSound', 0)
        gameglobal.rds.sound.playSound(soundIdx)
        chatClues = QCRD.data.get(const.CHAR_STORY_CON_NPC_CHAT, {}).get('clues', [])
        for cid in chatClues:
            if not QCD.data.has_key(cid):
                continue
            cond = QCD.data[cid].get('condition')
            if not cond or cond({'npcId': self.npcId,
             'chatId': 0}):
                p.cell.triggerCharsConditionByClient(const.CHAR_STORY_CON_NPC_CHAT, ('npcId', 'chatId'), (str(self.npcId), '0'))
                break

    def answer(self, option, current):
        super(Npc, self).answer(option, current)

    def onChatChoice(self, chatId):
        if not self.inWorld:
            return
        drd = DRD.data[self.npcId]
        if drd.has_key('chatIds'):
            if chatId in drd['chatIds']:
                BigWorld.player().cell.onQuestDialog(self.id, chatId)

    def _isTriggered(self):
        if self._isMarkerNpc():
            p = BigWorld.player()
            for questId in p.quests:
                markerInfo, _ = p.getQuestData(questId, const.QD_QUEST_MARKER, (None, None))
                needTrigger = markerInfo and markerInfo.has_key(self.npcId)
                gamelog.debug('zt: npc.use', markerInfo, needTrigger)
                if needTrigger:
                    isTriggered = markerInfo[self.npcId] > 0
                    gamelog.debug('zt: npc.use isTriggered', isTriggered)
                    if not isTriggered:
                        return False

        return True

    def getItemData(self):
        nd = NMCD.data.get(self.npcId, {})
        isGraveState = gameglobal.rds.ui.mapGameMapV2.isGraveState()
        if isGraveState:
            if hasattr(self, '_isMarkerNpc') and self._isMarkerNpc():
                pass
            elif hasattr(self, 'getOpacityValue'):
                opacityValue = self.getOpacityValue()
                if opacityValue[0] == gameglobal.OPACITY_FULL:
                    nd = copy.deepcopy(NMCD.data.get(self.npcId, {}))
                    nd['extraTint'] = SCD.data.get('ghostmatte', 'refaction002')
            else:
                nd = copy.deepcopy(NMCD.data.get(self.npcId, None))
                nd['extraTint'] = SCD.data.get('ghostmatte', 'refaction002')
        if nd is None:
            raise Exception('nmcd error ' + str(self.npcId) + '-' + str(type(self.npcId)))
        modelId = nd.get('model', 0)
        if not nd or not modelId:
            return {'model': gameglobal.defaultModelID,
             'dye': 'Default'}
        nd = self.checkChangeItemData(nd)
        return nd

    def checkChangeItemData(self, npcModelData):
        newNpcModelData = npcModelData
        if self.isMature:
            modelId = DPTCD.data.get('harvestedModelId', 0)
            if modelId:
                newNpcModelData = copy.copy(npcModelData)
                newNpcModelData['model'] = modelId
        return newNpcModelData

    def getModelScale(self):
        nd = NMCD.data.get(self.npcId, {})
        scale = nd.get('modelScale', 1.0)
        return (scale, scale, scale)

    def getFuncDisabled(self, funcId, indexId):
        if funcId == npcConst.NPC_FUNC_TELEPORT:
            return commcalc.getBitDword(self.functionFlag, indexId)
        elif funcId == npcConst.NPC_FUNC_DIRECT_TRANFER:
            return commcalc.getBitDword(self.functionFlag, indexId)
        else:
            return False

    def getTopIcon(self):
        if hasattr(self, 'shaxingNpcStatus'):
            if self.shaxingNpcStatus == gametypes.NPC_SHAXING_STATUS_SIGNUP:
                return NMCD.data.get(self.npcId, {}).get('signUpTopIcon')
            if self.shaxingNpcStatus == gametypes.NPC_SHAXING_STATUS_OBSERVE:
                return NMCD.data.get(self.npcId, {}).get('observeTopIcon')
        return NMCD.data.get(self.npcId, {}).get('topIcon')

    def setFuncDisabled(self, funcId, indexId, on):
        if funcId == npcConst.NPC_FUNC_TELEPORT:
            commcalc.calcBitDword(self.functionFlag, indexId, on)

    def npcTrapCallback(self, leaveWorld = False):
        if self.forbidUse() or not self._isPickNpc():
            return
        p = BigWorld.player()
        if (p.position - self.position).length <= SCD.data.get('questCompleteNpcTriggerChatDistance', 10):
            self.triggerNpcChat()
        npcDialogLength = NMCD.data.get(self.npcId, {}).get('npcDialogLength', SCD.data.get('npcDialogLength', 4)) + ND.data.get(self.npcId, {}).get('bodysize', 0)
        if (self.position - p.position).length <= npcDialogLength and not leaveWorld:
            if self.getNpcPriority() in (gameglobal.NPC_WITH_NO_CHAT, gameglobal.NPC_WITH_NO_FUNC):
                return
            if self.guildNUID and self.guildNUID != p.guildNUID:
                return
            p.npcTrapInCallback((self,))
        else:
            p.npcTrapOutCallback((self,))

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        if self.beHide or self.forbidUse():
            return
        p = BigWorld.player()
        if enteredTrap:
            npcPriority = self.getNpcPriority()
            if npcPriority in (gameglobal.NPC_WITH_NO_CHAT, gameglobal.NPC_WITH_NO_FUNC):
                return
            if self.guildNUID and self.guildNUID != p.guildNUID:
                return
            if not self._isTriggered():
                return
            p.npcTrapInCallback((self,))
            if npcPriority == gameglobal.NPC_WITH_COMPLETE_QUEST:
                self.showSucBubbleDialog()
        else:
            p.npcTrapOutCallback((self,))

    def trapChatCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        if self.beHide or self.forbidUse():
            return
        if enteredTrap:
            self.triggerNpcChat()

    def triggerNpcChat(self):
        if not self.getCompleteQuests():
            return
        msgId = self.choiceChatMsg()
        msgId and self.npcChat(msgId)

    def npcChat(self, msgId):
        msg = DD.data.get(msgId)
        if msg is None:
            return
        speakEvent = msg.get('speakEvent', None)
        speakEvent and uiUtils.dealNpcSpeakEvents(speakEvent, self.id, False)
        details = msg.get('details', '')
        duration = msg.get('interval', const.POPUP_MSG_SHOW_DURATION)
        msg and self.topLogo and self.topLogo.setChatMsg(details, duration)

    def choiceChatMsg(self):
        chatList = []
        for questId in self.getCompleteQuests():
            questItem = QD.data.get(questId)
            if questItem is None:
                continue
            chatTuple = questItem.get('finishDialog')
            if chatTuple is None:
                continue
            chatList.extend(chatTuple)

        if not chatList:
            return 0
        return choice(chatList)

    def playActions(self, actNames):
        gamelog.debug('@lihang:npc.playActions', self.id, actNames)
        if type(actNames) != tuple or len(actNames) < 1:
            return
        self.fashion.stopAction()
        for act in actNames:
            self.fashion.playSingleAction(act)

    def needBlackShadow(self):
        nmcd = NMCD.data.get(self.npcId, {})
        noBlackUfo = nmcd.get('noBlackUfo', False)
        return not noBlackUfo

    def onResetYaw(self):
        self.filter.setYaw(self.initYaw)

    def getOpacityValue(self):
        p = BigWorld.player()
        opacityVal = super(Npc, self).getOpacityValue()
        if not self.inWorld:
            return (gameglobal.OPACITY_HIDE, False)
        if self.needToHide():
            return (gameglobal.OPACITY_HIDE, False)
        if self.hideInFightForLoveFuben():
            return (gameglobal.OPACITY_HIDE, False)
        if gameglobal.rds.ui.cameraTable.isHideNpcs():
            return (gameglobal.OPACITY_HIDE, False)
        nd = ND.data.get(self.npcId, {})
        if self.isScenario == gameglobal.NORMAL_NPC:
            if gameglobal.GM_NPC_VISIBLE_ALL:
                return (gameglobal.OPACITY_FULL, True)
            if gameglobal.GM_NPC_VISIBLE_TAG.get(self.publishtag, 0) == 1:
                return (gameglobal.OPACITY_FULL, True)
            if gameglobal.GM_NPC_VISIBLE_TAG.get(self.publishtag, 0) == -1:
                return (gameglobal.OPACITY_HIDE, False)
            if gameglobal.SCENARIO_PLAYING != gameglobal.SCENARIO_END:
                scenarioIns = scenario.Scenario.PLAY_INSTANCE if scenario.Scenario.PLAY_INSTANCE else scenario.Scenario.INSTANCE
                if scenarioIns and self.npcId in scenarioIns.hideNpcIds:
                    self.hideByScenario(const.VISIBILITY_HIDE)
                    scenarioIns.hideNPCLog.append(self.id)
                    return (gameglobal.OPACITY_HIDE, False)
            if nd.has_key('islingshi'):
                return clientcom.getEntityLingShiOpacityValue(nd)
            if nd.has_key('displayXingjiTimes'):
                xingjiTimes = nd['displayXingjiTimes']
                if not formula.isInXingJiTimeIntervals(xingjiTimes):
                    return (gameglobal.OPACITY_HIDE, False)
            if nd.has_key('displayRealTimes'):
                realTimes = nd['displayRealTimes']
                weekSet = nd.get('displayRealWeekSet', 0)
                bHide = True
                for start, end in realTimes:
                    if utils.inCrontabRange(start, end, weekSet=weekSet):
                        bHide = False
                        break

                if bHide:
                    return (gameglobal.OPACITY_HIDE, False)
            if nd.has_key('hideRealTimes'):
                realTimes = nd['hideRealTimes']
                weekSet = nd.get('hideRealWeekSet', 0)
                for start, end in realTimes:
                    if utils.inCrontabRange(start, end, weekSet=weekSet):
                        return (gameglobal.OPACITY_HIDE, False)

            if self._isQuestNpc():
                opacityVal = self.getOpacityValueByQuest(opacityVal)
            if self._isMarkerNpc() or self._isCommonMarkerNpc():
                opacityVal = self.getOpacityValueByMarker(opacityVal)
            if self._isPuzzleNpc():
                opacityVal = self.getOpacityValueByPuzzle(opacityVal)
            if self._isRunManNpc():
                opacityVal = self.getOpacityValueByRunMan(opacityVal)
            if nd.has_key('multiCarrierHideList'):
                hideList = nd.get('multiCarrierHideList', ())
                p = BigWorld.player()
                if p.carrier.isRunningState() and p.carrier.carrierNo in hideList:
                    return (gameglobal.OPACITY_HIDE, False)
        return opacityVal

    def refreshOpacityState(self):
        if self.isScenario == gameglobal.NORMAL_NPC:
            super(Npc, self).refreshOpacityState()
            opacityValue = self.getOpacityValue()
            if opacityValue[0] == gameglobal.OPACITY_FULL:
                self.npcTrapCallback(False)
                self._addTriggerEff()
            else:
                self.npcTrapCallback(True)
                if self._isMarkerNpc() and self.id in gameglobal.rds.ui.pressKeyF.markers:
                    gameglobal.rds.ui.pressKeyF.removeMarker(self.id)

    def refreshOpacityOnTimer(self):
        if not self.inWorld:
            return
        nd = ND.data.get(self.npcId, {})
        if not (self.isScenario == gameglobal.NORMAL_NPC and (nd.has_key('displayXingjiTimes') or nd.has_key('displayRealTimes') or nd.has_key('hideRealTimes'))):
            return
        self.refreshOpacityState()
        nextTime = 0
        if self.isScenario == gameglobal.NORMAL_NPC:
            if nd.has_key('displayXingjiTimes'):
                for startTime, endTime in nd['displayXingjiTimes']:
                    tmpNextTime = formula.getRealTimeToAXingJiMoment(startTime)
                    if nextTime == 0 or tmpNextTime < nextTime:
                        nextTime = tmpNextTime
                    tmpNextTime = formula.getRealTimeToAXingJiMoment(endTime)
                    if nextTime == 0 or tmpNextTime < nextTime:
                        nextTime = tmpNextTime

            if nd.has_key('displayRealTimes'):
                weekSet = nd.get('displayRealWeekSet', 0)
                for start, end in nd['displayRealTimes']:
                    tmpNextTime = utils.getNextCrontabTime(start, weekSet=weekSet) - utils.getNow()
                    if nextTime == 0 or tmpNextTime < nextTime:
                        nextTime = tmpNextTime
                    tmpNextTime = utils.getNextCrontabTime(end, weekSet=weekSet) - utils.getNow()
                    if nextTime == 0 or tmpNextTime < nextTime:
                        nextTime = tmpNextTime

            if nd.has_key('hideRealTimes'):
                weekSet = nd.get('hideRealWeekSet', 0)
                for start, end in nd['hideRealTimes']:
                    tmpNextTime = utils.getNextCrontabTime(start, weekSet=weekSet) - utils.getNow()
                    if nextTime == 0 or tmpNextTime < nextTime:
                        nextTime = tmpNextTime
                    tmpNextTime = utils.getNextCrontabTime(end, weekSet=weekSet) - utils.getNow()
                    if nextTime == 0 or tmpNextTime < nextTime:
                        nextTime = tmpNextTime

        if self.refreshOnTimerHandle:
            BigWorld.cancelCallback(self.refreshOnTimerHandle)
            self.refreshOnTimerHandle = None
        if nextTime > 0:
            self.refreshOnTimerHandle = BigWorld.callback(nextTime + 2, self.refreshOpacityOnTimer)

    def set_physique(self, old):
        pass

    def set_aspect(self, old):
        pass

    def set_avatarConfig(self, old):
        if self.firstFetchFinished:
            pass

    def dealTrapInEvent(self, trapLengthType = 1):
        super(Npc, self).dealTrapInEvent(trapLengthType)
        if self._isQuestNpc():
            self.autoDelQuestNearBy()

    def addTrapEvent(self):
        if self.isScenario == gameglobal.NORMAL_NPC:
            for i in xrange(1, impPot.TRAP_MAX_NUM):
                trapLengthName = 'trapLength'
                if i != 1:
                    trapLengthName = trapLengthName + str(i)
                trapLength = self.getItemData().get(trapLengthName, 0)
                setattr(self, trapLengthName, trapLength)
                if self._isQuestNpc() and trapLength < const.QUEST_TRAP_LENGTH:
                    if i == 1:
                        setattr(self, trapLengthName, const.QUEST_TRAP_LENGTH)
                    else:
                        trapLength = self.getItemData().get(trapLengthName)
                        if trapLength != None:
                            setattr(self, trapLengthName, const.QUEST_TRAP_LENGTH)

            super(Npc, self).addTrapEvent()

    def isFunctionNpc(self):
        if self.npcHasFunc is not None:
            return self.npcHasFunc
        npcData = ND.data.get(self.npcId, {})
        functions = npcData.get('functions', None)
        if functions is None:
            self.npcHasFunc = False
        else:
            self.npcHasFunc = True
        return self.npcHasFunc

    def getBasicEffectLv(self):
        if self.isScenario == gameglobal.SCENARIO_PLAY_NPC:
            return gameglobal.EFFECT_HIGH
        return super(Npc, self).getBasicEffectLv()

    def getBasicEffectPriority(self):
        if self.isScenario == gameglobal.SCENARIO_PLAY_NPC:
            return gameglobal.EFF_HIGHEST_PRIORITY
        return super(Npc, self).getBasicEffectPriority()

    def isUrgentLoad(self):
        if self.isScenario == gameglobal.SCENARIO_PLAY_NPC:
            return True
        needUrgenToLoad = self.isFunctionNpc()
        p = BigWorld.player()
        if p and p.position.distSqrTo(self.position) < gameglobal.URGENT_LOADDIST * gameglobal.URGENT_LOADDIST and needUrgenToLoad:
            return True
        return False

    def getEffectLv(self):
        if self.isScenario == gameglobal.SCENARIO_PLAY_NPC:
            return gameglobal.EFF_HIGHEST_PRIORITY
        return super(Npc, self).getEffectLv()

    @property
    def randWingId(self):
        return 0

    def inFlyTypeWing(self):
        return self.getItemData().get('wingId', 0)

    @property
    def inFly(self):
        return self.inFlyTypeWing()

    def isKeyNpc(self):
        npcData = NMCD.data.get(self.npcId, {})
        topIcon = npcData.get('topIcon', None)
        if topIcon not in ('ansuo_1', 'tansuo_2', 'jiaotan_1', 'jiaotan_2', 'guankan_1'):
            return False
        return True

    def getShowLoadLv(self):
        if self.isFunctionNpc() or self.isKeyNpc():
            return gameglobal.SHOWLOADDEFAULTLV
        npcData = NMCD.data.get(self.npcId, {})
        noNeedHide = npcData.get('noNeedHide', False)
        if noNeedHide:
            return gameglobal.SHOWLOADDEFAULTLV
        if clientcom.getNpcModelMaxCnt() <= gameglobal.CURRENT_NPC_MODEL_CNT:
            return gameglobal.SHOWLOADMAXLV
        showLoadLv = npcData.get('showLoadLv', gameglobal.SHOWLOADDEFAULTLV)
        return showLoadLv

    def needToHide(self):
        if not gameglobal.rds.configData.get('enableHideNpc', True):
            return False
        p = BigWorld.player()
        if p.spaceNo != const.SPACE_NO_BIG_WORLD:
            return False
        if self.isScenario in (gameglobal.SCENARIO_PLAY_NPC, gameglobal.SCENARIO_EDIT_NPC):
            return False
        showLoadLv = self.getShowLoadLv()
        videoSettingLv = appSetting.VideoQualitySettingObj.getVideoQualityLv()
        if videoSettingLv >= showLoadLv:
            return False
        return True

    def hideInFightForLoveFuben(self):
        p = BigWorld.player()
        npcIds = FFLCD.data.get('needHideNpc', ())
        if p.inFightForLoveFb():
            if getattr(self, 'npcId', None) in npcIds:
                if not p.isFightForLoveCreator():
                    return True
        return False

    def onUpdateNpcModel(self):
        self.reloadModel()

    def addLingShiExtraTint(self):
        p = BigWorld.player()
        if not getattr(p, 'lingShiFlag', False):
            return
        lingShiTintName = ND.data.get(self.npcId, {}).get('lingShiTintName', '')
        if lingShiTintName:
            tintalt.ta_reset(self.allModels)
            tintalt.ta_add(self.allModels, lingShiTintName, tintType=tintalt.NPC_LINGSHI)

    def delLingShiExtraTint(self):
        tintalt.ta_reset(self.allModels)

    def set_isMature(self, old):
        if self.isMature:
            modelServer.loadModelByItemData(self.id, gameglobal.DEFAULT_THREAD, self.shiftModelFinished, self.getItemData())

    def shiftModelFinished(self, model):
        self.modelServer._singlePartModelFinish(model)
        self.resetTopLogo()
