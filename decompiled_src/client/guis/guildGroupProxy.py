#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildGroupProxy.o
import BigWorld
import gameglobal
import gametypes
from guis import uiConst
from ui import unicode2gbk
from uiProxy import UIProxy
from guis import uiUtils

class GuildGroupProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildGroupProxy, self).__init__(uiAdapter)
        self.modelMap = {'getGroupInfo': self.onGetGroupInfo,
         'confirmGroup': self.onConfirmGroup,
         'deleteGroup': self.onDeleteGroup,
         'createGroup': self.onCreateGroup}
        self.mediator = None
        self.canRefresh = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_GROUP, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_GROUP:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_GROUP)

    def show(self):
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_GROUP)

    def onGetGroupInfo(self, *arg):
        self.canRefresh = True
        self.refreshGroupInfo()

    def refreshGroupInfo(self):
        if self.canRefresh == False:
            return
        if self.mediator:
            self.canRefresh = False
            guild = BigWorld.player().guild
            groupList = []
            groups = [ x for x in guild.group.itervalues() if x.groupId not in gametypes.GUILD_TOURNAMENT_GUILD_GROUP ]
            groups.sort(key=lambda x: x.tWhen)
            for group in groups:
                if gametypes.GUILD_TOURNAMENT_GUILD_FAKE_GROUP.has_key(group.groupId):
                    continue
                groupList.append([group.groupId, group.name])

            self.mediator.Invoke('refreshGroupInfo', uiUtils.array2GfxAarry(groupList, True))

    def onConfirmGroup(self, *arg):
        groupId = int(arg[3][0].GetNumber())
        name = unicode2gbk(arg[3][1].GetString())
        self.canRefresh = True
        BigWorld.player().cell.renameGuildGroup(groupId, name)

    def onDeleteGroup(self, *arg):
        groupId = int(arg[3][0].GetNumber())
        self.canRefresh = True
        BigWorld.player().cell.removeGuildGroup(groupId)

    def onCreateGroup(self, *arg):
        name = unicode2gbk(arg[3][0].GetString())
        self.canRefresh = True
        BigWorld.player().cell.addGuildGroup(name)
