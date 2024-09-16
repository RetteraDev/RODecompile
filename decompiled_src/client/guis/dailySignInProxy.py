#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/dailySignInProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import utils
import time
import gametypes
import const
import clientUtils
from ui import gbk2unicode
from callbackHelper import Functor
from guis import ui
from guis import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from data import bonus_data as BD
from data import item_data as ID
from data import sign_in_data as SID
from cdata import font_config_data as FCD
from data import sign_in_config_data as SICD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from data import open_server_bonus_data as OSBD
from cdata import open_server_bonus_vp_data as OSBVD
from helpers import importantPlayRecommend as IPR
from data import vp_level_data as VLD
from cdata import novice_signin_reward_data as NSRD
from data import novice_logon_reward_data as NLRD
from data import login_time_reward_data as LTRD

class DailySignInProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DailySignInProxy, self).__init__(uiAdapter)
        self.modelMap = {'getDateInfo': self.onGetDateInfo,
         'getAttendInfo': self.onGetAttendInfo,
         'getShowInfo': self.onGetShowInfo,
         'retroactiveSign': self.onRetroactiveSign,
         'attendSign': self.onAttendSign,
         'enableServerBonus': self.onEnableServerBonus,
         'getServerBonusData': self.onGetServerBonusData,
         'gainServerBonus': self.onGainServerBonus,
         'getRecommendInfo': self.onGetRecommendInfo,
         'getSevenDayBonus': self.onGetSevenDayBonus,
         'sevenDayReward': self.onSevenDayReward,
         'getSignDay': self.onGetSignDay,
         'getOnlineRewardInfo': self.onGetOnlineRewardInfo,
         'getOnlineReward': self.onGetOnlineReward,
         'getTitleLabelDesc': self.onGetTitleLabelDesc,
         'getOnlineLevel': self.onGetOnlineLevel,
         'getRewardTime': self.onGetRewardTime,
         'iconClick': self.onIconClick,
         'getConfigTab': self.onGetConfigTab,
         'getFudanLevel': self.onGetFudanLevel,
         'getFudanRewardInfo': self.onGetFudanRewardInfo,
         'getFudanDesc': self.onGetFudanDesc,
         'getFudanTitleName': self.onGetFudanTitleName,
         'applyFudan': self.onApplyFudan}
        self.mediator = None
        self.mediatorIcon = None
        self.monthIdx = 1
        self.now = 0
        self.bonusTip = {}
        self.tabIndex = 0
        self.callBackHandler = None
        self.onlineLevelOver = {-1: 0}
        self.fudanIndex = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_DAILY_SIGNIN, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DAILY_SIGNIN:
            self.mediator = mediator
            self.currentLevelOver()
            self.refreshTabNotify()
            return GfxValue(self.tabIndex)
        if widgetId == uiConst.WIDGET_DAILY_SIGNIN_ICON:
            self.mediatorIcon = mediator
            ret = {}
            ret['rewardTime'] = self.getCurrentRewardTime()
            ret['level'] = 0
            p = BigWorld.player()
            currentOnlineLevel = p.noviceDailyOnline.phase - 1
            if currentOnlineLevel >= uiConst.DAILY_SIGNIN_LEVEL:
                ret['level'] = currentOnlineLevel
            return uiUtils.dict2GfxDict(ret)

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_DAILY_SIGNIN)

    def showIcon(self):
        if gameglobal.rds.configData.get('enableNoviceReward', False) and self.isShowIcon() and self.checkDailySignInStartTime() and not gameglobal.rds.configData.get('enableRewardGiftActivityIcons', False):
            self.uiAdapter.loadWidget(uiConst.WIDGET_DAILY_SIGNIN_ICON)
        else:
            self.hideIcon()

    def hideIcon(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_DAILY_SIGNIN_ICON)

    def refreshAll(self):
        self.currentLevelOver()
        self.refreshTabNotify()
        if self.isShowIcon():
            self.refreshIcon()
        else:
            self.hideIcon()
            self.setTab0()
        self.refreshPlane()

    def setTab0(self):
        if self.mediator:
            self.mediator.Invoke('setTabIndex', GfxValue(0))

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_DAILY_SIGNIN)

    def reset(self):
        self.mediator = None
        self.tabIndex = 0
        self.tabRet = []
        if self.callBackHandler:
            BigWorld.cancelCallback(self.callBackHandler)
            self.callBackHandler = None
        self.onlineLevelOver = {-1: 0}
        ui.set_cursor('arrow_normal', 'arrow_normal')

    def isShow(self):
        return self.show

    def refresh(self, now = None):
        if now is not None:
            self.now = now
        if self.mediator is not None:
            self.mediator.Invoke('refreshPlane', self.onGetDateInfo())
            gameglobal.rds.ui.topBar.onDailySignIn()
            self.refreshTabNotify()

    def refreshRecomm(self):
        if not self.mediator:
            return
        if not self._isEnabledServerBonus():
            return
        self.mediator.Invoke('refreshRecommendView')

    def __isleap(self, year):
        """Return True for leap years, False for non-leap years."""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

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

    def __getBonusInfo(self, fixedBonus, index, icon64 = False, forceIcon = False):
        bonusInfo = []
        idd = ID.data
        fcdd = FCD.data
        index = 0 if index >= len(fixedBonus) else index
        bonusType, bonusItemId, bonusNum = fixedBonus[index]
        bonusInfo.insert(0, bonusType)
        bonusInfo.insert(1, bonusNum)
        if bonusType == gametypes.BONUS_TYPE_ITEM or forceIcon:
            itemInfo = idd.get(bonusItemId, {})
            quality = itemInfo.get('quality', 1)
            color = fcdd.get(('item', quality), {}).get('qualitycolor', 'nothing')
            if icon64:
                bonusInfo.insert(2, uiUtils.getItemIconFile64(bonusItemId))
            else:
                bonusInfo.insert(2, uiUtils.getItemIconFile40(bonusItemId))
            bonusInfo.insert(3, itemInfo.get('name', '未知物品'))
            bonusInfo.insert(4, color)
            bonusInfo.insert(5, bonusItemId)
        return bonusInfo

    def __getBonusDisplayInfo(self, bonusItemId, icon64 = False):
        bonusInfo = []
        idd = ID.data
        fcdd = FCD.data
        bonusInfo.insert(0, 0)
        bonusInfo.insert(1, 1)
        itemInfo = idd.get(bonusItemId, {})
        quality = itemInfo.get('quality', 1)
        color = fcdd.get(('item', quality), {}).get('qualitycolor', 'nothing')
        if icon64:
            bonusInfo.insert(2, uiUtils.getItemIconFile64(bonusItemId))
        else:
            bonusInfo.insert(2, uiUtils.getItemIconFile40(bonusItemId))
        bonusInfo.insert(3, itemInfo.get('name', '未知物品'))
        bonusInfo.insert(4, color)
        bonusInfo.insert(5, bonusItemId)
        return bonusInfo

    def __tmpAttendTips(self, ret):
        nameMap = {gametypes.BONUS_TYPE_MONEY: '云券',
         gametypes.BONUS_TYPE_FAME: '声望',
         gametypes.BONUS_TYPE_EXP: '经验',
         gametypes.BONUS_TYPE_FISHING_EXP: '钓鱼经验',
         gametypes.BONUS_TYPE_SOC_EXP: '社会经验'}
        tipString = "<font size = \'14\' color = \'#f2ab0d\'>" + '签到物品' + '</font><br>'
        for i in range(0, ret['num']):
            if ret[i][0] == gametypes.BONUS_TYPE_ITEM:
                tipString += "<font size = \'12\'>" + '· ' + ret[i][3] + '×' + str(ret[i][1]) + '</font><br>'
            else:
                tipString += "<font size = \'12\'>" + '· ' + str(ret[i][1]) + '×' + nameMap.get(ret[i][0]) + '</font><br>'

        return GfxValue(gbk2unicode(tipString))

    def onCloseWidget(self, *arg):
        self.clearWidget()

    def onGetDateInfo(self, *arg):
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
        return uiUtils.dict2GfxDict(ret, True)

    def onGetAttendInfo(self, *arg):
        ret = {}
        p = BigWorld.player()
        timestamp = utils.getNow()
        self.now = self.now if self.now > timestamp else timestamp
        timeInfo = time.localtime(self.now)
        osTimeInfo = time.localtime(utils.getServerOpenTime())
        monthrange = self.__monthrange(timeInfo.tm_year, timeInfo.tm_mon)
        firstMonth = timeInfo.tm_year == osTimeInfo.tm_year and timeInfo.tm_mon == osTimeInfo.tm_mon
        if firstMonth:
            monthrange -= osTimeInfo.tm_mday - 1
        ret['attendCnt'] = p.signInCnt
        ret['attToday'] = p.signInApplied
        ret['reSignable'] = SICD.data.get('reSignInCnt', 0) - p.reSignInCnt > 0
        ret['reSignInCnt'] = SICD.data.get('reSignInCnt', 0)
        return uiUtils.dict2GfxDict(ret, True)

    def onGetShowInfo(self, *arg):
        ret = {}
        self.monthIdx = 1
        if arg[3][0] is not None:
            self.monthIdx = int(arg[3][0].GetNumber())
        sidd = SID.data
        for day in range(1, 32):
            signIn = sidd.get((self.monthIdx, day), {})
            showItemId = signIn.get('displayItemId', 0)
            displayInfo = self.__getBonusDisplayInfo(showItemId, True)
            displayInfo.append(signIn.get('isImportant', 0))
            displayInfo.append(signIn.get('displayItemNum', 0))
            ret[day] = displayInfo

        return uiUtils.dict2GfxDict(ret, True)

    def onGetToolTip(self, *arg):
        ret = {}
        slotIdx = 0
        if arg[3][0] is not None:
            key, slotIdx = arg[3][0].GetString().split('.')
        day = int(slotIdx) + 1
        sidd = SID.data
        bdd = BD.data
        signIn = sidd.get((self.monthIdx, day), {})
        bonusId = signIn.get('bonusId', 0)
        fixedBonus = bdd.get(bonusId, {}).get('fixedBonus', ())
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        for i in range(0, len(fixedBonus)):
            ret[i] = self.__getBonusInfo(fixedBonus, i)

        ret['num'] = len(fixedBonus)
        return self.__tmpAttendTips(ret)

    def onGetBonusItemTip(self, *arg):
        if arg[3][0] is not None:
            key, slotIdx = arg[3][0].GetString().split('.')
        slotIdx = int(slotIdx)
        if not self._checkBonusRewardEnable(slotIdx):
            tipStr = self.bonusTip[slotIdx]
        else:
            tipStr = self._getBonusTip(slotIdx)
        return GfxValue(gbk2unicode(tipStr))

    def _checkBonusRewardEnable(self, day):
        openDay = self._getOpenServerDay()
        if day <= openDay:
            return True
        return False

    def _getBonusTip(self, day):
        vpLv = self._getVpLv(day)
        itemInfo = self._getKnowItemInfo(day)
        tipStr = self.bonusTip[day]
        if itemInfo:
            hasVp = itemInfo[1]
            tip = itemInfo[0][2]
            vp = OSBVD.data.get((day, vpLv), {}).get('vp', 0)
            playerLv = BigWorld.player().lv
            vpDefaultLower = VLD.data.get(playerLv, {}).get('vpDefaultLower', 0)
            vpDefaultUpper = VLD.data.get(playerLv, {}).get('vpDefaultUpper', 0)
            exp = (vpDefaultLower + vpDefaultUpper) / 2 * vp
            tipStr = tip % (vp, exp) if hasVp else tip
        return tipStr

    def _getBonusItemId(self, day):
        itemId = 0
        itemInfo = self._getKnowItemInfo(day)
        if itemInfo:
            itemId = itemInfo[0][1]
        return itemId

    def _getKnowItemInfo(self, day):
        knowItem = OSBD.data.get(day, {}).get('knownItem', [])
        if len(knowItem) > 0:
            vpLv = self._getVpLv(day)
            lv1 = knowItem[0][0]
            lv2 = knowItem[1][0]
            lv3 = knowItem[2][0]
            if vpLv <= lv1:
                return [knowItem[0], True]
            elif vpLv > lv1 and vpLv <= lv2:
                return [knowItem[1], True]
            elif vpLv > lv2 and vpLv <= lv3:
                return [knowItem[2], False]
            else:
                return None

    def _getVpLv(self, day):
        vpLv = 0
        openServerBonus = BigWorld.player().openServerBonus
        if openServerBonus.has_key(day):
            bonusData = openServerBonus[day]
            vpLv = bonusData.vpLv
        return vpLv

    def onRetroactiveSign(self, *arg):
        reSignInType = SICD.data.get('reSignInType', gametypes.RE_SIGN_TYPE_LOGIN_TIME)
        reSignInItemId = SICD.data.get('reSignInItemId', 0)
        if reSignInType == gametypes.RE_SIGN_TYPE_CONSUME_ITEM and reSignInItemId:
            reSignInItemCnt = SICD.data.get('reSignInItemCnt', 1)
            itemName = ID.data.get(reSignInItemId, {}).get('name', '')
            ownCnt = BigWorld.player().inv.countItemInPages(int(reSignInItemId), enableParentCheck=True)
            cntStr = uiUtils.convertNumStr(ownCnt, reSignInItemCnt)
            itemData = uiUtils.getGfxItemById(reSignInItemId, cntStr)
            msg = GMD.data.get(GMDD.data.RE_SIGN_IN_CONSUME_ITEM_NOTITY, {}).get('text', '%d %s')
            msg = msg % (reSignInItemCnt, itemName)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self._doResignIn, itemData=itemData)
        else:
            self._doResignIn()

    def _doResignIn(self):
        BigWorld.player().cell.applyReSignInReward()

    def onAttendSign(self, *arg):
        BigWorld.player().cell.applySignInReward()
        self.refresh()

    def onEnableServerBonus(self, *arg):
        enabled = self._isEnabledServerBonus()
        return GfxValue(enabled)

    def _isEnabledServerBonus(self):
        enableNewServerSignInPanel = gameglobal.rds.configData.get('enableNewServerSignInPanel', False)
        enabled = gameglobal.rds.configData.get('enableOpenServerBonus', False)
        minLv = SCD.data.get('openServerBonusMinLv', 0)
        hasRewardedALL = self._getRewardedAll()
        isAvaliableLv = BigWorld.player().lv >= minLv
        return enabled and not hasRewardedALL and isAvaliableLv and not enableNewServerSignInPanel

    def _getRewardedAll(self):
        p = BigWorld.player()
        configData = OSBD.data
        data = p.openServerBonus if p.openServerBonus else {}
        for day in configData:
            if not data.has_key(day):
                return False
            if data.has_key(day):
                state = data[day].state
                if state == const.OPEN_SERVER_BONUS_STATE_READY:
                    return False
                if state == const.OPEN_SERVER_BONUS_STATE_WAITING:
                    return False

        return True

    def _getServerBonusData(self):
        p = BigWorld.player()
        configData = OSBD.data
        data = p.openServerBonus if p.openServerBonus else {}
        avaliableCount = 0
        now = utils.getNow()
        ret = {}
        openDays = self._getOpenServerDay()
        ret['desc'] = SCD.data.get('openServerBonusDesc', '活动已进行到第%d天') % min(30, openDays)
        ret['bonusItems'] = []
        isFirstWaiting = True
        for day in configData:
            obj = {}
            temp = configData.get(day, {})
            obj['day'] = day
            obj['showItem'] = uiUtils.getGfxItemById(temp.get('itemId', 0))
            obj['showItem'].pop('itemId')
            self.bonusTip[day] = temp.get('text', '奖励tips')
            obj['isImportant'] = temp.get('isImportant', 0)
            obj['countDown'] = 0
            if data.has_key(day):
                endTime = data[day].tEnd
                leftMin = endTime - now
                state = data[day].state
                obj['state'] = state
                if state == const.OPEN_SERVER_BONUS_STATE_READY:
                    avaliableCount += 1
                elif state == const.OPEN_SERVER_BONUS_STATE_WAITING:
                    if leftMin > 0 and isFirstWaiting:
                        obj['countDown'] = leftMin
                        isFirstWaiting = False
                    else:
                        obj['state'] = 0
                if self._checkBonusRewardEnable(day):
                    fixedItemId = self._getBonusItemId(day)
                    if fixedItemId != 0:
                        obj['showItem'] = uiUtils.getGfxItemById(fixedItemId)
                        obj['showItem'].pop('itemId')
            else:
                obj['state'] = 0
            ret['bonusItems'].append(obj)

        ret['count'] = avaliableCount
        return ret

    def onGetServerBonusData(self, *arg):
        ret = self._getServerBonusData()
        return uiUtils.dict2GfxDict(ret, True)

    def refreshServerBonus(self):
        ret = self._getServerBonusData()
        if self.mediator:
            self.mediator.Invoke('updateBonusView', uiUtils.dict2GfxDict(ret, True))

    def onGainServerBonus(self, *arg):
        BigWorld.player().cell.gainOpenServerBonus()

    def onGetRecommendInfo(self, *arg):
        ret = IPR.getRecommendInfo(BigWorld.player(), [1, 2])
        return uiUtils.dict2GfxDict(ret, True)

    def _getOpenServerDay(self):
        openDays = utils.getServerOpenDays() + 1
        return openDays

    def _hasReadyReward(self):
        p = BigWorld.player()
        data = p.openServerBonus if p.openServerBonus else {}
        for day in data:
            state = data[day].state
            if state == const.OPEN_SERVER_BONUS_STATE_READY:
                return True

        return False

    def notifyBonusPushMsg(self):
        if not self._isEnabledServerBonus():
            return
        if not self._hasReadyReward():
            return
        if gameglobal.rds.configData.get('enableWelfare', False):
            return
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_OPEN_SERVER_BONUS_PUSH, {'click': self.clickOpenServerBonus})
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_OPEN_SERVER_BONUS_PUSH)

    def clickOpenServerBonus(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_OPEN_SERVER_BONUS_PUSH)
        if self.mediator:
            self.mediator.Invoke('changeTabIndex', GfxValue(1))
        else:
            self.tabIndex = 1
            self.show()

    def notifyAttendPushMsg(self):
        if gameglobal.rds.configData.get('enableWelfare', False):
            return
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_DAILY_ATTEND_PUSH, {'click': self.clickOpenAttend})
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_DAILY_ATTEND_PUSH)

    def clickOpenAttend(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_DAILY_ATTEND_PUSH)
        if self.mediator:
            if gameglobal.rds.configData.get('enableOpenServerBonus', False):
                self.mediator.Invoke('changeTabIndex', GfxValue(0))
        else:
            self.tabIndex = 0
            self.show()

    def _getItemBouns(self):
        ret = []
        rewardDict = NSRD.data
        for key in sorted(rewardDict.keys()):
            obj = {}
            bonusId = rewardDict.get(key, 0).get('bonusId', 0)
            bonusIdList = clientUtils.genItemBonus(bonusId)
            arr = []
            for i in bonusIdList:
                arr.append(i)

            obj['extendBonus'] = arr
            obj['mainBonus'] = arr[0]
            ret.append(obj)

        return ret

    def onGetSevenDayBonus(self, *args):
        bonusData = []
        p = BigWorld.player()
        dayCnt = int(utils.calcDaysAfterEnterWorld(p)) - 1
        data = self._getItemBouns()
        i = 0
        for bonus in data:
            aBonus = {}
            aBonus['isSignIn'] = bool(1 << i + 1 & p.noviceSignInBM)
            if i < dayCnt and not aBonus['isSignIn']:
                aBonus['mainBonus'] = uiUtils.getGfxItemById(bonus['mainBonus'][0], bonus['mainBonus'][1], appendInfo={'state': uiConst.ITEM_GRAY})
            else:
                aBonus['mainBonus'] = uiUtils.getGfxItemById(bonus['mainBonus'][0], bonus['mainBonus'][1], appendInfo={'state': uiConst.ITEM_NORMAL})
            tBonusArray = []
            for eBonus in bonus['extendBonus']:
                tBonusArray.append(uiUtils.getGfxItemById(eBonus[0], eBonus[1]))

            aBonus['extendBonus'] = tBonusArray
            bonusData.append(aBonus)
            i += 1

        return uiUtils.array2GfxAarry(bonusData)

    def onSevenDayReward(self, *args):
        signInDay = int(args[3][0].GetNumber()) + 1
        p = BigWorld.player()
        p.cell.applyNoviceSigninReward(signInDay)

    def onGetSignDay(self, *args):
        p = BigWorld.player()
        dayCnt = int(utils.calcDaysAfterEnterWorld(p)) - 1
        return GfxValue(dayCnt)

    def refreshPlane(self):
        if self.mediator:
            self.mediator.Invoke('refreshPlane')

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

    def onGetOnlineRewardInfo(self, *args):
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

        return uiUtils.array2GfxAarry(ret, True)

    def onGetOnlineReward(self, *args):
        p = BigWorld.player()
        level = int(args[3][0].GetNumber()) + 1
        p.cell.applyNoviceOnlineReward(level)

    def onGetTitleLabelDesc(self, *args):
        p = BigWorld.player()
        dayCnt = int(utils.calcDaysAfterEnterWorld(p))
        ret = '活动时间 剩余%d天' % (SCD.data.get('dailySignInOnlineDay', 7) - dayCnt + 1)
        return GfxValue(gbk2unicode(ret))

    def initTab(self):
        ret = [1, 1, 1]
        p = BigWorld.player()
        dayCnt = int(utils.calcDaysAfterEnterWorld(p))
        if dayCnt > len(NLRD.data.items()) / uiConst.DAILY_SIGNIN_LEVEL or dayCnt < 0:
            ret[2] = 0
        else:
            ret[2] = 1
        if dayCnt > uiConst.DAILY_SIGNIN_MAX_DAY or dayCnt < 0:
            ret[1] = 0
        else:
            ret[1] = 1
        self.setTab(ret)
        return ret

    def onGetConfigTab(self, *args):
        fixedRet = [{'isShow': 1,
          'panel': 'DailySi_EveryDayRewardPanel',
          'name': '每日签到'}]
        p = BigWorld.player()
        dayCnt = int(utils.calcDaysAfterEnterWorld(p))
        if dayCnt > len(NLRD.data.items()) / uiConst.DAILY_SIGNIN_LEVEL or dayCnt < 0 or not self.checkDailySignInStartTime():
            pass
        else:
            tabItem = {'isShow': 1,
             'panel': 'DailySi_SevenDayRewardPanel',
             'name': '七日领奖'}
            fixedRet.append(tabItem)
        if dayCnt > uiConst.DAILY_SIGNIN_MAX_DAY or dayCnt < 0 or not self.checkDailySignInStartTime():
            pass
        else:
            tabItem = {'isShow': 1,
             'panel': 'DailySi_OnlineRewardPanel',
             'name': '在线奖励'}
            fixedRet.append(tabItem)
        self.fudanIndex = {}
        configRet = []
        if gameglobal.rds.configData.get('enableLoginReward', False):
            p = BigWorld.player()
            for key in p.fudanDict.keys():
                _level = self.calcFudanLevel(key)
                if not p.fudanIsNeedDisplay(key, p.fudanDict[key][0], p.fudanDict[key][1], _level):
                    continue
                configRetItem = {}
                _data = LTRD.data.get(key, {})
                if _data.get('bonus', []):
                    isShow = 1
                    panel = 'DailySignIn_FudanRewardPanel'
                    name = _data.get('title', '策划配置')
                    idData = {'actId': key}
                    configRetItem = {'isShow': isShow,
                     'panel': panel,
                     'name': name,
                     'data': idData}
                configRet.append(configRetItem)
                self.fudanIndex[key] = len(fixedRet) + len(configRet) - 1

        self.tabRet = fixedRet + configRet
        return uiUtils.array2GfxAarry(self.tabRet, True)

    def setTab(self, tabList):
        if self.mediator:
            self.mediator.Invoke('setTabVisible', uiUtils.array2GfxAarry(tabList))

    def refreshTabNotify(self):
        if self.mediator:
            self.mediator.Invoke('refreshTabNotify', uiUtils.array2GfxAarry(self._getRewardHasList()))

    def isShowIcon(self):
        ret = False
        p = BigWorld.player()
        dayCnt = int(utils.calcDaysAfterEnterWorld(p))
        if dayCnt > uiConst.DAILY_SIGNIN_MAX_DAY or dayCnt < 0:
            ret = False
        else:
            ret = True
        return ret

    def onGetOnlineLevel(self, *args):
        currentOnlineLevel = self._getCurrentOnlineLevel()
        return GfxValue(currentOnlineLevel)

    def _getCurrentOnlineLevel(self):
        p = BigWorld.player()
        currentOnlineLevel = p.noviceDailyOnline.phase - 1
        if currentOnlineLevel >= uiConst.DAILY_SIGNIN_LEVEL:
            currentOnlineLevel = uiConst.DAILY_SIGNIN_LEVEL - 1
        return currentOnlineLevel

    def onGetRewardTime(self, *args):
        rewardTime = self.getCurrentRewardTime()
        return GfxValue(rewardTime)

    def refreshIcon(self):
        if self.mediatorIcon:
            p = BigWorld.player()
            currentOnlineLevel = p.noviceDailyOnline.phase - 1
            if currentOnlineLevel >= uiConst.DAILY_SIGNIN_LEVEL:
                self.mediatorIcon.Invoke('startCountDown', (GfxValue(-1), GfxValue(currentOnlineLevel)))
            if self.isShowOnlineReward():
                self.mediatorIcon.Invoke('startCountDown')

    def onIconClick(self, *args):
        self.tabIndex = 2
        self.show()

    def getCurrentRewardTime(self):
        ret = 0
        p = BigWorld.player()
        currentOnlineLevel = self._getCurrentOnlineLevel()
        onlineRewardInfo = self._getOnlineRewardData()
        rewardTime = onlineRewardInfo[currentOnlineLevel]['rewardTime'] - p.noviceDailyOnline.getLogonTime()
        if rewardTime < 0:
            ret = 0
        else:
            ret = rewardTime
        return ret

    def isShowOnlineReward(self):
        ret = False
        p = BigWorld.player()
        dayCnt = int(utils.calcDaysAfterEnterWorld(p))
        currentOnlineLevel = p.noviceDailyOnline.phase - 1
        if dayCnt < 1 or dayCnt > len(NLRD.data.items()) / uiConst.DAILY_SIGNIN_LEVEL or currentOnlineLevel >= uiConst.DAILY_SIGNIN_LEVEL:
            ret = False
        else:
            ret = True
        return ret

    def _getRewardHasList(self):
        ret = []
        p = BigWorld.player()
        dayCnt = int(utils.calcDaysAfterEnterWorld(p))
        currentOnlineLevel = p.noviceDailyOnline.phase - 1
        if p.signInApplied >= 1:
            ret.append(0)
        else:
            ret.append(1)
        if dayCnt > len(NLRD.data.items()) / uiConst.DAILY_SIGNIN_LEVEL or dayCnt < 0 or not self.checkDailySignInStartTime():
            pass
        elif dayCnt < 0 or bool(1 << dayCnt & p.noviceSignInBM) or dayCnt > uiConst.DAILY_SIGNIN_MAX_DAY or not self.checkDailySignInStartTime():
            ret.append(0)
        else:
            ret.append(1)
        if dayCnt > uiConst.DAILY_SIGNIN_MAX_DAY or dayCnt < 0 or not self.checkDailySignInStartTime():
            pass
        elif self.isShowOnlineReward() and self.checkDailySignInStartTime():
            if dayCnt > len(NLRD.data.items()) / uiConst.DAILY_SIGNIN_LEVEL or dayCnt < 0 or not self.onlineLevelOver.get(currentOnlineLevel, 0):
                ret.append(0)
            else:
                ret.append(1)
        else:
            ret.append(0)
        for key in p.fudanDict.keys():
            if p.fudanDict[key][1]:
                ret.append(1)
            else:
                ret.append(0)

        return ret

    def currentLevelOver(self):
        self.onlineLevelOver = {-1: 0}
        rewardTime = self.getCurrentRewardTime()
        if self.callBackHandler:
            BigWorld.cancelCallback(self.callBackHandler)
        BigWorld.callback(rewardTime, Functor(self.setLevelOver))

    def setLevelOver(self):
        p = BigWorld.player()
        if not p or not p.inWorld:
            return
        currentOnlineLevel = p.noviceDailyOnline.phase - 1
        self.onlineLevelOver = {currentOnlineLevel: 1}
        self.refreshTabNotify()
        self.refreshPlane()

    def hasReward(self):
        bHasArr = self._getRewardHasList()
        for item in bHasArr:
            if item == 1:
                return True

        return False

    def checkDailySignInStartTime(self):
        p = BigWorld.player()
        dailySignInStartTime = SCD.data.get('dailySignInStartTime', {})
        startTime = utils.getTimeSecondFromStr(dailySignInStartTime)
        return p.enterWorldTime >= startTime

    def onGetFudanDesc(self, *args):
        actId = int(args[3][0].GetNumber())
        desc = LTRD.data.get(actId, {}).get('desc', '策划配置')
        return GfxValue(gbk2unicode(desc))

    def onGetFudanLevel(self, *args):
        actId = int(args[3][0].GetNumber())
        lv = self.calcFudanLevel(actId)
        return GfxValue(lv)

    def calcFudanLevel(self, actId):
        p = BigWorld.player()
        time, canApplyReward, goalTime = p.fudanDict.get(actId, [-1, False, 0])
        return p.calcFudanLevel(actId, time, canApplyReward)

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
                arr.append(j[0])

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

    def onGetFudanRewardInfo(self, *args):
        actId = int(args[3][0].GetNumber())
        ret = []
        p = BigWorld.player()
        curFudanLevel = self.calcFudanLevel(actId)
        bonusId = LTRD.data.get(actId, {}).get('bonus', [])[curFudanLevel]
        readyItem, notFinishArr, finishArr = self._getFudanBonusData(actId, curFudanLevel)
        for item in readyItem:
            obj = {}
            bList = []
            obj['levelState'] = 1
            for b in item['bonus']:
                bList.append(uiUtils.getGfxItemById(b, appendInfo={'state': uiConst.ITEM_NORMAL}))

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
                bList.append(uiUtils.getGfxItemById(b, appendInfo={'state': uiConst.ITEM_NORMAL}))

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
                bList.append(uiUtils.getGfxItemById(b, appendInfo={'state': uiConst.ITEM_NORMAL}))

            obj['bonus'] = bList
            obj['rewardTime'] = 0
            obj['rewardDesc'] = LTRD.data.get(actId, {}).get('bonus', [])[item['lv']][2]
            obj['lv'] = item['lv']
            ret.append(obj)

        return uiUtils.array2GfxAarry(ret, True)

    def onGetFudanTitleName(self, *args):
        actId = int(args[3][0].GetNumber())
        title = LTRD.data.get(actId, {}).get('title', '策划配置')
        return GfxValue(gbk2unicode(title))

    def onApplyFudan(self, *args):
        actId = int(args[3][0].GetNumber())
        p = BigWorld.player()
        p.base.applyLoginTimeReward(actId)
