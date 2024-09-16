#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildWWTournamentRankProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import uiConst
import utils
import gametypes
from uiProxy import UIProxy
from Scaleform import GfxValue
from data import bonus_data as BD
from cdata import ww_gtn_month_reward_data as WGMRD

class GuildWWTournamentRankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildWWTournamentRankProxy, self).__init__(uiAdapter)
        self.modelMap = {'getRankInfo': self.onGetRankInfo}
        self.mediator = None
        self.groupId = 0
        self.rankMap = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_WW_GUILD_TOURNAMENT_RANK, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_WW_GUILD_TOURNAMENT_RANK:
            self.mediator = mediator
            return GfxValue(self.tabIdx)

    def onGetRankInfo(self, *args):
        groupId = int(args[3][0].GetNumber())
        if groupId != self.groupId:
            self.groupId = groupId
            self.queryRankInfo()
        self.refreshInfo()

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            guildTournament = p.guildTournament.get(self.groupId)
            if not guildTournament:
                return
            if not self.rankMap:
                self.initRankMap()
            rankList = []
            for rankItem in guildTournament.ranks:
                rankInfo = {}
                rankInfo['rank'] = rankItem.rank
                rankInfo['guildName'] = rankItem.guildName
                rankInfo['score'] = rankItem.score
                if gameglobal.rds.configData.get('enableGuildTournamentSeason', False):
                    rankInfo['totalScore'] = rankItem.totalScore
                elif rankInfo['rank'] <= 4:
                    rankInfo['rankStatus'] = gameStrings.TEXT_GUILDWWTOURNAMENTRANKPROXY_58
                elif rankInfo['rank'] > 4 and rankInfo['rank'] <= 8:
                    rankInfo['rankStatus'] = gameStrings.TEXT_GUILDWWTOURNAMENTRANKPROXY_60
                else:
                    rankInfo['rankStatus'] = gameStrings.TEXT_GUILDWWTOURNAMENTRANKPROXY_62
                rid = self.rankMap.get((self.groupId, rankItem.rank), 0)
                bonusId = WGMRD.data.get((self.groupId, rid), {}).get('bonusId', 0)
                fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', [])
                fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
                slotList = []
                for item in fixedBonus:
                    slotList.append(uiUtils.getGfxItemById(item[1], count=item[2]))

                rankInfo['slotList'] = slotList
                rankList.append(rankInfo)

            self.mediator.Invoke('refreshInfo', uiUtils.array2GfxAarry(rankList, True))

    def queryRankInfo(self):
        p = BigWorld.player()
        guildTournament = p.guildTournament.get(self.groupId)
        if gameglobal.rds.configData.get('enableGuildTournamentSeason', False):
            p.cell.queryGuildTournamentRanks(self.groupId, guildTournament.rankVer)
        else:
            p.cell.queryWWGuildTournamentRanks(self.groupId, gametypes.GUILD_TOURNAMENT_QUERY_FOR_RANK, guildTournament.rankVer)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WW_GUILD_TOURNAMENT_RANK)

    def show(self, groupId):
        self.groupId = groupId
        self.tabIdx = groupId - 1
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WW_GUILD_TOURNAMENT_RANK)

    def initRankMap(self):
        rids = WGMRD.data.keys()
        for groupId, rid in rids:
            if isinstance(rid, tuple):
                for rank in range(rid[0], rid[1] + 1):
                    self.rankMap[groupId, rank] = rid

            else:
                self.rankMap[groupId, rid] = rid
