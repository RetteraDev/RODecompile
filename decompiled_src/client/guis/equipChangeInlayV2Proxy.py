#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangeInlayV2Proxy.o
from gamestrings import gameStrings
import BigWorld
import gameconfigCommon
import gameglobal
import gamelog
import uiUtils
import const
import ui
import utils
import gametypes
import commcalc
import copy
from gamestrings import gameStrings
from uiProxy import UIProxy
from callbackHelper import Functor
from guis import uiConst
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from guis import events
import itemToolTipUtils
from item import Item
from data import sys_config_data as SCD
from data import equip_gem_data as EGD
from data import equip_data as ED
from data import game_msg_data as GMD
from cdata import wen_yin_data as WYD
from cdata import equip_gem_inverted_data as EGID
from cdata import equip_gem_unlock_slot_data as EGUSD
from cdata import game_msg_def_data as GMDD
RES_KIND_EQUIP = 0
RES_KIND_SUB_EQUIP = 1
RES_KIND_INV = 2
MAX_GEM_CNT = 3
GEM_FRAME_NAME_TYPE_REF = {(2, 2): 'kuangzhan',
 (2, 1): 'bihu',
 (1, 2): 'paoxiao',
 (1, 1): 'weishe'}
LEFT_ITEM_CLS_NAME = 'EquipChangeBG_LeftItem'
ONE_SIDE_GEM_MAX_CNT = 3
COLOR_RED = '#FB0000'

class EquipChangeInlayV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipChangeInlayV2Proxy, self).__init__(uiAdapter)
        self.resetData()
        self.equipGemTypeMap = {}

    def registerPanel(self, widget):
        BigWorld.player().fillGemToEquipments(False)
        self.resetData()
        self.widget = widget
        self.initUI()
        self.genEquipGemTypeMap()
        self.widget.effect.visible = False
        self.doTabBtnClick('tab0')
        BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.refreshAll)
        BigWorld.player().registerEvent(const.EVENT_ITEM_REMOVE, self.refreshAll)

    def unRegisterPanel(self, *arg):
        self.resetData()
        BigWorld.player().unRegisterEvent(const.EVENT_ITEM_CHANGE, self.refreshAll)
        BigWorld.player().unRegisterEvent(const.EVENT_ITEM_REMOVE, self.refreshAll)

    def initUI(self, *args):
        self.widget.left.tab0.visible = False
        self.widget.left.tab1.visible = False
        self.widget.left.tab2.visible = False
        self.widget.left.scrollList.itemRenderer = LEFT_ITEM_CLS_NAME
        self.widget.left.scrollList.itemHeight = 64
        self.widget.left.scrollList.lableFunction = self.lableFunction
        self.widget.equipItem.removeBtn.visible = False
        self.widget.equipItem.addIcon.visible = False
        ASUtils.setHitTestDisable(self.widget.effect, True)
        self.widget.left.switchBtn.visible = gameconfigCommon.enableSubWenYin()
        self.widget.left.cancelBtn.visible = False
        self.widget.left.switchBtn.addEventListener(events.BUTTON_CLICK, self.handleSwtichBtnClick, False, 0, True)
        self.widget.left.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick, False, 0, True)

    def handleSwtichBtnClick(self, *args):
        if not self.isSubMode:
            self.isSubMode = True
            self.refreshAll()
        else:
            BigWorld.player().cell.switchWenYin()

    def handleCancelBtnClick(self, *args):
        self.isSubMode = False
        self.refreshAll()

    def resetData(self):
        self.selectedUUID = ''
        self.lastTabIdx = -1
        self.selectedEquipMc = None
        self.selectedGemMc = None
        self.selectedGemItemMc = None
        self.lastSelectedGemItem = None
        self.selectedGemItemUuid = ''
        self.selectedGemItemPos = (-1, -1)
        self.widget = None
        self.leftDataInfo = {}
        self.selectedPart = -1
        self.selectedGemPos = (-1, -1)
        self.selectedGemItemUuid = ''
        self.enableDikou = True
        self.equipGemTypeMap = {}
        self.gemItemCache = []
        self.bindItemConfirm = False
        self.bindMixItemConfirm = False
        self.mixItemId = 0
        self.maxLvGemPos = 0
        self.needAutoSelect = False
        self.autoSelectedGemItemUuid = ''
        self.isSubMode = False

    def onTabBtnClick(self, *args):
        e = ASObject(args[3][0])
        self.doTabBtnClick(e.currentTarget.name)

    def refreshLeftList(self, info):
        if not self.widget:
            return
        self.widget.left.switchBtn.label = gameStrings.GUAN_YIN_V3_SUB_BTN if not self.isSubMode else gameStrings.GUAN_YIN_V3_REPLACE_BTN
        self.widget.left.cancelBtn.visible = self.isSubMode
        idx = info['tabIdx']
        data = info['data']
        if self.lastTabIdx != idx:
            self.selectedUUID = ''
            self.selectedPart = -1
        if self.selectedUUID == '' and len(data) > 0:
            self.doLeftItemClick(data[0]['pos'])
            self.selectedUUID = data[0]['uuid']
        elif len(data) == 0:
            self.showNoneItemChoosed()
        self.widget.left.scrollList.dataArray = data
        self.widget.left.scrollList.validateNow()
        self.widget.txtNoEquip.visible = len(data) == 0
        self.lastTabIdx = idx

    def showNoneItemChoosed(self):
        self.widget.supportGemType.visible = False
        gfxItem = {}
        gfxItem['gemSlotState'] = uiConst.GEM_SLOT_LOCKED
        gfxItem['pos'] = [uiConst.GEM_TYPE_YIN, 1]
        gfxItem['noneItem'] = True
        yinSlots = [gfxItem, gfxItem, gfxItem]
        gfxItem['pos'] = [uiConst.GEM_TYPE_YANG, 1]
        yangSlots = [gfxItem, gfxItem, gfxItem]
        self.setOnSideGem('left', yinSlots, MAX_GEM_CNT)
        self.setOnSideGem('right', yangSlots, MAX_GEM_CNT)
        self.widget.gotoAndStop('enable')
        self.widget.confirmBtn.visible = False
        self.widget.equipItem.slot.data = None

    def lableFunction(self, *args):
        itemData = ASObject(args[3][0])
        item = ASObject(args[3][1])
        item.data = itemData
        for i, info in enumerate(item.data.slotDatas):
            getattr(item, 'itemSlot%d' % i).setSlotState(info['state'])

        if self.selectedUUID == itemData.uuid:
            item.selected = True
            self.selectedEquipMc = item
        else:
            item.selected = False
        item.removeEventListener(events.MOUSE_CLICK, self.handleClickLeftItem)
        item.addEventListener(events.MOUSE_CLICK, self.handleClickLeftItem, False, 0, True)

    def handleClickLeftItem(self, *args):
        if not self.widget:
            return
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if self.selectedUUID == itemMc.data.uuid:
            return
        if self.selectedEquipMc:
            self.selectedEquipMc.selected = False
        self.selectedEquipMc = itemMc
        self.selectedEquipMc.selected = True
        self.selectedGemPos = (-1, -1)
        self.needAutoSelect = True
        self.selectedUUID = self.selectedEquipMc.data.uuid
        selectedPart = self.selectedEquipMc.data.pos
        self.doLeftItemClick(selectedPart)

    def setOnSideGem(self, side, slotDatas, slotCnt):
        for i in xrange(MAX_GEM_CNT):
            gemMc = self.widget.getChildByName('%sGem%d' % (side, i))
            lockMc = self.widget.getChildByName('%sLock%d' % (side, i))
            if i >= slotCnt:
                lockMc.visible = False
                gemMc.visible = False
                continue
            else:
                lockMc.visible = True
                gemMc.visible = True
            slotData = slotDatas[i]
            gemMc.removeBtn.visible = False
            gemMc.addIcon.visible = False
            gemMc.slot.visible = False
            gemMc.slot.setSlotState(uiConst.ITEM_NORMAL)
            gemMc.slot.data = None
            gemMc.slot.validateNow()
            gemMc.pos = slotData['pos']
            lockMc.pos = slotData['pos']
            lockMc.btn.selected = False
            gemMc.addEventListener(events.MOUSE_CLICK, self.onGemClick, False, 0, True)
            lockMc.addEventListener(events.MOUSE_CLICK, self.onGemClick, False, 0, True)
            TipManager.removeTip(gemMc)
            TipManager.removeTip(lockMc)
            ASUtils.setHitTestDisable(lockMc.effect, True)
            lockMc.effect.gotoAndStop('normal')
            ASUtils.setMcEffect(gemMc.slot, '')
            if slotData['gemSlotState'] == uiConst.GEM_SLOT_LOCKED:
                gemMc.visible = False
                lockMc.visible = True
                if i != 0 and slotDatas[i - 1]['gemSlotState'] == uiConst.GEM_SLOT_LOCKED or slotData.has_key('noneItem'):
                    lockMc.gotoAndStop('cantUnlock')
                    ASUtils.setHitTestDisable(lockMc.btn, True)
                    lockMc.removeEventListener(events.MOUSE_CLICK, self.onGemClick)
                    TipManager.addTip(lockMc, gameStrings.EQUIP_CHANGE_GEM_PROXY_TIP_CANT_UNLOCK)
                else:
                    lockMc.gotoAndStop('lock')
                    ASUtils.setHitTestDisable(lockMc.btn, False)
                    TipManager.addTip(lockMc, gameStrings.EQUIP_CHANGE_GEM_PROXY_TIP_UNLOCK)
            elif slotData['gemSlotState'] == uiConst.GEM_SLOT_FILLED:
                lockMc.visible = False
                gemMc.visible = True
                gemMc.slot.visible = True
                gemMc.data = None
                gemMc.removeBtn.visible = True
                gemMc.slot.data = slotData
                if slotData['state'] == uiConst.ITEM_GRAY:
                    ASUtils.setMcEffect(gemMc.slot, 'gray')
                gemMc.slot.dragable = False
                gemMc.slot.validateNow()
                gemMc.removeBtn.data = slotData['pos']
                gemMc.removeBtn.addEventListener(events.BUTTON_CLICK, self.onRemoveBtnClick, False, 0, True)
            else:
                lockMc.visible = True
                lockMc.gotoAndStop('lock')
                lockMc.btn.selected = False
                gemMc.visible = False
                gemMc.slot.visible = True
                lockMc.effect.gotoAndStop(lockMc.effect.totalFrames)
                TipManager.addTip(lockMc, gameStrings.EQUIP_CHANGE_GEM_PROXY_TIP_INLAYT)

    def onGemClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        self.needAutoSelect = False
        if self.selectedGemPos[0] == target.pos[0] and self.selectedGemPos[1] == target.pos[1]:
            return
        else:
            if self.selectedGemMc:
                if self.selectedGemMc.effect:
                    self.selectedGemMc.btn.selected = False
                else:
                    self.selectedGemMc.slot.setSlotState(uiConst.ITEM_NORMAL)
                    if self.selectedGemMc.slot.data.state == uiConst.ITEM_GRAY:
                        ASUtils.setMcEffect(self.selectedGemMc.slot, 'gray')
            if target.effect:
                target.btn.selected = True
            else:
                target.slot.setSlotState(uiConst.ITEM_SELECTED)
                if target.slot.data.state == uiConst.ITEM_GRAY:
                    ASUtils.setMcEffect(target.slot, 'gray')
            self.selectedGemMc = target
            self.selectedGemItemMc = None
            self.doGemClick(target.pos[0], target.pos[1])
            return

    def refreshDetailInfo(self, info):
        self.widget.equipItem.slot.dragable = False
        self.widget.equipItem.slot.data = info
        self.widget.supportGemType.visible = True
        frameName = 'type%d' % len(info['supportGems'])
        self.widget.supportGemType.gotoAndStop(frameName)
        for index, supportType in enumerate(info['supportGems']):
            mc = self.widget.supportGemType.getChildByName('gem%d' % index)
            mc.gotoAndStop(GEM_FRAME_NAME_TYPE_REF.get(supportType))

        tipInfo = self.genGemTypeTips(info['supportGems'])
        TipManager.addTip(self.widget.supportGemType, tipInfo)
        yinSlots = info['yinSlots']
        yangSlots = info['yangSlots']
        self.widget.gotoAndStop('enable')
        self.setOnSideGem('left', yinSlots, info['yinSlotsCnt'])
        self.setOnSideGem('right', yangSlots, info['yangSlotsCnt'])
        self.widget.gem.visible = False
        self.widget.confirmBtn.visible = False

    def genGemTypeTips(self, supportGems):
        cfgData = SCD.data.get('gemTypeTips', {})
        tips = '%s\n' % cfgData.get('head', '')
        for gemType in supportGems:
            tips += '%s\n' % cfgData.get(gemType, '')

        return tips

    def refreshGemDetail(self, info):
        equipItem = self.getSelectedPart()
        self.selectedGemItemUuid = ''
        if getattr(self, 'autoSelectedGemItemUuid', None):
            self.selectedGemItemUuid = self.autoSelectedGemItemUuid
            self.autoSelectedGemItemUuid = ''
        state = info['gemState']
        self.widget.confirmBtn.enabled = True
        self.widget.confirmBtn.removeEventListener(events.MOUSE_CLICK, self.onInlayBtnClick)
        self.widget.confirmBtn.removeEventListener(events.MOUSE_CLICK, self.onLvUpBtnClick)
        self.widget.confirmBtn.removeEventListener(events.MOUSE_CLICK, self.onUnlockBtnClick)
        if state == uiConst.GEM_SLOT_EMPTY:
            self.widget.gotoAndStop('inlay')
            self.widget.gem.visible = False
            self.widget.confirmBtn.label = gameStrings.EQUIP_CHANGE_GEM_PROXY_INLAY
            self.widget.confirmBtn.enabled = False
            self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.onInlayBtnClick, False, 0, True)
            self.refreshGemList(info['gemList'])
        elif state == uiConst.GEM_SLOT_FILLED:
            lvUpInfo = info.get('lvUpInfo', None)
            if not lvUpInfo:
                return
            if lvUpInfo.get('noNewGemId', None):
                self.widget.gotoAndStop('enable')
                self.widget.confirmBtn.enabled = False
                BigWorld.player().showGameMsg(GMDD.data.GEM_MAX_LV, ())
            else:
                self.widget.gotoAndStop('filled')
                self.widget.gem.visible = False
                self.widget.confirmBtn.visible = True
                self.widget.confirmBtn.label = gameStrings.EQUIP_CHAGNE_GEM_PROXY_MIX
                self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.onLvUpBtnClick, False, 0, True)
                self.refreshLvUpInfo(lvUpInfo)
        elif state == uiConst.GEM_SLOT_LOCKED:
            self.widget.gotoAndStop('lock')
            self.widget.gem.visible = False
            self.widget.disableDiKou.visible = False
            self.widget.diKou.diKou.yunchuiBtn.addEventListener(events.MOUSE_CLICK, self.onYunChuiBtnClick, False, 0, True)
            self.widget.confirmBtn.visible = True
            self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.onUnlockBtnClick, False, 0, True)
            self.widget.confirmBtn.label = gameStrings.EQUIP_CHANGE_GEM_PROXY_UNLOCK
            self.setCost(info['unlockCost'])

    def setCost(self, data):
        widget = self.widget.diKou
        widget.diKou.checkBox.removeEventListener(events.MOUSE_CLICK, self.onCheckBoxSelected)
        widget.cashCost.cashText.text = data['cash']
        widget.cashCost.cashText.textColor = '0xFFFFFF' if data['cash'] <= data['playerCash'] else '0xF43804'
        widget.cashCost.visible = data['cash'] > 0
        if not widget.needItem.data:
            widget.needItem.setItemSlotData(data['item'])
        elif not int(widget.needItem.data.id) != data['item']['id']:
            widget.needItem.setItemSlotData(data['item'])
        else:
            widget.needItem.setValueAmountTxt(data['item']['count'])
        if data['showHelp']:
            widget.needItem.setSlotState(uiConst.COMPLETE_ITEM_LEAKED)
        else:
            widget.needItem.setSlotState(uiConst.ITEM_NORMAL)
        widget.needItem.dragable = False
        widget.needItem.setAutoFontSize(True, 11)
        widget.needItem.validateNow()
        TipManager.addItemTipById(widget.needItem, data['item']['itemId'])
        widget.needItem.visible = True
        if data['enableEquipDiKou']:
            widget.diKou.checkBox.selected = data['selectedDiKou']
            if data['selectedDiKou']:
                widget.diKou.yunchuiIcon.validateNow()
                widget.diKou.yunchui.htmlText = data['yunchui']
                widget.diKou.yunchuiBtn.enabled = data['yunchuiEnabled']
            else:
                widget.diKou.yunchui.htmlText = data['yunchui']
                widget.diKou.yunchuiBtn.enabled = False
        else:
            widget.diKou.visible = False
        self.widget.confirmBtn.enabled = data['isEnough']
        widget.diKou.checkBox.addEventListener(events.EVENT_SELECT, self.onCheckBoxSelected, False, 0, True)

    def refreshLvUpInfo(self, lvUpInfo):
        mixItemInfo = lvUpInfo.get('mixItemInfo', None)
        if mixItemInfo:
            self.widget.item1.visible = False
            self.widget.item0.visible = True
            self.widget.item2.visible = True
            needItemInfo = lvUpInfo['needItemInfo']
            self.widget.item0.data = needItemInfo
            if needItemInfo['showHelp']:
                self.widget.item0.setSlotState(uiConst.COMPLETE_ITEM_LEAKED)
            else:
                self.widget.item0.setSlotState(uiConst.ITEM_NORMAL)
            mixItemInfo = lvUpInfo['mixItemInfo']
            self.widget.item2.data = mixItemInfo
            if mixItemInfo['showHelp']:
                self.widget.item2.setSlotState(uiConst.COMPLETE_ITEM_LEAKED)
            else:
                self.widget.item2.setSlotState(uiConst.ITEM_NORMAL)
        else:
            self.widget.item0.visible = False
            self.widget.item2.visible = False
            self.widget.item1.visible = True
            needItemInfo = lvUpInfo['needItemInfo']
            self.widget.item1.data = needItemInfo
            if needItemInfo['showHelp']:
                self.widget.item1.setSlotState(uiConst.COMPLETE_ITEM_LEAKED)
            else:
                self.widget.item1.setSlotState(uiConst.ITEM_NORMAL)
        self.widget.item0.dragable = False
        self.widget.item1.dragable = False
        self.widget.item2.dragable = False
        self.widget.consume.visible = False
        self.widget.confirmBtn.enabled = lvUpInfo['isEnough']

    def refreshGemList(self, gemItems):
        self.selectedGemItemMc = None
        self.widget.gemList.scrollList.itemRenderer = 'EquipChangeGemWi_GemItem'
        self.widget.gemList.scrollList.lableFunction = self.gemListLabelFun
        self.widget.gemList.scrollList.dataArray = gemItems
        self.widget.gemList.scrollList.validateNow()
        if gemItems:
            pos = int(self.widget.gemList.scrollList.canvas.height * (self.maxLvGemPos * 1.0 / len(gemItems)))
            self.widget.gemList.scrollList.scrollTo(pos)
        self.widget.gemList.desc.text = gameStrings.EQUIP_CHAGNE_GEM_PROXY_GEMS

    def gemListLabelFun(self, *args):
        data = ASObject(args[3][0])
        mc = ASObject(args[3][1])
        item = BigWorld.player().inv.getQuickVal(int(data.itemPos[0]), int(data.itemPos[1]))
        mc.overMc.visible = False
        ASUtils.setHitTestDisable(mc.overMc, True)
        ASUtils.setHitTestDisable(mc.selectedMc, True)
        mc.item.data = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
        mc.item.setSlotState(data.state)
        mc.item.pos = data.pos
        mc.item.dragable = False
        mc.txtName.htmlText = data.gemName
        mc.txtProperty.htmlText = data.addProp
        mc.addEventListener(events.MOUSE_OVER, self.onGemItemOver, False, 0, True)
        mc.addEventListener(events.MOUSE_OUT, self.onGemItemOut, False, 0, True)
        mc.addEventListener(events.MOUSE_CLICK, self.onGemItemClick, False, 0, True)
        p = BigWorld.player()
        isEquip = bool(p.equipment[self.selectedPart] or commcalc.getAlternativeEquip(p, self.selectedPart))
        ASUtils.setMcEffect(mc.item, 'normal' if isEquip else 'gray')
        if self.selectedGemItemUuid and self.selectedGemItemUuid == item.uuid:
            mc.selectedMc.visible = True
            self.selectedGemItemMc = mc
            self.onGemItemClick(mc)
        else:
            mc.selectedMc.visible = False

    def onGemItemClick(self, *args):
        if not self.widget:
            return
        if len(args) == 1:
            currentTarget = args[0]
        else:
            currentTarget = ASObject(args[3][0]).currentTarget
        uuid = currentTarget.item.data.uuid
        if self.selectedGemItemMc and self.selectedGemItemMc.selectedMc:
            self.selectedGemItemMc.selectedMc.visible = False
        self.widget.gem.visible = True
        self.widget.gem.addIcon.visible = False
        self.widget.gem.removeBtn.visible = False
        slotData = currentTarget.item.data
        self.widget.gem.slot.data = slotData
        self.widget.gem.slot.dragable = False
        self.widget.gem.slot.setSlotState(uiConst.ITEM_NORMAL)
        self.widget.gem.slot.validateNow()
        self.widget.gem.slot.valueAmount.visible = False
        self.widget.confirmBtn.enabled = True
        self.widget.confirmBtn.visible = True
        currentTarget.selectedMc.visible = True
        self.selectedGemItemMc = currentTarget
        self.selectedGemItemUuid = uuid
        self.selectedGemItemPos = (int(currentTarget.item.pos[0]), int(currentTarget.item.pos[1]))

    def onGemItemOver(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.overMc.visible = True

    def onGemItemOut(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.overMc.visible = False

    def onRemoveBtnClick(self, *args):
        e = ASObject(args[3][0])
        gemType = int(e.currentTarget.data[0])
        gemSlotIdx = int(e.currentTarget.data[1])
        p = BigWorld.player()
        selectedItem = self.getSelectedPart()
        if not selectedItem:
            return
        self.needAutoSelect = True
        gamelog.info('jbx:removeWYGem', self.selectedPart, gemType, gemSlotIdx)
        if self.isSubMode:
            p.cell.removeSubWYGem(self.selectedPart, gemType, gemSlotIdx)
        else:
            p.cell.removeWYGem(self.selectedPart, gemType, gemSlotIdx)

    def getWenYin(self):
        if not self.isSubMode:
            return BigWorld.player().wenYin
        return BigWorld.player().subWenYin

    def onInlayBtnClick(self, *args):
        wenYin = self.getWenYin()
        if self.widget.currentFrameLabel == 'inlay':
            wenYinVal = self.getSelectedPart()
            if not wenYinVal:
                return
            p = BigWorld.player()
            gemItem = p.inv.getQuickVal(*self.selectedGemItemPos)
            if not gemItem:
                return
            if not wenYin.checkGemOrder(p.equipment, gemItem.id, self.selectedPart):
                msg = GMD.data.get(GMDD.data.WENYIN_INLAY_CONFIRM, {}).get('text', 'GMDD.data.WENYIN_INLAY_CONFIRM')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.confirmAddGem)
            else:
                self.confirmAddGem()

    @ui.looseGroupTradeConfirm(const.LAST_PARAMS, GMDD.data.RETURN_BACK_ADD_GEM)
    def confirmAddGem(self):
        self.showInalyEff()
        ASUtils.callbackAtFrame(self.widget.effect, 10, self.realAddGem)

    def realAddGem(self, *args):
        self.hideInalyEff()
        if self.selectedPart >= 0 and self.selectedGemPos[1] >= 0 and self.selectedGemItemPos[0] >= 0 and self.selectedGemItemPos[1] >= 0:
            self.needAutoSelect = True
            if self.isSubMode:
                BigWorld.player().cell.addSubWYGem(self.selectedPart, self.selectedGemPos[1], self.selectedGemItemPos[0], self.selectedGemItemPos[1])
            else:
                BigWorld.player().cell.addWYGem(self.selectedPart, self.selectedGemPos[1], self.selectedGemItemPos[0], self.selectedGemItemPos[1])

    def onCheckBoxSelected(self, *args):
        e = ASObject(args[3][0])
        self.enableDikou = e.currentTarget.selected
        selectedItem = self.getSelectedPart()
        if not selectedItem:
            return
        gemItem = selectedItem.getEquipGemSlot(self.selectedGemPos[0], self.selectedGemPos[1])
        info = self.getGemDetailInfo(gemItem)
        self.refreshGemDetail(info)

    def genEquipGemTypeMap(self):
        if self.equipGemTypeMap:
            return
        for key, vale in EGD.data.iteritems():
            equipLimit = vale.get('equipLimit', ())
            type = vale.get('type', 0)
            subType = vale.get('subType', 0)
            gemType = (type, subType)
            for part in equipLimit:
                gemTypeSet = self.equipGemTypeMap.get(part, set())
                gemTypeSet.add(gemType)
                self.equipGemTypeMap[part] = gemTypeSet

        for key, value in self.equipGemTypeMap.iteritems():
            value = list(value)
            value.sort(key=lambda type: type[0], reverse=True)
            self.equipGemTypeMap[key] = value

    def getLeftListInfo(self, tabIdx):
        info = {}
        info['tabIdx'] = tabIdx
        data = []
        p = BigWorld.player()
        for partId, partData in WYD.data.iteritems():
            itemInfo = self.getLeftPartData(partId)
            data.append(itemInfo)

        data.sort(key=lambda x: x['sortIdx'])
        info['data'] = data
        return info

    def getLeftPartData(self, partId):
        itemId = WYD.data.get(partId, {}).get('showItemId', 999)
        itemInfo = uiUtils.getGfxItemById(itemId)
        itemInfo['itemName'] = uiUtils.getItemColorName(itemId)
        itemInfo['uuid'] = partId
        itemInfo['sortIdx'] = 0
        slotDatas = []
        slotDatas.extend(self.getPartSlotData(partId, uiConst.GEM_TYPE_YIN))
        slotDatas.extend(self.getPartSlotData(partId, uiConst.GEM_TYPE_YANG))
        itemInfo['slotDatas'] = slotDatas
        itemInfo['quality'] = 0
        itemInfo['score'] = 0
        itemInfo['pos'] = partId
        return itemInfo

    def getLeftItemData(self, item, tabIdx, location):
        itemInfo = uiUtils.getGfxItem(item, location=location)
        itemInfo['itemName'] = uiUtils.getItemColorNameByItem(item, True, -1, True)
        itemInfo['sortIdx'] = uiUtils.getEquipSortIdxByPart(item)
        slotDatas = []
        slotDatas.extend(self.getItemSlotData(uiConst.GEM_TYPE_YIN, item, uiConst.GEM_SLOT_FILLED))
        slotDatas.extend(self.getItemSlotData(uiConst.GEM_TYPE_YANG, item, uiConst.GEM_SLOT_FILLED))
        itemInfo['slotDatas'] = slotDatas
        if tabIdx == RES_KIND_INV:
            itemInfo['quality'] = getattr(item, 'quality', 0)
            itemInfo['score'] = getattr(item, 'score', 0)
        return itemInfo

    def getDetailItemData(self):
        itemInfo = self.getLeftPartData(self.selectedPart)
        supportGems = self.equipGemTypeMap[WYD.data.get(self.selectedPart, {}).get('gemEquipType', 1)]
        itemInfo['supportGems'] = supportGems
        itemInfo['itemName'] = uiUtils.getItemColorName(WYD.data.get(self.selectedPart, {}).get('showItemId', 1))
        itemInfo['yinSlots'] = self.getPartSlotData(self.selectedPart, uiConst.GEM_TYPE_YIN)
        itemInfo['yangSlots'] = self.getPartSlotData(self.selectedPart, uiConst.GEM_TYPE_YANG)
        wenYinVal = self.getWenYin().get(self.selectedPart)
        itemInfo['yangSlotsCnt'] = len(getattr(wenYinVal, 'yangSlots', []))
        itemInfo['yinSlotsCnt'] = len(getattr(wenYinVal, 'yinSlots', []))
        return itemInfo

    def sort_unEquip(self, a, b):
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

    def getPartSlotData(self, partId, type, state = None):
        dataList = []
        p = BigWorld.player()
        for i in xrange(MAX_GEM_CNT):
            gemSlot = self.getWenYin().getGemSlot(partId, type, i)
            if gemSlot != None and gemSlot.gem:
                if state:
                    if gemSlot.state != state:
                        continue
                if gemSlot.gem:
                    gfxItem = uiUtils.getGfxItemById(gemSlot.gem.id, srcType=self.getSrcTypeStr())
                    self.gemItemCache.append(gemSlot.gem)
                else:
                    gfxItem = {}
                gfxItem['gemSlotState'] = gemSlot.state
                gfxItem['pos'] = [type, i]
                if self.getWenYin().isPartValid(p.equipment, partId, type, i):
                    gfxItem['state'] = uiConst.ITEM_NORMAL
                else:
                    gfxItem['state'] = uiConst.ITEM_GRAY
                dataList.append(gfxItem)
            elif not state:
                gfxItem = {}
                gfxItem['gemSlotState'] = uiConst.GEM_SLOT_EMPTY
                gfxItem['pos'] = [type, i]
                if self.getWenYin().isPartValid(p.equipment, partId, type, i):
                    gfxItem['state'] = uiConst.ITEM_NORMAL
                else:
                    gfxItem['state'] = uiConst.ITEM_GRAY
                dataList.append(gfxItem)

        return dataList

    def getItemSlotData(self, type, item, state = None):
        dataList = []
        for i in xrange(MAX_GEM_CNT):
            gemSlot = item.getEquipGemSlot(type, i)
            if gemSlot != None:
                if state:
                    if gemSlot.state != state:
                        continue
                if gemSlot.gem:
                    gfxItem = uiUtils.getGfxItemById(gemSlot.gem.id, srcType=self.getSrcTypeStr())
                    self.gemItemCache.append(gemSlot.gem)
                else:
                    gfxItem = {}
                gfxItem['gemSlotState'] = gemSlot.state
                gfxItem['pos'] = [type, i]
                dataList.append(gfxItem)
            elif not state:
                gfxItem = {}
                gfxItem['gemSlotState'] = uiConst.GEM_SLOT_LOCKED
                gfxItem['pos'] = [type, i]
                dataList.append(gfxItem)

        return dataList

    def getSrcTypeStr(self):
        str = 'equipChangeInlayV2%d' % len(self.gemItemCache)
        return str

    def onTabBtnClick(self, *args):
        e = ASObject(args[3][0])
        tabName = e.currentTarget.name
        self.doTabBtnClick(tabName)

    def doTabBtnClick(self, tabName):
        tabIdx = int(tabName[-1])
        info = self.getLeftListInfo(tabIdx)
        self.leftDataInfo = info
        self.refreshLeftList(info)

    def getSelectedPart(self):
        return self.getWenYin().get(self.selectedPart, None)

    def doLeftItemClick(self, partId):
        if self.selectedPart == partId:
            return
        else:
            if self.selectedGemMc:
                if self.selectedGemMc.slot:
                    self.selectedGemMc.slot.setSlotState(uiConst.ITEM_NORMAL)
                else:
                    self.selectedGemMc.btn.selected = False
                self.selectedGemMc = None
            self.selectedPart = partId
            selectedPart = self.getSelectedPart()
            if not selectedPart:
                self.showNoneItemChoosed()
                return
            itemInfo = self.getDetailItemData()
            self.refreshDetailInfo(itemInfo)
            selectedGemPos = self.getAutoSelectedGemPos()
            if selectedGemPos != None:
                self.selectedGemPos = selectedGemPos
                gemSlot = selectedPart.getEquipGemSlot(*self.selectedGemPos)
                info = self.getGemDetailInfo(gemSlot)
                self.refreshGemDetail(info)
                self.autoSelected()
            return

    def getGemList(self):
        gemList = []
        p = BigWorld.player()
        equipItem = self.getSelectedPart()
        gemType = self.selectedGemPos[0]
        for pg in p.inv.getPageTuple():
            for ps in p.inv.getPosTuple(pg):
                item = p.inv.getQuickVal(pg, ps)
                if item == const.CONT_EMPTY_VAL:
                    continue
                if not item.isEquipGem():
                    continue
                gemData = EGD.data.get(item.parentId(item.id), {})
                if not gemData:
                    continue
                if gemType != gemData.get('type', -1):
                    continue
                if not self.canAddGem(equipItem, item):
                    continue
                itemInfo = {}
                itemInfo['itemPos'] = (pg, ps)
                data = utils.getEquipGemData(item.id)
                prop = data.get('gemProps', [])
                addProp = ''
                if len(prop) > 0:
                    addProp += itemToolTipUtils.getGemProp(prop)
                itemInfo['addProp'] = addProp
                itemInfo['gemName'] = uiUtils.getItemColorNameByItem(item, True)
                itemInfo['gemLv'] = data.get('lv', 0)
                itemInfo['isBinded'] = item.isForeverBind()
                itemInfo['isAttProp'] = gemData.get('subType', 1) == 2
                itemInfo['pos'] = (pg, ps)
                if not self.checkGemOrder(item.id, self.selectedPart):
                    itemInfo['state'] = uiConst.ITEM_GRAY
                else:
                    itemInfo['state'] = uiConst.ITEM_NORMAL
                gemList.append(itemInfo)

        gemList.sort(cmp=self.sortGem)
        maxLv = -1
        maxLvGemPos = 0
        for index, itemInfo in enumerate(gemList):
            if itemInfo['gemLv'] > maxLv:
                item = p.inv.getQuickVal(*itemInfo['itemPos'])
                maxLv = itemInfo['gemLv']
                maxLvGemPos = index
                if itemInfo['state'] == uiConst.ITEM_NORMAL or not self.autoSelectedGemItemUuid:
                    self.autoSelectedGemItemUuid = item.uuid

        self.maxLvGemPos = maxLvGemPos
        return gemList

    def checkGemOrder(self, gemId, partId):
        p = BigWorld.player()
        return self.getWenYin().checkGemOrder(p.equipment, gemId, partId)

    def canAddGem(self, equpItem, item):
        p = BigWorld.player()
        for i in xrange(MAX_GEM_CNT):
            if equpItem._canAddGem(p, i, item, False, False):
                return True

        return False

    def sortGem(self, a, b):
        if a['state'] < b['state']:
            return -1
        if a['isAttProp'] and not b['isAttProp']:
            return -1
        if not a['isAttProp'] and b['isAttProp']:
            return 1
        if a['gemLv'] > b['gemLv']:
            return -1
        if a['gemLv'] < b['gemLv']:
            return 1
        if a['isBinded'] and not b['isBinded']:
            return -1
        if not a['isBinded'] and b['isBinded']:
            return 1
        return 0

    def getGemDetailInfo(self, gemSlot):
        info = {}
        equipItem = self.getSelectedPart()
        if not gemSlot:
            info['gemState'] = uiConst.GEM_SLOT_FILLED
        else:
            info['gemState'] = gemSlot.state
            if gemSlot.state == uiConst.GEM_SLOT_EMPTY:
                gemList = self.getGemList()
                info['gemList'] = gemList
            elif gemSlot.state == uiConst.GEM_SLOT_FILLED:
                lvUpInfo = self.getLvUpInfo(gemSlot)
                info['lvUpInfo'] = lvUpInfo
            elif gemSlot.state == uiConst.GEM_SLOT_LOCKED:
                info['unlockCost'] = self.getUnlockCost(equipItem)
        return info

    def getUnlockCost(self, item):
        itemId = item.id
        itemQuality = item.quality
        itemNum = 0
        cash = 0
        p = BigWorld.player()
        ed = ED.data.get(itemId, {})
        itemOrder = ed.get('order', 0)
        gemType = self.selectedGemPos[0]
        gemUnlockSlotData = EGUSD.data.get((itemQuality, itemOrder, gemType), {})
        itemNumCalc = gemUnlockSlotData.get('itemNum', [])
        cashCalc = gemUnlockSlotData.get('cash', [])
        if len(itemNumCalc) >= 2:
            if item:
                costRatio = ed.get('yangCostRatio', 1) if gemType == Item.GEM_TYPE_YANG else ed.get('yinCostRatio', 1)
                yangSlotsCnt = sum([ 1 for slot in getattr(item, 'yangSlots', ()) if not slot.isLocked() ])
                yinSlotsCnt = sum([ 1 for slot in getattr(item, 'yinSlots', ()) if not slot.isLocked() ])
                fvars = {'itemLv': item.itemLv,
                 'quality': itemQuality,
                 'p1': itemNumCalc[1],
                 'yangSlotsCnt': yangSlotsCnt,
                 'yinSlotsCnt': yinSlotsCnt}
                itemNum = int(round(commcalc._calcFormulaById(itemNumCalc[0], fvars) * costRatio))
        if len(cashCalc) > 2:
            cash = commcalc._calcFormulaById(cashCalc[0], cashCalc[1])
        costItemId = gemUnlockSlotData.get('itemId', 0)
        costInfo = {}
        costInfo['cash'] = cash
        costInfo['playerCash'] = p.cash
        costInfo['item'] = uiUtils.getGfxItemById(costItemId, 1, uiConst.ICON_SIZE64)
        ownNum = p.inv.countItemInPages(int(costItemId), enableParentCheck=True)
        if itemNum > ownNum:
            costInfo['itemCount'] = uiUtils.toHtml('%s/%s' % (ownNum, itemNum), COLOR_RED)
        else:
            costInfo['itemCount'] = '%s/%s' % (str(ownNum), str(itemNum))
        costInfo['showHelp'] = itemNum > ownNum
        costInfo['item']['count'] = costInfo['itemCount']
        costInfo['enableEquipDiKou'] = gameglobal.rds.configData.get('enableEquipDiKou', False)
        costInfo['selectedDiKou'] = self.enableDikou
        isEnough = True
        if costInfo['enableEquipDiKou'] and self.enableDikou:
            itemDict = {costItemId: itemNum}
            self.appendDiKouInfo(costInfo, itemDict)
            if not uiUtils.checkEquipMaterialDiKou(itemDict):
                isEnough = False
        else:
            if itemNum > ownNum:
                isEnough = False
            costInfo['yunchui'] = '%s/0' % format(p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID), ',')
        costInfo['isEnough'] = isEnough
        return costInfo

    def appendDiKouInfo(self, ret, itemDict):
        if itemDict != {}:
            p = BigWorld.player()
            _, yunchuiNeed, _, _ = utils.calcEquipMaterialDiKou(p, itemDict)
            yunchuiOwn = p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
            if yunchuiNeed > yunchuiOwn:
                ret['yunchui'] = '%s/%s' % (uiUtils.toHtml(format(yunchuiOwn, ','), COLOR_RED), format(yunchuiNeed, ','))
                ret['yunchuiEnabled'] = True
            else:
                ret['yunchui'] = '%s/%s' % (format(yunchuiOwn, ','), format(yunchuiNeed, ','))
                ret['yunchuiEnabled'] = False
            ret['diKouVisible'] = True
        else:
            ret['diKouVisible'] = False

    def getLvUpInfo(self, gemSlot):
        p = BigWorld.player()
        lvUpInfo = {}
        gemData = utils.getEquipGemData(gemSlot.gem.id)
        gemLv, gemType, gemSubType = gemData.get('lv', 0), gemData.get('type', 0), gemData.get('subType', 0)
        newGemId = EGID.data.get((gemLv + 1, gemType, gemSubType), None)
        isEnough = True
        if not newGemId:
            lvUpInfo['noNewGemId'] = True
            return lvUpInfo
        else:
            needNum = SCD.data.get('EquipGemRuneLvUpCount', 4) - 1
            mixItemNeed = EGD.data.get(newGemId, {}).get('mixItemNeed')
            self.bindMixItemConfirm = False
            self.mixItemId = mixItemNeed
            if mixItemNeed:
                needNum -= 1
                mixItemInfo = uiUtils.getGfxItemById(mixItemNeed)
                mixItemOwnCnt = p.inv.countItemInPages(mixItemNeed, enableParentCheck=True)
                mixItemBindCnt = p.inv.countItemInPages(mixItemNeed, enableParentCheck=True, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_ONLY)
                self.bindMixItemConfirm = mixItemBindCnt < 1
                str = '%d/%d' % (mixItemOwnCnt, 1)
                if mixItemOwnCnt < 1:
                    str = uiUtils.toHtml(str, COLOR_RED)
                    isEnough = isEnough and False
                mixItemInfo['count'] = str
                mixItemInfo['showHelp'] = mixItemOwnCnt < 1
                lvUpInfo['mixItemInfo'] = mixItemInfo
            parentId = gemSlot.gem.parentId(gemSlot.gem.id)
            needItemInfo = uiUtils.getGfxItemById(parentId)
            ownCnt = p.inv.countItemInPages(parentId, enableParentCheck=True, filterFunc=self.filterFun)
            bindCnt = p.inv.countItemInPages(parentId, enableParentCheck=True, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_ONLY, filterFunc=self.filterFun)
            self.bindItemConfirm = bindCnt < needNum
            str = '%d/%d' % (ownCnt, needNum)
            if ownCnt < needNum:
                str = uiUtils.toHtml(str, COLOR_RED)
                isEnough = isEnough and False
            needItemInfo['showHelp'] = ownCnt < needNum
            needItemInfo['count'] = str
            lvUpInfo['needItemInfo'] = needItemInfo
            lvUpInfo['isEnough'] = isEnough
            return lvUpInfo

    def filterFun(self, item):
        return item.ownedBy(BigWorld.player().gbId)

    def doGemClick(self, type, pos):
        type = int(type)
        pos = int(pos)
        if self.selectedGemPos[0] == type and self.selectedGemPos[1] == pos:
            return
        self.selectedGemPos = (type, pos)
        selectedPart = self.getSelectedPart()
        if not selectedPart:
            return
        gemSlot = selectedPart.getEquipGemSlot(type, pos)
        info = self.getGemDetailInfo(gemSlot)
        self.refreshGemDetail(info)

    def showInalyEff(self):
        if not self.widget:
            return
        if not self.widget.effect:
            return
        self.widget.effect.visible = True
        self.widget.effect.gotoAndPlay(1)

    def hideInalyEff(self):
        if not self.widget:
            return
        if not self.widget.effect:
            return
        self.widget.effect.visible = False

    def onYunChuiBtnClick(self, *arg):
        mall = gameglobal.rds.ui.tianyuMall
        if mall.mallMediator:
            mall.hide()
        mall.show(keyWord=gameStrings.EQUIP_CHANGE_GEM_PROXY_YUNCHUI)

    def onUnlockBtnClick(self, *args):
        self.doUnlockGem(self.selectedPart, self.getSelectedPart())

    def onLvUpBtnClick(self, *args):
        wenYinVal = self.getSelectedPart()
        if not self.IsAllSlotsFilled(wenYinVal):
            msg = GMD.data.get(GMDD.data.EQUIP_GEM_LVUP_CONFIM, {}).get('text', '')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, yesCallback=self.checkEquipOrder)
            return
        self.checkEquipOrder()

    def checkEquipOrder(self):
        item = self.getSelectedPart()
        gemSlot = item.getEquipGemSlot(*self.selectedGemPos)
        if not gemSlot:
            return
        gem = gemSlot.gem
        if not gem:
            return
        p = BigWorld.player()
        gemData = utils.getEquipGemData(gemSlot.gem.id)
        gemLv, gemType, gemSubType = gemData.get('lv'), gemData.get('type'), gemData.get('subType')
        newGemId = EGID.data.get((gemLv + 1, gemType, gemSubType))
        if not p.equipment[self.selectedPart]:
            partOrder = 0
        else:
            partOrder = p.equipment[self.selectedPart].addedOrder
        orderLimit = EGD.data.get(newGemId, {}).get('orderLimit', 0)
        if orderLimit > partOrder:
            msg = GMD.data.get(GMDD.data.EQUIP_CHANGE_GEM_CHECK_ORDER, {}).get('text', 'GMDD.data.EQUIP_CHANGE_GEM_CHECK_ORDER%s %d %d') % (uiUtils.getItemColorName(newGemId), orderLimit, partOrder)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, yesCallback=self.doItemGemLvUp)
        else:
            self.doItemGemLvUp()

    def doItemGemLvUp(self):
        item = self.getSelectedPart()
        gemSlot = item.getEquipGemSlot(*self.selectedGemPos)
        if not gemSlot:
            return
        gem = gemSlot.gem
        if not gem:
            return
        gemType, gemPos = self.selectedGemPos
        fun = Functor(self.sendUpgradeGemEquip, self.selectedPart, gemType, gemPos)
        checkFun = Functor(self.showMixItemBindCheck, fun)
        if self.bindItemConfirm:
            msg = GMD.data.get(GMDD.data.EQUIP_MIX_GEM_CHANGE_BIND_CONFIG, {}).get('text', '')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, yesCallback=checkFun)
        else:
            checkFun()

    def sendUpgradeGemEquip(self, part, gemType, gemPos):
        p = BigWorld.player()
        if not p:
            return
        self.needAutoSelect = True
        gamelog.info('jbx:upgradeWYGem', part, gemType, gemPos)
        if self.isSubMode:
            p.cell.upgradeWYGem(part, gemType, gemPos, False)
        else:
            p.cell.upgradeWYGem(part, gemType, gemPos, True)

    def showMixItemBindCheck(self, func):
        if not self.bindMixItemConfirm:
            func()
        else:
            msg = GMD.data.get(GMDD.data.EQUIP_MIX_GEM_CONSUME_UNBIND_CONFIG, {}).get('text', '%s') % utils.getItemName(self.mixItemId)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, func)

    @ui.checkEquipCanReturnByPos(const.LAST_PARAMS, GMDD.data.RETURN_BACK_UNLOCK_EQUIP_GEM)
    @ui.looseGroupTradeConfirm(const.LAST_PARAMS, GMDD.data.RETURN_BACK_UNLOCK_EQUIP_GEM)
    def doUnlockGem(self, partId, equipIt):
        if self.selectedGemPos[1] == -1:
            BigWorld.player().showGameMsg(GMDD.data.EQUIP_GEM_SLOT_CANNOT_UNLOCK, ())
            return
        p = BigWorld.player()
        if not equipIt:
            return
        if equipIt.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        ed = ED.data.get(equipIt.id, {})
        order = ed.get('order')
        unlockData = EGUSD.data.get((equipIt.quality, order, self.selectedGemPos[0]))
        if not unlockData:
            gamelog.error('cannot get unlock data', equipIt.id, equipIt.quality, order, self.selectedGemPos[0])
            return
        if not equipIt.isForeverBind():
            costItemId, costItemNumFormula = unlockData.get('itemId'), unlockData.get('itemNum')
            needBind = False
            if costItemId and costItemNumFormula:
                costRatio = ed.get('yangCostRatio', 1) if self.selectedGemPos[0] == Item.GEM_TYPE_YANG else ed.get('yinCostRatio', 1)
                yangSlotsCnt = sum([ 1 for slot in getattr(equipIt, 'yangSlots', ()) if not slot.isLocked() ])
                yinSlotsCnt = sum([ 1 for slot in getattr(equipIt, 'yinSlots', ()) if not slot.isLocked() ])
                fvars = {'itemLv': equipIt.itemLv,
                 'quality': equipIt.quality,
                 'p1': costItemNumFormula[1],
                 'yangSlotsCnt': yangSlotsCnt,
                 'yinSlotsCnt': yinSlotsCnt}
                costItemNum = int(round(commcalc._calcFormulaById(costItemNumFormula[0], fvars) * costRatio))
                if costItemNum:
                    removePlans = p.inv.canRemoveItemWithPlans(costItemId, costItemNum, enableParentCheck=True)
                    if removePlans:
                        needBind = any([ p.inv.getQuickVal(pg, pos).isForeverBind() for pg, pos, _ in removePlans ])
            if gameglobal.rds.configData.get('enableEquipDiKou', False):
                itemDict = {costItemId: costItemNum}
                _, yunchuiNeed, _, _ = utils.calcEquipMaterialDiKou(p, itemDict)
                if yunchuiNeed > 0:
                    msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_BIND_CONFIRM)
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=lambda : self.realUnlockGem(page, pos))
                    return
            if needBind:
                msg = GMD.data.get(GMDD.data.BIND_EQUIP_IF_UNLOCK, {}).get('text', gameStrings.TEXT_EQUIPCHANGEINLAYPROXY_1063)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.realUnlockGem, page, pos))
                return
        self.realUnlockGem(partId)

    def realUnlockGem(self, page, pos):
        self.showUnlockEff()
        ASUtils.callbackAtFrame(self.selectedGemMc.effect, 15, self.sendUnlockMsg)

    def sendUnlockMsg(self, *args):
        self.needAutoSelect = True
        BigWorld.player().cell.unlockEquipGemSlot(self.selectedPart[0], self.selectedPart[1], self.selectedPart[2], self.selectedGemPos[0], self.selectedGemPos[1])

    def showUnlockEff(self):
        if not self.widget:
            return
        if self.widget.currentFrameLabel != 'lock':
            return
        if not self.selectedGemMc:
            return
        if 'Lock' not in self.selectedGemMc.name or self.selectedGemMc.currentFrameLabel != 'lock':
            return
        self.selectedGemMc.effect.gotoAndPlay('unlock')

    def refreshAll(self, *args):
        if not self.widget:
            return
        if not self.widget.left:
            return
        BigWorld.player().fillGemToEquipments(False)
        info = self.getLeftListInfo(self.lastTabIdx)
        self.refreshLeftList(info)
        oldPos = copy.deepcopy(self.selectedPart)
        self.selectedPart = -1
        self.doLeftItemClick(oldPos)

    def autoSelected(self):
        item = self.getSelectedPart()
        if not item:
            return
        else:
            gemSlot = item.getEquipGemSlot(*self.selectedGemPos)
            if not gemSlot:
                return
            if self.selectedGemMc:
                if self.selectedGemMc.slot:
                    self.selectedGemMc.slot.setSlotState(uiConst.ITEM_NORMAL)
                else:
                    self.selectedGemMc.btn.selected = False
                self.selectedGemMc = None
            if self.selectedGemPos[0] == uiConst.GEM_TYPE_YANG:
                if gemSlot.state == uiConst.GEM_SLOT_FILLED:
                    self.selectedGemMc = self.widget.getChildByName('rightGem%d' % self.selectedGemPos[1])
                    self.selectedGemMc.slot.setSlotState(uiConst.ITEM_SELECTED)
                    if self.selectedGemMc.slot.data.state == uiConst.ITEM_GRAY:
                        ASUtils.setMcEffect(self.selectedGemMc.slot, 'gray')
                elif gemSlot.state == uiConst.GEM_SLOT_EMPTY:
                    self.selectedGemMc = self.widget.getChildByName('rightLock%d' % self.selectedGemPos[1])
                    self.selectedGemMc.btn.selected = True
                elif gemSlot.state == uiConst.GEM_SLOT_LOCKED:
                    self.selectedGemMc = self.widget.getChildByName('rightLock%d' % self.selectedGemPos[1])
                    self.selectedGemMc.btn.selected = True
            if self.selectedGemPos[0] == uiConst.GEM_TYPE_YIN:
                if gemSlot.state == uiConst.GEM_SLOT_FILLED:
                    self.selectedGemMc = self.widget.getChildByName('leftGem%d' % self.selectedGemPos[1])
                    self.selectedGemMc.slot.setSlotState(uiConst.ITEM_SELECTED)
                    if self.selectedGemMc.slot.data.state == uiConst.ITEM_GRAY:
                        ASUtils.setMcEffect(self.selectedGemMc.slot, 'gray')
                elif gemSlot.state == uiConst.GEM_SLOT_EMPTY:
                    self.selectedGemMc = self.widget.getChildByName('leftLock%d' % self.selectedGemPos[1])
                    self.selectedGemMc.btn.selected = True
                elif gemSlot.state == uiConst.GEM_SLOT_LOCKED:
                    self.selectedGemMc = self.widget.getChildByName('leftLock%d' % self.selectedGemPos[1])
                    self.selectedGemMc.btn.selected = True
            return

    def onGetToolTip(self, srcType):
        index = int(srcType.replace('equipChangeInlayV2', ''))
        if index < len(self.gemItemCache):
            item = self.gemItemCache[index]
            return gameglobal.rds.ui.inventory.GfxToolTip(item, location=const.ITEM_IN_BAG)

    def IsAllSlotsFilled(self, item):
        for i in xrange(MAX_GEM_CNT):
            gemSlot = item.getEquipGemSlot(uiConst.GEM_TYPE_YANG, i)
            if gemSlot and gemSlot.state != uiConst.GEM_SLOT_FILLED:
                return False
            gemSlot = item.getEquipGemSlot(uiConst.GEM_TYPE_YIN, i)
            if gemSlot and gemSlot.state != uiConst.GEM_SLOT_FILLED:
                return False

        return True

    def getAutoSelectedGemPos(self):
        item = self.getSelectedPart()
        if item:
            gemSlot = item.getEquipGemSlot(*self.selectedGemPos)
        else:
            gemSlot = None
        if not self.needAutoSelect and gemSlot:
            return self.selectedGemPos
        type = self.selectedGemPos[0]
        if self.selectedGemPos[0] < 1:
            type = uiConst.GEM_TYPE_YANG
        pos = -1
        minLv = 10
        minLvPos = -1
        minLvType = -1
        lockPos = -1
        lockType = -1
        for i in xrange(MAX_GEM_CNT):
            gemSlot = item.getEquipGemSlot(type, i)
            if gemSlot:
                if gemSlot.state == uiConst.GEM_SLOT_EMPTY:
                    pos = i
                    return (type, pos)
                if gemSlot.state == uiConst.GEM_SLOT_FILLED:
                    gemLv = EGD.data.get(gemSlot.gem.getParentId(), {}).get('lv', 100)
                    if gemLv < minLv:
                        minLv = gemLv
                        minLvPos = i
                        minLvType = type
                elif gemSlot.state == uiConst.GEM_SLOT_LOCKED and lockPos == -1:
                    lockPos = i
                    lockType = type

        type = type % 2 + 1
        for i in xrange(MAX_GEM_CNT):
            gemSlot = item.getEquipGemSlot(type, i)
            if gemSlot:
                if gemSlot.state == uiConst.GEM_SLOT_EMPTY:
                    pos = i
                    return (type, pos)
                if gemSlot.state == uiConst.GEM_SLOT_FILLED:
                    gemLv = EGD.data.get(gemSlot.gem.getParentId(), {}).get('lv', 100)
                    if gemLv < minLv:
                        minLv = gemLv
                        minLvPos = i
                        minLvType = type
                elif gemSlot.state == uiConst.GEM_SLOT_LOCKED and lockPos == -1:
                    lockPos = i
                    lockType = type

        if lockPos != -1:
            return (lockType, lockPos)
        elif minLvPos != -1:
            return (minLvType, minLvPos)
        else:
            return
