#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipEnhanceProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import copy
import gameglobal
import const
import utils
from ui import gbk2unicode
from guis import uiConst
from guis import uiUtils
from guis import ui
from uiProxy import SlotDataProxy
from item import Item
from data import sys_config_data as SCD
from data import equip_enhance_refining_data as EERD
from cdata import equip_enhance_probability_data as EEPD
from cdata import game_msg_def_data as GMDD
from cdata import equip_transform_dikou_data as ETDD

class EquipEnhanceProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipEnhanceProxy, self).__init__(uiAdapter)
        self.modelMap = {'checkEquipDiKou': self.onCheckEquipDiKou,
         'refreshHistoryBtn': self.onRefreshHistory,
         'toggleHistory': self.onToggleHistory,
         'closeAllPanel': self.onCloseAllPanel,
         'refreshRefine': self.onRefreshRefine,
         'toggleRefine': self.onToggleRefine,
         'confirmRefine': self.onConfirmRefine,
         'refreshContent': self.onRefreshContent,
         'changeUseNum': self.onChangeUseNum,
         'clickTianbiBtn': self.onClickTianbiBtn,
         'clickYunchuiBtn': self.onClickYunchuiBtn}
        self.mediator = None
        self.type = 'equipEnhance'
        self.bindType = 'equipEnhance'
        self.funcType = uiConst.EQUIP_FUNC_ENHANCE
        self.posMap = {}
        self.npcId = 0
        self.enhanceLv = 0
        self.slotCount = {}
        self.slotUseCount = {}
        self.typeNum = {}
        self.enhanceBeforeItem = None
        self.enhanceBeforeItemPos = [const.CONT_NO_PAGE, const.CONT_NO_POS]
        self.enhanceTargetLv = 0
        self.resultTxt = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_ENHANCE, self.clearAllWidget)

    def onCheckEquipDiKou(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableEquipDiKou', False))

    def onRefreshHistory(self, *args):
        openHistory = False
        item = self.getEnhanceItem()
        if item:
            history = BigWorld.player().getEnhanceHistory(item.uuid)
            if len(history) > 0:
                openHistory = True
        if self.mediator != None:
            self.mediator.Invoke('setHistoryEnable', GfxValue(openHistory))

    def onRefreshRefine(self, *args):
        hasRefine = False
        if self.posMap.has_key((0, 0)):
            page, pos = self.posMap[0, 0]
            item = BigWorld.player().inv.getQuickVal(page, pos)
            if item:
                if getattr(item, 'enhLv', 0) > 0:
                    hasRefine = True
        if self.mediator != None:
            self.mediator.Invoke('setRefineEnable', GfxValue(hasRefine))

    def onRefreshContent(self, *args):
        self.refreshHint()

    def onToggleHistory(self, *args):
        gameglobal.rds.ui.equipEnhanceHistory.toggle()

    def onToggleRefine(self, *args):
        pass

    def getMaxRefineLv(self):
        if self.posMap.get((0, 0)):
            key = self._getKey(0, 0)
            item = self.bindingData[key]
            lv = getattr(item, 'enhLv', 0) + 1
            maxLv = item.getMaxEnhLv(BigWorld.player())
            ret = min(lv, maxLv)
            equipRefining = getattr(item, 'enhanceRefining', {})
            nowMaxLv = 0
            for key in equipRefining:
                nowMaxLv = max(key, nowMaxLv)

            if nowMaxLv > maxLv:
                return nowMaxLv
            return ret
        else:
            return 0

    @ui.callFilter(1)
    def onConfirmRefine(self, *args):
        prop = self.countProbability()
        if prop < 1:
            txt = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_PROP_FAILED_COFIRM)
            prop = int(prop * 100)
            propText = '%d%%' % prop
            txt = txt % propText
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, self.trueConfirmStep1)
        else:
            self.trueConfirmStep1()

    def trueConfirmStep1(self):
        item = self.getEnhanceItem()
        self.trueConfirStepResume(item)

    @ui.checkEquipCanReturn(const.LAST_PARAMS, GMDD.data.RETURN_BACK_ENHANCE)
    @ui.looseGroupTradeConfirm(const.LAST_PARAMS, GMDD.data.RETURN_BACK_ENHANCE)
    def trueConfirStepResume(self, item):
        if gameglobal.rds.configData.get('enableEquipDiKou', False):
            diKouItem = self.getPosItem(0, 1)
            if diKouItem:
                itemId = diKouItem.getParentId()
                itemNum = self.slotUseCount.get(1, 1)
                itemDict = {itemId: itemNum}
                _, yunchuiNeed, _, _ = utils.calcEquipMaterialDiKou(BigWorld.player(), itemDict)
                if yunchuiNeed > 0 and not item.isForeverBind():
                    msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_BIND_CONFIRM)
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.trueConfirm)
                    return
        if self.isMaterialBinded():
            if not item.isForeverBind():
                msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_BIND_CONFIRM)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.trueConfirm)
            else:
                self.trueConfirm()
        else:
            self.trueConfirm()

    def isMaterialBinded(self):
        for i in xrange(1, 5):
            if self.posMap.has_key((0, i)):
                key = self._getKey(0, i)
                item = self.bindingData[key]
                ret = BigWorld.player().inv.countItemBind(item.getParentId(), enableParentCheck=True)
                if ret:
                    return ret

        return False

    def trueConfirm(self):
        p = BigWorld.player()
        if self.posMap.has_key((0, 0)):
            itemPage, itemPos = self.posMap[0, 0]
            self.enhanceBeforeItem = copy.deepcopy(p.inv.getQuickVal(itemPage, itemPos))
            self.enhanceBeforeItemPos = [itemPage, itemPos]
            self.enhanceTargetLv = self.getEnhanceLv()
            itemList = []
            itemNumList = []
            for i in xrange(1, 5):
                if self.posMap.has_key((0, i)):
                    key = self._getKey(0, i)
                    item = self.bindingData[key]
                    itemList.append(item.getParentId())
                    itemNumList.append(self.slotUseCount.get(i, 1))

            npcEnt = BigWorld.entities.get(self.npcId)
            item = BigWorld.player().inv.getQuickVal(itemPage, itemPos)
            equipRefining = getattr(item, 'enhanceRefining', {})
            if equipRefining.has_key(self.getEnhanceLv()):
                currentEquipRefining = int(equipRefining[self.getEnhanceLv()] * 100)
                data3 = EERD.data.get(self.getEnhanceLv(), {})
                max = 0
                progressList = data3.get('enhEffects', 0)
                for it in progressList:
                    if it[0] > max:
                        max = it[0]

                max = int(max * 100)
                if max == currentEquipRefining:
                    BigWorld.player().showGameMsg(GMDD.data.ENHANCE_MAX_CANNOT, ())
                    return
            if self.getEnhanceLv() > getattr(item, 'enhLv', 0):
                npcEnt and npcEnt.cell.enhanceItemInv(itemPage, itemPos, itemList, itemNumList)
            else:
                BigWorld.player().cell.reEnhanceEquip(itemPage, itemPos, self.getEnhanceLv(), itemList, itemNumList)

    def onCloseAllPanel(self, *arg):
        self.clearAllWidget()

    def clearAllWidget(self):
        self.clearWidget()
        gameglobal.rds.ui.equipEnhanceHistory.clearWidget()
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_ENHANCE:
            self.mediator = mediator
        BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)

    def clearWidget(self):
        self.posMap = {}
        self.mediator = None
        self.enhanceLv = 0
        self.typeNum = {}
        self.resultTxt = ''
        self.slotUseCount = {}
        self.bindingData = {}
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_ENHANCE)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def show(self, npcId):
        self.npcId = npcId
        self.enhanceLv = 0
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_ENHANCE)

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[12:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'equipEnhance%d.slot%d' % (bar, slot)

    def setItem(self, srcBar, srcSlot, destBar, destSlot, it, needRefreshUseNum = True):
        key = self._getKey(destBar, destSlot)
        if not self.binding.has_key(key):
            return
        else:
            self.resultTxt = None
            if destSlot != 0:
                if not self.posMap.has_key((0, 0)):
                    return
                item = BigWorld.player().inv.getQuickVal(srcBar, srcSlot)
                if item.hasLatch():
                    BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                    return
                if not self.checkItemCanAdd(item, 1):
                    return
                data = EEPD.data.get(item.getParentId(), {})
                type = data.get('type', 1)
                for k, v in self.bindingData.items():
                    if type == 1:
                        if v:
                            if EEPD.data.get(v.getParentId(), {}).get('type', 0) == 1:
                                bar, slot = self.getSlotID(k)
                                self.removeItem(bar, slot)
                                continue
                    if v and v.getParentId() == it.getParentId():
                        bar, slot = self.getSlotID(k)
                        self.removeItem(bar, slot)

            self.bindingData[key] = it
            if destSlot != 0:
                result = BigWorld.player().inv.countItemChild(it.getParentId())
                if result[0] > 0:
                    toolTipItem = Item(result[1][0])
                    self.bindingData[key] = toolTipItem
                    self.binding[key][0].Invoke('refreshTip')
            iconPath = uiUtils.getItemIconFile64(it.id)
            if destSlot == 0:
                count = it.cwrap
                enhanceLv = getattr(it, 'enhLv', 0)
                self.setNowRefineLv(enhanceLv + 1)
            else:
                count = BigWorld.player().inv.countItemInPages(it.getParentId(), enableParentCheck=True)
                type = EEPD.data.get(it.getParentId(), {}).get('type', 1)
                if type == 1:
                    maxNum = SCD.data.get('equipEnhanceMainMaterialNum', 0)
                else:
                    maxNum = SCD.data.get('equipEnhanceAssistMaterialNum', 0)
                count = maxNum
            self.slotCount[destSlot] = count
            if needRefreshUseNum:
                self.slotUseCount[destSlot] = 1
            if self.mediator:
                self.mediator.Invoke('showItemType', (GfxValue(destSlot), GfxValue(False)))
            if destSlot != 0:
                if self.mediator != None:
                    self.mediator.Invoke('setControlNum', (GfxValue(destSlot - 1), GfxValue(count), GfxValue(1)))
            color = uiUtils.getItemColorByItem(it)
            data = {'iconPath': iconPath,
             'color': color}
            self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
            self.posMap[destBar, destSlot] = (srcBar, srcSlot)
            self.refreshContent()
            return

    def checkItemCanAdd(self, item, num):
        lv = self.getEnhanceLv()
        if lv == 0:
            return False
        trueLv = max(lv, 1)
        prop = self.getItemProp(item, trueLv)
        if prop == 0:
            return False
        type = EEPD.data.get(item.getParentId(), {}).get('type', 1)
        preNum = self.typeNum.get(type, 0) + num
        if type == 1:
            maxNum = SCD.data.get('equipEnhanceMainMaterialNum', 0)
            if preNum > maxNum:
                return False
            else:
                return True
        else:
            maxNum = SCD.data.get('equipEnhanceAssistMaterialNum', 0)
            if preNum > maxNum:
                return False
            return True
        return False

    def removeItem(self, bar, slot):
        key = self._getKey(bar, slot)
        if not self.binding.has_key(key):
            return
        else:
            self.resultTxt = None
            self.slotCount[slot] = 0
            self.slotUseCount[slot] = 0
            self.bindingData[key] = None
            data = GfxValue(0)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            if self.posMap.has_key((bar, slot)):
                self.posMap.pop((bar, slot))
            if slot == 0:
                self.setNowRefineLv(0)
                if self.mediator:
                    self.mediator.Invoke('clearAllMaterialSlot', ())
                for i in xrange(1, 4):
                    self.removeItem(0, i)

            elif self.mediator:
                self.mediator.Invoke('setControlNum', (GfxValue(slot - 1), GfxValue(-1), GfxValue(1)))
                self.mediator.Invoke('setIconNum', (GfxValue(slot), GfxValue('')))
            if self.mediator:
                self.mediator.Invoke('showItemType', (GfxValue(slot), GfxValue(True)))
            self.refreshContent()
            return

    def onChangeUseNum(self, *arg):
        self.resultTxt = None
        index = int(arg[3][0].GetNumber()) + 1
        value = int(arg[3][1].GetNumber())
        self.slotUseCount[index] = value
        self.refreshContent()

    def getPosItem(self, page, pos):
        key = self._getKey(page, pos)
        item = self.bindingData.get(key, None)
        return item

    def moveItem(self, nPageSrc, nItemSrc, nPageDes, nItemDes):
        p = BigWorld.player()
        srcPage, srcPos = self.posMap.get((nPageSrc, nItemSrc), [-1, -1])
        dstPage, dstPos = self.posMap.get((nPageDes, nItemDes), [-1, -1])
        srcIt = p.inv.getQuickVal(srcPage, srcPos)
        dstIt = p.inv.getQuickVal(dstPage, dstPos)
        self.setItem(srcPage, srcPos, nPageDes, nItemDes, srcIt)
        if dstIt:
            self.setItem(dstPage, dstPos, nPageSrc, nItemSrc, dstIt)
        else:
            self.removeItem(nPageSrc, nItemSrc)
        self.posMap[nPageSrc, nItemSrc] = [dstPage, dstPos]
        self.posMap[nPageDes, nItemDes] = [srcPage, srcPos]
        self.refreshContent()

    def removeUnUsedItem(self):
        find = False
        for i in xrange(1, 5):
            if self.posMap.has_key((0, i)):
                if int(self.countProbability(0, i) * 100) == 0:
                    self.removeItem(0, i)
                    find = True

        if find:
            BigWorld.player().showGameMsg(GMDD.data.NEED_CHANGE_MATERIAL, ())

    def playFailAnimation(self, type):
        if not self.mediator:
            return
        self.mediator.Invoke('playAnimation', GfxValue(type))

    def refreshContent(self):
        if not self.mediator:
            return
        else:
            self.removeUnUsedItem()
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
            self.onRefreshRefine(None)
            self.onRefreshHistory(None)
            self.refreshType()
            self.refreshHint()
            self.refreshButton()
            self.refreshItemNumAndLv()
            self.refreshEquipEnhInfo()
            self.refreshDiKouInfo()
            return

    def refreshItemNumAndLv(self):
        if not self.mediator:
            return
        for k, v in self.bindingData.items():
            if v:
                bar, slot = self.getSlotID(k)
                if slot == 0:
                    count = v.cwrap
                    self.binding[k][0].Invoke('refreshTip')
                else:
                    count = BigWorld.player().inv.countItemInPages(v.getParentId(), enableParentCheck=True)
                    if count >= self.slotUseCount.get(slot, 1):
                        descStr = '%d/%d' % (count, self.slotUseCount.get(slot, 1))
                    else:
                        descStr = "<font color = \'#FB0000\'>%d</font>/%d" % (count, self.slotUseCount.get(slot, 1))
                    change = False
                    result = BigWorld.player().inv.countItemChild(v.getParentId())
                    if result[0] > 0:
                        toolTipItem = Item(result[1][0])
                    else:
                        toolTipItem = Item(v.getParentId())
                    if self.bindingData[k] != toolTipItem:
                        self.bindingData[k] = toolTipItem
                        change = True
                    if change:
                        self.binding[k][0].Invoke('refreshTip')
                    self.mediator.Invoke('setIconNum', (GfxValue(slot), GfxValue(gbk2unicode(descStr))))
                self.slotCount[slot] = count

    def refreshEquipEnhInfo(self):
        if self.mediator:
            info = {}
            item = self.getEnhanceItem()
            if item:
                info['enhLv'] = gameStrings.TEXT_EQUIPENHANCEPROXY_467 % getattr(item, 'enhLv', 0)
                if hasattr(item, 'enhanceRefining'):
                    equipRefining = item.enhanceRefining
                    maxLv = item.getMaxEnhLv(BigWorld.player())
                    totalNum = 0
                    lostNum = 0
                    for key in equipRefining:
                        totalNum += round(equipRefining[key] * 100)
                        if key > maxLv:
                            lostNum += round(equipRefining[key] * 100)

                    if lostNum:
                        totalRefine = gameStrings.TEXT_EQUIPENHANCEPROXY_479 % (totalNum, lostNum)
                    else:
                        totalRefine = gameStrings.TEXT_EQUIPENHANCEPROXY_481 % totalNum
                else:
                    totalRefine = gameStrings.TEXT_EQUIPENHANCEPROXY_483
                info['totalRefine'] = totalRefine
                info['star'] = uiUtils.getEquipStar(item)
                info['visible'] = True
            else:
                info['visible'] = False
            self.mediator.Invoke('refreshEquipEnhInfo', uiUtils.dict2GfxDict(info, True))

    def refreshDiKouInfo(self):
        if not gameglobal.rds.configData.get('enableEquipDiKou', False):
            return
        if self.mediator:
            info = {}
            item = self.getPosItem(0, 1)
            if item:
                p = BigWorld.player()
                itemId = item.getParentId()
                itemNum = self.slotUseCount.get(1, 1)
                itemDict = {itemId: itemNum}
                _, yunchuiNeed, tianbiNeed, _ = utils.calcEquipMaterialDiKou(p, itemDict)
                yunchuiOwn = p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
                if yunchuiNeed > yunchuiOwn:
                    info['yunchui'] = '%s/%s' % (uiUtils.toHtml(format(yunchuiOwn, ','), '#FB0000'), format(yunchuiNeed, ','))
                    info['yunchuiEnabled'] = True
                else:
                    info['yunchui'] = '%s/%s' % (format(yunchuiOwn, ','), format(yunchuiNeed, ','))
                    info['yunchuiEnabled'] = False
                if ETDD.data.get(itemId, {}).get('coin', 0) or tianbiNeed > 0:
                    if hasattr(p, 'unbindCoin') and hasattr(p, 'bindCoin') and hasattr(p, 'freeCoin'):
                        tianbiOwn = p.unbindCoin + p.bindCoin + p.freeCoin
                    else:
                        tianbiOwn = 0
                    if tianbiNeed > tianbiOwn:
                        info['tianbi'] = '%s/%s' % (uiUtils.toHtml(format(tianbiOwn, ','), '#FB0000'), format(tianbiNeed, ','))
                        info['tianbiEnabled'] = True
                    else:
                        info['tianbi'] = '%s/%s' % (format(tianbiOwn, ','), format(tianbiNeed, ','))
                        info['tianbiEnabled'] = False
                    info['tianbiVisible'] = True
                else:
                    info['tianbiVisible'] = False
                info['visible'] = True
            else:
                info['visible'] = False
            self.mediator.Invoke('refreshDiKouInfo', uiUtils.dict2GfxDict(info, True))

    def setNowRefineLv(self, lv):
        if self.mediator:
            key = self._getKey(0, 0)
            if self.bindingData.has_key(key):
                it = self.bindingData[key]
                if it and it.isEquip():
                    maxLv = it.getMaxEnhLv(BigWorld.player())
                    self.enhanceLv = min(lv, maxLv)
                    descStr = gameStrings.TEXT_EQUIPENHANCEPROXY_547 % self.enhanceLv
                else:
                    descStr = ''
                    self.enhanceLv = 0
            else:
                descStr = ''
                self.enhanceLv = 0
            materialCount = EERD.data.get(self.enhanceLv, {}).get('materialCount', 0)
            self.mediator.Invoke('showAllMaterialSlot', GfxValue(materialCount))
            self.mediator.Invoke('setEnhanceLv', GfxValue(gbk2unicode(descStr)))

    def refreshType(self):
        self.typeNum = {}
        for i in xrange(1, 5):
            if self.posMap.has_key((0, i)):
                page, pos = self.posMap[0, i]
                key = self._getKey(0, i)
                item = self.bindingData[key]
                data = EEPD.data.get(item.getParentId(), {})
                type = data.get('type', 1)
                if self.typeNum.has_key(type):
                    self.typeNum[type] += self.slotUseCount.get(i, 1)
                else:
                    self.typeNum[type] = self.slotUseCount.get(i, 1)

    def refreshButton(self):
        if not self.mediator:
            return
        self.mediator.Invoke('resetPreButton')
        for i in xrange(1, 5):
            if self.posMap.has_key((0, i)):
                key = self._getKey(0, i)
                item = self.bindingData[key]
                if not self.checkItemCanAdd(item, 1):
                    self.mediator.Invoke('enableNextButton', GfxValue(False))
                else:
                    self.mediator.Invoke('enableNextButton', GfxValue(True))

        if not self.posMap.has_key((0, 0)):
            pass
        elif gameglobal.rds.configData.get('enableEquipDiKou', False):
            item = self.getPosItem(0, 1)
            if item:
                itemId = item.getParentId()
                itemNum = self.slotUseCount.get(1, 1)
                itemDict = {itemId: itemNum}
                if uiUtils.checkEquipMaterialDiKou(itemDict):
                    self.mediator.Invoke('setConfirmEanble', GfxValue(True))
                    return
        elif self.posMap.has_key((0, 1)) or self.posMap.has_key((0, 2)) or self.posMap.has_key((0, 3)) or self.posMap.has_key((0, 4)):
            prop = int(self.countProbability() * 100)
            canConfirm = True
            for k, v in self.bindingData.items():
                if v:
                    bar, slot = self.getSlotID(k)
                    if slot != 0:
                        count = BigWorld.player().inv.countItemInPages(v.getParentId(), enableParentCheck=True)
                        if count < self.slotUseCount.get(slot, 1):
                            canConfirm = False

            mainMaterialNum = self.typeNum.get(1, 0)
            if prop > 0 and canConfirm and mainMaterialNum > 0:
                self.mediator.Invoke('setConfirmEanble', GfxValue(True))
                return
        self.mediator.Invoke('setConfirmEanble', GfxValue(False))

    def refreshHint(self):
        title = ''
        content = ''
        if self.resultTxt:
            title = "<font color = \'#FB0000\'>%s</font>" % self.resultTxt
        else:
            title = ''
        if not self.getEnhanceItem():
            content = gameStrings.TEXT_EQUIPENHANCEPROXY_626
        else:
            mainMaterialNum = self.typeNum.get(1, 0)
            if mainMaterialNum == 0:
                lv = self.getEnhanceLv()
                strName = 'prob%d' % lv
                metName = ''
                for key in EEPD.data:
                    if EEPD.data[key]['type'] == 1:
                        if EEPD.data[key].get(strName, 0) > 0:
                            metName = uiUtils.getItemColorName(key)
                            break

                content = gameStrings.TEXT_EQUIPENHANCEPROXY_639 % metName
            elif self.posMap.has_key((0, 1)) or self.posMap.has_key((0, 2)) or self.posMap.has_key((0, 3)) or self.posMap.has_key((0, 4)):
                prop = int(self.countProbability() * 100)
                data = EERD.data.get(self.getEnhanceLv(), {})
                cost = data.get('cost', 0)
                min = 0
                max = 0
                progressList = data.get('enhEffects', 0)
                for i in progressList:
                    if i[0] > max:
                        max = i[0]
                    if i[0] < min or min == 0:
                        if self.getEnhanceItem()._calcEquipRefining(self.countProbabilityForLv(self.getEnhanceLv()), i[1]) != 0:
                            min = i[0]

                min = int(min * 100)
                max = int(max * 100)
                color = '#79C725'
                if prop < 100:
                    color = '#FB0000'
                content = gameStrings.TEXT_EQUIPENHANCEPROXY_659 % (color,
                 prop,
                 min,
                 max,
                 cost)
            else:
                content = gameStrings.TEXT_EQUIPENHANCEPROXY_662
        if self.mediator != None:
            self.mediator.Invoke('setContent', (GfxValue(gbk2unicode(title)), GfxValue(gbk2unicode(content))))

    def countProbabilityForLv(self, lv):
        if not self.posMap.has_key((0, 0)):
            return 0
        count = 0
        for i in xrange(1, 4):
            if self.posMap.has_key((0, i)):
                key = self._getKey(0, i)
                item = self.bindingData[key]
                if item:
                    prop = self.getItemProp(item, lv)
                else:
                    prop = 0
                prop = self.slotUseCount.get(i, 1) * prop
                count += prop

        return count

    def countProbability(self, page = -1, pos = -1):
        if not self.posMap.has_key((0, 0)):
            return 0
        elif page == -1 and pos == -1:
            count = 0
            for i in xrange(1, 4):
                if self.posMap.has_key((0, i)):
                    key = self._getKey(0, i)
                    item = self.bindingData[key]
                    if item:
                        prop = self.getItemProp(item, self.getEnhanceLv())
                    else:
                        prop = 0
                    prop = self.slotUseCount.get(i, 1) * prop
                    count += prop

            return count
        key = self._getKey(page, pos)
        item = self.bindingData[key]
        if item:
            prop = self.getItemProp(item, self.getEnhanceLv())
            return prop
        else:
            return 0

    def getEnhanceLv(self):
        return self.enhanceLv

    def getItemProp(self, item, lv):
        data = EEPD.data.get(item.getParentId(), {})
        if not data:
            return 0
        name = 'prob%d' % lv
        prop = data.get(name, 0)
        return prop

    def findEmptyPos(self):
        pos = 1
        for i in xrange(1, 4):
            key = (self.funcType, i)
            if not self.posMap.has_key(key):
                return i

        return pos

    def isItemInView(self, page, pos):
        for key in self.posMap:
            if self.posMap[key] == (page, pos):
                return True

        return False

    def updateItemAfterEnhance(self, equipIt, needAddLv = True):
        key = self._getKey(0, 0)
        self.bindingData[key] = equipIt
        enhanceLv = getattr(equipIt, 'enhLv', 0)
        if needAddLv:
            self.setNowRefineLv(enhanceLv + 1)
        for i in xrange(1, 5):
            item = self.getPosItem(0, i)
            if item:
                key = self._getKey(0, i)
                page1, pos1 = BigWorld.player().inv.findItemInPages(item.getParentId(), enableParentCheck=True)
                if page1 != const.CONT_NO_PAGE and pos1 != const.CONT_NO_POS:
                    self.bindingData[key] = BigWorld.player().inv.getQuickVal(page1, pos1)
                else:
                    self.bindingData[key] = Item(item.id)
                self.posMap[0, i] = (page1, pos1)

        self.refreshContent()

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        if self.bindingData.has_key(key):
            return gameglobal.rds.ui.inventory.GfxToolTip(self.bindingData[key])
        else:
            return GfxValue('')

    def onOpenInventory(self, *arg):
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()

    def onRemoveItem(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        if bar == uiConst.EQUIP_FUNC_ENHANCE or slot in (0, 1):
            self.removeItem(bar, slot)

    def getEnhanceItem(self):
        if self.posMap.has_key((0, 0)):
            page, pos = self.posMap[0, 0]
            return BigWorld.player().inv.getQuickVal(page, pos)
        else:
            return None

    def onNotifySlotUse(self, *args):
        nPage, nItem = self.getSlotID(args[3][0].GetString())
        self.removeItem(nPage, nItem)

    def setResultText(self, targetLv, type, fromEnhanceProgress, toEnhanceProgress):
        content = ''
        data = EERD.data.get(targetLv, {})
        progressList = data.get('enhEffects', 0)
        colorDiv = int(data.get('colorDiv', 0) * 100)
        maxValue = 0
        for it in progressList:
            if it[0] > maxValue:
                maxValue = it[0]

        maxValue = int(maxValue * 100)
        if fromEnhanceProgress <= colorDiv:
            fromColor = '#FB0000'
        elif int(fromEnhanceProgress) == maxValue:
            fromColor = '#79C725'
        else:
            fromColor = '#e5c317'
        if toEnhanceProgress <= colorDiv:
            toColor = '#FB0000'
        elif int(toEnhanceProgress) == maxValue:
            toColor = '#79C725'
        else:
            toColor = '#e5c317'
        if type == 0:
            content = gameStrings.TEXT_EQUIPENHANCEPROXY_821 % (targetLv, toColor, toEnhanceProgress)
        elif type == 1:
            content = gameStrings.TEXT_EQUIPENHANCEPROXY_824 % (targetLv,
             fromColor,
             fromEnhanceProgress,
             toColor,
             toEnhanceProgress)
        elif type == 2:
            content = gameStrings.TEXT_EQUIPENHANCEPROXY_828 % (targetLv,
             fromColor,
             fromEnhanceProgress,
             toColor,
             toEnhanceProgress)
        elif type == 3:
            content = gameStrings.TEXT_EQUIPENHANCEPROXY_832 % targetLv
        self.resultTxt = content
        self.refreshContent()

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            if item:
                if item.isYaoPei():
                    return True
                if not item.isEquip() and not (hasattr(item, 'type') and item.type == Item.BASETYPE_ENHANCE):
                    return True
                if item.isEquip():
                    if item.getMaxEnhLv(BigWorld.player()) == 0:
                        return True
                elif hasattr(item, 'type') and item.type == Item.BASETYPE_ENHANCE:
                    if not gameglobal.rds.ui.equipEnhance.checkItemCanAdd(item, 1):
                        return True
                for nowPage, nowPos in self.posMap:
                    if (nowPage, nowPos) == (0, 0):
                        page1, pos1 = self.posMap[nowPage, nowPos]
                        if page == page1 and pos1 == pos:
                            return True
                    else:
                        itemMaterial = gameglobal.rds.ui.equipEnhance.getPosItem(nowPage, nowPos)
                        if itemMaterial.getParentId() == item.getParentId():
                            return True

        return False

    def onClickTianbiBtn(self, *args):
        BigWorld.player().openRechargeFunc()

    def onClickYunchuiBtn(self, *args):
        mall = gameglobal.rds.ui.tianyuMall
        if mall.mallMediator:
            mall.hide()
        mall.show(keyWord=gameStrings.TEXT_INVENTORYPROXY_3299)
