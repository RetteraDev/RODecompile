#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/dailyAttendProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import utils
import time
import gametypes
import const
from ui import gbk2unicode
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

class DailyAttendProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DailyAttendProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.onCloseWidget,
         'getDateInfo': self.onGetDateInfo,
         'getAttendInfo': self.onGetAttendInfo,
         'getShowInfo': self.onGetShowInfo,
         'retroactiveSign': self.onRetroactiveSign,
         'attendSign': self.onAttendSign,
         'enableServerBonus': self.onEnableServerBonus,
         'getServerBonusData': self.onGetServerBonusData,
         'gainServerBonus': self.onGainServerBonus,
         'getRecommendInfo': self.onGetRecommendInfo}
        self.mediator = None
        self.monthIdx = 1
        self.now = 0
        self.bonusTip = {}
        self.tabIndex = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_DAILY_ATTEND_NEW, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DAILY_ATTEND_NEW:
            self.mediator = mediator
            return GfxValue(self.tabIndex)

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DAILY_ATTEND_NEW)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DAILY_ATTEND_NEW)

    def isShow(self):
        return self.show

    def reset(self):
        self.tabIndex = 0
        ui.set_cursor('arrow_normal', 'arrow_normal')

    def refresh(self, now = None):
        if now is not None:
            self.now = now
        if self.mediator is not None:
            self.mediator.Invoke('refreshDisplay', self.onGetDateInfo())

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
            if not gameglobal.rds.configData.get('enableNoviceReward', False):
                self.show()
            else:
                gameglobal.rds.ui.dailySignIn.show()
