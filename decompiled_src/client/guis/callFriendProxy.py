#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/callFriendProxy.o
from gamestrings import gameStrings
import BigWorld
import uiConst
import uiUtils
from uiProxy import UIProxy
from ui import unicode2gbk
from helpers import taboo
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD

class CallFriendProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CallFriendProxy, self).__init__(uiAdapter)
        self.modelMap = {'send': self.onSend,
         'initModel': self.onInitModel}
        self.mediator = None
        self.friendName = ''
        self.myName = ''
        self.fid = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CALL_FRIEND:
            self.mediator = mediator

    def show(self, fid):
        p = BigWorld.player()
        self.fid = fid
        fVal = p.getFValByGbId(fid)
        self.friendName = fVal.name
        self.myName = p.realRoleName
        self.uiAdapter.loadWidget(uiConst.WIDGET_CALL_FRIEND)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CALL_FRIEND)

    def reset(self):
        self.mediator = None
        self.friendName = ''
        self.myName = ''
        self.fid = None

    def onInitModel(self, *args):
        self.refreshInfo()

    def onSend(self, *args):
        msg = unicode2gbk(args[3][0].GetString())
        p = BigWorld.player()
        if msg:
            isNormal, msg = taboo.checkDisbWord(msg)
            if not isNormal:
                p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_TABOO, ())
                return
            isNormal, msg = taboo.checkBSingle(msg)
            if not isNormal:
                p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_TABOO, ())
                return
            p.base.sendFlowbackInvitation(self.fid, self.friendName, msg)
            self.clearWidget()
        else:
            p.showGameMsg(GMDD.data.CALL_FRIEND_CONTENT_EMPTY_MSG, ())

    def refreshInfo(self):
        if self.mediator:
            ret = {}
            ret['friendName'] = self.friendName
            ret['myName'] = self.myName
            str = SCD.data.get('FLOWBACK_INVITE_PHONE_MSG_TEMPLATE', gameStrings.TEXT_CALLFRIENDPROXY_79) % (self.friendName,
             '',
             uiConst.CALL_FRIEND_URL,
             self.myName)
            ret['inputLenth'] = 65 - uiUtils.getCharLenth(str)
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(ret, True))
