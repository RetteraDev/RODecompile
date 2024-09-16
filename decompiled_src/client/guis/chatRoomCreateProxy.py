#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/chatRoomCreateProxy.o
import BigWorld
import gameglobal
import uiConst
import const
import uiUtils
import gametypes
from ui import unicode2gbk
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD

class ChatRoomCreateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChatRoomCreateProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'clickConfirm': self.onClickConfirm,
         'noRoomName': self.onNoRoomName,
         'getInitDate': self.GetInitDate}
        self.mediator = None
        self.type = uiConst.CHATROOM_CREATE
        self.data = ()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHATROOM_CREATE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CHATROOM_CREATE:
            self.mediator = mediator

    def show(self, type, data = ()):
        if not BigWorld.player().checkMapLimitUI(gametypes.MAP_LIMIT_UI_CHATROOM):
            return
        if self.mediator:
            return
        self.type = type
        self.data = data
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHATROOM_CREATE, True)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHATROOM_CREATE)

    def reset(self):
        super(self.__class__, self).reset()
        self.type = uiConst.CHATROOM_CREATE
        self.data = ()

    def onClickClose(self, *arg):
        self.hide()

    def onClickConfirm(self, *arg):
        if arg[3][2].GetString() == 'true':
            password = unicode2gbk(arg[3][3].GetString())
        else:
            password = ''
        chatRoomName = unicode2gbk(arg[3][1].GetString())
        if len(chatRoomName) > const.BOOTH_NAME_MAX * 2:
            BigWorld.player().showGameMsg(GMDD.data.CHATROOM_CREATE_TOO_LONG_NAME, ())
            return
        if self.type == uiConst.CHATROOM_CREATE:
            BigWorld.player().cell.createChatRoom(chatRoomName, int(arg[3][0].GetString()), password)
        elif self.type == uiConst.CHATROOM_RESET:
            BigWorld.player().cell.resetChatRoom(chatRoomName, int(arg[3][0].GetString()), password)
        self.hide()

    def GetInitDate(self, *arg):
        if self.type == uiConst.CHATROOM_RESET:
            self.updateData()

    def updateData(self):
        if self.mediator:
            self.mediator.Invoke('updateData', uiUtils.array2GfxAarry(self.data, True))

    def onNoRoomName(self, *arg):
        BigWorld.player().showGameMsg(GMDD.data.CHATROOM_CREATE_NOT_NAME, ())
