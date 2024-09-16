#Embedded file name: /WORKSPACE/data/entities/common/commoncard.o
import const
import time
import gameconfigCommon
from checkResult import CheckResult
import utils
from formula import calcCombatScoreType
from cdata import game_msg_def_data as GMDD
from cdata import card_to_item as CTI
from cdata import card_to_parent_item as CTPI
from data import base_card_data as BCD
from data import advance_card_data as ACD
from data import card_wash_group_data as CWGD
from data import sys_config_data as SCD

class CommonCard(object):

    def __init__(self, cardId, actived = False, progress = 0, advanceLv = 0, slot = None):
        self.id = cardId
        self.actived = actived
        self.progress = progress
        self.advanceLv = advanceLv
        self.addAdvanceLv = 0
        self.slot = list() if not slot else slot
        self.washNum = 0
        self.washTime = 0
        self.lastDelWashTime = 0
        self.washIndex = 0
        self.washSchemeLock = 0
        self.washProps = {}
        self.washPropsEx = {}
        self.newWashProps = {}
        self.washNotMaxNum = 0
        self.washNotFullProp = 0
        self.dueTime = 0
        self.notValid = False
        self.multiNewWashProps = {}

    def getConfigData(self):
        return BCD.data.get(self.id, {})

    def getAdvanceData(self):
        return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + self.advanceLv, {})

    @property
    def showPriority(self):
        return BCD.data.get(self.id, {}).get('showPriority', 0)

    @property
    def name(self):
        return BCD.data.get(self.id, {}).get('name', 0)

    @property
    def cardIcon(self):
        iconType = 'breakRankIcon' if self.isBreakRank else 'icon'
        iconId = str(BCD.data.get(self.id, {}).get(iconType, 'notFound'))
        return ''.join(('card/', iconId, '.dds'))

    @property
    def qualityIcon(self):
        iconType = 'equipIcon'
        iconId = str(ACD.data.get(self.id * const.CARD_PRESERVED_RANK + self.advanceLv, {}).get(iconType, 'notFound'))
        return ''.join(('card/quality/', iconId, '.dds'))

    @property
    def equipIcon(self):
        iconType = 'equipIcon'
        iconId = str(ACD.data.get(self.id * const.CARD_PRESERVED_RANK + self.advanceLv, {}).get(iconType, 'notFound'))
        return ''.join(('card/cardtype/', iconId, '.dds'))

    @property
    def renewalItems(self):
        return BCD.data.get(self.id, {}).get('renewalItems', ())

    @property
    def isCurrentPeriod(self):
        return BCD.data.get(self.id, {}).get('isCurrentPeriod', 0) == 1

    @property
    def propType(self):
        return BCD.data.get(self.id, {}).get('propType', 0)

    @property
    def monsterType(self):
        return BCD.data.get(self.id, {}).get('type', 0)

    @property
    def equipType(self):
        return BCD.data.get(self.id, {}).get('equipType', 0)

    @property
    def washFragment(self):
        return BCD.data.get(self.id, {}).get('washFragmentCnt', ())

    @property
    def school(self):
        return BCD.data.get(self.id, {}).get('school', ())

    @property
    def operatingCard(self):
        return bool(BCD.data.get(self.id, {}).get('operatingCard', 0))

    def isValidCard(self, tTime = 0):
        tTime = tTime or utils.getNow()
        if self.dueTime and self.dueTime <= tTime:
            return False
        if self.expiredTime and self.expiredTime <= tTime:
            return False
        return True

    @property
    def curWashIndex(self):
        if gameconfigCommon.enableCardWashScheme():
            return self.washIndex
        return 0

    @property
    def validDuration(self):
        return BCD.data.get(self.id, {}).get('validDuration')

    @property
    def validTime(self):
        return BCD.data.get(self.id, {}).get('validTime')

    @property
    def expiredTime(self):
        if not self.validTime:
            return 0
        ts = time.strptime(self.validTime, '%Y.%m.%d.%H.%M.%S')
        return time.mktime(ts)

    @property
    def canDecompose(self):
        return not bool(BCD.data.get(self.id, {}).get('noDecompose', 0))

    @property
    def noDecompose(self):
        return bool(BCD.data.get(self.id, {}).get('noDecompose', 0))

    @property
    def noCompose(self):
        return bool(BCD.data.get(self.id, {}).get('noCompose', 0))

    @property
    def noDecProgress(self):
        return bool(BCD.data.get(self.id, {}).get('noDecProgress', 0))

    @property
    def noDecomposeActive(self):
        return bool(BCD.data.get(self.id, {}).get('noDecomposeActive', 0))

    @property
    def noDecomposeLv(self):
        return bool(BCD.data.get(self.id, {}).get('noDecomposeLv', 0))

    @property
    def canRenewal(self):
        return bool(BCD.data.get(self.id, {}).get('canRenewal', 0))

    @property
    def noFixToSlot(self):
        return bool(BCD.data.get(self.id, {}).get('noFixToSlot', 0))

    @property
    def washFragmentType(self):
        if len(self.washFragment) > 0:
            return self.washFragment[0]
        return 0

    @property
    def washFragmentCnt(self):
        if len(self.washFragment) > 1:
            return self.washFragment[1]
        return 0

    @property
    def washNumId(self):
        return BCD.data.get(self.id, {}).get('washNumId', 0)

    @property
    def washGroupId(self):
        return BCD.data.get(self.id, {}).get('washGroupId', ())

    @property
    def version(self):
        return BCD.data.get(self.id, {}).get('versionId', 0)

    @property
    def randFuncId(self):
        return BCD.data.get(self.id, {}).get('randFuncId', 0)

    @property
    def numToFull(self):
        return BCD.data.get(self.id, {}).get('numToFull', 0)

    @property
    def numOfFull(self):
        return BCD.data.get(self.id, {}).get('numOfFull', 0)

    @property
    def isCoolingDown(self):
        return self.lastDelWashTime and utils.getNow() < self.lastDelWashTime + const.CARD_WASH_COOL_DOWN

    @property
    def fagmentCntValue(self):
        return self.compoundFragmentCnt(0)

    @property
    def fragmentType(self):
        return self.compoundFragmentType(0)

    @property
    def cardItemId(self):
        return CTI.data.get(self.id, [])

    @property
    def cardItemParentId(self):
        items = CTPI.data.get(self.id, [])
        if items:
            return items[0]
        return 0

    @property
    def advanceLvEx(self):
        if self.advanceLv < const.CARD_BREAK_RANK:
            return self.advanceLv
        return min(self.advanceLv + max(self.addAdvanceLv, 0), const.CARD_MAX_RANK)

    @property
    def decomposeRate(self):
        if self.expiredTime:
            return const.CARD_DEL_WASH_RETURN_EXPIRE
        else:
            return const.CARD_DEL_WASH_RETURN

    @property
    def isMaxLvCard(self):
        return bool(BCD.data.get(self.id, {}).get('isMaxLvCard', 0))

    def decomposeFragmentCnt(self, advanceLv):
        advanceLv = min(advanceLv, const.CARD_MAX_RANK)
        data = ACD.data.get(self.id * const.CARD_PRESERVED_RANK + advanceLv, None)
        if data:
            return data.get('decompoundCnt', 0)
        return 0

    def compoundFragment(self, advanceLv):
        return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + advanceLv, {}).get('compoundCnt', ())

    def compoundFragmentType(self, advanceLv):
        data = self.compoundFragment(advanceLv)
        if len(data) > 0:
            return data[0]
        return 0

    def compoundFragmentCnt(self, advanceLv):
        data = self.compoundFragment(advanceLv)
        if len(data) > 1:
            return data[1]
        return 0

    def getNeedRoleLv(self, advanceLvEx):
        data = ACD.data.get(self.id * const.CARD_PRESERVED_RANK + advanceLvEx, None)
        if data:
            return data.get('needRoleLv', 0)
        return 0

    def getAddDuration(self, advanceLv):
        return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + advanceLv, {}).get('addDuration', 0)

    @property
    def activeProps(self):
        return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + self.advanceLvEx, {}).get('activeProps', ())

    @property
    def activeCondProps(self):
        return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + self.advanceLvEx, {}).get('activeCondProps', ())

    @property
    def activeEffect(self):
        return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + self.advanceLvEx, {}).get('activeEffect', ())

    @property
    def advanceProps(self):
        return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + self.advanceLvEx, {}).get('advanceProps', ())

    @property
    def condProps(self):
        return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + self.advanceLvEx, {}).get('condProps', ())

    @property
    def applyedProps(self):
        if not self.actived:
            return ()
        return self.activeProps

    @property
    def equipProps(self):
        if not self.actived:
            return ()
        return self.advanceProps

    @property
    def equipPropKey(self):
        if not self.actived:
            return ()
        return (self.id, self.advanceLvEx)

    @property
    def cardActiveScore(self):
        if not self.actived or self.notValid:
            return 0
        return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + self.advanceLvEx, {}).get('activeScore', 0)

    @property
    def cardActiveScoreType(self):
        if not self.actived or self.notValid:
            return []
        return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + self.advanceLvEx, {}).get('activeScoreType', [])

    @property
    def cardEquipScore(self):
        if not self.actived or self.notValid:
            return 0
        return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + self.advanceLvEx, {}).get('equipScore', 0)

    @property
    def cardEquipScoreType(self):
        if not self.actived or self.notValid:
            return 0
        return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + self.advanceLvEx, {}).get('equipScoreType', [])

    @property
    def cardWashScore(self):
        if self.notValid:
            return 0
        score = 0
        for data in self.curWashProps.itervalues():
            score += data.get('score', 0)

        return score

    @property
    def cardWashScoreType(self):
        """
        :return: coeff\xa3\xac\xd3\xd0\xb5\xe3\xcc\xd8\xca\xe2\xa3\xac\xcf\xc8\xcb\xe3\xb3\xf6\xc1\xcbsub\xd6\xb5\xa3\xac\xd3\xd6\xb7\xd6\xb1\xf0\xc7\xf3\xb5\xc4\xcf\xb5\xca\xfd
        """
        if not self.curWashProps or self.notValid:
            return []
        scoreType = [0,
         0,
         0,
         0]
        for seq, data in self.curWashProps.iteritems():
            score = data.get('score', 0)
            washGroupId = data.get('washGroupId', 0)
            stage = data.get('stage', 0)
            sType = data.get('sType', 0)
            sId = data.get('sId', 0)
            coeff = CWGD.data.get((washGroupId,
             seq,
             stage,
             sType,
             sId), {}).get('scoreType', [])
            scoreType = calcCombatScoreType(scoreType, coeff, [], score, const.COMBAT_SCORE_TYPE_OP_COEFF)

        totalScore = self.cardWashScore
        if totalScore:
            return [ float(x) * 100 / totalScore for x in scoreType ]
        return [25,
         25,
         25,
         25]

    @property
    def passivitySkills(self):
        return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + self.advanceLvEx, {}).get('passivity', ())

    @property
    def isAdvanced(self):
        return self.advanceLvEx > 0

    @property
    def isFullAdvance(self):
        return self.advanceLv >= const.CARD_MAX_RANK

    @property
    def isBreakRank(self):
        return self.advanceLvEx >= const.CARD_BREAK_RANK

    @property
    def isBreakRankHigh(self):
        return self.advanceLvEx >= const.CARD_BREAK_RANK_HIGH

    @property
    def curWashProps(self):
        if self.curWashIndex == 0:
            return self.washProps
        else:
            return self.washPropsEx

    def selWashProps(self, schemeSelect = 0):
        if schemeSelect == 0:
            return self.washProps
        else:
            return self.washPropsEx

    @property
    def bossItemRetRate(self):
        return BCD.data.get(self.id, {}).get('bossItemRetRate', const.CARD_BOSS_ITEM_RETURN)

    def getRankUpItems(self):
        if self.advanceLv >= const.CARD_BREAK_RANK:
            return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + self.advanceLv + 1, {}).get('rankUpItems', None)

    def getBossItems(self, advanceLv = None, actived = None):
        actived = actived if actived is not None else self.actived
        advanceLv = advanceLv if advanceLv is not None else self.advanceLv
        if actived:
            return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + advanceLv + 1, {}).get('bossItems', None)
        else:
            return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + advanceLv, {}).get('bossItems', None)

    def getActiveProps(self, advanceLv):
        if not self.actived:
            return ()
        if advanceLv >= const.CARD_BREAK_RANK:
            advanceLvEx = min(advanceLv + max(self.addAdvanceLv, 0), const.CARD_MAX_RANK)
        else:
            advanceLvEx = advanceLv
        return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + advanceLvEx, {}).get('activeProps', ())

    def getActiveCondProps(self, advanceLv):
        if not self.actived:
            return ()
        if advanceLv >= const.CARD_BREAK_RANK:
            advanceLvEx = min(advanceLv + max(self.addAdvanceLv, 0), const.CARD_MAX_RANK)
        else:
            advanceLvEx = advanceLv
        return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + advanceLvEx, {}).get('activeCondProps', ())

    def getActiveEffect(self, advanceLv):
        if not self.actived:
            return ()
        if advanceLv >= const.CARD_BREAK_RANK:
            advanceLvEx = min(advanceLv + max(self.addAdvanceLv, 0), const.CARD_MAX_RANK)
        else:
            advanceLvEx = advanceLv
        return ACD.data.get(self.id * const.CARD_PRESERVED_RANK + advanceLvEx, {}).get('activeEffect', ())

    def getExtraItems(self):
        items = ()
        rankUpItems = self.getRankUpItems()
        if rankUpItems:
            items += rankUpItems
        bossItems = self.getBossItems()
        if bossItems:
            items += bossItems
        return items

    def getExtraItemsEx(self):
        candidates = []
        diKouDict = SCD.data.get('cardBossItemDikouDict', {})
        rankUpItems = self.getRankUpItems()
        if rankUpItems:
            for itemId, itemNum in rankUpItems:
                candidates.append(((itemId,), itemNum))

        bossItems = self.getBossItems()
        if bossItems:
            for itemId, itemNum in bossItems:
                diKouIds = diKouDict.get(itemId)
                if diKouIds:
                    candidates.append((diKouIds + (itemId,), itemNum))
                else:
                    candidates.append(((itemId,), itemNum))

        return candidates

    def checkCompose(self, useFragment = True, skipComposeCheck = False):
        if self.actived:
            return CheckResult(False, (GMDD.data.CARD_COMPOUND,))
        if useFragment and not skipComposeCheck and self.noCompose:
            return CheckResult(False, (GMDD.data.CARD_NOT_FRAGMENT_COMPOUND,))
        if useFragment and self.progress < self.compoundFragmentCnt(0):
            return CheckResult(False, (GMDD.data.CARD_NOFULL_PROGRESS,))
        if self.isExpiredCard():
            return CheckResult(False, (GMDD.data.CARD_HAS_EXPIRED,))
        return CheckResult(True, 0)

    def checkDecompose(self):
        if not self.actived:
            return CheckResult(False, (GMDD.data.CARD_NON_COMPOUND,))
        if self.expiredTime > 0:
            return CheckResult(False, (GMDD.data.EXPIRED_CARD_NO_DECOMPOSE,))
        if self.noDecompose:
            return CheckResult(False, (GMDD.data.CARD_NO_DECOMPOSE,))
        if self.noDecomposeActive:
            return CheckResult(False, (GMDD.data.CARD_CONFIG_NO_DECOMPOSE_ACTIVE,))
        if self.advanceLv > 0:
            return CheckResult(False, (GMDD.data.CARD_HAS_ADVANCE,))
        if self.progress > 0:
            return CheckResult(False, (GMDD.data.CARD_HAS_PROGRESS,))
        return CheckResult(True, 0)

    def checkUpgradeProgress(self, inc, num = 0):
        if self.operatingCard and inc > 0:
            return CheckResult(False, (GMDD.data.CARD_CONFIG_NO_FRAGMENT,))
        if self.advanceLv >= const.CARD_MAX_RANK:
            return CheckResult(False, (GMDD.data.CARD_FULL_PROGRESS,))
        needProgress = self.compoundFragmentCnt(self.advanceLv + 1 if self.actived else 0)
        if self.progress >= needProgress:
            return CheckResult(False, (GMDD.data.CARD_ENOUGH_PROGRESS,))
        if self.advanceLv == const.CARD_MAX_RANK - 1:
            if self.progress + inc + self.fagmentCntValue * num > needProgress:
                return CheckResult(False, (GMDD.data.CARD_WILL_OVER_PROGRESS,))
        if self.progress + inc > needProgress:
            return CheckResult(False, (GMDD.data.CARD_WILL_OVER_PROGRESS,))
        if num > 0:
            if self.progress + self.fagmentCntValue * (num - 1) + inc >= needProgress:
                return CheckResult(False, (GMDD.data.CARD_WILL_OVER_PROGRESS,))
        return CheckResult(True, 0)

    def checkDegradeProgress(self, deType):
        if self.noDecompose:
            return CheckResult(False, (GMDD.data.CARD_NO_DEGRADE_PROGRESS,))
        if deType not in const.CARD_DEGRADE_TYPE:
            return CheckResult(False, (GMDD.data.CARD_UNKNOW_DEGRADE,))
        if deType == const.CARD_DEGRADE_TYPE_PROGRESS:
            if self.noDecProgress:
                return CheckResult(False, (GMDD.data.CARD_CONFIG_NO_DEC_PROGRESS,))
            if self.progress == 0:
                return CheckResult(False, (GMDD.data.CARD_NULL_PROGRESS,))
        if deType == const.CARD_DEGRADE_TYPE_RANK:
            if self.noDecomposeLv:
                return CheckResult(False, (GMDD.data.CARD_CONFIG_NO_DECOMPOSE_RANK,))
            if self.advanceLv == 0:
                return CheckResult(False, (GMDD.data.CARD_ZERO_ADVANCE,))
        if deType == const.CARD_DEGRADE_TYPE_DECOMPOSE:
            return self.checkDecompose()
        return CheckResult(True, 0)

    def checkAdvance(self):
        if not self.actived:
            return CheckResult(False, (GMDD.data.CARD_NON_COMPOUND,))
        if self.noDecompose:
            return CheckResult(False, (GMDD.data.CARD_NO_ADVANCE,))
        if self.advanceLv >= const.CARD_MAX_RANK:
            return CheckResult(False, (GMDD.data.CARD_FULL_ADVANCE,))
        needProgress = self.compoundFragmentCnt(self.advanceLv + 1)
        if self.progress < needProgress:
            return CheckResult(False, (GMDD.data.CARD_LILING_NOT_ENOUGH,))
        return CheckResult(True, 0)

    def compound(self, useFragment = True):
        costProgress = 0
        if useFragment:
            costProgress = self.compoundFragmentCnt(0)
            self.progress -= costProgress
        self.actived = True
        self.advanceLv = 0
        if self.validDuration:
            self.dueTime = utils.getNow() + self.validDuration
        return costProgress

    def decompound(self):
        self.actived = False

    def upgradeProgress(self, inc):
        self.progress += inc
        return self.progress

    def getDelgradeProgress(self, deType):
        delProgress = 0
        if deType == const.CARD_DEGRADE_TYPE_PROGRESS:
            delProgress = self.progress
        elif deType == const.CARD_DEGRADE_TYPE_RANK:
            delProgress = self.progress
            delProgress += self.compoundFragmentCnt(self.advanceLv)
        elif deType == const.CARD_DEGRADE_TYPE_DECOMPOSE:
            delProgress = self.compoundFragmentCnt(0)
        return delProgress

    def degradeProgress(self, deType):
        getFragmentCnt = 0
        delLv = 0
        if deType == const.CARD_DEGRADE_TYPE_PROGRESS:
            getFragmentCnt = int(self.progress * self.decomposeFragmentCnt(self.advanceLv + 1) * 1.0 / 10000)
            self.progress = 0
        elif deType == const.CARD_DEGRADE_TYPE_RANK:
            getFragmentCnt = int(self.progress * self.decomposeFragmentCnt(self.advanceLv + 1) * 1.0 / 10000)
            getFragmentCnt += int(self.compoundFragmentCnt(self.advanceLv) * self.decomposeFragmentCnt(self.advanceLv) * 1.0 / 10000)
            delLv = 1
            self.advanceLv -= 1
            self.progress = 0
        elif deType == const.CARD_DEGRADE_TYPE_DECOMPOSE:
            delLv = self.advanceLv
        return (getFragmentCnt, delLv)

    def advance(self):
        self.progress -= self.compoundFragmentCnt(self.advanceLv + 1)
        self.advanceLv += 1
        if self.validDuration:
            self.dueTime = max(self.dueTime, utils.getNow()) + self.getAddDuration(self.advanceLv)

    def decompose(self):
        self.advanceLv = 0
        self.progress = 0
        self.washIndex = 0
        self.actived = False
        self.slot = []
        self.washNum = 0
        self.washProps = {}
        self.washPropsEx = {}
        self.newWashProps = {}

    def getWashCost(self):
        return self.washFragmentCnt

    def getDelWashCost(self):
        return self.compoundFragmentCnt(0)

    def checkCanWash(self):
        if not self.actived:
            return CheckResult(False, (GMDD.data.CARD_NON_COMPOUND,))
        if self.noFixToSlot:
            return CheckResult(False, (GMDD.data.CARD_CONFIG_NO_FIX_OR_WASH,))
        if self.advanceLvEx < const.CARD_BREAK_RANK:
            return CheckResult(False, (GMDD.data.CARD_WASH_NOT_OPEN,))
        return CheckResult(True, 0)

    def checkCanDelWash(self):
        if not self.actived:
            return CheckResult(False, (GMDD.data.CARD_NON_COMPOUND,))
        if self.noFixToSlot:
            return CheckResult(False, (GMDD.data.CARD_CONFIG_NO_FIX_OR_WASH,))
        if not self.washProps and not self.washPropsEx:
            return CheckResult(False, (GMDD.data.CARD_NOT_WASH,))
        return CheckResult(True, 0)

    def firstWash(self):
        return self.washNum == 1

    def checkConfirmWash(self, schemeSelect):
        if not self.actived:
            return CheckResult(False, (GMDD.data.CARD_NON_COMPOUND,))
        if self.noFixToSlot:
            return CheckResult(False, (GMDD.data.CARD_CONFIG_NO_FIX_OR_WASH,))
        if not self.newWashProps:
            return CheckResult(False, (GMDD.data.CARD_NOT_WASH,))
        if schemeSelect > self.washSchemeLock:
            return CheckResult(False, (GMDD.data.CARD_WSAH_SCHEME_NOT_UNLOCK,))
        return CheckResult(True, 0)

    def checkAutoConfirmWash(self, schemeSelect):
        if not self.actived:
            return CheckResult(False, (GMDD.data.CARD_NON_COMPOUND,))
        if self.noFixToSlot:
            return CheckResult(False, (GMDD.data.CARD_CONFIG_NO_FIX_OR_WASH,))
        if not self.multiNewWashProps:
            return CheckResult(False, (GMDD.data.CARD_NOT_WASH,))
        if schemeSelect > self.washSchemeLock:
            return CheckResult(False, (GMDD.data.CARD_WSAH_SCHEME_NOT_UNLOCK,))
        return CheckResult(True, 0)

    def wash(self, props, isAuto = False):
        if isAuto:
            self.multiNewWashProps = props
        else:
            self.newWashProps = props
        self.washNum += 1
        self.washTime = utils.getNow()

    def confirmWash(self, confirm = 0, schemeSelect = 0):
        if confirm and self.newWashProps:
            if schemeSelect == 0:
                self.washProps = self.newWashProps
            else:
                self.washPropsEx = self.newWashProps
        self.newWashProps = {}

    def confirmAutoWash(self, confirm = 0, schemeSelect = 0):
        if confirm and self.multiNewWashProps:
            if schemeSelect == 0:
                self.washProps = self.multiNewWashProps
            else:
                self.washPropsEx = self.multiNewWashProps
        self.multiNewWashProps = {}

    def delWash(self):
        self.washProps = {}
        self.washPropsEx = {}
        self.newWashProps = {}
        self.washNum = 0
        self.lastDelWashTime = utils.getNow()
        self.multiNewWashProps = {}

    def checkFixToSlot(self, slotVal, isEmptySlot):
        if self.noFixToSlot:
            return CheckResult(False, (GMDD.data.CARD_CONFIG_NO_FIX_OR_WASH,))
        data = self.getConfigData()
        usableSlots = data.get('slot', None)
        slotId = slotVal / const.CARD_SLOT_DIV_NUM
        slotIdx = slotVal % const.CARD_SLOT_DIV_NUM
        if slotId <= 0 or slotIdx <= 0:
            return CheckResult(False, (GMDD.data.CARD_NOT_FIX_SLOT,))
        if usableSlots and slotIdx not in usableSlots:
            return CheckResult(False, (GMDD.data.CARD_NOT_FIX_SLOT,))
        if slotVal in self.slot:
            return CheckResult(False, (GMDD.data.CARD_NOT_FIX_SLOT,))
        if not isEmptySlot and self.isFixedInSlot(slotId):
            return CheckResult(False, (GMDD.data.CARD_HAS_FIXED_SLOT,))
        return CheckResult(True, 0)

    def fixToSlot(self, slotVal):
        if slotVal not in self.slot:
            self.slot.append(slotVal)

    def unfixFromSlot(self, slotVal):
        if slotVal in self.slot:
            self.slot.remove(slotVal)

    def checkCanDikou(self, opType, dikouType):
        if dikouType == 0:
            return CheckResult(True, 0)
        if opType == const.CARD_ITEM_BEHAVIOR_WASH and dikouType == const.CARD_DIKOU_TYPE_WASH_POINT:
            if self.isCoolingDown:
                return CheckResult(False, (GMDD.data.CARD_WASH_WASH_POINT_COOL,))
        if not const.CARD_BEHAVIOR_DOKOU.has_key(opType) or dikouType not in const.CARD_BEHAVIOR_DOKOU[opType]:
            return CheckResult(False, (GMDD.data.CARD_WASH_CAN_NOT_DIKOU,))
        return CheckResult(True, 0)

    def checkCanAddDuration(self):
        if not self.actived:
            return CheckResult(False, (GMDD.data.CARD_NON_COMPOUND,))
        if not self.validDuration or not self.dueTime or not self.canRenewal:
            return CheckResult(False, (GMDD.data.CARD_CONFIG_NO_RENEWAL,))
        return CheckResult(True, 0)

    def addDuration(self, duration):
        self.dueTime = max(utils.getNow(), self.dueTime) + max(duration, 0)

    def getDecomponseRate(self, advanceLv, actived):
        if actived:
            rate = self.decomposeFragmentCnt(advanceLv + 1) * 1.0 / 10000
        else:
            rate = self.decomposeFragmentCnt(0) * 1.0 / 10000
        return rate

    def isFixedInSlot(self, slotId):
        if not self.slot:
            return False
        for slotVal in self.slot:
            if slotVal / const.CARD_SLOT_DIV_NUM == slotId:
                return True

        return False

    def getCardSlotVal(self, slotId):
        if not self.slot:
            return 0
        for slotVal in self.slot:
            if slotVal / const.CARD_SLOT_DIV_NUM == slotId:
                return slotVal

        return 0

    def getDecomposeFragmentCnt(self, startLv = 0):
        fragmentCnt = 0
        advanceLv = self.advanceLv
        for i in xrange(10):
            if advanceLv <= startLv:
                break
            fragmentCnt += int(self.compoundFragmentCnt(advanceLv) * self.decomposeFragmentCnt(advanceLv) * 1.0 / 10000)
            advanceLv -= 1

        fragmentCnt += self.progress
        return fragmentCnt

    def getDecomposeBossItems(self, startLv = 0, rate = None):
        rate = self.bossItemRetRate if rate is None else rate
        bossItems = {}
        advanceLv = self.advanceLv
        for i in xrange(10):
            if advanceLv <= startLv:
                break
            items = self.getBossItems(advanceLv - 1) or ()
            for itemId, itemNum in items:
                bossItems[itemId] = bossItems.get(itemId, 0) + int(round(itemNum * rate))

            advanceLv -= 1

        return bossItems

    def isExpiredCard(self, tTime = 0):
        if not self.expiredTime:
            return False
        tTime = tTime or utils.getNow()
        if tTime < self.expiredTime:
            return False
        return True

    def isNoRenewalDueCard(self, tTime = 0):
        if not self.dueTime or self.canRenewal:
            return False
        tTime = tTime or utils.getNow()
        if tTime < self.dueTime:
            return False
        return True

    def isDueCard(self, tTime = 0):
        if not self.dueTime:
            return False
        tTime = tTime or utils.getNow()
        if tTime < self.dueTime:
            return False
        return True

    def checkChangeWashScheme(self, schemeSelect):
        if not self.actived:
            return CheckResult(False, (GMDD.data.CARD_NON_COMPOUND,))
        if self.noFixToSlot:
            return CheckResult(False, (GMDD.data.CARD_CONFIG_NO_FIX_OR_WASH,))
        if schemeSelect and not gameconfigCommon.enableCardWashScheme:
            return CheckResult(False, (GMDD.data.CARD_WSAH_SCHEME_NOT_OPEN,))
        if schemeSelect and schemeSelect > self.washSchemeLock:
            return CheckResult(False, (GMDD.data.CARD_WSAH_SCHEME_NOT_UNLOCK,))
        return CheckResult(True, 0)

    def changeWashScheme(self, schemeSelect):
        if self.washIndex == schemeSelect:
            return False
        self.washIndex = schemeSelect
        return True

    def checkUnlockWashScheme(self, washIndex):
        if not self.actived:
            return CheckResult(False, (GMDD.data.CARD_NON_COMPOUND,))
        if self.noFixToSlot:
            return CheckResult(False, (GMDD.data.CARD_CONFIG_NO_FIX_OR_WASH,))
        if not gameconfigCommon.enableCardWashScheme():
            return CheckResult(False, (GMDD.data.CARD_WSAH_SCHEME_NOT_OPEN,))
        if self.washSchemeLock >= washIndex:
            return CheckResult(False, (GMDD.data.CARD_WSAH_SCHEME_HAS_UNLOCK,))
        if washIndex > self.washSchemeLock + 1:
            return CheckResult(False, (GMDD.data.CARD_WSAH_SCHEME_PREV_NOT_UNLOCK,))
        if washIndex > const.CARD_WASH_SCHEME_CURRENT_MAX:
            return CheckResult(False, (GMDD.data.CARD_WSAH_SCHEME_NOT_OPEN,))
        return CheckResult(True, 0)

    def unlockWashScheme(self, washIndex):
        self.washSchemeLock = washIndex
