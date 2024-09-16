#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newServiceCelebrateProxy.o
import BigWorld
import events
import utils
import const
import commNewServerActivity
from uiProxy import UIProxy
from data import new_server_activity_data as NSAD
BG_IOCN_PATH = 'newServiceActivities/%d.dds'

class NewServiceCelebrateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NewServiceCelebrateProxy, self).__init__(uiAdapter)
        self.widget = None

    def reset(self):
        pass

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None

    def initUI(self):
        if not self.widget:
            return
        iconId = NSAD.data.get('celebrateBgIconId', 2001)
        iconPath = BG_IOCN_PATH % iconId
        self.widget.mainMc.fitSize = True
        self.widget.mainMc.loadImage(iconPath)
        self.widget.mainMc.addEventListener(events.MOUSE_CLICK, self.handleIconClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return

    def handleIconClick(self, *args):
        urlPath = NSAD.data.get('celebrateUrlPath', '')
        if not urlPath:
            return
        BigWorld.openUrl(urlPath)

    def canOpenTab(self):
        if not commNewServerActivity.isNewServerActivityOpen(const.NEW_SERVICE_EXP_BONUS):
            return False
        days = utils.getServerOpenDays() + 1
        dayLimit = NSAD.data.get('openServerCelebrateDayLimit', 7)
        if days > dayLimit:
            return False
        return True
