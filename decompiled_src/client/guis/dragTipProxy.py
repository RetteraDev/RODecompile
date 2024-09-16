#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/dragTipProxy.o
from gamestrings import gameStrings
import BigWorld
import uiConst
import uiUtils
import gameglobal
import gamelog
import gametypes
from uiProxy import UIProxy
from data import sys_config_data as SCD

class DragTipProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DragTipProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirmDrag': self.confirmDrag,
         'cancelDrag': self.onCancelDrag,
         'resetDrag': self.onResetDrag}
        self.destroyOnHide = True
        self.mediator = None
        self.dragFlag = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DRAG_TIP:
            self.mediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DRAG_TIP)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DRAG_TIP)
        self.mediator = None
        self.dragFlag = None

    def confirmDrag(self, *arg):
        self.uiAdapter.dragButton.dragHotKeyDown()

    def onCancelDrag(self, *arg):
        self.confirmCancel()

    def onResetDrag(self, *arg):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_DRAGTIPPROXY_46, self.confirmReset)

    def exitDrag(self):
        if self.dragFlag is None:
            self.dragFlag = gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_DRAGTIPPROXY_51, self.confirmCancel, noCallback=self.clearDragFlag)

    def confirmReset(self):
        if self.mediator:
            self.mediator.Invoke('confirmReset')
            self.hide()
            gameglobal.rds.ui.resetSavePosWidget()
            gameglobal.rds.ui.actionbar.validateSlotVisible()
            gameglobal.rds.ui.questTrack.resetWidgetUI()

    def confirmCancel(self):
        if self.mediator:
            self.mediator.Invoke('confirmCancel')
            self.hide()
            self.clearDragFlag()

    def clearDragFlag(self):
        self.dragFlag = None
