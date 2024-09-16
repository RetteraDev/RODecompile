#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildPostProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import uiConst
import uiUtils
from uiProxy import UIProxy
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD

class GuildPostProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildPostProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm,
         'initData': self.onInitData}
        self.mediator = None
        self.memberGbId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_POST, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_POST:
            self.mediator = mediator

    def show(self, memberGbId):
        if memberGbId == BigWorld.player().gbId:
            BigWorld.player().showGameMsg(GMDD.data.GUILD_APPOINT_SELF_NOT_ALLOWED, ())
            return
        self.memberGbId = memberGbId
        if self.mediator:
            self.refreshInfo()
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_POST)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_POST)

    def reset(self):
        self.memberGbId = 0

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            if not guild.member.has_key(self.memberGbId):
                return
            numRoleDict = {}
            enableWingWorldArmy = gameglobal.rds.configData.get('enableWingWorldGuildRoleOptimization', False)
            for role in gametypes.GUILD_ROLE_LIST:
                numRoleDict[role] = 0

            for gbId in guild.member:
                numRoleDict[guild.member[gbId].roleId] += 1

            data = []
            for role in gametypes.GUILD_ROLE_LIST:
                if role in gametypes.GUILD_ROLE_IN_WING_WORLD and not enableWingWorldArmy:
                    visible = False
                elif role == gametypes.GUILD_ROLE_LADY:
                    visible = gameglobal.rds.configData.get('enableGuildLady', False)
                else:
                    visible = True
                if role == gametypes.GUILD_ROLE_LEADER:
                    labelName = gameStrings.TEXT_GUILDPOSTPROXY_72
                elif role == gametypes.GUILD_ROLE_NORMAL:
                    labelName = gameStrings.TEXT_GUILDPOSTPROXY_74
                else:
                    labelName = '%s(%d/%d)' % (gametypes.GUILD_ROLE_DICT[role], numRoleDict[role], guild._getMaxRoleIdCount(role))
                data.append((visible, labelName))

            data.append(guild.member[self.memberGbId].role)
            data.append(gametypes.GUILD_ROLE_DICT[guild.member[self.memberGbId].roleId])
            data.append(gametypes.GUILD_ROLE_LIST.index(guild.member[self.memberGbId].roleId))
            self.mediator.Invoke('refreshInfo', uiUtils.array2GfxAarry(data, True))

    def onConfirm(self, *arg):
        if self.memberGbId:
            p = BigWorld.player()
            roleIdx = int(arg[3][0].GetNumber())
            if p.guild.member.has_key(self.memberGbId):
                if gametypes.GUILD_ROLE_LIST[roleIdx] == gametypes.GUILD_ROLE_LEADER:
                    msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_POST_LEADER_HINT, '')
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.conformResignOK, self.memberGbId, p.guild.member[self.memberGbId].role))
                else:
                    p.cell.guildAppoint(self.memberGbId, p.guild.member[self.memberGbId].role, gametypes.GUILD_ROLE_LIST[roleIdx])
        self.hide()

    def conformResignOK(self, gbId, role):
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableInventoryLock', False):
            p.getCipher(p.cell.guildResign, (gbId, role))
        else:
            p.cell.guildResign('', gbId, role)

    def onInitData(self, *arg):
        self.refreshInfo()
