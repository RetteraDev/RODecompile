#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/guanYinSkillLvUpProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import gametypes
import const
from uiProxy import UIProxy
from cdata import guanyin_book_data as GBD
from cdata import pskill_template_data as PSTD
from cdata import game_msg_def_data as GMDD

class GuanYinSkillLvUpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuanYinSkillLvUpProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        self.slotIdx = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUAN_YIN_SKILL_LVUP, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUAN_YIN_SKILL_LVUP:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUAN_YIN_SKILL_LVUP)

    def reset(self):
        self.slotIdx = 0

    def show(self, slotIdx):
        self.slotIdx = slotIdx
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUAN_YIN_SKILL_LVUP)

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            equip = p.equipment[gametypes.EQU_PART_CAPE]
            if not equip:
                return
            if not equip.validGuanYinPos(self.slotIdx, 0):
                return
            bookId = equip.guanYinInfo[self.slotIdx][0]
            if not bookId:
                return
            info['bookId'] = bookId
            gpd = GBD.data.get(bookId, {})
            pskillId = gpd.get('pskillId', 0)
            pstd = PSTD.data.get(pskillId, {})
            info['skillInfo'] = {'iconPath': 'skill/icon/%d.dds' % pstd.get('icon', 0)}
            info['skillLv'] = 'Lv.%d' % gpd.get('lv', 0)
            info['skillName'] = pstd.get('sname', '')
            btnEnabled = True
            bookNeed = gpd.get('bookId', 0)
            info['bookNeed'] = bookNeed
            itemInfo = uiUtils.getGfxItemById(bookNeed)
            ownNum = p.inv.countItemInPages(bookNeed, enableParentCheck=True)
            needNum = 1
            if ownNum < needNum:
                itemInfo['count'] = "<font color = \'#F43804\'>%d/%d</font>" % (ownNum, needNum)
                btnEnabled = False
            else:
                itemInfo['count'] = '%d/%d' % (ownNum, needNum)
            info['itemInfo'] = itemInfo
            itemNeed = gpd.get('lvupItem')
            if itemNeed:
                itemId, needNum = itemNeed
                extraItemInfo = uiUtils.getGfxItemById(itemId)
                ownNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
                if ownNum < needNum:
                    extraItemInfo['count'] = "<font color = \'#F43804\'>%d/%d</font>" % (ownNum, needNum)
                    btnEnabled = False
                else:
                    extraItemInfo['count'] = '%d/%d' % (ownNum, needNum)
                info['extraItemInfo'] = extraItemInfo
                info['extraItemVisible'] = True
            else:
                info['extraItemVisible'] = False
            cashNeed = gpd.get('lvupCash', 0)
            if p.cash < cashNeed:
                cash = uiUtils.toHtml(format(cashNeed, ','), '#F43804')
                btnEnabled = False
            else:
                cash = format(cashNeed, ',')
            info['cash'] = cash
            info['btnEnabled'] = btnEnabled
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        bookNeed = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        equip = p.equipment[gametypes.EQU_PART_CAPE]
        if not equip:
            return
        if equip.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        ownBindNum = p.inv.countItemInPages(bookNeed, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_ONLY, enableParentCheck=True)
        if ownBindNum <= 0:
            msg = uiUtils.getTextFromGMD(GMDD.data.GUAN_YIN_SKILL_LV_UP_USE_UNBIND_HINT, '包裹内没有绑定技能书，将使用非绑技能书升级技能，确定要么？')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.realConfirm)
        else:
            self.realConfirm()

    def realConfirm(self):
        BigWorld.player().cell.guanYinPskillLvUpInEquip(const.RES_KIND_EQUIP, 0, gametypes.EQU_PART_CAPE, self.slotIdx, 0)
        self.hide()
