#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/challengePassportAppointProxy.o
import BigWorld
import gameglobal
import uiConst
from gamestrings import gameStrings
from guis import uiUtils
from guis import events
from guis.asObject import ASUtils
from guis.asObject import ASObject
from uiProxy import UIProxy

class ChallengePassportAppointProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChallengePassportAppointProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CHALLENGE_PASSPORT_APPOINT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHALLENGE_PASSPORT_APPOINT)

    def show(self):
        if not gameglobal.rds.configData.get('enableChallengePassport', False):
            return
        if not uiUtils.isInChallengePassport():
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CHALLENGE_PASSPORT_APPOINT, True)

    def initUI(self):
        self.widget.gotoAndPlay(0)
        ASUtils.callbackAtFrame(self.widget, 38, self.onFrameEnd)

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.season.visible = True
        season = uiUtils.getCurrentChallengePassportSeason()
        if season == -1:
            self.widget.season.txt.text = gameStrings.CHALLENGE_PASSPORT_SEASON_NEW
        else:
            self.widget.season.txt.text = gameStrings.CHALLENGE_PASSPORT_SEASON % uiUtils.convertIntToChn(season)

    def onFrameEnd(self, *args):
        BigWorld.callback(2.0, self.startBackplay)

    def onBackplayFinish(self):
        print 'ypc@ onBackplayFinish'
        self.uiAdapter.isStartRecodShowList = True
        self.hide()
        gameglobal.rds.ui.challengePassportAppoint2.show()
        self.uiAdapter.stopRecordShowList()

    def startBackplay(self):
        if not self.widget:
            return
        self.widget.addEventListener(events.EVENT_ENTER_FRAME, self.handleBackplay, False, 0, True)

    def handleBackplay(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if target.currentFrame > 1:
            target.gotoAndStop(target.currentFrame - 1)
        print 'ypc@ handleBackplay', target.currentFrame
        if target.currentFrame == 1:
            self.widget.removeEventListener(events.EVENT_ENTER_FRAME, self.handleBackplay)
            self.onBackplayFinish()
