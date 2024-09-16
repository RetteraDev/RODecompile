#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cCControlProxy.o
import BigWorld
import gameglobal
import gamelog
import const
from guis import uiConst
from guis.uiProxy import UIProxy
from helpers import cc
from guis import uiUtils

class CCControlProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CCControlProxy, self).__init__(uiAdapter)
        self.modelMap = {'dismiss': self.dismiss,
         'getCurrentInfo': self.onGetCurrentInfo,
         'doCCGuild': self.onDoCCGuild,
         'doCCGroup': self.onDoCCGroup,
         'doCCAuthority': self.onDoCCAuthority,
         'doAction': self.doAction}
        self.mediator = None
        self.isShow = False
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CC_CONTROL, self.closeWidget)

    def reset(self):
        self.dismiss()

    def doAction(self, *arg):
        tag = arg[3][0].GetString()
        p = BigWorld.player()
        if tag == 'create':
            gameglobal.rds.ui.cCCreateRoom.show()
            self.closeWidget()
        elif tag == 'open':
            cc.openCCRoomIntoFront()
        elif tag == 'share':
            p.doShareCurrentCid()
        elif tag == 'close':
            cc.closeCC()
        gamelog.debug('jinjj----------------tag', tag)

    def onDoCCGuild(self, *arg):
        p = BigWorld.player()
        p.doJoinGuildCCChannel()

    def onDoCCGroup(self, *arg):
        p = BigWorld.player()
        p.doJoinTeamChannel()

    def onDoCCAuthority(self, *arg):
        p = BigWorld.player()
        p.doJoinAuthorityChannel()

    def onGetCurrentInfo(self, *arg):
        return self._onGetCurrentInfo()

    def _onGetCurrentInfo(self, isClose = False):
        data = {}
        if isClose == False:
            data['isStartCC'] = cc.isStartCC()
            data['joinIngRoomId'] = cc.getCurrentCid()
        else:
            data['isStartCC'] = False
            data['joinIngRoomId'] = None
        p = BigWorld.player()
        if hasattr(p, 'guild'):
            if p.guild == None:
                data['isInGuild'] = False
            else:
                data['isInGuild'] = True
        else:
            data['isInGuild'] = False
        data['isInTeam'] = p.groupNUID
        if not data['isStartCC']:
            data['title'] = const.CC_CONTROL_TITLE_1
        elif not data['joinIngRoomId']:
            data['title'] = const.CC_CONTROL_TITLE_2
        else:
            data['title'] = const.CC_CONTROL_TITLE_3
        return uiUtils.dict2GfxDict(data, True)

    def refreshPanel(self, isClose = False):
        if self.mediator:
            data = self._onGetCurrentInfo(isClose)
            self.mediator.Invoke('refrashPanel', data)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def show(self):
        pass

    def dismiss(self, *arg):
        if self.isShow:
            self.uiAdapter.unLoadWidget(uiConst.WIDGET_CC_CONTROL)
        self.isShow = False

    def closeWidget(self):
        if self.isShow:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CC_CONTROL)
        self.isShow = False

    def toggle(self):
        gamelog.debug('jinjj----toggle')
        if self.isShow:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CC_CONTROL)
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CC_CONTROL)
        self.isShow = not self.isShow
