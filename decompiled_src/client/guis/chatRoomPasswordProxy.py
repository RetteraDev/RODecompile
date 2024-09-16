#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/chatRoomPasswordProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import gametypes
from ui import gbk2unicode
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD

class ChatRoomPasswordProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChatRoomPasswordProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'getName': self.onGetName,
         'clickConfirm': self.onClickConfirm,
         'noPassword': self.onNoPassword}
        self.mediator = None
        self.chatRoomNUID = 0
        self.chatRoomName = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHATROOM_PASSWORD, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CHATROOM_PASSWORD:
            self.mediator = mediator

    def show(self, chatRoomNUID, chatRoomName):
        if not BigWorld.player().checkMapLimitUI(gametypes.MAP_LIMIT_UI_CHATROOM):
            return
        if self.mediator:
            return
        self.chatRoomNUID = chatRoomNUID
        self.chatRoomName = chatRoomName
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHATROOM_PASSWORD, True)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHATROOM_PASSWORD)

    def reset(self):
        super(self.__class__, self).reset()
        self.chatRoomNUID = 0
        self.chatRoomName = ''

    def onClickClose(self, *arg):
        self.hide()

    def onGetName(self, *arg):
        return GfxValue(gbk2unicode(gameStrings.TEXT_CHATROOMPASSWORDPROXY_57 + self.chatRoomName + gameStrings.TEXT_CHATROOMPASSWORDPROXY_57_1))

    def onNoPassword(self, *arg):
        BigWorld.player().showGameMsg(GMDD.data.CHATROOM_NOT_PASSWORD, ())

    def onClickConfirm(self, *arg):
        password = arg[3][0].GetString()
        if not password:
            return
        BigWorld.player().cell.joinChatRoom(self.chatRoomNUID, password)
        self.hide()
