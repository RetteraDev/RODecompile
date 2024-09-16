#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/schoolTransferEquipConfirmProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import events
import const
import uiUtils
from uiProxy import UIProxy
from data import equip_data as ED
from cdata import game_msg_def_data as GMDD

class SchoolTransferEquipConfirmProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SchoolTransferEquipConfirmProxy, self).__init__(uiAdapter)
        self.widget = None
        self.page = const.CONT_NO_PAGE
        self.pos = const.CONT_NO_POS
        uiAdapter.registerEscFunc(uiConst.WIDGET_SCHOOL_TRANSFER_EQUIP_CONFIRM, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SCHOOL_TRANSFER_EQUIP_CONFIRM:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCHOOL_TRANSFER_EQUIP_CONFIRM)

    def reset(self):
        self.page = const.CONT_NO_PAGE
        self.pos = const.CONT_NO_POS

    def show(self, page, pos):
        if not gameglobal.rds.configData.get('enableSchoolTransfer', False):
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.SCHOOL_TRANSFER_DISABLED, ())
            return
        if not self.widget:
            self.page = page
            self.pos = pos
            self.uiAdapter.loadWidget(uiConst.WIDGET_SCHOOL_TRANSFER_EQUIP_CONFIRM, isModal=True)

    def initUI(self):
        self.widget.defaultCloseBtn = [self.widget.closeBtn, self.widget.cancelBtn]
        self.widget.itemSlot.dragable = False
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            item = p.inv.getQuickVal(self.page, self.pos)
            if not item:
                return
            edData = ED.data.get(item.id, {})
            if not edData:
                return
            btnEnabled = True
            cashNeed = edData.get('schoolTransferEquipCash', 0)
            needCost = cashNeed > 0
            if p.cash + p.bindCash < cashNeed:
                self.widget.cash.htmlText = uiUtils.toHtml(format(cashNeed, ','), '#F43804')
                btnEnabled = False
            else:
                self.widget.cash.htmlText = format(cashNeed, ',')
            itemCost = edData.get('schoolTransferEquipItemCost', None)
            if itemCost:
                needCost = True
                for itemId, needNum in itemCost:
                    self.widget.itemSlot.setItemSlotData(uiUtils.getGfxItemById(itemId))
                    ownNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
                    if ownNum < needNum:
                        self.widget.itemNum.htmlText = '%s/%s' % (uiUtils.toHtml(format(ownNum, ','), '#F43804'), format(needNum, ','))
                        btnEnabled = False
                    else:
                        self.widget.itemNum.htmlText = '%s/%s' % (format(ownNum, ','), format(needNum, ','))
                    break

            else:
                self.widget.itemSlot.setItemSlotData(None)
                self.widget.itemNum.htmlText = gameStrings.TEXT_BATTLEFIELDPROXY_1605
            if needCost:
                self.widget.hint.htmlText = gameStrings.TEXT_SCHOOLTRANSFEREQUIPCONFIRMPROXY_96
                self.widget.hint.y = 61
                self.widget.line.visible = True
                self.widget.cashTitle.visible = True
                self.widget.cashIcon.visible = True
                self.widget.cash.visible = True
                self.widget.itemTitle.visible = True
                self.widget.itemSlot.visible = True
                self.widget.itemNum.visible = True
            else:
                self.widget.hint.htmlText = uiUtils.getTextFromGMD(GMDD.data.SCHOOLTRANSFER_EQUIP_NO_COST, '')
                self.widget.hint.y = 91
                self.widget.line.visible = False
                self.widget.cashTitle.visible = False
                self.widget.cashIcon.visible = False
                self.widget.cash.visible = False
                self.widget.itemTitle.visible = False
                self.widget.itemSlot.visible = False
                self.widget.itemNum.visible = False
            self.widget.confirmBtn.enabled = btnEnabled
            return

    def handleClickConfirmBtn(self, *args):
        p = BigWorld.player()
        item = p.inv.getQuickVal(self.page, self.pos)
        if not item:
            return
        edData = ED.data.get(item.id, {})
        if not edData:
            return
        cashNeed = edData.get('schoolTransferEquipCash', 0)
        if uiUtils.checkBindCashEnough(cashNeed, p.bindCash, p.cash, self.trueConfirm, True):
            self.trueConfirm()

    def trueConfirm(self):
        BigWorld.player().cell.beginEquipSchoolTransfer(self.page, self.pos)
        self.hide()
