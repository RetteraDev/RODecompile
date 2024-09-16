#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ymfScoreV2Proxy.o
from gamestrings import gameStrings
import BigWorld
import uiConst
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import TipManager
MAX_PROGRESS_COUNT = 3
CONDITION_ITEM_HEIGHT = 20
from data import ymf_desc_data as YDD
from data import ymf_bonus_data as YBD
from data import sys_config_data as SCD
from data import guild_config_data as GCD

class YmfScoreV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(YmfScoreV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_YMF_SCORE_V2, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_YMF_SCORE_V2:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_YMF_SCORE_V2)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_YMF_SCORE_V2)

    def initUI(self):
        self.widget.expandBtn.visible = True
        self.widget.unExpandBtn.visible = False
        self.widget.expandBg.visible = False
        self.widget.unExpandBg.visible = True
        self.widget.list.visible = False
        self.widget.list.bg.alpha = 0.5
        self.widget.list.itemHeight = CONDITION_ITEM_HEIGHT
        self.widget.list.itemRenderer = 'YumufengScoreWi_YumufengScore_TextItem'
        self.widget.list.lableFunction = self.conditionItemFunction
        self.widget.list.dataArray = self.getConditinList()

    def getConditinList(self):
        conditionList = []
        for _, value in YDD.data.iteritems():
            conditionList.append(value.get('desc', gameStrings.TEXT_YMFSCOREV2PROXY_57))

        return conditionList

    def getData(self):
        ret = {}
        p = BigWorld.player()
        ymfScore = p.ymfScore.get(p.pvpTempCamp, 0)
        maxScore = SCD.data.get('ymfMaxScore', 100)
        showMaxScore = GCD.data.get('ymfShowMaxScore', 200)
        scoreAwardData = p.ymfScoreAward.get(p.pvpTempCamp, {})
        ymfData = YBD.data
        awardData = []
        isEnableGetReward = False
        for awardId in ymfData:
            data = {}
            data['title'] = ymfData.get(awardId, {}).get('title', gameStrings.TEXT_YMFSCOREV2PROXY_73)
            data['desc'] = ymfData.get(awardId, {}).get('desc', gameStrings.TEXT_YMFSCOREV2PROXY_74)
            data['score'] = ymfData.get(awardId, {}).get('score', 0)
            data['maxScore'] = maxScore
            data['showMaxScore'] = showMaxScore
            data['isReached'] = scoreAwardData.has_key(awardId)
            data['isGotReward'] = scoreAwardData.has_key(awardId) and scoreAwardData[awardId]
            if not isEnableGetReward and data['isReached'] and not data['isGotReward']:
                isEnableGetReward = True
            awardData.append(data)

        ret['awardData'] = awardData
        ret['currentScoreText'] = '%d/%d' % (ymfScore, maxScore)
        ret['currentScore'] = ymfScore
        ret['maxScore'] = maxScore
        ret['showMaxScore'] = showMaxScore
        ret['isEnableGetReward'] = isEnableGetReward
        return ret

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            data = self.getData()
            self.widget.getBtn.enabled = data['isEnableGetReward']
            awardList = data['awardData']
            for i in xrange(MAX_PROGRESS_COUNT):
                progressMc = getattr(self.widget, 'progress%d' % i)
                progressMc.visible = i < len(awardList)
                if progressMc.visible:
                    awardData = awardList[i]
                    showMaxScore = awardData['showMaxScore']
                    progressMc.x = self.widget.progressbar.x + int(min(showMaxScore, awardData['score']) * 1.0 / showMaxScore * self.widget.progressbar.width) - 15
                    progressMc.textField.text = awardData['title']
                    progressMc.gotoAndPlay('active' if awardData['isReached'] else 'dis')
                    TipManager.addTip(progressMc, awardData['desc'])
                else:
                    TipManager.removeTip(progressMc)

            self.widget.progressbar.currentValue = min(data['currentScore'], data['showMaxScore'])
            self.widget.progressbar.maxValue = data['showMaxScore']
            self.widget.score.htmlText = data['currentScoreText']
            self.widget.guildScore.text = str(p.guild.guildYMFScore if getattr(p, 'guild', None) else 0)
            TipManager.addTip(self.widget.progressbar, data['currentScoreText'])
            return

    def conditionItemFunction(self, *args):
        data = args[3][0].GetString()
        itemMc = ASObject(args[3][1])
        itemMc.textField.htmlText = ASObject(data)

    def _onGetBtnClick(self, *args):
        BigWorld.player().cell.applyYmfScoreBonus()

    def _onExpandBtnClick(self, *args):
        self.widget.expandBtn.visible = False
        self.widget.list.visible = True
        self.widget.unExpandBtn.visible = True
        self.widget.expandBg.visible = True
        self.widget.unExpandBg.visible = False

    def _onUnExpandBtnClick(self, *args):
        self.widget.expandBtn.visible = True
        self.widget.list.visible = False
        self.widget.unExpandBtn.visible = False
        self.widget.expandBg.visible = False
        self.widget.unExpandBg.visible = True

    def _onGuildRankBtnClick(self, *args):
        self.uiAdapter.yumufengGuildRank.getNewRankInfo()
        self.uiAdapter.yumufengGuildRank.show()
