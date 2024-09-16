#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/groupChatProxy.o
from gamestrings import gameStrings
import BigWorld
import gametypes
import const
import utils
import clientcom
import gameglobal
import gamelog
import copy
import re
import math
from uiProxy import UIProxy
from ui import unicode2gbk
from guis import events
from guis import ui
from guis import uiConst
from guis import uiUtils
from guis import menuManager
from guis import richTextUtils
from gamestrings import gameStrings
from asObject import MenuManager
from guis import hotkeyProxy
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
NINT_MSG_ITEM_TEXT_WIDTH = 164
PROSECUTE_MSG_NUM = 5
MAX_MESSAGE_NUM = 99
SYSTEM_MESSAGE_DEFAULT_PATH = 'systemMessageIcon/systemMsgSmall.dds'

class GroupChatProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GroupChatProxy, self).__init__(uiAdapter)
        self.widget = None
        self.recordInGroupChats = {}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GROUP_CHAT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GROUP_CHAT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GROUP_CHAT)

    def reset(self):
        self.currSelectItem = None
        self.currSelectId = []
        self.enterDown = False
        self.lastMsg = {}
        self.itemList = []
        self.facePanel = None
        self.isClosingSingleWindow = False
        self.systemMsgCurPage = 1
        self.systemMsgTotalPage = 1
        self.systemMsgNum = 0
        self.recordChatMsgData = {}
        self.groupMembers = []

    def clearAll(self):
        self.recordInGroupChats = {}

    def show(self):
        if not gameglobal.rds.configData.get('enableChatGroup', False):
            return
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_GROUP_CHAT)
        self.removeGroupMinChat()

    def removeGroupMinChat(self):
        for key in self.recordInGroupChats.keys():
            self.removeMinChat(key)

    def removeMinChat(self, key):
        if key in gameglobal.rds.ui.friend.minChatArr:
            gameglobal.rds.ui.friend.removeMinChat(key)

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleCloseBtnClick, False, 0, True)
        self.widget.groupItemMc.groupList.itemRenderer = 'GroupChat_headItem'
        self.widget.groupItemMc.groupList.lableFunction = self.itemFunction
        self.widget.groupItemMc.groupList.dataArray = []
        self.widget.groupItemMc.searchGroupInput.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleKeyEvent, False, 0, True)
        self.widget.gotoBtn.addEventListener(events.BUTTON_CLICK, self.handleGotoBtnClick, False, 0, True)
        self.widget.minBtn.addEventListener(events.BUTTON_CLICK, self.handleMinBtnClick, False, 0, True)
        self.widget.addEventListener(events.MOUSE_CLICK, self.handleWidgetClick, False, 0, True)
        self.widget.addEventListener(events.EVENT_TEXTLINK, self.handleTextLink, False, 0, True)

    def handleTextLink(self, *args):
        if not self.currSelectId:
            return
        e = ASObject(args[3][0])
        linkText = e.text
        p = BigWorld.player()
        if linkText.startswith('sprite'):
            p.base.chatToSprite(int(linkText[len('sprite'):]), 'chat')

    def handleCloseBtnClick(self, *args):
        self.realClose()

    def realClose(self):
        self.hide()

    def handleGotoBtnClick(self, *args):
        e = ASObject(args[3][0])
        if not self.currSelectId:
            return
        gbId = self.getSelectItemId('gbId')
        nuId = self.getSelectItemId('nuId')
        menuManager.getInstance().menuTarget.apply(gbId=gbId, extraInfo={'groupNUID': nuId})
        menuData = menuManager.getInstance().getMenuListById(uiConst.MENU_GROUP_CHAT_SEPARATE)
        gameglobal.rds.ui.chat.chatLogWindowMC.Invoke('showRightMenu', uiUtils.dict2GfxDict(menuData, True))

    def sureSeparateChat(self, gbId, groupNUID):
        if not self.widget:
            return
        p = BigWorld.player()
        itemIndex = self.getRemoveItemIndex()
        gamelog.info('@yj .. groupChatProxy..sureSeparateChat..gbId, itemIndex=', gbId, groupNUID, itemIndex)
        if itemIndex == -1:
            return
        self.itemList.pop(itemIndex)
        self.currSelectId = []
        if gbId:
            if gbId != const.XINYI_MANAGER_ID:
                fVal = p.getFValByGbId(gbId)
                if fVal:
                    self.recordInGroupChats[gbId]['isSeparate'] = True
                    initMsg = self.recordChatMsgData.get(gbId, [])
                    gameglobal.rds.ui.chatToFriend.show(initMsg, p._createFriendData(fVal), False, False)
            else:
                self.recordInGroupChats[gbId]['isSeparate'] = True
                initMsg = self.recordChatMsgData.get(gbId, [])
                gameglobal.rds.ui.chatToFriend.show(initMsg, gameglobal.rds.ui.friend.createXinYiManagerData(), False)
        elif groupNUID:
            self.recordInGroupChats[groupNUID]['isSeparate'] = True
            initMsg = self.recordChatMsgData.get(groupNUID, [])
            gameglobal.rds.ui.groupChatRoom.show(groupNUID, initMsg)
        if self.itemList:
            self.widget.groupItemMc.groupList.dataArray = self.itemList
            self.widget.groupItemMc.groupList.validateNow()
        else:
            self.hide()

    def removeGroupInChat(self, key):
        if key in self.recordInGroupChats:
            self.recordInGroupChats.pop(key)

    def handleMinBtnClick(self, *args):
        gbId = self.getSelectItemId('gbId')
        nuId = self.getSelectItemId('nuId')
        if gbId:
            self.uiAdapter.friend.addMinChat([gbId, gameStrings.GROUP_CHAT_MINI_NAME, 'groupChat'])
        elif nuId:
            self.uiAdapter.friend.addMinChat([nuId, gameStrings.GROUP_CHAT_MINI_NAME, 'groupChat'])
        self.hide()

    def refreshInfo(self):
        if not self.widget:
            return
        self.updateGroupItemList()

    def sortItem(self, a, b):
        p = BigWorld.player()
        if a.has_key('members') and b.has_key('members'):
            if a['members'][p.gbId][3] > b['members'][p.gbId][3]:
                return 1
            if a['members'][p.gbId][3] == b['members'][p.gbId][3]:
                if a['time'] < b['time']:
                    return 1
            return -1
        if a.has_key('members') and not b.has_key('members'):
            if a['members'][p.gbId][3] == 1:
                return 1
            if a['time'] < b['time']:
                return 1
        elif b.has_key('members') and not a.has_key('members'):
            if b['members'][p.gbId][3] == 1:
                return -1
            if a['time'] < b['time']:
                return 1
        elif a['time'] < b['time']:
            return 1
        return -1

    def updateGroupItemList(self):
        if not self.widget:
            return
        p = BigWorld.player()
        groups = sorted(self.recordInGroupChats.values(), cmp=self.sortItem)
        self.itemList = []
        for i in xrange(len(groups)):
            v = groups[i]
            if v.get('isSeparate', False):
                continue
            itemInfo = {}
            itemInfo['isGroupChat'] = v.get('isGroupChat', False)
            if v.get('isGroupChat', False):
                nuId = int(v.get('nuId', 0))
                members = v.get('members', {})
                msgAcceptOp = 0
                if p.gbId in members:
                    msgAcceptOp = members.get(p.gbId, ())[3]
                itemInfo['gbId'] = 0
                itemInfo['nuId'] = nuId
                itemInfo['name'] = v.get('name', 0)
                itemInfo['publicAnnouncement'] = v.get('publicAnnouncement', '')
                itemInfo['managerGbId'] = v.get('managerGbId', 0)
                itemInfo['members'] = members
                itemInfo['state'] = 0
                itemInfo['msgNum'] = len(p.groupUnreadMsgs.get(nuId, []))
                itemInfo['msgAcceptOp'] = msgAcceptOp
            else:
                gbId = int(v.get('id', 0))
                itemInfo['nuId'] = 0
                itemInfo['gbId'] = gbId
                itemInfo['name'] = v.get('name', 0)
                itemInfo['photoBorderIcon'] = v.get('photoBorderIcon', '')
                itemInfo['state'] = const.FRIEND_STATE_DESC[v.get('state', 0)]
                itemInfo['msgNum'] = p.friend.tempMsgCount.get(int(v.get('id', 0)), 0)
                itemInfo['photo'] = self.getPlayerPhoto(v.get('photo', ''), gbId, v.get('school', 3), v.get('sex', 0))
                itemInfo['level'] = v.get('level', 0)
                itemInfo['school'] = v.get('school', 0)
            self.itemList.append(itemInfo)

        self.widget.groupItemMc.groupList.dataArray = self.itemList
        self.widget.groupItemMc.groupList.validateNow()

    def getPlayerPhoto(self, photo, gbId = None, school = 3, sex = 0):
        p = BigWorld.player()
        if not photo and gbId:
            gbId = int(gbId)
            if gbId == p.gbId:
                photo = p._getFriendPhoto(p, school, sex)
            else:
                fVal = p.getFValByGbId(gbId)
                photo = p._getFriendPhoto(fVal, school, sex)
        if uiUtils.isDownloadImage(photo):
            imagePath = const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
            if not clientcom.isFileExist(imagePath):
                BigWorld.player().downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, self.onDownloadPhoto, (None,))
            else:
                photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
        return photo

    def onDownloadPhoto(self, status, callbackArgs):
        pass

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        groupItemMc = ASObject(args[3][1])
        self._setGroupItemMCData(itemData, groupItemMc)

    def _setGroupItemMCData(self, itemData, groupItemMc):
        groupItemMc.data = itemData
        if itemData.isGroupChat:
            MenuManager.getInstance().unRegister(groupItemMc)
            groupItemMc.groupItem.visible = True
            groupItemMc.playerItem.visible = False
            itemMc = groupItemMc.groupItem
            itemMc.mouseChildren = True
            itemMc.groupMc.playerName.text = itemData.name
            itemMc.groupMc.msgNum.visible = itemData.msgNum
            itemMc.groupMc.status.visible = False
            if itemData.msgNum > MAX_MESSAGE_NUM:
                msgStr = '%d+' % MAX_MESSAGE_NUM
                if itemData.msgAcceptOp:
                    itemMc.groupMc.msgNum.gotoAndStop('type3')
                else:
                    itemMc.groupMc.msgNum.gotoAndStop('type1')
                itemMc.groupMc.msgNum.visible = True
                itemMc.groupMc.msgNum.stateText.text = msgStr
            elif itemData.msgNum > 0:
                msgStr = '%d' % itemData.msgNum
                if itemData.msgAcceptOp:
                    itemMc.groupMc.msgNum.gotoAndStop('type4')
                else:
                    itemMc.groupMc.msgNum.gotoAndStop('type2')
                itemMc.groupMc.msgNum.visible = True
                itemMc.groupMc.msgNum.stateText.text = msgStr
            else:
                itemMc.groupMc.msgNum.visible = False
        else:
            gbId = itemData.gbId
            if gbId != const.FRIEND_SYSTEM_NOTIFY_ID and gbId != const.XINYI_MANAGER_ID:
                menuType = self.getMenuTypeByGbId(gbId)
                MenuManager.getInstance().registerMenuById(groupItemMc, menuType, {'fid': str(gbId)})
            else:
                MenuManager.getInstance().unRegister(groupItemMc)
            groupItemMc.groupItem.visible = False
            groupItemMc.playerItem.visible = True
            itemMc = groupItemMc.playerItem
            itemMc.playerMc.playerName.text = itemData.name
            itemMc.playerMc.head.icon.fitSize = True
            itemMc.playerMc.head.icon.loadImage(itemData.photo)
            itemMc.playerMc.head.borderImg.fitSize = True
            itemMc.playerMc.head.borderImg.loadImage(itemData.photoBorderIcon)
            if itemData.school != const.SCHOOL_DEFAULT:
                itemMc.playerMc.school.visible = True
                itemMc.playerMc.school.gotoAndPlay(uiConst.SCHOOL_FRAME_DESC.get(itemData.school, 'yuxu'))
            else:
                itemMc.playerMc.school.visible = False
            itemMc.playerMc.level.text = itemData.level
            isXinYiManager = itemData.gbId == const.XINYI_MANAGER_ID
            isSystem = itemData.gbId == const.FRIEND_SYSTEM_NOTIFY_ID
            itemMc.playerMc.level.visible = not (isXinYiManager or isSystem)
            itemMc.playerMc.lvBg.visible = not (isXinYiManager or isSystem)
            if itemData.state == 'hide':
                itemMc.playerMc.disabled = True
                itemMc.playerMc.status.gotoAndPlay('online')
                ASUtils.setMcEffect(itemMc.playerMc.head.icon, 'gray')
                ASUtils.setMcEffect(itemMc.playerMc.head.borderImg, 'gray')
            else:
                itemMc.playerMc.disabled = False
                itemMc.playerMc.status.gotoAndPlay(itemData.state)
                ASUtils.setMcEffect(itemMc.playerMc.head.icon, '')
                ASUtils.setMcEffect(itemMc.playerMc.head.borderImg, '')
            itemMc.playerMc.msgNum.visible = itemData.msgNum
            if itemData.msgNum > 99:
                itemMc.playerMc.msgNum.gotoAndStop('type1')
            else:
                itemMc.playerMc.msgNum.gotoAndStop('type2')
            itemMc.playerMc.msgNum.stateText.text = itemData.msgNum
        itemMc.validateNow()
        itemMc.mouseChildren = True
        itemMc.closeChatBtn.addEventListener(events.BUTTON_CLICK, self.handleCloseChatBtn, False, 0, True)
        TipManager.addTip(itemMc.closeChatBtn, gameStrings.GROUP_CHAT_ITEM_CLOSE)
        itemMc.isGroupChat = itemData.isGroupChat
        itemMc.nuId = itemData.nuId
        itemMc.gbId = itemData.gbId
        itemMc.targetName = itemData.name
        itemMc.info = itemData
        itemMc.addEventListener(events.BUTTON_CLICK, self.updateGroupItemDown, False, 0, True)
        itemMc.selected = False
        if not self.currSelectId:
            itemMc.selected = True
            if itemMc.isGroupChat:
                self.currSelectId = ('nuId', itemMc.nuId)
                self.clearItemMsgsCount(itemMc.groupMc.msgNum, itemMc.nuId, itemMc.isGroupChat)
            else:
                self.currSelectId = ('gbId', itemMc.gbId)
                self.clearItemMsgsCount(itemMc.playerMc.msgNum, itemMc.gbId, itemMc.isGroupChat)
            self.currSelectItem = itemMc
            self.updateChatPanel()
            self.hideOtherPanel()
        elif self.currSelectId[0] == 'nuId' and self.currSelectId[1] == itemMc.nuId:
            itemMc.selected = True
            self.currSelectItem = itemMc
            self.updateChatPanel()
            self.hideOtherPanel()
        elif self.currSelectId[0] == 'gbId' and self.currSelectId[1] == itemMc.gbId:
            itemMc.selected = True
            self.currSelectItem = itemMc
            self.updateChatPanel()
            self.hideOtherPanel()

    def getMenuTypeByGbId(self, gbId):
        p = BigWorld.player()
        fVal = p.getFValByGbId(int(gbId))
        if fVal:
            groupId = fVal.group
        else:
            groupId = 0
        isGlobalFriend = p.isGobalFirendGbId(int(gbId))
        menuId = uiConst.MENU_FRIEND
        if groupId == gametypes.FRIEND_GROUP_TEMP or not groupId:
            menuId = uiConst.MENU_FRIEND_TEMP
        elif isGlobalFriend:
            menuId = uiConst.MENU_GLOBAL_FRIEND
        return menuId

    def handleCloseChatBtn(self, *args):
        if not self.widget:
            return
        else:
            e = ASObject(args[3][0])
            itemMc = e.currentTarget.parent
            if not itemMc:
                return
            isGroupChat = itemMc.isGroupChat
            itemIndex = itemMc.parent.index
            if itemIndex != -1 and itemIndex < len(self.itemList):
                self.itemList.pop(itemIndex)
            if itemIndex == len(self.itemList):
                newIndex = itemIndex - 1
            else:
                newIndex = itemIndex
            if isGroupChat:
                key = long(itemMc.nuId)
            else:
                key = long(itemMc.gbId)
            if key == const.FRIEND_SYSTEM_NOTIFY_ID:
                gameglobal.rds.ui.systemMessage.clearTempMsg()
            self.removeGroupInChat(key)
            self.lastMsg[key] = None
            if self.itemList and newIndex >= 0:
                self.widget.groupItemMc.groupList.dataArray = self.itemList
                self.widget.groupItemMc.groupList.validateNow()
                parentMc = self.widget.groupItemMc.groupList.items[newIndex]
                isGroupChat = parentMc.data['isGroupChat']
                itemMc = parentMc.groupItem if isGroupChat else parentMc.playerItem
                itemMc.selected = True
                if itemMc.isGroupChat:
                    self.currSelectId = ('nuId', itemMc.nuId)
                    self.clearItemMsgsCount(itemMc.groupMc.msgNum, itemMc.nuId, True)
                else:
                    self.currSelectId = ('gbId', itemMc.gbId)
                    self.clearItemMsgsCount(itemMc.playerMc.msgNum, itemMc.gbId, False)
                self.currSelectItem = itemMc
                self.updateChatPanel()
                self.hideOtherPanel()
            else:
                self.hide()
            self.isClosingSingleWindow = True
            e.stopImmediatePropagation()
            return

    def getRemoveItemIndex(self):
        nuId = self.getSelectItemId('nuId')
        gbId = self.getSelectItemId('gbId')
        for i in xrange(len(self.itemList)):
            info = self.itemList[i]
            if nuId and nuId == info.get('nuId', 0) or gbId and gbId == info.get('gbId', 0):
                return i

        return -1

    def updateGroupItemDown(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if not itemMc.enabled:
            return
        if self.isClosingSingleWindow:
            self.isClosingSingleWindow = False
            return
        if not self.currSelectItem:
            return
        if self.currSelectId:
            self.currSelectItem.selected = False
            if self.currSelectId[0] == 'gbId' and self.currSelectId[1] == const.FRIEND_SYSTEM_NOTIFY_ID:
                gameglobal.rds.ui.systemMessage.clearTempMsg()
        itemMc.selected = True
        if itemMc.isGroupChat:
            self.currSelectId = ('nuId', itemMc.nuId)
            self.clearItemMsgsCount(itemMc.groupMc.msgNum, itemMc.nuId, itemMc.isGroupChat)
        else:
            self.currSelectId = ('gbId', itemMc.gbId)
            self.clearItemMsgsCount(itemMc.playerMc.msgNum, itemMc.gbId, itemMc.isGroupChat)
        self.currSelectItem = itemMc
        self.updateChatPanel()
        self.hideOtherPanel()

    @ui.callInCD(0.1)
    def handleKeyEvent(self, *args):
        e = ASObject(args[3][0])
        searchKey = self.widget.groupItemMc.searchGroupInput.text
        itemValList = self.getItemValListByStr(self.itemList, searchKey)
        self.widget.groupItemMc.groupList.dataArray = itemValList
        self.widget.groupItemMc.groupList.validateNow()

    def getItemValListByStr(self, itemList, searchKey):
        p = BigWorld.player()
        ret = []
        for info in itemList:
            if searchKey == '' or uiUtils.filterPinYin(searchKey, info.get('name', '')):
                ret.append(info)

        return ret

    def updateChatPanel(self):
        if not self.currSelectItem:
            return
        data = self.currSelectItem.parent.data
        gbId = 0
        if data:
            gbId = int(data.get('gbId', 0))
        p = BigWorld.player()
        p.friend.tempMsgs = [ x for x in p.friend.tempMsgs if x[0] != gbId ]
        p._checkBlink()
        if self.currSelectItem.isGroupChat:
            self.widget.chatMc.gotoAndStop('group')
            self.updateGroupChatMc()
            self.widget.gotoBtn.visible = True
        elif self.currSelectId[0] == 'gbId' and self.currSelectId[1] == const.FRIEND_SYSTEM_NOTIFY_ID:
            self.widget.chatMc.gotoAndStop('system')
            self.updateSystemMsgMc()
            self.widget.gotoBtn.visible = False
        else:
            self.widget.chatMc.gotoAndStop('single')
            self.updatePlayerChatMc()
            self.widget.gotoBtn.visible = True

    def updateGroupChatMc(self):
        if not self.widget:
            return
        p = BigWorld.player()
        groupMc = self.widget.chatMc.groupMc
        groupMc.faceBtn.addEventListener(events.MOUSE_CLICK, self.handleFaceBtnClick, False, 0, True)
        groupMc.searchMemberInput.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleMembersKeyEvent, False, 0, True)
        groupMc.sendBtn.addEventListener(events.BUTTON_CLICK, self.handleGroupSendMsg, False, 0, True)
        groupMc.quitBtn.addEventListener(events.BUTTON_CLICK, self.handleQuitBtnClick, False, 0, True)
        groupMc.inviteBtn.addEventListener(events.BUTTON_CLICK, self.handleInviteBtnClick, False, 0, True)
        groupMc.setupBtn.addEventListener(events.BUTTON_CLICK, self.handleSetupBtnClick, False, 0, True)
        groupMc.msgHistoryBtn.addEventListener(events.BUTTON_CLICK, self.handleHistoryBtnClick, False, 0, True)
        groupMc.msgInput.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleKeyUp, False, 0, True)
        groupMc.msgInput.addEventListener(events.KEYBOARD_EVENT_KEY_DOWN, self.handleInputKeyDown, False, 0, True)
        self.widget.stage.focus = groupMc.msgInput.textField
        groupMc.clearBtn.addEventListener(events.BUTTON_CLICK, self.handleClearMsgs, False, 0, True)
        groupMc.soundStartBtn.addEventListener(events.MOUSE_DOWN, self.handleStartSoundRecord, False, 0, True)
        _, _, desc = hotkeyProxy.getChatToFriendSoundRecordKey()
        groupMc.soundStartBtn.label = '%s%s' % (gameStrings.GROUP_CHAT_SOUND_BTN_LABEL, desc)
        groupMc.soundStartBtn.visible = p.enableSoundRecord()
        groupMc.prosecuteBtn.visible = False
        groupMc.colorBtn.visible = False
        groupMc.colorPanel.visible = False
        TipManager.addTip(groupMc.setupBtn, gameStrings.GROUP_CHAT_ROOM_SET_UP)
        TipManager.addTip(groupMc.quitBtn, gameStrings.GROUP_CHAT_ROOM_QUEIT)
        TipManager.addTip(groupMc.inviteBtn, gameStrings.GROUP_CHAT_ROOM_INVITE)
        groupMc.membersList.itemRenderer = 'GroupChat_memberItem'
        groupMc.membersList.lableFunction = self.itemMembersFunction
        groupNUID = self.getSelectItemId('nuId')
        groupType = p.groupChatData.get(groupNUID, {}).get('type', 0)
        if groupType in [gametypes.FRIEND_GROUP_SYSTEM_CHAT, gametypes.FRIEND_GROUP_SYSTEM_CHAT_PARTNER]:
            groupMc.quitBtn.visible = False
            groupMc.inviteBtn.visible = False
        else:
            groupMc.quitBtn.visible = True
            groupMc.inviteBtn.visible = True
        msgList = self.recordChatMsgData.get(groupNUID, [])
        self.updateGroupChatInfo(groupNUID)
        self.updateAllChatMsgItem(groupMc, groupNUID, msgList)

    def updateGroupChatInfo(self, groupNUID):
        if not self.widget:
            return
        if self.getSelectItemId('nuId') != groupNUID:
            return
        p = BigWorld.player()
        groupMc = self.widget.chatMc.groupMc
        groupInfo = p.groupChatData.get(groupNUID, {})
        members = groupInfo.get('members', {})
        self.groupMembers = []
        normalList = []
        managerList = []
        for gbId, member in members.items():
            itemInfo = gameglobal.rds.ui.groupChatRoom.getMemberInfo(gbId, member, groupInfo)
            if itemInfo.get('isManager', False):
                managerList.append(itemInfo)
            else:
                normalList.append(itemInfo)

        self.groupMembers = managerList + normalList
        groupMc.membersList.dataArray = self.groupMembers
        groupMc.membersList.validateNow()
        onlineNum = gameglobal.rds.ui.groupChatRoom.getOnlineNum(members)
        groupName = groupInfo.get('name', 0)
        playerNum = len(members.keys())
        titleName = groupName + '[' + str(playerNum) + ']'
        groupMc.groupName.tf.text = titleName
        groupMc.membersText.text = gameStrings.TEXT_GROUPCHATPROXY_632 % (onlineNum, playerNum)

    def itemMembersFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.itemData = itemData
        itemMc.identity.visible = itemData.isManager
        TipManager.addTip(itemMc.identity, gameStrings.GROUP_CHAT_MANAGER_INDENTITY)
        itemMc.playerMc.playerName.text = itemData.name
        itemMc.playerMc.head.icon.fitSize = True
        itemMc.playerMc.head.icon.loadImage(itemData.photo)
        itemMc.playerMc.head.borderImg.fitSize = True
        itemMc.playerMc.head.borderImg.loadImage(itemData.photoBorderIcon)
        itemMc.playerMc.school.gotoAndPlay(uiConst.SCHOOL_FRAME_DESC.get(itemData.school, 'yuxu'))
        itemMc.playerMc.level.text = itemData.level
        if itemData.online:
            ASUtils.setMcEffect(itemMc.playerMc.head, '')
        else:
            ASUtils.setMcEffect(itemMc.playerMc.head, 'gray')
        menuParam = {'roleName': itemData.name,
         'gbId': itemData.gbId}
        MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_CHAT, menuParam)
        itemMc.doubleClickEnabled = True
        itemMc.addEventListener(events.MOUSE_DOUBLE_CLICK, self.handleMemberClick, False, 0, True)
        itemMc.validateNow()

    def handleMemberClick(self, *args):
        e = ASObject(args[3][0])
        itemData = e.target.itemData
        gbId = int(itemData.gbId)
        p = BigWorld.player()
        fval = p.getFValByGbId(gbId)
        if fval:
            gameglobal.rds.ui.friend.beginChat(gbId)
        else:
            try:
                group = p.friend.defaultGroup if p.friend.defaultGroup else gametypes.FRIEND_GROUP_FRIEND
                p.base.addContactByGbId(gbId, group, 0)
            except:
                msg = gameStrings.TEXT_GROUPCHATPROXY_673 % itemData.name
                BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, [msg], 0, {})

    @ui.callInCD(0.1)
    def handleMembersKeyEvent(self, *args):
        e = ASObject(args[3][0])
        groupMc = self.widget.chatMc.groupMc
        searchKey = groupMc.searchMemberInput.text
        itemValList = self.getItemValListByStr(self.groupMembers, searchKey)
        groupMc.membersList.dataArray = itemValList
        groupMc.membersList.validateNow()

    def handleGroupSendMsg(self, *args):
        p = BigWorld.player()
        groupMc = self.widget.chatMc.groupMc
        msg = groupMc.msgInput.richText
        if msg:
            nuId = self.getSelectItemId('nuId')
            gameglobal.rds.ui.groupChatRoom.sendMsgToGroupRoom(nuId, msg)
            groupMc.msgInput.clearTxt()

    def handleQuitBtnClick(self, *args):
        nuId = self.getSelectItemId('nuId')
        gameglobal.rds.ui.groupChatRoom.quitGroupChatRoom(nuId)

    def handleSetupBtnClick(self, *args):
        nuId = self.getSelectItemId('nuId')
        gameglobal.rds.ui.groupChatSetup.show(nuId)

    def handleHistoryBtnClick(self, *args):
        e = ASObject(args[3][0])
        if gameglobal.rds.ui.groupChatHistoryMsg.widget:
            gameglobal.rds.ui.groupChatHistoryMsg.hide()
            return
        nuId = self.getSelectItemId('nuId')
        gameglobal.rds.ui.groupChatRoom.getHistoryByNuId(nuId, 1)

    def handleInviteBtnClick(self, *args):
        nuId = self.getSelectItemId('nuId')
        gameglobal.rds.ui.groupChatMembers.show(uiConst.GROUP_CHAT_MEMBERS_TYPE_INVITE, nuId)

    def updatePlayerChatMc(self):
        p = BigWorld.player()
        singleMc = self.widget.chatMc.singleMc
        singleMc.msgInput.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleKeyUp, False, 0, True)
        singleMc.msgInput.addEventListener(events.KEYBOARD_EVENT_KEY_DOWN, self.handleInputKeyDown, False, 0, True)
        self.widget.stage.focus = singleMc.msgInput.textField
        singleMc.msgInputScrollBar.scrollTarget = singleMc.msgInput.textField
        singleMc.sendBtn.addEventListener(events.BUTTON_CLICK, self.handleSendMsg, False, 0, True)
        singleMc.clearBtn.addEventListener(events.BUTTON_CLICK, self.handleClearMsgs, False, 0, True)
        singleMc.msgHistoryBtn.addEventListener(events.BUTTON_CLICK, self.handleMsgHistoryBtnClick, False, 0, True)
        singleMc.faceBtn.addEventListener(events.MOUSE_CLICK, self.handleFaceBtnClick, False, 0, True)
        singleMc.prosecuteBtn.addEventListener(events.BUTTON_CLICK, self.handleProsecuteBtnClick, False, 0, True)
        singleMc.soundStartBtn.addEventListener(events.MOUSE_DOWN, self.handleStartSoundRecord, False, 0, True)
        _, _, desc = hotkeyProxy.getChatToFriendSoundRecordKey()
        singleMc.soundStartBtn.label = '%s%s' % (gameStrings.GROUP_CHAT_SOUND_BTN_LABEL, desc)
        singleMc.soundStartBtn.visible = p.enableSoundRecord()
        singleMc.colorBtn.visible = False
        singleMc.colorPanel.visible = False
        TipManager.addTip(singleMc.prosecuteBtn, gameStrings.GROUP_CHAT_ROOM_PROSECUTE)
        singleMc.friendName.tf.text = self.currSelectItem.targetName
        gbId = int(self.currSelectItem.gbId)
        if gbId != const.FRIEND_SYSTEM_NOTIFY_ID and gbId != const.XINYI_MANAGER_ID:
            menuType = self.getMenuTypeByGbId(gbId)
            MenuManager.getInstance().registerMenuById(singleMc.friendName, menuType, {'fid': str(gbId)})
        else:
            MenuManager.getInstance().unRegister(singleMc.friendName)
        gbId = self.getSelectItemId('gbId')
        msgList = self.recordChatMsgData.get(gbId, [])
        self.updateAllChatMsgItem(singleMc, gbId, msgList)

    def handleStartSoundRecord(self, *args):
        p = BigWorld.player()
        p.recordUploadTranslateSound(self.submitSoundRecord)
        if self.widget:
            self.widget.stage.addEventListener(events.MOUSE_UP, self.handleEndSoundRecord, False, 0, True)

    def handleEndSoundRecord(self, *args):
        p = BigWorld.player()
        p.endSoundRecord()
        p.addSoundRecordNum(False, True)
        if self.widget:
            self.widget.stage.removeEventListener(events.MOUSE_UP, self.handleEndSoundRecord)

    def submitSoundRecord(self, duration, key, content):
        content = unicode2gbk(content)
        content = utils.soundRecordRichText(key, duration) + content
        gamelog.info('@yj .. groupChatProxy..submitSoundRecord..content=', content)
        gbId = self.getSelectItemId('gbId')
        if gbId:
            gameglobal.rds.ui.chatToFriend._sendAsMsgToFriend(gbId, content, autoInput=True)
        nuId = self.getSelectItemId('nuId')
        if nuId:
            gameglobal.rds.ui.groupChatRoom.sendMsgToGroupRoom(nuId, content, autoInput=True)

    def getChatMc(self):
        if self.currSelectId[0] == 'nuId':
            chatMc = self.widget.chatMc.groupMc
        else:
            chatMc = self.widget.chatMc.singleMc
        return chatMc

    def isCurrentGroupMcShow(self):
        if self.currSelectId[0] == 'nuId':
            return True
        return False

    def handleWidgetClick(self, *args):
        if self.facePanel:
            self.facePanel.visible = False

    def handleFaceBtnClick(self, *args):
        e = ASObject(args[3][0])
        chatMc = self.getChatMc()
        if not self.facePanel or not self.facePanel.parent:
            self.facePanel = self.widget.getInstByClsName('ChatFacePanel')
            self.facePanel.addEventListener(events.FACE_CLICK, self.handleFaceClick, False, 0, True)
            chatMc.addChild(self.facePanel)
            self.facePanel.x = chatMc.faceBtn.x - 14
            self.facePanel.y = chatMc.faceBtn.y - self.facePanel.height + 4
        self.facePanel.visible = True
        e.stopImmediatePropagation()

    def handleProsecuteBtnClick(self, *args):
        if not self.currSelectId:
            return
        fid = self.getSelectItemId('gbId')
        name = self.recordInGroupChats.get(fid, {}).get('name', '')
        msg = self.recordChatMsgData.get(fid, [])
        pMsg = ''
        if msg:
            msg = [ item['msg'] for item in msg ]
            if len(msg) > PROSECUTE_MSG_NUM:
                pMsg = ';'.join(msg[0:PROSECUTE_MSG_NUM])
            else:
                pMsg = ';'.join(msg)
        gameglobal.rds.ui.prosecute.show(name, uiConst.MENU_FRIEND, msg=pMsg)
        gameglobal.rds.ui.prosecute.channel = const.CHAT_FRIEND

    def handleFaceClick(self, *args):
        e = ASObject(args[3][0])
        chatMc = self.getChatMc()
        faceStr = utils.faceIdToString(int(e.data))
        chatMc.msgInput.insertRichText(faceStr)
        chatMc.msgInput.focused = 1
        self.facePanel.visible = False

    def appenInputMsg(self, msg):
        chatMc = self.getChatMc()
        if not chatMc:
            return
        chatMc.msgInput.appendRichText(msg)
        chatMc.msgInput.focused = 1

    def handleKeyUp(self, *args):
        e = ASObject(args[3][0])
        if e.keyCode == events.KEYBOARD_CODE_ENTER or e.keyCode == events.KEYBOARD_CODE_NUMPAD_ENTER:
            if self.enterDown:
                self.handleSendMsg()
            self.enterDown = False

    def handleSendMsg(self, *args):
        if self.isCurrentGroupMcShow():
            groupMc = self.widget.chatMc.groupMc
            msg = groupMc.msgInput.richText
            if msg:
                nuId = self.getSelectItemId('nuId')
                gameglobal.rds.ui.groupChatRoom.sendMsgToGroupRoom(nuId, msg)
                groupMc.msgInput.clearTxt()
        else:
            singleMc = self.widget.chatMc.singleMc
            msg = singleMc.msgInput.richText
            if msg:
                gbId = self.getSelectItemId('gbId')
                gameglobal.rds.ui.chatToFriend._sendAsMsgToFriend(gbId, msg)
                singleMc.msgInput.clearTxt()

    def handleClearMsgs(self, *args):
        if self.isCurrentGroupMcShow():
            groupMc = self.widget.chatMc.groupMc
            self.widget.removeAllInst(groupMc.msgList.canvas)
            groupMc.msgList.refreshHeight()
            groupMc.msgList.scrollToEnd()
            key = self.getSelectItemId('nuId')
        else:
            singleMc = self.widget.chatMc.singleMc
            self.widget.removeAllInst(singleMc.msgList.canvas)
            singleMc.msgList.refreshHeight()
            singleMc.msgList.scrollToEnd()
            key = self.getSelectItemId('gbId')
        self.recordChatMsgData[key] = []
        self.lastMsg[key] = None

    def handleMsgHistoryBtnClick(self, *args):
        if gameglobal.rds.ui.groupChatHistoryMsg.widget:
            gameglobal.rds.ui.groupChatHistoryMsg.hide()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GROUP_CHAT_HISTORY_MSG)
        if not self.isCurrentGroupMcShow():
            gbId = self.getSelectItemId('gbId')
            gameglobal.rds.ui.chatToFriend._getHistoryByFid(gbId, 0, 1)

    def handleInputKeyDown(self, *args):
        e = ASObject(args[3][0])
        if e.keyCode == events.KEYBOARD_CODE_ENTER or e.keyCode == events.KEYBOARD_CODE_NUMPAD_ENTER:
            self.enterDown = True

    def saveChatMsgData(self, fid, gfxMsg):
        gfxMsg['isRedPacket'] = False
        if gfxMsg.has_key('msg'):
            gfxMsg['isRedPacket'] = utils.isRedPacket(gfxMsg['msg'])
        fid = int(fid)
        if fid in self.recordChatMsgData:
            self.recordChatMsgData[fid].append(gfxMsg)
        else:
            self.recordChatMsgData[fid] = []
            self.recordChatMsgData[fid].append(gfxMsg)

    def setPMsgData(self, fid = None, msg = None):
        gfxMsg = {}
        gfxMsg['isMe'] = msg['isMe']
        gfxMsg['time'] = msg['time']
        gfxMsg['msg'] = msg['msg']
        if fid == '-1':
            gfxMsg['isKefu'] = True
        p = BigWorld.player()
        gfxMsg['photo'] = self.getPlayerPhoto(msg.get('photo', ''), fid)
        gfxMsg['photoBorderIcon'] = msg.get('photoBorderIcon', '')
        mpId = 0
        if msg['isMe']:
            mpId = p.selectedMPId
        elif fid:
            fVal = p.getFValByGbId(int(fid))
            if fVal:
                mpId = fVal.mingpaiId
        name = uiUtils.getNameWithMingPain(msg.get('name', ''), mpId)
        gfxMsg['name'] = name
        return gfxMsg

    def addMsgByPlayer(self, fid = None, msg = None, isSave = False):
        gamelog.info('@yj .. groupChatProxy..addMsgByPlayer..fid, msg, isSave=', fid, msg, isSave)
        if not self.widget:
            return
        if not msg:
            return
        gfxMsg = self.setPMsgData(fid, msg)
        gfxMsg['isInformationTips'] = False
        gfxMsg['isRedPacket'] = utils.isRedPacket(msg['msg'])
        if isSave:
            self.saveChatMsgData(fid, gfxMsg)
        singleMc = self.widget.chatMc.singleMc
        self.updateChatMsgItem(singleMc, int(fid), gfxMsg)

    def getMsgItem(self, msg):
        if msg.get('isMe', False):
            msgItem = self.widget.getInstByClsName('GroupChat_MyMsgItem')
        elif msg.get('isKefu', False):
            msgItem = self.widget.getInstByClsName('GroupChat_KefuMsgItem')
        else:
            msgItem = self.widget.getInstByClsName('GroupChat_FriendMsgItem')
        return msgItem

    def updateChatMsgItem(self, chatMsgMc, key, msg):
        if msg.get('isInformationTips', False):
            msgItem = self.widget.getInstByClsName('GroupChat_msgChangeTips')
            chatMsgMc.msgList.canvas.addChild(msgItem)
            msgItem.x = 5
            msgItem.descText.htmlText = msg.get('descText', '')
            msgItem.descText.height = msgItem.descText.textHeight + 10
        else:
            msgItem = self.getMsgItem(msg)
            chatMsgMc.msgList.canvas.addChild(msgItem)
            msgItem.msg.textFiled.width = NINT_MSG_ITEM_TEXT_WIDTH
            isMe = msg.get('isMe', False)
            msgItem.isMe = isMe
            msgItem.msgData = msg
            if isMe:
                msgItem.x = chatMsgMc.msgList.canvasMask.width
        if key in self.lastMsg and self.lastMsg[key]:
            lastMsgItem = self.lastMsg[key]
        else:
            lastMsgItem = None
        if lastMsgItem != None:
            msgItem.y = lastMsgItem.y + lastMsgItem.height + 4
        self.lastMsg[key] = msgItem
        chatMsgMc.msgList.refreshHeight()
        chatMsgMc.msgList.scrollToEnd()

    def updateAllChatMsgItem(self, chatMsgMc, key, msgList):
        self.widget.removeAllInst(chatMsgMc.msgList.canvas)
        p = BigWorld.player()
        lastMsgItem = None
        for msg in msgList:
            if msg.get('isInformationTips', False):
                msgItem = self.widget.getInstByClsName('GroupChat_msgChangeTips')
                chatMsgMc.msgList.canvas.addChild(msgItem)
                msgItem.descText.htmlText = msg.get('descText', '')
            else:
                msgItem = self.getMsgItem(msg)
                chatMsgMc.msgList.canvas.addChild(msgItem)
                msgItem.msg.textFiled.width = NINT_MSG_ITEM_TEXT_WIDTH
                isMe = msg.get('isMe', False)
                msgItem.isMe = isMe
                msgItem.msgData = msg
                if isMe:
                    msgItem.x = chatMsgMc.msgList.canvasMask.width
            if lastMsgItem != None:
                msgItem.y = lastMsgItem.y + lastMsgItem.height + 4
            lastMsgItem = msgItem

        self.lastMsg[key] = lastMsgItem
        chatMsgMc.msgList.refreshHeight()
        chatMsgMc.msgList.scrollToEnd()

    def getSelectItemId(self, szType):
        if not self.currSelectId:
            return 0
        if self.currSelectId[0] == szType:
            return long(self.currSelectId[1])

    def addPlayerChatItem(self, friendInfo, msgs = None, needSelect = True):
        """
        @param needSelect: \xe6\xb7\xbb\xe5\x8a\xa0\xe6\x95\xb0\xe6\x8d\xae\xe7\x9a\x84\xe6\x97\xb6\xe5\x80\x99\xe6\x98\xaf\xe4\xb8\x8d\xe6\x98\xaf\xe9\x9c\x80\xe8\xa6\x81\xe8\xae\xbe\xe4\xb8\xba\xe5\xbd\x93\xe5\x89\x8d\xe9\x80\x89\xe4\xb8\xad\xe7\x9a\x84\xe5\xaf\xb9\xe8\xaf\x9d
        """
        gamelog.info('@yj .. groupChatProxy..addPlayerChatItem..friendInfo, msgs=', friendInfo, msgs)
        if not friendInfo:
            return
        gbId = int(friendInfo.get('id', 0))
        if self.widget and gbId != self.currSelectId and needSelect:
            self.selectChatItemById(gbId)
        self.updateInGroupChatData(gbId, friendInfo, False)
        if msgs:
            for info in msgs:
                self.saveChatMsgData(gbId, info)

        self.show()

    def onUpdataFriendInfo(self, gbId):
        if not self.recordInGroupChats:
            return
        if not self.recordInGroupChats.get(gbId):
            return
        p = BigWorld.player()
        fVal = p.getFValByGbId(gbId)
        info = p._createFriendData(fVal)
        info['time'] = self.recordInGroupChats[gbId].get('time')
        self.recordInGroupChats[gbId] = info
        self.refreshInfo()

    def selectChatItemById(self, id):
        items = self.widget.groupItemMc.groupList.items
        itemMc = None
        for item in items:
            newData = copy.deepcopy(item.data)
            nuId = int(newData.get('nuId', 0))
            gbId = int(newData.get('gbId', 0))
            if nuId and nuId == id:
                itemMc = item.groupItem
                break
            elif gbId and gbId == id:
                itemMc = item.playerItem

        if not itemMc:
            return
        else:
            if self.currSelectId:
                self.currSelectItem.selected = False
            itemMc.selected = True
            if itemMc.isGroupChat:
                self.currSelectId = ('nuId', itemMc.nuId)
                self.clearItemMsgsCount(itemMc.groupMc.msgNum, itemMc.nuId, itemMc.isGroupChat)
            else:
                self.currSelectId = ('gbId', itemMc.gbId)
                self.clearItemMsgsCount(itemMc.playerMc.msgNum, itemMc.gbId, itemMc.isGroupChat)
            self.currSelectItem = itemMc
            self.updateChatPanel()
            self.hideOtherPanel()
            return

    def updateInGroupChatData(self, key, newInfo, isGroupChat = False):
        gamelog.debug('yedawang### updateInGroupChatData', key, newInfo, isGroupChat)
        isExist = False
        for id, info in self.recordInGroupChats.items():
            if id == key:
                info['time'] = utils.getNow()
                self.recordInGroupChats[key] = info
                isExist = True
                break

        if not newInfo:
            return
        if not isExist:
            self.currSelectId = []
            newInfo['isSeparate'] = False
            newInfo['isGroupChat'] = isGroupChat
            newInfo['time'] = utils.getNow()
            self.recordInGroupChats[key] = newInfo

    def addGroupChatItem(self, groupInfo = None, msgs = None, needSelect = True):
        """
        @param needSelect: \xe6\xb7\xbb\xe5\x8a\xa0\xe6\x95\xb0\xe6\x8d\xae\xe7\x9a\x84\xe6\x97\xb6\xe5\x80\x99\xe6\x98\xaf\xe4\xb8\x8d\xe6\x98\xaf\xe9\x9c\x80\xe8\xa6\x81\xe8\xae\xbe\xe4\xb8\xba\xe5\xbd\x93\xe5\x89\x8d\xe9\x80\x89\xe4\xb8\xad\xe7\x9a\x84\xe5\xaf\xb9\xe8\xaf\x9d
        """
        gamelog.info('yedawang### .. groupChatProxy..addGroupChatItem..groupInfo=', groupInfo, msgs)
        if not groupInfo:
            return
        nuId = groupInfo.get('nuId', 0)
        if self.widget and nuId != self.currSelectId and needSelect:
            self.selectChatItemById(nuId)
        self.updateInGroupChatData(nuId, groupInfo, True)
        if msgs:
            for info in msgs:
                self.saveChatMsgData(nuId, info)

        self.show()

    def addMsgByGroup(self, nuId = None, msg = None, isInformationTips = False):
        if not gameglobal.rds.configData.get('enableChatGroup', False):
            return
        gamelog.info('@yj .. groupChatProxy..addMsgByGroup..nuId, msg, isSave=', nuId, msg, isInformationTips)
        if not self.widget:
            return
        if not msg:
            return
        if isInformationTips:
            gfxMsg = {'descText': msg}
        else:
            p = BigWorld.player()
            senderGbId = msg.get('senderGbId', 0)
            member = p.groupChatData.get(nuId, {}).get('members', {}).get(senderGbId, ())
            gfxMsg = gameglobal.rds.ui.groupChatRoom.setGMsgData(member, msg)
        gfxMsg['isInformationTips'] = isInformationTips
        self.saveChatMsgData(nuId, gfxMsg)
        groupMc = self.widget.chatMc.groupMc
        self.updateChatMsgItem(groupMc, int(nuId), gfxMsg)

    def checkCurrentChated(self, gbId):
        if not self.widget:
            return False
        if not self.currSelectId:
            return False
        selGbId = self.getSelectItemId('gbId')
        if selGbId == gbId:
            return True
        return False

    def checkCurrentGroupChated(self, nuId):
        if not self.widget:
            return False
        if not self.currSelectId:
            return False
        selNuId = self.getSelectItemId('nuId')
        if selNuId == nuId:
            return True
        return False

    def checkChatedId(self, key):
        if not self.widget:
            return False
        for id, info in self.recordInGroupChats.items():
            if id == key:
                return True

        return False

    def updateItemMsgsCount(self, key, msg, isGroupChat = False):
        if not self.widget:
            return
        p = BigWorld.player()
        gfxMsg = {}
        if isGroupChat:
            senderGbId = msg.get('senderGbId', 0)
            member = p.groupChatData.get(key, {}).get('members', {}).get(senderGbId, ())
            gfxMsg = gameglobal.rds.ui.groupChatRoom.setGMsgData(member, msg)
        elif key != const.FRIEND_SYSTEM_NOTIFY_ID:
            gfxMsg = self.setPMsgData(key, msg)
        if gfxMsg:
            self.saveChatMsgData(key, gfxMsg)
        items = self.widget.groupItemMc.groupList.items
        for item in items:
            newData = copy.deepcopy(item.data)
            nuId = int(newData.get('nuId', 0))
            gbId = int(newData.get('gbId', 0))
            msgNum = newData.get('msgNum', 0)
            if nuId and nuId == key:
                msgNum = len(p.groupUnreadMsgs.get(nuId, []))
            elif gbId and gbId == key:
                msgNum = p.friend.tempMsgCount.get(gbId, 0)
            if newData['msgNum'] != msgNum:
                newData['msgNum'] = msgNum
                self.widget.groupItemMc.groupList.labelFunction(newData, item)
                self._setGroupItemMCData(newData, item)

    def updateGroupName(self, groupNUID, newName):
        if self.itemList:
            for itemInfo in self.itemList:
                if itemInfo['nuId'] == groupNUID:
                    itemInfo['name'] = newName

        if not self.widget:
            return
        items = self.widget.groupItemMc.groupList.items
        for item in items:
            newData = copy.deepcopy(item.data)
            nuId = int(newData.get('nuId', 0))
            if nuId and nuId == groupNUID:
                newData['name'] = newName
                self.widget.groupItemMc.groupList.labelFunction(newData, item)
                self._setGroupItemMCData(newData, item)

        for id, info in self.recordInGroupChats.items():
            if id == groupNUID:
                info['name'] = newName

    def getNewMsgs(self, fid):
        p = BigWorld.player()
        for gbId, type, msg, idx in p.friend.tempMsgs:
            if gbId == fid:
                return msg

    def clearItemMsgsCount(self, msgNumMc, key, isGroupChat = False):
        key = int(key)
        msgNumMc.visible = False
        p = BigWorld.player()
        if isGroupChat:
            sysNum = len(p.groupUnreadMsgs.get(key, []))
            if sysNum:
                p.clearGroupUnreadMsg(key)
                p._refreshFriendList()
        else:
            sysNum = p.friend.tempMsgCount.get(key, 0)
            if sysNum != 0:
                p.friend.tempMsgCount[key] = 0
                p._refreshFriendList()
        p._checkBlink()

    def isChatOpen(self, key):
        if not gameglobal.rds.configData.get('enableChatGroup', False):
            return False
        if not self.widget:
            return False
        p = BigWorld.player()
        if key in self.recordInGroupChats:
            return True
        return False

    def deleteGroupData(self, nuId):
        self.removeGroupInChat(nuId)
        if self.currSelectId and self.currSelectId[0] == 'nuId' and self.currSelectId[1] == str(nuId):
            self.currSelectId = None
        if not self.recordInGroupChats:
            self.hide()
        else:
            self.refreshInfo()

    def hideOtherPanel(self):
        gameglobal.rds.ui.groupChatHistoryMsg.hide()
        gameglobal.rds.ui.groupChatSetup.hide()
        gameglobal.rds.ui.groupChatMembers.hide()

    def onUpdateChatGroupMsgAcceptOp(self, nuid, acceptOp):
        for id, info in self.recordInGroupChats.items():
            if id == nuid:
                info['members'][BigWorld.player().gbId][3] = acceptOp

        self.updateGroupItemList()

    def addSystemMsgItem(self):
        id = const.FRIEND_SYSTEM_NOTIFY_ID
        if self.widget and id != self.currSelectId:
            self.selectChatItemById(id)
        systemInfo = {'id': str(id),
         'name': gameStrings.SYSTEM_MESSAGE_FRIEND_NAME,
         'state': 1}
        self.updateInGroupChatData(id, systemInfo, False)
        self.show()

    def updateSystemMsgMc(self):
        systemMc = self.widget.chatMc.systemMc
        systemMc.pageInput.textField.restrict = '0-9'
        systemMc.pageInput.addEventListener(events.EVENT_CHANGE, self.handleInputPage, False, 0, True)
        systemMc.lastBtn.addEventListener(events.BUTTON_CLICK, self.handleLastBtnClick, False, 0, True)
        systemMc.nextBtn.addEventListener(events.BUTTON_CLICK, self.handleNextBtnClick, False, 0, True)
        systemMc.headBtn.addEventListener(events.BUTTON_CLICK, self.handleHeadBtnClick, False, 0, True)
        systemMc.tailBtn.addEventListener(events.BUTTON_CLICK, self.handleTailBtnClick, False, 0, True)
        self.systemMsgCurPage = 1
        self.systemMsgTotalPage = 1
        self.systemMsgNum = 0
        self.getSystemNotifyInfo(self.systemMsgCurPage)

    def getSystemNotifyInfo(self, pageNum):
        if pageNum and self.systemMsgNum:
            totalPage = math.ceil(self.systemMsgNum * 1.0 / uiConst.SYSTEM_NOTIFY_HISTORY_PAGE_NUM)
            offSet = (totalPage - pageNum) * uiConst.SYSTEM_NOTIFY_HISTORY_PAGE_NUM
            limit = min(uiConst.SYSTEM_NOTIFY_HISTORY_PAGE_NUM, self.systemMsgNum - offSet)
        else:
            offSet = 0
            limit = uiConst.SYSTEM_NOTIFY_HISTORY_PAGE_NUM
        p = BigWorld.player()
        p.fetchSystemNotifyHistory(p.gbId, int(offSet), int(limit))

    def appendNewSystemNotifyMsg(self):
        if not self.widget:
            return
        offSet = (self.systemMsgTotalPage - self.systemMsgCurPage) * uiConst.SYSTEM_NOTIFY_HISTORY_PAGE_NUM
        limit = min(uiConst.SYSTEM_NOTIFY_HISTORY_PAGE_NUM, self.systemMsgNum - offSet + 1)
        p = BigWorld.player()
        p.fetchSystemNotifyHistory(p.gbId, int(offSet), int(limit))

    def appendSystemNotifyHistoryMsg(self, gbId, msgs, total, offset, limit):
        if not self.checkCurrentChated(const.FRIEND_SYSTEM_NOTIFY_ID):
            return
        self.systemMsgNum = total
        totalPage = math.ceil(total * 1.0 / uiConst.SYSTEM_NOTIFY_HISTORY_PAGE_NUM)
        currentPage = totalPage - math.ceil(offset / uiConst.SYSTEM_NOTIFY_HISTORY_PAGE_NUM)
        p = BigWorld.player()
        gfxMsg = []
        for msg in msgs:
            msgId = msg.get('msgId', 0)
            time = msg.get('time', 0)
            args = msg.get('args', [])
            args = gameglobal.rds.ui.systemMessage.changeCoding(args)
            text = p.getLinkText(args, GMD.data.get(msgId, {}))
            try:
                msgInfo = p.formatMsg(text, args)
            except:
                gamelog.debug('systemMssage error', text, args)
                continue

            sysTypeIcon = GMD.data.get(msgId, {}).get('sysTypeIcon', SYSTEM_MESSAGE_DEFAULT_PATH)
            gfxMsg.append({'msgId': msgId,
             'time': time,
             'msg': msgInfo,
             'sysTypeIcon': sysTypeIcon})

        systemMsgList = gfxMsg
        self.systemMsgTotalPage = max(int(totalPage), 1)
        self.systemMsgCurPage = max(int(currentPage), 1)
        self.updateSystemMsgList(systemMsgList, self.systemMsgTotalPage, self.systemMsgCurPage)

    def updateSystemMsgList(self, systemMsgList, totalPage, curPage):
        widget = self.widget.chatMc.systemMc
        self.widget.removeAllInst(widget.msgList.canvas)
        posY = 0
        tempMsgList = gameglobal.rds.ui.systemMessage.tempMsgList
        if tempMsgList:
            systemMsgList.extend(tempMsgList)
        for tInfo in systemMsgList:
            itemMc = self.widget.getInstByClsName('GroupChat_SystemMsgInfo')
            path = tInfo.get('sysTypeIcon', SYSTEM_MESSAGE_DEFAULT_PATH)
            itemMc.head.icon.clear()
            itemMc.head.icon.loadImage(path)
            itemMc.nameTxt.text = gameStrings.SYSTEM_MESSAGE_FRIEND_NAME
            itemMc.time.text = gameglobal.rds.ui.systemMessage.getSystemMsgTimeStr(tInfo.get('time', 0))
            itemMc.msg.text = tInfo.get('msg', '')
            itemMc.msg.height = itemMc.msg.textFiled.textHeight + 10
            itemMc.time.x = itemMc.msg.x + itemMc.msg.width - itemMc.time.textWidth - 12
            lineEnd = itemMc.msg.textFiled.numLines - 1
            endIndex = itemMc.msg.textFiled.getLineOffset(lineEnd) + itemMc.msg.textFiled.getLineLength(lineEnd) - 1
            endWordRect = itemMc.msg.textFiled.getCharBoundaries(endIndex)
            endlineWidth = endWordRect.x + endWordRect.width if endWordRect else 0
            if endlineWidth + itemMc.time.textWidth + 12 <= itemMc.msg.tf.width:
                itemMc.time.y = itemMc.msg.y + itemMc.msg.textFiled.textHeight - itemMc.time.textHeight
                itemMc.bg.height = itemMc.msg.y + itemMc.msg.height
            else:
                itemMc.time.y = itemMc.msg.y + itemMc.msg.textFiled.textHeight + 10
                itemMc.bg.height = itemMc.msg.y + itemMc.msg.height + itemMc.time.height
            itemMc.y = posY
            posY += itemMc.height
            widget.msgList.canvas.addChild(itemMc)
            widget.msgList.refreshHeight()
            widget.msgList.scrollToEnd()
            widget.pageText.text = '/%d' % totalPage
            widget.pageInput.text = curPage
            widget.headBtn.enabled = curPage != 1 and totalPage != 1
            widget.lastBtn.enabled = curPage > 1 and totalPage != 1
            widget.nextBtn.enabled = curPage < totalPage and totalPage != 1
            widget.tailBtn.enabled = curPage != totalPage and totalPage != 1

    def handleLastBtnClick(self, *args):
        if self.systemMsgCurPage > 1:
            self.systemMsgCurPage = self.systemMsgCurPage - 1
            self.getSystemNotifyInfo(self.systemMsgCurPage)

    def handleNextBtnClick(self, *args):
        if self.systemMsgCurPage < self.systemMsgTotalPage:
            self.systemMsgCurPage = self.systemMsgCurPage + 1
            self.getSystemNotifyInfo(self.systemMsgCurPage)

    def handleInputPage(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.text == '':
            e.currentTarget.text = '1'
        page = int(e.currentTarget.text)
        if page < 1:
            page = 1
        elif page > self.systemMsgTotalPage:
            page = self.systemMsgTotalPage
        e.currentTarget.text = str(page)
        self.systemMsgCurPage = page
        self.getSystemNotifyInfo(self.systemMsgCurPage)

    def handleHeadBtnClick(self, *args):
        if self.systemMsgCurPage != 1:
            self.systemMsgCurPage = 1
            self.getSystemNotifyInfo(self.systemMsgCurPage)

    def handleTailBtnClick(self, *args):
        if self.systemMsgCurPage != self.systemMsgTotalPage:
            self.systemMsgCurPage = self.systemMsgTotalPage
            self.getSystemNotifyInfo(self.systemMsgCurPage)
