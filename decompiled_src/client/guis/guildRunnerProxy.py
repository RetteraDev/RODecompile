#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildRunnerProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import utils
import gametypes
import gamescript
import commQuest
from uiProxy import UIProxy
from guis import uiUtils
from data import guild_run_man_data as GRMD
from data import guild_run_man_route_data as GRMRD
from data import bonus_data as BD
from cdata import quest_reward_data as QRD

class GuildRunnerProxy(UIProxy):

    def __init__(self, uiAdapter):
        self.EVERY_DAY_RUNNER = 1
        self.EVERY_WEEK_RUNNER = 2
        self.RUNNER_STATE_OPEN = 1
        self.RUNNER_STATE_CLOSE = 0
        super(GuildRunnerProxy, self).__init__(uiAdapter)
        self.runManType = 0
        self.startTime = 0
        self.mediator = None
        self.modelMap = {'updateBonus': self.onUpdateBonus}
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_RUNNER, self.hide)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator
        initData = self.getRunnerData()
        return uiUtils.dict2GfxDict(initData, True)

    def onUpdateBonus(self, *arg):
        index = int(arg[3][0].GetNumber())
        fixData = GRMRD.data.get((self.runManType, index), {})
        bonusData = self.getAllBonus(fixData)
        return uiUtils.dict2GfxDict(bonusData, True)

    def enableRunner(self):
        return gameglobal.rds.configData.get('enableGuildRunMan', False)

    def getRunnerData(self):
        p = BigWorld.player()
        runnerData = p.runMan[self.runManType]
        currNum = runnerData.currNum if runnerData.currNum > 0 else 1
        fixData = GRMRD.data.get((self.runManType, currNum), {})
        leftTime = self.startTime + fixData.get('time', 60) - utils.getNow()
        bonusData = self.getAllBonus(fixData)
        stepSeekIds = {}
        stepTips = {}
        for x, y in GRMRD.data:
            if x == self.runManType:
                stepSeekIds[y - 1] = GRMRD.data[x, y]['seekId']
                stepTips[y - 1] = gameStrings.TEXT_GUILDRUNNERPROXY_69 % y

        finishNum = 0
        for num in runnerData:
            if runnerData[num].passed and num > finishNum:
                finishNum = num

        data = {'leftTime': leftTime,
         'leftTimeStr': [gameStrings.TEXT_GUILDRUNNERPROXY_78, gameStrings.TEXT_FORMULA_1558],
         'rpValue': bonusData['rpValue'],
         'contribution': bonusData['contribution'],
         'experience': bonusData['experience'],
         'cash': bonusData['cash'],
         'bonusItem': bonusData['bonusItem'],
         'stepSum': len(stepTips),
         'currNum': currNum,
         'finishNum': finishNum,
         'stepSeekIds': stepSeekIds,
         'stepTips': stepTips}
        return data

    def getAllBonus(self, fixData):
        contribution = 0
        exp = 0
        cash = 0
        bonusItem = []
        rpValue = fixData.get('renpin', 0)
        rpLimit = rpValue * GRMD.data.get(self.runManType, {}).get('maxRewardPassNum', 20)
        bonusId = fixData.get('bonusId')
        if bonusId:
            fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', ())
            for bonusType, bonusItemId, bonusNum in fixedBonus:
                if bonusType == gametypes.BONUS_TYPE_GUILD_CONTRIBUTION:
                    contribution = bonusNum * BigWorld.player()._getGuildRunManRewardFactor(self.runManType)
                if bonusType == gametypes.BONUS_TYPE_ITEM:
                    bonusItem.append(uiUtils.getGfxItemById(bonusItemId, bonusNum))

        rewardId = fixData.get('rewardId')
        if rewardId:
            exp, cash = self.getAllReward(rewardId)
        data = {'rpValue': gameStrings.TEXT_GUILDRUNNERPROXY_115 % (rpValue, rpLimit),
         'bonusItem': bonusItem,
         'contribution': int(contribution),
         'experience': int(exp),
         'cash': int(cash)}
        return data

    def getAllReward(self, rewardId):
        factor = BigWorld.player()._getGuildRunManRewardFactor(self.runManType)
        rewardData = QRD.data.get(rewardId, None)
        if rewardData == None:
            return (0, 0)
        else:
            locals = {'flv': gamescript.FORMULA_FLV,
             'lv': BigWorld.player().lv,
             'slv': BigWorld.player().socLv,
             'questStar': 1,
             'grpCount': 1,
             'progress': 1}
            exp = commQuest._evaluateRewardData('expBonus', rewardData, locals) * factor
            cash = commQuest._evaluateRewardData('cashBonus', rewardData, locals) * factor
            return (exp, cash)

    def setType(self, type):
        self.runManType = type

    def setTime(self, time):
        self.startTime = time

    def show(self):
        if self.enableRunner():
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_RUNNER)

    def refreshView(self):
        if not self.enableRunner():
            return
        if self.mediator:
            self.mediator.Invoke('refresh', uiUtils.dict2GfxDict(self.getRunnerData(), True))

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_RUNNER)

    def reset(self):
        self.mediator = None
