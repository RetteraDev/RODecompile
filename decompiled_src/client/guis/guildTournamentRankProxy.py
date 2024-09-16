#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildTournamentRankProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
import utils
import gametypes
from uiProxy import UIProxy
from Scaleform import GfxValue
from data import bonus_data as BD
from cdata import guild_tournament_month_reward_data as GTMRD

class GuildTournamentRankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildTournamentRankProxy, self).__init__(uiAdapter)
        self.modelMap = {'getRankInfo': self.onGetRankInfo}
        self.mediator = None
        self.groupId = 0
        self.rankMap = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_TOURNAMENT_RANK, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_TOURNAMENT_RANK:
            self.mediator = mediator
            return GfxValue(self.tabIdx)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_TOURNAMENT_RANK)

    def show(self, groupId):
        self.groupId = groupId
        self.tabIdx = groupId - 1
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
            self.mediator.Invoke('setTabIndex', GfxValue(self.tabIdx))
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_TOURNAMENT_RANK)

    def queryRankInfo(self):
        p = BigWorld.player()
        guildTournament = p.guildTournament.get(self.groupId)
        p.cell.queryGuildTournamentRanks(self.groupId, guildTournament.rankVer)

    def onGetRankInfo(self, *arg):
        self.groupId = int(arg[3][0].GetNumber())
        self.refreshInfo(self.groupId)
        self.queryRankInfo()

    def refreshInfo(self, groupId):
        if self.groupId != groupId:
            return
        if self.mediator:
            p = BigWorld.player()
            guildTournament = p.guildTournament.get(self.groupId)
            if not guildTournament:
                return
            if not self.rankMap:
                self.initRankMap()
            info = {}
            rankList = []
            for rankItem in guildTournament.ranks:
                rankInfo = {}
                rankInfo['rank'] = rankItem.rank
                rankInfo['guildName'] = rankItem.guildName
                rankInfo['score'] = rankItem.score
                rid = self.rankMap.get((self.groupId, rankItem.rank), 0)
                bonusId = GTMRD.data.get((self.groupId, rid), {}).get('bonusId', 0)
                fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', [])
                fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
                slotList = []
                for item in fixedBonus:
                    slotList.append(uiUtils.getGfxItemById(item[1], count=item[2]))

                rankInfo['slotList'] = slotList
                rankList.append(rankInfo)

            info['rankList'] = rankList
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def initRankMap(self):
        rids = GTMRD.data.keys()
        for groupId, rid in rids:
            if isinstance(rid, tuple):
                for rank in range(rid[0], rid[1] + 1):
                    self.rankMap[groupId, rank] = rid

            else:
                self.rankMap[groupId, rid] = rid
