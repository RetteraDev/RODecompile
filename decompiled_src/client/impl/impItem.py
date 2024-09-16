#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impItem.o
from gamestrings import gameStrings
import re
import BigWorld
import const
import gameglobal
import logicInfo
import gametypes
import utils
import gamelog
import clientcom
import formula
import commcalc
import time
import copy
from guis import uiConst
from helpers import cellCmd
from helpers import charRes
from helpers import action
from inventoryCommon import InventoryCommon
from item import Item
from guis import uiUtils
from guis import events
from helpers.eventDispatcher import Event
from callbackHelper import Functor
from itemRedemption import ItemRedemptionVal
from sfx import sfx
from gamestrings import gameStrings
from data import item_data as ID
from data import sys_config_data as SCD
from data import fame_data as FD
from data import map_config_data as MCD
from data import consumable_item_data as CID
from data import game_msg_data as GMD
from data import skill_general_data as SGD
from cdata import game_msg_def_data as GMDD
from data import equip_prefix_prop_data as EPFPD
from data import equip_synthesize_data as ESD
from data import equip_data as ED
from data import wabao_data as WBD

def pcharAdd(matchobj):
    m0 = matchobj.group(1)
    m1 = matchobj.group(2)
    m2 = matchobj.group(3)
    tempm0 = str(utils.strToUint64(m0))
    return "<font color=\'%s\'>[<a href = \'event:ret%s\'><u>%s</u></a>]</font>" % (m1, tempm0, m2)


class ImpItem(object):

    def itemCoolDown(self, itemId):
        bwTime = BigWorld.time()
        data = ID.data.get(itemId, {})
        cd = data.get('cd', 0)
        cdgroup = data.get('cdgroup', itemId)
        logicInfo.cooldownItem[itemId] = (cd + bwTime, cd)
        if cdgroup != None:
            logicInfo.commonCooldownItem[cdgroup] = (cd + bwTime, cd)
        gameglobal.rds.ui.actionbar.updateItemSlot()
        gameglobal.rds.ui.bfDotaItemAndProp.refreshItemCooldown()
        infos = [(gameglobal.BUFF_SKILL_TYPE_ITEM, itemId)]
        gameglobal.rds.ui.buffSkill.updateCooldown()

    def applyEngageSucc(self):
        self.wantToDoEmote(const.MARRIAGE_ENGAGE_EMOTEID)

    def syncBattleFieldDotaEquipCD(self, cdInfoDict):
        gamelog.debug('@lhb syncBattleFieldDotaEquipCD ', cdInfoDict)
        for itemId, endTime in cdInfoDict.iteritems():
            skillId = ED.data.get(itemId, {}).get('skillId', 0)
            skillLv = ED.data.get(itemId, {}).get('skillLv', 0)
            skillCd = SGD.data.get((skillId, skillLv), {}).get('cd', 0)
            endTime = BigWorld.time() + (endTime - utils.getNow())
            logicInfo.cooldownItem[itemId] = (int(endTime), skillCd)

        gameglobal.rds.ui.bfDotaItemAndProp.refreshItemCooldown()

    def showRandomXinshouItem(self, randomItemList, page, pos):
        gamelog.debug('@lhb randomItem ', randomItemList)
        if not gameglobal.rds.ui.itemPreviewSelect.widget:
            gameglobal.rds.ui.itemPreviewSelect.show(randomItemList, page, pos)
            gameglobal.rds.ui.inventory.hide()

    def showCanSelectItemList(self, itemId, page, pos):
        """
        ui\xe5\xb1\x95\xe7\xa4\xba\xe5\x8f\xaf\xe9\x80\x89item\xe5\x88\x97\xe8\xa1\xa8
        :param itemId: \xe5\x8f\xb3\xe9\x94\xae\xe4\xbd\xbf\xe7\x94\xa8\xe7\x9a\x84itemId
        :return:
        """
        gameglobal.rds.ui.itemChoose.show(itemId, showType=1, page=page, pos=pos)
        gamelog.debug('@zmm showCanSelectItemList itemId: ', itemId)

    def clearCD(self):
        logicInfo.cooldownItem.clear()
        logicInfo.commonCooldownItem.clear()
        gameglobal.rds.ui.actionbar.updateItemSlot()

    def releaseWaBaoLoopEff(self):
        if self.waBaoLoopEff:
            for i in self.waBaoLoopEff:
                if i:
                    i.stop()

        self.waBaoLoopEff = []

    def playWaBaoLoopEff(self, loopEff):
        effLv = self.getBasicEffectLv()
        priority = self.getBasicEffectPriority()
        self.waBaoLoopEff = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, [effLv,
         priority,
         self.model,
         loopEff,
         sfx.EFFECT_LIMIT_MISC])

    def doPlayWabaoTurn(self, info, itemId):
        self.waBaoUsingItemId = itemId
        treasureId = CID.data.get(itemId, {}).get('treasureId')
        if treasureId:
            loopAction = WBD.data.get(treasureId, {}).get('loopAction')
            loopEff = WBD.data.get(treasureId, {}).get('loopEff')
            actions = [(loopAction,
              None,
              0,
              action.WA_BAO_ACTION)]
            self.fashion.playActionSequence2(self.modelServer.bodyModel, actions, action.WA_BAO_ACTION)
            self.releaseWaBaoLoopEff()
            self.playWaBaoLoopEff(loopEff)
            if info:
                itemInfo = info.get('itemInfo')
                if itemInfo:
                    self.waBaoResuletItem = itemInfo[0]
            startEmote = WBD.data.get(treasureId, {}).get('startEmote')
            if startEmote:
                self.doEmote(startEmote)

    def getWaBaoRawardEffect(self, itemId):
        retEff = None
        resultTreasureLv = ID.data.get(itemId, {}).get('treasureLv')
        treasureLv = ID.data.get(self.waBaoUsingItemId, {}).get('treasureLv')
        treasureId = CID.data.get(self.waBaoUsingItemId, {}).get('treasureId')
        if resultTreasureLv > treasureLv:
            retEff = WBD.data.get(treasureId, {}).get('specialEff')
        else:
            retEff = WBD.data.get(treasureId, {}).get('normalEff')
        if retEff:
            retEff = int(retEff)
        return retEff

    def onWabaoRewardDone(self, itemId):
        treasureId = CID.data.get(self.waBaoUsingItemId, {}).get('treasureId')
        if treasureId:
            if getattr(self, 'life') != gametypes.LIFE_DEAD:
                endAction = WBD.data.get(treasureId, {}).get('endAction')
                eff = self.getWaBaoRawardEffect(itemId)
                playSeq = []
                playSeq.append((endAction,
                 [eff],
                 action.WA_BAO_ACTION,
                 0,
                 1,
                 None))
                self.fashion.playActionWithFx(playSeq, action.WA_BAO_ACTION, None, 1, keep=0, priority=self.getSkillEffectPriority())
        self.releaseWaBaoLoopEff()
        self.waBaoUsingItemId = None
        endEmote = WBD.data.get(treasureId, {}).get('endEmote')
        if endEmote:
            self.doEmote(endEmote)

    def stopWaBaoAction(self):
        if self.fashion.doingActionType() == action.WA_BAO_ACTION:
            if getattr(self, 'life') != gametypes.LIFE_DEAD:
                self.fashion.stopAllActions()
        self.releaseWaBaoLoopEff()
        self.waBaoUsingItemId = None

    def batchItemsCoolDown(self, items):
        logicInfo.cooldownItem.clear()
        logicInfo.commonCooldownItem.clear()
        bwTime = BigWorld.time()
        infos = []
        for itemId, t in items.iteritems():
            data = ID.data.get(itemId, {})
            cd = data.get('cd', 0)
            cdgroup = data.get('cdgroup', itemId)
            logicInfo.cooldownItem[itemId] = (t + bwTime, cd)
            if cdgroup != None:
                logicInfo.commonCooldownItem[cdgroup] = (t + bwTime, cd)
            infos.append((gameglobal.BUFF_SKILL_TYPE_ITEM, itemId))

        gameglobal.rds.ui.actionbar.updateItemSlot()
        gameglobal.rds.ui.bfDotaItemAndProp.refreshItemCooldown()
        gameglobal.rds.ui.buffSkill.updateCooldown()

    def itemWarmUp(self, id):
        logicInfo.cooldownItem.pop(id, None)
        data = ID.data.get(id, {})
        if data.get('stype', None) and data.get('type', None):
            type = data['type']
            stype = data['stype']
            logicInfo.commonCooldownItem.pop((type, stype), None)

    def __getBagByResKind(self, resKind):
        bagDict = {const.RES_KIND_INV: self.inv,
         const.RES_KIND_FASHION_BAG: self.fashionBag,
         const.RES_KIND_MATERIAL_BAG: self.materialBag,
         const.RES_KIND_STORAGE: self.storage,
         const.RES_KIND_ZAIJU_BAG: self.zaijuBag,
         const.RES_KIND_CROSS_INV: self.crossInv,
         const.RES_KIND_SPRITE_MATERIAL_BAG: self.spriteMaterialBag,
         const.RES_KIND_HIEROGRAM_BAG: self.hierogramBag}
        if bagDict.has_key(resKind):
            return bagDict[resKind]
        raise NotImplementedError()

    def removeAllCommonItem(self, resKind):
        bag = self.__getBagByResKind(resKind)
        removeFuncDict = {const.RES_KIND_INV: lambda pg, ps: gameglobal.rds.ui.inventory.removeItem(pg, ps),
         const.RES_KIND_MATERIAL_BAG: lambda pg, ps: gameglobal.rds.ui.inventory.removeSackItem(const.MATERIAL_BAG_BIND_ID, ps),
         const.RES_KIND_FASHION_BAG: lambda pg, ps: gameglobal.rds.ui.fashionBag.removeItem(pg, ps),
         const.RES_KIND_STORAGE: lambda pg, ps: gameglobal.rds.ui.storage.removeItem(pg, ps),
         const.RES_KIND_ZAIJU_BAG: lambda pg, ps: None,
         const.RES_KIND_SPRITE_MATERIAL_BAG: lambda pg, ps: gameglobal.rds.ui.spriteMaterialBag.removeItem(pg, ps),
         const.RES_KIND_CROSS_INV: lambda pg, ps: gameglobal.rds.ui.crossServerBag.removeItem(pg, ps)}
        for pg in bag.getPageTuple():
            for ps in bag.getPosTuple(pg):
                if bag.getQuickVal(pg, ps):
                    removeFunc = removeFuncDict.get(resKind, None)
                    removeFunc and removeFunc(pg, ps)
                    bag.removeObj(pg, ps)

    def canPush(self, item):
        if item.isRubbing():
            return False
        if not hasattr(item, 'score'):
            return False
        p = BigWorld.player()
        part = item.whereEquip()
        if item.canEquip(p, part[0]) != Item.EQUIPABLE:
            return False
        for idNum in xrange(len(part)):
            if p.equipment.isEmpty(part[idNum]):
                return True
            if p.equipment.get(part[idNum]).score < item.score:
                return True

        return False

    def checkPushEquip(self, pushEq, uuid):
        part = pushEq.whereEquip()
        equip, _, _ = BigWorld.player().inv.findItemByUUID(uuid)
        if equip != const.CONT_EMPTY_VAL:
            if equip.whereEquip() == part:
                if equip.score < pushEq.score:
                    return uiConst.EQUIP_PUSH_REPLACE
                else:
                    return uiConst.EQUIP_PUSH_NONE
        return uiConst.EQUIP_PUSH_NORMAL

    def pushEquip(self, pushEq):
        if gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_GET_EQUIP) or self.inCombat and not (gameglobal.rds.ui.equipPush.mediator or gameglobal.rds.ui.equipPush.dataList):
            dataTuple = tuple(gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_GET_EQUIP))
            for item in dataTuple:
                result = self.checkPushEquip(pushEq, item['data'])
                if result == uiConst.EQUIP_PUSH_REPLACE:
                    gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_GET_EQUIP, item)
                elif result == uiConst.EQUIP_PUSH_NONE:
                    return

            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GET_EQUIP, {'data': pushEq.uuid})
        else:
            if gameglobal.rds.ui.equipPush.uuid:
                result = self.checkPushEquip(pushEq, gameglobal.rds.ui.equipPush.uuid)
                if result == uiConst.EQUIP_PUSH_REPLACE:
                    gameglobal.rds.ui.equipPush.close()
                elif result == uiConst.EQUIP_PUSH_NONE:
                    return
            dataTuple = tuple(gameglobal.rds.ui.equipPush.dataList)
            for uuid in dataTuple:
                result = self.checkPushEquip(pushEq, uuid)
                if result == uiConst.EQUIP_PUSH_REPLACE:
                    gameglobal.rds.ui.equipPush.dataList.remove(uuid)
                elif result == uiConst.EQUIP_PUSH_NONE:
                    return

            gameglobal.rds.ui.equipPush.dataList.append(pushEq.uuid)
            if not gameglobal.rds.ui.equipPush.mediator:
                gameglobal.rds.ui.equipPush.show()
        BigWorld.callback(SCD.data.get('autoCloseEquipPushCD', 120), Functor(gameglobal.rds.ui.equipPush.forceColse, pushEq.uuid))

    def lvUpEquipPush(self):
        allEquip = self.inv.findAllItemByAttr({'type': Item.BASETYPE_EQUIP})
        for pg, ps in allEquip:
            equip = self.inv.getQuickVal(pg, ps)
            if self.canPush(equip) and equip.lvReq and self.lv == equip.lvReq:
                self.pushEquip(equip)

    def delCompositeShopInfo(self, resKind, page, pos):
        bag = self._getUseBag(resKind)
        if bag:
            it = bag.getQuickVal(page, pos)
            if it and hasattr(it, 'compositeShopInfo'):
                delattr(it, 'compositeShopInfo')

    def autoSortInsert(self, kind, item, page, pos):
        if kind == const.RES_KIND_INV:
            self.inv.insertObj(item, page, pos)
            gameglobal.rds.ui.inventory.addItem(item, page, pos)
        elif kind == const.RES_KIND_STORAGE:
            self.storage.insertObj(item, page, pos)
            gameglobal.rds.ui.storage.addItem(item, page, pos)
        elif kind == const.RES_KIND_MATERIAL_BAG:
            self.materialBag.insertObj(item, page, pos)
            gameglobal.rds.ui.inventory.addSackItem(item, const.MATERIAL_BAG_BIND_ID, pos)
            gameglobal.rds.ui.meterialBag.addItem(item, page, pos)
        elif kind == const.RES_KIND_FASHION_BAG:
            self.fashionBag.insertObj(item, page, pos)
            gameglobal.rds.ui.fashionBag.addItem(item, page, pos)
        elif kind == const.RES_KIND_RIDE_WING_BAG:
            self.rideWingBag.insertObj(item, page, pos)
            if gameglobal.rds.ui.wingAndMount.mediator:
                gameglobal.rds.ui.wingAndMount.addItem(item, page, pos + 1)
        elif kind == const.RES_KIND_ZAIJU_BAG:
            self.zaijuBag.insertObj(item, page, pos)
            gameglobal.rds.ui.guildBusinessBag.updateItem(item, page, pos)
        elif kind == const.RES_KIND_SPRITE_MATERIAL_BAG:
            self.spriteMaterialBag.insertObj(item, page, pos)
            gameglobal.rds.ui.spriteMaterialBag.addItem(item, page, pos)
        elif kind == const.RES_KIND_HIEROGRAM_BAG:
            self.hierogramBag.insertObj(item, page, pos)
        elif kind == const.RES_KIND_CROSS_INV:
            self.crossInv.insertObj(item, page, pos)
            gameglobal.rds.ui.crossServerBag.addItem(item, page, pos)
        BigWorld.player().dispatchEvent(const.EVENT_ITEM_SORT, (kind,
         page,
         pos,
         item))

    def _resInsert(self, kind, item, page, pos, isNew = False):
        gamelog.debug('@hjx inventory#resInsert:', kind, item, page, pos, isNew)
        isNeedTriggerTutorial = False
        if kind == const.RES_KIND_INV:
            self.inv.insertObj(item, page, pos)
            if isNew and uiUtils._checkItemNewFlag(item=item):
                if item.uuid not in gameglobal.rds.ui.inventory.newItemSequence:
                    gameglobal.rds.ui.inventory.newItemSequence.append(item.uuid)
                if self.canPush(item):
                    self.pushEquip(item)
            gameglobal.rds.ui.inventory.addItem(item, page, pos)
            gameglobal.rds.ui.actionbar.refreshByBagUse(item)
            if gameglobal.rds.ui.compositeShop.isOpen:
                gameglobal.rds.ui.compositeShop.refreshBuyItemDisplayData()
            if gameglobal.rds.ui.skill.daoHangDirMediator:
                gameglobal.rds.ui.skill.refreshHaoHangDirectionPanel()
            if gameglobal.rds.ui.skill.enhanceMediator:
                if gameglobal.rds.ui.skill.enhanceType == uiConst.TYPE_XIUWEI_BAR:
                    gameglobal.rds.ui.skill.refreshXiuWeiBarInfo()
                elif gameglobal.rds.ui.skill.enhanceType == uiConst.TYPE_WUSHUANG_BAR:
                    gameglobal.rds.ui.skill.refreshWuShuangBarInfo()
                elif gameglobal.rds.ui.skill.enhanceType == uiConst.TYPE_RELIEVE:
                    gameglobal.rds.ui.skill.refreshRelieveInfo()
            if gameglobal.rds.ui.equipMix.mediator:
                gameglobal.rds.ui.equipMix.refresh()
            if gameglobal.rds.ui.equipEnhance.mediator:
                gameglobal.rds.ui.equipEnhance.refreshContent()
            isNeedTriggerTutorial = True
            gameglobal.rds.ui.roleInfo.updateSocialPanel()
            gameglobal.rds.ui.skill.refreshDetailInfo()
            gameglobal.rds.ui.equipSoulStar.refreshInfo()
            gameglobal.rds.ui.itemSelect.refreshItemList()
            if ID.data.get(item.id, {}).get('usePush', None) and isNew and gameglobal.rds.configData.get('enableItemUsePush', True):
                gameglobal.rds.ui.itemPushUse.isPush = True
                gameglobal.rds.ui.itemPushUse.isActionClick = False
                gameglobal.rds.ui.itemPushUse.isClickPush = False
                if item.type == Item.BASETYPE_PACK:
                    gameglobal.rds.ui.itemPushUse.show(item.uuid)
                else:
                    BigWorld.player().cell.checkUseCommonItem(page, pos, const.RES_KIND_INV)
            if CID.data.get(item.id, {}).get('autoUse', None):
                BigWorld.player().cell.useCommonItem(page, pos, 1, kind)
        elif kind == const.RES_KIND_CROSS_INV:
            self.crossInv.insertObj(item, page, pos)
            gameglobal.rds.ui.crossServerBag.addItem(item, page, pos)
            gameglobal.rds.ui.actionbar.refreshByBagUse(item)
            BigWorld.player().setUseItemAutoInPubg(kind, item, page, pos, isNew)
        elif kind == const.RES_KIND_QUEST_BAG:
            self.questBag.insertObj(item, page, pos)
            gameglobal.rds.ui.inventory.addItem(item, uiConst.BAG_PAGE_QUEST, pos)
            isNeedTriggerTutorial = True
        elif kind == const.RES_KIND_EQUIP:
            oldItem = self.equipment.get(pos)
            if oldItem != const.CONT_EMPTY_VAL and not oldItem.isShihun() and item.isShihun():
                gameglobal.rds.tutorial.onEquipShiHun()
            self.equipment.set(pos, item)
            page = const.RES_KIND_EQUIP
            gameglobal.rds.ui.actionbar.setItem(item, uiConst.EQUIP_ACTION_BAR, pos, sType=uiConst.SHORTCUT_TYPE_ITEM_EQUIP)
            gameglobal.rds.ui.equipRepair.setEquipState()
        elif kind == const.RES_KIND_INV_BAR:
            self.bagBar.insertObj(item, page, pos)
            gameglobal.rds.ui.inventory.addSackItem(item, const.BAG_BAR_BIND_ID, pos)
        elif kind == const.RES_KIND_FASHION_BAG:
            self.fashionBag.insertObj(item, page, pos)
            gameglobal.rds.ui.fashionBag.refresh()
        elif kind == const.RES_KIND_MATERIAL_BAG:
            self.materialBag.insertObj(item, page, pos)
            gameglobal.rds.ui.inventory.addSackItem(item, const.MATERIAL_BAG_BIND_ID, pos)
            gameglobal.rds.ui.meterialBag.addItem(item, page, pos)
        elif kind == const.RES_KIND_CART:
            self.cart.insertObj(item, page, pos)
            gameglobal.rds.ui.inventory.addSackItem(item, const.CART_BIND_ID, pos)
        elif kind == const.RES_KIND_TEMP_BAG:
            self.tempBag.insertObj(item, page, pos)
            isInterruptUpdate = gameglobal.rds.ui.activitySaleLuckyLottery.checkIsDrawingLuckyItem(item, page, pos)
            if not isInterruptUpdate:
                gameglobal.rds.ui.inventory.openTempBag()
                gameglobal.rds.ui.inventory.addSackItem(item, const.TEMP_BAG_BIND_ID, pos)
                gameglobal.rds.ui.inventory.updateTempBagNum()
        elif kind == const.RES_KIND_STORAGE:
            self.storage.insertObj(item, page, pos)
            gameglobal.rds.ui.storage.addItem(item, page, pos)
        elif kind == const.RES_KIND_STORAGE_BAR:
            self.storageBar.insertObj(item, page, pos)
            gameglobal.rds.ui.storage.addBarItem(item, pos)
        elif kind == const.RES_KIND_FASHION_BAG_BAR:
            self.fashionBagBar.insertObj(item, page, pos)
            gameglobal.rds.ui.fashionBag.addBarItem(item, pos)
        elif kind == const.RES_KIND_MATERIAL_BAG_BAR:
            self.materialBagBar.insertObj(item, page, pos)
            gameglobal.rds.ui.meterialBag.addBarItem(item, pos)
        elif kind == const.RES_KIND_FISHING_QUIP:
            self.fishingEquip.set(pos, item)
        elif kind == const.RES_KIND_BOOTH:
            if hasattr(item, 'remainNum'):
                item.canOverMax = True
                item.cwrap = item.remainNum
            self.booth.insertObj(item, page, pos)
            gameglobal.rds.ui.booth.addItem(item, page, pos)
        elif kind == const.RES_KIND_EXPLORE_EQUIP:
            self.exploreEquip.set(pos, item)
            if pos == gametypes.EXPLORE_EQUIP_SCROLL:
                gameglobal.rds.ui.explore.refreshExplorePanel()
            else:
                gameglobal.rds.ui.explore.refreshEquip()
                gameglobal.rds.ui.skill.refreshExploreSkill()
        elif kind == const.RES_KIND_LIFE_EQUIP:
            self.lifeEquipment.set(page, pos, item)
            gameglobal.rds.ui.roleInfo.updateSocialPanel()
        elif kind == const.RES_KIND_MALL_BAG:
            self.mallBag.insertObj(item, page, pos)
            gameglobal.rds.ui.inventory.addSackItem(item, const.MALL_BAR_BIND_ID, pos)
            gameglobal.rds.ui.inventory.updateMallTempBagNum()
        elif kind == const.RES_KIND_ZAIJU_BAG:
            self.zaijuBag.insertObj(item, page, pos)
            gameglobal.rds.ui.guildBusinessBag.updateItem(item, page, pos)
        elif kind == const.RES_KIND_SUB_EQUIP_BAG:
            self.subEquipment.setQuickVal(item, page, pos)
            subPos = gametypes.subEquipToEquipPartMap.get(pos, -1)
            page = const.RES_KIND_SUB_EQUIP_BAG
            if subPos != -1:
                subPos += const.SUB_EQUIP_PART_OFFSET
                gameglobal.rds.ui.actionbar.setItem(item, uiConst.EQUIP_ACTION_BAR, subPos, sType=uiConst.SHORTCUT_TYPE_ITEM_EQUIP)
            BigWorld.callback(0.2, gameglobal.rds.ui.roleInfo.refreshInfo)
        elif kind == const.RES_KIND_BATTLE_FIELD_BAG:
            self.battleFieldBag[pos] = item
            gameglobal.rds.sound.playSound(5622)
            gameglobal.rds.ui.bfDotaShop.refreshByBuyItemSucc(item.id)
            self.onBuyItem(item.id)
            gameglobal.rds.ui.bfDotaItemAndProp.refreshItemSlots([pos])
        elif kind == const.RES_KIND_SPRITE_MATERIAL_BAG:
            self.spriteMaterialBag.insertObj(item, page, pos)
            gameglobal.rds.ui.spriteMaterialBag.addItem(item, page, pos)
        elif kind == const.RES_KIND_SPRITE_MATERIAL_BAG_BAR:
            self.spriteMaterialBagBar.insertObj(item, page, pos)
            gameglobal.rds.ui.spriteMaterialBag.addBarItem(item, pos)
        elif kind == const.RES_KIND_HIEROGRAM_BAG:
            self.hierogramBag.insertObj(item, page, pos)
        elif kind == const.RES_KIND_HIEROGRAM_BAG_BAR:
            self.hierogramBagBar.insertObj(item, page, pos)
        if isNeedTriggerTutorial and isNew:
            if item:
                gameglobal.rds.tutorial.onGetItem(item.id)
        if kind == const.RES_KIND_RIDE_WING_BAG:
            self.rideWingBag.insertObj(item, page, pos)
            if gameglobal.rds.ui.wingAndMount.mediator:
                gameglobal.rds.ui.wingAndMount.addItem(item, page, pos + 1)
        if kind == const.RES_KIND_EQUIP and (pos == gametypes.EQU_PART_WINGFLY or pos == gametypes.EQU_PART_RIDE):
            if gameglobal.rds.ui.wingAndMount.mediator:
                if pos == gametypes.EQU_PART_WINGFLY:
                    targetPos = 1
                else:
                    targetPos = 0
                gameglobal.rds.ui.wingAndMount.addItem(item, targetPos, 0)
        self.checkExpireItem(item)

    def resInsertNew(self, kind, item, page, pos):
        if gameglobal.rds.ui.randomTreasureBagMain.drawing:
            gameglobal.rds.ui.randomTreasureBagMain.enQueueLotteryItem(kind, item, page, pos)
            return
        self._resInsert(kind, item, page, pos, True)
        BigWorld.player().dispatchEvent(const.EVENT_ITEM_CHANGE, (kind,
         page,
         pos,
         item))

    def resInsert(self, kind, item, page, pos):
        if gameglobal.rds.ui.activitySaleLottery.isLotterying == True:
            gameglobal.rds.ui.activitySaleLottery.setLotteryItem(kind, item, page, pos)
            return
        if gameglobal.rds.ui.activitySaleRandomCardDraw.isShowingResult == True:
            gameglobal.rds.ui.activitySaleRandomCardDraw.setCardDrawItem(kind, item, page, pos)
            return
        if gameglobal.rds.ui.randomTreasureBagMain.drawing:
            gameglobal.rds.ui.randomTreasureBagMain.enQueueLotteryItem(kind, item, page, pos)
            return
        self._resInsert(kind, item, page, pos)
        BigWorld.player().dispatchEvent(const.EVENT_ITEM_CHANGE, (kind,
         page,
         pos,
         item))

    def showEquipLabel(self):
        self.showEquipLabelCallback = 0
        if not hasattr(self, 'oldRadarDataCache'):
            return
        radarData = commcalc.createSelfRadarChartData(BigWorld.player(), True)
        gameglobal.rds.ui.showEquipLabel([int(radarData[0]) - int(self.oldRadarDataCache[0]),
         int(radarData[1]) - int(self.oldRadarDataCache[1]),
         int(radarData[2]) - int(self.oldRadarDataCache[2]),
         int(radarData[3]) - int(self.oldRadarDataCache[3]),
         int(radarData[4]) - int(self.oldRadarDataCache[4])])

    def resSet(self, kind, item, page, pos):
        if kind == const.RES_KIND_EQUIP:
            if hasattr(self, 'showEquipLabelCallback') and self.showEquipLabelCallback:
                BigWorld.cancelCallback(self.showEquipLabelCallback)
            else:
                self.oldRadarDataCache = commcalc.createSelfRadarChartData(BigWorld.player(), True)
            self.showEquipLabelCallback = BigWorld.callback(0.5, self.showEquipLabel)
            self.equipment.set(pos, item)
            if not item:
                return
            gameglobal.rds.ui.equipPush.forceColse(item.uuid)
            page = const.RES_KIND_EQUIP
            if gameglobal.rds.ui.roleInfo.tabIdx == uiConst.ROLEINFO_TAB_FASHION:
                gameglobal.rds.ui.roleInfo.setFashionItem(item, page, pos)
            else:
                gameglobal.rds.ui.actionbar.setItem(item, page, pos, sType=uiConst.SHORTCUT_TYPE_ITEM_EQUIP)
            if not item.isWingOrRide():
                gameglobal.rds.ui.roleInfo.onCheckEquipStarLvUp(pos)
            gameglobal.rds.ui.equipRepair.setEquipState()
            gameglobal.rds.ui.skill.refreshOtherSkillPanel()
            gameglobal.rds.ui.skill.refreshEmotePanel()
            gameglobal.rds.ui.actionbar.refreshByBagUse(item)
            BigWorld.callback(0.2, gameglobal.rds.ui.roleInfo.refreshInfo)
            gameglobal.rds.tutorial.onSetEquip(item.id)
            if gameglobal.rds.ui.equipFeed.mediator:
                gameglobal.rds.ui.equipFeed.refreshContent(True)
            gameglobal.rds.ui.playUseItemSound(item)
            player = BigWorld.player()
            headEquip = player.equipment[gametypes.EQU_PART_FASHION_HEAD]
            if headEquip:
                headType = charRes.getHeadType(headEquip.id)
                if getattr(item, 'equipType', None) == Item.EQUIP_BASETYPE_FASHION:
                    if headType == charRes.HEAD_TYPE1:
                        if getattr(item, 'equipSType', None) in (Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_ASSEMBLE,
                         Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_FRONT,
                         Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_LR,
                         Item.EQUIP_FASHION_SUBTYPE_FACEWEAR):
                            player.showGameMsg(GMDD.data.FASHION_ITEM_NOT_SHOW, item.name)
            if getattr(self, 'intimacyTgtEnter', False) and getattr(self, 'intimacyTgtId', None):
                if getattr(item, 'signerOne', None) or getattr(item, 'signerTwo', None):
                    self.cell.checkIntimacyTgt(self.intimacyTgtId, self.intimacyTgtEnter)
        elif kind == const.RES_KIND_SUB_EQUIP_BAG:
            self.subEquipment.setQuickVal(item, page, pos)
            subPos = gametypes.subEquipToEquipPartMap.get(pos, -1)
            page = const.RES_KIND_SUB_EQUIP_BAG
            if subPos != -1:
                subPos += const.SUB_EQUIP_PART_OFFSET
                gameglobal.rds.ui.actionbar.setItem(item, uiConst.EQUIP_ACTION_BAR, subPos, sType=uiConst.SHORTCUT_TYPE_ITEM_EQUIP)
            BigWorld.callback(0.2, gameglobal.rds.ui.roleInfo.refreshInfo)
        elif kind == const.RES_KIND_INV:
            itemOld = self.inv.getQuickVal(page, pos)
            if itemOld and not item:
                gameglobal.rds.ui.inventory.removeItem(page, pos)
            if item:
                self.inv.insertObj(item, page, pos)
                gameglobal.rds.ui.inventory.addItem(item, page, pos)
                if gameglobal.rds.ui.equipGem.mediator and gameglobal.rds.ui.equipGem.srcPos[0] == page and gameglobal.rds.ui.equipGem.srcPos[1] == pos:
                    gameglobal.rds.ui.equipGem.resSetPanel(item, page, pos)
                if gameglobal.rds.ui.equipmentSlot.mediator and gameglobal.rds.ui.equipmentSlot.srcPos[0] == page and gameglobal.rds.ui.equipmentSlot.srcPos[1] == pos:
                    gameglobal.rds.ui.equipmentSlot.resSetPanel(item, page, pos)
                if gameglobal.rds.ui.huiZhangRepair.mediator and gameglobal.rds.ui.huiZhangRepair.equipPage == page and gameglobal.rds.ui.huiZhangRepair.equipPos == pos:
                    gameglobal.rds.ui.huiZhangRepair.succeed()
            else:
                self.inv.removeObj(page, pos)
                gameglobal.rds.ui.inventory.removeItem(page, pos)
            if itemOld:
                gameglobal.rds.ui.actionbar.refreshByBagUse(itemOld)
            if gameglobal.rds.ui.equipFeed.mediator:
                gameglobal.rds.ui.equipFeed.refreshContent(True)
            if gameglobal.rds.ui.equipEnhance.mediator:
                gameglobal.rds.ui.equipEnhance.refreshContent()
            if page == gameglobal.rds.ui.runeForging.invPage and pos == gameglobal.rds.ui.runeForging.invPos:
                gameglobal.rds.ui.runeForging.refreshRuneEquip()
            if page == gameglobal.rds.ui.runeReforging.invPage and pos == gameglobal.rds.ui.runeReforging.invPos:
                gameglobal.rds.ui.runeReforging.refreshRuneEquip()
            if gameglobal.rds.ui.equipMix.mediator:
                gameglobal.rds.ui.equipMix.refresh()
            if gameglobal.rds.ui.equipEnhance.mediator:
                gameglobal.rds.ui.equipEnhance.refreshContent()
            if gameglobal.rds.ui.itemRecast.recastMed:
                gameglobal.rds.ui.itemRecast.refreshMatchIds()
            gameglobal.rds.ui.skill.refreshDetailInfo()
            gameglobal.rds.ui.equipSoulStar.refreshInfo()
            gameglobal.rds.ui.itemSelect.refreshItemList()
            if gameglobal.rds.ui.schoolTransferEquip.widget:
                gameglobal.rds.ui.schoolTransferEquip.refreshInfo()
        elif kind == const.RES_KIND_CROSS_INV:
            self.crossInv.insertObj(item, page, pos)
            gameglobal.rds.ui.crossServerBag.addItem(item, page, pos)
        elif kind == const.RES_KIND_QUEST_BAG:
            if item:
                self.questBag.insertObj(item, page, pos)
                gameglobal.rds.ui.inventory.addItem(item, uiConst.BAG_PAGE_QUEST, pos)
            else:
                self.questBag.removeObj(page, pos)
                gameglobal.rds.ui.inventory.removeItem(uiConst.BAG_PAGE_QUEST, pos)
        elif kind == const.RES_KIND_INV_BAR:
            if item:
                self.bagBar.insertObj(item, page, pos)
                gameglobal.rds.ui.inventory.addSackItem(item, const.BAG_BAR_BIND_ID, pos)
            else:
                self.bagBar.removeObj(page, pos)
                gameglobal.rds.ui.inventory.removeSackItem(const.BAG_BAR_BIND_ID, pos)
        elif kind == const.RES_KIND_FASHION_BAG:
            if item:
                self.fashionBag.insertObj(item, page, pos)
                gameglobal.rds.ui.inventory.addSackItem(item, const.FASHION_BAG_BIND_ID, pos)
            else:
                self.fashionBag.removeObj(page, pos)
                gameglobal.rds.ui.inventory.removeSackItem(const.FASHION_BAG_BIND_ID, pos)
        elif kind == const.RES_KIND_MATERIAL_BAG:
            if item:
                self.materialBag.insertObj(item, page, pos)
                gameglobal.rds.ui.inventory.addSackItem(item, const.MATERIAL_BAG_BIND_ID, pos)
                gameglobal.rds.ui.meterialBag.addItem(item, page, pos)
            else:
                self.materialBag.removeObj(page, pos)
                gameglobal.rds.ui.inventory.removeSackItem(const.MATERIAL_BAG_BIND_ID, pos)
                gameglobal.rds.ui.meterialBag.removeItem(page, pos)
        elif kind == const.RES_KIND_SPRITE_MATERIAL_BAG:
            if item:
                self.spriteMaterialBag.insertObj(item, page, pos)
                gameglobal.rds.ui.spriteMaterialBag.addItem(item, page, pos)
            else:
                self.spriteMaterialBag.removeObj(page, pos)
                gameglobal.rds.ui.spriteMaterialBag.removeItem(page, pos)
        elif kind == const.RES_KIND_CART:
            if item:
                self.cart.insertObj(item, page, pos)
                gameglobal.rds.ui.inventory.addSackItem(item, const.CART_BIND_ID, pos)
            else:
                self.cart.removeObj(page, pos)
                gameglobal.rds.ui.inventory.removeSackItem(const.CART_BIND_ID, pos)
        elif kind == const.RES_KIND_TEMP_BAG:
            if item:
                self.tempBag.insertObj(item, page, pos)
                gameglobal.rds.ui.inventory.addSackItem(item, const.TEMP_BAG_BIND_ID, pos)
            else:
                self.tempBag.removeObj(page, pos)
                gameglobal.rds.ui.inventory.removeSackItem(const.TEMP_BAG_BIND_ID, pos)
            gameglobal.rds.ui.inventory.updateTempBagNum()
        elif kind == const.RES_KIND_STORAGE:
            if item:
                self.storage.insertObj(item, page, pos)
                gameglobal.rds.ui.storage.addItem(item, page, pos)
            else:
                self.storage.removeObj(page, pos)
                gameglobal.rds.ui.storage.removeItem(page, pos)
        elif kind == const.RES_KIND_STORAGE_BAR:
            if item:
                self.storageBar.insertObj(item, page, pos)
                gameglobal.rds.ui.storage.addBarItem(item, pos)
            else:
                self.storageBar.removeObj(page, pos)
                gameglobal.rds.ui.storage.removeBarItem(pos)
        elif kind == const.RES_KIND_FASHION_BAG_BAR:
            if item:
                self.fashionBagBar.insertObj(item, page, pos)
                gameglobal.rds.ui.fashionBag.addBarItem(item, pos)
            else:
                self.fashionBagBar.removeObj(page, pos)
                gameglobal.rds.ui.fashionBag.removeBarItem(pos)
        elif kind == const.RES_KIND_MATERIAL_BAG_BAR:
            if item:
                self.materialBagBar.insertObj(item, page, pos)
                gameglobal.rds.ui.meterialBag.addBarItem(item, pos)
            else:
                self.materialBagBar.removeObj(page, pos)
                gameglobal.rds.ui.meterialBag.removeBarItem(pos)
        elif kind == const.RES_KIND_SPRITE_MATERIAL_BAG_BAR:
            if item:
                self.spriteMaterialBagBar.insertObj(item, page, pos)
                gameglobal.rds.ui.spriteMaterialBag.addBarItem(item, pos)
            else:
                self.spriteMaterialBagBar.removeObj(page, pos)
                gameglobal.rds.ui.spriteMaterialBag.removeBarItem(pos)
        elif kind == const.RES_KIND_FISHING_QUIP:
            self.fishingEquip.set(pos, item)
            gameglobal.rds.ui.fishing.refreshFishingPanel()
            gameglobal.rds.ui.fishing.refreshBaitSlot()
            gameglobal.rds.ui.roleInfo.updateSocialPanel()
        elif kind == const.RES_KIND_EXPLORE_EQUIP:
            self.exploreEquip.set(pos, item)
            if pos == gametypes.EXPLORE_EQUIP_SCROLL:
                gameglobal.rds.ui.explore.refreshExplorePanel()
            else:
                gameglobal.rds.ui.explore.refreshEquip()
                gameglobal.rds.ui.skill.refreshExploreSkill()
            gameglobal.rds.ui.roleInfo.updateSocialPanel()
        elif kind == const.RES_KIND_ZAIJU_BAG:
            if item:
                self.zaijuBag.insertObj(item, page, pos)
            else:
                self.zaijuBag.removeObj(page, pos)
            gameglobal.rds.ui.guildBusinessBag.updateItem(item, page, pos)
        elif kind == const.RES_KIND_HIEROGRAM_CRYSTALS:
            hieroCrystals = self.hierogramDict.get('hieroCrystals', None)
            if not hieroCrystals:
                return
            oldIt = hieroCrystals.get((page, pos), const.CONT_EMPTY_VAL)
            if oldIt and item and oldIt.uuid != item.uuid:
                return
            hieroCrystals[page, pos] = item
        if kind == const.RES_KIND_RIDE_WING_BAG:
            if item:
                self.rideWingBag.insertObj(item, page, pos)
            else:
                self.rideWingBag.removeObj(page, pos)
            if gameglobal.rds.ui.wingAndMount.mediator:
                gameglobal.rds.ui.wingAndMount.addItem(item, page, pos + 1)
        if kind == const.RES_KIND_EQUIP and (pos == gametypes.EQU_PART_WINGFLY or pos == gametypes.EQU_PART_RIDE):
            if gameglobal.rds.ui.wingAndMount.mediator:
                if pos == gametypes.EQU_PART_WINGFLY:
                    targetPos = 1
                else:
                    targetPos = 0
                gameglobal.rds.ui.wingAndMount.addItem(item, targetPos, 0)
        self.checkExpireItem(item)
        self.setDotaItemCoolDown(item)
        self.fillGemToEquipments()
        BigWorld.player().dispatchEvent(const.EVENT_ITEM_CHANGE, (kind,
         page,
         pos,
         item))

    def checkManualRefiningEffect(self):
        shouldPlayEffect = False
        if not getattr(self, 'firstFetchFinished', False):
            return
        manualEquipEffectAttached = getattr(self, 'manualEquipEffectAttached', False)
        effectId = SCD.data.get('manualEquipEffect', 118131)
        if shouldPlayEffect:
            if not manualEquipEffectAttached:
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getEquipEffectLv(),
                 self.getEquipEffectPriority(),
                 self.model,
                 effectId,
                 sfx.EFFECT_UNLIMIT))
                self.addFx(effectId, fx)
            self.manualEquipEffectAttached = True
        else:
            if self.manualEquipEffectAttached:
                self.removeFx(effectId)
            self.manualEquipEffectAttached = False

    def setDotaItemCoolDown(self, item):
        if Item.isDotaBattleFieldItem(item.id) and item.isEquip():
            skillId = ED.data.get(item.id, {}).get('skillId', 0)
            skillLv = ED.data.get(item.id, {}).get('skillLv', 0)
            skillCd = SGD.data.get((skillId, skillLv), {}).get('cd', 0)
            if skillCd:
                logicInfo.cooldownItem[item.id] = (BigWorld.time() + skillCd, skillCd)
                gameglobal.rds.ui.bfDotaItemAndProp.refreshItemCooldown()

    def buyBackResSet(self, item, page, pos):
        if page not in self.buyBackDict:
            self.buyBackDict[page] = [None] * const.BUY_BACK_LIST_SIZE
        self.buyBackDict[page][pos] = item
        if page == const.BUY_BACK_SHOP_PAGE:
            gameglobal.rds.ui.shop.updateBuyBackItem()
        else:
            gameglobal.rds.ui.compositeShop.updateBuyBackItem()
            gameglobal.rds.ui.yunChuiShop.updateBuybackItem()

    def resRemove(self, kind, page, pos):
        item = None
        if kind == const.RES_KIND_INV:
            item = self.inv.getQuickVal(page, pos)
            if item == const.CONT_EMPTY_VAL:
                return
            if item.type == Item.BASETYPE_EQUIP:
                gameglobal.rds.ui.equipPush.forceColse(item.uuid)
            if item.uuid in gameglobal.rds.ui.inventory.newItemSequence:
                gameglobal.rds.ui.inventory.newItemSequence.remove(item.uuid)
            gameglobal.rds.ui.inventory.removeItem(page, pos)
            self.inv.removeObj(page, pos)
            gameglobal.rds.ui.actionbar.refreshByBagUse(item)
            if gameglobal.rds.ui.compositeShop.isOpen:
                gameglobal.rds.ui.compositeShop.refreshBuyItemDisplayData()
            if gameglobal.rds.ui.payItem.mediator:
                gameglobal.rds.ui.payItem.refreshPayBag()
            if gameglobal.rds.ui.equipMix.mediator:
                gameglobal.rds.ui.equipMix.refresh()
            gameglobal.rds.ui.skill.refreshDetailInfo()
            gameglobal.rds.ui.equipSoulStar.refreshInfo()
            gameglobal.rds.ui.itemSelect.refreshItemList()
            gameglobal.rds.ui.purchaseShop.refreshItems()
            if gameglobal.rds.ui.inventory.tempBagMediator and gameglobal.rds.ui.inventory.tempBagType == uiConst.INVENTORY_TEMP_BAG_MATERIAL:
                gameglobal.rds.ui.inventory.openTempBagByType(uiConst.INVENTORY_TEMP_BAG_MATERIAL)
        elif kind == const.RES_KIND_CROSS_INV:
            item = self.crossInv.getQuickVal(page, pos)
            self.crossInv.removeObj(page, pos)
            gameglobal.rds.ui.crossServerBag.removeItem(page, pos)
            gameglobal.rds.ui.actionbar.refreshByBagUse(item)
        elif kind == const.RES_KIND_QUEST_BAG:
            item = self.questBag.getQuickVal(page, pos)
            if item == const.CONT_EMPTY_VAL:
                return
            if hasattr(item, 'cstype') and item.cstype == Item.SUBTYPE_2_GUILD_BUSINESS_FIND_PATH:
                if gameglobal.rds.ui.guildBusinessFindPath.mediator:
                    gameglobal.rds.ui.guildBusinessFindPath.hide()
            gameglobal.rds.ui.inventory.removeItem(uiConst.BAG_PAGE_QUEST, pos)
            self.questBag.removeObj(page, pos)
        elif kind == const.RES_KIND_EQUIP:
            if self.equipment.isFill(pos):
                if hasattr(self, 'showEquipLabelCallback') and self.showEquipLabelCallback:
                    BigWorld.cancelCallback(self.showEquipLabelCallback)
                else:
                    self.oldRadarDataCache = commcalc.createSelfRadarChartData(BigWorld.player(), True)
                self.showEquipLabelCallback = BigWorld.callback(0.5, self.showEquipLabel)
            self.equipment.set(pos, None)
            page = const.RES_KIND_EQUIP
            if gameglobal.rds.ui.roleInfo.tabIdx == uiConst.ROLEINFO_TAB_FASHION:
                gameglobal.rds.ui.roleInfo.removeFashionItem(page, pos)
            else:
                gameglobal.rds.ui.actionbar.removeItem(uiConst.EQUIP_ACTION_BAR, pos)
            gameglobal.rds.ui.equipRepair.setEquipState()
            gameglobal.rds.ui.skill.refreshOtherSkillPanel()
            gameglobal.rds.ui.skill.refreshEmotePanel()
            gameglobal.rds.ui.roleInfo.onCheckEquipStarLvUp(pos)
            BigWorld.callback(0.2, gameglobal.rds.ui.roleInfo.refreshInfo)
        elif kind == const.RES_KIND_SUB_EQUIP_BAG:
            self.subEquipment.setQuickVal(None, page, pos)
            subPos = gametypes.subEquipToEquipPartMap.get(pos, -1)
            page = const.RES_KIND_SUB_EQUIP_BAG
            if subPos != -1:
                subPos += const.SUB_EQUIP_PART_OFFSET
                gameglobal.rds.ui.actionbar.removeItem(uiConst.EQUIP_ACTION_BAR, subPos)
            BigWorld.callback(0.2, gameglobal.rds.ui.roleInfo.refreshInfo)
        elif kind == const.RES_KIND_INV_BAR:
            self.bagBar.removeObj(page, pos)
            gameglobal.rds.ui.inventory.removeSackItem(const.BAG_BAR_BIND_ID, pos)
        elif kind == const.RES_KIND_FASHION_BAG:
            self.fashionBag.removeObj(page, pos)
            gameglobal.rds.ui.fashionBag.refresh()
        elif kind == const.RES_KIND_MATERIAL_BAG:
            self.materialBag.removeObj(page, pos)
            gameglobal.rds.ui.inventory.removeSackItem(const.MATERIAL_BAG_BIND_ID, pos)
            gameglobal.rds.ui.meterialBag.removeItem(page, pos)
        elif kind == const.RES_KIND_CART:
            self.cart.removeObj(page, pos)
            gameglobal.rds.ui.inventory.removeSackItem(const.CART_BIND_ID, pos)
        elif kind == const.RES_KIND_TEMP_BAG:
            self.tempBag.removeObj(page, pos)
            gameglobal.rds.ui.inventory.removeSackItem(const.TEMP_BAG_BIND_ID, pos)
            if self.tempBag.areEmpty(page):
                gameglobal.rds.ui.inventory.closeTempBag()
            gameglobal.rds.ui.inventory.updateTempBagNum()
        elif kind == const.RES_KIND_STORAGE:
            self.storage.removeObj(page, pos)
            gameglobal.rds.ui.storage.removeItem(page, pos)
        elif kind == const.RES_KIND_STORAGE_BAR:
            self.storageBar.removeObj(page, pos)
            gameglobal.rds.ui.storage.removeBarItem(pos)
        elif kind == const.RES_KIND_FASHION_BAG_BAR:
            self.fashionBagBar.removeObj(page, pos)
            gameglobal.rds.ui.fashionBag.removeBarItem(pos)
        elif kind == const.RES_KIND_MATERIAL_BAG_BAR:
            self.materialBagBar.removeObj(page, pos)
            gameglobal.rds.ui.meterialBag.removeBarItem(pos)
        elif kind == const.RES_KIND_SPRITE_MATERIAL_BAG_BAR:
            self.spriteMaterialBagBar.removeObj(page, pos)
            gameglobal.rds.ui.spriteMaterialBag.removeBarItem(pos)
        elif kind == const.RES_KIND_FISHING_QUIP:
            self.fishingEquip.set(pos, const.CONT_EMPTY_VAL)
            gameglobal.rds.ui.skill.refreshFishingSkillPanel()
            gameglobal.rds.ui.fishing.refreshFishingPanel()
            gameglobal.rds.ui.fishing.refreshBaitSlot()
        elif kind == const.RES_KIND_BOOTH:
            self.booth.removeObj(page, pos)
            gameglobal.rds.ui.booth.removeItem(page, pos)
        elif kind == const.RES_KIND_EXPLORE_EQUIP:
            self.exploreEquip.set(pos, const.CONT_EMPTY_VAL)
            if pos == gametypes.EXPLORE_EQUIP_SCROLL:
                gameglobal.rds.ui.explore.refreshExplorePanel()
            else:
                gameglobal.rds.ui.skill.refreshExploreSkill()
                gameglobal.rds.ui.explore.hide()
        elif kind == const.RES_KIND_LIFE_EQUIP:
            self.lifeEquipment.set(page, pos, const.CONT_EMPTY_VAL)
        elif kind == const.RES_KIND_MALL_BAG:
            self.mallBag.removeObj(page, pos)
            gameglobal.rds.ui.inventory.removeSackItem(const.MALL_BAR_BIND_ID, pos)
            if self.mallBag.areEmpty(page):
                gameglobal.rds.ui.inventory.onCloseInvTempBag()
            gameglobal.rds.ui.inventory.updateMallTempBagNum()
        elif kind == const.RES_KIND_ZAIJU_BAG:
            self.zaijuBag.removeObj(page, pos)
            gameglobal.rds.ui.guildBusinessBag.updateItem(None, page, pos)
        elif kind == const.RES_KIND_BATTLE_FIELD_BAG:
            self.battleFieldBag.pop(pos, None)
            gameglobal.rds.sound.playSound(5623)
            gameglobal.rds.ui.bfDotaItemAndProp.refreshItemSlots([pos])
        elif kind == const.RES_KIND_SPRITE_MATERIAL_BAG:
            self.spriteMaterialBag.removeObj(page, pos)
            gameglobal.rds.ui.spriteMaterialBag.removeItem(page, pos)
        elif kind == const.RES_KIND_SPRITE_MATERIAL_BAG_BAR:
            self.spriteMaterialBagBar.removeObj(page, pos)
            gameglobal.rds.ui.spriteMaterialBag.removeBarItem(pos)
        elif kind == const.RES_KIND_HIEROGRAM_BAG:
            self.hierogramBag.removeObj(page, pos)
        elif kind == const.RES_KIND_HIEROGRAM_BAG_BAR:
            self.hierogramBagBar.removeObj(page, pos)
        elif kind == const.RES_KIND_RIDE_WING_BAG:
            self.rideWingBag.removeObj(page, pos)
            if gameglobal.rds.ui.wingAndMount.mediator:
                gameglobal.rds.ui.wingAndMount.addItem(None, page, pos + 1)
        if kind == const.RES_KIND_EQUIP and (pos == gametypes.EQU_PART_WINGFLY or pos == gametypes.EQU_PART_RIDE):
            if gameglobal.rds.ui.wingAndMount.mediator:
                if pos == gametypes.EQU_PART_WINGFLY:
                    targetPos = 1
                else:
                    targetPos = 0
                gameglobal.rds.ui.wingAndMount.addItem(None, targetPos, 0)
        BigWorld.player().dispatchEvent(const.EVENT_ITEM_REMOVE, (kind,
         page,
         pos,
         getattr(item, 'id', None)))

    def setResState(self, kind, activated):
        pass

    def resWrap(self, kind, page, pos, amount):
        gamelog.debug(gameStrings.TEXT_IMPITEM_1080 % amount)
        it = None
        if kind == const.RES_KIND_INV:
            self.inv.shiftObj(page, pos, amount)
            it = self.inv.getQuickVal(page, pos)
            gameglobal.rds.ui.inventory.addItem(it, page, pos)
            gameglobal.rds.ui.actionbar.refreshByBagUse(it)
            if gameglobal.rds.ui.compositeShop.isOpen:
                gameglobal.rds.ui.compositeShop.refreshBuyItemDisplayData()
            if gameglobal.rds.ui.skill.daoHangDirMediator:
                gameglobal.rds.ui.skill.refreshHaoHangDirectionPanel()
            if gameglobal.rds.ui.skill.enhanceMediator:
                if gameglobal.rds.ui.skill.enhanceType == uiConst.TYPE_XIUWEI_BAR:
                    gameglobal.rds.ui.skill.refreshXiuWeiBarInfo()
                elif gameglobal.rds.ui.skill.enhanceType == uiConst.TYPE_WUSHUANG_BAR:
                    gameglobal.rds.ui.skill.refreshWuShuangBarInfo()
                elif gameglobal.rds.ui.skill.enhanceType == uiConst.TYPE_RELIEVE:
                    gameglobal.rds.ui.skill.refreshRelieveInfo()
            if gameglobal.rds.ui.consign.mediator:
                page = gameglobal.rds.ui.consign.pageSrc
                pos = gameglobal.rds.ui.consign.posSrc
                gameglobal.rds.ui.inventory.updateSlotState(page, pos)
            if gameglobal.rds.ui.equipEnhance.mediator:
                gameglobal.rds.ui.equipEnhance.refreshContent()
            if gameglobal.rds.ui.equipMix.mediator:
                gameglobal.rds.ui.equipMix.refresh()
            gameglobal.rds.ui.skill.refreshDetailInfo()
            gameglobal.rds.ui.equipSoulStar.refreshInfo()
            gameglobal.rds.ui.itemSelect.refreshItemList()
            gameglobal.rds.ui.purchaseShop.refreshItems()
        elif kind == const.RES_KIND_CROSS_INV:
            it = self.crossInv.getQuickVal(page, pos)
            self.crossInv.shiftObj(page, pos, amount)
            gameglobal.rds.ui.crossServerBag.updateItem(it, page, pos)
            gameglobal.rds.ui.actionbar.refreshByBagUse(it)
        elif kind == const.RES_KIND_QUEST_BAG:
            self.questBag.shiftObj(page, pos, amount)
            it = self.questBag.getQuickVal(page, pos)
            gameglobal.rds.ui.inventory.addItem(it, uiConst.BAG_PAGE_QUEST, pos)
        elif kind == const.RES_KIND_INV_BAR:
            self.bagBar.shiftObj(page, pos, amount)
            it = self.bagBar.getQuickVal(0, pos)
            gameglobal.rds.ui.inventory.addSackItem(it, const.BAG_BAR_BIND_ID, pos)
        elif kind == const.RES_KIND_FASHION_BAG:
            self.fashionBag.shiftObj(page, pos, amount)
            it = self.fashionBag.getQuickVal(0, pos)
            gameglobal.rds.ui.fashionBag.refresh()
            gameglobal.rds.ui.inventory.addSackItem(it, const.FASHION_BAG_BIND_ID, pos)
        elif kind == const.RES_KIND_MATERIAL_BAG:
            self.materialBag.shiftObj(page, pos, amount)
            it = self.materialBag.getQuickVal(page, pos)
            gameglobal.rds.ui.inventory.addSackItem(it, const.MATERIAL_BAG_BIND_ID, pos)
            gameglobal.rds.ui.meterialBag.addItem(it, page, pos)
        elif kind == const.RES_KIND_CART:
            self.cart.shiftObj(page, pos, amount)
            it = self.cart.getQuickVal(0, pos)
            gameglobal.rds.ui.inventory.addSackItem(it, const.CART_BIND_ID, pos)
        elif kind == const.RES_KIND_TEMP_BAG:
            self.tempBag.shiftObj(page, pos, amount)
            it = self.tempBag.getQuickVal(0, pos)
            gameglobal.rds.ui.inventory.addSackItem(it, const.TEMP_BAG_BIND_ID, pos)
        elif kind == const.RES_KIND_STORAGE:
            self.storage.shiftObj(page, pos, amount)
            it = self.storage.getQuickVal(page, pos)
            gameglobal.rds.ui.storage.addItem(it, page, pos)
        elif kind == const.RES_KIND_STORAGE_BAR:
            self.storageBar.shiftObj(page, pos, amount)
            it = self.storageBar.getQuickVal(0, pos)
            gameglobal.rds.ui.storage.addBarItem(it, pos)
        elif kind == const.RES_KIND_FASHION_BAG_BAR:
            self.fashionBagBar.shiftObj(page, pos, amount)
            it = self.fashionBagBar.getQuickVal(0, pos)
            gameglobal.rds.ui.fashionBag.addBarItem(it, pos)
        elif kind == const.RES_KIND_MATERIAL_BAG_BAR:
            self.materialBagBar.shiftObj(page, pos, amount)
            it = self.materialBagBar.getQuickVal(0, pos)
            gameglobal.rds.ui.meterialBag.addBarItem(it, pos)
        elif kind == const.RES_KIND_BOOTH:
            self.booth.shiftObj(page, pos, amount)
            it = self.booth.getQuickVal(page, pos)
            it.cwrap = amount
            gameglobal.rds.ui.booth.addItem(it, page, pos)
        elif kind == const.RES_KIND_MALL_BAG:
            self.mallBag.shiftObj(page, pos, amount)
            it = self.mallBag.getQuickVal(0, pos)
            gameglobal.rds.ui.inventory.addSackItem(it, const.MALL_BAR_BIND_ID, pos)
            gameglobal.rds.ui.inventory.updateMallTempBagNum()
        elif kind == const.RES_KIND_BATTLE_FIELD_BAG:
            if self.battleFieldBag[pos].cwrap < amount:
                gameglobal.rds.sound.playSound(5622)
                gameglobal.rds.ui.bfDotaShop.refreshByBuyItemSucc(self.battleFieldBag[pos].id)
                self.onBuyItem(self.battleFieldBag[pos].id)
            else:
                gameglobal.rds.sound.playSound(5623)
            self.battleFieldBag[pos].cwrap = amount
            gameglobal.rds.ui.bfDotaItemAndProp.refreshItemSlots([pos])
        elif kind == const.RES_KIND_SPRITE_MATERIAL_BAG:
            self.spriteMaterialBag.shiftObj(page, pos, amount)
            it = self.spriteMaterialBag.getQuickVal(page, pos)
            gameglobal.rds.ui.spriteMaterialBag.addItem(it, page, pos)
        elif kind == const.RES_KIND_HIEROGRAM_BAG:
            self.hierogramBag.shiftObj(page, pos, amount)
            it = self.hierogramBag.getQuickVal(page, pos)
        elif kind == const.RES_KIND_HIEROGRAM_BAG_BAR:
            self.hierogramBagBar.shiftObj(page, pos, amount)
        if it:
            BigWorld.player().dispatchEvent(const.EVENT_ITEM_CHANGE, (kind,
             page,
             pos,
             it))

    def resWrapPart(self, srcKind, srcPage, srcPos, srcMany, dstKind, dstPage, dstPos):
        if srcKind == const.RES_KIND_BOOTH and dstKind == const.RES_KIND_INV:
            self.booth.wrapObj(srcPage, srcPos, -srcMany)
            invItem = self.inv.getQuickVal(dstPage, dstPos)
            self.resWrap(dstKind, dstPage, dstPos, invItem.cwrap + srcMany)

    def resWrapWhole(self, srcKind, srcPage, srcPos, dstKind, dstPage, dstPos):
        if srcKind == const.RES_KIND_BOOTH and dstKind == const.RES_KIND_INV:
            boothItem = self.booth.getQuickVal(srcPage, srcPos)
            invItem = self.inv.getQuickVal(dstPage, dstPos)
            self.resWrap(dstKind, dstPage, dstPos, invItem.cwrap + boothItem.cwrap)
            self.booth.removeObj(srcPage, srcPos)
            gameglobal.rds.ui.booth.removeItem(srcPage, srcPos)

    def resMove(self, srcKind, srcPage, srcPos, dstKind, dstPage, dstPos):
        if srcKind == const.RES_KIND_INV and srcKind == dstKind:
            gamelog.debug(gameStrings.TEXT_IMPITEM_1230, srcPage, srcPos, dstPage, dstPos)
            self.inv.moveObj(srcPage, srcPos, dstPage, dstPos)
            it = self.inv.getQuickVal(dstPage, dstPos)
            gameglobal.rds.ui.inventory.addItem(it, dstPage, dstPos)
            gameglobal.rds.ui.inventory.removeItem(srcPage, srcPos)
        elif srcKind == const.RES_KIND_CROSS_INV and srcKind == dstKind:
            self.crossInv.moveObj(srcPage, srcPos, dstPage, dstPos)
            it = self.crossInv.getQuickVal(dstPage, dstPos)
            gameglobal.rds.ui.crossServerBag.addItem(it, dstPage, dstPos)
            gameglobal.rds.ui.crossServerBag.removeItem(srcPage, srcPos)
        elif srcKind == const.RES_KIND_QUEST_BAG and srcKind == dstKind:
            self.questBag.moveObj(srcPage, srcPos, dstPage, dstPos)
            it = self.questBag.getQuickVal(dstPage, dstPos)
            gameglobal.rds.ui.inventory.addItem(it, uiConst.BAG_PAGE_QUEST, dstPos)
            gameglobal.rds.ui.inventory.removeItem(uiConst.BAG_PAGE_QUEST, srcPos)
        elif srcKind == const.RES_KIND_INV_BAR and srcKind == dstKind:
            self.bagBar.moveObj(srcPage, srcPos, dstPage, dstPos)
            it = self.bagBar.getQuickVal(dstPage, dstPos)
            gameglobal.rds.ui.inventory.addSackItem(it, const.BAG_BAR_BIND_ID, dstPos)
            gameglobal.rds.ui.inventory.removeSackItem(const.BAG_BAR_BIND_ID, srcPos)
        elif srcKind == const.RES_KIND_FASHION_BAG and srcKind == dstKind:
            self.fashionBag.moveObj(srcPage, srcPos, dstPage, dstPos)
            it = self.fashionBag.getQuickVal(dstPage, dstPos)
            gameglobal.rds.ui.inventory.addSackItem(it, const.FASHION_BAG_BIND_ID, dstPos)
            gameglobal.rds.ui.inventory.removeSackItem(const.FASHION_BAG_BIND_ID, srcPos)
            gameglobal.rds.ui.fashionBag.refresh()
        elif srcKind == const.RES_KIND_MATERIAL_BAG and srcKind == dstKind:
            self.materialBag.moveObj(srcPage, srcPos, dstPage, dstPos)
            it = self.materialBag.getQuickVal(dstPage, dstPos)
            gameglobal.rds.ui.inventory.addSackItem(it, const.MATERIAL_BAG_BIND_ID, dstPos)
            gameglobal.rds.ui.inventory.removeSackItem(const.MATERIAL_BAG_BIND_ID, srcPos)
            gameglobal.rds.ui.meterialBag.addItem(it, dstPage, dstPos)
            gameglobal.rds.ui.meterialBag.removeItem(srcPage, srcPos)
        elif srcKind == const.RES_KIND_CART and srcKind == dstKind:
            self.cart.moveObj(srcPage, srcPos, dstPage, dstPos)
            it = self.cart.getQuickVal(dstPage, dstPos)
            gameglobal.rds.ui.inventory.addSackItem(it, const.CART_BIND_ID, dstPos)
            gameglobal.rds.ui.inventory.removeSackItem(const.CART_BIND_ID, srcPos)
        elif srcKind == const.RES_KIND_TEMP_BAG and srcKind == dstKind:
            self.tempBag.moveObj(srcPage, srcPos, dstPage, dstPos)
            it = self.tempBag.getQuickVal(dstPage, dstPos)
            gameglobal.rds.ui.inventory.addSackItem(it, const.TEMP_BAG_BIND_ID, dstPos)
            gameglobal.rds.ui.inventory.removeSackItem(const.TEMP_BAG_BIND_ID, srcPos)
        elif srcKind == const.RES_KIND_STORAGE and srcKind == dstKind:
            self.storage.moveObj(srcPage, srcPos, dstPage, dstPos)
            it = self.storage.getQuickVal(dstPage, dstPos)
            gameglobal.rds.ui.storage.addItem(it, dstPage, dstPos)
            gameglobal.rds.ui.storage.removeItem(srcPage, srcPos)
        elif srcKind == const.RES_KIND_STORAGE_BAR and srcKind == dstKind:
            self.storageBar.moveObj(srcPage, srcPos, dstPage, dstPos)
            it = self.storageBar.getQuickVal(dstPage, dstPos)
            gameglobal.rds.ui.storage.addBarItem(it, dstPos)
            gameglobal.rds.ui.storage.removeBarItem(srcPos)
        elif srcKind == const.RES_KIND_FASHION_BAG_BAR and srcKind == dstKind:
            self.fashionBagBar.moveObj(srcPage, srcPos, dstPage, dstPos)
            it = self.fashionBagBar.getQuickVal(dstPage, dstPos)
            gameglobal.rds.ui.fashionBag.addBarItem(it, dstPos)
            gameglobal.rds.ui.fashionBag.removeBarItem(srcPos)
        elif srcKind == const.RES_KIND_MATERIAL_BAG_BAR and srcKind == dstKind:
            self.materialBagBar.moveObj(srcPage, srcPos, dstPage, dstPos)
            it = self.materialBagBar.getQuickVal(dstPage, dstPos)
            gameglobal.rds.ui.meterialBag.addBarItem(it, dstPos)
            gameglobal.rds.ui.meterialBag.removeBarItem(srcPos)
        elif srcKind == const.RES_KIND_INV and dstKind == const.RES_KIND_EQUIP:
            it = self.inv.getQuickVal(srcPage, srcPos)
            self.inv.removeObj(srcPage, srcPos)
            self.equipment.set(dstPos, it)
            dstPage = 2
            gameglobal.rds.ui.actionbar.setItem(it, dstPage, dstPos, sType=uiConst.SHORTCUT_TYPE_ITEM_EQUIP)
            gameglobal.rds.ui.inventory.removeItem(srcPage, srcPos)
        elif srcKind == const.RES_KIND_EQUIP and dstKind == const.RES_KIND_INV:
            it = self.equipment.get(srcPos)
            self.equipment.set(srcPos, None)
            self.inv.insertObj(it, dstPage, dstPos)
            srcPage = 2
            gameglobal.rds.ui.inventory.addItem(it, dstPage, dstPos)
            gameglobal.rds.ui.actionbar.removeItem(srcPage, srcPos)
        elif srcKind == const.RES_KIND_BOOTH and dstKind == const.RES_KIND_INV:
            it = self.booth.getQuickVal(srcPage, srcPos)
            self.booth.removeObj(srcPage, srcPos)
            self.resInsert(dstKind, it, dstPage, dstPos)
            gameglobal.rds.ui.booth.removeItem(srcPage, srcPos)
        elif srcKind == const.RES_KIND_INV and dstKind == const.RES_KIND_BOOTH:
            it = self.inv.getQuickVal(srcPage, srcPos)
            self.resRemove(srcKind, srcPage, srcPos)
            self.booth.insertObj(it, dstPage, dstPos)
            gameglobal.rds.ui.booth.addItem(it, dstPage, dstPos)
        elif srcKind == const.RES_KIND_BOOTH and srcKind == dstKind:
            it = self.booth.getQuickVal(srcPage, srcPos)
            self.booth.moveObj(srcPage, srcPos, dstPage, dstPos)
            gameglobal.rds.ui.booth.removeItem(srcPage, srcPos)
            gameglobal.rds.ui.booth.addItem(it, dstPage, dstPos)
        elif srcKind == const.RES_KIND_INV and dstKind == const.RES_KIND_RIDE_WING_BAG:
            it = self.inv.getQuickVal(srcPage, srcPos)
            self.resRemove(srcKind, srcPage, srcPos)
            self.rideWingBag.insertObj(it, dstPage, dstPos)
            gameglobal.rds.ui.wingAndMount.addItem(it, dstPage, dstPos + 1)
        elif srcKind == const.RES_KIND_RIDE_WING_BAG and dstKind == const.RES_KIND_INV:
            it = self.rideWingBag.getQuickVal(srcPage, srcPos)
            self.inv.insertObj(it, dstPage, dstPos)
            self.resRemove(srcKind, srcPage, srcPos)
            gameglobal.rds.ui.inventory.addItem(it, dstPage, dstPos)
        elif srcKind == const.RES_KIND_RIDE_WING_BAG and dstKind == const.RES_KIND_RIDE_WING_BAG:
            self.rideWingBag.moveObj(srcPage, srcPos, dstPage, dstPos)
            srcIt = self.rideWingBag.getQuickVal(srcPage, srcPos)
            dscIt = self.rideWingBag.getQuickVal(dstPage, dstPos)
            gameglobal.rds.ui.wingAndMount.addItem(dscIt, srcPage, srcPos + 1)
            gameglobal.rds.ui.wingAndMount.addItem(srcIt, dstPage, dstPos + 1)
        elif srcKind == const.RES_KIND_BATTLE_FIELD_BAG and dstKind == const.RES_KIND_BATTLE_FIELD_BAG:
            srcIt = self.battleFieldBag.pop(srcPos, None)
            self.battleFieldBag[dstPos] = srcIt
            gameglobal.rds.ui.bfDotaItemAndProp.refreshItemSlots([srcPos, dstPos])
        elif srcKind == const.RES_KIND_SPRITE_MATERIAL_BAG and srcKind == dstKind:
            self.spriteMaterialBag.moveObj(srcPage, srcPos, dstPage, dstPos)
            srcIt = self.rideWingBag.getQuickVal(srcPage, srcPos)
            gameglobal.rds.ui.spriteMaterialBag.removeItem(srcPage, srcPos)
            gameglobal.rds.ui.spriteMaterialBag.addItem(srcIt, dstPage, dstPos)
        elif srcKind == const.RES_KIND_HIEROGRAM_BAG and srcKind == dstKind:
            self.hierogramBag.moveObj(srcPage, srcPos, dstPage, dstKind)
        elif srcKind == const.RES_KIND_HIEROGRAM_BAG and dstKind == const.RES_KIND_INV:
            it = self.hierogramBag.getQuickVal(srcPage, srcPos)
            self.hierogramBag.removeObj(srcPage, srcPos)
            self.resInsert(dstKind, it, dstPage, dstPos)
        elif srcKind == const.RES_KIND_INV and dstKind == const.RES_KIND_HIEROGRAM_BAG:
            it = self.inv.getQuickVal(srcPage, srcPos)
            self.inv.removeObj(srcPage, srcPos)
            self.resInsert(dstKind, it, dstPage, dstPos)
        if dstKind == const.RES_KIND_EQUIP and (dstPos == gametypes.EQU_PART_WINGFLY or dstPos == gametypes.EQU_PART_RIDE):
            if gameglobal.rds.ui.wingAndMount.mediator:
                if dstPos == gametypes.EQU_PART_WINGFLY:
                    targetPos = 1
                else:
                    targetPos = 0
                it = self.equipment[dstPos]
                gameglobal.rds.ui.wingAndMount.addItem(it, targetPos, 0)
        if srcKind == const.RES_KIND_EQUIP and (srcPos == gametypes.EQU_PART_WINGFLY or srcPos == gametypes.EQU_PART_RIDE):
            if gameglobal.rds.ui.wingAndMount.mediator:
                if srcPos == gametypes.EQU_PART_WINGFLY:
                    targetPos = 1
                else:
                    targetPos = 0
                it = self.equipment[srcPos]
                gameglobal.rds.ui.wingAndMount.addItem(it, targetPos, 0)
        BigWorld.player().dispatchEvent(const.EVENT_ITEM_MOVE, (srcKind,
         srcPage,
         srcPos,
         dstKind,
         dstPage,
         dstPos))

    def resMovePart(self, srcKind, srcPage, srcPos, srcMany, dstKind, dstPage, dstPos):
        if srcKind == const.RES_KIND_INV and dstKind == const.RES_KIND_BOOTH:
            invItem = self.inv.getQuickVal(srcPage, srcPos)
            boothItem = invItem.deepcopy()
            boothItem.cwrap = srcMany
            invItem = self.inv.getQuickVal(srcPage, srcPos)
            self.resWrap(srcKind, srcPage, srcPos, invItem.cwrap - srcMany)
            self.booth.insertObj(boothItem, dstPage, dstPos)
            gameglobal.rds.ui.booth.addItem(boothItem, dstPage, dstPos)
        elif srcKind == const.RES_KIND_BOOTH and dstKind == const.RES_KIND_INV:
            boothItem = self.booth.getQuickVal(srcPage, srcPos)
            invItem = boothItem.deepcopy()
            invItem.cwrap = srcMany
            self.booth.wrapObj(srcPage, srcPos, -srcMany)
            self.resInsert(dstKind, invItem, dstPage, dstPos)
            gameglobal.rds.ui.booth.addItem(boothItem, srcPage, srcPos)

    def resExchange(self, srcKind, srcPage, srcPos, dstKind, dstPage, dstPos):
        if srcKind == const.RES_KIND_INV and srcKind == dstKind:
            gamelog.debug(gameStrings.TEXT_IMPITEM_1230, srcPage, srcPos, dstPage, dstPos)
            self.inv.exchangeObj(srcPage, srcPos, dstPage, dstPos)
            srcIt = self.inv.getQuickVal(dstPage, dstPos)
            dstIt = self.inv.getQuickVal(srcPage, srcPos)
            gameglobal.rds.ui.inventory.removeItem(dstPage, dstPos)
            gameglobal.rds.ui.inventory.removeItem(srcPage, srcPos)
            gameglobal.rds.ui.inventory.addItem(srcIt, dstPage, dstPos)
            gameglobal.rds.ui.inventory.addItem(dstIt, srcPage, srcPos)
        if srcKind == const.RES_KIND_CROSS_INV and srcKind == dstKind:
            gamelog.debug(gameStrings.TEXT_IMPITEM_1230, srcPage, srcPos, dstPage, dstPos)
            self.crossInv.exchangeObj(srcPage, srcPos, dstPage, dstPos)
            srcIt = self.crossInv.getQuickVal(dstPage, dstPos)
            dstIt = self.crossInv.getQuickVal(srcPage, srcPos)
            gameglobal.rds.ui.crossServerBag.removeItem(dstPage, dstPos)
            gameglobal.rds.ui.crossServerBag.removeItem(srcPage, srcPos)
            gameglobal.rds.ui.crossServerBag.addItem(srcIt, dstPage, dstPos)
            gameglobal.rds.ui.crossServerBag.addItem(dstIt, srcPage, srcPos)
        elif srcKind == const.RES_KIND_QUEST_BAG and srcKind == dstKind:
            self.questBag.exchangeObj(srcPage, srcPos, dstPage, dstPos)
            srcIt = self.questBag.getQuickVal(dstPage, dstPos)
            dstIt = self.questBag.getQuickVal(srcPage, srcPos)
            gameglobal.rds.ui.inventory.removeItem(uiConst.BAG_PAGE_QUEST, dstPos)
            gameglobal.rds.ui.inventory.removeItem(uiConst.BAG_PAGE_QUEST, srcPos)
            gameglobal.rds.ui.inventory.addItem(srcIt, uiConst.BAG_PAGE_QUEST, dstPos)
            gameglobal.rds.ui.inventory.addItem(dstIt, uiConst.BAG_PAGE_QUEST, srcPos)
        elif srcKind == const.RES_KIND_INV_BAR and srcKind == dstKind:
            self.bagBar.exchangeObj(srcPage, srcPos, dstPage, dstPos)
            srcIt = self.bagBar.getQuickVal(dstPage, dstPos)
            dstIt = self.bagBar.getQuickVal(srcPage, srcPos)
            gameglobal.rds.ui.inventory.removeSackItem(const.BAG_BAR_BIND_ID, dstPos)
            gameglobal.rds.ui.inventory.removeSackItem(const.BAG_BAR_BIND_ID, srcPos)
            gameglobal.rds.ui.inventory.addSackItem(srcIt, const.BAG_BAR_BIND_ID, dstPos)
            gameglobal.rds.ui.inventory.addSackItem(dstIt, const.BAG_BAR_BIND_ID, srcPos)
        elif srcKind == const.RES_KIND_FASHION_BAG and srcKind == dstKind:
            self.fashionBag.exchangeObj(srcPage, srcPos, dstPage, dstPos)
            srcIt = self.fashionBag.getQuickVal(dstPage, dstPos)
            dstIt = self.fashionBag.getQuickVal(srcPage, srcPos)
            gameglobal.rds.ui.inventory.removeSackItem(const.FASHION_BAG_BIND_ID, dstPos)
            gameglobal.rds.ui.inventory.removeSackItem(const.FASHION_BAG_BIND_ID, srcPos)
            gameglobal.rds.ui.inventory.addSackItem(srcIt, const.FASHION_BAG_BIND_ID, dstPos)
            gameglobal.rds.ui.inventory.addSackItem(dstIt, const.FASHION_BAG_BIND_ID, srcPos)
            gameglobal.rds.ui.fashionBag.refresh()
        elif srcKind == const.RES_KIND_MATERIAL_BAG and srcKind == dstKind:
            self.materialBag.exchangeObj(srcPage, srcPos, dstPage, dstPos)
            srcIt = self.materialBag.getQuickVal(dstPage, dstPos)
            dstIt = self.materialBag.getQuickVal(srcPage, srcPos)
            gameglobal.rds.ui.inventory.removeSackItem(const.MATERIAL_BAG_BIND_ID, dstPos)
            gameglobal.rds.ui.inventory.removeSackItem(const.MATERIAL_BAG_BIND_ID, srcPos)
            gameglobal.rds.ui.inventory.addSackItem(srcIt, const.MATERIAL_BAG_BIND_ID, dstPos)
            gameglobal.rds.ui.inventory.addSackItem(dstIt, const.MATERIAL_BAG_BIND_ID, srcPos)
            gameglobal.rds.ui.meterialBag.removeItem(dstPage, dstPos)
            gameglobal.rds.ui.meterialBag.removeItem(srcPage, srcPos)
            gameglobal.rds.ui.meterialBag.addItem(srcIt, dstPage, dstPos)
            gameglobal.rds.ui.meterialBag.addItem(dstIt, srcPage, srcPos)
        elif srcKind == const.RES_KIND_SPRITE_MATERIAL_BAG and srcKind == dstKind:
            self.spriteMaterialBag.exchangeObj(srcPage, srcPos, dstPage, dstPos)
            srcIt = self.spriteMaterialBag.getQuickVal(dstPage, dstPos)
            dstIt = self.spriteMaterialBag.getQuickVal(srcPage, srcPos)
            gameglobal.rds.ui.spriteMaterialBag.removeItem(dstPage, dstPos)
            gameglobal.rds.ui.spriteMaterialBag.removeItem(srcPage, srcPos)
            gameglobal.rds.ui.spriteMaterialBag.addItem(srcIt, dstPage, dstPos)
            gameglobal.rds.ui.spriteMaterialBag.addItem(dstIt, srcPage, srcPos)
        elif srcKind == const.RES_KIND_CART and srcKind == dstKind:
            self.cart.exchangeObj(srcPage, srcPos, dstPage, dstPos)
            srcIt = self.cart.getQuickVal(dstPage, dstPos)
            dstIt = self.cart.getQuickVal(srcPage, srcPos)
            gameglobal.rds.ui.inventory.removeSackItem(const.CART_BIND_ID, dstPos)
            gameglobal.rds.ui.inventory.removeSackItem(const.CART_BIND_ID, srcPos)
            gameglobal.rds.ui.inventory.addSackItem(srcIt, const.CART_BIND_ID, dstPos)
            gameglobal.rds.ui.inventory.addSackItem(dstIt, const.CART_BIND_ID, srcPos)
        elif srcKind == const.RES_KIND_TEMP_BAG and srcKind == dstKind:
            self.tempBag.exchangeObj(srcPage, srcPos, dstPage, dstPos)
            srcIt = self.tempBag.getQuickVal(dstPage, dstPos)
            dstIt = self.tempBag.getQuickVal(srcPage, srcPos)
            gameglobal.rds.ui.inventory.removeSackItem(const.TEMP_BAG_BIND_ID, dstPos)
            gameglobal.rds.ui.inventory.removeSackItem(const.TEMP_BAG_BIND_ID, srcPos)
            gameglobal.rds.ui.inventory.addSackItem(srcIt, const.TEMP_BAG_BIND_ID, dstPos)
            gameglobal.rds.ui.inventory.addSackItem(dstIt, const.TEMP_BAG_BIND_ID, srcPos)
        elif srcKind == const.RES_KIND_STORAGE and srcKind == dstKind:
            self.storage.exchangeObj(srcPage, srcPos, dstPage, dstPos)
            srcIt = self.storage.getQuickVal(dstPage, dstPos)
            dstIt = self.storage.getQuickVal(srcPage, srcPos)
            gameglobal.rds.ui.storage.removeItem(dstPage, dstPos)
            gameglobal.rds.ui.storage.removeItem(srcPage, srcPos)
            gameglobal.rds.ui.storage.addItem(srcIt, dstPage, dstPos)
            gameglobal.rds.ui.storage.addItem(dstIt, srcPage, srcPos)
        elif srcKind == const.RES_KIND_STORAGE_BAR and srcKind == dstKind:
            self.storageBar.exchangeObj(srcPage, srcPos, dstPage, dstPos)
            srcIt = self.storageBar.getQuickVal(dstPage, dstPos)
            dstIt = self.storageBar.getQuickVal(srcPage, srcPos)
            gameglobal.rds.ui.storage.removeBarItem(dstPos)
            gameglobal.rds.ui.storage.removeBarItem(srcPos)
            gameglobal.rds.ui.storage.addBarItem(srcIt, dstPos)
            gameglobal.rds.ui.storage.addBarItem(dstIt, srcPos)
        elif srcKind == const.RES_KIND_FASHION_BAG_BAR and srcKind == dstKind:
            self.fashionBagBar.exchangeObj(srcPage, srcPos, dstPage, dstPos)
            srcIt = self.fashionBagBar.getQuickVal(dstPage, dstPos)
            dstIt = self.fashionBagBar.getQuickVal(srcPage, srcPos)
            gameglobal.rds.ui.fashionBag.removeBarItem(dstPos)
            gameglobal.rds.ui.fashionBag.removeBarItem(srcPos)
            gameglobal.rds.ui.fashionBag.addBarItem(srcIt, dstPos)
            gameglobal.rds.ui.fashionBag.addBarItem(dstIt, srcPos)
        elif srcKind == const.RES_KIND_MATERIAL_BAG_BAR and srcKind == dstKind:
            self.materialBagBar.exchangeObj(srcPage, srcPos, dstPage, dstPos)
            srcIt = self.materialBagBar.getQuickVal(dstPage, dstPos)
            dstIt = self.materialBagBar.getQuickVal(srcPage, srcPos)
            gameglobal.rds.ui.meterialBag.removeBarItem(dstPos)
            gameglobal.rds.ui.meterialBag.removeBarItem(srcPos)
            gameglobal.rds.ui.meterialBag.addBarItem(srcIt, dstPos)
            gameglobal.rds.ui.meterialBag.addBarItem(dstIt, srcPos)
        elif srcKind == const.RES_KIND_SPRITE_MATERIAL_BAG_BAR and srcKind == dstKind:
            self.spriteMaterialBagBar.exchangeObj(srcPage, srcPos, dstPage, dstPos)
            srcIt = self.spriteMaterialBagBar.getQuickVal(dstPage, dstPos)
            dstIt = self.spriteMaterialBagBar.getQuickVal(srcPage, srcPos)
            gameglobal.rds.ui.spriteMaterialBag.removeBarItem(dstPos)
            gameglobal.rds.ui.spriteMaterialBag.removeBarItem(srcPos)
            gameglobal.rds.ui.spriteMaterialBag.addBarItem(srcIt, dstPos)
            gameglobal.rds.ui.spriteMaterialBag.addBarItem(dstIt, srcPos)
        elif srcKind == const.RES_KIND_INV and dstKind == const.RES_KIND_EQUIP:
            dstIt = self.equipment.get(dstPos)
            srcIt = self.inv.getQuickVal(srcPage, srcPos)
            self.equipment.set(dstPos, srcIt)
            self.inv.insertObj(dstIt, srcPage, srcPos)
            srcPage = 2
            gameglobal.rds.ui.actionbar.setItem(srcIt, dstPage, dstPos, sType=uiConst.SHORTCUT_TYPE_ITEM_EQUIP)
            gameglobal.rds.ui.inventory.addItem(dstIt, srcPage, srcPos, sType=uiConst.SHORTCUT_TYPE_ITEM_EQUIP)
        elif srcKind == const.RES_KIND_EQUIP and dstKind == const.RES_KIND_INV:
            srcIt = self.equipment.get(srcPos)
            dstIt = self.inv.getQuickVal(dstPage, dstPos)
            self.equipment.set(srcPos, dstIt)
            self.inv.insertObj(srcIt, dstPage, dstPos)
            srcPage = 2
            gameglobal.rds.ui.actionbar.setItem(dstIt, srcPage, srcPos, sType=uiConst.SHORTCUT_TYPE_ITEM_EQUIP)
            gameglobal.rds.ui.inventory.addItem(srcIt, dstPage, dstPos, sType=uiConst.SHORTCUT_TYPE_ITEM_EQUIP)
        elif srcKind == const.RES_KIND_INV and dstKind == const.RES_KIND_RIDE_WING_BAG:
            srcIt = self.inv.getQuickVal(srcPage, srcPos)
            dstIt = self.rideWingBag.getQuickVal(dstPage, dstPos)
            self.rideWingBag.insertObj(srcIt, dstPage, dstPos)
            self.inv.insertObj(dstIt, srcPos, srcPos)
            gameglobal.rds.ui.inventory.addItem(dstIt, srcPos, srcPos)
            gameglobal.rds.ui.wingAndMount.addItem(srcIt, dstPage, dstPos + 1)
        elif srcKind == const.RES_KIND_RIDE_WING_BAG and dstKind == const.RES_KIND_INV:
            dstIt = self.inv.getQuickVal(dstPage, dstPos)
            srcIt = self.rideWingBag.getQuickVal(srcPage, srcPos)
            self.rideWingBag.insertObj(dstIt, srcPage, srcPos)
            self.inv.insertObj(srcIt, dstPage, dstPos)
            gameglobal.rds.ui.inventory.addItem(srcIt, dstPage, dstPos + 1)
            gameglobal.rds.ui.wingAndMount.addItem(dstIt, srcPage, srcPos + 1)
        elif srcKind == const.RES_KIND_RIDE_WING_BAG and dstKind == const.RES_KIND_RIDE_WING_BAG:
            self.rideWingBag.exchangeObj(srcPage, srcPos, dstPage, dstPos)
            srcIt = self.rideWingBag.getQuickVal(srcPage, srcPos)
            dscIt = self.rideWingBag.getQuickVal(dstPage, dstPos)
            gameglobal.rds.ui.wingAndMount.addItem(dscIt, srcPage, srcPos + 1)
            gameglobal.rds.ui.wingAndMount.addItem(srcIt, dstPage, dstPos + 1)
        elif srcKind == const.RES_KIND_INV and dstKind == const.RES_KIND_CROSS_INV:
            self.crossInv.insertObj(srcIt, dstPage, dstPos)
            self.inv.insertObj(dstIt, srcPos, srcPos)
            gameglobal.rds.ui.crossServerBag.updateItem(srcIt, 0, dstPos)
            gameglobal.rds.ui.inventory.addItem(dstIt, srcPos, srcPos)
        elif srcKind == const.RES_KIND_CROSS_INV and dstKind == const.RES_KIND_INV:
            self.inv.insertObj(srcIt, dstPage, dstPos)
            self.crossInv.insertObj(dstIt, srcPos, srcPos)
            gameglobal.rds.ui.crossServerBag.updateItem(dstIt, 0, srcPos)
            gameglobal.rds.ui.inventory.addItem(srcIt, dstPage, dstPos)
        elif srcKind == const.RES_KIND_BATTLE_FIELD_BAG and dstKind == const.RES_KIND_BATTLE_FIELD_BAG:
            srcIt = self.battleFieldBag.pop(srcPos, None)
            dstIt = self.battleFieldBag.pop(dstPos, None)
            self.battleFieldBag[srcPos] = dstIt
            self.battleFieldBag[dstPos] = srcIt
            gameglobal.rds.ui.bfDotaItemAndProp.refreshItemSlots([srcPos, dstPos])
        elif srcKind == const.RES_KIND_HIEROGRAM_BAG and dstKind == const.RES_KIND_HIEROGRAM_BAG:
            srcIt = self.hierogramBag.getQuickVal(srcPage, srcPos)
            dstIt = self.hierogramBag.getQuickVal(dstPage, dstPos)
            self.hierogramBag.removeObj(srcPage, srcPos)
            self.hierogramBag.removeObj(dstPage, dstPos)
            self.hierogramBag.insertObj(dstIt, srcPage, srcPos)
            self.hierogramBag.insertObj(srcIt, dstPage, dstPos)
        if dstKind == const.RES_KIND_EQUIP and (dstPos == gametypes.EQU_PART_WINGFLY or dstPos == gametypes.EQU_PART_RIDE):
            if gameglobal.rds.ui.wingAndMount.mediator:
                if dstPos == gametypes.EQU_PART_WINGFLY:
                    targetPos = 1
                else:
                    targetPos = 0
                it = self.equipment[dstPos]
                gameglobal.rds.ui.wingAndMount.addItem(it, targetPos, 0)
        if srcKind == const.RES_KIND_EQUIP and (srcPos == gametypes.EQU_PART_WINGFLY or srcPos == gametypes.EQU_PART_RIDE):
            if gameglobal.rds.ui.wingAndMount.mediator:
                if srcPos == gametypes.EQU_PART_WINGFLY:
                    targetPos = 1
                else:
                    targetPos = 0
                it = self.equipment[srcPos]
                gameglobal.rds.ui.wingAndMount.addItem(it, targetPos, 0)
        BigWorld.player().dispatchEvent(const.EVENT_ITEM_MOVE, (srcKind,
         srcPage,
         srcPos,
         dstKind,
         dstPage,
         dstPos))

    def searchBestPosInInv(self, item):
        pg, ps = self.inv.searchBestInPages(item.id, item.cwrap, item)
        return (pg, ps)

    def discardItem(self, page, pos, amount = 1):
        gamelog.debug('PGF::Avatar discard item:', page, pos, amount)
        self.cell.discardItem(page, pos, amount)

    def constructItemInfo(self, kind, pageNo, pos):
        self.cell.randomItemInfo(kind, pageNo, str(pos))

    def resRandom(self, link):
        reFormat = re.compile('#\\[(.{8})\\](.{7})\\[(.+?)\\]#n#\\[0\\]', re.DOTALL)
        msg = reFormat.sub(pcharAdd, link)
        gameglobal.rds.ui.sendLink(msg)

    def activeStarSuccess(self, data):
        pass

    def activeStarFailed(self):
        pass

    def activeStarSuccessNew(self, data):
        gameglobal.rds.ui.equipChangeStarActivate.onActivateSuccess()

    def equipStarLvupSuccessNew(self, data):
        gameglobal.rds.ui.equipChangeStarLvUp.onActivateSuccess()

    def equipStarLvupInvSuccess(self, data):
        pass

    def equipStarLvupInvFailed(self):
        pass

    def enhanceSuccessNew(self, data):
        gameglobal.rds.ui.equipChangeEnhance.enhanceSuccess(data)
        gameglobal.rds.ui.equipRefineSuitsProp.refreshInfo()

    def enhanceSuccess(self, data):
        if not gameglobal.rds.ui.equipEnhance.getEnhanceItem():
            return
        uuid = gameglobal.rds.ui.equipEnhance.getEnhanceItem().uuid
        localTime = time.localtime(self.getServerTime())
        nowItem = gameglobal.rds.ui.equipEnhance.getEnhanceItem()
        preItem = gameglobal.rds.ui.equipEnhance.enhanceBeforeItem
        preLv = getattr(preItem, 'enhLv', 0)
        nowLv = getattr(nowItem, 'enhLv', 0)
        realEnhance = int(data.get('realRefining', 0) * 100)
        isUpdate = False
        if preLv < nowLv:
            isUpdate = True
            targetLv = nowLv
        else:
            targetLv = gameglobal.rds.ui.equipEnhance.enhanceTargetLv
        if isUpdate == False:
            fromEnhanceProgress = int(getattr(preItem, 'enhanceRefining', {}).get(targetLv, 0) * 100)
        else:
            fromEnhanceProgress = 0
        toEnhanceProgress = int(getattr(nowItem, 'enhanceRefining', {}).get(targetLv, 0) * 100)
        content = ''
        if isUpdate:
            self.showGameMsg(GMDD.data.ENHANCE_COMPLETE_LEVEL_INC, ())
            content = gameStrings.TEXT_EQUIPCHANGEENHANCEPROXY_574 % (nowLv, toEnhanceProgress)
            gameglobal.rds.ui.equipEnhance.playFailAnimation(0)
            gameglobal.rds.ui.equipEnhance.setResultText(nowLv, 0, fromEnhanceProgress, toEnhanceProgress)
            gameglobal.rds.ui.equipEnhanceResult.show()
        elif realEnhance > fromEnhanceProgress:
            content = gameStrings.TEXT_EQUIPCHANGEENHANCEPROXY_570 % (targetLv, fromEnhanceProgress, toEnhanceProgress)
            gameglobal.rds.ui.equipEnhanceResult.show()
            gameglobal.rds.ui.equipEnhance.playFailAnimation(0)
            gameglobal.rds.ui.equipEnhance.setResultText(targetLv, 1, fromEnhanceProgress, toEnhanceProgress)
        else:
            content = gameStrings.TEXT_EQUIPCHANGEENHANCEPROXY_566 % (targetLv, fromEnhanceProgress, realEnhance)
            gameglobal.rds.ui.equipEnhance.playFailAnimation(1)
            gameglobal.rds.ui.equipEnhance.setResultText(targetLv, 2, fromEnhanceProgress, realEnhance)
        self.addEnhanceHistory(uuid, localTime, content)

    def enhanceFaildNew(self, data):
        gameglobal.rds.ui.equipChangeEnhance.enhanceFaild(data)

    def enhanceFaild(self):
        gameglobal.rds.ui.equipEnhance.refreshContent()
        if not gameglobal.rds.ui.equipEnhance.getEnhanceItem():
            return
        uuid = gameglobal.rds.ui.equipEnhance.getEnhanceItem().uuid
        localTime = time.localtime(self.getServerTime())
        nowItem = gameglobal.rds.ui.equipEnhance.getEnhanceItem()
        preItem = gameglobal.rds.ui.equipEnhance.enhanceBeforeItem
        preLv = getattr(preItem, 'enhLv', 0)
        nowLv = getattr(nowItem, 'enhLv', 0)
        if preLv < nowLv:
            targetLv = nowLv
        else:
            targetLv = gameglobal.rds.ui.equipEnhance.enhanceTargetLv
        content = gameStrings.TEXT_EQUIPCHANGEENHANCEPROXY_609 % targetLv
        gameglobal.rds.ui.equipEnhance.playFailAnimation(2)
        gameglobal.rds.ui.equipEnhance.setResultText(targetLv, 3, 0, 0)
        self.addEnhanceHistory(uuid, localTime, content)
        self.showGameMsg(GMDD.data.ENHANCE_COMPLETE_LEVEL_KEEP, ())

    def enhancementTransferSuccess(self, isSuccess, downLv):
        if downLv > 0:
            self.showGameMsg(GMDD.data.EQUIP_ENHANCE_TRANSFER_SUCC_LV_DOWN, downLv)
        else:
            self.showGameMsg(GMDD.data.EQUIP_ENHANCE_TRANSFER_SUCC, ())

    def enhancementTransferSuccessNew(self, isSuccess, downLv):
        if downLv > 0:
            self.showGameMsg(GMDD.data.EQUIP_ENHANCE_TRANSFER_SUCC_LV_DOWN, downLv)
        else:
            self.showGameMsg(GMDD.data.EQUIP_ENHANCE_TRANSFER_SUCC, ())
        if isSuccess:
            gameglobal.rds.ui.equipChangeEnhanceTransfer.enhanceTransferSuccess()

    def onUseItemSucc(self, itemId):
        gameglobal.rds.tutorial.onUseItemEndCheck(itemId)
        gameglobal.rds.tutorial.onUseItem(itemId)
        data = CID.data.get(itemId, {})
        if data.get('useMultipleAtOnce', 0):
            gameglobal.rds.ui.itemBatchUse.onUseItem()
        if data.get('sType', 0) == Item.SUBTYPE_2_UNLOCK_MORPHER:
            key = None
            if data.has_key('faxing_style'):
                key = 'faxing_style'
            elif data.has_key('zhuangshi_style'):
                key = 'zhuangshi_style'
            requireSex = data.get('sex', 0)
            requireBodyType = data.get('bodyType', 0)
            value = data.get(key, None)
            subKey = (requireSex, requireBodyType)
            self.availableMorpher.setdefault(key, {})
            self.availableMorpher[key].setdefault(subKey, [])
            if value not in self.availableMorpher[key][subKey]:
                self.availableMorpher[key][subKey].append(value)
        elif data.get('sType', 0) == Item.SUBTYPE_2_RESET_SEX:
            self.isReturnToLogin = True
        elif data.get('sType', 0) == Item.SUBTYPE_2_SELECT_TO_OPEN_BOX:
            gameglobal.rds.ui.selectOpenBox.hide()
        if ID.data.get(itemId, {}).get('usePush', None) and gameglobal.rds.configData.get('enableItemUsePush', True):
            bagPage, bagPos = BigWorld.player().inv.findItemInPages(itemId)
            if bagPage != const.CONT_NO_PAGE and bagPos != const.CONT_NO_POS:
                gameglobal.rds.ui.itemPushUse.isPush = True
                if gameglobal.rds.ui.itemPushUse.isClickPush:
                    BigWorld.player().cell.checkUseCommonItem(bagPage, bagPos, const.RES_KIND_INV)
                elif Item(itemId).isStorehouse():
                    BigWorld.player().cell.checkUseCommonItem(bagPage, bagPos, const.RES_KIND_INV)
                else:
                    gameglobal.rds.ui.itemPushUse.hide()
            else:
                gameglobal.rds.ui.itemPushUse.hide()

    def repairLifeEquipSuccess(self, equipData):
        for (subType, part), data in equipData:
            newDura = data.get('cdura', None)
            newMDura = data.get('initMaxDura', None)
            equip = self.lifeEquipment.get(subType, part)
            if not equip:
                continue
            if newDura == None:
                try:
                    delattr(equip, 'cdura')
                except AttributeError:
                    pass

            else:
                setattr(equip, 'cdura', newDura)
            if newMDura == None:
                try:
                    delattr(equip, 'initMaxDura')
                except AttributeError:
                    pass

            else:
                setattr(equip, 'initMaxDura', newMDura)

        gameglobal.rds.ui.lifeSkillNew.refreshAssistPanel()

    def repairSpecialLifeEquipSuccess(self, equipData):
        for (subType, part), data in equipData:
            newDura = data.get('cdura', None)
            newMDura = data.get('initMaxDura', None)
            p = BigWorld.player()
            if subType == gametypes.LIFE_SKILL_TYPE_FISHING:
                equipInv = p.fishingEquip
            elif subType == gametypes.LIFE_SKILL_TYPE_EXPLORE:
                equipInv = p.exploreEquip
            equip = equipInv[part]
            if not equip:
                continue
            if newDura == None:
                try:
                    delattr(equip, 'cdura')
                except AttributeError:
                    pass

            else:
                setattr(equip, 'cdura', newDura)
            if newMDura == None:
                try:
                    delattr(equip, 'initMaxDura')
                except AttributeError:
                    pass

            else:
                setattr(equip, 'initMaxDura', newMDura)

        gameglobal.rds.ui.lifeSkillNew.refreshAssistPanel()

    def repairSuccess(self, equipData):
        for part, data in equipData:
            newDura = data.get('cdura', None)
            newMDura = data.get('initMaxDura', None)
            equip = self.equipment.get(part)
            if not equip:
                continue
            if newDura == None:
                try:
                    delattr(equip, 'cdura')
                except AttributeError:
                    pass

            else:
                setattr(equip, 'cdura', newDura)
            if newMDura == None:
                try:
                    delattr(equip, 'initMaxDura')
                except AttributeError:
                    pass

            else:
                setattr(equip, 'initMaxDura', newMDura)
            if not equip.isCanDye() and gameglobal.rds.ui.inventory.isDyeState:
                stat = uiConst.ITEM_GRAY
            elif equip.isLatchOfTime():
                stat = uiConst.ITEM_LATCH_TIME
            elif hasattr(equip, 'latchOfCipher'):
                stat = uiConst.ITEM_LATCH_CIPHER
            else:
                stat = uiConst.ITEM_NORMAL
            gameglobal.rds.ui.roleInfo.setSlotState(part, stat)

        gameglobal.rds.ui.equipRepair.setEquipState()
        self.showGameMsg(GMDD.data.REPAIR_FINISHED, ())

    def resSetProps(self, kind, uuid, page, pos, props):
        gamelog.debug('@zs impItem.resSetProps', self.id, kind, uuid, page, pos, props)
        if kind == const.RES_KIND_EQUIP:
            it = self.equipment.get(pos)
            if it and it.uuid == uuid:
                it.updateAttribute(props)
        elif kind == const.RES_KIND_SUB_EQUIP_BAG:
            it = self.subEquipment.get(page, pos)
            if it and it.uuid == uuid:
                it.updateAttribute(props)
        elif kind == const.RES_KIND_INV:
            self.inv.updateObj(uuid, page, pos, props)
            if props.has_key('cdura'):
                gameglobal.rds.ui.inventory.updateSlotState(page, pos)
        cEvent = Event(events.EVENT_ITEM_CHANGE, {'kind': kind,
         'page': page,
         'pos': pos})
        gameglobal.rds.ui.dispatchEvent(cEvent)

    def itemDurabilityUpdate(self, pos, newDura):
        gamelog.debug('@zs itemDurabilityUpdate', pos, newDura)
        p = BigWorld.player()
        equip = p.equipment.get(pos)
        if equip == const.CONT_EMPTY_VAL:
            return
        equip.cdura = newDura
        if equip.cdura < const.EQUIP_HALF_BROKEN * equip.initMaxDura:
            gameglobal.rds.ui.equipRepair.setEquipState()
        if equip.cdura == const.EQUIP_BROKEN:
            gameglobal.rds.ui.roleInfo.setSlotState(pos, uiConst.EQUIP_BROKEN)

    def lifeEquipItemDuraUpdate(self, subType, part, newDura):
        gamelog.debug('@hjx lifeEquipItemDuraUpdate', subType, part, newDura)
        p = BigWorld.player()
        equip = p.lifeEquipment.get(subType, part)
        if equip == const.CONT_EMPTY_VAL:
            return
        equip.cdura = newDura
        gameglobal.rds.ui.lifeSkillNew.refreshAssistPanel()

    def specialLifeEquipItemDuraUpdate(self, subType, parts, newDuras):
        p = BigWorld.player()
        if subType == gametypes.LIFE_SKILL_TYPE_FISHING:
            equipInv = p.fishingEquip
        else:
            equipInv = p.exploreEquip
        for i, part in enumerate(parts):
            equip = equipInv.get(part)
            if equip == const.CONT_EMPTY_VAL:
                continue
            equip.cdura = newDuras[i]

    def rideWingPropChanged(self, part, props):
        equip = self.equipment.get(part)
        talentTextMap = {gametypes.RIDE_TALENT_FLYRIDE: const.RIDE_WING_TALENT_FLY_TEXT,
         gametypes.RIDE_TALENT_DRAG_TAIL: const.RIDE_WING_TALENT_DRAGTAIL_TEXT,
         gametypes.RIDE_TALENT_MULTI_RIDER: const.RIDE_WING_TALENT_MULTI_TEXT,
         gametypes.RIDE_TALENT_SWIM: const.RIDE_WING_TALENT_SWIM_TEXT,
         gametypes.RIDE_TALENT_HUG: const.RIDE_WING_TALENT_MULTI_FLY_TEXT,
         gametypes.RIDE_TALENT_SHARE: const.RIDE_TALENT_SHARE_TEXT}
        if equip:
            oldStage = equip.rideWingStage
            for key, value in props.iteritems():
                if key == 'talents':
                    gotTalents = set(value).difference(set(getattr(equip, 'talents', [])))
                    lostTalents = set(getattr(equip, 'talents', [])).difference(set(value))
                    if gotTalents:
                        self.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.TEXT_IMPITEM_2005 % (equip.name, gameStrings.TEXT_IMPITEM_2006, ','.join((talentTextMap[x] for x in gotTalents))))
                    hungerName = SCD.data.get('WingDuraName', '')
                    typeName = SCD.data.get('WingDuraStageHunger', gameStrings.TEXT_IMPITEM_2009)
                    if equip.isRideEquip():
                        hungerName = SCD.data.get('RideDuraName', '')
                        typeName = SCD.data.get('RideDuraStageHunger', gameStrings.TEXT_IMPITEM_2012)
                    if lostTalents:
                        self.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.TEXT_IMPITEM_2014 % (equip.name,
                         hungerName,
                         typeName,
                         gameStrings.TEXT_IMPITEM_2015,
                         ','.join((talentTextMap[x] for x in lostTalents))))
                elif key == 'rideWingStage':
                    if value != getattr(equip, 'rideWingStage', 0):
                        self.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.TEXT_IMPITEM_2019 % (equip.name, SCD.data.get('rideWingStageText', {}).get(value, gameStrings.TEXT_GAME_1747)))
                setattr(equip, key, value)

            if oldStage != equip.rideWingStage and hasattr(self, 'ap'):
                self.ap.recalcSpeed()
            self.resSet(const.RES_KIND_EQUIP, equip, 0, part)
            self.checkExpireItem(equip)

    def setInvPosCount(self, posCountDict):
        self.inv.posCountDict = posCountDict
        for i in self.inv.getPageTuple():
            posCount = BigWorld.player().inv.posCountDict.get(i, 0)
            if posCount == 0:
                gameglobal.rds.ui.inventory.setBagTabAble(i, False)
                if gameglobal.rds.ui.inventory.page == i:
                    gameglobal.rds.ui.inventory.setFirstTab()
            else:
                gameglobal.rds.ui.inventory.setBagTabAble(i, True)
                if gameglobal.rds.ui.inventory.page == i:
                    gameglobal.rds.ui.inventory.setSlotCount(posCount)

    def getEquipment(self, entId):
        tgt = BigWorld.entities.get(entId)
        self.cell.getEquipment(tgt.roleName)

    def resEquipment(self, roleName, equip, lv, school, guildName, jingJie, aspect, physique, avatarConfig, signal, suitsCache, lastLogoffTime, guanYin, wenyin):
        gameglobal.rds.ui.targetRoleInfo.show(roleName, equip, lv, school, guildName, jingJie, aspect, physique, avatarConfig, signal, suitsCache, lastLogoffTime, guanYin, wenyin)

    def resTeamEquipment(self, teamCombatScores):
        gameglobal.rds.ui.fbDeadData.show(teamCombatScores)

    def updateBuyBackList(self, itemInfo, page):
        p = BigWorld.player()
        if page not in self.buyBackDict:
            p.buyBackDict[page] = [None] * const.BUY_BACK_LIST_SIZE
        else:
            for pos in range(len(self.buyBackDict[page])):
                p.buyBackDict[page][pos] = None

        for pos, it in enumerate(itemInfo):
            p.buyBackDict[page][pos] = it

        if page == const.BUY_BACK_SHOP_PAGE:
            gameglobal.rds.ui.shop.updateBuyBackItem()
        else:
            gameglobal.rds.ui.compositeShop.updateBuyBackItem()
            gameglobal.rds.ui.yunChuiShop.updateBuybackItem()

    def batchResInsert(self, resKind, data):
        for page, itemList in enumerate(data):
            for pos, itemDict in enumerate(itemList):
                if not itemDict:
                    continue
                item = Item()
                item.updateProp(itemDict)
                self.resInsert(resKind, item, page, pos)

    def batchInsertEquip(self, data):
        for part, itemDict in enumerate(data):
            if not itemDict:
                continue
            item = Item()
            item.updateProp(itemDict)
            self.resInsert(const.RES_KIND_EQUIP, item, 0, part)

    def batchInsertInvBar(self, data):
        for part, itemDict in enumerate(data):
            if not itemDict:
                continue
            item = Item()
            item.updateProp(itemDict)
            self.resInsert(const.RES_KIND_INV_BAR, item, 0, part)

    def batchInsertStorageBar(self, data):
        for part, itemDict in enumerate(data):
            if not itemDict:
                continue
            item = Item()
            item.updateProp(itemDict)
            self.resInsert(const.RES_KIND_STORAGE_BAR, item, 0, part)

    def batchInsertFashionBagBar(self, data):
        for part, itemDict in enumerate(data):
            if not itemDict:
                continue
            item = Item()
            item.updateProp(itemDict)
            self.resInsert(const.RES_KIND_FASHION_BAG_BAR, item, 0, part)

    def batchInsertMaterialBagBar(self, data):
        for part, itemDict in enumerate(data):
            if not itemDict:
                continue
            item = Item()
            item.updateProp(itemDict)
            self.resInsert(const.RES_KIND_MATERIAL_BAG_BAR, item, 0, part)

    def batchInsertSpriteMaterialBagBar(self, data):
        for part, itemDict in enumerate(data):
            if not itemDict:
                continue
            item = Item()
            item.updateProp(itemDict)
            self.resInsert(const.RES_KIND_SPRITE_MATERIAL_BAG_BAR, item, 0, part)

    def batchInsertFishingEquip(self, data):
        for part, itemDict in enumerate(data):
            if not itemDict:
                continue
            item = Item()
            item.updateProp(itemDict)
            self.resInsert(const.RES_KIND_FISHING_QUIP, item, 0, part)

    def batchInsertExploreEquip(self, data):
        for part, itemDict in enumerate(data):
            if not itemDict:
                continue
            item = Item()
            item.updateProp(itemDict)
            self.resInsert(const.RES_KIND_EXPLORE_EQUIP, item, 0, part)

    def batchInsertLifeEquip(self, data):
        for key, itemDict in data.iteritems():
            if not itemDict:
                continue
            subType, part = key
            item = Item()
            item.updateProp(itemDict)
            self.resInsert(const.RES_KIND_LIFE_EQUIP, item, subType, part)

    def batchInsertHierogramBagBar(self, data):
        for part, itemDict in enumerate(data):
            if not itemDict:
                continue
            item = Item()
            item.updateProp(itemDict)
            self.resInsert(const.RES_KIND_HIEROGRAM_BAG_BAR, item, 0, part)

    def checkExpireItem(self, item):
        if not item:
            return
        expireTime = item.getNearstExpireTime()
        if expireTime:
            self.addCheckExpireItemsCallback(expireTime)

    def addCheckExpireItemsCallback(self, tWhen):
        now = self.getServerTime()
        if not hasattr(self, '_nextCheckExpireItemsTime') or self._nextCheckExpireItemsTime <= now:
            self._nextCheckExpireItemsTime = 0
            self._nextCheckExpireItemsCallback = None
        if tWhen <= now - const.CLIENT_EXPIRETIME_CHECK_DELAY:
            return
        else:
            if tWhen <= now:
                tWhen = now + const.CLIENT_EXPIRETIME_CHECK_DELAY
            tWhen = tWhen + 1
            if self._nextCheckExpireItemsTime == 0 or tWhen < self._nextCheckExpireItemsTime:
                self._nextCheckExpireItemsTime = tWhen
                if self._nextCheckExpireItemsCallback:
                    BigWorld.cancelCallback(self._nextCheckExpireItemsCallback)
                self._nextCheckExpireItemsCallback = BigWorld.callback(tWhen - now, Functor(self.checkExpireItems, (self.inv,
                 None,
                 self.equipment,
                 self.fashionBag,
                 self.storage,
                 self.questBag)))
            return

    def checkExpireItems(self, containers = None, exclude = ()):
        if not self.inWorld:
            return
        else:
            now = self.getServerTime()
            tNext = 0
            p = self
            if containers and not isinstance(containers, tuple):
                containers = (containers,)
            allContainers = (p.inv,
             None,
             p.equipment,
             None,
             None,
             p.fashionBag,
             p.materialBag,
             p.cart,
             p.buyBackDict,
             None,
             None,
             self.storage,
             None,
             p.questBag)
            if not containers:
                containers = allContainers
            items = []
            resKind = None
            for container in containers:
                if not container:
                    continue
                resKind = allContainers.index(container)
                if isinstance(container, list):
                    for ps in range(len(container) - 1, -1, -1):
                        item = container[ps]
                        if item != const.CONT_EMPTY_VAL and isinstance(item, Item):
                            if item.isExpireTTL() or item.isEquipExpire():
                                BigWorld.player().dispatchEvent(const.EVENT_ITEM_CHANGE, (resKind,
                                 0,
                                 ps,
                                 item))
                            if (item.getTTLExpireType() in const.TTL_EXPIRE_NEED_PROCESS_TYPES or resKind in (const.RES_KIND_EQUIP,) and not hasattr(item, 'expired')) and item.isExpireTTL() or item.isEquipExpire():
                                items.append((resKind, 0, ps))
                                if resKind == const.RES_KIND_EQUIP:
                                    item.expired = True
                            elif hasattr(item, 'shihun') and not item.isShihun():
                                items.append((resKind, 0, ps))
                                item.setShihun(False)
                            else:
                                expireTime = item.getNearstExpireTime()
                                if expireTime > now - const.CLIENT_EXPIRETIME_CHECK_DELAY and (not tNext or expireTime < tNext):
                                    tNext = expireTime

                elif isinstance(container, dict):
                    for pg in container:
                        for ps in container:
                            item = container[pg][ps]
                            if item != const.CONT_EMPTY_VAL and isinstance(item, Item):
                                if item.isExpireTTL() or item.isEquipExpire():
                                    BigWorld.player().dispatchEvent(const.EVENT_ITEM_CHANGE, (resKind,
                                     pg,
                                     ps,
                                     item))
                                if item.getTTLExpireType() in const.TTL_EXPIRE_NEED_PROCESS_TYPES and item.isExpireTTL() or item.isEquipExpire():
                                    items.append((resKind, pg, ps))
                                elif hasattr(item, 'shihun') and not item.isShihun():
                                    items.append((resKind, 0, ps))
                                    item.setShihun(False)
                                else:
                                    expireTime = item.getNearstExpireTime()
                                    if expireTime > now and (not tNext or expireTime < tNext):
                                        tNext = expireTime

                else:
                    for pg in container.getPageTuple():
                        if pg in exclude:
                            continue
                        for ps in container.getPosTuple(pg):
                            item = container.getQuickVal(pg, ps)
                            if item != const.CONT_EMPTY_VAL and isinstance(item, Item):
                                if item.isExpireTTL() or item.isEquipExpire():
                                    BigWorld.player().dispatchEvent(const.EVENT_ITEM_CHANGE, (resKind,
                                     pg,
                                     ps,
                                     item))
                                if item.getTTLExpireType() in const.TTL_EXPIRE_NEED_PROCESS_TYPES and item.isExpireTTL() or item.isEquipExpire():
                                    items.append((resKind, pg, ps))
                                elif hasattr(item, 'shihun') and not item.isShihun():
                                    items.append((resKind, 0, ps))
                                    item.setShihun(False)
                                else:
                                    expireTime = item.getNearstExpireTime()
                                    if expireTime > now and (not tNext or expireTime < tNext):
                                        tNext = expireTime
                                if resKind == const.RES_KIND_INV:
                                    item.isExpireTTL() and gameglobal.rds.ui.actionbar.enableShortCutItem(item.id, False)

            if items:
                p.cell.itemsTTLExpire(items)
            if tNext:
                self.addCheckExpireItemsCallback(tNext)
            return

    def onPickItemSucc(self, entityId, isAssignFree):
        entity = BigWorld.entities.get(entityId)
        if not entity:
            return
        it = Item(entity.itemId, entity.itemNum)
        if it.type != Item.BASETYPE_MONEY and it.type != Item.BASETYPE_FUBEN:
            x, y = clientcom.worldPointToScreen(entity.position)
            if self.isInTeamOrGroup():
                isQualityMatch = getattr(it, 'quality', 0) >= entity.groupAssignQuality
                now = self.getServerTime()
                spaceNo = formula.getMapId(self.spaceNo)
                pickInterval = SCD.data.get('droppedItemFreePickInterval', const.DROPPED_ITEM_FREE_PICK_INTERVAL)
                droppedItemFreePickInterval = MCD.data.get(spaceNo, {}).get('droppedItemFreePickInterval', pickInterval)
                isOwnerMatch = now - entity.dropTime <= droppedItemFreePickInterval
                if not isAssignFree:
                    if entity.groupAssignWay == const.GROUP_ASSIGN_HEADER and isQualityMatch and isOwnerMatch:
                        gameglobal.rds.ui.showCurve([[x, y, it.id]], uiConst.ITEM_TO_TEAMBAG)
                    elif entity.groupAssignWay in (const.GROUP_ASSIGN_DICE, const.GROUP_ASSIGN_DICE_JOB) and isQualityMatch and isOwnerMatch:
                        gameglobal.rds.ui.showCurve([[x, y, it.id]], uiConst.ITEM_TO_DICEPANEL)
                    elif entity.groupAssignWay == const.GROUP_ASSIGN_AUCTION and isQualityMatch and isOwnerMatch:
                        gameglobal.rds.ui.showCurve([[x, y, it.id]], uiConst.ITEM_TO_AUCTION)
                    else:
                        gameglobal.rds.ui.showCurve([[x, y, it.id]], uiConst.ITEM_TO_INVENTORY)
                else:
                    gameglobal.rds.ui.showCurve([[x, y, it.id]], uiConst.ITEM_TO_INVENTORY)
            else:
                gameglobal.rds.ui.showCurve([[x, y, it.id]], uiConst.ITEM_TO_INVENTORY)

    def onBuyItem(self, itemId):
        gameglobal.rds.ui.showSpecialCurve([itemId])

    def resPrice(self, kind, page, pos, price):
        if kind == const.RES_KIND_BOOTH:
            it = BigWorld.player().booth.getQuickVal(page, pos)
            it.price = price

    def showCompositeShopBuyMessageBox(self, page, pos, many, fameId, fullType):
        fullDict = {const.FAME_FULL_TYPE_MAX: gameStrings.TEXT_IMPITEM_2349,
         const.FAME_FULL_TYPE_WEEK: gameStrings.TEXT_IMPITEM_2350,
         const.FAME_FULL_TYPE_DAY: gameStrings.TEXT_IMPITEM_2351}
        fameName = FD.data.get(fameId, 0).get('name', gameStrings.TEXT_CHALLENGEPROXY_199_1)
        msg = GMD.data.get(GMDD.data.FAME_LIMIT_WARNING, {}).get('text', '') % (gameStrings.TEXT_IMPITEM_2355,
         fameName,
         fullDict[fullType],
         fameName,
         gameStrings.TEXT_CONSIGNPROXY_1173)
        npc = BigWorld.entities.get(gameglobal.rds.ui.compositeShop.npcId)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(npc.cell.compositeShopBuy, BigWorld.player().openShopId, page, pos, many, True))

    def showFashionMessageBox(self, page, pos, part):
        cellCmd.fashionMessageBox(page, pos, part)

    def showEquipMessageBox(self, page, pos, part):
        cellCmd.equipMessageBox(page, pos, part)

    def updateEquipSlotState(self, part):
        item = self.equipment.get(part)
        gameglobal.rds.ui.roleInfo.onCheckEquipStarLvUp(part)
        gameglobal.rds.ui.actionbar.setEquipSlotState(item, part)

    def updateEquipItem(self, kind, item, page, pos, needCheck = True):
        if kind == const.RES_KIND_EQUIP:
            self.equipment.set(pos, item)
            gameglobal.rds.ui.roleInfo.onCheckEquipStarLvUp(pos)
        elif kind == const.RES_KIND_INV:
            self.inv.insertObj(item, page, pos)
        elif kind == const.RES_KIND_FASHION_BAG:
            self.fashionBag.insertObj(item, page, pos)
        elif kind == const.RES_KIND_WARDROBE_BAG:
            self.wardrobeBagUpdate(item)
        if needCheck:
            self.checkExpireItems((self.inv, None, self.equipment))
        BigWorld.player().dispatchEvent(const.EVENT_ITEM_CHANGE, (kind,
         page,
         pos,
         item))

    def updateEquipItemBySwitchDye(self, kind, item, page, pos):
        if kind == const.RES_KIND_WARDROBE_BAG:
            self.wardrobeBagUpdate(item)
        elif kind == const.RES_KIND_EQUIP:
            self.equipment[pos] = item
            self.wardrobeBag.refreshDrobeItems()
        self.itemDyeSchemeUpdate(item)

    def dyeEquipCallback(self, success):
        gameglobal.rds.ui.dyePlane.dyeEquipCallback(success)

    def randomDyeEquipCallback(self, success, equRes, equPage, equPos):
        gameglobal.rds.ui.randomDye.randomDyeEquipCallback(success, equRes, equPage, equPos)

    def dyeEquipDoubleCheck(self, resKind, equipPage, equipPos, consumeItemIds, dyeList, dyeMaterials):
        gamelog.debug('@hqx__________dyeEquipDoubleCheck')
        msg = gameStrings.DYE_EUIP_DOUBLE_CHECK_MSG
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(BigWorld.player().cell.dyeEquip, equipPage, str(equipPos), consumeItemIds, dyeList, resKind, dyeMaterials, True))

    def unlockDualDyeSucc(self, kind, item, page, pos):
        self.updateEquipItem(kind, item, page, pos, True)
        gameglobal.rds.ui.dyePlane.setEquip(page, pos, item, kind)

    def pushStarLvUpMsg(self, part):
        gameglobal.rds.ui.roleInfo.equipStarLvUpPush(part)

    def setFashionBagPosCount(self, posCountDict):
        self.fashionBag.posCountDict = posCountDict
        for i in range(0, const.STORAGE_PAGE_NUM):
            posCount = self.fashionBag.posCountDict.get(i, 0)
            if posCount == 0:
                gameglobal.rds.ui.fashionBag.setBagTabAble(i, False)
                if gameglobal.rds.ui.fashionBag.page == i:
                    gameglobal.rds.ui.fashionBag.setFirstTab()
            else:
                gameglobal.rds.ui.fashionBag.setBagTabAble(i, True)
                if gameglobal.rds.ui.fashionBag.page == i:
                    gameglobal.rds.ui.fashionBag.setSlotCount(posCount)

        enabledSlotCnt = 0
        for item in posCountDict:
            enabledSlotCnt = enabledSlotCnt + posCountDict[item]

        needRefreshFashionBag = False
        if hasattr(self.fashionBag, 'enabledSlotCnt'):
            if self.fashionBag.enabledSlotCnt != enabledSlotCnt:
                self.fashionBag.enabledSlotCnt = enabledSlotCnt
                needRefreshFashionBag = True
        else:
            self.fashionBag.enabledSlotCnt = enabledSlotCnt
            needRefreshFashionBag = True
        if needRefreshFashionBag:
            self.fashionBag.refreshContainer(self.fashionBag.enabledSlotCnt, const.FASHION_BAG_WIDTH, const.FASHION_BAG_HEIGHT, True)
            if gameglobal.rds.ui.fashionBag.mediator:
                gameglobal.rds.ui.fashionBag.refreshBag()

    def fashionBagPackSlotEnlarge(self, slotCnt):
        gameglobal.rds.ui.fashionBag.enablePackSlot(slotCnt)
        self.fashionBag.enabledPackSlotCnt = slotCnt

    def openFashionBag(self):
        gameglobal.rds.ui.fashionBag.show()

    def closePsersonalTreasureBox(self, boxId):
        p = BigWorld.player()
        if p.isInPUBG():
            p.closeTreasureBoxInPUBG(boxId)
        else:
            gameglobal.rds.ui.pickUp.hide()

    def openPersonalTreasureBoxRequest(self, boxId, items):
        p = BigWorld.player()
        if p.isInPUBG():
            p.pickTreasureBoxInPUBG(boxId, items)
        else:
            gameglobal.rds.ui.pickUp.show(boxId, items, False)

    def onUsePersonalTreasureBox(self, boxId, itemUUIDs):
        p = BigWorld.player()
        if p.isInPUBG():
            p.updateTreasureBoxInPUBG(boxId, itemUUIDs)
        else:
            gameglobal.rds.ui.pickUp.updateByList(boxId, itemUUIDs)

    def onPickPersonalTreasureBoxItem(self, ok, boxId, itemUUID):
        p = BigWorld.player()
        if ok:
            if p.isInPUBG():
                p.updateTreasureBoxInPUBG(boxId, itemUUID)
            else:
                gameglobal.rds.ui.pickUp.updateByOne(boxId, itemUUID)

    def onLeaveTreasureBoxTrap(self, boxId):
        p = BigWorld.player()
        if p.isInPUBG():
            p.closeTreasureBoxInPUBG(boxId)
        else:
            gameglobal.rds.ui.pickUp.hideById(boxId)

    def reforgeEquipJuexingRequest(self, page, pos, itemUUID, jxData):
        item = self.inv.getQuickVal(page, pos)
        if item:
            item.tempJXAlldata = jxData

    def onReforgeEquipJuexingStrength(self, resKind, page, pos, itemUUID, tempJXStrength, tempJXAddRatio):
        if resKind == const.RES_KIND_SUB_EQUIP_BAG:
            pos = gametypes.subEquipToEquipPartMap.get(pos, -1)
        gameglobal.rds.ui.equipChangeJuexingStrength.juexingStrengthResult(resKind, page, pos, itemUUID, tempJXStrength, tempJXAddRatio)

    def reforgeEquipJuexingRequestNew(self, resKind, page, pos, itemUUID, jxData):
        if resKind == const.RES_KIND_SUB_EQUIP_BAG:
            pos = gametypes.subEquipToEquipPartMap.get(pos, -1)
        gameglobal.rds.ui.equipChangeJuexingRebuild.juexingRebuildResult(resKind, page, pos, itemUUID, jxData)
        gameglobal.rds.ui.awakeRecast.juexingRebuildResult(resKind, page, pos, itemUUID, jxData)

    def onConfirmReforgeEquipJuexingStrength(self, resKind, page, pos, itemUUID, ok):
        if resKind == const.RES_KIND_SUB_EQUIP_BAG:
            pos = gametypes.subEquipToEquipPartMap.get(pos, -1)
        gameglobal.rds.ui.equipChangeJuexingStrength.juexingRebuildFinish(resKind, page, pos, itemUUID, ok)

    def reforgeEquipJuexingAllFinish(self, resKind, page, pos, itemUUID, ok):
        if resKind == const.RES_KIND_SUB_EQUIP_BAG:
            pos = gametypes.subEquipToEquipPartMap.get(pos, -1)
        gameglobal.rds.ui.equipChangeJuexingRebuild.juexingRebuildFinish(resKind, page, pos, itemUUID, ok)
        gameglobal.rds.ui.awakeRecast.juexingRebuildFinish(resKind, page, pos, itemUUID, ok)

    def setInvPackSlot(self, enabledPackSlotCnt):
        self.inv.enabledPackSlotCnt = enabledPackSlotCnt
        gameglobal.rds.ui.inventory.updateBagSlot(enabledPackSlotCnt)
        gamelog.debug('@zqc enabledPackSlotCnt ', enabledPackSlotCnt)

    def getEnhanceHistory(self, uuid):
        if not hasattr(self, 'enhanceHistory'):
            self.enhanceHistory = {}
        data = self.enhanceHistory.get(uuid, [])
        dataRe = copy.deepcopy(data)
        dataRe.reverse()
        return dataRe

    def addEnhanceHistory(self, uuid, historyTime, content):
        if not hasattr(self, 'enhanceHistory'):
            self.enhanceHistory = {}
        if not self.enhanceHistory.has_key(uuid):
            self.enhanceHistory[uuid] = []
        self.enhanceHistory[uuid].append((historyTime, content))
        if len(self.enhanceHistory[uuid]) > 50:
            self.enhanceHistory[uuid] = self.enhanceHistory[uuid][len(self.enhanceHistory[uuid]) - 50:]

    def onRecastItemSucc(self, uuidList):
        gameglobal.rds.ui.itemRecast.onRecastItemSucc(uuidList)

    def sendRedemption(self, data, ver):
        redemptions = []
        for dto in data:
            redemption = ItemRedemptionVal().fromDTO(dto)
            redemptions.append(redemption)

        gameglobal.rds.ui.equipRedemption.refreshData(redemptions, ver)
        if data:
            gameglobal.rds.ui.funcNpc.onFuncState()
            gameglobal.rds.ui.equipRedemption.show(gameglobal.rds.ui.equipRedemption.npcId)
        else:
            gameglobal.rds.ui.funcNpc.close()
            self.showGameMsg(GMDD.data.ITEM_REDEMPTION_NO_ITEMS, ())

    def sendRedemptionKeep(self):
        data = gameglobal.rds.ui.equipRedemption.redemptions
        if data:
            gameglobal.rds.ui.funcNpc.onFuncState()
            gameglobal.rds.ui.equipRedemption.show(gameglobal.rds.ui.equipRedemption.npcId)
        else:
            gameglobal.rds.ui.funcNpc.close()
            self.showGameMsg(GMDD.data.ITEM_REDEMPTION_NO_ITEMS, ())

    def onUpdateRedemption(self, data, ver):
        redemption = ItemRedemptionVal().fromDTO(data)
        gameglobal.rds.ui.equipRedemption.updateItem(redemption, ver)

    def onRemoveRedemption(self, uuid, ver):
        gameglobal.rds.ui.equipRedemption.removeItem(uuid, ver)

    def onProbePassiveItemByAttribute(self, callbackType, found, page, pos, errorMsg):
        if callbackType in (Item.SUBTYPE_2_RELIVE, Item.SUBTYPE_2_RELIVE_CW):
            gameglobal.rds.ui.deadAndRelive.reliveShowMessage(found, page, pos)
        elif errorMsg:
            self.showGameMsg(*errorMsg)

    def onRecycleItemSucc(self):
        if gameglobal.rds.ui.itemRecall.recallMed:
            gameglobal.rds.ui.itemRecall.resetRecall()

    def onProbeRecycleItemSucc(self, info):
        itemList, compExp, compCash, compFames = info
        gameglobal.rds.ui.itemRecall.updateEquipDisassData(itemList, compExp, compCash, compFames)

    def onProbeRecycleItemFail(self):
        pass

    def showResetEquipPrefixConfirm(self, npcEntId, page, pos, triggerId):
        item = BigWorld.player().inv.getQuickVal(page, pos)
        preGroupId, prefixId, opNUID = item.popProp('newPrefixInfo')
        newIt = item.deepcopy()
        newIt.removePrefixProps()
        newIt.preprops = []
        newIt.prefixInfo = (preGroupId, prefixId)
        prefixData = EPFPD.data.get(preGroupId)
        data = {}
        for pd in prefixData:
            if pd['id'] == prefixId:
                data = pd
                break

        if not data:
            return
        if data.has_key('props'):
            for pid, pType, pVal in data['props']:
                newIt.preprops.append((pid, pType, pVal))

    def showResetEquipPrefixConfirmNew(self, resKind, page, pos):
        if resKind == const.RES_KIND_SUB_EQUIP_BAG:
            pos = gametypes.subEquipToEquipPartMap.get(pos, -1)
        gameglobal.rds.ui.equipChangePrefixRebuild.prefixRebuildResult(resKind, page, pos)

    def resetEquipPrefixFinish(self, resKind, page, pos, ok):
        if resKind == const.RES_KIND_SUB_EQUIP_BAG:
            pos = gametypes.subEquipToEquipPartMap.get(pos, -1)
        gameglobal.rds.ui.equipChangePrefixRebuild.prefixRebuildFinish(resKind, page, pos, ok)

    def onExchangeEquipPreProp(self, ok):
        pass

    def onExchangeEquipPrePropNew(self, ok, srcUUID, tgtUUID):
        if ok:
            gameglobal.rds.ui.equipChangePrefixTransfer.prefixTransferSuccess(srcUUID, tgtUUID)

    def onEquipPropsTransfer(self, ok):
        pass

    def addSuitEffectToItemSucc(self, suitId):
        gameglobal.rds.ui.equipSuit.onActivateSuccess()

    def addSuitEffectToItemSuccNew(self, resKind, tgtEquipPage, tgtEquipPos, suitId):
        gameglobal.rds.ui.equipChangeSuitActivate.onActivateSuccess()

    def onNotifyExpXiuWei(self):
        if gameglobal.rds.ui.bottle.mediator:
            gameglobal.rds.ui.bottle.refresh()
        elif self.expXiuWeiPool == 0:
            gameglobal.rds.ui.bottle.notify()

    def onNotifyMakeSucc(self):
        if gameglobal.rds.ui.bottle.mediator:
            gameglobal.rds.ui.bottle.refresh()

    def onSetXiuWeiItem(self, itemId):
        if not itemId:
            return
        if gameglobal.rds.ui.bottle.mediator:
            gameglobal.rds.ui.bottle.setItem(itemId)

    def onUseItemOfExpXiuWeiPoolSucc(self):
        if gameglobal.rds.ui.bottle.mediator:
            gameglobal.rds.ui.bottle.refresh()

    def onUseFireworksReturn(self, suc):
        if suc:
            if gameglobal.rds.ui.fireWorkSender.mediator:
                gameglobal.rds.ui.fireWorkSender.clearWidget()

    def reserveCrossInv(self, pg, pos, srcPage, srcPos, val):
        if not self.inWorld:
            return
        else:
            srcIt = self.inv.getQuickVal(srcPage, srcPos)
            if val and srcIt:
                self.crossInv.reservedDict[pg, pos] = srcIt.uuid
            if not val:
                self.crossInv.reservedDict.pop((pg, pos), None)
            return

    def onSetRaffleDial(self, page, pos, dial):
        gameglobal.rds.ui.raffle.choose(page, pos, dial - 1)

    def onUseItemOfRaffle(self, page, pos, dial):
        gameglobal.rds.ui.raffle.success(page, pos, dial - 1)

    def onMixEquipItemSucc(self, triggerId):
        mixType = ESD.data.get(triggerId, {}).get('type')
        if mixType == gametypes.ITEM_SYNTHESIZE_JEWELRY:
            gameglobal.rds.ui.mixFameJewelry.mixJewelrySucc()
        else:
            gameglobal.rds.ui.equipMixNew.refreshAllSuc()

    def onUpgradeEquipItemSucc(self, triggerId):
        gameglobal.rds.ui.equipMixNew.refreshAllSuc()

    def setMaterialBagPosCount(self, posCountDict):
        self.materialBag.posCountDict = posCountDict
        gameglobal.rds.ui.meterialBag.refreshAll()

    def materialBagPackSlotEnlarge(self, slotCnt):
        gameglobal.rds.ui.meterialBag.enablePackSlot(slotCnt)
        self.materialBag.enabledPackSlotCnt = slotCnt

    def setSpriteMaterialBagPosCount(self, posCountDict):
        self.spriteMaterialBag.posCountDict = posCountDict
        gameglobal.rds.ui.spriteMaterialBag.refreshAllWithPackSlot()

    def spriteMaterialBagPackSlotEnlarge(self, slotCnt):
        self.spriteMaterialBag.enabledPackSlotCnt = slotCnt
        gameglobal.rds.ui.spriteMaterialBag.refreshAllWithPackSlot()

    def commonBagPackSlotEnlarge(self, bagId, slotCnt):
        """
        :param bagId:   const.RES_KIND_HIEROGRAM_BAG \xe7\xa5\x9e\xe6\xa0\xbc\xe5\x8c\x85
        """
        if bagId == const.RES_KIND_HIEROGRAM_BAG:
            self.hierogramBag.enabledPackSlotCnt = slotCnt
            gameglobal.rds.ui.runeInv.refreshInfo()

    def setCommonBagPosCount(self, bagId, posCountDict):
        if bagId == const.RES_KIND_HIEROGRAM_BAG:
            self.hierogramBag.posCountDict = posCountDict
            gameglobal.rds.ui.runeInv.refreshInfo()

    def resSubSysPropsUpdate(self, resKind, page, pos, data):
        if resKind == const.RES_KIND_HIEROGRAM_CRYSTALS:
            it = self.hierogramDict.get('hieroCrystals', {}).get((page, pos), const.CONT_EMPTY_VAL)
        else:
            bag = self.__getBagByResKind(resKind)
            it = bag.getQuickVal(page, pos)
        if it == const.CONT_EMPTY_VAL:
            return
        for subSysType, subSysProps in data.iteritems():
            if not it.subSysProps.has_key(subSysType):
                it.subSysProps[subSysType] = {}
            it.subSysProps[subSysType].update(subSysProps)

    def tuzhuangCallBack(self, result):
        if result:
            self.showGameMsg(GMDD.data.TUZHUANG_BUY_SUCCESS, ())
            gameglobal.rds.ui.tuZhuang.refreshMyMoney()
            if gameglobal.rds.ui.tuZhuang.isShow:
                gameglobal.rds.ui.tuZhuang.hide()
        else:
            self.showGameMsg(GMDD.data.TUZHUANG_BUY_FAIL, ())

    def onHuanfuSuccess(self):
        self.showGameMsg(GMDD.data.HUANFU_SUCCESS, ())
        if gameglobal.rds.ui.tuZhuang.isShow:
            gameglobal.rds.ui.tuZhuang.hide()

    def onHuanfuFailed(self):
        self.showGameMsg(GMDD.data.HUANFU_FAIL, ())

    def onMakeEquipSucc(self, tgtEquipId, makeType, guid):
        gameglobal.rds.ui.manualEquip.showSuccAni()
        gameglobal.rds.ui.manualEquip.refreshDetailInfo()

    def onIdentifyEquipSucc(self, tgtEquipId, guid):
        gameglobal.rds.ui.showScreenUI('widgets/ManualEquipSuccess.swf', 45)

    def onSwitchEquipBegin(self):
        gameglobal.rds.ui.roleInfo.switchEquipBegin()

    def onSwitchEquipSucc(self):
        self.showGameMsg(GMDD.data.SWITCH_EQUP_SUCCESS, ())
        self.fillGemToEquipments(True)
        gameglobal.rds.ui.roleInfo.switchEquipSucc()

    def onSyncMakeManualEquipDiscount(self, cnt):
        self.manualEquipDiscount = cnt
        gameglobal.rds.ui.manualEquip.refreshDetailInfo()

    def onUnrefineManualEquipment(self):
        gameglobal.rds.ui.equipChangeRefining.refreshInfo()

    def onRefineManualEquipment(self, resKind, page, pos, randomIdx):
        gamelog.info('jbx:onRefineManualEquipment', resKind, page, pos, randomIdx)
        gameglobal.rds.ui.equipChangeRefining.itemChange(resKind, page, pos, randomIdx)

    def onUpgradeEquipSucc(self, code):
        gamelog.info('jbx:onUpgradeEquipSucc', code)
        gameglobal.rds.ui.manualEquipLvUp.onUpgradeEquipSucc()


class InvClient(InventoryCommon):

    def __init__(self, pageCount, width, height, resKind):
        super(InvClient, self).__init__(pageCount, width, height, resKind)
        self.posCountDict = {}

    def getPosTuple(self, page):
        if not self._isValidPage(page):
            return ()
        return range(self.getPosCount(page))

    def getPosCount(self, page):
        if not self._isValidPage(page):
            return 0
        return self.posCountDict.get(page, 0)


class RideWingBagClient(InventoryCommon):
    ORIGINAL_POS_NUM = 3

    def __init__(self, pageCount, width, height, resKind):
        super(RideWingBagClient, self).__init__(pageCount, width, height, resKind)
        self.posCountDict = {}

    def getPosTuple(self, page):
        if not self._isValidPage(page):
            return ()
        return range(self.getPosCount(page))

    def getPosCount(self, page):
        if not self._isValidPage(page):
            return 0
        return self.posCountDict.get(page, 0)

    def canEnlargeSlot(self, page):
        if not self._isValidPage(page):
            return False
        count = self.getPosCount(page)
        if count + 1 > self.posCount:
            return False
        rideWingBagEnlargeCost = SCD.data.get('rideWingBagEnlargeCost', [])
        if self.getEnlargeSlotIndex(page) >= len(rideWingBagEnlargeCost):
            return False
        return True

    def getEnlargeSlotIndex(self, page):
        count = self.getPosCount(page)
        return count - self.ORIGINAL_POS_NUM


class WardrobeClient(object):

    def __init__(self):
        super(WardrobeClient, self).__init__()
        self.tempDrobeItems = {}
        self.drobeItems = {}
        self.loveList = None
        self.schemeInfo = None

    def onEquipChanged(self):
        self.refreshDrobeItems()

    def getDrobeItem(self, uuid):
        return self.drobeItems.get(uuid, None)

    def hasItem(self, assosiateIds):
        for uuid in self.drobeItems.keys():
            item = self.drobeItems.get(uuid, None)
            if item:
                if item.id in assosiateIds:
                    return True

        return False

    def initInfo(self, data):
        if data:
            for uuid in data:
                itemDict = data[uuid]
                if not itemDict:
                    continue
                item = Item()
                item.updateProp(itemDict)
                self.drobeItems[uuid] = item

        p = BigWorld.player()
        self.refreshDrobeItems()

    def getDrobeItems(self):
        if not self.tempDrobeItems:
            self.refreshDrobeItems()
        return self.tempDrobeItems

    def refreshDrobeItems(self):
        self.tempDrobeItems = {}
        for uuid in self.drobeItems:
            self.tempDrobeItems[uuid] = self.drobeItems[uuid]

        p = BigWorld.player()
        equipments = p.equipment
        for part in xrange(len(equipments)):
            equip = equipments[part]
            if equip and equip.isStorageByWardrobe():
                uuid = getattr(equip, 'uuid', 0)
                if uuid:
                    self.tempDrobeItems[uuid] = equip

    def requireLoveList(self):
        if self.loveList == None:
            BigWorld.player().base.queryWardrobeLoveList()

    def isLoveUUID(self, uuid):
        if self.loveList == None:
            return False
        else:
            return uuid in self.loveList

    def updateLoveList(self, loveList):
        self.loveList = loveList

    def updateSchemeInfo(self, schemeInfo):
        self.schemeInfo = schemeInfo

    def addItem(self, uuid, item):
        self.drobeItems[uuid] = item
        self.refreshDrobeItems()

    def delItem(self, uuid):
        del self.drobeItems[uuid]
        self.refreshDrobeItems()

    def changeItem(self, uuid, item):
        self.drobeItems[uuid] = item
        self.refreshDrobeItems()
