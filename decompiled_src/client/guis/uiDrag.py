#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/uiDrag.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import uiConst
import gamelog
import gametypes
import utils
import formula
from gamestrings import gameStrings
from helpers import cellCmd
from helpers import aspectHelper
from item import Item
from guis import ui
from callbackHelper import Functor
from guis import messageBoxProxy
from guis import uiUtils
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import general_skill_config_data as GSCD
from data import rune_data as RD
from data import sys_config_data as SCD
from data import item_data as ID

def getDargStartMethod(srcType):
    return '_start' + srcType[0].upper() + srcType[1:]


def getDargEndMethod(srcType, desType):
    if desType:
        return '_end' + srcType[0].upper() + srcType[1:] + 'To' + desType[0].upper() + desType[1:]
    else:
        return '_end' + srcType[0].upper() + srcType[1:] + 'ToNull'


def _startBagslot(nPageSrc, nItemSrc):
    if nPageSrc == uiConst.BAG_PAGE_QUEST:
        return
    if gameglobal.rds.ui.inventory.page != uiConst.BAG_PAGE_QUEST:
        if gameglobal.rds.ui.inventory.SynthesizeSrcItemPage == nPageSrc and gameglobal.rds.ui.inventory.SynthesizeSrcItemPos == nItemSrc or gameglobal.rds.ui.inventory.dyeItemPage == nPageSrc and gameglobal.rds.ui.inventory.dyeItemPos == nItemSrc:
            return
        gameglobal.rds.ui.inDragCommonItem = True
        gameglobal.rds.ui.dragInvPageSrc = nPageSrc
        gameglobal.rds.ui.dragInvItemSrc = nItemSrc
        sItem = BigWorld.player().inv.getQuickVal(nPageSrc, nItemSrc)
        if sItem != const.CONT_EMPTY_VAL and sItem.type in Item.BASETYPE_ITEM_ACTION_BAR:
            if not sItem.getPassiveUse():
                gameglobal.rds.ui.actionbar.setAllItemSlotVisible(True)
                gameglobal.rds.ui.actionbar.setNormalSlotsShine(True)
                gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_RED)
        else:
            gameglobal.rds.ui.actionbar.setAllSlotAlpha(uiConst.SKILL_ICON_STAT_RED)


def _startGuildStorage(nPageSrc, nItemSrc):
    gameglobal.rds.ui.inDragStorageItem = True
    gameglobal.rds.ui.dragGuildStoragePageSrc = nPageSrc
    gameglobal.rds.ui.dragGuildStorageItemSrc = nItemSrc


def _startFashionBag(nPageSrc, nItemSrc):
    gameglobal.rds.ui.inDragFashionBagItem = True
    gameglobal.rds.ui.dragFashionBagPageSrc = nPageSrc
    gameglobal.rds.ui.dragFashionBagItemSrc = nItemSrc


def _startEmote(nPageSrc, nItemSrc):
    gameglobal.rds.ui.actionbar.setAllItemSlotVisible(True)
    gameglobal.rds.ui.actionbar.setNormalSlotsShine(True)
    gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_RED)


def _startLifeSkill(nPageSrc, nItemSrc):
    gameglobal.rds.ui.actionbar.setAllItemSlotVisible(True)
    gameglobal.rds.ui.actionbar.setNormalSlotsShine(True)
    gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_RED)


def _startStorage(nPageSrc, nItemSrc):
    if nPageSrc != const.STORAGE_PAGE_BAG:
        gameglobal.rds.ui.inDragStorageItem = True
        gameglobal.rds.ui.dragStoragePageSrc = nPageSrc
        gameglobal.rds.ui.dragStorageItemSrc = nItemSrc


def _startMeterial(nPageSrc, nItemSrc):
    gameglobal.rds.ui.inDragMaterialBagItem = True
    gameglobal.rds.ui.dragMaterialBagPageSrc = nPageSrc
    gameglobal.rds.ui.dragMaterialBagItemSrc = nItemSrc


def _startSpriteMaterial(nPageSrc, nItemSrc):
    gameglobal.rds.ui.inDragSpriteMaterialBagItem = True
    gameglobal.rds.ui.dragSpriteMaterialBagPageSrc = nPageSrc
    gameglobal.rds.ui.dragSpriteMaterialBagItemSrc = nItemSrc


def _startSkillPanel(nPageSrc, nItemSrc):
    if nPageSrc == uiConst.SKILL_PANEL_SPECIAL_LEFT or nPageSrc == uiConst.SKILL_PANEL_SPECIAL_RIGHT:
        if nPageSrc == uiConst.SKILL_PANEL_SPECIAL_LEFT:
            skType = nItemSrc / 8
            gameglobal.rds.ui.actionbar.setSpecialSlotsShine(True, skType)
        else:
            gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_RED)
        gameglobal.rds.ui.actionbar.setNormalSlotState(uiConst.SKILL_ICON_STAT_RED)
        gameglobal.rds.ui.airbar.setAirSlotsState(uiConst.SKILL_ICON_STAT_RED)
        gameglobal.rds.ui.skill.setSpecialSlotsShine(True)
    elif nPageSrc in (uiConst.SKILL_PANEL_COMMON,
     uiConst.SKILL_PANEL_OTHER,
     uiConst.SKILL_PANEL_LIFE,
     uiConst.SKILL_PANEL_EXPLORE,
     uiConst.SKILL_PANEL_GUILD,
     uiConst.SKILL_PANEL_SOCIAL,
     uiConst.SKILL_PANEL_INTIMACY,
     uiConst.SKILL_PANEL_PUBG):
        gameglobal.rds.ui.actionbar.setAllItemSlotVisible(True)
        gameglobal.rds.ui.actionbar.setNormalSlotsShine(True)
        gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_RED)
        gameglobal.rds.ui.airbar.setAirSlotsState(uiConst.SKILL_ICON_STAT_RED)
    elif nPageSrc == uiConst.SKILL_PANEL_AIR_ORIG:
        if not (nItemSrc >= 0 and nItemSrc < uiConst.MAX_AIRBAR_SLOT_NUM):
            return
        gameglobal.rds.ui.actionbar.setNormalSlotState(uiConst.SKILL_ICON_STAT_RED)
        gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_RED)
        gameglobal.rds.ui.airbar.setAirSlotsShine(True)


def _startCrossBagSlot(nPageSrc, nItemSrc):
    gameglobal.rds.ui.inDragCommonItem = True
    gameglobal.rds.ui.dragCrossInvPageSrc = nPageSrc
    gameglobal.rds.ui.dragCrossInvItemSrc = nItemSrc
    sItem = BigWorld.player().crossInv.getQuickVal(nPageSrc, nItemSrc)
    if sItem != const.CONT_EMPTY_VAL and sItem.type in Item.BASETYPE_ITEM_ACTION_BAR:
        gameglobal.rds.ui.actionbar.setAllItemSlotVisible(True)
        gameglobal.rds.ui.actionbar.setNormalSlotsShine(True)
        gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_RED)
    else:
        gameglobal.rds.ui.actionbar.setAllSlotAlpha(uiConst.SKILL_ICON_STAT_RED)


def _startAirbar(nPageSrc, nItemSrc):
    if not (nItemSrc >= 0 and nItemSrc < uiConst.MAX_AIRBAR_SLOT_NUM):
        return
    gameglobal.rds.ui.actionbar.setNormalSlotState(uiConst.SKILL_ICON_STAT_RED)
    gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_RED)
    gameglobal.rds.ui.airbar.setAirSlotsShine(True)


def _startActionbar(nPageSrc, nItemSrc):
    gameglobal.rds.ui.inSchoolSwitch = BigWorld.player()._isSchoolSwitch()
    if not (nPageSrc == uiConst.SKILL_ACTION_BAR and nItemSrc >= uiConst.WUSHUANG_SKILL_START_POS_LEFT) and not nPageSrc == uiConst.EQUIP_ACTION_BAR:
        gameglobal.rds.ui.actionbar.setAllItemSlotVisible(True)
    if nPageSrc == uiConst.SKILL_ACTION_BAR:
        gameglobal.rds.ui.actionbar.mc.Invoke('setDraging', GfxValue(True))
    elif nPageSrc == uiConst.ITEM_ACTION_BAR:
        if gameglobal.rds.ui.actionbar.itemMc[0]:
            gameglobal.rds.ui.actionbar.itemMc[0].Invoke('setDraging', GfxValue(True))
    elif nPageSrc == uiConst.ITEM_ACTION_BAR2:
        if gameglobal.rds.ui.actionbar.itemMc[1]:
            gameglobal.rds.ui.actionbar.itemMc[1].Invoke('setDraging', GfxValue(True))
    if nPageSrc in (uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2):
        if nPageSrc == uiConst.SKILL_ACTION_BAR and nItemSrc < uiConst.WUSHUANG_SKILL_START_POS_LEFT or nPageSrc in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]:
            gameglobal.rds.ui.actionbar.setNormalSlotsShine(True)
            gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_RED)
            gameglobal.rds.ui.airbar.setAirSlotsState(uiConst.SKILL_ICON_STAT_RED)
        else:
            type = 0 if nItemSrc < uiConst.WUSHUANG_SKILL_START_POS_RIGHT else 1
            gameglobal.rds.ui.actionbar.setSpecialSlotsShine(True, type)
            gameglobal.rds.ui.actionbar.setNormalSlotState(uiConst.SKILL_ICON_STAT_RED)
    elif nPageSrc == uiConst.EQUIP_ACTION_BAR:
        gameglobal.rds.ui.actionbar.setNormalSlotsShine(True)
        gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_RED)


def _startSummonedWarSprite(nPageSrc, nItemSrc):
    gameglobal.rds.ui.actionbar.setAllItemSlotVisible(True)


def _startWingWorld(*args):
    gameglobal.rds.ui.actionbar.setAllItemSlotVisible(True)
    gameglobal.rds.ui.actionbar.setNormalSlotsShine(True)


def _startClanWarSkill(*args):
    gameglobal.rds.ui.actionbar.setAllItemSlotVisible(True)
    gameglobal.rds.ui.actionbar.setNormalSlotsShine(True)


def _endGuildStorageToGuildStorage(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    srcItem = p.guild.storage.getQuickVal(nPageSrc, nItemSrc)
    desItem = p.guild.storage.getQuickVal(nPageDes, nItemDes)
    if srcItem:
        if desItem:
            p.cell.storageGuildExchange(nPageSrc, nItemSrc, srcItem.uuid, srcItem.cwrap, nPageDes, nItemDes, desItem.uuid)
        else:
            p.cell.storageGuildExchange(nPageSrc, nItemSrc, srcItem.uuid, srcItem.cwrap, nPageDes, nItemDes, '')


def _endBagslotToWingAndMount(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.wingAndMount.moveItemFromBagIntoMine(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endBagslotToSpriteMaterial(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.spriteMaterialBag.dragBagSlotToSpriteMaterialBag(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endSpriteMaterialToSpriteMaterial(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.spriteMaterialBag.dragSpriteMaterialBagToSpriteMaterialBag(gameglobal.rds.ui.dragSpriteMaterialBagPageSrc, gameglobal.rds.ui.dragSpriteMaterialBagItemSrc, nPageDes, nItemDes)


def _endSpriteMaterialToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.spriteMaterialBag.dragSpriteMaterialBagToBagSlot(gameglobal.rds.ui.dragSpriteMaterialBagPageSrc, gameglobal.rds.ui.dragSpriteMaterialBagItemSrc, nPageDes, nItemDes)


def _endBagslotToEquipMixNew(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.equipMixNew.setNeedItem(nPageSrc, nItemSrc)


def _endFashionPropTransferToNull(nPageSrc, nItemSrc):
    gameglobal.rds.ui.fashionPropTransfer.removeItem(nPageSrc, nItemSrc)


def _endBagslotToFashionPropTransfer(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.fashionPropTransfer.setItem(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endBagslotToEquipPropTransfer(nPageSrc, nItemSrc, nPageDes, nItemDes):
    pass


def _endEquipPropTransferToNull(nPageSrc, nItemSrc):
    pass


def _endWingAndMountToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if nItemSrc == 0:
        if nPageSrc == 0 or nPageSrc == 1:
            if nPageSrc == 0:
                type = gametypes.EQU_PART_RIDE
            else:
                type = gametypes.EQU_PART_WINGFLY
            cellCmd.exchangeInvEqu(nPageDes, nItemDes, type)
    else:
        item = p.inv.getQuickVal(nPageDes, nItemDes)
        if not item:
            BigWorld.player().cell.rideWingBag2inv(nPageSrc, nItemSrc - 1, 1, nPageDes, nItemDes)
        else:
            p.showGameMsg(GMDD.data.CAN_NOT_EXCHANGE_TO_SLOT_ITEM, ())


def _endWingAndMountToWingAndMount(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if nItemSrc == 0 or nItemDes == 0:
        if nItemSrc == 0:
            if nPageSrc == 0:
                type = gametypes.EQU_PART_RIDE
            else:
                type = gametypes.EQU_PART_WINGFLY
            cellCmd.equipRideWingBag(nPageDes, nItemDes - 1, type)
        if nItemDes == 0:
            if nPageDes == 0:
                type = gametypes.EQU_PART_RIDE
            else:
                type = gametypes.EQU_PART_WINGFLY
            cellCmd.equipRideWingBag(nPageSrc, nItemSrc - 1, type)
    else:
        p.base.rideWingBag2rideWingBag(nPageSrc, nItemSrc - 1, 1, nPageDes, nItemDes - 1)


def _endBagslotToWAMUpGrade(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if nPageDes == 0 and nItemDes == 0:
        gameglobal.rds.ui.wingAndMountUpgrade.setItem(const.RES_KIND_INV, nPageSrc, nItemSrc)


def _endWAMUpGradeToNull(nPageSrc, nItemSrc):
    if nPageSrc == 0 and nItemSrc == 0:
        gameglobal.rds.ui.wingAndMountUpgrade.setItem(const.RES_KIND_INV, const.CONT_NO_PAGE, const.CONT_NO_POS)


def _endBagslotToGuildStorage(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.guildStorage.invItemToGuildStorage(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endBagslotToHuizhangRepair(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if gameglobal.rds.ui.sItem and nItemDes == 0:
        srcItem = gameglobal.rds.ui.sItem
        gameglobal.rds.ui.huiZhangRepair.setRepairHuiZhang(nPageSrc, nItemSrc, srcItem)


def _endGuildStorageToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    srcItem = p.guild.storage.getQuickVal(nPageSrc, nItemSrc)
    if srcItem:
        if srcItem.cwrap > 1:
            gameglobal.rds.ui.inventory.showNumberInputWidget(uiConst.WIDGET_GUILD_STORAGE, nPageSrc, nItemSrc, -1, nPageDes, nItemDes)
        else:
            p.cell.storageGuild2inv(nPageSrc, nItemSrc, srcItem.uuid, srcItem.cwrap, srcItem.id, nPageDes, nItemDes)


def _endPickUpToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.pickUp.pickOneItem(nItemSrc, nPageDes, nItemDes)


def _endSpriteMaterialToNull(nPageSrc, nItemSrc):
    if gameglobal.rds.ui.sItem == const.CONT_EMPTY_VAL:
        return


def _endBagslotToNull(nPageSrc, nItemSrc):
    if gameglobal.rds.ui.sItem == const.CONT_EMPTY_VAL:
        return
    if gameglobal.rds.ui.equipChange.mediator:
        BigWorld.player().showGameMsg(GMDD.data.FORBIDDEN_BY_EQUIP_CHANGE_PANEL_OPEN, ())
        return
    if gameglobal.rds.ui.manualEquipLvUp.widget:
        BigWorld.player().showGameMsg(GMDD.data.FORBIDEN_BY_MANUAL_EQUIP_LV_UP_OPEN, ())
        return
    if gameglobal.rds.ui.dragInvPageSrc == nPageSrc and gameglobal.rds.ui.dragInvItemSrc == nItemSrc:
        gameglobal.rds.ui.inventory.addItem(gameglobal.rds.ui.sItem, nPageSrc, nItemSrc)
    if not BigWorld.player().life:
        msg = GMD.data.get(GMDD.data.ITEM_CANNOT_DROP, {}).get('text', '')
        it = BigWorld.player().inv.getQuickVal(nPageSrc, nItemSrc)
        msg = msg % it.name
        BigWorld.player().showTopMsg(msg)
        return
    if gameglobal.rds.ui.sItem.isPrecious():
        gameglobal.rds.ui.doubleCheckWithInput.show(gameStrings.TEXT_UIDRAG_310, 'DELETE', title=gameStrings.TEXT_DIGONGPROXY_207_4, confirmCallback=gameglobal.rds.ui.inventory.confirmDiscard, cancelCallback=gameglobal.rds.ui.inventory.cancelDiscard)
    else:
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(gameglobal.rds.ui.inventory.confirmDiscard)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, Functor(gameglobal.rds.ui.inventory.cancelDiscard))]
        if gameglobal.rds.ui.sItem.isRuneEquip() and getattr(gameglobal.rds.ui.sItem, 'runeData', ()):
            dropConfirmText = gameStrings.TEXT_UIDRAG_317
        else:
            it = BigWorld.player().inv.getQuickVal(nPageSrc, nItemSrc)
            name = uiUtils.toHtml(it.name, '#cc2929')
            if gameglobal.rds.ui.sItem.isGuanYin() and len(gameglobal.rds.ui.sItem.getAllGuanYinPskill()) > 0:
                dropConfirmText = uiUtils.getTextFromGMD(GMDD.data.GUAN_YIN_DISCARD_HINT, gameStrings.TEXT_UIDRAG_322) % name
            else:
                dropConfirmText = gameStrings.TEXT_UIDRAG_324 % name
        dropMBId = gameglobal.rds.ui.messageBox.show(True, '', dropConfirmText, buttons, False, 0, uiConst.MESSAGEBOX_INVENTORY)
        gameglobal.rds.ui.inventory.dropMBIds.append(dropMBId)
    gameglobal.rds.ui.inventory.nPageSrc = nPageSrc
    gameglobal.rds.ui.inventory.nItemSrc = nItemSrc


def _endActionbarToNull(nPageSrc, nItemSrc):
    p = BigWorld.player()
    if nPageSrc in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]:
        if gameglobal.rds.ui.inSchoolSwitch != p._isSchoolSwitch():
            return
        if gameglobal.rds.ui.trade.isShow:
            return
        if p._isSchoolSwitch():
            return
        gameglobal.rds.ui.actionbar.discardItem(nPageSrc, nItemSrc, False, False)
    elif nPageSrc == uiConst.SKILL_ACTION_BAR:
        if p._isSchoolSwitch():
            return
        if nItemSrc >= uiConst.WUSHUANG_SKILL_START_POS_LEFT:
            gameglobal.rds.ui.skill.unEquipSpecialSkill(nPageSrc, nItemSrc)
            return
        gameglobal.rds.ui.actionbar.removeItem(nPageSrc, nItemSrc, False)
    elif nPageSrc == uiConst.EQUIP_ACTION_BAR:
        if p.isInPUBG():
            if not p.life:
                msg = GMD.data.get(GMDD.data.ITEM_CANNOT_DROP, {}).get('text', '')
                it = p.crossInv.getQuickVal(nPageSrc, nItemSrc)
                p.showTopMsg(msg % it.name)
                return
            p.cell.discardItem(nPageSrc, nItemSrc, 1)
            gameglobal.rds.sound.playSound(gameglobal.SD_2)


def _endSackslotToNull(nPageSrc, nItemSrc):
    if nPageSrc == const.TEMP_BAG_BIND_ID:
        BigWorld.player().showGameMsg(GMDD.data.ITEM_TEMP_BAG_FORBIDDEN_DROP, ())


def _endFishingToNull(nPageSrc, nItemSrc):
    posMap = {0: gametypes.FISHING_EQUIP_BAIT,
     1: gametypes.FISHING_EQUIP_ROD,
     2: gametypes.FISHING_EQUIP_BUOY,
     3: gametypes.FISHING_EQUIP_HOOK}
    if posMap.has_key(nItemSrc):
        BigWorld.player().cell.setConsumableFishingEquip(posMap[nItemSrc], 0)


def _endMailToNull(nPageSrc, nItemSrc):
    if nPageSrc == uiConst.MAIL_SEND:
        gameglobal.rds.ui.mail.removeItem(nPageSrc, nItemSrc)


def _endConsignToNull(nPageSrc, nItemSrc):
    gameglobal.rds.ui.consign.removeItem(nPageSrc, nItemSrc)


def _endTabAuctionConsignToNull(nPageSrc, nItemSrc):
    gameglobal.rds.ui.tabAuctionConsign.removeItem(nPageSrc, nItemSrc)


def _endTabAuctionCrossServerToNull(nPageSrc, nItemSrc):
    gameglobal.rds.ui.tabAuctionCrossServer.removeItem(nPageSrc, nItemSrc)


def _endEquipFeedToNull(nPageSrc, nItemSrc):
    gameglobal.rds.ui.equipFeed.removeItem(nPageSrc, nItemSrc)


def _endEquipFuncToNull(nPageSrc, nItemSrc):
    if nPageSrc == uiConst.EQUIP_FUNC_ENHANCE or nItemSrc in (0, 1):
        pass


def _endEquipEnhanceToNull(nPageSrc, nItemSrc):
    if nPageSrc == uiConst.EQUIP_FUNC_ENHANCE or nItemSrc in (0, 1):
        gameglobal.rds.ui.equipEnhance.removeItem(nPageSrc, nItemSrc)


def _endAirbarToAirbar(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.airbar.airbar2Airbar(nItemSrc, nItemDes)


def _endAirbarToNull(nPageSrc, nItemSrc):
    gameglobal.rds.ui.airbar.airbar2Null(nItemSrc)


def _endActionbarToActionbar(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if gameglobal.rds.ui.inSchoolSwitch != BigWorld.player()._isSchoolSwitch():
        return
    if nPageSrc == uiConst.EQUIP_ACTION_BAR and nPageDes in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]:
        if BigWorld.player()._isSchoolSwitch():
            return
        item = uiUtils.getEquipItemById(nItemSrc)
        if item == const.CONT_EMPTY_VAL:
            return
        if item.type in Item.BASETYPE_ITEM_ACTION_BAR:
            if gameglobal.rds.ui.trade.isShow:
                return
            if gameglobal.rds.ui.actionbar.isItemBarInEdit():
                return
            gameglobal.rds.ui.actionbar.dragItemFromEquipBar(item, nPageDes, nItemDes)
        else:
            BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_DRAG, ())
            return
    elif nPageSrc == uiConst.EQUIP_ACTION_BAR and nPageDes == uiConst.SKILL_ACTION_BAR:
        if nItemDes >= uiConst.WUSHUANG_SKILL_START_POS_LEFT:
            return
        item = uiUtils.getEquipItemById(nItemSrc)
        if item:
            gameglobal.rds.ui.actionbar.dragItemFromEquipBar(item, nPageDes, nItemDes)
    if nPageSrc != nPageDes:
        if not gameglobal.rds.ui.actionbar.getShortCut(nPageSrc, nItemSrc):
            return
        nSrcID = gameglobal.rds.ui.actionbar.getShortCut(nPageSrc, nItemSrc)[1]
        sType = gameglobal.rds.ui.actionbar.getShortCut(nPageSrc, nItemSrc)[0]
        bagPage, bagPos = BigWorld.player().inv.findItemInPages(nSrcID, includeExpired=True, includeLatch=True, includeShihun=True)
        if bagPage != const.CONT_NO_PAGE:
            i = BigWorld.player().inv.getQuickVal(bagPage, bagPos)
        elif sType in uiConst.SHORTCUT_TYPE_ITEM:
            i = Item(nSrcID)
        else:
            i = nSrcID
            p = BigWorld.player()
            nSrcID = gameglobal.rds.ui.actionbar.getActionIDByPos(nPageSrc, nItemSrc)
            if p.skillQteData.has_key(nSrcID):
                return
        if nPageDes in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2] and nPageSrc == uiConst.SKILL_ACTION_BAR or nPageDes == uiConst.SKILL_ACTION_BAR and nPageSrc in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2] or nPageDes in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2] and nPageSrc in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]:
            if nPageSrc == uiConst.SKILL_ACTION_BAR and nItemSrc >= uiConst.WUSHUANG_SKILL_START_POS_LEFT:
                BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_DRAG, ())
                return
            if nPageDes == uiConst.SKILL_ACTION_BAR and nItemDes >= uiConst.WUSHUANG_SKILL_START_POS_LEFT:
                BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_DRAG, ())
                return
            if gameglobal.rds.ui.trade.isShow:
                return
            gameglobal.rds.ui.actionbar.moveItem(nPageSrc, nItemSrc, nPageDes, nItemDes)
            return
        if nPageDes == uiConst.SKILL_ACTION_BAR and nItemDes < uiConst.WUSHUANG_SKILL_START_POS_LEFT:
            if gameglobal.rds.ui.trade.isShow or type(i) == Item or i in gameglobal.rds.ui.actionbar.otherSkill + gameglobal.rds.ui.actionbar.lifeSkill:
                return
            gameglobal.rds.ui.actionbar.setItem(i, nPageDes, nItemDes, False, False, sType)
        gameglobal.rds.ui.actionbar.setItem(i, nPageSrc, nItemSrc, False, False, sType)
        return
    if nPageSrc == uiConst.SKILL_ACTION_BAR:
        p = BigWorld.player()
        nSrcID = gameglobal.rds.ui.actionbar.getActionIDByPos(nPageSrc, nItemSrc)
        if p.skillQteData.has_key(nSrcID):
            return
        if nItemSrc < uiConst.WUSHUANG_SKILL_START_POS_LEFT and nItemDes >= uiConst.WUSHUANG_SKILL_START_POS_LEFT or nItemSrc >= uiConst.WUSHUANG_SKILL_START_POS_LEFT and nItemDes < uiConst.WUSHUANG_SKILL_START_POS_LEFT:
            return
        if nItemSrc >= uiConst.WUSHUANG_SKILL_START_POS_LEFT and nItemDes >= uiConst.WUSHUANG_SKILL_START_POS_LEFT:
            if nItemSrc >= uiConst.WUSHUANG_SKILL_START_POS_RIGHT and nItemDes < uiConst.WUSHUANG_SKILL_START_POS_RIGHT or nItemSrc < uiConst.WUSHUANG_SKILL_START_POS_RIGHT and nItemDes >= uiConst.WUSHUANG_SKILL_START_POS_RIGHT:
                gameglobal.rds.ui.actionbar.setItem(nSrcID, nPageSrc, nItemSrc, False, False, uiConst.SHORTCUT_TYPE_SKILL)
                return
            page = uiConst.SKILL_PANEL_SPECIAL_RIGHT
            srcSlot = nItemSrc - uiConst.WUSHUANG_SKILL_START_POS_LEFT
            desSlot = nItemDes - uiConst.WUSHUANG_SKILL_START_POS_LEFT
            gameglobal.rds.ui.skill.wushuangSkillDragFromSlot2Slot(page, srcSlot, page, desSlot)
            gameglobal.rds.ui.actionbar.setSpecialSlotShine()
            return
        gameglobal.rds.ui.actionbar.moveItem(nPageSrc, nItemSrc, nPageDes, nItemDes)
    elif nPageSrc in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]:
        p = BigWorld.player()
        nSrcID = gameglobal.rds.ui.actionbar.getActionIDByPos(nPageSrc, nItemSrc)
        if p.skillQteData.has_key(nSrcID):
            return
        if gameglobal.rds.ui.trade.isShow:
            return
        gameglobal.rds.ui.actionbar.moveItem(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endStorageToStorage(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if gameglobal.rds.ui.storage.npcId and BigWorld.entities.get(gameglobal.rds.ui.storage.npcId):
        p = BigWorld.player()
        ent = BigWorld.entities.get(gameglobal.rds.ui.storage.npcId)
        if nPageSrc != const.STORAGE_PAGE_BAG:
            sItem = p.storage.getQuickVal(nPageSrc, nItemSrc)
            if sItem:
                if nPageDes != const.STORAGE_PAGE_BAG:
                    ent.cell.storage2storage(nPageSrc, nItemSrc, sItem.cwrap, nPageDes, nItemDes)
                elif sItem.type != Item.BASETYPE_PACK:
                    p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_NOT_BAG, ())
                elif nItemDes < p.storage.enabledPackSlotCnt:
                    ent.cell.storage2StorageSlot(nPageSrc, nItemSrc, nItemDes)
        elif nPageSrc == const.STORAGE_PAGE_BAG and nPageDes == const.STORAGE_PAGE_BAG:
            BigWorld.player().base.toStorageSlot2StorageSlot(nItemSrc, nItemDes)
        else:
            sItem = p.storageBar.getQuickVal(0, nItemSrc)
            if sItem:
                if nPageDes != const.STORAGE_PAGE_BAG:
                    dItem = p.storage.getQuickVal(nPageDes, nItemDes)
                    if dItem and dItem.type != Item.BASETYPE_PACK:
                        p.showGameMsg(GMDD.data.ITEM_UNEQUIPPACK_FORBIDDEN_POS, ())
                    else:
                        ent.cell.storageSlot2Storage(nItemSrc, nPageDes, nItemDes)


def _endBagslotToStorage(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if gameglobal.rds.ui.sItem == const.CONT_EMPTY_VAL:
        return
    if gameglobal.rds.ui.storage.npcId and gameglobal.rds.ui.sItem and BigWorld.entities.get(gameglobal.rds.ui.storage.npcId):
        p = BigWorld.player()
        if gameglobal.rds.ui.inventory.page == uiConst.BAG_PAGE_QUEST:
            p.showGameMsg(GMDD.data.ITEM_CAN_NOT_MOVE_TO_STORAGE, ())
            return
        ent = BigWorld.entities.get(gameglobal.rds.ui.storage.npcId)
        if nPageDes == const.STORAGE_PAGE_BAG:
            if nItemDes < BigWorld.player().storage.enabledPackSlotCnt:
                ent.cell.inv2StorageSlot(nPageSrc, nItemSrc, nItemDes)
            else:
                p.showGameMsg(GMDD.data.STORAGE_UNLOCK_PACK_EQUIP_FORBIDDEN, ())
        else:
            dItem = p.storage.getQuickVal(nPageDes, nItemDes)
            if dItem:
                p.showGameMsg(GMDD.data.STORAGE_FORBIDDEN_DRAG, ())
            else:
                ent.cell.inv2storage(nPageSrc, nItemSrc, gameglobal.rds.ui.sItem.cwrap, nPageDes, nItemDes)


def _endBagslotToEquipSuit(nPageSrc, nItemSrc, nPageDes, nItemDes):
    it = BigWorld.player().inv.getQuickVal(nPageSrc, nItemSrc)
    gameglobal.rds.ui.equipSuit.setItem(nPageSrc, nItemSrc, uiConst.EQUIP_STAR_ACTIVATE, 0, it)
    gameglobal.rds.ui.inventory.updateCurrentPageSlotState()


def _endEquipSuitToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.equipSuit.onResetEquipSlot()


def _endEquipSuitToActionbar(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if nPageDes != uiConst.EQUIP_ACTION_BAR:
        return
    gameglobal.rds.ui.equipSuit.onResetEquipSlot()


def _endEquipSuitToNull(nPageSrc, nItemSrc):
    gameglobal.rds.ui.equipSuit.onResetEquipSlot()


def _endFashionBagToDyePlane(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    i = p.fashionBag.getQuickVal(nPageSrc, nItemSrc)
    if i and i.isCanDye():
        gameglobal.rds.ui.dyePlane.setEquip(nPageSrc, nItemSrc, i, const.RES_KIND_FASHION_BAG)


def _endBagslotToDyePlane(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    i = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if i:
        gameglobal.rds.ui.dyePlane.setEquip(nPageSrc, nItemSrc, i, const.RES_KIND_INV)


def _endBagslotToDyeReset(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    i = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if i:
        gameglobal.rds.ui.dyeReset.setEquip(nPageSrc, nItemSrc, i, const.RES_KIND_INV)


def _endFashionBagToDyeReset(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    i = p.fashionBag.getQuickVal(nPageSrc, nItemSrc)
    if i:
        gameglobal.rds.ui.dyeReset.setEquip(nPageSrc, nItemSrc, i, const.RES_KIND_FASHION_BAG)


def _endDyePlaneToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    pass


def _endStorageToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if gameglobal.rds.ui.storage.npcId and BigWorld.entities.get(gameglobal.rds.ui.storage.npcId):
        p = BigWorld.player()
        if nPageSrc != const.STORAGE_PAGE_BAG:
            sItem = p.storage.getQuickVal(nPageSrc, nItemSrc)
            if sItem:
                if sItem.isOneQuest() and gameglobal.rds.ui.inventory.page == uiConst.BAG_PAGE_QUEST or not sItem.isOneQuest() and gameglobal.rds.ui.inventory.page != uiConst.BAG_PAGE_QUEST:
                    dItem = p.inv.getQuickVal(nPageDes, nItemDes)
                    if dItem:
                        p.showGameMsg(GMDD.data.STORAGE_FORBIDDEN_DRAG, ())
                    else:
                        gameglobal.rds.ui.storage.gotoStorage2inv(nPageSrc, nItemSrc, sItem.id, sItem.cwrap, nPageDes, nItemDes)
        else:
            sItem = p.storageBar.getQuickVal(0, nItemSrc)
            if sItem and gameglobal.rds.ui.inventory.page != uiConst.BAG_PAGE_QUEST:
                dItem = p.inv.getQuickVal(nPageDes, nItemDes)
                if dItem:
                    p.showGameMsg(GMDD.data.STORAGE_FORBIDDEN_DRAG, ())
                else:
                    gameglobal.rds.ui.storage.gotoStorageSlot2Inv(nItemSrc, sItem.id, nPageDes, nItemDes)


@ui.checkEquipChangeOpen()
def _endBagslotToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if gameglobal.rds.configData.get('enableBindItemConvert', False):
        p = BigWorld.player()
        srcIt = BigWorld.player().inv.getQuickVal(nPageSrc, nItemSrc)
        targetIt = BigWorld.player().inv.getQuickVal(nPageDes, nItemDes)
        if srcIt and targetIt:
            if not srcIt.hasLatch() and not targetIt.hasLatch() and utils.checkValuableTradeItem(targetIt) and utils.checkValuableTradeItem(srcIt):
                allBind = False
                if srcIt.isForeverBind() and targetIt.isForeverBind():
                    allBind = True
                if srcIt.getBindConvertId() == targetIt.id or targetIt.getBindConvertId() == srcIt.id:
                    if srcIt.getBindConvertId() == targetIt.id:
                        page = nPageSrc
                        pos = nItemSrc
                        itemId = srcIt.id
                    else:
                        page = nPageDes
                        pos = nItemDes
                        itemId = targetIt.id
                    if allBind:
                        bindHint = uiUtils.getTextFromGMD(GMDD.data.CHANGE_BIND_CONFIRM, gameStrings.TEXT_INVENTORYPROXY_1418) % uiUtils.getItemColorName(itemId)
                    else:
                        bindHint = uiUtils.getTextFromGMD(GMDD.data.CHANGE_UNBIND_CONFIRM, gameStrings.TEXT_INVENTORYPROXY_1418) % uiUtils.getItemColorName(itemId)
                    if gameglobal.rds.ui.sItem:
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(bindHint, Functor(p.cell.convertBindItem, page, pos), noCallback=Functor(cellCmd.exchangeInv, nPageSrc, nItemSrc, gameglobal.rds.ui.sItem.cwrap, nPageDes, nItemDes))
                    else:
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(bindHint, Functor(p.cell.convertBindItem, page, pos))
                    return
        if gameglobal.rds.ui.sItem:
            cellCmd.exchangeInv(nPageSrc, nItemSrc, gameglobal.rds.ui.sItem.cwrap, nPageDes, nItemDes)
    elif gameglobal.rds.ui.sItem:
        cellCmd.exchangeInv(nPageSrc, nItemSrc, gameglobal.rds.ui.sItem.cwrap, nPageDes, nItemDes)


@ui.checkItemIsLock([0, 1])
def _endBagslotToTrade(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.trade.setInventoryItem(nPageSrc, nItemSrc, nPageDes, nItemDes)


@ui.checkItemIsLock([0, 1])
def _endBagslotToBindItemTrade(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.bindItemTrade.onBagSlotToBindItemSlot(nPageSrc, nItemSrc, nItemDes)


def _endBindItemTradeToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.bindItemTrade.revertGiveItem(nItemSrc)


@ui.checkItemIsLock([0, 1])
def _endBagslotToBooth(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.booth.onSetItem(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endBoothToBooth(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if not gameglobal.rds.ui.booth.boothType:
        return
    p = BigWorld.player()
    it = BigWorld.player().booth.getQuickVal(nPageSrc, nItemSrc)
    if not it:
        return
    if nPageDes == uiConst.BOOTH_SLOTS_SELL:
        p.cell.moveBoothSellItem(nPageSrc, nItemSrc, nPageDes, nItemDes, it.cwrap)
    elif nPageDes == uiConst.BOOTH_SLOTS_BUY:
        p.cell.moveBoothBuyItem(nPageSrc, nItemSrc, nPageDes, nItemDes, it.cwrap)


def _endBoothToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if gameglobal.rds.ui.booth.boothType:
        if nPageSrc == uiConst.BOOTH_SLOTS_SELL:
            gameglobal.rds.ui.booth.startCancelSell(nPageSrc, nItemSrc)
        elif nPageSrc == uiConst.BOOTH_SLOTS_BUY:
            BigWorld.player().cell.delBoothBuyItem(nPageSrc, nItemSrc)
    elif nPageSrc == uiConst.BOOTH_SLOTS_SELL:
        gameglobal.rds.ui.booth.startBuy(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endBoothToNull(nPageSrc, nItemSrc):
    if not gameglobal.rds.ui.booth.boothType:
        return
    p = BigWorld.player()
    it = p.booth.getQuickVal(nPageSrc, nItemSrc)
    if nPageSrc == uiConst.BOOTH_SLOTS_SELL:
        it and p.cell.revertBoothSellItem(nPageSrc, nItemSrc, it.cwrap)
    elif nPageSrc == uiConst.BOOTH_SLOTS_BUY:
        p.cell.delBoothBuyItem(nPageSrc, nItemSrc)


def _endBagslotToPayBag(nPageSrc, nItemSrc, nPageDes, nItemDes):
    it = BigWorld.player().inv.getQuickVal(nPageSrc, nItemSrc)
    gameglobal.rds.ui.inventory.addItem(it, nPageSrc, nItemSrc)
    gameglobal.rds.ui.payItem.setItem(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endFashionBagToActionbar(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if gameglobal.rds.ui.sItem == const.CONT_EMPTY_VAL:
        return
    if nPageDes == uiConst.EQUIP_ACTION_BAR:
        if BigWorld.player()._isSchoolSwitch():
            return
        cellCmd.exchangeFashionBagEqu(nPageSrc, nItemSrc, nItemDes)


def _endBagslotToActionbar(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if gameglobal.rds.ui.sItem == const.CONT_EMPTY_VAL:
        return
    item = gameglobal.rds.ui.sItem
    if nPageDes in (uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2):
        if item.type in Item.BASETYPE_ITEM_ACTION_BAR:
            if gameglobal.rds.ui.trade.isShow:
                return
            if gameglobal.rds.ui.actionbar.isItemBarInEdit():
                return
            if nPageDes == uiConst.SKILL_ACTION_BAR and nItemDes >= uiConst.WUSHUANG_SKILL_START_POS_LEFT:
                return
            gameglobal.rds.ui.actionbar.dragItemFromBag(item, nPageSrc, nItemSrc, nPageDes, nItemDes)
        else:
            BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_DRAG, ())
            return
    elif nPageDes == uiConst.EQUIP_ACTION_BAR:
        if BigWorld.player()._isSchoolSwitch():
            return
        cellCmd.exchangeInvEqu(nPageSrc, nItemSrc, nItemDes)


@ui.checkEquipChangeOpen()
def _endBagslotToSackslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if srcItem == const.CONT_EMPTY_VAL:
        return
    if nPageDes == const.BAG_BAR_BIND_ID:
        if srcItem.type != Item.BASETYPE_PACK or nItemDes >= const.BAG_BAR_WIDTH:
            return
        if nItemDes >= gameglobal.rds.ui.inventory.invBagSlot:
            p.showGameMsg(GMDD.data.UNLOCK_PACK_EQUIP_FORBIDDEN, ())
            return
        cellCmd.equipPack(nPageSrc, nItemSrc, nItemDes)
    elif nPageDes == const.MATERIAL_BAG_BIND_ID:
        if srcItem.type != Item.BASETYPE_MATERIAL:
            p.showGameMsg(GMDD.data.ITEM_MATERIAL_INV_PICK_FORBIDDEN, ())
            return
        p.base.inv2materialBag(nPageSrc, nItemSrc, srcItem.cwrap, 0, nItemDes)
    elif nPageDes == const.FASHION_BAG_BIND_ID:
        if srcItem.type != Item.BASETYPE_FASHION:
            p.showGameMsg(GMDD.data.ITEM_COMMODE_PICK_FORBIDDEN, ())
            return
        p.cell.inv2fashionBag(nPageSrc, nItemSrc, srcItem.cwrap, 0, nItemDes)
    elif nPageDes == const.TEMP_BAG_BIND_ID:
        p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_TO_TEMP_BAG, ())
    elif nPageDes == const.MALL_BAR_BIND_ID:
        p.showTopMsg(gameStrings.TEXT_UIDRAG_784)


def _endStorageToSackslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    srcItem = p.storage.getQuickVal(nPageSrc, nItemSrc)
    if srcItem == const.CONT_EMPTY_VAL:
        return
    if nPageDes in (const.MATERIAL_BAG_BIND_ID, const.FASHION_BAG_BIND_ID, const.TEMP_BAG_BIND_ID):
        p.showGameMsg(GMDD.data.STORAGE_FORBIDDEN_TO_OTHERBAG, ())


def _endSackslotToStorage(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    itemSrc = None
    if nPageSrc == const.TEMP_BAG_BIND_ID:
        itemSrc = p.tempBag.getQuickVal(0, nItemSrc)
    elif nPageSrc == const.MATERIAL_BAG_BIND_ID:
        itemSrc = p.materialBag.getQuickVal(0, nItemSrc)
    elif nPageSrc == const.FASHION_BAG_BIND_ID:
        itemSrc = p.fashionBag.getQuickVal(0, nItemSrc)
    if itemSrc:
        p.showGameMsg(GMDD.data.OTHERBAG_FORBIDDEN_TO_STORAGE, ())


def _endFashionToFashion(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if nItemSrc != nItemDes and nItemSrc in (26, 27) and nItemDes in (26, 27):
        p.cell.exchangeFashionEquip(nItemSrc, nItemDes)


def _endMyClothToMyCloth(nPageSrc, fromPart, nPageDes, toPart):
    fromPart = int(fromPart)
    toPart = int(toPart)
    if fromPart != toPart and fromPart in (26, 27) and toPart in (26, 27):
        aspectHelper.getInstance().exchangeEquip(fromPart, toPart)


def _endBagslotToFashion(nPageSrc, nItemSrc, nPageDes, nItemDes):
    item = gameglobal.rds.ui.sItem
    if item == const.CONT_EMPTY_VAL:
        return
    cellCmd.exchangeInvEqu(nPageSrc, nItemSrc, nItemDes)


@ui.checkEquipChangeOpen()
def _endBagslotToFashionBag(nPageSrc, nItemSrc, nPageDes, nItemDes):
    item = gameglobal.rds.ui.sItem
    p = BigWorld.player()
    if item == const.CONT_EMPTY_VAL:
        return
    if nPageDes == const.FASHION_BAG_PAGE_BAG:
        if nItemDes < BigWorld.player().fashionBag.enabledPackSlotCnt:
            p.base.toInv2FashionBagSlot(nPageSrc, nItemSrc, nItemDes)
        else:
            p.showGameMsg(GMDD.data.UNLOCK_FASHIONPACK_SLOT_FORBIDDEN, ())
    else:
        p.base.inv2fashionBag(nPageSrc, nItemSrc, 1, nPageDes, nItemDes)


def _endBagslotToShiHunRepair(nPageSrc, nItemSrc, nPageDes, nItemDes):
    item = gameglobal.rds.ui.sItem
    if item == const.CONT_EMPTY_VAL:
        return


@ui.checkEquipChangeOpen()
def _endFashionBagToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if nPageSrc != const.FASHION_BAG_PAGE_BAG:
        item = p.fashionBag.getQuickVal(nPageSrc, nItemSrc)
    else:
        item = p.fashionBagBar.getQuickVal(nPageSrc, nItemSrc)
    if item == const.CONT_EMPTY_VAL:
        return
    if nPageSrc != const.FASHION_BAG_PAGE_BAG:
        p.cell.fashionBag2inv(nPageSrc, nItemSrc, 1, nPageDes, nItemDes)
    else:
        sItem = p.fashionBagBar.getQuickVal(0, nItemSrc)
        if sItem and gameglobal.rds.ui.inventory.page != uiConst.BAG_PAGE_QUEST:
            dItem = p.inv.getQuickVal(nPageDes, nItemDes)
            if dItem:
                p.showGameMsg(GMDD.data.STORAGE_FORBIDDEN_DRAG, ())
            else:
                p.cell.toFashionBagSlot2Inv(nItemSrc, sItem.id, nPageDes, nItemDes)


def _endFashionBagToFashionBag(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if nPageDes == const.FASHION_BAG_PAGE_BAG and nPageSrc == const.FASHION_BAG_PAGE_BAG:
        p.base.fashionBagSlot2FashionBagSlot(nItemSrc, nItemDes)
    elif nPageDes != const.FASHION_BAG_PAGE_BAG and nPageSrc != const.FASHION_BAG_PAGE_BAG:
        item = p.fashionBag.getQuickVal(nPageSrc, nItemSrc)
        if item == const.CONT_EMPTY_VAL:
            return
        p.base.fashionBag2fashionBag(nPageSrc, nItemSrc, 1, nPageDes, nItemDes)


def _endBagslotToFishing(nPageSrc, nItemSrc, nPageDes, nItemDes):
    item = gameglobal.rds.ui.sItem
    if item == const.CONT_EMPTY_VAL:
        return
    if getattr(item, 'cstype', 0) == Item.SUBTYPE_2_FISHING_BAIT:
        if item.canEquipFishing(BigWorld.player().fishingLv, gametypes.FISHING_EQUIP_BAIT) == Item.EQUIPABLE:
            BigWorld.player().cell.setConsumableFishingEquip(nItemDes + 3, item.id)
    else:
        posMap = {0: gametypes.FISHING_EQUIP_BAIT,
         1: gametypes.FISHING_EQUIP_ROD,
         2: gametypes.FISHING_EQUIP_BUOY,
         3: gametypes.FISHING_EQUIP_HOOK}
        BigWorld.player().cell.setConsumableFishingEquip(posMap[nItemDes], item.id)


def _endBagslotToExplore(nPageSrc, nItemSrc, nPageDes, nItemDes):
    item = gameglobal.rds.ui.sItem
    if item == const.CONT_EMPTY_VAL:
        return
    if getattr(item, 'cstype', 0) == Item.SUBTYPE_2_EXPLORE_SCROLL:
        isQuestItem = bool(item.isQuestItem(item.id))
        if isQuestItem:
            nPageSrc = 0
        BigWorld.player().cell.equipScroll(nPageSrc, nItemSrc, bool(item.isQuestItem(item.id)))


def _endBagslotToSkillPanel(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if nPageDes == uiConst.SKILL_PANEL_LIFE:
        item = gameglobal.rds.ui.sItem
        if item == const.CONT_EMPTY_VAL:
            return
        if nItemDes == 0:
            return
        BigWorld.player().cell.exchangeInvFishingEqu(nPageSrc, nItemSrc, nItemDes - 1)
    elif nPageDes == uiConst.SKILL_PANEL_EXPLORE:
        item = gameglobal.rds.ui.sItem
        if item == const.CONT_EMPTY_VAL:
            return
        if nItemDes == 0:
            return
        BigWorld.player().cell.exchangeInvExploreEqu(nPageSrc, nItemSrc, gametypes.EXPLORE_EQUIP_COMPASS)


def _endBagslotToMail(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if nPageDes == uiConst.MAIL_SEND:
        p = BigWorld.player()
        item = p.inv.getQuickVal(nPageSrc, nItemSrc)
        if item:
            if item.isRuneHasRuneData():
                p.showGameMsg(GMDD.data.ITEM_MAIL_RUNE_EQUIP, ())
                return
            if item.isForeverBind():
                p.showGameMsg(GMDD.data.MAIL_ITEM_BIND, (item.name,))
                return
            if item.isItemNoMail():
                p.showGameMsg(GMDD.data.MAIL_ITEM_NOMAIL, (item.name,))
                return
            if item.hasLatch():
                p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                return
            if item.cwrap > 1:
                gameglobal.rds.ui.inventory.showNumberInputWidget(uiConst.NUMBER_WIDGET_ITEM_MAIL, nPageSrc, nItemSrc, nItemDes)
            else:
                gameglobal.rds.ui.mail.setItem(nPageSrc, nItemSrc, 0, nItemDes, item, 1)


def _endBagslotToItemMsgBox(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.itemMsgBox.trySetItem(const.RES_KIND_INV, nPageSrc, nItemSrc, nItemDes)


def _endFashionBagToItemMsgBox(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.itemMsgBox.trySetItem(const.RES_KIND_FASHION_BAG, nPageSrc, nItemSrc, nItemDes)


def _endBagslotToGuildDonate(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.guildDonate.setInventoryItem(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endBagslotToYaoPeiMix(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.yaoPeiMix.setInventoryItem(nPageSrc, nItemSrc)


def _endBagslotToYaoPeiFeed(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.yaoPeiFeed.setInventoryItem(nPageSrc, nItemSrc)


def _endBagslotToYaoPeiTransfer(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.yaoPeiTransfer.setInventoryItem(nPageSrc, nItemSrc, nItemDes)


def _endYaoPeiTransferToYaoPeiTransfer(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.yaoPeiTransfer.changeItem(nItemSrc, nItemDes)


def _endBagslotToYaoPeiReforge(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.yaoPeiReforge.setInventoryItem(nPageSrc, nItemSrc)


def _endBagslotToLottery(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.lottery.setInventoryItem(nPageSrc, nItemSrc)


def _endBagslotToConsign(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if gameglobal.rds.ui.inventory.page == uiConst.BAG_PAGE_QUEST:
        p.showGameMsg(GMDD.data.ITEM_TRADE_NOTRADE, ())
        return
    gameglobal.rds.ui.consign.setInventoryItem(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endBagslotToTabAuctionConsign(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if gameglobal.rds.ui.inventory.page == uiConst.BAG_PAGE_QUEST:
        p.showGameMsg(GMDD.data.ITEM_TRADE_NOTRADE, ())
        return
    gameglobal.rds.ui.tabAuctionConsign.removeItem(1, 99)
    gameglobal.rds.ui.tabAuctionConsign.setInventoryItem(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endBagslotToTabAuctionCrossServer(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if gameglobal.rds.ui.inventory.page == uiConst.BAG_PAGE_QUEST:
        p.showGameMsg(GMDD.data.ITEM_TRADE_NOTRADE, ())
        return
    gameglobal.rds.ui.tabAuctionCrossServer.removeItem(1, 99)
    gameglobal.rds.ui.tabAuctionCrossServer.setInventoryItem(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endBagslotToItemRecast(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    item = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if item:
        gameglobal.rds.ui.itemRecast.addItemToRecast(item, nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endActionbarToConsign(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if nPageSrc == uiConst.EQUIP_ACTION_BAR:
        p.showGameMsg(GMDD.data.ITEM_TRADE_NOTRADE, ())
        return


def _endActionbarToTabAuctionConsign(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if nPageSrc == uiConst.EQUIP_ACTION_BAR:
        p.showGameMsg(GMDD.data.ITEM_TRADE_NOTRADE, ())
        return


def _endActionbarToFashionBag(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if gameglobal.rds.ui.inventory.page == uiConst.BAG_PAGE_QUEST:
        return
    if nPageSrc == uiConst.EQUIP_ACTION_BAR:
        if BigWorld.player()._isSchoolSwitch():
            return
        cellCmd.exchangeFashionBagEqu(nPageDes, nItemDes, nItemSrc)


def _endActionbarToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if gameglobal.rds.ui.inventory.page == uiConst.BAG_PAGE_QUEST:
        return
    else:
        if nPageSrc == uiConst.EQUIP_ACTION_BAR:
            if BigWorld.player()._isSchoolSwitch():
                return
            cellCmd.exchangeInvEqu(nPageDes, nItemDes, nItemSrc)
        elif nPageSrc == uiConst.SKILL_ACTION_BAR:
            info = gameglobal.rds.ui.actionbar.getShortCut(nPageSrc, nItemSrc, None)
            if info:
                nSrcID = info[1]
                if info[0] in uiConst.SHORTCUT_TYPE_ITEM:
                    nSrcID = Item(info[1])
                gameglobal.rds.ui.actionbar.setItem(nSrcID, nPageSrc, nItemSrc, False, False, info[0])
        else:
            gameglobal.rds.ui.actionbar.refreshActionbarItem(nPageSrc, nItemSrc)
        return


def _endActionbarToSkillPanel(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if nPageSrc in [uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]:
        gameglobal.rds.ui.actionbar.refreshActionbarItem(nPageSrc, nItemSrc)


def _endSkillPanelToSkillPanel(nPageSrc, nItemSrc, nPageDes, nItemDes):
    skillProxy = gameglobal.rds.ui.skill
    if (nPageSrc, nPageDes) == (uiConst.SKILL_PANEL_SPECIAL_LEFT, uiConst.SKILL_PANEL_SPECIAL_RIGHT):
        skillProxy.wushuangSkillDragFromOrig2Slot(nPageSrc, nItemSrc, nPageDes, nItemDes)
    elif (nPageSrc, nPageDes) == (uiConst.SKILL_PANEL_SPECIAL_RIGHT, uiConst.SKILL_PANEL_SPECIAL_RIGHT):
        skillProxy.wushuangSkillDragFromSlot2Slot(nPageSrc, nItemSrc, nPageDes, nItemDes)
    elif nPageSrc == uiConst.SKILL_PANEL_AIR_ORIG and nPageDes == uiConst.SKILL_PANEL_AIR_SLOT:
        skillProxy.airSkillDragFromOrig2Slot(nItemSrc, nItemDes)
    elif nPageSrc == uiConst.SKILL_PANEL_AIR_SLOT and nPageDes == uiConst.SKILL_PANEL_AIR_SLOT:
        skillProxy.airSkillDragFromSlot2Slot(nItemSrc, nItemDes)


def _endEmoteToActionbar(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if nPageDes in (uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2):
        if nPageDes == uiConst.SKILL_ACTION_BAR and nItemDes >= uiConst.WUSHUANG_SKILL_START_POS_LEFT:
            return
        gameglobal.rds.ui.actionbar.dragFromEmote(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endEmoteToEmote(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if not gameglobal.rds.configData.get('enableNewEmotionPanel', False):
        gameglobal.rds.ui.emote.moveEmoteIcon(nItemSrc, nItemDes)
    else:
        gameglobal.rds.ui.emoteAction.moveEmoteIcon(nItemSrc, nItemDes)


def _endSkillPanelToAirbar(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if nPageSrc == uiConst.SKILL_PANEL_AIR_ORIG and nPageDes == uiConst.AIR_SKILL_BAR:
        gameglobal.rds.ui.airbar.skillPanelOrig2Airbar(nItemSrc, nItemDes)


def _endSkillPanelToActionbar(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if nPageSrc in (uiConst.SKILL_PANEL_COMMON,
     uiConst.SKILL_PANEL_GUILD,
     uiConst.SKILL_PANEL_SOCIAL,
     uiConst.SKILL_PANEL_INTIMACY) and nPageDes == uiConst.SKILL_ACTION_BAR:
        nSrcID = gameglobal.rds.ui.skill.getActionIDByPos(nPageSrc, nItemSrc)
        if nItemDes >= uiConst.WUSHUANG_SKILL_START_POS_LEFT:
            return
        gameglobal.rds.ui.actionbar.setItem(nSrcID, nPageDes, nItemDes, False, False, uiConst.SHORTCUT_TYPE_SKILL)
    elif nPageSrc == uiConst.SKILL_PANEL_SPECIAL_LEFT and nPageDes == uiConst.SKILL_ACTION_BAR:
        if nItemDes < uiConst.WUSHUANG_SKILL_START_POS_LEFT or not gameglobal.rds.ui.skill.dragMatch(nItemSrc, nItemDes):
            return
        desSlot = nItemDes - uiConst.WUSHUANG_SKILL_START_POS_LEFT
        desPage = uiConst.SKILL_PANEL_SPECIAL_RIGHT
        gameglobal.rds.ui.skill.wushuangSkillDragFromOrig2Slot(nPageSrc, nItemSrc, desPage, desSlot)
    elif nPageDes in (uiConst.SKILL_ACTION_BAR,
     uiConst.ITEM_ACTION_BAR,
     uiConst.ITEM_ACTION_BAR2,
     uiConst.EQUIP_ACTION_BAR):
        nSrcID = gameglobal.rds.ui.skill.getActionIDByPos(nPageSrc, nItemSrc)
        if nSrcID:
            gameglobal.rds.ui.skill.setItem(nSrcID, nPageSrc, nItemSrc)
        if gameglobal.rds.ui.actionbar.isItemBarInEdit():
            return
        if nPageSrc == uiConst.SKILL_PANEL_OTHER and nPageDes in (uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2):
            if nPageDes == uiConst.SKILL_ACTION_BAR and nItemDes >= uiConst.WUSHUANG_SKILL_START_POS_LEFT:
                return
            if nPageDes == uiConst.ITEM_ACTION_BAR and nItemDes >= uiConst.WUSHUANG_SKILL_START_POS_LEFT * 2:
                return
            gameglobal.rds.ui.actionbar.setRideItem(GSCD.data.get(nItemSrc).get('skillid'), nPageDes, nItemDes, False)
            return
        if nPageSrc == uiConst.SKILL_PANEL_LIFE and nPageDes in (uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR):
            if nPageDes == uiConst.SKILL_ACTION_BAR and nItemDes >= uiConst.WUSHUANG_SKILL_START_POS_LEFT:
                return
            if nPageDes == uiConst.ITEM_ACTION_BAR and nItemDes >= uiConst.WUSHUANG_SKILL_START_POS_LEFT * 2:
                return
            gameglobal.rds.ui.actionbar.setLifeItem(uiConst.LIFE_SKILL_FISHING, nPageDes, nItemDes, False)
            return
        if nPageSrc == uiConst.SKILL_PANEL_EXPLORE and nPageDes in (uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2) and nItemSrc == 0:
            gameglobal.rds.ui.actionbar.setLifeItem(uiConst.LIFE_SKILL_EXPLORE, nPageDes, nItemDes, False)
            return
        if nPageSrc in (uiConst.SKILL_PANEL_COMMON,
         uiConst.SKILL_PANEL_GUILD,
         uiConst.SKILL_PANEL_SOCIAL,
         uiConst.SKILL_PANEL_PUBG) and nPageDes in (uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2):
            gameglobal.rds.ui.actionbar.setItem(nSrcID, nPageDes, nItemDes, False, False, uiConst.SHORTCUT_TYPE_SKILL)
        if nPageSrc == uiConst.SKILL_PANEL_INTIMACY and nPageDes in (uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2):
            gameglobal.rds.ui.actionbar.setItem(nSrcID, nPageDes, nItemDes, False, False, uiConst.SHORTCUT_TYPE_SKILL)
            return


def _endLifeSkillToActionbar(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gamelog.debug('@hjx lifeSkill#_endLifeSkillToActionbar:', nPageSrc, nItemSrc, nPageDes, nItemDes)
    if nPageDes in (uiConst.SKILL_ACTION_BAR,
     uiConst.ITEM_ACTION_BAR,
     uiConst.EQUIP_ACTION_BAR,
     uiConst.ITEM_ACTION_BAR2):
        if gameglobal.rds.ui.actionbar.isItemBarInEdit():
            return
        if nPageSrc == uiConst.LIFE_SKILL_PANEL_SPECIAL and nPageDes in (uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2):
            if nPageDes == uiConst.SKILL_ACTION_BAR and nItemDes >= uiConst.WUSHUANG_SKILL_START_POS_LEFT:
                return
            if nItemSrc == 0:
                gameglobal.rds.ui.actionbar.setLifeItem(uiConst.LIFE_SKILL_FISHING, nPageDes, nItemDes, False)
            elif nItemSrc == 1:
                gameglobal.rds.ui.actionbar.setLifeItem(uiConst.LIFE_SKILL_EXPLORE, nPageDes, nItemDes, False)
            return
        if nPageSrc in (uiConst.LIFE_SKILL_PANEL_PRODUCE, uiConst.LIFE_SKILL_PANEL_MAKE, uiConst.LIFE_SKILL_PANEL_HOME):
            if nPageDes == uiConst.SKILL_ACTION_BAR and nItemDes >= uiConst.WUSHUANG_SKILL_START_POS_LEFT:
                return
            gameglobal.rds.ui.actionbar.setLifeItem(nItemSrc, nPageDes, nItemDes, False)


def _endWorldWarToActionbar(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.actionbar.setItem(nItemSrc, nPageDes, nItemDes, False, False, uiConst.SHORTCUT_TYPE_SKILL)


def _endWingWorldToActionbar(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.actionbar.setItem(nItemSrc, nPageDes, nItemDes, False, False, uiConst.SHORTCUT_TYPE_SKILL)
    gameglobal.rds.ui.actionbar.setNormalSlotsShine(False)
    gameglobal.rds.ui.actionbar.setAllItemSlotVisible(False)
    gameglobal.rds.ui.actionbar.refreshActionbar()


def _endClanWarSkillToActionbar(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.actionbar.setItem(nItemSrc, nPageDes, nItemDes, False, False, uiConst.SHORTCUT_TYPE_SKILL)
    gameglobal.rds.ui.actionbar.setNormalSlotsShine(False)
    gameglobal.rds.ui.actionbar.setAllItemSlotVisible(False)
    gameglobal.rds.ui.actionbar.refreshActionbar()


def _endSkillPanelToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if nPageSrc == uiConst.SKILL_PANEL_LIFE:
        if not BigWorld.player().stateMachine.checkStatus(const.CT_TAKE_OFF_FISHING_EQUIP):
            return
        BigWorld.player().cell.exchangeInvFishingEqu(nPageDes, nItemDes, nItemSrc - 1)
    elif nPageSrc == uiConst.SKILL_PANEL_EXPLORE:
        BigWorld.player().cell.exchangeInvExploreEqu(nPageDes, nItemDes, nItemSrc - 1)
    else:
        nSrcID = gameglobal.rds.ui.skill.getActionIDByPos(nPageSrc, nItemSrc)
        gameglobal.rds.ui.skill.setItem(nSrcID, nPageSrc, nItemSrc)


def _endTradeToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if nPageSrc == uiConst.TRADE_SLOTS_MINE:
        it = gameglobal.rds.ui.trade.Items[nPageSrc][nItemSrc]
        if it:
            BigWorld.player().cell.tradeItemR(nItemSrc, it.cwrap)


def _endSackslotToSackslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if nPageSrc != nPageDes:
        return
    if nPageSrc == const.BAG_BAR_BIND_ID and nItemDes < const.BAG_BAR_WIDTH:
        BigWorld.player().cell.exchangePack(nItemSrc, nItemDes)
        return
    if nPageSrc == const.CART_BIND_ID:
        return
    if nPageSrc == const.TEMP_BAG_BIND_ID:
        return
    if nPageSrc == const.MALL_BAR_BIND_ID:
        return
    if nPageSrc == const.MATERIAL_BAG_BIND_ID:
        materialBagItemSrc = BigWorld.player().materialBag.getQuickVal(0, nItemSrc)
        if materialBagItemSrc:
            BigWorld.player().base.materialBag2materialBag(0, nItemSrc, materialBagItemSrc.cwrap, 0, nItemDes)
    elif nPageSrc == const.FASHION_BAG_BIND_ID:
        fashionBagItemSrc = BigWorld.player().fashionBag.getQuickVal(0, nItemSrc)
        if fashionBagItemSrc:
            BigWorld.player().cell.fashionBag2fashionBag(0, nItemSrc, fashionBagItemSrc.cwrap, 0, nItemDes)


@ui.checkEquipChangeOpen()
def _endSackslotToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if gameglobal.rds.ui.inventory.page == uiConst.BAG_PAGE_QUEST:
        p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_TEMP_BAG_TO_QUEST_PAGE, ())
        return
    if nPageSrc == const.BAG_BAR_BIND_ID:
        packItemDest = p.inv.getQuickVal(nPageDes, nItemDes)
        if packItemDest == const.CONT_EMPTY_VAL:
            p.cell.unequipPack(nItemSrc, nPageDes, nItemDes)
        elif packItemDest.type == Item.BASETYPE_PACK:
            cellCmd.equipPack(nPageDes, nItemDes, nItemSrc)
        else:
            p.showGameMsg(GMDD.data.ITEM_UNEQUIPPACK_FORBIDDEN_POS, ())
            return
    elif nPageSrc == const.CART_BIND_ID:
        cartItemSrc = p.cart.getQuickVal(0, nItemSrc)
        if cartItemSrc:
            p.cell.takeCart(nItemSrc, nPageDes, nItemDes)
    elif nPageSrc == const.TEMP_BAG_BIND_ID:
        tempBagItemSrc = p.tempBag.getQuickVal(0, nItemSrc)
        if tempBagItemSrc:
            if Item.isQuestItem(tempBagItemSrc.id):
                tempBagDest = p.questBag.getQuickVal(nPageDes, nItemDes)
                if not tempBagDest:
                    p.cell.takeTempBagItemToQuestBag(nItemSrc, tempBagItemSrc.cwrap, nPageDes, nItemDes)
            else:
                tempBagDest = p.inv.getQuickVal(nPageDes, nItemDes)
                if not tempBagDest:
                    p.cell.takeTempBagItem(nItemSrc, tempBagItemSrc.cwrap, nPageDes, nItemDes)
    elif nPageSrc == const.MATERIAL_BAG_BIND_ID:
        materialBagItemSrc = p.materialBag.getQuickVal(0, nItemSrc)
        if materialBagItemSrc:
            materialBagItemDest = p.inv.getQuickVal(nPageDes, nItemDes)
            if not materialBagItemDest or materialBagItemDest.type == Item.BASETYPE_MATERIAL:
                cellCmd.materialBag2inv(0, nItemSrc, materialBagItemSrc.cwrap, nPageDes, nItemDes)
            else:
                p.showGameMsg(GMDD.data.ITEM_MATERIAL_INV_FORBIDDEN_EXCHANGE, ())
    elif nPageSrc == const.FASHION_BAG_BIND_ID:
        fashionBagItemSrc = p.fashionBag.getQuickVal(0, nItemSrc)
        if fashionBagItemSrc:
            fashionBagItemDest = p.inv.getQuickVal(nPageDes, nItemDes)
            if not fashionBagItemDest or fashionBagItemDest.type == Item.BASETYPE_FASHION:
                p.cell.fashionBag2inv(0, nItemSrc, fashionBagItemSrc.cwrap, nPageDes, nItemDes)
            else:
                p.showGameMsg(GMDD.data.ITEM_COMMODE_FORBIDDEN_EXCHANGE, ())
    elif nPageSrc == const.MALL_BAR_BIND_ID:
        mallBagItemSrc = p.mallBag.getQuickVal(0, nItemSrc)
        if mallBagItemSrc:
            mallBagItemDest = p.inv.getQuickVal(nPageDes, nItemDes)
            if not mallBagItemDest:
                p.cell.takeMallBagItem(nItemSrc, nPageDes, nItemDes)
            else:
                p.showTopMsg(gameStrings.TEXT_UIDRAG_1263)


def _endSackslotToTrade(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if nPageSrc == const.TEMP_BAG_BIND_ID:
        BigWorld.player().showGameMsg(GMDD.data.ITEM_TRADE_FORBIDDEN_TEMP_BAG_DRAG, ())


def _endFashionToFashionBag(nPageSrc, nItemSrc, nPageDes, nItemDes):
    cellCmd.exchangeFashionBagEqu(nPageDes, nItemDes, nItemSrc)


def _endFashionToActionbar(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if BigWorld.player()._isSchoolSwitch():
        return
    item = uiUtils.getEquipItemById(nItemSrc)
    if item == const.CONT_EMPTY_VAL:
        return
    if item.type in Item.BASETYPE_ITEM_ACTION_BAR:
        if gameglobal.rds.ui.trade.isShow:
            return
        if gameglobal.rds.ui.actionbar.isItemBarInEdit():
            return
        gameglobal.rds.ui.actionbar.dragItemFromEquipBar(item, nPageDes, nItemDes)
    else:
        BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_DRAG, ())
        return


def _endFashionBagToFashion(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    i = p.fashionBag.getQuickVal(nPageSrc, nItemSrc)
    if i == const.CONT_EMPTY_VAL:
        return
    if i.type == Item.BASETYPE_EQUIP:
        cellCmd.exchangeFashionBagEqu(nPageSrc, nItemSrc, nItemDes)


def _endFashionToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    cellCmd.exchangeInvEqu(nPageDes, nItemDes, nItemSrc)


def _endRuneViewToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if nPageSrc == uiConst.RUNE_TYPE_EQUIP and p.runeBoard.runeEquip:
        cellCmd.unequipRuneEquipment(nPageDes, nItemDes)
        return
    if gameglobal.rds.ui.runeForging.mediator or gameglobal.rds.ui.runeReforging.mediator:
        return
    p.cell.removeRune(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endBagslotToRuneView(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if not srcItem:
        return
    if nPageDes == uiConst.RUNE_TYPE_EQUIP and srcItem.isRuneEquip():
        cellCmd.equipRuneEquipment(nPageSrc, nItemSrc)
        return
    if srcItem.isRune() and BigWorld.player().getRuneData(srcItem.id, 'runeType', 0) == nPageDes:
        if not srcItem.isForeverBind():
            msg = GMD.data.get(GMDD.data.RUNE_EQUIP_BIND_TIP, {}).get('text', gameStrings.TEXT_INVENTORYPROXY_2658)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(cellCmd.addRune, nPageDes, nItemDes, nPageSrc, nItemSrc))
        else:
            cellCmd.addRune(nPageDes, nItemDes, nPageSrc, nItemSrc)


def _endBagslotToRuneInv(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    item = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if not item:
        return
    if gameglobal.rds.ui.equipChange.mediator:
        p.showGameMsg(GMDD.data.FORBIDDEN_BY_EQUIP_CHANGE_PANEL_OPEN, ())
        return
    if gameglobal.rds.ui.manualEquipLvUp.widget:
        p.showGameMsg(GMDD.data.FORBIDEN_BY_MANUAL_EQUIP_LV_UP_OPEN, ())
        return
    if nPageDes == uiConst.RUNE_INV_SLOT_PAGE:
        if item.type not in (Item.BASETYPE_PACK, Item.BASETYPE_PACK_EX):
            gamelog.info('jbx: pack bag type eroor ')
            return
        gamelog.info('jbx:inv2HierogramBagSlot', nPageSrc, nItemSrc, nItemDes)
        p.base.inv2HierogramBagSlot(nPageSrc, nItemSrc, nItemDes)
        return
    if not item.isRune():
        p.showDebugMessge(gameStrings.RUNE_INV_MOVE_WRONG_TYPE)
        return
    gamelog.info('jbx:inv2HierogramBag', nPageSrc, nItemSrc, item.cwrap, nPageDes, nItemDes)
    p.base.inv2HierogramBag(nPageSrc, nItemSrc, item.cwrap, nPageDes, nItemDes)
    p.showGameMsg(GMDD.data.MOVE_TO_RUNE_INV_W)


def _endHieroRoleToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if gameglobal.rds.ui.equipChange.mediator:
        p.showGameMsg(GMDD.data.FORBIDDEN_BY_EQUIP_CHANGE_PANEL_OPEN, ())
        return
    elif gameglobal.rds.ui.manualEquipLvUp.widget:
        p.showGameMsg(GMDD.data.FORBIDEN_BY_MANUAL_EQUIP_LV_UP_OPEN, ())
        return
    elif p.hierogramDict and p.hierogramDict.get('hieroEquip', None) and nPageSrc == uiConst.HIERO_TYPE_EQUIP:
        p.cell.unEquipHieroEquipment(nPageDes, nItemDes)
        return
    elif gameglobal.rds.ui.runeForging.mediator or gameglobal.rds.ui.runeReforging.mediator:
        return
    else:
        p.cell.removeHieroCrystal(nPageSrc, nItemSrc, nPageDes, nItemDes)
        return


def _endBagslotToHieroRole(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if not srcItem:
        return
    if gameglobal.rds.ui.equipChange.mediator:
        p.showGameMsg(GMDD.data.FORBIDDEN_BY_EQUIP_CHANGE_PANEL_OPEN, ())
        return
    if gameglobal.rds.ui.manualEquipLvUp.widget:
        p.showGameMsg(GMDD.data.FORBIDEN_BY_MANUAL_EQUIP_LV_UP_OPEN, ())
        return
    if nPageDes == uiConst.HIERO_TYPE_EQUIP and srcItem.isHieroEquip():
        if gameglobal.rds.ui.roleInformationHierogram.isLegitimateSlot(uiConst.HIERO_DRAG_BAG_ITEM, uiConst.HIERO_TYPE_EQUIP):
            p.cell.equipHieroEquipment(nPageSrc, nItemSrc)
        return
    if srcItem.isHieroCrystal():
        hieroType = p.getRuneData(srcItem.id, 'runeType', -1)
        if hieroType == nPageDes:
            if gameglobal.rds.ui.roleInformationHierogram.isLegitimateSlot(uiConst.HIERO_DRAG_BAG_ITEM, hieroType, nItemDes):
                if not srcItem.isForeverBind():
                    msg = GMD.data.get(GMDD.data.RUNE_EQUIP_BIND_TIP, {}).get('text', gameStrings.TEXT_INVENTORYPROXY_2658)
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.addHieroCrystal, nPageDes, nItemDes, nPageSrc, nItemSrc))
                else:
                    p.cell.addHieroCrystal(nPageDes, nItemDes, nPageSrc, nItemSrc)


def _endBagslotToRuneFeed(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if not srcItem:
        return


def _endRuneFeedToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if nItemSrc == uiConst.RUNE_FEED_ITEM:
        pass


def _endRuneFeedToNull(nPageSrc, nItemSrc):
    if nItemSrc == uiConst.RUNE_FEED_ITEM:
        pass


def _endBagslotToRuneLvUp(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if nPageDes:
        return
    p = BigWorld.player()
    srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if not srcItem:
        return
    gameglobal.rds.ui.runeLvUp.onAddItem(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endRuneLvUpToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.runeLvUp.removeItem(nPageSrc, nItemSrc)


def _endRuneLvUpToNull(nPageSrc, nItemSrc):
    gameglobal.rds.ui.runeLvUp.removeItem(nPageSrc, nItemSrc)


def _endBagslotToRuneChongXi(nPageSrc, nItemSrc, nPageDes, nItemDes):
    return
    p = BigWorld.player()
    srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if not srcItem:
        return
    if srcItem.isRunChongXi() and nPageDes == uiConst.RUNE_CHONGXI_ITEM:
        gameglobal.rds.ui.runeChongXi.addItem(srcItem, nPageDes, nItemDes)


def _endRuneChongXiToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    return
    if nPageSrc == uiConst.RUNE_CHONGXI_ITEM:
        gameglobal.rds.ui.runeChongXi.removeItem(nPageSrc, nItemSrc)


def _endRuneChongXiToNull(nPageSrc, nItemSrc):
    return
    if nPageSrc == uiConst.RUNE_CHONGXI_ITEM:
        gameglobal.rds.ui.runeChongXi.removeItem(nPageSrc, nItemSrc)


def _endBagslotToRuneReforging(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.runeReforging.setInventoryItem(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endRuneViewToRuneReforging(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if nPageSrc != uiConst.RUNE_TYPE_EQUIP:
        for runeDataVal in p.runeBoard.runeEquip.runeData:
            if runeDataVal.runeSlotsType == nPageSrc and runeDataVal.part == nItemSrc:
                srcItem = runeDataVal.item
                if srcItem and srcItem.isRune() and nPageDes == uiConst.RUNE_REFORGING_EQUIP and srcItem.canRuneReforging() and not nItemDes:
                    gameglobal.rds.ui.runeReforging.runePage = nPageSrc
                    gameglobal.rds.ui.runeReforging.runePart = nItemSrc
                    gameglobal.rds.ui.runeReforging.source = uiConst.RUNE_SOURCE_ROLE
                    gameglobal.rds.ui.runeReforging.invPage = const.CONT_NO_PAGE
                    gameglobal.rds.ui.runeReforging.invPos = const.CONT_NO_POS
                    gameglobal.rds.ui.runeReforging.addItem(srcItem, nPageDes, nItemDes)
                break


def _endRuneReforgingToNull(nPageSrc, nItemSrc):
    gameglobal.rds.ui.runeReforging.removeItem(nPageSrc, nItemSrc)


def _endBagslotToRuneForging(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.runeForging.setInventoryItem(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endRuneViewToRuneForging(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if nPageSrc != uiConst.RUNE_TYPE_EQUIP:
        for runeDataVal in p.runeBoard.runeEquip.runeData:
            if runeDataVal.runeSlotsType == nPageSrc and runeDataVal.part == nItemSrc:
                srcItem = runeDataVal.item
                if srcItem and srcItem.isRune() and nPageDes == uiConst.RUNE_REFORGING_EQUIP and srcItem.canRuneQiFu() and not nItemDes:
                    gameglobal.rds.ui.runeForging.runePage = nPageSrc
                    gameglobal.rds.ui.runeForging.runePart = nItemSrc
                    gameglobal.rds.ui.runeForging.source = uiConst.RUNE_SOURCE_ROLE
                    gameglobal.rds.ui.runeForging.invPage = const.CONT_NO_PAGE
                    gameglobal.rds.ui.runeForging.invPos = const.CONT_NO_POS
                    gameglobal.rds.ui.runeForging.addItem(srcItem, nPageDes, nItemDes)
                break


def _endRuneForgingToNull(nPageSrc, nItemSrc):
    gameglobal.rds.ui.runeForging.removeItem(nPageSrc, nItemSrc)


def _endBagslotToEquipFeed(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if gameglobal.rds.ui.inventory.page == uiConst.BAG_PAGE_QUEST:
        return
    p = BigWorld.player()
    srcIt = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if srcIt.isEquip():
        gameglobal.rds.ui.equipFeed.setItem(nPageSrc, nItemSrc, nPageDes, nItemDes, srcIt)


def _endActionbarToEquipFeed(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if nPageSrc != uiConst.EQUIP_ACTION_BAR or nItemDes != 0:
        return
    p = BigWorld.player()
    srcIt = p.equipment[nItemSrc]
    gameglobal.rds.ui.equipFeed.setItem(nPageSrc, nItemSrc, nPageDes, nItemDes, srcIt, False)


def _endBagslotToEquipFunc(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if gameglobal.rds.ui.inventory.page == uiConst.BAG_PAGE_QUEST:
        return
    p = BigWorld.player()
    srcIt = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if nItemDes in (0, 1):
        if srcIt.isEquip() and srcIt.getMaxEnhLv(p):
            pass
        elif nPageDes == uiConst.EQUIP_FUNC_ENHANCE:
            p.showGameMsg(GMDD.data.ITEM_ENHANCE_FORBID, ())
        else:
            p.showGameMsg(GMDD.data.ITEM_TRANSFER_FORBID, ())
    elif nPageDes == uiConst.EQUIP_FUNC_ENHANCE:
        if hasattr(srcIt, 'type') and srcIt.type == Item.BASETYPE_ENHANCE:
            pass
        else:
            p.showGameMsg(GMDD.data.ITEM_ENHANCE_FORBID, ())


def _endBagslotToEquipCopy(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if gameglobal.rds.ui.inventory.page == uiConst.BAG_PAGE_QUEST:
        return
    if nItemDes != 2:
        gameglobal.rds.ui.equipCopy.setItem(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endEquipCopyToNull(nPageSrc, nItemSrc):
    if nItemSrc in (0, 1):
        gameglobal.rds.ui.equipCopy.removeItem(nPageSrc, nItemSrc)


def _endBagslotToEquipEnhance(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if gameglobal.rds.ui.inventory.page == uiConst.BAG_PAGE_QUEST:
        return
    p = BigWorld.player()
    srcIt = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if not srcIt:
        return
    if nItemDes == 0:
        if srcIt.isEquip() and not srcIt.isYaoPei() and srcIt.getMaxEnhLv(p):
            gameglobal.rds.ui.equipEnhance.setItem(nPageSrc, nItemSrc, nPageDes, nItemDes, srcIt)
        elif nPageDes == uiConst.EQUIP_FUNC_ENHANCE:
            p.showGameMsg(GMDD.data.ITEM_ENHANCE_FORBID, ())
        else:
            p.showGameMsg(GMDD.data.ITEM_TRANSFER_FORBID, ())
    elif nPageDes == uiConst.EQUIP_FUNC_ENHANCE:
        if hasattr(srcIt, 'type') and srcIt.type == Item.BASETYPE_ENHANCE:
            gameglobal.rds.ui.equipEnhance.setItem(nPageSrc, nItemSrc, nPageDes, nItemDes, srcIt)
        else:
            p.showGameMsg(GMDD.data.ITEM_ENHANCE_FORBID, ())


def _endEquipFuncToEquipFunc(nPageSrc, nItemSrc, nPageDes, nItemDes):
    pass


def _endBagslotToUnBindItem(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    item = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if gameglobal.rds.ui.unBindItem.matchCondition(item):
        gameglobal.rds.ui.unBindItem.equipItem(item, nPageSrc, nItemSrc)


def _endBagslotToMixFameJewelry(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    item = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if gameglobal.rds.ui.mixFameJewelry.matchCondition(item):
        gameglobal.rds.ui.mixFameJewelry.equipItem(item, nPageSrc, nItemSrc)


def _endBagslotToEquipGem(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    item = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if item == None:
        return
    else:
        if gameglobal.rds.ui.equipGem.pageType == 1:
            if item.type == Item.BASETYPE_EQUIP:
                gameglobal.rds.ui.equipGem.equipItem(item, nPageSrc, nItemSrc)
            else:
                p.showGameMsg(GMDD.data.EQUIP_GEM_WRONG_TYPE_EQUIP, ())
        elif gameglobal.rds.ui.equipGem.pageType == 0:
            if gameglobal.rds.ui.equipGem.isPutEquip:
                if item.type == Item.BASETYPE_EQUIP_GEM and nPageDes == 1:
                    gameglobal.rds.ui.equipGem.equipGem(item, nPageSrc, nItemSrc)
                elif item.type == Item.BASETYPE_EQUIP and nPageDes == 0:
                    gameglobal.rds.ui.equipGem.equipItem(item, nPageSrc, nItemSrc)
                elif not gameglobal.rds.ui.equipGem.gem:
                    p.showGameMsg(GMDD.data.EQUIP_GEM_WRONG_TYPE_GEM, ())
            elif item.type == Item.BASETYPE_EQUIP and nPageDes == 0:
                gameglobal.rds.ui.equipGem.equipItem(item, nPageSrc, nItemSrc)
            else:
                p.showGameMsg(GMDD.data.EQUIP_GEM_WRONG_TYPE_EQUIP, ())
        return


def _endEquipGemToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.equipGem.returnItemToBag(nPageSrc)


def _endEquipGemToNull(nPageSrc, nItemSrc):
    gameglobal.rds.ui.equipGem.returnItemToBag(nPageSrc)


def _endUnBindItemToNull(nPageSrc, nItemSrc):
    gameglobal.rds.ui.unBindItem.clearPanel()


def _endMixFameJewelryToNull(nPageSrc, nItemSrc):
    gameglobal.rds.ui.mixFameJewelry.clearPanel()


def _endGemUnclokToNull(nPageSrc, nItemSrc):
    gameglobal.rds.ui.equipmentSlot.onRemoveItemToBag()


def _endGemUnclokToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.equipmentSlot.onRemoveItemToBag()


def _endBagslotToGemUnclok(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    srcIt = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if srcIt.type == Item.BASETYPE_EQUIP:
        if gameglobal.rds.ui.equipmentSlot.matchCondition(srcIt):
            gameglobal.rds.ui.equipmentSlot.equipItem(srcIt, nPageSrc, nItemSrc)
    else:
        p.showGameMsg(GMDD.data.EQUIP_GEM_WRONG_TYPE_EQUIP, ())


def _endBagslotToItemRecall(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    srcIt = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if gameglobal.rds.ui.itemRecall.checkRecallable(srcIt.id):
        gameglobal.rds.ui.itemRecall.setInventoryItem(srcIt, nPageSrc, nItemSrc)
        gameglobal.rds.ui.inventory.updateSlotState(nPageSrc, nItemSrc)
    else:
        p.showGameMsg(GMDD.data.CAN_NOT_RECALL_ITEM, ())


def _endItemRecallToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gameglobal.rds.ui.itemRecall.resetRecall()
    gameglobal.rds.ui.inventory.updateSlotState(nPageSrc, nItemSrc)


def _endCrossBagSlotToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if p._isSoul():
        p.showGameMsg(GMDD.data.DRAG_BETWEEN_CROSS_BAG_FORBIDDEN, ())
        return
    cellCmd.exchangeInvCrossInv(nPageDes, nItemDes, nPageSrc, nItemSrc, 0)


def _endBagslotToCrossBagSlot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    minCrossLv = SCD.data.get('minCrossServerBagLv', 69)
    enable = gameglobal.rds.configData.get('enableCrossServerBag', False) and p.lv >= minCrossLv or p.gmMode
    if p._isSoul() or not enable:
        if p.lv < minCrossLv:
            p.showGameMsg(GMDD.data.DRAG_BETWEEN_CROSS_BAG_FORBIDDEN_LV, ())
        else:
            p.showGameMsg(GMDD.data.DRAG_BETWEEN_CROSS_BAG_FORBIDDEN, ())
        return
    i = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if i:
        if ID.data.get(i.id, {}).get('canTakeToCrossServer', 0):
            cellCmd.exchangeInvCrossInv(nPageSrc, nItemSrc, nPageDes, nItemDes, 1)
        else:
            p.showGameMsg(GMDD.data.CROSS_ITEM_DRAG_FORBIDDEN_TYPE, ())


def _endActionbarToCrossBagSlot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if nPageSrc == uiConst.EQUIP_ACTION_BAR:
        if p.isInPUBG():
            cellCmd.exchangeCrossInvEqu(nPageDes, nItemDes, nItemSrc)


def _endCrossBagSlotToActionbar(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if nPageDes in (uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2):
        if gameglobal.rds.ui.sItem == const.CONT_EMPTY_VAL:
            return
        item = gameglobal.rds.ui.sItem
        if item.type in Item.BASETYPE_ITEM_ACTION_BAR:
            if gameglobal.rds.ui.trade.isShow:
                return
            if gameglobal.rds.ui.actionbar.isItemBarInEdit():
                return
            if nPageDes == uiConst.SKILL_ACTION_BAR and nItemDes >= uiConst.WUSHUANG_SKILL_START_POS_LEFT:
                return
            gameglobal.rds.ui.actionbar.dragItemFromBag(item, nPageSrc, nItemSrc, nPageDes, nItemDes)
        else:
            BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_DRAG, ())
            return
    elif nPageDes == uiConst.EQUIP_ACTION_BAR:
        if BigWorld.player()._isSchoolSwitch():
            return
        cellCmd.exchangeCrossInvEqu(nPageSrc, nItemSrc, nItemDes)


def _endCrossBagSlotToCrossBagSlot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if gameglobal.rds.ui.sItem == const.CONT_EMPTY_VAL:
        return
    cellCmd.exchangeCrossInv(nPageSrc, nItemSrc, gameglobal.rds.ui.sItem.cwrap, nPageDes, nItemDes)


def _endCrossBagSlotToNull(nPageSrc, nItemSrc):
    p = BigWorld.player()
    if not p._isSoul():
        p.showGameMsg(GMDD.data.DROP_CROSS_ITEM_FOBIDDEN_IN_OWN_SERVER, ())
        return
    if gameglobal.rds.ui.equipChange.mediator:
        p.showGameMsg(GMDD.data.FORBIDDEN_BY_EQUIP_CHANGE_PANEL_OPEN, ())
        return
    if gameglobal.rds.ui.manualEquipLvUp.widget:
        p.showGameMsg(GMDD.data.FORBIDEN_BY_MANUAL_EQUIP_LV_UP_OPEN, ())
        return
    if gameglobal.rds.ui.sItem == const.CONT_EMPTY_VAL:
        return
    if not p.life:
        msg = GMD.data.get(GMDD.data.ITEM_CANNOT_DROP, {}).get('text', '')
        it = p.crossInv.getQuickVal(nPageSrc, nItemSrc)
        msg = msg % it.name
        p.showTopMsg(msg)
        return
    gameglobal.rds.ui.crossServerBag.nPageSrc = nPageSrc
    gameglobal.rds.ui.crossServerBag.nItemSrc = nItemSrc
    if p.isInPUBG():
        gameglobal.rds.ui.crossServerBag.confirmDiscard()
    elif gameglobal.rds.ui.sItem.isPrecious():
        gameglobal.rds.ui.doubleCheckWithInput.show(gameStrings.TEXT_UIDRAG_310, 'DELETE', title=gameStrings.TEXT_DIGONGPROXY_207_4, confirmCallback=gameglobal.rds.ui.crossServerBag.confirmDiscard, cancelCallback=gameglobal.rds.ui.crossServerBag.cancelDiscard)
    else:
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(gameglobal.rds.ui.crossServerBag.confirmDiscard)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, Functor(gameglobal.rds.ui.crossServerBag.cancelDiscard))]
        if gameglobal.rds.ui.sItem.isRuneEquip() and getattr(gameglobal.rds.ui.sItem, 'runeData', ()):
            dropConfirmText = gameStrings.TEXT_UIDRAG_317
        else:
            it = BigWorld.player().crossInv.getQuickVal(nPageSrc, nItemSrc)
            name = uiUtils.toHtml(it.name, '#cc2929')
            if gameglobal.rds.ui.sItem.isGuanYin() and len(gameglobal.rds.ui.sItem.getAllGuanYinPskill()) > 0:
                dropConfirmText = uiUtils.getTextFromGMD(GMDD.data.GUAN_YIN_DISCARD_HINT, gameStrings.TEXT_UIDRAG_322) % name
            else:
                dropConfirmText = gameStrings.TEXT_UIDRAG_324 % name
        dropMBId = gameglobal.rds.ui.messageBox.show(True, '', dropConfirmText, buttons, False, 0, uiConst.MESSAGEBOX_INVENTORY)
        gameglobal.rds.ui.inventory.dropMBIds.append(dropMBId)


def _endSackslotToCrossBagSlot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    BigWorld.player().showGameMsg(GMDD.data.CROSS_BAG_ITEM_FORBIDDEN_DRAG, ())


def _endBagslotToWish(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    item = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if item:
        if item.isRuneHasRuneData():
            p.showGameMsg(GMDD.data.ITEM_MAIL_RUNE_EQUIP, ())
            return
        if item.isForeverBind():
            p.showGameMsg(GMDD.data.MAIL_ITEM_BIND, (item.name,))
            return
        if item.isItemNoMail():
            p.showGameMsg(GMDD.data.MAIL_ITEM_NOMAIL, (item.name,))
            return
        if item.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        if item.cwrap > 1:
            gameglobal.rds.ui.inventory.showNumberInputWidget(uiConst.NUMBER_WIDGET_WISH_MADE, nPageSrc, nItemSrc, nItemDes)
        else:
            gameglobal.rds.ui.wishMade.setItem(nPageSrc, nItemSrc, 0, nItemDes, item, 1)


def _endWishToNull(nPageSrc, nItemSrc):
    gameglobal.rds.ui.wishMade.removeItem(nPageSrc, nItemSrc)


def _endMeterialToStorage(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    itemSrc = p.materialBag.getQuickVal(0, nItemSrc)
    if itemSrc:
        p.showGameMsg(GMDD.data.OTHERBAG_FORBIDDEN_TO_STORAGE, ())


def _endStorageToMeterial(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    p.showGameMsg(GMDD.data.STORAGE_FORBIDDEN_TO_OTHERBAG, ())


def _endMeterialToMeterial(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if nPageSrc != const.METERIAL_BAG_PAGE_BAG and nPageDes != const.METERIAL_BAG_PAGE_BAG:
        materialBagItemSrc = BigWorld.player().materialBag.getQuickVal(nPageSrc, nItemSrc)
        if materialBagItemSrc:
            BigWorld.player().base.materialBag2materialBag(nPageSrc, nItemSrc, materialBagItemSrc.cwrap, nPageDes, nItemDes)


@ui.checkEquipChangeOpen()
def _endMeterialToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    if gameglobal.rds.ui.inventory.page == uiConst.BAG_PAGE_QUEST:
        p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_TEMP_BAG_TO_QUEST_PAGE, ())
    if nPageSrc == const.METERIAL_BAG_PAGE_BAG:
        item = p.materialBagBar.getQuickVal(0, nItemSrc)
        if item:
            p.cell.toMaterialBagSlot2Inv(nItemSrc, item.id, nPageDes, nItemDes)
    else:
        mPage = gameglobal.rds.ui.meterialBag.page
        materialBagItemSrc = p.materialBag.getQuickVal(mPage, nItemSrc)
        if materialBagItemSrc:
            materialBagItemDest = p.inv.getQuickVal(nPageDes, nItemDes)
            if not materialBagItemDest or materialBagItemDest.type == Item.BASETYPE_MATERIAL:
                cellCmd.materialBag2inv(mPage, nItemSrc, materialBagItemSrc.cwrap, nPageDes, nItemDes)
            else:
                p.showGameMsg(GMDD.data.ITEM_MATERIAL_INV_FORBIDDEN_EXCHANGE, ())


@ui.checkEquipChangeOpen()
def _endBagslotToMeterial(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if srcItem == const.CONT_EMPTY_VAL:
        return
    if nPageDes == const.METERIAL_BAG_PAGE_BAG:
        if nItemDes < getattr(p.materialBag, 'enabledPackSlotCnt', 0):
            p.base.toInv2MaterialBagSlot(nPageSrc, nItemSrc, nItemDes)
        else:
            p.showGameMsg(GMDD.data.UNLOCK_METERIALPACK_SLOT_FORBIDDEN, ())
    else:
        if srcItem.type != Item.BASETYPE_MATERIAL:
            p.showGameMsg(GMDD.data.ITEM_MATERIAL_INV_PICK_FORBIDDEN, ())
            return
        p.base.inv2materialBag(nPageSrc, nItemSrc, srcItem.cwrap, nPageDes, nItemDes)


def _endHomeTStorageToHomeTStorage(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    srcItem = gameglobal.rds.ui.homeTermsStorage.getQuickVal(nPageSrc, nItemSrc)
    if not srcItem:
        return
    if srcItem.isForeverBind():
        p.showGameMsg(GMDD.data.STORAGE_GUILD_ITEM_BIND, ())
        return
    strAmount = srcItem.cwrap
    stroageVersion = gameglobal.rds.ui.homeTermsStorage.getStorageVersion()
    p.cell.storageHomeChangePos(nPageSrc, nItemSrc, strAmount, nPageDes, nItemDes, stroageVersion)


def _endHomeTStorageToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    srcItem = gameglobal.rds.ui.homeTermsStorage.getQuickVal(nPageSrc, nItemSrc)
    if not srcItem:
        return
    if srcItem.isForeverBind():
        p.showGameMsg(GMDD.data.STORAGE_GUILD_ITEM_BIND, ())
        return
    strAmount = srcItem.cwrap
    cipher = p.cipherOfPerson
    stroageVersion = gameglobal.rds.ui.homeTermsStorage.getStorageVersion()
    p.cell.storageHome2Inv(nPageSrc, nItemSrc, strAmount, nPageDes, nItemDes, cipher, stroageVersion)


def _endBagslotToHomeTStorage(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if not srcItem:
        return
    if srcItem.isForeverBind():
        p.showGameMsg(GMDD.data.STORAGE_GUILD_ITEM_BIND, ())
        return
    strAmount = srcItem.cwrap
    cipher = p.cipherOfPerson
    stroageVersion = gameglobal.rds.ui.homeTermsStorage.getStorageVersion()
    p.cell.inv2StorageHome(nPageSrc, nItemSrc, strAmount, nPageDes, nItemDes, cipher, stroageVersion)


def _endSkillMacroToSkillMacro(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    p.base.moveMySkillMacro(nPageSrc, nItemSrc, nPageDes, nItemDes)


def _endSkillMacroToNull(nPageSrc, nItemSrc):
    gameglobal.rds.ui.skillMacroOverview.deleteMacro(nPageSrc, nItemSrc)


def _startSkillMacro(nPageSrc, nItemSrc):
    gameglobal.rds.ui.actionbar.setAllItemSlotVisible(True)
    gameglobal.rds.ui.actionbar.setNormalSlotsShine(True)
    gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_RED)
    gameglobal.rds.ui.airbar.setAirSlotsState(uiConst.SKILL_ICON_STAT_RED)


def _endSkillMacroToActionbar(nPageSrc, nItemSrc, nPageDes, nItemDes):
    if not gameglobal.rds.configData.get('enableSkillMacro', False) and BigWorld.isPublishedVersion():
        return
    if nItemDes >= uiConst.WUSHUANG_SKILL_START_POS_LEFT and nPageDes == uiConst.SKILL_ACTION_BAR:
        return
    nSrcID = gameglobal.rds.ui.skillMacroOverview.getActionInfoByPos(nPageSrc, nItemSrc)
    if nPageDes in (uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2):
        if gameglobal.rds.ui.actionbar.isItemBarInEdit():
            return
        gameglobal.rds.ui.actionbar.setItem(nSrcID, nPageDes, nItemDes, False, False, uiConst.SHORTCUT_TYPE_SKILL_MACRO)


def _endBfDotaItemToBfDotaItem(nPageSrc, nItemSrc, nPagDes, nItemDes):
    p = BigWorld.player()
    if formula.inDotaBattleField(p.mapID):
        if nItemSrc != nItemDes:
            p.cell.exchangeBattleFieldBag(nItemSrc, nItemDes)


def _endSummonedWarSpriteToActionbar(spriteIndex, spriteId, nPageDes, nItemDes):
    if nItemDes >= uiConst.WUSHUANG_SKILL_START_POS_LEFT and nPageDes == uiConst.SKILL_ACTION_BAR:
        return
    if nPageDes in (uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2):
        if gameglobal.rds.ui.actionbar.isItemBarInEdit():
            return
    gameglobal.rds.ui.actionbar.setItem((int(spriteIndex), int(spriteId)), nPageDes, nItemDes, False, False, uiConst.SHORTCUT_TYPE_SUMMONED_SPRITE)


def _startRuneInv(nPageSrc, nItemSrc):
    gameglobal.rds.ui.inDragRuneInvItem = True
    gameglobal.rds.ui.dragRuneInvPageSrc = nPageSrc
    gameglobal.rds.ui.dragRuneInvItemSrc = nItemSrc


def _endRuneInvToHieroRole(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gamelog.info('jbx:_endRuneInvToHieroRole', nPageSrc, nItemSrc, nPageDes, nItemDes)
    gameglobal.rds.ui.inDragRuneInvItem = False
    gameglobal.rds.ui.dragRuneInvPageSrc = None
    gameglobal.rds.ui.dragRuneInvItemSrc = None
    if gameglobal.rds.ui.equipChange.mediator:
        BigWorld.player().showGameMsg(GMDD.data.FORBIDDEN_BY_EQUIP_CHANGE_PANEL_OPEN, ())
        return
    elif gameglobal.rds.ui.manualEquipLvUp.widget:
        p.showGameMsg(GMDD.data.FORBIDEN_BY_MANUAL_EQUIP_LV_UP_OPEN, ())
        return
    elif nPageSrc == uiConst.RUNE_INV_SLOT_PAGE:
        return
    else:
        item = BigWorld.player().hierogramBag.getQuickVal(nPageSrc, nItemSrc)
        if not item or not item.isRune():
            return
        if not item.isForeverBind():
            msg = GMD.data.get(GMDD.data.RUNE_EQUIP_BIND_TIP, {}).get('text', '')
            p = BigWorld.player()
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.base.addHieroCrystalFromBag, nPageDes, nItemDes, nPageSrc, nItemSrc))
        else:
            gamelog.info('jbx:addHieroCrystalFromBag', nPageSrc, nItemSrc, item.cwrap, nPageDes, nItemDes)
            BigWorld.player().base.addHieroCrystalFromBag(nPageDes, nItemDes, nPageSrc, nItemSrc)
        return


def _endRuneInvToBagslot(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gamelog.info('jbx:_endShenGeBagToBagslot', nPageSrc, nItemSrc, nPageDes, nItemDes)
    gameglobal.rds.ui.inDragRuneInvItem = False
    gameglobal.rds.ui.dragRuneInvPageSrc = None
    gameglobal.rds.ui.dragRuneInvItemSrc = None
    if gameglobal.rds.ui.equipChange.mediator:
        BigWorld.player().showGameMsg(GMDD.data.FORBIDDEN_BY_EQUIP_CHANGE_PANEL_OPEN, ())
        return
    elif gameglobal.rds.ui.manualEquipLvUp.widget:
        p.showGameMsg(GMDD.data.FORBIDEN_BY_MANUAL_EQUIP_LV_UP_OPEN, ())
        return
    else:
        if nPageSrc == uiConst.RUNE_INV_SLOT_PAGE:
            item = BigWorld.player().hierogramBagBar.getQuickVal(0, nItemSrc)
            if not item:
                return
            gamelog.info('jbx:hierogramBagSlot2Inv', nItemSrc, item.id, nPageDes, nItemDes)
            BigWorld.player().cell.hierogramBagSlot2Inv(nItemSrc, item.id, nPageDes, nItemDes)
        else:
            item = BigWorld.player().hierogramBag.getQuickVal(nPageSrc, nItemSrc)
            if not item or not item.isRune():
                return
            gamelog.info('jbx:hierogramBag2Inv', nPageSrc, nItemSrc, item.cwrap, nPageDes, nItemDes)
            BigWorld.player().cell.hierogramBag2Inv(nPageSrc, nItemSrc, item.cwrap, nPageDes, nItemDes)
        return


def _endRuneInvToRuneInv(nPageSrc, nItemSrc, nPageDes, nItemDes):
    gamelog.info('jbx:_endRuneInvToRuneInv', nPageSrc, nItemSrc, nPageDes, nItemDes)
    if gameglobal.rds.ui.equipChange.mediator:
        BigWorld.player().showGameMsg(GMDD.data.FORBIDDEN_BY_EQUIP_CHANGE_PANEL_OPEN, ())
        return
    if gameglobal.rds.ui.manualEquipLvUp.widget:
        p.showGameMsg(GMDD.data.FORBIDEN_BY_MANUAL_EQUIP_LV_UP_OPEN, ())
        return
    gameglobal.rds.ui.inDragRuneInvItem = False
    if nPageSrc == uiConst.RUNE_INV_SLOT_PAGE or nPageDes == uiConst.RUNE_INV_SLOT_PAGE:
        if nPageSrc == nPageDes == uiConst.RUNE_INV_SLOT_PAGE:
            BigWorld.player().base.hierogramBagSlot2HierogramBagSlot(nItemSrc, nItemDes)
        return
    item = BigWorld.player().hierogramBag.getQuickVal(nPageSrc, nItemSrc)
    if not item:
        return
    BigWorld.player().base.hierogramBag2HierogramBag(nPageSrc, nItemSrc, item.cwrap, nPageDes, nItemDes)


def _endRuneInvToNull(nPageSrc, nItemSrc):
    gameglobal.rds.ui.inDragRuneInvItem = False
    gameglobal.rds.ui.dragRuneInvPageSrc = None
    gameglobal.rds.ui.dragRuneInvItemSrc = None


def _endBagslotToAvoidDoing(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if not srcItem:
        return
    gameglobal.rds.ui.avoidDoingActivityTip.setItem(srcItem)


def _endBagslotToSkillAppearanceConfirm(nPageSrc, nItemSrc, nPageDes, nItemDes):
    p = BigWorld.player()
    srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
    if not srcItem:
        return
    gameglobal.rds.ui.skillAppearanceConfirm.onItemDrag(srcItem)


def _endSpriteChallengeSelectToNull(nSpSrc, nSpIdSrc):
    gameglobal.rds.ui.spriteChallengeSelect.onSpriteDrag(nSpSrc, nSpIdSrc, -1, 0)


def _endSpriteChallengeSelectToSpriteChallengeSelect(nSpSrc, nSpIdSrc, nSpDes, nSpIdDes):
    gameglobal.rds.ui.spriteChallengeSelect.onSpriteDrag(nSpSrc, nSpIdSrc, nSpDes, nSpIdDes)


def _endMapGameDispatchToMapGameDispatch(nSpSrc, nSpIdSrc, nSpDes, nSpIdDes):
    gameglobal.rds.ui.mapGameDispatch.onSpriteDrag(nSpSrc, nSpIdSrc, nSpDes, nSpIdDes)


def _endMapGameDispatchToNull(nSpSrc, nSpIdSrc):
    gameglobal.rds.ui.mapGameDispatch.onSpriteDrag(nSpSrc, nSpIdSrc, -1, 0)
