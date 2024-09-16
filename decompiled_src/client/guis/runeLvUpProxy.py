#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/runeLvUpProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import utils
import gametypes
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from uiProxy import SlotDataProxy
from item import Item
from guis import ui
from guis import events
from callbackHelper import Functor
from data import rune_data as RD
from data import equip_gem_data as EGD
from data import game_msg_data as GMD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from cdata import rune_lv_up_consume_data as RLUCD
from cdata import equip_gem_inverted_data as EGID

class RuneLvUpProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(RuneLvUpProxy, self).__init__(uiAdapter)
        self.modelMap = {'runeLvUp': self.onRuneLvUp,
         'removeItem': self.onRemoveItem,
         'changeTab': self.onChangeTab}
        self.type = 'runeLvUp'
        self.bindType = 'runeLvUp'
        self.runeData = {}
        self.newRune = None
        self.mediator = None
        self.npcId = 0
        self.pageType = 'runeLvUp'
        self.costItemId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_RUNE_LVUP, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_RUNE_LVUP:
            self.mediator = mediator
            self.refreshLvUpBtn()

    def clearWidget(self):
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_RUNE_LVUP)

    def reset(self):
        super(self.__class__, self).reset()
        self.runeData = {}
        self.newRune = None
        self.pageType = 'runeLvUp'
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def clearPanel(self):
        for i in range(5):
            key = 'runeLvUp0.slot%d' % i
            bar, slot = self.getSlotID(key)
            self.removeItem(bar, slot)

        key = 'runeLvUp1.slot0'
        bar, slot = self.getSlotID(key)
        self.removeItem(bar, slot)

    def show(self, npcId):
        self.npcId = npcId
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RUNE_LVUP)

    def onChangeTab(self, *arg):
        self.pageType = arg[3][0].GetString()
        self.runeData = {}
        self.newRune = None
        self.clearPanel()
        self.refreshLvUpBtn()
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[8:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'runeLvUp%d.slot%d' % (bar, slot)

    def addNewRuneItem(self, newRune):
        self.newRune = newRune
        self.addItem(newRune, 1, 0)
        runeKey = tuple(self.runeData.keys())
        for id in runeKey:
            self.removeItem(0, id)

    @ui.checkItemIsLock([1, 2])
    def addRuneItem(self, pageSrc, posSrc, pageDes, posDes):
        p = BigWorld.player()
        item = p.inv.getQuickVal(pageSrc, posSrc)
        if posDes in self.runeData:
            pageRemove, posRemove = self.runeData[posDes]
            del self.runeData[posDes]
            gameglobal.rds.ui.inventory.updateSlotState(pageRemove, posRemove)
        if item:
            self.runeData[posDes] = (pageSrc, posSrc)
            gameglobal.rds.ui.inventory.updateSlotState(pageSrc, posSrc)
            self.addItem(item, pageDes, posDes)
            self.removeItem(1, 0)

    def addItem(self, item, page, pos):
        if item is not None:
            key = self._getKey(page, pos)
            if self.binding.get(key, None) is not None:
                data = uiUtils.getGfxItem(item, appendInfo={'count': 1})
                self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data, True))
                self.refreshLvUpBtn()

    def removeItem(self, page, pos):
        if not page and pos in self.runeData:
            invPage, invPos = self.runeData[pos]
            del self.runeData[pos]
            gameglobal.rds.ui.inventory.updateSlotState(invPage, invPos)
            self.refreshLvUpBtn()
        key = self._getKey(page, pos)
        if self.binding.get(key, None) is not None:
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
        if self.runeData == {} and self.mediator:
            self.mediator.Invoke('resetNeedItem')

    def onGetToolTip(self, *arg):
        p = BigWorld.player()
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        if bar:
            if self.newRune:
                return gameglobal.rds.ui.inventory.GfxToolTip(self.newRune)
        elif self.runeData[slot]:
            page, pos = self.runeData[slot]
            item = p.inv.getQuickVal(page, pos)
            if item:
                return gameglobal.rds.ui.inventory.GfxToolTip(item)
        return GfxValue('')

    def onRuneLvUp(self, *arg):
        runeData = tuple(self.runeData.values())
        hasBind = False
        hasUnBind = False
        runes = []
        for itemPos in runeData:
            item = BigWorld.player().inv.getQuickVal(itemPos[0], itemPos[1])
            if not item:
                continue
            if item.isForeverBind():
                hasBind = True
            else:
                hasUnBind = True
            if not BigWorld.player().inv.isEmpty(itemPos[0], itemPos[1]):
                runes.append(BigWorld.player().inv.getQuickVal(itemPos[0], itemPos[1]))

        if not runes:
            return
        tRuneType = self._getRuneItemType(runes[0].id)
        tLv = self._getRuneItemLv(runes[0].id)
        itemCost = RLUCD.data.get((tLv, tRuneType), {}).get('itemCost', [])
        if len(itemCost) > 0:
            itemId = int(itemCost[0])
            parentId = uiUtils.getParentId(itemId)
            _result1 = BigWorld.player().inv.countItemBind(itemId)
            _result2 = BigWorld.player().inv.countItemBind(parentId)
            hasCostItemBind = BigWorld.player().inv.countItemChild(itemId)
            _result3 = False
            if hasCostItemBind[0]:
                for childId in hasCostItemBind[1]:
                    _result3 = BigWorld.player().inv.countItemBind(childId)

            if _result1 or _result2 or _result3:
                hasBind = True
        if hasBind and hasUnBind and self.pageType == 'runeLvUp':
            txt = uiUtils.getTextFromGMD(GMDD.data.RUNE_BIND_CONFIRM)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, Functor(self.realCommit, runeData))
        else:
            self.realCommit(runeData)

    def realCommit(self, runeData):
        if self.pageType == 'runeLvUp':
            if self.checkRuneSubTypes(runeData):
                self.confirmRuneLvUp(runeData)
            else:
                descStr = gameStrings.TEXT_RUNELVUPPROXY_198
                descStr = GMD.data.get(GMDD.data.RUNE_LV_UP_MIX_TYPES, {}).get('text', descStr)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(descStr, Functor(self.confirmRuneLvUp, runeData), msgType='runeLvUp', isShowCheckBox=True)
        elif self.pageType == 'yinyangGem' and runeData:
            self.mixEquipGem(runeData)

    def confirmRuneLvUp(self, runeData):
        p = BigWorld.player()
        if runeData and self.npcId:
            npcEnt = BigWorld.entities.get(self.npcId)
            if gameglobal.rds.configData.get('enableHierogram', False):
                npcEnt and npcEnt.cell.hieroCrystalLevelUp(runeData)
            else:
                npcEnt and npcEnt.cell.runeLvUp(runeData)
        else:
            p.showGameMsg(GMDD.data.RUNE_LVUP_ITEM_LESS, ())

    def checkRuneSubTypes(self, runeData):
        p = BigWorld.player()
        if runeData and self.npcId:
            srcGems = [ p.inv.getQuickVal(pg, pos) for pg, pos in runeData ]
            firstGemType = 0
            for gem in srcGems:
                if gem:
                    firstGemType = self._getRuneItemSubType(gem.id)
                    break

            for gem in srcGems:
                if gem:
                    gemType = self._getRuneItemSubType(gem.id)
                    if firstGemType != gemType:
                        return False

        return True

    def mixEquipGem(self, runeData):
        p = BigWorld.player()
        srcGems = [ p.inv.getQuickVal(pg, pos) for pg, pos in runeData ]
        if not all(srcGems):
            return
        bindInfo = [ gem.isForeverBind() for gem in srcGems if gem ]
        gemData = utils.getEquipGemData(srcGems[0].id)
        gemLv, gemType, gemSubType = gemData.get('lv', 0), gemData.get('type', 0), gemData.get('subType', 0)
        if gemLv == 0:
            return
        newGemId = EGID.data.get((gemLv + 1, gemType, gemSubType))
        newGemData = utils.getEquipGemData(newGemId)
        mixItemNeed = EGD.data.get(newGemId, {}).get('mixItemNeed')
        if mixItemNeed:
            bindNum = p.inv.countItemInPages(mixItemNeed, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_ONLY, enableParentCheck=True)
            bindInfo.append(bindNum > 0)
        if any(bindInfo) and not all(bindInfo):
            msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_MIX_GEM_BIND, gameStrings.TEXT_RUNELVUPPROXY_253)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._onConfirmMixBindEquipGem, runeData))
        else:
            self._onConfirmMixBindEquipGem(runeData)

    def _onConfirmMixBindEquipGem(self, runeData):
        p = BigWorld.player()
        srcGems = [ p.inv.getQuickVal(pg, pos) for pg, pos in runeData ]
        if not all(srcGems):
            return
        bindInfo = [ gem.isForeverBind() for gem in srcGems ]
        gemData = utils.getEquipGemData(srcGems[0].id)
        gemLv, gemType, gemSubType = gemData.get('lv', 0), gemData.get('type', 0), gemData.get('subType', 0)
        if gemLv == 0:
            return
        newGemId = EGID.data.get((gemLv + 1, gemType, gemSubType))
        newGemData = utils.getEquipGemData(newGemId)
        if newGemData.has_key('levelLimit') and p.lv < newGemData['levelLimit']:
            msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_MIX_GEM_LV_LIMIT, gameStrings.TEXT_RUNELVUPPROXY_274)
            msg = msg % (newGemData.get('orderLimit', 1),)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._onConfirmMixLvLimitEquipGem, runeData))
        else:
            p.cell.mixEquipGem(runeData)

    def _onConfirmMixLvLimitEquipGem(self, runeData):
        BigWorld.player().cell.mixEquipGem(runeData)

    def onRemoveItem(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        self.removeItem(bar, slot)

    def refreshLvUpBtn(self):
        if self.mediator:
            runeData = tuple(self.runeData.values())
            if self.pageType == 'runeLvUp':
                isEnable, cash, msg = self._checkRuneLvUp(runeData)
            elif self.pageType == 'yinyangGem':
                isEnable, cash, msg = self._checkYinyangGem(runeData)
            self.mediator.Invoke('refreshLvUpBtn', (GfxValue(isEnable), GfxValue(cash), GfxValue(gbk2unicode(msg))))

    def _checkRuneLvUp(self, runeData):
        cash = ''
        if not runeData:
            return (False, cash, GMD.data.get(GMDD.data.RUNE_LVUP_RULE_NONE, {}).get('text', gameStrings.TEXT_RUNELVUPPROXY_301))
        p = BigWorld.player()
        runes = []
        for page, pos in runeData:
            if p.inv.isEmpty(page, pos):
                return (False, cash, GMD.data.get(GMDD.data.RUNE_LVUP_RULE_NONE, {}).get('text', gameStrings.TEXT_RUNELVUPPROXY_301))
            runes.append(p.inv.getQuickVal(page, pos))

        tRuneType = self._getRuneItemType(runes[0].id)
        if tRuneType not in const.ALL_RUNE_TYPE:
            return (False, cash, GMD.data.get(GMDD.data.RUNE_LVUP_RULE_NONE, {}).get('text', gameStrings.TEXT_RUNELVUPPROXY_301))
        tLv = self._getRuneItemLv(runes[0].id)
        for rIt in runes:
            if self._getRuneItemLv(rIt.id) != tLv:
                return (False, cash, GMD.data.get(GMDD.data.RUNE_LVUP_RULE_LV_ERROR, {}).get('text', gameStrings.TEXT_RUNELVUPPROXY_317))
            if self._getRuneItemType(rIt.id) != tRuneType:
                return (False, cash, GMD.data.get(GMDD.data.RUNE_LVUP_RULE_TYPE_ERROR, {}).get('text', gameStrings.TEXT_RUNELVUPPROXY_319))

        needNum = const.RUNE_ITEM_MIX_NUM_NEED.get(tRuneType, 0)
        if len(runes) > needNum:
            return (False, cash, GMD.data.get(GMDD.data.RUNE_LVUP_RULE_NUM_MORE, {}).get('text', gameStrings.TEXT_RUNELVUPPROXY_323) % const.RUNE_TYPE_DESC[tRuneType])
        if len(runes) < needNum:
            return (False, cash, GMD.data.get(GMDD.data.RUNE_LVUP_RULE_NUM_LESS, {}).get('text', gameStrings.TEXT_RUNELVUPPROXY_326) % (needNum - len(runes), const.RUNE_TYPE_DESC[tRuneType]))
        if (tLv, tRuneType) not in RLUCD.data:
            return (False, cash, '')
        cash = str(RLUCD.data[tLv, tRuneType].get('mCost', 0))
        if not self.updateCost():
            return (False, cash, GMD.data.get(GMDD.data.RUNE_LVUP_NOT_ENOUGH_ITEM_COST, {}).get('text', gameStrings.TEXT_RUNELVUPPROXY_334))
        return (True, cash, '')

    def updateCost(self):
        runes = []
        isEnough = True
        runeData = tuple(self.runeData.values())
        for page, pos in runeData:
            if not BigWorld.player().inv.isEmpty(page, pos):
                runes.append(BigWorld.player().inv.getQuickVal(page, pos))

        itemId = 0
        needNum = 0
        if self.pageType == 'runeLvUp':
            tRuneType = self._getRuneItemType(runes[0].id)
            tLv = self._getRuneItemLv(runes[0].id)
            itemCost = RLUCD.data.get((tLv, tRuneType), {}).get('itemCost', [])
            if len(itemCost) > 0:
                itemId = itemCost[0]
                needNum = itemCost[1]
        elif self.pageType == 'yinyangGem':
            gemData = utils.getEquipGemData(runes[0].id)
            gemLv, gemType, gemSubType = gemData.get('lv', 0), gemData.get('type', 0), gemData.get('subType', 0)
            newGemId = EGID.data.get((gemLv + 1, gemType, gemSubType))
            mixItemNeed = EGD.data.get(newGemId, {}).get('mixItemNeed')
            if mixItemNeed:
                itemId = mixItemNeed
                needNum = 1
        if itemId > 0 and needNum > 0:
            itemInfo = uiUtils.getGfxItemById(itemId)
            ownNum = BigWorld.player().inv.countItemInPages(int(itemId), enableParentCheck=True)
            countStr = '%d/%d' % (ownNum, needNum)
            if ownNum >= needNum:
                countStr = uiUtils.toHtml(countStr, '#FFFFE7')
            else:
                countStr = uiUtils.toHtml(countStr, '#F43804')
                isEnough = False
            itemInfo['count'] = countStr
            if self.mediator:
                self.mediator.Invoke('updateCost', uiUtils.dict2GfxDict(itemInfo, True))
        return isEnough

    def _checkYinyangGem(self, runeData):
        cash = ''
        if not runeData:
            return (False, cash, GMD.data.get(GMDD.data.EQUIP_GEM_LVUP_RULE_NONE, {}).get('text', gameStrings.TEXT_RUNELVUPPROXY_384))
        p = BigWorld.player()
        runes = []
        for page, pos in runeData:
            if p.inv.isEmpty(page, pos):
                return (False, cash, GMD.data.get(GMDD.data.EQUIP_GEM_LVUP_RULE_NONE, {}).get('text', gameStrings.TEXT_RUNELVUPPROXY_384))
            runes.append(p.inv.getQuickVal(page, pos))

        gemData = utils.getEquipGemData(runes[0].id)
        gemLv, gemType, gemSubType = gemData.get('lv', 0), gemData.get('type', 0), gemData.get('subType', 0)
        for rIt in runes:
            if self._getYinyangGemLv(rIt.id) != gemLv:
                return (False, cash, GMD.data.get(GMDD.data.EQUIP_GEM_LVUP_RULE_LV_ERROR, {}).get('text', gameStrings.TEXT_RUNELVUPPROXY_397))
            if self._getYinyangGemType(rIt.id) != gemType:
                return (False, cash, GMD.data.get(GMDD.data.EQUIP_GEM_LVUP_RULE_TYPE_ERROR, {}).get('text', gameStrings.TEXT_RUNELVUPPROXY_399))

        newGemId = EGID.data.get((gemLv + 1, gemType, gemSubType))
        if not newGemId:
            return (False, cash, GMD.data.get(GMDD.data.EQUIP_GEM_LVUP_RULE_NO_TARGET_ERROR, {}).get('text', gameStrings.TEXT_RUNELVUPPROXY_403))
        needNum = SCD.data.get('EquipGemRuneLvUpCount', 4)
        if EGD.data.get(newGemId, {}).get('mixItemNeed'):
            needNum -= 1
        if len(runes) > needNum:
            return (False, cash, GMD.data.get(GMDD.data.EQUIP_GEM_LVUP_RULE_NUM_MORE, {}).get('text', gameStrings.TEXT_RUNELVUPPROXY_410) % needNum)
        if len(runes) < needNum:
            return (False, cash, GMD.data.get(GMDD.data.EQUIP_GEM_LVUP_RULE_NUM_LESS, {}).get('text', gameStrings.TEXT_RUNELVUPPROXY_413) % (needNum - len(runes)))
        if not self.updateCost():
            return (False, cash, GMD.data.get(GMDD.data.RUNE_LVUP_NOT_ENOUGH_ITEM_COST, {}).get('text', gameStrings.TEXT_RUNELVUPPROXY_334))
        return (True, cash, '')

    def _getRuneItemLv(self, rId):
        return RD.data.get(rId, {}).get('lv', 0)

    def _getRuneItemType(self, rId):
        return RD.data.get(rId, {}).get('runeType', 0)

    def _getRuneItemSubType(self, rId):
        rData = RD.data.get(rId)
        if not rData:
            return None
        else:
            runeType = rData['runeType']
            if runeType == const.RUNE_TYPE_BENYUAN:
                return rData.get('benyuanType', 0)
            return rData.get('runeEffectType', 0)

    def _getYinyangGemType(self, rId):
        return utils.getEquipGemData(rId).get('type', 0)

    def _getYinyangGemLv(self, rId):
        return utils.getEquipGemData(rId).get('lv', 0)

    def isItemDisabled(self, kind, page, pos, item):
        if kind == const.RES_KIND_INV:
            return self.mediator and (page, pos) in self.runeData.values()

    @ui.uiEvent(uiConst.WIDGET_RUNE_LVUP, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onRuneLvupItemClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        else:
            self.onAddItem(nPage, nItem)
            return

    def onAddItem(self, nPage, nItem, pageDes = 0, posDes = 0):
        if not self.mediator:
            return
        p = BigWorld.player()
        i = p.inv.getQuickVal(nPage, nItem)
        posList = range(5)
        first = posList[posDes:]
        next = posList[:posDes]
        first.extend(next)
        if i.isRune() and self.pageType == 'yinyangGem':
            self.mediator.Invoke('selectTab', GfxValue('runeLvUp'))
        elif i.type == Item.BASETYPE_EQUIP_GEM and self.pageType == 'runeLvUp':
            self.mediator.Invoke('selectTab', GfxValue('yinyangGem'))
        if self.pageType == 'runeLvUp':
            if i.isRune():
                runeCount = min(i.cwrap, max(1, const.RUNE_ITEM_MIX_NUM_NEED.get(RD.data.get(i.id, {}).get('runeType', 0), 0) - len(self.runeData)))
                for num in first:
                    if num not in self.runeData or not self.runeData[num]:
                        self.addRuneItem(nPage, nItem, pageDes, num)
                        runeCount = runeCount - 1
                        if runeCount == 0:
                            return

                p.showGameMsg(GMDD.data.RUNE_LVUP_ITEM_FULL, ())
            else:
                p.showGameMsg(GMDD.data.WRONG_TYPE_FOR_RUNE_LVUP, ())
        elif self.pageType == 'yinyangGem':
            if i.type == Item.BASETYPE_EQUIP_GEM:
                gemData = utils.getEquipGemData(i.id)
                gemLv, gemType, gemSubType = gemData.get('lv', 0), gemData.get('type', 0), gemData.get('subType', 0)
                newGemId = EGID.data.get((gemLv + 1, gemType, gemSubType))
                needNum = SCD.data.get('EquipGemRuneLvUpCount', 4)
                if EGD.data.get(newGemId, {}).get('mixItemNeed'):
                    needNum -= 1
                runeCount = min(i.cwrap, max(1, needNum - len(self.runeData)))
                for num in xrange(needNum):
                    if num not in self.runeData or not self.runeData[num]:
                        self.addRuneItem(nPage, nItem, pageDes, num)
                        runeCount = runeCount - 1
                        if runeCount == 0:
                            return

                p.showGameMsg(GMDD.data.RUNE_LVUP_GEM_FULL, (needNum,))
            else:
                p.showGameMsg(GMDD.data.WRONG_TYPE_FOR_GEM_LVUP, ())
