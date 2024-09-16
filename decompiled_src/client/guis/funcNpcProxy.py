#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/funcNpcProxy.o
from gamestrings import gameStrings
import random
import BigWorld
from Scaleform import GfxValue
import commNpcFavor
import gameglobal
import gameconfigCommon
import gametypes
import uiConst
import npcConst
import gamelog
import const
import ui
import utils
from ui import gbk2unicode
from uiProxy import UIProxy
from helpers import capturePhoto
from guis import uiUtils
from guis import tipUtils
from item import Item
from gamestrings import gameStrings
from data import dialogs_data as GD
from data import npc_data as ND
from data import item_data as ID
from data import clan_war_fort_data as CCFD
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
from data import guild_config_data as GCD
from data import clan_courier_config_data as CCCD
from data import nf_npc_data as NND
from guis import npcFuncMappings

class FuncNpcProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FuncNpcProxy, self).__init__(uiAdapter)
        self.modelMap = {'getFuncNpcChatInfo': self.onGetFuncNpcChatInfo,
         'getChatString': self.onGetChatString,
         'clickCloseBtn': self.onClickCloseBtn,
         'registerQuest': self.onRegisterQuest,
         'registerNPCQuestCloseButton': self.onRegisterNPCQuestCloseButton,
         'questFuncBack': self.onBackBtnClick,
         'getFuncNpcDirectlyInfo': self.onGetFuncNpcDirectlyInfo,
         'getNpcType': self.onGetNpcType,
         'questFuncOk': self.onOkBtnClick,
         'getTooltip': self.onGetToolTip,
         'requirePrize': self.onRequirePrize,
         'getPrizeInfo': self.onGetPrizeInfo,
         'getExplanationInfo': self.onGetExplanation,
         'getCompensate': self.onGetAward,
         'requireCompensate': self.onRequireAward,
         'getFameSalaryInfo': self.onGetFameSalaryInfo,
         'getFameSalaryOption': self.onGetFameSalaryOption,
         'clickFameSalaryOption': self.onClickFameSalaryOption,
         'getBusinessSpyInfo': self.onGetBusinessSpyInfo}
        self.modelId = 0
        self.entityId = 0
        self.npcId = None
        self.choice = 0
        self.isShow = False
        self.headGen = None
        self.hasQuest = False
        self.defaultChatId = None
        self.mc = None
        self.npcQuestButton = None
        self.chatOption = []
        self.lastFuncType = 0
        self.lastFuncTypeData = 0
        self.explanationIndex = 0
        self.buttonCallback = None
        self.msgBoxId = 0

    def onGetNpcType(self, *arg):
        return GfxValue(self.lastFuncType)

    def open(self, entityId, npcId, defaultChatId, hasQuest = False):
        self.entityId = entityId
        self.npcId = npcId
        self.defaultChatId = defaultChatId
        self.hasQuest = hasQuest
        self.uiAdapter.openQuestWindow(uiConst.NPC_FUNC)

    def openDirectly(self, entityId, npcId, npcType):
        self.entityId = entityId
        self.npcId = npcId
        self.npcType = npcType
        self.uiAdapter.openQuestWindow(uiConst.NPC_FUNC_DIRECTLY)

    def onGetFuncNpcDirectlyInfo(self, *arg):
        self.lastFuncType = self.npcType
        uiChat = ND.data.get(self.npcId, {}).get('Uichat', [0])
        chatId = uiChat[0]
        msg = GD.data.get(chatId, {}).get('details', '')
        return GfxValue(gbk2unicode(msg))

    def onGetFuncNpcDirectlyInfoPy(self):
        self.lastFuncType = self.npcType
        uiChat = ND.data.get(self.npcId, {}).get('Uichat', [0])
        chatId = uiChat[0]
        msg = GD.data.get(chatId, {}).get('details', '')
        return msg

    def _getNpcName(self):
        try:
            npc = BigWorld.entity(self.entityId)
            if npc and npc.inWorld:
                return npc.roleName
            return uiUtils.getNpcName(self.npcId)
        except:
            gamelog.error(gameStrings.TEXT_FUNCNPCPROXY_128)

    def _getNpcChat(self):
        npc = BigWorld.entities.get(self.entityId)
        if npc and hasattr(npc, 'hasFuncClosed') and npc.hasFuncClosed():
            chatId = ND.data.get(self.npcId, {}).get('funcClosedChatId', [0])[0]
            data = GD.data.get(chatId, {})
            details = data.get('details', '')
            if details:
                return (details, -1)
        if len(self.defaultChatId):
            index = random.randint(0, len(self.defaultChatId) - 1)
            data = GD.data.get(self.defaultChatId[index], {})
            uiUtils.dealNpcSpeakEvents(data.get('speakEvent', None), self.entityId)
            robberChatId = npc.getNpcChatId() if hasattr(npc, 'getNpcChatId') else 0
            if robberChatId:
                self.defaultChatId[index] = robberChatId
            return (data.get('details', ''), self.defaultChatId[index])
        else:
            return ('', -1)

    def _getOptionChat(self, index):
        if index < len(self.chatOption):
            try:
                chatIdList = self.chatOption[index][1]
                i = random.randint(0, len(chatIdList) - 1)
                self.choice = chatIdList[i]
                return GD.data.get(chatIdList[i], {}).get('details', '')
            except:
                gamelog.error(gameStrings.TEXT_FUNCNPCPROXY_128)

    def _optionFilter(self, option):
        p = BigWorld.player()
        if option[1] == npcConst.NPC_FUNC_ARENA_CHALLENGE:
            if option[2] == gametypes.ARENA_CHALLENGE_TYPE_ACCEPT:
                if p.arenaChallengeStatus == gametypes.CROSS_ARENA_CHALLENGE_STATUS_APPLY_BY:
                    return True
                else:
                    return False
            elif option[2] == gametypes.ARENA_CHALLENGE_TYPE_ENTER:
                if p.arenaChallengeStatus == gametypes.CROSS_ARENA_CHALLENGE_STATUS_APPLY_BY_SUCC or p.arenaChallengeStatus == gametypes.CROSS_ARENA_CHALLENGE_STATUS_APPLY_SUCC or utils.hasRunningArenaChallenge(p):
                    return True
                else:
                    return False
        if option[1] == npcConst.NPC_FUNC_ACTIVITY_REWARD:
            activityType = option[2]
            needShowActivityInfo = SCD.data.get('needShowActivityRewardInfo', {})
            if activityType in needShowActivityInfo:
                if utils.getHostId() not in needShowActivityInfo.get(activityType, []):
                    return False
                else:
                    return True
            else:
                return True
        if option[1] == npcConst.NPC_FUNC_WINGWORLD_OPENDOOR:
            isFinish = gameglobal.rds.ui.wingWorldRemoveSeal.checkWingWorldRemoveMileStone('finish')
            if option[2] in (uiConst.NPC_BOSSDAMAGE_RANK_OPTION, uiConst.NPC_REMOVESEAL_RANK_OPTION):
                return not isFinish
        if (option[1] == npcConst.NPC_FUNC_COMPOSITE_SHOP or option[1] == npcConst.NPC_FUNC_PRIVATE_SHOP) and option[2] in SCD.data.get('COMPOSITE_SHOP_IDLIST_FASHION_EXHANGE', ()):
            return not gameglobal.rds.configData.get('enableFashionExhange', False)
        if option[1] == npcConst.NPC_FUNC_FASHION_EXHANGE:
            return gameglobal.rds.configData.get('enableFashionExhange', False)
        if option[1] == npcConst.NPC_FUNC_YABIAO:
            npcType = NYD.data.get(self.npcId, {}).get('type')
            if npcType == gametypes.NPC_YABIAO_COMPLETE:
                isFail = p.hasYabiaoFailItem() and not p.isYabiaoWhole()
                return bool(option[2]) == isFail
            return True
        if option[1] == npcConst.NPC_FUNC_ITEM_COMMIT:
            return self.uiAdapter.worldWar.enableWWNpcItemCommit()
        if option[1] == npcConst.NPC_FUNC_FREE_LOTTERY:
            return gameglobal.rds.configData.get('enableLotteryExchange', False) and p.lv >= SCD.data.get('freeLotteryLv', 45)
        if option[1] == npcConst.NPC_FUNC_GUILD_MERGE_STRT:
            return gameglobal.rds.configData.get('enableGuildMerger') and p.isGuildLeader() and p.guild.guildMergerVal.state == gametypes.GUILD_MERGER_STATE_CLOSE
        if option[1] == npcConst.NPC_FUNC_GUILD_MERGE_CONFIRM:
            return gameglobal.rds.configData.get('enableGuildMerger') and p.isGuildLeader() and p.guild.guildMergerVal.state in gametypes.GUILD_MERGE_CONFIRM_STATES
        if option[1] == npcConst.NPC_FUNC_GUILD_MERGE_CANCEL:
            return gameglobal.rds.configData.get('enableGuildMerger') and p.isGuildLeader() and p.guild.guildMergerVal.state in gametypes.GUILD_MERGE_CANCEL_STATES
        if option[1] == npcConst.NPC_FUNC_GUILD_CHANGE_NAME:
            return gameglobal.rds.configData.get('enableGuildMerger') and p.isGuildLeader() and getattr(p, 'guildMergeActivityStartTime', 0) and p.guildMergeActivityStartTime < utils.getNow() < p.guildMergeActivityStartTime + GCD.data.get('renameDuraAfterGuildMerger', const.TIME_INTERVAL_WEEK)
        if option[1] == npcConst.NPC_FUNC_WW_YABIAO_START:
            return gameglobal.rds.configData.get('enableWingWorldYabiao', False) and p.isGuildLeaders()
        if option[1] == npcConst.NPC_FUNC_WW_YABIAO_END:
            return gameglobal.rds.configData.get('enableWingWorldYabiao', False) and p.isGuildLeaders()
        if option[1] == npcConst.NPC_FUNC_WW_YABIAO_DAKA:
            return gameglobal.rds.configData.get('enableWingWorldYabiao', False) and p.isGuildLeaders()
        if option[1] == npcConst.NPC_FUNC_WW_YABIAO_SIHUO:
            return gameglobal.rds.configData.get('enableWingWorldYabiao', False)
        if option[1] == npcConst.NPC_FUNC_SCHOOL_TOP_TEST:
            return gameglobal.rds.configData.get('enableSchoolTopMatch', False) and gameglobal.rds.configData.get('enableSchoolTopTestFuben', False) and option[2] == p.school
        if option[1] == npcConst.NPC_FUNC_WINGWORLD_COMMIT_ITEM:
            return gameglobal.rds.configData.get('enableWingCelebrationActivity', False) and p.wingWorld.step == gametypes.WING_WORLD_SEASON_STEP_CELEBRATION
        if option[1] == npcConst.NPC_FUNC_WINGWORLD_CELEBRATION:
            return gameglobal.rds.configData.get('enableWingCelebrationActivity', False) and p.wingWorld.step == gametypes.WING_WORLD_SEASON_STEP_CELEBRATION
        if option[1] == npcConst.NPC_FUNC_OPEN_WING_WORLD_HISTORY_BOOK:
            return gameglobal.rds.configData.get('enableWingWorldHistoryBook', False)
        if option[1] == npcConst.NPC_FUNC_CROSS_CLAN_WAR_ENTER:
            clanWarStartTime = CCFD.data.values()[0].get('startTime', '')
            clanWarEndTime = CCFD.data.values()[0].get('endTime', '')
            if gameconfigCommon.enableClanWarCourier():
                clanWarEndTime = CCCD.data.get('moveEndTime', '')
            inClanWarTime = utils.inCrontabRange(clanWarStartTime, clanWarEndTime)
            return gameglobal.rds.configData.get('enableCrossClanWar', False) and getattr(p, 'crossClanWarTgtHostId', False) and (getattr(p, 'clanWarStatus', False) or p.inGlobalClanWarTime() and inClanWarTime) or gameconfigCommon.enableClanWarCourier() and inClanWarTime
        if option[1] == npcConst.NPC_FUNC_CROSS_CLAN_WAR_LEAVE:
            return gameglobal.rds.configData.get('enableCrossClanWar', False)
        if option[1] == npcConst.NPC_FUNC_SHOW_TOP_RANK:
            return gameglobal.rds.configData.get('enableSchoolTopMatch', False)
        if option[1] == npcConst.NPC_FUNC_SHOW_SCHOOL_TOP_VOTE:
            return gameglobal.rds.configData.get('enableSchoolTopMatch', False) and option[2] == p.school
        if option[1] == npcConst.NPC_FUNC_TELEPORT_BORN_ISLAND:
            return gameglobal.rds.configData.get('enableWingWorld', False)
        if option[1] == npcConst.NPC_FUNC_INTERACTIVE:
            npcPId = commNpcFavor.getNpcPId(self.npcId)
            return gameconfigCommon.enableNpcFavor() and p.checkNpcFrindLv() and NND.data.get(npcPId, {}).get('isGift', 0)
        if option[1] == npcConst.NPC_FUNC_NF_RECEIVE_GIFT:
            return gameconfigCommon.enableNpcFavor() and p.npcFavor.checkDailyGift(self.npcId) and not commNpcFavor.checkInLockTime() and p.checkNpcFrindLv()
        if option[1] == npcConst.NPC_FUNC_NF_ACTOR_ROLE:
            return gameconfigCommon.enableNpcFavor() and p.npcFavor.getNpcCosList(self.npcId) and not commNpcFavor.checkInLockTime() and p.checkNpcFrindLv()
        if option[1] == npcConst.NPC_FUNC_NF_ACCEPT_LOOP_QUEST:
            return gameconfigCommon.enableNpcFavor() and p.npcFavor.checkDailyQuest(self.npcId) and not commNpcFavor.checkInLockTime() and p.checkNpcFrindLv()
        if option[1] == npcConst.NPC_FUNC_NF_ACCEPT_LOOP_QUEST_WEEKLY:
            return gameconfigCommon.enableNpcFavor() and p.npcFavor.checkWeeklyQuest(self.npcId) and not commNpcFavor.checkInLockTime() and p.checkNpcFrindLv() and gameconfigCommon.enableNFNewQuestLoop()
        if option[1] == npcConst.NPC_FUNC_NF_ACCEPT_LOOP_QUEST_MONTHLY:
            return gameconfigCommon.enableNpcFavor() and p.npcFavor.checkMonthlyQuest(self.npcId) and not commNpcFavor.checkInLockTime() and p.checkNpcFrindLv() and gameconfigCommon.enableNFNewQuestLoop()
        if option[1] == npcConst.NPC_FUNC_NF_ACCEPT_QUEST:
            return gameconfigCommon.enableNpcFavor() and p.npcFavor.checkQuest(self.npcId) and not commNpcFavor.checkInLockTime() and p.checkNpcFrindLv()
        if option[1] == npcConst.NPC_FUNC_CROSS_SERVER_SXY_RANK:
            return gameconfigCommon.enableGSXY()
        if option[1] == npcConst.NPC_FUNC_CROSS_SERVER_SXY_CONTRIBUTE_RANK:
            return gameconfigCommon.enableGSXY()
        if option[1] == npcConst.NPC_FUNC_ENTER_CROSS_SERVER_SXY:
            return gameconfigCommon.enableGSXY()
        if option[1] == npcConst.NPC_FUNC_CLAN_COURIER_JCT_TELEPORT:
            return gameconfigCommon.enableClanWarCourier() and not BigWorld.player().isJct and not BigWorld.player().isClanCourierAvatar()
        if option[1] == npcConst.NPC_FUNC_MANUAL_EQUIP_LV_UP:
            return gameconfigCommon.enableUpgradeManaulEquip()
        if option[1] not in (npcConst.NPC_FUNC_ACTIVE_OLD_FRIEND,
         npcConst.NPC_FUNC_INACTIVE_OLD_FRIEND,
         npcConst.NPC_FUNC_FRIEND,
         npcConst.NPC_FUNC_GUILD):
            return True
        if option[1] == npcConst.NPC_FUNC_ACTIVE_OLD_FRIEND and not BigWorld.player().friend.oldFriendActive or option[1] == npcConst.NPC_FUNC_INACTIVE_OLD_FRIEND and BigWorld.player().friend.oldFriendActive or option[1] == npcConst.NPC_FUNC_FRIEND and BigWorld.player().friend.oldFriendActive:
            return True
        if option[1] == npcConst.NPC_FUNC_GUILD:
            if option[2] in gametypes.GUILD_NPC_FREE_RESIDENT:
                return gameglobal.rds.ui.guild.checkResidentNpcOption(self.entityId)
            else:
                return True
        return False

    def _getNpcOptions(self, movie):
        optionArray = movie.CreateArray()
        npc = BigWorld.entities.get(self.entityId)
        if npc is None:
            return optionArray
        else:
            p = BigWorld.player()
            p.stopAutoQuest()
            self.chatOption = npc.filterFunctions()
            if self.chatOption:
                i = 0
                for index, item in enumerate(self.chatOption):
                    if item[1] == npcConst.NPC_FUNC_QUEST:
                        if self.hasQuest:
                            ar = movie.CreateArray()
                            ar.SetElement(0, GfxValue(gbk2unicode(item[0])))
                            ar.SetElement(1, GfxValue(index))
                            optionArray.SetElement(i, ar)
                            i += 1
                    elif item[1] not in (npcConst.NPC_FUNC_MARKER, npcConst.NPC_FUNC_POINT_REFUND):
                        if self._optionFilter(item):
                            ar = movie.CreateArray()
                            ar.SetElement(0, GfxValue(gbk2unicode(item[0])))
                            ar.SetElement(1, GfxValue(index))
                            optionArray.SetElement(i, ar)
                            i += 1

            return optionArray

    def _getNpcOptionsPy(self):
        optionArray = []
        npc = BigWorld.entities.get(self.entityId)
        if npc is None:
            return optionArray
        else:
            p = BigWorld.player()
            p.stopAutoQuest()
            self.chatOption = npc.filterFunctions()
            if self.chatOption:
                for index, item in enumerate(self.chatOption):
                    if item[1] == npcConst.NPC_FUNC_QUEST:
                        if self.hasQuest:
                            ar = []
                            ar.append(item[0])
                            ar.append(index)
                            optionArray.append(ar)
                    elif item[1] not in (npcConst.NPC_FUNC_MARKER, npcConst.NPC_FUNC_POINT_REFUND):
                        if self._optionFilter(item):
                            ar = []
                            ar.append(item[0])
                            ar.append(index)
                            optionArray.append(ar)

            return optionArray

    def _getButtonOptions(self, movie):
        optionArray = movie.CreateArray()
        ent = BigWorld.entities.get(self.entityId)
        if ent is None:
            return optionArray
        else:
            self.chatOption = ent.filterFunctions()
            if self.chatOption:
                i = 0
                for index, item in enumerate(self.chatOption):
                    ar = movie.CreateArray()
                    ar.SetElement(0, GfxValue(gbk2unicode(item[0])))
                    ar.SetElement(1, GfxValue(index))
                    optionArray.SetElement(i, ar)
                    i += 1

            return optionArray

    def _getButtonOptionsPy(self):
        optionArray = []
        ent = BigWorld.entities.get(self.entityId)
        if ent is None:
            return optionArray
        else:
            self.chatOption = ent.filterFunctions()
            if self.chatOption:
                for index, item in enumerate(self.chatOption):
                    ar = []
                    ar.append(item[0])
                    ar.append(index)
                    optionArray.append(ar)

            return optionArray

    def onGetFuncNpcChatInfo(self, *arg):
        movie = self.movie
        obj = movie.CreateObject()
        npcName = self._getNpcName()
        chat, chatId = self._getNpcChat()
        options = None
        if self.buttonCallback:
            options = self._getButtonOptions(movie)
        else:
            options = self._getNpcOptions(movie)
        obj.SetMember('name', GfxValue(gbk2unicode(npcName)))
        obj.SetMember('chat', GfxValue(gbk2unicode(chat)))
        obj.SetMember('options', options)
        npc = BigWorld.entity(self.entityId)
        self.initHeadGen(npc)
        p = BigWorld.player()
        p.triggerNpcChat(npc.npcId, chatId)
        return obj

    def onGetFuncNpcChatInfoPy(self):
        obj = {}
        npcName = self._getNpcName()
        chat, chatId = self._getNpcChat()
        options = None
        if self.buttonCallback:
            options = self._getButtonOptionsPy()
        else:
            options = self._getNpcOptionsPy()
        obj['name'] = npcName
        obj['chat'] = chat
        obj['options'] = options
        obj['npcId'] = self.entityId
        npc = BigWorld.entity(self.entityId)
        if npc:
            p = BigWorld.player()
            p.triggerNpcChat(npc.npcId, chatId)
        return obj

    def onGetChatString(self, *arg):
        index = int(arg[3][0].GetNumber())
        self.click(index)

    def click(self, index):
        if index >= len(self.chatOption):
            return
        functype = self.chatOption[index][1]
        self.lastFuncType = functype
        if self.buttonCallback:
            self.buttonCallback(functype, self.chatOption[index][2])
            self.close()
            return
        npcFuncMappings.onFuncNpcProxyCallFunc(functype, self.entityId, self.chatOption, index)

    def enterClanWar(self):
        msg = GMD.data.get(GMDD.data.CROSS_CLAN_WAR_ENTER_CONFIRM, {}).get('text', 'CROSS_CLAN_WAR_ENTER_CONFIRM')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, BigWorld.player().cell.enterClanWar)

    def schoolTopTestConfirm(self):
        gamelog.info('jbx:schoolTopTestConfirm')
        BigWorld.player().cell.applySchoolTopDpsFuben()
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_SCHOOL_TOP_TEST)

    def unBindYixin(self):
        self.close()
        npc = BigWorld.entities.get(self.entityId)
        npc.cell.unbindYixin()

    def cancelUnBindYixin(self):
        self.close()

    def close(self):
        self.lastFuncType = 0
        self.lastFuncTypeData = None
        if gameglobal.rds.ui.quest.isShow:
            self.uiAdapter.closeQuestWindow()
        if gameglobal.rds.ui.npcV2.isShow:
            gameglobal.rds.ui.npcV2.leaveStage()
        self.buttonCallback = None

    def onClickCloseBtn(self, *arg):
        self.close()

    def initHeadGen(self, npc):
        if not npc:
            return
        if not self.headGen:
            self.headGen = capturePhoto.LargePhotoGen.getInstance('gui/taskmask.tga', 700)
        uiUtils.takePhoto3D(self.headGen, npc, npc.npcId)

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def openFuncPanelState(self, funcType):
        self.lastFuncType = funcType
        self.onFuncState()
        if self.mc:
            self.mc.Invoke('removeItems')

    def onFuncState(self, needShowBackBtn = True):
        if self.lastFuncType == npcConst.NPC_FUNC_EXPLANATION:
            pass
        elif self.lastFuncType == npcConst.NPC_FUNC_FB_TRAINING:
            gameglobal.rds.ui.trainingNpc.onSelectBoss(self.entityId)
        elif self.lastFuncType in (npcConst.NPC_FUNC_BUILD_PARTNER,
         npcConst.NPC_FUNC_ADD_PARTNER,
         npcConst.NPC_FUNC_KICKOUT_PARTNER,
         npcConst.NPC_FUNC_EXIT_PARTNER):
            if self.mc:
                self.mc.Invoke('removeItems')
        elif self.mc:
            self.mc.Invoke('onFuncState')
        if needShowBackBtn:
            if self.npcQuestButton and self.uiAdapter.quest.isShow:
                self.npcQuestButton.Invoke('onFuncState')
            elif self.uiAdapter.npcV2.isShow:
                self.uiAdapter.npcV2.showReturnBtn()

    def onDefaultState(self):
        if self.mc:
            self.mc.Invoke('onDefaltState')
            self.npcQuestButton.Invoke('onDefalutState')
        if self.lastFuncType == npcConst.NPC_FUNC_ITEM_ENHANCEMENT_TRANSFER:
            self.lastFuncType = 0
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_ITEM_ENHANCE:
            self.lastFuncType = 0
            gameglobal.rds.ui.equipEnhance.clearAllWidget()
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_FASHION_TRANSFER:
            self.lastFuncType = 0
            gameglobal.rds.ui.fashionPropTransfer.clearWidget()
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_EXCHANGE_EQUIP_PRE_PROP:
            self.lastFuncType = 0
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_COPY_CHARACTER:
            gameglobal.rds.ui.characterCopy.clearWidget()
        elif self.lastFuncType == npcConst.NPC_FUNC_TRANSFER_EQUIP_PROPS:
            self.lastFuncType = 0
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_ITEM_REFORGE_ENHANCE_JUEXING:
            self.lastFuncType = 0
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_BIRDLET:
            self.lastFuncType = 0
            if gameglobal.rds.ui.birdLetHotLine.mediator:
                gameglobal.rds.ui.birdLetHotLine.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_BIRDLET:
            self.lastFuncType = 0
            if gameglobal.rds.ui.birdLetHotLine.mediator:
                gameglobal.rds.ui.birdLetHotLine.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_SHOP:
            self.lastFuncType = 0
            gameglobal.rds.ui.shop.hide(True)
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_COMPOSITE_SHOP:
            self.lastFuncType = 0
            gameglobal.rds.ui.compositeShop.hide(True)
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_PRIVATE_SHOP:
            self.lastFuncType = 0
            gameglobal.rds.ui.compositeShop.hide()
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_MIX_EQUIP:
            self.lastFuncType = 0
            gameglobal.rds.ui.equipMix.hide()
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_MIX_EQUIP_NEW:
            self.lastFuncType = 0
            gameglobal.rds.ui.equipMixNew.hide()
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_UPGRADE_EQUIP or self.lastFuncType == npcConst.NPC_FUNC_EQUIP_WASH:
            self.lastFuncType = 0
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
            if self.lastFuncType == npcConst.NPC_FUNC_UPGRADE_EQUIP and gameglobal.rds.ui.wingAndMountUpgrade.mediator:
                gameglobal.rds.ui.wingAndMountUpgrade.clearWidget()
        elif self.lastFuncType == npcConst.NPC_FUNC_EQUP_STAR_ACTIVATE:
            self.lastFuncType = 0
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_UNLOCK_EQUIP_GEM_SLOT:
            self.lastFuncType = 0
            gameglobal.rds.ui.equipmentSlot.hide()
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_RANK:
            self.lastFuncType = 0
            gameglobal.rds.ui.ranking.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_REPAIR_SHIHUN:
            self.lastFuncType = 0
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_UNLOCK_EQUIP_GEM_SLOT:
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
            if gameglobal.rds.ui.equipmentSlot.mediator:
                gameglobal.rds.ui.equipmentSlot.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_GET_EXP_BONUS:
            if gameglobal.rds.ui.expBonus.mediator:
                gameglobal.rds.ui.expBonus.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_CBG:
            gameglobal.rds.ui.cbgMain.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_WORLD_CHALLENGE:
            gameglobal.rds.ui.challenge.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_YUNCHUIJI:
            gameglobal.rds.ui.yunchuiji.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_STORAGE:
            gameglobal.rds.ui.inventory.hide()
            gameglobal.rds.ui.storage.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_FAME_REWARD:
            self.lastFuncType = 0
            if gameglobal.rds.ui.fameSalary.mediator:
                gameglobal.rds.ui.fameSalary.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_ITEM_REDEMPTION:
            if gameglobal.rds.ui.equipRedemption.mediator:
                gameglobal.rds.ui.equipRedemption.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_FUNBEN_RANK:
            self.lastFuncType = 0
            if gameglobal.rds.ui.ranking.mediator:
                gameglobal.rds.ui.ranking.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_WMD_KILL_RANK or self.lastFuncType == npcConst.NPC_FUNC_WMD_SHANGJIN_RANK:
            self.lastFuncType = 0
            if gameglobal.rds.ui.wmdRankList.mediator:
                gameglobal.rds.ui.wmdRankList.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_YCWZ_RANK:
            self.lastFuncType = 0
            gameglobal.rds.ui.ycwzRankList.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_RECYCLE_ITEM:
            self.lastFuncType = 0
            gameglobal.rds.ui.itemRecall.hide()
            gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_RUBBING:
            self.lastFuncType = 0
            gameglobal.rds.ui.equipCopy.hide()
            gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_DYE_RESET:
            self.lastFuncType = 0
            gameglobal.rds.ui.dyeReset.hide()
            gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_GUILD_SALARY_ASSIGN:
            self.lastFuncType = 0
            gameglobal.rds.ui.guildSalaryAssign.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_GUILD_SALARY_RECEIVE:
            self.lastFuncType = 0
            gameglobal.rds.ui.guildSalaryReceive.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_DYE:
            self.lastFuncType = 0
            gameglobal.rds.ui.dyePlane.hide()
            gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_GUILD_LUXURY_RANK:
            self.lastFuncType = 0
            gameglobal.rds.ui.guildLuxuryRank.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_GUILD_SALARY_HISTORY:
            self.lastFuncType = 0
            gameglobal.rds.ui.guildSalaryHistory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_USER_ACCOUNT_BIND:
            self.lastFuncType = 0
            gameglobal.rds.ui.userAccountBind.hide()
            gameglobal.rds.ui.accountBind.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_MIGRATE:
            self.lastFuncType = 0
            gameglobal.rds.ui.migrateServer.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_BACKFLOW_VP:
            self.lastFuncType = 0
        elif self.lastFuncType == npcConst.NPC_FUNC_DGT_BUSINESS:
            self.lastFuncType = 0
            gameglobal.rds.ui.guildBusinessDelegate.hide()
            gameglobal.rds.ui.guildBusinessDelegatePublish.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_SUIT_ACTIVATE:
            self.lastFuncType = 0
            gameglobal.rds.ui.equipSuit.hide()
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_GUANYIN_REPAIR:
            self.lastFuncType = 0
            gameglobal.rds.ui.huiZhangRepair.hide()
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_COLLECT_ITEM:
            self.lastFuncType = 0
            gameglobal.rds.ui.xinmoBook.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_YAOPEI_MIX:
            self.lastFuncType = 0
            gameglobal.rds.ui.yaoPeiMix.hide()
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_YAOPEI_TRANSFER:
            self.lastFuncType = 0
            gameglobal.rds.ui.yaoPeiTransfer.hide()
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_YAOPEI_REFORGE:
            self.lastFuncType = 0
            gameglobal.rds.ui.yaoPeiReforge.hide()
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_LOTTERY:
            self.lastFuncType = 0
            gameglobal.rds.ui.lottery.hide()
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_FUBEN_AWARD_TIMES:
            self.lastFuncType = 0
            gameglobal.rds.ui.fubenAwardTimes.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_YABIAO:
            self.lastFuncType = 0
            self.uiAdapter.yaBiao.hideYaBiaoAccept()
        elif self.lastFuncType == npcConst.NPC_FUNC_METERIAL_BAG:
            self.lastFuncType = 0
            self.uiAdapter.inventory.hide()
            self.uiAdapter.inventory.closeMaterialBag()
            self.uiAdapter.meterialBag.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_WISH_MADE:
            self.lastFuncType = 0
            self.uiAdapter.wishMade.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_WISH_VIEW:
            self.lastFuncType = 0
            self.uiAdapter.wishMadeView.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_ZHENYAO_RANK_LIST:
            self.lastFuncType = 0
            self.uiAdapter.zhenyao.closeRankList()
        elif self.lastFuncType == npcConst.NPC_FUNC_MIX_FAME_JEWELRY:
            self.lastFuncType = 0
            gameglobal.rds.ui.mixFameJewelry.show()
        elif self.lastFuncType == npcConst.NPC_FUNC_MAKE_MANUAL_EQUIP:
            self.lastFuncType = 0
            gameglobal.rds.ui.manualEquip.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_FROZEN_PUNISH:
            self.lastFuncType = 0
            gameglobal.rds.ui.frozenPunish.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_IMPEACH_START:
            self.lastFuncType = 0
            gameglobal.rds.ui.worldWar.closeWWImpeachStart()
        elif self.lastFuncType == npcConst.NPC_FUNC_FASHION_EXHANGE:
            self.lastFuncType = 0
            gameglobal.rds.ui.itemMsgBox.escFunc()
        elif self.lastFuncType == npcConst.NPC_FUNC_FREE_LOTTERY:
            self.lastFuncType = 0
            gameglobal.rds.ui.freeLottery.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_SCHOOL_TRANSFER:
            if gameglobal.rds.ui.schoolTransferSelect.widget:
                gameglobal.rds.ui.schoolTransferSelect.hide()
            if gameglobal.rds.ui.schoolTransferCondition.widget:
                gameglobal.rds.ui.schoolTransferCondition.hide()
            if gameglobal.rds.ui.schoolTransferHint.widget:
                gameglobal.rds.ui.schoolTransferHint.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_SCHOOL_TRANSFER_EQUIP:
            if gameglobal.rds.ui.schoolTransferEquip.widget:
                gameglobal.rds.ui.schoolTransferEquip.hide()

    def isOnFuncState(self):
        return self.lastFuncType != 0

    def onRegisterQuest(self, *arg):
        self.mc = arg[3][0]

    def onRegisterNPCQuestCloseButton(self, *arg):
        gamelog.debug('ASLog', 'onRegisterNPCQuestCloseButton')
        self.npcQuestButton = arg[3][0]

    def onBackBtnClick(self, *arg):
        self.onDefaultState()

    def onOkBtnClick(self, *arg):
        gameglobal.rds.ui.trainingNpc.onOkBtnClick(self.entityId)

    def openPrizePanel(self, entityId):
        ent = BigWorld.entity(entityId)
        if ent:
            self.entityId = entityId
            self.npcId = ent.npcId
            self.uiAdapter.openQuestWindow(uiConst.NPC_PRIZE)

    def openExplanationPanel(self, entityId, index, defaultChatId = None):
        ent = BigWorld.entity(entityId)
        if ent:
            if defaultChatId:
                self.defaultChatId = defaultChatId
            self.explanationIndex = index
            self.entityId = entityId
            self.npcId = ent.npcId
            self.uiAdapter.openQuestWindow(uiConst.NPC_EXPLAIN)

    def openAwardPanel(self, npcConstType, entityId, defaultChatId = None, npcConstTypeData = None):
        ent = BigWorld.entity(entityId)
        if ent:
            if npcConstType in npcConst.NPC_CELL_AWARD:
                if not ent.awardInfo.has_key(npcConstType):
                    ent.cell.getAwardInfo(npcConstType)
            elif npcConstType == npcConst.NPC_FUNC_POINT_REFUND:
                p = BigWorld.player()
                if not p.hasCoinRefund(const.POINT_TYPE_REFUND_PAY):
                    p.base.queryCoinRefund(const.POINT_TYPE_REFUND_PAY)
                if not p.hasCoinRefund(const.POINT_TYPE_REFUND_FREE):
                    p.base.queryCoinRefund(const.POINT_TYPE_REFUND_FREE)
            elif npcConstType == npcConst.NPC_FUNC_GM_AWARD:
                p = BigWorld.player()
                p.base.listFlowbackBonus()
            if defaultChatId:
                self.defaultChatId = defaultChatId
            self.lastFuncType = npcConstType
            self.lastFuncTypeData = npcConstTypeData
            self.entityId = entityId
            self.npcId = ent.npcId
            self.uiAdapter.openQuestWindow(uiConst.NPC_AWARD)

    def openFameSalaryPanel(self, entityId, fameId, defaultChatId = None):
        ent = BigWorld.entity(entityId)
        if ent:
            if defaultChatId:
                self.defaultChatId = defaultChatId
            self.lastFuncType = npcConst.NPC_FUNC_FAME_REWARD
            self.lastFuncTypeData = fameId
            self.entityId = entityId
            self.npcId = ent.npcId
            self.uiAdapter.openQuestWindow(uiConst.NPC_FAME_SALARY)

    def openBusinessSpyPanel(self, entityId):
        ent = BigWorld.entity(entityId)
        if ent:
            self.lastFuncType = npcConst.NPC_FUNC_BUSINESS_SPY
            self.entityId = entityId
            self.npcId = ent.npcId
            self.uiAdapter.openQuestWindow(uiConst.NPC_BUSINESS_SPY)
            self.fetchSpyBusinessInfo(ent)

    @ui.callFilter(1, False)
    def fetchSpyBusinessInfo(self, ent):
        ent.cell.fetchSpyBusinessInfo()

    def onGetBusinessSpyInfo(self, *arg):
        ent = BigWorld.entity(self.entityId)
        self.initHeadGen(ent)
        info = self.onGetBusinessSpyInfoPy()
        return uiUtils.dict2GfxDict(info, True)

    def onGetBusinessSpyInfoPy(self):
        info = {}
        info['chat'] = self._getNpcChat()[0]
        info['npcId'] = self.entityId
        return info

    def refreshBusinessSpy(self, npcId, saleId, saleInfoType, businessNpcNo):
        if self.npcId == npcId and self.lastFuncType == npcConst.NPC_FUNC_BUSINESS_SPY:
            info = {}
            info['chat'] = gameglobal.rds.ui.guildBusinessShop.createSpyChat(saleId, saleInfoType, businessNpcNo)
            if self.uiAdapter.npcV2.isShow:
                self.uiAdapter.npcV2.updateBusinessSpy(info)
            elif self.mc and self.uiAdapter.quest.isShow:
                self.mc.Invoke('refreshBusinessSpy', uiUtils.dict2GfxDict(info, True))

    def openDifficultyPanel(self, npcConstType, entityId, defaultChatId = None, npcConstTypeData = None):
        ent = BigWorld.entity(entityId)
        if ent:
            self.lastFuncType = npcConstType
            self.lastFuncTypeData = npcConstTypeData
            self.entityId = entityId
            self.npcId = ent.npcId
            self.uiAdapter.openQuestWindow(uiConst.NPC_FUBEN_DIFFICULTY)

    def setDarkBg(self, showBg = False):
        if self.mc:
            self.mc.Invoke('setDarkBg', GfxValue(showBg))

    def onGetPrizeInfo(self, *arg):
        p = BigWorld.player()
        info = p.getFishAward()
        ret = self.movie.CreateArray()
        item = None
        for i, item in enumerate(info):
            obj = self.movie.CreateObject()
            obj.SetMember('awardType', GfxValue(item['awardType']))
            obj.SetMember('awardTime', GfxValue(item['awardTime']))
            obj.SetMember('name', GfxValue(gbk2unicode(item['name'])))
            obj.SetMember('questDesc', GfxValue(gbk2unicode(item['questDesc'])))
            bonusList = self.movie.CreateArray()
            bonusData = BD.data.get(item.get('bonus', 0), {})
            fixedBonus = bonusData.get('fixedBonus', ())
            fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
            for j, bonus in enumerate(fixedBonus):
                bonusType, bonusItemId, bonusNum = bonus
                itemInfo = {}
                itemInfo['bonusType'] = bonusType
                itemInfo['bonusItemId'] = bonusItemId
                itemInfo['count'] = bonusNum
                if bonusType == gametypes.BONUS_TYPE_ITEM:
                    it = Item(bonusItemId)
                    itemInfo['name'] = 'item'
                    itemInfo['iconPath'] = uiUtils.getItemIconFile40(it.id)
                    if not it.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
                        itemInfo['state'] = uiConst.EQUIP_NOT_USE
                    else:
                        itemInfo['state'] = uiConst.ITEM_NORMAL
                    quality = ID.data.get(bonusItemId, {}).get('quality', 1)
                    qualitycolor = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                    itemInfo['qualitycolor'] = qualitycolor
                bonusList.SetElement(j, uiUtils.dict2GfxDict(itemInfo, True))

            obj.SetMember('bonus', bonusList)
            ret.SetElement(i, obj)

        obj = self.movie.CreateObject()
        msg = item.get('prizeChat', '') if item else ''
        if not msg:
            msg = GD.data.get(ND.data.get(self.npcId, {}).get('Uichat', [0])[0], {}).get('details', '')
        obj.SetMember('chat', GfxValue(gbk2unicode(msg)))
        obj.SetMember('targetId', GfxValue(self.npcId))
        obj.SetMember('option', ret)
        npc = BigWorld.entity(self.entityId)
        self.initHeadGen(npc)
        return obj

    def onGetPrizeInfoPy(self):
        p = BigWorld.player()
        info = p.getFishAward()
        ret = []
        item = None
        for i, item in enumerate(info):
            obj = {}
            obj['awardType'] = item['awardType']
            obj['awardTime'] = item['awardTime']
            obj['name'] = item['name']
            obj['questDesc'] = item['questDesc']
            bonusList = []
            bonusData = BD.data.get(item.get('bonus', 0), {})
            fixedBonus = bonusData.get('fixedBonus', ())
            fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
            for j, bonus in enumerate(fixedBonus):
                bonusType, bonusItemId, bonusNum = bonus
                itemInfo = {}
                itemInfo['bonusType'] = bonusType
                itemInfo['bonusItemId'] = bonusItemId
                itemInfo['count'] = bonusNum
                if bonusType == gametypes.BONUS_TYPE_ITEM:
                    it = Item(bonusItemId)
                    itemInfo['name'] = 'item'
                    itemInfo['iconPath'] = uiUtils.getItemIconFile40(it.id)
                    if not it.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
                        itemInfo['state'] = uiConst.EQUIP_NOT_USE
                    else:
                        itemInfo['state'] = uiConst.ITEM_NORMAL
                    quality = ID.data.get(bonusItemId, {}).get('quality', 1)
                    qualitycolor = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                    itemInfo['qualitycolor'] = qualitycolor
                bonusList.append(itemInfo)

            obj['bonus'] = bonusList
            ret.append(obj)

        obj = {}
        msg = item.get('prizeChat', '') if item else ''
        if not msg:
            msg = GD.data.get(ND.data.get(self.npcId, {}).get('Uichat', [0])[0], {}).get('details', '')
        obj['chat'] = msg
        obj['targetId'] = self.npcId
        obj['option'] = ret
        obj['npcId'] = self.entityId
        obj['roleName'] = ''
        return obj

    def onGetExplanation(self, *arg):
        ent = BigWorld.entity(self.entityId)
        self.initHeadGen(ent)
        obj = self.onGetExplanationPy()
        return uiUtils.dict2GfxDict(obj, True)

    def onGetExplanationPy(self):
        ent = BigWorld.entity(self.entityId)
        npcName = self._getNpcName()
        chat = self._getNpcChat()[0]
        obj = {'title': '',
         'details': '',
         'chat': chat,
         'roleName': npcName}
        if ent:
            index = self.explanationIndex
            title = ADD.data.get(index, {}).get('title', gameStrings.TEXT_CROSSWINGWORLDCAMPSTUB_1394)
            details = ADD.data.get(index, {}).get('details', gameStrings.TEXT_CROSSWINGWORLDCAMPSTUB_1394)
            obj['title'] = title
            obj['details'] = details
            obj['npcId'] = self.entityId
        return obj

    def getToolTip(self, index):
        return tipUtils.getItemTipById(index)

    def onGetToolTip(self, *arg):
        index = int(arg[3][0].GetNumber())
        return self.getToolTip(index)

    def requirePrize(self, awardType, awardTime):
        p = BigWorld.player()
        if (awardType, awardTime) in p.globalAwardCache:
            p.cell.claimGlobalAwards(awardType, awardTime)
        self.close()

    def onRequirePrize(self, *arg):
        awardType = int(arg[3][0].GetNumber())
        awardTime = int(arg[3][1].GetNumber())
        self.requirePrize(awardType, awardTime)

    def onGetAward(self, *arg):
        ent = BigWorld.entity(self.entityId)
        self.initHeadGen(ent)
        if self.lastFuncType == npcConst.NPC_FUNC_COMPENSATE:
            return self.onGetCompensate(*arg)
        if self.lastFuncType == npcConst.NPC_FUNC_FORT_OCCUPY_AWARD:
            return self.onGetFortOccupyAwardInfo()
        if self.lastFuncType == npcConst.NPC_FUNC_GUILD_RANK_AWARD:
            return self.onGetGuildRankAwardInfo()
        if self.lastFuncType == npcConst.NPC_FUNC_MEMBER_RANK_AWARD:
            return self.onGetMemberRankAwardInfo()
        if self.lastFuncType == npcConst.NPC_FUNC_POINT_REFUND:
            return self.onGetCoinRefundInfo()
        if self.lastFuncType == npcConst.NPC_FUNC_GM_AWARD:
            return self.onGetGMAwardInfo()

    def onGetAwardPy(self):
        if self.lastFuncType == npcConst.NPC_FUNC_COMPENSATE:
            ret = self.onGetCompensatePy()
        elif self.lastFuncType == npcConst.NPC_FUNC_FORT_OCCUPY_AWARD:
            ret = self.onGetFortOccupyAwardInfoPy()
        elif self.lastFuncType == npcConst.NPC_FUNC_GUILD_RANK_AWARD:
            ret = self.onGetGuildRankAwardInfoPy()
        elif self.lastFuncType == npcConst.NPC_FUNC_MEMBER_RANK_AWARD:
            ret = self.onGetMemberRankAwardInfoPy()
        elif self.lastFuncType == npcConst.NPC_FUNC_POINT_REFUND:
            ret = self.onGetCoinRefundInfoPy()
        elif self.lastFuncType == npcConst.NPC_FUNC_GM_AWARD:
            ret = self.onGetGMAwardInfoPy()
        ret['npcId'] = self.entityId
        return ret

    def onGetGMAwardInfoPy(self):
        p = BigWorld.player()
        bonusList = []
        bonusType = gametypes.BONUS_TYPE_ITEM
        reward = {bonusType: bonusList}
        npcName = self._getNpcName()
        chat = self._getNpcChat()[0]
        for item in p.gmFlowbackBonus:
            if item is None:
                continue
            itemId = item[0]
            extraInfo = {'bonusType': bonusType,
             'state': uiConst.ITEM_NORMAL}
            itemInfo = uiUtils.getGfxItemById(itemId, picSize=uiConst.ICON_SIZE40, appendInfo=extraInfo)
            itemInfo['qualitycolor'] = itemInfo['color']
            bonusList.append(itemInfo)

        ret = {'title': gameStrings.GMAWARD_TITLE,
         'details': gameStrings.GMAWARD_DETAILS,
         'itemDesc': gameStrings.GMAWARD_ITEMDESC,
         'chat': chat,
         'roleName': npcName,
         'reward': reward}
        return ret

    def onGetGMAwardInfo(self):
        ret = self.onGetGMAwardInfoPy()
        return uiUtils.dict2GfxDict(ret, True)

    def onGetCoinRefundInfoPy(self):
        npcName = self._getNpcName()
        chat = self._getNpcChat()[0]
        p = BigWorld.player()
        refundCoins = {}
        for cType, coinDesc in const.POINT_TYPE_DESC.iteritems():
            refundCoins[coinDesc] = p.refundCoins.get(cType, 0)

        ret = {'title': gameStrings.TEXT_FUNCNPCPROXY_1103,
         'details': gameStrings.TEXT_FUNCNPCPROXY_1103_1,
         'itemDesc': '',
         'chat': chat,
         'roleName': npcName,
         'reward': refundCoins}
        return ret

    def onGetCoinRefundInfo(self):
        npcName = self._getNpcName()
        chat = self._getNpcChat()[0]
        p = BigWorld.player()
        refundCoins = self.movie.CreateObject()
        for cType, coinDesc in const.POINT_TYPE_DESC.iteritems():
            refundCoins.SetMember(gbk2unicode(coinDesc), GfxValue(p.refundCoins.get(cType, 0)))

        ret = {'title': gameStrings.TEXT_FUNCNPCPROXY_1103,
         'details': gameStrings.TEXT_FUNCNPCPROXY_1103_1,
         'itemDesc': '',
         'chat': chat,
         'roleName': npcName}
        ret = uiUtils.dict2GfxDict(ret, True)
        ret.SetMember('reward', refundCoins)
        return ret

    def onGetFubenDifficulty(self):
        ent = BigWorld.entity(self.entityId)
        self.initHeadGen(ent)
        obj = self.onGetFubenDifficultyPy()
        return uiUtils.dict2GfxDict(obj, True)

    def onGetFubenDifficultyPy(self):
        npcName = self._getNpcName()
        chat = self._getNpcChat()[0]
        currentMode = gameglobal.rds.ui.currentShishenMode
        modeStr = SCD.data.get('fubenModeNames', ['',
         gameStrings.TEXT_QUESTTRACKPROXY_1748,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_1,
         gameStrings.TEXT_QUESTTRACKPROXY_1748_2,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_3])
        optionNames = {gametypes.FB_SHISHEN_MODE_LOW: modeStr[1],
         gametypes.FB_SHISHEN_MODE_MID: modeStr[2],
         gametypes.FB_SHISHEN_MODE_HIGH: modeStr[3]}
        obj = {'chat': chat,
         'roleName': npcName,
         'title': gameStrings.TEXT_FUNCNPCPROXY_1130,
         'options': [gametypes.FB_SHISHEN_MODE_LOW, gametypes.FB_SHISHEN_MODE_HIGH],
         'currentMode': currentMode,
         'optionNames': optionNames,
         'npcId': self.entityId}
        return obj

    def onGetFameSalaryInfo(self, *arg):
        ent = BigWorld.entity(self.entityId)
        self.initHeadGen(ent)
        info = self.onGetFameSalaryInfoPy()
        return uiUtils.dict2GfxDict(info, True)

    def onGetFameSalaryInfoPy(self):
        info = {}
        info['roleName'] = self._getNpcName()
        info['chat'] = self._getNpcChat()[0]
        info['title'] = gameStrings.TEXT_FUNCNPCPROXY_1143
        info['fameId'] = self.lastFuncTypeData
        info['npcId'] = self.entityId
        return info

    def onGetFameSalaryOption(self, *arg):
        fameId = int(arg[3][0].GetNumber())
        BigWorld.player().cell.getFameRewardTime(fameId)

    def refreshNpcFameSalaryOption(self, fameId, rewardList):
        p = BigWorld.player()
        fameLv = p.getFameLv(fameId)
        fd = FD.data.get(fameId, {})
        bonusList = fd.get('payBonusNew', {}).get(fameLv, ())
        option = []
        if len(bonusList) > 0:
            for bonusId in bonusList:
                bonusInfo = FRBD.data.get(bonusId, {})
                if bonusInfo.get('rewardType', 0) in rewardList:
                    itemInfo = {}
                    itemInfo['fameId'] = fameId
                    itemInfo['bonusId'] = bonusId
                    itemInfo['desc'] = bonusInfo.get('desc', '')
                    option.append(itemInfo)

        info = {}
        info['title'] = gameStrings.TEXT_FUNCNPCPROXY_1143
        info['option'] = option
        if fameLv < fd.get('payBonusLimitLevel', 0):
            info['extraText'] = gameStrings.TEXT_FUNCNPCPROXY_1171
        else:
            info['extraText'] = gameStrings.TEXT_FUNCNPCPROXY_1173 if len(rewardList) > 0 else ''
        if self.uiAdapter.npcV2.isShow:
            self.uiAdapter.npcV2.updateFameSalary(info)
        elif self.uiAdapter.quest.isShow:
            self.mc.Invoke('refreshNpcFameSalaryOption', uiUtils.dict2GfxDict(info, True))

    def onClickFameSalaryOption(self, *arg):
        fameId = int(arg[3][0].GetNumber())
        bonusId = int(arg[3][1].GetNumber())
        self.clickFameSalaryOption(fameId, bonusId)

    def clickFameSalaryOption(self, fameId, bonusId):
        self.onFuncState()
        gameglobal.rds.ui.fameSalary.show(self.entityId, fameId, bonusId)

    def onGetCompensatePy(self):
        reward = {}
        self.lastFuncType = npcConst.NPC_FUNC_COMPENSATE
        npc = BigWorld.entities.get(self.entityId)
        if not npc:
            return None
        else:
            fixedBonus = npc.awardInfo.get(npcConst.NPC_FUNC_COMPENSATE, [])
            gamelog.debug('onGetCompensate', fixedBonus)
            for bonus in fixedBonus:
                bonusType, bonusItemId, bonusNum = bonus
                if bonusType == gametypes.BONUS_TYPE_ITEM:
                    if not reward.has_key(bonusType):
                        bonusList = []
                        reward[bonusType] = bonusList
                    itemInfo = {}
                    itemInfo['bonusType'] = bonusType
                    itemInfo['bonusItemId'] = bonusItemId
                    itemInfo['count'] = bonusNum
                    itemInfo['name'] = 'item'
                    itemInfo['id'] = bonusItemId
                    info = ID.data.get(bonusItemId, {})
                    quality = info.get('quality', 1)
                    color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                    itemInfo['iconPath'] = uiUtils.getItemIconFile40(bonusItemId)
                    itemInfo['qualitycolor'] = color
                    itemInfo['state'] = uiConst.ITEM_NORMAL
                    bonusList.append(itemInfo)
                else:
                    if bonusType == gametypes.BONUS_TYPE_MONEY and bonusItemId:
                        bonusType = bonusType * 10 + bonusItemId
                    if not reward.has_key(bonusType):
                        reward[bonusType] = 0
                    reward[bonusType] += bonusNum

            npcName = self._getNpcName()
            chat = self._getNpcChat()[0]
            ret = {'title': gameStrings.TEXT_FUNCNPCPROXY_1227_2,
             'details': gameStrings.TEXT_FUNCNPCPROXY_1227_1,
             'itemDesc': gameStrings.TEXT_FUNCNPCPROXY_1227_2,
             'chat': chat,
             'roleName': npcName,
             'reward': reward}
            return ret

    def onGetCompensate(self, *arg):
        ret = self.onGetCompensatePy()
        return uiUtils.dict2GfxDict(ret, True)

    def onGetFortOccupyAwardInfoPy(self):
        npc = BigWorld.entities.get(self.entityId)
        if not npc:
            return None
        else:
            chunk = BigWorld.ChunkInfoAt(npc.position)
            fortId = CMD.data.get(chunk, {}).get('fortId', 0)
            bonusId = CWFD.data.get(fortId, {}).get('fortNpcBonusId')
            return self._onGetBonusInfoPy(bonusId, [], gameStrings.TEXT_FUNCNPCPROXY_1244, gameStrings.TEXT_FUNCNPCPROXY_1244_1, gameStrings.TEXT_FUNCNPCPROXY_1244_2, self._getNpcChat()[0], self._getNpcName())

    def onGetFortOccupyAwardInfo(self):
        ret = self.onGetFortOccupyAwardInfoPy()
        return uiUtils.dict2GfxDict(ret, True)

    def onGetGuildRankAwardInfoPy(self):
        npc = BigWorld.entities.get(self.entityId)
        if not npc:
            return None
        else:
            bonusId, rank = npc.awardInfo.get(npcConst.NPC_FUNC_GUILD_RANK_AWARD, (0, 0))
            return self._onGetBonusInfoPy(bonusId, [], gameStrings.TEXT_FUNCNPCPROXY_1257, gameStrings.TEXT_FUNCNPCPROXY_1257, gameStrings.TEXT_FUNCNPCPROXY_1244_2, self._getNpcChat()[0], self._getNpcName())

    def onGetGuildRankAwardInfo(self):
        ret = self.onGetGuildRankAwardInfoPy()
        return uiUtils.dict2GfxDict(ret, True)

    def onGetMemberRankAwardInfoPy(self):
        npc = BigWorld.entities.get(self.entityId)
        if not npc:
            return None
        else:
            bonusId, rank = npc.awardInfo.get(npcConst.NPC_FUNC_MEMBER_RANK_AWARD, (0, 0))
            return self._onGetBonusInfoPy(bonusId, [], gameStrings.TEXT_FUNCNPCPROXY_1270, gameStrings.TEXT_FUNCNPCPROXY_1270, gameStrings.TEXT_FUNCNPCPROXY_1244_2, self._getNpcChat()[0], self._getNpcName())

    def onGetMemberRankAwardInfo(self):
        ret = self.onGetMemberRankAwardInfoPy()
        return uiUtils.dict2GfxDict(ret, True)

    def _onGetBonusInfoPy(self, bonusId, bonusItems, bonusTitle, details, itemDesc, chat, npcName):
        fixedBonus = []
        if bonusId:
            bonusData = BD.data.get(bonusId, {})
            fixedBonus.extend(bonusData.get('fixedBonus', ()))
            fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        reward = {}
        for bonus in fixedBonus:
            bonusType, bonusItemId, bonusNum = bonus
            if bonusType == gametypes.BONUS_TYPE_ITEM:
                if not reward.has_key(bonusType):
                    bonusList = []
                    reward[bonusType] = bonusList
                itemInfo = {}
                itemInfo['bonusType'] = bonusType
                itemInfo['bonusItemId'] = bonusItemId
                itemInfo['count'] = bonusNum
                itemInfo['name'] = 'item'
                itemInfo['id'] = bonusItemId
                info = ID.data.get(bonusItemId, {})
                quality = info.get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                itemInfo['iconPath'] = uiUtils.getItemIconFile40(bonusItemId)
                itemInfo['qualitycolor'] = color
                itemInfo['state'] = uiConst.ITEM_NORMAL
                bonusList.append(itemInfo)
            else:
                if not reward.has_key(bonusType):
                    reward[bonusType] = 0
                reward[bonusType] += bonusNum

        ret = {'title': bonusTitle,
         'details': details,
         'itemDesc': itemDesc,
         'chat': chat,
         'roleName': npcName,
         'reward': reward}
        return ret

    def onRequireAward(self, *arg):
        gamelog.debug('onRequireAward', self.lastFuncType)
        npc = BigWorld.entities.get(self.entityId)
        if not npc:
            return
        if npc.awardInfo.has_key(self.lastFuncType):
            npc.awardInfo.pop(self.lastFuncType)
        if self.lastFuncType == npcConst.NPC_FUNC_COMPENSATE:
            npc.cell.getCompensation(const.NPC_AWARD_TYPE_COMPENSATE)
        elif self.lastFuncType == npcConst.NPC_FUNC_FORT_OCCUPY_AWARD:
            npc.cell.getFortOccupyAward(const.NPC_AWARD_TYPE_CLAN_WAR_OCCUPY)
        elif self.lastFuncType == npcConst.NPC_FUNC_CROSS_CLAN_WAR_OCCUPY_AWARD:
            npc.cell.getAllCrossOccupyAward(const.NPC_AWARD_TYPE_CROSS_CLAN_WAR_ALL_OCCUPY)
        elif self.lastFuncType == npcConst.NPC_FUNC_POINT_REFUND:
            BigWorld.player().doQueryCoinRefund()
        elif self.lastFuncType == npcConst.NPC_FUNC_GM_AWARD:
            p = BigWorld.player()
            if not p.gmFlowbackBonus:
                p.showGameMsg(GMDD.data.GM_AWARD_ISNONE, ())
            else:
                p.base.getFlowbackBonus()
        self.close()

    def closeByInv(self):
        if self.lastFuncType == npcConst.NPC_FUNC_SHOP:
            gameglobal.rds.ui.shop.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_CONSIGN:
            gameglobal.rds.ui.consign.hide()
            gameglobal.rds.ui.tabAuction.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_ITEM_ENHANCE:
            gameglobal.rds.ui.equipEnhance.clearAllWidget()
        elif self.lastFuncType == npcConst.NPC_FUNC_FASHION_TRANSFER:
            gameglobal.rds.ui.fashionPropTransfer.clearWidget()
        elif self.lastFuncType == npcConst.NPC_FUNC_COPY_CHARACTER:
            gameglobal.rds.ui.characterCopy.clearWidget()
        elif self.lastFuncType == npcConst.NPC_FUNC_BIRDLET:
            if gameglobal.rds.ui.birdLetHotLine.mediator:
                gameglobal.rds.ui.birdLetHotLine.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_COMPOSITE_SHOP:
            gameglobal.rds.ui.compositeShop.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_PRIVATE_SHOP:
            gameglobal.rds.ui.compositeShop.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_MAIL:
            gameglobal.rds.ui.mail.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_GUILD:
            gameglobal.rds.ui.guildStorage.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_RUNE:
            gameglobal.rds.ui.runeLvUp.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_TRAINING_AWARD:
            gameglobal.rds.ui.trainingAreaAward.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_MIX_EQUIP:
            gameglobal.rds.ui.equipMix.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_MIX_EQUIP_NEW:
            gameglobal.rds.ui.equipMixNew.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_UPGRADE_EQUIP or self.lastFuncType == npcConst.NPC_FUNC_EQUIP_WASH:
            if self.lastFuncType == npcConst.NPC_FUNC_UPGRADE_EQUIP and gameglobal.rds.ui.wingAndMountUpgrade.mediator:
                gameglobal.rds.ui.wingAndMountUpgrade.clearWidget()
        elif self.lastFuncType == npcConst.NPC_FUNC_UNLOCK_EQUIP_GEM_SLOT:
            gameglobal.rds.ui.equipmentSlot.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_NOTICE_BOARD:
            gameglobal.rds.ui.noticeBoard.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_RANK:
            gameglobal.rds.ui.ranking.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_REPAIR_SHIHUN:
            self.close()
        elif self.lastFuncType == npcConst.NPC_FUNC_JOB_BOARD:
            if gameglobal.rds.ui.jobBoard.detailMed != None:
                gameglobal.rds.ui.jobBoard.closeDetail()
            else:
                gameglobal.rds.ui.jobBoard.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_YIXIN_BIND:
            if not BigWorld.player().yixinOpenId:
                gameglobal.rds.ui.yixinBind.closeWidget()
            else:
                gameglobal.rds.ui.yixinRewards.closeWidget()
        elif self.lastFuncType == npcConst.NPC_FUNC_DYE:
            gameglobal.rds.ui.dyePlane.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_FUNBEN_RANK:
            gameglobal.rds.ui.ranking.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_SUIT_ACTIVATE:
            gameglobal.rds.ui.equipSuit.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_GUANYIN_REPAIR:
            gameglobal.rds.ui.huiZhangRepair.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_DYE_RESET:
            gameglobal.rds.ui.dyeReset.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_GUILD_JOB:
            if gameglobal.rds.ui.guildJob.detailMed != None:
                gameglobal.rds.ui.guildJob.closeGuildJobDetail()
            else:
                gameglobal.rds.ui.guildJob.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_METERIAL_BAG:
            if gameglobal.rds.ui.expandPay.mediator:
                gameglobal.rds.ui.expandPay.hide()
            else:
                gameglobal.rds.ui.inventory.closeMaterialBag()
                gameglobal.rds.ui.meterialBag.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_SPRITE_MATERIAL_BAG:
            if gameglobal.rds.ui.spriteMaterialBag.widget:
                gameglobal.rds.ui.spriteMaterialBag.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_MAKE_MANUAL_EQUIP:
            gameglobal.rds.ui.manualEquip.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_STORAGE:
            if gameglobal.rds.ui.expandPay.mediator:
                gameglobal.rds.ui.expandPay.hide()
            else:
                gameglobal.rds.ui.storage.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_SCHOOL_TRANSFER:
            if gameglobal.rds.ui.schoolTransferSelect.widget:
                gameglobal.rds.ui.schoolTransferSelect.hide()
            if gameglobal.rds.ui.schoolTransferCondition.widget:
                gameglobal.rds.ui.schoolTransferCondition.hide()
            if gameglobal.rds.ui.schoolTransferHint.widget:
                gameglobal.rds.ui.schoolTransferHint.hide()
        elif self.lastFuncType == npcConst.NPC_FUNC_SCHOOL_TRANSFER_EQUIP:
            if gameglobal.rds.ui.schoolTransferEquip.widget:
                gameglobal.rds.ui.schoolTransferEquip.hide()
        else:
            self.close()

    def openFunc(self, entityId, npcId, defaultChatId, callback = None):
        self.entityId = entityId
        self.npcId = npcId
        self.defaultChatId = defaultChatId
        self.uiAdapter.openQuestWindow(uiConst.NPC_FUNC)
        self.buttonCallback = callback
