#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/skillMacroInputProxy.o
import BigWorld
import gameglobal
import gametypes
import uiUtils
import uiConst
import events
import copy
from guis import asObject
from guis import tipUtils
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from gameStrings import gameStrings
import skillMacro
from uiProxy import UIProxy
from data import skill_macro_command_data as SMCD
from data import skill_macro_arg_data as SMAD
TYPE_NUM = 4
MACRO_ITEM_OFFSET = 32
OVERVIEW_PANEL_WIDTH = 873
SKLL_MACRO_ICON_DICT = {0: 'skill/icon/%s.dds',
 1: 'item/icon/%s.dds',
 2: 'emote/%s.dds',
 3: 'skillMacroCommonIcon/%s.dds',
 4: 'skill/icon/%s.dds',
 uiConst.HORSE_RIDING: 'generalSkill/%s.dds',
 uiConst.WING_FLYING: 'generalSkill/%s.dds'}
SKILL_TYPE_LABEL_DICT = {0: gameStrings.SKILL_MACRO_TYPE_SKILL,
 1: gameStrings.SKILL_MACRO_TYPE_ITEM,
 2: gameStrings.SKILL_MACRO_TYPE_EMOTE,
 3: gameStrings.SKILL_MACRO_TYPE_CHAT}

class SkillMacroInputProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SkillMacroInputProxy, self).__init__(uiAdapter)
        self.macroInputData = []
        self.macroInputFilterData = []
        self.widget = None
        self.helpPicVisible = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_SKILL_MACRO_INPUT, self.clearWidget)

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initInputMacroPanel()
        self.initInputMacroLayout()

    def initInputMacroLayout(self):
        if gameglobal.rds.ui.skillMacroOverview.widget:
            x = gameglobal.rds.ui.skillMacroOverview.widget.x + OVERVIEW_PANEL_WIDTH
            y = gameglobal.rds.ui.skillMacroOverview.widget.y
            ASUtils.dragWidgetTo(self.widget, x, y)

    def initInputMacroPanel(self):
        self.initMacroInputData()
        self.widget.helpPic.visible = self.helpPicVisible
        for i in xrange(0, len(self.macroInputFilterData)):
            btn = self.widget.getChildByName('btn%d' % i)
            btn.addEventListener(events.MOUSE_CLICK, self.handleFilterBtnClick)

        if self.macroInputData and len(self.macroInputData[0]):
            self.widget.tip.visible = True
            self.widget.tip.tip.textField.text = gameStrings.SKILL_MACRO_INPUT_TIP
            self.widget.tip.tip.textField.width = self.widget.tip.tip.textField.textWidth
            self.widget.tip.tip.tipbg.width = self.widget.tip.tip.textField.textWidth + 15
            self.widget.tip.gotoAndPlay()
        self.setFilterIndex(0)
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def initMacroInputData(self):
        self.macroInputData = []
        self.macroInputFilterData = []
        for idx in xrange(0, TYPE_NUM):
            self.macroInputData.append([])
            self.macroInputFilterData.append({'label': SKILL_TYPE_LABEL_DICT[idx]})

        for id, macroItem in SMCD.data.iteritems():
            macroType = macroItem.get('subType', 0) if macroItem.get('subType', 0) else macroItem['type']
            if macroType == gametypes.MACRO_TYPE_SKILL:
                if macroItem.get('school', 0) != BigWorld.player().school:
                    continue
            item = copy.deepcopy(macroItem)
            item['id'] = id
            self.macroInputData[macroItem.get('type', 0)].append(item)

        for idx in xrange(0, len(self.macroInputData)):
            itemList = self.macroInputData[idx]
            itemList = sorted(itemList, cmp=lambda x, y: cmp(x['id'], y['id']))
            self.macroInputData[idx] = itemList

    def show(self, helpPicVisible = False, isForceShow = False):
        if self.widget:
            if not isForceShow:
                self.clearWidget()
        else:
            self.helpPicVisible = helpPicVisible
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SKILL_MACRO_INPUT)

    def handleFilterBtnClick(self, *args):
        targetBtn = ASObject(args[3][0]).currentTarget
        idx = int(targetBtn.name.replace('btn', ''))
        self.setFilterIndex(idx)
        self.widget.macroArea.refreshHeight()

    def handleFilterIndexChange(self, *args):
        idx = self.widget.filter.selectedIndex
        self.setFilterIndex(idx)
        self.widget.macroArea.refreshHeight()

    def setFilterIndex(self, idx):
        inputMacroList = self.macroInputData[idx]
        self.clearInputMacroArea()
        positionY = 0
        for item in inputMacroList:
            macroItem = self.widget.getInstByClsName('SkillMacroInput_Item')
            self.setMacroItem(macroItem, item)
            macroItem.y = positionY
            positionY += MACRO_ITEM_OFFSET
            self.widget.macroArea.canvas.addChild(macroItem)

    def setMacroItem(self, macroItem, item):
        macroItem.btn.label = item['describe']
        macroItem.icon.fitSize = True
        macroType = item.get('subType', 0) if item.get('subType', 0) else item['type']
        macroItem.icon.loadImage(SKLL_MACRO_ICON_DICT[macroType] % item['icon'])
        macroItem.btn.data = item['command']
        if macroType in (gametypes.MACRO_TYPE_SKILL,
         gametypes.MACRO_TYPE_ITEM,
         gametypes.MACRO_TYPE_EMOTE,
         uiConst.HORSE_RIDING,
         uiConst.WING_FLYING):
            itemId = self.getItemIdFromCommand(item['command'])
            if itemId:
                if macroType == gametypes.MACRO_TYPE_EMOTE:
                    TipManager.addItemTipById(macroItem.icon, itemId, True, 'upLeft', 'over', 'emote')
                elif macroType == gametypes.MACRO_TYPE_ITEM:
                    TipManager.addItemTipById(macroItem.icon, itemId, True)
                elif macroType == gametypes.MACRO_TYPE_SKILL or macroType == gametypes.MACRO_TYPE_SPRITE:
                    TipManager.addTipByType(macroItem.icon, tipUtils.TYPE_SKILL, itemId, True, 'upLeft')
                elif macroType in (uiConst.HORSE_RIDING, uiConst.WING_FLYING):
                    TipManager.addItemTipById(macroItem.icon, gameglobal.rds.ui.actionbar.otherSkill.get(itemId, 0), True, 'upLeft', 'over', 'otherSkill')
        macroItem.btn.addEventListener(events.MOUSE_CLICK, self.handleClickMacroItem)

    def getItemIdFromCommand(self, command):
        commandArgs = command.split(' ')
        for i in xrange(0, len(commandArgs)):
            if commandArgs[i].find('[') != -1:
                del commandArgs[i]
                break

        itemName = commandArgs[1]
        args = SMAD.data.get(itemName, {}).get('arg', [])
        if type(args) == list and len(args):
            return args[0]
        if type(args) != list:
            return args
        return 0

    def handleClickMacroItem(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        overviewPanel = gameglobal.rds.ui.skillMacroOverview.widget
        if overviewPanel:
            if not overviewPanel.createMacroT.visible:
                if not overviewPanel.inputArea.visible:
                    overviewPanel.noScriptT.visible = False
                    overviewPanel.inputArea.visible = True
                    overviewPanel.inputArea.canvas.inputT.text = target.data
                else:
                    macroCommands = overviewPanel.inputArea.canvas.inputT.text
                    if macroCommands:
                        index = overviewPanel.inputArea.canvas.inputT.textField.caretIndex
                        oldText = overviewPanel.inputArea.canvas.inputT.textField.text
                        if not index:
                            text = target.data
                            overviewPanel.inputArea.canvas.inputT.textField.text = '\n' + oldText
                        else:
                            text = '\n' + target.data
                        overviewPanel.inputArea.canvas.inputT.textField.replaceText(index, index, text)
                        length = len(text.decode('gbk'))
                        currentCaretIndex = index + length
                        overviewPanel.inputArea.canvas.inputT.textField.setSelection(currentCaretIndex, currentCaretIndex)
                    else:
                        macroCommands = target.data
                        overviewPanel.inputArea.canvas.inputT.text = macroCommands
                        currentCaretIndex = len(macroCommands.decode('gbk'))
                        overviewPanel.inputArea.canvas.inputT.validateNow()
                        overviewPanel.inputArea.canvas.inputT.textField.setSelection(currentCaretIndex, currentCaretIndex)
                    gameglobal.rds.ui.skillMacroOverview.hideErrorArea()

    def clearInputMacroArea(self):
        if self.widget:
            numChildren = self.widget.macroArea.canvas.numChildren
            for idx in xrange(0, numChildren):
                self.widget.macroArea.canvas.removeChildAt(0)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.helpPicVisible = False
        self.macroInputData = []
        self.macroInputFilterData = []
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SKILL_MACRO_INPUT)
