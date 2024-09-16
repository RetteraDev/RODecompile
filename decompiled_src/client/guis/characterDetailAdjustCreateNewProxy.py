#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/characterDetailAdjustCreateNewProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from asObject import ASObject
from guis.asObject import TipManager
from gamestrings import gameStrings
from uiProxy import UIProxy

class CharacterDetailAdjustCreateNewProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CharacterDetailAdjustCreateNewProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_CREATE_NEW, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_CREATE_NEW:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_CREATE_NEW)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_CREATE_NEW)

    def initUI(self):
        self.widget.createBtn.addEventListener(events.BUTTON_CLICK, self.clickBtn, False, 0, True)
        self.widget.uploadBtn.addEventListener(events.BUTTON_CLICK, self.clickBtn, False, 0, True)
        self.widget.uploadBtn.visible = gameglobal.rds.ui.characterDetailAdjust.enableUpload()
        TipManager.addTip(self.widget.uploadBtn, gameStrings.CHARACTER_DETAIL_ADJUST_NEW_SHARE)
        btnName = gameglobal.rds.ui.characterDetailAdjust.getCreateBtnName()
        if btnName:
            self.widget.createBtn.label = btnName

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

    def clickBtn(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if target.name == 'createBtn':
            gameglobal.rds.ui.characterDetailAdjust.clickCreateCharacter()
        else:
            gameglobal.rds.ui.characterDetailAdjust.onClickUploadCharacter()

    def setUploadEnable(self, value):
        if not self.widget or not self.widget.uploadBtn:
            return
        self.widget.uploadBtn.enabled = value
