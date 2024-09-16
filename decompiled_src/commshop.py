#Embedded file name: /WORKSPACE/data/entities/common/commshop.o
import math
import BigWorld
import gametypes
import gamelog
import utils
import const
import pubgUtils
if BigWorld.component != 'client':
    import gameconfig
else:
    import gameglobal
from cdata import game_msg_def_data as GMDD

def showGameMsg(owner, msgId, data):
    if BigWorld.component == 'client':
        owner.showGameMsg(msgId, data)
    elif BigWorld.component == 'cell':
        owner.sendGameMsg(msgId, data)


def _checkCompositeShopPreLimit(owner, compositeData, buyItemNum):
    if compositeData.has_key('lvLimit'):
        lvLimit = compositeData['lvLimit']
        if lvLimit[0] == -1:
            if owner.lv > lvLimit[1]:
                return False
        elif lvLimit[1] == -1:
            if owner.lv < lvLimit[0]:
                return False
        elif owner.lv < lvLimit[0] or owner.lv > lvLimit[1]:
            return False
    if compositeData.has_key('sexLimit'):
        sexLimit = compositeData['sexLimit']
        if owner.physique.sex != sexLimit:
            return False
    if compositeData.has_key('arenaScoreLimit'):
        arenaScoreLimit = compositeData['arenaScoreLimit']
        if owner.arenaInfo.arenaScore < arenaScoreLimit:
            return False
    if compositeData.has_key('shopJingJieRequire'):
        jingJieLimit = compositeData['shopJingJieRequire']
        if owner.jingJie < jingJieLimit:
            return False
    if compositeData.has_key('needJunJieLv'):
        needJunJieLv = compositeData['needJunJieLv']
        if owner.junJieLv < needJunJieLv:
            return False
    if compositeData.has_key('needFamousGeneralLv'):
        needFamousGeneralLv = compositeData['needFamousGeneralLv']
        if owner.famousGeneralLv < needFamousGeneralLv:
            return False
    if compositeData.has_key('needJueWeiLv'):
        needJueWeiLv = compositeData['needJueWeiLv']
        if owner.jueWeiLv < needJueWeiLv:
            return False
    fameLimit = compositeData.get('fameLimit', [])
    if not owner.enoughFame(fameLimit):
        return False
    if compositeData.has_key('qumoLimit'):
        qumoLimit = compositeData.get('qumoLimit', 100)
        if owner.qumoLv < qumoLimit:
            return False
    if compositeData.has_key('appearanceItemPointLimit'):
        appearanceItemPointLimit = compositeData.get('appearanceItemPointLimit', 0)
        if owner.appearanceItemCollectPoint < appearanceItemPointLimit:
            return False
    if compositeData.has_key('schoolLimit'):
        schoolLimit = compositeData['schoolLimit']
        if owner.school not in schoolLimit:
            return False
    if compositeData.has_key('needClue'):
        needClue = compositeData['needClue']
        for cid in needClue:
            if not owner.getClueFlag(cid):
                return False

    if compositeData.has_key('spIdLimit'):
        spId = compositeData.get('spIdLimit', 0)
        if not owner.isServerProgressFinished(spId):
            return False
    progressLimit = compositeData.get('progressLimit', -1)
    if owner.curEndlessMaxProgress < progressLimit:
        return False
    if compositeData.has_key('zmjStarBossLayerLimit'):
        layerLimit = compositeData.get('zmjStarBossLayerLimit', 0)
        killRecord = owner._getZMJData(const.ZMJ_FB_INFO_STAR_BOSS_RECORD, {})
        layer = killRecord and max(killRecord.keys()) or 0
        if layer < layerLimit:
            return False
    weeklyFameLimit = compositeData.get('weekBattleFieldFameLimit', 0)
    battleFame = owner.weeklyFame.get(gametypes.MISC_VAR_OCLI_WEEKLY_FAME, {}).get(const.BATTLE_FIELD_FAME_ID, 0)
    if BigWorld.component == 'client':
        if gameglobal.rds.configData.get('enableBattleFieldFame', False) and battleFame < weeklyFameLimit:
            return False
    elif gameconfig.enableBattleFieldFame() and battleFame < weeklyFameLimit:
        return False
    scProgressLimit = compositeData.get('spriteChallengeProgressLimit', -1)
    if owner.curSpriteChallengeMaxProgress < scProgressLimit:
        return False
    pubgRankPointsLimit = compositeData.get('pubgRankPointsLimit', 0)
    pubgRankPointsLv = pubgUtils.calcRankPointsLv(owner.pubgRankPoints)
    if not pubgRankPointsLv or pubgRankPointsLimit > 0 and pubgRankPointsLv < pubgRankPointsLimit:
        return False
    return True


def _applyDiscount(v, discountRate):
    if not v:
        return v
    newv = 0
    if discountRate > 0:
        newv = int(math.ceil(v * discountRate))
    if newv > 0:
        return newv
    else:
        return v


def _checkCompositeShopConsumeContrib(owner, compositeData, buyItemNum, bMsg = True):
    consumeContrib = compositeData.get('consumeContrib', 0)
    if consumeContrib == 0:
        return True
    if not owner._checkGuild():
        return
    consumeContrib *= buyItemNum
    consumeContrib = _applyDiscount(consumeContrib, compositeData.get('discountRate', 0))
    if owner.guildContrib < consumeContrib:
        bMsg and owner.client.showGameMsg(GMDD.data.GUILD_NOT_ENOUGH_CONTRIB, ())
        return False
    return True


def _checkCompositeShopconsumeWingWorldZhanXunRank(owner, compositeData, buyItemNum, bMsg = True):
    wingWorldZhanXunRank = compositeData.get('wingWorldZhanXunRank', ())
    if not wingWorldZhanXunRank:
        return True
    if BigWorld.component == 'client':
        if not gameglobal.rds.configData.get('enableWingWorld', False):
            return False
    elif not gameconfig.enableWingWorld():
        return False
    if owner.wingWorldZhanXunRankInLastWeek in xrange(wingWorldZhanXunRank[0], wingWorldZhanXunRank[1] + 1):
        return True
    if bMsg:
        owner.client.showGameMsg(GMDD.data.WING_WORLD_ZHAN_XUN_RANK_NOT_ENOUGH, ())
    return False


def _checkCompositeShopDotaBattleFieldCash(owner, compositeData, amount, bMsg = True):
    consumeDotaBattleFieldCash = compositeData.get('consumeDotaBattleFieldCash', 0)
    if consumeDotaBattleFieldCash == 0:
        return True
    if not owner.inFubenType(const.FB_TYPE_BATTLE_FIELD_DOTA):
        return False
    if owner.battleFieldDotaCash < consumeDotaBattleFieldCash * amount:
        bMsg and owner.client.showGameMsg(GMDD.data.DOTA_BATTLE_FIELD_NOT_ENOUGH_CASH, ())
        return False
    return True


def _checkCompositeShopConsumeCash(owner, compositeData, buyItemNum, bMsg = True):
    consumeCash = compositeData.get('consumeCash', 0)
    if consumeCash == 0:
        return True
    consumeCashType = compositeData.get('cashType', gametypes.CONSUME_CASH_TYPE_NO_LIMIT)
    consumeCash *= buyItemNum
    consumeCash = _applyDiscount(consumeCash, compositeData.get('discountRate', 0))
    gamelog.debug('@zs, _checkCompositeShopConsumeCash', consumeCashType, consumeCash, buyItemNum, owner.cash, owner.bindCash)
    if consumeCashType == gametypes.CONSUME_CASH_TYPE_NO_LIMIT:
        if not owner._canPay(consumeCash):
            bMsg and showGameMsg(owner, GMDD.data.SHOP_MONEY_LESS, ())
            return False
    elif consumeCashType == gametypes.CONSUME_CASH_TYPE_BIND_CASH:
        if owner.bindCash < consumeCash:
            bMsg and showGameMsg(owner, GMDD.data.SHOP_MONEY_LESS, ())
            return False
    elif consumeCashType == gametypes.CONSUME_CASH_TYPE_CASH:
        if owner.cash < consumeCash:
            bMsg and showGameMsg(owner, GMDD.data.SHOP_MONEY_LESS, ())
            return False
    else:
        return False
    return True


def _checkCompositeShopConsumeItem(owner, consumeItem):
    tDict = {}
    for itemId, itemNum in consumeItem:
        tDict[itemId] = tDict.setdefault(itemId, 0) + itemNum

    for itemId, itemNum in tDict.iteritems():
        if owner.inv.countItemInPages(itemId, enableParentCheck=True) < itemNum:
            return False

    return True


def _checkBuyItemConsume(owner, compositeData, buyItemNum, diJiaItemNum, diJiaSrcItemNum, bMsg = True):
    if buyItemNum == 0:
        return True
    if not _checkCompositeShopConsumeCash(owner, compositeData, buyItemNum, bMsg):
        return False
    consumeItem, consumeFame, _ = _calcCompositeShopConsumeInfo(owner, compositeData, buyItemNum, diJiaItemNum, diJiaSrcItemNum, False)
    if not _checkCompositeShopConsumeItem(owner, consumeItem):
        return False
    if not owner.enoughFame(consumeFame):
        return False
    return True


def _calcCompositeShopConsumeInfo(owner, compositeData, buyItemNum, diJiaItemNum, diJiaItemToItemNum, needSeparateDiJia):
    consumeDiJia = ()
    consumeItemDict = {}
    discountRate = compositeData.get('discountRate', 0)
    for itemId, num in compositeData.get('consumeItem', []):
        consumeItemDict[itemId] = consumeItemDict.setdefault(itemId, 0) + num * buyItemNum

    if diJiaItemToItemNum > 0:
        realConsumeDiJiaItemNum = 0
        realConsumeTgtItemNum = 0
        diJiaItemToItemNum = min(compositeData.get('diJiaSrcMaxNum', 1) * buyItemNum, diJiaItemToItemNum)
        tgtDiJiaItemId = compositeData['diJiaTargetItemId']
        tgtDiJiaItemNum = compositeData['diJiaTargetItemNum']
        srcDiJiaItemId = compositeData['diJiaSrcItemId']
        srcDiJiaItemNum = compositeData['diJiaSrcItemNum']
        probeTgtItemNum = diJiaItemToItemNum / srcDiJiaItemNum * tgtDiJiaItemNum
        if consumeItemDict[tgtDiJiaItemId] < probeTgtItemNum:
            realConsumeDiJiaItemNum = consumeItemDict[tgtDiJiaItemId] / tgtDiJiaItemNum * srcDiJiaItemNum
            realConsumeTgtItemNum = realConsumeDiJiaItemNum / srcDiJiaItemNum * tgtDiJiaItemNum
        else:
            realConsumeTgtItemNum = probeTgtItemNum
            realConsumeDiJiaItemNum = realConsumeTgtItemNum / tgtDiJiaItemNum * srcDiJiaItemNum
        consumeItemDict[tgtDiJiaItemId] -= realConsumeTgtItemNum
        if needSeparateDiJia:
            if consumeItemDict[tgtDiJiaItemId] <= 0:
                consumeItemDict[tgtDiJiaItemId] = 0
            if realConsumeDiJiaItemNum:
                consumeDiJia = (srcDiJiaItemId, realConsumeDiJiaItemNum)
        else:
            if consumeItemDict[tgtDiJiaItemId] == 0:
                del consumeItemDict[tgtDiJiaItemId]
            if realConsumeDiJiaItemNum:
                consumeItemDict[srcDiJiaItemId] = consumeItemDict.setdefault(srcDiJiaItemId, 0) + realConsumeDiJiaItemNum
    elif discountRate > 0:
        for itemId, num in consumeItemDict.items():
            consumeItemDict[itemId] = _applyDiscount(num, discountRate)

    consumeItem = consumeItemDict.items()
    consumeFame = []
    for fameId, num in compositeData.get('consumeFame', []):
        consumeFame.append((fameId, _applyDiscount(num * buyItemNum, discountRate)))

    if diJiaItemNum != 0:
        diJiaItemNum = min(compositeData.get('diJiaItemMaxNum', 1) * buyItemNum, diJiaItemNum)
        diJiaItemid = compositeData.get('diJiaItemid')
        tmpDict = {}
        for fameId, fameNum in consumeFame:
            tmpDict[fameId] = tmpDict.setdefault(fameId, 0) + fameNum

        diJiaFame = compositeData.get('diJiaFame', [])
        for diJiaFameId, diJiaFameNum in diJiaFame:
            if tmpDict.has_key(diJiaFameId):
                diJiaFameNum = diJiaFameNum * diJiaItemNum
                tmpDict[diJiaFameId] = max(tmpDict[diJiaFameId] - diJiaFameNum, 0)

        consumeFame = []
        if needSeparateDiJia:
            consumeDiJia = (diJiaItemid, diJiaItemNum)
            for fameId, fameNum in tmpDict.iteritems():
                if fameNum >= 0:
                    consumeFame.append((fameId, fameNum))

        else:
            consumeItem.append((diJiaItemid, diJiaItemNum))
            for fameId, fameNum in tmpDict.iteritems():
                if fameNum > 0:
                    consumeFame.append((fameId, fameNum))

    return (consumeItem, consumeFame, consumeDiJia)


def calcPrivateShopNextRefreshFreeTime(tRefreshFree):
    t = utils.getDaySecond(tRefreshFree)
    tNext = t + const.PRIVATE_SHOP_REFRESH_FREE_INTERVAL
    if tRefreshFree - t >= const.PRIVATE_SHOP_REFRESH_FREE_INTERVAL:
        tNext += const.PRIVATE_SHOP_REFRESH_FREE_INTERVAL
    return tNext
