#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildMemberAssginProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
from uiProxy import UIProxy
from ui import unicode2gbk

class GuildMemberAssginProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildMemberAssginProxy, self).__init__(uiAdapter)
        self.modelMap = {'initData': self.onInitData,
         'confirm': self.onConfirm}
        self.mediator = None
        self.page = 0
        self.pos = 0
        self.data = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_MEMBER_ASSGIN, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_MEMBER_ASSGIN:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_MEMBER_ASSGIN)

    def reset(self):
        self.page = 0
        self.pos = 0

    def show(self, page, pos, data):
        self.page = page
        self.pos = pos
        self.data = data
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_MEMBER_ASSGIN)

    def onInitData(self, *arg):
        self.refreshInfo()

    def onConfirm(self, *arg):
        bgId = int(arg[3][0].GetString())
        roleName = unicode2gbk(arg[3][1].GetString())
        p = BigWorld.player()
        if p.guild:
            sItem = p.guild.storage.getQuickVal(self.page, self.pos)
            if sItem:
                p.cell.storageGuildAssign(self.page, self.pos, sItem.uuid, bgId, roleName)
        self.hide()

    def refreshInfo(self):
        if self.mediator:
            self.mediator.Invoke('refreshInfo', uiUtils.array2GfxAarry(self.data, True))
