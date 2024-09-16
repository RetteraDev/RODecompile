#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/clanJoinProxy.o
import BigWorld
import gameglobal
import uiConst
import const
import uiUtils
import gametypes
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD

class ClanJoinProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ClanJoinProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        self.data = None
        self.justShow = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_CLAN_JOIN, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CLAN_JOIN:
            self.mediator = mediator
            self.refreshInfo()

    def show(self, data, justShow):
        if not gameglobal.rds.configData.get('enableClan', False):
            BigWorld.player().showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
            return
        if not self.mediator:
            if not justShow:
                p = BigWorld.player()
                if not len(data):
                    p.showGameMsg(GMDD.data.CLAN_JION_NO_CLAN, ())
                    return
                if not p.guildNUID:
                    p.showGameMsg(GMDD.data.GUILD_NOT_JOINED, (const.YOU,))
                    return
                if not p.guild.memberMe.roleId == gametypes.GUILD_ROLE_LEADER:
                    p.showGameMsg(GMDD.data.CLAN_CREATE_NOT_AUTHORIZED, ())
                    return
                if p.clanNUID:
                    p.showGameMsg(GMDD.data.CLAN_ALREADY_JOINED_SELF, ())
                    return
            self.data = data
            self.justShow = justShow
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CLAN_JOIN)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CLAN_JOIN)

    def reset(self):
        self.data = 0
        self.justShow = False

    def refreshInfo(self):
        if self.mediator:
            info = {}
            if self.justShow:
                info['nameTitle'] = '查看联盟'
            else:
                info['nameTitle'] = '加入联盟'
            info['justShow'] = self.justShow
            clanData = []
            for item in self.data:
                clanData.append((str(item[0]),
                 item[1],
                 item[2],
                 item[3]))

            info['clanData'] = clanData
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        BigWorld.player().cell.applyJoinClan(int(arg[3][0].GetString()))
        self.hide()
