#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guanYinAddSkillV3Proxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import const
import gametypes
from uiProxy import UIProxy
from callbackHelper import Functor
from guis.asObject import ASObject
from guis.asObject import ASDict
from guis import events
from gamestrings import gameStrings
from data import item_data as ID
from cdata import guanyin_data as GD
from cdata import guanyin_book_data as GBD
from cdata import game_msg_def_data as GMDD

class GuanYinAddSkillV3Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuanYinAddSkillV3Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.slotIdx = -1
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUAN_YIN_ADD_V3, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUAN_YIN_ADD_V3:
            self.widget = widget
            self.widget.defaultCloseBtn = [widget.closeBtn, widget.cancelBtn]
            self.widget.selectedItem.dragable = False
            self.widget.selectedItem.valueAmount.visible = False
            self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.onConfirm, False, 0, True)
            self.refreshInfo()
        BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)

    def clearWidget(self):
        self.widget = None
        self.slotIdx = -1
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUAN_YIN_ADD_V3)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
        self.uiAdapter.guanYinV3.refreshInfo()

    def reset(self):
        self.selectedMc = None
        gameglobal.rds.ui.guanYin.updateEmptyState(self.slotIdx, False)
        self.slotIdx = -1

    def show(self, slotIdx):
        if self.slotIdx != -1:
            gameglobal.rds.ui.guanYin.updateEmptyState(self.slotIdx, False)
        self.slotIdx = slotIdx
        gameglobal.rds.ui.guanYin.updateEmptyState(self.slotIdx, True)
        if self.widget:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUAN_YIN_ADD_V3)

    def getRefreshInfo(self):
        info = {}
        p = BigWorld.player()
        if self.slotIdx == uiConst.SUPER_SKILL_SLOT_POS:
            info['title'] = gameStrings.TEXT_GUANYINADDSKILLPROXY_61
        else:
            info['title'] = gameStrings.TEXT_GUANYINADDSKILLPROXY_63
        if p._isSoul():
            kind = const.RES_KIND_CROSS_INV
            useInv = p.crossInv
        else:
            kind = const.RES_KIND_INV
            useInv = p.inv
        itemMap = {}
        for pg in useInv.getPageTuple():
            for ps in useInv.getPosTuple(pg):
                it = useInv.getQuickVal(pg, ps)
                if it == const.CONT_EMPTY_VAL:
                    continue
                if self.slotIdx == uiConst.SUPER_SKILL_SLOT_POS:
                    if not it.isGuanYinSuperSkillBook():
                        continue
                    schReq = ID.data.get(it.id, {}).get('schReq', [])
                    if schReq and p.school not in schReq:
                        continue
                elif not it.isGuanYinNormalSkillBook():
                    continue
                itemId = it.getParentId()
                if itemId in itemMap:
                    continue
                itemMap[itemId] = useInv.countItemInPages(itemId, enableParentCheck=True, includeLatch=True)

        itemList = []
        for itemId, itemNum in itemMap.iteritems():
            if itemNum <= 0:
                continue
            page, pos = useInv.findItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True, includeLatch=True)
            item = useInv.getQuickVal(page, pos)
            if item:
                if kind == const.RES_KIND_CROSS_INV:
                    itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_CROSS_BAG)
                else:
                    itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
            else:
                itemInfo = uiUtils.getGfxItemById(itemId)
            itemInfo['count'] = str(itemNum)
            itemInfo['colorName'] = uiUtils.getItemColorName(itemId)
            itemList.append(itemInfo)

        itemList.sort(key=lambda x: x['id'], reverse=True)
        info['itemList'] = itemList
        return ASDict(info)

    def refreshInfo(self):
        if self.widget:
            p = BigWorld.player()
            equip = p.equipment[gametypes.EQU_PART_CAPE]
            self.widget.tipsMc.visible = self.slotIdx < uiConst.SUPER_SKILL_SLOT_POS and GD.data.get(equip.id if equip else 0, {}).get('pskillNum', -1) <= self.slotIdx
            info = self.getRefreshInfo()
            if self.selectedMc:
                self.selectedMc.selectMc.visible = False
            self.selectedMc = None
            self.widget.title.text = info.title
            self.widget.selectedItem.setItemSlotData(None)
            self.widget.selectedItemName.htmlText = ''
            self.widget.removeAllInst(self.widget.bookScrollWnd.canvas, False)
            posX = 0
            posY = 0
            itemInfo = None
            itemMc = None
            itemLen = len(info.itemList)
            for i in xrange(itemLen):
                itemInfo = info.itemList[i]
                itemMc = self.widget.getInstByClsName('M12_InventorySlot')
                itemMc.setItemSlotData(itemInfo)
                itemMc.dragable = False
                itemMc.addEventListener(events.MOUSE_CLICK, self.handleSelectItem, False, 0, True)
                itemMc.x = posX
                itemMc.y = posY
                if i % 5 == 4:
                    posX = 0
                    posY += itemMc.height
                else:
                    posX += itemMc.width
                self.widget.bookScrollWnd.canvas.addChild(itemMc)

            self.widget.bookScrollWnd.refreshHeight()
            self.widget.confirmBtn.enabled = False
        self.uiAdapter.guanYinV3.refreshInfo()

    def onConfirm(self, *arg):
        itemId = int(self.selectedMc.data.id)
        p = BigWorld.player()
        if p._isSoul():
            kind = const.RES_KIND_CROSS_INV
            useInv = p.crossInv
        else:
            kind = const.RES_KIND_INV
            useInv = p.inv
        itemId = uiUtils.getParentId(itemId)
        page, pos = useInv.findItemInPages(itemId, enableParentCheck=True)
        item = useInv.getQuickVal(page, pos)
        if not item:
            page, pos = useInv.findItemInPages(itemId, enableParentCheck=True, includeLatch=True)
            item = useInv.getQuickVal(page, pos)
            if not item:
                return
        if item.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        pskillId = GBD.data.get(item.id, {}).get('pskillId', [])
        if len(pskillId) > 0:
            pskillId = pskillId[0]
        else:
            pskillId = 0
        pskillList = p.guanYin.getAllGuanYinPskill()
        if pskillId in pskillList:
            if self.slotIdx == uiConst.SUPER_SKILL_SLOT_POS:
                p.showGameMsg(GMDD.data.GUAN_YIN_ADD_SUPER_SKILL_SAME_SKILL_HINT, ())
            else:
                p.showGameMsg(GMDD.data.GUAN_YIN_ADD_SKILL_SAME_SKILL_HINT, ())
            return
        if self.slotIdx == uiConst.SUPER_SKILL_SLOT_POS:
            self.realConfirm(kind, page, pos, self.slotIdx)
        elif not item.isForeverBind():
            msg = uiUtils.getTextFromGMD(GMDD.data.GUAN_YIN_ADD_SKILL_USE_UNBIND_HINT, gameStrings.TEXT_GUANYINADDSKILLPROXY_160)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.realConfirm, kind, page, pos, self.slotIdx))
        else:
            self.realConfirm(kind, page, pos, self.slotIdx)

    def handleSelectItem(self, *args):
        e = ASObject(args[3][0])
        if self.selectedMc:
            self.selectedMc.selectMc.visible = False
        self.selectedMc = e.currentTarget
        self.selectedMc.selectMc.visible = True
        self.widget.selectedItem.setItemSlotData(self.selectedMc.data)
        self.widget.selectedItemName.htmlText = self.selectedMc.data.colorName
        self.widget.confirmBtn.enabled = True

    def realConfirm(self, kind, page, pos, slotIdx):
        p = BigWorld.player()
        if slotIdx == uiConst.SUPER_SKILL_SLOT_POS:
            if self.uiAdapter.guanYinV3.isSubMode:
                p.showGameMsg(GMDD.data.CAN_NOT_ADD_GUANYIN_SUPER_SKILL_IN_SUBMODE)
                return
            p.cell.addGuanYinSuperPskillEx(kind, page, pos)
        elif self.uiAdapter.guanYinV3.isSubMode:
            p.cell.addGuanYinInAlternative(page, pos, slotIdx)
        else:
            p.cell.addGuanYinPskillEx(page, pos, slotIdx, 0)
        self.hide()

    def isItemDisabled(self, kind, page, pos, item):
        if self.widget and kind == const.RES_KIND_INV:
            return True
        else:
            return False
