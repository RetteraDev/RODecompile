#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/npcFuncMappings.o
from gamestrings import gameStrings
import BigWorld
import commNpcFavor
import npcConst
import gamelog
import gameglobal
import gametypes
import const
import utils
import formula
import Sound
import gameconfigCommon
import wingWorldUtils
from guis import uiUtils
from guis import uiConst
from callbackHelper import Functor
from helpers import cgPlayer
from data import dialogs_data as GD
from data import npc_data as ND
from data import item_data as ID
from cdata import font_config_data as FCD
from data import bonus_data as BD
from data import activity_desc_data as ADD
from data import clan_war_fort_data as CWFD
from data import chunk_mapping_data as CMD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import fame_data as FD
from data import fame_reward_bonus_data as FRBD
from data import npc_yabiao_data as NYD
from data import hobby_presale_config_data as HPCD
from data import quest_data as QD
from data import dawdler_data as DRD
from data import guild_config_data as GCD
from cdata import quest_npc_group_data as QNGD
from data import quest_npc_data as QND
from data import activity_reward_data as ACRD
from data import wing_world_config_data as WWCD
from data import duel_config_data as DCD
from cdata import region_server_name_data as RSND
from data import scenario_data as SCND
from gamestrings import gameStrings
CALL_TYPE_NPC_FUNC = 1
CALL_TYPE_DIRECTLY_F = 2
CALL_TYPE_ALL = 3
npcFuncMap = {}

def funcMap(functype, callType = CALL_TYPE_NPC_FUNC):

    def wrapper(func):
        if type(functype) == tuple:
            for functy in functype:
                npcFuncMap[functy, callType] = func

        else:
            npcFuncMap[functype, callType] = func
        return func

    return wrapper


def registerNpcFunc(functype, func, callType = CALL_TYPE_NPC_FUNC):
    npcFuncMap[functype, callType] = func


def onFuncState():
    gameglobal.rds.ui.funcNpc.onFuncState()


def close():
    gameglobal.rds.ui.funcNpc.close()


def getMappingFunc(functype, callType):
    if npcFuncMap.has_key((functype, callType)):
        return npcFuncMap[functype, callType]
    elif npcFuncMap.has_key((functype, CALL_TYPE_ALL)):
        return npcFuncMap[functype, CALL_TYPE_ALL]
    else:
        return None


def onImpPlayerCallFunc(functype, entId, options, hasQuest):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    npcData = ND.data.get(npcId, None)
    openType = npcData.get('full', 0)
    panelOpenType = npcData.get('open', 0)
    defaultChatId = ND.data.get(npcId, {}).get('chat', [])
    items = options.items()
    key, chatItem = items[0]
    npcFunc = getMappingFunc(functype, CALL_TYPE_DIRECTLY_F)
    if not npcFunc:
        return False
    else:
        params = {'openType': openType,
         'index': 0,
         'panelOpenType': panelOpenType,
         'defaultChatId': defaultChatId,
         'hasQuest': hasQuest,
         'options': options}
        npcFunc(functype, CALL_TYPE_DIRECTLY_F, entId, chatItem, params)
        return True


def onFuncNpcProxyCallFunc(functype, entId, chatOption, index):
    npcEnt = BigWorld.entity(entId)
    if not npcEnt:
        gamelog.error('dxk @onFuncNpcProxyCallFunc npc is null,return instead')
        close()
        return
    else:
        npcId = npcEnt.npcId
        npcData = ND.data.get(npcId, None)
        openType = npcData.get('full', 0)
        panelOpenType = npcData.get('open', 0)
        defaultChatId = ND.data.get(npcId, {}).get('chat', [])
        npcFunc = getMappingFunc(functype, CALL_TYPE_NPC_FUNC)
        if not npcFunc:
            return False
        chatItem = chatOption[index]
        params = {'openType': openType,
         'index': index,
         'panelOpenType': panelOpenType,
         'defaultChatId': defaultChatId}
        npcFunc(functype, CALL_TYPE_NPC_FUNC, entId, chatItem, params)
        return True


@funcMap(npcConst.NPC_FUNC_ITEM_ENHANCE)
def NPC_FUNC_ITEM_ENHANCE(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    if gameglobal.rds.configData.get('enableEquipChangeEnhance', False):
        close()
        gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_ENHANCE, 0)
    else:
        onFuncState()
        gameglobal.rds.ui.equipEnhance.show(entId)
        gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_ITEM_ENHANCEMENT_TRANSFER)
def NPC_FUNC_ITEM_ENHANCEMENT_TRANSFER(functype, callType, entId, chatItem, extraParams = None):
    if gameglobal.rds.configData.get('enableEquipChangeEnhance', False):
        close()
        gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_ENHANCE, 1)
    else:
        onFuncState()
        gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_ITEM_REFORGE_ENHANCE_JUEXING)
def NPC_FUNC_ITEM_REFORGE_ENHANCE_JUEXING(functype, callType, entId, chatItem, extraParams = None):
    if gameglobal.rds.configData.get('enableEquipChangeReforge', False):
        close()
        gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_REFORGE, 0)
    else:
        close()


@funcMap(npcConst.NPC_FUNC_EQUIP_WASH)
def NPC_FUNC_EQUIP_WASH(functype, callType, entId, chatItem, extraParams = None):
    if gameglobal.rds.configData.get('enableEquipChangeReforge', False):
        close()
        gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_REFORGE, 1)
    else:
        onFuncState()
        gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_EXCHANGE_EQUIP_PRE_PROP)
def NPC_FUNC_EXCHANGE_EQUIP_PRE_PROP(functype, callType, entId, chatItem, extraParams = None):
    if gameglobal.rds.configData.get('enableEquipChangeReforge', False):
        close()
        gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_REFORGE, 2)
    else:
        close()


@funcMap(npcConst.NPC_FUNC_EQUP_STAR_ACTIVATE)
def NPC_FUNC_EQUP_STAR_ACTIVATE(functype, callType, entId, chatItem, extraParams = None):
    if gameglobal.rds.configData.get('enableEquipChangeStar', False):
        close()
        gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_STAR, 0)
    else:
        onFuncState()
        gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_SUIT_ACTIVATE)
def NPC_FUNC_SUIT_ACTIVATE(functype, callType, entId, chatItem, extraParams = None):
    if gameglobal.rds.configData.get('enableEquipChangeSuit', False):
        close()
        gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_SUIT, 0)
    else:
        onFuncState()
        gameglobal.rds.ui.equipSuit.show()
        gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_FASHION_TRANSFER)
def NPC_FUNC_FASHION_TRANSFER(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.fashionPropTransfer.show()
    gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_RUBBING)
def NPC_FUNC_RUBBING(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.equipCopy.show(entId)
    gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_BIRDLET)
def NPC_FUNC_BIRDLET(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.birdLetHotLine.show(entId)


@funcMap(npcConst.NPC_FUNC_QUEST)
def NPC_FUNC_QUEST(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    if npc and npc.inWorld:
        player = BigWorld.player()
        debateQuestId = QND.data.get(npc.npcId, {}).get('debateQst', -1)
        if debateQuestId in player.quests and not player.getQuestData(debateQuestId, const.QD_QUEST_DEBATE) and not player.getQuestData(debateQuestId, const.QD_FAIL, True):
            npc.showDebateWindow()
        else:
            npc.showQuestWindow()


@funcMap(npcConst.NPC_FUNC_MIX_EQUIP)
def NPC_FUNC_MIX_EQUIP(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.equipMix.show(entId, chatItem[2])
    gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_MIX_EQUIP_NEW)
def NPC_FUNC_MIX_EQUIP_NEW(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.equipMixNew.show(entId, chatItem[2])
    gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_COPY_CHARACTER)
def NPC_FUNC_COPY_CHARACTER(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.characterCopy.show()


@funcMap(npcConst.NPC_FUNC_TRANSFER_EQUIP_PROPS)
def NPC_FUNC_TRANSFER_EQUIP_PROPS(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_UPGRADE_EQUIP)
def NPC_FUNC_UPGRADE_EQUIP(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    if chatItem[2] == npcConst.SPECIAL_FILTER_TYPE_WING:
        gameglobal.rds.ui.wingAndMountUpgrade.show(uiConst.WING_EVE, 0, -1, -1, entId)
    elif chatItem[2] == npcConst.SPECIAL_FILTER_TYPE_RIDE:
        gameglobal.rds.ui.wingAndMountUpgrade.show(uiConst.RIDE_EVE, 0, -1, -1, entId)
    gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_UNLOCK_EQUIP_GEM_SLOT)
def NPC_FUNC_UNLOCK_EQUIP_GEM_SLOT(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.equipmentSlot.show(entId)
    gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_APPLY_PK_MODE)
def NPC_FUNC_APPLY_PK_MODE(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    npc.cell.applyPolicePkMode()


@funcMap(npcConst.NPC_FUNC_ACTIVITY_REWARD)
def NPC_FUNC_ACTIVITY_REWARD(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    npc.cell.getActivityReward(chatItem[2])


@funcMap(npcConst.NPC_FUNC_ACCUMULAITED_ACTIVITY_REWARD)
def NPC_FUNC_ACCUMULAITED_ACTIVITY_REWARD(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    npc = BigWorld.entities.get(entId)
    close()
    totalSignInCnt = p.totalDailySignInCnt
    type = 0
    for reward in ACRD.data.get('*', []):
        signInCntLimit = reward.get('signInCntLimit', ())
        if signInCntLimit:
            if signInCntLimit[0] <= totalSignInCnt <= signInCntLimit[1]:
                type = reward.get('type', 0)

    if type:
        msg = gameStrings.ACCUMULAITED_ACTIVITY_REWARD_REMIND % totalSignInCnt
        if not gameglobal.rds.ui.funcNpc.msgBoxId:
            gameglobal.rds.ui.funcNpc.msgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(npc.cell.getActivityTotalDailySignInReward, type))


@funcMap(npcConst.NPC_FUNC_FB_AI)
def NPC_FUNC_FB_AI(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    if npc is not None:
        npc.showFbAIWindow(entId)


@funcMap(npcConst.NPC_FUNC_UNBIND_FRIENDSHIP)
def NPC_FUNC_UNBIND_FRIENDSHIP(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    if npc is not None:
        npc.showUnbindFriendshipWindow(entId)


@funcMap(npcConst.NPC_FUNC_APPLY_UNBIND_FRIENDSHIP_COOP)
def NPC_FUNC_APPLY_UNBIND_FRIENDSHIP_COOP(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    npc.cell.applyUnbindFriendshipWithCoop()


@funcMap(npcConst.NPC_FUNC_CANCEL_UNBIND_FRIENDSHIP_COOP)
def NPC_FUNC_CANCEL_UNBIND_FRIENDSHIP_COOP(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    npc.cell.cancelUnbindFriendshipWithCoop()


@funcMap(npcConst.NPC_FUNC_BIND_FRIENDSHIP_MULTI_CHOICE)
def NPC_FUNC_BIND_FRIENDSHIP_MULTI_CHOICE(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    if npc is not None:
        npc.showbindFriendshipWindow(entId)


@funcMap(npcConst.NPC_FUNC_FB_TRAINING)
def NPC_FUNC_FB_TRAINING(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.trainingArea.show(entId)


@funcMap(npcConst.NPC_FUNC_TELEPORT)
def NPC_FUNC_TELEPORT(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.npcPanel.showNpcFullScreen(entId)


@funcMap(npcConst.NPC_FUNC_ACCEPT_PRIZE)
def NPC_FUNC_ACCEPT_PRIZE(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.openPrizePanel(entId)


@funcMap(npcConst.NPC_FUNC_SHOP)
def NPC_FUNC_SHOP(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    onFuncState()
    npc.cell.openShop(chatItem[2])


@funcMap(npcConst.NPC_FUNC_TRAINING_AWARD)
def NPC_FUNC_TRAINING_AWARD(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    gameglobal.rds.ui.funcNpc.openDirectly(entId, npc.npcId, npcConst.NPC_FUNC_TRAINING_AWARD)
    gameglobal.rds.ui.trainingAreaAward.show()


@funcMap(npcConst.NPC_FUNC_APPLY_SHENG_SI_CHANG)
def NPC_FUNC_APPLY_SHENG_SI_CHANG(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    npc.cell.applyShengSiChang()


@funcMap(npcConst.NPC_FUNC_EXPLANATION)
def NPC_FUNC_EXPLANATION(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.funcNpc.openExplanationPanel(entId, chatItem[2])


@funcMap(npcConst.NPC_FUNC_CONTRACT)
def NPC_FUNC_CONTRACT(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    index = chatItem[2]
    if index:
        npc.formContract(index)
    else:
        npc.removeContract()


@funcMap(npcConst.NPC_FUNC_INTIMACY_REWARD)
def NPC_FUNC_INTIMACY_REWARD(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    npc and npc.cell.applyIntimacyYearlyReward()


@funcMap(npcConst.NPC_FUNC_ARENA_CHALLENGE)
def NPC_FUNC_ARENA_CHALLENGE(functype, callType, entId, chatItem, extraParams = None):
    close()
    sType = chatItem[2]
    if not gameglobal.rds.configData.get('enableArenaChallenge', False):
        BigWorld.player().showGameMsgEx(GMDD.data.ARENA_CHALLENGE_NOT_OPEN, ())
        return
    if sType == gametypes.ARENA_CHALLENGE_TYPE_APPLY:
        gameglobal.rds.ui.arenaChallengeApply.checkApplyRequest()
    elif sType == gametypes.ARENA_CHALLENGE_TYPE_ACCEPT:
        gameglobal.rds.ui.arenaChallengeDeclartion.showAcceptChallengeMsgBox()
    elif sType == gametypes.ARENA_CHALLENGE_TYPE_ENTER:
        gameglobal.rds.ui.arenaChallengeDeclartion.enterArena()
    elif sType == gametypes.ARENA_CHALLENGE_TYPE_QUERY:
        gameglobal.rds.ui.arenaChallengeReview.show()


@funcMap(npcConst.NPC_FUNC_INTIMACY_TIME_REGISTER)
def NPC_FUNC_INTIMACY_TIME_REGISTER(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    registerType = chatItem[2]
    npc and npc.cell.applyIntimacyRegister(registerType)


@funcMap(npcConst.NPC_FUNC_INTIMACY_REGISTER_REWARD)
def NPC_FUNC_INTIMACY_REGISTER_REWARD(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    registerType = chatItem[2]
    npc and npc.cell.applyIntimacyRegisterReward(registerType)


@funcMap(npcConst.NPC_FUNC_MAIL)
def NPC_FUNC_MAIL(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    npc.cell.openMail()


@funcMap(npcConst.NPC_FUMC_MARRIAGE_TYPE_CHOOSE)
def NPC_FUMC_MARRIAGE_TYPE_CHOOSE(functype, callType, entId, chatItem, extraParams = None):
    close()
    p = BigWorld.player()
    npc = BigWorld.entities.get(entId)
    if p.marriageType in (gametypes.MARRIAGE_TYPE_PACKAGE, gametypes.MARRIAGE_TYPE_GREAT):
        p.showGameMsg(GMDD.data.MARRIAGE_SUB_FAILED_ALREADY, ())
    elif p.marriageType == gametypes.MARRIAGE_TYPE_HIDE:
        p.showGameMsg(GMDD.data.MARRIAGE_SUB_FAILED_HIDE_MARRIAGE, ())
    else:
        npc.cell.marriageTypeChoose()


@funcMap(npcConst.NPC_FUMC_MARRIAGE_SET_INFO)
def NPC_FUMC_MARRIAGE_SET_INFO(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    p = BigWorld.player()
    if p.marriageType in (gametypes.MARRIAGE_TYPE_PACKAGE, gametypes.MARRIAGE_TYPE_GREAT):
        npc.cell.applyMarriagePackageInfoSet()
    else:
        p.showGameMsg(GMDD.data.MARRIAGE_PACKAGE_OPEN_FAILED_NO_MARRIAGE, ())


@funcMap(npcConst.NPC_FUMC_MARRIAGE_PARADE_MARCH)
def NPC_FUMC_MARRIAGE_PARADE_MARCH(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    p = BigWorld.player()
    if p.marriageType in (gametypes.MARRIAGE_TYPE_PACKAGE, gametypes.MARRIAGE_TYPE_GREAT):
        npc.cell.applyMarriageParade()
    else:
        p.showGameMsg(GMDD.data.MARRIAGE_PACKAGE_OPEN_FAILED_NO_MARRIAGE, ())


@funcMap(npcConst.NPC_FUNC_START_MARRIAGE)
def NPC_FUNC_START_MARRIAGE(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    npc.cell.applyMarriageStart()


@funcMap(npcConst.NPC_FUMC_MARRIAGE_ENTER_HALL)
def NPC_FUMC_MARRIAGE_ENTER_HALL(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    npc.cell.applyEnterMarriageHall()


@funcMap(npcConst.NPC_FUMC_MARRIAGE_DO_PLEDHE)
def NPC_FUMC_MARRIAGE_DO_PLEDHE(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    npc.cell.applyPledgeMarriageHall()


@funcMap(npcConst.NPC_FUMC_MARRIAGE_ENTER_ROOM)
def NPC_FUMC_MARRIAGE_ENTER_ROOM(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    npc.cell.applyEnterMarriageRoom()


@funcMap(npcConst.NPC_FUNC_MARRIAGE_RING_EXCHAGE)
def NPC_FUNC_MARRIAGE_RING_EXCHAGE(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    npc.cell.applyMarriageRingExchange()


@funcMap(npcConst.NPC_FIGHT_FOR_LOVE_APPLY)
def NPC_FIGHT_FOR_LOVE_APPLY(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.fightForLoveApply.show()


@funcMap(npcConst.NPC_FIGHT_FOR_LOVE_LINES)
def NPC_FIGHT_FOR_LOVE_LINES(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.fightForLoveLines.show()


@funcMap(npcConst.NPC_FUNC_CONSIGN)
def NPC_FUNC_CONSIGN(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    npc.cell.openConsign()


@funcMap(npcConst.NPC_FUNC_GUILD)
def NPC_FUNC_GUILD(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    op = chatItem[2]
    if op == gametypes.GUILD_NPC_OPTION_CREATE:
        npc.cell.openCreateGuild()
    elif op == gametypes.GUILD_NPC_OPTION_LIST:
        npc.cell.openGuildList()
    elif op == gametypes.GUILD_NPC_OPTION_BUILDING:
        gameglobal.rds.ui.guildBuildSelect.show(markerId=getattr(npc, 'markerId', 0), buildingNUID=npc.buildingNUID, npcId=npc.id)
    elif op == gametypes.GUILD_NPC_OPTION_ENTER:
        npc.cell.enterGuildScene()
    elif op == gametypes.GUILD_NPC_OPTION_EXIT:
        npc.cell.exitGuildScene()
    elif op == gametypes.GUILD_NPC_OPTION_FUNC:
        gameglobal.rds.ui.guild.openGuildBuilding(buildingNUID=npc.buildingNUID, npcEntityId=npc.id)
    elif op == gametypes.GUILD_NPC_OPTION_QUERY_RESIDENT:
        npc.cell.queryGuildResident()
    elif op == gametypes.GUILD_NPC_OPTION_RECOMMEND_RESIDENT:
        npc.cell.recommendGuildResident()
    elif op == gametypes.GUILD_NPC_OPTION_RECOMMENDED_RESIDENT:
        gameglobal.rds.ui.funcNpc.openDirectly(entId, npc.npcId, npcConst.NPC_FUNC_GUILD)
        gameglobal.rds.ui.guildResidentRec.show()
    elif op == gametypes.GUILD_NPC_OPTION_HIRED_RESIDENT:
        gameglobal.rds.ui.funcNpc.openDirectly(entId, npc.npcId, npcConst.NPC_FUNC_GUILD)
        gameglobal.rds.ui.guildResidentHired.show()
    elif op == gametypes.GUILD_NPC_OPTION_VIEW_HIRED_RESIDENT:
        if npc:
            gameglobal.rds.ui.guildResident.show(uiConst.GUILD_RESIDENT_PANEL_HIRED, npc.residentNUID)
    elif op == gametypes.GUILD_NPC_OPTION_ASSIGN_JOB:
        if npc:
            gameglobal.rds.ui.guildDispatch.show(npc.residentNUID)
    elif op == gametypes.GUILD_NPC_OPTION_RENAME:
        gameglobal.rds.ui.funcNpc.openDirectly(entId, npc.npcId, npcConst.NPC_FUNC_GUILD)
        gameglobal.rds.ui.guildRename.show()
    elif op == gametypes.GUILD_NPC_OPTION_WS_PRACTICE:
        gameglobal.rds.ui.funcNpc.openDirectly(entId, npc.npcId, npcConst.NPC_FUNC_GUILD)
        gameglobal.rds.ui.guildWuShuang.show()
    elif op == gametypes.GUILD_NPC_OPTION_APPLY_BUSINESS_MAN:
        npc.cell.applyGuildBusinessMan()
    elif op == gametypes.GUILD_NPC_OPTION_CANCEL_BUSINESS_MAN:
        npc.cell.cancelGuildBusinessMan()
    elif op == gametypes.GUILD_NPC_OPTION_RECV_INHERIT_FROM_NPC:
        msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_INHERIT_FROM_NPC_MSG, '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, npc.cell.tryRecvGuildInheritFromNpc)


@funcMap(npcConst.NPC_FUNC_WORLD_WAR)
def NPC_FUNC_WORLD_WAR(functype, callType, entId, chatItem, extraParams = None):
    op = chatItem[2]
    if op == gametypes.WORLD_WAR_NPC_OP_ENTER_OWN:
        BigWorld.player()._enterWorldWarOwn()
    elif op == gametypes.WORLD_WAR_NPC_OP_ENTER_ENEMY:
        BigWorld.player()._enterWorldWarEnemy()
    close()


@funcMap(npcConst.NPC_FUNC_GUILD_BUILDING_REMOVE)
def NPC_FUNC_GUILD_BUILDING_REMOVE(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.guildBuildSelectRemove.show(chatItem[2])


@funcMap(npcConst.NPC_FUNC_CLAN)
def NPC_FUNC_CLAN(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    op = chatItem[2]
    if op == gametypes.CLAN_NPC_OPTION_CREATE:
        npc.cell.openCreateClan()
    elif op == gametypes.CLAN_NPC_OPTION_LIST_FOR_JOIN:
        npc.cell.openClanList(op)
    elif op == gametypes.CLAN_NPC_OPTION_LIST_FOR_DISP:
        npc.cell.openClanList(op)


@funcMap(npcConst.NPC_FUNC_GUILD_RUN_MAN)
def NPC_FUNC_GUILD_RUN_MAN(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    runManType = chatItem[2]
    if runManType == 1:
        msg = GMD.data.get(GMDD.data.DAILY_RUN_MAN_HELP_MSG, {}).get('text', gameStrings.TEXT_NPCFUNCMAPPINGS_599)
    else:
        msg = GMD.data.get(GMDD.data.WEEK_RUN_MAN_HELP_MSG, {}).get('text', gameStrings.TEXT_NPCFUNCMAPPINGS_601)
    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(npc.cell.startGuildRunMan, runManType))


@funcMap(npcConst.NPC_FUNC_GUILD_RUN_MAN_VIEW)
def NPC_FUNC_GUILD_RUN_MAN_VIEW(functype, callType, entId, chatItem, extraParams = None):
    close()
    runManType = chatItem[2]
    gameglobal.rds.ui.guildRunner.setType(runManType)
    gameglobal.rds.ui.guildRunner.show()


@funcMap(npcConst.NPC_FUNC_GUILD_ROBBER_CHALLENGE)
def NPC_FUNC_GUILD_ROBBER_CHALLENGE(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    npc.cell.applyRobberChallenge()
    close()


@funcMap(npcConst.NPC_FUNC_CLAN_WAR)
def NPC_FUNC_CLAN_WAR(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    npc.cell.requestOpenClanWar()


@funcMap(npcConst.NPC_FUNC_RUNE)
def NPC_FUNC_RUNE(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    gameglobal.rds.ui.funcNpc.openDirectly(entId, npc.npcId, npcConst.NPC_FUNC_RUNE)
    gameglobal.rds.ui.runeLvUp.show(entId)
    gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_COMPOSITE_SHOP)
def NPC_FUNC_COMPOSITE_SHOP(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    onFuncState()
    gameglobal.rds.ui.funcNpc.openDirectly(entId, npc.npcId, npcConst.NPC_FUNC_COMPOSITE_SHOP)
    npc.cell.openCompositeShop(chatItem[2])


@funcMap(npcConst.NPC_FUNC_PRIVATE_SHOP)
def NPC_FUNC_PRIVATE_SHOP(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    onFuncState()
    gameglobal.rds.ui.funcNpc.openDirectly(entId, npc.npcId, npcConst.NPC_FUNC_PRIVATE_SHOP)
    uiUtils.closeCompositeShop()
    BigWorld.player().base.openPrivateShop(0, chatItem[2])


@funcMap(npcConst.NPC_FUNC_RUNE_FORGING)
def NPC_FUNC_RUNE_FORGING(functype, callType, entId, chatItem, extraParams = None):
    close()
    op = chatItem[2]
    if op == uiConst.GUILD_RUNE_FORGING:
        gameglobal.rds.ui.runeForging.show(entId)
    elif op == uiConst.GUILD_RUNE_REFORGING:
        gameglobal.rds.ui.runeReforging.show(entId)


@funcMap(npcConst.NPC_FUNC_COMPENSATE)
def NPC_FUNC_COMPENSATE(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.openAwardPanel(functype, entId)


@funcMap(npcConst.NPC_FUNC_POINT_REFUND)
def NPC_FUNC_POINT_REFUND(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.openAwardPanel(functype, entId)


@funcMap(npcConst.NPC_FUNC_FORT_OCCUPY_AWARD)
def NPC_FUNC_FORT_OCCUPY_AWARD(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.openAwardPanel(functype, entId)


@funcMap(npcConst.NPC_FUNC_GUILD_RANK_AWARD)
def NPC_FUNC_GUILD_RANK_AWARD(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.openAwardPanel(functype, entId)


@funcMap(npcConst.NPC_FUNC_GUILD_RESIDENT_TIRED)
def NPC_FUNC_GUILD_RESIDENT_TIRED(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.guildResidentUpdateTired.show(entId)


@funcMap(npcConst.NPC_FUNC_FAME_REWARD)
def NPC_FUNC_FAME_REWARD(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.openFameSalaryPanel(entId, chatItem[2])


@funcMap(npcConst.NPC_FUNC_MEMBER_RANK_AWARD)
def NPC_FUNC_MEMBER_RANK_AWARD(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.openAwardPanel(functype, entId)


@funcMap(npcConst.NPC_FUNC_FRIEND)
def NPC_FUNC_FRIEND(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    onFuncState()
    npc.cell.openActivateOldFriend()


@funcMap(npcConst.NPC_FUNC_ACTIVE_OLD_FRIEND)
def NPC_FUNC_ACTIVE_OLD_FRIEND(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    onFuncState()
    npc.cell.activateOldFriend()


@funcMap(npcConst.NPC_FUNC_INACTIVE_OLD_FRIEND)
def NPC_FUNC_INACTIVE_OLD_FRIEND(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    onFuncState()


@funcMap(npcConst.NPC_FUNC_RANK)
def NPC_FUNC_RANK(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    onFuncState()
    lvRequire = SCD.data.get('RankListLv', 70)
    p = BigWorld.player()
    if lvRequire > p.lv:
        p.showGameMsg(GMDD.data.OPEN_RANK_LV_LOW, lvRequire)
        return
    gameglobal.rds.ui.funcNpc.openDirectly(entId, npc.npcId, npcConst.NPC_FUNC_RANK)
    gameglobal.rds.ui.ranking.show(const.PROXY_KEY_TOP_COMBAT_SCORE, uiConst.RANK_TYPE_EQUIP_LV)


@funcMap(npcConst.NPC_FUNC_DYE)
def NPC_FUNC_DYE(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.dyePlane.show(entId)
    if not gameglobal.rds.configData.get('enableWardrobe', False):
        gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_HUAZHUANG)
def NPC_FUNC_HUAZHUANG(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.huazhuang.show(entId)


@funcMap(npcConst.NPC_FUNC_REPAIR_SHIHUN)
def NPC_FUNC_REPAIR_SHIHUN(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_SOCIAL_SCHOOL_REJOIN)
def NPC_FUNC_SOCIAL_SCHOOL_REJOIN(functype, callType, entId, chatItem, extraParams = None):
    close()
    BigWorld.player().rejoinSocSchool(chatItem[2])


@funcMap(npcConst.NPC_FUNC_QINGGONGJINSU)
def NPC_FUNC_QINGGONGJINSU(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.qingGongJingSu.showResult()


@funcMap(npcConst.NPC_FUNC_GUILD_GROWTH)
def NPC_FUNC_GUILD_GROWTH(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.guildGrowth.show(0, isNPCFlag=True, needChange=False)


@funcMap(npcConst.NPC_FUNC_YIXIN_BIND)
def NPC_FUNC_YIXIN_BIND(functype, callType, entId, chatItem, extraParams = None):
    isShowYixin = gameglobal.rds.configData.get('enableYixin', False)
    if not isShowYixin:
        BigWorld.player().showGameMsg(GMDD.data.YIXIN_FUNC_CLOSE, ())
        close()
        return
    if not BigWorld.player().yixinOpenId:
        gameglobal.rds.ui.yixinBind.show()
    else:
        gameglobal.rds.ui.yixinRewards.show()


@funcMap(npcConst.NPC_FUNC_YIXIN_UNBIND)
def NPC_FUNC_YIXIN_UNBIND(functype, callType, entId, chatItem, extraParams = None):
    isShowYixin = gameglobal.rds.configData.get('enableYixin', False)
    if not isShowYixin:
        BigWorld.player().showGameMsg(GMDD.data.YIXIN_FUNC_CLOSE, ())
        close()
        return
    if BigWorld.player().yixinOpenId:
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_NPCFUNCMAPPINGS_764, gameglobal.rds.ui.funcNpc.unBindYixin, gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, gameglobal.rds.ui.funcNpc.cancelUnBindYixin)
    else:
        close()
        gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_NPCFUNCMAPPINGS_767)


@funcMap(npcConst.NPC_FUNC_HUAZHUANG_PLUS)
def NPC_FUNC_HUAZHUANG_PLUS(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.huazhuangPlus.show(entId)


@funcMap(npcConst.NPC_FUNC_FUBEN_DIFFICULTY_ADJUST)
def NPC_FUNC_FUBEN_DIFFICULTY_ADJUST(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.openDifficultyPanel(functype, entId)


@funcMap(npcConst.NPC_FUNC_PURCHASE_SHOP)
def NPC_FUNC_PURCHASE_SHOP(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    gameglobal.rds.ui.purchaseShop.show(entId)
    npc.cell.openPurchaseShop()


@funcMap(npcConst.NPC_FUNC_RECAST_ITEM)
def NPC_FUNC_RECAST_ITEM(functype, callType, entId, chatItem, extraParams = None):
    index = extraParams.get('index', 0)
    npc = BigWorld.entities.get(entId)
    gameglobal.rds.ui.itemRecast.show(npc, index)
    gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_LIBERATE)
def NPC_FUNC_LIBERATE(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    npc.cell.npcLiberate(0)


@funcMap(npcConst.NPC_FUNC_QUERY_PLAYER_LOCATION)
def NPC_FUNC_QUERY_PLAYER_LOCATION(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    gameglobal.rds.ui.queryLocation.show(npc)


@funcMap(npcConst.NPC_FUNC_SHOW_SUI_XING_YU_RESULT)
def NPC_FUNC_SHOW_SUI_XING_YU_RESULT(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.suiXingYu.showGuildRank()


@funcMap(npcConst.NPC_FUNC_GET_EXP_BONUS)
def NPC_FUNC_GET_EXP_BONUS(functype, callType, entId, chatItem, extraParams = None):
    funcId = chatItem[2]
    gameglobal.rds.ui.expBonus.show(entId, funcId)


@funcMap(npcConst.NPC_FUNC_CBG)
def NPC_FUNC_CBG(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.cbgMain.show(entId)


@funcMap(npcConst.NPC_FUNC_WORLD_CHALLENGE)
def NPC_FUNC_WORLD_CHALLENGE(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    funcId = chatItem[2]
    gameglobal.rds.ui.challenge.show(entId, funcId)


@funcMap(npcConst.NPC_FUNC_YUNCHUIJI)
def NPC_FUNC_YUNCHUIJI(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.yunchuiji.show()


@funcMap(npcConst.NPC_FUNC_FREEZE_EXP_BONUS)
def NPC_FUNC_FREEZE_EXP_BONUS(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.expBonus.freezeOrUnFreezeBonus(entId)


@funcMap(npcConst.NPC_FUNC_PAY_BAIL)
def NPC_FUNC_PAY_BAIL(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    gameglobal.rds.ui.isolate.show(npc)


@funcMap(npcConst.NPC_FUNC_STORAGE)
def NPC_FUNC_STORAGE(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    if p:
        p.openStorage(entId)


@funcMap(npcConst.NPC_FUNC_ITEM_REDEMPTION)
def NPC_FUNC_ITEM_REDEMPTION(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.equipRedemption.npcId = entId
    gameglobal.rds.ui.equipRedemption.requetsData()


@funcMap(npcConst.NPC_FUNC_FUNBEN_RANK)
def NPC_FUNC_FUNBEN_RANK(functype, callType, entId, chatItem, extraParams = None):
    if gameglobal.rds.ui.ranking.mediator:
        gameglobal.rds.ui.ranking.hide()
    onFuncState()
    fubenNo = chatItem[2]
    gameglobal.rds.ui.ranking.show(const.PROXY_KEY_TOP_FB_TIME, fbNo=fubenNo)


@funcMap(npcConst.NPC_FUNC_WMD_KILL_RANK)
def NPC_FUNC_WMD_KILL_RANK(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.wmdRankList.openKillRank()


@funcMap(npcConst.NPC_FUNC_WMD_SHANGJIN_RANK)
def NPC_FUNC_WMD_SHANGJIN_RANK(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.wmdRankList.openShangjinRank()


@funcMap(npcConst.NPC_FUNC_YCWZ_RANK)
def NPC_FUNC_YCWZ_RANK(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.ycwzRankList.show()


@funcMap((npcConst.NPC_FUNC_FREE_CHAT_BY_BAIL, npcConst.NPC_FUNC_FREE_CHAT_BY_CASH, npcConst.NPC_FUNC_CLEAN_CHAT_BLOCK_FREQUENCY))
def NPC_FUNC_FREE_CHAT_BY_BAIL(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.onDefaultState()
    gameglobal.rds.ui.isolate.showFreeChatMsg(functype, entId)


@funcMap(npcConst.NPC_FUNC_RECYCLE_ITEM)
def NPC_FUNC_RECYCLE_ITEM(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    funcId = chatItem[2]
    gameglobal.rds.ui.itemRecall.show(entId, funcId)
    gameglobal.rds.ui.inventory.show()


@funcMap(npcConst.NPC_FUNC_FREE_FB_PUNISH_BY_BAIL)
def NPC_FUNC_FREE_FB_PUNISH_BY_BAIL(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.isolate.showFreeFbPunish(entId)


@funcMap(npcConst.NPC_FUNC_DYE_RESET)
def NPC_FUNC_DYE_RESET(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.dyeReset.show()


@funcMap(npcConst.NPC_FUNC_GUILD_SALARY_ASSIGN)
def NPC_FUNC_GUILD_SALARY_ASSIGN(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.guildSalaryAssign.show()


@funcMap(npcConst.NPC_FUNC_GUILD_SALARY_RECEIVE)
def NPC_FUNC_GUILD_SALARY_RECEIVE(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.guildSalaryReceive.show()


@funcMap(npcConst.NPC_FUNC_GUILD_LUXURY_RANK)
def NPC_FUNC_GUILD_LUXURY_RANK(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.guildLuxuryRank.show()


@funcMap(npcConst.NPC_FUNC_GUILD_SALARY_HISTORY)
def NPC_FUNC_GUILD_SALARY_HISTORY(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.guildSalaryHistory.show()


@funcMap(npcConst.NPC_FUNC_SAVE_AVATARCONFIG)
def NPC_FUNC_SAVE_AVATARCONFIG(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.characterDetailAdjust.onSaveNpcConfig()


@funcMap(npcConst.NPC_FUNC_USER_ACCOUNT_BIND)
def NPC_FUNC_USER_ACCOUNT_BIND(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    if gameglobal.rds.configData.get('enableBindReward', False):
        gameglobal.rds.ui.accountBind.show()
    else:
        gameglobal.rds.ui.userAccountBind.show()


@funcMap(npcConst.NPC_FUNC_MIGRATE)
def NPC_FUNC_MIGRATE(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entity(entId)
    if npc and npc.inWorld:
        gameglobal.rds.ui.migrateServer.npcId = entId
        npc.cell.useMigrate('')


@funcMap(npcConst.NPC_FUNC_BUSINESS)
def NPC_FUNC_BUSINESS(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entity(entId)
    gameglobal.rds.ui.funcNpc.openDirectly(entId, npc.npcId, npcConst.NPC_FUNC_BUSINESS)
    gameglobal.rds.ui.guildBusinessShop.show(entId)


@funcMap(npcConst.NPC_FUNC_BUSINESS_SPY)
def NPC_FUNC_BUSINESS_SPY(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.funcNpc.openBusinessSpyPanel(entId)


@funcMap(npcConst.NPC_FUNC_BUSINESS_BLACK)
def NPC_FUNC_BUSINESS_BLACK(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entity(entId)
    gameglobal.rds.ui.funcNpc.openDirectly(entId, npc.npcId, npcConst.NPC_FUNC_BUSINESS_BLACK)
    gameglobal.rds.ui.guildContraband.show(entId)


@funcMap(npcConst.NPC_FUNC_DGT_BUSINESS)
def NPC_FUNC_DGT_BUSINESS(functype, callType, entId, chatItem, extraParams = None):
    op = chatItem[2]
    if op == gametypes.BUSINESS_NPC_OPTION_ABANDON:
        close()
    else:
        onFuncState()
    gameglobal.rds.ui.guildBusinessDelegate.needShow(entId, op)


@funcMap(npcConst.NPC_FUNC_FLOWBACK_REWARD)
def NPC_FUNC_FLOWBACK_REWARD(functype, callType, entId, chatItem, extraParams = None):
    BigWorld.player().base.applyBackflowReward()
    close()


@funcMap(npcConst.NPC_FUNC_SUMMON_PLANE_IN_FORT_BATTLE_FIELD)
def NPC_FUNC_SUMMON_PLANE_IN_FORT_BATTLE_FIELD(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entity(entId)
    close()
    npc.cell.summonPlaneInFortBattleField()


@funcMap(npcConst.NPC_FUNC_BACKFLOW_VP)
def NPC_FUNC_BACKFLOW_VP(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.xiuYingExpGet.show(entId)


@funcMap(npcConst.NPC_FUNC_ACTIVITY_RESET_CHAR)
def NPC_FUNC_ACTIVITY_RESET_CHAR(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entity(entId)
    close()
    funcId = chatItem[2]
    gameglobal.rds.ui.npcPanel.showResetCharConfirm(entId, funcId)


@funcMap(npcConst.NPC_FUNC_APPLY_UNDISTURB)
def NPC_FUNC_APPLY_UNDISTURB(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entity(entId)
    close()
    npc.cell.applyUndisturb()


@funcMap(npcConst.NPC_FUNC_GUANYIN_REPAIR)
def NPC_FUNC_GUANYIN_REPAIR(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.huiZhangRepair.show()
    gameglobal.rds.ui.inventory.show()


@funcMap(npcConst.NPC_FUNC_PUZZLE)
def NPC_FUNC_PUZZLE(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entity(entId)
    close()
    puzzleNpcType = gameglobal.rds.ui.puzzle.npcType(npc.npcId)
    gamelog.debug('cgy#puzzleNpcType: ', puzzleNpcType)
    if puzzleNpcType == const.PUZZLE_NPC_WORLD:
        gameglobal.rds.ui.puzzle.npcId = npc.npcId
        npc.cell.acceptNpcPuzzle()
    elif puzzleNpcType in const.PUZZLE_NPC_KEJU:
        gameglobal.rds.ui.puzzle.showKeJuPanel(gameglobal.rds.ui.funcNpc._getNpcName(), npc.npcId, entId)
    elif puzzleNpcType == const.PUZZLE_NPC_TRIGGER:
        gameglobal.rds.ui.puzzle.npcId = npc.npcId
        npc.cell.acceptNpcPuzzleTrigger()
    elif puzzleNpcType == const.PUZZLE_NPC_PAIR:
        npc.cell.acceptNpcPairPuzzle()


@funcMap(npcConst.NPC_FUNC_FROZEN_PUNISH)
def NPC_FUNC_FROZEN_PUNISH(functype, callType, entId, chatItem, extraParams = None):
    punishType = chatItem[2]
    if punishType == uiConst.FROZEN_PUNISH_NORMAL:
        onFuncState()
        gameglobal.rds.ui.frozenPunish.show()
    elif punishType == uiConst.FROZEN_PUNISH_CBG:
        close()
        BigWorld.openUrl('http://tianyu.cbg.163.com')
    elif punishType == uiConst.FROZEN_PUNISH_MALL:
        close()
        gameglobal.rds.ui.tianyuMall.showMallTab(10000, 1)


@funcMap(npcConst.NPC_FUNC_COLLECT_ITEM)
def NPC_FUNC_COLLECT_ITEM(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    actId, bookType = chatItem[2]
    gameglobal.rds.ui.xinmoBook.queryInfo(actId, bookType)


@funcMap(npcConst.NPC_FUNC_YAOPEI_MIX)
def NPC_FUNC_YAOPEI_MIX(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.yaoPeiMix.show()
    gameglobal.rds.ui.inventory.show()


@funcMap(npcConst.NPC_FUNC_YAOPEI_TRANSFER)
def NPC_FUNC_YAOPEI_TRANSFER(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.yaoPeiTransfer.show()
    gameglobal.rds.ui.inventory.show()


@funcMap(npcConst.NPC_FUNC_YAOPEI_REFORGE)
def NPC_FUNC_YAOPEI_REFORGE(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.yaoPeiReforge.show()
    gameglobal.rds.ui.inventory.show()


@funcMap(npcConst.NPC_FUNC_PINGJIU)
def NPC_FUNC_PINGJIU(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entity(entId)
    close()
    npc.cell.pingjiu()


@funcMap(npcConst.NPC_FUNC_LOTTERY)
def NPC_FUNC_LOTTERY(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.lottery.show(chatItem[2])
    gameglobal.rds.ui.inventory.show()


@funcMap(npcConst.NPC_FUNC_FUBEN_AWARD_TIMES)
def NPC_FUNC_FUBEN_AWARD_TIMES(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.fubenAwardTimes.show(chatItem[2])


@funcMap(npcConst.NPC_FUNC_YABIAO)
def NPC_FUNC_YABIAO(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entity(entId)
    onFuncState()
    yabiaoType = chatItem[2]
    gameglobal.rds.ui.funcNpc.uiAdapter.yaBiao.onTriggerNpc(npc.id, npc.npcId, yabiaoType)


@funcMap(npcConst.NPC_FUNC_FAME_CASH_EXCHANGE)
def NPC_FUNC_FAME_CASH_EXCHANGE(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    fameId = chatItem[2]
    gameglobal.rds.ui.funcNpc.uiAdapter.fameCashExchange.show(entId, fameId)


@funcMap(npcConst.NPC_FUNC_METERIAL_BAG)
def NPC_FUNC_METERIAL_BAG(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.funcNpc.uiAdapter.inventory.show()
    if gameglobal.rds.configData.get('enableNewMaterialBag', False):
        gameglobal.rds.ui.funcNpc.uiAdapter.meterialBag.show()
    else:
        gameglobal.rds.ui.funcNpc.uiAdapter.inventory.openTempBagByType('meterial')


@funcMap(npcConst.NPC_FUNC_TUZHUANG)
def NPC_FUNC_TUZHUANG(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.funcNpc.uiAdapter.tuZhuang.show()


@funcMap(npcConst.NPC_FUNC_WISH_MADE)
def NPC_FUNC_WISH_MADE(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.funcNpc.uiAdapter.inventory.show()
    gameglobal.rds.ui.funcNpc.uiAdapter.wishMade.show()


@funcMap(npcConst.NPC_FUNC_WISH_VIEW)
def NPC_FUNC_WISH_VIEW(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.funcNpc.setDarkBg(True)
    gameglobal.rds.ui.funcNpc.uiAdapter.wishMadeView.show()


@funcMap(npcConst.NPC_FUNC_ITEM_COMMIT)
def NPC_FUNC_ITEM_COMMIT(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entity(entId)
    close()
    gameglobal.rds.ui.funcNpc.uiAdapter.worldWar.showWWItemCommitView(npc, chatItem[2])


@funcMap(npcConst.NPC_FUNC_ZHENYAO_RANK_LIST)
def NPC_FUNC_ZHENYAO_RANK_LIST(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.funcNpc.uiAdapter.zhenyao.showRankList()


@funcMap(npcConst.NPC_FUNC_GLOBAL_RANDOM_CHALLENGE)
def NPC_FUNC_GLOBAL_RANDOM_CHALLENGE(functype, callType, entId, chatItem, extraParams = None):
    challengeId = chatItem[2]
    npc = BigWorld.entities.get(entId)
    npc.cell.applyRandomChallenge(challengeId)


@funcMap(npcConst.NPC_FUNC_WINGWORLD_RANDOM_FUBEN)
def NPC_FUNC_WINGWORLD_RANDOM_FUBEN(functype, callType, entId, chatItem, extraParams = None):
    key = chatItem[2]
    npc = BigWorld.entities.get(entId)
    if npc:
        npc.cell.applyRandomFuben(key)


@funcMap(npcConst.NPC_FUNC_MAKE_MANUAL_EQUIP)
def NPC_FUNC_MAKE_MANUAL_EQUIP(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.manualEquip.show(entId)


@funcMap(npcConst.NPC_FUNC_SHAXING_SIGNUP)
def NPC_FUNC_SHAXING_SIGNUP(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    npc.cell.applyShaxingSignup()
    close()


@funcMap(npcConst.NPC_FUNC_SHAXING_OBSERVE)
def NPC_FUNC_SHAXING_OBSERVE(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    npc.cell.applyShaxingObserve()
    close()


@funcMap(npcConst.NPC_FUNC_HOME_ENTRANCE)
def NPC_FUNC_HOME_ENTRANCE(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    npc.cell.openHomeEntrance()
    close()


@funcMap(npcConst.NPC_FUNC_HOME_BUY)
def NPC_FUNC_HOME_BUY(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    p.openBuyHouse()


@funcMap(npcConst.NPC_FUNC_HOME_GOTO_MYFLOOR)
def NPC_FUNC_HOME_GOTO_MYFLOOR(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    p.cell.enterFloor(p.myHome.floorNo)


@funcMap(npcConst.NPC_FUNC_HOME_SELECT_FLOOR)
def NPC_FUNC_HOME_SELECT_FLOOR(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    p.openSendToFloor()


@funcMap(npcConst.NPC_FUNC_HOME_CHECK_INFO)
def NPC_FUNC_HOME_CHECK_INFO(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    p.openCheckHouse()


@funcMap(npcConst.NPC_FUNC_SHARE_CHAR_CONF)
def NPC_FUNC_SHARE_CHAR_CONF(functype, callType, entId, chatItem, extraParams = None):
    BigWorld.player().uploadCharacter(entId)


@funcMap(npcConst.NPC_FUNC_HOME_EXTENSION)
def NPC_FUNC_HOME_EXTENSION(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    p.confirmExpendRoom()


@funcMap(npcConst.NPC_FUNC_HOME_FLOOR)
def NPC_FUNC_HOME_FLOOR(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    p.cell.leaveFloor()


@funcMap(npcConst.NPC_FUNC_HOME_REMOVE_ROOM)
def NPC_FUNC_HOME_REMOVE_ROOM(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    p.confirmRemoveRoom()


@funcMap(npcConst.NPC_FUNC_HOME_MODEL_ROOM)
def NPC_FUNC_HOME_MODEL_ROOM(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    p.cell.enterFloor(const.HOME_MODEL_ROOM_FLOOR_NO)


@funcMap(npcConst.NPC_FUNC_IMPEACH_START)
def NPC_FUNC_IMPEACH_START(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.onDefaultState()
    p = BigWorld.player()
    p.cell.queryWWArmyImpeach(gametypes.WW_ARMY_IMPEACH_QUERY_NPC)


@funcMap(npcConst.NPC_FUNC_SCHOOL_TRANSFER)
def NPC_FUNC_SCHOOL_TRANSFER(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.schoolTransferSelect.show(const.SCHOOL_DEFAULT, False)


@funcMap(npcConst.NPC_FUNC_SCHOOL_TRANSFER_LOW_LEVEL)
def NPC_FUNC_SCHOOL_TRANSFER_LOW_LEVEL(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.schoolTransferSelect.show(const.SCHOOL_DEFAULT, True)


@funcMap(npcConst.NPC_FUNC_SCHOOL_TRANSFER_EQUIP)
def NPC_FUNC_SCHOOL_TRANSFER_EQUIP(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.schoolTransferEquip.show(chatItem[2])


@funcMap(npcConst.NPC_FUNC_COMPLETE_WORLD_WAR_ROB)
def NPC_FUNC_COMPLETE_WORLD_WAR_ROB(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    npc.cell.completeWorldWarRob()


@funcMap((npcConst.NPC_FUNC_APPRENTICE_GROWTH_LEVEL_REWARD_APPLY, npcConst.NPC_FUNC_APPRENTICE_GROWTH_GRADUATE_REWARD_APPLY))
def NPC_FUNC_APPRENTICE_GROWTH_LEVEL_REWARD_APPLY(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    gameglobal.rds.ui.funcNpc.uiAdapter.mentorEx.apprenticeGrowthLevelRewardApply(npc, functype)


@funcMap(npcConst.NPC_FUNC_APPRENTICE_GROWTH_REWARDED_QUERY)
def NPC_FUNC_APPRENTICE_GROWTH_REWARDED_QUERY(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    npc.cell.apprenticeGrowthRewardQuery()


@funcMap(npcConst.NPC_FUNC_DEEP_PEEK)
def NPC_FUNC_DEEP_PEEK(functype, callType, entId, chatItem, extraParams = None):
    close()
    npc = BigWorld.entities.get(entId)
    gamelog.debug('@lhb funNpc ', chatItem[2])
    npc and npc.cell.applyGMDeepPeek(chatItem[2][0], chatItem[2][1])


@funcMap(npcConst.NPC_FUNC_ONEKEY_CREATE_TEAM)
def NPC_FUNC_ONEKEY_CREATE_TEAM(functype, callType, entId, chatItem, extraParams = None):
    close()
    p = BigWorld.player()
    op = chatItem[2]
    p.oneKeyCreateTeamByGoal(op)


@funcMap(npcConst.NPC_FUNC_START_WORLD_WAR_ROB)
def NPC_FUNC_START_WORLD_WAR_ROB(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    if not gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
        p = BigWorld.player()
        p.startRob(npc)


@funcMap(npcConst.NPC_FUNC_CHECK_TEAM)
def NPC_FUNC_CHECK_TEAM(functype, callType, entId, chatItem, extraParams = None):
    close()
    labelId = chatItem[2]
    if uiUtils.checkLevelAndTime(labelId):
        gameglobal.rds.ui.team.openTeamWithType(labelId)


@funcMap(npcConst.NPC_FUNC_RESERVE_BUY)
def NPC_FUNC_RESERVE_BUY(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.hobbyPreSaleRule.show()


@funcMap(npcConst.NPC_FUNC_RESERVE_CODE_CHECK)
def NPC_FUNC_RESERVE_CODE_CHECK(functype, callType, entId, chatItem, extraParams = None):
    close()
    p = BigWorld.player()
    opType = 2
    p.base.queryExternalMallData(opType, '')


@funcMap(npcConst.NPC_FUNC_OPEN_WEBLINK)
def NPC_FUNC_OPEN_WEBLINK(functype, callType, entId, chatItem, extraParams = None):
    close()
    urlId = chatItem[2]
    url = ''
    if urlId == uiConst.VIEW_GIFT_LINK:
        url = HPCD.data.get('queryLink', '')
    elif urlId == uiConst.BUY_GIFR_LINK:
        url = HPCD.data.get('buyLink', '')
    BigWorld.openUrl(url)


@funcMap(npcConst.NPC_FUNC_GER_RESERVE_DEPOSIT)
def NPC_FUNC_GER_RESERVE_DEPOSIT(functype, callType, entId, chatItem, extraParams = None):
    close()
    p = BigWorld.player()
    opType = 3
    p.base.queryExternalMallData(opType, '')


@funcMap(npcConst.NOC_FUNC_OPEN_VOID_DREAMLAND)
def NOC_FUNC_OPEN_VOID_DREAMLAND(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.voidDreamland.show()


@funcMap(npcConst.NPC_FUNC_QUEST_LEARN)
def NPC_FUNC_QUEST_LEARN(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    close()
    p = BigWorld.player()
    questId = chatItem[2]
    if questId:
        p.cell.npcQuestQiecuo(questId, npc.npcId)


@funcMap(npcConst.NPC_FUNC_QUEST_DIALOG)
def NPC_FUNC_QUEST_DIALOG(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    npc = BigWorld.entities.get(entId)
    questId = chatItem[2]
    needDialog = QD.data.get(questId, {}).get('needDialog', ())
    needDialogGroup = QD.data.get(questId, {}).get('needDialogGroup', ())
    needDialogList = None
    if needDialogGroup:
        dialogGroupId, _ = needDialogGroup
        needDialogList = QNGD.data.get(dialogGroupId, {}).get('npcList', ())
    if npc.npcId in needDialog or needDialogList:
        drd = DRD.data.get(npc.npcId, {})
        if drd.has_key('quests') and questId in p.quests and p.questData.has_key(questId):
            quests = drd.get('quests', [])
            index = quests.index(questId)
            chatIds = [drd['chatIds'][index]]
        else:
            chatIds = drd.get('defaultChatId', [])
        if chatIds:
            chatId = chatIds[0]
            if chatId in GD.data:
                gameglobal.rds.ui.multiNpcChat.openMultiNpcChatWindow(npc.id, npc.npcId, chatIds, True)
            else:
                p.showChatWindow(chatId, npc.id, Functor(npc.onChatChoice, chatId))


@funcMap(npcConst.NPC_FUNC_QUEST_DEBATE)
def NPC_FUNC_QUEST_DEBATE(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    questId = chatItem[2]
    debateChatId = QD.data.get(questId, {}).get('debateChatId', 0)
    if debateChatId:
        gameglobal.rds.ui.debate.openDebatePanel(npc.npcId, entId, debateChatId)


@funcMap(npcConst.NPC_FUNC_QUEST_PUZZLE)
def NPC_FUNC_QUEST_PUZZLE(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    questId = chatItem[2]
    if questId:
        p.puzzleQuestUI(questId)


@funcMap(npcConst.NPC_FUNC_REAL_NAME_REWARD)
def NPC_FUNC_REAL_NAME_REWARD(functype, callType, entId, chatItem, extraParams = None):
    close()
    BigWorld.player().base.applyRealNameReward()


@funcMap(npcConst.NPC_FUNC_SCHOOL_ENTRUST)
def NPC_FUNC_SCHOOL_ENTRUST(functype, callType, entId, chatItem, extraParams = None):
    schoolType = chatItem[2]
    p = BigWorld.player()
    if schoolType == BigWorld.player().school:
        gameglobal.rds.ui.schoolEntrust.openSchoolEntrust()
    else:
        p.showGameMsg(GMDD.data.SCHOOL_ENTRUST_SCHOOL_LIMIT)


@funcMap(npcConst.NPC_FUNC_BUILD_PARTNER)
def NPC_FUNC_BUILD_PARTNER(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    BigWorld.player().cell.applyBuildPartner(npc.id)
    gameglobal.rds.ui.funcNpc.onDefaultState()


@funcMap(npcConst.NPC_FUNC_ADD_PARTNER)
def NPC_FUNC_ADD_PARTNER(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    BigWorld.player().cell.applyAddPartner(npc.id)
    gameglobal.rds.ui.funcNpc.onDefaultState()


@funcMap(npcConst.NPC_FUNC_KICKOUT_PARTNER)
def NPC_FUNC_KICKOUT_PARTNER(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    BigWorld.player().cell.applyKickoutPartner(npc.id)
    gameglobal.rds.ui.funcNpc.onDefaultState()


@funcMap(npcConst.NPC_FUNC_EXIT_PARTNER)
def NPC_FUNC_EXIT_PARTNER(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    BigWorld.player().cell.applyExitPartner(npc.id)
    gameglobal.rds.ui.funcNpc.onDefaultState()


@funcMap(npcConst.NPC_FUNC_PERSONAL_SPACE)
def NPC_FUNC_PERSONAL_SPACE(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    gameglobal.rds.ui.funcNpc.close()
    statueOwnerHostId = getattr(npc, 'statueOwnerHostId', 0)
    currentHostId = RSND.data.get(statueOwnerHostId, {}).get('currentHostId', 0)
    if currentHostId:
        statueOwnerHostId = currentHostId
    p = BigWorld.player()
    p.getPersonalSysProxy().openZoneOther(getattr(npc, 'statueOwnerGbId', 0), hostId=statueOwnerHostId)


@funcMap(npcConst.NPC_FUNC_FASHION_EXHANGE)
def NPC_FUNC_FASHION_EXHANGE(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    onFuncState()
    gameglobal.rds.ui.funcNpc.openDirectly(entId, npc.npcId, npcConst.NPC_FUNC_FASHION_EXHANGE)
    gameglobal.rds.ui.itemMsgBox.showExtend(uiConst.ITEM_MSG_BOX_EXTEND_FASHION)
    gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_GM_AWARD)
def NPC_FUNC_GM_AWARD(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.openAwardPanel(functype, entId)


@funcMap(npcConst.NPC_FUNC_TEAM_INVITE)
def NPC_FUNC_TEAM_INVITE(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    p.chatNpcInviteTeam(const.CHAT_INVITE_TEAM_FOR_XUNLING)


@funcMap(npcConst.NPC_FUNC_TEAM_INVITE_FOR_YOULI)
def NPC_FUNC_TEAM_INVITE_FOR_YOULI(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    p.chatNpcInviteTeam(const.CHAT_INVITE_TEAM_FOR_YOULI)


@funcMap(npcConst.NPC_FUNC_NEW_PLAYER_PARTNER_REWARD)
def NPC_FUNC_NEW_PLAYER_PARTNER_REWARD(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    p.chatNpcNewPlayerReward()
    close()


@funcMap(npcConst.NPC_FUNC_NEW_PLAYER_TREASURE_BOX)
def NPC_FUNC_NEW_PLAYER_TREASURE_BOX(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    p.chatNpcCreateTreasureBox()
    close()


@funcMap(npcConst.NPC_FUNC_MASS_ASTROLOGY)
def NPC_FUNC_MASS_ASTROLOGY(functype, callType, entId, chatItem, extraParams = None):
    if gameglobal.rds.configData.get('enableGuildMassAstrology', False):
        gameglobal.rds.ui.guildIdentifyStar.show()
    else:
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.GUILD_MASS_ASTROLOGY_CLOSED, ())
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()


@funcMap(npcConst.NPC_FUMC_CELEBRITY_STATUE)
def NPC_FUMC_CELEBRITY_STATUE(functype, callType, entId, chatItem, extraParams = None):
    close()
    topType = chatItem[2]
    if topType:
        gameglobal.rds.ui.famerRankHistory.show(topType)


@funcMap((npcConst.NPC_FUMC_TREASURE_BOX_WISH_NORMAL, npcConst.NPC_FUMC_TREASURE_BOX_WISH_CBT, npcConst.NPC_FUMC_TREASURE_BOX_WISH_RAFFLE))
def NPC_FUMC_TREASURE_BOX_WISH_NORMAL(functype, callType, entId, chatItem, extraParams = None):
    close()
    wishBoxId = chatItem[2]
    gameglobal.rds.ui.treasureBoxWish.show(wishBoxId)


@funcMap(npcConst.NPC_FUNC_OPEN_DYNAMIC_SHOP)
def NPC_FUNC_OPEN_DYNAMIC_SHOP(functype, callType, entId, chatItem, extraParams = None):
    shopId = chatItem[2]
    gameglobal.rds.ui.selfAdaptionShop.openShop(shopId)


@funcMap(npcConst.NPC_FUNC_TORCH_LIGHT)
def NPC_FUNC_TORCH_LIGHT(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    p = BigWorld.player()
    if not getattr(p, 'guild', None):
        return
    else:
        if getattr(npc, 'torchIdx', 0) and npc.torchIdx and p.guild.bonfire.torch.get(npc.torchIdx, False):
            close()
            gameglobal.rds.ui.funcNpc.uiAdapter.guildBonfire.lightBonfire(npc.torchIdx)
        return


@funcMap(npcConst.NPC_FUNC_MYSTERY_ANIMAL)
def NPC_FUNC_MYSTERY_ANIMAL(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.mysteryAnimal.show()


@funcMap(npcConst.NPC_FUNC_WINGWORLD_OPENDOOR)
def NPC_FUNC_WINGWORLD_OPENDOOR(functype, callType, entId, chatItem, extraParams = None):
    close()
    if not gameglobal.rds.configData.get('enableWingWorldOpenDoor', False):
        BigWorld.player().showGameMsg(GMDD.data.WINGWORLD_OPENDOOR_NOTOPEN, ())
        return
    if not gameglobal.rds.ui.wingWorldRemoveSeal.checkWingWorldRemoveMileStone('open'):
        return
    sType = chatItem[2]
    if sType == uiConst.NPC_REMOVESEAL_OPTION:
        gameglobal.rds.ui.funcNpc.openDirectly(entId, gameglobal.rds.ui.funcNpc.npcId, npcConst.NPC_FUNC_WINGWORLD_OPENDOOR)
        gameglobal.rds.ui.wingWorldRemoveSeal.show()
    elif sType == uiConst.NPC_BOSSDAMAGE_RANK_OPTION:
        gameglobal.rds.ui.bossDamageRank.show()
    elif sType == uiConst.NPC_REMOVESEAL_RANK_OPTION:
        gameglobal.rds.ui.removeSealRank.show()


@funcMap(npcConst.NPC_FUNC_FREE_LOTTERY)
def NPC_FUNC_FREE_LOTTERY(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.freeLottery.show()


@funcMap(npcConst.NPC_FUNC_SPRITE_MATERIAL_BAG)
def NPC_FUNC_SPRITE_MATERIAL_BAG(functype, callType, entId, chatItem, extraParams = None):
    onFuncState()
    gameglobal.rds.ui.spriteMaterialBag.show()
    gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_GUILD_MERGE_STRT)
def NPC_FUNC_GUILD_MERGE_STRT(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.guildMergeStart.show()


@funcMap(npcConst.NPC_FUNC_GUILD_MERGE_CONFIRM)
def NPC_FUNC_GUILD_MERGE_CONFIRM(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    p = BigWorld.player()
    if p.guild:
        text = GMD.data.get(GMDD.data.GUILD_MERGE_PREPARE_CONFIM, {}).get('text', '%s,%s') % p.guild.guildMergerVal.guildNames[::-1]
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(text, Functor(p.cell.applyComfirmGuildMerger, npc.id))


@funcMap(npcConst.NPC_FUNC_GUILD_MERGE_CANCEL)
def NPC_FUNC_GUILD_MERGE_CANCEL(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    npc = BigWorld.entities.get(entId)
    text = GMD.data.get(GMDD.data.GUILD_MERGE_CANCEL_CONFIRM, {}).get('text', '')
    gameglobal.rds.ui.messageBox.showYesNoMsgBox(text, Functor(p.cell.applyAbandonGuildMerger, npc.id))


@funcMap(npcConst.NPC_FUNC_GUILD_CHANGE_NAME)
def NPC_FUNC_GUILD_CHANGE_NAME(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.uiAdapter.guildChangeName.show()


@funcMap(npcConst.NPC_FUNC_WW_YABIAO_START)
def NPC_FUNC_WW_YABIAO_START(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    gamelog.info('jbx:yabiao start')
    close()
    p.cell.queryWingWorldGuildResourceForYabiao()


@funcMap(npcConst.NPC_FUNC_WW_YABIAO_END)
def NPC_FUNC_WW_YABIAO_END(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    p = BigWorld.player()
    gamelog.info('jbx:applyCompleteWingWorldYabiao')
    p.cell.applyCompleteWingWorldYabiao(npc.id)
    close()


@funcMap(npcConst.NPC_FUNC_WW_YABIAO_DAKA)
def NPC_FUNC_WW_YABIAO_DAKA(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    p = BigWorld.player()
    gamelog.info('jbx:yabiao applyWingWorldYabiaoDaKa', npc.id)
    p.cell.applyWingWorldYabiaoDaKa(npc.id)
    close()


@funcMap(npcConst.NPC_FUNC_WW_YABIAO_SIHUO)
def NPC_FUNC_WW_YABIAO_SIHUO(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    gamelog.info('jbx:yabiao sihuo')
    close()
    if not hasattr(p, 'wingWorldYabiaoData'):
        p.showGameMsg(GMDD.data.NOT_IN_YABIAO_STATE, ())
        return
    gameglobal.rds.ui.funcNpc.uiAdapter.wingWorldYaBiaoSiHuo.show()


@funcMap(npcConst.NPC_FUNC_SCHOOL_TOP_TEST)
def NPC_FUNC_SCHOOL_TOP_TEST(functype, callType, entId, chatItem, extraParams = None):
    close()
    p = BigWorld.player()
    if not gameglobal.rds.ui.funcNpc.uiAdapter.messageBox.checkOnceMap.get(uiConst.CHECK_ONCE_TYPE_SCHOOL_TOP_TEST, False):
        text = GMD.data.get(GMDD.data.SCHOOL_TOP_TEST_CONFIRM, {}).get('text', '')
        gameglobal.rds.ui.funcNpc.uiAdapter.messageBox.showYesNoMsgBox(text, gameglobal.rds.ui.funcNpc.schoolTopTestConfirm, isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_SCHOOL_TOP_TEST, isWeeklyCheckOnce=True)
    else:
        gameglobal.rds.ui.funcNpc.schoolTopTestConfirm()


@funcMap(npcConst.NPC_FUNC_SHOW_TOP_RANK)
def NPC_FUNC_SHOW_TOP_RANK(functype, callType, entId, chatItem, extraParams = None):
    close()
    topId = chatItem[2]
    gameglobal.rds.ui.funcNpc.uiAdapter.rankCommon.showRankCommon(topId)


@funcMap(npcConst.NPC_FUNC_SHOW_SCHOOL_TOP_VOTE)
def NPC_FUNC_SHOW_SCHOOL_TOP_VOTE(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.schoolTopVote.show()


@funcMap(npcConst.NPC_FUNC_WINGWORLD_COMMIT_ITEM)
def NPC_FUNC_WINGWORLD_COMMIT_ITEM(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    close()
    p.wingWorldCommitItem()


@funcMap(npcConst.NPC_FUNC_WINGWORLD_CELEBRATION)
def NPC_FUNC_WINGWORLD_CELEBRATION(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    close()
    p.requireStartWingWorldCelebration()


@funcMap(npcConst.NPC_FUNC_OPEN_WING_WORLD_HISTORY_BOOK)
def NPC_FUNC_OPEN_WING_WORLD_HISTORY_BOOK(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.funcNpc.uiAdapter.wingWorldHistoryBook.show()


@funcMap(npcConst.NPC_FUNC_CROSS_CLAN_WAR_OCCUPY_AWARD)
def NPC_FUNC_CROSS_CLAN_WAR_OCCUPY_AWARD(functype, callType, entId, chatItem, extraParams = None):
    close()
    npc = BigWorld.entities.get(entId)
    if npc:
        npc.cell.getAllCrossOccupyAward(const.NPC_AWARD_TYPE_CROSS_CLAN_WAR_ALL_OCCUPY)


@funcMap(npcConst.NPC_FUNC_CROSS_CLAN_WAR_ENTER)
def NPC_FUNC_CROSS_CLAN_WAR_ENTER(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.funcNpc.enterClanWar()


@funcMap(npcConst.NPC_FUNC_CROSS_CLAN_WAR_LEAVE)
def NPC_FUNC_CROSS_CLAN_WAR_LEAVE(functype, callType, entId, chatItem, extraParams = None):
    close()
    BigWorld.player().cell.leaveClanWar()


@funcMap(npcConst.NPC_FUNC_WW_ALLSOULS_EPIGRAPH)
def NPC_FUNC_WW_ALLSOULS_EPIGRAPH(functype, callType, entId, chatItem, extraParams = None):
    npc = BigWorld.entities.get(entId)
    gamelog.info('ypc@ all souls boss epigraph')
    close()
    gameglobal.rds.ui.funcNpc.uiAdapter.wingWorldEpigraph.requestEpigraphData(npc.id)


@funcMap(npcConst.NPC_FUNC_WW_RONGLU)
def NPC_FUNC_WW_RONGLU(functype, callType, entId, chatItem, extraParams = None):
    gamelog.info('ypc@ wing world ronglu npc!!!')
    close()
    gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WING_WORLD_RONGLU)


@funcMap(npcConst.NPC_FUNC_TELEPORT_BORN_ISLAND)
def NPC_FUNC_TELEPORT_BORN_ISLAND(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    npc = BigWorld.entities.get(entId)
    if not wingWorldUtils.isOpenWingWorld():
        p.showGameMsg(GMDD.data.WING_BORN_ISLAND_CLOSE, ())
        return
    if p.inWingWarCity():
        p.cell.teleportToWingBornIsland()
    else:
        npc.cell.enterToWingBornIslandByNpc()


@funcMap(npcConst.NPC_FUNC_SPRITE_EXPLORE)
def NPC_FUNC_SPRITE_EXPLORE(functype, callType, entId, chatItem, extraParams = None):
    if not gameglobal.rds.configData.get('enableExploreSprite', False):
        return
    p = BigWorld.player()
    p.cell.exploreSpriteSyncData()
    exploringList = list(p.spriteExtraDict['exploreSprite'].exploringIndexSet)
    close()
    if exploringList:
        gameglobal.rds.ui.summonedWarSpriteExploreState.show(exploringList)
    else:
        gameglobal.rds.ui.summonedWarSpriteExplore.show()


@funcMap(npcConst.NPC_FUNC_YAOJINGQITAN)
def NPC_FUNC_YAOJINGQITAN(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.yaoJingShouShu.show()


@funcMap(npcConst.NPC_FUNC_WINGWORLD_XINMO_ARENA)
def NPC_FUNC_WINGWORLD_XINMO_ARENA(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.wingStageChoose.show()


@funcMap(npcConst.NPC_FUNC_WINGWORLD_XINMO_UNIQUE_BOSS)
def NPC_FUNC_WINGWORLD_XINMO_UNIQUE_BOSS(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    close()
    p.cell.applyWingWorldXinMoUniqueBoss()


@funcMap(npcConst.NPC_FUNC_WINGWORLD_XINMO_YUHUANG)
def NPC_FUNC_WINGWORLD_XINMO_YUHUANG(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    close()
    p.cell.applyWingWorldXinMoArenaML()


@funcMap(npcConst.NPC_FUNC_WINGWORLD_XINMO_NORMAL_BOSS)
def NPC_FUNC_WINGWORLD_XINMO_NORMAL_BOSS(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    close()
    p.cell.applyWingWorldXinMoNormalBoss(chatItem[2])


@funcMap(npcConst.NPC_FUNC_OPEN_ZIXUN)
def NPC_FUNC_OPEN_ZIXUN(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.ziXunInfo.show(chatItem[2])


@funcMap(npcConst.NPC_FUNC_TRANSFER_CONTRIB_JUNZI)
def NPC_FUNC_TRANSFER_CONTRIB_JUNZI(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    npc = BigWorld.entities.get(entId)
    close()
    reduceContrib = p.fame.get(const.WW_CONTRIB_FAME_ID, 0)
    if reduceContrib <= 0:
        p.showGameMsg(GMDD.data.TRANSFER_CONTRIB_JUNZI_FAIL, ())
        return
    else:
        func = WWCD.data.get('transferContrib2JunziFormula', None)
        if not func:
            return
        addJunzi = int(func({'contrib': reduceContrib}))
        text = GMD.data.get(GMDD.data.CONTRIBUTE_TO_JUNZI_CONFIRM, {}).get('text', '%d/%d') % (reduceContrib, addJunzi)
        gameglobal.rds.ui.funcNpc.uiAdapter.messageBox.showYesNoMsgBox(text, npc.cell.applyTransferContrib2Junzi)
        return


@funcMap(npcConst.NPC_FUNC_BLANCE_ARENA_CREATETEAM)
def NPC_FUNC_BLANCE_ARENA_CREATETEAM(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    close()
    if not gameglobal.rds.configData.get('enableDoubleArena', False):
        p.showGameMsg(GMDD.data.DOUBLE_ARENA_NOT_OPEN, ())
        return
    p.cell.dArenaOpenPanel()


@funcMap(npcConst.NPC_FUNC_SHOP, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_SHOP(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcEnt.cell.openShop(chatItem[0])


@funcMap(npcConst.NPC_FUNC_QUEST, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_QUEST(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    hasQuest = extraParams.get('hasQuest', False)
    if hasQuest:
        gamelog.debug('@szh: questNpc panelOpenType')
        if npcEnt is not None:
            player = BigWorld.player()
            debateQuestId = QND.data[npcId].get('debateQst', -1)
            if debateQuestId in player.quests and not player.getQuestData(debateQuestId, const.QD_QUEST_DEBATE) and not player.getQuestData(debateQuestId, const.QD_FAIL, True):
                npcEnt.showDebateWindow()
            else:
                npcEnt.showQuestWindow()


@funcMap(npcConst.NPC_FUNC_FB_AI, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_FB_AI(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    if formula.getFubenNo(p.obSpaceNo) in const.GUILD_FUBEN_ELITE_NOS:
        return
    else:
        npcEnt = BigWorld.entity(entId)
        if npcEnt is not None:
            npcEnt.showFbAIWindow(entId)
        return


@funcMap(npcConst.NPC_FUNC_UNBIND_FRIENDSHIP, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_UNBIND_FRIENDSHIP(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    if npcEnt is not None:
        npcEnt.showUnbindFriendshipWindow(entId)


@funcMap(npcConst.NPC_FUNC_BIND_FRIENDSHIP_MULTI_CHOICE, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_BIND_FRIENDSHIP_MULTI_CHOICE(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    if npcEnt is not None:
        npcEnt.showbindFriendshipWindow(entId)


@funcMap(npcConst.NPC_FUNC_ITEM_ENHANCE, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_ITEM_ENHANCE(functype, callType, entId, chatItem, extraParams = None):
    if gameglobal.rds.configData.get('enableEquipChangeEnhance', False):
        gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_ENHANCE, 0)
    else:
        gameglobal.rds.ui.equipEnhance.show(entId)


@funcMap(npcConst.NPC_FUNC_ITEM_ENHANCEMENT_TRANSFER, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_ITEM_ENHANCEMENT_TRANSFER(functype, callType, entId, chatItem, extraParams = None):
    if gameglobal.rds.configData.get('enableEquipChangeEnhance', False):
        gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_ENHANCE, 1)


@funcMap(npcConst.NPC_FUNC_ITEM_REFORGE_ENHANCE_JUEXING, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_ITEM_REFORGE_ENHANCE_JUEXING(functype, callType, entId, chatItem, extraParams = None):
    if gameglobal.rds.configData.get('enableEquipChangeReforge', False):
        gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_REFORGE, 0)
    else:
        close()


@funcMap(npcConst.NPC_FUNC_EQUIP_WASH, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_EQUIP_WASH(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_REFORGE, 1)


@funcMap(npcConst.NPC_FUNC_EXCHANGE_EQUIP_PRE_PROP, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_EXCHANGE_EQUIP_PRE_PROP(functype, callType, entId, chatItem, extraParams = None):
    if gameglobal.rds.configData.get('enableEquipChangeReforge', False):
        gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_REFORGE, 2)


@funcMap(npcConst.NPC_FUNC_FASHION_TRANSFER, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_FASHION_TRANSFER(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.fashionPropTransfer.show()
    gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_RUBBING, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_RUBBING(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.equipCopy.show(entId)


@funcMap(npcConst.NPC_FUNC_MIX_EQUIP, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_MIX_EQUIP(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.equipMix.show(entId, chatItem[0])
    gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_MIX_EQUIP_NEW, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_MIX_EQUIP_NEW(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.equipMixNew.show(entId, chatItem[0])
    gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_UPGRADE_EQUIP, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_UPGRADE_EQUIP(functype, callType, entId, chatItem, extraParams = None):
    if chatItem[0] == npcConst.SPECIAL_FILTER_TYPE_RIDE:
        gameglobal.rds.ui.wingAndMountUpgrade.show(uiConst.RIDE_EVE, 0, -1, -1, entId)
    elif chatItem[0] == npcConst.SPECIAL_FILTER_TYPE_WING:
        gameglobal.rds.ui.wingAndMountUpgrade.show(uiConst.WING_EVE, 0, -1, -1, entId)


@funcMap(npcConst.NPC_FUNC_COMPOSITE_SHOP, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_COMPOSITE_SHOP(functype, callType, entId, chatItem, extraParams = None):
    openType = extraParams.get('openType', 0)
    npcEnt = BigWorld.entity(entId)
    if openType:
        gameglobal.rds.ui.funcNpc.openDirectly(entId, npcEnt.npcId, npcConst.NPC_FUNC_COMPOSITE_SHOP)
    BigWorld.entities.get(entId).cell.openCompositeShop(chatItem[0])


@funcMap(npcConst.NPC_FUNC_STORAGE, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_STORAGE(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    if utils.isAbilityOn() and not p.getAbilityData(gametypes.ABILITY_STORAGE_ON):
        p.showGameMsg(GMDD.data.ABILITY_LACK_MSG, (gameStrings.TEXT_NPCFUNCMAPPINGS_1852,))
        return
    BigWorld.entities.get(entId).cell.use()


@funcMap(npcConst.NPC_FUNC_ACCEPT_PRIZE, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_ACCEPT_PRIZE(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.openPrizePanel(entId)


@funcMap(npcConst.NPC_FUNC_FB_TRAINING, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_FB_TRAINING(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.trainingArea.show(entId)


@funcMap(npcConst.NPC_FUNC_MAIL, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_MAIL(functype, callType, entId, chatItem, extraParams = None):
    BigWorld.entities.get(entId).cell.openMail()


@funcMap(npcConst.NPC_FUNC_CONSIGN, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_CONSIGN(functype, callType, entId, chatItem, extraParams = None):
    BigWorld.entities.get(entId).cell.openConsign()


@funcMap(npcConst.NPC_FUNC_APPLY_SHENG_SI_CHANG, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_APPLY_SHENG_SI_CHANG(functype, callType, entId, chatItem, extraParams = None):
    defaultChatId = extraParams.get('defaultChatId', [])
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    gameglobal.rds.ui.funcNpc.open(entId, npcId, defaultChatId, False)


@funcMap(npcConst.NPC_FUNC_NOTICE_BOARD, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_NOTICE_BOARD(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    openType = extraParams.get('openType', 0)
    if openType:
        gameglobal.rds.ui.funcNpc.openDirectly(entId, npcEnt.npcId, npcConst.NPC_FUNC_NOTICE_BOARD)
    gameglobal.rds.ui.noticeBoard.show(chatItem[0][0], chatItem[0][1])


@funcMap(npcConst.NPC_FUNC_TRAINING_AWARD, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_TRAINING_AWARD(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    openType = extraParams.get('openType', 0)
    if openType:
        gameglobal.rds.ui.funcNpc.openDirectly(entId, npcEnt.npcId, npcConst.NPC_FUNC_TRAINING_AWARD)
    gameglobal.rds.ui.trainingAreaAward.show()


@funcMap(npcConst.NPC_FUNC_EXPLANATION, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_EXPLANATION(functype, callType, entId, chatItem, extraParams = None):
    defaultChatId = extraParams.get('defaultChatId', [])
    gameglobal.rds.ui.funcNpc.openExplanationPanel(entId, chatItem[0], defaultChatId)


@funcMap(npcConst.NPC_FUNC_RUNE, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_RUNE(functype, callType, entId, chatItem, extraParams = None):
    openType = extraParams.get('openType', 0)
    npcEnt = BigWorld.entity(entId)
    if openType:
        gameglobal.rds.ui.funcNpc.openDirectly(entId, npcEnt.npcId, npcConst.NPC_FUNC_RUNE)
    gameglobal.rds.ui.runeLvUp.show(entId)
    gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_TELEPORT, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_TELEPORT(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.npcPanel.showNpcFullScreen(entId)


@funcMap((npcConst.NPC_FUNC_COMPENSATE,
 npcConst.NPC_FUNC_FORT_OCCUPY_AWARD,
 npcConst.NPC_FUNC_GUILD_RANK_AWARD,
 npcConst.NPC_FUNC_MEMBER_RANK_AWARD,
 npcConst.NPC_FUNC_GM_AWARD), callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_COMPENSATE(functype, callType, entId, chatItem, extraParams = None):
    defaultChatId = extraParams.get('defaultChatId', [])
    gameglobal.rds.ui.funcNpc.openAwardPanel(functype, entId, defaultChatId)


@funcMap(npcConst.NPC_FUNC_JOB_BOARD, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_JOB_BOARD(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    openType = extraParams.get('openType', 0)
    if openType:
        gameglobal.rds.ui.funcNpc.openDirectly(entId, npcEnt.npcId, npcConst.NPC_FUNC_JOB_BOARD)
    gameglobal.rds.ui.jobBoard.getAvailableJobs(entId)


@funcMap(npcConst.NPC_FUNC_RANK, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_RANK(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    npcEnt = BigWorld.entity(entId)
    openType = extraParams.get('openType', 0)
    lvRequire = SCD.data.get('RankListLv', 0)
    if lvRequire > p.lv:
        p.showGameMsg(GMDD.data.OPEN_RANK_LV_LOW, lvRequire)
        return
    if openType:
        gameglobal.rds.ui.funcNpc.openDirectly(entId, npcEnt.npcId, npcConst.NPC_FUNC_RANK)
    gameglobal.rds.ui.ranking.show(const.PROXY_KEY_TOP_COMBAT_SCORE, uiConst.RANK_TYPE_EQUIP_LV)


@funcMap(npcConst.NPC_FUNC_DYE, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_DYE(functype, callType, entId, chatItem, extraParams = None):
    openType = extraParams.get('openType', 0)
    npcEnt = BigWorld.entity(entId)
    if openType:
        gameglobal.rds.ui.funcNpc.openDirectly(entId, npcEnt.npcId, npcConst.NPC_FUNC_DYE)
    gameglobal.rds.ui.dyePlane.show(entId)
    if not gameglobal.rds.configData.get('enableWardrobe', False):
        gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)


@funcMap(npcConst.NPC_FUNC_HUAZHUANG, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_HUAZHUANG(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.close()
    gameglobal.rds.ui.huazhuang.show(entId)


@funcMap(npcConst.NPC_FUNC_TUZHUANG, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_TUZHUANG(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.close()
    gameglobal.rds.ui.tuZhuang.show()


@funcMap(npcConst.NPC_FUNC_FAME_REWARD, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_FAME_REWARD(functype, callType, entId, chatItem, extraParams = None):
    defaultChatId = extraParams.get('defaultChatId', [])
    gameglobal.rds.ui.funcNpc.openFameSalaryPanel(entId, chatItem[0], defaultChatId)


@funcMap(npcConst.NPC_FUNC_SOCIAL_SCHOOL_REJOIN, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_SOCIAL_SCHOOL_REJOIN(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    defaultChatId = extraParams.get('defaultChatId', [])
    hasQuest = extraParams.get('hasQuest', False)
    gameglobal.rds.ui.funcNpc.open(entId, npcId, defaultChatId, hasQuest)


@funcMap(npcConst.NPC_FUNC_QINGGONGJINSU, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_QINGGONGJINSU(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    defaultChatId = extraParams.get('defaultChatId', [])
    hasQuest = extraParams.get('hasQuest', False)
    gameglobal.rds.ui.funcNpc.open(entId, npcId, defaultChatId, hasQuest)


@funcMap(npcConst.NPC_FUNC_GUILD_GROWTH, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_GUILD_GROWTH(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    defaultChatId = extraParams.get('defaultChatId', [])
    hasQuest = extraParams.get('hasQuest', False)
    gameglobal.rds.ui.funcNpc.open(entId, npcId, defaultChatId, hasQuest)


@funcMap(npcConst.NPC_FUNC_YIXIN_UNBIND, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_YIXIN_UNBIND(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    defaultChatId = extraParams.get('defaultChatId', [])
    hasQuest = extraParams.get('hasQuest', False)
    gameglobal.rds.ui.funcNpc.open(entId, npcId, defaultChatId, hasQuest)


@funcMap(npcConst.NPC_FUNC_YIXIN_BIND, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_YIXIN_BIND(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    isShowYixin = gameglobal.rds.configData.get('enableYixin', False)
    if not isShowYixin:
        BigWorld.player().showGameMsg(GMDD.data.YIXIN_FUNC_CLOSE, ())
        return
    if not BigWorld.player().yixinOpenId:
        gameglobal.rds.ui.yixinBind.show()
    else:
        gameglobal.rds.ui.yixinRewards.show()


@funcMap(npcConst.NPC_FUNC_HUAZHUANG_PLUS, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_HUAZHUANG_PLUS(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.close()
    gameglobal.rds.ui.huazhuangPlus.show(entId)


@funcMap(npcConst.NPC_FUNC_GUILD, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_GUILD(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    defaultChatId = extraParams.get('defaultChatId', [])
    hasQuest = extraParams.get('hasQuest', False)
    npcEnt = BigWorld.entity(entId)
    op = chatItem[0]
    if op == gametypes.GUILD_NPC_OPTION_BUILDING:
        gameglobal.rds.ui.guildBuildSelect.show(markerId=getattr(npcEnt, 'markerId', 0), buildingNUID=npcEnt.buildingNUID, npcId=npcEnt.id)
    elif op == gametypes.GUILD_NPC_OPTION_VIEW_HIRED_RESIDENT:
        gameglobal.rds.ui.guildResident.show(uiConst.GUILD_RESIDENT_PANEL_HIRED, npcEnt.residentNUID)
    elif op == gametypes.GUILD_NPC_OPTION_ASSIGN_JOB:
        gameglobal.rds.ui.guildDispatch.show(npcEnt.residentNUID)
    elif op == gametypes.GUILD_NPC_OPTION_RENAME:
        gameglobal.rds.ui.funcNpc.openDirectly(entId, npcEnt.npcId, npcConst.NPC_FUNC_GUILD)
        gameglobal.rds.ui.guildRename.show()
    elif op == gametypes.GUILD_NPC_OPTION_WS_PRACTICE:
        gameglobal.rds.ui.funcNpc.openDirectly(entId, npcEnt.npcId, npcConst.NPC_FUNC_GUILD)
        gameglobal.rds.ui.guildWuShuang.show()
    elif op == gametypes.GUILD_NPC_OPTION_RECV_INHERIT_FROM_NPC:
        canExecute = True
        if functype == gametypes.GUILD_NPC_OPTION_RECV_INHERIT_FROM_NPC:
            serverProgressMsId = SCD.data.get('serverExpAddProgressId', 0)
            if gameconfigCommon.enableServerExpAddLimit() and serverProgressMsId and not player.checkServerProgress(serverProgressMsId, True):
                canExecute = False
        if canExecute:
            msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_INHERIT_FROM_NPC_MSG, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, npcEnt.cell.tryRecvGuildInheritFromNpc)
    else:
        gameglobal.rds.ui.funcNpc.open(entId, npcId, defaultChatId, hasQuest)


@funcMap(npcConst.NPC_FUNC_GUILD_BUILDING_REMOVE, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_GUILD_BUILDING_REMOVE(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.guildBuildSelectRemove.show(chatItem[0])


@funcMap(npcConst.NPC_FUNC_FUBEN_DIFFICULTY_ADJUST, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_FUBEN_DIFFICULTY_ADJUST(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    defaultChatId = extraParams.get('defaultChatId', [])
    hasQuest = extraParams.get('hasQuest', False)
    gameglobal.rds.ui.funcNpc.open(entId, npcId, defaultChatId, hasQuest)


@funcMap(npcConst.NPC_FUNC_CRAZY_SHISHEN_BOARD, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_CRAZY_SHISHEN_BOARD(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    npcData = ND.data.get(npcId, None)
    gameglobal.rds.ui.funcNpc.close()
    functions = npcData.get('functions', [])
    if len(functions[0]) >= 3:
        gameglobal.rds.ui.shishenBoard.show(functions[0][2])


@funcMap(npcConst.NPC_FUNC_PURCHASE_SHOP, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_PURCHASE_SHOP(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.purchaseShop.show(entId)
    BigWorld.entities.get(entId).cell.openPurchaseShop()


@funcMap(npcConst.NPC_FUNC_POINT_REFUND, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_POINT_REFUND(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    defaultChatId = extraParams.get('defaultChatId', [])
    hasQuest = extraParams.get('hasQuest', False)
    p = BigWorld.player()
    if not p.hasCoinRefund(const.POINT_TYPE_REFUND_PAY):
        p.base.queryCoinRefund(const.POINT_TYPE_REFUND_PAY)
    if not p.hasCoinRefund(const.POINT_TYPE_REFUND_FREE):
        p.base.queryCoinRefund(const.POINT_TYPE_REFUND_FREE)
    if p.hasCoinRefund(const.POINT_TYPE_REFUND_PAY) and p.hasCoinRefund(const.POINT_TYPE_REFUND_FREE):
        gameglobal.rds.ui.funcNpc.openAwardPanel(npcConst.NPC_FUNC_POINT_REFUND, entId, defaultChatId)
    else:
        gameglobal.rds.ui.funcNpc.open(entId, npcId, defaultChatId, hasQuest)


@funcMap(npcConst.NPC_FUNC_FUNBEN_RANK, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_FUNBEN_RANK(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    npcData = ND.data.get(npcId, None)
    fubenNo = 0
    functions = npcData.get('functions', [])
    if len(functions[0]) >= 3:
        fubenNo = functions[0][2]
    gameglobal.rds.ui.ranking.show(const.PROXY_KEY_TOP_FB_TIME, fbNo=fubenNo)


@funcMap(npcConst.NPC_FUNC_WMD_KILL_RANK, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_WMD_KILL_RANK(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.wmdRankList.openKillRank()


@funcMap(npcConst.NPC_FUNC_WMD_SHANGJIN_RANK, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_WMD_SHANGJIN_RANK(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.wmdRankList.openShangjinRank()


@funcMap(npcConst.NPC_FUNC_YCWZ_RANK, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_YCWZ_RANK(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.ycwzRankList.show()


@funcMap(npcConst.NPC_FUNC_YUNCHUIJI, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_YUNCHUIJI(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.yunchuiji.show()


@funcMap(npcConst.NPC_FUNC_DYE_RESET, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_DYE_RESET(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    openType = extraParams.get('openType', 0)
    if openType:
        gameglobal.rds.ui.funcNpc.openDirectly(entId, npcEnt.npcId, npcConst.NPC_FUNC_DYE_RESET)
    gameglobal.rds.ui.dyeReset.show()


@funcMap(npcConst.NPC_FUNC_SAVE_AVATARCONFIG, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_SAVE_AVATARCONFIG(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.close()
    gameglobal.rds.ui.characterDetailAdjust.onSaveNpcConfig()


@funcMap(npcConst.NPC_FUNC_SUIT_ACTIVATE, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_SUIT_ACTIVATE(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.equipSuit.show()


@funcMap(npcConst.NPC_FUNC_MAKE_MANUAL_EQUIP, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_MAKE_MANUAL_EQUIP(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.manualEquip.show(entId)


@funcMap(npcConst.NPC_FUNC_GUANYIN_REPAIR, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_GUANYIN_REPAIR(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.huiZhangRepair.show()


@funcMap(npcConst.NPC_FUNC_SUMMON_PLANE_IN_FORT_BATTLE_FIELD, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_SUMMON_PLANE_IN_FORT_BATTLE_FIELD(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    defaultChatId = extraParams.get('defaultChatId', [])
    gameglobal.rds.ui.funcNpc.open(entId, npcId, defaultChatId, False)


@funcMap(npcConst.NPC_FUNC_ACTIVITY_RESET_CHAR, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_ACTIVITY_RESET_CHAR(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    defaultChatId = extraParams.get('defaultChatId', [])
    gameglobal.rds.ui.funcNpc.open(entId, npcId, defaultChatId, False)


@funcMap(npcConst.NPC_FUNC_APPLY_UNDISTURB, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_APPLY_UNDISTURB(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    defaultChatId = extraParams.get('defaultChatId', [])
    gameglobal.rds.ui.funcNpc.open(entId, npcId, defaultChatId, False)


@funcMap(npcConst.NPC_FUNC_COLLECT_ITEM, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_COLLECT_ITEM(functype, callType, entId, chatItem, extraParams = None):
    actId, bookType = chatItem[0][0], chatItem[0][1]
    gameglobal.rds.ui.xinmoBook.queryInfo(actId, bookType)


@funcMap(npcConst.NPC_FUNC_DIRECT_TRANFER, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_DIRECT_TRANFER(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    options = extraParams.get('options', {})
    gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_NPCFUNCMAPPINGS_2176 + options.values()[0][0][0], Functor(p.directTranfer, entId, options.values()[0][0][1], options.values()[0][0][2]), yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noCallback=None, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)


@funcMap(npcConst.NPC_FUNC_GUILD_JOB, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_GUILD_JOB(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    if gameglobal.rds.configData.get('enableGuildQuestBoard', False):
        gameglobal.rds.ui.guildJob.showGuildBoard(npcId, npcEnt)


@funcMap(npcConst.NPC_FUNC_FAME_CASH_EXCHANGE, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_FAME_CASH_EXCHANGE(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    npcData = ND.data.get(npcId, None)
    functions = npcData.get('functions', [])
    if len(functions[0]) >= 3:
        gameglobal.rds.ui.funcNpc.openDirectly(entId, npcEnt.npcId, npcConst.NPC_FUNC_FAME_CASH_EXCHANGE)
        gameglobal.rds.ui.fameCashExchange.show(entId, functions[0][2])


@funcMap(npcConst.NPC_FUNC_WISH_MADE, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_WISH_MADE(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    gameglobal.rds.ui.funcNpc.openDirectly(entId, npcEnt.npcId, npcConst.NPC_FUNC_WISH_MADE)
    gameglobal.rds.ui.inventory.show()
    gameglobal.rds.ui.wishMade.show()


@funcMap(npcConst.NPC_FUNC_WISH_VIEW, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_WISH_VIEW(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    gameglobal.rds.ui.funcNpc.openDirectly(entId, npcEnt.npcId, npcConst.NPC_FUNC_WISH_VIEW)
    gameglobal.rds.ui.wishMadeView.show()


@funcMap(npcConst.NPC_FUNC_ZHENYAO_RANK_LIST, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_ZHENYAO_RANK_LIST(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.zhenyao.showRankList()


@funcMap(npcConst.NPC_FUNC_MIX_FAME_JEWELRY, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_MIX_FAME_JEWELRY(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.mixFameJewelry.show()


@funcMap(npcConst.NPC_FUNC_SHAXING_SIGNUP, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_SHAXING_SIGNUP(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    hasQuest = extraParams.get('hasQuest', False)
    signUpChat = ND.data.get(npcId, {}).get('signUpChat', [])
    gameglobal.rds.ui.funcNpc.open(entId, npcId, signUpChat, hasQuest)


@funcMap(npcConst.NPC_FUNC_SHAXING_OBSERVE, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_SHAXING_OBSERVE(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    hasQuest = extraParams.get('hasQuest', False)
    observeChat = ND.data.get(npcId, {}).get('observeChat', [])
    gameglobal.rds.ui.funcNpc.open(entId, npcId, observeChat, hasQuest)


@funcMap(npcConst.NPC_FUNC_SHARE_CHAR_CONF, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_SHARE_CHAR_CONF(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    p.uploadCharacter()


@funcMap(npcConst.NPC_FUNC_REAL_NAME_REWARD, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_REAL_NAME_REWARD(functype, callType, entId, chatItem, extraParams = None):
    BigWorld.player().base.applyRealNameReward()


@funcMap(npcConst.NPC_FUNC_PERSONAL_SPACE, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_PERSONAL_SPACE(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    gameglobal.rds.ui.funcNpc.close()
    p = BigWorld.player()
    p.getPersonalSysProxy().openZoneOther(getattr(npcEnt, 'statueOwnerGbId', 0))


@funcMap(npcConst.NPC_FUNC_TEAM_INVITE, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_TEAM_INVITE(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    p.chatNpcInviteTeam(const.CHAT_INVITE_TEAM_FOR_XUNLING)


@funcMap(npcConst.NPC_FUNC_TEAM_INVITE_FOR_YOULI, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_TEAM_INVITE_FOR_YOULI(functype, callType, entId, chatItem, extraParams = None):
    p = BigWorld.player()
    p.chatNpcInviteTeam(const.CHAT_INVITE_TEAM_FOR_YOULI)


@funcMap(npcConst.NPC_FUNC_TORCH_LIGHT, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_TORCH_LIGHT(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    if getattr(npcEnt, 'torchIdx', 0):
        gameglobal.rds.ui.guildBonfire.lightBonfire(npcEnt.torchIdx)


@funcMap(npcConst.NPC_FUNC_MYSTERY_ANIMAL, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_MYSTERY_ANIMAL(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    defaultChatId = extraParams.get('defaultChatId', [])
    hasQuest = extraParams.get('hasQuest', False)
    gameglobal.rds.ui.funcNpc.open(entId, npcId, defaultChatId, False)


@funcMap(npcConst.NPC_FUNC_OPEN_ZIXUN, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_OPEN_ZIXUN(functype, callType, entId, chatItem, extraParams = None):
    gameglobal.rds.ui.funcNpc.close()
    gameglobal.rds.ui.ziXunInfo.show(chatItem[0])


@funcMap(npcConst.NPC_FUNC_TRANSFER_CONTRIB_JUNZI, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_TRANSFER_CONTRIB_JUNZI(functype, callType, entId, chatItem, extraParams = None):
    npcEnt = BigWorld.entity(entId)
    npcId = npcEnt.npcId
    defaultChatId = extraParams.get('defaultChatId', [])
    hasQuest = extraParams.get('hasQuest', False)
    gameglobal.rds.ui.funcNpc.open(entId, npcId, defaultChatId, False)


@funcMap(npcConst.NPC_FUNC_WW_ALLSOULS_EPIGRAPH, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_WW_ALLSOULS_EPIGRAPH(functype, callType, entId, chatItem, extraParams = None):
    gamelog.info('ypc@ all souls boss epigraph', entId)
    gameglobal.rds.ui.funcNpc.close()
    gameglobal.rds.ui.wingWorldEpigraph.requestEpigraphData(entId)


@funcMap(npcConst.NPC_FUNC_BATTLE_FIELD_NEW_FLAG_COMMIT)
def NPC_FUNC_BATTLE_FIELD_NEW_FLAG_COMMIT(functype, callType, entId, chatItem, extraParams = None):
    close()
    p = BigWorld.player()
    isCommit = False
    npc = BigWorld.entity(entId)
    towerId = DCD.data.get('newFlagCommitZaiju', {}).get(npc.npcId, 0)
    for i, pointId in enumerate(p.battleFiedlOccupyInfo):
        pointInfo = p.battleFiedlOccupyInfo[pointId]
        if towerId == pointInfo.get('fortId', 0) and pointInfo.get('camp', 0) == p.tempCamp:
            isCommit = True
            break

    if p._isOnZaiju():
        if isCommit:
            npc.cell.commitCanhuInNewFlagBattleField()
        else:
            p.showGameMsg(GMDD.data.BATTLE_FIELD_NEW_FALG_CONNOT_COMMIT)
    else:
        p.showGameMsg(GMDD.data.BATTLE_FIELD_NEW_FALG_COMMIT_ZAIJU_NULL)


@funcMap(npcConst.NPC_FUNC_ENTER_GUILD_FUBEN_NORMAL)
def NPC_FUNC_ENTER_GUILD_FUBEN_NORMAL(functype, callType, entId, chatItem, extraParams = None):
    close()
    p = BigWorld.player()
    if p.isInTeamOrGroup():
        if p.isHeader():
            msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_FUBEN_NORMAL_MSG_BOX, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(p.cell.applyEnterGuildFuben, const.FB_NO_GUILD_FUBEN))
        else:
            p.showGameMsg(GMDD.data.GUILD_FUBEN_NOT_GROUP_LEADER, ())
    else:
        p.showGameMsg(GMDD.data.GUILD_FUBEN_NOT_IN_GROUP, ())


@funcMap(npcConst.NPC_FUNC_ENTER_GUILD_FUBEN_ELITE)
def NPC_FUNC_ENTER_GUILD_FUBEN_ELITE(functype, callType, entId, chatItem, extraParams = None):
    close()
    p = BigWorld.player()
    p.cell.applyEnterGuildFuben(const.FB_NO_GUILD_FUBEN_ELITE)


@funcMap(npcConst.NPC_FUNC_OPEN_GUILD_FUBEN)
def NPC_FUNC_OPEN_GUILD_FUBEN(functype, callType, entId, chatItem, extraParams = None):
    close()
    p = BigWorld.player()
    if p.guild.memberMe.roleId in SCD.data.get('qualifyPostList', [1, 2]):
        msg = uiUtils.getTextFromGMD(GMDD.data.OPEN_GUILD_FUBEN_ELITE_MSG_BOX, '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(p.cell.applyOpenGuildFuben, const.FB_NO_GUILD_FUBEN_ELITE))
    else:
        p.showGameMsg(GMDD.data.OPEN_GUILD_FUBEN_POWER_LESS)


@funcMap(npcConst.NPC_FUNC_GUILD_FUBEN_SET_MEMBERS)
def NPC_FUNC_GUILD_FUBEN_SET_MEMBERS(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.guildMembersFbRank.show()


@funcMap(npcConst.NPC_FUNC_DONATE_SERVER)
def NPC_FUNC_DONATE_SERVER(functype, callType, entId, chatItem, extraParams = None):
    close()
    from guis import guildDonateProxy
    gameglobal.rds.ui.guildDonate.show(guildDonateProxy.DONATE_TYPE_SERVER)


@funcMap(npcConst.NPC_FUNC_DONATE_SERVER_RANK)
def NPC_FUNC_DONATE_SERVER_RANK(functype, callType, entId, chatItem, extraParams = None):
    close()
    gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_CROSS_CLAN_WAR_SERVER_CONTRIB)


@funcMap(npcConst.NPC_FUNC_MAIN_PLOT_PLAY_MOVIE)
def NPC_FUNC_MAIN_PLOT_PLAY_MOVIE(functype, callType, entId, chatItem, extraParams = None):
    close()
    scenarioId = chatItem[2]
    if not scenarioId:
        return
    p = BigWorld.player()
    scenarioName = SCND.data.get(scenarioId, {}).get('name', '')
    if scenarioName:
        p.scenarioPlay(scenarioName, 0)


@funcMap(npcConst.NPC_FUNC_TELEPORT_TO_GM_ACTIVITY_SERVER)
def NPC_FUNC_TELEPORT_TO_GM_ACTIVITY_SERVER(functype, callType, entId, charItem, extraParams = None):
    close()
    BigWorld.player().cell.teleportToGmActivityServer()


@funcMap(npcConst.NPC_FUNC_SOUL_BACK)
def NPC_FUNC_SOUL_BACK(functype, callType, entId, charItem, extraParams = None):
    close()
    goal = charItem[2]
    BigWorld.player().cell.soulbackByNpc(goal)


@funcMap(npcConst.NPC_FUNC_CQZZ_COMMIT_FLAG, callType=CALL_TYPE_ALL)
def NPC_FUNC_CQZZ_COMMIT_FLAG(functype, callType, entId, charItem, extraParams = None):
    close()
    npc = BigWorld.entity(entId)
    npc.cell.commitCqzzFlag()


@funcMap(npcConst.NPC_FUNC_CQZZ_TELEPORT, callType=CALL_TYPE_ALL)
def NPC_FUNC_CQZZ_TELEPORT(functype, callType, entId, charItem, extraParams = None):
    close()
    npc = BigWorld.entity(entId)
    npc.cell.teleportInCqzzBattleField()


@funcMap(npcConst.NPC_FUNC_ASSASSINATION_TOMB, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_ASSASSINATION_TOMB(functype, callType, entId, charItem, extraParams = None):
    close()
    if not gameglobal.rds.configData.get('enableAssassination', False):
        return
    gameglobal.rds.ui.assassinationTombstone.show(entId)


@funcMap(npcConst.NPC_FUNC_DOUBLE_PLANT_TREE, callType=CALL_TYPE_DIRECTLY_F)
def NPC_FUNC_DOUBLE_PLANT_TREE(functype, callType, entId, charItem, extraParams = None):
    close()
    p = BigWorld.player()
    p.doublePlantTreeReq(entId)


@funcMap(npcConst.NPC_FUNC_MANUAL_EQUIP_LV_UP, callType=CALL_TYPE_NPC_FUNC)
def NPC_FUNC_MANUAL_EQUIP_LV_UP(functype, callType, entId, charItem, extraParams = None):
    gameglobal.rds.ui.manualEquipLvUp.show(entId)


@funcMap(npcConst.NPC_FUNC_INTERACTIVE, callType=CALL_TYPE_ALL)
def NPC_FUNC_INTERACTIVE(functype, callType, entId, charItem, extraParams = None):
    close()
    gameglobal.rds.ui.npcInteractive.show(entId)


@funcMap(npcConst.NPC_FUNC_CROSS_SERVER_SXY_RANK, callType=CALL_TYPE_ALL)
def NPC_FUNC_CROSS_SERVER_SXY_RANK(functype, callType, entId, charItem, extraParams = None):
    close()
    gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_GSXY_GUILD_RANK)


@funcMap(npcConst.NPC_FUNC_CROSS_SERVER_SXY_CONTRIBUTE_RANK, callType=CALL_TYPE_ALL)
def NPC_FUNC_CROSS_SERVER_SXY_CONTRIBUTE_RANK(functype, callType, entId, charItem, extraParams = None):
    close()
    gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_GSXY_SERVER_CONTRIB)


@funcMap(npcConst.NPC_FUNC_ENTER_CROSS_SERVER_SXY, callType=CALL_TYPE_ALL)
def NPC_FUNC_ENTER_CROSS_SERVER_SXY(functype, callType, entId, charItem, extraParams = None):
    close()
    BigWorld.player().cell.enterMLGSXY()


@funcMap(npcConst.NPC_FUNC_CLAN_COURIER_JCT_TELEPORT)
def NPC_FUNC_CLAN_COURIER_JCT_TELEPORT(functype, callType, entId, chatItem, extraParams = None):
    close()
    npc = BigWorld.entities.get(entId)
    npc.cell.teleportToClanCourierJCT()


@funcMap(npcConst.NPC_FUNC_NF_RECEIVE_GIFT)
def NPC_FUNC_NF_RECEIVE_GIFT(functype, callType, entId, chatItem, extraParams = None):
    close()
    npc = BigWorld.entities.get(entId)
    gamelog.info('jbx:receiveGiftNF', commNpcFavor.getNpcPId(npc.npcId))
    BigWorld.player().base.receiveGiftNF(commNpcFavor.getNpcPId(npc.npcId))


@funcMap(npcConst.NPC_FUNC_NF_ACTOR_ROLE)
def NPC_FUNC_NF_ACTOR_ROLE(functype, callType, entId, chatItem, extraParams = None):
    close()
    npc = BigWorld.entities.get(entId)
    gameglobal.rds.ui.cosNpc.show(npc.npcId)


@funcMap(npcConst.NPC_FUNC_NF_ACCEPT_LOOP_QUEST)
def NPC_FUNC_NF_ACCEPT_LOOP_QUEST(functype, callType, entId, chatItem, extraParams = None):
    close()
    npc = BigWorld.entities.get(entId)
    gamelog.info('jbx:acceptDailyQuestLoopNF', commNpcFavor.getNpcPId(npc.npcId), gametypes.NF_QUESTLOOP_DAILY)
    BigWorld.player().base.acceptDailyQuestLoopNF(commNpcFavor.getNpcPId(npc.npcId), gametypes.NF_QUESTLOOP_DAILY)


@funcMap(npcConst.NPC_FUNC_NF_ACCEPT_LOOP_QUEST_WEEKLY)
def NPC_FUNC_NF_ACCEPT_LOOP_QUEST_WEEKLY(functype, callType, entId, chatItem, extraParams = None):
    close()
    npc = BigWorld.entities.get(entId)
    gamelog.info('jbx:acceptDailyQuestLoopNF', commNpcFavor.getNpcPId(npc.npcId), gametypes.NF_QUESTLOOP_WEEKLY)
    BigWorld.player().base.acceptDailyQuestLoopNF(commNpcFavor.getNpcPId(npc.npcId), gametypes.NF_QUESTLOOP_WEEKLY)


@funcMap(npcConst.NPC_FUNC_NF_ACCEPT_LOOP_QUEST_MONTHLY)
def NPC_FUNC_NF_ACCEPT_LOOP_QUEST_MONTHLY(functype, callType, entId, chatItem, extraParams = None):
    close()
    npc = BigWorld.entities.get(entId)
    gamelog.info('jbx:acceptDailyQuestLoopNF', commNpcFavor.getNpcPId(npc.npcId), gametypes.NF_QUESTLOOP_MONTHLY)
    BigWorld.player().base.acceptDailyQuestLoopNF(commNpcFavor.getNpcPId(npc.npcId), gametypes.NF_QUESTLOOP_MONTHLY)


@funcMap(npcConst.NPC_FUNC_NF_ACCEPT_QUEST)
def NPC_FUNC_NF_ACCEPT_QUEST(functype, callType, entId, chatItem, extraParams = None):
    close()
    npc = BigWorld.entities.get(entId)
    gamelog.info('jbx:acceptDailyQuestNF', commNpcFavor.getNpcPId(npc.npcId))
    BigWorld.player().base.acceptDailyQuestNF(commNpcFavor.getNpcPId(npc.npcId))
