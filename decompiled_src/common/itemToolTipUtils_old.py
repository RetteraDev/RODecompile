#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common/itemToolTipUtils_old.o
from gamestrings import gameStrings
import datetime
import BigWorld
import gametypes
import re
import math
import copy
from item import Item
import const
from gameclass import PSkillInfo
import time
import utils
import commcalc
from gamestrings import gameStrings
import flyUpUtils
import gameconfigCommon
from data import prop_ref_data as PRD
from data import rune_data as RD
from data import new_rune_data as NRD
from data import item_data as ID
from cdata import font_config_data as FCD
from data import equip_data as ED
from data import school_data as SD
from data import sys_config_data as SYSCD
from data import fishing_lv_data as FLD
from data import consumable_item_data as CID
from data import duel_config_data as DCD
from data import equip_prefix_prop_data as EPPD
from cdata import equip_star_factor_data as ESFCD
from cdata import rune_equip_exp_data as REED
from data import special_life_skill_equip_data as SLSED
from data import explore_lv_data as ELD
from cdata import equip_star_lv_up_data as ESLD
from data import rune_equip_data as REQD
from cdata import equip_order_factor_data as EOFD
from data import composite_shop_data as CSD
from data import fame_data as FD
from data import clan_war_airdefender_data as CWAD
from cdata import equip_special_props_data as ESPD
from cdata import pskill_data as PD
from cdata import rune_tips_data as RTD
from data import life_skill_equip_data as LSED
from data import life_skill_subtype_data as LSSD
from cdata import equip_prop_fix_data as EPFD
from data import rune_qifu_effect_data as RQED
from cdata import equip_enhance_prop_data as EEPD
from data import social_school_data as SSD
from data import prop_data as PPD
from data import state_data as SDD
from data import jingjie_data as JJD
from data import equip_enhance_refining_data as EERD
from cdata import equip_suits_data as ESD
from data import avatar_data as AD
from data import physics_config_data as PCD
from data import horsewing_speed_data as HSD
from data import horsewing_upgrade_data as HUD
from cdata import horsewing_talent_level_data as HTLD
from data import sys_config_data as SCD
from cdata import life_skill_quality_data as LSQD
from cdata import equip_quality_factor_data as EQFD
from cdata import equip_enhance_juexing_prop_data as EEJPD
from cdata import manual_equip_result_reverse_data as MERRD
from cdata import yaopei_prop_data as YPD
from data import equip_random_property_data as ERPD
from data import equip_property_pool_data as EPPOOLD
from data import manual_equip_props_data as MEPD
from data import extended_equip_prop_data as XEPD
from data import yaopei_extra_prop_data as YEPD
from data import vp_level_data as VLD
from data import equip_enhance_juexing_data as EEJD
from data import explore_data as EXD
from cdata import equip_suit_show_data as ESSD
from cdata import yaopei_lv_data as YLD
from cdata import guanyin_data as GD
from cdata import guanyin_book_data as GBD
from cdata import pskill_template_data as PTD
from cdata import hiero_equip_data as HED
from cdata import hiero_awake_rule_data as HARD
from cdata import pskill_data as PSD
from data import skill_general_data as SGD
from data import quest_data as QD
from data import gui_bao_ge_config_data as GBDCD
from data import gui_bao_ge_data as GBGD
from data import fight_for_love_config_data as FFLCD
from cdata import gui_bao_ge_item_reverse_data as GBGIRD
if BigWorld.component == 'client':
    from data import formula_client_data as FMD
else:
    from data import formula_server_data as FMD
BOOTH_SLOTS_SELL = 0
BOOTH_SLOTS_BUY = 1
NO_BOOTH = 0
NO_SELL = 1
NO_STORAGE = 2
NO_DISCARD = 3
NO_TRADE = 4
NO_ENHANCE = 5
NO_REPAIR = 6
NO_BUYBACK = 7
NO_Dye = 8
NO_MAIL = 9
NO_CONSIGN = 10
NO_LATCH = 11
NO_RETURN = 12
NO_BUYBACK_NORMAL = 13
NO_BUYBACK_POPULARITY = 14
NO_RUBBING = 15
RUNE_FORGING_LOW_LV = 1
RUNE_FORGING_LHIGH_LV = 2
PHYSICAL_ATTACK_DOWN = 118
PHYSICAL_ATTACK_UP = 119
SPELL_ATTACK_DOWN = 120
SPELL_ATTACK_UP = 121
MAX_SINGLE_PRICE = 10000000
ATTACK_PROP = frozenset([PHYSICAL_ATTACK_DOWN,
 PHYSICAL_ATTACK_UP,
 SPELL_ATTACK_DOWN,
 SPELL_ATTACK_UP])
PROPS_SHOW_SHRINK = (190,
 191,
 290,
 291,
 390,
 391,
 490,
 491)
LIFE_SKILL_EQUIP_LIST = ['identifyProb',
 'identifyQuality',
 'succProb',
 'lvUp']
LIFE_SKILL_EQUIP = {'identifyProb': (gameStrings.TEXT_ITEMTOOLTIPUTILS_130, 100),
 'identifyQuality': (gameStrings.TEXT_ITEMTOOLTIPUTILS_130_1, 1000),
 'succProb': (gameStrings.TEXT_ITEMTOOLTIPUTILS_130_2, 100),
 'lvUp': (gameStrings.TEXT_ITEMTOOLTIPUTILS_130_3, (gameStrings.TEXT_PRESSKEYFPROXY_29_2, 1))}
LIFE_SKILL = {1: gameStrings.TEXT_LIFESKILLFACTORY_1626,
 2: gameStrings.TEXT_ITEMTOOLTIPUTILS_131_1,
 3: gameStrings.TEXT_ITEMTOOLTIPUTILS_131_2,
 6: gameStrings.TEXT_GAMECONST_1211,
 7: gameStrings.TEXT_ITEMTOOLTIPUTILS_131_3,
 8: gameStrings.TEXT_ITEMTOOLTIPUTILS_131_4,
 9: gameStrings.TEXT_ITEMTOOLTIPUTILS_131_5,
 10: gameStrings.TEXT_ITEMTOOLTIPUTILS_131_6,
 11: gameStrings.TEXT_ITEMTOOLTIPUTILS_131_7}

def float2Int(num):
    return int(num)


def calAttrVal(item, location = 0):
    basic = []
    rand = []
    enh = []
    basicShift = []
    randShift = []
    maxEnhlv = getattr(item, 'maxEnhlv', 0)
    enhanceRefining = getattr(item, 'enhanceRefining', {})
    equipType = getattr(item, 'equipType', 0)
    equipSType = getattr(item, 'equipSType', 0)
    enhanceType = getattr(item, 'enhanceType', 0)
    if BigWorld.component == 'client' and location == const.ITEM_IN_EQUIPMENT:
        p = BigWorld.player()
        part = p.getEquipPart(item)
        mainEquip = p.equipment.get(part)
        subEquip = commcalc.getAlternativeEquip(p, part)
        if mainEquip and mainEquip.uuid == item.uuid:
            enhCalcData = commcalc.getEquipShareEnhProp(p, mainEquip, subEquip)
        elif subEquip and subEquip.uuid == item.uuid:
            enhCalcData = commcalc.getEquipShareEnhProp(p, subEquip, mainEquip)
        else:
            enhCalcData = {}
        if commcalc.enableShareEquipProp(p) and enhCalcData:
            maxEnhlv = enhCalcData['maxEnhlv']
            enhanceRefining = enhCalcData['enhanceRefining']
            equipType = enhCalcData['equipType']
            equipSType = enhCalcData['equipSType']
            enhanceType = enhCalcData['enhanceType']
    if hasattr(item, 'starLv'):
        starLevel = item.addedStarLv
    else:
        starLevel = 0
    quality = getattr(item, 'quality', 1)
    if not quality:
        quality = 1
    qualityFactor = EQFD.data.get(quality, {}).get('factor', 1.0)
    starFactor = ESFCD.data.get(starLevel, {}).get('factor', 1.0)
    if hasattr(item, 'props'):
        for idx, (pId, pType, pVal) in enumerate(item.props):
            if pType == gametypes.DATA_TYPE_NUM and item._isIntPropRef(pId):
                basic.append((pId,
                 pType,
                 float2Int(pVal * starFactor * qualityFactor),
                 idx))
                basicShift.append((pId,
                 float2Int(pVal * qualityFactor),
                 (starFactor - 1) * 100,
                 idx))
            else:
                basic.append((pId,
                 pType,
                 pVal * starFactor * qualityFactor,
                 idx))
                basicShift.append((pId,
                 float2Int(pVal * qualityFactor),
                 (starFactor - 1) * 100,
                 idx))

    if hasattr(item, 'rprops'):
        if item.isYaoPei():
            qualityFactor = 1
            starFactor = 1
        for idx, (pId, pType, pVal) in enumerate(item.rprops):
            valFactor = starFactor
            if BigWorld.component == 'client':
                p = BigWorld.player()
                if gameconfigCommon.enableNewLv89():
                    valFactor = starFactor + item.isSesMaker(p.gbId)
            if pType == gametypes.DATA_TYPE_NUM and item._isIntPropRef(pId):
                rand.append((pId,
                 pType,
                 round(int(pVal * valFactor * qualityFactor * 10) / 10.0, 1),
                 idx))
                randShift.append((pId,
                 round(int(pVal * qualityFactor * 10) / 10.0, 1),
                 (valFactor - 1) * 100,
                 idx))
            else:
                rand.append((pId,
                 pType,
                 pVal * valFactor * qualityFactor,
                 idx))
                randShift.append((pId,
                 pVal * qualityFactor,
                 (valFactor - 1) * 100,
                 idx))

        rand = [ [r[0],
         r[1],
         r[2],
         PRD.data.get(r[0], {}).get('priorityLevel', 0),
         r[3]] for r in rand ]
        rand.sort(key=lambda k: k[3])
        randShift = [ [r[0],
         r[1],
         r[2],
         PRD.data.get(r[0], {}).get('priorityLevel', 0),
         r[3]] for r in randShift ]
        randShift.sort(key=lambda k: k[3])
    if enhanceRefining:
        enhMaxLv = maxEnhlv
        refiningFactor = 0
        loseUseFactor = 0
        for key in enhanceRefining:
            refiningFactor += enhanceRefining[key]
            if key > enhMaxLv:
                loseUseFactor += enhanceRefining[key]

    else:
        refiningFactor = 0
    if refiningFactor != 0:
        if item.isEquip():
            enhanceData = EEPD.data.get((equipType, equipSType, enhanceType))
            if enhanceData:
                orderFactor = EOFD.data.get(item.addedOrder, {}).get('factor', 1.0)
                for pId, pType, value in enhanceData.get('enhProps', []):
                    if pType == gametypes.DATA_TYPE_NUM and item._isIntPropRef(pId):
                        val = float2Int(value * orderFactor * refiningFactor)
                        loseVal = float2Int(value * orderFactor * loseUseFactor)
                    else:
                        val = value * orderFactor * refiningFactor
                        loseVal = value * orderFactor * loseUseFactor
                    enh.append((pId,
                     pType,
                     val,
                     loseVal))

    enh = _mergeProps(enh)
    enh = [ [e[0],
     e[1],
     e[2],
     PRD.data.get(e[0], {}).get('priorityLevel', 0),
     PRD.data.get(e[0], {}).get('showColor', ''),
     e[3]] for e in enh ]
    enh.sort(key=lambda k: k[3])
    return (basic,
     rand,
     enh,
     basicShift,
     randShift)


def _mergeProps(props):
    propMap = {}
    for prop in props:
        if propMap.has_key(prop[0]):
            propMap[prop[0]][1] += prop[2]
            propMap[prop[0]][2] += prop[3]
        else:
            propMap[prop[0]] = [prop[1], prop[2], prop[3]]

    ret = [ [key,
     val[0],
     val[1],
     val[2]] for key, val in propMap.items() ]
    return ret


def _addBindInfo(it, isInBag = True, bRelative = False):
    bindInfo = ''
    if Item.isDotaBattleFieldItem(it.id):
        return bindInfo
    if hasattr(it, 'bindType'):
        if it.bindType == gametypes.ITEM_BIND_TYPE_FOREVER:
            bindInfo = gameStrings.TEXT_ITEMTOOLTIPUTILS_262 if isInBag or bRelative else gameStrings.TEXT_ITEMTOOLTIPUTILS_262_1
        elif it.bindType == gametypes.ITEM_BIND_TYPE_EQUIP:
            bindInfo = gameStrings.TEXT_ITEMTOOLTIPUTILS_264
        elif it.bindType == gametypes.ITEM_BIND_TYPE_USE:
            bindInfo = gameStrings.TEXT_ITEMTOOLTIPUTILS_266
    if it.canBeIdentified():
        bindInfo = gameStrings.TEXT_ITEMTOOLTIPUTILS_268
    return bindInfo


def _addDyeTypeFromChannel(it, channels):
    dyeDesc = ''
    descArray = [gameStrings.TEXT_BATTLEFIELDPROXY_1605, gameStrings.TEXT_BATTLEFIELDPROXY_1605, gameStrings.TEXT_BATTLEFIELDPROXY_1605]
    lastIndex = -1
    for i, channel in enumerate(channels):
        for material in it.dyeMaterials:
            if channel == material[0]:
                lastIndex = i
                dyeItemId = material[1]
                dyeMethod = material[2]
                desc = ID.data.get(dyeItemId, {}).get('name', gameStrings.TEXT_BATTLEFIELDPROXY_1605)
                if dyeMethod == const.DYE_BLEND:
                    desc += gameStrings.TEXT_ITEMTOOLTIPUTILS_283
                descArray[i] = desc
                break

    if lastIndex != -1:
        dyeDesc = '+'.join(descArray[0:lastIndex + 1])
    return dyeDesc


def _addDyeType(i):
    dyeDesc = ''
    if i.isEquip() and i.equipType in (Item.EQUIP_BASETYPE_ARMOR, Item.EQUIP_BASETYPE_FASHION):
        if i.isCanDye():
            if hasattr(i, 'dyeList') and i.dyeList:
                if hasattr(i, 'dyeMaterials') and i.dyeMaterials:
                    if i.isFashionEquip():
                        dyeDesc = _addDyeTypeFromChannel(i, (const.DYE_CHANNEL_1, const.DYE_CHANNEL_2, const.DYE_CHANNEL_TEXTURE))
                    else:
                        dyeDesc = _addDyeTypeFromChannel(i, (const.DYE_CHANNEL_TEXTURE,))
                        if not dyeDesc:
                            dyeDesc = _addDyeTypeFromChannel(i, (const.DYE_CHANNEL_1, const.DYE_CHANNEL_2, const.DYE_CHANNEL_3))
                else:
                    dyeDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_305
            else:
                dyeDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_305
        elif hasattr(i, 'realDyeId'):
            dyeDesc = ID.data.get(i.realDyeId, {}).get('name', '')
    return dyeDesc


def _addDyeTTLExpireTime(i):
    dyeTTLExpireTime = ''
    now = getServerTime()
    if hasattr(i, 'dyeTTLExpireTime') and i.dyeTTLExpireTime:
        if now < i.dyeTTLExpireTime:
            str = utils.formatDuration(i.dyeTTLExpireTime - now)
            dyeTTLExpireTime = gameStrings.TEXT_ITEMTOOLTIPUTILS_318 + str
    if hasattr(i, 'rongGuangExpireTime') and i.rongGuangExpireTime and now < i.rongGuangExpireTime:
        if dyeTTLExpireTime:
            dyeTTLExpireTime += '\n'
        str = utils.formatDuration(i.rongGuangExpireTime - now)
        dyeTTLExpireTime += gameStrings.TEXT_ITEMTOOLTIPUTILS_323 + str
    elif i.isCanRongGuang():
        if dyeTTLExpireTime:
            dyeTTLExpireTime += '\n'
        dyeTTLExpireTime += gameStrings.TEXT_ITEMTOOLTIPUTILS_327
    return "<font color=\'#FFFFE7\'>" + dyeTTLExpireTime + '</font>'


def formatLimitArray(i):
    ret = []
    iData = ID.data.get(i.id, {})
    if utils.getItemNoBooth(iData) == 1:
        ret.append(NO_BOOTH)
    if utils.getItemNoDrop(iData) == 1:
        ret.append(NO_DISCARD)
    if utils.getItemNoSell(iData):
        ret.append(NO_SELL)
    if i.isItemNoTrade():
        ret.append(NO_TRADE)
    if utils.getItemNoMail(iData) == 1:
        ret.append(NO_MAIL)
    if utils.getItemNoConsign(iData) == 1:
        ret.append(NO_CONSIGN)
    if not i.canMoveToStorage():
        ret.append(NO_STORAGE)
    if utils.getItemNoLatch(iData) == 1:
        ret.append(NO_LATCH)
    if i.isEquip() and utils.getItemNoRepair(iData) == 1:
        ret.append(NO_REPAIR)
    if utils.getItemNoReturn(iData) == 1:
        ret.append(NO_RETURN)
    if NO_SELL not in ret:
        if iData.get('noBuyBack', None) == 1:
            ret.append(NO_BUYBACK)
    if i.isEquip() and i.equipType in (Item.EQUIP_BASETYPE_ARMOR, Item.EQUIP_BASETYPE_FASHION) and i.isCanDye() == False:
        ret.append(NO_Dye)
    if i.isEquip() and i.equipType in (Item.EQUIP_BASETYPE_ARMOR, Item.EQUIP_BASETYPE_WEAPON) and not i.isCanRubbing():
        ret.append(NO_RUBBING)
    if utils.getItemNotShowConsign(iData) == 1 and NO_CONSIGN in ret:
        ret.remove(NO_CONSIGN)
    return filterLimit(i, ret)


def formatShopLimitArray(i):
    ret = []
    iData = ID.data.get(i.id, {})
    if NO_SELL not in ret:
        if iData.get('noBuyBack', None) == 2:
            ret.append(NO_BUYBACK_NORMAL)
        elif iData.get('noBuyBack', None) == 3:
            ret.append(NO_BUYBACK_POPULARITY)
    return ret


def filterLimit(i, l):
    bindFilter = [NO_TRADE,
     NO_MAIL,
     NO_CONSIGN,
     NO_BOOTH]
    if i.isForeverBind():
        for k in bindFilter:
            if k in l:
                l.remove(k)

    return l


def getAdditionalLimits(i):
    ret = ''
    if i.isItemApprenticeOnly():
        if not i.isForeverBind():
            ret += gameStrings.TEXT_ITEMTOOLTIPUTILS_409
    return ret


def getServerTime():
    if BigWorld.component == 'client':
        t = BigWorld.player().getServerTime()
    else:
        t = time.time()
    return t


def initData():
    if SCD.data.has_key('equipTypeMap'):
        equipTypeMap = SCD.data.get('equipTypeMap')
    else:
        equipTypeMap = {1: {1: gameStrings.TEXT_ITEMTOOLTIPUTILS_426,
             2: gameStrings.TEXT_ITEMTOOLTIPUTILS_426_1},
         2: {1: gameStrings.TEXT_ITEMTOOLTIPUTILS_427,
             2: gameStrings.TEXT_ITEMTOOLTIPUTILS_427_1,
             3: gameStrings.TEXT_ITEMTOOLTIPUTILS_427_2,
             4: gameStrings.TEXT_ITEMTOOLTIPUTILS_427_3,
             5: gameStrings.TEXT_ITEMTOOLTIPUTILS_427_4,
             6: gameStrings.TEXT_ITEMTOOLTIPUTILS_427_5,
             7: gameStrings.TEXT_EQUIPMIXNEWPROXY_189,
             8: gameStrings.TEXT_TIANYUMALLPROXY_3415},
         3: {1: gameStrings.TEXT_ITEMTOOLTIPUTILS_428,
             2: gameStrings.TEXT_ITEMTOOLTIPUTILS_428_1,
             3: gameStrings.TEXT_ITEMTOOLTIPUTILS_428_2,
             4: gameStrings.TEXT_ITEMTOOLTIPUTILS_428_3}}
    if SCD.data.has_key('gemEquipTypeMap'):
        gemEquipTypeMap = SCD.data.get('gemEquipTypeMap')
    else:
        gemEquipTypeMap = {1: gameStrings.TEXT_EQUIPMIXNEWPROXY_183,
         2: gameStrings.TEXT_EQUIPMIXNEWPROXY_185,
         3: gameStrings.TEXT_EQUIPMIXNEWPROXY_187}
    if SCD.data.has_key('fashionTypeMap'):
        fashionTypeMap = SCD.data.get('fashionTypeMap')
    else:
        fashionTypeMap = {1: gameStrings.TEXT_ITEMTOOLTIPUTILS_443,
         2: gameStrings.TEXT_ITEMTOOLTIPUTILS_443_1,
         3: gameStrings.TEXT_ITEMTOOLTIPUTILS_443_2,
         4: gameStrings.TEXT_ITEMTOOLTIPUTILS_443_3,
         5: gameStrings.TEXT_ITEMTOOLTIPUTILS_443_4,
         6: gameStrings.TEXT_ITEMTOOLTIPUTILS_443_5,
         7: gameStrings.TEXT_ITEMTOOLTIPUTILS_443_6,
         8: gameStrings.TEXT_ITEMTOOLTIPUTILS_443_7,
         9: gameStrings.TEXT_ITEMTOOLTIPUTILS_443_8,
         10: gameStrings.TEXT_ITEMTOOLTIPUTILS_443_9,
         11: gameStrings.TEXT_ITEMTOOLTIPUTILS_443_10,
         12: gameStrings.TEXT_ITEMTOOLTIPUTILS_443_11,
         13: gameStrings.TEXT_ITEMTOOLTIPUTILS_443_5,
         14: gameStrings.TEXT_ITEMTOOLTIPUTILS_443_5,
         15: gameStrings.TEXT_ITEMTOOLTIPUTILS_443_13,
         16: gameStrings.TEXT_ITEMTOOLTIPUTILS_443_14,
         18: gameStrings.TEXT_ITEMTOOLTIPUTILS_443_15}
    return (equipTypeMap, gemEquipTypeMap, fashionTypeMap)


def getMallUseTimeData(i, isInBag, isInChat, bRelative):
    gameStrings.TEXT_ITEMTOOLTIPUTILS_448
    itemData = ID.data.get(i.id, {})
    useTime = {}
    expireTime = 0
    mallBuyTime = 0
    if i.isOneMall():
        mallBuyTime = i._mallBuyTime
    commonExpireTime = i.getCommonExpireTime()
    if not isInChat and (isInBag or bRelative):
        expireTime = i.getTTLExpireTimeForItem()
    else:
        expireTime = itemData.get('ttl', 0)
    hasExpireTime = expireTime > 0
    if i.getTTLExpireType() in (const.TTL_EXPIRE_TYPE_NORMAL, const.TTL_EXPIRE_TYPE_REMOVE) and itemData.get('commonExpireTime', ''):
        if commonExpireTime < 0:
            commonExpireTime = utils.getDisposableCronTabTimeStamp(itemData.get('commonExpireTime', ''))
        timeArray = time.localtime(commonExpireTime)
        useTime['expireDate'] = gameStrings.ITEM_TOOL_EXPIRE_DATE % (timeArray.tm_year,
         timeArray.tm_mon,
         timeArray.tm_mday,
         timeArray.tm_hour,
         timeArray.tm_min)
    useTime['commonExpireTime'] = i.getCommonExpireTime()
    if hasattr(i, 'ownershipPercent'):
        useTime['ownerShipPercent'] = i.getOwnershipPercent()
    else:
        useTime['ownerShipPercent'] = -1
    useTime['isOneMall'] = i.isOneMall()
    canUseStartTime = itemData.get('canUseStartTime', '')
    remainTime = 0
    if canUseStartTime:
        remainTime = utils.getDisposableCronTabTimeStamp(canUseStartTime)
    useTime['canUseStartTime'] = remainTime
    useTime['expireTime'] = expireTime
    useTime['mallBuyTime'] = mallBuyTime
    useTime['hasExpireTime'] = hasExpireTime
    useTime['inBag'] = isInBag
    useTime['fashionCanRenewable'] = i.isMallFashionRenewable()
    useTime['canRenewable'] = itemData.get('canRenewal', False)
    useTime['notShowExpireTime'] = itemData.get('notShowExpireTime', False)
    return useTime


def getEquipSkillDesc(p, i, fullAppAPIDesc = False):
    equipSkillDesc = ''
    if BigWorld.component == 'client' and not Item.isDotaBattleFieldItem(i.id):
        if i.type == Item.BASETYPE_EQUIP:
            if not i.isYaoPei():
                equipSkillInfo = i.getSkillVal()
                if equipSkillInfo:
                    skillInfo = p.getSkillTipsInfo(equipSkillInfo[0], equipSkillInfo[1])
                    mainEff = skillInfo.getSkillData('mainEff', '')
                    equipSkillDesc = skillInfo.getSkillData('shortMainEff', mainEff)
            else:
                yaoPeiSkillId = getattr(i, 'yaoPeiSkillId', 0)
                if yaoPeiSkillId != 0:
                    yaopeiLv = i.getYaoPeiLv()
                    yaopeiSkillLv = YLD.data.get(yaopeiLv, {}).get('skillLv', 0)
                    skillInfo = p.getSkillTipsInfo(yaoPeiSkillId, yaopeiSkillLv if yaopeiSkillLv > 0 else 1)
                    mainEff = skillInfo.getSkillData('mainEff', '')
                    equipSkillDesc = skillInfo.getSkillData('shortMainEff', mainEff)
                    if yaopeiSkillLv == 0:
                        equipSkillDesc = skillInfo.getSkillData('shortMainEffGray', equipSkillDesc)
                    if yaopeiSkillLv > 0:
                        equipSkillDesc = "<font color = \'#FF7F00\'>" + equipSkillDesc + '</font>'
                    else:
                        equipSkillDesc = "<font color = \'#808080\'>" + equipSkillDesc + '</font>'
    elif i.isYaoPei():
        yaoPeiSkillId = getattr(i, 'yaoPeiSkillId', 0)
        if yaoPeiSkillId != 0:
            if fullAppAPIDesc:
                yaopeiSkillLv = YLD.data.get(SCD.data.get('maxYaoPeiLv', 20), {}).get('skillLv', 4)
                if (yaoPeiSkillId, yaopeiSkillLv) in SGD.data:
                    return gameStrings.TEXT_ITEMTOOLTIPUTILS_525 % SGD.data.get((yaoPeiSkillId, yaopeiSkillLv)).get('name', gameStrings.TEXT_DEBUGPROXY_101)
                for i in xrange(yaopeiSkillLv, 0, -1):
                    if (yaoPeiSkillId, i) in SGD.data:
                        return gameStrings.TEXT_ITEMTOOLTIPUTILS_525 % SGD.data.get((yaoPeiSkillId, i), {}).get('name', gameStrings.TEXT_DEBUGPROXY_101)

            else:
                yaopeiLv = i.getYaoPeiLv()
                yaopeiSkillLv = YLD.data.get(yaopeiLv, {}).get('skillLv', 0)
                return gameStrings.TEXT_ITEMTOOLTIPUTILS_533 % (yaoPeiSkillId, yaopeiSkillLv)
    return equipSkillDesc


def getYaopeiSkillInfo(p, i):
    skillName = ''
    skillLv = ''
    if BigWorld.component == 'client':
        from data import skill_general_template_data as SGTD
        if i.type == Item.BASETYPE_EQUIP:
            if i.isYaoPei():
                yaoPeiSkillId = getattr(i, 'yaoPeiSkillId', 0)
                if yaoPeiSkillId != 0:
                    yaopeiLv = i.getYaoPeiLv()
                    yaopeiSkillLv = YLD.data.get(yaopeiLv, {}).get('skillLv', 0)
                    skillLv = 'Lv.%d' % yaopeiSkillLv if yaopeiSkillLv > 0 else ''
                    skillName = '[%s]' % SGTD.data.get(yaoPeiSkillId, {}).get('name', '')
                    if yaopeiSkillLv == 0:
                        activeLv = getSkillActiveLv()
                        skillName += gameStrings.TEXT_ITEMTOOLTIPUTILS_552 % activeLv
                    if yaopeiSkillLv > 0:
                        skillName = "<font color = \'#FF7F00\'>" + skillName + '</font>'
                    else:
                        skillName = "<font color = \'#808080\'>" + skillName + '</font>'
    elif i.isYaoPei():
        yaoPeiSkillId = getattr(i, 'yaoPeiSkillId', 0)
        if yaoPeiSkillId != 0:
            yaopeiLv = i.getYaoPeiLv()
            yaopeiSkillLv = YLD.data.get(yaopeiLv, {}).get('skillLv', 0)
            skillLv = 'Lv.%d' % yaopeiSkillLv if yaopeiSkillLv > 0 else ''
            skillName = '%d' % yaoPeiSkillId
    return (skillName, skillLv)


def getSkillActiveLv():
    data = YLD.data
    for key in sorted(data.keys()):
        yaopeiData = data[key]
        skillLv = yaopeiData.get('skillLv', 0)
        if skillLv > 0:
            return key

    return 0


def getItemName(i, isInBag, bRelative):
    itemName = ''
    if hasattr(i, 'name'):
        itemName = i.name
        if hasattr(i, 'prefixInfo') and (isInBag or bRelative) and not i.isYaoPei():
            for prefixItem in EPPD.data.get(i.prefixInfo[0], []):
                if prefixItem['id'] == i.prefixInfo[1]:
                    if utils.isInternationalVersion():
                        itemName = i.name + prefixItem['name'] + i.getNameSuffix()
                    else:
                        itemName = prefixItem['name'] + i.name + i.getNameSuffix()
                    break
                else:
                    itemName = i.name + i.getNameSuffix()

        else:
            itemName = i.name + i.getNameSuffix()
    return itemName


def getTianAndDiLunSlotNum(i, isRuneEquipHasProp):
    tianlunSlotNum = ''
    if i.type == Item.BASETYPE_RUNE_EQUIP and isRuneEquipHasProp:
        tianlunSlotNum = gameStrings.TEXT_ITEMTOOLTIPUTILS_602 % i.getRuneEquipSlotNum(const.RUNE_TYPE_TIANLUN)
    dilunSlotNum = ''
    if i.type == Item.BASETYPE_RUNE_EQUIP and isRuneEquipHasProp:
        dilunSlotNum = gameStrings.TEXT_ITEMTOOLTIPUTILS_606 % i.getRuneEquipSlotNum(const.RUNE_TYPE_DILUN)
    return (tianlunSlotNum, dilunSlotNum)


def getReturnTime(i):
    returnTime = ''
    compositeShopInfo = getattr(i, 'compositeShopInfo', None)
    if compositeShopInfo and getServerTime() - compositeShopInfo[0] < SYSCD.data.get('timeToReturnShop', 600):
        returnTime = SYSCD.data.get('timeToReturnShop', 600) - (getServerTime() - compositeShopInfo[0])
        if returnTime <= 60:
            returnTime = gameStrings.TEXT_ITEMTOOLTIPUTILS_616 % returnTime
        elif returnTime <= 3600:
            returnTime = gameStrings.TEXT_ITEMTOOLTIPUTILS_618 % (returnTime / 60)
        elif returnTime <= 86400:
            returnTime = gameStrings.TEXT_ITEMTOOLTIPUTILS_620 % (returnTime / 3600)
        else:
            returnTime = gameStrings.TEXT_ITEMTOOLTIPUTILS_622 % (returnTime / 3600 / 24)
    return returnTime


def getFreezeUseTime(i):
    ret = 0
    if hasattr(i, 'freezeUseTime'):
        ret = i.freezeUseTime
    return ret


def getJingjieLimit(p, i):
    jingjie = ''
    itemData = ID.data.get(i.id, {})
    needJingJieId = itemData.get('needJingJie', -1)
    if needJingJieId == -1:
        jingjie = ''
    else:
        needJingJieName = JJD.data.get(needJingJieId, {}).get('name', gameStrings.TEXT_COMPOSITESHOPHELPFUNC_324)
        jingjie += gameStrings.TEXT_SKILLPROXY_4312 + needJingJieName
        if p and p.jingJie < needJingJieId:
            jingjie = "<font color = \'#F43804\'>" + jingjie + '</font>'
    return jingjie


def getSexReq(p, i):
    sexReq = ''
    itemData = ID.data.get(i.id, {})
    physique = getattr(p, 'physique', None)
    playerSex = getattr(physique, 'sex', -1)
    if playerSex != -1:
        itemSexReq = itemData.get('sexReq', 0)
        if itemSexReq != 0:
            if itemSexReq == 1:
                sexReq = gameStrings.TEXT_ITEMTOOLTIPUTILS_657
            else:
                sexReq = gameStrings.TEXT_ITEMTOOLTIPUTILS_659
            if itemSexReq == playerSex:
                sexReq = "<font color = \'#FFFFE7\'>" + sexReq + '</font>'
            else:
                sexReq = "<font color = \'#F43804\'>" + sexReq + '</font>'
    return sexReq


def getNewStarLv(i, location):
    newStarLv = {}
    if not hasattr(i, 'activeStarLv') or location == const.ITEM_IN_GUIBAOGE:
        newStarLv['activeStarLv'] = 0
        newStarLv['inactiveStarLv'] = 0
        newStarLv['starLv'] = 0
        newStarLv['maxStarLv'] = -1
        newStarLv['starExp'] = 0
        newStarLv['seExtraStarLv'] = 0
    else:
        newStarLv['activeStarLv'] = i.activeStarLv
        newStarLv['inactiveStarLv'] = i.inactiveStarLv
        newStarLv['starLv'] = i.starLv
        if _checkFashionType(i):
            newStarLv['maxStarLv'] = -1
        else:
            newStarLv['maxStarLv'] = i.maxStarLv
        newStarLv['seExtraStarLv'] = int(i.seExtraStarLv)
        newStarLv['starExp'] = i.starExp
    return newStarLv


def _checkFashionType(item):
    if getattr(item, 'type', 0) == Item.BASETYPE_EQUIP and getattr(item, 'equipType', 0) == Item.EQUIP_BASETYPE_FASHION:
        return True
    return False


def getShiHunInfo(i):
    shihunInfo = ''
    if hasattr(i, '_shihunEquip') and hasattr(i, '_shihunRole'):
        equipName = ID.data.get(i._shihunEquip, {}).get('name', '')
        shihunInfo = gameStrings.TEXT_ITEMTOOLTIPUTILS_698 + equipName + '</font>\n' + gameStrings.TEXT_ITEMTOOLTIPUTILS_698_1 + i._shihunRole + '</font>'
    shihunExpire = ''
    if i.isShihun() and i.getShihunExpireTime():
        restoreTime = utils.formatDatetime(i.getShihunExpireTime())
        costItem = utils.findItemCost(i)
        costItemName = ID.data.get(costItem[0][0], {}).get('name', '')
        num = costItem[0][1]
        shihunExpire = gameStrings.TEXT_ITEMTOOLTIPUTILS_706 + restoreTime + '</font>\n' + gameStrings.TEXT_ITEMTOOLTIPUTILS_707 + costItemName + 'X' + str(num) + '</font>'
    return (shihunInfo, shihunExpire)


def getLearnDesc(p, i):
    learnDesc = ''
    if getattr(i, 'cstype', None) == Item.SUBTYPE_2_SKILL_BOOK:
        skId = CID.data.get(i.id, {}).get('learnSkillId', -1)
        wsSkills = getattr(p, 'wsSkills', {})
        if not wsSkills.has_key(skId):
            learnDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_717
        else:
            learnDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_719
    elif getattr(i, 'cstype', None) == Item.SUBTYPE_2_SKILL_ENHANCE:
        skId = CID.data.get(i.id, {}).get('enhanceSkillId', -1)
        enhId = CID.data.get(i.id, {}).get('enhanceSkillPart', -1)
        skills = getattr(p, 'skills', {})
        skVal = skills.get(skId, None)
        if not skVal or not skVal.enhanceData.has_key(enhId):
            learnDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_717
        else:
            learnDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_719
    elif getattr(i, 'cstype', None) == Item.SUBTYPE_2_FAME_COLLECT:
        fameCollectInfo = getattr(p, 'fameCollectInfo')
        fcid = CID.data.get(i.id, {}).get('fameCollectId', -1)
        if not commcalc.getBit(fameCollectInfo, fcid):
            learnDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_734
        else:
            learnDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_736
    elif getattr(i, 'cstype', None) == Item.SUBTYPE_2_AIR_SKILL_BOOK:
        skId = CID.data.get(i.id, {}).get('learnSkillId', -1)
        airSkills = getattr(p, 'airSkills', {})
        if not airSkills.has_key(skId):
            learnDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_717
        else:
            learnDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_719
    elif getattr(i, 'cstype', None) == Item.SUBTYPE_2_ABILITY_BOOK:
        skId = CID.data.get(i.id, {}).get('abilityId', -1)
        if p.abilityIds.has_key(skId):
            learnDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_719
        else:
            learnDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_717
    return learnDesc


def getPriceInfo(p, i, bRelative, isInBag, isInBooth, inRepair, isCompositeShop, extraData, page):
    itemData = ID.data.get(i.id, {})
    sPriceType = itemData.get('sPriceType', gametypes.ITEM_PRICE_TYPE_BIND_CASH)
    priceLabel = ''
    boothLabel = ''
    price = 0
    boothPrice = 0
    if not bRelative and isInBooth and page == BOOTH_SLOTS_SELL and hasattr(i, 'price'):
        price = i.price
        priceLabel = gameStrings.TEXT_ITEMTOOLTIPUTILS_764
        boothPrice = i.price * i.cwrap
        boothLabel = gameStrings.TEXT_ITEMTOOLTIPUTILS_766
        if price > MAX_SINGLE_PRICE:
            priceLabel = gameStrings.TEXT_ITEMTOOLTIPUTILS_768
            boothLabel = gameStrings.TEXT_IMPITEM_2349
        sPriceType = itemData.get('bPriceType', gametypes.ITEM_PRICE_TYPE_CASH)
    elif not bRelative and isInBooth and page == BOOTH_SLOTS_BUY and hasattr(i, 'price'):
        price = i.price
        priceLabel = gameStrings.TEXT_ITEMTOOLTIPUTILS_774
        boothPrice = i.cwrap
        boothLabel = gameStrings.TEXT_ITEMTOOLTIPUTILS_776
        sPriceType = itemData.get('bPriceType', gametypes.ITEM_PRICE_TYPE_CASH)
    elif isCompositeShop and extraData:
        price = priceLabel = ''
        boothLabel = boothPrice = ''
    else:
        price = i.sPrice
        priceLabel = gameStrings.TEXT_ITEMTOOLTIPUTILS_785
        if not isInBag:
            price = i.sPrice
            priceLabel = ''
            sPriceType = itemData.get('sPriceType', gametypes.ITEM_PRICE_TYPE_BIND_CASH)
        if inRepair:
            if i.isEquip() and i.canRepair():
                school = getattr(p, 'school', const.SCHOOL_SHENTANG)
                lv = getattr(p, 'lv', 1)
                price = i.repairCost(school, lv)
                priceLabel = gameStrings.TEXT_ITEMTOOLTIPUTILS_795
        boothLabel = boothPrice = ''
        if not i.canSell(shopType=getattr(p, 'openShopType', 0)):
            price = ''
            priceLabel = ''
    return (sPriceType,
     priceLabel,
     boothLabel,
     price,
     boothPrice)


def getSignDesc(i):
    signDesc = ''
    if getattr(i, 'hideSign', 0):
        return ''
    signCode = getattr(i, 'signCode', '')
    signName = getattr(i, 'signName', '')
    if signCode and signName:
        signDesc = signName + ':\n' + signCode
    HTML_SPACIAL_CHARS = [('<', '&lt;'), ('>', '&gt;')]
    for x, y in HTML_SPACIAL_CHARS:
        signDesc = signDesc.replace(x, y)

    return signDesc


def getExtraProp(i, maxStarLv):
    extraSkill = ''
    extraProp = ''
    if i.isYaoPei():
        return (extraSkill, extraProp)
    if i.isAddStarExpItem():
        if i.isEquipStarExpItem():
            equipStarExp = CID.data.get(i.id, {}).get('equipStarExp', 0)
            extraProp = SCD.data.get('disassembleStarExpTip', '%s') % format(equipStarExp, ',')
            return (extraSkill, extraProp)
        else:
            disassembleStarExp = format(getattr(i, 'disassembleStarExp', 0), ',')
            extraProp = SCD.data.get('disassembleStarExpTip', '%s') % disassembleStarExp
            return (extraSkill, extraProp)
    if i.isGuanYinNormalSkillBook() or i.isGuanYinSuperSkillBook():
        bookInfo = GBD.data.get(i.id, {})
        if bookInfo:
            pskillId = bookInfo.get('pskillId', [])
            if len(pskillId) > 0:
                pskillId = pskillId[0]
            else:
                pskillId = 0
            lv = bookInfo.get('lv', 0)
            extraSkill = PD.data.get((pskillId, lv), {}).get('mainEff', '')
    if maxStarLv != -1:
        starSEffect, starPropFix = i._getStarEffetInfo()
        inPropFix = False
        if hasattr(i, 'propFix'):
            for props in i.propFix.itervalues():
                for item in props:
                    if starPropFix and item[0] == starPropFix[0]:
                        inPropFix = True
                    info = PRD.data.get(item[0], {})
                    extraProp += "<font color = \'#E89BFF\'>" + EPFD.data.get(item[0], {}).get('name', '') + ' '
                    if info['type'] == 2:
                        extraProp += '+'
                    elif info['type'] == 1:
                        extraProp += '-'
                    extraProp += str(int(item[1] * 100)) + '%</font>\n'

        ses = getattr(i, 'ses', {})
        mySes = []
        seManualProp = ''
        for sess in ses.itervalues():
            for spId in sess:
                mySes.append(spId)
                spData = ESPD.data.get(spId, {})
                if spData:
                    if spId in ses.get(Item.EQUIP_SE_MANUAL, []):
                        isEffectTxt = ''
                        if BigWorld.component == 'client':
                            p = BigWorld.player()
                            if gameconfigCommon.enableNewLv89():
                                if i.checkHasSesProp(spId, Item.SES_PROPS_MAKER):
                                    if not i.isSesMaker(p.gbId):
                                        isEffectTxt = SYSCD.data.get('specialPropNoEffectTxt', (gameStrings.COMMON_NOT_EFFECT_WITH_BRACKET, ''))[0]
                                    else:
                                        isEffectTxt = SYSCD.data.get('specialPropNoEffectTxt', ('', ''))[1]
                        seManualProp += "<font color = \'#FF7F00\'>%s:%s%s</font>\n" % (spData.get('name', gameStrings.TEXT_ITEMTOOLTIPUTILS_891), spData.get('desc', gameStrings.TEXT_ITEMTOOLTIPUTILS_891), isEffectTxt)
                    else:
                        extraProp += '%s:%s\n' % (spData.get('name', gameStrings.TEXT_ITEMTOOLTIPUTILS_891), spData.get('desc', gameStrings.TEXT_ITEMTOOLTIPUTILS_891))

        extraProp = extraProp + seManualProp
        starSEffect, starPropFix = i._getStarEffetInfo()
        if starPropFix and not inPropFix:
            starPropFixDesc = getStarPropFixDesc(i)
            extraProp += starPropFixDesc
        if starSEffect and starSEffect not in mySes:
            spData = ESPD.data.get(starSEffect, {})
            extraProp += "<font color = \'#808080\'>%s:%s</font>\n" % (spData.get('name', ''), spData.get('desc', ''))
    return (extraSkill, extraProp)


def getStarPropFixDesc(item):
    desc = ''
    starSEffect, starPropFix = item._getStarEffetInfo()
    name = EPFD.data.get(starPropFix[0], {}).get('name', '')
    info = PRD.data.get(starPropFix[0], {})
    desc += "<font color = \'#808080\'>" + name + ' '
    if info['type'] == 2:
        desc += '+'
    elif info['type'] == 1:
        desc += '-'
    desc += str(int(starPropFix[1] * 100)) + '%</font>\n'
    return desc


def getStarSEffectDesc(item):
    desc = ''
    starSEffect = ED.data.get(item.id, {}).get('starSEffect', 0)
    if not item.isManualEquip():
        spData = ESPD.data.get(starSEffect, {})
        return "<font color = \'#808080\'>%s:%s</font>\n" % (spData.get('name', ''), spData.get('desc', ''))
    starSEffect, starPropFix = item._getStarEffetInfo()
    espdData = ESPD.data.get(starPropFix)
    desc += "<font color = \'#808080\'>%s:%s</font>\n" % (espdData.get('name', ''), espdData.get('desc', ''))
    return desc


def getRuneInfo(i, isRuneEquipHasProp):
    allRuneEffects = ()
    runeEquipData = []
    if i.type == Item.BASETYPE_RUNE_EQUIP and isRuneEquipHasProp:
        allRuneEffects = [0] * const.RUNE_EFFECT_TYPE_NUM
        for runeDataVal in i.runeData:
            for effectId, val in enumerate(RD.data.get(runeDataVal.item.id, {})['runeEffects']):
                allRuneEffects[effectId] += val

    elif i.type in Item.BASETYPE_RUNES:
        runeEffects = RD.data.get(i.id, {}).get('runeEffects', []) or NRD.data.get(i.id, {}).get('runeEffects', [])
        if runeEffects:
            allRuneEffects = runeEffects
    if i.type == Item.BASETYPE_RUNE_EQUIP and isRuneEquipHasProp and REQD.data.get(i.id, {}).get('juexingValid', 1):
        tianLunEffects = [0] * const.RUNE_EFFECT_TYPE_NUM
        diLunEffects = [0] * const.RUNE_EFFECT_TYPE_NUM
        runeEquipData = [0] * 6
        runeEquipData[0] = REQD.data.get(i.id, {}).get('tianLunAwakeNeed', '')
        runeEquipData[1] = REQD.data.get(i.id, {}).get('diLunAwakeNeed', '')
        for runeDataVal in i.runeData:
            for effectId, val in enumerate(RD.data[runeDataVal.item.id]['runeEffects']):
                if runeDataVal.runeSlotsType == const.RUNE_TYPE_TIANLUN:
                    tianLunEffects[effectId] += val
                if runeDataVal.runeSlotsType == const.RUNE_TYPE_DILUN:
                    diLunEffects[effectId] += val

        tianLunAwake = True
        diLunAwake = True
        for effectId in range(const.RUNE_EFFECT_TYPE_NUM):
            if runeEquipData[0][effectId] > tianLunEffects[effectId]:
                tianLunAwake = False
                break

        for effectId in range(const.RUNE_EFFECT_TYPE_NUM):
            if runeEquipData[1][effectId] > diLunEffects[effectId]:
                diLunAwake = False
                break

        runeEquipData[4] = tianLunAwake
        runeEquipData[5] = diLunAwake
        tianLunPSkillList = REQD.data.get(i.id, {}).get('tianLunPSkillList', ())
        diLunPSkillList = REQD.data.get(i.id, {}).get('diLunPSkillList', ())
        if tianLunPSkillList:
            pskId = tianLunPSkillList[0]
            runeEquipData[2] = generateDesc(pskId, PSkillInfo(pskId, i.runeEquipLv, {}), i.runeEquipLv)
        if diLunPSkillList:
            pskId = diLunPSkillList[0]
            runeEquipData[3] = generateDesc(pskId, PSkillInfo(pskId, i.runeEquipLv, {}), i.runeEquipLv)
    return (allRuneEffects, runeEquipData)


def getHieroInfo(i, isHieroEquipHasProp):
    info = None
    tianlunWake = []
    tlCrystalLvSum = 0
    dilunWake = []
    dlCrystalLvSum = 0
    if i.type == Item.BASETYPE_HIEROGRAM_EQUIP and isHieroEquipHasProp:
        hieroEquipItem = None
        if BigWorld.component == 'client':
            p = BigWorld.player()
            hieroEquipItem = p.hierogramDict.get('hieroEquip', None)
            hieroCrystals = p.hierogramDict.get('hieroCrystals', None)
            if hieroCrystals:
                for hType, hPart in hieroCrystals:
                    crystalItemID = hieroCrystals[hType, hPart].id
                    addVal = RD.data.get(crystalItemID, {}).get('lv', 0) or NRD.data.get(crystalItemID, {}).get('lv', 0)
                    if hType == const.RUNE_TYPE_TIANLUN:
                        tlCrystalLvSum += addVal
                    elif hType == const.RUNE_TYPE_DILUN:
                        dlCrystalLvSum += addVal

        istlWake = False
        ruleIds = getRulesIDofEquipAwake(i.id, const.RUNE_TYPE_TIANLUN)
        for rid in ruleIds:
            match, sumLimit, _str = getAwakeRuleSumCondition(const.RUNE_TYPE_TIANLUN, rid)
            if match:
                if tlCrystalLvSum >= sumLimit and hieroEquipItem and i == hieroEquipItem:
                    tianlunWake.append(''.join(["<font color=\'#FFFFEA\'>", _str, '</font>']))
                    istlWake = True
                else:
                    tianlunWake.append(''.join(["<font color=\'#808080\'>", _str, '</font>']))

        isdlWake = False
        ruleIds = getRulesIDofEquipAwake(i.id, const.RUNE_TYPE_DILUN)
        for rid in ruleIds:
            match, sumLimit, _str = getAwakeRuleSumCondition(const.RUNE_TYPE_DILUN, rid)
            if match:
                if dlCrystalLvSum >= sumLimit and hieroEquipItem and i == hieroEquipItem:
                    dilunWake.append(''.join(["<font color=\'#FFFFEA\'>", _str, '</font>']))
                    isdlWake = True
                else:
                    dilunWake.append(''.join(["<font color=\'#808080\'>", _str, '</font>']))

        info = {'tianlun': gameStrings.TEXT_ITEMTOOLTIPUTILS_1032,
         'dilun': gameStrings.TEXT_ITEMTOOLTIPUTILS_1033,
         'tianlunWake': tianlunWake,
         'dilunWake': dilunWake}
    return info


def getRulesIDofEquipAwake(equipItemID, hieroType):
    if const.RUNE_TYPE_TIANLUN == hieroType:
        return HED.data.get(equipItemID, {}).get('tianlunAwakeRules', ())
    if const.RUNE_TYPE_DILUN == hieroType:
        return HED.data.get(equipItemID, {}).get('dilunAwakeRules', ())
    return ()


def getAwakeRuleSumCondition(hieroType, ruleID):
    sumLimit = HARD.data.get(ruleID, {}).get('awakeSumCondition', 0)
    typeCondition = HARD.data.get(ruleID, {}).get('hieroAwakeType', -1)
    detail = HARD.data.get(ruleID, {}).get('detail', -1)
    if hieroType == typeCondition:
        return (True, sumLimit, detail)
    else:
        return (False, 0, detail)


def getLvReq(p, i):
    itemData = ID.data.get(i.id, {})
    lvReq = {'satisfy': True,
     'desc': ''}
    if i.type == Item.BASETYPE_LIFE_SKILL:
        fishingLvReq = i.getFishingLvReq()
        if fishingLvReq:
            if fishingLvReq > getattr(p, 'fishingLv', 0):
                lvReq['satisfy'] = False
            else:
                lvReq['satisfy'] = True
            lvReq['desc'] = gameStrings.TEXT_ITEMTOOLTIPUTILS_1066 % (FLD.data.get(fishingLvReq, {}).get('name', ''), fishingLvReq)
        elif i.isExploreEquip():
            lv = SLSED.data.get(i.id, {}).get('exploreLvReq', 0)
            if lv > getattr(p, 'exploreLv', 0):
                lvReq['satisfy'] = False
            else:
                lvReq['satisfy'] = True
            lvReq['desc'] = gameStrings.TEXT_ITEMTOOLTIPUTILS_1066 % (ELD.data.get(lv, {}).get('name', ''), lv)
    else:
        fishingLvReq = i.getFishingLvReq()
        if fishingLvReq:
            if fishingLvReq > getattr(p, 'fishingLv', 0):
                lvReq['satisfy'] = False
            else:
                lvReq['satisfy'] = True
            lvReq['desc'] = gameStrings.TEXT_ITEMTOOLTIPUTILS_1066 % (FLD.data.get(fishingLvReq, {}).get('name', ''), fishingLvReq)
        elif i.isExploreEquip():
            lv = SLSED.data.get(i.id, {}).get('exploreLvReq', 0)
            if lv > getattr(p, 'exploreLv', 0):
                lvReq['satisfy'] = False
            else:
                lvReq['satisfy'] = True
            lvReq['desc'] = gameStrings.TEXT_ITEMTOOLTIPUTILS_1066 % (ELD.data.get(lv, {}).get('name', ''), lv)
            xunbaoExpNeed = SLSED.data.get(i.id, {}).get('xunbaoExpNeed', 0)
            if xunbaoExpNeed:
                if xunbaoExpNeed > getattr(p, 'xunbaoExp', 0):
                    lvReq['desc'] += gameStrings.TEXT_ITEMTOOLTIPUTILS_1093 % xunbaoExpNeed
                else:
                    lvReq['desc'] += gameStrings.TEXT_ITEMTOOLTIPUTILS_1095 % xunbaoExpNeed
            xiangyaoExpNeed = SLSED.data.get(i.id, {}).get('xiangyaoExpNeed', 0)
            if xiangyaoExpNeed:
                if xiangyaoExpNeed > getattr(p, 'xiangyaoExp', 0):
                    lvReq['desc'] += gameStrings.TEXT_ITEMTOOLTIPUTILS_1099 % xiangyaoExpNeed
                else:
                    lvReq['desc'] += gameStrings.TEXT_ITEMTOOLTIPUTILS_1101 % xiangyaoExpNeed
            zhuizongExpNeed = SLSED.data.get(i.id, {}).get('zhuizongExpNeed', 0)
            if zhuizongExpNeed:
                if zhuizongExpNeed > getattr(p, 'zhuizongExp', 0):
                    lvReq['desc'] += gameStrings.TEXT_ITEMTOOLTIPUTILS_1105 % zhuizongExpNeed
                else:
                    lvReq['desc'] += gameStrings.TEXT_ITEMTOOLTIPUTILS_1107 % zhuizongExpNeed
        elif i.lvReq and not itemData.has_key('maxLvReq'):
            ItemLvReq = i.originLvReq
            if ItemLvReq > getattr(p, 'realLv', 0):
                lvReq['satisfy'] = False
            else:
                lvReq['satisfy'] = True
            if ItemLvReq > 1:
                lvReq['desc'] = gameStrings.TEXT_ITEMTOOLTIPUTILS_1116 % ItemLvReq
                if ItemLvReq != i.lvReq:
                    lvReq['realLvReq'] = gameStrings.TEXT_ITEMTOOLTIPUTILS_1118 % i.lvReq
        elif i.lvReq and itemData.has_key('maxLvReq'):
            maxLvReq = itemData.get('maxLvReq', '')
            ItemLvReq = i.lvReq
            realLv = getattr(p, 'lv', 0)
            if ItemLvReq > realLv or maxLvReq < realLv:
                lvReq['satisfy'] = False
            else:
                lvReq['satisfy'] = True
            lvReq['desc'] = gameStrings.TEXT_ITEMTOOLTIPUTILS_1127 % (ItemLvReq, maxLvReq)
        elif itemData.has_key('maxLvReq'):
            maxLvReq = itemData['maxLvReq']
            if maxLvReq < getattr(p, 'lv', 0):
                lvReq['satisfy'] = False
            else:
                lvReq['satisfy'] = True
            lvReq['desc'] = gameStrings.TEXT_ITEMTOOLTIPUTILS_1134 % maxLvReq
        elif i.type == Item.BASETYPE_CONSUMABLE:
            lv = CID.data.get(i.id, {}).get('fishingLvReq', 0)
            if lv != 0:
                if lv > getattr(p, 'fishingLv', 0):
                    lvReq['satisfy'] = False
                else:
                    lvReq['satisfy'] = True
                lvReq['desc'] = gameStrings.TEXT_ITEMTOOLTIPUTILS_1066 % (FLD.data.get(lv, {}).get('name', ''), lv)
    return lvReq


def getFlyUpLvReq(p, i):
    itemData = ID.data.get(i.id, {})
    lvReq = i.lvReq
    if flyUpUtils.enableFlyUp():
        flyUpReduceReqLv = itemData.get('flyUpReduceReqLv', 0)
        if flyUpReduceReqLv:
            flyUpLvReq = lvReq - flyUpReduceReqLv
            desc = gameStrings.ITEM_FLYUP_LV_LOWER_LIMIT % flyUpLvReq
            return desc
    return ''


def getEnhInfo(p, item, enh, location):
    enhLvProp = ''
    enhDuProp = ''
    enhProp = ''
    enhJueXing = ''
    enhJueXingFinalList = []
    enhLvColor = {}
    enhFactor = 0
    enhMaxLv = 0
    refiningFactor = 0
    loseUseFactor = 0
    enhLv = getattr(item, 'enhLv', 0)
    maxEnhlv = getattr(item, 'maxEnhlv', 0)
    enhanceRefining = getattr(item, 'enhanceRefining', {})
    enhJuexingData = getattr(item, 'enhJuexingData', {})
    equipType = getattr(item, 'equipType', 0)
    equipSType = getattr(item, 'equipSType', 0)
    enhanceType = getattr(item, 'enhanceType', 0)
    if gameconfigCommon.enableEquipChangeJuexingStrength():
        enhJuexingAddRatio = getattr(item, 'enhJuexingAddRatio', {})
    else:
        enhJuexingAddRatio = {}
    if BigWorld.component == 'client' and location == const.ITEM_IN_EQUIPMENT:
        p = BigWorld.player()
        part = p.getEquipPart(item)
        mainEquip = p.equipment.get(part)
        subEquip = commcalc.getAlternativeEquip(p, part)
        if mainEquip and mainEquip.uuid == item.uuid:
            enhCalcData = commcalc.getEquipShareEnhProp(p, mainEquip, subEquip)
        elif subEquip and subEquip.uuid == item.uuid:
            enhCalcData = commcalc.getEquipShareEnhProp(p, subEquip, mainEquip)
        else:
            enhCalcData = {}
        if commcalc.enableShareEquipProp(p) and enhCalcData:
            enhLv = enhCalcData['enhLv']
            maxEnhlv = enhCalcData['maxEnhlv']
            enhanceRefining = enhCalcData['enhanceRefining']
            enhJuexingData = enhCalcData['enhJuexingData']
            equipType = enhCalcData['equipType']
            equipSType = enhCalcData['equipSType']
            enhanceType = enhCalcData['enhanceType']
    if enhLv:
        enhMaxLv = item.originMaxEnhlv
        if enhMaxLv:
            enhLvProp = gameStrings.TEXT_ITEMTOOLTIPUTILS_1207 % enhMaxLv
            if enhMaxLv != maxEnhlv:
                enhLvProp = enhLvProp + gameStrings.TEXT_ITEMTOOLTIPUTILS_1209 % maxEnhlv
            if enhanceRefining:
                enhLvColor = getEnhLvColor(maxEnhlv, enhanceRefining)
                refiningFactor = 0
                loseUseFactor = 0
                for key in enhanceRefining:
                    refiningFactor += round(enhanceRefining[key] * 100)
                    if key > maxEnhlv:
                        loseUseFactor += round(enhanceRefining[key] * 100)

                enhDuProp = gameStrings.TEXT_EQUIPCHANGEENHANCEPROXY_227
            star = 0
            if enhLv > 0 and enhanceRefining:
                find = False
                sumRef = sum(enhanceRefining.values())
                prefectionDiv = EERD.data.get(enhLv, {}).get('prefectionDiv', ())
                for k in xrange(0, len(prefectionDiv)):
                    if prefectionDiv[k] >= sumRef:
                        star = k
                        find = True
                        break

                if find == False:
                    star = 10
            enhFactor = star
    if enh:
        specialDesc, _ = getSpecialDesc(enh)
        enhProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1237 % specialDesc
        for enhItem in enh:
            if enhItem[0] not in ATTACK_PROP:
                pType = enhItem[1]
                info = PRD.data.get(enhItem[0], {})
                enhProp += info['name'] + ' '
                if info['type'] == 2:
                    enhProp += "<font color = \'#FFDF99\'>+"
                elif info['type'] == 1:
                    enhProp += "<font color = \'#FFDF99\'>-"
                enhProp += formatProp(enhItem[2], pType, info.get('showType', 0), '</font>', enhItem[5])

        if not loseUseFactor:
            enhProp += '(+%d%%)' % refiningFactor
        else:
            enhProp += "(+%d%%<font color = \'#FF0000\'>-%d%%</font>)" % (refiningFactor, loseUseFactor)
        if enhJuexingData:
            enhJueXingList = [ [key, val] for key, val in enhJuexingData.items() ]
            enhJueXingList.sort(key=lambda k: k[0])
            enhJueXingTitle = SCD.data.get('enhJueXingTitle', (gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1227,
             gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1227_1,
             gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1227_2,
             gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1227_3))
            jueXingPos = 0
            for key in enhJueXingList:
                if key[1]:
                    juexingDataList = key[1]
                    title = enhJueXingTitle[jueXingPos]
                    needGray = False
                    dataForEj = utils.getEquipEnhJuexingPropData(equipType, equipSType, key[0], enhanceType)
                    juexingStep = 0
                    if juexingDataList:
                        juexingStep = utils.getJuexingDataStep(item, key[0], juexingDataList[0], utils.getEquipEnhJuexingPyData())
                    hasNotIn = False
                    for j in juexingDataList:
                        if j[0] not in dataForEj:
                            hasNotIn = True

                    enhMaxLv = maxEnhlv
                    if key[0] > enhLv or hasNotIn or key[0] > enhMaxLv:
                        needGray = True
                    if needGray:
                        enhJueXing += "<font color =\'#808080\'>" + title + ' '
                    else:
                        enhJueXing += title + ' '
                    if enhJuexingAddRatio and key[0] in enhJuexingAddRatio:
                        addRatio = enhJuexingAddRatio[key[0]]
                    else:
                        addRatio = 0
                    for juexingData in juexingDataList:
                        pType = juexingData[1]
                        info = PRD.data.get(juexingData[0], {})
                        jueXingNum = juexingData[2]
                        if juexingData[0] in PROPS_SHOW_SHRINK:
                            jueXingNum = round(jueXingNum / 100.0, 1)
                        enhJueXing += info['name'] + '  +'
                        enhJueXing += formatProp(jueXingNum, pType, info.get('showType', 0))

                    if addRatio > 0:
                        enhJueXing += '</font>'
                        enhJueXing += toHtml(' (+%i%%) ' % int(addRatio * 100), getJuexingStrengthColor(addRatio))
                        enhJueXing += "<font color =\'#808080\'>"
                    if needGray:
                        enhJueXing += gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1266
                    else:
                        enhJueXing += '</font>'
                    enhJueXingFinalList.append([enhJueXing, juexingStep])
                    enhJueXing = ''
                    jueXingPos += 1

    return (enhLvProp,
     enhDuProp,
     enhProp,
     enhJueXingFinalList,
     enhLvColor,
     enhFactor,
     enhMaxLv)


def getJuexingStrengthColor(value):
    valueTmp = int(value * 100)
    colorRanges = SCD.data.get('juexingStrengthColor', {})
    ranges = colorRanges.keys()
    ranges.sort()
    for rangeEnd in ranges:
        if valueTmp <= rangeEnd:
            return colorRanges[rangeEnd]

    return '#b3b3b3'


def getPrefixProp(i, isRand, qualityFactor, isShiftInfo):
    prefixPropList = []
    if i.isYaoPei():
        return prefixPropList
    if not isRand and hasattr(i, 'preprops'):
        if hasattr(i, 'addedStarLv'):
            starLevel = i.addedStarLv
        else:
            starLevel = 0
        starFactor = ESFCD.data.get(starLevel, {}).get('factor', 1.0)
        preprops = [ tuple(list(pp) + [PRD.data.get(pp[0], {}).get('priorityLevel', 0)]) for pp in i.preprops ]
        preprops.sort(key=lambda k: k[3])
        for item in preprops:
            prdData = PRD.data.get(item[0], {})
            pShortName = prdData.get('shortName', '')
            showType = prdData.get('showType', 0)
            if prdData.get('type', 0) == 2:
                pValue = '+'
            elif prdData.get('type', 0) == 1:
                pValue = '-'
            else:
                pValue = ''
            if isShiftInfo and starFactor > 1:
                pValue += formatProp(item[2] * qualityFactor, item[1], showType)
                _value = round((starFactor - 1) * 100, 2)
                pValue += ' (+%s%%)' % str([str(_value), int(_value)][int(_value) == _value])
            else:
                pValue += formatProp(item[2] * starFactor * qualityFactor, item[1], showType)
            prefixPropList.append([item[0], pShortName, pValue])

    return prefixPropList


def getRandProp(i, isRand, rand, randShiftInfo):
    randPropList = []
    if not isRand and rand:
        for num, item in enumerate(rand):
            prdData = PRD.data.get(item[0], {})
            pShortName = prdData.get('shortName', '')
            showType = prdData.get('showType', 0)
            if prdData.get('type', 0) == 2:
                pValue = '+'
            elif prdData.get('type', 0) == 1:
                pValue = '-'
            else:
                pValue = ''
            if num < len(randShiftInfo) and randShiftInfo[num][2] > 0:
                pValue += formatProp(randShiftInfo[num][1], item[1], showType)
                _value = round(randShiftInfo[num][2], 2)
                pValue += ' (+%s%%)' % str([str(_value), int(_value)][int(_value) == _value])
            else:
                pValue += formatProp(item[2], item[1], showType)
            randPropList.append([item[0],
             pShortName,
             pValue,
             item[4]])

    return randPropList


def getFixedProp(i, qualityFactor, isShiftInfo):
    fixedPropList = []
    if i.isYaoPei():
        return fixedPropList
    if hasattr(i, 'extraProps'):
        if hasattr(i, 'starLv'):
            starLevel = i.starLv
        else:
            starLevel = 0
        starFactor = ESFCD.data.get(starLevel, {}).get('factor', 1.0)
        fixed = [ tuple(list(pp) + [PRD.data.get(pp[0], {}).get('priorityLevel', 0)]) for pp in i.extraProps ]
        fixed.sort(key=lambda k: k[3])
        for item in fixed:
            prdData = PRD.data.get(item[0], {})
            pShortName = prdData.get('shortName', '')
            showType = prdData.get('showType', 0)
            if prdData.get('type', 0) == 2:
                pValue = '+'
            elif prdData.get('type', 0) == 1:
                pValue = '-'
            else:
                pValue = ''
            if isShiftInfo and starFactor > 1:
                pValue += formatProp(item[2] * qualityFactor, item[1], showType)
                _value = round((starFactor - 1) * 100, 2)
                pValue += ' (+%s%%)' % str([str(_value), int(_value)][int(_value) == _value])
            else:
                pValue += formatProp(item[2] * starFactor * qualityFactor, item[1], showType)
            fixedPropList.append([item[0], pShortName, pValue])

    return fixedPropList


def getRideWingInfo(p, i):
    isHorse = False
    talents = []
    allTalents = []
    rideWingStage = 0
    maxRideWingStage = 0
    allTalentLevels = []
    horseWindProp = ''
    if i.isWingOrRide():
        talents = getattr(i, 'talents', [])
        allTalents = i.availableTalents()
        allTalentLevels = HTLD.data.get(i.id, {}).values()
        isHorse = True
        specialHorseWingProp = ''
        if hasattr(i, 'rideWingStage') and hasattr(i, 'maxRideWingStage'):
            rideWingStage = i.rideWingStage
            maxRideWingStage = i.maxRideWingStage
            for content in getRideWingItemContent(p, i.id, i.rideWingStage):
                if '+' in content:
                    specialHorseWingProp += content + '\n'
                else:
                    horseWindProp += content + '\n'

        horseWindProp = "<font color = \'#0088CC\'>" + specialHorseWingProp + '</font>' + horseWindProp
    return (isHorse,
     talents,
     allTalents,
     rideWingStage,
     maxRideWingStage,
     allTalentLevels,
     horseWindProp)


def getSomeDesc(i, isPublishedVersion, isInBag):
    desc = ''
    funcDesc = ''
    descTitle = ''
    historyDesc = ''
    itemData = ID.data.get(i.id, {})
    p = None
    if BigWorld.component == 'client':
        p = BigWorld.player()
    if i.type == Item.BASETYPE_CONSUMABLE and getattr(i, 'cstype', 0) == Item.SUBTYPE_2_CLAN_WAR_ANTI_AIR_TOWER:
        towerId = CID.data.get(i.id, {}).get('buildingId', 1)
        tData = CWAD.data.get(towerId, {})
        space = gameStrings.TEXT_ITEMTOOLTIPUTILS_1478 % tData.get('buildSpace', '')
        ttl = gameStrings.TEXT_ITEMTOOLTIPUTILS_1479 % tData.get('buildTTL', '')
        towerDesc = '%s' % tData.get('desc', '')
        desc = '%s\n%s\n\n%s' % (space, ttl, towerDesc)
    else:
        if hasattr(i, 'descTitle'):
            descTitle = i.descTitle
        else:
            descTitle = itemData.get('descTitle', '')
        if hasattr(i, 'funcDesc'):
            funcDesc = i.funcDesc
        else:
            funcDesc = itemData.get('funcDesc', '')
            wishDesc = None
            if p:
                if gameconfigCommon.enableUseItemWish():
                    import gameglobal
                    wishDesc = gameglobal.rds.ui.treasureBoxWish.getTreasureBoxWishDesc(i.id)
            if wishDesc:
                funcDesc += gameStrings.CURRENT_TREASURE_BOX_WISH_DESC % wishDesc
        lvReq = getattr(i, 'lvReq', 0)
        if CID.data.get(i.id, {}).get('vpAdd', 0):
            lv = getattr(p, 'lv', 0)
            if lvReq > lv:
                funcDesc = gameStrings.XIUYING_ITEM_LV_REQ
            else:
                vpDefaultLower = VLD.data.get(lv, {}).get('vpDefaultLower', 0)
                vpTransformRatio = VLD.data.get(lv, {}).get('vpTransformRatio', 0)
                vp = CID.data.get(i.id, {}).get('vpAdd', 0)
                funcDesc = funcDesc % (int(vp * vpTransformRatio) * vpDefaultLower, lv)
        if getattr(i, 'cstype', 0) == Item.SUBTYPE_2_TIHUCHA:
            lv = getattr(p, 'lv', 0)
            if lvReq > lv:
                funcDesc = gameStrings.XIUYING_ITEM_LV_REQ
            else:
                vpDefaultLower = VLD.data.get(lv, {}).get('vpDefaultLower', 0)
                transformRatio = VLD.data.get(lv, {}).get('transformRatio', 0)
                vp = VLD.data.get(lv, {}).get('tihuchaTransVp', 0)
                xiuying = vp * vpDefaultLower
                exp = vp * transformRatio
                funcDesc = funcDesc % (xiuying, lv, exp)
        if getattr(i, 'cstype', 0) == Item.SUBTYPE_2_VT_SEEK_MY_TREE:
            if p.isInDoublePlantTree() and hasattr(p, 'valentineInfo'):
                treePos = p.valentineInfo.treePos
                if treePos and treePos != (0, 0, 0):
                    funcDesc = funcDesc + gameStrings.SEEK_POS_TXT % str((int(treePos[0]), int(treePos[2]), int(treePos[1])))
        fireWorkItems = FFLCD.data.get('fireWorkItems', ())
        if i.id in fireWorkItems:
            targetName = getattr(i, 'targetName', '')
            if targetName:
                funcDesc = funcDesc % (targetName, targetName)
            else:
                funcDesc = funcDesc % (gameStrings.FIGHT_FOR_LOVE_CREATER_TXT, gameStrings.FIGHT_FOR_LOVE_CREATER_TXT)
        if hasattr(i, 'historyDesc'):
            historyDesc = i.historyDesc
        else:
            historyDesc = itemData.get('historyDesc', '')
        if hasattr(i, 'signerOne') and hasattr(i, 'signerTwo'):
            historyDesc = SCD.data.get('SIGNER_DESC', gameStrings.TEXT_ITEMTOOLTIPUTILS_1547) % (i.signerOne, i.signerTwo)
        marriageBegineTimestamp = getattr(p, 'marriageBegineTimestamp', 0)
        if getattr(i, 'cstype', 0) == Item.SUBTYPE_2_MARRIAGE_SUBSCRIBE:
            if marriageBegineTimestamp:
                historyDesc = historyDesc % utils.formatDatetime(marriageBegineTimestamp)
            else:
                historyDesc = ''
        if hasattr(i, 'wifeRoleName') and hasattr(i, 'husbandRoleName'):
            historyDesc = historyDesc % (i.husbandRoleName, i.wifeRoleName)
        if hasattr(i, 'desc'):
            desc = i.desc
        else:
            desc = itemData.get('desc', '')
    if not isPublishedVersion:
        if desc != '':
            desc += gameStrings.TEXT_ITEMTOOLTIPUTILS_1566 + str(i.id)
        else:
            desc += gameStrings.TEXT_ITEMTOOLTIPUTILS_1568 + str(i.id)
        if i.type == Item.BASETYPE_EQUIP:
            eData = ED.data.get(i.id)
            if eData:
                desc += gameStrings.TEXT_ITEMTOOLTIPUTILS_1572 + str(eData.get('modelId'))
        if itemData.get('testItem', 0):
            testTime = itemData.get('testTime', gameStrings.TEXT_GAME_1747)
            if testTime.isdigit():
                beginTime = datetime.datetime(1900, 1, 1, 0, 0, 0)
                expireTime = beginTime + datetime.timedelta(int(testTime) - 2)
                expireTimeStr = '%d/%d/%d' % (expireTime.year, expireTime.month, expireTime.day)
            else:
                expireTimeStr = testTime
            desc += gameStrings.TEXT_ITEMTOOLTIPUTILS_1581 % expireTimeStr
    if i.type == Item.BASETYPE_EQUIP_GEM and getattr(i, 'unvalidStr', ''):
        if funcDesc[-1] == '\n':
            funcDesc += i.unvalidStr
        else:
            funcDesc += '\n' + i.unvalidStr
    if BigWorld.component == 'client':
        import gameglobal
        if gameglobal.rds.ui.npcSendGift.lockDesc.get(i.id, ''):
            from guis import uiUtils
            funcDesc += '\n' + uiUtils.toHtml(gameglobal.rds.ui.npcSendGift.lockDesc.get(i.id, ''), '#d34024')
    return (desc,
     funcDesc,
     descTitle,
     historyDesc)


def getEquipTypeStr(equipType, equipSType, equipTypeMap, fashionTypeMap):
    strType = ''
    if equipType == 4:
        strType = fashionTypeMap.get(equipSType, gameStrings.TEXT_ITEMTOOLTIPUTILS_891)
    elif equipType in (1, 2, 3):
        strType = equipTypeMap.get(equipType, {}).get(equipSType, gameStrings.TEXT_ITEMTOOLTIPUTILS_891)
    return strType


def getEquipSType(itemId):
    ed = ED.data.get(itemId, {})
    etp = ed.get('equipType')
    equipSType = None
    if etp in (Item.EQUIP_BASETYPE_WEAPON, Item.EQUIP_BASETYPE_FASHION_WEAPON, Item.EQUIP_BASETYPE_WEAPON_RUBBING):
        equipSType = ed.get('weaponSType')
    elif etp in (Item.EQUIP_BASETYPE_ARMOR, Item.EQUIP_BASETYPE_ARMOR_RUBBING):
        equipSType = ed.get('armorSType')
    elif etp == Item.EQUIP_BASETYPE_JEWELRY:
        equipSType = ed.get('jewelSType')
    elif etp == Item.EQUIP_BASETYPE_FASHION:
        equipSType = ed.get('fashionSType')
    return equipSType


def getEquPart(i, equipTypeMap, fashionTypeMap):
    equPart = ''
    if Item.isDotaBattleFieldItem(i.id):
        return equPart
    if hasattr(i, 'equipType') and hasattr(i, 'equipSType'):
        equPart = getEquipTypeStr(i.equipType, i.equipSType, equipTypeMap, fashionTypeMap)
    elif i.type == Item.BASETYPE_RUNE_EQUIP:
        equPart = gameStrings.TEXT_ITEMTOOLTIPUTILS_1624
    elif i.type == Item.BASETYPE_HIEROGRAM_EQUIP:
        equPart = gameStrings.TEXT_ITEMTOOLTIPUTILS_1624
    elif i.type in Item.BASETYPE_RUNES:
        runeType = RD.data.get(i.id, {}).get('runeType', 0) or NRD.data.get(i.id, {}).get('runeType', 0)
        if runeType == const.RUNE_TYPE_TIANLUN:
            equPart = gameStrings.TEXT_CONST_7146
        elif runeType == const.RUNE_TYPE_DILUN:
            equPart = gameStrings.TEXT_CONST_7147
        elif runeType == const.RUNE_TYPE_BENYUAN:
            equPart = gameStrings.TEXT_CONST_7148
        else:
            equPart = ''
    elif i.isLifeEquip():
        subType = LSED.data.get(i.id, {}).get('subType', 1)
        equPart = gameStrings.TEXT_ITEMTOOLTIPUTILS_1639 % LSSD.data.get(subType, {}).get('name', '')
    elif i.type == Item.BASETYPE_UNIDENTIFIED_EQUIP:
        targetEquipId = MERRD.data.get(i.id, {}).get('targetEquipId')
        ed = ED.data.get(targetEquipId, {})
        equipType = ed.get('equipType')
        equipSType = getEquipSType(targetEquipId)
        equPart = getEquipTypeStr(equipType, equipSType, equipTypeMap, fashionTypeMap)
    else:
        equPart = ''
    return equPart


def getBasicProp(i, basic, yaopeiBonus = '', shiftInfo = []):
    basicProp = ''
    basicPropList = []
    if i.isWingOrRide():
        return (basicProp, basicPropList)
    if basic:
        if not i.isYaoPei():
            specialDesc, basicPropList = getSpecialDesc(basic, shiftInfo)
            if specialDesc != '':
                basicProp = specialDesc + '<br>'
        isDotaItem = Item.isDotaBattleFieldItem(i.id)
        for num, item in enumerate(basic):
            if isDotaItem and item[0] == const.PROP_CURE_ID:
                continue
            prdData = PRD.data.get(item[0], {})
            pName = prdData.get('name', '')
            pShortName = prdData.get('shortName', '')
            showType = prdData.get('showType', 0)
            if num < len(shiftInfo) and shiftInfo[num][2] > 0:
                pValue = formatProp(shiftInfo[num][1], item[1], showType)
                _value = round(shiftInfo[num][2], 2)
                pValue += ' (+%s%%)' % str([str(_value), int(_value)][int(_value) == _value])
            else:
                pValue = formatProp(item[2], item[1], showType)
            if yaopeiBonus != '':
                pValue += yaopeiBonus
            basicProp += '%s  %s<br>' % (pName, pValue)
            basicPropList.append([item[0],
             pShortName,
             '+%s' % pValue,
             item[3]])

    elif i.type == Item.BASETYPE_LIFE_SKILL:
        if i.whereEquipFishing() != -1:
            if i.getMaxRange():
                basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1689 % str(i.getMaxRange())
            if i.getControllability():
                basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1691 % str(i.getControllability())
                basicProp += showFishingLabourAndMental(i)
            if i.getHookAbility():
                basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1694 % str(i.getHookAbility())
            if i.getSensitivity():
                basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1696 % str(i.getSensitivity())
        elif i.whereEquipExplore() != -1:
            fData = SLSED.data.get(i.id, {})
            if fData.get('sensePower', 0):
                basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1700 % fData.get('sensePower', 0)
            if fData.get('pointer', 0):
                basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1702 % fData.get('pointer', 0)
            if fData.get('senseDist', 0):
                basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1704 % fData.get('senseDist', 0)
    elif i.type == Item.BASETYPE_CONSUMABLE:
        if i.whereEquipFishing() != -1:
            cData = CID.data.get(i.id)
            if cData.get('rodEnhance', 0):
                basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1689 % str(cData.get('rodEnhance', 0))
            if cData.get('attraction', 0):
                basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1712 % str(cData.get('attraction', 0))
            if cData.get('hookEnhance', 0):
                basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1694 % str(cData.get('hookEnhance', 0))
            if cData.get('buoyEnhance', 0):
                basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1696 % str(cData.get('buoyEnhance', 0))
        elif i.whereEquipExplore() != -1:
            fData = SLSED.data.get(i.id, {})
            scrollType = fData.get('expAdd', [0, 0])[0]
            if scrollType:
                basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1721
                if scrollType == 1:
                    basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1723
                elif scrollType == 2:
                    basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1725
                else:
                    basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1727
            if fData.get('powerNeed', 0):
                basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1729 % fData.get('powerNeed', 0)
            if fData.get('displayDist', 0):
                dist = ''
                if 5 <= fData.get('displayDist', 0) < 6.25:
                    dist = gameStrings.TEXT_ITEMTOOLTIPUTILS_1733
                elif 6.25 <= fData.get('displayDist', 0) < 7.5:
                    dist = gameStrings.TEXT_ITEMTOOLTIPUTILS_1735
                elif 7.5 <= fData.get('displayDist', 0) < 8.75:
                    dist = gameStrings.TEXT_ITEMTOOLTIPUTILS_1737
                elif 8.75 <= fData.get('displayDist', 0) <= 10:
                    dist = gameStrings.TEXT_ITEMTOOLTIPUTILS_1739
                basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1740 % dist
                basicProp += showExploreLabourAndMental(i)
    elif i.isLifeEquip():
        cfgdata = LSED.data.get(i.id, {})
        props = cfgdata.get('gProps', [])
        if len(props):
            basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1747
            for pId, type, pVal in props:
                propName = PRD.data.get(pId, {}).get('name', '')
                if propName:
                    basicProp += '%s %d<br>' % (propName, pVal)

            basicProp += '</font>'
        gProps = cfgdata.get('props', [])
        if len(gProps):
            basicProp += gameStrings.TEXT_ITEMTOOLTIPUTILS_1756
            for pId, pVal in gProps:
                propName = PPD.data.get(pId, {}).get('chName', '')
                if propName:
                    basicProp += '%s %d<br>' % (propName, pVal)

            basicProp += '</font>'
    elif i.type == Item.BASETYPE_EQUIP_GEM:
        prop = utils.getEquipGemData(i.id).get('gemProps', [])
        if len(prop) > 0:
            basicProp += getGemProp(prop)
    if not i.isLifeEquip():
        if basicProp != '':
            if '<br>' not in basicProp:
                basicProp = "<font size=\'15\'>" + basicProp + '</font>'
            else:
                basicProp = "<font size=\'15\'>" + basicProp
                firstEnterPos = basicProp.find('<br>')
                basicProp = basicProp.replace(basicProp[0:firstEnterPos], basicProp[0:firstEnterPos] + '</font>')
    return (basicProp, basicPropList)


def getFamePrice(i):
    famePrice = []
    itemData = ID.data.get(i.id, {})
    fameIds = itemData.get('famePrice', {})
    for shopIds, fameData in fameIds.items():
        shopName = ''
        if isinstance(shopIds, int):
            shopIds = (shopIds,)
        for index, shopId in enumerate(shopIds):
            if index != 0:
                shopName += gameStrings.TEXT_CHATPROXY_403
            shopName += CSD.data.get(shopId, {}).get('shopName', '')

        shopName += gameStrings.TEXT_ITEMTOOLTIPUTILS_1793
        fameName = FD.data.get(fameData[0], {}).get('name', gameStrings.TEXT_CHALLENGEPROXY_199_1)
        if shopName:
            famePrice.append([shopName, fameName, fameData[1]])

    return famePrice


def getQualityColor(i, isInBag):
    itemData = ID.data.get(i.id, {})
    if hasattr(i, 'quality'):
        quality = i.quality
    else:
        quality = itemData.get('quality', 1)
    if BigWorld.component == 'client':
        if BigWorld.player().isInBfDota() and itemData.has_key('dotaItemQuality'):
            quality = itemData.get('dotaItemQuality', 1)
    qualityColor = FCD.data.get(('item', quality), {}).get('qualitycolor', 'gray')
    return qualityColor


def getQualityColorById(itemId):
    itemData = ID.data.get(itemId, {})
    quality = itemData.get('quality', 1)
    if BigWorld.component == 'client':
        if BigWorld.player().isInBfDota() and itemData.has_key('dotaItemQuality'):
            quality = itemData.get('dotaItemQuality', 1)
    qualityColor = FCD.data.get(('item', quality), {}).get('qualitycolor', 'gray')
    return qualityColor


def checkIsRand(isInBag, isInChat, isInBooth, bRelative):
    if isInBag or isInChat or isInBooth or bRelative:
        return False
    return True


def getRandHint(i, rand, isRand):
    itemData = ID.data.get(i.id, {})
    hasRandPropId = ED.data.get(i.id, {}).get('randPropId', 0)
    hasPreGroupList = ED.data.get(i.id, {}).get('preGroupList', [])
    if (rand or getattr(i, 'preprops', None) or hasRandPropId) and isRand:
        randHint = gameStrings.TEXT_ITEMTOOLTIPUTILS_1832
        if itemData.get('quality', 0) == 0:
            randHint += gameStrings.TEXT_ITEMTOOLTIPUTILS_1834
    elif hasPreGroupList and isRand:
        randHint = gameStrings.TEXT_ITEMTOOLTIPUTILS_1832
    else:
        randHint = ''
    return randHint


def getDura(i):
    dura = ''
    itemData = ID.data.get(i.id, {})
    if hasattr(i, 'cdura') and hasattr(i, 'initMaxDura') and i._checkEquipDuraValid() and not i.isShihun():
        if i.isWingOrRide():
            pass
        elif int(math.ceil(i.cdura)) <= 0:
            dura = gameStrings.TEXT_ITEMTOOLTIPUTILS_1850 % (int(math.ceil(i.cdura)), int(i.initMaxDura))
        else:
            dura = gameStrings.TEXT_ITEMTOOLTIPUTILS_1852 % (int(math.ceil(i.cdura)), int(i.initMaxDura))
    elif i.isShihun():
        dura = gameStrings.TEXT_ITEMTOOLTIPUTILS_1855
    elif i.isRuneEquip() or i.isHieroEquip():
        dura = ''
    elif getattr(i, 'timeLimit', 0):
        dura = gameStrings.TEXT_ITEMTOOLTIPUTILS_1859 % (i.timeLimit, CID.data.get(i.id, {}).get('timeLimit', 0))
    elif itemData.get('mallItem', 0) == 1:
        dura = ''
    hasHoldMax, maxAmount = i.hasHoldMax()
    if hasHoldMax:
        if dura:
            dura += '\n'
        dura += gameStrings.TEXT_ITEMTOOLTIPUTILS_1867 % maxAmount
    return dura


def getStarExp(i, isRuneEquipHasProp):
    starExp = 0
    maxStarExp = 0
    if i.isYaoPei():
        hasExp, needExp = i.getYaoPaiLvUpExp()
        starExp = hasExp
        maxStarExp = needExp
    else:
        if hasattr(i, 'starExp'):
            starExp = i.starExp
            starExpData = ESLD.data.get(i.starLv, {})
            lvUpFormula = starExpData.get('upExp')
            maxStarExp = 0
            if lvUpFormula:
                maxStarExp = int(i.evalValue(lvUpFormula[0], lvUpFormula[1:]))
        elif i.type == Item.BASETYPE_RUNE_EQUIP and isRuneEquipHasProp:
            if const.RUNE_EQUIP_MAX_LV <= i.runeEquipLv:
                eData = REED.data.get((const.RUNE_EQUIP_MAX_LV - 1, i.runeEquipOrder))
                starExp = eData.get('upExp', 0)
                maxStarExp = int(eData.get('upExp', 0))
            else:
                eData = REED.data.get((i.runeEquipLv, i.runeEquipOrder))
                starExp = i.runeEquipExp
                maxStarExp = int(eData.get('upExp', 0))
        else:
            starExp = 0
            maxStarExp = 0
        if i.isWingOrRide():
            starExp = i.starExp
            maxStarExp = int(i.getRideWingMaxUpgradeExp())
    return (starExp, maxStarExp)


def getExcitmentReq(p, i):
    eReq = ''
    acExcitement = i.getAcExcitement()
    if acExcitement and hasattr(p, 'checkExcitementFeature') and not p.checkExcitementFeature(acExcitement):
        eReq = gameStrings.EXCITEMENT_FORBIDDEN_TIPS
    return eReq


def getRank(i, isRuneEquipHasProp, isHieroEquipHasProp):
    rank = ''
    if i.isYaoPei():
        lv = i.getYaoPeiLv()
        rank = 'Lv.%d' % lv
    elif i.isGuanYin():
        rank = ''
    elif i.type == Item.BASETYPE_RUNE_EQUIP and isRuneEquipHasProp:
        rank = gameStrings.TEXT_ITEMTOOLTIPUTILS_1922 % i.runeEquipOrder
    elif i.type == Item.BASETYPE_HIEROGRAM_EQUIP and isHieroEquipHasProp:
        rank = gameStrings.TEXT_ITEMTOOLTIPUTILS_1922 % i.hieroEquipOrder
    else:
        order = i.order
        if order:
            rank = gameStrings.TEXT_ITEMTOOLTIPUTILS_1928 % order
            if i.addedOrder != order:
                rank = rank + gameStrings.TEXT_ITEMTOOLTIPUTILS_1930 % str(i.addedOrder)
    return rank


def getSchReq(p, i):
    strSch = ''
    itemData = ID.data.get(i.id, {})
    if itemData.has_key('schReq'):
        strSch = ''
        for sc in itemData['schReq']:
            if sc == const.SCHOOL_TIANZHAO:
                if not gameconfigCommon.enableNewSchoolTianZhao():
                    continue
            strSch += SD.data.get(sc, {}).get('name', gameStrings.TEXT_GAME_1747) + ' '

        if getattr(p, 'realSchool', const.SCHOOL_DEFAULT) not in itemData['schReq']:
            strSch = gameStrings.TEXT_ITEMTOOLTIPUTILS_1946 % strSch
        else:
            strSch = gameStrings.TEXT_ITEMTOOLTIPUTILS_1948 % strSch
    else:
        strSch = ''
    return strSch


def getWrap(i, isInBag, location = 0):
    wrap = ''
    itemData = ID.data.get(i.id, {})
    mwrap = itemData.get('mwrap', 1)
    count = i.cwrap
    if mwrap > 1 and isInBag:
        wrap = gameStrings.TEXT_ITEMTOOLTIPUTILS_1960 % (count, mwrap)
    elif mwrap > 1 and (location == const.ITEM_IN_COMPOSITESHOP or location == const.ITEM_IN_SHOP):
        wrap = gameStrings.TEXT_ITEMTOOLTIPUTILS_1962 % mwrap
    else:
        wrap = ''
    return wrap


def getCtrlDesc(i, isInBag, location = None):
    ctrlDesc = ''
    itemData = ID.data.get(i.id, {})
    if itemData.get('ctrl', 0) and (isInBag or location in (const.ITEM_IN_FAME_SHOP, const.ITEM_IN_COMPOSITESHOP, const.ITEM_IN_ACHEVEMENT)):
        ctrlDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_1971
    return ctrlDesc


def getLifeSkillEquipDesc(i):
    lifeSkillEquipDesc = ''
    if i.isLifeEquip():
        lifeSkillEquipData = LSED.data.get(i.id, {})
        for field in LIFE_SKILL_EQUIP_LIST:
            lifeSkillEquipDesc += _calcLifeSkillEquip(lifeSkillEquipData, field)

        if lifeSkillEquipDesc != '':
            lifeSkillEquipDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_1981 + lifeSkillEquipDesc
    return lifeSkillEquipDesc


def getInitiativeSkillDesc(i):
    initiativeSkillDesc = ''
    if Item.isDotaBattleFieldItem(i.id) and BigWorld.component == 'client':
        p = BigWorld.player()
        skillId = ED.data.get(i.id, {}).get('skillId', 0)
        skillLv = ED.data.get(i.id, {}).get('skillLv', 0)
        from data import skill_client_data as SKCD
        if skillId + skillLv:
            skillName = SKCD.data.get((skillId, skillLv), {}).get('sname', '')
            initiativeSkillDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_1993 % skillName
            skillTipsInfo = p.getSkillTipsInfo(skillId, skillLv)
            mainEff = skillTipsInfo.getSkillData('shortMainEff', '')
            initiativeSkillDesc += mainEff
    return initiativeSkillDesc


def getPskillDesc(i):
    pskillDesc = ''
    if Item.isDotaBattleFieldItem(i.id) and BigWorld.component == 'client':
        extraDotaPskillIds = ID.data.get(i.id, {}).get('extraDotaPskillIds', [])
        if extraDotaPskillIds:
            for skillId, lv in extraDotaPskillIds:
                skillName = PTD.data.get(skillId, {}).get('sname', '')
                pskillDesc += gameStrings.TEXT_ITEMTOOLTIPUTILS_2007 % skillName
                mainEff = PSD.data.get((skillId, lv), {}).get('mainEff', '') + '\n'
                pskillDesc += mainEff

    return pskillDesc


def getDotaItemSellPriceDesc(i):
    sellPriceDesc = ''
    if Item.isDotaBattleFieldItem(i.id) and BigWorld.component == 'client':
        import gameglobal
        cash = gameglobal.rds.ui.bfDotaShop.itemTree.get(i.id, {}).get('cash', 0)
        sellPrice = int(cash / DCD.data.get('BATTLE_FIELD_DOTA_ITEM_SELL_RADIO'))
        sellPriceDesc = SCD.data.get('shop_sell_price_desc', '%d') % sellPrice
    return sellPriceDesc


def _calcLifeSkillEquip(data, field):
    desc = ''
    if data.has_key(field):
        lifePropData = LIFE_SKILL_EQUIP.get(field)
        desc += lifePropData[0]
        prob = data.get(field)
        if field == 'identifyQuality':
            if prob >= 0:
                desc += gameStrings.TEXT_ITEMTOOLTIPUTILS_2029 % float(abs(prob) * 1.0 / lifePropData[1])
            else:
                desc += gameStrings.TEXT_ITEMTOOLTIPUTILS_2031 % float(abs(prob) * 1.0 / lifePropData[1])
        elif field == 'lvUp':
            sbuType = data.get('subType', 0)
            lifeskillId = LSSD.data.get(sbuType, {}).get('lifeSkillId', 0)
            skillName = LIFE_SKILL.get(lifeskillId, 'not fined')
            desc = lifePropData[0] % (skillName, prob)
        elif prob >= 0:
            desc += '+%d%%' % (abs(prob) / lifePropData[1])
        else:
            desc += '-%d%%' % (abs(prob) / lifePropData[1])
        return desc + '\n'
    else:
        return desc


def getFashionItemHasTrans(i):
    if getattr(i, 'fashionTransProp', None):
        if len(i.fashionTransProp) == 3:
            if i.fashionTransProp[2] > utils.getNow():
                return True
    return False


def getMakeTypeDesc(item):
    if item.type == Item.BASETYPE_UNIDENTIFIED_EQUIP or item.isManualEquip():
        if item.makeType == Item.MAKE_TYPE_1:
            color = FCD.data.get(('item', 1), {}).get('color', '#ffffff')
            return gameStrings.TEXT_ITEMTOOLTIPUTILS_2058 % color
        if item.makeType == Item.MAKE_TYPE_2:
            color = FCD.data.get(('item', 2), {}).get('color', '#ffffff')
            return gameStrings.TEXT_ITEMTOOLTIPUTILS_2061 % color
        if item.makeType == Item.MAKE_TYPE_3:
            color = FCD.data.get(('item', 3), {}).get('color', '#ffffff')
            return gameStrings.TEXT_ITEMTOOLTIPUTILS_2064 % color
    else:
        return ''


def getCornerMark(item):
    if not utils.enableCalcRarityMiracle() or not hasattr(item, 'rarityMiracle'):
        return ''
    if item.rarityMiracle == Item.EQUIP_IS_RARITY:
        return 'rarity'
    if item.rarityMiracle == Item.EQUIP_IS_MIRACLE:
        return 'miracle'
    return ''


def checkUsePropList(item):
    if not hasattr(item, 'equipType'):
        return False
    if item.equipType in (Item.EQUIP_BASETYPE_WEAPON, Item.EQUIP_BASETYPE_JEWELRY):
        return True
    if item.equipType == Item.EQUIP_BASETYPE_ARMOR:
        if not hasattr(item, 'equipSType'):
            return False
        if Item.EQUIP_FASHION_SUBTYPE_HEAD <= item.equipSType <= Item.EQUIP_FASHION_SUBTYPE_SHOE:
            return True
        if item.equipSType == Item.EQUIP_ARMOR_SUBTYPE_GUANYIN:
            return True
    return False


def formatRet(p, i, bRelative = False, isInBag = True, isInChat = False, isInBooth = False, page = BOOTH_SLOTS_SELL, isCompositeShop = False, extraData = '', inRepair = False, isPublishedVersion = False, inHeaderAssignMode = False, assignTarget = None, location = 0, fullAppAPIDesc = False):
    itemData = ID.data.get(i.id, {})
    equipTypeMap, gemEquipTypeMap, fashionTypeMap = initData()
    isRuneEquipHasProp = True
    if i.isRuneEquip():
        if not hasattr(i, 'runeData') or not hasattr(i, 'runeEquipLv') or not hasattr(i, 'runeEquipOrder'):
            isRuneEquipHasProp = False
    isHieroEquipHasProp = True
    if i.isHieroEquip():
        if not hasattr(i, 'hieroEquipOrder'):
            isHieroEquipHasProp = False
    if getFashionItemHasTrans(i):
        ed = ED.data.get(i.fashionTransProp[0], {})
        i.props = ed.get('props', [])
        i.extraProps = ed.get('extraProps', [])
    basic, rand, enh, basicShift, randShift = calAttrVal(i, location)
    quality = getattr(i, 'quality', 1)
    if not quality:
        quality = 1
    qualityFactor = EQFD.data.get(quality, {}).get('factor', 1.0)
    if not hasattr(i, 'cstype'):
        if CID.data.get(i.id, {}).get('sType', None):
            i.cstype = CID.data.get(i.id, {}).get('sType', None)
    if BigWorld.component == 'client' and hasattr(i, 'refineManual'):
        p = BigWorld.player()
        refiningSrcName = i.refineManual.get(i.REFINE_MANUAL_ROLENAME, '')
        if refiningSrcName:
            refiningSrcName += gameStrings.TEXT_HELPPROXY_512
    else:
        refiningSrcName = ''
    itemName = getItemName(i, isInBag, bRelative)
    bindType = _addBindInfo(i, isInBag, bRelative)
    dyeType = _addDyeType(i)
    dyeTTLExpireTime = 0
    if hasattr(i, 'dyeTTLExpireTime') and i.dyeTTLExpireTime:
        dyeTTLExpireTime = i.dyeTTLExpireTime
    rongGuangExpireTime = 0
    if hasattr(i, 'rongGuangExpireTime') and i.rongGuangExpireTime:
        rongGuangExpireTime = i.rongGuangExpireTime
    canRongGuang = i.isCanRongGuang()
    huanfuExpireTime = 0
    if hasattr(i, 'currentSkin'):
        huanfuExpireTime = i.dyeSkins.get(i.currentSkin, 0)
    sPriceType, priceLabel, boothLabel, price, boothPrice = getPriceInfo(p, i, bRelative, isInBag, isInBooth, inRepair, isCompositeShop, extraData, page)
    extraLimit = ''
    conditionsList = itemData.get('conditionsList', [])
    if len(conditionsList) >= 0:
        extraLimit = getExtraLimit(p, i)
    if i.type == Item.BASETYPE_EQUIP_GEM:
        extraLimit = getGemLimit(i, gemEquipTypeMap)
    gatypeLabel = ''
    if hasattr(i, 'ownerGuildName'):
        gatypeLabel = gameStrings.TEXT_ITEMTOOLTIPUTILS_2175 % i.ownerGuildName
    if hasattr(i, 'ownerName') and i.ownerName != '':
        gatypeLabel = gameStrings.TEXT_ITEMTOOLTIPUTILS_2178 % i.ownerName
    iconPath = 'item/icon64/' + str(itemData.get('icon', 'notFound')) + '.dds'
    runeDesc = getRuneDesc(i)
    runePropDesc = getRunePropDesc(i)
    signDesc = getSignDesc(i)
    desc, funcDesc, descTitle, historyDesc = getSomeDesc(i, isPublishedVersion, isInBag)
    useSubEquipEnhLv = False
    enhLv = getattr(i, 'enhLv', 0)
    if BigWorld.component == 'client' and location == const.ITEM_IN_EQUIPMENT:
        p = BigWorld.player()
        part = p.getEquipPart(i)
        mainEquip = p.equipment.get(part)
        subEquip = commcalc.getAlternativeEquip(p, part)
        if mainEquip and mainEquip.uuid == i.uuid:
            enhCalcData = commcalc.getEquipShareEnhProp(p, mainEquip, subEquip)
        elif subEquip and subEquip.uuid == i.uuid:
            enhCalcData = commcalc.getEquipShareEnhProp(p, subEquip, mainEquip)
        else:
            enhCalcData = {}
        if commcalc.enableShareEquipProp(p) and enhCalcData:
            if enhLv < enhCalcData['enhLv']:
                useSubEquipEnhLv = True
                enhLv = enhCalcData['enhLv']
    if enhLv != 0:
        enhLv = '+%d' % enhLv
    else:
        enhLv = ''
    qualityColor = getQualityColor(i, isInBag)
    if hasattr(i, 'score'):
        score = '%d' % i.score
    else:
        score = ''
    initScore = ''
    if hasattr(i, 'initScore'):
        initScore = '%d' % i.initScore
    yaoPeiScore = ''
    yaopeiDetailScore = ''
    if hasattr(i, 'initYaoPeiScore'):
        yaoPeiScore = '%d' % i.yaoPeiScore
        yaopeiDetailScore = '%d' % i.initYaoPeiScore
        if hasattr(i, 'yaoPeiScore'):
            yaopeiDetailScore += "<font color= \'#FF7F00\'>" + ' +%d' % (i.yaoPeiScore - i.initYaoPeiScore) + '</font>'
    useTime = getMallUseTimeData(i, isInBag, isInChat, bRelative)
    dura = getDura(i)
    wrap = getWrap(i, isInBag, location)
    strSch = getSchReq(p, i)
    equPart = getEquPart(i, equipTypeMap, fashionTypeMap)
    exciteReq = getExcitmentReq(p, i)
    maxStarLv = getattr(i, 'maxStarLv', -1)
    starLv = getattr(i, 'starLv', 0)
    itemLv = getattr(i, 'itemLv', 1)
    sexReq = getSexReq(p, i)
    starExp, maxStarExp = getStarExp(i, isRuneEquipHasProp)
    rank = getRank(i, isRuneEquipHasProp, isHieroEquipHasProp)
    aptitude = ''
    tianlunSlotNum, dilunSlotNum = getTianAndDiLunSlotNum(i, isRuneEquipHasProp)
    isRand = checkIsRand(isInBag, isInChat, isInBooth, bRelative)
    randHint = getRandHint(i, rand, isRand)
    prefixPropList = getPrefixProp(i, isRand, qualityFactor, False)
    shiftPrefixPropList = getPrefixProp(i, isRand, qualityFactor, True)
    randPropList = getRandProp(i, isRand, rand, [])
    shiftRandPropList = getRandProp(i, isRand, rand, randShift)
    fixedPropList = getFixedProp(i, qualityFactor, False)
    shiftFixedPropList = getFixedProp(i, qualityFactor, True)
    tmpBasic = copy.deepcopy(basic)
    basicProp, basicPropList = getBasicProp(i, basic)
    shiftBasicProp, shiftBasicPropList = getBasicProp(i, tmpBasic, shiftInfo=basicShift)
    if getattr(i, 'fashionTransProp', None):
        if len(i.fashionTransProp) == 3:
            if i.fashionTransProp[2] > utils.getNow() or i.fashionTransProp[2] == -1:
                fromName = ID.data.get(i.fashionTransProp[0], {}).get('name', '')
                headStr = gameStrings.TEXT_ITEMTOOLTIPUTILS_2286 % fromName
                basicProp = headStr + basicProp
                shiftBasicProp = headStr + shiftBasicProp
                useTime['fashionPropExpireTime'] = i.fashionTransProp[2]
    if i.isYaoPei():
        basicPropList, shiftBasicPropList = getYaopeiBasicPropList(i)
        randPropList, shiftRandPropList = getYaopeiRandPropList(i, rand)
        yaopeiExtraPropList, yaopeiShiftExtraPropList = getYaopeiExtraPropList(i)
    else:
        yaopeiExtraPropList = []
        yaopeiShiftExtraPropList = []
    propList = []
    shiftPropList = []
    if checkUsePropList(i):
        addBasicPropList(i, propList, shiftPropList, basicPropList, shiftBasicPropList)
        addPrefixPropList(i, propList, shiftPropList, prefixPropList, shiftPrefixPropList)
        addFixedPropList(i, propList, shiftPropList, fixedPropList, shiftFixedPropList)
        addRandPropList(i, propList, shiftPropList, randPropList, shiftRandPropList)
        propList.extend(yaopeiExtraPropList)
        shiftPropList.extend(yaopeiShiftExtraPropList)
    isHorse, talents, allTalents, rideWingStage, maxRideWingStage, allTalentLevels, horseWindProp = getRideWingInfo(p, i)
    enhLvProp, enhDuProp, enhProp, enhJueXing, enhLvColor, enhFactor, enhMaxLv = getEnhInfo(p, i, enh, location)
    extraSkill, extraProp = getExtraProp(i, maxStarLv)
    equipSkillDesc = getEquipSkillDesc(p, i, fullAppAPIDesc=fullAppAPIDesc)
    yaopeiSkillInfo = getYaopeiSkillInfo(p, i)
    limits = formatLimitArray(i)
    additionalLimits = getAdditionalLimits(i)
    shopLimits = formatShopLimitArray(i)
    lvReq = getLvReq(p, i)
    flyUpLvReq = getFlyUpLvReq(p, i)
    if isCompositeShop:
        compositeShopData = extraData
    else:
        compositeShopData = ''
    if hasattr(i, 'lifeSkillItemMaker'):
        maker = "<font color = \'#00f6ff\'>" + gameStrings.TEXT_ITEMTOOLTIPUTILS_2343 % i.lifeSkillItemMaker + '</font>'
    elif hasattr(i, 'fromIntimacyRole'):
        maker = "<font color = \'#00f6ff\'>" + gameStrings.TEXT_ITEMTOOLTIPUTILS_2343 % i.fromIntimacyRole + '</font>'
    elif (i.type == Item.BASETYPE_UNIDENTIFIED_EQUIP or i.isManualEquip()) and hasattr(i, 'makerRole') and i.makerRole:
        maker = "<font color = \'#ffcc31\'>" + gameStrings.TEXT_ITEMTOOLTIPUTILS_2343 % i.makerRole + ' </font>' + getMakeTypeDesc(i)
    else:
        maker = ''
    allRuneEffects, runeEquipData = getRuneInfo(i, isRuneEquipHasProp)
    hieroWakeInfo = getHieroInfo(i, isHieroEquipHasProp)
    ownerShip = True
    if inHeaderAssignMode:
        if assignTarget and getattr(p, 'gbId', 0) not in assignTarget:
            ownerShip = False
    famePrice = getFamePrice(i)
    returnTime = getReturnTime(i)
    learnDesc = getLearnDesc(p, i)
    freezeUseTime = getFreezeUseTime(i)
    isEquip = i.isEquip()
    noBuyBack = itemData.get('noBuyBack', 0)
    shihunInfo, shihunExpire = getShiHunInfo(i)
    rubbingId = getattr(i, 'rubbing', None)
    if rubbingId != None and rubbingId != 0:
        surfaceValidity = getattr(i, 'rubbingTTLExpireTime', None)
        isValid = utils.getNow() >= surfaceValidity
        itemOtherShow = ID.data.get(rubbingId, {}).get('name', '')
    else:
        surfaceValidity = None
        itemOtherShow = ''
    itemOtherShowLab = ''
    if itemOtherShow:
        itemOtherShowLab = "<font color = \'#73E539\'>" + gameStrings.TEXT_ITEMTOOLTIPUTILS_2389 + itemOtherShow + gameStrings.TEXT_ITEMTOOLTIPUTILS_2389_1
    cornerMark = getCornerMark(i)
    surfaceLabel = ''
    if surfaceValidity != None:
        surfaceLabelTmp = gameStrings.TEXT_ITEMTOOLTIPUTILS_2395
        if surfaceValidity:
            surfaceLabelTmp = surfaceLabelTmp + time.strftime('%Y.%m.%d  %H:%M', time.localtime(surfaceValidity))
        if isValid == False:
            surfaceLabel = "<font color = \'#73E539\'>" + surfaceLabelTmp + '</font>'
        elif surfaceValidity != 0:
            surfaceLabel = "<font color = \'#F43804\'>" + surfaceLabelTmp + gameStrings.TEXT_ITEMTOOLTIPUTILS_2402
        else:
            surfaceLabel = "<font color = \'#73E539\'>" + surfaceLabelTmp + gameStrings.TEXT_ITEMTOOLTIPUTILS_2404
    autoFindWay = ''
    if itemData.has_key('navigatorTarget'):
        autoFindWay = gameStrings.TEXT_ITEMTOOLTIPUTILS_2407
    jingjie = getJingjieLimit(p, i)
    taozhuangDict = {}
    if hasattr(i, 'equipType'):
        taozhuangDict = getTaoZhuang(p, i, bRelative, location)
    baoshi = getBaoShiString(i)
    gemOwner = ''
    if i.type == Item.BASETYPE_EQUIP_GEM and hasattr(i, 'ownerRoleName'):
        gemOwner = gameStrings.TEXT_ITEMTOOLTIPUTILS_2419 + i.ownerRoleName
    newStarLv = getNewStarLv(i, location)
    jianding = getJianDing(i)
    valuablesTime, valuablesTimeLimits = getTimeFromValuableItem(i)
    for limit in valuablesTimeLimits:
        if limit not in limits:
            limits.append(limit)

    ctrlDesc = getCtrlDesc(i, isInBag, location)
    latchOfTime = getattr(i, 'latchOfTime', 0)
    useTime['latchOfTime'] = latchOfTime
    isRedemption = getattr(i, 'redemption', False)
    lifeSkillEquipDesc = getLifeSkillEquipDesc(i)
    initiativeSkillDesc = getInitiativeSkillDesc(i)
    isDotaItem = Item.isDotaBattleFieldItem(i.id)
    pskillDesc = getPskillDesc(i)
    sellPriceDesc = getDotaItemSellPriceDesc(i)
    coinConsignDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_2453 if i.isItemCoinConsign() else ''
    lineTxt = gameStrings.TEXT_ITEMTOOLTIPUTILS_2453 if i.isItemCoinConsign() else ''
    coinConsignHint = getCoinConsignHint(itemData, i)
    crossConsign = False
    if gameconfigCommon.enableTabAuction() and gameconfigCommon.enableCrossConsign():
        crossConsign = True
    if i.isItemCrossConsign() and crossConsign:
        coinConsignDesc += gameStrings.TEXT_ITEMTOOLTIPUTILS_2465
        lineTxt += gameStrings.TEXT_ITEMTOOLTIPUTILS_2465
        if len(lineTxt) > 13:
            coinConsignDesc += '<br>'
            lineTxt = ''
    if i.type == Item.BASETYPE_EQUIP and hasattr(i, 'maxEnhlv') and i.maxEnhlv > 0:
        coinConsignDesc += gameStrings.TEXT_ITEMTOOLTIPUTILS_2472
        lineTxt += gameStrings.TEXT_ITEMTOOLTIPUTILS_2472
        if len(lineTxt) > 13:
            coinConsignDesc += '<br>'
            lineTxt = ''
    if ED.data.get(i.id, {}).get('canPeel', 0):
        coinConsignDesc += gameStrings.TEXT_ITEMTOOLTIPUTILS_2479
        lineTxt += gameStrings.TEXT_ITEMTOOLTIPUTILS_2479
        if len(lineTxt) > 13:
            coinConsignDesc += '<br>'
            lineTxt = ''
    if i.canDisass():
        coinConsignDesc += gameStrings.CAN_DISASS_TXT
        lineTxt += gameStrings.CAN_DISASS_TXT
        if len(lineTxt) > 13:
            coinConsignDesc += '<br>'
            lineTxt = ''
    bindingConquestTimeDesc, bindingConquestEndStamp = getBindingConquestInfo(i)
    unbindTimes = ''
    if BigWorld.component == 'client' or fullAppAPIDesc:
        configTimes = ED.data.get(i.id, {}).get('unbindTimes', 0)
        equipUnbindTimes = getattr(i, 'unbindTimes', None)
        if equipUnbindTimes:
            unbindTimes = gameStrings.TEXT_ITEMTOOLTIPUTILS_2501 % (configTimes - equipUnbindTimes)
        elif configTimes > 0:
            unbindTimes = gameStrings.TEXT_ITEMTOOLTIPUTILS_2501 % configTimes
    mixJewelry = ''
    if gameconfigCommon.enableMixJewelry():
        if ED.data.get(i.id, {}).get('mixJewelryId', ()):
            mixJewelry = gameStrings.TEXT_ITEMTOOLTIPUTILS_2508
    isYaopeiMaxLv = i.getYaoPeiLv() >= SCD.data.get('maxYaoPeiLv', 20)
    guanYinSkillsInfo = getGuanYinSkillsInfo(i)
    guanYinSuperSkill = getGuanYinSuperSkill(i)
    lotteryInfo = getLotteryInfo(i)
    needIdentify = ''
    if i.isUnidentifiedManualEquip():
        needIdentify = gameStrings.TEXT_ITEMTOOLTIPUTILS_268
    configData = getGuiBaoGeConfigData(i.id)
    getWay = generateGetWay(configData.get('getway', []))
    specialPropLen = i.getSpecialPropLevel()
    ret = {'itemID': i.id,
     'refiningSrcName': refiningSrcName,
     'itemName': itemName,
     'bindType': bindType,
     'dyeType': dyeType,
     'isCurrentEquip': bRelative,
     'price': price,
     'priceLabel': priceLabel,
     'iconPath': iconPath,
     'desc': desc,
     'runeDesc': runeDesc,
     'runePropDesc': runePropDesc,
     'enhLv': enhLv,
     'qualityColor': qualityColor,
     'score': score,
     'initScore': initScore,
     'useTime': useTime,
     'randHint': randHint,
     'dura': dura,
     'schReq': strSch,
     'equPart': equPart,
     'starLv': starLv,
     'maxStarLv': maxStarLv,
     'useSubEquipEnhLv': useSubEquipEnhLv,
     'lv': itemLv,
     'starExp': starExp,
     'maxStarExp': maxStarExp,
     'rank': rank,
     'aptitude': aptitude,
     'enhProp': enhProp,
     'extraProp': extraProp,
     'basicProp': basicProp,
     'shiftBasicProp': shiftBasicProp,
     'propList': propList,
     'shiftPropList': shiftPropList,
     'cornerMark': cornerMark,
     'extraSkill': extraSkill,
     'limits': limits,
     'additionalLimits': additionalLimits,
     'lvReq': lvReq,
     'flyUpLvReq': flyUpLvReq,
     'sexReq': sexReq,
     'compositeShopData': compositeShopData,
     'boothLabel': boothLabel,
     'boothPrice': boothPrice,
     'initStarLv': 0,
     'maker': maker,
     'mixJewelry': mixJewelry,
     'tianlunSlotNum': tianlunSlotNum,
     'dilunSlotNum': dilunSlotNum,
     'allRuneEffects': allRuneEffects,
     'runeEquipData': runeEquipData,
     'ownerShip': ownerShip,
     'returnTime': returnTime,
     'famePrice': famePrice,
     'learnDesc': learnDesc,
     'isEquip': isEquip,
     'noBuyBack': noBuyBack,
     'sPriceType': sPriceType,
     'dyeTTLExpireTime': dyeTTLExpireTime,
     'rongGuangExpireTime': rongGuangExpireTime,
     'huanfuExpireTime': huanfuExpireTime,
     'canRongGuang': canRongGuang,
     'gatypeLabel': gatypeLabel,
     'descTitle': descTitle,
     'funcDesc': funcDesc,
     'signDesc': signDesc,
     'historyDesc': historyDesc,
     'shihunInfo': shihunInfo,
     'shihunExpire': shihunExpire,
     'extraLimit': extraLimit,
     'autoFindWay': autoFindWay,
     'enhLvProp': enhLvProp,
     'enhDuProp': enhDuProp,
     'jingjie': jingjie,
     'enhFactor': enhFactor,
     'enhLvColor': enhLvColor,
     'baoshi': baoshi,
     'taozhuangDict': taozhuangDict,
     'wrap': wrap,
     'enhMaxLv': enhMaxLv,
     'isHorse': isHorse,
     'allTalents': allTalents,
     'talents': talents,
     'gemOwner': gemOwner,
     'rideWingStage': rideWingStage,
     'maxRideWingStage': maxRideWingStage,
     'allTalentLevels': allTalentLevels,
     'horseWindProp': horseWindProp,
     'enhJueXing': enhJueXing,
     'newStarLv': newStarLv,
     'jianding': jianding,
     'equipSkillDesc': equipSkillDesc,
     'valuablesTime': valuablesTime,
     'identify': needIdentify,
     'ctrlDesc': ctrlDesc,
     'shopLimits': shopLimits,
     'coinConsignDesc': coinConsignDesc,
     'coinConsignHint': coinConsignHint,
     'lifeSkillEquipDesc': lifeSkillEquipDesc,
     'initiativeSkillDesc': initiativeSkillDesc,
     'pskillDesc': pskillDesc,
     'sellPriceDesc': sellPriceDesc,
     'isDotaItem': isDotaItem,
     'surfaceLabel': surfaceLabel,
     'itemOtherShowLab': itemOtherShowLab,
     'isRedemption': isRedemption,
     'freezeUseTime': freezeUseTime,
     'bindingConquestTimeDesc': bindingConquestTimeDesc,
     'bindingConquestEndStamp': bindingConquestEndStamp,
     'isYaoPei': i.isYaoPei(),
     'yaoPeiScore': yaoPeiScore,
     'yaopeiDetailScore': yaopeiDetailScore,
     'unbindTimes': unbindTimes,
     'isYaopeiMaxLv': isYaopeiMaxLv,
     'yaopeiSkillInfo': yaopeiSkillInfo,
     'isGuanYin': i.isGuanYin(),
     'guanYinSkillsInfo': guanYinSkillsInfo,
     'guanYinSuperSkill': guanYinSuperSkill,
     'lotteryInfo': lotteryInfo,
     'hieroWakeInfo': hieroWakeInfo,
     'exciteReq': exciteReq,
     'getWay': getWay,
     'guiBaoCoin': getItemGuiBaoCoin(i.id),
     'specialPropLen': specialPropLen}
    if location:
        func = TIP_FUNC_DICT.get(location, None)
        if func != None:
            ret = func(p, i, ret)
    return ret


def getItemGuiBaoCoin(itemId):
    return 0


def getCoinConsignHint(itemData, item):
    now = utils.getNow()
    coinPayLimit = utils.getItemCoinPayMailLimit(itemData)
    if not coinPayLimit:
        return ''
    elif item.canItemHandover(owner=None, msgId=0):
        return gameStrings.COIN_CONSIGN_HINT_1 % coinPayLimit
    else:
        tEnd = item.tCoinMail + SCD.data.get('coinMailCDDays', 0) * const.TIME_INTERVAL_DAY
        return gameStrings.COIN_CONSIGN_HINT_2 % utils.formatDuration(tEnd - now)


def getGuiBaoGeConfigData(id):
    guibaoId = GBGIRD.data.get(id, 0)
    if guibaoId:
        return GBGD.data.get(guibaoId, {})
    return {}


def generateGetWay(ways):
    getStr = ''
    for idx in ways:
        getStr += GBDCD.data.get('getway', {}).get(idx, '') + '\n'

    return getStr


INT_FLAG = 0

def getBindingConquestInfo(item):
    return (utils.pyStrToAsStr(SCD.data.get('BINDING_CONQUEST_DESC', '')), item.getGroupTradeEndStamp())


def generateDesc(pskillId, pSkillInfo, pskillLv = 1):
    desc = PD.data[pskillId, pskillLv]['desc']
    matchobj = re.search('\\$(.+?)\\$', desc)
    while matchobj:
        if matchobj.group(1) + 'Type' in PD.data[pskillId, 1]:
            valueType = PD.data[pskillId, 1][matchobj.group(1) + 'Type']
            value = pSkillInfo.getSkillData(matchobj.group(1))
        else:
            pSkillData = pSkillInfo.getSkillData('affectSkillData')[int(matchobj.group(1)[8:]) - 1]
            dataType = pSkillData[0]
            arg = pSkillData[1]
            index = pSkillData[2]
            if (dataType, arg, index) in RTD.data:
                valueType = RTD.data[dataType, arg, index]['flag']
            value = pSkillData[4]
        if valueType == INT_FLAG:
            if value == int(value):
                desc = desc.replace(matchobj.group(0), str(int(value)))
            else:
                desc = desc.replace(matchobj.group(0), str(int(value * 1000) / 1000.0))
        else:
            desc = desc.replace(matchobj.group(0), str(int(value * 100)))
        matchobj = re.search('\\$(.+?)\\$', desc)

    return desc


def getExtraLimit(p, item):
    if not p:
        return ''
    conditionsList = ID.data.get(item.id, {}).get('conditionsList', [])
    ret = ''
    isCheck = False
    for index, condition in enumerate(conditionsList):
        redColor = False
        if isCheck:
            isCheck = False
            continue
        extraLimitStr = ''
        value = 0
        if condition[0] == const.CON_FAME:
            fameId = condition[1]
            value = p.fame.get(fameId, 0)
            fameName = FD.data.get(fameId, {}).get('name', gameStrings.TEXT_CHALLENGEPROXY_199_1)
            extraLimitStr += gameStrings.TEXT_ITEMTOOLTIPUTILS_2637 + fameName + ': '
        elif condition[0] == const.CON_SOCIAL_LV:
            value = p.socLv
            extraLimitStr += gameStrings.TEXT_ITEMTOOLTIPUTILS_2640
        elif condition[0] == const.CON_SOCIAL_SCHOOL:
            value = p.curSocSchool
            schoolName = SSD.data.get(condition[3], {}).get('job', '')
            extraLimitStr += gameStrings.TEXT_ITEMTOOLTIPUTILS_2644 + schoolName
            if value == condition[3]:
                ret += extraLimitStr + '\n'
            else:
                ret += "<font color=\'#FF0000\'>" + extraLimitStr + '</font>\n'
            continue
        elif condition[0] == const.CON_LIFE_SKILL:
            skillId = condition[1]
            skillName = LIFE_SKILL[skillId]
            value = p.lifeSkill.get(skillId, {}).get('level', 0)
            extraLimitStr += gameStrings.TEXT_ITEMTOOLTIPUTILS_2637 + skillName + gameStrings.TEXT_ITEMTOOLTIPUTILS_2654
        elif condition[0] == const.CON_PROP:
            propId = condition[1]
            value = commcalc.getAvatarPropValueById(p, propId)
            propName = PPD.data.get(propId, {}).get('chName', gameStrings.TEXT_ITEM_3581)
            extraLimitStr += gameStrings.TEXT_ITEMTOOLTIPUTILS_2637 + propName + ': '
        elif condition[0] == const.CON_BUFF:
            stateId = condition[3]
            stateName = SDD.data.get(stateId, {}).get('name', '')
            extraLimitStr += gameStrings.TEXT_ITEMTOOLTIPUTILS_2663 + stateName
            redColor = True
            for state in p.states:
                if stateId in state:
                    redColor = False
                    break

            if redColor:
                ret += "<font color=\'#FF0000\'>" + extraLimitStr + '</font>\n'
            else:
                ret += extraLimitStr + '\n'
            continue
        elif condition[0] == const.CON_SKILL_ENHANC_POINT:
            value = utils.getTotalSkillEnhancePoint(p)
            extraLimitStr += gameStrings.TEXT_ITEMTOOLTIPUTILS_2676
        elif condition[0] == const.CON_NO_BUFF:
            stateId = condition[3]
            stateName = SDD.data.get(stateId, {}).get('name', '')
            extraLimitStr += gameStrings.TEXT_ITEMTOOLTIPUTILS_2680 + stateName
            redColor = False
            for state in p.states:
                if stateId in state:
                    redColor = True
                    break

            if redColor:
                ret += "<font color=\'#FF0000\'>" + extraLimitStr + '</font>\n'
            else:
                ret += extraLimitStr + '\n'
            continue
        elif condition[0] == const.CON_QUEST:
            questId = condition[1]
            questName = QD.data.get(questId, {}).get('name', '')
            extraLimitStr += gameStrings.TEXT_ITEMTOOLTIPUTILS_2694 + questName
            redColor = questId not in p.quests
            if redColor:
                ret += "<font color=\'#FF0000\'>" + extraLimitStr + '</font>\n'
            else:
                ret += extraLimitStr + '\n'
            continue
        elif condition[0] == const.CON_XIU_WEI_LEVEL:
            value = p.xiuweiLevel
            extraLimitStr += gameStrings.TEXT_ITEMTOOLTIPUTILS_2703
        op = condition[2]
        limit = str(condition[3])
        limitInt = condition[3]
        if op == const.CON_EQUAL:
            if value != limitInt:
                redColor = True
            extraLimitStr += limit
        elif op in (const.CON_GREATER_EQUAL, const.CON_GREATER):
            if index + 1 < len(conditionsList) and conditionsList[index + 1][0] == condition[0] and conditionsList[index + 1][1] == condition[1]:
                isCheck = True
                if value < limitInt or value > conditionsList[index + 1][3]:
                    redColor = True
                extraLimitStr += limit + '~' + str(conditionsList[index + 1][3])
            else:
                if value < limitInt:
                    redColor = True
                extraLimitStr += limit
        elif op in (const.CON_SMALLER_EQUAL, const.CON_SMALLER):
            if value > limitInt:
                redColor = True
            extraLimitStr += '0~' + limit
        if redColor:
            ret += "<font color=\'#FF0000\'>" + extraLimitStr + '</font>\n'
        else:
            ret += extraLimitStr + '\n'

    return ret


def getEnhLvColor(maxEnhlv, enhanceRefining):
    data = {}
    for i in xrange(1, maxEnhlv + 1):
        color = 0
        data2 = EERD.data.get(i, {})
        minValue = 0
        maxValue = 0
        progressList = data2.get('enhEffects', 0)
        colorDiv = int(data2.get('colorDiv', 0) * 100)
        for it in progressList:
            if it[0] > maxValue:
                maxValue = it[0]
            if it[0] < minValue or minValue == 0:
                minValue = it[0]

        minValue = int(minValue * 100)
        maxValue = int(maxValue * 100)
        if enhanceRefining.has_key(i):
            value = enhanceRefining[i] * 100
            if value <= colorDiv:
                color = 1
            elif int(value) == maxValue:
                color = 2
            else:
                color = 3
        data[i] = color

    return data


def getBaoShiString(item):
    baoShiList = []
    if not hasattr(item, 'yinSlots') or not hasattr(item, 'yangSlots'):
        return baoShiList
    getBaoShiList(item, baoShiList, 'yinSlots')
    getBaoShiList(item, baoShiList, 'yangSlots')
    return baoShiList


def getBaoShiList(item, baoShiList, baoShiTypeName):
    for prop in getattr(item, baoShiTypeName):
        baiShiSubType = 0
        desc = getBaoShiDesc(prop)
        if not prop.gem or not prop.gem.id:
            continue
        else:
            baiShiSubType = getEquipGemType(prop.gem.id)
        enable = True
        if not getattr(prop.gem, 'isValidGem', True):
            desc += gameStrings.EQUIP_CHANGE_GEM_LOCK
            enable = False
        elif gameconfigCommon.enableNewLv89():
            if hasattr(item, 'isSesWenYinEnh') and item.isSesWenYinEnh() != 0:
                desc += '(+%s%%)' % str(item.isSesWenYinEnh() * 100)
        baoShiList.append((baoShiTypeName,
         desc,
         Item.GEM_SLOT_FILLED,
         baiShiSubType,
         enable))

    return baoShiList


def getEquipGemType(gemId):
    gemData = utils.getEquipGemData(gemId)
    subType = gemData.get('subType', 0)
    lv = gemData.get('lv', 0)
    if not subType or not lv:
        return 0
    return (subType - 1) * 5 + min(5, max(lv - 2, (lv + 1) / 2))


def getBaoShiDesc(prop):
    desc = ''
    if not hasattr(prop, 'gem'):
        return desc
    if not prop.gem:
        return desc
    if prop.state == 1 and not prop.gem:
        desc = ''
    else:
        desc += prop.gem.name + ': '
        pType = prop.gemProps[0][1]
        info = PRD.data[prop.gemProps[0][0]]
        desc += info['name'] + '  '
        desc += formatProp(prop.gemProps[0][2], pType, info.get('showType', 0))
    return desc


def formatProp(propNum, pType, showType, hasFont = '', delNum = 0):
    propStr = ''
    if pType == 1:
        propStr = str(round(propNum * 100, 1)) + '%' + hasFont
    elif pType == 0:
        if showType == 0:
            if delNum > 0:
                propStr = "<font color =\'#ff0000\'>" + str(float2Int(propNum) - float2Int(delNum)) + '</font>'
            else:
                propStr = str(float2Int(propNum))
        elif showType == 2:
            if delNum > 0:
                propStr = "<font color =\'#ff0000\'>" + str(round(propNum, 1) - round(delNum, 1)) + '</font>'
            else:
                propStr = str(round(propNum, 1))
        elif delNum > 0:
            propStr = "<font color =\'#ff0000\'>" + str(round(propNum * 100, 1) - round(delNum * 100, 1)) + '%</font>'
        else:
            propStr = str(round(propNum * 100, 1)) + '%'
        propStr += hasFont
    return propStr


def getTaoZhuang(p, item, bRelative, location):
    taozhuangDict = {}
    taozhuangName = ''
    taozhuangGetSkill = ''
    taozhuangNotGetSkill = ''
    taozhuangList = []
    if BigWorld.component == 'client':
        import gameglobal
        if gameglobal.rds.ui.targetRoleInfo.mediator:
            if location == const.ITEM_IN_TARGET_ROLE and not bRelative:
                equipment = gameglobal.rds.ui.targetRoleInfo.equip
                suitsCache = gameglobal.rds.ui.targetRoleInfo.suitsCache
            elif bRelative:
                equipment = p.equipment
                suitsCache = p.suitsCache
            else:
                equipment = p.equipment
                suitsCache = p.suitsCache
        else:
            equipment = p.equipment
            suitsCache = p.suitsCache
    elif p and BigWorld.component == 'cell':
        equipment = p.equipment
        suitsCache = p.suitsCache
    else:
        equipment = {}
        suitsCache = {}
    mySuitId = getattr(item, 'suitId')
    if not mySuitId:
        return taozhuangDict
    taozhuangData = ESD.data.get(mySuitId, {})
    taozhuangShowData = ESSD.data.get(mySuitId, {})
    if len(taozhuangData.items()) <= 0:
        return taozhuangDict
    suits = taozhuangShowData.get('posName', [])
    if len(suits) <= 0:
        return taozhuangDict
    parentSuitIds = taozhuangData.items()[0][1].get('parentSuitId', [])
    suitEnabled = True
    if gameconfigCommon.enableEquipSuitReplace():
        for parentSuitId in parentSuitIds:
            if parentSuitId != mySuitId and parentSuitId in suitsCache:
                suitNum = suitsCache.get(parentSuitId, 0)
                parentData = ESD.data.get(parentSuitId, {})
                for num, sData in parentData.iteritems():
                    if num <= suitNum:
                        suitEnabled = False
                        break

            if not suitEnabled:
                break

    taozhuangName = taozhuangData.items()[0][1].get('name', '')
    taozhuangMaxNum = len(suits)
    taozhuangCurNum = suitsCache.get(mySuitId, 0) if suitEnabled else 0
    taozhuangName = gameStrings.TEXT_EQUIPCHANGESUITACTIVATEPROXY_372 % (taozhuangName, taozhuangCurNum, taozhuangMaxNum)
    if not suitEnabled:
        taozhuangName += gameStrings.ITEM_SUIT_DISABLE
    if taozhuangCurNum > 0:
        taozhuangName = "<font color=\'#73E539\'>" + taozhuangName + '</font>'
    for suit in suits:
        if len(suit) == 2:
            part = gametypes.EQUIP_SUIT_PART.get(suit[0], 0)
            equip = equipment.get(part)
            if equip:
                equipSuitId = getattr(equip, 'suitId')
                if equip.type == Item.BASETYPE_EQUIP and (equip.equipType == Item.EQUIP_BASETYPE_FASHION or equip.equipType == Item.EQUIP_BASETYPE_FASHION_WEAPON) and hasattr(equip, 'fashionTransProp'):
                    fashionTransProp = getattr(equip, 'fashionTransProp')
                    if fashionTransProp and len(fashionTransProp) >= 3:
                        srcItemName = ID.data.get(fashionTransProp[0], {}).get('name', '')
                        currentItemName = ID.data.get(equip.id, {}).get('name', '')
                        itemName = gameStrings.TEXT_ITEMTOOLTIPUTILS_2917 % (currentItemName, srcItemName)
                else:
                    itemName = suit[1]
                if equipSuitId == mySuitId:
                    taozhuangList.append((1, itemName))
                else:
                    taozhuangList.append((0, itemName))
            else:
                taozhuangList.append((0, suit[1]))

    taozhuangData = sorted(taozhuangData.iteritems(), key=lambda x: x[0])
    for item in taozhuangData:
        if item[0] == 'suits':
            continue
        desc = '[%s]%s<br>' % (str(item[0]), item[1].get('desc', ''))
        if item[0] <= taozhuangCurNum:
            taozhuangGetSkill += "<font color=\'#73E539\'>%s</font>" % desc
        else:
            taozhuangNotGetSkill += desc

    taozhuangDict = {'taozhuangName': taozhuangName,
     'taozhuangList': taozhuangList,
     'taozhuangGetSkill': taozhuangGetSkill,
     'taozhuangNotGetSkill': taozhuangNotGetSkill}
    return taozhuangDict


def getRideWingItemContent(p, itemId, stage):
    item = Item(itemId)
    if not item.isWingOrRide():
        return []
    item.rideWingStage = stage
    quality = ID.data.get(itemId, {}).get('quality', 1)
    canFly = False
    if item.isRideEquip():
        itemType = 1
        canFly = ED.data.get(item.id, {}).get('flyRide', 0)
    else:
        itemType = 2
        canFly = True
    hudKey = (quality, itemType, stage)
    currentInfo = HUD.data.get(hudKey, {})
    speedId = currentInfo.get('speedId', 0)
    content = []
    speedContent = getSpeedContent(p, speedId, canFly, itemType, item.isSwimRide())
    castContent = getCastContent(item)
    propContent = getPropContent(item)
    content.extend(propContent)
    content.extend(speedContent)
    content.extend(castContent)
    return content


def getPropContent(item):
    if not item.isWingOrRide():
        return []
    props = utils.getRideWingProps(item)
    if not props:
        return []
    content = []
    for prop in props:
        pType = prop[1]
        info = PRD.data.get(prop[0])
        prefixProp = ''
        prefixProp += info['name'] + ' '
        if info['type'] == 2:
            prefixProp += '+'
        elif info['type'] == 1:
            prefixProp += '-'
        prefixProp += formatProp(prop[2], pType, info.get('showType', 0))
        content.append(prefixProp)

    return content


def getCastContent(item):
    if not item.isWingOrRide():
        return []
    content = []
    horseQingGong = 0
    wingQingGong = 0
    if item.isRideEquip():
        canFly = ED.data.get(item.id, {}).get('flyRide', 0)
        if canFly:
            horseQingGong = utils.getHorseQinggongAdjust(item) * 10
            wingQingGong = utils.getWingQinggongAdjust(item) * 10
        else:
            horseQingGong = utils.getHorseQinggongAdjust(item) * 10
    else:
        wingQingGong = utils.getWingQinggongAdjust(item) * 10
    if horseQingGong:
        if item.isSwimRide():
            hStr = gameStrings.TEXT_ITEMTOOLTIPUTILS_3010 % horseQingGong
        else:
            hStr = gameStrings.TEXT_ITEMTOOLTIPUTILS_3012 % horseQingGong
        content.append(hStr)
    if wingQingGong:
        hStr = gameStrings.TEXT_ITEMTOOLTIPUTILS_3015 % wingQingGong
        content.append(hStr)
    return content


def getSpeedContent(p, speedId, isFly = False, itemType = 1, isSwimItem = False):
    content = []
    speedData = HSD.data.get(speedId, {})
    if not p:
        school = 3
    elif BigWorld.component == 'base':
        school = getSchoolFromBase(p.id)
    elif hasattr(p, 'school'):
        school = p.school
    else:
        school = 3
    avd = AD.data.get(school, {})
    if itemType == 1:
        commonMvSp = avd.get('rideSpeed', (0, 300))[1] / 60
    else:
        commonMvSp = avd.get('moveSpeed', (0, 300))[1] / 60
    commonFlySp = avd.get('flySpeed', (0, 300))[1] / 60
    dashCommonSpeed = PCD.data.get('dashForwardSpeed', 12)
    if not isSwimItem:
        runFactor = speedData.get('runFactor', 0)
        if runFactor:
            speed = commonMvSp * runFactor
            str = gameStrings.TEXT_ITEMTOOLTIPUTILS_3047 % speed
            content.append(str)
        dashFactor = speedData.get('dashFactor', 0)
        if dashFactor:
            speed = dashCommonSpeed * dashFactor
            str = gameStrings.TEXT_ITEMTOOLTIPUTILS_3052 % speed
            content.append(str)
    else:
        runFactor = speedData.get('swimRunFactor', 0)
        if runFactor:
            speed = commonMvSp * runFactor
            str = gameStrings.TEXT_ITEMTOOLTIPUTILS_3059 % speed
            content.append(str)
        dashFactor = speedData.get('swimDashFactor', 0)
        if dashFactor:
            speed = dashCommonSpeed * dashFactor
            str = gameStrings.TEXT_ITEMTOOLTIPUTILS_3064 % speed
            content.append(str)
    if isFly:
        flyMaxFactor = speedData.get('flyMaxFactor', 0)
        if flyMaxFactor:
            speed = commonFlySp * flyMaxFactor
            str = gameStrings.TEXT_ITEMTOOLTIPUTILS_3070 % speed
            content.append(str)
        flyRushMaxFactor = speedData.get('flyRushMaxFactor', 0)
        if flyRushMaxFactor:
            speed = commonFlySp * flyRushMaxFactor
            str = gameStrings.TEXT_ITEMTOOLTIPUTILS_3075 % speed
            content.append(str)
    return content


def getSchoolFromBase(roleId):
    import Netease
    rollVal = Netease.rollCache.get(roleId, None)
    if rollVal:
        return rollVal.school
    else:
        return -1


def getGemLimit(item, gemEquipTypeMap):
    limit = ''
    data = utils.getEquipGemData(item.id)
    limit += gameStrings.TEXT_ITEMTOOLTIPUTILS_3090 + str(data.get('orderLimit', 0))
    equipLimit = data.get('equipLimit', ())
    if len(equipLimit) == 0:
        return limit
    limit += gameStrings.TEXT_ITEMTOOLTIPUTILS_3094
    for equipId in equipLimit:
        limit += ' ' + gemEquipTypeMap.get(equipId, gameStrings.TEXT_BATTLEFIELDPROXY_1605)

    return limit


def getGemProp(prop):
    basicProp = ''
    specialDesc, _ = getSpecialDesc(prop)
    if specialDesc != '':
        basicProp = specialDesc + '<br>'
    for item in prop:
        pType = item[1]
        info = PRD.data[item[0]]
        basicProp += info['name'] + '  '
        if info['type'] == 2:
            basicProp += '+'
        elif info['type'] == 1:
            basicProp += '-'
        basicProp += formatProp(item[2], pType, info.get('showType', 0)) + '<br>'

    basicProp = "<font color=\'#BF7FFF\'>" + basicProp + '</font>'
    return basicProp


def TipInShop(p, it, infoDict):
    res = ''
    if infoDict.get('compositeShopData', None) != None:
        itemData = ID.data.get(it.id, None)
        if itemData and itemData.has_key('shopJingJieRequire'):
            jingJieLimit = itemData['shopJingJieRequire']
            jingJieName = JJD.data.get(jingJieLimit, {}).get('name', gameStrings.TEXT_COMPOSITESHOPHELPFUNC_324)
            res += gameStrings.TEXT_TIPUTILS_447
            res += gameStrings.TEXT_TIPUTILS_489
            res += gameStrings.TEXT_TIPUTILS_467
            res += "<font color = \'#ffff32\'>%s</font>\n" % (jingJieName,)
    infoDict['compositeShopData'] = res
    return infoDict


def TipInMall(p, it, infoDict):
    descNoCtrl = infoDict.get('ctrlDesc', None)
    itemData = ID.data.get(it.id, {})
    if itemData and descNoCtrl != None and itemData.get('ctrl', 0):
        descNoCtrl = gameStrings.TEXT_ITEMTOOLTIPUTILS_3135
    infoDict['ctrlDesc'] = descNoCtrl
    return infoDict


def TipInEquipMent(p, it, infoDict):
    infoDict['ctrlDesc'] = ''
    return infoDict


def TipInGuildStorage(p, it, infoDict):
    gatypeLabel = infoDict.get('gatypeLabel', '')
    if hasattr(it, 'gatype'):
        if it.gatype == gametypes.GUILD_STORAGE_ASSIGN_TYPE_MEMBER:
            gatypeLabel = gameStrings.TEXT_ITEMTOOLTIPUTILS_3147 % it.toRole
        elif it.gatype == gametypes.GUILD_STORAGE_ASSIGN_TYPE_ALL:
            gatypeLabel = gameStrings.TEXT_ITEMTOOLTIPUTILS_3149
    infoDict['gatypeLabel'] = gatypeLabel
    return infoDict


def TipInAvatarVideoAndWing(p, it, infoDict):
    infoDict['horseWindProp'] = ''
    infoDict['desc'] = ''
    infoDict['funcDesc'] = ''
    infoDict['limits'] = []
    infoDict['descTitle'] = ''
    infoDict['allTalents'] = []
    infoDict['isHorse'] = False
    infoDict['price'] = 0
    infoDict['lvReq'] = {'satisfy': True,
     'desc': ''}
    infoDict['coinConsignDesc'] = ''
    infoDict['newStarLv'] = {'maxStarLv': -1}
    infoDict['bindType'] = ''
    infoDict['equPart'] = ' '
    return infoDict


TIP_FUNC_DICT = {const.ITEM_IN_SHOP: TipInShop,
 const.ITEM_IN_MALL: TipInMall,
 const.ITEM_IN_EQUIPMENT: TipInEquipMent,
 const.ITEM_IN_GUILDSTORAGE: TipInGuildStorage,
 const.ITEM_IN_AVATAR_WING: TipInAvatarVideoAndWing}

def getJianDing(item):
    jianding = ''
    if item.canBeIdentified():
        lowId = getattr(item, 'identifyId', 0)
        lowItemName = ID.data.get(lowId, {}).get('name', gameStrings.TEXT_ITEMTOOLTIPUTILS_891)
        highId = LSQD.data.get(lowId, {}).get('fineItemId', 0)
        highItemName = ID.data.get(highId, {}).get('name', gameStrings.TEXT_ITEMTOOLTIPUTILS_891)
        highFactor = getattr(item, 'identifyQuality', 0)
        lowFactor = 100 - highFactor
        jianding += gameStrings.TEXT_ITEMTOOLTIPUTILS_3189 % highFactor
        jianding += gameStrings.TEXT_ITEMTOOLTIPUTILS_3190 % (lowItemName, lowFactor)
        jianding += gameStrings.TEXT_ITEMTOOLTIPUTILS_3191 % (highItemName, highFactor)
    return jianding


def getSpecialDesc(itemData, shiftInfo = []):
    prop = ''
    propIntervalList = []
    if not itemData or type(itemData) == tuple:
        return (prop, propIntervalList)
    itemData.sort(key=lambda x: x[0])
    shiftInfo.sort(key=lambda x: x[0])
    deleteList = []
    delShiftList = []
    propIntervalDict = {}
    for num, item in enumerate(itemData):
        if item[0] == PHYSICAL_ATTACK_DOWN:
            if len(item) < 5 or not item[5]:
                pValue = str(shiftInfo[num][1] if len(shiftInfo) > 0 else item[2])
                prop += gameStrings.TEXT_ITEMTOOLTIPUTILS_3214 % pValue
            else:
                pValue = str(item[2] - item[5])
                prop += gameStrings.TEXT_ITEMTOOLTIPUTILS_3217 % pValue
            pShortName = PRD.data.get(PHYSICAL_ATTACK_DOWN, {}).get('shortName', '')
            propIntervalDict[PHYSICAL_ATTACK_DOWN] = [pShortName, '+%s' % pValue, item[3]]
            if len(shiftInfo) > 0:
                delShiftList.append(shiftInfo[num])
                if shiftInfo[num][2] > 0:
                    _value = round(shiftInfo[num][2], 2)
                    extraValue = ' (+%s%%)' % str([str(_value), int(_value)][int(_value) == _value])
                    propIntervalDict[PHYSICAL_ATTACK_DOWN][1] += extraValue
            deleteList.append(item)
        elif item[0] == PHYSICAL_ATTACK_UP:
            if len(item) < 5 or not item[5]:
                pValue = str(shiftInfo[num][1] if len(shiftInfo) > 0 else item[2])
                prop += pValue
            else:
                pValue = str(item[2] - item[5])
                prop += "<font color=\'#FB0000\'>%s</font>" % pValue
            pShortName = PRD.data.get(PHYSICAL_ATTACK_UP, {}).get('shortName', '')
            propIntervalDict[PHYSICAL_ATTACK_UP] = [pShortName, '+%s' % pValue, item[3]]
            if len(shiftInfo) > 0:
                delShiftList.append(shiftInfo[num])
                if shiftInfo[num][2] > 0:
                    _value = round(shiftInfo[num][2], 2)
                    extraValue = ' (+%s%%)' % str([str(_value), int(_value)][int(_value) == _value])
                    propIntervalDict[PHYSICAL_ATTACK_UP][1] += extraValue
                    prop += extraValue
            deleteList.append(item)
        elif item[0] == SPELL_ATTACK_DOWN:
            if len(item) < 5 or not item[5]:
                pValue = str(shiftInfo[num][1] if len(shiftInfo) > 0 else item[2])
                prop += gameStrings.TEXT_ITEMTOOLTIPUTILS_3255 % pValue
            else:
                pValue = str(item[2] - item[5])
                prop += gameStrings.TEXT_ITEMTOOLTIPUTILS_3258 % pValue
            pShortName = PRD.data.get(SPELL_ATTACK_DOWN, {}).get('shortName', '')
            propIntervalDict[SPELL_ATTACK_DOWN] = [pShortName, '+%s' % pValue, item[3]]
            if len(shiftInfo) > 0:
                delShiftList.append(shiftInfo[num])
                if shiftInfo[num][2] > 0:
                    _value = round(shiftInfo[num][2], 2)
                    extraValue = ' (+%s%%)' % str([str(_value), int(_value)][int(_value) == _value])
                    propIntervalDict[SPELL_ATTACK_DOWN][1] += extraValue
            deleteList.append(item)
        elif item[0] == SPELL_ATTACK_UP:
            if len(item) < 5 or not item[5]:
                pValue = str(shiftInfo[num][1] if len(shiftInfo) > 0 else item[2])
                prop += pValue
            else:
                pValue = str(item[2] - item[5])
                prop += "<font color=\'#FB0000\'>%s</font>" % pValue
            pShortName = PRD.data.get(SPELL_ATTACK_UP, {}).get('shortName', '')
            propIntervalDict[SPELL_ATTACK_UP] = [pShortName, '+%s' % pValue, item[3]]
            if len(shiftInfo) > 0:
                delShiftList.append(shiftInfo[num])
                if shiftInfo[num][2] > 0:
                    _value = round(shiftInfo[num][2], 2)
                    extraValue = ' (+%s%%)' % str([str(_value), int(_value)][int(_value) == _value])
                    propIntervalDict[SPELL_ATTACK_UP][1] += extraValue
                    prop += extraValue
            deleteList.append(item)
        if item[0] in PROPS_SHOW_SHRINK:
            itemData[num] = (item[0], item[1], round(item[2] / 100.0, 1))

    for item in deleteList:
        itemData.remove(item)

    for item in delShiftList:
        shiftInfo.remove(item)

    for pId, value in propIntervalDict.iteritems():
        propIntervalList.append([pId,
         value[0],
         value[1],
         value[2]])

    propIntervalList.sort(key=lambda x: x[0])
    return (prop, propIntervalList)


def getRunePropDesc(item):
    if item.isNewHieroCrystal():
        baseAdd = item.subSysProps.get(item.ITEM_SUB_SYSTEM_PROPS_HIEROGRAM, {}).get('baseAdd', 0)
        feedCnt = item.subSysProps.get(item.ITEM_SUB_SYSTEM_PROPS_HIEROGRAM, {}).get('feedCount', 0)
        return gameStrings.EQUIP_CHANGE_RUNE_PROP_DESC % (baseAdd * 1.0 / 10000 * 100, feedCnt)
    else:
        return ''


def getRuneDesc(i):
    runeDesc = ''
    if i.type in Item.BASETYPE_RUNES:
        if i.type == Item.BASETYPE_HIEROGRAM_CRYSTAL:
            rData = NRD.data.get(i.id, {})
        else:
            rData = RD.data.get(i.id, {})
        runeDesc += "<font color = \'#FFFFE5\'>"
        if RUNE_FORGING_LOW_LV in rData.get('qiFuLvList', []):
            runeDesc += gameStrings.TEXT_RUNEFORGINGPROXY_203
            if RUNE_FORGING_LOW_LV in i.runeQiFuData:
                runeDesc += '\n'
                qData = i.runeQiFuData[RUNE_FORGING_LOW_LV][1]
                for skillId in qData:
                    skillLv = qData[skillId]
                    runeDesc += generateDesc(skillId, PSkillInfo(skillId, skillLv, {}), skillLv) + '\n'
                    qiFuId = i.runeQiFuData[RUNE_FORGING_LOW_LV][0]
                    effects = RQED.data.get(qiFuId).get('effects', [])
                    for effect in effects:
                        if effect[0] == gametypes.RUNE_QIFU_EFFECT_TYPE_SHENLI:
                            runeDesc += const.RUNE_POWER_DESC[effect[1]] + '*' + str(effect[2]) + '\n'

            else:
                runeDesc += gameStrings.TEXT_RUNEFORGINGPROXY_218
        if RUNE_FORGING_LHIGH_LV in rData.get('qiFuLvList', []):
            runeDesc += gameStrings.TEXT_RUNEFORGINGPROXY_221
            if RUNE_FORGING_LHIGH_LV in i.runeQiFuData:
                runeDesc += '\n'
                qData = i.runeQiFuData[RUNE_FORGING_LHIGH_LV][1]
                for skillId in qData:
                    skillLv = qData[skillId]
                    runeDesc += generateDesc(skillId, PSkillInfo(skillId, skillLv, {}), skillLv) + '\n'
                    qiFuId = i.runeQiFuData[RUNE_FORGING_LHIGH_LV][0]
                    effects = RQED.data.get(qiFuId).get('effects', [])
                    for effect in effects:
                        if effect[0] == gametypes.RUNE_QIFU_EFFECT_TYPE_SHENLI:
                            runeDesc += const.RUNE_POWER_DESC[effect[1]] + '*' + str(effect[2]) + '\n'

            else:
                runeDesc += gameStrings.TEXT_RUNEFORGINGPROXY_218
        runeDesc += '</font>'
        if BigWorld.component == 'client':
            propDesc = BigWorld.player().getRuneData(i.id, 'propDesc', None)
            addPercent = BigWorld.player().getRuneAddPercent(i)
            if addPercent:
                addPrecentDesc = '(+%.2f%%)' % (addPercent * 100)
            else:
                addPrecentDesc = ''
            if propDesc:
                runeDesc += "<font color = \'#BF7FFF\'>"
                runeDesc += propDesc + addPrecentDesc + '\n'
                runeDesc += '</font>'
        else:
            addPrecentDesc = ''
        if i.id in RD.data and 'pskillList' in RD.data.get(i.id, {}) and RD.data.get(i.id, {}).get('pskillList', ''):
            runeDesc += "<font color = \'#BF7FFF\'>"
            for skillId, skillLv in RD.data.get(i.id, {}).get('pskillList', ''):
                runeDesc += generateDesc(skillId, PSkillInfo(skillId, skillLv, {}), skillLv) + addPrecentDesc + '\n'

            runeDesc = runeDesc[:-1]
            runeDesc += '</font>'
    return runeDesc


def getTimeFromValuableItem(item):
    limits = []
    valuablesTime = 0
    if item and hasattr(item, 'valuableLatchOfTime'):
        latchOfTime = item.valuableLatchOfTime - 2 * SCD.data.get('redemptionDeliverTime', const.REDEMPTION_DELIVER_TIME)
        valuablesTime = max(latchOfTime - utils.getNow(), 0)
        if valuablesTime > 0:
            limits = SCD.data.get('valuableItemLimits', [NO_BOOTH,
             NO_SELL,
             NO_CONSIGN,
             NO_DISCARD,
             NO_MAIL,
             NO_TRADE])
    return (valuablesTime, limits)


def showFishingLabourAndMental(item):
    baseDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_3391
    labourDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_3392
    mentalDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_3393
    ret = ''
    if item and item.whereEquipFishing() == gametypes.FISHING_EQUIP_ROD:
        fed = SLSED.data.get(item.id, {})
        if not fed:
            return
        fishingLabourNeed = fed.get('needLabour', 0)
        fishingMentalNeed = fed.get('needMental', 0)
        if fishingLabourNeed <= 0 and fishingMentalNeed <= 0:
            fishingLabourNeed = SCD.data.get('fishingLabourNeed', 10)
        if fishingLabourNeed > 0:
            ret += baseDesc + labourDesc % (fishingLabourNeed / 10.0)
        if fishingMentalNeed > 0:
            if fishingLabourNeed <= 0:
                ret += baseDesc + mentalDesc % (fishingMentalNeed / 10.0)
            else:
                ret += ',' + mentalDesc % (fishingMentalNeed / 10.0)
    if ret:
        ret += '\n'
    return ret


def showExploreLabourAndMental(item):
    baseDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_3416
    labourDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_3392
    mentalDesc = gameStrings.TEXT_ITEMTOOLTIPUTILS_3393
    ret = ''
    if item:
        fData = SLSED.data.get(item.id, {})
        exploreId = fData.get('exploreId', 0)
        exploreData = EXD.data.get(exploreId, {})
    if fData and fData.get('displayDist', 0):
        exploreLabourNeed = exploreData.get('needLabour', 0)
        exploreMentalNeed = exploreData.get('needMental', 0)
        if exploreLabourNeed > 0:
            ret += baseDesc + labourDesc % (exploreLabourNeed / 10.0)
        if exploreMentalNeed > 0:
            if exploreLabourNeed <= 0:
                ret += baseDesc + mentalDesc % (exploreMentalNeed / 10.0)
            else:
                ret += ',' + mentalDesc % (exploreMentalNeed / 10.0)
    if ret:
        ret += '\n'
    return ret


def getYaopeiBasicPropList(i):
    basicPropList = []
    shiftBasicPropList = []
    if not i.isYaoPei():
        return (basicPropList, shiftBasicPropList)
    simple = []
    detail = []
    basicAdd, _, _ = i.getYaoPeiPropsAdd(i.getYaoPeiLv())
    if hasattr(i, 'yaoPeiProps'):
        for idx, (pid, pType, pVal) in enumerate(i.yaoPeiProps):
            if pType == gametypes.DATA_TYPE_NUM and i._isIntPropRef(pid):
                simple.append((pid,
                 pType,
                 pVal * basicAdd if basicAdd > 0 else pVal,
                 idx))
                detail.append((pid,
                 pType,
                 pVal,
                 idx))

    if basicAdd > 0:
        addPercent = round((basicAdd - 1) * 100)
        bonus = '(+%d%%)' % addPercent if addPercent > 0 else ''
    else:
        bonus = ''
    _, basicPropList = getBasicProp(i, simple)
    _, shiftBasicPropList = getBasicProp(i, detail, bonus)
    return (basicPropList, shiftBasicPropList)


def getYaopeiRandPropList(i, rand):
    randPropList = []
    shiftRandPropList = []
    if not i.isYaoPei():
        return (randPropList, shiftRandPropList)
    if rand:
        for item in rand:
            prdData = PRD.data.get(item[0], {})
            pShortName = prdData.get('shortName', '')
            showType = prdData.get('showType', 0)
            if prdData.get('type', 0) == 2:
                pValue = '+'
            elif prdData.get('type', 0) == 1:
                pValue = '-'
            else:
                pValue = ''
            _, extraAdd, _ = i.getYaoPeiPropsAdd(i.getYaoPeiLv())
            if extraAdd > 0:
                addPercent = round((extraAdd - 1) * 100)
                bonus = '(+%d%%)' % addPercent if addPercent > 0 else ''
            else:
                bonus = ''
            simple = '%s%s' % (pValue, formatProp(item[2] * extraAdd, item[1], showType))
            detail = '%s%s%s' % (pValue, formatProp(item[2], item[1], showType), bonus)
            randPropList.append([item[0],
             pShortName,
             simple,
             item[4]])
            shiftRandPropList.append([item[0],
             pShortName,
             detail,
             item[4]])

    return (randPropList, shiftRandPropList)


def getYaopeiExtraPropList(i):
    extraPropList = []
    shiftExtraPropList = []
    if not i.isYaoPei():
        return (extraPropList, shiftExtraPropList)
    extraProps = YPD.data.get(i.id, {}).get('extraProps', [])
    if hasattr(i, 'yaoPeiExtraProps') and len(extraProps) == len(i.yaoPeiExtraProps):
        tipsPropProgressBarOffset = SCD.data.get('tipsPropProgressBarOffset', 0)
        yaopeiLv = i.getYaoPeiLv()
        _, extraAdd, _ = i.getYaoPeiPropsAdd(yaopeiLv)
        for num, (pId, pType, pVal, minVal, maxVal, lv) in enumerate(i.yaoPeiExtraProps):
            if pType != gametypes.DATA_TYPE_NUM:
                continue
            prdData = PRD.data.get(pId, {})
            pShortName = prdData.get('shortName', '')
            showType = prdData.get('showType', 0)
            minminVal = minVal
            maxmaxVal = maxVal
            poolId, _ = extraProps[num]
            yepdData = YEPD.data.get(poolId, [])
            for yepd in yepdData:
                if yepd.get('aid', 0) == pId:
                    minminVal = yepd.get('minValue', (0, 0))[0]
                    maxmaxVal = yepd.get('maxValue', (0, 0))[1]
                    break

            remainingOffset = 100 - tipsPropProgressBarOffset
            if remainingOffset > 0 and maxmaxVal != minminVal:
                perOffset = (maxmaxVal - minminVal) * 1.0 / remainingOffset
            else:
                perOffset = 1
            barValue = int((maxVal - minminVal) / perOffset + tipsPropProgressBarOffset)
            subBarValue = int((pVal - minminVal) / perOffset + tipsPropProgressBarOffset)
            pRange = '(%s~%s)' % (formatProp(minVal, pType, showType), formatProp(maxVal, pType, showType))
            if yaopeiLv >= lv:
                if extraAdd > 0:
                    addPercent = round((extraAdd - 1) * 100)
                    bonus = '(+%d%%)' % addPercent if addPercent > 0 else ''
                else:
                    bonus = ''
                simple = '+%s' % formatProp(pVal * extraAdd, pType, showType)
                detail = '+%s%s%s' % (formatProp(pVal, pType, showType), pRange, bonus)
                pShortName = toHtml(pShortName, '#FFB914')
                simple = toHtml(simple, '#E5CF5C')
                detail = toHtml(detail, '#E5CF5C')
                shiftExtraPropList.append({'pId': pId,
                 'pName': pShortName,
                 'pValue': detail,
                 'barType': 'yellow',
                 'barValue': barValue,
                 'subBarValue': subBarValue})
            else:
                activeLv = gameStrings.TEXT_ITEMTOOLTIPUTILS_552 % lv
                simple = '+%s%s' % (pRange, activeLv)
                detail = '+%s%s' % (pRange, activeLv)
                pShortName = toHtml(pShortName, '#808080')
                simple = toHtml(simple, '#808080')
                detail = toHtml(detail, '#808080')
                shiftExtraPropList.append({'pId': pId,
                 'pName': pShortName,
                 'pValue': detail,
                 'barType': 'no'})
            extraPropList.append({'pId': pId,
             'pName': pShortName,
             'pValue': simple})

    return (extraPropList, shiftExtraPropList)


def getGuanYinSkillsInfo(item):
    if item.isGuanYin():
        if BigWorld.component == 'client':
            gd = GD.data.get(item.id, {})
            if not gd:
                return {}
            info = {}
            pskillNum = gd.get('pskillNum', 0)
            info['pskillNum'] = pskillNum
            skillList = []
            import gameglobal
            targetRoleInfo = gameglobal.rds.ui.targetRoleInfo
            p = BigWorld.player()
            if gameconfigCommon.enableGuanYinThirdPhase():
                if p.equipment[gametypes.EQU_PART_CAPE] and p.equipment[gametypes.EQU_PART_CAPE].uuid == item.uuid:
                    item = BigWorld.player().guanYin
                elif targetRoleInfo.equip and targetRoleInfo.equip[gametypes.EQU_PART_CAPE] and targetRoleInfo.equip[gametypes.EQU_PART_CAPE].uuid == item.uuid:
                    item = targetRoleInfo.guanYin
            for i in xrange(pskillNum):
                if not item.validGuanYinPos(i, 0):
                    continue
                skillInfo = {}
                bookId = item.guanYinInfo[i][0]
                bookInfo = GBD.data.get(bookId, {})
                if bookInfo:
                    pskillId = bookInfo.get('pskillId', [])
                    if len(pskillId) > 0:
                        pskillId = pskillId[0]
                    else:
                        pskillId = 0
                    lv = bookInfo.get('lv', 0)
                    skillName = "<font color = \'#ea7fff\'>[%s]</font>" % PTD.data.get(pskillId, {}).get('sname', '')
                    equipSkillDesc = "<font color = \'#f2b2ff\'>%s</font>" % PD.data.get((pskillId, lv), {}).get('desc', '')
                    skillInfo['skillIcon'] = 'skill/icon/%d.dds' % PTD.data.get(pskillId, {}).get('icon', 0)
                    skillInfo['skillLv'] = ''
                    skillInfo['skillDesc'] = '%s<br>%s' % (skillName, equipSkillDesc)
                    skillInfo['reddisabled'] = item.checkGuanYinPskillTimeOut(i, 0)
                    skillList.append(skillInfo)

            info['skillList'] = skillList
            return info
    return {}


def getGuanYinSuperSkill(item):
    if item.isGuanYin():
        if BigWorld.component == 'client':
            gd = GD.data.get(item.id, {})
            if not gd:
                return {}
            info = {}
            info['canEquipSuperSkill'] = gd.get('canEquipSuperSkill', 0) and gameconfigCommon.enableGuanYinSuperSkill()
            if info['canEquipSuperSkill']:
                skillInfo = {}
                guanYin = BigWorld.player().guanYin
                superSkillBook = guanYin.getSuperSkillBook()
                if superSkillBook:
                    bookId = superSkillBook.guanYinSuperBookId
                    bookInfo = GBD.data.get(bookId, {})
                    if bookInfo and superSkillBook and superSkillBook.checkGuanYinSuperSkill():
                        pskillId = bookInfo.get('pskillId', [])
                        if len(pskillId) > 0:
                            pskillId = pskillId[0]
                        else:
                            pskillId = 0
                        lv = bookInfo.get('lv', 0)
                        skillName = "<font color = \'#ffb91c\'>[%s]</font>" % PTD.data.get(pskillId, {}).get('sname', '')
                        equipSkillDesc = "<font color = \'#ffe09c\'>%s</font>" % PD.data.get((pskillId, lv), {}).get('desc', '')
                        skillInfo['skillIcon'] = 'skill/icon/%d.dds' % PTD.data.get(pskillId, {}).get('icon', 0)
                        skillInfo['skillLv'] = ''
                        skillInfo['skillDesc'] = '%s<br>%s' % (skillName, equipSkillDesc)
                        skillInfo['reddisabled'] = False
                        info['superSkill'] = skillInfo
                        info['empty'] = False
                    else:
                        info['empty'] = True
                else:
                    info['empty'] = True
            return info
    return {}


def getLotteryInfo(i):
    if not i.isLottery():
        return ''
    else:
        lotteryNo = getattr(i, 'lotteryNo', None)
        if not lotteryNo:
            return gameStrings.TEXT_ITEMTOOLTIPUTILS_3671
        _, issueTime, nuid = utils.decodeLottery(lotteryNo)
        lotteryInfo = gameStrings.TEXT_ITEMTOOLTIPUTILS_3674 % (utils.formatDate(issueTime, delimiter='/'), utils.getDisplayLotteryNo(nuid))
        return lotteryInfo


def toHtml(txt, color = None):
    msg = txt
    if color:
        msg = "<font color=\'%s\'>%s</font>" % (color, msg)
    return msg


def addBasicPropList(i, propList, shiftPropList, basicPropList, shiftBasicPropList):
    if len(basicPropList) == 0:
        return
    for item in basicPropList:
        pName = toHtml(item[1], '#FFFFE5')
        pValue = toHtml(item[2], '#E4E4CD')
        propList.append({'pId': item[0],
         'pName': pName,
         'pValue': pValue})

    tipsPropProgressBarOffset = SCD.data.get('tipsPropProgressBarOffset', 0)
    if i.isYaoPei():
        if not hasattr(i, 'yaoPeiProps'):
            return
        propLen = len(i.yaoPeiProps)
        if propLen != len(shiftBasicPropList):
            return
        basicProps = YPD.data.get(i.id, {}).get('basicProps', [])
        for item in shiftBasicPropList:
            pId = item[0]
            idx = item[3]
            if idx >= propLen or i.yaoPeiProps[idx][0] != pId:
                continue
            pName = toHtml(item[1], '#FFFFE5')
            pValue = toHtml(item[2], '#E4E4CD')
            minVal = 0
            maxVal = 0
            for propItem in basicProps:
                if propItem[0] == pId:
                    minVal = propItem[2]
                    maxVal = propItem[3]
                    break

            if minVal == maxVal:
                shiftPropList.append({'pId': pId,
                 'pName': pName,
                 'pValue': pValue,
                 'barType': 'no'})
                continue
            remainingOffset = 100 - tipsPropProgressBarOffset
            if remainingOffset > 0 and maxVal != minVal:
                perOffset = (maxVal - minVal) / remainingOffset
            else:
                perOffset = 1
            curVal = i.yaoPeiProps[idx][2]
            barValue = int((curVal - minVal) / perOffset + tipsPropProgressBarOffset)
            subBarValue = barValue
            shiftPropList.append({'pId': pId,
             'pName': pName,
             'pValue': pValue,
             'barType': 'white',
             'barValue': barValue,
             'subBarValue': subBarValue})

    elif i.isManualEquip():
        if not hasattr(i, 'makeType') or not hasattr(i, 'props'):
            return
        propLen = len(i.props)
        if propLen != len(shiftBasicPropList):
            return
        basicProps = MEPD.data.get(i.id, {}).get('basicProps', [])
        if len(basicProps) <= i.makeType:
            return
        basicProps = basicProps[0]
        for item in shiftBasicPropList:
            pId = item[0]
            idx = item[3]
            if idx >= propLen or i.props[idx][0] != pId:
                continue
            pName = toHtml(item[1], '#FFFFE5')
            pValue = toHtml(item[2], '#E4E4CD')
            minVal = 0
            maxVal = 0
            for propItem in basicProps:
                if propItem[0] == pId:
                    minVal = propItem[2]
                    maxVal = propItem[3]
                    break

            if minVal == maxVal:
                shiftPropList.append({'pId': pId,
                 'pName': pName,
                 'pValue': pValue,
                 'barType': 'no'})
                continue
            remainingOffset = 100 - tipsPropProgressBarOffset
            if remainingOffset > 0 and maxVal != minVal:
                perOffset = (maxVal - minVal) / remainingOffset
            else:
                perOffset = 1
            curVal = i.props[idx][2]
            barValue = int((curVal - minVal) / perOffset + tipsPropProgressBarOffset)
            subBarValue = barValue
            shiftPropList.append({'pId': pId,
             'pName': pName,
             'pValue': pValue,
             'barType': 'white',
             'barValue': barValue,
             'subBarValue': subBarValue})

    elif i.isExtendedEquip():
        if not hasattr(i, 'props'):
            return
        propLen = len(i.props)
        if propLen != len(shiftBasicPropList):
            return
        basicProps = XEPD.data.get(i.id, {}).get('basicProps', [])
        for item in shiftBasicPropList:
            pId = item[0]
            idx = item[3]
            if idx >= propLen or i.props[idx][0] != pId:
                continue
            pName = toHtml(item[1], '#FFFFE5')
            pValue = toHtml(item[2], '#E4E4CD')
            minVal = 0
            maxVal = 0
            for propItem in basicProps:
                if propItem[0] == pId:
                    minVal = propItem[2]
                    maxVal = propItem[3]
                    break

            if minVal == maxVal:
                shiftPropList.append({'pId': pId,
                 'pName': pName,
                 'pValue': pValue,
                 'barType': 'no'})
                continue
            remainingOffset = 100 - tipsPropProgressBarOffset
            if remainingOffset > 0 and maxVal != minVal:
                perOffset = (maxVal - minVal) / remainingOffset
            else:
                perOffset = 1
            curVal = i.props[idx][2]
            barValue = int((curVal - minVal) / perOffset + tipsPropProgressBarOffset)
            subBarValue = barValue
            shiftPropList.append({'pId': pId,
             'pName': pName,
             'pValue': pValue,
             'barType': 'white',
             'barValue': barValue,
             'subBarValue': subBarValue})

    else:
        for item in shiftBasicPropList:
            pName = toHtml(item[1], '#FFFFE5')
            pValue = toHtml(item[2], '#E4E4CD')
            shiftPropList.append({'pId': item[0],
             'pName': pName,
             'pValue': pValue,
             'barType': 'no'})


def addPrefixPropList(i, propList, shiftPropList, prefixPropList, shiftPrefixPropList):
    if len(prefixPropList) == 0:
        return
    for item in prefixPropList:
        pName = toHtml(item[1], '#73E539')
        pValue = toHtml(item[2], '#B3FB90')
        propList.append({'pId': item[0],
         'pName': pName,
         'pValue': pValue})

    for item in shiftPrefixPropList:
        pName = toHtml(item[1], '#73E539')
        pValue = toHtml(item[2], '#B3FB90')
        shiftPropList.append({'pId': item[0],
         'pName': pName,
         'pValue': pValue,
         'barType': 'no'})


def addFixedPropList(i, propList, shiftPropList, fixedPropList, shiftFixedPropList):
    if len(fixedPropList) == 0:
        return
    for item in fixedPropList:
        pName = toHtml(item[1], '#0088CC')
        pValue = toHtml(item[2], '#73D0FF')
        propList.append({'pId': item[0],
         'pName': pName,
         'pValue': pValue})

    for item in shiftFixedPropList:
        pName = toHtml(item[1], '#0088CC')
        pValue = toHtml(item[2], '#73D0FF')
        shiftPropList.append({'pId': item[0],
         'pName': pName,
         'pValue': pValue,
         'barType': 'no'})


def checkPropPoolMeet(pools, shiftRandPropList):
    propLen = len(shiftRandPropList)
    if propLen != sum((x[1] for x in pools)):
        return False
    poolList = []
    for pool in pools:
        poolList.extend([pool[0]] * pool[1])

    for item in shiftRandPropList:
        pId = item[0]
        idx = item[3]
        poolId = poolList[idx]
        eppooldData = EPPOOLD.data.get(poolId, [])
        isFind = False
        for ei in eppooldData:
            val = ei.get('value')
            if not val or val[0] != pId:
                continue
            isFind = True

        if not isFind:
            return False

    return True


def addRandPropList(i, propList, shiftPropList, randPropList, shiftRandPropList):
    if len(randPropList) == 0:
        return
    for item in randPropList:
        pName = toHtml(item[1], '#0088CC')
        pValue = toHtml(item[2], '#73D0FF')
        propList.append({'pId': item[0],
         'pName': pName,
         'pValue': pValue})

    tipsPropProgressBarOffset = SCD.data.get('tipsPropProgressBarOffset', 0)
    if not hasattr(i, 'rprops'):
        return
    propLen = len(i.rprops)
    if propLen != len(shiftRandPropList):
        return
    if i.isManualEquip():
        if not hasattr(i, 'makeType'):
            return
        extraPools = MEPD.data.get(i.id, {}).get('extraPools', [])
        if len(extraPools) <= i.makeType:
            return
        randPropId = extraPools[0]
    elif i.isExtendedEquip():
        randPropId = XEPD.data.get(i.id, {}).get('extraPools', 0)
    else:
        randPropId = ED.data.get(i.id, {}).get('randPropId', 0)
    curPools = []
    poolData = ERPD.data.get((randPropId, getattr(i, 'quality', 1)), [])
    for pd in poolData:
        pools = pd.get('pool', [])
        if checkPropPoolMeet(pools, shiftRandPropList):
            curPools = pools
            break

    poolList = []
    for pool in curPools:
        poolList.extend([pool[0]] * pool[1])

    if not poolList or len(poolList) != len(shiftRandPropList):
        return
    for item in shiftRandPropList:
        pId = item[0]
        idx = item[3]
        if idx >= propLen or i.rprops[idx][0] != pId:
            continue
        pName = toHtml(item[1], '#0088CC')
        pValue = toHtml(item[2], '#73D0FF')
        poolId = poolList[idx]
        eppooldData = EPPOOLD.data.get(poolId, [])
        minVal = 0
        maxVal = 0
        showBar = True
        for ei in eppooldData:
            val = ei.get('value')
            if not val or val[0] != pId:
                continue
            aid, atype, transType, amax, amin, pmin, pmax = val
            if transType != gametypes.PROPERTY_RAND_ABS:
                if pmin == pmax:
                    showBar = False
                    break
                formula = FMD.data.get(transType).get('formula')
                if not formula:
                    continue
                amin = i.evalValue(transType, pmin)
                amax = i.evalValue(transType, pmax)
            elif amin == amax:
                showBar = False
                break
            minVal = amin
            maxVal = amax
            break

        if showBar:
            remainingOffset = 100 - tipsPropProgressBarOffset
            curVal = i.rprops[idx][2]
            if remainingOffset > 0 and maxVal != minVal:
                perOffset = (maxVal - minVal) / remainingOffset
                barValue = int((curVal - minVal) / perOffset + tipsPropProgressBarOffset)
            else:
                barValue = 100
            subBarValue = barValue
            shiftPropList.append({'pId': pId,
             'pName': pName,
             'pValue': pValue,
             'barType': 'blue',
             'barValue': barValue,
             'subBarValue': subBarValue})
        else:
            shiftPropList.append({'pId': item[0],
             'pName': pName,
             'pValue': pValue,
             'barType': 'no'})
