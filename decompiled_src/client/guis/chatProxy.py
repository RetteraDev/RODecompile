#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/chatProxy.o
from gamestrings import gameStrings
import sys
import time
import locale
import BigWorld
import Math
from Scaleform import GfxValue
import CEFManager
import gamelog
import keys
import uiConst
import gameglobal
import gametypes
import const
import clientUtils
import utils
import re
import formula
import copy
import string
import commQuest
from callbackHelper import Functor
from item import Item
from guis import ui
from helpers import taboo
from uiProxy import UIProxy
from ui import gbk2unicode
from ui import unicode2gbk
from guis import richTextUtils
from guis import uiUtils
from appSetting import Obj as AppSettings
from guis import pinyinConvert
from guis import menuManager
from guis import hotkeyProxy
from guis.asObject import ASObject
from gameStrings import gameStrings
from data import state_data as SD
from data import mapSearch_ii_data as MII
from cdata import game_msg_def_data as GMDD
from data import title_data as TD
from cdata import font_config_data as FCD
from data import chat_channel_data as CCD
from data import quest_data as QD
from data import item_data as ID
from data import monster_data as MD
from data import achievement_data as AD
from data import achieve_target_data as ATD
from data import emote_data as ED
from data import sys_config_data as SCD
from data import chunk_mapping_data as CMD
from data import qiren_barrage_chat_data as QBCD
from cdata import migrate_server_data as MSD
from cdata import mapSearch_iii_data as MIII
from data import laba_config_data as LCD
from data import chat_reg_rule_data as CRRD
from data import fb_message_board_config_data as FMBCD
from data import chat_command_data as CCMD
from data import map_third_lv_data as MTLD
from cdata import personal_zone_config_data as PZCD
from guis import worldBossHelper
GM_CMD_NEED_TARGET_LOCKED = ['dmgstat',
 'statehitstat',
 'dpstat',
 'qcdmgstat',
 'rdmgstat',
 'healstat']
GM_CMD_NEED_VARIABLE_ARGS = ['createnpc', 'delnpc', 'evedel']
QIPAO_ID = '!$200'
YIXIN_ID = '!$201'
MAX_CHANNEL_NUM = 6
INIT_CHAT_TABS = [(const.CHANNEL_TAB_MULTIPLE, gameStrings.TEXT_CHATPROXY_76),
 (const.CHANNEL_TAB_SINGLE, gameStrings.TEXT_CHATPROXY_76_1),
 (const.CHANNEL_TAB_COMBAT, gameStrings.TEXT_CHATPROXY_76_2),
 (const.CHANNEL_TAB_SYSTEM, gameStrings.TEXT_BOOTHPROXY_694),
 (const.CHANNEL_TAB_GROUP, gameStrings.TEXT_CONST_5123)]
HTTP_LINK_REG = '<a href'

def FontColorAdd(matchobj):
    m = matchobj.group(2)
    return '<FONT COLOR=%s>' % m


class ChatProxy(UIProxy):
    UNACCEPT_TASK = 0
    ACCEPT_TASK = 1
    COMPLETE_TASK = 2
    MAX_TAB_NAME = 4

    def __init__(self, uiAdapter):
        super(ChatProxy, self).__init__(uiAdapter)
        self.modelMap = {'submitMessage': self.onSubmitMessage,
         'getPadChannels': self.onGetPadChannels,
         'getChannels': self.onGetChannels,
         'getChannelData': self.onGetChannelData,
         'registerMsgListener': self.onRegisterMsgListener,
         'showFace': self.showFace,
         'showGM': self.showGM,
         'getRightMenuVisible': self.onGetRightMenuVisible,
         'linkLeftClick': self.onLinkLeftClick,
         'fitting': self.onFitting,
         'registerChat': self.onRegisterChat,
         'isCommand': self.onIsCommand,
         'changeChannel': self.onChangeChannel,
         'createTab': self.onCreateTab,
         'configTab': self.onConfigTab,
         'deleteTab': self.onDeleteTab,
         'initChatConfig': self.onInitChatConfig,
         'closeChatConfig': self.onCloseChatConfig,
         'confirmConfig': self.onConfirmConfig,
         'confirmCreate': self.onConfirmCreate,
         'getTransparency': self.onGetTransparency,
         'setTransparency': self.onSetTransparency,
         'canCreateTab': self.onCanCreateTab,
         'setCurrentTab': self.onSetCurrentTab,
         'showAction': self.onShowAction,
         'showGameMsg': self.onShowGameMsg,
         'clickMenu': self.onClickMenu,
         'setInputAreaVisible': self.onSetInputAreaVisible,
         'isUIEnable': self.onIsUIEnable,
         'isNeedConfirm': self.onIsNeedConfirm,
         'getLastWorldExMessage': self.onGetLastWorldExMessage,
         'getLastWorldExType': self.onGetLastWorldExType,
         'getChatInfo': self.onGetChatInfo,
         'setChatInfo': self.onSetChatInfo,
         'setFontSize': self.onSetFontSize,
         'maxSize': self.onMaxSize,
         'sendPosInfo': self.doSendMapLink,
         'setOpenBarrage': self.onSetOpenBarrage,
         'changeLaba': self.onChangeLaba,
         'setOpenAnonymous': self.onSetAnonymous,
         'saveSelect': self.onSaveSelect,
         'saveAllLog': self.onSaveAllLog,
         'getChatLogs': self.onGetChatLogs,
         'showChatLogManager': self.onShowChatLogManager,
         'useTab': self.onUseTab,
         'solveTab': self.onSolveTab,
         'getTabTips': self.onGetTabTips,
         'chooseCmd': self.onChooseCmd,
         'setCommandData': self.onSetCommandData,
         'chatCommand': self.onChatCommand,
         'getDefaultChatList': self.onGetDefaultChatList,
         'getChannelIdByIconId': self.onGetChannelIdByIconId,
         'showSoundSetting': self.onShowSoundSetting,
         'startSoundRecord': self.onStartSoundRecord,
         'endSoundRecord': self.onEndSoundRecord,
         'getSounndRecordHotkey': self.onGetSounndRecordHotkey,
         'addGuildPuzzle': self.onAddGuildPuzzle,
         'isOtherUIinput': self.onIsOtherUIinput}
        self.handlers = {}
        self.channeltab = copy.copy(INIT_CHAT_TABS)
        self.chatLog = {const.CHANNEL_TAB_MULTIPLE: [],
         const.CHANNEL_TAB_COMBAT: [],
         const.CHANNEL_TAB_SYSTEM: [],
         const.CHANNEL_TAB_SINGLE: [],
         const.CHANNEL_TAB_CUSTOM1: [],
         const.CHANNEL_TAB_CUSTOM2: [],
         const.CHANNEL_TAB_GROUP: []}
        self.chatHistory = ChatHistory()
        self.allChatLog = {}
        self.chatAdjustMc = None
        self.chatAdjustMediator = None
        self.chatLogWindowMC = None
        self.destroyOnHide = False
        self.transparency = const.CHAT_NO_TRANSPARENT
        self.chatConfigType = const.CHAT_NONE_TYPE
        self.channelConfigTab = const.CHANNEL_TAB_NONE
        self.channelDeleteTab = const.CHANNEL_TAB_NONE
        self.curChannel = const.CHAT_CHANNEL_VIEW
        self.currentTab = 1
        self.isHide = False
        self.msgBoxId = 0
        self.isInputAreaVisible = False
        self.worldExQueue = []
        self.worldExHideCallbackId = None
        self.worldExShowCallbackId = None
        self.lastWorldEx = 0
        self.lastWorldExMessage = ''
        self.lastWorldExMessageType = 0
        self.hasHelloWord = False
        self.prosecuteMsg = ''
        self.blockList = []
        self.teamBlockList = []
        self.resetProsecuteArg()
        self.openBarrage = True
        self.isCanHuanFu = True
        self.hasSendAnyousWorldMsg = False
        self.hasSendAnyousWorldExMsg = False
        self.hasSendAnyousCorssWorldEx = False
        self.hasSendAnyousWorldWarMsg = False
        self.hasSendAnyousWorldWarCampMsg = False
        self.chatManagerChannel = const.CHAT_CHANNEL_VIEW
        self.checkTime = 0
        self.useAnonymousType = const.NORMAL_CHAT_MSG
        self.initMsg = []
        self.cmdData = []
        self.firterCommandList = []
        self.chooseCmdLen = 1024
        self.chatRegDict = {}
        self.targetName = ''
        self.linkClickInfo = {}
        self.cacheMessages = []
        self.hasCache = False
        self.sendAllCacheMsgsMsgTimer = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHAT_LOG_MANAGER, self.hideChatLogManager)

    def resetProsecuteArg(self):
        self.chatChannelId = -1
        self.chatTimestamp = '0'
        self.chatMsg = ''

    def closeInput(self):
        if self.chatLogWindowMC:
            self.chatLogWindowMC.Invoke('closeInput')

    def openInput(self):
        if self.chatLogWindowMC:
            isHide = self.chatLogWindowMC.Invoke('isHide').GetBool()
            if not isHide:
                self.chatLogWindowMC.Invoke('openInput')

    def onChangeLaba(self, *args):
        gameglobal.rds.ui.changeLaba.toggle()

    def onSetInputAreaVisible(self, *arg):
        visible = bool(arg[3][0].GetBool())
        if self.isInputAreaVisible == visible:
            return
        self.isInputAreaVisible = visible
        uiUtils.setApState(visible)

    def onIsUIEnable(self, *arg):
        enable = gameglobal.rds.ui.enableUI and not bool(gameglobal.rds.ui.booth.boothRecord) and not gameglobal.rds.ui.questionnaire.widget
        return GfxValue(enable)

    def onIsOtherUIinput(self, *args):
        isWebInFocus = False
        if hasattr(CEFManager, 'isWebInFocus'):
            isWebInFocus = bool(CEFManager.isWebInFocus() and BigWorld.player().needCefFilterKey())
        return GfxValue(gameglobal.rds.ui.bInput or isWebInFocus)

    def enableCampChannel(self):
        p = BigWorld.player()
        return gameglobal.rds.configData.get('enableWingWorldWarCamp', False) and gameglobal.rds.configData.get('enableWingWorldCampLaba', False)

    def initConfigChannelId(self):
        self.configChannelId = []
        for channel in CCD.data:
            if CCD.data[channel]['config']:
                if not gameglobal.rds.configData.get('enableClan', False):
                    if channel == const.CHAT_CHANNEL_CLAN:
                        continue
                if channel == const.CHAT_CHANNEL_WING_WORLD_CAMP:
                    if not self.enableCampChannel():
                        continue
                if CCD.data[channel].get('disable', 0):
                    continue
                if channel == const.CHAT_CHANNEL_SECRET:
                    if not gameglobal.rds.configData.get('enableSecretChannel', False):
                        continue
                if channel == const.CHAT_CHANNEL_CROSS_CLAN_WAR and not gameglobal.rds.configData.get('enableCrossClanWarLaba', False):
                    continue
                if channel == const.CLIENT_CHANNEL_BATTLE_FIELD_ALL_SIDE:
                    continue
                if channel == const.CHAT_CHANNEL_MAP_GAME:
                    if not gameglobal.rds.configData.get('enableMapGame', False):
                        continue
                if channel == const.CHAT_CHANNEL_ANONYMITY:
                    if not gameglobal.rds.configData.get('enableChatAnonymity', False):
                        continue
                self.configChannelId.append(channel)

    def setLinkClickInfo(self, info):
        self.linkClickInfo = info

    def applyLinkClickInfo(self):
        if self.linkClickInfo:
            txt = self.linkClickInfo.pop('txt', '')
            btnIdx = self.linkClickInfo.pop('btnIdx', 0)
            gameglobal.rds.ui._onLinkClick(btnIdx, txt)
            self.linkClickInfo = {}

    def onRegisterChat(self, *arg):
        self.chatLogWindowMC = arg[3][0]
        self.setFontSize(AppSettings.get(keys.SET_UI_SCALEDATA_CHAT, 12.0))
        if BigWorld.player().inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            self.goToBattleField()
        if gameglobal.CURRENT_WINDOW_STYLE == gameglobal.WINDOW_STYLE_CHAT:
            gameglobal.rds.ui.extendChatBox.regisiterChatLog(self.chatLogWindowMC)
        else:
            self.applyLinkClickInfo()

    def _registerMediator(self, widgetId, mediator):
        if widgetId in (uiConst.WIDGET_CHAT_CONFIG, uiConst.WIDGET_EXTEND_CHAT_CONFIG):
            self.chatAdjustMediator = mediator
            self.initConfigChannelId()
        elif widgetId == uiConst.WIDGET_CHAT_LOG_MANAGER:
            channelList = []
            for channelId, value in CCD.data.items():
                if channelId == const.CHAT_CHANNEL_SECRET:
                    if not gameglobal.rds.configData.get('enableSecretChannel', False):
                        continue
                elif channelId == const.CHAT_CHANNEL_WING_WORLD_CAMP:
                    if not gameglobal.rds.configData.get('enableWingWorldWarCamp', False):
                        continue
                if value.get('saveSortId', None):
                    channelList.append({'channelId': channelId,
                     'channelName': value.get('chatName', ''),
                     'sortId': value.get('saveSortId', 1)})

            channelList.sort(key=lambda cData: cData.get('sortId', 0))
            return uiUtils.dict2GfxDict({'channel': self.chatManagerChannel,
             'channelList': channelList}, True)
        self.refreshChannel()
        if not self.chatRegDict:
            for id, cfg in CRRD.data.iteritems():
                self.chatRegDict[id] = re.compile(cfg.get('regStr', ''))

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_CHAT_LOG_MANAGER:
            self.hideChatLogManager()
        else:
            self.hide(self.destroyOnHide)

    def hideChatLogManager(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHAT_LOG_MANAGER)

    def refreshChannel(self):
        p = BigWorld.player()
        if p:
            self.worldChannel = [const.CHAT_CHANNEL_VIEW,
             const.CHAT_CHANNEL_SINGLE,
             const.CHAT_CHANNEL_TEAM,
             const.CHAT_CHANNEL_GROUP,
             const.CHAT_CHANNEL_GUILD,
             const.CHAT_CHANNEL_WORLD,
             const.CHAT_CHANNEL_WING_WORLD_WAR if p.inWingWarCity() else const.CHAT_CHANNEL_SPACE,
             const.CHAT_CHANNEL_SCHOOL,
             const.CHAT_CHANNEL_WORLD_EX,
             const.CHAT_CHANNEL_NEW_PLAYER,
             const.CHAT_CHANNEL_DIGONG_LINE,
             const.CHAT_CHANNEL_CLAN,
             const.CHAT_CHANNEL_CROSS_SERVER_WORLD_EX,
             const.CHAT_CHANNEL_WORLD_WAR,
             const.CHAT_CHANNEL_OB,
             const.CHAT_CHANNEL_ANONYMITY]
            if gameglobal.rds.configData.get('enableSecretChannel', False):
                self.worldChannel.append(const.CHAT_CHANNEL_SECRET)
            if gameglobal.rds.configData.get('enableCrossClanWarLaba', False):
                self.worldChannel.append(const.CHAT_CHANNEL_CROSS_CLAN_WAR)
            if gameglobal.rds.configData.get('enableWingWorldWarCampMode', False):
                self.worldChannel.append(const.CHAT_CHANNEL_WING_WORLD_CAMP)
            if p.mapID in const.FB_NO_MARRIAGE_HALL_SET:
                self.worldChannel.append(const.CHAT_CHANNEL_MARRIAGE_HALL)
            self.arenaChannel = (const.CHAT_CHANNEL_ARENA,
             const.CHAT_CHANNEL_SINGLE,
             const.CHAT_CHANNEL_TEAM,
             const.CHAT_CHANNEL_GROUP,
             const.CHAT_CHANNEL_GUILD,
             const.CHAT_CHANNEL_WORLD,
             const.CHAT_CHANNEL_SCHOOL,
             const.CHAT_CHANNEL_WORLD_EX,
             const.CHAT_CHANNEL_CROSS_SERVER_WORLD_EX,
             const.CHAT_CHANNEL_WORLD_WAR,
             const.CHAT_CHANNEL_OB)
            self.battleFieldChannel = (const.CHAT_CHANNEL_BATTLE_FIELD,
             const.CLIENT_CHANNEL_BATTLE_FIELD_ALL_SIDE,
             const.CHAT_CHANNEL_SINGLE,
             const.CHAT_CHANNEL_TEAM,
             const.CHAT_CHANNEL_GROUP,
             const.CHAT_CHANNEL_GUILD,
             const.CHAT_CHANNEL_WORLD,
             const.CHAT_CHANNEL_SCHOOL,
             const.CHAT_CHANNEL_WORLD_EX,
             const.CHAT_CHANNEL_CROSS_SERVER_WORLD_EX,
             const.CHAT_CHANNEL_WORLD_WAR,
             const.CHAT_CHANNEL_OB)
            if formula.spaceInWorld(BigWorld.player().spaceNo):
                self.configChannel = self.worldChannel

    def onSetCurrentTab(self, *arg):
        self.currentTab = int(arg[3][0].GetNumber())

    def onSetFontSize(self, *arg):
        fontSize = arg[3][0].GetNumber()
        self.setFontSize(fontSize)
        AppSettings[keys.SET_UI_SCALEDATA_CHAT] = fontSize
        AppSettings.save()

    def onMaxSize(self, *arg):
        if gameglobal.CURRENT_WINDOW_STYLE == gameglobal.WINDOW_STYLE_CHAT:
            return uiUtils.array2GfxAarry((200, 1000))
        return uiUtils.array2GfxAarry(SCD.data.get('chatMaxSize', [100, 190]))

    def onShowAction(self, *arg):
        if not gameglobal.rds.configData.get('enableNewEmotionPanel', False):
            gameglobal.rds.ui.skill.showGeneralSkill(1)
        else:
            gameglobal.rds.ui.emoteAction.show()

    def onShowGameMsg(self, *arg):
        BigWorld.player().showGameMsg(arg[3][0].GetNumber(), ())

    def setChatText(self, msgText):
        if msgText is None:
            return
        else:
            msgText = msgText + ' '
            if self.chatLogWindowMC != None:
                if len(re.compile(HTTP_LINK_REG, re.IGNORECASE).findall(self.chatLogWindowMC.Invoke('getText').GetString())) >= 3:
                    BigWorld.player().showGameMsg(GMDD.data.ITEM_SEND_LIMITED, ())
                    return
                self.chatLogWindowMC.Invoke('settfInput', GfxValue(gbk2unicode(msgText)))
                self.showView()
            return

    def showTooltip(self, tipsType, gfxTipData):
        if self.chatLogWindowMC != None:
            self.chatLogWindowMC.Invoke('showTooltip', (GfxValue(tipsType), gfxTipData))

    def showTeamTooltip(self, teamInfo):
        gfxTipData = teamInfo
        reqSchool = teamInfo['schoolReq']
        reqSchoolNameList = []
        for school in reqSchool:
            reqSchoolNameList.append(const.SCHOOL_DICT[school])

        schoolReqStr = string.join(reqSchoolNameList, gameStrings.TEXT_CHATPROXY_403)
        if len(reqSchool) == len(const.ALL_SCHOOLS):
            schoolReqStr = gameStrings.TEXT_CHATPROXY_405
        reqLv = '%d-%d' % (teamInfo['lvMin'], teamInfo['lvMax'])
        gfxTipData['reqSchoolText'] = schoolReqStr
        gfxTipData['reqLvText'] = reqLv
        maxNum = 50
        if teamInfo['groupType'] == 1:
            maxNum = 5
        numStr = '%d/%d' % (teamInfo['memberCount'], maxNum)
        gfxTipData['numsText'] = numStr
        for i in xrange(len(gfxTipData['memInfo'])):
            school = gfxTipData['memInfo'][i]['school']
            gfxTipData['memInfo'][i]['schoolName'] = uiConst.SCHOOL_FRAME_DESC.get(school, '')

        gfxTipData['memInfo'].sort(cmp=lambda x, y: cmp(not x['isHeader'], not y['isHeader']))
        self.showTooltip(const.CHAT_TIPS_TEAM, uiUtils.dict2GfxDict(gfxTipData, True))

    def reset(self):
        for id in range(0, len(self.channeltab)):
            self.chatLog[self.channeltab[id][0]] = []

        if hasattr(self, 'worldChannel'):
            self.configChannel = self.worldChannel
        self.handlers = {}
        self.chatAdjustMc = None
        self.chatAdjustMediator = None
        self.chatLogWindowMC = None
        if self.worldExShowCallbackId:
            BigWorld.cancelCallback(self.worldExShowCallbackId)
        if self.worldExHideCallbackId:
            BigWorld.cancelCallback(self.worldExHideCallbackId)
        self.lastWorldEx = 0
        self.lastWorldExMessage = ''
        self.lastWorldExMessageType = 0
        self.worldExQueue = []
        self.worldExHideCallbackId = None
        self.worldExShowCallbackId = None
        self.blockList = []
        self.hideWorldExMessage()
        self.openBarrage = True
        self.hasSendAnyousWorldMsg = False
        self.hasSendAnyousWorldExMsg = False
        self.hasSendAnyousCorssWorldEx = False
        self.hasSendAnyousWorldWarMsg = False
        self.hasSendAnyousWorldWarCampMsg = False
        self.useAnonymousType = const.NORMAL_CHAT_MSG
        self.allChatLog = {}
        self.chatManagerChannel = const.CHAT_CHANNEL_VIEW
        self.checkTime = 0
        self.initMsg = []
        self.targetName = ''
        self.linkClickInfo = {}

    def onCanCreateTab(self, *arg):
        if len(BigWorld.player().chatConfig.groupPos) >= 1:
            return GfxValue(False)
        else:
            return GfxValue(True)

    def onGetTransparency(self, *arg):
        return GfxValue(self.transparency)

    def onSetTransparency(self, *arg):
        self.transparency = arg[3][0].GetNumber()

    def onGetPadChannels(self, *arg):
        return self.getPadChannelsArr()

    def goToBattleField(self):
        self.refreshChannel()
        self.configChannel = self.battleFieldChannel
        self.updatePadChannels()
        self.setCurChannel(const.CHAT_CHANNEL_BATTLE_FIELD)

    def goToArena(self):
        self.refreshChannel()
        self.configChannel = self.arenaChannel
        self.updatePadChannels()
        self.setCurChannel(const.CHAT_CHANNEL_ARENA)

    def goToWorld(self):
        self.refreshChannel()
        self.configChannel = self.worldChannel
        self.updatePadChannels()
        if BigWorld.player().isInCrossClanWarStatus():
            self.setCurChannel(const.CHAT_CHANNEL_CROSS_CLAN_WAR)
        else:
            self.setCurChannel(const.CHAT_CHANNEL_VIEW)

    def goToMarriageHall(self):
        self.refreshChannel()
        self.configChannel = self.worldChannel
        self.updatePadChannels()
        self.setCurChannel(const.CHAT_CHANNEL_MARRIAGE_HALL)

    def goToWingWorldWar(self):
        self.refreshChannel()
        self.configChannel = self.worldChannel
        self.updatePadChannels()
        self.setCurChannel(const.CHAT_CHANNEL_WING_WORLD_WAR)

    def updatePadChannels(self):
        if self.chatLogWindowMC != None:
            self.chatLogWindowMC.Invoke('updatePadChannels', self.getPadChannelsArr())

    def getPadChannelsArr(self):
        ar = []
        i = 0
        for id in xrange(0, len(self.configChannel)):
            channelInfo = CCD.data.get(self.configChannel[id], {})
            name = channelInfo.get('chatName', '') + channelInfo.get('shortCommand', '')
            if self.checkChannelCanUse(self.configChannel[id]) == False:
                continue
            channelId = self.configChannel[id]
            if channelInfo:
                name = channelInfo.get('chatName', '') + channelInfo.get('shortCommand', '')
            else:
                name = ''
            log = {}
            log['id'] = str(channelId)
            log['label'] = name
            log['channelName'] = channelInfo.get('chatName', '')
            ar.append(log)
            i = i + 1

        return uiUtils.array2GfxAarry(ar, True)

    def resetLaba(self):
        if self.chatLogWindowMC:
            self.chatLogWindowMC.Invoke('resetChannel', ())

    def onGetChannels(self, *arg):
        self.channeltab = copy.copy(INIT_CHAT_TABS)
        p = BigWorld.player()
        if not gameglobal.rds.isSinglePlayer and p:
            for id in p.chatConfig.groupName:
                self.channeltab.append((p.chatConfig.groupPos[id], p.chatConfig.groupName[id]))

        ar = []
        for id in range(0, min(len(self.channeltab), MAX_CHANNEL_NUM)):
            info = {}
            info['id'] = str(str(self.channeltab[id][0]))
            info['label'] = self.channeltab[id][1]
            ar.append(info)

        return uiUtils.array2GfxAarry(ar, True)

    def onGetChannelData(self, *arg):
        idvalue = arg[3][0]
        idStr = idvalue.GetString()
        for id in range(0, len(self.channeltab)):
            if float(idStr) == self.channeltab[id][0]:
                return uiUtils.array2GfxAarry(self.getChatHis(self.channeltab[id][0]))

    def updateChannelTab(self, isDelete = False, isAdd = False):
        p = BigWorld.player()
        addTabId = 0
        self.channeltab = copy.copy(INIT_CHAT_TABS)
        for id in p.chatConfig.groupName:
            addTabId = p.chatConfig.groupPos[id]
            self.channeltab.append((p.chatConfig.groupPos[id], p.chatConfig.groupName[id]))

        movie = gameglobal.rds.ui.movie
        ar = movie.CreateArray()
        for id in range(0, len(self.channeltab)):
            name = self.channeltab[id][1]
            Logname = GfxValue(gbk2unicode(name))
            Logid = GfxValue(str(self.channeltab[id][0]))
            log = movie.CreateObject()
            log.SetMember('id', Logid)
            log.SetMember('label', Logname)
            ar.SetElement(id, log)

        if self.chatLogWindowMC != None:
            if isDelete:
                self.chatLogWindowMC.Invoke('updateChannelTab', (ar, GfxValue(self.channelDeleteTab), GfxValue(0)))
            elif isAdd:
                self.chatLogWindowMC.Invoke('updateChannelTab', (ar, GfxValue(0), GfxValue(addTabId)))
            else:
                self.chatLogWindowMC.Invoke('updateChannelTab', (ar, GfxValue(0), GfxValue(0)))

    def onCreateTab(self, *arg):
        p = BigWorld.player()
        if const.CHANNEL_TAB_CUSTOM1 in p.chatConfig.groupPos:
            self.channelConfigTab = const.CHANNEL_TAB_CUSTOM2
        else:
            self.channelConfigTab = const.CHANNEL_TAB_CUSTOM1
        self.chatConfigType = const.CHAT_CREATE_TYPE
        self.openChatConfig()

    def onConfigTab(self, *arg):
        p = BigWorld.player()
        self.channelConfigTab = int(arg[3][0].GetNumber())
        self.chatConfigType = const.CHAT_CONFIG_TYPE
        self.openChatConfig()

    def onDeleteTab(self, *arg):
        p = BigWorld.player()
        self.channelDeleteTab = int(arg[3][0].GetNumber())
        if self.channelDeleteTab == const.CHANNEL_TAB_CUSTOM1 and len(p.chatConfig.groupPos) == 2:
            for id in p.chatConfig.groupPos:
                if p.chatConfig.groupPos[id] == const.CHANNEL_TAB_CUSTOM2:
                    p.cell.configGroup(id, p.chatConfig.groupName[id], const.CHANNEL_TAB_CUSTOM1)
                    self.chatLog[const.CHANNEL_TAB_CUSTOM1] = self.chatLog[const.CHANNEL_TAB_CUSTOM2]
                    break

        for id in p.chatConfig.groupPos:
            if p.chatConfig.groupPos[id] == self.channelDeleteTab:
                p.cell.removeGroup(id)
                break

    def onUseTab(self, *args):
        tabId = int(args[3][0].GetNumber())
        path = keys.SET_UI_TABNOTIFY_ID + str(tabId)
        AppSettings[path] = 1
        self.updateConfigTab2Data()

    def onSolveTab(self, *args):
        tabId = int(args[3][0].GetNumber())
        path = keys.SET_UI_TABNOTIFY_ID + str(tabId)
        AppSettings[path] = 0
        self.updateConfigTab2Data()

    def onGetTabTips(self, *args):
        tabTips = SCD.data.get('chatTabTips', gameStrings.TEXT_CHATPROXY_633)
        return GfxValue(gbk2unicode(tabTips))

    def openChatConfig(self):
        if gameglobal.CURRENT_WINDOW_STYLE == gameglobal.WINDOW_STYLE_CHAT:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EXTEND_CHAT_CONFIG)
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHAT_CONFIG)

    def onCloseChatConfig(self, *arg):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHAT_CONFIG)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EXTEND_CHAT_CONFIG)
        self.channelConfigTab = const.CHANNEL_TAB_NONE
        self.channelDeleteTab = const.CHANNEL_TAB_NONE
        self.chatConfigType = const.CHAT_NONE_TYPE

    def isInitChannelTab(self, tabId):
        for tab in self.channeltab:
            if tabId == tab[0]:
                return True

        return False

    def tabId2Index(self, tabId):
        for index, tab in enumerate(self.channeltab):
            if tabId == tab[0]:
                return index

        return -1

    def onInitChatConfig(self, *arg):
        if self.chatConfigType == const.CHAT_NONE_TYPE:
            return
        movie = arg[0]
        configObj = movie.CreateObject()
        configObj.SetMember('configType', GfxValue(self.chatConfigType))
        if self.chatConfigType == const.CHAT_CONFIG_TYPE:
            if self.isInitChannelTab(self.channelConfigTab):
                index = self.tabId2Index(self.channelConfigTab)
                configObj.SetMember('tabName', GfxValue(gbk2unicode(self.channeltab[index][1])))
            else:
                configObj.SetMember('tabName', GfxValue(gbk2unicode(BigWorld.player().chatConfig.groupName[self.channelConfigTab])))
        ar = movie.CreateArray()
        i = 0
        for channel in CCD.data:
            if CCD.data[channel]['config']:
                if channel == const.CHAT_CHANNEL_CLAN:
                    if not gameglobal.rds.configData.get('enableClan', False):
                        continue
                if channel == const.CHAT_CHANNEL_WING_WORLD_CAMP:
                    if not self.enableCampChannel():
                        continue
                if CCD.data[channel].get('disable', 0):
                    continue
                if channel == const.CHAT_CHANNEL_SECRET:
                    if not gameglobal.rds.configData.get('enableSecretChannel', False):
                        continue
                if channel == const.CHAT_CHANNEL_CROSS_CLAN_WAR and not gameglobal.rds.configData.get('enableCrossClanWarLaba', False):
                    continue
                if channel == const.CLIENT_CHANNEL_BATTLE_FIELD_ALL_SIDE:
                    continue
                if channel == const.CHAT_CHANNEL_MAP_GAME:
                    if not gameglobal.rds.configData.get('enableMapGame', False):
                        continue
                if channel == const.CHAT_CHANNEL_ANONYMITY:
                    if not gameglobal.rds.configData.get('enableChatAnonymity', False):
                        continue
                channelObj = movie.CreateObject()
                channelObj.SetMember('channelName', GfxValue(gbk2unicode("<font color=\'%s\'>%s</font>" % (CCD.data[channel]['color'], CCD.data[channel]['comment']))))
                if self.chatConfigType == const.CHAT_CREATE_TYPE:
                    channelObj.SetMember('isselect', GfxValue(False))
                elif self.channelConfigTab in BigWorld.player().chatConfig.channelConfig and not BigWorld.player().chatConfig.channelConfig[self.channelConfigTab].get(channel, False):
                    channelObj.SetMember('isselect', GfxValue(False))
                else:
                    channelObj.SetMember('isselect', GfxValue(True))
                ar.SetElement(i, channelObj)
                i = i + 1

        configObj.SetMember('array', ar)
        return configObj

    def onConfirmConfig(self, *arg):
        ar = arg[3][0]
        for id in range(0, len(self.configChannelId)):
            if ar.GetElement(id):
                BigWorld.player().cell.configChannel(self.configChannelId[id], self.channelConfigTab, ar.GetElement(id).GetBool())

        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHAT_CONFIG)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EXTEND_CHAT_CONFIG)
        self.chatConfigType = const.CHAT_NONE_TYPE

    def onConfirmCreate(self, *arg):
        tabName = unicode2gbk(arg[3][0].GetString())
        ar = arg[3][1]
        p = BigWorld.player()
        pos = const.CHANNEL_TAB_CUSTOM1
        for id in p.chatConfig.groupPos:
            if p.chatConfig.groupPos[id] == const.CHANNEL_TAB_CUSTOM1:
                pos = const.CHANNEL_TAB_CUSTOM2
                break

        if len(tabName) > self.MAX_TAB_NAME or tabName == '':
            BigWorld.player().showGameMsg(GMDD.data.CHAT_TAB_NAME_LARGE, ())
        else:
            BigWorld.player().cell.configGroup(self.channelConfigTab, tabName, pos)
            if ar:
                for id in range(0, len(self.configChannelId)):
                    channelElement = ar.GetElement(id)
                    if channelElement:
                        BigWorld.player().cell.configChannel(self.configChannelId[id], self.channelConfigTab, channelElement.GetBool())

            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHAT_CONFIG)
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EXTEND_CHAT_CONFIG)
            self.chatLog[pos] = []
            self.chatConfigType = const.CHAT_NONE_TYPE

    def onRegisterMsgListener(self, *arg):
        self.handlers['Chat.onNewLogMessage'] = arg[3][0]
        p = BigWorld.player()
        if self.hasHelloWord:
            p.showGameMsg(GMDD.data.HELLO_WORD, ())
            self.hasHelloWord = False
        if self.initMsg:
            for parmams in self.initMsg:
                self.addMessage(*parmams)

            self.initMsg = []
        if self.sendAllCacheMsgsMsgTimer:
            BigWorld.cancelCallback(self.sendAllCacheMsgsMsgTimer)
        self.sendAllCacheMsgsMsgTimer = BigWorld.callback(0, self.sendAllCacheMsgsMsgs)

    def parseMessage(self, msg):
        msg = re.sub('</?TEXTFORMAT.*?>', '', msg, 0, re.DOTALL)
        msg = re.sub('</?P.*?>', '', msg, 0, re.DOTALL)
        msg = re.sub('</?B.*?>', '', msg, 0, re.DOTALL)
        msg = self.extractFontColor(msg)
        return msg

    def extractFontColor(self, msg):
        fontFormat = re.compile('<FONT(.+?)COLOR=(.{9})(.+?)>', re.DOTALL)
        msg = fontFormat.sub(FontColorAdd, msg)
        return msg

    def delFont(self, matchobj):
        return matchobj.group(1)

    def submitMessage(self, channelId, msg = '', toPlaneTxt = True):
        if self.chatLogWindowMC:
            if channelId in self.configChannel:
                if toPlaneTxt:
                    msg = richTextUtils.htmlToPlaneText(msg)
                self.chatLogWindowMC.Invoke('handleChannelBtn', GfxValue(channelId))
                self.sendMessage(channelId, msg)

    def sendMessage(self, channel, msg, originalMsg = '', chatTargetName = '', autoInput = False, add2History = True):
        p = BigWorld.player()
        self.firterCommandList = []
        msg = self.parseMessage(msg)
        add2History and self.chatHistory.insert(msg)
        reFormat = re.compile('<FONT COLOR=\"#FFFFE6\">(.*?)</FONT>', re.DOTALL)
        msg = reFormat.sub(self.delFont, msg)
        msg = re.compile('!\\$([0-9]{1})').sub('#\\1', msg)
        msg = re.compile('#([0-9]{1})').sub('!$\\1', msg, uiConst.CHAT_MAX_FACE_CNT)
        msg = re.compile('\"!\\$([A-Fa-f0-9]{6})\"').sub('\"#\\1\"', msg)
        self.chooseCmdLen = 1024
        self.getCurChannel()
        if self.isRightChannel(self.curChannel):
            for cmd in self.cmdData:
                funcName = cmd.get('funcName', '')
                cmdText = cmd.get('showName', '')
                cmdLink = cmd.get('httpLink', '')
                if cmdText in msg:
                    if funcName:
                        func = getattr(self, funcName, None)
                        if func:
                            cmdLink = cmdLink % func(p)
                        else:
                            gamelog.warning('@lvc not cmd Func', funcName)
                    msg = msg.replace(cmdText, cmdLink)

        if msg[0] == '$':
            if p.adminOnClient(msg):
                return
            else:
                tmpCmd = msg.split()[0][1:].lower()
                if tmpCmd in GM_CMD_NEED_TARGET_LOCKED:
                    if p.targetLocked is not None:
                        msg = '%s %d' % (msg, p.targetLocked.id)
                    else:
                        p.chatToGm(gameStrings.TEXT_CHATPROXY_829)
                        return
                elif tmpCmd == 'runscript':
                    script = msg[len('$runscript '):]
                    try:
                        self.doRunScript(script)
                    except ImportError:
                        pass

                    return
                p.cell.adminOnCell(msg)
                return
        elif p.gmMode == const.GM_MODE_OBSERVER and not p.inFightObserve():
            return
        if msg[0] == '%':
            script = msg[1:]
            try:
                self.doRunScript(script)
            except ImportError:
                pass
            else:
                return

        elif msg[0] == '/':
            if msg[1:].lower().strip() in const.CLIENT_CHAT_SPECIAL_CMD:
                msg = msg.strip()
                p.cell.execSpecialChatCommand(msg)
                return
        if (richTextUtils.isSysRichTxt(msg) or richTextUtils.isSysRichTxt(originalMsg)) and not autoInput:
            p.showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
            return
        else:
            bReplace = False
            msg = msg + ':role'
            origMsg = msg
            if channel != const.CHAT_CHANNEL_WORLD_EX and channel != const.CHAT_CHANNEL_CROSS_SERVER_WORLD_EX and channel != const.CHAT_CHANNEL_WORLD_WAR:
                isNormal, msg, bReplace = taboo.checkDisbWordEx(msg)
            else:
                isNormal = taboo.checkDisbWordNoReplace(msg)
            if not isNormal:
                p.showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
                p.cell.markTabooMsg(channel, origMsg, 2)
                return
            if bReplace:
                p.cell.markTabooMsg(channel, origMsg, 4)
            flag, msg = self._tabooCheck(channel, msg, chatTargetName)
            if not flag:
                if channel in [const.CHAT_CHANNEL_WORLD_EX, const.CHAT_CHANNEL_CROSS_SERVER_WORLD_EX, const.CHAT_CHANNEL_WORLD_WAR]:
                    p.showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
                    return
                if channel in [const.CHAT_CHANNEL_WORLD]:
                    p.popupMsg(p.id, msg)
                if channel == const.CHAT_CHANNEL_SINGLE:
                    self.addMessage(channel, msg, chatTargetName, False, True)
                else:
                    self.addMessage(channel, msg, p.realRoleName, False, True)
                return
            if taboo.checkMonitorWord(msg):
                if channel != const.CHAT_CHANNEL_SINGLE:
                    self._reportFontlibMonitor(channel, gameStrings.TEXT_BOOTHPROXY_694, msg, const.FONT_LIB_MONITOR_THIRD)
                    if channel == const.CHAT_CHANNEL_CROSS_SERVER_WORLD_EX or channel == const.CHAT_CHANNEL_WORLD_EX or channel == const.CHAT_CHANNEL_WORLD_WAR:
                        p.showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
                        return
            if not AppSettings.get(keys.SET_DISABLE_SEMANTICS_RECOGNITION, 0):
                if gameglobal.rds.configData.get('enableSemantics', False):
                    emoteChannels = SCD.data.get('emoteChannels', [const.CHAT_CHANNEL_VIEW, const.CHAT_CHANNEL_TEAM])
                    if channel in emoteChannels:
                        doEmote = False
                        for key in ED.data.keys():
                            emoteData = ED.data.get(key, {})
                            shortcommand = emoteData.get('shortcommand', {})
                            for command in shortcommand:
                                if msg.lower().startswith('/' + command.lower()) and gameglobal.rds.ui.emote.isEmoteVail(emoteData):
                                    p.wantToDoEmote(key)
                                    doEmote = True
                                    break

                            if doEmote:
                                return

            if gameglobal.rds.configData.get('enableChatMultiLanguage', False):
                msg = self.addLanguageTag(msg)
            if channel == const.CHAT_CHANNEL_WORLD:
                useType = self.useAnonymousType
                if useType == const.NORMAL_CHAT_MSG:
                    p.cell.chatToWorld(msg, useType)
                elif self.hasSendAnyousWorldMsg == True or useType == 0:
                    p.cell.chatToWorld(msg, useType)
                else:
                    itemId = SCD.data.get('WORLD_ANONYMOUS_ITEM_ID', 400006)
                    itemData = uiUtils.getItemData(itemId)
                    count = BigWorld.player().inv.countItemInPages(itemId, enableParentCheck=True)
                    if count > 1:
                        itemData['count'] = '%d/1' % count
                    else:
                        itemData['count'] = "<font color = \'#FB0000\'>%d/1</font>" % count
                    msgShow = uiUtils.getTextFromGMD(GMDD.data.CAN_USE_THIS_WORLD_ANONYMOUS_ITEM, gameStrings.TEXT_CHATPROXY_936)
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msgShow, Functor(self.sendWorldChat, msg, useType), itemData=itemData)
            elif channel == const.CHAT_CHANNEL_GROUP:
                if p.groupNUID == 0 or p.groupType != gametypes.GROUP_TYPE_RAID_GROUP:
                    p.showGameMsg(GMDD.data.CHAT_NOT_IN_GROUP, ())
                else:
                    p.cell.chatToGroup(msg)
            elif channel == const.CHAT_CHANNEL_TEAM:
                if p.groupNUID == 0 or p.groupType != gametypes.GROUP_TYPE_TEAM_GROUP and p.groupType != gametypes.GROUP_TYPE_RAID_GROUP:
                    p.showGameMsg(GMDD.data.CHAT_NOT_IN_TEAM, ())
                else:
                    p.cell.chatToTeamGroup(msg)
            elif channel == const.CHAT_CHANNEL_GUILD:
                if p.guildNUID:
                    toYixin = not richTextUtils.isSoundRecord(msg)
                    p.cell.chatToGuild(msg, toYixin)
                else:
                    p.showGameMsg(GMDD.data.CHAT_NOT_IN_GUILD, ())
            elif channel == const.CHAT_CHANNEL_SCHOOL:
                p.cell.chatToSchool(msg)
            elif channel == const.CHAT_CHANNEL_ARENA:
                p.cell.chatToArena(msg)
            elif channel == const.CHAT_CHANNEL_BATTLE_FIELD:
                p.cell.chatToBattleField(msg)
            elif channel == const.CLIENT_CHANNEL_BATTLE_FIELD_ALL_SIDE:
                p.cell.chatToBattleFieldAll(msg)
            elif channel == const.CHAT_CHANNEL_VIEW:
                p.cell.chatToView(msg, const.POPUP_MSG_SHOW_DURATION)
            elif channel == const.CHAT_CHANNEL_WORLD_EX or channel == const.CHAT_CHANNEL_CROSS_SERVER_WORLD_EX or channel == const.CHAT_CHANNEL_WORLD_WAR or channel == const.CHAT_CHANNEL_WING_WORLD_CAMP:
                gameglobal.rds.ui.changeLaba.checkCurLabaCanUse()
                if channel == const.CHAT_CHANNEL_WORLD_EX:
                    gameglobal.rds.ui.changeLaba.checkCurLabaCanUse()
                    labaId = BigWorld.player().operation.get('curLabaId', 0)
                elif channel == const.CHAT_CHANNEL_CROSS_SERVER_WORLD_EX:
                    labaId = 0
                    for labaInfoId in LCD.data:
                        if LCD.data[labaInfoId]['type'] == gametypes.LABA_CROSS_SERVER:
                            labaId = labaInfoId
                            break

                elif channel == const.CHAT_CHANNEL_WORLD_WAR:
                    labaId = 0
                    for labaInfoId in LCD.data:
                        if LCD.data[labaInfoId]['type'] == gametypes.LABA_WORLD_WAR:
                            labaId = labaInfoId
                            break

                elif channel == const.CHAT_CHANNEL_WING_WORLD_CAMP:
                    for labaInfoId in LCD.data:
                        if LCD.data[labaInfoId]['type'] == gametypes.LABA_WING_WORLD_CAMP:
                            labaId = labaInfoId
                            break

                useType = self.useAnonymousType
                if channel == const.CHAT_CHANNEL_WORLD_EX:
                    if self.hasSendAnyousWorldExMsg == True or useType == 0:
                        p.cell.chatToWorldEx(msg, labaId, useType, '')
                    else:
                        itemId = SCD.data.get('WORLD_EX_ANONYMOUS_ITEM_ID', 400006)
                        itemData = uiUtils.getItemData(itemId)
                        count = BigWorld.player().inv.countItemInPages(itemId, enableParentCheck=True)
                        if count > 1:
                            itemData['count'] = '%d/1' % count
                        else:
                            itemData['count'] = "<font color = \'#FB0000\'>%d/1</font>" % count
                        msgShow = uiUtils.getTextFromGMD(GMDD.data.CAN_USE_THIS_WORLD_EX_ANONYMOUS_ITEM, gameStrings.TEXT_CHATPROXY_936)
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msgShow, Functor(self.sendWorldExChat, msg, labaId, useType), itemData=itemData)
                elif channel == const.CHAT_CHANNEL_CROSS_SERVER_WORLD_EX:
                    if self.hasSendAnyousCorssWorldEx == True or useType == 0:
                        if useType == const.NORMAL_CHAT_MSG:
                            useType = const.CROSS_SERVER_NORMAL_CHAT_MSG
                        else:
                            useType = const.CROSS_SERVER_ANONYMOUS_CHAT_MSG
                        p.cell.chatToWorldEx(msg, labaId, useType, '')
                    else:
                        itemId = SCD.data.get('WORLD_EX_CROSS_ANONYMOUS_ITEM_ID', 400006)
                        itemData = uiUtils.getItemData(itemId)
                        count = BigWorld.player().inv.countItemInPages(itemId, enableParentCheck=True)
                        if count > 1:
                            itemData['count'] = '%d/1' % count
                        else:
                            itemData['count'] = "<font color = \'#FB0000\'>%d/1</font>" % count
                        if useType == const.NORMAL_CHAT_MSG:
                            useType = const.CROSS_SERVER_NORMAL_CHAT_MSG
                        else:
                            useType = const.CROSS_SERVER_ANONYMOUS_CHAT_MSG
                        msgShow = uiUtils.getTextFromGMD(GMDD.data.CAN_USE_THIS_CROSS_WORLD_EX_ANONYMOUS_ITEM, gameStrings.TEXT_CHATPROXY_936)
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msgShow, Functor(self.sendWorldExChat, msg, labaId, useType), itemData=itemData)
                elif channel == const.CHAT_CHANNEL_WORLD_WAR:
                    if self.hasSendAnyousWorldWarMsg == True or useType == 0:
                        if useType == const.NORMAL_CHAT_MSG:
                            useType = const.WORLD_WAR_NORMAL_CHAT_MSG
                        else:
                            useType = const.WORLD_WAR_ANONYMOUS_CHAT_MSG
                        p.cell.chatToWorldEx(msg, labaId, useType, '')
                    else:
                        itemId = SCD.data.get('WORLD_WAR_ANONYMOUS_ITEM_ID', 400006)
                        itemData = uiUtils.getItemData(itemId)
                        count = BigWorld.player().inv.countItemInPages(itemId, enableParentCheck=True)
                        if count > 1:
                            itemData['count'] = '%d/1' % count
                        else:
                            itemData['count'] = "<font color = \'#FB0000\'>%d/1</font>" % count
                        if useType == const.NORMAL_CHAT_MSG:
                            useType = const.WORLD_WAR_NORMAL_CHAT_MSG
                        else:
                            useType = const.WORLD_WAR_ANONYMOUS_CHAT_MSG
                        msgShow = uiUtils.getTextFromGMD(GMDD.data.CAN_USE_THIS_WORLD_WAR_ANONYMOUS_ITEM, gameStrings.TEXT_CHATPROXY_936)
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msgShow, Functor(self.sendWorldExChat, msg, labaId, useType), itemData=itemData)
                elif channel == const.CHAT_CHANNEL_WING_WORLD_CAMP:
                    if self.hasSendAnyousWorldWarCampMsg == True or useType == 0:
                        if useType == const.NORMAL_CHAT_MSG:
                            useType = const.WING_WORLD_CAMP_NORMAL_CHAT_MSG
                        else:
                            useType = const.WING_WORLD_CAMP_ANONYMOUS_CHAT_MSG
                        p.cell.chatToWorldEx(msg, labaId, useType, '')
                    else:
                        itemId = SCD.data.get('WORLD_WAR_CAMP_ANONYMOUS_ITEM_ID', 400006)
                        itemData = uiUtils.getItemData(itemId)
                        count = BigWorld.player().inv.countItemInPages(itemId, enableParentCheck=True)
                        if count > 1:
                            itemData['count'] = '%d/1' % count
                        else:
                            itemData['count'] = "<font color = \'#FB0000\'>%d/1</font>" % count
                        if useType == const.NORMAL_CHAT_MSG:
                            useType = const.WING_WORLD_CAMP_NORMAL_CHAT_MSG
                        else:
                            useType = const.WING_WORLD_CAMP_ANONYMOUS_CHAT_MSG
                        msgShow = uiUtils.getTextFromGMD(GMDD.data.CAN_USE_THIS_WORLD_WAR_CAMP_ANONYMOUS_ITEM, gameStrings.TEXT_CHATPROXY_936)
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msgShow, Functor(self.sendWorldExChat, msg, labaId, useType), itemData=itemData)
            elif channel == const.CHAT_CHANNEL_SPACE or channel == const.CHAT_CHANNEL_WING_WORLD_WAR:
                p.cell.chatToSpace(msg)
            elif channel == const.CHAT_CHANNEL_SINGLE:
                if not chatTargetName:
                    p.showGameMsg(GMDD.data.CHAT_TARGET_EMPTY, ())
                else:
                    self.addMessage(const.CHAT_CHANNEL_SINGLE, msg, chatTargetName, False, True)
                    p.cell.chatToOne(chatTargetName, msg)
            elif channel == const.CHAT_CHANNEL_NEW_PLAYER:
                if self.inLowLevelChannel():
                    p.cell.chatToNovice(msg)
                else:
                    p.showGameMsg(GMDD.data.CHAT_NOT_NOVICE, ())
            elif channel == const.CHAT_CHANNEL_DIGONG_LINE:
                if formula.spaceInMultiLine(p.spaceNo):
                    p.cell.chatToDiGongLine(msg)
                else:
                    p.showGameMsg(GMDD.data.CHAT_NOT_IN_DIGONG, ())
            elif channel == const.CHAT_CHANNEL_CLAN:
                if p.clanNUID:
                    p.cell.chatToClan(msg)
                else:
                    p.showGameMsg(GMDD.data.CLAN_NOT_JOINED_CLAN, ())
            elif channel == const.CHAT_CHANNEL_OB:
                if formula.spaceInAnnalReplay(p.spaceNo):
                    p.cell.chatToWingWorldXinMoAnnal(channel, msg)
                elif formula.canObserveFB(p.spaceNo):
                    p.cell.chatToObservers(msg)
                else:
                    p.showGameMsg(GMDD.data.NOT_IN_FIGHT_OBSERVE, ())
            elif channel == const.CHAT_CHANNEL_SECRET:
                if re.search(HTTP_LINK_REG, msg, re.IGNORECASE):
                    p.showGameMsg(GMDD.data.CAN_NOT_SEND_LINK_TO_SECRET, ())
                    return
                p.cell.chatToSecret(msg)
            elif channel == const.CHAT_CHANNEL_MARRIAGE_HALL:
                p.cell.chatToMarriageHall(msg)
            elif channel == const.CHAT_CHANNEL_CROSS_CLAN_WAR:
                labaId = uiConst.CROSS_CLAN_WAR_LABA_ID
                useType = const.CROSS_CLAN_WAR_NORMAL_CHAT_MSG if self.useAnonymousType == const.NORMAL_CHAT_MSG else const.CROSS_CLAN_WAR_ANONYMOUS_CHAT_MSG
                p.cell.chatToWorldEx(msg, labaId, useType, '')
            elif channel == const.CHAT_CHANNEL_ANONYMITY:
                p.cell.chatToAnonymity(msg)
            self.updateSendNicknameSign(msg)
            return

    def onSubmitMessage(self, *arg):
        msg = unicode2gbk(arg[3][1].GetString())
        if msg == '':
            return
        idNum = arg[3][0].GetNumber()
        channel = int(idNum)
        chatTargetName = ''
        if channel == const.CHAT_CHANNEL_SINGLE:
            chatTargetName = unicode2gbk(arg[3][2].GetString())
        try:
            originalMsg = unicode2gbk(arg[3][3].GetString())
        except:
            originalMsg = ''

        self.sendMessage(channel, msg, originalMsg, chatTargetName)

    def inLowLevelChannel(self):
        p = BigWorld.player()
        lowLevelList = SCD.data.get('NOVICE_CHANNEL_LEVEL', [])
        lowLevelList2 = SCD.data.get('NOVICE_CHANNEL_LEVEL_LOW', [])
        for i in xrange(len(lowLevelList)):
            if p.lv <= lowLevelList[i] and p.lv >= lowLevelList2[i]:
                return True

        return False

    def checkNeedPushMessage(self, msg):
        if time.time() - self.checkTime < 3600:
            return False
        else:
            yuyueLv = SCD.data.get('YU_YUE_LIMIT_LV', 45)
            if BigWorld.player().lv < yuyueLv:
                return False
            self.checkTime = time.time()
            hasMsg = False
            if hasattr(BigWorld.player(), 'fbMessageBoard') and BigWorld.player().fbMessageBoard != None:
                hasMsg = BigWorld.player().fbMessageBoard.publishType
            if hasMsg:
                return False
            what = re.sub(taboo.tabooFilter, '', msg)
            matchCodeList = FMBCD.data.get('matchCodeSS', [])
            for pattern in matchCodeList:
                if re.search(pattern, what):
                    return True

            return False

    def sendWorldChat(self, msg, useType):
        BigWorld.player().cell.chatToWorld(msg, useType)
        self.hasSendAnyousWorldMsg = True

    def sendWorldExChat(self, msg, labaId, useType):
        if useType in [const.CROSS_SERVER_NORMAL_CHAT_MSG, const.CROSS_SERVER_ANONYMOUS_CHAT_MSG]:
            self.hasSendAnyousCorssWorldEx = True
        elif useType in [const.WORLD_WAR_NORMAL_CHAT_MSG, const.WORLD_WAR_ANONYMOUS_CHAT_MSG]:
            self.hasSendAnyousWorldWarMsg = True
        elif useType in [const.WING_WORLD_CAMP_NORMAL_CHAT_MSG, const.WING_WORLD_CAMP_ANONYMOUS_CHAT_MSG]:
            self.hasSendAnyousWorldWarCampMsg = True
        else:
            self.hasSendAnyousWorldExMsg = True
        BigWorld.player().cell.chatToWorldEx(msg, labaId, useType, '')

    def _tabooCheck(self, channel, msg, chatTargetName = ''):
        p = BigWorld.player()
        match = richTextUtils.isVoice(msg, True)
        if match:
            newMsg = msg[len(match.group(0)):]
        else:
            newMsg = msg
        if channel in [const.CHAT_CHANNEL_WORLD,
         const.CHAT_CHANNEL_WORLD_EX,
         const.CHAT_CHANNEL_CROSS_SERVER_WORLD_EX,
         const.CHAT_CHANNEL_WORLD_WAR]:
            isNormal, newMsg = taboo.checkBWorld(newMsg)
            if not isNormal:
                self._reportFontlibMonitor(channel, gameStrings.TEXT_BOOTHPROXY_694, msg, const.FONT_LIB_MONITOR_WORLD)
                p.cell.markTabooMsg(channel, msg, 3)
                return (False, msg)
        elif channel == const.CHAT_CHANNEL_SINGLE:
            isNormal, newMsg = taboo.checkBSingle(newMsg)
            if not isNormal:
                self._reportFontlibMonitor(channel, chatTargetName, msg, const.FONT_LIB_MONITOR_MASK_SINGLE)
                p.cell.markTabooMsg(channel, msg, 3)
                return (False, msg)
        else:
            isNormal, newMsg = taboo.checkAllLvDisWorld(newMsg)
            if not isNormal:
                self._reportFontlibMonitor(channel, gameStrings.TEXT_BOOTHPROXY_694, msg, const.FONT_LIB_MONITOR_ALL_LEVEL_MASK)
                p.cell.markTabooMsg(channel, msg, 3)
                return (False, msg)
            if p.lv <= 30:
                isNormal, newMsg = taboo.checkBNewbie(newMsg)
                if not isNormal:
                    self._reportFontlibMonitor(channel, gameStrings.TEXT_BOOTHPROXY_694, msg, const.FONT_LIB_MONITOR_NEWBIE_MASK)
                    return (False, msg)
        return (True, msg)

    def _reportFontlibMonitor(self, channel, receiver, msg, mtype):
        p = BigWorld.player()
        p.base.reportFontlibMonitor(channel, receiver, msg, p.getServerTime(), mtype)

    def onIsNeedConfirm(self, *arg):
        return GfxValue(False)

    def confirmSubmit(self, msg):
        if self.chatLogWindowMC:
            self.chatLogWindowMC.Invoke('confirmSubmit')

    def chatToCurrentChannel(self, msg):
        if self.chatLogWindowMC:
            if len(msg) > uiConst.CHAT_CHAR_LENGTH:
                msg = msg[:uiConst.CHAT_CHAR_LENGTH]
            self.chatLogWindowMC.Invoke('submitText', GfxValue(gbk2unicode(msg), GfxValue(False)))

    def setFontSize(self, size):
        if self.chatLogWindowMC:
            self.chatLogWindowMC.Invoke('setFontSize', GfxValue(size))

    def doRunScript(self, script):
        if BigWorld.isPublishedVersion():
            raise ImportError
        import resmgrimport
        for imp in sys.meta_path:
            if type(imp) is not resmgrimport.ResMgrImporter:
                continue
            if 'qc' not in imp.path:
                imp.path.append('qc')
            break

        import qcutil
        qcutil.run(script)

    def formatProsecuteMsg(self, channelId, msg):
        now = utils.getNow()
        if channelId in (const.CHAT_CHANNEL_INFO,):
            msg = ''
        msg = str(now) + '|' + str(channelId) + '|' + str(msg).replace('&apos;', gameStrings.TEXT_CHATPROXY_1260)
        return msg.encode('hex')

    def decodeProsecuteMsg(self, prosecuteMsg):
        chatTimestamp = '0'
        chatChannelId = -1
        chatMsg = ''
        if prosecuteMsg:
            prosecuteMsg = prosecuteMsg.decode('hex')
        if prosecuteMsg.find('|') != -1:
            chatTimestamp, chatChannelId, chatMsg = prosecuteMsg.split('|', 2)
        return (chatTimestamp, chatChannelId, chatMsg)

    def formatMessage(self, channel, msg, name, isAction, isSelf, fromGuild = '', useType = 0, gbId = 0, icon = 0, labaId = 0, mingPaiId = 0, msgProperties = {}, chatToAll = False, extra = None):
        p = BigWorld.player()
        if channel == const.CHAT_CHANNEL_BATTLE_FIELD and chatToAll:
            channel = const.CLIENT_CHANNEL_BATTLE_FIELD_ALL_SIDE
        channelInfo = CCD.data.get(channel, None)
        isFireWork = False
        if name and gametypes.FIREWORK_LABA_GAP_STR in name:
            isFireWork = True
            icon = 525
        if isFireWork and useType != const.CROSS_SERVER_ANONYMOUS_CHAT_MSG:
            senderName, targetName = name.split(gametypes.FIREWORK_LABA_GAP_STR, 1)
        else:
            senderName = ''
            targetName = ''
        if channelInfo == None:
            color = '#ffffff'
            chatName = gameStrings.TEXT_CHATPROXY_1294
            canSend = 0
            return
        else:
            color = channelInfo.get('color', '#ffffff')
            if not icon:
                icon = channelInfo.get('icon', None)
            if icon:
                chatName = '!$' + str(icon)
            else:
                chatName = channelInfo.get('chatName')
            canSend = channelInfo.get('canSend', 0)
            if canSend:
                chatName = "<a href = \'event:%s\'>%s</a>" % ('channel' + str(channel), chatName)
            if useType == const.WORLD_PUZZLE_GM_MSG:
                color = SCD.data.get('GM_PUZZLE_COLOR', '#ff0000')
            elif useType == const.WORLD_HOF_QUIZ_GM_MSG:
                color = SCD.data.get('GM_HOF_QUIZ_COLOR', '#29b1cc')
            eventName1 = ''
            if msg[-5:] == ':role' or richTextUtils.isRedPacket(msg):
                if msg[-5:] == ':role':
                    msg = msg[:-5]
                if useType == const.NORMAL_CHAT_MSG and not self.isAnonymousChannel(channel):
                    eventName = 'role' + name
                    if isFireWork and useType != const.CROSS_SERVER_ANONYMOUS_CHAT_MSG:
                        eventName = 'role' + senderName
                        eventName1 = 'role' + targetName
                elif useType == const.ANONYMOUS_CHAT_MSG or self.isAnonymousChannel(channel):
                    eventName = 'anonymous' + str(gbId)
                    if isFireWork and useType != const.CROSS_SERVER_ANONYMOUS_CHAT_MSG:
                        eventName1 = 'role' + targetName
                elif useType in [const.CROSS_SERVER_NORMAL_CHAT_MSG, const.CROSS_SERVER_ANONYMOUS_CHAT_MSG]:
                    parseItem = utils.parseCanonicalCrossServerRoleName(name)
                    playerName = parseItem[1]
                    serverName = parseItem[0]
                    name = uiUtils.getTextFromGMD(GMDD.data.CROSS_LABA_USERNAME_FORMAT, '[%s]%s') % (serverName, playerName)
                    if useType == const.CROSS_SERVER_NORMAL_CHAT_MSG:
                        eventName = 'rCross' + playerName + ':' + serverName
                        if isFireWork and useType != const.CROSS_SERVER_ANONYMOUS_CHAT_MSG:
                            eventName = 'rCross' + senderName + ':' + serverName
                            eventName1 = 'rCross' + targetName + ':' + serverName
                    else:
                        eventName = 'anCross' + str(gbId) + ':' + serverName
                elif useType in const.CROSS_WORLD_WAR_MSG:
                    parseItem = utils.parseCanonicalCrossServerRoleName(name)
                    playerName = parseItem[1]
                    serverName = parseItem[0]
                    name = uiUtils.getTextFromGMD(GMDD.data.CROSS_LABA_USERNAME_FORMAT, '[%s]%s') % (serverName, playerName)
                    if useType == const.WORLD_WAR_NORMAL_CHAT_MSG:
                        eventName = 'rCross' + playerName + ':' + serverName
                        if isFireWork and useType != const.WORLD_WAR_ANONYMOUS_CHAT_MSG:
                            eventName = 'rCross' + senderName + ':' + serverName
                            eventName1 = 'rCross' + targetName + ':' + serverName
                    else:
                        eventName = 'anCross' + str(gbId) + ':' + serverName
                elif useType == const.PRE_DEFINED_MSG:
                    eventName = name
                    if labaId and LCD.data.get(labaId, {}).get('type', -1) == gametypes.LABA_TEMPLATE_SELF_SERVER:
                        eventName = 'role' + name
            else:
                eventName = name
            eventName = re.sub('<', '&lt;', eventName)
            if eventName1:
                eventName1 = re.sub('<', '&lt;', eventName1)
            name = re.sub('<', '&lt;', name)
            fromGuild = re.sub('<', '&lt;', fromGuild)
            qpId = QIPAO_ID
            if msg[-10:] == ':fromYixin':
                msg = msg[:-10]
                qpId = YIXIN_ID
                tag = '[<a href = \"event:imageLink'
                if msg[:27] != tag:
                    isNormal, msg = taboo.checkDisbWord(msg)
                    if not isNormal:
                        return
                    isNormal, msg = taboo.checkBSingle(msg)
            msg = msg.replace('#FFFFE6', color)
            if isAction:
                formatmsg = "<p><font color=\'%s\'>%s%s</font></p>" % (color, chatName, msg)
                return formatmsg
            realName = name
            if mingPaiId and not self.isAnonymousChannel(channel):
                name += richTextUtils.mingPaiRichText(mingPaiId)
            isFromsprite = 0
            if msgProperties:
                postId = msgProperties.get(gametypes.MSG_ATTR_WW_ARMY_POST_ID, 0)
                if (gameglobal.rds.configData.get('enableWorldWarArmy', False) or gameglobal.rds.configData.get('enableWingWorld', False)) and not self.isAnonymousChannel(channel):
                    postId = msgProperties.get(gametypes.MSG_ATTR_WW_ARMY_POST_ID, 0)
                    camp = msgProperties.get(gametypes.MSG_ATTR_WING_ARMY_CAMP_ID, 0)
                    if postId:
                        name = richTextUtils.wwArmyPostRichText(postId, camp) + name
                isFromsprite = msgProperties.get('spriteId', 0)
            if channel == const.CHAT_CHANNEL_SINGLE:
                isFriend = False
                friendGroup = 0
                for friendId in p.friend:
                    if p.friend[friendId].name == realName and not isFromsprite:
                        if p.friend[friendId].group == 0:
                            if p.friend[friendId].apprentice == True:
                                friendGroup = gametypes.FRIEND_GROUP_APPRENTICE
                        else:
                            friendGroup = p.friend[friendId].group
                            if friendGroup >= const.FRIEND_CUSTOM_GROUP_BEGIN:
                                friendGroup = gametypes.FRIEND_GROUP_FRIEND
                    if friendGroup == gametypes.FRIEND_GROUP_FRIEND or friendGroup == gametypes.FRIEND_GROUP_APPRENTICE:
                        isFriend = True

                egnoreTalkFlag = msgProperties and msgProperties.get(gametypes.MSG_ATTR_EGNORE_TALK_FLAG, 0)
                if not p._isSoul() and not egnoreTalkFlag:
                    if isFriend:
                        name = uiUtils.getTextFromGMD(GMDD.data.SINGLE_CHAT_FRIEND_NAME, '%s') % name
                    elif name == p.playerName and isSelf:
                        name = uiUtils.getTextFromGMD(GMDD.data.SINGLE_CHAT_SELF_NAME, '%s') % name
                    elif p.summonedSpriteInWorld and p.summonedSpriteInWorld.roleName == realName and isFromsprite:
                        name = uiUtils.getTextFromGMD(GMDD.data.SINGLE_CHAT_SPRITE_NAME, '%s') % name
                    else:
                        name = uiUtils.getTextFromGMD(GMDD.data.SINGLE_CHAT_ANYOUS_NAME, '%s') % name
                if egnoreTalkFlag:
                    if isSelf:
                        formatmsg = gameStrings.TEXT_CHATPROXY_1435 % (color,
                         chatName,
                         eventName,
                         self.formatProsecuteMsg(channel, msg),
                         name,
                         msg)
                    else:
                        formatmsg = gameStrings.TEXT_CHATPROXY_1437 % (color,
                         chatName,
                         eventName,
                         self.formatProsecuteMsg(channel, msg),
                         name,
                         msg)
                elif isSelf:
                    formatmsg = gameStrings.TEXT_CHATPROXY_1440 % (color,
                     chatName,
                     eventName,
                     self.formatProsecuteMsg(channel, msg),
                     name,
                     qpId,
                     msg)
                else:
                    formatmsg = gameStrings.TEXT_CHATPROXY_1442 % (color,
                     chatName,
                     eventName,
                     self.formatProsecuteMsg(channel, msg),
                     name,
                     qpId,
                     msg)
            elif channel == const.CHAT_CHANNEL_CLAN:
                if len(name) > 0:
                    useName = uiUtils.getTextFromGMD(GMDD.data.CLAN_CHANNEL_NAME_TITLE, gameStrings.TEXT_CHATPROXY_1446)
                    useName = useName % (fromGuild, name)
                    formatmsg = "<p><font color=\'%s\'>%s<a href = \'event:%s$%s\'><u>%s</u></a>%s%s</font></p>" % (color,
                     chatName,
                     eventName,
                     self.formatProsecuteMsg(channel, msg),
                     useName,
                     qpId,
                     msg)
                else:
                    formatmsg = "<p><font color=\'%s\'>%s%s</font></p>" % (color, chatName, msg)
            elif channel == const.CHAT_CHANNEL_GUILD:
                if len(name) > 0:
                    guildPrivilegesName = self.getGuildPrivilegesName(name, mingPaiId)
                    formatmsg = "<p><font color=\'%s\'>%s%s<a href = \'event:%s$%s\'><u>%s</u></a>%s%s</font></p>" % (color,
                     chatName,
                     guildPrivilegesName,
                     eventName,
                     self.formatProsecuteMsg(channel, msg),
                     name,
                     qpId,
                     msg)
                else:
                    formatmsg = "<p><font color=\'%s\'>%s%s</font></p>" % (color, chatName, msg)
            elif channel == const.CHAT_CHANNEL_SCHOOL:
                if len(name) > 0:
                    schoolPrivilegesName = self.getSchoolPrivilegesName(extra)
                    formatmsg = "<p><font color=\'%s\'>%s%s<a href = \'event:%s$%s\'><u>%s</u></a>%s%s</font></p>" % (color,
                     chatName,
                     schoolPrivilegesName,
                     eventName,
                     self.formatProsecuteMsg(channel, msg),
                     name,
                     qpId,
                     msg)
                else:
                    formatmsg = "<p><font color=\'%s\'>%s%s</font></p>" % (color, chatName, msg)
            elif len(name) > 0:
                if channel in [const.CHAT_CHANNEL_VIEW, const.CHAT_CHANNEL_GROUP]:
                    if isFromsprite:
                        name = uiUtils.getTextFromGMD(GMDD.data.SINGLE_CHAT_SPRITE_NAME, '%s') % name
                if useType == 0:
                    if isFireWork and useType != const.CROSS_SERVER_ANONYMOUS_CHAT_MSG:
                        prosecuteMsg = self.formatProsecuteMsg(channel, msg)
                        formatmsg = gameStrings.TEXT_CHATPROXY_1475 % (color,
                         chatName,
                         eventName,
                         prosecuteMsg,
                         senderName,
                         eventName1,
                         prosecuteMsg,
                         targetName,
                         qpId,
                         msg)
                    else:
                        formatmsg = "<p><font color=\'%s\'>%s<a href = \'event:%s$%s\'><u>%s</u></a>%s%s</font></p>" % (color,
                         chatName,
                         eventName,
                         self.formatProsecuteMsg(channel, msg),
                         name,
                         qpId,
                         msg)
                elif isFireWork and useType != const.CROSS_SERVER_ANONYMOUS_CHAT_MSG:
                    prosecuteMsg = self.formatProsecuteMsg(channel, msg)
                    formatmsg = gameStrings.TEXT_CHATPROXY_1475 % (color,
                     chatName,
                     eventName,
                     prosecuteMsg,
                     senderName,
                     eventName1,
                     prosecuteMsg,
                     targetName,
                     qpId,
                     msg)
                else:
                    formatmsg = "<p><font color=\'%s\'>%s<a href = \'event:%s$%s\'><u>%s</u></a>%s%s</font></p>" % (color,
                     chatName,
                     eventName,
                     self.formatProsecuteMsg(channel, msg),
                     name,
                     qpId,
                     msg)
            else:
                formatmsg = "<p><font color=\'%s\'>%s%s</font></p>" % (color, chatName, msg)
            return formatmsg

    def getGuildPrivilegesName(self, name, mingPaiId):
        if not gameglobal.rds.configData.get('enableShowGuildPrivilegesInChat', False):
            return ''
        p = BigWorld.player()
        if not p.guild:
            return ''
        if mingPaiId and not self.isAnonymousChannel(const.CHAT_CHANNEL_GUILD):
            mingPaiStr = richTextUtils.mingPaiRichText(mingPaiId)
            realName = name[:name.find(mingPaiStr)]
        else:
            realName = name
        for member in p.guild.member.itervalues():
            if member.role == realName:
                return '[%s]' % gametypes.GUILD_PRIVILEGES.get(member.roleId, {}).get('name', '')

        return ''

    def getSchoolPrivilegesName(self, extra):
        if extra and extra.get('isSchoolTop', False):
            return gameStrings.SCHOOL_TOP_CHAT_WINDOW_PREFIX
        return ''

    def isBlock(self, name):
        p = BigWorld.player()
        if name in p.friend.getGroupMembersName(gametypes.FRIEND_GROUP_BLOCK):
            return True
        if name in p.friend.getGroupMembersName(gametypes.FRIEND_GROUP_BLOCK_ENEMY):
            return True
        if name in self.blockList:
            return True
        return False

    def isTeamBlock(self, teamId):
        if str(teamId) in self.teamBlockList:
            return True
        else:
            return False

    def updateSendNicknameSign(self, msg):
        p = BigWorld.player()
        if p.friend.intimacyTgt == 0:
            return
        tgtNickName = p.intimacyTgtNickName
        if not tgtNickName:
            return
        if msg.find(tgtNickName) == -1:
            return
        p.isSendIntimacyNickname = True

    def checkTgtNickname(self, channelId, msg, name):
        if not gameglobal.rds.configData.get('enableIntimacyTgtNickName', False):
            return
        checkChannelList = SCD.data.get('checkJieQiNickNameChannel', [])
        if channelId in checkChannelList:
            p = BigWorld.player()
            if not p.isSendIntimacyNickname:
                return
            p.isSendIntimacyNickname = False
            if p.friend.intimacyTgt == 0:
                return
            tgtNickName = p.intimacyTgtNickName
            if not tgtNickName:
                return
            if msg.find(tgtNickName) == -1:
                return
            p.base.notifyIntimacyTgtShowIntimate(msg)
            fVal = p.getFValByGbId(p.friend.intimacyTgt)
            tgtJieQiName = ''
            if fVal:
                tgtJieQiName = fVal.name
            if channelId == const.CHAT_CHANNEL_SINGLE:
                if name != tgtJieQiName:
                    desc = '%s:role' % gameStrings.JIEQI_TO_CALL_NICKNAME
                    desc = utils.encodeMsgHeader(desc, {gametypes.MSG_ATTR_EGNORE_TALK_FLAG: 1})
                    p.cell.chatToOne(tgtJieQiName, desc)
            elif channelId == const.CHAT_CHANNEL_TEAM or channelId == const.CHAT_CHANNEL_GROUP:
                if p.friend.intimacyTgt not in p.members:
                    desc = '%s:role' % gameStrings.JIEQI_TO_CALL_NICKNAME
                    desc = utils.encodeMsgHeader(desc, {gametypes.MSG_ATTR_EGNORE_TALK_FLAG: 1})
                    p.cell.chatToOne(tgtJieQiName, desc)

    def addMessage(self, channelId, msg, name, isAction = False, isSelf = False, fromGuild = '', labaId = 0, useType = 0, gbId = 0, icon = 0, mingpaiId = 0, msgProperties = None, chatToAll = False, extra = None):
        self.checkTgtNickname(channelId, msg, name)
        if CCD.data[channelId].get('disable', 0):
            channelId = CCD.data[channelId].get('combinedToChannelId', 0)
        if self.handlers.get('Chat.onNewLogMessage', None) is None:
            self.initMsg.append((channelId,
             msg,
             name,
             isAction,
             isSelf,
             fromGuild,
             labaId,
             useType,
             gbId,
             icon,
             mingpaiId))
            return
        else:
            if not msgProperties:
                msgProperties, msg = utils.decodeMsgHeader(msg)
            if msgProperties:
                if msgProperties.get('teamId', 0):
                    if self.isTeamBlock(msgProperties.get('teamId', 0)):
                        return
            p = BigWorld.player()
            if not isSelf and self.isBlock(name):
                return
            if self.checkLanguageBlock(msg, msgProperties, channelId):
                return
            if msg.find(uiConst.CHAT_MESSAGE_SEPARATOR) > 0:
                msg = self.generateMsg(msg)
                if not msg:
                    return
            msg = self.chatMsgReg(msg, name, gbId, int(channelId))
            msg = richTextUtils.parseSysTxt(msg)
            channel = int(channelId)
            if channel in (const.CHAT_CHANNEL_SPACE,
             const.CHAT_CHANNEL_DIGONG_LINE,
             const.CHAT_CHANNEL_GUILD,
             const.CHAT_CHANNEL_OB,
             const.CHAT_CHANNEL_BATTLE_FIELD,
             const.CHAT_CHANNEL_ARENA,
             const.CHAT_CHANNEL_MARRIAGE_HALL):
                if self.canSendBarrage(channel, msg):
                    colorData = SCD.data.get('barrageColorDict', {})
                    if colorData:
                        needAddRole = False
                        if msg[-5:] == ':role':
                            msg = msg[:-5]
                            needAddRole = True
                        reStr = '#['
                        for key in colorData:
                            reStr += key.lower()
                            reStr += key

                        reStr += ']'
                        msgList = re.split(reStr, msg)
                        cpMsgList = copy.deepcopy(msgList)
                        colorList = re.findall(reStr, msg)
                        for i in xrange(0, len(colorList)):
                            colorName = colorList[i].upper()
                            color = colorData.get(colorName)
                            if color:
                                if i + 1 >= len(msgList):
                                    continue
                                testMsg = "<font color=\'%s\'>%s</font>" % (color, msgList[i + 1])
                                cpMsgList[i + 1] = testMsg

                        msg = ''
                        barrageMsg = ''
                        for i in xrange(0, len(msgList)):
                            msg = msg + msgList[i]
                            barrageMsg = barrageMsg + cpMsgList[i]

                        self.addBarrageMsg(barrageMsg, name)
                        if needAddRole:
                            msg = msg + ':role'
                    else:
                        self.addBarrageMsg(msg, name)
            try:
                fmsg = self.formatMessage(channel, msg, name, isAction, isSelf, fromGuild, useType, gbId, icon, labaId, mingpaiId, msgProperties=msgProperties, chatToAll=chatToAll, extra=extra)
            except:
                fmsg = ''

            if not fmsg:
                return
            if channel in (const.CHAT_CHANNEL_WORLD_EX,
             const.CHAT_CHANNEL_CROSS_SERVER_WORLD_EX,
             const.CHAT_CHANNEL_WORLD_WAR,
             const.CHAT_CHANNEL_CROSS_CLAN_WAR):
                self.addWorldExMessage(fmsg, name, labaId)
            self.addMsgToArr(channelId, fmsg)
            channel = const.CHAT_CHANNEL_SPACE if channel == const.CHAT_CHANNEL_WING_WORLD_WAR else channel
            fmsg = gbk2unicode(fmsg)
            for id, _ in self.channeltab:
                if id in p.chatConfig.channelConfig and p.chatConfig.channelConfig[id].get(channel, False):
                    if id in p.chatConfig.groupPos:
                        self.addChatHis(p.chatConfig.groupPos[id], fmsg, name)
                        self.setNewLogMessage(p.chatConfig.groupPos[id], fmsg)
                    else:
                        self.addChatHis(id, fmsg, name)
                        self.setNewLogMessage(id, fmsg)

            if channel == const.CHAT_CHANNEL_SINGLE and not isSelf:
                gameglobal.rds.sound.playSound(gameglobal.SD_415)
            return

    def generateMsg(self, msg):
        p = BigWorld.player()
        sprLen = len(uiConst.CHAT_MESSAGE_SEPARATOR)
        index = msg.find(uiConst.CHAT_MESSAGE_SEPARATOR)
        type = int(msg[:index])
        msg = msg[index + sprLen:]
        if type == uiConst.CME_TYPE_SHARE_TEAM:
            index = msg.find(uiConst.CHAT_MESSAGE_SEPARATOR)
            content = msg[:index]
            msg = msg[index + sprLen:]
            index = msg.find(uiConst.CHAT_MESSAGE_SEPARATOR)
            pList = []
            while index >= 0:
                param = msg[:index]
                pList.append(param)
                msg = msg[index + sprLen:]
                index = msg.find(uiConst.CHAT_MESSAGE_SEPARATOR)

            color = '#ffec73'
            colorLink = '#55bdff'
            msgTeam = uiUtils.toHtml(pList[0], linkEventTxt='teamInfo%s' % pList[1])
            goalDesc = uiUtils.toHtml(pList[2], color=color)
            lvMin, lvMax = tuple(eval(pList[3]))
            msgLv = uiUtils.toHtml(gameStrings.SHARE_TEAM_INFO_LV_LIMIT % (lvMin, lvMax), color=color)
            jobReq = list(eval(pList[4]))
            msgInvite = uiUtils.toHtml('%s' % pList[5], color=colorLink, linkEventTxt='applyTeam%s' % pList[6])
            msgTeam2 = uiUtils.toHtml(gameStrings.TEXT_COMPOSITESHOPHELPFUNC_660 % msgInvite, color=colorLink)
            if not p.groupNUID or str(p.groupNUID) != pList[1]:
                if p.lv < lvMin or p.lv > lvMax or jobReq and p.school not in jobReq:
                    return
            if jobReq:
                jobReg = []
                for jobId in jobReq:
                    jobReg.append('[job.%d]' % jobId)

                msgJob = ''.join(jobReg)
                content = content % (msgTeam,
                 goalDesc,
                 msgLv,
                 msgJob,
                 msgTeam2)
            else:
                content = content % (msgTeam,
                 goalDesc,
                 msgLv,
                 msgTeam2)
            return content

    def addMsgToArr(self, channelId, msg):
        if self.allChatLog.has_key(channelId):
            logs = self.allChatLog.get(channelId)
        else:
            logs = []
            self.allChatLog[channelId] = logs
        if len(logs) >= SCD.data.get('maxSaveLogNum', 1000):
            logs.pop(0)
        logs.append(msg)

    def canSendBarrage(self, channel, msg):
        if not gameglobal.rds.configData.get('enableBarrage', False):
            return False
        if channel == const.CHAT_CHANNEL_GUILD and msg[-5:] != ':role':
            return False
        wenquanLineNo = SCD.data.get('barrageOpenSpace', (151,))
        p = BigWorld.player()
        mapId = formula.getMLGNo(p.spaceNo)
        if not mapId:
            mapId = formula.getMapId(p.spaceNo)
        if mapId in wenquanLineNo:
            if channel == const.CHAT_CHANNEL_GUILD and mapId != const.GUILD_SCENE_NO:
                return False
            if channel == const.CHAT_CHANNEL_SPACE:
                return False
            return True
        if mapId in QBCD.data.keys():
            if channel == const.CHAT_CHANNEL_SPACE:
                return True
        if formula.canObserveFB(p.spaceNo):
            if channel == const.CHAT_CHANNEL_OB:
                if p.inFightObserve():
                    return True
        if p.getArenaMode() in const.ARENA_CHALLENDE_MODE_LIST or utils.inLiveOfArenaPlayoffs(p):
            if channel == const.CHAT_CHANNEL_ARENA and msg[-5:] == ':role':
                return True
        if p.mapID in const.FB_NO_MARRIAGE_HALL_SET:
            if channel == const.CHAT_CHANNEL_MARRIAGE_HALL:
                return True
        if formula.spaceInAnnalReplay(p.spaceNo) and channel == const.CHAT_CHANNEL_OB:
            return True
        return False

    def addBarrageMsg(self, msg, name):
        nowMsg = msg
        if msg[-5:] == ':role':
            nowMsg = msg[:-5]
        if nowMsg[-10:] == ':fromYixin':
            nowMsg = nowMsg[:-10]
            tag = '[<a href = \"event:imageLink'
            if nowMsg[:27] != tag:
                isNormal, nowMsg = taboo.checkDisbWord(nowMsg)
                if not isNormal:
                    return
                isNormal, nowMsg = taboo.checkBSingle(nowMsg)
        if self.chatLogWindowMC:
            if self.openBarrage:
                isMy = False
                if name == BigWorld.player().roleName:
                    isMy = True
                gameglobal.rds.ui.barrage.addBarrageMsg(nowMsg, isMy)

    def onSetOpenBarrage(self, *args):
        self.openBarrage = args[3][0].GetBool()
        if not self.openBarrage:
            gameglobal.rds.ui.barrage.closeBullet()

    def onSetAnonymous(self, *args):
        ret = args[3][0].GetBool()
        if ret:
            self.useAnonymousType = const.ANONYMOUS_CHAT_MSG
        else:
            self.useAnonymousType = const.NORMAL_CHAT_MSG

    def onSaveSelect(self, *args):
        try:
            channelId = int(args[3][0].GetNumber())
            if not self.allChatLog.get(channelId):
                BigWorld.player().showGameMsg(GMDD.data.SAVE_CHAT_LOG_EMPTY, ())
            else:
                self.saveChatLog([channelId])
                self.hideChatLogManager()
        except:
            gamelog.error('@zhp save log Error', args[3][0].GetString())

    def onSaveAllLog(self, *args):
        self.saveChatLog()
        self.hideChatLogManager()

    def onGetChatLogs(self, *args):
        try:
            channelId = int(args[3][0].GetNumber())
            self.chatManagerChannel = channelId
            return uiUtils.array2GfxAarry(self.allChatLog.get(channelId, []), True)
        except:
            gamelog.error('@zhp get log Error', args[3][0].GetString())

    def onShowChatLogManager(self, *args):
        self.uiAdapter.loadWidget(uiConst.WIDGET_CHAT_LOG_MANAGER)

    def setBottomButton(self):
        wenquanLineNo = SCD.data.get('barrageOpenSpace', (151,))
        showBarrage = False
        p = BigWorld.player()
        mapId = formula.getMLGNo(p.spaceNo)
        if not mapId:
            mapId = formula.getMapId(p.spaceNo)
        if mapId in wenquanLineNo:
            showBarrage = True
        if mapId in QBCD.data.keys():
            showBarrage = True
        if formula.canObserveFB(p.spaceNo) and p.inFightObserve():
            showBarrage = True
        if p.getArenaMode() in const.ARENA_CHALLENDE_MODE_LIST:
            showBarrage = True
            self.openBarrage = False
        if utils.inLiveOfArenaPlayoffs(p):
            showBarrage = True
            self.openBarrage = True
        if p.mapID in const.FB_NO_MARRIAGE_HALL_SET:
            showBarrage = True
            self.openBarrage = True
        if not gameglobal.rds.configData.get('enableBarrage', False):
            showBarrage = False
        if formula.spaceInAnnalReplay(p.spaceNo):
            showBarrage = True
            self.openBarrage = True
        if showBarrage:
            gameglobal.rds.ui.barrage.show()
        else:
            gameglobal.rds.ui.barrage.clearWidget()
        canShowAnonymous = True
        isShowSoundRecord = p.enableSoundRecord()
        self.isCanHuanFu = True
        if self.chatLogWindowMC:
            self.chatLogWindowMC.Invoke('setBottomButton', (GfxValue(self.isCanHuanFu),
             GfxValue(showBarrage),
             GfxValue(self.openBarrage),
             GfxValue(self.useAnonymousType),
             GfxValue(canShowAnonymous),
             GfxValue(isShowSoundRecord)))

    def addWorldExMessage(self, fmsg, name, type = 0):
        self.worldExQueue.append((fmsg, name, type))
        if self.worldExHideCallbackId:
            BigWorld.cancelCallback(self.worldExHideCallbackId)
        lType = LCD.data.get(self.lastWorldExMessageType, {}).get('type')
        if lType == gametypes.LABA_CROSS_SERVER or lType == gametypes.LABA_WORLD_WAR:
            lastIsCrossLaba = True
        else:
            lastIsCrossLaba = False
        if len(self.worldExQueue) == 1:
            if lastIsCrossLaba == True:
                canShowTime = SCD.data.get('crossWorldExMinInterval', 20)
            else:
                canShowTime = SCD.data.get('worldExMinInterval', 5)
            if utils.getNow() - self.lastWorldEx >= canShowTime:
                self.showWorldExMessage()
            else:
                self.worldExShowCallbackId = BigWorld.callback(canShowTime + self.lastWorldEx - utils.getNow(), self.showWorldExMessage)
        elif len(self.worldExQueue) > SCD.data.get('worldExListMaxLength', 100):
            if self.worldExShowCallbackId:
                BigWorld.cancelCallback(self.worldExShowCallbackId)
            self.showWorldExMessage()

    def showWorldExMessage(self):
        if gameglobal.CURRENT_WINDOW_STYLE == gameglobal.WINDOW_STYLE_CHAT:
            return
        if self.chatLogWindowMC and len(self.worldExQueue):
            findCross = False
            for i in xrange(len(self.worldExQueue)):
                labaId = self.worldExQueue[i][2]
                severName = utils.parseCanonicalCrossServerRoleName(self.worldExQueue[i][1])[0]
                if LCD.data.get(labaId, {}).get('type') == gametypes.LABA_CROSS_SERVER and severName == gameglobal.gServerName:
                    findCross = True
                    outItem = self.worldExQueue.pop(i)
                    break

            if findCross == False:
                outItem = self.worldExQueue.pop(0)
            msg = outItem[0]
            msgType = outItem[2]
            swfName = self.getWorldExMessageSwfName(msgType)
            title = self.getWorldExMessageTitle(msgType)
            self.lastWorldEx = utils.getNow()
            self.lastWorldExMessage = msg
            self.lastWorldExMessageType = msgType
            if LCD.data.get(msgType, {}).get('type') == gametypes.LABA_CROSS_SERVER:
                isCrossLaba = True
            else:
                isCrossLaba = False
            msgColor = LCD.data.get(labaId, {}).get('color')
            if msgColor:
                replace = "color=\'%s\'" % msgColor
                msgContent = re.subn("color=\'([^\']*)\'", replace, msg, 1)
                if len(msgContent):
                    msg = msgContent[0]
            self.chatLogWindowMC.Invoke('showWorldExMessage', (GfxValue(gbk2unicode(msg)), GfxValue(gbk2unicode(swfName)), GfxValue(gbk2unicode(title))))
            if len(self.worldExQueue):
                showTime = LCD.data.get(msgType, {}).get('showMinTime')
                if isCrossLaba == False:
                    if not showTime:
                        showTime = SCD.data.get('worldExMinInterval', 5)
                elif not showTime:
                    showTime = SCD.data.get('crossWorldExMinInterval', 20)
                self.worldExShowCallbackId = BigWorld.callback(showTime, self.showWorldExMessage)
            else:
                showTime = LCD.data.get(msgType, {}).get('showMaxTime')
                if isCrossLaba == False:
                    if not showTime:
                        showTime = SCD.data.get('worldExMaxInterval', 60)
                elif not showTime:
                    showTime = SCD.data.get('crossWorldExMaxInterval', 120)
                self.worldExShowCallbackId = BigWorld.callback(showTime, self.hideWorldExMessage)

    def getWorldExMessageSwfName(self, type = 0):
        data = LCD.data.get(type, {})
        return data.get('swfName', 'Laba_001.swf')

    def getWorldExMessageTitle(self, type = 0):
        data = LCD.data.get(type, {})
        return data.get('title', '')

    def hideWorldExMessage(self):
        self.lastWorldExMessage = ''
        self.lastWorldExMessageType = 0
        if self.chatLogWindowMC:
            self.chatLogWindowMC.Invoke('hideWorldExMessage')

    def addSystemMessage(self, msg, color = None):
        if self.handlers.get('Chat.onNewLogMessage', None) is None:
            return
        else:
            channelInfo = CCD.data.get(0, None)
            if channelInfo == None:
                color = '#ffffff'
                chatName = gameStrings.TEXT_CHATPROXY_1294
            else:
                color = color if color else channelInfo.get('color', '#ffffff')
                icon = channelInfo.get('icon', None)
                if icon:
                    chatName = '!$' + str(channelInfo.get('icon'))
                else:
                    chatName = channelInfo.get('chatName')
            formatmsg = "<p><font color=\'%s\'>%s%s</font></p>" % (color, chatName, msg)
            self.addMsgToArr(0, formatmsg)
            formatmsg = formatmsg.decode(utils.defaultEncoding()).encode('utf-8')
            self.addChatHis(self.currentTab, formatmsg)
            self.setNewLogMessage(self.currentTab, formatmsg)
            return

    def setNewLogMessage(self, tabId, msg):
        path = keys.SET_UI_TABNOTIFY_ID + str(tabId)
        if tabId == uiConst.CHAT_TAB_PERSON:
            isNotify = AppSettings.get(path, 1)
        else:
            isNotify = AppSettings.get(path, 0)
        self.cacheMessages.append((tabId, msg, isNotify))
        self.hasCache = True

    def sendAllCacheMsgsMsgs(self):
        if self.hasCache and self.handlers.has_key('Chat.onNewLogMessage'):
            self.handlers['Chat.onNewLogMessage'].InvokeSelf(uiUtils.array2GfxAarry(self.cacheMessages))
            self.cacheMessages = []
        self.sendAllCacheMsgsMsgTimer = BigWorld.callback(0.1, self.sendAllCacheMsgsMsgs)

    def addChatHis(self, logId, fmsg, name = None):
        if len(self.chatLog[logId]) >= SCD.data.get('chatMaxHistory', 200):
            self.chatLog[logId].remove(self.chatLog[logId][0])
        self.chatLog[logId].append([fmsg, name])

    def updateConfigTab2Data(self):
        tabNotify = []
        for i, _ in self.channeltab:
            path = keys.SET_UI_TABNOTIFY_ID + str(i)
            tabNotify.append(AppSettings.get(path, 0))

        if self.chatLogWindowMC:
            self.chatLogWindowMC.Invoke('updateConfigTab2Data', uiUtils.array2GfxAarry(tabNotify))

    def getChatHis(self, logId):
        his = []
        for item in self.chatLog[logId]:
            his.append(item[0])

        return his

    def showFace(self, *arg):
        buttonName = arg[3][0].GetString()
        emotionId = int(buttonName[len('iconButton'):])
        prefix = '#BE:'
        p = BigWorld.player()
        p.cell.chatToView(prefix + str(emotionId), const.POPUP_MSG_SHOW_DURATION)

    def onGetLastWorldExMessage(self, *arg):
        return GfxValue(gbk2unicode(self.lastWorldExMessage))

    def onGetLastWorldExType(self, *arg):
        return GfxValue(self.getWorldExMessageSwfName(self.lastWorldExMessageType))

    def onGetChatInfo(self, *arg):
        info = {}
        key = keys.SET_UI_INFO + '/chatLog/'
        info['isHide'] = AppSettings.get(key + 'isHide', 0) if gameglobal.CURRENT_WINDOW_STYLE != gameglobal.WINDOW_STYLE_CHAT else 0
        info['alpha'] = AppSettings.get(key + 'alpha', -1.0)
        info['width'] = AppSettings.get(key + 'width', -1)
        info['height'] = AppSettings.get(key + 'height', -1)
        info['isPublished'] = BigWorld.isPublishedVersion()
        tabNotify = []
        for i in range(1, uiConst.CHAT_TAB_MAX):
            path = keys.SET_UI_TABNOTIFY_ID + str(i)
            if i == uiConst.CHAT_TAB_PERSON:
                tabNotify.append(AppSettings.get(path, 1))
            else:
                tabNotify.append(AppSettings.get(path, 0))

        info['tabNotify'] = tabNotify
        return uiUtils.dict2GfxDict(info, True)

    def onSetChatInfo(self, *arg):
        alpha = arg[3][0].GetElement(0).GetNumber()
        isHide = int(arg[3][0].GetElement(1).GetBool())
        key = keys.SET_UI_INFO + '/chatLog/'
        AppSettings[key + 'isHide'] = isHide
        AppSettings[key + 'alpha'] = alpha
        AppSettings[key + 'width'] = int(arg[3][0].GetElement(2).GetNumber())
        AppSettings[key + 'height'] = int(arg[3][0].GetElement(3).GetNumber())
        AppSettings.save()

    def showGM(self, *arg):
        signal = arg[3][0].GetString()
        if signal == 'DOWN':
            return GfxValue(self.handleDown())
        else:
            return GfxValue(self.handleUp())

    def handleUp(self):
        return self.chatHistory.handleUp()

    def handleDown(self):
        return self.chatHistory.handleDown()

    def onIsCommand(self, *arg):
        chatText = unicode2gbk(arg[3][0].GetString())
        ret = self.channelCommand(chatText)
        return GfxValue(ret)

    def channelCommand(self, chatText):
        if chatText == '':
            return False
        elif chatText[0] != '/':
            return False
        else:
            for channel in CCD.data:
                if channel == const.CHAT_CHANNEL_SINGLE:
                    continue
                shortCommand = CCD.data[channel].get('shortCommand', None)
                if shortCommand and self.checkChannelCanUse(channel) and (shortCommand + ' ' == chatText.lower() or '/' + CCD.data[channel]['chatName'] + ' ' == chatText.lower()):
                    self.setCurChannel(channel, '', True)
                    return True

            if chatText[0] == '/':
                channelInfo = CCD.data[const.CHAT_CHANNEL_SINGLE]
                shortCommand = channelInfo.get('shortCommand', None)
                if shortCommand:
                    length = len(shortCommand)
                    if shortCommand + ' ' == chatText[:length + 1].lower() and len(chatText[length + 1:]) > 0:
                        chatText = chatText[length + 1:-1]
                        self.updateChatTarge(chatText)
                        self.setCurChannel(const.CHAT_CHANNEL_SINGLE, '', True)
                        return True
                    length = len(channelInfo['chatName']) + 1
                    if '/' + channelInfo['chatName'] + ' ' == chatText[:length + 1].lower() and len(chatText[length + 1:]) > 0:
                        chatText = chatText[length + 1:-1]
                        self.updateChatTarge(chatText)
                        self.setCurChannel(const.CHAT_CHANNEL_SINGLE, '', True)
                        return True
            return False

    def onChatCommand(self, *arg):
        if gameglobal.rds.configData.get('enableChatCommand', True) and gameglobal.rds.configData.get('enableSemantics', False):
            p = BigWorld.player()
            self.getCurChannel()
            chatText = unicode2gbk(arg[3][0].GetString())
            self.firterCommandList = []
            if self.isInputOver(chatText) and self.isRightChannel(self.curChannel) and not p._isSoul():
                for cmd in self.cmdData:
                    funcName = cmd.get('funcName', '')
                    commandType = cmd.get('commandType', 0)
                    cmdEmote = cmd.get('cmdEmote', 0)
                    chatText = chatText.lower()
                    if funcName:
                        func = getattr(self, self.getJudgeFuncName(funcName), None)
                        if func:
                            if func(p):
                                for shortCommandName in cmd['shortCommandNames']:
                                    shortCommandName = shortCommandName.lower()
                                    isAppend = False
                                    pinyinFirstCommandName = pinyinConvert.strPinyinFirst(shortCommandName)
                                    pinyinFullCommandName = pinyinConvert.strPinyin(shortCommandName)
                                    if chatText in shortCommandName or chatText in pinyinFirstCommandName or chatText in pinyinFullCommandName:
                                        isAppend = True
                                        break

                                if isAppend:
                                    self.firterCommandList.append(cmd)
                        else:
                            gamelog.warning('@lvc not cmd Func', cmd, funcName)
                    else:
                        for shortCommandName in cmd['shortCommandNames']:
                            shortCommandName = shortCommandName.lower()
                            isAppend = False
                            pinyinFirstCommandName = pinyinConvert.strPinyinFirst(shortCommandName)
                            pinyinFullCommandName = pinyinConvert.strPinyin(shortCommandName)
                            if chatText in shortCommandName or chatText in pinyinFirstCommandName or chatText in pinyinFullCommandName:
                                isAppend = True
                                break

                        if isAppend and self.checkChannelCanUse(cmd.get('channelId', 5)):
                            if cmdEmote:
                                emoteChannels = SCD.data.get('emoteChannels', [const.CHAT_CHANNEL_VIEW, const.CHAT_CHANNEL_TEAM])
                                if self.curChannel in emoteChannels:
                                    self.firterCommandList.append(cmd)
                            else:
                                self.firterCommandList.append(cmd)

                self.showCommandList(self.firterCommandList, chatText)

    def isInputOver(self, chatText):
        return self.chooseCmdLen >= len(chatText)

    def isRightChannel(self, curChannel):
        if curChannel in const.CHAT_COMMAND_CHANNEL_LIST:
            return False
        return True

    def onChooseCmd(self, *args):
        name = unicode2gbk(args[3][0].GetString())
        cmd = self.getCmdByName(name)
        self.chooseCmdLen = len(name)
        commandType = cmd.get('commandType', 0)
        if commandType == const.CHAT_COMMAND_TYPE_SEND:
            if self.chatLogWindowMC != None:
                self.chatLogWindowMC.Invoke('clearTfInputTxt')
            self.setChatText(name)
        elif commandType == const.CHAT_COMMAND_TYPE_CHANGE:
            self.chooseCmdLen = 1024
            if cmd.get('channelId', 0) == const.CHAT_CHANNEL_SINGLE:
                httpLink = cmd.get('httpLink', '') + '  '
            else:
                httpLink = cmd.get('httpLink', '') + ' '
            self.channelCommand(httpLink)
            if self.chatLogWindowMC != None:
                self.chatLogWindowMC.Invoke('clearTfInputTxt')

    def getCmdByName(self, name):
        for cmd in self.cmdData:
            if cmd.get('showName') == name:
                return cmd

        return {}

    def onSetCommandData(self, *arg):
        self.cmdData = self.getCmdData()
        return uiUtils.array2GfxAarry(self.cmdData, True)

    def onGetDefaultChatList(self, *arg):
        ret = SCD.data.get('defaultChatTextList', ())
        return uiUtils.array2GfxAarry(ret, True)

    def onGetChannelIdByIconId(self, *arg):
        iconId = int(arg[3][0].GetNumber())
        channelId = -1
        for key, value in CCD.data.iteritems():
            if value.get('icon', -1) == iconId:
                channelId = key
                break

        return GfxValue(channelId)

    def getCmdData(self):
        ret = []
        for key, value in CCMD.data.items():
            if value.get('channelId') == const.CHAT_CHANNEL_SECRET and not gameglobal.rds.configData.get('enableSecretChannel'):
                continue
            cmd = {}
            cmd['id'] = key
            cmd['commandType'] = value.get('commandType', 0)
            cmd['funcName'] = value.get('funcName', '')
            cmd['httpLink'] = value.get('httpLink', '')
            cmd['showName'] = value.get('showName', '')
            cmd['shortCommandNames'] = value.get('shortCommandNames', ())
            cmd['shortCommandDesc'] = value.get('shortCommandDesc', '')
            cmd['cmdEmote'] = value.get('cmdEmote', 0)
            cmd['channelId'] = value.get('channelId', 5)
            ret.append(cmd)

        return ret

    def showCommandList(self, data, chatText):
        if self.chatLogWindowMC != None:
            if data:
                self.chatLogWindowMC.Invoke('showCommandList', uiUtils.array2GfxAarry(data, True))
            else:
                self.chatLogWindowMC.Invoke('showCommandListNone')

    def getCurChannel(self):
        if self.chatLogWindowMC != None:
            self.curChannel = int(self.chatLogWindowMC.Invoke('getCurChannel').GetNumber())

    def teamToGroup(self):
        if self.chatLogWindowMC != None and int(self.chatLogWindowMC.Invoke('getCurChannel').GetNumber()) == const.CHAT_CHANNEL_TEAM:
            self.setCurChannel(const.CHAT_CHANNEL_GROUP)

    def updateChatTarge(self, targetName):
        if self.chatLogWindowMC != None:
            self.chatLogWindowMC.Invoke('updateChatTarge', GfxValue(gbk2unicode(targetName)))

    def setCurChannel(self, channel, name = '', focusd = False):
        if self.chatLogWindowMC != None:
            self.chatLogWindowMC.Invoke('handleChannelBtn', (GfxValue(channel), GfxValue(gbk2unicode(name)), GfxValue(focusd)))

    def onClickMenu(self, *arg):
        menuName = arg[3][0].GetString()
        roleName = unicode2gbk(arg[3][1].GetString())
        try:
            name, self.prosecuteMsg = roleName[4:].split('$', 1)
            menuManager.getInstance().onMenuItemClick(menuName, uiConst.MENU_CHAT)
        except:
            raise Exception('@zhp chat rolename format error:%s' % roleName)

    def onFitting(self, *arg):
        p = BigWorld.player()
        roleName = unicode2gbk(arg[3][0].GetString())
        if roleName[:3] == 'ret':
            retCode = int(roleName[3:])
            p.base.chatToItem(retCode, 'fitting')
        elif roleName[:4] == 'item':
            gameglobal.rds.ui.fittingRoom.addItem(Item(int(roleName[4:]), 1, False))

    def onLinkLeftClick(self, *arg):
        p = BigWorld.player()
        roleName = unicode2gbk(arg[3][0].GetString())
        if roleName[:3] == 'ret':
            retCode = int(roleName[3:])
            p.base.chatToItem(retCode, 'chat')
        elif roleName[:4] == 'role' and roleName != 'role' + p.realRoleName:
            name, channel = roleName[4:].split('$', 1)
            gameglobal.rds.ui.chat.updateChatTarge(name)
            gameglobal.rds.ui.chat.setCurChannel(const.CHAT_CHANNEL_SINGLE, '', True)
        elif roleName[:7] == 'channel':
            gameglobal.rds.ui.chat.setCurChannel(int(roleName[7:]), '', True)
        elif roleName[:4] == 'item':
            pos = roleName.find(':')
            if pos == -1:
                itemId = roleName[4:]
                it = Item(int(itemId), 1, False)
            else:
                itemId = roleName[4:pos]
                it = Item(int(itemId), 1, False)
                itdata = roleName[pos + 1:].split(':')
                for i in range(0, len(itdata), 2):
                    attrv = itdata[i + 1]
                    if attrv.isdigit():
                        attrv = int(attrv)
                    setattr(it, itdata[i], attrv)

            gfxTipData = gameglobal.rds.ui.inventory.GfxToolTip(it)
            self.showTooltip(const.CHAT_TIPS_ITEM, gfxTipData)
        elif roleName[:4] == 'task':
            self.showTooltip(const.CHAT_TIPS_TASK, self.taskToolTip(int(roleName[4:])))
        elif roleName[:4] == 'achv':
            self.showTooltip(const.CHAT_TIPS_ACHIEVEMENT, self.achieveToolTip(roleName[4:]))
        elif roleName[:3] == 'net':
            BigWorld.openUrl('http://' + roleName[3:])
        elif roleName[:9] == 'imageLink':
            gameglobal.rds.ui.yixinImage.show(roleName[9:])
        elif roleName[:6] == 'mapPos':
            posStr = roleName[6:]
            posX, posY, posZ, mapName = posStr.split(',')
            spaceNo = formula.getMapId(p.spaceNo)
            if spaceNo != const.SPACE_NO_BIG_WORLD:
                BigWorld.player().showGameMsg(GMDD.data.MAP_NOT_IN_BIG_WORLD, ())
                return
            gameglobal.rds.ui.map.openMap(True, targetPos=(posX,
             posY,
             posZ,
             mapName))
        elif roleName[:10] == 'teamInvite':
            targetName = roleName[10:]
            BigWorld.player().cell.applyGroup(targetName)
        elif roleName[:8] == 'teamInfo':
            teamInfo = roleName[8:]
            groupId = int(teamInfo)
            p = BigWorld.player()
            if hasattr(p, 'teamInfoQueryDict'):
                if p.teamInfoQueryDict.get(groupId):
                    self.showTeamTooltip(p.teamInfoQueryDict[groupId])
            BigWorld.player().cell.queryLinkTeamInfo(groupId)
        elif roleName[:9] == 'macroInfo':
            if gameglobal.rds.ui.skillMacroOverview.checkMacroFull():
                return
            p = BigWorld.player()
            macroInfo = roleName[9:].split(',')
            macroId = long(macroInfo[0])
            gbId = long(macroInfo[1])
            school = int(macroInfo[2])
            now = int(macroInfo[3])
            if p.school != school:
                p.showGameMsg(GMDD.data.SKILL_MACRO_SHARE_SCHOOL_ERROR, ())
                return
            msg = uiUtils.getTextFromGMD(GMDD.data.SKILL_MACRO_SHARE_CONFIRM)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(gameglobal.rds.ui.skillMacroOverview.shareConfirm, macroId, gbId, now))
        elif roleName.startswith('sprite'):
            p.base.chatToSprite(int(roleName[len('sprite'):]), 'chat')

    def doSendMapLink(self, *args):
        p = BigWorld.player()
        if p.inWingCityOrBornIsland():
            spaceNo = self.uiAdapter.map.getMapIdBySpaceNo(p.spaceNo, p.position)
        else:
            spaceNo = formula.getMapId(p.spaceNo)
            if spaceNo != const.SPACE_NO_BIG_WORLD:
                BigWorld.player().showGameMsg(GMDD.data.MAP_NOT_IN_BIG_WORLD, ())
                return
        if MTLD.data.has_key(spaceNo):
            mapName = MTLD.data[spaceNo].get('mapPath', 'ycdg')
        else:
            mapName = MII.data[spaceNo].get('mapPath', 'ycdg')
        pos = p.position
        pos = BigWorld.findDropPoint(p.spaceID, Math.Vector3(pos.x, pos.y + 1, pos.z))
        if pos:
            pos = pos[0]
        self.doSendPos(pos.x, pos.y, pos.z, mapName, True)

    def doSendPos(self, x, y, z, mapName = '', isNavigate = False):
        color = FCD.data.get(('mapInfo', 0), {}).get('color', '#ffe566')
        if not isNavigate:
            content = uiUtils.getTextFromGMD(GMDD.data.CHAT_BROAD_POSITION, gameStrings.TEXT_PUPPET_ACTION_286)
            event = '%d,%d,%d,%s' % (round(x),
             round(y),
             round(z),
             mapName)
            msg = "<font color=\'%s\'><a href = \'event:mapPos%s\'><u>%s</u></a></font>" % (color, event, content)
        else:
            content = uiUtils.getTextFromGMD(GMDD.data.CHAT_BROAD_POSITION2, '[%s(%d,%d)]')
            p = BigWorld.player()
            if p.inWingCityOrBornIsland():
                mapId = self.uiAdapter.map.getMapIdBySpaceNo(p.spaceNo, p.position)
                mapName = MTLD.data.get(mapId, {}).get('mapName_ii', '')
                areaId = p.spaceNo
            else:
                name = uiUtils.getChunkName(x, z)
                areaId = CMD.data.get(name, {}).get('mapAreaId')
                if not areaId:
                    return
                mapName = MIII.data.get(areaId, {}).get('mapName_iii', '')
            content = content % (mapName, int(x), int(z))
            event = '%d,%d,%d,%s' % (p.spaceNo,
             round(x),
             round(y),
             round(z))
            msg = "<font color=\'%s\'> <a href = \'event:findPos:%s\'><u>%s</u></a> </font>" % (color, event, content)
        gameglobal.rds.ui.sendLink(msg)

    def onGetRightMenuVisible(self, *arg):
        roleName = unicode2gbk(arg[3][0].GetString())
        p = BigWorld.player()
        self.resetProsecuteArg()
        if utils.isRedPacket(roleName):
            roleName = 'role' + roleName
        if roleName[:4] == 'role':
            name, prosecuteMsg = roleName[4:].split('$', 1)
            self.chatTimestamp, self.chatChannelId, self.chatMsg = self.decodeProsecuteMsg(prosecuteMsg)
            if name != p.realRoleName:
                if not p._isSoul():
                    if '-' in name:
                        name = name.split('-')[0]
                    p.cell.getRoleInfo(name)
                else:
                    hostId = None
                    serverName = utils.parseServerNameFromCrossName(name)
                    for key, value in MSD.data.items():
                        if value.get('serverName') == serverName:
                            hostId = key
                            break

                    menuManager.getInstance().menuTarget.apply(roleName=name, hostId=hostId)
                    menuData = menuManager.getInstance().getMenuListById(uiConst.MENU_CHAT)
                    self.chatLogWindowMC.Invoke('showRightMenu', uiUtils.dict2GfxDict(menuData, True))
        if roleName[:9] == 'anonymous':
            gbId, prosecuteMsg = roleName[9:].split('$', 1)
            self.chatTimestamp, self.chatChannelId, self.chatMsg = self.decodeProsecuteMsg(prosecuteMsg)
            if self.chatLogWindowMC:
                menuManager.getInstance().menuTarget.apply(gbId=gbId)
                menuData = menuManager.getInstance().getMenuListById(uiConst.MENU_ANONYMOUS)
                self.chatLogWindowMC.Invoke('showRightMenu', uiUtils.dict2GfxDict(menuData, True))
        elif roleName[:7] == 'anCross':
            gbIdAndServerName, prosecuteMsg = roleName[7:].split('$', 1)
            parseItem = utils.parseCanonicalCrossServerRoleName(gbIdAndServerName)
            gbId = parseItem[0]
            serverName = parseItem[1]
            if serverName == gameglobal.gServerName:
                self.chatTimestamp, self.chatChannelId, self.chatMsg = self.decodeProsecuteMsg(prosecuteMsg)
                if self.chatLogWindowMC:
                    menuManager.getInstance().menuTarget.apply(gbId=gbId)
                    menuData = menuManager.getInstance().getMenuListById(uiConst.MENU_ANONYMOUS)
                    self.chatLogWindowMC.Invoke('showRightMenu', uiUtils.dict2GfxDict(menuData, True))
        elif roleName[:6] == 'rCross':
            gbIdAndServerName, prosecuteMsg = roleName[6:].split('$', 1)
            parseItem = utils.parseCanonicalCrossServerRoleName(gbIdAndServerName)
            name = parseItem[0]
            serverName = parseItem[1]
            if serverName == gameglobal.gServerName:
                self.chatTimestamp, self.chatChannelId, self.chatMsg = self.decodeProsecuteMsg(prosecuteMsg)
                if name != p.realRoleName:
                    p.cell.getRoleInfo(name)
            elif self.chatLogWindowMC:
                hostId = None
                for key, value in MSD.data.items():
                    if value.get('serverName') == serverName:
                        hostId = key
                        break

                if hostId and self.uiAdapter.friend.enableGlobalFriend():
                    menuManager.getInstance().menuTarget.apply(roleName=name, hostId=hostId)
                    menuData = menuManager.getInstance().getMenuListById(uiConst.MENU_CHAT_CROSS_SERVER)
                    self.chatLogWindowMC.Invoke('showRightMenu', uiUtils.dict2GfxDict(menuData, True))
        elif roleName[:8] == 'teamInfo':
            teamId = roleName[8:]
            menuManager.getInstance().menuTarget.apply(extraInfo={'teamId': teamId})
            menuData = menuManager.getInstance().getMenuListById(uiConst.MENU_SHARE_TEAM)
            self.chatLogWindowMC.Invoke('showRightMenu', uiUtils.dict2GfxDict(menuData, True))

    def showRightMenu(self, roleName, lv, school):
        if self.chatLogWindowMC:
            menuManager.getInstance().menuTarget.apply(roleName=roleName, school=school, lv=lv, channelId=self.chatChannelId)
            menuData = menuManager.getInstance().getMenuListById(uiConst.MENU_CHAT)
            self.chatLogWindowMC.Invoke('showRightMenu', uiUtils.dict2GfxDict(menuData, True))

    def showTargetRightMenu(self, roleName, gbId, hostId, menuId):
        if self.chatLogWindowMC:
            menuManager.getInstance().menuTarget.apply(roleName=roleName, gbId=gbId, hostId=hostId)
            menuData = menuManager.getInstance().getMenuListById(menuId)
            self.chatLogWindowMC.Invoke('showRightMenu', uiUtils.dict2GfxDict(menuData, True))

    def canInviteGuild(self):
        if not BigWorld.player().guild:
            return False
        return gameglobal.rds.ui.guild.checkAuthorization(gametypes.GUILD_ACTION_INVITE_MEMBER)

    def getTaskDetail(self, questId):
        qd = QD.data.get(questId, {})
        questName = qd.get('name', gameStrings.TEXT_CHATPROXY_2514)
        questDesc = qd.get('desc', gameStrings.TEXT_CHATPROXY_2514)
        questGoalsTermName = ''
        questGoalsTermCnt = ''
        if commQuest.enableQuestMaterialBag(self, qd):
            for itemId, cnt in qd['compMaterialItemCollectAndConsume']:
                name = ID.data.get(itemId, {}).get('name', '')
                questGoalsTermName = questGoalsTermName + name + '\n'
                questGoalsTermCnt = questGoalsTermCnt + gameStrings.TEXT_HISTORYCONSUMEDPROXY_256 + str(cnt) + '\n'

        elif qd.has_key('compItemCollect'):
            for i, (itemId, cnt) in enumerate(qd['compItemCollect']):
                name = ID.data.get(itemId, {}).get('name', '')
                questGoalsTermName = questGoalsTermName + name + '\n'
                questGoalsTermCnt = questGoalsTermCnt + gameStrings.TEXT_HISTORYCONSUMEDPROXY_256 + str(cnt) + '\n'

        elif qd.has_key('compItemCollectMulti'):
            for items in qd['compItemCollectMulti']:
                for itemId, cnt in items:
                    name = ID.data.get(itemId, {}).get('name', '')
                    questGoalsTermName = questGoalsTermName + name + '\n'
                    questGoalsTermCnt = questGoalsTermCnt + gameStrings.TEXT_HISTORYCONSUMEDPROXY_256 + str(cnt) + '\n'

        if qd.has_key('comSmtItem'):
            for itemId, cnt in qd['comSmtItem']:
                name = ID.data.get(itemId, {}).get('name', '')
                questGoalsTermName = questGoalsTermName + name + '\n'
                questGoalsTermCnt = questGoalsTermCnt + gameStrings.TEXT_HISTORYCONSUMEDPROXY_256 + str(cnt) + '\n'

        if qd.has_key('needMonsters'):
            for i, (mType, cnt) in enumerate(qd['needMonsters']):
                name = MD.data[mType]['name']
                questGoalsTermName = questGoalsTermName + name + '\n'
                questGoalsTermCnt = questGoalsTermCnt + gameStrings.TEXT_HISTORYCONSUMEDPROXY_256 + str(cnt) + '\n'

        if qd.has_key('beatMonsterNo'):
            mNo = qd['beatMonsterNo']
            name = MD.data[mNo]['name']
            questGoalsTermName = questGoalsTermName + name + '\n'
            questGoalsTermCnt = questGoalsTermCnt + gameStrings.TEXT_CHATPROXY_2558
        if qd.has_key('comBuff'):
            stateId = qd['comBuff']
            name = SD.data[stateId]['name']
            questGoalsTermName = questGoalsTermName + name + '\n'
            questGoalsTermCnt = questGoalsTermCnt + gameStrings.TEXT_CHATPROXY_2558
        if qd.has_key('comBuffEx'):
            stateIds = qd['comBuffEx']
            if stateIds[0] == 0:
                questGoalsTermName = questGoalsTermName + gameStrings.TEXT_CHATPROXY_2571 + '\n'
                questGoalsTermCnt = questGoalsTermCnt + '\n'
                for stateId in stateIds[1:]:
                    questGoalsTermName = questGoalsTermName + gameStrings.TEXT_CHATPROXY_2574 + SD.data[stateId]['name'] + '\n'
                    questGoalsTermCnt = questGoalsTermCnt + gameStrings.TEXT_CHATPROXY_2558

            elif stateIds[0] == 1:
                questGoalsTermName = questGoalsTermName + gameStrings.TEXT_CHATPROXY_2577 + '\n'
                questGoalsTermCnt = questGoalsTermCnt + '\n'
                for stateId in stateIds[1:]:
                    questGoalsTermName = questGoalsTermName + gameStrings.TEXT_CHATPROXY_2574 + SD.data[stateId]['name'] + '\n'
                    questGoalsTermCnt = questGoalsTermCnt + gameStrings.TEXT_CHATPROXY_2558

        if qd.has_key('markerNpcs'):
            markerMsgs = qd['markerNpcsMsg']
            for i, markerId in enumerate(qd['markerNpcs']):
                questGoalsTermName = questGoalsTermName + markerMsgs[i] + '\n'
                questGoalsTermCnt = questGoalsTermCnt + gameStrings.TEXT_CHATPROXY_2558

        if qd.has_key('debateChatId'):
            questGoalsTermName = questGoalsTermName + qd['debateMsg'] + '\n'
            questGoalsTermCnt = questGoalsTermCnt + gameStrings.TEXT_CHATPROXY_2558
        if qd.has_key('arenaWin'):
            questGoalsTermName = questGoalsTermName + gameStrings.TEXT_CHATPROXY_2597
            questGoalsTermCnt = questGoalsTermCnt + gameStrings.TEXT_HISTORYCONSUMEDPROXY_256 + str(qd['arenaWin']) + '\n'
        if qd.has_key('needDialog'):
            npcIds = qd['needDialog']
            dialogMsg = qd['needDialogMsg']
            for i, npcId in enumerate(npcIds):
                questGoalsTermName = questGoalsTermName + dialogMsg[i] + '\n'
                questGoalsTermCnt = questGoalsTermCnt + gameStrings.TEXT_CHATPROXY_2558

        return (questName,
         questDesc,
         questGoalsTermName,
         questGoalsTermCnt)

    def taskToolTip(self, taskId):
        p = BigWorld.player()
        type = self.UNACCEPT_TASK
        if taskId in p.quests:
            type = self.ACCEPT_TASK
        if p.getQuestFlag(taskId):
            type = self.COMPLETE_TASK
        questName, questDesc, questGoalsTermName, questGoalsTermCnt = self.getTaskDetail(taskId)
        taskToolTip = questName + ',' + str(type) + ',' + questDesc + gameStrings.TEXT_CHATPROXY_2618 + questGoalsTermName + ',' + questGoalsTermCnt
        return GfxValue(gbk2unicode(taskToolTip))

    def achieveToolTip(self, achieveData):
        tipData = {}
        achievementData = achieveData.split(':')
        achievementId = int(achievementData[0][2:])
        roleName = ''
        timeStr = ''
        aData = AD.data.get(achievementId, {})
        if len(achievementData) > 1 and achievementData[1][:4] == 'time':
            roleName = achievementData[2]
            timeStr = achievementData[1][4:]
        achieveDate = ''
        if roleName and timeStr:
            achieveDate = gameStrings.ACHIEVE_TIP_DATE_TEXT % (roleName, timeStr)
        achievementName = aData.get('name', '')
        achievementDesc = aData.get('desc', '')
        tipData['achievementName'] = achievementName
        tipData['achievementDesc'] = achievementDesc
        tipData['achieveDate'] = achieveDate
        rewardTitle = ''
        rewardTitleId = aData.get('rewardTitle', '')
        if rewardTitleId:
            titleData = TD.data.get(rewardTitleId, {})
            color = FCD.data.get(('title', titleData.get('style', 1)), {}).get('color', '')
            rewardTitle = gameStrings.ACHIEVE_TIP_REWARDTITLE_TEXT % (color, titleData.get('name', ''))
        tipData['rewardTitle'] = rewardTitle
        rewardItemHeadLine = ''
        rewardItemName = ''
        bonusId = AD.data[achievementId].get('bonusId', 0)
        rewardItems = clientUtils.genItemBonus(bonusId)
        if rewardItems:
            rewardItemHeadLine = gameStrings.ACHIEVE_TIP_REWARD_ITEM_TITLE_TEXT
            for i, (itemId, itemNum) in enumerate(rewardItems):
                itemData = ID.data.get(itemId, {})
                if itemData:
                    itemName = itemData.get('name', '')
                    quality = itemData.get('quality', 0)
                    color = FCD.data.get(('item', quality), {}).get('color', '')
                    rewardItemName += gameStrings.ACHIEVE_TIP_REWARD_ITEM_TEXT % (color, itemName, itemNum)
                    rewardItemName += '\n'

        tipData['rewardItemHeadLine'] = rewardItemHeadLine
        tipData['rewardItemName'] = rewardItemName
        targetList = []
        if aData.get('isExpand', 0) and aData.get('expandType', 1) != 1:
            for targetId in aData.get('achieveTargets', ()):
                itemInfo = {'targetName': ATD.data.get(targetId, {}).get('name', '')}
                itemInfo['isDone'] = str(targetId) in achievementData or achieveDate
                targetList.append(itemInfo)

        tipData['targetList'] = targetList
        tipData['expandCount'] = aData.get('expandCount', 1)
        return uiUtils.dict2GfxDict(tipData, True)

    def checkChannelCanUse(self, channelId):
        p = BigWorld.player()
        if channelId == const.CHAT_CHANNEL_CROSS_SERVER_WORLD_EX:
            if gameglobal.rds.configData.get('enableCrossServerLaba', False) == False:
                return False
        if channelId == const.CHAT_CHANNEL_WORLD_WAR:
            if gameglobal.rds.configData.get('enableWorldWarLaba', False) == False:
                return False
        if channelId == const.CHAT_CHANNEL_TEAM:
            if p.groupNUID == 0 or p.groupType != gametypes.GROUP_TYPE_TEAM_GROUP and p.groupType != gametypes.GROUP_TYPE_RAID_GROUP:
                return False
        if channelId == const.CHAT_CHANNEL_GROUP:
            if p.groupNUID == 0 or p.groupType != gametypes.GROUP_TYPE_RAID_GROUP:
                return False
        if channelId == const.CHAT_CHANNEL_GUILD:
            if not p.guildNUID:
                return False
        if channelId == const.CHAT_CHANNEL_CLAN:
            if not p.clanNUID or not gameglobal.rds.configData.get('enableClan', False):
                return False
        if channelId == const.CHAT_CHANNEL_NEW_PLAYER:
            if not self.inLowLevelChannel():
                return False
        if channelId == const.CHAT_CHANNEL_DIGONG_LINE:
            if not formula.spaceInMultiLine(p.spaceNo):
                return False
        if channelId == const.CHAT_CHANNEL_OB:
            if formula.canObserveFB(p.spaceNo) or formula.spaceInAnnalReplay(p.spaceNo):
                return True
            else:
                return False
        if channelId == const.CHAT_CHANNEL_CROSS_SERVER_WORLD_EX:
            if not gameglobal.rds.configData.get('enableYuanguLaba', True):
                return False
        if channelId == const.CLIENT_CHANNEL_BATTLE_FIELD_ALL_SIDE:
            if gameglobal.rds.ui.battleOfFortProgressBar.checkBattleFortNewFlag():
                return False
        if channelId == const.CHAT_CHANNEL_WING_WORLD_CAMP:
            if not self.enableCampChannel():
                return False
        if channelId == const.CHAT_CHANNEL_SCHOOL:
            if p.isInPUBG():
                return False
        if channelId == const.CHAT_CHANNEL_WORLD:
            if p.isInPUBG():
                return False
        if channelId == const.CHAT_CHANNEL_WORLD_EX:
            if p.isInPUBG():
                return False
        if channelId == const.CHAT_CHANNEL_ANONYMITY:
            if not gameglobal.rds.configData.get('enableChatAnonymity', True):
                return False
            if not worldBossHelper.getInstance().isInWorldBossActivity():
                return False
        return True

    def onChangeChannel(self, *arg):
        idNum = int(arg[3][0].GetNumber())
        configChannel = self.configChannel
        nowPos = 0
        for id in range(0, len(configChannel)):
            if idNum == configChannel[id]:
                nowPos = id
                break

        channelList = configChannel[nowPos:] + configChannel[:nowPos]
        idNum = channelList[0]
        for i in xrange(1, len(channelList)):
            if self.checkChannelCanUse(channelList[i]) == False:
                continue
            idNum = channelList[i]
            break

        return GfxValue(idNum)

    def hideView(self):
        if gameglobal.CURRENT_WINDOW_STYLE == gameglobal.WINDOW_STYLE_CHAT:
            return
        if self.chatLogWindowMC:
            self.isHide = self.chatLogWindowMC.Invoke('isHide').GetBool()
            self.chatLogWindowMC.Invoke('hideView')

    def showView(self):
        if gameglobal.CURRENT_WINDOW_STYLE == gameglobal.WINDOW_STYLE_CHAT:
            return
        if self.chatLogWindowMC and not self.isHide:
            self.chatLogWindowMC.Invoke('showView')

    def setInputText(self, info):
        if self.chatLogWindowMC:
            self.chatLogWindowMC.Invoke('setInputText', GfxValue(info))

    def forbidChat(self, roleName):
        if roleName and self.chatLogWindowMC:
            needRefresh = False
            for tabId, logs in self.chatLog.items():
                delLogs = []
                for log in logs:
                    if log[1] == roleName:
                        delLogs.append(log)

                if tabId == self.currentTab and len(delLogs):
                    needRefresh = True
                for delLog in delLogs:
                    logs.remove(delLog)

            delWorldLogs = []
            for worldChat in self.worldExQueue:
                if worldChat[1] == roleName:
                    delWorldLogs.append(worldChat)

            for delLog in delWorldLogs:
                self.worldExQueue.remove(delLog)

            if needRefresh:
                self._innerRefreshChatLog()
            matchResult = None
            if self.lastWorldExMessage != '':
                try:
                    string = 'event:channel8(.*)event:role' + roleName
                    matchResult = re.search(string, self.lastWorldExMessage)
                except:
                    matchResult = None

            if matchResult and self.chatLogWindowMC:
                if len(self.worldExQueue) > 0:
                    popOut = self.worldExQueue.pop(0)
                    msg = popOut[0]
                    msgType = popOut[2]
                    self.lastWorldExMessage = msg
                    self.lastWorldExMessageType = msgType
                    swfName = self.getWorldExMessageSwfName(msgType)
                    self.chatLogWindowMC.Invoke('showWorldExMessage', (GfxValue(gbk2unicode(msg)), GfxValue(gbk2unicode(swfName))))
                else:
                    self.chatLogWindowMC.Invoke('hideWorldExMessage')

    gameStrings.TEXT_CHATPROXY_2832

    @ui.callAfterTime(5)
    def _innerRefreshChatLog(self):
        if self.chatLogWindowMC:
            self.chatLogWindowMC.Invoke('setTabMessage', uiUtils.array2GfxAarry(self.getChatHis(self.currentTab)))

    def saveChatLog(self, channels = None):
        try:
            fileName = 'chat/chat_%s.html' % time.strftime('%Y_%m_%d %H-%M-%S')
            f = open(fileName, 'w')
            if not channels:
                channels = self.allChatLog.keys()
            for channelId in sorted(channels):
                logs = self.allChatLog.get(channelId)
                if not logs or not CCD.data.get(channelId, {}).get('saveSortId'):
                    continue
                channelName = '<p style=\"color:blue\">==================================================%s==================================================</p>' % CCD.data.get(channelId, {}).get('chatName', '')
                f.write(channelName)
                color = '#FF0000'
                name = CCD.data.get(channelId, {}).get('chatName', gameStrings.TEXT_BOOTHPROXY_694)
                formatLog = [ self.formatSaveChatLog(x, color, name) for x in logs ]
                f.writelines(formatLog)

            f.close()
            BigWorld.player().showGameMsg(GMDD.data.SAVE_CHAT_LOG_DONE, (fileName,))
        except:
            gamelog.error('@zhp save log error')

    def formatSaveChatLog(self, msg, color, name):
        if utils.isRedPacket(msg):
            return ''
        msg = re.sub('<font.*?>|</font>|<u>|</u>|<p>|</p>', '', msg, 0, re.IGNORECASE)
        msg = re.sub('<A.*?>|</A>', '', msg)
        msg = re.sub('<a.*?>|</a>', '', msg)
        msg = re.sub('\\!\\$200|\\!\\$201', gameStrings.TEXT_CHATPROXY_2867, msg, 0, re.IGNORECASE)
        msg = re.sub('\\!\\$5[0-9]{2}', '', msg, 0, re.IGNORECASE)
        msg = re.sub('\\!\\$', '#', msg, 0, re.IGNORECASE)
        msg = gameStrings.TEXT_CHATPROXY_2870 % (color, name) + msg + '<br>'
        return msg

    def getJudgeFuncName(self, name):
        ff = list(name)
        ff[0] = ff[0].upper()
        ff = 'can' + ''.join(ff)
        return str(ff)

    def addFriend(self, p):
        return (p.roleName, p.roleName)

    def teamInvite(self, p):
        leaderName = ''
        for memberGbId in p.members:
            if p.members[memberGbId]['isHeader']:
                leaderName = p.members[memberGbId]['roleName']

        return (leaderName, p.detailInfo['teamName'])

    def guildRecruit(self, p):
        if p.guild:
            return (p.guild.nuid, p.guildName)

    def baishi(self, p):
        return (p.roleName, p.roleName)

    def shoutu(self, p):
        return (p.roleName, p.roleName)

    def personalSpace(self, p):
        msg = PZCD.data.get('PERSONAL_ZONE_LINK_MSG', gameStrings.TEXT_CHATPROXY_2900)
        msg = msg % p.roleName
        return (p.gbId, int(gameglobal.rds.gServerid), msg)

    def inviteGuild(self, p):
        return (p.roleName, p.roleName)

    def canAddFriend(self, p):
        return True

    def canTeamInvite(self, p):
        leaderName = ''
        for memberGbId in p.members:
            if p.members[memberGbId]['isHeader']:
                leaderName = p.members[memberGbId]['roleName']

        if leaderName:
            return True
        else:
            return False

    def canGuildRecruit(self, p):
        if not p.guildNUID:
            return False
        return gameglobal.rds.ui.guild.checkAuthorization(gametypes.GUILD_ACTION_INVITE_MEMBER)

    def canBaishi(self, p):
        ret = False
        if gameglobal.rds.ui.mentor.enableApprentice():
            ret = p.checkApprenticeCondition()
        elif p.enableNewApprentice():
            ret = p.checkApprenticeConditionEx()
        return ret

    def canShoutu(self, p):
        ret = False
        if gameglobal.rds.ui.mentor.enableApprentice():
            ret = p.checkMentorCondition()
        elif p.enableNewApprentice():
            ret = p.checkMentorConditionEx()
        return ret

    def canPersonalSpace(self, p):
        return True

    def canInviteGuild(self, p):
        if p.guildNUID:
            return False
        else:
            return True

    def chatMsgReg(self, msg, name, gbId, channelId):
        if not gameglobal.rds.configData.get('enableChatLink', False):
            return msg
        if channelId in (const.CHAT_CHANNEL_CROSS_SERVER_LIST, const.CHAT_CHANNEL_SECRET):
            return msg
        if msg[-5:] != ':role':
            return msg
        if gbId == BigWorld.player().gbId:
            return msg
        msg = msg[:-5]
        addStr = ''
        for id, reg in self.chatRegDict.iteritems():
            if channelId not in CRRD.data.get(id, {}).get('blackList', ()) and reg.search(msg):
                addStr += self.getLinkText(id, name, gbId)

        return msg + addStr + ':role'

    def getLinkText(self, funcId, name, gbId = 0):
        cfgData = CRRD.data.get(funcId, {})
        p = BigWorld.player()
        menuTarget = menuManager.getInstance().funcMenuTarget
        menuTarget.apply(roleName=name)
        if funcId == uiConst.CHAT_REG_BAISHI and menuTarget.canBaishi(p):
            addstr = cfgData.get('linkText', '') % str(name)
        elif funcId == uiConst.CHAT_REG_SHOUTU and menuTarget.canShoutu(p):
            addstr = cfgData.get('linkText', '') % str(name)
        elif funcId == uiConst.CHAT_REG_APPLYTEAM and menuTarget.canApplyTeamInChat(p):
            addstr = cfgData.get('linkText', '') % str(name)
        elif funcId == uiConst.CHAT_REG_INVITETEAM and menuTarget.canInviteTeam(p):
            addstr = cfgData.get('linkText', '') % str(name)
        else:
            addstr = ''
        return addstr

    def isAnonymousChannel(self, channelId):
        return channelId in (const.CHAT_CHANNEL_SECRET,)

    def onShowSoundSetting(self, *arg):
        pass

    def onStartSoundRecord(self, *arg):
        p = BigWorld.player()
        p.recordUploadTranslateSound(self.submitSoundRecord)

    def onEndSoundRecord(self, *arg):
        p = BigWorld.player()
        p.endSoundRecord()
        p.addSoundRecordNum(True, False)
        self.targetName = self.getTargetName()

    def submitSoundRecord(self, duration, key, content):
        content = unicode2gbk(content)
        content = utils.soundRecordRichText(key, duration) + content
        gamelog.debug('bgf@chatProxy submitSoundRecord', self.curChannel, self.targetName)
        self.getCurChannel()
        ccd = CCD.data.get(self.curChannel, {})
        if ccd.get('disableSoundRecord', 0):
            BigWorld.player().showGameMsg(GMDD.data.SOUND_RECORD_DISABLED_CHANNELS, ())
            return
        self.sendMessage(self.curChannel, content, '', self.targetName, autoInput=True)

    def onGetSounndRecordHotkey(self, *arg):
        _, _, keyDesc = hotkeyProxy.getChatLogSoundRecordKey()
        desc = SCD.data.get('CHAT_SOUND_RECORD_HOTKEY_DESC', '%s') % keyDesc
        return GfxValue(gbk2unicode(desc))

    def getTargetName(self):
        targetName = ''
        if self.chatLogWindowMC:
            targetName = unicode2gbk(self.chatLogWindowMC.Invoke('getTargetName').GetString())
        return targetName

    def onAddGuildPuzzle(self, *args):
        self.uiAdapter.guildPuzzle.initPanel(ASObject(args[3][0]))

    def updateLabaPos(self):
        if self.chatLogWindowMC:
            self.chatLogWindowMC.Invoke('updateLabaPos')

    def updateSoundRecordTip(self):
        if self.chatLogWindowMC:
            self.chatLogWindowMC.Invoke('updateSoundRecordTip')

    def addLanguageTag(self, msg):
        val = locale.getdefaultlocale()
        lan = val[0] if val else ''
        return utils.encodeMsgHeader(msg, {'language': lan})

    def checkLanguageBlock(self, msg, msgProperties, channelId):
        if not gameglobal.rds.configData.get('enableChatMultiLanguage', False):
            return False
        if not CCD.data.get(channelId, {}).get('enabelFilterLanguage', False):
            return False
        isBlock = False
        lan = msgProperties.get('language', '').lower()
        filterLans = AppSettings.get(keys.SET_CHAT_LANGUAGES, '').split(',')
        if lan and filterLans:
            isBlock = not lan.startswith(tuple(filterLans))
        return isBlock


MAX_HISTORY_LINES = 20

class ChatHistory(object):

    def __init__(self, maxHistoryLines = MAX_HISTORY_LINES):
        super(ChatHistory, self).__init__()
        self.maxHistoryLines = maxHistoryLines
        self.queue = []
        self.historyPos = 0

    def insert(self, gmCmd):
        if richTextUtils.isSysRichTxt(gmCmd):
            return
        if len(self.queue) < self.maxHistoryLines:
            self.queue.append(gmCmd)
        else:
            self.queue.pop(0)
            self.queue.append(gmCmd)
        self.historyPos = len(self.queue)

    def handleUp(self):
        if len(self.queue) > 0 and self.historyPos >= 0 and self.historyPos <= len(self.queue):
            self.historyPos -= 1
            if self.historyPos == -1:
                return ''
            msg = self.queue[self.historyPos]
            msg = gbk2unicode(msg)
            return msg
        else:
            return ''

    def handleDown(self):
        if len(self.queue) > 0 and self.historyPos >= -1 and self.historyPos < len(self.queue):
            self.historyPos += 1
            if self.historyPos == len(self.queue):
                return ''
            msg = self.queue[self.historyPos]
            msg = gbk2unicode(msg)
            return msg
        else:
            return ''
