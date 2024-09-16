#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/friendProxy.o
from gamestrings import gameStrings
import os
import BigWorld
from Scaleform import GfxValue
from PIL import Image
import gameglobal
import gametypes
import const
import formula
import C_ui
import ui
import utils
import copy
import gameconfigCommon
import commNpcFavor
from friend import FriendVal
from guis import events
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from uiProxy import UIProxy
from guis import pinyinConvert
from guis.ui import unicode2gbk
from data import school_data as SD
from callbackHelper import Functor
from helpers import taboo
from gameStrings import gameStrings
from guis import richTextUtils
from guis import menuManager
from cdata import game_msg_def_data as GMDD
from data import nf_npc_level_data as NNLD
from data import game_msg_data as GMD
from data import friend_location_data as FLD
from data import guild_config_data as GCD
from data import apprentice_config_data as ACD
from data import sys_config_data as SCD
from data import item_data as ID
from data import intimacy_data as IND
from data import intimacy_config_data as ICD
from data import message_desc_data as MSGDD
from data import npc_data as ND
from data import fight_for_love_config_data as FFLCD
from data import seeker_data as SKD
from data import intimacy_numeric_data as CIND
from data import nf_npc_data as NND
from data import nf_npc_level_data as NNLD
from data import nf_npc_friendly_level_data as NNFLD
from data import fame_data as FD
FUNC_BAISHI = 1
FUNC_SHOU_TU = 2
FUNC_KICK_MENTOR = 3
FUNC_KICK_APPRENTICE = 4
TIME_JOIN_CHAR = '-'
OP_RENAME_GROUP = 1
OP_DELETE_GROUP = 2
OP_CHAT_TO_GROUP = 3
OP_NEW_GROUP = 4
OP_UP_GROUP = 5
OP_DOWN_GROUP = 6
OP_SET_DEFALUT_GROUP = 7
REMARK_TYPE_ADD = 0
REMARK_TYPE_MODIFY = 1
REMARK_TYPE_FRIST_ADD = 2

class FriendProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FriendProxy, self).__init__(uiAdapter)
        self.modelMap = {'getFriendsList': self.onGetFriendsList,
         'getRoleInfo': self.onGetRoleInfo,
         'closePanel': self.onClosePanel,
         'showChatWindow': self.onShowChatWindow,
         'modifyRoleSta': self.onModifyRoleSta,
         'changeTab': self.onChangeTab,
         'getGroups': self.onGetGroups,
         'addGroup': self.onAddGroup,
         'showNewGroupBox': self.onShowNewGroupBox,
         'closeNewGroupBox': self.onCloseNewGroupBox,
         'canInviteGuild': self.onCanInviteGuild,
         'getGroupMenu': self.onGetGroupMenu,
         'clickGroupMenu': self.onClickGroupMenu,
         'moveToGroup': self.onMoveToGroup,
         'isNewGroup': self.onIsNewGroup,
         'renameGroup': self.onRenameGroup,
         'getOldGroupName': self.onGetOldGroupName,
         'searchFriend': self.onSearchFriend,
         'closeSearchPanel': self.onCloseSearchPanel,
         'exactSearchFriend': self.onExactSearchFriend,
         'conditionSearchFriend': self.onConditionSearchFriend,
         'getConditionInfo': self.onGetConditionInfo,
         'getTab': self.onGetTab,
         'getTeamMenu': self.onGetTeamMenu,
         'autoSetToLeave': self.onAutoSetToLeave,
         'getAutoLeaveState': self.onGetAutoLeaveState,
         'showChatToFriend': self.onShowChatToFriend,
         'closeMinChat': self.onCloseMinChat,
         'closeNotice': self.onCloseNotice,
         'setSignature': self.onSetSignature,
         'setSignatureShow': self.onSetSignatureShow,
         'setting': self.onSetting,
         'showSprite': self.onShowSprite,
         'getSelfProfile': self.onGetSelfProfile,
         'getCities': self.onGetCities,
         'closeSelfProfile': self.onCloseSelfProfile,
         'saveProfile': self.onSaveProfile,
         'showProfile': self.onShowProfile,
         'getOtherProfile': self.onGetOtherProfile,
         'closeOtherProfile': self.onCloseOtherProfile,
         'viewFriendProfile': self.onViewFriendProfile,
         'selectFile': self.onSelectFile,
         'uploadFile': self.onUploadFile,
         'getUserDefineDDSSucc': self.onGetUserDefineDDSSucc,
         'isShowCustomRadio': self.onIsShowCustomRadio,
         'isCustomRadioUsed': self.onIsCustomRadioUsed,
         'applyIcon': self.onApplyIcon,
         'showIcon': self.onShowIcon,
         'isShowCC': self.isShowCC,
         'isShowYixin': self.isShowYixin,
         'isBindYixin': self.isBindYixin,
         'getFriendIsBindYixin': self.onGetIsBindYixin,
         'otherFunc': self.onOtherFunc,
         'addToFriend': self.onAddToFriend,
         'getConstellation': self.onGetConstellation,
         'setExpand': self.onSetExpand,
         'remarkFriend': self.onRemarkFriend,
         'getScoFriendInfo': self.onGetScoFriendInfo,
         'showChooseServer': self.onShowChooseServer,
         'isShowCallFriend': self.onIsShowCallFriend,
         'showCallFriendWidget': self.onShowCallFriendWidget,
         'clickSysMsgBtn': self.onClickSysMsgBtn,
         'createChatOpen': self.onCreateChatOpen,
         'groupChatOpen': self.onGroupChatOpen,
         'groupRightMenu': self.onGroupRightMenu,
         'enableGroupChat': self.onEnableGroupChat,
         'getGuildBtnRedPotVisible': self.onGetGuildBtnRedPotVisible,
         'showGroupChat': self.onShowGroupChat,
         'seekNpc': self.onSeekNpc,
         'isPartner': self.onIsPartner}
        self.mediator = None
        self.searchMediator = None
        self.minChatMediator = None
        self.noticeMediator = None
        self.isShow = False
        self.selectedTab = 'recent'
        self.groupName = None
        self.isNewGroup = True
        self.fidToMove = None
        self.groupToAdd = None
        self.minChatArr = []
        self.chatArrIdMap = {}
        self.otherGbId = None
        self.otherData = None
        self.provinces = [ value.get('provinceName') for key, value in FLD.data.items() ]
        self.srcResPath = ''
        self.imagePath = ''
        self.photo = ''
        self.imageHeight = 0
        self.imageWidth = 0
        self.dstPhoto = ''
        self.isCustomRadioUsed = False
        self.result = {}
        self.inited = False
        self.messagesBeforeInit = []
        self.expandHistory = {}
        self.remarkType = REMARK_TYPE_ADD
        self.remarkFid = 0
        self.friendsScoInfo = {}
        self.searchHostId = 0
        self.inviteList = []
        self.tempMsgs = None
        self.recentData = {}
        self.refreshMessageCallBack = None
        self.tempFriendAddList = []
        self.clearTempFriendCallBack = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SEARCH_FRIEND, self.closeSearchPanel)
        uiAdapter.registerEscFunc(uiConst.WIDGET_FRIEND_V2, Functor(self.hide, False))
        uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_PUSH_INIMACY_YEARLY_REWARD, {'click': self.clickIntimacyRewardPushIcon})

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FRIEND_V2:
            self.mediator = mediator
            BigWorld.player().registerEvent(const.EVENT_YIXIN_BIND_SUCCESS, self.bindYixinCallBack)
            BigWorld.player().registerEvent(const.EVENT_YIXIN_UNBIND_SUCCESS, self.unbindYixinCallBack)
            enableFriendInvite = gameglobal.rds.configData.get('enableFriendInvite', False)
            return uiUtils.dict2GfxDict({'enableFriendInvite': enableFriendInvite})
        if widgetId == uiConst.WIDGET_SEARCH_FRIEND:
            self.searchMediator = mediator
            self.searchHostId = int(gameglobal.rds.g_serverid)
            if self.enableGlobalFriend():
                BigWorld.player().base.queryCrossServerProgressIds(gameglobal.rds.ui.yunchuiji.crossMsIdsVer)
            return uiUtils.dict2GfxDict({'enableGlobalFriend': self.enableGlobalFriend(),
             'serverName': gameglobal.rds.loginManager.titleName()}, True)
        if widgetId == uiConst.WIDGET_MIN_CHAT:
            self.minChatMediator = mediator
        elif widgetId == uiConst.WIDGET_FRIEND_NOTICE:
            self.noticeMediator = mediator
        elif widgetId == uiConst.WIDGET_ADD_FREIND_REAMRK:
            fval = BigWorld.player().getFValByGbId(self.remarkFid)
            if self.remarkType == REMARK_TYPE_FRIST_ADD:
                self.remarkType = REMARK_TYPE_ADD
                remarkName = self.getSuggestRemark(fval)
            else:
                remarkName = fval.remarkName if fval else ''
            friendName = fval.name if fval else ''
            return uiUtils.dict2GfxDict({'type': self.remarkType,
             'fid': str(self.remarkFid),
             'remarkName': remarkName,
             'fName': friendName,
             'maxChar': const.FRIEND_REMARK_NAME_MAX_LEN}, True)

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_ADD_FREIND_REAMRK:
            self.hideRemark()
        else:
            UIProxy._asWidgetClose(self, widgetId, multiID)

    def bindYixinCallBack(self, params):
        if self.mediator:
            self.mediator.Invoke('setBindYixin', GfxValue(True))

    def unbindYixinCallBack(self, params):
        if self.mediator:
            self.mediator.Invoke('setBindYixin', GfxValue(False))

    def clickIntimacyRewardPushIcon(self):
        msg = MSGDD.data.get('rewardIntimacyYearly_notify_msg', gameStrings.TEXT_FRIENDPROXY_244)
        npcId = ICD.data.get('INTIMACY_YEARLY_REWARD_NPC_ID', 90188)
        npcName = ND.data.get(npcId, {}).get('name', '')
        msg = msg % (BigWorld.player().intimacyTgtName, npcName)
        gameglobal.rds.ui.messageBox.showMsgBox(msg)

    def show(self):
        if not BigWorld.player().checkMapLimitUI(gametypes.MAP_LIMIT_UI_FRIEND):
            return
        if self.isOptimizeVersion():
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FRIEND_V2)
        self.isShow = True

    def clearWidget(self):
        if self.isOptimizeVersion():
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FRIEND_V2)
        self.closeRenameGroupBox()
        self.closeSearchPanel()
        self.hideRemark()
        self.isShow = False
        if BigWorld.player():
            if BigWorld.player().__class__.__name__ == 'PlayerAvatar':
                BigWorld.player().unRegisterEvent(const.EVENT_YIXIN_BIND_SUCCESS, self.bindYixinCallBack)
                BigWorld.player().unRegisterEvent(const.EVENT_YIXIN_UNBIND_SUCCESS, self.unbindYixinCallBack)
        self.mediator = None
        if self.uiAdapter.wishMadeView.fMediator:
            self.uiAdapter.wishMadeView.closeFriendWish()

    def reset(self):
        self.minChatArr = []
        self.chatArrIdMap = {}
        self.inited = False
        self.messagesBeforeInit = []
        self.expandHistory = {}

    def onIsShowCustomRadio(self, *arg):
        enableCustomRadio = gameglobal.rds.configData.get('enableCustomRadio', False)
        return GfxValue(enableCustomRadio)

    def onGetFriendsList(self, *arg):
        fType = int(arg[3][0].GetNumber())
        ret = uiUtils.array2GfxAarry(self._getFriendListData(self._tabToGroups(self.selectedTab), fType))
        BigWorld.player().base.refreshOtherFriends()
        return ret

    def onGetRoleInfo(self, *arg):
        p = BigWorld.player()
        stateMap = {0: gameStrings.TEXT_UIUTILS_1414,
         1: gameStrings.TEXT_FRIENDPROXY_293_1,
         2: gameStrings.TEXT_FRIENDPROXY_293_2,
         3: gameStrings.TEXT_FRIENDPROXY_293_3,
         4: gameStrings.TEXT_FRIENDPROXY_293_4}
        photo = p._getFriendPhoto(p)
        if uiUtils.isDownloadImage(photo):
            p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, self.onDownloadPhoto, (None,))
            photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
        photoBorderIcon = p._getFriendPhotoBorderIcon(p, uiConst.PHOTO_BORDER_ICON_SIZE40)
        ret = [photo,
         const.FRIEND_STATE_DESC[p.friend.state],
         uiUtils.getNameWithMingPain(p.realRoleName, p.selectedMPId),
         '(' + stateMap[p.friend.state] + ')',
         p.friend.signature,
         p.friend.showsig,
         photoBorderIcon]
        ret = uiUtils.array2GfxAarry(ret, True)
        return ret

    def onClosePanel(self, *arg):
        self.hide(False)

    def createXinYiManagerData(self):
        p = BigWorld.player()
        xinYi = p.xinYiManager
        if xinYi:
            return {'id': str(const.XINYI_MANAGER_ID),
             'name': xinYi['name'],
             'photo': p.getXinYiMsgPhoto(),
             'signature': xinYi['signature'],
             'state': p.getXinYiOnline(),
             'yixinOpenId': 0}
        else:
            return None

    def onShowChatWindow(self, *arg):
        fid = int(arg[3][0].GetString())
        if fid == const.FRIEND_SYSTEM_NOTIFY_ID:
            self.openSystemMessageWnd(fid)
        elif fid == const.FRIEND_RECENT_INTERACT_ID:
            self.openRecentInteractWnd()
        elif fid == const.FRIEND_RECENT_FIGHT_FOR_LOVE_ID:
            p = BigWorld.player()
            p.seekFightForLoveNpc()
        elif fid == const.FRIEND_NPC_ID:
            npcId = int(arg[3][1].GetNumber())
            if not npcId:
                npcId = BigWorld.player().npcFavor.todayFavor[0]
            self.beginChat(fid, npcId)
        else:
            self.beginChat(fid)

    def openSystemMessageWnd(self, fid):
        if not gameglobal.rds.ui.systemMessage.widget:
            p = BigWorld.player()
            if not p.handleFriendMsg(0, fid):
                gameglobal.rds.ui.systemMessage.show()
            sysNum = p.friend.tempMsgCount.get(const.FRIEND_SYSTEM_NOTIFY_ID, 0)
            if sysNum != 0:
                p.friend.tempMsgCount[const.FRIEND_SYSTEM_NOTIFY_ID] = 0
                p.friend._refreshFriendList()

    def onShowCallFriendWidget(self, *arg):
        fid = int(arg[3][0].GetString())
        gameglobal.rds.ui.callFriend.show(fid)

    def onAddGroup(self, *arg):
        groupName = unicode2gbk(arg[3][0].GetString())
        p = BigWorld.player()
        if groupName == gameStrings.TEXT_FRIENDPROXY_362:
            p.showGameMsg(GMDD.data.FRIEND_GROUP_NAME_FORBID, ())
            return
        else:
            p.base.addFriendGroup(groupName)
            self.groupToAdd = groupName
            self.onCloseNewGroupBox(None)
            return

    def _tabToGroups(self, tabName):
        if not self.isOptimizeVersion():
            return self._tabToGroupsOld(tabName)
        else:
            groups = None
            if tabName == 'player':
                groups = BigWorld.player().getFriendGroupOrder()
                if gameconfigCommon.enableNpcFavor():
                    groups.append(gametypes.FRIEND_GROUP_NPC)
                groups.append(gametypes.FRIEND_GROUP_TEMP)
            elif tabName == 'recent':
                groups = [gametypes.FRIEND_GROUP_RECENT]
            elif tabName == 'enemy':
                groups = [gametypes.FRIEND_GROUP_ENEMY]
            elif tabName == 'black':
                groups = [gametypes.FRIEND_GROUP_BLOCK]
            elif tabName == 'guild':
                if gameglobal.rds.configData.get('enableChatGroup', False):
                    groups = [gametypes.FRIEND_GROUP_SYSTEM_CHAT, gametypes.FRIEND_GROUP_MEMBERS_CHAT]
                else:
                    groups = None
            return groups

    def onChangeTab(self, *arg):
        tabName = arg[3][0].GetString()
        if self.selectedTab == tabName:
            return
        groups = self._tabToGroups(tabName)
        self.selectedTab = tabName
        self.refreshFriendList(self._getFriendListData(groups))

    def refreshFriendList(self, arr = None, tabName = None):
        if tabName and tabName != self.selectedTab:
            return
        else:
            if self.mediator != None:
                self.mediator.Invoke('_innerRefreshView', GfxValue(True))
            return

    def refreshFriendListWithoutIcon(self, arr = None, tabName = None):
        if tabName and tabName != self.selectedTab:
            return
        else:
            if self.mediator != None:
                self.mediator.Invoke('_innerRefreshView', GfxValue(True))
            return

    @staticmethod
    def __friendCompare(f1, f2):
        msgCnt1 = f1[9]
        msgCnt2 = f2[9]
        if f1[5] == str(const.XINYI_MANAGER_ID):
            return -1
        elif f2[5] == str(const.XINYI_MANAGER_ID):
            return 1
        elif f1[5] == str(const.FRIEND_SYSTEM_NOTIFY_ID):
            return -1
        elif f2[5] == str(const.FRIEND_SYSTEM_NOTIFY_ID):
            return 1
        elif msgCnt1 != msgCnt2:
            return cmp(msgCnt2, msgCnt1)
        s1 = const.FRIEND_STATE_MAP[f1[1]]
        s2 = const.FRIEND_STATE_MAP[f2[1]]
        if s1 == s2:
            return cmp(f2[11], f1[11])
        elif s1 == gametypes.FRIEND_STATE_OFFLINE:
            return 1
        elif s2 == gametypes.FRIEND_STATE_OFFLINE:
            return -1
        r = cmp(s1, s2)
        if r:
            return r
        else:
            return cmp(f1[2], f2[2])

    @staticmethod
    def __npcFriendCompare(f1, f2):
        return cmp(f1['sortKey'], f2['sortKey'])

    @staticmethod
    def __friendCompareByTime(f1, f2):
        if not FriendProxy.isOptimizeVersion():
            return FriendProxy.__friendCompareByTimeOld(f1, f2)
        if f1[5] == str(const.FRIEND_RECENT_INTERACT_ID):
            return -1
        if f2[5] == str(const.FRIEND_RECENT_INTERACT_ID):
            return 1
        if f1[5] == str(const.FRIEND_RECENT_FIGHT_FOR_LOVE_ID):
            return -1
        if f2[5] == str(const.FRIEND_RECENT_FIGHT_FOR_LOVE_ID):
            return 1
        if f1[5] == str(const.XINYI_MANAGER_ID):
            return -1
        if f2[5] == str(const.XINYI_MANAGER_ID):
            return 1
        return cmp(f2[10], f1[10])

    def _getFriendListData(self, groups = None, filterType = None, online = False, selectFriend = False):
        if not self.isOptimizeVersion():
            return self._getFriendListDataOld(groups, filterType, online, selectFriend)
        else:
            p = BigWorld.player()
            friend = p.friend
            data = []
            gmap = {}
            gdataKey = 'children'
            if groups == None or gametypes.FRIEND_GROUP_FRIEND in groups:
                if not selectFriend:
                    groups = self._tabToGroups('player')
            if not groups:
                return data
            for id in groups:
                name = ''
                if id in friend.groups.keys():
                    name = friend.groups[id]
                elif id == gametypes.FRIEND_GROUP_GLOBAL_FRIEND:
                    name = gameStrings.TEXT_FRIENDPROXY_496
                elif id in (gametypes.FRIEND_GROUP_SYSTEM_CHAT, gametypes.FRIEND_GROUP_MEMBERS_CHAT, gametypes.FRIEND_GROUP_NPC):
                    name = friend.getNameByGroupId(id)
                if name:
                    gdata = {'name': gbk2unicode(uiUtils.htmlToText(name)),
                     'num': '0/0',
                     'children': [],
                     'id': id,
                     'total': 0,
                     'visibleNum': 0,
                     'expand': self.expandHistory.get(name, True)}
                    gmap[id] = len(data)
                    data.append(gdata)

            if gmap.has_key(gametypes.FRIEND_GROUP_RECENT):
                if not selectFriend:
                    recentInteractMsg = self.genRecentInteractMsg(name, const.FRIEND_RECENT_INTERACT_ID)
                    groupIndex = gmap[gametypes.FRIEND_GROUP_RECENT]
                    data[groupIndex][gdataKey].append(recentInteractMsg)
                    data[groupIndex]['total'] += 1
                    data[groupIndex]['visibleNum'] += 1
                    if gameconfigCommon.enableFightForLove():
                        recentInteractMsg = self.genRecentInteractMsg(name, const.FRIEND_RECENT_FIGHT_FOR_LOVE_ID)
                        groupIndex = gmap[gametypes.FRIEND_GROUP_RECENT]
                        data[groupIndex][gdataKey].append(recentInteractMsg)
                        data[groupIndex]['total'] += 1
                        data[groupIndex]['visibleNum'] += 1
                    if gameconfigCommon.enableNpcFavor() and p.needPushNpcQuest(p.npcFavor.todayFavor[0]):
                        recentInteractMsg = self.genRecentInteractMsg(name, const.FRIEND_NPC_ID)
                        groupIndex = gmap[gametypes.FRIEND_GROUP_RECENT]
                        data[groupIndex][gdataKey].append(recentInteractMsg)
                        data[groupIndex]['total'] += 1
                        data[groupIndex]['visibleNum'] += 1
            if gmap.has_key(gametypes.FRIEND_GROUP_FRIEND):
                if p.xinYiManager and not selectFriend:
                    xinYiData = self.genXinYiMsg(name)
                    groupIndex = gmap[gametypes.FRIEND_GROUP_FRIEND]
                    data[groupIndex][gdataKey].append(xinYiData)
                    data[groupIndex]['total'] += 1
                    data[groupIndex]['visibleNum'] += 1
            if gmap.has_key(gametypes.FRIEND_GROUP_SYSTEM_CHAT) and gameglobal.rds.configData.get('enableChatGroup', False):
                if not selectFriend:
                    for nuId, info in p.groupChatData.items():
                        if nuId and info.get('type', 0) in [gametypes.FRIEND_GROUP_SYSTEM_CHAT, gametypes.FRIEND_GROUP_SYSTEM_CHAT_PARTNER]:
                            membersGroupChat = self.getGroupChatMsg(info.get('name', ''), nuId, gametypes.FRIEND_GROUP_SYSTEM_CHAT)
                            groupIndex = gmap[gametypes.FRIEND_GROUP_SYSTEM_CHAT]
                            data[groupIndex][gdataKey].append(membersGroupChat)
                            data[groupIndex]['total'] += 1
                            data[groupIndex]['visibleNum'] += 1

            if gmap.has_key(gametypes.FRIEND_GROUP_MEMBERS_CHAT) and gameglobal.rds.configData.get('enableChatGroup', False):
                if not selectFriend:
                    for nuId, info in p.groupChatData.items():
                        if nuId and info.get('type', 0) == gametypes.FRIEND_GROUP_MEMBERS_CHAT:
                            membersGroupChat = self.getGroupChatMsg(info.get('name', ''), nuId, gametypes.FRIEND_GROUP_MEMBERS_CHAT)
                            groupIndex = gmap[gametypes.FRIEND_GROUP_MEMBERS_CHAT]
                            data[groupIndex][gdataKey].append(membersGroupChat)
                            data[groupIndex]['total'] += 1
                            data[groupIndex]['visibleNum'] += 1

            friendValues = friend.values()
            if self.enableGlobalFriend() and gmap.has_key(gametypes.FRIEND_GROUP_GLOBAL_FRIEND):
                globalFriends = getattr(p, 'globalFriends', None)
                if globalFriends:
                    for gVal in globalFriends.friends.values():
                        friendValues.append(uiUtils.globalFriend2FriendVal(gVal))

            for fVal in friendValues:
                if filterType > 0:
                    if filterType == gameglobal.FRIENDS_ACKNOWLEDGE and not fVal.acknowledge:
                        continue
                    if filterType == gameglobal.FRIENDS_NOT_ACKNOWLEDGE and fVal.acknowledge:
                        continue
                if online and const.FRIEND_STATE_DESC[fVal.state] != 'online':
                    continue
                photoBorderIcon40 = p._getFriendPhotoBorderIcon(fVal, uiConst.PHOTO_BORDER_ICON_SIZE40)
                photoBorderIcon108 = p._getFriendPhotoBorderIcon(fVal, uiConst.PHOTO_BORDER_ICON_SIZE108)
                photo = p._getFriendPhoto(fVal)
                if uiUtils.isDownloadImage(photo):
                    if p.isGlobalFriendVal(fVal):
                        p.downloadCrossNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, int(p.globalFriends.friends.get(fVal.gbId).server), gametypes.NOS_FILE_PICTURE, None, (None,))
                    else:
                        p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, None, (None,))
                    photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
                msgCnt = friend.tempMsgCount.get(fVal.gbId, 0)
                rvalue = fVal.pally
                if self.selectedTab == 'enemy':
                    rvalue = fVal.hatred
                isBindYixin = fVal.yixinOpenId
                isFlowBack = fVal.flowbackType
                place = self._getLastPlace(fVal.spaceNo, fVal.areaId)
                if p.isGlobalFriendVal(fVal):
                    place = utils.getServerName(int(p.globalFriends.friends.get(fVal.gbId).server))
                fdata = [photo,
                 const.FRIEND_STATE_DESC[fVal.state],
                 gbk2unicode(fVal.getFullName()),
                 gbk2unicode(fVal.signature),
                 rvalue > 0,
                 str(fVal.gbId),
                 fVal.school,
                 fVal.level,
                 gbk2unicode(place),
                 msgCnt,
                 fVal.time,
                 rvalue,
                 isBindYixin,
                 fVal.group,
                 gbk2unicode(name),
                 fVal.deleted,
                 isFlowBack,
                 gbk2unicode(uiUtils.getShortStr(fVal.getFullName(), 8)),
                 (pinyinConvert.strPinyinFirst(fVal.getFullName()), pinyinConvert.strPinyin(fVal.getFullName())),
                 fVal.sex if fVal.sex else 1,
                 fVal.acknowledge,
                 p.isGlobalFriendVal(fVal),
                 fVal.showsig,
                 gbk2unicode(fVal.remarkName),
                 gbk2unicode(fVal.name),
                 photoBorderIcon40,
                 photoBorderIcon108]
                if gametypes.FRIEND_GROUP_NPC in groups and fVal.group == gametypes.FRIEND_GROUP_NPC:
                    npcData = self.getNpcInfo(fVal.gbId)
                    groupIndex = gmap[gametypes.FRIEND_GROUP_NPC]
                    data[groupIndex][gdataKey].append(npcData)
                    data[groupIndex]['total'] += 1
                    data[groupIndex]['visibleNum'] += 1
                elif fVal.group in groups and fVal.group > 0 and fVal.group != gametypes.FRIEND_GROUP_TEMP:
                    groupIndex = gmap[fVal.group]
                    data[groupIndex][gdataKey].append(fdata)
                    data[groupIndex]['total'] += 1
                    if friend.isVisible(fVal.state):
                        data[groupIndex]['visibleNum'] += 1
                if fVal.group == gametypes.FRIEND_GROUP_BLOCK_ENEMY:
                    if gametypes.FRIEND_GROUP_ENEMY in groups:
                        groupIndex = gmap[gametypes.FRIEND_GROUP_ENEMY]
                        tmpData = copy.deepcopy(fdata)
                        tmpData[13] = gametypes.FRIEND_GROUP_ENEMY
                        data[groupIndex][gdataKey].append(tmpData)
                        data[groupIndex]['total'] += 1
                        if friend.isVisible(fVal.state):
                            data[groupIndex]['visibleNum'] += 1
                    if gametypes.FRIEND_GROUP_BLOCK in groups:
                        groupIndex = gmap[gametypes.FRIEND_GROUP_BLOCK]
                        tmpData = copy.deepcopy(fdata)
                        tmpData[13] = gametypes.FRIEND_GROUP_BLOCK
                        data[groupIndex][gdataKey].append(tmpData)
                        data[groupIndex]['total'] += 1
                        if friend.isVisible(fVal.state):
                            data[groupIndex]['visibleNum'] += 1
                if gametypes.FRIEND_GROUP_TEMP in groups and fVal.group == gametypes.FRIEND_GROUP_TEMP:
                    groupIndex = gmap[gametypes.FRIEND_GROUP_TEMP]
                    tmpData = copy.deepcopy(fdata)
                    tmpData[13] = gametypes.FRIEND_GROUP_TEMP
                    if fVal.gbId in p.friend.tempFriendList:
                        tmpData[10] = len(p.friend.tempFriendList) - p.friend.tempFriendList.index(fVal.gbId)
                    data[groupIndex][gdataKey].append(tmpData)
                    data[groupIndex]['total'] += 1
                    if friend.isVisible(fVal.state):
                        data[groupIndex]['visibleNum'] += 1
                if gametypes.FRIEND_GROUP_RECENT in groups and fVal.gbId in p.friend.recentFriendList:
                    groupIndex = gmap[gametypes.FRIEND_GROUP_RECENT]
                    tmpData = copy.deepcopy(fdata)
                    tmpData[13] = gametypes.FRIEND_GROUP_RECENT
                    tmpData[10] = len(p.friend.recentFriendList) - p.friend.recentFriendList.index(fVal.gbId)
                    data[groupIndex][gdataKey].append(tmpData)
                    data[groupIndex]['total'] += 1
                    if friend.isVisible(fVal.state):
                        data[groupIndex]['visibleNum'] += 1
                if gametypes.FRIEND_GROUP_APPRENTICE in groups and fVal.apprentice:
                    groupIndex = gmap[gametypes.FRIEND_GROUP_APPRENTICE]
                    tmpData = copy.deepcopy(fdata)
                    tmpData[13] = gametypes.FRIEND_GROUP_APPRENTICE
                    data[groupIndex][gdataKey].append(tmpData)
                    data[groupIndex]['total'] += 1
                    if friend.isVisible(fVal.state):
                        data[groupIndex]['visibleNum'] += 1

            for gdata in data:
                gId = gdata['id']
                if gId == gametypes.FRIEND_GROUP_RECENT:
                    gdata[gdataKey] = sorted(gdata[gdataKey], FriendProxy.__friendCompareByTime)
                    for item in gdata[gdataKey]:
                        gbId = long(item[5])
                        self.recentData[gbId] = self.recentData.get(gbId, '')
                        item.append(gbk2unicode(self.recentData[gbId]))

                    self.fetchAllRecentMsg()
                elif gId == gametypes.FRIEND_GROUP_TEMP:
                    gdata[gdataKey] = sorted(gdata[gdataKey], FriendProxy.__friendCompareByTime)
                elif gId == gametypes.FRIEND_GROUP_NPC:
                    gdata[gdataKey] = sorted(gdata[gdataKey], FriendProxy.__npcFriendCompare)
                else:
                    gdata[gdataKey] = sorted(gdata[gdataKey], FriendProxy.__friendCompare)
                gdata['num'] = '%s/%s' % (gdata['visibleNum'], gdata['total'])

            return data

    def getNpcInfo(self, npcId, isUnicode = True):
        cfgData = NND.data.get(npcId, {})
        seekId = cfgData.get('seekId', 10016028)
        seekData = SKD.data.get(seekId, {})
        npcInfo = {}
        npcInfo['npcId'] = npcId

        def toUnicode(strContent):
            if isUnicode:
                return gbk2unicode(strContent)
            else:
                return strContent

        p = BigWorld.player()
        foodVal, moodVal, healthVal, socialVal = p.npcFavor.getNpcStatus(npcId)
        npcInfo['name'] = toUnicode(NND.data.get(npcId, {}).get('name', ''))
        name = NND.data.get(npcId, {}).get('name', '')
        npcInfo['searchStr'] = (pinyinConvert.strPinyinFirst(name), pinyinConvert.strPinyin(name))
        npcInfo['headIcon'] = toUnicode(uiUtils.getPNpcIcon(npcId))
        npcInfo['borderImg'] = toUnicode(BigWorld.player().getPhotoBorderIcon(cfgData.get('borderId', 1), uiConst.PHOTO_BORDER_ICON_SIZE108))
        npcInfo['sex'] = toUnicode('male' if cfgData.get('sex', 1) == const.SEX_MALE else 'female')
        level, _ = p.npcFavor.getPlayerRelationLvAndVal(npcId)
        npcInfo['level'] = toUnicode(str('level%d' % level))
        npcInfo['hungryValue'] = foodVal
        npcInfo['moodValue'] = moodVal
        npcInfo['healythValue'] = healthVal
        npcInfo['socialValue'] = socialVal
        npcInfo['news'] = toUnicode(self.getNpcTxtNews(npcId))
        npcInfo['seekId'] = seekId
        spaceNo = seekData.get('spaceNo', 0)
        x, y, z = seekData.get('xpos', 0), seekData.get('ypos', 0), seekData.get('zpos', 0)
        spaceName = formula.whatSpaceName(spaceNo, False)
        npcInfo['seekTxt'] = toUnicode(gameStrings.NPC_NAVI_POS % (spaceNo,
         x,
         y,
         z,
         spaceName))
        npcInfo['groupName'] = toUnicode(BigWorld.player().friend.getNameByGroupId(gametypes.FRIEND_GROUP_NPC))
        npcInfo['id'] = -npcId
        npcInfo['fid'] = const.FRIEND_NPC_ID
        npcInfo['dailyText'] = self.getNpcDailyText(npcId, isUnicode)
        npcInfo['sortKey'] = (-1 if npcId == p.npcFavor.todayFavor[0] else 1, npcId)
        npcInfo['isFavorNpc'] = npcId == p.npcFavor.todayFavor[0]
        return npcInfo

    def getLimitDesc(self, npcPId, lv, key):
        if key == 'fameBuff':
            fameId = NNLD.data.get((npcPId, lv), {}).get('fameId', 427)
            fameName = FD.data.get(fameId, {}).get('name', '')
            return gameStrings.NPC_FUNC_TIP.get(key, '') % fameName
        elif key == 'expBuff':
            expName = NNLD.data.get((npcPId, lv), {}).get('expName', 'expName')
            return gameStrings.NPC_FUNC_TIP[key] % expName
        else:
            isComplete = BigWorld.player().npcFavor.checkIsCompleted(key, npcPId, lv)
            desc = gameStrings.NPC_FUNC_TIP[key]
            if isComplete:
                desc = desc.replace(gameStrings.NPC_FUN_TIP_CHANGE[0], gameStrings.NPC_FUN_TIP_CHANGE[1])
            return desc

    def getNpcDailyText(self, npcPId, isUnicode = True):
        p = BigWorld.player()

        def toUnicode(strContent):
            if isUnicode:
                return gbk2unicode(strContent)
            else:
                return strContent

        npcLv, _ = p.npcFavor.getPlayerRelationLvAndVal(npcPId)
        dailyTexts = []
        limitDic = {}
        info = NNLD.data.get((npcPId, npcLv), {})
        for keys, keyName in gameStrings.NPC_FUNC_TIP.iteritems():
            if limitDic.has_key(keys):
                continue
            if type(keys) == str:
                if not info.has_key(keys):
                    continue
                dailyTexts.append(toUnicode(self.getLimitDesc(npcPId, npcLv, keys)))
                limitDic[keys] = True
            elif any([ info.has_key(key) for key in keys ]):
                dailyTexts.append(toUnicode(self.getLimitDesc(npcPId, npcLv, keys)))
                limitDic[keys] = True

        return dailyTexts

    def getNpcTxtNews(self, npcPId):
        txtNews = NND.data.get(npcPId, {}).get('txtNews', ())
        lastNews = ''
        p = BigWorld.player()
        for questId, news in txtNews:
            if not questId:
                lastNews = news
            elif p.isQuestCompleted(questId):
                lastNews = news
            else:
                break

        return lastNews

    def getNpcVal(self, npcId):
        npcInfo = self.getNpcInfo(npcId, False)
        fVal = FriendVal(name=npcInfo['name'], dbID=0, gbId=const.FRIEND_NPC_ID, pally=0, group=gametypes.FRIEND_GROUP_NPC, box=None, school=0, sex=const.SEX_MALE if npcInfo['sex'] == 'male' else 2, level=npcInfo['level'], signature='', acknowledge=True, state=1, spaceNo=0, areaId=0, showsig=False, hatred=0, offlineMsgCnt=0, photo=npcInfo['headIcon'], opNuid=0, apprentice=False, yixinOpenId='', deleted=False, toHostID=0, flowbackType=0, intimacy=0, intimacySrc={}, intimacyLv=1, remarkName='', mingpaiId=0)
        fVal.temp = False
        fVal.recent = False
        fVal.time = utils.getNow()
        fVal.eid = 0
        return fVal

    def getNpcFriendData(self):
        childrenList = []
        for npcId in [73007,
         73008,
         73011,
         73010]:
            npcInfo = self.getNpcInfo(npcId)
            childrenList.append(npcInfo)

        groupInfo = {}
        groupInfo['name'] = gbk2unicode('npc')
        groupInfo['id'] = gametypes.FRIEND_GROUP_NPC
        childrenLen = len(childrenList)
        groupInfo['num'] = gbk2unicode('%d/%d' % (childrenLen, childrenLen))
        groupInfo['visibleNum'] = childrenLen
        groupInfo['total'] = childrenLen
        groupInfo['children'] = childrenList
        groupInfo['expand'] = False
        return groupInfo

    def updateSignature(self, signature):
        if self.mediator != None:
            self.mediator.Invoke('refreshRoleSig', GfxValue(gbk2unicode(signature)))

    def updateState(self, state):
        if self.mediator != None:
            self.mediator.Invoke('refreshRoleSta', GfxValue(const.FRIEND_STATE_DESC[state]))

    def onModifyRoleSta(self, *arg):
        state = const.FRIEND_STATE_MAP[arg[3][0].GetString()]
        p = BigWorld.player()
        p.base.updateFriendState(state)
        if state == gametypes.FRIEND_STATE_AWAY:
            p.base.setFriendOption(gametypes.FRIEND_OPTION_AUTO_AWAY, False)

    def onGetGroups(self, *arg):
        fid = int(arg[3][0].GetString())
        p = BigWorld.player()
        fVal = p.getFValByGbId(fid)
        if not fVal:
            return
        groups = p.friend.getFriendGroups()
        ret = []
        for group in groups:
            if group == fVal.group:
                continue
            name = p.friend.groups.get(group)
            if not name:
                continue
            ret.append(gbk2unicode(name))

        ret = uiUtils.array2GfxAarry(ret)
        return ret

    def _getFVal(self, arg):
        fid = int(arg[3][0].GetString())
        p = BigWorld.player()
        fVal = p.getFValByGbId(fid)
        return fVal

    def beginChat(self, fid, npcId = 0):
        p = BigWorld.player()
        if fid == const.FRIEND_NPC_ID:
            npcInfo = self.getNpcInfo(npcId, False)
            npcMsgs = p.npcFavor.npcMsgDic.get(npcId, [])
            msgs = [ p.createNpcChatMsg(npcId, msg.get('msg', '')) for msg in npcMsgs ]
            if not msgs and p.needPushNpcQuest(npcId) and not gameglobal.rds.ui.chatToFriend.isOpened(str(-npcId)):
                content = GMD.data.get(GMDD.data.NPC_FRIEND_FAVOR_PUSH, {}).get('text', 'GMDD.data.NPC_FRIEND_FAVOR_PUSH')
                msgs.append(p.createNpcChatMsg(npcId, content))
            gameglobal.rds.ui.chatToFriend.show(msgs, p._createNpcFriendData(npcInfo), False, False)
        elif fid != const.XINYI_MANAGER_ID:
            fVal = p.getFValByGbId(fid)
            if fVal:
                if gameglobal.rds.ui.chatToFriend.isOpened(fid):
                    pass
                elif gameglobal.rds.ui.groupChat.isChatOpen(fid):
                    gameglobal.rds.ui.chatToFriend.show(None, p._createFriendData(fVal), False, True)
                    gameglobal.rds.ui.friend.removeMinChat(fid)
                elif not p.handleFriendMsg(0, fid):
                    gameglobal.rds.ui.chatToFriend.show(None, p._createFriendData(fVal), False, True)
                    if fid in self.minChatArr:
                        self.removeMinChat(fid)
                p.base.checkFriendState(fid)
        elif gameglobal.rds.ui.groupChat.isChatOpen(fid) or gameglobal.rds.ui.chatToFriend.isOpened(fid):
            pass
        else:
            xinYiData = self.createXinYiManagerData()
            if xinYiData:
                if not p.handleFriendMsg(0, fid):
                    gameglobal.rds.ui.chatToFriend.show(None, xinYiData, False, True)
                    if fid in self.minChatArr:
                        self.removeMinChat(fid)

    def removeFriend(self, fid):
        p = BigWorld.player()
        fVal = p.getFValByGbId(fid)
        group = gametypes.FRIEND_GROUP_FRIEND
        if fVal:
            if p.isGlobalFriendVal(fVal):
                if self.enableGlobalFriend():
                    msg = gameStrings.TEXT_FRIENDPROXY_923 % fVal.name
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.base.removeRemoteFriend, fid))
            else:
                REMOVE_FRIEND_INTIMACY_NOTIFY_LV = ICD.data.get('REMOVE_FRIEND_INTIMACY_NOTIFY_LV', 5)
                if fVal.acknowledge and fVal.intimacyLv >= REMOVE_FRIEND_INTIMACY_NOTIFY_LV:
                    self.deleteFriendWithCipher(fid)
                else:
                    if fVal.acknowledge and fVal.intimacy > 0:
                        msg = gameStrings.TEXT_FRIENDPROXY_932 % fVal.name
                    else:
                        msg = gameStrings.TEXT_FRIENDPROXY_923 % fVal.name
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.removeFriend, fid, group))

    @ui.checkInventoryLock()
    def deleteFriendWithCipher(self, fId):
        p = BigWorld.player()
        fVal = p.friend.get(fId)
        if fVal.acknowledge and fVal.intimacy > 0:
            msg = gameStrings.TEXT_FRIENDPROXY_932 % fVal.name
        else:
            msg = gameStrings.TEXT_FRIENDPROXY_923 % fVal.name
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.base.deleteFriendWithCipher, fId, p.cipherOfPerson))

    def moveToBlack(self, fid):
        p = BigWorld.player()
        fVal = p.getFValByGbId(fid)
        if fVal:
            msg = gameStrings.TEXT_FRIENDPROXY_953 % fVal.name
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doMoveToBlack, fid))

    def doMoveToBlack(self, fid):
        p = BigWorld.player()
        if p.friend.isEnemy(fid):
            p.base.deleteEnemy(fid, gametypes.FRIEND_GROUP_BLOCK)
        else:
            p.base.addContactByGbId(fid, gametypes.FRIEND_GROUP_BLOCK, 0)

    def viewChatLog(self, fid):
        p = BigWorld.player()
        if fid != const.XINYI_MANAGER_ID:
            fVal = p.getFValByGbId(fid)
            if fVal:
                if gameglobal.rds.ui.chatToFriend.isShowed(fid):
                    gameglobal.rds.ui.chatToFriend.openHistory(fid)
                else:
                    gameglobal.rds.ui.chatToFriend.show(None, p._createFriendData(fVal), True)
        else:
            xinYi = p.xinYiManager
            if xinYi:
                if gameglobal.rds.ui.chatToFriend.isShowed(fid):
                    gameglobal.rds.ui.chatToFriend.openHistory(fid)
                else:
                    gameglobal.rds.ui.chatToFriend.show(None, self.createXinYiManagerData(), True)

    def moveOutBlack(self, fid):
        p = BigWorld.player()
        p.base.addContactByGbId(fid, gametypes.FRIEND_GROUP_FRIEND, 0)

    def deletePeople(self, fid, group = 0):
        p = BigWorld.player()
        fVal = p.getFValByGbId(fid)
        if fVal:
            p.removeFriend(fid, group or fVal.group)

    def onCanInviteGuild(self, *arg):
        return GfxValue(gameglobal.rds.ui.chat.canInviteGuild())

    def checkFriendToMove(self, group, groupName):
        if self.fidToMove and groupName == self.groupToAdd:
            BigWorld.player().base.addContactByGbId(self.fidToMove, group, 0)
            self.fidToMove = None
            self.groupToAdd = None

    def onShowNewGroupBox(self, *arg):
        isNew = arg[3][0].GetBool()
        fid = arg[3][1].GetString()
        self.showNewGroupBox(isNew, fid)

    def showNewGroupBox(self, isNew, fid):
        self.isNewGroup = isNew
        if fid:
            fid = int(fid)
            self.fidToMove = fid
        else:
            self.fidToMove = None
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_NEW_GROUP_BOX)

    def onCloseNewGroupBox(self, *arg):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_NEW_GROUP_BOX)
        self.isNewGroup = True

    def onGetGroupMenu(self, *arg):
        p = BigWorld.player()
        group = p.friend.getGroupByName(unicode2gbk(arg[3][0].GetString()))
        if not group or group == gametypes.FRIEND_GROUP_GLOBAL_FRIEND:
            return uiUtils.array2GfxAarry([])
        self.menuGroup = group
        if p.friend.isCustomGroup(group):
            ret = [[gbk2unicode(gameStrings.TEXT_FRIENDPROXY_1029), OP_CHAT_TO_GROUP], [gbk2unicode(gameStrings.TEXT_FRIENDPROXY_1030), OP_RENAME_GROUP], [gbk2unicode(gameStrings.TEXT_FRIENDPROXY_1031), OP_DELETE_GROUP]]
        elif self.selectedTab == 'player':
            ret = [[gbk2unicode(gameStrings.TEXT_FRIENDPROXY_1029), OP_CHAT_TO_GROUP], [gbk2unicode(gameStrings.TEXT_FRIENDPROXY_1030), OP_RENAME_GROUP]]
        else:
            ret = []
        if self.selectedTab == 'player':
            if len(p.friend.getFriendGroups()) < const.FRIEND_CUSTOM_GROUP_MAX:
                ret.insert(0, [gbk2unicode(gameStrings.TEXT_FRIENDPROXY_362), OP_NEW_GROUP])
            if group != p.friend.defaultGroup and group != gametypes.FRIEND_GROUP_APPRENTICE:
                ret.insert(0, [gbk2unicode(gameStrings.TEXT_FRIENDPROXY_1042), OP_SET_DEFALUT_GROUP])
            if p.friend.isOrderAbleGroup(group):
                groupOrder = p.getFriendGroupOrder()
                if group in groupOrder:
                    if groupOrder.index(group) != 0:
                        ret.insert(0, [gbk2unicode(gameStrings.TEXT_FRIENDPROXY_1047), OP_UP_GROUP])
                    if groupOrder.index(group) != len(groupOrder) - 1:
                        ret.insert(0, [gbk2unicode(gameStrings.TEXT_FRIENDPROXY_1050), OP_DOWN_GROUP])
        ret = uiUtils.array2GfxAarry(ret)
        return ret

    def onClickGroupMenu(self, *arg):
        groupName = unicode2gbk(arg[3][0].GetString())
        menuIdx = int(arg[3][1].GetString())
        p = BigWorld.player()
        group = p.friend.getGroupByName(groupName)
        if not group:
            return
        else:
            self.groupName = groupName
            if menuIdx == OP_RENAME_GROUP:
                self.showRenameGroupBox()
            elif menuIdx == OP_DELETE_GROUP:
                if not p.friend.hasFriendInCustomGroup(group):
                    msg = gameStrings.TEXT_FRIENDPROXY_1066 % groupName
                else:
                    msg = gameStrings.TEXT_FRIENDPROXY_1068 % groupName
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.base.deleteFriendGroup, group))
            elif menuIdx == OP_CHAT_TO_GROUP:
                gameglobal.rds.ui.chatToFriend.showChatGroup(group)
            elif menuIdx == OP_NEW_GROUP:
                self.showNewGroupBox(True, None)
            elif menuIdx == OP_SET_DEFALUT_GROUP:
                p.base.updateFriendDefaultGroup(group)
            elif menuIdx in (OP_UP_GROUP, OP_DOWN_GROUP):
                if p.friend.isOrderAbleGroup(group):
                    groupOrder = p.getFriendGroupOrder()
                else:
                    return
                idx = groupOrder.index(group)
                groupOrder.remove(group)
                if menuIdx == OP_UP_GROUP:
                    idx -= 1
                else:
                    idx += 1
                groupOrder.insert(idx, group)
                p.base.updateFriendGroupOrder(groupOrder)
            return

    def onMoveToGroup(self, *arg):
        fid = int(arg[3][0].GetString())
        groupName = unicode2gbk(arg[3][1].GetString())
        self.moveToGroup(fid, groupName)

    def moveToGroup(self, fid, groupName):
        p = BigWorld.player()
        group = p.friend.getGroupByName(groupName)
        p.base.addContactByGbId(fid, group, 0)

    def onIsNewGroup(self, *arg):
        return GfxValue(self.isNewGroup)

    def onRenameGroup(self, *arg):
        oldName = unicode2gbk(arg[3][0].GetString())
        newName = unicode2gbk(arg[3][1].GetString())
        p = BigWorld.player()
        oldGroup = p.friend.getGroupByName(oldName)
        if not oldGroup:
            self.closeRenameGroupBox()
            return
        p.base.renameFriendGroup(oldGroup, newName)
        self.closeRenameGroupBox()

    def onGetOldGroupName(self, *arg):
        return GfxValue(gbk2unicode(self.groupName))

    def showRenameGroupBox(self):
        self.isNewGroup = False
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_NEW_GROUP_BOX)

    def closeRenameGroupBox(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_NEW_GROUP_BOX)
        self.isNewGroup = True

    def onSearchFriend(self, *arg):
        if not gameglobal.rds.configData.get('enableRecommendFriend', False):
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SEARCH_FRIEND)
        else:
            gameglobal.rds.ui.recommendSearchFriend.show()

    def onCloseSearchPanel(self, *arg):
        self.closeSearchPanel()

    def closeSearchPanel(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SEARCH_FRIEND)
        self.uiAdapter.migrateServer.closePanel()
        self.searchHostId = int(gameglobal.rds.g_serverid)

    def onExactSearchFriend(self, *arg):
        playerName = unicode2gbk(arg[3][0].GetString())
        if self.isSearchSameSever():
            BigWorld.player().base.searchFriendByName(gametypes.SEARCH_PLAYER_FOR_FRIEND, playerName)
        else:
            BigWorld.player().base.queryGlobalFriendByName(self.searchHostId, playerName)

    def onConditionSearchFriend(self, *arg):
        pass

    def onGetConditionInfo(self, *arg):
        return []

    def onGetTab(self, *arg):
        return GfxValue(self.selectedTab)

    def onGetIsBindYixin(self, *arg):
        fid = int(arg[3][0].GetString())
        p = BigWorld.player()
        fVal = p.getFValByGbId(fid)
        if not fVal:
            return GfxValue(False)
        return GfxValue(fVal.yixinOpenId)

    def onGetTeamMenu(self, *arg):
        fid = int(arg[3][0].GetString())
        menu = []
        p = BigWorld.player()
        fVal = p.getFValByGbId(fid)
        if not fVal:
            return uiUtils.array2GfxAarry(menu)
        target = fVal.getEntity()
        if not p.friend.isFriend(fid) and not p.friend.isBlock(fid):
            menu.append(gbk2unicode(gameStrings.TEXT_FRIENDPROXY_1176))
        if not target:
            if fVal.state in gametypes.FRIEND_VISIBLE_STATES:
                menu.append(gbk2unicode(gameStrings.TEXT_FRIENDPROXY_1179))
                menu.append(gbk2unicode(gameStrings.TEXT_FRIENDPROXY_1180))
        else:
            if p.canApplyTeam(target):
                menu.append(gbk2unicode(gameStrings.TEXT_FRIENDPROXY_1179))
            if p.canInviteTeam(target):
                menu.append(gbk2unicode(gameStrings.TEXT_FRIENDPROXY_1180))
        if p.friend.isVisible(fVal.state):
            menu.append(gbk2unicode(gameStrings.TEXT_FRIENDPROXY_1187))
            menu.append(gbk2unicode(gameStrings.TEXT_FRIENDPROXY_1188))
        return uiUtils.array2GfxAarry(menu)

    def onAutoSetToLeave(self, *arg):
        state = arg[3][0].GetBool()
        p = BigWorld.player()
        p.base.setFriendOption(gametypes.FRIEND_OPTION_AUTO_AWAY, state)

    def onGetAutoLeaveState(self, *arg):
        p = BigWorld.player()
        return GfxValue(p.friend.getOption(gametypes.FRIEND_OPTION_AUTO_AWAY))

    def onShowChatToFriend(self, *arg):
        fid = int(arg[3][0].GetString())
        self.beginChat(fid)

    def onCloseMinChat(self, *arg):
        fid = int(arg[3][0].GetString())
        self.removeMinChat(fid)

    def onCloseNotice(self, *arg):
        fid = int(arg[3][0].GetString())
        self.removeNotice(fid)

    def setSearchResult(self, infoList):
        if self.searchMediator != None:
            info = []
            for gbId, name, level, spaceNo, areaId, school, isOnline, photo, sex, combatScore in infoList:
                spaceName = self._getLastPlace(spaceNo, areaId)
                info.append([gbk2unicode(name),
                 str(level),
                 gbk2unicode(spaceName),
                 gbk2unicode(SD.data[school]['name']),
                 str(gbId),
                 isOnline])

            self.searchMediator.Invoke('setSearchResult', uiUtils.array2GfxAarry(info))

    def _getLastPlace(self, spaceNo, areaId = None):
        return formula.whatFubenType(formula.getFubenNo(spaceNo)) in const.FB_TYPE_ARENA and gameStrings.TEXT_FRIENDPROXY_1225 or formula.whatAreaName(spaceNo, areaId, includeMLInfo=True)

    def addMinChat(self, info):
        if info[0] not in self.minChatArr:
            if len(self.minChatArr) >= 6 and info[0] != const.XINYI_MANAGER_ID:
                gameglobal.rds.ui.systemTips.show(gameStrings.TEXT_FRIENDPROXY_1231)
            else:
                self.minChatArr.append(info[0])
                if len(info) >= 3:
                    self.chatArrIdMap[info[0]] = info[2]
                info[0] = str(info[0])
                self.addMinChatIcon(info)
        elif info[0] == const.XINYI_MANAGER_ID:
            info[0] = str(info[0])
            self.addMinChatIcon(info)

    @ui.checkWidgetLoaded(uiConst.WIDGET_MIN_CHAT)
    def addMinChatIcon(self, info):
        if self.minChatMediator:
            self.minChatMediator.Invoke('addMinChat', uiUtils.array2GfxAarry(info, True))

    def removeMinChat(self, fid):
        if self.minChatMediator != None:
            if fid in self.minChatArr:
                self.minChatArr.remove(fid)
                if fid in self.chatArrIdMap.keys():
                    self.chatArrIdMap.pop(fid)
                self.minChatMediator.Invoke('removeMinChat', GfxValue(str(fid)))

    @ui.checkWidgetLoaded(uiConst.WIDGET_MIN_CHAT)
    def minChatShine(self, fid, shine):
        if self.minChatMediator != None:
            self.minChatMediator.Invoke('minChatShine', (GfxValue(str(fid)), GfxValue(shine)))

    @ui.checkWidgetLoaded(uiConst.WIDGET_FRIEND_NOTICE)
    def addNotice(self, info):
        if self.noticeMediator != None:
            info[0] = str(info[0])
            info[1] = gbk2unicode(info[1])
            info[2] = gbk2unicode(info[2])
            self.noticeMediator.Invoke('addNotice', uiUtils.array2GfxAarry(info))

    def removeNotice(self, fid):
        if self.noticeMediator != None:
            self.noticeMediator.Invoke('removeNotice', GfxValue(str(fid)))

    def onSetSignature(self, *arg):
        signature = unicode2gbk(arg[3][0].GetString())
        p = BigWorld.player()
        result, _ = taboo.checkNameDisWord(signature)
        if not result:
            p.showGameMsg(GMDD.data.FRIEND_SIGNATURE_TABOO, ())
            return
        p.base.updateFriendSignature(signature)

    def onSetSignatureShow(self, *arg):
        showsig = arg[3][0].GetBool()
        p = BigWorld.player()
        p.base.updateFriendShowsig(showsig)

    def setShowsig(self, show):
        if self.mediator:
            self.mediator.Invoke('setBtnState', GfxValue(show))

    def onSetting(self, *arg):
        gameglobal.rds.ui.gameSetting.show(uiConst.GAME_SETTING_BG_V2_TAB_PERSONAL)

    def onShowSprite(self, *arg):
        if gameglobal.rds.configData.get('enableFriendInvite', False):
            if gameglobal.rds.configData.get('enableInvitePoint', False):
                if gameglobal.rds.configData.get('enableSummonFriendV2', False):
                    gameglobal.rds.ui.summonFriendBGV2.show()
                else:
                    gameglobal.rds.ui.summonFriendNew.show()
            else:
                gameglobal.rds.ui.summonFriend.show(0)

    def showProfile(self):
        pass

    def _formatProviderData(self, arr):
        ret = []
        for ar in arr:
            ret.append({'label': ar})

        return ret

    def onGetSelfProfile(self, *arg):
        return uiUtils.dict2GfxDict(self.result, True)

    def onShowIcon(self, *arg):
        pass

    def getSelfProfile(self):
        self._getSelfProfile()

    def _getSelfProfile(self):
        p = BigWorld.player()
        constellation = p.friend.constellation
        month = p.friend.birthmonth
        day = p.friend.birthday
        age = 0
        province = p.friend.province
        city = p.friend.city
        desc = p.friend.description
        if p.friend.onlineTime and TIME_JOIN_CHAR in p.friend.onlineTime:
            timeBegin, timeEnd = p.friend.onlineTime.split(TIME_JOIN_CHAR)
        else:
            timeBegin, timeEnd = ('00:00', '00:00')
        defaultPhoto = 'headIcon/%s.dds' % str(p.school * 10 + p.physique.sex)
        pVisible = p.friend.pvisibility
        provinces = self._formatProviderData(self.provinces)
        cityNames = FLD.data.get(province, {}).get('cityNames', [])
        cities = self._formatProviderData(cityNames)
        status = p.profileIconStatus
        if not p.imageName:
            status = -1
        isCustomRadioUsed = self.isCustomRadioUsed
        if p.profileIconStatus == gametypes.NOS_FILE_STATUS_APPROVED and gameglobal.rds.configData.get('enableCustomRadio', False):
            isCustomRadioUsed = True
        self.result = {'month': month,
         'day': day,
         'constellation': constellation,
         'age': age,
         'provinceIndex': province,
         'cityIndex': city,
         'desc': desc,
         'provinces': provinces,
         'cities': cities,
         'pVisible': pVisible,
         'defaultPhoto': defaultPhoto,
         'isCustomRadioUsed': isCustomRadioUsed,
         'status': status,
         'isProfileIconUsed': p.profileIconUsed,
         'iconUpload': p.iconUpload,
         'sex': p.physique.sex,
         'yixin': p.yixinOpenId if p.yixinOpenId else gameStrings.TEXT_FRIENDPROXY_1353,
         'lv': p.lv,
         'timeBegin': timeBegin,
         'timeEnd': timeEnd,
         'timeProvider': uiUtils.getTimesProvider()}

    def onGetCities(self, *arg):
        index = int(arg[3][0].GetString())
        cityNames = FLD.data.get(index, {}).get('cityNames', [])
        cities = self._formatProviderData(cityNames)
        return uiUtils.array2GfxAarry(cities, True)

    def onCloseSelfProfile(self, *arg):
        self.closeProfile()

    def onSaveProfile(self, *arg):
        pvisibility = int(arg[3][0].GetNumber())
        photo = self.getPhotoFileName(arg[3][1].GetString())
        birthmonth = int(arg[3][2].GetNumber())
        birthday = int(arg[3][3].GetNumber())
        constellation = 0
        bloodType = 0
        province = int(arg[3][4].GetNumber())
        city = int(arg[3][5].GetNumber())
        qq = ''
        description = unicode2gbk(arg[3][6].GetString())
        timeBegin = unicode2gbk(arg[3][7].GetString())
        timeEnd = unicode2gbk(arg[3][8].GetString())
        isNormal, description = taboo.checkDisbWord(description)
        if not isNormal:
            BigWorld.player().showGameMsg(GMDD.data.CHAT_TABOO_WORD, ())
            return
        onlineTime = TIME_JOIN_CHAR.join((timeBegin, timeEnd))
        sex = BigWorld.player().physique.sex
        BigWorld.player().base.updateProfile(pvisibility, photo, constellation, birthmonth, birthday, sex, bloodType, province, city, qq, description, onlineTime)

    def onOtherFunc(self, *args):
        p = BigWorld.player()
        funcType = int(args[3][0].GetNumber())
        fid = int(args[3][1].GetString())
        fVal = p.getFValByGbId(fid)
        if not fVal:
            return
        if funcType == FUNC_BAISHI:
            p.cell.applyMentor(fVal.name)
        elif funcType == FUNC_SHOU_TU:
            p.cell.applyApprentice(fVal.name)
        elif funcType == FUNC_KICK_MENTOR:
            p.cell.kickMentor()
        elif funcType == FUNC_KICK_APPRENTICE:
            p.base.kickApprentice(fVal.gbId)

    def getPhotoFileName(self, photo):
        photoName = os.path.basename(photo)
        if uiUtils.isDownloadImage(photoName):
            return photoName.split('.')[0]
        if photoName == 'oldPhoto':
            return BigWorld.player().friend.photo.split('.')[0]
        return ''

    def onShowProfile(self, *arg):
        p = BigWorld.player()
        p.getPersonalSysProxy().openZoneMyself(const.PERSONAL_ZONE_SRC_FRIEND)

    @ui.callFilter(2)
    def onViewFriendProfile(self, *arg):
        gbId = int(arg[3][0].GetString())
        if self.isSearchSameSever():
            p = BigWorld.player()
            p.getPersonalSysProxy().openZoneOther(gbId)

    def viewFriendProfile(self, gbId, srcId = 0):
        if self.otherGbId == gbId:
            return
        fVal = BigWorld.player().getFValByGbId(gbId)
        dbId = fVal.dbID if fVal else 0
        BigWorld.player().base.viewFriendProfile(gbId, dbId, srcId)

    def showOtherProfile(self, gbId, data):
        pass

    def _createOtherProfile(self):
        p = BigWorld.player()
        fVal = p.getFValByGbId(self.otherGbId)
        photo = self.otherData[1]
        if not photo and fVal:
            photo = p._getFriendPhoto(fVal)
        if uiUtils.isDownloadImage(photo):
            if p.isGlobalFriendVal(fVal):
                p.downloadCrossNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, int(p.globalFriends.friends.get(fVal.gbId).server), gametypes.NOS_FILE_PICTURE, None, (None,))
            else:
                p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, self.onDownloadOtherPhoto, (None,))
            photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
        month = max(1, self.otherData[3])
        day = max(1, self.otherData[4])
        constellation = uiUtils.getConstellation(month, day)
        sex = self.otherData[5]
        province = self.provinces[self.otherData[7]]
        citys = FLD.data.get(self.otherData[7], {}).get('cityNames', [])
        index = min(len(citys) - 1, self.otherData[8])
        city = citys[index]
        desc = self.otherData[10]
        onlineTime = self.otherData[11] if self.otherData[11] else gameStrings.TEXT_FRIENDPROXY_1457
        roleName = self.otherData[12]
        level = self.otherData[13]
        school = self.otherData[14]
        guildName = self.otherData[15] if self.otherData[15] else gameStrings.TEXT_GM_COMMAND_GUILD_545
        deleted = fVal.deleted if fVal else False
        ret = {'month': month,
         'day': day,
         'constellation': constellation,
         'province': province,
         'city': city,
         'desc': desc,
         'photo': photo,
         'sex': sex,
         'lv': level,
         'school': const.SCHOOL_DICT.get(school, ''),
         'roleName': roleName,
         'fid': str(self.otherGbId),
         'guildName': guildName,
         'onlineTime': onlineTime,
         'deleted': deleted,
         'isFriend': bool(fVal)}
        if self.uiAdapter.mentor.enableApprentice():
            if hasattr(p, 'mentorGbId') and p.mentorGbId == self.otherGbId:
                ret['funcType'] = FUNC_KICK_MENTOR
                ret['funcLabel'] = gameStrings.TEXT_FRIENDPROXY_1476
            elif p.getApprenticeInfo(self.otherGbId):
                ret['funcType'] = FUNC_KICK_APPRENTICE
                ret['funcLabel'] = gameStrings.TEXT_FRIENDPROXY_1476
            elif p.checkMentorCondition() and level <= ACD.data.get('maxApprenticeLv', 50) and level >= ACD.data.get('minApprenticeLv', 19):
                ret['funcType'] = FUNC_SHOU_TU
                ret['funcLabel'] = gameStrings.TEXT_FRIENDPROXY_1483
            elif p.checkApprenticeCondition() and not getattr(p, 'mentorGbId', None) and level >= ACD.data.get('minMentorLv', 50):
                ret['funcType'] = FUNC_BAISHI
                ret['funcLabel'] = gameStrings.TEXT_FRIENDPROXY_1487
        return uiUtils.dict2GfxDict(ret, True)

    def onGetOtherProfile(self, *arg):
        return self._createOtherProfile()

    def onCloseOtherProfile(self, *arg):
        pass

    def onSelectFile(self, *arg):
        if hasattr(C_ui, 'ayncOpenFileDialog'):
            workPath = os.getcwd()
            C_ui.ayncOpenFileDialog(gameStrings.TEXT_CHARACTERDETAILADJUSTPROXY_1174, gameStrings.TEXT_FRIENDPROXY_1501, workPath, self.doSelectFile)

    def doSelectFile(self, path):
        if not os.path.exists(path):
            return
        if '.' in os.path.basename(os.path.splitext(path)[0]):
            gameglobal.rds.ui.messageBox.showMsgBox(GMD.data.get(GMDD.data.PICTURE_NAME_ILLEGAL, {}).get('text', gameStrings.TEXT_FRIENDPROXY_1507))
            return
        if not (path.endswith('.jpg') or path.endswith('.png') or path.endswith('.jpeg')):
            gameglobal.rds.ui.messageBox.showMsgBox(GMD.data.get(GMDD.data.PICTURE_SUFFIX_NAME_ILLEGAL, {}).get('text', gameStrings.TEXT_FRIENDPROXY_1510))
            return
        photoFileName = os.path.basename(path)
        fileName = photoFileName.split('.')[0]
        self.srcResPath = const.IMAGES_DOWNLOAD_DIR + '/' + photoFileName
        self.imagePath = const.IMAGES_DOWNLOAD_DIR + '/' + fileName + '.dds'
        BigWorld.player().cell.updateImageName(fileName)
        try:
            uiUtils.copyToImagePath(path)
            im = Image.open(self.srcResPath)
            im = im.resize((256, 256))
            im.save(self.srcResPath)
            BigWorld.convert2DXT5(self.srcResPath, const.IMAGES_DOWNLOAD_DIR)
        except:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_FRIENDPROXY_1525)
            return

    def onUploadFile(self, *arg):
        p = BigWorld.player()
        if self.imagePath == '':
            return
        profileIconUpLoadInterval = GCD.data.get('profileIconUpLoadInterval', 3600)
        now = utils.getNow()
        if now - p.profileIconLastUploadTimestamp < profileIconUpLoadInterval:
            delta = profileIconUpLoadInterval - (now - p.profileIconLastUploadTimestamp)
            p.showGameMsg(GMDD.data.USE_DEFINE_FILE_TIME_LIMIT, (utils.formatDuration(delta),))
            return
        if self.imageHeight > const.IMAGES_HEIGHT or self.imageWidth > const.IMAGES_WIDTH:
            p.showGameMsg(GMDD.data.USE_DEFINE_FILE_NON_STANDARD, ())
            return
        if not p.useIconUploadItemFlag:
            itemId, amount = SCD.data.get('friendIconUploadItem', (0, 0))
            if itemId:
                myswap = p.inv.countItemInPages(itemId, enableParentCheck=True)
                if myswap >= amount:
                    count = '%d/%d' % (myswap, amount)
                else:
                    count = "<font color=\'#FF0000\'>%d/%d</font>" % (myswap, amount)
                itemInfo = uiUtils.getGfxItemById(itemId, count=count)
                p.showGameMsg(GMDD.data.USE_DEFINE_FILE_NON_ITEM, ID.data[itemId]['name'])
                msg = uiUtils.getTextFromGMD(GMDD.data.UPLOAD_FILE_ITEM_ALERT)
                if msg:
                    msg = msg % uiUtils.getItemColorName(itemId)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.showUploadTime, itemData=itemInfo)
        else:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_FRIENDPROXY_1561 % utils.formatDuration(profileIconUpLoadInterval), self.realUpload)

    def showUploadTime(self):
        itemId, amount = SCD.data.get('friendIconUploadItem', (0, 0))
        p = BigWorld.player()
        if not p.inv.canRemoveItems({itemId: amount}, enableParentCheck=True):
            p.showGameMsg(GMDD.data.CUSTOM_NEED_ITEM, ID.data.get(itemId, {}).get('name', gameStrings.TEXT_FRIENDPROXY_1568))
        else:
            profileIconUpLoadInterval = GCD.data.get('profileIconUpLoadInterval', 3600)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_FRIENDPROXY_1561 % utils.formatDuration(profileIconUpLoadInterval), self.realUpload)

    def realUpload(self):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableNOSCustom', False):
            p.showGameMsg(GMDD.data.UPLOAD_FRIEND_ICON_UNAVAILABLE, ())
            return None
        else:
            p.uploadNOSFile(self.imagePath, gametypes.NOS_FILE_PICTURE, gametypes.NOS_FILE_SRC_FRIEND_ICON, {'gbId': p.gbId,
             'roleName': p.realRoleName}, self.onNOSServiceDone, (None,))
            return None

    def onNOSServiceDone(self, key, otherArgs):
        p = BigWorld.player()
        if key:
            if p.profileIconStatus == gametypes.NOS_FILE_STATUS_PENDING or p.profileIconStatus == gametypes.NOS_FILE_STATUS_APPROVED and p.profileIcon != p.friend.photo:
                p.base.abandonNOSFile(p.profileIcon)
            p.cell.updateProfileData(key, gametypes.NOS_FILE_STATUS_PENDING, False, True)
        else:
            p.showGameMsg(GMDD.data.USE_CUSTOM_PHOTO_UPLOAD_FAIL, ())

    def onGetUserDefineDDSSucc(self, *arg):
        self.imageHeight = int(arg[3][0].GetNumber())
        self.imageWidth = int(arg[3][1].GetNumber())

    def onDownloadPhoto(self, status, callbackArgs):
        p = BigWorld.player()
        photo = 'headIcon/%s.dds' % str(p.school * 10 + p.physique.sex)
        if status == gametypes.NOS_FILE_STATUS_APPROVED:
            photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + p.friend.photo + '.dds'
        self.refreshRoleIcon(photo)

    def refreshRoleIcon(self, photo):
        if self.mediator:
            self.mediator.Invoke('refreshRoleIcon', GfxValue(gbk2unicode(photo)))

    @ui.callAfterTime(0.5)
    def onDownloadFriendPhoto(self, status, callbackArgs):
        self.refreshFriendList()

    def onDownloadSelfProfilePhoto(self, status, callbackArgs):
        p = BigWorld.player()
        p.cell.updateProfileIconStatus(status)
        p.profileIconStatus = status
        self.photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + p.imageName + '.dds'
        if status == gametypes.NOS_FILE_STATUS_APPROVED:
            self.photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + p.profileIcon + '.dds'
        self.getSelfProfile()

    def onDownloadOtherPhoto(self, status, callbackArgs):
        p = BigWorld.player()
        fVal = p.getFValByGbId(self.otherGbId)
        if not fVal:
            return
        photo = 'headIcon/%s.dds' % str(fVal.school * 10 + fVal.sex)
        if status == gametypes.NOS_FILE_STATUS_APPROVED:
            photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + fVal.photo + '.dds'

    def onIsCustomRadioUsed(self, *arg):
        state = arg[3][0].GetBool()
        self.isCustomRadioUsed = state

    def onApplyIcon(self, *arg):
        p = BigWorld.player()
        p.base.abandonNOSFile(p.friend.photo)
        p.cell.updateProfileApply(True, False)

    def onAddToFriend(self, *arg):
        fid = int(arg[3][0].GetString())
        p = BigWorld.player()
        if p.friend.isEnemy(fid):
            fVal = p.getFValByGbId(fid)
            msg = gameStrings.TEXT_FRIENDPROXY_1641 % fVal.name
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onAddToFriendAccept, fid))
        else:
            self.onAddToFriendAccept(fid)

    def onAddToFriendAccept(self, gbId):
        p = BigWorld.player()
        if p.friend.isEnemy(gbId):
            p.base.deleteEnemy(gbId, True)
        elif not self.isSearchSameSever():
            p.base.addRemoteFriendRequest(self.searchHostId, gbId)
        else:
            group = p.friend.defaultGroup if p.friend.defaultGroup else gametypes.FRIEND_GROUP_FRIEND
            p.base.addContactByGbId(gbId, group, const.FRIEND_SRC_SEARCH_FRIEND)

    def onGetConstellation(self, *args):
        m = int(args[3][0].GetNumber())
        d = int(args[3][1].GetNumber())
        return GfxValue(gbk2unicode(uiUtils.getConstellation(m, d)))

    def onSetExpand(self, *args):
        groupName = unicode2gbk(args[3][0].GetString())
        expand = args[3][1].GetBool()
        self.expandHistory[groupName] = expand

    def refreshIcon(self, photoPath):
        pass

    def invitedCC(self, fid):
        isCCVersion = gameglobal.rds.configData.get('isCCVersion', False)
        if isCCVersion == True:
            fVal = BigWorld.player().getFValByGbId(fid)
            name = fVal.name
            p = BigWorld.player()
            p.inviteOtherToCC(name)

    def addYixinFriend(self, fid):
        p = BigWorld.player()
        if not hasattr(p, 'addYixinFriendList'):
            p.addYixinFriendList = {}
        if p.addYixinFriendList.has_key(fid):
            passTime = BigWorld.player().getServerTime() - p.addYixinFriendList[fid]
            if passTime < 3000:
                p.showGameMsg(GMDD.data.YIXIN_ERR_MAX_ADD_FRIEND_FREQUENT, ())
                return
        p.addYixinFriendList[fid] = BigWorld.player().getServerTime()
        p.base.addYixinFriend(fid)

    def isShowCC(self, *arg):
        isCCVersion = gameglobal.rds.configData.get('isCCVersion', False)
        return GfxValue(isCCVersion)

    def isShowYixin(self, *arg):
        isShowYixin = gameglobal.rds.configData.get('enableYixin', False)
        return GfxValue(isShowYixin)

    def isBindYixin(self, *arg):
        return GfxValue(BigWorld.player().yixinOpenId)

    def showAddRemark(self, fid):
        self.hideRemark()
        self.remarkType = REMARK_TYPE_ADD
        self.remarkFid = fid
        self.uiAdapter.loadWidget(uiConst.WIDGET_ADD_FREIND_REAMRK)

    def showModifyRemark(self, fid):
        self.hideRemark()
        self.remarkType = REMARK_TYPE_MODIFY
        self.remarkFid = fid
        self.uiAdapter.loadWidget(uiConst.WIDGET_ADD_FREIND_REAMRK)

    def hideRemark(self):
        if self.remarkType == REMARK_TYPE_ADD and self.remarkFid:
            self.beginChat(self.remarkFid)
            self.remarkFid = 0
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ADD_FREIND_REAMRK)

    def onFriendAdded(self, fid):
        if BigWorld.player().friend.isFriend(fid):
            self.hideRemark()
            self.remarkType = REMARK_TYPE_FRIST_ADD
            self.remarkFid = fid
            self.uiAdapter.loadWidget(uiConst.WIDGET_ADD_FREIND_REAMRK)

    def getSuggestRemark(self, fVal):
        if not fVal:
            return ''
        remarkName = SCD.data.get('remarkSrcNames', {}).get(fVal.srcId, '')
        if remarkName:
            return gameStrings.TEXT_COMMON_SERVER_WORLDWAR_260 % (remarkName, fVal.name)
        return fVal.name

    def onRemarkFriend(self, *args):
        fid = int(args[3][0].GetString())
        remarkName = unicode2gbk(args[3][1].GetString()).strip()
        result, _ = taboo.checkNameDisWord(remarkName)
        if not result:
            BigWorld.player().showGameMsg(GMDD.data.CHAT_TABOO_WORD, ())
            return
        self.hideRemark()
        fVal = BigWorld.player().getFValByGbId(fid)
        if fVal and fVal.remarkName != remarkName:
            BigWorld.player().base.updateFriendRemarkName(fVal.gbId, remarkName)

    def onGetScoFriendInfo(self, *args):
        fid = int(args[3][0].GetString())
        return uiUtils.dict2GfxDict(self.getScoFriendInfo(fid), True)

    def onShowChooseServer(self, *args):
        self.uiAdapter.migrateServer.showServerList(uiConst.CHOOSE_SERVER_TYPE_ALL, self.changeServer)

    def changeServer(self, serverId, serverName):
        self.searchHostId = int(serverId)
        if self.searchMediator:
            self.searchMediator.Invoke('setServerName', GfxValue(gbk2unicode(serverName)))
            self.setSearchResult([])

    def isSearchSameSever(self):
        return int(self.searchHostId) == int(gameglobal.rds.g_serverid)

    def getFamiUpIntimacyLv(self, intimacy):
        for lv, info in CIND.data.items():
            if intimacy >= info.get('minVal', 0) and intimacy <= info.get('maxVal', 0):
                return lv

        return 0

    def getScoFriendInfo(self, fid):
        result = {'isEnableIntimacy': self.isEnableIntimacy(),
         'fid': str(fid)}
        p = BigWorld.player()
        fVal = p.getFValByGbId(fid)
        if not fVal:
            return result
        result['nameMingPai'] = uiUtils.getNameWithMingPain(fVal.name, fVal.mingpaiId)
        result['intimacy'] = fVal.intimacy
        result['intimacyMaxLv'] = ICD.data.get('MAX_INTIMACY_LV', 9)
        result['isFamiIconUp'] = CIND.data.get(1, {}).get('minVal', 0) <= fVal.intimacy
        intimacyUpLv = self.getFamiUpIntimacyLv(fVal.intimacy)
        if result['isFamiIconUp'] and intimacyUpLv:
            result['intimacyLv'] = intimacyUpLv
            result['intimacyName'] = CIND.data.get(intimacyUpLv, {}).get('name', gameStrings.TEXT_FRIENDPROXY_1789)
            result['intimacyFull'] = CIND.data.get(intimacyUpLv, {}).get('maxVal', 0) <= fVal.intimacy
            result['intimacyLvTip'] = '%d + %d' % (fVal.intimacyLv, intimacyUpLv)
        else:
            result['intimacyLv'] = fVal.intimacyLv
            result['intimacyName'] = IND.data.get(fVal.intimacyLv, {}).get('name', gameStrings.TEXT_FRIENDPROXY_1789)
            result['intimacyFull'] = IND.data.get(fVal.intimacyLv, {}).get('maxVal', 0) <= fVal.intimacy
            result['intimacyLvTip'] = '%d' % fVal.intimacyLv
        if not p.isGlobalFriendVal(fVal):
            scoInfo = self.friendsScoInfo.get(fid)
            if scoInfo and scoInfo.get('expireTime', 0) >= utils.getNow():
                result['scoInfo'] = scoInfo.get('scoInfo')
            else:
                self.queryFriendSocInfo(fid)
        return result

    @ui.callInCD(1)
    def queryFriendSocInfo(self, fid):
        BigWorld.player().cell.queryFriendSocInfo(fid)

    def isEnableIntimacy(self):
        return gameglobal.rds.configData.get('enableIntimacy', False)

    def addFriendScoInfo(self, fid, scoInfoData):
        vipInfo = scoInfoData[5]
        combatScore = int(scoInfoData[7])
        if combatScore == 0:
            combatScore = gameStrings.TEXT_FRIENDPROXY_1817
        achievePoint = scoInfoData[8]
        renpinVal = scoInfoData[9]
        guibaoPoint = scoInfoData[10]
        imgDatas = []
        gfxScoData = {'zhangli': combatScore,
         'achiv': achievePoint,
         'imgDatas': imgDatas,
         'renpinVal': renpinVal,
         'enableRenpinVal': gameglobal.rds.configData.get('enableRenpinVal', True)}
        hasVip = vipInfo and vipInfo.get('basicPackage', {}) and int(vipInfo.get('basicPackage', {}).get('tExpire', 0)) > utils.getNow()
        idx = 0
        imgData = list(scoInfoData[:7])
        if gameglobal.rds.configData.get('enableAppearanceRank', False):
            imgData.append(scoInfoData[10])
        for scoItem in imgData:
            tmpInfo = {'icon': 'friend/score/%s.dds' % ICD.data.get('scoIcons', [1000] * len(imgData))[idx],
             'tip': ICD.data.get('scoIconTip', [gameStrings.TEXT_FRIENDPROXY_1834] * len(imgData))[idx]}
            if vipInfo == scoItem:
                if hasVip:
                    tmpInfo['num'] = ''
                    imgDatas.append(tmpInfo)
            elif type(scoItem) == int:
                tmpInfo['num'] = int(scoItem)
                imgDatas.append(tmpInfo)
            elif type(scoItem) == bool and scoItem:
                tmpInfo['num'] = ''
                imgDatas.append(tmpInfo)
            idx += 1

        fVal = BigWorld.player().getFValByGbId(fid)
        isBindYixin = None
        if fVal:
            isBindYixin = fVal.yixinOpenId
        if isBindYixin:
            tmpInfo = {'icon': 'friend/score/11000.dds',
             'tip': gameStrings.TEXT_FRIENDPROXY_1853,
             'color': 'shine',
             'num': ''}
            imgDatas.append(tmpInfo)
        else:
            tmpInfo = {'icon': 'friend/score/11000.dds',
             'tip': gameStrings.TEXT_FRIENDPROXY_1856,
             'color': 'hui',
             'num': ''}
            imgDatas.append(tmpInfo)
        self.friendsScoInfo[fid] = {'expireTime': utils.getNow() + const.FRIEND_SCO_EXPIRE_TIME,
         'scoInfo': gfxScoData}
        if self.mediator:
            self.mediator.Invoke('refreshScoInfo', uiUtils.dict2GfxDict(self.getScoFriendInfo(fid), True))

    def onIsShowCallFriend(self, *args):
        ret = False
        fid = int(args[3][0].GetString())
        if fid in self.inviteList:
            ret = True
        return GfxValue(ret)

    def onIsPartner(self, *args):
        fid = long(args[3][0].GetString())
        p = BigWorld.player()
        if not p.ntPartnerGbId:
            return GfxValue(False)
        ret = fid == p.ntPartnerGbId
        return GfxValue(ret)

    def refreshCallFriendsList(self, inviteList):
        self.inviteList = inviteList
        self.refreshFriendList()

    def setInviteList(self, inviteList, canPush):
        self.inviteList = inviteList
        if self.inviteList and canPush:
            self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_PUSH_CALL)

    def enableGlobalFriend(self):
        return gameglobal.rds.configData.get('enableGlobalFriend', False)

    def saveTeampMsg(self):
        p = BigWorld.player()
        if hasattr(p, 'friend'):
            self.tempMsgs = p.friend.getTempMsg()

    def clearTempMsg(self):
        self.tempMsgs = None

    def initTempMsg(self):
        p = BigWorld.player()
        if hasattr(p, 'friend'):
            p.friend.initTempMsg(self.tempMsgs)
            p._checkBlink()

    def onClickSysMsgBtn(self, *args):
        self.openSystemMessageWnd(const.FRIEND_SYSTEM_NOTIFY_ID)

    def fetchAllRecentMsg(self):
        p = BigWorld.player()
        p.fetchLastChatHistory(p.gbId, isSysHistory=True)
        for gbId in self.recentData:
            p.fetchLastChatHistory(gbId)

    def updateRecentData(self, gbId, msgText):
        msgText = self.convertRichMsg2Text(msgText)
        self.recentData[gbId] = msgText
        if self.mediator and self.selectedTab == 'recent':
            self.mediator.Invoke('refreshRecentGroupPlayerText', (GfxValue(str(gbId)), GfxValue(gbk2unicode(msgText))))

    def convertRichMsg2Text(self, msg):
        return richTextUtils.parseFriendChatMsg(msg)

    def openRecentInteractWnd(self):
        self.uiAdapter.recentlyInteract.show()

    def clearRecent(self):
        self.recentData = {}

    @staticmethod
    def isOptimizeVersion():
        return gameglobal.rds.configData.get('enableIMOptimize', False)

    def genXinYiMsg(self, name):
        p = BigWorld.player()
        xinYi = p.xinYiManager
        xinYiFullName = uiUtils.getShortStr(xinYi['name'], 8)
        xinYiFullName = uiUtils.toHtml(xinYiFullName, '#ffcc33')
        return [p.getXinYiMsgPhoto(),
         const.FRIEND_STATE_DESC[p.getXinYiOnline()],
         gbk2unicode(xinYi['name']),
         gbk2unicode(xinYi['signature']),
         False,
         str(const.XINYI_MANAGER_ID),
         0,
         0,
         '',
         0,
         0,
         0,
         True,
         gametypes.FRIEND_GROUP_FRIEND,
         gbk2unicode(name),
         False,
         False,
         gbk2unicode(xinYiFullName),
         (gbk2unicode(pinyinConvert.strPinyinFirst(xinYi['name'])), gbk2unicode(pinyinConvert.strPinyin(xinYi['name']))),
         const.SEX_MALE,
         True,
         False,
         True,
         '',
         gbk2unicode(xinYi['name'])]

    def getGroupChatMsg(self, name, nuId, group):
        p = BigWorld.player()
        showName = name
        msgAcceptOp = 0
        members = p.groupChatData.get(nuId, {}).get('members', ())
        if p.gbId in members:
            msgAcceptOp = members[p.gbId][3]
        return ['',
         const.FRIEND_STATE_DESC[1],
         gbk2unicode(showName),
         '',
         False,
         str(nuId),
         0,
         0,
         '',
         len(p.groupUnreadMsgs.get(nuId, [])),
         0,
         0,
         False,
         group,
         gbk2unicode(name),
         False,
         False,
         gbk2unicode(showName),
         (gbk2unicode(pinyinConvert.strPinyinFirst(showName)), gbk2unicode(pinyinConvert.strPinyin(showName))),
         const.SEX_UNKNOWN,
         True,
         False,
         False,
         '',
         showName,
         gbk2unicode(''),
         msgAcceptOp]

    def genRecentInteractMsg(self, name, recentId):
        showName = ''
        lastMsg = ''
        showIcon = 'systemMessageIcon/recentInteract.dds'
        if recentId == const.FRIEND_RECENT_INTERACT_ID:
            showName = gameStrings.RECENT_INTERACT_MESSSAGE_NAME
            lastMsg = gameStrings.RECENT_INTERACT_LAST_MSG
            showIcon = 'systemMessageIcon/recentInteract.dds'
        elif recentId == const.FRIEND_RECENT_FIGHT_FOR_LOVE_ID:
            showName = gameStrings.RECENT_FIGHT_FOR_LOVE_MESSSAGE_NAME
            lastMsg = gameStrings.RECENT_FIGHT_FOR_LOVE_LAST_MSG
            iconName = FFLCD.data.get('friendListIconName', '')
            showIcon = 'systemMessageIcon/%s.dds' % (iconName,)
        elif recentId == const.FRIEND_NPC_ID:
            npcPid, questId = BigWorld.player().npcFavor.todayFavor
            showName = NND.data.get(npcPid, {}).get('name', '')
            showIcon = uiUtils.getPNpcIcon(npcPid)
            lastMsg = GMD.data.get(GMDD.data.NPC_FRIEND_FAVOR_PUSH, {}).get('text', 'GMDD.data.NPC_FRIEND_FAVOR_PUSH')
        return [showIcon,
         const.FRIEND_STATE_DESC[1],
         showName,
         '',
         False,
         str(recentId),
         0,
         0,
         '',
         0,
         0,
         0,
         False,
         gametypes.FRIEND_GROUP_RECENT,
         gbk2unicode(name),
         False,
         False,
         gbk2unicode(showName),
         (gbk2unicode(pinyinConvert.strPinyinFirst(showName)), gbk2unicode(pinyinConvert.strPinyin(showName))),
         const.SEX_UNKNOWN,
         True,
         False,
         False,
         '',
         showName,
         gbk2unicode(lastMsg)]

    def _tabToGroupsOld(self, tabName):
        groups = None
        if tabName == 'player':
            groups = BigWorld.player().getFriendGroupOrder()
        elif tabName == 'temp':
            groups = [gametypes.FRIEND_GROUP_RECENT, gametypes.FRIEND_GROUP_TEMP]
        elif tabName == 'enemy':
            groups = [gametypes.FRIEND_GROUP_ENEMY]
        elif tabName == 'black':
            groups = [gametypes.FRIEND_GROUP_BLOCK]
        elif tabName == 'guild':
            groups = [gametypes.FRIEND_GROUP_CHAT]
        return groups

    @staticmethod
    def __friendCompareByTimeOld(f1, f2):
        if f1[5] == str(const.XINYI_MANAGER_ID):
            return -1
        if f2[5] == str(const.XINYI_MANAGER_ID):
            return 1
        if f1[5] == str(const.FRIEND_SYSTEM_NOTIFY_ID):
            return -1
        if f2[5] == str(const.FRIEND_SYSTEM_NOTIFY_ID):
            return 1
        return cmp(f2[10], f1[10])

    def _getFriendListDataOld(self, groups = None, filterType = None, online = False, selectFriend = False):
        p = BigWorld.player()
        friend = p.friend
        data = []
        gmap = {}
        gdataKey = 'children'
        if groups == None or gametypes.FRIEND_GROUP_FRIEND in groups:
            if not selectFriend:
                groups = p.getFriendGroupOrder()
        if not groups:
            return data
        else:
            for id in groups:
                name = ''
                if id in friend.groups.keys():
                    name = friend.groups[id]
                elif id == gametypes.FRIEND_GROUP_GLOBAL_FRIEND:
                    name = gameStrings.TEXT_FRIENDPROXY_496
                if name:
                    gdata = {'name': gbk2unicode(uiUtils.htmlToText(name)),
                     'num': '0/10',
                     'children': [],
                     'id': id,
                     'total': 0,
                     'visibleNum': 0,
                     'expand': self.expandHistory.get(name, True)}
                    gmap[id] = len(data)
                    data.append(gdata)

            if gmap.has_key(gametypes.FRIEND_GROUP_FRIEND):
                if p.xinYiManager and not selectFriend:
                    xinYi = p.xinYiManager
                    xinYiFullName = uiUtils.getShortStr(xinYi['name'], 8)
                    xinYiFullName = uiUtils.toHtml(xinYiFullName, '#ffcc33')
                    xinYiData = [p.getXinYiMsgPhoto(),
                     const.FRIEND_STATE_DESC[p.getXinYiOnline()],
                     gbk2unicode(xinYi['name']),
                     gbk2unicode(xinYi['signature']),
                     False,
                     str(const.XINYI_MANAGER_ID),
                     0,
                     0,
                     gbk2unicode(''),
                     0,
                     0,
                     0,
                     True,
                     gametypes.FRIEND_GROUP_FRIEND,
                     gbk2unicode(name),
                     False,
                     False,
                     gbk2unicode(xinYiFullName),
                     (gbk2unicode(pinyinConvert.strPinyinFirst(xinYi['name'])), gbk2unicode(pinyinConvert.strPinyin(xinYi['name']))),
                     const.SEX_MALE,
                     True,
                     False,
                     True,
                     gbk2unicode(''),
                     gbk2unicode(xinYi['name'])]
                    groupIndex = gmap[gametypes.FRIEND_GROUP_FRIEND]
                    data[groupIndex][gdataKey].append(xinYiData)
                    data[groupIndex]['total'] += 1
                    data[groupIndex]['visibleNum'] += 1
                if gameglobal.rds.configData.get('enableSystemMessage', False) and not selectFriend:
                    sysNum = friend.tempMsgCount.get(const.FRIEND_SYSTEM_NOTIFY_ID, 0)
                    systemMsg = ['systemMessageIcon/systemMsg.dds',
                     const.FRIEND_STATE_DESC[1],
                     gameStrings.SYSTEM_MESSAGE_FRIEND_NAME,
                     gbk2unicode(''),
                     False,
                     str(const.FRIEND_SYSTEM_NOTIFY_ID),
                     0,
                     0,
                     gbk2unicode(''),
                     sysNum,
                     0,
                     0,
                     False,
                     gametypes.FRIEND_GROUP_FRIEND,
                     gbk2unicode(name),
                     False,
                     False,
                     gbk2unicode(''),
                     (gbk2unicode(pinyinConvert.strPinyinFirst(gameStrings.SYSTEM_MESSAGE_FRIEND_NAME)), gbk2unicode(pinyinConvert.strPinyin(gameStrings.SYSTEM_MESSAGE_FRIEND_NAME))),
                     const.SEX_UNKNOWN,
                     True,
                     False,
                     False,
                     gbk2unicode(''),
                     gameStrings.SYSTEM_MESSAGE_FRIEND_NAME]
                    groupIndex = gmap[gametypes.FRIEND_GROUP_FRIEND]
                    data[groupIndex][gdataKey].append(systemMsg)
                    data[groupIndex]['total'] += 1
                    data[groupIndex]['visibleNum'] += 1
            friendValues = friend.values()
            if self.enableGlobalFriend() and gmap.has_key(gametypes.FRIEND_GROUP_GLOBAL_FRIEND):
                globalFriends = getattr(p, 'globalFriends', None)
                if globalFriends:
                    for gVal in globalFriends.friends.values():
                        friendValues.append(uiUtils.globalFriend2FriendVal(gVal))

            for fVal in friendValues:
                if not self.isOptimizeVersion() and fVal.gbId == const.FRIEND_SYSTEM_NOTIFY_ID:
                    continue
                if filterType > 0:
                    if filterType == gameglobal.FRIENDS_ACKNOWLEDGE and not fVal.acknowledge:
                        continue
                    if filterType == gameglobal.FRIENDS_NOT_ACKNOWLEDGE and fVal.acknowledge:
                        continue
                if online and const.FRIEND_STATE_DESC[fVal.state] != 'online':
                    continue
                photoBorderIcon40 = p._getFriendPhotoBorderIcon(fVal, uiConst.PHOTO_BORDER_ICON_SIZE40)
                photoBorderIcon108 = p._getFriendPhotoBorderIcon(fVal, uiConst.PHOTO_BORDER_ICON_SIZE108)
                photo = p._getFriendPhoto(fVal)
                if uiUtils.isDownloadImage(photo):
                    if p.isGlobalFriendVal(fVal):
                        p.downloadCrossNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, int(p.globalFriends.friends.get(fVal.gbId).server), gametypes.NOS_FILE_PICTURE, None, (None,))
                    else:
                        p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, None, (None,))
                    photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
                msgCnt = friend.tempMsgCount.get(fVal.gbId, 0)
                rvalue = fVal.pally
                if self.selectedTab == 'enemy':
                    rvalue = fVal.hatred
                isBindYixin = fVal.yixinOpenId
                isFlowBack = fVal.flowbackType
                place = self._getLastPlace(fVal.spaceNo, fVal.areaId)
                if p.isGlobalFriendVal(fVal):
                    place = utils.getServerName(int(p.globalFriends.friends.get(fVal.gbId).server))
                fdata = [photo,
                 const.FRIEND_STATE_DESC[fVal.state],
                 gbk2unicode(fVal.getFullName()),
                 gbk2unicode(fVal.signature),
                 rvalue > 0,
                 str(fVal.gbId),
                 fVal.school,
                 fVal.level,
                 gbk2unicode(place),
                 msgCnt,
                 fVal.time,
                 rvalue,
                 isBindYixin,
                 fVal.group,
                 gbk2unicode(name),
                 fVal.deleted,
                 isFlowBack,
                 gbk2unicode(uiUtils.getShortStr(fVal.getFullName(), 8)),
                 (pinyinConvert.strPinyinFirst(fVal.getFullName()), pinyinConvert.strPinyin(fVal.getFullName())),
                 fVal.sex,
                 fVal.acknowledge,
                 p.isGlobalFriendVal(fVal),
                 fVal.showsig,
                 gbk2unicode(fVal.remarkName),
                 gbk2unicode(fVal.name),
                 photoBorderIcon40,
                 photoBorderIcon108]
                if fVal.group in groups and fVal.group > 0 and fVal.group != gametypes.FRIEND_GROUP_TEMP:
                    groupIndex = gmap[fVal.group]
                    data[groupIndex][gdataKey].append(fdata)
                    data[groupIndex]['total'] += 1
                    if friend.isVisible(fVal.state):
                        data[groupIndex]['visibleNum'] += 1
                if fVal.group == gametypes.FRIEND_GROUP_BLOCK_ENEMY:
                    if gametypes.FRIEND_GROUP_ENEMY in groups:
                        groupIndex = gmap[gametypes.FRIEND_GROUP_ENEMY]
                        tmpData = copy.deepcopy(fdata)
                        tmpData[13] = gametypes.FRIEND_GROUP_ENEMY
                        data[groupIndex][gdataKey].append(tmpData)
                        data[groupIndex]['total'] += 1
                        if friend.isVisible(fVal.state):
                            data[groupIndex]['visibleNum'] += 1
                    if gametypes.FRIEND_GROUP_BLOCK in groups:
                        groupIndex = gmap[gametypes.FRIEND_GROUP_BLOCK]
                        tmpData = copy.deepcopy(fdata)
                        tmpData[13] = gametypes.FRIEND_GROUP_BLOCK
                        data[groupIndex][gdataKey].append(tmpData)
                        data[groupIndex]['total'] += 1
                        if friend.isVisible(fVal.state):
                            data[groupIndex]['visibleNum'] += 1
                if gametypes.FRIEND_GROUP_TEMP in groups and fVal.group == gametypes.FRIEND_GROUP_TEMP:
                    groupIndex = gmap[gametypes.FRIEND_GROUP_TEMP]
                    tmpData = copy.deepcopy(fdata)
                    tmpData[13] = gametypes.FRIEND_GROUP_TEMP
                    if fVal.gbId in p.friend.tempFriendList:
                        tmpData[10] = len(p.friend.tempFriendList) - p.friend.tempFriendList.index(fVal.gbId)
                    data[groupIndex][gdataKey].append(tmpData)
                    data[groupIndex]['total'] += 1
                    if friend.isVisible(fVal.state):
                        data[groupIndex]['visibleNum'] += 1
                if gametypes.FRIEND_GROUP_RECENT in groups and fVal.gbId in p.friend.recentFriendList:
                    groupIndex = gmap[gametypes.FRIEND_GROUP_RECENT]
                    tmpData = copy.deepcopy(fdata)
                    tmpData[13] = gametypes.FRIEND_GROUP_RECENT
                    tmpData[10] = len(p.friend.recentFriendList) - p.friend.recentFriendList.index(fVal.gbId)
                    data[groupIndex][gdataKey].append(tmpData)
                    data[groupIndex]['total'] += 1
                    if friend.isVisible(fVal.state):
                        data[groupIndex]['visibleNum'] += 1
                if gametypes.FRIEND_GROUP_APPRENTICE in groups and fVal.apprentice:
                    groupIndex = gmap[gametypes.FRIEND_GROUP_APPRENTICE]
                    tmpData = copy.deepcopy(fdata)
                    tmpData[13] = gametypes.FRIEND_GROUP_APPRENTICE
                    data[groupIndex][gdataKey].append(tmpData)
                    data[groupIndex]['total'] += 1
                    if friend.isVisible(fVal.state):
                        data[groupIndex]['visibleNum'] += 1

            for gdata in data:
                if gdata['id'] == gametypes.FRIEND_GROUP_TEMP or gdata['id'] == gametypes.FRIEND_GROUP_RECENT:
                    gdata[gdataKey] = sorted(gdata[gdataKey], FriendProxy.__friendCompareByTime)
                else:
                    gdata[gdataKey] = sorted(gdata[gdataKey], FriendProxy.__friendCompare)
                gdata['num'] = '%s/%s' % (gdata['visibleNum'], gdata['total'])

            return data

    def chatToPlayer(self, name):
        fid = self.findNameInFriend(name)
        if fid != -1:
            gameglobal.rds.ui.friend.beginChat(fid)
        else:
            p = BigWorld.player()
            if p:
                p.base.addContact(name, gametypes.FRIEND_GROUP_TEMP, 0)
                self.tempFriendAddList.append(name)
                self.resetAddTempCallBack()
                self.clearTempFriendCallBack = BigWorld.callback(5, self.clearTempCallBack)

    def onTempFriendAdded(self, name, fid):
        for i in xrange(len(self.tempFriendAddList)):
            if self.tempFriendAddList[i] == name:
                self.tempFriendAddList.pop(i)
                gameglobal.rds.ui.friend.beginChat(fid)
                return

        self.resetAddTempCallBack()

    def resetAddTempCallBack(self):
        if self.clearTempFriendCallBack:
            BigWorld.cancelCallback(self.clearTempFriendCallBack)
            self.clearTempFriendCallBack = None

    def clearTempCallBack(self):
        self.tempFriendAddList = []

    def findNameInFriend(self, name):
        for gbId in BigWorld.player().friend:
            if BigWorld.player().friend[gbId].name == name:
                return gbId

        return -1

    def onCreateChatOpen(self, *args):
        gameglobal.rds.ui.groupChatMembers.show(uiConst.GROUP_CHAT_MEMBERS_TYPE_CREATE)

    def onGroupChatOpen(self, *args):
        nuId = int(args[3][0].GetString())
        self.openGroupChat(nuId)

    def openGroupChat(self, nuId):
        p = BigWorld.player()
        groupInfo = p.groupChatData.get(nuId, {})
        gfxMsgs = p.getGroupUnreadMsgs(nuId)
        gameglobal.rds.ui.groupChat.addGroupChatItem(groupInfo, gfxMsgs)
        p._refreshFriendList()

    def onGroupRightMenu(self, *args):
        nuId = int(args[3][0].GetString())
        menuManager.getInstance().menuTarget.apply(extraInfo={'groupNUID': nuId})
        menuData = menuManager.getInstance().getMenuListById(uiConst.MENU_GROUP_CHAT)
        gameglobal.rds.ui.chat.chatLogWindowMC.Invoke('showRightMenu', uiUtils.dict2GfxDict(menuData, True))

    def onEnableGroupChat(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableChatGroup', False))

    def onGetGuildBtnRedPotVisible(self, *args):
        if not gameglobal.rds.configData.get('enableChatGroup', False):
            return GfxValue(False)
        p = BigWorld.player()
        for nuId in p.groupChatData.keys():
            acceptOp = p.groupChatData[nuId]['members'][p.gbId][3]
            if acceptOp:
                continue
            msgs = p.groupUnreadMsgs.get(nuId, [])
            if msgs:
                return GfxValue(True)

        return GfxValue(False)

    def onSeekNpc(self, *args):
        seedId = int(args[3][0].GetNumber())
        uiUtils.findPosWithAlert(seedId)

    def onShowGroupChat(self, *args):
        key = int(args[3][0].GetString())
        strSign = args[3][1].GetString()
        p = BigWorld.player()
        if strSign == 'groupChatRoom':
            gfxMsgs = p.getGroupUnreadMsgs(key)
            gameglobal.rds.ui.groupChatRoom.show(key, gfxMsgs)
            if key in self.minChatArr:
                self.removeMinChat(key)
        elif strSign == 'groupChat':
            if key in p.groupChatData:
                self.openGroupChat(key)
            else:
                self.beginChat(key)

    def showAllMinChat(self):
        if self.minChatArr:
            for key in reversed(self.minChatArr):
                strSign = self.chatArrIdMap.get(key, '')
                p = BigWorld.player()
                if strSign == 'groupChatRoom':
                    gfxMsgs = p.getGroupUnreadMsgs(key)
                    gameglobal.rds.ui.groupChatRoom.show(key, gfxMsgs)
                    if key in self.minChatArr:
                        self.removeMinChat(key)
                elif strSign == 'groupChat':
                    if key in p.groupChatData:
                        self.openGroupChat(key)
                    else:
                        self.beginChat(key)
                else:
                    self.beginChat(key)
