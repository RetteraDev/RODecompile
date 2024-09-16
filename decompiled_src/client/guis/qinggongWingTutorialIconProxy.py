#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/qinggongWingTutorialIconProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from data import sys_config_data as SCD

class QinggongWingTutorialIconProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QinggongWingTutorialIconProxy, self).__init__(uiAdapter)
        self.widget = None
        self.addEvent(events.EVENT_ROLE_SET_LV, self.pushIcon, isGlobal=True)
        self.reset()

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_QING_GONG_WING_TUTORIAL_ICON:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_QING_GONG_WING_TUTORIAL_ICON)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_QING_GONG_WING_TUTORIAL_ICON)

    def initUI(self):
        self.widget.iconBtn.addEventListener(events.MOUSE_CLICK, self.handleClickIconBtn, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return

    def handleClickIconBtn(self, *args):
        gameglobal.rds.ui.qinggongWingTutorial.show()

    def pushIcon(self, questId = 0):
        if not gameglobal.rds.configData.get('enableQinggongWingTutorialIcon', False):
            self.hide()
            return
        p = BigWorld.player()
        maxLevel = SCD.data.get('qinggongWingTutorialEnableLevel', {}).get('max', 0)
        if maxLevel and p.lv >= maxLevel:
            self.hide()
            return
        pushTaskID = SCD.data.get('qinggongWingTutorialPushTaskID', 0)
        if pushTaskID:
            if questId == pushTaskID:
                self.show()
            elif p.isQuestCompleted(pushTaskID):
                self.show()
