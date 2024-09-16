#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guanYinAddSkillProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import const
import gametypes
import gameconfigCommon
from uiProxy import UIProxy
from callbackHelper import Functor
from data import item_data as ID
from cdata import guanyin_book_data as GBD
from cdata import game_msg_def_data as GMDD

class GuanYinAddSkillProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuanYinAddSkillProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        self.slotIdx = -1
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUAN_YIN_ADD_SKILL, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUAN_YIN_ADD_SKILL:
            self.mediator = mediator
            self.refreshInfo()
        BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUAN_YIN_ADD_SKILL)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def reset(self):
        gameglobal.rds.ui.guanYin.updateEmptyState(self.slotIdx, False)
        self.slotIdx = -1

    def show(self, slotIdx):
        if gameconfigCommon.enableGuanYinThirdPhase():
            self.uiAdapter.guanYinAddSkillV3.show(slotIdx)
            return
        if self.slotIdx != -1:
            gameglobal.rds.ui.guanYin.updateEmptyState(self.slotIdx, False)
        self.slotIdx = slotIdx
        gameglobal.rds.ui.guanYin.updateEmptyState(self.slotIdx, True)
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUAN_YIN_ADD_SKILL)

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
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
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        equip = p.equipment[gametypes.EQU_PART_CAPE]
        if not equip:
            return
        if equip.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
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
        pskillList = equip.getAllGuanYinPskill()
        if pskillId in pskillList:
            if self.slotIdx == uiConst.SUPER_SKILL_SLOT_POS:
                p.showGameMsg(GMDD.data.GUAN_YIN_ADD_SUPER_SKILL_SAME_SKILL_HINT, ())
            else:
                p.showGameMsg(GMDD.data.GUAN_YIN_ADD_SKILL_SAME_SKILL_HINT, ())
            return
        if self.slotIdx == uiConst.SUPER_SKILL_SLOT_POS:
            self.realConfirm(kind, page, pos)
        elif not item.isForeverBind():
            msg = uiUtils.getTextFromGMD(GMDD.data.GUAN_YIN_ADD_SKILL_USE_UNBIND_HINT, gameStrings.TEXT_GUANYINADDSKILLPROXY_160)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.realConfirm, kind, page, pos))
        else:
            self.realConfirm(kind, page, pos)

    def realConfirm(self, kind, page, pos):
        p = BigWorld.player()
        if self.slotIdx == uiConst.SUPER_SKILL_SLOT_POS:
            p.cell.addGuanYinSuperPskill(const.RES_KIND_EQUIP, 0, gametypes.EQU_PART_CAPE, kind, page, pos)
        else:
            p.cell.addGuanYinPskill(const.RES_KIND_EQUIP, 0, gametypes.EQU_PART_CAPE, page, pos, self.slotIdx, 0)
        self.hide()

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            return True
        else:
            return False
