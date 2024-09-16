#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pubgKillAssistProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from asObject import ASUtils
from gameStrings import gameStrings
from guis.asObject import TipManager
KILL_ASSIST_MC_STOP_FRAME = 29

class PubgKillAssistProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PubgKillAssistProxy, self).__init__(uiAdapter)
        self.reset()

    def reset(self):
        self.widget = None
        self.killNum = 0
        self.assistNum = 0
        self.killMcDisappearCB = None
        self.assistMcDisappearCB = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PUBG_KILL_ASSIST_WIDGET:
            self.widget = widget
            self.initUI()
            self.refreshKillMc()
            self.refreshAssistMc()

    def initUI(self):
        self.widget.mouseEnabled = False
        self.widget.mouseChildren = False

    def clearWidget(self):
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PUBG_KILL_ASSIST_WIDGET)

    def showKill(self, num):
        self.killNum = num
        if not self.killNum:
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PUBG_KILL_ASSIST_WIDGET)
        else:
            self.refreshKillMc()

    def showAssist(self, num):
        self.assistNum = num
        if not self.assistNum:
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PUBG_KILL_ASSIST_WIDGET)
        else:
            self.refreshAssistMc()

    def refreshKillMc(self):
        if not self.widget:
            return
        killMc = self.widget.killMc
        killMc.stop()
        if self.killNum == 0:
            killMc.visible = False
        else:
            killMc.visible = True
            numFirst, numSecond = self.getNumFromEachDigit(self.killNum)
            numFirstMc = self.widget.getInstByClsName('PUBGKillAssist_killNums%d' % numFirst)
            numSecondMc = self.widget.getInstByClsName('PUBGKillAssist_killNums%d' % numSecond)
            killMc.num.first.removeChildAt(0)
            killMc.num.second.removeChildAt(0)
            numFirst and killMc.num.first.addChild(numFirstMc)
            killMc.num.second.addChild(numSecondMc)
            killMc.gotoAndPlay(1)
            self.killNum = 0
            self.killMcDisappearCB and ASUtils.cancelCallBack(self.killMcDisappearCB)
            self.killMcDisappearCB = ASUtils.callbackAtFrame(killMc, KILL_ASSIST_MC_STOP_FRAME, self._killMcDisapperCD)

    def _killMcDisapperCD(self, *arg):
        self.killMcDisappearCB = None
        if not self.widget:
            return
        else:
            killMc = self.widget.killMc
            killMc.stop()
            killMc.visible = False
            return

    def refreshAssistMc(self):
        if not self.widget:
            return
        assistMc = self.widget.assistMc
        assistMc.stop()
        if self.assistNum == 0:
            assistMc.visible = False
        else:
            assistMc.visible = True
            numFirst, numSecond = self.getNumFromEachDigit(self.assistNum)
            numFirstMc = self.widget.getInstByClsName('PUBGKillAssist_assistNums%d' % numFirst)
            numSecondMc = self.widget.getInstByClsName('PUBGKillAssist_assistNums%d' % numSecond)
            assistMc.num.first.removeChildAt(0)
            assistMc.num.second.removeChildAt(0)
            numFirst and assistMc.num.first.addChild(numFirstMc)
            assistMc.num.second.addChild(numSecondMc)
            assistMc.gotoAndPlay(1)
            self.assistNum = 0
            self.assistMcDisappearCB and ASUtils.cancelCallBack(self.assistMcDisappearCB)
            self.assistMcDisappearCB = ASUtils.callbackAtFrame(assistMc, KILL_ASSIST_MC_STOP_FRAME, self._assistMcDisapperCD)

    def _assistMcDisapperCD(self, *arg):
        self.assistMcDisappearCB = None
        if not self.widget:
            return
        else:
            assistMc = self.widget.assistMc
            assistMc.stop()
            assistMc.visible = False
            return

    def getNumFromEachDigit(self, num):
        if num <= 9:
            return (0, num)
        else:
            return (num // 10, num - num // 10 * 10)
