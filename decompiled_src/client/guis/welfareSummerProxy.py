#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/welfareSummerProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
from Scaleform import GfxValue
import utils
import clientUtils
import uiConst
from item import Item
from guis import uiUtils
from uiProxy import UIProxy
from ui import gbk2unicode
from data import activity_signin_bonus_data as ASBD
from data import activity_signin_type_data as ASTD
from data import sys_config_data as SCD
from cdata import activity_resignin_config_data as ARCD
from cdata import game_msg_def_data as GMDD

class WelfareSummerProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WelfareSummerProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getInfo': self.onGetInfo,
         'gainActivityBonus': self.onGainActivityBonus,
         'reSignInActivity': self.onReSignInActivity}
        self.panelMc = None
        self.activitySignId = 0
        self.signInEndDay = 0
        self.timer = None

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]

    def onUnRegisterMc(self, *arg):
        self.panelMc = None
        self.stopTimer()

    def onGetInfo(self, *args):
        signId = int(args[3][0].GetNumber())
        self.activitySignId = signId
        ret = self._getInfo()
        return uiUtils.dict2GfxDict(ret, True)

    def _getInfo(self):
        ret = {}
        self.initActivity(ret)
        ret['activitySignId'] = self.activitySignId
        self.stopTimer()
        self.updateTime()
        self.setTitle()
        return ret

    def initActivity(self, ret):
        if not self.activitySignId:
            return
        p = BigWorld.player()
        startDay = ASTD.data.get(self.activitySignId, {}).get('startDay', 20150801)
        activitySignInItemList = {}
        activityCnt = 0
        newSignInInfo = getattr(p, 'newSignInInfo', {})
        for key in ASBD.data:
            if key[0] == self.activitySignId:
                activitySignInItemList[key[1] - 1] = {}
                iconData = {}
                exactIconData = {}
                bonusId = ASBD.data[key].get('bonusId', 0)
                itemId = ASBD.data[key].get('displayItemId', 0)
                item = Item(itemId)
                iconData['iconPath'] = uiUtils.getItemIconFile64(item.id)
                iconData['count'] = clientUtils.genItemBonus(bonusId)[0][1]
                iconData['itemId'] = item.id
                activitySignInItemList[key[1] - 1]['isImportant'] = ASBD.data[key].get('isImportant', 0)
                exactBonusId = ASBD.data[key].get('exactDayBonus', 0)
                exactItemId = ASBD.data[key].get('exactDayDispalyItemId', 0)
                if exactBonusId and exactItemId:
                    exactIconData['iconPath'] = uiUtils.getItemIconFile64(exactItemId)
                    exactIconData['count'] = clientUtils.genItemBonus(exactBonusId)[0][1]
                    exactIconData['itemId'] = exactItemId
                    activitySignInItemList[key[1] - 1]['exactIconData'] = exactIconData
                activityCnt += 1
                activitySignInItemList[key[1] - 1]['iconData'] = iconData
                activitySignInItemList[key[1] - 1]['dayDesc'] = uiUtils._getDay(startDay, key[1] - 1)

        dates = getattr(newSignInInfo.get(self.activitySignId, {}), 'dates', [])
        for i in xrange(activityCnt):
            date = uiUtils._getDay(startDay, i)
            if date in dates:
                activitySignInItemList[i]['rewarded'] = True

        self.currDailyIndex = len(dates)
        self.signInEndDay = uiUtils._getDay(startDay, activityCnt - 1)
        activityDate = gameStrings.TEXT_WELFARESUMMERPROXY_105 + self.formatDate(startDay) + ' - ' + self.formatDate(self.signInEndDay)
        ret['currDailyIndex'] = self.currDailyIndex
        ret['startDay'] = startDay
        dayIndex = self._getDayIndex()
        ret['today'] = dayIndex
        ret['activityDate'] = activityDate
        ret['activitySignInItemList'] = activitySignInItemList
        ret['remainTime'] = 0
        resign = ARCD.data.get(self.activitySignId, {})
        MaxResignCnt = resign.get('reSignInCnt', 0)
        hasSignedToday = self.hasSignedToday()
        if hasSignedToday:
            notResignCnt = dayIndex + 1 - self.currDailyIndex
        else:
            notResignCnt = dayIndex - self.currDailyIndex
        if notResignCnt < 0:
            notResignCnt = 0
        resignCnt = getattr(newSignInInfo.get(self.activitySignId, {}), 'resignCnt', 0)
        self.canResignCnt = min(notResignCnt, MaxResignCnt - resignCnt)
        ret['enbaled'] = True
        if self.canResignCnt <= 0:
            self.canResignCnt = 0
            ret['enbaled'] = False
        ret['hasSignedToday'] = hasSignedToday
        ret['canResignCnt'] = self.canResignCnt
        ret['ResignDesc'] = gameStrings.TEXT_WELFARESUMMERPROXY_133 + str(notResignCnt) + gameStrings.TEXT_WELFARESUMMERPROXY_133_1 + gameStrings.TEXT_WELFARESUMMERPROXY_133_2 + str(self.canResignCnt) + gameStrings.TEXT_WELFARESUMMERPROXY_133_3
        ret['signInTitle'] = ASTD.data.get(self.activitySignId, {}).get('title', gameStrings.TEXT_WELFARESUMMERPROXY_134)

    def _checkShow(self):
        self.activitySignId = uiUtils.getActivitySignId()
        if not self.activitySignId:
            return False
        return True

    def hasSignedToday(self):
        if not self.activitySignId:
            return True
        else:
            newSignInInfo = getattr(BigWorld.player(), 'newSignInInfo', {}).get(self.activitySignId, None)
            if newSignInInfo:
                return newSignInInfo.hasSignedToday()
            return True

    def _getDayIndex(self):
        startDay = ASTD.data.get(self.activitySignId, {}).get('startDay', 0)
        if not startDay:
            return False
        dayIdx = utils.diffYearMonthDayInt(int(uiUtils.zonetime(utils.getNow(), SCD.data.get('curZone', '8'))), int(startDay))
        duration = ASTD.data.get(self.activitySignId, {}).get('duration', 7)
        dayIdx = max(0, dayIdx)
        dayIdx = min(dayIdx, duration - 1)
        return dayIdx

    def onGainActivityBonus(self, *args):
        BigWorld.player().cell.applySignInRewardV2(self.activitySignId)

    def onReSignInActivity(self, *args):
        gameglobal.rds.ui.activityReSignIn.show(self.canResignCnt)

    def notifyActivityAttendSignInMsg(self):
        if self.hasSignedToday():
            return
        if not self._checkShow():
            return
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_ACTIVITY_ATTEND_REWARD)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_ACTIVITY_ATTEND_REWARD, {'click': self.onPushMsgClick})

    def onPushMsgClick(self):
        if not self._checkShow():
            BigWorld.player().showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.TEXT_WELFAREMERGESERVERPROXY_178,))
            return
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_ACTIVITY_ATTEND_REWARD)
        gameglobal.rds.ui.welfare.show(uiConst.WELFARE_TAB_SUMMER)

    def formatDate(self, dateNum):
        dateNum = int(dateNum)
        dateStr = str(dateNum / 10000) + '.' + str(dateNum % 10000 / 100) + '.' + str(dateNum % 100)
        return dateStr

    def refreAvtivityPanel(self):
        if self.panelMc:
            ret = self._getInfo()
            self.panelMc.Invoke('refreAvtivityPanel', uiUtils.dict2GfxDict(ret, True))
        gameglobal.rds.ui.welfare.refreshInfo()

    def updateTime(self):
        endTime = self.formatDate(self.signInEndDay)
        endTimes = utils.getTimeSecondFromStr(endTime + '.23.59.59')
        leftTime = endTimes - utils.getNow()
        strTime = uiUtils.formatTime(leftTime)
        if leftTime < 0:
            gameglobal.rds.ui.welfare.refreshInfo()
            return
        if self.panelMc:
            self.panelMc.Invoke('setLeftTime', GfxValue(gbk2unicode(strTime)))
        self.timer = BigWorld.callback(1, self.updateTime)

    def setTitle(self):
        title = ASTD.data.get(self.activitySignId, {}).get('title', '')
        if self.panelMc:
            self.panelMc.Invoke('setTitle', GfxValue(gbk2unicode(title)))

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None
