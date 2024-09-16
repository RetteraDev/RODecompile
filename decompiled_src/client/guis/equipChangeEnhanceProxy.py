#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangeEnhanceProxy.o
from gamestrings import gameStrings
import BigWorld
import gameconfigCommon
import gameglobal
import uiUtils
import const
import ui
import utils
import time
import gametypes
import commcalc
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis import events
from data import sys_config_data as SCD
from data import equip_enhance_refining_data as EERD
from cdata import equip_enhance_probability_data as EEPD
from cdata import game_msg_def_data as GMDD

def sort_unEquip(a, b):
    if a['quality'] > b['quality']:
        return -1
    if a['quality'] < b['quality']:
        return 1
    if a['sortIdx'] < b['sortIdx']:
        return -1
    if a['sortIdx'] > b['sortIdx']:
        return 1
    if a['score'] > b['score']:
        return -1
    if a['score'] < b['score']:
        return 1
    return 0


class EquipChangeEnhanceProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipChangeEnhanceProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getDetailInfo': self.onGetDetailInfo,
         'getMaterialInfo': self.onGetMaterialInfo,
         'changeMaterialNum': self.onChangeMaterialNum,
         'setDiKouFlag': self.onSetDiKouFlag,
         'removeItem': self.onRemoveItem,
         'confirm': self.onConfirm,
         'clickYunChuiBtn': self.onClickYunChuiBtn,
         'clickCoinBtn': self.onClickCoinBtn,
         'clickHistoryBtn': self.onClickHistoryBtn,
         'clickCalcBtn': self.onClickCalcBtn,
         'showHelp': self.onShowHelp,
         'checkLevelHasNewJuexingLock': self.onCheckLevelHasNewJuexingLock}
        self.panelMc = None
        self.widget = None
        self.selectedPos = None
        self.selectedLv = 0
        self.materialId = 0
        self.materialNum = 0
        self.oldRefineLvInfo = (0, 0)

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]
        self.refreshLeftList()
        self.widget = ASObject(self.panelMc)
        self.oldRefineLvInfo = self.uiAdapter.equipRefineSuitsProp.getRefineLv()
        ASUtils.setHitTestDisable(self.widget.refineSuitsEffect, True)
        self.widget.refineSuitsEffect.visible = False
        self.widget.refineSuitsBtn.visible = gameconfigCommon.enableEquipEnhanceSuit()
        self.widget.refineSuitsBtn.addEventListener(events.BUTTON_CLICK, self.handleRefineSuitsBtnClick, False, 0, True)
        self.refreshRefineSuitsBtn()

    def handleRefineSuitsBtnClick(self, *args):
        if self.uiAdapter.equipRefineSuitsProp.widget:
            self.uiAdapter.equipRefineSuitsProp.hide()
        else:
            self.uiAdapter.equipRefineSuitsProp.show()

    def refreshRefineSuitsBtn(self):
        if gameconfigCommon.enableEquipEnhanceSuit():
            currentLv, nextLv = self.uiAdapter.equipRefineSuitsProp.getRefineLv()
            showLv = currentLv if currentLv else nextLv
            self.widget.refineSuitsBtn.label = uiUtils.intToRoman(showLv[0])

    def onUnRegisterMc(self, *arg):
        self.widget = None
        self.panelMc = None
        self.selectedPos = None
        if self.uiAdapter.equipEnhanceHistory.mediator:
            self.uiAdapter.equipEnhanceHistory.hide()
        if self.uiAdapter.equipRefineSuitsProp.widget:
            self.uiAdapter.equipRefineSuitsProp.hide()

    def refreshLeftList(self, refreshKind = -1):
        if self.panelMc:
            p = BigWorld.player()
            info = {}
            refreshAll = refreshKind == -1
            equipList = []
            if refreshAll or refreshKind == const.RES_KIND_EQUIP:
                for i, item in enumerate(p.equipment):
                    if not item:
                        continue
                    if not self.canEnhance(item):
                        continue
                    itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
                    itemInfo['itemName'] = uiUtils.getItemColorNameByItem(item, True, -1, True)
                    itemInfo['sortIdx'] = uiUtils.getEquipSortIdxByPart(item)
                    itemInfo['pos'] = [const.RES_KIND_EQUIP, 0, i]
                    equipList.append(itemInfo)

                equipList.sort(key=lambda x: x['sortIdx'])
            info['equipList'] = equipList
            subEquipList = []
            if refreshAll or refreshKind == const.RES_KIND_SUB_EQUIP_BAG:
                for pos in gametypes.EQU_PART_SUB:
                    item = commcalc.getAlternativeEquip(p, pos)
                    if not item:
                        continue
                    if not self.canEnhance(item):
                        continue
                    itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
                    itemInfo['itemName'] = uiUtils.getItemColorNameByItem(item, True, -1, True)
                    itemInfo['sortIdx'] = uiUtils.getEquipSortIdxByPart(item)
                    itemInfo['pos'] = [const.RES_KIND_SUB_EQUIP_BAG, 0, pos]
                    subEquipList.append(itemInfo)

                subEquipList.sort(key=lambda x: x['sortIdx'])
            info['subEquipList'] = subEquipList
            unEquipList = []
            if refreshAll or refreshKind == const.RES_KIND_INV:
                for pg in p.inv.getPageTuple():
                    for ps in p.inv.getPosTuple(pg):
                        item = p.inv.getQuickVal(pg, ps)
                        if item == const.CONT_EMPTY_VAL:
                            continue
                        if not self.canEnhance(item):
                            continue
                        itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
                        itemInfo['itemName'] = uiUtils.getItemColorNameByItem(item, True, -1, True)
                        itemInfo['sortIdx'] = uiUtils.getEquipSortIdxByPart(item)
                        itemInfo['quality'] = getattr(item, 'quality', 0)
                        itemInfo['score'] = getattr(item, 'score', 0)
                        itemInfo['pos'] = [const.RES_KIND_INV, pg, ps]
                        unEquipList.append(itemInfo)

                unEquipList.sort(cmp=sort_unEquip)
            info['unEquipList'] = unEquipList
            info['refreshAll'] = refreshAll
            info['refreshKind'] = refreshKind
            self.panelMc.Invoke('refreshLeftList', uiUtils.dict2GfxDict(info, True))

    def canEnhance(self, item):
        if not item.isEquip():
            return False
        if item.isYaoPei():
            return False
        if item.getMaxEnhLv(BigWorld.player()) == 0:
            return False
        return True

    def getEnhanceItem(self):
        p = BigWorld.player()
        item = None
        if self.selectedPos and self.selectedPos[0] == const.RES_KIND_EQUIP:
            item = p.equipment.get(self.selectedPos[2])
        elif self.selectedPos and self.selectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
            item = commcalc.getAlternativeEquip(p, self.selectedPos[2])
        elif self.selectedPos and self.selectedPos[0] == const.RES_KIND_INV:
            item = p.inv.getQuickVal(self.selectedPos[1], self.selectedPos[2])
        return item

    def onGetDetailInfo(self, *arg):
        kind = int(arg[3][0].GetNumber())
        page = int(arg[3][1].GetNumber())
        pos = int(arg[3][2].GetNumber())
        if self.selectedPos and self.selectedPos[0] == kind and self.selectedPos[1] == page and self.selectedPos[2] == pos:
            return
        self.selectedPos = (kind, page, pos)
        self.refreshDetailInfo()

    def refreshDetailInfo(self, updateData = None):
        if self.panelMc:
            info = {}
            item = self.getEnhanceItem()
            if item:
                targetItemInfo = {}
                if self.selectedPos and self.selectedPos[0] in (const.RES_KIND_EQUIP, const.RES_KIND_SUB_EQUIP_BAG):
                    targetItemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
                elif self.selectedPos and self.selectedPos[0] == const.RES_KIND_INV:
                    targetItemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
                info['targetItemInfo'] = targetItemInfo
                totalNum, lostNum, enhProp = uiUtils.getEquipTotalRefine(item)
                totalRefine = gameStrings.TEXT_EQUIPCHANGEENHANCEPROXY_218 % uiUtils.toHtml('+%d%%' % totalNum, color='#E6BF73')
                if lostNum:
                    totalRefine += uiUtils.toHtml(' -%d%%' % lostNum, color='#FD1414')
                if enhProp == '':
                    enhProp = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                totalRefine += gameStrings.TEXT_EQUIPCHANGEENHANCEPROXY_223 % uiUtils.toHtml(enhProp, color='#E6BF73')
                info['totalRefine'] = totalRefine
                info['star'] = uiUtils.getEquipStar(item)
                info['starTips'] = gameStrings.TEXT_EQUIPCHANGEENHANCEPROXY_227
                info['historyBtnTips'] = gameStrings.TEXT_EQUIPCHANGEENHANCEPROXY_229
                info['calcBtnTips'] = gameStrings.TEXT_EQUIPCHANGEENHANCEPROXY_230
                info['refiningList'] = self.getRefiningList(item, updateData)
                info['updateDataFlag'] = updateData != None
                info['isEmpty'] = False
            else:
                info['isEmpty'] = True
            self.panelMc.Invoke('refreshDetailInfo', uiUtils.dict2GfxDict(info, True))

    def getRefiningList(self, item, updateData):
        maxEnhlv = item.getMaxEnhLv(BigWorld.player())
        enhanceRefining = getattr(item, 'enhanceRefining', {})
        totalRefining = uiUtils.getEquipTotalRefining(item)
        updateEnhLv = updateData.get('enhLv', 0) if updateData else 0
        firstOut = False
        refiningList = []
        for i in xrange(1, maxEnhlv + 1):
            eerd = EERD.data.get(i, {})
            enhEffects = eerd.get('enhEffects', [])
            colorDiv = int(eerd.get('colorDiv', 0) * 100)
            minRange = 0
            maxRange = 0
            for it in enhEffects:
                if it[0] < minRange or minRange == 0:
                    minRange = it[0]
                if it[0] > maxRange:
                    maxRange = it[0]

            minRange = int(minRange * 100)
            maxRange = int(maxRange * 100)
            if enhanceRefining.has_key(i):
                value = int(enhanceRefining[i] * 100)
                canClick = True
                if value <= colorDiv:
                    barColor = 'red'
                elif int(value) == maxRange:
                    barColor = 'green'
                else:
                    barColor = 'orange'
                refinePer = '%d%%' % int(value)
                currentValue = 100.0 * value / maxRange
            else:
                if firstOut == False:
                    firstOut = True
                    canClick = True
                else:
                    canClick = False
                barColor = 'red'
                refinePer = '?%'
                currentValue = 0
            refiningInfo = {}
            refiningInfo['lv'] = i
            refiningInfo['lvTxt'] = 'Lv.%d' % i
            refiningInfo['refinePer'] = refinePer
            refiningInfo['refineRange'] = '%d%%~%d%%' % (minRange, maxRange)
            refiningInfo['currentValue'] = currentValue
            if currentValue <= 0:
                refiningInfo['iconState'] = 'special' if uiUtils.checkEnhlvCanJuexing(i) else 'normal'
                refiningInfo['iconTips'] = self._getJuexingTip(i, totalRefining)
            else:
                refiningInfo['iconState'] = 'normal'
                refiningInfo['iconTips'] = ''
            refiningInfo['barColor'] = barColor
            refiningInfo['canClick'] = canClick
            if not canClick:
                refiningInfo['refinePer'] = uiUtils.toHtml(refiningInfo['refinePer'], '#666666')
                refiningInfo['refineRange'] = uiUtils.toHtml(refiningInfo['refineRange'], '#666666')
            if i == updateEnhLv:
                if updateData.has_key('realRefining'):
                    refiningInfo['isLvUp'] = False
                    enhRefining = updateData.get('enhRefining', 0)
                else:
                    refiningInfo['isLvUp'] = True
                    enhRefining = 0
                refiningInfo['oldCurrentValue'] = 100.0 * int(enhRefining * 100) / maxRange
                refiningInfo['needProcessing'] = True
            else:
                refiningInfo['needProcessing'] = False
            if gameglobal.rds.configData.get('enableEquipChangeJuexingStrength', False):
                refiningLimit = uiUtils.getEnhlvJuexingRefiningLimit(i)
                refiningInfo['showLock'] = uiUtils.isEnhlvRefiningShowLock(i) and not uiUtils.checkEquipRefiningLimitLv(totalRefining, refiningLimit)
            else:
                refiningInfo['showLock'] = False
            refiningList.append(refiningInfo)

        return refiningList

    def onGetMaterialInfo(self, *arg):
        self.selectedLv = int(arg[3][0].GetNumber())
        self.refreshMaterialInfo()

    def refreshMaterialInfo(self, *arg):
        if self.panelMc:
            info = {}
            self.materialId = 0
            strName = 'prob%d' % self.selectedLv
            for key, value in EEPD.data.iteritems():
                if value.get('type', 0) != 1:
                    continue
                if value.get(strName, 0) > 0:
                    self.materialId = key
                    break

            info['materialItemInfo'] = uiUtils.getGfxItemById(self.materialId)
            info['lvTitle'] = gameStrings.TEXT_EQUIPCHANGEENHANCEPROXY_344 % self.selectedLv
            info['maxNum'] = SCD.data.get('equipEnhanceMainMaterialNum', 0)
            self.panelMc.Invoke('refreshMaterialInfo', uiUtils.dict2GfxDict(info, True))

    def onChangeMaterialNum(self, *arg):
        self.materialNum = int(arg[3][0].GetNumber())
        self.refreshConsumeInfo()

    def onSetDiKouFlag(self, *arg):
        self.uiAdapter.equipChange.useDiKou = arg[3][0].GetBool()
        self.refreshConsumeInfo()

    def refreshConsumeInfo(self):
        if self.panelMc:
            p = BigWorld.player()
            info = {}
            own = p.inv.countItemInPages(self.materialId, enableParentCheck=True)
            info['materialNumStr'] = uiUtils.convertNumStr(own, self.materialNum, notEnoughColor='#E51717')
            info['materialNeedHelp'] = own < self.materialNum
            isMaterialNeedDikou = uiUtils.isItemHasDiKouInfo(self.materialId)
            if self.uiAdapter.equipChange.useDiKou and isMaterialNeedDikou:
                itemDict = {self.materialId: self.materialNum}
                btnEnabled = uiUtils.checkEquipMaterialDiKou(itemDict)
            else:
                itemDict = {}
                btnEnabled = own >= self.materialNum
            if isMaterialNeedDikou:
                info['useDiKou'] = self.uiAdapter.equipChange.useDiKou
                info['diKouInfo'] = uiUtils.getEquipMaterialDiKouInfo(itemDict)
                info['needShowDikou'] = True
            else:
                info['useDiKou'] = False
                info['diKouInfo'] = {}
                info['needShowDikou'] = False
            item = self.getEnhanceItem()
            prop = self.countProbability()
            eerd = EERD.data.get(self.selectedLv, {})
            enhEffects = eerd.get('enhEffects', [])
            minRange = 0
            maxRange = 0
            for it in enhEffects:
                if it[0] < minRange or minRange == 0:
                    if item and item._calcEquipRefining(prop, it[1]) != 0:
                        minRange = it[0]
                if it[0] > maxRange:
                    maxRange = it[0]

            minRange = int(minRange * 100)
            maxRange = int(maxRange * 100)
            info['refineRange'] = '%d%%~%d%%' % (minRange, maxRange)
            prop = int(prop * 100)
            if prop < 100:
                info['successRate'] = uiUtils.toHtml('%d%%' % prop, '#CC2929')
            else:
                info['successRate'] = uiUtils.toHtml('%d%%' % prop, '#7ACC29')
            needCash = eerd.get('cost', 0)
            info['cashStr'] = uiUtils.convertNumStr(p.cash, needCash, showOwnStr=False, needThousand=True)
            if p.cash < needCash:
                btnEnabled = False
            info['btnEnabled'] = btnEnabled
            self.panelMc.Invoke('refreshConsumeInfo', uiUtils.dict2GfxDict(info, True))

    def countProbability(self):
        strName = 'prob%d' % self.selectedLv
        prop = EEPD.data.get(self.materialId, {}).get(strName, 0)
        return prop * self.materialNum

    def onRemoveItem(self, *arg):
        self.selectedPos = None
        self.refreshDetailInfo()

    def onConfirm(self, *arg):
        p = BigWorld.player()
        item = self.getEnhanceItem()
        if not item:
            return
        if item.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        enhanceRefining = getattr(item, 'enhanceRefining', {})
        if enhanceRefining.has_key(self.selectedLv):
            currentEquipRefining = int(enhanceRefining[self.selectedLv] * 100)
            eerd = EERD.data.get(self.selectedLv, {})
            enhEffects = eerd.get('enhEffects', [])
            maxRange = 0
            for it in enhEffects:
                if it[0] > maxRange:
                    maxRange = it[0]

            maxRange = int(maxRange * 100)
            if maxRange <= currentEquipRefining:
                p.showGameMsg(GMDD.data.ENHANCE_MAX_CANNOT, ())
                return
            if gameglobal.rds.configData.get('enableEquipChangeJuexingStrength', False):
                refiningLimit = uiUtils.getEnhlvJuexingRefiningLimit(self.selectedLv)
                totalRefining = uiUtils.getEquipTotalRefining(item)
                if not uiUtils.checkEquipRefiningLimitLv(totalRefining, self.selectedLv):
                    p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.EQUIP_CHANGE_REFINIING_TIP_WARNING % refiningLimit)
                    return
        self.trueConfirmStep1()

    @ui.callFilter(1)
    def trueConfirmStep1(self):
        prop = self.countProbability()
        if prop < 1:
            propStr = '%d%%' % int(prop * 100)
            msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_PROP_FAILED_COFIRM, '%s') % propStr
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirmStep2)
        else:
            self.trueConfirmStep2()

    def trueConfirmStep2(self):
        item = self.getEnhanceItem()
        if not item:
            return
        self.trueConfirmStep3(item)

    @ui.checkEquipCanReturn(const.LAST_PARAMS, GMDD.data.RETURN_BACK_ENHANCE)
    @ui.looseGroupTradeConfirm(const.LAST_PARAMS, GMDD.data.RETURN_BACK_ENHANCE)
    def trueConfirmStep3(self, item):
        p = BigWorld.player()
        if self.uiAdapter.equipChange.useDiKou:
            itemDict = {self.materialId: self.materialNum}
        else:
            itemDict = {}
        _, yunChuiNeed, _, _ = utils.calcEquipMaterialDiKou(p, itemDict)
        if yunChuiNeed > 0 and not item.isForeverBind():
            msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_BIND_CONFIRM)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirm)
            return
        if p.inv.countItemBind(self.materialId, enableParentCheck=True):
            if not item.isForeverBind():
                msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_BIND_CONFIRM)
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirm)
            else:
                self.trueConfirm()
        else:
            self.trueConfirm()

    def trueConfirm(self):
        p = BigWorld.player()
        item = self.getEnhanceItem()
        if not item:
            return
        itemList = [self.materialId]
        itemNumList = [self.materialNum]
        realPos = self.selectedPos[2]
        if self.selectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
            realPos = gametypes.equipTosubEquipPartMap.get(self.selectedPos[2], -1)
        if realPos < 0:
            return
        if self.selectedLv > getattr(item, 'enhLv', 0):
            p.cell.enhanceItemInvNew(self.selectedPos[0], self.selectedPos[1], realPos, itemList, itemNumList)
        else:
            p.cell.reEnhanceEquipNew(self.selectedPos[0], self.selectedPos[1], realPos, self.selectedLv, itemList, itemNumList)

    def onClickYunChuiBtn(self, *arg):
        if gameglobal.rds.configData.get('enableBuyYunChuiCreditThroughCoin', False):
            self.uiAdapter.tianBiToYunChui.show()
        else:
            mall = self.uiAdapter.tianyuMall
            if mall.mallMediator:
                mall.hide()
            mall.show(keyWord=gameStrings.TEXT_INVENTORYPROXY_3299)

    def onClickCoinBtn(self, *arg):
        BigWorld.player().openRechargeFunc()

    def onClickHistoryBtn(self, *arg):
        if self.uiAdapter.equipEnhanceHistory.mediator:
            self.uiAdapter.equipEnhanceHistory.refreshHistoryInfo()
        else:
            self.uiAdapter.equipEnhanceHistory.toggle()

    def onClickCalcBtn(self, *arg):
        pass

    def onShowHelp(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        if gameglobal.rds.configData.get('enableNewItemSearch', False):
            self.uiAdapter.itemSourceInfor.openPanel()
        else:
            self.uiAdapter.help.showByItemId(itemId)

    def onCheckLevelHasNewJuexingLock(self, *args):
        lv = ASObject(args[3][0])
        if gameglobal.rds.configData.get('enableEquipChangeJuexingStrength', False):
            return uiUtils.hasJuexingNew(lv)
        return False

    def enhanceSuccess(self, updateData):
        p = BigWorld.player()
        uuid = updateData.get('uuid', '')
        resKind = updateData.get('resKind', 0)
        enhLv = updateData.get('enhLv', 0)
        enhRefining = int(updateData.get('enhRefining', 0) * 100)
        if updateData.has_key('realRefining'):
            realRefining = int(updateData.get('realRefining', 0) * 100)
            if realRefining <= enhRefining:
                content = gameStrings.TEXT_EQUIPCHANGEENHANCEPROXY_566 % (enhLv, enhRefining, realRefining)
                p.showGameMsg(GMDD.data.ENHANCE_SUCCESS_LOSE, ())
                updateData = None
            else:
                content = gameStrings.TEXT_EQUIPCHANGEENHANCEPROXY_570 % (enhLv, enhRefining, realRefining)
                p.showGameMsg(GMDD.data.ENHANCE_SUCCESS_BATTER, ())
                gameglobal.rds.sound.playSound(3988)
        else:
            content = gameStrings.TEXT_EQUIPCHANGEENHANCEPROXY_574 % (enhLv, enhRefining)
            p.showGameMsg(GMDD.data.ENHANCE_COMPLETE_LEVEL_INC, ())
            if uiUtils.checkEnhlvCanJuexing(enhLv):
                if uiUtils.hasJuexingNew(enhLv):
                    p.showGameMsg(GMDD.data.ENHANCE_COMPLETE_NEW_JUEXING_NEW, ())
                else:
                    p.showGameMsg(GMDD.data.ENHANCE_COMPLETE_NEW_JUEXING, ())
            gameglobal.rds.sound.playSound(3988)
        self.refreshLeftList(resKind)
        item = self.getEnhanceItem()
        if item and updateData and item.uuid == updateData.get('uuid', ''):
            self.refreshDetailInfo(updateData)
        else:
            self.refreshConsumeInfo()
        localTime = time.localtime(utils.getNow())
        p.addEnhanceHistory(uuid, localTime, content)
        self.refreshEnhanceEffect()
        self.refreshRefineSuitsBtn()

    def refreshEnhanceEffect(self):
        newEnhanceLvInfo = self.uiAdapter.equipRefineSuitsProp.getRefineLv()
        if newEnhanceLvInfo[0] == self.oldRefineLvInfo[1]:
            self.widget.refineSuitsEffect.visible = True
            self.widget.refineSuitsEffect.gotoAndPlay(1)
        self.oldRefineLvInfo = newEnhanceLvInfo

    def enhanceFaild(self, updateData):
        p = BigWorld.player()
        self.refreshConsumeInfo()
        uuid = updateData.get('uuid', '')
        enhLv = updateData.get('enhLv', 0)
        content = gameStrings.TEXT_EQUIPCHANGEENHANCEPROXY_609 % enhLv
        gameglobal.rds.sound.playSound(3989)
        localTime = time.localtime(utils.getNow())
        p.addEnhanceHistory(uuid, localTime, content)

    def _getJuexingTip(self, jxlevel, totalRefining):
        retStr = ''
        if gameglobal.rds.configData.get('enableEquipChangeJuexingStrength', False):
            if uiUtils.checkEnhlvCanJuexing(jxlevel):
                if uiUtils.hasJuexingNew(jxlevel):
                    retStr += gameStrings.EQUIP_CHANGE_REFINIING_TIP_3
                else:
                    retStr += gameStrings.EQUIP_CHANGE_REFINIING_TIP_1
            needRefining = uiUtils.getEnhlvJuexingRefiningLimit(jxlevel)
            if not uiUtils.checkEquipRefiningLimitLv(totalRefining, needRefining):
                retStr += '' if not retStr else ', '
                retStr += gameStrings.EQUIP_CHANGE_REFINIING_TIP_2 % (needRefining, totalRefining)
        elif uiUtils.checkEnhlvCanJuexing(jxlevel):
            retStr = gameStrings.EQUIP_CHANGE_REFINIING_TIP_1
        else:
            retStr = ''
        return retStr
