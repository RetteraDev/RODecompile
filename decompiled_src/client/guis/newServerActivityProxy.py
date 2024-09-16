#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/newServerActivityProxy.o
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
from cdata import font_config_data as FCD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from data import open_server_bonus_data as OSBD
from cdata import open_server_bonus_vp_data as OSBVD
from helpers import importantPlayRecommend as IPR
from data import activity_signin_bonus_data as ASBD
from data import activity_achieve_score_condition_data as AASCD
from cdata import activity_achieve_score_bonus_data as AASBD
from data import activity_achieve_score_config_data as AASFD
from cdata import activity_resignin_config_data as ARCD
from data import activity_signin_type_data as ASTD
from data import vp_level_data as VLD

class NewServerActivityProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NewServerActivityProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.onCloseWidget,
         'getDateInfo': self.onGetNewServerDateInfo,
         'attendSign': self.onAttendServerSign,
         'enableServerBonus': self.onEnableNewServerBonus,
         'getServerBonusData': self.onGetNewServerBonusData,
         'gainServerBonus': self.onGainNewServerBonus,
         'getRecommendInfo': self.onGetNewRecommendInfo,
         'getScoreInfo': self.onGetScoreInfo,
         'getServerScoreReward': self.onGetServerScoreReward,
         'attendResign': self.onAttendResign,
         'enableNewServerSignIn': self.onEnableNewServerSignIn}
        self.mediator = None
        self.monthIdx = 1
        self.now = 0
        self.bonusTip = {}
        self.tabIndex = 0
        self.awardScores = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_NEW_SERVER_ACTIVITY, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_NEW_SERVER_ACTIVITY:
            self.mediator = mediator
            if self.tabIndex == 0 and not self.enableNewServerSignIn():
                self.tabIndex = 1
            return GfxValue(self.tabIndex)

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_NEW_SERVER_ACTIVITY)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_NEW_SERVER_ACTIVITY)
        self.mediator = None
        self.tabIndex = 0
        ui.set_cursor('arrow_normal', 'arrow_normal')

    def isShow(self):
        return self.show

    def reset(self):
        pass

    def refresh(self, now = None):
        if now is not None:
            self.now = now
        if self.mediator is not None:
            self.mediator.Invoke('refreshDisplay', self.onGetNewServerDateInfo())

    def refreshRecomm(self):
        if not self.mediator:
            return
        if not self._isEnabledServerBonus():
            return
        self.mediator.Invoke('refreshRecommendView')

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

    def __tmpAttendTips(self, ret, title):
        nameMap = {gametypes.BONUS_TYPE_MONEY: '云券',
         gametypes.BONUS_TYPE_FAME: '声望',
         gametypes.BONUS_TYPE_EXP: '经验',
         gametypes.BONUS_TYPE_FISHING_EXP: '钓鱼经验',
         gametypes.BONUS_TYPE_SOC_EXP: '社会经验'}
        tipString = "<font size = \'14\' color = \'#f2ab0d\'>" + title + '</font><br>'
        for i in range(0, ret['num']):
            if ret[i][0] == gametypes.BONUS_TYPE_ITEM:
                tipString += "<font size = \'12\'>" + '· ' + ret[i][3] + '×' + str(ret[i][1]) + '</font><br>'
            else:
                tipString += "<font size = \'12\'>" + '· ' + str(ret[i][1]) + '×' + nameMap.get(ret[i][0]) + '</font><br>'

        return GfxValue(gbk2unicode(tipString))

    def onCloseWidget(self, *arg):
        self.clearWidget()

    def onGetNewServerDateInfo(self, *arg):
        ret = self._generateSignInData()
        return uiUtils.dict2GfxDict(ret, True)

    def _generateSignInData(self):
        ret = {}
        items = []
        signInData = ASBD.data
        newSignInInfo = self._getNewServerSignInfo()
        dates = []
        resignCnt = 0
        assignedCnt = 0
        if newSignInInfo:
            resignCnt = newSignInInfo.resignCnt
            assignedCnt = len(newSignInInfo.dates)
            dates = newSignInInfo.dates
        today = int(self._getTodayDate())
        canSignCnt = 0
        for key in signInData:
            if key[0] != const.ACTIVITY_NEW_SERVER_ACHIEVE:
                continue
            obj = {}
            data = signInData[key]
            day = data.get('day', 0)
            obj['day'] = day
            date = self._convertToDate(day - 1)
            displayItemId = data.get('displayItemId', 0)
            isImportant = data.get('isImportant', 0)
            obj['item'] = uiUtils.getGfxItemById(displayItemId)
            obj['item'].pop('itemId')
            obj['isImportant'] = isImportant
            obj['status'] = 0
            if day <= len(dates):
                obj['status'] = 1
            if int(date) <= today:
                canSignCnt += 1
            items.append(obj)

        items = sorted(items, key=lambda d: d['day'])
        ret['items'] = items
        hasSigned = today in dates
        resignData = ARCD.data.get(const.ACTIVITY_NEW_SERVER_ACHIEVE, None)
        totalResign = resignData.get('reSignInCnt', 0)
        missedCnt = canSignCnt - assignedCnt
        if today not in dates:
            missedCnt -= 1
        restResignCnt = totalResign - resignCnt
        restResignCnt = min(missedCnt, restResignCnt)
        attendInfo = {'resignCntStr': '%d次' % restResignCnt,
         'missedCnt': '%d次' % missedCnt,
         'hasSigned': hasSigned,
         'resignCnt': restResignCnt}
        ret['attendInfo'] = attendInfo
        return ret

    def refreshSignActivity(self):
        if self.mediator:
            ret = self._generateSignInData()
            self.mediator.Invoke('refreshSignIn', uiUtils.dict2GfxDict(ret, True))

    def _convertToDate(self, day):
        daySec = utils.getServerOpenTime() + day * 24 * 60 * 60
        date = time.strftime('%Y%m%d', time.localtime(daySec))
        return date

    def _getTodayDate(self):
        daySec = utils.getNow()
        date = time.strftime('%Y%m%d', time.localtime(daySec))
        return date

    def onGetToolTip(self, *arg):
        ret = {}
        slotIdx = 0
        if arg[3][0] is not None:
            key, slotIdx = arg[3][0].GetString().split('.')
        day = int(slotIdx) + 1
        signInData = ASBD.data
        bdd = BD.data
        bonusId = signInData.get((const.ACTIVITY_NEW_SERVER_ACHIEVE, day), {}).get('bonusId', 0)
        fixedBonus = bdd.get(bonusId, {}).get('fixedBonus', ())
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        for i in range(0, len(fixedBonus)):
            ret[i] = self.__getBonusInfo(fixedBonus, i)

        ret['num'] = len(fixedBonus)
        return self.__tmpAttendTips(ret, '签到物品')

    def onGetBonusItemTip(self, *arg):
        if arg[3][0] is not None:
            key, slotIdx = arg[3][0].GetString().split('.')
        slotIdx = int(slotIdx)
        if not self._checkBonusRewardEnable(slotIdx):
            tipStr = self.bonusTip[slotIdx]
        else:
            tipStr = self._getNewServerBonusTip(slotIdx)
        return GfxValue(gbk2unicode(tipStr))

    def onGetAchieveItemTip(self, *arg):
        ret = {}
        slotIdx = 0
        if arg[3][0] is not None:
            key, slotIdx = arg[3][0].GetString().split('.')
        day = int(slotIdx) + 1
        achieveData = AASBD.data
        bdd = BD.data
        bonusId = achieveData.get((const.ACTIVITY_NEW_SERVER_ACHIEVE, day), {}).get('bonusId', 0)
        fixedBonus = bdd.get(bonusId, {}).get('fixedBonus', ())
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        for i in range(0, len(fixedBonus)):
            ret[i] = self.__getBonusInfo(fixedBonus, i)

        ret['num'] = len(fixedBonus)
        return self.__tmpAttendTips(ret, '积分奖励')

    def _checkBonusRewardEnable(self, day):
        openDay = self._getOpenServerDay()
        if day <= openDay:
            return True
        return False

    def _getNewServerBonusTip(self, day):
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

    def _doResignIn(self):
        BigWorld.player().cell.applyReSignInReward()

    def onAttendServerSign(self, *arg):
        BigWorld.player().cell.applySignInRewardV2(const.ACTIVITY_NEW_SERVER_ACHIEVE)

    def onEnableNewServerBonus(self, *arg):
        enabled = self._isEnabledServerBonus()
        return GfxValue(enabled)

    def _isEnabledServerBonus(self):
        enabled = gameglobal.rds.configData.get('enableOpenServerBonus', False)
        minLv = SCD.data.get('openServerBonusMinLv', 0)
        hasRewardedALL = self._getRewardedAll()
        isAvaliableLv = BigWorld.player().lv >= minLv
        return enabled and not hasRewardedALL and isAvaliableLv

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

    def onGetNewServerBonusData(self, *arg):
        ret = self._getServerBonusData()
        return uiUtils.dict2GfxDict(ret, True)

    def refreshNewServerBonus(self):
        ret = self._getServerBonusData()
        if self.mediator:
            self.mediator.Invoke('updateBonusView', uiUtils.dict2GfxDict(ret, True))

    def onGainNewServerBonus(self, *arg):
        BigWorld.player().cell.gainOpenServerBonus()

    def onGetNewRecommendInfo(self, *arg):
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

    def onGetScoreInfo(self, *arg):
        rewardData = self._getScoreAward()
        award = rewardData[0]
        hasReward = rewardData[1]
        progress = self._getProgressBar()
        progressBar = progress[0]
        maxScore = progress[1]
        achieve = self._getAchievement()
        isLock = not self.enableNewServerScore()
        duration = AASFD.data.get(const.ACTIVITY_NEW_SERVER_ACHIEVE, {}).get('duration', 30)
        endTimeSec = utils.getDaySecond(utils.getServerOpenTime()) + duration * 24 * 60 * 60
        endTime = time.strftime('%m-%d %H:%M', time.localtime(endTimeSec))
        endTime = '活动截止时间至%s' % endTime
        ret = {}
        ret['award'] = award
        ret['progressBar'] = progressBar
        ret['achieve'] = achieve
        ret['isLock'] = isLock
        achieveScores = getattr(BigWorld.player(), 'activityAchieveScore', {}).get(const.ACTIVITY_NEW_SERVER_ACHIEVE, {})
        totalScore = achieveScores.get('val', 0)
        ret['ProgressScore'] = '%d/%d' % (totalScore, maxScore)
        ret['totalScore'] = totalScore
        ret['endTime'] = endTime
        ret['hasReward'] = hasReward
        return uiUtils.dict2GfxDict(ret, True)

    def _getScoreAward(self):
        awardItem = []
        awardData = AASBD.data
        achieveScores = getattr(BigWorld.player(), 'activityAchieveScore', {}).get(const.ACTIVITY_NEW_SERVER_ACHIEVE, {})
        rewardedActivityTypes = getattr(BigWorld.player(), 'rewardedActivityTypes', [])
        totalScore = achieveScores.get('val', 0)
        hasAvalibaleReward = False
        for key in awardData:
            if key[0] != const.ACTIVITY_NEW_SERVER_ACHIEVE:
                continue
            data = awardData[key]
            bonusId = data.get('bonusId', 0)
            fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', ())
            fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
            if fixedBonus:
                itemId = fixedBonus[0][1]
            else:
                itemId = 0
            needScore = data.get('score', 0)
            status = -1
            if needScore <= totalScore and key not in rewardedActivityTypes:
                status = 0
                hasAvalibaleReward = True
            elif key in rewardedActivityTypes:
                status = 1
            data = uiUtils.getGfxItemById(itemId, appendInfo={'status': status,
             'needScore': needScore})
            data.pop('itemId')
            awardItem.append(data)

        awardItem = sorted(awardItem, key=lambda d: d['needScore'])
        return (awardItem, hasAvalibaleReward)

    def _getProgressBar(self):
        progressbar = []
        awardData = AASBD.data
        achieveScores = getattr(BigWorld.player(), 'activityAchieveScore', {}).get(const.ACTIVITY_NEW_SERVER_ACHIEVE, {})
        currentScore = achieveScores.get('val', 0)
        temp = []
        for key in awardData:
            if key[0] != const.ACTIVITY_NEW_SERVER_ACHIEVE:
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

    def _getAchievement(self):
        achievementItem = []
        achieveScores = getattr(BigWorld.player(), 'activityAchieveScore', {}).get(const.ACTIVITY_NEW_SERVER_ACHIEVE, {})
        finishedAchieves = achieveScores.get('finished', [])
        achieveData = AASCD.data
        for key in achieveData:
            if key[0] != const.ACTIVITY_NEW_SERVER_ACHIEVE:
                continue
            data = achieveData[key]
            obj = {}
            obj['score'] = data.get('score', 0)
            obj['detail'] = ''
            obj['detailContent'] = data.get('desc', '')
            obj['achieveId'] = key[2]
            obj['status'] = 1 if (key[1], key[2]) in finishedAchieves else 0
            obj['sortId'] = data.get('sortId', 0)
            achievementItem.append(obj)

        achievementItem = sorted(achievementItem, key=lambda d: d['sortId'])
        achievementItem = sorted(achievementItem, key=lambda d: d['status'])
        return achievementItem

    def onGetServerScoreReward(self, *arg):
        BigWorld.player().cell.applyActivityAchieveScoreReward(const.ACTIVITY_NEW_SERVER_ACHIEVE)

    def onAttendResign(self, *arg):
        resignData = ARCD.data.get(const.ACTIVITY_NEW_SERVER_ACHIEVE, None)
        if not resignData:
            return
        reSignInItemId = resignData.get('reSignInItemId', 0)
        newSignInInfo = self._getNewServerSignInfo()
        resignCnt = 0
        if newSignInInfo:
            resignCnt = newSignInInfo.resignCnt
        reSignInItemCnt = resignData.get('reSignInItemCnt', {}).get(resignCnt + 1, 0)
        ownCnt = BigWorld.player().inv.countItemInPages(int(reSignInItemId), enableParentCheck=True)
        cntStr = uiUtils.convertNumStr(ownCnt, reSignInItemCnt)
        msg = GMD.data.get(GMDD.data.RESIGNIN_ITEM_COST, {}).get('text', '是否消耗物品补签?')
        itemDataList = []
        itemData = uiUtils.getGfxItemById(reSignInItemId, count=cntStr)
        itemDataList.append(itemData)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.onConfirmResignin, yesBtnText='补签', noBtnText='取消', title='系统提示', itemData=itemDataList)

    def onConfirmResignin(self):
        BigWorld.player().cell.applyReSignInRewardV2(const.ACTIVITY_NEW_SERVER_ACHIEVE)

    def refreshScoreDisplay(self):
        if self.mediator:
            self.mediator.Invoke('refreshScoreDisplay', self.onGetScoreInfo())

    def isNewServerActivityEnd(self):
        signInDuration = ASTD.data.get(const.ACTIVITY_NEW_SERVER_ACHIEVE, {}).get('duration', 15)
        scoreDuration = AASCD.data.get(const.ACTIVITY_NEW_SERVER_ACHIEVE, {}).get('duration', 30)
        bonusDuration = 30
        maxDuraion = max(signInDuration, scoreDuration)
        maxDuraion = max(maxDuraion, bonusDuration)
        openDays = self._getOpenServerDay()
        return openDays > maxDuraion

    def notifyNewServerSignInMsg(self):
        if gameglobal.rds.configData.get('enableWelfare', False):
            return
        enableNewServerSignIn = gameglobal.rds.configData.get('enableNewServerSignIn', False)
        if enableNewServerSignIn and self._hasSignInReward():
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_NEW_SERVER_SIGNIN_REWARD, {'click': self.clickOpenSignIn})
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_NEW_SERVER_SIGNIN_REWARD)

    def clickOpenSignIn(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_NEW_SERVER_SIGNIN_REWARD)
        if self.mediator:
            self.mediator.Invoke('changeTabIndex', GfxValue(0))
        else:
            self.tabIndex = 0
            self.show()

    def _hasSignInReward(self):
        newSignInInfo = self._getNewServerSignInfo()
        dates = []
        if newSignInInfo:
            dates = newSignInInfo.dates
        today = int(self._getTodayDate())
        hasSigned = today in dates
        return not hasSigned

    def notifyNewServerBonusPushMsg(self):
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
            self.mediator.Invoke('changeTabIndex', GfxValue(2))
        else:
            self.tabIndex = 2
            self.show()

    def notifyNewServerScorePushMsg(self):
        if gameglobal.rds.configData.get('enableWelfare', False):
            return
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_NEW_SERVER_SCORE_REWARD, {'click': self.clickOpenNewServerScore})
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_NEW_SERVER_SCORE_REWARD)

    def clickOpenNewServerScore(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_NEW_SERVER_SCORE_REWARD)
        if self.mediator:
            self.mediator.Invoke('changeTabIndex', GfxValue(1))
        else:
            self.tabIndex = 1
            self.show()

    def enableNewServerSignIn(self):
        enableNewServerSignIn = gameglobal.rds.configData.get('enableNewServerSignIn', False)
        signInDuration = ASTD.data.get(const.ACTIVITY_NEW_SERVER_ACHIEVE, {}).get('duration', 30)
        openDays = self._getOpenServerDay()
        return enableNewServerSignIn and signInDuration >= openDays

    def enableNewServerScore(self):
        scoreDuration = AASCD.data.get(const.ACTIVITY_NEW_SERVER_ACHIEVE, {}).get('duration', 30)
        openDays = self._getOpenServerDay()
        enableActivityAchieveScore = gameglobal.rds.configData.get('enableActivityAchieveScore', False)
        return scoreDuration >= openDays and enableActivityAchieveScore

    def onEnableNewServerSignIn(self, *arg):
        return GfxValue(self.enableNewServerSignIn())

    def _getNewServerSignInfo(self):
        newSignInInfo = BigWorld.player().newSignInInfo
        if newSignInInfo and newSignInInfo.get(const.ACTIVITY_NEW_SERVER_ACHIEVE):
            return newSignInInfo.get(const.ACTIVITY_NEW_SERVER_ACHIEVE)
