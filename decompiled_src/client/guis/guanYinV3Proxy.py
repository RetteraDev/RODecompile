#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guanYinV3Proxy.o
import BigWorld
import gameconfigCommon
import gameglobal
import uiConst
import uiUtils
import gametypes
import const
from uiProxy import UIProxy
from guis.asObject import TipManager
from guis import events
from guis.asObject import ASUtils
from guis.asObject import ASObject
from gamestrings import gameStrings
from data import sys_config_data as SCD
from cdata import guanyin_data as GD
from cdata import guanyin_book_data as GBD
from cdata import pskill_template_data as PSTD
from cdata import game_msg_def_data as GMDD
MAX_SLOT_NUM = 6
SUPER_SKILL_SLOT_POS = 5

class GuanYinV3Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuanYinV3Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUAN_YIN_V3, self.hide)

    def reset(self):
        self.isSubMode = False

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUAN_YIN_V3:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        if gameconfigCommon.enableSubGuanYin():
            self.widget.swtichBtn.visible = True
            self.widget.swtichBtn.addEventListener(events.BUTTON_CLICK, self.handleSwitchBtnClick, False, 0, True)
            self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick, False, 0, True)
        else:
            self.widget.swtichBtn.visible = False
        self.widget.cancelBtn.visible = False

    def handleSwitchBtnClick(self, *args):
        if self.isSubMode:
            BigWorld.player().cell.switchGuanYin()
        else:
            self.isSubMode = True
            self.refreshInfo()

    def handleCancelBtnClick(self, *args):
        self.isSubMode = False
        self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUAN_YIN_V3)

    def show(self):
        if self.widget:
            self.widget.swapPanelToFront()
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUAN_YIN_V3)

    def getRefreshInfo(self):
        info = {}
        p = BigWorld.player()
        equip = p.equipment[gametypes.EQU_PART_CAPE]
        gd = GD.data.get(equip.id if equip else 0, {})
        info['itemInfo'] = uiUtils.getGfxItem(equip, location=const.ITEM_IN_EQUIPMENT) if equip else {}
        pskillNum = gd.get('pskillNum', 0)
        skillList = []
        guanYin = p.guanYin
        for i in xrange(SUPER_SKILL_SLOT_POS):
            skillInfo = {}
            if self.isSubMode:
                bookId = p.subGuanYinInfo.get(i)
            else:
                guanYinSlotVal = guanYin.get(i)
                bookId = guanYinSlotVal.guanYinInfo[0]
            if bookId > 0:
                skillInfo = self.createSkillInfo(bookId)
                if guanYin.checkGuanYinPskillTimeOut(i, 0):
                    skillInfo['state'] = uiConst.SKILL_ICON_STAT_RED
                else:
                    skillInfo['state'] = uiConst.SKILL_ICON_STAT_USEABLE
                skillInfo['empty'] = False
            else:
                skillInfo['empty'] = True
            skillInfo['slotId'] = i
            skillInfo['isPre'] = i >= pskillNum
            skillList.append(skillInfo)

        info['skillList'] = skillList
        info['canEquipSuperSkill'] = gameglobal.rds.configData.get('enableGuanYinSuperSkill', False)
        if info['canEquipSuperSkill']:
            skillInfo = {}
            superSkillBook = guanYin.getSuperSkillBook()
            if superSkillBook and superSkillBook.checkGuanYinSuperSkill():
                skillInfo = self.createSkillInfo(superSkillBook.guanYinSuperBookId)
                skillInfo['empty'] = False
            else:
                skillInfo['empty'] = True
            skillInfo['isPre'] = not gd.get('canEquipSuperSkill', 0)
            skillInfo['slotId'] = SUPER_SKILL_SLOT_POS
            info['superSkill'] = skillInfo
        info['grayTipsList'] = SCD.data.get('guanYinGrayTipsList', ['',
         '',
         '',
         '',
         ''])
        return info

    def refreshInfo(self):
        if self.widget:
            p = BigWorld.player()
            info = self.getRefreshInfo()
            if not info:
                self.hide()
                return
            self.widget.cancelBtn.visible = self.isSubMode
            self.widget.swtichBtn.label = gameStrings.GUAN_YIN_V3_SUB_BTN if not self.isSubMode else gameStrings.GUAN_YIN_V3_REPLACE_BTN
            self.widget.item.setItemSlotData(info['itemInfo'])
            itemMc = None
            skillLen = len(info['skillList'])
            for i in xrange(MAX_SLOT_NUM):
                itemMc = getattr(self.widget, 'skillItem' + str(i))
                itemMc.slotIdx = i
                if i == SUPER_SKILL_SLOT_POS:
                    if info['canEquipSuperSkill']:
                        itemMc.visible = True
                        self.refreshSlot(itemMc, info['superSkill'], True)
                    else:
                        itemMc.visible = True
                        itemMc.removeBtn.visible = False
                        itemMc.gotoAndStop('empty')
                        itemMc.slot.setItemSlotData(None)
                        itemMc.slot.setSlotState(1)
                        itemMc.selectedEff.visible = False
                        itemMc.state.visible = True
                        itemMc.state.htmlText = gameStrings.GUAN_YIN_V3_CANT_ADD
                        itemMc.operatingState.visible = False
                        itemMc.slot.keyBind.visible = False
                        itemMc.addSuccessEff.visible = False
                        itemMc.removeSuccessEff.visible = False
                        itemMc.lvUpSuccessEff.visible = False
                else:
                    smallState = getattr(self.widget, 'smallState' + str(i))
                    isEmpty = info['skillList'][i]['empty']
                    isPre = info['skillList'][i]['isPre']
                    if not isEmpty:
                        if isPre:
                            smallState.gotoAndStop('noItem')
                        else:
                            smallState.gotoAndStop('normal')
                    elif isPre:
                        smallState.gotoAndStop('disable')
                    else:
                        smallState.gotoAndStop('empty')
                    if isPre:
                        itemMc.gotoAndStop('disable')
                    self.refreshSlot(itemMc, info['skillList'][i], False)
                    if not p.equipment[gametypes.EQU_PART_CAPE]:
                        smallState.gotoAndStop('noItem')

    def refreshSlot(self, itemMc, itemInfo, isSuperSkill):
        slotId = itemInfo['slotId']
        isPre = itemInfo['isPre']
        if itemInfo['empty']:
            itemMc.gotoAndStop('empty')
            itemMc.slot.setItemSlotData(None)
            itemMc.slot.setSlotState(1)
            itemMc.selectedEff.visible = False
            if self.uiAdapter.guanYinAddSkillV3.slotIdx == slotId:
                itemMc.state.visible = False
                itemMc.operatingState.visible = True
                itemMc.operatingState.text = gameStrings.GUAN_YIN_V3_ADD if not isPre else gameStrings.GUAN_YIN_V3_PRE_ADD
            else:
                itemMc.state.visible = True
                itemMc.state.htmlText = gameStrings.GUAN_YIN_V3_NOT_ADD if not isPre else gameStrings.GUAN_YIN_V3_NOT_PRE_ADD
                itemMc.operatingState.visible = False
            if isSuperSkill and isPre:
                itemMc.slot.removeEventListener(events.MOUSE_CLICK, self.handleAddSkill)
                itemMc.state.visible = True
                itemMc.operatingState.visible = False
                itemMc.state.htmlText = uiUtils.toHtml(gameStrings.GUAN_YIN_V3_CANT_ADD, '#B2B2B2')
            else:
                itemMc.slot.addEventListener(events.MOUSE_CLICK, self.handleAddSkill, False, 0, True)
        else:
            itemMc.gotoAndStop('normal')
            itemMc.slot.binding = 'skills20.' + str(itemInfo['bookId'])
            itemMc.slot.setItemSlotData(itemInfo)
            itemMc.slot.setSlotState(itemInfo.get('state', 0))
            itemMc.slot.dragable = False
            itemMc.slot.removeEventListener(events.MOUSE_CLICK, self.handleAddSkill)
            itemMc.skillLv.text = itemInfo['skillLv']
            itemMc.skillName.text = itemInfo['skillName']
            ASUtils.setHitTestDisable(itemMc.skillLv, True)
            if isSuperSkill:
                itemMc.removeBtn.enabled = not isPre
                itemMc.removeBtn.label = gameStrings.GUAN_YIN_V3_REPLACE
                itemMc.removeBtn.addEventListener(events.MOUSE_CLICK, self.handleAddSkill, False, 0, True)
            else:
                itemMc.removeBtn.label = gameStrings.GUAN_YIN_V3_REMOVE
                itemMc.removeBtn.addEventListener(events.MOUSE_CLICK, self.handleRemoveSkill, False, 0, True)
        ASUtils.setMcEffect(itemMc.slot, 'gray' if isPre else '')
        itemMc.empty = itemInfo['empty']
        itemMc.slot.keyBind.visible = False
        itemMc.addSuccessEff.visible = False
        itemMc.removeSuccessEff.visible = False
        itemMc.lvUpSuccessEff.visible = False
        if not isSuperSkill and itemInfo['empty']:
            TipManager.addTip(itemMc, gameStrings.GUAN_YIN_V3_VALID_LV % uiConst.GUAN_YIN_VALID_LV.get(slotId, 6))
        else:
            TipManager.removeTip(itemMc)

    def handleAddSkill(self, *args):
        e = ASObject(args[3][0])
        self.addSkill(e.currentTarget.parent.slotIdx)

    def handleRemoveSkill(self, *args):
        e = ASObject(args[3][0])
        self.removeSkill(e.currentTarget.parent.slotIdx)

    def handleLvUpSkill(self, *args):
        e = ASObject(args[3][0])
        set.lvUpSkill(e.currentTarget.parent.slotIdx)

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

    def addSkill(self, slotIdx):
        slotIdx = int(slotIdx)
        p = BigWorld.player()
        if slotIdx != uiConst.SUPER_SKILL_SLOT_POS and p._isSoul():
            p.showGameMsg(GMDD.data.GUAN_YIN_ADD_NORMAL_SKILL_FAIL_IN_CROSS, ())
            return
        gameglobal.rds.ui.guanYinAddSkillV3.show(slotIdx)

    def getBookId(self, slotIdx):
        p = BigWorld.player()
        guanYin = p.guanYin
        if not guanYin.validGuanYinPos(slotIdx, 0):
            return 0
        elif self.isSubMode:
            return p.subGuanYinInfo.get(slotIdx, 0)
        else:
            guanYinSlotVal = guanYin.get(slotIdx)
            bookId = guanYinSlotVal.guanYinInfo[0]
            return bookId

    def removeSkill(self, slotIdx):
        slotIdx = int(slotIdx)
        p = BigWorld.player()
        if gameglobal.rds.ui.guanYinAddSkillV3.widget:
            p.showGameMsg(GMDD.data.GUAN_YIN_TRANSFORM_PANEL_OPEN, ())
            return
        if p._isSoul():
            p.showGameMsg(GMDD.data.GUAN_YIN_REMOVE_SKILL_FAIL_IN_CROSS, ())
            return
        bookId = self.getBookId(slotIdx)
        if not bookId:
            return
        if self.isSubMode:
            p.cell.removeGuanYinInAlternative(slotIdx)
        else:
            p.cell.removeGuanYinPskillEx(slotIdx, 0)

    def lvUpSkill(self, slotIdx):
        slotIdx = int(slotIdx)
        p = BigWorld.player()
        if gameglobal.rds.ui.guanYinAddSkill.widget:
            p.showGameMsg(GMDD.data.GUAN_YIN_TRANSFORM_PANEL_OPEN, ())
            return
        if p._isSoul():
            p.showGameMsg(GMDD.data.WIDGET_IN_BLACK_LIST, ())
            return
        equip = p.equipment[gametypes.EQU_PART_CAPE]
        bookId = self.getBookId(slotIdx)
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
        if self.widget:
            info = {}
            info['slotIdx'] = slotIdx
            info['doing'] = doing
            if not getattr(self.widget, 'skillItem' + str(info['slotIdx']).empty):
                return
            if info['doing']:
                getattr(self.widget, 'skillItem' + str(info['slotIdx'])).selectedEff.visible = True
                getattr(self.widget, 'skillItem' + str(info['slotIdx'])).state.htmlText = "<font color=\'#E5C317\'>%s</font>" % gameStrings.GUAN_YIN_V3_ADD
            else:
                getattr(self.widget, 'skillItem' + str(info['slotIdx'])).selectedEff.visible = False
                getattr(self.widget, 'skillItem' + str(info['slotIdx'])).state.htmlText = "<font color=\'#73E539\'>%s</font>" % gameStrings.GUAN_YIN_V3_NOT_ADD

    def chechPanelOpen(self):
        if self.widget or self.uiAdapter.guanYinAddSkillV3.widget:
            return True
        return False

    def playAddSuccessEff(self, slotIdx, bookId):
        BigWorld.player().showGameMsg(GMDD.data.GUAN_YIN_ADD_SUCCESS, ())
        if self.widget:
            info = {}
            info['slotIdx'] = slotIdx
            info['iconPath'] = uiUtils.getItemIconFile64(bookId)
            itemMc = getattr(self.widget, 'skillItem' + str(info['slotIdx']))
            itemMc.addSuccessEff.visible = True
            itemMc.addSuccessEff.icon.fitSize = True
            itemMc.addSuccessEff.icon.loadImage(info['iconPath'])
            itemMc.addSuccessEff.gotoAndPlay(1)

    def playRemoveSuccessEff(self, slotIdx, bookId):
        if self.widget:
            info = {}
            info['slotIdx'] = slotIdx
            info['iconPath'] = uiUtils.getItemIconFile64(bookId)
            getattr(self.widget, 'skillItem' + str(info['slotIdx'])).removeSuccessEff.visible = True
            getattr(self.widget, 'skillItem' + str(info['slotIdx'])).removeSuccessEff.icon.fitSize = True
            getattr(self.widget, 'skillItem' + str(info['slotIdx'])).removeSuccessEff.icon.loadImage(info['iconPath'])
            getattr(self.widget, 'skillItem' + str(info['slotIdx'])).removeSuccessEff.gotoAndPlay(1)

    def playLvUpSuccessEff(self, slotIdx):
        if self.widget:
            info = {}
            info['slotIdx'] = slotIdx
            getattr(self.widget, 'skillItem' + str(info['slotIdx'])).lvUpSuccessEff.visible = True
            getattr(self.widget, 'skillItem' + str(info['slotIdx'])).lvUpSuccessEff.gotoAndPlay(1)
