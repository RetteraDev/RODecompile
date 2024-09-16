#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerItem.o
from gamestrings import gameStrings
import zlib
import BigWorld
import gameglobal
import const
import item
import gametypes
import gamelog
import utils
import math
import commcalc
import commQuest
import cPickle
from gamescript import FormularEvalEnv
from guis import ui
from guis import uiUtils
from guis import cursor
from guis import uiConst
from gamestrings import gameStrings
from gameclass import SkillInfo
from helpers import cellCmd
from helpers import navigator
from helpers import avatarMorpher
from helpers import strmap
from callbackHelper import Functor
from data import item_data as ID
from data import fame_data as FD
from data import state_data as SD
from data import consumable_item_data as CID
from data import summon_sprite_foot_dust_data as SSFDD
from data import summon_sprite_skin_data as SSSD
from data import sys_config_data as SYSD
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import vip_package_data as VPD
from data import qiren_config_data as QCD
from data import monster_event_trigger_data as METD
from data import map_config_data as MCD
from data import sys_config_data as SCD
from cdata import manual_equip_cost_data as MECD
from data import manual_equip_props_data as MEPD
from cdata import item_synthesize_set_data as ISSD
from data import vp_level_data as VLD
from data import summon_sprite_info_data as SSID
from cdata import gui_bao_ge_item_reverse_data as GBGIRD
from data import formula_client_data as FCD
from cdata import server_progress_prop_def_data as SPPDD

class ImpPlayerItem(object):

    def useBagItem(self, page, index, fromBag = const.RES_KIND_INV):
        if not self._isSoul():
            if fromBag == const.RES_KIND_INV:
                i = self.inv.getQuickVal(page, index)
                if not i:
                    return
                acExcitement = i.getAcExcitement()
                if acExcitement and not self.checkExcitementFeature(acExcitement):
                    return
                elif i.type == item.Item.BASETYPE_EQUIP:
                    if i.isRubbing():
                        self.showGameMsg(GMDD.data.RUBBING_FORBIDDEN_USE, ())
                        return
                    return self.trueUseBagItemCheckEquip(page, index)
                else:
                    return self.trueUseBagItem(page, index)
            else:
                self.truUseCrossBagItem(page, index)
        else:
            i = self.realInv.getQuickVal(page, index)
            if not i:
                return
            acExcitement = i.getAcExcitement()
            if acExcitement and not self.checkExcitementFeature(acExcitement):
                return
            if self._checkCommonUseItem(i):
                self._useConsumeItem(i, page, index)

    @ui.looseGroupTradeConfirm([1, 2], GMDD.data.RETURN_BACK_EQUIP)
    def trueUseBagItemCheckEquip(self, page, index):
        return self.trueUseBagItem(page, index)

    def checkItemCanUse(self, item):
        if hasattr(item, 'isExpireTTL') and item.isExpireTTL():
            self.showGameMsg(GMDD.data.ITEM_TTL_EXPIRE, (ID.data.get(item.id)['name'],))
            return False
        if item.hasLatch():
            self.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return False
        return True

    def truUseCrossBagItem(self, page, index):
        i = self.crossInv.getQuickVal(page, index)
        if i == const.CONT_EMPTY_VAL:
            return
        if ID.data.get(i.id, {}).get('canTakeToCrossServer', 0):
            if self._checkCommonUseItem(i):
                self._useConsumeItem(i, page, index, const.RES_KIND_CROSS_INV)
        else:
            self.showGameMsg(GMDD.data.USE_IN_CROSS_BAG_FORBIDDEN, ())

    def previewBagItem(self, nPage, nItem):
        i = self.inv.getQuickVal(nPage, nItem)
        if i != const.CONT_EMPTY_VAL:
            if CID.data.get(i.id, {}).get('itemQuest', ()):
                gameglobal.rds.ui.itemRewardList.show(i.id)
            else:
                gameglobal.rds.ui.fittingRoom.addItem(i)

    def trueUseBagItem(self, page, index):
        i = self.inv.getQuickVal(page, index)
        if i == const.CONT_EMPTY_VAL:
            return
        elif not i.isOneQuest() and self._isOnZaiju():
            self.showGameMsg(GMDD.data.BIANSHEN_USEITEM, ())
            return
        else:
            bsNoUseItem = None
            if self.bsState:
                sId = self.bsState[0]
                bsNoUseItem = SD.data.get(sId).get('bsNoUseItem', None)
            if bsNoUseItem == const.NOUSEALLITEM or bsNoUseItem == const.NOUSEQUESTITEM and i.isOneQuest():
                self.showGameMsg(GMDD.data.BIANSHEN_USEITEM, ())
                return
            elif i.isDye() or i.isRongGuang() or getattr(i, 'cstype', 0) == item.Item.SUBTYPE_2_RUBBING_CLEAN:
                if hasattr(i, 'isExpireTTL') and i.isExpireTTL():
                    self.showGameMsg(GMDD.data.ITEM_TTL_EXPIRE, (ID.data.get(i.id)['name'],))
                    return
                inv = gameglobal.rds.ui.inventory
                inv.dyeItemPage = page
                inv.dyeItemPos = index
                inv.setDyeState(i.isDye() or i.isRongGuang())
                return
            elif getattr(i, 'cstype', 0) == item.Item.SUBTYPE_2_OCCUPY_EQUIP_GEM:
                gameglobal.rds.ui.clearState()
                inv = gameglobal.rds.ui.inventory
                inv.setChangeOwnerState(page, index)
                self.showGameMsg(GMDD.data.CHOOSE_GEM_TO_CHANGE_OWNER, ())
                return True
            elif getattr(i, 'cstype', 0) == item.Item.SUBTYPE_2_ADD_EXP_BONUS:
                expBonus = gameglobal.rds.ui.expBonus
                if expBonus.isFreezed:
                    totalSec = expBonus.getTotalRemainTime()
                    hours = CID.data.get(i.id, {}).get('expBonusData', [1, 1])[1]
                    msg = GMD.data.get(GMDD.data.APPLY_EXP_WHEN_FREEZED_TIP, {}).get('text', gameStrings.TEXT_EXPBONUSPROXY_298) % (utils.formatTimeStr(int(totalSec), gameStrings.TEXT_EXPBONUSPROXY_79_1), utils.formatTimeStr(int(totalSec + hours * const.TIME_INTERVAL_HOUR), gameStrings.TEXT_EXPBONUSPROXY_79_1))
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.useApplyBonusItem, i, page, index))
                else:
                    self.useApplyBonusItem(i, page, index)
                return
            if getattr(i, 'cstype', 0) in (item.Item.SUBTYPE_2_SIGN_ITEM, item.Item.SUBTYPE_2_SIGN_CLEAN):
                if hasattr(i, 'isExpireTTL') and i.isExpireTTL():
                    self.showGameMsg(GMDD.data.ITEM_TTL_EXPIRE, (ID.data.get(i.id)['name'],))
                    return
                if i.hasLatch():
                    self.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                    return
                gameglobal.rds.ui.clearState()
                inv = gameglobal.rds.ui.inventory
                inv.setSignEquipState(page, index)
                if ui.get_cursor_state() != ui.SIGNEQUIP_STATE:
                    ui.reset_cursor()
                    ui.set_cursor_state(ui.SIGNEQUIP_STATE)
                    ui.set_cursor(cursor.equipSign)
                    ui.lock_cursor()
                    return True
            elif getattr(i, 'cstype', 0) == item.Item.SUBTYPE_2_RESTORE_FASHION_PROP:
                if hasattr(i, 'isExpireTTL') and i.isExpireTTL():
                    self.showGameMsg(GMDD.data.ITEM_TTL_EXPIRE, (ID.data.get(i.id)['name'],))
                    return
                if i.hasLatch():
                    self.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                    return
                gameglobal.rds.ui.clearState()
                if ui.get_cursor_state() != ui.RESET_FASHION_PROP:
                    ui.reset_cursor()
                    ui.set_cursor_state(ui.RESET_FASHION_PROP)
                    ui.set_bindItemPos(const.RES_KIND_INV, page, index)
                    ui.set_cursor(cursor.pickup)
                    ui.lock_cursor()
                    gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
                    return True
            elif getattr(i, 'cstype', 0) == item.Item.SUBTYPE_2_RESET_ONE_ABILITY:
                if not self.checkItemCanUse(i):
                    return
                gameglobal.rds.ui.clearState()
                gameglobal.rds.ui.lifeSkillNew.changeToTab(1)
                if ui.get_cursor_state() != ui.CANCEL_ABILITY_STATE:
                    ui.reset_cursor()
                    ui.set_cursor_state(ui.CANCEL_ABILITY_STATE)
                    ui.set_bindItemPos(const.RES_KIND_INV, page, index)
                    ui.set_cursor(cursor.equipCancelAbility)
                    ui.lock_cursor()
                    return True
            elif getattr(i, 'cstype', 0) == item.Item.SUBTYPE_2_RESET_ONE_ABILITY_NODE:
                if not self.checkItemCanUse(i):
                    return
                gameglobal.rds.ui.clearState()
                gameglobal.rds.ui.lifeSkillNew.changeToTab(1)
                if ui.get_cursor_state() != ui.CANCEL_ABILITY_NODE_STATE:
                    ui.reset_cursor()
                    ui.set_cursor_state(ui.CANCEL_ABILITY_NODE_STATE)
                    ui.set_bindItemPos(const.RES_KIND_INV, page, index)
                    ui.set_cursor(cursor.equipCancelAbility)
                    ui.lock_cursor()
                    return True
            elif i.isAddStarExpItem():
                if not gameglobal.rds.configData.get('enableDisassembleEquip', False):
                    self.showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
                    return
                if not self.checkItemCanUse(i):
                    return
                gameglobal.rds.ui.clearState()
                if ui.get_cursor_state() != ui.ADD_STAR_EXP_STATE:
                    ui.reset_cursor()
                    ui.set_cursor_state(ui.ADD_STAR_EXP_STATE)
                    ui.set_bindItemPos(const.RES_KIND_INV, page, index)
                    ui.set_cursor(cursor.addStarExp)
                    ui.lock_cursor()
                    gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
                    return True
            elif getattr(i, 'cstype', 0) == item.Item.SUBTYPE_2_FIREWORKS_LA_BA:
                fireworkLabaId = CID.data.get(i.id, {}).get('fireworkLabaId', None)
                if fireworkLabaId:
                    targetName = ''
                    if getattr(self.targetLocked, 'IsAvatar', False):
                        targetName = getattr(self.targetLocked, 'roleName', '')
                    gameglobal.rds.ui.fireWorkSender.show(targetName, page, index)
                    return True
                else:
                    targetLocked = self.targetLocked
                    if not targetLocked:
                        self.showGameMsg(GMDD.data.FIREWORK_NO_TARGET, ())
                        return
                    if not getattr(targetLocked, 'IsAvatar', False):
                        self.showGameMsg(GMDD.data.FIREWORK_NEED_AVATAR, ())
                        return
                    targetGbId = getattr(i, 'targetGbId', None)
                    if targetGbId and targetGbId != targetLocked.gbId:
                        self.showGameMsg(GMDD.data.ITEM_NEED_TARGET_GBID_RIGHT, (i.name,))
                        return
                    self.cell.useFireworksLaba(page, index, targetLocked.roleName, '', const.NORMAL_CHAT_MSG, False)
                    return True
            elif getattr(i, 'cstype', 0) == item.Item.SUBTYPE_2_LIFE_SKILL_ITEM_IDENTIFY:
                if hasattr(i, 'isExpireTTL') and i.isExpireTTL():
                    self.showGameMsg(GMDD.data.ITEM_TTL_EXPIRE, (ID.data.get(i.id)['name'],))
                    return
                if i.hasLatch():
                    self.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                    return
                gameglobal.rds.ui.clearState()
                if ui.get_cursor_state() != ui.IDENTIFY_ITEM_STATE:
                    ui.reset_cursor()
                    ui.set_cursor_state(ui.IDENTIFY_ITEM_STATE)
                    ui.set_cursor(cursor.identify)
                    ui.lock_cursor()
                    inv = gameglobal.rds.ui.inventory
                    inv.setIdentifyState(page, index)
                    return True
            elif getattr(i, 'cstype', 0) == item.Item.SUBTYPE_2_EQUIP_IDENTIFY:
                if hasattr(i, 'isExpireTTL') and i.isExpireTTL():
                    self.showGameMsg(GMDD.data.ITEM_TTL_EXPIRE, (ID.data.get(i.id)['name'],))
                    return
                if i.hasLatch():
                    self.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                    return
                gameglobal.rds.ui.clearState()
                if ui.get_cursor_state() != ui.IDENTIFY_MANUAL_EQUIP_STATE:
                    ui.reset_cursor()
                    ui.set_cursor_state(ui.IDENTIFY_MANUAL_EQUIP_STATE)
                    ui.set_cursor(cursor.identify)
                    ui.lock_cursor()
                    inv = gameglobal.rds.ui.inventory
                    inv.setIdentifyState(page, index)
                    return True
            elif getattr(i, 'cstype', 0) == item.Item.SUBTYPE_2_ITEM_RENEWAL:
                if hasattr(i, 'isExpireTTL') and i.isExpireTTL():
                    self.showGameMsg(GMDD.data.ITEM_TTL_EXPIRE, (ID.data.get(i.id)['name'],))
                    return
                if i.hasLatch():
                    self.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                    return
                gameglobal.rds.ui.clearState()
                if ui.get_cursor_state() != ui.RENEWAL_STATE:
                    ui.reset_cursor()
                    ui.set_cursor_state(ui.RENEWAL_STATE)
                    ui.set_cursor(cursor.repair)
                    ui.lock_cursor()
                    inv = gameglobal.rds.ui.inventory
                    inv.setRenewalState(page, index)
                    return True
            else:
                if getattr(i, 'cstype', 0) == item.Item.SUBTYPE_2_RESET_ONE_PROP:
                    if hasattr(i, 'isExpireTTL') and i.isExpireTTL():
                        self.showGameMsg(GMDD.data.ITEM_TTL_EXPIRE, (ID.data.get(i.id)['name'],))
                        return
                    if i.hasLatch():
                        self.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                        return
                    gameglobal.rds.ui.propReset.show(i.id, page, index)
                    return
                if getattr(i, 'cstype', 0) == item.Item.SUBTYPE_2_QUERY_PLAYER_POSITION:
                    if hasattr(i, 'isExpireTTL') and i.isExpireTTL():
                        self.showGameMsg(GMDD.data.ITEM_TTL_EXPIRE, (ID.data.get(i.id)['name'],))
                        return
                    if i.hasLatch():
                        self.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                        return
                    gameglobal.rds.ui.queryLocation.show()
                    return
                if getattr(i, 'cstype', None) == item.Item.SUBTYPE_2_GUILD_OPEN_ROUND_TABLE:
                    gameglobal.rds.ui.roundTable.openRoundTableByItem(i, page, index, gametypes.ROUND_TABLE_TYPE_GUILD)
                    return
                if getattr(i, 'cstype', None) == item.Item.SUBTYPE_2_FUBEN_OPEN_ROUND_TABLE:
                    gameglobal.rds.ui.roundTable.openRoundTableByItem(i, page, index, gametypes.ROUND_TABLE_TYPE_FUBEN)
                    return
                if getattr(i, 'cstype', None) == item.Item.SUBTYPE_2_VIP_SERVICE:
                    self.vipItemUseConfirm(i, page, index)
                    return
                if getattr(i, 'cstype', None) == item.Item.SUBTYPE_2_FAME:
                    fullDict = {const.FAME_FULL_TYPE_MAX: gameStrings.TEXT_IMPITEM_2349,
                     const.FAME_FULL_TYPE_WEEK: gameStrings.TEXT_IMPITEM_2350,
                     const.FAME_FULL_TYPE_DAY: gameStrings.TEXT_IMPITEM_2351}
                    full, already, fullType = self.checkUseItemFameFull(i)
                    fameId = CID.data.get(i.id, {}).get('fameId', 0)
                    fameName = FD.data.get(fameId, {}).get('name', gameStrings.TEXT_CHALLENGEPROXY_199_1)
                    if full and not already:
                        msg = GMD.data.get(GMDD.data.FAME_LIMIT_WARNING, {}).get('text', '') % (gameStrings.TEXT_CLANWARPROXY_217,
                         fameName,
                         fullDict[fullType],
                         fameName,
                         gameStrings.TEXT_CLANWARPROXY_217)
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.useFameItem, i, page, index))
                    else:
                        self.useFameItem(i, page, index)
                elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_BALANCE_ARENA_UPLOAD_TEMP:
                    gameglobal.rds.ui.balanceTemplateUpload.show(i)
                elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_ARENA_PLAYOFFS_VOTE:
                    self.onVoteItemClick()
                elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_ARENA_PLAYOFFS_AID:
                    gameglobal.rds.ui.arenaPlayoffsSupport.show()
                elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_NT_ITEM_PURCHASE:
                    if self._checkCommonUseItem(i):
                        gameglobal.rds.ui.tianyuMall.newPlayerTBBuyMallItem(Functor(self.newPlayerTBConfirmBuyCallBack, i, page, index))
                elif i.type in (item.Item.BASETYPE_CONSUMABLE, item.Item.BASETYPE_FASHION) and not i.isTianyucanjing() and not i.isServerDonate():
                    if self._checkCommonUseItem(i):
                        self._useConsumeItem(i, page, index)
                elif i.type == item.Item.BASETYPE_EQUIP:
                    if gameglobal.rds.configData.get('enableMallItemRenewal', False) == True:
                        if i.isMallFashionRenewable() and i.isExpireTTLEC():
                            msg = uiUtils.getTextFromGMD(GMDD.data.EXPIRE_ASK_FOR_RESUME, gameStrings.TEXT_IMPPLAYERITEM_390)
                            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.onOpenItemResume, i, page, index), noCallback=Functor(self.onEquipContinue, i, page, index))
                            return
                    dstPos = self.getBestMainEquipPart(i)
                    if dstPos in gametypes.EQU_PART_SUB and gameglobal.rds.ui.roleInfo.getSubEquipFlag():
                        dstPos = self.getBestSubEquipPart(i) + const.SUB_EQUIP_PART_OFFSET
                    if dstPos != -1:
                        if gameglobal.rds.configData.get('enableWardrobe', False) and self.isWardrobeCloth(i):
                            if GBGIRD.data.has_key(i.id):
                                cellCmd.equipWardrobeItemFromInv(page, index, i)
                            else:
                                from data import gui_bao_ge_config_data as GBGCD
                                filterIds = GBGCD.data.get('filterIds', ())
                                if i.id not in filterIds:
                                    msg = 'cant insert cloth from bag by itemId %s,%s,%s' % (str(i.id), str(i.equipType), str(i.equipSType))
                                    self.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, [msg], 0, {})
                                self.showGameMsg(GMDD.data.ITEM_ID_NOT_IN_GUIBAOGE, ())
                                cellCmd.exchangeInvEqu(page, index, dstPos)
                        else:
                            cellCmd.exchangeInvEqu(page, index, dstPos)
                elif i.type == item.Item.BASETYPE_PACK:
                    ps = self.bagBar.searchEmpty(0)
                    config = SCD.data.get('invEnlargeCost', ())
                    cashBagNumber = 0
                    for cash, bag in config:
                        if bag == 0:
                            cashBagNumber = cashBagNumber + 1

                    if ps >= BigWorld.player().inv.enabledPackSlotCnt:
                        if ps >= cashBagNumber:
                            gameglobal.rds.ui.expandPay.show(uiConst.EXPAND_INVENTORY_EXPAND, ps)
                        else:
                            data = config[ps]
                            gameglobal.rds.ui.expandPay.expandType = uiConst.EXPAND_INVENTORY_EXPAND
                            gameglobal.rds.ui.inventory.showPayMessage(data[0])
                    elif ps != -1:
                        cellCmd.equipPack(page, index, ps)
                elif i.type == item.Item.BASETYPE_LIFE_SKILL:
                    equipPosMap = item.Item.FISHING_EQUIP_PART_TABLE
                    BigWorld.player().cell.exchangeInvFishingEqu(page, index, equipPosMap[i.fishingEquipType])
                elif i.type == item.Item.BASETYPE_LIFE_EQUIP:
                    self.cell.equipLifeEqu(page, index)
                else:
                    itemData = ID.data.get(i.id, {})
                    targetData = itemData.get('navigatorTarget', '')
                    if len(targetData):
                        msg = uiUtils.getTextFromGMD(GMDD.data.NAVIGATOR_NEED_LEAVE_SPACE_HINT, '%s %s') % (MCD.data.get(self.mapID).get('name', ''), itemData.get('name', ''))
                        uiUtils.findPosWithAlert(targetData, msg)
                    else:
                        spriteKeyWord = itemData.get('spriteKeyWord', None)
                        if spriteKeyWord:
                            gameglobal.rds.ui.help.show(spriteKeyWord)
            return

    @ui.checkInventoryLock()
    def newPlayerTBConfirmBuyCallBack(self, item, page, index):
        bag = self._getUseBag(const.RES_KIND_INV)
        it = bag.getQuickVal(page, index)
        if it == const.CONT_EMPTY_VAL:
            return
        if it.id != item.id:
            return
        self.cell.useCommonItemWithCipher(page, index, 1, self.cipherOfPerson)

    def isWardrobeCloth(self, item):
        return item.isFashionEquip()

    def checkUseItemFameFull(self, it):
        defRet = (False, False, const.FAME_FULL_TYPE_NONE)
        if not it:
            return defRet
        data = CID.data.get(it.id, {})
        fameId = data.get('fameId', 0)
        fameNum = data.get('fameNum', 0)
        if not (data and fameId and fameNum):
            return defRet
        fd = FD.data.get(fameId, {})
        if not fd:
            return defRet
        oldVal = self.getFame(fameId)
        maxVal = fd.get('maxVal', 0)
        if maxVal == 0:
            maxVal = const.FAME_MAX_VALUE
        if oldVal >= maxVal:
            return (True, True, const.FAME_FULL_TYPE_MAX)
        if oldVal + fameNum > maxVal:
            return (True, False, const.FAME_FULL_TYPE_MAX)
        dayVal = self.fameDay.get(fameId, 0)
        dayMax = self.calcGainLimit(fameId, 'dayGainLimit')
        if dayMax > 0:
            if dayVal >= dayMax:
                return (True, True, const.FAME_FULL_TYPE_DAY)
            if dayVal + fameNum > dayMax:
                return (True, False, const.FAME_FULL_TYPE_DAY)
        weekVal, weekMax = self.fameWeek.get(fameId, (0, 0))
        if weekMax > 0:
            if weekVal >= weekMax:
                return (True, True, const.FAME_FULL_TYPE_WEEK)
            if weekVal + fameNum > weekMax:
                return (True, False, const.FAME_FULL_TYPE_WEEK)
        return defRet

    def calcGainLimit(self, fameId, name):
        fd = FD.data.get(fameId, {})
        if fd.has_key(name):
            script = str(fd.get(name))
            return FormularEvalEnv.evaluate(script, {'lv': self.lv})
        return 0

    def useFameItem(self, it, page, index):
        if self._checkCommonUseItem(it):
            self._useConsumeItem(it, page, index)

    def onOpenItemResume(self, item, page, pos, bagType = const.RES_KIND_INV):
        gameglobal.rds.ui.itemResume.show(item, page, pos, bagType)

    def onEquipContinue(self, item, page, pos):
        dstPos = self.getBestMainEquipPart(item)
        if dstPos in gametypes.EQU_PART_SUB and gameglobal.rds.ui.roleInfo.getSubEquipFlag():
            dstPos = self.getBestSubEquipPart(item) + const.SUB_EQUIP_PART_OFFSET
        cellCmd.exchangeInvEqu(page, pos, dstPos)

    def useFashionBagItem(self, page, index):
        i = self.fashionBag.getQuickVal(page, index)
        if i == const.CONT_EMPTY_VAL:
            return
        if i.type == item.Item.BASETYPE_EQUIP:
            if gameglobal.rds.configData.get('enableFashionBagRenew', False):
                if gameglobal.rds.configData.get('enableMallItemRenewal', False) == True:
                    if i.isMallFashionRenewable() and i.isExpireTTLEC():
                        msg = uiUtils.getTextFromGMD(GMDD.data.EXPIRE_ASK_FOR_RESUME, gameStrings.TEXT_IMPPLAYERITEM_390)
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.onOpenItemResume, i, page, index, const.RES_KIND_FASHION_BAG))
                        return
            dstPos = self.getBestMainEquipPart(i)
            if gameglobal.rds.configData.get('enableWardrobe', False) and self.isWardrobeCloth(i):
                cellCmd.equipWardrobeItemFromFashion(page, index, i)
            else:
                cellCmd.exchangeFashionBagEqu(page, index, dstPos)

    def useQuestItem(self, page, index):
        i = self.questBag.getQuickVal(0, index)
        if i == const.CONT_EMPTY_VAL:
            return
        else:
            if i.isExploreEquip():
                self.useExploreItem(i, page, index)
            elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_GUILD_BUSINESS_FIND_PATH:
                gameglobal.rds.ui.guildBusinessFindPath.show()
            elif i.isOneQuest() and hasattr(i, 'cstype'):
                if ID.data[i.id].get('tgtType', const.ITEM_NO_TARGET) == const.ITEM_NO_TARGET:
                    self.cell.useQuestItem(0, index)
                else:
                    target = BigWorld.entities.get(self.lockedId, None) if self.lockedId > 0 else self
                    if target:
                        tgtType = ID.data[i.id].get('tgtType')
                        tgtDist = ID.data[i.id].get('tgtDist', -1)
                        if commQuest.checkMonsterEventItem(target, i.id):
                            self.cell.triggerMonsterEvent(target.id, target.triggerEventIndex)
                            return
                        if target != self and tgtDist > 0 and self.position.distTo(target.position) > tgtDist:
                            self.showGameMsg(GMDD.data.ITEM_FORBIDDEN_FAR, (i.name,))
                            return
                        if tgtType == const.ITEM_NEED_TARGET_ENEMY and not self.isEnemy(target):
                            self.showGameMsg(GMDD.data.ITEM_NEED_TARGET_ENEMY, (i.name,))
                            return
                        if tgtType == const.ITEM_NEED_TARGET_FRIEND and self.isEnemy(target):
                            self.showGameMsg(GMDD.data.ITEM_NEED_TARGET_FRIEND, (i.name,))
                            return
                        if tgtType == const.ITEM_NEED_TARGET_TEAMATE and (not target.IsAvatar or self.id == target.id or not self._getMembers().has_key(target.gbId)):
                            self.showGameMsg(GMDD.data.ITEM_NEED_TARGET_TEAMMATE, (i.name,))
                            return
                        if tgtType == const.ITEM_NEED_TARGET_NOT_SELF and self == target:
                            self.showGameMsg(GMDD.data.ITEM_NEED_TARGET_NOT_SELF, (i.name,))
                            return
                        if hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_MONSTER_EVENT and getattr(target, 'IsMonster', False):
                            if commQuest.checkMonsterEventItem(target, i.id):
                                self.cell.triggerMonsterEvent(target.id, target.triggerEventIndex)
                                return
                        if hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_USE_SKILL and getattr(self, 'weaponState', 0) in (gametypes.WEAR_WAIST_ATTACH, gametypes.WEAR_BACK_ATTACH) and gameglobal.rds.ui.zaijuV2.widget:
                            gameglobal.rds.ui.zaijuV2.handleLeaveBtnClick()
                        self.cell.useQuestItemWithTarget(0, index, target.id)
            return

    @ui.checkItemMixNeedHint(1, 2)
    def batchUseBagItem(self, page, index):
        i = self.inv.getQuickVal(page, index)
        if i == const.CONT_EMPTY_VAL:
            return
        else:
            bsNoUseItem = None
            if self.bsState:
                sId = self.bsState[0]
                bsNoUseItem = SD.data.get(sId).get('bsNoUseItem', None)
            if bsNoUseItem == const.NOUSEALLITEM or bsNoUseItem == const.NOUSEQUESTITEM and i.isOneQuest():
                self.showGameMsg(GMDD.data.BIANSHEN_USEITEM, ())
                return
            if i.type in (item.Item.BASETYPE_CONSUMABLE, item.Item.BASETYPE_FASHION):
                if not self._checkCommonUseItem(i):
                    return
                if ID.data[i.id].get('tgtType', const.ITEM_NO_TARGET) == const.ITEM_NO_TARGET:
                    consumableItemData = CID.data.get(i.id, None)
                    if consumableItemData:
                        batchUseType = consumableItemData.get('batchUseType', 0)
                        if batchUseType:
                            self.cell.batchUseCommonItem(page, index, i.cwrap, const.RES_KIND_INV)
            return

    def useActionBarItem(self, page, index, fromBag = True):
        gamelog.debug('jorsef: useActionBarItem', page, index)
        self.useBagItem(page, index, fromBag)

    def showMessageBox(self, i, page, index):
        msg = ''
        if i.cstype == item.Item.SUBTYPE_2_RESET_BODYTYPE:
            msg = SYSD.data.get('resetBodyTypeTip', gameStrings.TEXT_IMPPLAYERITEM_637)
        elif i.cstype == item.Item.SUBTYPE_2_RESET_ROLENAME:
            msg = SYSD.data.get('resetRolenameTip', gameStrings.TEXT_IMPPLAYERITEM_639)
        elif i.cstype == item.Item.SUBTYPE_2_RESET_AVATARCONFIG:
            msg = SYSD.data.get('resetAvatarconfigTip', gameStrings.TEXT_IMPPLAYERITEM_641)
        elif i.cstype == item.Item.SUBTYPE_2_RESET_SEX:
            sexName = const.SEX_NAME[self.physique.sex]
            msg = SYSD.data.get('resetSexTip', gameStrings.TEXT_IMPPLAYERITEM_644 % sexName)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onConfirmUseItem, i, page, index))

    def vipItemUseConfirm(self, i, page, index):
        cidd = CID.data.get(i.id, {})
        packageId = cidd.get('packageID', 0)
        days = cidd.get('days', 0)
        vpdd = VPD.data.get(packageId, {})
        now = utils.getNow()
        if vpdd.get('isBasic', 0):
            if self.vipBasicPackage.get('tExpire', 0) < now:
                msg = gameStrings.TEXT_IMPPLAYERITEM_656
                cBasicDays = days
            else:
                msg = gameStrings.TEXT_IMPPLAYERITEM_659
                cBasicDays = days + int(math.ceil(max(self.vipBasicPackage.get('tExpire', 0) - now, 0) / const.TIME_INTERVAL_DAY))
            if cBasicDays > SCD.data.get('VIP_BUY_MAX_DAY', 60):
                self.onConfirmUseItem(i, page, index)
                return
            msg += gameStrings.TEXT_IMPPLAYERITEM_666 % days
        else:
            if self.vipBasicPackage.get('tExpire', 0) < now:
                self.onConfirmUseItem(i, page, index)
                return
            packageLeftTime = max(self.vipAddedPackage.get(packageId, {}).get('tExpire', 0) - now, 0)
            basicLeftTime = max(self.vipBasicPackage.get('tExpire', 0) - now, 0)
            canBuyDay = int(math.ceil((basicLeftTime - packageLeftTime) / const.TIME_INTERVAL_DAY))
            msg = ''
            if canBuyDay < days:
                self.onConfirmUseItem(i, page, index)
                return
            canBuyDay = days
            if self.vipAddedPackage.get(packageId, {}).get('tExpire', 0) < utils.getNow():
                msg += gameStrings.TEXT_IMPPLAYERITEM_656
            else:
                msg += gameStrings.TEXT_IMPPLAYERITEM_659
            name = vpdd.get('name', gameStrings.TEXT_IMPPLAYERITEM_689)
            msg += gameStrings.TEXT_IMPPLAYERITEM_690 % (canBuyDay, name)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onConfirmUseItem, i, page, index))

    def onConfirmUseItem(self, i, page, index):
        if self._checkCommonUseItem(i):
            self.cell.useCommonItem(page, index, 1, const.RES_KIND_INV)

    def _getUseBag(self, resKind):
        if resKind == const.RES_KIND_INV:
            return self.realInv
        elif resKind == const.RES_KIND_CROSS_INV:
            return self.crossInv
        else:
            return None

    def onXiuWeiLastRankQueryCallBack(self, i, page, index):
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableStraightLvUpV2', False):
            cfgID = CID.data.get(i.id, {}).get('lvUpRoleIDs', {}).get(BigWorld.player().school)
            from data import straight_lv_up_role_data as SLURD
            lvFormula = SLURD.data.get(cfgID, {}).get('lvFormula', 0)
            f = FCD.data.get(lvFormula, {}).get('formula', None)
            minTopLv = getattr(p, 'xiuweiLastRankLv', 0)
            toLv = int(math.ceil(f({'minTopLv': minTopLv})))
            msg = GMD.data.get(GMDD.data.ALERT_OF_USE_STRAIGHT_UP_V2, {}).get('text', '') % toLv
        else:
            msg = GMD.data.get(GMDD.data.ALERT_OF_USE_STRAIGHT_UP, {}).get('text', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.onConfirmUseItem, i, page, index))

    def _useConsumeItem(self, i, page, index, resKind = const.RES_KIND_INV):
        p = BigWorld.player()
        bag = self._getUseBag(resKind)
        it = bag.getQuickVal(page, index)
        if it == const.CONT_EMPTY_VAL:
            return
        else:
            target = BigWorld.entities.get(self.lockedId, None)
            if commQuest.checkMonsterEventItem(target, i.id):
                self.cell.triggerMonsterEvent(target.id, target.triggerEventIndex)
                return
            if i.type == item.Item.BASETYPE_EQUIP:
                nItemDes = p.getBestMainEquipPart(i)
                if nItemDes != gametypes.EQU_PART_NONE:
                    cellCmd.exchangeCrossInvEqu(page, index, nItemDes)
            elif hasattr(i, 'cstype') and i.cstype in (item.Item.SUBTYPE_2_FISHING_BAIT,
             item.Item.SUBTYPE_2_ROD_ENHANCE,
             item.Item.SUBTYPE_2_BUOY_ENHANCE,
             item.Item.SUBTYPE_2_HOOK_ENHANCE):
                if i.cstype == item.Item.SUBTYPE_2_FISHING_BAIT:
                    canEquipFishing = i.canEquipFishing(self.fishingLv, gametypes.FISHING_EQUIP_BAIT)
                    if canEquipFishing != item.Item.EQUIPABLE:
                        if canEquipFishing == item.Item.WRONG_FISHING_LV:
                            self.showGameMsg(GMDD.data.ITEM_FORBIDDEN_WRONG_FISHINGLV, ())
                        return
                    if self.stateMachine.checkStatus(const.CT_EQUIP_FISH_BAIT):
                        if gameglobal.rds.ui.fishing.FishStartMediator == None:
                            gameglobal.rds.ui.fishing.showFishingStart()
                    else:
                        return
                posMap = {item.Item.SUBTYPE_2_ROD_ENHANCE: gametypes.FISHING_EQUIP_ROD,
                 item.Item.SUBTYPE_2_BUOY_ENHANCE: gametypes.FISHING_EQUIP_BUOY,
                 item.Item.SUBTYPE_2_HOOK_ENHANCE: gametypes.FISHING_EQUIP_HOOK,
                 item.Item.SUBTYPE_2_FISHING_BAIT: gametypes.FISHING_EQUIP_BAIT}
                self.cell.setConsumableFishingEquip(posMap[i.cstype], i.id)
            elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_HUAZHUANG:
                gameglobal.rds.ui.huazhuang.show()
            elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_RED_PACKET:
                gameglobal.rds.ui.redPacket.show()
            elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_DYEBAG:
                gameglobal.rds.ui.dyePlane.show()
            elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_STORY_EDIT:
                gameglobal.rds.ui.storyEditDebug.showStoryEdit()
            elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_COLOR_CARD:
                inv = gameglobal.rds.ui.inventory
                inv.chooseColorCard(page, index)
            elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_NEW_AVATAR_STRAIGHT_UP:
                if gameglobal.rds.configData.get('enableStraightLvUpV2', False):
                    p.queryXiuWeiLastRankLv(Functor(self.onXiuWeiLastRankQueryCallBack, i, page, index))
                else:
                    msg = GMD.data.get(GMDD.data.ALERT_OF_USE_STRAIGHT_UP, {}).get('text', '')
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.onConfirmUseItem, i, page, index))
            elif hasattr(i, 'cstype') and i.cstype in (item.Item.SUBTYPE_2_RESET_BODYTYPE,
             item.Item.SUBTYPE_2_RESET_ROLENAME,
             item.Item.SUBTYPE_2_RESET_AVATARCONFIG,
             item.Item.SUBTYPE_2_RESET_SEX):
                self.showMessageBox(i, page, index)
            elif hasattr(i, 'cstype') and i.cstype in (item.Item.SUBTYPE_2_ZHUANGSHI_CLEAN, item.Item.SUBTYPE_2_ZHUANGSHI):
                self.useZhuangshiItem(i, page, index)
            else:
                if hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_MULTI_TELEPORT:
                    return
                if hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_MONSTER_EVENT:
                    target = BigWorld.entities.get(self.lockedId, None)
                    triggered = False
                    if commQuest.checkMonsterEventItem(target, i.id):
                        self.cell.triggerMonsterEvent(target.id, target.triggerEventIndex)
                        triggered = True
                    if not triggered:
                        self.showGameMsg(GMDD.data.USE_MONSTER_EVENT_ITEM_FAIL, ())
                elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_RIDE_EXP_ADD:
                    gameglobal.rds.ui.messageBox.dismiss(getattr(self, 'useCommonItemMsgBoxId', 0))
                    rideWingType = CID.data.get(i.id, {}).get('rideWingType', 0)
                    name = ID.data[i.id].get('name', '')
                    if rideWingType == const.PLAYER_VEHICLE_RIDE:
                        if not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_RIDE_EXP_ADD):
                            msg = uiUtils.getTextFromGMD(GMDD.data.USE_RIDE_ITEM_EXP_ADD, '%s') % name
                            self.useCommonItemMsgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.cell.useCommonItem, page, index, 1, resKind), isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_RIDE_EXP_ADD)
                        else:
                            self.cell.useCommonItem(page, index, 1, resKind)
                    elif rideWingType == const.PLAYER_VEHICLE_WING:
                        if not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_WING_EXP_ADD):
                            msg = uiUtils.getTextFromGMD(GMDD.data.USE_WING_ITEM_EXP_ADD, '%s') % name
                            self.useCommonItemMsgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.cell.useCommonItem, page, index, 1, resKind), isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_WING_EXP_ADD)
                        else:
                            self.cell.useCommonItem(page, index, 1, resKind)
                elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_TIHUCHA:
                    msg = uiUtils.getTextFromGMD(GMDD.data.TIHUCHA_TRANS_MSG, '')
                    tVp = VLD.data.get(self.lv, {}).get('tihuchaTransVp', 0)
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.cell.useCommonItem, page, index, 1, resKind))
                elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_SPRITE_STATE:
                    spriteStateFilterType = CID.data.get(i.id, {}).get('spriteStateFilterType', 0)
                    if spriteStateFilterType == const.SPRITE_STATE_FILTER_CURRENT:
                        msg = gameStrings.ZMJ_SPRITE_ITEM_USE_TXT
                        if self.summonedSpriteInWorld:
                            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.cell.useCommonItem, page, index, 1, resKind))
                        else:
                            self.showGameMsg(GMDD.data.SPRITE_STATE_NO_CALLOUT_SPRITE, ())
                    else:
                        self.cell.useCommonItem(page, index, 1, resKind)
                elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_HP_POOL:
                    hpStoneVal = CID.data.get(i.id, {}).get('hpStone', 0)
                    if self.hpPool >= const.HP_POOL_MAX:
                        self.showGameMsg(GMDD.data.FAIL_HP_POOL_MAX, ())
                    elif self.hpPool + hpStoneVal > const.HP_POOL_MAX:
                        msg = uiUtils.getTextFromGMD(GMDD.data.USE_HPSTONE_WILL_OVERFLOW, 'too much hpPool')
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.cell.useCommonItem, page, index, 1, resKind))
                    else:
                        self.cell.useCommonItem(page, index, 1, resKind)
                elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_MP_POOL:
                    mpStoneVal = CID.data.get(i.id, {}).get('mpStone', 0)
                    if self.mpPool >= const.MP_POOL_MAX:
                        self.showGameMsg(GMDD.data.FAIL_MP_POOL_MAX, ())
                    elif self.mpPool + mpStoneVal > const.MP_POOL_MAX:
                        msg = uiUtils.getTextFromGMD(GMDD.data.USE_MPSTONE_WILL_OVERFLOW, 'too much mpPool')
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.cell.useCommonItem, page, index, 1, resKind))
                    else:
                        self.cell.useCommonItem(page, index, 1, resKind)
                elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_SPRITE_SKIN:
                    spriteSkinId = CID.data.get(i.id, {}).get('spriteSkinId', ())
                    spriteId = spriteSkinId[0]
                    for data in BigWorld.player().summonSpriteList.values():
                        pSpriteId = data.get('spriteId', None)
                        if spriteId == pSpriteId:
                            self.cell.useCommonItem(page, index, 1, resKind)
                            return

                    self.showGameMsg(GMDD.data.SUMMON_SPRITE_SKIN_UNLOCK_FAIL_NO_SUMMON, (SSSD.data.get(spriteSkinId, {}).get('skinName', ''), SSID.data.get(spriteId, {}).get('name', {})))
                elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_FINISH_QUESTION:
                    gameglobal.rds.ui.questionnaire.show(uiConst.QUESTIONNAIRE_TYPE_ITEM, i.id)
                elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_SPRITE_DUST:
                    spriteDustId = CID.data.get(i.id, {}).get('spriteDustId', ())
                    spriteId = spriteDustId[0]
                    for data in BigWorld.player().summonSpriteList.values():
                        pSpriteId = data.get('spriteId', None)
                        if spriteId == pSpriteId:
                            self.cell.useCommonItem(page, index, 1, resKind)
                            return

                    self.showGameMsg(GMDD.data.SUMMON_SPRITE_DUST_UNLOCK_FAIL_NO_SUMMON, (SSFDD.data.get(spriteDustId, {}).get('footDustName', ''), SSID.data.get(spriteId, {}).get('name', {})))
                elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_OPTIONAL_BONUS:
                    gameglobal.rds.ui.optionalRewardBox.showMulti(i.id, page, index)
                elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_GET_SELECT_ITEM:
                    self.cell.useCommonItem(page, index, 1, resKind)
                elif gameglobal.rds.configData.get('enableUseMultipleItems', False) and CID.data.get(i.id, {}).get('useMultipleAtOnce', 0) and i.cwrap > 1:
                    gameglobal.rds.ui.itemBatchUse.setItem(i, page, index)
                    gameglobal.rds.ui.itemBatchUse.show()
                elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_FINISH_MAIN_QUEST:
                    if gameglobal.rds.configData.get('enableSummonedSprite', False) and getattr(self, 'summonSpriteList', {}) and not getattr(self, 'spriteBattleIndex', 0):
                        msg = uiUtils.getTextFromGMD(GMDD.data.CHECK_FINISH_QUEST_ITEM_SPRITE, '')
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.useFinishQuestItem, page, index, resKind), yesBtnText=gameStrings.TEXT_IMPPLAYERITEM_881)
                    else:
                        self.useFinishQuestItem(page, index, resKind)
                elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_VT_PLANT:
                    p.plantTreeReq(Functor(self.onConfirmUseItem, i, page, index))
                elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_VT_SEEK_MY_TREE:
                    p.seekToDPTree()
                elif p.getServerProgressStatusData(SPPDD.data.EXP_TO_YUANSHEN) and i.id in SCD.data.get('expToYuanshenItemIds', []):
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(SCD.data.get('expToYuanshenMsgBoxTxt', '') % i.name, yesCallback=Functor(self.onConfirmUseItem, i, page, index))
                elif ID.data[i.id].get('tgtType', const.ITEM_NO_TARGET) == const.ITEM_NO_TARGET:
                    clues = ID.data[i.id].get('relatedClues', ())
                    for cid in clues:
                        if self.getClueFlag(cid):
                            msg = QCD.data.get('useQirenItemConfirm', gameStrings.TEXT_IMPPLAYERITEM_904)
                            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cell.useCommonItem, page, index, 1, resKind))
                            break
                    else:
                        self.cell.useCommonItem(page, index, 1, resKind)

                else:
                    target = BigWorld.entities.get(self.lockedId, None) if self.lockedId > 0 else self
                    if target:
                        tgtDist = ID.data[i.id].get('tgtDist', -1)
                        if target != self and tgtDist > 0 and self.position.distTo(target.position) > tgtDist:
                            self.showGameMsg(GMDD.data.ITEM_FORBIDDEN_FAR, (i.name,))
                            return
                        tgtType = ID.data[i.id].get('tgtType')
                        if tgtType == const.ITEM_NEED_TARGET_ENEMY and not self.isEnemy(target):
                            self.showGameMsg(GMDD.data.ITEM_NEED_TARGET_ENEMY, (i.name,))
                            return
                        if tgtType == const.ITEM_NEED_TARGET_FRIEND and self.isEnemy(target):
                            self.showGameMsg(GMDD.data.ITEM_NEED_TARGET_FRIEND, (i.name,))
                            return
                        if tgtType == const.ITEM_NEED_TARGET_TEAMATE and (not target.IsAvatar or self.id == target.id or not self._getMembers().has_key(target.gbId)):
                            self.showGameMsg(GMDD.data.ITEM_NEED_TARGET_TEAMMATE, (i.name,))
                            return
                        if tgtType == const.ITEM_NEED_TARGET_NOT_SELF and self == target:
                            self.showGameMsg(GMDD.data.ITEM_NEED_TARGET_NOT_SELF, (i.name,))
                            return
                        clues = ID.data[i.id].get('relatedClues', ())
                        for cid in clues:
                            if self.getClueFlag(cid):
                                msg = QCD.data.get('useQirenItemConfirm', gameStrings.TEXT_IMPPLAYERITEM_904)
                                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cell.useCommonItemWithTarget, resKind, page, index, target.id))
                                break
                        else:
                            self.cell.useCommonItemWithTarget(resKind, page, index, target.id)

            return

    def useFinishQuestItem(self, page, index, resKind):
        msg = uiUtils.getTextFromGMD(GMDD.data.FINISH_MAIN_QUEST_MSG_BOX_DESC, '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.cell.useCommonItem, page, index, 1, resKind))

    def _checkCommonUseItem(self, i):
        if not i:
            return False
        if self.inCombat or self.bufActState or self.isUseQingGong:
            if i.type == item.Item.BASETYPE_EQUIP:
                self.showGameMsg(GMDD.data.CHANGE_EQUIP_FORBIDDEN_IN_COMBAT, ())
                return False
        if i.type == item.Item.BASETYPE_EQUIP:
            return True
        data = CID.data.get(i.id)
        if not data:
            return False
        exclude = ('UNCONTROL_ST', 'MAN_DOWN_ST') if data.get('useUnderControl', 0) else ()
        if not self.stateMachine.checkStatus_check(const.CT_USE_ITEM, exclude):
            return False
        if not hasattr(i, 'cstype'):
            self.chatToEventEx(gameStrings.TEXT_IMPPLAYERITEM_971, const.CHANNEL_COLOR_RED)
            return False
        if i.cstype == item.Item.SUBTYPE_2_SKILL_BOOK:
            skillId = CID.data.get(i.id, {}).get('learnSkillId', -1)
            if self.getSkills().has_key(skillId):
                self.showGameMsg(GMDD.data.LEARN_SKILL_FORBIDEN, ())
                return False
        if i.cstype == item.Item.SUBTYPE_2_USE_SKILL and hasattr(i, 'skillId'):
            skillId = i.skillId
            skillLv = i.skillLv
            if not self.checkSkill(SkillInfo(skillId, skillLv)):
                return False
        if i.cstype in (item.Item.SUBTYPE_2_CLAN_WAR_STONE,
         item.Item.SUBTYPE_2_CLAN_WAR_RELIVE_BOARD,
         item.Item.SUBTYPE_2_CLAN_WAR_ANTI_AIR_TOWER,
         item.Item.SUBTYPE_2_CLAN_WAR_GATE,
         item.Item.SUBTYPE_2_CLAN_WAR_STONE_CORE):
            if self.inMoving():
                return False
        if i.cstype == item.Item.SUBTYPE_2_RESET_SEX:
            if not utils.checkCanChangeSex(self):
                return False
        if i.cstype == item.Item.SUBTYPE_2_RESET_BODYTYPE:
            if not utils.checkCanChangeBodyType(self):
                return False
        return True

    def getEquipPart(self, i):
        partList = i.whereEquip()
        p = BigWorld.player()
        dstPos = partList[0]
        if len(partList) > 1:
            for id in range(0, len(partList)):
                part = partList[id]
                mainEquip = p.equipment.get(part)
                subEquip = commcalc.getAlternativeEquip(p, part)
                if mainEquip and getattr(mainEquip, 'uuid', '') == getattr(i, 'uuid', ''):
                    dstPos = part
                    break
                elif subEquip and getattr(subEquip, 'uuid', '') == getattr(i, 'uuid', ''):
                    dstPos = part
                    break

        return dstPos

    def getBestMainEquipPart(self, i):
        partList = i.whereEquip()
        p = BigWorld.player()
        dstPos = partList[0]
        if len(partList) > 1:
            for id in range(0, len(partList)):
                part = partList[id]
                if p.equipment.isEmpty(part):
                    dstPos = part
                    break
                elif dstPos != part:
                    dstEquipItem = p.equipment.get(dstPos)
                    tempEquipItem = p.equipment.get(part)
                    if dstEquipItem.score != 0 and tempEquipItem.score != 0 and dstEquipItem.score > tempEquipItem.score:
                        dstPos = part
                    elif dstEquipItem.quality > tempEquipItem.quality:
                        dstPos = part

        return dstPos

    def checkGetBestMainEquipPart(self, tempEquipItem):
        p = BigWorld.player()
        dstPart = p.getBestMainEquipPart(tempEquipItem)
        if tempEquipItem.canEquip(p, dstPart) == item.Item.EQUIPABLE:
            if p.equipment.isEmpty(dstPart):
                return (True, dstPart)
            dstEquipItem = p.equipment.get(dstPart)
            if dstEquipItem.score != 0 and tempEquipItem.score != 0 and dstEquipItem.score >= tempEquipItem.score:
                return (False, None)
            elif dstEquipItem.quality >= tempEquipItem.quality:
                return (False, None)
            else:
                return (True, dstPart)
        return (False, None)

    def getBestSubEquipPart(self, i):
        partList = i.whereEquip()
        p = BigWorld.player()
        dstPos = partList[0]
        if len(partList) > 1:
            for id in range(0, len(partList)):
                part = partList[id]
                if not commcalc.getAlternativeEquip(p, part):
                    dstPos = part
                    break
                elif dstPos != part and commcalc.getAlternativeEquip(p, dstPos).score > commcalc.getAlternativeEquip(p, part).score:
                    dstPos = part

        return dstPos

    def checkCanDoAction(self):
        if not self.stateMachine.checkStatus(const.CT_ACTION_SPELL):
            return False
        return True

    def showBag(self, isDown):
        if isDown:
            if self._isSoul() and gameglobal.rds.configData.get('enableCrossServerBag', False):
                if gameglobal.rds.ui.crossServerBag.isShow():
                    gameglobal.rds.ui.crossServerBag.hide()
                else:
                    gameglobal.rds.ui.crossServerBag.show()
            elif gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
            else:
                gameglobal.rds.ui.inventory.show()

    def canPay(self, total):
        return total <= self.cash + self.bindCash

    @ui.checkItemMixNeedHint(1, 2)
    def useSynthesizeItem(self, page, pos):
        if self.life == gametypes.LIFE_DEAD or self.inCombat or self.isUseQingGong or gameglobal.rds.ui.trade.isShow:
            return
        it = self.inv.getQuickVal(page, pos)
        if it == const.CONT_EMPTY_VAL:
            return
        self.cell.useCommonItem(page, pos, 1, const.RES_KIND_INV)

    def set_renewalTypeExpireTimeDict(self, old):
        gameglobal.rds.ui.roleInfo.refreshRenewal()

    def useApplyBonusItem(self, i, page, index):
        if self._checkCommonUseItem(i):
            self._useConsumeItem(i, page, index)

    def checkSetPassword(self, callback = None):
        if gameglobal.rds.configData.get('enableInventoryLock', False):
            if self.hasInvPassword:
                if callback:
                    callback()
                return True
            elif getattr(self, 'bShowPasswordHint', False):
                if callback:
                    callback()
                return True
            else:
                self.bShowPasswordHint = True
                msg = GMD.data.get(GMDD.data.STORAGE_PASSWORD_HINT, {}).get('text', gameStrings.TEXT_IMPPLAYERITEM_1130)
                if not callback:
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, gameglobal.rds.ui.inventorySetPassword.show, yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_644, noBtnText=gameStrings.TEXT_AVATAR_2876_1)
                else:
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(gameglobal.rds.ui.inventorySetPassword.show, callback), yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_644, noCallback=callback, noBtnText=gameStrings.TEXT_AVATAR_2876_1)
                return False
        else:
            if callback:
                callback()
            return True

    def navigateToUseItem(self, resKind, page, pos, uuid, useSpaceNo, usePos):
        failedCallback = Functor(self.onNavigateToUsePosFail, resKind, page, pos, uuid, useSpaceNo, usePos)
        arriveCallback = Functor(self.onNavigateToUsePos, resKind, page, pos, uuid, useSpaceNo, usePos)
        navigator.getNav().pathFinding((usePos[0],
         usePos[1],
         usePos[2],
         useSpaceNo), failedCallback=failedCallback, arriveCallback=arriveCallback)

    @ui.callAfterTime(time=0.1)
    def onNavigateToUsePos(self, resKind, page, pos, uuid, useSpaceNo, usePos):
        bag = self._getUseBag(resKind)
        it, mpage, mpos = bag.findItemByUUID(uuid)
        self._useConsumeItem(it, mpage, mpos, resKind)

    def onNavigateToUsePosFail(self, resKind, page, pos, uuid, useSpaceNo, usePos):
        posDesc = '(%s,%s)' % (int(usePos[0]), int(usePos[2]))
        self.showGameMsg(GMDD.data.USE_ITEM_FAIL_SEEK, (posDesc,))

    def doPlayWabaoTurn(self, cbtPosInfo, itemId):
        resItemList = cbtPosInfo.get('itemInfo')
        jumpList = cbtPosInfo.get('jumpInfo')
        if resItemList and jumpList:
            gameglobal.rds.ui.waBao.show(itemId, resItemList, jumpList)
        self.inWabaoStatus = True
        super(self.__class__, self).doPlayWabaoTurn(cbtPosInfo, itemId)

    def stopWaBaoAction(self):
        super(self.__class__, self).stopWaBaoAction()
        self.inWabaoStatus = False

    def onWabaoRewardDone(self, itemId):
        self.inWabaoStatus = False
        gameglobal.rds.ui.showSpecialCurve([itemId])
        super(self.__class__, self).onWabaoRewardDone(itemId)

    def onCheckUseCommonItem(self, page, pos, resKind):
        bag = self._getUseBag(resKind)
        item = bag.getQuickVal(page, pos)
        if item:
            if gameglobal.rds.ui.itemPushUse.mediator:
                gameglobal.rds.ui.itemPushUse.hide()
            if item.isStorehouse():
                BigWorld.callback(0.5, Functor(gameglobal.rds.ui.itemPushUse.show, item.uuid, True))
            else:
                BigWorld.callback(0.5, Functor(gameglobal.rds.ui.itemPushUse.show, item.uuid))

    def makeManualEquip(self, npcEntId, tgtEquipId, makeType, isHaveMakeBook, isSelectDiKou, isTianBiEnough, bMsg = True):
        if not isHaveMakeBook:
            bMsg and self.showGameMsg(GMDD.data.MAKE_EQUIP_MATERIAL_NOT_ENOUGH, ())
            return
        if isSelectDiKou and not isTianBiEnough:
            bMsg and self.showGameMsg(GMDD.data.MAKE_EQUIP_COIN_NOT_ENOUGH, ())
            return
        if not MECD.data.has_key(tgtEquipId) or not MEPD.data.has_key(tgtEquipId):
            return
        costData = MECD.data[tgtEquipId]
        if makeType and makeType > len(costData.get('extraCost', ())) or makeType < 0:
            return
        itemConsumeSetId = costData.get('materialSetNeed')
        sd = ISSD.data.get(itemConsumeSetId, ())
        costDict = {}
        UnEffectBindingItems = []
        for d in sd:
            itemId = d.get('itemId', 0)
            if itemId == 0:
                continue
            numRange = d.get('numRange', (0, 0))
            itemSearchType = d.get('itemSearchType', gametypes.ITEM_MIX_TYPE_NO_PARENT)
            enableParentCheck = True if itemSearchType == gametypes.ITEM_MIX_TYPE_PARENT else False
            if costDict.has_key(itemId):
                raise Exception(gameStrings.TEXT_IMPPLAYERITEM_1217 % (tgtEquipId, makeType))
            costDict[itemId] = (numRange, enableParentCheck)
            if d.get('UnEffectBinding', 0) and gameglobal.rds.configData.get('enableMakeManualEquipWhiteList', False):
                UnEffectBindingItems.append(itemId)

        needBind = False
        for itemId, (numRange, enableParentCheck) in costDict.iteritems():
            numNeed = max(numRange)
            if not numNeed:
                continue
            remain, res = self.inv.cntItemWithPlans(itemId, numNeed, enableParentCheck=enableParentCheck)
            if remain:
                itemName = ID.data.get(itemId, {}).get('name', '')
                if self.inv.hasItemExpireTTL(itemId, enableParentCheck=enableParentCheck):
                    bMsg and self.showGameMsg(GMDD.data.MAKE_EQUIP_MATERIAL_EXPIRED, (itemName,))
                else:
                    if isSelectDiKou:
                        continue
                    bMsg and self.showGameMsg(GMDD.data.MAKE_EQUIP_MATERIAL_NOT_ENOUGH, (itemName,))
                return
            if itemId in UnEffectBindingItems:
                continue
            needBind = needBind or any([ self.inv.getQuickVal(pg, pos).isForeverBind() for pg, pos, _ in res ])

        if makeType > 0:
            remainDiscountTime = gameglobal.rds.ui.manualEquip.getMaterialDiscountTime()
            extraCostDiscount = costData.get('extraCostDiscount', [])
            if remainDiscountTime and extraCostDiscount:
                extraCostData = costData.get('extraCostDiscount')
            else:
                extraCostData = costData['extraCost']
            extraCost = extraCostData[makeType - 1]
            if costDict.has_key(extraCost[0]):
                raise Exception(gameStrings.TEXT_IMPPLAYERITEM_1253 % (tgtEquipId, makeType))
            numRange = (extraCost[1], extraCost[1])
            costDict[extraCost[0]] = (numRange, True)
            for itemId, (numRange, enableParentCheck) in costDict.iteritems():
                numNeed = max(numRange)
                if not numNeed:
                    continue
                remain, res = self.inv.cntItemWithPlans(itemId, numNeed, enableParentCheck=enableParentCheck)
                if remain:
                    itemName = ID.data.get(itemId, {}).get('name', '')
                    if self.inv.hasItemExpireTTL(itemId, enableParentCheck=enableParentCheck):
                        bMsg and self.showGameMsg(GMDD.data.MAKE_EQUIP_MATERIAL_EXPIRED, (itemName,))
                    else:
                        if isSelectDiKou:
                            continue
                        bMsg and self.showGameMsg(GMDD.data.MAKE_EQUIP_MATERIAL_NOT_ENOUGH, (itemName,))
                    return

        if costData.has_key('cashNeed') and not self._canPayCash(costData['cashNeed']):
            bMsg and self.showGameMsg(GMDD.data.MAKE_EQUIP_CASH_NOT_ENOUGH, ())
            return
        if needBind:
            msg = GMD.data.get(GMDD.data.MAKE_MANUL_EQUIP_BIND, {}).get('text', gameStrings.TEXT_EQUIPCHANGESTARACTIVATEPROXY_450)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(BigWorld.player().cell.makeManualEquip, tgtEquipId, makeType))
        else:
            BigWorld.player().cell.makeManualEquip(tgtEquipId, makeType)

    def useZhuangshiItem(self, it, page, pos):
        morpher = avatarMorpher.AvatarModelMorpher(self.id, True)
        morpher.readConfig(self.avatarConfig)
        data = CID.data.get(it.id, {})
        newMaskCTex = data.get('zhuangshi', 1)
        ttl = data.get('zhuangshiTTL', 0)
        headMorpher = morpher.dyeMorpher.dyeMorphers.get('head', None)
        if headMorpher and headMorpher.transformMap.has_key('maskCTex'):
            headMorpher.transformMap['maskCTex'][1] = (newMaskCTex,)
            headMorpher.transformMap['facemask_power'][1] = (1.0,)
            headMorpher.transformMap['facemask_color'][1] = headMorpher.transformMap['facemask_color'][2]
            avatarConfig = morpher.export(self.avatarConfig)
            sm = strmap.strmap(avatarConfig)
            if ttl:
                sm.set('zhuangshiTTL', ttl + utils.getNow())
                self.zhuangshiTTL = ttl + utils.getNow()
            avatarConfig = zlib.compress(sm.__str__())
            self.cell.useCommonItemWithParam(page, pos, avatarConfig, 0)

    def checkAvatarZhuangshi(self):
        sm = strmap.strmap(self.avatarConfig)
        ttl = sm.get('zhuangshiTTL', 0)
        self.zhuangshiTTL = ttl
        if ttl and utils.getNow() >= ttl:
            morpher = avatarMorpher.AvatarModelMorpher(self.id, True)
            morpher.readConfig(self.avatarConfig)
            headMorpher = morpher.dyeMorpher.dyeMorphers.get('head', None)
            if headMorpher and headMorpher.transformMap.has_key('maskCTex'):
                headMorpher.transformMap['maskCTex'][1] = (1,)
                headMorpher.transformMap['facemask_power'][1] = (0.0,)
                avatarConfig = morpher.export(self.avatarConfig)
                sm = strmap.strmap(avatarConfig)
                sm.set('zhuangshiTTL', 0)
                avatarConfig = zlib.compress(sm.__str__())
                self.avatarConfig = avatarConfig
                self.cell.setAvatarConfig(avatarConfig)

    def showItemStateTimeWaste(self, page, pos):
        i = self.realInv.getQuickVal(page, pos)
        msg = GMD.data.get(GMDD.data.ITEM_STATE_TIME_WASTE, {}).get('text', gameStrings.TEXT_IMPPLAYERITEM_1326)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cell.useCommonItemWithParam, page, pos, 'bForce', True))

    def showDikouItemStateTimeWaste(self, itemId):
        msg = GMD.data.get(GMDD.data.ITEM_STATE_TIME_WASTE, {}).get('text', gameStrings.TEXT_IMPPLAYERITEM_1326)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cell.useCommonDikouItemWithParam, itemId, 'bForce', True))

    def updateEquipSoulSchemeData(self, schemeNo, data):
        self.equipSoulSchemeInfo[schemeNo] = data
        gameglobal.rds.ui.schemeSwitch.refreshInfo()
        gameglobal.rds.ui.equipSoul.refreshSchemeInfo()

    def getCurEquipSoulSchemeName(self):
        return self.getEquipSoulSchemeName(self.currEquipSoulSchemeNo)

    def getEquipSoulSchemeName(self, schemeNo):
        schemeName = self.equipSoulSchemeInfo.get(schemeNo, {}).get('name', '')
        if schemeName == '':
            schemeName = uiUtils.getDefaultSchemeName(uiConst.SCHEME_SWITCH_EQUIP_SOUL, schemeNo)
        return schemeName

    def getEquipSoulSchemeExpireTime(self, schemeNo):
        if schemeNo == const.EQUIP_SOUL_SCHEME_NO_VIP:
            addedPackageId = 10013
            expireTime = self.vipAddedPackage.get(addedPackageId, {}).get('tExpire', 0)
            if expireTime:
                return expireTime
        return self.equipSoulSchemeInfo.get(schemeNo, {}).get('expireTime', 0)

    def syncUseItemWish(self, wishInfo):
        self.useItemWish.update(wishInfo)
        needAddBuff = False
        for itemId in self.useItemWish:
            if self.useItemWish[itemId]:
                needAddBuff = True
                break

        if needAddBuff:
            stateId = SCD.data.get('itemWishBuffId', 0)
            if stateId:
                BigWorld.player().addFakeState(stateId)
        else:
            stateId = SCD.data.get('itemWishBuffId', 0)
            if stateId:
                BigWorld.player().quitFakeState(stateId)

    def itemWishConfirmInfoSend(self, info):
        try:
            data = cPickle.loads(info)
        except:
            data = {}

        self.itemWishConfirmInfo = data
