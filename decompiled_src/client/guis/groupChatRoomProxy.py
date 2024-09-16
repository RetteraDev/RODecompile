#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/groupChatRoomProxy.o
from gamestrings import gameStrings
import BigWorld
import gametypes
import const
import utils
import ui
import re
import gameglobal
import gamelog
import clientcom
import math
from uiProxy import UIProxy
from guis import events
from guis import uiUtils
from guis import uiConst
from guis import menuManager
from guis import richTextUtils
from helpers import taboo
from gamestrings import gameStrings
from asObject import MenuManager
from guis import hotkeyProxy
from ui import unicode2gbk
from callbackHelper import Functor
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from cdata import game_msg_def_data as GMDD
NINT_MSG_ITEM_TEXT_WIDTH = 164

class GroupChatRoomProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GroupChatRoomProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GROUP_CHAT_ROOM, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GROUP_CHAT_ROOM:
            multiID = int(widget.multiID)
            for nuId, v in self.widgetMaps.iteritems():
                if v['multiID'] == multiID:
                    v['widget'] = widget
                    widget.groupNUID = nuId
                    self.initUI(widget)
                    self.refreshInfo(nuId)
                    break

    def getTopChatPanelWidget(self):
        if self.widgetMaps:
            topIndex = 0
            topWidget = None
            for nuId, v in self.widgetMaps.iteritems():
                widget = v['widget']
                if widget and widget.parent:
                    index = widget.parent.getChildIndex(widget)
                    if index > topIndex:
                        topIndex = index
                        topWidget = widget

        return (topIndex, topWidget)

    def getWidgetByMc(self, mc):
        while not getattr(mc, 'groupNUID', None) and getattr(mc, 'parent', None):
            mc = mc.parent

        return mc

    def _asWidgetClose(self, widgetId, multiID):
        self.closeWidgetByMultiId(multiID)

    def clearWidget(self):
        for nuId, v in self.widgetMaps.iteritems():
            self.uiAdapter.unLoadWidget(v['multiID'])

    def reset(self):
        self.widgetMaps = {}
        self.groupChatMsgs = {}
        self.lastMsg = {}
        self.groupMembers = {}
        self.historyMsgNum = 0
        self.enterDown = False
        self.sendId = 0

    def closeWidgetByMultiId(self, multiID):
        self.uiAdapter.unLoadWidget(multiID)
        groupNUID = 0
        for nuId, v in self.widgetMaps.iteritems():
            if v['multiID'] == multiID:
                groupNUID = nuId
                break

        if groupNUID:
            gameglobal.rds.ui.groupChat.removeGroupInChat(groupNUID)
            self.widgetMaps.pop(groupNUID)

    def show(self, groupNUID, initMsg = None):
        gamelog.info('@yj .. groupChatRoom.show .. groupNUID, initMsg=', groupNUID, initMsg)
        if initMsg:
            self.groupChatMsgs[groupNUID] = initMsg
        if groupNUID in self.widgetMaps:
            widget = self.widgetMaps[groupNUID]['widget']
            widget.refreshInfo(groupNUID)
            return
        else:
            multiID = self.uiAdapter.loadWidget(uiConst.WIDGET_GROUP_CHAT_ROOM)
            self.widgetMaps[groupNUID] = {'widget': None,
             'multiID': multiID}
            return

    def initUI(self, widget):
        p = BigWorld.player()
        widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleCloseBtnClick, False, 0, True)
        widget.searchMemberInput.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleMembersKeyEvent, False, 0, True)
        widget.gotoBtn.addEventListener(events.BUTTON_CLICK, self.handleGotoBtnClick, False, 0, True)
        widget.minBtn.addEventListener(events.BUTTON_CLICK, self.handleMinBtnClick, False, 0, True)
        widget.prosecuteBtn.addEventListener(events.BUTTON_CLICK, self.handleProsecuteBtnClick, False, 0, True)
        widget.inviteBtn.addEventListener(events.BUTTON_CLICK, self.handleInviteBtnClick, False, 0, True)
        widget.setupBtn.addEventListener(events.BUTTON_CLICK, self.handleSetupBtnClick, False, 0, True)
        widget.quitBtn.addEventListener(events.BUTTON_CLICK, self.handleQuitBtnClick, False, 0, True)
        widget.sendBtn.addEventListener(events.BUTTON_CLICK, self.handleSendBtnClick, False, 0, True)
        widget.msgHistoryBtn.addEventListener(events.BUTTON_CLICK, self.handleHistoryBtnClick, False, 0, True)
        widget.faceBtn.addEventListener(events.MOUSE_CLICK, self.handleFaceBtnClick, False, 0, True)
        widget.clearBtn.addEventListener(events.MOUSE_CLICK, self.handleClearMsgs, False, 0, True)
        widget.msgInput.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleKeyUp, False, 0, True)
        widget.msgInput.addEventListener(events.KEYBOARD_EVENT_KEY_DOWN, self.handleInputKeyDown, False, 0, True)
        widget.soundStartBtn.addEventListener(events.MOUSE_DOWN, self.handleStartSoundRecord, False, 0, True)
        _, _, desc = hotkeyProxy.getChatToFriendSoundRecordKey()
        widget.soundStartBtn.label = '%s%s' % (gameStrings.GROUP_CHAT_SOUND_BTN_LABEL, desc)
        widget.soundStartBtn.visible = p.enableSoundRecord()
        widget.addEventListener(events.MOUSE_CLICK, self.handleWidgetClick, False, 0, True)
        widget.colorBtn.visible = False
        widget.colorPanel.visible = False
        widget.prosecuteBtn.visible = False
        groupNUID = int(widget.groupNUID)
        groupType = p.groupChatData.get(groupNUID, {}).get('type', 0)
        if groupType in [gametypes.FRIEND_GROUP_SYSTEM_CHAT, gametypes.FRIEND_GROUP_SYSTEM_CHAT_PARTNER]:
            widget.quitBtn.visible = False
            widget.inviteBtn.visible = False
        else:
            widget.quitBtn.visible = True
            widget.inviteBtn.visible = True
        TipManager.addTip(widget.setupBtn, gameStrings.GROUP_CHAT_ROOM_SET_UP)
        TipManager.addTip(widget.quitBtn, gameStrings.GROUP_CHAT_ROOM_QUEIT)
        TipManager.addTip(widget.inviteBtn, gameStrings.GROUP_CHAT_ROOM_INVITE)
        TipManager.addTip(widget.prosecuteBtn, gameStrings.GROUP_CHAT_ROOM_PROSECUTE)
        widget.membersList.itemRenderer = 'GroupChatRoom_memberItem'
        widget.membersList.lableFunction = self.itemFunction
        widget.membersList.dataArray = []

    def refreshInfo(self, groupNUID = 0):
        widget = self.widgetMaps[groupNUID]['widget']
        if not widget:
            return
        self.updateGroupChatRoomMembers(groupNUID)
        self.updateInitChatMsgItem(groupNUID)

    def updateGroupChatRoomMembers(self, groupNUID):
        widget = self.widgetMaps[groupNUID]['widget']
        if not widget:
            return
        p = BigWorld.player()
        groupInfo = p.groupChatData.get(groupNUID, {})
        if not groupInfo:
            return
        members = groupInfo.get('members', [])
        normalList = []
        managerList = []
        for gbId, member in members.items():
            itemInfo = self.getMemberInfo(gbId, member, groupInfo)
            if itemInfo.get('isManager', False):
                managerList.append(itemInfo)
            else:
                normalList.append(itemInfo)

        self.groupMembers[groupNUID] = managerList + normalList
        widget.membersList.dataArray = self.groupMembers[groupNUID]
        widget.membersList.validateNow()
        onlineNum = self.getOnlineNum(members)
        widget.chatRoomName.tf.text = groupInfo.get('name', '')
        widget.membersText.text = gameStrings.TEXT_GROUPCHATPROXY_632 % (onlineNum, len(members.keys()))

    def getOnlineNum(self, members):
        onlineNum = 0
        for gbId, member in members.items():
            if member[4]:
                onlineNum = onlineNum + 1

        return onlineNum

    def getMemberInfo(self, gbId, member, groupInfo):
        p = BigWorld.player()
        groupType = groupInfo.get('type', 0)
        itemInfo = {}
        itemInfo['gbId'] = gbId
        itemInfo['name'] = member[0]
        itemInfo['level'] = member[1]
        itemInfo['online'] = member[4]
        itemInfo['school'] = member[6]
        itemInfo['photo'] = gameglobal.rds.ui.groupChat.getPlayerPhoto(member[2], gbId, member[6], member[7])
        itemInfo['photoBorderIcon'] = p.getPhotoBorderIcon(member[5], uiConst.PHOTO_BORDER_ICON_SIZE40)
        if groupType in [gametypes.FRIEND_GROUP_SYSTEM_CHAT, gametypes.FRIEND_GROUP_SYSTEM_CHAT_PARTNER]:
            itemInfo['isManager'] = False
        else:
            managerGbId = groupInfo.get('managerGbId', 0)
            itemInfo['isManager'] = True if gbId and gbId == managerGbId else False
        return itemInfo

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.identity.visible = itemData.isManager
        itemMc.playerMc.playerName.text = itemData.name
        itemMc.playerMc.head.icon.fitSize = True
        itemMc.playerMc.head.icon.loadImage(itemData.photo)
        itemMc.playerMc.head.school.gotoAndPlay(uiConst.SCHOOL_FRAME_DESC.get(itemData.school, 'yuxu'))
        itemMc.playerMc.head.lv.text = itemData.level
        itemMc.playerMc.head.borderImg.fitSize = True
        itemMc.playerMc.head.borderImg.loadImage(itemData.photoBorderIcon)
        if itemData.online:
            itemMc.playerMc.disabled = True
            ASUtils.setMcEffect(itemMc.playerMc.head.icon, '')
            ASUtils.setMcEffect(itemMc.playerMc.head.borderImg, '')
        else:
            itemMc.playerMc.disabled = False
            ASUtils.setMcEffect(itemMc.playerMc.head.icon, 'gray')
            ASUtils.setMcEffect(itemMc.playerMc.head.borderImg, 'gray')
        menuParam = {'roleName': itemData.name,
         'gbId': itemData.gbId}
        MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_CHAT, menuParam)
        itemMc.validateNow()

    def handleCloseBtnClick(self, *args):
        e = ASObject(args[3][0])
        widget = self.getWidgetByMc(e.currentTarget)
        groupNUID = int(widget.groupNUID)
        multiID = self.widgetMaps[groupNUID]['multiID']
        self.closeWidgetByMultiId(multiID)

    @ui.callInCD(0.1)
    def handleMembersKeyEvent(self, *args):
        e = ASObject(args[3][0])
        widget = self.getWidgetByMc(e.currentTarget)
        groupNUID = int(widget.groupNUID)
        searchKey = widget.searchMemberInput.text
        members = self.groupMembers.get(groupNUID, {})
        itemValList = self.getItemValListByStr(members, searchKey)
        widget.membersList.dataArray = itemValList
        widget.membersList.validateNow()

    def getItemValListByStr(self, itemList, searchKey):
        p = BigWorld.player()
        ret = []
        for info in itemList:
            if searchKey == '' or uiUtils.filterPinYin(searchKey, info.get('name', '')):
                ret.append(info)

        return ret

    def handleGotoBtnClick(self, *args):
        e = ASObject(args[3][0])
        widget = self.getWidgetByMc(e.currentTarget)
        groupNUID = int(widget.groupNUID)
        menuManager.getInstance().menuTarget.apply(gbId=0, extraInfo={'groupNUID': groupNUID})
        menuData = menuManager.getInstance().getMenuListById(uiConst.MENU_GROUP_CHAT_MERGE)
        gameglobal.rds.ui.chat.chatLogWindowMC.Invoke('showRightMenu', uiUtils.dict2GfxDict(menuData, True))

    def handleProsecuteBtnClick(self, *args):
        pass

    def handleInviteBtnClick(self, *args):
        e = ASObject(args[3][0])
        widget = self.getWidgetByMc(e.currentTarget)
        groupNUID = int(widget.groupNUID)
        gameglobal.rds.ui.groupChatMembers.show(uiConst.GROUP_CHAT_MEMBERS_TYPE_INVITE, groupNUID)

    def handleSetupBtnClick(self, *args):
        e = ASObject(args[3][0])
        widget = self.getWidgetByMc(e.currentTarget)
        groupNUID = int(widget.groupNUID)
        gameglobal.rds.ui.groupChatSetup.show(groupNUID)

    def handleQuitBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        widget = self.getWidgetByMc(target)
        if not widget:
            return
        nuId = int(widget.groupNUID)
        self.quitGroupChatRoom(nuId)

    def quitGroupChatRoom(self, nuId):
        p = BigWorld.player()
        groupInfo = p.groupChatData.get(nuId, {})
        managerGbId = groupInfo.get('managerGbId', 0)
        groupName = groupInfo.get('name', '')
        hostId = utils.getHostId()
        if p.gbId == managerGbId:
            msg = uiUtils.getTextFromGMD(GMDD.data.GROUP_CHAT_BREAK_UP_DESC, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.base.disbandChatGroup, nuId, hostId))
        else:
            msg = uiUtils.getTextFromGMD(GMDD.data.GROUP_CHAT_QUIT_CLOSE_DESC, '%s') % groupName
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.base.quitChatGroup, nuId, hostId, 0))

    def handleMinBtnClick(self, *args):
        e = ASObject(args[3][0])
        p = BigWorld.player()
        widget = self.getWidgetByMc(e.currentTarget)
        nuId = int(widget.groupNUID)
        multiID = self.widgetMaps[nuId]['multiID']
        self.closeWidgetByMultiId(multiID)
        groupName = p.groupChatData.get(nuId, {}).get('name', '')
        self.uiAdapter.friend.addMinChat([nuId, groupName, 'groupChatRoom'])

    def handleFaceBtnClick(self, *args):
        e = ASObject(args[3][0])
        widget = self.getWidgetByMc(e.currentTarget)
        if not widget.facePanel:
            widget.facePanel = widget.getInstByClsName('ChatFacePanel')
            widget.facePanel.addEventListener(events.FACE_CLICK, self.handleFaceClick, False, 0, True)
            widget.addChild(widget.facePanel)
            widget.facePanel.x = widget.faceBtn.x - 14
            widget.facePanel.y = widget.faceBtn.y - widget.facePanel.height + 4
        widget.facePanel.visible = True
        e.stopImmediatePropagation()

    def handleClearMsgs(self, *args):
        e = ASObject(args[3][0])
        widget = self.getWidgetByMc(e.currentTarget)
        widget.removeAllInst(widget.msgList.canvas)
        widget.msgList.refreshHeight()
        widget.msgList.scrollToEnd()
        nuId = int(widget.groupNUID)
        self.lastMsg[nuId] = None
        self.groupChatMsgs[nuId] = []

    def handleKeyUp(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        widget = self.getWidgetByMc(target)
        if not widget:
            return
        nuId = int(widget.groupNUID)
        if e.keyCode == events.KEYBOARD_CODE_ENTER or e.keyCode == events.KEYBOARD_CODE_NUMPAD_ENTER:
            if self.enterDown:
                msg = widget.msgInput.richText
                self.sendMsgToGroupRoom(nuId, msg)
                widget.msgInput.clearTxt()
            self.enterDown = False

    def handleInputKeyDown(self, *args):
        e = ASObject(args[3][0])
        if e.keyCode == events.KEYBOARD_CODE_ENTER or e.keyCode == events.KEYBOARD_CODE_NUMPAD_ENTER:
            self.enterDown = True

    def handleStartSoundRecord(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        widget = self.getWidgetByMc(target)
        if not widget:
            return
        p = BigWorld.player()
        p.recordUploadTranslateSound(self.submitSoundRecord)
        widget.stage.addEventListener(events.MOUSE_UP, self.handleEndSoundRecord, False, 0, True)

    def handleEndSoundRecord(self, *args):
        e = ASObject(args[3][0])
        target = e.target
        widget = self.getWidgetByMc(target)
        if not widget:
            return
        self.sendId = int(widget.groupNUID)
        p = BigWorld.player()
        p.endSoundRecord()
        p.addSoundRecordNum(False, True)
        widget.stage.removeEventListener(events.MOUSE_UP, self.handleEndSoundRecord)

    def submitSoundRecord(self, duration, key, content):
        content = unicode2gbk(content)
        content = utils.soundRecordRichText(key, duration) + content
        gamelog.info('@yj .. groupChatRoomProxy..submitSoundRecord..content=', content)
        if self.sendId:
            self.sendMsgToGroupRoom(self.sendId, content, autoInput=True)

    def handleFaceClick(self, *args):
        e = ASObject(args[3][0])
        widget = self.getWidgetByMc(e.currentTarget)
        faceStr = utils.faceIdToString(int(e.data))
        widget.msgInput.insertRichText(faceStr)
        widget.msgInput.focused = 1
        widget.facePanel.visible = False

    def appenInputMsg(self, widget, msg):
        if not widget:
            return
        widget.msgInput.appendRichText(msg)
        widget.msgInput.focused = 1

    def handleWidgetClick(self, *args):
        e = ASObject(args[3][0])
        widget = self.getWidgetByMc(e.currentTarget)
        if widget.facePanel:
            widget.facePanel.visible = False

    def handleHistoryBtnClick(self, *args):
        if gameglobal.rds.ui.groupChatHistoryMsg.widget:
            gameglobal.rds.ui.groupChatHistoryMsg.hide()
            return
        e = ASObject(args[3][0])
        widget = self.getWidgetByMc(e.currentTarget)
        nuId = int(widget.groupNUID)
        self.getHistoryByNuId(nuId, 1)

    def handleSendBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        widget = self.getWidgetByMc(target)
        if not widget:
            return
        msg = widget.msgInput.richText
        self.sendMsgToGroupRoom(int(widget.groupNUID), msg)
        widget.msgInput.clearTxt()

    def sendMsgToGroupRoom(self, nuId, msg, autoInput = False):
        msg = uiUtils.parseMsg(msg)
        reFormat = re.compile('<FONT COLOR=\"#FFFFE6\">(.*?)</FONT>', re.DOTALL)
        msg = reFormat.sub(self.delFont, msg)
        if richTextUtils.isSysRichTxt(msg) and not autoInput:
            BigWorld.player().showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
            return
        p = BigWorld.player()
        rawMsg = re.sub('</?FONT.*?>', '', msg, 0, re.DOTALL)
        if utils.isEmpty(rawMsg):
            p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_EMPTY, ())
            return
        isNormal, msg = taboo.checkDisbWord(msg)
        if not isNormal:
            p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_TABOO, ())
            return
        isNormal, msg = taboo.checkBSingle(msg)
        if not isNormal:
            p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_TABOO, ())
            return
        p.base.commitChatGroupMsg(nuId, msg, utils.getHostId())

    def delFont(self, matchobj):
        return matchobj.group(1)

    def isOpened(self, nuId):
        widget = self.widgetMaps.get(nuId, {}).get('widget', '')
        if widget:
            return True
        return False

    def getHistoryByNuId(self, groupNUID, pageNum):
        p = BigWorld.player()
        if pageNum and self.historyMsgNum:
            totalPage = math.ceil(self.historyMsgNum * 1.0 / uiConst.CHAT_TO_FRIEND_HISTORY_PAGE_NUM)
            offSet = (totalPage - pageNum) * uiConst.CHAT_TO_FRIEND_HISTORY_PAGE_NUM
            limit = min(uiConst.CHAT_TO_FRIEND_HISTORY_PAGE_NUM, self.historyMsgNum - offSet)
        else:
            offSet = 0
            limit = uiConst.CHAT_TO_FRIEND_HISTORY_PAGE_NUM
        return p.fetchGroupChatHistory(int(groupNUID), int(offSet), int(limit))

    def updateInitChatMsgItem(self, groupNUID):
        widget = self.widgetMaps[groupNUID]['widget']
        if not widget:
            return
        else:
            msgList = self.groupChatMsgs.get(groupNUID, [])
            lastMsgItem = None
            for msg in msgList:
                if msg.get('isInformationTips', False):
                    msgItem = widget.getInstByClsName('GroupChatRoom_msgChangeTips')
                    widget.msgList.canvas.addChild(msgItem)
                    msgItem.descText.htmlText = msg.get('descText', '')
                else:
                    isMe = msg.get('isMe', False)
                    msgItem = self.getMsgItem(widget, isMe)
                    widget.msgList.canvas.addChild(msgItem)
                    msgItem.msg.textFiled.width = NINT_MSG_ITEM_TEXT_WIDTH
                    msgItem.isMe = isMe
                    msgItem.msgData = msg
                    if isMe:
                        msgItem.x = widget.msgList.canvasMask.width
                if lastMsgItem != None:
                    msgItem.y = lastMsgItem.y + lastMsgItem.height + 4
                lastMsgItem = msgItem

            self.lastMsg[groupNUID] = lastMsgItem
            widget.msgList.refreshHeight()
            widget.msgList.scrollToEnd()
            return

    def setGMsgData(self, member, msg):
        gfxMsg = {}
        gfxMsg['isMe'] = msg['isMe']
        gfxMsg['time'] = msg['time']
        gfxMsg['msg'] = msg['msg']
        p = BigWorld.player()
        senderGbId = msg.get('senderGbId', 0)
        gfxMsg['photo'] = gameglobal.rds.ui.groupChat.getPlayerPhoto(member[2], senderGbId, member[6], member[7])
        gfxMsg['photoBorderIcon'] = p.getPhotoBorderIcon(member[5], uiConst.PHOTO_BORDER_ICON_SIZE40)
        mpId = 0
        if msg['isMe']:
            mpId = p.selectedMPId
        elif senderGbId:
            fVal = p.getFValByGbId(int(senderGbId))
            if fVal:
                mpId = fVal.mingpaiId
        name = uiUtils.getNameWithMingPain(member[0], mpId)
        gfxMsg['name'] = name
        return gfxMsg

    def addGroupMsgByPlayer(self, groupNUID, msg, isInformationTips = False):
        if not gameglobal.rds.configData.get('enableChatGroup', False):
            return
        gamelog.info('@yj .. groupChatRoomProxy..addGroupMsgByPlayer..groupNUID,msg=', groupNUID, msg)
        widget = self.widgetMaps[groupNUID]['widget']
        if not widget:
            return
        if not msg:
            return
        if isInformationTips:
            gfxMsg = {'descText': msg}
        else:
            p = BigWorld.player()
            senderGbId = msg.get('senderGbId', 0)
            member = p.groupChatData.get(groupNUID, {}).get('members', {}).get(senderGbId, ())
            if not member:
                return
            gfxMsg = self.setGMsgData(member, msg)
        gfxMsg['isInformationTips'] = isInformationTips
        if groupNUID in self.groupChatMsgs:
            self.groupChatMsgs[groupNUID].append(gfxMsg)
        else:
            self.groupChatMsgs[groupNUID] = []
            self.groupChatMsgs[groupNUID].append(gfxMsg)
        self.updateChatMsgItem(widget, groupNUID, gfxMsg)

    def getMsgItem(self, widget, isMe):
        if isMe:
            msgItem = widget.getInstByClsName('GroupChatRoom_MyMsgItem')
        else:
            msgItem = widget.getInstByClsName('GroupChatRoom_FriendMsgItem')
        return msgItem

    def updateChatMsgItem(self, widget, groupNUID, msg):
        if msg.get('isInformationTips', False):
            msgItem = widget.getInstByClsName('GroupChatRoom_msgChangeTips')
            widget.msgList.canvas.addChild(msgItem)
            msgItem.descText.htmlText = msg.get('descText', '')
        else:
            isMe = msg.get('isMe', False)
            msgItem = self.getMsgItem(widget, isMe)
            widget.msgList.canvas.addChild(msgItem)
            msgItem.msg.textFiled.width = NINT_MSG_ITEM_TEXT_WIDTH
            msgItem.isMe = isMe
            msgItem.msgData = msg
            if isMe:
                msgItem.x = widget.msgList.canvasMask.width
        if groupNUID in self.lastMsg and self.lastMsg[groupNUID]:
            lastMsgItem = self.lastMsg[groupNUID]
        else:
            self.lastMsg = {}
            lastMsgItem = None
        if lastMsgItem != None:
            msgItem.y = lastMsgItem.y + lastMsgItem.height + 4
        self.lastMsg[groupNUID] = msgItem
        widget.msgList.refreshHeight()
        widget.msgList.scrollToEnd()

    def appendHistoryMsg(self, groupNUID, msgs, total, offset, limit):
        gamelog.info('@yj .. groupChatRoomProxy.appendHistoryMsg.msgs=', msgs)
        self.historyMsgNum = total
        totalPage = math.ceil(self.historyMsgNum * 1.0 / uiConst.CHAT_TO_FRIEND_HISTORY_PAGE_NUM)
        currentPage = totalPage - math.ceil(offset / uiConst.CHAT_TO_FRIEND_HISTORY_PAGE_NUM)
        gamelog.info('@yj .. groupChatRoomProxy.appendHistoryMsg.totalPage, currentPage=', totalPage, currentPage)
        gameglobal.rds.ui.groupChatHistoryMsg.show(0, msgs, totalPage, currentPage, groupNUID)

    def clearHistroyNum(self):
        self.historyMsgNum = 0

    def sureGroupMergeChat(self, groupNUID):
        multiID = self.widgetMaps[groupNUID]['multiID']
        self.closeWidgetByMultiId(multiID)
        p = BigWorld.player()
        groupInfo = p.groupChatData.get(groupNUID, {})
        if not groupInfo:
            return
        msg = self.groupChatMsgs.get(groupNUID, [])
        gameglobal.rds.ui.groupChat.addGroupChatItem(groupInfo, msg)
