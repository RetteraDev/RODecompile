#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/clanCreateProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
import uiUtils
import gametypes
from ui import unicode2gbk
from uiProxy import UIProxy
from helpers import taboo
from data import guild_config_data as GCD
from cdata import game_msg_def_data as GMDD

class ClanCreateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ClanCreateProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm,
         'close': self.onClose,
         'initData': self.onInitData}
        self.mediator = None
        self.npcId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_CLAN_CREATE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CLAN_CREATE:
            self.mediator = mediator

    def show(self, npcId):
        if not gameglobal.rds.configData.get('enableClan', False):
            BigWorld.player().showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
            return
        if not self.mediator:
            p = BigWorld.player()
            if not p.guildNUID:
                p.showGameMsg(GMDD.data.GUILD_NOT_JOINED, (const.YOU,))
                return
            if not p.guild.memberMe.roleId == gametypes.GUILD_ROLE_LEADER:
                p.showGameMsg(GMDD.data.CLAN_CREATE_NOT_AUTHORIZED, ())
                return
            if p.clanNUID:
                p.showGameMsg(GMDD.data.CLAN_CREATE_ALREADY_JOINED, ())
                return
            self.npcId = npcId
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CLAN_CREATE)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CLAN_CREATE)

    def reset(self):
        super(self.__class__, self).reset()
        self.npcId = 0

    def onClose(self, *arg):
        self.hide()

    def onConfirm(self, *arg):
        p = BigWorld.player()
        name = unicode2gbk(arg[3][0].GetString())
        result, _ = taboo.checkNameDisWord(name)
        if not result:
            p.showGameMsg(GMDD.data.CLAN_NAME_TABOO, ())
            return
        nameLength = int(arg[3][1].GetString())
        if nameLength < const.CLAN_NAME_MIN_LEN / 2:
            p.showGameMsg(GMDD.data.CLAN_INVALID_NAME, (const.CLAN_NAME_MIN_LEN / 2, const.CLAN_NAME_MAX_LEN / 2))
            return
        npc = BigWorld.entities.get(self.npcId)
        if npc:
            npc.cell.createClan(name)
        self.hide()

    def onInitData(self, *arg):
        return uiUtils.array2GfxAarry([GCD.data.get('clanCreateGuildLv', const.CLAN_CREATE_GUILD_LV), GCD.data.get('clanCreateFee', const.CLAN_CREATE_FEE), BigWorld.player().guild.bindCash], True)

    def updateCash(self):
        if self.mediator:
            self.mediator.Invoke('updateCash', GfxValue(str(BigWorld.player().guild.bindCash)))
