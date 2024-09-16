#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yumufengScoreProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
import gameglobal
from guis import uiConst
from guis import uiUtils
from data import ymf_desc_data as YDD
from data import ymf_bonus_data as YBD
from data import sys_config_data as SCD

class YumufengScoreProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(YumufengScoreProxy, self).__init__(uiAdapter)
        self.modelMap = {'getReward': self.onGetReward}
        self.mediator = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_YUMUFENG_SCORE:
            self.mediator = mediator
            return self._getData()

    def show(self):
        if self.mediator:
            self.updateView()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YUMUFENG_SCORE)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YUMUFENG_SCORE)

    def onGetReward(self, *arg):
        BigWorld.player().cell.applyYmfScoreBonus()

    def _getData(self):
        ret = {}
        p = BigWorld.player()
        ymfScore = p.ymfScore.get(p.pvpTempCamp, 0)
        maxScore = SCD.data.get('ymfMaxScore', 100)
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
            data['isReached'] = scoreAwardData.has_key(awardId)
            data['isGotReward'] = scoreAwardData.has_key(awardId) and scoreAwardData[awardId]
            if not isEnableGetReward and data['isReached'] and not data['isGotReward']:
                isEnableGetReward = True
            awardData.append(data)

        conditionData = YDD.data
        conditionList = []
        for conditionId in conditionData:
            conditionList.append(conditionData.get(conditionId, {}).get('desc', gameStrings.TEXT_YMFSCOREV2PROXY_57))

        ret['awardData'] = awardData
        ret['conditionList'] = conditionList
        ret['currentScoreText'] = gameStrings.TEXT_YUMUFENGSCOREPROXY_74 % (ymfScore, maxScore)
        ret['currentScore'] = ymfScore
        ret['maxScore'] = maxScore
        ret['isEnableGetReward'] = isEnableGetReward
        return uiUtils.dict2GfxDict(ret, True)

    def updateView(self):
        ret = {}
        p = BigWorld.player()
        ymfScore = p.ymfScore.get(p.pvpTempCamp, 0)
        maxScore = SCD.data.get('ymfMaxScore', 100)
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
            data['isReached'] = scoreAwardData.has_key(awardId)
            data['isGotReward'] = scoreAwardData.has_key(awardId) and scoreAwardData[awardId]
            if not isEnableGetReward and data['isReached'] and not data['isGotReward']:
                isEnableGetReward = True
            awardData.append(data)

        ret['awardData'] = awardData
        ret['currentScoreText'] = gameStrings.TEXT_YUMUFENGSCOREPROXY_74 % (ymfScore, maxScore)
        ret['currentScore'] = ymfScore
        ret['maxScore'] = maxScore
        ret['isEnableGetReward'] = isEnableGetReward
        if self.mediator:
            self.mediator.Invoke('updateView', uiUtils.dict2GfxDict(ret, True))
