#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guanYinProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import gametypes
import const
import gameconfigCommon
from uiProxy import UIProxy
from callbackHelper import Functor
from data import sys_config_data as SCD
from cdata import guanyin_data as GD
from cdata import guanyin_book_data as GBD
from cdata import pskill_template_data as PSTD
from cdata import game_msg_def_data as GMDD

class GuanYinProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuanYinProxy, self).__init__(uiAdapter)
        self.modelMap = {'addSkill': self.onAddSkill,
         'removeSkill': self.onRemoveSkill,
         'lvUpSkill': self.onLvUpSkill}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUAN_YIN, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUAN_YIN:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUAN_YIN)

    def show(self):
        if gameconfigCommon.enableGuanYinThirdPhase():
            self.uiAdapter.guanYinV3.show()
            return
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUAN_YIN)

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            equip = p.equipment[gametypes.EQU_PART_CAPE]
            if not equip:
                self.hide()
                return
            gd = GD.data.get(equip.id, {})
            if not gd:
                return
            info['itemInfo'] = uiUtils.getGfxItem(equip, location=const.ITEM_IN_EQUIPMENT)
            pskillNum = gd.get('pskillNum', 0)
            skillList = []
            for i in xrange(pskillNum):
                if not equip.validGuanYinPos(i, 0):
                    continue
                skillInfo = {}
                bookId = equip.guanYinInfo[i][0]
                if bookId:
                    skillInfo = self.createSkillInfo(bookId)
                    if equip.checkGuanYinPskillTimeOut(i, 0):
                        skillInfo['state'] = uiConst.SKILL_ICON_STAT_RED
                    else:
                        skillInfo['state'] = uiConst.SKILL_ICON_STAT_USEABLE
                    skillInfo['empty'] = False
                else:
                    skillInfo['empty'] = True
                skillList.append(skillInfo)

            info['skillList'] = skillList
            info['canEquipSuperSkill'] = gd.get('canEquipSuperSkill', 0) and gameglobal.rds.configData.get('enableGuanYinSuperSkill', False)
            if info['canEquipSuperSkill']:
                skillInfo = {}
                if equip.checkGuanYinSuperSkill():
                    skillInfo = self.createSkillInfo(equip.guanYinSuperBookId)
                    skillInfo['empty'] = False
                else:
                    skillInfo['empty'] = True
                info['superSkill'] = skillInfo
            info['grayTipsList'] = SCD.data.get('guanYinGrayTipsList', ['',
             '',
             '',
             '',
             ''])
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def createSkillInfo(self, bookId):
        gpd = GBD.data.get(bookId, {})
        pskillId = gpd.get('pskillId', [])
        if len(pskillId) > 0:
            pskillId = pskillId[0]
        else:
            pskillId = 0
        pstd = PSTD.data.get(pskillId, {})
        skillInfo = {}
        skillInfo['bookId'] = bookId
        skillInfo['iconPath'] = 'skill/icon/%d.dds' % pstd.get('icon', 0)
        skillInfo['skillLv'] = ''
        skillInfo['skillName'] = pstd.get('sname', '')
        return skillInfo

    def onAddSkill(self, *arg):
        slotIdx = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if slotIdx != uiConst.SUPER_SKILL_SLOT_POS and p._isSoul():
            p.showGameMsg(GMDD.data.GUAN_YIN_ADD_NORMAL_SKILL_FAIL_IN_CROSS, ())
            return
        equip = p.equipment[gametypes.EQU_PART_CAPE]
        if not equip:
            return
        if equip.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        gameglobal.rds.ui.guanYinAddSkill.show(slotIdx)

    def onRemoveSkill(self, *arg):
        slotIdx = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if gameglobal.rds.ui.guanYinAddSkill.mediator:
            p.showGameMsg(GMDD.data.GUAN_YIN_TRANSFORM_PANEL_OPEN, ())
            return
        if p._isSoul():
            p.showGameMsg(GMDD.data.GUAN_YIN_REMOVE_SKILL_FAIL_IN_CROSS, ())
            return
        equip = p.equipment[gametypes.EQU_PART_CAPE]
        if not equip:
            return
        if equip.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        if not equip.validGuanYinPos(slotIdx, 0):
            return
        bookId = equip.guanYinInfo[slotIdx][0]
        if not bookId:
            return
        gpd = GBD.data.get(bookId, {})
        btnEnabled = True
        removeItem = gpd.get('removeItem')
        if removeItem:
            itemId, needNum = removeItem
            itemInfo = uiUtils.getGfxItemById(itemId)
            ownNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
            if ownNum < needNum:
                itemInfo['count'] = "<font color = \'#F43804\'>%d/%d</font>" % (ownNum, needNum)
                btnEnabled = False
            else:
                itemInfo['count'] = '%d/%d' % (ownNum, needNum)
        else:
            itemInfo = {}
        removeCash = gpd.get('removeCash', 0)
        if removeCash != 0:
            if p.cash < removeCash:
                cashVal = uiUtils.toHtml(format(removeCash, ','), '#F43804')
                btnEnabled = False
            else:
                cashVal = format(removeCash, ',')
            bonusInfo = {'bonusType': 'cash',
             'value': cashVal}
        else:
            bonusInfo = {}
        msg = uiUtils.getTextFromGMD(GMDD.data.GUAN_YIN_REMOVE_SKILL_HINT, '%s') % uiUtils.getItemColorName(bookId)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.removeGuanYinPskill, const.RES_KIND_EQUIP, 0, gametypes.EQU_PART_CAPE, slotIdx, 0), itemData=itemInfo, bonusIcon=bonusInfo, yesBtnEnable=btnEnabled)

    def onLvUpSkill(self, *arg):
        slotIdx = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if gameglobal.rds.ui.guanYinAddSkill.mediator:
            p.showGameMsg(GMDD.data.GUAN_YIN_TRANSFORM_PANEL_OPEN, ())
            return
        if p._isSoul():
            p.showGameMsg(GMDD.data.WIDGET_IN_BLACK_LIST, ())
            return
        equip = p.equipment[gametypes.EQU_PART_CAPE]
        if not equip:
            return
        if equip.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        if not equip.validGuanYinPos(slotIdx, 0):
            return
        bookId = equip.guanYinInfo[slotIdx][0]
        if not bookId:
            return
        if GBD.data.get(bookId, {}).get('lv', 0) >= GD.data.get(equip.id, {}).get('pskillMaxLv', 0):
            p.showGameMsg(GMDD.data.GUAN_YIN_SPKILL_LV_UP_LV, ())
            return
        bookNeed = GBD.data.get(bookId, {}).get('bookId', 0)
        if bookNeed != 0:
            pass
        else:
            p.showGameMsg(GMDD.data.GUAN_YIN_SPKILL_LV_UP_LV, ())

    def updateEmptyState(self, slotIdx, doing):
        if self.mediator:
            info = {}
            info['slotIdx'] = slotIdx
            info['doing'] = doing
            self.mediator.Invoke('updateEmptyState', uiUtils.dict2GfxDict(info, True))

    def chechPanelOpen(self):
        if self.mediator or gameglobal.rds.ui.guanYinAddSkill.mediator:
            return True
        return False

    def playAddSuccessEff(self, slotIdx, bookId):
        BigWorld.player().showGameMsg(GMDD.data.GUAN_YIN_ADD_SUCCESS, ())
        if self.mediator:
            info = {}
            info['slotIdx'] = slotIdx
            info['iconPath'] = uiUtils.getItemIconFile64(bookId)
            self.mediator.Invoke('playAddSuccessEff', uiUtils.dict2GfxDict(info, True))

    def playRemoveSuccessEff(self, slotIdx, bookId):
        if self.mediator:
            info = {}
            info['slotIdx'] = slotIdx
            info['iconPath'] = uiUtils.getItemIconFile64(bookId)
            self.mediator.Invoke('playRemoveSuccessEff', uiUtils.dict2GfxDict(info, True))

    def playLvUpSuccessEff(self, slotIdx):
        if self.mediator:
            info = {}
            info['slotIdx'] = slotIdx
            self.mediator.Invoke('playLvUpSuccessEff', uiUtils.dict2GfxDict(info, True))
