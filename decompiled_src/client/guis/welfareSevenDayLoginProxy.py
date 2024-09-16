#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/welfareSevenDayLoginProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import utils
import uiConst
import clientUtils
from uiProxy import UIProxy
from gamestrings import gameStrings
from cdata import novice_signin_reward_data as NSRD

class WelfareSevenDayLoginProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WelfareSevenDayLoginProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'confirm': self.onConfirm}
        self.panelMc = None
        self.timer = None
        self.dayCnt = 0

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]
        self.refreshInfo(True)

    def onUnRegisterMc(self, *arg):
        self.panelMc = None
        self.stopTimer()

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def refreshInfo(self, firstOpen = False):
        if self.panelMc:
            p = BigWorld.player()
            info = {}
            self.dayCnt = int(utils.calcDaysAfterEnterWorld(p)) - 1
            info['dayCnt'] = self.dayCnt
            info['firstOpen'] = firstOpen
            bonusList = []
            for key in sorted(NSRD.data.keys()):
                bonusId = NSRD.data.get(key, {}).get('bonusId', 0)
                bonus = clientUtils.genItemBonus(bonusId)
                bonusInfo = {}
                bonusInfo['mainBonus'] = bonus[0]
                bonusInfo['extendBonus'] = bonus
                bonusList.append(bonusInfo)

            rewardList = []
            i = 0
            for bonus in bonusList:
                rewardInfo = {}
                rewardInfo['hasSignIn'] = bool(1 << i + 1 & p.noviceSignInBM)
                if i < self.dayCnt and not rewardInfo['hasSignIn']:
                    rewardInfo['mainBonus'] = uiUtils.getGfxItemById(bonus['mainBonus'][0], bonus['mainBonus'][1], appendInfo={'state': uiConst.ITEM_GRAY})
                else:
                    rewardInfo['mainBonus'] = uiUtils.getGfxItemById(bonus['mainBonus'][0], bonus['mainBonus'][1], appendInfo={'state': uiConst.ITEM_NORMAL})
                tBonusArray = []
                for eBonus in bonus['extendBonus']:
                    tBonusArray.append(uiUtils.getGfxItemById(eBonus[0], eBonus[1]))

                rewardInfo['extendBonus'] = tBonusArray
                rewardList.append(rewardInfo)
                i += 1

            info['rewardList'] = rewardList
            info['loginScuuLabelList'] = [gameStrings.TEXT_WELFARESEVENDAYLOGINPROXY_78,
             gameStrings.TEXT_WELFARESEVENDAYLOGINPROXY_78_1,
             gameStrings.TEXT_WELFARESEVENDAYLOGINPROXY_78_2,
             gameStrings.TEXT_WELFARESEVENDAYLOGINPROXY_78_3,
             gameStrings.TEXT_WELFARESEVENDAYLOGINPROXY_78_4,
             gameStrings.TEXT_WELFARESEVENDAYLOGINPROXY_78_5,
             gameStrings.TEXT_WELFARESEVENDAYLOGINPROXY_78_6]
            self.panelMc.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
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

    def onConfirm(self, *arg):
        dayCnt = int(arg[3][0].GetNumber()) + 1
        BigWorld.player().cell.applyNoviceSigninReward(dayCnt)

    def applyRewardSucc(self):
        gameglobal.rds.ui.welfare.refreshInfo()
        self.refreshInfo()
