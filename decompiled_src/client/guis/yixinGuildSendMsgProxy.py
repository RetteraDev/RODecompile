#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yixinGuildSendMsgProxy.o
import BigWorld
import gameglobal
from guis import uiConst
from guis.uiProxy import UIProxy
from ui import unicode2gbk
from helpers import taboo
from cdata import game_msg_def_data as GMDD

class YixinGuildSendMsgProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(YixinGuildSendMsgProxy, self).__init__(uiAdapter)
        self.modelMap = {'dismiss': self.dismiss,
         'sendChatMsg': self.onSendMsg}
        self.mediator = None
        self.isShow = False
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_YIXIN_GUILD_SEND_MSG, self.closeWidget)

    def reset(self):
        self.dismiss()

    def onSendMsg(self, *args):
        msg = unicode2gbk(args[3][0].GetString())
        p = BigWorld.player()
        isNormal, msg = taboo.checkDisbWord(msg)
        if not isNormal:
            p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_TABOO, ())
            return
        isNormal, msg = taboo.checkBSingle(msg)
        if len(msg):
            BigWorld.player().cell.sendPublicYixinMsg(msg)
            self.closeWidget()

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def dismiss(self, *arg):
        self.closeWidget()

    def closeWidget(self):
        if self.isShow:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YIXIN_GUILD_SEND_MSG)
        self.isShow = False
        self.mediator = None

    def toggle(self):
        if self.isShow:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YIXIN_GUILD_SEND_MSG)
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YIXIN_GUILD_SEND_MSG)
        self.isShow = not self.isShow
