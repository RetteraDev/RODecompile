#Embedded file name: /WORKSPACE/data/entities/common/commnpcfavor.o
import copy
import BigWorld
import utils
import formula
import const
if BigWorld.component in ('base', 'cell'):
    import Netease
from userSoleType import UserSoleType
from userDictType import UserDictType
from item import Item
from data import sys_config_data as SCD
from data import npc_data as ND
from data import nf_npc_data as NFND
from data import nf_npc_friendly_level_data as NFNFLD
from data import nf_npc_level_data as NFNLD
from data import quest_data as QD
from data import item_data as ID
from data import equip_gem_data as EGD
from data import nf_give_item_group_data as NFGIGD
from data import nf_give_item_friendly_data as NFGIFD
from cdata import manual_equip_cost_data as MECD
from cdata import item_synthesize_set_data as ISSD
NF_FEATURE_FOOD = 0
NF_FEATURE_MOOD = 1
NF_FEATURE_HEALTH = 2
NF_FEATURE_SOCIAL = 3
NF_FEATURE_INDEX_CNT = 4
NF_FEATURE_INDEX_LIST = [NF_FEATURE_FOOD,
 NF_FEATURE_MOOD,
 NF_FEATURE_HEALTH,
 NF_FEATURE_SOCIAL]
NF_FEATURE_VAL_MIN = 0
NF_FEATURE_VAL_MAX = 100
NF_FEATURE_REDUCE_INTERVAL = 300
NF_GIVE_ITEM_LOVE = 1
NF_GIVE_ITEM_LIKE = 2
NF_GIVE_ITEM_NOT_LIKE = 3
NF_GIVE_ITEM_HATE = 4
NF_PERMANENT_FRIENDLY_NAME = '好感度'
NF_DAILY_FRIENDLY_NAME = '今日印象值'
NF_HEARTBEAT_NAME = '七日心动值'
NF_GIVE_ITEM_TYPE_MANUAL_EQUIP = 1
NF_GIVE_ITEM_TYPE_EQUIP = 2
NF_GIVE_ITEM_TYPE_HIEROGRAM = 3
NF_GIVE_ITEM_TYPE_EQUIP_GEM = 4
NF_GIVE_ITEM_TYPE_GUAN_YIN_NORMAL_SKILL_BOOK = 5
NF_GIVE_ITEM_TYPE_SPRITE_TEXT_BOOK = 6
NF_GIVE_ITEM_MSG_MAX_CNT = 3
NF_ITEM_ARMOR_TYPE = frozenset([1,
 2,
 3,
 4,
 5])
NF_ITEM_JEWEL_TYPE = frozenset([1, 2, 3])
NF_PFRIENDLY_SOURCE_QUEST = 1
NF_PFRIENDLY_SOURCE_GIVE_ITEM = 2
NF_PFRIENDLY_SOURCE_DAILY_RESET = 3
NF_PFRIENDLY_SOURCE_OTHER = 4
NF_PFRIENDLY_ENHANCE_TYPE_NONE = 0
NF_PFRIENDLY_ENHANCE_TYPE_LIKE = 1
NF_DFRIENDLY_SOURCE_NONE = 0
NF_DFRIENDLY_SOURCE_ASK_ITEM = 1
NF_DFRIENDLY_SOURCE_DAILY_RESET = 2
NF_DFRIENDLY_SOURCE_DAILY_RESET_BY_HB = 3

def getNpcPId(npcId):
    return ND.data.get(npcId, {}).get('npcParentId', 0)


def getNpcLv(npcPId):
    return NFND.data.get(npcPId, {}).get('npcLv', 0)


def getPFriendlyLv(npcPId, pfVal, owner):
    npcLv = getNpcLv(npcPId)
    nfPfLv = 0
    for (nLv, nfLv), data in NFNFLD.data.iteritems():
        if nLv == npcLv and data.get('friendlyBegin', 0) <= pfVal <= data.get('friendlyEnd', 0):
            nfPfLv = nfLv
            break

    while nfPfLv > 0:
        if _checkPFriendlyLvUnlock(npcPId, nfPfLv, owner):
            return nfPfLv
        nfPfLv -= 1

    return 0


def _checkPFriendlyLvUnlock(npcPId, pfLv, owner):
    lockQuest = NFNLD.data.get((npcPId, pfLv), {}).get('lockQuest', 0)
    if not lockQuest:
        return True
    elif BigWorld.component == 'base':
        return lockQuest in owner.nfPFriendlyUnlockQuest
    elif BigWorld.component == 'cell':
        return owner.getQuestFlag(lockQuest)
    elif BigWorld.component == 'client':
        return owner.getQuestFlag(lockQuest)
    else:
        return False


def getPFriendlyMaxVal(npcPId):
    npcLv = getNpcLv(npcPId)
    npcData = NFND.data.get(npcPId, {})
    maxLv = npcData.get('maxFavorLv', 0)
    if maxLv == 0:
        cnt = const.NPC_FRIENDLY_MAX_LV
        for i in range(cnt):
            nfnld = NFNFLD.data.get((npcLv, i), {})
            if nfnld and i > maxLv:
                maxLv = i
            if not nfnld:
                break

    nfnld = NFNFLD.data.get((npcLv, maxLv), {})
    return (maxLv, nfnld.get('friendlyBegin', 0), nfnld.get('friendlyEnd', 0))


def getFeatureAddProb(feature):
    fId = SCD.data.get('nfFeatureAddFId', 0)
    if not fId:
        return 0
    args = {}
    for idx, val in enumerate(feature):
        args['feature%d' % (idx + 1)] = val

    return formula.calcFormulaById(fId, args)


def getGiveItemType(item):
    if not item:
        return 0
    itemId = item.id
    if item.isEquip():
        if item.isManualEquip():
            iType = NF_GIVE_ITEM_TYPE_MANUAL_EQUIP
        else:
            iType = NF_GIVE_ITEM_TYPE_EQUIP
    elif item.isHierogramItem(itemId):
        iType = NF_GIVE_ITEM_TYPE_HIEROGRAM
    elif item.isEquipGem():
        iType = NF_GIVE_ITEM_TYPE_EQUIP_GEM
    elif item.isGuanYinNormalSkillBook():
        iType = NF_GIVE_ITEM_TYPE_GUAN_YIN_NORMAL_SKILL_BOOK
    elif item.isSpriteTextBook():
        iType = NF_GIVE_ITEM_TYPE_SPRITE_TEXT_BOOK
    else:
        iType = Item.parentId(itemId)
    return iType


def getGiveItemGId(item):
    iType = getGiveItemType(item)
    for itemGId, gData in NFGIGD.data.iteritems():
        if iType in gData.get('typeList', []):
            return itemGId

    return 0


def getFriendlyVal(item):
    if not item:
        return 0
    itemId = item.id
    itemData = ID.data.get(itemId, {})
    if not itemData:
        return 0
    itemType = itemData.get('type', 0)
    if item.isEquip():
        if item.isManualEquip():
            defaultValFId = NFGIFD.data.get(NF_GIVE_ITEM_TYPE_MANUAL_EQUIP, {}).get('formula', 0)
            makeType = item.makeType if hasattr(item, 'makeType') else 0
            args = {'makeType': makeType + 1,
             'type': itemType}
            extraCost = MECD.data.get(itemId, {}).get('extraCost', ())
            extraCost1, extraCost2 = (extraCost[0][1], extraCost[1][1]) if extraCost else (0, 0)
            extraCostDiscount = MECD.data.get(itemId, {}).get('extraCostDiscount', ())
            if extraCostDiscount:
                extraCost1, extraCost2 = extraCostDiscount[0][1], extraCostDiscount[1][1]
            args['extraCost1'] = extraCost1
            args['extraCost2'] = extraCost2
            materialSetNeed = MECD.data.get(itemId, {}).get('materialSetNeed', 0)
            itemSetData = ISSD.data.get(materialSetNeed, {})
            newItemId = itemSetData[0]['itemId'] if itemSetData else 0
            sPrice = ID.data.get(newItemId, {}).get('sPrice', 0)
            args['sPrice'] = sPrice
            args['lvReq'] = itemData.get('lvReq', 0)
            return formula.calcFormulaById(defaultValFId, args)
        else:
            defaultValFId = NFGIFD.data.get(NF_GIVE_ITEM_TYPE_EQUIP, {}).get('formula', 0)
            quality = itemData.get('quality', 0)
            lvReq = itemData.get('lvReq', 0)
            args = {'quality': quality,
             'lvReq': lvReq,
             'type': itemType}
            return formula.calcFormulaById(defaultValFId, args)
    else:
        if item.isHierogramItem(itemId):
            defaultValFId = NFGIFD.data.get(NF_GIVE_ITEM_TYPE_HIEROGRAM, {}).get('formula', 0)
            runeData = Item.getRuneCfgData(itemId)
            runeType, lv = (runeData.get('runeType', 0), runeData.get('lv', 0)) if runeData else (0, 0)
            args = {'runeType': runeType,
             'lv': lv,
             'type': itemType}
            return formula.calcFormulaById(defaultValFId, args)
        if item.isEquipGem():
            defaultValFId = NFGIFD.data.get(NF_GIVE_ITEM_TYPE_EQUIP_GEM, {}).get('formula', 0)
            gemData = EGD.data.get(Item.parentId(itemId), {})
            lv = gemData.get('lv', 0)
            args = {'lv': lv,
             'type': itemType}
            return formula.calcFormulaById(defaultValFId, args)
        if item.isGuanYinNormalSkillBook():
            defaultValFId = NFGIFD.data.get(NF_GIVE_ITEM_TYPE_GUAN_YIN_NORMAL_SKILL_BOOK, {}).get('formula', 0)
            quality = itemData.get('quality', 0)
            args = {'quality': quality,
             'type': itemType}
            return formula.calcFormulaById(defaultValFId, args)
        if item.isSpriteTextBook():
            defaultValFId = NFGIFD.data.get(NF_GIVE_ITEM_TYPE_SPRITE_TEXT_BOOK, {}).get('formula', 0)
            quality = itemData.get('quality', 0)
            args = {'quality': quality,
             'type': itemType}
            return formula.calcFormulaById(defaultValFId, args)
    return NFGIFD.data.get(Item.parentId(itemId), {}).get('defaultVal', 0)


def syncQuestInfo(npcPId, askItems, loveItems):
    Netease.nfQuestNpcPId = npcPId
    Netease.nfAskItems = askItems
    Netease.nfLoveItems = loveItems
    for e in BigWorld.entities.values():
        if not utils.instanceof(e, 'Avatar'):
            continue
        e.syncQuestInfoNF(npcPId, askItems, loveItems)


def getQuestNpcPId():
    return Netease.nfQuestNpcPId


def getQuestItemInfo(questId):
    return QD.data.get(questId, {}).get('nfItemGroupId', ())


def getAskItems():
    return Netease.nfAskItems


def getLoveItems():
    return Netease.nfLoveItems


NF_FRIENDLY_LV_INVALID = -1

class NpcFavorTopVal(UserSoleType):

    def __init__(self, maxNum = 0, leastGbId = 0, topData = {}):
        super(NpcFavorTopVal, self).__init__()
        self.maxNum = maxNum
        self.leastGbId = leastGbId
        self.topData = copy.copy(topData)

    def detectRecord(self, gbId, val, name, sex, school, borderId, photo):
        if gbId in self.topData or len(self.topData) < self.maxNum:
            self.topData[gbId] = (val,
             name,
             sex,
             school,
             borderId,
             photo,
             utils.getNow())
            self._getLeastVal()
        elif self.leastGbId and val > self.topData[self.leastGbId]:
            self.topData.pop(self.leastGbId)
            self.topData[gbId] = (val,
             name,
             sex,
             school,
             borderId,
             photo,
             utils.getNow())
            self._getLeastVal()

    def removeRecord(self, gbId):
        self.topData.pop(gbId, None)
        self._getLeastVal()

    def renameRecord(self, gbId, name):
        for g, d in self.topData.iteritems():
            if g == gbId:
                data = list(self.topData[gbId])
                data[1] = name
                self.topData[gbId] = tuple(data)
                break

    def getFirstGbId(self):
        firstGbId = 0
        for gbId, data in self.topData.iteritems():
            if not firstGbId or firstGbId not in self.topData:
                firstGbId = gbId
                continue
            firstData = self.topData[firstGbId]
            if data[0] > firstData[0] or data[0] == firstData[0] and data[-1] < firstData[-1]:
                firstGbId = gbId

        return firstGbId

    def _getLeastVal(self):
        leastGbId = 0
        for gbId, data in self.topData.iteritems():
            if not leastGbId or leastGbId not in self.topData:
                leastGbId = gbId
                continue
            leastData = self.topData[leastGbId]
            if data[0] < leastData[0] or data[0] == leastData[0] and data[-1] > leastData[-1]:
                leastGbId = gbId

        self.leastGbId = leastGbId


class NpcFavorPFriendlyTopVal(UserDictType):
    """
    {pflv: NpcFavorTopVal, ...}
    """

    def _lateReload(self):
        super(NpcFavorPFriendlyTopVal, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def getDTO(self):
        return [ (pfLv, val.topData) for pfLv, val in self.iteritems() ]

    def getFirstPFGbId(self):
        candidateLvs = self.keys()
        candidateLvs.sort(reverse=True)
        for lv in candidateLvs:
            gbId = self[lv].getFirstGbId()
            if gbId:
                return (lv, gbId)

        return (0, 0)


class NpcFavorPFriendlyTop(UserDictType):
    """
    {npcPId: NpcFavorPFriendlyTopVal, ...}
    """

    def _lateReload(self):
        super(NpcFavorPFriendlyTop, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def getOneDTO(self, npcPId):
        if npcPId in self:
            return self[npcPId].getDTO()
        return []

    def getPFLv(self, npcPId, gbId):
        pfTopVal = self.get(npcPId)
        if not pfTopVal:
            return NF_FRIENDLY_LV_INVALID
        for pfLv, topVal in pfTopVal.iteritems():
            if gbId in topVal.topData:
                return pfLv

        return NF_FRIENDLY_LV_INVALID


NF_ACTION_LOCK_INTERVAL = 600
NF_RESET_DAILY_LOCK_CRONTAB = '10 0 * * *'
NF_RESET_DAILY_REWARD_CRONTAB = '5 0 * * *'
NF_RESET_WEEKLY_REWARD_CRONTAB = '5 0 * * 0'

def checkInLockTime():
    tNow = utils.getNow()
    begin = utils.getDaySecond(tNow)
    return begin <= tNow < begin + NF_ACTION_LOCK_INTERVAL


NF_DAILY_QUEST_STAT_RECEIVE = 0
NF_DAILY_QUEST_STAT_COMPLETE = 1
NF_DAILY_QUEST_STAT_ABANDON = 2
NF_DAILY_QUEST_STAT_ACCOM = frozenset([NF_DAILY_QUEST_STAT_COMPLETE, NF_DAILY_QUEST_STAT_ABANDON])
