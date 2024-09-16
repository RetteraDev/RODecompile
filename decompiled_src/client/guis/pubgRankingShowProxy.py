#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pubgRankingShowProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import const
import gametypes
import pubgUtils
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis import uiUtils
from guis import teamInviteV2Proxy
from guis import tipUtils
from guis import events
from guis.asObject import ASUtils
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import Tweener
from cdata import game_msg_def_data as GMDD
from data import duel_config_data as DCD
from cdata import pubg_rank_points_data as PRPD

class PubgRankingShowProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PubgRankingShowProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PUBG_RANKING_SHOW_WIDGET, self.hide)

    def reset(self):
        self.rankingTipsMc = None
        self.allRankingDataList = list()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PUBG_RANKING_SHOW_WIDGET:
            self.widget = widget
            self.refreshAll()

    @property
    def curPlayerRankId(self):
        p = BigWorld.player()
        curPlayerRankId = p.getRankLvInPUBGByRankPoint(p.pubgRankPoints)
        return curPlayerRankId

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PUBG_RANKING_SHOW_WIDGET)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PUBG_RANKING_SHOW_WIDGET)
        else:
            self.hide()

    def refreshAll(self):
        self.refreshData()
        self.refreshLeftUI()
        self.refreshRightMainContent()

    def refreshData(self):
        self.allRankingDataList = list()
        p = BigWorld.player()
        pubgRankIdList = PRPD.data.keys()
        pubgRankIdList.sort()
        for rankId in pubgRankIdList:
            rankShowData = self.getRankShowData(rankId, rankId == self.curPlayerRankId)
            self.allRankingDataList.append(rankShowData)

    def getRankShowData(self, rankId, isSelf = False):
        p = BigWorld.player()
        rankData = PRPD.data.get(rankId, {})
        tempRankData = dict()
        tempRankData['rankingName'] = rankData.get('des', '')
        isSelf and tempRankData['rankingName'] + gameStrings.PUBG_RANKING_SHOW_RANK_TIPS_CURRENT
        tempRankData['rankingIcon'] = rankData.get('rankingIconFrame', '')
        tempRankData['seasonRankingRewardHintTxt'] = rankData.get('seasonRankingRewardHint', '')
        tempRankData['getRankingRewardHintTxt'] = rankData.get('rankingRewardHint', '')
        tempRankData['RankingHintTxt'] = gameStrings.PUBG_RANKING_SHOW_RANK_POINT_TXT % (rankData.get('rank1', 0), rankData.get('rank2', 1))
        if rankData.get('rankMailId', None):
            if p.playerRankPointMarkData and rankId in p.playerRankPointMarkData:
                tempRankData['RankingRewardHintTxt'] = gameStrings.PUBG_RANKING_SHOW_REWARD_GET_HINT
            else:
                tempRankData['RankingRewardHintTxt'] = gameStrings.PUBG_RANKING_SHOW_REWARD_NO_GET_HINT
        else:
            tempRankData['RankingRewardHintTxt'] = ''
        return tempRankData

    def refreshLeftUI(self):
        p = BigWorld.player()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.gradingTxt.text = p.getCurRankNameInPUBG()
        self.widget.rankPointTxt.text = gameStrings.PUBG_PVP_MAIN_PROXY_RANK_POINT_TXT % p.pubgRankPoints
        self.widget.gameSeasonTxt.text = DCD.data.get('pubgGameSeasonTxt', '')
        self.widget.gameSeasonTimeTxt.text = DCD.data.get('pubgGameSeasonTimeTxt', '')
        addTipsMcList = [self.widget.leftRankingDataBg, self.widget.gradingTxt]
        for mc in addTipsMcList:
            TipManager.addTipByFunc(mc, self.rankingTipsLabelFunction, [self.getRankShowData(self.curPlayerRankId, True), mc, 'mouse'], False)

    def refreshRightMainContent(self):
        listMc = self.widget.mainContent
        listMc.itemRenderer = 'PUBGRankingShow_RankingItem'
        listMc.lableFunction = self.rankingItemLabelFunction
        listMc.column = 3
        listMc.itemWidth = 170
        listMc.itemHeight = 204
        listMc.dataArray = self.allRankingDataList
        listMc.validateNow()

    def rankingItemLabelFunction(self, *args):
        rankingItemData = ASObject(args[3][0])
        rankingItemMc = ASObject(args[3][1])
        TipManager.addTipByFunc(rankingItemMc, self.rankingTipsLabelFunction, [rankingItemData, rankingItemMc, 'upCenter'], False)
        rankingItemMc.rankingIcon.gotoAndStop(str(rankingItemData.rankingIcon))
        rankingItemMc.rankingName.text = rankingItemData.rankingName
        rankingItemMc.RankingHintTxt.text = rankingItemData.RankingHintTxt
        rankingItemMc.RankingRewardHintTxt.text = rankingItemData.RankingRewardHintTxt

    def rankingTipsLabelFunction(self, *args):
        rankingItemData = ASObject(args[3][0])[0]
        rankingItemMc = ASObject(args[3][0])[1]
        location = ASObject(args[3][0])[2]
        if not self.rankingTipsMc:
            self.rankingTipsMc = self.widget.getInstByClsName('PUBGRankingShow_RankingTips')
        TipManager.showImediateTip(rankingItemMc, self.rankingTipsMc, location)
        self.rankingTipsMc.rankingIcon.gotoAndStop(str(rankingItemData.rankingIcon))
        self.rankingTipsMc.rankingName.text = rankingItemData.rankingName
        self.rankingTipsMc.rankingNums.text = rankingItemData.RankingHintTxt
        if rankingItemData.seasonRankingRewardHintTxt == '':
            self.rankingTipsMc.seasonRankingRewardTitleTxt.visible = False
            self.rankingTipsMc.seasonRankingRewardHintTxt.visible = False
        else:
            self.rankingTipsMc.seasonRankingRewardTitleTxt.visible = True
            self.rankingTipsMc.seasonRankingRewardHintTxt.visible = True
            self.rankingTipsMc.seasonRankingRewardTitleTxt.text = gameStrings.PUBG_RANKING_SHOW_RANK_TIPS_SEASON_REWARD_TITLE
            self.rankingTipsMc.seasonRankingRewardHintTxt.text = rankingItemData.seasonRankingRewardHintTxt
        if rankingItemData.getRankingRewardHintTxt == '':
            self.rankingTipsMc.getRankingRewardTitleTxt.visible = False
            self.rankingTipsMc.getRankingRewardHintTxt.visible = False
        else:
            self.rankingTipsMc.getRankingRewardTitleTxt.visible = True
            self.rankingTipsMc.getRankingRewardHintTxt.visible = True
            self.rankingTipsMc.getRankingRewardTitleTxt.text = gameStrings.PUBG_RANKING_SHOW_RANK_TIPS_REWARD_TITLE
            self.rankingTipsMc.getRankingRewardHintTxt.text = rankingItemData.getRankingRewardHintTxt
        return self.rankingTipsMc
