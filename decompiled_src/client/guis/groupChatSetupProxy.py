#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/groupChatSetupProxy.o
import BigWorld
import gametypes
import const
import utils
import gameglobal
import ui
from uiProxy import UIProxy
from guis import events
from guis import uiUtils
from guis import uiConst
from helpers import taboo
from guis.asObject import ASObject
from guis.asObject import ASUtils
from cdata import game_msg_def_data as GMDD
MIN_GROUP_NAME = 2

class GroupChatSetupProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GroupChatSetupProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GROUP_CHAT_SETUP, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GROUP_CHAT_SETUP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GROUP_CHAT_SETUP)

    def reset(self):
        self.groupNUID = 0
        self.titleName = ''

    def show(self, groupNUID):
        self.groupNUID = groupNUID
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_GROUP_CHAT_SETUP)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.msgInputScrollBar.scrollTarget = self.widget.msgInput.textField
        self.widget.checkBox.disabled = False
        self.widget.groupNameEdit.addEventListener(events.EVENT_CHANGE, self.handleGroupNameEdit, False, 0, True)
        self.widget.groupNameEdit.textField.addEventListener(events.FOCUS_EVENT_FOCUS_IN, self.handleEditFocusIn, False, 0, True)
        self.widget.groupNameEdit.textField.addEventListener(events.FOCUS_EVENT_FOCUS_OUT, self.handleEditFocusOut, False, 0, True)
        self.widget.saveBtn.addEventListener(events.BUTTON_CLICK, self.handleSaveBtnClick, False, 0, True)
        self.widget.addBtn.addEventListener(events.BUTTON_CLICK, self.handleAddBtnClick, False, 0, True)
        self.widget.removeBtn.addEventListener(events.BUTTON_CLICK, self.handleRemoveBtnClick, False, 0, True)
        self.widget.transferBtn.addEventListener(events.BUTTON_CLICK, self.handleTransferBtnClick, False, 0, True)
        self.widget.quitBtn.addEventListener(events.BUTTON_CLICK, self.handleQuitBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        groupInfo = p.groupChatData.get(self.groupNUID, {})
        managerGbId = groupInfo.get('managerGbId', 0)
        members = groupInfo.get('members', {})
        self.titleName = groupInfo.get('name', '')
        self.widget.groupNameEdit.validateNow()
        self.widget.groupNameEdit.textField.text = self.titleName
        self.widget.msgInput.validateNow()
        self.widget.msgInput.textField.text = groupInfo.get('publicAnnouncement', '')
        self.widget.checkBox.selected = members.get(p.gbId, ())[3]
        self.widget.checkBox.addEventListener(events.EVENT_SELECT, self.handleCheckBox, False, 0, True)
        p = BigWorld.player()
        groupType = groupInfo.get('type', 0)
        if groupType in [gametypes.FRIEND_GROUP_SYSTEM_CHAT, gametypes.FRIEND_GROUP_SYSTEM_CHAT_PARTNER]:
            self.widget.saveBtn.visible = False
            self.widget.addBtn.enabled = False
            self.widget.removeBtn.enabled = False
            self.widget.transferBtn.enabled = False
            self.widget.quitBtn.enabled = False
        elif managerGbId == p.gbId:
            ASUtils.setHitTestDisable(self.widget.groupNameEdit, False)
            ASUtils.setHitTestDisable(self.widget.msgInput, False)
            self.widget.saveBtn.visible = True
            self.widget.addBtn.enabled = True
            self.widget.removeBtn.enabled = True
            self.widget.transferBtn.enabled = True
            self.widget.quitBtn.enabled = True
        else:
            ASUtils.setHitTestDisable(self.widget.groupNameEdit, True)
            ASUtils.setHitTestDisable(self.widget.msgInput, True)
            self.widget.saveBtn.visible = False
            self.widget.addBtn.enabled = False
            self.widget.removeBtn.enabled = False
            self.widget.transferBtn.enabled = False
            self.widget.quitBtn.enabled = True

    def handleGroupNameEdit(self, *args):
        e = ASObject(args[3][0])

    def handleEditFocusIn(self, *args):
        pass

    def handleEditFocusOut(self, *args):
        e = ASObject(args[3][0])
        if not self.widget:
            return
        tName = self.widget.groupNameEdit.textField.text
        if tName == self.titleName:
            return
        isValid = self.checkGroupName(tName)
        if not isValid:
            return
        p = BigWorld.player()
        p.base.updateChatGroupName(self.groupNUID, tName, utils.getHostId())

    def handleCheckBox(self, *args):
        opType = self.widget.checkBox.selected
        p = BigWorld.player()
        p.base.setChatGroupAcceptOp(self.groupNUID, opType, utils.getHostId())
        self.widget.checkBox.disabled = True

    def handleSaveBtnClick(self, *args):
        announcementDesc = self.widget.msgInput.textField.text
        p = BigWorld.player()
        p.base.updateChatGroupPublicAnnouncement(self.groupNUID, announcementDesc, utils.getHostId())

    def handleAddBtnClick(self, *args):
        gameglobal.rds.ui.groupChatMembers.show(uiConst.GROUP_CHAT_MEMBERS_TYPE_INVITE, self.groupNUID)

    def handleRemoveBtnClick(self, *args):
        gameglobal.rds.ui.groupChatMembers.show(uiConst.GROUP_CHAT_MEMBERS_TYPE_REMOVE, self.groupNUID)

    def handleTransferBtnClick(self, *args):
        gameglobal.rds.ui.groupChatMembers.show(uiConst.GROUP_CHAT_MEMBERS_TYPE_TRANSFER, self.groupNUID)

    def handleQuitBtnClick(self, *args):
        p = BigWorld.player()
        groupInfo = p.groupChatData.get(self.groupNUID, {})
        managerGbId = groupInfo.get('managerGbId', 0)
        if p.gbId == managerGbId:
            p.base.disbandChatGroup(self.groupNUID, utils.getHostId())
        else:
            p.base.quitChatGroup(self.groupNUID, utils.getHostId(), 0)
        self.hide()

    def setAnnouncementSuccess(self, nuId, publicAnnouncement):
        if not self.widget:
            return
        if self.groupNUID != nuId:
            return
        self.widget.msgInput.textField.text = publicAnnouncement

    def setGroupNameSuccess(self, nuId, newName):
        if not self.widget:
            return
        if self.groupNUID != nuId:
            return
        self.widget.groupNameEdit.textField.text = newName

    def changedAcceptOpSuccess(self, nuId):
        if not self.widget:
            return
        if self.groupNUID != nuId:
            return
        self.widget.checkBox.disabled = False

    def checkGroupName(self, newName):
        p = BigWorld.player()
        if not newName or newName.isspace():
            p.showGameMsg(GMDD.data.GROUP_CHAT_NAME_EMPTY, ())
            return False
        tmpStr = unicode(newName, utils.defaultEncoding())
        if len(tmpStr) < MIN_GROUP_NAME:
            p.showGameMsg(GMDD.data.GROUP_CHAT_NAME_SHORT, ())
            return False
        retval, newName = taboo.checkNameDisWord(newName)
        if not retval:
            p.showGameMsg(GMDD.data.GROUP_CHAT_NAME_DISWORD, ())
            return False
        return True
