#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaPskillHoverProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import formula
from data import duel_config_data as DCD
from cdata import pskill_arena_temp_data as PATD
from cdata import pskill_temp_data as PTD
from uiProxy import UIProxy

class ArenaPskillHoverProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ArenaPskillHoverProxy, self).__init__(uiAdapter)
        self.widget = None
        self.pSkillData = None
        self.addEvent(events.EVENT_PLAYER_SPACE_NO_CHANGED, self.onSpaceNoChanged, 0, True)
        self.reset()

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ARENA_PSKILL_HOVER:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def onSpaceNoChanged(self):
        self.hide()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ARENA_PSKILL_HOVER)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ARENA_PSKILL_HOVER)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.tip.visible = True
        self.widget.adjustBtn.addEventListener(events.BUTTON_CLICK, self.toggleTip, False, 0, True)

    def openTip(self, *args):
        self.widget.tip.visible = True

    def hideTip(self, *args):
        self.widget.tip.visible = False

    def toggleTip(self, *args):
        self.widget.tip.visible = not self.widget.tip.visible

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.moveButtom(-self.widget.tip.content.textHeight)
        if formula.isBalanceAreanFb(formula.getFubenNo(p.spaceNo)):
            arenaPskillTip = DCD.data.get('arenaPskillTip', {})
            if arenaPskillTip:
                self.widget.tip.content.htmlText = arenaPskillTip.get(p.school, '')
            else:
                self.widget.tip.content.htmlText = ''
        else:
            tipText = self.generatePskillInfo()
            self.widget.tip.content.htmlText = tipText
        self.moveButtom(self.widget.tip.content.textHeight)

    def generatePskillInfo(self):
        tipText = ''
        if not self.pSkillData:
            return
        for pskill in self.pSkillData:
            desc = PTD.data.get(pskill, {}).get('desc', '')
            if desc:
                tipText += desc + '\n'

        return tipText

    def moveButtom(self, textHeight):
        tipMc = self.widget.tip
        needMoveMcs = (tipMc.line2, tipMc.tip, tipMc.tipIcon)
        for mcItem in needMoveMcs:
            mcItem.y = mcItem.y + textHeight

        tipMc.bg.height = tipMc.bg.height + textHeight

    def onGetArenaTempPskill(self, data):
        p = BigWorld.player()
        self.pSkillData = data
        if not self.needHide():
            if data:
                self.show()
        else:
            self.hide()

    def needHide(self):
        p = BigWorld.player()
        fubenNo = formula.getFubenNo(p.spaceNo)
        if fubenNo in (4111, 4112, 4113, 4116, 4117, 4118):
            return True
        return False
