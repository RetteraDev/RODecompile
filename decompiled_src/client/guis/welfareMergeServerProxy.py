#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/welfareMergeServerProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
from Scaleform import GfxValue
import utils
import gametypes
import clientUtils
from guis import uiUtils
from guis import uiConst
from uiProxy import UIProxy
from callbackHelper import Functor
from ui import gbk2unicode
from cdata import activity_achieve_score_bonus_data as AASBD
from data import bonus_data as BD
from data import activity_achieve_score_condition_data as AASCD
from data import activity_achieve_score_config_data as AASCFD
from cdata import game_msg_def_data as GMDD

class WelfareMergeServerProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WelfareMergeServerProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getInfo': self.onGetInfo,
         'gainAchieveBonus': self.onGainAchieveBonus}
        self.panelMc = None
        self.activityScoreId = 0
        self.scoreEndDay = 0
        self.timer = None

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]

    def onUnRegisterMc(self, *arg):
        self.panelMc = None
        self.stopTimer()

    def onGetInfo(self, *args):
        self.activityScoreId = uiUtils.getActivityScoreId()
        ret = self._getInfo()
        return uiUtils.dict2GfxDict(ret, True)

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def _getInfo(self):
        ret = {}
        self.initScore(ret)
        ret['activityScoreId'] = self.activityScoreId
        self.stopTimer()
        self.updateTime()
        return ret

    def initScore(self, ret):
        if not self.activityScoreId:
            return
        p = BigWorld.player()
        rewardedActivityTypes = p.rewardedActivityTypes
        keys = AASBD.data.keys()
        achieveScores = getattr(p, 'activityAchieveScore', {}).get(self.activityScoreId, {})
        totalScore = achieveScores.get('val', 0)
        awardList = {}
        for key in keys:
            if key[0] != self.activityScoreId:
                continue
            itemDict = {}
            iconData = {}
            if AASBD.data[key].get('score', 0) <= totalScore:
                if key in rewardedActivityTypes:
                    itemDict['rewarded'] = True
                else:
                    itemDict['rewarded'] = False
            itemDict['score'] = AASBD.data.get(key, {}).get('score', 0)
            bonusId = AASBD.data[key].get('bonusId', 0)
            fixedBonus = BD.data[bonusId].get('fixedBonus', ())
            fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
            if fixedBonus:
                itemId = fixedBonus[0][1]
            else:
                continue
            iconData['iconPath'] = uiUtils.getItemIconFile64(itemId)
            iconData['count'] = clientUtils.genItemBonus(bonusId)[0][1]
            iconData['itemId'] = itemId
            itemDict['iconData'] = iconData
            awardList[key[1] - 1] = itemDict

        ret['awardList'] = awardList
        ret['awardLength'] = len(awardList)
        achievementItem = []
        keys = AASCD.data.keys()
        finishedAchievementItems = getattr(p, 'activityAchieveScore', {}).get(self.activityScoreId, {}).get('finished', [])
        for key in keys:
            if key[0] != self.activityScoreId:
                continue
            obj = {}
            obj['score'] = gameStrings.TEXT_WELFAREMERGESERVERPROXY_108 + str(AASCD.data[key].get('score', 0))
            obj['detail'] = ''
            obj['detailContent'] = AASCD.data[key].get('desc', '')
            obj['achieveId'] = key[2]
            index = AASCD.data[key].get('sortId', 0)
            obj['sortId'] = index
            if (uiConst.ACTIVITY_CONDITION_TYPE, key[2]) in finishedAchievementItems:
                obj['status'] = 1
            else:
                obj['status'] = 0
            achievementItem.append(obj)

        achievementItem = sorted(achievementItem, key=lambda d: d['sortId'])
        achievementItem = sorted(achievementItem, key=lambda d: d['status'])
        ret['achievementItem'] = achievementItem
        ret['achievementScore'] = gameStrings.TEXT_WELFAREMERGESERVERPROXY_122 + str(totalScore)
        progress = self._getProgressBar()
        ret['progressBar'] = progress[0]
        ret['maxScore'] = progress[1]
        ret['ProgressScore'] = '%d/%d' % (totalScore, progress[1])
        activityScoreConfigData = AASCFD.data.get(self.activityScoreId, {})
        self.scoreEndDay = uiUtils._getDay(activityScoreConfigData.get('startDay', 0), activityScoreConfigData.get('duration', 0) - 1)
        endTime = self.formatDate(self.scoreEndDay)
        ret['endTime'] = gameStrings.TEXT_WELFAREMERGESERVERPROXY_130 + endTime
        ret['scoreTitle'] = activityScoreConfigData.get('topic', gameStrings.TEXT_WELFAREMERGESERVERPROXY_131)

    def refreScorePanel(self):
        if self.panelMc:
            ret = self._getInfo()
            self.panelMc.Invoke('refreScorePanel', uiUtils.dict2GfxDict(ret, True))
        gameglobal.rds.ui.welfare.refreshInfo()

    def _getProgressBar(self):
        progressbar = []
        awardData = AASBD.data
        achieveScores = getattr(BigWorld.player(), 'activityAchieveScore', {}).get(self.activityScoreId, {})
        currentScore = achieveScores.get('val', 0)
        temp = []
        for key in awardData:
            if key[0] != self.activityScoreId:
                continue
            data = {}
            needScore = awardData[key].get('score', 0)
            data['needScore'] = needScore
            temp.append(data)

        temp = sorted(temp, key=lambda d: d['needScore'])
        maxScore = 0
        lastMaxScore = 0
        for key in temp:
            data = {}
            needScore = key['needScore']
            data['needScore'] = needScore
            data['currentScore'] = needScore if currentScore >= needScore else currentScore - lastMaxScore
            maxScore = needScore
            lastMaxScore = needScore
            progressbar.append(data)

        return (progressbar, maxScore)

    def notifyActivityScorePushMsg(self):
        if not self._checkShow():
            return
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_ACTIVITY_SCORE_REWARD)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_ACTIVITY_SCORE_REWARD, {'click': self.show})

    def show(self):
        if not self._checkShow():
            BigWorld.player().showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.TEXT_WELFAREMERGESERVERPROXY_178,))
            return
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_ACTIVITY_SCORE_REWARD)
        gameglobal.rds.ui.welfare.show(uiConst.WELFARE_TAB_MERGE_SERVER)

    def formatDate(self, dateNum):
        dateNum = int(dateNum)
        dateStr = str(dateNum / 10000) + '.' + str(dateNum % 10000 / 100) + '.' + str(dateNum % 100)
        return dateStr

    def onGainAchieveBonus(self, *args):
        BigWorld.player().cell.applyActivityAchieveScoreReward(self.activityScoreId)

    def _checkShow(self):
        self.activityScoreId = uiUtils.getActivityScoreId()
        if not self.activityScoreId:
            return False
        return True

    def updateTime(self):
        endTime = self.formatDate(self.scoreEndDay)
        endTimes = utils.getTimeSecondFromStr(endTime + '.23.59.59')
        leftTime = endTimes - utils.getNow()
        strTime = uiUtils.formatTime(leftTime)
        if leftTime < 0:
            gameglobal.rds.ui.welfare.refreshInfo()
            return
        if self.panelMc:
            self.panelMc.Invoke('setLeftTime', GfxValue(gbk2unicode(strTime)))
        self.timer = BigWorld.callback(1, self.updateTime)
