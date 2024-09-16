#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteFastSubmitProxy.o
import BigWorld
import uiConst
import events
import gameglobal
from uiProxy import UIProxy
from guis import uiUtils
from cdata import game_msg_def_data as GMDD

class SummonedWarSpriteFastSubmitProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteFastSubmitProxy, self).__init__(uiAdapter)
        self.widget = None
        self.checkOnceMap = {}
        self.checkOnceType = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_FAST_SUBMIT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_FAST_SUBMIT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_FAST_SUBMIT)

    def reset(self):
        pass

    def show(self, checkOnceType = None):
        self.checkOnceType = checkOnceType
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_FAST_SUBMIT, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.checkBox.addEventListener(events.EVENT_SELECT, self.onCheckBox, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.desc.text = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_EXPLORE_FAST_SUBMIT_DESC, '')

    def getCheckOnceData(self, type):
        return self.checkOnceMap.get(type, False)

    def onCheckBox(self, *arg):
        checkBoxSelect = self.widget.checkBox.selected
        if self.checkOnceType:
            self.checkOnceMap[self.checkOnceType] = checkBoxSelect

    def _onSureBtnClick(self, e):
        p = BigWorld.player()
        canSubmitItmes = gameglobal.rds.ui.summonedWarSpriteExplorePlan.getCanSubmitItems()
        p.base.exploreSpriteQuickCommitItem(canSubmitItmes)
        self.hide()

    def _onCancelBtnClick(self, e):
        self.hide()
