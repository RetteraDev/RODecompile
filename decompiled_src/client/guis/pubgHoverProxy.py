#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pubgHoverProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import const
import gametypes
import pubgUtils
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis import uiUtils
from cdata import game_msg_def_data as GMDD
from gamestrings import gameStrings
from data import duel_config_data as DCD
from guis.asObject import Tweener
BUBBLE_HOR_PADDING = 7
BUBBLE_ORIGIN_HEIFGHT = 54
BUBBLE_MIN_WIDTH = 150

class PubgHoverProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PubgHoverProxy, self).__init__(uiAdapter)
        self.widget = None
        self.bubbleCallBack = None
        self.reset()

    def reset(self):
        if self.bubbleCallBack:
            BigWorld.cancelCallback(self.bubbleCallBack)
        self.bubbleCallBack = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PUBG_HOVER_WIDGET:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PUBG_HOVER_WIDGET)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PUBG_HOVER_WIDGET)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.guideBtn.addEventListener(events.BUTTON_CLICK, self.showGuide)
        self.widget.adjustMenu.visible = False
        self.widget.bubble.visible = False
        p = BigWorld.player()
        if p.canChangeTemplate():
            self.widget.adjustMenu.adjustSkillBtn.addEventListener(events.MOUSE_DOWN, self.openSkillWindow, False, 0, True)
            self.widget.adjustMenu.adjustPropBtn.addEventListener(events.MOUSE_DOWN, self.openPropWindow, False, 0, True)
            self.widget.adjustBtn.addEventListener(events.BUTTON_CLICK, self.showAdjustMenu)
            self.widget.adjustMenu.addEventListener(events.FOCUS_EVENT_FOCUS_OUT, self.hideAdjustMenu, False, 0, True)
        else:
            self.widget.adjustBtn.enabled = False
        self.widget.skillBtn.addEventListener(events.BUTTON_CLICK, self.openSkillPanel)
        self.widget.skillBtn.enabled = False

    def setAdjustBtnVisible(self, visible):
        if not self.widget:
            return
        self.widget.adjustBtn.enabled = visible

    def showAdjustMenu(self, *args):
        self.widget.adjustMenu.visible = True
        self.widget.adjustMenu.gotoAndPlay(1)
        self.widget.stage.focus = self.widget.adjustMenu

    def hideAdjustMenu(self, *args):
        e = ASObject(args[3][0])
        if not self.widget:
            return
        self.widget.adjustMenu.visible = False

    def openPropWindow(self, *args):
        gameglobal.rds.ui.roleInfo.show()

    def openSkillWindow(self, *args):
        gameglobal.rds.ui.skill.show()

    def showGuide(self, *args):
        gameglobal.rds.ui.baoDian.show(introType=uiConst.BAODIAN_TYPE_PUBG)

    def openSkillPanel(self, *args):
        gameglobal.rds.ui.pubgGeneralSkill.show()

    def refreshInfo(self):
        if not self.widget:
            return

    def showPubgGuildTip(self, tipType):
        if not self.widget:
            return
        pubgGuildTips = DCD.data.get('pubgGuildTips', [])
        if tipType:
            tipIndex = tipType - 1
            if tipIndex < len(pubgGuildTips):
                tipText, remainTime = pubgGuildTips[tipIndex]
                self.popBubble(tipText, remainTime)
        else:
            self.hideBubble()

    def popBubble(self, text, remainTime = 0):
        if not self.widget:
            return
        self.hideBubble()
        bubble = self.widget.bubble
        bubble.textField.htmlText = text
        textWidth = bubble.textField.textWidth
        bubble.textField.width = textWidth + BUBBLE_HOR_PADDING
        bubble.bg.width = max(BUBBLE_MIN_WIDTH, textWidth + BUBBLE_HOR_PADDING * 3)
        if remainTime:
            self.bubbleCallBack = BigWorld.callback(remainTime, self.hideBubble)
        bubble.visible = True
        Tweener.removeTweens()
        bubble.scaleX = 0.4
        bubble.scaleY = 0.4
        bubble.alpha = 0
        effect = {'alpha': 1,
         'time': 0.3,
         'transition': 'easeInOutCubic',
         'scaleY': 1.0,
         'scaleX': 1.0}
        Tweener.addTween(bubble, effect)

    def hideBubble(self):
        if self.bubbleCallBack:
            BigWorld.cancelCallback(self.bubbleCallBack)
        self.bubbleCallBack = None
        if not self.widget:
            return
        else:
            self.widget.bubble.visible = False
            return
