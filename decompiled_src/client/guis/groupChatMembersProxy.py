#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/groupChatMembersProxy.o
from gamestrings import gameStrings
import BigWorld
import ui
import gameglobal
import utils
import gametypes
from uiProxy import UIProxy
from guis import events
from guis import uiConst
from gamestrings import gameStrings
from guis import uiUtils
from guis.asObject import ASObject
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class GroupChatMembersProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GroupChatMembersProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GROUP_CHAT_MEMBERS, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GROUP_CHAT_MEMBERS:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GROUP_CHAT_MEMBERS)

    def reset(self):
        self.membersType = 1
        self.selectedGbIds = []
        self.selectedNames = []
        self.itemList = []
        self.groupNUID = None

    def show(self, membersType = uiConst.GROUP_CHAT_MEMBERS_TYPE_CREATE, groupNUID = 0):
        self.membersType = membersType
        self.groupNUID = groupNUID
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_GROUP_CHAT_MEMBERS)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.sureBtn.addEventListener(events.BUTTON_CLICK, self.handleSureBtnClick, False, 0, True)
        self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick, False, 0, True)
        self.widget.searchInput.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleMembersKeyEvent, False, 0, True)
        self.widget.membersList.itemRenderer = 'GroupChatMembers_palyerItem'
        self.widget.membersList.lableFunction = self.itemFunction
        self.widget.membersList.dataArray = []
        self.widget.membersNumText.text = ''
        self.widget.sureBtn.enabled = False

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        groupInfo = p.groupChatData.get(self.groupNUID, {})
        members = groupInfo.get('members', {})
        if self.membersType in [uiConst.GROUP_CHAT_MEMBERS_TYPE_CREATE, uiConst.GROUP_CHAT_MEMBERS_TYPE_INVITE]:
            self.itemList = self.getInviteMembers(members)
            self.widget.selectAllBtn.visible = True
            self.widget.clearBtn.visible = True
            self.widget.selectAllBtn.addEventListener(events.BUTTON_CLICK, self.handleSelectAllBtnClick, False, 0, True)
            self.widget.clearBtn.addEventListener(events.BUTTON_CLICK, self.handleClearBtnClick, False, 0, True)
            self.widget.titleMc.titleText.text = gameStrings.GROUP_CHAT_MEMBERS_INVITE_TITLE
        elif self.membersType == uiConst.GROUP_CHAT_MEMBERS_TYPE_REMOVE:
            self.itemList = self.getRemoveMembers(members)
            self.widget.selectAllBtn.visible = False
            self.widget.clearBtn.visible = False
            self.widget.titleMc.titleText.text = gameStrings.GROUP_CHAT_MEMBERS_REMOVE_TITLE
        elif self.membersType == uiConst.GROUP_CHAT_MEMBERS_TYPE_TRANSFER:
            self.itemList = self.getRemoveMembers(members)
            self.widget.selectAllBtn.visible = False
            self.widget.clearBtn.visible = False
            self.widget.titleMc.titleText.text = gameStrings.GROUP_CHAT_MEMBERS_TRANSFER_TITLE
        self.widget.membersList.dataArray = self.itemList
        self.widget.membersList.validateNow()

    def getInviteMembers(self, existMembers):
        p = BigWorld.player()
        friendValues = p.friend.values()
        itemList = []
        for fVal in friendValues:
            if not fVal.acknowledge:
                continue
            if fVal.level < SCD.data.get('createChatGroupLv', 20):
                continue
            gbId = int(fVal.gbId)
            if gbId in existMembers:
                continue
            itemInfo = {}
            itemInfo['gbId'] = gbId
            itemInfo['name'] = fVal.getFullName()
            itemInfo['photo'] = gameglobal.rds.ui.groupChat.getPlayerPhoto(fVal.photo, gbId, fVal.school, fVal.sex)
            itemInfo['photoBorderIcon'] = p._getFriendPhotoBorderIcon(fVal, uiConst.PHOTO_BORDER_ICON_SIZE40)
            itemInfo['isSelect'] = False
            itemInfo['level'] = fVal.level
            itemInfo['school'] = fVal.school
            itemList.append(itemInfo)

        return itemList

    def getRemoveMembers(self, members):
        p = BigWorld.player()
        itemList = []
        for gbId, member in members.items():
            if gbId == p.gbId:
                continue
            itemInfo = {}
            itemInfo['gbId'] = gbId
            itemInfo['name'] = member[0]
            itemInfo['photo'] = gameglobal.rds.ui.groupChat.getPlayerPhoto(member[2], gbId, member[6], member[7])
            itemInfo['photoBorderIcon'] = p.getPhotoBorderIcon(member[5], uiConst.PHOTO_BORDER_ICON_SIZE40)
            itemInfo['isSelect'] = False
            itemInfo['level'] = member[1]
            itemInfo['online'] = member[4]
            itemInfo['school'] = member[6]
            itemList.append(itemInfo)

        return itemList

    def handleSelectAllBtnClick(self, *args):
        if self.membersType not in [uiConst.GROUP_CHAT_MEMBERS_TYPE_CREATE, uiConst.GROUP_CHAT_MEMBERS_TYPE_INVITE]:
            return
        self.selectedGbIds = []
        for itemInfo in self.itemList:
            if itemInfo.get('gbId', 0):
                self.selectedGbIds.append(itemInfo.get('gbId', 0))
            if itemInfo.get('name'):
                self.selectedNames.append(itemInfo.get('name'))

        self.widget.membersList.dataArray = self.itemList
        self.widget.membersList.validateNow()

    def handleClearBtnClick(self, *args):
        if self.membersType not in [uiConst.GROUP_CHAT_MEMBERS_TYPE_CREATE, uiConst.GROUP_CHAT_MEMBERS_TYPE_INVITE]:
            return
        self.selectedGbIds = []
        self.selectedNames = []
        self.widget.membersList.dataArray = self.itemList
        self.widget.membersList.validateNow()

    def getGroupChatTitleName(self):
        p = BigWorld.player()
        playerNameList = []
        ownerName = p.playerName.decode(utils.defaultEncoding())[0].encode('gbk')
        playerNameList.append(ownerName)
        playerNum = len(self.selectedGbIds)
        for i in xrange(playerNum):
            if i > 1:
                break
            gbId = self.selectedGbIds[i]
            fVal = p.friend.get(gbId, None)
            if fVal:
                playerName = fVal.name.decode(utils.defaultEncoding())[0].encode('gbk')
                playerNameList.append(playerName)

        if playerNum > 2:
            titleName = gameStrings.TEXT_CHATPROXY_403.join(playerNameList) + '...'
        else:
            titleName = gameStrings.TEXT_CHATPROXY_403.join(playerNameList)
        return titleName

    def handleSureBtnClick(self, *args):
        p = BigWorld.player()
        if not self.selectedGbIds:
            p.showGameMsg(GMDD.data.GROUP_CHAT_MEMBERS_NONE_SELECTED, ())
            return
        if self.membersType == uiConst.GROUP_CHAT_MEMBERS_TYPE_CREATE:
            titleName = self.getGroupChatTitleName()
            p.base.createChatGroup(gametypes.FRIEND_GROUP_MEMBERS_CHAT, titleName, self.selectedGbIds, utils.getHostId())
        elif self.membersType == uiConst.GROUP_CHAT_MEMBERS_TYPE_INVITE:
            p.base.inviteChatGroup(self.groupNUID, self.selectedGbIds, utils.getHostId())
        elif self.membersType == uiConst.GROUP_CHAT_MEMBERS_TYPE_REMOVE:
            p.base.kickOutChatGroupMember(self.groupNUID, self.selectedGbIds, utils.getHostId())
        elif self.membersType == uiConst.GROUP_CHAT_MEMBERS_TYPE_TRANSFER:
            p.base.transferChatGroupManager(self.groupNUID, self.selectedGbIds[0], utils.getHostId())

    def kickOut(self):
        BigWorld.player().base.kickOutChatGroupMember(self.groupNUID, self.selectedGbIds, utils.getHostId())

    def handleCancelBtnClick(self, *args):
        self.hide()

    @ui.callInCD(0.1)
    def handleMembersKeyEvent(self, *args):
        e = ASObject(args[3][0])
        searchKey = self.widget.searchInput.text
        itemValList = gameglobal.rds.ui.groupChat.getItemValListByStr(self.itemList, searchKey)
        self.widget.membersList.dataArray = itemValList
        self.widget.membersList.validateNow()

    def handleCheckBox(self, *args):
        itemMc = ASObject(args[3][0]).currentTarget
        gbId = int(itemMc.membersData.get('gbId', 0))
        name = itemMc.membersData.get('name')
        if itemMc.selected:
            if gbId not in self.selectedGbIds:
                self.selectedGbIds.append(gbId)
            if name not in self.selectedNames:
                self.selectedNames.append(name)
        else:
            if gbId in self.selectedGbIds:
                self.selectedGbIds.remove(gbId)
            if name in self.selectedNames:
                self.selectedNames.remove(name)
        if self.membersType == uiConst.GROUP_CHAT_MEMBERS_TYPE_CREATE:
            self.widget.sureBtn.enabled = len(self.selectedGbIds) >= 2
        else:
            self.widget.sureBtn.enabled = len(self.selectedGbIds) >= 1
        memberNumTxt = ''
        if self.membersType in (uiConst.GROUP_CHAT_MEMBERS_TYPE_CREATE, uiConst.GROUP_CHAT_MEMBERS_TYPE_INVITE, uiConst.GROUP_CHAT_MEMBERS_TYPE_REMOVE):
            memberNumTxt = gameStrings.TEXT_GROUPCHATMEMBERSPROXY_241 % len(self.selectedGbIds)
            if self.membersType == uiConst.GROUP_CHAT_MEMBERS_TYPE_CREATE and len(self.selectedGbIds) < 2:
                memberNumTxt = memberNumTxt + gameStrings.TEXT_GROUPCHATMEMBERSPROXY_243
        elif self.membersType == uiConst.GROUP_CHAT_MEMBERS_TYPE_TRANSFER and itemMc.selected:
            memberNumTxt = gameStrings.TEXT_GROUPCHATMEMBERSPROXY_246 % itemMc.membersData.get('name', '')
        self.widget.membersNumText.text = memberNumTxt

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.membersData = itemData
        itemMc.selected = int(itemData.gbId) in self.selectedGbIds
        itemMc.addEventListener(events.EVENT_SELECT, self.handleCheckBox, False, 0, True)
        if self.membersType == uiConst.GROUP_CHAT_MEMBERS_TYPE_TRANSFER:
            itemMc.groupName = 'membersBtn'
        else:
            itemMc.groupName = None
        itemMc.playerMc.playerName.text = itemData.name
        itemMc.playerMc.playerIcon.icon.fitSize = True
        itemMc.playerMc.playerIcon.icon.loadImage(itemData.photo)
        itemMc.playerMc.school.gotoAndPlay(uiConst.SCHOOL_FRAME_DESC.get(itemData.school, 'yuxu'))
        itemMc.playerMc.level.text = itemData.level
        itemMc.playerMc.playerIcon.borderImg.fitSize = True
        itemMc.playerMc.playerIcon.borderImg.loadImage(itemData.photoBorderIcon)
