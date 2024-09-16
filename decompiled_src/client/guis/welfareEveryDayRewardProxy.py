#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/welfareEveryDayRewardProxy.o
import BigWorld
import gameglobal
import uiUtils
import utils
import time
import gametypes
from uiProxy import UIProxy
from gameStrings import gameStrings
from data import item_data as ID
from data import sign_in_data as SID
from data import sign_in_config_data as SICD
from cdata import game_msg_def_data as GMDD

class WelfareEveryDayRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WelfareEveryDayRewardProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getShowInfo': self.onGetShowInfo,
         'retroactiveSign': self.onRetroactiveSign,
         'attendSign': self.onAttendSign}
        self.panelMc = None
        self.now = 0

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]

    def onUnRegisterMc(self, *arg):
        self.panelMc = None

    def onGetShowInfo(self, *arg):
        ret = {}
        mDateInfo = self.getDateInfo()
        ret['dateInfo'] = mDateInfo
        mAttendInfo = self.getAttendInfo()
        ret['attendInfo'] = mAttendInfo
        ret['bonusInfo'] = self.getBonusInfo(2 if mDateInfo['month'] % 2 == 0 else 1)
        missCnt = mDateInfo['signDay'] - mAttendInfo['attendCnt']
        if mAttendInfo['attToday'] < 1:
            missCnt -= 1
        ret['retroactiveBtnEnabled'] = missCnt > 0
        textInfo = {}
        textInfo['totalSignText'] = gameStrings.WELFARE_EVERYDAYREWARD_TOTALSIGNTEXT % mAttendInfo['attendCnt']
        textInfo['leaveSignText'] = gameStrings.WELFARE_EVERYDAYREWARD_LEAVESIGNTEXT % missCnt
        textInfo['dateText'] = '%d/%d/%d' % (mDateInfo['year'], mDateInfo['month'], mDateInfo['day'])
        ret['textInfo'] = textInfo
        return uiUtils.dict2GfxDict(ret, True)

    def onRetroactiveSign(self, *arg):
        reSignInType = SICD.data.get('reSignInType', gametypes.RE_SIGN_TYPE_LOGIN_TIME)
        reSignInItemId = SICD.data.get('reSignInItemId', 0)
        if reSignInType == gametypes.RE_SIGN_TYPE_CONSUME_ITEM and reSignInItemId:
            reSignInItemCnt = SICD.data.get('reSignInItemCnt', 1)
            itemName = ID.data.get(reSignInItemId, {}).get('name', '')
            ownCnt = BigWorld.player().inv.countItemInPages(int(reSignInItemId), enableParentCheck=True)
            cntStr = uiUtils.convertNumStr(ownCnt, reSignInItemCnt)
            itemData = uiUtils.getGfxItemById(reSignInItemId, cntStr)
            msg = uiUtils.getTextFromGMD(GMDD.data.RE_SIGN_IN_CONSUME_ITEM_NOTITY, '%d %s') % (reSignInItemCnt, itemName)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self._doResignIn, itemData=itemData)
        else:
            self._doResignIn()

    def _doResignIn(self):
        BigWorld.player().cell.applyReSignInReward()

    def onAttendSign(self, *arg):
        BigWorld.player().cell.applySignInReward()

    def refresh(self):
        if self.panelMc:
            self.panelMc.Invoke('refreshDisplay')
        gameglobal.rds.ui.welfare.refreshInfo()

    def getDateInfo(self):
        ret = {}
        timestamp = utils.getNow()
        self.now = self.now if self.now > timestamp else timestamp
        timeInfo = time.localtime(self.now)
        osTimeInfo = time.localtime(utils.getServerOpenTime())
        ret['year'] = timeInfo.tm_year
        ret['month'] = timeInfo.tm_mon
        ret['day'] = timeInfo.tm_mday
        ret['monthrange'] = self.__monthrange(timeInfo.tm_year, timeInfo.tm_mon)
        ret['firstMonth'] = timeInfo.tm_year == osTimeInfo.tm_year and timeInfo.tm_mon == osTimeInfo.tm_mon
        ret['osYear'] = osTimeInfo.tm_year
        ret['osMonth'] = osTimeInfo.tm_mon
        ret['osDay'] = osTimeInfo.tm_mday
        if ret['firstMonth']:
            ret['monthrange'] -= osTimeInfo.tm_mday - 1
            ret['signDay'] = ret['day'] - osTimeInfo.tm_mday + 1
        else:
            ret['signDay'] = ret['day']
        return ret

    def getAttendInfo(self):
        ret = {}
        p = BigWorld.player()
        ret['attendCnt'] = p.signInCnt
        ret['attToday'] = p.signInApplied
        ret['reSignable'] = SICD.data.get('reSignInCnt', 0) - p.reSignInCnt > 0
        ret['reSignInCnt'] = SICD.data.get('reSignInCnt', 0)
        return ret

    def getBonusInfo(self, monthIdx):
        ret = {}
        for day in range(1, 32):
            signIn = SID.data.get((monthIdx, day), {})
            displayInfo = uiUtils.getGfxItemById(signIn.get('displayItemId', 0), signIn.get('displayItemNum', 0))
            displayInfo['isImportant'] = signIn.get('isImportant', 0)
            ret[day] = displayInfo

        return ret

    def __monthrange(self, year, month):
        """Return number of days (28-31) for year, month."""
        if not 1 <= month <= 12:
            return 0
        mdays = [0,
         31,
         28,
         31,
         30,
         31,
         30,
         31,
         31,
         30,
         31,
         30,
         31]
        return mdays[month] + (month == 2 and self.__isleap(year))

    def __isleap(self, year):
        """Return True for leap years, False for non-leap years."""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
