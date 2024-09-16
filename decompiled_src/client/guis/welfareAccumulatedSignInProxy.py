#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/welfareAccumulatedSignInProxy.o
import BigWorld
import gameglobal
import utils
import clientUtils
import time
import datetime
from Scaleform import GfxValue
from guis import uiUtils
from uiProxy import UIProxy
from ui import gbk2unicode
from gameStrings import gameStrings
from data import sys_config_data as SCD
from data import novice_checkin_reward_data as NCRD

class WelfareAccumulatedSignInProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WelfareAccumulatedSignInProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getInfo': self.onGetInfo,
         'getBonus': self.onGetBonus}
        self.panelMc = None

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]

    def onUnRegisterMc(self, *arg):
        self.panelMc = None

    def onGetBonus(self, *args):
        BigWorld.player().cell.applyNoviceCheckInReward()

    def onGetInfo(self, *arg):
        p = BigWorld.player()
        ret = {}
        idx = 1
        data = NCRD.data
        bonusInfos = []
        while data.get(idx, {}):
            bonusInfo = []
            itemInfos = clientUtils.genItemBonus(data.get(idx, {}).get('bonusId', 0))
            for itemInfo in itemInfos:
                bonusInfo.append(uiUtils.getGfxItemById(itemInfo[0], itemInfo[1]))

            bonusInfos.append(bonusInfo)
            idx += 1

        ret['bonusInfos'] = bonusInfos
        ret['noviceCheckInDays'] = SCD.data.get('noviceCheckInDays', 0)
        ret['enterWorldDays'] = utils.calcDaysAfterEnterWorld(p)
        ret['signedStates'] = []
        signedDays = self.getSignedDays()
        for i in xrange(0, ret['noviceCheckInDays']):
            dayCnt = i + 1
            ret['signedStates'].append(dayCnt <= signedDays)

        bgIdx = signedDays if signedDays else 1
        ret['welfareSignInBg'] = data.get(bgIdx, {}).get('welfareSignInBg', '')
        ret['welfareSignInTitle'] = SCD.data.get('welfareSignInTitle', '')
        ret['leftTime'] = self.getLeftTime()
        ret['hasSigned'] = not self.isHasReward()
        ret['signedDays'] = signedDays
        return uiUtils.dict2GfxDict(ret, True)

    def getSignedDays(self):
        signedDays = 0
        p = BigWorld.player()
        noviceCheckInAvaliableDays = SCD.data.get('noviceCheckInAvaliableDays', 0)
        for i in xrange(1, noviceCheckInAvaliableDays + 1):
            signedDays += p.noviceCheckInBM >> i & 1

        return signedDays

    def refreshPanel(self):
        if self.panelMc:
            self.panelMc.Invoke('initPanel')

    def getLeftTime(self):
        p = BigWorld.player()
        leftDays = self.getLeftDays()
        if leftDays < 0:
            return utils.formatTimeStr(0, gameStrings.ACCUMULATED_SIGN_IN__LEFT_TIME)
        leftSeconds = leftDays * 24 * 3600
        return utils.formatTimeStr(int(leftSeconds), gameStrings.ACCUMULATED_SIGN_IN__LEFT_TIME)

    def getLeftDays(self):
        p = BigWorld.player()
        nowStamp = utils.getNow()
        enterWorldDays = utils.calcDaysAfterEnterWorld(p)
        noviceCheckInAvaliableDays = SCD.data.get('noviceCheckInAvaliableDays', 0)
        leftDays = noviceCheckInAvaliableDays - enterWorldDays
        return leftDays

    def isTimeAvaliable(self):
        return self.getLeftDays() >= 0

    def isHasReward(self):
        p = BigWorld.player()
        enterWorldDays = utils.calcDaysAfterEnterWorld(p)
        noviceCheckInAvaliableDays = SCD.data.get('noviceCheckInAvaliableDays', 0)
        signedDays = self.getSignedDays()
        noviceCheckInDays = SCD.data.get('noviceCheckInDays', 0)
        return enterWorldDays <= noviceCheckInAvaliableDays and not p.noviceCheckInBM >> enterWorldDays & 1 and signedDays < noviceCheckInDays
