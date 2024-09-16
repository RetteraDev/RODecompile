#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/balanceArena2PersonRewardProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from data import duel_config_data as DCD
from guis import uiUtils
from guis.asObject import ASObject
from gamestrings import gameStrings
ATTEND_REWARD = [[gameStrings.TEXT_BALANCEARENA2PERSONREWARDPROXY_13, (999, 1)],
 [gameStrings.TEXT_BALANCEARENA2PERSONREWARDPROXY_14, (999, 1), (999, 1)],
 [gameStrings.TEXT_BALANCEARENA2PERSONREWARDPROXY_14, (999, 1), (999, 1)],
 [gameStrings.TEXT_BALANCEARENA2PERSONREWARDPROXY_14, (999, 1), (999, 1)]]
RANK_REWARD = [[gameStrings.TEXT_BALANCEARENA2PERSONREWARDPROXY_19, (999, 1)],
 [gameStrings.TEXT_BALANCEARENA2PERSONREWARDPROXY_20, (999, 1), (999, 1)],
 [gameStrings.TEXT_BALANCEARENA2PERSONREWARDPROXY_21, (999, 1), (999, 1)],
 [gameStrings.TEXT_BALANCEARENA2PERSONREWARDPROXY_22, (999, 1), (999, 1)],
 [gameStrings.TEXT_BALANCEARENA2PERSONREWARDPROXY_23, (999, 1), (999, 1)]]
STATE16_REWARD = [[gameStrings.TEXT_BALANCEARENA2PERSONREWARDPROXY_26, (999, 1)],
 [gameStrings.TEXT_BALANCEARENA2PERSONREWARDPROXY_27, (999, 1), (999, 1)],
 [gameStrings.TEXT_BALANCEARENA2PERSONREWARDPROXY_28, (999, 1), (999, 1)],
 [gameStrings.TEXT_BALANCEARENA2PERSONREWARDPROXY_29, (999, 1), (999, 1)],
 [gameStrings.TEXT_BALANCEARENA2PERSONREWARDPROXY_30, (999, 1), (999, 1)]]
REWARD_SCORES = [(1, 100),
 (2, 1000),
 (2, 2000),
 (2, 5000)]

class BalanceArena2PersonRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BalanceArena2PersonRewardProxy, self).__init__(uiAdapter)
        self.widget = None
        self.todayScore = 0
        self.totalScore = 0
        self.scrollTo = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_BALANCE_ARENA_2PERSON_REWARD, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BALANCE_ARENA_2PERSON_REWARD:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BALANCE_ARENA_2PERSON_REWARD)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BALANCE_ARENA_2PERSON_REWARD)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.attendRewards.itemRenderer = 'BalanceArena2PersonReward_Item'
        self.widget.attendRewards.lableFunction = self.itemFunction
        self.initReward()
        self.initTips()
        self.queryServerInfo()

    def itemFunction(self, *args):
        attendRewards = DCD.data.get('DoubleArenaAttendReward', ATTEND_REWARD)
        reqireScores = DCD.data.get('DoubleArenaRewardScores', REWARD_SCORES)
        index = args[3][0].GetNumber()
        itemMc = ASObject(args[3][1])
        itemMc.isGet.visible = False
        rewardInfo = attendRewards[index]
        reqireInfo = reqireScores[index]
        itemMc.value.text = str(reqireScores[index][1])
        self.setRewardData(itemMc, rewardInfo)
        if reqireInfo[0] == 1:
            if self.todayScore >= reqireInfo[1]:
                itemMc.isGet.visible = True
            else:
                self.scrollTo = index
                itemMc.isGet.visible = False
        elif reqireInfo[0] == 2:
            if self.totalScore >= reqireInfo[1]:
                itemMc.isGet.visible = True
            else:
                self.scrollTo = index
                itemMc.isGet.visible = False

    def queryServerInfo(self):
        p = BigWorld.player()
        p.base.dArenaQueryFightScore()

    def initTips(self):
        tips = DCD.data.get('DoubleArenaRewardTips', [])
        for i in xrange(len(tips)):
            self.widget.getChildByName('tip%s' % str(i)).htmlText = tips[i]

    def initReward(self):
        rankReward = DCD.data.get('DoubleArenaRankReward', RANK_REWARD)
        for i in xrange(len(rankReward)):
            rewardMc = self.widget.getChildByName('reward1%s' % str(i + 1))
            rewardInfo = rankReward[i]
            self.setRewardData(rewardMc, rewardInfo)

        state16Reward = DCD.data.get('DoubleArenaState16Reward', STATE16_REWARD)
        for i in xrange(len(state16Reward)):
            rewardMc = self.widget.getChildByName('reward2%s' % str(i + 1))
            rewardInfo = state16Reward[i]
            self.setRewardData(rewardMc, rewardInfo)

    def setRewardData(self, rewardMc, rewardInfo):
        if not rewardMc or not rewardInfo:
            return
        rewardMc.info.text = rewardInfo[0]
        for j in xrange(2):
            slotMc = rewardMc.getChildByName('slot%s' % str(j))
            if len(rewardInfo) <= j + 1:
                slotMc.visible = False
            else:
                slotMc.visible = True
                rewardID = rewardInfo[j + 1][0]
                itemData = uiUtils.getGfxItemById(rewardID, rewardInfo[j + 1][1])
                slotMc.setItemSlotData(itemData)
                slotMc.dragable = False

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.todayScore = getattr(p, 'doubleArenatodayScore', 0)
        self.totalScore = getattr(p, 'doubleArenatotalScore', 0)
        self.refreshScore()
        self.refreshRewad()

    def refreshRewad(self):
        attendRewards = DCD.data.get('DoubleArenaAttendReward', ATTEND_REWARD)
        attendIndexs = range(len(attendRewards))
        self.widget.attendRewards.dataArray = attendIndexs
        self.widget.attendRewards.validateNow()
        self.widget.attendRewards.scrollTo(self.scrollTo)

    def refreshScore(self):
        self.widget.todayScore.text = gameStrings.DOUBLEARENA_TODAY_SCORE % str(self.todayScore)
        self.widget.totalScore.text = gameStrings.DOUBLEARENA_TOTAL_SCORE % str(self.totalScore)
