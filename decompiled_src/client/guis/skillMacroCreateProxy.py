#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/skillMacroCreateProxy.o
import BigWorld
import gameglobal
import gametypes
import uiUtils
import uiConst
import events
from guis import asObject
from guis.asObject import ASObject
from guis.asObject import ASUtils
from helpers import taboo
from gameStrings import gameStrings
from uiProxy import UIProxy
from data import skill_macro_icon_data as SMID
from data import skill_macro_command_data as SMCD
from cdata import game_msg_def_data as GMDD
OFFSET = 52
MAX_LINE_NUM = 5
SLOT_NAME = 'SkillMacroOverview_Slot'

class SkillMacroCreateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SkillMacroCreateProxy, self).__init__(uiAdapter)
        self.widget = None
        self.createIconPath = {}
        self.createMacroName = ''
        self.isModify = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_CREATE_SKILL_MACRO, self.clearWidget)

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initCreateMacroPanel()

    def openCreateSkillMacro(self, name = '', rawIcon = '', isModify = False):
        self.createMacroName = name
        self.createIconPath['rawIcon'] = rawIcon
        self.isModify = isModify
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CREATE_SKILL_MACRO, True)

    def initCreateMacroPanel(self):
        data = SMID.data
        p = BigWorld.player()
        idx = 0
        x = 0
        y = 0
        slotNum = 0
        for id, info in data.iteritems():
            data = {}
            data['rawIcon'] = info.get('icon', '')
            iconName = p.getIconNameFromRawIcon(data['rawIcon'])
            if info.get('school', 0):
                if p.school != info.get('school', 0):
                    continue
                data['iconType'] = uiConst.MACRO_SKILL_ICON_TYPE
                data['iconPath'] = uiConst.MACRO_SKILL_ICON % iconName
            else:
                data['iconType'] = uiConst.MACRO_COMMON_ICON_TYPE
                data['iconPath'] = uiConst.MACRO_COMMON_ICON % iconName
            slotNum += 1
            slot = self.widget.getInstByClsName(SLOT_NAME)
            slot.x = x
            slot.y = y
            if not slotNum % MAX_LINE_NUM:
                y += OFFSET
                x = 0
            else:
                x += OFFSET
            slot.name = 'slot%d' % idx
            slot.setItemSlotData(data)
            slot.dragable = False
            slot.addEventListener(events.MOUSE_CLICK, self.handleClickCreateIcon)
            self.widget.iconArea.canvas.addChild(slot)
            self.widget.iconArea.refreshHeight()
            idx += 1

        if self.isModify:
            self.selectMacroByRawIcon(self.createIconPath.get('rawIcon', ''))
        else:
            self.selectMacroByName('slot0')
        ASUtils.setHitTestDisable(self.widget.titlePic, True)
        if self.isModify:
            self.widget.titlePic.title.text = gameStrings.SKILL_MACRO_MODIFY_TITLE
        self.widget.macroName.text = self.createMacroName
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleConfirmCreateMacro)
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.cancelBtn.addEventListener(events.MOUSE_CLICK, self.handleClickCancelBtn)
        self.widget.macroName.focused = True

    def handleConfirmCreateMacro(self, *args):
        p = BigWorld.player()
        if gameglobal.rds.ui.skillMacroOverview.macroNum >= gametypes.MAX_SLOT_NUM and not self.isModify:
            p.showGameMsg(GMDD.data.SKILL_MACRO_FULL_TIP, ())
            return
        if not self.widget.macroName.text or not self.createIconPath:
            if not self.widget.macroName.text:
                p.showGameMsg(GMDD.data.SKILL_MACRO_NAME_NEED, ())
            if not self.createIconPath:
                p.showGameMsg(GMDD.data.SKILL_MACRO_ICON_NEED, ())
            return
        if gameglobal.rds.ui.skillMacroOverview.checkSelectedMacroChanged():
            selectMacroTxt = uiUtils.getTextFromGMD(GMDD.data.SKILL_MACRO_SELECTED_CHANGE_CONFIRM)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(selectMacroTxt, self.createMacro)
            return
        self.createMacro()

    def createMacro(self):
        macroName = self.widget.macroName.text
        isNormal, macroName = taboo.checkNameDisWordWithReplace(macroName)
        isNormal, macroName = taboo.checkPingBiWord(macroName)
        isNormal, macroName = taboo.checkTiHuanWord(macroName, False)
        isNormal, macroName = taboo.checkBSingle(macroName)
        overviewPanel = gameglobal.rds.ui.skillMacroOverview.widget
        if not overviewPanel:
            return
        gameglobal.rds.ui.skillMacroOverview.setEditVisible(True)
        skillMacroItem = overviewPanel.skillMacroItem
        data = {}
        if self.isModify:
            data = skillMacroItem.macroSlot.data
        else:
            data['macroList'] = []
            overviewPanel.noScriptT.visible = True
            overviewPanel.inputArea.visible = False
        data['macroName'] = macroName
        data['iconPath'] = self.createIconPath['iconPath']
        data['rawIcon'] = self.createIconPath['rawIcon']
        data['iconType'] = self.createIconPath['iconType']
        skillMacroItem.macroName.text = data['macroName']
        skillMacroItem.macroSlot.setItemSlotData(data)
        skillMacroItem.modifyName.addEventListener(events.MOUSE_CLICK, gameglobal.rds.ui.skillMacroOverview.handleModifySkillMacro)
        overviewPanel.inputBg.addEventListener(events.MOUSE_CLICK, gameglobal.rds.ui.skillMacroOverview.handleClickInput)
        if not self.isModify:
            gameglobal.rds.ui.skillMacroOverview.cancelSelectMacro()
        else:
            gameglobal.rds.ui.skillMacroOverview.editMode = uiConst.MODIFYING
        gameglobal.rds.ui.skillMacroOverview.saveMacro()
        self.clearWidget()

    def handleClickCreateIcon(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        self.selectMacroByName(target.name)

    def setCreateIconPathByData(self, data):
        self.createIconPath['iconPath'] = data.iconPath
        self.createIconPath['rawIcon'] = data.rawIcon
        self.createIconPath['iconType'] = data.iconType

    def selectMacroByName(self, name):
        for i in xrange(0, self.widget.iconArea.canvas.numChildren):
            slot = self.widget.iconArea.canvas.getChildByName('slot%d' % i)
            if name == slot.name:
                self.setCreateIconPathByData(slot.data)
                slot.setSlotState(uiConst.MACRO_SELECTED)
            else:
                slot.setSlotState(uiConst.MACRO_NORMAL)

    def selectMacroByRawIcon(self, rawIcon):
        for i in xrange(0, self.widget.iconArea.canvas.numChildren):
            slot = self.widget.iconArea.canvas.getChildByName('slot%d' % i)
            if slot.data and slot.data.rawIcon == rawIcon:
                self.setCreateIconPathByData(slot.data)
                slot.setSlotState(uiConst.MACRO_SELECTED)
            else:
                slot.setSlotState(uiConst.MACRO_NORMAL)

    def handleClickCancelBtn(self, *args):
        self.clearWidget()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.widget = None
        self.isModify = False
        self.createIconPath = {}
        self.createMacroName = ''
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CREATE_SKILL_MACRO)
