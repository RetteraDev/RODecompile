#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yunchuijiProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import const
import utils
import commServerProgress
from guis import events
from guis import ui
from guis import uiConst
from guis import uiUtils
from uiProxy import UIProxy
from data import server_progress_data as SPD
from data import server_progress_reverted_data as SPRD
from data import server_progress_config_data as SPCD
from data import server_progress_target_data as SPTD
from data import guild_tournament_data as GTD
CATE_ICON_TEMPLATE = 'yunchuiji/%s.dds'
TARGET_TYPE_PROGRESS = 1
TARGET_TYPE_DESCRIPTION = 2

class YunchuijiProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(YunchuijiProxy, self).__init__(uiAdapter)
        self.modelMap = {'getTabsInfo': self.onGetTabsInfo,
         'getYunChuijiInfoByTab': self.onGetYunChuijiInfoByTab}
        self.mediator = None
        self.yunchuijiWidgetId = uiConst.WIDGET_YUNCHUIJI
        self.crossMsIds = {}
        self.crossMsIdsVer = 0
        uiAdapter.registerEscFunc(self.yunchuijiWidgetId, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.yunchuijiWidgetId:
            spd = getattr(BigWorld.player(), 'serverProgressData', None)
            if spd and len(spd) >= 4:
                ver = spd[3]
            else:
                ver = 0
            BigWorld.player().cell.queryServerProgress(ver)
            self.mediator = mediator

    def show(self):
        if not gameglobal.rds.configData.get('enableServerProgress', False):
            return
        gameglobal.rds.ui.loadWidget(self.yunchuijiWidgetId)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(self.yunchuijiWidgetId)
        self.mediator = None

    def reset(self):
        self.mediator = None
        self.crossMsIds = {}
        self.crossMsIdsVer = 0

    @ui.uiEvent(uiConst.WIDGET_YUNCHUIJI, events.EVENT_UPDATE_SERVER_PROGRESS)
    def updateServerProgress(self):
        if not self.mediator:
            return
        self.mediator.Invoke('updateServerProgress')

    def onGetTabsInfo(self, *arg):
        ret = []
        tabIds = SPRD.data.keys()
        tabNames = SPCD.data.get('yunchuijiTabName', {})
        for i in range(len(tabIds)):
            tabId = tabIds[i]
            if tabId not in tabNames:
                continue
            tabInfo = {}
            tabInfo['tabName'] = tabNames[tabId]
            tabInfo['tabId'] = tabId
            ret.append(tabInfo)

        return uiUtils.array2GfxAarry(ret, True)

    def onGetYunChuijiInfoByTab(self, *arg):
        tabId = int(arg[3][0].GetNumber())
        ret = []
        tabData = SPRD.data.get(tabId, {})
        subCateIds = tabData.keys()
        subCateNames = SPCD.data.get('yunchuijiCategoryName', {})
        subCateIcons = SPCD.data.get('yunchuijiCategoryIcon', {})
        subCateOrder = SPCD.data.get('yunchuijiCategoryOrder', {})
        for i in range(len(subCateIds)):
            cateId = subCateIds[i]
            if cateId not in subCateNames:
                continue
            if cateId not in subCateIcons:
                continue
            if cateId not in subCateOrder:
                continue
            cateInfo = {}
            cateData = tabData[cateId]
            cateInfo['cateId'] = cateId
            cateInfo['cateName'] = subCateNames[cateId]
            cateInfo['cateIcon'] = CATE_ICON_TEMPLATE % str(subCateIcons[cateId])
            cateInfo['cateItems'] = self.genCateItems(cateData)
            cateInfo['cateOrder'] = subCateOrder[cateId]
            ret.append(cateInfo)

        ret.sort(key=lambda info: info['cateOrder'])
        return uiUtils.array2GfxAarry(ret, True)

    def genCateItems(self, cateData):
        completeKeys, nowKey, spVars = self.collectSpItemIds(cateData)
        openTime = utils.getServerOpenTime()
        now = utils.getNow()
        spdd = SPD.data
        ret = []
        gtMsIds = [ data.get('serverProgressMsId') for data in GTD.data.itervalues() ]
        for key in completeKeys:
            spInfo = {}
            if spdd.get(key, {}).get('disable'):
                continue
            if key in gtMsIds and not gameglobal.rds.configData.get('enableGuildTournament', False):
                continue
            spInfo.update(spdd.get(key, {}))
            spInfo['leftTimeInfo'] = self.genLeftTimeInfo(key, spInfo)
            spInfo['complete'] = True
            ret.append(spInfo)

        if nowKey:
            spInfo = {}
            spData = spdd.get(nowKey, {})
            spInfo.update(spData)
            spInfo['complete'] = False
            spInfo['targetInfos'] = self.genTargetInfos(spInfo)
            spInfo['now'] = now - now % const.TIME_INTERVAL_DAY
            delayFinishedDays = self.getDelayFinishDay(nowKey)
            if delayFinishedDays:
                spInfo['minExpire'] = delayFinishedDays
            elif spData.get('minDuration', 0):
                spInfo['minExpire'] = openTime + spData['minDuration'] * const.TIME_INTERVAL_DAY
            else:
                spInfo['minExpire'] = 0
            maxDuration = commServerProgress.getMaxDuration(nowKey, BigWorld.player().serverProgresses)
            if spData.get('maxDuration', 0):
                spInfo['maxExpire'] = openTime + maxDuration * const.TIME_INTERVAL_DAY
            else:
                spInfo['maxExpire'] = 0
            if not spData.get('disable') and (nowKey not in gtMsIds or gameglobal.rds.configData.get('enableGuildTournament', False)):
                ret.append(spInfo)
        return ret

    def genLeftTimeInfo(self, key, spInfo):
        delayDays = spInfo.get('delayDays', 0)
        if not delayDays:
            return ''
        spd = getattr(BigWorld.player(), 'serverProgressData', None)
        if not spd:
            vars = {}
        else:
            _, _, vars, _ = spd
        now = utils.getNow()
        finishTime = vars.get('finishTime', {}).get(key, now)
        delayExpire = utils.getDaySecond(finishTime)
        nowDaySec = utils.getDaySecond(now)
        leftDays = delayDays - (nowDaySec - delayExpire) / const.TIME_INTERVAL_DAY
        if leftDays <= 0:
            return ''
        elif leftDays > 0:
            return SPCD.data.get('delayDaysTips', gameStrings.TEXT_YUNCHUIJIPROXY_197) % leftDays
        else:
            return

    def genTargetInfos(self, spInfo):
        if spInfo.get('complete', True):
            return []
        else:
            sptdd = SPTD.data
            spd = getattr(BigWorld.player(), 'serverProgressData', None)
            if not spd:
                vars = {}
            else:
                _, _, vars, _ = spd
            ret = []
            targetIds = spInfo.get('targetIds', ())
            for tid in targetIds:
                tgtInfo = {}
                tData = sptdd.get(tid, {})
                if not tData.get('showTarget', 1):
                    continue
                tgtInfo.update(tData)
                varKey = tData.get('var', 'unknow')
                tgtInfo['varValue'] = vars.get(varKey, 0)
                tgtInfo['targetType'] = TARGET_TYPE_PROGRESS
                fmtString = tData.get('format', '')
                if fmtString.find('%d') >= 0:
                    tgtInfo['tipFormat'] = fmtString % tgtInfo['varValue']
                else:
                    tgtInfo['tipFormat'] = fmtString
                ret.append(tgtInfo)

            return ret

    def getDelayFinishDay(self, key):
        delayFinishedDays = SPD.data.get(key, {}).get('delayFinishedDays', 0)
        if delayFinishedDays:
            spd = getattr(BigWorld.player(), 'serverProgressData', None)
            if not spd:
                return 0
            _, targets, vars, _ = spd
            targetInfo = {}
            for targetId, tWhen in targets:
                targetInfo[targetId] = tWhen

            serverTime = utils.getServerOpenTime()
            now = utils.getNow()
            nowExpire = utils.getDaySecond(now)
            earlestTime = serverTime + SPD.data.get(key, {}).get('minDuration', 0) * const.TIME_INTERVAL_DAY
            if nowExpire < earlestTime:
                return 0
            targetIds = SPD.data.get(key, {}).get('targetIds', ())
            allTargetFinish = True
            targetFinishTime = 0
            for targetId in targetIds:
                if targetId not in targetInfo.keys():
                    allTargetFinish = False
                elif targetFinishTime < targetInfo.get(targetId, 0):
                    targetFinishTime = targetInfo.get(targetId)

            if not allTargetFinish:
                return 0
            if targetFinishTime < earlestTime:
                targetFinishTime = earlestTime
            targetFinishExpire = utils.getDaySecond(targetFinishTime)
            delayFinishExpire = targetFinishExpire + delayFinishedDays * const.TIME_INTERVAL_DAY
            return delayFinishExpire
        else:
            return 0

    def collectSpItemIds(self, cateData):
        itemKeys = []
        for key in cateData.keys():
            cId = SPD.data.get(key, {}).get('serverConfigId', 0)
            if cId and not utils.checkInCorrectServer(cId):
                continue
            itemKeys.append(key)

        itemKeys.sort(key=lambda spId: cateData[spId]['pos'])
        if not itemKeys:
            return ([], 0, {})
        else:
            spd = getattr(BigWorld.player(), 'serverProgressData', None)
            if not spd:
                return ([], 0, {})
            mileStones, targets, vars, ver = spd
            completeKeys = []
            nowKey = 0
            for key in itemKeys:
                if key in mileStones:
                    completeKeys.append(key)

            if not completeKeys:
                nowKey = itemKeys[0]
                return (completeKeys, nowKey, vars)
            if len(completeKeys) == len(itemKeys):
                return (completeKeys, 0, vars)
            lastComplete = completeKeys[-1]
            lastIndex = itemKeys.index(lastComplete)
            if lastIndex < len(itemKeys) - 1:
                nowKey = itemKeys[lastIndex + 1]
            return (completeKeys, nowKey, vars)
