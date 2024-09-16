#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/xinmoRecordProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import datetime
import utils
import gametypes
from uiProxy import UIProxy
from Scaleform import GfxValue
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from callbackHelper import Functor
from data import activity_basic_data as ABD
from cdata import collect_item_pos2item_data as CIPD
from data import collect_item_data as CID
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import bonus_data as BD

class XinmoRecordProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(XinmoRecordProxy, self).__init__(uiAdapter)
        self.modelMap = {'updateData': self.onUpdateXinmoData,
         'getData': self.onGetXinmoData,
         'forceClose': self.onForceClose,
         'findPath': self.onFindPath,
         'getServerBonus': self.onGetServerBonus,
         'getPersonBonus': self.onGetPersonBonus,
         'getScore': self.onGetScore}
        self.mediator = None
        self.timerId = None
        self.timerCountdown = 0
        self.roundInfo = {}
        self.updatePanelFlag = False
        self.isForceClose = False
        self.bossCountDown = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_XINMO_RECORD, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_XINMO_RECORD:
            self.mediator = mediator
            if self.timerId:
                return uiUtils.dict2GfxDict({'enable': False,
                 'txt': gameStrings.TEXT_XINMORECORDPROXY_48 % self.timerCountdown}, True)
            else:
                return uiUtils.dict2GfxDict({'enable': True,
                 'txt': gameStrings.TEXT_XINMORECORDPROXY_50}, True)

    def show(self):
        if gameglobal.rds.configData.get('enableCollectItem', False):
            self.isForceClose = False
            self.removeXinmoRecordMsg()
            self.requestData()
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_XINMO_RECORD)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_XINMO_RECORD)
        if not self.isForceClose:
            if self._checkActivityTime() or self._checkNotifyTime():
                self.pushXinmoRecordMsg()
            self.isForceClose = False

    def requestData(self):
        BigWorld.player().base.queryRoundInfo(10234)

    def onForceClose(self, *arg):
        self.isForceClose = True
        msg = GMD.data.get(GMDD.data.FORCE_CLOSE_XINMO_RECORD_TIP, {}).get('text', gameStrings.TEXT_XINMORECORDPROXY_73)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.hide))

    def _getXinmoDict(self):
        p = BigWorld.player()
        collectItemDict = p.collectItemDict if hasattr(p, 'collectItemDict') else {}
        xinmoDict = collectItemDict.get(10234, {})
        return xinmoDict

    def updateRoundInfo(self, roundInfo):
        self.roundInfo = roundInfo
        self.updateView()

    def updateView(self):
        ret = {}
        ret['round'] = self.roundInfo.get('roundNo', 0) - 1 if self.roundInfo.get('roundNo', 0) > 0 else 0
        ret['rarePos'] = self.roundInfo.get('rarePos', -1)
        ret['rareCharacterTips'] = CID.data.get(1, {}).get('rareCharacterTip', gameStrings.TEXT_XINMOBOOKPROXY_54)
        ret['countDown'] = self._getBossRefreshTimeCountDown()
        ret['countDownStr'] = self._getActivityDesc()
        ret['progress'] = self._getProgress()
        ret['items'] = self._getXinmoItems()
        xinmoDict = self._getXinmoDict()
        ret['count'] = '%d/%d' % (xinmoDict.get('handInCnt', 0), CID.data.get(1, {}).get('handInLimt', 0))
        ret['qumoFlag'] = xinmoDict.get('qumoFlag', 0)
        ret['qumoFame'] = xinmoDict.get('qumoFame', 0)
        contribution = xinmoDict.get('contribution', 0)
        ret['contribution'] = contribution
        ret['desc'] = CID.data.get(1, {}).get('desc', gameStrings.TEXT_XINMOBOOKPROXY_54)
        ret['tips'] = CID.data.get(1, {}).get('tips', gameStrings.TEXT_XINMORECORDPROXY_104)
        ret['personRewards'] = self._getPersonRewards()
        ret['serverProgress'] = self._getServerProgress()
        ret['qumoScoreTips'] = GMD.data.get(GMDD.data.XINMO_QUMO_CALCULATE_TIPS, {}).get('text', gameStrings.TEXT_XINMORECORDPROXY_107)
        ret['contributeTips'] = CID.data.get(1, {}).get('contributeTips', gameStrings.TEXT_XINMOBOOKPROXY_54)
        ret['isActivityEnd'] = not self._checkActivityTime()
        if self.updatePanelFlag:
            BigWorld.player().showGameMsg(GMDD.data.COLLECT_ITEM_UPDATE_PANEL_SUCCESS, ())
            self.updatePanelFlag = False
        if self.mediator:
            self.mediator.Invoke('updateView', uiUtils.dict2GfxDict(ret, True))

    def _getServerProgress(self):
        progress = {}
        xinmoDict = self._getXinmoDict()
        contribution = xinmoDict.get('contribution', 0)
        currentRound = self.roundInfo.get('roundNo', 0) - 1 if self.roundInfo.get('roundNo', 0) > 0 else 0
        abClassification = CID.data.get(1, {}).get('abClassification', [])
        activeBonus = CID.data.get(1, {}).get('activeBonus', [])
        abLowBound = CID.data.get(1, {}).get('abLowBound', 80)
        nowItemId = 0
        nextItemId = 0
        for index in xrange(len(activeBonus)):
            bonusId = activeBonus[index]
            targetRound = abClassification[index]
            fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', ())
            fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
            if fixedBonus:
                itemId = fixedBonus[0][1]
            else:
                itemId = 0
            if currentRound >= targetRound:
                nowItemId = itemId
            if currentRound < targetRound and nextItemId == 0:
                nextItemId = itemId

        endBonus = xinmoDict.get('endBonus', {})
        isRewarded = 0
        for key in endBonus:
            if endBonus.get(key, 0) == 1:
                isRewarded = 1
            if endBonus.get(key, 0) == 2:
                isRewarded = 2

        progress['nowItemId'] = nowItemId
        progress['nextItemId'] = nextItemId
        progress['nowItem'] = uiUtils.getGfxItemById(nowItemId)
        progress['nextItem'] = uiUtils.getGfxItemById(nextItemId)
        progress['tips'] = GMD.data.get(GMDD.data.XINMO_SERVER_REWARD_TIPS, {}).get('text', gameStrings.TEXT_XINMORECORDPROXY_160) % abLowBound
        progress['currentRound'] = currentRound
        progress['rounds'] = abClassification
        progress['isRewarded'] = isRewarded
        return progress

    def _getPersonRewards(self):
        xinmoDict = self._getXinmoDict()
        bonusState = xinmoDict.get('bonus', {})
        conMilestones = CID.data.get(1, {}).get('conMilestones', [])
        conBonus = CID.data.get(1, {}).get('conBonus', [])
        rewards = []
        for index in xrange(len(conBonus)):
            rewardId = conBonus[index]
            rewardObj = {}
            fixedBonus = BD.data.get(rewardId, {}).get('fixedBonus', ())
            fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
            if fixedBonus:
                fixedBonus = fixedBonus[0]
            else:
                fixedBonus = (0, 0, 0)
            rewardObj['item'] = uiUtils.getGfxItemById(fixedBonus[1], count=fixedBonus[2])
            condition = conMilestones[index] if index < len(conMilestones) else 0
            rewardObj['condition'] = gameStrings.TEXT_XINMORECORDPROXY_183 % condition
            rewardObj['conditionFlag'] = 0
            if bonusState.has_key(rewardId):
                if bonusState.get(rewardId, 0) == 1:
                    rewardObj['condition'] = uiUtils.toHtml(gameStrings.TEXT_XINMORECORDPROXY_187, '#79C725')
                    rewardObj['conditionFlag'] = 1
                elif bonusState.get(rewardId, 0) == 2:
                    rewardObj['condition'] = uiUtils.toHtml(gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_187, '#808080')
                    rewardObj['conditionFlag'] = 2
            rewards.append(rewardObj)

        return rewards

    def _getProgress(self):
        maxValue = self.roundInfo.get('needItemCnt', 100)
        if maxValue == 0:
            maxValue = 100
        ret = {'4': [0, maxValue],
         '5': [0, maxValue],
         '6': [0, maxValue],
         '1': [0, maxValue],
         '3': [0, maxValue],
         '2': [0, maxValue]}
        if self.roundInfo.has_key('posInfo'):
            for i in xrange(6):
                ret[str(i + 1)][0] = self.roundInfo.get('posInfo', {}).get(i + 1, 0)

        return ret

    def _getXinmoItems(self):
        data = CIPD.data
        p = BigWorld.player()
        items = []
        replaceItemId = 0
        for key in data.iterkeys():
            itemId = data.get(key, {}).get('originItem', 0)
            count = p.inv.countItemInPages(itemId, enableParentCheck=True)
            pathNpc = str(data.get(key, {}).get('pathNpc', ()))
            if count > 0:
                count = str(count)
            items.append(uiUtils.getGfxItemById(itemId, count=count, appendInfo={'index': key,
             'pathNpc': pathNpc}))
            replaceItemId = data.get(key, {}).get('replaceItems', [0])[0]

        items.sort(key=lambda k: k['index'])
        count = p.inv.countItemInPages(replaceItemId, enableParentCheck=True)
        if count > 0:
            count = str(count)
        items.append(uiUtils.getGfxItemById(replaceItemId, count=count))
        return items

    def onUpdateXinmoData(self, *arg):
        if self.timerId == None:
            self.updatePanelFlag = True
            self.timerCountdown = 30
            self.requestData()
            self.timerId = BigWorld.callback(1, self.updateTimer)

    def onGetXinmoData(self, *arg):
        self.updateView()

    def updateTimer(self):
        self.timerCountdown -= 1
        self.refreshUpdateBtn()
        if self.timerCountdown > 0:
            self.timerId = BigWorld.callback(1, self.updateTimer)
        else:
            self.timerId = None

    def refreshUpdateBtn(self):
        if self.mediator:
            if self.timerCountdown > 0:
                msg = gameStrings.TEXT_XINMORECORDPROXY_48 % self.timerCountdown
                self.mediator.Invoke('refreshUpdateBtn', (GfxValue(gbk2unicode(msg)), GfxValue(False)))
            else:
                self.mediator.Invoke('refreshUpdateBtn', (GfxValue(gbk2unicode(gameStrings.TEXT_XINMORECORDPROXY_50)), GfxValue(True)))

    def _checkNotifyTime(self):
        data = ABD.data.get(10234, {})
        joinActTimeList = data.get('joinActTime', ())
        weekSet = data.get('weekSet', 0)
        for joinActTime in joinActTimeList:
            if utils.inCrontabRange(joinActTime[0], joinActTime[1], weekSet=weekSet):
                return True

        return False

    def _checkActivityTime(self):
        data = ABD.data.get(10234, {})
        weekSet = data.get('weekSet', 0)
        startTimes = data.get('startTimes', None)
        endTimes = data.get('endTimes', None)
        if endTimes and startTimes:
            if utils.inCrontabRange(startTimes[0], endTimes[0], weekSet=weekSet):
                return True
        return False

    def _getCountDown(self):
        countDown = -1
        now = utils.getNow()
        data = ABD.data.get(10234, {})
        if self._checkActivityTime():
            endTimes = data.get('endTimes', None)
            if endTimes:
                countDown = utils.getNextCrontabTime(endTimes[0]) - now
        elif self._checkNotifyTime():
            startTimes = data.get('startTimes', None)
            if startTimes:
                countDown = utils.getNextCrontabTime(startTimes[0]) - now
        return countDown

    def pushXinmoRecordMsg(self):
        if gameglobal.rds.configData.get('enableCollectItem', False):
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_PUSH_XINMO_RECORD)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_PUSH_XINMO_RECORD, {'click': self.clickOpenXinmoRecord})

    def _getPushMsgTip(self):
        tipMsg = gameStrings.TEXT_XINMORECORDPROXY_297
        if self._checkActivityTime() and self._checkCollectItemSignUp():
            if self.isInSameDayTime():
                if self._isInBossRefreshTime():
                    tipMsg = GMD.data.get(GMDD.data.COLLECT_ITEM_PUSH_IN_BOSS_MSG, {}).get('text', gameStrings.TEXT_XINMORECORDPROXY_301)
                else:
                    refreshTime = self._getBossRefreshTime()
                    tipMsg = GMD.data.get(GMDD.data.COLLECT_ITEM_PUSH_BOSS_REFRESH_MSG, {}).get('text', gameStrings.TEXT_XINMORECORDPROXY_304) % refreshTime
            else:
                tipMsg = gameStrings.TEXT_XINMORECORDPROXY_297
        return tipMsg

    def removeXinmoRecordMsg(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PUSH_XINMO_RECORD)

    def clickOpenXinmoRecord(self):
        self.show()

    def _checkCollectItemSignUp(self):
        isSignUp = False
        p = BigWorld.player()
        now = utils.getNow()
        if hasattr(p, 'collectItemDict'):
            start = p.collectItemDict.get(10234, {}).get('start', 0)
            end = p.collectItemDict.get(10234, {}).get('end', 0)
            if now > start and now < end:
                isSignUp = True
        return isSignUp

    def onFindPath(self, *arg):
        pathStr = arg[3][0].GetString()
        uiUtils.findPosById(pathStr)

    def _isInBossRefreshTime(self):
        refreshTime = CID.data.get(1, {}).get('refreshTime', [])
        for rTime in refreshTime:
            if utils.inCrontabRange(rTime[0], rTime[1]):
                return True

        return False

    def _getBossRefreshTimeCountDown(self, skipInBoss = False):
        if not self._checkActivityTime():
            return 0
        if not self._checkCollectItemSignUp():
            return 0
        if not self.isInSameDayTime():
            return 0
        if not skipInBoss and self._isInBossRefreshTime():
            return 0
        now = utils.getNow()
        startTime = self.getNearStartTime()
        return startTime - now

    def _getActivityDesc(self):
        if not self._checkActivityTime():
            return gameStrings.TEXT_XINMORECORDPROXY_358
        if self._checkActivityTime() and not self._checkCollectItemSignUp():
            return gameStrings.TEXT_XINMORECORDPROXY_361
        if self._isInBossRefreshTime():
            return gameStrings.TEXT_XINMORECORDPROXY_364
        if not self.isInSameDayTime():
            return gameStrings.TEXT_XINMORECORDPROXY_367
        return gameStrings.TEXT_XINMORECORDPROXY_358

    def getNearStartTime(self):
        refreshTime = CID.data.get(1, {}).get('refreshTime', [])
        startTime = None
        for rTime in refreshTime:
            if startTime == None:
                startTime = utils.getNextCrontabTime(rTime[0])
            else:
                startTime = min(startTime, utils.getNextCrontabTime(rTime[0]))

        return startTime

    def isInSameDayTime(self):
        refreshTime = CID.data.get(1, {}).get('refreshTime', [])
        if len(refreshTime) > 0:
            begin = refreshTime[0][0]
            end = refreshTime[len(refreshTime) - 1][1]
            if utils.inCrontabRange(begin, end):
                return True
        return False

    def _getBossRefreshTime(self):
        startTime = self.getNearStartTime()
        return datetime.datetime.fromtimestamp(startTime).strftime('%H:%M:%S')

    def updateBossCountDown(self):
        if self._checkActivityTime():
            countDown = self._getBossRefreshTimeCountDown(True)
            if countDown > 0 and not self.bossCountDown:
                self.bossCountDown = BigWorld.callback(countDown, self.notifyBossRefresh)

    def notifyBossRefresh(self):
        self.bossCountDown = None
        BigWorld.player().showGameMsg(GMDD.data.COLLECT_ITEM_BOSS_REFRESH, ())
        gameglobal.rds.ui.xinmoRecord.updateBossCountDown()

    def onGetServerBonus(self, *arg):
        BigWorld.player().base.useCollectItemEndBonus(10234)

    def onGetPersonBonus(self, *arg):
        BigWorld.player().base.useCollectItemBonus(10234)

    def onGetScore(self, *arg):
        BigWorld.player().base.useQumoFame(10234, 0)

    def cancelBossCountDown(self):
        if self.bossCountDown:
            BigWorld.cancelCallback(self.bossCountDown)
            self.bossCountDown = None
