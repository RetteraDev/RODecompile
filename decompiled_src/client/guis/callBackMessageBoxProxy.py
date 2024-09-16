#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/callBackMessageBoxProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import uiConst
import gameglobal
from uiProxy import UIProxy
from ui import gbk2unicode
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD

class CallBackMessageBoxProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CallBackMessageBoxProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'clickOk': self.onClickOk,
         'clickCancel': self.onClickCancel,
         'getInitData': self.onGetInitData}
        self.mediator = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CALLBACK_MESSAGEBOX:
            self.mediator = mediator

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_CALLBACK_MESSAGEBOX)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CALLBACK_MESSAGEBOX)

    def onClickClose(self, *arg):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PUSH_CALL)
        self.hide()

    def reset(self):
        self.mediator = None

    def onClickSearch(self, *arg):
        if gameglobal.rds.configData.get('enableFriendInvite', False):
            if gameglobal.rds.configData.get('enableSummonFriendV2', False):
                gameglobal.rds.ui.summonFriendBGV2.show()
            else:
                gameglobal.rds.ui.summonFriendNew.show()
        else:
            gameglobal.rds.ui.summonFriend.show(5)
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PUSH_CALL)
        self.hide()

    def onClickOk(self, *arg):
        gameglobal.rds.ui.friend.show()
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PUSH_CALL)
        self.hide()

    def onClickCancel(self, *arg):
        BigWorld.player().base.setShowFlowbackInviteListWithDifferent(True)
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PUSH_CALL)
        self.hide()

    def onGetInitData(self, *arg):
        msg = GMD.data.get(GMDD.data.MSG_CALL_FRIDENDS_TEXT, {}).get('text', gameStrings.TEXT_CALLBACKMESSAGEBOXPROXY_69)
        return GfxValue(gbk2unicode(msg))
