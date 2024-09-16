#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/prosecuteProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
import gametypes
from gamestrings import gameStrings
from guis import uiUtils
from uiProxy import UIProxy
from ui import unicode2gbk
from data import menu_config_data as MCD
from cdata import game_msg_def_data as GMDD

class ProsecuteProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ProsecuteProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm,
         'close': self.onClose,
         'initData': self.onInitData,
         'getGbId': self.onGetGbId}
        self.mediator = None
        self.entName = None
        self.source = None
        self.boothName = ''
        self.msg = ''
        self.channel = -1
        self.timeStamp = 0
        self.gbId = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_PROSECUTE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PROSECUTE:
            self.mediator = mediator

    def onGetGbId(self, *args):
        return GfxValue(self.gbId)

    def show(self, entName, source, boothName = '', msg = None):
        if self.entName != entName or self.source != source:
            self.source = source
            self.entName = entName
            self.boothName = boothName
            if source == uiConst.MENU_CHAT:
                self.timeStamp = int(gameglobal.rds.ui.chat.chatTimestamp)
                self.channel = int(gameglobal.rds.ui.chat.chatChannelId)
                if self.channel < 0:
                    self.source = uiConst.MENU_CHAT_SYSTEM
                self.msg = gameglobal.rds.ui.chat.chatMsg
            elif source == uiConst.MENU_ANONYMOUS:
                self.timeStamp = int(gameglobal.rds.ui.chat.chatTimestamp)
                self.channel = int(gameglobal.rds.ui.chat.chatChannelId)
                self.msg = gameglobal.rds.ui.chat.chatMsg
                self.gbId = self.entName
                self.entName = uiUtils.getTextFromGMD(GMDD.data.PROSECUTE_TARGET, gameStrings.TEXT_PROSECUTEPROXY_61)
            elif source == uiConst.MENU_GUILD_BILLBOARD_PICTURE:
                self.gbId = self.entName
            else:
                self.msg = ''
                self.channel = -1
                self.timeStamp = 0
            if msg:
                self.msg = msg
            if self.mediator:
                self.refresh()
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PROSECUTE)

    def refresh(self):
        if self.mediator:
            self.mediator.Invoke('refresh', self.onInitData())

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PROSECUTE)

    def reset(self):
        super(self.__class__, self).reset()
        self.entName = None
        self.source = None
        self.msg = ''
        self.gbId = ''

    def onClose(self, *arg):
        self.hide()

    def setMailProsecuteArg(self, extra):
        self.channel = const.CHAT_CHANNEL_MAIL
        self.timeStamp = extra.get('timeStamp', 0)
        self.msg = extra.get('msg', '')
        self.entName = extra.get('fromRole')

    def onConfirm(self, *arg):
        p = BigWorld.player()
        index = int(arg[3][0].GetNumber())
        addToBlackName = arg[3][1].GetBool()
        msg = unicode2gbk(arg[3][2].GetString())
        if p.isolateType != gametypes.ISOLATE_TYPE_NONE:
            p.showGameMsg(GMDD.data.FORBIDDEN_IN_ISOLATE, ())
            return
        if not self.gbId:
            BigWorld.player().cell.reportProsecute(self.entName, index, self.channel, self.timeStamp, msg, self.boothName)
        else:
            BigWorld.player().cell.reportProsecute(self.gbId, index, self.channel, self.timeStamp, msg, self.boothName)
        if addToBlackName:
            p.base.addContact(self.entName, gametypes.FRIEND_GROUP_BLOCK, 0)
        self.hide()

    def onInitData(self, *arg):
        ret = {'entName': self.entName}
        prosecuteItems = list(MCD.data.get(self.source, {}).get('prosecuteItems', []))
        if not self.boothName and gametypes.PROSECUTE_TYPE_ILLEGAL_BOOTHNAME in prosecuteItems:
            prosecuteItems.remove(gametypes.PROSECUTE_TYPE_ILLEGAL_BOOTHNAME)
        prosecuteItems = [ (dataId, gameStrings.PROSECUTE_TXT_MAP[dataId]) for dataId in prosecuteItems ]
        ret['prosecuteItems'] = prosecuteItems
        ret['source'] = self.source
        ret['boothName'] = self.boothName
        ret['msg'] = self.msg
        ret['channel'] = self.channel
        return uiUtils.dict2GfxDict(ret, True)
