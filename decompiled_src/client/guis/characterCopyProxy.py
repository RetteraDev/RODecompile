#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/characterCopyProxy.o
from gamestrings import gameStrings
import copy
import BigWorld
import const
import gameglobal
from guis import uiConst
from guis.uiProxy import UIProxy
from ui import unicode2gbk
from guis import uiUtils
from guis import ui
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD

class CharacterCopyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CharacterCopyProxy, self).__init__(uiAdapter)
        self.modelMap = {'getContent': self.onGetContent,
         'confirm': self.commit}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHARACTER_COPY, self.clearWidget)

    def onGetContent(self, *args):
        serverList = copy.copy(SCD.data.get('serverList', [gameStrings.TEXT_CHARACTERCOPYPROXY_32, gameStrings.TEXT_CHARACTERCOPYPROXY_32_1]))
        if const.SERVER_CORPERATION in serverList:
            serverList.remove(const.SERVER_CORPERATION)
        return uiUtils.array2GfxAarry(serverList, True)

    @ui.callFilter(1)
    def commit(self, *args):
        serverName = unicode2gbk(args[3][0].GetString())
        name = unicode2gbk(args[3][1].GetString())
        if len(name) >= 4:
            BigWorld.player().base.avatarPeekAnother(serverName, name)
        else:
            BigWorld.player().showGameMsg(GMDD.data.NAME_LENGTH_NOT_ENOUGH, ())

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def clearWidget(self):
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        if self.mediator:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHARACTER_COPY)
        self.mediator = None

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHARACTER_COPY)
