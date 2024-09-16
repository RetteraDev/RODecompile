#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildTournamentApplyProxy.o
import BigWorld
import const
import gameglobal
import uiUtils
import uiConst
from uiProxy import UIProxy
from data import guild_tournament_data as GTD

class GuildTournamentApplyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildTournamentApplyProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        self.groupId = 0
        self.subGroupId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_TOURNAMENT_APPLY, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_TOURNAMENT_APPLY:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_TOURNAMENT_APPLY)

    def reset(self):
        self.groupId = 0

    def show(self, groupId, subGroupId = 0):
        self.groupId = groupId
        self.subGroupId = subGroupId
        if self.mediator:
            self.refreshInfo()
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_TOURNAMENT_APPLY)

    def refreshInfo(self):
        if self.mediator:
            baseData = GTD.data.get(self.groupId, {})
            if not baseData:
                return
            info = {}
            info['title'] = baseData.get('applyTitle', '')
            if gameglobal.rds.configData.get('enableGuildTournamentTestBF', False):
                num = baseData.get('testMaxNum', 0)
            else:
                num = baseData.get('maxNum', 0)
            if not gameglobal.rds.configData.get('enableGuildTournamentMultiGroup', False):
                info['num'] = baseData.get('applyNum', '%d') % num
            else:
                info['num'] = baseData.get('applyNumMulti', '')
            if gameglobal.rds.configData.get('enableWWGuildTournament', False):
                info['level'] = baseData.get('wwapplyLevel', '')
            else:
                info['level'] = baseData.get('applyLevel', '')
            p = BigWorld.player()
            guildTournament = p.guildTournament.get(self.groupId)
            if gameglobal.rds.configData.get('enableGuildTournamentMultiGroup', False):
                isSeed = guildTournament.subGroups[self.subGroupId].isSeed
            else:
                isSeed = guildTournament.isSeed
            if guildTournament and isSeed:
                if not gameglobal.rds.configData.get('enableGuildTournamentMultiGroup', False):
                    info['desc'] = baseData.get('applySeedDesc', '')
                else:
                    info['desc'] = baseData.get('applySeedDescMulti', '')
            elif not gameglobal.rds.configData.get('enableGuildTournamentMultiGroup', False):
                info['desc'] = baseData.get('applyDesc', '%d') % (const.GUILD_TOURNAMENT_REAL_MAX_CANDIDATES - guildTournament.appliedSeedNum)
            else:
                info['desc'] = baseData.get('applyDescMulti', '%d') % (const.GUILD_TOURNAMENT_REAL_MAX_CANDIDATES - guildTournament.appliedSeedNum)
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        BigWorld.player().cell.applyGuildTournament(self.groupId, self.subGroupId)
        self.hide()
