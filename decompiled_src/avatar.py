#Embedded file name: /WORKSPACE/data/entities/client/avatar.o
import time
import traceback
import math
import copy
import inspect
import socket
import random
import cPickle
import zlib
from os.path import getsize
import BigWorld
import Sound
import C_ui
import Math
import Pixie
import ResMgr
import keys
import game
import gameglobal
import Hijack
import combatProto
import utils
import const
import clientcom
import iCombatUnit
import gametypes
import func
import storageCommon
import equipment
import subEquipment
import chatConfig
import formula
import commcalc
import container
import gamelog
import fishingEquipment
import friend
import runeCommon
import inventoryCommon
from battleFieldBagCommon import BattleFieldBagCommon
import exploreEquipment
import lifeEquipment
import netWork
import appSetting
import commQuest
import clientUtils
import gameConfigUtils
import gameconfigCommon
import pg_protect
import summonedSpriteAccessory
import summonSpriteBiography
import summonSpriteAppearance
import personalZoneSkin
import spriteChat
import spriteWingWorldRes
import logicInfo
from wingWorldForge import WingWorldForge
from gamescript import ScriptRunningEnv
from helpers import CEFControl
from helpers import tickManager
from sfx import physicsEffect
from roleSaleData import RoleSaleData
from guis import cursor
from guis import ui
from guis import hotkey as HK
from guis import exceptChannel
from guis import events
from guis import uiConst
from guis import menuManager
from guis import uiUtils
from guis import messageBoxProxy
from guis import topLogo
from guis import worldBossHelper
from helpers import avatarMorpher
from helpers import vertexMorpher
from helpers import keyboardPhysics
from helpers import mousePhysics
from helpers import actionPhysics
from helpers import fashion
from helpers import ufo
from helpers import modelServer
from helpers import action
from helpers import clientSM
from helpers import loadingProgress
from helpers import cellCmd
from helpers import qingGong
from helpers import bianshenState
from helpers import stateSafe
from helpers import impJumpFashion
from helpers import navigator
from helpers import scenario
from helpers import outlineHelper
from helpers import inWaterStateSound
from helpers import action as ACT
from helpers import updateAmbientMusic
from helpers import sceneInfo
from helpers import tintalt
from helpers import charRes
from helpers import preload as PLD
from helpers import autoSkill
from helpers import spaceData
from helpers import seqTask
from helpers import buildingProxy
from helpers import navigatorRouter
from helpers import clanWar
from helpers.strmap import strmap
from helpers.guild import GuildGrowth
from helpers.eventDispatcher import Event
from helpers.tournament import GuildTournament, CrossGuildTournament, CrossRankGuildTournament
from helpers import protect
from helpers import entityDebugNameFactory
from helpers import deadPlayBack
from helpers import remoteInterface
from helpers import ccControl
from helpers import taboo
from helpers import uuControl
from helpers import cc
from helpers import zaijuBag
from helpers.worldWar import WorldWar
from helpers.wingWorld import WingWorld
from helpers.wingWorld import WingWorldCityMinMap
from helpers.guild import RunManPlayerRoute
from helpers import editorHelper
from helpers.skillAppearancesUtils import SkillAppearancesDetail
from callbackHelper import Functor
from helpers import performanceMonitor
from helpers.ftbDataHelper import FtbDataHelper
from helpers.challengePassportHelper import ChallengePassportDataHelper
from helpers import AnonymousNameManager
from helpers import gameAntiCheatingManager
from sfx import sfx
from sfx import screenRipple
from sfx import screenEffect
from sfx import keyboardEffect
from appSetting import setShaderIndex
from appSetting import Obj as AppSettings
from flagStateCommon import FlagStateCommon
from VirtualMonster import VirtualMonster
from Monster import Monster
from FishGroup import FishGroup
from questLoops import QuestLoopChain
from commActivity import GroupLuckJoyVal
from sMath import limit, distance3D, distance2D
from debug import writer
from gameclass import SkillQteDict
from teamEndless import TeamEndless
from impl.impQuest import ImpQuest
from impl.impChat import ImpChat
from impl.impTeam import ImpTeam
from impl.impArena import ImpArena
from impl.impArenaPlayoffs import ImpArenaPlayoffs
from impl.impWish import ImpWish
from impl.impItem import ImpItem
from impl.impTrade import ImpTrade
from impl.impFuben import ImpFuben
from impl.impAction import ImpAction
from impl.impProperty import ImpProperty
from impl.impSwim import ImpSwim
from impl.impRide import ImpRide
from impl.impBianshen import ImpBianshen
from impl.impTutorial import ImpTutorial
from impl.impReport import ImpReport
from impl.impQieCuo import ImpQieCuo
from impl.impSignature import ImpSignature
from impl.impFriend import ImpFriend
from impl.impTop import ImpTop
from impl.impClanWar import ImpClanWar
from impl.impClanChallenge import ImpClanChallenge
from impl.impClan import ImpClan
from impl.impLifeSkill import ImpLifeSkill
from impl.impSignIn import ImpSignIn
from impl.impSocial import ImpSocial
from impl.impJobQuest import ImpJobQuest
from impl.impWorldAreaMgr import ImpWorldAreaMgr
from impl.impNOSService import ImpNOSService
from impl.impStats import ImpStats
from impl.impCC import ImpCC
from impl.impMall import ImpMall
from impl.impCharge import ImpCharge
from impl.impComm import ImpComm
from impl.impJunJie import ImpJunJie
from impl.impPlayerComm import ImpPlayerComm
from impl.impCombat import ImpCombat
from impl.impMarriage import ImpMarriage
from impl.impYixin import ImpYixin
from impl.impPropEx import ImpPropEx
from impl.impFameCollect import ImpFameCollect
from impl.impPartner import ImpPartner
from impl.impBattleField import ImpBattleField
from impl.impShengSiChang import ImpShengSiChang
from impl.impTeamShengSiChang import ImpTeamShengSiChang
from impl.impAchievement import ImpAchievement
from impl.impActivities import ImpActivities
from impl.impMultiLine import ImpMultiLine
from impl.impStorage import ImpStorage
from impl.impFishing import ImpFishing
from impl.impBooth import ImpBooth
from impl.impRune import ImpRune
from impl.impHierogram import ImpHierogram
from impl.impItem import InvClient
from impl.impItem import RideWingBagClient
from impl.impMail import ImpMail
from impl.impQte import ImpQte
from impl.impEmote import ImpEmote
from impl.impInteractive import ImpInteractive
from impl.impDelegate import ImpDelegate
from impl.impConsign import ImpConsign
from impl.impExplore import ImpExplore
from impl.impGuild import ImpGuild
from impl.impFbMessageBoard import ImpFbMessageBoard
from impl.impStorageGuild import ImpStorageGuild
from impl.impGuildShop import ImpGuildShop
from impl.impGuildMemberSkill import ImpGuildMemberSkill
from impl.impChatRoom import ImpChatRoom
from impl.impAdmin import ImpAdmin
from impl.impCoinMarket import ImpCoinMarket
from impl.impApprentice import ImpApprentice
from impl.impCoinConsign import ImpCoinConsign
from impl.impCBG import ImpCBG
from impl.impFlyUp import ImpFlyUp
from impl.impChallengePassport import ImpChallengePassport
from impl.impPUBG import ImpPUBG
from impl.impAssassination import ImpAssassination
from impl.impDoublePlantTree import ImpDoublePlantTree
from impl.impPhotoBorder import ImpPhotoBorder
from impl.impMissTianyu import ImpMissTianyu
from impl.impBet import ImpBet
from impl.impCBGItem import ImpCBGItem
from impl.impDoubleArena import ImpDoubleArena
from impl.impNeteaseMembership import ImpNeteaseMembership
from impl.impBindingProperty import ImpBindingProperty
from impl.impOfflineIncome import ImpOfflineIncome
from impl.impServerProgress import ImpServerProgress
from impl.impCrossConsign import ImpCrossConsign
from impl.impPlayerCombat import ImpPlayerCombat
from impl.impPlayerUI import ImpPlayerUI
from impl.impPlayerRideFly import ImpPlayerRideFly
from impl.impPlayerProperty import ImpPlayerProperty
from impl.impPlayerItem import ImpPlayerItem
from impl.impPlayerNpc import ImpPlayerNpc
from impl.impPlayerDebug import ImpPlayerDebug
from impl.impPlayerSwim import ImpPlayerSwim
from impl.impPlayerTeam import ImpPlayerTeam
from impl.impPlayerAbility import ImpPlayerAbility
from impl.impPlayerBooth import ImpPlayerBooth
from impl.impPlayerSight import ImpPlayerSight
from impl.impPlayerVehicle import ImpPlayerVehicle
from impl.impPlayerCheck import ImpPlayerCheck
from impl.impPlayerJingJie import ImpPlayerJingJie
from impl.impPlayerVip import ImpPlayerVip
from impl.impInvitation import ImpInvitation
from impl.impPlayerApprentice import ImpPlayerApprentice
from impl.impPlayerLottery import ImpPlayerLottery
from impl.impOpenServerBonus import ImpOpenServerBonus
from impl.impFriendInvitation import ImpFriendInvitation
from impl.impMigrate import ImpMigrate
from impl.impGuildTournament import ImpGuildTournament
from impl.impItemGive import ImpItemGive
from impl.impPuzzle import ImpPuzzle
from impl.impWorldChallenge import ImpWorldChallenge
from impl.impShuangxiu import ImpShuangxiu
from impl.impContract import ImpContract
from impl.impCollectItem import ImpCollectItem
from impl.impHandInItem import ImpHandInItem
from impl.impChars import ImpChars
from impl.impYabiao import ImpYabiao
from impl.impWorldWar import ImpWorldWar
from impl.impRedPacket import ImpRedPacket
from impl.impAppearanceCollect import ImpAppearanceCollect
from impl.impItemCommit import ImpItemCommit
from impl.impZhenyaoMatch import ImpZhenyaoMatch
from impl.impFaceEmote import ImpFaceEmote
from impl.impHome import ImpHome
from impl.impPlayerRewardHall import ImpPlayerRewardHall
from impl.impPersonalZone import ImpPersonalZone
from impl.impChatGroup import ImpChatGroup
from impl.impActivation import ImpActivation
from impl.impFriendRecall import ImpFriendRecall
from impl.impRandomLottery import ImpRandomLottery
from impl.impActivityCollect import ImpActivityCollect
from impl.impRandomTreasureBagLottery import ImpRandomItemsLottery
from impl.impLuckyDraw import ImpLuckyDraw
from impl.impRandomTurnOverCard import ImpRandomTurnOverCard
from impl.impHuntGhost import ImpHuntGhost
from impl.impRandomCardDraw import ImpRandomCardDraw
from impl.impGroupPurchase import ImpGroupPurchase
from impl.impShaxing import ImpShaxing
from impl.impShareCharConf import ImpShareCharConf
from impl.impPrivateShop import ImpPrivateShop
from impl.impGuildRobber import ImpGuildRobber
from impl.impSchool import ImpSchool
from impl.impWorldWarRob import ImpWorldWarRob
from impl.impStraightLvUp import ImpStraightLvUp
from impl.impSummonSprite import ImpSummonSprite
from impl.impSummonSpriteBiography import ImpSummonSpriteBiography
from impl.impPlayerSummonSprite import ImpPlayerSummonSprite
from commonAvatarBitsetOwnClient import ImpAvatarBitSetOwnClient
from commonAvatarPersistentBitsetOwnClient import ImpAvatarPersistentBitSetOwnClient
from impl.impRoundTable import ImpRoundTable
from impl.impSkillMacro import ImpSkillMacro
from impl.impStorageHome import ImpStorageHome
from impl.impQuestion import ImpQuestion
from impl.impEvaluate import ImpEvaluate
from impl.impGuildMerger import ImpGuildMerger
from impl.impExcitement import ImpExcitement
from impl.impMiniGame import ImpMiniGame
from impl.impMultiCarrier import ImpMultiCarrier
from impl.impPlayerSoundRecord import ImpPlayerSoundRecord
from impl.impPairPuzzle import ImpPairPuzzle
from impl.impCareerGuideShare import ImpCareerGuideShare
from impl.impSimpleQte import ImpSimpleQte
from impl.impItemUseFeedback import ImpItemUseFeedback
from impl.impDynamicShop import ImpDynamicShop
from impl.impGuildConsign import ImpGuildConsign
from impl.impWorldConsign import ImpWorldConsign
from impl.impFlowbackGroup import ImpFlowbackGroup
from impl.impWingWorld import ImpWingWorld
from impl.impDeepLearningDataApply import ImpDeepLearningDataApply
from impl.impRewardRecovery import ImpRewardRecovery
from impl.impAvoidDoingActivity import ImpAvoidDoingActivity
from impl.impCard import ImpCard
from impl.impLotteryExchange import ImpLotteryExchange
from impl.impAnnal import ImpAnnal
from impl.impWingWorldCarrier import ImpWingWorldCarrier
from impl.impWingWorldXinMo import ImpWingWorldXinMo
from impl.impQuizzes import ImpQuizzes
from impl.impSummonSpriteWingWorld import ImpSummonSpriteWingWorld
from impl.impWingWorldYabiao import ImpWingWorldYabiao
from impl.impWingWorldForge import ImpWingWorldForge
from impl.impSpriteGrowth import ImpSpriteGrowth
from impl.impCharTemp import ImpCharTemp
from impl.impFightForLove import ImpFightForLove
from impl.impOneKeyConfig import ImpOneKeyConfig
from impl.impSchoolTop import ImpSchoolTop
from impl.impNewServerActivity import ImpNewServerActivity
from impl.impHistoryConsumed import ImpHistoryConsumed
from impl.impArenaScore import ImpArenaScore
from impl.impFTB import ImpFTB
from impl.impWardrobeClient import ImpWardrobeClient
from impl.impItem import WardrobeClient
from impl.impTeamEndless import ImpTeamEndless
from impl.impSpriteChallenge import ImpSpriteChallenge
from impl.impCqzz import ImpCqzz
from impl.impGuanYin import ImpGuanYin
from impl.impSecondSchoolClient import ImpSecondSchoolClient
from impl.impWenYin import ImpWenYin
from impl.impTitle import ImpTitle
from impl.impPuppet import ImpPuppet
from impl.impWingWorldCamp import ImpWingWorldCamp
from impl.impBattleFieldChaos import ImpBattleFieldChaos
from impl.impMapGame import ImpMapGame
from impl.impClanWarCourier import ImpClanWarCourier
from impl.impNpcFavor import ImpNpcFavor
from impl.impNewPlayerTreasureBox import ImpNewPlayerTreasureBox
from impl.impWorldBoss import ImpWorldBoss
from impl.impLunZhanYunDian import ImpLunZhanYunDian
from data import couple_emote_basic_data as CEBD
from data import sys_config_data as SCD
from data import fb_data as FD
from data import monster_data as MD
from data import arena_data as AD
from data import battle_field_data as BFD
from data import sheng_si_chang_data as SSCD
from data import map_config_data as MCD
from data import multiline_digong_data as MDD
from data import fb_preload_data as FPD
from data import space_client_entitiy_data as SPCCED
from data import client_entitiy_data as CLIED
from data import school_switch_general_data as SSGD
from data import school_data as SD
from data import vp_level_data as VLD
from data import message_desc_data as MSGDD
from data import guild_challenge_data as GCHD
from data import empty_zaiju_data as EZD
from data import zaiju_data as ZJD
from cdata import transport_ref_data as TRD
from cdata import teleport_destination_data as TDD
from cdata import game_msg_def_data as GMDD
from cdata import migrate_config_data as MICD
from data import arena_mode_data as AMD
from data import avl_quest_update_lv_data as AQULD
from data import teleport_spell_data as TSD
from data import interactive_data as ID
from data import game_msg_data as GMD
from data import duel_config_data as DCD
from data import wing_world_config_data as WWCD
from data import sys_config_data as SCD
from data import fight_for_love_config_data as FFLCD
from helpers import aspectHelper
import miniclient

def precise(value):
    return int(float(value) * 10)


def isSamePosition(pos1, pos2):
    return precise(pos1[0]) == precise(pos2[0]) and precise(pos1[1]) == precise(pos2[1]) and precise(pos1[2]) == precise(pos2[2])


createAvatars = []
BLOCK_SIZE = 128 * 1024
PG_FILE_PATH = '../res/entities.pg'

class AvatarMeta(type):

    def __init__(cls, name, bases, dic):
        super(AvatarMeta, cls).__init__(name, bases, dic)
        inherits = (ImpSwim,
         ImpRide,
         ImpQuest,
         ImpChat,
         ImpTeam,
         ImpItem,
         ImpTrade,
         ImpChatRoom,
         ImpFuben,
         ImpBattleField,
         ImpShengSiChang,
         ImpTeamShengSiChang,
         ImpProperty,
         ImpAction,
         ImpArena,
         ImpArenaPlayoffs,
         ImpWish,
         ImpTutorial,
         ImpReport,
         ImpBianshen,
         ImpAchievement,
         ImpActivities,
         ImpSignIn,
         ImpQieCuo,
         ImpTop,
         ImpMultiLine,
         ImpFriend,
         ImpStorage,
         ImpBooth,
         ImpFishing,
         ImpCrossConsign,
         ImpPUBG,
         ImpRune,
         ImpHierogram,
         ImpMail,
         ImpQte,
         ImpDelegate,
         ImpEmote,
         ImpInteractive,
         ImpConsign,
         ImpExplore,
         ImpGuild,
         ImpFbMessageBoard,
         ImpAdmin,
         ImpClanWar,
         ImpClanChallenge,
         ImpClan,
         ImpPropEx,
         ImpGuildMemberSkill,
         ImpLifeSkill,
         ImpSocial,
         ImpJobQuest,
         ImpWorldAreaMgr,
         ImpStorageGuild,
         ImpGuildShop,
         ImpNOSService,
         ImpAssassination,
         ImpStats,
         ImpCC,
         ImpMall,
         ImpPartner,
         ImpJunJie,
         ImpCharge,
         ImpFameCollect,
         ImpComm,
         ImpCombat,
         ImpYixin,
         ImpCoinMarket,
         ImpInvitation,
         ImpApprentice,
         ImpCoinConsign,
         ImpCBG,
         ImpChallengePassport,
         ImpDoubleArena,
         ImpNeteaseMembership,
         ImpBindingProperty,
         ImpOfflineIncome,
         ImpServerProgress,
         ImpOpenServerBonus,
         ImpFriendInvitation,
         ImpMigrate,
         ImpMarriage,
         ImpGuildTournament,
         ImpItemGive,
         ImpPuzzle,
         ImpWorldChallenge,
         ImpShuangxiu,
         ImpContract,
         ImpFlyUp,
         ImpBet,
         ImpCBGItem,
         ImpCollectItem,
         ImpHandInItem,
         ImpChars,
         ImpYabiao,
         ImpWorldWar,
         ImpRedPacket,
         ImpSignature,
         ImpAppearanceCollect,
         ImpItemCommit,
         ImpZhenyaoMatch,
         ImpFaceEmote,
         ImpPersonalZone,
         ImpChatGroup,
         ImpShaxing,
         ImpActivation,
         ImpHome,
         ImpShareCharConf,
         ImpPrivateShop,
         ImpGuildRobber,
         ImpSchool,
         ImpWorldWarRob,
         ImpPhotoBorder,
         ImpMissTianyu,
         ImpAvatarBitSetOwnClient,
         ImpAvatarPersistentBitSetOwnClient,
         ImpStraightLvUp,
         ImpSummonSprite,
         ImpSummonSpriteBiography,
         ImpRoundTable,
         ImpSkillMacro,
         ImpStorageHome,
         ImpQuestion,
         ImpEvaluate,
         ImpExcitement,
         ImpGuildMerger,
         ImpMiniGame,
         ImpMultiCarrier,
         ImpPairPuzzle,
         ImpCareerGuideShare,
         ImpSimpleQte,
         ImpItemUseFeedback,
         ImpDynamicShop,
         ImpGuildConsign,
         ImpWorldConsign,
         ImpFlowbackGroup,
         ImpWingWorld,
         ImpDeepLearningDataApply,
         ImpRewardRecovery,
         ImpCard,
         ImpLotteryExchange,
         ImpAnnal,
         ImpFriendRecall,
         ImpGroupPurchase,
         ImpRandomItemsLottery,
         ImpRandomLottery,
         ImpRandomCardDraw,
         ImpWingWorldCarrier,
         ImpWingWorldXinMo,
         ImpQuizzes,
         ImpAvoidDoingActivity,
         ImpSummonSpriteWingWorld,
         ImpWingWorldYabiao,
         ImpWingWorldForge,
         ImpSpriteGrowth,
         ImpCharTemp,
         ImpFightForLove,
         ImpRandomTurnOverCard,
         ImpHuntGhost,
         ImpOneKeyConfig,
         ImpSchoolTop,
         ImpNewServerActivity,
         ImpHistoryConsumed,
         ImpArenaScore,
         ImpFTB,
         ImpWardrobeClient,
         ImpLuckyDraw,
         ImpTeamEndless,
         ImpSpriteChallenge,
         ImpCqzz,
         ImpGuanYin,
         ImpSecondSchoolClient,
         ImpWenYin,
         ImpHandInItem,
         ImpPuppet,
         ImpWingWorldCamp,
         ImpBattleFieldChaos,
         ImpMapGame,
         ImpClanWarCourier,
         ImpNpcFavor,
         ImpActivityCollect,
         ImpNewPlayerTreasureBox,
         ImpDoublePlantTree,
         ImpWorldBoss,
         ImpLunZhanYunDian)
        for inherit in inherits:
            AvatarMeta._moduleMixin(cls, name, inherit)

    def _moduleMixin(cls, name, module):
        for name, fun in inspect.getmembers(module, inspect.ismethod):
            setattr(cls, name, fun.im_func)

        for name, memb in inspect.getmembers(module):
            if name == '__module__':
                continue
            if memb.__class__.__name__ in const.BUILTIN_OBJS:
                setattr(cls, name, memb)


serverCallTimestamp = {}
DEFAULT_CELL_CALL_LIMIT_TIME = 0.2
excludeMethod = ['cell.startJumping',
 'base.chatToException',
 'cell.updateLocked',
 'cell.cancelAction',
 'cell.startQinggongState',
 'cell.endUpQinggongState']

class PropertyWrapper(object):

    def __init__(self, propertyName):
        self.roleName = None
        self.property = None
        self.propertyName = propertyName
        self.base = None

    def __getattribute__(self, name):
        propertyName = super(PropertyWrapper, self).__getattribute__('propertyName')
        attr = super(PropertyWrapper, self).__getattribute__('property')
        key = propertyName + '.' + name
        if key not in excludeMethod:
            lastTime = serverCallTimestamp.get(key, 0)
            diff = time.time() - lastTime
            if diff < DEFAULT_CELL_CALL_LIMIT_TIME:
                roleName = super(PropertyWrapper, self).__getattribute__('roleName')
                msg = 'call %s too many times, %s' % (key, roleName)
                gamelog.error('----', msg)
            serverCallTimestamp[key] = time.time()
        method = getattr(attr, name, None)
        gamelog.debug('----call', propertyName, name)
        return method


class Avatar(iCombatUnit.IAvatarCombatUnit):
    IsAvatar = True
    IsCombatUnit = True
    IsAvatarOrPuppet = True
    __metaclass__ = AvatarMeta

    def set_protectStatus(self, old):
        gamelog.debug('@hjx protectStatus#set_protectStatus:', old, self.protectStatus)

    def set_hidingPower(self, old):
        super(Avatar, self).set_hidingPower(old)
        if self == BigWorld.player():
            if self.realSchool == const.SCHOOL_YECHA:
                gameglobal.rds.ui.actionbar.setYeChaVisible(self.inHiding())
        pet = self._getPet()
        if pet:
            pet.refreshOpacityState()
        apEffectEx = getattr(self, 'apEffectEx', None)
        if apEffectEx:
            apEffectEx.resetEffect()

    def set_antiHidingPower(self, old):
        super(Avatar, self).set_antiHidingPower(old)

    def set_life(self, old):
        gamelog.debug('jorsef: Avatar#set_life', self.__class__)
        apEffectEx = getattr(self, 'apEffectEx', None)
        if apEffectEx:
            apEffectEx.set_life(old)
        p = BigWorld.player()
        self.resetTopLogo()
        if self.life == gametypes.LIFE_DEAD:
            self.set_hp(0)
            if self.topLogo and self.life != old:
                self.topLogo.updateRoleName(self.topLogo.name)
            if self == p:
                gameglobal.rds.ui.player.stopTweenMp()
                if gameglobal.rds.ui.quest.isShow:
                    gameglobal.rds.ui.npcPanel.hideNpcFullScreen()
                if gameglobal.rds.ui.npcV2.isShow:
                    gameglobal.rds.ui.npcV2.leaveStage()
            if hasattr(BigWorld.player(), 'getOperationMode') and BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE:
                if self == BigWorld.player().targetLocked:
                    BigWorld.player().unlockTarget()
        elif self.topLogo and self.life != old:
            if self.isInSSCorTeamSSC():
                self.topLogo.updateRoleName(const.SSC_ROLENAME)
                self.topLogo.setAvatarTitle(const.SSC_TITLENAME, 1)
            elif self.bHideFightForLoveFighterName():
                nameInfo = self.getFightForLoveNameInfo()
                self.topLogo.updateRoleName(nameInfo.get('name', ''))
                self.topLogo.setAvatarTitle(nameInfo.get('title', ''), 1)
            elif hasattr(p, 'checkAssassination') and p.checkAssassination(self):
                if hasattr(p, 'refreshAllUIName'):
                    self.refreshAllUIName()
            elif getattr(self, 'jctSeq', 0) and p.inClanCourier():
                self.topLogo.updateRoleName(self.getJCTRoleName())
                self.topLogo.setAvatarTitle('', 1)
            else:
                hasattr(self, 'refreshTopLogoName') and self.refreshTopLogoName()
                hasattr(self, 'refreshToplogoTitle') and self.refreshToplogoTitle()
                self.topLogo.updateRoleName(self.topLogo.name)
        if p.targetLocked == self:
            gameglobal.rds.ui.actionbar.checkSkillStatOnPropModified()
        if self.life == gametypes.LIFE_DEAD and p.id == self.id and p.isDoingAction:
            cellCmd.cancelAction(const.CANCEL_ACT_DEAD)
        if self.fashion.isPlayer:
            if self.life == gametypes.LIFE_DEAD and p.id == self.id and self.touchAirWallProcess == 1:
                gamelog.debug('jorsef: set_life, in touchAirWall, return', self.touchAirWallProcess)
                return
        self.clientLife(old)

    def set_camp(self, old):
        super(Avatar, self).set_camp(old)
        if self.topLogo:
            self.topLogo.updateRoleName(self.topLogo.name)
        self.refreshOpacityState()
        BigWorld.player().updateTargetFocus(self)

    def loadImmediately(self):
        val = super(Avatar, self).loadImmediately()
        if val:
            return val
        if gameglobal.rds.GameState > gametypes.GS_LOGIN:
            return BigWorld.player().isInBfDota()
        return False

    def set_tempCamp(self, old):
        super(Avatar, self).set_tempCamp(old)
        if self.topLogo:
            self.topLogo.updateRoleName(self.topLogo.name)
        BigWorld.player().updateTargetFocus(self)

    def set_inCombat(self, oldInCombat):
        if not self.fashion:
            return
        super(Avatar, self).set_inCombat(oldInCombat)
        if self.inCombat:
            if self.weaponState == gametypes.WEAPON_HANDFREE:
                self.switchWeaponState(gametypes.WEAPON_DOUBLEATTACH, False)
        elif not self.inWeaponCallback:
            if not (self.skillPlayer.inWeaponBuff or self.bufActState):
                self.switchWeaponState(gametypes.WEAPON_HANDFREE)
        p = BigWorld.player()
        if p.targetLocked == self:
            gameglobal.rds.ui.target.setCombatVisible(self.inCombat)
        if p.optionalTargetLocked == self:
            gameglobal.rds.ui.subTarget.setCombatVisible(self.inCombat)
        if p.isTeamLeaderByGbId(self.gbId):
            if self.inCombat:
                p.startGroupFollowAutoAttack()
            else:
                p.stopGroupFollowAutoAttack()
        if not p.isInBfDota() and getattr(self, 'topLogo', None) and not gameglobal.gHideAvatarBlood and not self.fashion.isPlayer:
            self.topLogo.showBlood(self.inCombat)
            if formula.spaceInWingWorldXinMoArena(formula.getAnnalSrcSceneNo(p.spaceNo)):
                if self.tempCamp == 1 or self.tempCamp == 2 and self != p:
                    self.topLogo.showBlood(True)
        if self.inCombat and self.fashion.doingActionType() in [ACT.BORED_ACTION]:
            self.fashion.stopAction()
        if self.inFly:
            self.qinggongMgr.stopWingFlyModelAction()
        BigWorld.player().updateTargetFocus(self)
        if self.inCombat and self == p:
            if self.summonedSpriteInWorld:
                self.summonedSpriteInWorld.updateSpriteLockTarget()

    def set_statesServerAndOwn(self, old):
        gamelog.debug('jorsef: set_statesServerAndOwn, ', self.__class__, old)
        super(Avatar, self).set_statesServerAndOwn(old)
        p = BigWorld.player()
        if self == p:
            gameglobal.rds.ui.actionbar.checkAllSkillMultiStat([gameglobal.SKILL_STAT_LACK_ENERGY, gameglobal.SKILL_STAT_SKILL_TGT])
        elif p.targetLocked == self:
            gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_LACK_ENERGY)

    def checkNeiYiBuff(self):
        p = BigWorld.player()
        if self._isHasState(self, const.SHOW_TO_ALL):
            return True
        states = self.getState(self, const.SHOW_TO_ONE)
        for state in states:
            if self != p and state and state[3] == p.id:
                return True

        return False

    def canOutline(self):
        p = BigWorld.player()
        if p and hasattr(p, 'isBianShenZaiJuInPUBG') and p.isBianShenZaiJuInPUBG(self):
            return False
        return super(Avatar, self).canOutline()

    def canChangeDiffuseInFocus(self):
        p = BigWorld.player()
        if p and hasattr(p, 'isBianShenZaiJuInPUBG') and p.isBianShenZaiJuInPUBG(self):
            return False
        return super(Avatar, self).canChangeDiffuseInFocus()

    def canChangeTgtCursorInFocus(self):
        p = BigWorld.player()
        if p and hasattr(p, 'isBianShenZaiJuInPUBG') and p.isBianShenZaiJuInPUBG(self):
            return False
        return super(Avatar, self).canChangeTgtCursorInFocus()

    def set_pkMode(self, old):
        p = BigWorld.player()
        if p == self:
            gameglobal.rds.ui.player.updatePKState(p.pkMode)
        elif self.topLogo:
            self.topLogo.updatePkTopLogo()
        if self.topLogo:
            self.topLogo.updateRoleName(self.topLogo.name)

    def set_pkStatus(self, old):
        if self.topLogo:
            self.topLogo.updateRoleName(self.topLogo.name)
        p = BigWorld.player()
        if p.targetLocked == self:
            p._updatePkTopLogo()
        self.refreshOpacityState()

    def set_lastPkTime(self, old):
        if self.topLogo:
            self.topLogo.updateAvatarPkColor()

    def set_inClanWar(self, old):
        if self.topLogo:
            self.topLogo.updateRoleName(self.topLogo.name)
            self.topLogo.gui.minAlpha = self.inClanWar
        p = BigWorld.player()
        if p.targetLocked and p.targetLocked == self:
            ufoType = ufo.UFO_NORMAL
            target = p.targetLocked
            if p.isEnemy(target):
                ufoType = self.getTargetUfoType(target)
            self.setTargetUfo(target, ufoType)

    def _getPlayersNeedToUpdatePkTopLogo(self, oldGroupNUID):
        p = BigWorld.player()
        if p.pkMode != const.PK_MODE_KILL:
            return []
        res = []
        if utils.instanceof(self, 'PlayerAvatar'):
            for en in BigWorld.entities.values():
                if en.__class__.__name__ == 'Avatar' and en.topLogo and en.groupNUID != 0 and en.groupNUID in (oldGroupNUID, p.groupNUID):
                    res.append(en)

        elif utils.instanceof(self, 'Avatar'):
            if self.topLogo and p.groupNUID != 0 and p.groupNUID in (oldGroupNUID, self.groupNUID):
                res.append(self)
        return res

    def set_groupNUID(self, old):
        p = BigWorld.player()
        pList = self._getPlayersNeedToUpdatePkTopLogo(old)
        if pList:
            p._updatePkTopLogo(pList)
        if p.targetLocked and p.targetLocked == self:
            ufoType = ufo.UFO_NORMAL
            target = p.targetLocked
            if p.isEnemy(target):
                ufoType = self.getTargetUfoType(target)
            self.setTargetUfo(target, ufoType)
        if old > 0 and self.groupNUID == 0:
            if self.topLogo and hasattr(self, 'groupMark'):
                for key, value in self.groupMark.items():
                    ent = BigWorld.entities.get(key)
                    if ent:
                        ent.topLogo.removeTeamLogo()

                self.groupMark = {}
        self.refreshOpacityState()
        if getattr(self, 'spriteObjId', None):
            ent = BigWorld.entity(self.spriteObjId)
            if ent:
                ent.refreshOpacityState()
        gameglobal.rds.ui.refreshTeamLogoOrIdentity(self.id)
        gameglobal.rds.littlemap.onLittleMapEnter(self)

    def set_groupIndex(self, old):
        self.refreshOpacityState()

    def setTargetUfo(self, target, ufoType):
        if target:
            if target.fashion and target.needAttachUFO():
                target.fashion.attachUFO(ufoType)
            if target.topLogo:
                target.topLogo.showSelector(*ufo.SELECTOR_ARGS_MAP[ufoType])

    def _setHpTeam(self):
        p = BigWorld.player()
        if p.inFubenTypes(const.FB_TYPE_ARENA):
            gameglobal.rds.ui.teamComm.setTeamHp(self.id, self.hp, self.mhp)
            gameglobal.rds.ui.teamEnemyArena.setTeamHp(self.id, self.hp, self.mhp)
        elif p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            gameglobal.rds.ui.teamComm.setTeamHp(self.id, self.hp, self.mhp)
            gameglobal.rds.ui.group.setGroupHp(self.id, self.hp, self.mhp)
        elif p.isInTeam() and p.isInMyTeam(self):
            gameglobal.rds.ui.teamComm.setTeamHp(self.id, self.hp, self.mhp)
        elif p.isInGroup() and p.isInMyTeam(self):
            gameglobal.rds.ui.teamComm.setTeamHp(self.id, self.hp, self.mhp)
            gameglobal.rds.ui.group.setGroupHp(self.id, self.hp, self.mhp)
        elif p.inFightObserve():
            gameglobal.rds.ui.teamComm.setTeamHp(self.id, self.hp, self.mhp)

    def getRealHp(self, v = None):
        if v is None:
            v = self.hpPercent
        return self.mhp * v / const.TOPLOGO_SCALE

    def getRealMp(self, v = None):
        if v is None:
            v = self.mpPercent
        return self.mmp * v / const.TOPLOGO_SCALE

    def onUpdateTargetLockedInfo(self, hp, mp):
        if hp != self.hp:
            self.hp = hp
            self.set_hp(hp)
        if mp != self.mp:
            self.mp = mp
            self.set_mp(mp)

    def set_hpOthers(self, old):
        self.hp = self.hpOthers
        self.set_hp(old)

    def set_mpOthers(self, old):
        self.mp = self.mpOthers
        self.set_mp(old)

    def set_hpPercent(self, old):
        if not (BigWorld.player().inHighLoadScene() and not gameglobal.rds.configData.get('enableTargetLockedUpdateInHighLoadScene')):
            targetLocked = BigWorld.player().targetLocked
            if targetLocked and targetLocked.id == self.id:
                return
        self.hp = self.getRealHp()
        self.set_hp(self.getRealHp(old))

    def set_mpPercent(self, old):
        if not (BigWorld.player().inHighLoadScene() and not gameglobal.rds.configData.get('enableTargetLockedUpdateInHighLoadScene')):
            targetLocked = BigWorld.player().targetLocked
            if targetLocked and targetLocked.id == self.id:
                return
        self.mp = self.getRealMp()
        self.set_mp(self.getRealMp(old))

    def set_hp(self, old):
        super(Avatar, self).set_hp(old)
        self._setHpTeam()
        clientcom.setDotaEntityBlood(self)

    def set_mhp(self, old):
        super(Avatar, self).set_mhp(old)
        self._setHpTeam()
        clientcom.setDotaEntityBlood(self)
        if self.topLogo:
            self.topLogo.setDotaHpMax(self.mhp)

    def set_hpHole(self, old):
        super(Avatar, self).set_hpHole(old)

    def _setMpTeam(self):
        p = BigWorld.player()
        if p.inFubenTypes(const.FB_TYPE_ARENA):
            gameglobal.rds.ui.teamComm.setTeamMp(self.id, self.mp, self.mmp)
            gameglobal.rds.ui.teamEnemyArena.setTeamMp(self.id, self.mp, self.mmp)
        elif p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            gameglobal.rds.ui.teamComm.setTeamMp(self.id, self.mp, self.mmp)
            gameglobal.rds.ui.group.setGroupMp(self.id, self.mp, self.mmp)
        elif p.isInTeam():
            gameglobal.rds.ui.teamComm.setTeamMp(self.id, self.mp, self.mmp)
        elif p.isInGroup():
            gameglobal.rds.ui.teamComm.setTeamMp(self.id, self.mp, self.mmp)

    def set_crossFromHostId(self, old):
        topLogo = getattr(self, 'topLogo', None)
        if topLogo and self.crossFromHostId:
            topLogo.updateRoleName(self.roleName)
            topLogo.removeGuildIcon()

    def set_crossServerGoal(self, old):
        pass

    def setCrossToHostId(self, hostId):
        self.crossToHostId = hostId

    def set_mp(self, old):
        super(Avatar, self).set_mp(old)
        self._setMpTeam()
        if self.topLogo:
            self.topLogo.onUpdateMp()

    def set_mmp(self, old):
        super(Avatar, self).set_mmp(old)
        self._setMpTeam()
        if self.topLogo:
            self.topLogo.onUpdateMp()

    def _getAspect(self):
        if self == BigWorld.player():
            return self.__dict__['aspect']
        elif gameglobal.rds.GameState > gametypes.GS_LOGIN and self.pubAspect.isEmpty():
            return self.miniAspect
        else:
            return self.pubAspect

    def _setAspect(self, value):
        if self == BigWorld.player():
            self.__dict__['aspect'] = value
        else:
            self.pubAspect = value

    aspect = property(_getAspect, _setAspect, None, '')

    def _getSpeed(self):
        if self.isRealGroupFollow() and self.isGroupSyncSpeed():
            return self.followSpeed
        else:
            return self.__dict__['speed']

    def _setSpeed(self, value):
        if getattr(self, 'inGroupFollow', None):
            self.followSpeed = value
        else:
            self.__dict__['speed'] = value

    speed = property(_getSpeed, _setSpeed, None, '')

    @property
    def realAspect(self):
        if self._isSchoolSwitch():
            return self.switchedAspect
        elif not self.switchedAspect.isEmpty():
            return self.switchedAspect
        elif self == BigWorld.player():
            hackAspect = aspectHelper.getInstance().hackAspect(self.aspect)
            return hackAspect
        else:
            return self.aspect

    @property
    def mapID(self):
        return formula.getMapId(self.spaceNo)

    @property
    def realPhysique(self):
        if self._isSchoolSwitch():
            return self.switchedPhysique
        else:
            return self.physique

    @property
    def realSchool(self):
        if self._isSchoolSwitch():
            return self.switchedSchool
        else:
            return self.school

    @property
    def socialSchool(self):
        return self.curSocSchool

    @property
    def realLv(self):
        p = BigWorld.player()
        if not self.inWorld:
            return 1
        fbNo = formula.getFubenNo(p.spaceNo)
        arenaMode = formula.fbNo2ArenaMode(fbNo)
        if self.rebalanceMode:
            methodID, factor = self.getMethodFactorByModeID(gametypes.REBALANCE_SUBSYS_ID_LV, self.rebalanceMode)
            if self.rebalanceMode:
                if methodID == const.REBALANCE_METHOD_1_UPLIMIT:
                    return min(factor, self.lv)
                if methodID == const.REBALANCE_METHOD_2_SETVALUE:
                    return factor
                return self.lv
        if self._isSchoolSwitch():
            return self.switchedLv
        elif p.inFubenTypes(const.FB_TYPE_ARENA) and AMD.data.get(arenaMode, {}).get('needReCalcLv', 0):
            return formula.calcArenaLv(arenaMode, p.lv)
        elif self.inFuben() and self.fbGuideEffect == const.GUIDE_MASTER_MODE:
            fbNo = formula.getFubenNo(self.spaceNo)
            fd = FD.data[fbNo]
            if fd.get('recommendLv', 0):
                return fd.get('recommendLv', 0)
            return self.lv
        elif self.inMLSpace() and MDD.data.get(formula.getMLGNo(self.spaceNo), {}).has_key('digongLv'):
            return MDD.data[formula.getMLGNo(self.spaceNo)]['digongLv']
        else:
            return self.lv

    def realLvByCause(self, cause):
        if cause == gametypes.REAL_LV_DEFAULT:
            return self.realLv
        if cause in (gametypes.REAL_LV_EQUIPMENT, gametypes.REAL_LV_PROPERTY):
            if self._isSchoolSwitch():
                return self.switchedLv
            else:
                return self.lv

    @property
    def wushuang(self):
        return {gametypes.WS_TYPE_1: self.wushuang1,
         gametypes.WS_TYPE_2: self.wushuang2}

    @property
    def tCamp(self):
        return self.tempCamp

    def _getAvatarConfig(self):
        if self == BigWorld.player():
            return self.__dict__['avatarConfig']
        else:
            return self.pubAvatarConfig

    def _setAvatarConfig(self, value):
        if self == BigWorld.player():
            self.__dict__['avatarConfig'] = value
        else:
            self.pubAvatarConfig = value

    avatarConfig = property(_getAvatarConfig, _setAvatarConfig, None, '')

    @property
    def realAvatarConfig(self):
        if self._isSchoolSwitch():
            if not self.switchAvatarConfig:
                self.switchAvatarConfig = self._getSchoolSwitchAvatarConfig()
            return self.switchAvatarConfig
        else:
            return self.avatarConfig

    @property
    def maxVp(self):
        return int(VLD.data.get(self.lv, {}).get('maxVp', 0) + self.vpAdd[2])

    @property
    def realInv(self):
        if self._isSoul() and gameglobal.rds.configData.get('enableCrossServerBag', False):
            return self.crossInv
        return self.inv

    @property
    def realRoleName(self):
        if self._isSoul():
            return utils.parseRoleNameFromCrossName(self.roleName)
        return self.roleName

    @property
    def schoolSwitchName(self):
        if self._isSchoolSwitch():
            name = SSGD.data.get(self.schoolSwitchNo, {}).get('name', None)
            if name:
                return name
        return self.realRoleName

    def getOriginHostId(self):
        return self.crossFromHostId or utils.getCurrHostId()

    def getCountryId(self):
        if gameconfigCommon.enableWingWorldWarCampMode():
            return self.wingWorldCamp
        else:
            return self.getOriginHostId()

    def __init__(self):
        super(Avatar, self).__init__()
        self.topLogo = utils.MyNone
        self.questLogo = utils.MyNone
        self.rider = None
        self.waterHeight = 0
        self.flyHeight = 3000
        self.keyEventMods = None
        self.modelServer = modelServer.AvatarModelServer(self)
        self.exception = None
        self.serverBootTime = 0
        self.clientBootTime = 0
        self.jumpState = 0
        self.isDashing = False
        self.dashNormalJump = False
        self.dashingStartTime = 0
        self.dashingInitTime = 0
        self.dashingJumpStartTime = 0
        self.isJumping = False
        self.isFalling = False
        self.bufActState = None
        self.buffModelScale = None
        self.buffIdModelScale = None
        self.jumpActionMgr = impJumpFashion.JumpActionManager(self.id)
        self.qinggongMgr = qingGong.QingGongMgr(self.id)
        self.bianshenStateMgr = bianshenState.BianshenStateMgr(self.id)
        self.fishingMgr = None
        self.inWeaponCallback = None
        self.inWingTakeOff = False
        self.takeOffActionPlayed = True
        self.partsUpdating = False
        self.isChangeMasterMonsterPart = False
        self.inForceNavigate = False
        self.delayHangupWeapon = False
        self.inWenQuanState = False
        self.actionProgressCallback = None
        self.initDelegations()
        self.skillFlagState = FlagStateCommon()
        self.flagStateCommon = FlagStateCommon()
        self.switchAvatarConfig = None
        self.interactiveRangeEntered = False
        self.canSelectWhenHide = True
        self.needPlayIntro = False
        self.needConfigOp = False
        self.isInsideWater = False
        self.createUsedZaijuData = {}
        self.leavedZaiju = {}
        self.holdZaijuModel = {}
        self.oldCarrier = {}
        self.oldWingWorldCarrier = {}
        self.enterCCRoomInfo = []
        self.needKeepCCRoomInfo = None
        self.applyTimeDict = {}
        self.itemClientEffects = {}
        self.equipEnhanceEffects = []
        self.horseGroundMoveEffects = []
        self.horseDashEffects = []
        self.flyMoveEffects = []
        self.flyDashEffects = []
        self.isDoingAction = False
        self.guildConnectEffectCB = None
        self.apprenticeBeTrainId = None
        self.rideTogetherDownHorse = False
        self.lastSwitchPKModeStamp = 0
        self.activityStateIds = []
        self.noticeShow = False
        self.intimacyInterEffects = []
        self.teleportSpellEffs = []
        self.interactiveSpecialIdleCB = None
        self.bufNoJump = False
        self.inMeiHuo = False
        self.inFear = False
        self.inChaoFeng = False
        self.faceEmoteExpire = {}
        self.faceEmoteXmlInfo = {}
        self.apprenticeInfo = {}
        self.apprenticeVal = {}
        self.apprenticeGbIds = []
        self.waBaoResuletItem = None
        self.waBaoLoopEff = []
        self.waBaoUsingItemId = None
        self.interactiveActionId = None
        self.sprintStartCB = None
        self.sprintSpeeding = False
        self.backMove = False
        self.stateForceSyncTime = 0
        self.expXiuWei = 0
        self.wearEffectConnect = None
        self.avatarDanDaoCB = None
        self.avatarDanDaoCancelCB = None
        self.spriteObjId = 0
        self.spriteBattleIndex = 0
        self.lastSpriteBattleIndex = 0
        self.spriteExtraDict = {}
        self.statesClientAndOwn = {}
        self.battleFiedlOccupyInfo = {}
        self.battleFiedlMonstersPos = {}
        self.battleFieldZaijus = {}
        self.fbAvoidDieItemCnt = 0
        self.groupChatData = {}
        self.groupUnreadMsgs = {}
        self.skillCastDelayCallback = None
        self.skillCastDelayInfo = []
        self.wingHorseIdleEffect = {}
        self.trialActEffectDict = {}
        self.stateSECount = {}
        self.trialEffectCallback = None
        self.apEffectEx = physicsEffect.PhysicsEffectMgrEx(self)
        self.inChangeGravity = False
        self.chcheGravity = None

    def onReturnToCharacterSelectPanel(self):
        pass

    def prerequisites(self):
        return []

    def needHideEntity(self):
        if self != BigWorld.player():
            spaceNo = getattr(BigWorld.player(), 'spaceNo', 0)
            mapId = formula.getMapId(spaceNo)
            if MCD.data.get(mapId, {}).get('hideAvatar', 0):
                return True
            if self.isolateType in gametypes.TEL_ISOLATE_TYPES:
                return True
        return False

    def getOpacityValue(self):
        scenarioIns = scenario.Scenario.PLAY_INSTANCE if scenario.Scenario.PLAY_INSTANCE else scenario.Scenario.INSTANCE
        if scenarioIns and self.isPlayingAmericanMarriageScenario() and self.isWifeOrHusband():
            return (gameglobal.OPACITY_FULL, True)
        if scenarioIns and self.isPlayingFightForLoveScenario() and self.isFightForLoveScenarioActor():
            return (gameglobal.OPACITY_FULL, True)
        if gameglobal.rds.GameState == gametypes.GS_LOGIN and (gameglobal.rds.loginScene.inSelectStage() or gameglobal.rds.loginScene.inBodyTypeStage()):
            return (gameglobal.OPACITY_HIDE, False)
        p = BigWorld.player()
        if formula.inDotaBattleField(getattr(p, 'mapID', 0)) and not getattr(self, 'bianshen', (0, 0))[1] and not getattr(p, 'backToBfEnd', False):
            return (gameglobal.OPACITY_HIDE, False)
        if self.gbId != getattr(p, 'gbId', 0) and self.inPUBGPlane():
            return (gameglobal.OPACITY_HIDE, False)
        if self.needHideEntity():
            return (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, False)
        if self.isInCoupleRide() and self.isInCoupleRideAsRider():
            noAttachModel = CEBD.data.get(self.coupleEmote[0], {}).get('noAttachModel')
            if not noAttachModel:
                if gameglobal.gHideOtherPlayerFlag == gameglobal.HIDE_DEFINE_SELF and not gameglobal.HIDE_MODE_CUSTOM_SHOW_TOPLOGO:
                    return (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, False)
                return (gameglobal.OPACITY_HIDE_WITHOUT_NAME, True)
        if self.inCarrousel():
            return (gameglobal.OPACITY_HIDE_WITHOUT_NAME, True)
        if self.isRidingTogether() and self.isRidingTogetherAsVice():
            if gameglobal.gHideOtherPlayerFlag == gameglobal.HIDE_DEFINE_SELF and not gameglobal.HIDE_MODE_CUSTOM_SHOW_TOPLOGO:
                return (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, False)
            return (gameglobal.OPACITY_HIDE_WITHOUT_NAME, True)
        if getattr(self, 'gmFollow', 0):
            return (gameglobal.OPACITY_HIDE, False)
        if self.inFlyTypeObserver():
            return (gameglobal.OPACITY_HIDE, False)
        if self.carrier.has_key(self.id):
            cEnt = self.carrier.getCarrierEnt()
            if cEnt:
                return cEnt.getOpacityValue()
        if getattr(self, 'assassinationTeleport', 0):
            if self.gbId != BigWorld.player().gbId:
                return (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, False)
        return super(Avatar, self).getOpacityValue()

    def setTargetCapsUse(self, canUse):
        super(Avatar, self).setTargetCapsUse(canUse)
        if canUse:
            if self.isOnWingWorldCarrier():
                self.targetCaps = []

    def enterWorld(self):
        self.syncSubProps()
        if not hasattr(self, 'hp'):
            if hasattr(BigWorld.player(), 'inHighLoadScene') and BigWorld.player().inHighLoadScene() and gameglobal.rds.configData.get('enableHpMpOptimization', False):
                self.hp = self.getRealHp()
            else:
                self.hp = self.hpOthers
        if not hasattr(self, 'mp'):
            if hasattr(BigWorld.player(), 'inHighLoadScene') and BigWorld.player().inHighLoadScene() and gameglobal.rds.configData.get('enableHpMpOptimization', False):
                self.mp = self.getRealMp()
            else:
                self.mp = self.mpOthers
        self.aspectOld = copy.deepcopy(self.aspect)
        self.serverSignal = self.signal
        self.physiqueOld = copy.deepcopy(self.physique)
        if gameglobal.rds.isSinglePlayer:
            self.filter = BigWorld.AvatarDropFilter()
        elif gameglobal.rds.GameState <= gametypes.GS_LOGIN:
            self.filter = BigWorld.ClientFilter()
        else:
            self.filter = BigWorld.AvatarFilter()
        self.resetClientYawMinDist()
        if hasattr(BigWorld.player(), 'mapID') and BigWorld.player().mapID == const.ML_SPACE_NO_WENQUAN_FLOOR1:
            self.inWenQuanState = True
        self.calcInteractiveChangeFashionId()
        if gameglobal.rds.isSinglePlayer:
            self.school = gameglobal.rds.school
            if len(self.roleName) == 0:
                self.roleName = '单机测试'
                self.titleName = '测试我的称谓'
            self.fashion = fashion.Fashion(self.id)
            self.fashion.loadDummyModel()
            self.modelServer.bodyModel = self.model
            self.modelServer.bodyUpdate()
        else:
            self.fashion = fashion.Fashion(self.id)
            self.fashion.loadDummyModel()
            self.modelServer.setUrgent(self.isUrgentLoad())
            self.modelServer.bodyModel = self.model
            clientcom.fetchTintEffectsContents(self.id, self.afterSetTintEffects)
        self.skillId = 1
        self.skillLevel = 1
        self.isFlyLeftWeapon = False
        self.isFlyRightWeapon = False
        self.chargeSkillId = None
        self.chargeSkillLv = None
        self.isUseQingGong = False
        self.sharedCnt = 0
        gameglobal.rds.littlemap.onLittleMapEnter(self)
        self.clientLife(self.life)
        self.handClimb = commcalc.getSingleBit(self.signal, gametypes.SIGNAL_HAND_CLIMB)
        self.showBackWaist = commcalc.getSingleBit(self.signal, gametypes.SIGNAL_SHOW_BACK)
        if hasattr(self, 'groupNUID') and self.groupNUID > 0 and self.groupNUID == BigWorld.player().groupNUID:
            gameglobal.rds.ui.group.setGroupHp(self.id, self.hp, self.mhp)
        if self._isOnZaiju():
            zjNo = self._getZaijuNo()
            ezd = EZD.data.get(zjNo, {})
            if ezd.get('isYabiao'):
                self.addYabiaoPot()
        p = BigWorld.player()
        gamelog.debug('@lhb enterWorld', formula.inDotaBattleField(getattr(p, 'mapID', 0)))
        if formula.inDotaBattleField(getattr(p, 'mapID', 0)):
            gamelog.debug('@lhb in dota')
            p.bfDotaEntityIdRecord.setdefault(const.DOTA_ENTITY_TYPE_LITTLE_MAP, set()).add(self.id)
            if getattr(self, 'tempCamp', 0) != getattr(p, 'tempCamp', 0):
                if not getattr(self, 'vehicleId', None):
                    gamelog.debug('@lhb in dota is enemy')
                    not clientcom.bfDotaAoIInfinity() and p.cell.onEnemyEnterRangeInBattleFieldDota(self.id)
                self.resetDotaLvRecord()
            elif self.id != p.id:
                p.selfSideDotaEntityIdSet.add(self.id)
        if self.carrier.isReadyState():
            self.enterTopLogoRange()
            self.resetCarrierReadyEmote({})
        if p.IsAvatar and self.gbId in p.members and self.id != p.id:
            p.cell.reqAddSubscribee(self.id, False, False)
        if clientcom.bfDotaAoIInfinity():
            self.notifyTeleportDist = gameglobal.NOTIFY_TELEPORT_DIST
        if self.id in gameglobal.rds.spriteOwnerDict:
            self.spriteObjId = gameglobal.rds.spriteOwnerDict[self.id]
        self.dotaLogList = []
        if p.IsAvatar:
            p.aoiAvatarCnt += 1
        if hasattr(p, 'operation') and not p.operation['commonSetting'][17] and p.inWingCity() and p.aoiAvatarCnt >= WWCD.data.get('autoArmorModeAvatarCnt', 100):
            uiUtils.enabledClanWarArmorMode()
        self.skillAppearancesDetail = SkillAppearancesDetail(self)
        if gameglobal.rds.GameState > gametypes.GS_LOGIN:
            self._setMpTeam()
            self._setHpTeam()

    def resetDotaLvRecord(self):
        p = BigWorld.player()
        if self.id != p.id:
            if not hasattr(p, 'bfDotaLvRecord'):
                p.bfDotaLvRecord = {}
            p.bfDotaLvRecord[self.gbId] = max(p.bfDotaLvRecord.get(self.gbId, 1), self.battleFieldDotaLv)

    def calcInteractiveChangeFashionId(self):
        self.interactiveChangeFashionId = 0
        interactiveObjectId = getattr(self, 'interactiveObjectId', 0)
        if interactiveObjectId:
            changeFashionData = ID.data.get(interactiveObjectId, {}).get('changeFashion', {})
            changeFashionId = changeFashionData.get((self.physique.sex, self.physique.bodyType), 0)
            self.interactiveChangeFashionId = changeFashionId

    def afterSetTintEffects(self, ownerId, tintAvatarTas, tintAvatarName, tintEffects):
        if not self.inWorld:
            return
        clientcom.tintSectionsToCache(self, tintAvatarTas, tintAvatarName, tintEffects)
        self.modelServer.bodyUpdate()
        self.modelServer.weaponUpdate()
        self.modelServer.wearUpdate()
        if not self.inWenQuanState:
            self.modelServer.horseUpdate()
            self.modelServer.wingFlyModelUpdate()
            self.modelServer.enterBooth()

    def isUrgentLoad(self):
        if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
            return True
        return False

    def leaveWorld(self):
        if self.attachSkillData:
            if self.attachSkillData[0] == BigWorld.player().id:
                self.modelServer.leaveAttachSkill(BigWorld.player().id, self.id)
            if self.attachSkillData[1] == BigWorld.player().id:
                self.modelServer.leaveAttachSkill(self.id, BigWorld.player().id)
        if self.belongToRoundTable:
            self.modelServer.leaveRoundTable(self.belongToRoundTable)
        if self.interactiveObjectEntId:
            self.modelServer.leaveInteractiveObject(self.interactiveObjectEntId)
        if self.isGuildSitInChair():
            self.guildLeaveChair()
        if self.inMultiCarrier():
            carrierEntId = self.carrier.carrierEntId
            carrierEnt = BigWorld.entities.get(carrierEntId, None)
            self.modelServer.leaveCarrier(carrierEnt)
        super(Avatar, self).leaveWorld()
        if gameglobal.rds.GameState > gametypes.GS_LOGIN and self.isRealModel and self.id != BigWorld.player().id:
            seqTask.modelMemoryCtrl().decAvatarModel()
        if self.inFishing() and self.fishingMgr:
            self.fishingMgr.release()
            self.fishingMgr = None
        self.modelServer.release()
        self.modelServer = None
        self.isMoving = False
        self.isUseQingGong = False
        self.jumpActionMgr = None
        self.qinggongMgr = None
        self.model = None
        for m in self.models[:]:
            if m:
                self.delModel(m)

        if hasattr(BigWorld.player(), 'targetLocked') and BigWorld.player().targetLocked == self:
            BigWorld.player().unlockTarget()
        if hasattr(self, 'boothStat') and self.boothStat == const.BOOTH_STAT_OPEN and gameglobal.rds.ui.booth.otherBoothInfo:
            if gameglobal.rds.ui.booth.otherBoothInfo[0] == self.id:
                gameglobal.rds.ui.booth.hide()
        self.leaveInteractiveRange()
        self.itemClientEffects = {}
        gameglobal.rds.littlemap.onLittleMapLeave(self)
        self.releaseHorseWingEffect()
        gamelog.debug('@lhb leaveWorld', self.inFubenType(const.FB_TYPE_BATTLE_FIELD_DOTA))
        p = BigWorld.player()
        if formula.inDotaBattleField(getattr(p, 'mapID', 0)):
            entitySet = p.bfDotaEntityIdRecord.get(const.DOTA_ENTITY_TYPE_LITTLE_MAP, set())
            entitySet and self.id in entitySet and entitySet.remove(self.id)
            if getattr(p, 'tempCamp', 0) != getattr(self, 'tempCamp', 0):
                if not clientcom.bfDotaAoIInfinity():
                    self.cell.onMyLeaveRangeInBattleFieldDota()
                self.resetDotaLvRecord()
            elif p.id != self.id and self.id in getattr(p, 'selfSideDotaEntityIdSet', []):
                p.selfSideDotaEntityIdSet.remove(self.id)
        if self.wearEffectConnect:
            self.wearEffectConnect.release()
        self.oldCarrier = {}
        self.oldWingWorldCarrier = {}
        self.checkGmFollowLeaveWorld()
        self.delYaBiaoAttackerEffect()
        if p and hasattr(p, 'aoiAvatarCnt'):
            p.aoiAvatarCnt = max(0, p.aoiAvatarCnt - 1)
        if hasattr(self, 'skillAppearancesDetail'):
            self.skillAppearancesDetail.clear()
        self.apEffectEx.stopAllEffect()
        if self.trialEffectCallback:
            BigWorld.cancelCallback(self.trialEffectCallback)
            self.trialEffectCallback = None

    def checkGmFollowLeaveWorld(self):
        p = BigWorld.player()
        mapID = getattr(p, 'mapID', 0)
        isInGuildTournament = formula.isNativeGuildTournament(mapID) or formula.isCrossServerGuildTournament(mapID) or formula.isRankGuildTournament(mapID)
        if hasattr(p, 'gmFollow') and p.gmFollow == self.id:
            if p.isInBfDota() or isInGuildTournament or p.isInPUBG():
                p.physics.followTarget = None
                if hasattr(p, 'modelServer') and hasattr(p.modelServer, 'leaveGmFollow'):
                    p.modelServer.leaveGmFollow()
                BigWorld.callback(2, gameglobal.rds.ui.fightObserve.autoObSpecificTgb)
            elif mapID in const.GUILD_FUBEN_NOS:
                if hasattr(p, 'cell') and hasattr(p.cell, 'freeModeOb'):
                    p.cell.freeModeOb()
                if hasattr(p, 'cell') and hasattr(p.cell, 'obSpecificTgt'):
                    BigWorld.callback(2, Functor(p.cell.obSpecificTgt, self.id))

    def enterTopLogoRange(self, rangeDist = -1):
        if not self.firstFetchFinished:
            return
        opValue = self.getOpacityValue()
        if opValue[0] in gameglobal.OPACITY_HIDE_TOPLOGO and not opValue[1] and not BigWorld.player().isInBfDota():
            return
        if self.needHideEntity():
            return
        super(Avatar, self).enterTopLogoRange(rangeDist)
        if self.topLogo:
            opValue = self.getOpacityValue()
            if opValue[0] in (gameglobal.OPACITY_HIDE, gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE_WITHOUT_NAME):
                if opValue[1]:
                    self.hide(True, opValue[1])
            self.refreshTopLogo()
            p = BigWorld.player()
            if self == p:
                self.topLogo.hideName(gameglobal.gHidePlayerName)
                self.topLogo.hideAvatarTitle(gameglobal.gHidePlayerTitle)
            else:
                self.topLogo.hideName(gameglobal.gHideAvatarName)
                self.topLogo.hideAvatarTitle(gameglobal.gHideAvatarTitle)
            if not gameglobal.rds.configData.get('enableNewCamera', False):
                if gameglobal.rds.ui.camera.isShow and gameglobal.rds.ui.camera.isHideAllUI and (p.isInTeam() or p.isInGroup()):
                    p.hideAllTeamTopLogo(True)
            elif gameglobal.rds.ui.cameraV2.isShow and gameglobal.rds.ui.cameraV2.isHideAllUI and (p.isInTeam() or p.isInGroup):
                p.hideAllTeamTopLogo(True)

    def enterInteractiveRange(self, rangeDist = -1):
        if self.needHideEntity():
            return
        p = BigWorld.player()
        if hasattr(p, 'checkAvatarRange'):
            p.checkAvatarRange(self, True)
        forceShow = False
        if formula.inHuntBattleField(p.mapID) and p._isHasState(self, const.BATTLE_FIELD_HUNT_IN_TRAP_BUFF):
            forceShow = True
        if hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE or forceShow:
            if self.getOpacityValue()[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE, gameglobal.OPACITY_HIDE_WITHOUT_NAME):
                return
            if self.carrier and self.id in self.carrier:
                return
            self.interactiveRangeEntered = True
            BigWorld.player().enterInteractiveCallback(self)

    def leaveInteractiveRange(self, rangeDist = -1):
        p = BigWorld.player()
        if hasattr(p, 'checkAvatarRange'):
            p.checkAvatarRange(self, False)
        if self.interactiveRangeEntered:
            self.interactiveRangeEntered = False
            BigWorld.player().leaveInteractiveCallback(self)

    def enterLoadModelRange(self, rangeDist = -1):
        pass

    def callClientMethod(self, methodName, methodArgs):
        if not hasattr(self, methodName):
            return
        getattr(self, methodName)(*methodArgs)

    def inGuildSpace(self, gsNo_ = 0):
        if self.spaceNo <= 0:
            return False
        if not formula.spaceInGuild(self.spaceNo):
            return False
        if gsNo_ and formula.getGuildSceneNo(self.spaceNo) != gsNo_:
            return False
        return True

    def reloadModel(self):
        if self.modelServer.bodyUpdateStatus != modelServer.BODY_UPDATE_STATUS_NORMAL:
            return
        self.modelServer.setUrgent(True)
        clientcom.fetchTintEffectsContents(self.id, self.afterSetTintEffects)

    def checkStatus(self):
        gamelog.debug('zf:checkStatus..........................', self.id, self.roleName, self.life, self.model.scale)
        self.clientLife(self.life)
        self.autoSetRenderFlag()
        self.fashion.setGuard(self.inCombat)
        if self.inFly:
            self.resetFly(False)
        self.resetTopLogo()
        if self.hidingPower:
            self.resetHiding()

    def getTargetUfoType(self, target):
        p = BigWorld.player()
        ufoType = ufo.UFO_NORMAL
        if target.IsCreation:
            if hasattr(target, 'ownerId') and BigWorld.entity(target.ownerId):
                target = BigWorld.entity(target.ownerId)
            else:
                return ufoType
        if getattr(target, 'atkType', const.MONSTER_ATK_TYPE_NO_ATK) == const.MONSTER_ATK_TYPE_ACTIVE_RANGE_ATK or hasattr(target, 'avatarInstance'):
            ufoType = ufo.UFO_ATK_ENEMY
        elif target.IsFragileObject:
            ufoType = ufo.UFO_PASSIVE_ENEMY
        elif target.IsNaiveCombatUnit:
            ufoType = ufo.UFO_ATK_ENEMY
        elif getattr(target, 'inCombat', False):
            ufoType = ufo.UFO_ATK_ENEMY
        else:
            ufoType = ufo.UFO_PASSIVE_ENEMY
        if self.inMLYaoLiSpace():
            mlRelation = (self._mlSpaceForceWithMonster(self), self._mlSpaceForceWithMonster(target))
            if all(mlRelation):
                ufoType = ufo.UFO_NORMAL
        if getattr(target, 'isFlyMonster', False) or getattr(target, 'isJumping', False) or getattr(target, 'inFly', False) or getattr(target, 'inSwim', False):
            ufoType = ufoType + 1
        if isinstance(target, VirtualMonster):
            ufoType = ufo.UFO_NULL
        if p.isBianShenZaiJuInPUBG(target):
            ufoType = ufo.UFO_NULL
        return ufoType

    def clientLife(self, old):
        p = BigWorld.player()
        self.updateBodySlope()
        self.resetClientYawMinDist()
        if self.life == gametypes.LIFE_ALIVE:
            self.updateModelFreeze(-1.0)
            if hasattr(self.filter, 'disableSmooth'):
                self.filter.disableSmooth = False
            if self.model != None and len(self.model.motors) > 0:
                self.model.motors[0].matcherCoupled = True
            if old == gametypes.LIFE_DEAD:
                self.skillPlayer.castLoop = False
                SummonActionName = self.fashion.action.getSummonAction(self.fashion)
                if SummonActionName:
                    self.fashion.playAction([SummonActionName], action.STANDUP_ACTION)
                    duration = 0
                    try:
                        duration = self.model.action(SummonActionName).duration
                    except:
                        pass

                    BigWorld.callback(duration + 0.1, Functor(self.resetTopLogoAfterAction, self))
                else:
                    self.fashion.stopAllActions()
            if self == p:
                self.restoreGravity()
                self.touchAirWallProcess = 0
            self.resetShadowUfo()
        elif self.life == gametypes.LIFE_DEAD:
            if hasattr(self.filter, 'disableSmooth'):
                self.filter.disableSmooth = True
            if self.fashion.doingActionType() == action.DEAD_ACTION:
                return
            if self == p:
                if getattr(self, 'ap', None):
                    self.ap.stopMove()
            self.qinggongMgr.actionType = gametypes.QINGGONG_ACT_DEFAULT
            self.jumpState = gametypes.DEFAULT_JUMP
            self.fashion.stopAllActions()
            dieActionName = self.fashion.getDieActionName()
            dieIdleName = self.fashion.getDeadActionName()
            if dieActionName != None and dieIdleName != None:
                if self.model.freezeTime > 0:
                    self.updateModelFreeze(-1.0)
                if self.life == old:
                    self.fashion.playAction([dieIdleName], action.DEAD_ACTION, self.afterDieAction, 0)
                else:
                    self.fashion.playAction([dieActionName, dieIdleName], action.DEAD_ACTION, self.afterDieAction, 0)
            else:
                gamelog.error('Error:, can not find die action ', dieActionName, dieIdleName, self.model.sources)
            if self == p:
                reliveHereEnable = not (self.touchAirWallProcess > 0 or self.downCliff > 0)
                spaceNo = formula.getMapId(self.spaceNo)
                reliveHereType = MCD.data.get(spaceNo, {}).get('reliveHereType', gametypes.RELIVE_HERE_TYPE_FORBID)
                if uiUtils.isInFubenShishenLow():
                    reliveHereType = gametypes.RELIVE_HERE_TYPE_NORMAL
                reliveHereEnable = reliveHereEnable and reliveHereType != gametypes.RELIVE_HERE_TYPE_FORBID
                reliveNearEnable = self.canReliveNear and (not MCD.data.get(spaceNo, {}).get('forbidReliveNear', 0) or self.touchAirWallProcess > 0)
                if self.isInSSCorTeamSSC():
                    gameglobal.rds.ui.deadAndRelive.show(False, reliveNearEnable, False, None, reliveHereType)
                elif not self.bHideFightForLoveFighterName():
                    gameglobal.rds.ui.deadAndRelive.show(reliveHereEnable, reliveNearEnable, False, None, reliveHereType)
                else:
                    reliveTime = FFLCD.data.get('reliveTime', 10)
                    gameglobal.rds.ui.player.setReliveCountDown(reliveTime)
                if self.inFubenTypes(const.FB_TYPE_GROUP_SET) and not self.canReliveNear:
                    gameglobal.rds.ui.deadAndRelive.tip = 'BOSS战中暂时无法使用'
                else:
                    gameglobal.rds.ui.deadAndRelive.tip = ''

    def errorMessage(self, msg):
        self.chatToEventEx(msg, 0)

    def combatMessagePb(self, bytes):
        num, data, dmg, toall = combatProto.combatMessageProtoClient(bytes)
        if toall:
            self.showGameMsg(num, data)
        elif dmg:
            self.combatMessageDamage(num, data, dmg)
        else:
            self.showGameMsg(num, data)

    def combatMessage(self, num, data):
        self.chatToEventEx(data, 0)

    def combatMessageDamage(self, num, data, damage):
        self.chatToEventEx(data, 0)

    def use(self):
        p = BigWorld.player()
        if p.canBeAttack(self):
            p.beginAttack(self)
        elif self.inBoothing():
            if self == BigWorld.player():
                gameglobal.rds.ui.booth.show()
            else:
                self.cell.queryBooth()
        elif self.chatRoomName:
            if self != p and not p.chatRoomNUID:
                p.cell.joinChatRoom(self.chatRoomNUID, '')
        elif p.getOperationMode() == gameglobal.ACTION_MODE:
            if self == p.targetLocked:
                gameglobal.rds.ui.target.showRightMenu(uiConst.MENU_TARGET, self.crossFromHostId)
        else:
            gameglobal.rds.ui.target.showRightMenu(uiConst.MENU_TARGET, self.crossFromHostId)

    def interactive(self):
        if gameglobal.rds.ui.pressKeyF.interactiveAvatars:
            hostId = None
            if self._isSoul():
                hostId = self.crossFromHostId
            elif BigWorld.player()._isSoul():
                hostId = BigWorld.player().crossToHostId
            gameglobal.rds.ui.target.showRightMenu(uiConst.MENU_TARGET, hostId)

    def dispatchClient(self, funcFlag, funcArgs):
        func = funcMapOfClient[funcFlag]
        func(self, *funcArgs)

    def playerRelation(self, tgt):
        if tgt.fashion.isPlayer:
            return gametypes.RELATION_FRIENDLY
        elif self.isEnemy(tgt):
            return gametypes.RELATION_ENEMY
        else:
            return gametypes.RELATION_FRIENDLY

    def onTargetCursor(self, enter):
        if self.inBoothing():
            if enter:
                if ui.get_cursor_state() == ui.NORMAL_STATE:
                    ui.set_cursor_state(ui.TARGET_STATE)
                    if (self.position - BigWorld.player().position).length > const.MAKE_BOOTH_DIST:
                        ui.set_cursor(cursor.booth_dis)
                    else:
                        ui.set_cursor(cursor.booth)
                    ui.lock_cursor()
            elif ui.get_cursor_state() == ui.TARGET_STATE:
                ui.reset_cursor()
            return
        if enter:
            if ui.get_cursor_state() == ui.NORMAL_STATE:
                relation = BigWorld.player().playerRelation(self)
                if relation == gametypes.RELATION_ENEMY:
                    ui.set_cursor_state(ui.TARGET_STATE)
                    ui.set_cursor(cursor.attack)
                    ui.lock_cursor()
                else:
                    ui.set_cursor_state(ui.TARGET_STATE)
                    ui.set_cursor(cursor.talk)
                    ui.lock_cursor()
        elif ui.get_cursor_state() == ui.TARGET_STATE:
            ui.reset_cursor()
        super(Avatar, self).onTargetCursor(enter)

    def serverDisconnect(self, cause):
        gamelog.debug('@hjx logOff#serverDisconnect:', cause, self.isReturnToLogin)
        if cause == const.SERVER_DISCONNECT_LOGOFF:
            if self.isReturnToLogin or getattr(gameglobal.rds, 'transServerInfo', None):
                gameglobal.rds.loginManager.disconnectFromGame()
            else:
                clientcom.openForceUrl()
                BigWorld.quit()

    def setLoadingDist(self, dist):
        dist = gameglobal.MAX_LOADING_DIST if dist == 0 else limit(dist, 1, 500)
        gameglobal.setLoadingDist(dist)

    def serverNameSet(self, name):
        gameglobal.gServerName = name
        BigWorld.setDmpPlayerInfo(name, self.roleName)

    def getServerTime(self):
        if self.clientBootTime:
            return self.clientBootTime + BigWorld.time()
        else:
            return time.time()

    def getGameTime(self):
        t = self.serverBootTime + const.TIME_SYSTEM_TO_REAL * BigWorld.time()
        return time.localtime(t)

    def serverTimeSet(self, boot, now, isFirstTime):
        boot = boot * 1.0 / 1000
        now = now * 1.0 / 1000
        gamelog.debug('jorsef11: serverTimeSet', now, boot, BigWorld.time())
        gamelog.debug('jorsef11: serverTimeSet now: ', time.time())
        oldTime = self.getServerTime()
        self.serverBootTime = boot
        self.clientBootTime = now - BigWorld.time()
        gamelog.debug('jorsef11: after serverTimeSet', self.serverBootTime, self.clientBootTime)
        if not isFirstTime and now - oldTime < 120:
            return
        year, month, day = self.getGameTime()[0:3]
        BigWorld.setGameDate(year, month, day)
        p = BigWorld.player()
        if p.topLogo:
            p.topLogo.updateRoleName(p.topLogo.name)
        if self == p:
            self.setupActivityNotify()
        self.checkExpireItems((self.inv,
         self.equipment,
         self.fashionBag,
         self.storage,
         self.questBag))
        if isFirstTime:
            nextCheckExpireItemsTime = getattr(self, '_nextCheckExpireItemsTime', 0)
            if nextCheckExpireItemsTime:
                self._nextCheckExpireItemsTime = 0
                self.addCheckExpireItemsCallback(nextCheckExpireItemsTime)
            nextCheckExpireWardrobeItemsTime = getattr(self, '_nextCheckExpireWardrobeItemsTime', 0)
            if nextCheckExpireWardrobeItemsTime:
                self._nextCheckExpireWardrobeItemsTime = 0
                self.addCheckExpireWardrobeItemsCallback(nextCheckExpireWardrobeItemsTime)
            self.setXConsignStartCallBack()
        self.nofityModelFinish()

    def serverTimeProxy(self, now, boot, still):
        boot = boot * 1.0 / 1000
        now = now * 1.0 / 1000
        gamelog.debug('jorsef: serverTimeProxy', now, boot, still)
        import timeProxy
        timeProxy.toProxy(still, now)
        self.serverBootTime = boot
        self.clientBootTime = now - BigWorld.time()
        year, month, day = self.getGameTime()[0:3]
        BigWorld.setGameDate(year, month, day)
        import time
        curTime = time.localtime()
        res = '%02d.%02d.%02d.%02d.%02d.%02d' % (curTime[0],
         curTime[1],
         curTime[2],
         curTime[3],
         curTime[4],
         curTime[5])
        self.chatToGm('时间被设置为：%s' % res)

    def serverTimeOrigin(self, now, boot):
        boot = boot * 1.0 / 1000
        now = now * 1.0 / 1000
        gamelog.debug('jorsef: serverTimeOrigin', now, boot)
        import timeProxy
        timeProxy.toOrigin()
        self.serverBootTime = boot
        self.clientBootTime = now - BigWorld.time()
        year, month, day = self.getGameTime()[0:3]
        BigWorld.setGameDate(year, month, day)

    def transferServer(self, hostId, account, info):
        pass

    def doQinggongAction(self, qtype):
        gamelog.debug('qinggong:开始做轻功动作')
        if self.life == gametypes.LIFE_DEAD:
            return
        self.qinggongMgr.doQinggongAction(qtype)
        self.apEffectEx.doQinggongAction(qtype)

    def qinggongActionFailed(self, qtype):
        gamelog.debug('qinggongActionFailed:', qtype)

    def qinggongStateFailed(self, stype):
        gamelog.debug('qinggongStateFailed:', stype)

    def startEpRegenTime(self):
        pass

    def npcDialog(self, entId, options):
        pass

    def needBlackShadow(self):
        return True

    def _getSchoolSwitchAvatarConfig(self):
        if self._isSchoolSwitch():
            if SSGD.data.has_key(self.schoolSwitchNo):
                ssgd = SSGD.data[self.schoolSwitchNo]
                if ssgd.has_key('avatarConfigId'):
                    filePath = '%s/%d.xml' % (gameglobal.AVATAR_TEMPLATE_PATH, ssgd['avatarConfigId'])
                    avatarInfo = ResMgr.openSection(filePath)
                    avatarConfig = avatarInfo.readString('avatarConfig')
                    return avatarConfig

    def set_avatarConfig(self, old):
        if self.partsUpdating:
            return
        if not self.realAvatarConfig:
            return
        self.setAvatarConfig(True)
        if self == BigWorld.player():
            self.needCharSnapshot = True

    def useAvatarConfig(self, old):
        gamelog.debug('b.e.:set_avatarConfig', self.partsUpdating)
        if self.partsUpdating:
            return
        p = BigWorld.player()
        if gameglobal.rds.loginScene.inAvatarStage() and gameglobal.rds.GameState <= gametypes.GS_LOGIN:
            gameglobal.rds.ui.characterDetailAdjust.applyMorpher(self)
            return
        if not self.realAvatarConfig:
            return
        self.setAvatarConfig(False)
        if self == p:
            fxType = strmap(self.realAvatarConfig).get('fxType')
            if fxType:
                Sound.setFxStyle(fxType)

    def setAvatarConfig(self, needDyeMorph):
        if not self.isRealModel:
            return
        avatarConfig = self.realAvatarConfig
        if needDyeMorph:
            m = avatarMorpher.AvatarModelMorpher(self.id, False)
            m.readConfig(avatarConfig)
            m.apply()
        else:
            m = vertexMorpher.AvatarFaceMorpher(self.id)
            m.readConfig(avatarConfig)
            m.apply()
        self.resetTopLogo()

    def afterModelFinish(self):
        super(Avatar, self).afterModelFinish()
        if gameglobal.rds.GameState > gametypes.GS_LOGIN:
            self.refreshOpacityState()
        self.clientLife(self.life)
        self.clientStateEffect.restoreBufActState()
        self.forceUpdateEffect()
        self.effectOld = self.effect.deepcopy()
        self.statesOld = copy.deepcopy(self.getStates())
        if not gameglobal.rds.isSinglePlayer:
            self.useAvatarConfig(0)
        if self.life == gametypes.LIFE_DEAD:
            self.playDieAction(False)
        self.refreshEquipEnhanceEffects()
        if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
            if gameglobal.rds.loginScene.inCreateStage():
                if gameglobal.rds.loginScene.player is None:
                    gameglobal.rds.loginScene.player = self
                if gameglobal.rds.loginScene.player != None:
                    if hasattr(BigWorld, 'openAvatarShadow'):
                        BigWorld.openAvatarShadow(gameglobal.rds.loginScene.player.model)
                BigWorld.callback(0.5, Functor(clientcom.setModelPhysics, self.modelServer.bodyModel))
                gameglobal.rds.loginScene.moveToDestination(0, 'show_%d_%d.track' % (self.physique.sex, self.physique.bodyType))
            elif gameglobal.rds.loginScene.inAvatarStage():
                if gameglobal.rds.loginScene.player != None:
                    if hasattr(BigWorld, 'openAvatarShadow'):
                        BigWorld.openAvatarShadow(gameglobal.rds.loginScene.player.model)
                BigWorld.callback(0.5, Functor(clientcom.setModelPhysics, self.modelServer.bodyModel))
                gameglobal.rds.loginScene.player.model.expandVisibilityBox(1000)
            elif gameglobal.rds.loginScene.inSelectZeroStage():
                self.setTargetCapsUse(False)
            gameglobal.rds.loginScene.loadingDec()
            self.setRongGuang(True)
            self.model.visible = False
            if gameglobal.rds.loginScene.inCreateSelectNewStage():
                gamelog.debug('ypc@ hide avatar!!!', gameglobal.rds.loginScene.player)
                self.hide(True)
            else:
                BigWorld.callback(0.1, self.refreshOpacityState)
        else:
            self.setRongGuang()
        if self.itemClientEffectCache:
            self.refreshItemClientEffect([], self.itemClientEffectCache.keys())
        if self.apprenticeTrainInfo:
            self.set_apprenticeTrainInfo(())
        self.checkModelValid(0)
        if self.belongToRoundTable:
            self.modelServer.enterRoundTable()
        if self.inInteractiveObject():
            self.modelServer.enterInteractiveObject()
        if self.carrier.isRunningState():
            if self.carrier.has_key(self.id):
                self.modelServer.enterCarrier()
        self.refreshYabiaoEffect()
        self.setFaceEmoteId()
        self.soulTeamTopLogo()
        self.refreshWeaponVisible()
        if self.bWingWorldYabiaoAttacker > utils.getNow():
            self.addYabiaoAttackerEffect()
        monsterIdList = sfx.G_MONSTER_LOCKED.get(self.id, [])
        for monsterId in monsterIdList:
            if monsterId and BigWorld.entities.get(monsterId, None):
                monster = BigWorld.entities[monsterId]
                if getattr(monster, 'IsMonster', False) and monster.inWorld and monster.firstFetchFinished and monster.getConnectorTgtId() and not monster.targetLockConnector:
                    monster.addConnectEff()

        if hasattr(self, 'setAssassinationModelFinish'):
            self.setAssassinationModelFinish()
        if getattr(self, 'jctSeq', 0) and BigWorld.player().inClanCourier():
            self.changeClanWarHunt(True)
        apEffectEx = getattr(self, 'apEffectEx', None)
        if apEffectEx:
            apEffectEx.resetEffect()
        BigWorld.callback(3, self.refreshWingHorseIdleEffect)

    def soulTeamTopLogo(self):
        topLogo = getattr(self, 'topLogo', None)
        if topLogo and self._isSoul():
            topLogo.updateRoleName(self.roleName)

    def afterPartsUpdateFinish(self):
        gamelog.debug('b.e.:avatar@afterPartsUpdateFinish')
        if gameglobal.rds.loginScene.inAvatarStage() and gameglobal.rds.GameState <= gametypes.GS_LOGIN:
            BigWorld.callback(0.5, Functor(clientcom.setModelPhysics, self.modelServer.bodyModel))
            self.useAvatarConfig(0)
            tintalt.ta_add(self.allModels, gameglobal.rds.xuanrenTint, [], tintType=tintalt.AVATARTINT)
        elif not gameglobal.rds.isSinglePlayer:
            self.setAvatarConfig(True)
        self.setRongGuang()
        self.checkModelValid(1)
        self.setFaceEmoteId()
        if hasattr(self, 'setAssassinationModelFinish'):
            self.setAssassinationModelFinish()

    def checkModelValid(self, where = 0):
        if self.isRealModel and self.modelServer and self.modelServer.bodyModel:
            model = self.modelServer.bodyModel
            if model.sources[-1].find('dummy.model') == -1:
                p = BigWorld.player()
                if where == 0:
                    msg = 'afterModelFinish model %s, spaceNo: %d, entity: %s' % (str(model.sources), getattr(p, 'spaceNo', 0), str(self))
                else:
                    msg = 'afterPartsModelFinish model %s, spaceNo: %d, entity: %s' % (str(model.sources), getattr(p, 'spaceNo', 0), str(self))
                clientUtils.reportEngineException(msg)

    def afterWeaponUpdate(self, weapon):
        if not self.inWorld:
            return
        if getattr(self, 'hidingPower', None):
            self.resetHiding()

    def afterWearUpdate(self, wear):
        if not self.inWorld:
            return
        if getattr(self, 'hidingPower', None):
            self.resetHiding()

    def _isOnLoginScene(self):
        if gameglobal.rds.loginScene.inAvatarStage() and gameglobal.rds.GameState <= gametypes.GS_LOGIN:
            self.am.matchCaps = [keys.CAPS_IDLE1, keys.CAPS_AVATAR_IDLE]
            return True
        return False

    def selfInjure(self, what, delta):
        pass

    def stopCast(self, skillId, skillLv, targetId, stopAction):
        super(Avatar, self).stopCast(skillId, skillLv, targetId, stopAction)
        self.skillPlayer.stopCast(skillId, skillLv, targetId)

    def applyByGroup(self, srcName, srcLevel, srcSchool, srcGbId):
        pass

    def rejectApply(self, groupNUID):
        pass

    def sendSkillInfo(self, skills):
        pass

    def sendPSkillInfo(self, pskId, subSrc, enable, level, pData):
        pass

    def batchUpdatePSkillEnable(self, enablePsks, disablePsks):
        pass

    def updatePSkillEnable(self, pskId, enable):
        pass

    def sendFamousGeneralAward(self, awardInfo):
        pass

    def sendTriggerPSkillInfo(self, pskId, level, enable):
        pass

    def batchUpdateTriggerPSkillEnable(self, enablePsks, disablePsks):
        pass

    def updateTriggerPSkillEnable(self, pskId, enable):
        pass

    def sendWsSkillInfo(self, res):
        pass

    def sendSocialSkillInfo(self, skills):
        pass

    def sendFlagState(self, states):
        pass

    def clearSkillInfo(self):
        pass

    def clearQingGongSkillInfo(self):
        pass

    def sendQingGongSkillInfo(self, skillId, enable, lv):
        pass

    def updateQingGongSkillInfo(self, skillId, enable, lv):
        pass

    def sendZaijuSkillInfo(self, isPSkill, info):
        pass

    def updatePropScheme(self, schemeNo, scheme, schemeName, status, expireTime):
        pass

    def updateSkillInfos(self, skillInfos):
        pass

    def updateSkillInfo(self, skillId, enable, lv, enhanceData):
        pass

    def updateAirSkill(self, skillId, lv, enable, exp):
        pass

    def onQueryBackflowVp(self, amount):
        pass

    def onGetBackflowVp(self, ok):
        pass

    def updateWsSkillInfo(self, skillId, enable, lv, slots, proficiency, daoHeng, lingli):
        pass

    def updateWsSelect(self, skillId, select):
        pass

    def removePSkill(self, pskillId):
        pass

    def removeTriggerPSkill(self, pskillId):
        pass

    def updatePSkillNextTriggerTime(self, pskId, nextTriggerTime):
        pass

    def updatePSkillTriggerInvalidTime(self, pskId, triggerInvalidTime):
        pass

    def sendAirSkillInfo(self, skills):
        pass

    def sendEquipSoulInfo(self, data):
        pass

    def onGetServerPlayerMaxLv(self, lv):
        pass

    def skillTimeUpdate(self, skill, level, remainTime, cdStorage):
        pass

    def batchSkillTimeUpdate(self, data):
        pass

    def testTime(self):
        pass

    def sendAccTutorial(self, data):
        pass

    def addFogEffect(self, radius = 25.0):
        pass

    def delFogEffect(self):
        pass

    def reliveHereRes(self, resultCode):
        pass

    def onPushAppMsg(self, info):
        pass

    def onLoadAppMsg(self, info):
        pass

    def faceToDir(self, yaw, immediately = False, forbidCamRotate = False):
        pass

    def faceToDirWidthCamera(self, yaw, immediately = False):
        pass

    def updateEquipSoulSchemeData(self, schemeNo, data):
        pass

    def hotfixMD5Send(self, smd5):
        pass

    def reliveByOtherRequest(self, srcId, timeInterval, srcRole):
        pass

    def pullByOtherRequest(self, sRoleName, timeInterval):
        pass

    def fameUpdate(self, fameId, value, nWeek, mWeek, nDay, extraValue, mLastWeekExtra, fameTransferParam):
        pass

    def fameSend(self, fameInfo):
        pass

    def socSchoolSend(self, socSchoolInfo):
        pass

    def sendFbAward(self, fbAward):
        pass

    def handleCombatMsg(self, msgs):
        pass

    def notifyRefMonster(self, spaceNo, spaceMonsters, msg):
        pass

    def beUseSkillRequest(self, sRoleName, skillId, level, timeInterval):
        pass

    def skillQte(self, srcSkId, qteSkills, interval, lastTime, triggerTime, switchOn):
        pass

    def restoreOnKillMonster(self, monsterId, hpAdd, mpAdd):
        if hpAdd > 0:
            gameglobal.rds.ui.hpMap[monsterId] = hpAdd
        if mpAdd > 0:
            gameglobal.rds.ui.mpMap[monsterId] = mpAdd

    def sendLearnedPSkillInfos(self, skillInfos):
        pass

    def sendLearnedPSkillInfo(self, pskId, lv, enable):
        pass

    def sendAirPSkill(self, pskId, lv, enable):
        pass

    def updateCalcEntities(self, creationId, ids):
        pass

    def showBianshiMvp(self):
        gamelog.debug('wy:showBianshiMvp')
        if self.topLogo:
            self.topLogo.showMvp()
        gameglobal.rds.ui.teamComm.setMvp(self.id)

    def notifyMonsterDie(self, spaceNo, charType, args):
        pass

    def toggleCollide(self):
        pass

    def changeModel(self):
        pass

    def showGMMessage(self, title, desc):
        gameglobal.rds.ui.gmMessage.show(title, desc)

    def showEntityId(self, show):
        pass

    def addRedPacketDone(self, ok, sn, pType, money, cnt, channel, msg, extra):
        pass

    def onGetRedPacket(self, ok, sn, pType, srcGbID, srcName, money):
        pass

    def onQueryRedPacketAssignInfo(self, sn, data):
        pass

    def onQueryLuckyRedPacket(self, sn, data):
        pass

    def onQueryMyRedPacket(self, redPackets, totalSendCash, totalSendCoin, totalRevCash, totalRevCoin):
        pass

    def updateLuckRedPacket(self, sn, data):
        pass

    def rewardHallLogonCheck(self):
        pass

    def _isOnZaiju(self):
        return self.bianshen[0] == gametypes.BIANSHEN_ZAIJU

    def _getZaijuNo(self):
        return self.bianshen[1]

    def _isInBianyao(self):
        return self.bianshen[0] == gametypes.BIANSHEN_BIANYAO

    def _isOnZaijuOrBianyao(self):
        return self._isOnZaiju() or self._isInBianyao()

    def _getZaijuOrBianyaoNo(self):
        return self.bianshen[1]

    def _isSchoolSwitch(self):
        return getattr(self, 'schoolSwitchNo', 0) > 0

    def _getSchoolSwitchNo(self):
        return self.schoolSwitchNo

    def leaveDlgRange(self, unUsedDist):
        boothInfo = gameglobal.rds.ui.booth.otherBoothInfo
        if not gameglobal.rds.ui.booth.boothType and boothInfo and boothInfo[0] == self.id:
            gameglobal.rds.ui.booth.closeNumber()
            gameglobal.rds.ui.booth.onCloseQuantity()
            gameglobal.rds.ui.booth.hide()

    def sendTransportDest(self, transportEntId, transportId, destDict):
        pass

    def getXinYiOnline(self):
        if self.xinYiManager:
            return self.xinYiManager['onlineState']
        else:
            return 0

    def createXinYiMsg(self, msg):
        if self.xinYiManager:
            xinYi = self.xinYiManager
            return {'name': xinYi['name'],
             'time': utils.getNow(),
             'msg': msg,
             'photo': self.getXinYiMsgPhoto(),
             'isMe': False}
        else:
            return None

    def getXinYiMsgPhoto(self):
        if self.xinYiManager:
            xinYi = self.xinYiManager
            return 'xinYiHeadIcon/' + xinYi['profile'] + '.dds'
        else:
            return 'xinYiHeadIcon/1.dds'

    def onChatAvatar(self, msg):
        gameglobal.rds.ui.gmChat.receiveMsg(msg)

    def onGMDisconnectAvatar(self):
        gameglobal.rds.ui.gmChat.setState(uiConst.GM_CAHT_HIDE)
        gameglobal.rds.ui.gmChat.hide()

    def chatFromXinYi(self, msg):
        if not self.inWorld:
            return
        isNormal, msg = taboo.checkDisbWord(msg)
        if not isNormal:
            return
        isNormal, msg = taboo.checkBSingle(msg)
        m = self.createXinYiMsg(msg)
        if m:
            if gameglobal.rds.ui.chatToFriend.isOpened(const.XINYI_MANAGER_ID):
                gameglobal.rds.ui.chatToFriend.receiveMsg(const.XINYI_MANAGER_ID, m)
            else:
                self._addTempMsg(const.XINYI_MANAGER_ID, gametypes.FRIEND_MSG_TYPE_CHAT, m)
                name = BigWorld.player().xinYiManager['name'] + '向你发送了信息'
                gameglobal.rds.ui.friend.addMinChat([const.XINYI_MANAGER_ID,
                 name,
                 msg,
                 BigWorld.player().getXinYiMsgPhoto(),
                 True])
                gameglobal.rds.ui.friend.minChatShine(const.XINYI_MANAGER_ID, True)
            if hasattr(self, 'chatDB'):
                self.chatDB.saveMsg(const.XINYI_MANAGER_ID, m['name'], m['name'], False, m['photo'], msg, m['time'])
            gameglobal.rds.sound.playSound(gameglobal.SD_403)

    def showTeleportStoneConfirm(self, destId, costItemId):
        pass

    def showWingWorldTeleportStoneConfirm(self, destId, cash, extraCash):
        pass

    def showTeleportStoneAndReliveConfirm(self, destId, needCostItem):
        pass

    def calcNpcGroundPos(self, npcId, offsetY):
        pass

    def onGetSeekerMapData(self, datas):
        pass

    def sightAll(self, spaceID, ver, info):
        pass

    def sightEnter(self, spaceID, oldID, info):
        pass

    def sightLeave(self, oldID):
        pass

    def sightAlterExtra(self, oldID, newInfo):
        pass

    def onAcceptQuestByClientNpc(self, npcID, questId, isSucc):
        pass

    def onCompleteQuestByClientNpc(self, npcID, questId):
        pass

    def switchHideMode(self, hideMode):
        pass

    def updateClientConfig(self, config):
        pass

    def updateClientConfigForOne(self, config):
        pass

    def relogNotify(self):
        pass

    def getClientMD5(self):
        Hijack.get_proc_code(Hijack._hijack_counter)

    def getAllClientHackMD5(self, keyName):
        if not keyName:
            Hijack.check_by_proc()
        else:
            Hijack.check_by_key(keyName)

    def getMousePos(self, interval, totalTime):
        Hijack.checkMousePos(interval, totalTime)

    def getWindowTitle(self):
        Hijack.checkWindowTitle()

    def getDumpFilesInfo(self):
        info = clientUtils.getDumpFilesInfo()
        self.base.onGetDumpFilesInfo(zlib.compress(cPickle.dumps(info, -1)))

    def onFetchNOSKey(self, md5, timeStamp, filePath):
        pass

    def enableAbilityNode(self, anNode, star):
        pass

    def syncAbilityIds(self, abilityIds):
        pass

    def forbidChat(self, talkerName):
        pass

    def teleportToVehicle(self, vehicleId, posOffset, yawOffset):
        pass

    def onGetVipAward(self, serviceID, packageID):
        pass

    def sendVipInfo(self, res):
        pass

    def setAccountTotalCoin(self, val):
        pass

    def onBuyVipService(self, mIds, succ):
        pass

    def onGetVipCompensate(self, dayCnt, succ):
        pass

    def onQueryVipIsSameCompensate(self, isSame):
        pass

    def onGetAllVipAward(self, serviceInfo):
        pass

    def refreshVipInfo(self, resetDailyServices, resetWeeklyServices, expiredServices):
        pass

    def isValidVipProp(self, propID):
        pass

    def updateVipCnt(self, serviceID, cnt):
        pass

    def onBotTest(self):
        pass

    def serverCancelWaitForRideTogetherLoading(self):
        pass

    def set_isWaitingRideTogether(self, old):
        pass

    def waitForRideTogetherLoading(self):
        pass

    def continueRideTogetherNavigate(self):
        pass

    def startProgressLoading(self):
        pass

    def endProgressLoading(self):
        pass

    def setClientMentorQulification(self, enable):
        pass

    def onApplyMentor(self, apprenticeName, apprenticeGbId, apprenticeSchool, apprenticeLv, apprenticeGuildName, apprenticeSignature, apprenticeSex):
        pass

    def onApplyMentorEx(self, apprenticeName, apprenticeGbId, apprenticeSchool, apprenticeLv, apprenticeGuildName, apprenticeSignature, apprenticeSex):
        pass

    def onApplyApprentice(self, mentorName, mentorGbId, mentorSchool, mentorLv, mentorGuildName, mentorSignature, mentorSex):
        pass

    def onApplyApprenticeEx(self, mentorName, mentorGbId, mentorSchool, mentorLv, mentorGuildName, mentorSignature, mentorSex):
        pass

    def kickMentor(self, mentorName, offTime, punish):
        pass

    def kickApprentice(self, apprenticeName, apprenticeGbId, offTime, punish):
        pass

    def kickMentorEx(self, mentorName, mentorGbId, offTime, punish):
        pass

    def kickApprenticeEx(self, apprenticeName, apprenticeGbId, offTime, punish):
        pass

    def onAddApprenticeInfo(self, mentorGbId, matesGbIds, apprenticeGbIds):
        pass

    def onAddApprenticeInfoEx(self, mentorInfo, matesGbIds, apprenticeGbIds):
        pass

    def onRemoveApprenticeInfo(self, mentorGbId, matesGbIds, apprenticeGbIds):
        pass

    def onRemoveApprenticeInfoEx(self, mentorGbId, matesGbIds, apprenticeGbIds):
        pass

    def onApplyTraining(self):
        pass

    def onApplyTrainingEx(self):
        pass

    def apprenticeGraduate(self):
        pass

    def apprenticeGraduateEx(self):
        pass

    def setApprenticeGraduate(self, val):
        pass

    def sendApprenticeValEx(self, totalVal, weeklyVal, apprenticeVal, gbId, src):
        pass

    def onApplyGraduateEx(self, apprenticeGbId, apprenticeName, grade):
        pass

    def enableMentorQulificationEx(self):
        pass

    def enableApprenticeQulificationEx(self):
        pass

    def onApprenticeLogOnEx(self, apprenticeName, apprenticeGbId):
        pass

    def onMentorLogOnEx(self, mentorName, mentorGbId):
        pass

    def onSetBeMentorSloganEx(self, slogan):
        pass

    def onSetBeApprenticeSloganEx(self, slogan):
        pass

    def onApplySoleMentorEx(self, apprenticeGbId, apprenticeName):
        pass

    def onApplySoleApprenticeEx(self, mentorGbId, mentorName):
        pass

    def onSetSoleApprenticeEx(self, gbId, roleType, name):
        pass

    def onApplySoleDismissEx(self, gbId, name):
        pass

    def onClearSoleApprenticeEx(self, gbId, roleType):
        pass

    def applyGraduateEx(self, mentorGbId, ret):
        pass

    def onGetApprenticeInfoEx(self, gbId, ret):
        pass

    def onSetApprenticeOptEx(self, mentorRejectOptEx, apprenticeRejectOptEx):
        pass

    def onGetGraduateRemarkByGbIdEx(self, gbId, res):
        pass

    def sendApprenticePreferenceInfo(self, mentorPreferenceInfo, apprenticePreferenceInfo):
        pass

    def onQueryApprenticeGrowthFeedBack(self, val, growthConsumeRewarded):
        pass

    def onApplyLevelGrowthFeedback(self, apprenticeVal, growthConsumeVal, growthConsumeCash):
        pass

    def onGetLevelGrowthFeedback(self, mentorGbId, mentorName, apprenticeVal, growthConsumeVal, growthConsumeCash):
        pass

    def onApplyGraduateGrowthFeedback(self, apprenticeGbId, apprenticeVal, growthConsumeVal, growthConsumeCash):
        pass

    def onGetGraduateGrowthFeedback(self, mentorGbId, mentorName, apprenticeVal, growthConsumeVal, growthConsumeCash):
        pass

    def resetJingSuTuneTime(self):
        pass

    def sendStatistic(self, hostid, send):
        pass

    def updateFameBonusInfo(self, data):
        pass

    def _isSoul(self):
        flag = getattr(self, 'crossServerFlag', -1)
        return flag == const.CROSS_SERVER_STATE_IN

    def _isReturn(self):
        flag = getattr(self, 'crossServerFlag', -1)
        return flag == const.CROSS_SERVER_STATE_RETURN

    def _isBody(self):
        flag = getattr(self, 'crossServerFlag', -1)
        return flag == const.CROSS_SERVER_STATE_OUT

    def _isInCross(self):
        flag = getattr(self, 'crossServerFlag', -1)
        return flag == const.CROSS_SERVER_STATE_IN or flag == const.CROSS_SERVER_STATE_RETURN

    def flashPush(self, path):
        pass

    def takeFigurePhoto(self, fileName = 'figure.png', needCheck = True):
        pass

    def onCheckUploadCharSnapshot(self, fileName):
        pass

    def onApplyShuangxiu(self, srcId):
        pass

    def setPlayRecommendFinishedActivities(self, playRecommendedFinishedActivities):
        pass

    def yaoPeiMixFinish(self, ok, pg, ps):
        gameglobal.rds.ui.yaoPeiMix.mixFinish(ok, pg, ps)

    def addYaoPeiExpFinish(self, ok, resKind, pg, ps):
        gameglobal.rds.ui.yaoPeiFeed.feedFinish(ok, resKind, pg, ps)

    def yaoPeiTransferFinish(self, ok, sPg, sPs, tPg, tPs):
        gameglobal.rds.ui.yaoPeiTransfer.transferFinish(ok, sPg, sPs, tPg, tPs)

    def yaoPeiReforgeFinish(self, ok, pg, ps, idx, nVal):
        gameglobal.rds.ui.yaoPeiReforge.reforgeFinish(ok, pg, ps, idx, nVal)

    def clientPersistentNotify(self, add, notifyType, notifyArgs):
        pass

    def onGetRewardByLottery(self, page, pos, lotteryId, issueTime, nuid, flag, rank):
        pass

    def onQueryLottery(self, page, pos, lotteryId, issueTime, nuid, flag, rank):
        pass

    def unbindEquipSucc(self, pg, ps):
        gameglobal.rds.ui.unBindItem.unbindEquipSucc(pg, ps)

    def updatePvpEnhance(self, data):
        pass

    def notifyZiXunTime(self, succ, time):
        pass

    def transferBack(self):
        pass

    def onAddGuanYinPskill(self, resKind, srcPage, srcPos, tgtPage, tgtPos, slot, part, bookId):
        gameglobal.rds.ui.guanYin.refreshInfo()
        gameglobal.rds.ui.guanYin.playAddSuccessEff(slot, bookId)

    def onAddGuanYinSuperPskill(self, resKind, srcPage, srcPos, tgtPage, tgtPos, bookId):
        gameglobal.rds.ui.guanYin.refreshInfo()
        gameglobal.rds.ui.guanYin.playAddSuccessEff(uiConst.SUPER_SKILL_SLOT_POS, bookId)

    def onGuanYinPskillLvUpInEquip(self, resKind, page, pos, slot, part):
        gameglobal.rds.ui.guanYin.refreshInfo()
        gameglobal.rds.ui.guanYin.playLvUpSuccessEff(slot)

    def onGuanYinPskillLvUpInInv(self, page, pos):
        pass

    def onRemoveGuanYinPskill(self, resKind, page, pos, slot, part, bookId):
        gameglobal.rds.ui.guanYin.refreshInfo()
        gameglobal.rds.ui.guanYin.playRemoveSuccessEff(slot, bookId)

    def onGuanYinPskillBookMix(self, resultId, page, pos):
        pass

    def navigateToUseItem(self, resKind, page, pos, uuid, useSpaceNo, usePos):
        pass

    def doUIEvent(self, eventType):
        pass

    def onCheckUseCommonItem(self, page, pos, resKind):
        pass

    def setSecondEscPlayScenario(self, secondEscPlayScenario):
        pass

    def showItemStateTimeWaste(self, page, pos):
        pass

    def onGenSchoolTransferCondition(self, optype, condition):
        pass

    def sendSchoolTransferInfo(self, res):
        pass

    def switchAvatarRelationByCamp(self, enable):
        pass

    def onSetWSSchemeNameRes(self, isOK, schemeID, newName):
        pass

    def onSwitchWSSchemeRes(self, isOK, newSchemeID):
        pass

    def onGetWSSchemeHotKeys(self, schemeID, data):
        pass

    def onGetWSSchemesInfo(self, currSchemeID, timeExtra1, timeExtra2, timeSpecial, nameDefault, nameExtra1, nameExtra2, nameSpecial):
        pass

    def onRenewalWSSchemeTimeRes(self, isOK, schemeID, timeEndBefore, timeEndAfter):
        pass

    def notifyWSDaoHengFull(self, id):
        pass

    def queryClientVar(self, uuid, queryString):
        pass

    def executeClientCmd(self, uuid, clientCmd):
        pass

    def useTeamShareBoxConfirm(self, outOfScopeNames, boxId):
        msg = ''
        if len(outOfScopeNames) > 1:
            msg = "队员<font color=\'#be2727\'>%s</font>等人超出领奖范围,如继续开宝箱则这些队员无法领取奖励,是否继续?" % outOfScopeNames[0]
        else:
            msg = "队员<font color=\'#be2727\'>%s</font>超出领奖范围,如继续开宝箱则该队员无法领取奖励,是否继续?" % outOfScopeNames[0]
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cell.onUseTeamShareBoxConfirmed, boxId), yesBtnText='是', noBtnText='否', isModal=False, msgType='pushLoop', textAlign='center')

    def useEndlessBoxConfirm(self, msgId, boxId):
        msgData = GMD.data.get(msgId)
        if not msgData:
            return
        text = msgData.get('text')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(text, Functor(self.cell.onUseEndlessBoxConfirmed, boxId), yesBtnText='是', noBtnText='否', isModal=False, msgType='pushLoop', textAlign='center')

    def abandonQuestLoopConfirm(self, questLoopId, type, questName):
        text = '是否确定放弃 %s 任务' % questName
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(text, Functor(self.cell.onAbandonQuestLoopConfirm, questLoopId, type), yesBtnText='是', noBtnText='否', isModal=False, msgType='pushLoop', textAlign='center')

    def pushCompensateNotification(self, isAccountBonus, compInfo):
        if not gameglobal.rds.configData.get('enalbeGetCompensationFromGUI', False):
            return
        if len(compInfo) >= 6:
            compType = compInfo[5]
            if not (compType == 0 or compType == 1):
                return
        if not hasattr(self, 'compInfo'):
            self.compInfo = []
        for currCompItem in self.compInfo:
            if currCompItem[4] == compInfo[4]:
                return

        self.compInfo.append(compInfo)
        data = {'data': compInfo}
        if isAccountBonus == 0:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_PUSH_COMPENSATION1, data)
        else:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_PUSH_COMPENSATION2, data)

    def removeTeamSSCGroupEffect(self):
        if getattr(self, 'teamSSCGroupEffectId', 0) == 0:
            return
        self.removeFx(self.teamSSCGroupEffectId)

    def addTeamSSCGroupEffect(self):
        if getattr(self, 'tempCamp', 0) == 0:
            return
        effects = DCD.data.get('teamShengSiChangEffects', (3110, 3112, 3114, 3116, 3118, 3120, 3111, 3113, 3115, 3117, 3119))
        self.teamSSCGroupEffectId = effects[self.tempCamp - 1]
        fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getEquipEffectLv(),
         self.getEquipEffectPriority(),
         self.model,
         self.teamSSCGroupEffectId,
         sfx.EFFECT_UNLIMIT))
        fx and self.addFx(self.teamSSCGroupEffectId, fx)

    def updatePerformanceFilter(self, op, info):
        if op == 'add':
            self.monitor.add(info)
        elif op == 'del':
            self.monitor.remove(info)

    def onGetInteractTeams(self, interactTeamList):
        """
        \xd7\xee\xbd\xfc\xd7\xe9\xb6\xd3\xca\xfd\xbe\xdd\xb7\xb5\xbb\xd8
        :param interactTeamList: \xd7\xee\xbd\xfc\xd7\xe9\xb6\xd3\xc1\xd0\xb1\xed\xa3\xac\xb1\xa3\xb4\xe6\xd7\xee\xbd\xfc\xd7\xee\xb6\xe050\xcc\xf5\xb6\xd3\xce\xe9\xca\xfd\xbe\xdd\xa3\xac\xc3\xbf\xcc\xf5\xb6\xd3\xce\xe9\xca\xfd\xbe\xdd\xbe\xf9\xce\xaa\xd2\xbb\xb8\xf6\xd4\xaa\xd7\xe9\xa3\xba(timestamp, type, id, mateList)\xd4\xaa\xd7\xe9\xa3\xac
        \xc6\xe4\xd6\xd0mateList\xce\xaa\xc1\xd0\xb1\xed\xa3\xacmateList\xd4\xaa\xcb\xd8\xce\xaa\xd4\xaa\xd7\xe9\xa3\xac\xd4\xaa\xd7\xe9\xca\xfd\xbe\xdd\xa3\xba(gbId, roleName, teamLeaderFlag, photo, sex, school)
        :return:
        """
        gameglobal.rds.ui.recentlyInteract.onGetInteractTeams(interactTeamList)

    def syncUseItemWish(self, wishInfo):
        pass

    def itemWishConfirmInfoSend(self, info):
        pass

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


class PlayerAvatarMeta(AvatarMeta):

    def __init__(cls, name, bases, dic):
        inherits = (ImpPlayerSwim,
         ImpPlayerCombat,
         ImpPlayerRideFly,
         ImpPlayerProperty,
         ImpPlayerNpc,
         ImpPlayerItem,
         ImpPlayerDebug,
         ImpPlayerUI,
         ImpPlayerTeam,
         ImpMultiLine,
         ImpFishing,
         ImpPlayerBooth,
         ImpPlayerSight,
         ImpPlayerVehicle,
         ImpPlayerAbility,
         ImpPlayerComm,
         ImpPlayerCheck,
         ImpPlayerJingJie,
         ImpPlayerVip,
         ImpPlayerApprentice,
         ImpPlayerLottery,
         ImpPlayerRewardHall,
         ImpPlayerSoundRecord,
         ImpPlayerSummonSprite)
        for inherit in inherits:
            AvatarMeta._moduleMixin(cls, name, inherit)


class PlayerAvatar(Avatar):
    __metaclass__ = PlayerAvatarMeta

    def onBecomePlayer(self):
        self.deepLearningData = {}
        self.isSendIntimacyNickname = False
        self.inWabaoStatus = False
        self.arenaPlayoffsCurRoundNum = 0
        self.buildIntimacyCnt = 0
        self.isOldBuildIntimacy = True
        self.inviteGroupFailedInfo = {}
        self.bfHookScore = 0
        self.cpEmoteSkillCD = {}
        self.arenaPlayoffsMember = {}
        self.arenaPlayoffsTeam = {}
        self.arenaScorePlayoffsMember = {}
        self.arenaScorePlayoffsTeam = {}
        self.arenaScorePlayoffsTeamNUID = 0
        self.arenaScorePlayoffsTeamHeader = 0
        self.resetWithQuitGroupAutoInfo()
        self.arenaSidePrepareDict = {}
        self.abilityIds = {}
        self.skills = {}
        self.pskills = {}
        self.triggerPSkills = {}
        self.learnedPSkills = {}
        self.airPSkills = {}
        self.airSkills = {}
        self.lifeSkill = {}
        self.partner = {}
        self.marriageBeInvitedInfo = {}
        self.marriageRedPacketInfo = []
        self.marriageMsgDict = {}
        self.marriageTgtEquipment = {}
        self.marriageSkillTime = 0
        self.zmjData = {}
        self.zmjPhotoData = {}
        self.expAddParamBuffVal = 0
        self.fightForLovePhase = 0
        self.fightForLoveResult = {}
        self.fightForLoveMsgIds = {}
        self.conditionalPropTips = {}
        self.conditionalPropTime = {}
        self.buffTreasureBoxIds = []
        self.partnerMsgBox = {}
        self.zaijuSkills = {}
        self.qingGongSkills = {}
        self.intimacySkills = {}
        self.bianshiDict = {}
        self.fame = {}
        self.fameDay = {}
        self.fameWeek = {}
        self.doQingGongActionState = False
        self.questMonsterInfo = {}
        self.wsSkills = {}
        self.guildGrowth = GuildGrowth()
        self.guildSkills = {}
        self.guildMemberSkills = {}
        self.guildEntities = {}
        self.pendingGuildEntIds = []
        self.pendingGuildMarkerIds = []
        self.guildWSPractice = []
        self.guildWSDaoheng = []
        self.importantPlayRecommendInfo = {}
        self.serverProgresses = {}
        self.extraServerProgresses = {}
        self.serverProgressStatus = {}
        self.valuableTrade = {}
        self.fbAward = []
        self.flagStates = []
        self.openServerBonus = None
        self.refreshDroppedItemList = []
        self.refreshDroppedItemHandle = None
        self.curLifeSkillType = -1
        self.cipherOfPerson = ''
        self.guildTournament = GuildTournament()
        self.crossGtn = CrossGuildTournament()
        self.crossRankGtn = CrossRankGuildTournament()
        self.inv = InvClient(pageCount=const.INV_PAGE_NUM, width=const.INV_WIDTH, height=const.INV_HEIGHT, resKind=const.RES_KIND_INV)
        self.battleFieldBag = BattleFieldBagCommon()
        self.crossInv = InvClient(pageCount=const.CROSS_INV_PAGE_NUM, width=const.CROSS_INV_WIDTH, height=const.CROSS_INV_HEIGHT, resKind=const.RES_KIND_CROSS_INV)
        self.questBag = inventoryCommon.InventoryCommon(pageCount=const.QUEST_BAG_PAGE_NUM, width=const.QUEST_BAG_WIDTH, height=const.QUEST_BAG_HEIGHT, resKind=const.RES_KIND_QUEST_BAG)
        self.cart = container.Container(const.CART_PAGE_NUM, const.CART_WIDTH, const.CART_HEIGHT)
        self.fashionBag = container.Container(const.FASHION_BAG_PAGE_NUM, const.FASHION_BAG_WIDTH, const.FASHION_BAG_HEIGHT)
        self.fashionBagBar = container.Container(const.FASHION_BAG_BAR_PAGE_NUM, const.FASHION_BAG_MAX_SLOT_NUM, const.FASHION_BAG_BAR_HEIGHT)
        self.materialBag = container.Container(const.MATERIAL_BAG_PAGE_NUM, const.MATERIAL_BAG_WIDTH, const.MATERIAL_BAG_HEIGHT)
        self.materialBagBar = container.Container(const.MATERIAL_BAG_BAR_PAGE_NUM, const.MATERIAL_BAG_MAX_SLOT_NUM, const.MATERIAL_BAG_BAR_HEIGHT)
        self.spriteMaterialBag = container.Container(const.SPRITE_MATERIAL_BAG_PAGE_NUM, const.SPRITE_MATERIAL_BAG_WIDTH, const.SPRITE_MATERIAL_BAG_HEIGHT)
        self.spriteMaterialBagBar = container.Container(const.SPRITE_MATERIAL_BAG_BAR_PAGE_NUM, const.SPRITE_MATERIAL_BAG_MAX_SLOT_NUM, const.SPRITE_MATERIAL_BAG_BAR_HEIGHT)
        self.mallBag = container.Container(const.MALL_BAG_PAGE_NUM, const.MALL_BAG_WIDTH, const.MALL_BAG_HEIGHT)
        self.rideWingBag = RideWingBagClient(const.RIDE_WING_BAG_PAGE_NUM, SCD.data.get('rideWingBagWidth', const.RIDE_WING_BAG_WIDTH), const.RIDE_WING_BAG_HEIGHT, const.RES_KIND_RIDE_WING_BAG)
        self.zaijuBag = zaijuBag.ZaijuBag(const.ZAIJU_BAG_PAGE_NUM, const.ZAIJU_BAG_WIDTH, const.ZAIJU_BAG_HEIGHT)
        self.hierogramBag = container.Container(const.HIEROGRAM_BAG_PAGE_BAG, const.HIEROGRAM_BAG_WIDTH, const.HIEROGRAM_BAG_HEIGHT)
        self.hierogramBagBar = container.Container(const.HIEROGRAM_BAG_BAR_PAGE_NUM, const.HIEROGRAM_BAG_MAX_SLOT_NUM, const.HIEROGRAM_BAG_BAR_HEIGHT)
        self.tempBag = container.Container(const.TEMP_BAG_PAGE_NUM, const.TEMP_BAG_WIDTH, const.TEMP_BAG_HEIGHT)
        self.bagBar = container.Container(const.BAG_BAR_PAGE_NUM, const.BAG_BAR_WIDTH, const.BAG_BAR_HEIGHT)
        self.storage = storageCommon.StorageCommon()
        self.storageBar = container.Container(const.STORAGE_BAR_PAGE_NUM, const.STORAGE_MAX_SLOT_NUM, const.STORAGE_BAR_HEIGHT)
        self.equipment = equipment.Equipment()
        self.subEquipment = subEquipment.SubEquipment()
        self.chatConfig = chatConfig.ChatConfig()
        self.buyBackDict = {}
        self.fishingEquip = fishingEquipment.FishingEquipment()
        self.booth = container.Container(const.BOOTH_PAGE_NUM, const.BOOTH_WIDTH, const.BOOTH_HEIGHT)
        self.friend = friend.Friend().initClient()
        self.localClanWar = clanWar.ClanWar()
        self.crossClanWar = clanWar.ClanWar()
        self.declareWarGuild = set()
        self.guild = None
        self.annalReplay = None
        self.questLoopChain = QuestLoopChain()
        self.groupLuckJoy = GroupLuckJoyVal()
        self.globalMonsters = {}
        self.runMan = RunManPlayerRoute()
        self.xinYiManager = {}
        self.privateShop = {}
        self.worldWar = WorldWar()
        self.wingWorld = WingWorld()
        self.crossToHostId = 0
        self.appliedGuilds = []
        self.runeBoard = runeCommon.RuneCommon()
        self.exploreEquip = exploreEquipment.ExploreEquipment()
        self.lifeEquipment = lifeEquipment.LifeEquipment()
        self.skillQteData = SkillQteDict()
        self.summonedSpriteAccessory = summonedSpriteAccessory.SummonedSpriteAccessory()
        self.mallInfo = {}
        self.mallHistory = []
        self.unbindCoin = 0
        self.bindCoin = 0
        self.freeCoin = 0
        self.mallCash = 0
        self.mallScore = 0
        self.totalMallScore = 0
        self.commonPoints = 0
        self.standbyPoints = 0
        self.specialPoints = 0
        self.fbGuideInfo = {}
        self.summonSpriteList = {}
        self.summonSpriteListCache = {}
        self.spriteGrowthInfo = {}
        self.newFlagBattleFieldStatus = {}
        self.newFlagBattleFieldStage = {}
        self.teamEndless = TeamEndless()
        self.teamEndlessRewardTimes = {}
        self.membersGuideCnt = {}
        self.openShopId = 0
        self.openShopType = 0
        self.expBonusFreeze = False
        self.expBonus = {}
        self.vipWeeklyBonus = []
        self.vipDailyBonus = []
        self.vipValidCnt = []
        self.vipBasicPackage = {}
        self.basicPackageBuyRecord = None
        self.vipAddedPackage = {}
        self.vipClientCheckServices = {}
        self.vipClientCheckProps = {}
        self.vipCompensateCnt = 0
        self.coinConsignData = {}
        self.hotkeyData = {}
        self.skillEnhancePointBonus = {}
        self.chargeRewardInfo = []
        self.dailyStats = {}
        self.equipSoul = {}
        self.equipSoulSchemeInfo = {}
        self.needCharSnapshot = False
        self.charSnapshopOp = 0
        self.partnerEquipment = {}
        self.summonSpriteProps = {}
        self.summonSpritePropsWithFami = {}
        self.summonSpriteVirtualBaseProps = {}
        self.groupFollowTempOutInfo = {}
        self.groupHeaderTargets = []
        self.allCardBags = {}
        self.buffListenerConfig = {}
        self.listenerBuffData = {}
        self.listeningBuffShowData = {}
        self.pyq_skey = ''
        self.pyq_forcePublishUrl = ''
        self.topicList = []
        self.pyqNewsNum = 0
        self.pyqNewsNumTickId = 0
        self.summonSpriteBio = summonSpriteBiography.SummonSpriteBiographies()
        self.summonSpriteBioTargets = summonSpriteBiography.SummonSpriteBiographyTargets()
        self.summonSpriteBioStatsInfo = {}
        self.guildMembersFbData = {}
        self.guildFubenRoundNum = {}
        self.latency = [0,
         0,
         0,
         0,
         0]
        self.logCnt = 0
        self.ap = None
        self.target = None
        self.targetLocked = None
        self.lastTargetLocked = None
        self.optionalTargetLocked = None
        self.modelServer.setUrgent(True)
        self._updateQuestNextFrame = False
        self.relogNotifyState = False
        self.isInCbgRoleSelling = False
        self.clientInnerRange = ((75.0, 'enterTopLogoRange'), (3.0, 'enterInteractiveRange'))
        self.clientOuterRange = ((85.0, 'leaveTopLogoRange'), (4.0, 'leaveInteractiveRange'), (const.NPC_USE_DIST * 1.0, 'leaveDlgRange'))
        self.curAttackTarget = None
        self.attackDistance = 2
        self.schedule = None
        self.isAscending = False
        self.castSkillBusy = False
        self.attackBusy = False
        self.autoUseSkill = False
        self.mouseMidKeydown = False
        self.lockHotKey = 0
        self.lockMouseKey = 0
        self.isChargeKeyDown = False
        self.roundCurNotFinishedCnt = 1
        self.isPathfinding = False
        self.isLockYaw = False
        self.isForceMove = gameglobal.FORCE_MOVE_NONE
        self.inDanDao = False
        self.danDaoUseDir = False
        self.miniGameSerialNumber = None
        self.spellingType = action.S_DEFAULT
        self.isGuiding = const.GUIDE_TYPE_NONE
        self.guideSkillCancelMode = gameglobal.GUIDESKILL_CANCEL_NOMAL
        self.lastUseSkillId = None
        self.lastTargetLocked = None
        self.chargeSkillKeyTime = None
        self.startMovingTime = BigWorld.time()
        self.endMovingTime = BigWorld.time()
        self.tLastMoving = 0
        self.lastStopMoveTime = 0
        self.isWaitSkillReturn = False
        self.afterLoadShowAchievement = False
        self.weaponTypes = {'leftWeapon': 0,
         'rightWeapon': 0}
        self.lastSyncTime = BigWorld.time()
        self.idleLastCheckTime = BigWorld.time()
        self.idleTimeCount = 0
        self.touchAirWallProcess = 0
        self.clientControl = True
        self.inForceMove = False
        self.lastSpaceNo = 0
        self.isGuaJiState = False
        self.dropForBlood = (0, 0)
        self.exception = exceptChannel.ExceptChannel(True, False)
        if self.inWorld:
            self.enterWorld(0)
        if gameglobal.rds.GameState != gametypes.GS_LOADING:
            if gameglobal.rds.isSinglePlayer:
                gameglobal.rds.cam.configCamera()
            loadingProgress.instance().show(True)
            gameglobal.rds.cam.cc.firstPerson = 1
        if hasattr(BigWorld, 'detachScreenEffect'):
            BigWorld.detachScreenEffect()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LOGIN_WIN)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LOGINLOGOTIPS2)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LOGINLOGO)
        self.oldPlayerStateSet = set([])
        self.oldTargetStateSet = set([])
        self.oldMasterStateSet = set([])
        self.oldPartStateSet = set([])
        gameglobal.rds.bar = None
        gameglobal.rds.soltId = None
        self.excludeCam = False
        if not hasattr(self, 'spaceNo'):
            self.spaceNo = 0
        self.showWorldGUI = True
        self.lastRegenTime = 0.0
        self.lastEpRegenTime = 0.0
        self.skillLog = [None, None]
        self.isInPhase = False
        self.phaseBounds = None
        self.checkPhaseAreaCallback = None
        self.confirmBtn = None
        self.isReturnToLogin = False
        self.collideWithPlayer = True
        self.hideNpcs = {}
        self.isPin = False
        self.confusionalState = gameglobal.CONFUSIONAL_DEFAULT
        self.inDyingEntities = []
        self.holdingSkills = []
        self.lvUpRewardData = {}
        self.stateAttrCache = None
        self.wingStateTime = (0, 0)
        self.buildingProxy = buildingProxy.BuildingProxyMgr()
        self.navigatorRouter = navigatorRouter.NavigatorRouter()
        BigWorld.enableBkgAnimLoad(True)
        self.inSlowTime = 0
        self.slowTimeNeedActions = []
        self.stageFinishCallback = None
        self.envHurtTimerId = 0
        self.lastEnvHurtTime = 0
        self.playDyingSoundId = 0
        self.playDyingEffect = False
        self.playDyingCallback = None
        self.oldCurrentScrollNum = 0
        self.msgCache = []
        self.trapCD = {}
        self.autoSkill = autoSkill.AutoSkillMgr(self)
        self.lockEnemy = False
        self.observedMembers = {}
        self.observedMembersPos = {}
        self.todayGiveInheritCnt = 0
        self.todayRecvInheritCnt = 0
        self.circleShapes = []
        for fxId in SCD.data.get('sfxCircleShapes', gameglobal.SFX_CIRCLE_SHAPES):
            fx = clientUtils.pixieFetch(sfx.getPath(fxId))
            if fx:
                fx.enableTerrainTouch(False)
            self.circleShapes.append(fx)

        self.circleShapeCallback = None
        self.selfEffectLv = gameglobal.EFFECT_MID
        self.monsterEffectLv = gameglobal.EFFECT_MID
        self.otherAvatarEffectLv = gameglobal.EFFECT_MID
        self.spaceEffectLv = gameglobal.EFFECT_MID
        self.enemyAvatarEffectLv = gameglobal.EFFECT_MID
        self.npcEffectLv = gameglobal.EFFECT_MID
        self.members = {}
        self.smallTeamGbIds = []
        self.bfMemStats = []
        self.bfSideStats = {}
        self.battleFieldTeam = {}
        self.bfTimeRec = {}
        self.bfFlagInfo = {}
        self.bfFortInfo = {}
        self.bfPlaneInfo = {}
        self.bfPlanePosInfo = []
        self.bfScore = {}
        self.bfResultInfo = {}
        self.bfSideIndex = 0
        self.bfSideNUID = 0
        self.bfHeaderGbId = 0
        self.bfGroupNeedOpen = True
        self.bfIsJumpWeakSide = False
        self.isBfTroopLogon = False
        self.sscStage = -1
        self.isNeedRefreshCounting = False
        self.arenaTeam = {}
        self.groupMapMark = {}
        self.bfDuelStats = {}
        self.battleFieldFbNo = 0
        self.arrangeDict = {}
        self.bfArrange = []
        self.isOnLoaded = False
        self.isMemoryLoadedNotified = False
        self.qingGongTimePair = (0, 0, 0)
        self.showCoupleEmoteRequest = None
        self.showRideTogetherRequest = None
        self.showRideTogetherApplyRequest = None
        self.selectTeamerByTabIdx = 0
        self.preloaded = False
        self.dailyAttendShowed = False
        self.nosDownListCallbacks = {}
        self.nosStatusFetchCallbacks = {}
        self.nosStatusFetchCallbacksTimeStamp = {}
        self.nosFileStatusCache = {}
        self.nosFileStatusTimeStamp = {}
        self.tabTargetCandidates = []
        self.tabTargetIdx = 0
        self.lastTabTime = 0
        self.forbidApplyShader = False
        self.shaderHandle = None
        self.othersInfo = {}
        self.observeOthersInfo = {}
        self.oldPkDefenseGbIdList = []
        self.hasQuestRepaired = False
        self.availableMorpher = {}
        self.questInfoCache = {}
        self.questLoopModifyTimer = 0
        self.inAutoQuest = False
        self.lastCompletedQuestInfo = {}
        self.autoQuestLoopId = 0
        self.autoQuestTimer = None
        self.autoQuestLastPos = None
        self.refundCoins = {}
        self.spaceClientEntities = {}
        self.jingsuTotalTuneTime = 0
        self.mentorGbId = 0
        self.matesGbIds = []
        self.apprenticeGbIds = []
        self.apprenticeGraduateFlag = 0
        self.hasPushLatencyMsg = False
        self.fbPunish = {}
        self.moveEndTime = 0
        self.intimacyTgtEnter = False
        self.intimacyTgtId = None
        self.sprintCount = 0
        self.clientPersistentNotifyList = {}
        self.mingpaiInfo = {}
        self.selectedMPId = 0
        self.yabiaoZaijuInfo = (1, 1)
        self.clientTransportList = []
        self.gtnLiveType = 0
        self.teleportCB = None
        self.disturb = {}
        self.myWishMsg = []
        self.personalSignatureList = []
        self.fearCB = None
        self.meiHuoCB = None
        self.chaoFengCB = None
        self.speedFieldCB = None
        self.latestZiXunTime = 0
        self.rewardHall = {}
        self.inInteractiveObjTemp = None
        self.soleMentorGbId = 0
        self.soleApprenticeGbId = 0
        self.mentorRejectOptEx = 0
        self.apprenticeRejectOptEx = 0
        self.interactiveObjStoryLastTime = 0
        self.shaXingSignUpWaitMsgId = None
        self.ckBoxHideMyJieqi = 0
        self.zoneMsgPermission = 0
        self.zoneHeadIconPermission = 0
        self.fudanDict = {}
        self.hierogramDict = {}
        self.groupMark = {}
        self.lastPathFindInfo = {}
        self.clientGroupFollowInfo = {}
        self.delayGroupFollow = False
        self.groupFollowAutoAttackFlag = False
        self.delayGroupFollowType = 0
        self.groupFollowHeaderGroundPos = None
        self.groupFollowHeaderSpaceNo = None
        self.groupFollowHeaderInPathFinding = False
        self.groupFollowHeaderPathCallback = None
        self.headerPathCache = None
        self.evaluateInfo = {}
        self.WSSchemeInfo = {}
        self.secondEscPlayScenarioFlag = bytearray('')
        gameglobal.rds.ui.friend.initTempMsg()
        self.gameMsgCDDict = {}
        self.sharedCnt = 0
        self.pgBreaker = 0
        self.speedField = None
        self.inSimpleQte = None
        self.chaseEntityCallback = None
        self.resetWeeklySig = False
        self.transportIdSet = set()
        self.holdPreloadDotaZaijuModel = {}
        self.preloadDotaZaijuFetchs = {}
        self.isNewFameRecord = {}
        self.bfDotaZaijuRecord = {}
        self.bfTeammateInfo = {}
        self.bfEnemyInfo = {}
        self.bfDotaTalentSkillRecord = {}
        self.isInBfDotaChooseHero = False
        self.selfSideDotaEntityIdSet = set()
        self.bfDotaSkillInitRecord = {}
        self.reliveTimeRecord = {}
        self.isNewFameRecord = {}
        self.currentWorldRefreshQuestInfo = {}
        self.bfMemPerforms = []
        self.bfEnd = False
        self.bfHistoryVers = [0,
         0,
         0,
         0,
         0,
         0]
        self.bfHistoryInfo = {'battleFieldFortHistory': {},
         'battleFieldResHistory': {},
         'battleFieldFlagHistory': {},
         'battleFieldNewFlagHistory': {},
         'battleFieldCqzzHistory': {},
         'battleFieldPUBGHistory': {}}
        self.registerEvent(const.EVENT_ITEM_CHANGE, gameglobal.rds.ui.buffSkill.refreshItemChange)
        self.registerEvent(const.EVENT_ITEM_REMOVE, gameglobal.rds.ui.buffSkill.onItemRemove)
        self.summonedSpriteInWorld = None
        self.summonedSpriteLifeList = []
        self.spriteBattleCallBackList = []
        self.changeToFollowStateCB = None
        self.favorEquipInfo = {}
        self.weekOperationActivityInfo = {}
        self.weekPrivilegeBuyInfo = {}
        self.summonSpriteSkin = summonSpriteAppearance.SummonSpriteAppearanceDict()
        self.summonSpriteFootDust = summonSpriteAppearance.SummonSpriteAppearanceDict()
        self.weekPrivilegeBuyInfo = {}
        self.itemWishConfirmInfo = {}
        self.personalZoneSkin = personalZoneSkin.PersonalZoneSkinDict()
        if clientcom.enalbePreOpenCEF():
            CEFControl.openCEFProgress()
        self.bfDotaEntityIdRecord = {}
        self.visibleBfDotaEnemyIdSet = set()
        self.canRemoveSkillEnhances = {}
        self.spriteChats = spriteChat.SpriteChatDict()
        self.spriteWingWorldRes = spriteWingWorldRes.SpriteWingWorldRes()
        self.friendRecallStatics = {}
        self.wingWorldMiniMap = WingWorldCityMinMap()
        game.cancelTick()
        self.firstOnlineForRefore = True
        self.xinMoAnnalFakeCnt = 0
        self.roleSaleData = RoleSaleData()
        for initAttr in const.CLIENT_PLAYER_INIT_ATTRS:
            if not hasattr(self, initAttr[0]):
                setattr(self, initAttr[0], initAttr[1])

        self.aoiAvatarCnt = 0
        self.ftbDataDetail = FtbDataHelper()
        self.wingWorldForgeData = WingWorldForge()
        self.wardrobeBag = WardrobeClient()
        self.rejectChatGroupInviteOp = 0
        self.autoPickSetting = {}
        self.autoFilterSetting = {}
        self.autoPickEnable = True
        self.curPoisonCircleData = []
        self.curPUBGStateProgress = 0
        self.curPUBGNumsData = [0,
         0,
         0,
         0,
         0]
        self.allTeammateMapMark = {}
        self.curAirPlaneData = {}
        self.curDisasterDataInPUBG = {}
        self.curDisasterEndCBInPUBG = None
        self.curBossInPUBG = {}
        self.curTreasureBoxInPUBG = {}
        self.curTeamMemberInPUBG = {}
        self.pubgSkills = {}
        self.curCanEquipListInPUBG = []
        self.curEquippingInPUBGCB = False
        self.skyZoneDataInPUBGCB = None
        self.playSoundInPUBGCB = None
        self.isCanRegenMpInPUBG = True
        self.playerRankPointMarkData = None
        self.playerAllBattleData = dict()
        self.challengePassportData = ChallengePassportDataHelper()
        self.localClanChallengeCombatResult = {}
        self.localClanChallengeMemberInfo = {}
        self.localClanChallengeMemberDetail = {}
        self.localClanWarChallengeBaseInfo = {}
        self.localTargetChallengeGuild = {}
        self.localClanWarChallengeState = None
        self.crossClanChallengeCombatResult = {}
        self.crossClanChallengeMemberInfo = {}
        self.crossClanChallengeMemberDetail = {}
        self.crossClanWarChallengeBaseInfo = {}
        self.crossTargetChallengeGuild = {}
        self.crossClanWarChallengeStage = None
        logicInfo.cooldownClanWarSkill = {}
        self.missTianyuState = gametypes.MISS_TIANYU_CLOSE
        self.straightUpTask = {}
        self.anonymNameMgr = AnonymousNameManager.getInstance()
        self.gameAntiCheatingManager = gameAntiCheatingManager.getInstance()
        self.realNameState = const.REALNAME_STATE_NOT_CHECK
        self.curPlayerAge = 18
        self.monthRechargeLimit = -1
        self.betDatas = []
        self.myBetDict = {}
        self.spriteChallengeInfo = {}
        self.spriteChallengeResult = {}
        self.spriteChallengeList = []
        self.spriteChallengeProgress = 0
        self.bonusHistory = {}
        self.clanCourierDic = {}
        self.summonSpriteSEOrder = {}

    def MRACOnline(self):
        module = None
        try:
            import MRAC as module
        except:
            pass

        if module and module.enabled():
            module.onLine(str(self.gbId))

    def MRACOffline(self):
        module = None
        try:
            import MRAC as module
        except:
            pass

        if module and module.enabled():
            module.offLine()

    def enterWorld(self, initial = 1):
        gameglobal.rds.ui.startRecordShowList()
        BigWorld.callback(2, self.callAfterEnterWorld)
        if initial:
            sfx.gEffectMgr.LRUEffectCache.realClearEffectCache()
            sfx.gEffectMgr.oldEffectCache.realClearEffectCache()
            Avatar.enterWorld(self)
            gameglobal.rds.ui.characterCreate.clear()
            gameglobal.rds.ui.characterCreateSelectNew.hide()
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHARACTER_NAVIGATION)
            gameglobal.rds.ui.unLoadWidget(uiConst.BUTTON_CHARACTER_NEXT)
            if gameglobal.rds.ui.chat.chatLogWindowMC:
                self.showGameMsg(GMDD.data.HELLO_WORD, ())
            else:
                gameglobal.rds.ui.chat.hasHelloWord = True
            gfeInst = getattr(gameglobal.rds, 'gfe', None)
            if gfeInst:
                gfeInst.initGfe()
        gameglobal.rds.loginManager.waitingForEnterGame = False
        BigWorld.enableLODAll(True)
        BigWorld.TextureStreamingPrio(3)
        BigWorld.setWindowTitle(1, self.roleName)
        PLD.freeTempPreload()
        self.filter = BigWorld.PlayerAvatarFilter()
        self.filter.feetDist = 0.1
        self._keyboardPhysics = keyboardPhysics.KeyboardPhysics()
        self._mousePhysics = mousePhysics.MousePhysics()
        self._actionPhysics = actionPhysics.ActionPhysics()
        self.physics = keys.STANDARD_PHYSICS
        self.physics.modelWidth = 1.2
        self.physics.modelDepth = 0.84
        self.physics.modelHeight = 1.8
        self.physics.scrambleHeight = 1.0
        self.lockEnemy = False
        self.selfEffectLv = gameglobal.EFFECT_MID
        self.monsterEffectLv = gameglobal.EFFECT_MID
        self.otherAvatarEffectLv = gameglobal.EFFECT_MID
        self.spaceEffectLv = gameglobal.EFFECT_MID
        self.enemyAvatarEffectLv = gameglobal.EFFECT_MID
        self.npcEffectLv = gameglobal.EFFECT_MID
        self.members = {}
        self.smallTeamGbIds = []
        self.memberGuideQuests = {}
        self.shortcutToPostion = False
        self.shortcutToPostionSkillId = 1
        BigWorld.renderFeatures('vsm', True)
        AppSettings.applySetting()
        self.shaderHandle = BigWorld.callback(0.5, setShaderIndex)
        self.startTime = time.clock()
        gameglobal.rds.ui.initHud()
        self.losePhysics()
        self.rightMouseAble = True
        loadingProgress.instance().startProgress(self._onLoaded)
        BigWorld.enableOfflineFocus(False)
        BigWorld.target.source = self.matrix
        BigWorld.target.updateBBoxFreq = 5
        BigWorld.target.enableGUI(True)
        BigWorld.target.exclude = self
        BigWorld.target.caps(keys.CAP_CAN_USE)
        BigWorld.dcursor().pitch = -0.2
        BigWorld.dcursor().yaw = self.yaw
        cam = gameglobal.rds.cam.cc
        cam.source = BigWorld.dcursor().matrix
        cam.target = BigWorld.PlayerMatrix()
        cam.set(self.matrix)
        cam.reverseView = False
        gameglobal.rds.cam.setAdaptiveFov()
        BigWorld.enableClearCameraSpace(True)
        BigWorld.enableCameraChange(True)
        game.cameraType(0)
        BigWorld.cameraBindPlayer(True)
        gameglobal.rds.cam.cc.target = BigWorld.PlayerMatrix()
        if not getattr(self, 'keyBindings', None):
            self.reload()
        self.circleEffect = sfx.CircleEffect()
        self.chooseEffect = sfx.ChooseEffect()
        self.stateMachine = clientSM.StateMachine(self.id)
        self.autoSkill.init()
        if gameglobal.rds.GameState >= gametypes.GS_LOADING:
            self.checkStatus()
        self.resetCamera()
        stateSafe.beginCheck()
        self._updateEntityDropFilter()
        self.enterTopLogoRange()
        self.set_spaceNo(self.spaceNo)
        if not gameglobal.KEEP_HIDE_MODE_CUSTOM:
            gameglobal.gHideMode = gameglobal.HIDE_MODE0
            gameglobal.HIDE_MODE_CUSTOM = 0
            gameglobal.gHideMonsterFlag = gameglobal.HIDE_NO_MONSTER
        else:
            self.refreshCurrMode()
        if self.isolateType != gametypes.ISOLATE_TYPE_NONE:
            self.hidePlayerNearby(gameglobal.HIDE_ALL_PLAYER)
        elif not gameglobal.KEEP_HIDE_MODE_CUSTOM:
            gameglobal.gHideOtherPlayerFlag = gameglobal.HIDE_NOBODY
        gameglobal.KEEP_HIDE_MODE_CUSTOM = False
        self.setPlayerLogonData()
        self.questMonsterInfo = self._getQuestMonsterInfo()
        inWaterStateSound.setInWaterCallback()
        updateAmbientMusic.startAmbientSound()
        BigWorld.setWindowTitle(1, self.roleName)
        BigWorld.setWindowTitle(2, '@%d' % (self.clientDBID,))
        BigWorld.setWindowTitle(3, '%d' % (self.id,))
        Hijack.hijack_check(0)
        gameglobal.rds.gbId = self.gbId
        protect.nepRoleLogin(self.roleURS, self.roleName, self.gbId, self.lv)
        self.qingGongTimePair = (0, 0, 0)
        self.showCoupleEmoteRequest = None
        self.showRideTogetherRequest = None
        self.showRideTogetherApplyRequest = None
        if self.novice:
            self.needPlayIntro = True
            self.needConfigOp = True
        else:
            self.needPlayIntro = False
            self.needConfigOp = False
        spriteLv = SCD.data.get('showSprite', 17)
        if self.lv >= spriteLv and gameglobal.rds.ui.spriteAni.getSetting():
            gameglobal.rds.ui.spriteAni.show()
        migratePushLv = MICD.data.get('migratePushLv', 40)
        if self.lv >= migratePushLv:
            gameglobal.rds.ui.migrateServer.pushMigrate()
        self.set_carnivalBonusInfo(None)
        BigWorld.callback(0.1, self.logClientInfo)
        BigWorld.callback(0.1, self.logClientSetting)
        self.applyRewardCode()
        self.entityDebugNameFactory = entityDebugNameFactory.getInstance()
        self.onEnterSpace()
        gameglobal.rds.ui.topBar.startXingJiTimer()
        gameglobal.rds.ui.summonedSpriteUnitFrameV2.show()
        gameglobal.rds.ui.rewardGiftActivityIcons.show()
        gameglobal.rds.ui.buffListenerShow.show()
        self.reCalcBuffListenerIds()
        self.setSafeModeState()
        gameglobal.rds.ui.chat.refreshChannel()
        gameglobal.rds.ui.kejuGuide.checkKejuState()
        miniclient.avatarEnterWorld(self.gbId, self.lv)
        gameglobal.rds.ui.loginWin.userName = self.roleURS
        gameglobal.rds.loginUserName = self.roleURS
        self.guildIconRefreshTime = 0
        self.guildFlagIconStatus = gametypes.NOS_FILE_STATUS_APPROVED
        if self.guildIcon:
            self.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, self.guildIcon, gametypes.NOS_FILE_PICTURE, self.onGuildIconDownloadNOSFile, (None,))
        self.refreshWingShare()
        self.refreshRideShare()
        self.refreshWingTemp()
        self.refreshRideTemp()
        self.hasDesktopShortcut = 2
        if hasattr(BigWorld, 'hasDesktopShortcut') and BigWorld.hasDesktopShortcut():
            self.hasDesktopShortcut = 1
        self.setConfigData()
        gameglobal.rds.ui.ime.enableIme()
        gameglobal.rds.ui.newGuiderOperationHint.showOrHide()
        if gameglobal.rds.configData.get('enableCCSelfUpdate', False):
            cc.checkUpdate()
        gameglobal.rds.ui.playRecomm.initIncompleteNotifyHandler(False)
        gameglobal.rds.ui.roleInfo.checkAllEquipStarLvUp()
        self.notifyMLDoubleExpFlag = False
        gameglobal.rds.needSendInfoToHttp = True
        gameglobal.rds.ui.questLog.checkActivityQuestAccepted()
        gameglobal.rds.ui.addNoviceHintPushMessage()
        gameglobal.rds.ui.bottle.notify()
        self.saveMemoryDBConfig()
        gameglobal.rds.ui.qinggongWingTutorialIcon.pushIcon(0)
        gameglobal.rds.ui.ziXunInfo.needAutoShow = True
        if gameglobal.rds.ui.roleInfo.titleNewTime == 0:
            gameglobal.rds.ui.roleInfo.titleNewTime = self.enterTimeOfDay
        BigWorld.player().cell.updateRandWingEnable(AppSettings.get(keys.SET_ENABLE_RAND_WING, 0))
        gameglobal.rds.ui.monsterClanWarActivity.checkRewardState()
        self.onEnterWorld()
        self.sendGadInfo()
        self.bfBulletInfo = {}
        self.base.getPersonalZoneConfig()
        if not self.marriageTgtEquipment:
            self.cell.queryMarriageAspect()
        BigWorld.callback(10, self.helloRuss)
        gameglobal.rds.ui.lifeSkillNew.addFishingPushMsg()
        self.base.checkXConsignClrResults()
        self.setXConsignStartCallBack()
        self.base.queryEvaluate()
        self.queryBonusHistory()
        self.thisEnterWorldTime = BigWorld.time()
        if utils.isInternationalVersion():
            self.MRACOnline()
        self.initTopLogoFontSize()
        enableGatherInputCache = gameglobal.rds.configData.get('enableGatherInputCache', -1)
        if enableGatherInputCache >= 0:
            if hasattr(BigWorld, 'setEnableGatherInputCacheNew'):
                BigWorld.setEnableGatherInputCacheNew(True)
                BigWorld.setGatherInputTime(enableGatherInputCache)
        self.monitor = performanceMonitor.PerformanceMonitor.getInstance()
        if gameglobal.rds.configData.get('enableWingWorldXinMo', False):
            gameglobal.rds.ui.wingStageChoose.currChoose = {}
            gameglobal.rds.ui.teamRankingList.data = None
        gameglobal.rds.ui.duelMatchTime.resetDuelMatch()
        self.quitWaitingArena()
        self.dArenaOnSyncTimeInfo(gametypes.DOUBLE_ARENA_STATE_CLOSE, 0)
        aspectHelper.getInstance().registerEvents()
        aspectHelper.getInstance().resetData()
        logicInfo.spriteManualSkillCoolDown = None
        if gameglobal.rds.ui.roleInformationJunjie.checkFamousGeneralLvUp():
            gameglobal.rds.ui.roleInformationJunjie.pushFamousGeneralLvUpMsg()
        self.cqzzFlagPosGetState = {}
        gameglobal.rds.ui.summonedSpriteUnitFrameV2.clearAwakeCD()
        sfx.G_MONSTER_LOCKED.clear()
        gameglobal.rds.ui.wingWorldOverView.queryCampNotice()
        self.initNpcFavor()
        self.creationVisibleByBuff = {}
        BigWorld.callback(2, self.callAfterEnterWorld)

    def callAfterEnterWorld(self):
        if not self.inWorld:
            return
        self.showSafeMode()
        self.base.getWSSchemesInfo()
        self.base.queryDailyWelfareBuyInfo()
        self.cell.queryWingWorldOpenStageInfo()
        self.base.queryHistoryConsumedStatus()
        gameglobal.rds.ui.activitySaleFirstPay.getRechargeInfo()
        gameglobal.rds.ui.arenaPlayoffsBet.notifyBetStartPushMsg()
        gameglobal.rds.ui.accountBind.addPushMsg()
        gameglobal.rds.ui.summonFriendNew.showMessageBox()
        gameglobal.rds.ui.summonFriendInviteV2.showMessageBox()
        gameglobal.rds.ui.celebrityRank.pushIcon()
        gameglobal.rds.ui.languageSetting.checkSetting()
        gameglobal.rds.ui.baiDiShiLianPush.tryStartTimer()
        gameglobal.rds.ui.wingWorldPush.tryStartTimer()
        if gameglobal.rds.configData.get('enableWingWorld', False):
            self.cell.queryWingWorldResume(self.wingWorld.state, self.wingWorld.briefVer, self.wingWorld.countryVer, self.wingWorld.cityVer, self.wingWorld.campVer)
            self.cell.queryWingWorldArmy(self.wingWorld.armyVer, self.wingWorld.armyOnlineVer)
            if gameglobal.rds.configData.get('enableWingWorldXinMo', False):
                gameglobal.rds.ui.wingCombatPush.tryStartTimer()
        if gameglobal.rds.configData.get('enableSpriteChallenge'):
            from guis import spriteChallengeHelper
            self.base.querySpriteChallengeInfo(spriteChallengeHelper.getInstance().getSelfLvKeyStr())
        if hasattr(self, '_isOnZaijuOrBianyao'):
            if self._isOnZaijuOrBianyao():
                zjd = ZJD.data.get(self._getZaijuOrBianyaoNo(), {})
                skills = tuple(zjd.get('skills', ())) + tuple(zjd.get('icons', ()))
                if zjd.get('replaceBar', 1) == 0:
                    self.showZaijuUI(skills=skills)
                else:
                    self.showZaijuUI(showType=uiConst.ZAIJU_SHOW_TYPE_EXIT)
        self.getExtraServerProgress()
        gameglobal.rds.ui.voidDreamland.tryAddPushInfo()
        BigWorld.player().cell.queryWingCelebrationActivityData()
        if getattr(self, 'schoolTopStage', {}).get(self.school, None) == gametypes.SCHOOL_TOP_STAGE_MATCH_START:
            self.base.querySchoolTopDetails()
        self.cell.querySchoolTopDpsTimesWeekly()
        gameglobal.rds.ui.pvPPanel.pushTodayActivityMsg()
        self.getTopicList()
        self.cell.queryClanWarApplyHost()
        self.refreshWingWorldQueueInfo()
        worldBossHelper.getInstance().onEnterWorld()
        if gameglobal.rds.configData.get('enableBet', False):
            self.base.queryAllBet()

    def initTopLogoFontSize(self):
        gameglobal.rds.ui.setTopLogoFontSize(AppSettings.get(keys.SET_UI_SCALEDATA_TOPLOGO, uiConst.DEFAULT_FONT_SIZE))

    def helloRuss(self):
        filePath = PG_FILE_PATH
        if not getattr(gameglobal.rds, 'clientPackageCheckData', ''):
            return
        try:
            blockSize = getsize(filePath) / BLOCK_SIZE
            pgPlainTextMd5 = gameglobal.rds.clientPackageCheckData
            lines = pgPlainTextMd5.split('\n')
            line_count = int(lines[0], 10)
            blockSize = min(blockSize, line_count)
            blockNums = random.sample(xrange(blockSize - 1), 10)
            with open(filePath, 'rb') as f:
                for blockNum in blockNums:
                    f.seek(BLOCK_SIZE * blockNum)
                    bytes = f.read(BLOCK_SIZE)
                    same = pg_protect.ChecksumMd5(bytes, blockNum, pgPlainTextMd5)
                    if not same:
                        self.pgBreaker = 1
                        return

            self.pgBreaker = 0
        except Exception as e:
            gamelog.info('----m.l@Avatar.helloRuss', e.message)

    def sendGadInfo(self):
        try:
            netWork.sendGadInfo(gameglobal.rds.loginUserName, gameglobal.rds.clientInfo.mac_info)
        except:
            pass

    def saveMemoryDBConfig(self):
        memoryDBRate = gameglobal.rds.configData.get('memoryDBRate', 0)
        appSetting.VideoQualitySettingObj.setMemoryRate(memoryDBRate)
        AppSettings.save()

    def applyRewardCode(self):
        self.applyRewardHandler = None
        if getattr(gameglobal.rds, 'gameCode', None):
            gameCode = gameglobal.rds.gameCode.strip()
            if gameglobal.rds.isFeiHuo:
                gameCodeSendTime = SCD.data.get('feihuoGameCodeSendTime', 10.0)
            elif gameglobal.rds.isYiYou:
                gameCodeSendTime = SCD.data.get('yiyouGameCodeSendTime', 10.0)
            elif gameglobal.rds.isShunWang:
                gameCodeSendTime = SCD.data.get('shunwangGameCodeSendTime', 10.0)
            else:
                gameCodeSendTime = SCD.data.get('gameCodeSendTime', 10.0)
            self.applyRewardHandler = BigWorld.callback(gameCodeSendTime, Functor(self.base.applyRewardByCode, gameCode))

    def setConfigData(self):
        BigWorld.enablePerformance(True, gameglobal.LOG_PERFORMANCE_TIME)
        enableProxyDist = gameglobal.rds.configData.get('enableProxyDist', False)
        if enableProxyDist:
            if hasattr(BigWorld, 'proxyDist'):
                BigWorld.proxyDist(400)
        elif hasattr(BigWorld, 'proxyDist'):
            BigWorld.proxyDist(-1)

    def getSystemInfo(self):
        funcs = ['OSDesc',
         'CPUDesc',
         'CPUSerial',
         'CPUCores',
         'CPUFrequency',
         'PhysicsMemoryTotal',
         'PhysicsMemoryAvail',
         'VideoCardDesc',
         'VideoLocalMemoryTotal',
         'VideoLocalMemoryAvail',
         'procMemUsage']
        SystemInfo = []
        for funcName in funcs:
            f = getattr(BigWorld, funcName)
            v = None
            if funcName in ('CPUFrequency', 'CPUCurFrequency'):
                v = f(0)
            else:
                v = f()
            SystemInfo.append(str(v))

        return ';'.join(SystemInfo)

    def setPlayerLogonData(self):
        gamelog.debug('@zs Avatar.setPlayerLogonData', self.id)
        if not hasattr(gameglobal.rds, 'playerLogonData'):
            return
        data = gameglobal.rds.playerLogonData
        del gameglobal.rds.playerLogonData
        gamelog.debug('@zs set playerLogonData begin')
        invData = data.get('inv', None)
        if invData:
            invItemData, invBarItemData, posCountData, selectList, enabledPackSlotCnt = invData
            self.setInvPosCount(posCountData)
            self.batchResInsert(const.RES_KIND_INV, invItemData)
            self.batchInsertInvBar(invBarItemData)
            self.fashionBag.selectList = selectList
            self.setInvPackSlot(enabledPackSlotCnt)
        crossInvData = data.get('crossInv', None)
        if crossInvData:
            invItemData, invBarItemData, posCountData, selectList, enabledPackSlotCnt, reservedDict = crossInvData
            self.crossInv.posCountDict = posCountData
            self.crossInv.reservedDict = reservedDict
            self.batchResInsert(const.RES_KIND_CROSS_INV, invItemData)
        fashionBagData = data.get('fashionBag', None)
        if fashionBagData:
            activated, itemData, slotData, enabledPackSlotCnt, posCountDict = fashionBagData
            enabledSlotCnt = 0
            for item in posCountDict:
                enabledSlotCnt = enabledSlotCnt + posCountDict[item]

            needRefreshFashionBag = False
            if hasattr(self.fashionBag, 'enabledSlotCnt'):
                if self.fashionBag.enabledSlotCnt != enabledSlotCnt:
                    self.fashionBag.enabledSlotCnt = enabledSlotCnt
                    needRefreshFashionBag = True
            else:
                self.fashionBag.enabledSlotCnt = enabledSlotCnt
                needRefreshFashionBag = True
            self.fashionBagPackSlotEnlarge(enabledPackSlotCnt)
            self.fashionBag.posCountDict = posCountDict
            if needRefreshFashionBag:
                self.fashionBag.refreshContainer(self.fashionBag.enabledSlotCnt, const.FASHION_BAG_WIDTH, const.FASHION_BAG_HEIGHT)
                if gameglobal.rds.ui.fashionBag.mediator:
                    gameglobal.rds.ui.fashionBag.refreshBag()
            self.setResState(const.RES_KIND_FASHION_BAG, activated)
            self.batchResInsert(const.RES_KIND_FASHION_BAG, itemData)
            if slotData:
                self.batchInsertFashionBagBar(slotData)
        materialBagData = data.get('materialBag', None)
        gamelog.debug('materialBag', materialBagData)
        if materialBagData:
            activated, itemData, slotData, enabledPackSlotCnt, posCountDict = materialBagData
            self.materialBag.posCountDict = posCountDict
            self.setResState(const.RES_KIND_MATERIAL_BAG, activated)
            self.batchResInsert(const.RES_KIND_MATERIAL_BAG, itemData)
            self.materialBagPackSlotEnlarge(enabledPackSlotCnt)
            if slotData:
                self.batchInsertMaterialBagBar(slotData)
        spriteMaterialBagData = data.get('spriteMaterialBag', None)
        gamelog.debug('spriteMaterialBag', spriteMaterialBagData)
        if spriteMaterialBagData:
            activated, itemData, slotData, enabledPackSlotCnt, posCountDict = spriteMaterialBagData
            self.spriteMaterialBag.posCountDict = posCountDict
            self.setResState(const.RES_KIND_SPRITE_MATERIAL_BAG, activated)
            self.batchResInsert(const.RES_KIND_SPRITE_MATERIAL_BAG, itemData)
            self.spriteMaterialBagPackSlotEnlarge(enabledPackSlotCnt)
            if slotData:
                self.batchInsertSpriteMaterialBagBar(slotData)
        mallBagData = data.get('mallBag', None)
        if mallBagData:
            self.batchResInsert(const.RES_KIND_MALL_BAG, mallBagData)
        rideWingBagData = data.get('rideWingBag', None)
        if rideWingBagData:
            bagData, posCountDict = rideWingBagData
            self.batchResInsert(const.RES_KIND_RIDE_WING_BAG, bagData)
            self.rideWingBag.posCountDict = posCountDict
        cartData = data.get('cart', None)
        if cartData:
            self.batchResInsert(const.RES_KIND_CART, cartData)
        equipmentData = data.get('equipment', None)
        if equipmentData:
            self.batchInsertEquip(equipmentData)
        tempBagData = data.get('tempBag', None)
        if tempBagData:
            self.batchResInsert(const.RES_KIND_TEMP_BAG, tempBagData)
        storageData, barData, enabledPackSlotCnt, posCountDict = data.get('storage', (None,
         None,
         0,
         {}))
        if storageData:
            self.batchResInsert(const.RES_KIND_STORAGE, storageData)
        if barData:
            self.batchInsertStorageBar(barData)
        self.storage.enabledPackSlotCnt = enabledPackSlotCnt
        self.storage.posCountDict = posCountDict
        fishingEquipData = data.get('fishingEquip', None)
        if fishingEquipData:
            self.batchInsertFishingEquip(fishingEquipData)
        questBagData = data.get('questBag', None)
        if questBagData:
            self.batchResInsert(const.RES_KIND_QUEST_BAG, questBagData)
        exploreEquipData = data.get('exploreEquip', None)
        if exploreEquipData:
            self.batchInsertExploreEquip(exploreEquipData)
        lifeEquipData = data.get('lifeEquipment', None)
        if lifeEquipData:
            self.batchInsertLifeEquip(lifeEquipData)
        zaijuBagData = data.get('zaijuBag', None)
        if zaijuBagData:
            self.batchResInsert(const.RES_KIND_ZAIJU_BAG, zaijuBagData)
        subEquipmentData = data.get('subEquipment', None)
        if subEquipmentData:
            self.batchResInsert(const.RES_KIND_SUB_EQUIP_BAG, subEquipmentData)
        cardBagData = data.get('cardBag', None)
        if cardBagData:
            self.initCardBag(cardBagData)
        wardrobeBagData = data.get('wardrobeBag', None)
        self.initWardrobeBag(wardrobeBagData)
        hierogramBagData = data.get('hierogramBag', None)
        if hierogramBagData:
            activated, itemData, slotData, enabledPackSlotCnt, posCountDict = hierogramBagData
            self.hierogramBag.posCountDict = posCountDict
            self.setResState(const.RES_KIND_HIEROGRAM_BAG, activated)
            self.batchResInsert(const.RES_KIND_HIEROGRAM_BAG, itemData)
            self.commonBagPackSlotEnlarge(const.RES_KIND_HIEROGRAM_BAG, enabledPackSlotCnt)
            if slotData:
                self.batchInsertHierogramBagBar(slotData)

    def _onLoaded(self):
        if self is None:
            return
        if not self.inWorld:
            return
        enableUIGCControl = gameglobal.rds.configData.get('enableUIGCControl', True)
        if enableUIGCControl:
            if self.inFuben() and hasattr(gameglobal.rds.ui.movie, 'StopGC'):
                gameglobal.rds.ui.stopGC(True)
            else:
                gameglobal.rds.ui.stopGC(False)
        navigator.getNav().InitSeekNavsBySpaceNo(self.mapID)
        navigator.getNav().clearOtherNavs()
        gameglobal.rds.GameState = gametypes.GS_PLAYGAME
        BigWorld.worldDrawEnabled(True)
        if not gameglobal.rds.configData.get('enableNewCamera', False):
            if gameglobal.rds.ui.camera.isShow:
                gameglobal.rds.ui.camera.hide()
        elif gameglobal.rds.ui.cameraV2.isShow:
            gameglobal.rds.ui.cameraV2.hide()
        gameglobal.rds.ui.restoreUI()
        gameglobal.rds.ui.initHud()
        if gameglobal.rds.ui.map.isShow:
            gameglobal.rds.ui.map.findMe()
        self.unlockTarget()
        fbNo = formula.getFubenNo(self.spaceNo)
        gamelog.debug('hjx debug tutor _onLoaded', fbNo)
        if self.inFubenType(const.FB_TYPE_SHENGSICHANG):
            self.enterSSCBefore()
        elif self.inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
            self.enterTeamSSCBefore()
        elif self.inFubenTypes(const.FB_TYPE_ARENA):
            gameglobal.rds.ui.arenaWait.endArenaWait()
            self.enterArenaBefore()
        elif fbNo in FD.data:
            self.onEnterFuben(fbNo)
        elif self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            self.onBattleFieldLoaded(fbNo)
        else:
            gameglobal.rds.ui.teamComm.refreshMemberInfo()
            gameglobal.rds.ui.fuben.onCloseFubenReward()
            if gameglobal.rds.ui.compositeShop.isOpen:
                gameglobal.rds.ui.compositeShop.closeShop()
            if gameglobal.rds.ui.arenaWait.isShow:
                gameglobal.rds.ui.arenaWait.hide()
        if self.inFubenType(const.FB_TYPE_MARRIAGE_HALL):
            gameglobal.rds.ui.chat.goToMarriageHall()
            gameglobal.rds.ui.marryHallFunc.show()
        else:
            gameglobal.rds.ui.marryHallFunc.hide()
            gameglobal.rds.ui.marryRedPacket.hide()
        if self.checkMarriageHallMaidMsg():
            self.addMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_MAID_HALL)
        elif not self.checkMarriageHallMaidMsg(True):
            self.removeMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_MAID_HALL)
        if self.checkMarriageCarrierMsg():
            self.addMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_APPLY_CARRIER)
        elif not self.checkMarriageCarrierMsg(True):
            self.removeMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_APPLY_CARRIER)
        if self.checkMarriageRoomMaidMsg():
            self.addMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_ROOM)
        elif not self.checkMarriageRoomMaidMsg(True):
            self.removeMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_ROOM)
        if fbNo == const.FB_NO_MARRIAGE_CHINESE_HALL:
            gameglobal.rds.sound.playMusic(const.MARRIAGE_CHINESE_HALL_MUSIC_ID)
        if fbNo in const.FB_NO_MARRIAGE_ROOM_SET:
            gameglobal.rds.sound.playMusic(const.MARRIAGE_ROOM_MUSIC_ID)
            gameglobal.rds.sound.playAmbient(const.MARRIAGE_ROOM_SOUND_EFFECT_ID)
        if self.isInGroup():
            gameglobal.rds.ui.group.showGroupTeam()
        if self.isShowFeedbackIcon():
            gameglobal.rds.ui.feedback.startCallBack()
        if self.life == gametypes.LIFE_DEAD and gameglobal.rds.ui.deadAndRelive.isShow:
            BigWorld.beginGrayFilter(3)
            gameglobal.rds.ui.deadAndRelive.hide()
            if gameglobal.rds.ui.fbDeadData.mediator:
                gameglobal.rds.ui.fbDeadData.hide()
            if gameglobal.rds.ui.fbDeadDetailData.mediator:
                gameglobal.rds.ui.fbDeadDetailData.hide()
            reliveHereEnable = not (self.touchAirWallProcess > 0 or self.downCliff > 0)
            spaceNo = formula.getMapId(self.spaceNo)
            reliveHereType = MCD.data.get(spaceNo, {}).get('reliveHereType', gametypes.RELIVE_HERE_TYPE_FORBID)
            if uiUtils.isInFubenShishenLow():
                reliveHereType = gametypes.RELIVE_HERE_TYPE_NORMAL
            reliveHereEnable = reliveHereEnable and reliveHereType != gametypes.RELIVE_HERE_TYPE_FORBID
            reliveNearEnable = not MCD.data.get(spaceNo, {}).get('forbidReliveNear', 0) and self.canReliveNear
            gameglobal.rds.ui.deadAndRelive.show(reliveHereEnable, reliveNearEnable, False, None, reliveHereType)
            if self.inFubenTypes(const.FB_TYPE_GROUP_SET) and not self.canReliveNear:
                gameglobal.rds.ui.deadAndRelive.tip = 'BOSS战中暂时无法使用'
            else:
                gameglobal.rds.ui.deadAndRelive.tip = ''
        gameglobal.rds.ui.equipRepair.show()
        gameglobal.rds.ui.systemPush.refresh()
        if gameglobal.rds.ui.assign.isDiceShow:
            gameglobal.rds.ui.assign.closeDice()
            for item in gameglobal.rds.ui.assign.diceBag:
                gameglobal.rds.ui.assign.showDice(item[0], True, item[1])

        if menuManager.getInstance().MsgBoxId:
            gameglobal.rds.ui.messageBox.dismiss(menuManager.getInstance().MsgBoxId)
            menuManager.getInstance().MsgBoxId = None
        gameglobal.rds.ui.fuben.showFubenOneResultLoaded()
        self._updateEntityDropFilter()
        BigWorld.dcursor().yaw = self.yaw
        cam = gameglobal.rds.cam.cc
        cam.set(self.matrix)
        cam.turningHalfLife = 0
        cam.firstPerson = 0
        if self.ap:
            self.ap.stopMove()
            self.ap.reset()
            self.ap.inLoadingProgress = False
        if self.fashion:
            self.fashion.breakJump()
            self.fashion.breakFall()
        gameglobal.rds.tutorial.onLoginTrigger()
        noviceScenarioMap = SCD.data.get('noviceScenarioMap', {})
        if self.needPlayIntro and self.mapID in const.PLAY_CG_MAP_IDS:
            self.needPlayIntro = False
            BigWorld.worldDrawEnabled(False)
            gameglobal.noviceScenarioName = noviceScenarioMap.get((self.school, self.realPhysique.sex, self.realPhysique.bodyType), 'xsc4001.xml')
            self.scenarioPlay(gameglobal.noviceScenarioName, 0)
        else:
            gameglobal.rds.ui.dispatchEvent(events.EVENT_TYPE_SCENARIO_END)
        if self.needConfigOp:
            self.needConfigOp = False
            opMode = SD.data.get(self.school, {}).get('opMode', gameglobal.KEYBOARD_MODE)
            uiUtils.setAvatarPhysics(opMode, True)
            self.applyCommonOperation()
        gameglobal.rds.ui.actionbar.initAllSkillStat()
        BigWorld.callback(0.5, self.refreshPkToplogo)
        BigWorld.callback(0.5, self.refreshTopLogo)
        self.refreshFFLCreaterEnterPushMessage()
        loadingProgress.instance().inLoading = False
        if self.afterLoadShowAchievement == True:
            self.afterLoadShowAchievement = False
        gameglobal.rds.ui.fishingGame.checkNeedLoadByNotice()
        gameglobal.rds.sound.playPhaseMusic(self.mapID, self.isInPhase)
        self.scenarioPlayAfterTeleport()
        self.buildingProxy.spaceChanged()
        self.doLoadWingCityStaticBuildings()
        gameglobal.rds.cam.setAdaptiveFov()
        gameglobal.rds.ui.fangkadian.setArmorBtnVisible(True)
        if self.firstFetchFinished:
            self._preloadAll()
        if gameglobal.rds.ui.diGong.isShow:
            mlgNo = formula.getMLGNo(self.spaceNo)
            self.cell.queryLines(mlgNo)
        if gameglobal.rds.configData.get('enableWenQuanDetail', False) and hasattr(self, 'mapID') and self.mapID == const.ML_SPACE_NO_WENQUAN_FLOOR1:
            isWenquanAutoOpen = AppSettings.get(keys.SET_UI_AUTO_OPEN_WENQUAN_DETAIL, 1)
            if isWenquanAutoOpen and not gameglobal.rds.ui.wenQuanDetail.isShow:
                gameglobal.rds.ui.wenQuanDetail.show()
        if gameglobal.rds.configData.get('enableQuestRepair', False) and not self.hasQuestRepaired:
            self.hasQuestRepaired = True
            if commQuest.checkQuestAbnormalState(self):
                MBButton = messageBoxProxy.MBButton
                buttons = [MBButton('确定', Functor(self.cell.repairQuestStatus)), MBButton('取消')]
                gameglobal.rds.ui.messageBox.show(False, '', '任务状态不一致，是否选择修复？', buttons)
        self.showArmorMsg()
        self.showCancelHideInDiGong()
        gameglobal.rds.ui.chat.setBottomButton()
        self.showQuickJoinGroup()
        if not self.isOnLoaded:
            self.isOnLoaded = True
        self.playTeleportSpellLeave()
        if gameglobal.rds.configData.get('enableSetTeleportPitch', True):
            BigWorld.dcursor().pitch = SCD.data.get('teleportPitch', -0.2)
        if self.inFightObserve():
            gameglobal.rds.ui.showEnterObserveModeState()
            gameglobal.rds.ui.fightObserve.showActionBar()
            gameglobal.rds.ui.teamComm.refreshMemberInfo(1)
            gameglobal.rds.ui.player.resetPlayerUFOpacity()
            self.refreshFollowAvatarClient()
            gameglobal.rds.cam.reset()
        fubenNo = formula.getFubenNo(self.spaceNo)
        lastFubenNo = formula.getFubenNo(self.lastSpaceNo)
        if gameglobal.rds.ui.questTrack.needHideQuestTrack(fubenNo) or gameglobal.rds.ui.questTrack.needHideQuestTrack(lastFubenNo):
            gameglobal.rds.ui.questTrack.resetQuestTrackOpacity()
        if self.spaceInHomeOrLargeRoom():
            self.onEnterHomeRoom()
        gameglobal.rds.ui.actionbar.updateEmoteItemCooldown()
        self.onResetWeekly()
        mapId = formula.getMapId(self.spaceNo)
        if mapId == const.SPACE_NO_BIG_WORLD or formula.spaceInWingBornIsland(self.spaceNo):
            gameglobal.rds.ui.rewardGiftActivityIcons.show()
            gameglobal.rds.ui.excitementIcon.show()
            gameglobal.rds.ui.wingWorldPush.checkState()
        self.refreshPartnerTitle()
        keyboardEffect.addKeyboardEffect('effect_background')
        keyboardEffect.addWASDEffect()
        keyboardEffect.updateHpEffect()
        if self.groupHeader == self.id:
            self.syncHeaderClientGroundPos(force=True)
            self.cell.startGroupHeaderFollowSync()
        if getattr(self, 'delayGroupFollow', None) and getattr(self, 'inGroupFollow', None):
            self.setTempGroupFollow()
        gameglobal.rds.ui.ziXunInfo.recordTime()
        if BigWorld.player().getFame(const.REFORGE_EQUIP_JUEXING_FAME_ID) >= 3 and self.firstOnlineForRefore:
            self.firstOnlineForRefore = False
            self.showGameMsg(GMDD.data.LIANQI_DICE_FAME_GE_THREE, ())
        if self.mapID == const.FB_NO_SCHOOL_TOP_MATCH:
            self.enterSchoolTopMatch()
        self.challengePassportData.onSceneLoaded()
        self.isInCrossClanWarStatus() and gameglobal.rds.ui.crossClanWarInfo.show()
        if self.pyqNewsNumTickId:
            tickManager.stopTick(self.pyqNewsNumTickId)
        self.pyqNewsNumTickId = tickManager.addTick(const.PERSONAL_ZONE_NEWS_NUM_CHECK_INTERVAL, self.getPyqNewNum)
        self.getPyqNewNum()
        if getattr(self, 'lingShiFlag', False):
            self.onLeaveLingShi()
            self.onEnterLingShi()
        gameglobal.rds.ui.activityGuide.checkPush()
        gameglobal.rds.ui.stopRecordShowList()
        if getattr(self, 'showStrightUpPop', False):
            self.showStrightUpPop = False
            gameglobal.rds.ui.straightUpPop.show()
        self.syncUseItemWish(self.useItemWish)
        apEffectEx = getattr(self, 'apEffectEx', None)
        if apEffectEx:
            apEffectEx.resetEffect()
        gameglobal.rds.ui.zmjActivityBossPanel.refreshPushMsg()
        self.addCampNoticeMessage()
        gameAntiCheatingManager.getInstance().startRecordLog()

    def playTeleportSpellLeave(self):
        enableTeleportSpell = gameglobal.rds.configData.get('enableTeleportSpell', False)
        if enableTeleportSpell:
            if self.life == gametypes.LIFE_DEAD:
                return
            if self.isInApprenticeTrain() or self.isInApprenticeBeTrain():
                return
            data = TSD.data.get(gameglobal.TELEPORT_SPELL_LEAVE_FUBEN)
            teleportAction = data.get('action')
            effect = data.get('effect')
            playSeq = []
            playSeq.append((teleportAction,
             [],
             action.TELEPORT_SPELL_ACTION,
             1,
             1.0,
             None))
            self.fashion.playActionWithFx(playSeq, action.TELEPORT_SPELL_ACTION, None, False, 0, 0)
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
             self.getSkillEffectPriority(),
             self.model,
             effect,
             sfx.EFFECT_LIMIT_MISC,
             gameglobal.EFFECT_LAST_TIME))

    def _updateEntityDropFilter(self):
        for pair in BigWorld.entities.items():
            ent = pair[1]
            if hasattr(ent.filter, 'updateDrop'):
                ent.filter.updateDrop()

    def restorePhysics(self):
        if gameglobal.rds.GameState == gametypes.GS_LOADING:
            return
        if getattr(self, 'physics', None):
            self.physics.isActive = True

    def checkStatus(self):
        super(PlayerAvatar, self).checkStatus()
        self.resetCamera()

    def leaveWorld(self):
        if hasattr(BigWorld, 'setEnableGatherInputCacheNew'):
            BigWorld.setEnableGatherInputCacheNew(False)
        self.onLeaveWorld()
        miniclient.avatarLeaveWorld()
        self.relogNotifyState = False
        self.isInCbgRoleSelling = False
        Hijack.hijack_uncheck()
        if self.playDyingEffect:
            screenEffect.delEffect(gameglobal.EFFECT_TAG_HP)
            self.playDyingEffect = False
            if self.playDyingSoundId > 0:
                Sound.stopFx(self.playDyingSoundId)
                self.playDyingSoundId = 0
        if not self.ap:
            return
        self.ap.ccamera.canRotate = False
        self.ap.dcursor.canRotate = False
        if self.ap.__class__.__name__ == 'KeyboardPhysics':
            self.ap.stopMoveExceptAuto()
        self.ap.release()
        if self.exception != None:
            self.exception.clear()
            self.exception = None
        Avatar.leaveWorld(self)
        self.models = []
        self._keyboardPhysics.downKeyBindings = None
        self._keyboardPhysics.keyBindings = None
        self._keyboardPhysics.player = None
        self._keyboardPhysics = None
        self._mousePhysics.downKeyBindings = None
        self._mousePhysics.keyBindings = None
        self._mousePhysics.player = None
        self._mousePhysics = None
        self._actionPhysics.downKeyBindings = None
        self._actionPhysics.keyBindings = None
        self._actionPhysics.player = None
        self._actionPhysics = None
        self.physics.clear()
        self.stateMachine.player = None
        self.stateMachine = None
        mds = self.models
        for m in mds:
            if m:
                self.delModel(m)

        self.target = None
        self.targetLocked = None
        self.lastTargetLocked = None
        stateSafe.stopCheck()
        Sound.stopStateFx()
        BigWorld.checkFashionInvisible(0)
        loadingProgress.gLastSpace = ''
        BigWorld.setWindowTitle(1, '')
        updateAmbientMusic.endAmbientSound()
        self.inDyingEntities = []
        self.clearShapeEffect()
        if getattr(self, 'logCallback', 0):
            BigWorld.cancelCallback(self.logCallback)
        self.autoSkill.release()
        self.autoSkill = None
        game.tick()
        self.buildingProxy.clearAll()
        self.navigatorRouter.release()
        self.navigatorRouter = None
        self.msgCache = []
        self.trapCD = {}
        self.preloaded = False
        self.applyTimeDict = {}
        self.phaseBounds = None
        self.confirmBtn = None
        if self.checkPhaseAreaCallback:
            BigWorld.cancelCallback(self.checkPhaseAreaCallback)
            self.checkPhaseAreaCallback = None
        if deadPlayBack.getInstance():
            deadPlayBack.getInstance().resetTimer()
        if self.questLoopModifyTimer > 0:
            BigWorld.cancelCallback(self.questLoopModifyTimer)
        if getattr(self, 'wingSpeedShareTimeCallBack', 0):
            BigWorld.cancelCallback(self.wingSpeedShareTimeCallBack)
            self.wingSpeedShareTimeCallBack = 0
        if getattr(self, 'rideSpeedShareTimeCallBack', 0):
            BigWorld.cancelCallback(self.rideSpeedShareTimeCallBack)
            self.rideSpeedShareTimeCallBack = 0
        if getattr(self, 'wingSpeedTmpTimeCallBack', 0):
            BigWorld.cancelCallback(self.wingSpeedTmpTimeCallBack)
            self.wingSpeedShareTimeCallBack = 0
        if getattr(self, 'rideSpeedTmpTimeCallBack', 0):
            BigWorld.cancelCallback(self.rideSpeedTmpTimeCallBack)
            self.rideSpeedShareTimeCallBack = 0
        applyRewardHandler = getattr(self, 'applyRewardHandler', 0)
        if applyRewardHandler:
            BigWorld.cancelCallback(applyRewardHandler)
        if not hasattr(gameglobal.rds, 'transServerInfo') or not gameglobal.rds.transServerInfo:
            gameglobal.rds.notifiedActs.clear()
        loadingProgress.instance().enableGuildloadCheck = False
        self.unRegisterEvent(const.EVENT_ITEM_CHANGE, gameglobal.rds.ui.buffSkill.refreshItemChange)
        self.unRegisterEvent(const.EVENT_ITEM_REMOVE, gameglobal.rds.ui.buffSkill.onItemRemove)
        if utils.isInternationalVersion():
            self.MRACOffline()
        keyboardEffect.removeKeyboardEffect('effect_background')
        topLogo.TopLogoObj.getInstance().clear_cache()
        if self.monitor:
            self.monitor.clearAll()
            self.monitor = None
        gameglobal.rds.ui.rankCommon.clearCache()
        gameglobal.rds.ui.newServiceFirstKill.clearCache()
        gameglobal.rds.ui.huntGhost.stopTick()
        self.ftbDataDetail.clear()
        self.ftbDataDetail = None
        worldBossHelper.getInstance().stopTick()
        appSetting.restoreShader()
        sceneInfo.gAreaEventObj.release()
        worldBossHelper.getInstance().clearBossInfos()
        if getattr(self, 'enterTeamSSCCallBack', None):
            BigWorld.cancelCallback(self.enterTeamSSCCallBack)

    def losePhysics(self):
        if hasattr(self, 'physics') and self.physics:
            self.physics.isActive = False

    def setRightMouseAble(self, rightMouseAble):
        if rightMouseAble == False and self.ap._msright:
            self.ap._key_mr_down(False)
        self.rightMouseAble = rightMouseAble

    def setPhysics(self, physicsMode = gameglobal.KEYBOARD_MODE):
        if not self.inWorld or not self._keyboardPhysics:
            return
        gamelog.debug('setPhysics', self.ap, self.physics, self._keyboardPhysics, self._mousePhysics)
        if self.ap:
            self.ap.stopChasing()
            self.ap.restore()
            self.ap.stopMove()
            self.ap.navigation.stop()
            self.ap.releaseTargetLockedEffect()
        if physicsMode == gameglobal.KEYBOARD_MODE:
            HK.hotkeyMap = copy.deepcopy(HK.DefaultHotkeyMap)
            HK.HKM = HK.hotkeyMap
            self.ap = self._keyboardPhysics
            self.physics.jumpEndNotifier = self._keyboardPhysics.jumpEnd
            self.physics.breakJumpNotifier = self._keyboardPhysics.breakJumpCallback
            self.physics.collideNotifier = self._keyboardPhysics.collideCallback
            self.physics.actionPromoteNotifier = self._keyboardPhysics.actionPromoteCallback
        elif physicsMode == gameglobal.MOUSE_MODE:
            HK.hotkeyMap = copy.deepcopy(HK.WanMeiHotkeyMap)
            HK.HKM = HK.hotkeyMap
            self.ap = self._mousePhysics
            self.physics.jumpEndNotifier = self._mousePhysics.jumpEnd
            self.physics.breakJumpNotifier = self._mousePhysics.breakJumpCallback
            self.physics.collideNotifier = self._mousePhysics.collideCallback
            self.physics.actionPromoteNotifier = self._mousePhysics.actionPromoteCallback
        else:
            HK.hotkeyMap = copy.deepcopy(HK.BnsHotkeyMap)
            HK.HKM = HK.hotkeyMap
            self.ap = self._actionPhysics
            self.physics.jumpEndNotifier = self._actionPhysics.jumpEnd
            self.physics.breakJumpNotifier = self._actionPhysics.breakJumpCallback
            self.physics.collideNotifier = self._actionPhysics.collideCallback
            self.physics.actionPromoteNotifier = self._actionPhysics.actionPromoteCallback
        self.physics.upSpeedAttenu = 0
        self.ap.setPlayerPhysics(self, keys.STANDARD_PHYSICS)
        self.doLoadHotKey()
        self.ap._recalcSpeed()
        self.updateWalkSpeed()
        gameglobal.rds.cam.resetDcursorPitch()
        gameglobal.rds.ui.actionbar.refreshActionbar()

    def entityLeaveWorld(self, entity):
        if self.targetLocked == entity:
            self.unlockTarget()

    def useKey(self, isDown):
        if not isDown or self.life == gametypes.LIFE_DEAD:
            return
        if self.circleEffect.isShowingEffect:
            return
        isShowingEffect = self.chooseEffect.isShowingEffect
        if isShowingEffect:
            if self.target:
                self.chooseEffect.run(self.target)
                self.ap.reset()
                return
        if self.target != None and isDown:
            if self.targetLocked != self.target:
                if self.needUseKey():
                    self.lockTarget(self.target, lockAim=True)
                    self.ap.onTargetFocus(self.target, True)

    def needUseKey(self):
        if self.getOperationMode() == gameglobal.ACTION_MODE and not BigWorld.player().ap.showCursor:
            if self.isInApprenticeTrain() or self.isInApprenticeBeTrain():
                return True
            return False
        return True

    def escapeKey(self, isDown):
        gamelog.debug('jorsef: escape_key is pressed')
        if isDown:
            return
        scenarioIns = scenario.Scenario.PLAY_INSTANCE if scenario.Scenario.PLAY_INSTANCE else scenario.Scenario.INSTANCE
        if scenarioIns and gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            if not scenarioIns.editMode and not self.canSecondEsc(scenarioIns):
                if scenarioIns.canEsc:
                    gameglobal.rds.ui.scenarioBox.show()
                elif scenarioIns._canGroupEsc():
                    BigWorld.player().cell.scenarioGroupEsc()
                    if scenarioIns._canGroupSingleEsc():
                        BigWorld.player().scenarioStopPlay()
                else:
                    self.showGameMsg(self.getEscMsg(scenarioIns), ())
            else:
                scenarioIns.stopPlay()
            return
        if gameglobal.F12_MODE == gameglobal.F12_MODE_NOUI:
            self.showUI(True)
        elif self.isDoingAction:
            cellCmd.cancelAction(const.CANCEL_ACT_ESC)
        elif not gameglobal.rds.configData.get('enableNewCamera', False) and gameglobal.rds.ui.camera.isShow:
            if not gameglobal.rds.ui.camera.inPhotoing:
                gameglobal.rds.ui.camera.hide()
        elif gameglobal.rds.configData.get('enableNewCamera', False) and gameglobal.rds.ui.cameraV2.isShow:
            if not gameglobal.rds.ui.cameraV2.inPhotoing:
                gameglobal.rds.ui.cameraV2.hide()
        else:
            if gameglobal.rds.ui.chat.isInputAreaVisible:
                return
            if gameglobal.rds.ui.shop.inRepair:
                gameglobal.rds.ui.shop.clearRepairState()
            elif gameglobal.rds.ui.dragButton.isDragAble():
                gameglobal.rds.ui.dragTip.exitDrag()
            else:
                if gameglobal.rds.ui.guildFindStar.mediator and gameglobal.rds.ui.guildFindStar.needCloseMsgBox:
                    gameglobal.rds.ui.guildFindStar.close()
                    return
                if ccControl.ccBoxCmdParseManager.isFormOpen():
                    ccControl.ccBoxCmdParseManager.closeForm()
                else:
                    if gameglobal.rds.ui.closeTopByEsc():
                        return
                    if self.spellingType in [action.S_SPELLING] or self.isGuiding:
                        self.ap.cancelskill()
                    elif self.spellingType in [action.S_SPELLCHARGE]:
                        cellCmd.cancelSkill()
                    elif self.targetLocked is not None:
                        if self.getOperationMode() == gameglobal.ACTION_MODE:
                            lockAim = getattr(self.ap, 'lockAim', False)
                            if lockAim:
                                self.ap.lockAim = False
                                self.ap.onTargetBlur(self.targetLocked)
                                if getattr(self.targetLocked, 'life', gametypes.LIFE_ALIVE) == gametypes.LIFE_DEAD:
                                    self.unlockTarget()
                            else:
                                self.unlockTarget()
                                if getattr(menuManager.getInstance().menuTarget, 'menuId', 0) in (uiConst.MENU_ENTITY, uiConst.MENU_TARGET):
                                    gameglobal.rds.ui.hideAllMenu()
                                gameglobal.rds.ui.systemSettingV2.show()
                        else:
                            self.unlockTarget()
                    elif self.ap.groupMapMarkCircle.isInGroupMapMarkStatus():
                        self.ap.groupMapMarkCircle.stop()
                    elif BigWorld.player().circleEffect.isShowingEffect and BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE:
                        BigWorld.player().circleEffect.cancel()
                    elif BigWorld.player().chooseEffect.isShowingEffect:
                        BigWorld.player().chooseEffect.cancel()
                    elif not gameglobal.rds.ui.fuben.fubenRewardMed:
                        gameglobal.rds.ui.systemSettingV2.show()

    def targetFocus(self, entity):
        gamelog.debug('jjh.targetFocus', entity.id)
        self.target = entity
        entity.isInHover = True
        if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            return
        if not gameglobal.rds.configData.get('enableNewCamera', False):
            if gameglobal.rds.ui.camera.isShow:
                return
        elif gameglobal.rds.ui.cameraV2.isShow:
            return
        if not (self.getOperationMode() == gameglobal.ACTION_MODE and not self.ap.showCursor):
            if entity.canOutline():
                if editorHelper.instance().selectedEnt:
                    editorHelper.instance().targetFocus(self.target)
                else:
                    outlineHelper.setTarget(self.target)
            elif entity.canChangeDiffuseInFocus():
                entity.model.diffuseScale = SCD.data.get('diffuseScale', (1.3, 1.3, 1.3)) if entity.model else None
        if isinstance(entity, FishGroup):
            entity.showFishTips(True)
        try:
            if entity.canChangeTgtCursorInFocus():
                entity.onTargetCursor(True)
        except AttributeError:
            traceback.print_exc()
            gamelog.error("zf33:ERROR:entity can\'t set target cursor")

        if self.ap:
            if self.getOperationMode() == gameglobal.ACTION_MODE and not self.ap.showCursor:
                if entity != self.targetLocked:
                    self.ap.onTargetFocus(entity, False)
                elif self.ap.targetFadeTimer:
                    BigWorld.cancelCallback(self.ap.targetFadeTimer)

    def targetBlur(self, entity):
        self.target = None
        entity.isInHover = False
        if entity.canOutline():
            if editorHelper.instance().selectedEnt:
                editorHelper.instance().targetBlur(entity)
            else:
                outlineHelper.setTarget(None)
        elif entity.model:
            entity.model.diffuseScale = (1, 1, 1)
        try:
            entity.onTargetCursor(False)
        except AttributeError:
            traceback.print_exc()
            gamelog.error("zf33:ERROR:entity can\'t restore target cursor")

        if self.ap:
            if self.getOperationMode() == gameglobal.ACTION_MODE and not self.ap.showCursor:
                self.ap.onTargetBlur(entity)
        if isinstance(entity, FishGroup):
            entity.showFishTips(False)
        if self.isInBfDota():
            gameglobal.rds.ui.actionbar.bar = None
            gameglobal.rds.ui.actionbar.soltId = None

    def lockTarget(self, target, fromUIProxy = False, lockAim = False, quickLock = False):
        utils.recusionLog(11)
        if getattr(target, 'noSelected', None):
            if not getattr(target, 'syncUnits', None):
                return
            if target.syncUnits.values():
                for unit in target.syncUnits.values():
                    if unit:
                        virtureEid = unit[0]
                        target = BigWorld.entities.get(virtureEid, None)
                        if target and target.inWorld:
                            break

        if self.targetLocked is not None and self.targetLocked == target:
            return
        if self.isFightForLoveRunning() and target and target.IsAvatar and target != self and target.isFightForLoveCreator():
            return
        if hasattr(self, 'isBianShenZaiJuInPUBG') and self.isBianShenZaiJuInPUBG(target):
            return
        if self.targetLocked:
            self.lastTargetLocked = self.targetLocked
        if self.targetLocked is not None:
            if isinstance(self.targetLocked, VirtualMonster) and isinstance(target, VirtualMonster) and target.masterMonsterID == self.targetLocked.masterMonsterID:
                self.isChangeMasterMonsterPart = True
            self.unlockTarget()
            if self.targetLocked is not None:
                return
        if not hasattr(target, 'fashion') or target.fashion is None:
            return
        if getattr(target, 'forbidLock', False):
            return
        self.targetLocked = target
        self.cell.updateLocked(target.id)
        target.refreshRealModelState()
        if hasattr(target, 'refreshOpacityState') and not getattr(target, 'inHidingReveal', False):
            target.refreshOpacityState()
        self.ap.changeCursorState(self.targetLocked, lockAim, quickLock)
        self.ap.updateTargetLockedEffect()
        if target.showTargetUnitFrame():
            gameglobal.rds.ui.target.showTargetUnitFrame()
        else:
            gameglobal.rds.ui.target.updateTargetDir()
        if isinstance(target, VirtualMonster) or isinstance(target, Monster):
            gamelog.debug('@szh: the changed target is', target.id)
            target.lockEffect()
        self.isChangeMasterMonsterPart = False
        self.updateTargetLockedUfo()
        if isinstance(target, Avatar):
            gameglobal.rds.ui.target.setCombatVisible(target.inCombat)
        if isinstance(target, VirtualMonster) and hasattr(target, 'effect') and hasattr(target, 'masterMonsterID'):
            master = BigWorld.entities.get(target.masterMonsterID)
            if master:
                self._addMasterAllStateIcon(master)
        elif BigWorld.player().oldMasterStateSet:
            self.dealMasterStateIcon(target, set([]), BigWorld.player().oldMasterStateSet)
            BigWorld.player().oldMasterStateSet = set([])
        self._addTargetAllStateIcon(target)
        if self.targetLocked != None:
            gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_SKILL_TGT)
            if self.targetLocked.IsCombatUnit and self.targetLocked != self:
                self.targetLocked.addRanges()
        if fromUIProxy and gameglobal.gHideMode != gameglobal.HIDE_MODE0 and target.IsAvatar:
            target.hide(False)
        if self.targetLocked != None:
            teamIndex = gameglobal.rds.ui.group.getTeamIdByEntId(self.targetLocked.id)
            if teamIndex != None:
                gameglobal.rds.ui.group.setSelect(teamIndex)
            gameglobal.rds.ui.teamComm.setSelect(self.targetLocked.id, True)
        outlineHelper.setLockedTarget()
        if self.targetLocked != None:
            gameglobal.rds.ui.monsterBlood.setLockMonster(target.id)
        if gameglobal.rds.configData.get('enableHpMpOptimization', False):
            try:
                if self.lastTargetLocked and isinstance(self.lastTargetLocked, Avatar) and self.lastTargetLocked.inWorld:
                    self.lastTargetLocked.cell.unlockedByClient()
                if self.targetLocked and isinstance(self.targetLocked, Avatar):
                    self.targetLocked.cell.lockedByClient()
            except Exception as e:
                gamelog.error('lockTarget', e.message)

        if self.summonedSpriteInWorld:
            self.summonedSpriteInWorld.updateSpriteLockTarget()

    def updateTargetLockedUfo(self):
        target = self.targetLocked
        ufoType = ufo.UFO_NORMAL
        if self.isEnemy(target):
            ufoType = self.getTargetUfoType(target)
        elif getattr(target, 'isFlyMonster', False) or getattr(target, 'isJumping', False) or getattr(target, 'inFly', False) or getattr(target, 'inSwim', False):
            ufoType = ufoType + 1
        self.setTargetUfo(self.targetLocked, ufoType)

    def unlockTarget(self):
        gamelog.debug('unlockTarget')
        if self.targetLocked:
            utils.recusionLog(12)
            if self.getOperationMode() == gameglobal.ACTION_MODE:
                BigWorld.target.clear()
            self.cell.updateLocked(0)
            target = self.targetLocked
            if not target.inWorld:
                self.targetLocked = None
                return
            if isinstance(target, VirtualMonster) or isinstance(target, Monster):
                target.unlockEffect()
            if getattr(self, 'targetLocked', None):
                self.targetLocked = None
            if self.getOperationMode() == gameglobal.ACTION_MODE:
                self.ap.aimCross.turnToAimState()
                self.ap.lockAim = False
            self.setTargetUfo(target, ufo.UFO_SHADOW)
            gameglobal.rds.ui.target.hideTargetUnitFrame()
            teamIndex = gameglobal.rds.ui.group.getTeamIdByEntId(target.id)
            if teamIndex != None:
                gameglobal.rds.ui.group.unSelect()
            gameglobal.rds.ui.teamComm.setSelect(target.id, False)
            if hasattr(target, 'topLogo') and target.topLogo:
                if not self.isInBfDota() and hasattr(target, 'inCombat') and target.IsMonster:
                    target.topLogo.showMonsterBlood(target.inCombat)
            if self.isCombatUnit(target) and target != self:
                target.delRanges()
            gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_SKILL_TGT)
            if gameglobal.gHideMode != gameglobal.HIDE_MODE0 and (target.IsAvatar or target.IsSummonedSprite) or self.isShowClanWarExcludeSelf() and target.IsSummonedSprite:
                target.refreshOpacityState()
            outlineHelper.setLockedTarget()
            self.ap.cancelTargetLockedEffect()
            gameglobal.rds.ui.monsterBlood.setUnlockMonster()
            if gameglobal.rds.configData.get('enableHpMpOptimization', False):
                try:
                    if isinstance(target, Avatar):
                        target.cell.unlockedByClient()
                except Exception as e:
                    gamelog.error('unlockTarget', e.message)

    def refreshTargetLocked(self):
        target = self.targetLocked
        if target:
            ufoType = ufo.UFO_NORMAL
            if self.isEnemy(target):
                ufoType = self.getTargetUfoType(target)
            elif getattr(target, 'isFlyMonster', False) or getattr(target, 'isJumping', False) or getattr(target, 'inFly', False) or getattr(target, 'inSwim', False):
                ufoType = ufoType + 1
            self.setTargetUfo(self.targetLocked, ufoType)

    def loseGravity(self):
        if getattr(self, 'physics', None):
            self.setGravity(0.0)

    def restoreGravity(self):
        if gameglobal.rds.GameState == gametypes.GS_LOADING:
            return
        if self.life == gametypes.LIFE_DEAD:
            return
        if self.inSwim or self.inFly:
            return
        if getattr(self, 'physics', None):
            self.setGravity(gametypes.NOMAL_DOWNGRAVITY)
            self.ap.setJumpEnergy()

    def reload(self):
        if gameglobal.rds.isSinglePlayer:
            self.downKeyBindings = [([HK.HKM[keys.KEY_LEFTMOUSE]], self.useKey),
             ([HK.HKM[HK.KEY_ZOOMIN]], self.cameraCloseTo),
             ([HK.HKM[HK.KEY_ZOOMOUT]], self.cameraAwayFrom),
             ([HK.HKM[keys.KEY_ESCAPE]], self.escapeKey),
             ([HK.HKM[HK.KEY_DEBUG_VIEW]], self.showDebug),
             ([HK.HKM[keys.KEY_F1]], self.startFly),
             ([HK.HKM[keys.KEY_F2]], self.startDash),
             ([HK.HKM[keys.KEY_F3]], self.changeMount),
             ([HK.HKM[HK.KEY_DOWN]], self.startSlowDown),
             ([HK.HKM[HK.KEY_FUBEN_MONSTER]], self.showMonsterDebug),
             ([HK.HKM[HK.KEY_SINGLE_DEBUG]], self.showSingleDebug),
             ([HK.HKM[HK.KEY_SHOWUI]], self.showUI)]
        else:
            skillKeyBindings = self.createSkillKeyBinding()
            itemKeyBindings = self.createItemKeyBinding()
            qteSkillKeyBindings = [ ([HK.HKM[k]], Functor(self.useQteSkillByKey, i)) for i, k in enumerate(HK.SHORTCUT_QTE_SKILL_KEYS) ]
            otherKeyBindisng = self.createOtherKeyBindings()
            self.downKeyBindings = self.getDowKeyBindins(otherKeyBindisng, skillKeyBindings, itemKeyBindings, qteSkillKeyBindings)
            if gameglobal.rds.configData.get('enableNewItemSearch', False):
                self.downKeyBindings.append(([HK.HKM[HK.KEY_ITEM_SOURCE]], self.showItemSource))
            if gameglobal.rds.configData.get('enableSkillMacro', False) and gameglobal.rds.configData.get('enableOpenSkillMacroEntry', True):
                self.downKeyBindings.append(([HK.HKM[HK.KEY_SKILL_MACRO]], self.showSkillMacro))
            if gameglobal.rds.configData.get('enableCardSys', False) and gameglobal.rds.configData.get('enableOpenSkillMacroEntry', True):
                self.downKeyBindings.append(([HK.HKM[HK.KEY_CARD_SYSTEM]], self.showCardSystem))
        if BigWorld.isPublishedVersion():
            self.downKeyBindings.remove(([HK.HKM[HK.KEY_DEBUG_VIEW]], self.showDebug))
            self.downKeyBindings.remove(([HK.HKM[HK.KEY_HIDE_MONSTER_LOGO]], self.hideMonsterTopLogo))
        self.conflictKeyDict = {}
        if gameglobal.rds.configData.get('enableNewItemSearch', False):
            self.conflictKeyDict[HK.HKM[HK.KEY_ITEM_SOURCE]] = (self.showItemSource, self.dealItemSourceConflict)
        if gameglobal.rds.configData.get('enableSkillMacro', False):
            self.conflictKeyDict[HK.HKM[HK.KEY_SKILL_MACRO]] = (self.showSkillMacro, self.dealSkillMacroConflict)
        if gameglobal.rds.configData.get('enableCardSys', False):
            self.conflictKeyDict[HK.HKM[HK.KEY_CARD_SYSTEM]] = (self.showCardSystem, self.dealShowCardSystemConflict)
        if gameglobal.rds.configData.get('enableSummonedSprite', False) and not self.isInBfDota() and not self.isInPUBG():
            self.conflictKeyDict[HK.HKM[HK.KEY_SPRITE_TELEPORT_BACK]] = (self.spriteTeleportBack, self.removeHotKeyConflict)
            self.conflictKeyDict[HK.HKM[HK.KEY_SPRITE_MANUAL_SKILL]] = (self.spriteUseManualSkill, self.removeHotKeyConflict)
            self.conflictKeyDict[HK.HKM[HK.KEY_SPRITE_WAR]] = (self.showSpriteWar, self.removeHotKeyConflict)
        self.keyBindings = keys.buildBindList(self.downKeyBindings)
        if self.ap:
            self.ap.reload()

    def getDowKeyBindins(self, otherKeyBindisng, skillKeyBindings, itemKeyBindings, qteSkillKeyBindings):
        if formula.inDotaBattleField(getattr(self, 'mapID', 0)):
            return skillKeyBindings + itemKeyBindings + otherKeyBindisng + qteSkillKeyBindings
        else:
            return otherKeyBindisng + skillKeyBindings + itemKeyBindings + qteSkillKeyBindings

    def createOtherKeyBindings(self):
        unOpen = []
        if gameglobal.rds.configData.get('enableSummonedSprite', False):
            unOpen.append(([HK.HKM[HK.KEY_SPRITE_TELEPORT_BACK]], self.spriteTeleportBack))
            unOpen.append(([HK.HKM[HK.KEY_SPRITE_MANUAL_SKILL]], self.spriteUseManualSkill))
            unOpen.append(([HK.HKM[HK.KEY_SPRITE_WAR]], self.showSpriteWar))
        if gameglobal.rds.configData.get('enableCardSys', False):
            unOpen.append(([HK.HKM[HK.KEY_CARD_SYSTEM]], self.showCardSystem))
        return [([HK.HKM[keys.KEY_LEFTMOUSE]], self.useKey),
         ([HK.HKM[HK.KEY_ZOOMIN]], self.cameraCloseTo),
         ([HK.HKM[HK.KEY_ZOOMOUT]], self.cameraAwayFrom),
         ([HK.HKM[keys.KEY_ESCAPE]], self.escapeKey),
         ([HK.HKM[keys.KEY_TAB]], self.selectNearAttackable),
         ([HK.HKM[HK.KEY_BATTLE_APPLY]], self.showBattleApplyWin),
         ([HK.HKM[HK.KEY_SHOW_PVP]], self.showArenaPanel),
         ([HK.HKM[HK.KEY_PICK_ITEM]], self.pickNearByItems),
         ([HK.HKM[HK.KEY_SUMMARY]], self.showSummary),
         ([HK.HKM[HK.KEY_HIDE_MONSTER_LOGO]], self.hideMonsterTopLogo),
         ([HK.HKM[HK.KEY_SHOW_BAG]], self.showBag),
         ([HK.HKM[HK.KEY_SHOW_ROLEINFO]], self.showRoleInfo),
         ([HK.HKM[HK.KEY_RELATION]], self.showGuild),
         ([HK.HKM[HK.KEY_SHOW_TEAMINFO]], self.showTeamInfo),
         ([HK.HKM[HK.KEY_SHOW_TASKLOG]], self.showTaskLog),
         ([HK.HKM[HK.KEY_SHOW_MAP]], self.showMap),
         ([HK.HKM[HK.KEY_SHOW_SKILL]], self.showSkill),
         ([HK.HKM[HK.KEY_SHOW_RANK]], self.showRankList),
         ([HK.HKM[HK.KEY_HIDE_PLAYER_MONSTER]], self.hidePlayerAndMonster),
         ([HK.HKM[HK.KEY_SHOWUI]], self.showUI),
         ([HK.HKM[HK.KEY_SELECT_TEAMER]], self.selectTeamerByTab),
         ([HK.HKM[HK.KEY_SELECT_TEAMER1]], self.selectTeamer0),
         ([HK.HKM[HK.KEY_SELECT_TEAMER2]], self.selectTeamer1),
         ([HK.HKM[HK.KEY_SELECT_TEAMER3]], self.selectTeamer2),
         ([HK.HKM[HK.KEY_SELECT_TEAMER4]], self.selectTeamer3),
         ([HK.HKM[HK.KEY_SELECT_TEAMER_ME]], self.selectTeamerMe),
         ([HK.HKM[HK.KEY_SELECT_TEAMER_ME_SPRITE]], self.selectTeamerMeSprite),
         ([HK.HKM[keys.KEY_RETURN]], self.showChatLogWiew),
         ([HK.HKM[keys.KEY_Y]], self.showAchievementInfo),
         ([HK.HKM[HK.KEY_SHOW_MORE_RECOMM]], self.showMoreRecomm),
         ([HK.HKM[HK.KEY_DRAG_UI]], self.dragUI),
         ([HK.HKM[HK.KEY_SHOW_FRIEND]], self.showFriend),
         ([HK.HKM[HK.KEY_DEBUG_VIEW]], self.showDebug),
         ([HK.HKM[HK.KEY_MORPH_DEBUG]], self.showMorphDebug),
         ([HK.HKM[keys.KEY_NUMLOCK]], self.startAutoMove),
         ([HK.HKM[HK.KEY_SHOW_LIFE_SKILL]], self.showLifeSkill),
         ([HK.HKM[HK.KEY_SHOW_GENERAL_SKILL]], self.showGeneralSkill),
         ([HK.HKM[HK.KEY_SHOW_MAIL]], self.showMail),
         ([HK.HKM[HK.KEY_SHOW_CONSIGN]], self.showConsign),
         ([HK.HKM[HK.KEY_SHOWFPS]], self.showFps),
         ([HK.HKM[HK.KEY_WEAPON_IN_HAND]], self.weaponInHand),
         ([HK.HKM[HK.KEY_SHOW_CAMERA]], self.showCamera),
         ([HK.HKM[HK.KEY_LEAVE_ZAIJU]], self.onKeyLeaveRideAndZaiju),
         ([HK.HKM[HK.KEY_SHOW_HELP]], self.showHelp),
         ([HK.HKM[HK.KEY_SHOW_PLAYRECOMM]], self.showPlayerComm),
         ([HK.HKM[HK.KEY_ASSIGN_CONFIRM]], self.assignConfirm),
         ([HK.HKM[HK.KEY_ASSIGN_CANCEL]], self.assignGiveUp),
         ([HK.HKM[HK.KEY_ASSIGN_GREED]], self.assignGreed),
         ([HK.HKM[HK.KEY_SWITCH_RUN_WALK]], self.switchToRun),
         ([HK.HKM[HK.KEY_CAMERA_NEAR]], self.cameraCloseTo),
         ([HK.HKM[HK.KEY_CAMERA_FAR]], self.cameraAwayFrom),
         ([HK.HKM[HK.KEY_SHOW_DELEGATION]], self.showDelegation),
         ([HK.HKM[HK.KEY_BF_RETURN]], self.BFgoHomeClick),
         ([HK.HKM[HK.KEY_BF_COUNT]], self.BFopenStatsClick),
         ([HK.HKM[HK.KEY_SIMPLE_FIND_POS]], self.questSimpleFindPos),
         ([HK.HKM[HK.KEY_GROUP_FOLLOW]], self.quickGroupFollow),
         ([HK.HKM[HK.KEY_NEXT_TRACK_TAB]], self.gotoNextTrackTab),
         ([HK.HKM[HK.KEY_RIDE_WING]], self.toggleRideWing),
         ([HK.HKM[HK.KEY_TURN_CAMERA]], self.turnCamera),
         ([HK.HKM[HK.KEY_ROLE_CARD]], self.showRoleCard),
         ([HK.HKM[HK.KEY_FENG_WU_ZHI]], self.showFengWuZhi),
         ([HK.HKM[HK.KEY_PERSON_SPACE]], self.showPersonSpace),
         ([HK.HKM[HK.KEY_MOUNT_WING]], self.showMountWing),
         ([HK.HKM[HK.KEY_STALL]], self.showStall),
         ([HK.HKM[HK.KEY_PVP_ENHANCE]], self.showPvpEnhance),
         ([HK.HKM[HK.KEY_CHAT_ROOM]], self.showChatRoom),
         ([HK.HKM[HK.KEY_JIE_QI]], self.showJieQi),
         ([HK.HKM[HK.KEY_MENTOR]], self.showMentor),
         ([HK.HKM[HK.KEY_PVP_JJC]], self.showPvpJJC),
         ([HK.HKM[HK.KEY_GUI_BAO]], self.showGuibao),
         ([HK.HKM[HK.KEY_USER_BACK]], self.showUserBack),
         ([HK.HKM[HK.KEY_SUMMON_FRIEND]], self.showSummonFriend),
         ([HK.HKM[HK.KEY_CHATLOG_SOUND_RECORD]], self.startChatLogSoundRecord),
         ([HK.HKM[HK.KEY_CHAT_TO_FRIEND_SOUND_RECORD]], self.startChatToFriendSoundRecord),
         ([HK.HKM[HK.KEY_OPEN_WING_WORLD_UI]], self.openWingWorldUI),
         ([HK.HKM[HK.KEY_OPEN_ASSASSINATION_MAIN_UI]], self.openAssassinationMainUI),
         ([HK.HKM[HK.KEY_VOICE]], self.voiceCapture)] + unOpen

    def createSkillKeyBinding(self):
        if formula.inDotaBattleField(getattr(self, 'mapID', 0)):
            skillKeyBindings = [ ([HK.HKM[k]], Functor(self.useSkillByKeyInDota, i)) for i, k in enumerate(HK.SHORCUT_SKILL_KEYS_DOTA) ]
            skillKeyBindings.append(([HK.HKM[HK.KEY_DOTA_RETURN_HOME]], Functor(self.handleReturnHomeKey)))
            skillKeyBindings.append(([HK.HKM[HK.KEY_DOTA_OPEN_SHOP]], Functor(self.handleOpenDotaShop)))
            skillKeyBindings.append(([HK.HKM[HK.KEY_DOTA_SHOW_DETAIL]], Functor(self.handleShowDotaDetail)))
            skillKeyBindings.append(([HK.HKM[HK.KEY_DOTA_SHOW_PROP]], Functor(self.handleShowDotaProp)))
            skillKeyBindings.append(([HK.HKM[HK.KEY_DOTA_BUY_ITEM_SHORTCUT0]], Functor(self.hanldeShortCutBuy, 0)))
            skillKeyBindings.append(([HK.HKM[HK.KEY_DOTA_BUY_ITEM_SHORTCUT1]], Functor(self.hanldeShortCutBuy, 1)))
            if gameglobal.rds.configData.get('enableBfDotaMapMark', False):
                skillKeyBindings.append(([HK.HKM[HK.KEY_DOTA_MAP_MARK]], Functor(self.handleLittleMapMarkInDota, HK.KEY_DOTA_MAP_MARK)))
                skillKeyBindings.append(([HK.HKM[HK.KEY_DOTA_MAP_ATK]], Functor(self.handleLittleMapMarkInDota, HK.KEY_DOTA_MAP_ATK)))
                skillKeyBindings.append(([HK.HKM[HK.KEY_DOTA_MAP_RETREAT]], Functor(self.handleLittleMapMarkInDota, HK.KEY_DOTA_MAP_RETREAT)))
                skillKeyBindings.append(([HK.HKM[HK.KEY_DOTA_MAP_GATHER]], Functor(self.handleLittleMapMarkInDota, HK.KEY_DOTA_MAP_GATHER)))
        else:
            skillKeyBindings = [ ([HK.HKM[k]], Functor(self.useSkillByKey, i)) for i, k in enumerate(HK.SHORCUT_SKILL_KEYS) ]
        return skillKeyBindings

    def createItemKeyBinding(self):
        if formula.inDotaBattleField(getattr(self, 'mapID', 0)):
            itemKeyBindings = [ ([HK.HKM[k]], Functor(self.useItemByKeyInDota, i)) for i, k in enumerate(HK.SHORTCUT_ITEM_KEYS_DOTA) ]
        else:
            itemKeyBindings = [ ([HK.HKM[k]], Functor(self.useItemByKey, i)) for i, k in enumerate(HK.SHORTCUT_ITEM_KEYS) ]
        return itemKeyBindings

    def afterModelFinish(self):
        if self.life == gametypes.LIFE_DEAD:
            reliveHereEnable = not (self.touchAirWallProcess > 0 or self.downCliff > 0)
            spaceNo = formula.getMapId(self.spaceNo)
            reliveHereType = MCD.data.get(spaceNo, {}).get('reliveHereType', gametypes.RELIVE_HERE_TYPE_FORBID)
            if uiUtils.isInFubenShishenLow():
                reliveHereType = gametypes.RELIVE_HERE_TYPE_NORMAL
            reliveHereEnable = reliveHereEnable and reliveHereType != gametypes.RELIVE_HERE_TYPE_FORBID
            reliveNearEnable = not MCD.data.get(spaceNo, {}).get('forbidReliveNear', 0)
            gameglobal.rds.ui.deadAndRelive.show(reliveHereEnable, reliveNearEnable, False, None, reliveHereType)
        super(PlayerAvatar, self).afterModelFinish()
        self.enterWaterHeight = self.getEnterWaterHeight()
        self.leaveWaterHeight = 5.0 * self.getModelHeight() / 7.0
        self.physics.swimHeight = 1.0 * self.getModelHeight() / 7.0
        self._setMaxSlideAngleByMap()
        self.am.footTwistSpeed = SCD.data.get('footTwistSpeed', gameglobal.FOOTTWISTSPEED)
        if hasattr(self.filter, 'noSlideMaterial'):
            self.filter.noSlideMaterial = gameglobal.NOSLIDEMATTERKINDS
        if gameglobal.rds.GameState != gametypes.GS_LOADING:
            self._preloadAll()
        clientcom.setModelPhysics(self.modelServer.bodyModel)
        gameglobal.rds.ui.roleInfo.takePhoto3D(0)
        gameglobal.rds.ui.fittingRoom.showFitting()
        if self.targetLocked == self:
            gameglobal.rds.ui.target.showTargetUnitFrame()

    def _preloadAll(self):
        if self.preloaded:
            return
        self.preloadEffect(self.getAllSkillEffects())
        actionList = []
        actionList.extend(self.getAllSkillActions())
        actionList.extend(self.getAllQingGongActions())
        self.preloadAction(actionList)
        self.preloaded = True

    def _setMaxSlideAngleByMap(self):
        self.filter.maxSlideAngle = math.radians(MCD.data.get(self.mapID, {}).get('maxSlideAngle', math.degrees(0.9)))
        if MCD.data.get(self.mapID, {}).has_key('maxSlideAngle'):
            self.filter.applySlide = True
        else:
            self.filter.applySlide = self.inClanWar

    def afterPartsUpdateFinish(self):
        super(PlayerAvatar, self).afterPartsUpdateFinish()
        clientcom.setModelPhysics(self.modelServer.bodyModel)
        gameglobal.rds.ui.roleInfo.takePhoto3D(0)
        gameglobal.rds.ui.fittingRoom.showFitting()
        if self.targetLocked == self:
            gameglobal.rds.ui.target.showTargetUnitFrame()

    def afterWeaponUpdate(self, weapon):
        if weapon.followModelBias > 0:
            self.afterWearUpdate(weapon)
            return
        super(PlayerAvatar, self).afterWeaponUpdate(weapon)
        if weapon.isHangUped() or weapon.isDetached():
            gameglobal.rds.ui.roleInfo.takeWeaponPhoto(weapon)
            gameglobal.rds.ui.fittingRoom.showFitting()

    def afterWearUpdate(self, wear):
        super(PlayerAvatar, self).afterWearUpdate(wear)
        gameglobal.rds.ui.roleInfo.takeWearPhoto(wear)
        gameglobal.rds.ui.fittingRoom.showFitting()

    def preloadEffect(self, fxs):
        for fxId in fxs:
            sfx.gEffectMgr.preloadFx(fxId, self.getEffectLv(), charRes.transBodyType(self.realPhysique.sex, self.realPhysique.bodyType))

    def preloadAction(self, actionList):
        model = self.modelServer.bodyModel
        if model and hasattr(model, 'resideActions'):
            model.resideActions(*actionList)

    def needCefFilterKey(self):
        if gameglobal.rds.ui.miniGame.widget or gameglobal.rds.ui.cefTest.widget or gameglobal.rds.ui.bfDotaHeros.widget:
            return True
        return False

    def handleKeyEvent--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'relogNotifyState'
6	POP_JUMP_IF_FALSE '13'

9	LOAD_CONST        None
12	RETURN_END_IF     None

13	LOAD_GLOBAL       'gameglobal'
16	LOAD_ATTR         'isModalDlgShow'
19	POP_JUMP_IF_FALSE '63'
22	LOAD_FAST         'key'
25	LOAD_GLOBAL       'keys'
28	LOAD_ATTR         'KEY_MOUSE0'
31	LOAD_GLOBAL       'keys'
34	LOAD_ATTR         'KEY_MOUSE1'
37	BUILD_TUPLE_2     None
40	COMPARE_OP        'not in'
43_0	COME_FROM         '19'
43	POP_JUMP_IF_FALSE '63'

46	LOAD_FAST         'self'
49	LOAD_ATTR         'chatToEventEx'
52	LOAD_CONST        '\xbc\xfc\xc5\xcc\xd7\xb4\xcc\xac\xb1\xbb\xcb\xf8\xb6\xa8'
55	CALL_FUNCTION_1   None
58	POP_TOP           None

59	LOAD_CONST        None
62	RETURN_END_IF     None

63	LOAD_GLOBAL       'gameglobal'
66	LOAD_ATTR         'rds'
69	LOAD_ATTR         'ui'
72	LOAD_ATTR         'bInput'
75	POP_JUMP_IF_FALSE '91'

78	LOAD_FAST         'isDown'
81	POP_JUMP_IF_FALSE '91'

84	LOAD_CONST        None
87	RETURN_END_IF     None
88	JUMP_FORWARD      '91'
91_0	COME_FROM         '88'

91	LOAD_FAST         'self'
94	LOAD_ATTR         'needCefFilterKey'
97	CALL_FUNCTION_0   None
100	POP_JUMP_IF_FALSE '134'

103	LOAD_FAST         'key'
106	LOAD_GLOBAL       'keys'
109	LOAD_ATTR         'KEY_ESCAPE'
112	LOAD_GLOBAL       'keys'
115	LOAD_ATTR         'KEY_LALT'
118	BUILD_TUPLE_2     None
121	COMPARE_OP        'not in'
124	POP_JUMP_IF_FALSE '134'

127	LOAD_CONST        None
130	RETURN_END_IF     None
131	JUMP_FORWARD      '134'
134_0	COME_FROM         '131'

134	LOAD_FAST         'self'
137	LOAD_ATTR         'lockHotKey'
140	UNARY_NOT         None
141	POP_JUMP_IF_TRUE  '432'
144	LOAD_FAST         'self'
147	LOAD_ATTR         'lockHotKey'
150	POP_JUMP_IF_FALSE '245'
153	LOAD_FAST         'key'
156	LOAD_GLOBAL       'keys'
159	LOAD_ATTR         'KEY_ESCAPE'
162	LOAD_GLOBAL       'keys'
165	LOAD_ATTR         'KEY_RETURN'
168	LOAD_GLOBAL       'HK'
171	LOAD_ATTR         'HKM'
174	LOAD_GLOBAL       'HK'
177	LOAD_ATTR         'KEY_ITEM_SOURCE'
180	BINARY_SUBSCR     None
181	LOAD_ATTR         'key'
184	BUILD_TUPLE_3     None
187	COMPARE_OP        'in'
190	POP_JUMP_IF_TRUE  '432'
193	LOAD_FAST         'key'
196	LOAD_GLOBAL       'keys'
199	LOAD_ATTR         'KEY_MOUSE0'
202	LOAD_GLOBAL       'keys'
205	LOAD_ATTR         'KEY_MOUSE1'
208	BUILD_TUPLE_2     None
211	COMPARE_OP        'in'
214	POP_JUMP_IF_FALSE '224'
217	LOAD_FAST         'isDown'
220	UNARY_NOT         None
221_0	COME_FROM         '214'
221	POP_JUMP_IF_TRUE  '432'
224	LOAD_FAST         'self'
227	LOAD_ATTR         'isInUnlockableHotKey'
230	LOAD_FAST         'key'
233	LOAD_FAST         'mods'
236	CALL_FUNCTION_2   None
239_0	COME_FROM         '141'
239_1	COME_FROM         '190'
239_2	COME_FROM         '221'
239	POP_JUMP_IF_FALSE '245'

242	JUMP_FORWARD      '432'

245	LOAD_FAST         'self'
248	LOAD_ATTR         'lockMouseKey'
251	POP_JUMP_IF_TRUE  '394'

254	LOAD_FAST         'key'
257	LOAD_GLOBAL       'keys'
260	LOAD_ATTR         'KEY_MOUSE0'
263	LOAD_GLOBAL       'keys'
266	LOAD_ATTR         'KEY_MOUSE1'
269	BUILD_TUPLE_2     None
272	COMPARE_OP        'in'
275	POP_JUMP_IF_FALSE '390'

278	LOAD_FAST         'key'
281	LOAD_GLOBAL       'keys'
284	LOAD_ATTR         'KEY_MOUSE0'
287	COMPARE_OP        '=='
290	POP_JUMP_IF_FALSE '299'
293	LOAD_CONST        '_msleft'
296	JUMP_FORWARD      '302'
299	LOAD_CONST        '_msright'
302_0	COME_FROM         '296'
302	STORE_FAST        'desc'

305	LOAD_GLOBAL       'hasattr'
308	LOAD_FAST         'self'
311	LOAD_ATTR         'ap'
314	LOAD_FAST         'desc'
317	CALL_FUNCTION_2   None
320	POP_JUMP_IF_FALSE '390'
323	LOAD_FAST         'self'
326	LOAD_ATTR         'isLockYaw'
329	UNARY_NOT         None
330_0	COME_FROM         '320'
330	POP_JUMP_IF_FALSE '390'

333	LOAD_GLOBAL       'setattr'
336	LOAD_FAST         'self'
339	LOAD_ATTR         'ap'
342	LOAD_FAST         'desc'
345	LOAD_GLOBAL       'True'
348	CALL_FUNCTION_3   None
351	POP_TOP           None

352	LOAD_FAST         'self'
355	LOAD_ATTR         'ap'
358	LOAD_ATTR         'moveControl'
361	LOAD_FAST         'desc'
364	LOAD_FAST         'isDown'
367	CALL_FUNCTION_2   None
370	POP_TOP           None

371	LOAD_FAST         'self'
374	LOAD_ATTR         'ap'
377	LOAD_ATTR         'checkShowCursor'
380	CALL_FUNCTION_0   None
383	POP_TOP           None
384	JUMP_ABSOLUTE     '390'
387	JUMP_FORWARD      '390'
390_0	COME_FROM         '387'

390	LOAD_CONST        None
393	RETURN_END_IF     None

394	LOAD_FAST         'self'
397	LOAD_ATTR         'inSlowTime'
400	POP_JUMP_IF_FALSE '428'

403	LOAD_FAST         'self'
406	LOAD_ATTR         'ap'
409	LOAD_ATTR         'handleKeyEvent'
412	LOAD_FAST         'isDown'
415	LOAD_FAST         'key'
418	LOAD_FAST         'mods'
421	CALL_FUNCTION_3   None
424	POP_TOP           None
425	JUMP_FORWARD      '428'
428_0	COME_FROM         '425'

428	LOAD_CONST        None
431	RETURN_VALUE      None
432_0	COME_FROM         '242'

432	LOAD_FAST         'self'
435	LOAD_ATTR         'isInCbgRoleSelling'
438	POP_JUMP_IF_FALSE '445'

441	LOAD_CONST        None
444	RETURN_END_IF     None

445	LOAD_GLOBAL       'gameglobal'
448	LOAD_ATTR         'rds'
451	LOAD_ATTR         'ui'
454	LOAD_ATTR         'fishing'
457	LOAD_ATTR         'FishMediator'
460	POP_JUMP_IF_FALSE '494'
463	LOAD_FAST         'key'
466	LOAD_GLOBAL       'keys'
469	LOAD_ATTR         'KEY_F'
472	COMPARE_OP        '=='
475	POP_JUMP_IF_FALSE '494'
478	LOAD_FAST         'mods'
481	LOAD_CONST        0
484	COMPARE_OP        '=='
487_0	COME_FROM         '460'
487_1	COME_FROM         '475'
487	POP_JUMP_IF_FALSE '494'

490	LOAD_CONST        None
493	RETURN_END_IF     None

494	LOAD_GLOBAL       'gameglobal'
497	LOAD_ATTR         'rds'
500	LOAD_ATTR         'ui'
503	LOAD_ATTR         'fishing'
506	LOAD_ATTR         'isCharging'
509	CALL_FUNCTION_0   None
512	POP_JUMP_IF_FALSE '561'
515	LOAD_FAST         'key'
518	LOAD_GLOBAL       'keys'
521	LOAD_ATTR         'KEY_A'
524	COMPARE_OP        '=='
527	POP_JUMP_IF_TRUE  '545'
530	LOAD_FAST         'key'
533	LOAD_GLOBAL       'keys'
536	LOAD_ATTR         'KEY_D'
539	COMPARE_OP        '=='
542_0	COME_FROM         '527'
542	POP_JUMP_IF_FALSE '561'
545	LOAD_FAST         'mods'
548	LOAD_CONST        0
551	COMPARE_OP        '=='
554_0	COME_FROM         '512'
554_1	COME_FROM         '542'
554	POP_JUMP_IF_FALSE '561'

557	LOAD_CONST        None
560	RETURN_END_IF     None

561	LOAD_FAST         'key'
564	LOAD_GLOBAL       'keys'
567	LOAD_ATTR         'KEY_MOUSE2'
570	COMPARE_OP        '=='
573	POP_JUMP_IF_FALSE '588'

576	LOAD_GLOBAL       'True'
579	LOAD_FAST         'self'
582	STORE_ATTR        'mouseMidKeydown'
585	JUMP_FORWARD      '588'
588_0	COME_FROM         '585'

588	LOAD_FAST         'key'
591	LOAD_GLOBAL       'keys'
594	LOAD_ATTR         'KEY_MOUSE0'
597	LOAD_GLOBAL       'keys'
600	LOAD_ATTR         'KEY_MOUSE1'
603	BUILD_TUPLE_2     None
606	COMPARE_OP        'in'
609	POP_JUMP_IF_FALSE '636'

612	LOAD_GLOBAL       'HK'
615	LOAD_ATTR         'keyDef'
618	LOAD_FAST         'key'
621	LOAD_CONST        1
624	LOAD_CONST        0
627	CALL_FUNCTION_3   None
630	STORE_FAST        'rdfkey'
633	JUMP_FORWARD      '657'

636	LOAD_GLOBAL       'HK'
639	LOAD_ATTR         'keyDef'
642	LOAD_FAST         'key'
645	LOAD_CONST        1
648	LOAD_FAST         'mods'
651	CALL_FUNCTION_3   None
654	STORE_FAST        'rdfkey'
657_0	COME_FROM         '633'

657	LOAD_FAST         'key'
660	LOAD_GLOBAL       'keys'
663	LOAD_ATTR         'KEY_LALT'
666	COMPARE_OP        '=='
669	POP_JUMP_IF_FALSE '710'

672	LOAD_FAST         'isDown'
675	POP_JUMP_IF_FALSE '694'

678	LOAD_FAST         'self'
681	LOAD_ATTR         'showTopLogo'
684	LOAD_GLOBAL       'False'
687	CALL_FUNCTION_1   None
690	POP_TOP           None
691	JUMP_ABSOLUTE     '710'

694	LOAD_FAST         'self'
697	LOAD_ATTR         'showTopLogo'
700	LOAD_GLOBAL       'True'
703	CALL_FUNCTION_1   None
706	POP_TOP           None
707	JUMP_FORWARD      '710'
710_0	COME_FROM         '707'

710	LOAD_FAST         'self'
713	LOAD_ATTR         'isInBfDota'
716	CALL_FUNCTION_0   None
719	POP_JUMP_IF_FALSE '799'
722	LOAD_GLOBAL       'gameglobal'
725	LOAD_ATTR         'rds'
728	LOAD_ATTR         'ui'
731	LOAD_ATTR         'zaijuV2'
734	LOAD_ATTR         'isLearnSkillkeyDown'
737	POP_JUMP_IF_FALSE '799'
740	LOAD_FAST         'mods'
743	LOAD_CONST        2
746	COMPARE_OP        '=='
749_0	COME_FROM         '719'
749_1	COME_FROM         '737'
749	POP_JUMP_IF_FALSE '799'

752	LOAD_CONST        0
755	STORE_FAST        'mods'

758	LOAD_FAST         'rdfkey'
761	LOAD_ATTR         'setPart'
764	LOAD_CONST        1
767	LOAD_FAST         'key'
770	LOAD_FAST         'mods'
773	CALL_FUNCTION_3   None
776	POP_TOP           None

777	LOAD_FAST         'self'
780	LOAD_ATTR         'processKeyEvent'
783	LOAD_FAST         'rdfkey'
786	LOAD_GLOBAL       'True'
789	LOAD_FAST         'mods'
792	CALL_FUNCTION_3   None
795	POP_TOP           None
796	JUMP_FORWARD      '906'

799	LOAD_FAST         'self'
802	LOAD_ATTR         'processKeyEvent'
805	LOAD_FAST         'rdfkey'
808	LOAD_GLOBAL       'False'
811	LOAD_FAST         'mods'
814	CALL_FUNCTION_3   None
817	POP_JUMP_IF_TRUE  '906'

820	LOAD_FAST         'mods'
823	LOAD_GLOBAL       'HK'
826	LOAD_ATTR         'getCastSelfKeyMod'
829	CALL_FUNCTION_0   None
832	COMPARE_OP        '=='
835	POP_JUMP_IF_FALSE '906'
838	LOAD_FAST         'self'
841	LOAD_ATTR         'keyInSkill'
844	LOAD_FAST         'key'
847	LOAD_CONST        0
850	CALL_FUNCTION_2   None
853_0	COME_FROM         '835'
853	POP_JUMP_IF_FALSE '906'

856	LOAD_CONST        0
859	STORE_FAST        'mods'

862	LOAD_FAST         'rdfkey'
865	LOAD_ATTR         'setPart'
868	LOAD_CONST        1
871	LOAD_FAST         'key'
874	LOAD_FAST         'mods'
877	CALL_FUNCTION_3   None
880	POP_TOP           None

881	LOAD_FAST         'self'
884	LOAD_ATTR         'processKeyEvent'
887	LOAD_FAST         'rdfkey'
890	LOAD_GLOBAL       'True'
893	LOAD_FAST         'mods'
896	CALL_FUNCTION_3   None
899	POP_TOP           None
900	JUMP_ABSOLUTE     '906'
903	JUMP_FORWARD      '906'
906_0	COME_FROM         '796'
906_1	COME_FROM         '903'

906	LOAD_FAST         'self'
909	LOAD_ATTR         'ap'
912	POP_JUMP_IF_FALSE '940'

915	LOAD_FAST         'self'
918	LOAD_ATTR         'ap'
921	LOAD_ATTR         'handleKeyEvent'
924	LOAD_FAST         'isDown'
927	LOAD_FAST         'key'
930	LOAD_FAST         'mods'
933	CALL_FUNCTION_3   None
936	POP_TOP           None
937	JUMP_FORWARD      '940'
940_0	COME_FROM         '937'

Syntax error at or near `JUMP_FORWARD' token at offset 937

    def processKeyEvent(self, rdfkey, inskill, mods = None):
        if not getattr(self, 'keyBindings', None):
            return
        for downKeys, upKeySets, action in self.keyBindings:
            if rdfkey in downKeys:
                okayToGo = 1
                for downKey in downKeys:
                    if okayToGo:
                        okayToGo = downKey.isAnyDown()
                        if inskill:
                            okayToGo = BigWorld.getKeyDownState(rdfkey.key, HK.getCastSelfKeyMod())
                    else:
                        break

                if okayToGo:
                    for upKeys in upKeySets:
                        allDown = 1
                        for upKey in upKeys:
                            if allDown:
                                allDown = upKey.isAnyDown()
                            else:
                                break

                        if upKeys:
                            okayToGo = okayToGo and not allDown

                for conflictKey, actions in self.conflictKeyDict.iteritems():
                    if actions[0] != action:
                        if conflictKey.inkeyDef(rdfkey.key, rdfkey.mods) or conflictKey.inkeyDef(rdfkey.key2, rdfkey.mods2):
                            conflictAction = actions[1]
                            arginfo = inspect.getargspec(conflictAction)
                            if len(arginfo.args) > 1:
                                conflictAction(conflictKey, rdfkey)
                            else:
                                conflictAction()

                self.keyEventMods = mods
                action(okayToGo)
                self.keyEventMods = None
                return True

        return False

    def updateQuestSign(self):
        gamelog.debug('JJH Avatar: updateQuestSign')
        if not self._updateQuestNextFrame:
            self._updateQuestNextFrame = True
            BigWorld.callback(0.001, self._realUpdateQuest)
        else:
            return

    def _realUpdateQuest(self):
        pass

    def onGeometryMapped(self, path):
        gamelog.debug('jorsef: Avatar.onGeometryMapped ', path)
        if isinstance(BigWorld.player(), PlayerAvatar):
            navigator.getNav().stopPathFinding()
        loadingProgress.gLastSpace = path
        gamelog.debug('jorsef: Avatar.onGeometryMapped ', loadingProgress.gLastSpace)
        self.refreshSpaceEntities()

    def onNewSpace(self, path):
        self.isInPhase = False
        if self.checkPhaseAreaCallback:
            BigWorld.cancelCallback(self.checkPhaseAreaCallback)
            self.checkPhaseAreaCallback = None
        gamelog.debug('jorsef: Avatar.onNewSpace ', path, loadingProgress.gLastSpace)
        if isinstance(BigWorld.player(), PlayerAvatar):
            navigator.getNav().stopPathFinding()
        if gameglobal.rds.GameState != gametypes.GS_LOADING:
            mapName = C_ui.get_map_name()[0]
            loadingProgress.instance().show(True, loadingProgress.gLastSpace.split('/')[2])
            BigWorld.callback(0, Functor(loadingProgress.instance().startProgress, self._onLoaded))
            BigWorld.callback(2, Functor(loadingProgress.instance().fadeTo, mapName))
            gameglobal.rds.cam.cc.firstPerson = 1
        loadingProgress.gLastSpace = path

    def onTeleport(self, spaceID, pos):
        if not self:
            return
        if spaceID == self.spaceID:
            self.lastSpaceNo = self.spaceNo
        self.lastTeleportPos = Math.Vector3(pos)
        self.lastTeleportTime = utils.getNow()
        if self.checkPhaseAreaCallback:
            BigWorld.cancelCallback(self.checkPhaseAreaCallback)
            self.checkPhaseAreaCallback = None
        gamelog.debug('jorsef: Avatar.onTeleport ', spaceID, self.spaceID, self.lastSpaceNo, self.spaceNo, pos, loadingProgress.gLastSpace)
        try:
            if gameglobal.rds.ui.map.isShow:
                gameglobal.rds.ui.map.openMap(False)
        except:
            pass

        if isinstance(BigWorld.player(), PlayerAvatar):
            if navigator.getNav().canSetDelay():
                gamelog.debug('jorsef: navigator: setDelayPathFinding')
                navigator.getNav().setDelayPathFinding(1.0, None, None)
            else:
                gamelog.debug('jorsef: navigator: stopPathFinding')
                navigator.getNav().stopPathFinding()
            if self.runOnWater:
                self.cell.leaveRunOnWater()
            if gameglobal.rds.configData.get('enableWingWorld', False):
                self.checkWingWorldContinuePathFinding()
        teleportDis = (pos - self.position).length
        if gameglobal.rds.GameState != gametypes.GS_LOADING:
            mapName = C_ui.get_map_name()[0]
            if self.spaceNo == 1:
                mapName = uiUtils.getChunkName(pos[0], pos[2])
            gamelog.debug('jorsef: Avatar.onTeleport loading ', mapName, teleportDis)
            if self.spaceID != spaceID and not self._isSwitchLine(self.spaceNo, self.lastSpaceNo) and navigator.getPhaseMappingNum(self.spaceNo) == navigator.getPhaseMappingNum(self.lastSpaceNo):
                if teleportDis < const.MIN_DIST_FOR_LOADINGPROGRESS:
                    if FD.data.get(formula.getFubenNo(self.spaceNo), {}).get('isPhaseFb', False) or FD.data.get(formula.getFubenNo(self.lastSpaceNo), {}).get('isPhaseFb', False) or MDD.data.get(formula.getMLGNo(self.spaceNo), {}).get('isPhaseML', False) or MDD.data.get(formula.getMLGNo(self.lastSpaceNo), {}).get('isPhaseML', False):
                        screenRipple.rippleScreen()
                        self.scenarioPlayAfterTeleport()
                    elif formula.spaceInHomeFloor(self.spaceNo):
                        loadingProgress.instance().show(True, mapName)
                        gamelog.debug('jorsef: Avatar.onTeleport loading 0')
                        BigWorld.callback(0, Functor(loadingProgress.instance().startProgress, self._onLoaded))
                        BigWorld.callback(1.0, Functor(loadingProgress.instance().fadeTo2, self.spaceNo))
                        gameglobal.rds.cam.cc.firstPerson = 1
                    loadingProgress.instance().onServerLoaded(False)
                else:
                    loadingProgress.instance().show(True, mapName)
                    gamelog.debug('jorsef: Avatar.onTeleport loading 1')
                    BigWorld.callback(0, Functor(loadingProgress.instance().startProgress, self._onLoaded))
                    BigWorld.callback(1.0, Functor(loadingProgress.instance().fadeTo2, self.spaceNo))
                    gameglobal.rds.cam.cc.firstPerson = 1
            elif self.spaceID != spaceID or self.spaceID == spaceID and teleportDis > const.MIN_DIST_FOR_LOADINGPROGRESS and not self.isInBfDota():
                loadingProgress.instance().show(True, mapName)
                gamelog.debug('jorsef: Avatar.onTeleport loading 2')
                BigWorld.callback(0, Functor(loadingProgress.instance().startProgress, self._onLoaded))
                BigWorld.callback(1.0, Functor(loadingProgress.instance().fadeTo2, self.spaceNo))
                gameglobal.rds.cam.cc.firstPerson = 1
            elif not isSamePosition(self.position, pos):
                if getattr(self, 'scenarioAfterTeleport', None):
                    screenRipple.rippleScreen()
                loadingProgress.instance().onServerLoaded(False)
                self.scenarioPlayAfterTeleport()
            else:
                loadingProgress.instance().onServerLoaded(False)
            if self.fashion != None:
                if self.life != gametypes.LIFE_DEAD:
                    self.fashion.breakJump()
                    self.fashion.breakFall()
                    self.fashion.stopAllActions()
            self.isAscending = False
            if self.ap != None:
                self.ap.stopMove()
        clientcom.resetModelPhysics(self.modelServer.bodyModel)
        self.faceToDirWidthCamera(self.yaw)
        self.clearDropForBlood()
        if gameglobal.HIDE_ALL_MODELS:
            self.fashion.hide(True)

    def getTeleportCost(self, destId):
        if self.crossServerGoal == gametypes.SOUL_OUT_GOAL_CROSS_CLAN_WAR:
            return 0
        cash = 0
        refData = TRD.data.get(destId, {})
        td = TDD.data.get(destId, None)
        if self.school in refData.get('cashFreeSchools', ()):
            return 0
        if refData.has_key('cash') and td:
            fvars = {'distance': distance3D(self.position, td['pos']),
             'lv': self.lv}
            cash = eval(refData['cash'], fvars)
            if self.tride.inRide():
                for k, v in self.tride.iteritems():
                    if k == self.id:
                        continue
                    member = BigWorld.entities.get(k)
                    if member:
                        fvars = {'distance': distance3D(member.position, td['pos']),
                         'lv': member.lv}
                        cash += eval(refData['cash'], fvars)

        return cash

    def _isSwitchLine(self, srcSpaceNo, dstSpaceNo):
        if srcSpaceNo == dstSpaceNo:
            return False
        if formula.spaceInMultiLine(srcSpaceNo) and formula.spaceInMultiLine(dstSpaceNo) and formula.getMLGNo(srcSpaceNo) == formula.getMLGNo(dstSpaceNo) and formula.getMLFloorNo(srcSpaceNo) == formula.getMLFloorNo(dstSpaceNo):
            return True
        return False

    def releaseSpaceEntities(self):
        if not self.spaceClientEntities:
            return
        for entDict in self.spaceClientEntities.values():
            if entDict:
                for entId in entDict.values():
                    if entId:
                        BigWorld.destroyEntity(entId)

                entDict.clear()

        self.spaceClientEntities.clear()

    def createClientEntities(self):
        keyNo = None
        if self.inFuben():
            keyNo = formula.getFubenNo(self.spaceNo)
        elif self.inMLSpace():
            keyNo = formula.getMLNo(self.spaceNo)
        if not keyNo:
            return
        clientEntityIds = SPCCED.data.get(keyNo, {}).get('clientEntityIds', [])
        if not clientEntityIds:
            return
        clientEntityIds = clientEntityIds[:5]
        for tid in clientEntityIds:
            eData = CLIED.data.get(tid, {})
            if eData:
                spaceID = self.spaceID
                modelName = eData.get('model', 0)
                scale = eData.get('scale', 1)
                noDrop = eData.get('noDrop', False)
                keepEffs = eData.get('keepEffs', [])
                effTime = eData.get('effTime', 0)
                attrs = {'modelName': modelName,
                 'scale': scale,
                 'noDrop': noDrop,
                 'keepEffs': keepEffs,
                 'effTime': effTime}
                position = eData.get('pos', (0, 0, 0))
                direction = eData.get('dir', (0, 0, 0))
                clientShip = BigWorld.createEntity('ClientShip', spaceID, 0, position, direction, {'attrs': attrs})
                self.addClientEntity(keyNo, tid, clientShip)

    def addClientEntity(self, mlgNo, tid, ent):
        if not self.spaceClientEntities.get(mlgNo, {}):
            self.spaceClientEntities[mlgNo] = {tid: ent}
        else:
            entDict = self.spaceClientEntities.get(mlgNo, {})
            entDict[tid] = ent

    def refreshSpaceEntities(self):
        self.releaseSpaceEntities()
        self.createClientEntities()

    def handleMLGNo(self, mlgNo, oldMlgNo):
        isSame = bool(mlgNo == oldMlgNo)
        if mlgNo in const.ML_SPACE_NO_SXY:
            gameglobal.rds.ui.suiXingYu.intoMultoLine()
        elif mlgNo == const.ML_SPACE_NO_DAFUWENG:
            isSame or gameglobal.rds.ui.questTrack.hideTrackPanel(True)
        elif mlgNo == const.ML_GROUP_NO_LUEYINGGU:
            if gameglobal.rds.configData.get('enableGuildYMF', False):
                gameglobal.rds.ui.ymfScoreV2.show()
            else:
                gameglobal.rds.ui.yumufengScore.show()
        elif mlgNo in WWCD.data.get('wingWorldDGList', ()):
            isSame or self.cell.queryWingWorldBossStats()
            isSame or gameglobal.rds.ui.wingWorldPreTaskTip.show(0, 0)
        if oldMlgNo in const.ML_SPACE_NO_SXY:
            isSame or gameglobal.rds.ui.suiXingYu.leaveMultoLine()
        elif oldMlgNo == const.ML_SPACE_NO_DAFUWENG:
            isInBigWorld = bool(self.mapID == const.SPACE_NO_BIG_WORLD)
            isInBigWorld and gameglobal.rds.ui.questTrack.hideTrackPanel(False)
        elif oldMlgNo == const.ML_GROUP_NO_LUEYINGGU:
            isSame or gameglobal.rds.ui.yumufengScore.hide()
            isSame or gameglobal.rds.ui.ymfScoreV2.hide()
        elif oldMlgNo in WWCD.data.get('wingWorldDGList', ()):
            isSame or gameglobal.rds.ui.wingWorldPreTaskTip.hide()

    def set_spaceNo(self, old):
        gamelog.debug('jorsef: loading set_spaceNo', old, self.spaceNo)
        if gameglobal.rds.configData.get('enableMaterialLoadStatistics', False):
            gameglobal.rds.uiLog.addMapCntLog(self.mapID)
        self.membersGuideCnt = {}
        if hasattr(BigWorld, 'setPlayerMapID'):
            BigWorld.setPlayerMapID(self.mapID)
        BigWorld.callback(1.0, Functor(loadingProgress.instance().fadeTo2, self.spaceNo))
        if formula.spaceInGuild(BigWorld.player().spaceNo):
            BigWorld.callback(10, loadingProgress.instance().beginGuildLoadCheck)
        BigWorld.darkWorld(False, (0, 0, 0, 0))
        self.lastSpaceNo = old
        oldMapId = formula.getMapId(old)
        newMapId = formula.getMapId(self.spaceNo)
        oldFbNo = formula.getFubenNo(old)
        if formula.inDotaBattleField(oldMapId) and not formula.inDotaBattleField(newMapId):
            self.onLeaveDotaBf()
        if not formula.inDotaBattleField(oldMapId) and formula.inDotaBattleField(newMapId):
            self.onEnterDotaBf()
        if not formula.spaceInWingWarCity(old) and formula.spaceInWingWarCity(self.spaceNo):
            self.onEnterWingWarCity()
        if formula.spaceInWingWarCity(old) and not formula.spaceInWingWarCity(self.spaceNo):
            self.onLeaveWingWarCity()
        if not formula.spaceInWingPeaceCity(old) and formula.spaceInWingPeaceCity(self.spaceNo):
            self.onEnterWingPeaceCity()
        if formula.spaceInWingPeaceCity(old) and not formula.spaceInWingPeaceCity(self.spaceNo):
            self.onLeaveWingPeaceCity()
        if not self.inWingPeaceCityOrBornIsland():
            gameglobal.rds.ui.wingWorldYaBiao.delPushIcon()
        if oldFbNo in FD.data:
            self.onLeaveFuben(oldFbNo)
        elif oldFbNo in BFD.data:
            self.onLeaveBattleField(oldFbNo)
            if formula.whatFubenType(oldFbNo) == const.FB_TYPE_BATTLE_FIELD_NEW_FLAG:
                self.resetTopLogo()
        elif oldFbNo in SSCD.data:
            if oldFbNo == const.FB_NO_SHENG_SI_CHANG:
                self.onLeaveShengSiChang()
            elif oldFbNo == const.FB_NO_TEAM_SHENG_SI_CHANG:
                self.onLeaveTeamShengSiChang()
        elif oldFbNo in AD.data:
            self.onLeaveArena()
        elif oldFbNo in const.FB_NO_MARRIAGE_HALL_SET:
            gameglobal.rds.ui.chat.goToWorld()
        elif formula.spaceInMultiLine(old) or formula.spaceInMultiLine(self.spaceNo):
            gameglobal.rds.ui.player.setLv(self.lv)
            mlgNo = formula.getMLGNo(self.spaceNo)
            oldMlgNo = formula.getMLGNo(old)
            self.handleMLGNo(mlgNo, oldMlgNo)
        if formula.inWorld(old) and formula.spaceInMultiLine(self.spaceNo):
            if getattr(self, 'groupNUID', None):
                self.cell.cancelGroupFollow()
        if oldFbNo != 0 and gameglobal.rds.ui.dying.isOpen == True:
            gameglobal.rds.ui.dying.close()
        oldFbMode = formula.whatFubenMode(oldFbNo)
        if oldFbMode == const.FB_MODE_SPEED:
            self.fubenClockCommand(const.CLOCK_CLOSE, ())
        fbNo = formula.getFubenNo(self.spaceNo)
        if oldFbNo in const.FB_NO_MARRIAGE_HALL_SET:
            gameglobal.rds.sound.stopMusic(const.MARRIAGE_CHINESE_HALL_MUSIC_ID)
        if oldFbNo in const.FB_NO_MARRIAGE_ROOM_SET:
            self.leaveMarriageRoom()
            gameglobal.rds.sound.stopMusic(const.MARRIAGE_ROOM_MUSIC_ID)
        if fbNo in const.FB_NO_MARRIAGE_ROOM_SET:
            self.enterMarriageRoom()
        fbMode = formula.whatFubenMode(fbNo)
        if fbMode == const.FB_MODE_SPEED:
            self.cell.onClientEnterFuben()
        if self.inFuben():
            for en in BigWorld.entities.values():
                if en.IsAvatar and en.topLogo:
                    en.topLogo.hidePkTopLogo()

            self.preLoadFubenData()
            gameglobal.rds.ui.questTrack.refreshFubenTrack(True)
        else:
            self.clearPreLoadFubenData()
            gameglobal.rds.ui.ranking.hideTeamRankEval()
            for en in BigWorld.entities.values():
                if en.IsAvatar and en.topLogo:
                    en.topLogo.updatePkTopLogo()

            if not formula.spaceInMultiLine(self.spaceNo):
                gameglobal.rds.ui.diGong.closeDigongClock()
                gameglobal.rds.ui.diGong.onClosePanel()
                gameglobal.rds.ui.daFuWeng.hide()
                gameglobal.rds.ui.questTrack.refreshFubenTrack(False)
            self.endCalcDps()
            if AQULD.data.has_key((old, const.QD_ALLOW_SPACE)) or AQULD.data.has_key((self.spaceNo, const.QD_ALLOW_SPACE)):
                modifiedQuestIds = AQULD.data.get((old, const.QD_ALLOW_SPACE), []) + AQULD.data.get((self.spaceNo, const.QD_ALLOW_SPACE), [])
                self.onQuestInfoModifiedAtClient(const.QD_ALLOW_SPACE, {'questIds': modifiedQuestIds})
            if gameglobal.rds.ui.fightObserve.actionBarMediator:
                gameglobal.rds.ui.fightObserve.closeActionBar()
                gameglobal.rds.cam.reset()
            if formula.inHuntBattleField(formula.getMapId(old)):
                gameglobal.rds.ui.scoreInfo.hide()
                gameglobal.rds.ui.littleScoreInfo.hide()
                gameglobal.rds.ui.vehicleSkill.hide()
                gameglobal.rds.ui.vehicleChoose.hide()
        if formula.getMapId(old) == const.ML_SPACE_NO_WENQUAN_FLOOR1 and gameglobal.rds.ui.wenQuanDetail.isShow:
            gameglobal.rds.ui.wenQuanDetail.hide()
        sceneInfo.gAreaEventObj.deleteAreaEvent(self.spaceNo)
        if self.isShowFeedbackIcon():
            gameglobal.rds.ui.feedback.showIcon()
            gameglobal.rds.ui.feedback.closeFeedbackWidget()
        gameglobal.rds.ui.player.showDoubleExp()
        if hasattr(self, 'groupMapMark'):
            for key, val in self.groupMapMark.items():
                gamelog.debug('@hjx mapMark#set_spaceNo:', self.id, self.spaceNo, val, self.mapMarkStatus)
                if val['spaceNo'] == self.spaceNo and self.mapMarkStatus.has_key(key) and self.mapMarkStatus[key] == False:
                    if not self.attachFx.has_key(val['effectId']):
                        fx = self.attachEffect(val['effectId'], val['pos'], val['yaw'])
                        self.addFx(val['effectId'], fx)
                        self.mapMarkStatus[key] = True

            self.cell.updateMapMarkStatus(self.mapMarkStatus.keys(), self.mapMarkStatus.values())
        if self.mapID == const.ML_SPACE_NO_WENQUAN_FLOOR1:
            self.inWenQuanState = True
            clientcom.fetchTintEffectsContents(self.id, self.afterSetTintEffects)
        elif self.inWenQuanState and self.clientStateEffect:
            self.clientStateEffect._delDefaultModelState()
        if self.inFuben() and not self.inFubenTypes(const.FB_TYPE_ARENA) or formula.inPhaseSpace(self.spaceNo):
            gameglobal.rds.ui.map.openMap(False)
            gameglobal.rds.ui.questTrack.setLeaveBtnVisible(True)
            gameglobal.rds.ui.phaseFuben.closePhaseFubenList()
        else:
            gameglobal.rds.ui.questTrack.setLeaveBtnVisible(False)
            gameglobal.rds.ui.phaseFuben.hide()
        if formula.spaceInGuild(old) != formula.spaceInGuild(self.spaceNo):
            gameglobal.rds.ui.dispatchEvent(events.EVENT_GUILD_TUTORIAL_UPDATE)
        if formula.spaceInGuild(old) and not formula.spaceInGuild(self.spaceNo):
            while self.pendingGuildEntIds:
                self.pendingGuildEntIds.pop()

            while self.pendingGuildMarkerIds:
                self.pendingGuildMarkerIds.pop()

            self.clearGuildEntities()
            gameglobal.rds.ui.guildRobberActivityPush.hide()
            self.onLeaveGuildSpace()
            gameglobal.rds.ui.dispatchEvent(events.EVENT_LEAVE_GUILD_SPACE)
        elif not formula.spaceInGuild(old) and formula.spaceInGuild(self.spaceNo):
            gameglobal.rds.ui.dispatchEvent(events.EVENT_ENTER_GUILD_SPACE)
        gameglobal.rds.ui.topBar.switchTopBar()
        gameglobal.rds.ui.actionbar.updateEmoteItemCooldown()
        self._setMaxSlideAngleByMap()
        if not (formula.spaceInMultiLine(self.spaceNo) and formula.spaceInMultiLine(old)):
            Sound.stopCues()
            self.notifyMLDoubleExpFlag = False
            gameglobal.rds.ui.quickJoin.closeJoinClick()
        oldFbNo = formula.getFubenNo(old)
        fbNo = formula.getFubenNo(self.spaceNo)
        if oldFbNo not in BFD.data and fbNo in BFD.data:
            self.enterBFBefore()
            if formula.whatFubenType(fbNo) == const.FB_TYPE_BATTLE_FIELD_NEW_FLAG:
                self.resetTopLogo()
        if oldFbNo not in GCHD.data and fbNo in GCHD.data:
            gameglobal.rds.ui.guildChallengeField.enterChallengeBefore(fbNo)
        elif gameglobal.rds.ui.guildChallengeField.mediator:
            gameglobal.rds.ui.guildChallengeField.hide()
        gameglobal.rds.ui.chat.updatePadChannels()
        gameglobal.rds.tutorial.onLeaveMap(oldMapId)
        if self.isOnFlyRide():
            if formula.mapLimit(formula.LIMIT_WINGFLY, formula.getMapId(self.spaceNo)):
                self.cell.leaveFlyRide()
        self.resetCollideWithWater()
        if oldFbNo != fbNo:
            gameglobal.rds.ui.monsterClanWarActivity.startMonsterClanActivity()
        if gameglobal.rds.ui.questTrack:
            gameglobal.rds.ui.questTrack.updateWhenSpaceChange()
        if self.inWorldWarEx():
            gameglobal.rds.ui.worldWar.startCheckInactive()
        if not gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
            if self.inWorldWar():
                self.onCheckWWRobAura(False)
                self.onCheckBossHint()
        elif formula.spaceInWorldWarRob(self.spaceNo):
            self.onCheckWWRobAura(False)
            self.onCheckBossHint()
        VideoQualitySettingObj = appSetting.VideoQualitySettingObj
        VideoQualitySettingObj.resetAvatarModelNoDrawDist(VideoQualitySettingObj.getVideoQualityLv())
        VideoQualitySettingObj.setAvatarModelCnt()
        if gameglobal.rds.ui.diGongPuzzle.widget:
            gameglobal.rds.ui.diGongPuzzle.hide()
        if hasattr(self, 'topLogo') and self.topLogo:
            self.topLogo.showTitleEffect(self.curEffectTitleId)
        e = Event(events.EVENT_PLAYER_SPACE_NO_CHANGED, old)
        gameglobal.rds.ui.dispatchEvent(e)
        if hasattr(BigWorld, 'setTopLogoTotalUpdateCount'):
            if gameglobal.rds.configData.get('enableToplogoTotalOptimize', 0) and clientcom.needDoOptimize():
                optimizeCnt = gameglobal.rds.configData.get('enableToplogoTotalOptimize', gameglobal.TOPLOGO_TOTAL_OPTIMIZE)
                BigWorld.setTopLogoTotalUpdateCount(optimizeCnt)
            else:
                BigWorld.setTopLogoTotalUpdateCount(gameglobal.TOPLOGO_TOTAL_COUNT)
        self.recommendFriendOnLeaveMap(old, self.spaceNo)
        if hasattr(self, 'groupMark'):
            isHide = AppSettings.get(keys.SET_TEAM_TOP_LOGO_MARK, 1)
            if hasattr(self, 'topLogo') and (self.isInTeam() or self.isInGroup()):
                self.topLogo.setTeamTopLogo(self, isHide)
            ents = BigWorld.entities.values()
            for ent in ents:
                if ent.IsAvatar and (ent.isInTeam() or ent.isInGroup()):
                    if hasattr(ent, 'topLogo'):
                        ent.topLogo.setTeamTopLogo(ent, isHide)

        if formula.spaceInWingWorldXinMoArena(formula.getAnnalSrcSceneNo(old)) or formula.spaceInWingWorldXinMoArena(old):
            gameglobal.rds.ui.cheerTopBar.hide()
        if formula.spaceInWingWorldXinMoArena(self.spaceNo):
            self.enterArenaBefore()
        if formula.spaceInWingWorldXinMoArena(formula.getAnnalSrcSceneNo(self.spaceNo)) or formula.spaceInWingWorldXinMoArena(self.spaceNo):
            if gameglobal.rds.configData.get('enableWingWorldXinMo', False):
                roundNo = gameglobal.rds.ui.zhiQiangDuiJue.roundNo
                matchNo = gameglobal.rds.ui.zhiQiangDuiJue.matchNo
                gameglobal.rds.ui.cheerTopBar.show(roundNo, matchNo)
                gameglobal.rds.ui.zhiQiangDuiJue.hide()
                gameglobal.rds.ui.wingStageChoose.hide()
                gameglobal.rds.ui.combatHistory.hide()
        if formula.spaceInWingWorldXinMoUniqueBoss(formula.getAnnalSrcSceneNo(old)) or formula.spaceInWingWorldXinMoUniqueBoss(old):
            gameglobal.rds.ui.cheerTopBarBoss.hide()
        if formula.spaceInWingWorldXinMoUniqueBoss(formula.getAnnalSrcSceneNo(self.spaceNo)) or formula.spaceInWingWorldXinMoUniqueBoss(self.spaceNo):
            if gameglobal.rds.configData.get('enableWingWorldXinMo', False):
                gameglobal.rds.ui.zhiQiangDuiJue.hide()
                gameglobal.rds.ui.wingStageChoose.hide()
                gameglobal.rds.ui.combatHistory.hide()
        if formula.isBalanceArenaCrossServerML(formula.getMLGNo(old)):
            gameglobal.rds.ui.balanceArenaHover.hide()
        if formula.isBalanceArenaCrossServerML(formula.getMLGNo(self.spaceNo)):
            gameglobal.rds.ui.balanceArenaHover.show()
        self.setMapConfig(old)
        self.setCollideWithPlayer()
        self.setAnimationMemoryLimit()
        gameglobal.rds.ui.refreshPlayerPos(False)
        BigWorld.callback(2, self.checkGuildBonfire)
        if not self.isInRobSpace():
            gameglobal.rds.ui.worldWarRobResult.hidePanel()
            if self.worldWar.robBossHintTimeID:
                BigWorld.cancelCallback(self.worldWar.robBossHintTimeID)
                self.worldWar.robBossHintTimeID = 0
        if oldMapId == const.FB_NO_SCHOOL_TOP_MATCH and newMapId != const.FB_NO_SCHOOL_TOP_MATCH:
            self.leaveSchoolTopMatch()
        if oldMapId == const.FB_NO_SCHOOL_TOP_DPS:
            gameglobal.rds.ui.rankCommon.hide()
        if formula.spaceInWingBornIslandOrPeaceCity(newMapId):
            gameglobal.rds.ui.wingWorldMap.show()
        else:
            gameglobal.rds.ui.wingWorldMap.hide()
        if self.inClanChallengeOb():
            gameglobal.rds.ui.fightObserve.showActionBar()
        if formula.inTeamEndlessFubenSpace(self.spaceNo):
            gameglobal.rds.ui.voidLunHuiStart.clearAll()
            gameglobal.rds.ui.voidLunHuiBar.show()
        else:
            gameglobal.rds.ui.voidLunHuiBar.hide()
            gameglobal.rds.ui.voidLunHuiRank.clearAll()
        if formula.inNewFlagBattleField(formula.getMapId(old)):
            self.newFlagClear()
        from guis import spriteChallengeHelper
        if formula.inSpriteChallengeSpace(old):
            self.resultSpriteChallengeStats = {}
            gameglobal.rds.ui.spriteChallengeSelect.removePushMsg()
            gameglobal.rds.ui.spriteChallengeResult.hide()
            if not formula.inSpriteChallengeSpace(self.spaceNo):
                self.spriteChallengeProgress = 0
                spriteChallengeHelper.getInstance().setLinkedUIVisible(True)
        if formula.inSpriteChallengeSpace(self.spaceNo):
            if self.spriteChallengeProgress:
                gameglobal.rds.ui.spriteChallengeSelect.show(self.spriteChallengeProgress, False)
            spriteChallengeHelper.getInstance().setLinkedUIVisible(False)
        else:
            gameglobal.rds.ui.spriteChallengeSelect.hide()
        self.autoSetMapPkProtectConfig()
        self.checkTeamInfo()
        gameglobal.rds.ui.clanWarYaBiao.addPushIcon()
        gameglobal.rds.ui.huntGhost.pushMessage()
        sfx.gEffectMgr.LRUEffectCache.realClearEffectCache()
        gameAntiCheatingManager.getInstance().startRecordLog()

    def setAnimationMemoryLimit(self):
        animationMemLimit = gameglobal.ANIMATION_MEMORY_LIMIT
        if not BigWorld.isWow64():
            animationMemLimit = animationMemLimit / 2
        BigWorld.newAnimationMemoryLimit(1, animationMemLimit)

    def setCollideWithPlayer(self):
        if clientcom.needDoOptimize():
            self.collideWithPlayer = False
        else:
            self.collideWithPlayer = MCD.data.get(formula.getMapId(self.spaceNo), {}).get('collideWithPlayer', False)

    def showCancelHideInBFConfirm(self):
        fbNo = formula.getFubenNo(self.spaceNo)
        if fbNo in BFD.data or fbNo in SSCD.data or fbNo in AD.data:
            if gameglobal.gHideMode:
                msg = MSGDD.data.get('cancelBlockHideInBF_msg', '您当前屏蔽了玩家显示，是否取消屏蔽？（可通过F10设置屏蔽模式）')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.cancelHideConfirmCB, yesBtnText='确定', noCallback=None, noBtnText='取消')

    def showCancelHideInDiGong(self):
        p = BigWorld.player()
        mlgNo = formula.getMLGNo(p.spaceNo)
        showCancelHideTip = MDD.data.get(mlgNo, {}).get('showCancelHideTip', False)
        if gameglobal.gHideMode and showCancelHideTip and formula.getMLFloorNo(p.spaceNo) <= 0 and formula.getMLFloorNo(p.lastSpaceNo) <= 0:
            msg = MSGDD.data.get('cancelBlockHideInDG', '您当前屏蔽了玩家显示，是否取消屏蔽？（可通过F10设置屏蔽模式）')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.cancelHideConfirmCB, yesBtnText='确定', noCallback=None, noBtnText='取消')

    def queryBonusHistory(self):
        group = SCD.data.get('activityRobberHistory', 2086)
        self.cell.queryBonusHistory(group)

    def cancelHideConfirmCB(self):
        self.showGameMsg(GMDD.data.HIDE_NOBODY, ())
        gameglobal.HIDE_MODE_CUSTOM = 0
        self.switchHideModeCustom(False)

    def setSpaceShaderIndex(self, shaderIndex, forbidApplyShader):
        if self.shaderHandle:
            BigWorld.cancelCallback(self.shaderHandle)
        self.shaderHandle = BigWorld.callback(1, lambda : self._setShaderIndex(shaderIndex, forbidApplyShader))

    def _setShaderIndex(self, shaderIndex, forbidApplyShader):
        self.shaderHandle = None
        if forbidApplyShader:
            appSetting.setShaderIndex(shaderIndex, False, True)
            self.forbidApplyShader = True
        else:
            self.forbidApplyShader = False
            appSetting.setShaderIndex(shaderIndex, False, True)

    def onPhaseSpace(self, path, back):
        gamelog.debug('jorsef: onPhaseSpace', path, back, self.spaceID, gameglobal.rds.GameState)
        self.isInPhase = not back
        if self.isInPhase:
            self.phaseBounds = MCD.data.get(formula.getMapId(self.spaceNo), {}).get('mapBounds', None)
            if not self.checkPhaseAreaCallback:
                self.checkPhaseAreaState()
        if gameglobal.rds.GameState != gametypes.GS_LOADING:
            gameglobal.rds.sound.playPhaseMusic(self.mapID, self.isInPhase)
        if loadingProgress.gLastSpace != '':
            gameglobal.rds.cam.cc.firstPerson = 0
        loadingProgress.gLastSpace = path

    def showMsg(self, type, msg, color = const.CHANNEL_COLOR_GREEN):
        self.chatToEventEx(msg, color)

    def checkPathfinding(self):
        return self.isPathfinding

    def cancelPathfinding(self):
        if self.inForceNavigate:
            return
        navigator.getNav().stopPathFinding()

    def cancelDelayPathfinding(self):
        navigator.getNav().clearDelay()

    def movingNotifier(self, isMoving, moveSpeed = 1.0):
        gamelog.debug('#movingNotifier:', isMoving, moveSpeed, self.id)
        super(PlayerAvatar, self).movingNotifier(isMoving, moveSpeed)
        self.clearHoldingSkills()
        if isMoving:
            self.modelServer.poseManager.stopPoseModel()
            if self._getFlag(gametypes.FLAG_REMOVE_STATE_ON_MOVE):
                self.cell.removeStateOnMove()
        else:
            currentScrollNum = gameglobal.rds.cam.currentScrollNum
            if gameglobal.rds.cam.getKey(currentScrollNum) < 3:
                self.modelServer.poseManager.startLookAtPose()
            self.recordMoveToPosition()
            self.enterFlyRideWhenNeed()
        self.spriteOwnerMoving(isMoving)
        gameglobal.rds.cam.resetDepthOfField()
        gameglobal.rds.emoteFlag = {}
        self.tLastMoving = utils.getNow()

    def enterFlyRideWhenNeed(self):
        if not self.isOnFlyRide():
            return
        if self.inFly:
            return
        distanceFromWater = self.qinggongMgr.getDistanceFromWater()
        if not distanceFromWater:
            return
        if abs(distanceFromWater) > 0.1:
            return
        if self.bianshenStateMgr.canFly():
            self.cell.enterFlyRide()

    def recordMoveToPosition(self):
        try:
            record = gameglobal.rds.configData.get('recordMoveToPosition', False)
            if not record:
                return
            now = time.time()
            moveEndTime = getattr(self, 'moveEndTime', 0)
            if now - moveEndTime < 0.1:
                return
            protect.nepActionRoleMoveTo(protect.eMove_Default, self.position[0], self.position[2])
            self.moveEndTime = now
        except:
            pass

    def getFaceDir(self):
        return Math.Vector3(math.sin(self.yaw), 0, math.cos(self.yaw))

    def transferServer(self, hostId, account, info):
        gamelog.debug('zt: Avatar.transferServer', hostId, account, info)
        netWork.transferServer(hostId, account, info)

    def deleteModel(self, model):
        gamelog.debug('deleteModel:', model)
        self.delModel(model)

    def _refreshAllNearByEntities(self):
        ents = BigWorld.entities.values()
        if ents == None or len(ents) <= 0:
            return
        for ent in ents:
            if hasattr(ent, 'refreshOpacityState'):
                ent.refreshOpacityState()

    def showMagicField(self, down):
        pass

    def qinggongStateFailed(self, stype):
        gamelog.debug('qinggongStateFailed:', stype)
        super(PlayerAvatar, self).qinggongStateFailed(stype)
        if stype in gametypes.QINGGONG_STATE_DASH_SET:
            if self.qinggongMgr.jumpDashFlag:
                self.qinggongMgr.jumpDashFlag = False
            self.qinggongMgr.setState(qingGong.STATE_DASH)
            self.qinggongMgr.doFuncByEvent(qingGong.EVENT_DEFAULT)

    def qinggongActionFailed(self, qtype):
        gamelog.debug('----m.l@qinggongActionFailed:', qtype)
        super(PlayerAvatar, self).qinggongActionFailed(qtype)
        if qtype in (gametypes.QINGGONG_ROLL_LEFT,
         gametypes.QINGGONG_ROLL_RIGHT,
         gametypes.QINGGONG_ROLL_BACK,
         gametypes.QINGGONG_ROLL_FORWARD,
         gametypes.QINGGONG_ROLL_UP,
         gametypes.QINGGONG_ROLL_DOWN):
            if self.fashion.doingActionType() in (action.ROLL_ACTION, action.ROLLSTOP_ACTION):
                self.fashion.stopAllActions()
        self.ap.upwardMagnitude = 0
        self.qinggongMgr.setQingGongActionType(gametypes.QINGGONG_ACT_DEFAULT)
        if qtype in (gametypes.QINGGONG_DOUBLE_JUMP,
         gametypes.QINGGONG_FAST_RUN_JUMP,
         gametypes.QINGGONG_MOUNT_JUMP,
         gametypes.QINGGONG_FAST_RUN_DOUBLE_JUMP):
            if self.ap.jumpCnt >= 1:
                self.ap.jumpCnt -= 1

    def startEpRegenTime(self):
        super(PlayerAvatar, self).startEpRegenTime()
        self.lastEpRegenTime = time.time()

    def setGravity(self, gravity, forceUpdate = False):
        if self.inPUBGParachute():
            return
        if (self.canFly() or self.canSwim()) and not forceUpdate:
            if self.canFly() and self.isPathfinding or self.fashion.doingActionType() == action.WING_LAND_ACTION:
                self._setGravity(gravity)
            else:
                self._setGravity(0.0)
        else:
            self._setGravity(gravity)

    def _setGravity(self, gravity):
        if self.inChangeGravity:
            self.cacheGravity = gravity
        else:
            self.physics.gravity = gravity

    def upRiding(self):
        if not self.inRiding() and hasattr(self, 'equipment') and self.equipment[gametypes.EQU_PART_RIDE] and not self.equipment[gametypes.EQU_PART_RIDE].isExpireTTL():
            return self.enterRide()
        return False

    def lockKey(self, index, lockMouse = True):
        self.lockHotKey = commcalc.setSingleBit(self.lockHotKey, index, 1)
        gameglobal.rds.bar = None
        gameglobal.rds.soltId = None
        if lockMouse:
            self.ap.ccamera.canRotate = False
            self.ap.dcursor.canRotate = False
            self.lockMouseKey = 1

    def unlockKey(self, index):
        self.lockHotKey = commcalc.setSingleBit(self.lockHotKey, index, 0)
        self.lockMouseKey = 0

    def followPlayer(self, height, scale, m):
        pos = BigWorld.player().position
        m.position = (pos.x, pos.y + height, pos.z)
        m.yaw = BigWorld.player().yaw
        m.scale = (scale, scale, scale)
        self.followPlayer(height, scale, m)

    def testTime(self):
        gamelog.debug('jjh@Avatar.testTime, INFO:', self.cell.getServerTime(self.getServerTime() * 1000))

    def sendAccTutorial(self, data):
        gamelog.debug('hjx dehug tutor sendAccTutorial:', data)
        gameglobal.rds.tutorial.loadAccTutorial(data)

    def calcNpcGroundPos(self, npcId, offsetY):
        try:
            npc = BigWorld.entities[npcId]
        except KeyError:
            self.chatToGm('该NPC:%d 不存在/不在附近' % npcId)
            return

        res = BigWorld.findDropPoint(self.spaceID, npc.position + Math.Vector3(0, offsetY, 0))
        if res is None:
            self.chatToGm('该NPC:%d贴地失败,请增大偏移:%d' % (npcId, offsetY))
        else:
            position = res[0]
            self.cell.placeNpcGround(npcId, position, (npc.pitch, npc.roll, npc.yaw))

    def onGetSeekerMapData(self, datas):
        if writer.write2File(datas):
            gamelog.debug('ok')

    def doLoadHotKey(self):
        if self.hotkeyData:
            HK.loadHotkey(self.hotkeyData)
        self.reload()

    def addFogEffect(self, radius = 25.0):
        if getattr(self, 'fogModel', None):
            return
        charRes.getSimpleModel('scene/common_tech/unit_ball.model', None, Functor(self._afterFogModelFinished, radius))

    def _afterFogModelFinished(self, radius, model):
        self.fogModel = model
        self.addModel(self.fogModel)
        followMotor = BigWorld.Indicator()
        followMotor.follow = self.matrix
        self.fogModel.addMotor(followMotor)
        self.fogModel.scale = (radius, radius, radius)

    def delFogEffect(self):
        gamelog.debug('jorsef: delFogEffect')
        if not hasattr(self, 'fogModel') or self.fogModel == None:
            return
        self.delModel(self.fogModel)
        self.fogModel = None

    def hotfixMD5Send(self, smd5):
        gamelog.debug('jorsef: hotfix md5 Avatar', gameglobal.gHotfixMD5 != smd5)
        if gameglobal.gHotfixMD5 != smd5:
            self.base.fetchHotfix()

    def onPushAppMsg(self, info):
        gamelog.debug('@hjx app#onPushAppMsg:', info)
        gameglobal.rds.ui.daShan.addDaShanList(info)

    def onLoadAppMsg(self, info):
        info = cPickle.loads(zlib.decompress(info))
        gameglobal.rds.ui.daShan.setDaShanList(info)

    def notifyRefMonster(self, spaceNo, spaceMonsters, msg):
        if self.spaceNo != spaceNo:
            return
        self.showGameMsg(msg, ())
        for pos, monster in spaceMonsters:
            gameglobal.rds.ui.littleMap.showMonsterPoint(pos[0], pos[1])

    def notifyMonsterDie(self, spaceNo, charType, args):
        if self.spaceNo != spaceNo:
            return
        monsterData = MD.data.get(charType)
        if monsterData:
            msgId = monsterData.get('dieNotify', 0)
            if msgId:
                self.showGameMsg(msgId, *args)

    def toggleCollide(self):
        self.ap.physics.collide = not self.ap.physics.collide
        self.chatToGm((self.ap.physics.collide and '开启' or '关闭') + '主角碰撞')

    def onReturnToCharacterSelectPanel(self):
        gamelog.debug('@zs returnToCharactreSelelct playerAvatar')
        chatDB = getattr(self, 'chatDB', None)
        game.clearAll(False)
        self.clientInnerRange = ()
        self.clientOuterRange = ()
        self.skillRanges.clear()
        self.cancelAllCallback()
        BigWorld.worldDrawEnabled(False)
        gameglobal.rds.ui.characterDetailAdjust.showTips('正返回人物选择界面。。。', 1)
        gameglobal.rds.GameState = gametypes.GS_LOGIN
        if chatDB != None:
            chatDB.close()
        keyboardEffect.removeKeyboardEffect('effect_background')

    def cancelAllCallback(self):
        BigWorld.clearCallback()

    def switchWeaponState(self, weaponState, haveAct = True, forceSwitch = False):
        cellCmd.switchWeaponState(weaponState)
        super(PlayerAvatar, self).switchWeaponState(weaponState, haveAct, forceSwitch)

    def fangKaDian(self):
        if not self.stateMachine.checkStatus(const.CT_FANG_KA_DIAN):
            return
        if not MCD.data.get(formula.getMapId(self.spaceNo), {}).get('fangKaDian', 0) and not formula.spaceInClanWarPhase(self.spaceNo):
            self.showGameMsg(GMDD.data.FANG_KA_DIAN_NOT_ALLOWED, ())
            return
        if self.inWingWarCity():
            self.cell.wingWorldWarTeleportToOwnerReliveBoard(self.wingWorldMiniMap.hostMinMap.defaultReliveBoardEntNo)
            return
        ents = BigWorld.entities.values()
        try:
            if ents:
                for ent in ents:
                    if ent and ent.__class__.__name__ == 'ClanWarReliveBoard':
                        guildNUID = getattr(ent, 'guildNUID', None)
                        if guildNUID and guildNUID == getattr(self, 'guildNUID', None):
                            if (ent.position - self.position).length < SCD.data.get('clanWarReliveBoardKaDianLimit', 40):
                                self.showGameMsg(GMDD.data.FANG_KA_DIAN_CLAN_WAR_NOT_ALLOWED, ())
                                return

        except:
            pass

        navigator.getNav().getNearbyPoint(self.position, self.spaceNo, self._fangKaDian)

    def _fangKaDian(self, pointNum, dist, point):
        gamelog.debug('l.b.@fangkadian', pointNum, dist, point)
        if self.inClanWar:
            self.cell.fangKaDian(Math.Vector3(0, 0, 0), False)
            return
        fangkaDist = const.FANG_KA_DIAN_DIST
        if self.inPubgZone():
            fangkaDist = DCD.data.get('pubgFangkaDist', const.FANG_KA_DIAN_DIST)
        if pointNum > 0:
            if dist <= fangkaDist:
                self.cell.fangKaDian(Math.Vector3(point[0], point[1], point[2]), True)
                return
        if self.isInPUBG():
            self.showGameMsg(GMDD.data.FANG_KA_DIAN_NOT_ALLOWED_PUBG, ())
        else:
            self.cell.fangKaDian(Math.Vector3(0, 0, 0), False)

    def reportEngineException(self, eType, content, lv):
        self.base.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_ENGINE, [content], lv, '', '', '')

    def questionQuery(self, qId, answer, birthday, tOn, tOff, host):
        gameglobal.rds.ui.help.showQueryResult(qId, answer, birthday, tOn, tOff, host)

    def onSpaceData(self, spaceID, key, data):
        if not self:
            return
        if not self.inWorld:
            return
        spaceData.instance().set(spaceID, key, data)

    def onEnterSpace(self):
        if not self:
            return
        if not self.inWorld:
            return
        BigWorld.callback(0.1, Functor(spaceData.instance().enterSpace, self.spaceID))

    def preLoadFubenData(self):
        fbNo = formula.getMapId(self.spaceNo)
        data = FPD.data.get(fbNo, {})
        self.clearPreLoadFubenData()
        if data:
            effs = data.get('effectId', [])
            for eff in effs:
                sfx.gEffectMgr.preloadFx(eff, self.monsterEffectLv)

            models = data.get('modelId', [])
            actionLists = data.get('actionList', {})
            for model in models:
                path = clientUtils.getModelPath(model)
                gamelog.debug('preLoadArenaData', path)
                actionList = actionLists.get(model, [])
                charRes.getSimpleModel(path, None, Functor(self._peloadModelFinished, actionList))

    def clearPreLoadFubenData(self):
        self.holdPreLoadModel = []

    def _peloadModelFinished(self, actionList, model):
        if len(actionList) > 0:
            if hasattr(self, 'holdPreLoadModel') and model not in self.holdPreLoadModel:
                self.holdPreLoadModel.append(model)
            if model and hasattr(model, 'resideActions'):
                model.resideActions(*actionList)

    def setCameraSensitivity(self, value):
        BigWorld.dcursor().mouseSensitivity = max(value * 0.001, 0.003)

    def reportClientException(self, msgType, msgList, msgLv, extra):
        if gameconfigCommon.enableUploadTBToAppdump():
            self.exception.uploadTB(msgList)
            return
        if not hasattr(self, 'lastReportExceptionTime'):
            self.lastReportExceptionTime = 0
        now = time.time()
        if now - self.lastReportExceptionTime < 1:
            return
        self.lastReportExceptionTime = now
        digest = extra.get('digest', '')
        user = self.roleName if hasattr(self, 'roleName') else ''
        localIP = socket.gethostbyname(socket.gethostname())
        enableRecursionLog = gameglobal.rds.configData.get('enableRecursionLog', False)
        if enableRecursionLog:
            recursion = False
            if msgList:
                for m in msgList:
                    if 'recursion' in m:
                        recursion = True

                if recursion:
                    msgList.append(str(utils.logList))
            utils.clearLog()
        self.base.reportClientException(msgType, msgList, msgLv, digest, user, localIP)

    def updateBodySlope(self):
        super(PlayerAvatar, self).updateBodySlope()
        if self.physics:
            modelHeight = self.getModelHeight()
            if hasattr(self.model, 'floatage') and self.model.floatage:
                modelHeight += self.model.floatage.floatHeight
            self.physics.modelHeight = max(modelHeight, 1.4)

    def onEnvHurt(self):
        collideRes = BigWorld.collide(self.spaceID, self.position + Math.Vector3(0, 1, 0), self.position + Math.Vector3(0, -0.25, 0))
        if collideRes and collideRes[2] == gametypes.MATERIAL_TYPE_LAVA:
            self.cell.selfInjure(gametypes.CLIENT_HURT_BY_ENV, 1.0, 0)
            self.envHurtTimerId = BigWorld.callback(1.0, self.onEnvHurt)
        else:
            self.envHurtTimerId = 0

    def updateClientConfig(self, config):
        import gameconfigCommon
        rawConf = gameconfigCommon.convertDataWithCid(cPickle.loads(zlib.decompress(config)))
        gameglobal.resetConfigData()
        gameglobal.rds.configData.update(rawConf)
        gameConfigUtils.updateClientConfigFromAvatar(gameglobal.rds.configData)

    def updateClientConfigForOne(self, config):
        gameglobal.rds.configData.update(config)
        gameConfigUtils.updateClientConfigFromAvatar(config)

    def relogNotify(self):
        self.motionPin()
        self.relogNotifyState = True
        gameglobal.rds.relogStr = '你已被顶号，请稍后\n'
        if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            scenario.Scenario.getInstanceInPlay().stopPlay()
        gameglobal.rds.ui.messageBox.show(True, '返回登录界面', gameglobal.rds.relogStr, [])

    def logClientInfo(self):
        if not self.inWorld:
            return
        memUsage = BigWorld.getMemoryInfo()
        screenSize = BigWorld.screenSize()
        fps = BigWorld.getFps()
        direction = (self.roll, self.pitch, self.yaw)
        latency = BigWorld.LatencyInfo().value[3]
        self.latency[self.logCnt] = latency
        self.logCnt = (self.logCnt + 1) % 5
        videoQuality = appSetting.VideoQualitySettingObj._value[1]
        isAppActive = int(gameglobal.gIsAppActive)
        limitForegroundFPS = int(gameglobal.FORGROUND_FPS) if gameglobal.FORGROUND_FPS < gameglobal.LIMIT_MAX_FPS else 1000
        limitBackgroundFPS = int(gameglobal.BACKGROUND_FPS) if gameglobal.BACKGROUND_FPS < gameglobal.LIMIT_MAX_FPS else 1000
        hasDesktopShortcut = getattr(self, 'hasDesktopShortcut', 2)
        uuStatus = uuControl.UU_STATUS
        if hasattr(BigWorld, 'monitorWidth'):
            monitorWidth = BigWorld.monitorWidth()
        else:
            monitorWidth = 0
        if hasattr(BigWorld, 'monitorHeight'):
            monitorHeight = BigWorld.monitorHeight()
        else:
            monitorHeight = 0
        data = [str(self.spaceNo),
         str(self.position),
         str(direction),
         str(memUsage),
         str(screenSize),
         str(fps),
         str(latency),
         str(videoQuality),
         str(isAppActive),
         str(limitForegroundFPS),
         str(limitBackgroundFPS),
         str(hasDesktopShortcut),
         str(uuStatus),
         str(self.pgBreaker),
         str(monitorWidth),
         str(monitorHeight)]
        self.base.recordClientLog(gametypes.CLIENT_RECORD_TYPE_CLIENT_INFO, data)
        self.logCallback = BigWorld.callback(120, self.logClientInfo)

    def logClientSetting(self):
        try:
            enableModelRoll = AppSettings[keys.SET_DISABLE_MODEL_ROLL]
        except:
            enableModelRoll = 0

        data = [str(enableModelRoll)]
        self.base.recordClientLog(gametypes.CLIENT_RECORD_TYPE_SETTING, data)

    def onGuildIconDownloadNOSFile(self, status, callbackArgs):
        self.cell.setGuildIconStatus(status)
        gameglobal.rds.ui.zhanQi.refreshUserDefineInfo()
        if self.guildIconStatus == gametypes.NOS_FILE_STATUS_PENDING:
            self.downloadNOSFileDirectly(const.IMAGES_DOWNLOAD_RELATIVE_DIR, self.guildIcon, gametypes.NOS_FILE_PICTURE, self.onGuildIconDownloadNOSFileDirectly, (None,))

    def onGuildIconDownloadNOSFileDirectly(self, status, callbackArgs):
        gameglobal.rds.ui.zhanQi.refreshUserDefineInfo()

    def onGuildFlagIconDownloadNOSFile(self, status):
        self.guildFlagIconStatus = status

    def getClientShip(self, clientEntityId):
        spaceClientEntities = self.spaceClientEntities
        if not spaceClientEntities:
            return
        keyNo = None
        if self.inFuben():
            keyNo = formula.getFubenNo(self.spaceNo)
        elif self.inMLSpace():
            keyNo = formula.getMLNo(self.spaceNo)
        if not keyNo:
            return
        entDict = spaceClientEntities.get(keyNo, {})
        if not entDict:
            return
        if clientEntityId and entDict.has_key(clientEntityId):
            entId = entDict.get(clientEntityId, 0)
            clientShip = BigWorld.entities.get(entId, None)
            return clientShip

    def hideClientShip(self, clientEntityId):
        clientShip = self.getClientShip(clientEntityId)
        if clientShip and getattr(clientShip, 'model', None):
            clientShip.model.visible = False

    def showClientShip(self, clientEntityId):
        clientShip = self.getClientShip(clientEntityId)
        if clientShip and getattr(clientShip, 'model', None):
            clientShip.model.visible = True

    def forbidChat(self, talkerName):
        gameglobal.rds.ui.chat.forbidChat(talkerName)

    def getOpacityValue(self):
        scenarioIns = scenario.Scenario.PLAY_INSTANCE if scenario.Scenario.PLAY_INSTANCE else scenario.Scenario.INSTANCE
        if scenarioIns and self.isPlayingAmericanMarriageScenario() and self.isWifeOrHusband():
            return (gameglobal.OPACITY_FULL, True)
        if scenarioIns and self.isPlayingFightForLoveScenario() and self.isFightForLoveScenarioActor():
            return (gameglobal.OPACITY_FULL, True)
        if scenarioIns and gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            if scenarioIns.hidePlayer:
                return (gameglobal.OPACITY_HIDE, False)
        if gameglobal.rds.ui.fullscreenFittingRoom.mediator or gameglobal.rds.ui.tuZhuang.med:
            return (gameglobal.OPACITY_HIDE, False)
        if self.inFightObserve():
            return (gameglobal.OPACITY_HIDE, False)
        return super(PlayerAvatar, self).getOpacityValue()

    def resetJingSuTuneTime(self):
        self.jingsuTotalTuneTime = 0

    def setJingSuTuneTime(self, tuneTime, maxTuneTime):
        if self.jingsuTotalTuneTime <= maxTuneTime:
            self.showGameMsg(GMDD.data.JINGSU_TUNE_TIME_LIMITED, ())
            return
        old = self.jingsuTotalTuneTime
        self.jingsuTotalTuneTime = max(maxTuneTime, self.jingsuTotalTuneTime + tuneTime)
        gameglobal.rds.ui.qingGongJingSuTime.setPotTime(self.jingsuTotalTuneTime - old)

    def sendStatistic(self, hostid, send):
        gameglobal.rds.gServerid = hostid

    def clientPersistentNotify(self, add, notifyType, notifyArgs):
        if not self.inWorld:
            return
        if notifyType not in self.clientPersistentNotifyList:
            self.clientPersistentNotifyList[notifyType] = []
        for notifyId in notifyArgs:
            if add and notifyId not in self.clientPersistentNotifyList[notifyType]:
                self.clientPersistentNotifyList[notifyType].append(notifyId)
            if not add and notifyId in self.clientPersistentNotifyList[notifyType]:
                self.clientPersistentNotifyList[notifyType].remove(notifyId)

        if notifyType == gametypes.CLIENT_PERSISTENT_NOTIFY_MAP:
            gameglobal.rds.ui.littleMap.refreshNpcPos()
        elif notifyType == gametypes.CLIENT_PERSISTENT_NOTIFY_MAP_MONSTER_CLAN_WAR:
            gameglobal.rds.ui.zhanJu.updateView()

    def transferBack(self):
        if hasattr(gameglobal.rds, 'cipherOfPerson'):
            self.cipherOfPerson = gameglobal.rds.cipherOfPerson

    def crossServerCipher(self):
        if self._isSoul() and hasattr(gameglobal.rds, 'cipherOfPerson'):
            self.cipherOfPerson = gameglobal.rds.cipherOfPerson

    def doUIEvent(self, eventType):
        if eventType == gametypes.UI_EVENT_FULL_SCREEN_HONG_BAO:
            gameglobal.rds.ui.showHongBao(random.randint(5, 10))

    def queryClientVar(self, uuid, queryString):
        script = '%s.%s' % ('ent', queryString)
        try:
            res = ScriptRunningEnv.processExec(script, 'ret(%s)' % (script,), {'ent': BigWorld.player()})
            res = str(res) + ' type:' + str(type(res))
            res = res.replace('<', '&lt;').replace('>', '&gt;')
        except:
            import sys
            res = 'Unexpected error: %s' % (str(sys.exc_info()[:2]),)
            res = res.replace('<', '&lt;').replace('>', '&gt;')

        self.base.onQueryClientVar(uuid, res)

    def notifyWSDaoHengFull(self, id):
        if gameglobal.rds.ui.skill.daoHangDirMediator and id == gameglobal.rds.ui.skill.skillId:
            return
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WS_DAOHANG_NOTIFY, {'click': Functor(self.onNotifyWSDaoHengClick, id)})
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WS_DAOHANG_NOTIFY)

    def onNotifyWSDaoHengClick(self, skillId):
        if uiConst.MESSAGE_TYPE_WS_DAOHANG_NOTIFY in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WS_DAOHANG_NOTIFY)
        gameglobal.rds.ui.skill.openWuDaoPanel(skillId)

    def executeClientCmd(self, uuid, clientCmd):
        try:
            res = ScriptRunningEnv.processExec(clientCmd, 'ret(%s)' % (clientCmd,), globals())
            res = str(res) + ' type:' + str(type(res))
            res = res.replace('<', '&lt;').replace('>', '&gt;')
        except:
            import sys
            res = 'Unexpected error: %s' % (str(sys.exc_info()[:2]),)
            res = res.replace('<', '&lt;').replace('>', '&gt;')

        self.base.onQueryClientVar(uuid, res)

    def onCbgRoleStartSelling(self):
        self.isInCbgRoleSelling = True

    def onCbgRoleFinishSelling(self):
        self.isInCbgRoleSelling = False


def preload(preLoadlist):
    preLoadlist += PLD.getPreloadList()


def preloadNow(item):
    PLD.preloadModel(item)


funcMapOfClient = {func.groupQuery: PlayerAvatar.groupQuery,
 func.groupArrange: PlayerAvatar.groupArrange,
 func.groupRequest: PlayerAvatar.groupRequest,
 func.groupRecommend: PlayerAvatar.groupRecommend,
 func.groupAward: PlayerAvatar.groupAward,
 func.arenaStart: PlayerAvatar.arenaStart,
 func.arenaQuery: PlayerAvatar.arenaQuery,
 func.arenaEndNotify: PlayerAvatar.arenaEndNotify,
 func.arenaApplySucc: PlayerAvatar.arenaApplySucc,
 func.arenaCountDown: PlayerAvatar.arenaCountDown,
 func.arenaChallengeQuickStart: PlayerAvatar.arenaChallengeQuickStart,
 func.arenaSyncPrepareDict: PlayerAvatar.arenaSyncPrepareDict,
 func.notifyLeaveArena: PlayerAvatar.notifyLeaveArena,
 func.arenaResultNotify: PlayerAvatar.arenaResultNotify,
 func.battleFieldEndNotify: PlayerAvatar.battleFieldEndNotify,
 func.battleFieldCountDown: PlayerAvatar.battleFieldCountDown,
 func.battleFieldFirstBloodNotify: PlayerAvatar.battleFieldFirstBloodNotify,
 func.battleFieldArrange: PlayerAvatar.battleFieldArrange,
 func.battleFieldKillAvatar: PlayerAvatar.battleFieldKillAvatar,
 func.shengSiChangQuery: PlayerAvatar.shengSiChangQuery,
 func.shengSiChangCountDown: PlayerAvatar.shengSiChangCountDown,
 func.shengSiChangEndNotify: PlayerAvatar.shengSiChangEndNotify,
 func.teamShengSiChangEndNotify: PlayerAvatar.teamShengSiChangEndNotify,
 func.teamShengSiChangCountDown: PlayerAvatar.teamShengSiChangCountDown,
 func.partnerQuery: Avatar.partnerQuery,
 func.tradeRequest: Avatar.tradeRequest,
 func.tradeConfirm: Avatar.tradeConfirm,
 func.tradeUnConfirm: Avatar.tradeUnConfirm,
 func.tradeStart: Avatar.tradeStart,
 func.tradeFinal: Avatar.tradeFinal,
 func.tradeFinish: Avatar.tradeFinish,
 func.tradeCancel: Avatar.tradeCancel,
 func.tradeCash: Avatar.tradeCash,
 func.tradeItem: Avatar.tradeItem,
 func.tradeItemFinish: Avatar.tradeItemFinish,
 func.questionQuery: PlayerAvatar.questionQuery,
 func.coupleRequest: PlayerAvatar.coupleRequest}
