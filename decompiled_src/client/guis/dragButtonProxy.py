#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/dragButtonProxy.o
from Scaleform import GfxValue
import gameglobal
import clientcom
from appSetting import Obj as AppSettings
from guis import uiConst
from uiProxy import UIProxy

class DragButtonProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DragButtonProxy, self).__init__(uiAdapter)
        self.modelMap = {'setDragType': self.onSetDragType,
         'openTutorial': self.onOpenTutorial,
         'closeTutorial': self.onCloseTutorial,
         'openFeedbackUrl': self.onOpenFeedbackUrl}
        self.isShow = False
        self.mediator = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DRAG_BUTTON:
            self.mediator = mediator
        self.mediator.Invoke('setVisible', GfxValue(False))

    def onSetDragType(self, *arg):
        dragType = arg[3][0]
        self.setDragType(dragType.GetBool())

    def dragHotKeyDown(self):
        dragAble = self.isDragAble()
        self.setDragType(not dragAble)
        if not dragAble:
            AppSettings.save()

    def setDragType(self, isDragAble):
        if not self.canDrag() and isDragAble:
            return
        self.mediator.Invoke('setDragAble', GfxValue(isDragAble))
        if isDragAble == False:
            gameglobal.rds.ui.actionbar.refreshAfterDragDisabled()
            self.uiAdapter.saveAllDragWidgetPos()
            self.uiAdapter.onSaveWidgetHidden()
            if gameglobal.rds.ui.dragTip.mediator:
                gameglobal.rds.ui.dragTip.hide()
        elif not gameglobal.rds.ui.dragTip.mediator:
            gameglobal.rds.ui.dragTip.show()

    def onOpenTutorial(self, *arg):
        if not self.isShow:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_NEW_GUIDER)
            self.isShow = True
        else:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_NEW_GUIDER)
            self.isShow = False

    def onCloseTutorial(self, *arg):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_NEW_GUIDER)
        self.isShow = False

    def onOpenFeedbackUrl(self, *arg):
        clientcom.openUrl(gameglobal.rds.ui.loginWin.userName)

    def canDrag(self):
        if self.mediator != None:
            return self.mediator.Invoke('isDragAvaliable').GetBool()
        else:
            return False

    def isDragAble(self):
        if self.mediator != None:
            return self.mediator.Invoke('isDragAble').GetBool()
        else:
            return False
