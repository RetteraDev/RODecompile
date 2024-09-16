#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impChatRoom.o
import BigWorld
import gameglobal
import gametypes
from guis import uiConst
from helpers.chatRoom import Member, ChatRoom
from cdata import game_msg_def_data as GMDD

class ImpChatRoom(object):

    def set_chatRoomNUID(self, old):
        p = BigWorld.player()
        if self == p:
            if old and not self.chatRoomNUID:
                p.motionUnpin()
                gameglobal.rds.ui.chatRoomWindow.hide()
            if self.chatRoomNUID and not old:
                p.ap.stopMove(True)
                p.motionPin()

    def set_chatRoomName(self, old):
        if self.chatRoomName:
            self.topLogo.setChatRoomVisible(True)
            self.topLogo.setChatRoomName(self.chatRoomName)
        else:
            self.topLogo.setChatRoomVisible(False)

    def onResetChatRoom(self, chatRoomName):
        self.chatRoom.fName = chatRoomName
        gameglobal.rds.ui.chatRoomWindow.updateName()

    def onLoadChatRoom(self, data):
        rHeader, rBuild, tBuild, fName, fType, member = data
        chatRoom = ChatRoom()
        chatRoom.rHeader = rHeader
        chatRoom.rBuild = rBuild
        chatRoom.tBuild = tBuild
        chatRoom.fName = fName
        chatRoom.fType = fType
        for gbId, role, school, level, sex, tJoin, roleId in member:
            chatRoom.member[gbId] = Member(gbId=gbId, role=role, school=school, level=level, sex=sex, roleId=roleId, tJoin=tJoin)

        self.chatRoom = chatRoom
        gameglobal.rds.ui.chatRoomWindow.show()

    def onAddMemberChatRoom(self, gbId, role, school, level, sex, tJoin, roleId):
        if self.chatRoomNUID:
            self.chatRoom.member[gbId] = Member(gbId=gbId, role=role, school=school, level=level, sex=sex, roleId=roleId, tJoin=tJoin)
            gameglobal.rds.ui.chatRoomWindow.refreshInfo()

    def onDelMemberChatRoom(self, gbId):
        if self.chatRoomNUID:
            self.chatRoom.member.pop(gbId, None)
            gameglobal.rds.ui.chatRoomWindow.refreshInfo()

    def onLeaveChatRoom(self, chatRoomName):
        self.chatRoom = None

    def onKickedoutChatRoom(self, role):
        self.chatRoom = None
        self.showGameMsg(GMDD.data.CHATROOM_KICKEDOUT, (role,))

    def onAppointChatRoom(self, gbId):
        if self.chatRoomNUID:
            self.chatRoom.rHeader = gbId
            self.chatRoom.member[gbId].roleId = gametypes.CHATROOM_ROLE_LEADER
            gameglobal.rds.ui.chatRoomWindow.memberAppoint(gbId)

    def onMemberLevelUpdateChatRoom(self, gbId, lv):
        if self.chatRoomNUID:
            self.chatRoom.member[gbId].level = lv
            gameglobal.rds.ui.chatRoomWindow.memberLevelUpdate(gbId, lv)

    def onMemberRenameChatRoom(self, gbId, name):
        if self.chatRoom:
            self.chatRoom.member[gbId].role = name
            gameglobal.rds.ui.chatRoomWindow.memberRename(gbId, name)

    def beChatToChatRoom(self, gbId, msg):
        if self.chatRoom:
            if gbId in self.chatRoom.member:
                gameglobal.rds.ui.chatRoomWindow.receiveMsg(gbId, msg)

    def showChatRoomPasswordWiget(self, chatRoomNUID, chatRoomName):
        gameglobal.rds.ui.chatRoomPassword.show(chatRoomNUID, chatRoomName)

    def onGetChatRoomData(self, chatRoomName, chatType, password):
        gameglobal.rds.ui.chatRoomCreate.show(uiConst.CHATROOM_RESET, (chatRoomName, chatType, password))
