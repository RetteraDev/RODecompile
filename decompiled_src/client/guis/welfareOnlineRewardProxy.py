#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/welfareOnlineRewardProxy.o
import BigWorld
import gameglobal
import uiUtils
import utils
import uiConst
import clientUtils
from callbackHelper import Functor
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import novice_logon_reward_data as NLRD

class WelfareOnlineRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WelfareOnlineRewardProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getOnlineReward': self.onGetOnlineReward}
        self.panelMc = None
        self.onlineLevelOver = {-1: 0}
        self.timer = None
        self.callBackHandler = None
        self.dayCnt = 0

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]
        self.currentLevelOver()
        self.refreshInfo()

    def onUnRegisterMc(self, *arg):
        self.panelMc = None
        self.onlineLevelOver = {-1: 0}
        self.stopTimer()
        self.cancelCB()

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def cancelCB(self):
        if self.callBackHandler:
            BigWorld.cancelCallback(self.callBackHandler)
            self.callBackHandler = None

    def refreshInfo(self):
        if self.panelMc:
            p = BigWorld.player()
            ret = {}
            self.dayCnt = int(utils.calcDaysAfterEnterWorld(p)) - 1
            onlineLevel = self.getOnlineLevel()
            rewardInfo = self.getOnlineRewardInfo()
            ret = {'onlineLevel': onlineLevel,
             'rewardInfo': rewardInfo}
            self.panelMc.Invoke('refreshInfo', uiUtils.dict2GfxDict(ret, True))
            self.stopTimer()
            self.updateTime()

    def updateTime(self):
        if self.panelMc:
            p = BigWorld.player()
            dayCnt = int(utils.calcDaysAfterEnterWorld(p)) - 1
            if self.dayCnt != dayCnt:
                gameglobal.rds.ui.welfare.refreshInfo()
                self.refreshInfo()
                return
            nowDaySec = utils.getServerDaySecond(utils.getNow(), True)
            leftTime = (uiConst.DAILY_SIGNIN_MAX_DAY - dayCnt) * uiConst.ONE_DAT_TIME - (utils.getNow() - nowDaySec)
            if nowDaySec == utils.getNow():
                leftTime -= uiConst.ONE_DAT_TIME
            if leftTime < 0:
                return
            timeHint = uiUtils.formatTime(leftTime)
            info = {'timeHint': timeHint}
            self.panelMc.Invoke('updateTime', uiUtils.dict2GfxDict(info, True))
            self.timer = BigWorld.callback(1, self.updateTime)

    def getOnlineLevel(self):
        p = BigWorld.player()
        currentOnlineLevel = p.noviceDailyOnline.phase - 1
        if currentOnlineLevel >= uiConst.DAILY_SIGNIN_LEVEL:
            currentOnlineLevel = uiConst.DAILY_SIGNIN_LEVEL - 1
        return currentOnlineLevel

    def getIsComplete(self):
        p = BigWorld.player()
        currentOnlineLevel = p.noviceDailyOnline.phase - 1
        if currentOnlineLevel >= uiConst.DAILY_SIGNIN_LEVEL:
            return True
        return False

    def getOnlineRewardInfo(self):
        ret = []
        p = BigWorld.player()
        onlineRewardInfo = self._getOnlineRewardData()
        bonusData = self._getOnlineBonusData(onlineRewardInfo)
        currentOnlineLevel = p.noviceDailyOnline.phase - 1
        i = 0
        for info in bonusData:
            obj = {}
            bList = []
            if i < currentOnlineLevel:
                obj['levelState'] = 2
                for b in bonusData[i]['bonus']:
                    bList.append(uiUtils.getGfxItemById(b, appendInfo={'state': uiConst.ITEM_NORMAL}))

                obj['bonus'] = bList
                obj['rewardTime'] = 0
            elif i == currentOnlineLevel:
                obj['levelState'] = 1
                for b in bonusData[i]['bonus']:
                    bList.append(uiUtils.getGfxItemById(b, appendInfo={'state': uiConst.ITEM_NORMAL}))

                obj['bonus'] = bList
                rewardTime = onlineRewardInfo[i]['rewardTime'] - p.noviceDailyOnline.getLogonTime()
                if rewardTime < 0:
                    obj['rewardTime'] = 0
                else:
                    obj['rewardTime'] = rewardTime
            else:
                obj['levelState'] = 0
                for b in bonusData[i]['bonus']:
                    bList.append(uiUtils.getGfxItemById(b, appendInfo={'state': uiConst.ITEM_NORMAL}))

                obj['bonus'] = bList
                obj['rewardTime'] = onlineRewardInfo[i]['rewardTime']
            if self.onlineLevelOver.get(i):
                obj['btnState'] = (i, 1)
            else:
                obj['btnState'] = (i, 0)
            obj['rewardDesc'] = onlineRewardInfo[i]['rewardDesc']
            i += 1
            ret.append(obj)

        return ret

    def _getOnlineRewardData(self):
        ret = []
        p = BigWorld.player()
        dayCnt = int(utils.calcDaysAfterEnterWorld(p))
        i = 1
        while i <= uiConst.DAILY_SIGNIN_LEVEL:
            obj = {}
            obj['rewardDesc'] = NLRD.data.get((dayCnt, i), {}).get('rewardDesc', '')
            obj['rewardTime'] = NLRD.data.get((dayCnt, i), {}).get('requireTime', 0)
            obj['bonusId'] = NLRD.data.get((dayCnt, i), {}).get('bonusId', 0)
            ret.append(obj)
            i += 1

        return ret

    def _getOnlineBonusData(self, onlineRewardInfo):
        ret = []
        for data in onlineRewardInfo:
            obj = {}
            bonusId = data.get('bonusId', 0)
            items = clientUtils.genItemBonus(bonusId)
            arr = []
            for i in items:
                arr.append(i[0])

            obj['bonus'] = arr
            ret.append(obj)

        return ret

    def currentLevelOver(self):
        self.onlineLevelOver = {-1: 0}
        rewardTime = self.getCurrentRewardTime()
        if self.callBackHandler:
            BigWorld.cancelCallback(self.callBackHandler)
        self.callBackHandler = BigWorld.callback(rewardTime, Functor(self.setLevelOver))

    def setLevelOver(self):
        p = BigWorld.player()
        if not p or not p.inWorld:
            return
        currentOnlineLevel = p.noviceDailyOnline.phase - 1
        self.onlineLevelOver = {currentOnlineLevel: 1}
        gameglobal.rds.ui.welfare.refreshInfo()
        self.refreshInfo()

    def getCurrentRewardTime(self):
        ret = 0
        p = BigWorld.player()
        currentOnlineLevel = self.getOnlineLevel()
        onlineRewardInfo = self._getOnlineRewardData()
        rewardTime = onlineRewardInfo[currentOnlineLevel]['rewardTime'] - p.noviceDailyOnline.getLogonTime()
        if rewardTime < 0:
            ret = 0
        else:
            ret = rewardTime
        return ret

    def applyRewardSucc(self):
        gameglobal.rds.ui.welfare.refreshInfo()
        self.currentLevelOver()
        self.refreshInfo()

    def onGetOnlineReward(self, *args):
        p = BigWorld.player()
        level = int(args[3][0].GetNumber()) + 1
        p.cell.applyNoviceOnlineReward(level)

    def isHasReward(self):
        return self.getCurrentRewardTime() == 0
