#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yaoPeiTransferProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import events
import ui
import formula
import const
import utils
from uiProxy import SlotDataProxy
from callbackHelper import Functor
from data import sys_config_data as SCD
from cdata import yaopei_lv_data as YLD
from cdata import yaopei_lv_exp_data as YLED
from cdata import game_msg_def_data as GMDD
from data import item_data as ID
from cdata import pursue_yaopei_data as PYD
TRANSFER_READY = 1
TRANSFER_WAITING = 2
TRANSFER_FINISH = TRANSFER_READY

class YaoPeiTransferProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(YaoPeiTransferProxy, self).__init__(uiAdapter)
        self.bindType = 'yaoPeiTransfer'
        self.type = 'yaoPeiTransfer'
        self.modelMap = {'confirm': self.onConfirm,
         'removeItem': self.onRemoveItem}
        self.mediator = None
        self.posMap = {}
        self.transferState = TRANSFER_READY
        self.oldLv = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_YAOPEI_TRANSFER, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_YAOPEI_TRANSFER:
            self.mediator = mediator
            self.refreshInfo()
        BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YAOPEI_TRANSFER)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def reset(self):
        self.transferState = TRANSFER_READY
        self.oldLv = 0
        for key, val in self.posMap.items():
            page, pos = val
            self.posMap.pop(key)
            gameglobal.rds.ui.inventory.updateSlotState(page, pos)

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YAOPEI_TRANSFER)

    def refreshInfo(self):
        if self.mediator:
            self.transferState = TRANSFER_READY
            p = BigWorld.player()
            info = {}
            oldItemPos = self.posMap.get((0, 0), (None, None))
            newItemPos = self.posMap.get((0, 1), (None, None))
            btnEnabled = True
            if oldItemPos[0] == None and newItemPos[0] == None:
                btnEnabled = False
                info['extraVisible'] = False
                info['hint'] = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_TRANSFER_LACK_ALL_HINT, gameStrings.TEXT_YAOPEITRANSFERPROXY_79)
            elif oldItemPos[0] == None:
                btnEnabled = False
                info['extraVisible'] = False
                newItem = p.inv.getQuickVal(newItemPos[0], newItemPos[1])
                if newItem.getYaoPeiLv() >= SCD.data.get('maxYaoPeiLv', 0):
                    info['hint'] = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_TRANSFER_TARGET_MAX_LV, gameStrings.TEXT_YAOPEITRANSFERPROXY_86)
                else:
                    info['hint'] = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_TRANSFER_LACK_OLD_HINT, gameStrings.TEXT_YAOPEITRANSFERPROXY_88)
                info['newItemInfo'] = self.createBaseItemInfo(newItem)
            elif newItemPos[0] == None:
                btnEnabled = False
                info['extraVisible'] = False
                info['hint'] = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_TRANSFER_LACK_NEW_HINT, gameStrings.TEXT_YAOPEITRANSFERPROXY_94)
                oldItem = p.inv.getQuickVal(oldItemPos[0], oldItemPos[1])
                info['oldItemInfo'] = self.createBaseItemInfo(oldItem)
            else:
                oldItem = p.inv.getQuickVal(oldItemPos[0], oldItemPos[1])
                info['oldItemInfo'] = self.createBaseItemInfo(oldItem)
                newItem = p.inv.getQuickVal(newItemPos[0], newItemPos[1])
                info['newItemInfo'] = self.createBaseItemInfo(newItem)
                if newItem.getYaoPeiLv() >= SCD.data.get('maxYaoPeiLv', 0):
                    btnEnabled = False
                    info['extraVisible'] = False
                    info['hint'] = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_TRANSFER_TARGET_MAX_LV, gameStrings.TEXT_YAOPEITRANSFERPROXY_86)
                elif oldItem.yaoPeiExp <= newItem.yaoPeiExp:
                    btnEnabled = False
                    info['extraVisible'] = False
                    info['hint'] = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_TRANSFER_LACK_EXP_HINT, gameStrings.TEXT_YAOPEITRANSFERPROXY_112)
                else:
                    info['extraVisible'] = True
                    oldLv = newItem.getYaoPeiLv()
                    oldBasicAdd, oldExtraAdd, oldSkillLv = newItem.getYaoPeiPropsAdd(oldLv)
                    newLv = uiUtils.calcYaoPeiLv(newItem.quality, oldItem.yaoPeiExp)
                    newBasicAdd, newExtraAdd, newSkillLv = newItem.getYaoPeiPropsAdd(newLv)
                    maxActivatedLv = newItem.calcMaxYaoPeiLv()
                    propList = []
                    propActivateList = []
                    propList.append({'isProp': True,
                     'propName': 'Lv',
                     'oldValue': oldLv,
                     'newValue': newLv})
                    oldLvReqUp = ID.data.get(newItem.id, {}).get('lvReq', 0) + YLD.data.get(oldLv, {}).get('lvReqUp', 0)
                    newLvReqUp = ID.data.get(newItem.id, {}).get('lvReq', 0) + YLD.data.get(newLv, {}).get('lvReqUp', 0)
                    propList.append({'isProp': True,
                     'propName': gameStrings.TEXT_YAOPEITRANSFERPROXY_131,
                     'oldValue': oldLvReqUp,
                     'newValue': newLvReqUp})
                    if hasattr(newItem, 'yaoPeiProps'):
                        for prop in newItem.yaoPeiProps:
                            propInfo = gameglobal.rds.ui.yaoPeiLvUp.createPropInfo(prop[0], prop[1], prop[2], oldBasicAdd, newBasicAdd)
                            propList.append(propInfo)

                    if hasattr(newItem, 'rprops'):
                        for prop in newItem.rprops:
                            propInfo = gameglobal.rds.ui.yaoPeiLvUp.createPropInfo(prop[0], prop[1], prop[2], oldExtraAdd, newExtraAdd)
                            propList.append(propInfo)

                    if hasattr(newItem, 'yaoPeiExtraProps'):
                        for prop in newItem.yaoPeiExtraProps:
                            if prop[5] <= oldLv:
                                propInfo = gameglobal.rds.ui.yaoPeiLvUp.createPropInfo(prop[0], prop[1], prop[2], oldExtraAdd, newExtraAdd)
                                propList.append(propInfo)
                            elif prop[5] <= newLv:
                                propActivateInfo = gameglobal.rds.ui.yaoPeiLvUp.createPropActivateInfo(prop[0], prop[1], prop[2], prop[3], prop[4], newLv <= maxActivatedLv)
                                propActivateList.append(propActivateInfo)

                    yaoPeiSkillId = getattr(newItem, 'yaoPeiSkillId', 0)
                    if yaoPeiSkillId and oldSkillLv < newSkillLv:
                        if oldSkillLv > 0:
                            skillInfo = {}
                            skillInfo['isProp'] = False
                            skillInfo['skillDesc'] = gameStrings.TEXT_YAOPEILVUPPROXY_89 % (newSkillLv - oldSkillLv)
                            propList.append(skillInfo)
                        elif newSkillLv > 0:
                            skillInfo = {}
                            skillInfo['isProp'] = False
                            skillInfo['skillDesc'] = gameglobal.rds.ui.yaoPeiLvUp.createSkillDesc(yaoPeiSkillId)
                            propActivateList.append(skillInfo)
                    info['propList'] = propList
                    info['propActivateList'] = propActivateList
                    fId = SCD.data.get('yaoPeiTransferCost', 0)
                    if fId:
                        cash = formula.calcFormulaById(fId, {'quality': oldItem.quality,
                         'lv': oldItem.getYaoPeiLv()})
                    else:
                        cash = 0
                    if p.cash < cash:
                        extraCash = uiUtils.toHtml(format(cash, ','), '#F43804')
                        btnEnabled = False
                    else:
                        extraCash = format(cash, ',')
                    info['extraCash'] = extraCash
            info['btnEnabled'] = btnEnabled
            weekDiff = utils.getIntervalWeek(utils.getNow(), utils.getServerOpenTime())
            yaoPeiTargetExp = PYD.data.get(weekDiff, None)
            info['showPursueTip'] = False
            if yaoPeiTargetExp:
                info['showPursueTip'] = True
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def createBaseItemInfo(self, item):
        info = uiUtils.getGfxItem(item)
        yaoPeiLv = item.getYaoPeiLv()
        info['lv'] = 'Lv.%d' % yaoPeiLv
        nowLvExp = YLED.data.get((item.quality, yaoPeiLv), {}).get('exp', 0)
        maxYaoPeiLv = SCD.data.get('maxYaoPeiLv', 0)
        if yaoPeiLv >= maxYaoPeiLv:
            nowExp = 1
            lvMaxExp = 1
        else:
            nowExp = item.yaoPeiExp - nowLvExp
            lvMaxExp = YLED.data.get((item.quality, yaoPeiLv + 1), {}).get('exp', 0) - nowLvExp
        currentValue = 100.0
        if lvMaxExp > nowExp:
            currentValue = currentValue * nowExp / lvMaxExp
        info['currentValue'] = currentValue
        info['expBarText'] = str(round(currentValue, 1)) + '%'
        return info

    def transferFinish(self, ok, sPg, sPs, tPg, tPs):
        if ok:
            if self.posMap.get((0, 0), (None, None)) != (sPg, sPs) or self.posMap.get((0, 1), (None, None)) != (tPg, tPs):
                return None
            self.transferSuccess()
        else:
            self.refreshInfo()

    def transferSuccess(self):
        if self.mediator:
            self.transferState = TRANSFER_FINISH
            p = BigWorld.player()
            info = {}
            oldItemPos = self.posMap.get((0, 0), (None, None))
            newItemPos = self.posMap.get((0, 1), (None, None))
            oldItem = p.inv.getQuickVal(oldItemPos[0], oldItemPos[1])
            info['oldItemInfo'] = self.createBaseItemInfo(oldItem)
            newItem = p.inv.getQuickVal(newItemPos[0], newItemPos[1])
            info['newItemInfo'] = self.createBaseItemInfo(newItem)
            oldBasicAdd, oldExtraAdd, oldSkillLv = oldItem.getYaoPeiPropsAdd(self.oldLv)
            newLv = newItem.getYaoPeiLv()
            newBasicAdd, newExtraAdd, newSkillLv = newItem.getYaoPeiPropsAdd(newLv)
            propList = []
            propActivateList = []
            propList.append({'isProp': True,
             'propName': 'Lv',
             'oldValue': self.oldLv,
             'newValue': newLv})
            oldLvReqUp = ID.data.get(newItem.id, {}).get('lvReq', 0) + YLD.data.get(self.oldLv, {}).get('lvReqUp', 0)
            newLvReqUp = ID.data.get(newItem.id, {}).get('lvReq', 0) + YLD.data.get(newLv, {}).get('lvReqUp', 0)
            propList.append({'isProp': True,
             'propName': gameStrings.TEXT_YAOPEITRANSFERPROXY_131,
             'oldValue': oldLvReqUp,
             'newValue': newLvReqUp})
            if hasattr(newItem, 'yaoPeiProps'):
                for prop in newItem.yaoPeiProps:
                    propInfo = gameglobal.rds.ui.yaoPeiLvUp.createPropInfo(prop[0], prop[1], prop[2], oldBasicAdd, newBasicAdd)
                    propList.append(propInfo)

            if hasattr(newItem, 'rprops'):
                for prop in newItem.rprops:
                    propInfo = gameglobal.rds.ui.yaoPeiLvUp.createPropInfo(prop[0], prop[1], prop[2], oldExtraAdd, newExtraAdd)
                    propList.append(propInfo)

            if hasattr(newItem, 'yaoPeiExtraProps'):
                for prop in newItem.yaoPeiExtraProps:
                    if prop[5] <= self.oldLv:
                        propInfo = gameglobal.rds.ui.yaoPeiLvUp.createPropInfo(prop[0], prop[1], prop[2], oldExtraAdd, newExtraAdd)
                        propList.append(propInfo)
                    elif prop[5] <= newLv:
                        propActivateInfo = gameglobal.rds.ui.yaoPeiLvUp.createPropActivateInfo(prop[0], prop[1], prop[2], prop[3], prop[4], True)
                        propActivateList.append(propActivateInfo)

            yaoPeiSkillId = getattr(newItem, 'yaoPeiSkillId', 0)
            if yaoPeiSkillId and oldSkillLv < newSkillLv:
                if oldSkillLv > 0:
                    skillInfo = {}
                    skillInfo['isProp'] = False
                    skillInfo['skillDesc'] = gameStrings.TEXT_YAOPEILVUPPROXY_89 % (newSkillLv - oldSkillLv)
                    propList.append(skillInfo)
                elif newSkillLv > 0:
                    skillInfo = {}
                    skillInfo['isProp'] = False
                    skillInfo['skillDesc'] = gameglobal.rds.ui.yaoPeiLvUp.createSkillDesc(yaoPeiSkillId)
                    propActivateList.append(skillInfo)
            info['propList'] = propList
            info['propActivateList'] = propActivateList
            info['hint'] = gameStrings.TEXT_YAOPEITRANSFERPROXY_286
            self.mediator.Invoke('transferSuccess', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        self.transferState = TRANSFER_WAITING
        oldItemPos = self.posMap.get((0, 0), (None, None))
        newItemPos = self.posMap.get((0, 1), (None, None))
        if oldItemPos[0] == None or newItemPos[0] == None:
            return
        else:
            p = BigWorld.player()
            item = p.inv.getQuickVal(newItemPos[0], newItemPos[1])
            self.oldLv = item.getYaoPeiLv()
            isBind = item.isForeverBind()
            needMessageBox = False
            msg = ''
            if isBind and item.yaoPeiExp > 0:
                needMessageBox = True
                msg = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_TRANSFER_EXP_COVER_HINT, '')
            elif not isBind and item.yaoPeiExp <= 0:
                needMessageBox = True
                msg = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_TRANSFER_UNBIND_TO_BIND_HINT, '')
            elif not isBind and item.yaoPeiExp > 0:
                needMessageBox = True
                msg = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_TRANSFER_UNBIND_TO_BIND_AND_EXP_COVER_HINT, '')
            if needMessageBox:
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.realConfirm, oldItemPos[0], oldItemPos[1], newItemPos[0], newItemPos[1]), noCallback=self.refreshInfo)
            else:
                self.realConfirm(oldItemPos[0], oldItemPos[1], newItemPos[0], newItemPos[1])
            return

    def realConfirm(self, srcPage, srcPos, tgtPage, tgtPos):
        p = BigWorld.player()
        item = p.inv.getQuickVal(srcPage, srcPos)
        if item.getYaoPeiMaterialWeekly():
            msg = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_TRANSFER_MATERIALWEEKLY_COVER_HINT, gameStrings.TEXT_YAOPEITRANSFERPROXY_327)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.yaoPeiTransfer, srcPage, srcPos, tgtPage, tgtPos), noCallback=self.refreshInfo)
        else:
            p.cell.yaoPeiTransfer(srcPage, srcPos, tgtPage, tgtPos)

    def onRemoveItem(self, *arg):
        if self.transferState != TRANSFER_READY:
            return
        else:
            key = arg[3][0].GetString()
            _, slot = self.getSlotID(key)
            if self.posMap.get((0, slot), (None, None))[0] == None:
                return
            self.removeItem(slot, True)
            return

    def getSlotID(self, key):
        _, idItem = key.split('.')
        return (0, int(idItem[4:]))

    def _getKey(self, slot):
        return 'yaoPeiTransfer0.slot%d' % slot

    def setItem(self, srcBar, srcSlot, destSlot):
        if self.transferState != TRANSFER_READY:
            return
        p = BigWorld.player()
        srcItem = p.inv.getQuickVal(srcBar, srcSlot)
        if srcItem.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        self.removeItem(destSlot, False)
        key = self._getKey(destSlot)
        if self.binding.has_key(key):
            self.posMap[0, destSlot] = (srcBar, srcSlot)
            gameglobal.rds.ui.inventory.updateSlotState(srcBar, srcSlot)
            self.refreshInfo()

    def removeItem(self, slot, needRefresh):
        key = self._getKey(slot)
        if self.binding.has_key(key):
            srcBar, srcSlot = self.posMap.get((0, slot), (None, None))
            if srcBar != None:
                self.posMap.pop((0, slot))
                gameglobal.rds.ui.inventory.updateSlotState(srcBar, srcSlot)
        if needRefresh:
            self.refreshInfo()

    def findEmptyPos(self):
        for i in xrange(2):
            key = (0, i)
            if not self.posMap.has_key(key):
                return i

        return 1

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            if item.isYaoPei():
                return (page, pos) in self.posMap.values()
            else:
                return True
        else:
            return False

    @ui.uiEvent(uiConst.WIDGET_YAOPEI_TRANSFER, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        else:
            desPos = self.findEmptyPos()
            self.setInventoryItem(nPage, nItem, desPos)
            return

    def setInventoryItem(self, nPageSrc, nItemSrc, nItemDes):
        p = BigWorld.player()
        srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
        if srcItem:
            if srcItem.isYaoPei():
                self.setItem(nPageSrc, nItemSrc, nItemDes)

    def changeItem(self, nItemSrc, nItemDes):
        if self.transferState != TRANSFER_READY:
            return
        p = BigWorld.player()
        srcBar, srcSlot = self.posMap.get((0, nItemSrc), (const.CONT_NO_PAGE, const.CONT_NO_POS))
        srcItem = p.inv.getQuickVal(srcBar, srcSlot)
        if not srcItem:
            return
        destBar, destSlot = self.posMap.get((0, nItemDes), (const.CONT_NO_PAGE, const.CONT_NO_POS))
        destItem = p.inv.getQuickVal(destBar, destSlot)
        if destItem:
            self.setItem(destBar, destSlot, nItemSrc)
            self.setItem(srcBar, srcSlot, nItemDes)
        else:
            self.removeItem(nItemSrc, False)
            self.setItem(srcBar, srcSlot, nItemDes)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        _, slot = self.getSlotID(key)
        srcBar, srcSlot = self.posMap.get((0, slot), (None, None))
        item = BigWorld.player().inv.getQuickVal(srcBar, srcSlot)
        return gameglobal.rds.ui.inventory.GfxToolTip(item)
