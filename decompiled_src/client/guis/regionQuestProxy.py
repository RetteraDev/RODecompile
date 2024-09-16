#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/regionQuestProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import const
import commQuest
from guis import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from data import fame_data as FD
from data import world_quest_data as WQD
from data import world_area_state_data as WASD
SUCCESS = 1
FAILED = 2
PROGRESS_TYPE_INCREASE = 1
PROGRESS_TYPE_DECREASE = 2

class RegionQuestProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RegionQuestProxy, self).__init__(uiAdapter)
        self.modelMap = {'getQuestInfo': self.onGetQuestInfo,
         'closePanel': self.onClosePanel,
         'autoFindPath': self.onAutoFindPath,
         'getStateInfo': self.onGetStateInfo}
        self.mediator = None
        self.stateMed = None
        self.questId = 0
        self.areaId = 0
        self.stateId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_REGION_QUEST, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_REGION_QUEST:
            self.mediator = mediator
        elif widgetId == uiConst.WIDGET_REGION_STATE:
            self.stateMed = mediator

    def show(self, questId):
        self.questId = questId
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_REGION_QUEST)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_REGION_QUEST)

    def _createRegionQuestInfo(self):
        p = BigWorld.player()
        ret = {}
        data = WQD.data.get(self.questId, {})
        region = data.get('areaName', '')
        if region:
            region = gameStrings.TEXT_TIANYUMALLPROXY_1486 + region + gameStrings.TEXT_ITEMQUESTPROXY_85_1
        name = data.get('name', '')
        additionalDesc = data.get('additionalDesc', '')
        shortDesc = data.get('shortDesc', '')
        desc = data.get('desc', '')
        stepDesc = data.get('rewardDesc', '')
        award = []
        exp, money, _, _ = commQuest.calcWAReward(p, self.questId)
        if exp > 0:
            award.append({'type': 'exp',
             'value': exp})
        if money > 0:
            award.append({'type': 'cash',
             'value': money})
        fame = data.get('compFame', [])
        for fameInfo in fame:
            fi = {}
            fi['type'] = 'fame'
            fi['value'] = fameInfo[1]
            fi['tip'] = FD.data.get(fameInfo[0], {}).get('name') if len(fameInfo) else ''
            if fi['value'] > 0:
                award.append(fi)

        items = []
        ret = {'region': region,
         'name': name,
         'additionalDesc': additionalDesc,
         'shortDesc': shortDesc,
         'desc': desc,
         'stepDesc': stepDesc,
         'award': award,
         'items': items}
        goals = []
        questVars = data.get('questVars', [])
        for questVar in questVars:
            num = p.getWorldQuestData(self.questId, const.WAQD_VARS, {}).get(questVar[0], 0)
            goalDesc = questVar[1]
            showType = questVar[2]
            addtion = questVar[3]
            showTypeContribute = questVar[4] if len(questVar) >= 5 else 0
            serverTime = p.getServerTime()
            if goalDesc.find('(%d/%d)') != -1:
                goalDesc = goalDesc % (num, int(addtion))
            goals.append([num,
             goalDesc,
             showType,
             addtion,
             serverTime,
             showTypeContribute])
            if showType == 1:
                tgtVarRange = data.get('tgtVarRange', ())
                for index, range in enumerate(tgtVarRange):
                    ret['stepMaxValue%s' % index] = range
                    val = p.getWorldQuestData(self.questId, const.WAQD_TGT_VAR, 0)
                    for i in xrange(index):
                        val -= tgtVarRange[i]

                    ret['stepCurrentValue%s' % index] = val

                rewardRate = data.get('rewardRate', ())
                for index, rate in enumerate(rewardRate):
                    ret['rewardRate%s' % index] = rate

        ret['goals'] = goals
        ret['awardLvNeed'] = data.get('thresholdLv', 0)
        ret['awardLvMatch'] = p.lv >= ret['awardLvNeed']
        return uiUtils.dict2GfxDict(ret, True)

    def refreshRegionQuestInfo(self):
        if self.mediator:
            self.mediator.Invoke('setQuestInfo', self._createRegionQuestInfo())

    def showState(self, state):
        self.stateId = state
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_REGION_STATE)

    def closeState(self):
        self.stateMed = None
        self.stateId = 0
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_REGION_STATE)

    def _createRegionStateInfo(self):
        p = BigWorld.player()
        ret = []
        data = WASD.data.get(self.stateId, {})
        questVars = data.get('questVars', [])
        for questVar in questVars:
            stateName = data.get('stateName', '')
            maxValue = int(questVar[3])
            currentValue = p.worldStateData.get(questVar[0], maxValue)
            showType = questVar[2]
            if showType == PROGRESS_TYPE_DECREASE:
                currentValue = int(maxValue - (p.getServerTime() - currentValue))
            tip = questVar[1]
            ret.append({'stateName': stateName,
             'maxValue': maxValue,
             'currentValue': currentValue,
             'showType': showType,
             'tip': tip})

        return uiUtils.array2GfxAarry(ret, True)

    def refreshRegionStateInfo(self):
        if self.stateMed:
            self.stateMed.Invoke('setStateInfo', self._createRegionStateInfo())

    def onGetQuestInfo(self, *arg):
        ret = self._createRegionQuestInfo()
        return ret

    def onClosePanel(self, *arg):
        self.hide()

    def onAutoFindPath(self, *arg):
        id = arg[3][0].GetString()
        uiUtils.findPosById(id)

    def onGetStateInfo(self, *arg):
        ret = self._createRegionStateInfo()
        return ret
