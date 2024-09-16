#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/welfareFudanRewardProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import utils
import uiConst
import clientUtils
from callbackHelper import Functor
from crontab import CronTab
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import login_time_reward_data as LTRD

class WelfareFudanRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WelfareFudanRewardProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'applyFudan': self.onApplyFudan}
        self.panelMc = None
        self.timer = None
        self.callBackHandler = None
        self.actId = -1

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]
        self.actId = int(arg[3][1].GetNumber())
        self.refreshInfo()

    def onUnRegisterMc(self, *arg):
        self.panelMc = None
        self.stopTimer()
        self.cancelCB()
        self.actId = -1

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def refreshInfo(self):
        if self.panelMc:
            p = BigWorld.player()
            ret = {}
            fudanLevel = self.getFudanLevel()
            rewardInfo = self.getFudanRewardInfo()
            titleName = self.getFudanTitleName()
            ret = {'fudanLevel': fudanLevel,
             'rewardInfo': rewardInfo,
             'titleName': titleName}
            self.panelMc.Invoke('refreshInfo', uiUtils.dict2GfxDict(ret, True))
            self.stopTimer()
            self.updateTime()

    def updateTime(self):
        if self.panelMc:
            p = BigWorld.player()
            leftTime = 0
            startTime = LTRD.data.get(self.actId, {}).get('startTime', [None])[0]
            endTime = LTRD.data.get(self.actId, {}).get('endTime', [None])[0]
            if startTime and endTime and utils.inTimeTupleRange(startTime, endTime, weekSet=0):
                leftTime = int(utils.nextByTimeTuple(endTime, p.getServerTime(), weekSet=0))
                if leftTime < 0:
                    return
                timeHint = uiUtils.formatTime(leftTime)
                info = {'timeHint': timeHint}
                self.panelMc.Invoke('updateTime', uiUtils.dict2GfxDict(info, True))
                self.timer = BigWorld.callback(1, self.updateTime)
            else:
                gameglobal.rds.ui.welfare.hide()

    def cancelCB(self):
        if self.callBackHandler:
            BigWorld.cancelCallback(self.callBackHandler)
            self.callBackHandler = None

    def updateLevelInfo(self):
        p = BigWorld.player()
        fudanInfo = p.fudanDict.get(self.actId, [])
        rewardTime = 0
        if fudanInfo:
            rewardTime = fudanInfo[2] - utils.getNow()
        if self.callBackHandler:
            BigWorld.cancelCallback(self.callBackHandler)
        self.callBackHandler = BigWorld.callback(rewardTime, Functor(self.refreshInfo))

    def getFudanLevel(self):
        lv = self.calcFudanLevel(self.actId)
        return lv

    def getFudanRewardInfo(self):
        actId = self.actId
        ret = []
        p = BigWorld.player()
        curFudanLevel = self.calcFudanLevel(actId)
        readyItem, notFinishArr, finishArr = self._getFudanBonusData(actId, curFudanLevel)
        for item in readyItem:
            obj = {}
            bList = []
            obj['levelState'] = 1
            for b in item['bonus']:
                bList.append(uiUtils.getGfxItemById(b[0], b[1], appendInfo={'state': uiConst.ITEM_NORMAL}))

            obj['bonus'] = bList
            if p.fudanDict.get(actId, [0, False, 0])[2] - utils.getNow() < 0:
                obj['rewardTime'] = 0
            else:
                obj['rewardTime'] = p.fudanDict.get(actId, [0, False, 0])[2] - utils.getNow()
            obj['rewardDesc'] = LTRD.data.get(actId, {}).get('bonus', [])[item['lv']][2]
            obj['lv'] = item['lv']
            obj['btnState'] = item['btnState']
            ret.append(obj)

        for item in notFinishArr:
            obj = {}
            bList = []
            obj['levelState'] = 0
            for b in item['bonus']:
                bList.append(uiUtils.getGfxItemById(b[0], b[1], appendInfo={'state': uiConst.ITEM_NORMAL}))

            obj['bonus'] = bList
            if item['state'] == 'curLv':
                if p.fudanDict.get(actId, [0, False, 0])[2] - utils.getNow() < 0:
                    obj['rewardTime'] = 0
                else:
                    obj['rewardTime'] = p.fudanDict.get(actId, [0, False, 0])[2] - utils.getNow()
            else:
                obj['rewardTime'] = LTRD.data.get(actId, {}).get('bonus', [])[item['lv']][3] * 60
            obj['rewardDesc'] = LTRD.data.get(actId, {}).get('bonus', [])[item['lv']][2]
            obj['lv'] = item['lv']
            ret.append(obj)

        for item in finishArr:
            obj = {}
            bList = []
            obj['levelState'] = 2
            for b in item['bonus']:
                bList.append(uiUtils.getGfxItemById(b[0], b[1], appendInfo={'state': uiConst.ITEM_NORMAL}))

            obj['bonus'] = bList
            obj['rewardTime'] = 0
            obj['rewardDesc'] = LTRD.data.get(actId, {}).get('bonus', [])[item['lv']][2]
            obj['lv'] = item['lv']
            ret.append(obj)

        return ret

    def _getFudanBonusData(self, actId, curLv):
        ret = []
        finishArr = []
        notFinishArr = []
        readyItem = []
        p = BigWorld.player()
        fuDanRewardInfo = LTRD.data.get(actId, {}).get('bonus', [])
        i = 0
        for data in fuDanRewardInfo:
            obj = {}
            bonusId = data[1]
            items = clientUtils.genItemBonus(bonusId)
            arr = []
            for j in items:
                arr.append(j)

            obj['bonus'] = arr
            obj['lv'] = i
            if curLv == i:
                if p.fudanDict.get(actId, [0, False, 0])[1]:
                    obj['btnState'] = 1
                else:
                    obj['btnState'] = 0
                obj['state'] = 'curLv'
                readyItem.append(obj)
            elif curLv < i:
                obj['state'] = 'cannot'
                notFinishArr.append(obj)
            elif curLv > i:
                obj['state'] = 'finished'
                finishArr.append(obj)
            i += 1

        return (readyItem, notFinishArr, finishArr)

    def getFudanDesc(self):
        desc = LTRD.data.get(self.actId, {}).get('desc', gameStrings.TEXT_MONSTERCLANWARACTIVITYPROXY_348)
        return desc

    def getFudanTitleName(self):
        title = LTRD.data.get(self.actId, {}).get('title', gameStrings.TEXT_MONSTERCLANWARACTIVITYPROXY_348)
        return title

    def calcFudanLevel(self, actId):
        p = BigWorld.player()
        time, canApplyReward, goalTime = p.fudanDict.get(actId, [-1, False, 0])
        return p.calcFudanLevel(actId, time, canApplyReward)

    def isHasReward(self):
        p = BigWorld.player()
        for key in p.fudanDict.keys():
            if p.fudanDict[key][1]:
                return True

        return False

    def isHasRewardById(self, actId):
        p = BigWorld.player()
        if p.fudanDict.get(actId, [0])[1]:
            return True
        return False

    def onApplyFudan(self, *args):
        actId = int(args[3][0].GetNumber())
        p = BigWorld.player()
        p.base.applyLoginTimeReward(actId)
