#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/disIndicatorProxy.o
import BigWorld
import gameglobal
import gamelog
import clientUtils
import gametypes
import clientcom
import events
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from asObject import ASUtils
from guis.asObject import TipManager
from gamestrings import gameStrings
SO_FAR_DIS = 999

class DisIndicatorProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DisIndicatorProxy, self).__init__(uiAdapter)
        self.widget = None
        self.updateCB = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_DISINDICATOR, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_DISINDICATOR:
            self.widget = widget
            self.initUI()

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DISINDICATOR)

    def clearWidget(self):
        if self.updateCB:
            BigWorld.cancelCallback(self.updateCB)
            self.updateCB = None
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DISINDICATOR)

    def reset(self):
        pass

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        pass

    def initState(self):
        self.refreshInfo()

    def refreshInfo(self):
        if self.hasBaseData():
            if self.updateCB:
                BigWorld.cancelCallback(self.updateCB)
                self.updateCB = None
            self.updateInfo()

    def updateInfo(self):
        if self.widget:
            p = BigWorld.player()
            if p.inGroupFollow:
                self.widget.content.text1.textField.text = self.getDistance()
                if self.widget.content.currentFrameLabel == 'end':
                    self.widget.content.text0.x = self.widget.content.text1.x + self.widget.content.text1.width - self.widget.content.text1.textField.textWidth - self.widget.content.text0.width - 5
                self.widget.content.text0.textMc.teamText.textField.text = gameStrings.GROUP_DIS_FOLLOW_BTN_TEXT_FOLLOW if p.isInTeam() else gameStrings.GROUP_DIS_FOLLOW_BTN_TEXT_FOLLOW_GROUP
            else:
                self.hide()
            self.updateCB = BigWorld.callback(0.1, self.updateInfo)

    def getDistance(self):
        p = BigWorld.player()
        headerPosition = p.clientGroupFollowInfo.get(gametypes.TEAM_SYNC_PROPERTY_POSITION, ())
        headerEnt = BigWorld.entity(p.groupHeader)
        if headerEnt:
            headerPosition = headerEnt.position
        elif p.delayGroupFollow:
            return gameStrings.DISINDICATOR_DELAY_FAR_TEXT
        headerSpaceNo = p.clientGroupFollowInfo.get(gametypes.TEAM_SYNC_PROPERTY_SPACENO, ())
        if p.spaceNo == headerSpaceNo:
            dirVector = p.position - headerPosition
            if dirVector.length > SO_FAR_DIS:
                return gameStrings.DISINDICATOR_SO_FAR_TEXT
            else:
                return str(int(dirVector.length))
        else:
            return gameStrings.DISINDICATOR_SO_FAR_TEXT

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False
