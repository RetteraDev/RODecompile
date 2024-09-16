#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/tipUtils.o
from gamestrings import gameStrings
import time
import BigWorld
from Scaleform import GfxValue
import const
import gameglobal
import itemToolTipUtils
import uiUtils
import uiConst
import gametypes
import commGuild
import commcalc
import hotkey
import utils
import descUtils
from operator import itemgetter
from item import Item
from ui import gbk2unicode, unicode2gbk
from helpers.guild import getGTSD
from asObject import TipManager
from guis import compositeShopHelpFunc
from guis.asObject import ASObject
import hotkey as HK
from data import use_item_wish_data as UIWD
from data import conditional_prop_data as CPD
from data import consumable_item_data as CID
from data import equip_data as ED
from data import item_data as ID
from data import fame_data as FD
from data import junjie_config_data as JJCD
from data import jingjie_data as JJD
from data import sys_config_data as SCD
from cdata import font_config_data as FCD
from data import qing_gong_skill_data as QGSD
from cdata import composite_shop_trade_data as CSTD
from data import mingpai_data as MPD
from data import juewei_data as JD
from data import school_data as SD
from data import qiren_clue_data as QCD
from data import qiren_role_data as QRD
from data import state_data as STD
from data import summon_sprite_data as SSD
from data import bonus_set_data as BSD
from data import bonus_box_data as BBD
from data import bonus_data as BD
from data import box_bonus_map_data as BBMD
from data import wing_world_config_data as WWCD
from data import treasure_box_data as TBD
from data import new_server_activity_data as NSAD
from cdata import xiuwei_bonus_level_data as XBLD
from compositeShopProxy import CompositeShopProxy
TYPE_ITEM = 1
TYPE_TASK = 2
TYPE_ACHIEVEMENT = 3
TYPE_TITLE = 4
TYPE_DEFAULT_BLACK = 5
TYPE_DEFAULT_WHITE = 6
TYPE_SKILL = 7
TYPE_WS_SKILL = 8
TYPE_SKILL_COMPARE = 9
TYPE_WS_SKILL_COMPARE = 10
TYPE_SKILL_NEXT = 11
TYPE_WS_SKILL_NEXT = 12
TYPE_VP = 13
TYPE_QINGGONG = 14
TYPE_SKILL_ENHANCE = 15
TYPE_SOCIAL_JOB = 16
TYPE_GUILD_RESIDENT_SKILL = 17
TYPE_MALL_VIP = 18
TYPE_GUILD_REPAIR_FEE = 19
TYPE_SKILL_GUIDE = 20
TYPE_INTERACTIVE_OBJ_REWARD = 23
TYPE_BUFF = 24
TYPE_QUEST_TRACK_GUILD_AWARD = 25
TYPE_ARENA_PLAYOFFS_BET_TOP4 = 26
TYPE_ARENA_PLAYOFFS_BET_DAY = 27
TYPE_EQUIP_SOUL_POOL = 28
TYPE_EQUIP_SOUL_STONE = 29
TYPE_SPRITE_HEAD_TIP = 32
TYPE_CARD_TIP = 33
TYPE_SPRITE_DETAIL_TIP = 34
TYPE_SPRITE_SIMPLE_TIP = 35
TYPE_CARD_SUIT_TIP = 36
TYPE_ZMJ_SPRITE_SIMPLE_TIP = 37
currentTipInfo = None

def onGetItemTipByInfo(*args):
    gfxLocation = args[3][0].GetMember('location')
    gfxUUID = args[3][0].GetMember('uuid')
    gfxItemId = args[3][0].GetMember('itemId')
    if gfxUUID:
        uuid = unicode2gbk(gfxUUID.GetString(), gfxUUID.GetString()).decode('hex')
    else:
        uuid = ''
    if gfxLocation:
        location = int(gfxLocation.GetNumber())
    else:
        location = const.ITEM_IN_NONE
    if gfxItemId:
        itemId = gfxItemId.GetNumber()
    else:
        itemId = 0
    if location and uuid:
        return getItemTipByUUID(uuid, location)
    if location and itemId:
        return getItemTipById(itemId, location)


def getItemTipById(itemId, location = const.ITEM_IN_NONE):
    p = BigWorld.player()
    if location == const.ITEM_IN_BAG:
        srcPage, srcPos = p.inv.findItemInPages(itemId, enableParentCheck=False, includeExpired=True, includeLatch=True, includeShihun=True)
        if srcPage >= 0 and srcPos >= 0:
            it = p.inv.getQuickVal(srcPage, srcPos)
        else:
            it = Item(itemId)
    else:
        it = Item(itemId)
    return _getItemTip(it, location)


def getItemTipByLocation(it, location = const.ITEM_IN_BAG):
    return _getItemTip(it, location)


def getItemTipByUUID(uuid, location = const.ITEM_IN_NONE):
    p = BigWorld.player()
    it = None
    if location == const.ITEM_IN_BAG:
        it, _, _ = p.inv.findItemByUUID(uuid)
    elif location == const.ITEM_IN_CROSS_BAG:
        it, _, _ = p.crossInv.findItemByUUID(uuid)
    elif location == const.ITEM_IN_CONSIGN_HISTORY:
        for item in getattr(p, 'consignTradeHistory', []):
            if item[3].uuid == uuid:
                it = item[3]
                break

    elif location == const.ITEM_IN_GUILDSTORAGE:
        it, _, _ = p.guild.storage.findItemByUUID(uuid)
    elif location == const.ITEM_IN_EQUIPMENT:
        for item in getattr(p, 'equipment', []):
            if not item:
                continue
            if item.uuid == uuid:
                it = item
                break

        if not it:
            for pos in gametypes.EQU_PART_SUB:
                item = commcalc.getAlternativeEquip(p, pos)
                if not item:
                    continue
                if item.uuid == uuid:
                    it = item
                    break

    elif location == const.ITEM_IN_RUNEBOARD:
        runeEquip = BigWorld.player().runeBoard.runeEquip
        if runeEquip:
            if runeEquip.uuid == uuid:
                it = runeEquip
            if not it:
                for runeDataVal in runeEquip.runeData:
                    if not runeDataVal.item:
                        continue
                    if runeDataVal.item.uuid == uuid:
                        it = runeDataVal.item
                        break

    elif location == const.ITEM_IN_HIEROGRAM:
        if p.hierogramDict:
            hieroEquipItem = p.hierogramDict.get('hieroEquip', None)
            if hieroEquipItem:
                if hieroEquipItem.uuid == uuid:
                    it = hieroEquipItem
            if not it:
                hieroCrystals = p.hierogramDict.get('hieroCrystals', {})
                for hType, hPart in hieroCrystals:
                    if hieroCrystals[hType, hPart].uuid == uuid:
                        it = hieroCrystals[hType, hPart]
                        break

    elif location == const.ITEM_IN_BUSINESS_BAG:
        it, _, _ = p.zaijuBag.findItemByUUID(uuid)
    elif location == const.ITEM_MANUAL_EQUIP:
        fromItem, _, _ = p.inv.findItemByUUID(uuid)
        it = fromItem.getItemAfterIdentify()
        it.unbindTimes = getattr(it, 'unbindTimes', 0) + 1
        if it:
            return _getItemTip(it, const.ITEM_IN_BAG)
    elif location == const.ITEM_IN_BIND_TRADE:
        it = gameglobal.rds.ui.bindItemTrade.findItemByUUID(uuid)
    elif location == const.ITEM_IN_METERIAL_BAG:
        if gameglobal.rds.ui.meterialBag.page < len(p.materialBag.pages):
            pageCnt = len(p.materialBag.pages[gameglobal.rds.ui.meterialBag.page])
            for ps in xrange(pageCnt):
                item = p.materialBag.getQuickVal(gameglobal.rds.ui.meterialBag.page, ps)
                if item and item.uuid == uuid:
                    it = item
                    break

    elif location == const.ITEM_IN_CROSS_CONSIGN_HISTORY:
        itemDic = gameglobal.rds.ui.tabAuctionCrossServer.historyInfoCache
        for k, v in itemDic.iteritems():
            if v.get('item', None) and v.get('item', None).uuid == uuid:
                it = v.get('item', None)
                break

    elif location == const.ITEM_IN_HOME_STORAGE:
        it, _, _ = gameglobal.rds.ui.homeTermsStorage.findItemByUUID(uuid)
    elif location == const.ITEM_IN_FASHION_BAG:
        it, _, _ = p.fashionBag.findItemByUUID(uuid)
    elif location == const.ITEM_IN_HIEROGRAM_BAG:
        it, _, _ = p.hierogramBag.findItemByUUID(uuid)
    elif location == const.ITEM_IN_REFINING:
        it = gameglobal.rds.ui.equipChangeRefining.resetItem
    if it:
        return _getItemTip(it, location)
    else:
        return


def getItemTipByPagePos(page, pos, location = const.ITEM_IN_NONE):
    p = BigWorld.player()
    it = None
    if location == const.ITEM_IN_BAG:
        it = p.inv.getQuickVal(page, pos)
    elif location == const.ITEM_IN_EQUIPMENT:
        it = p.equipment.get(pos)
    elif location == const.ITEM_IN_SPRITE_MATERIAL_BAG:
        it = p.spriteMaterialBag.getQuickVal(page, pos)
    return _getItemTip(it, location)


def _getItemTip(item, location = const.ITEM_IN_NONE):
    if not item:
        return
    else:
        ret = []
        if item.type == Item.BASETYPE_CONSUMABLE and hasattr(item, 'cstype'):
            if item.cstype == Item.SUBTYPE_2_SKILL_BOOK:
                skillId = CID.data.get(item.id, {}).get('learnSkillId', -1)
                if skillId == -1:
                    if gameglobal.rds.ui.skill.isQingGong(item.name):
                        idx = gameglobal.rds.ui.skill.getQingGongIdxByName(item.name)
                        return gameglobal.rds.ui.skill.formQingGongTip(idx)
                    else:
                        return GfxValue('')
                else:
                    ret.append(formatRet(item, location))
                    ret.append(gameglobal.rds.ui.skill.formatTooltip(skillId))
                    return uiUtils.array2GfxAarry(ret, True)
            elif item.cstype == Item.SUBTYPE_2_SKILL_ENHANCE:
                skillId = CID.data.get(item.id, {}).get('enhanceSkillId', -1)
                enhId = CID.data.get(item.id, {}).get('enhanceSkillPart', -1)
                if skillId < 0 or enhId < 0:
                    ret.append(formatRet(item, location))
                    return uiUtils.array2GfxAarry(ret, True)
                else:
                    ret.append(formatRet(item, location))
                    ret.append(gameglobal.rds.ui.skill.getSkillEnhanceTipBySkillId(skillId, enhId))
                    return uiUtils.array2GfxAarry(ret, True)
            else:
                if item.cstype == Item.SUBTYPE_2_ITEM_BOX:
                    ret.append(formatRet(item, location))
                    if gameglobal.rds.configData.get('enableItemBoxRewardShow'):
                        cidData = CID.data.get(item.id, {})
                        showMustObtain = cidData.get('showMustObtain', 0)
                        showPossibleObtain = cidData.get('showPossibleObtain', 0)
                        if showMustObtain == 1 or showPossibleObtain == 1:
                            mustObtainIdList = []
                            possibleObtainIdList = []
                            _getItemBoxRewardList(cidData, item.id, mustObtainIdList, possibleObtainIdList)
                            if showMustObtain == 1 and mustObtainIdList:
                                mustObtainInfoList = {}
                                for itemId, _, _ in mustObtainIdList:
                                    if itemId != 0:
                                        mustObtainInfoList[itemId] = uiUtils.getGfxItemById(itemId, 0)

                                ret[0]['mustObtainList'] = mustObtainInfoList.values()
                            if showPossibleObtain == 1 and possibleObtainIdList:
                                possibleObtainIdList = sorted(possibleObtainIdList, key=itemgetter(1))
                                possibleObtainInfoList = {}
                                for itemId, _, _ in possibleObtainIdList:
                                    if itemId != 0:
                                        possibleObtainInfoList[itemId] = uiUtils.getGfxItemById(itemId, 0)

                                ret[0]['possibleObtainList'] = possibleObtainInfoList.values()
                    return uiUtils.array2GfxAarry(ret, True)
                if item.cstype == Item.SUBTYPE_2_CARD:
                    cData = CID.data.get(item.id, {})
                    cardId = cData.get('cardId', 0)
                    useType = cData.get('param', 0)
                    tipData = None
                    if useType == const.CARD_ITEM_BEHAVIOR_LV_TO_TOP:
                        tipData = gameglobal.rds.ui.cardSystem.getCardTipData(cardId, oriData=True, fullLv=True)
                    else:
                        tipData = gameglobal.rds.ui.cardSystem.getCardTipData(cardId, oriData=True)
                    if tipData:
                        ret.append(formatRet(item, location))
                        ret.append(tipData)
                        return uiUtils.array2GfxAarry(ret, True)
        if item.type == Item.BASETYPE_EQUIP and location != const.ITEM_IN_EQUIPMENT:
            iEd = ED.data[item.id]
            ret.append(formatRet(item, location))
            if not item.isYaoPei():
                contrastScore = ret[0].get('score', '')
            else:
                contrastScore = ret[0].get('yaoPeiScore', '')
            p = BigWorld.player()
            if hasattr(p, 'equipment') and not Item.isDotaBattleFieldItem(item.id):
                for idNum in xrange(len(BigWorld.player().equipment)):
                    relativeItem = BigWorld.player().equipment.get(idNum)
                    if relativeItem != None:
                        relativeItemEd = ED.data.get(relativeItem.id, {})
                        if relativeItemEd:
                            if iEd['equipType'] == relativeItemEd['equipType']:
                                if relativeItemEd['equipType'] == Item.EQUIP_BASETYPE_ARMOR:
                                    if relativeItemEd['armorSType'] != iEd['armorSType']:
                                        continue
                                elif relativeItemEd['equipType'] == Item.EQUIP_BASETYPE_WEAPON:
                                    if relativeItemEd['weaponSType'] != iEd['weaponSType']:
                                        continue
                                elif relativeItemEd['equipType'] == Item.EQUIP_BASETYPE_JEWELRY:
                                    if relativeItemEd['jewelSType'] != iEd['jewelSType']:
                                        continue
                                elif relativeItemEd['equipType'] == Item.EQUIP_BASETYPE_FASHION:
                                    if relativeItemEd['fashionSType'] != iEd['fashionSType']:
                                        continue
                                retItem = formatRet(relativeItem, const.ITEM_IN_EQUIPMENT, True)
                                retItem['contrastScore'] = contrastScore
                                ret.append(retItem)

            return uiUtils.array2GfxAarry(ret, True)
        if item.type == Item.BASETYPE_RUNE_EQUIP:
            ret.append(formatRet(item, location))
            if BigWorld.player().runeBoard.runeEquip and item != BigWorld.player().runeBoard.runeEquip:
                ret.append(formatRet(BigWorld.player().runeBoard.runeEquip, const.ITEM_IN_RUNEBOARD, True))
            return uiUtils.array2GfxAarry(ret, True)
        if item.type == Item.BASETYPE_LIFE_SKILL:
            ret.append(formatRet(item, location))
            if item.isFishingEquip():
                part = item.whereEquipFishing()
                relativeItem = BigWorld.player().fishingEquip[part]
                if relativeItem and item != relativeItem:
                    ret.append(formatRet(relativeItem, const.ITEM_IN_LIFE_SKILL_EQUIP, True))
            if item.isExploreEquip():
                part = item.whereEquipExplore()
                relativeItem = BigWorld.player().exploreEquip[part]
                if relativeItem and item != relativeItem:
                    ret.append(formatRet(relativeItem, const.ITEM_IN_LIFE_SKILL_EQUIP, True))
            return uiUtils.array2GfxAarry(ret, True)
        ret.append(formatRet(item, location))
        return uiUtils.array2GfxAarry(ret, True)


def formatRet(i, location = const.ITEM_IN_NONE, bRelative = False):
    p = BigWorld.player()
    if p.__class__.__name__ == 'PlayerAccount':
        p = gameglobal.rds.loginScene.player
    inRepair = gameglobal.rds.ui.shop.inRepair
    isPublishedVersion = BigWorld.isPublishedVersion()
    inHeaderAssignMode = p.isInTeamOrGroup() and p.groupAssignWay == const.GROUP_ASSIGN_HEADER
    pos = gameglobal.rds.ui.assign.selectPos
    if pos != None:
        if pos < len(gameglobal.rds.ui.assign.assignTarget):
            assignTarget = gameglobal.rds.ui.assign.assignTarget[pos]
        else:
            assignTarget = None
    else:
        assignTarget = None
    isInBag = location in (const.ITEM_IN_BAG,
     const.ITEM_IN_EQUIPMENT,
     const.ITEM_IN_GUILDSTORAGE,
     const.ITEM_IN_RUNEBOARD,
     const.ITEM_IN_TARGET_ROLE,
     const.ITEM_IN_BLARENA_TEMPLATE,
     const.ITEM_IN_METERIAL_BAG,
     const.ITEM_IN_HIEROGRAM,
     const.ITEM_IN_CROSS_CONSIGN_HISTORY,
     const.ITEM_IN_HOME_STORAGE,
     const.ITEM_IN_SPRITE_MATERIAL_BAG,
     const.ITEM_IN_WARDROBE,
     const.ITEM_IN_REFINING)
    isInChat = location == const.ITEM_IN_CHAT
    isInBooth = location in (const.ITEM_IN_BOOTH_BUY, const.ITEM_IN_BOOTH_SELL)
    isCompositeShop = location == const.ITEM_IN_COMPOSITESHOP
    page = uiConst.BOOTH_SLOTS_SELL
    if location == const.ITEM_IN_BOOTH_BUY:
        page = uiConst.BOOTH_SLOTS_BUY
    if location == const.ITEM_IN_COMPOSITESHOP:
        extraData = _getCompositeShopItemExtraData(i)
    else:
        extraData = None
    ret = itemToolTipUtils.formatRet(p, i, bRelative, isInBag, isInChat, isInBooth, page, isCompositeShop, extraData, inRepair, isPublishedVersion, inHeaderAssignMode, assignTarget, location)
    ret['itemSourceKey'] = '' if Item.isDotaBattleFieldItem(i.id) else _getItemSourceShortKey()
    return ret


def _getItemSourceShortKey():
    if gameglobal.rds.configData.get('enableNewItemSearch', False):
        detial = HK.HKM[hotkey.KEY_ITEM_SOURCE]
        return detial.getBrief()
    else:
        return ''


def _getCompositeShopItemExtraData(shopItem):
    if not shopItem:
        return
    compositeId = shopItem.compositeId
    if not CSTD.data.has_key(compositeId):
        return ''
    compositeData = CSTD.data.get(compositeId, {})
    res = ''
    if compositeData:
        if compositeData.has_key('lvLimit'):
            lvLimit = compositeData['lvLimit']
            res += gameStrings.TEXT_TIPUTILS_447
            res += gameStrings.TEXT_TIPUTILS_448
            res += gameStrings.TEXT_TIPUTILS_449
            if lvLimit[0] == -1:
                res += gameStrings.TEXT_TIPUTILS_451 % lvLimit[1]
            elif lvLimit[1] == -1:
                res += gameStrings.TEXT_TIPUTILS_453 % lvLimit[0]
            else:
                res += gameStrings.TEXT_TIPUTILS_455 % (lvLimit[0], lvLimit[1])
        if compositeData.has_key('sexLimit'):
            sexLimit = compositeData['sexLimit']
            desc = const.SEX_NAME[sexLimit]
            res += gameStrings.TEXT_TIPUTILS_447
            res += gameStrings.TEXT_TIPUTILS_461 % (desc,)
        if compositeData.has_key('arenaScoreLimit'):
            arenaScoreLimit = compositeData['arenaScoreLimit']
            res += gameStrings.TEXT_TIPUTILS_447
            res += gameStrings.TEXT_TIPUTILS_466
            res += gameStrings.TEXT_TIPUTILS_467
            res += "<font color = \'#ffff32\'>%d</font>\n" % (arenaScoreLimit,)
        if compositeData.has_key('delegationRank'):
            maoxianFameLv = compositeData['delegationRank']
            maoxianFameName = FD.data.get(const.FAME_TYPE_ORG, {}).get('lvDesc')[maoxianFameLv]
            res += gameStrings.TEXT_TIPUTILS_447
            res += gameStrings.TEXT_TIPUTILS_474
            res += gameStrings.TEXT_TIPUTILS_467
            res += "<font color = \'#ffff32\'>%s</font>\n" % (maoxianFameName,)
        if compositeData.has_key('qumoLimit'):
            qumoLimit = compositeData['qumoLimit']
            res += gameStrings.TEXT_TIPUTILS_447
            res += gameStrings.TEXT_TIPUTILS_481
            res += gameStrings.TEXT_TIPUTILS_467
            res += gameStrings.TEXT_TIPUTILS_483 % (qumoLimit,)
        if compositeData.has_key('shopJingJieRequire'):
            jingJieLimit = compositeData['shopJingJieRequire']
            jingJieName = JJD.data.get(jingJieLimit, {}).get('name', gameStrings.TEXT_COMPOSITESHOPHELPFUNC_324)
            res += gameStrings.TEXT_TIPUTILS_447
            res += gameStrings.TEXT_TIPUTILS_489
            res += gameStrings.TEXT_TIPUTILS_467
            res += "<font color = \'#ffff32\'>%s</font>\n" % (jingJieName,)
        if compositeData.has_key('needJunJieLv'):
            junJieLvLimit = compositeData['needJunJieLv']
            junJieName = JJCD.data.get(junJieLvLimit, {}).get('name', gameStrings.TEXT_COMPOSITESHOPHELPFUNC_324)
            res += gameStrings.TEXT_TIPUTILS_447
            res += gameStrings.TEXT_TIPUTILS_497
            res += gameStrings.TEXT_TIPUTILS_467
            res += "<font color = \'#ffff32\'>%s</font>\n" % (junJieName,)
        if compositeData.has_key('needJueWeiLv'):
            jueweiLimit = compositeData['needJueWeiLv']
            jueweiName = JD.data.get(jueweiLimit, {}).get('name', gameStrings.TEXT_COMPOSITESHOPHELPFUNC_324)
            res += gameStrings.TEXT_TIPUTILS_447
            res += gameStrings.TEXT_TIPUTILS_505
            res += gameStrings.TEXT_TIPUTILS_467
            res += "<font color = \'#ffff32\'>%s</font>\n" % (jueweiName,)
        if compositeData.has_key('schoolLimit'):
            schLimit = compositeData['schoolLimit']
            schoolNames = ''
            for school in schLimit:
                schoolNames += SD.data.get(school, {}).get('name', gameStrings.TEXT_GAME_1747) + ' '

            res += gameStrings.TEXT_TIPUTILS_514
            res += gameStrings.TEXT_TIPUTILS_515
            res += "<font color = \'#ffff32\'>%s</font>\n" % (schoolNames,)
        if compositeData.has_key('needClue'):
            needClue = compositeData['needClue']
            roleId = QCD.data.get(needClue[0], {}).get('pushRoleId')
            role = QRD.data.get(roleId, {}).get('name', '')
            res += gameStrings.TEXT_TIPUTILS_447
            res += gameStrings.TEXT_TIPUTILS_523
            res += "<font color = \'#ffff32\'>%s</font>\n" % (role,)
        elif compositeData.has_key('fameLimit'):
            option = gameglobal.rds.ui.compositeShop.option
            fameLimit = compositeData['fameLimit']
            p = BigWorld.player()
            for fameId, fameNum in fameLimit:
                fd = FD.data.get(fameId, {})
                if not fd or fd.has_key('lvDesc'):
                    continue
                fameLv, _ = compositeShopHelpFunc._getFameLv(fameId, fameNum)
                schoolFame = fd.get('schoolFame', 0)
                if option != CompositeShopProxy.OPTION_SHOP_BUY_BACK:
                    fameName = fd.get('shopTips', '')
                    fameLvName = SCD.data.get('fameLvName', {}).get(fameLv, '')
                else:
                    fameName = fd.get('name', '')
                    fameLvName = SCD.data.get('fameLvNameModify', {}).get(fameLv, '')
                if schoolFame:
                    if schoolFame == p.school:
                        fameLvName = SCD.data.get('selfSchoolFameLvName', {}).get(schoolFame, {}).get(fameLv, '')
                    else:
                        fameLvName = SCD.data.get('otherSchoolFameLvName', {}).get(schoolFame, {}).get(fameLv, '')
                showFameLimitVal = compositeData.get('showFameLimitVal', 0)
                if showFameLimitVal:
                    fameLvName = str(fameNum)
                    fameName = fd.get('name', '')
                if fameLvName == '':
                    continue
                res += gameStrings.TEXT_TIPUTILS_447
                res += "<font color = \'#ffff32\'>%s </font>" % (fameName,)
                res += gameStrings.TEXT_TIPUTILS_467
                res += "<font color = \'#ffff32\'>%s</font>\n" % (fameLvName,)

        if compositeData.has_key('consumeCash'):
            consumeCash = compositeData['consumeCash']
            cashType = compositeData['cashType']
            desc = ''
            if cashType == gametypes.CONSUME_CASH_TYPE_NO_LIMIT:
                desc = gameStrings.TEXT_INVENTORYPROXY_3297
            elif cashType == gametypes.CONSUME_CASH_TYPE_BIND_CASH:
                desc = gameStrings.TEXT_INVENTORYPROXY_3297
            elif cashType == gametypes.CONSUME_CASH_TYPE_CASH:
                desc = gameStrings.TEXT_INVENTORYPROXY_3296
            res += gameStrings.TEXT_TIPUTILS_574
            res += "<font color = \'#ffff32\'>%s </font>" % (desc,)
            res += "<font color = \'#ffffff\'>%d</font>\n" % (consumeCash,)
        if compositeData.has_key('consumeFame'):
            consumeFame = compositeData['consumeFame']
            for fameId, fameNum in consumeFame:
                fd = FD.data.get(fameId)
                if not fd:
                    continue
                fameName = fd['name']
                res += gameStrings.TEXT_TIPUTILS_574
                res += "<font color = \'#ffff32\'>%s </font>" % (fameName,)
                res += gameStrings.TEXT_TIPUTILS_588 % (fameNum,)

        if compositeData.has_key('consumeItem'):
            consumeItem = compositeData['consumeItem']
            for itemId, itemNum in consumeItem:
                d = ID.data.get(itemId)
                if not d:
                    continue
                itemName = d['name']
                res += gameStrings.TEXT_TIPUTILS_574
                res += "<font color = \'#ffff32\'>%s </font>" % (itemName,)
                res += gameStrings.TEXT_TIPUTILS_600 % (itemNum,)

        if compositeData.has_key('consumeExp'):
            consumeExp = compositeData['consumeExp']
            res += gameStrings.TEXT_TIPUTILS_574
            res += gameStrings.TEXT_TIPUTILS_605
            res += gameStrings.TEXT_TIPUTILS_588 % (consumeExp,)
        if compositeData.has_key('consumeContrib'):
            consumeContrib = compositeData['consumeContrib']
            res += gameStrings.TEXT_TIPUTILS_574
            res += gameStrings.TEXT_TIPUTILS_611
            res += gameStrings.TEXT_TIPUTILS_588 % (consumeContrib,)
    if compositeData.has_key('diJiaItemid'):
        diJiaItemid = compositeData['diJiaItemid']
        d = ID.data.get(diJiaItemid)
        itemName = d['name']
        itemQuality = d.get('quality', 1)
        fontColor = FCD.data['item', itemQuality]['color']
        res += gameStrings.TEXT_TIPUTILS_623
        res += "<font color = \'%s\'>%s</font>" % (fontColor, itemName)
        res += gameStrings.TEXT_TIPUTILS_625
        diJiaFame = compositeData.get('diJiaFame', [])
        for i, fameInfo in enumerate(diJiaFame):
            if i != 0:
                res += gameStrings.TEXT_TIPUTILS_630
            fameId, fameNum = fameInfo
            fd = FD.data.get(fameId)
            if not fd:
                continue
            fameName = fd['name']
            res += "<font color = \'#ffff32\'>%s</font>" % (fameName,)
            res += "<font color = \'#41d95a\'>%d</font>" % (fameNum,)
            res += gameStrings.TEXT_TIPUTILS_640

        diJiaItemMaxNum = compositeData.get('diJiaItemMaxNum', 1)
        res += gameStrings.TEXT_TIPUTILS_643
        res += "<font color = \'#41d95a\'>%d</font>" % (diJiaItemMaxNum,)
        res += gameStrings.TEXT_TIPUTILS_645
    return res


def _getFameLvCondition(fameId, fameVal):
    fd = FD.data.get(fameId)
    ret = 1
    if fd.has_key('lvUpCondition'):
        lvUpCondition = fd.get('lvUpCondition', [])
        if lvUpCondition:
            lvArray = lvUpCondition[1].items()
        else:
            lvArray = []
    else:
        lvArray = fd.get('lvUpNeed', {}).items()
    lvArray.sort(key=lambda k: k[1], reverse=True)
    for key, val in lvArray:
        if fameVal >= val:
            ret = key + 1
            break

    return ret


def onGetTipDataByType(*args):
    global currentTipInfo
    currentTipInfo = None
    tipType = int(args[3][0].GetNumber())
    if tipType == TYPE_VP:
        return getVpTip()
    elif tipType == TYPE_QINGGONG:
        arr = uiUtils.gfxArray2Array(args[3][1])
        skillId = int(arr[0].GetNumber())
        isNext = arr[1].GetBool()
        return getQingGongTip(skillId, isNext)
    elif tipType == TYPE_SKILL_ENHANCE:
        arg = args[3][1]
        extraInfo = {}
        if arg.IsString():
            part = int(args[3][1].GetString())
        else:
            part = int(arg.GetMember('part').GetNumber())
            extraInfo = ASObject(arg.GetMember('extraInfo'))
        return uiUtils.dict2GfxDict(gameglobal.rds.ui.skill.getSkillEnhanceTip(part, extraInfo), True)
    elif tipType == TYPE_GUILD_REPAIR_FEE:
        return getRepairFeeInfo()
    else:
        if tipType == TYPE_SKILL or tipType == TYPE_WS_SKILL:
            arg = args[3][1]
            isPSkill = False
            extraInfo = {}
            try:
                if arg.IsNumber():
                    skillId = int(args[3][1].GetNumber())
                    lv = 0
                else:
                    skillId = int(arg.GetMember('skillId').GetNumber())
                    lv = int(arg.GetMember('lv').GetNumber())
                    if arg.GetMember('isPSkill') and arg.GetMember('isPSkill').IsBool():
                        isPSkill = arg.GetMember('isPSkill').GetBool()
                    extraInfo = ASObject(arg.GetMember('extraInfo'))
            except:
                skillId = 0
                lv = 0

            if skillId:
                if isPSkill:
                    return gameglobal.rds.ui.skill.formatPSkillTooltip(skillId, sLv=lv)
                elif extraInfo:
                    return gameglobal.rds.ui.skill.formatTooltip(skillId, sLv=lv, extraInfo=extraInfo)
                else:
                    return gameglobal.rds.ui.skill.formatTooltip(skillId, sLv=lv)
        elif tipType == TYPE_SKILL_GUIDE:
            if gameglobal.rds.ui.skillGuide.mediator:
                part = int(args[3][1].GetNumber())
                skillId = gameglobal.rds.ui.skillGuide.currentSkillId
                return uiUtils.dict2GfxDict(gameglobal.rds.ui.skill.getSkillEnhanceTipBySkillId(skillId, part), True)
        elif tipType == TYPE_INTERACTIVE_OBJ_REWARD:
            if gameglobal.rds.ui.interactiveObj.rewardMediator:
                idx = int(args[3][1].GetNumber())
                return uiUtils.dict2GfxDict(gameglobal.rds.ui.interactiveObj.getRewardTip(idx), True)
        elif tipType == TYPE_BUFF:
            buffId = int(args[3][1].GetNumber())
            buffPropIds = STD.data.get(buffId, {}).get('buffPropIds')
            if buffPropIds:
                currentTipInfo = {'tipId': int(args[3][2].GetNumber()),
                 'buffPropIds': buffPropIds,
                 'buffId': buffId,
                 'buffPropValueDict': {},
                 'tipType': tipType}
                for propId in set(buffPropIds):
                    BigWorld.player().cell.queryBufferTipsProperty(propId)

            else:
                return GfxValue(gbk2unicode(getBuffTip(buffId)))
        else:
            if tipType == TYPE_QUEST_TRACK_GUILD_AWARD:
                questId = int(args[3][1].GetNumber())
                return getQuestTrackGuildAwardInfo(questId)
            if tipType == TYPE_ARENA_PLAYOFFS_BET_TOP4:
                arr = uiUtils.gfxArray2Array(args[3][1])
                lvKey = arr[0].GetString()
                bType = int(arr[1].GetNumber())
                betId = int(arr[2].GetNumber())
                idx = int(arr[3].GetNumber())
                return gameglobal.rds.ui.arenaPlayoffsBetMyself.getTop4Tip(lvKey, bType, betId, idx)
            if tipType == TYPE_ARENA_PLAYOFFS_BET_DAY:
                arr = uiUtils.gfxArray2Array(args[3][1])
                lvKey = arr[0].GetString()
                bType = int(arr[1].GetNumber())
                betId = int(arr[2].GetNumber())
                idx = int(arr[3].GetNumber())
                return gameglobal.rds.ui.arenaPlayoffsBetMyself.getDayTip(lvKey, bType, betId, idx)
            if tipType == TYPE_EQUIP_SOUL_POOL:
                arr = uiUtils.gfxArray2Array(args[3][1])
                spid = int(arr[0].GetNumber())
                schreq = int(arr[1].GetNumber())
                return gameglobal.rds.ui.equipSoul.getPoolTip(spid, schreq)
            if tipType == TYPE_EQUIP_SOUL_STONE:
                arr = uiUtils.gfxArray2Array(args[3][1])
                spid = int(arr[0].GetNumber())
                schreq = int(arr[1].GetNumber())
                x = int(arr[2].GetNumber())
                y = int(arr[3].GetNumber())
                return gameglobal.rds.ui.equipSoul.getStoneTip(spid, schreq, x, y)
            if tipType == TYPE_SPRITE_HEAD_TIP or tipType == TYPE_SPRITE_SIMPLE_TIP:
                arr = uiUtils.gfxArray2Array(args[3][1])
                if arr[0].IsNumber():
                    spriteIndex = int(arr[0].GetNumber())
                    return gameglobal.rds.ui.summonedWarSpriteMine.getSpriteTipByIndex(spriteIndex)
                else:
                    spriteUUID = arr[0].GetString()
                    return gameglobal.rds.ui.ranking.getSpriteTipDataByUUID(spriteUUID)
            else:
                if tipType == TYPE_CARD_TIP:
                    arr = uiUtils.gfxArray2Array(args[3][1])
                    return gameglobal.rds.ui.cardSystem.getCardTipData(arr[0].GetNumber())
                if tipType == TYPE_CARD_SUIT_TIP:
                    arr = uiUtils.gfxArray2Array(args[3][1])
                    return gameglobal.rds.ui.ranking.getCardSuitTipData(arr[0].GetString())
                if tipType == TYPE_ZMJ_SPRITE_SIMPLE_TIP:
                    arr = uiUtils.gfxArray2Array(args[3][1])
                    return gameglobal.rds.ui.rankCommon.getZmjSpriteTipDataByGbId(int(arr[0].GetString()))
                if tipType == TYPE_SPRITE_DETAIL_TIP:
                    arr = uiUtils.gfxArray2Array(args[3][1])
                    if arr[0].IsNumber():
                        spriteIndex = int(arr[0].GetNumber())
                        return gameglobal.rds.ui.summonedWarSpriteMine.getSpriteDetailTipByIndex(spriteIndex)
                    else:
                        spriteUUID = arr[0].GetString()
                        return gameglobal.rds.ui.ranking.getSpriteDetailTipDataByUUID(spriteUUID)
        return


def getVpTip():
    p = BigWorld.player()
    expParam, transformRatio = p.getVpLvData()
    ret = {}
    vpStages = p.getAllVpStageAndExp()
    for stage, value in vpStages.iteritems():
        stageRange, expParam = value
        if isinstance(stageRange, tuple):
            stageRange = '%d-%d' % stageRange
        else:
            stageRange = str(stageRange)
        ret['vpStage' + str(stage)] = gameStrings.TEXT_TIPUTILS_822 % stageRange
        if expParam <= 1:
            ret['vpStage' + str(stage)] += gameStrings.TEXT_TIPUTILS_824
        else:
            ep = expParam - 1
            ret['vpStage' + str(stage)] += gameStrings.TEXT_TIPUTILS_827 % (ep, ep)

    return uiUtils.dict2GfxDict(ret, True)


def getQingGongTip(idx, isNext):
    p = BigWorld.player()
    ret = {}
    if idx == uiConst.QINGGONG_FLAG_BASIC:
        lv = 1
        qgData = QGSD.data.get((idx, 1), {})
    else:
        skVal = p.qingGongSkills.get(idx, None)
        lv = skVal.level if skVal else 1
        if skVal:
            lv = skVal.level
            qgData = QGSD.data.get((idx, lv), {})
        else:
            lv = 0
            qgData = QGSD.data.get((idx, 1), {})
    skillName = qgData.get('name', gameStrings.TEXT_GAME_1747)
    iconPath = 'misc/%s.dds' % str(qgData.get('icon', 'notFound'))
    costValue = qgData.get('consumeDesc1', '')
    conCostValue = qgData.get('consumeDesc2', '')
    desc = qgData.get('qinggongDesc', '') + '\n' + qgData.get('operDesc', '')
    ret['current'] = {'skillName': skillName,
     'lv': lv,
     'iconPath': iconPath,
     'costValue': costValue,
     'conCostValue': conCostValue,
     'desc': desc}
    if isNext:
        qgData = QGSD.data.get((idx, lv + 1), {})
        if not qgData:
            isNext = False
        itemName = ID.data.get(qgData.get('skillBookId', 0), {}).get('name', '')
        moeny = qgData.get('needCash', 0)
        exp = qgData.get('needExp', 0)
        desc = qgData.get('mainChangeDesc', '') + '\n' + qgData.get('detailChangeDesc', '')
        ret['next'] = {'skillName': skillName,
         'lv': lv + 1,
         'iconPath': iconPath,
         'itemName': itemName,
         'moeny': moeny,
         'exp': exp,
         'desc': desc}
    ret['isNext'] = isNext
    return uiUtils.dict2GfxDict(ret, True)


def getRepairFeeInfo():
    guild = BigWorld.player().guild
    info = {}
    baseMojing, baseXirang, baseWood, baseBindCash = guild._getBaseMaintainFee()
    info['baseCash'] = format(baseBindCash, ',')
    buildingMojing, buildingXirang, buildingWood, buildingBindCash = guild._getBuildingMaintainFee()
    info['buildingCash'] = format(buildingBindCash, ',')
    info['buildingWood'] = format(buildingWood, ',')
    info['buildingMojing'] = format(buildingMojing, ',')
    info['buildingXirang'] = format(buildingXirang, ',')
    growthMojing, growthXirang, growthWood, growthBindCash = guild._getGrowthMaintainFee()
    info['growthCash'] = format(growthBindCash, ',')
    info['salaryCash'] = format(guild._getTotalSalary(), ',')
    totalMojing, totalXirang, totalWood, totalCash = commGuild.calcMaintainFee(guild)
    info['totalCash'] = format(totalCash, ',')
    info['totalWood'] = format(totalWood, ',')
    info['totalMojing'] = format(totalMojing, ',')
    info['totalXirang'] = format(totalXirang, ',')
    return uiUtils.dict2GfxDict(info)


def getQuestTrackGuildAwardInfo(questId):
    data = getGTSD().data.get(questId, {})
    info = {}
    info['guildCash'] = data.get('bindCash', 0)
    info['guildWood'] = data.get('wood', 0)
    info['guildMojing'] = data.get('mojing', 0)
    info['guildXirang'] = data.get('xirang', 0)
    info['contrib'] = data.get('contrib', 0)
    return uiUtils.dict2GfxDict(info)


def getBonusInfo(fixedBonus, index, icon64 = False, forceIcon = False):
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
        bonusInfo.insert(3, itemInfo.get('name', gameStrings.TEXT_TIANYUMALLPROXY_1455))
        bonusInfo.insert(4, color)
        bonusInfo.insert(5, bonusItemId)
    return bonusInfo


def tmpAttendTips(ret, title):
    nameMap = {gametypes.BONUS_TYPE_MONEY: gameStrings.TEXT_INVENTORYPROXY_3297,
     gametypes.BONUS_TYPE_FAME: gameStrings.TEXT_CHALLENGEPROXY_199_1,
     gametypes.BONUS_TYPE_EXP: gameStrings.TEXT_GAMETYPES_6408,
     gametypes.BONUS_TYPE_FISHING_EXP: gameStrings.TEXT_ARENARANKAWARDPROXY_213,
     gametypes.BONUS_TYPE_SOC_EXP: gameStrings.TEXT_IMPL_IMPACTIVITIES_663}
    tipString = "<font size = \'14\' color = \'#f2ab0d\'>" + title + '</font><br>'
    for i in range(0, ret['num']):
        if ret[i][0] == gametypes.BONUS_TYPE_ITEM:
            tipString += "<font size = \'12\'>" + gameStrings.TEXT_ROLECARDPROXY_430 + ret[i][3] + gameStrings.TEXT_HISTORYCONSUMEDPROXY_256 + str(ret[i][1]) + '</font><br>'
        else:
            tipString += "<font size = \'12\'>" + gameStrings.TEXT_ROLECARDPROXY_430 + str(ret[i][1]) + gameStrings.TEXT_HISTORYCONSUMEDPROXY_256 + nameMap.get(ret[i][0]) + '</font><br>'

    return GfxValue(gbk2unicode(tipString))


def getItemInfoById(itemId, showNum = False):
    iconData = {}
    iconData['iconPath'] = uiUtils.getItemIconFile64(itemId)
    if showNum:
        iconData['num'] = 1
    else:
        iconData['num'] = ''
    iconData['itemId'] = itemId
    return iconData


def getMingPaiTip(mpId, owner = None):
    mpData = MPD.data.get(mpId)
    if not mpData:
        return
    tip = {'name': mpData.get('name', ''),
     'desc': mpData.get('desc', ''),
     'time': ''}
    if owner and hasattr(owner, 'mingpaiInfo') and owner.mingpaiInfo.has_key(mpId):
        mpInfo = owner.mingpaiInfo.get(mpId)
        if mpInfo and len(mpInfo) == 2 and mpInfo[1] > 0:
            expireTime = mpInfo[0] + mpInfo[1]
            tip['time'] = gameStrings.TEXT_TIPUTILS_974 % time.strftime('%Y-%m-%d %H:%M', time.localtime(expireTime))
    return tip


def getBuffTip(buffId):
    data = STD.data.get(buffId, None)
    detail = ''
    desc = ''
    p = BigWorld.player()
    conditionalFakeIconIds = SCD.data.get('conditionalFakeIconIds', ())
    treasureBoxBuffId = NSAD.data.get('treasureBoxBuffId', 0)
    wishBoxBuffId = SCD.data.get('itemWishBuffId', 0)
    if data != None:
        name = data.get('name', '')
        if buffId == uiConst.ZHIQIANGZHILI_BUFF:
            if hasattr(p, 'wingWorldXinmoArenaFinalWinnerBuffDesc'):
                descFromPlayer = '<br>'.join((str(name) for gbid, name in p.wingWorldXinmoArenaFinalWinnerBuffDesc.iteritems()))
                desc = data.get('desc', '') % descFromPlayer
            else:
                desc = WWCD.data.get('wingWorldXinMoBuffDesc', {}).get(buffId, '')
        elif buffId == uiConst.POMOZHISHI_BUFF:
            if hasattr(p, 'wingWorldXinMoUniqueBossWinnerBuffDesc'):
                descFromPlayer = '<br>'.join((str(name) for gbid, name in p.wingWorldXinMoUniqueBossWinnerBuffDesc.iteritems()))
                desc = data.get('desc', '') % descFromPlayer
            else:
                desc = WWCD.data.get('wingWorldXinMoBuffDesc', {}).get(buffId, '')
        elif buffId in conditionalFakeIconIds:
            if hasattr(p, 'conditionalPropTips'):
                desc = ''
                for k, v in p.conditionalPropTips.iteritems():
                    iconId = CPD.data.get(k, {}).get('buffIconId', 0)
                    if not buffId == iconId:
                        continue
                    descArr = []
                    for msgId, args in v:
                        text = uiUtils.getTextFromGMD(msgId) % args
                        descArr.append(text)

                    desc += '<br>'.join(descArr)
                    desc += '<br>'

        elif buffId == treasureBoxBuffId:
            if hasattr(p, 'buffTreasureBoxIds'):
                desc = ''
                descArr = []
                for boxId, boxType in p.buffTreasureBoxIds:
                    boxInfo = TBD.data.get(boxId)
                    text = ''
                    if boxType == gametypes.NEW_SERVER_ACTIVITY_BONUS_BOX_EX1:
                        text = boxInfo.get('bonusDescEx1', '')
                    elif boxType == gametypes.NEW_SERVER_ACTIVITY_BONUS_BOX_EX2:
                        text = boxInfo.get('bonusDescEx2', '')
                    if text:
                        descArr.append(text)

                desc += '<br>'.join(descArr)
                desc += '<br>'
        elif buffId == uiConst.GUILD_INERIT_BUFF:
            buffInfo = p.statesServerAndOwn.get(buffId, [])
            desc = ''
            if buffInfo:
                remainTime = buffInfo[0][1] + buffInfo[0][2]
                desc = data.get('desc', '') % utils.formatDatetime(remainTime)
        elif buffId == uiConst.GUILD_MAKE_PROFIT_PUNISH:
            if p.statesServerAndOwn.has_key(buffId):
                desc = data.get('desc', '') % p.freezeGuildContri
        elif buffId == uiConst.FAME_MAKE_PROFIT_PUNISH:
            if p.statesServerAndOwn.has_key(buffId):
                desc = ''
                for fameId, fameVal in p.freezeFameDict.iteritems():
                    desc += descUtils.getFameName(fameId) + ': ' + str(fameVal) + '/'

                desc = data.get('desc', '') % (desc[:-1],)
        elif wishBoxBuffId and buffId == wishBoxBuffId:
            wishDesc = ''
            for itemId in p.useItemWish:
                selectedWishType = p.useItemWish[itemId]
                if not selectedWishType:
                    continue
                itemList = UIWD.data.get(itemId, [])
                for wishData in itemList:
                    wishType = wishData.get('wishType', 0)
                    if selectedWishType and selectedWishType == wishType:
                        wishDesc += wishData.get('wishDetailDesc', '')

                if itemId != p.useItemWish.keys()[-1]:
                    wishDesc += '\n'

            desc = data.get('desc', '') % wishDesc
        elif buffId == SCD.data.get('extraYuanShenBuff', 0):
            xiuweiBLD = XBLD.data.get(p.xiuweiLevel, {})
            if xiuweiBLD and p.lv >= xiuweiBLD.get('startlv', 999) and xiuweiBLD.get('CatchUp', False):
                desc = data.get('desc', '%.2f%%') % (xiuweiBLD.get('exYuanShen', 0) * 100.0)
        else:
            desc = data.get('desc', '')
        detail = name + '<br>' + desc
    return detail


def onQueryBufferTipsProperty(pId, value):
    if not currentTipInfo:
        return
    buffProIds = currentTipInfo.get('buffPropIds', ())
    buffId = currentTipInfo.get('buffId')
    buffValueDict = currentTipInfo.get('buffPropValueDict', {})
    if buffProIds and buffId:
        if pId in buffProIds:
            buffValueDict[pId] = value
        if len(set(buffProIds)) == len(buffValueDict):
            buffTip = getBuffTip(buffId)
            if buffTip:
                if len(buffProIds) == 1:
                    buffTip = buffTip % value
                else:
                    buffTip = buffTip % tuple([ buffValueDict[buffProIds[i]] for i in xrange(len(buffProIds)) ])
                TipManager.showTipByTipId(currentTipInfo.get('tipType', 0), currentTipInfo.get('tipId', 0), buffTip)


def getSummonedSpriteTips(spriteId, spriteIdx = -1):
    sData = SSD.data.get(spriteId, {})
    tip = sData.get('name', spriteId)
    spriteInfo = BigWorld.player().summonSpriteList.get(spriteIdx)
    if spriteInfo:
        tip = spriteInfo.get('name', tip)
        tip += '\nLv.%s' % spriteInfo.get('props', {}).get('lv', 0)
    if spriteInfo:
        p = BigWorld.player()
        state = gameStrings.TEXT_TIPUTILS_1097
        if not spriteInfo or utils.getSpriteBattleState(spriteIdx):
            state = gameStrings.TEXT_TIPUTILS_1099
        if spriteInfo and spriteIdx in p.summonedSpriteLifeList:
            state = gameStrings.TEXT_TIPUTILS_1101
        if spriteInfo and spriteIdx in p.spriteBattleCallBackList:
            state = gameStrings.TEXT_TIPUTILS_1103
        tip += '\n' + state
    return tip


def _getItemBoxRewardList(itemCidData, itemId, mustObtainList, possibleObtainList):
    if itemCidData.get('itemSetInfo', None):
        _appendCidSetList(itemCidData, mustObtainList, possibleObtainList)
    elif itemCidData.get('itemBoxInfo', None):
        _appendCidBoxList(itemCidData, mustObtainList, possibleObtainList)
    elif itemCidData.get('bonusId', None):
        _appendCidBonusIdList(itemCidData, mustObtainList, possibleObtainList)
    elif itemCidData.get('needReMapBonusId', 0) == 1:
        _appendCidReMapBonusIdList(itemCidData, itemId, mustObtainList, possibleObtainList)


def _appendCidSetList(itemCidData, mustObtainList, possibleObtainList):
    bonusSetId, _ = itemCidData.get('itemSetInfo', (0, 0))
    if bonusSetId == 0:
        return
    _genBonusInSingleBonusSet(bonusSetId, mustObtainList, possibleObtainList)


def _appendCidBoxList(itemCidData, mustObtainList, possibleObtainList):
    bonusBoxId, _ = itemCidData.get('itemBoxInfo', (0, 0))
    if bonusBoxId == 0:
        return
    _genBonusInSingleBonusBox(bonusBoxId, mustObtainList, possibleObtainList)


def _appendCidBonusIdList(itemCidData, mustObtainList, possibleObtainList):
    bonusId = itemCidData.get('bonusId', 0)
    if bonusId == 0:
        return
    _genBonusWithBonusId(bonusId, mustObtainList, possibleObtainList)


def _appendCidReMapBonusIdList(itemCidData, itemId, mustObtainList, possibleObtainList):
    needReMapBonusId = itemCidData.get('needReMapBonusId', 0)
    if needReMapBonusId:
        bonusBoxId = reMapBonusBoxId(itemId)
        if bonusBoxId == 0:
            return
        _genBonusInSingleBonusBox(bonusBoxId, mustObtainList, possibleObtainList)


def _genBonusInSingleBonusSet(setId, mustObtainList, possibleObtainList, superRate = const.RANDOM_RATE_BASE_10K[1] + 1):
    data = BSD.data.get(setId, None)
    if data == None:
        return []
    else:
        calcType = data[0]['calcType']
        for d in data:
            dt = d
            if calcType == 1:
                if d.has_key('configName') and not utils.getConfigVal(d['configName']):
                    dt = {}
                    dt.update(d)
                    dt['bonusRate'] = d['bonusRateByConfig']
                curRate = dt['bonusRate']
                bonusId = dt.get('bonusId', 0)
                bonusNum = dt.get('maxBonusNum', 0)
            elif calcType == 2:
                curRate = d['bonusRate']
                bonusId = d.get('bonusId', 0)
                bonusNum = dt.get('maxBonusNum', 0)
            else:
                break
            if superRate != const.RANDOM_RATE_BASE_10K[1] + 1:
                if dt['bonusType'] == gametypes.BONUS_TYPE_BONUS_SET:
                    _genBonusInSingleBonusSet(bonusId, [], possibleObtainList, curRate * superRate / (const.RANDOM_RATE_BASE_10K[1] + 1))
                else:
                    possibleObtainList.append((bonusId, curRate, bonusNum))
            elif curRate > const.RANDOM_RATE_BASE_10K[1]:
                if dt['bonusType'] == gametypes.BONUS_TYPE_BONUS_SET:
                    _genBonusInSingleBonusSet(bonusId, mustObtainList, possibleObtainList)
                else:
                    mustObtainList.append((bonusId, curRate, bonusNum))
            elif dt['bonusType'] == gametypes.BONUS_TYPE_BONUS_SET:
                _genBonusInSingleBonusSet(bonusId, [], possibleObtainList, curRate * superRate / (const.RANDOM_RATE_BASE_10K[1] + 1))
            else:
                possibleObtainList.append((bonusId, curRate, bonusNum))

        return []


def _genBonusInSingleBonusBox(boxId, mustObtainList, possibleObtainList):
    p = BigWorld.player()
    if not p:
        return []
    if hasattr(p, 'recentMaxCombatScore'):
        recentMaxCombatScore = getattr(p, 'recentMaxCombatScore', 0)
    else:
        recentMaxCombatScore = getattr(p, 'combatScore', 0)
    boxData = _getBonusBoxDataByLv(boxId, p.lv, recentMaxCombatScore)
    if not boxData:
        return []
    if boxData.has_key('itemBonus') and utils.filtItemByConfig(boxData['itemBonus'][0], lambda e: e):
        itemId, rate, minNum, maxNum = boxData['itemBonus']
        if rate > const.RANDOM_RATE_BASE_10K[1]:
            mustObtainList.append((itemId, rate, maxNum))
        else:
            possibleObtainList.append((itemId, rate, maxNum))
    calcType = boxData.get('calcType')
    bonusSets = boxData.get('bonusSets', [])
    for setId, setRate in bonusSets:
        if setRate > const.RANDOM_RATE_BASE_10K[1]:
            _genBonusInSingleBonusSet(setId, mustObtainList, possibleObtainList)
        else:
            _genBonusInSingleBonusSet(setId, [], possibleObtainList, setRate)

    return []


def _getBonusBoxDataByLv(bonusBoxId, level, score):
    boxDataInfo = BBD.data.get(bonusBoxId, None)
    if boxDataInfo == None:
        return
    else:
        data = None
        dataByConfig = None
        for boxData in boxDataInfo:
            if boxData['lvStart'] <= level <= boxData['lvEnd']:
                if score > 0 and boxData.has_key('minScore') and score < boxData['minScore']:
                    continue
                if score > 0 and boxData.has_key('maxScore') and score > boxData['maxScore']:
                    continue
                if boxData.has_key('configName'):
                    if not utils.getConfigVal(boxData['configName']):
                        dataByConfig = boxData
                        break
                else:
                    data = boxData

        return dataByConfig or data


def _genBonusWithBonusId(bonusId, mustObtainList, possibleObtainList):
    bData = BD.data.get(bonusId)
    if not bData:
        return []
    bType = bData['type']
    if bType == gametypes.BONUS_DATA_TYPE_BOX:
        boxList = bData.get('bonusIds', [])
        _genBonusInBonusBoxWithoutCheck(boxList, mustObtainList, possibleObtainList)
    elif bType == gametypes.BONUS_DATA_TYPE_SET:
        setList = bData.get('bonusIds', [])
        _genBonusInBonusSetWithoutCheck(setList, mustObtainList, possibleObtainList)
    elif bType == gametypes.BONUS_DATA_TYPE_FIXED:
        fixedBonus = bData.get('fixedBonus', [])
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        for bt, itemId, itemNum in fixedBonus:
            mustObtainList.append((itemId, const.RANDOM_RATE_BASE_10K[1] + 1, itemNum))


def _genBonusInBonusBoxWithoutCheck(bonusBoxIdList, mustObtainList, possibleObtainList):
    for boxId in bonusBoxIdList:
        _genBonusInSingleBonusBox(boxId, mustObtainList, possibleObtainList)


def _genBonusInBonusSetWithoutCheck(bonusSetIdList, mustObtainList, possibleObtainList):
    for setId in bonusSetIdList:
        _genBonusInSingleBonusSet(setId, mustObtainList, possibleObtainList)


def reMapBonusBoxId(itemId):
    p = BigWorld.player()
    candidateId = 0
    bonusBoxIds = BBMD.data.get(itemId, [])
    for val in bonusBoxIds:
        schoolList = val.get('school', ())
        if len(schoolList) > 0 and p.school not in schoolList:
            continue
        sexList = val.get('sex', ())
        if len(sexList) > 0 and p.physique.sex not in sexList:
            continue
        bodyTypeList = val.get('bodyType', ())
        if len(bodyTypeList) > 0 and p.physique.bodyType not in bodyTypeList:
            continue
        candidateId = val.get('bonusBoxId', 0)
        return candidateId

    return 0
