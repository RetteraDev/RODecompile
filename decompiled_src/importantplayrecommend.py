#Embedded file name: /WORKSPACE/data/entities/client/helpers/importantplayrecommend.o
import BigWorld
import copy
import gametypes
import gameglobal
import utils
import const
from crontab import CronTab
from data import important_play_recomm_data as IPRD
from data import quest_loop_data as QLD
from data import quest_data as QD
from data import fame_data as FD
from data import mall_config_data as MCFD
from data import mall_item_data as MID
from data import play_recomm_config_data as PRCD
from data import consumable_reverse_data as CRD
from data import world_war_config_data as WWCD
ASTATE_BEFORE = 1
ASTATE_PROCESS = 2
ASTATE_AFTER = 3
ASTATE_ORDER = 4
ORDER_OFFSET_COMPLETE = 500

class ImportantRecommendItem(object):

    def __init__(self, prid = 0, name = '', value = 0, maxValue = 0, astate = ASTATE_BEFORE, extParams = {}, rData = {}):
        self.prid = prid
        self.name = name
        self.rData = rData
        self.value = value
        self.maxValue = maxValue
        self.astate = astate
        self.extParams = copy.deepcopy(extParams)
        self.order = IPRD.data.get(prid).get('order', 0)
        self.order += ORDER_OFFSET_COMPLETE if value >= maxValue or astate == ASTATE_AFTER else 0

    def getDTO(self):
        return (self.prid,
         self.name,
         self.value,
         self.maxValue,
         self.extParams,
         self.order)

    def getTips(self, key):
        tipData = self.rData.get(key, None)
        if tipData is None:
            return ''
        if type(tipData) == str:
            return tipData
        if type(tipData) == dict:
            lv = BigWorld.player().lv
            for lvRange in tipData:
                if len(lvRange) == 2 and lv >= lvRange[0] and lv <= lvRange[1]:
                    return tipData[lvRange]

        return ''

    def formatReturn(self):
        ret = {}
        ret['prid'] = self.prid
        ret['name'] = self.name
        ret['tips1'] = self.getTips('tips1')
        ret['tips2'] = self.getTips('tips2')
        ret['aState'] = self.astate
        ret['spriteKeyWord'] = self.rData.get('spriteKeyWord', '')
        ret['totalBuff'] = self.rData.get('totalBuff', 0)
        ret.update(self.extParams)
        desc = self.rData.get('desc', '')
        if type(desc) == str:
            ret['desc'] = (desc,)
        elif type(desc) == tuple:
            ret['desc'] = desc
        else:
            ret['desc'] = ('',)
        tips3 = self.rData.get('tips3', '')
        tips3Title = self.extParams.get('tips3Title', '')
        tips3Desc = self.extParams.get('tips3Desc', '')
        if tips3 and tips3Title and tips3Desc:
            ret['tips3'] = tips3 % (tips3Title, tips3Desc)
        ret['completeFlag'] = self.value >= self.maxValue
        if self.rData.get('funcType', 0) == gametypes.RECOMMEND_TYPE_YOULI:
            ret['completeFlag'] &= self.extParams.get('value1', 0) >= self.extParams.get('maxValue1', 0)
            ret['completeFlag'] &= self.extParams.get('value2', 0) >= self.extParams.get('maxValue2', 0)
        if self.extParams.has_key('seekId'):
            ret['seekId'] = self.extParams['seekId']
        else:
            ret['seekId'] = self.rData.get('seekId', '')
        seekName = self.rData.get('seekName', None)
        if not seekName:
            ret['seekName'] = ''
            ret['seekNum'] = 0
        elif len(seekName) == 1:
            ret['seekName'] = seekName[0]
            ret['seekNum'] = 1
        else:
            ret['seekName'] = seekName
            ret['seekNum'] = len(seekName)
        baoDian = self.rData.get('book', (-1, -1, -1))
        if baoDian == (-1, -1, -1):
            ret['hasBook'] = False
        else:
            ret['mainBookId'] = baoDian[0]
            ret['subBookId'] = baoDian[1]
            ret['bookPageIdx'] = baoDian[2]
            ret['hasBook'] = True
        disParam1 = self.rData.get('displayParam1', '')
        if disParam1.find('%d/%d') >= 0:
            if self.extParams.get('maxValue1', 0):
                ret['disParam1'] = disParam1 % (self.extParams.get('value1', 0), self.extParams.get('maxValue1', 0))
            else:
                ret['disParam1'] = disParam1 % (self.value, self.maxValue)
        else:
            ret['disParam1'] = disParam1
        disParam2 = self.rData.get('displayParam2', '')
        if disParam2.find('%d/%d') >= 0:
            ret['disParam2'] = disParam2 % (self.extParams.get('value2', 0), self.extParams.get('maxValue2', 0))
        else:
            ret['disParam2'] = disParam2
        disParam3 = self.rData.get('displayParam3', '')
        if disParam3.find('%d/%d') >= 0:
            ret['disParam3'] = disParam3 % (self.extParams.get('value3', 0), self.extParams.get('maxValue3', 0))
        elif disParam3.find('%f') >= 0:
            disParam3 = disParam3.replace('%f', '%.1f')
            ret['disParam3'] = disParam3 % (self.extParams.get('value3', 1),)
        else:
            ret['disParam3'] = disParam3
        if self.rData.get('funcType', 0) == gametypes.RECOMMEND_TYPE_YOULI:
            if self.extParams.get('value1', 0) == 0:
                ret['disParam2'] = '尚未接取'
            elif self.value == 0:
                ret['disParam2'] = '上周游历'
            else:
                ret['disParam2'] = '本周游历'
            ret['totalBuff'] = True
        return ret


def _getRecommendFuben(owner, dgroup, rdata, prid, fbData):
    if not fbData:
        return
    fbValue = 0
    fbMaxValue = 0
    lastEnterDays = 0
    extraParam = {}
    coef = 1
    for fbNo, value, maxValue, _lastEnterDays, _coef in fbData:
        fbMaxValue = maxValue
        fbValue = max(value, fbValue)
        lastEnterDays = max(lastEnterDays, _lastEnterDays)
        coef = max(_coef, coef)

    lastEnterDays = min(3, lastEnterDays + 1)
    extraParam['value2'] = lastEnterDays
    extraParam['maxValue2'] = 3
    extraParam['value3'] = coef
    extraParam['maxValue3'] = coef
    ritem = ImportantRecommendItem(prid, rdata.get('name'), fbValue, fbMaxValue, extParams=extraParam, rData=rdata)
    dgroup.append(ritem)


def _getRecommendNormalLoopQuest(owner, dgroup, rdata, prid, questLoopId):
    info = owner.questLoopInfo.get(questLoopId)
    qldata = QLD.data.get(questLoopId)
    if not qldata:
        print 'cf: _getRecommendNormalLoopQuest questLoop not exist', questLoopId
        return
    maxLoopCnt = qldata.get('maxLoopCnt', 0)
    if not info:
        dgroup.append(ImportantRecommendItem(prid, rdata.get('name'), 0, maxLoopCnt, rData=rdata))
    else:
        loopCnt = info.loopCnt
        if info.isYesterday():
            loopCnt = 0
        dgroup.append(ImportantRecommendItem(prid, rdata.get('name'), loopCnt, maxLoopCnt, {}, rData=rdata))


def _getRecommendYouLi(owner, dgroup, rdata, prid, questLoopId):
    extraParam = {}
    info = owner.questLoopInfo.get(questLoopId)
    qldata = QLD.data.get(questLoopId)
    if not qldata:
        print 'cf: _getRecommendYouLi questLoop not exist', questLoopId
        return
    weekSet = rdata.get('weekSet', 0)
    beginTime = rdata.get('beginTime')
    endTime = rdata.get('endTime')
    if beginTime and endTime and not utils.inDateRange(beginTime, endTime, weekSet=weekSet):
        return
    maxLoopCnt = qldata.get('groupNum', 0)
    extraParam['value1'] = 0
    extraParam['maxValue1'] = maxLoopCnt
    extraParam['value2'] = 0
    extraParam['maxValue2'] = 1
    if not info:
        dgroup.append(ImportantRecommendItem(prid, rdata.get('name'), 0, 1, extParams=extraParam, rData=rdata))
    else:
        extraParam['value1'] = len(info.questInfo)
        value = 0
        if info.isYesterday():
            value = 0
        else:
            value = 1
            if len(info.questInfo) == 0:
                if questLoopId in owner.questInfoCache.get('available_taskLoops', []):
                    value = 0
                else:
                    extraParam['value1'] = maxLoopCnt
                    extraParam['value2'] = 1
            else:
                qid, complete = info.questInfo[-1]
                extraParam['value2'] = int(complete)
        dgroup.append(ImportantRecommendItem(prid, rdata.get('name'), value, 1, extParams=extraParam, rData=rdata))


def _getRecommendQumo(owner, dgroup, rdata, prid, activityType):
    qldd = QLD.data
    qdd = QD.data
    for questLoopId, info in owner.questLoopInfo.iteritems():
        qldata = qldd.get(questLoopId)
        if not qldata:
            continue
        if qldata.get('activityType') == activityType:
            info = owner.questLoopInfo.get(questLoopId)
            maxLoopCnt = qldata.get('maxLoopCnt', 0)
            if not info:
                qId = qldd.get(questLoopId, {}).get('quests', [0])[0]
                loopCnt = 0
            else:
                loopCnt = info.loopCnt
                qId = info.getCurrentQuest()
            defShowFirst = rdata.get('showFirstQuestTip', 1)
            available = questLoopId in owner.questInfoCache.get('available_taskLoops', [])
            finishedLoopQuest = False
            if not qId and (defShowFirst or available):
                qId = qldd.get(questLoopId, {}).get('quests', [0])[0]
                if not available:
                    finishedLoopQuest = True
            if not qId:
                continue
            qData = qdd.get(qId, {})
            beginTime = rdata.get('beginTime')
            endTime = rdata.get('endTime')
            weekSet = rdata.get('weekSet', 0)
            params = {}
            params['seekId'] = qData.get('playRecommSeekId', None)
            if not finishedLoopQuest:
                params['tips3Title'] = qData.get('name', None)
                params['tips3Desc'] = qData.get('shortDesc', None)
                params['totalBuff'] = beginTime and endTime and utils.inDateRange(beginTime, endTime, weekSet=weekSet)
            dgroup.append(ImportantRecommendItem(prid, qldata.get('name'), loopCnt, maxLoopCnt, extParams=params, rData=rdata))


def _getRecommendWenQuan(owner, dgroup, rdata, prid):
    ritem = ImportantRecommendItem(prid, rdata.get('name'), rData=rdata)
    ritem.extParams['ranges'] = {}
    for i in range(len(gametypes.RECOMMEND_WENQUAN_FAME)):
        fameId = gametypes.RECOMMEND_WENQUAN_FAME[i]
        ritem.extParams['value' + str(i + 1)] = owner.getFame(fameId)
        ritem.extParams['maxValue' + str(i + 1)] = FD.data.get(fameId).get('maxVal', 0)

    ritem.value = ritem.extParams.get('value1', 0)
    ritem.maxValue = ritem.extParams.get('maxValue1', 0)
    dgroup.append(ritem)


def _getItemUseLimitTime(limitType):
    if limitType == gametypes.ITEM_USE_LIMIT_TYPE_DAY:
        return utils.getDaySecond()
    elif limitType == gametypes.ITEM_USE_LIMIT_TYPE_WEEK:
        return utils.getWeekSecond()
    elif limitType == gametypes.ITEM_USE_LIMIT_TYPE_MONTH:
        return utils.getMonthSecond()
    elif limitType == gametypes.ITEM_USE_LIMIT_TYPE_QUARTER:
        return utils.getQuarterSecond()
    elif limitType == gametypes.ITEM_USE_LIMIT_TYPE_YEAR:
        return utils.getYearInt()
    else:
        return None


def _getRecommendUseItemLimit(owner, dgroup, rdata, prid):
    funcParam = rdata.get('funcParam', ())
    limitType = funcParam and (isinstance(funcParam, list) or isinstance(funcParam, tuple)) and funcParam[0]
    if not limitType:
        limitType = gametypes.ITEM_USE_LIMIT_TYPE_DAY
    history = owner.itemUseHistory.get(funcParam)
    if history:
        t = _getItemUseLimitTime(limitType)
        data = history.get(limitType, (0, 0))
        if t == data[0]:
            value = data[1]
        else:
            value = 0
    else:
        value = 0
    maxValue = 200
    if funcParam and len(funcParam) >= 2 and funcParam[1] == const.USE_LIMIT_LINGSHI_ITEM_GROUP:
        itemList = CRD.data.get(const.USE_LIMIT_LINGSHI_ITEM_GROUP, [])
        if itemList:
            maxValue = min(utils.getUseLimitByLv(itemList[0], owner.lv, limitType, maxValue), maxValue)
    ritem = ImportantRecommendItem(prid, rdata.get('name'), value, maxValue, rData=rdata)
    dgroup.append(ritem)


def _getRecommendSimple(owner, dgroup, rdata, prid, value = 0, maxValue = 0):
    ritem = ImportantRecommendItem(prid, rdata.get('name'), value, maxValue, rData=rdata)
    dgroup.append(ritem)
    return ritem


def _getRecommendActivity(owner, dgroup, rdata, prid):
    beginTime = rdata.get('beginTime')
    endTime = rdata.get('endTime')
    orderBeginTime = rdata.get('orderBeginTime')
    orderEndTime = rdata.get('orderEndTime')
    weekSet = rdata.get('weekSet', 0)
    extraParam = {}
    if not beginTime or not endTime:
        return
    if not utils.inDateRange(beginTime, endTime, weekSet=weekSet):
        return
    playRecommendBlackList = WWCD.data.get('playRecommendBlackList', None)
    enableWorldWar = gameglobal.rds.configData.get('enableWorldWar', False)
    if enableWorldWar and BigWorld.player().worldWar.state != gametypes.WORLD_WAR_STATE_CLOSE and playRecommendBlackList and prid in playRecommendBlackList:
        return
    aState = ASTATE_BEFORE
    dayBegin = '0 0 ' + '%s %s %s' % tuple(beginTime.split()[2:])
    if beginTime != endTime and utils.inCrontabRange(beginTime, endTime):
        aState = ASTATE_PROCESS
        extraParam['leftTime'] = CronTab(endTime).next(utils.getNow())
    elif orderBeginTime and orderEndTime and utils.inCrontabRange(orderBeginTime, orderEndTime):
        aState = ASTATE_ORDER
        extraParam['leftTime'] = CronTab(orderEndTime).next(utils.getNow())
    elif utils.inCrontabRange(dayBegin, beginTime):
        aState = ASTATE_BEFORE
    else:
        aState = ASTATE_AFTER
    actId = rdata.get('funcParam', (0,))
    actId = 0 if not actId else actId[0]
    extraParam['actId'] = actId
    value = int(aState == ASTATE_AFTER)
    maxValue = 1
    ritem = ImportantRecommendItem(prid, rdata.get('name'), value, maxValue, astate=aState, extParams=extraParam, rData=rdata)
    dgroup.append(ritem)


def _getRecommendVip(owner, dgroup, rdata, prid):
    basicPackageLabel = ''
    addedPackageLabel = ''
    hasBasicPackage = False
    hasAddedPackage = False
    if not owner.vipBasicPackage and MCFD.data.get('vipFirstBuyDaysList', {}) and MCFD.data.get('vipFirstBuyBasicPackage', 0):
        basicPackageLabel = rdata.get('displayParam3', '1天币体验7天')
        hasBasicPackage = False
        mid = MCFD.data.get('vipFirstBuyBasicPackage', 0)
    else:
        leftTime = float(owner.vipBasicPackage.get('tExpire', 0) - utils.getNow())
        hasBasicPackage = leftTime > 0
        mid = MCFD.data.get('vipBasicPackage', 0)
        if hasBasicPackage:
            basicPackageLabel = rdata.get('displayParam1', '基础包剩余%d天') % int(max(round(leftTime / const.TIME_INTERVAL_DAY), 1))
    if hasBasicPackage:
        mid = rdata.get('funcParam', (0,))[0]
    addedPackageId = MID.data.get(mid, {}).get('packageID', 0)
    leftTime = float(owner.vipAddedPackage.get(addedPackageId, {}).get('tExpire', 0) - utils.getNow())
    hasAddedPackage = leftTime > 0
    if hasAddedPackage:
        addedPackageLabel = rdata.get('displayParam2', '增值包剩余%d天') % int(max(round(leftTime / const.TIME_INTERVAL_DAY), 1))
    value = hasBasicPackage + hasAddedPackage
    maxValue = 2
    extrParam = {}
    extrParam['hasBasic'] = hasBasicPackage
    extrParam['hasAdded'] = hasAddedPackage
    extrParam['basicLabel'] = basicPackageLabel
    extrParam['addedLabel'] = addedPackageLabel
    extrParam['mallId'] = mid
    extrParam['packageID'] = addedPackageId
    extrParam['itemId'] = MID.data.get(mid, {}).get('itemId', 0)
    extrParam.update(_genBoughtVipPackageInfo(owner, rdata.get('funcParam', (0,))[0]))
    dgroup.append(ImportantRecommendItem(prid, rdata.get('name'), value, maxValue, extParams=extrParam, rData=rdata))


def _genBoughtVipPackageInfo(owner, addedMid):
    ret = {}
    basicPkgId = owner.vipBasicPackage.get('packageID', 0)
    firstMid = MCFD.data.get('vipFirstBuyBasicPackage', 0)
    basicMid = MCFD.data.get('vipBasicPackage', 0)
    if MID.data.get(firstMid, {}).get('packageID', 0) == basicPkgId:
        bMid = firstMid
    else:
        bMid = basicMid
    ret['basicMallId'] = bMid
    ret['basicPackageId'] = basicPkgId
    ret['basicItemId'] = MID.data.get(bMid, {}).get('itemId', 0)
    ret['addedMallId'] = addedMid
    ret['addedPackageId'] = MID.data.get(addedMid, {}).get('packageID', 0)
    ret['addedItemId'] = MID.data.get(addedMid, {}).get('itemId', 0)
    return ret


def _genRecommendItems(owner, filter = None):
    result = {}
    iprdd = IPRD.data
    for prid, rdata in iprdd.iteritems():
        rType = rdata.get('type', 1)
        dgroup = result.setdefault(rType, [])
        if utils.getEnableCheckServerConfig():
            serverConfigId = rdata.get('serverConfigId', 0)
            if serverConfigId and not utils.checkInCorrectServer(serverConfigId):
                continue
        if filter != None:
            if rType not in filter:
                continue
        if rdata.get('lv'):
            minlv, maxlv = rdata.get('lv')
            if owner.lv < minlv or owner.lv > maxlv:
                continue
        if gameglobal.rds.loginManager.serverMode() == gametypes.SERVER_MODE_NOVICE:
            if rdata.get('hideInNovice', 0):
                continue
        funcType = rdata.get('funcType')
        funcParam = rdata.get('funcParam')
        if funcType == gametypes.RECOMMEND_TYPE_FUBEN:
            _getRecommendFuben(owner, dgroup, rdata, prid, owner.importantPlayRecommendInfo.get(prid))
        elif funcType == gametypes.RECOMMEND_TYPE_NORMAL_QUEST_LOOP:
            _getRecommendNormalLoopQuest(owner, dgroup, rdata, prid, *funcParam)
        elif funcType == gametypes.RECOMMEND_TYPE_YOULI:
            _getRecommendYouLi(owner, dgroup, rdata, prid, *funcParam)
        elif funcType == gametypes.RECOMMEND_TYPE_QUMO:
            _getRecommendQumo(owner, dgroup, rdata, prid, *funcParam)
        elif funcType == gametypes.RECOMMEND_TYPE_USE_ITEM_LIMIT:
            _getRecommendUseItemLimit(owner, dgroup, rdata, prid)
        elif funcType == gametypes.RECOMMEND_TYPE_DIGONG:
            curNum, allNum = gameglobal.rds.ui.player.getKillMonsterNum()
            _getRecommendSimple(owner, dgroup, rdata, prid, curNum, allNum)
        elif funcType == gametypes.RECOMMEND_TYPE_WENQUAN:
            _getRecommendWenQuan(owner, dgroup, rdata, prid)
        elif funcType == gametypes.RECOMMEND_TYPE_ACTIVITY:
            _getRecommendActivity(owner, dgroup, rdata, prid)
        elif funcType == gametypes.RECOMMEND_TYPE_VIP:
            _getRecommendVip(owner, dgroup, rdata, prid)

    return result


def getRecommendInfo(owner, rFilter = None):
    result = _genRecommendItems(owner, rFilter)
    for dgroup in result.itervalues():
        dgroup.sort(key=lambda x: x.order)

    formatResult = {}
    for rType, dgroup in result.iteritems():
        formatResult[rType] = [ rItem.formatReturn() for rItem in dgroup ]

    return formatResult


def incompleteItemsNum(owner):
    filter = PRCD.data.get('importantPushTypes', ())
    result = _genRecommendItems(owner, filter)
    inCompleteNum = 0
    allNum = 0
    for dgroup in result.itervalues():
        for iItem in dgroup:
            inCompleteNum += iItem.value < iItem.maxValue
            allNum += 1

    return (inCompleteNum, allNum)


def inCompleteItemsNotifyCheck(owner):
    inCompleteNum, allNum = incompleteItemsNum(owner)
    return 100 * inCompleteNum / max(allNum, 1)
