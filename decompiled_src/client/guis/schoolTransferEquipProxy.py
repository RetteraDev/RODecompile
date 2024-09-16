#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/schoolTransferEquipProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import events
import const
import uiUtils
import copy
import tipUtils
from uiProxy import UIProxy
from asObject import ASObject
from guis.asObject import TipManager
from data import equip_data as ED
from cdata import game_msg_def_data as GMDD

class SchoolTransferEquipProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SchoolTransferEquipProxy, self).__init__(uiAdapter)
        self.widget = None
        self.sType = 0
        self.selectedItemSlot = None
        self.oldItemTipRetMap = {}
        self.newItemTipRetMap = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_SCHOOL_TRANSFER_EQUIP, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SCHOOL_TRANSFER_EQUIP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCHOOL_TRANSFER_EQUIP)

    def reset(self):
        self.sType = 0
        self.selectedItemSlot = None
        self.oldItemTipRetMap = {}
        self.newItemTipRetMap = {}

    def hide(self, destroy = True):
        super(SchoolTransferEquipProxy, self).hide(destroy)
        if self.uiAdapter.funcNpc.isOnFuncState():
            self.uiAdapter.funcNpc.close()

    def show(self, sType):
        if not gameglobal.rds.configData.get('enableSchoolTransfer', False):
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.SCHOOL_TRANSFER_DISABLED, ())
            return
        if not self.widget:
            self.sType = sType
            self.uiAdapter.loadWidget(uiConst.WIDGET_SCHOOL_TRANSFER_EQUIP)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        if self.sType == 0:
            self.widget.title.textField.text = gameStrings.TEXT_SCHOOLTRANSFEREQUIPPROXY_65
            self.widget.hint.text = gameStrings.TEXT_SCHOOLTRANSFEREQUIPPROXY_66
            self.widget.emptyHint.text = gameStrings.TEXT_SCHOOLTRANSFEREQUIPPROXY_67
            self.widget.bg.gotoAndStop('equip')
        else:
            self.widget.title.textField.text = gameStrings.TEXT_SCHOOLTRANSFEREQUIPPROXY_70
            self.widget.hint.text = gameStrings.TEXT_SCHOOLTRANSFEREQUIPPROXY_71
            self.widget.emptyHint.text = gameStrings.TEXT_SCHOOLTRANSFEREQUIPPROXY_72
            self.widget.bg.gotoAndStop('other')
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            itemList = []
            for pg in p.inv.getPageTuple():
                for ps in p.inv.getPosTuple(pg):
                    item = p.inv.getQuickVal(pg, ps)
                    if item == const.CONT_EMPTY_VAL:
                        continue
                    if not item.isEquip():
                        continue
                    if self.sType == 0:
                        if item.isFashionEquip() or item.isRideEquip():
                            continue
                    elif not item.isFashionEquip() and not item.isRideEquip():
                        continue
                    schoolTransferInfo = getattr(item, 'schoolTransferInfo', None)
                    if not schoolTransferInfo:
                        continue
                    if schoolTransferInfo[0] != p.school:
                        continue
                    itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
                    if item.isLatchOfTime():
                        state = uiConst.ITEM_LATCH_TIME
                    elif hasattr(item, 'latchOfCipher'):
                        state = uiConst.ITEM_LATCH_CIPHER
                    else:
                        state = uiConst.ITEM_NORMAL
                    itemInfo['state'] = state
                    itemInfo['pos'] = (pg, ps)
                    itemList.append(itemInfo)

            self.widget.removeAllInst(self.widget.equipScrollWnd.canvas)
            self.selectedItemSlot = None
            posX = 0
            posY = 0
            itemLen = len(itemList)
            slotRowNum = itemLen / 4 + (1 if itemLen % 4 != 0 else 0)
            slotShowNum = max(slotRowNum * 4, 16)
            for i in xrange(slotShowNum):
                itemMc = self.widget.getInstByClsName('SchoolTransferEquip_ItemSlot')
                itemMc.selectedMc.visible = False
                if i < itemLen:
                    itemMc.slot.setItemSlotData(itemList[i])
                    itemMc.slot.dragable = False
                    itemMc.addEventListener(events.MOUSE_CLICK, self.handleClickItemSlot, False, 0, True)
                    if self.selectedItemSlot == None:
                        self.selectedItemSlot = itemMc
                else:
                    itemMc.slot.setItemSlotData(None)
                    itemMc.removeEventListener(events.MOUSE_CLICK, self.handleClickItemSlot)
                itemMc.x = posX
                itemMc.y = posY
                if i % 4 == 3:
                    posX = 0
                    posY += 56
                else:
                    posX += 56
                i += 1
                self.widget.equipScrollWnd.canvas.addChild(itemMc)

            self.widget.equipScrollWnd.refreshHeight()
            if self.selectedItemSlot:
                self.selectedItemSlot.selectedMc.visible = True
                self.widget.emptyHint.visible = False
            else:
                self.widget.emptyHint.visible = True
            self.refreshDetailInfo()
            return

    def refreshDetailInfo(self):
        if not self.widget:
            return
        else:
            self.widget.removeAllInst(self.widget.tipScrollWnd.canvas.oldTip, False)
            self.widget.removeAllInst(self.widget.tipScrollWnd.canvas.newTip, False)
            if not self.selectedItemSlot:
                self.widget.oldSchool.text = ''
                self.widget.newSchool.text = ''
                self.widget.tipScrollWnd.refreshHeight()
                self.widget.confirmBtn.enabled = False
                return
            p = BigWorld.player()
            page = int(self.selectedItemSlot.slot.data.pos[0])
            pos = int(self.selectedItemSlot.slot.data.pos[1])
            oldItem = p.inv.getQuickVal(page, pos)
            if not oldItem:
                return
            schoolTransferInfo = getattr(oldItem, 'schoolTransferInfo', None)
            self.widget.oldSchool.text = const.SCHOOL_DICT.get(schoolTransferInfo[1], '')
            self.widget.newSchool.text = const.SCHOOL_DICT.get(schoolTransferInfo[0], '')
            newItem = copy.deepcopy(oldItem)
            newItem.doEquipSchoolTransfer()
            newItem.bindType = oldItem.getSchoolTransferBindType()
            if not self.oldItemTipRetMap.has_key(oldItem.uuid):
                self.oldItemTipRetMap[oldItem.uuid] = tipUtils.formatRet(oldItem, location=const.ITEM_IN_BAG)
            oldItemTipRet = self.oldItemTipRetMap[oldItem.uuid]
            oldItemTipMc = TipManager.getItemTip(oldItemTipRet)
            oldItemTipMc.shift.visible = False
            oldItemTipMc.layOutvisibleLableList(False)
            if not self.newItemTipRetMap.has_key(newItem.uuid):
                self.newItemTipRetMap[newItem.uuid] = tipUtils.formatRet(newItem, location=const.ITEM_IN_NONE)
            newItemTipRet = self.newItemTipRetMap[newItem.uuid]
            newItemTipMc = TipManager.getItemTip(newItemTipRet)
            newItemTipMc.shift.visible = False
            newItemTipMc.layOutvisibleLableList(False)
            self.widget.tipScrollWnd.canvas.oldTip.addChild(oldItemTipMc)
            self.widget.tipScrollWnd.canvas.newTip.addChild(newItemTipMc)
            self.widget.tipScrollWnd.scrollbar.position = 0
            self.widget.tipScrollWnd.refreshHeight()
            self.widget.confirmBtn.enabled = True
            return

    def handleClickItemSlot(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.selectedMc.visible:
            return
        if self.selectedItemSlot:
            self.selectedItemSlot.selectedMc.visible = False
        self.selectedItemSlot = itemMc
        self.selectedItemSlot.selectedMc.visible = True
        self.refreshDetailInfo()

    def handleClickConfirmBtn(self, *args):
        if not self.selectedItemSlot:
            return
        else:
            p = BigWorld.player()
            page = int(self.selectedItemSlot.slot.data.pos[0])
            pos = int(self.selectedItemSlot.slot.data.pos[1])
            item = p.inv.getQuickVal(page, pos)
            if not item:
                return
            if item.hasLatch():
                BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                return
            showHint = False
            if gameglobal.rds.configData.get('enableUnbindEquip', False):
                configTimes = ED.data.get(item.id, {}).get('unbindTimes', 0)
                equipUnbindTimes = getattr(item, 'unbindTimes', None)
                if equipUnbindTimes:
                    if configTimes - equipUnbindTimes > 0:
                        showHint = True
                elif configTimes > 0:
                    showHint = True
            if showHint:
                msg = uiUtils.getTextFromGMD(GMDD.data.SCHOOL_TRANSFER_EQUIP_CLEAR_UNBINDTIMES, '')
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirm)
            else:
                self.trueConfirm()
            return

    def trueConfirm(self):
        page = int(self.selectedItemSlot.slot.data.pos[0])
        pos = int(self.selectedItemSlot.slot.data.pos[1])
        self.uiAdapter.schoolTransferEquipConfirm.show(page, pos)
