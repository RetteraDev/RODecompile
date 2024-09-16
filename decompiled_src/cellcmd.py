#Embedded file name: /WORKSPACE/data/entities/client/helpers/cellcmd.o
import BigWorld
import utils
import const
import gameglobal
import gametypes
import combatUtils
import skillDataInfo
import commcalc
import clientcom
from guis import hotkey as HK
from guis import hotkey
from guis import ui
from item import Item
from callbackHelper import Functor
from gameclass import SkillInfo
from guis import messageBoxProxy, uiConst
from helpers import protect
from sfx import keyboardEffect
from gamestrings import gameStrings
from cdata import game_msg_def_data as GMDD
from data import item_data as ID
from data import wear_show_data as WSD
from data import equip_data as ED
from cdata import gui_bao_ge_item_reverse_data as GBGIRD
MIN_SKILL_INTERVAL = 0.0
MIN_ATTACK_INTERVAL = 0.5
stampMap = {'useSkill': 0.0,
 'attack': 0.0,
 'startQinggongAction': 0.0,
 'startQinggongState': 0.0}

def useSkill(skillId, skillLv, target, isDebug = False):
    global stampMap
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    timeNow = utils.getNow()
    if timeNow - stampMap['useSkill'] < MIN_SKILL_INTERVAL:
        p.chatToEventEx('发送指令过于频繁', const.CHANNEL_COLOR_RED)
        return
    skillInfo = p.getSkillInfo(skillId, skillLv)
    isSpellCharge = skillDataInfo.isChargeSkill(skillInfo)
    if not isSpellCharge:
        p.isWaitSkillReturn = True
        BigWorld.callback(const.SKILL_INTERVAL, Functor(_resetIsWaitSkillReturn, p))
    p.skillLog = [skillId, BigWorld.time()]
    if not isDebug:
        if target == None:
            beastSkill = skillInfo.getSkillData('beastSkill', 0)
            beast = p.getBeast()
            if beastSkill:
                _callUseSkill(p, skillInfo, beast)
            else:
                _callUseSkill(p, skillInfo, BigWorld.player())
            if BigWorld.player().chooseEffect.isShowingEffect:
                BigWorld.player().chooseEffect.cancel()
        else:
            if hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE and p.optionalTargetLocked and p.optionalTargetLocked.inWorld:
                isDamageSkill = skillDataInfo.isEnemySkill(skillInfo)
                isHealSkill = skillDataInfo.isFriendSkill(skillInfo)
                isEnemy = p.isEnemy(p.targetLocked)
                isCastSelfKeyDown = HK.isCastSelfKeyDown()
                if not isCastSelfKeyDown and (isEnemy and isHealSkill or not isEnemy and isDamageSkill):
                    if p.optionalTargetLocked and getattr(p.optionalTargetLocked, 'IsCombatUnit', False):
                        target = p.optionalTargetLocked
                    if not p.ap.lockAim:
                        p.lockTarget(p.optionalTargetLocked)
            _callUseSkill(p, skillInfo, target)
            if BigWorld.player().chooseEffect.isShowingEffect:
                BigWorld.player().chooseEffect.cancel()
    elif target == None:
        p.cell.useSkillDebug(skillId, skillLv, BigWorld.player().id)
    else:
        p.cell.useSkillDebug(skillId, skillLv, target.id)
    stampMap['useSkill'] = timeNow
    gameglobal.rds.sound.lastUseSkill[skillId] = timeNow


def _callUseSkill(p, skillInfo, tgt):
    if not tgt or not tgt.inWorld:
        return
    if gameglobal.rds.configData.get('enableSkillClientCalc', False) and combatUtils.needClientEffectCalc(p, skillInfo):
        effectDict = combatUtils.calcUseSkillEffect(p, tgt, skillInfo)
        strValue = utils.getStrFromEffectDict(effectDict)
        p.cell.useSkillWithClientCalc(skillInfo.num, tgt.id, strValue, p.getServerTime())
    else:
        p.cell.useSkill(skillInfo.num, tgt.id, p.getServerTime())
    nepLogUseSkill(skillInfo.num)
    if gameglobal.rds.bar is None and gameglobal.rds.soltId is None:
        return


def nepLogUseSkill(skillId):
    try:
        protect.nepActionRoleActivity(protect.eNEActivity_KMonster, skillId, 0, 0)
    except:
        pass


def _resetIsWaitSkillReturn(owner):
    owner.isWaitSkillReturn = False


def startQinggongAction(actionType, position):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    p.cell.startQinggongAction(actionType, position)


def startQinggongState(qinggongState, position):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    if not qinggongState:
        return
    p.cell.startQinggongState(qinggongState, position)


def switchWeaponState(weaponState):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    if weaponState == p.weaponState:
        return
    p.cell.switchWeaponState(weaponState)


def cancelSkill():
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    p.cell.cancelSkill()


def cancelAction(cause = const.CANCEL_ACT_ANY_WAY):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    p.cell.cancelAction(cause)


def cancelFishing():
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    p.cell.stopFishing(False)


def castChargeSkill():
    p = BigWorld.player()
    if not p.chargeSkillId:
        return
    isSpellCharge = skillDataInfo.isChargeSkill(SkillInfo(p.chargeSkillId, p.chargeSkillLv))
    if isSpellCharge:
        p.cell.castChargeSkill(p.chargeSkillId, p.lockedId)
        p.isChargeKeyDown = False
        gameglobal.rds.ui.castbar.chargeSkillOver = True
    p.chargeSkillId = None
    p.chargeSkillLv = None


def endUpQinggongState():
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    if p.qinggongState == gametypes.QINGGONG_STATE_DEFAULT and not p.ap.needForceEndQingGong:
        return
    if p.ap.needForceEndQingGong:
        p.ap.needForceEndQingGong = False
    p.cell.endUpQinggongState()


@ui.checkEquipChangeOpen()
def exchangeFashionBagEqu(nPageDes, nItemDes, nItemSrc):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    invIt = p.fashionBag.getQuickVal(nPageDes, nItemDes)
    if invIt == const.CONT_EMPTY_VAL:
        equIt = p.equipment.get(nItemSrc)
        if equIt == const.CONT_EMPTY_VAL:
            return
        if equIt.isCombatEquReq() and p.inCombat:
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_TAKE_OFF_EQUIP, ())
            return
        if equIt.equipType in (Item.EQUIP_BASETYPE_WEAPON, Item.EQUIP_BASETYPE_FASHION_WEAPON):
            if not p.stateMachine.checkStatus(const.CT_TAKE_OFF_WEAPON):
                return
        elif not p.stateMachine.checkStatus(const.CT_TAKE_OFF_EQUIP_ITEM):
            return
        if nPageDes == const.CONT_NO_POS:
            return
        p.cell.exchangeFashionBagEqu(nPageDes, nItemDes, nItemSrc, True)
    elif invIt.type == Item.BASETYPE_EQUIP:
        if nPageDes == const.CONT_NO_POS:
            return
        if hasattr(invIt, 'equipType') and invIt.equipType == Item.EQUIP_BASETYPE_FASHION:
            if invIt.isEquipBind():
                MBButton = messageBoxProxy.MBButton
                buttons = [MBButton('确定', Functor(onConfirmExchangeFashionBagFashion, nPageDes, nItemDes, nItemSrc)), MBButton('取消')]
                gameglobal.rds.ui.messageBox.show(True, '', '此操作会绑定时装，是否继续？', buttons)
            else:
                p.cell.exchangeFashionBagFashion(nPageDes, nItemDes, nItemSrc, False)
        else:
            p.cell.exchangeFashionBagEqu(nPageDes, nItemDes, nItemSrc, False)


@ui.checkEquipChangeOpen()
def onConfirmExchangeFashionBagFashion(nPageDes, nItemDes, nItemSrc):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    p.cell.exchangeFashionBagFashion(nPageDes, nItemDes, nItemSrc, False)


@ui.checkEquipChangeOpen()
def equipRideWingBag(nPageDes, nItemDes, nItemSrc):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    invIt = p.rideWingBag.getQuickVal(nPageDes, nItemDes)
    if invIt == const.CONT_EMPTY_VAL:
        equIt = p.equipment.get(nItemSrc)
        if equIt == const.CONT_EMPTY_VAL:
            return
        if equIt.isCombatEquReq() and p.inCombat:
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_TAKE_OFF_EQUIP, ())
            return
        if not p.stateMachine.checkStatus(const.CT_TAKE_OFF_EQUIP_ITEM):
            return
        p.base.equipRideWingBag(nPageDes, nItemDes, nItemSrc)
    elif invIt.type == Item.BASETYPE_EQUIP:
        equIt = p.equipment.get(nItemSrc)
        if equIt != const.CONT_EMPTY_VAL:
            if equIt.isCombatEquReq() and p.inCombat:
                p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_TAKE_OFF_EQUIP, ())
                return
            if not p.stateMachine.checkStatus(const.CT_TAKE_OFF_EQUIP_ITEM):
                return
        if invIt.isCombatEquReq() and p.inCombat:
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_EQUIP, ())
            return
        if invIt.equipType in (Item.EQUIP_BASETYPE_WEAPON, Item.EQUIP_BASETYPE_FASHION_WEAPON):
            if not p.stateMachine.checkStatus(const.CT_USE_WEAPON):
                return
        elif not p.stateMachine.checkStatus(const.CT_EQUIP_ITEM):
            return
        if ID.data[invIt.id].has_key('schReq') and p.realSchool not in ID.data[invIt.id]['schReq']:
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_WRONG_SCHOOL, invIt.name)
            return
        if getattr(invIt, 'lvReq', 0) and p.lv < getattr(invIt, 'lvReq', 0):
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_WRONG_LEVEL, invIt.name)
            return
        maxLvReq = ID.data.get(invIt.id, {}).get('maxLvReq', 0)
        if maxLvReq != 0 and p.lv > maxLvReq:
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_WRONG_LEVEL, invIt.name)
            return
        sexReq = ID.data.get(invIt.id, {}).get('sexReq', const.SEX_UNKNOWN)
        if sexReq != const.SEX_UNKNOWN and p.physique.sex != sexReq:
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_WRONG_SEX, invIt.name)
            return
        if invIt.isEquipBind():
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton('确定', Functor(_onConfirmEquipWingBag, nPageDes, nItemDes, nItemSrc)), MBButton('取消')]
            gameglobal.rds.ui.messageBox.show(True, '', '此操作会绑定装备，是否继续？', buttons)
        else:
            p.base.equipRideWingBag(nPageDes, nItemDes, nItemSrc)


@ui.checkEquipChangeOpen()
def exchangeInvEqu(nPageDes, nItemDes, nItemSrc):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    if nItemSrc == gametypes.EQU_PART_CAPE and (gameglobal.rds.ui.guanYinV3.widget or gameglobal.rds.ui.guanYinAddSkillV3.widget):
        p.showGameMsg(GMDD.data.EXCHANGE_INV_IN_GUAN_YIN_OPEN, ())
        return
    invIt = p.inv.getQuickVal(nPageDes, nItemDes)
    if nItemSrc >= const.SUB_EQUIP_PART_OFFSET:
        equIt = commcalc.getAlternativeEquip(p, nItemSrc - const.SUB_EQUIP_PART_OFFSET)
        isSubEquip = True
    else:
        equIt = p.equipment.get(nItemSrc)
        isSubEquip = False
    if invIt == const.CONT_EMPTY_VAL:
        if not _checkEquipCanRemove(equIt):
            return
        if isSubEquip:
            p.cell.exchangeInvSubEqu(nPageDes, nItemDes, nItemSrc - const.SUB_EQUIP_PART_OFFSET, True)
        else:
            p.cell.exchangeInvEqu(nPageDes, nItemDes, nItemSrc, True)
    elif invIt.type == Item.BASETYPE_EQUIP:
        if equIt != const.CONT_EMPTY_VAL:
            if not _checkEquipCanRemove(equIt):
                return
        if not _checkEquipCanTakeOn(invIt):
            return
        if hasattr(invIt, 'equipType') and invIt.equipType == Item.EQUIP_BASETYPE_FASHION:
            if invIt.isEquipBind():
                MBButton = messageBoxProxy.MBButton
                buttons = [MBButton('确定', Functor(_onConfirmEquipItem, nPageDes, nItemDes, nItemSrc)), MBButton('取消')]
                gameglobal.rds.ui.messageBox.show(True, '', '此操作会绑定时装，是否继续？', buttons)
            elif isSubEquip:
                pass
            else:
                p.cell.exchangeInvFashion(nPageDes, nItemDes, nItemSrc, False)
        elif invIt.isEquipBind():
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton('确定', Functor(_onConfirmEquipItem, nPageDes, nItemDes, nItemSrc)), MBButton('取消')]
            gameglobal.rds.ui.messageBox.show(True, '', '此操作会绑定装备，是否继续？', buttons)
        elif isSubEquip:
            p.cell.exchangeInvSubEqu(nPageDes, nItemDes, nItemSrc - const.SUB_EQUIP_PART_OFFSET, False)
        else:
            p.cell.exchangeInvEqu(nPageDes, nItemDes, nItemSrc, False)


@ui.checkEquipChangeOpen()
def exchangeCrossInvEquList(equipPartDataList):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    realEquipPartDataList = []
    for nPageDes, nItemDes, nItemSrc in equipPartDataList:
        invIt = p.crossInv.getQuickVal(nPageDes, nItemDes)
        equIt = p.equipment.get(nItemSrc)
        if invIt == const.CONT_EMPTY_VAL:
            continue
        elif invIt.type == Item.BASETYPE_EQUIP:
            if equIt != const.CONT_EMPTY_VAL:
                if not _checkEquipCanRemove(equIt, showError=False):
                    continue
            if not _checkEquipCanTakeOn(invIt, showError=False):
                continue
            if hasattr(invIt, 'equipType') and invIt.equipType == Item.EQUIP_BASETYPE_FASHION:
                continue
        realEquipPartDataList.append({'page': nPageDes,
         'pos': nItemDes,
         'part': nItemSrc})

    if realEquipPartDataList:
        p.cell.exchangeInvEquList(realEquipPartDataList, True)


@ui.checkEquipChangeOpen()
def exchangeCrossInvEqu(nPageDes, nItemDes, nItemSrc):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    invIt = p.crossInv.getQuickVal(nPageDes, nItemDes)
    equIt = p.equipment.get(nItemSrc)
    if invIt == const.CONT_EMPTY_VAL:
        if not _checkEquipCanRemove(equIt):
            return
        p.cell.exchangeInvEqu(nPageDes, nItemDes, nItemSrc, True)
    elif invIt.type == Item.BASETYPE_EQUIP:
        if equIt != const.CONT_EMPTY_VAL:
            if not _checkEquipCanRemove(equIt):
                return
        if not _checkEquipCanTakeOn(invIt):
            return
        if hasattr(invIt, 'equipType') and invIt.equipType == Item.EQUIP_BASETYPE_FASHION:
            if invIt.isEquipBind():
                MBButton = messageBoxProxy.MBButton
                buttons = [MBButton('确定', Functor(_onConfirmEquipItem, nPageDes, nItemDes, nItemSrc)), MBButton('取消')]
                gameglobal.rds.ui.messageBox.show(True, '', '此操作会绑定时装，是否继续？', buttons)
            else:
                p.cell.exchangeInvFashion(nPageDes, nItemDes, nItemSrc, False)
        elif invIt.isEquipBind():
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton('确定', Functor(_onConfirmEquipItem, nPageDes, nItemDes, nItemSrc)), MBButton('取消')]
            gameglobal.rds.ui.messageBox.show(True, '', '此操作会绑定装备，是否继续？', buttons)
        else:
            p.cell.exchangeInvEqu(nPageDes, nItemDes, nItemSrc, False)


def _checkEquipCanRemove(equIt, showError = True):
    p = BigWorld.player()
    if equIt == const.CONT_EMPTY_VAL:
        return False
    if equIt.isCombatEquReq() and p.inCombat:
        showError and p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_TAKE_OFF_EQUIP, ())
        return False
    if equIt.isGuanYin() and gameglobal.rds.ui.guanYin.chechPanelOpen():
        showError and p.showGameMsg(GMDD.data.GUANYIN_CHANGE_ERROR_PANEL_OPEN, ())
        return False
    if equIt.equipType in (Item.EQUIP_BASETYPE_WEAPON, Item.EQUIP_BASETYPE_FASHION_WEAPON):
        if not p.stateMachine.checkStatus(const.CT_TAKE_OFF_WEAPON, bMsg=showError):
            return False
    elif not p.stateMachine.checkStatus(const.CT_TAKE_OFF_EQUIP_ITEM, bMsg=showError):
        return False
    return True


def _checkEquipCanTakeOn(equipItem, showError = True):
    p = BigWorld.player()
    if equipItem.isRubbing():
        showError and p.showGameMsg(GMDD.data.RUBBING_FORBIDDEN_USE, ())
        return False
    if equipItem.isCombatEquReq() and p.inCombat:
        showError and p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_EQUIP, ())
        return False
    if equipItem.equipType in (Item.EQUIP_BASETYPE_WEAPON, Item.EQUIP_BASETYPE_FASHION_WEAPON):
        if not p.stateMachine.checkStatus(const.CT_USE_WEAPON, bMsg=showError):
            return False
    elif not p.stateMachine.checkStatus(const.CT_EQUIP_ITEM, bMsg=showError):
        return False
    if hasattr(equipItem, 'equipType') and equipItem.equipType != Item.EQUIP_BASETYPE_FASHION:
        equipItemData = ID.data.get(equipItem.id, {})
        if equipItemData.has_key('schReq') and p.realSchool not in equipItemData['schReq']:
            showError and p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_WRONG_SCHOOL, equipItem.name)
            return False
        if getattr(equipItem, 'lvReq', 0) and p.lv < getattr(equipItem, 'lvReq', 0):
            showError and p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_WRONG_LEVEL, equipItem.name)
            return False
        maxLvReq = equipItemData.get('maxLvReq', 0)
        if maxLvReq != 0 and p.lv > maxLvReq:
            showError and p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_WRONG_LEVEL, equipItem.name)
            return False
        sexReq = ID.data.get(equipItem.id, {}).get('sexReq', const.SEX_UNKNOWN)
        if sexReq != const.SEX_UNKNOWN and p.physique.sex != sexReq:
            showError and p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_WRONG_SEX, equipItem.name)
            return False
    return True


@ui.checkEquipChangeOpen()
def fashionMessageBox(nPageDes, nItemDes, nItemSrc):
    MBButton = messageBoxProxy.MBButton
    buttons = [MBButton('确定', Functor(_onConfirmFashion, nPageDes, nItemDes, nItemSrc)), MBButton('取消')]
    gameglobal.rds.ui.messageBox.show(True, '', '装备后将不能退货，是否继续？', buttons)


@ui.checkEquipChangeOpen()
def equipMessageBox(nPageDes, nItemDes, nItemSrc):
    MBButton = messageBoxProxy.MBButton
    buttons = [MBButton('确定', Functor(_onConfirmEquipItem, nPageDes, nItemDes, nItemSrc)), MBButton('取消')]
    gameglobal.rds.ui.messageBox.show(True, '', '装备后将不能退货，是否继续？', buttons)


@ui.checkEquipChangeOpen()
def _onConfirmFashion(nPageDes, nItemDes, nItemSrc):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    p.cell.exchangeInvFashion(nPageDes, nItemDes, nItemSrc, True)


@ui.checkEquipChangeOpen()
def _onConfirmEquipItem(nPageDes, nItemDes, nItemSrc):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    invIt = p.inv.getQuickVal(nPageDes, nItemDes)
    if nItemSrc >= const.SUB_EQUIP_PART_OFFSET:
        if hasattr(invIt, 'equipType') and invIt.equipType == Item.EQUIP_BASETYPE_FASHION:
            pass
        else:
            p.cell.exchangeInvSubEqu(nPageDes, nItemDes, nItemSrc - const.SUB_EQUIP_PART_OFFSET, True)
    elif hasattr(invIt, 'equipType') and invIt.equipType == Item.EQUIP_BASETYPE_FASHION:
        p.cell.exchangeInvFashion(nPageDes, nItemDes, nItemSrc, True)
    else:
        p.cell.exchangeInvEqu(nPageDes, nItemDes, nItemSrc, True)


@ui.checkEquipChangeOpen()
def _onConfirmEquipWingBag(nPageDes, nItemDes, nItemSrc):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    p.base.equipRideWingBag(nPageDes, nItemDes, nItemSrc)


def equipPack(pageSrc, posSrc, posDes):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    p.cell.equipPack(pageSrc, posSrc, posDes)


def equipRuneEquipment(nPage, nItem):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    if gameglobal.rds.ui.runeChongXi.mediator:
        p.showGameMsg(GMDD.data.RUNE_FORBIDDEN_IN_FEED, ())
        return
    if gameglobal.rds.ui.runeForging.mediator or gameglobal.rds.ui.runeReforging.mediator:
        return
    runeEquip = p.inv.getQuickVal(nPage, nItem)
    if not gameglobal.rds.ui.roleInfo.mediator and runeEquip.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
        gameglobal.rds.ui.roleInfo.show()
        gameglobal.rds.ui.roleInfo.tabIdx = uiConst.ROLEINFO_TAB_RUNE
    p.cell.equipRuneEquipment(nPage, nItem)


def unequipRuneEquipment(nPage, nItem):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    if gameglobal.rds.ui.runeChongXi.mediator:
        p.showGameMsg(GMDD.data.RUNE_FORBIDDEN_IN_FEED, ())
        return
    if gameglobal.rds.ui.runeForging.mediator or gameglobal.rds.ui.runeReforging.mediator:
        return
    p.cell.unequipRuneEquipment(nPage, nItem)


def addRune(nPageDes, nItemDes, nPageSrc, nItemSrc):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    if gameglobal.rds.ui.runeForging.mediator or gameglobal.rds.ui.runeReforging.mediator:
        return
    if not gameglobal.rds.ui.roleInfo.mediator:
        gameglobal.rds.ui.roleInfo.show()
        gameglobal.rds.ui.roleInfo.tabIdx = uiConst.ROLEINFO_TAB_RUNE
    p.cell.addRune(nPageDes, nItemDes, nPageSrc, nItemSrc)


def buy(shopId, ent, nPage, nItem, cwrap):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    ent.cell.buy(shopId, nPage, nItem, cwrap)


@ui.checkEquipChangeOpen()
def exchangeInv(nPageSrc, nItemSrc, cwrap, nPageDes, nItemDes):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    p.cell.exchangeInv(nPageSrc, nItemSrc, cwrap, nPageDes, nItemDes)


@ui.checkEquipChangeOpen()
def exchangeInvCrossInv(nPageSrc, nItemSrc, nPageDes, nItemDes, toCrossInv):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    p.cell.exchangeInvCrossInv(nPageSrc, nItemSrc, nPageDes, nItemDes, toCrossInv)


@ui.checkEquipChangeOpen()
def exchangeCrossInv(nPageSrc, nItemSrc, cwrap, nPageDes, nItemDes):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    p.cell.exchangeCrossInv(nPageSrc, nItemSrc, cwrap, nPageDes, nItemDes)


@ui.checkEquipChangeOpen()
def materialBag2inv(nPageSrc, nItemSrc, cwrap, nPageDes, nItemDes):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    p.cell.materialBag2inv(nPageSrc, nItemSrc, cwrap, nPageDes, nItemDes)


def enterWingFly(needAction):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    enableRandWingFly = gameglobal.rds.configData.get('enableRandWingFly', False)
    needRand = True
    if not enableRandWingFly:
        needRand = False
    if not p.isEnableRandWing():
        needRand = False
    p.cell.enterWingFly(needAction, False, needRand)


def useEquipmentSkill(equipPart, equipSkillId):
    p = BigWorld.player()
    if p.relogNotifyState:
        return
    target = p.targetLocked
    skillInfo = SkillInfo(equipSkillId, 1)
    if not target or not target.inWorld or skillInfo.getSkillData('noTgt'):
        p.cell.useEquipmentSkill(equipPart, equipSkillId, p.id)
    else:
        p.cell.useEquipmentSkill(equipPart, equipSkillId, target.id)


def useWearSkill(equipPart, wearId):
    p = BigWorld.player()
    wsd = WSD.data.get(wearId, {})
    key = clientcom.getAvatarKey(p)
    skills = wsd.get(key + 'Skills', [])
    if skills:
        skill = skills[0]
        p.useWearSkill(True, skill[0], skill[1], equipPart)


@ui.checkEquipChangeOpen()
def equipWardrobeItemFromInv(srcPage, srcPos, invIt):
    p = BigWorld.player()
    if not checkCanInsertInfoBag(invIt):
        return False
    if hasattr(invIt, 'equipType') and invIt.equipType in (Item.EQUIP_BASETYPE_FASHION, Item.EQUIP_BASETYPE_FASHION_WEAPON):
        if invIt.isEquipBind():
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.CONFIRM, Functor(p.base.requireInv2wardrobeBag, srcPage, srcPos, '')), MBButton(gameStrings.CANCEL)]
            gameglobal.rds.ui.messageBox.show(True, '', gameStrings.WARDROBE_BIND_CONFIRM, buttons)
        elif invIt.canReturnToShop():
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.CONFIRM, Functor(p.base.requireInv2wardrobeBag, srcPage, srcPos, '')), MBButton(gameStrings.CANCEL)]
            gameglobal.rds.ui.messageBox.show(True, '', gameStrings.WARDROBE_CANT_RETURN_CONFIRM, buttons)
        else:
            p.base.requireInv2wardrobeBag(srcPage, srcPos, '')
    else:
        return False
    return True


@ui.checkEquipChangeOpen()
def equipWardrobeItemFromFashion(srcPage, srcPos, invIt):
    p = BigWorld.player()
    if not checkCanInsertInfoBag(invIt):
        return False
    if hasattr(invIt, 'equipType') and invIt.equipType in (Item.EQUIP_BASETYPE_FASHION, Item.EQUIP_BASETYPE_FASHION_WEAPON):
        if invIt.isEquipBind():
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.CONFIRM, Functor(p.base.requireFashionBag2wardrobeBag, srcPage, srcPos)), MBButton(gameStrings.CANCEL)]
            gameglobal.rds.ui.messageBox.show(True, '', gameStrings.WARDROBE_BIND_CONFIRM, buttons)
        elif invIt.canReturnToShop():
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.CONFIRM, Functor(p.base.requireFashionBag2wardrobeBag, srcPage, srcPos)), MBButton(gameStrings.CANCEL)]
            gameglobal.rds.ui.messageBox.show(True, '', gameStrings.WARDROBE_CANT_RETURN_CONFIRM, buttons)
        else:
            p.base.requireFashionBag2wardrobeBag(srcPage, srcPos)
    else:
        return False
    return True


def removeWardrobeItemFromWardrobe(itemUUID):
    p = BigWorld.player()
    emptyPages = p.inv.searchEmptyInAllPage()
    if emptyPages:
        destPage, destPos = emptyPages[0]
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.CONFIRM, Functor(p.base.requireInv2wardrobeBag, destPage, destPos, itemUUID)), MBButton(gameStrings.CANCEL)]
        gameglobal.rds.ui.messageBox.show(True, '', gameStrings.WARDROBE_RETURN_ITEM_CONFIRM, buttons)
    else:
        p.showGameMsg(GMDD.data.BAG_FULL, ())


def getWardrobeItemNum(item):
    p = BigWorld.player()
    wardrobeItems = p.wardrobeBag.getDrobeItems()
    count = 0
    for uuid in wardrobeItems:
        wardrobeItem = wardrobeItems[uuid]
        if item.id == wardrobeItem.id or GBGIRD.data.get(item.id, 0) and GBGIRD.data.get(item.id, 0) == GBGIRD.data.get(wardrobeItem.id, 0):
            if getEquipType(wardrobeItem.id) == getEquipType(item.id) and getEquipSType(wardrobeItem.id) == getEquipSType(item.id):
                count += 1

    return count


def getEquipType(itemId):
    ed = ED.data.get(itemId, {})
    etp = ed.get('equipType', 0)
    return etp


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


def checkCanInsertInfoBag(item):
    p = BigWorld.player()
    bodyType = p.physique.bodyType
    if item.hasLatch():
        p.showGameMsg(GMDD.data.ITEM_STORAGE_LOCKED, ())
        return
    if not item.isCanDye():
        num = getWardrobeItemNum(item)
        if item.equipType == Item.EQUIP_BASETYPE_FASHION and item.equipSType == Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_LR:
            if num > 1:
                p.showGameMsg(GMDD.data.WARDROBE_HAVE_2_CANTDYE_TOUSHI, ())
        elif num > 0:
            p.showGameMsg(GMDD.data.WARDROBE_HAVE_CANTDYE_ITEM, ())
            return False
    if not utils.inAllowBodyType(item.id, bodyType):
        p.showGameMsg(GMDD.data.ITEM_USE_BODYTYPE_ERROR, ())
        return False
    if not utils.inAllowSex(item.id, p.physique.sex):
        p.showGameMsg(GMDD.data.WARDROBE_SEX_NOT_FIT, ())
        return False
    schReq = ID.data.get(item.id, {}).get('schReq', ())
    if schReq and p.school not in schReq:
        p.showGameMsg(GMDD.data.WARDROBE_SHCOOL_NOT_FIT, ())
        return False
    if hasattr(item, 'isExpireTTL') and item.isExpireTTL():
        p.showGameMsg(GMDD.data.ITEM_TTL_EXPIRE, (item.name,))
        return False
    if not GBGIRD.data.has_key(item.id):
        from data import gui_bao_ge_config_data as GBGCD
        filterIds = GBGCD.data.get('filterIds', ())
        if item.id not in filterIds:
            msg = 'cant insert cloth by itemId %s' % str(item.id)
            p.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, [msg], 0, {})
        p.showGameMsg(GMDD.data.ITEM_ID_NOT_IN_GUIBAOGE, ())
        return False
    return True
