#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/voidDreamlandRuleProxy.o
import BigWorld
import gameglobal
import uiConst
import math
from uiProxy import UIProxy
from data import activity_desc_data as ADD
MAX_LINES_ONE_PAGE = 18

class VoidDreamlandRuleProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(VoidDreamlandRuleProxy, self).__init__(uiAdapter)
        self.widget = None
        self.totalPage = 1
        self.currPage = 1
        self.maxLinesAPage = -1
        self.soundIdx = -1
        uiAdapter.registerEscFunc(uiConst.WIDGET_VOID_DREAMLAND_RULE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_VOID_DREAMLAND_RULE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()
            gameglobal.rds.sound.playSound(gameglobal.SD_480)

    def show(self):
        if self.widget:
            self.refreshInfo()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_VOID_DREAMLAND_RULE)

    def clearWidget(self):
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_VOID_DREAMLAND_RULE)
        gameglobal.rds.sound.playSound(gameglobal.SD_481)

    def reset(self):
        self.totalPage = 1
        self.currPage = 1
        self.maxLinesAPage = -1
        self.soundIdx = -1

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        title = ADD.data.get(uiConst.DESC_VOID_DREAMLAND_RULE_ID, {}).get('title', '')
        details = ADD.data.get(uiConst.DESC_VOID_DREAMLAND_RULE_ID, {}).get('details', '')
        self.soundIdx = ADD.data.get(uiConst.DESC_VOID_DREAMLAND_RULE_ID, {}).get('backgroundSound', 0)
        self.widget.readBtn.gotoAndStop('play')
        self.widget.title.text = title
        self.widget.background.htmlText = details
        self.widget.background.mouseWheelEnabled = False
        numLines = self.widget.background.numLines
        self.maxLinesAPage = self.widget.background.getLineIndexAtPoint(0, self.widget.background.height)
        if self.maxLinesAPage == -1:
            self.maxLinesAPage = MAX_LINES_ONE_PAGE
        self.totalPage = max(int(math.ceil(numLines * 1.0 / self.maxLinesAPage)), 1)
        nullLines = max(self.maxLinesAPage * self.totalPage - numLines, 0)
        for i in range(nullLines):
            details = details + '\n'

        self.widget.background.htmlText = details
        self.currPage = 1
        self.updateBackgroundInfo()
        self.updatePageStepper()

    def _onPrevBtnClick(self, e):
        if self.currPage > 1:
            self.currPage = self.currPage - 1
            self.updateBackgroundInfo()
            self.updatePageStepper()
            gameglobal.rds.sound.playSound(gameglobal.SD_8)

    def _onNextBtnClick(self, e):
        if self.currPage < self.totalPage:
            self.currPage = self.currPage + 1
            self.updateBackgroundInfo()
            self.updatePageStepper()
            gameglobal.rds.sound.playSound(gameglobal.SD_8)

    def _onReadBeginBtnClick(self, e):
        self.widget.readBtn.gotoAndStop('stop')
        gameglobal.rds.sound.playSound(self.soundIdx)
        gameglobal.rds.sound.playSound(gameglobal.SD_8)

    def _onReadStopBtnClick(self, e):
        self.widget.readBtn.gotoAndStop('play')
        gameglobal.rds.sound.stopSound(self.soundIdx)
        gameglobal.rds.sound.playSound(gameglobal.SD_8)

    def updateBackgroundInfo(self):
        scrollTo = (self.currPage - 1) * self.maxLinesAPage + 1
        self.widget.background.scrollV = scrollTo

    def updatePageStepper(self):
        self.widget.pageControl.textField.text = '%d/%d' % (self.currPage, self.totalPage)
        self.widget.pageControl.prevBtn.enabled = self.currPage > 1 and self.totalPage != 1
        self.widget.pageControl.nextBtn.enabled = self.currPage < self.totalPage and self.totalPage != 1
