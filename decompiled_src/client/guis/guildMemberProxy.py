#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildMemberProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import gametypes
from Scaleform import GfxValue
from guis.ui import gbk2unicode
from uiProxy import UIProxy
FLOW_BACK_DESC = gameStrings.TEXT_GUILDMEMBERPROXY_12

class GuildMemberProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildMemberProxy, self).__init__(uiAdapter)
        self.modelMap = {'initData': self.onInitData,
         'accept': self.onAccept,
         'reject': self.onReject,
         'rejectAll': self.onRejectAll,
         'autoAccept': self.onAutoAccept,
         'getRadioSelect': self.onGetRadioSelect,
         'showLvSet': self.onShowLvSet}
        self.mediator = None
        self.data = None
        self.autoAccept = None
        self.autoLv = 0
        self.updateGuildAutoAcceptHandle = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_MEMBER, self.hide)
        self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_APPLY, {'click': self.clickApplyPush})

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_MEMBER:
            self.mediator = mediator

    def clickApplyPush(self):
        gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_GUILD_APPLY, {'data': 'data'})
        self.getGuildApplyList()

    def getGuildApplyList(self, needToFront = False):
        if self.mediator:
            if needToFront:
                self.mediator.Invoke('swapPanelToFront')
        BigWorld.player().cell.getGuildApplyList(1)

    def show(self, data):
        self.data = data
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_MEMBER)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_MEMBER)

    def reset(self):
        self.data = None
        self.autoAccept = None
        if self.updateGuildAutoAcceptHandle:
            BigWorld.cancelCallback(self.updateGuildAutoAcceptHandle)
            self.updateGuildAutoAcceptHandle = None
        else:
            self.updateGuildAutoAcceptHandle = None

    def onAccept(self, *arg):
        BigWorld.player().cell.acceptGuildApply(int(arg[3][0].GetString()))

    def onReject(self, *arg):
        BigWorld.player().cell.rejectGuildApply(int(arg[3][0].GetString()))

    def onRejectAll(self, *arg):
        BigWorld.player().cell.rejectGuildApplyAll()

    def onInitData(self, *arg):
        self.refreshInfo()

    def refreshInfo(self):
        if self.mediator:
            guild = BigWorld.player().guild
            if not guild:
                self.hide()
                return
            info = {}
            self.autoAccept = guild.options.get(gametypes.GUILD_OPTION_AUTO_ACCEPT, 0)
            info['autoAccept'] = self.autoAccept
            info['autoAcceptEnabled'] = guild.memberMe.roleId == gametypes.GUILD_ROLE_LEADER
            info['memberList'] = self.data if self.data else []
            info['autoLv'] = FLOW_BACK_DESC % guild.options.get(gametypes.GUILD_OPTION_AUTO_ACCEPT_LV, 0)
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onAutoAccept(self, *arg):
        autoAccept = int(arg[3][0].GetString())
        if self.autoAccept == autoAccept:
            return
        self.autoAccept = autoAccept
        if not self.updateGuildAutoAcceptHandle:
            self.updateGuildAutoAcceptHandle = BigWorld.callback(1, self.updateGuildAutoAccept)

    def updateGuildAutoAccept(self):
        if self.updateGuildAutoAcceptHandle:
            BigWorld.cancelCallback(self.updateGuildAutoAcceptHandle)
            self.updateGuildAutoAcceptHandle = None
            if self.autoAccept != gametypes.GUILD_AUTO_ACCEPT_FLOWBACK:
                BigWorld.player().cell.updateGuildAutoAccept(self.autoAccept, 0)
            else:
                BigWorld.player().cell.updateGuildAutoAccept(self.autoAccept, self.autoLv)

    def onGetRadioSelect(self, *args):
        self.autoAccept = BigWorld.player().guild.options.get(gametypes.GUILD_OPTION_AUTO_ACCEPT, 0)
        return GfxValue(self.autoAccept)

    def setAutoLv(self, lv):
        self.autoLv = lv
        if self.mediator:
            str = FLOW_BACK_DESC % lv
            self.mediator.Invoke('setLvRadio', GfxValue(gbk2unicode(str)))

    def onShowLvSet(self, *args):
        gameglobal.rds.ui.guildMemberLvSet.show()
