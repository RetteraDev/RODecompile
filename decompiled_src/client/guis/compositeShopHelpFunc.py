#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/compositeShopHelpFunc.o
from gamestrings import gameStrings
import BigWorld
import utils
import const
import gametypes
import commShop
import uiUtils
import gameglobal
import pubgUtils
from item import Item
from guis import ui
from gameStrings import gameStrings
from cdata import game_msg_def_data as GMDD
from cdata import composite_shop_trade_data as CSTD
from data import item_data as ID
from data import fame_data as FD
from data import sys_config_data as SCD
from data import jingjie_data as JJD
from data import junjie_config_data as JJCD
from data import juewei_data as JD
from data import school_data as SD
from data import qiren_clue_data as QCD
from data import qiren_role_data as QRD
from data import famous_general_lv_data as FGLD
from data import server_progress_data as SPD
MAOXIANJIA_FAMEID = 410
DIJIA_ITEM_TO_FAME = 0
DIJIA_ITEM_TO_ITEM = 1
YUNCHUI_FAME_ID = 453
LV_LIMIT_INDEX_LOWER_IDX = 0
LV_LIMIT_INDEX_UPPER_IDX = 1
LV_NO_LIMIT_VALUE = -1
ITEM_MAX_SHOW_CNT = 999

def getConsumeInfo(compositeId, buyItemNum, diJiaItemNum, diJiaItemToItemNum, isAddFameInfoToConditionList = False):
    compositeData = CSTD.data.get(compositeId, {})
    if not compositeData:
        return
    p = BigWorld.player()
    itemNum = buyItemNum if buyItemNum > 0 else 1
    consumeItem, consumeFame, consumeDiJia = commShop._calcCompositeShopConsumeInfo(p, compositeData, itemNum, diJiaItemNum, diJiaItemToItemNum, True)
    consumeItemInfo = {}
    conditionList = []
    isValid, limitedInfo = getLimitedInfo(compositeData)
    conditionList.extend(limitedInfo)
    isValid, costItemInfo, costItemList = getCostItemInfo(consumeItem, compositeData, isValid)
    conditionList.extend(costItemInfo)
    cfgDijiaFameLis = getCfgDijiaFameList(compositeData)
    fameInfo, isValid = getFameInfo(compositeData, consumeFame, isValid, conditionList, cfgDijiaFameLis, isAddFameInfoToConditionList)
    guildInfo, juqingInfo, consumeCash, consumeBindCash, isValid = getOtherInfo(compositeData, isValid, buyItemNum)
    conditionList.extend(guildInfo)
    conditionList.extend(juqingInfo)
    diJiaInfo, isValid = getDiJiaInfo(compositeData, consumeDiJia, costItemList, isValid, buyItemNum)
    consumeItemInfo['fameInfo'] = fameInfo
    consumeItemInfo['consumeDiJiaInfo'] = diJiaInfo
    consumeItemInfo['conditionList'] = conditionList
    consumeItemInfo['consumeCash'] = consumeCash
    discountRate = compositeData.get('discountRate', 0)
    costTianBi = compositeData.get('consumeCoin', 0)
    consumeItemInfo['tianBi'] = commShop._applyDiscount(costTianBi, discountRate)
    consumeItemInfo['consumeBindCash'] = consumeBindCash
    consumeItemInfo['playerCash'] = p.cash
    consumeItemInfo['playerBindCash'] = p.bindCash
    consumeItemInfo['isValid'] = isValid
    consumeItemInfo['count'] = buyItemNum
    consumeItemInfo['fameCash'] = str(p.fame.get(YUNCHUI_FAME_ID, 0))
    consumeItemInfo['compositeId'] = compositeId
    return consumeItemInfo


def hasDiJiaInfo(compositeId):
    compositeData = CSTD.data.get(compositeId, {})
    if _getDijiaItemId(compositeData):
        return True
    else:
        return False


def hasLvMaxLimit(lvLimit):
    return lvLimit[LV_LIMIT_INDEX_LOWER_IDX] == LV_NO_LIMIT_VALUE


def hasLvMinLimit(lvLimit):
    return lvLimit[LV_LIMIT_INDEX_UPPER_IDX] == LV_NO_LIMIT_VALUE


def getOtherInfo(compositeData, isValid, buyItemNum):
    p = BigWorld.player()
    guildInfo = []
    juqingInfo = []
    if compositeData.has_key('consumeContrib'):
        fameName = gameStrings.TEXT_CONST_8340
        consumeContrib = compositeData['consumeContrib'] * buyItemNum
        isGuildContributionValid = p.guildContrib >= consumeContrib
        guildInfo.append([fameName, isGuildContributionValid, format(p.guildContrib, ',') + '/' + format(consumeContrib, ',')])
        isValid = isValid and isGuildContributionValid
    if compositeData.has_key('needClue'):
        needClue = compositeData['needClue']
        desc = compositeData.get('clueDesc', '')
        finished = all([ p.getClueFlag(cid) for cid in needClue ])
        if not desc:
            roleId = QCD.data.get(needClue[0], {}).get('pushRoleId')
            role = QRD.data.get(roleId, {}).get('name', '')
            desc = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_108 % role
        juqingInfo.append([desc, finished, ''])
        isValid = isValid and finished
    consumeCash, consumeBindCash, coin = _calcConsumeCash(compositeData, buyItemNum)
    consumeCashType = compositeData.get('cashType', gametypes.CONSUME_CASH_TYPE_NO_LIMIT)
    if consumeCashType == gametypes.CONSUME_CASH_TYPE_NO_LIMIT:
        if p.cash + p.bindCash < consumeCash + consumeBindCash:
            isValid = False
    elif consumeCashType == gametypes.CONSUME_CASH_TYPE_BIND_CASH:
        if p.bindCash < consumeBindCash:
            isValid = False
    elif consumeCashType == gametypes.CONSUME_CASH_TYPE_CASH:
        if p.cash < consumeCash:
            isValid = False
    if p.getTianBi() < coin:
        isValid = False
    return (guildInfo,
     juqingInfo,
     consumeCash,
     consumeBindCash,
     isValid)


def buyItem(shopId, item, itemNum, diJiaItemCount, diJiaItem2ItemCount, page, pos, npcEnt = None):
    p = BigWorld.player()
    itemId = item.id
    wrapNum = Item.maxWrap(itemId)
    judge = (1, wrapNum, GMDD.data.ITEM_TRADE_NUM)
    if not ui.inputRangeJudge(judge, itemNum, (wrapNum,)):
        return
    if itemNum > Item.maxWrap(itemId):
        p.showGameMsg(GMDD.data.SHOP_BUY_ITEM_OVER_MWRAP, ())
        return
    buyIt = Item(itemId, cwrap=itemNum, genRandProp=False)
    if ID.data.get(buyIt.id, {}).get('needOwner'):
        buyIt.setOwner(p.gbId, p.realRoleName)
    if Item.isDotaBattleFieldItem(itemId):
        invPage, invPos = p.battleFieldBag.searchBestInPages(itemId, itemNum, buyIt)
    elif Item.isQuestItem(itemId):
        invPage, invPos = p.questBag.searchBestInPages(itemId, itemNum, buyIt)
    elif p._isInCross():
        if gameglobal.rds.configData.get('enableWingWorld', False):
            invPage, invPos = p.crossInv.searchBestInPages(itemId, itemNum, buyIt)
    else:
        invPage, invPos = p.inv.searchBestInPages(itemId, itemNum, buyIt)
    if invPage == const.CONT_NO_PAGE or invPos == const.CONT_NO_POS:
        p.showGameMsg(GMDD.data.SHOP_BAG_FULL, ())
        return
    compositeId = item.compositeId
    if not CSTD.data.has_key(compositeId):
        return False
    compositeData = CSTD.data.get(compositeId, {})
    if not commShop._checkCompositeShopPreLimit(p, compositeData, itemNum):
        p.showGameMsg(GMDD.data.COMPOSITE_SHOP_BUY_FORBIDDEN_PRE_LIMIT, ())
        return
    if not _checkdiJiaItem(compositeData, diJiaItemCount, diJiaItem2ItemCount):
        return
    if not compositeData.get('diJiaItemid'):
        diJiaItemCount = 0
    if not compositeData.get('diJiaSrcItemId'):
        diJiaItem2ItemCount = 0
    if not commShop._checkBuyItemConsume(p, compositeData, itemNum, diJiaItemCount, diJiaItem2ItemCount):
        p.showGameMsg(GMDD.data.COMPOSITE_SHOP_BUY_FORBIDDEN_MATERIAL_SHORTAGE, ())
        return
    if compositeData.has_key('lvLimit'):
        lvLimit = compositeData['lvLimit']
        if hasLvMaxLimit(lvLimit):
            if p.lv > lvLimit[LV_LIMIT_INDEX_UPPER_IDX]:
                return
        elif hasLvMinLimit(lvLimit):
            if p.lv < lvLimit[LV_LIMIT_INDEX_LOWER_IDX]:
                return
        elif p.lv < lvLimit[LV_LIMIT_INDEX_LOWER_IDX] or p.lv > lvLimit[LV_LIMIT_INDEX_UPPER_IDX]:
            return
    diJiaItemId = _getDijiaItemId(compositeData)
    if diJiaItemCount != 0 or diJiaItem2ItemCount != 0:
        diJiaItemPage, diJiaItemPos = BigWorld.player().inv.findItemInPages(diJiaItemId, enableParentCheck=True, includeExpired=True, includeLatch=True, includeShihun=True)
        if diJiaItemPage == const.CONT_NO_PAGE or diJiaItemPos == const.CONT_NO_POS:
            return
    else:
        diJiaItemPage, diJiaItemPos = (0, 0)
    if p.getPrivateShop(shopId):
        p.base.buyPrivateShopItem(shopId, page, pos, itemNum, invPage, invPos, diJiaItemPage, diJiaItemPos, diJiaItemCount, diJiaItem2ItemCount)
        return True
    if npcEnt:
        npcEnt.cell.compositeShopSell(shopId, page, pos, itemNum, invPage, invPos, diJiaItemPage, diJiaItemPos, diJiaItemCount, diJiaItem2ItemCount)
        return True
    gameglobal.rds.sound.playSound(gameglobal.SD_26)


def _checkdiJiaItem(compositeData, diJiaItemNum, diJiaItemToItemNum):
    diJiaType = _getDijiaType(compositeData)
    if diJiaType == DIJIA_ITEM_TO_FAME and diJiaItemNum == 0:
        return True
    if diJiaType == DIJIA_ITEM_TO_ITEM and diJiaItemToItemNum == 0:
        return True
    p = BigWorld.player()
    diJiaItemId = _getDijiaItemId(compositeData)
    if diJiaItemId == 0:
        return True
    curCnt = p.inv.countItemInPages(diJiaItemId, enableParentCheck=True)
    if diJiaItemNum > curCnt:
        p.showGameMsg(GMDD.data.COMPOSITE_SHOP_BUY_FORBIDDEN_DIJIA_ITEM_NUM, ())
        return False
    return True


def _getDijiaItemId(compositeData):
    if not compositeData:
        return 0
    diJiaType = _getDijiaType(compositeData)
    if diJiaType == DIJIA_ITEM_TO_FAME:
        return compositeData.get('diJiaItemid', 0)
    if diJiaType == DIJIA_ITEM_TO_ITEM:
        return compositeData.get('diJiaSrcItemId', 0)


def _getDijiaType(compositeData):
    if not compositeData:
        return DIJIA_ITEM_TO_ITEM
    diJiaItemid = compositeData.get('diJiaItemid', 0)
    diJiaSrcItemid = compositeData.get('diJiaSrcItemId', 0)
    if diJiaItemid > 0:
        return DIJIA_ITEM_TO_FAME
    if diJiaSrcItemid > 0:
        return DIJIA_ITEM_TO_ITEM
    return DIJIA_ITEM_TO_FAME


def getFameInfo(compositeData, consumeFame, isValid, conditionLsit, diJiaFame, isAddFameInfoToConditionList):
    p = BigWorld.player()
    diJiaType = _getDijiaType(compositeData)
    fameInfo = []
    for fameId, fameNum in consumeFame:
        fameName = FD.data.get(fameId, {}).get('name', '')
        curFameNum = p.fame.get(fameId, 0)
        fameValid = curFameNum >= fameNum
        isValid = isValid and fameValid
        if isAddFameInfoToConditionList:
            cntStr = '%s/%s' % (format(curFameNum, ','), format(fameNum, ','))
        else:
            cntStr = format(fameNum, ',')
        addItem = [fameName, fameValid, cntStr]
        if isAddFameInfoToConditionList:
            conditionLsit.append(addItem)
        fameInfo.append(addItem)
        if diJiaType == DIJIA_ITEM_TO_FAME and diJiaFame and diJiaFame[0][0] == fameId:
            conditionLsit.append(['addDijia', True, ''])

    return (fameInfo, isValid)


def _getFameLv(fameId, fameVal):
    fameLv, maxLv, curFame, maxFame, extra = gameglobal.rds.ui.roleInfoFame.getFameLv(fameId, fameVal, True)
    return (fameLv, extra)


def getLimitedInfo(compositeData):
    p = BigWorld.player()
    consumeItemInfo = []
    isValid = True
    if compositeData.has_key('lvLimit'):
        lvLimit = compositeData['lvLimit']
        if hasLvMaxLimit(lvLimit):
            itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_289 % lvLimit[LV_LIMIT_INDEX_UPPER_IDX]
            isLvValid = isValid and p.realLv <= lvLimit[LV_LIMIT_INDEX_UPPER_IDX]
            consumeItemInfo.append([itemName, isLvValid, ''])
        elif hasLvMinLimit(lvLimit):
            itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_293 % lvLimit[LV_LIMIT_INDEX_LOWER_IDX]
            isLvValid = p.realLv >= lvLimit[LV_LIMIT_INDEX_LOWER_IDX]
            consumeItemInfo.append([itemName, isLvValid, ''])
        else:
            itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_297 % (lvLimit[LV_LIMIT_INDEX_LOWER_IDX], lvLimit[LV_LIMIT_INDEX_UPPER_IDX])
            isLvValid = p.realLv >= lvLimit[LV_LIMIT_INDEX_LOWER_IDX] and p.realLv <= lvLimit[LV_LIMIT_INDEX_UPPER_IDX]
            consumeItemInfo.append([itemName, isLvValid, ''])
        isValid = isValid and isLvValid
    if compositeData.has_key('sexLimit'):
        sexLimit = compositeData['sexLimit']
        itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_303 % (const.SEX_NAME[sexLimit],)
        isSexValid = p.realPhysique.sex == sexLimit
        consumeItemInfo.append([itemName, isSexValid, ''])
        isValid = isValid and isSexValid
    if compositeData.has_key('arenaScoreLimit'):
        arenaScoreLimit = compositeData['arenaScoreLimit']
        itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_310 % (arenaScoreLimit,)
        isArenaValid = p.arenaInfo.arenaScore >= arenaScoreLimit
        consumeItemInfo.append([itemName, isArenaValid, ''])
        isValid = isValid and isArenaValid
    if compositeData.has_key('qumoLimit'):
        qumoLimit = compositeData['qumoLimit']
        itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_317 % (qumoLimit,)
        isQumoValid = p.qumoLv >= qumoLimit
        consumeItemInfo.append([itemName, isQumoValid, ''])
        isValid = isValid and isQumoValid
    if compositeData.has_key('shopJingJieRequire'):
        jingJieLimit = compositeData['shopJingJieRequire']
        jingJieName = JJD.data.get(jingJieLimit, {}).get('name', gameStrings.TEXT_COMPOSITESHOPHELPFUNC_324)
        itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_325 % (jingJieName,)
        isJingJieValid = p.jingJie >= jingJieLimit
        consumeItemInfo.append([itemName, isJingJieValid, ''])
        isValid = isValid and isJingJieValid
    if compositeData.has_key('needJunJieLv'):
        junJieLvLimit = compositeData['needJunJieLv']
        junJieName = JJCD.data.get(junJieLvLimit, {}).get('name', gameStrings.TEXT_COMPOSITESHOPHELPFUNC_324)
        itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_333 % (junJieName,)
        isJunJieValid = p.junJieLv >= junJieLvLimit
        consumeItemInfo.append([itemName, isJunJieValid, ''])
        isValid = isValid and isJunJieValid
    if compositeData.has_key('needJueWeiLv'):
        jueWeiLvLimit = compositeData['needJueWeiLv']
        jueWeiName = JD.data.get(jueWeiLvLimit, {}).get('name', gameStrings.TEXT_COMPOSITESHOPHELPFUNC_324)
        itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_341 % (jueWeiName,)
        isJueWeiValid = p.jueWeiLv >= jueWeiLvLimit
        consumeItemInfo.append([itemName, isJueWeiValid, ''])
        isValid = isValid and isJueWeiValid
    if compositeData.has_key('schoolLimit'):
        schLimit = compositeData['schoolLimit']
        schoolNames = ''
        for school in schLimit:
            schoolNames += SD.data.get(school, {}).get('name', gameStrings.TEXT_GAME_1747) + ' '

        itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_351 % schoolNames
        isSchoolValid = p.realSchool in schLimit
        consumeItemInfo.append([itemName, isSchoolValid, ''])
        isValid = isValid and isSchoolValid
    if compositeData.has_key('appearanceItemPointLimit'):
        appearanceItemPointLimit = compositeData['appearanceItemPointLimit']
        itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_358 % (appearanceItemPointLimit,)
        isAppearanceItemCollectPointValid = p.appearanceItemCollectPoint >= appearanceItemPointLimit
        consumeItemInfo.append([itemName, isAppearanceItemCollectPointValid, ''])
        isValid = isValid and isAppearanceItemCollectPointValid
    if compositeData.has_key('delegationRank'):
        maoxianFameLv = compositeData['delegationRank']
        maoxianFameName = FD.data.get(MAOXIANJIA_FAMEID, {}).get('lvDesc')[maoxianFameLv]
        itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_366 % (maoxianFameName,)
        isDelegationRankValid = p.delegationRank >= maoxianFameLv
        consumeItemInfo.append([itemName, isDelegationRankValid, ''])
        isValid = isValid and isDelegationRankValid
    if compositeData.has_key('wingWorldZhanXunRank'):
        rankMin, rankMax = compositeData.get('wingWorldZhanXunRank', (1, 100))
        itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_373 % (rankMin, rankMax)
        isZhanXunRankValid = rankMin <= p.wingWorldZhanXunRankInLastWeek <= rankMax
        consumeItemInfo.append([itemName, isZhanXunRankValid, ''])
        isValid = isValid and isZhanXunRankValid
    if compositeData.has_key('needFamousGeneralLv'):
        needFamousGeneralLv = compositeData.get('needFamousGeneralLv', 0)
        isFamousLvReached = p.famousGeneralLv >= needFamousGeneralLv
        itemName = gameStrings.COMPOSITE_SHOP_FAMOUS_LV_REQUIRE % FGLD.data.get(needFamousGeneralLv, {}).get('name', '')
        consumeItemInfo.append([itemName, isFamousLvReached, ''])
        isValid = isValid and isFamousLvReached
    if compositeData.has_key('spIdLimit'):
        spId = compositeData.get('spIdLimit', 0)
        isCompleted = p.isServerProgressFinished(spId)
        consumeItemInfo.append([SPD.data.get(spId, {}).get('description', ''), isCompleted, ''])
        isValid = isValid and isCompleted
    if compositeData.has_key('progressLimit'):
        progressLevel = compositeData.get('progressLimit')
        itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_393 % progressLevel
        isProgressLevelReached = p.curEndlessMaxProgress >= progressLevel
        consumeItemInfo.append([itemName, isProgressLevelReached, '%d/%d' % (p.curEndlessMaxProgress, progressLevel)])
        isValid = isValid and isProgressLevelReached
    if compositeData.has_key('spriteChallengeProgressLimit'):
        scProgressLimit = compositeData.get('spriteChallengeProgressLimit')
        itemName = gameStrings.COMPOSITE_SHOP_SPRITE_PROGRESS % scProgressLimit
        isSCProgressLevelReached = p.curSpriteChallengeMaxProgress >= scProgressLimit
        consumeItemInfo.append([itemName, isSCProgressLevelReached, '%d/%d' % (p.curSpriteChallengeMaxProgress, scProgressLimit)])
        isValid = isValid and isSCProgressLevelReached
    if compositeData.has_key('zmjStarBossLayerLimit'):
        layerLimit = compositeData.get('zmjStarBossLayerLimit', 0)
        killRecord = p._getZMJData(const.ZMJ_FB_INFO_STAR_BOSS_RECORD, {})
        layer = killRecord and max(killRecord.keys()) or 0
        if layerLimit > 0:
            itemName = gameStrings.ZMJ_STAR_BOSS_LAYER_LIMIT % layerLimit
            isSCProgressLevelReached = layer >= layerLimit
            consumeItemInfo.append([itemName, isSCProgressLevelReached, ''])
            isValid = isValid and isSCProgressLevelReached
    if compositeData.has_key('fameLimit'):
        fameLimit = compositeData['fameLimit']
        for fameId, fameNum in fameLimit:
            fd = FD.data.get(fameId, {})
            if not fd or fd.has_key('lvDesc'):
                continue
            fameLv, extraFame = _getFameLv(fameId, fameNum)
            fameName = fd.get('shopTips', '')
            schoolFame = fd.get('schoolFame', 0)
            if schoolFame:
                if schoolFame == p.school:
                    fameLvName = SCD.data.get('selfSchoolFameLvName', {}).get(schoolFame, {}).get(fameLv, '')
                else:
                    fameLvName = SCD.data.get('otherSchoolFameLvName', {}).get(schoolFame, {}).get(fameLv, '')
                fameName = fd.get('name', '')
            else:
                fameLvName = SCD.data.get('fameLvName', {}).get(fameLv, '')
            showFameLimitVal = compositeData.get('showFameLimitVal', 0)
            if showFameLimitVal:
                fameLvName = str(fameNum)
                fameName = fd.get('name', '')
            if fameLvName == '':
                continue
            if extraFame <= 0 or showFameLimitVal:
                itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_443 % (fameName, fameLvName)
            else:
                extraFame = str(extraFame)
                itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_446 % (fameName, fameLvName, extraFame)
            if schoolFame:
                schoolFameLv = gameglobal.rds.ui.roleInfoFame.getFameLv(fameId)[0]
                isFameValid = schoolFameLv >= fameLv
            else:
                isFameValid = p.getFame(fameId) >= fameNum
            consumeItemInfo.append([itemName, isFameValid, ''])
            isValid = isValid and isFameValid

    if compositeData.has_key('pubgRankPointsLimit'):
        pubgRankPointsLvLimit = compositeData.get('pubgRankPointsLimit', 0)
        if pubgRankPointsLvLimit > 0:
            pubgRankPointsLimitData = p.getRankDataInPUBGByLv(pubgRankPointsLvLimit)
            playerRankPointsLv = p.getRankLvInPUBGByRankPoint(p.pubgRankPoints)
            itemName = gameStrings.PUBG_COMPOSITE_SHOP_RANK_POINTS_LIMIT_DES % pubgRankPointsLimitData.get('des', gameStrings.PUBG_PVP_BATTLE_FIELD_V2_RANK_DEFAULT_DES)
            isPlayerRankPointLvReached = playerRankPointsLv >= pubgRankPointsLvLimit
            consumeItemInfo.append([itemName, isPlayerRankPointLvReached, ''])
            isValid = isValid and isPlayerRankPointLvReached
    return (isValid, consumeItemInfo)


def getMaxBuyCnt(item):
    count = ITEM_MAX_SHOW_CNT if item.remainNum == const.ITEM_NUM_INFINITE else item.remainNum
    remainCnt = getCompositeRemainBuyCount(item)
    if remainCnt >= 0:
        maxCnt = max(1, min(count, remainCnt))
    else:
        maxCnt = max(1, count)
    maxCnt = min(Item.maxWrap(item.id), maxCnt)
    return maxCnt


def getConsumeMaxNum(item):
    if not item:
        return 0
    p = BigWorld.player()
    compositeData = CSTD.data.get(item.compositeId, {})
    consumeItem, consumeFame, _ = commShop._calcCompositeShopConsumeInfo(p, compositeData, 1, 0, 0, False)
    ret = ITEM_MAX_SHOW_CNT if item.remainNum == const.ITEM_NUM_INFINITE else item.remainNum
    if ret == const.ITEM_NUM_INFINITE:
        ret = ITEM_MAX_SHOW_CNT
    for itemId, itemNum in consumeItem:
        curItemNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
        ret = min(curItemNum / itemNum, ret)

    for fameId, fameNum in consumeFame:
        curFameNum = p.fame.get(fameId, 0)
        ret = min(curFameNum / fameNum, ret)

    if compositeData.has_key('consumeContrib'):
        consumeContrib = compositeData['consumeContrib']
        ret = min(p.guildContrib / consumeContrib, ret)
    consumeCash, consumeBindCash, coin = _calcConsumeCash(compositeData, 1)
    if coin > 0:
        ret = min(p.getTianBi() / coin, ret)
    consumeCashType = compositeData.get('cashType', gametypes.CONSUME_CASH_TYPE_NO_LIMIT)
    if consumeCashType == gametypes.CONSUME_CASH_TYPE_NO_LIMIT and (consumeCash > 0 or consumeBindCash > 0):
        ret = min((p.cash + p.bindCash) / (consumeCash + consumeBindCash), ret)
    elif consumeCashType == gametypes.CONSUME_CASH_TYPE_BIND_CASH and consumeBindCash > 0:
        ret = min(p.bindCash / consumeBindCash, ret)
    elif consumeCashType == gametypes.CONSUME_CASH_TYPE_CASH and consumeCash > 0:
        ret = min(p.cash / consumeCash, ret)
    buyLimitType = CSTD.data.get(item.compositeId, {}).get('buyLimitType', 0)
    if buyLimitType != const.COMPOSITE_BUY_LIMIT_TYPE_NO:
        remainBuyCount = max(0, getCompositeRemainBuyCount(item))
        ret = min(item.mwrap, ret, remainBuyCount)
    else:
        ret = min(item.mwrap, ret)
    if ret == 0:
        ret = 1
    return ret


def _calcConsumeCash(compositeData, buyNum = 0):
    cash = 0
    bindCash = 0
    coin = compositeData.get('consumeCoin', 0)
    discountRate = compositeData.get('discountRate', 1)
    coin *= buyNum
    coin *= discountRate
    consumeCash = compositeData.get('consumeCash', 0)
    if consumeCash == 0 and coin:
        return (cash, bindCash, coin)
    consumeCashType = compositeData.get('cashType', gametypes.CONSUME_CASH_TYPE_NO_LIMIT)
    consumeCash *= buyNum
    p = BigWorld.player()
    if consumeCashType == gametypes.CONSUME_CASH_TYPE_NO_LIMIT:
        bindCash = min(consumeCash, p.bindCash)
        cash = max(consumeCash - bindCash, 0)
    elif consumeCashType == gametypes.CONSUME_CASH_TYPE_BIND_CASH:
        bindCash = consumeCash
    elif consumeCashType == gametypes.CONSUME_CASH_TYPE_CASH:
        cash = consumeCash
    return (cash, bindCash, coin)


def getCompositeRemainBuyCount(shopItem):
    p = BigWorld.player()
    dataKey = _getCompositeItemLimitKey(shopItem.compositeId)
    if dataKey not in p.compositeShopItemBuyLimit:
        buyCount = 0
        lastBuyTime = 0
    else:
        buyCount, lastBuyTime = p.compositeShopItemBuyLimit[dataKey]
    buyLimitType = CSTD.data.get(shopItem.compositeId, {}).get('buyLimitType', 0)
    buyLimitCount = CSTD.data.get(shopItem.compositeId, {}).get('buyLimitCount', -1)
    if lastBuyTime:
        samePeriod = False
        now = utils.getNow()
        if buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_DAY:
            samePeriod = utils.isSameDay(lastBuyTime, now)
        elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_WEEK:
            samePeriod = utils.isSameWeek(lastBuyTime, now)
        elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_MONTH:
            samePeriod = utils.isSameMonth(lastBuyTime, now)
        elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_FOREVER:
            samePeriod = True
        elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_FAMOUS_GENERAL_SEASON:
            samePeriod = utils.inCurrentFamousGeneralSeason(lastBuyTime)
        elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_ENDLESS_CHALLENGE_SEASON:
            samePeriod = utils.isSameEndlessChallengeSeason(lastBuyTime)
        elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_SPRITE_CHALLENGE_SEASON:
            samePeriod = utils.isSameSpriteChallengeSeason(lastBuyTime)
        elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_PUBG_SEASON:
            samePeriod = pubgUtils.isSamePubgSeason(now, lastBuyTime)
        if not samePeriod:
            buyCount = 0
    return buyLimitCount - buyCount


def _getCompositeItemLimitKey(compositeId):
    compositeData = CSTD.data[compositeId]
    if 'buyLimitGroup' in compositeData:
        return 'g%d' % (compositeData['buyLimitGroup'],)
    else:
        return 'i%d' % (compositeId,)


def getCostItemInfo(consumeItem, compositeData, isValid):
    p = BigWorld.player()
    costItemInfo = []
    diJiaType = _getDijiaType(compositeData)
    tgtDiJiaItemId = compositeData.get('diJiaTargetItemId', 0)
    costItemList = {}
    for itemId, itemNum in consumeItem:
        if not itemId:
            continue
        itemName = ID.data.get(itemId, {}).get('name', '')
        if itemId in costItemList:
            curItemNum = costItemList[itemId]
        else:
            curItemNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
            if curItemNum - itemNum < 0:
                costItemList[itemId] = 0
            else:
                costItemList[itemId] = curItemNum - itemNum
        if curItemNum >= itemNum:
            costItemInfo.append([itemName,
             True,
             str(curItemNum) + '/' + str(itemNum),
             itemId])
        else:
            costItemInfo.append([itemName,
             False,
             str(curItemNum) + '/' + str(itemNum),
             itemId])
            isValid = False
        if diJiaType == DIJIA_ITEM_TO_ITEM and itemId == tgtDiJiaItemId:
            costItemInfo.append(['addDijia', True, ''])

    return (isValid, costItemInfo, costItemList)


def _getDijiaType(compositeData):
    if not compositeData:
        return DIJIA_ITEM_TO_ITEM
    diJiaItemid = compositeData.get('diJiaItemid', 0)
    diJiaSrcItemid = compositeData.get('diJiaSrcItemId', 0)
    if diJiaItemid > 0:
        return DIJIA_ITEM_TO_FAME
    if diJiaSrcItemid > 0:
        return DIJIA_ITEM_TO_ITEM
    return DIJIA_ITEM_TO_FAME


def getCfgDijiaFameList(compositeData):
    diJiaType = _getDijiaType(compositeData)
    if diJiaType == DIJIA_ITEM_TO_FAME:
        return compositeData.get('diJiaFame', [])
    return []


def getDiJiaInfo(compositeData, consumeDiJia, costItemList, isValid, buyItemNum):
    p = BigWorld.player()
    diJiaItemId = _getDijiaItemId(compositeData)
    diJiaType = _getDijiaType(compositeData)
    cfgDiJiaFameList = getCfgDijiaFameList(compositeData)
    tgtDiJiaItemId = compositeData.get('diJiaTargetItemId', 0)
    if diJiaType == DIJIA_ITEM_TO_FAME:
        diJiaItemMaxNum = compositeData.get('diJiaItemMaxNum', 0)
    elif diJiaType == DIJIA_ITEM_TO_ITEM:
        diJiaItemMaxNum = compositeData.get('diJiaSrcMaxNum', 0)
    else:
        diJiaItemMaxNum = 0
    consumeDiJiaInfo = {}
    if diJiaItemMaxNum:
        diJiaItemNum = consumeDiJia[1] if consumeDiJia else 0
        diJiaItemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_660 % ID.data.get(diJiaItemId, {}).get('name', '')
        if diJiaItemId in costItemList:
            curItemNum = costItemList[diJiaItemId]
        else:
            curItemNum = p.inv.countItemInPages(diJiaItemId, enableParentCheck=True)
            if curItemNum - diJiaItemNum < 0:
                costItemList[diJiaItemId] = 0
            else:
                costItemList[diJiaItemId] = curItemNum - diJiaItemNum
        if curItemNum >= diJiaItemNum:
            diJiaDesc1 = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_670 % diJiaItemName
            diJiaNumStr = '%d/%d' % (curItemNum, diJiaItemNum)
        else:
            diJiaDesc1 = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_670 % uiUtils.toHtml(diJiaItemName, '#D9482B')
            diJiaNumStr = uiUtils.toHtml('%d/%d' % (curItemNum, diJiaItemNum), '#D9482B')
            isValid = False
        if diJiaType == DIJIA_ITEM_TO_FAME and cfgDiJiaFameList:
            diJiaDesc2 = ''
            for fameId, fameNum in cfgDiJiaFameList:
                if diJiaDesc2 != '':
                    diJiaDesc2 += '<br>'
                diJiaDesc2 += gameStrings.TEXT_COMPOSITESHOPHELPFUNC_682 % (1, FD.data.get(fameId, {}).get('name', ''), fameNum)

        elif diJiaType == DIJIA_ITEM_TO_ITEM:
            diJiaDesc2 = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_682 % (compositeData.get('diJiaSrcItemNum', 0), ID.data.get(tgtDiJiaItemId, {}).get('name', ''), compositeData.get('diJiaTargetItemNum', 0))
        else:
            diJiaDesc2 = ''
        consumeDiJiaInfo['curNum'] = curItemNum
        consumeDiJiaInfo['itemNum'] = diJiaItemNum
        consumeDiJiaInfo['numLimit'] = diJiaItemMaxNum * buyItemNum
        consumeDiJiaInfo['visible'] = True
        consumeDiJiaInfo['diJiaItemId1'] = diJiaItemId
        consumeDiJiaInfo['diJiaItemId2'] = tgtDiJiaItemId
        consumeDiJiaInfo['diJiaDesc1'] = diJiaDesc1
        consumeDiJiaInfo['diJiaDesc2'] = diJiaDesc2
        consumeDiJiaInfo['diJiaNumStr'] = diJiaNumStr
        consumeDiJiaInfo['check'] = curItemNum >= diJiaItemNum
        consumeDiJiaInfo['itemName'] = ID.data.get(diJiaItemId, {}).get('name', '')
    else:
        consumeDiJiaInfo['visible'] = False
    return (consumeDiJiaInfo, isValid)


def _getDijiaItemId(compositeData):
    if not compositeData:
        return 0
    diJiaType = _getDijiaType(compositeData)
    if diJiaType == DIJIA_ITEM_TO_FAME:
        return compositeData.get('diJiaItemid', 0)
    if diJiaType == DIJIA_ITEM_TO_ITEM:
        return compositeData.get('diJiaSrcItemId', 0)
