#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/characterDetailAdjustLookAtNewProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy

class CharacterDetailAdjustLookAtNewProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CharacterDetailAdjustLookAtNewProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_LOOKAT_NEW, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_LOOKAT_NEW:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_LOOKAT_NEW)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CHARACTER_DETAIL_ADJUST_LOOKAT_NEW)

    def initUI(self):
        value = gameglobal.rds.ui.characterDetailAdjust.getLookAtChoice()
        self.widget.lookAtCkbox.selected = value
        self.widget.lookAtCkbox.addEventListener(events.EVENT_SELECT, self.changeLookAtValue, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

    def changeLookAtValue(self, *args):
        gameglobal.rds.ui.characterDetailAdjust.setLookAtChoice(self.widget.lookAtCkbox.selected)
